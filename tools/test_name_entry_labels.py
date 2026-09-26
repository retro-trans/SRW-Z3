"""Read-only fixtures and in-memory patches; no build or installation."""
import json
from pathlib import Path
import struct
import unittest
from cpk import CPK
import eboot
import trdata
import name_entry_labels as n
from intermission_layout import text


class NameEntryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path('work/build_0.6.17_english_namefix_20260919')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        cpk = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = cpk.read(next(e for e in cpk.files if e['id'] == 0))

    def test_only_registered_pointers_change(self):
        new = n.apply(self.ui, self.mapping, self.widths)
        allowed = {p for _, rows in n.BINDINGS for r in rows for p in range(r, r + 4)}
        self.assertTrue(all(a == b or i in allowed for i, (a, b) in enumerate(zip(self.ui, new))))
        for _, rows in n.BINDINGS:
            for row in rows:
                self.assertEqual(self.ui[row + 4:row + 32], new[row + 4:row + 32])

    def test_palette_and_other_name_entry_fields_unchanged(self):
        new = n.apply(self.ui, self.mapping, self.widths)
        changed = {r for _, rows in n.BINDINGS for r in rows}
        count = 0
        for row in range(0xbc274, 0xbc9f4 + 1, 32):
            if row not in changed:
                self.assertEqual(self.ui[row:row + 32], new[row:row + 32])
                self.assertEqual(text(self.ui, row), text(new, row))
                self.assertNotIn(text(self.ui, row).decode('cp932'), n.hooks())
                count += 1
        self.assertGreater(count, 15)

    def test_reject_changed_source(self):
        new = bytearray(self.ui)
        struct.pack_into('>I', new, n.BINDINGS[0][1][0], 0)
        with self.assertRaises(AssertionError):
            n.apply(new, self.mapping, self.widths)

    def test_runtime_sources_loaded_as_exact_hooks(self):
        trdata.use_glossary('analysis/glossary.json')
        loaded = eboot.load_ui_hook()
        for jp, en in n.hooks().items():
            self.assertEqual(loaded[jp], en)
            self.assertNotIn(jp, eboot.UI_PREFIX)
            self.assertNotIn(jp, eboot.UI_JOINED)
        self.assertNotIn('Ｚ－ＢＬＵＥ', loaded)


if __name__ == '__main__':
    unittest.main()
