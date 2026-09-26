"""Complete title-variant inventory, packed alignment and byte isolation."""
import json,unittest,struct
from pathlib import Path
from cpk import CPK
import aiddata,eboot
import mech_info_layout as M


class MechInfoTests(unittest.TestCase):
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
            if jp==M.JP:found.update(refs.get(p,[]))
        self.assertEqual(found,set(M.ROWS))

    def test_title_only_patch_and_packed_fit(self):
        changed=M.apply(self.source,self.mapping,self.widths)
        M.check(self.built,self.mapping,self.widths)
        for r in M.ROWS:
            self.assertEqual(changed[r:r+32],self.built[r:r+32])
        allowed={p for r in M.ROWS for p in range(r+4,r+8)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,changed))))

    def test_actual_translation_matches_measured_label(self):
        segs=eboot._segments(self.elf)
        def zstr(va):
            p=eboot._off(segs,va);return self.elf[p:self.elf.index(b'\0',p)]
        p=eboot._off(segs,eboot.NAME_TBL)
        while True:
            key,val=struct.unpack_from('>II',self.elf,p)
            self.assertNotEqual(key,0,'missing Mech Info translation')
            if zstr(key)==M.JP.encode('cp932'):
                self.assertEqual(zstr(val&0x3fffffff),eboot._encode_marked(M.LABEL,self.mapping));break
            p+=8


if __name__=='__main__':unittest.main()
