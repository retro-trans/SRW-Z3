"""The primary MtV highlight uses parsed character columns, not draw records.

Prefer the registered rendered link with the same scene AND glossary index.
This fixes both its start position and width. Do not equate a glossary index
with a flat render-slot index: speakers, repeated terms and other scenes differ.
Reuse the obsolete fixed-cell geometry block; no new RX segment or relocation.
"""
import hashlib
import vwf
from category_port import require

START = 0x810D64EE
END = 0x810D65C0
SOURCE_SHA = '26642e7f83a2bd5401943fce376e3f4c84f7d3191e92f356155ab6571ff2c09d'


def stub(select_at, offset):
    return vwf.assemble('''
        push.w {r4-r8,lr}
        bl 0x810d6dc8
        ldr.w r8,[r0,#0xc]
        mov r0,r6
        bl 0x81109ed2
        mov r7,r0
        bl 0x810d8b1e
        mov r4,r0
        movs r6,#0
    loop:
        mov r0,r4
        mov r1,r6
        bl 0x810d8df8
        cbz r0,next
        ldr r1,[r0,#0xc]
        cmp r1,r8
        bne next
        ldr r1,[r0,#0x10]
        cmp r1,r7
        beq found
    next:
        adds r6,#1
        cmp.w r6,#256
        blo loop
        b done
    found:
        mov r8,r6
        mov r6,r0
        mov r4,r8
        subw r5,r5,#0x714
        bl %d
        addw r5,r5,#0x714
        addw r2,r2,#1024
        ldrsb.w r1,[r2,r4]
        adds r1,#1
        vmov s1,r1
        vcvt.f32.s32 s1,s1
        vstr s1,[r5,#12]
        ldrsh.w r1,[r6]
        vmov s2,r1
        vcvt.f32.s32 s2,s2
        vstr s2,[r5]
        ldrsh.w r1,[r6,#2]
        adds r1,#1
        vmov s0,r1
        vcvt.f32.s32 s0,s0
        vstr s0,[r5,#4]
    done:
        pop.w {r4-r8,lr}
        b.w %d
    ''' % (select_at, END), START)


def apply_text(text, base, select_at, offset):
    original = bytes(text[START-base:END-base])
    require(hashlib.sha256(original).hexdigest() == SOURCE_SHA,
            'Primary link geometry source differs/already patched')
    code = stub(select_at, offset)
    require(len(code) <= END-START, 'Primary geometry replacement too large')
    text[START-base:END-base] = code + vwf.assemble('nop', START)*( (END-START-len(code))//2 )
    return original, dict(start=hex(START), end=hex(END), code_bytes=len(code),
                          matching='scene identity and glossary index',
                          no_registered_match='leave zero rectangle; no fabricated highlight')
