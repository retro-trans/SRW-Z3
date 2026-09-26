"""Translate both split Unit Info currency captions; preserve live amounts."""
import struct

import aiddata
import digraph as dg
import localization
from intermission_layout import ink, text

LABEL_ID = 'ui.mech_info_layout:funds_z_chips'
# Original AIDDATAPACK member 0: funds/chips widgets in both layout variants.
ROWS = ((0x9a7d4, 0x9a7f4), (0xb9dd4, 0xb9e14))
AMOUNT = 0xb9df4
QUAD = 23
GAP = 8


def apply(blob, mapping, widths, pristine):
    label = localization.message(LABEL_ID)
    out = bytearray(blob)
    allowed = set()
    for funds, chips in ROWS:
        for record, jp, en in ((funds, '所持資金／', label), (chips, 'チップ：', '')):
            assert text(pristine, record) == jp.encode('cp932'), hex(record)
            assert blob[record+4:record+32] == pristine[record+4:record+32], hex(record)
            raw = dg.encode_mixed(en, mapping) + b'\0'
            at = (len(out)+3) & ~3
            out += bytes(at-len(out)) + raw
            struct.pack_into('>I', out, record, at-aiddata.STR_BASE)
            allowed.update(range(record, record+4))
        # Only the visible glyph quad shrinks slightly, retaining origin,
        # baseline, colour and draw flags. Numeric widgets are never edited.
        assert out[funds+19] == 25 and not out[funds+23] & 0x40
        out[funds+19] = QUAD
        allowed.add(funds+19)
    assert all(a == b or i in allowed for i, (a,b) in enumerate(zip(blob,out)))
    check(out, mapping, widths)
    return bytes(out)


def check(blob, mapping, widths):
    label = localization.message(LABEL_ID)
    amount_x = struct.unpack_from('>f', blob, AMOUNT+4)[0]
    for funds, chips in ROWS:
        assert text(blob,funds) == dg.encode_mixed(label,mapping)
        assert text(blob,chips) == b''
        assert blob[funds+19] == QUAD and not blob[funds+23] & 0x40
        origin = struct.unpack_from('>f',blob,funds+4)[0]
        assert ink(label,mapping,widths,QUAD)+GAP <= (amount_x-origin)*640
    print('PASS: both Unit Info Funds / Z Chips captions fit; numeric widgets preserved.')
