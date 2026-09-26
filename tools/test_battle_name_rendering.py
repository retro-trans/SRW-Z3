"""In-memory RPW and actual PPC hook tests; no build/install or runtime claim."""
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

import battle_name_rendering as B
from cpk import CPK
import digraph as dg
import eboot
import rpw
import trdata
from test_ps3_link_identity import CPU


class BattleNameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.16_batched_source_20260919')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        trdata.use_glossary('analysis/glossary.json')
        cp = CPK('work/lib/RPW_DATA.CPK')
        cls.raw = cp.read(cp.files[0])
        cls.names = B.hooks()
        cls.elf = bytearray((root / 'EBOOT.BIN').read_bytes())
        segs = eboot._segments(cls.elf)
        struct.pack_into('>I', cls.elf, eboot._off(segs, eboot.NAME_SITE), eboot.NAME_ORIG)
        # Reuse the real .16 executable layout/atlas; isolate the new exact
        # entries so failures cannot be hidden by an older glossary entry.
        with patch.object(eboot, 'load_ui_hook', return_value=cls.names):
            eboot.name_hook(cls.elf, segs, {}, cls.mapping)

    def test_names_still_use_full_canonical_english(self):
        self.assertEqual(self.names, {'第４の使徒': 'the Fourth Angel',
                                     'ネオ・ジオン兵': 'Neo Zeon Soldier',
                                     '宇宙魔王兵': 'Space Demon King Soldier'})
        loaded = eboot.load_ui_hook()
        for jp, en in self.names.items():
            self.assertEqual(loaded[jp], en)
            self.assertNotIn(jp, eboot.UI_PREFIX | eboot.UI_JOINED | eboot.UI_KEY_VWF)
        # This distinct squad label is plural and joined. Do not overwrite
        # it with the singular battle name while fixing the other two.
        self.assertEqual(loaded['マリーメイア兵'], 'Mariemaia Soldiers')
        self.assertIn('マリーメイア兵', eboot.UI_JOINED)
        self.assertEqual(loaded['宇宙魔王軍'], 'Space Demon Army')
        self.assertEqual(loaded['宇宙魔王'], 'Space Demon King')
        self.assertIn('宇宙魔王軍', eboot.UI_JOINED)
        self.assertIn('宇宙魔王', eboot.UI_JOINED)
        B.check_elf(self.elf, self.mapping)

    def test_space_demon_soldier_all_twelve_references_and_full_old_text(self):
        strings = rpw.jstrings(self.raw)
        slots = rpw.slots(self.raw)
        hits = [slot for slot, i in slots.items() if strings[i] == '宇宙魔王兵']
        self.assertEqual(len(hits), 12)
        self.assertTrue(all(slot[0] == 'pilot-nw' for slot in hits))
        self.assertIn(strings.index('宇宙魔王兵'), B.deferred_indices(self.raw))
        cp = CPK('work/build_0.6.17_english_namefix_20260919/RPW_DATA.CPK')
        old = cp.read(cp.files[0])
        _, _, start, end, _ = next(c for c in rpw.chunks(old) if c[0] == 'j-string')
        old_strings = old[start:end].split(b'\0')
        old_slots = rpw.slots(old)
        for slot in hits:
            self.assertEqual(old_strings[old_slots[slot]],
                             dg.encode_mixed('Space Demon King Soldier', self.mapping))

    def test_frozen_build_does_not_pass_new_rpw_gate(self):
        cp = CPK('work/build_0.6.16_batched_source_20260919/RPW_DATA.CPK')
        with self.assertRaises(AssertionError):
            B.check_rpw(self.raw, cp.read(cp.files[0]))

    def test_rpw_native_names_stay_short_and_other_slots_unchanged(self):
        strings = rpw.jstrings(self.raw)
        swaps = rpw.plan_all(strings, dict(self.names, **{'ミサト': 'Misato',
                                                        'マリーメイア兵': 'Mariemaia Soldier'}))
        deferred = B.deferred_indices(self.raw)
        filtered = B.defer_swaps(self.raw, swaps)
        self.assertEqual(set(swaps) - set(filtered), deferred)
        self.assertEqual(filtered, {i: en for i, en in swaps.items() if i not in deferred})
        slots = rpw.slots(self.raw)
        overrides = {slot: swaps[i] for slot, i in slots.items() if i in swaps}
        safe_overrides = B.defer_overrides(self.raw, overrides)
        self.assertEqual(safe_overrides, {slot: en for slot, en in overrides.items()
                                        if slots[slot] not in deferred})
        enc = {i: dg.encode_mixed(en, self.mapping) for i, en in filtered.items()}
        ov = {slot: dg.encode_mixed(en, self.mapping) for slot, en in safe_overrides.items()}
        new, _ = rpw.build_grown(self.raw, enc, ov)
        self.assertGreater(B.check_rpw(self.raw, new), 3)
        # Removing the deferred entries cannot silently change unrelated
        # slots: compare their actual bytes against the non-deferred control.
        control, _ = rpw.build_grown(self.raw,
            {i: dg.encode_mixed(en, self.mapping) for i, en in swaps.items()},
            {slot: dg.encode_mixed(en, self.mapping) for slot, en in overrides.items()})
        def raw_strings(blob):
            _, _, start, end, _ = next(c for c in rpw.chunks(blob) if c[0] == 'j-string')
            return blob[start:end].split(b'\0')
        js_new, js_control = raw_strings(new), raw_strings(control)
        ns, cs = rpw.slots(new), rpw.slots(control)
        for slot, i in slots.items():
            if i not in deferred:
                self.assertEqual(js_new[ns[slot]], js_control[cs[slot]], slot)

    def run_hook(self, raw):
        c = CPU(self.elf)
        pointer = 0x2100000
        c.put(pointer, raw + b'\0')
        c.put(eboot.HOOK_JSTATE, bytes(12))
        c.r[3] = pointer
        c.r[4:11] = [101, 102, 103, -1, 105, 106, 107]
        c.f[1:4] = [12.5, 18.25, 1.]
        c.lr = 0x123456
        saved = c.r[:], c.f[:], c.lr
        c.run(eboot.NAME_SITE, {eboot.NAME_SITE + 4})
        self.assertEqual(c.r[1:3], saved[0][1:3])
        self.assertEqual(c.r[4:11], saved[0][4:11])
        self.assertEqual(c.r[14:], saved[0][14:])
        self.assertEqual(c.f, saved[1])
        self.assertEqual(c.lr, saved[2])
        self.assertEqual(c.read(pointer, len(raw) + 1), raw + b'\0')
        return c.string(c.r[3]), c.r[3] == pointer

    def test_actual_ppc_hook_returns_entire_name_after_short_buffer_copy(self):
        # Model the observed 15-letter boundary, NOT a claim that this is
        # the as-yet-unidentified native copy function. Original Japanese
        # survives even this limit; full English is selected after copying.
        for jp, en in self.names.items():
            expected = dg.encode_mixed(en, self.mapping)
            self.assertGreater(len(expected), 30)
            native = jp.encode('cp932') + b'\0'
            copied = (native[:31] + b'\0').split(b'\0')[0]
            self.assertEqual(copied, jp.encode('cp932'))
            actual, unchanged = self.run_hook(copied)
            self.assertFalse(unchanged)
            self.assertEqual(actual, expected)

    def test_exact_matching_does_not_claim_suffixes_or_other_names(self):
        for raw in ['第５の使徒'.encode('cp932'), '第４の使徒改'.encode('cp932'),
                    '宇宙魔王'.encode('cp932'), '宇宙魔王軍'.encode('cp932'),
                    '宇宙魔王兵０１'.encode('cp932'),
                    'ミサト'.encode('cp932'), b'', b'Custom',
                    dg.encode_mixed('the Fourth Angel', self.mapping)]:
            actual, unchanged = self.run_hook(raw)
            self.assertTrue(unchanged)
            self.assertEqual(actual, raw)

    def test_source_guard_rejects_missing_pilot_name(self):
        with patch.object(rpw, 'slots', return_value={}):
            with self.assertRaisesRegex(ValueError, 'source changed'):
                B.deferred_indices(self.raw)


if __name__ == '__main__':
    unittest.main()
