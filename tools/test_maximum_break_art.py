"""Native nine-piece regression, independent of any historical build folder."""
import struct
import tempfile
import unittest
from pathlib import Path

from PIL import Image
from cpk import CPK
import maximum_break_art as art

FONT=Path('E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF')


def rectangles(blob):
    result=[]
    for p,_,_,_ in art.BANNER_PIECES:
        anchor=p-(16 if p==0x419c else 12)
        x,y=struct.unpack_from('<2h',blob,anchor)
        l,t,r,b,u,v,s,q=struct.unpack_from('<4h4H',blob,p)
        result.append(((x+l,y+t,x+r,y+b),(u,v,s,q)))
    return result


def reconstruct(blob):
    """Sample actual packed UV endpoints into initial-keyframe screen quads.

    Diagnostic CPU projection, not an emulator/effects playback substitute.
    """
    atlas=art.texture(blob,16)
    canvas=Image.new('RGBA',(1472,176))
    for (l,t,r,b),uv in rectangles(blob):
        tile=atlas.crop(uv).resize((r-l,b-t),Image.Resampling.BILINEAR)
        canvas.alpha_composite(tile,(l+736,t+88))
    return canvas


class MaximumBreakTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not art.SOURCE.exists() or not FONT.exists():
            raise unittest.SkipTest('local pristine CMN/font required')
        archive=CPK(str(art.SOURCE))
        cls.source=archive.read(archive.files[0])
        cls.built=art.apply(cls.source,FONT)

    def test_native_duplicate_glyph_explains_continuous_repaint_failure(self):
        native=rectangles(self.source)
        self.assertEqual(native[0][1],native[3][1])
        self.assertEqual(len(set(uv for _,uv in native)),8)
        self.assertTrue(any(a[0][2]>b[0][0] for a,b in zip(native,native[1:])))
        fixed=rectangles(self.built)
        self.assertEqual(len(set(uv for _,uv in fixed)),9)

    def test_whole_letters_once_and_contiguous_screen_bounds(self):
        self.assertEqual(''.join(art.BANNER_CHUNKS),'MAXIMUMBREAK')
        expected_x=-736
        for (l,t,r,b),(u,v,s,q) in rectangles(self.built):
            self.assertEqual(l,expected_x)
            self.assertEqual((t,b),(-88,88))
            self.assertEqual((u,v,s,q),(l+737,0,r+735,176))
            expected_x=r
        self.assertEqual(expected_x,736)

    def test_sampled_ink_is_not_cut_at_cell_edges(self):
        atlas=art.texture(self.built,16)
        for _,(u,v,s,q) in rectangles(self.built):
            tile=atlas.crop((u,v,s,q))
            l,t,r,b=tile.getchannel('A').getbbox()
            self.assertGreater(l,0)
            self.assertLess(r,tile.width)
            self.assertGreater(t,0)
            self.assertLess(b,tile.height)
        image=reconstruct(self.built)
        self.assertEqual(image.size,(1472,176))
        self.assertIsNotNone(image.getbbox())

    def test_exact_allowlist_preserves_animation_and_other_art(self):
        art.verify(self.source,self.built,FONT)
        restored=bytearray(self.built[:art.GTF])
        for p,_,_,_ in art.BANNER_PIECES:
            restored[p:p+16]=self.source[p:p+16]
        self.assertEqual(restored,self.source[:art.GTF])
        self.assertEqual(art.texture(self.source,1).tobytes(),
                         art.texture(self.built,1).tobytes())

    def test_source_and_rectangle_drift_fail_closed(self):
        bad=bytearray(self.source);bad[0]^=1
        with self.assertRaises(AssertionError):art.apply(bytes(bad),FONT)
        bad=bytearray(self.source);bad[art.BANNER_PIECES[0][0]]^=1
        with self.assertRaises(AssertionError):art.patch_banner_pieces(bad,FONT)

    def test_verify_rejects_old_uvs_and_unrelated_animation_changes(self):
        bad=bytearray(self.built)
        for p,_,_,_ in art.BANNER_PIECES:
            bad[p:p+16]=self.source[p:p+16]
        with self.assertRaises(AssertionError):art.verify(self.source,bytes(bad),FONT)
        bad=bytearray(self.built);bad[0x418c]^=1
        with self.assertRaises(AssertionError):art.verify(self.source,bytes(bad),FONT)

    def test_archive_round_trip_preserves_other_members(self):
        with tempfile.TemporaryDirectory(prefix='maximum_break_',dir='work') as directory:
            art.build(directory,FONT)
            old=CPK(str(art.SOURCE));new=CPK(str(Path(directory)/'CMN.CPK'))
            self.assertEqual([f['id'] for f in old.files],[f['id'] for f in new.files])
            for i,(a,b) in enumerate(zip(old.files,new.files)):
                self.assertEqual(new.read(b),self.built if i==0 else old.read(a))


if __name__=='__main__':unittest.main()
