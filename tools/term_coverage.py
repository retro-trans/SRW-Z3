"""Which glossary terms in the SOURCE did not survive into the translation?

`tokenise.py` converts a literal English term into a `$$日本語$$` reference by
matching the glossary's English exactly. That is safe -- it round-trips -- but
it is silent about the case that matters: a translator who rendered a term
differently from the glossary. Those never tokenise, so they never track a
later rename, and nothing complains.

So compare the two sides directly. For every record, take the glossary terms
whose JAPANESE appears in the source line, and check whether that term's
English (or a reference to it) appears in the translation. What comes out is a
list of terms a human should look at, not a list of errors: a term can legally
vanish (Japanese repeats a name English would pronoun away) and a term can be
inflected past a literal match.

    python tools/term_coverage.py <member.lua> <answers.json>.. [--min-len 3]
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import luarec   # noqa: E402
import terms as T   # noqa: E402


def coverage(recs, answers, gterms, min_len=3):
    """[(sha, jp_term, english_wanted, translation)] for terms that vanished."""
    by_jp = {}
    for t in gterms:
        if t.get("en") and len(t["jp"]) >= min_len:
            by_jp.setdefault(t["jp"], []).append(t)
    missed = []
    for r in recs:
        en = answers.get(r["sha"])
        if not en:
            continue
        # lines are hand-wrapped, so a term can straddle a break: "Destruction"
        # then an indented "Incident". Collapse whitespace before matching, or
        # every wrapped term reads as missing.
        flat = " ".join(en.split())
        jp = r["jp"]
        for term_jp, cands in by_jp.items():
            if term_jp not in jp:
                continue
            # the reference form counts as present, as does any candidate's English
            if "$$" + term_jp in en:
                continue
            if any(c["en"] and c["en"].lower() in flat.lower() for c in cands):
                continue
            missed.append((r["sha"], term_jp, "/".join(c["en"] for c in cands), en))
    return missed


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    lua = argv[1]
    paths = [a for a in argv[2:] if not a.startswith("--")]
    min_len = int(argv[argv.index("--min-len") + 1]) if "--min-len" in argv else 3
    recs = luarec.records(open(lua, "rb").read().decode("cp932"))
    answers = {}
    for p in paths:
        answers.update(json.load(open(p, encoding="utf-8")))
    g = json.load(open("analysis/glossary.json", encoding="utf-8"))

    missed = coverage(recs, answers, g["terms"], min_len)
    seen = {}
    for sha, jp, want, en in missed:
        seen.setdefault((jp, want), []).append((sha, en))
    print("%s: %d records, %d term occurrences not carried through"
          % (os.path.basename(lua), len(recs), len(missed)))
    for (jp, want), rows in sorted(seen.items(), key=lambda kv: -len(kv[1])):
        print("  %-16s glossary says %-30s  %d line(s)" % (jp, want, len(rows)))
        sha, en = rows[0]
        print("      %s  %r" % (sha, en.replace("\n", " / ")[:88]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
