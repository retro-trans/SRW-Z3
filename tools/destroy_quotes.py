"""Map shot-down / retreat quotes, as exact draw-time hooks.

When a unit is destroyed or forced out on the map, its pilot says a line from
one EBOOT table (VA 0x6f5980..0x6f72d0; e.g. Michel's
「ミスった…！　スカル２、撤退する！」). None of its 146 lines had a hook, so
every one drew in Japanese under an English speaker name.

The lines are referenced from 12-byte records (text VA, character/condition
key, type), often several characters to one generic line. Wording lives in
the `destroy_quotes` catalog group, keyed by EBOOT VA, with the translator's
speaker identification kept as context. Keys point at the Japanese already in
the ELF (no EXT copy) and there are no per-line pairs, exactly as for
bonus_descriptions.
"""
from pathlib import Path
import localization

GROUP = 'destroy_quotes'


def hooks():
    cat = localization.english()
    defs = cat.document('localization/messages/%s.json' % GROUP)['messages']
    return {d['source']: cat.text(mid) for mid, d in defs.items() if cat.text(mid)}


def check_hooks(entries, mapping):
    import eboot
    original = Path('work/EBOOT_dec.elf').read_bytes()
    found = hooks()
    for jp, en in found.items():
        assert jp.encode('cp932') + b'\0' in original, jp
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
    print('PASS: %d shot-down quotes hooked exactly.' % len(found))
