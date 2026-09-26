"""Verify unverified glossary terms against akurasu's Z3 lists, mechanically.

The point is to make "verified" mean something. A term is only promoted when
its English matches an entry on akurasu's Z3 Mech List or Pilot Database --
the same source the hand-verified terms came from -- so the green tier on the
glossary page keeps its meaning.

Matching normalises case, spacing and the game's fullwidth spaces, because
`M6 Bushnell` and `Ｍ６　ブッシュネル` are the same unit. It is deliberately
exact otherwise: a near-miss is reported, not silently accepted, because a
near-miss is exactly where a wrong name hides (Doven Wolf vs Dreissen).

    python tools/verify_akurasu.py <glossary.json> <sources-dir> [--apply]
"""
import io
import json
import os
import re
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = re.sub(r"[\s\u3000]+", " ", s).strip()
    s = re.sub(r"[.\-'’]", "", s)
    return s


def load_list(path):
    out = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            out[norm(line)] = line
    return out


def unverified(t):
    if t.get("src", "").startswith("akurasu"):
        return False
    if t["status"] == "official":
        return False
    return True


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    gpath, srcdir = argv[1], argv[2]
    apply = "--apply" in argv
    g = json.load(open(gpath, encoding="utf-8"))
    mechs = load_list(os.path.join(srcdir, "akurasu_z3_mechs.txt"))
    pilots = load_list(os.path.join(srcdir, "akurasu_z3_pilots.txt"))
    # a unit "(variant)" on akurasu still verifies the base name
    mech_base = {norm(re.sub(r"\s*[\(\[].*$", "", v)): v for v in mechs.values()}

    hit, miss, near = [], [], []
    for t in g["terms"]:
        if not unverified(t) or not t["en"]:
            continue
        key = norm(t["en"])
        src = None
        if t["kind"] == "robot":
            if key in mechs or key in mech_base:
                src = "akurasu:Super_Robot_Wars/Z3/Mech_List"
        elif t["kind"] == "pilot":
            if key in pilots:
                src = "akurasu:Super_Robot_Wars/Z3/Pilot_Database"
            elif t.get("field") == "CHNN" and key and " " not in key:
                # A short name is the game's own abbreviation of a full name.
                # It verifies when it is a whole token of a full name akurasu
                # lists -- `Amata` from `Amata Sora`. Whole-token, so `Rei`
                # cannot be claimed by `Reina`.
                if any(key in k.split(" ") for k in pilots):
                    src = "akurasu:Super_Robot_Wars/Z3/Pilot_Database (short name)"
        if src:
            hit.append(t)
            if apply:
                t["src"] = src
                if t["status"] != "ambiguous":
                    t["status"] = "official"
        else:
            miss.append(t)
            # report near-misses: same first token in the right list
            pool = mech_base if t["kind"] == "robot" else pilots
            first = key.split(" ")[0] if key else ""
            cand = [v for k, v in pool.items() if first and k.split(" ")[0] == first and k != key]
            if cand:
                near.append((t, cand[:3]))

    print("checked %d unverified terms" % (len(hit) + len(miss)))
    print("  verified on akurasu : %d" % len(hit))
    print("  no match            : %d" % len(miss))
    print("  near-miss (review)  : %d" % len(near))
    if near:
        print()
        print("near-misses -- same first word, different spelling:")
        for t, c in near:
            print("  %-7s %-26s glossary=%r  akurasu=%s" % (t["kind"], t["jp"][:26], t["en"], c))
    if apply:
        json.dump(g, open(gpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\napplied.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
