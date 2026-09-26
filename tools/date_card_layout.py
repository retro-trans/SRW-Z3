"""PS3: opt the full-screen date drawer into existing VWF-aware centering.

Only its LR-identified call at 0x14c588 opts in. Native center 640, vertical
position 340, size 40, mode/style, calendar and translation data are unchanged.
"""
import struct
import eboot
import president_report_layout as P
from localization import Catalog

CALL=0x14c588


def verify_sources(b,mapping):
    segs=eboot._segments(b)
    def word(va):return struct.unpack_from('>I',b,eboot._off(segs,va))[0]
    assert word(CALL)==0x48000001|((P.SITE-CALL)&0x3fffffc)
    for va,w in ((0x14c560,0x38600028),(0x14c578,0x38e00001),
                 (0x14c57c,0xc022a8ec),(0x14c584,0xc042a8f0)):
        assert word(va)==w,hex(va)
    assert word(P.SITE)==0x48000000|((P.CAVE-P.SITE)&0x3fffffc)
    rows={};at=eboot._off(segs,eboot.NAME_TBL)
    while True:
        jp,en=struct.unpack_from('>II',b,at)
        if not jp:break
        if not en&0xc0000000:
            rows[bytes(eboot._cstr(b,eboot._off(segs,jp)))]=bytes(eboot._cstr(b,eboot._off(segs,en)))
        at+=8
    cat=Catalog();definitions=cat.document('localization/messages/date_cards.json')['messages']
    assert len(definitions)==77
    for mid,row in definitions.items():
        en=cat.text(mid)
        assert '\n' not in en and all(32<=ord(c)<127 for c in en)
        assert rows[row['source'].encode('cp932')]==eboot._encode_marked(en,mapping),mid
    return segs


def apply(b,mapping):
    segs=verify_sources(b,mapping)
    old,new=P.stub(mapping),P.stub(mapping,True)
    off=eboot._off(segs,P.CAVE)
    assert b[off:off+len(new)]==old+bytes(len(new)-len(old)), 'Expected original centering wrapper'
    out=bytearray(b);out[off:off+len(new)]=new
    check(out,mapping)
    return bytes(out),[(off,off+len(new))]


def check(b,mapping):
    segs=verify_sources(b,mapping);raw=P.stub(mapping,True)
    off=eboot._off(segs,P.CAVE)
    assert b[off:off+len(raw)]==raw
