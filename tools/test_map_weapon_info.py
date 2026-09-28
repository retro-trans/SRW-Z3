"""Read-only fixtures and in-memory MAP row checks; never builds game files."""
from pathlib import Path
import json
import struct
import unittest
from cpk import CPK
import eboot
import trdata
import map_weapon_info as M


class MapWeaponInfoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.elf = Path('work/EBOOT_dec.elf').read_bytes()
        k = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = k.read(k.files[0])
        root = Path('work/build_0.6.21_english_20260925_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        k = CPK(str(root / 'AIDDATAPACK.CPK'))
        cls.current = k.read(k.files[0])

    def test_complete_source_inventory_and_guard(self):
        M.check_source(self.elf, self.ui)
        for _, _, off in M.STATES + M.PATTERNS:
            bad = bytearray(self.elf)
            bad[off] ^= 1
            with self.assertRaises(AssertionError):
                M.check_source(bad, self.ui)

    def test_pristine_and_released_ui_composition_is_scoped(self):
        allowed = {i for r in M.HEADERS for i in range(r + 4, r + 8)}
        allowed |= {i for r in M.DEFAULTS for i in range(r, r + 4)}
        for before in (self.ui, self.current):
            after = M.apply(before, self.mapping, self.widths, self.ui)
            self.assertTrue(all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, after))))
            # Values, font sizes, icons and targeting data must stay native.
            for r in M.HEADERS + M.DEFAULTS:
                self.assertEqual(before[r + 8:r + 32], after[r + 8:r + 32])
            for r in M.PATTERN_DEFAULTS + M.IFF_HEADERS:
                self.assertEqual(before[r:r + 32], after[r:r + 32])

    def test_all_states_patterns_and_exact_hooks(self):
        loaded = eboot.load_ui_hook()
        for jp, mid, _ in M.STATES + M.PATTERNS:
            self.assertEqual(loaded[jp], M.localization.english().text(mid))
            self.assertNotIn(jp, eboot.UI_PREFIX | eboot.UI_JOINED)
        M.check_widths(self.mapping, self.widths)
        self.assertEqual(M.hooks(), {'有効': 'On', '無効': 'Off'})

    def test_old_overflow_and_new_guard(self):
        self.assertGreater(M.VALUE_X + M.ink('Self-Centered', self.mapping, self.widths, 28), M.RIGHT)
        self.assertGreater(607.5 + M.ink('Pattern:', self.mapping, self.widths, 28), M.VALUE_X)
        after = bytearray(M.apply(self.ui, self.mapping, self.widths, self.ui))
        struct.pack_into('>f', after, M.HEADERS[0] + 4, -0.05078125)
        with self.assertRaises(AssertionError):
            M.check_ui(after, self.mapping, self.widths)

    def test_full_ui_hook_table_in_memory(self):
        blob = bytearray(self.elf)
        eboot.add_segment(blob)
        segs = eboot._segments(blob)
        count, skipped, *_ = eboot.name_hook(blob, segs, {}, self.mapping)
        self.assertEqual(skipped, 0)
        entries = {}
        pos = eboot._off(segs, eboot.NAME_TBL)
        for _ in range(count):
            key, value = struct.unpack_from('>II', blob, pos)
            entries[bytes(eboot._cstr(blob, eboot._off(segs, key)))] = (
                value & 0xc0000000,
                bytes(eboot._cstr(blob, eboot._off(segs, value & 0x3fffffff))))
            pos += 8
        M.check_hooks(entries, self.mapping)
        self.assertEqual(blob[0x7111f8:0x711258], self.elf[0x7111f8:0x711258])


if __name__ == '__main__':
    unittest.main()
