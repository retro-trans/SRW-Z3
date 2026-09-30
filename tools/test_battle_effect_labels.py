"""Source and packed-pointer regressions for the battle animation banner."""
import json
import struct
import unittest
from pathlib import Path

import battle_effect_labels as effects
import eboot
import localization


class BattleEffectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import trdata
        trdata.use_glossary('analysis/glossary.json')
        root=Path('work/build_0.6.23_english_20260929')
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        effects.check_source(cls.source)
        new=bytearray(cls.source);eboot.add_segment(new);segs=eboot._segments(new)
        cls.result=eboot.command_labels(new,segs,effects.labels(),eboot._off(segs,eboot.NAME_STR),
                                        cls.mapping,cls.widths,window=False)
        cls.built=bytes(new)

    def test_all_labels_and_duplicate_references_translate(self):
        self.assertEqual(len(effects.BINDINGS),39)
        self.assertEqual(sum(len(refs) for _,_,refs in effects.BINDINGS),51)
        self.assertEqual(self.result[2],[])
        effects.check_built(self.built,self.mapping,self.widths)

    def test_at_field_reuses_canonical_ability_and_loader(self):
        cat=localization.english();mid='abilities:r_0121a166c715cdff'
        jp=cat.definition(mid)['source']
        self.assertEqual(cat.text(mid),'A.T. Field')
        self.assertEqual(effects.labels()[jp],cat.text(mid))
        self.assertEqual(eboot.load_commands(eboot.UI_UTF8_FILE)[jp],cat.text(mid))
        self.assertEqual(eboot.load_ui_hook()[jp],cat.text(mid))

    def test_shipped_utf8_table_reproduces_report(self):
        blob=Path('work/build_0.6.23_english_20260929/EBOOT.BIN').read_bytes()
        segs=eboot._segments(blob)
        jp=localization.english().definition('abilities:r_0121a166c715cdff')['source']
        for ref in (0x84e638,0x84e63c):
            va=struct.unpack_from('>I',blob,ref)[0]
            self.assertEqual(eboot._cstr(blob,eboot._off(segs,va)),jp.encode('utf-8'))

    def test_source_and_delivered_reference_guards(self):
        for off in (0x6dd6e0,0x84e638,0x84e63c,0x84e6e4):
            bad=bytearray(self.source);bad[off]^=1
            with self.assertRaises(AssertionError):effects.check_source(bad)
        bad=bytearray(self.built)
        # A.T. Field fits in place; force a different unchanged UTF-8 string.
        struct.pack_into('>I',bad,0x84e63c,0x6ed658)
        with self.assertRaises(AssertionError):effects.check_built(bad,self.mapping,self.widths)

    def test_changes_are_strings_references_unicode_and_ext_header_only(self):
        before=self.source;segs=eboot._segments(before)
        allowed=set()
        for jp in effects.labels():
            key=b'\0'+jp.encode('utf-8')+b'\0';p=0
            while True:
                hit=before.find(key,p,segs[0]['off']+segs[0]['filesz'])
                if hit<0:break
                start=hit+1;end=start+len(key)-2
                while before[end]==0:end+=1
                allowed.update(range(start,end));p=hit+1
                va=eboot._va(segs,start)
                for ref in range(segs[1]['off'],segs[1]['off']+segs[1]['filesz']-3,4):
                    if struct.unpack_from('>I',before,ref)[0]==va:allowed.update(range(ref,ref+4))
        table=eboot.unicode_table(before,segs)
        allowed.update(range(table+2*0x120,table+2*0x17f))
        ext=next(s for s in eboot._segments(self.built) if s['va']==eboot.EXT_VA)
        allowed.update(range(ext['hdr'],ext['hdr']+56))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(before,self.built))))


if __name__=='__main__':unittest.main()
