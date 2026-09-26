"""Footer layout and byte-boundary tests, using a synthetic texture container."""
import hashlib
import os
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

import title_footer as footer

FONT = Path(os.environ.get('TITLE_FOOTER_TEST_FONT',
            'E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'))


@unittest.skipUnless(FONT.exists(), 'set TITLE_FOOTER_TEST_FONT to a TrueType font')
class TitleFooterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        header = bytearray(footer.GTF+0x180)
        header[footer.GTF:footer.GTF+4] = b'\x02\x02\0\0'
        struct.pack_into('>I', header, footer.GTF+8, 7)
        struct.pack_into('>II', header, footer.GTF+16, 0x180, 1280*720*4)
        header[footer.GTF+24] = 0xa5
        struct.pack_into('>HH', header, footer.GTF+32, *footer.SIZE)
        cls.original = bytes(header) + bytes((255,12,24,56))*(1280*720) + b'untouched next texture'

    def apply(self, version='0.6.2'):
        with patch.object(footer, 'SOURCE_SHA256', hashlib.sha256(self.original).hexdigest()):
            return footer.apply(self.original, FONT, version)

    def test_layout_has_two_right_aligned_separate_lines(self):
        ink = footer.overlay(FONT, '0.6.2').getchannel('A')
        # Both lines reach the same right edge, with empty rows between them.
        self.assertEqual(ink.crop((0,0,340,29)).getbbox()[2], 340)
        self.assertEqual(ink.crop((0,29,340,56)).getbbox()[2], 340)
        self.assertIsNone(ink.crop((0,29,340,33)).getbbox())
        self.assertEqual(footer.BOX[2:], (1252,696))

    def test_only_footer_rows_can_change(self):
        built = self.apply()
        offset,_ = footer.texture_span(self.original)
        restored = bytearray(built)
        for y in range(footer.BOX[1],footer.BOX[3]):
            p = offset+(y*1280+footer.BOX[0])*4
            restored[p:p+340*4] = self.original[p:p+340*4]
        self.assertEqual(restored, self.original)
        self.assertNotEqual(built, self.original)
        self.assertEqual(len(built),len(self.original))

    def test_repeatable(self):
        self.assertEqual(self.apply(), self.apply())

    def test_version_changes_visible_pixels(self):
        self.assertNotEqual(self.apply('0.6.2'), self.apply('0.6.3'))

    def test_invalid_or_overwide_version_rejected(self):
        with self.assertRaises(ValueError):
            footer.overlay(FONT, 'latest')
        with self.assertRaisesRegex(AssertionError, 'overflow'):
            footer.overlay(FONT, '0.6.'+'9'*80)

    def test_unknown_game_source_rejected(self):
        with self.assertRaisesRegex(AssertionError, 'source'):
            footer.apply(self.original, FONT, '0.6.2')

    def test_wrong_built_version_rejected(self):
        with patch.object(footer, 'SOURCE_SHA256', hashlib.sha256(self.original).hexdigest()):
            with self.assertRaisesRegex(AssertionError, 'wrong-version'):
                footer.verify(self.original, self.apply('0.6.2'), FONT, '0.6.3')


if __name__ == '__main__':
    unittest.main()
