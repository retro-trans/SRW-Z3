"""Weapon required-skill labels: category coverage and emitted exact hooks."""
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch
import eboot
import required_skill_levels as labels
import trdata
from intermission_layout import ink


class RequiredSkillLevelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.19_english_20260924_r3')
        cls.source = Path('work/EBOOT_dec.elf').read_bytes()
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        trdata.use_glossary('analysis/glossary.json')

    def test_original_composer_and_all_digits(self):
        labels.check_source(self.source)
        # Only indices 0..9 reach this Newtype-plus-digit construction.
        self.assertEqual(self.source[0x305fb8:0x305fbc], bytes.fromhex('2f1f0009'))
        for off in (0x7106a8, 0x7cbd84, 0x305f74, 0x710710):
            changed = bytearray(self.source)
            changed[off] ^= 1
            with self.assertRaises(AssertionError):
                labels.check_source(changed)

    def test_complete_exact_category_and_widths(self):
        hooks = eboot.load_ui_hook()
        self.assertEqual(len(labels.hooks()), 10)
        for n in range(10):
            key = labels.PREFIX + chr(0xff10 + n)
            self.assertEqual(hooks[key], 'Newtype L' + str(n))
            self.assertNotIn(key, eboot.UI_PREFIX | eboot.UI_JOINED)
            # Screenshot: required-skill value has >230 native pixels.
            self.assertLess(ink(hooks[key], self.mapping, self.widths, 28), 230)
        self.assertNotIn('ニュータイプＬ３以上で発動し、', labels.hooks())

    def test_emitted_entries_preserve_composer_and_values(self):
        blob = bytearray(self.source)
        eboot.add_segment(blob)
        segs = eboot._segments(blob)
        with patch.object(eboot, 'load_ui_hook', return_value=labels.hooks()):
            count, skipped, *_ = eboot.name_hook(blob, segs, {}, self.mapping)
        self.assertEqual((count, skipped), (10, 0))
        entries = {}
        pos = eboot._off(segs, eboot.NAME_TBL)
        for _ in range(count):
            jp, en = struct.unpack_from('>II', blob, pos)
            entries[bytes(eboot._cstr(blob, eboot._off(segs, jp)))] = (
                en >> 30, bytes(eboot._cstr(blob, eboot._off(segs, en & 0x3fffffff))))
            pos += 8
        labels.check(entries, self.mapping)
        self.assertEqual(blob[0x305f58:0x306098], self.source[0x305f58:0x306098])
        self.assertEqual(blob[0x7106a8:0x710748], self.source[0x7106a8:0x710748])


if __name__ == '__main__':
    unittest.main()
