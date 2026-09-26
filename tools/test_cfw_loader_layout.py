"""Synthetic ELF layout, relocation and corruption-rejection tests."""
from pathlib import Path
import struct
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/ps3'))
import cfw_loader_layout as m


def fixture():
    data = bytearray(0x8F0000)
    data[:7] = b'\x7fELF\x02\x02\x01'
    struct.pack_into('>HHIQQQIHHHHHH', data, 16,
                     2, 21, 1, 0x7A09A0, 64, 0x85DAD0, 0, 64, 56, 8, 64, 32, 31)
    rows = [
        (1, 0x400005, 0, 0x10000, 0x10000, 0x780000, 0x780000, 0x10000),
        (1, 0x600006, 0x780000, 0x790000, 0x790000, 0xD9E34, 0x46EF80, 0x10000),
        (1, 4, 0x860000, 0xC00000, 0xC00000, 0x90000, 0x90000, 0x10000),
        (1, 6, m.TAIL, 0, 0, 0, 0, 0x10000),
        (1, 0x6600006, m.TAIL, 0, 0, 0, 0, 0x10000),
        (7, 4, 0x7CF640, 0x7DF640, 0x7DF640, 8, 0x1F8, 8),
        (0x60000001, 0, 0x779420, 0x789420, 0x789420, 0x28, 0x28, 8),
        (0x60000002, 0, 0x779448, 0x789448, 0x789448, 0x40, 0x40, 4)]
    for i, row in enumerate(rows):
        m.PH.pack_into(data, 64 + i * 56, *row)
    data[0x200:0x208] = b'CODETEST'
    data[0x780000:0x780008] = b'DATATEST'
    data[m.TAIL:m.TAIL + 8] = b'TAILTEST'
    data[m.EXT:m.EXT + 8] = b'TEXTTEST'
    data[-8:] = b'END-TEXT'
    for i, row in ((1, (0, 1, 6, 0x10200, 0x200, 8, 0, 0, 4, 0)),
                   (28, (0, 8, 3, 0x869E80, m.TAIL, 0x393100, 0, 0, 128, 0)),
                   (29, (0, 1, 0, 0, m.TAIL, 8, 0, 0, 1, 0))):
        m.SH.pack_into(data, 0x85DAD0 + i * 64, *row)
    return bytes(data)


class LoaderLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = fixture()
        cls.after = m.fold(cls.before)

    def test_two_loads_preserve_addresses_and_payload(self):
        report = m.verify(self.before, self.after)
        self.assertEqual(report['active_loads'], 2)
        self.assertEqual(self.after[m.NEW_EXT:m.NEW_EXT + 8], b'TEXTTEST')
        self.assertEqual(self.after[m.NEW_TAIL - 8:m.NEW_TAIL], b'END-TEXT')
        self.assertEqual(self.after[m.TAIL_START:m.TAIL_START + 8], b'TAILTEST')
        self.assertEqual(m.sections(self.after)[0] % 8, 0)

    def test_bss_offset_not_relocated_but_nonalloc_tail_is(self):
        _, old = m.sections(self.before)
        _, new = m.sections(self.after)
        self.assertEqual(new[28], old[28])
        self.assertEqual(new[29][4], old[29][4] + m.DELTA)
        self.assertFalse(any(self.after[m.TAIL:m.NEW_EXT]))

    def test_corruption_in_each_preserved_region_rejected(self):
        for address in (24, 0x200, 0x780000, m.TAIL, m.NEW_EXT,
                        m.NEW_TAIL, m.TAIL_START, m.sections(self.after)[0] + 28 * 64):
            damaged = bytearray(self.after)
            damaged[address] ^= 1
            with self.subTest(address=hex(address)), self.assertRaises(ValueError):
                m.verify(self.before, damaged)

    def test_unknown_layout_and_repeated_transform_rejected(self):
        changed = bytearray(self.before)
        changed[64 + 56 + 7] ^= 1
        for data in (changed, self.before[:-1], self.after):
            with self.assertRaises(ValueError):
                m.fold(data)

    def test_allocated_section_offsets_are_not_silently_moved(self):
        changed = bytearray(self.before)
        m.SH.pack_into(changed, 0x85DAD0 + 29 * 64,
                       0, 1, 2, 0, m.TAIL, 8, 0, 0, 1, 0)
        with self.assertRaisesRegex(ValueError, 'Section payload changed'):
            m.fold(changed)


if __name__ == '__main__':
    unittest.main()
