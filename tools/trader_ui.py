"""Scoped D-Trader/result widgets. Preserve offsets and runtime values."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import ink

# Only Trade List's two narrow category columns, not the wider Buy screen.
CATEGORY_ROWS = (0xa2674,0xa2694,0xa2ad4,0xa2af4)

STATS = '移動　　　　　\nタイプ\nＨＰ\nＥＮ\n装甲値\n運動性\n照準値\n武器射程\n地形適応\n所持数'
ROWS = {
    0xa2d94: ('第話', _l10n.literal('trader_ui.ROWS/0')),
    0xa2f54: ('第話', _l10n.literal('trader_ui.ROWS/1')),
    0xa2d74: ('　クリア', _l10n.literal('trader_ui.ROWS/2')),
    0xa2f74: ('　クリア', _l10n.literal('trader_ui.ROWS/3')),
    0xa8ff4: ('購入', _l10n.literal('trader_ui.ROWS/4')),
    0xa9014: ('売却', _l10n.literal('trader_ui.ROWS/5')),
    0xa26b4: ('【Ｄトレーダー：購入】', _l10n.literal('trader_ui.ROWS/6')),
    0xa2834: ('【Ｄトレーダー：売却】', _l10n.literal('trader_ui.ROWS/7')),
    0xa2694: ('強化システム', _l10n.literal('trader_ui.ROWS/8')),
    0xa26f4: ('強化システム', _l10n.literal('trader_ui.ROWS/9')),
    0xa2af4: ('強化システム', _l10n.literal('trader_ui.ROWS/10')),
    0xa2714: ('エクストラ', _l10n.literal('trader_ui.ROWS/11')),
    0xa2734: ('購入価格', _l10n.literal('trader_ui.ROWS/12')),
    0xa2754: ('購入価格', _l10n.literal('trader_ui.ROWS/13')),
    0xa2774: ('購入価格', _l10n.literal('trader_ui.ROWS/14')),
    0xa2794: (STATS, _l10n.literal('trader_ui.ROWS/15')),
    0xa2b14: (STATS, _l10n.literal('trader_ui.ROWS/16')),
    0xa27d4: ('個', ''),
    0xa2b54: ('個', ''),
    0xa2894: ('売却価格', _l10n.literal('trader_ui.ROWS/17')),
    0xa28b4: ('売却額．', _l10n.literal('trader_ui.ROWS/18')),
    0xa28d4: ('未装備数', _l10n.literal('trader_ui.ROWS/19')),
    0xa28f4: ('所持数', _l10n.literal('trader_ui.ROWS/20')),
    0xa2914: ('売却数', _l10n.literal('trader_ui.ROWS/21')),
    0xaa774: ('＜獲得ボーナス＞', _l10n.literal('trader_ui.ROWS/22')),
    0xaa874: ('＜獲得ボーナス＞', _l10n.literal('trader_ui.ROWS/23')),
    0x988b4: ('攻', _l10n.literal('trader_ui.ROWS/24')),
}


def apply(blob, mapping, widths):
    result = bytearray(blob)
    for record,(jp,en) in ROWS.items():
        ref = struct.unpack_from('>I',blob,record)[0]+aiddata.STR_BASE
        assert blob[ref:ref+len(jp.encode('cp932'))+1] == jp.encode('cp932')+b'\0', (hex(record),jp)
        raw = dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        pos = (len(result)+3)&~3
        result += bytes(pos-len(result))+raw
        struct.pack_into('>I',result,record,pos-aiddata.STR_BASE)
        if record in (0xa8ff4,0xa9014):
            # Fixed 28px widget: use the actual ink edge, not ASCII count.
            center = struct.unpack_from('>f',blob,record+4)[0]
            ink = sum(widths[dg.cell_index(mapping[c])] for c in en)*28/32.
            struct.pack_into('>f',result,record+4,center-ink/(2*640))
            result[record+23] &= ~0x40
        if record == 0x988b4:
            # Two Latin letters within the former single-kanji badge.
            result[record+16:record+22] = bytes.fromhex('111115171117')
        if record in (0xa2d94,0xa2f54,0xa2d74,0xa2f74):
            # Keep a gap before the separately drawn episode number; retain
            # Clear's original visible start after the fullwidth blank.
            x = struct.unpack_from('>f',blob,record+4)[0]
            delta = -8 if record in (0xa2d94,0xa2f54) else 28
            struct.pack_into('>f',result,record+4,x+delta/640.)
    for r in CATEGORY_ROWS:
        # The supplied Trade List has ~150 native pixels before the first
        # item icon. 23px Power Parts uses 136px, leaving visible separation.
        # Systems keeps the category readable without squeezing its lettering.
        result[r+16:r+22]=bytes((23,23,21,23,23,23))
    # The generic Confirm translation overlaps the next controller icon here.
    record=0xa2534
    ref=struct.unpack_from('>I',blob,record)[0]+aiddata.STR_BASE
    assert blob[ref:ref+7]=='：決定'.encode('cp932')+b'\0'
    raw=dg.encode_mixed(': OK',mapping)+b'\0'
    pos=(len(result)+3)&~3;result+=bytes(pos-len(result))+raw
    struct.pack_into('>I',result,record,pos-aiddata.STR_BASE)
    return bytes(result)


def verify(before, after, mapping, widths):
    assert after == apply(before,mapping,widths)
    allowed=set()
    for r in tuple(ROWS)+(0xa2534,):allowed.update(range(r,r+4))
    for r in (0xa8ff4,0xa9014):allowed.update(range(r+4,r+8));allowed.add(r+23)
    for r in (0xa2d94,0xa2f54,0xa2d74,0xa2f74):allowed.update(range(r+4,r+8))
    allowed.update(range(0x988b4+16,0x988b4+22))
    for r in CATEGORY_ROWS:allowed.update(range(r+16,r+22))
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(before,after)))
    for r,(jp,en) in ROWS.items():
        p=struct.unpack_from('>I',after,r)[0]+aiddata.STR_BASE
        raw = dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        assert after[p:p+len(raw)] == raw
        assert raw.count(b'\n') == jp.count('\n')
    for line in ROWS[0xa2794][1].splitlines():
        assert sum(widths[dg.cell_index(mapping[c])] for c in line)*28/32 < 120
    check_categories(after,mapping,widths)


def check_categories(blob,mapping,widths):
    for r in CATEGORY_ROWS:
        assert blob[r+16:r+22]==bytes((23,23,21,23,23,23)),hex(r)
    assert ink('Power Parts',mapping,widths,23)+12 < 150
    assert ink('Systems',mapping,widths,23)+12 < 150
