"""Guard the actual runtime table, not only the warning's FSSA templates."""
import json
from pathlib import Path
import unittest
import eboot
import trdata
import weapon_requirement_runtime as W
from intermission_layout import ink


class RuntimeWarningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path('work/EBOOT_dec.elf').read_bytes()
        root = Path('work/build_0.6.20_english_20260925_r2')
        cls.mapping = json.loads((root/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        trdata.use_glossary('analysis/glossary.json')

    def test_complete_runtime_table_and_exact_whitespace(self):
        keys = W.source_inventory(self.source)
        hooks = eboot.load_ui_hook()
        self.assertEqual(len(keys),16)
        self.assertEqual(len(W.hooks()),14)
        for jp in keys[:-1]:
            self.assertEqual(hooks[jp],W.hooks()[jp])
            self.assertNotIn(jp,eboot.UI_PREFIX | eboot.UI_JOINED)
            self.assertTrue(hooks[jp].startswith('・'))
            self.assertLess(ink(hooks[jp],self.mapping,self.widths,31),420)
        self.assertEqual(hooks['・気力'],'・Focus')
        self.assertEqual(hooks['・移動後可能　'],'・Use After Moving')
        # Song EN uses a separate fixed-size native copy; previous batch hooks it.
        self.assertEqual(hooks['・歌ＥＮ'],'・Song EN')
        self.assertNotIn(W.PLACEHOLDER,W.hooks())

    def test_source_table_and_constructor_corruption_rejected(self):
        for pos in (W.TABLE,0x7cc28c,0x321088,0x7115c0):
            damaged = bytearray(self.source)
            damaged[pos] ^= 1
            with self.subTest(pos=hex(pos)), self.assertRaises(AssertionError):
                W.source_inventory(damaged)

    def test_static_and_runtime_basic_labels_agree(self):
        import weapon_requirements as static
        hooks = W.hooks()
        for jp,en in static.LABELS:
            key = '・'+jp
            if key not in hooks:
                key += '　'
            self.assertEqual(hooks[key],'・'+en)


if __name__ == '__main__':
    unittest.main()
