"""Execute the emitted link-width hooks; no game build or install."""
import json
import struct
import unittest
from pathlib import Path
import eboot
import digraph as dg
import link_background_layout as L
from check_confirmation_tabs import execute as glyph_advance


def run(code, regs, memory, floats):
    """Small strict interpreter for the three straight-line PPC helpers."""
    def get(p,n): return bytes(memory[p+i] for i in range(n))
    def put(p,b): memory.update(enumerate(b,p))
    changed=set()
    for pos in range(0,len(code),4):
        w=int.from_bytes(code[pos:pos+4],'big')
        if w==0x4e800020: return changed
        op,t,a,b=w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
        imm=w&65535;imm=imm-65536 if imm&32768 else imm
        if op==15: regs[t]=((regs[a] if a else 0)+(imm<<16))&0xffffffffffffffff
        elif op==24: regs[a]=regs[t]|(w&65535)
        elif op==7: regs[t]=regs[a]*imm
        elif op==32: regs[t]=int.from_bytes(get(regs[a]+imm,4),'big')
        elif op==31 and (w>>1)&1023==266: regs[t]=regs[a]+regs[b]
        elif op==31 and (w>>1)&1023==444: regs[a]=regs[t]|regs[b]
        elif op==21:
            assert (w>>11)&31==0 and (w>>6)&31==24 and (w>>1)&31==31
            regs[a]=regs[t]&255
        elif op==48:
            assert a!=0
            floats[t]=get(regs[a]+imm,4)
        elif op in (38,52):
            assert a!=0
            raw=bytes([regs[t]&255]) if op==38 else floats[t]
            address=regs[a]+imm;put(address,raw);changed.update(range(address,address+len(raw)))
        else: raise AssertionError(hex(w))
    raise AssertionError('missing return')


class LinkBackground(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        root=Path('work/build_0.6.12_approved_subtitle')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}

    def fixture(self):
        regs=[0x3000000+i*0x1000 for i in range(32)]
        floats=[struct.pack('>f',i+.25) for i in range(32)]
        memory={}
        memory.update(enumerate(bytes(1024),L.WIDTHS))
        return regs,memory,floats

    def test_all_slots_and_metadata(self):
        regs,mem,f=self.fixture();initial=regs[:];initialf=f[:]
        put=lambda p,b:mem.update(enumerate(b,p))
        capture,select,draw=L.stubs()
        record=bytes(range(20))
        for index in range(256):
            regs[:]=initial;f[:]=initialf
            regs[3]=18;put(regs[28],record)
            value=struct.pack('>f',index+.375)
            put(eboot.PEN_ACC,value)
            put(regs[1]+0x70,struct.pack('>II',index//16,index%16))
            changed=run(capture,regs,mem,f)
            self.assertEqual(changed,{initial[28]+4}|set(range(L.WIDTHS+index*4,L.WIDTHS+index*4+4)))
            self.assertEqual(bytes(mem[initial[28]+i] for i in range(20)),record[:4]+b'\x12'+record[5:])
            self.assertEqual(bytes(mem[eboot.PEN_ACC+i] for i in range(4)),value)
            self.assertTrue(all(regs[i]==initial[i] for i in set(range(32))-{0,3,9,10}))
            self.assertTrue(all(f[i]==initialf[i] for i in set(range(32))-{13}))
        # Lookup a cached width after PEN_ACC changed for later dialogue.
        for index in (0,1,15,16,127,255,-1,256):
            regs[:]=initial;f[:]=initialf;regs[4]=index
            run(select,regs,mem,f)
            self.assertEqual(regs[29],regs[3])
            self.assertTrue(all(regs[i]==initial[i] for i in set(range(32))-{0,4,9,29}))
            # The original code/callee can clobber f0 before the draw hook.
            f[0]=struct.pack('>f',999.)
            before=bytes(range(32));put(regs[31],before)
            changed=run(draw,regs,mem,f)
            self.assertEqual(changed,set(range(regs[31]+8,regs[31]+12)))
            expected=struct.pack('>f',(index&255)+.375)
            self.assertEqual(bytes(mem[regs[31]+i] for i in range(32)),before[:8]+expected+before[12:])
        # Slot reuse replaces its prior width rather than accumulating it.
        regs[:]=initial;put(regs[1]+0x70,bytes(8));put(eboot.PEN_ACC,struct.pack('>f',44.5))
        run(capture,regs,mem,f)
        self.assertEqual(bytes(mem[L.WIDTHS+i] for i in range(4)),struct.pack('>f',44.5))

    def test_width_from_real_glyph_advances(self):
        widths=bytes(self.widths.get(i,32) for i in range(eboot.ATLAS_CELLS))
        for label in ('Kei','Kira','Alto','ZEXIS','Kurara','Hibiki','Otsuka','Destruction Incident','Regeneration War','W','iiii','日本'):
            raw=dg.encode_mixed(label,self.mapping)
            for pitch,quad in ((31,23.25),(28,28),(42,28)):
                acc=0.
                for i in range(0,len(raw),2):
                    cell=dg.cell_index(int.from_bytes(raw[i:i+2],'big'))
                    _,acc=glyph_advance(eboot.vwf_stub(),widths,cell,0,0,pitch,quad,acc)
                regs,mem,f=self.fixture();put=lambda p,b:mem.update(enumerate(b,p))
                put(regs[1]+0x70,bytes(8));put(eboot.PEN_ACC,struct.pack('>f',acc))
                run(L.stubs()[0],regs,mem,f);regs[4]=0
                run(L.stubs()[1],regs,mem,f);run(L.stubs()[2],regs,mem,f)
                actual=struct.unpack('>f',bytes(mem[regs[31]+8+j] for j in range(4)))[0]
                self.assertEqual(actual,acc)
                if label in ('Alto','ZEXIS','Kurara'): self.assertLess(actual,len(label)*pitch)
                if label=='日本': self.assertEqual(actual,2*pitch)

    def test_source_guards_and_patch_isolation(self):
        b=bytearray(self.source);segs=eboot._segments(b)
        size=segs[1]['off']-segs[0]['off']
        struct.pack_into('>QQ',b,segs[0]['hdr']+32,size,size)
        eboot.add_segment(b);segs=eboot._segments(b)
        # Exercise real font/keyword pipeline; only in memory.
        report=eboot.apply_vwf(b,segs,self.widths);L.check(b)
        expected=set(range(len(self.source),len(b)))
        for lo,hi in [report['site'],report['stub'],report['table'],*report['kw']]:expected.update(range(lo,hi))
        for s in segs:expected.update(range(s['hdr'],s['hdr']+56))
        expected.update(range(0x38,0x3a))
        self.assertTrue(all(a==z or i in expected for i,(a,z) in enumerate(zip(self.source,b))))
        # The original function never references our spare stack slot.
        import capstone
        dis=capstone.Cs(capstone.CS_ARCH_PPC,capstone.CS_MODE_64|capstone.CS_MODE_BIG_ENDIAN)
        code=self.source[0x1b8584:0x1b87b8]
        self.assertFalse(any('0x88(r1)' in i.op_str for i in dis.disasm(code,0x1c8584)))
        broken=bytearray(self.source);broken[0x1be140]^=1
        with self.assertRaises(AssertionError):L.guard_source(broken,eboot._segments(broken))


if __name__=='__main__':unittest.main()
