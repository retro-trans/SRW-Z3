"""Live-capture-derived Library centering; preserve the visible text mode."""
import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
import intermission_layout as layout

# Colored glyph X extents in the user's 2560x1440 capture. The selected
# Sound Select is yellow, others cyan; outlines excluded from measurement.
BOUNDS={0xa62b4:(676,1394),0xa62d4:(676,1394),0xa62f4:(593,1451),
        0xa6314:(949,1259),0xa6334:(737,1214),0xa6354:(713,1250)}


class LibraryAlignment(unittest.TestCase):
    def test_live_centers_and_preserved_modes(self):
        root=Path('work/build_0.6.6_aboard_order')
        m=json.loads((root/'pairs.json').read_text())
        w={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cpk=CPK('work/orig/AIDDATAPACK.CPK')
        source=cpk.read(next(f for f in cpk.files if f['id']==0))
        result=layout.apply(source,m,w)
        oldcpk=CPK(str(root/'AIDDATAPACK.CPK'))
        old=oldcpk.read(next(f for f in oldcpk.files if f['id']==0))
        for r,(left,right) in BOUNDS.items():
            shift=layout.LIBRARY_LIVE_X_CORRECTION[r]
            self.assertAlmostEqual((left+right)/4+shift,639.5)
            # The longest translated title remains inside the blue center
            # button's approximately x=401..879 native-pixel bounds.
            self.assertGreater(left/2+shift,401+8)
            self.assertLess(right/2+shift,879-8)
            self.assertEqual(result[r+8:r+32],old[r+8:r+32])
            self.assertEqual(result[r+23],1)
            self.assertEqual(layout.text(result,r),layout.text(old,r))
            delta=(struct.unpack_from('>f',result,r+4)[0]-struct.unpack_from('>f',old,r+4)[0])*640
            self.assertAlmostEqual(delta,shift,places=4)
        self.assertEqual(result[0xa62b4+4:0xa62b4+8],result[0xa62d4+4:0xa62d4+8])


if __name__=='__main__':unittest.main()
