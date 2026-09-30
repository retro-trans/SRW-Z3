"""Shared centered unit-name templates, including battle-preview variants.

Names are already translated in RPW. Native centering nevertheless counts
fixed cells: the reported 24-character EVA name reserves 600px at size25,
but the shipped English glyphs advance306.25px. Center by rendered advance.
References identify templates even when a caller copies/recolors the record.
"""
import struct
from intermission_layout import text

# FSSA member0 record -> string reference, original eight font/style bytes.
TEMPLATES={
    0x9d3d4:(0x4868,'3a3a1a1c1c1c0140'),
    0x9d414:(0x48a8,'ffff171919190240'),
    0x9d494:(0x4928,'3232151715170460'),
    0x9d794:(0x4b3e,'2827171919192240'),
    0x9d7b4:(0x4b5e,'2827171919191240'),
    0x9d7d4:(0x4b7e,'2827171919193240'),
    0x9d7f4:(0x4b9e,'2827171919194240'),
    0x9d814:(0x4bbe,'1717151717172440'),
    0x9d834:(0x4bde,'1717151717171440'),
    0x9d854:(0x4bfe,'1717151717173440'),
    0x9d874:(0x4c1e,'1717151717174440'),
    0xae174:(0xc916,'ffff171919195240'),
    0xb6754:(0x122b2,'3a3a1a1c1c1c0140'),
    0xb67d4:(0x122f4,'3a3a1a1c1c1c0140'),
    0xb6914:(0x124a6,'3a3a1a1c1c1c0140'),
    0xb92d4:(0x146e8,'3a3a1a1c1c1c0140'),
    0xba0b4:(0x14ef4,'ffff171919190240'),
}


def check_ui(blob):
    for row,(reference,style) in TEMPLATES.items():
        assert struct.unpack_from('>I',blob,row)[0]==reference,hex(row)
        assert blob[row+16:row+24]==bytes.fromhex(style),hex(row)
        assert text(blob,row)=='ニルヴァーシュｔｙｐｅＺＥＲＯ'.encode('cp932'),hex(row)


def emit_opt_in(emit,const,assembler):
    # 0x513d4 is specifically FSSA's centered-string path; r31 is a valid
    # 32-byte text record. Source references are unique to these name templates.
    emit('lwz',9,31,0)
    for reference,_ in TEMPLATES.values():
        const(10,reference)
        emit('cmplw',9,10);assembler.br('beq','measure')
