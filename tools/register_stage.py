"""Register a translated stage in every table a build and a deploy read.

    python tools/register_stage.py STG0031A [STG0031B ..]

Four files carry one line (or one block) per shipped stage and all four have
to agree, which is exactly the kind of four-place edit that gets done in three
places at 2am:

    platforms/ps3/manifest.py  what the build patches, member by member
    tools/deploy.py            where the built SDAT goes on the disc
    tools/extract.py           where the pristine one is read back from
    tools/apply_xdelta.py      where a distributed patch applies it

A stage is registered only for the members whose translation file holds
English, and re-running is a no-op. Nothing is written until every file has
been read and edited in memory, so a failure leaves all four untouched.

Line endings are never normalised. More than one person edits these files and
at least one of them is mixed CRLF/LF; rewriting every ending would bury a
one-line addition inside a whole-file diff. An inserted line copies the
ending of the line it follows.
"""
import io
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLES = ["tools/deploy.py", "tools/extract.py", "tools/apply_xdelta.py"]
MANIFEST = "platforms/ps3/manifest.py"
TABLE_ANCHOR = '    "STG0030.SDAT": "DATA/STAGE",'
MANIFEST_MARKER = " # The between-stage intermission scenes"


def luadir(name):
    n = name[3:].lstrip("0") or "0"
    return "work/lua" + n.lower()


def transpath(name, mid):
    return "translation/stage%s_%02d.json" % (name[3:].lower(), mid)


def members(name):
    out = []
    for mid in range(0, 10):
        p = os.path.join(ROOT, transpath(name, mid))
        if not os.path.isfile(p):
            continue
        doc = json.load(open(p, encoding="utf-8"))
        if any(r.get("en") for r in (doc.get("LINES") or [])):
            out.append(mid)
    return out


def insert_after(text, anchor, addition):
    """`addition` on its own line after `anchor`, in the anchor's own ending."""
    end = text.index(anchor) + len(anchor)
    nl = "\r\n" if text[end:end + 2] == "\r\n" else "\n"
    return text[:end] + nl + addition + text[end:]


def insert_before(text, marker, addition):
    i = text.index(marker)
    nl = "\r\n" if "\r\n" in text[:i] else "\n"
    return text[:i] + addition + nl + text[i:]


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    names = [a.upper() for a in argv[1:] if not a.startswith("-")]
    if not names:
        print(__doc__.strip())
        return 2

    edits = {p: open(os.path.join(ROOT, p), "rb").read().decode("utf-8")
             for p in TABLES + [MANIFEST]}
    added = []

    for name in names:
        mids = members(name)
        if not mids:
            print("%s: no translation file with English yet -- skipped" % name)
            continue
        sdat = name + ".SDAT"

        for p in TABLES:
            if '"%s"' % sdat in edits[p]:
                continue
            if TABLE_ANCHOR not in edits[p]:
                print("%s: anchor not found in %s" % (name, p))
                return 1
            edits[p] = insert_after(edits[p], TABLE_ANCHOR,
                                    '    "%s": "DATA/STAGE",' % sdat)

        if '"sdat": "%s"' % sdat not in edits[MANIFEST]:
            if MANIFEST_MARKER not in edits[MANIFEST]:
                print("%s: intermission marker not found in the manifest" % name)
                return 1
            nl = "\r\n" if "\r\n" in edits[MANIFEST] else "\n"
            block = [' {"cpk": "work/stage_dec/%s.cpk", "sdat": "%s",' % (name, sdat),
                     '  "members": [']
            for mid in mids:
                block.append('    {"id": %d, "lua": "%s/%s_%05d.lua",'
                             % (mid, luadir(name), name, mid))
                block.append('     "trans": "%s"},' % transpath(name, mid))
            block.append('  ]},')
            edits[MANIFEST] = insert_before(edits[MANIFEST], MANIFEST_MARKER,
                                            nl.join(block))
        added.append((name, mids))

    for p, text in edits.items():
        open(os.path.join(ROOT, p), "wb").write(text.encode("utf-8"))
    for name, mids in added:
        print("registered %s  members %s" % (name, ", ".join(str(m) for m in mids)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
