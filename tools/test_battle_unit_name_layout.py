"""Execute the emitted PPC against shipped font metrics and name templates."""
import json
import struct
import unittest
from pathlib import Path

import aiddata
import battle_unit_name_layout as names
import digraph as dg
import eboot
import search_layout
from check_search_layout import execute,check
from cpk import CPK

ROOT=Path('work/build_0.6.23_english_20260929')


class UnitNameCenteringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping=json.loads((ROOT/'pairs.json').read_text())
        cls.elf=(ROOT/'EBOOT.BIN').read_bytes()
        cls.original=Path('work/EBOOT_dec.elf').read_bytes()
        cls.segs=eboot._segments(cls.elf)
        at=eboot._off(cls.segs,eboot.TABLE_VA)
        cls.widths=cls.elf[at:at+eboot.ATLAS_CELLS]
        k=CPK('work/orig/AIDDATAPACK.CPK');cls.ui=k.read(k.files[0])
        k=CPK(str(ROOT/'AIDDATAPACK.CPK'));cls.built_ui=k.read(k.files[0])
        cls.code=search_layout.stub()

    def test_complete_centered_template_inventory_and_unique_references(self):
        names.check_ui(self.ui);names.check_ui(self.built_ui)
        refs=aiddata.refs(self.ui)
        found=set()
        jp='ニルヴァーシュｔｙｐｅＺＥＲＯ'
        for p,t,_,_ in aiddata.strings(self.ui):
            if t==jp:
                for r in refs.get(p,[]):
                    if self.ui[r+23]&0xc0==0x40:found.add(r)
        self.assertEqual(found,set(names.TEMPLATES))
        for row,(ref,_) in names.TEMPLATES.items():
            self.assertEqual(refs[aiddata.STR_BASE+ref],[row])

    def test_full_names_centered_in_all_templates_and_copies(self):
        examples=('Evangelion Unit-00 (Kai)','Gurren Lagann',
                  'Dancouga Nova Max God','VF-25F Messiah (Alto)',
                  'Lancelot Albion','Gunleon','M','Wiii')
        for row in names.TEMPLATES:
            data=self.ui[row:row+32]
            for name in examples:
                raw=dg.encode_mixed(name,self.mapping)
                cells=[int.from_bytes(raw[i:i+2],'big') for i in range(0,len(raw),2)]
                for size in (23,25,28):
                    width=sum(self.widths[dg.cell_index(c)] for c in cells)*size/32
                    for copied in (None,data[:12]+bytes.fromhex('60ff60ff')+data[16:]):
                        pc,x=execute(self.code,self.widths,raw,row,900.,(size,)*3,
                                     mode=0,copied=copied,record_data=data)
                        self.assertEqual(pc,eboot.NAME_SITE)
                        self.assertAlmostEqual(x+width/2,900.,places=4)

    def test_screenshot_fixed_cell_error_and_new_width(self):
        row=0x9d7d4;data=self.ui[row:row+32]
        raw=dg.encode_mixed('Evangelion Unit-00 (Kai)',self.mapping)
        at=eboot._off(self.segs,search_layout.CAVE)
        old=self.elf[at:at+len(self.code)]
        self.assertEqual(execute(old,self.widths,raw,row,900.,(25,)*3,
                                 mode=0,record_data=data),(0x14954,900.))
        pc,x=execute(self.code,self.widths,raw,row,900.,(25,)*3,
                     mode=0,record_data=data)
        self.assertEqual(pc,eboot.NAME_SITE)
        self.assertEqual(2*(900-x),306.25)
        self.assertEqual(len(raw)//2*25,600)
        self.assertEqual(x-(900-600/2),146.875)

    def test_all_packed_robot_name_variants(self):
        import rpw
        k=CPK(str(ROOT/'RPW_DATA.CPK'));blob=k.read(k.files[0])
        _,_,start,end,_=next(c for c in rpw.chunks(blob) if c[0]=='j-string')
        strings=blob[start:end].split(b'\0')
        variants={strings[i] for key,i in rpw.slots(blob).items() if key[0]=='robot'}
        row=0x9d7d4;data=self.ui[row:row+32];measured=0
        for raw in variants:
            valid=len(raw)%2==0
            cells=[int.from_bytes(raw[i:i+2],'big') for i in range(0,len(raw),2)]
            valid=valid and all(0x81<=c>>8<=0x97 and 0x40<=c&255<=0xfc
                               and dg.cell_index(c)<eboot.ATLAS_CELLS
                               and self.widths[dg.cell_index(c)]!=32 for c in cells)
            pc,x=execute(self.code,self.widths,raw,row,900.,(25,)*3,
                         mode=0,record_data=data)
            if valid:
                expected=sum(self.widths[dg.cell_index(c)] for c in cells)*25/32
                self.assertEqual(pc,eboot.NAME_SITE)
                self.assertAlmostEqual(x+expected/2,900.,places=4)
                measured+=1
            else:self.assertEqual((pc,x),(0x14954,900.))
        self.assertGreater(measured,200)
        print('PASS: %d distinct packed unit names, %d VWF-centered.'%(len(variants),measured))

    def test_unknown_hidden_and_unrelated_labels_retain_fallback(self):
        row=0x9d7d4;data=self.ui[row:row+32]
        for raw in ('？？？？'.encode('cp932'),'日本'.encode('cp932'),b'ASCII',b'\x81'):
            self.assertEqual(execute(self.code,self.widths,raw,row,900.,(25,)*3,
                                     record_data=data),(0x14954,900.))
        raw=dg.encode_mixed('Evangelion Unit-00 (Kai)',self.mapping)
        for row in (0xb0d14,0x9d434,0x9d3b4):
            self.assertEqual(execute(self.code,self.widths,raw,row,900.,(25,)*3,
                                     record_data=self.ui[row:row+32]),(0x14954,900.))

    def test_existing_grid_tabs_and_permission_gate(self):
        import ppc_permissions
        # Install the enlarged hook only into a throwaway in-memory image.
        out=bytearray(self.elf)
        at=eboot._off(self.segs,search_layout.CAVE)
        out[at:at+0x400]=bytes(0x400)
        out[at:at+len(self.code)]=self.code
        check(bytes(out),self.mapping,self.built_ui)
        ppc_permissions.check_changed_branches(self.original,bytes(out))


if __name__=='__main__':unittest.main()
