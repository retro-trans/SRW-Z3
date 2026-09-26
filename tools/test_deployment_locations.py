"""Regression tests for deployment role/centering and map caption isolation."""
import json
import struct
import unittest
from pathlib import Path
import command_layout as C
import deployment_layout as D
import map_locations as M
import digraph as dg
import eboot
from check_confirmation_tabs import execute

ROOT=Path(__file__).resolve().parents[1]
FONT='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'

class DeploymentTests(unittest.TestCase):
    def test_helper_space_and_pristine_padding(self):
        self.assertLessEqual(eboot.STUB_VA+len(eboot.vwf_stub()),eboot.KW_SITES[0][2])
        for (_,reg,start),(_,_,end) in zip(eboot.KW_SITES,eboot.KW_SITES[1:]):
            self.assertLessEqual(start+len(eboot.kw_stub(reg)),end)
        path=ROOT/'work/EBOOT_dec.elf'
        if not path.exists():self.skipTest('local pristine executable unavailable')
        blob=path.read_bytes()
        segs=eboot._segments(blob)
        start=eboot.STUB_VA-segs[0]['va']
        end=eboot.KW_SITES[1][2]-segs[0]['va']
        self.assertFalse(any(blob[start:end]))

    def test_roles_and_complete_option_sets(self):
        self.assertEqual(len(D.CONFIRMATIONS),7)
        self.assertIn('teams',D.CONFIRMATIONS['このメンバーで出撃しますか？'])
        self.assertIn('battleships',D.CONFIRMATIONS['この母艦で出撃しますか？'])
        self.assertEqual(len(D.OPTIONS),10)
        self.assertEqual(len(D.QUESTIONS),2)

    def test_pad_banks_unique(self):
        self.assertEqual(len(C.CODES),len(set(C.CODES)))
        self.assertEqual(len(C.CODEPOINTS),len(set(C.CODEPOINTS)))
        self.assertEqual(len(C.CODES),len(C.LABELS))
        for jp in D.CONFIRMATIONS:
            self.assertEqual(C.count_coefficient(C.dialog_index(jp)),len(jp)/2.)

    def test_actual_ppc_centering(self):
        widths_path=ROOT/'work/out_0.6.2/widths.json'
        if not widths_path.exists():self.skipTest('local mapping fixture unavailable')
        mapping=json.loads((ROOT/'work/out_0.6.2/pairs.json').read_text())
        wd={int(k):v for k,v in json.loads(widths_path.read_text()).items()}
        widths=bytes(wd.get(i,32) for i in range(eboot.ATLAS_CELLS))
        data=b''.join(struct.pack('>ff',C.count_coefficient(i),sum(widths[dg.cell_index(mapping[c])] for c in label)/64.) for i,label in enumerate(C.LABELS))
        extra=((C.CAVE,C.stub()),(C.DATA,data))
        for i,label in enumerate(C.LABELS):
            ink=sum(widths[dg.cell_index(mapping[c])] for c in label)
            for pitch in (23,31,42):
                for quad in (25,28,32):
                    origin=640-C.count_coefficient(i)*pitch
                    advance,acc=execute(eboot.vwf_stub(),widths,dg.cell_index(C.CODES[i]),origin,origin,pitch,quad,0,extra)
                    self.assertAlmostEqual(origin+advance+ink*quad/64.,640,places=3)
                    self.assertAlmostEqual(acc,advance,places=3)

class MapTests(unittest.TestCase):
    def test_complete_catalogue(self):
        self.assertEqual(set(M.ROWS),M.EXPECTED)
        self.assertEqual(len(M.ROWS),83)
        self.assertEqual(M.english(94),'Neo Tokyo-2')
        self.assertEqual(M.SOURCES[174]['caption_rect'],[0,104,440,24])
        self.assertGreater(M.SOURCES[148]['sample_count'],0)

    def test_glossary_tokens_resolve(self):
        for member in M.ROWS:
            self.assertTrue(M.english(member).isascii())
            self.assertNotIn('$$',M.english(member))

    def test_caption_only_and_source_rejection(self):
        path=ROOT/'work/deploy_locations/eff_94.bin'
        if not path.exists() or not Path(FONT).exists():self.skipTest('local source/font fixtures unavailable')
        original=path.read_bytes();built=M.apply(original,FONT,94)
        M.verify(original,built,FONT,94)
        corrupt=bytearray(original);corrupt[0]^=1
        with self.assertRaises(AssertionError):M.apply(bytes(corrupt),FONT,94)
        corrupt=bytearray(built);corrupt[40]^=1
        with self.assertRaises(AssertionError):M.verify(original,bytes(corrupt),FONT,94)

    def test_right_anchor_preserved(self):
        path=ROOT/'work/deploy_locations/eff_120.bin'
        if not path.exists() or not Path(FONT).exists():self.skipTest('local source/font fixtures unavailable')
        original=path.read_bytes()
        self.assertEqual(M.alignment(original,120),'right')
        tile=M.render(original,FONT,120)
        box=tile.getchannel('A').getbbox()
        self.assertGreater(box[0],20)
        self.assertLessEqual(box[2],tile.width-6)

if __name__=='__main__':unittest.main()
