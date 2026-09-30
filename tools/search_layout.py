"""Screen-local VWF centering for the Spirit search grid and its three tabs.

The FSSA centered-text call at 0x513d4 has r31=record and r26=UI resource.
The grid color path (0xadecc..0xae404) passes a stack copy of its template,
not the original record address. Recognize that exact caller as well.
Shared unit-name templates also opt in by their unique string references,
including copied/recolored records. Other centered widgets keep the original
routine (including confirmation overlays). Unknown/control strings also
fall back, so the game's hidden-name question marks are not rewritten.
"""
import localization as _l10n
import struct

SITE = 0x513D4
CAVE = 0x78E000
RECORD_BASE = 0x97D54
GRID = tuple(range(0xACE94, 0xACF14, 32))
TABS = (0xA8614, 0xA8634, 0xA8654, 0xA87F4, 0xA8814,
        0xA8834, 0xA8974, 0xA8994, 0xA89B4)
TAB_TEXT = (_l10n.literal('search_layout.TAB_TEXT/0'), _l10n.literal('search_layout.TAB_TEXT/1'), _l10n.literal('search_layout.TAB_TEXT/2')) * 3
GRID_CALLER = 0xAE408  # return from the grid's colored-entry draw at 0xae404
GRID_STRINGS = (0xC2D4, 0xC2DA, 0xC2E0, 0xC2E6)


def stub():
    import eboot
    P, a = eboot._ppc(), eboot._Asm()
    def emit(op, *args): a.emit(P[op](*args))
    def const(r, v):
        emit('lis', r, v >> 16); emit('ori', r, r, v & 65535)
    def tail(dest): a.emit(P['b'](dest - (CAVE + len(a.w)*4)))
    # r26/r31 are live nonvolatile registers in this one FSSA caller.
    emit('lwz', 9, 26, 0x50)
    emit('subf', 9, 9, 31)
    for record in GRID + TABS:
        const(10, record - RECORD_BASE)
        emit('cmplw', 9, 10); a.br('beq', 'measure')
    import battle_unit_name_layout
    battle_unit_name_layout.emit_opt_in(emit,const,a)
    # 0x510cc saves its caller's LR at +0xf0 in its 0xe0-byte frame.
    # The grid's colored entries use an exact 32-byte template copy made at
    # 0xadecc..0xadf10, passed via stack +0x78 at 0xae404. Address-only
    # matching cannot identify it. Check both call provenance and template
    # string reference; do not broaden centering to arbitrary stack records.
    emit('ld', 9, 1, 0xf0)
    const(10, GRID_CALLER)
    emit('cmplw', 9, 10); a.br('bne', 'original')
    emit('lwz', 9, 31, 0)
    for ref in GRID_STRINGS:
        const(10, ref)
        emit('cmplw', 9, 10); a.br('beq', 'measure')
    a.br('b', 'original')
    a.label('measure')
    emit('cmpwi', 7, 1); a.br('bne', 'original')  # CP932 only
    emit('stdu', 1, 1, -0x80)
    emit('mr', 12, 3)
    emit('addi', 10, 0, 0)
    emit('stw', 10, 1, 0x70); emit('lfs', 12, 1, 0x70)  # total pixels
    const(11, eboot.TABLE_VA)
    a.label('loop')
    emit('lbz', 9, 12, 0)
    emit('cmpwi', 9, 0); a.br('beq', 'done')
    emit('addi', 10, 10, 1)
    emit('cmpwi', 10, 256); a.br('bgt', 'fallback')
    emit('cmplwi', 9, 0x81); a.br('blt', 'fallback')
    emit('cmplwi', 9, 0x97); a.br('bgt', 'fallback')
    emit('lbz', 0, 12, 1)
    emit('cmplwi', 0, 0x40); a.br('blt', 'fallback')
    emit('cmplwi', 0, 0xfc); a.br('bgt', 'fallback')
    emit('addi', 9, 9, -0x81); emit('mulli', 9, 9, 192)
    emit('add', 9, 9, 0); emit('addi', 9, 9, -0x40)
    emit('cmplwi', 9, eboot.ATLAS_CELLS); a.br('bge', 'fallback')
    emit('lbzx', 9, 11, 9)
    # Restrict to our narrowed atlas glyphs; original Japanese is untouched.
    emit('cmpwi', 9, 32); a.br('beq', 'fallback')
    emit('std', 9, 1, 0x70); emit('lfd', 13, 1, 0x70)
    emit('fcfid', 13, 13); emit('frsp', 13, 13)
    emit('lwz', 9, 2, -0x7f3c)
    emit('lfs', 0, 9, 0x54)
    emit('lhz', 0, 9, 0xac)
    emit('cmpwi', 0, 0); a.br('beq', 'advance')
    emit('lfs', 0, 9, 0x78)
    emit('lhz', 0, 12, 0)
    # Same category switches as 0x14504..0x1455c in the real drawer.
    for flag, lo, hi in [(0xb1,0x8340,0x8491),(0xae,0x8260,0x8279),
                         (0xb0,0x829f,0x82f1),(0xaf,0x8281,0x829a),
                         (0xb2,0x8140,0x825f)]:
        skip = 'skip_%x' % flag
        emit('cmplwi', 0, lo); a.br('blt', skip)
        emit('cmplwi', 0, hi); a.br('bgt', skip)
        emit('lbz', 0, 9, flag)
        emit('cmpwi', 0, 0); a.br('bne', 'alternate')
        emit('lhz', 0, 12, 0)
        a.label(skip)
    a.br('b', 'advance')
    a.label('alternate'); emit('lfs', 0, 9, 0x88)
    a.label('advance')
    emit('fmuls', 13, 13, 0)
    const(0, 0x3d000000)  # 1/32
    emit('stw', 0, 1, 0x70); emit('lfs', 0, 1, 0x70)
    emit('fmuls', 13, 13, 0)
    emit('fadds', 12, 12, 13)
    emit('addi', 12, 12, 2); a.br('b', 'loop')
    a.label('done')
    const(0, 0x3f000000)  # half the rendered width
    emit('stw', 0, 1, 0x70); emit('lfs', 0, 1, 0x70)
    emit('fmuls', 12, 12, 0); emit('fsubs', 1, 1, 12)
    emit('addi', 1, 1, 0x80)
    tail(0x140f4)  # left-edge draw, with normal translation/color processing
    a.label('fallback'); emit('addi', 1, 1, 0x80)
    a.label('original'); tail(0x14954)
    code = a.code()
    # command_layout starts at 0x78e400; do not consume its reservation.
    assert len(code) <= 0x400
    return code


def apply(elf, segs):
    import eboot
    site, cave = (eboot._off(segs, x) for x in (SITE, CAVE))
    old = 0x48000001 | ((0x14954-SITE) & 0x3fffffc)
    assert struct.unpack_from('>I', elf, site)[0] == old
    code = stub()
    assert not any(elf[cave:cave+len(code)]), 'search cave occupied'
    elf[cave:cave+len(code)] = code
    struct.pack_into('>I', elf, site, 0x48000001 | ((CAVE-SITE)&0x3fffffc))
    return [(site, site+4), (cave, cave+len(code))]


def tabs(blob, mapping):
    import aiddata
    edits = []
    for record, en in zip(TABS, TAB_TEXT):
        off = aiddata.STR_BASE + struct.unpack_from('>I', blob, record)[0]
        jp = blob[off:blob.index(b'\0', off)].decode('cp932')
        assert jp == {'Spirit':'精神コマンド','Skills':'特殊スキル','Abilities':'特殊能力'}[en]
        assert aiddata.refs(blob)[off] == [record]
        edits.append({'off':off, 'en':en})
    new, done, unref = aiddata.repoint(blob, edits, mapping)
    assert not unref
    assert not aiddata.verify_repoint(blob, new, done, mapping)
    return new
