"""Dual wrapper checks; layout regression suite supplies mapped-data coverage."""
from pathlib import Path
import struct
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/ps3'))
import build_dual_0614 as m
from test_cfw_loader_layout import fixture


class DualTests(unittest.TestCase):
    def test_iso_append_preserves_files_and_updates_both_trees(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            stage = root / 'stage'
            exe = stage / 'PS3_GAME/USRDIR/EBOOT.BIN'
            exe.parent.mkdir(parents=True)
            exe.write_bytes(b'old elf')
            (stage / 'OTHER').write_bytes(b'unchanged asset')
            aliases = {m.d.EBOOT: m.d.EBOOT, '/OTHER': '/OTHER'}
            expected = {name: m.d.info(stage / name.lstrip('/')) for name in aliases}
            source, target = root / 'source.iso', root / 'target.iso'
            m.d.write_image(source, stage, aliases, expected)
            reader = m.c.ISO9660(str(source))
            try:
                inventory = dict(reader.walk())
            finally:
                reader.fh.close()
            before = m.d.info(source)
            m.append_executable(source, target, b'new wrapped executable')
            actual = m.verify_members(source, target, inventory, aliases, b'new wrapped executable')
            self.assertEqual(actual['/OTHER'], expected['/OTHER'])
            self.assertEqual(m.d.info(source), before)
            with self.assertRaises(ValueError):
                m.append_executable(source, target, b'overwrite')

    def test_rpc_debug_extraction(self):
        elf = m.layout.fold(fixture())
        data = bytearray(0x1000)
        data[:4] = b'SCE\0'
        struct.pack_into('>H', data, 8, 0x8000)
        struct.pack_into('>QQ', data, 16, len(data), len(elf))
        data.extend(elf)
        self.assertEqual(m.rpc_decode(data), elf)
        for offset in (0, 8, 16, 24):
            bad = bytearray(data)
            bad[offset] ^= 1
            with self.subTest(offset=offset), self.assertRaises(ValueError):
                m.rpc_decode(bad)

    def test_does_not_accept_plain_elf_as_hardware_wrapper(self):
        with self.assertRaises(ValueError):
            m.rpc_decode(fixture())


if __name__ == '__main__':
    unittest.main()
