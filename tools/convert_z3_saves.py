"""Convert decrypted Jigoku-hen saves between RPCS3 and Vita3K, offline.

Writes NEW workspace output only; never installs or overwrites live saves.
These are emulator imports, NOT signed PS3 or encrypted physical-Vita saves.

Legacy standalone 0.6.14 reference. The maintained converter is now in
../retro-trans-tools/retro_trans/z3_saves.py and Retro Trans's Z3 saves tab.
Keep this historical implementation for existing packagers/native checks;
make future converter changes in Retro Trans. No new standalone release implied.
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import struct
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PS3_ID = 'NPJB00520'
VITA_ID = 'PCSG00264'
FORMATS = {
    'STAGE.BIN': (0x48000, 0x40610, (0x40, 0x440, 0x108B0, 0x368B0, 0x3B3B0, 0x3B7B0), 0x440),
    'SYSTEM.BIN': (0xE0000, 0xD7A70, (0x40, 0x440, 0xD8F8, 0x1DD68, 0x87CC4,
                                     0x92014, 0x92A18, 0xD2810, 0xD2C10), 0xD8F8),
}
TEXT_FIELDS = {'TITLE': (4, 64), 'SUB_TITLE': (0x44, 128), 'DETAIL': (0xC4, 512)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def row(data):
    return dict(bytes=len(data), sha256=digest(data))


def checksum(data, start, length):
    # Native routines: PS3 VA0x176824, Vita VA0x810B47BC.
    # Sum little-endian words modulo 65536, excluding the final word.
    end = start + max(0, (length & ~1) - 2)
    require(0 <= start <= end <= len(data), 'Checksum region out of bounds')
    return sum(w[0] for w in struct.iter_unpack('<H', data[start:end])) & 0xFFFF


def inspect(data, kind, platform):
    require(kind in FORMATS and platform in ('ps3', 'vita'), 'Unsupported format/platform')
    size, used, offsets, payload = FORMATS[kind]
    require(len(data) == size, 'Unexpected save length: ' + kind)
    require(struct.unpack_from('<H', data, 2)[0] == 101, 'Unsupported save version')
    require(struct.unpack_from('>I' if platform == 'ps3' else '<I', data, 4)[0] == used,
            'Wrong platform or size header')
    require(struct.unpack_from('<' + 'I' * len(offsets), data, 8) == offsets,
            'Unexpected section layout')
    require(not any(data[8 + 4 * len(offsets):0x40]), 'Unknown header extension')
    checks = ((0, payload, size - payload), (0x40, 0x44, 0x3FC))
    for stored, start, length in checks:
        require(struct.unpack_from('<H', data, stored)[0] == checksum(data, start, length),
                'Save checksum mismatch at ' + hex(stored))
    report = dict(platform=platform, kind=kind, version=101, checksums_valid=True,
                  payload_sha256=digest(data[8:]), **row(data))
    if kind == 'STAGE.BIN':
        report['funds'] = struct.unpack_from('<I', data, 0x440)[0]
        report['z_chips'] = struct.unpack_from('<I', data, 0x44C)[0]
    return report


def convert(data, kind, source, target):
    require(source != target, 'Choose different source and target platforms')
    before = inspect(data, kind, source)
    converted = data[:4] + data[4:8][::-1] + data[8:]
    after = inspect(converted, kind, target)
    require(before['payload_sha256'] == after['payload_sha256'], 'Progress data changed')
    require(converted[:4] == data[:4], 'Checksum or version changed')
    require(converted[:4] + converted[4:8][::-1] + converted[8:] == data,
            'Non-lossless round trip')
    return converted


def sfo_fields(data):
    require(len(data) >= 20 and data[:8] == b'\0PSF\x01\x01\0\0', 'Bad SFO header')
    keys, values, count = struct.unpack_from('<III', data, 8)
    require(20 + count * 16 <= keys <= values <= len(data), 'Bad SFO table bounds')
    fields = {}
    for i in range(count):
        entry = 20 + i * 16
        key, typ, length, capacity, offset = struct.unpack_from('<HHIII', data, entry)
        keypos = keys + key
        require(keys <= keypos < values, 'Bad SFO key offset')
        end = data.find(b'\0', keypos, values)
        require(end >= keypos, 'Unterminated SFO key')
        name = data[keypos:end].decode('ascii')
        start = values + offset
        require(name not in fields and length <= capacity and start + capacity <= len(data),
                'Bad SFO value bounds or duplicate key')
        fields[name] = (entry, typ, start, length, capacity)
    ranges = sorted((f[2], f[2] + f[4]) for f in fields.values())
    require(all(a[1] <= b[0] for a, b in zip(ranges, ranges[1:])), 'Overlapping SFO values')
    return fields


def sfo_text(data):
    result = {}
    for name, (_, typ, start, length, _) in sfo_fields(data).items():
        if typ == 0x204:
            require(length > 0 and data[start + length - 1] == 0, 'Unterminated SFO string')
            result[name] = data[start:start + length - 1].decode('utf-8')
    return result


def update_sfo(template, changes):
    fields = sfo_fields(template)
    out = bytearray(template)
    for name, text in changes.items():
        require(name in fields, 'SFO field missing: ' + name)
        entry, typ, start, _, capacity = fields[name]
        encoded = text.encode('utf-8') + b'\0'
        require(typ == 0x204 and len(encoded) <= capacity, 'SFO text does not fit: ' + name)
        out[start:start + capacity] = encoded.ljust(capacity, b'\0')
        struct.pack_into('<I', out, entry + 4, len(encoded))
    require(all(sfo_text(out)[k] == v for k, v in changes.items()), 'SFO round trip failed')
    # Account and other destination-specific metadata stay byte-for-byte intact.
    for name, (_, _, start, length, capacity) in fields.items():
        if name not in changes:
            require(out[start:start + capacity] == template[start:start + capacity],
                    'Unrelated destination SFO metadata changed')
    return bytes(out)


def slot_text(data):
    require(len(data) == 0x34C, 'Unexpected Vita3K SlotParam size')
    result = {}
    for name, (start, capacity) in TEXT_FIELDS.items():
        field = data[start:start + capacity]
        end = field.find(b'\0')
        require(end >= 0, 'Unterminated slot text')
        result[name] = field[:end].decode('utf-8')
    return result


def make_slot(template, text, kind, timestamp):
    slot_text(template)
    out = bytearray(template)
    for name, (start, capacity) in TEXT_FIELDS.items():
        field = text[name].encode('utf-8') + b'\0'
        require(len(field) <= capacity, 'Slot text does not fit: ' + name)
        out[start:start + capacity] = field.ljust(capacity, b'\0')
    icon = ('app0:DATA/kurodata/icon_' + ('sys' if kind == 'SYSTEM.BIN' else 'stg') + '.png').encode()
    out[0x2C4:0x304] = (icon + b'\0').ljust(64, b'\0')
    # Vita3K writes this SceDateTime directly. Preserve source file's local time.
    when = datetime.fromtimestamp(timestamp)
    struct.pack_into('<6HI', out, 0x30C, when.year, when.month, when.day,
                     when.hour, when.minute, when.second, when.microsecond)
    require(slot_text(out) == {k: text[k] for k in TEXT_FIELDS}, 'Slot text round trip failed')
    return bytes(out)


def read_folder(folder, allowed):
    require(folder.is_dir() and not folder.is_symlink(), 'Missing or linked save folder')
    entries = list(folder.iterdir())
    require({p.name for p in entries} == set(allowed), 'Unexpected files in ' + str(folder))
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'Linked/non-file save entry')
    return {p.name: p.read_bytes() for p in entries}


def load_ps3(root):
    result = []
    for folder in sorted(root.glob(PS3_ID + '-*')):
        if not folder.is_dir():
            continue  # Unrelated archived backup, e.g. NPJB00520-SYS.zip.
        suffix = folder.name[len(PS3_ID):]
        match = re.fullmatch(r'-STG-(\d{3})', suffix)
        require(suffix == '-SYS' or match, 'Unknown PS3 save folder')
        kind = 'SYSTEM.BIN' if suffix == '-SYS' else 'STAGE.BIN'
        files = read_folder(folder, (kind, 'PARAM.SFO', 'ICON0.PNG', 'PIC1.PNG'))
        metadata = sfo_text(files['PARAM.SFO'])
        require(metadata['SAVEDATA_DIRECTORY'] == folder.name, 'SFO directory mismatch')
        require('時獄篇' in metadata['TITLE'], 'Wrong PS3 game title')
        inspect(files[kind], kind, 'ps3')
        index = 0 if kind == 'SYSTEM.BIN' else int(match[1]) + 1
        result.append(dict(folder=folder, files=files, kind=kind, slot=index,
                           metadata=metadata, timestamp=(folder / kind).stat().st_mtime))
    require(any(s['slot'] == 0 for s in result) and any(s['slot'] > 0 for s in result),
            'Need PS3 system and manual save templates')
    require(len({s['slot'] for s in result}) == len(result), 'Duplicate PS3 slot')
    return result


def load_vita(root):
    require(root.name == VITA_ID and not root.is_symlink(), 'Wrong Vita save root')
    result, expected = [], set()
    for folder in sorted(root.glob(VITA_ID + '-*')):
        suffix = folder.name[len(VITA_ID):]
        match = re.fullmatch(r'-STG-(\d{3})', suffix)
        require(suffix == '-SYS' or match, 'Unknown Vita save folder')
        kind = 'SYSTEM.BIN' if suffix == '-SYS' else 'STAGE.BIN'
        index = 0 if kind == 'SYSTEM.BIN' else int(match[1])
        require(kind == 'SYSTEM.BIN' or index > 0, 'Vita manual slots are one-based')
        files = read_folder(folder, (kind,))
        param = root / ('SlotParam_' + str(index) + '.bin')
        require(param.is_file() and not param.is_symlink(), 'Missing or linked Vita slot metadata')
        files['slot'] = param.read_bytes()
        metadata = slot_text(files['slot'])
        require('時獄篇' in metadata['TITLE'], 'Wrong Vita game title')
        inspect(files[kind], kind, 'vita')
        expected.update((folder.name, param.name))
        result.append(dict(folder=folder, files=files, kind=kind, slot=index,
                           metadata=metadata, timestamp=(folder / kind).stat().st_mtime))
    require({p.name for p in root.iterdir()} == expected, 'Unrecognized Vita save-root entries')
    require(any(s['slot'] == 0 for s in result) and any(s['slot'] > 0 for s in result),
            'Need Vita system and manual save templates')
    require(len({s['slot'] for s in result}) == len(result), 'Duplicate Vita slot')
    return result


def source_blobs(ps3, vita):
    files = {}
    for platform, saves in (('rpcs3', ps3), ('vita3k', vita)):
        for save in saves:
            for name, data in save['files'].items():
                relative = (save['folder'].name + '/' + name if name != 'slot'
                            else 'SlotParam_' + str(save['slot']) + '.bin')
                files[platform + '/' + relative] = data
    return files


def packages(ps3, vita):
    outputs = {'rpcs3-to-vita3k': {}, 'vita3k-to-rpcs3': {}}
    mapping = []
    for saves, templates, source, target, direction in (
            (ps3, vita, 'ps3', 'vita', 'rpcs3-to-vita3k'),
            (vita, ps3, 'vita', 'ps3', 'vita3k-to-rpcs3')):
        out = outputs[direction]
        for save in saves:
            kind, slot = save['kind'], save['slot']
            template = next(s for s in templates if s['kind'] == kind)
            converted = convert(save['files'][kind], kind, source, target)
            if target == 'vita':
                folder = VITA_ID + ('-SYS' if slot == 0 else '-STG-%03d' % slot)
                prefix = VITA_ID + '/' + folder + '/'
                out[prefix + kind] = converted
                out[VITA_ID + '/SlotParam_%d.bin' % slot] = make_slot(
                    template['files']['slot'], save['metadata'], kind, save['timestamp'])
            else:
                folder = PS3_ID + ('-SYS' if slot == 0 else '-STG-%03d' % (slot - 1))
                prefix = 'savedata/' + folder + '/'
                out[prefix + kind] = converted
                fields = {k: save['metadata'][k] for k in TEXT_FIELDS}
                fields['SAVEDATA_DIRECTORY'] = folder
                out[prefix + 'PARAM.SFO'] = update_sfo(template['files']['PARAM.SFO'], fields)
                for icon in ('ICON0.PNG', 'PIC1.PNG'):
                    out[prefix + icon] = template['files'][icon]
            mapping.append(dict(direction=direction, source_folder=save['folder'].name,
                                destination_folder=folder, slot=slot, kind=kind,
                                description=save['metadata']['DETAIL'],
                                source=row(save['files'][kind]), converted=inspect(converted, kind, target),
                                changed_offsets=[i for i, (a, b) in enumerate(zip(save['files'][kind], converted)) if a != b],
                                round_trip_exact=convert(converted, kind, target, source) == save['files'][kind]))
    return outputs, mapping


def put_files(root, files):
    for name, data in files.items():
        parts = name.split('/')
        require(all(p and p not in ('.', '..') and ':' not in p and '\\' not in p for p in parts),
                'Unsafe output name')
        path = root.joinpath(*parts)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as stream:
            stream.write(data)
        require(path.read_bytes() == data, 'Output read-back mismatch')


def make_zip(path, files):
    with zipfile.ZipFile(str(path), 'x', compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)
    with zipfile.ZipFile(str(path)) as archive:
        require(set(archive.namelist()) == set(files) and len(archive.infolist()) == len(files),
                'ZIP inventory mismatch')
        for name, data in files.items():
            require(archive.read(name) == data, 'ZIP content/CRC mismatch')
    return row(path.read_bytes())


def build(ps3_root, vita_root, output, write=False, guide_path=None, expected_sources=None):
    output = output.resolve()
    require((ROOT / 'work').resolve() in output.parents and not output.exists(),
            'Output must be a NEW folder under workspace work/')
    ps3_root, vita_root = ps3_root.resolve(), vita_root.resolve()
    require(ps3_root not in output.parents and vita_root not in output.parents,
            'Output cannot be inside a live save root')
    ps3, vita = load_ps3(ps3_root), load_vita(vita_root)
    backups = source_blobs(ps3, vita)
    if expected_sources is not None:
        require({n: row(b) for n, b in backups.items()} == expected_sources,
                'Saves changed since checking. Check saves again before converting.')
    converted, mappings = packages(ps3, vita)
    report = dict(schema=1, game='SRW Z3 Jigoku-hen', title_ids=[PS3_ID, VITA_ID],
                  status='converted_emulator_test_candidates', runtime_tested=False, installed=False,
                  source_roots=dict(rpcs3=str(ps3_root), vita3k=str(vita_root)),
                  source_files={n: row(b) for n, b in backups.items()}, mappings=mappings,
                  originals_unchanged=True, checksums_preserved=True,
                  body_bytes_preserved=True, only_binary_change='reverse bytes 4:8 (native size field)',
                  not_for_direct_physical_console_install=True)
    print('Validated %d RPCS3 saves and %d Vita3K saves.' % (len(ps3), len(vita)), flush=True)
    for m in mappings:
        print(m['direction'], m['source_folder'], '->', m['destination_folder'],
              '| checksums OK; exact round trip', flush=True)
    if not write:
        print('DRY RUN: no files changed.', flush=True)
        return report
    guide = Path(guide_path or ROOT / 'docs/SAVE_CONVERSION.md').read_bytes()
    output.mkdir(parents=True)
    put_files(output / 'original-backups', backups)
    report['packages'] = {}
    for direction, files in converted.items():
        package = dict(files)
        package['README-FIRST.md'] = guide
        put_files(output / direction, package)
        name = direction + '.zip'
        report['packages'][direction] = dict(name=name, **make_zip(output / name, package),
                                            files={n: row(b) for n, b in files.items()})
    # Re-read the live sources, verifying that neither the converter nor a
    # concurrently running emulator altered them during generation.
    require(source_blobs(load_ps3(ps3_root), load_vita(vita_root)) == backups,
            'Source saves changed during build; outputs must not be used')
    put_files(output, {'README-FIRST.md': guide,
                      'CONVERSION_AUDIT.json': (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')})
    print('BOTH CONVERSIONS VERIFIED:', output, flush=True)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ps3-save-root', type=Path, required=True)
    parser.add_argument('--vita-save-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    build(args.ps3_save_root, args.vita_save_root, args.output, args.write)


if __name__ == '__main__':
    main()
