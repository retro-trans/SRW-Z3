"""Write translated battle voice lines into SRVC.BIN, in place, any section.

    python tools/voice_section.py <doc.json>... [--out work/out/SRVC.BIN]
    python tools/voice_section.py translation/voice_*.json --out work/out/SRVC.BIN

Was Genion-only (POOL/INDEX/COUNT were module constants). The geometry now
comes per section from work/voice/sections.json and is re-proven before every
write -- see tools/voice_lib.py for why in-place is the only legal shape.

This script stays useful for one-section iteration, but the build applies
every translation/voice_*.json itself (tools/build_project.py): a doc encoded
against a stale atlas mapping renders as garbage, and forgetting to re-run
this by hand once cost four days of a silently regressed patch.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digraph as dg     # noqa: E402
import voice_lib as V    # noqa: E402

SRC = "work/srvc/SRVC.BIN"    # the pristine ISO extract (tools/isoread.py)
LATIN = "E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF"


def load_mapping(path="work/out/pairs.json"):
    m = json.load(open(path, encoding="utf-8"))
    return {(k if len(k) == 1 else (k[0], k[1])): v for k, v in m.items()}


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    flags = {"--out", "--src"}
    args, skip = [], False
    for a in argv[1:]:
        if skip:
            skip = False
        elif a in flags:
            skip = True
        elif not a.startswith("--"):
            args.append(a)
    if not args:
        print(__doc__.strip())
        return 2
    out = argv[argv.index("--out") + 1] if "--out" in argv else "work/out/SRVC.BIN"
    src = argv[argv.index("--src") + 1] if "--src" in argv else SRC
    docs = [json.load(open(p, encoding="utf-8")) for p in args]
    dg.use_letters(LATIN, cap=22, dilate=0.5)
    mapping = load_mapping()
    old = open(src, "rb").read()
    new, report = V.apply_docs(old, docs, mapping)
    probs = V.verify(old, new, report)
    for rep, path in zip(report, args):
        print("section %s (%s) from %s" % (rep["sec"], rep["unit"] or "?",
                                           os.path.basename(path)))
        for n, off, room, used in rep["slots"]:
            print("  entry %3d @%#08x  %d of %d bytes used" % (n, off, used, room))
        print("  %d lines written in place" % rep["written"])
    print("%d lines in %d sections, file size unchanged (%d B)"
          % (sum(r["written"] for r in report), len(report), len(new)))
    for p in probs:
        print("  PROBLEM %s" % p)
    if probs:
        return 1
    open(out, "wb").write(new)
    print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
