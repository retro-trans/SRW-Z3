"""All 83 Japan/world/space map-pin captions; no animation or map changes."""
import hashlib
import json
import re
import struct
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from attack_heading import morton
import terms

ROOT=Path(__file__).resolve().parents[1]
CATALOG=json.loads((ROOT/'translation/map_locations.json').read_text(encoding='utf-8'))
ROWS={r[0]:(r[1],r[2]) for r in CATALOG['rows']}
SOURCES={r['member']:r for r in json.loads((ROOT/'translation/map_location_sources.json').read_text(encoding='utf-8'))['rows']}
EXPECTED=set(range(92,114))|set(range(116,157))|set(range(167,187))
assert len(ROWS)==83 and set(ROWS)==set(SOURCES)==EXPECTED

def english(member):
    glossary=json.loads((ROOT/'analysis/glossary.json').read_text(encoding='utf-8'))
    result=terms.expand(ROWS[member][1],terms.index(glossary),'map caption %d'%member)
    assert result.isascii() and result
    return result

def span(blob,member):
    row=SOURCES[member];g=row['gtf']
    assert blob[g:g+4]==b'\x02\x02\0\0' and blob[g+24]==0x85
    assert list(struct.unpack_from('>HH',blob,g+32))==row['texture_size']
    off,size=struct.unpack_from('>II',blob,g+16)
    assert size==row['texture_size'][0]*row['texture_size'][1]*4
    assert g+off+size<=len(blob)
    return g+off

def caption(blob,member):
    offset=span(blob,member);x,y,w,h=SOURCES[member]['caption_rect']
    data=b''.join(blob[offset+4*morton(xx,yy):offset+4*morton(xx,yy)+4]
                  for yy in range(y,y+h) for xx in range(x,x+w))
    return Image.frombytes('RGBA',(w,h),data,'raw','ARGB')

def alignment(blob,member):
    box=caption(blob,member).getchannel('A').getbbox()
    assert box is not None
    return 'right' if box[0]>20 else 'left'

def render(blob,font_path,member):
    w,h=SOURCES[member]['caption_rect'][2:]
    label=english(member);font=ImageFont.truetype(font_path,22*4)
    l,t,r,b=font.getbbox(label)
    ink=Image.new('RGBA',(r-l,b-t))
    ImageDraw.Draw(ink).text((-l,-t),label,font=font,fill=(218,232,253,255))
    # Preserve nominal cap height; only horizontal condensation for long names.
    nw=min(w-12,round(ink.width/4));nh=round(ink.height/4)
    assert 0<nw<=w-12 and 0<nh<=h-2
    ink=ink.resize((nw,nh),Image.Resampling.LANCZOS)
    tile=Image.new('RGBA',(w,h),(218,232,253,0))
    x=w-6-nw if alignment(blob,member)=='right' else 6
    tile.alpha_composite(ink,(x,(h-nh)//2))
    return tile

def audit_source(blob,member):
    row=SOURCES[member]
    assert hashlib.sha256(blob).hexdigest()==row['sha256'], ('map source changed',member)
    span(blob,member)
    x,y,w,h=row['caption_rect'];key=struct.pack('>4H',x,y,w,h)
    positions=[]
    for m in re.finditer(re.escape(key),blob[:row['gtf']]):
        p=m.start()-2
        if blob[p:p+2]==b'\0\0' and blob[p+10:p+12]==b'\x50\0' and blob[p+14:p+16]==b'\0\0':
            positions.append(p)
    assert len(positions)==row['sample_count'] and positions
    return positions

def apply(blob,font_path,member):
    audit_source(blob,member)
    tile=render(blob,font_path,member);out=bytearray(blob);offset=span(blob,member)
    x,y,w,h=SOURCES[member]['caption_rect']
    for yy in range(h):
        for xx in range(w):
            r,g,b,a=tile.getpixel((xx,yy));p=offset+4*morton(x+xx,y+yy)
            out[p:p+4]=bytes((a,r,g,b))
    return bytes(out)

def verify(original,built,font_path,member):
    assert len(original)==len(built) and original!=built
    assert caption(built,member).tobytes()==render(original,font_path,member).tobytes()
    # Mask the permitted rectangle and compare every remaining byte, including
    # all animation UVs/vertices, timing, photos, glows, map geometry and headers.
    a=bytearray(original);b=bytearray(built);offset=span(original,member)
    x,y,w,h=SOURCES[member]['caption_rect']
    for yy in range(y,y+h):
        for xx in range(x,x+w):
            p=offset+4*morton(xx,yy);a[p:p+4]=b[p:p+4]=bytes(4)
    assert a==b, ('outside map caption changed',member)
    audit_source(original,member)

def verify_archive(original,built,font_path,other_changed=()):
    old={f['id']:f for f in original.files};new={f['id']:f for f in built.files}
    assert old.keys()==new.keys()
    for member in ROWS:
        verify(original.read(old[member]),built.read(new[member]),font_path,member)
    for member in old.keys()-ROWS.keys()-set(other_changed):
        # Untouched members retain their compressed payload exactly.
        a,b=old[member],new[member]
        assert a['size']==b['size'] and a['extract']==b['extract']
        assert original.buf[a['offset']:a['offset']+a['size']]==built.buf[b['offset']:b['offset']+b['size']],member
    print('PASS: 83 map captions; all other member payloads unchanged except declared title assets.')
