"""Regression coverage for the title-screen Library label atlas."""
import unittest
from pathlib import Path
import title_library_buttons as B
import title_footer as F

class TitleLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=Path('work/title_buttons/original.member')
        if not source.exists() or not B.FONT.exists():
            raise unittest.SkipTest('local title source/font unavailable')
        cls.original=source.read_bytes()
        cls.font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'

    def test_complete_animation_family(self):
        B.audit(self.original)
        self.assertEqual(len(B.ROWS),5)
        self.assertEqual(sum(row[-1] for row in B.ROWS),2292)

    def test_only_five_rectangles_change(self):
        result=B.apply(self.original,self.font)
        B.verify(self.original,result,self.font)
        self.assertNotEqual(result,self.original)

    def test_footer_composition(self):
        result=B.apply(self.original,self.font,'0.6.3')
        B.verify(self.original,result,self.font,'0.6.3')
        self.assertEqual(F.background(result).tobytes(),
                         F.background(F.apply(self.original,self.font,'0.6.3')).tobytes())

    def test_unrelated_change_rejected(self):
        result=bytearray(B.apply(self.original,self.font))
        result[0]^=1
        with self.assertRaises(AssertionError):B.verify(self.original,bytes(result),self.font)

    def test_source_drift_rejected(self):
        source=bytearray(self.original);source[0]^=1
        with self.assertRaises(AssertionError):B.apply(bytes(source),self.font)

if __name__=='__main__':unittest.main()
