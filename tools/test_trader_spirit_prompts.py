"""Native fixed-copy replay, UI byte isolation and source-contract checks."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from cpk import CPK
import digraph as dg
import trader_spirit_prompts as S
import aiddata
from intermission_layout import text
from test_ps3_link_identity import CPU


class TraderSpiritPromptsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        root=Path('work/build_0.6.21_english_20260925_r2')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        k=CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui=k.read(k.files[0])
        k=CPK(str(root/'AIDDATAPACK.CPK'))
        cls.current=k.read(k.files[0])

    def test_exact_byte_isolation_and_guards(self):
        out=S.patch_elf(self.source,self.mapping)
        allowed={p for _,d,_ in S.rows() if 'eboot_offset' in d['context']
                 for p in range(int(d['context']['eboot_offset'],16),
                                int(d['context']['eboot_offset'],16)+d['context']['bytes'])}
        allowed.update(p for va,_,_ in S.INLINE for p in range(va-0x10000,va-0x10000+4))
        self.assertEqual(len(out),len(self.source))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,out))))
        for offset in (0x70cfd0,0x70cfe8,0x70cff0,0x7cb6b8,0x29f9bc):
            bad=bytearray(self.source);bad[offset]^=1
            with self.assertRaises(AssertionError):
                S.patch_elf(bad,self.mapping)
        rows=[(mid,d,en+'!' if mid.endswith(':buy_suffix') else en) for mid,d,en in S.rows()]
        with patch.object(S,'rows',return_value=iter(rows)):
            with self.assertRaisesRegex(AssertionError,'native append length'):
                S.patch_elf(self.source,self.mapping)

    def test_native_buy_and_sell_suffix_copies(self):
        out=S.patch_elf(self.source,self.mapping)
        names=json.loads(Path('translation/parts.json').read_text(encoding='utf-8'))
        names=[v for k,v in names.items() if not k.startswith('_') and v]
        self.assertIn('Chimera Squad ID',names)
        bykey={mid.split(':')[1]:(d,en) for mid,d,en in S.rows()}
        for key,start,end in (('buy_suffix',0x2aed34,0x2aedb4),
                              ('sell_count_suffix',0x2afa64,0x2afaf4)):
            d,en=bykey[key]
            suffix=dg.encode_mixed(en,self.mapping)
            for name in (names if key=='buy_suffix' else ['1','9','99']):
                prefix=dg.encode_mixed('「'+name,self.mapping)
                c=CPU(out);dest=0x3000000
                c.put(dest,prefix+b'\xcc'*64)
                c.r[9]=dest+len(prefix)
                c.r[11]=int(d['context']['eboot_offset'],16)+0x10000
                c.run(start,{end})
                self.assertEqual(c.read(dest,len(prefix)+len(suffix)),prefix+suffix)
                self.assertEqual(c.read(dest+len(prefix)+len(suffix),8),b'\xcc'*8)
        # Compiler-inlined middle suffix must agree with its TOC source.
        c=CPU(out);dest=0x3000000
        c.put(dest,b'\xcc'*32);c.r[9]=0;c.r[11]=dest;c.r[27]=dest
        c.run(0x2af9bc,{0x2af9e8})
        self.assertEqual(c.read(dest,4),dg.encode_mixed(bykey['sell_name_suffix'][1],self.mapping))
        self.assertEqual(c.read(dest+4,8),b'\xcc'*8)

    def test_spirit_ui_pristine_and_installed_composition(self):
        widgets={int(w,16) for _,d,_ in S.rows() for w in d['context'].get('widgets',[])}
        self.assertEqual(widgets,{0xabb74,0xac854,0xaca34,0xaca94,0xacc54})
        refs=aiddata.refs(self.ui)
        for _,d,_ in S.rows():
            registered={int(w,16) for w in d['context'].get('widgets',[])}
            if registered:
                found={r for p,j,_,_ in aiddata.strings(self.ui) if j==d['source']
                       for r in refs.get(p,[])}
                self.assertEqual(found,registered,d['source'])
        allowed={p for r in widgets for p in range(r,r+4)}
        for before in (self.ui,self.current):
            out=S.apply_ui(before,self.mapping,self.widths,self.ui)
            self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(before,out))))
            for r in widgets:
                self.assertEqual(before[r+4:r+32],out[r+4:r+32])
            self.assertEqual(text(out,0xaca34),b'')
            self.assertEqual(text(out,0xaca94),b'')
            self.assertEqual(text(out,0xabb74),dg.encode_mixed('SP Cost\nSP',self.mapping,newline=b'\n'))
            # Name insertion, numbers, confirmation controls and suffix survive.
            for r in (0xac874,0xacc74,0xaca54,0xacab4,0xaca74,0xabb94,0xabbb4,0xabbd4):
                self.assertEqual(before[r:r+32],out[r:r+32])


if __name__=='__main__':
    unittest.main()
