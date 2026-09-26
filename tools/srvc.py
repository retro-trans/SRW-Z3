"""Read and edit DATA/BTLC/SRVC.BIN -- the battle voice-line table.

Layout, derived rather than documented:

    202 sections, each   [ index of LE u32 offsets ][ text pool ]

An index entry is an offset relative to ITS OWN section's pool base, not to the
file. 48,058 entries address 32,035 distinct cp932 strings, so a line reused by
several situations is stored once and pointed at repeatedly. One section per
playable unit, which is why a single pilot's voice set can be translated on its
own.

Writing strategy: **never move a byte that already exists.** Sections sit back
to back, so growing one in place would shift every section after it. Instead
the English WAS appended past the end of the file (this cannot work: the game
reads one block per unit through the EBOOT table -- see tools/srvc_blocks.py;
kept for the record) and the chosen index entries
are rewritten to `new_position - section_pool_base`. Offsets are full u32s, so
a section near the front can reach the end of a 2 MB file comfortably. Every
original byte stays where it is, which is what makes the edit verifiable:
outside the appended block, only the four-byte entries we chose may differ.

    python tools/srvc.py sections <SRVC.BIN>
    python tools/srvc.py find     <SRVC.BIN> <substring>
    python tools/srvc.py dump     <SRVC.BIN> <section> [out.json]
"""
import io
import json
import os
import re
import struct
import sys

KANA = re.compile(r"[぀-ヿ一-鿿]")
OPEN = b"\x81\x75"          # 「 -- essentially every spoken line opens with it


def _text_at(b, p, minlen=4):
    e = b.find(b"\x00", p)
    if e < 0 or e - p < minlen:
        return None
    try:
        s = b[p:e].decode("cp932")
    except Exception:
        return None
    return s if KANA.search(s) else None


def sections(b):
    """[{pool, index, count}] -- one per voice set, in file order.

    Found by structure, not by a header: a pool starts where a run of preceding
    words all resolve, relative to that point, to decodable Japanese.
    """
    out, seen, p = [], set(), 0
    while True:
        p = b.find(OPEN, p)
        if p < 0:
            break
        o, n = p - 4, 0
        while o >= 0:
            v = struct.unpack_from("<I", b, o)[0]
            if v > len(b) - p or _text_at(b, p + v) is None:
                break
            n += 1
            o -= 4
        if n >= 8 and p not in seen:
            seen.add(p)
            out.append({"pool": p, "index": o + 4, "count": n})
        p += 2
    return out


def entries(b, secs=None):
    """{index word position: (section pool, absolute string offset)}."""
    secs = secs if secs is not None else sections(b)
    out = {}
    for s in secs:
        for i in range(s["count"]):
            w = s["index"] + 4 * i
            v = struct.unpack_from("<I", b, w)[0]
            out[w] = (s["pool"], s["pool"] + v)
    return out


def strings(b, sec):
    """{absolute offset: text} for one section, in index order (deduped)."""
    out = {}
    for i in range(sec["count"]):
        v = struct.unpack_from("<I", b, sec["index"] + 4 * i)[0]
        p = sec["pool"] + v
        s = _text_at(b, p)
        if s is not None:
            out[p] = s
    return out


def apply(b, swaps, secs=None):
    """`swaps` = {absolute string offset: encoded bytes}.

    Appends each replacement once and repoints every index entry that pointed
    at the original. Returns (new bytes, {offset: entries repointed}).
    """
    secs = secs if secs is not None else sections(b)
    ents = entries(b, secs)
    out = bytearray(b)
    where, moved = {}, {}
    # sorted, so a rebuild produces the same bytes: every verification in
    # this project is a byte comparison, and dict order would break that
    for off in sorted(swaps):
        enc = swaps[off]
        if enc in where:
            pos = where[enc]
        else:
            if len(out) % 4:
                out += b"\x00" * (4 - len(out) % 4)
            pos = len(out)
            out += enc + b"\x00"
            where[enc] = pos
        n = 0
        for w, (pool, target) in ents.items():
            if target != off:
                continue
            rel = pos - pool
            if rel < 0 or rel > 0xFFFFFFFF:
                raise SystemExit("offset %d unreachable from pool %#x" % (pos, pool))
            struct.pack_into("<I", out, w, rel)
            n += 1
        if not n:
            raise SystemExit("no index entry points at %#x -- refusing to strand it" % off)
        moved[off] = n
    return bytes(out), moved


def build(pristine, docs, mapping, encode):
    """Apply every voice translation document to the pristine file.

    `docs` = [{pool, LINES:{japanese: english}}]. A section is addressed by
    its text-pool offset, not by its ordinal: the section list is recovered
    structurally, so ordinals are an artefact of the parse while the pool
    offset is a fixed position in the shipped file.

    Encoding happens HERE, with the mapping of the run that is building, so
    the voice lines can never go stale against a reshuffled atlas.
    """
    secs = sections(pristine)
    bypool = {s['pool']: s for s in secs}
    swaps, missing = {}, []
    for doc in docs:
        # `"pool": "*"` means every section: some barks are shared by dozens
        # of pilots, and a probe wants them all at once
        if doc.get('pool') == '*':
            targets = secs
        else:
            pool = int(doc['pool'], 16) if isinstance(doc['pool'], str) else doc['pool']
            sec = bypool.get(pool)
            if sec is None:
                raise SystemExit('no voice section with pool %#x' % pool)
            targets = [sec]
        want = doc.get('LINES') or {}
        seen = set()
        for sec in targets:
            for off, jp in strings(pristine, sec).items():
                if jp in want:
                    swaps[off] = encode(want[jp])
                    seen.add(jp)
        missing += [jp for jp in want if jp not in seen]
    if missing:
        raise SystemExit('voice lines not found in their section: %r' % missing[:5])
    if not swaps:
        return pristine, {}, 0
    new, moved = apply(pristine, swaps, secs)
    n = verify(pristine, new, swaps, moved)
    return new, moved, n


def verify(orig, new, swaps, moved):
    """Outside the appended block, only the chosen entries may have changed."""
    assert len(new) >= len(orig), "file shrank"
    ents = entries(orig)
    allowed = set()
    for off in swaps:
        for w, (_pool, target) in ents.items():
            if target == off:
                allowed.update(range(w, w + 4))
    bad = [i for i in range(len(orig))
           if orig[i] != new[i] and i not in allowed]
    assert not bad, "unexpected byte change at %s" % [hex(x) for x in bad[:8]]
    # and every repointed entry must now resolve to what we put there
    for w, (pool, target) in ents.items():
        if target in swaps:
            v = struct.unpack_from("<I", new, w)[0]
            got = new[pool + v:new.find(b"\x00", pool + v)]
            assert got == swaps[target], "entry %#x resolves wrong" % w
    return sum(moved.values())


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd, path = argv[1], argv[2]
    b = open(path, "rb").read()
    secs = sections(b)

    if cmd == "sections":
        print("%d sections, %d index entries" % (len(secs), sum(s["count"] for s in secs)))
        for i, s in enumerate(secs[:20]):
            st = strings(b, s)
            print("  %3d  pool %#09x  index %#09x  %4d entries, %4d distinct lines"
                  % (i, s["pool"], s["index"], s["count"], len(st)))
        return 0

    if cmd == "find":
        needle = argv[3]
        for i, s in enumerate(secs):
            st = strings(b, s)
            hits = [t for t in st.values() if needle in t]
            if hits:
                print("  section %3d (pool %#09x): %d of %d lines contain it"
                      % (i, s["pool"], len(hits), len(st)))
        return 0

    if cmd == "dump":
        i = int(argv[3])
        st = strings(b, secs[i])
        print("section %d: pool %#x, %d distinct lines" % (i, secs[i]["pool"], len(st)))
        if len(argv) > 4:
            json.dump({("%#x" % k): v for k, v in sorted(st.items())},
                      open(argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("  -> %s" % argv[4])
        return 0

    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
