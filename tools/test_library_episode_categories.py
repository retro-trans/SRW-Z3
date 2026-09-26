import json
import struct
import unittest
import unicodedata
from pathlib import Path
from cpk import CPK
import aiddata
import eboot
import episode_heading_hooks as episode
import library_list_labels as library
import trdata

class Categories(unittest.TestCase):
    def test_episode_inventory_and_composed_heading(self):
        titles,records=episode.catalog();hooks=episode.hooks()
        self.assertEqual(len(titles),159)
        self.assertEqual(len({unicodedata.normalize('NFKC',t) for t,e in titles}),159)
        self.assertEqual(hooks['第１０話『魔王の誘い』'],"Episode 10 『The Demon King's Invitation』")
        self.assertEqual(hooks['第０１話『禁忌という名の希望』'],hooks['第１話『禁忌という名の希望』'])
        for n,i in records:
            if n>0:
                wide=str(n).translate(str.maketrans('0123456789','０１２３４５６７８９'))
                self.assertIn('第'+wide+'話『'+titles[i][0]+'』',hooks)
        self.assertLess(len(hooks),400)

    def test_library_source_family_and_numeric_isolation(self):
        root=Path('work/build_0.6.7_library_alignment')
        m=json.loads((root/'pairs.json').read_text());w={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c=CPK('work/orig/AIDDATAPACK.CPK');b=c.read(next(f for f in c.files if f['id']==0))
        new=library.apply(b,m,w,b);allowed=set()
        for r in library.ROWS:allowed.update(range(r,r+4))
        for r in library.TITLES:
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22));allowed.add(r+23)
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,new))))
        refs=aiddata.refs(b)
        for jp in {jp for jp,en in library.ROWS.values()}:
            # Ignore a coincidental integer inside the string pool at 0x631d4;
            # real captions in this family have the white RGBA field.
            found={r for off,t,_,_ in aiddata.strings(b) if t==jp for r in refs.get(off,[])
                   if b[r+12:r+16]==b'\xff'*4}
            self.assertEqual(found,{r for r,(t,_) in library.ROWS.items() if t==jp})

    def test_all_squads_allow_joined_draws_without_save_edits(self):
        trdata.use_glossary('analysis/glossary.json');hooks=eboot.load_ui_hook()
        rows=json.loads(Path('translation/squad_names_hook.json').read_text(encoding='utf-8'))['lines']
        self.assertEqual(len(rows),157)
        for row in rows:self.assertIn(row['jp'],eboot.UI_JOINED)
        self.assertEqual(hooks['機械獣軍団'],'Mech. Beast Army')
        self.assertNotIn('My Custom Squad',eboot.UI_JOINED)

if __name__=='__main__':unittest.main()
