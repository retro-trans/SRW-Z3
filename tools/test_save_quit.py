"""Regression tests for save-line centering, end-session script and trophy text."""
import json
import re
import struct
import unittest
from pathlib import Path
import command_layout as C
import digraph as dg
import eboot
import suspend_scene as S
import trophy_labels as T
import trdata
from cpk import CPK
from check_confirmation_tabs import execute

ROOT=Path(__file__).resolve().parents[1]

class SaveQuitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary(str(ROOT/'analysis/glossary.json'))
        cls.mapping=json.loads((ROOT/'work/out_0.6.2/pairs.json').read_text())

    def test_save_lines_have_independent_pads(self):
        hooks=eboot.load_ui_hook()
        for jp,en in C.SAVE_DIALOGS.items():
            self.assertEqual(hooks[jp],en)
            self.assertEqual(C.count_coefficient(C.dialog_index(jp)),len(jp)/2.)
        a=C.dialog_index('セーブが終了しました。');b=C.dialog_index('このままゲームを続けますか？')
        self.assertNotEqual(a,b)
        wd={int(k):v for k,v in json.loads((ROOT/'work/out_0.6.2/widths.json').read_text()).items()}
        widths=bytes(wd.get(i,32) for i in range(eboot.ATLAS_CELLS))
        data=b''.join(struct.pack('>ff',C.count_coefficient(i),sum(widths[dg.cell_index(self.mapping[c])] for c in label)/64.) for i,label in enumerate(C.LABELS))
        extra=((C.CAVE,C.stub()),(C.DATA,data))
        for index in range(C.SAVE_START,len(C.LABELS)):
            ink=sum(widths[dg.cell_index(self.mapping[c])] for c in C.LABELS[index])
            for pitch,quad in [(31,28),(28,31),(42,25)]:
                origin=640-C.count_coefficient(index)*pitch
                advance,_=execute(eboot.vwf_stub(),widths,dg.cell_index(C.CODES[index]),origin,origin,pitch,quad,0,extra)
                self.assertAlmostEqual(origin+advance+ink*quad/64,640,places=3)

    def test_scene_only_sixteen_bodies_change(self):
        source=ROOT/'work/save_quit/STG0700.cpk'
        if not source.exists():self.skipTest('local source unavailable')
        k=CPK(str(source));old=k.read(next(f for f in k.files if f['id']==1))
        new=S.patch(old,self.mapping)
        pattern=re.compile(rb'(?<!--)\[\[(.*?)\]\]',re.S)
        before=list(pattern.finditer(old));after=list(pattern.finditer(new))
        self.assertEqual(len(before),len(after))
        changed=[i for i,(a,b) in enumerate(zip(before,after)) if a.group(1)!=b.group(1)]
        import luarec
        records=luarec.records(old.decode('cp932'))
        added=[i for i,r in enumerate(records) if r['event']=='t_057' and 3<=r['n']<=11]
        self.assertEqual(len(added),9)
        self.assertEqual(changed,sorted(list(range(563,570))+added))
        # Replacing all literal bodies with one marker exposes every command,
        # voice cue, event identity, face state and wait/timing byte unchanged.
        self.assertEqual(pattern.sub(b'[[TEXT]]',old),pattern.sub(b'[[TEXT]]',new))
        bad=old.replace('お疲れ様、今日はここまでにしておくかい？'.encode('cp932'),'お早う様、今日はここまでにしておくかい？'.encode('cp932'),1)
        with self.assertRaises(AssertionError):S.patch(bad,self.mapping)

    def test_left_aligned_notification_is_isolated(self):
        import save_prompt_layout as layout
        original=(ROOT/'work/deploy_locations/aid_original.bin').read_bytes()
        result=layout.apply(original,self.mapping)
        self.assertEqual(original[layout.ROW+4:layout.ROW+32],result[layout.ROW+4:layout.ROW+32])

    def test_trophy_metadata_and_checksum(self):
        path=ROOT/'work/orig/TROPHY.TRP'
        if not path.exists():path=Path('E:/SRWZ3/PS3_GAME/TROPDIR/NPWR05207_00/TROPHY.TRP')
        if not path.exists():self.skipTest('local trophy source unavailable')
        original=path.read_bytes();built=T.apply(original);T.verify(original,built)
        broken=bytearray(built);broken[-1]^=1
        with self.assertRaises(AssertionError):T.verify(original,bytes(broken))

    def test_distribution_paths(self):
        import deploy,extract,apply_xdelta,iso_patch
        for table in [deploy.LAYOUT,extract.DISC,apply_xdelta.LAYOUT]:
            self.assertEqual(table['STG0700.SDAT'],'DATA/STAGE')
            self.assertEqual(table['TROPHY.TRP'],'../TROPDIR/NPWR05207_00')
        self.assertEqual(iso_patch.shipped_paths()['TROPHY.TRP'],['PS3_GAME','TROPDIR','NPWR05207_00','TROPHY.TRP'])

if __name__=='__main__':unittest.main()
