"""Public #24: ALL Attack heading, AID member 1 texture 2.

Only the two 80x40 word cells are replaced. The game supplies the yellow
tint and shadow; keep the atlas white like the original word sprites.
"""
import struct
from PIL import Image, ImageDraw, ImageFont

def span(blob):
    p = 12 + 2*36
    assert struct.unpack_from('>I', blob, 8)[0] == 4
    assert blob[p+12] == 0x85
    assert struct.unpack_from('>HH', blob, p+20) == (512, 512)
    return struct.unpack_from('>I', blob, p+4)[0]

def morton(x, y):
    return sum(((x>>i)&1)<<(2*i) | ((y>>i)&1)<<(2*i+1) for i in range(9))

def apply(blob, font_path):
    start = span(blob)
    result = bytearray(blob)
    font = ImageFont.truetype(font_path, 30*4)
    for cell, text in enumerate(('ALL', 'Attack')):
        l,t,r,b = font.getbbox(text)
        ink = Image.new('RGBA', (r-l,b-t))
        ImageDraw.Draw(ink).text((-l,-t), text, font=font, fill='white')
        ink = ink.resize((min(70,round(ink.width/4)), 29), Image.Resampling.LANCZOS)
        tile = Image.new('RGBA',(80,40))
        tile.alpha_composite(ink, ((80-ink.width)//2,4))
        for y in range(40):
            for x in range(80):
                r,g,b,a = tile.getpixel((x,y))
                p = start + 4*morton(cell*80+x,y)
                result[p:p+4] = bytes((a,r,g,b))
    return bytes(result)

def verify(original, built, font_path):
    assert built == apply(original, font_path), 'ALL Attack sprite mismatch'
    assert original != built
    start = span(original)
    allowed = {start+4*morton(x,y)+c for x in range(160) for y in range(40) for c in range(4)}
    assert all(i in allowed for i,(a,b) in enumerate(zip(original,built)) if a!=b)
    assert len(original)==len(built)
