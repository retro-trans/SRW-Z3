"""Build three unsplit, controlled PS3 boot tests. Dry-run unless --write.

Uses the existing CFW-test1 ISO layout and wrapper, not a new compatibility fix.
Only creates a new folder under work; no emulator, saves or old builds changed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess

import cfw_package as c

EBOOT = '/PS3_GAME/USRDIR/EBOOT.BIN'
CLEAN_SHA256 = 'd9b198be47421c7fd8725015ef23ea20e327d0b042234516b3d48ea56415f959'
FSELF_SHA256 = 'b3bc066b39b69adff7fd59c849b14bb8754c4c306c549aa1ecd791b953799554'
NAMES = ('01-SRW-Z3-Japanese-Repacked.iso',
         '02-SRW-Z3-Japanese-CFW-Wrapper.iso',
         '03-SRW-Z3-English-0.6.13-CFW.iso')


def info(path):
    return {'bytes': path.stat().st_size, 'sha256': c.digest(path)}


def changed(before, after):
    c.require(set(before) == set(after), 'Diagnostic file inventory changed')
    return sorted(n for n in before if before[n] != after[n])


def verify_isolation(original, control, translated, replacements, previous):
    c.require(changed(original, control) == [EBOOT],
              'Wrapper control must change ONLY EBOOT.BIN')
    differences = changed(control, translated)
    c.require(EBOOT in differences and set(differences) <= set(replacements),
              'English build differs outside snapshot replacements')
    c.require(translated == previous, 'English contents differ from failing CFW-test1')
    return differences


def verify_clean_headers(original, clean):
    phoff, headers = c.elf_headers(clean)
    eoff, poff = struct.unpack_from('>QQ', original, 0x30)
    c.require(original[eoff:eoff + 64] == clean[:64], 'Clean ELF header differs from original SELF')
    c.require(original[poff:poff + len(headers) * 56] ==
              clean[phoff:phoff + len(headers) * 56], 'Clean ELF program table differs')


def extract_original(source, stage, inventory):
    expected = {}
    with source.open('rb') as stream:
        for name, entry in inventory.items():
            target = stage / c.safe_relative(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            wanted = c.bounded_hash(stream, entry['lba'] * c.SECTOR, entry['size'])
            stream.seek(entry['lba'] * c.SECTOR)
            remaining = entry['size']
            with target.open('xb') as out:
                while remaining:
                    block = stream.read(min(c.BLOCK, remaining))
                    c.require(block, 'Unexpected source EOF')
                    out.write(block)
                    remaining -= len(block)
            expected[name] = info(target)
            c.require(expected[name] == {'bytes': entry['size'], 'sha256': wanted},
                      'Original extraction mismatch: ' + name)
    return expected


def write_image(image, stage, primary, expected):
    import pycdlib
    c.require(not image.exists(), 'Refusing existing ISO')
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, vol_ident='PS3VOLUME', sys_ident='PLAYSTATION3')
    try:
        directories = {str(p).replace('\\', '/') for n in expected
                       for p in Path(n).parents if str(p) not in ('/', '\\', '.')}
        for directory in sorted(directories, key=lambda p: (p.count('/'), p)):
            iso.add_directory(iso_path=directory, joliet_path=directory)
        for name in sorted(expected):
            path = stage / c.safe_relative(name)
            c.require(info(path) == expected[name], 'Staged file changed: ' + name)
            iso.add_file(str(path), iso_path=primary[name] + ';1', joliet_path=name)
        iso.write(str(image))
    finally:
        iso.close()
    c.stamp_disc(image)
    report = {'name': image.name, 'disc': c.verify_disc_header(image)}
    print('Verifying both filesystem trees:', image.name, flush=True)
    for joliet in (True, False):
        reader = c.ISO9660(str(image), joliet=joliet)
        try:
            actual = dict(reader.walk())
            keys = set(expected) if joliet else set(primary.values())
            c.require(set(actual) == keys, 'Output disc inventory mismatch')
            for name, wanted in expected.items():
                entry = actual[name if joliet else primary[name]]
                c.require(entry['size'] == wanted['bytes'] and
                          c.bounded_hash(reader.fh, entry['lba'] * c.SECTOR,
                                         entry['size']) == wanted['sha256'],
                          'Output file mismatch: ' + name)
        finally:
            reader.fh.close()
    report.update(info(image))
    report['files_verified_each_tree'] = len(expected)
    print('VERIFIED:', image.name, report['bytes'], report['sha256'], flush=True)
    return report


def wrap(executable, original, fself, generated):
    c.require(not generated.exists(), 'Refusing wrapper overwrite')
    subprocess.run([str(fself), str(executable), str(generated)], check=True)
    data = c.retain_application_metadata(generated.read_bytes(), original)
    return data, c.verify_self(data, executable.read_bytes(), original)


def preflight(source, build, output, fself, clean, previous):
    c.require(c.ROOT / 'work' in output.parents, 'Output must be under work')
    state = c.preflight(source, build, output, fself)
    c.require(state[0]['version'] == '0.6.13', 'Expected failing 0.6.13 snapshot')
    c.require(c.digest(clean) == CLEAN_SHA256, 'Pristine ELF hash mismatch')
    c.require(c.digest(fself) == FSELF_SHA256, 'Changed wrapper tool')
    old = json.loads(previous.read_text(encoding='utf-8'))
    c.require(old['package'] == 'CFW-test1' and
              old['base_manifest_sha256'] == c.digest(build / 'build_manifest.json') and
              old['fself_tool_sha256'] == FSELF_SHA256, 'Wrong prior CFW audit')
    c.require(shutil.disk_usage(output.parent).free > 24 * 2**30, 'Need 24 GiB free')
    entry = state[2][EBOOT]
    with source.open('rb') as stream:
        stream.seek(entry['lba'] * c.SECTOR)
        original = stream.read(entry['size'])
    c.control_records(original)
    verify_clean_headers(original, clean.read_bytes())
    print('Diagnostic override: THREE FULL ISOs; NO split files will be created.', flush=True)
    print('01: all original files; 02: only wrapper; 03: existing English 0.6.13.', flush=True)
    return state, old


def build_all(source, build, output, fself, clean, previous, state, old):
    manifest, replacements, inventory, primary = state
    output.mkdir()
    stage = output / 'intermediate_disc'
    stage.mkdir()
    print('Extracting verified original game files...', flush=True)
    original_files = extract_original(source, stage, inventory)
    original_self = (stage / c.safe_relative(EBOOT)).read_bytes()
    tests = [write_image(output / NAMES[0], stage, primary, original_files)]
    tests[0]['changes_from_original'] = []
    wrapper, clean_report = wrap(clean, original_self, fself, output / 'clean_fself_generated.bin')
    (stage / c.safe_relative(EBOOT)).write_bytes(wrapper)
    control_files = dict(original_files)
    control_files[EBOOT] = info(stage / c.safe_relative(EBOOT))
    c.require(changed(original_files, control_files) == [EBOOT], 'Control isolation failed')
    tests.append(write_image(output / NAMES[1], stage, primary, control_files))
    tests[1].update(changes_from_original=[EBOOT], executable=clean_report)
    translated_files = dict(control_files)
    print('Applying the validated 0.6.13 snapshot...', flush=True)
    for name, local in replacements.items():
        if name == EBOOT:
            continue
        path = stage / c.safe_relative(name)
        shutil.copyfile(build / local, path)
        translated_files[name] = info(path)
        c.require(translated_files[name] == {'bytes': manifest['files'][local]['bytes'],
                                            'sha256': manifest['files'][local]['sha256']},
                  'Snapshot changed during build')
    wrapper, english_report = wrap(build / 'EBOOT.BIN', original_self, fself,
                                   output / 'english_fself_generated.bin')
    (stage / c.safe_relative(EBOOT)).write_bytes(wrapper)
    translated_files[EBOOT] = info(stage / c.safe_relative(EBOOT))
    differences = verify_isolation(original_files, control_files, translated_files,
                                   replacements, old['files'])
    tests.append(write_image(output / NAMES[2], stage, primary, translated_files))
    tests[2].update(changes_from_test02=differences, executable=english_report,
                    file_contents_identical_to_previous_cfw_test1=True)
    report = {'schema': 1, 'package': 'PS3 boot isolation tests', 'hardware_tested': False,
              'original_iso_md5': c.SOURCE_MD5, 'source_path': str(source),
              'snapshot_manifest_sha256': c.digest(build / 'build_manifest.json'),
              'clean_elf_sha256': CLEAN_SHA256,
              'clean_elf_provenance': 'Existing pristine RPCS3-decrypted baseline; pinned SHA256; '
                                      'ELF and program headers match original SELF. Not freshly decrypted.',
              'fself_sha256': FSELF_SHA256, 'previous_audit_sha256': c.digest(previous),
              'split_files_created': False, 'installed': False, 'tests': tests,
              'original_files': original_files, 'control_files': control_files,
              'translated_files': translated_files}
    (output / 'SHA256SUMS.txt').write_text(''.join(t['sha256'] + '  ' + t['name'] + '\n'
                                                for t in tests), encoding='utf-8')
    (output / 'README-TEST.txt').write_text(
        'PS3 boot isolation tests - use an existing CFW setup only\n\n'
        'These are FULL, UNSPLIT ISO files. No emulator install or firmware change was made.\n'
        'Transfer to /dev_hdd0/PS3ISO/ using your existing transfer method.\n'
        'Do not put these full files on FAT32 USB. Do not install them as PKGs.\n'
        'Mount one ISO at a time using the same manager/settings, then launch its disc icon.\n'
        'The two Japanese tests have the same game title/icon: select by exact filename.\n'
        'Do not copy intermediate_disc or the generated BIN files. Keep saves untouched.\n\n'
        '1. ' + NAMES[0] + '\n   Original Japanese files and original executable, rebuilt ISO.\n'
        '2. ' + NAMES[1] + '\n   Same Japanese files; only executable wrapping changes.\n'
        '3. ' + NAMES[2] + '\n   Existing English 0.6.13 CFW-test1 contents, repackaged for comparison.\n'
        '   This is NOT a new fix; every game-file hash matches the previous CFW-test1.\n\n'
        'For each test report: mounts? title screen? exact error?\n'
        '01 failure: investigate repack/transfer/mount versus the working original ISO.\n'
        '01 passes, 02 fails: executable wrapper/decryption-baseline/CFW compatibility.\n'
        '01 and 02 pass, 03 fails: translated executable or translated assets.\n'
        'All pass: boot confirmed only; gameplay and stage-10 skip still need testing.\n'
        'Record CFW/Cobra and manager versions when available. Do not change firmware for this test.\n'
        'These tests do not distinguish every possible cause; no hardware compatibility claim.\n',
        encoding='utf-8')
    # Completion marker only after all three full read-backs and cross-test checks.
    (output / 'DIAGNOSTIC_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('ALL THREE UNSPLIT TESTS VERIFIED:', output, flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--build', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--fself', type=Path, required=True)
    ap.add_argument('--clean-elf', type=Path, required=True)
    ap.add_argument('--previous-audit', type=Path, required=True)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    paths = [p.resolve() for p in (a.source, a.build, a.out, a.fself, a.clean_elf, a.previous_audit)]
    state, old = preflight(*paths)
    if a.write:
        build_all(*paths, state, old)
    else:
        print('DRY RUN passed. No files changed.', flush=True)


if __name__ == '__main__':
    main()
