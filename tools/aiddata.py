"""UI text: the FSSA string pool in DATA/AIDDATA/AIDDATAPACK.CPK.

The menu screens -- scenario select, the protagonist setup sheet, the battle
COMMAND list -- are NOT textures. An earlier pass concluded they were, on the
strength of a scan that found nothing; that scan read raw file bytes, and every
one of these strings lives inside a CRILAYLA-compressed CPK member, so it could
never have found them. Searching decompressed members finds all three.

Member 0 is a 1.1 MB `FSSA` resource holding ~52,000 cp932 strings, NUL
separated with a byte or two of slack. Member 4 holds the protagonist sheet.

Strings are written IN PLACE and never longer than the original. How they are
referenced is not known -- no plain offset table was found -- so shortening is
the only edit that is safe without understanding it. A string ends at its first
NUL, so a shorter replacement leaves the tail unread and no offset moves.

    python tools/aiddata.py <AIDDATAPACK.CPK> <member> [substring]
"""
import io
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

NUL = bytes((0,))
MAGIC = b"FSSA"


def strings(d):
    """[(offset, text, bytes, slack)] for every cp932 string in the blob."""
    out, i = [], 0
    n = len(d)
    while i < n:
        if d[i] >= 0x81:
            e = d.find(NUL, i)
            if e < 0:
                break
            try:
                t = d[i:e].decode("cp932")
            except Exception:
                i = e + 1
                continue
            j = e
            while j < n and d[j] == 0:
                j += 1
            out.append((i, t, e - i, j - e))
            i = j
        else:
            i += 1
    return out


def apply(d, edits, mapping, pairs=False):
    """`edits` = [{off, en}]. Writes text + NUL, never past the original end.

    `pairs=True` encodes with PAIR cells -- two letters per 2-byte cell -- for
    slots too small to spend a whole cell on each letter. The room measured is
    to the next STRING, not to the terminator, since the padding after a string
    is free space: that is what makes "Nick" fit 愛称's four text bytes.
    """
    import digraph as dg
    out = bytearray(d)
    done = []
    for row in edits:
        off = row["off"]
        e = d.find(NUL, off)
        room = e - off
        if pairs:
            j = e
            while j < len(d) and d[j] == 0:
                j += 1
            room = j - off - 1          # text + padding, keeping one terminator
        enc = (dg.encode_pairs(row["en"], mapping, newline=bytes((10,)))
               if pairs else
               dg.encode_mixed(row["en"], mapping, newline=bytes((10,))))
        if len(enc) > room:
            raise SystemExit("%#08x: %r needs %d bytes, original is %d"
                             % (off, row["en"], len(enc), room))
        out[off:off + len(enc)] = enc
        out[off + len(enc)] = 0
        done.append((off, len(enc), room))
    return bytes(out), done


def roster_resupply_headers(d, mapping):
    """Mark just the two narrow Unit List Resupply headings for a short hook.

    補． is an internal, same-size content key for ui_hook's Sup. label.
    Never change standalone 補給 globally: Spirit names must stay Resupply.
    """
    offsets = (0x66710, 0x667A4)
    for off in offsets:
        if d[off:off + 5] != '補給'.encode('cp932') + NUL:
            raise SystemExit('unexpected roster Resupply heading at %#x' % off)
    return apply(d, [{'off': off, 'en': '補．'} for off in offsets], mapping)


def roster_team_overlay(d, mapping):
    """Blank the separate vowel stroke over the roster's hooked チ　ム label."""
    off = 0x662A6
    pattern = 'ー'.encode('cp932') + bytes(2) + 'チ　ム'.encode('cp932') + bytes(2)
    if d[off:off + len(pattern)] != pattern:
        raise SystemExit('unexpected roster Team overlay at %#x' % off)
    # Keep both slots and their terminators intact. ui_hook translates the
    # second string at its original left edge; no global kana replacement.
    return apply(d, [{'off': off, 'en': '　'}], mapping)


def team_label_fragments(d, mapping):
    """Translate only the reordered three-fragment Mech Info Team label."""
    pattern = 'ー'.encode('cp932') + bytes(2) + 'チ'.encode('cp932') + bytes(2) + 'ム．'.encode('cp932') + bytes(2)
    edits, start = [], 0
    while (off := d.find(pattern, start)) >= 0:
        # Stored e/T/am order; the widgets draw them as T/e/am.
        edits.extend({'off': off + rel, 'en': en}
                     for rel, en in [(0, 'e'), (4, 'T'), (8, 'am')])
        start = off + len(pattern)
    if not edits:
        raise SystemExit('Mech Info split Team label not found in pristine UI')
    return apply(d, edits, mapping)


def verify(old, new, done):
    problems = []
    if len(new) != len(old):
        problems.append("size changed: %d -> %d" % (len(old), len(new)))
    spans = [(o, o + n + 1) for o, n, _r in done]
    for i in range(min(len(old), len(new))):
        if old[i] != new[i] and not any(a <= i < b for a, b in spans):
            problems.append("byte %#x changed outside every edited string" % i)
            break
    return problems


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    k = CPK(argv[1])
    d = k.read(k.files[int(argv[2])])
    print("member %s: %d bytes, magic %r" % (argv[2], len(d), d[:4]))
    want = argv[3] if len(argv) > 3 else None
    n = 0
    for off, t, nb, slack in strings(d):
        if want and want not in t:
            continue
        if len(t) > 40:
            continue
        print("   %#08x  %3dB +%d  [%2d cells]  %s" % (off, nb, slack, nb // 2, t))
        n += 1
        if n > 200:
            print("   ...")
            break
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))


# The string region, and the widget records that address it. Found by taking
# each header word as a candidate base and testing whether a known string's
# offset appears as a reference: relative to 0x59478 every UI string has
# exactly one big-endian u32 referent, and those referents sit 0x20 apart.
#
# A record is 32 bytes:  [0] string offset, rel to STR_BASE
#                        [1] [2] x, y as big-endian floats
#                        [3] colour RGBA
#                        [4..7] style and flags
#
# This is what lifts the length limit. Menu text no longer has to fit the
# Japanese it replaces: append English past the end of the member and rewrite
# the offset. Everything before was capped at the original slot -- 姓 at one
# cell, 移動 at two -- because no reference table had been found.
STR_BASE = 0x59478
REC = 0x20
REC_ALIGN = 0x14        # every reference seen starts at 0x14 mod 0x20


def refs(d, base=STR_BASE):
    """{string offset (absolute): [record positions referencing it]}.

    Only positions at a record start count. Every reference checked lands at
    0x14 mod 0x20, so scanning all 4-byte positions would add coincidences --
    a 1.1 MB file has plenty of words that happen to look like an offset.
    """
    out = {}
    for p in range(REC_ALIGN, len(d) - 4, REC):
        v = struct.unpack_from(">I", d, p)[0]
        if 0 < v < len(d) - base:
            out.setdefault(base + v, []).append(p)
    return out


def repoint(d, edits, mapping, base=STR_BASE):
    """`edits` = [{off, en}]. Appends English and rewrites every reference.

    Nothing existing moves, so no other offset changes meaning; the member
    simply grows. Only records whose word 0 pointed at an edited string are
    touched.
    """
    import digraph as dg
    out = bytearray(d)
    idx = refs(d, base)
    done, unref = [], []
    for row in edits:
        off = row["off"]
        where = idx.get(off, [])
        if not where:
            unref.append(row)
            continue
        enc = dg.encode_mixed(row["en"], mapping, newline=bytes((10,))) + NUL
        pos = (len(out) + 3) & ~3
        out += bytes(pos - len(out))
        out += enc
        rel = pos - base
        for w in where:
            struct.pack_into(">I", out, w, rel)
        done.append((off, pos, len(where), row["en"]))
    return bytes(out), done, unref


def verify_repoint(old, new, done, mapping, base=STR_BASE):
    """Re-derived from the two blobs, not from what repoint() decided.

    Below the original end, ONLY the record words that pointed at an edited
    string may differ. Above it, each appended string must decode back to the
    English asked for, and every rewritten record must resolve to it.
    """
    import digraph as dg
    problems = []
    if len(new) < len(old):
        problems.append("member shrank")
        return problems
    idx = refs(old, base)
    allowed = set()
    for off, _pos, _n, _en in done:
        for w in idx.get(off, []):
            allowed.update(range(w, w + 4))
    for i in range(len(old)):
        if old[i] != new[i] and i not in allowed:
            problems.append("byte %#x changed outside every reference" % i)
            break
    for off, pos, n, en in done:
        want = dg.encode_mixed(en, mapping, newline=bytes((10,))) + NUL
        if new[pos:pos + len(want)] != want:
            problems.append("%r not written at %#x" % (en, pos))
        seen = 0
        for w in idx.get(off, []):
            if struct.unpack_from(">I", new, w)[0] != pos - base:
                problems.append("record %#x still points elsewhere" % w)
            else:
                seen += 1
        if seen != n:
            problems.append("%r: %d of %d records repointed" % (en, seen, n))
    return problems
