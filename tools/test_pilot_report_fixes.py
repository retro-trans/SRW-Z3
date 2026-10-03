"""October pilot name/Spirit-card/link-spacing screenshot regressions."""
import json
from pathlib import Path
import struct
import unittest

import aiddata
import check_stage
from check_search_layout import execute
from cpk import CPK
import digraph
import eboot
import localization
import pilot_name_layout as layout
import rpw
import search_layout
import terms

ROOT = Path('work/build_0.6.24_english_20260930')


class PilotReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cat = localization.english()
        cls.terms = json.loads(Path('analysis/glossary.json').read_text(encoding='utf8'))['terms']
        cls.mapping = json.loads((ROOT/'pairs.json').read_text())
        cls.elf = (ROOT/'EBOOT.BIN').read_bytes()
        cls.segs = eboot._segments(cls.elf)
        at = eboot._off(cls.segs, eboot.TABLE_VA)
        cls.widths = cls.elf[at:at+eboot.ATLAS_CELLS]
        k = CPK('work/lib/RPW_DATA.CPK'); cls.source = k.read(k.files[0])
        k = CPK('work/orig/AIDDATAPACK.CPK'); cls.ui = k.read(k.files[0])

    def test_hilde_and_link_spacing(self):
        for mid in ('glossary:r_94c2a0c1f414ed06', 'library.pt_080:r_03d41715b84571fa'):
            self.assertEqual(self.cat.text(mid), 'Hilde Schbeiker')
        self.assertEqual(self.cat.text('name_pieces:r_b26eb2c380dfc726'), 'Schbeiker')
        ids = ('stage0025_03:r_4ae9c4bd77494c4a', 'stage0025_03:r_3c9956c9d519d2a2')
        values = {mid:self.cat.text(mid) for mid in ids}
        self.assertIn('the 《$$ホワイトファング$$》 and', values[ids[0]])
        self.assertIn('new 《$$ＰＳ$$》 there', values[ids[1]])
        self.assertTrue(check_stage.widths_ready())
        index = terms.index({'terms': self.terms})
        self.assertEqual(check_stage.check(
            [{'sha':mid, 'jp':self.cat.definition(mid)['source']} for mid in ids],
            values, mapping=self.mapping, term_idx=index), [])

    def test_surname_status_separator_and_nickname_isolation(self):
        overrides = rpw.surname_first_overrides(self.source, self.terms)
        self.assertEqual(len(overrides), 104)
        for rec in (590, 613):
            self.assertEqual(overrides['pilot-nw',rec,1], 'Akagi ')
            self.assertEqual(overrides['pilot-nw',rec,2], 'Shunsuke')
        self.assertTrue(all(col in (1,2) for _,_,col in overrides))
        encoded = {key:digraph.encode_mixed(value,self.mapping) for key,value in overrides.items()}
        after,_ = rpw.build_grown(self.source,{},encoded)
        def strings(blob):
            _,_,start,end,_ = next(c for c in rpw.chunks(blob) if c[0]=='j-string')
            return blob[start:end].split(b'\0')
        before_strings,after_strings = strings(self.source),strings(after)
        old_slots,new_slots = rpw.slots(self.source),rpw.slots(after)
        for key in old_slots:
            self.assertEqual(after_strings[new_slots[key]],
                             encoded.get(key,before_strings[old_slots[key]]), key)

    def test_spirit_card_measured_center_and_copies(self):
        layout.check_ui(self.ui)
        self.assertEqual(aiddata.refs(self.ui)[aiddata.STR_BASE+layout.REFERENCE], [layout.ROW])
        data = self.ui[layout.ROW:layout.ROW+32]
        center = (struct.unpack_from('>f',data,4)[0]+1)*640
        self.assertAlmostEqual(center,167.5)
        name = self.cat.text('glossary:r_c1022288dcebcde2')
        self.assertEqual(name,'Commander Tanaka')
        raw = digraph.encode_mixed(name,self.mapping)
        self.assertEqual(center-len(raw)//2*25/2, -32.5)
        width = sum(self.widths[digraph.cell_index(int.from_bytes(raw[i:i+2],'big'))]
                    for i in range(0,len(raw),2))*25/32
        for copy in (None, data[:12]+bytes.fromhex('60ff60ff')+data[16:]):
            pc,x = execute(search_layout.stub(),self.widths,raw,layout.ROW,center,
                           (25,25,24),mode=0,record_data=data,copied=copy)
            self.assertEqual(pc,0x140f4)
            self.assertAlmostEqual(x+width/2,center)
            self.assertGreaterEqual(x,46)
            self.assertLessEqual(x+width,288)
        print('Spirit card: full Tanaka label %.2fpx; centered x=%.2f..%.2f' %
              (width,center-width/2,center+width/2))

    def test_old_build_reproduces_offset_and_unrelated_fallback_stays(self):
        code = search_layout.stub()
        self.assertLessEqual(len(code),0x400)
        at = eboot._off(self.segs,search_layout.CAVE)
        raw = digraph.encode_mixed('Commander Tanaka',self.mapping)
        data = self.ui[layout.ROW:layout.ROW+32]
        self.assertEqual(execute(self.elf[at:at+0x400],self.widths,raw,layout.ROW,
                                167.5,(25,25,24),mode=0,record_data=data), (0x14954,167.5))
        for value in (b'ASCII','？？？？'.encode('cp932')):
            self.assertEqual(execute(code,self.widths,value,layout.ROW,167.5,
                                    (25,25,24),record_data=data), (0x14954,167.5))
        unrelated = 0xb0d14
        self.assertEqual(execute(code,self.widths,raw,unrelated,167.5,(25,25,24),
                                record_data=self.ui[unrelated:unrelated+32]), (0x14954,167.5))
        changed = bytearray(self.ui); changed[layout.ROW+19] ^= 1
        with self.assertRaises(AssertionError): layout.check_ui(changed)

    def test_raw_and_hardware_layout_permissions(self):
        import sys
        import ppc_permissions
        sys.path.insert(0,'platforms/ps3')
        import cfw_loader_layout
        # Throwaway memory only: leave all game/build files untouched.
        after = bytearray(self.elf)
        at = eboot._off(self.segs,search_layout.CAVE)
        code = search_layout.stub()
        after[at:at+len(code)] = code
        self.assertEqual(after[at+0x400:at+0x500], self.elf[at+0x400:at+0x500])
        pristine = Path('work/EBOOT_dec.elf').read_bytes()
        ppc_permissions.check_changed_branches(pristine,bytes(after))
        folded = cfw_loader_layout.fold(bytes(after))
        ppc_permissions.check_changed_branches(pristine,folded)
        pos = eboot._off(eboot._segments(folded),search_layout.CAVE)
        self.assertEqual(folded[pos:pos+len(code)],code)


if __name__ == '__main__':
    unittest.main()
