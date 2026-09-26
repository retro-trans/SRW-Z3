"""Rewrite literal glossary terms in translated prose as `$$id$$` references.

A one-off migration for text written before `tools/terms.py` existed, and a
repeat pass for prose written by hand since.

The safety property is simple and absolute: a rewritten string is kept ONLY if
expanding it again reproduces the original character for character. Anything
that does not round-trip is left alone and reported. So a full build before and
after this tool must produce byte-identical output -- that is the test, not an
argument.

What is skipped, and why:

* English shared by two terms (21 of them, e.g. `Aquarion EVOL` is both the
  series and the robot). There is no way to know which id the line meant.
* Terms with no English yet.
* Single-word terms that are ordinary English words (`An`, `King`, `Sphere`,
  `Zero`...). A pilot is named 安 = "An", and all 140 matches for it were the
  article; capitalisation does not separate them because a sentence starts
  with one. They are listed on every run and re-admitted one at a time with
  --force, which is right for `Sphere` (always the plot device when capital).
  --skip/--only/--force match either the Japanese or the English.
* `NAMES` maps and the `jp` side of anything. Only prose is touched:
  `LINES[].en` in the stage files, `ENTRIES[].DSCR/DSC2` in the library batches.

Longest term wins, so `Sphere Reactor` is never split into `$$sphere$$ Reactor`.
A suffix stays outside the token, which is what makes plurals work:
`Spheres` -> `$$sphere$$s`.

    python tools/tokenise.py <glossary.json> <dir>.. [--write] [--skip a,b]
                                                     [--min-len N] [--only a,b]
                                                     [--force a,b]

Dry run by default: nothing is written until --write.
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import terms as T   # noqa: E402

# A single-word term that is ALSO an ordinary English word cannot be
# matched safely: 安 is a pilot named An, and all 140 hits for it were the
# article. Capitalisation does not separate them either, because a
# sentence starts with one. These are skipped by default and can be
# forced back in one at a time with --only.
COMMON = set("""
a an the and or but if then than that this these those there here
i you he she it we they me him her us them my your his its our their
is am are was were be been being do does did done has have had
will would shall should can could may might must
of to in into on at by for from with without within about over under
up down out off again once no not now just only also very too so
one two three all any both each few more most other some such own same
king queen prince princess angel zero ace arc bell hero heroine
sun moon star sky wind fire water earth light dark shadow storm
blade sword shield crown giant beast dragon knight master lord lady
mother father sister brother son daughter child man woman boy girl
doctor professor captain colonel major general president chairman
teacher student soldier pilot captain sergeant nurse driver
east west north south left right front back top bottom
red blue green black white gray grey gold silver
war peace world sphere soul heart mind body life death time space
first second third last next new old good bad big small long short
""".split())


def risky(en):
    """A term whose English is a single ordinary word."""
    return " " not in en and en.lower() in COMMON


def candidates(g, skip=(), min_len=2, only=(), force=()):
    """[(english, id, pattern)] longest first; ambiguous and ordinary-word
    English removed unless named in --only."""
    dropped = []
    idx = T.index(g)
    by_en = {}
    for t in g["terms"]:
        if t.get("en"):
            by_en.setdefault(t["en"], []).append(T.token_for(t, idx))
    out = []
    for en, ids in by_en.items():
        if len(ids) > 1:            # two terms, same English: unresolvable
            continue
        names = {ids[0].strip('$').split('#')[0], en}   # japanese or english
        if (names & skip) or len(en) < min_len:
            continue
        if only and not (names & only):
            continue
        if risky(en) and not (names & force):
            dropped.append((ids[0], en))
            continue
        out.append((en, ids[0]))
    candidates.dropped = sorted(dropped)
    out.sort(key=lambda p: (-len(p[0]), p[0]))
    # compile once: 1,116 terms x 1,046 strings is not the place to build
    # a pattern per pass
    return [(en, tid, re.compile(r"(?<![0-9A-Za-z])" + re.escape(en) +
                                 r"(?![0-9A-Za-z])")) for en, tid in out]


def rewrite(text, cands, idx):
    """Tokenise, then prove it. Returns (new_text, {id: count}) or (text, {})
    if the round trip does not match exactly."""
    if not text:
        return text, {}
    out = text
    hits = {}
    for en, tid, pat in cands:
        if en not in out:
            continue
        # do not match inside an existing token
        pieces = []
        last = 0
        for m in pat.finditer(out):
            if "$$" in out[max(0, m.start() - 64):m.start()].rsplit("\n", 1)[-1]:
                # cheap guard: skip if an unclosed $$ precedes on this line
                seg = out[:m.start()].rsplit("\n", 1)[-1]
                if seg.count("$$") % 2:
                    continue
            pieces.append(out[last:m.start()])
            pieces.append(tid)
            last = m.end()
            hits[tid] = hits.get(tid, 0) + 1
        if not pieces:
            continue
        pieces.append(out[last:])
        out = "".join(pieces)
    if out == text:
        return text, {}
    if T.expand(out, idx) != text:          # the invariant
        return text, {"__ROUNDTRIP__": 1}
    return out, hits


def sources(dirs):
    """(path, doc) for every translation JSON that holds prose."""
    for d in dirs:
        files = [d] if os.path.isfile(d) else [
            os.path.join(r, f) for r, _s, fs in os.walk(d)
            for f in fs if f.endswith(".json")]
        for p in sorted(files):
            try:
                doc = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            if "LINES" in doc or "ENTRIES" in doc:
                yield p, doc


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    gpath = argv[1]
    dirs = [a for a in argv[2:] if not a.startswith("--")]
    write = "--write" in argv
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv else set()
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else set()
    force = set(argv[argv.index("--force") + 1].split(",")) if "--force" in argv else set()
    min_len = int(argv[argv.index("--min-len") + 1]) if "--min-len" in argv else 2

    g = json.load(open(gpath, encoding="utf-8"))
    idx = T.index(g)
    cands = candidates(g, skip, min_len, only, force)
    print("%d terms eligible (of %d)" % (len(cands), len(idx)))
    drop = getattr(candidates, "dropped", [])
    if drop:
        print("%d skipped as ordinary English words -- pass --only <id> to force one:"
              % len(drop))
        print("   " + ", ".join("%s(%s)" % (i.strip('$'), e) for i, e in drop[:24]))

    total = {}
    failed = []
    changed_files = 0
    for p, doc in sources(dirs):
        touched = 0
        for blk in doc.get("LINES", []) or []:
            if isinstance(blk, dict) and blk.get("en"):
                new, hits = rewrite(blk["en"], cands, idx)
                if hits.get("__ROUNDTRIP__"):
                    failed.append((p, blk.get("sha", "?")))
                    continue
                if new != blk["en"]:
                    blk["en"] = new
                    touched += 1
                for k, v in hits.items():
                    total[k] = total.get(k, 0) + v
        for eid, ent in (doc.get("ENTRIES") or {}).items():
            if not isinstance(ent, dict):
                continue
            for f in ("DSCR", "DSC2"):
                if ent.get(f):
                    new, hits = rewrite(ent[f], cands, idx)
                    if hits.get("__ROUNDTRIP__"):
                        failed.append((p, "%s.%s" % (eid, f)))
                        continue
                    if new != ent[f]:
                        ent[f] = new
                        touched += 1
                    for k, v in hits.items():
                        total[k] = total.get(k, 0) + v
        if touched:
            changed_files += 1
            print("  %-42s %d strings" % (os.path.relpath(p), touched))
            if write:
                json.dump(doc, open(p, "w", encoding="utf-8"),
                          ensure_ascii=False, indent=1)

    n = sum(v for k, v in total.items() if not k.startswith("__"))
    print()
    print("%d references in %d files, %d distinct terms" % (n, changed_files, len(total)))
    for tid, c in sorted(total.items(), key=lambda kv: -kv[1])[:25]:
        print("   %-34s %4d" % (tid, c))
    if failed:
        print("%d strings left alone (did not round-trip): %s" % (len(failed), failed[:5]))
    print("WRITTEN" if write else "dry run -- pass --write to apply")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
