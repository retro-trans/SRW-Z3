"""Currency separators must never intersect growing runtime balances."""
import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
from intermission_layout import text
import deployment_menu_text as layout


class CurrencyCounters(unittest.TestCase):
    def test_all_variants_and_isolation(self):
        root=Path('work/build_0.6.4_support_squads')
        mapping={k if len(k)==1 else tuple(k):v for k,v in
                 json.loads((root/'pairs.json').read_text()).items()}
        widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cpk=CPK('work/orig/AIDDATAPACK.CPK')
        source=cpk.read(next(f for f in cpk.files if f['id']==0))
        patched=layout.apply(source,mapping,widths)
        allowed=set()
        for r in layout.ROWS:
            allowed.update(range(r,r+4))
            if r in layout.HELP:
                allowed.update(range(r+4,r+8));allowed.add(r+23)
        for r in layout.COLONS:allowed.update(range(r+4,r+8))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(source,patched))))
        self.assertEqual(len(layout.CURRENCY_COLONS),6)
        for r in layout.CURRENCY_COLONS:
            self.assertEqual(text(source,r),'：'.encode('cp932'))
            self.assertEqual(text(patched,r),b'')
            # Empty ink cannot overlap any value, including the reported
            # six-digit balance. Numeric widgets themselves are untouched.
            for balance in (0,7,1366,119992,999999,9999999,99999999):
                self.assertFalse(text(patched,r),balance)
            self.assertEqual(source[r+8:r+32],patched[r+8:r+32])
        for r in set(layout.COLONS)-set(layout.CURRENCY_COLONS):
            self.assertEqual(text(patched,r),'：'.encode('cp932'))


if __name__=='__main__':unittest.main()
