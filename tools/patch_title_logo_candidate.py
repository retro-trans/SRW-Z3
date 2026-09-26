"""Isolated title member replacement in the existing unstamped candidate.

Dry-run first. --write packs and audits a sibling archive before replacement.
All other compressed payloads must be byte-identical; keep a title-member backup.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from cpk import CPK
import cpkpatch
import title_logo as L
import title_footer as F

TARGET=Path('work/out_0.6.3/EFFPS3.CPK')
BACKUP=Path('work/title_logo.before.member')


def digest(data): return hashlib.sha256(data).hexdigest()


def inventory(path):
    k=CPK(str(path)); hashes={}
    for f in k.files:
        hashes[str(f['id'])]=(f['size'],f['extract'],digest(k.buf[f['offset']:f['offset']+f['size']]))
    blob=k.read(next(f for f in k.files if f['id']==F.MEMBER))
    return hashes,blob,digest(k.buf)


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    before,base,archive_hash=inventory(TARGET)
    built=L.apply(base)
    if built==base:
        print('English title logo already present; no changes.');return
    L.verify(base,built)
    print('Only member %d changes; %d other member payloads preserved.'%(F.MEMBER,len(before)-1))
    print('Title SHA256:',digest(base),'->',digest(built))
    if not args.write: return
    if BACKUP.exists(): assert BACKUP.read_bytes()==base, 'different title backup already exists'
    else: BACKUP.write_bytes(base)
    member=Path('work/title_logo.next.member');member.write_bytes(built)
    staged=TARGET.with_name('EFFPS3.title-logo.next.cpk')
    assert staged.resolve().parent==TARGET.resolve().parent and staged!=TARGET
    assert not staged.exists(), 'staging archive already exists; inspect it first'
    cpkpatch.build(str(TARGET),str(staged),{F.MEMBER:str(member)})
    after,packed,next_hash=inventory(staged)
    assert set(before)==set(after)
    for ident,record in before.items():
        if int(ident)!=F.MEMBER: assert after[ident]==record, 'other member changed: '+ident
    L.verify(base,packed)
    # Refuse to overwrite a candidate modified while packing.
    with TARGET.open('rb') as f:
        h=hashlib.sha256()
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    assert h.hexdigest()==archive_hash, 'candidate changed concurrently'
    os.replace(str(staged),str(TARGET))
    L.atlas(packed).save(TARGET.parent/'title_logo_atlas.png')
    Path('work/title_logo_patch_audit.json').write_text(json.dumps({
        'archive':str(TARGET),'before_sha256':archive_hash,'after_sha256':next_hash,
        'title_before_sha256':digest(base),'title_after_sha256':digest(packed),
        'unchanged_other_payloads':len(before)-1,'backup':str(BACKUP),
        'members_before':before,'members_after':after},indent=2)+'\n',encoding='utf-8')
    print('Packed candidate verified; no ISO, release or deployment changes.')


if __name__=='__main__': main()
