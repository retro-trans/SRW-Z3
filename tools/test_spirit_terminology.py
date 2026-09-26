"""Akurasu Z3 command identities, distinct from the Fighting Spirit skill."""
import json
from pathlib import Path
import unittest

import digraph

ROOT = Path(__file__).resolve().parents[1]


def catalog(name, source=False):
    folder = 'messages' if source else 'locales/en'
    return json.loads((ROOT / 'localization' / folder / (name + '.json'))
                      .read_text(encoding='utf-8'))['messages']


class SpiritTerminologyTests(unittest.TestCase):
    def test_japanese_identities_and_distinct_names(self):
        source, locale = catalog('spirits', True), catalog('spirits')
        names = {row['source']: locale[key]['text'] for key, row in source.items()}
        self.assertEqual(names['闘志'], 'Fury')
        self.assertEqual(names['直撃'], 'Break')
        self.assertEqual(len(names.values()), len(set(names.values())))
        legacy = json.loads((ROOT / 'translation/spirits.json').read_text(encoding='utf-8'))
        for jp in ('闘志', '直撃'):
            self.assertEqual(legacy[jp], names[jp])

    def test_compact_flags_keep_native_identity(self):
        self.assertEqual(digraph.TINY_CELLS['\ue007'], ('Fu', 0x86BF))
        self.assertEqual(digraph.TINY_CELLS['\ue012'], ('Br', 0x86CA))

    def test_related_effects_and_no_stale_command_name(self):
        for name in ('spirits', 'ability_hook', 'bonus_descriptions', 'spirit_hook',
                     'parts_desc_hook', 'parts_descriptions.unshipped'):
            for key, row in catalog(name).items():
                self.assertNotIn('Fighting Spirit', ' '.join(row['text'].split()), key)
        self.assertIn('Fury', catalog('ability_hook')['ability_hook:r_1b9b2aab5cb104da']['text'])
        bravery = catalog('spirit_hook')['spirit_hook:r_77ca87eacd17ad52']['text']
        self.assertIn('Break', bravery)
        self.assertNotIn('Fury', bravery)
        for key in ('bonus_descriptions:va_70ade8', 'bonus_descriptions:va_70b168'):
            self.assertIn('Fury', catalog('bonus_descriptions')[key]['text'])

    def test_unrelated_pilot_skill_keeps_its_name(self):
        source, locale = catalog('skills', True), catalog('skills')
        names = {row['source']: locale[key]['text'] for key, row in source.items()}
        self.assertEqual(names['戦意高揚'], 'Fighting Sp')
        self.assertEqual(names['闘争心'], 'Instinct')


if __name__ == '__main__':
    unittest.main()
