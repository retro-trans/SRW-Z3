"""Execute actual PPC for bonus centering; no game files written."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
import bonus_centering as B
import eboot
import president_report_layout as W
import trdata
from test_president_report_layout import execute, style, expected_width


class BonusCenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.19_english_20260924_r3')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        trdata.use_glossary('analysis/glossary.json')
        cls.hooks = eboot.load_ui_hook()

    def test_all_single_line_bonus_centers_and_registers(self):
        self.assertEqual(len(B.rows()), 110)
        examples = [(jp, en) for _,jp,en in B.rows()] + [(B.LOCK, self.hooks[B.LOCK])]
        with patch.object(eboot, 'load_ui_hook', return_value=self.hooks):
            for jp,en in examples:
                for quad,pitch in [(23,23), (25,40), (31,35)]:
                    s = style(quad,pitch)
                    dest,x = execute(self.mapping,self.widths,jp.encode('cp932'),s)
                    self.assertEqual(dest, eboot.NAME_SITE, jp)
                    raw = eboot._encode_marked(en,self.mapping)
                    self.assertAlmostEqual(x + expected_width(raw,self.widths,s)/2,640,places=4)

    def test_nonmatching_multiline_and_wrong_encoding_fall_back(self):
        from bonus_descriptions import hooks
        cases = [b'Unrelated message', b'', (B.rows()[0][1]+'!').encode('cp932')]
        cases += [jp.encode('cp932') for jp,en in hooks().items() if '\n' in jp or '\n' in en]
        with patch.object(eboot, 'load_ui_hook', return_value=self.hooks):
            for raw in cases:
                self.assertEqual(execute(self.mapping,self.widths,raw,style(25,40)), (W.SITE+4,640))
            self.assertEqual(execute(self.mapping,self.widths,B.LOCK.encode('cp932'),style(25,40),0), (W.SITE+4,640))

    def test_source_pointer_keys_and_cave_budget(self):
        source = Path('work/EBOOT_dec.elf').read_bytes()
        for va,jp,_ in B.rows():
            key=jp.encode('cp932')+b'\0'
            self.assertEqual(source[va-0x10000:va-0x10000+len(key)],key)
        self.assertLessEqual(W.CAVE + len(W.stub(self.mapping,True)), W.DATA)
        self.assertLessEqual(W.DATA + len(W.regions(self.mapping,True)[2][1]),W.END)


if __name__ == '__main__':
    unittest.main()
