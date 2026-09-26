"""Scoped test 06: fold translation tables into the native RW LOAD.

This is a hardware compatibility candidate, not a proven 80010001 fix.
Only the pinned test-03 executable is accepted by the build entry point.
Dry-run unless --write; never edits existing outputs or installed games.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct

import cfw_cross_diagnostics as x

d, c = x.d, x.c
ELF_SHA = 'ce24c55c6e08e1782c02704fda308cfa1a8b67a4267dfcae599023207b45b694'
NAME = '06-SRW-Z3-English-Two-LOAD-CFW.iso'
PH = struct.Struct('>IIQQQQQQ')
SH = struct.Struct('>IIQQQQIIQQ')
TAIL = 0x859E34
EXT = 0x860000
NEW_EXT = 0xBF0000
NEW_TAIL = 0xC80000
# Preserve original section/table alignment when moving the nonloaded tail.
TAIL_START = NEW_TAIL + TAIL % 16
DELTA = TAIL_START - TAIL


def sections(data):
    offset = struct.unpack_from('>Q', data, 40)[0]
    size, count = struct.unpack_from('>HH', data, 58)
    c.require(size == SH.size and count == 32 and offset + size * count <= len(data),
              'Unexpected section table')
    return offset, [SH.unpack_from(data, offset + i * size) for i in range(count)]


def fold(data):
    phoff, rows = c.elf_headers(data)
    c.require(len(data) == 0x8F0000 and phoff == 64 and len(rows) == 8,
              'Unexpected English ELF layout')
    c.require(rows[0] == (1, 0x400005, 0, 0x10000, 0x10000, 0x780000, 0x780000, 0x10000)
              and rows[1] == (1, 0x600006, 0x780000, 0x790000, 0x790000,
                              0xD9E34, 0x46EF80, 0x10000)
              and rows[2] == (1, 4, EXT, 0xC00000, 0xC00000, 0x90000, 0x90000, 0x10000),
              'Unexpected translation LOADs')
    c.require(all(r[0] == 1 and r[3:7] == (0, 0, 0, 0) for r in rows[3:5]),
              'Expected empty placeholder LOADs')
    shoff, shrows = sections(data)
    c.require(TAIL <= shoff and shoff + 32 * 64 <= EXT, 'Section table outside tail')
    out = bytearray(data[:TAIL])
    out.extend(bytes(NEW_EXT - TAIL))
    out.extend(data[EXT:])
    out.extend(bytes(TAIL_START - NEW_TAIL))
    out.extend(data[TAIL:EXT])
    struct.pack_into('>Q', out, 40, shoff + DELTA)
    updated = list(rows)
    rw = list(rows[1])
    rw[5] = rw[6] = 0x500000
    updated[1] = tuple(rw)
    updated[2] = (1, rows[2][1], NEW_TAIL, 0, 0, 0, 0, rows[2][7])
    for i in (3, 4):
        empty = list(rows[i])
        empty[2] = NEW_TAIL
        updated[i] = tuple(empty)
    for i, row in enumerate(updated):
        PH.pack_into(out, phoff + i * PH.size, *row)
    for i, row in enumerate(shrows):
        changed = list(row)
        # ALLOC/NOBITS sections keep their native offset, including .bss.
        if row[1] != 8 and row[5] and not (row[2] & 2):
            c.require(TAIL <= row[4] and row[4] + row[5] <= EXT,
                      'Nonallocated section outside movable tail')
            changed[4] += DELTA
        SH.pack_into(out, shoff + DELTA + i * SH.size, *changed)
    verify(data, bytes(out))
    return bytes(out)


def verify(before, after):
    phoff, old = c.elf_headers(before)
    _, new = c.elf_headers(after)
    c.require(len(after) == TAIL_START + EXT - TAIL, 'Unexpected candidate length')
    active = [r for r in new if r[0] == 1 and r[6]]
    c.require(len(active) == 2 and new[0] == old[0] and new[5:] == old[5:],
              'Native code/TLS/process headers changed')
    c.require(new[1] == (1, old[1][1], 0x780000, 0x790000, 0x790000,
                         0x500000, 0x500000, 0x10000), 'Unexpected merged LOAD')
    c.require(all(r[3:7] == (0, 0, 0, 0) for r in new[2:5]), 'Nonempty placeholder')
    c.require(all((r[1] & 3) != 3 and r[2] % r[7] == r[3] % r[7] for r in active),
              'W+X or misaligned LOAD')
    c.require(active[0][3] + active[0][6] <= active[1][3], 'Overlapping LOADs')
    # Restore only deliberately changed ELF header fields, then compare the
    # entire original file-backed memory region, including all patched code.
    prefix = bytearray(after[:TAIL])
    prefix[40:48] = before[40:48]
    prefix[phoff + PH.size:phoff + PH.size * 5] = before[phoff + PH.size:phoff + PH.size * 5]
    c.require(prefix == before[:TAIL], 'Original code/data bytes changed')
    c.require(not any(after[TAIL:NEW_EXT]), 'BSS/scratch/gap is not zero-filled')
    c.require(after[NEW_EXT:NEW_TAIL] == before[EXT:], 'Translation table bytes changed')
    c.require(new[1][3] + NEW_EXT - new[1][2] == old[2][3], 'Table runtime address changed')
    oldshoff, oldsh = sections(before)
    newshoff, newsh = sections(after)
    c.require(newshoff == oldshoff + DELTA, 'Wrong relocated section table')
    c.require(newshoff % 8 == 0 and not any(after[NEW_TAIL:TAIL_START]),
              'Unaligned section table or nonzero padding')
    tail = bytearray(after[TAIL_START:])
    tail[oldshoff - TAIL:oldshoff - TAIL + 32 * 64] = before[oldshoff:oldshoff + 32 * 64]
    c.require(tail == before[TAIL:EXT], 'Nonloaded tail contents changed')
    for a, b in zip(oldsh, newsh):
        expected = list(a)
        if a[1] != 8 and a[5] and not (a[2] & 2):
            expected[4] += DELTA
        c.require(tuple(expected) == b, 'Section metadata changed unexpectedly')
        if a[8] and a[1] != 8:
            c.require(b[4] % a[8] == a[4] % a[8], 'Section alignment changed')
        if a[1] != 8 and a[5]:
            c.require(before[a[4]:a[4] + a[5]] == after[b[4]:b[4] + b[5]],
                      'Section payload changed')
    return {'active_loads': 2, 'code_and_initialized_data_preserved': True,
            'translation_table_va': '0xC00000', 'translation_bytes_preserved': True,
            'original_bss_and_scratch_zeroed': True, 'section_payloads_preserved': True,
            'entry_tls_process_parameters_preserved': True, 'no_writable_executable_load': True}


def preflight(output):
    output = x.output_path(output)
    audit = x.PRIOR / 'DIAGNOSTIC_AUDIT.json'
    c.require(c.digest(audit) == x.AUDIT_SHA, 'Source audit pin mismatch')
    prior = json.loads(audit.read_text(encoding='utf-8'))
    source = x.PRIOR / d.NAMES[2]
    print('Hashing exact test-03 source ISO...', flush=True)
    c.require(d.info(source) == {k: prior['tests'][2][k] for k in ('bytes', 'sha256')},
              'Source ISO changed')
    c.verify_disc_header(source)
    inventory, primary = c.read_inventory(source)
    c.require(set(inventory) == set(prior['translated_files']), 'Source paths differ')
    fself = c.ROOT / 'work/cfw_psl1ght/fself.exe'
    c.require(c.digest(fself) == d.FSELF_SHA256, 'Wrapper tool changed')
    c.require(shutil.disk_usage(output.parent).free > 12 * 2**30, 'Need 12 GiB free')
    with source.open('rb') as stream:
        entry = inventory[d.EBOOT]
        stream.seek(entry['lba'] * c.SECTOR)
        original = stream.read(entry['size'])
    c.require(hashlib.sha256(original).hexdigest() == prior['translated_files'][d.EBOOT]['sha256'],
              'Original SELF changed')
    x.executable_info(original)
    offset = struct.unpack_from('>Q', original, 16)[0]
    elf = original[offset:]
    c.require(hashlib.sha256(elf).hexdigest() == ELF_SHA, 'Wrong English ELF')
    candidate = fold(elf)
    print('Two-LOAD candidate passes mapped-data and code-preservation checks.', flush=True)
    return output, prior, source, inventory, primary, fself, original, elf, candidate


def build(state):
    output, prior, source, inventory, primary, fself, original, elf, candidate = state
    output.mkdir()
    elfpath = output / 'EBOOT-two-load.elf'
    elfpath.write_bytes(candidate)
    wrapped, self_report = d.wrap(elfpath, original, fself, output / 'fself-generated.bin')
    stage = output / 'intermediate_disc'
    stage.mkdir()
    print('Extracting exact English test-03 files to new staging folder...', flush=True)
    files = d.extract_original(source, stage, inventory)
    c.require(files == prior['translated_files'], 'Extracted source contents differ')
    target = stage / c.safe_relative(d.EBOOT)
    target.write_bytes(wrapped)
    files[d.EBOOT] = d.info(target)
    c.require(d.changed(prior['translated_files'], files) == [d.EBOOT], 'Isolation failed')
    print('Building full unsplit test-06 ISO; only EBOOT differs from test 03...', flush=True)
    test = d.write_image(output / NAME, stage, primary, files)
    (output / 'README-TEST.md').write_text(
        (c.ROOT / 'platforms/ps3/TWO_LOAD_TEST.md').read_text(encoding='utf-8'), encoding='utf-8')
    (output / 'SHA256SUMS.txt').write_text(test['sha256'] + '  ' + NAME + '\n', encoding='ascii')
    report = dict(schema=1, package='PS3 test 06 two-LOAD candidate', hardware_tested=False,
                  installed=False, split_files_created=False, source_audit_sha256=x.AUDIT_SHA,
                  source_iso=prior['tests'][2], source_elf_sha256=ELF_SHA,
                  fself_sha256=d.FSELF_SHA256, candidate_elf=d.info(elfpath),
                  user_hardware_reports={'01': 'loads', '02': 'loads', '03': '80010001',
                                         '04': '80010001', '05': 'loads'},
                  changed_from_03=[d.EBOOT], layout_checks=verify(elf, candidate),
                  self_checks=self_report, test=test, files=files)
    # Completion marker written only after every file passes both ISO-tree reads.
    (output / 'DIAGNOSTIC_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('TEST 06 COMPLETE AND VERIFIED:', output, flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    state = preflight(args.out)
    if args.write:
        build(state)
    else:
        print('DRY RUN passed; no files changed.', flush=True)


if __name__ == '__main__':
    main()
