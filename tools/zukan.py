"""Read the in-game library (図鑑) -- keywords, pilots and robots.

Lives in `COMMONDATA/MTDATA/MTZKN_{KW,PT,RT}.CPK`, one CPK member per entry,
uncompressed but obfuscated.

The obfuscation is **XOR 0x5E, with 0x00 and 0x5E left alone**. Both are fixed
points of the key (0x5E ^ 0x5E == 0x00), so skipping them means the encoder
never creates a NUL byte and never destroys one -- the little-endian lengths
survive, and so does a cp932 trail byte that happens to be 0x5E.

That last case is the one that bites: `タ` is 0x83 0x5E, and a naive whole-buffer
XOR turns it into 0x83 0x00, which is why `フルメタル・パニック` first came out
as `フルメ?ル・パニック`. The header decodes to `ZKANKYWD`, which is how the
key was found in the first place.

Body is a chain of `tag(4) + u32 length + payload` chunks:

    DSIZ  total size          DATA  the record body
    WORD  the term            SRCE  which series it comes from
    DSCR  description         DSC2  second description (usually identical)

Pilots and robots use the same container with their own tags.

    python tools/zukan.py list <MTZKN_KW.CPK>
    python tools/zukan.py dump <MTZKN_KW.CPK> <out.json>
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

KEY = 0x5E


FIXED = (0x00, KEY)


def deobfuscate(b):
    """XOR 0x5E, leaving the key's two fixed points untouched."""
    return bytes(x if x in FIXED else x ^ KEY for x in b)


def chunks(b, start, end):
    """Walk tag/length chunks. Nested containers are walked too."""
    out = []
    p = start
    while p + 8 <= end:
        tag = b[p:p + 4]
        if not tag.isalnum():
            break
        ln = struct.unpack_from("<I", b, p + 4)[0]
        body = b[p + 8: p + 8 + ln]
        out.append((tag.decode("ascii", "replace"), body))
        p += 8 + ln
    return out


def text(b):
    return b.rstrip(b"\0").decode("cp932", "replace")


def parse(raw):
    b = deobfuscate(raw)
    magic = b[:8].decode("ascii", "replace")
    rec = {"magic": magic}
    # the outer DSIZ/DATA chunks wrap the real fields; walk both levels
    for tag, body in chunks(b, 16, len(b)):
        if tag in ("DSIZ", "DATA"):
            for t2, b2 in chunks(body, 0, len(body)):
                if t2 not in ("DSIZ", "DATA"):
                    rec[t2] = text(b2)
                else:
                    for t3, b3 in chunks(b2, 0, len(b2)):
                        rec[t3] = text(b3)
        else:
            rec[tag] = text(body)
    return rec


def read_all(path):
    k = CPK(path)
    out = []
    for e in k.files:
        try:
            r = parse(k.read(e))
        except Exception as ex:                     # noqa: BLE001
            r = {"error": str(ex)}
        r["id"] = e["id"]
        out.append(r)
    return out


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd, path = argv[1], argv[2]
    recs = read_all(path)
    if cmd == "list":
        keys = set()
        for r in recs:
            keys |= set(r)
        print("%d entries, fields: %s" % (len(recs), sorted(keys - {"id", "magic"})))
        for r in recs[:12]:
            name = r.get("WORD") or r.get("NAME") or r.get("PNAM") or "?"
            src = r.get("SRCE", "")
            print("  %4d  %-28s %s" % (r["id"], name[:28], src[:30]))
    elif cmd == "dump":
        json.dump(recs, open(argv[3], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("%d entries -> %s" % (len(recs), argv[3]))
    else:
        print("unknown command %r" % cmd)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))


# --- writing -------------------------------------------------------------
# obfuscate == deobfuscate: XOR-with-fixed-points is an involution. For any x
# outside {0x00, 0x5E}, x ^ 0x5E lands outside that set too, so applying the
# transform twice returns x exactly.
obfuscate = deobfuscate

HEADER_FMT = "<II"
VERSION = 0x00000100
HDRVAL = 0x0000000C


def build(magic, fields):
    """Fields -> one obfuscated library entry.

    Layout, verified byte-for-byte against the shipped file:

        magic(8) version(4) hdrval(4)
        DSIZ len(4)              -- covers everything from DATA onward
        DATA len(4)              -- covers the field chunks
        <tag(4) len(4) payload> ...
    """
    data = b"".join(t.encode("ascii") + struct.pack("<I", len(p)) + p
                    for t, p in fields)
    body = b"DATA" + struct.pack("<I", len(data)) + data
    out = (magic.encode("ascii") + struct.pack(HEADER_FMT, VERSION, HDRVAL)
           + b"DSIZ" + struct.pack("<I", len(body)) + body)
    return obfuscate(out)


def parse_ordered(raw):
    """Like parse(), but keeps field order and raw payloads so an entry can be
    rebuilt with only some fields changed."""
    b = deobfuscate(raw)
    magic = b[:8].decode("ascii", "replace")
    fields = []
    p = 16
    while p + 8 <= len(b):
        tag = b[p:p + 4]
        if not tag.isalnum():
            break
        ln = struct.unpack_from("<I", b, p + 4)[0]
        if tag in (b"DSIZ", b"DATA"):
            p += 8
            continue
        fields.append((tag.decode("ascii"), b[p + 8: p + 8 + ln]))
        p += 8 + ln
    return magic, fields
