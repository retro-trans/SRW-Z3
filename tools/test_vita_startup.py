"""Source-matched startup labels and isolated native heading graphics."""
from pathlib import Path
import sys
import unittest
from unittest import mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import startup_art as A
import ui_text as U
from category_port import Port,encoded


class StartupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from category_port import SOURCE
        if not SOURCE.exists():raise unittest.SkipTest('Private audited Vita source required')
        cls.port=Port();cls.rows={}
        def capture(original,widths,rows,**kwargs):cls.rows.update(rows);return b'',{}
        with mock.patch.object(U,'patch',side_effect=capture):
            _,cls.audit=U.prepare(cls.port)
        k=cls.port.cpk(A.ARCHIVE);cls.raw=k.read(next(e for e in k.files if e['id']==A.MEMBER))
        cls.changed,cls.art=A.apply(cls.raw,cls.port.catalog)

    def test_all_startup_text_labels_and_default_names_have_native_keys(self):
        defs=self.port.catalog.document('localization/messages/ui_aiddata.json')['messages']
        verified=0
        for mid,row in defs.items():
            text=self.port.catalog.text(mid)
            if mid.endswith(('_heading','_format')) or any(0xe000<=ord(c)<=0xf8ff for c in text):continue
            self.assertEqual(self.rows[row['source'].encode('cp932')],encoded(text,self.port.mapping),mid)
            verified+=1
        self.assertEqual(verified,13)
        self.assertEqual(self.rows['ヒビキ'.encode('cp932')],encoded('Hibiki',self.port.mapping))
        self.assertEqual(self.rows['カミシロ'.encode('cp932')],encoded('Kamishiro',self.port.mapping))

    def test_headings_only_change_two_observed_word_cells(self):
        start,pal=A.layout(self.raw)
        allowed={start+A.pixel(x+xx,y+yy) for x,y,w,h,mid in A.ROWS for yy in range(h) for xx in range(w)}
        changed={i for i,(a,b) in enumerate(zip(self.raw,self.changed)) if a!=b}
        self.assertTrue(changed);self.assertTrue(changed<=allowed)
        self.assertEqual(self.raw[pal:pal+1024],self.changed[pal:pal+1024])
        self.assertEqual(len(self.raw),len(self.changed))
        for x,y,w,h,mid in A.ROWS:
            offsets={start+A.pixel(x+xx,y+yy) for yy in range(h) for xx in range(w)}
            self.assertTrue(changed&offsets)
            bbox=A.tile(self.port.catalog.text(mid),w,h).getchannel('A').getbbox()
            self.assertGreaterEqual(bbox[0],3);self.assertLessEqual(bbox[2],w-3)

    def test_morton_is_bijective_and_source_guard_rejects_repatch(self):
        self.assertEqual(len({A.pixel(x,y) for y in range(512) for x in range(512)}),512*512)
        with self.assertRaises(ValueError):A.apply(self.changed,self.port.catalog)
        with self.assertRaises(ValueError):A.apply(self.raw[:-1],self.port.catalog)

    def test_build_consumer_receives_only_expected_member(self):
        with mock.patch.object(self.port,'emit') as sink:
            audit=A.prepare(self.port)
        sink.assert_called_once_with(A.ARCHIVE,A.MEMBER,self.changed)
        self.assertFalse(audit['runtime_tested'])


if __name__=='__main__':unittest.main()
