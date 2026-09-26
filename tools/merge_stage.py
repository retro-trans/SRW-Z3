"""Merge translator answer files into a stamped stage translation.

Answers come back keyed by `sha`, which is a hash of the SOURCE TEXT, not of a
position -- so identical lines share one. That is usually what you want (「………」
is translated once), but it means two translators working on different slices
of the same member can both answer the same sha. Four do, in stage 2. A silent
`dict.update` would let whichever file loaded last win, so disagreements are
reported instead of resolved.

Output is the stamped shape the build reads: one record per Lua record, in Lua
order, carrying `(event, n, pid, sha, jp, en)`. Duplicate records share their
translation, which is why the count of records exceeds the count of answers.

    python tools/merge_stage.py <member.lua> <out.json> <answers.json>..
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import luarec   # noqa: E402


def merge(paths):
    """(answers, conflicts). A conflict is one sha answered two ways."""
    answers, source, conflicts = {}, {}, []
    for p in paths:
        d = json.load(open(p, encoding="utf-8"))
        for sha, en in d.items():
            if sha in answers and answers[sha] != en:
                conflicts.append((sha, source[sha], answers[sha], p, en))
                continue                      # first answer stands
            answers.setdefault(sha, en)
            source.setdefault(sha, p)
    return answers, conflicts


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    lua, out = argv[1], argv[2]
    answers, conflicts = merge(argv[3:])
    recs = luarec.records(open(lua, "rb").read().decode("cp932"))

    lines = []
    for r in recs:
        lines.append({"event": r["event"], "n": r["n"], "pid": r["pid"],
                      "sha": r["sha"], "jp": r["jp"].replace("\r\n", "\n"),
                      "en": answers.get(r["sha"], "")})
    blank = sum(1 for x in lines if not x["en"])
    json.dump({"LINES": lines}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    print("%s: %d records from %d answers -> %s%s"
          % (os.path.basename(lua), len(lines), len(answers), out,
             "" if not blank else "  (%d records left blank)" % blank))
    for sha, p1, a, p2, b in conflicts:
        print("  CONFLICT %s" % sha)
        print("     %-28s %r" % (os.path.basename(p1), a[:60]))
        print("     %-28s %r" % (os.path.basename(p2), b[:60]))
    if conflicts:
        print("%d sha answered two ways; the first file's answer was kept"
              % len(conflicts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
