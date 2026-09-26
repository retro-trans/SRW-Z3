"""Execute the actual date-card call and both native font modes on all 77 dates."""
import gc
import json
from pathlib import Path
import struct
import sys
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'platforms/vita'))
import date_card_centering as D
from category_port import Port
from inspect_vwf import segment
from self_decrypt import parse
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *

BASE = ROOT/'work/vita/english_repatch_test16_02/SRW-Z3-Vita-rePatch-test16-hardware-test.zip'


def draw_positions(executable, keys, font_mode):
    gc.collect()
    u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
    info = parse(executable)
    for n in (0, 1):
        data, base = segment(executable, info, n)
        u.mem_map(base, (len(data)+4095)//4096*4096)
        u.mem_write(base, data)
    u.mem_map(0x200000, 0x10000)
    state = 0x8138AA58
    u.reg_write(UC_ARM_REG_C1_C0_2, 0xf << 20)
    u.reg_write(UC_ARM_REG_FPEXC, 1 << 30)
    positions = []

    def number(reg):
        return struct.unpack('<f', struct.pack('<I', u.reg_read(reg)))[0]

    def external(cpu, address, size, user):
        if address == 0x8121DC30:
            data = bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0), 512))
            cpu.reg_write(UC_ARM_REG_R0, data.index(0))
        elif address == 0x81006E10:
            positions.append((number(UC_ARM_REG_S0), number(UC_ARM_REG_S1),
                              number(UC_ARM_REG_S2), bytes(cpu.mem_read(state+0x6c, 2))))
        else:
            return
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    u.hook_add(UC_HOOK_CODE, external)
    for key in keys:
        u.mem_write(state, bytes(0x78))
        for off, value in ((0x14, 40), (0x1c, 39), (0x40, 40), (0x50, 20)):
            u.mem_write(state+off, struct.pack('<f', value))
        u.mem_write(state+0x6c, struct.pack('<H', font_mode))
        u.mem_write(0x201000, key+b'\0')
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.reg_write(UC_ARM_REG_R0, 0x201000)
        u.reg_write(UC_ARM_REG_R1, 1)
        u.reg_write(UC_ARM_REG_R2, 0)
        for reg, value in ((UC_ARM_REG_S0, 640), (UC_ARM_REG_S1, 340), (UC_ARM_REG_S2, .5)):
            u.reg_write(reg, struct.unpack('<I', struct.pack('<f', value))[0])
        saved = {reg: 0x100+reg for reg in (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7)}
        for reg, value in saved.items():
            u.reg_write(reg, value)
        u.emu_start(D.CALL | 1, D.CALL+4, count=200000)
        assert u.reg_read(UC_ARM_REG_PC) == D.CALL+4
        assert u.reg_read(UC_ARM_REG_SP) == 0x208000
        assert all(u.reg_read(reg) == value for reg, value in saved.items())
    return positions


class DateCenterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BASE.exists():
            raise unittest.SkipTest('Private test16 package needed')
        with zipfile.ZipFile(BASE) as archive:
            cls.before = archive.read('rePatch/PCSG00264/eboot.bin')
        cls.after, cls.audit = D.apply(cls.before, 0x812B5E38)
        cls.port = Port()
        definitions = cls.port.catalog.document('localization/messages/date_cards.json')['messages']
        cls.dates = [(row['source'], cls.port.text(cls.port.catalog.text(mid))) for mid, row in definitions.items()]

    def test_all_dates_both_font_modes_centered_with_vertical_and_font_state_unchanged(self):
        self.assertEqual(len(self.dates), 77)
        self.assertTrue(any('April 27' in en for jp, en in self.dates))
        for mode in (0, 1):
            positions = draw_positions(self.after, [jp.encode('cp932') for jp, en in self.dates], mode)
            self.assertEqual(len(positions), 77)
            for (jp, en), (x, y, depth, state) in zip(self.dates, positions):
                width = sum(self.port.widths[ch] for ch in en)*40/32
                self.assertAlmostEqual(x+width/2, 640, places=5, msg=jp)
                self.assertEqual((y, depth, state), (340, .5, struct.pack('<H', mode)))

    def test_reproduces_reported_offset_before_fix(self):
        jp, en = next((jp, en) for jp, en in self.dates if en.endswith('April 27'))
        before = draw_positions(self.before, [jp.encode('cp932')], 1)[0][0]
        after = draw_positions(self.after, [jp.encode('cp932')], 1)[0][0]
        self.assertGreater(before, after)
        self.assertGreater(abs(before-after), 50)
        self.assertEqual(draw_positions(self.before, [jp.encode('cp932')], 0),
                         draw_positions(self.after, [jp.encode('cp932')], 0))

    def test_stub_branches_relocate_with_code(self):
        for shift in (0x1000, 0x230000):
            # Every control-flow target must have a PC-relative branch encoding.
            from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
            md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
            raw = D.stub(D.RESERVATION, 0x812B5E38)
            before = [(i.address, i.mnemonic, i.op_str) for i in md.disasm(raw, D.RESERVATION)]
            after = [(i.address, i.mnemonic, i.op_str) for i in md.disasm(raw, D.RESERVATION+shift)]
            for old, new in zip(before, after):
                if old[1] in ('bl', 'b.w', 'beq'):
                    self.assertEqual(int(new[2].lstrip('#'), 16)-int(old[2].lstrip('#'), 16), shift)

    def test_unknown_date_native_fallback_both_modes(self):
        keys = ['未登録の日付'.encode('cp932')]
        for mode in (0, 1):
            self.assertEqual(draw_positions(self.before, keys, mode), draw_positions(self.after, keys, mode))

    def test_only_call_and_stub_changed_no_data_relocations_or_other_ui_edits(self):
        old_info, new_info = parse(self.before), parse(self.after)
        self.assertEqual(old_info, new_info)
        a, base = segment(self.before, old_info, 0)
        b, _ = segment(self.after, new_info, 0)
        allowed = set(range(D.CALL-base, D.CALL-base+4)) | set(range(
            D.RESERVATION-base, D.RESERVATION-base+self.audit['stub_bytes']))
        self.assertTrue({i for i, (x, y) in enumerate(zip(a, b)) if x != y} <= allowed)
        for n in range(1, len(old_info['infos'])):
            self.assertEqual(segment(self.before, old_info, n), segment(self.after, new_info, n))
        with self.assertRaisesRegex(ValueError, 'already patched'):
            D.apply(self.after, 0x812B5E38)
        with self.assertRaisesRegex(ValueError, 'lookup'):
            D.apply(self.before, 0x812B5E3A)


if __name__ == '__main__':
    unittest.main()
