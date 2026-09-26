"""Which stage scripts are translated, and what is left.

Derived, never hand-maintained: the disc's own DATA/STAGE listing is the
denominator, `platforms/ps3/manifest.py` says what a build registers, and the
translation files say how many records are actually answered. A stage counts
as done only when every registered member has an English record for every
Japanese record.

    python tools/stage_status.py            # summary plus the next stages
    python tools/stage_status.py --all      # every script, one line each
    python tools/stage_status.py --next 3   # just the next N to do
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DISC = "E:/SRWZ3/PS3_GAME/USRDIR/DATA/STAGE"


def scripts():
    """Every stage script on the disc, in play order."""
    if not os.path.isdir(DISC):
        return []
    out = [f[:-5] for f in sorted(os.listdir(DISC)) if f.endswith(".SDAT")]
    return [s for s in out if s.startswith("STG")]


def kind(name):
    n = name[3:]
    num = int(re.match(r"(\d+)", n).group(1))
    if num <= 100:
        return "story"
    if 200 <= num < 300:
        return "intermission"
    return "other"


def registered():
    """{sdat: [(member id, translation path)]} from the build manifest."""
    src = open(os.path.join(ROOT, "platforms", "ps3", "manifest.py"),
               encoding="utf-8").read()
    out = {}
    for blk in re.finditer(r'"sdat":\s*"(STG[^"]+)\.SDAT"(.*?)\n\s*\]\}',
                           src, re.S):
        out[blk.group(1)] = re.findall(
            r'"id":\s*(\d+),\s*"lua":[^,]+,\s*\n?\s*"trans":\s*"([^"]+)"',
            blk.group(2))
    return out


def counts(path):
    """(records, answered) for one translation file."""
    p = os.path.join(ROOT, path)
    if not os.path.isfile(p):
        return (0, 0)
    doc = json.load(open(p, encoding="utf-8"))
    lines = doc.get("LINES") or []
    return (len(lines), sum(1 for r in lines if r.get("en")))


def rows():
    reg = registered()
    for s in scripts():
        members = reg.get(s, [])
        tot = ans = 0
        for _id, path in members:
            t, a = counts(path)
            tot += t
            ans += a
        if not members:
            state = "todo"
        elif ans == 0:
            state = "registered, empty"
        elif ans < tot:
            state = "partial"
        else:
            state = "done"
        yield s, kind(s), state, tot, ans


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    data = list(rows())
    if not data:
        print("no disc listing at %s -- is the game extracted?" % DISC)
        return 2
    show_all = "--all" in argv
    n_next = 8
    if "--next" in argv:
        n_next = int(argv[argv.index("--next") + 1])

    for k in ("story", "intermission", "other"):
        grp = [r for r in data if r[1] == k]
        done = [r for r in grp if r[2] == "done"]
        recs = sum(r[4] for r in grp)
        print("%-13s %3d scripts, %3d done, %3d to go   (%d records answered)"
              % (k, len(grp), len(done), len(grp) - len(done), recs))

    todo = [r for r in data if r[2] != "done" and r[1] == "story"]
    print("\nnext story scripts: %s"
          % " ".join(r[0] for r in todo[:n_next]) if todo else "\nstory: all done")
    other = [r for r in data if r[2] != "done" and r[1] == "other"]
    if other:
        print("also untranslated: %s" % " ".join(r[0] for r in other))

    if show_all:
        print("")
        for s, k, state, tot, ans in data:
            print("  %-12s %-12s %-18s %5d/%-5d" % (s, k, state, ans, tot))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
