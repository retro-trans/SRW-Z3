"""Keep long battle speaker names out of the native 31-byte caption field.

See docs/BATTLE_NAME_TRANSPORT.md for the native producer/consumer trace.
Only the three caption strcpy call sites and the name-only draw call change.
Short strings retain native representation. Long strings use a tagged pointer
to the same battle-lifetime text already retained by the native speaker cache.
The native 31-byte snapshot copy preserves this token; no structure grows.
"""
import hashlib
import struct

COPY_SITES = (0x1073e4, 0x107494, 0x10767c)
DRAW_SITE = 0x10826c
STRCPY = 0x55a460
DRAW = 0x110c3c
CAPACITY = 31
# Reserved RX gap after runtime-name data, before search_layout at0x78E000.
# EXT is data-only, including after hardware packaging; never emit code there.
CAVE = 0x78DC00
CAVE_END = 0x78DD00
MAGIC = 0x01424e50  # control byte + BNP; cannot be a canonical name prefix
# Guard the cache lifetime contract, 31-byte clear, display field selection,
# and native snapshot transfer, not merely the four replaced instructions.
NATIVE_REGIONS = (
    (0x10098c, 0x100a84, '94eee2c87630f165ffd0914c92605c849ee225d9a21bd53bcb5c868b5d6a7ba0'),
    (0x105798, 0x10585c, 'e9ce4735ac6a3f8ca20c2540c7faae96945c609a306ce193ec79ea03370aa48a'),
    (0x11e014, 0x11e0b8, '0c150443147af5ad6679e40ecd83be4aae186c7ab60a730a8c309bb774776890'),
    (0x11fef0, 0x120010, 'e82783d4e226b79b7226bc8d8f84c9a7489a14570494666b212ffcc32b848d4d'),
)


def branch(site, target, link=True):
    displacement = target - site
    assert displacement % 4 == 0 and -(1 << 25) <= displacement < (1 << 25)
    return struct.pack('>I', 0x48000000 | (displacement & 0x3fffffc) | int(link))


def copy_stub():
    import eboot
    p, a = eboot._ppc(), eboot._Asm()
    a.emit(p['addi'](6, 0, 0))
    a.label('scan')
    a.emit(p['lbzx'](7, 4, 6))
    a.emit(p['cmpwi'](7, 0)); a.br('beq', 'short')
    a.emit(p['addi'](6, 6, 1))
    a.emit(p['cmpwi'](6, CAPACITY)); a.br('blt', 'scan')
    a.emit(p['lis'](7, MAGIC >> 16)); a.emit(p['ori'](7, 7, MAGIC & 65535))
    a.emit(p['stw'](7, 3, 0)); a.emit(p['stw'](4, 3, 4))
    a.emit(p['addi'](7, 0, 0)); a.emit(p['stb'](7, 3, 8))
    a.emit(0x4e800020)
    a.label('short')
    a.emit(p['addi'](6, 0, 0))
    a.label('copy')
    a.emit(p['lbzx'](7, 4, 6)); a.emit(p['add'](8, 3, 6))
    a.emit(p['stb'](7, 8, 0)); a.emit(p['addi'](6, 6, 1))
    a.emit(p['cmpwi'](7, 0)); a.br('bne', 'copy')
    a.emit(0x4e800020)
    return a.code()


def draw_stub(va):
    import eboot
    p, a = eboot._ppc(), eboot._Asm()
    # Check one byte at a time: an empty/short ordinary string is never read
    # beyond its terminator. A native reset clears byte zero, invalidating it.
    for i, value in enumerate(MAGIC.to_bytes(4, 'big')):
        a.emit(p['lbz'](0, 4, i)); a.emit(p['cmpwi'](0, value))
        a.br('bne', 'draw')
    a.emit(p['lwz'](4, 4, 4))
    a.label('draw')
    a.emit(int.from_bytes(branch(va + len(a.w) * 4, DRAW, False), 'big'))
    return a.code()


def patch(blob, cursor):
    import eboot
    out = bytearray(blob)
    segs = eboot._segments(out)
    assert cursor % 4 == 0
    import ppc_permissions
    copy_va = CAVE
    copy = copy_stub()
    draw_va = copy_va + len(copy)
    payload = copy + draw_stub(draw_va)
    assert copy_va + len(payload) <= CAVE_END, 'Battle transport exceeds RX reservation'
    start = ppc_permissions.executable_offset(out, copy_va, len(payload))
    assert not any(out[start:start + len(payload)]), 'Battle transport cave occupied'
    for site, original, target in [(s, STRCPY, copy_va) for s in COPY_SITES] + [(DRAW_SITE, DRAW, draw_va)]:
        off = eboot._off(segs, site)
        assert out[off:off + 4] == branch(site, original), ('Battle transport source changed', hex(site))
        out[off:off + 4] = branch(site, target)
    out[start:start + len(payload)] = payload
    check(out)
    return out, cursor  # no translation-data allocation


def target(blob, site):
    import eboot
    off = eboot._off(eboot._segments(blob), site)
    w = struct.unpack_from('>I', blob, off)[0]
    assert w & 0xfc000003 == 0x48000001, hex(site)
    disp = w & 0x3fffffc
    return site + (disp - 0x4000000 if disp & 0x2000000 else disp)


def check(blob):
    import eboot
    import ppc_permissions
    segs = eboot._segments(blob)
    for start, end, digest in NATIVE_REGIONS:
        off = eboot._off(segs, start)
        assert hashlib.sha256(blob[off:off + end - start]).hexdigest() == digest, ('Battle transport contract changed', hex(start))
    copy_va = target(blob, COPY_SITES[0])
    assert copy_va == CAVE, 'Battle transport must use reserved RX cave'
    assert all(target(blob, site) == copy_va for site in COPY_SITES)
    draw_va = target(blob, DRAW_SITE)
    assert draw_va == copy_va + len(copy_stub())
    for va, raw in ((copy_va, copy_stub()), (draw_va, draw_stub(draw_va))):
        assert CAVE <= va and va + len(raw) <= CAVE_END
        off = ppc_permissions.executable_offset(blob, va, len(raw))
        assert blob[off:off + len(raw)] == raw, hex(va)
    # Dialogue and the encoding flag loads are NOT routed through the token.
    for va, raw in ((0x108258, '809f0020'), (0x108260, '88bf0028'),
                    (0x108280, '809f0024')):
        off = eboot._off(segs, va)
        assert blob[off:off + 4] == bytes.fromhex(raw), hex(va)
    assert blob[eboot._off(segs, 0x108290):eboot._off(segs, 0x108290) + 4] == branch(0x108290, DRAW)
    print('PASS: all 3 battle name producers use bounded transport; name-only draw resolves full text.')
