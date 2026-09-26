"""Source coverage, overlay/state preservation and packed warning text."""
import json
import unittest
from pathlib import Path
from cpk import CPK
import aiddata
import weapon_requirements as req


class WeaponRequirementsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out = Path('work/out_0.6.3')
        def read(path):
            k = CPK(str(path))
            return k.read(next(f for f in k.files if f['id']==0))
        cls.old = read('work/orig/AIDDATAPACK.CPK')
        cls.new = read(out/'AIDDATAPACK.CPK')
        cls.mapping = json.loads((out/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}

    def test_exact_source_category_inventory(self):
        refs = aiddata.refs(self.old)
        wanted = {jp for jp,en in req.ROWS.values()}
        found = {r for off,jp,_,_ in aiddata.strings(self.old) if jp in wanted for r in refs.get(off,[])}
        self.assertEqual(found,set(req.ROWS))
        self.assertEqual(len(found),14)

    def test_packed_text_and_color_registration(self):
        req.check(self.new,self.mapping,self.widths)
        for r in req.ROWS:
            # Position and alignment are intentionally changed on header only.
            if r not in (req.BASE,req.ACCENT):
                self.assertEqual(self.old[r+4:r+32],self.new[r+4:r+32])
            else:
                self.assertEqual(self.old[r+8:r+23],self.new[r+8:r+23])
                self.assertEqual(self.old[r+24:r+32],self.new[r+24:r+32])
                self.assertEqual(self.old[r+23]&~0x40,self.new[r+23])

    def test_patch_isolation_and_unchanged_placeholder(self):
        updated = req.apply(self.old,self.mapping,self.widths)
        allowed = {i for r in req.ROWS for i in range(r,r+4)}
        allowed |= {i for r in (req.BASE,req.ACCENT) for i in range(r+4,r+8)}
        allowed |= {req.BASE+23,req.ACCENT+23}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.old,updated))))
        self.assertEqual(self.old[0xa9af4:0xa9b14],self.new[0xa9af4:0xa9b14])


if __name__ == '__main__':
    unittest.main()
