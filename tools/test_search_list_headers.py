"""Verify the reported Spirit/Skills list family in the packed candidate."""
import json,unittest
from pathlib import Path
from cpk import CPK
import aiddata
import search_list_headers as headers
import trader_art,attack_heading
from intermission_layout import text

class SearchListHeaderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out=Path('work/out_0.6.3')
        if not (out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('local candidate unavailable')
        old=CPK('work/orig/AIDDATAPACK.CPK');new=CPK(str(out/'AIDDATAPACK.CPK'))
        read=lambda k,i:k.read(next(f for f in k.files if f['id']==i))
        cls.old=read(old,0);cls.new=read(new,0)
        cls.oldart=read(old,1);cls.newart=read(new,1)
        cls.mapping=json.loads((out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}

    def test_packed_columns_fit_and_preserve_state(self):
        headers.check(self.new,self.mapping,self.widths)
        for r in headers.ROWS:self.assertEqual(self.old[r+4:r+32],self.new[r+4:r+32])
        for r in (0xad1d4,0xad3d4):self.assertEqual(self.old[r:r+32],self.new[r:r+32])

    def test_category_inventory(self):
        refs=aiddata.refs(self.old)
        for jp,wanted in [('消費\n',{0xad194,0xad394}),('使用回数\n',{0xad154}),('＋効果',{0xad1f4,0xad3f4})]:
            found=set()
            for off,label,_,_ in aiddata.strings(self.old):
                if label==jp:found.update(refs.get(off,[]))
            self.assertEqual(found,wanted)
            self.assertTrue(found<=headers.ROWS.keys())

    def test_shared_battle_word_sprites(self):
        font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'
        trader_art.verify(attack_heading.apply(self.oldart,font),self.newart,font)
        labels={en for _,_,en,_ in trader_art.CELLS}
        self.assertTrue({'Support','Attack','Defend','Re-','Counter','Center','Wide','Map','Wpn','Song','Maximum','Break'}<=labels)

if __name__=='__main__':unittest.main()
