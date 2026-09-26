"""Fold verification verdicts back into the glossary.

A verification agent returns one JSON row per term: verified, corrected, or
unverified, with a URL wherever it claims the first two. This applies them
with the same discipline the tiers on the glossary page promise:

  verified    -> src = the URL, status = official (ambiguous terms stay so)
  corrected   -> en replaced by the wiki spelling, src = the URL, and the
                 change is ALSO applied to every translation file, because a
                 name lives in the script and the library as well as here
  unverified  -> untouched. It stays in its tier honestly.

A verdict of verified/corrected with no URL is refused, not applied: a
citation-free promotion is exactly the thing this whole exercise exists to
prevent.

    python tools/apply_verification.py <glossary.json> <verdicts.json> [more.json ...]
"""
import glob
import io
import json
import sys


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    gpath, files = argv[1], argv[2:]
    g = json.load(open(gpath, encoding="utf-8"))
    idx = {}
    for t in g["terms"]:
        idx.setdefault((t["kind"], t["en"]), []).append(t)

    verified = corrected = unverified = refused = unmatched = 0
    renames = []
    for f in files:
        for row in json.load(open(f, encoding="utf-8")):
            v = row.get("verdict")
            if v == "unverified":
                unverified += 1
                continue
            if not row.get("url"):
                refused += 1
                print("  REFUSED (no url): %r" % row.get("en"))
                continue
            hits = idx.get((row.get("kind") or _kind_of(row, g), row["en"])) \
                or [t for t in g["terms"] if t["en"] == row["en"]]
            if not hits:
                unmatched += 1
                print("  unmatched: %r" % row["en"])
                continue
            for t in hits:
                t["src"] = row["url"]
                if t["status"] != "ambiguous":
                    t["status"] = "official"
                if v == "corrected" and row.get("correct_en") and row["correct_en"] != t["en"]:
                    renames.append((t["en"], row["correct_en"]))
                    t["note"] = ((t.get("note") or "") + " [spelling corrected on verification]").strip()
                    t["en"] = row["correct_en"]
                    corrected += 1
                else:
                    verified += 1

    json.dump(g, open(gpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    # a corrected name must change everywhere it was already used
    touched = 0
    if renames:
        for p in glob.glob("translation/**/*.py", recursive=True):
            s = open(p, encoding="utf-8").read()
            o = s
            for a, b in renames:
                s = s.replace(a, b)
            if s != o:
                open(p, "w", encoding="utf-8").write(s)
                touched += 1

    print("verified %d, corrected %d, unverified %d, refused %d, unmatched %d"
          % (verified, corrected, unverified, refused, unmatched))
    if renames:
        print("renames applied to %d translation files:" % touched)
        for a, b in sorted(set(renames)):
            print("   %s -> %s" % (a, b))
    return 0


def _kind_of(row, g):
    for t in g["terms"]:
        if t["en"] == row["en"]:
            return t["kind"]
    return ""


if __name__ == "__main__":
    sys.exit(main(sys.argv))
