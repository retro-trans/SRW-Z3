"""Translate battle action labels and Maximum Break in BTLC/CMN.CPK.

Keep texture sizes and animation timing unchanged. Repack the nine animated
banner pieces and their XY/UV rectangles together (the native atlas repeats
one Japanese glyph). Includes the four cyan attack badges, Combo Attack,
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
# Left-to-right native pieces: rectangle offset, initial X, initial Y,
# signed XY bounds and unsigned UV endpoints. The fourth piece reuses the
# first glyph; a continuous English repaint cannot work with these samples.
BANNER_PIECES=(
    (0x419c,-632,0,(-88,-88,88,88,1,0,175,176)),
    (0x4080,-504,0,(-84,-88,84,88,177,0,343,176)),
    (0x3f70,-344,4,(-96,-96,96,80,345,0,535,176)),
    (0x3e60,-160,0,(-88,-88,88,88,1,0,175,176)),
    (0x3d58,-56,0,(-84,-88,84,88,537,0,703,176)),
    (0x3c48,176,0,(-96,-92,96,84,705,0,895,176)),
    (0x3b38,332,0,(-92,-84,92,92,897,0,1079,176)),
    (0x3a24,496,0,(-100,-86,100,90,1081,0,1279,176)),
    (0x3910,624,0,(-96,-84,96,92,1281,0,1471,176)),
)
BANNER_CHUNKS=('MA','XI','M','U','M','B','R','EA','K')


def banner_layout(font_path):
    """Nine whole-letter cells, with a common baseline and font scale."""
    font=ImageFont.truetype(str(Path(font_path).with_name('SCE-PS3-RD-BI-LATIN.TTF')),210)
    boxes=[font.getbbox(s) for s in BANNER_CHUNKS]
    top=min(b[1] for b in boxes);bottom=max(b[3] for b in boxes)
    # Transparent gutters protect outlines from bilinear sampling of neighbours.
    # An extra word gap follows MAXIMUM. Widths sum exactly to the native atlas.
    pads=[16]*9;pads[4]+=24
    scale=(1472-sum(pads))/sum(b[2]-b[0] for b in boxes)
    widths=[round((b[2]-b[0])*scale)+pad for b,pad in zip(boxes,pads)]
    widths[-1]+=1472-sum(widths)
    result=[];x=0
    for label,box,width,pad in zip(BANNER_CHUNKS,boxes,widths,pads):
        result.append((x,width,label,box,pad))
        x+=width
    return font,top,bottom,result


def patch_banner_pieces(out,font_path):
    for (p,anchor_x,anchor_y,expected),cell in zip(BANNER_PIECES,banner_layout(font_path)[3]):
        assert struct.unpack_from('<4h4H',out,p)==expected,'Maximum Break sprite source drift'
        anchor_offset=p-(16 if p==0x419c else 12)
        assert struct.unpack_from('<2h',out,anchor_offset)==(anchor_x,anchor_y)
        x,w,_,_,_=cell
        # Lay out the settled phrase in screen space, not in the original
        # overlapping Japanese glyph boxes. Keep all keyframe values intact.
        struct.pack_into('<4h4H',out,p,x-736-anchor_x,-88-anchor_y,
                         x+w-736-anchor_x,88-anchor_y,x+1,0,x+w-1,176)
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
    font,top,bottom,cells=banner_layout(font_path)
    canvas=Image.new('L',(1472,176))
    for x,w,label,(l,t,r,b),pad in cells:
        mask=Image.new('L',(r-l,bottom-top))
        ImageDraw.Draw(mask).text((-l,-top),label,font=font,fill=255)
        mask=mask.resize((w-pad,144),Image.Resampling.LANCZOS)
        canvas.paste(mask,(x+8,16))
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
    patch_banner_pieces(out,font_path)
    return bytes(out)

def verify(original,built,font_path):
    assert built==apply(original,font_path) and built!=original
    restored=bytearray(built)
    for p,_,_,_ in BANNER_PIECES:
        restored[p:p+16]=original[p:p+16]
    for index,(x,y,w,h) in list(RECTS.items())+[(i,r) for i,r,_,_ in ACTION_RECTS]:
        p=GTF+12+36*index;tw=struct.unpack_from('>H',original,p+20)[0]
        off=GTF+struct.unpack_from('>I',original,p+4)[0]
        for row in range(h):
            q=off+((y+row)*tw+x)*4;restored[q:q+w*4]=original[q:q+w*4]
    assert restored==original,'bytes outside lettering and nine banner rectangles changed'
    print('PASS: Maximum Break nine-piece XY/UV layout and battle action surfaces; all other pixels and animation commands unchanged.')

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
