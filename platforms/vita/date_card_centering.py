"""Date-card-only entry into VWF-aware centering, including native font mode 3.

The native date drawer already uses x=640, y=340 and size=40. Its center
routine bypasses UI.CENTER_SITE when font_state+0x6c is nonzero. Keep that
font state for drawing; select the measured-width branch only for date cards.
"""
from category_port import require, digest
from inspect_vwf import segment
from self_decrypt import parse, make_fself
import vwf

CALL = 0x8109E384
NATIVE_CENTER = 0x8100791E
MEASURED_PATH = 0x81007944
RESERVATION = 0x812B5F68  # immediately after the native-name wrapper; leave room for link hooks
LIMIT = 0x812B5FF4  # leave both UI relative-pointer words intact


def stub(address, lookup):
    # Unknown/untranslated dates keep the complete native behavior. Known
    # dates are guaranteed single-line Latin by the category preparation.
    # Reproduce the native prologue/argument saves, then skip only the mode
    # test. Its original epilogue unwinds this identical frame.
    return vwf.assemble('''
        push {r7,lr}
        vpush {s0-s1}
        mov r7,r0
        bl %d
        cmp r7,r0
        vpop {s0-s1}
        pop.w {r7,lr}
        beq unchanged
        push {r4-r6,lr}
        vpush {s16-s19}
        vmov.f32 s16,s2
        vmov.f32 s17,s1
        vmov.f32 s18,s0
        mov r4,r2
        mov r5,r1
        mov r6,r0
        b.w %d
    unchanged:
        b.w %d
    ''' % (lookup, MEASURED_PATH, NATIVE_CENTER), address)


def apply(executable, lookup):
    import ui_text
    info = parse(executable)
    raw, base = segment(executable, info, 0)
    code = stub(RESERVATION, lookup)
    require(RESERVATION + len(code) <= LIMIT, 'Date centering exceeds reserved code space')
    expected = vwf.assemble('bl %d' % NATIVE_CENTER, CALL)
    require(raw[CALL-base:CALL-base+4] == expected, 'Date drawer call changed/already patched')
    require(raw[lookup-base:lookup-base+len(ui_text.stub(lookup))] == ui_text.stub(lookup),
            'Expected exact-text translation lookup not found')
    # The existing width hook must be a BL, not the unpatched multiply.
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    site = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(
        raw[ui_text.CENTER_SITE-base:ui_text.CENTER_SITE-base+4], ui_text.CENTER_SITE))
    require(len(site) == 1 and site[0].mnemonic == 'bl', 'VWF-aware center hook required')
    require(not any(raw[RESERVATION-base:LIMIT-base]), 'Date code reservation occupied')
    changed = bytearray(raw)
    changed[CALL-base:CALL-base+4] = vwf.assemble('bl %d' % RESERVATION, CALL)
    changed[RESERVATION-base:RESERVATION-base+len(code)] = code
    segments = {n: segment(executable, info, n)[0] for n in range(len(info['infos']))}
    segments[0] = bytes(changed)
    result = make_fself(info, segments)
    restored = bytearray(segments[0])
    restored[CALL-base:CALL-base+4] = expected
    restored[RESERVATION-base:RESERVATION-base+len(code)] = bytes(len(code))
    require(bytes(restored) == raw, 'Date patch changed unrelated code')
    return result, dict(call=hex(CALL), stub_address=hex(RESERVATION), stub_bytes=len(code),
                        scope='Date-card caller only; known translated strings',
                        native_x=640, native_y=340, native_font_size=40,
                        font_state_preserved=True, unknown_text_native_fallback=True,
                        unchanged_other_segments=True, sha256=digest(result), runtime_tested=False)
