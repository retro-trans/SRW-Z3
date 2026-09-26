"""Reward-message category coverage, installed hooks and exact centering."""
import json,struct,unittest
from pathlib import Path
import eboot,trdata,gift_reports as G
import president_report_layout as W
from intermission_layout import ink
from patch_gift_candidate import update,BASE,REGIONS,BACKUP
from test_president_report_layout import execute,style,expected_width


class GiftReports(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out=Path('work/out_0.6.3')
        cls.mapping=json.loads((cls.out/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((cls.out/'widths.json').read_text()).items()}
        trdata.use_glossary('analysis/glossary.json')
        cls.hooks=eboot.load_ui_hook()

    def test_complete_source_category(self):
        found=G.inventory()
        self.assertEqual(set(found),set(G.messages()))
        self.assertEqual(len(found),22)
        self.assertEqual(sum(map(len,found.values())),87)
        scopedog={jp:paths for jp,paths in found.items() if jp.startswith('スコープドッグ用')}
        self.assertEqual(len(scopedog),3)
        self.assertEqual(sum(map(len,scopedog.values())),5)

    def test_whole_and_explicit_line_hooks(self):
        doc=json.loads(G.HOOK.read_text(encoding='utf-8'))
        self.assertIs(doc['line_pairs'],False)
        self.assertEqual({r['jp']:r['en'] for r in doc['lines']},G.hooks())
        self.assertEqual(len(doc['lines']),39)
        for jp,en in G.hooks().items():
            self.assertEqual(self.hooks[jp],trdata._ex(en,str(G.HOOK)))
            self.assertEqual(len(jp.splitlines()),len(en.splitlines()))
            for line in self.hooks[jp].splitlines():
                self.assertLessEqual(ink(line,self.mapping,self.widths,28),1000)
                self.assertTrue(all(c in self.mapping for c in line),line)

    def test_emitted_reward_centering(self):
        cases=0
        for jp in G.centered_lines():
            rendered=eboot._encode_marked(self.hooks[jp],self.mapping)
            for quad,pitch,alt,flags in [(28,28,0,()),(28,32,0,()),
                                      (31,35,1,()),(20,28,1,tuple(range(0xae,0xb3)))]:
                s=style(quad,pitch,alt,flags)
                dest,x=execute(self.mapping,self.widths,jp.encode('cp932'),s)
                self.assertEqual(dest,eboot.NAME_SITE)
                self.assertAlmostEqual(x+expected_width(rendered,self.widths,s)/2,640,places=4)
                cases+=1
        print('PASS: %d emitted-PPC reward centering/register cases.'%cases)

    def test_exact_opt_in_only(self):
        import command_layout
        self.assertFalse(set(G.centered_lines())&set(command_layout.EXTRA_DIALOGS))
        for jp in G.centered_lines():
            raw=jp.encode('cp932')
            for text in (raw[:-2],raw+b'!',b'prefix'+raw):
                self.assertEqual(execute(self.mapping,self.widths,text,style(28,32)),(W.SITE+4,640))
            self.assertEqual(execute(self.mapping,self.widths,raw,style(28,32),0),(W.SITE+4,640))
        for jp in command_layout.EXTRA_DIALOGS:
            self.assertEqual(execute(self.mapping,self.widths,jp.encode('cp932'),style(28,32)),(W.SITE+4,640))

    def test_installed_hooks_and_reproducible_scoped_patch(self):
        if not BACKUP.exists():self.skipTest('Candidate not patched yet')
        before=json.loads(BASE.read_text(encoding='utf-8'))
        next_backup=Path('work/focus_EBOOT.before.bin')
        endpoint=json.loads(Path('work/focus_hooks_before.json').read_text(encoding='utf-8')) if next_backup.exists() else self.hooks
        replay,stats=update(BACKUP.read_bytes(),self.mapping,before,endpoint,json.loads(REGIONS.read_text()))
        data=(self.out/'EBOOT.BIN').read_bytes()
        self.assertEqual(replay,next_backup.read_bytes() if next_backup.exists() else data)
        self.assertEqual(stats[:2],(30,0))
        segs=eboot._segments(data);p=eboot._off(segs,eboot.NAME_TBL);table={}
        while struct.unpack_from('>I',data,p)[0]:
            k,v=struct.unpack_from('>II',data,p)
            table[eboot._cstr(data,eboot._off(segs,k))]=eboot._cstr(data,eboot._off(segs,v&0x3fffffff))
            p+=8
        import command_layout
        for jp in G.hooks():
            self.assertEqual(table[jp.encode('cp932')],command_layout.dialog_prefix(jp)+eboot._encode_marked(self.hooks[jp],self.mapping))
        W.check(data,self.mapping)


if __name__=='__main__':unittest.main()
