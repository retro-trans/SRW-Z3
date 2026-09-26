"""Build boot-only crossover tests from the exact previous PS3 ISOs 02 and 03.

04 = 02 with ONLY the English EBOOT from 03.
05 = 03 with ONLY the Japanese wrapped EBOOT from 02.
No translation, wrapping, signing, installation or existing-image modification.
Dry-run by default. Only writes a new directory under ignored work/.
"""
import argparse
import json
from pathlib import Path
import shutil
import struct

import cfw_diagnostics as d

c = d.c
PRIOR = c.ROOT / 'work/ps3_boot_diagnostics_20260915'
AUDIT_SHA = 'e6715d550601c7ca9f6cc3c5f88b0d309d23b8deb0e3e124ab8df652722b9069'
NAMES = ('04-SRW-Z3-English-EBOOT-Japanese-Data.iso',
         '05-SRW-Z3-Japanese-EBOOT-English-Data.iso')


def output_path(path):
    path = path.resolve()
    c.require((c.ROOT / 'work').resolve() in path.parents and not path.exists(),
              'Output must be a NEW directory under work')
    c.require(path.parent.is_dir(), 'Output parent must exist')
    return path


def crossover_inventories(control, english):
    differences = d.changed(control, english)
    c.require(d.EBOOT in differences and len(differences) > 1,
              'Expected differing executable AND data')
    first = dict(control)
    first[d.EBOOT] = english[d.EBOOT]
    second = dict(english)
    second[d.EBOOT] = control[d.EBOOT]
    c.require(d.changed(control, first) == [d.EBOOT] and
              d.changed(english, second) == [d.EBOOT], 'Crossover isolation failed')
    return first, second


def copy_member(source, entry, target, expected):
    target.parent.mkdir(parents=True, exist_ok=True)
    c.require(entry['size'] == expected['bytes'], 'Source member size mismatch')
    with source.open('rb') as src, target.open('wb') as out:
        src.seek(entry['lba'] * c.SECTOR)
        remaining = entry['size']
        while remaining:
            block = src.read(min(c.BLOCK, remaining))
            c.require(block, 'Unexpected source EOF')
            out.write(block)
            remaining -= len(block)
    c.require(d.info(target) == expected, 'Copied member hash mismatch')


def executable_info(data):
    c.require(data[:4] == b'SCE\0', 'Missing SELF executable')
    offset, length = struct.unpack_from('>QQ', data, 16)
    c.require(offset + length == len(data), 'Bad SELF payload bounds')
    elf = data[offset:]
    _, headers = c.elf_headers(elf)
    return {'elf_bytes': len(elf),
            'entry': struct.unpack_from('>Q', elf, 24)[0],
            'program_headers': [dict(zip(('type', 'flags', 'offset', 'vaddr',
                                         'paddr', 'filesz', 'memsz', 'align'), row))
                                for row in headers]}


def preflight(output):
    output = output_path(output)
    audit_path = PRIOR / 'DIAGNOSTIC_AUDIT.json'
    c.require(c.digest(audit_path) == AUDIT_SHA, 'Previous audit pin mismatch')
    old = json.loads(audit_path.read_text(encoding='utf-8'))
    sources, inventories, aliases = [], [], []
    for index, key in ((1, 'control_files'), (2, 'translated_files')):
        test = old['tests'][index]
        c.require(test['name'] == d.NAMES[index], 'Unexpected previous ISO name')
        image = PRIOR / test['name']
        print('Verifying source ISO:', image.name, flush=True)
        c.require(d.info(image) == {k: test[k] for k in ('bytes', 'sha256')},
                  'Previous ISO damaged or changed')
        c.verify_disc_header(image)
        inventory, primary = c.read_inventory(image)
        c.require(set(inventory) == set(old[key]), 'Previous inventory differs')
        c.require(all(inventory[n]['size'] == row['bytes'] for n, row in old[key].items()),
                  'Previous member size mismatch')
        sources.append(image)
        inventories.append(inventory)
        aliases.append(primary)
    c.require(aliases[0] == aliases[1], 'Source filesystem aliases differ')
    expected = crossover_inventories(old['control_files'], old['translated_files'])
    c.require(shutil.disk_usage(output.parent).free > 16 * 2**30, 'Need 16 GiB free')
    print('04: English EBOOT + Japanese data (only EBOOT differs from working 02).', flush=True)
    print('05: Japanese EBOOT + English data (only EBOOT differs from failing 03).', flush=True)
    print('BOOT ONLY: mismatched text/fonts are expected; do not load/save progress.', flush=True)
    return output, old, sources, inventories, aliases[0], expected


def build(state):
    output, old, sources, inventories, primary, expected = state
    output.mkdir()
    stage = output / 'intermediate_disc'
    stage.mkdir()
    print('Extracting verified working-02 contents into NEW staging tree...', flush=True)
    original = d.extract_original(sources[0], stage, inventories[0])
    c.require(original == old['control_files'], 'Working-02 extracted contents differ')
    executable_path = stage / c.safe_relative(d.EBOOT)
    japanese_eboot = executable_info(executable_path.read_bytes())
    copy_member(sources[1], inventories[1][d.EBOOT], executable_path, expected[0][d.EBOOT])
    english_eboot = executable_info(executable_path.read_bytes())
    tests = [d.write_image(output / NAMES[0], stage, primary, expected[0])]
    tests[0].update(reference='02', changed_files=[d.EBOOT],
                    eboot_from='03', all_other_files_from='02')
    print('Preparing inverse crossover using exact 03 data and exact 02 EBOOT...', flush=True)
    differences = d.changed(expected[0], expected[1])
    for number, name in enumerate(differences, 1):
        index = 0 if name == d.EBOOT else 1
        copy_member(sources[index], inventories[index][name], stage / c.safe_relative(name),
                    expected[1][name])
        if number % 50 == 0:
            print('Prepared changed files:', number, '/', len(differences), flush=True)
    tests.append(d.write_image(output / NAMES[1], stage, primary, expected[1]))
    tests[1].update(reference='03', changed_files=[d.EBOOT],
                    eboot_from='02', all_other_files_from='03')
    guide = (c.ROOT / 'platforms/ps3/CROSS_BOOT_TEST.md').read_text(encoding='utf-8')
    (output / 'README-TEST.md').write_text(guide, encoding='utf-8')
    (output / 'SHA256SUMS.txt').write_text(''.join(t['sha256'] + '  ' + t['name'] + '\n'
                                                for t in tests), encoding='ascii')
    report = dict(schema=1, package='PS3 boot crossover tests 04-05',
                  source_audit_sha256=AUDIT_SHA,
                  prior_user_report={'01': 'loads', '02': 'loads', '03': '80010001'},
                  prior_report_same_settings_assumed=True,
                  sources=[{k: old['tests'][i][k] for k in ('name', 'bytes', 'sha256')}
                           for i in (1, 2)],
                  tests=tests, hardware_tested=False, installed=False,
                  split_files_created=False, boot_only_not_for_gameplay=True,
                  executable_comparison={'japanese': japanese_eboot, 'english': english_eboot},
                  files_04=expected[0], files_05=expected[1])
    # Completion marker only after both ISO trees and every member pass read-back.
    (output / 'DIAGNOSTIC_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('BOTH CROSSOVER ISOs VERIFIED:', output, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    state = preflight(args.out)
    if args.write:
        build(state)
    else:
        print('DRY RUN passed. No files changed.', flush=True)


if __name__ == '__main__':
    main()
