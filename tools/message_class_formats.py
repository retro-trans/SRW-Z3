"""Translate shared reward format strings; preserve inserted names/items."""
import localization as _l10n
import digraph as dg

FORMATS = {
    0x6e4f88: ('%sのエースボーナスの効果で', _l10n.literal('message_class_formats.FORMATS/0')),
    0x6e4fa8: ('強化パーツ『%s』を', _l10n.literal('message_class_formats.FORMATS/1')),
}

def encoded(jp, en, mapping):
    assert jp.count('%s') == en.count('%s') == 1
    left, right = en.split('%s')
    raw = dg.encode_mixed(left, mapping) + b'%s' + dg.encode_mixed(right, mapping) + b'\0'
    capacity = len(jp.encode('cp932')) + 1
    assert len(raw) <= capacity, (en, len(raw), capacity)
    return raw + bytes(capacity-len(raw))

def patch(elf, mapping):
    out = bytearray(elf)
    for off, (jp, en) in FORMATS.items():
        original = jp.encode('cp932') + b'\0'
        assert out[off:off+len(original)] == original
        out[off:off+len(original)] = encoded(jp, en, mapping)
    assert len(out) == len(elf)
    return out

def check(elf, mapping):
    for off, (jp, en) in FORMATS.items():
        raw = encoded(jp, en, mapping)
        assert elf[off:off+len(raw)] == raw
        assert raw.count(b'%s') == 1
        for value in ('Hibiki', 'Repair Kit', 'Custom Name'):
            value = dg.encode_mixed(value, mapping)
            result = raw.split(b'\0')[0] % value
            assert value in result
    print('PASS: Ace Bonus and item-reward templates retain runtime values and ASCII format specifiers.')
