"""Ace / Custom / Full Upgrade bonus descriptions, as exact draw-time hooks.

The executable keeps these ~240 descriptions in one table (VA 0x709668 to
0x70c4c8). None had a hook, so every bonus effect drew in Japanese, and the
Custom Bonus popup showed a Japanese effect line under an English title.

Each description is drawn as a standalone string (the "Ace Bonus" heading is a
separate, already-hooked draw), so an exact entry per description is enough.
Wording lives in the `bonus_descriptions` catalog group, keyed by EBOOT VA; the
one fragment of the table (`武器の射`, the head of a composed string) is left out.
"""
from pathlib import Path
import localization

GROUP = 'bonus_descriptions'


def hooks():
    cat = localization.english()
    defs = cat.document('localization/messages/%s.json' % GROUP)['messages']
    out = {}
    for mid, definition in defs.items():
        en = cat.text(mid)
        if en:
            out[definition['source']] = en
    return out


def check_hooks(entries, mapping):
    import eboot
    original = Path('work/EBOOT_dec.elf').read_bytes()
    found = hooks()
    for jp, en in found.items():
        assert jp.encode('cp932') + b'\0' in original, jp
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
    print('PASS: %d bonus descriptions hooked exactly.' % len(found))
