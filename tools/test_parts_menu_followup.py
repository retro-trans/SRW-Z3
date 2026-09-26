import json
import struct
import unittest
from pathlib import Path
from cpk import CPK
import eboot
import digraph as dg
import command_layout as L
import parts_menu_followup as P
import menu_followup as M
from intermission_layout import ink
from check_command_layout import check_blank_cells, check_prep_references
from check_confirmation_tabs import execute


class PartsMenuFollowup(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root=Path('work/build_0.6.12_approved_subtitle')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c=CPK('work/orig/AIDDATAPACK.CPK');cls.ui=c.read(c.files[0])
        cls.source=Path('work/EBOOT_dec.elf').read_bytes()

    def prepared_elf(self):
        b=bytearray(self.source);segs=eboot._segments(b)
        size=segs[1]['off']-segs[0]['off']
        struct.pack_into('>QQ',b,segs[0]['hdr']+32,size,size)
        eboot.add_segment(b);segs=eboot._segments(b)
        eboot.apply_vwf(b,segs,self.widths)
        L.install(b,segs,self.mapping,self.widths)
        return b,segs

    def test_ui_isolation(self):
        out=P.apply(self.ui,self.mapping,self.widths,self.ui)
        allowed={i for r in P.ROWS for i in range(r,r+4)}
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.ui,out))))
        # Prior Z Chips coverage is preserved; no duplicate patch needed.
        prior=M.apply(self.ui,self.mapping,self.widths,self.ui)
        out=P.apply(prior,self.mapping,self.widths,self.ui)
        M.check(out,self.mapping,self.widths,self.ui)

    def test_utf8_popup_references_and_scope(self):
        b,segs=self.prepared_elf()
        labels=eboot.load_commands(eboot.UI_UTF8_FILE)
        family={jp:labels[jp] for jp,en in L.PREP_ROWS.values()}
        result=eboot.command_labels(b,segs,family,eboot._off(segs,eboot.NAME_STR),self.mapping,self.widths,window=False)
        self.assertFalse(result[2],result[2])
        check_prep_references(b,self.source)
        # These glyphs are deliberately present only on this table's labels.
        for off,(jp,en) in L.PREP_ROWS.items():
            self.assertLess(ink(en,self.mapping,self.widths,28),220,en)
            encoded=L.prefix(en).encode('utf8')+''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in en).encode('utf8')+b'\0'
            self.assertEqual(b.count(encoded),1,en)

    def test_all_pad_banks_live_pitch(self):
        b,segs=self.prepared_elf()
        at=lambda va,n: b[eboot._off(segs,va):eboot._off(segs,va)+n]
        extra=((L.CAVE,at(L.CAVE,len(L.stub()))),(L.DATA,at(L.DATA,len(L.LABELS)*8)))
        widths=bytearray(self.widths.get(i,32) for i in range(eboot.ATLAS_CELLS))
        for i,label in enumerate(L.LABELS):
            ink=sum(widths[dg.cell_index(self.mapping[c])] for c in label)
            for pitch in (23,31,37.28,42):
                for quad in (23.3,28,32):
                    origin=115-L.count_coefficient(i)*pitch
                    advance,acc=execute(eboot.vwf_stub(),widths,dg.cell_index(L.CODES[i]),origin,origin,pitch,quad,0,extra)
                    self.assertLess(abs(origin+advance+ink*quad/64-115),.0001)
                    self.assertLess(abs(acc-advance),.0001)
        # Non-pad cells immediately around the extended banks must still
        # use the ordinary font path, not a layout-table index.
        for cell in {dg.cell_index(c) for c in (0x8460,0x846e,0x8470,0x8492,0x889e)} | {dg.cell_index(c) for c in self.mapping.values()}:
            if cell in {dg.cell_index(c) for c in L.CODES}: continue
            advance,acc=execute(eboot.vwf_stub(),widths,cell,0,0,31,28,0,extra)
            expected=31 if widths[cell]==32 else widths[cell]*28/32.
            self.assertLess(abs(advance-expected),.0001)
        check_blank_cells(CPK('work/TPACKPS3.CPK'))


if __name__=='__main__': unittest.main()
