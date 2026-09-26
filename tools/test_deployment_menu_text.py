import json,struct,unittest
from pathlib import Path
from cpk import CPK
import aiddata,trader_art,attack_heading,eboot
import deployment_menu_text as D

class DeploymentMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        out=Path('work/out_0.6.3')
        if not (out/'AIDDATAPACK.CPK').exists():raise unittest.SkipTest('candidate unavailable')
        s=CPK('work/orig/AIDDATAPACK.CPK');b=CPK(str(out/'AIDDATAPACK.CPK'))
        cls.source=s.read(s.files[0]);cls.built=b.read(b.files[0])
        cls.art=s.read(s.files[1]);cls.built_art=b.read(b.files[1])
        cls.mapping=json.loads((out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}

    def test_source_family_inventory(self):
        refs=aiddata.refs(self.source)
        for jp in ('ＳＲポイント\n出撃チーム','ＳＲポイント\nターン数','Ｚチップ\n資金'):
            found={r for p,s,_,_ in aiddata.strings(self.source) if s==jp for r in refs.get(p,[])}
            self.assertEqual(found,{r for r,(s,_) in D.ROWS.items() if s==jp})
        for r in D.HELP:
            jp=D.ROWS[r][0]
            found={q for p,s,_,_ in aiddata.strings(self.source) if s==jp for q in refs.get(p,[])}
            self.assertTrue(found.issubset(D.HELP))

    def test_packed_labels_and_unchanged_numeric_widgets(self):
        new=D.apply(self.source,self.mapping,self.widths);D.check(self.built,self.mapping,self.widths)
        for r in D.ROWS:self.assertEqual(new[r+4:r+32],self.built[r+4:r+32])
        allowed={p for r in D.ROWS for p in range(r,r+4)}
        allowed.update(p for r in D.HELP for p in range(r+4,r+8))
        allowed.update(r+23 for r in D.HELP)
        allowed.update(p for r in D.COLONS for p in range(r+4,r+8))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(self.source,new))))

    def test_defensive_sprite_family_pixel_isolation(self):
        font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'
        before=attack_heading.apply(self.art,font)
        trader_art.verify(before,self.built_art,font)
        labels={s for t,rect,s,size in trader_art.CELLS if t==0}
        self.assertTrue({'Barrier','Shield Def.','Parry','Dbl Img'}<=labels)

    def test_robot_mafia_display_hook(self):
        b=Path('work/out_0.6.3/EBOOT.BIN').read_bytes();segs=eboot._segments(b)
        p=eboot._off(segs,eboot.NAME_TBL)
        while True:
            key,value=struct.unpack_from('>II',b,p)
            self.assertNotEqual(key,0,'Robot Mafia exact hook missing')
            k=eboot._off(segs,key)
            if b[k:b.index(b'\0',k)]=='ロボットマフィア'.encode('cp932'):
                v=eboot._off(segs,value&0x3fffffff)
                self.assertEqual(b[v:b.index(b'\0',v)],eboot._encode_marked('Robot Mafia',self.mapping))
                break
            p+=8

if __name__=='__main__':unittest.main()
