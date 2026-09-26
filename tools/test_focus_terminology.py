"""Focus/Foc stat consistency without touching generic morale or Spirit identities."""
import json,re,unittest
from pathlib import Path
from unittest.mock import patch
import eboot,trdata,digraph as dg
from standardize_focus import FILES
from patch_focus_candidate import OUT,BACKUP,update_elf,update_rpw,update_voice,name_changes,table


class FocusTerminology(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.mapping=json.loads((OUT/'pairs.json').read_text())

    def test_source_stat_consistency(self):
        for path in FILES+('translation/parts_desc_hook.json','translation/parts_descriptions.unshipped.json','translation/skill_hook.json'):
            self.assertNotRegex(Path(path).read_text(encoding='utf-8'),r'\bMorale\b')
        for jp,en in eboot.load_ui_hook().items():
            self.assertNotRegex(en,r'\bMorale\b')

    def test_screenshot_labels_and_compact_names(self):
        hooks=eboot.load_ui_hook()
        self.assertTrue(any('Req. Focus' in en for en in hooks.values()))
        self.assertTrue(any('Starting Focus +5 when deployed.' in en for en in hooks.values()))
        names=json.loads(Path('translation/skills.json').read_text(encoding='utf-8'))
        self.assertEqual(names['気力＋（ダメージ）'],'Foc+ Dmg')
        self.assertEqual(names['気力＋ボーナス'],'Foc Bonus')
        self.assertEqual(len(name_changes()),5)

    def test_spirit_and_ordinary_dialogue_unchanged(self):
        spirits=json.loads(Path('translation/spirits.json').read_text(encoding='utf-8'))
        self.assertEqual(spirits['集中'],'Focus')
        self.assertEqual(spirits['集中＋'],'Focus+')
        self.assertIn('Crush their morale!',Path('translation/voice_135.json').read_text(encoding='utf-8'))
        self.assertIn("people's morale",Path('translation/stage0046a_03.json').read_text(encoding='utf-8'))

    def test_elf_delta_and_active_hooks(self):
        old=BACKUP.read_bytes();data=(OUT/'EBOOT.BIN').read_bytes()
        before=json.loads(Path('work/focus_hooks_before.json').read_text(encoding='utf-8'))
        # Replay the historical Focus-only delta against its own endpoint.
        # The later Counterattack repair has independent replay coverage.
        historical=dict(eboot.load_ui_hook())
        for key in ('・反撃する','・反撃する\n・防御する\n・回避する'):
            historical[key]=before[key]
        with patch('patch_focus_candidate.eboot.load_ui_hook',return_value=historical):
            replay,stats=update_elf(old,self.mapping)
        self.assertEqual(Path('work/counterattack_EBOOT.before.bin').read_bytes(),replay)
        self.assertEqual(stats[:2],(163,0))
        active=table(data)
        for jp,en in eboot.load_ui_hook().items():
            if before.get(jp)!=en:
                self.assertEqual(active[jp.encode('cp932')][1],eboot._encode_marked(en,self.mapping))

    def test_rpw_name_only_delta(self):
        data=(OUT/'RPW_DATA.CPK').read_bytes()
        replay,counts=update_rpw(Path('work/focus_RPW.before.bin').read_bytes(),self.mapping)
        self.assertEqual(data,replay)
        self.assertEqual(list(counts.values()),[1]*5)

    def test_voice_tips_only_delta(self):
        replay,count=update_voice(Path('work/focus_SRVC.before.bin').read_bytes(),BACKUP.read_bytes(),self.mapping)
        self.assertEqual(replay,(OUT/'SRVC.BIN').read_bytes())
        self.assertEqual(count,2)


if __name__=='__main__':unittest.main()
