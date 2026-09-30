"""Akurasu terminology regression; local fixtures only, no game output."""
import json
from pathlib import Path
import unittest
from cpk import CPK
import bonus_descriptions
import build_project
import digraph as dg
import eboot
import localization
import rpw
import skill_name_transport
import trdata
from intermission_layout import ink


class AggressiveBeastTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        root = Path('work/build_0.6.21_english_20260925_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}

    def test_name_and_bonus_agree(self):
        cat = localization.english()
        name = cat.text('skills:r_671a3037d9a84efd')
        self.assertEqual(name, 'Aggressive Beast')
        self.assertEqual(build_project.load_labels()['野性化'], name)
        bonus = cat.text('bonus_descriptions:va_70a2d8')
        self.assertIn(name, bonus)
        self.assertNotIn('Feral', bonus)
        jp = '「野性化」発動時、\n一度だけ精神コマンド「覚醒」が掛かる。'
        self.assertEqual(bonus_descriptions.hooks()[jp], bonus)
        self.assertEqual(eboot.load_ui_hook()[jp], bonus)
        # Conservative bounds within the reported wide skill panel and bonus
        # help panel; measured with the released font, not a visual-test claim.
        self.assertLess(ink(name, self.mapping, self.widths, 31), 400)
        self.assertLessEqual(len(bonus.splitlines()), 3)
        for line in bonus.splitlines():
            self.assertTrue(all(c in self.mapping for c in line))
            self.assertLess(ink(line, self.mapping, self.widths, 28), 600)

    def test_rpw_keeps_safe_native_name_and_preserves_other_strings(self):
        cpk = CPK('work/orig/RPW_DATA.CPK')
        before = cpk.read(cpk.files[0])
        strings = rpw.jstrings(before)
        plan = rpw.plan_all(strings, {'野性化': 'Aggressive Beast'})
        self.assertTrue(plan)
        encoded = {i: dg.encode_mixed(en, self.mapping) for i, en in plan.items()}
        overrides = skill_name_transport.overrides(before)
        after, appended = rpw.build_grown(before, encoded, overrides)
        self.assertGreater(appended, 0)
        def raw_strings(blob):
            _, _, start, end, _ = next(c for c in rpw.chunks(blob) if c[0] == 'j-string')
            return blob[start:end].split(b'\0')
        old, new = raw_strings(before), raw_strings(after)
        slots_old, slots_new = rpw.slots(before), rpw.slots(after)
        self.assertEqual(slots_old.keys(), slots_new.keys())
        found = 0
        for slot, i in slots_old.items():
            self.assertEqual(new[slots_new[slot]], overrides.get(slot, encoded.get(i, old[i])), slot)
            found += i in plan
        self.assertGreater(found, 0)
        self.assertEqual(skill_name_transport.hooks()[0]['野性化'], 'Aggressive Beast')


if __name__ == '__main__':
    unittest.main()
