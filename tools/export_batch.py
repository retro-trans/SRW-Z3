"""Export library entries as translation briefs for a subagent.

Writes one markdown file per batch containing the Japanese source, plus a
shared glossary sheet. Keeping the brief on disk means a translator agent only
needs a path, not a wall of pasted text.

    python tools/export_batch.py <MTZKN_*.json> <kind> <outdir> <batch-size>
"""
import json
import os
import sys

FIELDS = {
    "kw": [("WORD", "term"), ("SRCE", "series")],
    "pt": [("CHFN", "full name"), ("CHNN", "short name"), ("PRDC", "series")],
    "rt": [("RBTN", "unit"), ("RBN2", "unit alt"), ("PLTN", "pilot"),
           ("PRDC", "series"), ("HEIT", "height"), ("WEIT", "weight")],
}


def glossary_sheet(gpath, out):
    g = json.load(open(gpath, encoding="utf-8"))
    lines = ["# Settled terminology - USE THESE EXACTLY", ""]
    for kind in ("series", "keyword", "pilot", "robot"):
        rows = [t for t in g["terms"] if t["kind"] == kind and t["en"]]
        if not rows:
            continue
        lines.append("## %s" % kind)
        for t in sorted(rows, key=lambda r: r["jp"]):
            flag = "  [AMBIGUOUS: %s]" % t["note"] if t["status"] == "ambiguous" else ""
            lines.append("- %s = %s%s" % (t["jp"], t["en"], flag))
        lines.append("")
    open(out, "w", encoding="utf-8").write("\n".join(lines))
    return sum(1 for t in g["terms"] if t["en"])


def main(argv):
    src, kind, outdir, size = argv[1], argv[2], argv[3], int(argv[4])
    os.makedirs(outdir, exist_ok=True)
    recs = json.load(open(src, encoding="utf-8"))
    todo = [r for r in recs if r.get("DSCR")]
    made = []
    for i in range(0, len(todo), size):
        chunk = todo[i:i + size]
        lo, hi = chunk[0]["id"], chunk[-1]["id"]
        p = os.path.join(outdir, "%s_%04d.md" % (kind, lo))
        L = ["# %s entries %d-%d (%d records)" % (kind, lo, hi, len(chunk)), ""]
        for r in chunk:
            L.append("## id %d" % r["id"])
            for f, label in FIELDS[kind]:
                if r.get(f):
                    L.append("- %s (%s): %s" % (label, f, r[f]))
            L.append("")
            L.append("DSCR:")
            L.append("```")
            L.append(r["DSCR"])
            L.append("```")
            if r.get("DSC2") and r["DSC2"] != r["DSCR"]:
                L.append("DSC2 (DIFFERS - translate separately):")
                L.append("```")
                L.append(r["DSC2"])
                L.append("```")
            L.append("")
        open(p, "w", encoding="utf-8").write("\n".join(L))
        made.append((p, lo, hi, len(chunk)))
    for p, lo, hi, n in made:
        print("%s  ids %d-%d  %d records" % (p, lo, hi, n))
    print("%d batches" % len(made))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
