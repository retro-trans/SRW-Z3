"""Four missed chapter narration pages: exact draw hooks, no record edits.

Unlike the opening crawl's 84-byte records, these resources have other
strides and metadata. Never feed them to narration.apply(). English lives
in the shared catalog; full keys and translations are stored by name_hook.
"""
import hashlib
from pathlib import Path
import localization
from cpk import CPK
from intermission_layout import ink

GROUP = 'chapter_narration'
# Native member 7 resources, not episode numbers. Entire-resource guards also
# preserve timings, row positions, page breaks and animation metadata.
SOURCES = {
    'STG0026': ('94cba43c0ce38ab8c74122fc360cb223a7655e45b94297941bda4a63525116b6', (0x114, 0x154, 0x194)),
    'STG0052': ('628eec4d2c401e9c632a260d820cd33d8dec4cd267cc7aed0102638542d96418', (0x114, 0x154, 0x194)),
    'STG0083': ('147e5489f53ad69b4b6585a6f534dbe1662d495f76ffffa93ff3c7a6235aa3c0', (0x12c, 0x172, 0x1b8)),
    'STG0098A': ('19dc1b58e3bab5855ef3c85c59d7edefc5426074ad30c311c2dae7d1f4e15b5f', (0x10c, 0x14a, 0x188, 0x1c6)),
}


def rows():
    cat = localization.english()
    defs = cat.document('localization/messages/' + GROUP + '.json')['messages']
    return [(d['context'], d['source'], cat.text(mid)) for mid, d in defs.items()]


def hooks():
    result = {}
    for _, jp, en in rows():
        assert jp not in result and en and '\n' not in en and '\r' not in en, jp
        result[jp] = en
    return result


def check_source():
    records = rows()
    assert {c['stage'] for c, _, _ in records} == SOURCES.keys()
    for stage, (digest, offsets) in SOURCES.items():
        k = CPK(str(Path('work/stage_dec') / (stage + '.cpk')))
        raw = k.read(next(f for f in k.files if f['id'] == 7))
        assert hashlib.sha256(raw).hexdigest() == digest, stage
        selected = [(c, jp) for c, jp, _ in records if c['stage'] == stage]
        assert tuple(c['offset'] for c, _ in selected) == offsets, stage
        for c, jp in selected:
            key = jp.encode('cp932') + b'\0'
            off = c['offset']
            assert c['member'] == 7 and raw[off:off + len(key)] == key, (stage, off)


def check_hooks(entries, mapping, widths):
    import eboot
    for jp, en in hooks().items():
        assert all(c in mapping for c in en), en
        # Full screen narration at 32px; conservative 1000px ink budget.
        assert ink(en, mapping, widths, 32) <= 1000, en
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
    print('PASS: all 13 chapter narration rows, four pages, exact hooks and font widths.')
