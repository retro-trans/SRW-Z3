"""Broad Vita adapter safeguards; no output files or emulator installation."""
from pathlib import Path
import struct
import sys
import unittest
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'platforms/vita'))
import category_port as P
import luarec
import build_library
from text_codec import dictionary_for, decode
from cpk import CPK


class CategoryTests(unittest.TestCase):
    def setUp(self):
        self.widths={chr(i):10 for i in range(32,127)}

    def test_wrap_preserves_words_controls_and_link_span(self):
        text='One $n two 《linked words》 three four'
        result=P.wrap(text,self.widths,210)
        self.assertEqual(''.join(text.split()),''.join(result.split()))
        self.assertIn('《linked words》',result)
        self.assertTrue(all(w<=210 for w in P.line_widths(result,self.widths)))

    def test_wrap_rejects_bad_links_and_unsplittable_tokens(self):
        for text in ('bad 《link','bad 》link','《nested 《link》》','x'*100):
            with self.subTest(text=text),self.assertRaises(ValueError):
                P.wrap(text,self.widths,210)

    def test_dialogue_quotes_are_explicit_display_aliases(self):
        source='Name\n「｢Quoted text｣」'
        self.assertEqual(P.dialogue(source,self.widths),'Name\n「「Quoted text」」')
        self.assertIn('｢',source)

    def test_dialogue_reflow_does_not_join_speaker_or_blank_paragraph(self):
        text='Name\n「One\n　two\n　three\n　four」'
        self.assertEqual(P.dialogue(text,self.widths),'Name\n「One two three four」')
        text='Name\n「One\n\n　two\n　three」'
        self.assertEqual(P.dialogue(text,self.widths),text)

    def test_exact_encoding_roundtrip_and_lf_container(self):
        text='One $n\n「Two」'
        mapping=dictionary_for([text],list(range(0x8740,0x877F)))
        data=P.encoded(text,mapping)
        self.assertNotIn(b'\r',data)
        self.assertEqual(decode(data.replace(b'\n',b'\r\n'),mapping),text)

    def subset_fixture(self):
        source=('t_001 = {\r\n{WPos_B, 3, FDMode_Normal, pid_SIN, [[「Hi $n」]]},\r\n'
                '{WPos_B, 3, FDMode_Normal, pid_SIN, [[「Untouched」]]},\r\n};\r\nCmd_End();\r\n').encode('cp932')
        rows=luarec.records(source.decode('cp932'))
        rows[0]['en']='「Hello $n」'
        mapping=dictionary_for([rows[0]['en']],list(range(0x8740,0x877F)))
        return source,rows,mapping

    def test_subset_keeps_untranslated_strings_and_commands(self):
        source,rows,mapping=self.subset_fixture()
        result,total,count=P.patch_subset(source,rows[:1],mapping,self.widths)
        self.assertEqual((total,count),(2,1))
        self.assertIn('[[「Untouched」]]'.encode('cp932'),result)
        self.assertTrue(result.endswith(b'Cmd_End();\r\n'))

    def test_subset_rejects_wrong_source_and_missing_control(self):
        source,rows,mapping=self.subset_fixture()
        rows[0]['sha']='wrong'
        with self.assertRaises(ValueError):P.patch_subset(source,rows[:1],mapping,self.widths)
        source,rows,mapping=self.subset_fixture();rows[0]['en']='「Hello」'
        with self.assertRaises(ValueError):P.patch_subset(source,rows[:1],mapping,self.widths)

    def test_voice_table_segment_relative_repacked_and_inverse(self):
        old=list(range(0,277*16,16));new=[n*2 for n in old]
        location=dict(segment=0,relative_offset=12)
        packed=struct.pack('<277I',*old)
        for off in (32,160):
            blob=b'x'*(off+12)+packed+b'trailer'
            with mock.patch.object(P,'parse_self',return_value=dict(infos=[(off,12+len(packed),1,2)])):
                changed=P.replace_voice_table(blob,location,old,new)
                self.assertEqual(changed[:off+12],blob[:off+12])
                self.assertEqual(changed[-7:],b'trailer')
                self.assertEqual(P.replace_voice_table(changed,location,new,old),blob)
                with self.assertRaises(ValueError):P.replace_voice_table(changed,location,old,new)

    def test_voice_table_refuses_out_of_bounds_and_bad_offsets(self):
        old=list(range(277));loc=dict(segment=0,relative_offset=12)
        with mock.patch.object(P,'parse_self',return_value=dict(infos=[(0,10,1,2)])):
            with self.assertRaises(ValueError):P.replace_voice_table(b'\0'*1200,loc,old,old)
        with self.assertRaises(ValueError):P.replace_voice_table(b'',loc,old,[0]*277)

    def test_library_default_wrapper_and_optional_vita_wrapper(self):
        fields=[('DSCR',b'original')]
        fake=mock.Mock(files=[{'id':0}]);fake.read.return_value=b'raw'
        with mock.patch.object(build_library,'CPK',return_value=fake),mock.patch.object(build_library.zukan,'parse_ordered',return_value=(b'magic',fields)),mock.patch.object(build_library.library_cv,'load_catalog',return_value={}),mock.patch.object(build_library,'wrap',return_value='default'):
            default=list(build_library._rendered('MTZKN_KW.CPK',{'terms':[]},{0:{'DSCR':'text'}}))
            custom=list(build_library._rendered('MtZkn_KW.cpk',{'terms':[]},{0:{'DSCR':'text'}},wrap_text=lambda t:'vita'))
        self.assertEqual(default[0][3],{0:'default'})
        self.assertEqual(custom[0][3],{0:'vita'})

    @unittest.skipUnless((P.SOURCE/'CommonData/MtData/rpw_data.cpk').exists(),'Local audited Vita data required')
    def test_real_rpw_pointer_checks_reject_binary_corruption(self):
        k=CPK(str(P.SOURCE/'CommonData/MtData/rpw_data.cpk'));raw=k.read(k.files[0])
        i=next(i for i,s in enumerate(P.rpw.jstrings(raw)) if i>0 and s)
        swaps={0:b'long replacement for sentinel',i:b'long replacement for native string'}
        built,_=P.rpw.build_grown(raw,swaps)
        self.assertGreater(P.verify_rpw(raw,built,swaps,{}),1000)
        chunk=next(c for c in P.rpw.chunks(built) if c[0]=='pilot')
        corrupt=bytearray(built);struct.pack_into('<I',corrupt,chunk[2]+4,0xFFFFFFFC)
        with self.assertRaises(ValueError):P.verify_rpw(raw,bytes(corrupt),swaps,{})


if __name__=='__main__':unittest.main()
