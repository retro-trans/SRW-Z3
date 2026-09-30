"""Exact user-requested Sphere titles; unrelated vocabulary stays intact."""
from pathlib import Path
import json
import unittest
import localization
import terms

TITLES = {
    '悲しみの乙女': 'Sorrowful Maiden',
    '傷だらけの獅子': 'Wounded Lion',
    '偽りの黒羊': 'Lying Black Sheep',
    '尽きぬ水瓶': 'Inexhaustable Water Gourd',
    'いがみ合う双子': 'Quarreling Twins',
}
OLD = ('Maiden of Sorrow', 'Scarred Lion', 'False Black Ram',
       'Deceiving Black', 'Endless Water Jar', 'Never-Emptying Water Jar',
       'Inexhaustible Water Bearer', 'Feuding Twins', 'Bickering Twins')


class SphereTitleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = localization.english()
        cls.idx = terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8')))

    def test_exact_glossary_spelling(self):
        for jp, en in TITLES.items():
            self.assertEqual(terms.expand('$$'+jp+'$$', self.idx), en)

    def test_no_old_sphere_title_variants(self):
        for p in Path('localization/locales/en').glob('*.json'):
            for mid, row in json.loads(p.read_text(encoding='utf-8')).get('messages', {}).items():
                for old in OLD:
                    self.assertNotIn(old.lower(), (row.get('text') or '').lower(), mid)

    def test_quarreling_twins_dialogue_and_scenario(self):
        for mid in ('stage0053_04:r_0c705091f748360e', 'stage0053_04:r_24e1a808a1609a1a'):
            self.assertIn('$$いがみ合う双子$$', self.cat.text(mid))
            self.assertIn('Quarreling Twins', terms.expand(self.cat.text(mid), self.idx))
        self.assertEqual(self.cat.text('scenario_titles:r_16dc368a89b428b2'), 'The Quarreling Twins')
        # An ordinary comparison in Suzune's explanation remains lowercase.
        self.assertIn('Just like quarreling twins', self.cat.text('stage0097_04:r_889b93ef12326ef0'))

    def test_screenshots_and_library_use_same_titles(self):
        kira = terms.expand(self.cat.text('stage0052_03:r_7cbc63dad295f862'), self.idx)
        kouji = terms.expand(self.cat.text('stage0052_03:r_d7f1c506e78e55ff'), self.idx)
        self.assertIn("'Sorrowful Maiden'", kira)
        self.assertIn("'Wounded Lion'", kira)
        self.assertIn("'Wavering Scales'", kira)
        self.assertIn("'Lying Black Sheep' and 'Inexhaustable Water Gourd'", kouji)
        library = self.cat.text('library.kw_104:r_b265314c2661a9a3')
        self.assertNotIn('$$ラム$$', library)  # unrelated character Ram, not this Sphere
        for name in TITLES.values():
            self.assertIn(name, terms.expand(library, self.idx))

    def test_vi_prose_preserved_through_shared_terms(self):
        cat = localization.Catalog(language='vi')
        vi_title = cat.text('glossary:quarreling_twins')
        self.assertEqual(vi_title, 'Cặp song sinh thù địch')
        for mid in ('stage0053_04:r_0c705091f748360e', 'stage0053_04:r_24e1a808a1609a1a',
                    'stage0060_03:r_c9016e3ab05470b0', 'stage0069_03:r_f2d72b948cc38cfe'):
            # Catalog.text also validates the new shared token contract.
            text = cat.text(mid)
            self.assertEqual(text.count('$$いがみ合う双子$$'), 1)
            self.assertIn(vi_title, text.replace('$$いがみ合う双子$$', vi_title))
        for mid in ('stage0052_03:r_7cbc63dad295f862', 'stage0052_03:r_d7f1c506e78e55ff'):
            self.assertTrue(cat.text(mid))
        self.assertEqual(cat.text('glossary:sorrowful_maiden'), 'Trinh nữ bi thương')
        self.assertEqual(cat.text('glossary:wounded_lion'), 'Sư tử đầy thương tích')
        self.assertEqual(cat.text('glossary:lying_black_sheep'), 'Cừu đen dối trá')
        self.assertEqual(cat.text('glossary:inexhaustable_water_gourd'), 'Bình nước vô tận')


if __name__ == '__main__':
    unittest.main()
