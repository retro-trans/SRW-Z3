"""Two native startup heading sprites, separate from the text-widget hook.

P8 indices are Morton-ordered (Y in even bits) in the verified square Vita
atlas. Only the two observed word cells change; palettes and UVs survive.
"""
import hashlib
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from category_port import require
from title_art import nearest_palette

ARCHIVE='DATA/AIDDATA/AIDDataPack.cpk'
MEMBER=1
FONT=Path('C:/Windows/Fonts/arialbd.ttf')
SOURCE_SHA256='d33206f0bf10b45e88ee1b87a58f575241ac9c8e0dca1b4db12e5bf809db360b'
ROWS=((304,384,208,48,'ui_aiddata:protagonist_setup_heading'),
      (272,432,240,40,'ui_aiddata:scenario_select_heading'))
SPREAD=tuple(sum(((x>>i)&1)<<(2*i) for i in range(9)) for x in range(512))


def pixel(x,y):
    return SPREAD[y] | (SPREAD[x]<<1)


def layout(data):
    require(hashlib.sha256(data).hexdigest()==SOURCE_SHA256,'Startup atlas source changed')
    require(data[:8]==b'GXT\0\x03\0\0\x10','Wrong startup GXT')
    require(struct.unpack_from('<5I',data,8)==(4,192,1052672,0,4),'Wrong startup atlas layout')
    for i in range(4):
        require(struct.unpack_from('<6IHHI',data,32+i*32)==
                (192+i*262144,262144,0,0,0,0x95000000,512,512,1),'Wrong startup texture')
    require(len(data)==1052864,'Wrong startup atlas length')
    return 192+2*262144,192+4*262144+2*1024


def image(data):
    # Also accepts a patched preview. Metadata and palette are preserved by apply.
    start=192+2*262144;pal=192+4*262144+2*1024
    im=Image.frombytes('P',(512,512),bytes(data[start+pixel(x,y)] for y in range(512) for x in range(512)))
    im.putpalette(data[pal:pal+1024],rawmode='RGBA')
    return im.convert('RGBA')


def tile(text,w,h,font_path=FONT):
    font=ImageFont.truetype(str(font_path),30*4)
    l,t,r,b=font.getbbox(text)
    require(r>l and b>t,'Empty startup heading')
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),text,font=font,fill='white')
    scale=min(.25,(w-8)/ink.width,(h-8)/ink.height)
    ink=ink.resize((max(1,round(ink.width*scale)),max(1,round(ink.height*scale))),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(w,h));out.alpha_composite(ink,((w-ink.width)//2,(h-ink.height)//2))
    return out


def apply(data,catalog):
    start,pal=layout(data);out=bytearray(data);allowed=set();rows=[]
    palette=tuple(tuple(data[p:p+4]) for p in range(pal,pal+1024,4))
    match=nearest_palette(palette)
    for x,y,w,h,mid in ROWS:
        text=catalog.text(mid);ink=tile(text,w,h)
        for yy in range(h):
            for xx in range(w):
                p=start+pixel(x+xx,y+yy);allowed.add(p)
                out[p]=match(ink.getpixel((xx,yy)))
        rows.append(dict(message=mid,text=text,rectangle=[x,y,w,h]))
    require(all(a==b or i in allowed for i,(a,b) in enumerate(zip(data,out))),
            'Startup atlas changed outside headings')
    require(bytes(out)!=data and len(out)==len(data),'No startup art change')
    return bytes(out),dict(status='native_heading_candidate',rows=rows,
        source_sha256=SOURCE_SHA256,sha256=hashlib.sha256(out).hexdigest(),
        palette_uv_background_preserved=True,runtime_tested=False)


def prepare(port):
    cpk=port.cpk(ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==MEMBER))
    changed,audit=apply(raw,port.catalog)
    port.emit(ARCHIVE,MEMBER,changed)
    return audit
