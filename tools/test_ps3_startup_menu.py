"""Startup sprite bounds, canonical wording, native UVs and archive isolation."""
import unittest
from pathlib import Path
from cpk import CPK
import startup_menu_layout as S
from localization import Catalog
from platforms.ps3 import build_link_background_update as B


class StartupMenuTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=Path('game')/B.UI_PATH
        cls.cpk=CPK(str(cls.source))
        cls.changed,cls.members=B.patch_ui(cls.source)
    def test_no_other_archive_member_or_header_changes(self):
        changed=self.changed;old=self.cpk.buf
        first=min(e['offset'] for e in self.cpk.files)
        self.assertEqual(changed[:first],old[:first])
        for e in self.cpk.files:
            p,n=e['offset'],e['size']
            if e['id'] not in (0,1):self.assertEqual(changed[p:p+n],old[p:p+n])
            else:
                raw=self.cpk.read(e)
                expected=S.apply_ui(raw) if e['id']==0 else S.apply_art(raw)
                self.assertEqual(changed[p:p+n],expected)
        self.assertEqual(len(changed),len(old))
    def test_only_heading_square_changes_in_widgets(self):
        raw=self.cpk.read(self.cpk.files[0]);changed=S.apply_ui(raw)
        S.validate_quads(changed)
        diff=[i for i,(a,b) in enumerate(zip(raw,changed)) if a!=b]
        self.assertEqual(len(diff),1) # CP932 square -> equal-width space
        import struct,aiddata
        pointer=struct.unpack_from('>I',raw,0xa1454)[0]+aiddata.STR_BASE
        self.assertEqual(diff[0],pointer+1)
        self.assertEqual(changed[pointer:pointer+2],'　'.encode('cp932'))
    def test_words_use_same_canonical_messages_as_vita_and_fit_cells(self):
        cat=Catalog()
        self.assertEqual([cat.text(r[4]) for r in S.ROWS],['Scenario Select','Main','Tutorial','Scenario'])
        for x,y,w,h,mid,stroke in S.ROWS:
            bbox=S.tile(cat.text(mid),w,h,stroke).getchannel('A').getbbox()
            self.assertGreaterEqual(bbox[0],3);self.assertLessEqual(bbox[2],w-3)
            self.assertLessEqual(abs(bbox[0]-(w-bbox[2])),1)
            self.assertLessEqual(abs(bbox[1]-(h-bbox[3])),1)


if __name__=='__main__':unittest.main()
