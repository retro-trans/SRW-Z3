"""Packed-candidate checks for the battle action/selection family."""
import json,struct,unittest
from pathlib import Path
from cpk import CPK
import eboot,digraph as dg
import maximum_break_art as art
import tag_reward_layout as menu
from intermission_layout import text,ink

WARNINGS={
 '選択できる行動変更が存在しません':'No other actions are available.',
 '攻撃対象の選択はできません':'You cannot select an attack target.',
 '使用可能な武器がありません':'No usable weapons.',
 '戦闘不能状態です':'This unit is incapacitated.',
}
ACTIONS={'・アシストなし':'・No Assist','・アシスト攻撃':'・Assist Attack',
 '・武器選択':'・Select Weapon','・参加しない':'・Do Not Join',
 '・反撃する':'・Counterattack','・防御する':'・Defend','・回避する':'・Evade','攻撃する':'Attack'}

class BattleActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=Path('work/out_0.6.3')
        if not (cls.out/'EBOOT.BIN').exists():raise unittest.SkipTest('local candidate unavailable')
        cls.b=(cls.out/'EBOOT.BIN').read_bytes();cls.orig=Path('work/EBOOT_dec.elf').read_bytes()
        cls.segs=eboot._segments(cls.b)
        cls.mapping=json.loads((cls.out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((cls.out/'widths.json').read_text()).items()}
        cls.font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'

    def test_action_menu_variants_and_power_parts(self):
        k=CPK(str(self.out/'AIDDATAPACK.CPK'));data=k.read(k.files[0])
        menu.check(data,self.mapping,self.widths)
        old=CPK('work/orig/AIDDATAPACK.CPK');source=old.read(old.files[0])
        for r in menu.ACTION_ROWS:
            self.assertEqual(data[r+4:r+32],source[r+4:r+32])
        self.assertEqual(text(data,0xa9214),dg.encode_mixed('＜Power Parts＞',self.mapping))

    def test_dynamic_action_lookup(self):
        def zstr(va):
            p=eboot._off(self.segs,va);return self.b[p:self.b.index(b'\0',p)]
        entries={};p=eboot._off(self.segs,eboot.NAME_TBL)
        while True:
            key,value=struct.unpack_from('>II',self.b,p)
            if not key:break
            entries.setdefault(zstr(key),zstr(value&0x3fffffff));p+=8
        for jp,en in ACTIONS.items():
            self.assertEqual(entries[jp.encode('cp932')],eboot._encode_marked(en,self.mapping))
            self.assertLess(ink(en,self.mapping,self.widths,28),280)

    def test_all_four_utf8_warning_references(self):
        _,encode=eboot.vwf_face(bytearray(self.b),self.segs,self.mapping)
        labels=eboot.load_commands(eboot.UI_UTF8_FILE)
        for jp,en in WARNINGS.items():
            self.assertEqual(labels[jp],en)
            key=b'\0'+jp.encode('utf-8')+b'\0';p=self.orig.index(key)+1
            expected=encode(en).encode('utf-8')+b'\0'
            va=eboot._va(self.segs,p)
            lo=self.segs[1]['off'];hi=lo+self.segs[1]['filesz']
            refs=[q for q in range(lo,hi,4) if self.orig[q:q+4]==struct.pack('>I',va)]
            self.assertTrue(refs)
            for q in refs:
                dest=eboot._off(self.segs,struct.unpack_from('>I',self.b,q)[0])
                self.assertEqual(self.b[dest:dest+len(expected)],expected)
            self.assertLess(ink(en,self.mapping,self.widths,28),900)

    def test_animation_family_and_unrelated_members(self):
        old=CPK(str(art.SOURCE));new=CPK(str(self.out/'CMN.CPK'))
        self.assertEqual(len(art.ACTION_RECTS),9)
        self.assertEqual([f['id'] for f in old.files],[f['id'] for f in new.files])
        for a,b in zip(old.files,new.files):
            if a['id']==0:art.verify(old.read(a),new.read(b),self.font)
            else:self.assertEqual(old.read(a),new.read(b))

if __name__=='__main__':unittest.main()
