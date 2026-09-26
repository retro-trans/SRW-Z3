import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
import menu_followup as M
import intermission_layout as I


class MenuFollowup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.12_approved_subtitle')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c=CPK('work/orig/AIDDATAPACK.CPK'); cls.source=c.read(c.files[0])

    def test_inventory_and_exact_isolation(self):
        b=self.source; out=M.apply(b,self.mapping,self.widths,b)
        allowed={i for r in M.ROWS for i in range(r,r+4)}
        allowed.update(i for r in (*M.PROMPTS,*M.COMMANDER) for i in range(r+4,r+8))
        allowed.update(r+23 for r in M.PROMPTS)
        allowed.update(i for _,rs,_ in M.BUTTONS for r in rs for i in range(r+4,r+8))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,out))))
        self.assertEqual(len(M.PROMPTS),4)
        self.assertEqual(len(M.COMMANDER),2)
        self.assertEqual(len(M.CHIPS),9)
        self.assertEqual(sum(len(rs) for _,rs,_ in M.BUTTONS),12)

    def test_measured_button_centres(self):
        # Caption extents in the user's original image; Search is selected.
        bounds=[(966,1195,1140,28),(1499,1744,1677.5,28),
                (2152,2344,2207.5,31),(2082,2279,2210,28),
                (2062,2272,2210,28)]
        for (_,_,delta),(left,right,center,size) in zip(M.BUTTONS,bounds):
            corrected=(left+right)/2+delta*size/28*M.SCREEN_SCALE
            self.assertAlmostEqual(corrected,center)
            self.assertLess((right-left)/2*31/size,230)

    def test_store_caption_and_empty_fragments(self):
        b=self.source; out=I.apply(b,self.mapping,self.widths)
        self.assertAlmostEqual(211+I.STORE_LIVE_X_CORRECTION*M.SCREEN_SCALE,377)
        for r in I.LIVE_CENTERED:
            expected=-1/1280.+I.STORE_LIVE_X_CORRECTION/640.
            self.assertAlmostEqual(struct.unpack_from('>f',out,r+4)[0],expected)
        self.assertEqual(I.text(out,0xa9094),b'')
        self.assertEqual(I.text(out,0xa90b4),b'')

    def test_stale_button_source_rejected(self):
        b=bytearray(self.source); b[0xa31d4+4:0xa31d4+8]=bytes(4)
        with self.assertRaises(AssertionError):
            M.apply(b,self.mapping,self.widths,self.source)


if __name__=='__main__': unittest.main()
