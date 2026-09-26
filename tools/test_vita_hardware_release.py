"""Synthetic offline hardware-applier regression checks; no private game data."""
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/vita'))
import apply_vita_hardware as h


def row(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def put(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)


def fixture(root):
    package, source, output = root / 'package', root / 'source', root / 'output'
    authid = 0x210000101CCE0108
    auth = bytearray(range(144))
    struct.pack_into('<Q', auth, 0, authid)
    put(root / 'private-auth.bin', bytes(auth))
    eboot = bytearray(0xA0)
    eboot[:4] = b'SCE\0'
    struct.pack_into('<Q', eboot, 0x38, 0x80)
    struct.pack_into('<Q', eboot, 0x80, authid)
    blobs = {'eboot.bin': bytes(eboot)}
    blobs.update({'DATA/fixture%03d.cpk' % i: ('new%d' % i).encode() for i in range(119)})
    records = {}
    for name, data in blobs.items():
        delta = 'patches/' + name + '.xdelta'
        put(source / name, b'old')
        put(package / delta, data)
        records[name] = dict(source=row(b'old'), target=row(data), patch=dict(name=delta, **row(data)))
    manifest = dict(schema=1, kind='vita-hardware-repatch-deltas', title_id='PCSG00264',
                    app_version='01.00', program_authority_id=authid, files=records)
    put(package / 'manifest.json', json.dumps(manifest).encode())
    put(package / 'README.md', b'Synthetic instructions')
    return package, source, output, root / 'private-auth.bin', blobs


def decode_stub(command, check):
    # Synthetic tests focus on applier orchestration and failure guards.
    # Production release validation separately runs the real xdelta executable.
    shutil.copyfile(command[-2], command[-1])


class HardwareReleaseTests(unittest.TestCase):
    def test_dry_run_and_full_overlay_auth_sanitization(self):
        with tempfile.TemporaryDirectory() as tmp:
            package, source, output, auth, blobs = fixture(Path(tmp))
            original_auth = auth.read_bytes()
            with patch.object(h.subprocess, 'run', side_effect=decode_stub) as decoder:
                h.apply(package, source, output, auth, 'fake-xdelta')
                decoder.assert_not_called()
                self.assertFalse(output.exists())
                report = h.apply(package, source, output, auth, 'fake-xdelta', True)
                self.assertEqual(decoder.call_count, 120)
            self.assertEqual(auth.read_bytes(), original_auth)
            self.assertEqual(report['status'], 'hardware_test_candidate')
            self.assertFalse(report['physical_vita_tested'])
            self.assertEqual(report['missing_files'], [])
            self.assertEqual(len(report['files']), 121)
            for name, data in blobs.items():
                self.assertEqual((source / name).read_bytes(), b'old')
                self.assertEqual((output / 'rePatch/PCSG00264' / name).read_bytes(), data)
            sanitized = (output / 'rePatch/PCSG00264/self_auth.bin').read_bytes()
            self.assertEqual(sanitized[:8], original_auth[:8])
            self.assertEqual(sanitized[16:80], original_auth[16:80])
            self.assertEqual(sanitized[8:16] + sanitized[80:], bytes(72))
            with zipfile.ZipFile(output / 'SRW-Z3-Vita-rePatch-0.6.14-hardware-test.zip') as archive:
                self.assertEqual(len(archive.namelist()), 123)
                self.assertIsNone(archive.testzip())
                self.assertEqual(archive.read('rePatch/PCSG00264/self_auth.bin'), sanitized)

    def test_missing_bad_auth_or_source_never_writes(self):
        for defect in ('missing_auth', 'bad_auth', 'bad_source', 'bad_delta'):
            with self.subTest(defect=defect), tempfile.TemporaryDirectory() as tmp:
                package, source, output, auth, _ = fixture(Path(tmp))
                if defect == 'missing_auth':
                    auth = auth.with_name('missing.bin')
                elif defect == 'bad_auth':
                    auth.write_bytes(bytes(144))
                elif defect == 'bad_source':
                    (source / 'eboot.bin').write_bytes(b'wrong')
                else:
                    (package / 'patches/eboot.bin.xdelta').write_bytes(b'wrong')
                with self.assertRaises((ValueError, OSError)):
                    h.apply(package, source, output, auth, 'unused', True)
                self.assertFalse(output.exists())

    def test_output_isolation_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            package, source, output, auth, _ = fixture(Path(tmp))
            for bad in (source, source / 'new', package / 'new', source.parent):
                with self.subTest(path=bad), self.assertRaises(ValueError):
                    h.apply(package, source, bad, auth, 'unused', True)

    def test_module_auth_and_unsafe_payload_paths_rejected(self):
        for name in ('sce_module/libc.suprx', 'sce_sys/param.sfo', 'self_auth.bin',
                     '../eboot.bin', '/eboot.bin', 'DATA/../../escape.bin'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                h.allowed(name)

    def test_wrong_decoder_output_cannot_get_success_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            package, source, output, auth, _ = fixture(Path(tmp))
            with patch.object(h.subprocess, 'run', side_effect=lambda cmd, check: Path(cmd[-1]).write_bytes(b'bad')):
                with self.assertRaisesRegex(ValueError, 'Output mismatch'):
                    h.apply(package, source, output, auth, 'fake-xdelta', True)
            self.assertFalse((output / 'FILES.json').exists())
            self.assertFalse((output / 'SRW-Z3-Vita-rePatch-0.6.14-hardware-test.zip').exists())


if __name__ == '__main__':
    unittest.main()
