"""Ink-center only the known UTF-8 combat effect banners.

The native effect caller sets a normal font then calls the shared centered
drawer, which counts Japanese cells. Retain its center, scale, animation and
color; bypass cell centering only for this caller and the 39 translated labels.
"""
import hashlib
import struct
import battle_effect_labels as labels
import localization
from intermission_layout import ink
from battle_name_transport import branch, target

SITE = 0x110860
CALLER = 0x103634
CAVE = 0x78DD00  # RX, after battle_name_transport, before search_layout
TABLE = 0x78DE00
END = 0x78E000
CONTRACTS = (
    (0x103580, 0x103638, '88598169fc53833faa95df031d10a9fd69eec12736c00d91ebaaeab6a409e506'),
    (0x1107bc, SITE, 'a7b9ddf0d817d679b3aa3aa35bb017434ccae83eb72363716e8d3fe5c49443d5'),
    (SITE+4, 0x110938, '09e44ddc79f116c1beb006d9fcd34c95bff212096a0d3475ebab6c9325707f65'),
)


def stub():
    import eboot
    p, a = eboot._ppc(), eboot._Asm()
    def emit(op, *args): a.emit(p[op](*args))
    def const(r, v):
        emit('lis', r, v >> 16); emit('ori', r, r, v & 65535)
    def tail(va): a.emit(int.from_bytes(branch(CAVE+4*len(a.w), va, False), 'big'))
    # 0x1107bc saved its caller at SP+0xb0 in the native 0xa0 frame.
    emit('ld', 9, 1, 0xb0); const(10, CALLER)
    emit('cmplw', 9, 10); a.br('bne', 'original')
    emit('cmpwi', 7, 0); a.br('bne', 'original')
    emit('lwz', 11, 2, -0x7f3c)
    emit('lhz', 9, 11, 0xac)
    emit('cmpwi', 9, 0); a.br('bne', 'original')
    const(10, TABLE)
    a.label('scan')
    emit('lwz', 9, 10, 0)
    emit('cmpwi', 9, 0); a.br('beq', 'original')
    emit('cmplw', 9, 3); a.br('beq', 'found')
    emit('addi', 10, 10, 8); a.br('b', 'scan')
    a.label('found')
    # Negative half-width in ems; the VWF advance uses quad width /32.
    emit('lfs', 13, 10, 4); emit('lfs', 0, 11, 0x54)
    emit('fmuls', 13, 13, 0); emit('fadds', 1, 1, 13)
    tail(0x140f4)
    a.label('original'); tail(0x14954)
    code = a.code()
    assert CAVE+len(code) <= TABLE
    return code


def table(blob, mapping, widths):
    cat = localization.english()
    result = bytearray()
    for mid, _, refs in labels.BINDINGS:
        va = struct.unpack_from('>I', blob, refs[0])[0]
        result += struct.pack('>If', va, -ink(cat.text(mid), mapping, widths, 32)/64)
    result += bytes(8)
    assert TABLE+len(result) <= END
    return bytes(result)


def contract(blob):
    import eboot
    segs = eboot._segments(blob)
    for lo, hi, digest in CONTRACTS:
        off = eboot._off(segs, lo)
        assert hashlib.sha256(blob[off:off+hi-lo]).hexdigest() == digest, hex(lo)


def patch(blob, mapping, widths):
    import eboot, ppc_permissions
    contract(blob); labels.check_built(blob, mapping, widths)
    out = bytearray(blob); segs = eboot._segments(out)
    for va, raw in ((CAVE, stub()), (TABLE, table(out, mapping, widths))):
        off = ppc_permissions.executable_offset(out, va, len(raw))
        assert not any(out[off:off+len(raw)]), 'Effect layout RX reservation occupied'
        out[off:off+len(raw)] = raw
    off = eboot._off(segs, SITE)
    assert out[off:off+4] == branch(SITE, 0x14954)
    out[off:off+4] = branch(SITE, CAVE)
    check(out, mapping, widths)
    return out


def check(blob, mapping, widths):
    import ppc_permissions
    contract(blob); labels.check_built(blob, mapping, widths)
    assert target(blob, SITE) == CAVE
    for va, raw in ((CAVE, stub()), (TABLE, table(blob, mapping, widths))):
        off = ppc_permissions.executable_offset(blob, va, len(raw))
        assert blob[off:off+len(raw)] == raw
    print('PASS: 39 combat effect widths, scoped caller/encoding/font and RX layout guards.')
