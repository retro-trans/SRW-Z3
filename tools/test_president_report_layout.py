"""Execute the emitted PPC; check centering, registers and fallback isolation."""
import json,struct,unittest
from pathlib import Path
import eboot,digraph as dg
import president_report_layout as W
from check_confirmation_tabs import f32


def execute(mapping,widths,text,style,cp932=1,date_cards=False,caller=0,extra_rows=None):
    mem={}
    def put(p,b):mem.update(enumerate(b,p))
    def get(p,n):return bytes(mem[p+i] for i in range(n))
    def signed(x,n):return x-(1<<n) if x&(1<<(n-1)) else x
    mask=(1<<64)-1
    r=[0x2000000+i*0x100 for i in range(32)]
    r[3]=0x3100000;r[7]=cp932
    initial=r[:];stack=r[1]
    f=[int.from_bytes(struct.pack('>d',i+.125),'big') for i in range(32)]
    def rf(i):return struct.unpack('>d',f[i].to_bytes(8,'big'))[0]
    def wf(i,x):f[i]=int.from_bytes(struct.pack('>d',x),'big')
    wf(1,640);fi=f[:]
    put(r[3],text+b'\0')
    for va,raw in W.regions(mapping,date_cards):put(va,raw)
    for va,jp in zip(W.JP_VAS,W.battle_reports.HOOKS):put(va,jp.encode('cp932')+b'\0')
    # Simulate the exact lookup rows used by the added reward whitelist.
    import trdata
    trdata.use_glossary('analysis/glossary.json')
    translated=eboot.load_ui_hook()
    rows=[];ptr=0x3300000
    for jp in W.centered_lines():
        key=jp.encode('cp932')+b'\0';en=eboot._encode_marked(translated[jp],mapping)+b'\0'
        rows.append(struct.pack('>II',ptr,ptr+len(key)))
        put(ptr,key+en);ptr+=len(key)+len(en)
    for va,jp,en in W.bonus_centering.rows():
        put(va,jp.encode('cp932')+b'\0')
        raw=eboot._encode_marked(en,mapping)+b'\0'
        rows.append(struct.pack('>II',va,ptr));put(ptr,raw);ptr+=len(raw)
    for key,en in (extra_rows or {}).items():
        key+=b'\0';en+=b'\0'
        rows.append(struct.pack('>II',ptr,ptr+len(key)))
        put(ptr,key+en);ptr+=len(key)+len(en)
    put(eboot.NAME_TBL,b''.join(rows)+bytes(8))
    put(eboot.TABLE_VA,bytes(widths.get(i,32) for i in range(eboot.ATLAS_CELLS)))
    state=0x3200000;put(state,style);put(r[2]-0x7f3c,struct.pack('>I',state))
    pc,cr=W.SITE,0xa53cc35a
    for steps in range(100000):
        if pc in (W.SITE+4,eboot.NAME_SITE):break
        word=int.from_bytes(get(pc,4),'big');pc+=4
        op,rt,ra,rb=word>>26,(word>>21)&31,(word>>16)&31,(word>>11)&31
        imm=signed(word&65535,16);xo=(word>>1)&1023
        if op in (14,15):r[rt]=((r[ra] if ra else 0)+imm*(65536 if op==15 else 1))&mask
        elif op==24:r[ra]=r[rt]|(word&65535)
        elif op==7:r[rt]=(r[ra]*imm)&mask
        elif op==31 and xo==266:r[rt]=(r[ra]+r[rb])&mask
        elif op==31 and xo==444:r[ra]=r[rt]|r[rb]
        elif op==31 and xo==19:r[rt]=cr
        elif word==0x7d2802a6:r[9]=caller
        elif op==31 and xo==144:
            assert (word>>12)&255==255
            cr=r[rt]&0xffffffff
        elif op in (32,34,40,58):
            size={32:4,34:1,40:2,58:8}[op]
            r[rt]=int.from_bytes(get(r[ra]+imm,size),'big')
        elif op==31 and xo==87:r[rt]=get(r[ra]+r[rb],1)[0]
        elif op in (10,11) or op==31 and xo==32:
            lhs=r[ra]&0xffffffff
            rhs=r[rb]&0xffffffff if op==31 else word&65535
            if op==11:lhs=signed(lhs,32);rhs=imm
            cr=(cr&0x0fffffff)|((8 if lhs<rhs else 4 if lhs>rhs else 2)<<28)
        elif op==18:
            assert not word&3
            pc=pc-4+signed(word&0x3fffffc,26)
        elif op==16:
            assert rt in (4,12)
            if bool(cr&(1<<(31-ra)))==(rt==12):pc=pc-4+signed(word&0xfffc,16)
        elif op in (36,62,54):
            offset=signed(word&0xfffc,16) if op==62 else imm
            address=r[ra]+offset
            size=4 if op==36 else 8
            assert stack-0xc0<=address<=stack-8,hex(address)
            value=f[rt] if op==54 else r[rt]
            put(address,value.to_bytes(8,'big')[-size:])
            if op==62 and word&3==1:r[ra]=address
        elif op==48:wf(rt,struct.unpack('>f',get(r[ra]+imm,4))[0])
        elif op==50:f[rt]=int.from_bytes(get(r[ra]+imm,8),'big')
        elif op==63 and xo==846:wf(rt,float(signed(f[rb],64)))
        elif op==63 and xo==12:wf(rt,f32(rf(rb)))
        elif op==59 and (word>>1)&31 in (20,21,25):
            kind=(word>>1)&31
            wf(rt,f32(rf(ra)-rf(rb) if kind==20 else
                      rf(ra)+rf(rb) if kind==21 else rf(ra)*rf((word>>6)&31)))
        else:raise AssertionError('Unknown instruction %08x at %x'%(word,pc-4))
    else:raise AssertionError('wrapper did not tail-call')
    assert cr==0xa53cc35a
    assert all(r[i]==initial[i] for i in range(32) if i!=1)
    assert all(f[i]==fi[i] for i in range(32) if i!=1)
    assert r[1]==stack-(0xc0 if pc==W.SITE+4 else 0)
    return pc,rf(1)


def style(quad,pitch,alternate=0,flags=()):
    b=bytearray(0xc0)
    for off,value in [(0x54,quad),(0x5c,pitch),(0x78,quad+3),(0x80,pitch+5),
                      (0x88,quad+7),(0x90,pitch+11)]:struct.pack_into('>f',b,off,value)
    struct.pack_into('>H',b,0xac,alternate)
    for flag in flags:b[flag]=1
    return b


def expected_width(raw,widths,s):
    total=0
    for i in range(0,len(raw),2):
        code=int.from_bytes(raw[i:i+2],'big');off=0x54
        if struct.unpack_from('>H',s,0xac)[0]:
            off=0x78
            for flag,lo,hi in [(0xae,0x8260,0x8279),(0xaf,0x8281,0x829a),
                               (0xb0,0x829f,0x82f1),(0xb1,0x8340,0x8491),
                               (0xb2,0x8140,0x825f)]:
                if lo<=code<=hi and s[flag]:off=0x88
        w=widths.get(dg.cell_index(code),32)
        quad,pitch=struct.unpack_from('>f',s,off)[0],struct.unpack_from('>f',s,off+8)[0]
        total+=pitch if w==32 else quad*w/32
    return total


class PresidentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import trdata
        trdata.use_glossary('analysis/glossary.json')
        p=Path('work/out_0.6.3')
        if not (p/'pairs.json').exists():raise unittest.SkipTest('local candidate unavailable')
        cls.mapping=json.loads((p/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((p/'widths.json').read_text()).items()}
        cls.elf=(p/'EBOOT.BIN').read_bytes()

    def test_emitted_ppc_center_and_register_preservation(self):
        examples=[(jp.encode('cp932'),dg.encode_mixed(en,self.mapping))
                  for jp,en in W.battle_reports.HOOKS.items()]
        for n in ('０','５','１０','５０','１００','９９９９','２１４７４８３６４７'):
            raw=W.battle_reports.format_bytes(self.mapping).split(b'\0')[0].replace(b'%s',n.encode('cp932'))
            examples.append((raw,raw))
        cases=0
        for q,p in [(28,28),(28,32),(31,35),(20,28)]:
            for alt,flags in [(0,()),(1,()),(1,(0xb2,)),(1,(0xb1,)),(1,tuple(range(0xae,0xb3)))]:
                s=style(q,p,alt,flags)
                for raw,rendered in examples:
                    dest,x=execute(self.mapping,self.widths,raw,s)
                    self.assertEqual(dest,eboot.NAME_SITE)
                    self.assertAlmostEqual(x+expected_width(rendered,self.widths,s)/2,640,places=4)
                    cases+=1
        print('PASS: %d emitted-PPC President centering/register cases.'%cases)

    def test_unrelated_malformed_and_non_cp932_unchanged(self):
        fmt=W.battle_reports.format_bytes(self.mapping).split(b'\0')[0]
        cases=[b'',b'A','別の報酬です'.encode('cp932')]
        cases += [fmt.replace(b'%s',n) for n in [b'',b'5','５'.encode('cp932')*11,'Ａ'.encode('cp932')]]
        for jp in W.battle_reports.HOOKS:
            raw=jp.encode('cp932');cases.extend(raw[:i] for i in range(len(raw)))
            cases.append(raw+b'!')
        for raw in cases:
            self.assertEqual(execute(self.mapping,self.widths,raw,style(28,32)),(W.SITE+4,640))
        for jp in W.battle_reports.HOOKS:
            self.assertEqual(execute(self.mapping,self.widths,jp.encode('cp932'),style(28,32),0),(W.SITE+4,640))

    def test_candidate_byte_isolation_and_hook_agreement(self):
        W.check(self.elf,self.mapping)
        # Also runnable after packing: restore just this patch's own regions.
        b=bytearray(self.elf);segs=eboot._segments(b)
        for va,raw in W.regions(self.mapping):
            p=eboot._off(segs,va)
            b[p:p+len(raw)]=struct.pack('>I',W.ORIGINAL) if va==W.SITE else bytes(len(raw))
        new=W.apply(b,self.mapping)
        self.assertEqual(new,self.elf)
        allowed={p+i for va,raw in W.regions(self.mapping)
                 for p in [eboot._off(segs,va)] for i in range(len(raw))}
        self.assertEqual(len(b),len(new))
        self.assertTrue(all(a==v or i in allowed for i,(a,v) in enumerate(zip(b,new))))
        self.assertEqual(b[W.battle_reports.FORMAT_OFF:W.battle_reports.FORMAT_OFF+40],
                         new[W.battle_reports.FORMAT_OFF:W.battle_reports.FORMAT_OFF+40])


if __name__=='__main__':unittest.main()
