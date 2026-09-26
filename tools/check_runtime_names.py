"""Execute emitted name-reader PPC instructions in a strict, read-only test CPU.

Only instructions actually used by these leaf stubs are supported. Unknown
opcodes and unmapped reads fail; this is not a replacement for RPCS3 visual QA.
"""
import argparse
import json
import struct
from pathlib import Path
import eboot
import runtime_names as rn


def execute(blob, segs, reader, source, nickname, lr):
    site, _, toc, _, _, cave = reader
    memory = {}
    def put(address, data):
        memory.update(enumerate(data, address))
    def get(address, size):
        return bytes(memory[address+i] for i in range(size))
    put(site, blob[eboot._off(segs, site):eboot._off(segs, site)+8])
    put(cave, blob[eboot._off(segs, cave):eboot._off(segs, cave)+0x200])
    put(rn.DATA_VA, blob[eboot._off(segs, rn.DATA_VA):eboot._off(segs, rn.DATA_VA)+64])
    pointer = 0 if source is None else 0x2000000
    put(0x7dd920+toc, struct.pack('>I', pointer))
    if source is not None:
        put(pointer, source+b'\0')
    # Nickname getter must use its own source at the shared TOC slot.
    if toc != -0x4528:
        put(0x7dd920-0x4528, struct.pack('>I', 0x2000100))
        put(0x2000100, nickname+b'\0')
    regs = [0x3000000+i*16 for i in range(32)]
    regs[2] = 0x7dd920
    original_regs = regs[:]
    cr, original_cr = 0xa53cc35a, 0xa53cc35a
    pc = site
    def signed(v, bits):
        return v-(1 << bits) if v & (1 << (bits-1)) else v
    for steps in range(500):
        w = int.from_bytes(get(pc, 4), 'big')
        pc += 4
        op, rt, ra, imm = w >> 26, (w >> 21) & 31, (w >> 16) & 31, w & 65535
        if w == 0x4e800020:
            break
        if w == 0x7d800026:
            regs[12] = cr
        elif w == 0x7d8ff120:
            cr = regs[12]
        elif w == 0x7d6802a6:
            regs[11] = lr
        elif op in (32, 34):
            regs[rt] = int.from_bytes(get(regs[ra]+signed(imm, 16), 4 if op == 32 else 1), 'big')
        elif op in (14, 15):
            regs[rt] = ((regs[ra] if ra else 0)+signed(imm, 16)*(65536 if op == 15 else 1)) & ((1 << 64)-1)
        elif op == 24:
            regs[ra] = regs[rt] | imm
        elif op == 11 or (w & 0xfc0007fe) == 0x7c000040:
            left = signed(regs[ra] & 0xffffffff, 32) if op == 11 else regs[ra] & 0xffffffff
            right = signed(imm, 16) if op == 11 else regs[(w >> 11) & 31] & 0xffffffff
            cr = (cr & 0x0fffffff) | ((8 if left < right else 4 if left > right else 2) << 28)
        elif op == 18:
            assert not w & 3
            pc = pc-4+signed(w & 0x3fffffc, 26)
        elif op == 16:
            bo, bi = (w >> 21) & 31, (w >> 16) & 31
            assert bo in (4, 12)
            test = bool(cr & (1 << (31-bi)))
            if test == (bo == 12):
                pc = pc-4+signed(w & 0xfffc, 16)
        else:
            raise AssertionError(f'unsupported PPC instruction {w:08x} at {pc-4:x}')
    else:
        raise AssertionError('stub did not return')
    assert cr == original_cr
    for i in set(range(32))-{0, 3, 9, 10, 11, 12}:
        assert regs[i] == original_regs[i], i
    # Interpreter allows no stores: neither save data nor the source can change.
    output = bytearray()
    if regs[3]:
        for i in range(64):
            byte = get(regs[3]+i, 1)[0]
            if not byte: break
            output.append(byte)
        else: raise AssertionError('unterminated returned string')
    return regs[3], bytes(output)


def check(blob, mapping):
    segs = eboot._segments(blob)
    rn.verify(blob, segs, mapping)
    _, addresses = rn.payload(mapping)
    count = 0
    for reader in rn.READERS:
        jp, en = reader[3:5]
        default = jp.encode('cp932')
        encoded = eboot.dg.encode_mixed(en, mapping)
        cases = [None, b'', b'Alex', 'アキラ'.encode('cp932'), encoded, default+b'A']
        cases += [default[:i] for i in range(len(default))]
        cases += [default[:i]+bytes([default[i] ^ 1])+default[i+1:] for i in range(len(default))]
        cases += [default]
        for source in cases:
            for lr in (0x1afd28, *rn.FULL_SURNAME_RETURNS):
                pointer, result = execute(blob, segs, reader, source, 'ヒビキ'.encode('cp932'), lr)
                expected = encoded if source == default else source or b''
                assert result == expected, (reader[0], source, result)
                assert pointer == (addresses[en] if source == default else 0 if source is None else 0x2000000)
                count += 1
    surname = rn.READERS[2]
    for length in (0, 6, 12, 19, 20, 21, 22, 23, 24):
        nick = b'X'*length
        for lr in (0x1afdb0, *rn.FULL_SURNAME_RETURNS):
            _, result = execute(blob, segs, surname, surname[3].encode('cp932'), nick, lr)
            compact = lr in rn.FULL_SURNAME_RETURNS and length > 20
            assert result == (b'Kamishiro' if compact else eboot.dg.encode_mixed('Kamishiro', mapping))
            if lr in rn.FULL_SURNAME_RETURNS:
                for full in (nick+b'\x81\x45'+result, result+nick):
                    assert len(full)+1 <= 41, (length, lr)
            count += 1
    # Default $F is built from the nickname, not the separately editable $n.
    first = execute(blob, segs, rn.READERS[1], 'ヒビキ'.encode('cp932'), b'', 0x1afe94)[1]
    last = execute(blob, segs, surname, 'カミシロ'.encode('cp932'), 'ヒビキ'.encode('cp932'), 0x1afed8)[1]
    assert first == eboot.dg.encode_mixed('Hibiki', mapping)
    assert last == eboot.dg.encode_mixed('Kamishiro', mapping)
    assert len(first+b'\x81\x45'+last)+1 <= 41
    print(f'PASS: {count} emitted-PPC name-reader cases; defaults, custom/empty/null names, CR/registers and full-name capacity.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    out = Path(p.parse_args().out)
    mapping = {k: v for k, v in json.loads((out/'pairs.json').read_text()).items() if len(k) == 1}
    check((out/'EBOOT.BIN').read_bytes(), mapping)
