"""Stamp every stage translation record with its identity from the Lua.

Turns a bare list of English strings into records that carry
`(event, n, pid, sha, jp, en)`, so a translation binds to a specific line
rather than to "the Nth block", and a reorder or an edit to the wrong line is
a hard error instead of a silent speaker shift.

Idempotent: re-stamping a stamped file just refreshes `jp`/`sha` from the
Lua and asserts the identities still line up.

    python tools/stamp_ids.py <member.lua> <translation.json>
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import luarec  # noqa: E402


def stamp(lua_text, lines):
    recs = luarec.records(lua_text)
    if len(recs) != len(lines):
        raise SystemExit("lua has %d records, translation has %d"
                         % (len(recs), len(lines)))
    out = []
    for r, item in zip(recs, lines):
        en = item["en"] if isinstance(item, dict) else item
        if isinstance(item, dict) and "event" in item:
            # already stamped: the identity must still match the Lua
            if (item["event"], item["n"]) != (r["event"], r["n"]):
                raise SystemExit("record %s#%s in the translation is %s#%s in the lua"
                                 % (item["event"], item["n"], r["event"], r["n"]))
        out.append({"event": r["event"], "n": r["n"], "pid": r["pid"],
                    "sha": r["sha"], "jp": r["jp"].replace("\r\n", "\n"), "en": en})
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    lua, jpath = argv[1], argv[2]
    text = open(lua, "rb").read().decode("cp932")
    d = json.load(open(jpath, encoding="utf-8"))
    d["LINES"] = stamp(text, d["LINES"])
    json.dump(d, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n = len(d["LINES"])
    print("%s: %d records stamped with (event, n, pid, sha, jp)" % (os.path.basename(jpath), n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
