"""In-memory chapter hooks and read-only native narration fixtures."""
from pathlib import Path
import json
import struct
import unittest
import chapter_narration as N
import eboot
import trdata


class ChapterNarrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        root = Path('work/build_0.6.21_english_20260925_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}

    def test_all_four_pages_and_thirteen_source_rows(self):
        N.check_source()
        self.assertEqual(len(N.rows()), 13)
        self.assertEqual([sum(c['stage'] == s for c, _, _ in N.rows()) for s in N.SOURCES], [3, 3, 3, 4])

    def test_exact_whole_row_hooks_and_no_extra_lines(self):
        loaded = eboot.load_ui_hook()
        for jp, en in N.hooks().items():
            self.assertEqual(loaded[jp], en)
            self.assertNotIn(jp, eboot.UI_PREFIX | eboot.UI_JOINED | eboot.UI_KEY_VWF)
            self.assertNotIn('\n', en)
            self.assertNotIn('\r', en)
        self.assertEqual(N.hooks()['それがシンカへの道……'], 'That is the path to evolution...')

    def test_complete_ui_hook_table_and_measured_width(self):
        original = Path('work/EBOOT_dec.elf').read_bytes()
        blob = bytearray(original)
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
        N.check_hooks(entries, self.mapping, self.widths)
        # Regression gate rejects a stale/missing Japanese-row translation.
        del entries[next(iter(N.hooks())).encode('cp932')]
        with self.assertRaises(KeyError):
            N.check_hooks(entries, self.mapping, self.widths)


if __name__ == '__main__':
    unittest.main()
