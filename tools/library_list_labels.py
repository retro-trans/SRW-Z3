"""Library list headers and the shared Japanese-order/series-order controls."""
import localization as _l10n
import struct
import aiddata, digraph as dg
from intermission_layout import text, ink

ROWS={
 0xa4fd4:('：＜５０音順へ＞',_l10n.literal('library_list_labels.ROWS/0')),
 0xa4ff4:('：＜作品順へ＞',_l10n.literal('library_list_labels.ROWS/1')),
 0xa54f4:('キャラクター事典',_l10n.literal('library_list_labels.ROWS/2')),
 0xa5514:('キャラクター名',_l10n.literal('library_list_labels.ROWS/3')),
 0xa5554:('ロボット大図鑑',_l10n.literal('library_list_labels.ROWS/4')),
 0xa5574:('ロボット名',_l10n.literal('library_list_labels.ROWS/5')),
 0xa55b4:('用語事典',_l10n.literal('library_list_labels.ROWS/6')),
 0xa55d4:('用語名',_l10n.literal('library_list_labels.ROWS/7')),
 0xbcc74:('用語事典',_l10n.literal('library_list_labels.ROWS/8')),
 0xbcc94:('用語名',_l10n.literal('library_list_labels.ROWS/9')),
 0xbd354:('用語事典',_l10n.literal('library_list_labels.ROWS/10')),
 0xbd374:('用語名',_l10n.literal('library_list_labels.ROWS/11')),
}
TITLES=(0xa54f4,0xa5554,0xa55b4,0xbcc74,0xbd354)

def apply(blob,mapping,widths,original):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(original,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in TITLES:
            center=struct.unpack_from('>f',original,r+4)[0]
            struct.pack_into('>f',out,r+4,center-ink(en,mapping,widths,24)/1280.)
            out[r+16:r+22]=bytes((24,24,22,24,24,24));out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22));allowed.add(r+23)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),hex(r)
        assert ink(en,mapping,widths,blob[r+19])<(310 if r in TITLES else 360)
        if r in TITLES:assert not blob[r+23]&0x40
    print('PASS: all three Library list titles/name headers and both sort-mode hints. Sorting behavior unchanged.')
