"""Independent, bounded terrain-record inventory for every available map."""
import hashlib
import json
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DISC_SOURCE = Path('E:/SRWZ3/PS3_GAME/USRDIR/DATA/MAPETC/ATTR')
SNAPSHOT = ROOT/'work/orig/MAPATTR'
EXTRA = {row['jp']: row['en'] for row in json.loads(
    (ROOT/'translation/terrain_all_hook.json').read_text(encoding='utf8'))['lines']}

def key(jp):
    number = str(list(EXTRA).index(jp)).zfill(3)
    return '地' + number.translate(str.maketrans('0123456789','０１２３４５６７８９'))

def inventory(source=None):
    source = source or (SNAPSHOT if SNAPSHOT.exists() else DISC_SOURCE)
    files = sorted(source.glob('*.ZLD'))
    assert files, 'No terrain source files found'
    names, records, manifests = {}, [], {}
    for path in files:
        blob = path.read_bytes()
        width,height,count,flags,unit,base,size,grid = struct.unpack_from('<8I',blob)
        assert base == 32 and size == count*32 and grid == width*height, path
        assert len(blob) == base+size+grid and count > 0, path
        assert max(blob[base+size:]) < count, path
        manifests[path.name] = hashlib.sha256(blob).hexdigest()
        for i in range(count):
            offset = base+i*32+4
            raw = blob[offset:offset+28]
            assert b'\0' in raw, (path, i)
            name = raw.split(b'\0')[0].decode('cp932')
            assert name and not any(raw[len(name.encode('cp932')):]), (path, i)
            ref = {'file':path.name, 'record':i, 'offset':offset}
            names.setdefault(name, []).append(ref)
            records.append(dict(ref,jp=name))
    return {'files':manifests, 'names':names, 'records':records}

def render(blob):
    out = bytearray(blob)
    count = struct.unpack_from('<I',blob,8)[0]
    allowed = set()
    for i in range(count):
        p = 0x24+i*32
        jp = blob[p:p+28].split(b'\0')[0].decode('cp932')
        if jp in EXTRA:
            raw = key(jp).encode('cp932')
            out[p:p+28] = raw + bytes(28-len(raw))
            allowed.update(range(p,p+28))
    assert len(out) == len(blob)
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    return bytes(out)

def prepare(outdir):
    import shutil
    baseline = inventory()
    if not SNAPSHOT.exists():
        SNAPSHOT.mkdir(parents=True)
        for name in baseline['files']:
            shutil.copy2(DISC_SOURCE/name,SNAPSHOT/name)
    assert inventory(SNAPSHOT)['files'] == baseline['files']
    for name in baseline['files']:
        (Path(outdir)/name).write_bytes(render((SNAPSHOT/name).read_bytes()))

def check_maps(outdir):
    baseline = inventory()
    for name in baseline['files']:
        source = SNAPSHOT if SNAPSHOT.exists() else DISC_SOURCE
        assert (Path(outdir)/name).read_bytes() == render((source/name).read_bytes()),name
    print('PASS: all 64 prepared maps match terrain-text-only edits; stats, headers and tile grids unchanged.')
