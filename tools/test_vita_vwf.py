"""Execute the actual generated Thumb hooks, not a Python spacing imitation."""
import hashlib
from pathlib import Path
import struct
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'platforms/vita'))
import vwf
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


def number(value):
    return struct.unpack('<f', struct.pack('<I', value))[0]


class Machine:
    def __init__(self, shift=0, widths=None, data_shift=None):
        self.shift = shift
        if data_shift is None:
            data_shift = shift
        self.scratch = 0x8168C61C + data_shift
        code, self.entries, _ = vwf.stubs(widths or bytes([32]*192), 0x8168C61C)
        self.uc = u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        u.mem_map((vwf.TEXT_END + shift) & ~4095, 4096)
        u.mem_write(vwf.TEXT_END + shift, code)
        # Apply the actual appended format0 relocation, using the loader's
        # R_ARM_REL32 rule with separately chosen code/data load addresses.
        header, addend, offset = struct.unpack('<III', vwf.pen_relocation(0x81000000, 0x812B6000, 0x8168C61C))
        assert header == 0x310
        patch_address = 0x81000000 + shift + offset
        symbol_address = 0x812B6000 + data_shift
        u.mem_write(patch_address, struct.pack('<I', (symbol_address+addend-patch_address) & 0xFFFFFFFF))
        u.mem_map(self.scratch & ~4095, 4096)
        u.mem_write(self.scratch+4,widths or bytes([32]*192))
        u.mem_map(0x200000, 0x10000)
        u.reg_write(UC_ARM_REG_CPSR, 0xA8000030)
        u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.reg_write(UC_ARM_REG_C1_C0_2, 0xF << 20)
        u.reg_write(UC_ARM_REG_FPEXC, 1 << 30)
        self.stop = 0x200000

    def invoke(self, name):
        self.uc.reg_write(UC_ARM_REG_LR, self.stop | 1)
        self.uc.emu_start((self.entries[name] + self.shift) | 1, self.stop, count=500)
        assert self.uc.reg_read(UC_ARM_REG_PC) == self.stop, 'Hook did not return'

    def pen(self):
        return struct.unpack('<f', self.uc.mem_read(self.scratch, 4))[0]


class VwfCpuTests(unittest.TestCase):
    def test_all_bank_widths_and_original_fallback(self):
        widths = bytes(1 + i % 32 for i in range(192))
        for shift in (0, 0x1000000):
            machine = Machine(shift, widths)
            u = machine.uc
            for cell in [0, 1151, 1344, 4479, 65535] + list(range(1152, 1344)):
                with self.subTest(shift=shift, cell=cell):
                    u.reg_write(UC_ARM_REG_R9, cell)
                    u.reg_write(UC_ARM_REG_S18, bits(21.25))
                    u.reg_write(UC_ARM_REG_S19, bits(24))
                    u.reg_write(UC_ARM_REG_S21, bits(31))
                    u.mem_write(machine.scratch, struct.pack('<f', 7.5))
                    machine.invoke('advance')
                    w = widths[cell-1152] if 1152 <= cell < 1344 else 32
                    advance = 31 if w == 32 else w * 24 / 32
                    self.assertAlmostEqual(number(u.reg_read(UC_ARM_REG_S18)), 21.25+advance)
                    self.assertAlmostEqual(machine.pen(), 7.5+advance)
                    self.assertEqual(u.reg_read(UC_ARM_REG_S19), bits(24))
                    self.assertEqual(u.reg_read(UC_ARM_REG_S21), bits(31))

    def test_preserves_live_registers_stack_and_flags(self):
        m = Machine(widths=bytes([10]*192))
        u = m.uc
        regs = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
                UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_S0, UC_ARM_REG_S1]
        for i, reg in enumerate(regs):
            if reg != UC_ARM_REG_SP:
                u.reg_write(reg, 1152 if reg == UC_ARM_REG_R9 else 100+i)
        u.reg_write(UC_ARM_REG_S19, bits(20))
        u.reg_write(UC_ARM_REG_S21, bits(22))
        before = [u.reg_read(reg) for reg in regs]
        flags = u.reg_read(UC_ARM_REG_CPSR) & 0xF8000000
        m.invoke('advance')
        self.assertEqual(before, [u.reg_read(reg) for reg in regs])
        self.assertEqual(flags, u.reg_read(UC_ARM_REG_CPSR) & 0xF8000000)

    def test_four_piece_origins_and_reset(self):
        for name, target, base, col in (
                ('normal', UC_ARM_REG_R11, UC_ARM_REG_R11, UC_ARM_REG_R3),
                ('mode1', UC_ARM_REG_R9, UC_ARM_REG_R9, UC_ARM_REG_R3),
                ('keyword', UC_ARM_REG_R10, UC_ARM_REG_R10, UC_ARM_REG_R3),
                ('substitution', UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R11)):
            for shift in (0, 0x1000000):
                m = Machine(shift)
                m.uc.reg_write(base, 100)
                m.uc.reg_write(col, 42*128+64)
                m.uc.mem_write(m.scratch, struct.pack('<f', 999))
                m.invoke(name)
                self.assertEqual(m.uc.reg_read(target), 142)
                self.assertEqual(m.pen(), 0)

    def test_piece_accumulator_uses_pixels_not_bytes(self):
        for shift in (0, 0x1000000):
            for width in (0, 0.25, 12.5, 323.75):
                m = Machine(shift)
                m.uc.reg_write(UC_ARM_REG_R9, 900)
                m.uc.reg_write(UC_ARM_REG_R0, 300)  # Deliberately unrelated byte count.
                m.uc.mem_write(m.scratch, struct.pack('<f', width))
                m.invoke('piece_end')
                self.assertEqual(m.uc.reg_read(UC_ARM_REG_R9), 900+int(width*128))
                self.assertEqual(m.uc.reg_read(UC_ARM_REG_R0), 300)
                self.assertEqual(m.pen(), 0)

    def test_independently_relocated_code_and_data(self):
        for code_shift, data_shift in ((0x1000000, 0x5000000), (0x5000000, 0), (0, 0x1000000)):
            m = Machine(code_shift, bytes([10]*192), data_shift)
            m.uc.reg_write(UC_ARM_REG_R3, 128)
            m.uc.reg_write(UC_ARM_REG_R11, 100)
            m.invoke('normal')
            self.assertEqual(m.uc.reg_read(UC_ARM_REG_R11), 101)
            m.uc.reg_write(UC_ARM_REG_R9, 1152)
            m.uc.reg_write(UC_ARM_REG_S19, bits(24))
            m.uc.reg_write(UC_ARM_REG_S21, bits(31))
            m.invoke('advance')
            self.assertEqual(m.pen(), 7.5)
            m.uc.reg_write(UC_ARM_REG_R9, 0)
            m.invoke('piece_end')
            self.assertEqual(m.uc.reg_read(UC_ARM_REG_R9), 960)

    def test_rejects_unknown_input_and_invalid_widths(self):
        with self.assertRaises(ValueError):
            vwf.patch(b'not a pinned executable', bytes([32]*192))
        for invalid in (bytes(192), bytes([33]*192), bytes([32]*191)):
            with self.assertRaises(ValueError):
                vwf.stubs(invalid, 0x8168C61C)


class VwfExecutableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from inspect_vwf import load, PILOT
        if not PILOT.exists():
            raise unittest.SkipTest('Private pinned Vita pilot unavailable')
        cls.original, cls.original_info = load()
        cls.widths = bytes(1+i % 31 for i in range(192))
        cls.candidate, cls.audit = vwf.patch(cls.original, cls.widths)

    def test_preserves_segments_and_extends_without_overlap(self):
        old, new = self.original_info, vwf.parse(self.candidate)
        for i in range(5):
            a, b = old['infos'][i], new['infos'][i]
            before, after = self.original[a[0]:a[0]+a[1]], self.candidate[b[0]:b[0]+b[1]]
            self.assertEqual(old['phdrs'][i][2], new['phdrs'][i][2])
            if i == 3:
                self.assertEqual(before, after[:-12])
                self.assertEqual(after[-12:], vwf.pen_relocation(0x81000000, 0x812B6000, 0x8168C61C))
            elif i >= 2:
                self.assertEqual(before, after)
            elif i == 1:
                self.assertEqual(before, after[:len(before)])
                self.assertFalse(any(after[len(before):-192]))
                self.assertEqual(after[-192:],self.widths)
        p0, p1 = new['phdrs'][:2]
        self.assertEqual(p0[2]+p0[5], p1[2])
        self.assertGreaterEqual(p1[1], p0[1]+p0[4])
        self.assertEqual(p1[5], self.original_info['phdrs'][1][5]+4+192)
        self.assertEqual((p0[6],p1[6]),(5,6))  # RX code, RW non-executable data.
        with self.assertRaises(ValueError):
            vwf.patch(self.candidate, self.widths)  # No double-patching.

    def test_actual_original_drawer_and_glyph_lookup(self):
        # GPU calls are intercepted, but text decoding, lookup, loop, original
        # branches, patched BL, widths, line breaks and final pen run on ARM.
        u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        u.mem_map(0x81000000, 0x690000)
        info = vwf.parse(self.candidate)
        for i in (0, 1):
            off, size = info['infos'][i][:2]
            u.mem_write(info['phdrs'][i][2], self.candidate[off:off+size])
        u.mem_map(0x200000, 0x10000)
        u.reg_write(UC_ARM_REG_CPSR, 0x30)
        u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.reg_write(UC_ARM_REG_C1_C0_2, 0xF << 20)
        u.reg_write(UC_ARM_REG_FPEXC, 1 << 30)
        state, quads = 0x8138AA58, []
        u.mem_write(state, bytes(0x78))
        for offset, value in ((0x14, 24), (0x18, 24), (0x1C, 31), (0x20, 32)):
            u.mem_write(state+offset, struct.pack('<f', value))
        noops = {0x8100985E, 0x810095D0, 0x8100986A, 0x81009DA8, 0x81009776, 0x81008F64}

        def external(cpu, address, size, data):
            if address == 0x8100970A:
                cpu.reg_write(UC_ARM_REG_R0, 0x202000)
            elif address == 0x8100973C:
                quads.append((cpu.reg_read(UC_ARM_REG_R9),
                              number(cpu.reg_read(UC_ARM_REG_S0)),
                              number(cpu.reg_read(UC_ARM_REG_S1))))
            elif address not in noops:
                return
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

        u.hook_add(UC_HOOK_CODE, external)
        # Two bank cells followed by ordinary Japanese punctuation; newline
        # restores the initial X. Full-page lookup must land on our bank.
        payload = bytes.fromhex('8741874281410a874300')
        u.mem_write(0x201000, payload)
        u.reg_write(UC_ARM_REG_R0, 0x201000)
        u.reg_write(UC_ARM_REG_R1, 1)
        u.reg_write(UC_ARM_REG_S0, bits(100))
        u.reg_write(UC_ARM_REG_S1, bits(200))
        u.reg_write(UC_ARM_REG_S2, bits(0))
        u.reg_write(UC_ARM_REG_LR, 0x200001)
        u.emu_start(0x81006E11, 0x200000, count=10000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC), 0x200000)
        self.assertEqual(quads, [(1153, 100, 200), (1154, 101.5, 200),
                                (1, 103.75, 200), (1155, 100, 232)])
        self.assertEqual(struct.unpack('<f', u.mem_read(state+0xC, 4))[0], 103)


class VwfLayoutTests(unittest.TestCase):
    def test_pixel_budget_and_native_byte_buffer_guard(self):
        from prepare_vwf import validate_layout, line_widths
        widths = {chr(i): 10 for i in range(32, 127)}
        self.assertEqual(line_widths('Wi《m》.\n$a', widths), [40, 192])
        validate_layout('A'*70, b'\x87\x41'*70, widths)
        with self.assertRaises(ValueError):
            validate_layout('A'*97, b'\x87\x41'*97, widths)
        with self.assertRaises(ValueError):
            validate_layout('A', b'\x87\x41'*129, widths)

    def test_single_letter_codec_preserves_keywords_controls(self):
        from text_codec import encode, decode
        mapping = {chr(i): 0x8700+i for i in range(32, 127)}
        text = 'Wi. 《D estruction》 $a\n「Yes」'
        payload, _ = encode(text, mapping)
        self.assertEqual(decode(payload, mapping), text)
        self.assertIn(b'$a', payload)
        self.assertIn('《'.encode('cp932'), payload)


if __name__ == '__main__':
    unittest.main()
