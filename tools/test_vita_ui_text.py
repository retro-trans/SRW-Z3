"""Execute real generated Thumb UI hook and original Vita drawer on Unicorn."""
from pathlib import Path
import struct
import sys
import unittest
from unittest import mock
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'platforms/vita'))
import ui_text as UI
import vwf
from test_vita_vwf import bits, number
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import *


class UiHookTests(unittest.TestCase):
    def test_percentages_are_not_printf_placeholders(self):
        for text in ('Hit rate and evasion +30% for 1 turn.',
                     'Assist Attack damage +5% per available support use.',
                     'Recover 10% of maximum HP.'):
            self.assertFalse(UI.has_format(text,english=True))
        for text in ('%s', '%d turns', '%02d', '% f', '30% for %d turns'):
            self.assertTrue(UI.has_format(text,english=True))

    def machine(self,rows,text_shift=0,data_shift=0):
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
        start=vwf.TEXT_END+296+text_shift
        u.mem_map((start&~4095),4096)
        # Stub ADR must shift with code. Assembly's absolute literal address
        # is compiled at original VA; load bytes rather than reassembling.
        u.mem_write(start,UI.stub(vwf.TEXT_END+296))
        target=0x8168C620+data_shift
        payload=UI.table(rows)
        u.mem_map(target&~4095,((target%4096+len(payload)+4095)//4096)*4096)
        u.mem_write(target,payload)
        pointer=UI.POINTER+text_shift
        u.mem_write(pointer,struct.pack('<I',(target-pointer)&0xFFFFFFFF))
        u.mem_map(0x200000,0x10000)
        u.reg_write(UC_ARM_REG_CPSR,0xA8000030)
        u.reg_write(UC_ARM_REG_SP,0x208000)
        u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20)
        u.reg_write(UC_ARM_REG_FPEXC,1<<30)
        return u,start,target

    def invoke(self,rows,key,text_shift=0,data_shift=0):
        u,start,target=self.machine(rows,text_shift,data_shift)
        u.mem_write(0x201000,key+b'\0')
        regs=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,
              UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R8,
              UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,
              UC_ARM_REG_S1,UC_ARM_REG_S2]
        for i,r in enumerate(regs):u.reg_write(r,100+i)
        before=[u.reg_read(r) for r in regs]
        u.reg_write(UC_ARM_REG_R7,0x201000);u.reg_write(UC_ARM_REG_LR,0x200001)
        flags=u.reg_read(UC_ARM_REG_CPSR)&0xF8000000
        # Full-catalog misses scan more entries than the small synthetic
        # fixtures. Keep a bounded budget large enough for the shipped table.
        u.emu_start(start|1,0x200000,count=100000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
        self.assertEqual([u.reg_read(r) for r in regs],before)
        self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
        self.assertEqual(u.reg_read(UC_ARM_REG_LR),0x200001)
        self.assertEqual(u.reg_read(UC_ARM_REG_CPSR)&0xF8000000,flags)
        self.assertEqual(number(u.reg_read(UC_ARM_REG_S0)),-1)
        p=u.reg_read(UC_ARM_REG_R7);out=bytearray()
        while True:
            b=bytes(u.mem_read(p+len(out),1))
            if b==b'\0':break
            out+=b
        return bytes(out),p

    def test_exact_match_and_independent_segment_relocation(self):
        key='ページ切換え'.encode('cp932')
        for t,d in ((0,0),(0x1000000,0x2000000),(0x2000000,0x1000000)):
            result,p=self.invoke({key:b'\x87\x41\x87\x42'},key,t,d)
            self.assertEqual(result,b'\x87\x41\x87\x42')
            self.assertNotEqual(p,0x201000)

    def test_full_compare_rejects_hash_collision_and_prefix(self):
        self.assertEqual(UI.hash_key(b'Aa'),UI.hash_key(b'B@'))
        rows={b'Aa':b'first',b'B@':b'second'}
        self.assertEqual(self.invoke(rows,b'Aa')[0],b'first')
        self.assertEqual(self.invoke(rows,b'B@')[0],b'second')
        for key in (b'A',b'Aaa',b'',b'Unknown'):
            self.assertEqual(self.invoke(rows,key),(key,0x201000))

    def test_empty_output_is_supported_but_bad_table_refused(self):
        self.assertEqual(self.invoke({b'caption':b''},b'caption')[0],b'')
        for rows in ({},{b'':b'x'},{b'a\0b':b'x'},{b'a':b'x\0y'}):
            with self.assertRaises(ValueError):UI.table(rows)

    def test_1510_entry_table_last_match_and_unmatched(self):
        rows={('key%04d'%i).encode():('value%04d'%i).encode() for i in range(1510)}
        self.assertEqual(self.invoke(rows,b'key1509')[0],b'value1509')
        self.assertEqual(self.invoke(rows,b'absent'),(b'absent',0x201000))

    def test_description_wrapper_preserves_caller_and_handles_null(self):
        rows={b'whole\nsource':b'first\nsecond\nthird',b'blank':b''}
        for shift,data_shift in ((0,0),(0x1000000,0x2000000)):
            for key in (None,b'',b'missing',b'blank',b'whole\nsource'):
                u,lookup,target=self.machine(rows,shift,data_shift)
                address=lookup+len(UI.stub(vwf.TEXT_END+296))
                u.mem_write(address,UI.description_stub(address-shift,lookup-shift))
                regs=[UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,
                      UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,
                      UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,
                      UC_ARM_REG_S0,UC_ARM_REG_S1,UC_ARM_REG_S2]
                for i,r in enumerate(regs):u.reg_write(r,100+i)
                source=0 if key is None else 0x201000
                if key is not None:u.mem_write(source,key+b'\0')
                u.reg_write(UC_ARM_REG_R2,source)
                before=[u.reg_read(r) for r in regs]
                u.reg_write(UC_ARM_REG_LR,0x200001)
                u.emu_start(address|1,0x200000,count=20000)
                self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
                self.assertEqual([u.reg_read(r) for r in regs],before)
                self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
                self.assertEqual(u.reg_read(UC_ARM_REG_LR),0x200001)
                self.assertEqual(struct.unpack('<I',u.mem_read(0x208018,4))[0],before[0])
                p=u.reg_read(UC_ARM_REG_R0)
                self.assertEqual(u.reg_read(UC_ARM_REG_CPSR)&0xF8000000,
                                 0x08000000 | (0x40000000 if p==0 else p&0x80000000))
                if key in rows:
                    self.assertEqual(bytes(u.mem_read(p,len(rows[key])+1)),rows[key]+b'\0')
                else:self.assertEqual(p,source)

    def test_native_line_buffer_limit_counts_each_encoded_line(self):
        UI.table({b'a':b'x'*256+b'\n'+b'y'*256})
        with self.assertRaises(ValueError):UI.table({b'a':b'x'*257})

    def test_catalog_filters_conflicts_private_glyphs_formats_and_links(self):
        definitions={
            'ui_hook':{'ui_hook:a':{'source':'選択'},'ui_hook:b':{'source':'不明'},
                       'ui_hook:c':{'source':'数値%d'},'ui_hook:d':{'source':'部品'},
                       'ui_hook:e':{'source':'《言葉》'},'ui_hook:f':{'source':None},
                       'ui_hook:g':{'source':'長文'}},
            'ui_utf8':{'ui_utf8:a':{'source':'不明'}}}
        values={'ui_hook:a':'Select','ui_hook:b':'Unknown','ui_hook:c':'Value %d',
                'ui_hook:d':'\ue000','ui_hook:e':'《Word》','ui_hook:f':'Missing','ui_utf8:a':'Other',
                'ui_hook:g':'x'*129}
        catalog=SimpleNamespace(manifest={'groups':list(definitions)},text=lambda mid:values[mid],
            document=lambda path:{'messages':definitions[Path(path).stem]})
        port=SimpleNamespace(catalog=catalog,text=lambda v:v,
                             mapping={chr(n):0x8700+n for n in range(32,127)},width_bank=bytes([12]*192))
        native={r['source'].encode('cp932') for d in definitions.values() for r in d.values() if r['source']}
        captured=[]
        def build(original,widths,rows,**kwargs):captured.append(rows);return b'candidate',{}
        with mock.patch.object(UI,'native_sources',return_value=(b'',{},[],native,10)),mock.patch.object(UI,'load',return_value=(b'',{})),mock.patch.object(UI,'patch',side_effect=build):
            _,audit=UI.prepare(port)
        self.assertEqual(set(captured[0]),{'選択'.encode('cp932')})
        for reason in ('conflicting_source','platform_private_glyph','runtime_format_or_control','keyword_link','no_source','native_line_buffer_limit'):
            self.assertEqual(audit['skipped'][reason],1)

    def test_widget_caption_preference_is_scoped_and_names_are_display_only(self):
        definitions={
            'ui_aiddata':{'ui_aiddata:finish':{'source':'設定終了'}},
            'ui.key_help_labels':{'ui.key_help_labels:finish':{'source':'設定終了'}},
            'ui.runtime_names':{'ui.runtime_names:first':{'source':'ヒビキ'}}}
        values={'ui_aiddata:finish':'Done','ui.key_help_labels:finish':'Finish Settings',
                'ui.runtime_names:first':'Hibiki'}
        catalog=SimpleNamespace(manifest={'groups':list(definitions)},text=lambda mid:values[mid],
            document=lambda path:{'messages':definitions[Path(path).stem]})
        port=SimpleNamespace(catalog=catalog,text=lambda v:v,
                             mapping={chr(n):0x8700+n for n in range(32,127)},width_bank=bytes([12]*192))
        finish='設定終了'.encode('cp932');name='ヒビキ'.encode('cp932')
        region=b'\0'+finish+b'\0'+name+b'\0';captured=[]
        def build(original,widths,rows,**kwargs):captured.append(rows);return b'candidate',{}
        for widgets in ({finish},set()):
            with mock.patch.object(UI,'native_sources',return_value=(b'',{},[region],widgets,1)),mock.patch.object(UI,'load',return_value=(b'',{})),mock.patch.object(UI,'patch',side_effect=build),mock.patch('runtime_names_vita.rows',return_value={}):
                _,audit=UI.prepare(port)
            rows=captured[-1]
            self.assertEqual(finish in rows,bool(widgets))
            if widgets:self.assertEqual(rows[finish],UI.encoded('Done',port.mapping))
            self.assertEqual(rows[name],UI.encoded('Hibiki',port.mapping))
            self.assertEqual(self.invoke(rows,name)[0],rows[name])
            for custom in ('アキラ','ヒビキＡ','ヒビキ改'):
                key=custom.encode('cp932')
                self.assertEqual(self.invoke(rows,key),(key,0x201000))


class UiExecutableTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from inspect_vwf import load,PILOT
        if not PILOT.exists():raise unittest.SkipTest('Private original executable required')
        cls.original,cls.original_info=load();cls.widths=bytes([12]*192)
        cls.key='検索'.encode('cp932')
        cls.mixed='PP回復'
        cls.converted=UI.converted_key(cls.mixed,cls.original,cls.original_info)
        cls.candidate,cls.audit=UI.patch(cls.original,cls.widths,
            {cls.key:bytes.fromhex('87418742'),cls.converted:bytes.fromhex('87418742')})

    def test_source_guard_and_two_independent_relocations(self):
        info=vwf.parse(self.candidate);base,base_audit=vwf.patch(self.original,self.widths)
        old=vwf.parse(base)
        self.assertEqual(info['phdrs'][0][2],old['phdrs'][0][2])
        self.assertEqual(info['phdrs'][1][2],old['phdrs'][1][2])
        original_reloc=base[old['infos'][3][0]:sum(old['infos'][3][:2])]
        new_reloc=self.candidate[info['infos'][3][0]:sum(info['infos'][3][:2])]
        self.assertEqual(new_reloc[:-12],original_reloc)
        self.assertEqual(new_reloc[-12:].hex(),self.audit['relocation'])
        with self.assertRaises(ValueError):UI.patch(self.candidate,self.widths,{self.key:b'x'})

    def test_native_center_uses_translated_width_for_sjis_and_utf8(self):
        rows={self.key:bytes.fromhex('87418742'),'検索'.encode('utf-8'):bytes.fromhex('87418742')}
        candidate,audit=UI.patch(self.original,self.widths,rows,birthday=True)
        for mode,key,known in ((1,self.key,True),(0,'検索'.encode('utf-8'),True),
                               (1,'不明'.encode('cp932'),False)):
            u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x81000000,0x6A0000)
            info=vwf.parse(candidate)
            for i in (0,1):
                off,n=info['infos'][i][:2];u.mem_write(info['phdrs'][i][2],candidate[off:off+n])
            u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
            u.reg_write(UC_ARM_REG_SP,0x208000);u.reg_write(UC_ARM_REG_LR,0x200001)
            u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20);u.reg_write(UC_ARM_REG_FPEXC,1<<30)
            state=0x8138AA58;u.mem_write(state,bytes(0x78))
            u.mem_write(state+0x14,struct.pack('<f',24));u.mem_write(state+0x1c,struct.pack('<f',31))
            u.mem_write(0x201000,key+b'\0');u.reg_write(UC_ARM_REG_R0,0x201000)
            u.reg_write(UC_ARM_REG_R1,mode);u.reg_write(UC_ARM_REG_R2,0)
            u.reg_write(UC_ARM_REG_S0,bits(100));u.reg_write(UC_ARM_REG_S1,bits(200))
            u.reg_write(UC_ARM_REG_S2,bits(0));positions=[]
            def external(cpu,address,size,data):
                if address==0x8121DC30:cpu.reg_write(UC_ARM_REG_R0,len(key))
                elif address==0x8121DA90:cpu.reg_write(UC_ARM_REG_R0,len(key.decode('utf-8')))
                elif address==0x81006E10:positions.append(number(cpu.reg_read(UC_ARM_REG_S0)))
                else:return
                cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
            u.hook_add(UC_HOOK_CODE,external);u.emu_start(0x8100791F,0x200000,count=20000)
            self.assertEqual(positions,[91 if known else 69])
            self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)

    def test_birthday_drawer_keeps_all_calendar_values_and_only_changes_suffixes(self):
        candidate,audit=UI.patch(self.original,self.widths,{self.key:b'x'},birthday=True)
        info=vwf.parse(candidate)
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x81000000,0x6A0000)
        for i in (0,1):
            off,size=info['infos'][i][:2]
            u.mem_write(info['phdrs'][i][2],candidate[off:off+size])
        u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
        u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20);u.reg_write(UC_ARM_REG_FPEXC,1<<30)
        draws=[]
        def draw(cpu,address,size,data):
            if address==0x810073C0:draws.append(cpu.reg_read(UC_ARM_REG_R0))
            elif address==0x81007916:
                p=cpu.reg_read(UC_ARM_REG_R0)
                draws.append(bytes(cpu.mem_read(p,3)))
            else:return
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        u.hook_add(UC_HOOK_CODE,draw)
        u.mem_write(0x202004,struct.pack('<I',0x203000))
        u.mem_write(0x812DF168,struct.pack('<ii',120,322))
        for month in range(1,13):
            for day in range(1,32):
                values=struct.pack('<II',month-1,day-1)
                u.mem_write(0x2031C0,values);draws.clear()
                u.reg_write(UC_ARM_REG_R4,0x202000);u.reg_write(UC_ARM_REG_SP,0x208000)
                u.emu_start(0x8106DA1B,0x8106DADA,count=200)
                self.assertEqual(draws,[month,'／'.encode('cp932')+b'\0',day])
                self.assertEqual(bytes(u.mem_read(0x2031C0,8)),values)
        # Other date uses still see the native Japanese suffix strings.
        self.assertEqual(bytes(u.mem_read(0x8125BF4C,3)),'月'.encode('cp932')+b'\0')
        self.assertEqual(bytes(u.mem_read(0x8125BF50,3)),'日'.encode('cp932')+b'\0')
        self.assertTrue(audit['birthday_draw_only'])

    def test_birthday_tail_stub_relocates_with_text_and_preserves_draw_arguments(self):
        address=0x812B5F04;code=UI.birthday_stub(address)
        for shift in (0,0x1000000):
            u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map((address+shift)&~4095,4096)
            u.mem_write(address+shift,code)
            for r,v in ((UC_ARM_REG_CPSR,0xA8000030),(UC_ARM_REG_R1,1),(UC_ARM_REG_R2,42),
                        (UC_ARM_REG_LR,0x12345),(UC_ARM_REG_SP,0x20000)):
                u.reg_write(r,v)
            target=0x81007916+shift;u.mem_map(target&~4095,4096)
            u.emu_start((address+shift)|1,target,count=3)
            self.assertEqual(u.reg_read(UC_ARM_REG_PC),target)
            self.assertEqual(u.reg_read(UC_ARM_REG_R0),address+shift+8)
            for r,v in ((UC_ARM_REG_R1,1),(UC_ARM_REG_R2,42),(UC_ARM_REG_LR,0x12345),(UC_ARM_REG_SP,0x20000)):
                self.assertEqual(u.reg_read(r),v)
            self.assertEqual(u.reg_read(UC_ARM_REG_CPSR)&0xF8000000,0xA8000000)

    def test_ui_candidate_accepts_separate_native_voice_table_edit(self):
        from category_port import replace_voice_table
        info=vwf.parse(self.candidate)
        location=dict(segment=1,relative_offset=433180)
        at=info['infos'][1][0]+location['relative_offset']
        old=list(struct.unpack_from('<277I',self.candidate,at))
        # Synthetic new offsets exercise composition only, not SRVC content.
        new=[v*2 for v in old]
        changed=replace_voice_table(self.candidate,location,old,new)
        self.assertEqual(replace_voice_table(changed,location,new,old),self.candidate)

    def test_original_description_entry_counts_translated_lines(self):
        key='説明\n文章'.encode('cp932');value=bytes.fromhex('8741')+b'\n'+bytes.fromhex('8742')+b'\n'+bytes.fromhex('8743')
        candidate,audit=UI.patch(self.original,self.widths,{key:value})
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x81000000,0x6A0000)
        info=vwf.parse(candidate)
        for i in (0,1):
            off,size=info['infos'][i][:2]
            u.mem_write(info['phdrs'][i][2],candidate[off:off+size])
        u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
        u.reg_write(UC_ARM_REG_SP,0x208000);u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20)
        u.reg_write(UC_ARM_REG_FPEXC,1<<30)
        u.mem_write(0x201000,key+b'\0');u.reg_write(UC_ARM_REG_R2,0x201000)
        # Only imported strlen is intercepted. The original entry, null
        # checks, cached pointer and native line counter run unmodified.
        def strlen(cpu,address,size,data):
            if address!=0x8121DC30:return
            p=cpu.reg_read(UC_ARM_REG_R0);n=0
            while bytes(cpu.mem_read(p+n,1))!=b'\0':n+=1
            cpu.reg_write(UC_ARM_REG_R0,n)
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        u.hook_add(UC_HOOK_CODE,strlen)
        u.emu_start(0x810D9DC5,0x810D9DF2,count=20000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x810D9DF2)
        self.assertEqual(u.reg_read(UC_ARM_REG_R0),3)
        p=struct.unpack('<I',u.mem_read(u.reg_read(UC_ARM_REG_SP)+0x14,4))[0]
        self.assertEqual(bytes(u.mem_read(p,len(value)+1)),value+b'\0')

    def draw(self,source,mode,expected=None,font=24,origin_x=100):
        # Unicorn owns large native translation buffers behind small Python
        # callback cycles. Collect previous machines before the next case,
        # especially with the 32-bit Python runtime used by this workspace.
        import gc
        gc.collect()
        info=vwf.parse(self.candidate)
        end=max(p[2]+p[5] for p in info['phdrs'][:2])
        u=Uc(UC_ARCH_ARM,UC_MODE_THUMB);u.mem_map(0x81000000,(end-0x81000000+4095)&~4095)
        for i in (0,1):
            off,size=info['infos'][i][:2]
            u.mem_write(info['phdrs'][i][2],self.candidate[off:off+size])
        u.mem_map(0x200000,0x10000);u.reg_write(UC_ARM_REG_CPSR,0x30)
        u.reg_write(UC_ARM_REG_SP,0x208000);u.reg_write(UC_ARM_REG_C1_C0_2,0xF<<20)
        u.reg_write(UC_ARM_REG_FPEXC,1<<30)
        state=0x8138AA58;u.mem_write(state,bytes(0x78));quads=[]
        for off,value in ((0x14,font),(0x18,font),(0x1C,31),(0x20,32)):
            u.mem_write(state+off,struct.pack('<f',value))
        noops={0x8100985E,0x810095D0,0x8100986A,0x81009DA8,0x81009776,0x81008F64}
        def gpu(cpu,address,size,data):
            if address==0x8121DA90:
                # Imported UTF-8 -> UCS2 routine only. The original game's
                # UCS2 -> native font lookup/converter below runs untouched.
                p=cpu.reg_read(UC_ARM_REG_R1);s=bytearray()
                while bytes(cpu.mem_read(p+len(s),1))!=b'\0':s+=cpu.mem_read(p+len(s),1)
                text=bytes(s).decode('utf-8')
                cpu.mem_write(cpu.reg_read(UC_ARM_REG_R0),text.encode('utf-16le')+b'\0\0')
                cpu.reg_write(UC_ARM_REG_R0,len(text))
            elif address==0x8100970A:cpu.reg_write(UC_ARM_REG_R0,0x202000)
            elif address==0x8100973C:quads.append((cpu.reg_read(UC_ARM_REG_R9),number(cpu.reg_read(UC_ARM_REG_S0))))
            elif address not in noops:return
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        u.hook_add(UC_HOOK_CODE,gpu)
        u.mem_write(0x201000,source+b'\0');u.reg_write(UC_ARM_REG_R0,0x201000)
        u.reg_write(UC_ARM_REG_R1,mode);u.reg_write(UC_ARM_REG_S0,bits(origin_x))
        u.reg_write(UC_ARM_REG_S1,bits(200));u.reg_write(UC_ARM_REG_S2,bits(0))
        u.reg_write(UC_ARM_REG_LR,0x200001)
        u.emu_start(0x81006E11,0x200000,count=100000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
        self.assertEqual(quads,expected if expected is not None else [(1153,100),(1154,109)])
        return u

    def test_original_drawer_consumes_hooked_vwf_english(self):
        self.draw(self.key,1)

    def test_original_utf8_converter_then_hook_handles_ascii_font_mapping(self):
        self.assertNotEqual(self.converted,self.mixed.encode('cp932'))
        u=self.draw(self.mixed.encode('utf-8'),0)
        self.assertEqual(bytes(u.mem_read(0x8138AAD0,len(self.converted)+1)),self.converted+b'\0')


if __name__=='__main__':unittest.main()
