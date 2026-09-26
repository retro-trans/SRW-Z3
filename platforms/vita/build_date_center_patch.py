"""Date-card-only EBOOT update for the verified test16 Vita patch; no install.

Dry-run first. A NEW work/vita output directory is required for --write.
Uses the already-sanitized test16 package; never reads self_auth.bin or saves.
"""
import argparse
import io
import json
from pathlib import Path
import zipfile

from category_port import ROOT, require, digest
from build_install_zip import hash_file
import date_card_centering
from build_repatch import inspect_eboot

SOURCE = ROOT/'work/vita/english_repatch_test16_02/SRW-Z3-Vita-rePatch-test16-hardware-test.zip'
SOURCE_SHA = '8dd8d49e9de652edfb6601959965f5e54b5b0cf92457dd34606d832ce0c4f486'
ENTRY = 'rePatch/PCSG00264/eboot.bin'
ZIP_NAME = 'SRW-Z3-Vita-test16-date-centering-update.zip'
GUIDE = '''# Vita test16 date-card centering update

This is a small update to the already-working English test16 patch, NOT a full
game or standalone patch. It changes only the date-card draw call and a small
code stub. All 77 dates use English-width centering in both native font modes.
Wording, dates, vertical position, font size, save files and other UI are unchanged.
The earlier defeat-condition, Z Chips and menu-alignment reports are NOT fixed
by this date-only update. CPU verification passed; in-game visual retest is needed.

## Physical Vita (existing working test16 rePatch required)

1. Fully close the game. Back up your current ux0:rePatch/PCSG00264/eboot.bin
   somewhere outside the active rePatch directory.
2. Extract the ZIP. Copy rePatch/PCSG00264/eboot.bin to
   ux0:rePatch/PCSG00264/eboot.bin, replacing ONLY that file.
3. Keep your existing self_auth.bin and all other English patch files unchanged.
   Do not copy to ux0:app or ux0:patch. This is not a VPK.
4. Start the game and check April 27 plus a few other date cards. Text should
   have equal left/right margins at the same vertical position.

## Vita3K (existing working test16 English installation required)

With Vita3K fully closed, back up eboot.bin in its configured
ux0/app/PCSG00264 folder, then replace ONLY that eboot.bin with the one from
the ZIP. The ZIP's rePatch directory is a physical-Vita layout, not a Vita3K
automatic installer. Do not copy self_auth.bin or overwrite savedata.

## Rollback

Close the game/emulator and restore the eboot.bin backup. No other file needs
to change. Do not apply this update over a newer or differently patched build;
it would replace that executable with the test16-based version.
'''


def plan():
    require(hash_file(SOURCE)[1] == SOURCE_SHA, 'Source test16 rePatch package changed')
    with zipfile.ZipFile(SOURCE) as archive:
        original = archive.read(ENTRY)
    inspect_eboot(original)
    changed, audit = date_card_centering.apply(original, 0x812B5E38)
    inspect_eboot(changed)
    report = dict(kind='test16-date-card-centering-only', source_zip_sha256=SOURCE_SHA,
                  source_eboot_sha256=digest(original), eboot_sha256=digest(changed),
                  eboot_bytes=len(changed), patch=audit, dates=77, installed=False,
                  runtime_tested=False, no_auth_license_save_or_asset_changes=True)
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, payload in ((ENTRY, changed), ('README-INSTALL.md', GUIDE.encode('utf-8'))):
            member = zipfile.ZipInfo(name, (2026, 9, 17, 0, 0, 0))
            member.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(member, payload, compresslevel=9)
    data = stream.getvalue()
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        require(set(archive.namelist()) == {ENTRY, 'README-INSTALL.md'}, 'Unexpected ZIP contents')
        require(archive.read(ENTRY) == changed and archive.testzip() is None, 'ZIP read-back failed')
    report['zip'] = dict(name=ZIP_NAME, bytes=len(data), sha256=digest(data))
    return changed, data, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    out = args.output.resolve()
    require((ROOT/'work/vita').resolve() in out.parents and not out.exists(),
            'Use a NEW work/vita subdirectory')
    changed, zipped, report = plan()
    print(json.dumps(report, indent=2))
    print('Only date-card caller and reserved code change; original package is untouched.')
    if not args.write:
        print('DRY RUN: inspect the plan, then add --write. No files written.')
        return
    out.mkdir(parents=True)
    for name, data in ((ZIP_NAME, zipped), ('eboot.bin', changed),
                       ('README-INSTALL.md', GUIDE.encode('utf-8')),
                       ('BUILD_AUDIT.json', (json.dumps(report, indent=2)+'\n').encode('utf-8'))):
        with (out/name).open('xb') as stream:
            stream.write(data)
        require((out/name).read_bytes() == data, 'Disk read-back failed: '+name)
    print('Saved verified date-only update:', out)


if __name__ == '__main__':
    main()
