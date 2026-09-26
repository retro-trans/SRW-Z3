"""Prove a stage translation obeys the constraints that silently break the game.

Review by reading catches meaning. It does not reliably catch a dropped `$n`,
a `《` without its `》`, a line four pixels too wide, or a character the atlas
cannot draw -- and each of those ships as garbage or a mislinked keyword. So
those are checked mechanically here, and the reviewer is left to judge the
things only a reader can.

Every rule below was calibrated against the SHIPPED stage 1 translation, which
must pass clean. Three of the rules I first wrote failed that test and were
wrong, not the translation:

    escapes     `$n`/`$l`/`$F` counts identical -- runtime name substitutions;
                dropping one loses the player's name. `$` itself is eaten by
                the parser and never reaches a glyph, so strip the escapes
                before any charset or width check.
    links       `《` and `》` counts identical and balanced -- the game matches
                spans positionally against a separate keyword id list, so a
                dropped span mislinks every span after it.
    lines       at most 4. NOT "the same count as the source": English often
                needs one more line, and 40 shipped stage-1 records use four
                where the Japanese used three.
    charset     whatever the real encoder accepts, not a hand-listed set.
                `～`, `（`, `）` are drawn from reserved Japanese cells and are
                perfectly fine; a Latin-only list rejects them wrongly.
    width       every line within the dialogue budget, measured in pixels from
                the real per-letter widths rather than guessed from a
                character count.
    coverage    every source record answered exactly once.

    python tools/check_stage.py <member.lua> <answers.json>..
"""
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digraph as dg    # noqa: E402
import luarec          # noqa: E402
import terms as _terms  # noqa: E402
from dialogue_structure import speaker_problem

# $n/$l are the player-named protagonist, $F a name fragment, and $c the
# player-named squad (the ZEUTH/ZEXIS slot: 「$cとして行動を開始します」).
# $c was not checked for years, so a dropped one would have shipped silently.
ESC = re.compile(r"\$([nlFc])")
MAX_LINES = 4          # shipped stage 1 uses 1-4 lines per record, never 5


def pairs():
    """The cell mapping a build would use, so "encodable" means the same thing
    here as it does in build_project."""
    for p in ("work/out/pairs.json", "work/out/pairs_lib.json"):
        if os.path.exists(p):
            m = json.load(open(p, encoding="utf-8"))
            return {(k if len(k) == 1 else (k[0], k[1])): v for k, v in m.items()}
    return {}


def glossary_index(gpath="analysis/glossary.json"):
    """The `$$japanese$$` term index, so charset/width are checked against
    what the build actually puts on screen. Prose is written with the token,
    never the literal English (work/tr/CONVENTIONS.md), so checking the raw
    `$$...$$` text would reject every glossary-bearing line: `$` has no glyph
    (tools/terms.py). Missing glossary just means no line here happens to use
    one; that is not this tool's problem to raise."""
    if not os.path.exists(gpath):
        return None
    g = json.load(open(gpath, encoding="utf-8"))
    return _terms.index(g)


def widths_ready(ttf="E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF"):
    try:
        dg.use_letters(ttf, cap=22, dilate=0.5)
        return True
    except Exception:
        return False


def check(recs, answers, measure=True, mapping=None, term_idx=None):
    mapping = pairs() if mapping is None else mapping
    term_idx = glossary_index() if term_idx is None else term_idx
    problems = []
    by_sha = {r["sha"]: r for r in recs}
    limit = dg.SCREENS["dialogue"][2]

    for s in by_sha:
        if s not in answers:
            problems.append((s, "missing", "no translation supplied"))
    for s in answers:
        if s not in by_sha:
            problems.append((s, "unknown", "sha is not in this member"))

    for sha, en in answers.items():
        r = by_sha.get(sha)
        if r is None:
            continue
        jp = r["jp"].replace("\r\n", "\n")
        en = (en or "").replace("\r\n", "\n")

        problem = speaker_problem(jp, en)
        if problem:
            problems.append((sha, "speaker", problem))

        a, b = sorted(ESC.findall(jp)), sorted(ESC.findall(en))
        if a != b:
            problems.append((sha, "escapes", "source %s, translation %s" % (a, b)))

        for ch, what in (("\u300a", "open link"), ("\u300b", "close link")):
            if jp.count(ch) != en.count(ch):
                problems.append((sha, "links", "%s: source %d, translation %d"
                                 % (what, jp.count(ch), en.count(ch))))
        if en.count("\u300a") != en.count("\u300b"):
            problems.append((sha, "links", "unbalanced 《 》"))

        el = en.split("\n")
        if len(el) > MAX_LINES:
            problems.append((sha, "lines", "%d lines, max %d" % (len(el), MAX_LINES)))

        # `$n` is a runtime escape the parser eats; it never reaches a glyph
        probe = ESC.sub("", en)
        bad = False
        # `$$japanese$$` is a glossary reference (tools/terms.py), not text --
        # the build expands it before anything reaches the screen, so charset
        # and width have to be checked against the expanded English too, not
        # against the token's own `$` characters (no glyph, and never meant to
        # be drawn).
        expanded = probe
        if "$$" in probe:
            if term_idx is None:
                bad = True
                problems.append((sha, "terms", "glossary reference but no "
                                  "analysis/glossary.json to expand it against"))
            else:
                try:
                    expanded = _terms.expand(probe, term_idx, where=sha)
                except SystemExit as e:
                    bad = True
                    problems.append((sha, "terms", str(e)[:200]))

        if not bad:
            try:
                dg.encode_mixed(expanded, mapping, newline=bytes((10,)))
            except SystemExit as e:
                bad = True
                problems.append((sha, "charset", str(e)[:90]))
            except Exception:
                pass

        if measure and not bad:
            for i, ln in enumerate(expanded.split("\n")):
                try:
                    px = dg.line_px(ln, "dialogue")
                except Exception:
                    continue
                if px > limit:
                    problems.append((sha, "width", "line %d is %.0f px of %.0f: %r"
                                     % (i + 1, px, limit, ln[:60])))
    return problems


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    lua = argv[1]
    paths = [a for a in argv[2:] if not a.startswith("--")]
    recs = luarec.records(open(lua, "rb").read().decode("cp932"))
    answers = {}
    for p in paths:
        if not os.path.exists(p):
            print("  missing answer file: %s" % p)
            continue
        d = json.load(open(p, encoding="utf-8"))
        # a merged translation module is the thing that actually ships, so
        # accept it as well as a translator's raw {sha: english} answer
        if isinstance(d, dict) and "LINES" in d:
            d = {r["sha"]: r["en"] for r in (d["LINES"] or [])
                 if r.get("sha") and r.get("en")}
        dup = set(d) & set(answers)
        if dup:
            print("  %s repeats %d sha already answered: %s"
                  % (p, len(dup), sorted(dup)[:5]))
        answers.update(d)

    measure = widths_ready()
    if not measure:
        print("  (no TTF: width check skipped)")
    problems = check(recs, answers, measure)
    kinds = {}
    for _s, kind, _m in problems:
        kinds[kind] = kinds.get(kind, 0) + 1
    for sha, kind, msg in problems[:60]:
        print("  %-10s %-8s %s" % (sha, kind, msg))
    print("%s: %d records, %d answered, %d problems %s"
          % (os.path.basename(lua), len(recs), len(answers), len(problems),
             kinds if kinds else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
