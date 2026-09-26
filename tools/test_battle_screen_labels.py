"""Read-only source checks and in-memory patches; no game build/install."""
import json
from pathlib import Path
import struct
import unittest
from cpk import CPK
import eboot
import battle_screen_labels as b
import weapon_requirements
import rpw
import digraph


class BattleScreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.15_hardware_source_20260919')
        cls.mapping = json.loads((root/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        cpk = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = cpk.read(next(e for e in cpk.files if e['id']==0))
        cpk = CPK(str(root/'AIDDATAPACK.CPK'))
        cls.built_ui = cpk.read(next(e for e in cpk.files if e['id']==0))
        cls.elf = Path('work/EBOOT_dec.elf').read_bytes()

    def test_ui_only_registered_pointers_change(self):
        new = b.apply(self.ui,self.mapping,self.widths)
        allowed = {p for row,_,_ in b.ROWS for p in range(row,row+4)}
        self.assertTrue(all(x==y or i in allowed for i,(x,y) in enumerate(zip(self.ui,new))))
        for row,_,_ in b.ROWS:
            self.assertEqual(self.ui[row+4:row+32],new[row+4:row+32])
        self.assertGreater(len(new),len(self.ui))

    def test_reject_changed_source(self):
        data = bytearray(self.ui)
        struct.pack_into('>I',data,b.ROWS[0][0],0)
        with self.assertRaises(AssertionError):
            b.apply(data,self.mapping,self.widths)

    def test_requirement_widgets_already_english_in_015(self):
        weapon_requirements.check(self.built_ui,self.mapping,self.widths)

    def test_utf8_relocation_and_lookup_key_isolation(self):
        data = bytearray(self.elf)
        b.check_source_elf(data)
        eboot.add_segment(data)
        segs = eboot._segments(data)
        cur = eboot._off(segs,eboot.NAME_STR)
        result = eboot.command_labels(data,segs,b.utf8_labels(),cur,self.mapping,self.widths,window=False)
        # Misato and Toji fit their original 16-byte slots; the other three relocate.
        self.assertEqual(result[:3],(2,3,[]))
        b.check_elf(data,self.mapping)
        table = eboot.unicode_table(self.elf,eboot._segments(self.elf))
        allowed = {p for _,_,refs in b.UTF8_BINDINGS for ref in refs for p in range(ref,ref+4)}
        allowed.update(range(0x6dd090,0x6dd0a0))
        allowed.update(range(0x6dd118,0x6dd128))
        allowed.update(range(table+2*0x120,table+2*0x17f))
        ext_header = next(s['hdr'] for s in segs if s['va']==eboot.EXT_VA)
        allowed.update(range(ext_header,ext_header+56))
        self.assertTrue(all(x==y or i in allowed for i,(x,y) in enumerate(zip(self.elf,data))))

    def test_reject_changed_name_table(self):
        for _,_,refs in b.UTF8_BINDINGS:
            data = bytearray(self.elf)
            struct.pack_into('>I',data,refs[0],0)
            with self.assertRaises(AssertionError):
                b.check_source_elf(data)

    def test_utf8_loader_uses_glossary(self):
        names = b.utf8_names()
        self.assertEqual(names,{'鉄人':'Tetsujin','ミサト':'Misato','トウジ':'Toji'})
        loaded = eboot.load_commands(eboot.UI_UTF8_FILE)
        for jp,en in b.utf8_labels().items():
            self.assertEqual(loaded[jp],en)

    def test_toji_battle_name_missing_from_015(self):
        data = Path('work/build_0.6.15_hardware_source_20260919/EBOOT.BIN').read_bytes()
        segs = eboot._segments(data)
        va = struct.unpack_from('>I',data,0x84e1c8)[0]
        self.assertEqual(eboot._cstr(data,eboot._off(segs,va)),'トウジ'.encode('utf-8'))

    def test_015_reported_long_names_are_complete_in_rpw(self):
        original = CPK('work/lib/RPW_DATA.CPK')
        old = original.read(original.files[0])
        built = CPK('work/build_0.6.15_hardware_source_20260919/RPW_DATA.CPK')
        new = built.read(built.files[0])
        originals = rpw.jstrings(old)
        starts, _ = rpw._starts(new)
        _, _, body_offset, body_end, _ = next(c for c in rpw.chunks(new) if c[0] == 'j-string')
        body = new[body_offset:body_end]
        new_slots = rpw.slots(new)
        names = {'ネオ・ジオン兵':'Neo Zeon Soldier','第４の使徒':'the Fourth Angel',
                 'マリーメイア兵':'Mariemaia Soldier'}
        found = {jp:0 for jp in names}
        for slot,index in rpw.slots(old).items():
            jp = originals[index]
            if slot[0] == 'pilot-nw' and jp in names:
                offset = starts[new_slots[slot]]
                expected = digraph.encode_mixed(names[jp],self.mapping)
                self.assertEqual(body[offset:body.index(b'\0',offset)],expected)
                found[jp] += 1
        self.assertTrue(all(count>0 for count in found.values()))

    def test_current_sync_label_still_needs_translation(self):
        from intermission_layout import text
        self.assertEqual(text(self.built_ui,0x9e394),'シンクロ率'.encode('cp932'))

    def test_barrier_help_keeps_two_lines_and_final_newline(self):
        en = b.utf8_labels()[b.localization.english().definition(b.HELP_ID)['source']]
        self.assertEqual(en.count('\n'),2)
        self.assertTrue(en.endswith('\n'))

    def test_sword_help_keeps_conditional_parry_and_two_lines(self):
        en = b.localization.message(b.SWORD_HELP_ID)
        self.assertEqual(en.count('\n'), 2)
        self.assertTrue(en.endswith('\n'))
        self.assertIn('may parry certain enemy attacks', en)


if __name__ == '__main__':
    unittest.main()
