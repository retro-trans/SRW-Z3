"""PS3 primary selection geometry: render-record identity, not character cells.

The secondary/backlog helper has a flat render-slot index. The primary helper
instead has a glossary index within scene zero. Match BOTH identities before
using the renderer's x/y and the per-slot measured width. Keep the original
style getter, vertical inset, colour/draw tail, and selection/navigation data.
"""
import hashlib
import struct
import eboot

SITE = 0x1C6964
END = 0x1C6A60
TAIL = 0x1C6900
CAVE = 0x78EE00
SOURCE_SHA = '52b93871ea6b8a5cfd6881afa3dbdae1e8e5634671f205cf80facfbe25298de9'


def branch(site, target, link=False):
    return 0x48000000 | ((target-site) & 0x3fffffc) | int(link)


def stub():
    from link_background_layout import WIDTHS
    p = eboot._ppc()
    a = eboot._Asm()
    emit = a.emit
    def call(target):
        emit(branch(CAVE+len(a.w)*4, target, True))
    # Reuse the primary function's dead local temporaries, not caller linkage
    # or saved nonvolatile registers. r26/r27/r30/r31 stay live for draw tail.
    call(0x1C93C8)
    emit(p['lwz'](9,3,12)); emit(p['stw'](9,1,0x70))
    emit(p['mr'](3,31)); call(0x2540E4)
    emit(p['stw'](3,1,0x74))
    call(0x1CDD74); emit(p['mr'](29,3))
    emit(p['addi'](28,0,0))
    a.label('loop')
    emit(p['mr'](3,29)); emit(p['mr'](4,28)); call(0x1CDBB0)
    emit(p['cmpwi'](3,0)); a.br('beq','next')
    emit(p['lwz'](9,3,12)); emit(p['lwz'](10,1,0x70))
    emit(p['cmplw'](9,10)); a.br('bne','next')
    emit(p['lwz'](9,3,16)); emit(p['lwz'](10,1,0x74))
    emit(p['cmplw'](9,10)); a.br('beq','found')
    a.label('next')
    emit(p['addi'](28,28,1)); emit(p['cmpwi'](28,256))
    a.br('blt','loop'); a.br('b','done')
    a.label('found')
    emit(p['stw'](3,1,0x78))
    emit(p['lis'](9,WIDTHS>>16)); emit(p['ori'](9,9,WIDTHS&65535))
    emit(p['mulli'](10,28,4)); emit(p['add'](9,9,10))
    emit(p['lfs'](0,9,0)); emit(p['stfs'](0,1,0x7c))
    emit(p['mr'](3,31)); emit(p['mr'](4,27)); call(0x1C671C)
    emit(p['lbz'](9,3,0x2d)); emit(p['extsb'](9,9))
    emit(p['addi'](9,9,1))
    emit(p['lwz'](11,1,0x78))
    emit(p['lhz'](10,11,2)); emit(p['extsh'](10,10))
    emit(p['addi'](10,10,1))
    emit(p['lhz'](11,11,0)); emit(p['extsh'](11,11))
    # Convert signed integers exactly as native PPC64 code does.
    for reg, offset in ((11,0),(10,4),(9,12)):
        emit(p['std'](reg,1,0x90)); emit(p['lfd'](0,1,0x90))
        emit(p['fcfid'](0,0)); emit(p['frsp'](0,0))
        emit(p['stfs'](0,30,offset))
    emit(p['lfs'](0,1,0x7c)); emit(p['stfs'](0,30,8))
    a.label('done')
    emit(branch(CAVE+len(a.w)*4,TAIL))
    raw = a.code()
    assert CAVE+len(raw) <= 0x78F000  # next independently owned helper
    return raw


def guard(b, segs, patched=False):
    pos = eboot._off(segs,SITE)
    native = bytearray(b[pos:pos+END-SITE])
    if patched:
        assert int.from_bytes(native[:4],'big') == branch(SITE,CAVE)
        native[:4] = struct.pack('>I',branch(SITE,0x1C93C8,True))
        # v3 reuses only the arithmetic made unreachable by the v2 branch.
        import link_identity_geometry as identity
        if native[4:] == identity.dead_code():
            native[4:] = identity.DEAD_NATIVE
    assert hashlib.sha256(native).hexdigest() == SOURCE_SHA
    # Scene-zero lookup, selected glossary index, active render slot and
    # registration identity. These are NOT interchangeable indices.
    words = {0x1c8ff0:0x8003000c, 0x2540e4:0x81230004,
             0x2540e8:0x88690003, 0x1cdc1c:0x88090005,
             0x1ce1bc:0x93dc0010, 0x1ce1c4:0x907c000c}
    for va, word in words.items():
        assert int.from_bytes(b[eboot._off(segs,va):eboot._off(segs,va)+4],'big') == word, hex(va)


def apply(b,segs):
    guard(b,segs)
    raw = stub(); pos = eboot._off(segs,SITE); dst = eboot._off(segs,CAVE)
    assert not any(b[dst:dst+len(raw)])
    b[pos:pos+4] = struct.pack('>I',branch(SITE,CAVE))
    b[dst:dst+len(raw)] = raw
    check(b)
    return [(pos,pos+4),(dst,dst+len(raw))]


def check(b):
    segs = eboot._segments(b)
    guard(b,segs,True)
    dst = eboot._off(segs,CAVE)
    assert b[dst:dst+len(stub())] == stub()
