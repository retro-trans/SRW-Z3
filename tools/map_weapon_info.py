"""MAP weapon IFF states and the complete pattern row, PS3 only.

Keep native runtime value anchors and font sizes. Move only the three static
Pattern headers; use measured compact names for all four pattern modes.
Exact draw hooks cover live EBOOT states, while the two FSSA defaults are
translated separately. No native string buffers or targeting logic change.
"""
import struct
import aiddata
import digraph as dg
import localization
from intermission_layout import text, ink

HEADERS = (0xadb74, 0xb7574, 0xb8934)
IFF_HEADERS = (0xadb54, 0xb7554, 0xb8914)
DEFAULTS = (0x9dbb4, 0xb89f4)
PATTERN_DEFAULTS = (0x9dbd4, 0xb8a14)
PATTERNS = (
    ('自機中心', 'ui_hook:r_6ff1323b355593e0', 0x711218),
    ('着弾点指定', 'ui_hook:r_b7b5625d7cd4282f', 0x711228),
    ('直線探索', 'ui_hook:r_36133ad73a73ef98', 0x711238),
    ('方向指定', 'ui_hook:r_920740a0219c5085', 0x711248),
)
STATES = (('無効', 'map_weapon_info:iff_off', 0x7111f8),
          ('有効', 'map_weapon_info:iff_on', 0x711200))
PATTERN_X = 570.5
VALUE_X = 691.5
RIGHT = 830.0  # conservative inner right edge, before the panel border
GAP = 8.0


def hooks():
    return {jp: localization.english().text(mid) for jp, mid, _ in STATES}


def check_source(elf, ui):
    for jp, _, off in STATES + PATTERNS:
        raw = jp.encode('cp932') + b'\0'
        assert elf[off:off + len(raw)] == raw, (jp, hex(off))
    assert elf[0x711208:0x711213] == '－－－－－'.encode('cp932') + b'\0'
    expected = [(r, '形式：') for r in HEADERS]
    expected += [(r, '敵味方識別：') for r in IFF_HEADERS]
    expected += [(r, '無効') for r in DEFAULTS]
    expected += [(r, '方向指定') for r in PATTERN_DEFAULTS]
    for r, jp in expected:
        assert text(ui, r) == jp.encode('cp932'), (hex(r), jp)
        assert ui[r + 19] == 28, hex(r)
    for r in HEADERS:
        assert struct.unpack_from('>f', ui, r + 4)[0] == -0.05078125, hex(r)
    # Inventory every FSSA member-0 occurrence, not just the screenshot's view.
    refs = aiddata.refs(ui)
    for jp in ('形式：', '敵味方識別：', '無効', '方向指定'):
        actual = {r for p, s, _, _ in aiddata.strings(ui) if s == jp
                  for r in refs.get(p, [])}
        assert actual == {r for r, s in expected if s == jp}, (jp, actual)


def apply(blob, mapping, widths, original):
    for r in HEADERS + DEFAULTS:
        assert blob[r:r + 32] == original[r:r + 32], hex(r)
    out = bytearray(blob)
    for r in HEADERS:
        struct.pack_into('>f', out, r + 4, (PATTERN_X - 640) / 640)
    raw = dg.encode_mixed(hooks()['無効'], mapping) + b'\0'
    p = (len(out) + 3) & ~3
    out += bytes(p - len(out)) + raw
    for r in DEFAULTS:
        struct.pack_into('>I', out, r, p - aiddata.STR_BASE)
    allowed = {i for r in HEADERS for i in range(r + 4, r + 8)}
    allowed |= {i for r in DEFAULTS for i in range(r, r + 4)}
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(blob, out)))
    check_ui(out, mapping, widths)
    return bytes(out)


def check_widths(mapping, widths):
    cat = localization.english()
    def width(mid):
        en = cat.text(mid)
        assert all(c in mapping for c in en), (mid, en)
        return ink(en, mapping, widths, 28)
    assert 351.5 + width('ui_hook:r_02479dc8fe989560') + GAP <= 520.5
    for _, mid, _ in STATES:
        assert 520.5 + width(mid) + GAP <= PATTERN_X, mid
    assert PATTERN_X + width('ui_hook:r_a2df00f91a9b0a9e') + GAP <= VALUE_X
    for _, mid, _ in PATTERNS:
        assert VALUE_X + width(mid) <= RIGHT, mid


def check_ui(blob, mapping, widths):
    for r in HEADERS:
        x = 640 + struct.unpack_from('>f', blob, r + 4)[0] * 640
        assert abs(x - PATTERN_X) < 0.001, (hex(r), x)
    for r in DEFAULTS:
        assert text(blob, r) == dg.encode_mixed(hooks()['無効'], mapping), hex(r)
    check_widths(mapping, widths)
    print('PASS: MAP row, three headers, two IFF states and all four patterns fit.')


def check_hooks(entries, mapping):
    import eboot
    cat = localization.english()
    for jp, mid, _ in STATES + PATTERNS:
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(cat.text(mid), mapping)), jp
