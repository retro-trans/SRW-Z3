"""In-memory banner checks; does not build or install game archives."""
import unittest
from cpk import CPK
import berserk_banner as b

FONT='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'


class BerserkBannerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        k=CPK('work/orig/EFFPS3.CPK')
        cls.original=k.read(next(f for f in k.files if f['id']==b.MEMBER))
        cls.built=b.apply(cls.original,FONT)

    def test_only_text_pixels_change(self):
        b.verify(self.original,self.built,FONT)

    def test_source_guard(self):
        damaged=bytearray(self.original);damaged[0]^=1
        with self.assertRaises(AssertionError):b.apply(damaged,FONT)

    def test_reject_changed_animation(self):
        damaged=bytearray(self.built);damaged[0x80]^=1
        with self.assertRaises(AssertionError):b.verify(self.original,damaged,FONT)

    def test_both_word_sprites_centered_with_margin(self):
        im=b.atlas(self.built)
        for rect in ((0,8,512,40),(0,40,512,80)):
            tile=im.crop(rect);box=tile.getchannel('A').getbbox()
            self.assertIsNotNone(box)
            self.assertLessEqual(abs(box[0]-(512-box[2])),1)
            self.assertGreater(box[1],0)
            self.assertLess(box[3],tile.height)

    def test_transparent_pixels_have_no_hidden_color(self):
        tile=b.atlas(self.built).crop((0,8,512,80))
        transparent=[p for p in tile.getdata() if p[3]==0]
        self.assertTrue(transparent)
        self.assertTrue(all(p==(0,0,0,0) for p in transparent))


if __name__=='__main__':unittest.main()
