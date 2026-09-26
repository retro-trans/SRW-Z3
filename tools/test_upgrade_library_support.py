"""Packed regressions for the upgrade / blank Library / support count report."""
import json,struct,unittest
from pathlib import Path
from cpk import CPK
import aiddata,digraph as dg
import upgrade_list_labels as U
import intermission_layout as L
import battle_preview_layout as B

class UpgradeLibrarySupportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out=Path('work/out_0.6.3')
        if not (out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('candidate unavailable')
        a=CPK('work/orig/AIDDATAPACK.CPK');b=CPK(str(out/'AIDDATAPACK.CPK'))
        cls.source=a.read(a.files[0]);cls.built=b.read(b.files[0])
        cls.m=json.loads((out/'pairs.json').read_text())
        cls.w={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}

    def test_upgrade_category_and_numeric_isolation(self):
        refs=aiddata.refs(self.source)
        for jp in ('武器改造度','照準値\n武器'):
            found={r for p,t,_,_ in aiddata.strings(self.source) if t==jp for r in refs.get(p,[])}
            self.assertEqual(found,{r for r,(t,_) in U.ROWS.items() if t==jp})
        new=U.apply(self.source,self.m,self.w);U.check(self.built,self.m,self.w)
        allowed={p for r in U.ROWS for p in range(r,r+4)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,new))))
        for r in U.ROWS:self.assertEqual(self.source[r+4:r+32],self.built[r+4:r+32])

    def test_all_library_buttons_are_plain_visible_glyphs_in_source_mode(self):
        L.check(self.built,self.m,self.w)
        self.assertEqual(len(L.LIBRARY),6)  # Robot title has two states.
        labels=set()
        for r in L.LIBRARY:
            en=L.ROWS[r][1];labels.add(en);raw=L.text(self.built,r)
            self.assertEqual(raw,dg.encode_mixed(en,self.m))
            self.assertEqual(self.built[r+23],self.source[r+23])
            self.assertEqual(self.built[r+22],self.source[r+22])
            self.assertNotIn(r,L.LIVE_CENTERED)
            for i in range(0,len(raw),2):
                self.assertGreater(self.w[dg.cell_index(int.from_bytes(raw[i:i+2],'big'))],0)
        self.assertEqual(labels,{'Robot Encyclopedia','Character Encyclopedia','Glossary','Sound Select','Scenario Chart'})

    def test_three_support_titles_leave_room_for_counter(self):
        B.check(self.built,self.m,self.w)
        for r,label in [(0xb0eb4,'S. Atk'),(0xb0ed4,'Re-Atk'),(0xb0ef4,'S. Def')]:
            self.assertEqual(L.text(self.built,r),dg.encode_mixed(label,self.m))
            self.assertEqual(self.source[r+4:r+32],self.built[r+4:r+32])
            self.assertEqual(self.built[r+19],23)
            self.assertGreater(96-L.ink(label,self.m,self.w,23),12)
        new=B.apply(self.source,self.m,self.w)
        allowed={p for r in B.ROWS for p in range(r,r+4)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,new))))

if __name__=='__main__':unittest.main()
