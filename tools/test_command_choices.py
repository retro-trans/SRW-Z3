"""Screenshot menu families: static templates plus live UTF-8 rows."""
import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
import eboot
import trdata
import tag_reward_layout as T
import command_choice_labels as C
from intermission_layout import text
import digraph as dg


class CommandChoiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.23_english_20260929')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        cls.shipped=(root/'EBOOT.BIN').read_bytes()
        k=CPK('work/orig/AIDDATAPACK.CPK');cls.ui=k.read(k.files[0])
        cls.fixed=T.apply(cls.ui,cls.mapping,cls.widths)
        trdata.use_glossary('analysis/glossary.json')

    def test_static_variants_and_style_isolation(self):
        for r in (0x9cf94,0x9cfb4,0xa95d4):
            self.assertEqual(text(self.fixed,r),dg.encode_mixed(T.ROWS[r][1],self.mapping,newline=b'\n'))
            self.assertEqual(self.fixed[r+4:r+32],self.ui[r+4:r+32])
        T.check(self.fixed,self.mapping,self.widths)

    def test_all_live_sources_and_shipped_omission(self):
        C.check_source(self.source)
        C.check_source(self.shipped)
        with self.assertRaises(AssertionError):C.check_built(self.shipped,self.mapping,self.widths)
        self.assertEqual([r for _,_,r in C.UTF8],list(range(0x780578,0x780594,4)))

    def test_live_utf8_patch_and_no_unrelated_bytes(self):
        b=bytearray(self.source);cursor,_=eboot.add_segment(b)
        before=bytes(b);segs=eboot._segments(b)
        result=eboot.command_labels(b,segs,C.utf8_labels(),cursor,self.mapping,self.widths,window=False)
        self.assertFalse(result[2])
        C.check_built(b,self.mapping,self.widths)
        allowed=set(range(cursor,result[3]))
        allowed.update(range(*result[4]))
        for _,va,ref in C.UTF8:
            allowed.update(range(ref,ref+4))
            pos=eboot._off(segs,va);end=before.index(0,pos)
            while before[end]==0:end+=1
            allowed.update(range(pos,end))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(before,b))))

    def test_hook_agreement_and_guard_failure(self):
        hooks=eboot.load_ui_hook();utf8=eboot.load_commands(eboot.UI_UTF8_FILE)
        for jp,en in C.hooks().items():self.assertEqual(hooks[jp],en)
        for jp,en in C.utf8_labels().items():self.assertEqual(utf8[jp],en)
        bad=bytearray(self.source);bad[0x780590]^=1
        with self.assertRaises(AssertionError):C.check_source(bad)


if __name__=='__main__':unittest.main()
