"""Fold the NAMES a translation batch produced into the glossary.

Subagents translate names as they go; this pulls them in as `proposed` so they
can be reviewed, and never overwrites a term already settled against akurasu.

    python tools/harvest_names.py <glossary.json> <library_pt.py|library_rt.py> <kind>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trdata  # noqa: E402


def load_names(path, gpath=None, kind=None):
    """NAMES from a translation file, parsed not executed. A directory of
    batch files is assembled; a single .json is read directly; the legacy
    library_*.py shim is accepted by reading the JSON directory it wraps."""
    amb = trdata.ambiguous_terms(gpath) if gpath else set()
    if os.path.isdir(path):
        # batch files are <prefix>_NNN.json where the prefix is the library
        # kind (pt/rt/kw), NOT the directory name -- deriving it from the
        # directory matched nothing and harvested 0 names without an error.
        prefix = {"pilot": "pt", "robot": "rt", "keyword": "kw"}.get(kind, kind)
        if not prefix:
            raise SystemExit("a batch directory needs the kind to pick a prefix")
        return trdata.assemble(path, prefix, amb)[1]
    if path.endswith(".json"):
        return trdata.names(path)
    base = os.path.basename(path)
    if base.startswith("library_") and base.endswith(".py"):
        d = os.path.join(os.path.dirname(os.path.abspath(path)), "library")
        return trdata.assemble(d, base[len("library_"):-3], amb)[1]
    raise SystemExit("%s: expected a .json translation file or a batch directory" % path)


def main(argv):
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    gpath, mpath, kind = argv[1], argv[2], argv[3]
    g = json.load(open(gpath, encoding="utf-8"))
    names = load_names(mpath, gpath, kind)
    idx = {(t["kind"], t["jp"]): t for t in g["terms"]}
    added = kept = skipped = 0
    for jp, en in names.items():
        for k in (kind, "series"):
            t = idx.get((k, jp))
            if t is None:
                continue
            if t["en"] and t.get("status") in ("official", "ambiguous"):
                kept += 1          # already settled; the agent does not win
            elif t["en"] and t["en"] != en:
                kept += 1
            else:
                t["en"] = en
                t["status"] = t.get("status") or "proposed"
                if t["status"] == "todo":
                    t["status"] = "proposed"
                t["src"] = "subagent batch"
                added += 1
            break
        else:
            skipped += 1
    json.dump(g, open(gpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("%d names: %d added, %d already settled, %d not in the seed"
          % (len(names), added, kept, skipped))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
