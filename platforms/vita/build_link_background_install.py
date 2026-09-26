"""Full Vita3K install ZIP: pinned test16 assets plus verified link/date EBOOT.

Dry-run first. Writes only a new work/vita folder; never installs or reads auth.
"""
import argparse
import copy
import io
import json
from pathlib import Path
import zipfile

import build_install_zip as package
import build_repatch as baseline
from category_port import ROOT, require

NAME = 'SRW-Z3-Vita3K-test16-linkfix-v4-install.zip'
PATCH = ROOT/'work/vita/link_background_test16_04/eboot.bin'
PATCH_SHA = 'f79fcef07290bbc5c9b4c191c7109514fc7fc97ec191bfebb3be0e77de65ae0d'
GUIDE = '''# Vita3K installable English package: test16 + link/date fixes v4

This is a complete Vita3K game archive, not the earlier rePatch overlay.
V4 fixes missing dialogue term backgrounds by supplying the current scene
when registration has no explicit backlog scene. Backlog selection is retained.
Contains the working test16 files, with selected-link backgrounds positioned
and sized to rendered English text and all 77 date cards centered. V3 fixes
the separate speaker-name widget missed by v2 and translates term labels
during native identity comparison (v2 could hide dialogue term highlights).
CPU tests execute the real name widget and registration code, reproducing
both old failures as negative controls. Check Kei/Kira, Destruction Incident and
Regeneration War in both dialogue and backlog. Other pending translation/menu
issues are unchanged. Intended only for your own game in Vita3K, not a physical
Vita or a signed retail PKG.

1. Stop the game and back up your existing installation and savedata first.
   Savedata is under your configured Vita3K storage:
   ux0/user/<user-id>/savedata/PCSG00264 (usually user-id 00).
2. In Vita3K choose File > Install .zip, .vpk (wording may vary).
3. Select SRW-Z3-Vita3K-test16-linkfix-v4-install.zip directly; do not extract it.
4. If prompted that PCSG00264 already exists, choose reinstall/overwrite only
   after making backups. Do not delete savedata. If no overwrite option is
   offered or installation fails, cancel and report the exact message.
5. Launch PCSG00264 and select BOTH Destruction Incident and Regeneration War
   in dialogue, then switch to the speaker name. Check the same selections in
   backlog, link navigation/library entries, a later scene, and a date card.

Keep the existing Vita firmware and fonts installed. No separate Japanese PKG,
rePatch, VitaShell or self_auth.bin is required for this archive in Vita3K.
No saves, license files, auth dumps or firmware are included. Nothing is
installed automatically. Archive checks passed; this new package has not been
installed or visually tested in Vita3K yet. Keep the previous package/backups
for rollback; do not remove a working installation blindly.
'''


def plan():
    source = baseline.SOURCE/baseline.SOURCE_ZIP
    audit_path = baseline.SOURCE/'BUILD_AUDIT.json'
    require(package.hash_file(audit_path)[1] == baseline.AUDIT_SHA, 'Source audit mismatch')
    require(package.hash_file(source)[1] == baseline.ZIP_SHA, 'Source ZIP mismatch')
    require(package.hash_file(PATCH)[1] == PATCH_SHA, 'Link/date executable mismatch')
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    inventory = copy.deepcopy(audit['files'])
    require(len(inventory) == 589 and audit['title_id'] == 'PCSG00264', 'Wrong base inventory')
    package.verify_zip(source, inventory)
    changed = PATCH.read_bytes()
    baseline.inspect_eboot(changed)
    for name in inventory:
        require('self_auth.bin' not in name.lower(), 'Auth material not allowed')
    require('sce_sys/param.sfo' in inventory, 'Missing Vita3K installation metadata')
    inventory['eboot.bin'] = dict(bytes=len(changed), sha256=PATCH_SHA,
                                 change='test16 + link backgrounds + date centering')
    print('PLAN: 589 installable game files; ONLY eboot.bin differs from test16.', flush=True)
    print('Root: PCSG00264/; includes sce_sys/param.sfo and existing converted modules.', flush=True)
    print('No auth, license, firmware, saves or automatic installation.', flush=True)
    return source, changed, inventory


def write(output, source, changed, inventory):
    output.mkdir(parents=True)
    target = output/NAME
    with zipfile.ZipFile(source) as old, zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED,
                                                       compresslevel=1, allowZip64=True) as new:
        for index, name in enumerate(sorted(inventory), 1):
            path = 'PCSG00264/'+package.safe_name(name)
            entry = zipfile.ZipInfo(path, (2026, 9, 17, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            entry.file_size = inventory[name]['bytes']
            stream = io.BytesIO(changed) if name == 'eboot.bin' else old.open(path)
            with stream, new.open(entry, 'w', force_zip64=entry.file_size >= 2**31) as dest:
                while True:
                    chunk = stream.read(4*1024**2)
                    if not chunk:
                        break
                    dest.write(chunk)
            if index % 50 == 0:
                print('Packaged:', index, '/ 589', flush=True)
    package.verify_zip(target, inventory)
    size, sha = package.hash_file(target)
    report = dict(build='vita3k-test16-linkfix-install', title_id='PCSG00264',
                  source_zip_sha256=baseline.ZIP_SHA, source_audit_sha256=baseline.AUDIT_SHA,
                  executable_sha256=PATCH_SHA, changed_from_test16=['eboot.bin'],
                  zip=dict(name=NAME, bytes=size, sha256=sha), files=inventory,
                  verification='All 589 files read back: size, SHA256 and ZIP CRC',
                  installed=False, runtime_tested=False, no_auth_license_or_save_files=True)
    for name, data in [('BUILD_AUDIT.json', (json.dumps(report,indent=2)+'\n').encode()),
                       ('README-INSTALL.md',GUIDE.encode()),
                       (NAME+'.sha256',(sha+'  '+NAME+'\n').encode())]:
        with (output/name).open('xb') as f:
            f.write(data)
    print('VERIFIED:', target, '\nBytes:', size, '\nSHA256:', sha, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    output = package.check_output(args.output)
    source, changed, inventory = plan()
    if not args.write:
        print('DRY RUN: no files written. Inspect before --write.')
        return
    write(output, source, changed, inventory)


if __name__ == '__main__':
    main()
