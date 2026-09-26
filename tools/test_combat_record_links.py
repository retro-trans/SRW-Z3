"""Complete Combat Record link and tooltip family in packed candidate."""
import json,struct,unittest
from pathlib import Path
from cpk import CPK
import eboot,aiddata
import combat_record_links as C

class CombatRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out=Path('work/out_0.6.3')
        if not (out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('local candidate unavailable')
        old=CPK('work/orig/AIDDATAPACK.CPK');new=CPK(str(out/'AIDDATAPACK.CPK'))
        cls.source=old.read(old.files[0]);cls.built=new.read(new.files[0])
        cls.mapping=json.loads((out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}
        cls.elf=(out/'EBOOT.BIN').read_bytes()

    def test_all_source_link_copies(self):
        refs=aiddata.refs(self.source)
        for jp,en in C.LINKS:
            found=set()
            for p,s,_,_ in aiddata.strings(self.source):
                if s==jp:found.update(refs.get(p,[]))
            self.assertEqual(found,{r for r,v in C.ROWS.items() if v==(jp,en)})
            self.assertEqual(len(found),3)

    def test_packed_labels_and_metadata(self):
        C.check(self.built,self.mapping,self.widths)
        for r in C.ROWS:self.assertEqual(self.built[r+4:r+32],self.source[r+4:r+32])
        # Independent patch isolation proves that values/templates are untouched.
        result=C.apply(self.source,self.mapping,self.widths)
        allowed={p for r in C.ROWS for p in range(r,r+4)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,result))))

    def test_four_built_help_strings(self):
        original=Path('work/EBOOT_dec.elf').read_bytes();segs=eboot._segments(self.elf)
        _,encode=eboot.vwf_face(bytearray(self.elf),segs,self.mapping)
        translations={r['jp']:r['en'] for r in json.loads(Path(eboot.UI_UTF8_FILE).read_text(encoding='utf-8'))['lines']}
        for jp,en in C.HELP.items():
            self.assertEqual(translations[jp],en)
            pos=original.index(b'\0'+jp.encode('utf-8')+b'\0')+1
            expected=encode(en).encode('utf-8')+b'\0'
            self.assertEqual(self.elf[pos:pos+len(expected)],expected)

if __name__=='__main__':unittest.main()
