"""Validate direct patched PPC branches against ELF LOAD permissions.

Compare native executable sections, not strings that happen to resemble
instructions. Follow reachable injected code outside those native sections,
including conditional paths and call continuations. Indirect branch targets
and runtime pointer lifetimes still require their own tests.
"""
import struct


def loads(blob):
    if blob[:6] != b'\x7fELF\x02\x02':
        raise ValueError('Expected big-endian ELF64')
    offset = struct.unpack_from('>Q', blob, 32)[0]
    size, count = struct.unpack_from('>HH', blob, 54)
    if size != 56:
        raise ValueError('Unexpected ELF program header size')
    return [row for i in range(count)
            for row in [struct.unpack_from('>IIQQQQQQ', blob, offset + i * size)]
            if row[0] == 1 and row[6]]


def executable_offset(blob, va, size=4):
    for row in loads(blob):
        if row[3] <= va and va + size <= row[3] + row[5]:
            if not row[1] & 1 or row[1] & 2:
                raise ValueError('Code at %#x is not in a read-only executable LOAD' % va)
            offset = row[2] + va - row[3]
            if offset + size > len(blob):
                break
            return offset
    raise ValueError('Code at %#x is not file-backed executable memory' % va)


def code_sections(blob):
    offset = struct.unpack_from('>Q', blob, 40)[0]
    size, count = struct.unpack_from('>HH', blob, 58)
    if size != 64:
        raise ValueError('Unexpected ELF section header size')
    result = []
    for i in range(count):
        row = struct.unpack_from('>IIQQQQIIQQ', blob, offset + i * size)
        if row[2] & 4 and row[5]:  # SHF_EXECINSTR
            executable_offset(blob, row[3], row[5])
            result.append((row[3], row[3] + row[5], row[4]))
    if not result:
        raise ValueError('No original executable sections')
    return result


def branch_target(word, pc):
    op = word >> 26
    if op not in (16, 18):
        return None
    bits = 26 if op == 18 else 16
    displacement = word & ((1 << bits) - 4)
    if displacement & (1 << (bits - 1)):
        displacement -= 1 << bits
    return ((0 if word & 2 else pc) + displacement) & 0xffffffff


def check_changed_branches(original, patched):
    sections = code_sections(original)
    pending, seen, edges = [], set(), set()

    def destination(pc, target):
        executable_offset(patched, target)
        edges.add((pc, target))
        if not any(lo <= target < hi for lo, hi, _ in sections):
            pending.append(target)

    for lo, hi, offset in sections:
        base = executable_offset(patched, lo, hi - lo)
        for va in range(lo, hi, 4):
            pos = base + va - lo
            word = struct.unpack_from('>I', patched, pos)[0]
            old = struct.unpack_from('>I', original, offset + va - lo)[0]
            target = branch_target(word, va)
            if old != word and target is not None:
                destination(va, target)
    while pending:
        pc = pending.pop()
        if pc in seen or any(lo <= pc < hi for lo, hi, _ in sections):
            continue
        seen.add(pc)
        if len(seen) > 16384:
            raise ValueError('Injected-code traversal exceeded bound')
        pos = executable_offset(patched, pc)
        word = struct.unpack_from('>I', patched, pos)[0]
        if word == 0:
            raise ValueError('Injected code falls into zero padding at %#x' % pc)
        target = branch_target(word, pc)
        if target is not None:
            destination(pc, target)
            if word >> 26 == 18 and not word & 1:
                continue  # unconditional non-link branch has no fallthrough
        # bclr/bcctr: stop unconditional returns/tails; retain conditional
        # fallthrough and link-return continuation. Do not invent indirect PCs.
        if word >> 26 == 19 and (word >> 1) & 1023 in (16, 528):
            if (word >> 21) & 20 == 20 and not word & 1:
                continue
        pending.append(pc + 4)
    return {'direct_branch_edges': len(edges), 'injected_instructions': len(seen)}
