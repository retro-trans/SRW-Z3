"""Synthetic and local read-only checks for the experimental Vita overlay."""
import hashlib
import json
from pathlib import Path
import struct
import sys
import unittest
from unittest import mock
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'platforms/vita'))
from font_gxt import FontPage, index_for_code
from text_codec import dictionary_for, encode, decode, segment
from build_test import patch_script, verify_script
import install_test
import luarec


def font_fixture():
    size = 4096 * 1120 // 2
    blob = bytearray(64 + size + 128)
    blob[:8] = b'GXT\0\x03\0\0\x10'
    struct.pack_into('<5I', blob, 8, 1, 64, size + 128, 2, 0)
    struct.pack_into('<6IHHI', blob, 32, 64, size, 0, 0, 0x60000000, 0x94000000, 4096, 1120, 1)
    for p in range(2):
        for i in range(16):
            blob[64 + size + p * 64 + i * 4:64 + size + p * 64 + i * 4 + 4] = bytes([255, 255, 255, i * 17])
    return bytes(blob)


class VitaBuildTests(unittest.TestCase):
    def test_codec_preserves_exact_text_and_controls(self):
        text = '\u300cHi, $n! \u300aA link\u300b\u300d\nNot shortened.'
        mapping = dictionary_for([text], list(range(0x8540, 0x85FD)))
        data, cells = encode(text, mapping)
        self.assertEqual(decode(data, mapping), text)
        self.assertIn(b'$n', data)
        self.assertEqual(len(cells), 2)

    def test_dynamic_segmentation_and_fallback(self):
        self.assertEqual(segment('abcd', {'a', 'b', 'c', 'd', 'ab', 'bc', 'cd'}), ['ab', 'cd'])
        self.assertEqual(segment('abc', {'a', 'b', 'c', 'bc'}), ['a', 'bc'])

    def test_missing_glyph_and_malformed_control_fail(self):
        with self.assertRaises(ValueError):
            encode('Unmapped', {})
        with self.assertRaises(ValueError):
            dictionary_for(['bad $1'], list(range(100)))

    def test_native_p4_nibble_order_and_metadata(self):
        original = font_fixture()
        page = FontPage(original)
        coverage = bytearray(1024)
        coverage[0], coverage[1] = 17, 238
        result = page.replace({0: coverage})
        self.assertEqual(result[64], 0xE1)
        self.assertEqual(result[:64], original[:64])
        self.assertEqual(result[-128:], original[-128:])
        self.assertEqual(FontPage(result).indices()[:2], bytes([1, 14]))
        changed = [i for i, (a, b) in enumerate(zip(result, original)) if a != b]
        self.assertEqual(changed, [64])

    def test_rejects_wrong_texture_format(self):
        data = bytearray(font_fixture())
        struct.pack_into('<I', data, 52, 0x95000000)
        with self.assertRaises(ValueError):
            FontPage(data)

    def test_dialogue_only_edits_and_wrong_source_refusal(self):
        source = 't_001 = {\r\n{WPos_B, 3, FDMode_Normal, pid_SIN, [[\u300cHi $n\u300d]]},\r\n};\r\nCmd_End();\r\n'.encode('cp932')
        rows = luarec.records(source.decode('cp932'))
        rows[0]['en'] = '\u300cHello $n\u300d'
        mapping = dictionary_for([rows[0]['en']], list(range(0x8540, 0x85FD)))
        patched, stats = patch_script(source, rows, mapping)
        verify_script(source, patched, rows, mapping)
        with self.assertRaises(ValueError):
            verify_script(source, patched.replace(b'Cmd_End', b'Cmd_Bad'), rows, mapping)
        rows[0]['sha'] = 'badstamp'
        with self.assertRaises(ValueError):
            patch_script(source, rows, mapping)

    def test_placeholder_removal_refused(self):
        source = 't_001 = {\r\n{WPos_B, 3, FDMode_Normal, pid_SIN, [[$n]]},\r\n};\r\n'.encode('cp932')
        rows = luarec.records(source.decode('cp932'))
        rows[0]['en'] = 'Hello'
        mapping = dictionary_for(['Hello'], list(range(0x8540, 0x85FD)))
        with self.assertRaises(ValueError):
            patch_script(source, rows, mapping)

    def test_vita_anchor_indices(self):
        self.assertEqual([index_for_code(c) for c in (0x8149, 0x824F, 0x8260, 0x8281)], [9, 207, 224, 257])

    def installer_fixture(self, root):
        game = root / 'ux0/app/PCSG00264'
        game.mkdir(parents=True)
        changes = []
        for n, name in enumerate(sorted(install_test.ALLOWED)):
            original, patched = ('original%d' % n).encode(), ('patched%d' % n).encode()
            dest, src = game / name, root / ('new%d' % n)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(original)
            src.write_bytes(patched)
            changes.append((name, src, dest, {'original_sha256': hashlib.sha256(original).hexdigest(),
                                             'patched_sha256': hashlib.sha256(patched).hexdigest()}))
        audit = {'build': 'synthetic', 'files': {c[0]: c[3] for c in changes}}
        return game, audit, changes

    def test_installer_dry_run_no_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            game, audit, changes = self.installer_fixture(root)
            with mock.patch.object(install_test, 'preflight', return_value=(game, audit, changes)):
                install_test.install(game, root, write=False)
            self.assertFalse((root / 'work').exists())
            for name, src, dest, info in changes:
                self.assertEqual(install_test.sha(dest), info['original_sha256'])

    def test_installer_running_emulator_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            game, audit, changes = self.installer_fixture(root)
            with mock.patch.object(install_test, 'preflight', return_value=(game, audit, changes)), \
                    mock.patch.object(install_test, 'running', return_value=True):
                with self.assertRaises(ValueError):
                    install_test.install(game, root, write=True)

    def test_installer_rolls_back_partial_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            game, audit, changes = self.installer_fixture(root)
            real_copy = install_test.shutil.copy2

            def copy(source, destination):
                if Path(source) == changes[1][1]:
                    Path(destination).write_bytes(b'partial failure')
                    raise OSError('synthetic failure')
                return real_copy(source, destination)

            with mock.patch.object(install_test, 'ROOT', root), \
                    mock.patch.object(install_test, 'preflight', return_value=(game, audit, changes)), \
                    mock.patch.object(install_test, 'running', return_value=False), \
                    mock.patch.object(install_test.shutil, 'copy2', side_effect=copy):
                with self.assertRaises(OSError):
                    install_test.install(game, root, write=True)
            for name, src, dest, info in changes:
                self.assertEqual(install_test.sha(dest), info['original_sha256'])
            self.assertEqual(len(list((root / 'work/vita/backups').glob('*/BACKUP.json'))), 1)


if __name__ == '__main__':
    unittest.main()
