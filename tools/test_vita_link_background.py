"""Real Thumb glyph advances -> link registration -> native highlight rectangle."""
import gc
import struct
import sys
from pathlib import Path
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import link_background as L
import date_card_centering as D
import vwf
from category_port import Port, encoded
from inspect_vwf import segment
from self_decrypt import parse
from test_vita_date_centering import BASE, draw_positions
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE
from unicorn.arm_const import *


def bits(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]


class LinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not BASE.exists():
            raise unittest.SkipTest('Private test16 package required')
        cls.before = zipfile.ZipFile(BASE).read('rePatch/PCSG00264/eboot.bin')
        cls.dated, _ = D.apply(cls.before, 0x812b5e38)
        cls.after, cls.audit = L.apply(cls.dated)
        cls.port = Port()

    def machine(self, code_shift=0, data_shift=0):
        gc.collect()
        u = Uc(UC_ARCH_ARM, UC_MODE_THUMB)
        info = parse(self.after)
        for n in (0, 1):
            data, base = segment(self.after, info, n)
            if n == 0:
                data = bytearray(data)
                for address in (vwf.DELTA, L.ui_text.POINTER, L.ui_text.NAMES_POINTER):
                    value = struct.unpack_from('<I', data, address-base)[0]
                    struct.pack_into('<I', data, address-base, (value+data_shift-code_shift)&0xffffffff)
                data = bytes(data)
            base += code_shift if n == 0 else data_shift
            u.mem_map(base, (len(data)+4095)//4096*4096); u.mem_write(base, data)
        u.mem_map(0x200000, 0x10000)
        u.reg_write(UC_ARM_REG_CPSR, 0x30); u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.reg_write(UC_ARM_REG_C1_C0_2, 0xf << 20); u.reg_write(UC_ARM_REG_FPEXC, 1 << 30)
        noops = {0x8100985e, 0x810095d0, 0x8100986a, 0x81009da8, 0x81009776, 0x81008f64, 0x8100973c}

        def external(cpu, address, size, user):
            address -= code_shift
            if address == 0x8121dc30:
                data = bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0), 512))
                cpu.reg_write(UC_ARM_REG_R0, data.index(0))
            elif address == 0x810ce51e:
                cpu.reg_write(UC_ARM_REG_R0, 0x204000)
            elif address == 0x8100970a:
                cpu.reg_write(UC_ARM_REG_R0, 0x202000)
            elif address not in noops:
                return
            cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        u.hook_add(UC_HOOK_CODE, external)
        text, base = segment(self.after, info)
        delta = struct.unpack_from('<I', text, vwf.DELTA-base)[0]
        self.pen = ((vwf.DELTA+delta) & 0xffffffff)+data_shift
        self.cache = int(self.audit['cache_address'], 16)+data_shift
        self.code_shift = code_shift
        return u

    def capture(self, u, index, payload=b'link', height=28):
        u.mem_write(0x201000, payload+b'\0')
        u.mem_write(0x208000, struct.pack('<II', index//16, index%16))
        u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.reg_write(UC_ARM_REG_R0, 0x201000)
        u.reg_write(UC_ARM_REG_R4, 0x203000)
        u.reg_write(UC_ARM_REG_R7, 0x204000)
        u.mem_write(0x20402d,bytes((height,)))
        u.mem_write(0x203000, bytes(range(20)))
        u.emu_start((L.CAPTURE+self.code_shift) | 1, L.CAPTURE+self.code_shift+6, count=2000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC), L.CAPTURE+self.code_shift+6)
        self.assertEqual(u.reg_read(UC_ARM_REG_SP), 0x208000)
        self.assertEqual(bytes(u.mem_read(0x203000, 20)), bytes(range(4))+bytes([len(payload)])+bytes(range(5,20)))
        self.assertEqual(u.reg_read(UC_ARM_REG_R0), len(payload))

    def select(self, u, index, valid=True):
        u.mem_write(0x203000, struct.pack('<hhBBBBIII', 100, 200, 20, 1, 31, 28, 10, 20, 30))
        u.mem_write(0x204000, bytes(0x40))
        u.mem_write(0x20402d, bytes((28,31)))
        u.mem_write(0x205000, b'Q'*0x740)
        u.reg_write(UC_ARM_REG_R0, 0x203000 if valid else 0)
        u.reg_write(UC_ARM_REG_R5, 0x205000)
        u.reg_write(UC_ARM_REG_R8, index & 0xffffffff)
        u.reg_write(UC_ARM_REG_SP, 0x208000)
        u.emu_start((L.SELECT+self.code_shift) | 1, 0x810d6a76+self.code_shift, count=2000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC), 0x810d6a76+self.code_shift)
        self.assertEqual(u.reg_read(UC_ARM_REG_SP), 0x208000)
        if not valid:
            self.assertEqual(bytes(u.mem_read(0x205000, 0x740)), b'Q'*0x740)
            return
        x,y,width,height = struct.unpack('<4f', u.mem_read(0x205714, 16))
        self.assertEqual((x,y,height), (100,200,29))
        self.assertEqual(bytes(u.mem_read(0x203000, 20)), struct.pack('<hhBBBBIII',100,200,20,1,31,28,10,20,30))
        return width

    def test_all_256_slots_reuse_and_later_text_does_not_change_saved_width(self):
        u = self.machine()
        for index in range(256):
            u.mem_write(self.pen, struct.pack('<f', index+.375))
            self.capture(u, index, height=20+index%16)
            self.assertEqual(bytes(u.mem_read(self.cache+1024+index,1)),bytes((20+index%16,)))
        u.mem_write(self.pen, struct.pack('<f', 9999))
        for index in range(256):
            self.assertEqual(self.select(u, index), index+.375)
        u.mem_write(self.pen, struct.pack('<f', 19.5))
        self.capture(u, 0)
        self.assertEqual(self.select(u, 0), 19.5)
        for index in (-1, 256, 5000):
            self.select(u, index, valid=False)

    def test_actual_glyph_widths_for_names_terms_and_japanese(self):
        u = self.machine()
        for label in ('Kei','Destruction Incident','Regeneration War','Alto','ZEXIS','Kouji','Hibiki','Wiii','日本'):
            for font, pitch in ((24,31),(28,28),(32,42)):
                payload = encoded(label, self.port.mapping)
                state = 0x8138aa58
                u.mem_write(state, bytes(0x78))
                for off, value in ((0x14,font),(0x18,font),(0x1c,pitch),(0x20,32)):
                    u.mem_write(state+off,struct.pack('<f',value))
                u.mem_write(self.pen, bytes(4)); u.mem_write(0x201000,payload+b'\0')
                u.reg_write(UC_ARM_REG_R0,0x201000); u.reg_write(UC_ARM_REG_R1,1)
                u.reg_write(UC_ARM_REG_S0,bits(100));u.reg_write(UC_ARM_REG_S1,bits(200));u.reg_write(UC_ARM_REG_S2,bits(0))
                u.reg_write(UC_ARM_REG_LR,0x200001);u.reg_write(UC_ARM_REG_SP,0x208000)
                u.emu_start(0x81006e11,0x200000,count=30000)
                self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
                expected = sum(self.port.widths[c]*font/32 if c in self.port.widths else pitch for c in label)
                actual = struct.unpack('<f',u.mem_read(self.pen,4))[0]
                self.assertAlmostEqual(actual,expected)
                self.capture(u,17,payload)
                u.mem_write(self.pen,struct.pack('<f',999))
                self.assertAlmostEqual(self.select(u,17),expected)
                if label in ('Alto','ZEXIS'):
                    self.assertLess(expected,len(label)*pitch)

    def test_independent_code_data_relocation(self):
        for code_shift,data_shift in ((0x1000000,0x5000000),(0x5000000,0),(0,0x1000000)):
            u=self.machine(code_shift,data_shift)
            for index in (0,15,16,255):
                u.mem_write(self.pen,struct.pack('<f',index+12.75))
                self.capture(u,index)
                self.assertEqual(self.select(u,index),index+12.75)

    def test_preserves_date_fix_and_record_identity_code(self):
        keys = ['新多元世紀０００１年　４月２７日'.encode('cp932')]
        self.assertEqual(draw_positions(self.after,keys,1),draw_positions(self.dated,keys,1))
        old_info,new_info=parse(self.dated),parse(self.after)
        old,base=segment(self.dated,old_info);new,_=segment(self.after,new_info)
        allowed=set(range(L.CAVE-base,L.CAVE-base+self.audit['code_bytes']))
        allowed.update(range(L.main_links.START-base,L.main_links.END-base))
        from platforms.vita import link_identity_geometry as G
        allowed.update(range(G.SECONDARY-base,G.SECONDARY_END-base))
        allowed.update(range(G.NAME-base,G.NAME_END-base))
        allowed.update(range(G.COMPARE-base,G.COMPARE-base+4))
        allowed.update(range(0x8110b41a-base,0x8110b41e-base))
        allowed.update(range(0x810d8d86-base,0x810d8d8a-base))
        for address in (L.CAPTURE,L.SELECT,L.STORE):allowed.update(range(address-base,address-base+4))
        self.assertTrue({i for i,(a,b) in enumerate(zip(old,new)) if a!=b} <= allowed)
        a,_=segment(self.dated,old_info,1);b,_=segment(self.after,new_info,1)
        self.assertTrue(b.startswith(a));self.assertFalse(any(b[len(a):]))
        for n in (2,3,4):self.assertEqual(segment(self.dated,old_info,n),segment(self.after,new_info,n))
        with self.assertRaises(ValueError):L.apply(self.after)

    def primary(self, u, slot=17, keyword=3, match=True, context_type=0, active=0,
                stale_scene=False, legacy=False, registered_record=None):
        # Execute native main geometry, including native link-manager lookup.
        # The flat render index deliberately differs from the glossary index.
        obj,ctx,manager,banks,scene=0x205000,0x204800,0x206000,0x207000,0x206800
        u.mem_write(obj,bytes(0x740));u.mem_write(obj+4,struct.pack('<I',0x206900))
        u.mem_write(0x206903,bytes((keyword,)))
        u.mem_write(ctx,bytes(16));u.mem_write(ctx+4,struct.pack('<I',0x206a00))
        u.mem_write(0x206a00,struct.pack('<I',context_type))
        u.mem_write(0x8132bfb4,struct.pack('<I',manager))
        u.mem_write(manager,bytes(0x50));u.mem_write(manager+12,struct.pack('<I',scene))
        u.mem_write(0x8132c00c,struct.pack('<I',banks));u.mem_write(banks,bytes(0x48))
        u.mem_write(0x209000,bytes(16*20))
        u.mem_write(banks+4+(slot//16)*4,struct.pack('<I',0x209000))
        record=struct.pack('<hhBBBBIII',182,120,6,1,31,32,2,scene+4 if stale_scene else scene,
                           keyword if match else keyword+1)
        if registered_record is not None:record=registered_record
        u.mem_write(0x209000+(slot%16)*20,record)
        u.mem_write(0x204000,bytes(0x40));u.mem_write(0x20402d,bytes((28,31,32)))
        u.mem_write(0x204020,struct.pack('<hh',182,120))
        styles=[]
        def external(cpu,address,size,user):
            if address==0x8121db90:
                cpu.mem_write(cpu.reg_read(UC_ARM_REG_R0),bytes(cpu.reg_read(UC_ARM_REG_R2)))
            elif legacy and address==0x810d6f80:
                cpu.mem_write(cpu.reg_read(UC_ARM_REG_R3),bytes((0,0,3)))
                cpu.reg_write(UC_ARM_REG_R0,1)
            elif address==0x81109dd8:cpu.reg_write(UC_ARM_REG_R0,active)
            elif address in (0x810ce4e2,0x810ce514,0x810ce4d8,0x810ce50a):
                styles.append(address);cpu.reg_write(UC_ARM_REG_R0,0x204000)
            else:return
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        hook=u.hook_add(UC_HOOK_CODE,external)
        regs={UC_ARM_REG_R4:80,UC_ARM_REG_R5:obj+0x714,UC_ARM_REG_R6:obj,
              UC_ARM_REG_R7:ctx,UC_ARM_REG_R8:0x123456,UC_ARM_REG_LR:0x200001}
        for r,v in regs.items():u.reg_write(r,v)
        u.reg_write(UC_ARM_REG_SP,0x208000)
        u.emu_start(L.main_links.START|1,L.main_links.END,count=100000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC),L.main_links.END)
        self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
        for r,v in regs.items():
            if not legacy or r not in (UC_ARM_REG_R8,UC_ARM_REG_LR):
                self.assertEqual(u.reg_read(r),v)
        self.assertEqual(bytes(u.mem_read(0x209000+(slot%16)*20,20)),record)
        u.hook_del(hook)
        return struct.unpack('<4f',u.mem_read(obj+0x714,16)),styles

    def test_primary_uses_render_slot_identity_and_actual_x_not_character_column(self):
        u=self.machine()
        for slot in (0,15,16,17,255):
            u.mem_write(self.cache+slot*4,struct.pack('<f',38.25))
            u.mem_write(self.cache+1024+slot,b'\x1c')
            rectangle,styles=self.primary(u,slot)
            self.assertEqual(rectangle,(182,121,38.25,29))
            self.assertEqual(styles,[])
        rectangle,styles=self.primary(u,17,match=False)
        self.assertEqual(rectangle,(0,0,0,0));self.assertEqual(styles,[])
        rectangle,styles=self.primary(u,17,stale_scene=True)
        self.assertEqual(rectangle,(0,0,0,0));self.assertEqual(styles,[])
        for context in (0,5,10,7):
            for active in (0,1):
                rectangle,styles=self.primary(u,17,context_type=context,active=active)
                self.assertEqual(rectangle[3],29)  # height of actual rendered style
                self.assertEqual(styles,[])

    def test_reproduces_first_packages_fixed_width_kei_background(self):
        u=self.machine()
        original,base=segment(self.dated,parse(self.dated))
        start,end=L.main_links.START,L.main_links.END
        u.mem_write(start,original[start-base:end-base])
        u.mem_write(self.cache+17*4,struct.pack('<f',38.25))
        rectangle,_=self.primary(u,17,legacy=True)
        self.assertEqual(rectangle,(182,121,93,29))
        self.assertGreater(rectangle[2],38.25*2)

    def test_real_styled_keyword_draw_keeps_measured_width_for_kei(self):
        u=self.machine();style=0x203800
        u.mem_write(style,bytes(0x40));u.mem_write(style,struct.pack('<I',1))
        u.mem_write(style+0x2c,bytes((24,28,31,32,0,0,0,0)))
        u.mem_write(0x8138aa58,bytes(0x78));u.mem_write(0x8150c138,struct.pack('<I',1))
        payload=encoded('Kei',self.port.mapping)
        u.mem_write(0x201000,payload+b'\0');u.mem_write(self.pen,bytes(4))
        u.mem_write(0x208000,struct.pack('<I',style))
        for r,v in ((UC_ARM_REG_R0,0x201000),(UC_ARM_REG_R1,0),(UC_ARM_REG_R2,182),
                    (UC_ARM_REG_R3,120),(UC_ARM_REG_LR,0x200001)):
            u.reg_write(r,v)
        u.emu_start(0x810d9f93,0x200000,count=50000)
        self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
        expected=sum(self.port.widths[c]*24/32 for c in 'Kei')
        self.assertEqual(struct.unpack('<f',u.mem_read(self.pen,4))[0],expected)
        self.capture(u,17,payload)
        rectangle,_=self.primary(u,17)
        self.assertEqual(rectangle,(182,121,expected,29))

    def test_real_name_widget_geometry_not_keyword_fixture(self):
        u=self.machine()
        new,base=segment(self.after,parse(self.after))
        old,_=segment(self.dated,parse(self.dated))
        for label in ('Kei','Kira','Alto','Hibiki','Wiii','日本'):
            for font,pitch in ((24,31),(21,27),(32,42)):
                payload=encoded(label,self.port.mapping)
                for legacy in (True,False):
                    block=old if legacy else new
                    u.mem_write(0x8110b3e8,block[0x8110b3e8-base:0x8110b43a-base])
                    u.ctl_remove_cache(0x8110b3e8,0x8110b43a)
                    u.mem_write(0x201000,payload+b'\0')
                    u.mem_write(0x203000,bytes(0x68))
                    u.mem_write(0x203004,struct.pack('<ffIIII',182.,120.,font,28,pitch,29))
                    u.mem_write(0x204000,struct.pack('<I',0x204100))
                    u.mem_write(0x204100,bytes(20))
                    u.reg_write(UC_ARM_REG_SP,0x208000)
                    initial={UC_ARM_REG_R0:0x201000,UC_ARM_REG_R4:0x204000,
                             UC_ARM_REG_R5:0x203000,UC_ARM_REG_R6:0x1234,UC_ARM_REG_R7:0x4567}
                    for r,value in initial.items():u.reg_write(r,value)
                    u.emu_start(0x8110b3e9,0x8110b43a,count=100000)
                    self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x8110b43a)
                    self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
                    for r in (UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7):
                        self.assertEqual(u.reg_read(r),initial[r])
                    x,y,right,bottom,flag=struct.unpack('<5f',u.mem_read(0x204100,20))
                    width=len(payload)//2*pitch if legacy or label=='日本' else sum(self.port.widths[c]*font/32 for c in label)
                    self.assertEqual((x,y,right,bottom,flag),(182.,120.,182.+width,149.,1.))
                    if label=='Kei' and font==24 and pitch==31:
                        self.assertEqual(width,93 if legacy else 38.25)

    def test_name_measurement_helper_with_independent_relocation(self):
        for cs,ds in ((0x1000000,0x5000000),(0x5000000,0)):
            u=self.machine(cs,ds)
            u.mem_write(0x201000,encoded('Kei',self.port.mapping)+b'\0')
            u.mem_write(0x203000,bytes(0x68))
            u.mem_write(0x20300c,struct.pack('<III',24,28,31))
            u.reg_write(UC_ARM_REG_R0,0x201000);u.reg_write(UC_ARM_REG_R5,0x203000)
            u.reg_write(UC_ARM_REG_LR,0x200001)
            start=int(self.audit['name_and_identity']['name_helper'],16)+cs
            u.emu_start(start|1,0x200000,count=100000)
            self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
            self.assertEqual(u.reg_read(UC_ARM_REG_R0),bits(38.25))

    def test_native_registration_matches_translated_second_glossary_entry(self):
        # V2's fixture hand-filled a correct ID; actual registration compared
        # English rendered labels to Japanese and silently left ID zero.
        u=self.machine()
        data,db=segment(self.after,parse(self.after),1)
        text,tb=segment(self.after,parse(self.after))
        table=(L.ui_text.POINTER+struct.unpack_from('<I',text,L.ui_text.POINTER-tb)[0])&0xffffffff
        offset=table-db
        targets=[encoded(s,self.port.mapping) for s in ('Destruction Incident','Regeneration War')]
        keys={}
        for j in range(struct.unpack_from('<I',data,offset)[0]):
            _,key,value=struct.unpack_from('<III',data,offset+4+12*j)
            en=data[offset+value:].split(b'\0',1)[0]
            if en in targets:keys[en]=data[offset+key:].split(b'\0',1)[0]
        self.assertEqual(len(keys),2)
        def put(p,*words):u.mem_write(p,struct.pack('<'+'I'*len(words),*words))
        def cstr(p):return bytes(u.mem_read(p,512)).split(b'\0',1)[0]
        comparisons=[]
        def external(cpu,address,size,user):
            if address==0x810d50fa:cpu.reg_write(UC_ARM_REG_R0,0x206700)
            elif address in (0x810ee1de,0x810ee2a2):cpu.reg_write(UC_ARM_REG_R0,0x206f00)
            elif address==0x810ed928:cpu.reg_write(UC_ARM_REG_R0,0x206a00+cpu.reg_read(UC_ARM_REG_R1)*4)
            elif address==0x8121da20:
                a,b=cstr(cpu.reg_read(UC_ARM_REG_R0)),cstr(cpu.reg_read(UC_ARM_REG_R1))
                comparisons.append((a,b));cpu.reg_write(UC_ARM_REG_R0,0 if a==b else 1)
            else:return
            cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
        hook=u.hook_add(UC_HOOK_CODE,external)
        site=0x810d8dc6
        for version in (2,3,4):
            legacy=version==2
            u.mem_write(site,vwf.assemble('blx 0x8121da20',site) if legacy else text[site-tb:site-tb+4])
            u.ctl_remove_cache(site,site+4)
            scene_site=0x810d8d86
            u.mem_write(scene_site,vwf.assemble('bl 0x810d5158',scene_site) if version<4 else text[scene_site-tb:scene_site-tb+4])
            u.ctl_remove_cache(scene_site,scene_site+4)
            u.mem_write(0x206000,bytes(0x50));put(0x206004,0x209000)
            # Normal dialogue has no explicit backlog scene. Execute the
            # real context getter and fallback, rather than faking its result.
            put(0x206704,0)
            put(0x8132bfb4,0x206600);put(0x20660c,0x206800)
            u.mem_write(0x209000,bytes(16*20))
            put(0x206818,0x206900);put(0x206900,0x206980,2);put(0x206980,0,1)
            put(0x206a00,0x20a000,0x20a200)
            for at,en in zip((0x20a000,0x20a200),targets):u.mem_write(at,keys[en]+b'\0')
            u.mem_write(0x201000,targets[1]+b'\0')
            u.mem_write(0x204000,bytes(0x40));u.mem_write(0x20402d,bytes((28,31,32)))
            u.mem_write(self.pen,struct.pack('<f',173.25))
            put(0x208000,120)
            for r,value in ((UC_ARM_REG_R0,0x206000),(UC_ARM_REG_R1,0x201000),
                            (UC_ARM_REG_R2,0x204000),(UC_ARM_REG_R3,182),
                            (UC_ARM_REG_SP,0x208000),(UC_ARM_REG_LR,0x200001)):
                u.reg_write(r,value)
            u.emu_start(0x810d8cd9,0x200000,count=200000)
            self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
            record=struct.unpack('<hhBBBBIII',u.mem_read(0x209000,20))
            self.assertEqual(record[-2:],(0,0) if version<4 else (0x206800,1))
            self.assertEqual(struct.unpack('<f',u.mem_read(self.cache,4))[0],173.25)
            self.assertEqual(bytes(u.mem_read(self.cache+1024,1)),b'\x1c')
            registered=bytes(u.mem_read(0x209000,20))
            rectangle,_=self.primary(u,slot=0,keyword=1,registered_record=registered)
            self.assertEqual(rectangle,(0,0,0,0) if version<4 else (182,121,173.25,29))
        self.assertIn((targets[1],targets[1]),comparisons)
        u.hook_del(hook)

    def test_scene_fallback_preserves_backlog_and_relocates(self):
        from platforms.vita import dialogue_link_scene as S
        for cs,ds in ((0,0),(0x1000000,0x5000000)):
            for explicit,current in ((0,0x206800),(0x206a00,0x206800),(0,0)):
                u=self.machine(cs,ds)
                # Native getter global contains a relocated pointer in a real
                # loader. Supply that relocation, leaving the helper untouched.
                calls=[]
                def external(cpu,address,size,user):
                    if address!=0x810d6dc8+cs:return
                    calls.append(address)
                    self.assertEqual(cpu.reg_read(UC_ARM_REG_SP)%8,0)
                    cpu.reg_write(UC_ARM_REG_R0,0x206600)
                    cpu.reg_write(UC_ARM_REG_PC,cpu.reg_read(UC_ARM_REG_LR))
                u.hook_add(UC_HOOK_CODE,external)
                u.mem_write(0x206704,struct.pack('<I',explicit))
                u.mem_write(0x20660c,struct.pack('<I',current))
                u.reg_write(UC_ARM_REG_R0,0x206700)
                u.reg_write(UC_ARM_REG_R1,0x12345678)
                u.reg_write(UC_ARM_REG_LR,0x200001)
                u.emu_start((S.CAVE+cs)|1,0x200000,count=1000)
                self.assertEqual(u.reg_read(UC_ARM_REG_PC),0x200000)
                self.assertEqual(u.reg_read(UC_ARM_REG_R0),explicit or current)
                self.assertEqual(u.reg_read(UC_ARM_REG_R1),0x12345678)
                self.assertEqual(u.reg_read(UC_ARM_REG_SP),0x208000)
                self.assertEqual(len(calls),int(not explicit))


if __name__=='__main__':unittest.main()
