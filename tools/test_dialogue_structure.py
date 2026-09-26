"""Speaker-header regressions: source text, not portrait or previous speaker."""
import unittest
from unittest.mock import patch

import check_stage
import dialogue_structure as structure
import localization
import luarec
import patch_lua


SOURCE = '葵\n（何だろう…。\n　あたしの中の何かが、目を覚まそうとしている…）'
BROKEN = '(What is this...\n Something inside me is trying to wake up...)'
FIXED = 'Aoi\n' + BROKEN
LUA = ('t_101 = {\n{WPos_B, 3, FDMode_Normal, pid_AOI,\n[['
       + SOURCE + ']]},\n};\n').encode('cp932')


class DialogueStructureTests(unittest.TestCase):
    def test_missing_and_joined_headers(self):
        for value in (BROKEN, '$$葵$$'+BROKEN, 'Aoi'+BROKEN, 'Aoi', '\n'+BROKEN):
            with self.subTest(value=value):
                self.assertIsNotNone(structure.speaker_problem(SOURCE, value))
        for value in (FIXED, '$$葵$$\n'+BROKEN, '$n\n'+BROKEN):
            self.assertIsNone(structure.speaker_problem(SOURCE, value))

    def test_anonymous_narration_labels_and_crlf(self):
        for source in ('\n（何だろう…）', '（何だろう…）', '地球',
                       '長い説明\n続き', None):
            self.assertIsNone(structure.speaker_problem(source, BROKEN))
        self.assertIsNone(structure.speaker_problem(
            SOURCE.replace('\n', '\r\n'), FIXED.replace('\n', '\r\n')))
        self.assertIsNotNone(structure.speaker_problem('？？？\n「誰だ」', '「Who?」'))

    def test_stage_checker_and_patcher_reject_before_encoding(self):
        recs = luarec.records(LUA.decode('cp932'))
        with patch.object(check_stage.dg, 'encode_mixed', return_value=b''):
            result = check_stage.check(recs, {recs[0]['sha']: BROKEN},
                                       measure=False, mapping={}, term_idx={})
        self.assertIn('speaker', [p[1] for p in result])
        for value in (BROKEN, 'Aoi'+BROKEN):
            with self.assertRaisesRegex(SystemExit, 'speaker header'):
                patch_lua.patch(LUA, [value], {})
        with patch.object(patch_lua.dg, 'VWF', False), patch.object(
                patch_lua.dg, 'encode_mixed', side_effect=lambda en, _: en.encode('ascii')):
            patched = patch_lua.patch(LUA, [FIXED], {})
        self.assertIn(b'[[Aoi\n(What is this...', patched)
        self.assertEqual(patched.split(b'[[')[0], LUA.split(b'[[')[0])

    def test_catalog_gate_rejects_future_regression(self):
        catalog = localization.Catalog()
        mid = 'stage0050b_04:r_1956994937f8171e'
        self.assertTrue(catalog.text(mid).startswith('$$葵$$\n'))
        # Retain tokens; proves this is a structural check, not token counting.
        row = catalog.locale('en', 'stage0050b_04')[mid]
        row['text'] = row['text'].replace('$$葵$$\n', '$$葵$$', 1)
        with self.assertRaisesRegex(ValueError, 'Dialogue speaker'):
            catalog.text(mid)

    def test_entire_catalog_and_reported_speakers(self):
        catalog = localization.Catalog()
        checked = named = 0
        for group in catalog.manifest['groups']:
            definitions = catalog.document('localization/messages/'+group+'.json')['messages']
            for mid, definition in definitions.items():
                if definition['kind'] != 'dialogue':
                    continue
                checked += 1
                named += bool(structure.named_source(definition.get('source')))
                self.assertIsNone(structure.speaker_problem(
                    definition.get('source'), catalog.text(mid)), mid)
        self.assertGreaterEqual(checked, 62788)
        self.assertGreaterEqual(named, 58502)
        for suffix, name in (('ec335e69f984b8b3', 'ダストン'),
                             ('1956994937f8171e', '葵'),
                             ('48f49f6728c15612', '葵'),
                             ('0ebc5a6f1e0f81bf', 'アマタ')):
            self.assertTrue(catalog.text('stage0050b_04:r_'+suffix).startswith('$$'+name+'$$\n'))


if __name__ == '__main__':
    unittest.main()
