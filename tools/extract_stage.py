"""Walk one decrypted STAGE container down to its Lua source.

    STG*.SDAT --[unsdat]--> CPK --[cpk.py]--> CRILAYLA --> Lua (cp932)

Takes an already-decrypted container (run tools/unsdat.py first) and writes
its members out, naming each by the .lua path the file declares in its own
header comment where it has one.

    python tools/extract_stage.py <decrypted.sdat> <outdir>
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

NAME_RE = re.compile(rb'"([^"\r\n]+\.lua)"')


def declared_name(blob):
    """Some Lua members open with a comment naming their source path.
    Most do not, so this is a bonus, not the classifier."""
    m = NAME_RE.search(blob[:4096])
    if not m:
        return None
    return os.path.basename(m.group(1).decode("cp932", "replace"))


def is_lua(blob):
    """Lua members are CRLF text in cp932 with no NUL bytes. The binary
    members are NUL-heavy tables, so the two never get confused."""
    head = blob[:4096]
    if b"\0" in head:
        return False
    try:
        head.decode("cp932")
    except UnicodeDecodeError as e:
        # a fixed-size slice can cut a two-byte cp932 character in half;
        # only an error away from the very end means it is not text
        if e.start < len(head) - 2:
            return False
    return b"\r\n" in head and (b"--" in head or b"=" in head)


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    src, outdir = argv[1], argv[2]
    os.makedirs(outdir, exist_ok=True)

    cpk = CPK(src)
    stem = os.path.splitext(os.path.basename(src))[0]
    for e in cpk.files:
        blob = cpk.read(e)
        lua = is_lua(blob)
        name = declared_name(blob) or (
            "%s_%05d.%s" % (stem, e["id"], "lua" if lua else "bin"))
        dest = os.path.join(outdir, name)
        with open(dest, "wb") as fh:
            fh.write(blob)
        print("  %-34s %8d B  %s" % (name, len(blob), "lua" if lua else "bin"))
    print("%d members -> %s" % (len(cpk.files), outdir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
