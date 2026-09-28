"""Demo series-name sprites in BTLC/OP.CPK (four sets of six captions).

Use canonical glossary messages, not independent translations. Only replace
the six full-width ARGB texture payloads; demo scripts, actors and timing stay
byte-identical. Source hashes also guard the visually identified slot order.
"""
import hashlib
import shutil
import struct
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from cpk import CPK
import cpkpatch
import localization

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work/orig/OP.CPK'
FONT = Path('C:/Windows/Fonts/timesbd.ttf')
GTF = 0x60
SIZE = (1280, 64)
HASHES = (
    '3385f7b21081b34ce5718eaf565782d914d533b4bde7a26d405b3972170e2016',
    'db97029df28c6d0ae14ccef7c109fbb51a53288bdae0a54572462c983305c398',
    '6ecd1ee9099f6d0ad28381e5f36a4e1aaf0936559d6138d3e76fd6e56b57b13f',
    '3206b213166747463291dedcb30fa5c321445bf38a6e19fe69cbb8911fd834d8',
)
# Texture order visually checked against all 24 original caption images.
MESSAGES = (
    ('35de22c2f00d27b2', 'cc4b6d9a5835b064', '26d5de1194a7448b',
     '2824459a9912fac2', '2000eabda61a68d5', '490a4c8e08ac5dc2'),
    ('8b2191cfd1f9e3f5', '6416b2cf6f67cf93', '36dddc5a6af05e66',
     '587e4f404bcab3f1', '5985d999d6d6d61e', 'f1fb3797442a9d3d'),
    ('c6d8f38cf3e312c9', '4fac3d25759d0157', '9e48cfa2bcb27737',
     '5c9cc4c5310b12c6', '319e6c286eaaf722', '33232fad44b41ea8'),
    ('0c18a8f681e32d8a', '1b90eaad6d57183f', '9c0d8db220493bf6',
     '71bb80483700299f', '9ebe897072995f53', '85e7706f124685c8'),
)


def message_id(member, texture):
    return 'glossary:r_' + MESSAGES[member][texture]


def span(blob, texture):
    assert 0 <= texture < 6
    assert blob[GTF:GTF+4] == b'\x02\x02\0\0'
    assert struct.unpack_from('>I', blob, GTF+8)[0] == 6
    p = GTF+12+36*texture
    offset, size = struct.unpack_from('>II', blob, p+4)
    assert blob[p+12] == 0xa5
    assert struct.unpack_from('>HH', blob, p+20) == SIZE
    assert offset == 256+texture*1280*64*4 and size == 1280*64*4
    assert GTF+offset+size <= len(blob)
    return GTF+offset, size


def audit_source(blob, member):
    assert hashlib.sha256(blob).hexdigest() == HASHES[member], 'Demo source changed'
    for texture in range(6):
        span(blob, texture)


def tile(member, texture, font=FONT):
    label = localization.message(message_id(member, texture))
    assert label and label.isascii() and '\n' not in label
    scale = 4
    face = ImageFont.truetype(str(font), 52*scale)
    stroke = 2*scale
    l, t, r, b = face.getbbox(label, stroke_width=stroke)
    ink = Image.new('RGBA', (r-l+8, b-t+8))
    ImageDraw.Draw(ink).text((4-l, 4-t), label, font=face, fill='white',
                             stroke_width=stroke, stroke_fill='black')
    # Maintain readable height; condense only titles wider than the screen.
    ink = ink.resize((min(1248, round(ink.width/scale)), round(ink.height/scale)),
                     Image.Resampling.LANCZOS)
    assert ink.height <= 56, 'Demo title exceeds the native strip height'
    result = Image.new('RGBA', SIZE)
    result.alpha_composite(ink, ((SIZE[0]-ink.width)//2, (SIZE[1]-ink.height)//2))
    box = result.getchannel('A').getbbox()
    assert box and box[0] >= 16 and box[2] <= 1264 and box[1] >= 4 and box[3] <= 60
    return result


def pixels(member, texture, font=FONT):
    r, g, b, a = tile(member, texture, font).split()
    return Image.merge('RGBA', (a, r, g, b)).tobytes()


def apply(original, member, font=FONT):
    audit_source(original, member)
    built = bytearray(original)
    for texture in range(6):
        start, size = span(original, texture)
        built[start:start+size] = pixels(member, texture, font)
    return bytes(built)


def verify(original, built, member, font=FONT):
    audit_source(original, member)
    assert len(original) == len(built) and original != built
    restored = bytearray(built)
    for texture in range(6):
        start, size = span(original, texture)
        assert span(built, texture) == (start, size)
        assert built[start:start+size] == pixels(member, texture, font)
        restored[start:start+size] = original[start:start+size]
    assert restored == original, 'Demo changed outside title texture pixels'


def members(archive):
    rows = {f['id']: archive.read(f) for f in archive.files}
    assert len(archive.files) == 4 and set(rows) == set(range(4))
    return rows


def verify_archive(source, built, font=FONT):
    originals, replacements = members(source), members(built)
    for member in range(4):
        verify(originals[member], replacements[member], member, font)


def build(out, font=FONT):
    # Only called by an explicitly requested full build. Never accept a
    # translated game copy as a pristine input on subsequent runs.
    source = SOURCE if SOURCE.exists() else ROOT/'game/PS3_GAME/USRDIR/DATA/BTLC/OP.CPK'
    originals = members(CPK(str(source)))
    for member, original in originals.items():
        audit_source(original, member)
    if not SOURCE.exists():
        SOURCE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, SOURCE)
    with tempfile.TemporaryDirectory(prefix='demo_titles_', dir=str(out)) as tmp:
        replacements = {}
        for member, original in originals.items():
            built = apply(original, member, font)
            verify(original, built, member, font)
            path = Path(tmp)/('%d.member' % member)
            path.write_bytes(built)
            replacements[member] = str(path)
        target = Path(out)/'OP.CPK'
        cpkpatch.build(str(SOURCE), str(target), replacements)
        verify_archive(CPK(str(SOURCE)), CPK(str(target)), font)
    print('[demo] All 24 series captions translated; demo scripts and timing unchanged.')
