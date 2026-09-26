"""Native P8 Vita episode cards and map captions, using shared PS3 wording.

Native GXT palettes/layout and native animation records are validated; no PS3
texture or machine-code bytes are inserted. All edits have explicit masks.
"""
from functools import lru_cache
import struct
from PIL import Image,ImageDraw,ImageFont
from category_port import require,digest
from title_art import nearest_palette
from build_test import TPACK
import scenario_title as titles
import map_locations as locations
from prepare_vwf import FONT

ARCHIVE='DATA/anime/effvita.cpk'


@lru_cache(maxsize=32)
def swizzle(width,height):
    require(width&(width-1)==0 and height&(height-1)==0,'Non-power-of-two swizzled page')
    bits=min(width,height).bit_length()-1
    spread=[sum(((v>>i)&1)<<(2*i) for i in range(bits)) for v in range(max(width,height))]
    return tuple(spread[y]+(spread[x]<<1)+((x>>bits if width>=height else y>>bits)<<(bits*2))
                 for y in range(height) for x in range(width))


class Page:
    def __init__(self,data,gxt=0,texture=0):
        require(data[gxt:gxt+8]==b'GXT\0\x03\0\0\x10','Wrong native GXT')
        n,begin,total,p4,p8=struct.unpack_from('<5I',data,gxt+8)
        require(p4==0 and p8==n and texture<n,'Unexpected native P8 palettes')
        off,size,palette,flags,kind,fmt,w,h,mips=struct.unpack_from('<6IHHI',data,gxt+32+32*texture)
        require((palette,flags,fmt,mips)==(0,0,0x95000000,1) and size==w*h and
                kind in (0,0x60000000),'Unsupported native P8 texture')
        self.start=gxt+off;self.w=w;self.h=h;self.kind=kind
        self.pal=gxt+begin+total-p8*1024+texture*1024
        require(gxt+begin+total<=len(data) and self.start+size<=self.pal,'Invalid P8 extents')
        self.palette=tuple(tuple(data[i:i+4]) for i in range(self.pal,self.pal+1024,4))
        self.data=data
        self.order=swizzle(w,h) if kind==0 else None

    def address(self,x,y):
        return self.start+(self.order[y*self.w+x] if self.order else y*self.w+x)

    def image(self):
        raw=self.data[self.start:self.start+self.w*self.h]
        if self.order:raw=bytes(raw[p] for p in self.order)
        im=Image.frombytes('P',(self.w,self.h),raw)
        im.putpalette(bytes(v for color in self.palette for v in color[:3]))
        im.info['transparency']=bytes(color[3] for color in self.palette)
        return im.convert('RGBA')

    def paint(self,out,rect,tile,allowed):
        x,y,w,h=rect
        require(tile.size==(w,h) and 0<=x<x+w<=self.w and 0<=y<y+h<=self.h,'Invalid art rectangle')
        match=nearest_palette(self.palette)
        pixels=tile.load()
        for yy in range(h):
            for xx in range(w):
                at=self.address(x+xx,y+yy);out[at]=match(pixels[xx,yy]);allowed.add(at)


def verify_mask(original,changed,allowed):
    require(len(original)==len(changed) and original!=changed,'Empty or resized artwork edit')
    require(all(a==b or i in allowed for i,(a,b) in enumerate(zip(original,changed))),
            'Artwork changed outside declared regions')


def title(data,member):
    page=Page(data);require((page.w,page.h,page.kind)==(1536,256,0x60000000),'Wrong title texture')
    # This rasterizer reads the shared scenario catalog; members are texture
    # IDs, not episode numbers. Preserve both sharp and glow halves.
    tile=Image.frombytes('RGBA',(1536,256),titles.title_pixels(str(FONT),titles.TITLES[member]),'raw','ARGB')
    out=bytearray(data);allowed=set();page.paint(out,(0,0,1536,256),tile,allowed)
    verify_mask(data,out,allowed);return bytes(out)


def samples(data,gxt,rect):
    """Vita sample: little-endian UVs/vertices, flags10 and byte-sized mode."""
    x,y,w,h=rect;out=[]
    for at in range(40,gxt-16,2):
        z,xx,yy,ww,hh,flags,mode=struct.unpack_from('<7H',data,at)
        tex=struct.unpack_from('>H',data,at+14)[0]
        if (z,xx,yy,ww,hh,flags)==(0,x,y,w,h,10) and mode in (1,2,3,257,258,259) and tex==0:out.append(at)
    return out


def map_caption(data,member):
    spec=locations.SOURCES[member];g=spec['gtf'];page=Page(data,g)
    require([page.w,page.h]==spec['texture_size'],'Map texture dimensions differ')
    rect=spec['caption_rect'];refs=samples(data,g,rect)
    require(len(refs)==spec['sample_count'],'Native map-caption UV inventory differs: '+str(member))
    x,y,w,h=rect;old=page.image().crop((x,y,x+w,y+h));box=old.getchannel('A').getbbox()
    require(box is not None,'Missing original caption ink')
    label=locations.english(member);font=ImageFont.truetype(str(FONT),22*4)
    l,t,r,b=font.getbbox(label);ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),label,font=font,fill=(218,232,253,255))
    ink=ink.resize((min(w-12,round(ink.width/4)),round(ink.height/4)),Image.Resampling.LANCZOS)
    tile=Image.new('RGBA',(w,h));tile.alpha_composite(ink,((w-6-ink.width if box[0]>20 else 6),(h-ink.height)//2))
    out=bytearray(data);allowed=set();page.paint(out,rect,tile,allowed)
    verify_mask(data,out,allowed);return bytes(out)


def episode_geometry(data,g,member):
    edits=[];counts=[0,0,0]
    for at in range(40,g-16,2):
        z,x,y,w,h,flags,mode=struct.unpack_from('<7H',data,at)
        tex=struct.unpack_from('>H',data,at+14)[0]
        if z or flags!=10 or mode not in (1,2):continue
        coords=list(struct.unpack_from('<8h',data,at-16))
        if tex==2 and y==0 and w==144 and h==112 and x in (0,288):
            require(coords in ([-338,-145,-274,-145,-338,-95,-274,-95],
                               [-337,-145,-273,-145,-337,-95,-273,-95]),'Episode quad differs')
            coords[2]+=128;coords[6]+=128
            edits.extend(((at-16,struct.pack('<8h',*coords)),(at+6,struct.pack('<H',288))));counts[0]+=1
        elif tex in ((4,) if member==87 else (4,5)) and x==0 and y in (0,112) and w==96 and h==112:
            expected=([-275,-150,-223,-150,-275,-90,-223,-90] if member==87 else
                      [-230,-150,-178,-150,-230,-90,-178,-90] if tex==4 else
                      [-277,-150,-225,-150,-277,-90,-225,-90])
            require(coords==expected,'Episode digit placement differs')
            for i in (0,2,4,6):coords[i]+=128
            edits.append((at-16,struct.pack('<8h',*coords)));counts[1]+=1
        elif tex==2 and y==0 and w==144 and h==112 and x in (144,432):
            edits.append((at-40,bytes(16)));counts[2]+=1
    require(counts==[1691,1674 if member==87 else 3348,1650],'Episode animation sample counts differ')
    return edits


def episode(data,member):
    import localization
    catalog=localization.Catalog()
    g=titles.EFFECTS[member];out=bytearray(data);allowed=set()
    def paint(tex,rect,tile):Page(data,g,tex).paint(out,rect,tile,allowed)
    if member in (87,88):
        for at,payload in episode_geometry(data,g,member):
            out[at:at+len(payload)]=payload;allowed.update(range(at,at+len(payload)))
        tile=Image.new('RGBA',(288,112));ink=titles.word(catalog.text('ui.episode_heading_hooks:episode_label'),str(FONT),110,(272,96))
        tile.alpha_composite(ink.resize((272,96),Image.Resampling.LANCZOS),(8,8))
        paint(2,(0,0,288,112),tile);paint(2,(288,0,288,112),titles.glowing(tile))
    if member==89:
        for text,rect,glow in ((catalog.text('ui.episode_heading_hooks:final_label'),(592,0,432,112),112),
                               (titles.TITLES[103],(0,544,1024,128),672)):
            x,y,w,h=rect;tile=Image.new('RGBA',(w,h));ink=titles.word(text,str(FONT),140,(w-24,h-24))
            tile.alpha_composite(ink,((w-ink.width)//2,(h-ink.height)//2))
            paint(2,rect,tile);paint(2,(x,glow,w,h),titles.glowing(tile))
    else:
        label=titles.TITLES[105 if member==90 else 5]
        tile=Image.frombytes('RGBA',(1536,256),titles.title_pixels(str(FONT),label),'raw','ARGB')
        paint(3,(0,0,1536,256),tile)
    verify_mask(data,out,allowed);return bytes(out)


def prepare(port):
    report=[];cpk=port.cpk(TPACK)
    for member in sorted(titles.TITLES):
        original=cpk.read(next(e for e in cpk.files if e['id']==member));changed=title(original,member)
        port.emit(TPACK,member,changed)
        report.append(dict(archive=TPACK,member=member,source_sha256=digest(original),sha256=digest(changed)))
    cpk=port.cpk(ARCHIVE)
    for member in sorted(set(locations.ROWS)|set(titles.EFFECTS)):
        original=cpk.read(next(e for e in cpk.files if e['id']==member))
        changed=map_caption(original,member) if member in locations.ROWS else episode(original,member)
        port.emit(ARCHIVE,member,changed)
        report.append(dict(archive=ARCHIVE,member=member,source_sha256=digest(original),sha256=digest(changed)))
    return dict(status='native_scene_art_verified',title_cards=124,map_captions=83,episode_effects=5,
                members=report,unrelated_pixels_palettes_and_timing_preserved=True,runtime_tested=False)
