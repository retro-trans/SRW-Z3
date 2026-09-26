import json
import unittest
from pathlib import Path
from cpk import CPK
import aiddata
import aboard_order_labels as layout


class AboardOrderLabels(unittest.TestCase):
    def test_source_family_and_isolation(self):
        cpk=CPK('work/orig/AIDDATAPACK.CPK')
        original=cpk.read(next(f for f in cpk.files if f['id']==0))
        refs=aiddata.refs(original)
        discovered=set()
        for off,jp,_,_ in aiddata.strings(original):
            if jp in ('搭載中','：全機逆順配置'):
                discovered.update(refs.get(off,[]))
        self.assertEqual(discovered,set(layout.CAPTIONS)|{0x9bc74})
        root=Path('work/build_0.6.5_currency')
        mapping={k if len(k)==1 else tuple(k):v for k,v in
                 json.loads((root/'pairs.json').read_text()).items()}
        widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        patched=layout.apply(original,mapping,widths,original)
        allowed=set()
        for r in layout.ROWS:allowed.update(range(r,r+4))
        for r in layout.CAPTIONS:
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(original,patched))))
        for r in layout.ROWS:
            self.assertEqual(original[r+8:r+16],patched[r+8:r+16])
            self.assertEqual(original[r+22:r+32],patched[r+22:r+32])


if __name__=='__main__':unittest.main()
