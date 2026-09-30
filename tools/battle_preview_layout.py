"""Battle-preview labels only; retain counters, punctuation and widget styles."""
import localization as _l10n
import struct
import aiddata
import command_layout as layout
import digraph as dg

ROWS = {
    0x9ac94: ('攻撃', _l10n.literal('battle_preview_layout.ROWS/0')),
    0xb11f4: ('攻撃', _l10n.literal('battle_preview_layout.ROWS/1')),
    0xbbe94: ('残弾数', _l10n.literal('battle_preview_layout.ROWS/2')),
    0xb0eb4: ('援護攻撃', _l10n.literal('battle_preview_layout.ROWS/3')),
    0xb0ef4: ('援護防御', _l10n.literal('battle_preview_layout.ROWS/4')),
    0xb0ed4: ('再攻撃', _l10n.literal('battle_preview_layout.ROWS/5')),
    0xb0cf4: ('戦闘開始', _l10n.literal('battle_preview_layout.ROWS/6')),
    0xb0d14: ('戦闘開始', _l10n.literal('battle_preview_layout.ROWS/7')),
    0xb1014: ('戦闘開始', _l10n.literal('battle_preview_layout.ROWS/8')),
    0xb1034: ('戦闘開始', _l10n.literal('battle_preview_layout.ROWS/9')),
}


def encoded(label, mapping):
    pad = (struct.pack('>H', layout.CODES[layout.LABELS.index(label)])
           if label == 'Start Battle' else b'')
    return pad + dg.encode_mixed(label, mapping) + b'\0'


def check(blob, mapping, widths):
    import battle_unit_name_layout
    battle_unit_name_layout.check_ui(blob)
    for record, (_, label) in ROWS.items():
        pos = struct.unpack_from('>I', blob, record)[0] + aiddata.STR_BASE
        raw = encoded(label, mapping)
        assert blob[pos:pos+len(raw)] == raw, (hex(record), label)
        if label == 'Start Battle':
            assert blob[record+23] & 0x40, 'Live pad requires centered draw'
    def ink(label, quad):
        return sum(widths[dg.cell_index(mapping[c])] for c in label)*quad/32.
    # Native-coordinate budgets from the label/colon widgets and screenshot.
    colon_gap = (struct.unpack_from('>f', blob, 0xbbeb4+4)[0]
                 - struct.unpack_from('>f', blob, 0xbbe94+4)[0])*640
    assert ink('Rnd.', 23)+4 < colon_gap
    assert ink('S. Atk', 23)+12 < 96
    # Actual screenshot: the use counter starts about 96 native pixels
    # after the title origin. Check every title sharing that narrow panel.
    for label in ('S. Atk','S. Def','Re-Atk'):
        assert ink(label,23)+12<96
    assert ink('Atk.', 37)+8 < 94
    assert ink('Start Battle', 31)+16 < 220
    print('PASS: ten battle-preview variants; all three support-panel titles clear the use counter.')


def apply(blob, mapping, widths):
    result = bytearray(blob)
    for record, (jp, label) in ROWS.items():
        pos = struct.unpack_from('>I', blob, record)[0] + aiddata.STR_BASE
        original = jp.encode('cp932') + b'\0'
        assert blob[pos:pos+len(original)] == original, hex(record)
        raw = encoded(label, mapping)
        pos = (len(result)+3) & ~3
        result += bytes(pos-len(result)) + raw
        struct.pack_into('>I', result, record, pos-aiddata.STR_BASE)
    allowed = {p for r in ROWS for p in range(r, r+4)}
    assert all(x == y or i in allowed for i, (x,y) in enumerate(zip(blob,result)))
    check(result, mapping, widths)
    return bytes(result)
