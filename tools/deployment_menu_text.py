"""Map deployment help/counters; preserve numeric fields and menu behavior."""
import localization as _l10n
import struct
import aiddata,digraph as dg
from intermission_layout import text,ink

ROWS={
 0xaba94:('ＳＲポイント\n出撃チーム',_l10n.literal('deployment_menu_text.ROWS/0')),
 0xac014:('ＳＲポイント\n出撃チーム',_l10n.literal('deployment_menu_text.ROWS/1')),
 0xab9d4:('ＳＲポイント\nターン数',_l10n.literal('deployment_menu_text.ROWS/2')),
 0xabab4:('Ｚチップ\n資金',_l10n.literal('deployment_menu_text.ROWS/3')),
 0xac034:('Ｚチップ\n資金',_l10n.literal('deployment_menu_text.ROWS/4')),
 0xab9f4:('Ｚチップ\n資金',_l10n.literal('deployment_menu_text.ROWS/5')),
 0xabad4:('隊',''),0xac054:('隊',''),
 0xac894:('＜回収＞　味方のチームを選択します。',_l10n.literal('deployment_menu_text.ROWS/6')),
 0xac8b4:('＜修理＞　味方のチームを選択します。',_l10n.literal('deployment_menu_text.ROWS/7')),
 0xac8d4:('＜補給＞　味方のチームを選択します。',_l10n.literal('deployment_menu_text.ROWS/8')),
 0xac8f4:('＜出撃準備＞　出撃の準備を行います。',_l10n.literal('deployment_menu_text.ROWS/9')),
 0xacb74:('＜検索ＭＡＰ確認＞　所持ユニットを確認します。',_l10n.literal('deployment_menu_text.ROWS/10')),
 0xacb94:('＜検索ＭＡＰ確認＞　所持ユニットを確認します。',_l10n.literal('deployment_menu_text.ROWS/11')),
 0xacbf4:('＜回収＞　味方のチームを選択します。',_l10n.literal('deployment_menu_text.ROWS/12')),
}
COLONS={r:174. for r in (0xabaf4,0xabb14,0xabb34,0xabb54,0xac074,0xac094,0xac0b4,0xac0d4)}
COLONS.update({r:1166. for r in (0xaba14,0xaba34,0xaba54,0xaba74)})
# Currency values grow leftward as their digit count increases. A fixed
# separator is unsafe (119992 already intersects it). Omit punctuation in
# both currency rows across all three variants; retain live numeric layout.
CURRENCY_COLONS=(0xabb34,0xabb54,0xac0b4,0xac0d4,0xaba54,0xaba74)
for r in CURRENCY_COLONS:
    ROWS[r]=('：','')
HELP=tuple(r for r in ROWS if r>=0xac894)

def apply(blob,mapping,widths):
    from cpk import CPK
    k=CPK('work/orig/AIDDATAPACK.CPK');original=k.read(k.files[0])
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(original,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in HELP and original[r+23]&0x40:
            center=struct.unpack_from('>f',original,r+4)[0]
            struct.pack_into('>f',out,r+4,center-ink(en,mapping,widths,original[r+19])/1280.)
            out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.add(r+23)
    for r,x in COLONS.items():
        assert text(original,r)=='：'.encode('cp932')
        struct.pack_into('>f',out,r+4,(x-640)/640);allowed.update(range(r+4,r+8))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),hex(r)
        for line in en.split('\n'):assert ink(line,mapping,widths,blob[r+19])<(850 if r in HELP else 112)
        if r in HELP:
            assert not blob[r+23]&0x40
    for r,x in COLONS.items():assert abs(640+640*struct.unpack_from('>f',blob,r+4)[0]-x)<.001
    for r in CURRENCY_COLONS:assert text(blob,r)==b'',hex(r)
    print('PASS: 7 map-help widgets and deployment/map counters; all six currency separators omitted, live numbers unchanged.')
