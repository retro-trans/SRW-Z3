"""Upgrade-family coverage, fixed records and native unlock composer replay."""
import json
from pathlib import Path
import struct
import unittest
import digraph as dg
import eboot
import trdata
import trader_upgrade_text as T
import unlock_reports as U
from test_ps3_link_identity import CPU


class UpgradeTextTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        root=Path('work/build_0.6.21_english_20260925_r2')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}

    def test_inventory_and_fixed_record_isolation(self):
        T.check_source(self.source)
        rows=list(T.rows())
        self.assertEqual(len(rows),31)
        self.assertEqual(sum(d['context']['role']=='completed' for _,d,_ in rows)+len(U.CONDITIONS),21)
        out=T.patch(self.source,self.mapping)
        allowed=set()
        for mid,d,en in rows:
            c=d['context']
            if c['role'] in ('lore','effect'):
                off=int(c['eboot_offset'],16);cap=c['capacity']
                allowed.update(range(off,off+cap))
                raw=dg.encode_mixed(en,self.mapping,newline=b'\n')+b'\0'
                self.assertLessEqual(len(raw),cap,mid)
                self.assertEqual(out[off:off+len(raw)],raw)
        self.assertEqual(len(self.source),len(out))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,out))))
        for off in (0x6b0538,0x6b09b8,0x6b0828,0x6b0f28):
            bad=bytearray(self.source);bad[off]^=1
            with self.assertRaises(AssertionError):T.check_source(bad)

    def test_complete_and_mixed_hooks(self):
        hooks=eboot.load_ui_hook()
        expected={**U.CONDITIONS,**T.hooks(),**T.mixed_hooks()}
        for key,en in expected.items():
            self.assertEqual(hooks[key],en)
            self.assertNotIn(key,eboot.UI_PREFIX|eboot.UI_JOINED)
        self.assertEqual(len(T.mixed_hooks()),4)
        self.assertTrue(set(T.mixed_hooks())<=eboot.UI_KEY_VWF)
        self.assertEqual(hooks['『エースパイロットを３名育成』を達成'],'Completed: Raise 3 Ace Pilots')
        self.assertEqual(hooks['システムＺＣＩ'],'System ZCI')

    def test_native_fixed_copy_prefix_and_suffix(self):
        elf=bytearray(self.source);cursor,_=eboot.add_segment(elf)
        patched,_=U.patch(elf,self.mapping,cursor)
        segs=eboot._segments(patched)
        copied=[]
        for i,(start,end,src,dst) in enumerate(((0x2b25e0,0x2b2670,9,11),
                                              (0x2b2934,0x2b2974,11,9))):
            ptr,_,jp,en=U.PARTS[i]
            address=struct.unpack_from('>I',patched,ptr)[0]
            raw=U.encoded_part(jp,en,self.mapping)[:-1]
            self.assertEqual(len(raw),[18,8][i])
            c=CPU(patched);dest=0x3000000;c.put(dest,b'\xcc'*64)
            c.r[src]=address;c.r[dst]=dest;c.run(start,{end})
            self.assertEqual(c.read(dest,len(raw)),raw)
            self.assertEqual(c.read(dest+len(raw),8),b'\xcc'*8)
            copied.append(raw)
        for _,d,en in T.rows():
            if d['context']['role']=='name':
                composed=copied[0]+d['source'].encode('cp932')+copied[1]
                key=next(k for k,v in T.mixed_hooks().items() if en in v)
                self.assertEqual(composed,eboot._encode_marked(key,self.mapping))
        # Original English replacement was 32 bytes but native copy took 18.
        old=dg.encode_mixed('Now at D-Trader: ',self.mapping)
        self.assertEqual(old[:18],dg.encode_mixed('Now at D-',self.mapping))
        with self.assertRaisesRegex(AssertionError,'fixed-copy budget'):
            U.encoded_part(U.PARTS[0][2],'Now at D-Trader: ',self.mapping)


if __name__=='__main__':unittest.main()
