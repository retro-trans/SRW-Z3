"""Build-number footer on the game's press-any-button title screen.

LUACPK member 1 defines ScAnime_Z3TITLE = 295; EFF member 0 is shared,
so the animation lives in member 296. Its texture 0 is the stationary
1280x720 title background. Textures 3/4 are the subsequent menu backgrounds.
Only texture 0's bottom-right rectangle changes: no animation commands,
logo, prompt, other menu, or external bitmap is replaced.
"""
import hashlib
import struct

from PIL import Image, ImageDraw, ImageFont

from build_version import version_key

MEMBER = 296
GTF = 0x1FE290
SOURCE_SHA256 = 'dec8e258f43dc5ba892a2ceab84e0a6777a387e5bc7b57c48ed8fb98da4c9e7e'
URL = 'github.com/retro-trans'
SIZE = (1280, 720)
# 28 pixels from the right edge, 24 from the bottom; below the prompt.
BOX = (912, 640, 1252, 696)
FONT_SIZE = 18


def texture_span(blob):
    assert blob[GTF:GTF+4] == b'\x02\x02\0\0', 'unexpected title texture header'
    assert struct.unpack_from('>I', blob, GTF+8)[0] == 7
    offset, size = struct.unpack_from('>II', blob, GTF+16)
    assert blob[GTF+24] == 0xa5, 'title must use linear ARGB32'
    assert struct.unpack_from('>HH', blob, GTF+32) == SIZE
    assert size == SIZE[0]*SIZE[1]*4 and GTF+offset+size <= len(blob)
    return GTF+offset, size


def overlay(font_path, version):
    """Native build-time text, independent of the game's shared font mapping."""
    version_key(version)
    scale = 4
    width, height = BOX[2]-BOX[0], BOX[3]-BOX[1]
    canvas = Image.new('RGBA', (width*scale, height*scale))
    font = ImageFont.truetype(str(font_path), FONT_SIZE*scale)
    for text, bottom in (('v'+version, 26), (URL, height)):
        l,t,r,b = font.getbbox(text, stroke_width=scale)
        assert r-l < width*scale-4*scale, 'title footer would overflow'
        assert b-t <= 24*scale, 'title footer line would overlap'
        ink = Image.new('RGBA', (r-l,b-t))
        ImageDraw.Draw(ink).text((-l,-t), text, font=font,
                                fill=(240,246,255,255), stroke_width=scale,
                                stroke_fill=(5,12,32,240))
        canvas.alpha_composite(ink, (width*scale-ink.width, bottom*scale-ink.height))
    return canvas.resize((width,height), Image.Resampling.LANCZOS)


def background(blob):
    offset,size = texture_span(blob)
    return Image.frombytes('RGBA', SIZE, blob[offset:offset+size], 'raw','ARGB')


def apply(blob, font_path, version):
    assert hashlib.sha256(blob).hexdigest() == SOURCE_SHA256, 'unexpected title animation source'
    offset,_ = texture_span(blob)
    x0,y0,x1,y1 = BOX
    tile = background(blob).crop(BOX)
    tile.alpha_composite(overlay(font_path, version))
    r,g,b,a = tile.split()
    pixels = Image.merge('RGBA', (a,r,g,b)).tobytes()
    result = bytearray(blob)
    stride = (x1-x0)*4
    for row in range(y1-y0):
        p = offset + ((y0+row)*SIZE[0]+x0)*4
        result[p:p+stride] = pixels[row*stride:(row+1)*stride]
    return bytes(result)


def verify(original, built, font_path, version):
    assert built == apply(original, font_path, version), 'missing or wrong-version title footer'
    assert built != original and len(built) == len(original)
    offset,_ = texture_span(original)
    x0,y0,x1,y1 = BOX
    restored = bytearray(built)
    for row in range(y0,y1):
        p = offset + (row*SIZE[0]+x0)*4
        restored[p:p+(x1-x0)*4] = original[p:p+(x1-x0)*4]
    assert restored == original, 'title art outside footer or animation commands changed'
    print('PASS: title footer v%s / %s; only bottom-right title pixels changed.' % (version, URL))
