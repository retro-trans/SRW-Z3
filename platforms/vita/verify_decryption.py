"""Independently inspect already decrypted Vita files; dry-run by default.

No license access. --report saves non-secret file hashes/format results only.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from cpk import CPK


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(4 << 20), b''):
            h.update(data)
    return h.hexdigest()


def sfo(data):
    assert data[:4] == b'\0PSF', 'Invalid PARAM.SFO'
    keys, values, count = struct.unpack_from('<III', data, 8)
    result = {}
    for i in range(count):
        k, typ, length, capacity, v = struct.unpack_from('<HHIII', data, 20 + i * 16)
        name = data[keys + k:data.index(b'\0', keys + k)].decode('ascii')
        if typ == 0x204:
            result[name] = data[values + v:values + v + length].rstrip(b'\0').decode('utf-8')
    return result


def verify(source, destination):
    def inventory(root):
        return {p.relative_to(root).as_posix(): p for p in root.rglob('*') if p.is_file()
                and not p.relative_to(root).as_posix().startswith(('sce_pfs/', 'sce_sys/package/'))}
    original, plain = inventory(source), inventory(destination)
    assert set(original) == set(plain), 'Decrypted inventory differs from source excluding PFS/package metadata'
    metadata = sfo((destination / 'sce_sys/param.sfo').read_bytes())
    assert metadata['TITLE_ID'] == 'PCSG00264'
    cpks, gxts, members = 0, 0, 0
    files, candidates = {}, []
    candidate_ids = {'DATA/STAGE/STG0001a.cpk': [4], 'DATA/STAGE/STG0001b.cpk': [3, 4]}
    for name, path in sorted(plain.items()):
        size = path.stat().st_size
        assert original[name].stat().st_size == size, 'File size differs: ' + name
        info = {'bytes': size, 'sha256': sha256(path)}
        if path.suffix.lower() == '.cpk':
            archive = CPK(str(path))
            assert archive.files, 'Empty archive index: ' + name
            for entry in archive.files:
                assert 0 <= entry['offset'] <= size and 0 <= entry['size'] <= size - entry['offset'], 'Member outside archive'
            info['cpk_members'] = len(archive.files)
            members += len(archive.files)
            cpks += 1
            if name in candidate_ids:
                for fid in candidate_ids[name]:
                    matching = [entry for entry in archive.files if entry['id'] == fid]
                    assert len(matching) == 1, 'Missing/ambiguous pilot candidate'
                    payload = archive.read(matching[0])
                    assert len(payload) == (matching[0]['extract'] or matching[0]['size'])
                    candidates.append({'archive': name, 'member_id': fid, 'bytes': len(payload),
                                       'sha256': hashlib.sha256(payload).hexdigest(),
                                       'prefix_hex': payload[:8].hex(), 'translation_mapping_verified': False})
            del archive
        elif path.suffix.lower() == '.gxt':
            with path.open('rb') as f:
                assert f.read(4) == b'GXT\0', 'Texture signature invalid: ' + name
            gxts += 1
        files[name] = info
    assert cpks == 176 and gxts == 189, 'Archive/texture counts differ from inspected package'
    assert len(candidates) == 3
    with (destination / 'eboot.bin').open('rb') as f:
        magic = f.read(4)
    assert magic == b'SCE\0', 'Unexpected EBOOT container'
    return {'schema': 1, 'title_id': metadata['TITLE_ID'], 'app_version': metadata.get('APP_VER'),
            'status': 'pfs_decrypted_formats_verified', 'files_verified': len(files),
            'source_inventory_matches': True, 'cpk_archives': cpks, 'cpk_members_indexed': members,
            'gxt_textures': gxts, 'pilot_candidates': candidates, 'files': files,
            'eboot_container': 'SCE SELF; executable-layer decryption not verified',
            'playable_translation': False, 'license_or_key_in_report': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--decrypted', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if args.report:
        assert ROOT / 'work/vita' in args.report.resolve().parents
        assert not args.report.exists(), 'Report already exists'
    report = verify(args.source, args.decrypted)
    print(json.dumps({k: v for k, v in report.items() if k != 'files'}, indent=2))
    if args.report:
        with args.report.open('x', encoding='utf-8') as out:
            json.dump(report, out, indent=2)
            out.write('\n')
        print('Saved non-secret verification report.')
    else:
        print('Dry-run: no files written.')


if __name__ == '__main__':
    main()
