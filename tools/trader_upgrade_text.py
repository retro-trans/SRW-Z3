"""Complete four-record upgrade-system family and 21 unlock-report conditions.

Native 0x380-byte records keep IDs, prices and names intact. Text-only lore
and effect fields are encoded within their original padded capacities.
Names and completed reports use exact draw hooks; composed system notices
need mixed VWF/Japanese keys because names are inserted after translation.
"""
from pathlib import Path
import re
import struct
import digraph as dg
import localization
import trdata
from intermission_layout import ink

GROUP='trader_upgrade_text'


def rows():
    cat=localization.english()
    for mid,d in cat.document('localization/messages/'+GROUP+'.json')['messages'].items():
        yield mid,d,trdata._ex(cat.text(mid),mid)


def hooks():
    return {d['source']:en for _,d,en in rows() if d['context']['role'] in ('name','completed')}


def mixed_hooks():
    import unlock_reports as U
    # This is the actual fixed-length native concatenation, including padding.
    prefix=U.PARTS[0][3].ljust(9)
    suffix=U.PARTS[1][3].ljust(4)
    return {prefix+d['source']+suffix:prefix+en+U.PARTS[1][3]
            for _,d,en in rows() if d['context']['role']=='name'}


def check_source(blob):
    import unlock_reports as U
    conditions=set(U.SOURCES.values())
    fields=set()
    for mid,d,_ in rows():
        c=d['context']
        if c['role']=='completed':
            off=int(c['condition_offset'],16);conditions.add(off)
            jp=d['source'][1:-4]  # remove native 『 / 』を達成 wrapper
        else:
            off=int(c['eboot_offset'],16);fields.add(off);jp=d['source']
        raw=jp.encode('cp932')+b'\0'
        assert blob[off:off+len(raw)]==raw,(mid,hex(off))
    inventory={0x70d6f0+m.start() for m in re.finditer(rb'[^\0]+',blob[0x70d6f0:0x70d970])}
    inventory.update(0x6b0828+i*0x380 for i in range(4))
    assert conditions==inventory and len(conditions)==21
    assert fields=={0x6b0538+i*0x380+delta for i in range(4) for delta in (0,16,256)}
    # Type/category and system index at each 16-byte record header.
    source=Path('work/EBOOT_dec.elf').read_bytes()
    for i in range(4):
        off=0x6b0528+i*0x380
        assert blob[off:off+16]==source[off:off+16],hex(off)


def patch(blob,mapping):
    check_source(blob)
    out=bytearray(blob)
    for mid,d,en in rows():
        c=d['context']
        if c['role'] not in ('lore','effect'):
            continue
        off=int(c['eboot_offset'],16);cap=c['capacity']
        raw=dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        assert len(raw)<=cap,(mid,len(raw),cap)
        out[off:off+cap]=raw+bytes(cap-len(raw))
    return bytes(out)


def check(blob,mapping,widths):
    import eboot
    source=Path('work/EBOOT_dec.elf').read_bytes()
    check_source(source)
    allowed=set()
    for mid,d,en in rows():
        c=d['context']
        for line in en.split('\n'):
            assert ink(line,mapping,widths,31 if c['role']=='completed' else 28)<=c['width_limit'],mid
        if c['role'] in ('lore','effect'):
            assert len(en.splitlines())<=3,mid
            off=int(c['eboot_offset'],16);cap=c['capacity']
            raw=dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
            assert len(raw)<=cap and blob[off:off+cap]==raw+bytes(cap-len(raw)),mid
            allowed.update(range(off,off+cap))
    start,end=0x6b0528,0x6b1328
    assert all(blob[p]==source[p] or p in allowed for p in range(start,end)), 'System record metadata/name/condition changed'
    segs=eboot._segments(blob);p=eboot._off(segs,eboot.NAME_TBL);entries={}
    while True:
        key,value=struct.unpack_from('>II',blob,p)
        if not key:break
        entries[eboot._cstr(blob,eboot._off(segs,key))]=(value & 0xc0000000,
            eboot._cstr(blob,eboot._off(segs,value & 0x3fffffff)))
        p+=8
    import unlock_reports as U
    for jp,en in {**U.CONDITIONS,**hooks()}.items():
        assert entries[jp.encode('cp932')]==(0,eboot._encode_marked(en,mapping)),jp
    for key,en in mixed_hooks().items():
        assert entries[eboot._encode_marked(key,mapping)]==(0,eboot._encode_marked(en,mapping)),key
    print('PASS: all four upgrade systems and all 21 report conditions inventoried; names/effects/lore and mixed notices covered.')
