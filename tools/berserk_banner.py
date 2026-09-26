"""Translate EVA's Berserk cut-in word sprites, preserving animation/tint.

EFFPS3 member 307, texture 0: solid lettering at y=8..39, outline at
y=40..79. The other texture rows are a line/wave, not part of the label.
"""
import hashlib
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import localization

MEMBER = 307
GTF = 0x7dd80
SOURCE_HASH = '1885d0c317b381057a4bbe46e572ef251d18324b3138eef8b612da4c8204bdea'
MESSAGE = 'abilities:r_3633df5b7b8f47fa'


def morton(x, y):
    # Rectangular 512x128 swizzle: seven interleaved bits, then x's high bits.
    return sum(((x >> i) & 1) << (2*i) | ((y >> i) & 1) << (2*i+1)
               for i in range(7)) | ((x >> 7) << 14)


def span(blob):
    assert blob[GTF:GTF+4] == b'\x02\x02\0\0'
    assert struct.unpack_from('>I',blob,GTF+8)[0] == 8
    p=GTF+12
    off,size=struct.unpack_from('>II',blob,p+4)
    assert blob[p+12] == 0x85 and size == 512*128*4
    assert struct.unpack_from('>HH',blob,p+20) == (512,128)
    assert GTF+off+size <= len(blob)
    return GTF+off


def audit_source(blob):
    assert hashlib.sha256(blob).hexdigest() == SOURCE_HASH, 'Berserk source changed'
    span(blob)
    for uv,count in (((0,8,512,32),141),((0,40,512,40),141)):
        key=struct.pack('>8H',0,*uv,0x5800,0x0101,0)
        assert blob[:GTF].count(key) == count, 'Berserk animation/UV source changed'


def atlas(blob):
    start=span(blob)
    pixels=b''.join(blob[start+4*morton(x,y):start+4*morton(x,y)+4]
                    for y in range(128) for x in range(512))
    return Image.frombytes('RGBA',(512,128),pixels,'raw','ARGB')


def lettering(font_path):
    label=localization.message(MESSAGE).upper()
    assert label and label.isascii()
    face=ImageFont.truetype(font_path,120)
    l,t,r,b=face.getbbox(label)
    mask=Image.new('L',(r-l,b-t))
    ImageDraw.Draw(mask).text((-l,-t),label,font=face,fill=255)
    width=round(mask.width/mask.height*30)
    assert width <= 480, 'Berserk label exceeds sprite width'
    mask=mask.resize((width,30),Image.Resampling.LANCZOS)
    solid=Image.new('L',(512,32));solid.paste(mask,((512-width)//2,1))
    outline=Image.new('L',(512,40));outline.paste(mask,((512-width)//2,5))
    outline=ImageChops.subtract(outline.filter(ImageFilter.MaxFilter(3)),
                               outline.filter(ImageFilter.MinFilter(3)))
    tile=Image.new('RGBA',(512,72),(255,255,255,0))
    alpha=Image.new('L',tile.size);alpha.paste(solid,(0,0));alpha.paste(outline,(0,32))
    tile.putalpha(alpha)
    # Match the source's transparent-black background, including hidden RGB.
    return Image.alpha_composite(Image.new('RGBA',tile.size),tile)


def apply(blob,font_path):
    audit_source(blob)
    tile=lettering(font_path);out=bytearray(blob);start=span(blob)
    for y in range(72):
        for x in range(512):
            r,g,b,a=tile.getpixel((x,y));p=start+4*morton(x,y+8)
            out[p:p+4]=bytes((a,r,g,b))
    return bytes(out)


def verify(original,built,font_path):
    audit_source(original)
    assert len(original)==len(built) and original!=built
    assert atlas(built).crop((0,8,512,80)).tobytes()==lettering(font_path).tobytes()
    a=bytearray(original);b=bytearray(built);start=span(original)
    for y in range(8,80):
        for x in range(512):
            p=start+4*morton(x,y);a[p:p+4]=b[p:p+4]=bytes(4)
    assert a==b, 'Berserk change outside lettering pixels'
    print('PASS: Berserk solid/outline lettering; cut-in, UVs, tint, wave and other textures unchanged.')
