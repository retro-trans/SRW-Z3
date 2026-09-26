"""Source-bound activation dialogs and dynamic skill-learning confirmations.

Activation text is UTF-8 and is not seen by the CP932 content hook. The
training screen composes names at runtime, then uses compiler-unrolled
fixed-length copies for the suffixes. Repointing only those strings would
truncate English. Six verified copy blocks are replaced by NUL-copy loops;
the names, levels, decisions, and both 256-byte caller buffers are unchanged.
"""
import struct
from pathlib import Path
import localization
import digraph as dg

GROUP = 'activation_prompts'
# Original copy-block VAs, byte counts (including NUL), and canonical suffix.
COPY_BLOCKS = (
    (0x31ddb8, 15, 'skill_upgrade'),
    (0x31dec4, 27, 'skill_plus'),
    (0x31dffc, 27, 'skill_plus'),
    (0x31e118, 31, 'skill_overwrite'),
    (0x31e39c, 23, 'skill_new'),
    (0x31e498, 23, 'skill_new'),
)


def rows():
    import terms
    cat = localization.english()
    index = terms.index(cat.legacy('analysis/glossary.json'))
    definitions = cat.document('localization/messages/%s.json' % GROUP)['messages']
    return [(mid.split(':', 1)[1], d, terms.expand(cat.text(mid), index, GROUP))
            for mid, d in definitions.items()]


def activation_labels():
    return tuple(dict.fromkeys(en for key, _, en in rows() if not key.startswith('skill_')))


def source_inventory(elf):
    # Exactly the whole adjacent activation-dialog family; the empty word at
    # 0x78027c separates the GAI and Tengen Toppa pointer arrays.
    strings = [s.decode('utf8') for s in elf[0x6d4fe8:0x6d53c0].split(b'\0') if s]
    expected = [d['source'] for key, d, _ in rows() if not key.startswith('skill_')]
    assert strings == expected and len(strings) == 17, 'Activation source family changed'
    expected_pointers = {int(p, 16) for key, d, _ in rows()
                         if not key.startswith('skill_') for p in d['context']['pointer_offsets']}
    assert expected_pointers == set(range(0x780240, 0x78028c, 4)) - {0x78027c}
    for _, d, _ in rows():
        off = int(d['context']['eboot_offset'], 16)
        raw = d['source'].encode(d['context']['encoding']) + b'\0'
        assert elf[off:off + len(raw)] == raw, (hex(off), d['source'])
        for pointer in d['context']['pointer_offsets']:
            assert struct.unpack_from('>I', elf, int(pointer, 16))[0] == off + 0x10000
    # The only caller gives the composer two separate 0x100-byte buffers.
    assert elf[0x30eabc:0x30ead4] == bytes.fromhex(
        '380100a0392101a0781f0020793e00207fe3fb787fc4f378')
    return strings


def original_copy(count):
    """Exact compiler scheduling, checked byte-for-byte before changing code."""
    import eboot
    p = eboot._ppc()
    words = []
    # Four-byte groups; the fifth group schedules its offset-16 load last.
    for start in range(0, count - 3, 4):
        offsets = [start + i for i in range(4)]
        order = [1, 2, 3, 0] if start == 16 else [0, 1, 2, 3]
        regs = [0, 11, 10, 8]
        words += [p['lbz'](regs[i], 9, offsets[i]) for i in order]
        words += [p['stb'](regs[i], 3, offsets[i]) for i in range(4)]
    start = count - 3
    words += [p['lbz'](reg, 9, off) for reg, off in [(0, start + 2), (11, start), (10, start + 1)]]
    words += [p['stb'](reg, 3, off) for reg, off in [(0, start + 2), (11, start), (10, start + 1)]]
    return b''.join(struct.pack('>I', w) for w in words)


def copy_loop():
    """Uses only r0/r8/r11 from the original scratch set; keeps r3/r9/LR."""
    import eboot
    p, a = eboot._ppc(), eboot._Asm()
    a.emit(p['addi'](8, 0, 0))
    a.label('copy')
    a.emit(p['lbzx'](0, 9, 8))
    a.emit(p['add'](11, 3, 8))
    a.emit(p['stb'](0, 11, 0))
    a.emit(p['addi'](8, 8, 1))
    a.emit(p['cmpwi'](0, 0))
    a.br('bne', 'copy')
    return a.code()


def encoded(key, en, mapping):
    import command_layout, eboot
    if key.startswith('skill_'):
        return dg.encode_mixed(en, mapping) + b'\0'
    return (command_layout.prefix(en) + ''.join(chr(eboot.VWF_CP_BASE + ord(c)) for c in en)).encode('utf8') + b'\0'


def patch(elf, mapping, cursor):
    import eboot
    # The source strings are never changed by any earlier translation step.
    source_inventory(elf)
    check_buffer_budget(mapping)
    out = bytearray(elf)
    segs = eboot._segments(out)
    allowed = set()
    start = cursor
    limit = eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE
    shared = {}
    for key, d, en in rows():
        raw = encoded(key, en, mapping)
        if raw not in shared:
            assert cursor + len(raw) <= limit, 'Activation prompts exceed unchanged EXT'
            assert not any(out[cursor:cursor + len(raw)]), 'Activation prompt allocation is occupied'
            out[cursor:cursor + len(raw)] = raw
            shared[raw] = eboot._va(segs, cursor)
            cursor = (cursor + len(raw) + 3) & ~3
        for pointer in d['context']['pointer_offsets']:
            off = int(pointer, 16)
            struct.pack_into('>I', out, off, shared[raw])
            allowed.update(range(off, off + 4))
    loop = copy_loop()
    for va, count, _ in COPY_BLOCKS:
        off = eboot._off(segs, va)
        expected = original_copy(count)
        assert out[off:off + len(expected)] == expected, ('Skill suffix copy changed', hex(va))
        out[off:off + len(expected)] = loop + bytes.fromhex('60000000') * ((len(expected) - len(loop)) // 4)
        allowed.update(range(off, off + len(expected)))
    allowed.update(range(start, cursor))
    assert len(out) == len(elf) and all(a == b or i in allowed for i, (a, b) in enumerate(zip(elf, out)))
    return bytes(out), cursor


def check_buffer_budget(mapping):
    cat = localization.english()
    glossary = {t['jp']: t['en'] for t in cat.legacy('analysis/glossary.json')['terms'] if t['en']}
    skill_names = []
    for mid, definition in cat.document('localization/messages/skills.json')['messages'].items():
        skill_names.append(glossary.get(definition['source'], cat.text(mid)))
    for name in skill_names:
        for key, _, en in rows():
            if key.startswith('skill_'):
                # Include native level/+level formatting and both quote cells.
                line = '「' + name + 'Ｌ９＋９' + en
                assert len(dg.encode_mixed(line, mapping)) + 1 <= 256, (key, name)
    return skill_names


def check(elf, mapping, widths):
    import eboot
    from intermission_layout import ink
    source = Path('work/EBOOT_dec.elf').read_bytes()
    source_inventory(source)
    segs = eboot._segments(elf)
    for key, d, en in rows():
        raw = encoded(key, en, mapping)
        for pointer in d['context']['pointer_offsets']:
            target = struct.unpack_from('>I', elf, int(pointer, 16))[0]
            off = eboot._off(segs, target)
            assert elf[off:off + len(raw)] == raw, key
        original = int(d['context']['eboot_offset'], 16)
        size = len(d['source'].encode(d['context']['encoding'])) + 1
        assert elf[original:original + size] == source[original:original + size]
        if not key.startswith('skill_'):
            assert ink(en, mapping, widths, 31) <= 1080, (key, en)
    for va, count, _ in COPY_BLOCKS:
        off = eboot._off(segs, va)
        raw = copy_loop() + bytes.fromhex('60000000') * ((len(original_copy(count)) - len(copy_loop())) // 4)
        assert elf[off:off + len(raw)] == raw, hex(va)
    for name in check_buffer_budget(mapping):
        for key, _, en in rows():
            if key.startswith('skill_'):
                assert ink(name + ' L9+9' + en.replace('」', ''), mapping, widths, 31) + 32 <= 1080, (key, name)
    print('PASS: 17 activation lines / 18 pointers; 4 dynamic skill suffixes / 6 NUL-copy sites; widths and 256-byte buffers.')
