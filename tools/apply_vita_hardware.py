"""Create a NEW physical-Vita rePatch overlay from original files; dry-run default.

No firmware, keys or raw authentication data are distributed. This is a
hardware test candidate, not a Vita3K installer or a signed game package.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import zipfile

from apply_vita_release import matches, safe, sha
from repatch_auth import require, sanitize_auth

TITLE = 'PCSG00264'


def allowed(name):
    safe(Path.cwd(), name)
    require(name == 'eboot.bin' or
            (name.startswith(('DATA/', 'CommonData/')) and
             name.lower().endswith(('.bin', '.cpk'))),
            'Not an allowed hardware patch payload: ' + name)


def separate(output, other):
    return output != other and other not in output.parents and output not in other.parents


def read_manifest(package):
    manifest = json.loads((package / 'manifest.json').read_text(encoding='utf-8'))
    require(manifest['schema'] == 1 and manifest['kind'] == 'vita-hardware-repatch-deltas'
            and manifest['title_id'] == TITLE and manifest['app_version'] == '01.00',
            'Unsupported hardware patch manifest')
    records = manifest['files']
    require('eboot.bin' in records and len(records) == 120, 'Incomplete hardware patch inventory')
    require(len({n.lower() for n in records}) == len(records), 'Case-colliding files')
    patch_names = set()
    for name, record in records.items():
        allowed(name)
        require(record['patch']['name'] == 'patches/' + name + '.xdelta', 'Unexpected delta path')
        patch_names.add(record['patch']['name'])
    require(len(patch_names) == len(records), 'Duplicate delta files')
    return manifest


def executable_authid(data):
    require(len(data) >= 0x80 and data[:4] == b'SCE\0', 'Not a SELF executable')
    offset = struct.unpack_from('<Q', data, 0x38)[0]
    require(0x80 <= offset <= min(4096, len(data)) - 32, 'Invalid SELF authority offset')
    return struct.unpack_from('<Q', data, offset)[0]


def apply(package, source, output, self_auth, xdelta, write=False):
    package, source, output, self_auth = [Path(p).resolve() for p in
                                        (package, source, output, self_auth)]
    require(source.is_dir(), 'Original game source folder is missing')
    require(not output.exists() and separate(output, source) and separate(output, package),
            'Output must be a NEW folder separate from the source and patch package')
    require(output not in self_auth.parents, 'Output cannot contain the authentication input')
    manifest = read_manifest(package)
    records = manifest['files']
    for name, record in records.items():
        require(matches(safe(source, name), record['source']),
                'Wrong source file: ' + name + '; requires original PFS-decrypted PCSG00264 v01.00')
        require(matches(safe(package, record['patch']['name']), record['patch']),
                'Damaged delta file: ' + name)
    # Read only. Do not print raw bytes or use the raw dump in any output.
    raw_auth = self_auth.read_bytes()
    auth, auth_info = sanitize_auth(raw_auth, manifest['program_authority_id'])
    guide = (package / 'README.md').read_bytes()
    print('Verified 120 original files and 120 hardware deltas; authentication structure matches.', flush=True)
    print('Output: rePatch/PCSG00264 with 120 patched files plus sanitized self_auth.bin.', flush=True)
    print('Excludes emulator modules, unchanged game data, licenses, firmware and saves.', flush=True)
    print('Hardware test candidate: this exact build still needs a real-Vita load/save test.', flush=True)
    if not write:
        print('DRY RUN: no files created. Add --write after checking the plan.', flush=True)
        return manifest
    output.mkdir(parents=True)
    tree = output / 'rePatch' / TITLE
    for index, (name, record) in enumerate(records.items(), 1):
        dest = safe(tree, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([str(xdelta), '-d', '-s', str(safe(source, name)),
                        str(safe(package, record['patch']['name'])), str(dest)], check=True)
        require(matches(dest, record['target']), 'Output mismatch; do NOT use this output: ' + name)
        if index % 25 == 0:
            print('Verified patched files:', index, '/ 120', flush=True)
    require(executable_authid((tree / 'eboot.bin').read_bytes()) == manifest['program_authority_id'],
            'Output executable and authentication do not match')
    with (tree / 'self_auth.bin').open('xb') as stream:
        stream.write(auth)
    require((tree / 'self_auth.bin').read_bytes() == auth and not any(auth[8:16] + auth[80:]),
            'Sanitized authentication read-back failed')
    require(self_auth.read_bytes() == raw_auth, 'Authentication input changed; do NOT use output')
    for name, record in records.items():
        require(matches(safe(source, name), record['source']), 'Source changed; do NOT use output')
    files = {name: record['target'] for name, record in records.items()}
    files['self_auth.bin'] = dict(bytes=len(auth), sha256=hashlib.sha256(auth).hexdigest())
    report = dict(title_id=TITLE, app_version='01.00', release='0.6.14',
                  status='hardware_test_candidate', physical_vita_tested=False,
                  destination='ux0:rePatch/PCSG00264/', missing_files=[],
                  authentication=auth_info, files=files, originals_unchanged=True)
    extras = {'README-INSTALL.md': guide,
              'FILES.json': (json.dumps(report, indent=2) + '\n').encode('utf-8')}
    for name, data in extras.items():
        with (output / name).open('xb') as stream:
            stream.write(data)
    zpath = output / 'SRW-Z3-Vita-rePatch-0.6.14-hardware-test.zip'
    with zipfile.ZipFile(str(zpath), 'x', zipfile.ZIP_DEFLATED) as archive:
        for name in files:
            archive.write(str(safe(tree, name)), 'rePatch/' + TITLE + '/' + name)
        for name, data in extras.items():
            archive.writestr(name, data)
    with zipfile.ZipFile(str(zpath)) as archive:
        require(len(archive.infolist()) == len(files) + len(extras), 'Wrong ZIP inventory')
        for name, row in files.items():
            data = archive.read('rePatch/' + TITLE + '/' + name)
            require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                    'ZIP content/hash mismatch')
        for name, data in extras.items():
            require(archive.read(name) == data, 'ZIP instructions/manifest mismatch')
    print('SUCCESS: all 121 payloads and ZIP hashes verified. Original inputs unchanged.', flush=True)
    print('Copy the generated rePatch/PCSG00264 folder with VitaShell; do not install as a VPK.', flush=True)
    print('Completed local hardware ZIP:', zpath, flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--self-auth', type=Path, required=True)
    parser.add_argument('--xdelta', default='xdelta3')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    try:
        apply(Path(__file__).resolve().parent, args.source, args.output,
              args.self_auth, args.xdelta, args.write)
    except (ValueError, OSError, KeyError, subprocess.CalledProcessError, zipfile.BadZipFile) as error:
        parser.exit(1, 'STOPPED: ' + str(error) + '\nDo not install any incomplete output.\n')


if __name__ == '__main__':
    main()
