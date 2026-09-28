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
}
OLD = ('Maiden of Sorrow', 'Scarred Lion', 'False Black Ram',
       'Deceiving Black', 'Endless Water Jar', 'Never-Emptying Water Jar',
       'Inexhaustible Water Bearer')


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
                    self.assertNotIn(old, row.get('text') or '', mid)

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
        for mid in ('stage0052_03:r_7cbc63dad295f862', 'stage0052_03:r_d7f1c506e78e55ff'):
            self.assertTrue(cat.text(mid))
        self.assertEqual(cat.text('glossary:sorrowful_maiden'), 'Trinh nữ bi thương')
        self.assertEqual(cat.text('glossary:wounded_lion'), 'Sư tử đầy thương tích')
        self.assertEqual(cat.text('glossary:lying_black_sheep'), 'Cừu đen dối trá')
        self.assertEqual(cat.text('glossary:inexhaustable_water_gourd'), 'Bình nước vô tận')


if __name__ == '__main__':
    unittest.main()
