"""Spirit target composites and record-screen captions, scoped to their widgets."""
import localization as _l10n
import struct
import aiddata,digraph as dg
from intermission_layout import text,ink

TARGETS={'自分単体':_l10n.literal('record_screen_labels.TARGETS/0'),'味方単体':_l10n.literal('record_screen_labels.TARGETS/1'),'敵単体':_l10n.literal('record_screen_labels.TARGETS/2'),
         '味方全体':_l10n.literal('record_screen_labels.TARGETS/3'),'敵全体':_l10n.literal('record_screen_labels.TARGETS/4'),
         '自分周囲':_l10n.literal('record_screen_labels.TARGETS/5'),'味方周囲':_l10n.literal('record_screen_labels.TARGETS/6'),'敵周囲':_l10n.literal('record_screen_labels.TARGETS/7'),
         '自分チーム':_l10n.literal('record_screen_labels.TARGETS/8'),'味方チーム':_l10n.literal('record_screen_labels.TARGETS/9'),'敵チーム':_l10n.literal('record_screen_labels.TARGETS/10')}
ROWS={0x9bed4:('：ランキング切換',_l10n.literal('record_screen_labels.ROWS/11')),
      0xaed14:('【エースパイロットＢＥＳＴ５】',_l10n.literal('record_screen_labels.ROWS/12'))}

# Live headings are separate FSSA fragments, NOT the similarly named UTF-8
# Key Help captions. Records are listed in visual order, not storage order.
# Replace the leftmost fragment, blank only its siblings, and centre the
# complete English caption inside the original group's advance bounds.
TITLE_GROUPS = (
    (_l10n.literal('record_screen_labels.TITLE_GROUPS/13'), ((0xa03f4,'～'), (0xa03d4,'パイ'),
       (0xa0374,'ロット'), (0xa0394,'ＴＯ'), (0xa03b4,'Ｐ５'), (0xa0414,'～'))),
    (_l10n.literal('record_screen_labels.TITLE_GROUPS/14'), ((0xa07f4,'エースパイ'), (0xa0814,'ロット'),
       (0xa0834,'ＢＥ'), (0xa0854,'ＳＴ５'))),
    (_l10n.literal('record_screen_labels.TITLE_GROUPS/15'), ((0xa0874,'エースパイ'), (0xa0894,'ロット'),
       (0xa08b4,'ＢＥ'), (0xa08d4,'ＳＴ５'))),
    (_l10n.literal('record_screen_labels.TITLE_GROUPS/16'), ((0xa25f4,'：ト'), (0xa2614,'レ'),
       (0xa2634,'ード'), (0xa2654,'リスト'))),
    (_l10n.literal('record_screen_labels.TITLE_GROUPS/17'), ((0xa2a54,'：ト'), (0xa2a74,'レ'),
       (0xa2a94,'ード'), (0xa2ab4,'リスト'))),
)

def title_bounds(original, group):
    first, last = group[0][0], group[-1][0]
    left = struct.unpack_from('>f',original,first+4)[0]*640
    right = (struct.unpack_from('>f',original,last+4)[0]*640
             + len(group[-1][1])*original[last+20])
    return left, right

def hooks():
    return dict(TARGETS)

def apply(blob,mapping,widths,original):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(original,r)==jp.encode('cp932')
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
        allowed.update(range(r,r+4))
    for en, group in TITLE_GROUPS:
        for n,(r,jp) in enumerate(group):
            assert text(original,r)==jp.encode('cp932'),hex(r)
            p=(len(out)+3)&~3
            out+=bytes(p-len(out))+dg.encode_mixed(en if n==0 else '',mapping)+b'\0'
            struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
            allowed.update(range(r,r+4))
        r=group[0][0]
        left,right=title_bounds(original,group)
        width=ink(en,mapping,widths,original[r+19])
        assert width+8 < right-left, (en,width,right-left)
        struct.pack_into('>f',out,r+4,(left+right-width)/1280.)
        allowed.update(range(r+4,r+8))
        # These are left-anchored italic fragments; retain all text modes,
        # baselines, font sizes, colours and animation records.
        assert not original[r+23]&0x40
    # Dynamic Spirit target values share this prototype; compact type avoids
    # touching the adjacent Duration widget or the selection/target logic.
    r=0x9e6f4
    assert text(original,r)=='自分単体'.encode('cp932')
    out[r+16:r+22]=bytes((26,26,24,26,26,26))
    allowed.update(range(r+16,r+22))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths,original)
    return bytes(out)

def check(blob,mapping,widths,original=None):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping)
        assert ink(en,mapping,widths,blob[r+19])<350
    for en,group in TITLE_GROUPS:
        for n,(r,_) in enumerate(group):
            assert text(blob,r)==dg.encode_mixed(en if n==0 else '',mapping),hex(r)
            if original is not None:
                assert blob[r+8:r+32]==original[r+8:r+32],hex(r)
        if original is not None:
            r=group[0][0]
            left,right=title_bounds(original,group)
            width=ink(en,mapping,widths,blob[r+19])
            x=struct.unpack_from('>f',blob,r+4)[0]*640
            assert abs(x+width/2-(left+right)/2)<0.001,hex(r)
            assert left+4<x and x+width<right-4,en
    assert blob[0x9e6f4+16:0x9e6f4+22]==bytes((26,26,24,26,26,26))
    assert all(ink(en,mapping,widths,26)<165 for en in TARGETS.values())
    print('PASS: Spirit targets, ranking controls and all five split record-title groups translated.')
