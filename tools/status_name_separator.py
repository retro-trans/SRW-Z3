"""Pilot Info full-name join: replace the native middle dot with a VWF space.

At 0x31b978 the western-order path copies pilot-nw col2, appends CP932
0x8145, then joins col1 at 0x31c2a0 before drawing field14 at 0x31ba10.
Only those two separator-byte immediates change. The surname-first branch,
player/save name builders, string lengths, buffers and unrelated dots stay put.
"""
import struct
import digraph
import eboot

START = 0x31b99c
SOURCE = bytes.fromhex(
    '3800ff81 8082e618 7c63da14 39200045 78630020 9ba30002 98030000 99230001')
SITES = (0x31b99c, 0x31b9a8)


def expected(mapping):
    separator = digraph.encode_mixed(' ', mapping)
    assert len(separator) == 2, 'Pilot separator requires one VWF cell'
    result = bytearray(SOURCE)
    struct.pack_into('>I', result, 0, 0x38000000 | separator[0])
    struct.pack_into('>I', result, 12, 0x39200000 | separator[1])
    return bytes(result)


def patch(blob, mapping):
    segs = eboot._segments(blob)
    off = eboot._off(segs, START)
    assert blob[off:off+len(SOURCE)] == SOURCE, 'Pilot full-name join source drift'
    out = bytearray(blob)
    out[off:off+len(SOURCE)] = expected(mapping)
    check(out, mapping)
    return bytes(out)


def check(blob, mapping):
    off = eboot._off(eboot._segments(blob), START)
    assert blob[off:off+len(SOURCE)] == expected(mapping), 'Pilot separator mismatch'
