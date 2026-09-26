"""Patch only Library CV credits in the existing local VWF candidate.

Dry-run by default; --write keeps a backup and validates before replacement.
Does not rebuild descriptions, fonts, EBOOT, or install anything.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile

from cpk import CPK
import cpkpatch
import digraph as dg
import library_cv
import zukan
from intermission_layout import ink

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'work/lib/MTZKN_PT.CPK'
TARGET = ROOT / 'work/out_0.6.3/MTZKN_PT.CPK'
BACKUP = ROOT / 'work/library_cv.before.CPK'
REPORT = ROOT / 'work/library_cv_audit.json'


def credits(source):
    rows = {}
    for entry in source.files:
        magic, fields = zukan.parse_ordered(source.read(entry))
        found = [(i, p) for i, (tag, p) in enumerate(fields) if tag == 'ACTR']
        if len(found) != 1:
            raise ValueError('Expected one ACTR in entry %d' % entry['id'])
        index, raw = found[0]
        rows[entry['id']] = (index, raw.rstrip(b'\0').decode('cp932'), magic)
    return rows


def plan(source, current, mapping, widths):
    catalog = library_cv.load_catalog()
    actors = credits(source)
    if set(actors) != {e['id'] for e in current.files}:
        raise ValueError('Source/candidate Library IDs differ')
    expected, replacements, audit = {}, {}, []
    for entry in current.files:
        index, jp, source_magic = actors[entry['id']]
        en = library_cv.romanize(jp, catalog)
        if any(c not in mapping for c in en):
            raise ValueError('Candidate requires a VWF letter mapping for ' + en)
        # Conservative 400px budget at 32px type; no geometry is modified.
        width = ink(en, mapping, widths, 32)
        if width > 400:
            raise ValueError('CV exceeds header width: ' + en)
        magic, fields = zukan.parse_ordered(current.read(entry))
        if magic != source_magic or fields[index][0] != 'ACTR':
            raise ValueError('Source/candidate Library structure differs')
        wanted = dg.encode_mixed(en, mapping, newline=b'\n')
        old = fields[index][1]
        # CP932 contains duplicate encodings (e.g. Hidaka's 髙). Compare the
        # original credit as Unicode, not a decode/re-encode byte round trip.
        if old.rstrip(b'\0') != wanted and old.rstrip(b'\0').decode('cp932', 'replace') != jp:
            raise ValueError('Unexpected existing CV in entry %d' % entry['id'])
        changed = list(fields)
        changed[index] = ('ACTR', wanted)
        expected[entry['id']] = (magic, changed)
        if old != wanted:
            replacements[entry['id']] = zukan.build(magic, changed)
        audit.append({'id': entry['id'], 'credit': en, 'width_at_32px': width})
    return expected, replacements, audit


def verify(before, after, expected):
    if [e['id'] for e in before.files] != [e['id'] for e in after.files]:
        raise ValueError('Rebuilt Library IDs/order differ')
    for original, rebuilt in zip(before.files, after.files):
        magic, fields = zukan.parse_ordered(after.read(rebuilt))
        if (magic, fields) != expected[original['id']]:
            raise ValueError('Rebuilt field mismatch: %d' % original['id'])
        old_magic, old_fields = zukan.parse_ordered(before.read(original))
        if magic != old_magic or len(fields) != len(old_fields):
            raise ValueError('Library structure changed')
        for old, new in zip(old_fields, fields):
            if old[0] != new[0] or (old[0] != 'ACTR' and old != new):
                raise ValueError('Non-CV field changed: %d %s' % (original['id'], old[0]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    mapping = json.loads((TARGET.parent / 'pairs.json').read_text())
    widths = {int(k): v for k, v in json.loads((TARGET.parent / 'widths.json').read_text()).items()}
    source, current = CPK(str(SOURCE)), CPK(str(TARGET))
    expected, replacements, audit = plan(source, current, mapping, widths)
    named = [r for r in audit if r['credit'] != '---']
    report = {'entries': len(audit), 'credited_entries': len(named),
              'distinct_actors': len({r['credit'] for r in named}),
              'placeholders': len(audit) - len(named),
              'changed_entries': len(replacements),
              'before_sha256': hashlib.sha256(current.buf).hexdigest(),
              'credits': audit}
    print({k: v for k, v in report.items() if k != 'credits'})
    print('Aoi:', next(r for r in audit if r['id'] == 296))
    print('Widest:', max(audit, key=lambda r: r['width_at_32px']))
    if not replacements:
        verify(current, current, expected)
        print('All CV credits already synchronized.')
        return
    if args.write and BACKUP.exists():
        raise ValueError('Backup already exists; refusing to overwrite it')
    with tempfile.TemporaryDirectory(prefix='library_cv_', dir=str(ROOT / 'work')) as tmp:
        reps = {}
        for fid, raw in replacements.items():
            member = Path(tmp) / ('%d.bin' % fid)
            member.write_bytes(raw)
            reps[fid] = str(member)
        staged = Path(tmp) / 'MTZKN_PT.CPK'
        cpkpatch.build(str(TARGET), str(staged), reps)
        rebuilt = CPK(str(staged))
        verify(current, rebuilt, expected)
        report['after_sha256'] = hashlib.sha256(rebuilt.buf).hexdigest()
        print('Verified every member: only ACTR changed; all other fields preserved.')
        if args.write:
            if TARGET.read_bytes() != bytes(current.buf):
                raise ValueError('Candidate changed during validation')
            with BACKUP.open('xb') as backup:
                backup.write(current.buf)
            os.replace(str(staged), str(TARGET))
            REPORT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            print('Local candidate updated; no deployment.')


if __name__ == '__main__':
    main()
