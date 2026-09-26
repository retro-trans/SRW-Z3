"""Synthetic packaging checks; no game files or emulator required."""
import importlib.util
import hashlib
import io
from pathlib import Path
import struct
import tempfile
import unittest
import pycdlib

spec = importlib.util.spec_from_file_location("cfw", Path(__file__).resolve().parents[1] / "platforms/ps3/cfw_package.py")
cfw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cfw)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def image(self):
        path = self.root / "sample.iso"
        iso = pycdlib.PyCdlib()
        iso.new(interchange_level=3, joliet=3)
        iso.add_fp(io.BytesIO(b"sample payload"), 14, iso_path="/FILE.BIN;1", joliet_path="/File.bin")
        iso.write(str(path))
        iso.close()
        return path

    def test_header_and_two_trees(self):
        path = self.image()
        cfw.stamp_disc(path)
        report = cfw.verify_disc_header(path)
        self.assertEqual(report["encrypted_regions"], 0)
        self.assertEqual(report["sectors"] % 32, 0)
        for joliet, name in [(True, "/File.bin"), (False, "/FILE.BIN")]:
            reader = cfw.ISO9660(str(path), joliet=joliet)
            try:
                entry = dict(reader.walk())[name]
                reader.fh.seek(entry["lba"] * 2048)
                self.assertEqual(reader.fh.read(entry["size"]), b"sample payload")
            finally:
                reader.fh.close()

    def test_stale_range_rejected(self):
        path = self.image()
        cfw.stamp_disc(path)
        with path.open("r+b") as f:
            f.seek(12)
            f.write(struct.pack(">I", 12))
        with self.assertRaisesRegex(ValueError, "Stale disc ranges"):
            cfw.verify_disc_header(path)

    def test_split_rejoins_and_refuses_overwrite(self):
        path = self.image()
        parts = cfw.split_iso(path, self.root, chunk_size=4096)
        self.assertEqual(cfw.verify_parts(path, self.root, parts), cfw.digest(path))
        with self.assertRaisesRegex(ValueError, "refusing overwrite"):
            cfw.split_iso(path, self.root, chunk_size=4096)
        with (self.root / parts[0]["name"]).open("r+b") as f:
            f.write(b"corrupt")
        with self.assertRaisesRegex(ValueError, "Split part changed"):
            cfw.verify_parts(path, self.root, parts)

    def test_invalid_split_sizes(self):
        for size in (0, -2048, 4097, 2**32):
            with self.assertRaises(ValueError):
                cfw.split_iso(self.root / "none", self.root, size)

    def test_unsafe_paths(self):
        for name in ("../escape", "/../escape", "C:/escape", "a\\b"):
            with self.assertRaises(ValueError):
                cfw.safe_relative(name)

    def test_plain_elf_rejected_as_self(self):
        with self.assertRaisesRegex(ValueError, "Expected SELF"):
            cfw.control_records(b"\x7fELF" + bytes(128))

    def self_fixture(self):
        elf = bytearray(128)
        elf[:6] = b"\x7fELF\x02\x02"
        struct.pack_into(">HHIQQQIHHHHHH", elf, 16,
                         2, 21, 1, 0x10000, 64, 0, 0, 64, 56, 1, 64, 0, 0)
        struct.pack_into(">IIQQQQQQ", elf, 64, 1, 5, 120, 0x10000, 0x10000, 8, 8, 16)
        elf[120:] = b"payload!"
        wrapped = bytearray(512 + len(elf))
        wrapped[:4] = b"SCE\0"
        struct.pack_into(">IHH", wrapped, 4, 2, 0x8000, 1)
        struct.pack_into(">QQ", wrapped, 16, 512, len(elf))
        struct.pack_into(">QQQ", wrapped, 0x28, 0x80, 0xa0, 0xe0)
        struct.pack_into(">Q", wrapped, 0x48, 0x120)
        struct.pack_into(">QQ", wrapped, 0x58, 0x160, 112)
        struct.pack_into(">QIIQQ", wrapped, 0x80, 123, 0x1000002, 4, 1, 0)
        wrapped[0xa0:0xe0] = elf[:64]
        wrapped[0xe0:0x118] = elf[64:120]
        struct.pack_into(">QQIIII", wrapped, 0x120, 632, 8, 1, 0, 0, 2)
        struct.pack_into(">IIQ", wrapped, 0x160, 1, 48, 1)
        struct.pack_into(">IIQ", wrapped, 0x190, 2, 64, 0)
        wrapped[0x190 + 36:0x190 + 56] = hashlib.sha1(elf).digest()
        wrapped[512:] = elf
        return bytes(wrapped), bytes(elf)

    def test_self_metadata_retained(self):
        original, elf = self.self_fixture()
        generated = bytearray(original)
        generated[0x80:0xa0] = bytes(32)
        generated[0x170:0x190] = bytes([0xff]) * 32
        wrapped = cfw.retain_application_metadata(generated, original)
        self.assertTrue(cfw.verify_self(wrapped, elf, original)["payload_byte_identical"])

    def test_self_corruption_rejected(self):
        original, elf = self.self_fixture()
        for offset in (512 + 120, 0x120, 0xa0, 0xe0, 0x80, 0x170, 0x190 + 36):
            corrupt = bytearray(original)
            corrupt[offset] ^= 1
            with self.assertRaises(ValueError):
                cfw.verify_self(corrupt, elf, original)


if __name__ == "__main__":
    unittest.main()
