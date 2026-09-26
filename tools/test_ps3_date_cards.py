"""Every canonical date card, real emitted PPC, font modes and isolation."""
import json,struct,unittest
from pathlib import Path
import eboot,date_card_layout as D,president_report_layout as P
from localization import Catalog
from test_president_report_layout import execute,style,expected_width


class DateCards(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.12_approved_subtitle')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cat=Catalog();defs=cat.document('localization/messages/date_cards.json')['messages']
        cls.rows={v['source'].encode('cp932'):eboot._encode_marked(cat.text(k),cls.mapping) for k,v in defs.items()}
        cls.source=Path('work/ps3_link_background_v2_20260917/installed-backup-01/EBOOT-v2.BIN').read_bytes()
    def test_all_77_cards_center_with_actual_font_modes(self):
        self.assertEqual(len(self.rows),77)
        for raw,rendered in self.rows.items():
            for s in (style(40,40),style(30,40,3),style(30,40,3,(0xb2,))):
                dest,x=execute(self.mapping,self.widths,raw,s,date_cards=True,caller=D.CALL+4,extra_rows=self.rows)
                width=expected_width(rendered,self.widths,s)
                self.assertEqual(dest,eboot.NAME_SITE)
                self.assertAlmostEqual(x+width/2,640,places=4)
                self.assertGreaterEqual(x,0);self.assertLessEqual(x+width,1280)
    def test_original_fails_opt_in_and_other_callers_unchanged(self):
        raw=next(k for k in self.rows if '４月１０日'.encode('cp932') in k)
        s=style(30,40,3)
        self.assertEqual(execute(self.mapping,self.widths,raw,s,caller=D.CALL+4,extra_rows=self.rows),(P.SITE+4,640))
        self.assertEqual(execute(self.mapping,self.widths,raw,s,date_cards=True,caller=0x1234,extra_rows=self.rows),(P.SITE+4,640))
        for text in (b'',b'hello',raw+b'!',raw[:-1],'未知の日付'.encode('cp932')):
            self.assertEqual(execute(self.mapping,self.widths,text,s,date_cards=True,caller=D.CALL+4,extra_rows=self.rows),(P.SITE+4,640))
        self.assertEqual(execute(self.mapping,self.widths,raw,s,cp932=0,date_cards=True,caller=D.CALL+4,extra_rows=self.rows),(P.SITE+4,640))
    def test_only_center_helper_changes_not_dates_font_or_position(self):
        out,ranges=D.apply(self.source,self.mapping)
        self.assertEqual(len(out),len(self.source));D.check(out,self.mapping);P.check(out,self.mapping)
        allowed={i for start,end in ranges for i in range(start,end)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,out))))
        for start,end in ((0x6ef5d0,0x6f0000),(0x6e5048,0x6e5064),(0x13c524,0x13c590)):
            self.assertEqual(self.source[start:end],out[start:end])
        with self.assertRaises(AssertionError):D.apply(out,self.mapping)
        corrupt=bytearray(out);corrupt[ranges[0][0]+100]^=1
        with self.assertRaises(AssertionError):D.check(corrupt,self.mapping)
    def test_president_and_reward_cases_are_unchanged_by_date_opt_in(self):
        for jp in list(P.battle_reports.HOOKS)+list(P.gift_reports.centered_lines()):
            raw=jp.encode('cp932');s=style(30,40,3,(0xb2,))
            self.assertEqual(execute(self.mapping,self.widths,raw,s),execute(self.mapping,self.widths,raw,s,date_cards=True))
    def test_cumulative_update_matches_v3_plus_dates(self):
        import zipfile
        from platforms.ps3 import build_date_card_update as B
        with zipfile.ZipFile('work/ps3_link_background_v3_20260917/SRW-Z3-PS3-RPCS3-link-background-v3-menu-update.zip') as z:
            v3=z.read('PS3_GAME/USRDIR/EBOOT.BIN')
        self.assertEqual(B.patch(self.source,self.mapping)[0],B.patch(v3,self.mapping)[0])
        broken=bytearray(v3);broken[100]^=1
        with self.assertRaises(ValueError):B.patch(broken,self.mapping)


if __name__=='__main__':unittest.main()
