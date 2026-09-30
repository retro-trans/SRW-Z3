"""Upgrade rank overlap regression; source-only, no game installation."""
import json
import struct
import unittest
from pathlib import Path

from cpk import CPK
import aiddata
import digraph as dg
import upgrade_list_labels as labels
from intermission_layout import text,ink


class UpgradeRankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.23_english_20260929')
        k=CPK('work/orig/AIDDATAPACK.CPK');cls.source=k.read(k.files[0])
        k=CPK(str(root/'AIDDATAPACK.CPK'));cls.shipped=k.read(k.files[0])
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cls.fixed=labels.apply(cls.shipped,cls.mapping,cls.widths)

    def test_all_three_native_weapon_rank_pairs_covered(self):
        refs=aiddata.refs(self.source)
        found={r for p,s,_,_ in aiddata.strings(self.source) if s=='武器'
               for r in refs.get(p,[]) if text(self.source,r+32)=='ＲＡＮＫ'.encode('cp932')}
        self.assertEqual(found,{r for r,_ in labels.RANK_PAIRS})

    def test_shipped_panels_reproduce_overlap(self):
        for first,suffix in labels.RANK_PAIRS[1:]:
            self.assertEqual(text(self.shipped,first),'武器'.encode('cp932'))
            self.assertEqual(text(self.shipped,suffix),'ＲＡＮＫ'.encode('cp932'))
            gap=(struct.unpack_from('>f',self.shipped,suffix+4)[0]
                 -struct.unpack_from('>f',self.shipped,first+4)[0])*640
            self.assertAlmostEqual(gap,53,places=3)
            self.assertGreater(ink('Weapon',self.mapping,self.widths,28),gap+50)

    def test_compact_combined_label_and_no_second_draw(self):
        for first,suffix in labels.RANK_PAIRS:
            self.assertEqual(text(self.fixed,first),dg.encode_mixed('Wpn Rank',self.mapping))
            self.assertEqual(text(self.fixed,suffix),b'')
        self.assertEqual(ink('Wpn Rank',self.mapping,self.widths,28),135.625)
        labels.check(self.fixed,self.mapping,self.widths)

    def test_only_label_pointers_change_numeric_and_style_bytes_preserved(self):
        allowed={p for row in labels.ROWS for p in range(row,row+4)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.shipped,self.fixed))))
        for row in labels.ROWS:
            self.assertEqual(self.fixed[row+4:row+32],self.shipped[row+4:row+32])
        # Other RANK captions belong to different controls and must remain.
        for row in (0x99034,0x9c494,0xb2894):
            self.assertEqual(text(self.fixed,row),text(self.shipped,row))
            self.assertEqual(self.fixed[row:row+32],self.shipped[row:row+32])

    def test_output_gate_rejects_return_of_duplicate_suffix(self):
        for _,suffix in labels.RANK_PAIRS:
            bad=bytearray(self.fixed)
            bad[suffix:suffix+4]=self.source[suffix:suffix+4]
            with self.assertRaises(AssertionError):labels.check(bad,self.mapping,self.widths)


if __name__=='__main__':unittest.main()
