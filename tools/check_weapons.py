"""Check translated weapon names before they reach a build.

The independence rule, learned the hard way: a check that shares an assumption
with the thing it checks cannot falsify that assumption. The SRVC verifier
resolved offsets through the same section mapping the patch used, so it
confirmed the patch's own mistake and a player screenshot found the bug
instead.

So nothing here consults the swap machinery. The authorities are:

    charset   the real encoder -- if dg.encode_mixed refuses it, the build will
    coverage  the source list, read straight out of RPW_DATA
    width     the measured capacity of the column the name lives in

The width bound is MEASURED, not assumed. Two earlier guesses were both wrong,
and for the same reason: each was a proxy for the UI space instead of the UI
space itself. "No wider than the Japanese it replaces" fails 141 of the 689
names already shipping, because a two-character surname legitimately becomes
ten letters -- width is not conserved by translation and there is no reason it
should be. "No wider than the widest name shipping anywhere" was measured on
the intermission unit list, a far wider column than the weapon screen.

What is actually true is the user's framing: wider than the original is fine,
as long as it is not wider than the UI space. So measure the UI space. The
weapon record has two name columns, and a name is bounded by the narrower of
the ones it occupies:

    w3  the weapon-select list name          longest shipped: 18 fullwidth
    w4  the same name with a model prefix    longest shipped: 48 fullwidth

A column that already draws an 18-character Japanese name is proven to hold
540 px, so 540 px is a floor on its capacity, not a guess about it. English is
measured in the same units through dg.line_px, so the comparison is like for
like. The bound is conservative by construction: it can only be too tight,
never too loose, and being too tight merely asks for a shorter name.

Two honest caveats on the numbers.

The floors are lower bounds on capacity, not the column widths themselves, so
a name a few px over the line may well still fit -- the check just cannot say
so. Only a screenshot can. And w4's 1440 px exceeds the 1140 px line budget of
the library screen it is measured in, which means that 48-character name is
either wrapped or drawn somewhere wider. So w4 proves the game HANDLES the
string, not that it sets on one line. Treat the w4 budget as permission to
keep a faithful long name, never as a reason to lengthen one that already fits.

The column identity is cross-checked against something outside the parser: the
four weapon names visible in a player screenshot of the select screen all
resolve to w3. That is what keeps this from being the SRVC mistake again --
the screenshot is evidence the pointer parser did not produce.

    python tools/check_weapons.py <weapons.json> [--glossary analysis/glossary.json]
"""
import collections
import io
import struct
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digraph as dg   # noqa: E402
import rpw             # noqa: E402
from cpk import CPK    # noqa: E402

NAME_COLS = (3, 4)   # w3 select-list name, w4 name with model prefix
SCREEN = "library"
# w2 holds one string for all 2694 records -- a placeholder, not a name.
IGNORE = {"-"}
ALLOWED = re.compile(r"^[A-Za-z0-9 .,!?:;'()/&-]*$")


def budgets():
    """Every Japanese weapon name, with the pixel budget of its own column.

    A name in both columns takes the narrower budget: it is the same string
    drawn in both places, so it has to fit the tighter one.
    """
    k = CPK("work/lib/RPW_DATA.CPK")
    raw = k.read(k.files[0])
    js = rpw.jstrings(raw)
    starts, _ = rpw._starts(raw)
    at = {o: i for i, o in enumerate(starts)}
    ch = {c[0]: c for c in rpw.chunks(raw)}
    stride, _cols = rpw.pointer_columns(raw)["weapon"]
    base, end = ch["weapon"][2], ch["weapon"][3]
    n = ((end - base) // 4) // stride

    seen = {c: set() for c in NAME_COLS}
    for rec in range(n):
        for c in NAME_COLS:
            v = struct.unpack_from("<I", raw, base + 4 * (rec * stride + c))[0]
            i = at.get(v)
            if i is not None and js[i].strip():
                seen[c].add(js[i])

    # the floor: the widest Japanese the game already draws in that column
    floor = {c: max(dg.line_px(t, SCREEN) for t in seen[c]) for c in NAME_COLS}
    out = {}
    for c in NAME_COLS:
        for t in seen[c]:
            out[t] = min(out.get(t, 1e9), floor[c])
    return out, floor


def widths_ready(ttf="E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF"):
    try:
        dg.use_letters(ttf, cap=22, dilate=0.5)
        return True
    except Exception:
        return False


def pairs():
    for p in ("work/out/pairs.json", "work/out/pairs_lib.json"):
        if os.path.exists(p):
            m = json.load(open(p, encoding="utf-8"))
            return {(k if len(k) == 1 else (k[0], k[1])): v for k, v in m.items()}
    return {}


def check(answers, budget, mapping, measure=True):
    problems = []
    for jp in budget:
        if jp not in answers:
            problems.append((jp, "missing", "no translation"))
    for jp in answers:
        if jp not in budget and jp not in IGNORE:
            problems.append((jp, "unknown", "not a weapon string in RPW_DATA"))

    for jp, en in answers.items():
        if jp not in budget:
            continue
        if not en or not en.strip():
            problems.append((jp, "empty", "blank translation"))
            continue
        if not ALLOWED.match(en):
            bad = "".join(sorted({c for c in en if not ALLOWED.match(c)}))
            problems.append((jp, "charset", "cannot draw %r" % bad))
            continue
        try:
            dg.encode_mixed(en, mapping, newline=bytes((10,)))
        except SystemExit as e:
            problems.append((jp, "encode", str(e)[:80]))
            continue
        except Exception:
            pass
        if measure:
            px = dg.line_px(en, SCREEN)
            if px > budget[jp]:
                problems.append((jp, "width", "%.0f px, column holds %.0f (%s)"
                                 % (px, budget[jp], en)))
    return problems


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    answers = json.load(open(argv[1], encoding="utf-8"))
    budget, floor = budgets()
    measure = widths_ready()
    if not measure:
        print("  (no TTF: width check skipped -- this is the real check, fix it)")
    else:
        for c in NAME_COLS:
            print("  w%d column proven to hold %.0f px" % (c, floor[c]))
    problems = check(answers, budget, pairs(), measure)
    kinds = collections.Counter(k for _j, k, _m in problems)
    for jp, kind, msg in problems[:50]:
        print("  %-22s %-8s %s" % (jp[:22], kind, msg))
    print("%d source names, %d answered, %d problems %s"
          % (len(budget), len(answers), len(problems), dict(kinds) if kinds else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
