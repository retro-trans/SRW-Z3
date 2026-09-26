"""Per-section geometry and the (retired) in-place writer for battle voice lines.

Since 2026-09-06 the build rebuilds SRVC.BIN block by block
(tools/srvc_blocks.py) and lines may be any length; this module now only
supplies the section geometry that maps a doc's entry numbers to strings.

Everything here exists because SRVC.BIN offsets are POOL-BOUNDED: an index
word is relative to its own section's pool base and every legitimate one is
inside that pool's span. Appending past the end and repointing crashed the
game (`ce7d83c`), and an earlier repoint corrupted barks it never selected
(`bea5636`). So the only write shape this module knows is: overwrite a
string inside its own byte slot, pad with NUL, never move an offset, never
change the file's size.

Geometry per section comes from `work/voice/sections.json` (written by
tools/extract.py from srvc_link.sections(), the canonical parser). A doc may
carry its own index/count/pool and then those win -- but they are still
PROVEN here before a byte is written, because a parser is a suggestion and
the proof is not: all COUNT index words of the section must land on real
string starts inside the section's own pool span. A wrong base does not fit
N-for-N.
"""
import json
import os
import struct

NUL = bytes((0,))
BRK = chr(92) + "n"          # SRVC writes a line break as literal backslash-n
HERE = os.path.dirname(os.path.abspath(__file__))
SECTIONS = os.path.join(HERE, "..", "work", "voice", "sections.json")


def table(path=SECTIONS):
    """{sec: {index, count, pool, limit}} -- limit ends the section's pool."""
    rows = json.load(open(path, encoding="utf-8"))
    rows = sorted(rows, key=lambda r: r["index"])
    out = {}
    for i, r in enumerate(rows):
        nxt = rows[i + 1]["index"] if i + 1 < len(rows) else None
        out[r["sec"]] = {"index": r["index"], "count": r["count"],
                         "pool": r["pool"], "limit": nxt}
    return out


def geometry(doc, tab=None):
    """A doc's (index, count, pool, limit). Doc fields win; the table fills
    in what the doc leaves out, which is the normal case."""
    tab = table() if tab is None else tab
    sec = doc.get("section")
    base = dict(tab.get(sec, {})) if sec is not None else {}
    for k in ("index", "count", "pool", "limit"):
        if doc.get(k) is not None:
            base[k] = doc[k]
    missing = [k for k in ("index", "count", "pool") if base.get(k) is None]
    if missing:
        raise SystemExit("section %r: no geometry for %s -- give it in the doc "
                         "or re-run extract.py" % (sec, ", ".join(missing)))
    return base["index"], base["count"], base["pool"], base.get("limit")


def starts(b, pool, limit=None):
    """Offsets a string may legally begin at, walking NUL to NUL."""
    limit = len(b) if limit is None else min(limit, len(b))
    out, p = set(), pool
    while p < limit:
        out.add(p)
        e = b.find(NUL, p)
        if e < 0:
            break
        p = e + 1
    return out


def index_words(b, index, count):
    return [struct.unpack_from("<I", b, index + 4 * i)[0] for i in range(count)]


def prove(b, index, count, pool, limit=None, sec=None):
    """The base check, independent of the parser that suggested the base.

    Every index word must resolve pool-relatively to a real string start
    inside the section's own pool. This is what a wrong base fails.
    """
    st = starts(b, pool, limit)
    bad = [i for i, v in enumerate(index_words(b, index, count))
           if (pool + v) not in st]
    if bad:
        raise SystemExit(
            "section %s: base %#x unproven -- %d of %d index words do not land "
            "on a string start in the pool" % (sec, pool, len(bad), count))
    return True


def encode(text, mapping, enc=None):
    """English -> the bytes the slot holds, brackets included.

    The literal backslash-n break is passed through raw: the game's text
    parser consumes it, and encoding it would try to draw a backslash.
    """
    if enc is not None:
        return enc(text)
    import digraph as dg
    whole = "\u300c" + text + "\u300d"
    return BRK.encode("ascii").join(
        dg.encode_mixed(part, mapping, newline=bytes((10,)))
        for part in whole.split(BRK))


def apply_docs(b, docs, mapping, enc=None, tab=None):
    """Write every doc in place. Returns (bytes, report).

    report[i] = {sec, unit, written, slots:[(entry, off, room, used)]}.
    Two entries of one section that share a byte slot -- the file stores a
    reused line once -- must agree; the writer refuses a disagreement rather
    than letting whichever sorted last win silently.
    """
    tab = table() if tab is None else tab
    out = bytearray(b)
    report, claimed = [], {}
    for doc in docs:
        index, count, pool, limit = geometry(doc, tab)
        sec = doc.get("section")
        prove(b, index, count, pool, limit, sec)
        words = index_words(b, index, count)
        lines = doc.get("lines", doc)
        slots = []
        for k in sorted(lines, key=lambda x: int(x)):
            n = int(k)
            v = lines[k]
            en = v["en"] if isinstance(v, dict) else v
            if en is None or en == "":
                continue
            if not 0 <= n < count:
                raise SystemExit("section %s: entry %d is outside the section "
                                 "(%d entries)" % (sec, n, count))
            off = pool + words[n]
            e = b.find(NUL, off)
            room = e - off
            data = encode(en, mapping, enc)
            if len(data) > room:
                raise SystemExit(
                    "section %s entry %d: %r needs %d bytes, slot holds %d -- "
                    "compress it, never truncate" % (sec, n, en, len(data), room))
            prev = claimed.get(off)
            if prev is not None and prev[1] != data:
                raise SystemExit(
                    "section %s entry %d shares slot %#x with entry %d but the "
                    "English differs -- one stored line serves every entry that "
                    "points at it" % (sec, n, off, prev[0]))
            claimed[off] = (n, data)
            out[off:off + room] = data + bytes(room - len(data))
            slots.append((n, off, room, len(data)))
        report.append({"sec": sec, "unit": doc.get("unit"),
                       "written": len(slots), "slots": slots})
    return bytes(out), report


def verify(old, new, report, tab=None):
    """Re-derived from the two files, sharing no assumption with the writer.

    The independence rule: the append-era verifier resolved entries through
    the same section map the patch used, so it confirmed the patch's own
    mistake. Here the questions are byte questions -- did the file change
    size, did anything move outside a slot we chose, did any index word
    change anywhere in the file.
    """
    tab = table() if tab is None else tab
    problems = []
    if len(new) != len(old):
        problems.append("file size changed: %d -> %d" % (len(old), len(new)))
        return problems
    slots = [(o, o + r) for rep in report for _n, o, r, _u in rep["slots"]]
    slots.sort()
    for i in range(len(old)):
        if old[i] != new[i]:
            if not any(a <= i < z for a, z in slots):
                problems.append("byte %#x changed outside every target slot" % i)
                break
    for rep in report:
        g = tab.get(rep["sec"])
        if not g:
            continue
        if (index_words(old, g["index"], g["count"])
                != index_words(new, g["index"], g["count"])):
            problems.append("section %s: index words changed; in-place must "
                            "never touch them" % rep["sec"])
    return problems
