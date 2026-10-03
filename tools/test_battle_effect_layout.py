"""Execute the emitted effect-layout PPC, including unrelated-call fallbacks."""
import json
import struct
import unittest
from pathlib import Path
import eboot
import battle_effect_layout as layout
import localization
from intermission_layout import ink


def execute(code, table, pointer, center, size, caller=layout.CALLER, encoding=0, font=0):
    mem = {}
    def put(p, raw): mem.update(enumerate(raw, p))
    def get(p, n): return bytes(mem[p+i] for i in range(n))
    def signed(v, bits): return v-(1<<bits) if v&(1<<(bits-1)) else v
    def f32(v): return struct.unpack('>f', struct.pack('>f', v))[0]
    r = [0x3000000+i*0x10000 for i in range(32)]
    r[2]=0x7dd920; r[3]=pointer; r[7]=encoding
    f=[i+.25 for i in range(32)]; f[1]=center
    put(r[1]+0xb0, struct.pack('>Q',caller))
    style=0x5000000
    put(r[2]-0x7f3c,struct.pack('>I',style))
    put(style+0xac,struct.pack('>H',font))
    put(style+0x54,struct.pack('>f',size))
    put(layout.CAVE,code); put(layout.TABLE,table)
    initial=r[:]; initialf=f[:]; pc=layout.CAVE; cr=0xa53cc35a
    for _ in range(1000):
        if pc in (0x140f4,0x14954):break
        w=int.from_bytes(get(pc,4),'big');pc+=4
        op,t,a,b=w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
        imm=signed(w&65535,16);xo=(w>>1)&1023
        if op in (14,15):r[t]=((r[a] if a else 0)+imm*(65536 if op==15 else 1))&((1<<64)-1)
        elif op==24:r[a]=r[t]|(w&65535)
        elif op in (32,40):r[t]=int.from_bytes(get(r[a]+imm,4 if op==32 else 2),'big')
        elif op==58:r[t]=int.from_bytes(get(r[a]+signed(w&0xfffc,16),8),'big')
        elif op==11 or (op==31 and xo==32):
            av=signed(r[a]&0xffffffff,32) if op==11 else r[a]&0xffffffff
            bv=imm if op==11 else r[b]&0xffffffff
            cr=(cr&0xfffffff)|((8 if av<bv else 4 if av>bv else 2)<<28)
        elif op==18:
            assert w&3==0
            pc=pc-4+signed(w&0x3fffffc,26)
        elif op==16:
            assert t in (4,12)
            if bool(cr&(1<<(31-a)))==(t==12):pc=pc-4+signed(w&0xfffc,16)
        elif op==48:f[t]=struct.unpack('>f',get(r[a]+imm,4))[0]
        elif op==59 and (w>>1)&31 in (21,25):
            f[t]=f32(f[a]+f[b] if (w>>1)&31==21 else f[a]*f[(w>>6)&31])
        else:raise AssertionError(hex(w))
    else:raise AssertionError('unbounded stub')
    assert all(r[i]==initial[i] for i in set(range(32))-{9,10,11})
    assert all(f[i]==initialf[i] for i in set(range(32))-{0,1,13})
    assert cr&0xfffffff==0x053cc35a
    return pc,f[1]


class EffectLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.24_english_20260930')
        cls.before=(root/'EBOOT.BIN').read_bytes()
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cls.built=layout.patch(cls.before,cls.mapping,cls.widths)
        cls.table=layout.table(cls.built,cls.mapping,cls.widths)

    def test_all_effects_center_and_preserve_registers(self):
        cat=localization.english()
        for mid,_,refs in layout.labels.BINDINGS:
            for ref in refs:
                ptr=struct.unpack_from('>I',self.before,ref)[0]
                for size in (24,28,32):
                    for center in (160.,640.,1120.):
                        pc,x=execute(layout.stub(),self.table,ptr,center,size)
                        self.assertEqual(pc,0x140f4)
                        self.assertAlmostEqual(x+ink(cat.text(mid),self.mapping,self.widths,size)/2,center,places=4)

    def test_unrelated_callers_encodings_fonts_and_strings_fall_back(self):
        ptr=struct.unpack_from('>I',self.table)[0]
        for changes in ({'caller':0},{'caller':layout.CALLER+4},{'encoding':1},{'font':1},{'pointer':0x123456}):
            args=dict(pointer=ptr,center=640.,size=32);args.update(changes)
            self.assertEqual(execute(layout.stub(),self.table,**args),(0x14954,640.))

    def test_lambda_driver_reproduces_old_left_shift(self):
        width=ink('Lambda Driver',self.mapping,self.widths,32)
        old_width=len('Lambda Driver')*32
        self.assertGreater((old_width-width)/2,80)
        self.assertLess(width,360)

    def test_only_hook_and_reserved_rx_bytes_change(self):
        segs=eboot._segments(self.built);allowed=set()
        for va,n in ((layout.SITE,4),(layout.CAVE,len(layout.stub())),(layout.TABLE,len(self.table))):
            off=eboot._off(segs,va);allowed.update(range(off,off+n))
        self.assertEqual(len(self.before),len(self.built))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.before,self.built))))
        import ppc_permissions
        ppc_permissions.check_changed_branches(Path('work/EBOOT_dec.elf').read_bytes(),self.built)
        import sys
        sys.path.insert(0,'platforms/ps3')
        import cfw_loader_layout
        folded=cfw_loader_layout.fold(self.built)
        layout.check(folded,self.mapping,self.widths)
        ppc_permissions.check_changed_branches(Path('work/EBOOT_dec.elf').read_bytes(),folded)

    def test_rejects_source_drift_or_occupied_cave(self):
        segs=eboot._segments(self.before)
        for va in (0x103600,layout.SITE,layout.CAVE,layout.TABLE):
            bad=bytearray(self.before);bad[eboot._off(segs,va)]^=1
            with self.assertRaises(AssertionError):layout.patch(bad,self.mapping,self.widths)


if __name__=='__main__':unittest.main()
