"""SRVC.BIN as the game reads it: 276 blocks addressed by a table in the EBOOT.

The battle-voice loader (EBOOT VA 0x11ab20 -> 0x11142c -> 0x114188 -> parser
0x111488; notes in work/srvc_loader_notes.md) never walks the file. It takes
the unit's u16 voice-bank id, reads `tab[id]` and `tab[id+1]` from a table of
277 big-endian u32 file offsets at EBOOT file offset TABLE_OFF, and issues a
partial read of exactly that window. Inside the block everything is
self-describing:

    +0  u8  3          +1 u8 n1 (74)   +2 u8 n2   +3 u8 n3
    +4  u16le n4       +6 u16le n6 = number of voice lines
    +8  A[n1]*4  B[n4]*8  C[n2]*8  D[n3]*4  cue[n6]*8  offs[n6] u32le  pool

So a block can GROW: rewrite its offs + pool, shift everything after it, and
write the new starts into the EBOOT table in the same build. The two are one
change -- a grown SRVC.BIN with the old table blanks every later unit's text
(the +64-byte experiment of 2026-09-06).

`rebuild()` keeps the block count and order, copies header..cue verbatim,
lays the pool out in the original's order (a string shared by several
entries stays shared), pads each block to 16 bytes as the original does, and
returns the new table. `rebuild(b, tab, {})` reproduces the pristine file
byte for byte -- that round trip is the proof the parser is right.
"""
import re
import struct

TABLE_OFF = 0x830BE0      # file offset in EBOOT_dec.elf and in the shipped EBOOT.BIN
NBLOCKS = 276
TABLE_LEN = (NBLOCKS + 1) * 4
NUL = bytes((0,))


def read_table(elf):
    tab = list(struct.unpack_from(">%dI" % (NBLOCKS + 1), elf, TABLE_OFF))
    if tab[0] != 0 or any(b <= a for a, b in zip(tab, tab[1:])):
        raise SystemExit("EBOOT: no SRVC block table at %#x" % TABLE_OFF)
    return tab


def pack_table(tab):
    return struct.pack(">%dI" % len(tab), *tab)


def parse(b, tab):
    """[{i, base, end, n6, offs_at, pool, offs:[...]}] for every block."""
    if tab[-1] != len(b):
        raise SystemExit("SRVC.BIN is %d bytes but the table ends at %d" % (len(b), tab[-1]))
    out = []
    for i in range(NBLOCKS):
        base, end = tab[i], tab[i + 1]
        n1, n2, n3 = b[base + 1], b[base + 2], b[base + 3]
        n4, n6 = struct.unpack_from("<HH", b, base + 4)
        p = base + 8 + n1 * 4 + n4 * 8 + n2 * 8 + n3 * 4
        offs_at, pool = p + n6 * 8, p + n6 * 12
        offs = list(struct.unpack_from("<%dI" % n6, b, offs_at)) if n6 else []
        if pool > end or any(pool + o >= end for o in offs):
            raise SystemExit("block %d: string offsets leave the block" % i)
        out.append({"i": i, "base": base, "end": end, "n6": n6,
                    "offs_at": offs_at, "pool": pool, "offs": offs})
    return out


def string_at(b, off):
    e = b.find(NUL, off)
    return b[off:e]


def rebuild(b, tab, repl):
    """repl = {absolute offset of an ORIGINAL string: new bytes (no NUL)}.

    Returns (new_bytes, new_table, report); report = per block
    (i, old_size, new_size, strings_replaced)."""
    blocks = parse(b, tab)
    out = bytearray()
    newtab = []
    report = []
    for blk in blocks:
        newtab.append(len(out))
        out += b[blk["base"]:blk["offs_at"]]
        # The original pool, string by string, in its own order -- including
        # strings no entry references (the pristine file carries 65 KB of
        # them). Only strings named in repl change; everything else, and
        # the layout, stays as it was.
        raw = b[blk["pool"]:blk["end"]].rstrip(NUL)
        raw = raw + NUL if raw else raw           # a textless block has no pool at all
        starts = [0] + [m.end() for m in re.finditer(NUL, raw)]
        starts = [x for x in starts if x < len(raw)]
        pos, pool, hit = {}, bytearray(), 0
        for st in starts:
            pos[st] = len(pool)
            s = repl.get(blk["pool"] + st)
            if s is None:
                s = raw[st:raw.index(NUL, st)]
            else:
                hit += 1
            pool += s + NUL
        def newoff(o):
            st = max(x for x in starts if x <= o)      # mid-string pointers keep their tail
            return pos[st] + (o - st)
        out += struct.pack("<%dI" % blk["n6"], *[newoff(o) for o in blk["offs"]])
        out += pool
        # the original's own trailing zeros (12 blocks carry a spare 16), then 16-align
        tail = blk["end"] - (blk["pool"] + len(raw))
        out += bytes(tail)
        out += bytes((-len(out)) % 16)
        report.append((blk["i"], blk["end"] - blk["base"], len(out) - newtab[-1], hit))
    newtab.append(len(out))
    return bytes(out), newtab, report


def verify(new, newtab, old, oldtab, repl):
    """Independent of the writer: parse the new file through the NEW table and
    check every entry reads back as its original string or its replacement,
    and that the two files have the same block count and line counts."""
    problems = []
    nb, ob = parse(new, newtab), parse(old, oldtab)
    if len(nb) != len(ob):
        return ["block count changed"]
    for a, z in zip(nb, ob):
        if a["n6"] != z["n6"]:
            problems.append("block %d: line count %d -> %d" % (z["i"], z["n6"], a["n6"]))
            continue
        if new[a["base"]:a["offs_at"]] != old[z["base"]:z["offs_at"]]:
            problems.append("block %d: header bytes changed" % z["i"])
        for k, (o_new, o_old) in enumerate(zip(a["offs"], z["offs"])):
            src = z["pool"] + o_old
            want = repl.get(src, string_at(old, src))
            got = string_at(new, a["pool"] + o_new)
            if got != want:
                problems.append("block %d entry %d: reads back wrong" % (z["i"], k))
                break
    return problems
