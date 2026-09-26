import struct
import unittest
from cpk import CPK
import pilot_swap_alignment as layout

class PilotSwapAlignment(unittest.TestCase):
    def test_source_inventory_and_isolation(self):
        c=CPK('work/orig/AIDDATAPACK.CPK')
        b=c.read(next(f for f in c.files if f['id']==0))
        out=layout.apply(b)
        allowed={i for r in layout.ROWS for i in range(r+4,r+8)}
        self.assertEqual(len(out),len(b))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,out))))
        self.assertEqual(out[0xb22d4:0xb22f4],b[0xb22d4:0xb22f4])
        for r,(size,_) in layout.ROWS.items():
            self.assertEqual(out[r+8:r+32],b[r+8:r+32])
            delta=(struct.unpack_from('>f',out,r+4)[0]-struct.unpack_from('>f',b,r+4)[0])*640
            self.assertAlmostEqual(delta,layout.shift(size),places=4)

    def test_capture_center_and_highlight_clearance(self):
        left,right=1032/2.,1405/2.
        center=(876+1395)/4.
        self.assertAlmostEqual((left+right)/2+layout.NORMAL_SHIFT,center)
        for size,_ in layout.ROWS.values():
            half_width=(right-left)/2*size/28.
            self.assertGreater(center-half_width,876/2.+16)
            self.assertLess(center+half_width,1395/2.-16)

if __name__=='__main__':unittest.main()
