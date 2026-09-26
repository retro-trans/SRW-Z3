"""Private-source regression coverage for the reported Vita screenshots."""
import sys,struct,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'platforms/vita'))
from category_port import Port,encoded
import ui_text,ui_layout,runtime_headings,scene_art
from self_decrypt import parse
from inspect_vwf import segment


class ScreenshotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port=Port();cls.candidate,cls.audit=ui_text.prepare(cls.port)
        data,base=segment(cls.candidate,parse(cls.candidate),1)
        start=int(cls.audit['table_address'],16)-base;count=struct.unpack_from('<I',data,start)[0]
        cls.rows={}
        for i in range(count):
            h,k,v=struct.unpack_from('<III',data,start+4+i*12)
            key=data[start+k:data.index(b'\0',start+k)];value=data[start+v:data.index(b'\0',start+v)]
            cls.rows[key]=value

    def test_every_reported_text_family_is_in_final_executable(self):
        cases={'修理':'Repair','精神コマンド':'Spirit','工事区画':'Construction Site',
               '１．敵の全滅。':'1. Destroy all enemies.',
               '１．ジェニオンの撃墜。':'1. The Genion is shot down.',
               '３ターン以内に敵を全滅させる。':'Destroy all enemies within 3 turns.',
               '新多元世紀０００１年　４月１０日':'New Multidimensional Century 0001 - April 10',
               '第１話『禁忌という名の希望』':'Episode 1 『A Hope Called Taboo』'}
        cases.update({'メモリーカードにセーブ':'Save to Memory Card',
                      '新規作成してよろしいですか？':'Create a new save?',
                      '上書きしてよろしいですか？':'Overwrite the existing save?',
                      'いいえ':'No','はい':'Yes'})
        cases.update({'移動':'Move','能力':'Stats','エースボーナス':'Ace Bonus',
                      'ヒビキ・カミシロ':'Hibiki Kamishiro',
                      '消費':'Use','消費\n':'SP Cost\n',
                      '＋効果':'+Eff.','回復：':'Rec:',
                      '回復：\n回復：':'Rec:\nRec:',
                      '：検索結果へ':': Back to Results',
                      '＜検索ＭＡＰ確認＞　所持ユニットを確認します。':'[Map Search] Check your units.'})
        for jp,en in cases.items():
            with self.subTest(source=jp):self.assertEqual(self.rows[jp.encode('cp932')],encoded(en,self.port.mapping))
        for group in ('spirit_hook','skill_hook'):
            definitions=self.port.catalog.document('localization/messages/'+group+'.json')['messages']
            for mid,row in definitions.items():
                jp=row.get('source')
                if jp:self.assertIn(jp.encode('cp932'),self.rows,mid)
        self.assertEqual(self.audit['groups']['date_cards'],77)
        self.assertEqual(self.audit['movement_literal_slots'],19)
        self.assertEqual(self.audit['chart_literal_slots'],1)

    def test_post_prologue_narration_and_sp_columns(self):
        import post_narration
        native=post_narration.sources(self.port)
        self.assertEqual(len(native),18)
        self.assertEqual(native['ＺＥＵＴＨの帰還直後に発生した時空震動は'],1604)
        defs=self.port.catalog.document('localization/messages/issue_hook.json')['messages']
        for jp in native:
            mid=next(mid for mid,row in defs.items() if row.get('source')==jp)
            en=self.port.text(self.port.catalog.text(mid))
            self.assertEqual(self.rows[jp.encode('cp932')],encoded(en,self.port.mapping))
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,_=ui_layout.apply(raw,self.port);widgets=ui_layout.records(raw)
        for off in (0xAD1B4,0xAD3B4):self.assertEqual(changed[widgets[off][0]],0)
        for off in (0xAD1D4,0xAD3D4):
            ptr,jp=widgets[off]
            self.assertEqual(changed[ptr:ptr+5],raw[ptr:ptr+5])
            self.assertEqual(changed[off:off+32],raw[off:off+32])

    def test_scoped_compact_headers_and_pilot_labels(self):
        import ui_widget_bindings
        from inspect_vwf import load
        original,info=load()
        archive=self.port.cpk(ui_layout.ARCHIVE)
        raw=archive.read(next(e for e in archive.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port)
        bindings=ui_widget_bindings.bindings(raw,self.port)
        self.assertEqual(len(bindings),38)
        allowed=set()
        for row in bindings:
            ptr=row['pointer'];alias=row['alias'].encode()
            self.assertEqual(changed[ptr:ptr+5],alias+b'\0')
            expected=encoded(row['text'],self.port.mapping)
            self.assertEqual(self.rows[alias],expected)
            self.assertEqual(self.rows[ui_text.converted_key(row['alias'],original,info)],expected)
            self.assertLessEqual(row['width'],row['budget'])
            allowed.update(range(ptr,ptr+5))
        # Native section pointers, coordinates, sort/cursor flags and line
        # spacing remain intact. Only labels and previously allowed sizes move.
        self.assertEqual(changed[:80],raw[:80])
        byoff={int(row['record'],16):row for row in bindings}
        for start in (0xAFEF4,0xB44D4):
            self.assertEqual([byoff[start+i*32]['text'] for i in range(4)],
                             ['Rep.','Resup','S. Atk','S. Def'])
            for i in range(3):
                off=start+i*32
                gap=(struct.unpack_from('<f',raw,off+36)[0]-struct.unpack_from('<f',raw,off+4)[0])*640
                self.assertGreaterEqual(gap-byoff[off]['width'],7.9)
        for off in range(0xA8514,0xA8614,32):
            self.assertIn(byoff[off]['text'],('Settings 1','Settings 2'))
            self.assertLess(byoff[off]['width'],210)
        for off in (0x9AC94,0xB11F4):
            self.assertEqual(byoff[off]['text'],'Atk.')
            self.assertLessEqual(byoff[off]['width']+16,94)
        self.assertEqual(self.rows['攻撃'.encode('cp932')],encoded('Attack',self.port.mapping))

    def test_native_drawer_consumes_widget_aliases_commands_and_full_name(self):
        from test_vita_ui_text import UiExecutableTests
        import ui_widget_bindings
        archive=self.port.cpk(ui_layout.ARCHIVE)
        raw=archive.read(next(e for e in archive.files if e['id']==0))
        selected=(0x99334,0xAA694,0xAB154,0xAB354,0x9AC94,0xB11F4,0xA8514,0xAFEF4,0xAFF14,0xAFF34,0xB8494,0xB8254)
        cases=[(r['alias'],r['text']) for r in ui_widget_bindings.bindings(raw,self.port)
               if int(r['record'],16) in selected]
        cases += [('移動','Move'),('能力','Stats'),('ヒビキ・カミシロ','Hibiki Kamishiro')]
        runner=UiExecutableTests();runner.candidate=self.candidate
        for source,en in cases:
            expected=[];x=100
            for ch in en:
                cell=1152+(self.port.mapping[ch]&255)-64
                expected.append((cell,x));x+=self.port.widths[ch]*24/32
            for mode,codec in ((1,'cp932'),(0,'utf-8')):
                with self.subTest(source=source,mode=mode):
                    runner.draw(source.encode(codec),mode,expected)

    def test_scope_mask_and_status_cell_indexing(self):
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port)
        self.assertEqual(len(changed),len(raw));self.assertGreater(len(audit['rows']),100)
        followup={r['record'] for r in audit['intermission_bindings'] if r['center'] is not None}
        followup.add(0xA9074)  # Parts/Network test separately checks its single centering flag.
        for off,(p,jp) in ui_layout.records(raw).items():
            if off in followup:continue
            if off in {active for row,active,jp,index in ui_layout.CHOICE_ROWS}:
                self.assertEqual(raw[off:off+4],changed[off:off+4])
                self.assertEqual(raw[off+8:off+16],changed[off+8:off+16])
            else:self.assertEqual(raw[off:off+16],changed[off:off+16])
            self.assertEqual(raw[off+21:off+32],changed[off+21:off+32])
        p,jp=ui_layout.records(raw)[0xBBDF4]
        en=self.port.catalog.text('ui_aiddata:r_e20bfd42ad95a3c9')
        self.assertEqual(changed[p:p+len(jp.encode('cp932'))],encoded(en,self.port.mapping))
        with self.assertRaises(ValueError):ui_layout.apply(changed,self.port)

    def test_right_stick_and_split_result_unit_headers(self):
        import ui_widget_bindings
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port);native=ui_layout.records(raw)
        bound={int(r['record'],16):r for r in ui_widget_bindings.bindings(raw,self.port)}
        self.assertEqual(bound[0x99334]['text'],'Right Stick')
        self.assertLess(bound[0x99334]['width']*25/32,145)
        for prefix,suffix in ((0xAA694,0xAA6B4),(0xAB354,0xAB374)):
            self.assertEqual(bound[prefix]['text'],'Unit')
            ptr,jp=native[suffix];self.assertEqual(jp,'ット')
            self.assertEqual(changed[ptr],0)
            self.assertEqual(changed[ptr+1:ptr+5],raw[ptr+1:ptr+5])
        self.assertEqual(bound[0xAB154]['text'],'Unit')
        # Other suffixes, reward amounts, EXP/PP/Score/Lv and all record
        # coordinates remain unchanged. No global Japanese fragment hooks.
        for off in (0xA46D4,0xAA654,0xAA674,0xAB174,0xAB194,0xAB1B4,0xAB1D4,0xAB1F4):
            self.assertEqual(changed[off:off+32],raw[off:off+32])
            ptr,jp=native[off];end=ptr+len(jp.encode('cp932'))+1
            self.assertEqual(changed[ptr:end],raw[ptr:end])
        self.assertNotIn('ユニ'.encode('cp932'),self.rows)
        self.assertNotIn('ット'.encode('cp932'),self.rows)

    def test_settings_tabs_and_both_confirmation_layers(self):
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port)
        rows={int(r['record'],16):r for r in audit['rows']}
        for off in range(0xA8514,0xA8614,32):
            self.assertLessEqual(rows[off]['width'],230)
            self.assertEqual(changed[off+16:off+18],bytes((24,24)))
        text,choices=ui_layout.choice_text(self.port)
        self.assertEqual(self.rows['はい　／　いいえ'.encode('cp932')],encoded(text,self.port.mapping))
        # Check actual emitted glyph advances and record positions, not only
        # the helper's returned widths. All four active/inactive states align.
        words=(self.port.catalog.text('issue_hook:r_665f01666859013b'),
               self.port.catalog.text('issue_hook:r_a571eec59b258d11'))
        for row,active,jp,index in ui_layout.CHOICE_ROWS:
            prefix=text[:text.index(words[index])]
            base=struct.unpack_from('<f',changed,row+4)[0]*640
            expected=base+sum(self.port.widths[c] for c in prefix)*ui_layout.CHOICE_FONT/32
            actual=struct.unpack_from('<f',changed,active+4)[0]*640
            if changed[active+23]&0x40:
                actual-=sum(self.port.widths[c] for c in words[index])*ui_layout.CHOICE_FONT/64
            self.assertAlmostEqual(actual,expected,places=4)
            self.assertEqual(raw[active+8:active+16],changed[active+8:active+16])
            self.assertEqual(raw[active+21:active+32],changed[active+21:active+32])
            self.assertEqual(changed[row+16:row+21],changed[active+16:active+21])
            self.assertEqual(changed[active+16],28)

    def test_scene_caption_native_sample_inventory(self):
        cpk=self.port.cpk(scene_art.ARCHIVE)
        for member,spec in scene_art.locations.SOURCES.items():
            raw=cpk.read(next(e for e in cpk.files if e['id']==member))
            with self.subTest(member=member):
                self.assertEqual(len(scene_art.samples(raw,spec['gtf'],spec['caption_rect'])),spec['sample_count'])

    def test_intermission_reward_and_attack_badge_bindings(self):
        import intermission_fixes
        from inspect_vwf import load
        executable,info=load()
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port);native=ui_layout.records(raw)
        rows=intermission_fixes.bindings(raw,self.port);self.assertEqual(len(rows),57)
        for r in rows:
            ptr=r['pointer'];self.assertEqual(changed[ptr:ptr+3],r['alias'].encode()+b'\0')
            expected=encoded(r['text'],self.port.mapping)
            self.assertEqual(self.rows[r['alias'].encode()],expected)
            self.assertEqual(self.rows[ui_text.converted_key(r['alias'],executable,info)],expected)
            self.assertLessEqual(r['width'],r['budget'])
        byoff={r['record']:r for r in rows}
        for off,en in ((0x988B4,'AT'),(0xAA794,'SR Point earned.'),
                       (0xAA7D4,'Bonus funds received: 10000.'),(0xA0234,'Intermission'),
                       (0xA3594,'Team Setup'),(0xA3314,'Pilot Swap'),(0xA3694,'D-Trader')):
            self.assertEqual(byoff[off]['text'],en)
        for off,jp in intermission_fixes.blanks(native).items():
            ptr,source=native[off];self.assertEqual(source,jp);self.assertEqual(changed[ptr],0)
            self.assertEqual(changed[ptr+1:ptr+len(jp.encode('cp932'))+1],raw[ptr+1:ptr+len(jp.encode('cp932'))+1])
        # Menu/counter records not named by this adapter remain byte-identical.
        for off in (0xA2D14,0xA2D34,0xA2D54,0xA2C94):self.assertEqual(changed[off:off+32],raw[off:off+32])

    def test_intermission_native_draws_and_matched_confirmation_pitch(self):
        import intermission_fixes
        from test_vita_ui_text import UiExecutableTests
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        runner=UiExecutableTests();runner.candidate=self.candidate
        seen=set()
        for row in intermission_fixes.bindings(raw,self.port):
            en=row['text']
            if en in seen or not en.isascii():continue
            seen.add(en);expected=[];x=100
            for ch in en:
                expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]*24/32
            for mode in (0,1):runner.draw(row['alias'].encode(),mode,expected)
        text,choices=ui_layout.choice_text(self.port)
        expected=[];x=100
        for ch in text:
            expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]*28/32
        runner.draw('はい　／　いいえ'.encode('cp932'),1,expected,font=28)
        for jp,en,(prefix,width) in zip(('はい','いいえ'),('Yes','No'),choices):
            x=100+prefix*28/32;expected=[]
            for ch in en:
                expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]*28/32
            runner.draw(jp.encode('cp932'),1,expected,font=28,origin_x=100+prefix*28/32)

    def test_roster_upgrade_library_bindings_and_preserved_widgets(self):
        import roster_library_fixes as fixes
        from inspect_vwf import load
        executable,info=load()
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port);native=ui_layout.records(raw)
        bindings=fixes.bindings(raw,self.port);self.assertEqual(len(bindings),45)
        self.assertEqual(self.audit['groups']['roster_library_aliases'],98)
        byoff={r['record']:r for r in bindings}
        for r in bindings:
            p=r['pointer'];payload=r['alias'].encode()+b'\0'
            self.assertEqual(changed[p:p+len(payload)],payload)
            self.assertEqual(self.rows[r['alias'].encode()],encoded(r['text'],self.port.mapping))
            self.assertEqual(self.rows[ui_text.converted_key(r['alias'],executable,info)],
                             encoded(r['text'],self.port.mapping))
            self.assertLessEqual(r['width'],r['budget'])
            # Includes special Library modes and fonts, coordinates, indices,
            # numeric/upgrade bars, sort flags and selection state.
            off=r['record'];self.assertEqual(changed[off:off+32],raw[off:off+32])
        for off,en in ((0xAEBD4,'[Pilot List]'),(0xAEB74,'Upgrades'),(0xAFA54,'DEF'),
                       (0xAFD74,'Wpn Rank'),(0xAF594,'Sight\nWpn Rank'),(0xA8FD4,'Library'),
                       (0xA62B4,'Robot Library'),(0xA62F4,'Character Library'),
                       (0xA6314,'Glossary'),(0xA6334,'Sound Select'),(0xA6354,'Scenario Chart')):
            self.assertEqual(byoff[off]['text'],en)
        for off in fixes.LIBRARY:
            self.assertEqual(changed[off+23],1)
            self.assertLess(byoff[off]['width']*38/32+16,475)
        for off,jp in fixes.BLANKS.items():
            p,s=native[off];self.assertEqual(s,jp);self.assertEqual(changed[p],0)
            self.assertEqual(changed[p+1:p+len(jp.encode('cp932'))+1],raw[p+1:p+len(jp.encode('cp932'))+1])
        # Other combat Defense and RANK labels are not globally overwritten.
        for off in (0xB1374,0xAF574,0xB3194,0xAFD94,0xB48D4):
            self.assertEqual(changed[off:off+32],raw[off:off+32])
            p,jp=native[off];n=len(jp.encode('cp932'))+1
            self.assertEqual(changed[p:p+n],raw[p:p+n])
        self.assertEqual(self.rows['：決定'.encode('cp932')],encoded('：Confirm',self.port.mapping))

    def test_roster_library_native_draws_and_line_split_aliases(self):
        import roster_library_fixes as fixes
        from test_vita_ui_text import UiExecutableTests
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        runner=UiExecutableTests();runner.candidate=self.candidate
        for r in fixes.bindings(raw,self.port):
            self.assertEqual(r['alias'].count('\n'),r['source'].count('\n'))
            for key,en in zip(r['alias'].split('\n'),r['text'].split('\n')):
                self.assertEqual(self.rows[key.encode()],encoded(en,self.port.mapping))
                expected=[];x=100
                for ch in en:
                    expected.append((1152+(self.port.mapping[ch]&255)-64,x))
                    x+=self.port.widths[ch]
                for mode in (0,1):runner.draw(key.encode(),mode,expected,font=32)

    def test_parts_network_slots_filter_and_unchanged_values(self):
        import parts_network_fixes as f
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port);native=ui_layout.records(raw)
        rows=f.bindings(raw,self.port);self.assertEqual(len(rows),19)
        byoff={r['record']:r for r in rows}
        for r in rows:
            p=r['pointer'];payload=r['alias'].encode()+b'\0'
            self.assertEqual(changed[p:p+len(payload)],payload)
            self.assertEqual(self.rows[r['alias'].encode()],encoded(r['text'],self.port.mapping))
            self.assertLessEqual(r['width'],r['budget'])
            off=r['record']
            if off in (0xAD194,0xAD394):
                self.assertEqual(changed[off:off+16],raw[off:off+16])
                self.assertEqual(changed[off+21:off+32],raw[off+21:off+32])
                self.assertEqual(changed[off+16:off+21],bytes((24,24,22,24,24)))
            elif off!=f.STORE:self.assertEqual(changed[off:off+32],raw[off:off+32])
        for off,en in ((0xAEB94,'[Power Parts]'),(0xAF5D4,'Equipped Power Parts'),
                       (0xAE074,': Select Slot'),(0xAFCB4,'Rep'),(0xAFCD4,'Resup'),
                       (0xB63F4,'(Team)'),(0xA9074,'PS Store'),(0xA9054,'Bonus Maps'),
                       (0xA90D4,'Upload'),(0xA90F4,'Download'),(0xAD194,'SP Cost\n')):
            self.assertEqual(byoff[off]['text'],en)
        for first in (0xAFCB4,0xB47F4):
            for off in (first,first+32):
                gap=(struct.unpack_from('<f',raw,off+36)[0]-struct.unpack_from('<f',raw,off+4)[0])*640
                self.assertGreaterEqual(gap-byoff[off]['width'],7.9)
        for off,jp in f.BLANKS.items():
            p,s=native[off];self.assertEqual(s,jp);self.assertEqual(changed[p],0)
            self.assertEqual(changed[p+1:p+len(jp.encode('cp932'))+1],raw[p+1:p+len(jp.encode('cp932'))+1])
        off=f.STORE
        self.assertEqual(changed[off:off+4],raw[off:off+4])
        self.assertEqual(changed[off+8:off+23],raw[off+8:off+23])
        self.assertEqual(changed[off+24:off+32],raw[off+24:off+32])
        self.assertEqual(changed[off+23],raw[off+23]|0x40)
        self.assertAlmostEqual(struct.unpack_from('<f',changed,off+4)[0],f.STORE_X,places=7)
        p,jp,new=f.filter_source(raw)
        self.assertEqual(changed[p:p+len(jp.encode('cp932'))],new.encode('cp932'))
        self.assertEqual(len(jp),len(new));self.assertEqual(jp.split('　')[:3],new.split('　')[:3])
        self.assertEqual(jp.split('　')[4],new.split('　')[4])
        self.assertEqual(self.rows['消費'.encode('cp932')],encoded('Use',self.port.mapping))
        self.assertEqual(self.rows[f.FILTER_ALIAS.encode('cp932')],encoded('Use',self.port.mapping))
        for off in (0xB6434,0xB64F4,0xB5D34,0xAFCF4,0xAFD14,0xAFD34):
            self.assertEqual(changed[off:off+32],raw[off:off+32])
            p,jp=native[off];end=p+len(jp.encode('cp932'))+1
            self.assertEqual(changed[p:end],raw[p:end])

    def test_parts_network_native_draws_and_scoped_sp_cost(self):
        import parts_network_fixes as f
        from test_vita_ui_text import UiExecutableTests
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        runner=UiExecutableTests();runner.candidate=self.candidate;cases=[]
        for row in f.bindings(raw,self.port):
            cases += [(key,en) for key,en in zip(row['alias'].split('\n'),row['text'].split('\n')) if key]
        cases += [('：スロット決定',': Select Slot'),('（チーム）','(Team)'),
                  ('（タッグ）','(Team)'),('消費','Use'),(f.FILTER_ALIAS,'Use')]
        for key,en in cases:
            expected=[];x=100
            for ch in en:
                expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]
            for mode,codec in ((0,'utf-8'),(1,'cp932')):
                runner.draw(key.encode(codec),mode,expected,font=32)

    def test_direct_clear_footer_both_native_paths(self):
        from test_vita_ui_text import UiExecutableTests
        from test_vita_phase_warning import native_center
        jp='クリア';en='Clear'
        self.assertEqual(self.audit['groups']['menu_followup'],2)
        for codec in ('cp932','utf-8'):
            self.assertEqual(self.rows[jp.encode(codec)],encoded(en,self.port.mapping))
        runner=UiExecutableTests();runner.candidate=self.candidate
        expected=[];x=100
        for ch in en:
            expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]
        for mode,codec in ((0,'utf-8'),(1,'cp932')):
            runner.draw(jp.encode(codec),mode,expected,font=32)
            self.assertEqual(native_center(self.candidate,jp.encode(codec),mode),[640-sum(self.port.widths[c] for c in en)/2])

    def test_remaining_team_warning_all_counts_and_native_draw(self):
        import phase_warning as warning
        from test_vita_phase_warning import native_lines,native_center
        from test_vita_ui_text import UiExecutableTests
        from inspect_vwf import load
        original,_=load()
        first,last=warning.START,warning.END
        before,base=segment(original,parse(original),0)
        after,newbase=segment(self.candidate,parse(self.candidate),0)
        self.assertEqual(before[first-base:last-base],after[first-newbase:last-newbase])
        self.assertEqual(self.audit['groups']['remaining_team_warning'],200)
        counts=list(range(1,101))
        native=native_lines(self.candidate,counts)
        for count,(jp,second) in zip(counts,native):
            en='Teams still able to act: %d.'%(count%100)
            self.assertEqual(self.rows[jp],encoded(en,self.port.mapping))
            self.assertEqual(self.rows[jp.decode('cp932').encode('utf-8')],self.rows[jp])
            self.assertLessEqual(sum(self.port.widths[c] for c in en),1000)
            self.assertEqual(self.rows[second],encoded('End the phase?',self.port.mapping))
        for fragment in (warning.PREFIX,warning.SUFFIX,warning.DIGITS):
            self.assertNotIn(fragment.encode('cp932'),self.rows)
        runner=UiExecutableTests();runner.candidate=self.candidate
        for count in (1,6,9,10,99):
            jp=native[count-1][0].decode('cp932');en='Teams still able to act: %d.'%count
            expected=[];x=100
            for ch in en:
                expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]
            for mode,codec in ((0,'utf-8'),(1,'cp932')):
                runner.draw(jp.encode(codec),mode,expected,font=32)
                width=sum(self.port.widths[c] for c in en)
                self.assertEqual(native_center(self.candidate,jp.encode(codec),mode),[640-width/2])

    def test_preset_squad_inventory_and_reported_name(self):
        import squad_names
        from test_vita_ui_text import UiExecutableTests,UiHookTests
        jp='特別捜査官';en='Special Investigator'
        self.assertEqual(self.audit['native_preset_squad_names'],242)
        self.assertIn(jp.encode('cp932'),self.port.native_squad_names)
        self.assertEqual(self.rows[jp.encode('cp932')],encoded(en,self.port.mapping))
        self.assertLessEqual(sum(self.port.widths[c] for c in en),320)
        self.assertEqual(squad_names.names('-- 特別捜査官\n"not a team", -- dialogue'),[])
        for name in ('竹尾ＧＣ','サポート'):
            escaped=name.encode('cp932').replace(b'\\',b'\\\\')
            source=(b'"'+escaped+b'", -- '+ 'チーム名'.encode('cp932')).decode('cp932')
            self.assertEqual(squad_names.names(source),[name])
        machine=UiHookTests()
        for key in (b'My Custom Squad','私のチーム'.encode('cp932'),jp.encode('cp932')+b'!'):
            self.assertNotIn(key,self.rows)
            self.assertEqual(machine.invoke(self.rows,key),(key,0x201000))
        runner=UiExecutableTests();runner.candidate=self.candidate
        expected=[];x=100
        for ch in en:
            expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]
        for mode,codec in ((0,'utf-8'),(1,'cp932')):runner.draw(jp.encode(codec),mode,expected,font=32)

    def test_split_team_labels_and_unrelated_fragments(self):
        import team_labels
        from test_vita_ui_text import UiExecutableTests
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port);native=ui_layout.records(raw)
        rows=team_labels.bindings(raw,self.port);self.assertEqual(len(rows),2)
        self.assertEqual(self.audit['groups']['team_label_aliases'],4)
        runner=UiExecutableTests();runner.candidate=self.candidate
        expected=[];x=100
        for ch in 'Team':
            expected.append((1152+(self.port.mapping[ch]&255)-64,x));x+=self.port.widths[ch]
        for r in rows:
            p=r['pointer'];self.assertEqual(changed[p:p+3],r['alias'].encode()+b'\0')
            self.assertEqual(r['text'],'Team');self.assertLessEqual(r['width'],r['budget'])
            off=r['record'];self.assertEqual(changed[off:off+32],raw[off:off+32])
            for mode in (0,1):runner.draw(r['alias'].encode(),mode,expected,font=32)
        for off,jp in team_labels.BLANKS.items():
            p,s=native[off];self.assertEqual(s,jp);self.assertEqual(changed[p],0)
            self.assertEqual(changed[p+1:p+len(jp.encode('cp932'))+1],raw[p+1:p+len(jp.encode('cp932'))+1])
            self.assertEqual(changed[off:off+32],raw[off:off+32])
        for off in (0xAD894,0xAD8B4,0xAD954):
            self.assertEqual(changed[off:off+32],raw[off:off+32])
        for fragment in ('チ','ム．','ー'):self.assertNotIn(fragment.encode('cp932'),self.rows)

    def test_semantic_glyphs_encode_as_one_cell(self):
        self.assertEqual(len(self.port.coverage),125)
        for ch in self.port.mapping:
            if ord(ch)>=0xE000:self.assertEqual(len(encoded(ch,self.port.mapping)),2)

    def test_battle_preview_widths_and_sakuya_suspend_scene(self):
        import trdata,luarec
        from category_port import patch_subset
        cpk=self.port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
        changed,audit=ui_layout.apply(raw,self.port)
        rows={int(r['record'],16):r for r in audit['rows']}
        for off in (0x9AC94,0xB11F4):
            self.assertLessEqual(rows[off]['width']+8,94)
        for off in (0xB0F34,0xB0F74,0xB0FB4,0xB0FF4):
            self.assertLessEqual(rows[off]['width']+3*rows[off]['font']+4,100)
        # The battle's Air cell and both semantic status arrays were already
        # patched by test03; verify this package still includes those changes.
        ptr,jp=ui_layout.records(raw)[0x9D614]
        self.assertEqual(changed[ptr:ptr+2],encoded(self.port.catalog.text('ui_hook:r_a60b107ea3c36a86'),self.port.mapping))
        cpk=self.port.cpk('DATA/STAGE/STG0700.cpk');native=cpk.read(next(e for e in cpk.files if e['id']==1))
        dialogue=trdata.shared_records('suspend_scene_dancouga')
        self.assertEqual([(r['event'],r['n']) for r in dialogue],[('t_057',n) for n in range(3,12)])
        self.assertTrue(dialogue[0]['en'].startswith('Sakuya\n'))
        output,total,count=patch_subset(native,dialogue,self.port.mapping,self.port.widths)
        self.assertEqual((total,count),(872,9))
        self.assertIn(encoded(dialogue[0]['en'],self.port.mapping,b'\r\n'),output)
        # Same source identities for PS3; share wording, never Vita byte offsets.
        from cpk import CPK
        ps3=ROOT/'work/save_quit/STG0700.cpk'
        if ps3.exists():
            archive=CPK(str(ps3));source=archive.read(next(e for e in archive.files if e['id']==1))
            self.assertEqual(source,native)


if __name__=='__main__':unittest.main()
