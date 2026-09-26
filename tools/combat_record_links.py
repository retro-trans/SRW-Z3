"""Combat Record navigation family: all three widget copies and count suffixes."""
import localization as _l10n
import struct
import aiddata,digraph as dg
from intermission_layout import text,ink

LINKS=(('『パイロットＴＯＰ５』へ',_l10n.literal('combat_record_links.LINKS/0')),
       ('『レクチャープレート』へ',_l10n.literal('combat_record_links.LINKS/1')),
       ('『トレードリスト』へ',_l10n.literal('combat_record_links.LINKS/2')),
       ('『Ｚクリスタル状況』へ',_l10n.literal('combat_record_links.LINKS/3')))
ROWS={base+32*i:pair for base in (0xa79b4,0xbdd54,0xbde94) for i,pair in enumerate(LINKS)}
SUFFIXES=(0xa7f34,0xa81d4)
ROWS.update({r:('人','') for r in SUFFIXES})
HELP={
 '『パイロットＴＯＰ５』へ移行します。':_l10n.literal('combat_record_links.HELP/4'),
 '『トレードリスト』へ移行します。':_l10n.literal('combat_record_links.HELP/5'),
 '『レクチャープレート』へ移行します。':_l10n.literal('combat_record_links.HELP/6'),
 '『Ｚクリスタル状況』へ移行します。':_l10n.literal('combat_record_links.HELP/7'),
}

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),hex(r)
        assert ink(en,mapping,widths,25)<270,(en,ink(en,mapping,widths,25))
    print('PASS: all 12 Combat Record navigation widgets and two Ace Pilot suffixes; numbers and selection metadata unchanged.')
