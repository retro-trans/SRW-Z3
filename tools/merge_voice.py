"""Merge a translator's answer into a publishable voice document.

    python tools/merge_voice.py 17 [--answer work/voice/answer/017.json]
                                   [--out translation/voice_017.json]

The answer is a bare {entry: english} object, which is all a translator
should have to produce -- order-free, and two answers can never overwrite
each other's work. The published document is self-describing: it carries the
Japanese, the budget and the section, so a reviewer can check a line without
regenerating anything.

Nothing is written unless tools/check_voice.py passes clean, so a bad answer
never reaches translation/.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_voice as C     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
NOTE = ("Voice lines may be any length since the block rebuild; budget is "
        "the original slot size, informational only. Keep a line under about "
        "36 cells -- one per letter, one per backslash-n break -- so it fits "
        "the screen. "
        "Regenerate jp with tools/extract.py; the Japanese for this section "
        "is source/voice/%03d.json.")


def rd(*parts):
    return json.load(open(os.path.join(ROOT, *parts), encoding="utf-8"))


def build(sec, answer):
    src = {r["i"]: r for r in C.source(sec)}
    secrow = {r["sec"]: r for r in rd("work", "voice", "sections.json")}[sec]
    gl = rd("analysis", "glossary.json")
    terms = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
    pilots = rd("work", "voice", "pilots.json")
    who = next((r for r in pilots if sec in r["sections"]), None)

    def en_of(jp):
        """Glossary English for a name; unit names may hold two spellings
        separated by a slash. Falls back to the Japanese, never to nothing."""
        if not jp:
            return None
        for cand in [jp] + [h.strip() for h in jp.split("/")]:
            for key in (cand, cand.replace(" ", ""), cand.replace("　", "")):
                if terms.get(key):
                    return terms[key]
        return jp

    lines = {}
    for k in sorted(answer, key=int):
        n = int(k)
        lines[str(n)] = {"jp": src[n]["jp"], "en": answer[k],
                         "budget": src[n]["budget"]}
    doc = {"section": sec,
           "unit": en_of(secrow.get("unit")),
           "unit_jp": secrow.get("unit"),
           "pilots": [en_of(who["pilot"])] if who and who["pilot"] else [],
           "note": NOTE % sec,
           "lines": lines}
    # A correction read out of the lines themselves beats the weapon match.
    ipath = os.path.join(ROOT, "analysis", "voice_identity.json")
    if os.path.exists(ipath):
        fixed = json.load(open(ipath, encoding="utf-8")).get(str(sec))
        if fixed:
            doc["unit"] = fixed.get("unit")
            doc["unit_jp"] = None
            doc["pilots"] = [fixed["pilot"]] if fixed.get("pilot") else []
            doc["note"] += "  IDENTITY: " + fixed["why"]
    return doc


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    args, flags, skip = [], {}, None
    for a in argv[1:]:
        if skip:
            flags[skip], skip = a, None
        elif a in ("--answer", "--out"):
            skip = a
        elif not a.startswith("--"):
            args.append(a)
    if not args:
        print(__doc__.strip())
        return 2
    rc = 0
    for a in args:
        sec = int(a)
        ap = flags.get("--answer", "work/voice/answer/%03d.json" % sec)
        out = flags.get("--out", "translation/voice_%03d.json" % sec)
        answer = json.load(open(os.path.join(ROOT, ap), encoding="utf-8"))
        problems, notes = C.validate(sec, answer)
        got, want, missing = C.coverage(sec, answer)
        print("section %d: %d of %d distinct lines answered" % (sec, got, want))
        for n in notes:
            print("  note    %s" % n)
        for p in problems:
            print("  PROBLEM %s" % p)
        if problems:
            print("  refused -- fix the answer, nothing written")
            rc = 1
            continue
        if missing:
            print("  %d entries left in Japanese: %s%s"
                  % (len(missing), " ".join(str(m) for m in missing[:20]),
                     " ..." if len(missing) > 20 else ""))
        doc = build(sec, answer)
        path = os.path.join(ROOT, out)
        json.dump(doc, open(path, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print("  wrote %s (%d lines)" % (out, len(doc["lines"])))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
