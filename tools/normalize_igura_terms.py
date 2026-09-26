"""Reviewed spelling migration: preview by default, --write applies the bulk rewrite.

Only canonical English values/token metadata and the glossary binding change.
Compatibility views are regenerated separately through localization.py.
"""
import argparse
import json
from pathlib import Path
import re
import localization

ROOT = Path(__file__).resolve().parents[1]
RX = re.compile(r'\b(?:(Rare|Rea) )?(Iglar|Igler|Igura)(s?)\b')
TERMS = [('rare_igura', 'レア・イグラー', 'Rare Igura'),
         ('igura', 'イグラー', 'Igura')]


def normalized(text):
    def replace(m):
        jp = 'レア・イグラー' if m[1] else 'イグラー'
        return '$$' + jp + '$$' + m[3]
    return RX.sub(replace, text)


def plan():
    changed = {}
    reviewed = []
    def load(relative):
        return json.loads((ROOT / relative).read_text(encoding='utf-8'))
    for path in sorted((ROOT / 'localization/locales/en').glob('*.json')):
        # The title is already correctly spelled and its TSV adapter is literal.
        if path.stem in ('glossary', 'scenario_titles'):
            continue
        doc = load(path)
        defs_path = Path('localization/messages') / path.name
        defs = load(defs_path)
        affected = False
        for mid, row in doc['messages'].items():
            old = row.get('text')
            if not old or not RX.search(old):
                continue
            new = normalized(old)
            if mid == 'stage0046a_03:r_09d0fcc600cdd3df':
                new = new.replace('The strongest $$レア・イグラー$$...', 'The strongest $$レア・イグラー$$s...')
            if mid == 'stage0083_04:r_9293c52555ba1457':
                new = new.replace("there's a rare few", 'there are a rare few').replace(
                    'that is the $$レア・イグラー$$.', 'those are the $$レア・イグラー$$s.')
            if mid in ('stage0085a_03:r_4740e748fae085ee', 'stage0089a_03:r_2acc8ade0cc6dfa2'):
                new = new.replace('about being $$レア・イグラー$$s', 'about $$レア・イグラー$$s')
            if mid in ('stage0037_03:r_9796b3efa401a303', 'stage0044a_03:r_00c55e25f87b71d0'):
                new = new.replace('So profound, $$レア・イグラー$$!', 'So profound, $$レア・イグラー$$s!')
            # User's reported collective address; preserve both scene copies.
            if old == '$$ジン$$\n（Makes no sense, Rare Iglar!）':
                new = '$$ジン$$\n（Makes no sense, $$レア・イグラー$$s!）'
            if old == new:
                continue
            row['text'] = new
            row['status'] = 'translated'
            defs['messages'][mid]['tokens'] = localization.TOKEN.findall(new)
            reviewed.append((mid, old, new))
            affected = True
        if affected:
            changed[path] = doc
            changed[ROOT / defs_path] = defs
    defs_path = ROOT / 'localization/messages/glossary.json'
    en_path = ROOT / 'localization/locales/en/glossary.json'
    defs, en = load(defs_path), load(en_path)
    legacy_path = ROOT / 'platforms/ps3/localization/legacy.json'
    legacy = load(legacy_path)
    bindings = legacy['documents']['analysis/glossary.json']['template']['terms']
    for key, jp, text in TERMS:
        mid = 'glossary:' + key
        if mid in defs['messages']:
            assert defs['messages'][mid]['source'] == jp
            assert en['messages'][mid]['text'] == text
            continue
        assert not any(t['jp'] == jp for t in bindings), jp
        defs['messages'][mid] = dict(source=jp, kind='glossary',
            context={'kind': 'keyword'}, source_status='available', tokens=[], links=0, link_closes=0)
        en['messages'][mid] = dict(text=text, status='translated')
        bindings.append(dict(jp=jp, en={'$message': mid}, kind='keyword',
            source='Aquarion EVOL', zukan_id=None, field='', status='confirmed',
            note='User-approved Igura spelling, 2026-09-25. Singular here; plural s stays outside the token.',
            src='User screenshot correction; scenario_titles:r_d029fa3a95e174a1 and stage0037_03'))
        changed[defs_path], changed[en_path], changed[legacy_path] = defs, en, legacy
    return changed, reviewed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    changes, rows = plan()
    print('%d canonical entries in %d files; %d documents including definitions/bindings.' %
          (len(rows), len({mid.split(':')[0] for mid, _, _ in rows}), len(changes)))
    for mid, old, new in rows[:4]:
        print(mid, '\n BEFORE:', old, '\n AFTER: ', new)
    for mid, old, new in rows:
        if 'Makes no sense' in old:
            print('SCREENSHOT:', mid, new)
    if not args.write:
        print('DRY RUN: no files changed.')
        return
    for path, doc in changes.items():
        path.write_text(localization.dump(doc), encoding='utf-8')
    print('Applied canonical bulk spelling/token migration. Run localization sync separately.')


if __name__ == '__main__':
    main()
