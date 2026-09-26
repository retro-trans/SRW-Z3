"""Name-entry labels only; never translate the selectable character palette."""
import struct
from pathlib import Path
import localization
import digraph as dg
import aiddata
from intermission_layout import text, ink

BINDINGS = (
    ('heading', (0xa5914, 0xa5a74, 0xa5c14)),
    ('space', (0x9be94,)),
    ('delete', (0x9beb4,)),
    ('auto', (0xbc274, 0xbc4d4)),
    ('hiragana', (0xbc294, 0xbc394, 0xbc574, 0xbc654)),
    ('reset', (0xbc2b4, 0xbc3b4, 0xbc494, 0xbc4f4)),
    ('confirm', (0xbc2d4, 0xbc3d4, 0xbc4b4, 0xbc514)),
    ('katakana', (0xbc6f4,)),
    ('kanji', (0xbc794, 0xbc814)),
    ('alphanumeric', (0xbc894,)),
    ('symbols', (0xbc8f4,)),
    ('auto_help', (0xbc534, 0xbc614)),
    ('type_help', (0xbc554, 0xbc974)),
    ('hiragana_help', (0xbc5f4, 0xbc6d4)),
    ('katakana_help', (0xbc774,)),
    ('kanji_reading_help', (0xbc7f4,)),
    ('kanji_help', (0xbc874,)),
    ('alphanumeric_help', (0xbc8d4,)),
    ('symbols_help', (0xbc934,)),
    ('left_help', (0xbc994,)),
    ('right_help', (0xbc9b4,)),
    ('reset_help', (0xbc9d4,)),
    ('finish_help', ()),
    ('return_help', (0xbc9f4,)),
)


def labels():
    cat = localization.english()
    return {key: (cat.definition('ui_aiddata:name_entry_' + key)['source'],
                  cat.text('ui_aiddata:name_entry_' + key)) for key, _ in BINDINGS}


def hooks():
    # Runtime replacements of the category/button/help text can come from
    # EBOOT rather than the FSSA templates. Keep original lookup/input data.
    return dict(labels().values())


def apply(blob, mapping, widths):
    out = bytearray(blob)
    allowed = set()
    names = labels()
    for key, rows in BINDINGS:
        jp, en = names[key]
        for row in rows:
            assert text(blob, row) == jp.encode('cp932'), (key, hex(row))
            p = (len(out) + 3) & ~3
            out += bytes(p - len(out)) + dg.encode_mixed(en, mapping) + b'\0'
            struct.pack_into('>I', out, row, p - aiddata.STR_BASE)
            allowed.update(range(row, row + 4))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(blob, out)))
    check(out, mapping, widths)
    return bytes(out)


def check(blob, mapping, widths):
    names = labels()
    for key, rows in BINDINGS:
        jp, en = names[key]
        # Widths in the native1280-wide layout, before screenshot scaling.
        budget = 730 if key.endswith('_help') else (290 if key == 'heading' else 180)
        size = 31 if key.endswith('_help') else 28
        assert ink(en, mapping, widths, size) <= budget, (key, en)
        for row in rows:
            assert text(blob, row) == dg.encode_mixed(en, mapping), (key, hex(row))
    print('PASS: name-entry labels/help fit; only selected text pointers change.')


def check_hooks(entries, mapping):
    import eboot
    original = Path('work/EBOOT_dec.elf').read_bytes()
    for jp, en in hooks().items():
        if jp.encode('cp932') + b'\0' in original:
            assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
