"""Native member identity, text-only edits, shared wording and build handoff."""
from pathlib import Path
import sys
import unittest
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import opening_narration as N
from category_port import Port,encoded,SOURCE
from build_vwf_zip import Replacements


class OpeningNarrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SOURCE.exists():raise unittest.SkipTest('Private audited Vita source required')
        cls.port=Port();k=cls.port.cpk(N.ARCHIVE)
        cls.original=k.read(next(e for e in k.files if e['id']==N.MEMBER))
        cls.changed,cls.audit=N.apply(cls.original,cls.port)

    def test_all_28_rows_use_shared_english_without_exceeding_native_capacity(self):
        self.assertEqual(len(self.audit['rows']),28)
        for row in self.audit['rows']:
            off=row['offset'];en=self.port.text(self.port.catalog.text(row['message']))
            payload=encoded(en,self.port.mapping)
            self.assertEqual(self.changed[off:self.changed.index(b'\0',off)],payload)
            self.assertLessEqual(len(payload),52)
            self.assertNotIn(b'\n',payload)
        self.assertEqual([r['offset'] for r in self.audit['rows'][:4]],[356,440,524,608])

    def test_every_byte_outside_written_text_and_terminator_is_unchanged(self):
        allowed={i for r in self.audit['rows'] for i in range(r['offset'],r['offset']+r['encoded_bytes']+1)}
        changed={i for i,(a,b) in enumerate(zip(self.original,self.changed)) if a!=b}
        self.assertTrue(changed);self.assertTrue(changed<=allowed)
        self.assertEqual(len(self.changed),8000)
        for off in range(N.BASE,len(self.original),N.STRIDE):
            self.assertEqual(self.changed[off+53:off+N.STRIDE],self.original[off+53:off+N.STRIDE])

    def test_changed_source_wrong_member_and_repatch_are_rejected(self):
        k=self.port.cpk(N.ARCHIVE);wrong=k.read(next(e for e in k.files if e['id']==6))
        for data in (wrong,self.changed,self.original[:-1],b'X'+self.original[1:]):
            with self.assertRaises(ValueError):N.apply(data,self.port)

    def test_long_or_multiline_locale_is_rejected_without_truncation(self):
        for value in ('x'*27,'line\nline','$$unknown$$'):
            with mock.patch.object(self.port.catalog,'text',return_value=value),mock.patch.object(self.port,'text',side_effect=lambda x:x):
                with self.assertRaises(ValueError):N.apply(self.original,self.port)

    def test_separate_narration_and_stage_lua_members_coexist_in_build_sink(self):
        replacements=Replacements();replacements.put(N.ARCHIVE,4,b'already translated Lua')
        with mock.patch.object(self.port,'emit',side_effect=replacements.put) as sink:
            report=N.prepare(self.port)
        sink.assert_called_once_with(N.ARCHIVE,7,self.changed)
        self.assertEqual(replacements.archives[N.ARCHIVE][4],b'already translated Lua')
        self.assertEqual(report['records'],28)
        self.assertFalse(report['runtime_tested'])


if __name__=='__main__':unittest.main()
