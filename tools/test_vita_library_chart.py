"""Reported library/chart UI, executable aliases and bounded native art."""
import sys,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'platforms/vita'),str(ROOT/'work/vita/python_deps')]
from category_port import Port,encoded
from inspect_vwf import load,segment
from self_decrypt import parse
import ui_text,ui_layout,library_chart


class LibraryChartTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port=Port();cls.exe,cls.audit=ui_text.prepare(cls.port)
        raw,base=segment(cls.exe,parse(cls.exe),1)
        start=int(cls.audit['table_address'],16)-base;cls.rows={}
        for i in range(struct.unpack_from('<I',raw,start)[0]):
            _,k,v=struct.unpack_from('<III',raw,start+4+i*12)
            cls.rows[raw[start+k:raw.index(b'\0',start+k)]]=raw[start+v:raw.index(b'\0',start+v)]

    def test_all_reported_list_names_and_source_series(self):
        wanted=['破界事変','再世戦争','アビス','烙印','アイム','時空震動',
                '特別教育実習生','第２新東京市','新世時空震動','ＵＣＷ','ＡＤＷ',
                '大時空震動','オリジナル','超時空世紀オーガス']
        names={t['jp']:t['en'] for t in self.port.glossary['terms'] if t['en']}
        for jp in wanted:
            with self.subTest(source=jp):
                self.assertEqual(self.rows[jp.encode('cp932')],encoded(names[jp],self.port.mapping))
        for jp,en in [('用語名','Term'),('キャラクター名','Character Name'),('ロボット名','Robot Name'),
                      ('用語事典','Glossary'),('：＜５０音順へ＞',': Kana Order'),('：＜作品順へ＞',': Series Order')]:
            self.assertEqual(self.rows[jp.encode('cp932')],encoded(en,self.port.mapping))

    def test_chart_composition_private_confirm_and_buffers(self):
        original,info=load();rows,edits=library_chart.hooks(self.port,original,info)
        for jp,en in [('第１話','Episode 1'),('『禁忌という名の希望』','『A Hope Called Taboo』'),
                      ('：スピードＵＰ',': Speed Up'),(library_chart.ALIAS,': OK')]:
            self.assertEqual(self.rows[jp.encode('cp932')],encoded(en,self.port.mapping))
        old,base=segment(original,info,0);new,_=segment(self.exe,parse(self.exe),0)
        self.assertEqual(len(edits),1)
        self.assertEqual(new[0x8126DB68-base:0x8126DB70-base],b'~COK\0\0\0\0')
        # Original metadata, format/digit fragments and navigation code are
        # unchanged. No expanded English is copied into the 128-byte buffers.
        for a,b in [(0x810B2F00,0x810B31A0),(0x810C006A,0x810C0238),
                    (0x81271AF8,0x81271B70),(0x8126DB70,0x8126DB90)]:
            self.assertEqual(new[a-base:b-base],old[a-base:b-base])
        olddata,_=segment(original,info,1);newdata,_=segment(self.exe,parse(self.exe),1)
        self.assertEqual(newdata[:len(olddata)],olddata)

    def test_real_native_drawer_for_reported_labels(self):
        from test_vita_ui_text import UiExecutableTests
        cases=[('破界事変','Destruction Incident'),('オリジナル','Original'),
               ('第１話','Episode 1'),
               ('：スピードＵＰ',': Speed Up'),(library_chart.ALIAS,': OK')]
        runner=UiExecutableTests();runner.candidate=self.exe;runner.port=self.port
        for jp,en in cases:
            # Native SJIS mode used by the chart and native list draws.
            expected=[];x=100
            for ch in en:
                expected.append((1152+(self.port.mapping[ch]&255)-64,x))
                x+=self.port.widths[ch]*24/32
            runner.draw(jp.encode('cp932'),1,expected=expected)

    def test_chart_art_changes_only_letter_regions(self):
        cpk=self.port.cpk(library_chart.ARCHIVE)
        from scene_art import Page
        for fid,(g,sha) in library_chart.SOURCES.items():
            raw=cpk.read(next(e for e in cpk.files if e['id']==fid))
            changed,audit=library_chart.apply(raw,fid,self.port.catalog)
            restored=bytearray(changed)
            for region in audit['regions']:
                page=Page(raw,g,region['texture']);x,y,w,h=region['rectangle']
                for yy in range(y,y+h):
                    at=page.address(x,yy);restored[at:at+w]=raw[at:at+w]
            self.assertEqual(bytes(restored),raw)
            # The complete icon strip and chart panel shapes stay exact.
            for index in [1]:
                a=Page(raw,g,index).image();b=Page(changed,g,index).image()
                self.assertEqual(a.crop((640,0,1280,720)).tobytes(),b.crop((640,0,1280,720)).tobytes())


if __name__=='__main__':unittest.main()
