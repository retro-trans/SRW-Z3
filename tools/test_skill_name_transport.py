"""Level-up row overflow regression; local fixtures, no game build."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from cpk import CPK
import digraph as dg
import eboot
import rpw
import skill_name_transport as S
import trdata


def member(path):
    c = CPK(str(path))
    return c.read(c.files[0])


def slot_bytes(blob):
    _, _, start, end, _ = next(c for c in rpw.chunks(blob) if c[0] == 'j-string')
    strings = blob[start:end].split(b'\0')
    return {slot: strings[i] for slot, i in rpw.slots(blob).items()}


class SkillNameTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.23_english_20260929')
        cls.original = member('work/orig/RPW_DATA.CPK')
        cls.shipped = member(root/'RPW_DATA.CPK')
        cls.mapping = json.loads((root/'pairs.json').read_text())
        cls.source = Path('work/EBOOT_dec.elf').read_bytes()
        # Override the same three semantic columns on the already-built data,
        # as build_project does after its ordinary translations and overrides.
        cls.fixed, _ = rpw.build_grown(cls.shipped, {}, S.overrides(cls.original))

    def test_shipped_adjacent_row_terminator_loss(self):
        name = slot_bytes(self.shipped)[('sk-pri', 47, 2)]
        self.assertEqual(name, dg.encode_mixed('Aggressive Beast', self.mapping))
        self.assertEqual(len(name), 32)
        memory = bytearray(8 * 32)
        memory[:len(name)+1] = name + b'\0'
        dashes = ('－'*10).encode('cp932')
        memory[32:32+len(dashes)+1] = dashes + b'\0'
        self.assertEqual(bytes(memory).split(b'\0')[0], name + dashes)
        with self.assertRaises(AssertionError): S.check_rpw(self.original, self.shipped)

    def test_all_skill_columns_fit_with_largest_suffix(self):
        self.assertEqual(S.check_rpw(self.original, self.fixed), 207)
        for slot, name in slot_bytes(self.fixed).items():
            if slot[0] != 'sk-pri' or not 1 <= slot[2] <= 3:
                continue
            for suffix in ('', 'Ｌ９', '＋９', 'Ｌ９＋９'):
                value = name + suffix.encode('cp932') + b'\0'
                self.assertLessEqual(len(value), 32, slot)
                memory = bytearray(b'\xcc' * 64)
                memory[:len(value)] = value
                memory[32:53] = ('－'*10).encode('cp932') + b'\0'
                self.assertEqual(bytes(memory).split(b'\0')[0], value[:-1])

    def test_only_capacity_selected_skill_slots_change(self):
        old, new = slot_bytes(self.shipped), slot_bytes(self.fixed)
        changed = {k for k in old if old[k] != new[k]}
        self.assertEqual(changed, set(S.overrides(self.original)))
        self.assertEqual(len(changed), 6)
        self.assertEqual(set(S.deferred().values()), {'Aggressive Beast', 'Abnormal Survivor'})

    def test_draw_labels_and_suffix_scope(self):
        trdata.use_glossary('analysis/glossary.json')
        loaded = eboot.load_ui_hook()
        labels, prefixes = S.hooks()
        for jp, en in labels.items():
            self.assertEqual(loaded[jp], en)
            self.assertEqual(jp in eboot.UI_PREFIX, jp in prefixes)
        self.assertNotIn('野性化', eboot.UI_PREFIX)
        self.assertEqual(prefixes, {'野性化Ｌ', '野性化＋', '異能生存体Ｌ', '異能生存体＋'})

    def test_native_row_and_suffix_guards(self):
        S.check_source(self.source)
        broken = bytearray(self.source)
        broken[0x2ffbd4-0x10000+3] = 0x40  # stride32 ->64
        with self.assertRaises(AssertionError): S.check_source(broken)

    def test_future_long_names_use_same_capacity_rule(self):
        with patch.object(S, 'names', return_value={'底力': 'Longer Skill Name', '野性化': 'Short'}):
            self.assertEqual(S.deferred(), {'底力': 'Longer Skill Name'})
            self.assertEqual(set(S.overrides(self.original)), {('sk-pri', 13, c) for c in (1, 2, 3)})


if __name__ == '__main__': unittest.main()
