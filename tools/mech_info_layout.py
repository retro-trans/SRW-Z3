"""Center both Mech Info headings without moving adjacent U/P/W tabs."""
import localization as _l10n
import struct
from intermission_layout import text,ink

ROWS=(0xa0654,0xba014)
LABEL=_l10n.literal('mech_info_layout.LABEL/0')
JP='機体能力'
# Native 1280px screen: pointed title tab is approximately x=192..432.
# Exclude the slanted ends when checking the English text's fit.
CENTER=312.
SAFE=(212.,412.)
QUAD=31


def apply(blob,mapping,widths):
    out=bytearray(blob)
    width=ink(LABEL,mapping,widths,QUAD)
    assert width<SAFE[1]-SAFE[0]
    for r in ROWS:
        assert text(blob,r)==JP.encode('cp932'),hex(r)
        assert blob[r+16:r+20]==bytes((42,42,27,31))
        assert not blob[r+23]&0x40
        struct.pack_into('>f',out,r+4,(CENTER-width/2-640)/640)
    allowed={p for r in ROWS for p in range(r+4,r+8)}
    assert len(blob)==len(out)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)


def check(blob,mapping,widths):
    width=ink(LABEL,mapping,widths,QUAD)
    for r in ROWS:
        assert text(blob,r)==JP.encode('cp932')
        left=640+struct.unpack_from('>f',blob,r+4)[0]*640
        assert abs(left+width/2-CENTER)<.001
        assert SAFE[0]<=left and left+width<=SAFE[1]
        assert blob[r+19]==QUAD and not blob[r+23]&0x40
    print('PASS: both Mech Info headings centered at native x=312; only title x positions changed.')
