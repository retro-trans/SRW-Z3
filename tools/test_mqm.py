"""Synthetic MQM provenance/coverage/scoring tests; no translation changes."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

import mqm as M


class MQMTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in ('BASE_RULES.md', 'localization/README.md', 'docs/AI_PROOFREADING.md',
                         'tools/mqm.py', 'tools/proofread_stage.py', 'tools/terms.py',
                         'tools/localization.py', 'localization/qa/mqm_profile.json'):
            self.put(relative, (M.ROOT / relative).read_text(encoding='utf-8'))
        self.put('localization/manifest.json', dict(schema=1, groups=['stage0001a', 'glossary'], languages=['en']))
        self.put('platforms/ps3/localization/legacy.json', dict(documents={
            'analysis/glossary.json': dict(template=dict(terms=[
                dict(jp='名前', en={'$message': 'glossary:name'}, kind='pilot')]))}))
        self.put('localization/messages/glossary.json', dict(messages={
            'glossary:name': dict(source='名前', source_status='available', kind='glossary', tokens=[], links=0)}))
        self.put('localization/locales/en/glossary.json', dict(messages={
            'glossary:name': dict(text='Name', status='translated')}))
        # Deliberately reverse insertion order; event/n establishes dialogue order.
        definitions = {('stage0001a:%03d' % n): dict(source='名前\n「はい」', source_status='available',
                        kind='dialogue', context=dict(event='event1', n=n), tokens=['$$名前$$'], links=0)
                       for n in reversed(range(83))}
        locale = {mid: dict(text='$$名前$$\n「Yes.」', status='translated') for mid in definitions}
        self.put('localization/messages/stage0001a.json', dict(messages=definitions))
        self.put('localization/locales/en/stage0001a.json', dict(messages=locale))
        with contextlib.redirect_stdout(io.StringIO()):
            self.files = M.prepare(self.root, ['stage0001*'], 'synthetic test')
        self.snap = json.loads(self.files['snapshot.json'])
        self.mid = 'stage0001a:000'

    def put(self, relative, value):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value if isinstance(value, str) else M.L.dump(value), encoding='utf-8')

    def review(self):
        return dict(schema=1, snapshot_id=self.snap['snapshot_id'], batch_id='batch-0001',
                    reviewer=dict(session='review-session', model='synthetic'),
                    examined_ids=[self.mid, 'stage0001a:001'], assessed_ids=[self.mid],
                    uncertainties=[], findings=[])

    def finding(self, fid='F001', category='accuracy', severity='major'):
        return dict(id=fid, message_id=self.mid, category=category, severity=severity,
                    confidence='high', source_quote='はい', target_quote='Yes.',
                    context_ids=['stage0001a:001'], explanation='Synthetic validation evidence.',
                    suggestion='Synthetic suggestion, never applied.', evidence='Synthetic PS3 width result')

    def challenge(self, review):
        value = M.challenge_template(self.snap, review)
        value.update(reviewer=dict(session='challenge-session', model='synthetic'),
                     examined_ids=review['examined_ids'], assessed_ids=review['assessed_ids'])
        for decision in value['decisions']:
            decision.update(verdict='accept', reason='Synthetic adjudication.')
        return value

    def result(self, reviews=(), challenges=()):
        with contextlib.redirect_stdout(io.StringIO()):
            return json.loads(M.report(self.snap, list(reviews), list(challenges))['report.json'])

    def test_prepare_canonical_expansion_batches_order(self):
        self.assertEqual([len(b['assigned_ids']) for b in self.snap['batches']], [80, 3])
        self.assertEqual(self.snap['batches'][0]['assigned_ids'][0], self.mid)
        self.assertEqual(self.snap['rows'][self.mid]['expanded_target'], 'Name\n「Yes.」')
        self.assertEqual(self.snap['rows'][self.mid]['source_characters'], 6)
        self.assertNotIn('translation/', ''.join(p.name for p in self.root.iterdir()))

    def test_dry_run_new_path_no_files_then_roundtrip(self):
        out = self.root / 'work/run'
        with contextlib.redirect_stdout(io.StringIO()):
            M.output(self.root, out, self.files)
        self.assertFalse(out.exists())
        with contextlib.redirect_stdout(io.StringIO()):
            M.output(self.root, out, self.files, True)
        self.assertEqual(M.snapshot(out / 'snapshot.json'), self.snap)
        with self.assertRaisesRegex(ValueError, 'NEW'):
            M.output(self.root, out, self.files, True)
        with self.assertRaisesRegex(ValueError, 'NEW'):
            M.output(self.root, self.root / 'outside', self.files, True)

    def test_modified_snapshot_and_scene_rejected(self):
        out = self.root / 'work/run'
        with contextlib.redirect_stdout(io.StringIO()):
            M.output(self.root, out, self.files, True)
        (out / 'scenes/scene-0001.json').write_text('[]', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Scene modified'):
            M.snapshot(out / 'snapshot.json')
        data = copy.deepcopy(self.snap)
        data['label'] = 'changed'
        (out / 'snapshot.json').write_text(M.L.dump(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Snapshot modified'):
            M.snapshot(out / 'snapshot.json')

    def test_empty_reports_are_not_perfect_scores(self):
        result = self.result()
        self.assertIsNone(result['penalty_per_1000_source_characters'])
        self.assertEqual(result['challenged_rows'], 0)
        self.assertEqual(result['status'], 'partial review')
        review = self.review()
        review['assessed_ids'] = []
        with self.assertRaisesRegex(ValueError, 'empty template'):
            M.validate_review(self.snap, review)

    def test_coverage_and_penalty_only_second_pass_rows(self):
        review = self.review()
        review['findings'] = [self.finding()]
        result = self.result([review])
        self.assertEqual(len(result['pending_or_uncertain']), 1)
        self.assertIsNone(result['penalty_per_1000_source_characters'])
        result = self.result([review], [self.challenge(review)])
        self.assertEqual(result['weighted_linguistic_penalty'], 5)
        self.assertEqual(result['reviewed_source_characters'], 6)
        self.assertEqual(result['penalty_per_1000_source_characters'], 833.3333)
        self.assertEqual(result['first_pass_rows'], 1)
        self.assertEqual(result['batch_coverage'][0]['examined'], 2)
        self.assertEqual(result['status'], 'partial review')

    def test_complete_clean_coverage_still_not_human_validated(self):
        reviews, challenges = [], []
        for batch in self.snap['batches']:
            review = self.review()
            review.update(batch_id=batch['id'], assessed_ids=batch['assigned_ids'], examined_ids=batch['assigned_ids'])
            reviews.append(review)
            challenges.append(self.challenge(review))
        result = self.result(reviews, challenges)
        self.assertEqual(result['challenged_rows'], 83)
        self.assertEqual(result['status'], 'review complete; not human-validated')
        self.assertEqual(result['penalty_per_1000_source_characters'], 0)

    def test_stale_identity_scope_quote_and_context_guards(self):
        review = self.review()
        review['findings'] = [self.finding()]
        for key, value in [('snapshot_id', 'stale'), ('batch_id', 'missing'),
                           ('assessed_ids', ['stage0001a:082']), ('examined_ids', [self.mid, self.mid])]:
            invalid = copy.deepcopy(review)
            invalid[key] = value
            with self.assertRaises(ValueError):
                M.validate_review(self.snap, invalid)
        for key, value in [('source_quote', 'not there'), ('target_quote', 'No!'),
                           ('category', 'made-up'), ('severity', 'huge'), ('confidence', 'certain'),
                           ('context_ids', ['stage0001a:082'])]:
            invalid = copy.deepcopy(review)
            invalid['findings'][0][key] = value
            with self.assertRaises(ValueError):
                M.validate_review(self.snap, invalid)

    def test_fresh_challenge_hash_guard_and_duplicate_batches(self):
        review = self.review()
        challenge = self.challenge(review)
        challenge['reviewer']['session'] = review['reviewer']['session']
        with self.assertRaisesRegex(ValueError, 'fresh challenge'):
            self.result([review], [challenge])
        challenge = self.challenge(review)
        review['uncertainties'] = [dict(message_id=self.mid, reason='new uncertainty')]
        with self.assertRaisesRegex(ValueError, 'Stale'):
            self.result([review], [challenge])
        with self.assertRaisesRegex(ValueError, 'Duplicate batch'):
            self.result([review, review])

    def test_missing_source_excluded_and_no_fabricated_accuracy(self):
        self.snap['rows'][self.mid].update(source=None, source_status='not_extracted', source_characters=0)
        review = self.review()
        finding = self.finding(category='fluency')
        finding['source_quote'] = ''
        review['findings'] = [finding]
        result = self.result([review], [self.challenge(review)])
        self.assertIsNone(result['penalty_per_1000_source_characters'])
        self.assertEqual(len(result['separate_or_source_unavailable']), 1)
        finding['category'] = 'accuracy'
        with self.assertRaisesRegex(ValueError, 'Source-dependent'):
            M.validate_review(self.snap, review)

    def test_uncertainty_not_a_clean_pass(self):
        review = self.review()
        review['uncertainties'] = [dict(message_id=self.mid, reason='Ambiguous subject')]
        result = self.result([review], [self.challenge(review)])
        self.assertEqual(result['status'], 'provisional: unresolved findings')
        self.assertEqual(result['weighted_linguistic_penalty'], 0)

    def test_duplicates_count_once_and_cannot_point_to_self(self):
        review = self.review()
        review['findings'] = [self.finding('F001'), self.finding('F002')]
        challenge = self.challenge(review)
        challenge['decisions'][1].update(verdict='duplicate', duplicate_of='F001')
        result = self.result([review], [challenge])
        self.assertEqual(result['weighted_linguistic_penalty'], 5)
        self.assertEqual(len(result['duplicates']), 1)
        challenge['decisions'][1]['duplicate_of'] = 'F002'
        with self.assertRaisesRegex(ValueError, 'Duplicate must'):
            self.result([review], [challenge])

    def test_design_separate_critical_flag_and_neutral_zero(self):
        review = self.review()
        review['findings'] = [self.finding('F001', 'design_markup', 'critical'),
                              self.finding('F002', 'style', 'neutral')]
        result = self.result([review], [self.challenge(review)])
        self.assertEqual(result['weighted_linguistic_penalty'], 0)
        self.assertEqual(result['release_blocking_accepted_criticals'], 1)
        self.assertEqual(len(result['separate_or_source_unavailable']), 1)
        del review['findings'][0]['evidence']
        with self.assertRaisesRegex(ValueError, 'evidence'):
            M.validate_review(self.snap, review)

    def test_source_count_ignores_whitespace_controls_links(self):
        row = dict(source='名\n《はい》 $n %s', source_status='available', tokens=['$n', '%s'])
        self.assertEqual(M.source_chars(row), 3)

    def test_json_duplicate_keys_rejected(self):
        path = self.root / 'bad.json'
        path.write_text('{"findings": [], "findings": []}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Duplicate JSON key'):
            M.read(path)

    def test_rejected_uncertain_and_omitted_decisions_not_scored(self):
        review = self.review()
        review['findings'] = [self.finding('F001'), self.finding('F002'), self.finding('F003')]
        challenge = self.challenge(review)
        challenge['decisions'][0]['verdict'] = 'reject'
        challenge['decisions'][1]['verdict'] = 'uncertain'
        challenge['decisions'].pop()
        result = self.result([review], [challenge])
        self.assertEqual(result['weighted_linguistic_penalty'], 0)
        self.assertEqual(len(result['pending_or_uncertain']), 2)
        self.assertEqual(len(result['rejected']), 1)
        self.assertEqual(result['provenance'][0]['review_sha256'], M.digest(review))

    def test_prepare_preserves_broken_tokens_as_hints_not_score(self):
        path = self.root / 'localization/locales/en/stage0001a.json'
        data = M.read(path)
        data['messages'][self.mid]['text'] = 'No token left.'
        self.put('localization/locales/en/stage0001a.json', data)
        with contextlib.redirect_stdout(io.StringIO()):
            files = M.prepare(self.root, ['stage0001*'], 'broken token test')
        self.assertTrue(json.loads(files['snapshot.json'])['rows'][self.mid]['structural_findings'])

    def test_no_match_and_output_traversal_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'No catalog groups'):
            M.prepare(self.root, ['no-group'], 'test')
        out = self.root / 'work/new'
        with self.assertRaises(ValueError), contextlib.redirect_stdout(io.StringIO()):
            M.output(self.root, out, {'../escape.txt': 'bad'}, True)
        self.assertFalse(out.exists())

    def test_proofread_companion_uses_selected_root_and_stage1_suffix(self):
        self.put('reference/translation/stage0001a.json', dict(LINES=[
            dict(sha='one', jp='名前\n「はい」', en='Name\n「Yes.」', event='event1')]))
        self.put('reference/translation/stage0002_03.json', dict(LINES=[
            dict(sha='two', jp='名前\n「いいえ」', en='Name\n「No.」')]))
        self.put('reference/analysis/glossary.json', dict(terms=[]))
        ship = M.P.corpus('stage0001', str(self.root / 'reference'))
        self.assertEqual(set(ship), {'two'})
        result = M.P.bundle('STG0001', str(self.root / 'proof'), str(self.root / 'reference'))
        self.assertEqual(result[:2], (1, 1))


if __name__ == '__main__':
    unittest.main()
