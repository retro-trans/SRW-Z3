"""Read-only source fixtures and in-memory category repairs; no game build."""
from pathlib import Path
import json
import struct
import unittest
import subprocess
import sys
from cpk import CPK
import eboot
import trdata
import command_swap_labels as C
import battle_speaker_names as B
from intermission_layout import text, ink


class CommandSwapTests(unittest.TestCase):
    def test_ui_entrypoint_initializes_glossary_in_fresh_process(self):
        code = '''
import sys
sys.path.insert(0, 'tools')
import build_ui, command_swap_labels, trdata
assert trdata._IDX is None
def stop_before_output(_):
    rows = list(command_swap_labels.rows())
    assert rows and all('$$' not in row[1] for row in rows)
    raise SystemExit(0)
build_ui.load_mapping = stop_before_output
build_ui.main(['build_ui.py'])
'''
        result = subprocess.run([sys.executable, '-X', 'utf8', '-c', code],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.original = Path('work/EBOOT_dec.elf').read_bytes()
        k = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = k.read(k.files[0])
        root = Path('work/build_0.6.20_english_20260925_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        k = CPK(str(root / 'AIDDATAPACK.CPK'))
        cls.current_ui = k.read(k.files[0])

    def test_source_guards_and_complete_speaker_category(self):
        C.check_source(self.original, self.ui)
        B.check_source(self.original)
        self.assertEqual(sum(len(refs) for _, _, refs in B.rows()), 1155)
        self.assertEqual(len(list(B.rows())), 470)
        for off in (0x84e2e4, 0x84e614, 0x6dd2d0):
            bad = bytearray(self.original)
            bad[off] ^= 1
            with self.assertRaises(AssertionError):
                B.check_source(bad)
        bad = bytearray(self.original)
        bad[0x6d93d0] ^= 1
        with self.assertRaises(AssertionError):
            C.check_source(bad, self.ui)

    def test_ui_composition_only_changes_registered_text(self):
        for before in (self.ui, self.current_ui):
            after = C.apply(before, self.mapping, self.widths, self.ui)
            allowed = {p for _, _, rows, _, _, _ in C.rows() for r in rows for p in range(r, r + 4)}
            self.assertTrue(all(a == b or i in allowed for i, (a, b) in enumerate(zip(before, after))))
            # Runtime insertion fields, quotes and status numbers stay native.
            for r in (0xac854, 0xaca34, 0xaca94, 0xac754):
                self.assertEqual(before[r:r+32], after[r:r+32])

    def test_hooks_use_existing_equipment_terms_and_exact_matching(self):
        import gift_reports
        hooks = C.hooks()
        loaded = eboot.load_ui_hook()
        for jp, en in hooks.items():
            self.assertEqual(loaded[jp], en)
            self.assertNotIn(jp, eboot.UI_PREFIX | eboot.UI_JOINED)
            self.assertNotIn('$$', en)
        for jp, en in gift_reports.CONVERSIONS.items():
            self.assertEqual(hooks[jp], en)
            self.assertLess(ink(en, self.mapping, self.widths, 25), 390)
        self.assertEqual(hooks['ＢＷＳ'], 'BWS')
        self.assertNotIn('なし', hooks)
        self.assertNotIn('を使用します。', hooks)

    def test_tactical_title_fits_shared_targeting_anchors(self):
        import digraph as dg
        root = Path('work/build_0.6.23_english_20260929')
        mapping = json.loads((root / 'pairs.json').read_text())
        widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}
        k = CPK(str(root / 'AIDDATAPACK.CPK'))
        shipped = k.read(k.files[0])
        self.assertEqual(text(shipped, C.TACTICAL_TITLE), dg.encode_mixed('＜Tactical Cmd＞', mapping))
        with self.assertRaises(AssertionError):
            C.check_tactical_spacing(shipped, mapping, widths, '＜Tactical Cmd＞')
        fixed = C.apply(self.ui, mapping, widths, self.ui)
        self.assertEqual(text(fixed, C.TACTICAL_TITLE), dg.encode_mixed('＜Tactics＞', mapping))
        C.check_tactical_spacing(fixed, mapping, widths)
        for r in (C.TACTICAL_TITLE,) + C.TACTICAL_HINTS:
            self.assertEqual(fixed[r+4:r+32], self.ui[r+4:r+32])
        # Only the compact footer changes; command-menu terminology remains.
        self.assertEqual(C.hooks()['戦術指揮'], 'Tactical Cmd')
        self.assertEqual(C.hooks()['＜戦術指揮＞'], '＜Tactics＞')
        for jp in ('効果範囲を選択します。', '効果範囲を決定します。',
                   '味方のチームを選択します。', '敵方のチームを選択します。'):
            self.assertIn(jp, C.hooks())

    def test_speaker_patch_is_scoped_and_disambiguated(self):
        before = bytearray(self.original)
        eboot.add_segment(before)
        segs = eboot._segments(before)
        cursor = eboot._off(segs, eboot.NAME_STR)
        after, end = B.patch(before, cursor)
        allowed = {p for _, _, refs in B.rows() for r in refs for p in range(r, r + 4)}
        self.assertTrue(all(a == b or i in allowed or cursor <= i < end
                            for i, (a, b) in enumerate(zip(before, after))))
        B.check(after)
        ids = {r: mid for mid, _, refs in B.rows() for r in refs}
        for r, expected in ((0x84e2e4, 'Zessica'), (0x84db04, 'Ray'),
                            (0x84e16c, 'Rei'), (0x84d8ec, 'Mehna'), (0x84db70, 'Mina')):
            self.assertEqual(B.localization.message(ids[r]), expected)
        for mid, _, _ in B.rows():
            self.assertLess(ink(B.localization.message(mid), self.mapping, self.widths, 31), 430)
        # Every native source string is untouched, even names shared by slots.
        for _, va, _ in B.rows():
            off = va - 0x10000
            self.assertEqual(before[off:off+16], after[off:off+16])


if __name__ == '__main__':
    unittest.main()
