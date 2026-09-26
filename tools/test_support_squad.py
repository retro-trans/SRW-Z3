"""Source-driven regressions for the September 13 map screenshots."""
import json
import struct
import unittest
from pathlib import Path
from PIL import ImageFont
import squad_names
import support_popup_layout as layout
import trader_art
import trdata
import eboot
from cpk import CPK

FONT='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'


class SupportSquadTests(unittest.TestCase):
    def test_word_geometry_and_isolation(self):
        k=CPK('work/orig/AIDDATAPACK.CPK')
        source=k.read(k.files[0]);built=layout.apply(source)
        layout.verify(source,built)
        allowed={p+i for p,_ in layout.changes(source) for i in range(4)}
        self.assertEqual(len(source),len(built))
        self.assertTrue(all(a==b or i in allowed for i,(a,b) in enumerate(zip(source,built))))
        # Independently scan the atlas UVs: every shared word quad, not only
        # the two reported vertices, must be included in the patch inventory.
        for tx,w in ((0,72),(72,72),(144,72),(216,40)):
            uv=((tx+w/2,108),(tx,88),(tx+w,88),(tx+w,128),(tx,128))
            found={p for p in range(0,len(source)-80,4)
                   if all(struct.unpack_from('>2f',source,p+i*16+8)==(u/512,v/512)
                          for i,(u,v) in enumerate(uv))}
            self.assertEqual(found,{p for group in layout.GROUPS for p,x,_,_ in group if x==tx})
        for group in layout.GROUPS:
            def center(blob):
                a,z=group[0],group[-1]
                wa,wz=(a[2],z[2]) if blob is source else (a[3],z[3])
                return (struct.unpack_from('>f',blob,a[0])[0]*640-wa/2+
                        struct.unpack_from('>f',blob,z[0])[0]*640+wz/2)/2
            self.assertAlmostEqual(center(source),center(built),places=4)

    def test_restored_font_aspect(self):
        font=ImageFont.truetype(FONT,120)
        for word,native_width in [('Support',132),('Defend',118),('Attack',106)]:
            tile=trader_art.tile(word,72,40,30,FONT)
            l,t,r,b=tile.getbbox()
            x0,y0,x1,y1=font.getbbox(word)
            actual=(r-l)*native_width/72/(b-t)
            natural=(x1-x0)/(y1-y0)
            self.assertLess(abs(actual/natural-1),.12,word)
            self.assertLess(b,40)

    def test_lua_escaped_trail_byte_and_category(self):
        # Escaping must happen before CP932 decoding: both names contain
        # characters whose second byte is a backslash.
        for jp in ['竹尾ＧＣ','サポート','ＴＤＤ－１','クラッシャー隊']:
            escaped=jp.encode('cp932').replace(b'\\',b'\\\\')
            source=(b'"'+escaped+b'", -- '+ 'チーム名'.encode('cp932')).decode('cp932')
            self.assertEqual(squad_names.names(source),[jp])
        self.assertEqual(squad_names.names('-- クラッシャー隊\n"not a team", -- dialogue'),[])

    def test_preset_category_coverage(self):
        from audit_message_classes import inventory
        trdata.use_glossary('analysis/glossary.json')
        hooks=eboot.load_ui_hook()
        rows,stages=inventory()
        squads={r['jp'] for r in rows if r['class']=='squad-name'}
        self.assertGreaterEqual(len(stages),142)
        self.assertGreaterEqual(len(squads),157)
        self.assertFalse(squads-hooks.keys(),squads-hooks.keys())
        self.assertEqual(hooks['クラッシャー隊'],'Crusher Squad')
        self.assertEqual(hooks['ロボットマフィア'],'Robot Mafia')
        self.assertNotIn('My Custom Squad',hooks)
        print('Covered %d unique preset squad names across %d archives.'%(len(squads),len(stages)))

if __name__=='__main__':unittest.main()
