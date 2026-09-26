"""Source-backed operation-condition catalog (not a game build)."""
import re
from collections import defaultdict
from pathlib import Path
from cpk import CPK
import audit_message_classes as audit


def source_rows():
    found = {}
    for path in sorted((audit.ROOT / 'work/stage_dec').glob('STG*.cpk')):
        source = audit.preset_text(CPK(str(path)), path)
        if source is None:
            continue
        match = re.search(r'OPERATE_TBL\s*=\s*\{.*?str_tbl\s*=\s*\{(.*?)\};.*?id_tbl\s*=\s*\{(.*?)\};', source, re.S)
        if not match:
            assert '作戦目的テーブルはありません。' in source and 'OPERATE_TBL' not in source, path
            continue
        strings = [s.replace('\\n', '\n') for s in re.findall(r'"((?:\\.|[^"\\])*)"', match[1])]
        tokens = re.findall(r'true|false|-?\d+', re.sub(r'--[^\r\n]*', '', match[2]))
        assert len(tokens) % 8 == 0, path
        roles = defaultdict(set)
        for start in range(0, len(tokens), 8):
            assert tokens[start] in {'true', 'false'}, path
            for role, values in [('victory', tokens[start+1:start+4]),
                                 ('defeat', tokens[start+4:start+7]),
                                 ('sr', tokens[start+7:start+8])]:
                for value in values:
                    if int(value) >= 0:
                        roles[int(value)].add(role)
        for i, jp in enumerate(strings):
            row = found.setdefault(jp, {'jp': jp, 'roles': set(), 'sources': set()})
            row['roles'].update(roles[i])
            row['sources'].add(f'{path.name}:str_tbl[{i}]')
    return [dict(row, roles=sorted(row['roles']), sources=sorted(row['sources']))
            for _, row in sorted(found.items())]


if __name__ == '__main__':
    import argparse
    import hashlib
    import json
    import eboot
    import trdata
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    trdata.use_glossary(str(audit.ROOT / 'analysis/glossary.json'))
    hooks = eboot.load_ui_hook()
    rows = source_rows()
    missing = [dict(row, id='mission_conditions_all:r_' + hashlib.sha256(row['jp'].encode()).hexdigest()[:16])
               for row in rows if row['jp'] not in hooks]
    print(f'{len(rows)} unique source conditions; {len(missing)} untranslated complete conditions')
    print('Examples:', json.dumps(missing[:4], ensure_ascii=False))
    if args.out and not args.write:
        print('DRY RUN: pass --write to export review batches to', args.out)
    if args.out and args.write:
        args.out.mkdir(parents=True, exist_ok=False)
        (args.out / 'missing.json').write_text(json.dumps(missing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        for i in range(0, len(missing), 80):
            (args.out / f'batch_{i//80+1}.json').write_text(json.dumps(missing[i:i+80], ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
