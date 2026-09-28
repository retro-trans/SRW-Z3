"""User-approved names, their biography, and ordinary-word exclusions."""
import json
from pathlib import Path
import unittest
import localization
import terms


class RandMelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = localization.english()
        cls.idx = terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8')))

    def test_glossary_resolves_user_spellings(self):
        self.assertEqual(terms.expand('$$ランド$$ and $$メール$$', self.idx), 'Rand and Mel')
        self.assertEqual(terms.expand('land, mail, Land Battleship', self.idx), 'land, mail, Land Battleship')

    def test_screenshot_dialogue_and_biography(self):
        dialogue = terms.expand(self.cat.text('stage0052_03:r_702f82442fcec8a9'), self.idx)
        self.assertIn("Mel... you mean Rand's partner, Mel?", dialogue)
        bio = terms.expand(self.cat.text('library.kw_104:r_3ee26d16dc9ec419'), self.idx)
        self.assertIn('Her full name is Mel Beater.', bio)
        self.assertIn('the master of Rand Travis.', bio)
        self.assertIn('She has known Rand since', bio)
        self.assertNotIn('Land', bio)
        self.assertNotIn('Mail', bio)

    def test_source_backed_rand_references_are_tokenized(self):
        count = 0
        for p in Path('localization/locales/en').glob('stage*.json'):
            for mid, row in json.loads(p.read_text(encoding='utf-8'))['messages'].items():
                text = row.get('text') or ''
                if '$$ランド$$' in text:
                    count += 1
                    self.assertNotIn('Land', text)
                    self.assertIn('Rand', terms.expand(self.cat.text(mid), self.idx))
        self.assertEqual(count, 8)
        ordinary = self.cat.text('stage0044b_04:r_5b23687574286204')
        self.assertIn('Land on Earth', ordinary)

    def test_vietnamese_shared_token_contract(self):
        cat = localization.Catalog(language='vi')
        self.assertEqual(cat.text('glossary:rand'), 'Rand')
        count = 0
        for p in Path('localization/locales/vi').glob('stage*.json'):
            for mid, row in json.loads(p.read_text(encoding='utf-8'))['messages'].items():
                if '$$ランド$$' in (row.get('text') or ''):
                    self.assertEqual(cat.text(mid), row['text'])
                    count += 1
        self.assertEqual(count, 6)


if __name__ == '__main__':
    unittest.main()
