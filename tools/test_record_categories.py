"""Source inventory, text fit, and isolation for record-screen translations."""
import json
import ast
import struct
import unittest
from pathlib import Path
from cpk import CPK
import aiddata
import digraph as dg
import eboot
import trdata
import record_screen_labels as labels
import trade_list_flavor as lore
import trader_ui
from intermission_layout import text,ink


class RecordCategories(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        root=Path('work/build_0.6.9_pilot_swap_alignment')
        cls.mapping=json.loads((root/'pairs.json').read_text())
        cls.widths={int(k):v for k,v in json.loads((root/'widths.json').read_text()).items()}
        c=CPK('work/orig/AIDDATAPACK.CPK')
        cls.source=c.read(next(f for f in c.files if f['id']==0))

    def test_target_category_and_locks(self):
        hooks=eboot.load_ui_hook()
        self.assertEqual(hooks['味方単体'],'One Ally')
        self.assertEqual(hooks['敵チーム'],'Enemy Team')
        for jp,en in labels.TARGETS.items():
            self.assertEqual(hooks[jp],en)
            self.assertIn(jp,eboot.UI_JOINED)
        self.assertNotIn('？？？？',labels.hooks())
        self.assertNotIn('????',labels.hooks())

    def test_caption_and_target_widget_isolation(self):
        b=self.source
        new=labels.apply(b,self.mapping,self.widths,b)
        allowed={i for r in labels.ROWS for i in range(r,r+4)}
        for _,group in labels.TITLE_GROUPS:
            allowed.update(i for r,_ in group for i in range(r,r+4))
            allowed.update(range(group[0][0]+4,group[0][0]+8))
        allowed.update(range(0x9e704,0x9e70a))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,new))))
        self.assertEqual(b[0x9e70a:0x9e734],new[0x9e70a:0x9e734])
        refs=aiddata.refs(b)
        for jp,en in labels.ROWS.values():
            found={r for p,t,_,_ in aiddata.strings(b) if t==jp for r in refs.get(p,[])}
            self.assertEqual(found,{r for r,v in labels.ROWS.items() if v==(jp,en)})

    def test_lore_inventory_and_three_line_hooks(self):
        lore.check(self.mapping,self.widths)
        hooks=eboot.load_ui_hook()
        for jp,en in lore.hooks().items():
            self.assertEqual(hooks[jp],en)
            for original,english in zip(jp.splitlines(),en.splitlines()):
                self.assertEqual(hooks[original.strip()],english)
        self.assertIn('Focus',list(lore.hooks().values())[-1])

    def test_trade_help_caption_is_separate_from_split_heading(self):
        source=Path('work/EBOOT_dec.elf').read_bytes()
        self.assertTrue(source[0x6d9170:].startswith('トレードリスト'.encode('utf8')+b'\0'))
        rows=json.loads(Path('translation/ui_utf8.json').read_text(encoding='utf8'))['lines']
        self.assertEqual([r['en'] for r in rows if r['jp']=='トレードリスト'],['Trade List'])
        self.assertEqual([''.join(jp for _,jp in group)
                          for en,group in labels.TITLE_GROUPS if en==': Trade List'],
                         ['：トレードリスト']*2)

    def test_live_title_fragments_fit_and_keep_styles(self):
        b=self.source
        new=labels.apply(b,self.mapping,self.widths,b)
        self.assertEqual(len(labels.TITLE_GROUPS),5)
        self.assertEqual(''.join(jp for _,jp in labels.TITLE_GROUPS[0][1]),'～パイロットＴＯＰ５～')
        for en,group in labels.TITLE_GROUPS:
            r=group[0][0];left,right=labels.title_bounds(b,group)
            width=ink(en,self.mapping,self.widths,b[r+19])
            x=struct.unpack_from('>f',new,r+4)[0]*640
            self.assertAlmostEqual(x+width/2,(left+right)/2,places=4)
            self.assertGreater(x-left,4)
            self.assertGreater(right-x-width,4)
            for n,(r,_) in enumerate(group):
                self.assertEqual(new[r+8:r+32],b[r+8:r+32])
                if n:self.assertEqual(text(new,r),b'')
        # Do not depend on guessed whole-string hooks for split widgets.
        self.assertEqual(labels.hooks(),labels.TARGETS)

    def test_trade_categories_do_not_crowd_items(self):
        b=self.source
        new=trader_ui.apply(b,self.mapping,self.widths)
        trader_ui.verify(b,new,self.mapping,self.widths)
        self.assertEqual(trader_ui.ROWS[0xa26f4][1],'Upgrade Systems')
        for r in trader_ui.CATEGORY_ROWS:
            en='Systems' if r in (0xa2694,0xa2af4) else 'Power Parts'
            self.assertGreater(150-ink(en,self.mapping,self.widths,23),12)
            self.assertEqual(new[r+4:r+16],b[r+4:r+16])
            self.assertEqual(new[r+22:r+32],b[r+22:r+32])
        # No changes to item rows, lock markers, or unknown-entry text.
        allowed={i for r in trader_ui.ROWS for i in range(r,r+4)}
        allowed.update(range(0xa2534,0xa2538))
        for r in (0xa8ff4,0xa9014,0xa2d94,0xa2f54,0xa2d74,0xa2f74):
            allowed.update(range(r+4,r+8))
        allowed.update((0xa8ff4+23,0xa9014+23))
        for r in (*trader_ui.CATEGORY_ROWS,0x988b4):allowed.update(range(r+16,r+22))
        self.assertTrue(all(a==z or i in allowed for i,(a,z) in enumerate(zip(b,new))))

    def test_production_ui_passes_in_memory_without_packaging(self):
        # Execute the actual UI pass order, stopping before its first output
        # file. No archive, release, ISO or installed game file is written.
        import build_ui
        tree=ast.parse(Path('tools/build_ui.py').read_text(encoding='utf8'))
        main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        stop=next(i for i,n in enumerate(main.body) if isinstance(n,ast.Assign)
                  and any(isinstance(t,ast.Name) and t.id=='tmp' for t in n.targets))
        # First statement only rewraps process stdout; omit that for unittest.
        main.body=main.body[1:stop]+[ast.Return(value=ast.Name(id='new',ctx=ast.Load()))]
        module=ast.fix_missing_locations(ast.Module(body=[main],type_ignores=[]))
        scope=dict(vars(build_ui))
        self.assertTrue(Path('work/orig/AIDDATAPACK.CPK').is_file())
        exec(compile(module,'<in-memory UI checks>','exec'),scope)
        out=scope['main'](['build_ui.py','--out','work/build_0.6.12_approved_subtitle'])
        labels.check(out,self.mapping,self.widths,self.source)
        trader_ui.check_categories(out,self.mapping,self.widths)
        for r in trader_ui.CATEGORY_ROWS:
            expected='Systems' if r in (0xa2694,0xa2af4) else 'Power Parts'
            # Power Parts is translated by the shared hook, so its original
            # bytes may remain here; Systems is an explicit repointed label.
            if expected=='Systems':
                self.assertEqual(text(out,r),dg.encode_mixed(expected,self.mapping))

    def test_header_guards_reject_stale_source_and_bad_position(self):
        b=bytearray(self.source)
        b[0xa03f4:0xa03f8]=b[0xa03d4:0xa03d8]
        with self.assertRaises(AssertionError):
            labels.apply(b,self.mapping,self.widths,b)
        out=bytearray(labels.apply(self.source,self.mapping,self.widths,self.source))
        struct.pack_into('>f',out,0xa25f4+4,0.)
        with self.assertRaises(AssertionError):
            labels.check(out,self.mapping,self.widths,self.source)


if __name__=='__main__':unittest.main()
