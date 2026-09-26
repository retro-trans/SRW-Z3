"""Deployment reverse-order hint and both split teams-aboard captions."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text, ink

CAPTIONS=(0x99934,0x99d54)
ROWS={0x9bc74:('：全機逆順配置',_l10n.literal('aboard_order_labels.ROWS/0'))}
for r in CAPTIONS:
    ROWS[r]=('搭載中',_l10n.literal('aboard_order_labels.ROWS/1'))
    ROWS[r+32]=('チ　ム：','')
    ROWS[r+64]=('ー','')


def apply(blob,mapping,widths,original):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(original,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
        allowed.update(range(r,r+4))
        if r in CAPTIONS:
            # Start 16 native pixels earlier, inside the existing banner;
            # the count stays where the game draws it. No colon to collide.
            x=struct.unpack_from('>f',original,r+4)[0]-16/640.
            struct.pack_into('>f',out,r+4,x)
            out[r+16:r+22]=bytes((20,20,19,20,20,22))
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)


def check(blob,mapping,widths):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),hex(r)
        assert ink(en,mapping,widths,blob[r+19])<(144 if r in CAPTIONS else 190)
    for r in CAPTIONS:
        assert blob[r+16:r+22]==bytes((20,20,19,20,20,22))
        assert abs(struct.unpack_from('>f',blob,r+4)[0]-(.10078124701976776-16/640.))<1e-6
    print('PASS: Reverse Order hint and both Teams Aboard split captions; count fields untouched.')
