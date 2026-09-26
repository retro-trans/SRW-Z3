"""Training tabs and Data/Key Help UI records reported September 13."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink
from key_help_labels import SLOT_HELP_JP,SLOT_HELP_EN

ROWS={0x99334:('右スティック',_l10n.literal('training_help_layout.ROWS/0')),
      0xbe094:(SLOT_HELP_JP,SLOT_HELP_EN)}
ROWS.update({r:('：キーヘルプへ',': Key Help') for r in (0xa48d4,0xa48f4,0xa4c94,0xa4cb4)})
ROWS.update({r:('：スロット決定',': Select Slot') for r in (0xae074,0xb68d4)})
# Three state copies of the split tab, plus its standalone caption.
LEARN={0xb5c34:'スキル',0xb5c54:'修得',0xb5cb4:'スキル',
       0xb5cd4:'修得',0xb5f14:'スキル',0xb5f34:'修得',0xb5eb4:'スキル修得'}
# The captured ink centres differ by ~594.5 screen pixels whereas their
# tab centres differ by ~533.75. At 2434/1280 scale, -32 native pixels
# matches the Raise Stats tab's inset. Baselines, sizes and hooks stay intact.
LEARN_SHIFT=-32.


def apply(blob,mapping,widths,pristine):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(pristine,r)==jp.encode('cp932'),hex(r)
        raw=dg.encode_mixed(en,mapping)+b'\0'
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
        allowed.update(range(r,r+4))
    for r,jp in LEARN.items():
        assert text(blob,r)==jp.encode('cp932'),hex(r)
        assert blob[r+4:r+8]==pristine[r+4:r+8]
        x=struct.unpack_from('>f',pristine,r+4)[0]
        struct.pack_into('>f',out,r+4,x+LEARN_SHIFT/640.)
        allowed.update(range(r+4,r+8))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths,pristine)
    return bytes(out)


def check(blob,mapping,widths,pristine=None):
    if pristine is None:
        from cpk import CPK
        c=CPK('work/orig/AIDDATAPACK.CPK');pristine=c.read(c.files[0])
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),(hex(r),en)
        assert blob[r+4:r+32]==pristine[r+4:r+32],hex(r)
        size=blob[r+20]
        budget=1050 if r==0xbe094 else 190
        assert ink(en,mapping,widths,size)<budget,(en,budget)
    for r,jp in LEARN.items():
        assert text(blob,r)==jp.encode('cp932')
        assert blob[r+8:r+32]==pristine[r+8:r+32]
        delta=(struct.unpack_from('>f',blob,r+4)[0]-struct.unpack_from('>f',pristine,r+4)[0])*640
        assert abs(delta-LEARN_SHIFT)<0.0001
    print('PASS: Learn Skills tab states; four Key Help hints, two Select Slot hints, Right Stick and parts-slot help.')
