"""Command-footer/help and complete live swap-equipment label family.

Only text pointers change in FSSA. Dynamic equipment uses exact draw hooks;
native equipment IDs, buffers, stats, positions and selection logic stay intact.
"""
from pathlib import Path
import struct
import aiddata
import digraph as dg
import localization
import trdata
from intermission_layout import text, ink

GROUP = 'command_swap_labels'
SWAP_TABLES = ((0x84b9fc, 0x6d93b0), (0x858d1c, 0x710800))
SWAP_DELTAS = (0, 8, 32, 48, 0, 64, 0, 64, 0, 64)
# Existing canonical terminology, including the already translated command.
ALIASES = (
    ('Ｅチェンジ', 'ui_eboot:r_6b15af9a0057cdc8', (0xac934,), (), 230, ''),
    ('おうえん', 'spirits:r_42a3f8446262fc22', (0xac874, 0xaca54), (), 230, ''),
    ('かんのう', 'spirits:r_180ca4e2094a2a03', (0xacab4,), (), 230, ''),
    ('戦術指揮', 'ui_eboot:r_15b4a90140e8a33a', (0xac9d4,), (), 230, ''),
    ('「スーパー・リペアキット」', 'parts:r_478a3d96ae9d85bb', (0xac974,), (), 1000, '「」'),
    ('ラウンドムーバー', 'ui.gift_reports:r_cd78bc2d48f96a46', (), (0x6d93b8, 0x710808), 390, ''),
    ('軽量仕様', 'ui.gift_reports:r_fdac634157ce7815', (), (0x6d93d0, 0x710820), 390, ''),
    ('強襲仕様', 'ui.gift_reports:r_b76e7b2887324130', (), (0x6d93e0, 0x710830), 390, ''),
)


def rows():
    cat = localization.english()
    for mid, d in cat.document('localization/messages/' + GROUP + '.json')['messages'].items():
        c = d['context']
        yield (d['source'], trdata._ex(cat.text(mid), mid),
               tuple(int(p, 16) for p in c['widgets']),
               tuple(int(p, 16) for p in c['eboot_offsets']), c['width_limit'], c['hook'])
    for jp, mid, widgets, offsets, width, quotes in ALIASES:
        en = cat.text(mid)
        if quotes:
            en = quotes[0] + en + quotes[1]
        yield jp, en, widgets, offsets, width, True


def hooks():
    return {jp: en for jp, en, _, _, _, hook in rows() if hook}


def check_source(elf, ui):
    # Both complete runtime tables: four equipment names, repeated BWS and
    # native None entries. Do not confuse unused FSSA sample lists with these.
    for table, base in SWAP_TABLES:
        pointers = tuple(struct.unpack_from('>I', elf, table + 8 * i)[0] for i in range(10))
        assert pointers == tuple(base + d + 0x10000 for d in SWAP_DELTAS), hex(table)
        names = {elf[p - 0x10000:elf.index(b'\0', p - 0x10000, p - 0x10000 + 64)].decode('cp932')
                 for p in pointers}
        assert names - {'なし'} <= hooks().keys(), names
    for jp, _, widgets, offsets, _, _ in rows():
        raw = jp.encode('cp932')
        for p in offsets:
            assert elf[p:p + len(raw) + 1] == raw + b'\0', (jp, hex(p))
        for r in widgets:
            assert text(ui, r) == raw, (jp, hex(r))


def apply(blob, mapping, widths, original):
    check_source(Path('work/EBOOT_dec.elf').read_bytes(), original)
    out = bytearray(blob)
    allowed = set()
    for jp, en, widgets, _, _, _ in rows():
        for r in widgets:
            assert text(blob, r) == jp.encode('cp932'), (jp, hex(r))
            p = (len(out) + 3) & ~3
            out += bytes(p - len(out)) + dg.encode_mixed(en, mapping) + b'\0'
            struct.pack_into('>I', out, r, p - aiddata.STR_BASE)
            allowed.update(range(r, r + 4))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(blob, out)))
    check_ui(out, mapping, widths)
    return bytes(out)


def check_ui(blob, mapping, widths):
    count = 0
    for jp, en, widgets, _, width, _ in rows():
        for r in widgets:
            assert text(blob, r) == dg.encode_mixed(en, mapping), (jp, hex(r))
            assert ink(en, mapping, widths, blob[r + 19]) <= width, (jp, width)
            count += 1
    print('PASS: %d command/footer widgets; geometry and dynamic placeholders unchanged.' % count)


def check_hooks(entries, mapping, widths):
    import eboot
    for jp, en, _, offsets, width, hook in rows():
        if hook:
            assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
        if offsets:
            assert ink(en, mapping, widths, 25) <= width, (jp, en)
    print('PASS: command help and all four swap-equipment names covered by exact hooks.')


def check_elf(blob, mapping, widths):
    import eboot
    source = Path('work/EBOOT_dec.elf').read_bytes()
    for table, base in SWAP_TABLES:
        assert blob[table:table + 76] == source[table:table + 76], hex(table)
        assert blob[base:base + 72] == source[base:base + 72], hex(base)
    segs = eboot._segments(blob)
    entries = {}
    p = eboot._off(segs, eboot.NAME_TBL)
    while True:
        key, value = struct.unpack_from('>II', blob, p)
        if not key:
            break
        entries[eboot._cstr(blob, eboot._off(segs, key))] = (
            value & 0xc0000000, eboot._cstr(blob, eboot._off(segs, value & 0x3fffffff)))
        p += 8
    check_hooks(entries, mapping, widths)
