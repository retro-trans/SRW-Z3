"""Source-bound single-line bonus labels eligible for live English centering.

Multiline descriptions keep their existing layout. Opt in by exact content,
not a generic draw caller: the same widget also displays unrelated messages.
Pointer keys avoid copying the description table into the small code cave.
"""
from functools import lru_cache
from pathlib import Path
import localization

LOCK = '機体改造１０段階で取得'


@lru_cache(maxsize=1)
def rows():
    cat = localization.english()
    source = Path('work/EBOOT_dec.elf').read_bytes()
    result = []
    for mid, d in cat.document('localization/messages/bonus_descriptions.json')['messages'].items():
        jp, en = d['source'], cat.text(mid)
        if '\n' in jp or '\n' in en:
            continue
        assert en and all(32 <= ord(c) < 127 for c in en), mid
        # Historical context calls these VAs, but they are file offsets.
        off = int(d['context']['eboot_va'], 16)
        raw = jp.encode('cp932') + b'\0'
        assert source[off:off + len(raw)] == raw, mid
        result.append((off + 0x10000, jp, en))
    return tuple(result)
