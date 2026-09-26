"""Decode the game's texture container to PNG.

Two containers appear in the CPKs:

    02 02 ...   the game's own wrapper
    01 05 ...   a PS3 GTF

Both share the same 0x80 header layout as far as we need it:

    0x04  u32  payload size (excludes the 0x80 header)
    0x0B  u8   texture count
    0x18  u8   pixel format (0xA5 = 32bpp seen, 0xAB = 16bpp seen)
    0x20  u16  width
    0x22  u16  height

Derived by diffing headers across members of different sizes, then confirmed
by arithmetic: 1536x256x4 == 1572864 and 1280x720x4 == 3686400, both exact.

Getting this wrong is what made early dumps look like horizontal stripes --
that is the signature of reading 32bpp data at 8bpp.

    python tools/tex.py <file.cpk> <member-id> <out.png>
    python tools/tex.py --raw <file.bin> <out.png>
"""
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

HEADER = 0x80


def info(b):
    return {
        "payload": struct.unpack_from(">I", b, 0x04)[0],
        "count": b[0x0B],
        "format": b[0x18],
        "width": struct.unpack_from(">H", b, 0x20)[0],
        "height": struct.unpack_from(">H", b, 0x22)[0],
    }


def to_png(b, path, crop=None):
    m = info(b)
    w, h = m["width"], m["height"]
    px = b[HEADER:]
    if not w or not h:
        raise SystemExit("no dimensions in header: %r" % m)
    bpp = len(px) / float(w * h)
    if abs(bpp - 4.0) > 0.01:
        print("  warning: %.2f bytes/pixel, expected 4 (format 0x%02X)"
              % (bpp, m["format"]))
    cw, ch = crop or (w, h)
    cw, ch = min(cw, w), min(ch, h)

    raw = bytearray()
    for y in range(ch):
        raw.append(0)                      # filter: none
        base = y * w * 4
        for x in range(cw):
            i = base + x * 4
            # strongest channel, so glyphs show whatever the channel order is
            raw.append(max(px[i], px[i + 1], px[i + 2], px[i + 3]))

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", cw, ch, 8, 0, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    with open(path, "wb") as fh:
        fh.write(png)
    return m, (cw, ch)


def main(argv):
    if len(argv) >= 3 and argv[1] == "--raw":
        b = open(argv[2], "rb").read()
        m, size = to_png(b, argv[3])
    elif len(argv) >= 4:
        cpk = CPK(argv[1])
        want = int(argv[2])
        hit = [e for e in cpk.files if e["id"] == want]
        if not hit:
            raise SystemExit("no member with id %d" % want)
        b = cpk.read(hit[0])
        m, size = to_png(b, argv[3])
    else:
        print(__doc__.strip())
        return 2
    print("%dx%d fmt=0x%02X count=%d -> %s (%dx%d written)"
          % (m["width"], m["height"], m["format"], m["count"],
             argv[-1], size[0], size[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
