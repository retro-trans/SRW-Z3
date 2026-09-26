"""Coherent build gates; synthetic bytes only, no package or install writes."""
from pathlib import Path
import sys
import unittest
from unittest import mock
from types import SimpleNamespace

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import build_vwf_zip as B
from category_port import Port


class BuildGates(unittest.TestCase):
    def test_report_rejects_nested_failures_but_allows_documented_gaps(self):
        B.check_report({'status':'partial_member_verified','remaining':865,'issues':[]})
        for report in ({'status':'blocked'},{'members':[{'issues':[{'reason':'bad'}]}]},
                       {'library':[{'status':'blocked'}]}):
            with self.assertRaises(ValueError):B.check_report(report)

    def test_replacements_reject_duplicate_or_mixed_whole_file(self):
        for reverse in (False,True):
            r=B.Replacements()
            r.put('DATA/a.cpk',None if reverse else 1,b'good')
            for member in (None,1):
                with self.assertRaises(ValueError):r.put('DATA/a.cpk',member,b'bad')
        r=B.Replacements();r.put('DATA/a.cpk',1,b'one');r.put('DATA/a.cpk',2,b'two')
        self.assertEqual(r.archives['DATA/a.cpk'],{1:b'one',2:b'two'})

    def test_replacement_paths_and_payload_types_are_guarded(self):
        for path in ('../x','/x','sce_sys/package/work.bin','DATA/../x'):
            with self.assertRaises(ValueError):B.Replacements().put(path,None,b'x')
        with self.assertRaises(ValueError):B.Replacements().put('DATA/a.cpk',0,bytearray(b'x'))

    def test_sink_is_explicit_and_default_adapter_does_not_write(self):
        port=Port.__new__(Port);port.sink=None
        port.emit('DATA/a.cpk',1,b'text')
        sink=mock.Mock();port.sink=sink;port.emit('DATA/a.cpk',1,b'text')
        sink.assert_called_once_with('DATA/a.cpk',1,b'text')

    def test_archive_verification_checks_changed_and_unchanged_members(self):
        def archive(second=b'old'):
            entries=[dict(id=1,offset=0,size=3,extract=3),dict(id=2,offset=3,size=3,extract=3)]
            data=b'new'+second
            return SimpleNamespace(buf=data,files=entries,read=lambda e:data[e['offset']:e['offset']+e['size']])
        for bad in (False,True):
            with mock.patch.object(B,'CPK',side_effect=[archive(),archive(b'BAD' if bad else b'old')]),mock.patch.object(B.cpkpatch,'validate_itoc'):
                if bad:
                    with self.assertRaises(ValueError):B.verify_archive('old','new',{1:b'new'})
                else:self.assertEqual(B.verify_archive('old','new',{1:b'new'})['members_verified'],2)


if __name__=='__main__':unittest.main()
