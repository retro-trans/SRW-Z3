"""Regression negatives for source coverage and victory/defeat context."""
import unittest
import json
from pathlib import Path
import struct
from unittest.mock import patch
import audit_message_classes as audit
import eboot, trdata
import mission_conditions as mission


class MissionConditionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary(str(audit.ROOT / 'analysis/glossary.json'))
        cls.hooks = eboot.load_ui_hook()

    def test_all_extracted_mission_variants_are_translated_and_fit(self):
        root = Path('work/build_0.6.17_english_namefix_20260919')
        mapping = json.loads((root / 'pairs.json').read_text())
        widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        report = audit.check(self.hooks, mapping, widths)
        self.assertTrue(report['complete'])
        self.assertEqual(report['missing_count'], 0)
        self.assertGreater(len(report['stages']), 100)

    def test_episode19_stg0031b_screenshot(self):
        expected = {
            '１．５ターン目を迎える。': '1. Turn 5 begins.',
            '２．第６の使徒を撃墜する。': '2. Shoot down the Sixth Angel.',
            '２．シンジ・レイ・アマタ・ヒビキ、いずれかの撃墜。':
                '2. Shinji, Rei, Amata or Hibiki is shot down.',
        }
        for jp, en in expected.items():
            self.assertEqual(self.hooks[jp], en)
        sr = self.hooks['４ターン以内に第６の使徒のＨＰを２００００以下にする。']
        self.assertIn('20,000', sr)
        self.assertIn('4 turns', sr)
        self.assertIn('Sixth Angel', sr)

    def test_lua_display_escapes_not_only_point(self):
        for source, displayed in [('ポ\\イント', 'ポイント'), ('ソ\\ーラー', 'ソーラー'),
                                  ('倒\\す', '倒す'), ('竹\\尾', '竹尾'), ('Ｚｙ－\\９８', 'Ｚｙ－９８')]:
            self.assertEqual(mission.displayed_variants(source), {source, displayed})

    def test_new_catalog_line_counts_and_no_unexpanded_markers(self):
        rows = mission.additional_lines()
        self.assertEqual(len(rows), 180)
        for row in rows:
            self.assertEqual(row['jp'].count('\n'), row['en'].count('\n'), row)
            self.assertNotIn('$', row['en'], row)

    def test_shared_fragments_retain_their_meaning(self):
        fragments = mission.line_hooks(mission.additional_lines())
        self.assertEqual(fragments['マップをクリアする。'], 'Clear the map.')
        self.assertEqual(fragments['敵を全滅させる。'], 'Destroy all enemies.')
        self.assertEqual(fragments['アフラ・グニスを撃墜する。'], 'Shoot down Ahura Gnis.')
        self.assertEqual(fragments['マキシマムブレイクで撃墜する。'], 'using Maximum Break.')
        for jp, en in fragments.items():
            self.assertEqual(self.hooks[jp], en)
        contradictory = [dict(role='sr', jp='共有の条件です。\n条件は続く。', en='First.\nNext.'),
                         dict(role='sr', jp='共有の条件です。\n条件は変わる。', en='Wrong.\nLater.')]
        with self.assertRaisesRegex(AssertionError, 'Mission line conflict'):
            mission.line_hooks(contradictory)

    def test_all_hooks_fit_existing_extension_and_are_emitted(self):
        # Rebuild ONLY the table in memory, never save/boot an executable.
        root = Path('work/build_0.6.17_english_namefix_20260919')
        blob = bytearray((root / 'EBOOT.BIN').read_bytes())
        mapping = json.loads((root / 'pairs.json').read_text())
        segs = eboot._segments(blob)
        before_headers = bytes(blob[:0x300])
        terms = json.loads(Path('analysis/glossary.json').read_text(encoding='utf-8'))['terms']
        names = {t['jp']: t['en'] for t in terms if t['en']}
        all_names = dict(names)
        for path in sorted(Path('translation/library').glob('*.json')):
            all_names.update(trdata.names(str(path)))
        from build_project import load_labels
        weapons = json.loads(Path('translation/weapons.json').read_text(encoding='utf-8'))
        names = {**load_labels(), **weapons, **names}
        names.update(trdata.assemble('translation/library', 'kw',
                     trdata.ambiguous_terms('analysis/glossary.json'))[1])
        struct.pack_into('>I', blob, eboot._off(segs, eboot.NAME_SITE), eboot.NAME_ORIG)
        with patch.object(eboot, 'HOOK_ALL_SET', set(all_names)):
            count, skipped, end, *_ = eboot.name_hook(blob, segs, names, mapping)
        self.assertGreater(count, 4095)
        self.assertEqual(skipped, 0)
        self.assertLess(end, eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE)
        self.assertEqual(bytes(blob[:0x300]), before_headers)
        entries = {}
        pos = eboot._off(segs, eboot.NAME_TBL)
        for _ in range(count):
            jp, en = struct.unpack_from('>II', blob, pos)
            entries[bytes(eboot._cstr(blob, eboot._off(segs, jp)))] = (en >> 30,
                bytes(eboot._cstr(blob, eboot._off(segs, en & 0x3fffffff))))
            pos += 8
        for row in mission.expand(mission.additional_lines()):
            self.assertEqual(entries[row['jp'].encode('cp932')],
                             (0, eboot._encode_marked(row['en'], mapping)))
        for jp, en in mission.line_hooks(mission.additional_lines()).items():
            self.assertEqual(entries[jp.encode('cp932')], (0, eboot._encode_marked(en, mapping)))
        print('PASS: %d hook entries; %d bytes left in unchanged extension.' %
              (count, eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE - end))

    def test_shared_english_never_aliases_keys_or_tutorial_tail(self):
        root = Path('work/build_0.6.17_english_namefix_20260919')
        blob = bytearray((root / 'EBOOT.BIN').read_bytes())
        mapping = json.loads((root / 'pairs.json').read_text())
        segs = eboot._segments(blob)
        inputs = {'甲乙': 'Test', '丙丁': 'Test', '\x01戊己': 'Test'}
        struct.pack_into('>I', blob, eboot._off(segs, eboot.NAME_SITE), eboot.NAME_ORIG)
        with patch.object(eboot, 'load_ui_hook', return_value=inputs):
            count, skipped, *_ = eboot.name_hook(blob, segs, {}, mapping)
        self.assertEqual((count, skipped), (3, 0))
        entries = {}
        pos = eboot._off(segs, eboot.NAME_TBL)
        for _ in range(count):
            jp, en = struct.unpack_from('>II', blob, pos)
            entries[eboot._cstr(blob, eboot._off(segs, jp)).decode('cp932')] = (jp, en)
            pos += 8
        self.assertEqual(entries['甲乙'][1], entries['丙丁'][1])
        self.assertNotEqual(entries['甲乙'][0], entries['丙丁'][0])
        self.assertNotEqual(entries['甲乙'][1], entries['\x01戊己'][1])
        end = eboot._off(segs, entries['\x01戊己'][1]) + len(eboot._encode_marked('Test', mapping)) + 1
        self.assertEqual(eboot._cstr(blob, end), eboot._encode_marked('.', mapping))

    def test_missing_effect_is_rejected(self):
        hooks = dict(self.hooks)
        del hooks['バリア貫通']
        with self.assertRaisesRegex(AssertionError, 'Untranslated source messages'):
            audit.check(hooks)

    def test_victory_cannot_use_defeat_wording(self):
        hooks = dict(self.hooks, **{'クシャトリヤの撃墜。': 'Kshatriya is shot down.'})
        with self.assertRaises(AssertionError):
            audit.check_roles(hooks)

    def test_defeat_cannot_use_victory_wording(self):
        hooks = dict(self.hooks, **{'シンジの撃墜。': 'Shoot down Shinji.'})
        with self.assertRaises(AssertionError):
            audit.check_roles(hooks)

    def test_displayed_name_and_point_variants(self):
        for jp in ('ヒビキ、またはカレンの撃墜。', '相手のポイントに到達する。',
                   '第４の使徒のポイント到達。', '練馬ＲＤが自軍のポイントに到達する。'):
            for number, prefix in enumerate(('', '１．', '２．', '３．')):
                self.assertEqual(self.hooks[prefix + jp],
                                 (str(number) + '. ' if number else '') + self.hooks[jp])


if __name__ == '__main__':
    unittest.main()
