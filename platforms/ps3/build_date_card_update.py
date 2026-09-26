"""Cumulative older-RPCS3 v4 update: v3 link/menu fixes plus all date cards.

Dry-run by default. Does not install or modify any original game file.
"""
import argparse,hashlib,io,json,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_link_background_update as V3
import date_card_layout as D

V3_SHA='fe55a5e284096a1ba7a18684e634d490adc97c274283379fbd11860991f3fa97'
V3_UI_SHA='9f979073c15756d5adfdcd9343ecf215cc36a87f759cb539c643cadb794d5349'
NAME='SRW-Z3-PS3-RPCS3-v4-date-center-update.zip'
GUIDE='''# RPCS3 v4: centered date cards, plus v3 highlights and startup menus

For the inspected older English RPCS3 build and its v1/v2/v3 updates only.
NOT a physical PS3 SELF/ISO or a Vita installer. No installation is automatic.

All 77 translated full-screen date cards are centered using rendered width.
Date values, wording, font size, vertical position, fades and timing are kept.
Includes v3 name/term highlights, scenario-selection artwork and DOB format.

Close RPCS3 completely. Back up these two files outside the game folder:
- PS3_GAME/USRDIR/EBOOT.BIN
- PS3_GAME/USRDIR/DATA/AIDDATA/AIDDATAPACK.CPK

Check the input hashes against BUILD_AUDIT.json. If they are a different
release, do not install this patch. Copy BOTH matching files from the ZIP into
E:/Projects/SRW Z3/game/, preserving the paths above. Keep all other files.
Do not delete/reinstall the game or overwrite saves or fonts.

Restart and check the April 10 date card and later short/long dates. Confirm
the sentence is centered horizontally with the same font and vertical level.
Also retest v3 dialogue/backlog links and scenario menus. Automated tests
pass; in-game visual confirmation is still pending.

Rollback: close RPCS3 and restore both backed-up files. Saves are unaffected.
'''


def patch(original,mapping):
    if V3.digest(original)==V3_SHA:base=original;ranges=[]
    else:base,ranges,_=V3.patch(original)
    changed,extra=D.apply(base,mapping);ranges+=extra
    allowed={i for start,end in ranges for i in range(start,end)}
    assert len(changed)==len(original)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(original,changed)))
    return changed,ranges


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source',type=Path,default=ROOT/'game/PS3_GAME/USRDIR/EBOOT.BIN')
    ap.add_argument('--ui-source',type=Path,default=ROOT/'game'/V3.UI_PATH)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--write',action='store_true')
    args=ap.parse_args();out=args.output.resolve()
    if out.exists() or (ROOT/'work').resolve() not in out.parents:raise ValueError('Use a NEW directory under work')
    mapping=json.loads((ROOT/'work/build_0.6.12_approved_subtitle/pairs.json').read_text())
    original=args.source.read_bytes();ui_source=args.ui_source.read_bytes()
    changed,ranges=patch(original,mapping)
    if V3.digest(ui_source)==V3_UI_SHA:ui=ui_source
    else:ui,_=V3.patch_ui(args.ui_source)
    report=dict(source_sha256=V3.digest(original),eboot_sha256=V3.digest(changed),eboot_bytes=len(changed),
        ui_source_sha256=V3.digest(ui_source),ui_sha256=V3.digest(ui),ui_bytes=len(ui),
        changed_executable_bytes=sum(a!=b for a,b in zip(original,changed)),allowed_ranges=ranges,
        date_cards=77,native_center=640,native_y=340,native_size=40,installed=False,runtime_tested=False)
    stream=io.BytesIO()
    payloads={'PS3_GAME/USRDIR/EBOOT.BIN':changed,V3.UI_PATH:ui,'README-INSTALL.md':GUIDE.encode(),
              'BUILD_AUDIT.json':(json.dumps(report,indent=2)+'\n').encode()}
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in payloads.items():
            entry=zipfile.ZipInfo(name,(2026,9,17,0,0,0));entry.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(entry,data,compresslevel=9)
    zipped=stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(zipped)) as z:
        assert z.testzip() is None
        for name,data in payloads.items():assert z.read(name)==data
    report.update(zip_sha256=V3.digest(zipped),zip_bytes=len(zipped))
    print(json.dumps(report,indent=2))
    if not args.write:print('DRY RUN: no files written.');return
    out.mkdir(parents=True)
    for name,data in ((NAME,zipped),('README-INSTALL.md',GUIDE.encode()),('BUILD_AUDIT.json',(json.dumps(report,indent=2)+'\n').encode())):
        with (out/name).open('xb') as f:f.write(data)
        assert (out/name).read_bytes()==data
    assert args.source.read_bytes()==original and args.ui_source.read_bytes()==ui_source
    print('Saved verified update:',out)


if __name__=='__main__':main()
