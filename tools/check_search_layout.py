"""Execute the actual screen-local PPC stub; no emulator visual QA implied."""
import json
import struct
from pathlib import Path
import eboot
import digraph as dg
import search_layout as layout
from check_confirmation_tabs import f32


def execute(code, widths, raw, record, x, sizes, flags=(1,1,1,1,1), mode=1,
            copied=None, caller=0):
    memory = {}
    def put(p, b): memory.update(enumerate(b, p))
    def get(p,n): return bytes(memory[p+i] for i in range(n))
    def signed(n,bits): return n-(1<<bits) if n & (1<<(bits-1)) else n
    r = [0x3000000+i*0x10000 for i in range(32)]
    r[2] = 0x7dd920
    f = [struct.pack('>d',i+.25) for i in range(32)]
    def rf(i): return struct.unpack('>d',f[i])[0]
    def wf(i,v): f[i] = struct.pack('>d',v)
    wf(1,x)
    r[7]=1
    ui, recbase, style = r[26], 0x4000000, 0x5000000
    r[31] = recbase + record-layout.RECORD_BASE
    stack = r[1]
    put(stack+0xf0, struct.pack('>Q',caller))
    if copied is not None:
        # 0x510cc's 0xe0-byte frame below the grid frame; clone is at +0x78.
        r[31] = stack+0xe0+0x78
        put(r[31],copied)
    put(ui+0x50,struct.pack('>I',recbase))
    put(r[2]-0x7f3c,struct.pack('>I',style))
    put(style+0xac,struct.pack('>H',mode))
    for off,value in zip((0x54,0x78,0x88), sizes): put(style+off,struct.pack('>f',value))
    for off,value in zip((0xae,0xaf,0xb0,0xb1,0xb2),flags): put(style+off,bytes([value]))
    put(layout.CAVE,code); put(eboot.TABLE_VA,widths); put(r[3],raw+b'\0')
    initial, initialf = r[:],f[:]
    pc, cr = layout.CAVE, 0xa53cc35a
    for _ in range(30000):
        if pc in (0x140f4,0x14954): break
        w=int.from_bytes(get(pc,4),'big'); pc+=4
        op,t,a,b=w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
        imm=signed(w&65535,16); xo=(w>>1)&1023
        if op in (14,15): r[t]=((r[a] if a else 0)+imm*(65536 if op==15 else 1))&((1<<64)-1)
        elif op==24: r[a]=r[t]|(w&65535)
        elif op in (32,34,40): r[t]=int.from_bytes(get(r[a]+imm,{32:4,34:1,40:2}[op]),'big')
        elif op==58: r[t]=int.from_bytes(get(r[a]+signed(w&0xfffc,16),8),'big')
        elif op==31 and xo==87: r[t]=get(r[a]+r[b],1)[0]
        elif op==31 and xo in (266,40,444):
            if xo==444: r[a]=r[t]|r[b]
            else: r[t]=(r[a]+r[b] if xo==266 else r[b]-r[a])&((1<<64)-1)
        elif op==7: r[t]=(signed(r[a]&0xffffffff,32)*imm)&((1<<64)-1)
        elif op in (10,11) or (op==31 and xo==32):
            av = (signed(r[a]&0xffffffff,32) if op==11 else r[a]&0xffffffff)
            bv = imm if op==11 else (w&65535 if op==10 else r[b]&0xffffffff)
            cr=(cr&0x0fffffff)|((8 if av<bv else 4 if av>bv else 2)<<28)
        elif op==18:
            assert w&3==0
            pc=pc-4+signed(w&0x3fffffc,26)
        elif op==16:
            assert t in (4,12)
            if bool(cr&(1<<(31-a)))==(t==12): pc=pc-4+signed(w&0xfffc,16)
        elif op in (36,62):
            off=signed(w&0xfffc,16) if op==62 else imm
            address=r[a]+off
            assert stack-0x80<=address<stack
            put(address,r[t].to_bytes(8,'big')[-(8 if op==62 else 4):])
            if op==62 and w&3==1: r[a]=address
        elif op==48: wf(t,struct.unpack('>f',get(r[a]+imm,4))[0])
        elif op==50: f[t]=get(r[a]+imm,8)
        elif op==63 and xo==846: wf(t,float(signed(int.from_bytes(f[b],'big'),64)))
        elif op==63 and xo==12: wf(t,f32(rf(b)))
        elif op==59 and (w>>1)&31 in (20,21,25):
            kind=(w>>1)&31
            wf(t,f32(rf(a)-rf(b) if kind==20 else rf(a)+rf(b) if kind==21 else rf(a)*rf((w>>6)&31)))
        else: raise AssertionError('unknown PPC %08x at %x'%(w,pc-4))
    else: raise AssertionError('stub loop')
    assert all(r[i]==initial[i] for i in set(range(32))-{0,9,10,11,12})
    assert all(f[i]==initialf[i] for i in set(range(32))-{0,1,12,13})
    assert cr&0x0fffffff==0x053cc35a
    return pc,rf(1)


def grid_copy(pristine, ui, record):
    """Replay the real grid's eight lwz/stw pairs, not an original-pointer fixture."""
    segs=eboot._segments(pristine)
    def word(va): return struct.unpack_from('>I',pristine,eboot._off(segs,va))[0]
    # The colored-entry path uses that copy for both style and drawing.
    expected={0xadecc:0x390f02f0, 0xadf4c:0x38010078,
              0xadf60:0xf80100f0, 0xae3d0:0xe88100f0,
              0xae3e4:0xe88100f0, 0x51100:0xf80100f0}
    for va,value in expected.items(): assert word(va)==value,(hex(va),hex(word(va)))
    assert word(0xae404)==0x48000001|((0x510cc-0xae404)&0x3fffffc)
    result=bytearray(32); regs={}
    # Includes interspersed extsw; only the eight loads and stores copy bytes.
    for va in range(0xaded0,0xadf14,4):
        w=word(va); op=w>>26; reg=(w>>21)&31; base=(w>>16)&31; off=w&65535
        if op==32:
            assert base==3 and off in range(0,32,4)
            regs[reg]=ui[record+off:record+off+4]
        elif op==36:
            assert base==1 and off in range(0x78,0x98,4)
            result[off-0x78:off-0x74]=regs[reg]
        else: assert va==0xaded8  # extsw r8,r8, unrelated to the copy
    assert result==ui[record:record+32]
    assert int.from_bytes(result[:4],'big') in layout.GRID_STRINGS
    return bytes(result)


def check(blob,mapping,ui):
    import aiddata
    segs=eboot._segments(blob)
    code=blob[eboot._off(segs,layout.CAVE):eboot._off(segs,layout.CAVE)+len(layout.stub())]
    assert code==layout.stub()
    assert struct.unpack_from('>I',blob,eboot._off(segs,layout.SITE))[0]==0x48000001|((layout.CAVE-layout.SITE)&0x3fffffc)
    widths=blob[eboot._off(segs,eboot.TABLE_VA):eboot._off(segs,eboot.TABLE_VA)+eboot.ATLAS_CELLS]
    names=[v for k,v in json.loads(Path('translation/spirits.json').read_text(encoding='utf-8')).items() if not k.startswith('_')]
    names+=list(layout.TAB_TEXT)
    cases=0
    for name in names:
        raw=dg.encode_mixed(name,mapping)
        codes=[int.from_bytes(raw[i:i+2],'big') for i in range(0,len(raw),2)]
        for mode,sizes,flags in [(0,(31,42,28),(1,)*5),(1,(31,42,28),(1,)*5),(1,(31,42,28),(0,)*5)]:
            def quad(c):
                if not mode:return sizes[0]
                alt=any(flag and lo<=c<=hi for flag,lo,hi in zip(flags,(0x8260,0x8281,0x829f,0x8340,0x8140),(0x8279,0x829a,0x82f1,0x8491,0x825f)))
                return sizes[2 if alt else 1]
            for center in (160.,400.,640.,880.,1120.):
                pc,x=execute(code,widths,raw,layout.GRID[cases%4],center,sizes,flags,mode)
                if any(widths[dg.cell_index(c)]==32 for c in codes):
                    assert pc==0x14954 and x==center
                else:
                    expected=sum(widths[dg.cell_index(c)]*quad(c)/32 for c in codes)
                    assert pc==0x140f4 and abs(x+expected/2-center)<.001,(name,x,expected)
                cases+=1
    for raw in ('？？？？'.encode('cp932'),b'hello',b'\x81',b'\x97\xfc'):
        pc,x=execute(code,widths,raw,layout.GRID[0],160.,(31,42,28))
        assert pc==0x14954 and x==160.
    for record in (0xa9974,0xb0d14,layout.GRID[0]-32,layout.GRID[-1]+32):
        pc,x=execute(code,widths,dg.encode_mixed('Intuition',mapping),record,160.,(31,42,28))
        assert pc==0x14954 and x==160.
    for record,text in zip(layout.TABS,layout.TAB_TEXT):
        off=aiddata.STR_BASE+struct.unpack_from('>I',ui,record)[0]
        raw=ui[off:ui.index(b'\0',off)]
        assert raw==dg.encode_mixed(text,mapping)
        pc,x=execute(code,widths,raw,record,640.,(31,28,26))
        assert pc==0x140f4 and 2*(640-x)<220,('tab overflow',text,x)
    pristine=Path('work/EBOOT_dec.elf').read_bytes()
    copied_cases=0
    for record in layout.GRID:
        copied=grid_copy(pristine,ui,record)
        for name in names:
            raw=dg.encode_mixed(name,mapping)
            for center in (160.,400.,640.,880.,1120.):
                expected=execute(code,widths,raw,record,center,(31,42,28))
                actual=execute(code,widths,raw,record,center,(31,42,28),
                               copied=copied,caller=layout.GRID_CALLER)
                assert actual==expected,('copied grid entry',name,actual,expected)
                copied_cases+=1
        for raw in ('？？？？'.encode('cp932'),b'hello',b'\x81'):
            assert execute(code,widths,raw,record,160.,(31,42,28),
                           copied=copied,caller=layout.GRID_CALLER)==(0x14954,160.)
        raw=dg.encode_mixed('Intuition',mapping)
        # Same template in another caller, or another template in this caller,
        # must not opt in to the new exception.
        for caller,data in [(0xae408+4,copied),(0,copied),
                            (layout.GRID_CALLER,b'\0'*4+copied[4:])]:
            assert execute(code,widths,raw,record,160.,(31,42,28),
                           copied=data,caller=caller)==(0x14954,160.)
    print('PASS: %d original-record and %d real-template-copy PPC cases; nine tabs; unrelated callers unchanged.'%(cases,copied_cases))
