"""All 124 runtime title cards, fallback titles, and episode headings.

Member IDs are texture IDs, NOT stage numbers: branches and bonus scenarios
have their own cards. The reviewed JP/EN catalog is the coverage contract.
Preserve animation timing, digits, backgrounds, and unrelated atlas regions.
"""
import localization as _l10n
import csv
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GTF = 0xdf450
TITLE = _l10n.literal('scenario_title.TITLE/0')
CATALOG = Path(__file__).resolve().parents[1]/'translation/scenario_titles.tsv'
with CATALOG.open(encoding='utf-8', newline='') as stream:
    ROWS = list(csv.DictReader(stream, delimiter='\t'))
TITLES = {int(r['member']): r['English'] for r in ROWS}
assert len(ROWS) == len(TITLES) == 124 and set(TITLES) == set(range(5,129))
assert all(r['Japanese'] and r['English'].isascii() for r in ROWS)
EFFECTS = {87: GTF, 88: 0x101c70, 89: 0xc4d30, 90: 0xe7ba0, 91: 0x10d430}

def face(font_path):
    return str(Path(font_path).with_name('SCE-PS3-SR-R-LATIN.TTF'))

def word(text, font_path, size, bounds):
    font=ImageFont.truetype(face(font_path),size*2)
    l,t,r,b=font.getbbox(text)
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),text,font=font,fill='white')
    scale=min(.5,bounds[0]/ink.width,bounds[1]/ink.height)
    return ink.resize((round(ink.width*scale),round(ink.height*scale)),Image.Resampling.LANCZOS)

def glowing(ink):
    result=ink.filter(ImageFilter.GaussianBlur(3))
    result.alpha_composite(ink)
    return result

def argb(im):
    r,g,b,a=im.split()
    return Image.merge('RGBA',(a,r,g,b)).tobytes()

def title_pixels(font_path, title=TITLE):
    tile=Image.new('RGBA',(1536,128))
    ink=word(title,font_path,140,(1280,104))
    tile.alpha_composite(ink,((1536-ink.width)//2,(128-ink.height)//2))
    page=Image.new('RGBA',(1536,256))
    page.paste(tile,(0,0));page.paste(glowing(tile),(0,128))
    return argb(page)

def title_apply(blob,font_path,member=5):
    assert blob[24]==0xa5 and struct.unpack_from('>HH',blob,32)==(1536,256)
    off,n=struct.unpack_from('>II',blob,16)
    assert n==1536*256*4
    return blob[:off]+title_pixels(font_path,TITLES[member])+blob[off+n:]

def edits(blob, member=87):
    assert member in (87,88)
    result=[];counts=[0,0,0]
    for p in range(40,EFFECTS[member]-16,2):
        z,x,y,w,h,flags,mode,tex=struct.unpack_from('>8H',blob,p)
        if z or flags!=0x5000 or mode not in (0x0100,0x0200):continue
        coords=list(struct.unpack_from('>8h',blob,p-16))
        if tex==2 and y==0 and w==144 and h==112 and x in (0,288):
            assert coords in ([-338,-145,-274,-145,-338,-95,-274,-95],[-337,-145,-273,-145,-337,-95,-273,-95])
            coords[2]+=128;coords[6]+=128
            result.extend([(p-16,struct.pack('>8h',*coords)),(p+6,struct.pack('>H',288))]);counts[0]+=1
        elif tex in ((4,) if member==87 else (4,5)) and x==0 and y in (0,112) and w==96 and h==112:
            expected = [-275,-150,-223,-150,-275,-90,-223,-90] if member==87 else (
                [-230,-150,-178,-150,-230,-90,-178,-90] if tex==4 else
                [-277,-150,-225,-150,-277,-90,-225,-90])
            assert coords==expected
            for i in (0,2,4,6):coords[i]+=128
            result.append((p-16,struct.pack('>8h',*coords)));counts[1]+=1
        elif tex==2 and y==0 and w==144 and h==112 and x in (144,432):
            # Hide this quad's four vertex colors; do not overwrite nearby
            # Epilogue/logo artwork to manufacture a blank texture cell.
            result.append((p-40,b'\0'*16));counts[2]+=1
    assert counts==[1691,1674 if member==87 else 3348,1650],counts
    return result

def paint_rect(result, gtf, texture, rect, tile):
    """Replace one linear atlas rectangle; retain all adjacent pixels."""
    x,y,w,h=rect
    p=gtf+12+36*texture
    tw,th=struct.unpack_from('>HH',result,p+20)
    assert result[p+12]==0xa5 and tile.size==(w,h)
    assert 0<=x and 0<=y and x+w<=tw and y+h<=th
    off=gtf+struct.unpack_from('>I',result,p+4)[0]
    data=argb(tile)
    for row in range(h):
        q=off+((row+y)*tw+x)*4
        result[q:q+w*4]=data[row*w*4:(row+1)*w*4]

def effect_apply(blob,font_path,member=87):
    gtf=EFFECTS[member]
    assert blob[gtf:gtf+4]==b'\x02\x02\0\0'
    result=bytearray(blob)
    if member==89:
        # Final Episode has no digit quads; title and header share texture 2.
        for text,rect,glow_y in (("Final Episode",(592,0,432,112),112),
                                (TITLES[103],(0,544,1024,128),672)):
            x,y,w,h=rect
            tile=Image.new('RGBA',(w,h))
            ink=word(text,font_path,140,(w-24,h-24))
            tile.alpha_composite(ink,((w-ink.width)//2,(h-ink.height)//2))
            paint_rect(result,gtf,2,rect,tile)
            paint_rect(result,gtf,2,(x,glow_y,w,h),glowing(tile))
        return bytes(result)
    if member in (90,91):
        # Bonus scenario / Epilogue headings already English. Only fallback.
        p=gtf+12+36*3
        assert struct.unpack_from('>HH',blob,p+20)==(1536,256)
        off=gtf+struct.unpack_from('>I',blob,p+4)[0]
        result[off:off+1536*256*4]=title_pixels(font_path,TITLES[105 if member==90 else 5])
        return bytes(result)
    for off,data in edits(blob,member):result[off:off+len(data)]=data
    p=gtf+12+36*2
    assert blob[p+12]==0xa5 and struct.unpack_from('>HH',blob,p+20)==(1024,352)
    tile=Image.new('RGBA',(288,112))
    ink=word('Episode',font_path,110,(272,96))
    # The original quad scales 112 texture rows down to 50 screen units.
    # Compensate vertically so the longer word matches the existing digit.
    ink=ink.resize((272,96),Image.Resampling.LANCZOS)
    tile.alpha_composite(ink,((288-ink.width)//2,(112-ink.height)//2))
    for x,im in ((0,tile),(288,glowing(tile))):
        paint_rect(result,gtf,2,(x,0,288,112),im)
    p=gtf+12+36*3
    assert blob[p+12]==0xa5 and struct.unpack_from('>HH',blob,p+20)==(1536,256)
    off=gtf+struct.unpack_from('>I',blob,p+4)[0]
    result[off:off+1536*256*4]=title_pixels(font_path)
    return bytes(result)

def verify_title(original,built,font_path,member=5):
    assert built==title_apply(original,font_path,member) and built!=original
    assert len(original)==len(built)

def verify_effect(original,built,font_path,member=87):
    assert built==effect_apply(original,font_path,member) and built!=original
    assert len(original)==len(built)
    # Digit pixels and all subsequent textures (including background) retained.
    gtf=EFFECTS[member]
    following=3 if member==89 else 4
    off=gtf+struct.unpack_from('>I',original,gtf+12+36*following+4)[0]
    assert original[off:]==built[off:]
