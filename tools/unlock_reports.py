"""Translate unlock notices without changing item names or unlock logic."""
import localization as _l10n
import struct
from pathlib import Path
import digraph as dg
from intermission_layout import ink

CONDITIONS={
 '『第４話をクリア』を達成':_l10n.literal('unlock_reports.CONDITIONS/0'),
 '『味方ユニットのＨＰが２０％以下に減少』を達成':_l10n.literal('unlock_reports.CONDITIONS/1'),
}
SOURCES={'第４話をクリア':0x70d710,'味方ユニットのＨＰが２０％以下に減少':0x70d7d0}
# Two verified TOC referents used by the report's concatenation path.
# Its middle field (the runtime item name) remains completely untouched.
PARTS=((0x7cb71c,0x71e530,'Ｄトレーダーにて「',_l10n.literal('unlock_reports.PARTS/2')),
       (0x7cb720,0x71e548,'」発売！','.'))

def encoded_part(jp,en,mapping):
    # Native std::string construction copies exactly 18 / 8 bytes, NOT a
    # NUL-terminated English string. Match both length and allocation budget.
    size=len(jp.encode('cp932'))
    raw=dg.encode_mixed(en,mapping)
    space=dg.encode_mixed(' ',mapping)
    assert len(raw)<=size and (size-len(raw))%len(space)==0, 'Unlock notice fixed-copy budget'
    return raw+space*((size-len(raw))//len(space))+b'\0'

def patch(elf,mapping,cursor):
    import eboot
    out=bytearray(elf);segs=eboot._segments(out);allowed=set();start=cursor
    for ptr,oldva,jp,en in PARTS:
        assert struct.unpack_from('>I',out,ptr)[0]==oldva
        pos=eboot._off(segs,oldva);rawjp=jp.encode('cp932')+b'\0'
        assert out[pos:pos+len(rawjp)]==rawjp
        raw=encoded_part(jp,en,mapping)
        busy=[i for i in range(cursor,min(cursor+len(raw),len(out))) if out[i]]
        assert cursor+len(raw)<=len(out) and not busy, (
            'unlock report text needs %d free bytes at file %#x (va %#x); occupied at %s: %r'
            % (len(raw),cursor,eboot._va(segs,cursor),[hex(i) for i in busy[:4]],
               bytes(out[cursor:cursor+len(raw)])))
        out[cursor:cursor+len(raw)]=raw
        struct.pack_into('>I',out,ptr,eboot._va(segs,cursor));allowed.update(range(ptr,ptr+4))
        cursor=(cursor+len(raw)+3)&~3
    allowed.update(range(start,cursor))
    assert len(elf)==len(out) and all(x==y or i in allowed for i,(x,y) in enumerate(zip(elf,out)))
    return bytes(out),cursor

def check(elf,hooks,mapping,widths):
    import eboot
    pristine=Path('work/EBOOT_dec.elf').read_bytes();segs=eboot._segments(elf)
    for jp,off in SOURCES.items():
        raw=jp.encode('cp932')+b'\0'
        assert pristine[off:off+len(raw)]==raw
        assert elf[off:off+len(raw)]==raw
        full='『'+jp+'』を達成'
        assert hooks[full]==CONDITIONS[full]
        assert ink(CONDITIONS[full],mapping,widths,28)<850
    for ptr,oldva,jp,en in PARTS:
        raw=encoded_part(jp,en,mapping)
        pos=eboot._off(segs,struct.unpack_from('>I',elf,ptr)[0])
        assert pos is not None and elf[pos:pos+len(raw)]==raw
        original=eboot._off(segs,oldva)
        assert elf[original:original+len(jp.encode('cp932'))+1]==jp.encode('cp932')+b'\0'
    for name in ('Worldbreaker Crest','Crest of Rebirth','Auto-Defenser'):
        line=PARTS[0][3]+name+'.'
        assert ink(line,mapping,widths,31)<850
    print('PASS: original two unlock conditions and fixed-byte D-Trader notice; runtime item names and requirements preserved.')
