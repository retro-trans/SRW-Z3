"""Source-family, output, sizing and no-numeric-edit checks; no build writes."""
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from cpk import CPK
import aiddata
import eboot
import trdata
import song_deployment_labels as S
from intermission_layout import text, ink


class SongDeploymentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        archive = CPK('work/orig/AIDDATAPACK.CPK')
        cls.ui = archive.read(archive.files[0])
        cls.elf = Path('work/EBOOT_dec.elf').read_bytes()
        root = Path('work/build_0.6.20_english_20260925_r2')
        cls.mapping = json.loads((root / 'pairs.json').read_text())
        cls.widths = {int(k): v for k, v in json.loads((root / 'widths.json').read_text()).items()}

    def test_source_guards_and_all_duplicate_widgets(self):
        S.check_source(self.elf, self.ui)
        refs = aiddata.refs(self.ui)
        for _, d, _ in S.rows():
            widgets = {int(r, 16) for r in d['context']['widgets']}
            if not widgets:
                continue
            found = {r for p, jp, _, _ in aiddata.strings(self.ui)
                     if jp == d['source'] for r in refs.get(p, [])}
            self.assertEqual(found, widgets, d['source'])
        bad = bytearray(self.elf)
        bad[0x711100] ^= 1
        with self.assertRaises(AssertionError):
            S.check_source(bad, self.ui)

    def test_only_string_pointers_change_and_text_fits(self):
        out = S.apply(self.ui, self.mapping, self.widths, self.ui)
        allowed = {p for _, d, _ in S.rows() for w in d['context']['widgets']
                   for p in range(int(w, 16), int(w, 16) + 4)}
        self.assertTrue(all(a == b or i in allowed for i, (a,b) in enumerate(zip(self.ui,out))))
        self.assertEqual(text(out,0xacb14),b'')
        # Prefix is shorter than the original: it cannot enter the old number gap.
        self.assertLess(ink('Left:',self.mapping,self.widths,23),len('～あと')*23)

    def test_exact_hooks_and_no_global_counter_fragments(self):
        trdata.use_glossary('analysis/glossary.json')
        hooks = eboot.load_ui_hook()
        self.assertEqual(hooks['消費歌ＥＮ'], 'Song EN')
        self.assertEqual(hooks['気力上昇'], 'Focus Up')
        self.assertEqual(len(S.hooks()),19)
        for jp, en in S.hooks().items():
            self.assertEqual(hooks[jp],en)
            self.assertNotIn(jp,eboot.UI_PREFIX | eboot.UI_JOINED)
            self.assertLess(ink(en,self.mapping,self.widths,28),280)
        for jp in ('～あと','機～','搭乗','艦名'):
            self.assertNotIn(jp,S.hooks())

    def test_song_stat_uses_compact_label_and_preserves_full_help(self):
        rows = {mid: (d, en) for mid, d, en in S.rows()}
        definition, label = rows['song_deployment_labels:song_soul']
        self.assertEqual(label, 'Sng')
        self.assertEqual(S.hooks()['歌魂'], label)
        self.assertEqual(definition['context']['width_limit'], 56)
        self.assertEqual(definition['context']['widgets'], [])
        self.assertIn('Song Soul', rows['song_deployment_labels:song_stats'][1])
        # Shared CQB styles: normal 28, compact 25, and enlarged 36/42.
        # Compare at every scale, not only this screenshot's font size.
        for size in (25, 28, 36, 42):
            self.assertLess(ink(label,self.mapping,self.widths,size), 2*size)
            self.assertLess(ink(label,self.mapping,self.widths,size),
                            ink('CQB',self.mapping,self.widths,size))
            self.assertGreater(ink('Song Soul',self.mapping,self.widths,size), 2*size)
        out = S.apply(self.ui,self.mapping,self.widths,self.ui)
        bad_rows = [(mid, d, 'Song Soul' if mid.endswith(':song_soul') else en)
                    for mid,d,en in S.rows()]
        with patch.object(S, 'rows', return_value=iter(bad_rows)):
            with self.assertRaisesRegex(AssertionError, 'song_soul'):
                S.check_ui(out,self.mapping,self.widths)

    def test_composes_with_current_shipped_ui_without_other_edits(self):
        archive = CPK('work/build_0.6.20_english_20260925_r2/AIDDATAPACK.CPK')
        before = archive.read(archive.files[0])
        after = S.apply(before,self.mapping,self.widths,self.ui)
        widgets = {int(w,16) for _,d,_ in S.rows() for w in d['context']['widgets']}
        for r in widgets:
            self.assertEqual(before[r+4:r+32],after[r+4:r+32])


if __name__ == '__main__':
    unittest.main()
