"""Scoped Change Pilots placement in the intermission button grid."""
import struct
from intermission_layout import text

# Original normal/highlighted records; the separate team-editor caption at
# 0xb22d4 is a different layout and must not inherit this correction.
ROWS={0xa3314:(28,-0.0023437500931322575),
      0xa3334:(31,-0.0054687499068677425)}
# User's 2560x1440 capture: normal green ink x=1032..1405, button
# x=876..1395. Native 1280x720 center correction = (2271-2437)/4.
# Highlighted variant scales with its original 31px vs 28px font.
NORMAL_SHIFT=-41.5

def shift(size):
    return NORMAL_SHIFT*size/28.

def apply(blob):
    out=bytearray(blob)
    for r,(size,x) in ROWS.items():
        assert text(blob,r)=='のせかえ'.encode('cp932'),hex(r)
        assert blob[r+19]==size,hex(r)
        assert abs(struct.unpack_from('>f',blob,r+4)[0]-x)<1e-7,hex(r)
        struct.pack_into('>f',out,r+4,x+shift(size)/640.)
    allowed={i for r in ROWS for i in range(r+4,r+8)}
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out)
    return bytes(out)

def check(blob):
    for r,(size,x) in ROWS.items():
        assert text(blob,r)=='のせかえ'.encode('cp932'),hex(r)
        assert blob[r+19]==size,hex(r)
        assert abs(struct.unpack_from('>f',blob,r+4)[0]-(x+shift(size)/640.))<1e-7,hex(r)
    print('PASS: normal/highlighted Change Pilots button X alignment; original font and text hooks retained.')
