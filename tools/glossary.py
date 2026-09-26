"""The translation glossary: one place a term's English form is decided.

Seeded from the game's own library (図鑑), which is better provenance than any
outside list -- the game states which series every term belongs to, so
`ガイオウ` in a Gundam entry and in an original entry can be told apart.

Why a database and not a find-and-replace list: the PS2 project's hard-won
rule is that **a term and its 《》 links are ONE edit**, and that the entries
which break a global rename are the AMBIGUOUS ones. So every term carries:

    jp          the japanese as it appears in the game
    en          the english to use
    kind        keyword | pilot | robot | series
    source      the series the library assigns it to
    status      official  -- a published english name exists, use it verbatim
                proposed  -- our coinage, may still change
                ambiguous -- do NOT globally replace; the same string means
                             different things in different series
    note        why, when it is not obvious

    python tools/glossary.py seed  <libdir> <glossary.json>
    python tools/glossary.py merge <glossary.json> <patch.json>
    python tools/glossary.py stats <glossary.json>
    python tools/glossary.py check <glossary.json>
"""
import json
import os
import sys

KINDS = ("series", "keyword", "pilot", "robot")


def load(path):
    if os.path.exists(path):
        return json.load(open(path, encoding="utf-8"))
    return {"meta": {"note": "seeded from the in-game library"}, "terms": []}


def save(g, path):
    g["terms"].sort(key=lambda t: (KINDS.index(t["kind"]), t.get("source", ""), t["jp"]))
    json.dump(g, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def seed(libdir, path):
    g = load(path)
    have = {(t["kind"], t["jp"]) for t in g["terms"]}
    added = 0

    def add(kind, jp, source="", zid=None, field=""):
        nonlocal added
        jp = (jp or "").strip()
        if not jp or (kind, jp) in have:
            return
        have.add((kind, jp))
        g["terms"].append({"jp": jp, "en": "", "kind": kind, "source": source,
                           "zukan_id": zid, "field": field, "status": "todo",
                           "note": ""})
        added += 1

    kw = json.load(open(os.path.join(libdir, "MTZKN_KW.json"), encoding="utf-8"))
    pt = json.load(open(os.path.join(libdir, "MTZKN_PT.json"), encoding="utf-8"))
    rt = json.load(open(os.path.join(libdir, "MTZKN_RT.json"), encoding="utf-8"))

    for r in kw:
        add("series", r.get("SRCE", "").strip("\u300c\u300d"))
        add("keyword", r.get("WORD"), r.get("SRCE", ""), r["id"], "WORD")
    for r in pt:
        add("series", r.get("PRDC", "").strip("\u300c\u300d"))
        add("pilot", r.get("CHFN"), r.get("PRDC", ""), r["id"], "CHFN")
        if r.get("CHNN") and r.get("CHNN") != r.get("CHFN"):
            add("pilot", r.get("CHNN"), r.get("PRDC", ""), r["id"], "CHNN")
    for r in rt:
        add("series", r.get("PRDC", "").strip("\u300c\u300d"))
        add("robot", r.get("RBTN"), r.get("PRDC", ""), r["id"], "RBTN")
        if r.get("RBN2") and r.get("RBN2") != r.get("RBTN"):
            add("robot", r.get("RBN2"), r.get("PRDC", ""), r["id"], "RBN2")
    save(g, path)
    return added, len(g["terms"])


def stats(g):
    out = {}
    for k in KINDS:
        ts = [t for t in g["terms"] if t["kind"] == k]
        done = [t for t in ts if t["en"]]
        out[k] = (len(done), len(ts))
    return out


def check(g):
    """Problems that silently corrupt a translation."""
    bad = []
    seen = {}
    for t in g["terms"]:
        if t["en"] and t["status"] == "todo":
            bad.append(("status still todo though translated", t["jp"]))
        key = (t["kind"], t["jp"])
        if key in seen and seen[key] != t["en"]:
            bad.append(("same term, two different english", t["jp"]))
        seen[key] = t["en"]
    # One english for two different japanese terms is usually a mistake, but
    # the game itself spells some series two ways (with and without a colon),
    # so a term can declare itself an intentional alias.
    # Likewise `ambiguous`: two different people can legitimately share an
    # english name (桂 and 渓 are both "Kei"). That is a fact to record, not a
    # collision to fix -- the rule it implies is "never rename globally".
    rev = {}
    for t in g["terms"]:
        if not t["en"] or t.get("alias") or t["status"] == "ambiguous":
            continue
        k = (t["kind"], t["en"].lower())
        if k in rev and rev[k] != t["jp"]:
            bad.append(("one english for two japanese: %r" % t["en"],
                        "%s / %s" % (rev[k], t["jp"])))
        rev[k] = t["jp"]
    return bad


def lint_translation(g, lines):
    """Flag places a translation contradicts the glossary.

    This is the whole point of having one. It caught `時空震動` being shipped
    as "Spacetime Tremor" in stage 1 while the glossary settled on
    "Spacequake" -- the kind of drift nobody notices until two scenes disagree
    on screen.
    """
    import re
    text = "\n".join(lines)
    gl = {t["en"]: t["jp"] for t in g["terms"]
          if t["kind"] == "keyword" and t["en"] and t["status"] != "ambiguous"}
    hits = []
    for used in sorted(set(re.findall(r"《(.*?)》", text))):
        if used not in gl:
            hits.append(("linked term is not the glossary english", used))
    for t in g["terms"]:
        if t["kind"] == "keyword" and t["jp"] in text:
            hits.append(("japanese term left untranslated", t["jp"]))
    return hits


def merge(g, patch):
    """Apply {jp, kind, en, status, note} rows onto the seeded terms."""
    idx = {(t["kind"], t["jp"]): t for t in g["terms"]}
    applied = missing = 0
    for row in patch:
        key = (row["kind"], row["jp"])
        t = idx.get(key)
        if t is None:
            missing += 1
            continue
        t["en"] = row["en"]
        t["status"] = row.get("status", "proposed")
        if row.get("note"):
            t["note"] = row["note"]
        applied += 1
    return applied, missing


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd = argv[1]
    if cmd == "seed":
        added, total = seed(argv[2], argv[3])
        print("added %d terms, %d total -> %s" % (added, total, argv[3]))
        return 0
    g = load(argv[2])
    if cmd == "merge":
        patch = json.load(open(argv[3], encoding="utf-8"))
        a, m = merge(g, patch)
        save(g, argv[2])
        print("applied %d, %d not found in the seed" % (a, m))
        return 0
    if cmd == "stats":
        for k, (d, n) in stats(g).items():
            pct = 100.0 * d / n if n else 0
            print("  %-8s %4d / %-4d  %5.1f%%" % (k, d, n, pct))
        tot = sum(n for _, n in stats(g).values())
        done = sum(d for d, _ in stats(g).values())
        print("  %-8s %4d / %-4d  %5.1f%%" % ("TOTAL", done, tot, 100.0 * done / tot))
    elif cmd == "check":
        bad = check(g)
        for why, what in bad:
            print("  %-42s %s" % (why, what))
        print("%d problems" % len(bad))
    else:
        print("unknown command %r" % cmd)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
