"""Build a patched disc image from the pristine ISO and a release snapshot,
changing as little of the image as possible -- so that ONE xdelta covers
the whole game.

    python tools/iso_patch.py <version> [--iso PATH] [--out PATH]
                              [--xdelta PATH] [--verify-only PATH]

The image is plain ISO9660 (PS3 discs are). Every shipped file grew, so it
cannot be overwritten in its original extent. Instead each new file is
APPENDED at the end of the image on a sector boundary and its directory
record (in the primary tree and, if present, the Joliet tree) is repointed
to the new extent. Nothing else moves: the delta between the two images is
the appended data plus a few directory bytes, which is what keeps the
single xdelta small and deterministic. The old extents stay in place,
unreferenced.

Verification re-parses the patched image, reads every shipped file back
through the directory tree, and compares its SHA-1 with the snapshot's
manifest -- the same independence rule as the RPW writer: the check never
reuses the writer's own offsets.
"""
import argparse
import hashlib
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deploy   # noqa: E402  -- LAYOUT: shipped name -> dir under PS3_GAME/USRDIR

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DEFAULT_ISO = os.path.join(ROOT, "Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso")
DEFAULT_XD = os.path.join(ROOT, "work", "xdelta3-3.1.0-x86_64.exe")
SECTOR = 2048


def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_delta(xdelta, source, delta, expected):
    """Decode the distribution asset independently; never trust encoding alone."""
    with tempfile.TemporaryDirectory(prefix='verify-', dir=os.path.dirname(delta)) as temp:
        decoded = os.path.join(temp, 'decoded.iso')
        subprocess.run([xdelta, '-d', '-s', source, delta, decoded], check=True)
        if sha1(decoded) != sha1(expected):
            raise SystemExit('decoded ISO patch does not reproduce the release: ' + delta)
    print('decode-verified: ' + os.path.basename(delta), flush=True)


class Iso:
    """Just enough ISO9660 to walk the directory trees and patch records."""

    def __init__(self, fh):
        self.fh = fh
        self.trees = []              # [(name, root_extent, root_size, joliet)]
        lba = 16
        while True:
            self.fh.seek(lba * SECTOR)
            d = self.fh.read(SECTOR)
            if d[1:6] != b"CD001":
                break
            t = d[0]
            if t == 255:
                break
            if t in (1, 2):
                joliet = t == 2 and d[88:91] in (b"%/@", b"%/C", b"%/E")
                ext = struct.unpack_from("<I", d, 156 + 2)[0]
                size = struct.unpack_from("<I", d, 156 + 10)[0]
                self.trees.append(("joliet" if joliet else "primary", lba, ext, size))
            lba += 1
        if not self.trees:
            raise SystemExit("no ISO9660 volume descriptor found")

    def records(self, extent, size, joliet):
        """Yield (name, record_abs_offset, ext_lba, data_len) of one directory."""
        self.fh.seek(extent * SECTOR)
        data = self.fh.read(size)
        pos = 0
        while pos < len(data):
            ln = data[pos]
            if ln == 0:                      # padding to the next sector
                pos = (pos // SECTOR + 1) * SECTOR
                continue
            rec = data[pos:pos + ln]
            ext = struct.unpack_from("<I", rec, 2)[0]
            dlen = struct.unpack_from("<I", rec, 10)[0]
            flags = rec[25]
            nl = rec[32]
            raw = rec[33:33 + nl]
            if raw in (b"\x00", b"\x01"):
                name = "." if raw == b"\x00" else ".."
            elif joliet:
                name = raw.decode("utf-16-be", "replace")
            else:
                name = raw.decode("ascii", "replace")
            base = name.split(";")[0]
            yield base, extent * SECTOR + pos, ext, dlen, bool(flags & 2)
            pos += ln

    def find(self, tree, path):
        """(record_abs_offset, ext_lba, data_len) of a file by path segments."""
        _, _, ext, size, joliet = tree[0], tree[1], tree[2], tree[3], tree[0] == "joliet"
        for i, seg in enumerate(path):
            hit = None
            for name, off, e, dl, isdir in self.records(ext, size, joliet):
                if name.upper() == seg.upper():
                    hit = (off, e, dl, isdir)
                    break
            if hit is None:
                return None
            off, e, dl, isdir = hit
            if i == len(path) - 1:
                return off, e, dl
            if not isdir:
                return None
            ext, size = e, dl
        return None


def shipped_paths():
    out = {}
    for name, sub in deploy.LAYOUT.items():
        import posixpath
        path=posixpath.normpath('PS3_GAME/USRDIR/'+sub+'/'+name)
        assert path.startswith('PS3_GAME/')
        segs=path.split('/')
        out[name] = segs
    return out


def build(iso_in, snapshot, out_path):
    shutil.copyfile(iso_in, out_path)
    fh = open(out_path, "r+b")
    iso = Iso(fh)
    total = os.path.getsize(out_path)
    assert total % SECTOR == 0, "image is not sector-aligned"
    next_lba = total // SECTOR
    fh.seek(0, 2)
    paths = shipped_paths()
    log = []
    for name, segs in sorted(paths.items()):
        src = os.path.join(snapshot, name)
        if not os.path.isfile(src):
            raise SystemExit("snapshot lacks %s" % name)
        data = open(src, "rb").read()
        lba = next_lba
        pad = (-len(data)) % SECTOR
        fh.seek(0, 2)
        fh.write(data + bytes(pad))
        next_lba += (len(data) + pad) // SECTOR
        hits = 0
        for tree in iso.trees:
            r = iso.find(tree, segs)
            if r is None:
                continue
            off, old_lba, old_len = r
            # extent: LE at +2, BE at +6; data length: LE at +10, BE at +14
            fh.seek(off + 2); fh.write(struct.pack("<I", lba) + struct.pack(">I", lba))
            fh.seek(off + 10); fh.write(struct.pack("<I", len(data)) + struct.pack(">I", len(data)))
            hits += 1
        if hits == 0:
            raise SystemExit("%s: not found in any directory tree" % "/".join(segs))
        log.append((name, len(data), lba, hits))
    # volume space size (sectors): LE at +80, BE at +84 in every volume descriptor
    for _, dlba, _, _ in iso.trees:
        fh.seek(dlba * SECTOR + 80)
        fh.write(struct.pack("<I", next_lba) + struct.pack(">I", next_lba))
    fh.close()
    return log


def verify(out_path, snapshot, manifest):
    """Read every shipped file back through the directory tree; compare SHA-1s."""
    want = {}
    if manifest and os.path.isfile(manifest):
        m = json.load(open(manifest, encoding="utf-8"))
        files = m.get("files", m)
        for name, info in files.items():
            want[name] = info["sha1"] if isinstance(info, dict) else info
    fh = open(out_path, "rb")
    iso = Iso(fh)
    bad = []
    for name, segs in shipped_paths().items():
        for tree in iso.trees:
            r = iso.find(tree, segs)
            if r is None:
                bad.append("%s: missing in %s tree" % (name, tree[0])); continue
            _, lba, dlen = r
            fh.seek(lba * SECTOR)
            h = hashlib.sha1(fh.read(dlen)).hexdigest()
            ref = want.get(name) or sha1(os.path.join(snapshot, name))
            if h != ref:
                bad.append("%s (%s tree): sha1 %s != %s" % (name, tree[0], h, ref))
    fh.close()
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("version")
    ap.add_argument("--iso", default=DEFAULT_ISO)
    ap.add_argument("--out", default=None, help="patched image path (default work/patched_<version>.iso)")
    ap.add_argument("--xdelta", default=DEFAULT_XD)
    ap.add_argument("--no-delta", action="store_true", help="build and verify the image only")
    ap.add_argument("--reuse", action="store_true", help="skip the build if the patched image already exists (verify / encode only)")
    ap.add_argument("--prev", default=None, help="also encode an update delta from work/patched_<PREV>.iso (players on PREV update without the original image)")
    ap.add_argument("--prev-iso", help="Explicit existing previous-version ISO (requires --prev)")
    ap.add_argument("--dry-run", action="store_true", help="Check inputs and show planned outputs without writing")
    a = ap.parse_args()
    snapshot = os.path.join(ROOT, "releases", a.version)
    manifest = os.path.join(ROOT, "releases", a.version + ".json")
    if not os.path.isdir(snapshot):
        sys.exit("no snapshot at %s -- run tools/release.py first" % snapshot)
    out = a.out or os.path.join(ROOT, "work", "patched_%s.iso" % a.version)
    if a.prev_iso and not a.prev:
        sys.exit('--prev-iso requires --prev')
    previous = a.prev_iso or (os.path.join(ROOT, 'work', 'patched_%s.iso' % a.prev) if a.prev else None)
    if a.dry_run:
        if not os.path.isfile(a.iso) or (previous and not os.path.isfile(previous)):
            sys.exit('Missing original or previous ISO')
        with open(manifest, encoding='utf-8') as stream:
            recorded = json.load(stream)['files']
        for name in shipped_paths():
            if sha1(os.path.join(snapshot,name)) != recorded[name]['sha1']:
                sys.exit('Snapshot hash mismatch: '+name)
        print('DRY RUN: validated %d snapshot files; original: %s' % (len(recorded),a.iso))
        print('Output image:',out)
        print('Original delta:', 'SRW-Z3-English-%s.iso.xdelta' % a.version)
        if previous:print('Update source:',previous,'; update:',a.prev,'->',a.version)
        print('RPCS3 legacy image format only; not physical-console validated. No files written.')
        return
    if a.reuse and os.path.isfile(out):
        print("reusing existing %s" % out, flush=True)
        log = list(shipped_paths())
    else:
        print("building %s from %s + %s" % (out, os.path.basename(a.iso), snapshot), flush=True)
        log = build(a.iso, snapshot, out)
        for name, size, lba, hits in log:
            print("  %-26s %10d B  -> LBA %d  (%d record%s)" % (name, size, lba, hits, "s" if hits != 1 else ""), flush=True)
    bad = verify(out, snapshot, manifest)
    if bad:
        for b in bad:
            print("  VERIFY FAILED: " + b)
        sys.exit(1)
    print("verified: all %d shipped files read back from the patched image match the snapshot" % len(log), flush=True)
    if a.no_delta:
        return
    delta = os.path.join(ROOT, "releases", "%s_xdelta" % a.version, "SRW-Z3-English-%s.iso.xdelta" % a.version)
    os.makedirs(os.path.dirname(delta), exist_ok=True)
    src_size = os.path.getsize(a.iso)
    # source window must span the whole image so unchanged data matches by copy
    r = subprocess.run([a.xdelta, "-e", "-f", "-B", str(min(src_size, 2 ** 31 - 1)), "-s", a.iso, out, delta])
    if r.returncode != 0:
        sys.exit("xdelta3 encode failed")
    verify_delta(a.xdelta, a.iso, delta, out)
    print("delta: %s  (%d bytes)" % (delta, os.path.getsize(delta)))
    if a.prev:
        prev_iso = previous
        if not os.path.isfile(prev_iso):
            sys.exit("no previous patched image at %s" % prev_iso)
        upd = os.path.join(os.path.dirname(delta), "SRW-Z3-English-%s-to-%s.iso.xdelta" % (a.prev, a.version))
        r = subprocess.run([a.xdelta, "-e", "-f", "-B", str(min(os.path.getsize(prev_iso), 2 ** 31 - 1)), "-s", prev_iso, out, upd])
        if r.returncode != 0:
            sys.exit("xdelta3 encode (update) failed")
        verify_delta(a.xdelta, prev_iso, upd, out)
        print("update delta: %s  (%d bytes)" % (upd, os.path.getsize(upd)))


if __name__ == "__main__":
    main()
