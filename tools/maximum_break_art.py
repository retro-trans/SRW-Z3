"""Translate battle action labels and Maximum Break in BTLC/CMN.CPK.

Keep the 1472x176 banner texture, 136x192 badge atlas, UVs and animation
commands unchanged. Includes the four cyan attack badges, Combo Attack,
Counter, Attack Again, Support Attack and Support Defend. The already-English
red ribbons are texture 1 and remain unchanged.
"""
import localization as _l10n
import hashlib,struct
from pathlib import Path
from collections import Counter
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from cpk import CPK
import cpkpatch
from scenario_title import paint_rect

SOURCE=Path('work/orig/CMN.CPK')
GTF=0x9de0
SOURCE_HASH='1359e4fa6b1adb2ab711a5e7c88960d82d37ae4d927ac9f737fd0e263247e2cc'
RECTS={16:(0,0,1472,176),6:(5,164,126,24)}
# Native battle-animation surfaces, separate from the map UI word atlas.
ACTION_RECTS=(
    (6,(5,36,126,24),_l10n.literal('maximum_break_art.ACTION_RECTS/0'),'cyan'),
    (6,(5,68,126,24),_l10n.literal('maximum_break_art.ACTION_RECTS/1'),'cyan'),
    (6,(5,100,126,24),_l10n.literal('maximum_break_art.ACTION_RECTS/2'),'cyan'),
    (6,(5,132,126,24),_l10n.literal('maximum_break_art.ACTION_RECTS/3'),'cyan'),
    (10,(0,0,192,48),_l10n.literal('maximum_break_art.ACTION_RECTS/4'),'cyan'),
    (11,(0,0,272,64),_l10n.literal('maximum_break_art.ACTION_RECTS/5'),'pink'),
    (11,(0,64,272,64),_l10n.literal('maximum_break_art.ACTION_RECTS/6'),'purple'),
    (11,(0,128,272,64),_l10n.literal('maximum_break_art.ACTION_RECTS/7'),'purple'),
    (11,(0,192,272,64),_l10n.literal('maximum_break_art.ACTION_RECTS/8'),'gold'),
)

def action_tile(rect,label,color,font_path):
    _,_,w,h=rect
    face=ImageFont.truetype(str(Path(font_path).with_name('SCE-PS3-RD-BI-LATIN.TTF')),h*4)
    l,t,r,b=face.getbbox(label)
    mask=Image.new('L',(r-l,b-t));ImageDraw.Draw(mask).text((-l,-t),label,font=face,fill=255)
    border=3 if h==24 else 6
    mask=mask.resize((min(w-border*2,round(mask.width/mask.height*(h-border*2))),h-border*2),Image.Resampling.LANCZOS)
    canvas=Image.new('L',(w,h));canvas.paste(mask,((w-mask.width)//2,border))
    out=Image.new('RGBA',(w,h),(0,8,8,255) if h==24 else (0,0,0,0))
    tint={'cyan':(0,210,215),'pink':(232,40,167),'purple':(121,73,238),'gold':(224,161,18)}[color]
    edge=Image.new('RGBA',(w,h),tint+(255,));edge.putalpha(canvas.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(.7)))
    out.alpha_composite(edge)
    fill=Image.new('RGBA',(w,h));draw=ImageDraw.Draw(fill)
    for y in range(h):
        ratio=y/max(1,h-1)
        rgb=tuple(round(255*(1-ratio)+v*ratio) for v in tint)
        draw.line((0,y,w-1,y),fill=rgb+(255,))
    fill.putalpha(canvas);out.alpha_composite(fill)
    return out

def texture(blob,index):
    p=GTF+12+36*index;o,n=struct.unpack_from('>II',blob,p+4)
    size=struct.unpack_from('>HH',blob,p+20)
    assert blob[p+12]==0xa5 and n==size[0]*size[1]*4
    return Image.frombytes('RGBA',size,blob[GTF+o:GTF+o+n],'raw','ARGB')

def banner(original,font_path):
    # Use the existing PS3 bold italic face and sample the original gold
    # stripe palette by row. No external bitmap or screenshot is embedded.
    font=ImageFont.truetype(str(Path(font_path).with_name('SCE-PS3-RD-BI-LATIN.TTF')),210)
    l,t,r,b=font.getbbox('MAXIMUM BREAK')
    mask=Image.new('L',(r-l,b-t));ImageDraw.Draw(mask).text((-l,-t),'MAXIMUM BREAK',font=font,fill=255)
    mask=mask.resize((1400,144),Image.Resampling.LANCZOS)
    canvas=Image.new('L',(1472,176));canvas.paste(mask,(36,16))
    out=Image.new('RGBA',canvas.size)
    for radius,color in ((5,(30,25,16,255)),(4,(246,245,228,255)),(2,(85,49,12,255))):
        edge=canvas.filter(ImageFilter.MaxFilter(radius*2+1))
        layer=Image.new('RGBA',canvas.size,color);layer.putalpha(edge);out.alpha_composite(layer)
    fill=Image.new('RGBA',canvas.size);draw=ImageDraw.Draw(fill)
    previous=(190,116,20)
    for y in range(176):
        colors=Counter((r,g,b) for r,g,b,a in [original.getpixel((x,y)) for x in range(original.width)]
                       if a>240 and r>g>40 and g>b*1.3)
        if colors:previous=colors.most_common(1)[0][0]
        draw.line((0,y,1471,y),fill=previous+(255,))
    fill=fill.filter(ImageFilter.GaussianBlur(.8))
    fill.putalpha(canvas);out.alpha_composite(fill)
    assert out.getchannel('A').getbbox()[0]>0 and out.getchannel('A').getbbox()[2]<1472
    return out

def badge(original,font_path):
    # This rectangle is inside the orange frame, on the dark name plate.
    tile=Image.new('RGBA',(126,24),(6,3,0,255))
    font=ImageFont.truetype(str(Path(font_path).with_name('SCE-PS3-RD-BI-LATIN.TTF')),64)
    l,t,r,b=font.getbbox('MAX BREAK',stroke_width=2)
    ink=Image.new('RGBA',(r-l,b-t));ImageDraw.Draw(ink).text((-l,-t),'MAX BREAK',font=font,
         fill=(255,48,0,255),stroke_width=2,stroke_fill=(241,177,16,255))
    ink=ink.resize((114,18),Image.Resampling.LANCZOS)
    tile.alpha_composite(ink,(6,2));return tile

def apply(blob,font_path):
    assert hashlib.sha256(blob).hexdigest()==SOURCE_HASH,'unexpected battle UI source'
    assert struct.unpack_from('>I',blob,GTF+8)[0]==20
    original=texture(blob,16);assert original.size==(1472,176)
    small=texture(blob,6);assert small.size==(136,192)
    out=bytearray(blob)
    paint_rect(out,GTF,16,RECTS[16],banner(original,font_path))
    paint_rect(out,GTF,6,RECTS[6],badge(small,font_path))
    for index,rect,label,color in ACTION_RECTS:
        paint_rect(out,GTF,index,rect,action_tile(rect,label,color,font_path))
    return bytes(out)

def verify(original,built,font_path):
    assert built==apply(original,font_path) and built!=original
    restored=bytearray(built)
    for index,(x,y,w,h) in list(RECTS.items())+[(i,r) for i,r,_,_ in ACTION_RECTS]:
        p=GTF+12+36*index;tw=struct.unpack_from('>H',original,p+20)[0]
        off=GTF+struct.unpack_from('>I',original,p+4)[0]
        for row in range(h):
            q=off+((y+row)*tw+x)*4;restored[q:q+w*4]=original[q:q+w*4]
    assert restored==original,'non-lettering texture or animation bytes changed'
    print('PASS: Maximum Break plus nine battle action surfaces; frames, arrows, controls, UVs and animation bytes unchanged.')

def build(out,font_path):
    assert SOURCE.exists(),'extract the pristine BTLC/CMN.CPK to work/orig first'
    k=CPK(str(SOURCE));original=k.read(k.files[0]);built=apply(original,font_path)
    verify(original,built,font_path)
    tmp=Path(out)/'maximum_break.member';tmp.write_bytes(built)
    cpkpatch.build(str(SOURCE),str(Path(out)/'CMN.CPK'),{0:str(tmp)});tmp.unlink()
    texture(built,16).save(Path(out)/'maximum_break_banner.png')
    texture(built,6).save(Path(out)/'maximum_break_badge.png')
    texture(built,10).save(Path(out)/'combo_attack.png')
    texture(built,11).save(Path(out)/'battle_action_banners.png')
