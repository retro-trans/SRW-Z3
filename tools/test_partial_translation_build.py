"""Partial releases document mission backlog without hiding broken translations."""
import json
import unittest
from unittest.mock import patch
import audit_message_classes as audit
import narration_layout


class PartialBuildTests(unittest.TestCase):
    def run_check(self, rows, hooks, partial):
        with patch.object(audit, 'inventory', return_value=(rows, ['STG0001A.cpk'])), \
             patch.object(audit, 'check_roles') as role_check:
            result = audit.check(hooks, allow_untranslated_missions=partial)
            role_check.assert_called_once_with(hooks, allow_untranslated_missions=partial)
            return result

    def test_default_remains_strict(self):
        with self.assertRaises(AssertionError):
            self.run_check([{'class': 'mission', 'jp': '未訳'}], {}, False)

    def test_shared_turn_boundary_is_role_neutral(self):
        self.assertTrue(audit.role_neutral('７ターン目を迎える。', 'Turn 7 begins.'))
        self.assertFalse(audit.role_neutral('７ターン目を迎える。', 'Survive until turn 7.'))
        self.assertFalse(audit.role_neutral('敵の撃墜。', 'Shoot down the enemy.'))

    def test_partial_reports_exact_backlog(self):
        missing = {'class': 'mission', 'jp': '未訳'}
        report = self.run_check([missing, {'class': 'effect', 'jp': '既訳'}], {'既訳': 'Translated'}, True)
        self.assertFalse(report['complete'])
        self.assertEqual(report['missing'], [missing])
        self.assertEqual(report['translated_variants'], 1)

    def test_partial_cannot_hide_missing_ui(self):
        for kind in ['effect', 'reward', 'unlock', 'unlock-shop', 'squad-name']:
            with self.assertRaises(AssertionError):
                self.run_check([{'class': kind, 'jp': '未訳'}], {}, True)

    def test_partial_still_rejects_japanese_translation(self):
        with self.assertRaises(AssertionError):
            self.run_check([{'class': 'mission', 'jp': '未訳'}], {'未訳': 'まだ日本語'}, True)

    def test_narration_selection_ignores_new_action_rows(self):
        rows = narration_layout.rows()
        self.assertEqual(len(rows), 18)
        self.assertEqual([row['jp'] for row in rows], list(narration_layout.KEYS))
        self.assertFalse(any(row['jp'].startswith('・') for row in rows))

    def test_narration_missing_key_rejected(self):
        rows = narration_layout.rows()[:-1]
        with patch.object(narration_layout.Path, 'read_text', return_value=json.dumps({'lines': rows})):
            with self.assertRaises(AssertionError):
                narration_layout.rows()

    def test_narration_duplicate_key_rejected(self):
        rows = narration_layout.rows()
        with patch.object(narration_layout.Path, 'read_text', return_value=json.dumps({'lines': rows + rows[:1]})):
            with self.assertRaises(AssertionError):
                narration_layout.rows()


if __name__ == '__main__':
    unittest.main()
