"""Native Vita title P8 textures: reuse approved artwork and shared menu text.

Only palette indices in seven sampled rectangles change. No palette, GXT
header, animation command, native Z sprite or executable is replaced.
"""
import hashlib
from functools import lru_cache
import struct
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from PIL import Image
import title_logo as logo
import title_library_buttons as buttons

ARCHIVE = 'DATA/anime/effvita.cpk'
MEMBER = 296
GXT = 0x1fe290
SOURCE_SHA256 = '804e3007c4a84ba0181c5d4fae786a70d782d90b4a62d5b20ebec14cf456af71'
SIZES = ((1280,720),(1024,720),(1024,720),(1280,720),
         (1280,720),(720,512),(720,720))


def require(ok, message):
    if not ok:
        raise ValueError(message)


class Title:
    def __init__(self, data):
        self.data = bytes(data)
        require(data[GXT:GXT+8] == b'GXT\0\x03\0\0\x10', 'Wrong title GXT')
        count, offset, size, p4, p8 = struct.unpack_from('<5I',data,GXT+8)
        require((count,offset,p4,p8)==(7,256,0,7), 'Unexpected title palettes')
        self.palettes = GXT+offset+size-p8*1024
        require(GXT+offset+size<=len(data), 'Truncated GXT')
        self.textures = []
        expected = offset
        for i, dimensions in enumerate(SIZES):
            at,n,pal,flags,kind,fmt,w,h,mips = struct.unpack_from('<6IHHI',data,GXT+32+i*32)
            require((at,n,pal,flags,kind,fmt,w,h,mips)==
                    (expected,dimensions[0]*dimensions[1],0,0,0x60000000,0x95000000,
                     dimensions[0],dimensions[1],1), 'Unsupported title texture')
            self.textures.append((GXT+at,w,h))
            expected += n
        require(GXT+expected==self.palettes, 'Wrong palette location')

    def palette(self, texture):
        at = self.palettes+texture*1024
        return tuple(tuple(self.data[p:p+4]) for p in range(at,at+1024,4))

    def image(self, texture):
        at,w,h = self.textures[texture]
        im = Image.frombytes('P',(w,h),self.data[at:at+w*h])
        im.putpalette(bytes(v for rgba in self.palette(texture) for v in rgba),rawmode='RGBA')
        return im.convert('RGBA')


def audit(data):
    require(hashlib.sha256(data).hexdigest()==SOURCE_SHA256, 'Vita title source changed')
    title = Title(data)
    rows = [(1,(0,0,706,296),1,0x1a,1706),(1,(0,603,339,117),0,0xa,1657)]
    rows += [(5,row[:4],0,0xa,row[-1]) for row in buttons.ROWS]
    for texture,rect,mode,flags,count in rows:
        pattern = struct.pack('<6H',mode,*rect,flags)+bytes((1,1,0,texture))
        require(data[:GXT].count(pattern)==count, 'Native Vita title UV/animation drift')
    return title


def nearest_palette(palette):
    # Premultiplied colour distance avoids opaque dark fringes at alpha edges.
    vectors = [(r*a//255,g*a//255,b*a//255,a*2) for r,g,b,a in palette]
    @lru_cache(maxsize=65536)
    def match(rgba):
        r,g,b,a = rgba
        q = (r*a//255,g*a//255,b*a//255,a*2)
        return min(range(256), key=lambda i: sum((x-y)**2 for x,y in zip(q,vectors[i])))
    return match


def spans(title):
    for texture,rect in [(1,r[:4]) for r in logo.ROWS]+[(5,r[:4]) for r in buttons.ROWS]:
        x,y,w,h = rect
        at,stride,_ = title.textures[texture]
        for yy in range(y,y+h):
            yield at+yy*stride+x,w


def apply(data):
    title = audit(data)
    out = bytearray(data)
    tiles = [(1,rect,tile) for rect,tile in logo.tiles()]
    tiles += [(5,row[:4],buttons.tile(row)) for row in buttons.ROWS]
    matchers = {i:nearest_palette(title.palette(i)) for i in (1,5)}
    for texture,(x,y,w,h),tile in tiles:
        at,stride,_ = title.textures[texture]
        palette = title.palette(texture)
        pixels = tile.load()
        for yy in range(h):
            for xx in range(w):
                pos = at+(y+yy)*stride+x+xx
                rgba = pixels[xx,yy]
                # Keep fully transparent unused source bytes unchanged.
                if rgba[3]==0 and palette[data[pos]][3]==0:
                    continue
                out[pos] = matchers[texture](rgba)
    verify(data,bytes(out))
    return bytes(out)


def verify(original,changed):
    title = audit(original)
    require(len(original)==len(changed) and original!=changed, 'Missing or resized title patch')
    restored = bytearray(changed)
    for at,n in spans(title):
        restored[at:at+n] = original[at:at+n]
    require(bytes(restored)==original, 'Unrelated Vita title data changed')
    new = Title(changed)
    # Includes transparent intersection with the native animated Z region.
    for box in logo.Z_BOXES:
        require(title.image(1).crop(box).tobytes()==new.image(1).crop(box).tobytes(),
                'Native Z artwork changed')


def prepare(port):
    archive = port.cpk(ARCHIVE)
    original = archive.read(next(e for e in archive.files if e['id']==MEMBER))
    changed = apply(original)
    port.emit(ARCHIVE,MEMBER,changed)
    return dict(status='member_verified',archive=ARCHIVE,member=MEMBER,
                source_sha256=SOURCE_SHA256,patched_sha256=hashlib.sha256(changed).hexdigest(),
                library_labels=5,title_regions=2,animation_samples_preserved=5655,
                palettes_preserved=True,runtime_tested=False,issues=[])


def preview():
    """Generate local comparison atlases only; never an installable build."""
    from cpk import CPK
    source = ROOT/'work/vita/decrypted_PCSG00264'/ARCHIVE
    archive = CPK(str(source))
    original = archive.read(next(e for e in archive.files if e['id']==MEMBER))
    output = ROOT/'work/vita/title_art_review'
    output.mkdir(exist_ok=True)
    old = audit(original)
    for i in (1,5):
        old.image(i).save(output/('original-%d.png'%i))
    changed = apply(original)
    new = Title(changed)
    for i in (1,5):
        new.image(i).save(output/('english-%d.png'%i))
    print('Verified title-only preview:',output,flush=True)


if __name__=='__main__':
    preview()
