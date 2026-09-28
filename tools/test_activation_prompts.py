"""Read-only fixtures, in-memory EBOOT patch, and emitted-PPC checks."""
import json
import struct
import unittest
from pathlib import Path
from unittest.mock import patch
import activation_prompts as prompts
import command_layout as layout
import digraph as dg
import eboot
import trdata
from check_confirmation_tabs import execute


class ActivationPromptsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.19_english_20260924_r3')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        cls.source = Path('work/EBOOT_dec.elf').read_bytes()

    def test_complete_source_family_and_guard_negatives(self):
        self.assertEqual(len(prompts.source_inventory(self.source)), 17)
        for off in (0x6d4fe8, 0x780278, 0x710940, 0x7cbf94, 0x30eabc):
            damaged = bytearray(self.source)
            damaged[off] ^= 1
            with self.assertRaises(AssertionError):
                prompts.source_inventory(damaged)
        for va, count, _ in prompts.COPY_BLOCKS:
            off = va - 0x10000
            expected = prompts.original_copy(count)
            self.assertEqual(self.source[off:off + len(expected)], expected)
        damaged = bytearray(self.source)
        damaged[prompts.COPY_BLOCKS[0][0] - 0x10000] ^= 1
        cursor, _ = eboot.add_segment(damaged)
        with self.assertRaisesRegex(AssertionError, 'Skill suffix copy changed'):
            prompts.patch(damaged, self.mapping, cursor)

    def test_in_memory_executable_budget_and_references(self):
        from build_project import load_labels
        trdata.use_glossary('analysis/glossary.json')
        names = {
            t['jp']: t['en'] for t in trdata._load('analysis/glossary.json')['terms'] if t['en']}
        all_names = dict(names)
        for file in sorted(Path('translation/library').glob('*.json')):
            all_names.update(trdata.names(str(file)))
        names = {**load_labels(), **trdata._load('translation/weapons.json'), **names}
        names.update(trdata.assemble('translation/library', 'kw',
                     trdata.ambiguous_terms('analysis/glossary.json'))[1])
        with patch.object(eboot, 'HOOK_ALL_SET', set(all_names)):
            new, report = eboot.patch(self.source, names, self.mapping, widths=self.widths)
        prompts.check(new, self.mapping, self.widths)
        import trader_upgrade_text
        trader_upgrade_text.check(new,self.mapping,self.widths)
        import weapon_requirement_runtime
        weapon_requirement_runtime.check(new, self.mapping, self.widths)
        import battle_speaker_names
        battle_speaker_names.check(new)
        import battle_screen_labels
        battle_screen_labels.check_elf(new, self.mapping)
        import command_swap_labels
        command_swap_labels.check_elf(new, self.mapping, self.widths)
        eboot.verify(self.source, new, names, self.mapping, report['vwf'])
        import sys
        sys.path.insert(0, str(Path('platforms/ps3').resolve()))
        import cfw_loader_layout
        import ppc_permissions
        folded = cfw_loader_layout.fold(new)
        permissions = ppc_permissions.check_changed_branches(self.source, folded)
        print('PASS: folded current EBOOT branch permissions:', permissions)
        import check_command_layout
        from cpk import CPK
        archive = CPK('work/build_0.6.19_english_20260924_r3/AIDDATAPACK.CPK')
        ui = archive.read(next(f for f in archive.files if f['id'] == 0))
        check_command_layout.check(new, self.mapping, ui)
        segs = eboot._segments(new)
        remaining = eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE - report['battle_name_transport_end']
        self.assertGreater(remaining, 0)
        print('PASS: complete current EBOOT in memory; %d bytes remain after all extensions.' % remaining)
        # Original branch tails and all buffers/name construction remain intact.
        for va in (0x31de30, 0x31df9c, 0x31e0d4, 0x31e210, 0x31e454, 0x31e550):
            off = va - 0x10000
            self.assertEqual(new[off:off + 4], self.source[off:off + 4])

    def test_all_activation_pads_execute_at_live_pitches(self):
        self.assertFalse(set(layout.CODES) & set(self.mapping.values()))
        widths = bytes(self.widths.get(i, 32) for i in range(eboot.ATLAS_CELLS))
        data = b''.join(struct.pack('>ff', layout.count_coefficient(i),
                         sum(widths[dg.cell_index(self.mapping[c])] for c in label) / 64)
                        for i, label in enumerate(layout.LABELS))
        extra = ((layout.CAVE, layout.stub()), (layout.DATA, data))
        self.assertLessEqual(eboot.STUB_VA + len(eboot.vwf_stub()), eboot.KW_SITES[0][2])
        for i in range(len(layout.LABELS)):
            label = layout.LABELS[i]
            code = layout.CODES[i]
            if i >= layout.ACTIVATION_START:
                with self.assertRaises(UnicodeDecodeError):
                    struct.pack('>H', code).decode('cp932')
            ink = sum(widths[dg.cell_index(self.mapping[c])] for c in label)
            for pitch in (23, 31, 37.28):
                for quad in (25, 31, 32):
                    origin = 640 - layout.count_coefficient(i) * pitch
                    advance, _ = execute(eboot.vwf_stub(), widths, dg.cell_index(code),
                                         origin, origin, pitch, quad, 0, extra)
                    self.assertAlmostEqual(origin + advance + ink * quad / 64, 640, delta=.0001)

    def test_emitted_copy_loop_preserves_dynamic_prefix_and_tail(self):
        # Execute the actual PPC instructions, including the NUL byte. A
        # guard after each result catches the old fixed-size-copy truncation.
        code = prompts.copy_loop()
        for name in ('B-Save', 'Support Atk', 'A much longer translated name'):
            for key, _, suffix in prompts.rows():
                if not key.startswith('skill_'):
                    continue
                prefix = dg.encode_mixed('「' + name, self.mapping)
                src = dg.encode_mixed(suffix, self.mapping) + b'\0'
                memory = dict(enumerate(prefix + b'\0' + b'\xCC' * 230, 0x2000))
                memory.update(enumerate(src, 0x1000))
                regs = [0x100000 + i * 256 for i in range(32)]
                regs[3], regs[9] = 0x2000 + len(prefix), 0x1000
                before = regs[:]
                pc, equal = 0, False
                for _ in range(10000):
                    if pc == len(code):
                        break
                    word = struct.unpack_from('>I', code, pc)[0]
                    op, rt, ra, rb = word >> 26, (word >> 21) & 31, (word >> 16) & 31, (word >> 11) & 31
                    imm = word & 65535
                    imm -= 65536 if imm & 32768 else 0
                    pc += 4
                    if op == 14:
                        regs[rt] = (regs[ra] if ra else 0) + imm
                    elif op == 31 and (word >> 1) & 1023 == 87:
                        regs[rt] = memory[regs[ra] + regs[rb]]
                    elif op == 31 and (word >> 1) & 1023 == 266:
                        regs[rt] = regs[ra] + regs[rb]
                    elif op == 38:
                        memory[regs[ra] + imm] = regs[rt] & 255
                    elif op == 11:
                        equal = regs[ra] == imm
                    elif op == 16 and word & 0xFFFF0000 == 0x40820000:
                        if not equal:
                            pc = pc - 4 + imm
                    else:
                        self.fail('Unknown PPC instruction %08x' % word)
                else:
                    self.fail('Copy loop did not terminate')
                result = bytes(memory[0x2000 + i] for i in range(len(prefix) + len(src)))
                self.assertEqual(result, prefix + src)
                self.assertEqual(memory[0x2000 + len(result)], 0xCC)
                for reg in set(range(32)) - {0, 8, 11}:
                    self.assertEqual(regs[reg], before[reg])


if __name__ == '__main__':
    unittest.main()
