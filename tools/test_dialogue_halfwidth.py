"""Reject single-byte half-width cells; verify the reported stage in memory."""
import json
from pathlib import Path
import struct
import unittest
from unittest.mock import patch

from cpk import CPK
import check_stage
import digraph as dg
import patch_lua
import trdata


class HalfwidthTests(unittest.TestCase):
    def test_all_halfwidth_cp932_characters_rejected(self):
        for code in range(0xff61,0xffa0):
            ch=chr(code)
            self.assertEqual(len(ch.encode('cp932')),1)
            for encoder in (dg.encode_letters,dg.encode_pairs,dg.encode_hybrid):
                with self.subTest(code=hex(code),encoder=encoder.__name__):
                    with self.assertRaisesRegex(SystemExit,'unsafe half-width'):
                        encoder(ch,{})

    def test_fullwidth_quotes_links_and_runtime_escapes_unchanged(self):
        text='「《A》$n」\n（$l$F$c）'
        expected='「《'.encode('cp932')+struct.pack('>H',0x8640)
        expected+='》'.encode('cp932')+b'$n'+'」'.encode('cp932')+b'\r\n'
        expected+='（'.encode('cp932')+b'$l$F$c'+'）'.encode('cp932')
        self.assertEqual(dg.encode_letters(text,{'A':0x8640}),expected)

    def test_stage_checker_rejects_old_quote(self):
        problems=check_stage.check([{'sha':'example','jp':'「A」'}],
                                  {'example':'「｢A｣」'},measure=False,
                                  mapping={'A':0x8640},term_idx={})
        self.assertTrue(any(kind=='charset' and 'half-width' in message
                            for _,kind,message in problems))

    def test_english_catalog_has_no_halfwidth_cells(self):
        for path in Path('localization/locales/en').glob('*.json'):
            for mid,row in json.loads(path.read_text(encoding='utf-8'))['messages'].items():
                self.assertFalse(any(0xff61<=ord(c)<=0xff9f for c in row.get('text') or ''),mid)

    def test_stage25_patch_removes_only_132_bad_bytes(self):
        mapping=json.loads(Path('work/build_0.6.16_batched_source_20260919/pairs.json').read_text())
        trdata.use_glossary('analysis/glossary.json')
        records=trdata.records('translation/stage0025_03.json')
        with patch.object(dg,'VWF',True):
            fixed=patch_lua.patch(Path('work/lua25/STG0025_00003.lua').read_bytes(),records,mapping)
        opening='「｢'.encode('cp932');closing='｣」'.encode('cp932')
        for version,folder in (
                ('0.6.15','work/build_0.6.15_hardware_source_20260919'),
                ('0.6.16','work/build_0.6.16_batched_source_20260919')):
            archive=CPK(str(Path(folder)/'STG0025.SDAT.cpk'))
            old=archive.read(next(f for f in archive.files if f['id']==3))
            with self.subTest(version=version):
                self.assertEqual(old.count(opening),66)
                self.assertEqual(old.count(closing),66)
                expected=old.replace(opening,'「'.encode('cp932')).replace(closing,'」'.encode('cp932'))
                self.assertEqual(fixed,expected)
                self.assertEqual(len(old)-len(fixed),132)


if __name__=='__main__':unittest.main()
