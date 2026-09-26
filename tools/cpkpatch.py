"""Rebuild an ITOC CPK with replacement members.

Why this exists: CriPakTools cannot rebuild ITOC archives. It writes the
content region on 0x800 boundaries while leaving the ITOC implying the packed
layout, so even its own reader then points at padding. ITOC has no FileOffset
column, so the reader recomputes positions and the writer's layout rule has to
match it exactly.

The rule, verified against every member of an untouched STG*.SDAT: members sit
back to back from ContentOffset, each padded up to Align (16).

Replacements are stored UNCOMPRESSED (ExtractSize == FileSize), which is legal
and avoids needing a CRILAYLA compressor. Untouched members keep their original
bytes verbatim, still compressed.

    python tools/cpkpatch.py <in.cpk> <out.cpk> --replace 3=new3.lua [5=new5.lua]
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK, UTFTable   # noqa: E402

NUL = bytes(1)


def validate_itoc(buf):
    """Check the lengths the runtime uses, not just our permissive reader."""
    header = UTFTable(buf, 0x10)
    offset = header.get(0, "ItocOffset") or 0
    if not offset:
        raise ValueError("missing ITOC")
    chunk_size = struct.unpack_from("<Q", buf, offset + 8)[0]
    table = UTFTable(buf, offset + 16)
    actual_size = 16 + table.size + 8
    declared_size = header.get(0, "ItocSize")
    if declared_size != actual_size or chunk_size != table.size + 8:
        raise ValueError("ITOC length mismatch: header=%s, chunk=%d, table=%d"
                         % (declared_size, 16 + chunk_size, actual_size))
    if offset + actual_size > header.get(0, "ContentOffset"):
        raise ValueError("ITOC overlaps member payloads")
    ids = []
    for key, count in (("DataL", "FilesL"), ("DataH", "FilesH")):
        blob = table.get(0, key)
        sub = UTFTable(blob) if blob else None
        rows = sub.n_rows if sub else 0
        if rows != table.get(0, count):
            raise ValueError("ITOC %s count mismatch" % key)
        if sub:
            ids.extend(sub.get(i, "ID") for i in range(rows))
    if len(ids) != len(set(ids)) or len(ids) != header.get(0, "Files"):
        raise ValueError("ITOC member IDs/count mismatch")


def build(src, dst, replacements):
    cpk = CPK(src)
    if not cpk.files:
        raise SystemExit("%s: no members (is this an ITOC CPK?)" % src)

    itoc_off = cpk._h("ItocOffset") or 0
    if not itoc_off:
        raise SystemExit("%s: not an ITOC CPK; this tool only handles ITOC" % src)

    content_off = cpk._h("ContentOffset") or 0
    align = cpk._h("Align") or 1

    buf = bytearray(cpk.buf)
    itoc = UTFTable(cpk.buf, itoc_off + 0x10)

    # locate every member's size fields inside the DataL/DataH sub-tables
    where = {}   # id -> (blob_abs_offset, sub_table, row)
    for key in ("DataL", "DataH"):
        blob = itoc.get(0, key)
        if not blob:
            continue
        blob_abs = itoc.blob_offset[(0, key)]
        sub = UTFTable(blob, 0)
        for r in range(sub.n_rows):
            where[sub.get(r, "ID")] = (blob_abs, sub, r)

    # gather payloads in ID order
    payloads = []
    for e in cpk.files:
        fid = e["id"]
        if fid in replacements:
            with open(replacements[fid], "rb") as replacement:
                data = replacement.read()
            payloads.append((fid, data, len(data), len(data)))   # uncompressed
        else:
            raw = cpk.buf[e["offset"]: e["offset"] + e["size"]]
            payloads.append((fid, raw, e["size"], e["extract"]))

    # A replacement can outgrow the 16-bit DataL columns (English stage 3
    # member 3 is 68 KB uncompressed against a 52 KB Japanese original). The
    # game's own archives keep such members in DataH (32-bit), and the reader
    # merges both tables sorted by ID, so moving the row is layout-safe.
    moved = []
    for fid, _data, size, extract in payloads:
        if fid not in where:
            raise SystemExit("id %d has no ITOC entry" % fid)
        _blob_abs, sub, _row = where[fid]
        _code, width = _coltype(sub, "FileSize")
        if width == 2 and max(size, extract) > 0xFFFF:
            _move_to_datah(buf, cpk, fid)
            moved.append(fid)
    if moved:
        itoc = UTFTable(buf, itoc_off + 0x10)
        where = {}
        for key in ("DataL", "DataH"):
            blob = itoc.get(0, key)
            if not blob:
                continue
            blob_abs = itoc.blob_offset[(0, key)]
            sub = UTFTable(blob, 0)
            for r in range(sub.n_rows):
                where[sub.get(r, "ID")] = (blob_abs, sub, r)
        print("  ids %s moved DataL -> DataH (size outgrew 16 bits)"
              % ",".join(map(str, moved)))

    # patch the size tables, refusing anything that would not fit its column
    for fid, _data, size, extract in payloads:
        if fid not in where:
            raise SystemExit("id %d has no ITOC entry" % fid)
        blob_abs, sub, row = where[fid]
        for col, val in (("FileSize", size), ("ExtractSize", extract)):
            code, width = _coltype(sub, col)
            limit = (1 << (width * 8)) - 1
            if val > limit:
                raise SystemExit(
                    "id %d: %s=%d overflows the %d-bit %s column. It would have "
                    "to move to DataH, which this tool does not do."
                    % (fid, col, val, width * 8,
                       "DataL" if width == 2 else "DataH"))
            off = blob_abs + sub.field_offset[(row, col)]
            struct.pack_into(code if width > 1 else ">" + code, buf, off, val)

    # Keep only the output header in memory. Large effects archives otherwise
    # require another full-size bytearray and can exhaust 32-bit Python.
    out = bytearray(buf[:content_off])
    del buf

    # Header size fields, decoded from an untouched archive:
    #   ContentSize       aligned total, INCLUDING a final pad the file omits
    #   EnabledDataSize   sum of FileSize    (stored sizes)
    #   EnabledPackedSize sum of ExtractSize (unpacked sizes)
    aligned_total = 0
    for _fid, _data, size, _extract in payloads:
        aligned_total += size
        if align and aligned_total % align:
            aligned_total += align - (aligned_total % align)

    for col, val in (("ContentSize", aligned_total),
                     ("EnabledDataSize", sum(p[2] for p in payloads)),
                     ("EnabledPackedSize", sum(p[3] for p in payloads))):
        try:
            cpk.header.patch(out, 0, col, val)
        except (KeyError, struct.error):
            pass

    validate_itoc(out)
    with open(dst, "wb") as fh:
        fh.write(out)
        pos = content_off
        for i, (_fid, data, size, _extract) in enumerate(payloads):
            fh.write(data)
            pos += size
            # Match the original archive: padding BETWEEN members, not EOF.
            if i != len(payloads)-1 and align and pos % align:
                pad = align - (pos % align)
                fh.write(b'\0' * pad)
                pos += pad
    return len(payloads), pos


def _coltype(table, col):
    from cpk import TYPES
    return TYPES[table.column_type(col)]


def _rows_edit(blob, edit):
    """Return a sub-@UTF blob with its fixed-size integer rows replaced by
    `edit(rows)`. Schema and strings are untouched; the string/data offsets
    and the table size shift by the row-area delta. Only valid for tables
    whose rows carry no string or blob columns (CpkItocL/CpkItocH)."""
    assert blob[:4] == b"@UTF", "not a @UTF sub-table"
    size = struct.unpack_from(">I", blob, 4)[0]
    d = 8
    rows_off, str_off, data_off, name_off, n_cols, row_len, n_rows = \
        struct.unpack_from(">IIIIHHI", blob, d)
    rstart, rend = d + rows_off, d + rows_off + row_len * n_rows
    rows = [bytes(blob[rstart + i * row_len: rstart + (i + 1) * row_len])
            for i in range(n_rows)]
    rows = edit(rows)
    # An archive whose CpkItocH is EMPTY declares row_len 0 (STG0019 ships
    # that way). Adding the first row there has to establish the row length
    # from the row itself, or the table stays 0 x 0 and the reader sees no
    # entry -- which is exactly how "id 3 has no ITOC entry" happened.
    new_row_len = row_len
    if rows:
        widths = {len(r) for r in rows}
        if len(widths) != 1:
            raise SystemExit("sub-@UTF rows differ in length: %s" % sorted(widths))
        w = widths.pop()
        if row_len and w != row_len:
            raise SystemExit("row length %d does not match the table's %d" % (w, row_len))
        new_row_len = w
    delta = new_row_len * len(rows) - (rend - rstart)
    out = bytearray(blob[:rstart]) + b"".join(rows) + blob[rend:]
    struct.pack_into(">I", out, 4, size + delta)
    struct.pack_into(">I", out, d + 4, str_off + delta)
    struct.pack_into(">I", out, d + 8, data_off + delta)
    struct.pack_into(">H", out, d + 18, new_row_len)
    struct.pack_into(">I", out, d + 20, len(rows))
    return bytes(out)


def _build_datah(rows):
    """A correct, freshly built CpkItocH sub-@UTF holding `rows`.

    Some archives (STG0019) ship an EMPTY CpkItocH whose schema is a
    placeholder: row_len 0, the ID column flagged STORAGE_ZERO and the other
    two columns all-zero bytes. No row can be inserted into that, so when a
    member outgrows DataL's 16-bit sizes we replace the whole table with one
    built to the same shape the populated archives use (per-row ID u16,
    FileSize u32, ExtractSize u32; string blob identical to CpkItocL's but
    naming CpkItocH).
    """
    strings = b"".join((b"<NULL>", NUL, b"CpkItocH", NUL, b"ID", NUL,
                        b"FileSize", NUL, b"ExtractSize", NUL))
    name_off, id_off, fs_off, es_off = 7, 16, 19, 28
    schema = (struct.pack(">BI", 0x52, id_off)
              + struct.pack(">BI", 0x54, fs_off)
              + struct.pack(">BI", 0x54, es_off))
    row_len = 10
    rows_off = 24 + len(schema)
    body = b"".join(rows)
    str_off = rows_off + len(body)
    data_off = str_off + len(strings)
    head = struct.pack(">IIIIHHI", rows_off, str_off, data_off, name_off,
                       3, row_len, len(rows))
    blob = head + schema + body + strings
    return b"@UTF" + struct.pack(">I", len(blob)) + blob


def _datah_is_usable(dh):
    """True when an existing CpkItocH can take another row."""
    if not dh:
        return False
    try:
        sub = UTFTable(dh, 0)
        if sub.n_rows == 0:
            return False
        for col, want in (("ID", 0x02), ("FileSize", 0x04), ("ExtractSize", 0x04)):
            if sub.column_type(col) != want:
                return False
        return all((0, c) in sub.field_offset for c in ("ID", "FileSize", "ExtractSize"))
    except Exception:
        return False

def _move_to_datah(buf, cpk, fid):
    """Move one member's size row from CpkItocL (u16) to CpkItocH (u32),
    rewriting the ITOC in place. The chunk grows by 4 bytes into its own
    padding; ContentOffset does not move."""
    import bisect
    itoc_off = cpk._h("ItocOffset")
    content = cpk._h("ContentOffset")
    base = itoc_off + 0x10
    parent = UTFTable(buf, base)
    dl, dh = parent.get(0, "DataL"), parent.get(0, "DataH")
    if not dl:
        raise SystemExit("ITOC lacks DataL; cannot move id %d" % fid)
    subL = UTFTable(dl, 0)
    rl = [r for r in range(subL.n_rows) if subL.get(r, "ID") == fid]
    if len(rl) != 1:
        raise SystemExit("id %d not exactly once in DataL" % fid)
    fs, es = subL.get(rl[0], "FileSize"), subL.get(rl[0], "ExtractSize")
    new_row = struct.pack(">HII", fid, fs, es)
    newL = _rows_edit(dl, lambda rows: [r for i, r in enumerate(rows) if i != rl[0]])

    def add(rows):
        ids = [struct.unpack_from(">H", r, 0)[0] for r in rows]
        i = bisect.bisect(ids, fid)
        return rows[:i] + [new_row] + rows[i:]
    if _datah_is_usable(dh):
        subH = UTFTable(dh, 0)
        for col, want in (("ID", 0x02), ("FileSize", 0x04), ("ExtractSize", 0x04)):
            if subH.column_type(col) != want:
                raise SystemExit("unexpected CpkItocH schema (%s)" % col)
        newH = _rows_edit(dh, add)
    else:
        d2 = 8
        n_rows_h = struct.unpack_from(">I", dh, d2 + 20)[0] if dh else 0
        if n_rows_h:
            raise SystemExit("CpkItocH has %d rows but is unreadable" % n_rows_h)
        newH = _build_datah(add([]))

    d = base + 8
    data_off = struct.unpack_from(">I", buf, d + 8)[0]
    data_abs = d + data_off
    old_end = base + 8 + parent.size
    new_data = newL + newH
    delta = len(new_data) - (old_end - data_abs)
    pad = content - (data_abs + len(new_data))
    if pad < 0:
        raise SystemExit("ITOC would overrun ContentOffset moving id %d" % fid)
    buf[data_abs:content] = new_data + b"\0" * pad
    struct.pack_into(">I", buf, base + 4, parent.size + delta)          # @UTF size
    csz = struct.unpack_from("<I", buf, itoc_off + 8)[0]                # chunk size, LE
    struct.pack_into("<I", buf, itoc_off + 8, csz + delta)
    parent.patch(buf, 0, "FilesL", parent.get(0, "FilesL") - 1)
    parent.patch(buf, 0, "FilesH", parent.get(0, "FilesH") + 1)
    oL = parent.field_offset[(0, "DataL")]
    struct.pack_into(">II", buf, oL, 0, len(newL))
    oH = parent.field_offset[(0, "DataH")]
    struct.pack_into(">II", buf, oH, len(newL), len(newH))
    try:                                    # header ItocSize, where present
        if cpk._h("ItocSize"):
            # Derive from the newly written chunk. The source header is stale
            # after the first promotion; old + delta lost earlier growth when
            # TWO dialogue members crossed 64 KiB (e.g. STG0018).
            cpk.header.patch(buf, 0, "ItocSize", 16 + csz + delta)
    except (KeyError, struct.error):
        pass


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--replace", nargs="+", default=[], metavar="ID=FILE")
    a = ap.parse_args(argv)

    reps = {}
    for item in a.replace:
        if "=" not in item:
            raise SystemExit("--replace wants ID=FILE, got %r" % item)
        k, v = item.split("=", 1)
        reps[int(k)] = v

    n, size = build(a.src, a.dst, reps)
    print("%d members, %d replaced -> %s (%d bytes)"
          % (n, len(reps), a.dst, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
