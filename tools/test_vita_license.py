"""Synthetic identity checks; never accesses real license material."""
import importlib.util
import json
from pathlib import Path
import struct
import unittest

spec = importlib.util.spec_from_file_location("license_check", Path(__file__).resolve().parents[1] / "platforms/vita/validate_license.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class LicenseTests(unittest.TestCase):
    def fixture(self):
        cid = b"JP0700-PCSG00264_00-ABCDEFGHIJKLMNOP"
        pkg, rif = bytearray(128), bytearray(512)
        pkg[:4] = b"\x7fPKG"
        struct.pack_into(">Q", pkg, 0x18, 999)
        pkg[0x30:0x30 + len(cid)] = cid
        rif[0x10:0x10 + len(cid)] = cid
        struct.pack_into(">HHH", rif, 0, 1, 1, 1)
        struct.pack_into("<Q", rif, 8, 0x0123456789abcdef)
        rif[0x50:0x60] = b"PRIVATE_TEST_KEY"
        return pkg, rif

    def test_matching_and_secret_free(self):
        pkg, rif = self.fixture()
        report = mod.inspect(pkg, 999, rif)
        self.assertTrue(report["full_content_id_matches"])
        self.assertTrue(report["nonpdrm_account_marker"])
        self.assertTrue(report["license_key_present"])
        self.assertFalse(report["cryptographic_validity_verified"])
        self.assertNotIn("PRIVATE_TEST_KEY", json.dumps(report))
        self.assertNotIn(bytes(rif[0x50:0x60]).hex(), json.dumps(report))

    def test_different_full_content_id(self):
        pkg, rif = self.fixture()
        rif[0x10 + 20] = ord("Z")
        self.assertFalse(mod.inspect(pkg, 999, rif)["full_content_id_matches"])

    def test_invalid_size_and_magic(self):
        pkg, rif = self.fixture()
        with self.assertRaises(ValueError):
            mod.inspect(pkg, 999, rif[:-1])
        pkg[0] = 0
        with self.assertRaises(ValueError):
            mod.inspect(pkg, 999, rif)

    def test_missing_key_and_wrong_size(self):
        pkg, rif = self.fixture()
        rif[0x50:0x60] = bytes(16)
        report = mod.inspect(pkg, 998, rif)
        self.assertFalse(report["license_key_present"])
        self.assertFalse(report["pkg_size_matches_header"])

    def test_malformed_id_redacted(self):
        with self.assertRaisesRegex(ValueError, "value suppressed"):
            mod.content_id(b"DO_NOT_LOG_THIS")


if __name__ == "__main__":
    unittest.main()
