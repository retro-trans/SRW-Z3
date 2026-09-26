"""Read dialogue records out of a scenario Lua with their real identity.

A record is an anonymous table entry -- the game gives no per-line id. But it
does give structure, and that is what a line's identity is built from:

    event     the named table it sits in       t_001
    ordinal   its position within that event   2
    pid       the speaker's pilot id           pid_KEI
    jp        the source text

`(event, ordinal)` is stable across builds and survives translation. Text is
NOT a key: STG0001B_00003 has eight duplicate records, so matching by content
would be ambiguous even in the shipped Japanese.

Every record found here is in the same order as patch_lua's BLOCK walk -- the
two are cross-checked in tests, because a disagreement would mean a
translation binds to the wrong line.

    python tools/luarec.py <member.lua>
"""
import hashlib
import io
import re
import sys

# `--[[ ... ]]` is a block comment, not a string; same rule as patch_lua.BLOCK
BLOCK = re.compile(r"(?<!--)\[\[(.*?)\]\]", re.S)
EVENT = re.compile(r"^(t_\d+)\s*=\s*\{(.*?)^\};", re.M | re.S)
# the record header immediately before a [[ ... ]]: {WPos_B, 3, FDMode_Normal, pid_SIN,
HEAD = re.compile(r"\{\s*(\w+)\s*,\s*(\d+)\s*,\s*(\w+)\s*,\s*(pid_\w+)\s*,\s*$", re.M)


def digest(jp):
    """Short stable fingerprint of the source text, for change detection."""
    return hashlib.sha1(jp.replace("\r\n", "\n").encode("utf-8")).hexdigest()[:10]


def records(text):
    """All dialogue records in file order, each with its identity."""
    out = []
    # map every block's start offset to (event, ordinal)
    ident = {}
    for ev in EVENT.finditer(text):
        name, body, base = ev.group(1), ev.group(2), ev.start(2)
        for n, m in enumerate(BLOCK.finditer(body)):
            ident[base + m.start()] = (name, n)
    for m in BLOCK.finditer(text):
        jp = m.group(1)
        event, ordinal = ident.get(m.start(), (None, None))
        # speaker id from the header line just before this block
        head = HEAD.search(text, max(0, m.start() - 120), m.start())
        pid = head.group(4) if head else None
        out.append({"event": event, "n": ordinal, "pid": pid,
                    "jp": jp, "sha": digest(jp)})
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    text = open(argv[1], "rb").read().decode("cp932")
    recs = records(text)
    for i, r in enumerate(recs):
        first = r["jp"].split("\r\n")[0]
        print("%3d  %-6s #%-3s %-12s %s  %s" % (i, r["event"], r["n"], r["pid"], r["sha"], first[:24]))
    print("%d records, %d without an event, %d without a pid"
          % (len(recs), sum(1 for r in recs if r["event"] is None),
             sum(1 for r in recs if r["pid"] is None)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
