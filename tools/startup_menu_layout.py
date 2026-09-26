"""PS3 startup sprites, using the same canonical labels and cells as Vita."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from attack_heading import morton,span
from localization import Catalog
import aiddata

FONT='C:/Windows/Fonts/arialbd.ttf'
ROWS=((272,432,240,40,'ui_aiddata:scenario_select_heading',False),
      (136,472,72,40,'ui.vita_menu_art:main',True),
      (208,472,168,40,'ui.vita_menu_art:tutorial',True),
      (376,472,136,40,'ui.vita_menu_art:scenario',True))
QUADS=((0x534c8,136,72),(0x53518,376,136),(0x53568,376,136),(0x535b8,208,168))


def validate_quads(ui):
    for at,x,w in QUADS:
        for i,(u,v) in enumerate(((x+w/2,492),(x,472),(x+w,472),(x+w,512),(x,512))):
            assert struct.unpack_from('>ff',ui,at+i*16+8)==(u/512,v/512)


def tile(text,w,h,stroke):
    font=ImageFont.truetype(FONT,120);sw=4 if stroke else 0
    l,t,r,b=font.getbbox(text,stroke_width=sw)
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),text,font=font,fill='white',stroke_width=sw,stroke_fill='black')
    scale=min(.25,(w-8)/ink.width,(h-8)/ink.height)
    ink=ink.resize((max(1,round(ink.width*scale)),max(1,round(ink.height*scale))),Image.Resampling.LANCZOS)
    out=Image.new('RGBA',(w,h));out.alpha_composite(ink,((w-ink.width)//2,(h-ink.height)//2))
    return out


def apply_art(raw):
    start=span(raw);out=bytearray(raw);allowed=set();catalog=Catalog()
    for x,y,w,h,mid,stroke in ROWS:
        ink=tile(catalog.text(mid),w,h,stroke)
        for yy in range(h):
            for xx in range(w):
                p=start+4*morton(x+xx,y+yy);r,g,b,a=ink.getpixel((xx,yy))
                out[p:p+4]=bytes((a,r,g,b));allowed.update(range(p,p+4))
    assert len(out)==len(raw) and out!=raw
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(raw,out)))
    return bytes(out)


def apply_ui(raw):
    validate_quads(raw)
    p=struct.unpack_from('>I',raw,0xa1454)[0]+aiddata.STR_BASE
    assert raw[p:p+2]=='■'.encode('cp932')
    out=bytearray(raw);out[p:p+2]='　'.encode('cp932')
    assert len(out)==len(raw)
    return bytes(out)


def image(raw):
    start=span(raw);im=Image.new('RGBA',(512,512));pixels=im.load()
    for y in range(512):
        for x in range(512):
            p=start+4*morton(x,y);a,r,g,b=raw[p:p+4];pixels[x,y]=(r,g,b,a)
    return im


if __name__=='__main__':
    from cpk import CPK
    c=CPK('game/PS3_GAME/USRDIR/DATA/AIDDATA/AIDDATAPACK.CPK')
    raw=c.read(next(e for e in c.files if e['id']==1))
    out=Path('work/ps3_link_v3_review');out.mkdir(exist_ok=True)
    image(raw).save(str(out/'startup-before.png'))
    image(apply_art(raw)).save(str(out/'startup-after.png'))
