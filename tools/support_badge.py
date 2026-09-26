"""Public issue #23: the map's remaining Support Attack uses badge.

TPACK member 2, texture 1 contains four 80x80 tiles (uses 1..4).
This is NOT a generic attack/defense selector: 2e4a6c calls 2f3ca0
(pilot +0x50, skill 1), then 2e43e8 forwards that count to 329e34.
32a41c binds texture 1 and draws row count-1. Defense uses the separate
2f3cac getter (+0x51, skill 4); it never feeds this map badge. Hence AT
here, not DF, and no changes to counters, skill names or gameplay code.
"""
import struct

from PIL import Image, ImageDraw, ImageFont

MEMBER = 2
TEXTURE = 1
WIDTH, HEIGHT = 80, 320
LABEL_BOX = (37, 2, 77, 24)


def texture_span(blob):
    assert blob[:4] == b'\x02\x02\0\0'
    assert struct.unpack_from('>I', blob, 8)[0] == 8
    descriptor = 12 + TEXTURE * 36
    offset, size = struct.unpack_from('>II', blob, descriptor + 4)
    assert blob[descriptor + 12] == 0xa5, 'expected linear ARGB32'
    assert struct.unpack_from('>HH', blob, descriptor + 20) == (WIDTH, HEIGHT)
    assert size == WIDTH * HEIGHT * 4 and offset + size <= len(blob)
    return offset, size


def label(font_path):
    # Match the original 22px-high, yellow/black outlined label, with AA.
    ss = 4
    font = ImageFont.truetype(font_path, 24 * ss)
    l, t, r, b = font.getbbox('AT', stroke_width=ss)
    ink = Image.new('RGBA', (r-l, b-t))
    ImageDraw.Draw(ink).text((-l, -t), 'AT', font=font,
                            fill=(255, 255, 128, 255),
                            stroke_width=ss, stroke_fill=(0, 0, 0, 255))
    ink = ink.resize((round(ink.width/ss), round(ink.height/ss)), Image.Resampling.LANCZOS)
    assert ink.width <= 40 and ink.height <= 22
    result = Image.new('RGBA', (40, 22))
    result.alpha_composite(ink, ((40-ink.width)//2, (22-ink.height)//2))
    return result


def apply(blob, font_path):
    offset, size = texture_span(blob)
    result = bytearray(blob)
    r, g, b, a = label(font_path).split()
    ink = Image.merge('RGBA', (a, r, g, b)).tobytes()
    # Replace only label pixels. Copying the whole page through an image
    # decoder could change invisible RGB bytes or the existing numeral art.
    x0, y0, x1, y1 = LABEL_BOX
    for tile in range(4):
        for y in range(y1-y0):
            p = offset + ((tile*80+y0+y)*WIDTH+x0)*4
            result[p:p+(x1-x0)*4] = ink[y*40*4:(y+1)*40*4]
    return bytes(result)


def verify(original, built, font_path):
    expected = apply(original, font_path)
    assert built == expected, 'support badge differs from the AT-only pixel patch'
    offset, size = texture_span(original)
    for tile in range(4):
        p = offset + (tile*80+24)*WIDTH*4
        end = offset + (tile+1)*80*WIDTH*4
        assert original[p:end] == built[p:end], 'remaining-use numeral changed'
    assert built[:offset] == original[:offset]
    assert built[offset+size:] == original[offset+size:]
    assert built != original, 'Japanese badge was not replaced'


def verify_attack_reader(elf):
    """Fail if a different runtime changes the type that uses these tiles."""
    import eboot
    segs = eboot._segments(elf)
    # Attack counter getter, separate defense getter, and attack skill init.
    expected = {
        0x2f3ca0: (0x81230004, 0x88690050, 0x4e800020),
        0x2f3cac: (0x81230004, 0x88690051, 0x4e800020),
        0x2f3dec: (0x38800001,),  # skill 1 = Support Attack (RPW sk-pri)
        0x2f3dfc: (0x987d0050,),
        0x2e4a6c: (0x48000001 | ((0x2f3ca0-0x2e4a6c) & 0x3fffffc),),
        0x2e4a74: (0xb07f0002,),  # preserve the count in per-unit draw state
        0x2e43d8: (0xa07d0002,),
        0x2e43e8: (0x48000001 | ((0x329e34-0x2e43e8) & 0x3fffffc),),
        0x329e34: (0x8122e834, 0x90690000, 0x4e800020),
        0x32a41c: (0x38800001,),  # only this branch selects texture 1
        0x32a43c: (0x811f0000,),
        0x32a448: (0x3908ffff,),  # row = count - 1, zero still suppressed
    }
    for va, words in expected.items():
        off = eboot._off(segs, va)
        assert elf[off:off+4*len(words)] == struct.pack('>'+'I'*len(words), *words), hex(va)
