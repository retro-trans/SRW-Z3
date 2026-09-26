"""Scoped missing battle/unit labels; source-guarded, no gameplay changes."""
import struct
import aiddata
import digraph as dg
import localization
from intermission_layout import text, ink

ROWS = ((0xa9754, 'ui_aiddata:battle_ko_risk', 125),
        (0xa9794, 'ui_aiddata:battle_armor', 100),
        (0x9e394, 'ui_aiddata:sync_rate', 125))
TETSUJIN_ID = 'glossary:r_33d597bb4a2bdf96'
TETSUJIN_UTF8_REFS = (0x84d46c, 0x84d4d8)
TETSUJIN_ORIGINAL_VA = 0x6ebbd8
MISATO_ID = 'glossary:r_bb5d440e312db945'
TOJI_ID = 'glossary:r_0de2d941a5560480'
HELP_ID = 'ui_utf8:barrier_icon_help'
SWORD_HELP_ID = 'ui_utf8:sword_icon_help'
UTF8_BINDINGS = (
    (TETSUJIN_ID, TETSUJIN_ORIGINAL_VA, TETSUJIN_UTF8_REFS),
    (MISATO_ID, 0x6ed090, (0x84e190, 0x84e194, 0x84e224, 0x84e228)),
    (TOJI_ID, 0x6ed118, (0x84e1c8,)),
    (HELP_ID, 0x71fe58, (0x858be4,)),
    (SWORD_HELP_ID, 0x71fa20, (0x858bcc,)),
)


def utf8_names():
    # Reuse the glossary; do not fork an editable English name into UI data.
    cat = localization.english()
    return {cat.definition(mid)['source']: cat.text(mid) for mid in (TETSUJIN_ID, MISATO_ID, TOJI_ID)}


def utf8_labels():
    cat = localization.english()
    return {cat.definition(mid)['source']: cat.text(mid) for mid, _, _ in UTF8_BINDINGS}


def check_source_elf(blob):
    import eboot
    segs = eboot._segments(blob)
    low = segs[1]['off']; high = low + segs[1]['filesz']
    for mid, va, expected_refs in UTF8_BINDINGS:
        off = eboot._off(segs,va)
        jp = localization.english().definition(mid)['source']
        assert off is not None and eboot._cstr(blob,off) == jp.encode('utf-8'), mid
        refs = tuple(p for p in range(low,high-3,4)
                     if struct.unpack_from('>I',blob,p)[0] == va)
        assert refs == expected_refs, ('Battle/help table changed', mid, refs)


def apply(blob, mapping, widths):
    cat = localization.english()
    out = bytearray(blob)
    allowed = set()
    for row, mid, budget in ROWS:
        assert text(blob, row) == cat.definition(mid)['source'].encode('cp932'), hex(row)
        en = cat.text(mid)
        assert ink(en, mapping, widths, blob[row+19]) <= budget, mid
        p = (len(out)+3) & ~3
        out += bytes(p-len(out)) + dg.encode_mixed(en, mapping) + b'\0'
        struct.pack_into('>I', out, row, p-aiddata.STR_BASE)
        allowed.update(range(row, row+4))
    assert all(a == b or i in allowed for i, (a,b) in enumerate(zip(blob,out)))
    check_ui(out, mapping, widths)
    return bytes(out)


def check_ui(blob, mapping, widths):
    for row, mid, budget in ROWS:
        en = localization.message(mid)
        assert text(blob,row) == dg.encode_mixed(en,mapping), mid
        assert ink(en,mapping,widths,blob[row+19]) <= budget, mid
    for mid in (HELP_ID, SWORD_HELP_ID):
        help_text = localization.message(mid)
        assert len(help_text.splitlines()) == 2 and help_text.endswith('\n')
        assert all(ink(line,mapping,widths,25) <= 963 for line in help_text.splitlines())
    print('PASS: KO Risk, Armor, Sync Rate, barrier and sword help fit; numeric/skull widgets untouched.')


def check_elf(blob, mapping):
    import eboot
    segs = eboot._segments(blob)
    table = eboot.unicode_table(blob,segs)
    for mid, _, refs in UTF8_BINDINGS:
        en = localization.message(mid)
        expected = ''.join(chr(eboot.VWF_CP_BASE+ord(c)) if ' ' <= c <= '~' else c for c in en).encode('utf-8')
        for ref in refs:
            va = struct.unpack_from('>I',blob,ref)[0]
            off = eboot._off(segs,va)
            assert off is not None and eboot._cstr(blob,off) == expected, (mid, hex(ref))
        for ch in en:
            if ' ' <= ch <= '~':
                assert struct.unpack_from('>H',blob,table+2*(eboot.VWF_CP_BASE+ord(ch)))[0] == mapping[ch]
    print('PASS: Tetsujin, Misato, Toji, barrier and sword UTF-8 references use canonical text and current font.')
