"""Offline AI-only MQM packets, challenge templates and validated reports.

No model calls, translation writes, compatibility sync, builds or installs.
Every output command is dry-run unless --write is supplied; outputs must be
new directories inside work/. Review schemas and prompts: docs/AI_PROOFREADING.md.
"""
import argparse
from collections import Counter, OrderedDict
import fnmatch
import hashlib
import json
from pathlib import Path
import re

import localization as L
import proofread_stage as P
import terms

ROOT = Path(__file__).resolve().parents[1]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(L.dump(value).encode('utf-8')).hexdigest()


def read(path):
    # Duplicate keys otherwise silently discard findings or verdicts.
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique)


def source_chars(row):
    if row['source_status'] != 'available' or not row['source']:
        return 0
    text = row['source']
    for token in sorted(set(row['tokens']), key=len, reverse=True):
        text = text.replace(token, '')
    text = L.TOKEN.sub('', text).replace('《', '').replace('》', '')
    return sum(not c.isspace() for c in text)


def output(root, out, files, write=False):
    out = Path(out).resolve()
    require((Path(root).resolve() / 'work') in out.parents and not out.exists(),
            'Use a NEW directory below work/ (never overwrite an existing run)')
    print('%s: %d new files -> %s' % ('WRITE' if write else 'DRY RUN', len(files), out))
    for name, data in list(files.items())[:8]:
        print('  %s (%d UTF-8 bytes)' % (name, len(data.encode('utf-8'))))
    if not write:
        print('Nothing written. Inspect the preview, then repeat with --write.')
        return
    # Validate every destination before writing anything.
    paths = {name: L.safe_path(out, name) for name in files}
    out.mkdir(parents=True)
    for name, data in files.items():
        path = paths[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(data)


def prepare(root, patterns, label):
    root = Path(root)
    catalog = L.Catalog(root)
    groups = []
    for pattern in patterns:
        hits = sorted(g for g in catalog.manifest['groups'] if fnmatch.fnmatchcase(g, pattern))
        require(hits, 'No catalog groups match: ' + pattern)
        groups.extend(g for g in hits if g not in groups)
    pinned = {}

    def pin(relative):
        text = (root / relative).read_text(encoding='utf-8')
        pinned[relative] = text
        return text

    profile = json.loads(pin('localization/qa/mqm_profile.json'))
    for name in ('BASE_RULES.md', 'localization/README.md', 'docs/AI_PROOFREADING.md',
                 'tools/mqm.py', 'tools/proofread_stage.py', 'tools/terms.py',
                 'tools/localization.py', 'localization/manifest.json',
                 'platforms/ps3/localization/legacy.json',
                 'localization/messages/glossary.json', 'localization/locales/en/glossary.json'):
        pin(name)
    # Render the glossary from canonical entries, NEVER from a stale mirror.
    glossary = catalog.legacy('analysis/glossary.json')
    index = terms.index(glossary)
    rows, scenes = OrderedDict(), OrderedDict()
    for group in groups:
        definitions = json.loads(pin('localization/messages/' + group + '.json'))['messages']
        locale = json.loads(pin('localization/locales/en/' + group + '.json'))['messages']
        require(not (locale.keys() - definitions.keys()), 'Unknown locale IDs in ' + group)
        for mid, definition in definitions.items():
            entry = locale.get(mid, {})
            text = entry.get('text')
            require(text is None or isinstance(text, str), 'Invalid text: ' + mid)
            require(definition.get('source') is None or isinstance(definition['source'], str),
                    'Invalid source: ' + mid)
            structural = []
            try:
                catalog.text(mid)
            except ValueError as error:
                structural.append(str(error))
            try:
                expanded = terms.expand(text, index, mid)
                if terms.stray(text):
                    structural.append('Unparsed glossary token')
            except SystemExit as error:
                expanded = None
                structural.append(str(error))
            context = definition.get('context', {})
            scene_key = (group, str(context.get('event', 'group')))
            if scene_key not in scenes:
                scenes[scene_key] = dict(id='scene-%04d' % (len(scenes) + 1), rows=[])
            row = dict(id=mid, group=group, kind=definition['kind'], context=context,
                       source=definition.get('source'), source_status=definition.get('source_status'),
                       target=text, expanded_target=expanded, status=entry.get('status', 'missing'),
                       tokens=definition.get('tokens', []), links=definition.get('links', 0),
                       structural_findings=structural, scene=scenes[scene_key]['id'])
            row['source_characters'] = source_chars(row)
            row['hints_not_errors'] = P.flags_for({'jp': row['source'], 'en': text}, {})
            rows[mid] = row
            scenes[scene_key]['rows'].append(mid)

    # Use explicit event/n order for dialogue, not hash or alphabetical ID order.
    for scene in scenes.values():
        scene['rows'].sort(key=lambda mid: rows[mid]['context'].get('n', 0))
    batches = []
    for group in groups:
        ordered = [mid for (g, _), scene in scenes.items() if g == group for mid in scene['rows']]
        for start in range(0, len(ordered), profile['batch_rows']):
            assigned = ordered[start:start + profile['batch_rows']]
            batches.append(dict(id='batch-%04d' % (len(batches) + 1), group=group,
                                assigned_ids=assigned,
                                scene_ids=list(dict.fromkeys(rows[mid]['scene'] for mid in assigned))))

    # Inputs are hashed in the snapshot. Guard against changes during capture.
    for relative, text in pinned.items():
        require((root / relative).read_text(encoding='utf-8') == text,
                'Input changed during capture: ' + relative)
    concordance = OrderedDict()
    for row in rows.values():
        for term in sorted(set(P.TERMLIKE.findall(P.body(row['source'] or '')))):
            concordance.setdefault(term, []).append(row['id'])
    concordance = {term: ids for term, ids in concordance.items() if len(ids) > 1}
    snap = dict(schema=1, label=label, language='en', profile=profile,
                scope='Selected canonical catalog groups; NOT proof of shipped PS3/Vita content',
                selection='Explicit group selection; no statistical whole-game inference',
                groups=groups, rows=rows, batches=batches, scenes=list(scenes.values()),
                glossary=glossary, concordance=concordance,
                inputs={name: hashlib.sha256(text.encode('utf-8')).hexdigest()
                        for name, text in pinned.items()})
    snap['snapshot_id'] = digest(snap)
    files = {'snapshot.json': L.dump(snap)}
    for name, text in pinned.items():
        files['inputs/' + name] = text
    files['glossary-do-not-touch.json'] = L.dump(glossary)
    files['concordance.json'] = L.dump(concordance)
    for scene in scenes.values():
        files['scenes/' + scene['id'] + '.json'] = L.dump([rows[mid] for mid in scene['rows']])
    for batch in batches:
        template = dict(schema=1, snapshot_id=snap['snapshot_id'], batch_id=batch['id'],
                        reviewer=dict(session='', model=''), examined_ids=[], assessed_ids=[],
                        uncertainties=[], findings=[])
        files['batches/' + batch['id'] + '.json'] = L.dump(batch)
        files['templates/' + batch['id'] + '.review.json'] = L.dump(template)
    files['START-HERE.md'] = (
        '# AI-assessed MQM review packet\n\n'
        'Read inputs/BASE_RULES.md and inputs/docs/AI_PROOFREADING.md completely.\n'
        'Review batches/ in order; full context is in scenes/. Use concordance.json\n'
        'to compare recurring terms. glossary-do-not-touch.json pins spellings.\n'
        'Copy a templates/*.review.json into a separate responses directory.\n'
        'Do not edit this packet, canonical translations, or generated mirrors.\n'
        'Empty templates are NOT completed reviews. No AI has assessed these rows yet.\n'
        'Runtime substitutions stay symbolic; expanded_target is not a width proof.\n'
        'Near/voice lookups: optional proofread_stage companion, see the guide.\n')
    print('Scope: %s; %d groups, %d rows, %d batches, %d source characters' %
          (label, len(groups), len(rows), len(batches), sum(r['source_characters'] for r in rows.values())))
    print('Sample:', L.dump(list(rows.values())[:1])[:2200])
    return files


def snapshot(path):
    snap = read(path)
    saved = snap.pop('snapshot_id')
    require(digest(snap) == saved, 'Snapshot modified; start a new run')
    snap['snapshot_id'] = saved
    require(snap['schema'] == 1 and snap['profile']['id'] == 'srw-z3-ai-mqm-v1', 'Unsupported snapshot')
    # Context, rules and glossary files must match the pinned snapshot too.
    folder = Path(path).parent
    for relative, wanted in snap['inputs'].items():
        text = L.safe_path(folder / 'inputs', relative).read_text(encoding='utf-8')
        require(hashlib.sha256(text.encode('utf-8')).hexdigest() == wanted,
                'Pinned input modified: ' + relative)
    require(read(folder / 'glossary-do-not-touch.json') == snap['glossary'], 'Glossary modified')
    require(read(folder / 'concordance.json') == snap['concordance'], 'Concordance modified')
    for scene in snap['scenes']:
        require(read(folder / 'scenes' / (scene['id'] + '.json')) ==
                [snap['rows'][mid] for mid in scene['rows']], 'Scene modified: ' + scene['id'])
    for batch in snap['batches']:
        require(read(folder / 'batches' / (batch['id'] + '.json')) == batch, 'Batch modified')
    return snap


def nonempty(value, label):
    require(isinstance(value, str) and value.strip(), 'Required nonempty ' + label)


def ids(value, allowed, label):
    require(isinstance(value, list) and all(isinstance(v, str) for v in value), 'Invalid ' + label)
    require(len(value) == len(set(value)), 'Duplicate ' + label)
    require(set(value) <= set(allowed), 'Out-of-scope ' + label)
    return set(value)


def actor(value):
    require(isinstance(value, dict), 'Missing reviewer identity')
    for key in ('session', 'model'):
        nonempty(value.get(key), 'reviewer.' + key)


def validate_review(snap, review):
    require(review.get('schema') == 1 and review.get('snapshot_id') == snap['snapshot_id'], 'Stale review')
    batches = {b['id']: b for b in snap['batches']}
    require(review.get('batch_id') in batches, 'Unknown batch')
    actor(review.get('reviewer'))
    batch = batches[review['batch_id']]
    examined = ids(review.get('examined_ids'), snap['rows'], 'examined_ids')
    assessed = ids(review.get('assessed_ids'), batch['assigned_ids'], 'assessed_ids')
    require(assessed <= examined, 'Assessed rows must have been examined')
    require(assessed, 'An empty template is not a review')
    require(isinstance(review.get('uncertainties'), list), 'Missing uncertainties list')
    for item in review['uncertainties']:
        require(item.get('message_id') in assessed, 'Uncertainty outside assessed rows')
        nonempty(item.get('reason'), 'uncertainty reason')
    require(isinstance(review.get('findings'), list), 'Missing findings list')
    found = set()
    for finding in review['findings']:
        fid = finding.get('id')
        require(isinstance(fid, str) and re.fullmatch(r'F[0-9]{3,}', fid), 'Finding ID must be F001 etc.')
        require(fid not in found, 'Duplicate finding ID')
        found.add(fid)
        mid = finding.get('message_id')
        require(mid in assessed, 'Finding outside assessed rows')
        row = snap['rows'][mid]
        category = finding.get('category')
        require(category in snap['profile']['linguistic_categories'] + snap['profile']['separate_categories'],
                'Unknown MQM category')
        require(finding.get('severity') in snap['profile']['severity_weights'], 'Unknown severity')
        require(finding.get('confidence') in ('low', 'medium', 'high'), 'Unknown confidence')
        for key in ('explanation', 'suggestion'):
            nonempty(finding.get(key), key)
        # Empty quotes are legitimate for omissions/missing translations, but
        # source-dependent verdicts always require actual source evidence.
        for key, text in (('source_quote', row['source']), ('target_quote', row['target'])):
            quote = finding.get(key)
            require(isinstance(quote, str) and (not quote or quote in (text or '')),
                    'Quote is not in frozen text: ' + key)
        if category in ('accuracy', 'terminology', 'context'):
            require(row['source_status'] == 'available' and finding['source_quote'],
                    'Source-dependent finding needs an available source quote')
        if category == 'design_markup':
            nonempty(finding.get('evidence'), 'layout/check evidence and platform')
        ids(finding.get('context_ids'), examined, 'context_ids')
    return batch


def challenge_template(snap, review):
    validate_review(snap, review)
    return dict(schema=1, snapshot_id=snap['snapshot_id'], batch_id=review['batch_id'],
                review_sha256=digest(review), reviewer=dict(session='', model=''),
                examined_ids=[], assessed_ids=[], uncertainties=[],
                decisions=[dict(finding_id=f['id'], verdict='uncertain', reason='', duplicate_of=None)
                           for f in review['findings']])


def validate_challenge(snap, review, challenge):
    require(challenge.get('schema') == 1 and challenge.get('snapshot_id') == snap['snapshot_id'] and
            challenge.get('batch_id') == review['batch_id'] and
            challenge.get('review_sha256') == digest(review), 'Stale or mismatched challenge')
    actor(challenge.get('reviewer'))
    require(challenge['reviewer']['session'] != review['reviewer']['session'],
            'Use a fresh challenge session, not the first reviewer session')
    examined = ids(challenge.get('examined_ids'), snap['rows'], 'challenge examined_ids')
    assessed = ids(challenge.get('assessed_ids'), review['assessed_ids'], 'challenge assessed_ids')
    require(assessed and assessed <= examined, 'Challenge must examine its assessed rows')
    require(isinstance(challenge.get('uncertainties'), list), 'Missing challenge uncertainties')
    for item in challenge['uncertainties']:
        require(item.get('message_id') in assessed, 'Challenge uncertainty outside assessed rows')
        nonempty(item.get('reason'), 'challenge uncertainty reason')
    findings = {f['id']: f for f in review['findings']}
    require(isinstance(challenge.get('decisions'), list), 'Missing decisions')
    decisions = {}
    for decision in challenge['decisions']:
        fid = decision.get('finding_id')
        require(fid in findings and fid not in decisions, 'Unknown or duplicate decision')
        require(findings[fid]['message_id'] in assessed, 'Decision outside challenge coverage')
        require(decision.get('verdict') in ('accept', 'reject', 'uncertain', 'duplicate'), 'Unknown verdict')
        nonempty(decision.get('reason'), 'decision reason')
        decisions[fid] = decision
    # Partial challenges may omit decisions; omitted findings remain pending.
    for fid, decision in decisions.items():
        if decision['verdict'] == 'duplicate':
            other = decision.get('duplicate_of')
            require(other != fid and other in decisions and decisions[other]['verdict'] == 'accept',
                    'Duplicate must point to an accepted finding in the same batch')
            require(all(findings[fid][key] == findings[other][key] for key in ('message_id', 'category')),
                    'Duplicate must describe the same message/category')
        else:
            require(decision.get('duplicate_of') is None, 'Only duplicates have duplicate_of')
    return assessed, decisions


def report(snap, reviews, challenges):
    by_batch, challenge_by_batch = {}, {}
    for review in reviews:
        validate_review(snap, review)
        require(review['batch_id'] not in by_batch, 'Duplicate batch review; resolve revisions first')
        by_batch[review['batch_id']] = review
    for challenge in challenges:
        bid = challenge.get('batch_id')
        require(bid in by_batch and bid not in challenge_by_batch, 'Unknown or duplicate challenge batch')
        challenge_by_batch[bid] = challenge
    assessed, checked = set(), set()
    accepted, pending, rejected, duplicates, uncertainties = [], [], [], [], []
    coverage = []
    for bid, review in by_batch.items():
        assessed.update(review['assessed_ids'])
        uncertainties.extend(dict(batch_id=bid, pass_name='review', **u) for u in review['uncertainties'])
        second, decisions = set(), {}
        if bid in challenge_by_batch:
            challenge = challenge_by_batch[bid]
            second, decisions = validate_challenge(snap, review, challenge)
            checked.update(second)
            uncertainties.extend(dict(batch_id=bid, pass_name='challenge', **u) for u in challenge['uncertainties'])
        coverage.append(dict(batch_id=bid, assigned=len(next(b for b in snap['batches'] if b['id'] == bid)['assigned_ids']),
                             examined=len(review['examined_ids']), assessed=len(review['assessed_ids']),
                             challenged=len(second)))
        for finding in review['findings']:
            d = decisions.get(finding['id'], dict(verdict='pending'))
            item = dict(batch_id=bid, finding=finding, decision=d)
            {'accept': accepted, 'reject': rejected, 'duplicate': duplicates,
             'uncertain': pending, 'pending': pending}[d['verdict']].append(item)
    eligible = {mid for mid in checked if snap['rows'][mid]['source_characters'] > 0}
    denom = sum(snap['rows'][mid]['source_characters'] for mid in eligible)
    weights = snap['profile']['severity_weights']
    scored = [item for item in accepted if item['finding']['message_id'] in eligible and
              item['finding']['category'] in snap['profile']['linguistic_categories']]
    points = sum(weights[item['finding']['severity']] for item in scored)
    severe = sum(item['finding']['severity'] == 'critical' for item in accepted)
    complete = checked == set(snap['rows'])
    result = dict(label=snap['profile']['label'], snapshot_id=snap['snapshot_id'], build_label=snap['label'],
                  scope=snap['scope'], selection=snap['selection'],
                  status='provisional: unresolved findings' if pending or uncertainties else
                         ('review complete; not human-validated' if complete else 'partial review'),
                  selected_rows=len(snap['rows']), first_pass_rows=len(assessed), challenged_rows=len(checked),
                  score_eligible_rows=len(eligible), excluded_rows_without_countable_source=len(checked - eligible),
                  selected_source_characters=sum(r['source_characters'] for r in snap['rows'].values()),
                  reviewed_source_characters=denom, weighted_linguistic_penalty=points,
                  penalty_per_1000_source_characters=round(points * 1000 / denom, 4) if denom else None,
                  denominator=snap['profile']['denominator'], release_blocking_accepted_criticals=severe,
                  pass_fail='NOT ASSIGNED: no calibrated threshold; no runtime validation',
                  provenance=[dict(batch_id=bid, review_sha256=digest(r), reviewer=r['reviewer'],
                                   challenge_sha256=digest(challenge_by_batch[bid]) if bid in challenge_by_batch else None,
                                   challenger=challenge_by_batch[bid]['reviewer'] if bid in challenge_by_batch else None)
                              for bid, r in by_batch.items()],
                  penalties_by_category=dict(Counter({cat: sum(weights[i['finding']['severity']] for i in scored
                      if i['finding']['category'] == cat) for cat in snap['profile']['linguistic_categories']})),
                  batch_coverage=coverage, accepted=accepted, pending_or_uncertain=pending,
                  rejected=rejected, duplicates=duplicates, uncertainties=uncertainties,
                  separate_or_source_unavailable=[i for i in accepted if i not in scored],
                  structural_hints=[dict(message_id=mid, issues=r['structural_findings'])
                                    for mid, r in snap['rows'].items() if r['structural_findings']],
                  ps3_runtime='not assessed', vita_runtime='not assessed')
    summary = ('# AI-assessed MQM — provisional evidence, not certification\n\n'
               'Build label: {build_label}\n\nStatus: {status}\n\n'
               'Selected: {selected_rows} rows; first pass: {first_pass_rows}; '
               'second pass: {challenged_rows}; score-eligible: {score_eligible_rows}.\n\n'
               'Weighted linguistic penalties: {weighted_linguistic_penalty} over '
               '{reviewed_source_characters} source characters.\n\n'
               'Penalties / 1,000 source characters (lower is better): '
               '{penalty_per_1000_source_characters}\n\n'
               'No universal passing grade or whole-game extrapolation. Missing-source and '
               'design/markup findings are separate. Structural hints are not scored findings. '
               'Read report.json for uncertainty, exclusions and row coverage. '
               'Neither platform has been visually validated by this report.\n').format(**result)
    fixes = dict(snapshot_id=snap['snapshot_id'], automatic_application=False,
                 order=['adjudicated meaning fixes by stable ID',
                        'corpus-wide glossary-name script preview, then approved name fixes',
                        'update protected name list; technical checks; fresh review'],
                 meaning=[i for i in accepted if i['finding']['category'] not in ('terminology', 'design_markup')
                          and i['finding']['severity'] != 'neutral'],
                 terminology_requiring_corpus_scan=[i for i in accepted if i['finding']['category'] == 'terminology'
                                                    and i['finding']['severity'] != 'neutral'],
                 design_markup=[i for i in accepted if i['finding']['category'] == 'design_markup'
                                and i['finding']['severity'] != 'neutral'])
    print(summary)
    files = {'report.json': L.dump(result), 'REPORT.md': summary, 'fix-plan.json': L.dump(fixes)}
    for bid, review in by_batch.items():
        files['evidence/' + bid + '.review.json'] = L.dump(review)
        if bid in challenge_by_batch:
            files['evidence/' + bid + '.challenge.json'] = L.dump(challenge_by_batch[bid])
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('--group', action='append', required=True, help='Catalog group or quoted glob; repeatable')
    prep.add_argument('--label', required=True, help='Honest content/build label, not an implied platform release')
    challenge = sub.add_parser('challenge')
    challenge.add_argument('--snapshot', type=Path, required=True)
    challenge.add_argument('--review', type=Path, required=True)
    scoring = sub.add_parser('report')
    scoring.add_argument('--snapshot', type=Path, required=True)
    scoring.add_argument('--review', type=Path, action='append', default=[])
    scoring.add_argument('--challenge', type=Path, action='append', default=[])
    for command in (prep, challenge, scoring):
        command.add_argument('--out', type=Path, required=True)
        command.add_argument('--write', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'prepare':
            files = prepare(ROOT, args.group, args.label)
        else:
            snap = snapshot(args.snapshot)
            if args.command == 'challenge':
                review = read(args.review)
                files = {'challenge.template.json': L.dump(challenge_template(snap, review)),
                         'review.json': L.dump(review)}
            else:
                files = report(snap, [read(p) for p in args.review], [read(p) for p in args.challenge])
        output(ROOT, args.out, files, args.write)
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, 'MQM stopped: %s\n' % error)


if __name__ == '__main__':
    raise SystemExit(main())
