"""Measured centering for the Spirit selection card's pilot-name widget.

The screenshot's Commander Tanaka is 16 translated cells. Native fixed-cell
centering at 25px starts at x=-32.5 despite the card center being x=167.5.
Use the existing guarded VWF center drawer; preserve the full canonical name.
"""
import struct
from intermission_layout import text

ROW = 0xb9914
REFERENCE = 0x14bf2
STYLE = bytes.fromhex('1919171918190240')


def check_ui(blob):
    assert struct.unpack_from('>I', blob, ROW)[0] == REFERENCE
    assert blob[ROW+16:ROW+24] == STYLE
    assert text(blob, ROW) == 'ビッグボルフォッグ'.encode('cp932')


def emit_opt_in(emit, const, assembler):
    emit('lwz', 9, 31, 0)
    const(10, REFERENCE)
    emit('cmplw', 9, 10)
    assembler.br('beq', 'measure')
