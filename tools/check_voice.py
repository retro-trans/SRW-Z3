"""Check translated voice lines before they ever reach the game file.

    python tools/check_voice.py work/voice/answer/017.json
    python tools/check_voice.py translation/voice_*.json

Answers a translator can run without a build: the atlas is not needed to
know that a line is over budget, uses a character the font cannot draw, or
answers an entry that is not a distinct string of that section.

Length is in CELLS, not characters. Every letter costs one cell (two
bytes); the literal backslash-n line break costs one cell too, though it is
two characters. That is why `cost()` is not `len()`.

Since the block rebuild (tools/srvc_blocks.py, 2026-09-06) a line may be
any length: the per-entry `budget` in source/voice is the size of the
ORIGINAL byte slot and is informational only. What still limits a line is
the screen -- DISPLAY_CELLS is the working cap, checked as a note, not a
failure, until the true width is measured in-game.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
BRK = chr(92) + "n"
# Exactly the cells the atlas allocates for Latin text (work/out/pairs.json).
# A character outside this set has no cell, so the build fails on it -- catch
# it here, where the fix is cheap.
OK = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
         " .,!?:;'-()/&%+=[]")
DISPLAY_CELLS = 36
JP = re.compile(r"[　-ヿ一-鿿！-｠]")


def source(sec):
    p = os.path.join(ROOT, "source", "voice", "%03d.json" % sec)
    return json.load(open(p, encoding="utf-8"))


def cost(en):
    """Cells this English occupies in its slot."""
    return len(en) - en.count(BRK)


# Two barks are "the same line" if they differ only in how long the shout is
# held or how it is punctuated -- 「ハァァ！」 and 「ハァ…！」 are one grunt,
# and giving them different English would be noise. Anything else that ships
# the same English is a collapse worth reporting.
STRIP = "「」！？。、…・　 ー～" + "".join("ぁぃぅぇぉっゃゅょァィゥェォッャュョ")


def bark(jp):
    return "".join(c for c in jp if c not in STRIP)


def validate(sec, lines):
    """`lines` = {entry: english}. Returns (problems, notes)."""
    src = {r["i"]: r for r in source(sec)}
    shared = {i for i, r in src.items() if r["shared"]}
    problems, notes = [], []
    for k in sorted(lines, key=int):
        n, en = int(k), lines[k]
        r = src.get(n)
        if r is None:
            problems.append("entry %d is not in section %d" % (n, sec))
            continue
        if n in shared:
            problems.append("entry %d is a repeat of an earlier string -- "
                            "translate the first entry that holds it, not this"
                            % n)
        if cost(en) > DISPLAY_CELLS:
            notes.append("entry %d: %r is %d cells, over the %d-cell display cap"
                         % (n, en, cost(en), DISPLAY_CELLS))
        bad = sorted({c for c in en.replace(BRK, "") if c not in OK})
        if bad:
            problems.append("entry %d: cannot draw %s"
                            % (n, " ".join(repr(c) for c in bad)))
        if JP.search(en):
            problems.append("entry %d: still holds Japanese text" % n)
        if en.startswith("「") or en.endswith("」"):
            problems.append("entry %d: drop the quote brackets, the writer "
                            "adds them" % n)
        if BRK in r["jp"] and BRK not in en:
            notes.append("entry %d: the Japanese breaks the line, the English "
                         "does not" % n)
        if BRK not in r["jp"] and BRK in en:
            notes.append("entry %d: the English adds a line break the Japanese "
                         "does not have" % n)
        if not en.strip():
            problems.append("entry %d is empty -- omit the key instead" % n)
    # Different Japanese lines that ship the same English. The player hears
    # barks back to back, so this reads as a bug -- and it is usually a
    # meaning error, not a nuance: 193 had four lines on "Locked!", two of
    # which actually said "parts secured". It happens when a long glossary
    # name eats the budget and only punctuation is left to vary; the fix is
    # to let one line carry the name and the others carry their meaning.
    same = {}
    for k, en in lines.items():
        same.setdefault(en, []).append(int(k))
    for en, ks in sorted(same.items()):
        jp = {bark(src[n]["jp"]) for n in ks if n in src}
        if len(ks) > 1 and len(jp) > 1:
            problems.append("entries %s all say %r, but their Japanese "
                            "differs -- give each its own line"
                            % (" ".join(str(n) for n in sorted(ks)), en))
    return problems, notes


def coverage(sec, lines):
    src = source(sec)
    todo = [r["i"] for r in src if not r["shared"]
            and not any(m in r["jp"] for m in ("－－－", "無音",
                                               "表示しません"))]
    have = {int(k) for k in lines}
    return len(have & set(todo)), len(todo), sorted(set(todo) - have)


def load(path):
    """(sec, {entry: english}) from either shape: a bare answer keyed by
    entry, or a published translation/voice_*.json doc."""
    doc = json.load(open(path, encoding="utf-8"))
    if "lines" in doc:
        return doc["section"], {k: (v["en"] if isinstance(v, dict) else v)
                                for k, v in doc["lines"].items()}
    base = os.path.basename(path)
    digits = "".join(c for c in base if c.isdigit())
    if not digits:
        raise SystemExit("%s: no section number in the name and no 'section' "
                         "field in the file" % base)
    return int(digits), doc


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__.strip())
        return 2
    bad = 0
    for path in args:
        sec, lines = load(path)
        problems, notes = validate(sec, lines)
        got, want, missing = coverage(sec, lines)
        print("%s -- section %d: %d of %d distinct lines answered"
              % (os.path.basename(path), sec, got, want))
        for n in notes:
            print("  note    %s" % n)
        for p in problems:
            print("  PROBLEM %s" % p)
        if missing:
            print("  missing %d entries: %s%s"
                  % (len(missing), " ".join(str(m) for m in missing[:20]),
                     " ..." if len(missing) > 20 else ""))
        bad += len(problems)
    print("%d problems" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
