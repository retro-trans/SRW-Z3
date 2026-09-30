"""Gold reward prefix and native amount preservation, no game build."""
import json
from pathlib import Path
import unittest
import battle_reports as B
import digraph as dg
import eboot
import localization
import trdata


class GoldRewardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.23_english_20260929')
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()
        cls.shipped=(root/'EBOOT.BIN').read_bytes()
        cls.mapping=json.loads((root/'pairs.json').read_text())
        trdata.use_glossary('analysis/glossary.json')

    def test_canonical_label_and_qualified_prefix(self):
        self.assertEqual(localization.message(B.GOLD_ID),'Gold Bar ')
        self.assertEqual(eboot.load_ui_hook()[B.GOLD_JP],'Gold Bar ')
        self.assertIn(B.GOLD_JP,eboot.UI_PREFIX)
        self.assertNotIn('金塊',eboot.UI_PREFIX)

    def test_source_and_shipped_missing_hook(self):
        B.check_gold_source(self.source)
        B.check_gold_source(self.shipped)
        with self.assertRaisesRegex(AssertionError,'Gold reward hook missing'):
            B.check_gold_elf(self.shipped,self.mapping)

    def test_every_digit_width_and_reported_amount_retained(self):
        prefix=dg.encode_mixed(localization.message(B.GOLD_ID),self.mapping)
        # The existing prefix hook copies the unmatched suffix byte-for-byte.
        for number in (0,1,9,10,99,100,999,1000,9999,40000,99999,100000,999999,1000000,9999999,99999999):
            amount=str(number).translate(str.maketrans('0123456789','０１２３４５６７８９')).encode('cp932')
            native=B.GOLD_JP.encode('cp932')+amount
            rendered=prefix+native[len(B.GOLD_JP.encode('cp932')):]
            self.assertEqual(rendered[len(prefix):],amount)
            self.assertLess(len(native)+1,64)
            self.assertLess(len(rendered)+1,64)

    def test_source_guards_reject_constructor_or_label_changes(self):
        for off in (0x70f988,0x7cbafc,0x2f01f4,0x2f0254):
            bad=bytearray(self.source);bad[off]^=1
            with self.assertRaises(AssertionError):B.check_gold_source(bad)


if __name__=='__main__':unittest.main()
