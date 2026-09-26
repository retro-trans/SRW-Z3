"""rePatch packaging tests; all executable/auth fixtures are synthetic."""
import io
from pathlib import Path
import struct
import sys
import tempfile
import unittest
from unittest import mock
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/vita'))
import build_repatch as R
import self_decrypt as S


def executable(flags=5, memsize=32):
    payload = b'X' * 32
    header = struct.pack('<16sHHIIIIIHHHHHH', b'\x7fELF\1\1\1' + bytes(9),
                         0xfe04, 40, 1, 0x1000, 52, 0, 0x05000000,
                         52, 32, 1, 0, 0, 0)
    info = dict(elf=header, elen=288, ai=(0x210000101cce0108, 0, 8, 0, 0),
                phdrs=[(1, 256, 0x1000, 0, 32, memsize, flags, 16)])
    return S.make_fself(info, {0: payload})


class RepatchTests(unittest.TestCase):
    def test_path_allowlist(self):
        for name in ('eboot.bin', 'self_auth.bin', 'DATA/BTLC/SRVC.BIN',
                     'CommonData/MtData/test.cpk'):
            self.assertEqual(R.payload_name(name), 'rePatch/PCSG00264/' + name)
        for name in ('../eboot.bin', 'DATA/../../foo.bin', 'DATA\\foo.bin',
                     '/eboot.bin', 'C:/eboot.bin', 'sce_sys/param.sfo',
                     'sce_module/libc.suprx', 'sce_sys/package/work.bin',
                     'DATA/license/a.bin', 'DATA/foo.rif', 'self_auth.bin/extra'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                R.payload_name(name)

    def test_select_only_changed_game_files(self):
        old = {'eboot.bin': R.blob_row(b'old'), 'DATA/a.cpk': R.blob_row(b'old'),
               'DATA/b.cpk': R.blob_row(b'unchanged'),
               'sce_module/libc.suprx': R.blob_row(b'encrypted'),
               'sce_sys/param.sfo': R.blob_row(b'metadata')}
        new = dict(old)
        new.update({'eboot.bin': R.blob_row(b'new'), 'DATA/a.cpk': R.blob_row(b'new'),
                    'sce_module/libc.suprx': R.blob_row(b'plain')})
        self.assertEqual(set(R.select_files(new, old)), {'eboot.bin', 'DATA/a.cpk'})
        new['sce_sys/param.sfo'] = R.blob_row(b'changed metadata')
        with self.assertRaises(ValueError):
            R.select_files(new, old)

    def test_inventory_mismatch_case_collision_and_missing_eboot(self):
        row = R.blob_row(b'old')
        with self.assertRaises(ValueError):
            R.select_files({'eboot.bin': row}, {})
        with self.assertRaises(ValueError):
            R.select_files({'eboot.bin': row}, {'eboot.bin': row})
        collision = {'eboot.bin': row, 'DATA/a.cpk': row, 'DATA/A.cpk': row}
        with self.assertRaises(ValueError):
            R.select_files(collision, collision)

    def test_plain_executable_and_unchanged_segment_audit(self):
        raw = executable()
        audit = R.inspect_eboot(raw)
        self.assertEqual(audit['authid'], 0x210000101cce0108)
        self.assertEqual(audit['segment_sha256'], [R.blob_row(b'X' * 32)['sha256']])
        with self.assertRaises(ValueError):
            R.inspect_eboot(raw[:-1])
        with self.assertRaises(ValueError):
            R.inspect_eboot(executable(flags=7))
        with self.assertRaises(ValueError):
            R.inspect_eboot(executable(memsize=31))
        damaged = bytearray(raw)
        damaged[0x700] = 1  # Unknown wrapper byte must not slip through.
        with self.assertRaises(ValueError):
            R.inspect_eboot(bytes(damaged))

    def test_auth_shape_and_authority_not_claimed_as_provenance(self):
        data = bytearray(144)
        struct.pack_into('<Q', data, 0, 123)
        data[16] = 1
        row = R.validate_auth(bytes(data), 123)
        self.assertEqual(row['bytes'], 144)
        self.assertIn('user must supply', row['validation'])
        for bad, authority in ((bytes(data[:-1]), 123), (bytes(data), 124),
                               (bytes(data[:16]) + bytes(128), 123),
                               (bytes(512), 123)):
            with self.assertRaises(ValueError):
                R.validate_auth(bad, authority)

    def test_missing_auth_refuses_without_explicit_staging_option(self):
        with mock.patch.object(R, 'check_output', return_value=Path('unused')):
            with self.assertRaisesRegex(ValueError, 'Supply --self-auth'):
                R.build(Path('unused'), write=True)

    def test_auth_sanitizer_preserves_only_consumed_fields(self):
        raw = bytearray(range(144))
        struct.pack_into('<Q', raw, 0, 123)
        original = bytes(raw)
        safe, row = R.sanitize_auth(raw, 123)
        self.assertEqual(bytes(raw), original)
        self.assertEqual(safe[:8], original[:8])
        self.assertEqual(safe[16:80], original[16:80])
        self.assertEqual(safe[8:16] + safe[80:], bytes(72))
        self.assertFalse(row['raw_auth_included'])
        self.assertEqual(row['sha256'], R.blob_row(safe)['sha256'])
        self.assertEqual(R.sanitize_auth(safe, 123)[0], safe)
        with self.assertRaises(ValueError):
            R.sanitize_auth(original, 124)

    def test_sanitized_auth_zip_roundtrip_and_raw_auth_rejected(self):
        raw = bytearray(range(144))
        struct.pack_into('<Q', raw, 0, 0x210000101cce0108)
        safe, _ = R.sanitize_auth(raw, 0x210000101cce0108)
        for label, auth in (('sanitized', safe), ('raw', bytes(raw))):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / 'test.zip'
                blobs = {R.payload_name('eboot.bin'): executable(),
                         R.payload_name('self_auth.bin'): auth}
                entries = {n: R.blob_row(b) for n, b in blobs.items()}
                with zipfile.ZipFile(str(path), 'x') as archive:
                    for name, data in blobs.items():
                        R.write_entry(archive, name, io.BytesIO(data), entries[name])
                if label == 'raw':
                    with self.assertRaisesRegex(ValueError, 'Unsanitized'):
                        R.verify(path, entries)
                else:
                    R.verify(path, entries)

    def test_sanitized_auth_with_wrong_executable_rejected(self):
        raw = bytearray(144)
        struct.pack_into('<Q', raw, 0, 123)
        raw[16] = 1
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'test.zip'
            blobs = {R.payload_name('eboot.bin'): executable(),
                     R.payload_name('self_auth.bin'): bytes(raw)}
            entries = {n: R.blob_row(b) for n, b in blobs.items()}
            with zipfile.ZipFile(str(path), 'x') as archive:
                for name, data in blobs.items():
                    R.write_entry(archive, name, io.BytesIO(data), entries[name])
            with self.assertRaisesRegex(ValueError, 'authority ID'):
                R.verify(path, entries)

    def test_zip_readback_hashes_and_extra_files(self):
        data = b'fixture payload'
        name = R.payload_name('DATA/a.cpk')
        entries = {name: R.blob_row(data)}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'test.zip'
            with zipfile.ZipFile(str(path), 'x') as archive:
                R.write_entry(archive, name, io.BytesIO(data), entries[name])
            R.verify(path, entries)
            with self.assertRaises(ValueError):
                R.verify(path, {name: R.blob_row(b'wrong')})
            with zipfile.ZipFile(str(path), 'a') as archive:
                archive.writestr('unexpected', b'x')
            with self.assertRaises(ValueError):
                R.verify(path, entries)

    def test_source_mismatch_during_write_is_rejected(self):
        with zipfile.ZipFile(io.BytesIO(), 'w') as archive:
            with self.assertRaises(ValueError):
                R.write_entry(archive, R.payload_name('eboot.bin'),
                              io.BytesIO(b'wrong'), R.blob_row(b'expected'))


if __name__ == '__main__':
    unittest.main()
