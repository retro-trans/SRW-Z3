"""Package test16's changed files for physical-Vita rePatch (no installation).

Requires a console-dumped self_auth.bin for a hardware-test package. An explicit
--allow-incomplete produces a clearly named staging ZIP, NOT a ready-to-use patch.
No license, firmware, plugins, saves, original modules or sce_sys are packaged.
The auth dump is never packaged raw: only its authority ID and capability/
attribute fields are retained; padding and the shared-secret region are zeroed.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import struct
import sys
import zipfile

from build_install_zip import check_output, hash_file, hash_stream, safe_name
from self_decrypt import ROOT, make_fself, parse, require, take
from repatch_auth import validate_auth, sanitize_auth

TITLE = 'PCSG00264'
PREFIX = 'rePatch/' + TITLE + '/'
SOURCE = ROOT / 'work/vita/english_vwf_test_16'
SOURCE_ZIP = 'SRW-Z3-Vita-English-VWF-test-16.zip'
ZIP_SHA = '3a44d8f901af3f9aceab19d9ef44612568e00b59686985cd76ef21aa6b2b6ce8'
AUDIT_SHA = '48255815fe557a0914e89c41d37ccff2e78428574666b426c94c1dccf6f86800'
BASE_AUDIT_SHA = 'c124078bc65a6a5e92d747290b3a5979aab6117b0ad6be3bc112b0be25cb2392'
MODULES = {'sce_module/' + n + '.suprx' for n in
           ('libc', 'libface', 'libfios2', 'libsmart', 'libult')}


def payload_name(name):
    safe_name(name)
    require(name in ('eboot.bin', 'self_auth.bin') or
            (name.startswith(('DATA/', 'CommonData/')) and
             name.lower().endswith(('.cpk', '.bin'))),
            'Not an allowed rePatch payload: ' + name)
    return PREFIX + name


def select_files(current, base):
    require(set(current) == set(base), 'Source and base inventories differ')
    require(len({n.lower() for n in current}) == len(current), 'Case collision')
    selected = {}
    for name, row in current.items():
        safe_name(name)
        if row['sha256'] == base[name]['sha256']:
            require(row['bytes'] == base[name]['bytes'], 'Unchanged size mismatch')
            continue
        if name in MODULES:
            continue  # Original encrypted game supplies these unmodified modules.
        payload_name(name)  # Fail closed for any changed metadata or unknown file.
        selected[name] = dict(bytes=row['bytes'], sha256=row['sha256'],
                              original_sha256=base[name]['sha256'])
    require('eboot.bin' in selected, 'Missing translated executable')
    return selected


def inspect_eboot(data):
    info = parse(data)
    require(info['sdk'] == 0xc0 and info['ai'][2] == 8, 'Not an APP fSELF')
    segments = {}
    for index, (ph, si) in enumerate(zip(info['phdrs'], info['infos'])):
        require(si[2:] == (1, 2) and si[1] == ph[4], 'Not a plain complete segment')
        require(ph[0] != 1 or (ph[5] >= ph[4] and ph[6] & 3 != 3),
                'Invalid memory size or writable/executable load segment')
        segments[index] = take(data, si[0], si[1])
    require(make_fself(info, segments) == data, 'Unexpected executable wrapper')
    return dict(authid=info['ai'][0], segment_bytes_preserved=True,
                segment_sha256=[hashlib.sha256(segments[i]).hexdigest()
                                for i in range(len(segments))],
                wrapper='unchanged test16 plain SELF; physical loader untested')


def write_entry(archive, name, stream, expected):
    entry = zipfile.ZipInfo(name, (2026, 9, 15, 0, 0, 0))
    entry.compress_type = zipfile.ZIP_DEFLATED
    entry.external_attr = 0o100644 << 16
    entry.file_size = expected['bytes']
    digest, size = hashlib.sha256(), 0
    with archive.open(entry, 'w', force_zip64=entry.file_size >= 2**31) as out:
        while True:
            chunk = stream.read(4 * 1024**2)
            if not chunk:
                break
            out.write(chunk)
            digest.update(chunk)
            size += len(chunk)
    require((size, digest.hexdigest()) == (expected['bytes'], expected['sha256']),
            'Source changed or hash mismatch: ' + name)


def verify(path, entries):
    with zipfile.ZipFile(str(path)) as archive:
        require(len(archive.infolist()) == len(entries) and
                set(archive.namelist()) == set(entries), 'ZIP inventory mismatch')
        for name, expected in entries.items():
            entry = archive.getinfo(name)
            require(not entry.flag_bits & 1, 'Encrypted ZIP entry')
            with archive.open(entry) as stream:
                result = hash_stream(stream)  # CRC also checked through EOF.
            require(result == (expected['bytes'], expected['sha256']),
                    'ZIP read-back failed: ' + name)
        if PREFIX + 'self_auth.bin' in entries:
            auth = archive.read(PREFIX + 'self_auth.bin')
            require(len(auth) == 0x90 and not any(auth[8:16] + auth[0x50:]),
                    'Unsanitized authentication data in ZIP')
            require(PREFIX + 'eboot.bin' in entries, 'Auth without matching executable')
            executable = inspect_eboot(archive.read(PREFIX + 'eboot.bin'))
            validate_auth(auth, executable['authid'])


def blob_row(data):
    return dict(bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def build(output, self_auth=None, allow_incomplete=False, write=False):
    output = check_output(output)
    require(self_auth is not None or allow_incomplete,
            'Supply --self-auth from your Vita, or explicitly use --allow-incomplete')
    audit_path = SOURCE / 'BUILD_AUDIT.json'
    base_path = ROOT / 'work/vita/decryption_audit.json'
    require(hash_file(audit_path)[1] == AUDIT_SHA, 'Source audit pin mismatch')
    require(hash_file(base_path)[1] == BASE_AUDIT_SHA, 'Base audit pin mismatch')
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    base = json.loads(base_path.read_text(encoding='utf-8'))
    require(audit['title_id'] == base['title_id'] == TITLE and
            audit['app_version'] == base['app_version'] == '01.00', 'Wrong game version')
    require(len(audit['files']) == 589, 'Unexpected source inventory')
    selected = select_files(audit['files'], base['files'])
    require(len(selected) == 120, 'Unexpected test16 patch inventory')
    source_zip = SOURCE / SOURCE_ZIP
    print('Checking pinned test16 source ZIP...', flush=True)
    require(hash_file(source_zip) == (1872598616, ZIP_SHA), 'Source ZIP pin mismatch')
    with zipfile.ZipFile(str(source_zip)) as source:
        names = {TITLE + '/' + n for n in audit['files']}
        require(len(source.infolist()) == len(names) and set(source.namelist()) == names,
                'Source ZIP inventory mismatch')
        eboot = source.read(TITLE + '/eboot.bin')
        require(blob_row(eboot) == {k: selected['eboot.bin'][k] for k in ('bytes', 'sha256')},
                'Executable hash mismatch')
        executable = inspect_eboot(eboot)
        auth = None
        if self_auth is not None:
            auth, selected['self_auth.bin'] = sanitize_auth(
                self_auth.read_bytes(), executable['authid'])
        status = 'hardware_test_candidate' if auth is not None else 'incomplete_missing_self_auth'
        name = ('SRW-Z3-Vita-rePatch-test16-' +
                ('hardware-test.zip' if auth is not None else 'NEEDS-SELF-AUTH.zip'))
        manifest = dict(schema=2, build='vita-repatch-test16-02', title_id=TITLE,
                        app_version='01.00', status=status, physical_vita_tested=False,
                        required_destination='ux0:rePatch/PCSG00264/',
                        missing_files=[] if auth is not None else ['self_auth.bin'],
                        source_zip_sha256=ZIP_SHA, source_audit_sha256=AUDIT_SHA,
                        base_audit_sha256=BASE_AUDIT_SHA, executable=executable,
                        payload_bytes=sum(v['bytes'] for v in selected.values()),
                        excluded='original modules, unchanged files, sce_sys, licenses, '
                                 'firmware, plugins, saves', files=selected)
        print('Status:', status, '| payload files:', len(selected),
              '| expanded bytes:', manifest['payload_bytes'], flush=True)
        if not write:
            print('Dry run passed; no output written.')
            return manifest
        warning = ('# INCOMPLETE: DO NOT INSTALL YET\n\nThis ZIP lacks self_auth.bin. '
                   'Complete the preparation steps below first.\n\n' if auth is None else
                   '# HARDWARE TEST CANDIDATE: NOT CONSOLE-VERIFIED\n\n')
        guide = warning + (ROOT / 'platforms/vita/REPATCH_INSTALL.md').read_text(encoding='utf-8')
        extras = {'README-INSTALL.md': guide.encode('utf-8'),
                  'FILES.json': (json.dumps(manifest, indent=2) + '\n').encode('utf-8')}
        entries = {payload_name(n): row for n, row in selected.items()}
        entries.update({n: blob_row(b) for n, b in extras.items()})
        output.mkdir()
        partial = output / (name + '.partial')
        with zipfile.ZipFile(str(partial), 'x', compression=zipfile.ZIP_DEFLATED,
                             compresslevel=6, allowZip64=True) as dest:
            for index, (n, row) in enumerate(sorted(selected.items()), 1):
                stream = io.BytesIO(auth) if n == 'self_auth.bin' else source.open(TITLE + '/' + n)
                with stream:
                    write_entry(dest, payload_name(n), stream, row)
                if index % 25 == 0:
                    print('Packaged:', index, '/', len(selected), flush=True)
            for n, data in extras.items():
                write_entry(dest, n, io.BytesIO(data), entries[n])
        verify(partial, entries)
        target = output / name
        partial.rename(target)
        size, sha = hash_file(target)
        manifest['zip'] = dict(name=name, bytes=size, sha256=sha)
        manifest['verification'] = 'Every packaged file read back: size, SHA256, CRC'
        (output / 'BUILD_AUDIT.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        (output / 'README-INSTALL.md').write_text(guide, encoding='utf-8')
        (output / (name + '.sha256')).write_text(sha + '  ' + name + '\n', encoding='ascii')
        print('VERIFIED:', target, '\nBytes:', size, '\nSHA256:', sha, flush=True)
        return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--self-auth', type=Path)
    parser.add_argument('--allow-incomplete', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    build(args.output, args.self_auth, args.allow_incomplete, args.write)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print('BUILD FAILED:', str(exc), file=sys.stderr)
        sys.exit(1)
