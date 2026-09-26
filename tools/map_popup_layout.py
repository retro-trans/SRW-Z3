"""Compact labels in the narrow map-hover popup; never move hidden values."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink

ROWS={
    0xac714: ('移動',_l10n.literal('map_popup_layout.ROWS/0')),
    0xb9b94: ('援攻．\n援防．',_l10n.literal('map_popup_layout.ROWS/1')),
    0xbb254: ('援攻．',_l10n.literal('map_popup_layout.ROWS/2')), 0xbb274: ('援攻．',_l10n.literal('map_popup_layout.ROWS/3')),
    0xbb2b4: ('援防．',_l10n.literal('map_popup_layout.ROWS/4')), 0xbb2d4: ('援防．',_l10n.literal('map_popup_layout.ROWS/5')),
    0xab9b4: ('回復：\n回復：',_l10n.literal('map_popup_layout.ROWS/6')),
    0xac194: ('回復：\n回復：',_l10n.literal('map_popup_layout.ROWS/7')),
}
SUPPORT=(0xb9b94,0xbb254,0xbb274,0xbb2b4,0xbb2d4)
REGEN=(0xab9b4,0xac194)

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r not in REGEN:
            size=18 if r in SUPPORT else 22
            out[r+16:r+21]=bytes((size,size,size-2,size,size))
            allowed.update(range(r+16,r+21))
        # Positions, line spacing, color/state flags, unknown-value templates
        # and every other field must stay intact, including the two-row variant.
        assert out[r+4:r+16]==blob[r+4:r+16]
        assert out[r+21:r+32]==blob[r+21:r+32]
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),(hex(r),en)
        assert en.count('\n')==jp.count('\n')
        size,budget=(18,50) if r in SUPPORT else (23,54) if r in REGEN else (22,36)
        for line in en.split('\n'):assert ink(line,mapping,widths,size)<=budget,(line,budget)
        if r in SUPPORT:
            for line in en.split('\n'): assert ink(line,mapping,widths,28)<45
        if r not in REGEN:
            assert blob[r+16:r+21]==bytes((size,size,size-2,size,size))
    assert blob[0xb9b94+21]==32
    print('PASS: compact popup MV, five support-label variants and two recovery-label copies fit; row spacing preserved.')
