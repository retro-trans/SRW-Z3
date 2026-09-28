"""Keep lore-name capitalization without changing ordinary uses of sphere."""
import json
from pathlib import Path
import re
import unittest
import localization
import terms


class LoreCapitalizationTests(unittest.TestCase):
    def test_catalog_has_no_lore_lowercase_overrides(self):
        bad_token = re.compile(r'\$\$(?:スフィア|次元力)(?:#[^$|]+)?\|lc\$\$')
        for p in Path('localization/locales/en').glob('*.json'):
            for mid, row in json.loads(p.read_text(encoding='utf-8')).get('messages', {}).items():
                text = row.get('text') or ''
                self.assertIsNone(bad_token.search(text), mid)
                for m in re.finditer(r'\bdimensional[ -]power\b', text, re.I):
                    self.assertEqual(m[0], 'Dimensional Power', mid)

    def test_reported_dialogue_expands_with_capitals(self):
        idx = terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8')))
        cat = localization.english()
        kouji = terms.expand(cat.text('stage0052_03:r_adec86483b13599a'), idx)
        banagher = terms.expand(cat.text('stage0052_03:r_2cf701bbcde3ec13'), idx)
        self.assertIn('about Sphere and Dimensional Power', kouji)
        self.assertIn('「Dimensional Power pulls energy', banagher)

    def test_ordinary_sphere_references_unchanged(self):
        cat = localization.english()
        self.assertIn('sphere of human life', cat.text('stage0095_04:r_f5432119677514f7'))
        self.assertIn('curl into a sphere', cat.text('library.rt_000:r_44ead4450a866673'))
        self.assertIn('Earth sphere', cat.text('library.kw_018:r_ee8207e70f8fc923'))

    def test_shared_vietnamese_references_still_validate(self):
        cat = localization.Catalog(language='vi')
        for filename in ('stage0052_03.json', 'stage0055_03.json'):
            rows = json.loads((Path('localization/locales/vi') / filename).read_text(encoding='utf-8'))['messages']
            for mid, row in rows.items():
                text = row.get('text') or ''
                if '$$スフィア$$' in text or '$$次元力$$' in text:
                    self.assertEqual(cat.text(mid), text)


if __name__ == '__main__':
    unittest.main()
