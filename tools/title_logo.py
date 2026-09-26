"""English title word sprites; native Z pixels, UVs and animation stay intact."""
import hashlib
import struct
from pathlib import Path
from PIL import Image
import title_footer as F

SIZE=(1024,720)
ASSETS=Path(__file__).resolve().parents[1]/'work/title_logo_final'
ROWS=(
    (0,0,706,296,'wordmark.png','294369bf76cdae6613224ec7887ff8438984111d58644a75825482fa27e81356'),
    (0,603,339,117,'subtitle-v2.png','49ecf6e63ceec727ad73c367af784b239969f3ec47747437a0f9739773075d1c'),
)
# All sampled rectangles of the separate native Z frame and fiery fills.
Z_BOXES=((24,304,473,601),(664,268,1024,550),(666,268,1024,564))


def span(blob):
    p=F.GTF+12+36
    assert blob[p+12]==0xa5
    assert struct.unpack_from('>HH',blob,p+20)==SIZE
    off,size=struct.unpack_from('>II',blob,p+4)
    assert size==SIZE[0]*SIZE[1]*4 and F.GTF+off+size<=len(blob)
    return F.GTF+off


def atlas(blob):
    p=span(blob)
    return Image.frombytes('RGBA',SIZE,blob[p:p+SIZE[0]*SIZE[1]*4],'raw','ARGB')


def audit(blob):
    span(blob)
    for rect,count in (((1,0,0,706,296,0x5800),1706),((0,0,603,339,117,0x5000),1657)):
        pattern=struct.pack('>6H',*rect)+b'\x01\x01\0\x01'
        assert blob[:F.GTF].count(pattern)==count, 'title animation/UV source drift'


def tiles():
    for x,y,w,h,name,sha in ROWS:
        path=ASSETS/name
        preparer = 'prepare_approved_subtitle.py' if name == 'subtitle-v2.png' else 'clean_title_logo.py'
        assert path.exists(), 'Missing clean title art; run tools/%s --write with the saved approved source.' % preparer
        assert hashlib.sha256(path.read_bytes()).hexdigest()==sha, 'unreviewed title art: '+name
        with Image.open(path) as im:
            assert im.mode=='RGBA' and im.size==(w,h)
            yield (x,y,w,h),im.copy()


def restore_regions(original,built):
    out=bytearray(built);p=span(original)
    for x,y,w,h,_,_ in ROWS:
        for yy in range(y,y+h):
            start=p+(yy*SIZE[0]+x)*4
            out[start:start+w*4]=original[start:start+w*4]
    return bytes(out)


def apply(base):
    audit(base)
    before=atlas(base);im=before.copy()
    for (x,y,w,h),tile in tiles():
        # Preserve unused transparent RGBA bytes too, including the transparent
        # intersection with the fiery Z's sampling rectangle.
        old=im.crop((x,y,x+w,y+h))
        pixels=[new if new[3] or prev[3] else prev
                for prev,new in zip(old.getdata(),tile.getdata())]
        tile.putdata(pixels);im.paste(tile,(x,y))
    for box in Z_BOXES:
        assert im.crop(box).tobytes()==before.crop(box).tobytes(), 'Z sprite changed'
    r,g,b,a=im.split();raw=Image.merge('RGBA',(a,r,g,b)).tobytes()
    out=bytearray(base);p=span(base);out[p:p+len(raw)]=raw
    return bytes(out)


def verify(base,built):
    assert len(base)==len(built) and base!=built
    assert built==apply(base), 'English title logo mismatch'
    assert restore_regions(base,built)==base, 'unrelated title bytes changed'
    print('PASS: English title sprites; original Z, 3363 word-sprite samples and all other title bytes preserved.')


def verify_complete(original,built,font_path,version=None):
    import title_library_buttons as B
    base=restore_regions(original,built)
    B.verify(original,base,font_path,version)
    verify(base,built)
