"""Synthetic executable/package safety checks; no real license in fixtures."""
import hashlib
import io
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zipfile
import zlib

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/vita'))
import self_decrypt as sd
import build_install_zip as package

FAKE_REFERENCE = '''
KeyType::METADATA, SceType::SELF, 5, "%s", "%s", 0x0, 0xFFFFFFFFFFFFFFFF, SelfType::APP
KeyType::NPDRM, SceType::SELF, 1, "%s", "%s", 0x0, 0xFFFFFFFFFFFFFFFF, SelfType::APP
''' % ('11' * 32, '33' * 16, '22' * 16, '00' * 16)
FAKE_LICENSE = b'fake-local-key!!'


def fixture():
    raw = b'test executable payload, not game data' * 4
    elf = struct.pack('<16sHHIIIIIHHHHHH', b'\x7fELF\1\1\1' + bytes(9),
                      0xfe04, 40, 1, 0x1000, 52, 0, 0x05000000, 52, 32, 1, 0, 0, 0)
    info = dict(elf=elf, elen=256+len(raw), ai=(1, 0, 8, 0, 0),
                phdrs=[(1, 256, 0x1000, 0, len(raw), len(raw), 5, 16)])
    plain = sd.make_fself(info, {0: raw})
    compressed = zlib.compress(raw)
    key, iv = b'K' * 16, b'I' * 16
    cipher = sd.AES.new(key, sd.AES.MODE_CTR, nonce=b'', initial_value=int.from_bytes(iv, 'big')).encrypt(compressed)
    out = bytearray(plain[:4096] + cipher)
    struct.pack_into('<H', out, 8, 0x0540)
    struct.pack_into('<Q', out, 32, len(out))
    sioff = struct.unpack_from('<Q', out, 88)[0]
    struct.pack_into('<4Q', out, sioff, 4096, len(cipher), 2, 1)
    metadata = bytearray(4096 - 0x630 - 64)
    struct.pack_into('<Q6I', metadata, 0, 0, 0, 1, 2, 0, 0, 0)
    struct.pack_into('<QQIiIiIiiI', metadata, 32, 4096, len(cipher), 2, 0, 1, 0, 3, 0, 1, 2)
    metadata[80:112] = key + iv
    mkey, miv = b'M' * 16, b'V' * 16
    minfo = mkey + bytes(16) + miv + bytes(16)
    wrapped = sd.AES.new(b'\x11' * 32, sd.AES.MODE_CBC, b'\x33' * 16).encrypt(minfo)
    pre = sd.AES.new(b'\x22' * 16, sd.AES.MODE_CBC, bytes(16)).decrypt(FAKE_LICENSE)
    out[0x630:0x670] = sd.AES.new(pre, sd.AES.MODE_CBC, bytes(16)).encrypt(wrapped)
    out[0x670:4096] = sd.AES.new(mkey, sd.AES.MODE_CBC, miv).encrypt(bytes(metadata))
    return bytes(out), raw, plain


class SelfTests(unittest.TestCase):
    def test_encrypted_to_plain_exact_roundtrip(self):
        source, raw, expected = fixture()
        output, audit = sd.convert(source, FAKE_LICENSE, FAKE_REFERENCE)
        self.assertEqual(output, expected)
        self.assertEqual(audit['segment_sha256'], [hashlib.sha256(raw).hexdigest()])
        self.assertTrue(audit['segment_bytes_preserved'])

    def test_wrong_key_rejected(self):
        source, _, _ = fixture()
        with self.assertRaisesRegex(ValueError, 'padding validation failed'):
            sd.convert(source, b'bad-license-key!', FAKE_REFERENCE)

    def test_truncated_payload_rejected(self):
        source, _, _ = fixture()
        with self.assertRaises(ValueError):
            sd.convert(source[:-1], FAKE_LICENSE, FAKE_REFERENCE)

    def test_corrupt_segment_rejected(self):
        source, _, _ = fixture()
        source = source[:-1] + bytes([source[-1] ^ 1])
        with self.assertRaises((ValueError, zlib.error)):
            sd.convert(source, FAKE_LICENSE, FAKE_REFERENCE)

    def test_unknown_revision_rejected(self):
        source, _, _ = fixture()
        source = source[:9] + b'\x7f' + source[10:]
        with self.assertRaisesRegex(ValueError, 'Unsupported key revision'):
            sd.convert(source, FAKE_LICENSE, FAKE_REFERENCE)

    def test_no_keys_in_audit(self):
        import json
        source, _, _ = fixture()
        output, audit = sd.convert(source, FAKE_LICENSE, FAKE_REFERENCE)
        self.assertNotIn(FAKE_LICENSE.decode(), json.dumps(audit))
        self.assertNotIn(FAKE_LICENSE, output)


class PackageTests(unittest.TestCase):
    def test_forbidden_names(self):
        for name in ('../x', '/root', 'C:/x', 'a\\b', 'a/../b',
                     'sce_sys/package/work.bin', 'sce_pfs/files.db', 'key.rif', 'work.bin'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                package.safe_name(name)

    def test_casing_preserved(self):
        name = 'DATA/tabata/TPACKVITA.cpk'
        self.assertEqual(package.safe_name(name), name)

    def test_zip_roundtrip_and_changed_hash_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.zip'
            data = b'fixture-only'
            inventory = {'sce_sys/param.sfo': dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())}
            package.write_zip(path, {'sce_sys/param.sfo': data}, inventory)
            package.verify_zip(path, inventory)
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(archive.namelist(), ['PCSG00264/sce_sys/param.sfo'])
            inventory['sce_sys/param.sfo']['sha256'] = '0' * 64
            with self.assertRaises(ValueError):
                package.verify_zip(path, inventory)

    def test_existing_and_external_output_rejected(self):
        for path in (sd.ROOT / 'work/vita', sd.ROOT, Path('C:/Windows/new-vita-build')):
            with self.assertRaises(ValueError):
                package.check_output(path)


if __name__ == '__main__':
    unittest.main()
