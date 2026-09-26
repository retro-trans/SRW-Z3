"""Regression tests for moved mission presets and conflicting menu hooks."""
import json
import unittest
from pathlib import Path
from cpk import CPK
import audit_message_classes as A
import eboot
import trdata
import patch_counterattack_candidate as C


class FakeCPK:
    def __init__(self, contents):
        self.contents=contents
        self.files=[{'id':i} for i in contents]
    def read(self, entry): return self.contents[entry['id']].encode('cp932')


PRESET='-- "out/stage0068preset.lua"\nOPERATE_TBL = { str_tbl = { "敵の全滅。" }; };'


class MissionPresetTests(unittest.TestCase):
    def test_preset_in_member_one(self):
        self.assertEqual(A.preset_text(FakeCPK({1:PRESET}),'STG0068.cpk'),PRESET)

    def test_preset_after_shared_constants(self):
        self.assertEqual(A.preset_text(FakeCPK({1:'-- stage_require.lua',3:PRESET}),'STG0068.cpk'),PRESET)

    def test_missing_preset_rejected(self):
        with self.assertRaisesRegex(AssertionError,'missing mission preset'):
            A.preset_text(FakeCPK({1:'-- stage_require.lua'}),'STG0068.cpk')

    def test_ambiguous_preset_rejected(self):
        with self.assertRaisesRegex(AssertionError,'ambiguous mission preset'):
            A.preset_text(FakeCPK({1:PRESET,3:PRESET}),'STG0068.cpk')

    def test_known_dialogue_only_routes(self):
        self.assertIsNone(A.preset_text(FakeCPK({i:'-- dialogue' for i in (0,2,3,4)}),'STG0210.cpk'))
        self.assertIsNone(A.preset_text(FakeCPK({1:'SC_PROCESS_STAGE_CLEAR'}),'STG0200.cpk'))

    def test_route_exception_cannot_hide_new_objectives(self):
        with self.assertRaisesRegex(AssertionError,'objective table without named preset'):
            A.preset_text(FakeCPK({0:'',2:'',3:'OPERATE_TBL = {}',4:''}),'STG0210.cpk')

    def test_real_stage_68_reads_member_three(self):
        path=A.ROOT/'work/stage_dec/STG0068.cpk'
        if not path.exists(): self.skipTest('local source unavailable')
        cpk=CPK(str(path))
        self.assertEqual(A.preset_text(cpk,path),cpk.read(next(f for f in cpk.files if f['id']==3)).decode('cp932'))
        self.assertIn('OPERATE_TBL',A.preset_text(cpk,path))


class CounterattackTests(unittest.TestCase):
    def test_no_conflicting_source_entries(self):
        rows=json.loads((A.ROOT/'translation/issue_hook.json').read_text(encoding='utf-8'))['lines']
        seen={}
        for row in rows:
            self.assertTrue(row['jp'] not in seen or seen[row['jp']]==row['en'],row['jp'])
            seen[row['jp']]=row['en']
        self.assertEqual(sum(row['jp']=='・反撃する' for row in rows),1)
        self.assertEqual(seen['・反撃する'],'・Counterattack')
        self.assertEqual(seen[C.KEY],C.NEW)

    def test_whole_menu_and_line_agree(self):
        trdata.use_glossary(str(A.ROOT/'analysis/glossary.json'))
        hooks=eboot.load_ui_hook([str(A.ROOT/'translation/issue_hook.json')])
        self.assertEqual(hooks[C.KEY].splitlines()[0],hooks['・反撃する'])

    def test_candidate_delta_and_replay(self):
        if not C.BACKUP.exists(): self.skipTest('local backup unavailable')
        mapping=json.loads((C.OUT/'pairs.json').read_text())
        built=C.update(C.BACKUP.read_bytes(),mapping)
        self.assertEqual(built,(C.OUT/'EBOOT.BIN').read_bytes())
        self.assertEqual(C.update(built,mapping),built)


if __name__=='__main__': unittest.main()
