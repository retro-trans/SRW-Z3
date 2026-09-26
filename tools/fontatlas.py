"""Extract the dialogue font atlas and measure per-glyph ink widths.

The atlas lives in `DATA/TABATA/TPACKPS3.CPK` as the two 16bpp members
(format byte 0xAB), 4096x1120 each, laid out as a grid of 32x32 cells:
128 columns x 35 rows = 4480 cells per page.

The glyphs are already **proportional** -- measured ink runs 8px for `i`/`l`
up to 24px for `h`, inside a 32px cell. The renderer nonetheless advances a
full cell per glyph, which is why English reads as spaced out. Any fix needs
these real widths, which is what this produces.

    python3 tools/fontatlas.py <TPACKPS3.CPK> <outdir>

Writes page PNGs plus metrics.json: for every cell, the ink bounding box and
advance width.  Needs python3 (the 3.12 interpreter), not the venv python.
"""
import json
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

CELL = 32
FONT_FORMAT = 0xAB          # 16bpp; the 32bpp members are artwork


def alpha_plane(px, w, h):
    """16bpp -> one byte of coverage per pixel."""
    out = bytearray(w * h)
    for i in range(w * h):
        v = (px[i * 2] << 8) | px[i * 2 + 1]
        # take the strongest nibble so this works whatever the channel order is
        out[i] = max((v >> 12) & 0xF, (v >> 8) & 0xF,
                     (v >> 4) & 0xF, v & 0xF) * 17
    return out


def write_png(gray, w, h, path):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += gray[y * w:(y + 1) * w]

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n"
                 + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
                 + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
                 + chunk(b"IEND", b""))


def measure(gray, w, h, threshold=32):
    """Ink bounding box per cell."""
    cells = []
    for row in range(h // CELL):
        for col in range(w // CELL):
            x0, y0 = col * CELL, row * CELL
            left, right, top, bottom = CELL, -1, CELL, -1
            for y in range(y0, y0 + CELL):
                base = y * w
                for x in range(x0, x0 + CELL):
                    if gray[base + x] > threshold:
                        dx, dy = x - x0, y - y0
                        if dx < left: left = dx
                        if dx > right: right = dx
                        if dy < top: top = dy
                        if dy > bottom: bottom = dy
            blank = right < 0
            cells.append({
                "index": row * (w // CELL) + col,
                "row": row, "col": col,
                "blank": blank,
                "left": None if blank else left,
                "right": None if blank else right,
                "width": 0 if blank else right - left + 1,
                "top": None if blank else top,
                "bottom": None if blank else bottom,
            })
    return cells


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cpk, outdir = argv[1], argv[2]
    os.makedirs(outdir, exist_ok=True)
    k = CPK(cpk)
    pages = 0
    summary = {}
    for e in k.files:
        b = k.read(e)
        if len(b) < 0x80 or b[0x18] != FONT_FORMAT:
            continue
        w, h = struct.unpack_from(">H", b, 0x20)[0], struct.unpack_from(">H", b, 0x22)[0]
        gray = alpha_plane(b[0x80:], w, h)
        png = os.path.join(outdir, "atlas_%d.png" % e["id"])
        write_png(gray, w, h, png)
        cells = measure(gray, w, h)
        used = [c for c in cells if not c["blank"]]
        widths = sorted(c["width"] for c in used)
        summary["page_%d" % e["id"]] = {
            "width": w, "height": h, "cell": CELL,
            "cells": len(cells), "non_blank": len(used),
            "width_min": widths[0] if widths else 0,
            "width_max": widths[-1] if widths else 0,
            "width_median": widths[len(widths) // 2] if widths else 0,
            "cells_detail": cells,
        }
        print("page id=%d  %dx%d  %d cells, %d inked, ink width %d-%d (median %d)"
              % (e["id"], w, h, len(cells), len(used),
                 widths[0] if widths else 0, widths[-1] if widths else 0,
                 widths[len(widths) // 2] if widths else 0))
        print("   -> %s" % png)
        pages += 1
    with open(os.path.join(outdir, "metrics.json"), "w") as fh:
        json.dump(summary, fh, indent=1)
    print("%d atlas pages -> %s/metrics.json" % (pages, outdir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
