"""Read-only: shot-down quote hooks load exactly, point at the ELF, no line pairs."""
from pathlib import Path
import unittest
import eboot
import trdata
import destroy_quotes as b


class DestroyQuoteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.loaded = eboot.load_ui_hook()
        cls.hooks = b.hooks()
        cls.elf = Path('work/EBOOT_dec.elf').read_bytes()

    def test_every_description_is_an_exact_hook(self):
        self.assertEqual(len(self.hooks), 146)
        for jp, en in self.hooks.items():
            self.assertEqual(self.loaded[jp], en)
            self.assertNotIn(jp, eboot.UI_PREFIX)
            self.assertNotIn(jp, eboot.UI_JOINED)

    def test_keys_are_whole_strings_in_the_executable(self):
        # resident keys must be complete NUL-delimited strings, never fragments
        for jp in self.hooks:
            self.assertIn(b'\0' + jp.encode('cp932') + b'\0', self.elf)
            self.assertIn(jp, eboot.UI_ELF_RESIDENT)

    def test_no_per_line_pairs(self):
        for jp in self.hooks:
            for line in jp.split('\n')[1:] if '\n' in jp else ():
                line = line.strip('　 ')
                if line and line not in self.hooks:
                    self.assertNotIn(line, self.loaded, line)

    def test_michel_is_translated(self):
        self.assertEqual(self.hooks['「ミスった…！　スカル２、撤退する！」'],
                         '「I messed up...! Skull 2, withdrawing!」')


if __name__ == '__main__':
    unittest.main()
