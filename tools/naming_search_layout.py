"""Naming choices and search setup: scoped text widgets, not naming logic."""
import localization as _l10n
import struct
from pathlib import Path
import digraph as dg
from intermission_layout import text,ink
import aiddata

REPORTS = {
    '自動更新の設定を「パイロット」に設定しました。': _l10n.literal('naming_search_layout.REPORTS/0'),
    '自動更新の設定を「機体」に設定しました。': _l10n.literal('naming_search_layout.REPORTS/1'),
    '自動更新の設定を解除しました。': _l10n.literal('naming_search_layout.REPORTS/2'),
}
ROWS = {
    0xb2534: ('メインユニットのパイロット名から設定します。', _l10n.literal('naming_search_layout.ROWS/3')),
    0xb2554: ('パイロット', _l10n.literal('naming_search_layout.ROWS/4')),
    0xb2574: ('メインユニットの機体名から設定します。', _l10n.literal('naming_search_layout.ROWS/5')),
    0xb2594: ('機体', _l10n.literal('naming_search_layout.ROWS/6')),
    0xb25b4: ('チーム内から連想されるキーワードで設定します。', _l10n.literal('naming_search_layout.ROWS/7')),
    0xb25d4: ('キーワード', _l10n.literal('naming_search_layout.ROWS/8')),
    0xb25f4: ('各チームごとに上記の中から選択し、設定します。', _l10n.literal('naming_search_layout.ROWS/9')),
    0xb2614: ('ランダム', _l10n.literal('naming_search_layout.ROWS/10')),
    0xb2634: ('メインユニットのパイロット名から自動更新します。', _l10n.literal('naming_search_layout.ROWS/11')),
    0xb2654: ('＜パイロット＞', _l10n.literal('naming_search_layout.ROWS/12')),
    0xb2674: ('メインユニットの機体名から自動更新します。', _l10n.literal('naming_search_layout.ROWS/13')),
    0xb2694: ('＜機体＞', _l10n.literal('naming_search_layout.ROWS/14')),
    0xb26b4: ('自動更新をしません。（任意の名称設定が可能）', _l10n.literal('naming_search_layout.ROWS/15')),
    0xb26d4: ('＜設定なし＞', _l10n.literal('naming_search_layout.ROWS/16')),
    0xa9234: ('＜検索設定＞', _l10n.literal('naming_search_layout.ROWS/17')),
}
HEADINGS = tuple(range(0xb2554,0xb26f4,64))+(0xa9234,)
EMPTY_FILTERS=(0xa8674,0xa86f4,0xa8774)
for r in EMPTY_FILTERS:ROWS[r]=('：検索なし',_l10n.literal('naming_search_layout.ROWS/18'))
for r in (0x9b974,0x9b9b4,0xb2474,0xb26f4):
    ROWS[r]=('：設定の切換\n：設定終了',_l10n.literal('naming_search_layout.ROWS/19'))
for r in (0x9b9d4,0xb2494,0xb2714):
    ROWS[r]=('：設定クリア\n：検索項目の設定',_l10n.literal('naming_search_layout.ROWS/20'))
ROWS[0x9b994]=('：検索項目の設定\n：設定クリア',_l10n.literal('naming_search_layout.ROWS/21'))

def raw(r,en,mapping):
    import command_layout
    prefix=struct.pack('>H',command_layout.CODES[command_layout.EMPTY_FILTER_INDEX]) if r in EMPTY_FILTERS else b''
    return prefix+dg.encode_mixed(en,mapping,newline=b'\n')

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw(r,en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in HEADINGS:
            size=25 if r==0xa9234 else 32
            center=struct.unpack_from('>f',blob,r+4)[0]
            struct.pack_into('>f',out,r+4,center-ink(en,mapping,widths,size)/1280.)
            out[r+16:r+22]=bytes((size,size,size-2,size,size,size))
            out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22));allowed.add(r+23)
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==raw(r,en,mapping),(hex(r),en)
        assert en.count('\n')==jp.count('\n')
        if r in HEADINGS:assert ink(en,mapping,widths,25 if r==0xa9234 else 32)<260,en
        elif r in EMPTY_FILTERS:
            assert blob[r+23]&0x40
            assert ink(en,mapping,widths,25)<95
        elif '\n' in en:
            assert max(ink(s,mapping,widths,28) for s in en.split('\n'))<190
        else:assert ink(en,mapping,widths,25)<565,(en,ink(en,mapping,widths,25))
    print('PASS: naming descriptions/options, three search-filter templates and all eight controller-hint copies fit.')

def check_reports(hooks,mapping,widths):
    import command_layout
    pristine=Path('work/EBOOT_dec.elf').read_bytes()
    for jp,en in REPORTS.items():
        assert jp.encode('cp932')+b'\0' in pristine
        assert hooks[jp]==en
        assert command_layout.count_coefficient(command_layout.dialog_index(jp))==len(jp)/2.
        assert ink(en,mapping,widths,32)<800
    print('PASS: all three naming-update reports translated and live-centered.')
