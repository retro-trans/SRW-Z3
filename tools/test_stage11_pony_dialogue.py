"""Reported run-together Pony Man dialogue must remain readable and fit."""
import json
from pathlib import Path
import unittest

import check_stage
import localization
import terms


EXPECTED = {
    'stage0011_03:r_d60d0818e965232f':
        "$n\n「Apparently, all he says is 'poni'.\n"
        "　Accounts of his appearance vary,\n"
        "　but so far, it's all speculation.」",
    'stage0011_03:r_5b23687574286204':
        "$n\n「The most common accounts describe a half-man,\n"
        "　half-beast creature with a horse's lower body,\n"
        "　racehorse speed, horse-like snorts, and a love of carrots...」",
}


class PonyDialogueTests(unittest.TestCase):
    def test_wording(self):
        catalog = localization.english()
        for mid, expected in EXPECTED.items():
            with self.subTest(mid=mid):
                self.assertEqual(catalog.text(mid), expected)

    def test_structure_encoding_and_width(self):
        catalog = localization.english()
        pair_path = Path('work/build_0.6.24_english_20260930/pairs.json')
        if not pair_path.exists():
            self.skipTest('Local release font mapping is unavailable')
        self.assertTrue(check_stage.widths_ready(), 'PS3 font required for width check')
        raw = json.loads(pair_path.read_text(encoding='utf-8'))
        mapping = {k if len(k) == 1 else (k[0], k[1]): v for k, v in raw.items()}
        index = terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8')))
        records = [{'sha': mid, 'jp': catalog.definition(mid)['source']} for mid in EXPECTED]
        answers = {mid: catalog.text(mid) for mid in EXPECTED}
        self.assertEqual(check_stage.check(records, answers, mapping=mapping,
                                           term_idx=index), [])


if __name__ == '__main__':
    unittest.main()
