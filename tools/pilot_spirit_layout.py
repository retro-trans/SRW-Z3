"""Pilot status Spirit-name/cost columns, both status-sheet variants.

Keep full canonical Spirit names. Compact only their glyph metrics and move
the cost column 24 native pixels into the remaining panel space. Preserve
five-row line spacing, live costs, unknown commands, colors and all text.
"""
import struct
import localization
from intermission_layout import text, ink

ROWS = ((0xb83f4, 0xb8414), (0xb8cb4, 0xb8cd4))
NAMES_JP = 'てかげん\n集中\nド根性\nひらめき\n魂'
COSTS_JP = '\n'.join(['（９９９）'] * 5)
SOURCE_STYLE = bytes.fromhex('3a3a1a1c1c36')
STYLE = bytes((18, 18, 16, 18, 18, 54))
COST_SHIFT = 24


def names():
    cat = localization.english()
    return [cat.text(mid) for mid in cat.document('localization/messages/spirits.json')['messages']
            if cat.text(mid, allow_missing=True)]


def apply(blob, mapping, widths, original):
    out = bytearray(blob)
    allowed = set()
    for name, cost in ROWS:
        assert text(original, name) == NAMES_JP.encode('cp932'), hex(name)
        assert text(original, cost) == COSTS_JP.encode('cp932'), hex(cost)
        assert original[name+16:name+22] == SOURCE_STYLE, hex(name)
        assert blob[name+16:name+22] == SOURCE_STYLE, 'Spirit metrics already modified'
        assert blob[cost+4:cost+8] == original[cost+4:cost+8], 'Spirit cost position already modified'
        out[name+16:name+22] = STYLE
        x = struct.unpack_from('>f', original, cost+4)[0]
        struct.pack_into('>f', out, cost+4, x + COST_SHIFT/640.)
        allowed.update(range(name+16, name+22))
        allowed.update(range(cost+4, cost+8))
    assert all(a == b or i in allowed for i, (a,b) in enumerate(zip(blob,out)))
    check(out, mapping, widths, original)
    return bytes(out)


def check(blob, mapping, widths, original):
    for name, cost in ROWS:
        assert blob[name+16:name+22] == STYLE
        # Live five-row cadence and cost rendering are not reduced or rewritten.
        assert blob[name+21] == original[name+21] == 54
        assert blob[cost+8:cost+32] == original[cost+8:cost+32]
        nx = struct.unpack_from('>f', blob, name+4)[0]
        cx = struct.unpack_from('>f', blob, cost+4)[0]
        ox = struct.unpack_from('>f', original, cost+4)[0]
        assert abs((cx-ox)*640 - COST_SHIFT) < .001
        gap = (cx-nx)*640
        for label in names():
            assert ink(label, mapping, widths, STYLE[3]) + 8 < gap, label
        # Five fixed-pitch source cells cover the widest (999)/(???) cost.
        # Use a conservative 224px budget from the name's inset left edge,
        # leaving space at the panel border before the next stats column.
        assert gap + 5 * original[cost+18] < 224
    print('PASS: every Spirit name clears the cost column in both pilot sheets; costs/unknown rows unchanged.')
