"""Isolated Focus wording update: EBOOT hooks, five RPW names, two voice tips."""
import argparse,json,struct
from pathlib import Path
import eboot,trdata,digraph as dg,rpw,srvc_blocks as S
from patch_parts_candidate import patch
from standardize_focus import BASE,SOURCES

OUT=Path('work/out_0.6.3')
BACKUP=Path('work/focus_EBOOT.before.bin')


def table(data):
    segs=eboot._segments(data);p=eboot._off(segs,eboot.NAME_TBL);rows={}
    while struct.unpack_from('>I',data,p)[0]:
        k,v=struct.unpack_from('>II',data,p)
        rows[eboot._cstr(data,eboot._off(segs,k))]=(v,eboot._cstr(data,eboot._off(segs,v&0x3fffffff)))
        p+=8
    return rows


def name_changes():
    sources=json.loads(SOURCES.read_text(encoding='utf-8'))
    old=json.loads(sources['translation/skills.json'])
    new=json.loads(Path('translation/skills.json').read_text(encoding='utf-8'))
    return {jp:(en,new[jp]) for jp,en in old.items() if en!=new[jp]}


def update_rpw(data,mapping):
    out=bytearray(data);_,_,lo,hi,_=next(c for c in rpw.chunks(data) if c[0]=='j-string')
    counts={};allowed=set()
    for jp,(old,new) in name_changes().items():
        a,b=dg.encode_mixed(old,mapping),dg.encode_mixed(new,mapping)
        count=0;p=lo
        while p<hi:
            end=data.index(0,p);value=data[p:end]
            if value.startswith(a) and not value[len(a):].replace(rpw.FILL,b''):
                assert len(b)<=len(value) and (len(value)-len(b))%2==0
                out[p:end]=b+rpw.FILL*((len(value)-len(b))//2)
                allowed.update(range(p,end));count+=1
            p=end+1
        assert count>0,(jp,old)
        counts[jp]=count
    assert len(data)==len(out)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(data,out)))
    return bytes(out),counts


def update_voice(data,elf,mapping):
    sources=json.loads(SOURCES.read_text(encoding='utf-8'))
    old=json.loads(sources['translation/voice_121.json'])['lines']
    new=json.loads(Path('translation/voice_121.json').read_text(encoding='utf-8'))['lines']
    changes={dg.encode_mixed('「'+row['en']+'」',mapping):dg.encode_mixed('「'+new[k]['en']+'」',mapping)
             for k,row in old.items() if row['en']!=new[k]['en']}
    assert len(changes)==2
    out=bytearray(data);seen=set();allowed=set()
    for block in S.parse(data,S.read_table(elf)):
        for off in set(block['offs']):
            p=block['pool']+off;raw=S.string_at(data,p)
            if raw in changes:
                en=changes[raw];assert len(en)<=len(raw)
                out[p:p+len(raw)]=en+bytes(len(raw)-len(en))
                allowed.update(range(p,p+len(raw)));seen.add(raw)
    assert seen==set(changes)
    assert len(data)==len(out)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(data,out)))
    return bytes(out),len(seen)


def update_elf(old,mapping):
    before=json.loads(BASE.read_text(encoding='utf-8'))
    trdata.use_glossary('analysis/glossary.json')
    after=eboot.load_ui_hook()
    assert not set(before)-set(after)
    # Whitespace can change when shorter prose is wrapped, but no meaning or
    # keys outside this exact terminology change may be modified.
    for jp,en in after.items():
        if before.get(jp)!=en:
            assert jp in before
            assert before[jp].replace('Morale','Focus').split()==en.split(),jp
    rows=table(old)
    for jp,(a,b) in name_changes().items():
        if jp.encode('cp932') in rows:
            assert rows[jp.encode('cp932')][1]==dg.encode_mixed(a,mapping)
            before[jp]=a;after[jp]=b
    return patch(old,mapping,before,after)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');a=ap.parse_args()
    mapping=json.loads((OUT/'pairs.json').read_text())
    old=(OUT/'EBOOT.BIN').read_bytes()
    elf,stats=update_elf(old,mapping)
    rp,c=update_rpw((OUT/'RPW_DATA.CPK').read_bytes(),mapping)
    voice,n=update_voice((OUT/'SRVC.BIN').read_bytes(),old,mapping)
    print('EBOOT delta:',stats,'; skill-name copies:',list(c.values()),'; voice tips:',n)
    print('RPW/voice offsets and all file sizes preserved; no gameplay, voice-table or executable-code changes.')
    if a.write:
        for filename,target in [('EBOOT.BIN',BACKUP),('RPW_DATA.CPK',Path('work/focus_RPW.before.bin')),('SRVC.BIN',Path('work/focus_SRVC.before.bin'))]:
            assert not target.exists()
        for filename,new,target in [('EBOOT.BIN',elf,BACKUP),('RPW_DATA.CPK',rp,Path('work/focus_RPW.before.bin')),('SRVC.BIN',voice,Path('work/focus_SRVC.before.bin'))]:
            target.write_bytes((OUT/filename).read_bytes());(OUT/filename).write_bytes(new)


if __name__=='__main__':main()
