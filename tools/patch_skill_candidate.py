"""Isolated skill-description hook update; snapshot, dry run, then --write."""
import argparse
import json
from pathlib import Path
import eboot
import trdata
from patch_parts_candidate import patch


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--snapshot',action='store_true')
    ap.add_argument('--write',action='store_true')
    args = ap.parse_args()
    baseline = Path('work/skill_hooks_before.json')
    trdata.use_glossary('analysis/glossary.json')
    after = eboot.load_ui_hook()
    if args.snapshot:
        assert not args.write and not baseline.exists()
        baseline.write_bytes(json.dumps(after,ensure_ascii=False).encode('utf-8'))
        print('Saved effective pre-edit skill hook baseline.')
        return
    before = json.loads(baseline.read_text(encoding='utf-8'))
    rows = json.loads(Path('translation/skill_hook.json').read_text(encoding='utf-8'))['lines']
    keys = {r['jp'] for r in rows}
    fragments = {line.strip('　 ') for r in rows for line in r['jp'].split('\n')}
    assert {jp for jp in after if before.get(jp) != after[jp]} <= keys
    assert set(before)-set(after) <= fragments
    out = Path('work/out_0.6.3')
    path = out/'EBOOT.BIN'
    old = path.read_bytes()
    mapping = json.loads((out/'pairs.json').read_text())
    data,stats = patch(old,mapping,before,after)
    print('Skill delta: %d replacements, %d obsolete fragments removed; %d new text bytes; %d lookup rows.'%stats)
    print('PASS: only lookup entries/new text changed; code, voice data and file size preserved.')
    if args.write:
        backup = Path('work/skill_descriptions_EBOOT.before.bin')
        assert not backup.exists()
        backup.write_bytes(old)
        path.write_bytes(data)


if __name__ == '__main__':
    main()
