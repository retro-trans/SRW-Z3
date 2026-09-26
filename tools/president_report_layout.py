"""Center President and exact stage reward report lines by rendered advance.

The centered drawer measures Japanese before NAME_SITE substitutes English.
Its public entry is wrapped; exact strings opt in and every other call keeps
the displaced prologue. No report constructor, amount or text buffer changes.
"""
import struct
import digraph as dg
import battle_reports
import gift_reports
import bonus_centering

SITE = 0x14954
CAVE = 0x78F000
DATA = 0x78F800
END = 0x790000
ORIGINAL = 0xF821FF41  # stdu r1,-0xc0(r1)
JP_VAS = (0x6F4F30, 0x6F4F50)


def centered_lines():
    return list(gift_reports.centered_lines()) + [bonus_centering.LOCK]


def bonus_table(mapping):
    end = DATA + sum(map(len, strings(mapping)))
    end += sum(len(jp.encode('cp932')) + 1 for jp in centered_lines()) + 1
    return (end + 3) & ~3


def strings(mapping):
    return [dg.encode_mixed(s,mapping)+b'\0' for s in
            list(battle_reports.HOOKS.values())+[' PP.']]


def stub(mapping,date_cards=False):
    import eboot
    P,a=eboot._ppc(),eboot._Asm()
    def emit(op,*args): a.emit(P[op](*args))
    def const(r,v):
        emit('lis',r,v>>16);emit('ori',r,r,v&65535)
    def tail(dest): emit('b',dest-(CAVE+4*len(a.w)))
    data=strings(mapping)
    ptrs=[DATA,DATA+len(data[0]),DATA+len(data[0])+len(data[1])]
    emit('stdu',1,1,-0xa0)
    for r,off in [(0,0x30),(9,0x38),(10,0x40),(11,0x48),(12,0x50)]:
        emit('std',r,1,off)
    a.emit(0x7C000026)  # mfcr r0
    emit('std',0,1,0x58)
    for f,off in [(0,0x60),(12,0x68),(13,0x70)]:
        a.emit(0xD8000000|(f<<21)|(1<<16)|off)  # stfd
    emit('cmpwi',7,1);a.br('bne','fallback')
    if date_cards:
        # Only the native full-screen date-card caller opts in. Look up the
        # whole composed string; unknown cards keep native behavior.
        a.emit(0x7D2802A6)  # mflr r9; LR itself is never changed
        const(11,0x14c58c)
        emit('cmplw',9,11);a.br('beq','gift_lookup')
    # Reward reports use the same centered drawer. Opt in only the reviewed
    # single-line keys; obtain English from the normal hook table so glossary
    # changes cannot leave a stale duplicate measurement string here.
    const(11,DATA+sum(map(len,data)))
    a.label('gift_key')
    emit('lbz',9,11,0);emit('cmpwi',9,0);a.br('beq','bonus_start')
    emit('mr',12,3)
    a.label('gift_match')
    emit('lbz',9,12,0);emit('lbz',10,11,0)
    emit('cmplw',9,10);a.br('bne','gift_skip')
    emit('cmpwi',9,0);a.br('beq','gift_lookup')
    emit('addi',12,12,1);emit('addi',11,11,1);a.br('b','gift_match')
    a.label('gift_skip')
    emit('lbz',9,11,0);emit('addi',11,11,1)
    emit('cmpwi',9,0);a.br('bne','gift_skip');a.br('b','gift_key')
    a.label('bonus_start');const(12,bonus_table(mapping))
    a.label('bonus_row')
    emit('lwz',11,12,0);emit('cmpwi',11,0);a.br('beq','president')
    emit('mr',9,3)
    a.label('bonus_match')
    emit('lbz',0,9,0);emit('lbz',10,11,0)
    emit('cmplw',0,10);a.br('bne','bonus_next')
    emit('cmpwi',0,0);a.br('beq','gift_lookup')
    emit('addi',9,9,1);emit('addi',11,11,1);a.br('b','bonus_match')
    a.label('bonus_next');emit('addi',12,12,4);a.br('b','bonus_row')
    a.label('gift_lookup');const(12,eboot.NAME_TBL)
    a.label('gift_row')
    emit('lwz',11,12,0);emit('cmpwi',11,0);a.br('beq','fallback')
    emit('mr',9,3)
    a.label('gift_compare')
    emit('lbz',0,9,0);emit('lbz',10,11,0)
    emit('cmplw',0,10);a.br('bne','gift_next_row')
    emit('cmpwi',0,0);a.br('beq','gift_english')
    emit('addi',9,9,1);emit('addi',11,11,1);a.br('b','gift_compare')
    a.label('gift_next_row');emit('addi',12,12,8);a.br('b','gift_row')
    a.label('gift_english');emit('lwz',12,12,4);a.br('b','measure')
    a.label('president')
    for i,va in enumerate(JP_VAS):
        emit('mr',12,3);const(11,va)
        a.label('match%d'%i)
        emit('lbz',9,12,0);emit('lbz',10,11,0)
        emit('cmplw',9,10);a.br('bne','next%d'%i)
        emit('cmpwi',9,0);a.br('beq','english%d'%i)
        emit('addi',12,12,1);emit('addi',11,11,1)
        a.br('b','match%d'%i)
        a.label('english%d'%i);const(12,ptrs[i]);a.br('b','measure')
        a.label('next%d'%i)
    # Only +<1..10 fullwidth decimal digits> PP. is eligible. ASCII,
    # controls, truncated strings and other reward formats remain original.
    emit('mr',12,3)
    for i,b in enumerate(dg.encode_mixed('+',mapping)):
        emit('lbz',9,12,i);emit('cmplwi',9,b);a.br('bne','fallback')
    emit('addi',12,12,len(dg.encode_mixed('+',mapping)))
    emit('addi',11,0,0)
    a.label('digits')
    emit('lbz',9,12,0);emit('cmplwi',9,0x82);a.br('bne','suffix')
    emit('lbz',9,12,1)
    emit('cmplwi',9,0x4f);a.br('blt','suffix')
    emit('cmplwi',9,0x58);a.br('bgt','suffix')
    emit('addi',11,11,1);emit('cmpwi',11,10);a.br('bgt','fallback')
    emit('addi',12,12,2);a.br('b','digits')
    a.label('suffix')
    emit('cmpwi',11,0);a.br('beq','fallback')
    const(11,ptrs[2])
    a.label('suffix_loop')
    emit('lbz',9,12,0);emit('lbz',10,11,0)
    emit('cmplw',9,10);a.br('bne','fallback')
    emit('cmpwi',9,0);a.br('beq','amount')
    emit('addi',12,12,1);emit('addi',11,11,1);a.br('b','suffix_loop')
    a.label('amount');emit('mr',12,3)
    a.label('measure')
    emit('addi',0,0,0);emit('stw',0,1,0x78);emit('lfs',12,1,0x78)
    const(11,eboot.TABLE_VA)
    a.label('glyph')
    emit('lbz',9,12,0);emit('cmpwi',9,0);a.br('beq','done')
    emit('lbz',0,12,1)
    emit('addi',9,9,-0x81);emit('mulli',9,9,192)
    emit('add',9,9,0);emit('addi',9,9,-0x40)
    emit('lbzx',10,11,9)
    emit('lwz',9,2,-0x7f3c)
    emit('lhz',0,9,0xac);emit('cmpwi',0,0);a.br('beq','normal')
    emit('lhz',0,12,0)
    for flag,lo,hi in [(0xb1,0x8340,0x8491),(0xae,0x8260,0x8279),
                       (0xb0,0x829f,0x82f1),(0xaf,0x8281,0x829a),
                       (0xb2,0x8140,0x825f)]:
        skip='skip%x'%flag
        emit('cmplwi',0,lo);a.br('blt',skip)
        emit('cmplwi',0,hi);a.br('bgt',skip)
        emit('lbz',0,9,flag);emit('cmpwi',0,0);a.br('bne','alternate')
        emit('lhz',0,12,0);a.label(skip)
    emit('addi',9,9,0x78);a.br('b','advance')
    a.label('alternate');emit('addi',9,9,0x88);a.br('b','advance')
    a.label('normal');emit('addi',9,9,0x54)
    a.label('advance')
    emit('cmpwi',10,32);a.br('beq','fullwidth')
    emit('std',10,1,0x78);emit('lfd',13,1,0x78)
    emit('fcfid',13,13);emit('frsp',13,13)
    emit('lfs',0,9,0);emit('fmuls',13,13,0)
    const(0,0x3d000000);emit('stw',0,1,0x78);emit('lfs',0,1,0x78)
    emit('fmuls',13,13,0);a.br('b','sum')
    a.label('fullwidth');emit('lfs',13,9,8)
    a.label('sum');emit('fadds',12,12,13)
    emit('addi',12,12,2);a.br('b','glyph')
    a.label('done')
    const(0,0x3f000000);emit('stw',0,1,0x78);emit('lfs',0,1,0x78)
    emit('fmuls',12,12,0);emit('fsubs',1,1,12)
    def restore():
        for f,off in [(0,0x60),(12,0x68),(13,0x70)]:emit('lfd',f,1,off)
        emit('ld',0,1,0x58);a.emit(0x7C0FF120)  # mtcrf 255,r0
        for r,off in [(0,0x30),(9,0x38),(10,0x40),(11,0x48),(12,0x50)]:
            emit('ld',r,1,off)
        emit('addi',1,1,0xa0)
    restore();tail(eboot.NAME_SITE)
    a.label('fallback');restore();a.emit(ORIGINAL);tail(SITE+4)
    code=a.code()
    assert CAVE+len(code)<=DATA
    return code


def regions(mapping,date_cards=False):
    import eboot
    data=b''.join(strings(mapping))+b''.join(jp.encode('cp932')+b'\0'
                                           for jp in centered_lines())+b'\0'
    data += bytes(bonus_table(mapping) - DATA - len(data))
    data += b''.join(struct.pack('>I', va) for va, _, _ in bonus_centering.rows()) + bytes(4)
    assert DATA+len(data)<=END
    return [(SITE,struct.pack('>I',eboot._ppc()['b'](CAVE-SITE))),
            (CAVE,stub(mapping,date_cards)),(DATA,data)]


def apply(elf,mapping):
    import eboot
    out=bytearray(elf);segs=eboot._segments(out)
    site=eboot._off(segs,SITE)
    assert struct.unpack_from('>I',out,site)[0]==ORIGINAL
    for va,raw in regions(mapping):
        p=eboot._off(segs,va)
        assert p is not None and eboot._off(segs,va+len(raw)-1)==p+len(raw)-1
        if va!=SITE:assert not any(out[p:p+len(raw)]),'President cave occupied'
        out[p:p+len(raw)]=raw
    check(out,mapping)
    return bytes(out)


def check(elf,mapping):
    import eboot
    segs=eboot._segments(elf)
    off=eboot._off(segs,CAVE)
    has_dates=elf[off:off+len(stub(mapping,True))]==stub(mapping,True)
    for va,raw in regions(mapping,has_dates):
        p=eboot._off(segs,va);assert elf[p:p+len(raw)]==raw,hex(va)
    # Measurement text must be precisely what the existing draw-time hook uses.
    entries={}
    p=eboot._off(segs,eboot.NAME_TBL)
    while True:
        jp,en=struct.unpack_from('>II',elf,p)
        if not jp:break
        key=bytes(eboot._cstr(elf,eboot._off(segs,jp)))
        if key in {s.encode('cp932') for s in centered_lines()} | {jp.encode('cp932') for _,jp,_ in bonus_centering.rows()}:
            assert not en&0xc0000000,'Reward centering requires an exact hook'
        entries[bytes(eboot._cstr(elf,eboot._off(segs,jp)))]=eboot._cstr(elf,eboot._off(segs,en&0x3fffffff))
        p+=8
    for (jp,en),raw in zip(battle_reports.HOOKS.items(),strings(mapping)):
        assert entries[jp.encode('cp932')]==raw[:-1],en
    for va,jp in zip(JP_VAS,battle_reports.HOOKS):
        assert eboot._cstr(elf,eboot._off(segs,va))==jp.encode('cp932')
    for jp in centered_lines():
        en=eboot.load_ui_hook()[jp]
        assert entries[jp.encode('cp932')]==eboot._encode_marked(en,mapping),jp
    for va,jp,en in bonus_centering.rows():
        assert eboot._cstr(elf,eboot._off(segs,va))==jp.encode('cp932')
        assert entries[jp.encode('cp932')]==eboot._encode_marked(en,mapping),jp
    print('PASS: President/reward/bonus centering wrapper and exact English hook agreement.')
