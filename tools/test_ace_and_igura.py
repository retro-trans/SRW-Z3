"""Screenshot regressions: ace-talk coverage and glossary spelling consistency."""
import hashlib
import json
from pathlib import Path
import re
import unittest

import audit_message_classes
import check_stage
import digraph
import localization
import luarec
import normalize_igura_terms
import patch_lua
import terms
import trdata
from cpk import CPK

ROOT = Path(__file__).resolve().parents[1]


class IguraTests(unittest.TestCase):
    def test_battle_subtitles_expand_before_encoding(self):
        trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
        glossary = terms.index(json.loads((ROOT / 'analysis/glossary.json').read_text(encoding='utf-8')))
        affected = 0
        igura_affected = 0
        for path in (ROOT / 'translation').glob('voice_*.json'):
            original = json.loads(path.read_text(encoding='utf-8'))
            loaded = trdata.voice_document(str(path))
            for key, row in original['lines'].items():
                before = row['en'] if isinstance(row, dict) else row
                after_row = loaded['lines'][key]
                after = after_row['en'] if isinstance(after_row, dict) else after_row
                if '$$' in (before or ''):
                    affected += 1
                    self.assertNotIn('$$', after)
                    self.assertEqual(after, terms.expand(before, glossary))
                    if '$$イグラー$$' in before or '$$レア・イグラー$$' in before:
                        igura_affected += 1
                        self.assertIn('Igura', after)
                else:
                    self.assertEqual(before, after)
                if isinstance(row, dict):
                    self.assertEqual({k: v for k, v in row.items() if k != 'en'},
                                     {k: v for k, v in after_row.items() if k != 'en'})
            self.assertEqual({k: v for k, v in original.items() if k != 'lines'},
                             {k: v for k, v in loaded.items() if k != 'lines'})
        self.assertGreater(affected, 0)
        self.assertGreater(igura_affected, 0)

    def test_word_boundaries_and_plural_tokens(self):
        normalize = normalize_igura_terms.normalized
        self.assertEqual(normalize('Rare Iglars and Iglar'), '$$レア・イグラー$$s and $$イグラー$$')
        self.assertEqual(normalize("Rare Igler's / Rea Iglar"), "$$レア・イグラー$$'s / $$レア・イグラー$$")
        self.assertEqual(normalize('configuration'), 'configuration')

    def test_catalog_no_obsolete_spellings(self):
        for path in (ROOT / 'localization/locales/en').glob('*.json'):
            rows = json.loads(path.read_text(encoding='utf-8'))['messages']
            for mid, row in rows.items():
                self.assertNotRegex(row.get('text') or '', r'\b(?:Iglar|Igler)s?\b', mid)

    def test_reported_line_and_contextual_meaning(self):
        cat = localization.Catalog()
        for mid in ['stage0037_03:r_4b0e43ba6a5f2f5b', 'stage0044a_03:r_e51ecf6d6aa42e75']:
            self.assertEqual(cat.text(mid), '$$ジン$$\n（Makes no sense, $$レア・イグラー$$s!）')
        for mid in ['stage0085a_03:r_4740e748fae085ee', 'stage0089a_03:r_2acc8ade0cc6dfa2']:
            self.assertIn('about $$レア・イグラー$$s.', cat.text(mid))
            self.assertNotIn('about being', cat.text(mid))
        self.assertEqual(cat.text('glossary:rare_igura'), 'Rare Igura')
        self.assertEqual(cat.text('glossary:igura'), 'Igura')

    def test_all_affected_dialogue_records_fit(self):
        cat = localization.Catalog()
        glossary = cat.legacy('analysis/glossary.json')
        idx = terms.index(glossary)
        self.assertTrue(check_stage.widths_ready())
        examined = 0
        for group in cat.manifest['groups']:
            if not group.startswith('stage'):
                continue
            defs = cat.document('localization/messages/' + group + '.json')['messages']
            for mid, definition in defs.items():
                en = cat.text(mid)
                if '$$レア・イグラー$$' not in en and '$$イグラー$$' not in en:
                    continue
                jp = definition['source']
                sha = luarec.digest(jp)
                self.assertEqual(check_stage.check([dict(jp=jp, sha=sha)], {sha: en}, True, term_idx=idx), [], mid)
                examined += 1
        self.assertGreater(examined, 50)


class AceTalkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ROOT / 'work/stage_dec/STG0500.cpk'
        cls.cpk = CPK(str(cls.source))
        cls.lua = cls.cpk.read(next(f for f in cls.cpk.files if f['id'] == 1))
        cls.records = luarec.records(cls.lua.decode('cp932'))
        trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
        cls.rows = trdata.records(str(ROOT / 'translation/stage0500_01.json'))
        cls.mapping = json.loads((ROOT / 'work/build_0.6.19_english_20260924_r3/pairs.json').read_text())

    def test_complete_source_identity_and_screenshot(self):
        self.assertEqual(hashlib.sha256(self.source.read_bytes()).hexdigest(),
                         '6c4d7e6441d0f27cc9aabf73fc005158c47c3826ca4fb480fca91ceb080a668b')
        self.assertEqual(len(self.rows), 1247)
        self.assertEqual(len({r['sha'] for r in self.records}), 918)
        self.assertEqual(len(self.rows), len(self.records))
        for source, row in zip(self.records, self.rows):
            self.assertTrue(row['en'])
            for key in ('event', 'n', 'pid', 'sha'):
                self.assertEqual(source[key], row[key])
        hits = [r for r in self.rows if 'おめでとうございます、宗介様！' in r['jp']]
        self.assertEqual(len(hits), 2)  # The scene has an alternate branch.
        for hit in hits:
            self.assertIn('Congratulations, Sousuke!', hit['en'])
            self.assertIn('Happy Ace Pilot!', hit['en'])

    def test_full_dialogue_constraints(self):
        self.assertTrue(check_stage.widths_ready())
        self.assertEqual(check_stage.check(self.records, {r['sha']: r['en'] for r in self.rows}, True), [])

    def test_only_text_changes_not_scene_commands(self):
        self.assertTrue(check_stage.widths_ready())
        translated = patch_lua.patch(self.lua, self.rows, self.mapping)
        block = re.compile(rb'(?<!--)\[\[(.*?)\]\]', re.S)
        self.assertEqual(block.sub(b'[[TEXT]]', self.lua), block.sub(b'[[TEXT]]', translated))
        self.assertEqual(len(block.findall(translated)), 1247)
        self.assertIsNone(audit_message_classes.preset_text(self.cpk, self.source))

    def test_build_and_distribution_tables(self):
        from platforms.ps3.manifest import STAGES
        import deploy, extract, apply_xdelta
        entries = [r for r in STAGES if r['sdat'] == 'STG0500.SDAT']
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]['members'][0]['id'], 1)
        self.assertEqual(entries[0]['members'][0]['trans'], 'translation/stage0500_01.json')
        for table in (deploy.LAYOUT, extract.DISC, apply_xdelta.LAYOUT):
            self.assertEqual(table['STG0500.SDAT'], 'DATA/STAGE')


if __name__ == '__main__':
    unittest.main()
