"""Work out whose voice each section is, from the names spoken inside it.

The file carries no speaker labels: no prefix on the lines, no directory in the
header, no cue names in the audio container. But battle barks are full of names
-- a pilot announces their own on a sortie or a finisher, and calls out allies
and rivals constantly. So score every section against every glossary pilot name
and see which name owns it.

The result is checkable rather than merely plausible: if the scoring is finding
real speakers, the mapping should be close to one-name-one-section. Names that
win many sections at once, or sections whose best name barely beats the runner
up, are exactly the cases to distrust, and both are reported.

    python tools/srvc_identify.py <SRVC.BIN> <glossary.json> [out.json]
"""
import collections
import io
import json
import os
import pickle
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import srvc   # noqa: E402

MIN_NAME = 3          # shorter names collide with ordinary words


def load_sections(path):
    cache = os.path.join(os.path.dirname(path), "sections.pickle")
    if os.path.exists(cache):
        return pickle.load(open(cache, "rb"))
    b = open(path, "rb").read()
    secs = srvc.sections(b)
    try:
        pickle.dump(secs, open(cache, "wb"))
    except OSError:
        pass
    return secs


def score(b, secs, names):
    """[(section, [(name, hits)...])] -- names spoken in each section."""
    out = []
    for s in secs:
        texts = list(srvc.strings(b, s).values())
        blob = "\n".join(texts)
        c = collections.Counter()
        for jp in names:
            n = blob.count(jp)
            if n:
                c[jp] = n
        out.append((s, c.most_common()))
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    path, gpath = argv[1], argv[2]
    b = open(path, "rb").read()
    secs = load_sections(path)
    g = json.load(open(gpath, encoding="utf-8"))
    names = sorted({t["jp"] for t in g["terms"]
                    if t["kind"] == "pilot" and len(t["jp"]) >= MIN_NAME},
                   key=len, reverse=True)
    en = {t["jp"]: t["en"] for t in g["terms"] if t["en"]}
    print("%d sections, scoring against %d pilot names" % (len(secs), len(names)))

    rows = score(b, secs, names)
    best, claims = {}, collections.Counter()
    for i, (s, top) in enumerate(rows):
        if not top:
            continue
        name, n = top[0]
        runner = top[1][1] if len(top) > 1 else 0
        best[i] = (name, n, runner)
        claims[name] += 1

    named = len(best)
    unique = sum(1 for n_ in claims.values() if n_ == 1)
    print("sections with a named winner: %d of %d; names winning exactly one "
          "section: %d" % (named, len(secs), unique))
    print()
    print("  sec  pool         lines  winner                 hits  runner-up  confidence")
    for i, (s, top) in enumerate(rows):
        if i not in best:
            continue
        name, n, runner = best[i]
        conf = "strong" if n >= 3 and n >= 2 * max(1, runner) else (
            "weak" if n <= 1 or n <= runner else "fair")
        print("  %3d  %#010x  %4d  %-20s %4d  %8d  %s"
              % (i, s["pool"], s["count"], "%s / %s" % (name, en.get(name, "?"))[:20],
                 n, runner, conf))

    dupes = [(k, v) for k, v in claims.items() if v > 1]
    if dupes:
        print()
        print("names claiming several sections (a pilot has one voice set, so "
              "these need a closer look):")
        for k, v in sorted(dupes, key=lambda kv: -kv[1])[:10]:
            print("   %-16s %d sections" % ("%s/%s" % (k, en.get(k, "?")), v))

    if len(argv) > 3:
        json.dump({str(i): {"pool": "%#x" % rows[i][0]["pool"],
                            "name_jp": best[i][0], "name_en": en.get(best[i][0]),
                            "hits": best[i][1], "runner_up": best[i][2]}
                   for i in best},
                  open(argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("-> %s" % argv[3])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
