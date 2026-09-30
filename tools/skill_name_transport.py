"""Keep skill names inside native 32-byte result rows, expanding only at draw.

The result producer at0x2ffb38 stores eight strings at stride0x20. It appends
up to two fullwidth suffix pairs (L9/+9) before strcpy. A 32-byte English
name loses its terminator when the next row is copied, displaying both rows.
Select by capacity, never by a particular skill's spelling.
"""
import hashlib
import struct
import localization
import rpw
import digraph as dg

CAPACITY = 32
SUFFIX_BYTES = 8  # fullwidth L + digit + plus + digit
REGIONS = (
    (0x2ffb38, 0x2ffca0, '611ebb8b62cbc938f820b4dab7d8e2a504385e75854336335fab0cff59136e89'),
    (0x300058, 0x30017c, '1716fbb214910f1a347011f4318fd3bd81ee846f9ccf4c1d2f638b23a340195e'),
)


def names():
    cat = localization.english()
    result = {cat.definition(mid)['source']: cat.text(mid)
              for mid in cat.locale('en', 'skills')}
    # Match build_project's precedence for strings shared with other tables.
    for group in ('weapons', 'glossary'):
        for mid in cat.locale('en', group):
            jp = cat.definition(mid)['source']
            if jp in result:
                result[jp] = cat.text(mid)
    return result


def deferred():
    # Current VWF transport is exactly two bytes per English letter.
    result = {jp: en for jp, en in names().items()
              if 2 * len(en) + SUFFIX_BYTES + 1 > CAPACITY}
    for jp in result:
        assert len(jp.encode('cp932')) + SUFFIX_BYTES + 1 <= CAPACITY, jp
    return result


def hooks():
    exact, prefixes = {}, set()
    for jp, en in deferred().items():
        exact[jp] = en
        # Only level/bonus suffixes qualify as prefixes; no broad skill-name
        # prefix can consume prose, another skill name or a description.
        for suffix, label in (('Ｌ', ' L'), ('＋', '+')):
            exact[jp + suffix] = en + label
            prefixes.add(jp + suffix)
    return exact, prefixes


def overrides(raw):
    js = rpw.jstrings(raw)
    keys = deferred()
    result = {slot: js[i].encode('cp932') for slot, i in rpw.slots(raw).items()
              if slot[0] == 'sk-pri' and 1 <= slot[2] <= 3 and js[i] in keys}
    assert {v.decode('cp932') for v in result.values()} == set(keys)
    return result


def check_source(blob):
    import eboot
    segs = eboot._segments(blob)
    for start, end, expected in REGIONS:
        pos = eboot._off(segs, start)
        assert hashlib.sha256(blob[pos:pos+end-start]).hexdigest() == expected, hex(start)


def check_rpw(original, patched):
    expected = overrides(original)
    _, _, start, end, _ = next(c for c in rpw.chunks(patched) if c[0] == 'j-string')
    strings = patched[start:end].split(b'\0')
    count = 0
    for slot, i in rpw.slots(patched).items():
        if slot[0] != 'sk-pri' or not 1 <= slot[2] <= 3:
            continue
        value = strings[i]
        assert len(value) + SUFFIX_BYTES + 1 <= CAPACITY, (slot, len(value))
        if slot in expected:
            assert value == expected[slot], slot
        count += 1
    assert count == 207, 'Skill name-column inventory changed'
    return count


def check_elf(blob, mapping):
    import eboot
    check_source(blob)
    segs = eboot._segments(blob)
    pos = eboot._off(segs, eboot.NAME_TBL)
    entries = {}
    while True:
        jp, en = struct.unpack_from('>II', blob, pos)
        if not jp:
            break
        key = eboot._cstr(blob, eboot._off(segs, jp))
        entries.setdefault(bytes(key), (en >> 30, eboot._cstr(blob, eboot._off(segs, en & 0x3fffffff))))
        pos += 8
        assert pos < eboot._off(segs, eboot.NAME_STR)
    labels, prefixes = hooks()
    for jp, en in labels.items():
        assert entries[jp.encode('cp932')] == (2 if jp in prefixes else 0, dg.encode_mixed(en, mapping)), jp
