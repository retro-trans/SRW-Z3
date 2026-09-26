"""Execute actual PS3 name geometry and registration loop, old and patched."""
import struct
import unittest
from pathlib import Path
import eboot
import link_identity_geometry as I

SOURCE=Path('work/ps3_link_background_v2_20260917/installed-backup-01/EBOOT-original.BIN')


class CPU:
    def __init__(self,blob):
        self.regions=[(s['va'],blob[s['off']:s['off']+s['filesz']]) for s in eboot._segments(blob) if s['filesz']]
        self.mem={};self.r=[0]*32;self.f=[0.]*32;self.cr=[0]*8;self.lr=0;self.calls={};self.writes=set()
        self.r[1]=0x2000000;self.r[2]=0x7dd920
        self.put(self.r[1],bytes(0x200))
    def read(self,p,n):
        def byte(p):
            if p in self.mem:return self.mem[p]
            for base,raw in self.regions:
                if base<=p<base+len(raw):return raw[p-base]
            raise AssertionError('unmapped read '+hex(p))
        return bytes(byte(p+i) for i in range(n))
    def put(self,p,raw):self.mem.update(enumerate(raw,p))
    def u32(self,p):return int.from_bytes(self.read(p,4),'big')
    def string(self,p):
        raw=bytearray()
        while self.read(p,1)!=b'\0':raw+=self.read(p,1);p+=1
        return bytes(raw)
    def run(self,pc,ends):
        r,f=self.r,self.f
        def signed(x,bits):
            x&=(1<<bits)-1
            return x-(1<<bits) if x>>(bits-1) else x
        for step in range(400000):
            if pc in ends:return pc
            if pc in self.calls:
                result=self.calls[pc](self)
                # Native callees may clobber volatile state; helpers must not
                # accidentally rely on fixture callees preserving it.
                for j in [0]+list(range(3,13)):r[j]=0xBAD00000+j
                f[:14]=[12345.]*14;self.cr=[99]*8;r[3]=result;pc=self.lr;continue
            w=self.u32(pc);op,t,a,b=w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
            imm=signed(w,16);nextpc=pc+4
            if op==18:
                nextpc=pc+signed(w&0x3fffffc,26)
                if w&1:self.lr=pc+4
            elif op==16:
                bo,bi=(w>>21)&31,(w>>16)&31;cmp=self.cr[bi//4]
                assert bo in (4,12) and bi%4<3
                if (cmp<0,cmp>0,cmp==0)[bi%4]==(bo==12):nextpc=pc+signed(w&0xfffc,16)
            elif w==0x4e800020:nextpc=self.lr
            elif op==14:r[t]=(r[a] if a else 0)+imm
            elif op==15:r[t]=(r[a] if a else 0)+(imm<<16)
            elif op==24:r[a]=r[t]|(w&65535)
            elif op==29:
                r[a]=r[t]&((w&65535)<<16)
                self.cr[0]=signed(r[a],32)
            elif op==7:r[t]=r[a]*imm
            elif op in (10,11):
                self.cr[(w>>23)&7]=((r[a]&0xffffffff)-(w&65535) if op==10 else signed(r[a],32)-imm)
            elif op==21:
                sh,mb,me=(w>>11)&31,(w>>6)&31,(w>>1)&31
                assert mb<=me
                rot=((r[t]<<sh)|(r[t]>>(32-sh if sh else 32)))&0xffffffff
                r[a]=rot&sum(1<<(31-i) for i in range(mb,me+1))
            elif op==30:
                # All emitted/native clrldi forms in these routines.
                mb=((w>>6)&31)|((w&32))
                assert (w&0x1c)==0
                r[a]=r[t]&((1<<(64-mb))-1)
            elif op in (32,34,35,40,58):
                n={32:4,34:1,35:1,40:2,58:8}[op]
                address=(r[a] if a else 0)+imm
                r[t]=int.from_bytes(self.read(address,n),'big')
                if op==35:r[a]=address
            elif op==31:
                xo=(w>>1)&1023
                if xo in (0,32):self.cr[(w>>23)&7]=(signed(r[a],32)-signed(r[b],32) if xo==0 else (r[a]&0xffffffff)-(r[b]&0xffffffff))
                elif xo==444:r[a]=r[t]|r[b]
                elif xo==266:r[t]=r[a]+r[b]
                elif xo==40:r[t]=r[b]-r[a]
                elif xo==235:r[t]=signed(r[a],32)*signed(r[b],32)
                elif xo==87:r[t]=self.read((r[a] if a else 0)+r[b],1)[0]
                elif xo==986:r[a]=signed(r[t],32)
                elif w==0x7c0802a6:r[0]=self.lr
                elif w==0x7c0803a6:self.lr=r[0]
                else:raise AssertionError((hex(pc),hex(w)))
            elif op in (48,50):
                raw=self.read(r[a]+imm,4 if op==48 else 8)
                f[t]=struct.unpack('>f',raw)[0] if op==48 else raw
            elif op==63:
                xo=(w>>1)&1023
                if xo==846:f[t]=float(int.from_bytes(f[b],'big',signed=True))
                elif xo==12:f[t]=struct.unpack('>f',struct.pack('>f',f[b]))[0]
                else:raise AssertionError((hex(pc),hex(w)))
            elif op==59:
                xo=(w>>1)&31
                if xo==21:f[t]=f[a]+f[b]
                elif xo==25:f[t]=f[a]*f[(w>>6)&31]
                else:raise AssertionError((hex(pc),hex(w)))
                f[t]=struct.unpack('>f',struct.pack('>f',f[t]))[0]
            elif op in (36,38,39,52,62):
                n=8 if op==62 else (1 if op in (38,39) else 4)
                address=(r[a] if a else 0)+(signed(w&0xfffc,16) if op==62 else imm)
                raw=struct.pack('>f',f[t]) if op==52 else (r[t]&((1<<(8*n))-1)).to_bytes(n,'big')
                self.put(address,raw);self.writes.update(range(address,address+n))
                if op==39 or (op==62 and w&3==1):r[a]=address
            else:raise AssertionError((hex(pc),hex(w)))
            pc=nextpc
        raise AssertionError('unbounded execution')


class IdentityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.old=SOURCE.read_bytes();cls.new=bytearray(cls.old)
        import link_background_layout as L
        L.apply(cls.new,eboot._segments(cls.new),dialogue_scene=True)
        cls.entries={};c=CPU(cls.old);at=eboot.NAME_TBL
        while c.u32(at):
            jp,en=c.u32(at),c.u32(at+4)
            if en<0x40000000:cls.entries[c.string(jp)]=(jp,en,c.string(en))
            at+=8
    def measure(self,jp,quad,pitch,patched=True,custom=None):
        c=CPU(self.new if patched else self.old);widget=0x2100000;rect=0x2101000;pointer=0x2102000
        raw=jp.encode('cp932') if custom is None else custom
        c.put(pointer,raw+b'\0');c.put(widget,bytes(0x68));c.put(rect,bytes(24))
        c.put(widget+4,struct.pack('>ffIIII',215.,416.,quad,quad,pitch,29))
        c.r[3]=pointer;c.r[31]=widget;c.r[29]=rect
        c.calls[0x554dac]=lambda x:len(x.string(x.r[3]))
        before=c.read(widget,0x68);c.run(0x2562d4,{0x256238})
        self.assertEqual(c.read(widget,0x68),before)
        self.assertEqual(struct.unpack('>ff',c.read(rect+12,8)),(445.,1.))
        self.assertEqual(c.r[11],1)
        self.assertTrue(c.writes<=set(range(rect,rect+24))|set(range(c.r[1]+0x70,c.r[1]+0x78)))
        return struct.unpack('>f',c.read(rect+8,4))[0]-215
    def test_real_name_widget_uses_translated_width_at_multiple_fonts(self):
        import digraph as dg
        import json
        mapping=json.loads(Path('work/build_0.6.12_approved_subtitle/pairs.json').read_text())
        c=CPU(self.old)
        fixtures=[(jp.encode('cp932'),self.entries[jp.encode('cp932')][2])
                  for jp in ('桂木桂','キラ','アルト','ヒビキ')]
        fixtures += [(dg.encode_mixed(en,mapping),dg.encode_mixed(en,mapping)) for en in ('Kei','Kira','Alto','Hibiki','Wiii')]
        for raw,encoded in fixtures:
            for quad,pitch in ((24,31),(21,27),(32,42)):
                expected=sum(c.read(eboot.TABLE_VA+dg.cell_index(int.from_bytes(encoded[i:i+2],'big')),1)[0] for i in range(0,len(encoded),2))*quad/32
                self.assertEqual(self.measure('',quad,pitch,custom=raw),expected)
                self.assertEqual(self.measure('',quad,pitch,False,custom=raw),len(raw)//2*pitch)
    def test_unknown_names_keep_native_pitch(self):
        for raw in ('日本'.encode('cp932'),b'Custom',b'',b'\xff\xff'):
            self.assertEqual(self.measure('',24,31,custom=raw),(len(raw)//2)*31)
    def test_native_registration_assigns_second_translated_glossary_identity(self):
        candidates=[(k,v) for k,v in self.entries.items() if k in ('破界事変'.encode('cp932'),'再世戦争'.encode('cp932'))]
        self.assertEqual(len(candidates),2)
        for selected in range(2):
            for patched in (False,True):
                c=CPU(self.new if patched else self.old)
                manager,refs,record=0x2200000,0x2200100,0x2200200
                c.put(manager,struct.pack('>II',refs,2));c.put(refs,struct.pack('>II',10,11));c.put(record,bytes(20))
                desc={}
                for index,(jp,(ptr,_,en)) in enumerate(candidates):
                    desc[10+index]=0x2200300+index*4;c.put(desc[10+index],struct.pack('>I',ptr))
                c.r[29]=manager;c.r[31]=refs;c.r[28]=record
                c.r[27]=candidates[selected][1][1]
                c.calls[0x1ce048]=lambda x:desc[x.r[3]]
                c.calls[0x55a30c]=lambda x:0 if x.string(x.r[3])==x.string(x.r[4]) else 1
                c.run(0x1ce1f4,{0x1ce244,0x1ce2b8})
                self.assertEqual(c.u32(record+16),selected if patched else 0)
                self.assertEqual(c.read(record,16),bytes(16))
                # Use the ID actually produced by native registration in the
                # primary geometry helper. Legacy ID 0 hides selected term 1.
                from test_main_link_background_layout import PrimaryGeometry,execute
                import main_link_background_layout as M
                r,mem,calls,records,render_record,_=PrimaryGeometry().fixture(selected=selected,width=173.25,x=182,y=120)
                mem.update(enumerate(c.read(record+16,4),records+17*20+16))
                execute(M.stub(),M.CAVE,r,mem,calls)
                actual=struct.unpack('>ffff',bytes(mem[r[30]+j] for j in range(16)))
                self.assertEqual(actual,(182.,121.,173.25,32.) if patched or selected==0 else (0.,0.,0.,0.))
    def test_birthday_hooks_keep_numeric_calls_and_render_slash(self):
        c=CPU(self.new);p=I.BIRTHDAY+12
        self.assertEqual(c.string(p),'／'.encode('cp932'))
        for site in (0xf7904,0xf795c):
            off=eboot._off(eboot._segments(self.old),site)
            self.assertEqual(self.old[off:off+4],self.new[off:off+4])
        r=c.r[:];c.lr=123;c.run(I.BIRTHDAY,{0x14a7c})
        self.assertEqual(c.r[3],p);self.assertEqual(c.lr,123)
        self.assertEqual(c.r[:3]+c.r[4:],r[:3]+r[4:])
        self.assertEqual(c.u32(0xf797c),0x60000000)

    def test_dialogue_context_is_filled_before_native_identity_registration(self):
        import dialogue_link_scene as S
        # Start BEFORE the native scene getter, not after hand-filling its
        # output. A null context is normal in dialogue; backlog supplies one.
        for explicit,current in ((0,0x2300000),(0x2301000,0x2300000),(0,0)):
            for legacy in (False,True):
                c=CPU(self.new); context=0x2310000; manager=0x2310100
                c.put(context,struct.pack('>II',0,explicit))
                c.put(manager,bytes(12)+struct.pack('>I',current))
                c.put(0x2320000,bytes(20));c.r[28]=0x2320000;c.r[30]=0
                c.r[3]=context
                if legacy:c.put(S.SITE,struct.pack('>I',I.branch(S.SITE,0x1c4938,True)))
                calls=[]
                c.calls[0x1c93c8]=lambda cpu:(calls.append(True) or manager)
                saved=c.r[1];nonvolatile=c.r[14:]
                c.run(S.SITE,{0x1ce1c8})
                want=explicit if legacy or explicit else current
                self.assertEqual(c.u32(0x232000c),want)
                self.assertEqual(c.u32(0x2320010),0)
                self.assertEqual(c.r[1],saved);self.assertEqual(c.r[14:],nonvolatile)
                self.assertEqual(len(calls),int(not legacy and not explicit))

    def test_null_dialogue_scene_through_registration_and_primary_geometry(self):
        import dialogue_link_scene as S
        from test_main_link_background_layout import PrimaryGeometry,execute
        import main_link_background_layout as M
        keys=['破界事変'.encode('cp932'),'再世戦争'.encode('cp932')]
        for legacy in (True,False):
            c=CPU(self.new);scene=0x2300000;context=0x2300100
            manager=0x2300200;refs=0x2300300;record=0x2300400
            c.put(context,bytes(8));c.put(manager,bytes(12)+struct.pack('>I',scene))
            c.put(scene,bytes(24)+struct.pack('>I',0x2300500))
            c.put(0x2300500,struct.pack('>II',refs,2));c.put(refs,struct.pack('>II',10,11))
            c.put(record,bytes(20))
            for j,key in enumerate(keys):c.put(0x2300600+j*4,struct.pack('>I',self.entries[key][0]))
            c.r[3]=context;c.r[28]=record;c.r[30]=0;c.r[27]=self.entries[keys[1]][1]
            c.calls[0x1c93c8]=lambda cpu:manager
            c.calls[0x1ce048]=lambda cpu:0x2300600+(cpu.r[3]-10)*4
            c.calls[0x55a30c]=lambda cpu:int(cpu.string(cpu.r[3])!=cpu.string(cpu.r[4]))
            if legacy:c.put(S.SITE,struct.pack('>I',I.branch(S.SITE,0x1c4938,True)))
            c.run(S.SITE,{0x1ce244,0x1ce2b8})
            self.assertEqual((c.u32(record+12),c.u32(record+16)),(0,0) if legacy else (scene,1))
            r,mem,calls,records,_,_=PrimaryGeometry().fixture(selected=1,width=173.25,x=182,y=120)
            # Pass both registration fields through untouched and point the
            # primary scene manager at the scene used by registration.
            primary_manager=calls[0x1c93c8](r,mem)
            mem.update(enumerate(struct.pack('>I',scene),primary_manager+12))
            mem.update(enumerate(c.read(record+12,8),records+17*20+12))
            execute(M.stub(),M.CAVE,r,mem,calls)
            rect=struct.unpack('>4f',bytes(mem[r[30]+j] for j in range(16)))
            self.assertEqual(rect,(0.,0.,0.,0.) if legacy else (182.,121.,173.25,32.))


if __name__=='__main__':unittest.main()
