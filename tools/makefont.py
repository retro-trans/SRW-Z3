"""Draw an original Latin face into the game's font atlas.

Why this exists: the shipped Latin glyphs are properly proportional (8px `i`,
24px `h`) but the renderer advances a fixed ~37.28px regardless, so English
reads as tiny letters separated by large gaps. The advance is a code constant
with no width table to edit, so until it is patched the only lever is the
glyph art: draw letters that fill the 32px cell, and the gap drops to ~14% of
pitch -- clean monospace instead of broken-looking text.

The letterforms here are original: a geometric sans defined as stroke
skeletons and rasterised with an anti-aliased signed-distance pen. No existing
typeface is copied or embedded.

    python3 tools/makefont.py <TPACKPS3.CPK> <out.CPK> [--preview out.png]
"""
import math
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK          # noqa: E402

CELL = 32
ATLAS_FORMAT = 0xAB
CELLS_PER_ROW = 128
SJIS_OFFSET = 0              # unused; see cell_index (flat 192 stride)

# --- cell geometry -------------------------------------------------------
# generous width so glyphs fill the em and the fixed gap looks deliberate
X0, X1 = 3.0, 28.0           # left/right of the drawing box
CAP, BASE = 5.0, 26.0        # cap top, baseline
XH = 13.0                    # x-height top
DESC = 30.5                  # descender depth
PEN = 3.0                    # stroke thickness


def lerp(a, b, t):
    return a + (b - a) * t


def X(t):
    return lerp(X0, X1, t)


def Y(t):
    """0 = cap top, 1 = baseline; values outside that range are legal."""
    return lerp(CAP, BASE, t)


def L(x1, y1, x2, y2):
    return ("L", X(x1), Y(y1), X(x2), Y(y2))


def A(cx, cy, rx, ry, a0, a1):
    return ("A", X(cx), Y(cy), rx * (X1 - X0) / 2.0, ry * (BASE - CAP) / 2.0,
            math.radians(a0), math.radians(a1))


def arc_pts(g, n=26):
    _, cx, cy, rx, ry, a0, a1 = g
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n),
             cy + ry * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]


def segments(strokes):
    segs = []
    for g in strokes:
        if g[0] == "L":
            segs.append((g[1], g[2], g[3], g[4]))
        else:
            p = arc_pts(g)
            segs += [(p[i][0], p[i][1], p[i + 1][0], p[i + 1][1])
                     for i in range(len(p) - 1)]
    return segs


def dist_seg(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    d2 = dx * dx + dy * dy
    t = 0.0 if d2 == 0 else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / d2))
    qx, qy = x1 + t * dx, y1 + t * dy
    return math.hypot(px - qx, py - qy)


def raster(strokes):
    """Anti-aliased 32x32 coverage via distance to the stroke skeleton."""
    segs = segments(strokes)
    cell = bytearray(CELL * CELL)
    if not segs:
        return cell
    half = PEN / 2.0
    for y in range(CELL):
        for x in range(CELL):
            px, py = x + 0.5, y + 0.5
            d = min(dist_seg(px, py, *s) for s in segs)
            a = half + 0.5 - d
            if a > 0:
                cell[y * CELL + x] = 255 if a >= 1 else int(a * 255)
    return cell


def P(*pts):
    """A polyline. Curves are polygonal here; at 32px with a 3px pen and
    anti-aliasing the difference from true arcs is not visible."""
    return ("P", pts)


def segments2(shapes):
    segs = []
    for kind, pts in shapes:
        for i in range(len(pts) - 1):
            (a, b), (c, d) = pts[i], pts[i + 1]
            segs.append((X(a), Y(b), X(c), Y(d)))
    return segs


XT = 0.38          # x-height top
DS = 1.21          # descender depth

O_RING = [(0.5, 0), (0.85, 0.13), (1, 0.5), (0.85, 0.87), (0.5, 1),
          (0.15, 0.87), (0, 0.5), (0.15, 0.13), (0.5, 0)]
o_ring = [(0.5, XT), (0.83, 0.5), (0.96, 0.69), (0.83, 0.9), (0.5, 1),
          (0.17, 0.9), (0.04, 0.69), (0.17, 0.5), (0.5, XT)]
a_bowl = [(0.9, 0.55), (0.65, XT), (0.3, XT), (0.06, 0.55), (0.06, 0.85),
          (0.3, 1), (0.65, 1), (0.9, 0.85)]

GLYPHS = {
 "A": [P((0,1),(0.5,0),(1,1)), P((0.18,0.62),(0.82,0.62))],
 "B": [P((0,0),(0,1)), P((0,0),(0.62,0),(0.87,0.14),(0.87,0.36),(0.6,0.5),(0,0.5)),
       P((0.6,0.5),(0.92,0.64),(0.92,0.86),(0.64,1),(0,1))],
 "C": [P((0.96,0.16),(0.7,0),(0.3,0),(0.04,0.22),(0.04,0.78),(0.3,1),(0.7,1),(0.96,0.84))],
 "D": [P((0,0),(0,1)), P((0,0),(0.55,0),(0.92,0.26),(0.92,0.74),(0.55,1),(0,1))],
 "E": [P((0.95,0),(0,0),(0,1),(0.95,1)), P((0,0.5),(0.75,0.5))],
 "F": [P((0.95,0),(0,0),(0,1)), P((0,0.5),(0.72,0.5))],
 "G": [P((0.96,0.16),(0.7,0),(0.3,0),(0.04,0.22),(0.04,0.78),(0.3,1),(0.72,1),(0.96,0.8),(0.96,0.56),(0.56,0.56))],
 "H": [P((0,0),(0,1)), P((1,0),(1,1)), P((0,0.5),(1,0.5))],
 "I": [P((0.2,0),(0.8,0)), P((0.5,0),(0.5,1)), P((0.2,1),(0.8,1))],
 "J": [P((0.78,0),(0.78,0.78),(0.56,1),(0.26,1),(0.05,0.8))],
 "K": [P((0,0),(0,1)), P((0.95,0),(0.04,0.56)), P((0.34,0.38),(0.97,1))],
 "L": [P((0,0),(0,1),(0.9,1))],
 "M": [P((0,1),(0,0),(0.5,0.64),(1,0),(1,1))],
 "N": [P((0,1),(0,0),(1,1),(1,0))],
 "O": [P(*O_RING)],
 "P": [P((0,1),(0,0),(0.66,0),(0.93,0.16),(0.93,0.4),(0.66,0.56),(0,0.56))],
 "Q": [P(*O_RING), P((0.62,0.72),(1.0,1.06))],
 "R": [P((0,1),(0,0),(0.66,0),(0.93,0.16),(0.93,0.4),(0.66,0.56),(0,0.56)), P((0.5,0.56),(0.97,1))],
 "S": [P((0.93,0.14),(0.66,0),(0.3,0),(0.05,0.16),(0.05,0.38),(0.3,0.5),(0.7,0.52),(0.95,0.64),(0.95,0.86),(0.7,1),(0.32,1),(0.05,0.86))],
 "T": [P((0,0),(1,0)), P((0.5,0),(0.5,1))],
 "U": [P((0,0),(0,0.76),(0.24,1),(0.76,1),(1,0.76),(1,0))],
 "V": [P((0,0),(0.5,1),(1,0))],
 "W": [P((0,0),(0.22,1),(0.5,0.36),(0.78,1),(1,0))],
 "X": [P((0,0),(1,1)), P((1,0),(0,1))],
 "Y": [P((0,0),(0.5,0.52),(1,0)), P((0.5,0.52),(0.5,1))],
 "Z": [P((0,0),(1,0),(0,1),(1,1))],

 "a": [P(*a_bowl), P((0.9,XT),(0.9,1))],
 "b": [P((0.05,0),(0.05,1)), P((0.05,0.55),(0.3,XT),(0.66,XT),(0.9,0.55),(0.9,0.85),(0.66,1),(0.3,1),(0.05,0.85))],
 "c": [P((0.9,0.52),(0.65,XT),(0.32,XT),(0.06,0.56),(0.06,0.84),(0.32,1),(0.65,1),(0.9,0.88))],
 "d": [P((0.93,0),(0.93,1)), P((0.93,0.55),(0.68,XT),(0.32,XT),(0.08,0.55),(0.08,0.85),(0.32,1),(0.68,1),(0.93,0.85))],
 "e": [P((0.06,0.69),(0.93,0.69),(0.93,0.53),(0.68,XT),(0.34,XT),(0.06,0.56),(0.06,0.85),(0.32,1),(0.7,1),(0.92,0.9))],
 "f": [P((0.86,0.08),(0.62,0),(0.42,0.14),(0.42,1)), P((0.1,0.42),(0.8,0.42))],
 "g": [P(*a_bowl), P((0.9,XT),(0.9,1.09),(0.66,DS),(0.3,DS),(0.1,1.12))],
 "h": [P((0.06,0),(0.06,1)), P((0.06,0.56),(0.32,XT),(0.68,XT),(0.93,0.58),(0.93,1))],
 "i": [P((0.5,XT),(0.5,1)), P((0.5,0.13),(0.5,0.19))],
 "j": [P((0.62,XT),(0.62,1.09),(0.42,DS),(0.18,1.17)), P((0.62,0.13),(0.62,0.19))],
 "k": [P((0.08,0),(0.08,1)), P((0.86,XT),(0.09,0.78)), P((0.42,0.63),(0.92,1))],
 "l": [P((0.36,0),(0.36,0.9),(0.6,1))],
 "m": [P((0.03,1),(0.03,XT)), P((0.03,0.5),(0.24,XT),(0.45,0.5),(0.45,1)), P((0.45,0.5),(0.68,XT),(0.93,0.52),(0.93,1))],
 "n": [P((0.06,1),(0.06,XT)), P((0.06,0.56),(0.32,XT),(0.68,XT),(0.93,0.58),(0.93,1))],
 "o": [P(*o_ring)],
 "p": [P((0.05,XT),(0.05,DS)), P((0.05,0.55),(0.3,XT),(0.66,XT),(0.9,0.55),(0.9,0.85),(0.66,1),(0.3,1),(0.05,0.85))],
 "q": [P((0.93,XT),(0.93,DS)), P((0.93,0.55),(0.68,XT),(0.32,XT),(0.08,0.55),(0.08,0.85),(0.32,1),(0.68,1),(0.93,0.85))],
 "r": [P((0.12,1),(0.12,XT)), P((0.12,0.57),(0.4,0.4),(0.76,XT))],
 "s": [P((0.9,0.5),(0.62,XT),(0.3,XT),(0.09,0.5),(0.09,0.63),(0.36,0.7),(0.68,0.73),(0.9,0.83),(0.88,0.95),(0.62,1),(0.28,1),(0.07,0.9))],
 "t": [P((0.36,0.1),(0.36,0.88),(0.56,1),(0.76,0.95)), P((0.1,0.4),(0.68,0.4))],
 "u": [P((0.06,XT),(0.06,0.82),(0.3,1),(0.66,1),(0.93,0.82)), P((0.93,XT),(0.93,1))],
 "v": [P((0.05,XT),(0.5,1),(0.95,XT))],
 "w": [P((0.02,XT),(0.25,1),(0.5,0.63),(0.75,1),(0.98,XT))],
 "x": [P((0.08,XT),(0.92,1)), P((0.92,XT),(0.08,1))],
 "y": [P((0.05,XT),(0.5,1)), P((0.95,XT),(0.3,DS))],
 "z": [P((0.08,XT),(0.92,XT),(0.08,1),(0.92,1))],

 "0": [P(*O_RING)],
 "1": [P((0.24,0.18),(0.5,0),(0.5,1)), P((0.22,1),(0.78,1))],
 "2": [P((0.06,0.2),(0.3,0),(0.68,0),(0.93,0.2),(0.93,0.4),(0.06,1),(0.96,1))],
 "3": [P((0.06,0.13),(0.34,0),(0.7,0),(0.93,0.16),(0.93,0.36),(0.6,0.5),(0.95,0.64),(0.95,0.86),(0.7,1),(0.32,1),(0.05,0.87))],
 "4": [P((0.74,1),(0.74,0),(0.04,0.72),(0.98,0.72))],
 "5": [P((0.9,0),(0.15,0),(0.09,0.45),(0.4,0.36),(0.7,0.4),(0.94,0.6),(0.94,0.85),(0.68,1),(0.3,1),(0.05,0.88))],
 "6": [P((0.86,0.1),(0.6,0),(0.3,0.05),(0.07,0.36),(0.05,0.72),(0.26,0.96),(0.6,1),(0.89,0.86),(0.9,0.62),(0.65,0.46),(0.3,0.48),(0.07,0.66))],
 "7": [P((0.04,0),(0.96,0),(0.42,1))],
 "8": [P((0.5,0),(0.82,0.12),(0.86,0.32),(0.5,0.5),(0.14,0.32),(0.18,0.12),(0.5,0)),
       P((0.5,0.5),(0.9,0.66),(0.92,0.86),(0.5,1),(0.08,0.86),(0.1,0.66),(0.5,0.5))],
 "9": [P((0.14,0.9),(0.4,1),(0.7,0.95),(0.93,0.64),(0.95,0.28),(0.74,0.04),(0.4,0),(0.11,0.14),(0.1,0.38),(0.35,0.54),(0.7,0.52),(0.93,0.34))],

 ".": [P((0.5,0.96),(0.5,1))],
 ",": [P((0.54,0.94),(0.42,1.12))],
 "!": [P((0.5,0.04),(0.5,0.72)), P((0.5,0.96),(0.5,1))],
 "?": [P((0.12,0.19),(0.35,0),(0.68,0),(0.91,0.18),(0.91,0.36),(0.5,0.58),(0.5,0.72)), P((0.5,0.96),(0.5,1))],
 ":": [P((0.5,0.44),(0.5,0.48)), P((0.5,0.96),(0.5,1))],
 ";": [P((0.5,0.44),(0.5,0.48)), P((0.54,0.94),(0.42,1.12))],
 "'": [P((0.52,0.04),(0.46,0.26))],
 "-": [P((0.14,0.62),(0.86,0.62))],
 "(": [P((0.7,-0.04),(0.4,0.26),(0.4,0.78),(0.7,1.08))],
 ")": [P((0.3,-0.04),(0.6,0.26),(0.6,0.78),(0.3,1.08))],
 "/": [P((0.88,-0.04),(0.12,1.08))],
 "=": [P((0.14,0.44),(0.86,0.44)), P((0.14,0.72),(0.86,0.72))],
 "+": [P((0.5,0.3),(0.5,0.9)), P((0.2,0.6),(0.8,0.6))],
 "%": [P((0.9,0.0),(0.1,1.0)), P((0.2,0.05),(0.35,0.05),(0.35,0.3),(0.2,0.3),(0.2,0.05)),
       P((0.65,0.7),(0.8,0.7),(0.8,0.95),(0.65,0.95),(0.65,0.7))],
 "[": [P((0.7,-0.04),(0.35,-0.04),(0.35,1.08),(0.7,1.08))],
 "]": [P((0.3,-0.04),(0.65,-0.04),(0.65,1.08),(0.3,1.08))],
 "&": [P((0.92,1),(0.22,0.22),(0.32,0.02),(0.56,0.02),(0.64,0.22),(0.1,0.72),(0.14,0.94),(0.4,1),(0.7,0.82),(0.86,0.56))],
}


def raster2(shapes):
    segs = segments2(shapes)
    cell = bytearray(CELL * CELL)
    half = PEN / 2.0
    for y in range(CELL):
        for x in range(CELL):
            px, py = x + 0.5, y + 0.5
            d = min(dist_seg(px, py, *s) for s in segs)
            a = half + 0.5 - d
            if a > 0:
                cell[y * CELL + x] = 255 if a >= 1 else int(a * 255)
    return cell


# Characters whose FF-block fullwidth form cp932 places in a duplicate area
# far outside the atlas (U+FF07 encodes as 0xEEFB). Same substitutions as
# tools/fullwidth.py, so text and font agree on which codepoint is used.
FW_SUBSTITUTE = {
    "'": "\u2019",      # cp932 0x8166
    '"': "\u201d",      # cp932 0x8168
    "-": "\uff0d",
}


def fullwidth_code(ch):
    """SJIS code of the fullwidth form of an ASCII character."""
    if ch == " ":
        fw = "\u3000"
    elif ch in FW_SUBSTITUTE:
        fw = FW_SUBSTITUTE[ch]
    elif 0x21 <= ord(ch) <= 0x7E:
        fw = chr(ord(ch) - 0x21 + 0xFF01)
    else:
        fw = ch
    enc = fw.encode("cp932")
    if len(enc) != 2:
        raise ValueError("%r does not encode as a 2-byte cp932 code" % ch)
    return (enc[0] << 8) | enc[1]


ATLAS_CELLS = 4480          # 128 cols x 35 rows
CELLS_PER_LEAD = 192        # a flat stride: exactly 1.5 atlas rows per lead byte


def cell_index(code):
    """SJIS code -> atlas cell.

        cell = (lead - 0x81) * 192 + (trail - 0x40)

    The atlas does not pack the 188 valid SJIS codes of a lead byte
    contiguously. It gives every lead byte a flat 192-cell stride -- exactly
    1.5 rows of 128 -- and indexes straight off the trail byte, so the unused
    trails below 0x40 and the invalid 0x7F simply occupy dead cells.

    Two wrong models were tried first, each caught in-game:
      * 188 (valid codes only) shifted every trail >= 0x80 one cell early:
        lowercase came out as a Caesar cipher, `Look` -> `Lppl`.
      * 189 with offset 3 fixed lead 0x82 but not lead 0x81, so punctuation
        was still wrong: `!` rendered as `:`.

    Verified against four in-game anchors: !=9, 0=207, A=224, a=257.
    """
    hi, lo = code >> 8, code & 0xFF
    idx = (hi - 0x81) * CELLS_PER_LEAD + (lo - 0x40)
    if not 0 <= idx < ATLAS_CELLS:
        raise ValueError("code 0x%04X maps to cell %d, outside the atlas"
                         % (code, idx))
    return idx


def put_cell(buf, w, idx, cov):
    """Write one 32x32 coverage cell into the 16bpp atlas (A4R4G4B4-style:
    the same nibble in every channel, which is how tools/tex.py reads it)."""
    row, col = idx // CELLS_PER_ROW, idx % CELLS_PER_ROW
    x0, y0 = col * CELL, row * CELL
    for y in range(CELL):
        base = 0x80 + ((y0 + y) * w + x0) * 2
        for x in range(CELL):
            n = cov[y * CELL + x] >> 4
            v = (n << 12) | (n << 8) | (n << 4) | n
            i = base + x * 2
            buf[i] = (v >> 8) & 0xFF
            buf[i + 1] = v & 0xFF


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    src, dst = argv[1], argv[2]
    preview = None
    if "--preview" in argv:
        preview = argv[argv.index("--preview") + 1]

    cpk = CPK(src)
    target = None
    for e in cpk.files:
        b = cpk.read(e)
        if len(b) >= 0x80 and b[0x18] == ATLAS_FORMAT:
            target = (e, bytearray(b))
            break
    if not target:
        raise SystemExit("no atlas member (format 0x%02X) in %s" % (ATLAS_FORMAT, src))
    e, buf = target
    w = struct.unpack_from(">H", buf, 0x20)[0]
    print("atlas member id=%d  %dx%d" % (e["id"], w, struct.unpack_from(">H", buf, 0x22)[0]))

    drawn = []
    for ch in sorted(GLYPHS):
        code = fullwidth_code(ch)
        idx = cell_index(code)
        cov = raster2(GLYPHS[ch])
        put_cell(buf, w, idx, cov)
        drawn.append((ch, code, idx))
    print("drew %d glyphs" % len(drawn))
    for ch, code, idx in drawn[:6]:
        print("   '%s' -> 0x%04X -> cell %d (row %d col %d)"
              % (ch, code, idx, idx // CELLS_PER_ROW, idx % CELLS_PER_ROW))

    tmp = dst + ".member"
    with open(tmp, "wb") as fh:
        fh.write(bytes(buf))

    import cpkpatch
    n, size = cpkpatch.build(src, dst, {e["id"]: tmp})
    os.remove(tmp)
    print("repacked %d members -> %s (%d bytes)" % (n, dst, size))

    if preview:
        cols = 16
        rows = (len(drawn) + cols - 1) // cols
        pw, ph = cols * CELL, rows * CELL
        gray = bytearray(pw * ph)
        for i, (ch, code, idx) in enumerate(drawn):
            cov = raster2(GLYPHS[ch])
            cx, cy = (i % cols) * CELL, (i // cols) * CELL
            for y in range(CELL):
                for x in range(CELL):
                    gray[(cy + y) * pw + cx + x] = cov[y * CELL + x]
        raw = bytearray()
        for y in range(ph):
            raw.append(0)
            raw += gray[y * pw:(y + 1) * pw]

        def chunk(t, d):
            return (struct.pack(">I", len(d)) + t + d
                    + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF))
        with open(preview, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n"
                     + chunk(b"IHDR", struct.pack(">IIBBBBB", pw, ph, 8, 0, 0, 0, 0))
                     + chunk(b"IDAT", zlib.compress(bytes(raw), 6))
                     + chunk(b"IEND", b""))
        print("preview -> %s" % preview)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
