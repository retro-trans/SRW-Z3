"""Numbered operation conditions: draw continuation lines without the indent.

When a stage has several victory/defeat conditions, the game numbers them from
a four-entry table (EBOOT pointers at 0x7c8594: １． ２． ３． and 　　) and
draws EACH LINE separately: "１．" + line 1, then "　　" + every further line,
so the Japanese wraps under its text rather than its number.

The draw hook matches whole strings. Line 1 ("１．..." ) has a key; the
indented continuation ("　　...") never did, so the second line of every
numbered multi-line condition stayed Japanese -- Episode 25's
"ダグザとカミーユをパラオのポイントに到達させる。" under an English line 1.
Hooking the indented forms would cost ~10 KB of the nearly full hook extension.

Instead the indent string becomes empty. Continuation lines are then drawn as
the plain line, which mission_conditions.line_hooks and the generic line pairs
already translate. The English continuation starts under "1." rather than
under the text after it; nothing else changes. Only this table references the
string, and both it and the pointer are verified before anything is written.
"""
import struct
import eboot

INDENT_VA = 0x6fa2a8          # '　　' (file offset 0x6ea2a8 in the plain ELF)
TABLE_VA = 0x7d8594           # the four pointers: １． ２． ３．
INDENT = '　　'.encode('cp932') + b'\0'


def _offsets(b):
    segs = eboot._segments(b)
    return eboot._off(segs, INDENT_VA), eboot._off(segs, TABLE_VA)


def apply(b):
    b = bytearray(b)
    off, table = _offsets(b)
    assert b[off:off + len(INDENT)] == INDENT, 'operation indent moved'
    assert struct.unpack_from('>4I', b, table)[3] == INDENT_VA, 'operation number table moved'
    b[off:off + len(INDENT) - 1] = bytes(len(INDENT) - 1)
    return b


def check(b):
    off, table = _offsets(b)
    assert struct.unpack_from('>4I', b, table)[3] == INDENT_VA
    assert b[off:off + len(INDENT)] == bytes(len(INDENT))
    numbers = [struct.unpack_from('>I', b, table + 4 * i)[0] for i in range(3)]
    segs = eboot._segments(b)
    for i, va in enumerate(numbers):
        o = eboot._off(segs, va)
        assert b[o:o + 5] == '１２３'[i].encode('cp932') + '．'.encode('cp932') + b'\0'
    print('PASS: numbered operation conditions draw continuation lines unindented '
          '(existing line hooks apply); number prefixes unchanged.')
