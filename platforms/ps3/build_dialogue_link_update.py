"""RPCS3 v5 EBOOT-only update from pinned v4. Dry-run; never auto-installs."""
import argparse,hashlib,io,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import eboot,dialogue_link_scene as S
import link_background_layout as L
import date_card_layout as D

SOURCE_SHA='4d30f693ec685e06ff975be9f5d5ed42e0f8fde13674292b11ac26f3ce222621'
NAME='SRW-Z3-PS3-RPCS3-v5-dialogue-links-update.zip'
ENTRY='PS3_GAME/USRDIR/EBOOT.BIN'
GUIDE='''# RPCS3 v5: dialogue link backgrounds

For the installed v4 English build only. Keeps its backlog, name, menu, DOB
and date-centering fixes. The only replacement is EBOOT.BIN, not game assets.
Not an installer for physical PS3 or Vita.

Close RPCS3 completely. Keep a copy of the old EBOOT.BIN outside the game
folder, then replace game/PS3_GAME/USRDIR/EBOOT.BIN with this ZIP's file.
Do not delete the install cache: no CPK/archive content changed. Do not touch
saves, fonts, authentication files or the other game files.

Select each of Destruction Incident and Regeneration War in dialogue,
switch to the speaker name, open/return from a linked entry, then check the
same selections in backlog. Also check a later scene and a date card.
Automated native-instruction tests pass; an in-game visual retest is required.
To roll back, close RPCS3 and restore the old EBOOT.BIN. Nothing is installed
automatically by this builder.
'''


def patch(original):
    assert hashlib.sha256(original).hexdigest()==SOURCE_SHA,'Requires pinned v4 EBOOT'
    changed=bytearray(original); ranges=S.apply(changed,eboot._segments(changed))
    allowed={i for lo,hi in ranges for i in range(lo,hi)}
    assert len(changed)==len(original)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(original,changed)))
    L.check(changed)
    mapping=json.loads((ROOT/'work/build_0.6.12_approved_subtitle/pairs.json').read_text())
    D.check(changed,mapping)
    return bytes(changed),ranges


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'game'/ENTRY)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--write',action='store_true')
    args=ap.parse_args();out=args.output.resolve()
    assert (ROOT/'work').resolve() in out.parents and not out.exists(),'Use a NEW work subdirectory'
    original=args.source.read_bytes();changed,ranges=patch(original)
    digest=lambda x:hashlib.sha256(x).hexdigest()
    report=dict(source_sha256=SOURCE_SHA,eboot_sha256=digest(changed),eboot_bytes=len(changed),
        changed_bytes=sum(a!=b for a,b in zip(original,changed)),allowed_ranges=ranges,
        archives_changed=False,install_cache_refresh_required=False,installed=False,runtime_tested=False)
    payloads={ENTRY:changed,'README-INSTALL.md':GUIDE.encode(),
              'BUILD_AUDIT.json':(json.dumps(report,indent=2)+'\n').encode()}
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in payloads.items():
            entry=zipfile.ZipInfo(name,(2026,9,17,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,data,compresslevel=9)
    zipped=stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(zipped)) as z:
        assert z.testzip() is None
        for name,data in payloads.items():assert z.read(name)==data
    report.update(zip_sha256=digest(zipped),zip_bytes=len(zipped))
    print(json.dumps(report,indent=2))
    if not args.write:print('DRY RUN: no files written.');return
    out.mkdir(parents=True)
    for name,data in ((NAME,zipped),('EBOOT.BIN',changed),('README-INSTALL.md',GUIDE.encode()),
                      ('BUILD_AUDIT.json',(json.dumps(report,indent=2)+'\n').encode())):
        with (out/name).open('xb') as f:f.write(data)
        assert (out/name).read_bytes()==data
    assert args.source.read_bytes()==original


if __name__=='__main__':main()
