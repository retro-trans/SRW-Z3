"""PCSG00264 1.00 Thumb VWF candidate, porting the PS3 advance/pen rules.

Not a PS3 code transplant. Pinned Vita instructions, relative Thumb branches,
and native GXT cell numbers only. This module does not install or release files.
"""
import copy
import hashlib
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'work/vita/python_deps'), str(Path(__file__).parent)]
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB, KS_MODE_LITTLE_ENDIAN
from self_decrypt import make_fself, parse, require

SOURCE_SHA = '14414068b44fa8ded7f9acb467dceddb4cd02c88845a4109a6e811960cc985d1'
TEXT_END = 0x812B5D54
TEXT_LIMIT = 0x812B6000
DELTA = TEXT_LIMIT - 4
BANK_CELL = 6 * 192  # SJIS 0x87xx, not ASCII and not existing Japanese cells.
SITES = {
    'advance': (0x81007370, 'vadd.f32 s18, s18, s21'),
    'normal': (0x810DA058, 'mla r11, r3, r2, r11'),
    'mode1': (0x810DA0F2, 'mla r9, r3, r0, r9'),
    'keyword': (0x810DA1FE, 'mla r10, r3, r2, r10'),
    'substitution': (0x810DA48A, 'mla r7, r11, r7, r8'),
    'piece_end': (0x810D9F4E, 'add.w r9, r9, r0, asr #1'),
}


def assemble(source, address):
    result, _ = Ks(KS_ARCH_ARM, KS_MODE_THUMB | KS_MODE_LITTLE_ENDIAN).asm(source, address)
    require(result is not None, 'Thumb assembly failed')
    return bytes(result)


def pen_relocation(text_base, data_base, scratch):
    """SCE format0 R_ARM_REL32: patch seg0 delta word, symbol seg1 scratch.

    Vita3K kernel/src/relocation.cpp: format(4), symseg(4), code(8),
    patchseg(4), code2(8), dist2(4), then addend32 and offset32.
    Rel32 writes symbol_segment_loaded_base + addend - patch_loaded_address.
    """
    return struct.pack('<III', (1 << 4) | (3 << 8), scratch-data_base, DELTA-text_base)


def stubs(widths, scratch):
    require(len(widths) == 192 and all(1 <= w <= 32 for w in widths), 'Invalid width bank')
    blob = bytearray()
    entries = {}

    def emit(name, source):
        address = TEXT_END + len(blob)
        entries[name] = address
        blob.extend(assemble(source, address))
        return address

    # Relative pointer: ADR reaches the delta word, whose value is relative
    # to itself. The appended REL32 record updates it even when code and
    # data move independently. Within-text ADR/BL need no relocations.
    helper = emit('scratch', 'adr r0, #%d; ldr r1, [r0]; add r0, r1; bx lr' % DELTA)
    save = 'push.w {r0-r3, r12, lr}; mrs r0, apsr; push {r0}; '
    restore = 'pop {r0}; msr apsr_nzcvq, r0; pop.w {r0-r3, r12, pc}'
    # PS3 rule: sentinel 32 retains the game's advance; Latin uses measured
    # width/32 times the actual glyph quad width. Preserve s19/s21 and flags.
    emit('advance', save + '''
        vpush {s0-s1}
        vmov.f32 s0, s21
        sub.w r0, r9, #%d
        cmp r0, #192
        bhs original
        adr r1, #%d
        ldr r2, [r1]
        add r1, r2
        adds r1, #4
        ldrb r0, [r1, r0]
        cmp r0, #32
        beq original
        vmov s0, r0
        vcvt.f32.u32 s0, s0, #5
        vmul.f32 s0, s0, s19
    original:
        vadd.f32 s18, s18, s0
        bl %d
        vldr s1, [r0]
        vadd.f32 s1, s1, s0
        vstr s1, [r0]
        vpop {s0-s1}
    ''' % (BANK_CELL, DELTA, helper) + restore)
    reset=emit('reset', 'push.w {r0,r1,r12,lr}; mrs r0,apsr; push {r0}; '
        'bl %d; movs r1,#0; str r1,[r0]; pop {r0}; msr apsr_nzcvq,r0; '
        'pop.w {r0,r1,r12,pc}' % helper)
    for name, target, base, column in (
            ('normal', 'r11', 'r11', 'r3'),
            ('mode1', 'r9', 'r9', 'r3'),
            ('keyword', 'r10', 'r10', 'r3'),
            ('substitution', 'r7', 'r8', 'r11')):
        # Unlike the other callbacks, the keyword callback keeps its row in
        # LR across the original MLA. BL necessarily destroys that live value.
        # Recover the same native fifth argument loaded at 0x810DA192;
        # 0x30 caller offset + 4 bytes holding our return address.
        row_restore='ldr.w lr, [sp, #0x34]; ' if name=='keyword' else ''
        emit(name, 'push {lr}; add.w %s, %s, %s, asr #7; bl %d; '
             % (target, base, column, reset) + row_restore + 'pop {pc}')
    # PS3 piece layout units are 1/128 pixel, rather than a count of SJIS
    # characters. The original byte count/pointer advancement stays intact.
    emit('piece_end', save + '''
        vpush {s0}
        bl %d
        vldr s0, [r0]
        vcvt.s32.f32 s0, s0, #7
        vmov r1, s0
        add r9, r1
        movs r1, #0
        str r1, [r0]
        vpop {s0}
    ''' % helper + restore)
    require(TEXT_END + len(blob) <= DELTA, 'VWF code exceeds verified segment gap')
    code_size = len(blob)
    blob.extend(bytes(DELTA - TEXT_END - len(blob)))
    blob.extend(struct.pack('<I', (scratch - DELTA) & 0xFFFFFFFF))
    return bytes(blob), entries, code_size


def patch(original, widths):
    require(hashlib.sha256(original).hexdigest() == SOURCE_SHA, 'Unknown Vita executable; refusing patch')
    info = parse(original)
    require(len(info['phdrs']) == 5, 'Unexpected segment count')
    require(all(s[2:] == (1, 2) for s in info['infos']), 'Expected plain SELF')
    segs = {i: original[s[0]:s[0]+s[1]] for i, s in enumerate(info['infos'])}
    p0, p1 = info['phdrs'][:2]
    require(p0[2] + p0[4] == TEXT_END and p0[4] == p0[5] and p0[6] == 5,
            'Unexpected text layout')
    require(p1[2] == TEXT_LIMIT and p1[6] == 6, 'Unexpected data layout')
    scratch = (p1[2] + p1[5] + 3) & ~3
    code, entries, used = stubs(widths, scratch)
    changed = bytearray(segs[0])
    audit_sites = []
    for name, (site, instruction) in SITES.items():
        old, new = assemble(instruction, site), assemble('bl %d' % entries[name], site)
        off = site - p0[2]
        require(len(old) == len(new) == 4 and changed[off:off+4] == old,
                'Instruction mismatch at ' + name)
        changed[off:off+4] = new
        audit_sites.append(dict(name=name, address=hex(site), original=old.hex(), patched=new.hex()))
    changed.extend(code)
    segs[0] = bytes(changed)
    # Keep all original BSS zero-filled and append one NEW float and the
    # immutable 192-byte width bank. Data is not executable; the existing
    # relocated scratch pointer also addresses the adjacent width bank. This
    # not borrow a guessed unused game global. Existing segment indexes,
    # virtual addresses and relocation payloads are preserved.
    segs[1] += bytes(scratch - p1[2] + 4 - len(segs[1]))
    segs[1] += widths
    require(info['phdrs'][3][0] == 0x60000000, 'Expected final SCE relocation segment')
    relocation = pen_relocation(p0[2], p1[2], scratch)
    segs[3] += relocation
    updated = copy.deepcopy(info)
    phdrs = [list(p) for p in info['phdrs']]
    for i in (0, 1):
        phdrs[i][4] = phdrs[i][5] = len(segs[i])
    phdrs[3][4] = len(segs[3])
    cursor = 52 + 32 * len(phdrs)
    for i in sorted(range(len(phdrs)), key=lambda i: info['phdrs'][i][1]):
        align = max(16, phdrs[i][7])
        cursor = (cursor + align - 1) & -align
        phdrs[i][1] = cursor
        cursor += len(segs[i])
    updated['phdrs'] = [tuple(p) for p in phdrs]
    updated['elen'] = cursor
    result = make_fself(updated, segs)
    # Apart from six guarded instruction replacements, original code is exact.
    restored = bytearray(segs[0][:p0[4]])
    for row in audit_sites:
        off = int(row['address'], 16) - p0[2]
        restored[off:off+4] = bytes.fromhex(row['original'])
    require(bytes(restored) == original[info['infos'][0][0]:info['infos'][0][0]+p0[4]],
            'Unexpected original text mutation')
    require(segs[1][:p1[4]] == original[info['infos'][1][0]:info['infos'][1][0]+p1[4]]
            and not any(segs[1][p1[4]:scratch-p1[2]+4]), 'Original data/BSS mutation')
    audit = dict(source_sha256=SOURCE_SHA, candidate_sha256=hashlib.sha256(result).hexdigest(),
                 sites=audit_sites, code_bytes=used, reserved_gap_bytes=len(code),
                 scratch_address=hex(scratch), entries={k: hex(v) for k, v in entries.items()},
                 original_relocation_bytes_preserved=True,
                 added_relocation=dict(segment=3, kind='SCE-format0-R_ARM_REL32', bytes=relocation.hex()),
                 original_bss_preserved=True,
                 runtime_tested=False, release_ready=False)
    return result, audit
