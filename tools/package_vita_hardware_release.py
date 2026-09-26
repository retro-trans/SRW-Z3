"""Package frozen 0.6.14 hardware deltas only. No auth/game payloads uploaded."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'platforms/vita'))
import build_repatch as hardware
from apply_vita_release import matches, safe, sha

ORIGINAL_ZIP = ROOT / 'work/release_0.6.14/SRW-Z3-Vita3K-0.6.14-from-original.zip'
ORIGINAL_SHA = 'ef55294e4758ccac1e67accca602ca503b22804bb90fa710a97ddbeeecac858e'
CURRENT_EBOOT = ROOT / 'work/vita/link_background_test16_04/eboot.bin'
EBOOT_SHA = 'f79fcef07290bbc5c9b4c191c7109514fc7fc97ec191bfebb3be0e77de65ae0d'
NAME = 'SRW-Z3-Vita-Hardware-0.6.14-from-original'


def build(output, write=False):
    output = output.resolve()
    hardware.require((ROOT / 'work').resolve() in output.parents and not output.exists(),
                     'Choose a NEW output directory under work/')
    hardware.require(sha(ORIGINAL_ZIP) == ORIGINAL_SHA, 'Frozen Vita delta ZIP mismatch')
    hardware.require(sha(CURRENT_EBOOT) == EBOOT_SHA, 'Current executable mismatch')
    executable = hardware.inspect_eboot(CURRENT_EBOOT.read_bytes())
    with zipfile.ZipFile(ORIGINAL_ZIP) as source:
        original = json.loads(source.read('manifest.json'))
        current = {n: row['target'] for n, row in original['files'].items()}
        base = {n: row['source'] for n, row in original['files'].items()}
        selected = hardware.select_files(current, base)
        hardware.require(len(selected) == 120, 'Unexpected hardware payload count')
        manifest = dict(schema=1, kind='vita-hardware-repatch-deltas', title_id='PCSG00264',
                        app_version='01.00', target_label='0.6.14 (test16-linkfix-v4)',
                        program_authority_id=executable['authid'], physical_vita_tested=False,
                        self_auth_included=False, files={n: original['files'][n] for n in selected})
        blobs = {}
        for name, row in manifest['files'].items():
            patch = row['patch']
            data = source.read(patch['name'])
            hardware.require(len(data) == patch['bytes'] and hashlib.sha256(data).hexdigest() == patch['sha256'],
                             'Frozen delta hash mismatch: ' + name)
            blobs[patch['name']] = data
    for dest, src in {
            'apply_vita_hardware.py': ROOT / 'tools/apply_vita_hardware.py',
            'apply_vita_release.py': ROOT / 'tools/apply_vita_release.py',
            'repatch_auth.py': ROOT / 'platforms/vita/repatch_auth.py',
            'README.md': ROOT / 'docs/VITA_HARDWARE_RELEASE_0.6.14.md'}.items():
        blobs[dest] = src.read_bytes()
    blobs['manifest.json'] = (json.dumps(manifest, indent=2) + '\n').encode('utf-8')
    print('Hardware release: 120 hash-locked deltas, scripts, guide and manifest.', flush=True)
    print('Excludes all auth, raw game files, emulator modules, metadata, saves, firmware and keys.', flush=True)
    print('Target matches current 0.6.14 Vita content. Hardware runtime remains unverified.', flush=True)
    print('Output:', output / (NAME + '.zip'), flush=True)
    if not write:
        print('DRY RUN: no output written.', flush=True)
        return manifest
    output.mkdir(parents=True)
    staging = output / NAME
    staging.mkdir()
    for name, data in blobs.items():
        target = safe(staging, name)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
    archive_path = output / (NAME + '.zip')
    with zipfile.ZipFile(archive_path, 'x', zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(blobs.items()):
            archive.writestr(name, data)
    with zipfile.ZipFile(archive_path) as archive:
        hardware.require(len(archive.infolist()) == len(blobs), 'Wrong release ZIP inventory')
        for name, data in blobs.items():
            hardware.require(archive.read(name) == data, 'Release ZIP read-back failed')
    print('Verified release ZIP:', archive_path.stat().st_size, 'bytes; SHA256:', sha(archive_path), flush=True)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    build(args.output, args.write)
