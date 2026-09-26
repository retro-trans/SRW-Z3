"""Execute PS3 primary PPC geometry and reproduce the old fixed-cell error."""
import struct
import unittest
from pathlib import Path
import eboot
import main_link_background_layout as M
import link_background_layout as L


def execute(code, base, r, mem, calls):
    f = [0.] * 32
    pc = base
    compare = 0
    writes = set()
    def signed(x, bits):
        x &= (1 << bits)-1
        return x-(1 << bits) if x >> (bits-1) else x
    def read(addr, n):
        return bytes(mem[addr+i] for i in range(n))
    for _ in range(20000):
        if pc == M.TAIL:
            return writes
        assert base <= pc < base+len(code), hex(pc)
        w = int.from_bytes(code[pc-base:pc-base+4], 'big')
        op,t,a,b = w>>26,(w>>21)&31,(w>>16)&31,(w>>11)&31
        imm = signed(w,16)
        following = pc+4
        if op == 18:
            target = pc+signed(w&0x3fffffc,26)
            if w&1:
                result = calls[target](r,mem)
                # A real callee may destroy every volatile general/FP register.
                for i in [0]+list(range(3,13)): r[i] = 0xBAD00000+i
                f[:14] = [98765.] * 14
                r[3] = result
                compare = 77
            else: following = target
        elif op == 16:
            bo,bi = (w>>21)&31,(w>>16)&31
            assert bi < 3 and bo in (4,12)
            flag = (compare<0,compare>0,compare==0)[bi]
            if flag == (bo==12): following = pc+signed(w&0xfffc,16)
        elif op == 14: r[t] = (r[a] if a else 0)+imm
        elif op == 15: r[t] = (r[a] if a else 0)+(imm<<16)
        elif op == 24: r[a] = r[t] | (w&65535)
        elif op == 7: r[t] = r[a]*imm
        elif op == 11: compare = signed(r[a],32)-imm
        elif op in (32,34,40):
            n = {32:4,34:1,40:2}[op]
            r[t] = int.from_bytes(read((r[a] if a else 0)+imm,n),'big')
        elif op == 31:
            xo = (w>>1)&1023
            if xo == 32: compare = (r[a]&0xffffffff)-(r[b]&0xffffffff)
            elif xo == 444: r[a] = r[t] | r[b]
            elif xo == 266: r[t] = r[a]+r[b]
            elif xo == 235: r[t] = signed(r[a],32)*signed(r[b],32)
            elif xo in (922,954,986): r[a] = signed(r[t],{922:16,954:8,986:32}[xo])
            else: raise AssertionError(hex(w))
        elif op in (48,50):
            raw = read(r[a]+imm,4 if op==48 else 8)
            f[t] = struct.unpack('>f',raw)[0] if op==48 else raw
        elif op == 63:
            xo = (w>>1)&1023
            if xo == 846: f[t] = float(int.from_bytes(f[b],'big',signed=True))
            elif xo == 12: f[t] = struct.unpack('>f',struct.pack('>f',f[b]))[0]
            else: raise AssertionError(hex(w))
        elif op in (36,52,62):
            n = 8 if op==62 else 4
            address = r[a]+imm
            raw = struct.pack('>f',f[t]) if op==52 else (r[t]&((1<<(8*n))-1)).to_bytes(n,'big')
            mem.update(enumerate(raw,address)); writes.update(range(address,address+n))
        else: raise AssertionError((hex(pc),hex(w)))
        pc = following
    raise AssertionError('unbounded loop')


class PrimaryGeometry(unittest.TestCase):
    def fixture(self, slot=17, scene=0x123456, selected=7, width=38.25, x=315, y=560):
        r = [0x3000000+i*0x1000 for i in range(32)]
        mem = {}
        put = lambda p,b: mem.update(enumerate(b,p))
        manager,records,style = 0x100000,0x110000,0x120000
        put(manager,bytes(0x50)); put(manager+12,struct.pack('>I',scene))
        put(style,bytes(0x40)); put(style+0x2d,b'\x1f')
        put(r[30],bytes(32)); put(L.WIDTHS,bytes(1024))
        put(L.WIDTHS+slot*4,struct.pack('>f',width))
        record = struct.pack('>hhBBBBIII',x,y,222,1,31,35,0xABCDEF,scene,selected)
        put(records+slot*20,record)
        def get(regs,memory):
            self.assertEqual(regs[3],manager)
            index = regs[4]
            self.assertTrue(0 <= index < 256)
            address = records+index*20
            return address if memory.get(address+5,0) else 0
        def get_style(regs,memory):
            self.assertEqual((regs[3],regs[4]),(r[31],r[27]))
            return style
        calls = {0x1c93c8:lambda r,m:manager,
                 0x2540e4:lambda r,m:selected, 0x1cdd74:lambda r,m:manager,
                 0x1cdbb0:get, 0x1c671c:get_style}
        return r,mem,calls,records,record,style

    def test_every_slot_identity_positions_width_and_register_liveness(self):
        for slot in range(256):
            r,m,c,records,record,_ = self.fixture(slot=slot,x=-15,y=-7,width=slot+.375)
            original = r[:]; before = dict(m)
            writes = execute(M.stub(),M.CAVE,r,m,c)
            actual = struct.unpack('>ffff',bytes(m[original[30]+j] for j in range(16)))
            self.assertEqual(actual,(-15.,-6.,slot+.375,32.))
            self.assertEqual(bytes(m[records+slot*20+j] for j in range(20)),record)
            self.assertTrue(all(r[i]==original[i] for i in [1,2]+list(range(13,28))+[30,31]))
            allowed = set(range(original[1]+0x70,original[1]+0x80)) | set(range(original[1]+0x90,original[1]+0x98)) | set(range(original[30],original[30]+16))
            self.assertTrue(writes <= allowed)
            self.assertTrue(all(m[k]==v for k,v in before.items() if k not in writes))

    def test_rejects_stale_scene_wrong_glossary_and_inactive_records(self):
        for offset,value in ((12,0x654321),(16,99),(5,0)):
            r,m,c,records,_,_ = self.fixture()
            address = records+17*20+offset
            m.update(enumerate(value.to_bytes(1 if offset==5 else 4,'big'),address))
            execute(M.stub(),M.CAVE,r,m,c)
            self.assertEqual(bytes(m[r[30]+j] for j in range(16)),bytes(16))
        # An earlier active record with same glossary index but other scene
        # must not supply the current rectangle or its cached width.
        r,m,c,records,record,_ = self.fixture()
        wrong = bytearray(record); struct.pack_into('>I',wrong,12,0x654321)
        m.update(enumerate(wrong,records))
        execute(M.stub(),M.CAVE,r,m,c)
        self.assertEqual(struct.unpack('>ffff',bytes(m[r[30]+j] for j in range(16))),(315.,561.,38.25,32.))

    def test_old_primary_reproduces_fixed_cell_width_and_shift(self):
        source = Path('work/EBOOT_dec.elf').read_bytes()
        r,m,c,_,_,style = self.fixture()
        r[3] = style
        # Original compact result: row 0, column 9, length 3 ('Kei').
        m.update(enumerate(bytes([0,9,3]),r[1]+0x70))
        m.update(enumerate(struct.pack('>hh',232,560),style+0x20))
        m[style+0x2e] = 31; m[style+0x2f] = 35
        execute(source[0x1b69ac:0x1b6a60],0x1c69ac,r,m,{})
        old = struct.unpack('>ffff',bytes(m[r[30]+j] for j in range(16)))
        self.assertEqual(old,(511.,561.,93.,32.))
        # Same label's renderer record gives x=315, width=38.25, not 511/93.
        r,m,c,_,_,_ = self.fixture()
        execute(M.stub(),M.CAVE,r,m,c)
        self.assertEqual(struct.unpack('>ffff',bytes(m[r[30]+j] for j in range(16))),(315.,561.,38.25,32.))

    def test_packager_accepts_baseline_and_v1_with_identical_result(self):
        import zipfile
        from platforms.ps3 import build_link_background_update as build
        original = Path('work/ps3_link_background_v2_20260917/installed-backup-01/EBOOT-original.BIN').read_bytes()
        with zipfile.ZipFile('work/ps3_link_background_20260917/SRW-Z3-PS3-RPCS3-link-background-update.zip') as z:
            v1 = z.read('PS3_GAME/USRDIR/EBOOT.BIN')
        updated,_,_ = build.patch(original)
        self.assertEqual(build.patch(v1)[0],updated)
        v2=Path('work/ps3_link_background_v2_20260917/installed-backup-01/EBOOT-v2.BIN').read_bytes()
        self.assertEqual(build.patch(v2)[0],updated)
        broken = bytearray(original); broken[100] ^= 1
        with self.assertRaises(ValueError): build.patch(broken)
        broken = bytearray(updated)
        segs = eboot._segments(broken)
        broken[eboot._off(segs,M.CAVE)+4] ^= 1
        with self.assertRaises(AssertionError): L.check(broken)


if __name__ == '__main__': unittest.main()
