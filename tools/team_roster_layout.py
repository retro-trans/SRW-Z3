"""Team-roster heading translations and narrow title/footer clearances."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink

BONUS = {0xb0474:'チームボーナス',0xb0494:'チームボーナス',
         0xb0554:'タッグボーナス',0xb3fb4:'タッグボーナス',0xb4fb4:'タッグボーナス'}
MAXIMUM=(0xb0194,0xb04b4,0xb3e54)
SUPPORT={0xb01f4:'援攻',0xb0214:'援防',0xb0574:'援攻',0xb0594:'援防',
         0xb3fd4:'援攻',0xb3ff4:'援防',0xb4f74:'援攻',0xb4f94:'援防'}
MOVE=(0xaf614,0xb3374)
ROWS={r:(jp,_l10n.literal('team_roster_layout.ROWS/0')) for r,jp in BONUS.items()}
ROWS.update({r:('＜マキシマムブレイク＞','＜Max Break＞') for r in MAXIMUM})
ROWS.update({r:(jp,'S. Atk' if jp=='援攻' else 'S. Def') for r,jp in SUPPORT.items()})
ROWS.update({r:('移動','Move') for r in MOVE})
# Shift only the suffix/colon pieces: the existing faction-colored heading
# and its closing bracket stay untouched. Includes Team and Unit views.
TITLE_PARTS={0xaf054:'ユニット',0xaf074:'：',0xaf0b4:'ユニット',0xaf0d4:'：',
             0xaf1f4:'チーム',0xaf214:'：',0xaf254:'チーム',0xaf274:'：',
             0xb2d34:'ユニット',0xb2d54:'：',0xb2df4:'タッグ',0xb2dd4:'：'}
FOOTER={0xb3394:'【】',0xb33b4:'空陸－地',0xb33d4:'９９／'}

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r not in MOVE:
            size=21 if r in SUPPORT else 22 if r in BONUS else 28
            old_width=len(jp)*(28 if r in SUPPORT or r in MAXIMUM else blob[r+20])
            x=struct.unpack_from('>f',blob,r+4)[0]
            struct.pack_into('>f',out,r+4,x+(old_width-ink(en,mapping,widths,size))/1280.)
            out[r+16:r+22]=bytes((size,size,size-2,size,size,size))
            out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22));allowed.add(r+23)
    for records,delta in ((TITLE_PARTS,28),(FOOTER,32)):
        for r,jp in records.items():
            assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
            x=struct.unpack_from('>f',blob,r+4)[0]
            struct.pack_into('>f',out,r+4,x+delta/640.)
            allowed.update(range(r+4,r+8))
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),(hex(r),en)
        if r in SUPPORT:assert ink(en,mapping,widths,21)<=63
        if r in BONUS:assert ink(en,mapping,widths,22)<140
        if r in MAXIMUM:assert ink(en,mapping,widths,28)<240
    # Move has 41px before the original value block, now extended by 32px.
    label_x=struct.unpack_from('>f',blob,0xb3374+4)[0]*640
    bracket_x=struct.unpack_from('>f',blob,0xb3394+4)[0]*640
    assert bracket_x-label_x-ink('Move',mapping,widths,24)>=9.9
    # The bracket uses a 176px internal span and a 24px closing glyph.
    assert bracket_x+640+176+24<640
    colon_x=struct.unpack_from('>f',blob,0xaf274+4)[0]*640+640
    assert abs(colon_x-(217.5+28))<1e-4
    assert colon_x-(6.5+ink('【　Enemy List',mapping,widths,31))>=10
    suffix_x=struct.unpack_from('>f',blob,0xaf254+4)[0]*640+640
    assert suffix_x+ink('Team',mapping,widths,28)<380
    print('PASS: team bonus/Max Break/support columns; faction-title suffix gaps; Move footer clears its value block.')
