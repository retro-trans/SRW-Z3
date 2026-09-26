"""Translate shared UI word sprites without modifying neighboring artwork."""
import localization as _l10n
import struct
from PIL import Image,ImageDraw,ImageFont
from attack_heading import morton

# Bounds follow the actual word-cell edges in the original 512x512 atlas.
CELLS = (
    # Map-battle defensive activation words (yellow tint/shadow supplied in game).
    (0,(0,24,128,48),_l10n.literal('trader_art.CELLS/0'),22),
    (0,(0,48,88,72),_l10n.literal('trader_art.CELLS/1'),22),
    (0,(88,48,136,72),_l10n.literal('trader_art.CELLS/2'),22),
    (0,(0,72,64,96),_l10n.literal('trader_art.CELLS/3'),22),
    (0,(0,192,296,232),_l10n.literal('trader_art.CELLS/4'),30),
    (2,(160,0,296,40),_l10n.literal('trader_art.CELLS/5'),30),
    (2,(296,0,392,40),_l10n.literal('trader_art.CELLS/6'),30),
    (2,(392,0,512,40),_l10n.literal('trader_art.CELLS/7'),30),
    (2,(0,88,72,128),_l10n.literal('trader_art.CELLS/8'),30),
    (2,(72,88,144,128),_l10n.literal('trader_art.CELLS/9'),30),
    (2,(144,88,216,128),_l10n.literal('trader_art.CELLS/10'),30),
    (2,(216,88,256,128),_l10n.literal('trader_art.CELLS/11'),30),
    (2,(256,88,336,128),_l10n.literal('trader_art.CELLS/12'),30),
    (2,(336,88,384,128),_l10n.literal('trader_art.CELLS/13'),30),
    (2,(320,40,512,88),_l10n.literal('trader_art.CELLS/14'),30),
    (2,(0,40,176,88),_l10n.literal('trader_art.CELLS/15'),30),
    (2,(176,40,320,88),_l10n.literal('trader_art.CELLS/16'),30),
    (2,(56,192,112,224),_l10n.literal('trader_art.CELLS/17'),26),
    (2,(56,320,88,352),_l10n.literal('trader_art.CELLS/18'),26),
    # The renderer combines Armor/Sight with the shared Japanese suffix 値.
    # English needs no suffix; keep its slot transparent without moving UVs.
    (2,(56,256,112,288),_l10n.literal('trader_art.CELLS/19'),26),
    (2,(56,224,112,256),_l10n.literal('trader_art.CELLS/20'),26),
    (2,(56,352,88,384),'',26),
)

def tile(text,width,height,size,font_path):
    if not text:return Image.new('RGBA',(width,height))
    font=ImageFont.truetype(font_path,size*4)
    l,t,r,b=font.getbbox(text)
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),text,font=font,fill='white')
    # These words have enlarged native quads in support_popup_layout. Keep
    # one point size/baseline (including Support's descender), rather than
    # stretching every word to the same height as well as squeezing its width.
    word_height=round(ink.height/4) if text in ('Support','Attack','Defend','Re-') else 29
    ink=ink.resize((min(width-8,round(ink.width/4)),min(word_height,height-6)),Image.Resampling.LANCZOS)
    result=Image.new('RGBA',(width,height))
    x=width-ink.width if text=='Mobi' else 0 if text=='lity' else (width-ink.width)//2
    result.alpha_composite(ink,(x,4))
    return result

def apply(blob,font_path):
    result=bytearray(blob)
    assert struct.unpack_from('>I',blob,8)[0]==4
    for texture,(x0,y0,x1,y1),text,size in CELLS:
        p=12+texture*36
        assert blob[p+12]==0x85 and struct.unpack_from('>HH',blob,p+20)==(512,512)
        start=struct.unpack_from('>I',blob,p+4)[0]
        ink=tile(text,x1-x0,y1-y0,size,font_path)
        for y in range(y0,y1):
            for x in range(x0,x1):
                r,g,b,a=ink.getpixel((x-x0,y-y0))
                p=start+4*morton(x,y)
                result[p:p+4]=bytes((a,r,g,b))
    return bytes(result)

def verify(before,after,font_path):
    assert after==apply(before,font_path) and after!=before
    allowed=set()
    for texture,(x0,y0,x1,y1),text,size in CELLS:
        start=struct.unpack_from('>I',before,12+texture*36+4)[0]
        allowed.update(start+4*morton(x,y)+c for x in range(x0,x1) for y in range(y0,y1) for c in range(4))
    assert len(before)==len(after)
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(before,after)))
