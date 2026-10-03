"""Compound name records and Spirit panel layout, using read-only fixtures."""
from pathlib import Path
import json
import struct
import unittest
from cpk import CPK
import digraph
import rpw
import trdata
import pilot_spirit_layout as S


def strings(blob):
    _, _, start, end, _ = next(c for c in rpw.chunks(blob) if c[0] == 'j-string')
    return blob[start:end].split(b'\0')


class PilotStatusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.terms = trdata._load('analysis/glossary.json')['terms']
        root = Path('work/build_0.6.20_english_20260925_r2')
        cls.mapping = json.loads((root/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        k = CPK('work/lib/RPW_DATA.CPK')
        cls.rpw = k.read(k.files[0])
        k = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = k.read(k.files[0])
        k = CPK(str(root/'AIDDATAPACK.CPK'))
        cls.current_ui = k.read(k.files[0])
        k = CPK(str(root/'RPW_DATA.CPK'))
        cls.current_rpw = k.read(k.files[0])

    def test_compound_category_and_canonical_spelling(self):
        override = rpw.compound_name_overrides(self.rpw, self.terms)
        self.assertEqual(len(override), 30)
        for rec in (858, 859, 860, 897, 898, 899):
            self.assertEqual(override['pilot-nw',rec,2], 'Asuka Langley')
            self.assertEqual(override['pilot-nw',rec,1], 'Shikinami')
        for rec in (861, 862, 900):
            self.assertEqual(override['pilot-nw',rec,2], 'Mari Illustrious')
            self.assertEqual(override['pilot-nw',rec,1], 'Makinami')
        self.assertFalse(any(col == 0 for _,_,col in override))
        # Changing the canonical full name, not a second literal, drives output.
        terms = [dict(t, en='Asuka Example Shikinami') if t['jp']=='式波・アスカ・ラングレー'
                 else t for t in self.terms]
        self.assertEqual(rpw.compound_name_overrides(self.rpw,terms)['pilot-nw',858,2], 'Asuka Example')

    def test_rpw_fix_composes_without_touching_other_slots(self):
        overrides = rpw.compound_name_overrides(self.rpw,self.terms)
        overrides.update(rpw.surname_first_overrides(self.rpw,self.terms))
        encoded = {k:digraph.encode_mixed(v,self.mapping) for k,v in overrides.items()}
        # Test both pristine data and the current installed translation.
        for before in (self.rpw,self.current_rpw):
            after, _ = rpw.build_grown(before,{},encoded)
            rpw.check_compound_names(self.rpw,after,self.terms,self.mapping)
            old_text,new_text = strings(before),strings(after)
            old_slots,new_slots = rpw.slots(before),rpw.slots(after)
            for key in old_slots:
                if key not in overrides:
                    self.assertEqual(old_text[old_slots[key]],new_text[new_slots[key]],key)

    def test_spirit_layout_all_names_and_both_sheets(self):
        for before in (self.ui,self.current_ui):
            after = S.apply(before,self.mapping,self.widths,self.ui)
            allowed = {p for name,cost in S.ROWS
                       for p in (*range(name+16,name+22),*range(cost+4,cost+8))}
            self.assertEqual(len(before),len(after))
            self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(before,after))))
            for name,cost in S.ROWS:
                self.assertEqual(before[name:name+16],after[name:name+16])
                self.assertEqual(before[name+21:name+32],after[name+21:name+32])
                self.assertEqual(before[cost:cost+4],after[cost:cost+4])

    def test_layout_source_guard(self):
        changed = bytearray(self.ui)
        changed[S.ROWS[0][0]+19] ^= 1
        with self.assertRaises(AssertionError):
            S.apply(changed,self.mapping,self.widths,self.ui)
        changed = bytearray(self.ui)
        struct.pack_into('>I',changed,S.ROWS[1][1],0)
        with self.assertRaises(AssertionError):
            S.apply(changed,self.mapping,self.widths,changed)


if __name__ == '__main__':
    unittest.main()
