"""Exact translations for the warning list rebuilt by the executable.

The 14 FSSA widgets repaired earlier are templates, not the only text source.
VA 0x331088 loads the separate 16-slot table at 0x869194; the constructor
copies its Japanese keys into eight 0x101-byte rows and sets failure colors.
Translate only at the final drawer, leaving those buffers and flags intact.
"""
import hashlib
from pathlib import Path
import struct
import localization

GROUP = 'weapon_requirement_runtime'
TABLE = 0x859194  # File offset, not VA.
OFFSETS = (0x7115b0, 0x7115b8, 0x7115c0, 0x7115c8, 0x7115d8,
           0x7115e0, 0x7115e8, 0x7115f8, 0x711608, 0x711620,
           0x711638, 0x711650, 0x711668, 0x711668, 0x711688, 0x711698)
CONSTRUCTOR = (0x321060, 0x321490)
CONSTRUCTOR_SHA = 'd619a753f239e6cca14b1c884f9caee84a1f87afdff0e678a16c1cda8c1c7a0a'
PLACEHOLDER = '・－－－－－－－－－'


def rows():
    cat = localization.english()
    for mid, d in cat.document('localization/messages/' + GROUP + '.json')['messages'].items():
        yield int(d['context']['eboot_offset'], 16), d['source'], cat.text(mid)


def source_inventory(source):
    assert struct.unpack_from('>16I', source, TABLE) == tuple(p + 0x10000 for p in OFFSETS)
    assert struct.unpack_from('>I', source, 0x7cc28c)[0] == TABLE + 0x10000
    lo, hi = CONSTRUCTOR
    assert hashlib.sha256(source[lo:hi]).hexdigest() == CONSTRUCTOR_SHA
    keys = []
    for p in OFFSETS:
        end = source.index(b'\0', p, p + 128)
        keys.append(source[p:end].decode('cp932'))
    assert keys[-1] == PLACEHOLDER
    expected = {p: jp for p, jp, _ in rows()}
    assert set(expected) == set(OFFSETS[:-1])
    for p, jp in zip(OFFSETS[:-1], keys[:-1]):
        assert expected[p] == jp, hex(p)
    return keys


def hooks():
    source_inventory(Path('work/EBOOT_dec.elf').read_bytes())
    return {jp: en for _, jp, en in rows()}


def check(elf, mapping, widths):
    import eboot
    from intermission_layout import ink
    source = Path('work/EBOOT_dec.elf').read_bytes()
    source_inventory(source)
    segs = eboot._segments(elf)
    # Buffers, selection predicates, colors and the original Japanese source
    # stay byte-for-byte native. Includes the separate fixed-size Song EN copy.
    spans = [(TABLE, TABLE + 64), (0x7cc28c, 0x7cc29c), CONSTRUCTOR,
             (OFFSETS[0], OFFSETS[-1] + len(PLACEHOLDER.encode('cp932')) + 1)]
    for lo, hi in spans:
        pos = eboot._off(segs, lo + 0x10000)
        assert elf[pos:pos + hi - lo] == source[lo:hi], hex(lo)
    entries = {}
    p = eboot._off(segs, eboot.NAME_TBL)
    while True:
        key, value = struct.unpack_from('>II', elf, p)
        if not key:
            break
        entries[eboot._cstr(elf, eboot._off(segs, key))] = (
            value & 0xc0000000,
            eboot._cstr(elf, eboot._off(segs, value & 0x3fffffff)))
        p += 8
    for _, jp, en in rows():
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
        assert ink(en, mapping, widths, 31) < 420, en
    print('PASS: all 16 runtime weapon-warning slots covered (14 unique labels plus placeholder); native state/color logic unchanged.')
