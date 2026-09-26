"""Separate name-widget width and translated keyword identity for Vita.

Reuse only arithmetic blocks made obsolete by measured geometry. No new RX
segment, absolute pointer, record format, or global strcmp behavior changes.
"""
import vwf
import ui_text
from category_port import require
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB

SECONDARY = 0x810D6A12
SECONDARY_END = 0x810D6A76
NAME = 0x8110B3FA
NAME_END = 0x8110B406
COMPARE = 0x810D8DC6


def target(text,base,site):
    ins = list(Cs(CS_ARCH_ARM,CS_MODE_THUMB).disasm(text[site-base:site-base+4],site))
    require(len(ins)==1 and ins[0].mnemonic=='bl','Expected installed hook')
    return int(ins[0].op_str.lstrip('#'),16)


def apply(text,base,name_at):
    lookup=target(text,base,ui_text.SITE)
    center=target(text,base,ui_text.CENTER_SITE)
    require(text[lookup-base:lookup-base+len(ui_text.stub(lookup))]==ui_text.stub(lookup),'Unknown lookup')
    require(text[center-base:center-base+len(ui_text.center_stub(center,lookup))]==ui_text.center_stub(center,lookup),'Unknown measured-width helper')
    edits=[]
    def put(address,expected,raw):
        original=bytes(text[address-base:address-base+len(raw)])
        if expected is not None:
            require(original==vwf.assemble(expected,address),'Geometry guard '+hex(address))
        edits.append((address,original))
        text[address-base:address-base+len(raw)]=raw
    secondary=vwf.assemble('''
        addw r2,r5,#0x714
        ldrsb.w r1,[r0,#0x2d]
        adds r1,#1
        vmov s2,r1
        vcvt.f32.s32 s2,s2
        vstr s2,[r2,#12]
        ldrsh.w r1,[r8]
        vmov s0,r1
        vcvt.f32.s32 s0,s0
        vstr s0,[r2]
        ldrsh.w r1,[r8,#2]
        vmov s1,r1
        vcvt.f32.s32 s1,s1
        vstr s1,[r2,#4]
        b.w %d
    '''%SECONDARY_END,SECONDARY)
    compare_at=SECONDARY+len(secondary)
    compare=vwf.assemble('''push {r7,lr}; vpush {s0-s1}; mov r7,r1;
        bl %d; mov r1,r7; vpop {s0-s1}; blx 0x8121da20; pop {r7,pc}'''%lookup,compare_at)
    require(compare_at+len(compare)<=SECONDARY_END,'Comparison helper exceeds obsolete geometry')
    # Entire original geometry is guarded, including the now-unused width math.
    old='''ldrb.w r1,[r8,#4]; lsrs r1,r1,#1; ldrsb.w r2,[r0,#0x2e]; mul r1,r1,r2;
        ldrsh.w r2,[r8]; vmov s0,r2; ldrsb.w r0,[r0,#0x2d]; ldrsh.w r2,[r8,#2];
        vmov s1,r2; adds r0,#1; vmov s2,r0; vcvt.f32.s32 s0,s0; vmov s3,r1;
        movw r0,#0x714; adds r0,r5,r0; vcvt.f32.s32 s1,s1; mov.w r1,#0x718;
        vcvt.f32.s32 s2,s2; vstr s0,[r0]; vcvt.f32.s32 s3,s3; adds r0,r5,r1;
        movw r1,#0x71c; vstr s1,[r0]; adds r0,r5,r1; mov.w r1,#0x720;
        adds r1,r5,r1; vstr s3,[r0]; vstr s2,[r1]'''
    raw=secondary+compare
    raw+=vwf.assemble('nop',0)*((SECONDARY_END-SECONDARY-len(raw))//2)
    put(SECONDARY,old,raw)
    put(COMPARE,'blx 0x8121da20',vwf.assemble('bl %d'%compare_at,COMPARE))
    # r0 is the actual displayed name returned by the native name resolver.
    # Reuse the existing translated Latin measurement helper. Its fallback
    # receives native cell count/pitch for unknown/Japanese labels. The fake
    # font-state contains only the float quad width at +0x14 which it reads.
    name=vwf.assemble('''
        push {r4,r6,r7,lr}
        sub sp,#24
        mov r6,r0
        blx 0x8121dc30
        lsrs r0,r0,#1
        vmov s0,r0
        vcvt.f32.u32 s0,s0
        ldr r0,[r5,#0x14]
        vmov s1,r0
        vcvt.f32.u32 s1,s1
        ldr r0,[r5,#0xc]
        vmov s2,r0
        vcvt.f32.u32 s2,s2
        vstr s2,[sp,#0x14]
        mov r0,sp
        bl %d
        vmov r0,s0
        add sp,#24
        pop {r4,r6,r7,pc}
    '''%center,name_at)
    from main_link_background import END
    require(name_at+len(name)<=END,'Name helper exceeds obsolete primary geometry')
    require(text[name_at-base:name_at-base+len(name)]==vwf.assemble('nop',0)*(len(name)//2),'Name helper reservation occupied')
    put(name_at,None,name)
    put(NAME,'blx 0x8121dc30; ldr r1,[r5,#0x14]; lsrs r0,r0,#1; mul r0,r1,r0',
        vwf.assemble('bl %d; nop.w; nop.w'%name_at,NAME))
    # The helper returns float bits; native VMOV s2,r0 remains in place.
    put(0x8110B41A,'vcvt.f32.u32 s2,s2',vwf.assemble('nop.w',0x8110B41A))
    return edits,dict(name_helper=hex(name_at),name_bytes=len(name),
        compare_helper=hex(compare_at),compare_bytes=len(compare),
        name_geometry=hex(NAME),term_identity_comparison=hex(COMPARE))
