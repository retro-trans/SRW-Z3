"""PS3 long battle-name workaround: translate at draw time, not before copying.

These historical three-name deferrals predate the category-wide native
caption fix in battle_name_transport.py (see docs/BATTLE_NAME_TRANSPORT.md).
Retain the compatible RPW representation and exact draw hooks; do not extend
this exception list to repair additional names. The shared transport now
protects all names from the established 31-byte caption overflow.
"""
import localization
import rpw
import struct

MESSAGE_IDS = (
    'glossary:r_113f2c9a6485442c',
    'enemy_names:r_34dc6d5fcf53fd54',
    'enemy_names:r_50e87a2fb9246781',
)


def hooks():
    cat = localization.english()
    return {cat.definition(mid)['source']: cat.text(mid) for mid in MESSAGE_IDS}


def deferred_indices(raw):
    keys = set(hooks())
    strings = rpw.jstrings(raw)
    found = {strings[i] for slot, i in rpw.slots(raw).items()
             if slot[0] == 'pilot-nw' and strings[i] in keys}
    if found != keys:
        raise ValueError('Long battle-name source changed: ' + repr(keys - found))
    if any(len(jp.encode('cp932')) > 30 for jp in keys):
        raise ValueError('Deferred battle name exceeds the observed safe length')
    return {i for i, jp in enumerate(strings) if jp in keys}


def defer_swaps(raw, swaps):
    keep = deferred_indices(raw)
    return {i: value for i, value in swaps.items() if i not in keep}


def defer_overrides(raw, overrides):
    keep = deferred_indices(raw)
    slots = rpw.slots(raw)
    return {slot: value for slot, value in overrides.items()
            if slots[slot] not in keep}


def check_rpw(original, patched):
    keys = deferred_indices(original)
    old_strings = rpw.jstrings(original)
    _, _, start, end, _ = next(c for c in rpw.chunks(patched) if c[0] == 'j-string')
    # VWF cell codes in unrelated translated slots need not decode as CP932.
    new_strings = patched[start:end].split(b'\0')
    new_slots = rpw.slots(patched)
    count = 0
    for slot, index in rpw.slots(original).items():
        if index in keys:
            assert new_strings[new_slots[slot]] == old_strings[index].encode('cp932'), slot
            count += 1
    assert count
    return count


def check_elf(blob, mapping):
    import eboot
    import digraph
    segs = eboot._segments(blob)
    entries = {}
    pos = eboot._off(segs, eboot.NAME_TBL)
    while True:
        jp, en = struct.unpack_from('>II', blob, pos)
        if not jp:
            break
        key = bytes(eboot._cstr(blob, eboot._off(segs, jp)))
        entries.setdefault(key, (en >> 30, eboot._cstr(blob, eboot._off(segs, en & 0x3fffffff))))
        pos += 8
        assert pos < eboot._off(segs, eboot.NAME_STR), 'Unterminated name hook table'
    for jp, en in hooks().items():
        assert entries[jp.encode('cp932')] == (0, digraph.encode_mixed(en, mapping)), jp
    stub = eboot._off(segs, eboot.NAME_STUB)
    assert blob[stub:stub + len(eboot.name_stub())] == eboot.name_stub()
