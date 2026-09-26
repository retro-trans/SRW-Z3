"""Pilot skill coverage, layout, mechanics wording and isolated candidate patch."""
import json
import struct
import unittest
from pathlib import Path
import eboot, rpw, trdata
from build_skill_descriptions import ROOT, HOOK, generate
from skill_description_catalog import CATALOG
from intermission_layout import ink
from patch_parts_candidate import patch


class SkillDescriptions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out = ROOT/'work/out_0.6.3'
        cls.mapping = json.loads((cls.out/'pairs.json').read_text())
        cls.widths = {int(k):v for k,v in json.loads((cls.out/'widths.json').read_text()).items()}
        cls.doc = json.loads(HOOK.read_text(encoding='utf-8'))

    def test_complete_inventory(self):
        result = generate(self.mapping,self.widths)
        self.assertEqual(len(CATALOG),68)
        self.assertEqual(len(result),124)
        self.assertEqual(result,{r['jp']:r['en'] for r in self.doc['lines']})

    def test_fit_and_encoding(self):
        for r in self.doc['lines']:
            self.assertLessEqual(len(r['en'].splitlines()),3)
            for line in r['en'].splitlines():
                self.assertLessEqual(ink(line,self.mapping,self.widths,28),740)
                self.assertTrue(all(c in self.mapping for c in line),line)
            self.assertNotIn('$$',r['en'])
            self.assertTrue(eboot._encode_marked(r['en'],self.mapping))

    def test_no_arbitrary_fragment_pairs(self):
        self.assertIs(self.doc['line_pairs'],False)
        self.assertEqual(len(eboot.load_ui_hook(paths=[str(HOOK)])),124)

    def test_key_effects_and_variant_distinctions(self):
        self.assertIn('Halves damage',CATALOG['ハーフカット'])
        self.assertIn('30% or less',CATALOG['ハーフカット'])
        self.assertIn('per available support use',CATALOG['援護攻撃'])
        self.assertIn('30%',CATALOG['野性化'])
        self.assertIn('rank A',CATALOG['重力干渉１'])
        self.assertIn('rank S',CATALOG['重力干渉２'])
        self.assertIn('100%',CATALOG['逆さまの力１'])
        self.assertIn('50%',CATALOG['逆さまの力２'])
        self.assertIn('rounded up',CATALOG['Ｂセーブ'])
        self.assertIn('No effect for sub-pilots',CATALOG['精神耐性'])
        self.assertIn('Barrier Field',CATALOG['断ち切る力'])
        self.assertNotIn('????',CATALOG['断ち切る力'])

    def test_original_rpw_description_bytes(self):
        def descriptions(path):
            raw = path.read_bytes()
            _,_,start,end,_ = next(c for c in rpw.chunks(raw) if c[0]=='j-string')
            strings = raw[start:end].split(b'\0')
            return {slot:strings[i] for slot,i in rpw.slots(raw).items()
                    if slot[0]=='sk-pri' and slot[2] in (4,5)}
        self.assertEqual(descriptions(ROOT/'work/orig/RPW_DATA.CPK'),
                         descriptions(self.out/'RPW_DATA.CPK'))

    def test_installed_exact_hooks_and_patch_isolation(self):
        backup = ROOT/'work/skill_descriptions_EBOOT.before.bin'
        if not backup.exists():
            self.skipTest('Apply candidate patch before testing installed hooks')
        trdata.use_glossary(str(ROOT/'analysis/glossary.json'))
        before = json.loads((ROOT/'work/skill_hooks_before.json').read_text(encoding='utf-8'))
        next_backup=ROOT/'work/gift_reports_EBOOT.before.bin'
        endpoint=json.loads((ROOT/'work/gift_hooks_before.json').read_text(encoding='utf-8')) if next_backup.exists() else eboot.load_ui_hook()
        replay,_ = patch(backup.read_bytes(),self.mapping,before,endpoint)
        self.assertEqual(replay,next_backup.read_bytes() if next_backup.exists() else (self.out/'EBOOT.BIN').read_bytes())
        data=(self.out/'EBOOT.BIN').read_bytes()
        segs = eboot._segments(data)
        p = eboot._off(segs,eboot.NAME_TBL)
        table = {}
        while struct.unpack_from('>I',data,p)[0]:
            k,v = struct.unpack_from('>II',data,p)
            a,b = eboot._off(segs,k),eboot._off(segs,v & 0x3fffffff)
            table[data[a:data.index(0,a)]] = data[b:data.index(0,b)]
            p += 8
        for r in self.doc['lines']:
            self.assertEqual(table[r['jp'].encode('cp932')],eboot._encode_marked(r['en'],self.mapping))


if __name__ == '__main__':
    unittest.main()
