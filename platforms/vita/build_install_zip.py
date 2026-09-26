"""Build a full Vita3K install ZIP from this user's verified decrypted base.

Dry-run by default. Only writes to a NEW work/vita subfolder with --write.
Never installs, uploads, changes source data, or includes license material.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import sys
import zipfile

from self_decrypt import ROOT, convert, require

BASE = ROOT / 'work/vita/decrypted_PCSG00264'
PILOT = ROOT / 'work/vita/english_pilot_01_checked'
NAME = 'SRW-Z3-Vita-English-pilot-01-install.zip'
SELF_NAMES = ['eboot.bin'] + ['sce_module/' + n + '.suprx' for n in
                              ('libc', 'libface', 'libfios2', 'libsmart', 'libult')]
PINS = {
    'work/vita/decryption_audit.json': 'c124078bc65a6a5e92d747290b3a5979aab6117b0ad6be3bc112b0be25cb2392',
    'work/vita/english_pilot_01_checked/BUILD_AUDIT.json': '8e0fa0124264795c8ef66e7c3572acc4b32aa7c781896773e9f9cf2d8f6b9f6b',
    'work/vita/self_reference/sce_utils.cpp': 'aa70c0dcfc912ead27abb2040cba0d9c2f3b543ecf7c5baa7c56c4459270a7d3',
    'work/vita/self_reference/sce_types.h': '97e27a59e386afba2568332eb6c6eb1f2d038fa24de88679de2b602bf820c9f1',
    'work/vita/self_reference/self.h': 'ffd3a6fd16a6a2aa9ad86541934acca2dff452b42b7ad944ef480d29826a262e',
}


def hash_stream(stream):
    h = hashlib.sha256()
    size = 0
    while True:
        chunk = stream.read(4 * 1024**2)
        if not chunk:
            break
        h.update(chunk)
        size += len(chunk)
    return size, h.hexdigest()


def hash_file(path):
    with path.open('rb') as stream:
        return hash_stream(stream)


def safe_name(name):
    p = PurePosixPath(name)
    parts = [x.lower() for x in p.parts]
    require(name and not p.is_absolute() and '\\' not in name and ':' not in name
            and all(x not in ('', '.', '..') for x in name.split('/')), 'Unsafe archive path')
    require('sce_pfs' not in parts and 'package' not in parts and
            not any(x in ('work.bin', 'license', 'licenses') or x.endswith(('.rif', '.zrif'))
                    for x in parts), 'License or encryption metadata excluded')
    return name


def check_output(path):
    path = path.resolve()
    parent = (ROOT / 'work/vita').resolve()
    require(parent in path.parents and path != parent and not path.exists(),
            'Output must be a new folder under work/vita')
    return path


def prepare(license_path, include_pilot=True):
    for path, expected in PINS.items():
        require(hash_file(ROOT / path)[1] == expected, 'Reference/audit hash mismatch: ' + path)
    audit = json.loads((ROOT / 'work/vita/decryption_audit.json').read_text())
    pilot = json.loads((PILOT / 'BUILD_AUDIT.json').read_text())
    require(audit['title_id'] == pilot['title_id'] == 'PCSG00264' and
            audit['app_version'] == pilot['app_version'] == '01.00', 'Wrong game version')
    expected = audit['files']
    actual = {p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()}
    require(actual == set(expected) and len(actual) == 589, 'Base inventory differs')
    require(len({n.lower() for n in actual}) == len(actual), 'Case-colliding source files')
    sources, inventory = {}, {}
    for i, name in enumerate(sorted(actual), 1):
        safe_name(name)
        src = BASE / name
        require(not src.is_symlink(), 'Source symlink is not allowed')
        size, sha = hash_file(src)
        require((size, sha) == (expected[name]['bytes'], expected[name]['sha256']),
                'Base file hash mismatch: ' + name)
        sources[name] = src
        inventory[name] = dict(bytes=size, sha256=sha, change='unchanged')
        if i % 100 == 0:
            print('Verified base files:', i, '/', len(actual), flush=True)
    for name, f in (pilot['files'].items() if include_pilot else []):
        require(name in actual and expected[name]['sha256'] == f['original_sha256'],
                'Patch base mismatch')
        path = PILOT / 'overlay/PCSG00264' / name
        size, sha = hash_file(path)
        require((size, sha) == (f['bytes'], f['patched_sha256']), 'Patch file mismatch')
        sources[name] = path
        inventory[name] = dict(bytes=size, sha256=sha, change='English dialogue/font')
    license_data = license_path.read_bytes()
    require(len(license_data) == 512 and b'PCSG00264' in license_data[16:64],
            'Wrong local game license')
    reference = (ROOT / 'work/vita/self_reference/sce_utils.cpp').read_text()
    executable_audit = {}
    for name in SELF_NAMES:
        transformed, result = convert((BASE / name).read_bytes(), license_data[80:96], reference)
        sources[name] = transformed
        inventory[name] = dict(bytes=len(transformed), sha256=result['patched_sha256'],
                               change='Decrypted SELF container; segment bytes preserved')
        executable_audit[name] = result
        print('Executable verified:', name, '(' + str(result['segments']) + ' segments)', flush=True)
    require(sum(v['change'] != 'unchanged' for v in inventory.values()) == (9 if include_pilot else 6),
            'Unexpected number of changed files')
    return sources, inventory, executable_audit


def write_zip(path, sources, inventory):
    with zipfile.ZipFile(str(path), 'x', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=1, allowZip64=True) as archive:
        for i, name in enumerate(sorted(sources), 1):
            entry = zipfile.ZipInfo('PCSG00264/' + safe_name(name), (2026, 9, 14, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            entry.file_size = inventory[name]['bytes']
            source = sources[name]
            stream = io.BytesIO(source) if isinstance(source, bytes) else source.open('rb')
            h, size = hashlib.sha256(), 0
            with stream, archive.open(entry, 'w', force_zip64=entry.file_size >= 2**31) as dst:
                while True:
                    chunk = stream.read(4 * 1024**2)
                    if not chunk:
                        break
                    dst.write(chunk)
                    h.update(chunk)
                    size += len(chunk)
            require(size == inventory[name]['bytes'] and h.hexdigest() == inventory[name]['sha256'],
                    'Source changed while packaging: ' + name)
            if i % 50 == 0:
                print('Packaged files:', i, '/', len(sources), flush=True)


def verify_zip(path, inventory):
    with zipfile.ZipFile(str(path)) as archive:
        require(len(archive.infolist()) == len(inventory), 'Archive entry count mismatch')
        require(set(archive.namelist()) == {'PCSG00264/' + n for n in inventory},
                'Archive inventory mismatch')
        for i, (name, f) in enumerate(sorted(inventory.items()), 1):
            safe_name(name)
            entry = archive.getinfo('PCSG00264/' + name)
            require(entry.file_size == f['bytes'] and not entry.flag_bits & 1,
                    'Incorrect or encrypted ZIP entry')
            with archive.open(entry) as stream:
                size, sha = hash_stream(stream)  # Also validates ZIP CRC to EOF.
            require((size, sha) == (f['bytes'], f['sha256']), 'ZIP read-back hash mismatch')
            if i % 100 == 0:
                print('Read-back verified:', i, '/', len(inventory), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--license', type=Path, default=Path('E:/SRWZ3/iso/work.bin'))
    ap.add_argument('--output', type=Path, default=ROOT / 'work/vita/english_pilot_01_install')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    output = check_output(args.output)
    sources, inventory, executables = prepare(args.license)
    print('Plan: 589 game files; 3 English CPKs; 6 decrypted executables; 580 unchanged.')
    print('No license, firmware, saves, installation or PS3 changes.')
    print('Expanded game bytes:', sum(f['bytes'] for f in inventory.values()))
    if not args.write:
        print('DRY RUN PASSED; no output written.')
        return
    output.mkdir()
    path = output / NAME
    write_zip(path, sources, inventory)
    verify_zip(path, inventory)
    size, sha = hash_file(path)
    result = dict(schema=1, build='vita-english-pilot-01-install', title_id='PCSG00264',
                  app_version='01.00', stage_dialogue_records=244, runtime_tested=False,
                  full_english_port=False, zip=dict(name=NAME, bytes=size, sha256=sha),
                  files=inventory, executables=executables, reference_pins=PINS,
                  verification='All 589 ZIP entries read back; SHA256, sizes and CRC passed',
                  no_license_or_key_in_package=True)
    (output / 'INSTALL_AUDIT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    (output / 'README-INSTALL.md').write_text((ROOT / 'platforms/vita/INSTALL_ZIP.md').read_text(encoding='utf-8'), encoding='utf-8')
    (output / (NAME + '.sha256')).write_text(sha + '  ' + NAME + '\n', encoding='ascii')
    print('FULL ZIP VERIFIED:', path)
    print('Bytes:', size, 'SHA256:', sha)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print('BUILD FAILED:', str(exc), file=sys.stderr)
        sys.exit(1)
