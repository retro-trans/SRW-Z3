"""Read files out of the PS3 disc image without mounting it.

The disc is an ISO9660 + UDF hybrid; ISO9660 alone reaches every file we care
about, so this parses that and ignores UDF. It exists because the interesting
containers (notably `DATA/TABATA/TPACKPS3.CPK`, which is a plain CPK and needs
no decryption) can be pulled straight from the image on a machine that has no
emulator installed yet.

    python tools/isoread.py list    <image.iso> [substring]
    python tools/isoread.py extract    <image.iso> <path-substring> <outfile>
    python tools/isoread.py extractall <image.iso> <outdir>
"""
import os
import struct
import sys

SECTOR = 2048


# Joliet supplementary descriptors announce themselves with one of these
JOLIET_ESCAPES = (b"%/@", b"%/C", b"%/E")


class ISO9660:
    """ISO9660, preferring the Joliet tree when the disc carries one.

    This matters: plain ISO9660 truncates names to 31 characters, and this
    disc has longer ones (`SMP_VIDEO_YUV2RGB_CONV_VERTEX.CGELF` is 35). An
    extract built from the ISO9660 tree is missing those files under the names
    the game asks for, and the game hangs waiting on a shader it cannot open.
    Joliet stores the same tree with UCS-2 names and no truncation.
    """

    def __init__(self, path, joliet=True):
        self.fh = open(path, "rb")
        pvd = self._sector(16)
        if pvd[0] != 1 or pvd[1:6] != b"CD001":
            raise SystemExit("%s: no ISO9660 primary volume descriptor" % path)
        self.joliet = False
        if joliet:
            # supplementary descriptors follow the primary, terminated by 255
            for lba in range(17, 32):
                d = self._sector(lba)
                if d[1:6] != b"CD001" or d[0] == 255:
                    break
                if d[0] == 2 and d[88:91] in JOLIET_ESCAPES:
                    pvd = d
                    self.joliet = True
                    break
        # the root directory record is embedded at offset 156 of the descriptor
        self.root = self._record(pvd, 156)[0]

    def _sector(self, lba, n=1):
        self.fh.seek(lba * SECTOR)
        return self.fh.read(n * SECTOR)

    def _record(self, buf, off):
        """One directory record -> (entry, length). Length 0 ends a sector."""
        ln = buf[off]
        if ln == 0:
            return None, 0
        lba = struct.unpack_from("<I", buf, off + 2)[0]     # both-endian: LE half
        size = struct.unpack_from("<I", buf, off + 10)[0]
        flags = buf[off + 25]
        nlen = buf[off + 32]
        raw = buf[off + 33: off + 33 + nlen]
        if len(raw) > 1 and getattr(self, "joliet", False):
            name = raw.decode("utf-16-be", "replace")
        else:
            name = raw.decode("ascii", "replace")
        # both trees append a ";1" version suffix to file identifiers
        if ";" in name:
            name = name.split(";")[0]
        return ({"lba": lba, "size": size, "dir": bool(flags & 0x02),
                 "name": name}, ln)

    def _entries(self, rec):
        n = (rec["size"] + SECTOR - 1) // SECTOR
        buf = self._sector(rec["lba"], n)
        out = []
        for s in range(n):
            off = s * SECTOR
            end = off + SECTOR
            while off < end:
                e, ln = self._record(buf, off)
                if ln == 0:
                    break
                # 0x00 and 0x01 are the "." and ".." records
                if e["name"] not in ("\x00", "\x01"):
                    out.append(e)
                off += ln
        return out

    def walk(self, rec=None, prefix=""):
        for e in self._entries(rec or self.root):
            path = prefix + "/" + e["name"]
            if e["dir"]:
                yield from self.walk(e, path)
            else:
                yield path, e

    def read(self, e):
        self.fh.seek(e["lba"] * SECTOR)
        return self.fh.read(e["size"])

    def copy(self, e, dest, chunk=1 << 22):
        """Stream one file out. The disc holds ~1 GB members, so never pull a
        whole file into memory just to write it straight back out."""
        self.fh.seek(e["lba"] * SECTOR)
        left = e["size"]
        with open(dest, "wb") as out:
            while left:
                buf = self.fh.read(min(chunk, left))
                if not buf:
                    raise IOError("%s: short read, %d bytes missing"
                                  % (dest, left))
                out.write(buf)
                left -= len(buf)


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd, image = argv[1], argv[2]
    iso = ISO9660(image)
    if cmd == "list":
        want = argv[3].upper() if len(argv) > 3 else ""
        n = 0
        for path, e in iso.walk():
            if want and want not in path.upper():
                continue
            print("%12d  %s" % (e["size"], path))
            n += 1
        print("-- %d files" % n)
    elif cmd == "extract":
        if len(argv) < 5:
            print("extract needs <path-substring> <outfile>")
            return 2
        want = argv[3].upper()
        hits = [(p, e) for p, e in iso.walk() if want in p.upper()]
        if not hits:
            raise SystemExit("no file matching %r" % argv[3])
        if len(hits) > 1:
            raise SystemExit("%r is ambiguous:\n  %s"
                             % (argv[3], "\n  ".join(p for p, _ in hits)))
        path, e = hits[0]
        with open(argv[4], "wb") as fh:
            fh.write(iso.read(e))
        print("%s  %d bytes -> %s" % (path, e["size"], argv[4]))
    elif cmd == "extractall":
        if len(argv) < 4:
            print("extractall needs <outdir>")
            return 2
        outdir = argv[3]
        files = list(iso.walk())
        total = sum(e["size"] for _, e in files)
        done = 0
        for i, (path, e) in enumerate(files, 1):
            dest = os.path.join(outdir, path.lstrip("/").replace("/", os.sep))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            iso.copy(e, dest)
            done += e["size"]
            if i % 25 == 0 or i == len(files):
                print("  %3d/%d  %5.1f%%  %s"
                      % (i, len(files), 100.0 * done / total, path[:56]),
                      flush=True)
        print("%d files, %.2f GB -> %s" % (len(files), total / 2 ** 30, outdir))
    else:
        print("unknown command %r" % cmd)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
