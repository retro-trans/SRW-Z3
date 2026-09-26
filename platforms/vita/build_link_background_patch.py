"""Test16 link-background update retaining date centering. Dry-run first; no install."""
import argparse
import io
import json
from pathlib import Path
import zipfile
from category_port import ROOT, require, digest
from build_repatch import inspect_eboot
import build_date_center_patch as dates
import link_background

ZIP_NAME='SRW-Z3-Vita-test16-link-background-v4-update.zip'
GUIDE='''# Vita test16 link-background v4 update (includes date centering)

For the existing working English test16 patch, with or without the earlier
date-centering-only update. Not a standalone game, VPK, or newer-build update.

V4 supplies the current scene for dialogue link registration when no explicit
backlog scene is set. V3 silently omitted dialogue backgrounds in that case.
Explicit backlog scenes, geometry and navigation are unchanged.
V3 fixes the separate speaker-name widget in dialogue/backlog and translates
term labels for native ID comparison before matching rendered geometry.
V2 missed names entirely and could hide main-dialogue terms with mismatched IDs.
Backlog term width correction is retained. Name widths use the existing Latin
measurement helper and the name widget's own font size; unknown Japanese uses
native fallback. Term geometry uses the actual rendered style height.
Record formats, selection/navigation, wording and colors stay unchanged.
All 77 date cards retain
the previous centering correction. In-game visual retest is still required.
Defeat-condition Japanese, Z Chips footer and menu alignment remain pending.

## Physical Vita

1. Close the game completely. Back up ux0:rePatch/PCSG00264/eboot.bin elsewhere.
2. Extract the ZIP; copy ONLY rePatch/PCSG00264/eboot.bin to the matching
   ux0:rePatch/PCSG00264/eboot.bin, replacing that file.
3. Keep existing self_auth.bin and all other working test16 patch files.
   Do not copy into ux0:app or ux0:patch and do not install as a VPK.

## Vita3K

Close Vita3K completely. Back up eboot.bin in its configured ux0/app/PCSG00264
folder, then replace ONLY that file with the eboot.bin inside the ZIP.
The ZIP's rePatch directory is a physical-Vita layout, not an emulator installer.
Do not copy authentication files or touch savedata.

## Check and rollback

Check Kei/Kira and both Destruction Incident/Regeneration War in dialogue AND
backlog, including switching names to terms. Select ZEXIS, then Alto: boxes should
end at its linked text instead of extending into the following word/blank area.
Check another name/term, open its library entry, navigate back, and check a
date card. Close the game and restore your eboot.bin backup to undo the update.
Do not apply to a newer/different build: it replaces the executable with a
test16-based version. Nothing is installed automatically.
'''


def plan():
    dated, _, previous=dates.plan()
    changed, links=link_background.apply(dated)
    inspect_eboot(changed)
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,payload in ((dates.ENTRY,changed),('README-INSTALL.md',GUIDE.encode('utf-8'))):
            member=zipfile.ZipInfo(name,(2026,9,17,0,0,0));member.compress_type=zipfile.ZIP_DEFLATED
            archive.writestr(member,payload,compresslevel=9)
    zipped=stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(zipped)) as archive:
        require(set(archive.namelist())=={dates.ENTRY,'README-INSTALL.md'},'Unexpected ZIP content')
        require(archive.read(dates.ENTRY)==changed and archive.testzip() is None,'ZIP read-back failed')
    report=dict(kind='test16-link-background-plus-date-centering',
        source_zip_sha256=dates.SOURCE_SHA,source_eboot_sha256=previous['source_eboot_sha256'],
        eboot_sha256=digest(changed),eboot_bytes=len(changed),link_background=links,
        date_centering=previous['patch'],installed=False,runtime_tested=False,
        no_auth_license_save_or_asset_changes=True,
        zip=dict(name=ZIP_NAME,bytes=len(zipped),sha256=digest(zipped)))
    return changed,zipped,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--write',action='store_true');args=parser.parse_args()
    out=args.output.resolve()
    require((ROOT/'work/vita').resolve() in out.parents and not out.exists(),'Use a NEW work/vita subdirectory')
    changed,zipped,report=plan();print(json.dumps(report,indent=2))
    if not args.write:
        print('DRY RUN: no files written. Inspect before --write.');return
    out.mkdir(parents=True)
    for name,data in ((ZIP_NAME,zipped),('eboot.bin',changed),('README-INSTALL.md',GUIDE.encode('utf-8')),
                      ('BUILD_AUDIT.json',(json.dumps(report,indent=2)+'\n').encode('utf-8'))):
        with (out/name).open('xb') as stream:stream.write(data)
        require((out/name).read_bytes()==data,'Disk read-back failed')
    print('Saved verified link-background update:',out)


if __name__=='__main__':main()
