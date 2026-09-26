"""Build a pinned 0.6.14 RPCS3/modified-console candidate. Dry-run first.

Changes only EBOOT's container/layout, not translations. No publishing/install.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import subprocess

import cfw_loader_layout as layout

d, c = layout.x.d, layout.c
ROOT = c.ROOT
SOURCE = ROOT / 'work/release_image_0.6.14.iso'
SOURCE_SHA = 'c15b65a87d35cb4f3478fba829b4f14e6307de96b64979fdbc400b1d25e02462'
ELF_SHA = 'bbc597561a9c908e5b7da1564bf1923d4feba03986ee4a1dd2ca4d1a9ce5973d'
ORIGINAL = Path('E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso')
ORIGINAL_SHA = '1b45cdd1651b98fe24b544223488289790ae87d5f82f1db272285fb4e4dffa89'
FSELF = ROOT / 'work/cfw_psl1ght/fself.exe'
XDELTA = ROOT / 'work/xdelta3-3.1.0-x86_64.exe'
NAME = 'SRW-Z3-English-0.6.14-dual-test1.iso'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def rpc_decode(data):
    """Mirror RPCS3 CheckDebugSelf's 0x80 key-version branch (not a boot test)."""
    c.require(data[:4] == b'SCE\0' and len(data) >= 32, 'Invalid SELF')
    c.require(struct.unpack_from('<H', data, 8)[0] == 0x80, 'Not RPCS3 debug SELF')
    offset, size = struct.unpack_from('>QQ', data, 16)
    c.require(offset >= 32 and offset + size == len(data), 'Invalid SELF extent')
    elf = data[offset:]
    c.elf_headers(elf)
    return elf


def read_member(path, entry):
    with path.open('rb') as stream:
        stream.seek(entry['lba'] * c.SECTOR)
        data = stream.read(entry['size'])
    c.require(len(data) == entry['size'], 'Truncated ISO member')
    return data


def preflight(output):
    output = layout.x.output_path(output)
    c.require(shutil.disk_usage(output.parent).free > 25 * 2**30, 'Need 25 GiB free')
    print('Verifying frozen release and original ISO...', flush=True)
    c.require(c.digest(SOURCE) == SOURCE_SHA, 'Released ISO hash mismatch')
    c.require(c.digest(ORIGINAL) == ORIGINAL_SHA, 'Original ISO hash mismatch')
    c.require(c.digest(FSELF) == d.FSELF_SHA256, 'Wrapper tool hash mismatch')
    c.require(XDELTA.is_file(), 'Missing xdelta3')
    inventory, names = c.read_inventory(SOURCE)
    original_inventory, _ = c.read_inventory(ORIGINAL)
    elf = read_member(SOURCE, inventory[d.EBOOT])
    c.require(sha(elf) == ELF_SHA, 'Released executable changed')
    original = read_member(ORIGINAL, original_inventory[d.EBOOT])
    c.control_records(original)
    folded = layout.fold(elf)
    report = layout.verify(elf, folded)
    print(json.dumps(report, indent=2), flush=True)
    print('Only EBOOT changes; 553 other files preserved. New output:', output, flush=True)
    print('No firmware, saves, installed game or GitHub release changed.', flush=True)
    return output, inventory, names, elf, original, folded


def append_executable(source, target, wrapped):
    c.require(not target.exists(), 'Output ISO already exists')
    shutil.copyfile(source, target)
    with target.open('r+b') as stream:
        iso = c.Iso(stream)
        c.require(len(iso.trees) == 2, 'Expected two ISO trees')
        stream.seek(0, 2)
        offset = stream.tell()
        c.require(offset % c.SECTOR == 0, 'Unaligned source ISO')
        stream.write(wrapped + bytes(-len(wrapped) % c.SECTOR))
        for tree in iso.trees:
            found = iso.find(tree, d.EBOOT.strip('/').split('/'))
            c.require(found is not None, 'Missing EBOOT directory record')
            stream.seek(found[0] + 2)
            stream.write(struct.pack('<I', offset // c.SECTOR))
            stream.write(struct.pack('>I', offset // c.SECTOR))
            stream.write(struct.pack('<I', len(wrapped)))
            stream.write(struct.pack('>I', len(wrapped)))
    c.stamp_disc(target)
    c.verify_disc_header(target)


def verify_members(source, target, inventory, aliases, wrapped):
    expected = {}
    with source.open('rb') as stream:
        for name, entry in inventory.items():
            expected[name] = dict(bytes=entry['size'], sha256=c.bounded_hash(
                stream, entry['lba'] * c.SECTOR, entry['size']))
    expected[d.EBOOT] = dict(bytes=len(wrapped), sha256=sha(wrapped))
    for joliet in (True, False):
        reader = c.ISO9660(str(target), joliet=joliet)
        try:
            actual = dict(reader.walk())
            c.require(set(actual) == (set(expected) if joliet else set(aliases.values())),
                      'Changed ISO file inventory')
            for name, info in expected.items():
                entry = actual[name if joliet else aliases[name]]
                c.require(entry['size'] == info['bytes'] and c.bounded_hash(
                    reader.fh, entry['lba'] * c.SECTOR, entry['size']) == info['sha256'],
                    'ISO member mismatch: ' + name)
        finally:
            reader.fh.close()
    return expected


def build(state):
    output, inventory, aliases, elf, original, folded = state
    output.mkdir()
    elfpath = output / 'EBOOT-two-load.elf'
    elfpath.write_bytes(folded)
    wrapped, self_report = d.wrap(elfpath, original, FSELF, output / 'wrapper-generated.bin')
    c.require(rpc_decode(wrapped) == folded, 'RPCS3 extraction differs')
    (output / 'EBOOT.BIN').write_bytes(wrapped)
    image = output / NAME
    append_executable(SOURCE, image, wrapped)
    print('Verifying all 554 files in both ISO trees...', flush=True)
    files = verify_members(SOURCE, image, inventory, aliases, wrapped)
    # Installer-compatible flat snapshot: frozen release, not current catalogs.
    snapshot = output / 'snapshot'
    snapshot.mkdir()
    manifest = json.loads((ROOT / 'work/build_0.6.14_release/build_manifest.json').read_text())
    for name, info in manifest['files'].items():
        c.require(Path(name).name == name, 'Unsafe snapshot path')
        src = ROOT / 'work/build_0.6.14_release' / name
        c.require(d.info(src) == info, 'Frozen snapshot changed: ' + name)
        shutil.copyfile(src, snapshot / name)
    (snapshot / 'EBOOT.BIN').write_bytes(wrapped)
    manifest['files']['EBOOT.BIN'] = d.info(snapshot / 'EBOOT.BIN')
    manifest['compatibility_candidate'] = 'dual-test1; hardware runtime unverified'
    manifest['loader_layout_checks'] = layout.verify(elf, folded)
    (snapshot / 'build_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    shutil.copyfile(ROOT / 'work/build_0.6.14_release/message_coverage.json',
                    snapshot / 'message_coverage.json')
    delta = output / 'SRW-Z3-English-0.6.14-to-dual-test1.iso.xdelta'
    print('Encoding incremental xdelta...', flush=True)
    subprocess.run([str(XDELTA), '-e', '-s', str(SOURCE), str(image), str(delta)], check=True)
    decoded = output / 'delta-verification.iso'
    subprocess.run([str(XDELTA), '-d', '-s', str(SOURCE), str(delta), str(decoded)], check=True)
    image_info = d.info(image)
    c.require(d.info(decoded) == image_info, 'Delta round-trip mismatch')
    # Remove only our verified temporary duplicate, never an input or game tree.
    decoded.unlink()
    shutil.copyfile(ROOT / 'docs/PS3_DUAL_TEST_0.6.14.md', output / 'README.md')
    audit = dict(schema=1, candidate='0.6.14-dual-test1', hardware_tested=False,
                 rpcs3_runtime_tested=False, installed=False,
                 source_iso_sha256=SOURCE_SHA, source_elf_sha256=ELF_SHA,
                 original_iso_sha256=ORIGINAL_SHA, fself_sha256=d.FSELF_SHA256,
                 executable=d.info(output / 'EBOOT.BIN'), folded_elf=d.info(elfpath),
                 self_checks=self_report, layout_checks=layout.verify(elf, folded),
                 rpcs3_debug_self_extraction_verified=True,
                 changed_files=[d.EBOOT], files_verified_each_tree=len(files),
                 image=image_info, delta=d.info(delta), delta_decode_verified=True, files=files)
    (output / 'AUDIT.json').write_text(json.dumps(audit, indent=2) + '\n')
    (output / 'SHA256SUMS.txt').write_text(image_info['sha256'] + '  ' + image.name + '\n' +
                                         audit['delta']['sha256'] + '  ' + delta.name + '\n')
    print('COMPLETE: candidate built and statically verified; runtime testing required.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    state = preflight(args.out)
    if args.write:
        build(state)
    else:
        print('DRY RUN PASSED; no files written.')


if __name__ == '__main__':
    main()
