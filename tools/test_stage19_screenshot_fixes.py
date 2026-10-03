"""Stage 19 screenshot corrections: grammar, authored wrapping and referent."""
import json
from pathlib import Path
import unittest

import check_stage
import digraph
import localization
import terms


IDS = (
    'stage0019_03:r_38762a09460d8b6b',
    'stage0019_03:r_d80a9688790ed583',
    'stage0019_03:r_d22851aaafbbf8fc',
    'stage0019_03:r_e598c2a0b27e7f50',
)


class Stage19ScreenshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = localization.english()
        cls.texts = {mid: cls.catalog.text(mid) for mid in IDS}

    def test_core_and_sarcasm(self):
        self.assertIn('Destroying it is the only way', self.texts[IDS[0]])
        self.assertEqual(self.texts[IDS[3]], '$n\n（Did he miss the sarcasm...?）')

    def test_ryouma_breaks_only_between_clauses_or_sentences(self):
        self.assertEqual(self.texts[IDS[1]].splitlines()[1:], [
            '「Even that quiet $n is managing just fine.',
            '　No need to worry.」',
        ])
        self.assertEqual(self.texts[IDS[2]].splitlines()[1:], [
            '「If we mean to act like adults,',
            '　we need to show these kids, him included, a way forward.」',
        ])

    def test_source_structure_encoding_and_measured_widths(self):
        pair_path = Path('work/build_0.6.24_english_20260930/pairs.json')
        if not pair_path.exists():
            self.skipTest('Local release font mapping is unavailable')
        self.assertTrue(check_stage.widths_ready(), 'PS3 font required for width check')
        raw_pairs = json.loads(pair_path.read_text(encoding='utf-8'))
        mapping = {k if len(k) == 1 else (k[0], k[1]): v
                   for k, v in raw_pairs.items()}
        records = [{'sha': mid, 'jp': self.catalog.definition(mid)['source']}
                   for mid in IDS]
        index = terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8')))
        self.assertEqual(check_stage.check(records, self.texts, mapping=mapping,
                                           term_idx=index), [])
        # The generic checker strips runtime names; measure the actual default
        # and an eight-wide-letter stress case explicitly as well.
        for name in ('Hibiki', 'WWWWWWWW'):
            for mid, value in self.texts.items():
                expanded = terms.expand(value, index).replace('$n', name)
                for line in expanded.splitlines():
                    with self.subTest(mid=mid, name=name, line=line):
                        self.assertLessEqual(digraph.line_px(line, 'dialogue'),
                                             digraph.SCREENS['dialogue'][2])


if __name__ == '__main__':
    unittest.main()
