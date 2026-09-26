"""Exact title-only alignment and complete source-variant coverage."""
import json,unittest,struct
from pathlib import Path
from cpk import CPK
import aiddata,eboot
import weapon_info_layout as W

class WeaponInfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out=Path('work/out_0.6.3')
        if not (out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('local candidate unavailable')
        a=CPK('work/orig/AIDDATAPACK.CPK');b=CPK(str(out/'AIDDATAPACK.CPK'))
        cls.source=a.read(a.files[0]);cls.built=b.read(b.files[0])
        cls.mapping=json.loads((out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}
        cls.elf=(out/'EBOOT.BIN').read_bytes()

    def test_all_heading_occurrences(self):
        refs=aiddata.refs(self.source);found=set()
        for p,jp,_,_ in aiddata.strings(self.source):
            if jp=='武器性能':found.update(refs.get(p,[]))
        self.assertEqual(found,set(W.ROWS))

    def test_title_only_patch_and_packed_fit(self):
        changed=W.apply(self.source,self.mapping,self.widths)
        W.check(self.built,self.mapping,self.widths)
        for r in W.ROWS:
            self.assertEqual(changed[r:r+32],self.built[r:r+32])
        allowed={p for r in W.ROWS for p in range(r+4,r+8)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,changed))))

    def test_actual_translation_matches_measured_label(self):
        segs=eboot._segments(self.elf)
        def zstr(va):
            p=eboot._off(segs,va);return self.elf[p:self.elf.index(b'\0',p)]
        p=eboot._off(segs,eboot.NAME_TBL)
        while True:
            key,val=struct.unpack_from('>II',self.elf,p)
            self.assertNotEqual(key,0,'missing Weapon Info translation')
            if zstr(key)=='武器性能'.encode('cp932'):
                self.assertEqual(zstr(val&0x3fffffff),eboot._encode_marked(W.LABEL,self.mapping));break
            p+=8

if __name__=='__main__':unittest.main()
