"""Cache the shipped `{sha: english}` table once, so slices need not rebuild it.

    python tools/shipped_index.py          writes work/tr/shipped.json

Every brief tells its slice to reuse the English of any record whose Japanese
already ships, because a record's identity is a hash of its Japanese. Building
that table means reading every `translation/stage*.json`, and six slices doing
it in parallel is what a usage limit killed mid-scan in stage 83 -- all six
died during the survey, before writing a single record.

Doing it once per batch costs one pass and leaves a file each slice can load
in a line. The table records the MAJORITY wording for a sha and how many
copies it has, plus the runners-up, so a slice can see that a sha is contested
without re-deriving the counts -- stage 80 hit a genuine 1-1 tie and stage 78
a 36-3 split, and those want different handling.

Battle subtitles are deliberately NOT here: `translation/voice_*.json` has no
`sha` at all, being a `lines` dict of `{jp, en}`. Search those by Japanese
text when you want precedent for a term.
"""
import collections
import io
import json
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build(root=ROOT):
    ship = collections.defaultdict(collections.Counter)
    files = 0
    for path in sorted(glob.glob(os.path.join(root, "translation", "stage*.json"))):
        try:
            with io.open(path, encoding="utf-8") as stream:
                doc = json.load(stream)
        except Exception:
            continue
        files += 1
        for rec in doc.get("LINES", []):
            if rec.get("en"):
                ship[rec["sha"]][rec["en"]] += 1
    out = {}
    contested = 0
    for sha, counter in ship.items():
        ranked = counter.most_common()
        row = {"en": ranked[0][0], "n": ranked[0][1]}
        if len(ranked) > 1:
            contested += 1
            # a slice that lands on one of these should know it is a choice
            row["others"] = [[text, n] for text, n in ranked[1:]]
            row["tied"] = ranked[1][1] == ranked[0][1]
        out[sha] = row
    return out, files, contested


def main(argv):
    table, files, contested = build()
    target = os.path.join(ROOT, "work", "tr", "shipped.json")
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with io.open(target, "w", encoding="utf-8") as stream:
        json.dump(table, stream, ensure_ascii=False)
    size = os.path.getsize(target)
    print("%d shas from %d files (%d ship more than one wording) -> %s  %.1f MB"
          % (len(table), files, contested, os.path.relpath(target, ROOT),
             size / 1048576.0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
