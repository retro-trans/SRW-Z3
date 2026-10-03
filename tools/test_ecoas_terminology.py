"""User-approved ECOAS acronym across prose and existing faction label."""
import json
from pathlib import Path
import unittest
import localization
import terms


class EcoasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat=localization.english()
        cls.idx=terms.index(json.loads(Path('analysis/glossary.json').read_text(encoding='utf8')))

    def test_glossary_and_existing_squad_label_agree(self):
        self.assertEqual(terms.expand('$$エコーズ$$',self.idx),'ECOAS')
        self.assertEqual(self.cat.text('squad_names_hook:r_0121a166c715cdff'),'ECOAS')

    def test_screenshot_and_parallel_route(self):
        for mid in ('stage0007b_03:r_adec86483b13599a','stage0006_03:r_0abcaf0c31978670'):
            value=self.cat.text(mid)
            self.assertIn('$$エコーズ$$',value)
            self.assertIn('ECOAS',terms.expand(value,self.idx))
            self.assertNotIn('Echoes',value)

    def test_source_identified_organization_references_are_consistent(self):
        count=0
        for p in Path('localization/locales/en').glob('*.json'):
            for mid,row in (json.loads(p.read_text(encoding='utf8')).get('messages') or {}).items():
                value=row.get('text') or ''
                source=self.cat.definition(mid).get('source') or ''
                if 'エコーズ' in source:
                    self.assertNotIn('Echoes',value,mid)
                if '$$エコーズ$$' in value:
                    self.assertEqual(value.count('$$エコーズ$$'),1,mid)
                    self.assertIn('ECOAS',terms.expand(value,self.idx))
                    count+=1
        self.assertGreaterEqual(count,45)

    def test_vietnamese_uses_same_acronym_without_fallback(self):
        vi=localization.Catalog(language='vi')
        self.assertEqual(vi.text('glossary:ecoas'),'ECOAS')
        for mid in ('stage0006_03:r_0abcaf0c31978670','stage0007b_03:r_adec86483b13599a'):
            row=vi.locale('vi',mid.split(':')[0])[mid]
            self.assertIn('$$エコーズ$$',row['text'])
            if row['status']=='needs_review':
                with self.assertRaises(ValueError):vi.text(mid)
            else:
                self.assertEqual(vi.text(mid),row['text'])


if __name__=='__main__':unittest.main()
