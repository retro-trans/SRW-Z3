"""Lossless catalog migration and multi-language safeguards; no game build."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import localization as L
from migrate_localization import Migration


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.mid = 'example:greeting'
        self.template = {'off':1234,'lines':[{'jp':'原文','en':{'$message':self.mid}}]}
        self.put('localization/manifest.json',dict(schema=1,groups=['example'],languages={'en':{},'fr':{}}))
        self.put('localization/messages/example.json',dict(messages={self.mid:dict(source='原文',kind='ui',tokens=['%s'],links=0)}))
        self.put('localization/locales/en/example.json',dict(messages={self.mid:dict(text='Hello %s',status='imported')}))
        self.put('platforms/ps3/localization/legacy.json',dict(documents={'translation/example.json':dict(format='json',template=self.template)}))
        self.put('platforms/ps3/localization/python.json',dict(literals={'greeting':dict(template={'$join':['Prefix: ',{'$message':self.mid}]})}))
        self.put('translation/example.json',dict(off=1234,lines=[dict(jp='原文',en='Hello %s')]))
        self.put('localization/compatibility.json',dict(files={'translation/example.json':L.sha((self.root/'translation/example.json').read_bytes())}))

    def put(self,name,value):
        path=self.root/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(L.dump(value),encoding='utf-8')

    def french(self,text,status='reviewed'):
        self.put('localization/locales/fr/example.json',dict(messages={self.mid:dict(text=text,status=status)}))

    def test_local_source_not_shipped_in_git_has_actionable_error(self):
        for relative in ('localization/messages/example.json',
                         'platforms/ps3/localization/legacy.json'):
            with self.subTest(relative=relative):
                (self.root/relative).unlink()
                with self.assertRaisesRegex(ValueError, 'docs/LOCAL_SOURCE_DATA.md'):
                    L.Catalog(self.root).document(relative)

    def test_one_message_two_platform_consumers(self):
        catalog=L.Catalog(self.root)
        self.assertEqual(catalog.legacy('translation/example.json')['lines'][0]['en'],catalog.text(self.mid))
        self.assertEqual(catalog.literal('greeting'),'Prefix: Hello %s')
        self.assertEqual(catalog.legacy('translation/example.json')['off'],1234)

    def test_locale_changes_text_not_id_or_bindings(self):
        self.french('Bonjour %s')
        french=L.Catalog(self.root,'fr')
        self.assertEqual(french.text(self.mid),'Bonjour %s')
        self.assertEqual(french.legacy('translation/example.json')['off'],1234)
        self.assertEqual(french.definition(self.mid)['source'],'原文')

    def test_missing_is_not_silent_english(self):
        with self.assertRaisesRegex(ValueError,'Missing fr'):
            L.Catalog(self.root,'fr').text(self.mid)
        self.assertEqual(L.Catalog(self.root,'fr','en').text(self.mid),'Hello %s')

    def test_draft_requires_review_or_explicit_fallback(self):
        self.french('Bonjour %s','needs_review')
        with self.assertRaisesRegex(ValueError,'Unreviewed'):
            L.Catalog(self.root,'fr').text(self.mid)
        self.assertEqual(L.Catalog(self.root,'fr','en').text(self.mid),'Hello %s')

    def test_placeholder_guard(self):
        self.french('Bonjour')
        with self.assertRaisesRegex(ValueError,'Placeholder'):
            L.Catalog(self.root,'fr').text(self.mid)

    def test_glossary_and_link_guards(self):
        self.put('localization/messages/example.json',dict(messages={self.mid:dict(source='原文',kind='dialogue',tokens=['$$人$$'],links=1)}))
        for text in ('《name》', '$$人$$', '《$$人$$'):
            self.french(text)
            with self.assertRaises(ValueError): L.Catalog(self.root,'fr').text(self.mid)
        self.french('《$$人$$》')
        self.assertEqual(L.Catalog(self.root,'fr').text(self.mid),'《$$人$$》')

    def test_unknown_locale_id_detected(self):
        self.put('localization/locales/en/example.json',dict(messages={'example:unknown':dict(text='x')}))
        self.assertTrue(any('Unknown locale ID' in e for e in L.Catalog(self.root).validate()[1]))

    def test_sync_dry_run_then_write_keeps_metadata(self):
        self.put('localization/locales/en/example.json',dict(messages={self.mid:dict(text='Welcome %s',status='reviewed')}))
        before=(self.root/'translation/example.json').read_bytes()
        self.assertEqual(L.sync(self.root),1)
        self.assertEqual((self.root/'translation/example.json').read_bytes(),before)
        self.assertEqual(L.sync(self.root,True),1)
        self.assertEqual(L.Catalog(self.root).check_compatibility(),1)
        self.assertEqual(L.read_json(self.root/'translation/example.json')['off'],1234)

    def test_sync_refuses_unexported_user_edits(self):
        self.put('translation/example.json',{'user':'unrelated change'})
        with self.assertRaisesRegex(ValueError,'Unexported legacy edit'):
            L.sync(self.root,True)
        self.assertEqual(L.read_json(self.root/'translation/example.json'),{'user':'unrelated change'})

    def test_safe_path_rejects_escape(self):
        for name in ('../outside','/absolute','C:/absolute','dir\\outside'):
            with self.assertRaises(ValueError): L.safe_path(self.root,name)

    def test_migration_ids_do_not_depend_on_english(self):
        first,second=Migration(self.root),Migration(self.root)
        self.assertEqual(first.add('test','context','English','日本語'),second.add('test','context','French','日本語'))
        with self.assertRaisesRegex(ValueError,'collision'):
            first.add('test','context','Another','日本語')

    def test_load_external_json_stays_compatible(self):
        self.assertEqual(L.load_legacy(self.root/'translation/example.json'),L.read_json(self.root/'translation/example.json'))

    def cli(self, *arguments):
        original = L.Catalog
        with mock.patch.object(L,'ROOT',self.root), mock.patch.object(L,'Catalog',
                side_effect=lambda **kwargs: original(self.root,**kwargs)), mock.patch('sys.argv',['localization.py']+list(arguments)):
            L.main()

    def test_language_scaffold_dry_run_and_write(self):
        self.cli('add-language','de')
        self.assertFalse((self.root/'localization/locales/de').exists())
        self.cli('add-language','de','--write')
        row=L.read_json(self.root/'localization/locales/de/example.json')['messages'][self.mid]
        self.assertEqual(row,dict(text=None,status='missing'))
        with self.assertRaisesRegex(ValueError,'Missing de'):
            L.Catalog(self.root,'de').text(self.mid)

    def test_locale_export_includes_ui_and_audited_fallback(self):
        out=self.root/'work/fr-review'
        self.cli('export','--language','fr','--fallback','en','--out',str(out))
        self.assertFalse(out.exists())
        self.cli('export','--language','fr','--fallback','en','--out',str(out),'--write')
        self.assertEqual(L.read_json(out/'LOCALIZATION_UI.json')['greeting'],'Prefix: Hello %s')
        self.assertEqual(L.read_json(out/'LOCALIZATION_EXPORT.json')['fallback'],'en')
        self.assertFalse(L.read_json(out/'LOCALIZATION_EXPORT.json')['game_build_ready'])


class ProjectCatalogTests(unittest.TestCase):
    def test_entire_english_catalog_and_compatibility(self):
        catalog=L.Catalog()
        counts,errors=catalog.validate()
        self.assertEqual(errors,[])
        self.assertGreaterEqual(sum(counts.values()),82457)
        self.assertGreaterEqual(catalog.check_compatibility(),475)

    def test_compatibility_receipt_matches_current_exports(self):
        receipt=L.read_json(L.ROOT/'localization/compatibility.json')
        for name,digest in receipt['files'].items():
            self.assertEqual(L.sha((L.ROOT/name).read_bytes()),digest,name)

    def test_vita_groups_are_shared_and_no_offsets_copied(self):
        binding=L.read_json(L.ROOT/'platforms/vita/localization/bindings.json')
        catalog=L.Catalog()
        for group in binding['shared_groups']:
            self.assertIn(group,catalog.manifest['groups'])
        self.assertNotIn('off',binding)
        self.assertNotIn('address',binding)

    def test_vita_opening_reads_neutral_catalog_without_ps3_bindings(self):
        catalog=L.Catalog()
        for group in ('stage0001a','stage0001b_03','stage0001b_04'):
            expected=L.read_json(L.ROOT/('translation/'+group+'.json'))['LINES']
            self.assertEqual(catalog.dialogue_records(group),expected)
        self.assertNotIn('platforms/ps3/localization/legacy.json',catalog.cache)


if __name__=='__main__':
    unittest.main()
