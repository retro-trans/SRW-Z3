"""Team Setup and Sub Orders: labels, accent headers and live-number templates.

Both screens were almost wholly Japanese: only the strings some other family
happened to hook at draw time came out English, which is why the menu read
"Change Pilots / Transform / 並び替え / チーム名称".

Wording lives in the shared catalog (`ui_aiddata:team_order_<key>`); this module
only binds it to FSSA widgets in AIDDATAPACK member 0. Binding kinds:

  label    repoint the widget's string.
  blank    repoint to an empty string: the Japanese split one phrase across
           several widgets (パイ + ロット：, バランス + オーダー), and the English
           lives whole in the first.
  accent   a coloured fragment drawn over its base line at a fixed x. The
           English accent must be a substring of the English base; both are
           switched to left-aligned and the accent is moved to the measured
           English position, as weapon_requirements does. Without this the
           accent keeps its Japanese x -- that is the overlapping "Custom Bonus"
           the user reported.
  accent_center  an accent base retaining its native center with English
           measurement (the Ace Bonus acquired notification).
  gap      a template with full-width spaces where a live number is drawn by
           another widget. The English keeps a gap of the same width and is
           moved so the gap starts exactly where the Japanese one did; the
           number widget itself is never touched.

Runtime copies of some strings are drawn from EBOOT, so `hooks()` supplies them
to the exact draw-time hook as well.
"""
import struct
import localization
import aiddata
import digraph as dg
from intermission_layout import text, ink

F = '　'
PREFIX = 'ui_aiddata:team_order_'

# key: (kind, rows)
BINDINGS = {
    # Sub Orders
    'so_training': ('label', (0xa6f94, 0xa6fb4)),
    'so_patrol': ('label', (0xa6fd4, 0xa6ff4)),
    'so_simulator': ('label', (0xa7014, 0xa7034)),
    'so_funding': ('label', (0xa7054, 0xa7074)),
    'so_run_all': ('label', (0xa7094, 0xa70b4, 0xa70d4)),
    'so_run_each': ('label', (0xa70f4, 0xa7114, 0xa7134)),
    'so_fill': ('label', (0xa7154,)),
    'so_mode': ('label', (0xa7194,)),
    'so_training_help': ('label', (0xa71b4,)),
    'so_patrol_help': ('label', (0xa71d4,)),
    'so_simulator_help': ('label', (0xa71f4,)),
    'so_funding_help': ('label', (0xa7214,)),
    'so_run_all_help': ('label', (0xa7234,)),
    'so_run_each_help': ('label', (0xa7254,)),
    'so_training_run': ('label', (0xa7274,)),
    'so_patrol_run': ('label', (0xa7294,)),
    'so_simulator_run': ('label', (0xa72b4,)),
    'so_funding_run': ('label', (0xa72d4,)),
    'so_all_done': ('label', (0xa72f4,)),
    'so_no_pilots': ('label', (0xa7314,)),
    'so_return_top': ('label', (0xa7354,)),
    'so_head_training': ('label', (0xa7394,)),
    'so_head_patrol': ('label', (0xa73b4,)),
    'so_head_simulator': ('label', (0xa73d4,)),
    'so_head_funding': ('label', (0xa73f4,)),
    'so_funds_badge': ('label', (0xa7474,)),
    'so_assigned': ('label', (0xa76d4,)),
    'so_raised_slash': ('label', (0xa7794,)),
    'so_raised': ('label', (0xa78f4,)),
    'so_idle_total': ('label', (0xa75f4, 0xa7934)),
    'so_idle_pi': ('blank', (0xa7654, 0xa7994)),
    'so_idle_lot': ('blank', (0xa7634, 0xa7974)),
    'so_left': ('label', (0xa7614, 0xa7954)),
    'so_can_pick': ('gap', (0xa7334,)),
    'so_got_pp': ('gap', (0xa77b4,)),
    'so_got_kills': ('gap', (0xa7814,)),
    'so_got_exp': ('gap', (0xa7874,)),
    'so_got_funds': ('gap', (0xa78d4,)),
    # Team Setup
    'tf_deploy': ('label', (0xb1ab4,)),
    'tf_grab': ('label', (0xb1bb4,)),
    'tf_place': ('label', (0xb1bd4,)),
    'tf_switch': ('label', (0xb1bf4,)),
    'tf_start': ('label', (0xb1c74,)),
    'tf_exclude': ('label', (0xb1c94,)),
    'tf_move_from': ('label', (0xb1d14,)),
    'tf_move_to': ('label', (0xb1d34,)),
    'tf_swap_from': ('label', (0xb1d54,)),
    'tf_swap_to': ('label', (0xb1d74,)),
    'tf_diamond': ('label', (0xb1e74, 0xb1e94)),
    'tf_keep_left': ('gap', (0xb1eb4,)),
    'tf_balance_head': ('label', (0xb1ef4,)),
    'tf_order_head': ('blank', (0xb1f14,)),
    'tf_auto_name_head': ('gap', (0xb1f34,)),
    'tf_sort_head': ('gap', (0xb1f54, 0xb1f74)),
    'tf_reorder': ('label', (0xb2314,)),
    'tf_team_name': ('label', (0xb2334,)),
    'tf_search_on': ('label', (0xb2434,)),
    'tf_search_off': ('label', (0xb2454,)),
    'tf_basic': ('label', (0xb24d4,)),
    'tf_basic_help': ('label', (0xb24b4,)),
    'tf_balance': ('label', (0xb2514,)),
    'tf_balance_help': ('label', (0xb24f4,)),
    # accent headers; the base key is the key without its _accent suffix
    'tf_auto_hint': ('accent_base', (0xb1ff4,)),
    'tf_auto_hint_accent': ('accent', (0xb2014,)),
    'tf_rename_hint': ('accent_base', (0xb2054,)),
    'tf_rename_hint_accent': ('accent', (0xb2074,)),
    'tf_update_hint': ('accent_base', (0xb20b4,)),
    'tf_update_hint_accent1': ('accent', (0xb20d4,)),
    'tf_update_hint_accent2': ('accent', (0xb20f4,)),
    'cb_got': ('accent_base', (0xaaa34,)),
    'cb_got_accent': ('accent', (0xaaa54,)),
    'ab_got': ('accent_center', (0xaa814,)),
    'ab_got_accent': ('accent', (0xaa834,)),
}
# EBOOT-drawn copies and runtime messages, supplied to the exact draw hook
RUNTIME = ('rt_renamed', 'rt_rename_marked', 'rt_balance_run', 'rt_grab', 'rt_place',
           'rt_switch', 'rt_to_swap', 'rt_to_move')
# widths the English may take, in native 1280-wide pixels, where the family
# has more room than its own Japanese: button columns sized for the longest
# label, help bars ~900 px wide, and a badge column already holding "Kills"
BUDGET = {
    'so_training': 252, 'so_patrol': 252, 'so_simulator': 252, 'so_funding': 252,
    'so_fill': 260, 'so_funding_run': 900, 'so_head_funding': 260,
    'so_funds_badge': 80, 'so_assigned': 230, 'so_raised': 100, 'tf_place': 75,
    'tf_balance_head': 224, 'tf_team_name': 180, 'tf_search_on': 180,
    'tf_search_off': 180, 'tf_auto_name_head': 350,
    # key hints share the family's widest slot (：移動モードへ, 147 px), which
    # already holds the shipped ': Move mode'
    'tf_move_from': 147, 'tf_swap_from': 147,
}


def base_of(key):
    return key.split('_accent')[0]


def labels():
    cat = localization.english()
    return {key: (cat.definition(PREFIX + key)['source'], cat.text(PREFIX + key))
            for key in list(BINDINGS) + list(RUNTIME)}


def hooks():
    names = labels()
    return {names[k][0]: names[k][1] for k in RUNTIME}


def _left(blob, row, jp_ink):
    """Left edge of a widget's Japanese text, in screen units (640 px = 1)."""
    x = struct.unpack_from('>f', blob, row + 4)[0]
    return x - jp_ink / 1280. if blob[row + 23] & 0x40 else x


def _width(s, mapping, widths, size):
    return max(ink(line, mapping, widths, size) for line in s.split('\n'))


def apply(blob, mapping, widths):
    names = labels()
    out = bytearray(blob)
    allowed = set()

    def repoint(row, en):
        p = (len(out) + 3) & ~3
        out.extend(bytes(p - len(out)) + dg.encode_mixed(en, mapping, newline=b'\n') + b'\0')
        struct.pack_into('>I', out, row, p - aiddata.STR_BASE)
        allowed.update(range(row, row + 4))

    def place(row, x):
        struct.pack_into('>f', out, row + 4, x)
        out[row + 23] &= ~0x40
        allowed.update(range(row + 4, row + 8))
        allowed.add(row + 23)

    for key, (kind, rows) in BINDINGS.items():
        jp, en = names[key]
        for row in rows:
            assert text(blob, row) == jp.encode('cp932'), (key, hex(row))
            assert en.count('\n') <= jp.count('\n'), key
            repoint(row, en)
            size = blob[row + 19]
            if kind == 'gap':
                jp_pre, en_pre = jp.split(F)[0], en.split(F)[0]
                assert F * (jp.count(F)) in jp and en.count(F) == jp.count(F), key
                left = _left(blob, row, ink(jp, mapping, widths, size))
                shift = (ink(jp_pre, mapping, widths, size) - ink(en_pre, mapping, widths, size)) / 640.
                place(row, left + shift)
            elif kind in ('accent_base', 'accent_center'):
                # The acquired-Ace notice retains the native sentence center.
                measured = en if kind == 'accent_center' else jp
                left = _left(blob, row, ink(measured, mapping, widths, size))
                place(row, left)
                for akey, (akind, arows) in BINDINGS.items():
                    if akind == 'accent' and base_of(akey) == key:
                        ajp, aen = names[akey]
                        assert aen in en, (akey, aen, en)
                        pre = en[:en.index(aen)]
                        for arow in arows:
                            assert blob[arow + 19] == size, akey
                            # the accent's own repoint happens in its turn
                            place(arow, left + ink(pre, mapping, widths, size) / 640.)
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(blob, out)))
    check(out, mapping, widths, blob)
    return bytes(out)


def check(blob, mapping, widths, original=None):
    names = labels()
    for key, (kind, rows) in BINDINGS.items():
        jp, en = names[key]
        for row in rows:
            assert text(blob, row) == dg.encode_mixed(en, mapping, newline=b'\n'), (key, hex(row))
            size = blob[row + 19]
            if kind == 'blank':
                assert en == '', key
                continue
            if kind == 'accent':
                continue                      # measured as part of its base
            limit = BUDGET.get(key, max(len(l) for l in jp.split('\n')) * size)
            assert _width(en, mapping, widths, size) <= limit, (key, en, limit)
            if kind == 'accent_center' and original is not None:
                assert original[row+23] & 0x40
                center = struct.unpack_from('>f', original, row+4)[0]*640
                left = struct.unpack_from('>f', blob, row+4)[0]*640
                assert abs(left+ink(en,mapping,widths,size)/2-center)<.01, key
    # accents sit exactly over their English substring
    for key, (kind, rows) in BINDINGS.items():
        if kind != 'accent':
            continue
        base = base_of(key)
        (brow,) = BINDINGS[base][1]
        bx = struct.unpack_from('>f', blob, brow + 4)[0]
        size = blob[brow + 19]
        en = names[base][1]
        pre = en[:en.index(names[key][1])]
        for row in rows:
            ax = struct.unpack_from('>f', blob, row + 4)[0]
            assert abs((ax - bx) * 640 - ink(pre, mapping, widths, size)) < .01, key
            assert not blob[row + 23] & 0x40 and not blob[brow + 23] & 0x40, key
    # live-number gaps start where the Japanese gap started
    if original is not None:
        for key, (kind, rows) in BINDINGS.items():
            if kind != 'gap':
                continue
            jp, en = names[key]
            for row in rows:
                size = original[row + 19]
                jl = _left(original, row, ink(jp, mapping, widths, size))
                el = struct.unpack_from('>f', blob, row + 4)[0]
                jgap = jl * 640 + ink(jp.split(F)[0], mapping, widths, size)
                egap = el * 640 + ink(en.split(F)[0], mapping, widths, size)
                assert abs(jgap - egap) < .01, key
    n = sum(len(rows) for _, rows in BINDINGS.values())
    print('PASS: Team Setup / Sub Orders / Custom Bonus: %d widgets; accents registered, '
          'live-number gaps aligned, English fits.' % n)


def check_hooks(entries, mapping):
    import eboot
    from pathlib import Path
    original = Path('work/EBOOT_dec.elf').read_bytes()
    for jp, en in hooks().items():
        assert jp.encode('cp932') + b'\0' in original, jp
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
