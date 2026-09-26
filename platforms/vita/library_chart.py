"""Native library/chart display adapters; never change sorting or episode IDs.

Chart strings are drawn by code, not ASSF. Match complete formatted results
and alias only its private Confirm literal. Raster edits are bounded to the
two native title/background lettering regions; palettes and animation survive.
"""
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from category_port import require,digest,encoded
from inspect_vwf import segment
from scene_art import Page,verify_mask
from prepare_vwf import FONT
import runtime_headings
import episode_heading_hooks as shared
import unicodedata

ARCHIVE='DATA/anime/effvita.cpk'
SOURCES={297:(0x62C00,'5f08bb01b9036d2faec06aa8361bb130a633264adbe41f5609fd729b30a37633'),
         298:(0x1A0,'4f0db4da2992e6b9af6254c38836753ec213853e9de5dd83c76d18ffa4517eb3')}
HEADER=(112,12,432,68)
SUBTITLE=(128,176,1056,384)
TITLE_MID='ui.title_library_buttons:r_e96afa13f4c5fa9c'
ALIAS='~COK'


def hooks(port,executable,info):
    import ui_text
    text,base=segment(executable,info,0);data,dbase=segment(executable,info,1)
    def at(address,value):
        require(text[address-base:address-base+len(value)]==value,'Chart source changed: '+hex(address))
    at(0x8126DB68,'：決定\0\0：戻る\0\0：スピードＵＰ\0\0『%s』\0'.encode('cp932'))
    at(0x81271AF8,b''.join(c.encode('cp932')+b'\0\0' for c in '０１２３４５６７８９第話'))
    # Private literal, both callers, and unmodified native draw entry.
    import vwf
    for address in (0x810B2F6A,0x810B30BA):
        at(address,vwf.assemble('movw r0,#0xdb68; movt r0,#0x8126',address))
    require(ALIAS.encode()+b'\0' not in text,'Chart alias already exists')
    compact=port.catalog.text('ui.library_chart:confirm')
    require(sum(port.widths[c] for c in compact)*28/32+716<=840,
            'Chart Confirm overlaps native Back icon')
    speed=port.catalog.text('ui.library_chart:speed')
    require(sum(port.widths[c] for c in speed)*28/32+1036<=1264,'Chart speed text exceeds frame')
    rows={k:encoded(compact,port.mapping) for k in
          (ALIAS.encode(),ui_text.converted_key(ALIAS,executable,info))}
    rows['：スピードＵＰ'.encode('cp932')]=encoded(speed,port.mapping)
    translations={unicodedata.normalize('NFKC',r['Japanese']):r['English'] for r in shared.scenario_title.ROWS}
    translations.update({unicodedata.normalize('NFKC',jp):en for jp,en in shared.EXTRA.items()})
    for i in range(159):
        ptr=struct.unpack_from('<I',data,runtime_headings.TITLES-dbase+i*4)[0]-base
        require(0<=ptr<len(text),'Chart title pointer outside source')
        jp=text[ptr:text.index(b'\0',ptr)].decode('cp932')
        en=translations[unicodedata.normalize('NFKC',jp)]
        rows[('『'+jp+'』').encode('cp932')]=encoded('『'+en+'』',port.mapping)
    for i in range(181):
        number=struct.unpack_from('<h',data,runtime_headings.RECORDS-dbase+i*32+14)[0]
        if 0<number<=99:
            wide=str(number).translate(str.maketrans('0123456789','０１２３４５６７８９'))
            en=port.catalog.text('ui.library_chart:episode').format(number=number)
            rows[('第'+wide+'話').encode('cp932')]=encoded(en,port.mapping)
    return rows,[(0x8126DB68,'：決定',ALIAS.encode()+b'\0\0')]


def label(text,size,font_size,color='white',stroke=0):
    font=ImageFont.truetype(str(FONT),font_size)
    l,t,r,b=font.getbbox(text,stroke_width=stroke)
    ink=Image.new('RGBA',(r-l+4,b-t+4))
    ImageDraw.Draw(ink).text((2-l,2-t),text,font=font,fill=color,
                           stroke_width=stroke,stroke_fill='black')
    scale=min(1,(size[0]-16)/ink.width,(size[1]-8)/ink.height)
    ink=ink.resize((round(ink.width*scale),round(ink.height*scale)),Image.Resampling.LANCZOS)
    tile=Image.new('RGBA',size);tile.alpha_composite(ink,((size[0]-ink.width)//2,(size[1]-ink.height)//2))
    return tile


def apply(raw,member,catalog):
    gxt,sha=SOURCES[member];require(digest(raw)==sha,'Chart artwork source changed')
    page=Page(raw,gxt,1);require((page.w,page.h,page.kind)==(1280,720,0x60000000),'Chart atlas changed')
    before=page.image();x,y,w,h=HEADER
    # Repeat the adjacent unlettered header material, keeping its horizontal
    # rules, the button-icon strip, panel borders and every other texel intact.
    clean=before.crop((552,y,616,y+h));tile=Image.new('RGBA',(w,h))
    for xx in range(0,w,clean.width):tile.paste(clean,(xx,0))
    ink=label(catalog.text(TITLE_MID),(w,h),52,stroke=2)
    glow=Image.new('RGBA',(w,h),(190,80,255,0))
    glow.putalpha(ink.getchannel('A').filter(ImageFilter.GaussianBlur(4)))
    tile.alpha_composite(glow);tile.alpha_composite(ink)
    out=bytearray(raw);allowed=set();page.paint(out,HEADER,tile,allowed)
    regions=[dict(texture=1,rectangle=HEADER,message=TITLE_MID)]
    if member==297:
        page=Page(raw,gxt,2);require((page.w,page.h)==(1280,720),'Chart background changed')
        original=page.image();x,y,w,h=SUBTITLE
        # Recreate the dark letter bed from the unlettered top texture strip.
        # Its hue/noise follow the source left-to-right purple/red gradient.
        tile=original.crop((x,0,x+w,128)).resize((w,h))
        pixels=tile.load()
        for yy in range(h):
            for xx in range(w):
                r,g,b,a=pixels[xx,yy];pixels[xx,yy]=(r//12,g//12,b//12,a)
        ink=label(catalog.text('ui.library_chart:subtitle'),(w,h),140)
        mask=ink.getchannel('A');colored=Image.new('RGBA',(w,h));px=colored.load()
        for xx in range(w):
            f=xx/(w-1);color=(int(131*(1-f)+159*f),int(35*(1-f)+30*f),int(224*(1-f)+92*f),255)
            for yy in range(h):px[xx,yy]=color
        colored.putalpha(mask.point(lambda a:a*3//4))
        glow=colored.copy();glow.putalpha(mask.filter(ImageFilter.GaussianBlur(14)).point(lambda a:a//2))
        tile.alpha_composite(glow);tile.alpha_composite(colored)
        # Soft outside edge avoids a rectangular seam. All original lettering
        # lies more than 20 texels inside this region, fully covered here.
        old=original.crop((x,y,x+w,y+h));blend=Image.new('L',(w,h));bp=blend.load()
        for yy in range(h):
            for xx in range(w):bp[xx,yy]=min(255,int(min(xx,yy,w-1-xx,h-1-yy)*255/20))
        tile=Image.composite(tile,old,blend)
        page.paint(out,SUBTITLE,tile,allowed)
        regions.append(dict(texture=2,rectangle=SUBTITLE,message='ui.library_chart:subtitle'))
    verify_mask(raw,bytes(out),allowed)
    return bytes(out),dict(member=member,source_sha256=sha,sha256=digest(out),regions=regions,
                          palette_animation_and_other_pixels_preserved=True,runtime_tested=False)


def prepare(port):
    archive=port.cpk(ARCHIVE);rows=[]
    for member in SOURCES:
        raw=archive.read(next(e for e in archive.files if e['id']==member))
        changed,audit=apply(raw,member,port.catalog);port.emit(ARCHIVE,member,changed);rows.append(audit)
    return dict(status='native_chart_art_verified',archive=ARCHIVE,members=rows,issues=[])
