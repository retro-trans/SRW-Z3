"""Native title geometry, alpha, composition and strict preservation checks."""
import unittest
from pathlib import Path
from PIL import Image
import title_logo as L
import title_library_buttons as B


class TitleLogoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path=Path('work/title_buttons/original.member')
        if not path.exists(): raise unittest.SkipTest('local title source required')
        cls.original=path.read_bytes()
        cls.font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'

    def test_native_uvs(self): L.audit(self.original)

    def test_clean_transparent_assets(self):
        for rect,im in L.tiles():
            self.assertEqual(im.mode,'RGBA')
            self.assertEqual(im.getchannel('A').getextrema(),(0,255))
            self.assertEqual(im.getpixel((im.width-1,0))[3],0)
        main=Image.open(L.ASSETS/'wordmark.png')
        self.assertEqual(main.getchannel('A').crop((0,0,706,50)).getbbox(),None)

    def test_byte_preservation_and_original_z(self):
        built=L.apply(self.original);L.verify(self.original,built)
        for box in L.Z_BOXES:
            self.assertEqual(L.atlas(built).crop(box).tobytes(),L.atlas(self.original).crop(box).tobytes())

    def test_library_and_footer_composition(self):
        base=B.apply(self.original,self.font,'0.6.3')
        L.verify_complete(self.original,L.apply(base),self.font,'0.6.3')

    def test_unrelated_change_rejected(self):
        built=bytearray(L.apply(self.original));built[0]^=1
        with self.assertRaises(AssertionError): L.verify(self.original,bytes(built))

    def test_idempotent(self):
        built=L.apply(self.original)
        self.assertEqual(L.apply(built),built)

    def test_approved_subtitle_cleanup(self):
        from prepare_approved_subtitle import prepare, DEST
        with Image.open(DEST) as saved:
            self.assertEqual(saved.tobytes(), prepare().tobytes())
            self.assertEqual(saved.getchannel('A').getbbox(), (8, 5, 324, 79))
            # Preserve real transparency and the shorter supporting line.
            self.assertIsNone(saved.getchannel('A').crop((0, 80, 339, 117)).getbbox())


if __name__=='__main__': unittest.main()
