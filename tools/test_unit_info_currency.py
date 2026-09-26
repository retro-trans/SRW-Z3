import json
from pathlib import Path
import unittest

from cpk import CPK
import unit_info_currency as P


class UnitInfoCurrencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.13_batched_ui')
        cls.mapping = json.loads((root/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c = CPK('work/orig/AIDDATAPACK.CPK')
        cls.pristine = c.read(c.files[0])
        c = CPK(str(root/'AIDDATAPACK.CPK'))
        cls.built = c.read(c.files[0])

    def test_both_variants_and_existing_build_isolation(self):
        for source in (self.pristine, self.built):
            out = P.apply(source,self.mapping,self.widths,self.pristine)
            allowed = {i for pair in P.ROWS for r in pair for i in range(r,r+4)}
            allowed.update(funds+19 for funds,_ in P.ROWS)
            self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(source,out))))
            self.assertEqual(out[P.AMOUNT:P.AMOUNT+32],source[P.AMOUNT:P.AMOUNT+32])

    def test_wrong_source_rejected(self):
        wrong = bytearray(self.pristine)
        wrong[P.ROWS[0][0]:P.ROWS[0][0]+4] = wrong[P.ROWS[0][1]:P.ROWS[0][1]+4]
        with self.assertRaises(AssertionError):
            P.apply(self.built,self.mapping,self.widths,wrong)

    def test_overlong_locale_rejected(self):
        from unittest.mock import patch
        with patch.object(P.localization,'message',return_value='Funds / Z Chips: '*10):
            with self.assertRaises(AssertionError):
                P.apply(self.built,self.mapping,self.widths,self.pristine)


if __name__ == '__main__':
    unittest.main()
