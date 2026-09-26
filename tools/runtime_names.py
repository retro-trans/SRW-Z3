"""Translate default player names at the dialogue escape readers, never in saves.

BLJS10256: 1afcf8 builds the $n/$f/$l/$F substitution table. Its three
leaf getters return first name, nickname and surname. $F calls nickname and
surname again, preserving the saved name-order flag and original separator.
The naming/serialization/lookup-key pointers are deliberately not repointed.
"""
import localization as _l10n
import struct

# site, original lwz r3, TOC displacement, default, English, code cave
READERS = (
    (0x1af5a8, 0x8062bad4, -0x452c, 'ヒビキ', _l10n.literal('runtime_names.READERS/0'), 0x78d000),
    (0x1af5b0, 0x8062bad8, -0x4528, 'ヒビキ', _l10n.literal('runtime_names.READERS/1'), 0x78d200),
    (0x1af5b8, 0x8062badc, -0x4524, 'カミシロ', _l10n.literal('runtime_names.READERS/2'), 0x78d400),
)
DATA_VA = 0x78d600
FULL_SURNAME_RETURNS = (0x1afed8, 0x1b016c)


def payload(mapping):
    import digraph
    data = bytearray()
    addresses = {}
    for en in ('Hibiki', 'Kamishiro'):
        addresses[en] = DATA_VA + len(data)
        data += digraph.encode_mixed(en, mapping) + b'\0'
    addresses['compact'] = DATA_VA + len(data)
    data += b'Kamishiro\0'
    return bytes(data), addresses


def stub(reader, addresses):
    import eboot
    site, original, toc, jp, en, cave = reader
    P, A = eboot._ppc(), eboot._Asm()
    def pointer(r, va):
        A.emit(P['lis'](r, va >> 16)); A.emit(P['ori'](r, r, va & 65535))
    A.emit(original)
    A.emit(0x7d800026)                    # mfcr r12: retain the caller's CR
    A.emit(P['cmpwi'](3, 0)); A.br('beq', 'return')
    # Byte-wise, NUL-inclusive equality: no overread after an early mismatch,
    # no substring replacements, and no writes to editable/save buffers.
    for i, byte in enumerate(jp.encode('cp932') + b'\0'):
        A.emit(P['lbz'](0, 3, i)); A.emit(P['cmpwi'](0, byte))
        A.br('bne', 'return')
    if en == 'Kamishiro':
        # Replacement fields are 41 bytes including NUL. A 21-24 byte custom
        # nickname plus the 18-byte VWF surname could overflow $F. For those
        # two full-name calls only, use the native ASCII surname (9 bytes).
        # Custom bytes, normal VWF names, standalone $l and name order survive.
        A.emit(0x7d6802a6)                # mflr r11
        for i, ret in enumerate(FULL_SURNAME_RETURNS):
            pointer(10, ret)
            A.emit(P['cmplw'](11, 10)); A.br('beq', 'length')
        A.br('b', 'english')
        A.label('length')
        A.emit(P['lwz'](9, 2, -0x4528))   # stored nickname, not a translated copy
        A.emit(P['addi'](10, 0, 0))
        A.label('scan')
        A.emit(P['lbz'](0, 9, 0)); A.emit(P['cmpwi'](0, 0))
        A.br('beq', 'english')
        A.emit(P['addi'](9, 9, 1)); A.emit(P['addi'](10, 10, 1))
        A.emit(P['cmpwi'](10, 21)); A.br('blt', 'scan')
        pointer(3, addresses['compact']); A.br('b', 'return')
    A.label('english')
    pointer(3, addresses[en])
    A.label('return')
    A.emit(0x7d8ff120)                    # mtcrf 255,r12
    A.emit(0x4e800020)                    # blr, original LR unchanged
    code = A.code()
    assert len(code) <= 0x200
    return code


def apply(blob, segs, mapping):
    import eboot
    data, addresses = payload(mapping)
    for reader in READERS:
        site, original, _, _, _, cave = reader
        off = eboot._off(segs, site)
        assert blob[off:off+8] == struct.pack('>II', original, 0x4e800020), hex(site)
        code = stub(reader, addresses)
        dest = eboot._off(segs, cave)
        assert not any(blob[dest:dest+len(code)]), 'runtime-name cave overlaps existing data'
        blob[dest:dest+len(code)] = code
        struct.pack_into('>I', blob, off, 0x48000000 | ((cave-site) & 0x3fffffc))
    off = eboot._off(segs, DATA_VA)
    assert not any(blob[off:off+len(data)])
    blob[off:off+len(data)] = data
    return len(READERS)


def verify(blob, segs, mapping):
    import eboot
    data, addresses = payload(mapping)
    for reader in READERS:
        site, original, _, _, _, cave = reader
        off = eboot._off(segs, site)
        assert blob[off:off+8] == struct.pack('>II', 0x48000000 | ((cave-site) & 0x3fffffc), 0x4e800020)
        code = stub(reader, addresses)
        dest = eboot._off(segs, cave)
        assert blob[dest:dest+len(code)] == code
    off = eboot._off(segs, DATA_VA)
    assert blob[off:off+len(data)] == data
