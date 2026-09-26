"""CRI CPK archive reader.

SRW Z3 wraps its data in CRI Middleware CPK archives. This parses the @UTF
tables that describe them and extracts member files, transparently
decompressing CRILAYLA where present.

Pure stdlib on purpose: no dependency should stand between a fork and a build.

    python tools/cpk.py list   <file.cpk>
    python tools/cpk.py info   <file.cpk>
    python tools/cpk.py unpack <file.cpk> <outdir>
"""
import os
import struct
import sys

# @UTF column storage classes (flags & 0xf0)
STORAGE_ZERO = 0x10
STORAGE_CONSTANT = 0x30
STORAGE_PERROW = 0x50

# @UTF value types (flags & 0x0f) -> (struct code, byte width)
TYPES = {
    0x00: ("B", 1), 0x01: ("b", 1),
    0x02: (">H", 2), 0x03: (">h", 2),
    0x04: (">I", 4), 0x05: (">i", 4),
    0x06: (">Q", 8), 0x07: (">q", 8),
    0x08: (">f", 4), 0x09: (">d", 8),
    0x0A: ("string", 4),
    0x0B: ("bytes", 8),
}


class UTFTable:
    """One @UTF table: a schema plus rows, addressed by column name."""

    def __init__(self, buf, base=0):
        if buf[base:base + 4] != b"@UTF":
            raise ValueError("not an @UTF table at 0x%x" % base)
        self.size = struct.unpack_from(">I", buf, base + 4)[0]
        d = base + 8  # every offset below is relative to here

        (rows_off, str_off, data_off, name_off,
         n_cols, row_len, n_rows) = struct.unpack_from(">IIIIHHI", buf, d)

        self.buf = buf
        self.field_offset = {}   # (row, column) -> absolute offset of the value
        self.blob_offset = {}    # (row, column) -> absolute offset of blob data
        self.strings = buf[d + str_off: d + data_off]
        self.name = self._str(name_off)
        self.n_rows = n_rows

        # --- schema ---
        self.columns = []   # (name, flags, constant_or_None)
        p = d + 0x18
        for _ in range(n_cols):
            flags = buf[p]
            p += 1
            cname = self._str(struct.unpack_from(">I", buf, p)[0])
            p += 4
            const = None
            if flags & 0xF0 == STORAGE_CONSTANT:
                const, p = self._read(buf, p, flags & 0x0F, d + data_off)
            self.columns.append((cname, flags, const))

        # --- rows ---
        self.rows = []
        for r in range(n_rows):
            p = d + rows_off + r * row_len
            row = {}
            for cname, flags, const in self.columns:
                store = flags & 0xF0
                if store == STORAGE_ZERO:
                    row[cname] = 0
                elif store == STORAGE_CONSTANT:
                    row[cname] = const
                else:
                    self.field_offset[(r, cname)] = p
                    typ = flags & 0x0F
                    if typ == 0x0B:
                        off, _ln = struct.unpack_from(">II", buf, p)
                        self.blob_offset[(r, cname)] = d + data_off + off
                    row[cname], p = self._read(buf, p, typ, d + data_off)
            self.rows.append(row)

    def _str(self, off):
        end = self.strings.find(b"\0", off)
        return self.strings[off:end].decode("utf-8", "replace")

    def _read(self, buf, p, typ, data_base):
        if typ not in TYPES:
            raise ValueError("unknown @UTF type 0x%x" % typ)
        code, width = TYPES[typ]
        if code == "string":
            return self._str(struct.unpack_from(">I", buf, p)[0]), p + 4
        if code == "bytes":
            off, ln = struct.unpack_from(">II", buf, p)
            return buf[data_base + off: data_base + off + ln], p + 8
        if width == 1:
            return struct.unpack_from(">" + code, buf, p)[0], p + 1
        return struct.unpack_from(code, buf, p)[0], p + width

    def get(self, row, key, default=None):
        return self.rows[row].get(key, default)

    def column_type(self, key):
        for cname, flags, _const in self.columns:
            if cname == key:
                return flags & 0x0F
        raise KeyError(key)

    def patch(self, buf, row, key, value):
        """Overwrite one per-row integer in `buf` (a bytearray) in place.
        Only valid for per-row columns; constants are shared by every row."""
        off = self.field_offset.get((row, key))
        if off is None:
            raise KeyError("%r is not a per-row field" % key)
        code, width = TYPES[self.column_type(key)]
        if width == 1:
            struct.pack_into(">" + code, buf, off, value)
        else:
            struct.pack_into(code, buf, off, value)


def decompress_crilayla(src):
    """CRILAYLA: LZ variant that emits its output back-to-front."""
    if src[:8] != b"CRILAYLA":
        return src
    usize, dsize = struct.unpack_from("<II", src, 8)
    header = src[0x10 + dsize: 0x10 + dsize + 0x100]  # raw 0x100 prefix
    out = bytearray(usize)

    pos = 0x10 + dsize - 1   # bits are consumed backwards
    pool = bits = 0

    def take(n):
        nonlocal pos, pool, bits
        v = 0
        while n:
            if not bits:
                pool = src[pos]
                pos -= 1
                bits = 8
            k = min(n, bits)
            v = (v << k) | ((pool >> (bits - k)) & ((1 << k) - 1))
            bits -= k
            n -= k
        return v

    VLE = (2, 3, 5, 8)
    o = usize - 1
    while o >= 0:
        if take(1):
            ref = o + take(13) + 3
            ln = 3
            for width in VLE:
                d = take(width)
                ln += d
                if d != (1 << width) - 1:
                    break
            else:
                while True:
                    d = take(8)
                    ln += d
                    if d != 255:
                        break
            for _ in range(ln):
                out[o] = out[ref]
                o -= 1
                ref -= 1
                if o < 0:
                    break
        else:
            out[o] = take(8)
            o -= 1
    return header + bytes(out)


class CPK:
    def __init__(self, path):
        self.path = path
        with open(path, "rb") as fh:
            self.buf = fh.read()
        if self.buf[:4] != b"CPK ":
            raise ValueError("%s: not a CPK" % path)
        self.header = UTFTable(self.buf, 0x10)
        self.files = self._toc() or self._itoc()

    def _h(self, key):
        return self.header.get(0, key)

    def _toc(self):
        toc_off = self._h("TocOffset") or 0
        if not toc_off:
            return []
        content = self._h("ContentOffset") or 0
        # file offsets are relative to whichever of the two comes first
        base = min(toc_off, content) if content else toc_off
        toc = UTFTable(self.buf, toc_off + 0x10)
        out = []
        for r in range(toc.n_rows):
            out.append({
                "dir": toc.get(r, "DirName", "") or "",
                "name": toc.get(r, "FileName", ""),
                "size": toc.get(r, "FileSize", 0),
                "extract": toc.get(r, "ExtractSize", 0),
                "offset": base + (toc.get(r, "FileOffset", 0) or 0),
                "id": toc.get(r, "ID", r),
            })
        return out

    def _itoc(self):
        """ITOC layout: no filenames. Files are identified by ID and laid out
        back to back from ContentOffset, each padded up to Align."""
        itoc_off = self._h("ItocOffset") or 0
        if not itoc_off:
            return []
        itoc = UTFTable(self.buf, itoc_off + 0x10)
        sizes = {}
        for key in ("DataL", "DataH"):   # 16-bit and 32-bit size tables
            blob = itoc.get(0, key)
            if not blob:
                continue
            sub = UTFTable(blob, 0)
            for r in range(sub.n_rows):
                sizes[sub.get(r, "ID")] = (sub.get(r, "FileSize", 0),
                                           sub.get(r, "ExtractSize", 0))
        align = self._h("Align") or 1
        off = self._h("ContentOffset") or 0
        out = []
        for i in sorted(sizes):
            size, extract = sizes[i]
            out.append({"dir": "", "name": "%05d.bin" % i, "size": size,
                        "extract": extract, "offset": off, "id": i})
            off += size
            if align and off % align:
                off += align - (off % align)
        return out

    def read(self, entry):
        raw = self.buf[entry["offset"]: entry["offset"] + entry["size"]]
        if entry["extract"] and entry["extract"] != entry["size"]:
            return decompress_crilayla(raw)
        return raw

    def unpack(self, outdir):
        n = 0
        for e in self.files:
            rel = os.path.join(e["dir"].replace("/", os.sep), e["name"])
            dest = os.path.join(outdir, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(dest, "wb") as fh:
                fh.write(self.read(e))
            n += 1
        return n


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd, path = argv[1], argv[2]
    cpk = CPK(path)
    if cmd == "info":
        print("%s\n  files=%d" % (path, len(cpk.files)))
        for k, _f, _c in cpk.header.columns:
            print("  %-20s %s" % (k, cpk.header.get(0, k)))
    elif cmd == "list":
        for e in cpk.files:
            flag = "CRILAYLA" if e["extract"] != e["size"] else ""
            print("%10d %10d  %-8s %s/%s"
                  % (e["size"], e["extract"], flag, e["dir"], e["name"]))
        print("-- %d files" % len(cpk.files))
    elif cmd == "unpack":
        if len(argv) < 4:
            print("unpack needs an output directory")
            return 2
        print("%d files -> %s" % (cpk.unpack(argv[3]), argv[3]))
    else:
        print("unknown command %r" % cmd)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
