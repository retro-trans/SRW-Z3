"""Read-only fixtures and in-memory patches; no build or installation."""
import json
from pathlib import Path
import struct
import unittest
from cpk import CPK
import eboot
import trdata
import team_order_labels as t
from intermission_layout import text, ink


class TeamOrderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.18_english_20260923_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        cpk = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = cpk.read(next(e for e in cpk.files if e['id'] == 0))
        cls.new = t.apply(cls.ui, cls.mapping, cls.widths)

    def test_only_pointer_position_and_centring_bytes_change(self):
        allowed = set()
        for kind, rows in t.BINDINGS.values():
            for r in rows:
                allowed.update(range(r, r + 8))
                allowed.add(r + 23)
        changed = {i for i, (a, b) in enumerate(zip(self.ui, self.new)) if a != b}
        self.assertTrue(changed <= allowed)
        for kind, rows in t.BINDINGS.values():
            for r in rows:
                self.assertEqual(self.ui[r + 8:r + 23], self.new[r + 8:r + 23])

    def test_plain_labels_keep_their_position(self):
        for kind, rows in t.BINDINGS.values():
            if kind in ('label', 'blank'):
                for r in rows:
                    self.assertEqual(self.ui[r + 4:r + 32], self.new[r + 4:r + 32], hex(r))

    def test_split_phrases_are_blank(self):
        for key, (kind, rows) in t.BINDINGS.items():
            if kind == 'blank':
                for r in rows:
                    self.assertEqual(text(self.new, r), b'')

    def test_accent_starts_where_its_english_substring_starts(self):
        names = t.labels()
        base = t.BINDINGS['cb_got'][1][0]
        accent = t.BINDINGS['cb_got_accent'][1][0]
        # "Custom Bonus" opens "Custom Bonus obtained.": both at the same x
        self.assertEqual(self.new[base + 4:base + 8], self.new[accent + 4:accent + 8])
        base = t.BINDINGS['tf_rename_hint'][1][0]
        accent = t.BINDINGS['tf_rename_hint_accent'][1][0]
        size = self.ui[base + 19]
        bx = struct.unpack_from('>f', self.new, base + 4)[0]
        ax = struct.unpack_from('>f', self.new, accent + 4)[0]
        self.assertAlmostEqual((ax - bx) * 640, ink('Select ', self.mapping, self.widths, size), 3)
        self.assertIn(names['tf_rename_hint_accent'][1], names['tf_rename_hint'][1])

    def test_live_number_widgets_untouched(self):
        # the widgets that draw the numbers follow each template; never edited
        for key in ('so_got_pp', 'so_got_kills', 'so_got_exp', 'so_got_funds', 'so_can_pick',
                    'tf_keep_left', 'so_left', 'so_idle_total'):
            # a widget record spans [row-8, row+0x18): string pointer at +8,
            # x at +0xc, size at +0x1b, centring flag at +0x1f
            for r in t.BINDINGS[key][1]:
                nxt = r + 0x20
                if nxt not in {x for _, rows in t.BINDINGS.values() for x in rows}:
                    self.assertEqual(self.ui[nxt - 8:nxt + 0x18], self.new[nxt - 8:nxt + 0x18], key)

    def test_reject_changed_source(self):
        new = bytearray(self.ui)
        struct.pack_into('>I', new, t.BINDINGS['tf_reorder'][1][0], 0)
        with self.assertRaises(AssertionError):
            t.apply(new, self.mapping, self.widths)

    def test_runtime_sources_loaded_as_exact_hooks(self):
        trdata.use_glossary('analysis/glossary.json')
        loaded = eboot.load_ui_hook()
        original = Path('work/EBOOT_dec.elf').read_bytes()
        for jp, en in t.hooks().items():
            self.assertEqual(loaded[jp], en)
            self.assertIn(jp.encode('cp932') + b'\0', original)
            self.assertNotIn(jp, eboot.UI_PREFIX)
            self.assertNotIn(jp, eboot.UI_JOINED)


if __name__ == '__main__':
    unittest.main()
