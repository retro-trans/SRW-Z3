"""Carry a translated section's English to the sections that repeat it.

    python tools/voice_propagate.py            propagate everything available
    python tools/voice_propagate.py 18         only from section 18
    python tools/voice_propagate.py --list     what would be carried, no writes

Twenty groups of sections hold the same voice set two or three times over:
17, 18 and 19 are 197 of 198 byte-identical, and 4,115 of the 31,670 lines
to translate live in such repeats. Translating them again would not only
waste the work, it would ship the SAME unit saying the same Japanese two
different ways on screen.

Lines are matched by their Japanese text, never by entry number: the entry
numbering differs between sections of a group, the strings do not. Anything
the source section does not cover is left for a translator, so a partial
match is still useful.
"""
import glob
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_voice as C     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SENTINEL = ("－－－", "無音", "表示しません")


def lines_of(sec):
    """Distinct, translatable lines of a section: {jp: entry}."""
    src = C.source(sec)
    return {r["jp"]: r["i"] for r in src if not r["shared"]
            and not any(m in r["jp"] for m in SENTINEL)}


def groups():
    """Sections that hold the same voice set, from work/voice/clusters.json
    if it is there, else recomputed by comparing the line sets themselves."""
    p = os.path.join(ROOT, "work", "voice", "clusters.json")
    if os.path.exists(p):
        return [g for g in json.load(open(p, encoding="utf-8")) if len(g) > 1]
    sets, out, seen = {}, [], set()
    for f in sorted(glob.glob(os.path.join(ROOT, "source", "voice", "*.json"))):
        b = os.path.basename(f)[:-5]
        if b.isdigit():
            sets[int(b)] = set(lines_of(int(b)))
    for i in sorted(sets):
        if i in seen:
            continue
        g = [i]
        for j in sorted(sets):
            if j > i and j not in seen and sets[i] and sets[j]:
                if len(sets[i] & sets[j]) >= 0.9 * min(len(sets[i]), len(sets[j])):
                    g.append(j); seen.add(j)
        seen.add(i)
        if len(g) > 1:
            out.append(g)
    return out


def english_of(sec):
    """{jp: english} for a section that has been translated, from its
    published doc if there is one, else from a raw answer file."""
    doc = os.path.join(ROOT, "translation", "voice_%03d.json" % sec)
    if os.path.exists(doc):
        d = json.load(open(doc, encoding="utf-8"))
        return {v["jp"]: v["en"] for v in d["lines"].values()
                if isinstance(v, dict)}
    ans = os.path.join(ROOT, "work", "voice", "answer", "%03d.json" % sec)
    if os.path.exists(ans):
        src = {r["i"]: r["jp"] for r in C.source(sec)}
        a = json.load(open(ans, encoding="utf-8"))
        return {src[int(k)]: v for k, v in a.items() if int(k) in src}
    return {}


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    only = {int(a) for a in argv[1:] if not a.startswith("--")}
    dry = "--list" in argv
    total = 0
    for g in groups():
        have = [s for s in g if english_of(s)]
        if only:
            have = [s for s in have if s in only]
        if not have:
            continue
        src_sec = have[0]
        by_jp = english_of(src_sec)
        for dst in g:
            if dst == src_sec or english_of(dst):
                continue
            want = lines_of(dst)
            out = {str(i): by_jp[jp] for jp, i in want.items() if jp in by_jp}
            if not out:
                continue
            path = "work/voice/answer/%03d.json" % dst
            print("%d -> %d: %d of %d lines%s"
                  % (src_sec, dst, len(out), len(want),
                     "" if len(out) == len(want) else
                     " (%d left to translate)" % (len(want) - len(out))))
            total += len(out)
            if not dry:
                json.dump(out, open(os.path.join(ROOT, path), "w",
                                    encoding="utf-8"),
                          ensure_ascii=False, indent=1)
    print("%d lines carried%s" % (total, " (dry run)" if dry else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
