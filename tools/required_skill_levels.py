"""Exact hooks for the composed weapon required-skill level family.

The existing Newtype L hook matches the prefix alone, not the runtime string
after the fullwidth digit is appended. Retain the native composer and level;
derive all ten complete labels from the canonical prefix instead.
"""
from pathlib import Path
import struct
import localization

PREFIX = 'ニュータイプＬ'
MESSAGE = 'ui_hook:r_c6e2e5a0cf999610'


def hooks():
    english = localization.english().text(MESSAGE)
    return {PREFIX + chr(0xff10 + n): english + str(n) for n in range(10)}


def check_source(source):
    raw = PREFIX.encode('cp932') + b'\0'
    assert source[0x7106a8:0x7106a8 + len(raw)] == raw
    assert struct.unpack_from('>I', source, 0x7cbd84)[0] == 0x7206a8
    assert source[0x305f74:0x305f78] == bytes.fromhex('83c2e464')
    for n in range(10):
        off = 0x7106f8 + 8 * n
        assert source[off:off + 3] == chr(0xff10 + n).encode('cp932') + b'\0'


def check(entries, mapping):
    import eboot
    check_source(Path('work/EBOOT_dec.elf').read_bytes())
    for jp, en in hooks().items():
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
    print('PASS: all ten composed Newtype required-skill levels hooked exactly; native values unchanged.')
