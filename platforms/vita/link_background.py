"""Cache actual VWF link width by native bank/slot; preserve 20-byte records.

The sole registration caller follows keyword drawing, before piece_end clears
the VWF pen. Terms have primary/secondary geometry paths. Speaker names instead
use the separate widget fixed by link_identity_geometry. Cache measured width
and actual rendered style height per term slot. main_link_background replaces
the primary fixed-column path; secondary geometry preserves its native style.
The 16x16 width/height cache is appended to RW data, relative to the existing
relocated names table. No absolute new data pointer or executable data page.
"""
import copy
import struct
import sys
from category_port import ROOT, require, digest
from inspect_vwf import segment
from self_decrypt import parse, make_fself
import vwf
import ui_text
import main_link_background as main_links

# PS3 tools have modules with the same names. UI helpers add tools/ to the
# import path, so deferred unqualified imports can silently choose PS3 code.
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

CAPTURE = 0x810D8D6C
SELECT = 0x810D6A08
STORE = 0x810D6A6E
CAVE = 0x812B5FA0
LIMIT = ui_text.NAMES_POINTER


def stubs(offset):
    # At capture entry the bank/slot are [sp]/[sp+4]. The native strlen
    # result must remain in r0 for the untouched byte-length record field.
    capture = vwf.assemble('''
        push {r4,lr}
        blx %d
        adr.w r1,#%d
        ldr r2,[r1]
        add r1,r2
        ldr r2,[r1]
        adr.w r1,#%d
        ldr r3,[r1]
        add r1,r3
        adds r1,#%d
        ldr r3,[sp,#8]
        ldr r4,[sp,#12]
        add.w r3,r4,r3,lsl #4
        str.w r2,[r1,r3,lsl #2]
        addw r1,r1,#1024
        ldrb.w r2,[r7,#0x2d]
        strb.w r2,[r1,r3]
        pop {r4,pc}
    ''' % (0x8121DC30, vwf.DELTA, ui_text.NAMES_POINTER, offset), CAVE)
    select_at = CAVE+len(capture)
    # r8 is still the requested index; r0 is the fetched record. r1-r3 are
    # dead here (the following style call overwrites them). r2 additionally
    # returns the cache base to our primary helper. Preserve r0 and
    # all callee-saved registers except the original movs destination r8.
    # Null records skip both the cache write and the original draw.
    select = vwf.assemble('''
        cbz r0,unchanged
        adr.w r1,#%d
        ldr r2,[r1]
        add r1,r2
        addw r1,r1,#%d
        mov r2,r1
        ldr.w r1,[r1,r8,lsl #2]
        str.w r1,[r5,#0x71c]
    unchanged:
        movs.w r8,r0
        bx lr
    ''' % (ui_text.NAMES_POINTER, offset), select_at)
    require(select_at+len(select) <= LIMIT, 'Link-width hooks exceed RX reservation')
    return capture, select, select_at


def apply(executable):
    info = parse(executable)
    segments = {n: segment(executable, info, n)[0] for n in range(len(info['infos']))}
    text = bytearray(segments[0]); base = info['phdrs'][0][2]
    # Guard registration provenance, bounded bank/slot allocation, and the
    # selected record/index flow. Do not apply to an unrelated native layout.
    guards = {
        CAPTURE: 'blx 0x8121dc30', SELECT: 'movs.w r8,r0', STORE: 'vstr s3,[r0]',
        0x810DA26A: 'bl 0x810d9f92', 0x810DA298: 'bl 0x810d8cd8',
        0x810D8D0C: 'bl 0x810d8c54', 0x810D8D10: 'ldr.w r9,[sp,#4]',
        0x810D8D4E: 'ldr r0,[sp]', 0x810D8D50: 'add.w r1,r9,r9,lsl #2',
        0x810D8D70: 'strb r0,[r4,#4]', 0x810D6A02: 'mov r1,r8',
        0x810D6A04: 'bl 0x810d8df8', 0x810D6A0C: 'beq 0x810d6a76',
    }
    for address, source in guards.items():
        expected = vwf.assemble(source, address)
        require(text[address-base:address-base+len(expected)] == expected,
                'Link source guard failed at '+hex(address))
    require(not any(text[CAVE-base:LIMIT-base]), 'Link hook cave occupied/already patched')
    pointer = struct.unpack_from('<I', text, ui_text.NAMES_POINTER-base)[0]
    names = (ui_text.NAMES_POINTER+pointer) & 0xffffffff
    p1 = info['phdrs'][1]
    require(p1[4] == p1[5] == len(segments[1]), 'Expected fully initialized VWF data segment')
    cache = (p1[2]+len(segments[1])+3) & ~3
    offset = cache-names
    require(p1[2] <= names < cache and 0 < offset <= 255, 'Unknown relocated names-table layout')
    capture, select, select_at = stubs(offset)
    replacements = {CAPTURE: vwf.assemble('bl %d' % CAVE, CAPTURE),
                    SELECT: vwf.assemble('bl %d' % select_at, SELECT)}
    for address, replacement in replacements.items():
        require(len(replacement) == 4, 'Link hook instruction size mismatch')
        text[address-base:address-base+4] = replacement
    text[CAVE-base:CAVE-base+len(capture+select)] = capture+select
    main_original, main_audit = main_links.apply_text(text, base, select_at, offset)
    from platforms.vita import link_identity_geometry
    extra_edits, extra_audit = link_identity_geometry.apply(text,base,
        main_links.START+main_audit['code_bytes'])
    from platforms.vita import dialogue_link_scene
    extra_edits += dialogue_link_scene.apply(text,base)
    extra_audit['dialogue_scene_fallback'] = hex(dialogue_link_scene.CAVE)
    # All existing Vita relocation entries are format0. Verify the loader
    # cannot overwrite ANY replaced instruction, not only the primary block.
    protected=[(main_links.START,main_links.END),(CAVE,CAVE+len(capture+select))]
    protected += [(a,a+len(raw)) for a,raw in extra_edits]
    protected += [(a,a+len(raw)) for a,raw in replacements.items()]
    for n, ph in enumerate(info['phdrs']):
        if ph[0] != 0x60000000:
            continue
        for at in range(0, len(segments[n]), 12):
            word, addend, off = struct.unpack_from('<III', segments[n], at)
            require(word & 15 == 0, 'Unknown native relocation format')
            if (word >> 16) & 15 == 0:
                for delta, kind in ((0,(word >> 8)&255),((word >> 28)*2,(word >> 20)&255)):
                    require(not kind or all(off+delta+4 <= lo-base or off+delta >= hi-base
                            for lo,hi in protected), 'Relocation overlaps link geometry')
    restored = bytearray(text)
    for address,original in reversed(extra_edits):
        restored[address-base:address-base+len(original)]=original
    restored[main_links.START-base:main_links.END-base] = main_original
    for address in replacements:
        restored[address-base:address-base+4] = segments[0][address-base:address-base+4]
    restored[CAVE-base:CAVE-base+len(capture+select)] = bytes(len(capture+select))
    require(bytes(restored) == segments[0], 'Unrelated code changed')
    segments[0] = bytes(text)
    segments[1] += bytes(cache-p1[2]-len(segments[1])+256*5)
    updated = copy.deepcopy(info)
    headers = [list(p) for p in info['phdrs']]
    headers[1][4] = headers[1][5] = len(segments[1])
    cursor = 52+32*len(headers)
    for n in sorted(range(len(headers)), key=lambda n: headers[n][1]):
        align = max(16, headers[n][7]); cursor = (cursor+align-1) & -align
        headers[n][1] = cursor; cursor += len(segments[n])
    updated['phdrs'] = [tuple(p) for p in headers]; updated['elen'] = cursor
    result = make_fself(updated, segments)
    return result, dict(capture=hex(CAPTURE), select=hex(SELECT), store=hex(STORE),
        capture_stub=hex(CAVE), select_stub=hex(select_at), code_bytes=len(capture+select),
        cache_address=hex(cache), cache_bytes=1280, names_relative_offset=offset,
        slots=256, record_format_and_navigation_unchanged=True,
        translated_term_identity_comparison=True, existing_relocations_unchanged=True,
        primary_geometry=main_audit, name_and_identity=extra_audit, date_centering_preserved=True,
        runtime_tested=False, sha256=digest(result))
