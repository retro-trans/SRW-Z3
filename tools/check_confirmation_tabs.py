"""Execute the emitted VWF PPC stub with unequal quad widths and pitches.

This tests machine instructions rather than repeating the implementation's
spacing formula. Unknown instructions, unmapped accesses and register damage
fail. It is not an in-game visual test.
"""
import struct
import eboot
import digraph as dg


def f32(value):
    return struct.unpack('>f', struct.pack('>f', value))[0]


def execute(code, widths, cell, origin, pen, pitch, quad, acc, extra=()):
    memory = {}
    def put(address, data):
        memory.update(enumerate(data, address))
    def get(address, size):
        return bytes(memory[address+i] for i in range(size))
    def signed(value, bits):
        return value-(1 << bits) if value & (1 << (bits-1)) else value
    regs = [0x2000000+i*0x100 for i in range(32)]
    initial = regs[:]
    floats = [int.from_bytes(struct.pack('>d', i+.125), 'big') for i in range(32)]
    def readf(i):
        return struct.unpack('>d', floats[i].to_bytes(8,'big'))[0]
    def writef(i, value):
        floats[i] = int.from_bytes(struct.pack('>d', value), 'big')
    writef(31, f32(origin)); initial_floats = floats[:]
    stack = regs[1]
    put(eboot.STUB_VA, code)
    put(eboot.TABLE_VA, widths)
    for address, data in extra:
        put(address, data)
    put(stack+0xc2, struct.pack('>H',cell))
    for off,value in [(0x84,pen),(0x94,pitch),(0x9c,quad)]:
        put(stack+off, struct.pack('>f',value))
    put(eboot.PEN_ACC, struct.pack('>f',acc))
    pc, cr = eboot.STUB_VA, 0xa53cc35a
    for _ in range(100):
        word = int.from_bytes(get(pc,4),'big'); pc += 4
        op,rt,ra,rb = word >> 26,(word >> 21)&31,(word >> 16)&31,(word >> 11)&31
        imm = signed(word & 65535,16)
        if word == 0x4e800020:
            break
        if op in (14,15):
            regs[rt] = ((regs[ra] if ra else 0)+imm*(65536 if op==15 else 1)) & ((1 << 64)-1)
        elif op == 24:
            regs[ra] = regs[rt] | (word & 65535)
        elif op == 7:
            regs[rt] = (regs[ra]*imm) & ((1 << 64)-1)
        elif op == 31 and (word >> 1)&1023 == 266:
            regs[rt] = (regs[ra]+regs[rb]) & ((1 << 64)-1)
        elif op == 40:
            regs[rt] = int.from_bytes(get(regs[ra]+imm,2),'big')
        elif op == 31 and (word >> 1)&1023 == 87:
            regs[rt] = get(regs[ra]+regs[rb],1)[0]
        elif op == 11:
            a = signed(regs[ra] & 0xffffffff,32)
            cr = (cr & 0x0fffffff) | ((8 if a<imm else 4 if a>imm else 2) << 28)
        elif op == 18:
            assert not word & 3
            pc = pc-4+signed(word & 0x3fffffc,26)
        elif op == 16:
            bo,bi = rt,ra
            assert bo in (4,12)
            if bool(cr & (1 << (31-bi))) == (bo==12):
                pc = pc-4+signed(word & 0xfffc,16)
        elif op in (62,36,52):
            address = regs[ra]+imm
            size = 8 if op==62 else 4
            assert address in (stack+0xd0,eboot.PEN_ACC), hex(address)
            data = struct.pack('>f',readf(rt)) if op==52 else regs[rt].to_bytes(8,'big')[-size:]
            put(address,data)
        elif op == 48:
            writef(rt,struct.unpack('>f',get(regs[ra]+imm,4))[0])
        elif op == 50:
            floats[rt] = int.from_bytes(get(regs[ra]+imm,8),'big')
        elif op == 63 and (word >> 1)&1023 == 846:  # fcfid: reinterpret integer bits
            writef(rt,float(signed(floats[rb],64)))
        elif op == 63 and (word >> 1)&1023 == 12:
            writef(rt,f32(readf(rb)))
        elif op == 59 and (word >> 1)&31 in (20,21,25):
            kind = (word >> 1)&31
            result = (readf(ra)-readf(rb) if kind==20 else
                      readf(ra)+readf(rb) if kind==21 else
                      readf(ra)*readf((word >> 6)&31))
            writef(rt,f32(result))
        else:
            raise AssertionError('Unknown instruction %08x at %x' % (word,pc-4))
    else:
        raise AssertionError('VWF stub did not return')
    assert cr & 0x0fffffff == 0x053cc35a
    assert all(regs[i]==initial[i] for i in set(range(32))-{0,9})
    assert all(floats[i]==initial_floats[i] for i in set(range(32))-{10,13})
    return readf(13),struct.unpack('>f',get(eboot.PEN_ACC,4))[0]


def check(blob, mapping):
    segs = eboot._segments(blob)
    pos = eboot._off(segs,eboot.STUB_VA)
    code = blob[pos:pos+len(eboot.vwf_stub())]
    pos = eboot._off(segs,eboot.TABLE_VA)
    widths = blob[pos:pos+eboot.ATLAS_CELLS]
    row = dg.encode_mixed('Yes\ue01e/\ue01fNo',mapping)
    cells = [int.from_bytes(row[i:i+2],'big') for i in range(0,len(row),2)]
    cases = 0
    for origin in (0,463.5,-88.5,1024):
        for pitch in (25,31,37.28):
            for quad in (23.3,25,28,40):
                pen,acc = f32(origin),0.0
                for glyph in cells:
                    if glyph in (mapping['/'],mapping['N']):
                        column = 3 if glyph==mapping['/'] else 5
                        assert abs(pen-f32(origin+column*f32(pitch))) < .001, (origin,pitch,quad,glyph,pen)
                    advance,acc = execute(code,widths,dg.cell_index(glyph),origin,pen,pitch,quad,acc)
                    pen = f32(pen+advance); cases += 1
                assert abs(acc-(pen-origin)) < .001
    # The shared drawer must keep ordinary glyphs on their old code path.
    for glyph in list(mapping.values())+[0x8140,0x889f]:
        cell = dg.cell_index(glyph)
        for pitch,quad in [(25,28),(31,23.3)]:
            advance,acc = execute(code,widths,cell,120,163,pitch,quad,7)
            w = widths[cell]
            expected = pitch if w==32 else w*quad/32
            assert abs(advance-expected)<.0001 and abs(acc-7-advance)<.0001
            cases += 1
    print('PASS:',cases,'emitted-PPC VWF cases: live-pitch tabs, unequal scales, ordinary glyphs and register preservation.')
