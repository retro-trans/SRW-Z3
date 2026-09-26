"""Power-part source inventory, effects, glyph fit and candidate safety."""
import json
import struct
import unittest
from pathlib import Path
import eboot
import trdata
import rpw
from build_parts_descriptions import ROOT, DESC, HOOK, generate, wrap
from parts_description_catalog import CATALOG
from patch_parts_candidate import patch
from intermission_layout import ink


class PartsDescriptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = ROOT / 'work/out_0.6.3'
        cls.mapping = json.loads((cls.out / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((cls.out / 'widths.json').read_text()).items()}
        cls.descriptions = json.loads(DESC.read_text(encoding='utf-8'))
        cls.hook = json.loads(HOOK.read_text(encoding='utf-8'))

    def test_all_parts_and_all_original_variants(self):
        expected = generate(self.mapping, self.widths)
        self.assertEqual(len(CATALOG), 69)
        self.assertEqual(len(expected), 300)
        self.assertEqual(expected, {k:v for k,v in self.descriptions.items() if not k.startswith('_')})
        self.assertEqual(expected, {r['jp']:r['en'] for r in self.hook['lines']})

    def test_every_variant_fits_with_dlc_and_valid_glyphs(self):
        for row in self.hook['lines']:
            en = row['en']
            self.assertLessEqual(len(en.splitlines()), 3)
            for line in en.splitlines():
                self.assertLessEqual(ink(line, self.mapping, self.widths, 28), 540)
                self.assertTrue(all(c in self.mapping for c in line), repr(line))
            self.assertEqual('ＤＬ専用' in row['jp'], 'DLC only.' in en.replace('\n', ' '))
            self.assertNotIn('$$', en)
            self.assertTrue(eboot._encode_marked(en, self.mapping))

    def test_effect_regressions(self):
        for row in self.hook['lines']:
            jp, en = row['jp'], row['en'].replace('\n', ' ')
            if 'マップ兵器及び' in jp:
                self.assertRegex(en, 'exclud')
                self.assertIn('MAP', en)
                self.assertTrue('range-1' in en or 'range of 1' in en)
            if '切り払い' in jp:
                for text in ('100% Parry', 'pilot status', 'consecutive-targeting', 'placement penalties'):
                    self.assertIn(text, en)
            if 'ＨＰのダメージ％' in jp:
                self.assertIn('missing HP% / 3', en)
                self.assertIn('60%', en)
                self.assertIn('+20%', en)
            if '出撃１ターン目' in jp:
                self.assertIn('second deployed turn', en)
            if '複数の精神' in jp or '「愛・勇気・魂' in jp or '精神コマンド「愛」「勇気」' in jp:
                for name in ('Love', 'Bravery', 'Soul', 'Fury', 'Zeal', 'Snipe', 'Assail', 'Guard', 'Focus'):
                    self.assertIn(name, en)

    def test_no_accidental_line_fragment_generation(self):
        self.assertIs(self.hook['line_pairs'], False)
        exact = eboot.load_ui_hook(paths=[str(HOOK)])
        # load_ui_hook always appends module-supplied families (mission lines,
        # name entry, team orders, bonus descriptions), so the table's total
        # size says nothing about this file; check the parts rows directly.
        parts = {row['jp'] for row in self.hook['lines']}
        self.assertEqual(len(parts), 300)
        self.assertTrue(parts <= set(exact))
        for jp in parts:
            for line in jp.split('\n')[1:]:
                line = line.strip('　 ')
                if line and line not in parts:
                    self.assertNotIn(line, exact, line)

    def test_rpw_descriptions_still_original(self):
        def descriptions(path):
            raw = path.read_bytes()
            _, _, start, end, _ = next(c for c in rpw.chunks(raw) if c[0] == 'j-string')
            # Translated name glyph cells need not be legal Unicode CP932;
            # compare the untouched description bytes without decoding names.
            strings = raw[start:end].split(b'\0')
            return {slot: strings[i] for slot,i in rpw.slots(raw).items()
                    if slot[0] == 'boost-p' and 3 <= slot[2] <= 8}
        self.assertEqual(descriptions(ROOT / 'work/orig/RPW_DATA.CPK'),
                         descriptions(self.out / 'RPW_DATA.CPK'))

    def test_candidate_delta_is_reproducible_and_all_keys_installed(self):
        baseline = ROOT / 'work/parts_hooks_before.json'
        backup = ROOT / 'work/parts_descriptions_EBOOT.before.bin'
        if not backup.exists():
            self.skipTest('Run candidate patch --write to verify its byte isolation')
        trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
        before = json.loads(baseline.read_text(encoding='utf-8'))
        current = eboot.load_ui_hook()
        # Later isolated hook batches legitimately alter the live table.
        # Replay this batch against its historical endpoint, then check the
        # currently installed part entries independently below.
        next_baseline = ROOT / 'work/skill_hooks_before.json'
        next_backup = ROOT / 'work/skill_descriptions_EBOOT.before.bin'
        endpoint = json.loads(next_baseline.read_text(encoding='utf-8')) if next_backup.exists() else current
        replay, _ = patch(backup.read_bytes(), self.mapping, before, endpoint)
        self.assertEqual(replay, next_backup.read_bytes() if next_backup.exists() else (self.out / 'EBOOT.BIN').read_bytes())
        data = (self.out / 'EBOOT.BIN').read_bytes()
        segs = eboot._segments(data)
        table, p = {}, eboot._off(segs, eboot.NAME_TBL)
        while struct.unpack_from('>I', data, p)[0]:
            k,v = struct.unpack_from('>II', data, p)
            a,b = eboot._off(segs,k), eboot._off(segs,v & 0x3fffffff)
            table[data[a:data.index(0,a)]] = data[b:data.index(0,b)]
            p += 8
        for row in self.hook['lines']:
            # This immutable .3 fixture predates BOTH Akurasu renames:
            # 鉄壁 Wall -> Guard and 闘志 Fighting Spirit -> Fury.
            # Rewrap the historical wording using its original metrics.
            en = wrap(row['en'].replace('Assail, Guard and', 'Assail, Wall and')
                      .replace('Fury', 'Fighting Spirit'), self.mapping, self.widths)
            self.assertEqual(table[row['jp'].encode('cp932')],
                             eboot._encode_marked(en, self.mapping))


if __name__ == '__main__':
    unittest.main()
