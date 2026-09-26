"""Offline review must be honest about missing data and never mutate sources."""
from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
import unittest

import compare_translation as C
import localization as L


class ComparisonTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        definitions, en, fr = {}, {}, {}
        samples = [
            ('normal', '日本語', 'Hello', 'translated', 'available'),
            ('missing', '日本語', None, 'missing', 'available'),
            ('blank', '枠', '', 'translated', 'available'),
            ('unknown', None, 'Existing text', 'imported', 'not_extracted'),
            ('draft', '日本語', 'Draft', 'needs_review', 'available'),
            ('same', 'HP', 'HP', 'imported', 'available'),
            ('term', 'レイ', '$$レイ#333$$', 'translated', 'available'),
            ('broken', '日本語', '$$unknown$$', 'translated', 'available'),
            ('markup', '<script>', '</script><img src=x onerror=alert(1)>', 'translated', 'available'),
        ]
        for key, source, text, status, available in samples:
            mid = 'sample:'+key
            definitions[mid] = dict(source=source, kind='ui', context={}, source_status=available,
                                    tokens=L.TOKEN.findall(text or ''), links=0)
            en[mid] = dict(text=text, status=status)
            fr[mid] = dict(text=None, status='missing')
        fr['sample:term'] = dict(text='$$レイ#333$$', status='translated')
        self.put('localization/manifest.json', dict(schema=1,groups=['sample','glossary'],languages={'en':{},'fr':{}}))
        self.put('localization/messages/sample.json',dict(messages=definitions))
        self.put('localization/locales/en/sample.json',dict(messages=en))
        self.put('localization/locales/fr/sample.json',dict(messages=fr))
        gdefs = {f'glossary:{key}':dict(source='レイ',kind='glossary',context={'kind':'pilot'},
                  source_status='available',tokens=[],links=0) for key in ('ray','rei')}
        self.put('localization/messages/glossary.json',dict(messages=gdefs))
        self.put('localization/locales/en/glossary.json',dict(messages={
            'glossary:ray':dict(text='Ray',status='translated'),
            'glossary:rei':dict(text='Rei',status='translated')}))
        self.put('platforms/ps3/localization/legacy.json',dict(documents={
            'analysis/glossary.json':dict(template=dict(terms=[
                dict(jp='レイ',kind='pilot',zukan_id=168,en={'$message':'glossary:ray'}),
                dict(jp='レイ',kind='pilot',zukan_id=333,en={'$message':'glossary:rei'})]))}))

    def put(self, path, value):
        target=self.root/path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(L.dump(value), encoding='utf-8')

    def rows(self, language='en'):
        return C.collect(L.Catalog(self.root, language), ['sample'])

    def test_flags_are_distinct_and_blank_is_not_missing(self):
        rows={r['id']:r for r in self.rows()}
        for key, flag in [('missing','untranslated'),('blank','blank'),('unknown','source-unavailable'),
                          ('draft','needs-review'),('same','same-as-source'),('broken','invalid')]:
            self.assertIn(flag,rows['sample:'+key]['flags'])
        for key in ('blank','unknown','same'):
            self.assertNotIn('untranslated',rows['sample:'+key]['flags'])
        self.assertEqual(rows['sample:normal']['flags'],[])

    def test_glossary_discriminator_and_no_english_fallback(self):
        en={r['id']:r for r in self.rows()}
        self.assertEqual(en['sample:term']['expanded'],'Rei')
        fr={r['id']:r for r in self.rows('fr')}
        self.assertIsNone(fr['sample:normal']['target'])
        self.assertIsNone(fr['sample:term']['expanded'])
        self.assertIn('Missing locale glossary term',fr['sample:term']['issues'][0])

    def test_search_and_selection(self):
        rows=self.rows()
        self.assertEqual(len(C.select(rows,'untranslated')),1)
        self.assertEqual(len(C.select(rows,search='HELLO')),1)
        self.assertEqual(len(C.select(rows,search='日本語')),4)
        self.assertEqual(len(C.select(rows,search='Rei')),1)
        with self.assertRaisesRegex(ValueError,'No catalog groups'):
            C.collect(L.Catalog(self.root),['no-such-group'])

    def test_description_dictionary_scope_precedence_and_missing_locale(self):
        manifest=L.read_json(self.root/'localization/manifest.json')
        manifest['groups'] += ['skills','spirits','ui.skill_description_catalog']
        self.put('localization/manifest.json',manifest)
        for group, value in [('skills','Skill name'),('spirits','Spirit name')]:
            self.put('localization/messages/'+group+'.json',dict(messages={group+':a':dict(
                source='愛',kind='ui',source_status='available',context={},tokens=[],links=0)}))
            self.put('localization/locales/en/'+group+'.json',dict(messages={group+':a':dict(
                text=value,status='translated')}))
        group='ui.skill_description_catalog';mid=group+':a'
        self.put('localization/messages/'+group+'.json',dict(messages={mid:dict(
            source='愛',kind='ui',source_status='available',context={},tokens=['$$愛$$'],links=0)}))
        for language in ('en','fr'):
            self.put('localization/locales/'+language+'/'+group+'.json',dict(messages={mid:dict(
                text='Use $$愛$$',status='translated')}))
        row=C.collect(L.Catalog(self.root),[group])[0]
        self.assertEqual(row['expanded'],'Use Spirit name')
        self.assertEqual(row['issues'],[])
        row=C.collect(L.Catalog(self.root,'fr'),[group])[0]
        self.assertIn('invalid',row['flags'])
        self.assertIsNone(row['expanded'])
        issues=[]
        self.assertIsNone(C.expand('$$愛$$',C.glossary_index(L.Catalog(self.root)),issues))
        self.assertTrue(issues)  # No cross-category fallback to Spirit names.

    def test_json_cannot_close_script_or_inject_markup(self):
        rows=self.rows();html=C.render(rows,'en')
        self.assertNotIn('</script><img',html)
        self.assertNotIn('innerHTML',html)
        payload=html.split('<script type="application/json" id="data">',1)[1].split('</script>',1)[0]
        self.assertEqual(json.loads(payload)['rows'],rows)
        self.assertIn('textContent',html)

    def run_cli(self,*args):
        with redirect_stdout(io.StringIO()),redirect_stderr(io.StringIO()):
            return C.main(list(args),root=self.root)

    def test_dry_run_new_output_and_no_source_mutation(self):
        before={p:p.read_bytes() for p in self.root.rglob('*.json')}
        out=self.root/'work/review.html'
        self.assertEqual(self.run_cli('--out',str(out)),0)
        self.assertFalse(out.exists())
        self.assertEqual(self.run_cli('--out',str(out),'--write'),0)
        saved=out.read_bytes()
        self.assertEqual(self.run_cli('--out',str(out),'--write'),1)
        self.assertEqual(out.read_bytes(),saved)
        self.assertEqual(before,{p:p.read_bytes() for p in before})

    def test_protected_output_unknown_language_and_category(self):
        self.assertEqual(self.run_cli('--out',str(self.root/'README.md'),'--write'),1)
        out=str(self.root/'work/review.html')
        self.assertEqual(self.run_cli('--out',out,'--language','de'),1)
        self.assertEqual(self.run_cli('--out',out,'--kind','not-a-kind'),1)


if __name__ == '__main__':
    unittest.main()
