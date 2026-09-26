"""Apply only the reviewed parts-hook delta to an existing local candidate.

Dry-run first. Requires the effective pre-edit hook snapshot. Preserves the
existing executable, voice tables, and all non-parts content. No RPW writes.
"""
import argparse
import json
import struct
from pathlib import Path
import eboot
import trdata


def patch(old, mapping, before, after):
    changed = {jp: en for jp, en in after.items() if before.get(jp) != en}
    removed = set(before) - set(after)
    segs = eboot._segments(old)
    start = eboot._off(segs, eboot.NAME_TBL)
    limit = eboot._off(segs, eboot.NAME_STR)
    old_rows, seen = [], set()
    p = start
    while struct.unpack_from('>I', old, p)[0]:
        key, val = struct.unpack_from('>II', old, p)
        off = eboot._off(segs, key)
        raw = old[off:old.index(0, off)]
        old_rows.append((key, val, raw))
        p += 8
    table_end = p + 8
    out = bytearray(old)
    append_start = cursor = (len(old.rstrip(b'\0')) + 39) & ~7
    assert cursor >= limit
    pool = {}

    def append(raw):
        nonlocal cursor
        if raw in pool:
            return pool[raw]
        end = cursor + len(raw) + 1
        assert end <= len(old) and not any(old[cursor:end]), 'No safe text space'
        out[cursor:end] = raw + b'\0'
        va = eboot._va(segs, cursor)
        cursor = end
        pool[raw] = va
        return va

    delta = {jp.encode('cp932'): en for jp, en in changed.items()}
    delete = {jp.encode('cp932') for jp in removed}
    rows = []
    for key, val, raw in old_rows:
        if raw in delete:
            seen.add(raw)
            continue
        if raw in delta:
            assert not val & 0xc0000000, 'Parts must be exact matches'
            val = append(eboot._encode_marked(delta[raw], mapping))
            seen.add(raw)
        rows.append((key, val))
    missing = (set(delta) | delete) - seen
    # The baseline is the source truth: all old delta keys must be installed.
    assert not (missing & {jp.encode('cp932') for jp in before}), missing
    for raw in sorted(missing - delete):
        rows.append((append(raw), append(eboot._encode_marked(delta[raw], mapping))))
    table = b''.join(struct.pack('>II', *row) for row in rows) + bytes(8)
    assert start + len(table) <= limit
    allowed_end = max(table_end, start + len(table))
    out[start:allowed_end] = table + bytes(allowed_end - start - len(table))
    assert len(old) == len(out)
    assert old[:start] == out[:start]
    assert old[allowed_end:append_start] == out[allowed_end:append_start]
    assert old[cursor:] == out[cursor:]
    return bytes(out), (len(changed), len(removed), cursor - append_start, len(rows))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', default='work/out_0.6.3')
    ap.add_argument('--baseline', default='work/parts_hooks_before.json')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    out = Path(args.out)
    path = out / 'EBOOT.BIN'
    before = json.loads(Path(args.baseline).read_text(encoding='utf-8'))
    trdata.use_glossary('analysis/glossary.json')
    after = eboot.load_ui_hook()
    parts = json.loads(Path('translation/parts_desc_hook.json').read_text(encoding='utf-8'))['lines']
    keys = {row['jp'] for row in parts}
    fragments = {line.strip('　 ') for row in parts for line in row['jp'].split('\n')}
    assert {jp for jp in after if before.get(jp) != after[jp]} <= keys, 'Unrelated hook edits since baseline'
    assert set(before) - set(after) <= fragments, 'Unrelated removals since baseline'
    mapping = json.loads((out / 'pairs.json').read_text())
    old = path.read_bytes()
    data, stats = patch(old, mapping, before, after)
    print('Parts delta: %d replacements, %d obsolete fragments removed; %d new text bytes; %d lookup rows.' % stats)
    print('PASS: only lookup table and new text changed; code, voice tables and file size unchanged.')
    if args.write:
        backup = Path('work/parts_descriptions_EBOOT.before.bin')
        assert not backup.exists(), 'Backup already exists; verify instead of applying twice'
        backup.write_bytes(old)
        path.write_bytes(data)


if __name__ == '__main__':
    main()
