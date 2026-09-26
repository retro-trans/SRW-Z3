"""Source-bound partial translation of shared end-session scenes."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
import cpkpatch
from cpk import CPK
import digraph as dg
import luarec
import trdata

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/'translation/suspend_scene.json'
SOURCE=ROOT/'work/orig/STG0700.SDAT'
NAME='STG0700.SDAT'
SOURCE_SHA256='c94570e929132034639c44d6105a800a6dc318b6b61b5a8f7491a70c97814bc4'

def translations():
    return trdata.records(str(CATALOG))+trdata.shared_records('suspend_scene_dancouga')

def patch(original,mapping):
    text=original.decode('cp932');records=luarec.records(text)
    assert len(records)==872
    wanted={(r['event'],r['n']):r for r in translations()}
    assert len(wanted)==16
    matches=list(luarec.BLOCK.finditer(text));changes=[]
    for record,match in zip(records,matches):
        key=(record['event'],record['n'])
        if key not in wanted:continue
        row=wanted[key]
        assert record['sha']==row['sha'] and record['pid']==row['pid'],key
        en=row['en'];jp=record['jp'].replace('\r\n','\n')
        assert len(en.split('\n'))==len(jp.split('\n'))
        assert en.count('「')==jp.count('「')==1 and en.count('」')==jp.count('」')==1
        assert re.findall(r'\$[nlFc]',en)==re.findall(r'\$[nlFc]',jp)
        assert all(len(line)<=55 for line in en.split('\n')[1:])
        assert all(line.startswith('　') for line in en.split('\n')[2:])
        start=len(text[:match.start(1)].encode('cp932'))
        end=len(text[:match.end(1)].encode('cp932'))
        encoded=dg.encode_mixed(en.replace('\n','\r\n'),mapping)
        changes.append((start,end,encoded))
    assert len(changes)==len(wanted)
    built=bytearray();cursor=0
    for start,end,encoded in changes:
        built+=original[cursor:start]+encoded;cursor=end
    built+=original[cursor:]
    # Every byte outside these selected long-string bodies is copied verbatim.
    return bytes(built)

def prepare(npdata):
    if not SOURCE.exists():
        from extract import Source
        Source(disc='E:/SRWZ3/PS3_GAME/USRDIR').path(NAME)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==SOURCE_SHA256
    target=ROOT/'work/save_quit/STG0700.cpk'
    target.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run([str(npdata),'-d',str(SOURCE),str(target),'0'],check=True,capture_output=True)
    return target

def build(out,mapping,npdata):
    source=prepare(npdata);archive=CPK(str(source))
    original=archive.read(next(f for f in archive.files if f['id']==1))
    built=patch(original,mapping)
    out=Path(out)
    check_widths(mapping,{int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()})
    member=out/'suspend_scene.member';member.write_bytes(built)
    cpkpath=out/'STG0700.cpk'
    cpkpatch.build(str(source),str(cpkpath),{1:str(member)})
    packed=CPK(str(cpkpath))
    assert packed.read(next(f for f in packed.files if f['id']==1))==built
    assert archive.read(next(f for f in archive.files if f['id']==0))==packed.read(next(f for f in packed.files if f['id']==0))
    subprocess.run([str(npdata),'-e',str(cpkpath),str(out/NAME),'2','0','00','1','16','0','','0'],check=True,capture_output=True)
    check=out/'STG0700.check.cpk'
    subprocess.run([str(npdata),'-d',str(out/NAME),str(check),'0'],check=True,capture_output=True)
    assert check.read_bytes()==cpkpath.read_bytes()
    member.unlink();check.unlink()
    print('PASS: shared end-session scenes: 16/16 dialogue records, packed and SDAT round-trip verified; all other source bytes preserved.')

def check_widths(mapping,widths):
    from intermission_layout import ink
    for row in translations():
        for line in row['en'].split('\n')[1:]:
            assert ink(line,mapping,widths,31)<963,(row['sha'],line)

def check(out,mapping,widths):
    out=Path(out);source=ROOT/'work/save_quit/STG0700.cpk'
    original=CPK(str(source));built=CPK(str(out/'STG0700.cpk'))
    def member(k,i):return k.read(next(f for f in k.files if f['id']==i))
    assert member(built,1)==patch(member(original,1),mapping)
    assert member(built,0)==member(original,0)
    check_widths(mapping,widths)
    print('PASS: built end-session scenes have all 16 translations, matching global glyphs and fitting dialogue width; voice/control data unchanged.')
