import sys,unittest,struct
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
from category_port import Port
import menu_followup_art as art,startup_art,ui_layout,parts_network_fixes as network

class MenuFollowupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port=Port();archive=cls.port.cpk(ui_layout.ARCHIVE)
        cls.ui=archive.read(next(e for e in archive.files if e['id']==0))
        cls.raw=archive.read(next(e for e in archive.files if e['id']==1))
        cls.prior,_=startup_art.apply(cls.raw,cls.port.catalog)
        cls.changed,cls.audit=art.apply(cls.raw,cls.port.catalog)

    def test_four_word_cells_preserve_startup_palettes_and_other_pixels(self):
        allowed={192+page*262144+startup_art.pixel(x+xx,y+yy)
                 for page,x,y,w,h,mid in art.CELLS for xx in range(w) for yy in range(h)}
        changed={i for i,(a,b) in enumerate(zip(self.prior,self.changed)) if a!=b}
        self.assertTrue(changed);self.assertTrue(changed<=allowed)
        self.assertEqual(len(self.changed),len(self.raw))
        self.assertEqual(self.raw[192+4*262144:],self.changed[192+4*262144:])
        for page,x,y,w,h,mid in art.CELLS:
            offsets={192+page*262144+startup_art.pixel(x+xx,y+yy) for xx in range(w) for yy in range(h)}
            self.assertTrue(changed&offsets)
            bbox=art.tile(self.port.catalog.text(mid),w,h).getchannel('A').getbbox()
            self.assertGreaterEqual(bbox[0],3);self.assertLessEqual(bbox[2],w-3)
        art.validate_quads(self.ui)
        with self.assertRaises(ValueError):art.apply(self.changed,self.port.catalog)

    def test_square_only_and_vita_store_position(self):
        changed,audit=ui_layout.apply(self.ui,self.port);native=ui_layout.records(self.ui)
        ptr,jp=native[0xA1454]
        self.assertEqual(changed[ptr:ptr+len(jp.encode('cp932'))],('　'+jp[1:]).encode('cp932'))
        self.assertEqual(changed[0xA1454:0xA1474],self.ui[0xA1454:0xA1474])
        # Original Japanese width supplied a left-shifted caller origin.
        # Record X changes by 88 native pixels = 66 in the supplied 960px crop.
        x=struct.unpack_from('<f',changed,network.STORE+4)[0]
        self.assertAlmostEqual((x-1/1280)*640*(960/1280),66,places=4)
        self.assertAlmostEqual(54.5+(x-1/1280)*640*(960/1280),120.5,places=4)
        for record in (0xA9034,0xA9054,0xA90D4,0xA90F4):
            self.assertEqual(changed[record:record+32],self.ui[record:record+32])
        for p,x,w in art.QUADS:self.assertEqual(changed[p:p+80],self.ui[p:p+80])

if __name__=='__main__':unittest.main()
