"""Native Intermission/Scenario word cells; original palettes and quads stay."""
import struct
from PIL import Image,ImageDraw,ImageFont
from category_port import require,digest
from title_art import nearest_palette
import startup_art as startup

# Atlas cells are shared by the native sprite-word renderer, bypassing VWF.
CELLS=((0,0,192,296,40,'ui_hook:r_4e63c037d3cb8a3d'),
       (2,136,472,72,40,'ui.vita_menu_art:main'),
       (2,208,472,168,40,'ui.vita_menu_art:tutorial'),
       (2,376,472,136,40,'ui.vita_menu_art:scenario'))
QUADS=((0x534C8,136,72),(0x53518,376,136),
       (0x53568,376,136),(0x535B8,208,168))

def validate_quads(raw):
    for p,x,w in QUADS:
        for i,(u,v) in enumerate(((x+w/2,492),(x,472),(x+w,472),(x+w,512),(x,512))):
            require(struct.unpack_from('<ff',raw,p+i*16+8)==(u/512,v/512),
                    'Scenario sprite UV changed')

def tile(text,w,h):
    font=ImageFont.truetype(str(startup.FONT),30*4)
    l,t,r,b=font.getbbox(text,stroke_width=4)
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),text,font=font,fill='white',stroke_width=4,stroke_fill='black')
    scale=min(.25,(w-8)/ink.width,(h-8)/ink.height)
    ink=ink.resize((max(1,round(ink.width*scale)),max(1,round(ink.height*scale))),Image.Resampling.LANCZOS)
    result=Image.new('RGBA',(w,h));result.alpha_composite(ink,((w-ink.width)//2,(h-ink.height)//2))
    return result

def apply(raw,catalog):
    # Regenerate from the original, carrying both prior startup heading edits.
    prior,previous=startup.apply(raw,catalog);out=bytearray(prior);allowed=set();rows=[]
    for page,x,y,w,h,mid in CELLS:
        start=192+page*262144;pal=192+4*262144+page*1024
        palette=tuple(tuple(raw[p:p+4]) for p in range(pal,pal+1024,4));match=nearest_palette(palette)
        text=catalog.text(mid);ink=tile(text,w,h)
        for yy in range(h):
            for xx in range(w):
                p=start+startup.pixel(x+xx,y+yy);allowed.add(p);out[p]=match(ink.getpixel((xx,yy)))
        rows.append(dict(page=page,rectangle=[x,y,w,h],message=mid,text=text))
    require(len(out)==len(prior) and all(a==b or i in allowed for i,(a,b) in enumerate(zip(prior,out))),
            'Menu art changed outside word cells')
    return bytes(out),dict(status='native_menu_word_candidate',source_sha256=digest(raw),
        sha256=digest(out),rows=rows,prior_startup_headings=previous,
        palettes_and_quads_preserved=True,runtime_tested=False)

def prepare(port):
    archive=port.cpk(startup.ARCHIVE)
    validate_quads(archive.read(next(e for e in archive.files if e['id']==0)))
    raw=archive.read(next(e for e in archive.files if e['id']==startup.MEMBER))
    changed,audit=apply(raw,port.catalog);port.emit(startup.ARCHIVE,startup.MEMBER,changed)
    return audit
