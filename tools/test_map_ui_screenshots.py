"""Packed-asset regressions for Tag Commands, stat popups and Parts headers."""
import json,struct,unittest
from pathlib import Path
from cpk import CPK
import digraph as dg
import eboot
import tag_reward_layout as tag
import naming_search_layout as search
import trader_art,attack_heading
from intermission_layout import text,ink

class MapUITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=Path('work/out_0.6.3')
        if not (cls.out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('local candidate unavailable')
        cls.font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'
        cls.mapping={(k if len(k)==1 else tuple(k)):v for k,v in json.loads((cls.out/'pairs.json').read_text()).items()}
        cls.widths={int(k):v for k,v in json.loads((cls.out/'widths.json').read_text()).items()}
        old=CPK('work/orig/AIDDATAPACK.CPK');new=CPK(str(cls.out/'AIDDATAPACK.CPK'))
        read=lambda k,i:k.read(next(f for f in k.files if f['id']==i))
        cls.source=read(old,0);cls.data=read(new,0)
        cls.old_art=read(old,1);cls.art=read(new,1)

    def test_tag_commands_and_header_family(self):
        tag.check(self.data,self.mapping,self.widths)
        for row in tag.HEADERS:
            self.assertEqual(self.source[row+8:row+23],self.data[row+8:row+23])
            self.assertEqual(self.source[row+24:row+32],self.data[row+24:row+32])
        en=search.ROWS[0xa9234][1]
        self.assertEqual(text(self.data,0xa9234),dg.encode_mixed(en,self.mapping))

    def test_stat_sprite_isolation(self):
        before=attack_heading.apply(self.old_art,self.font)
        trader_art.verify(before,self.art,self.font)
        self.assertIsNone(trader_art.tile('',32,32,26,self.font).getbbox())

    def test_clear_marks_runtime_translations(self):
        blob=(self.out/'EBOOT.BIN').read_bytes();segs=eboot._segments(blob)
        def zstr(va):
            p=eboot._off(segs,va);return blob[p:blob.index(b'\0',p)]
        entries={};p=eboot._off(segs,eboot.NAME_TBL)
        while True:
            key,target=struct.unpack_from('>II',blob,p)
            if not key:break
            entries[zstr(key)]=zstr(target&0x3fffffff);p+=8
        lines={'マークは全てクリアされてしまいます。':'All marked Spirits will be cleared.',
               'よろしいですか？':'Are you sure?'}
        for jp,en in lines.items():
            self.assertEqual(entries[jp.encode('cp932')],eboot._encode_marked(en,self.mapping))
            self.assertLess(ink(en,self.mapping,self.widths,28),900)
        source=Path('work/EBOOT_dec.elf').read_bytes()
        # The constructor copies fixed UTF-8 byte counts: never translate its
        # literals in place; conversion precedes the runtime lookup above.
        for jp in lines:
            key=jp.encode('utf-8')+b'\0';start=0;count=0
            while True:
                start=source.find(key,start)
                if start<0:break
                self.assertEqual(blob[start:start+len(key)],key);start+=len(key);count+=1
            self.assertGreater(count,0)
        self.assertEqual(blob[0x7c6a60:0x7c6a68],source[0x7c6a60:0x7c6a68])

if __name__=='__main__':unittest.main()
