"""Five title-screen Library labels; preserve all UVs and animation states."""
import localization as _l10n
import hashlib
import re
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import title_footer as footer

TEXTURE=5
SIZE=(720,512)
# Actual animation sample rectangles, not guessed text bounding boxes.
# x, y, width, height, English, number of references in the animation.
ROWS=(
    (3,269,269,60,_l10n.literal('title_library_buttons.ROWS/0'),468),
    (1,204,307,55,_l10n.literal('title_library_buttons.ROWS/1'),463),
    (1,137,167,57,_l10n.literal('title_library_buttons.ROWS/2'),459),
    (1,74,301,53,_l10n.literal('title_library_buttons.ROWS/3'),455),
    (3,8,297,58,_l10n.literal('title_library_buttons.ROWS/4'),447),
)
FONT=Path('C:/Windows/Fonts/timesbd.ttf')

def span(blob):
    p=footer.GTF+12+TEXTURE*36
    assert blob[p+12]==0xa5
    assert struct.unpack_from('>HH',blob,p+20)==SIZE
    offset,size=struct.unpack_from('>II',blob,p+4)
    assert size==SIZE[0]*SIZE[1]*4 and footer.GTF+offset+size<=len(blob)
    return footer.GTF+offset

def atlas(blob):
    offset=span(blob)
    return Image.frombytes('RGBA',SIZE,blob[offset:offset+SIZE[0]*SIZE[1]*4],'raw','ARGB')

def tile(row,font=FONT):
    x,y,w,h,text,_=row
    face=ImageFont.truetype(str(font),42*4)
    l,t,r,b=face.getbbox(text)
    ink=Image.new('RGBA',(r-l,b-t));ImageDraw.Draw(ink).text((-l,-t),text,font=face,fill='white')
    width=min(w-16,round(ink.width/4));height=min(h-16,round(ink.height/4))
    ink=ink.resize((width,height),Image.Resampling.LANCZOS)
    result=Image.new('RGBA',(w,h),(255,255,255,0))
    result.alpha_composite(ink,((w-width)//2,(h-height)//2))
    box=result.getchannel('A').getbbox()
    assert box and box[0]>=7 and box[2]<=w-7 and box[1]>=7 and box[3]<=h-7
    assert abs((box[0]+box[2])/2-w/2)<=1
    glow=Image.new('RGBA',(w,h),(182,182,182,0))
    glow.putalpha(result.getchannel('A').filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(5)).point(lambda a:round(a*176/255)))
    glow.alpha_composite(result)
    return glow

def audit(original):
    assert hashlib.sha256(original).hexdigest()==footer.SOURCE_SHA256
    span(original)
    for x,y,w,h,en,count in ROWS:
        pattern=struct.pack('>6H',0,x,y,w,h,0x5000)+b'\x01\x01\0\x05'
        assert len(list(re.finditer(re.escape(pattern),original[:footer.GTF])))==count,en

def apply(original,font_path,version=None,menu_font=FONT):
    audit(original)
    base=footer.apply(original,font_path,version) if version is not None else original
    out=bytearray(base);offset=span(base)
    for row in ROWS:
        x,y,w,h,_,_=row;im=tile(row,menu_font)
        r,g,b,a=im.split();pixels=Image.merge('RGBA',(a,r,g,b)).tobytes()
        for yy in range(h):
            p=offset+((y+yy)*SIZE[0]+x)*4
            out[p:p+w*4]=pixels[yy*w*4:(yy+1)*w*4]
    return bytes(out)

def verify(original,built,font_path,version=None,menu_font=FONT):
    assert built==apply(original,font_path,version,menu_font)
    restored=bytearray(built);offset=span(original)
    for x,y,w,h,_,_ in ROWS:
        for yy in range(y,y+h):
            p=offset+(yy*SIZE[0]+x)*4
            restored[p:p+w*4]=original[p:p+w*4]
    if version is not None:footer.verify(original,bytes(restored),font_path,version)
    else:assert bytes(restored)==original
    print('PASS: all five title Library labels; 2292 animation samples unchanged; footer and all other title artwork preserved.')
