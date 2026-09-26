"""Write a hardware disc image that keeps the original disc's layout.

The fresh writer (`cfw_diagnostics.write_image`) rebuilds ISO9660 and Joliet
from a staged tree, so nearly every file lands at a new offset. That fixed the
hardware defects of the legacy append images but made an original-to-release
xdelta about 3 GB: xdelta only looks for matches inside a window of the source,
and a disc whose data has all moved looks new to it.

None of the defects that the fresh writer fixed needs the files to move:

  * the stale sector-range table -> `stamp_disc` writes ONE plaintext region
    covering the finished image, exactly as it does for the fresh writer;
  * the stale UDF tree -> its recognition sequence, anchors and descriptor
    sequences are zeroed, so no reader can find it. The fresh image had no
    UDF at all; this reaches the same state for every reader;
  * the plain ELF -> the caller supplies the fake-SELF-wrapped EBOOT.

So here the original bytes stay where they were. Each replaced file is
APPENDED on a sector boundary and its record in BOTH trees is repointed; the
old extents stay behind, unreferenced. The delta is then the appended data
plus a few header and directory bytes.

Verification never trusts the writer's own offsets: the image is re-parsed,
every one of the disc's files is read back through each tree and hashed.
"""
import shutil
import struct
from pathlib import Path

import cfw_package as c

SECTOR = c.SECTOR
UDF_VRS = (b'BEA01', b'NSR02', b'NSR03', b'TEA01', b'BOOT2', b'CDW02')
AVDP_TAG = 2


def _directory_extents(iso):
    """Sectors owned by ISO9660 structures: descriptors, path tables, dirs."""
    owned = set(range(16, 16 + len(iso.trees) + 1))       # descriptors + terminator
    for kind, dlba, root, size in iso.trees:
        joliet = kind == 'joliet'
        iso.fh.seek(dlba * SECTOR)
        desc = iso.fh.read(SECTOR)
        table = struct.unpack_from('<I', desc, 132)[0]
        for off, fmt in ((140, '<I'), (144, '<I'), (148, '>I'), (152, '>I')):
            lba = struct.unpack_from(fmt, desc, off)[0]
            if lba:
                owned.update(range(lba, lba + -(-table // SECTOR)))
        pending = [(root, size)]
        seen = set()
        while pending:
            ext, length = pending.pop()
            if ext in seen:
                continue
            seen.add(ext)
            owned.update(range(ext, ext + -(-length // SECTOR)))
            for name, _off, e, dl, isdir in iso.records(ext, length, joliet):
                if isdir and name not in ('.', '..'):
                    pending.append((e, dl))
    return owned


def _udf_sectors(fh, total_sectors):
    """Every sector that makes the UDF tree discoverable."""
    found = []
    lba = 16
    while True:                                 # skip the ISO9660 descriptors
        fh.seek(lba * SECTOR)
        head = fh.read(6)
        if head[1:6] != b'CD001':
            break
        lba += 1
        if head[0] == 255:
            break
    while True:                                 # the volume recognition sequence
        fh.seek(lba * SECTOR)
        head = fh.read(6)
        if head[1:6] not in UDF_VRS:
            break
        found.append(lba)
        lba += 1
    # UDF puts its anchor at 256 and at N-256 and/or N-1
    for anchor in sorted({256, total_sectors - 256, total_sectors - 1}):
        if not 256 <= anchor < total_sectors:
            continue
        fh.seek(anchor * SECTOR)
        tag = fh.read(32)
        if len(tag) == 32 and struct.unpack_from('<H', tag, 0)[0] == AVDP_TAG:
            found.append(anchor)
            # main and reserve volume descriptor sequences: (length, location)
            for off in (16, 24):
                length, loc = struct.unpack_from('<II', tag, off)
                found.extend(range(loc, loc + -(-length // SECTOR)))
    return sorted(set(found))


def udf_present(path):
    path = Path(path)
    with path.open('rb') as fh:
        return bool(_udf_sectors(fh, path.stat().st_size // SECTOR))


def write(image, source, inventory, primary, replacements, expected):
    """Build `image` from `source` with `replacements` {disc name: local file}.

    `inventory` is the source's Joliet walk {name: {lba, size}}; `primary`
    maps each Joliet name to its primary-tree name; `expected` is every
    file's {bytes, sha256} in the finished image.
    """
    image = Path(image)
    c.require(not image.exists(), 'Refusing existing ISO')
    c.require(set(replacements) <= set(inventory), 'Replacement absent from source disc')
    shutil.copyfile(source, image)
    with image.open('r+b') as fh:
        iso = c.Iso(fh)
        c.require(len(iso.trees) == 2, 'Expected primary and Joliet trees')
        c.require(sorted(t[0] for t in iso.trees) == ['joliet', 'primary'],
                  'Expected one primary and one Joliet tree')
        total = fh.seek(0, 2)
        c.require(total % SECTOR == 0, 'Unaligned source ISO')
        owned = _directory_extents(iso)
        for entry in inventory.values():
            owned.update(range(entry['lba'], entry['lba'] + -(-entry['size'] // SECTOR)))
        udf = _udf_sectors(fh, total // SECTOR)
        clash = owned.intersection(udf)
        c.require(not clash, 'UDF sectors overlap ISO9660 data: %s' % sorted(clash)[:8])
        next_lba = total // SECTOR
        for name in sorted(replacements):
            local = Path(replacements[name])
            size = local.stat().st_size
            c.require(size < 2**32, 'File too large for one ISO9660 extent: ' + name)
            lba = next_lba
            fh.seek(lba * SECTOR)
            with local.open('rb') as src:
                shutil.copyfileobj(src, fh, c.BLOCK)
            fh.write(bytes(-size % SECTOR))
            next_lba += -(-size // SECTOR)
            for tree in iso.trees:
                path = name if tree[0] == 'joliet' else primary[name]
                hit = iso.find(tree, path.strip('/').split('/'))
                c.require(hit is not None, 'Missing %s record: %s' % (tree[0], name))
                off, old_lba, old_len = hit
                c.require((old_lba, old_len) == (inventory[name]['lba'], inventory[name]['size']),
                          'Record does not match the source inventory: ' + name)
                # extent: LE at +2, BE at +6; data length: LE at +10, BE at +14
                fh.seek(off + 2)
                fh.write(struct.pack('<I', lba) + struct.pack('>I', lba))
                fh.seek(off + 10)
                fh.write(struct.pack('<I', size) + struct.pack('>I', size))
        for lba in udf:
            fh.seek(lba * SECTOR)
            fh.write(bytes(SECTOR))
    c.stamp_disc(image)       # one whole-image plaintext region + volume size
    return verify(image, primary, expected)


def verify(image, primary, expected):
    image = Path(image)
    report = {'name': image.name, 'disc': c.verify_disc_header(image), 'layout': 'preserved'}
    c.require(not udf_present(image), 'UDF tree still discoverable')
    report['udf'] = 'absent'
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
                          c.bounded_hash(reader.fh, entry['lba'] * SECTOR,
                                         entry['size']) == wanted['sha256'],
                          'Output file mismatch: ' + name)
        finally:
            reader.fh.close()
    info = {'bytes': image.stat().st_size, 'sha256': c.digest(image)}
    report.update(info)
    report['files_verified_each_tree'] = len(expected)
    print('VERIFIED:', image.name, report['bytes'], report['sha256'], flush=True)
    return report
