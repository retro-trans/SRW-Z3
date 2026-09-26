"""How much of the battle voice track is translated, and what to do next.

    python tools/voice_status.py            progress, then the best targets
    python tools/voice_status.py --all      every section, translated first

31,670 distinct lines across 211 sections is a many-session job, so the
question "what is done and what is worth doing next" has to be answerable
from the files themselves -- never from memory or a stale list.

A section is worth doing next in proportion to how many lines it buys and
how sure we are whose lines they are: `pts` is srvc_link's weapon-match
confidence, and a section nobody can attribute gets generic barks or gets
left alone, not a guessed name.
"""
import glob
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SENTINEL = ("－－－", "無音", "表示しません")


def rd(*parts):
    return json.load(open(os.path.join(ROOT, *parts), encoding="utf-8"))


def distinct(sec):
    """Lines that actually need translating: one per stored string, minus
    the developers' placeholders, which never reach the screen."""
    src = rd("source", "voice", "%03d.json" % sec)
    return [r for r in src if not r["shared"]
            and not any(m in r["jp"] for m in SENTINEL)]


def done_by_section():
    out = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "translation", "voice_*.json"))):
        doc = json.load(open(p, encoding="utf-8"))
        sec = doc.get("section")
        if sec is None:
            continue
        out[sec] = (len(doc.get("lines", {})), os.path.basename(p))
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    rows = rd("work", "voice", "sections.json")
    gl = rd("analysis", "glossary.json")
    terms = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
    pilots = rd("work", "voice", "pilots.json")
    who = {s: r for r in pilots for s in r["sections"]}
    done = done_by_section()
    answers = {int(os.path.basename(p)[:-5])
               for p in glob.glob(os.path.join(ROOT, "work", "voice", "answer",
                                               "*.json"))
               if os.path.basename(p)[:-5].isdigit()}

    def en_of(jp):
        if not jp:
            return None
        for cand in [jp] + [h.strip() for h in jp.split("/")]:
            for key in (cand, cand.replace(" ", ""), cand.replace("　", "")):
                if terms.get(key):
                    return terms[key]
        return None

    table = []
    for r in rows:
        sec = r["sec"]
        n = len(distinct(sec))
        d = done.get(sec)
        w = who.get(sec) or {}
        table.append({
            "sec": sec, "lines": n, "done": d[0] if d else 0,
            "file": d[1] if d else None, "answered": sec in answers,
            "unit": en_of(r.get("unit")) or r.get("unit"),
            "pilot": en_of(w.get("pilot")) or w.get("pilot"),
            "pts": r.get("pts", 0)})

    total = sum(t["lines"] for t in table)
    shipped = sum(t["done"] for t in table)
    secs_done = sum(1 for t in table if t["file"])
    print("%d of %d lines translated (%.1f%%), %d of %d sections"
          % (shipped, total, 100.0 * shipped / total, secs_done, len(table)))
    pending = [t for t in table if t["answered"] and not t["file"]]
    if pending:
        print("%d sections answered but not merged: %s"
              % (len(pending), " ".join(str(t["sec"]) for t in pending)))

    show = ([t for t in table if t["file"]] +
            sorted((t for t in table if not t["file"]),
                   key=lambda t: (-t["pts"], -t["lines"]))) \
        if "--all" in argv else \
        sorted((t for t in table if not t["file"]),
               key=lambda t: (-t["pts"], -t["lines"]))[:25]
    if "--all" not in argv:
        print("\nBest targets left (confidence first, then size):")
    print("\n%4s %6s %6s %-32s %-22s %s"
          % ("sec", "lines", "done", "unit", "pilot", "pts"))
    for t in show:
        print("%4d %6d %6s %-32s %-22s %.1f"
              % (t["sec"], t["lines"], t["done"] or "-",
                 (t["unit"] or "?")[:32], (t["pilot"] or "")[:22], t["pts"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
