import json
from pathlib import Path
import unittest
import tempfile

import build_library
from cpk import CPK
import library_cv
import patch_library_cv_candidate as patch
import zukan


class LibraryCVTests(unittest.TestCase):
    def test_catalog(self):
        catalog = library_cv.load_catalog()
        self.assertEqual(len(catalog), 154)
        self.assertEqual(catalog['池澤春菜'], 'Haruna Ikezawa')
        self.assertEqual(catalog['－－－'], '---')
        self.assertEqual(catalog['神奈延年'], 'Nobutoshi Canna')
        self.assertEqual(catalog['村上龍'], 'Ryu Murakami')

    def test_catalog_is_not_a_battle_dialogue_document(self):
        self.assertFalse(library_cv.CATALOG.match('voice_*.json'))

    def test_unknown_rejected(self):
        with self.assertRaises(ValueError):
            library_cv.romanize('Unknown actor', library_cv.load_catalog())

    def test_longer_credit_roundtrip(self):
        fields = [('ACTR', b'Haruna Ikezawa'), ('VOIC', b'\x00\xff\x5e'),
                  ('DSCR', b'Unchanged'), ('LOOK', b'\x01\x02')]
        self.assertEqual(zukan.parse_ordered(zukan.build('TESTTEST', fields)),
                         ('TESTTEST', fields))

    def test_unrelated_field_change_rejected(self):
        class Archive:
            files = [{'id': 0}]
            def __init__(self, fields):
                self.raw = zukan.build('TESTTEST', fields)
            def read(self, entry):
                return self.raw
        before = Archive([('ACTR', b'old'), ('VOIC', b'original')])
        changed = [('ACTR', b'new'), ('VOIC', b'changed')]
        with self.assertRaisesRegex(ValueError, 'Non-CV'):
            patch.verify(before, Archive(changed), {0: ('TESTTEST', changed)})

    @unittest.skipUnless(patch.SOURCE.exists(), 'requires local game Library')
    def test_complete_source_coverage_and_pooling(self):
        actors = patch.credits(CPK(str(patch.SOURCE)))
        catalog = library_cv.load_catalog()
        self.assertEqual(len(actors), 408)
        self.assertEqual({r[1] for r in actors.values()}, set(catalog))
        texts = list(build_library.collect_texts(str(patch.SOURCE), {'terms': []}, {}))
        self.assertTrue(set(catalog.values()).issubset(texts))
        rendered = list(build_library._rendered(str(patch.SOURCE), {'terms': []}, {}))
        for entry, magic, fields, outputs in rendered:
            index, jp, _ = actors[entry['id']]
            self.assertEqual(outputs[index], catalog[jp])

    @unittest.skipUnless(patch.SOURCE.exists(), 'requires local game Library')
    def test_normal_builder_writes_every_credit(self):
        # Exercise the normal build path independently of the candidate updater.
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'MTZKN_PT.CPK'
            self.assertEqual(build_library.build(str(patch.SOURCE), {'terms': []}, {}, str(output)), 408)
            actual = patch.credits(CPK(str(output)))
            source = patch.credits(CPK(str(patch.SOURCE)))
            catalog = library_cv.load_catalog()
            for fid, (_, jp, _) in source.items():
                self.assertEqual(actual[fid][1], catalog[jp])

    @unittest.skipUnless(patch.TARGET.exists(), 'requires local candidate')
    def test_candidate_only_cv_changes(self):
        source = CPK(str(patch.SOURCE))
        before = CPK(str(patch.BACKUP if patch.BACKUP.exists() else patch.TARGET))
        mapping = json.loads((patch.TARGET.parent / 'pairs.json').read_text())
        widths = {int(k): v for k, v in json.loads((patch.TARGET.parent / 'widths.json').read_text()).items()}
        expected, replacements, audit = patch.plan(source, before, mapping, widths)
        if patch.BACKUP.exists():
            patch.verify(before, CPK(str(patch.TARGET)), expected)
        self.assertEqual(len(audit), 408)
        self.assertLessEqual(max(r['width_at_32px'] for r in audit), 400)


if __name__ == '__main__':
    unittest.main()
