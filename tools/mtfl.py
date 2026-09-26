"""Read and write MTV_ALL_KEYWORD_DEF.CPK -- the file the KEYWORD library reads.

This is NOT MTZKN_KW. The zukan index is a separate copy the game never opens
for the keyword screen; patching it changed nothing on screen, which is how
this file was found. It holds the same 141 entries in its own order.

Container (inside the single CPK member):

    0x00  'MTFLz2_2', version '0.94', two chunk descriptors (kwrb, lkke)
    then  u32 count (141), then the INDEX, then TEXT, then footer

Index: record 0 is 8 u32 with no prefix; every later record is
    FFFFFFFF, id, off_w,len_w, off_s,len_s, off_d,len_d, off_d2,len_d2
and the final id follows one more FFFFFFFF. Offsets are relative to TEXT.
The ids are a permutation of 0..140 -- file order is not id order.

Text: NUL-terminated strings back to back, XORed with 0x7A. The XOR skips
the key byte itself -- a plaintext 0x7A is stored as 0x7A, not 0x00 -- the
same fixed-point rule the zukan files use with 0x5E. Miss that and 33 entries
(every one containing 陽, 配, 越...) look corrupt.

Two unindexed strings exist and are copied verbatim: a '￠' prefix at the
start of TEXT and an 'ENDoMTFLs' terminator at the end. The last string
is NOT NUL-terminated; the 'E' of the marker follows it directly.
"""
import json
import struct
import sys

KEY = 0x7A
NREC = 141
FIELDS = (("WORD", 0, 1), ("SRCE", 2, 3), ("DSCR", 4, 5), ("DSC2", 6, 7))


def xor(b):
    return bytes(c if c == KEY else c ^ KEY for c in b)


def parse(raw):
    pay = raw[0x20:]
    u = struct.unpack_from("<%dI" % (len(pay) // 4), pay)
    i141 = u.index(NREC)
    tab = list(u[i141 + 1:])
    wins = [tab[0:8]]
    ids = []
    i = 8
    while len(wins) < NREC:
        ids.append(tab[i + 1])
        wins.append(tab[i + 2:i + 10])
        i += 10
    ids.append(tab[i + 1])
    idx_end = 0x20 + 4 * (i141 + 1 + i + 2)
    # TEXT base: structural and language-independent. Measured on both the
    # Japanese original and an English rebuild: offsets are relative to
    # idx_end+16, and the verbatim 2-byte prefix 0x81 0x91 (FULLWIDTH CENT
    # SIGN) + NUL sits 12 bytes after that base -- record 0 WORD at base+15.
    base = idx_end - 0x20 + 16
    prefix = bytes([0x81 ^ KEY, 0x91 ^ KEY, 0x00])
    if pay[base + 12:base + 15] != prefix:
        raise ValueError("TEXT base wrong: prefix reads %r" % pay[base + 12:base + 15])
    return {"ids": ids, "wins": wins, "i141": i141, "idx_end": idx_end, "base": base}


def strings(raw, p):
    pay = raw[0x20:]
    out = {}
    for eid, f in zip(p["ids"], p["wins"]):
        rec = {}
        for n, fo, fl in FIELDS:
            o, l = f[fo], f[fl]
            rec[n] = xor(pay[p["base"] + o:p["base"] + o + l]).decode("cp932")
        out[eid] = rec
    return out


def build(raw, p, texts, order=None):
    """Re-emit the file with `texts[id][field]` (cp932-encodable strings, or
    raw bytes) replacing the originals. Offsets are recomputed; the ￠ prefix
    and NDoMTFLs terminator are preserved verbatim."""
    pay = raw[0x20:]
    base = p["base"]
    # the prefix: bytes from TEXT start up to record 0's first string
    prefix = pay[base:base + min(f[0] for f in p["wins"])]
    # terminator: after the last indexed byte
    last_end = max(f[fo] + f[fl] + 1 for f in p["wins"] for _, fo, fl in FIELDS)
    text_end = None
    # find 'NDoMTFLs' after last_end
    marker = pay.find(b"ENDoMTFLs", base + last_end - 4)
    tail = pay[marker:]
    # lay out new strings in the original file order
    # Every distinct string is stored ONCE; every field with those exact bytes
    # points at the same offset. The shipped file does this for all fields:
    # 「オリジナル」 is stored once for 56 entries, and 123 DSC2s share their
    # DSCR. Writing duplicates inflated the file by 51 KB and shifted offsets.
    text = bytearray(prefix)
    where = {}
    # `order` (record indices) decides where each record's strings land in
    # the pool; default is file order. Used to probe offset limits.
    for k in (order if order is not None else range(NREC)):
        for n, fo, fl in FIELDS:
            s_ = texts[p["ids"][k]][n]
            b_ = s_ if isinstance(s_, bytes) else s_.encode("cp932")
            if b_ not in where:
                where[b_] = len(text)
                text += xor(b_) + b"\x00"
    new_wins = []
    for eid, f in zip(p["ids"], p["wins"]):
        w = []
        for n, fo, fl in FIELDS:
            s = texts[eid][n]
            b = s if isinstance(s, bytes) else s.encode("cp932")
            w += [where[b], len(b)]
        new_wins.append(w)
    text = text[:-1]          # the last string runs straight into ENDoMTFLs, no NUL
    idx = struct.pack("<8I", *new_wins[0])
    for k in range(1, NREC):
        idx += struct.pack("<10I", 0xFFFFFFFF, p["ids"][k - 1], *new_wins[k])
    idx += struct.pack("<2I", 0xFFFFFFFF, p["ids"][NREC - 1])
    head = raw[:0x20 + 4 * (p["i141"] + 1)]
    gap = raw[len(head) + len(idx):0x20 + base] if False else pay[p["idx_end"] - 0x20:base]
    out = bytearray(head + idx + gap + bytes(text) + tail)
    # Three size words count the bytes up to the ENDoMTFLs terminator and must
    # follow the text: the header word at 0x10 and the `brwk` chunk total are
    # marker - 0x20, the chunk body is marker - 0x30. Left at the original
    # values, the game reads a 72 KB block out of a 178 KB one and every
    # keyword definition past it comes up empty on screen.
    marker = out.find(b"ENDoMTFLs")
    if marker < 0:
        raise ValueError("ENDoMTFLs terminator lost")
    struct.pack_into("<I", out, 0x10, marker - 0x20)
    struct.pack_into("<I", out, 0x24, marker - 0x20)
    struct.pack_into("<I", out, 0x2c, marker - 0x30)
    # The `jstr` chunk descriptor (16 bytes: tag, total, hdr, body) sits between
    # the index and the text; its BODY is how many text bytes the loader
    # XOR-0x7A decodes at load. build() copies it verbatim, so it kept the
    # original 0x10620 -- the game then decoded only the first ~67 KB and every
    # definition past that showed a BLANK panel. Point it at the real text.
    j = out.find(b"jstr")
    if j < 0:
        raise ValueError("jstr text-chunk descriptor not found")
    text_start = j + 16
    body = marker - text_start
    struct.pack_into("<I", out, j + 4, body + 0x10)     # total = body + header
    struct.pack_into("<I", out, j + 12, body)           # body  = text length
    return bytes(out)


if __name__ == "__main__":
    sys.stdout = __import__("io").TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
    from cpk import CPK
    k = CPK(sys.argv[1]); raw = k.read(k.files[0])
    p = parse(raw); s = strings(raw, p)
    print("base 0x%x, %d entries, first ids %s" % (p["base"], len(s), p["ids"][:6]))
    json.dump(s, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
