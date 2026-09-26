"""September screenshot follow-up: scope footer/header edits to their widgets."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink

ROWS={0xaeb74:(_l10n.literal('ui_followup_layout.ROWS/0'),'【機体・武器改造】'),
      0xb2bb4:(_l10n.literal('ui_followup_layout.ROWS/1'),'【機体・武器改造】'),
      0xa7ed4:(_l10n.literal('ui_followup_layout.ROWS/2'),'＜レコードライブラリ―＞'),
      0xa8174:(_l10n.literal('ui_followup_layout.ROWS/3'),'＜レコードライブラリ―＞')}
MOVES=(0xb2114,0xb2194,0xb21d4,0xb2214)
EPISODES=(0xa2d94,0xa2f54,0xa3194,0xa3a54,0xa3df4,0xa3ff4,0xa41f4,0xa43f4,0xa45f4)
CLEARS=(0xa2d74,0xa2f74,0xa3a74,0xa3e14,0xa4014,0xa4214,0xa4414,0xa4614)
TURNS=(0xa2cf4,0xa2ed4,0xa30b4,0xa39d4,0xa3d74,0xa3f74,0xa4174,0xa4374,0xa4574)
for r in MOVES:ROWS[r]=(_l10n.literal('ui_followup_layout.ROWS/4'),'移動')
for r in EPISODES:ROWS[r]=(_l10n.literal('ui_followup_layout.ROWS/5'),'第話')
for r in CLEARS:ROWS[r]=(_l10n.literal('ui_followup_layout.ROWS/6'),'　クリア')
for r in TURNS:ROWS[r]=(_l10n.literal('ui_followup_layout.ROWS/7'),'＜　　ターン＞')
ROWS[0xa2bb4]=(_l10n.literal('ui_followup_layout.ROWS/8'),'クリア')
ROWS[0xa2b94]=(_l10n.literal('ui_followup_layout.ROWS/9'),'最終話')

def apply(blob,mapping,widths,pristine=None):
    # Source validation is against the untouched records, since the generic
    # UI pass may already have translated the embedded word "turns".
    if pristine is None:
        from cpk import CPK
        k=CPK('work/orig/AIDDATAPACK.CPK');pristine=k.read(k.files[0])
    out=bytearray(blob);allowed=set()
    for r,(en,jp) in ROWS.items():
        assert text(pristine,r)==jp.encode('cp932'),(hex(r),jp)
        raw=dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in EPISODES+CLEARS:
            # Normalize the two older D-Trader-adjusted variants too, so the
            # leading space is not applied on top of its earlier +28px move.
            out[r+4:r+8]=pristine[r+4:r+8];allowed.update(range(r+4,r+8))
        if r in MOVES:
            out[r+16:r+21]=bytes((22,22,20,22,22));allowed.update(range(r+16,r+21))
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(en,jp) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),(hex(r),en)
    for en,size,budget in [('MV',22,36),('Ep',28,42),(' Clear',28,96),('[Upgrades]',31,250),('＜Record Library＞',31,300)]:
        assert ink(en,mapping,widths,size)<budget,(en,ink(en,mapping,widths,size))
    # Two full-width spaces retain the turn-count slot; the added ASCII space
    # separates the dynamically rendered number from "turns".
    for r in TURNS:assert text(blob,r)==dg.encode_mixed('＜\u3000\u3000 turns＞',mapping)
    print('PASS: upgrade and Record Library headings, four MV labels, nine stage/turn footer variants; dynamic values untouched.')
