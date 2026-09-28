"""Glossary references in translated prose: `$$日本語$$`.

Names were already dynamic -- the zukan, RPW_DATA and the EBOOT all look a name
up by its Japanese key at build time, so changing `analysis/glossary.json`
changes every one of them. Prose was not: a term inside a sentence was written
out literally, so renaming one meant editing every line that mentioned it
(`Sphere` alone appeared 83 times across 11 files).

So prose refers to a term by its JAPANESE, and the build expands it:

    "The $$スフィア$$ reacts to his will."  ->  "The Sphere reacts to his will."
    "three $$スフィア$$s"                  ->  "three Spheres"

Suffixes stay OUTSIDE the token so plurals and possessives need no syntax.
`|lc` lower-cases the first letter for mid-sentence use; nothing else is
supported, because anything cleverer hides the real text from the person
writing the line.
Never use `|lc` for the lore terms Sphere (スフィア) or Dimensional Power
(次元力); their capitalization is required even in the middle of a sentence.

The key is the Japanese and NOT a slug of the English, because the English is
the thing that changes -- an English-derived id starts lying the moment a term
is renamed. It is also the key the rest of the pipeline already uses, so a term
has exactly one name rather than two that can drift apart.

`$$` is safe as a delimiter. The game's own text escapes are `$n` and `$l` (the
player-named protagonist), both a SINGLE dollar, and no Japanese source string
anywhere contains `$$`. `$` is not in the drawable glyph set either, so it
never reaches the screen on its own.

## Discriminators

1,125 of 1,141 terms are unique by their Japanese and need nothing. Which
discriminator the rest need falls out of the collision:

    $$アクエリオンＥＶＯＬ#series$$   12 Japanese strings name two KINDS of thing
                                  (a series and its lead robot, a keyword and
                                  a pilot); the kind settles it
    $$レイ#333$$                   4 Japanese short names belong to two
                                  different PEOPLE of the same kind -- レイ is
                                  both Ray Lovelock and Rei Ayanami; the zukan
                                  entry settles it

A numeric discriminator is a zukan entry id and an alphabetic one is a kind, so
the two can never be confused. A bare reference to an ambiguous term is a hard
error: picking one silently is exactly how Ray Lovelock ended up called Rei.

    python tools/terms.py check <glossary.json> <dir>..   # lint every reference
    python tools/terms.py list  <glossary.json> [substr]  # find the right token
"""
import io
import json
import os
import re
import sys

# body = anything but the delimiters; discriminator = a kind name or an entry id
TOKEN = re.compile(r"\$\$([^$|#\n]{1,64}?)(?:#([A-Za-z0-9_-]{1,16}))?(\|lc)?\$\$")
KIND_ORDER = ["keyword", "pilot", "robot", "series"]


def index(g):
    """{japanese: [terms]}, in a stable order."""
    idx = {}
    for t in sorted(g["terms"], key=lambda t: (KIND_ORDER.index(t["kind"]),
                                               t.get("zukan_id") if t.get("zukan_id") is not None else -1)):
        idx.setdefault(t["jp"], []).append(t)
    return idx


def token_for(t, idx):
    """The reference that addresses exactly this term and nothing else."""
    same = idx.get(t["jp"], [])
    if len(same) < 2:
        return "$$%s$$" % t["jp"]
    if sum(1 for x in same if x["kind"] == t["kind"]) < 2:
        return "$$%s#%s$$" % (t["jp"], t["kind"])
    if t.get("zukan_id") is None:
        raise SystemExit("%r (%s) shares its Japanese with another term of the "
                         "same kind and has no zukan_id to tell them apart"
                         % (t["jp"], t["en"]))
    return "$$%s#%d$$" % (t["jp"], t["zukan_id"])


def resolve(jp, disc, idx, where=""):
    """The one term a reference names, or a hard error."""
    same = idx.get(jp)
    if not same:
        raise SystemExit("%sno glossary term for %r" % (where and where + ": ", jp))
    if disc is None:
        if len(same) == 1:
            return same[0]
        raise SystemExit(
            "%s%r is ambiguous (%s) -- name one of: %s"
            % (where and where + ": ", jp,
               ", ".join("%s/%s" % (x["kind"], x["en"]) for x in same),
               ", ".join(token_for(x, idx) for x in same)))
    if disc.isdigit():
        hit = [x for x in same if x.get("zukan_id") == int(disc)]
    else:
        hit = [x for x in same if x["kind"] == disc]
    if len(hit) == 1:
        return hit[0]
    raise SystemExit("%s%r#%s matches %d terms -- try one of: %s"
                     % (where and where + ": ", jp, disc, len(hit),
                        ", ".join(token_for(x, idx) for x in same)))


def expand(text, idx, where=""):
    """Resolve every reference in `text`. An unknown or ambiguous one stops the
    build -- shipping a literal `$$...$$` on screen is worse than not
    building."""
    if text is None or "$$" not in text:
        return text

    def sub(m):
        jp, disc, mod = m.group(1), m.group(2), m.group(3)
        t = resolve(jp, disc, idx, where)
        en = t.get("en")
        if not en:
            raise SystemExit("%sterm %r has no English yet"
                             % (where and where + ": ", jp))
        return (en[:1].lower() + en[1:]) if mod else en

    return TOKEN.sub(sub, text)


def used(text):
    """(japanese, discriminator) for every reference in a string."""
    return [(m.group(1), m.group(2)) for m in TOKEN.finditer(text or "")]


def stray(text):
    """`$$...$$` that did not parse -- a typo that would otherwise reach the
    screen verbatim. `$n` and `$l` are the game's own escapes and are never
    touched, because they are a single dollar."""
    if text is None:
        return []
    return [s for s in re.findall(r"\$\$[^$\n]{0,64}\$?\$?", TOKEN.sub("", text))
            if s.startswith("$$")]


def walk_sources(dirs):
    """(path, field, text) for every English string a build reads: `LINES[].en`
    in the stage modules, `ENTRIES[id].DSCR/DSC2` and `NAMES` in the library
    batches. `jp` is never touched."""
    for d in dirs:
        if os.path.isfile(d):
            files = [d]
        else:
            files = [os.path.join(r, f)
                     for r, _s, fs in os.walk(d) for f in fs if f.endswith(".json")]
        for p in sorted(files):
            try:
                doc = json.load(open(p, encoding="utf-8"))
            except Exception:
                continue
            for blk in doc.get("LINES", []) or []:
                if isinstance(blk, dict) and blk.get("en"):
                    yield p, "LINES[%s].en" % blk.get("sha", "?"), blk["en"]
            for eid, ent in (doc.get("ENTRIES") or {}).items():
                for f in ("DSCR", "DSC2"):
                    if isinstance(ent, dict) and ent.get(f):
                        yield p, "ENTRIES[%s].%s" % (eid, f), ent[f]
            for jp, en in (doc.get("NAMES") or {}).items():
                if en:
                    yield p, "NAMES[%s]" % jp, en


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd, gpath = argv[1], argv[2]
    g = json.load(open(gpath, encoding="utf-8"))
    idx = index(g)

    if cmd == "list":
        # the Japanese is matched as typed and the English case-insensitively.
        # Lowercasing the pattern for BOTH made a fullwidth query silently
        # miss: "ＡＧ".lower() is "ａｇ", which no glossary key contains, so
        # `list ＡＧ` reported 0 of 1141 for a term that is right there.
        raw_pat = argv[3] if len(argv) > 3 else ""
        pat = raw_pat.lower()
        hits = [t for t in g["terms"]
                if raw_pat in t["jp"] or pat in (t["en"] or "").lower()]
        for t in sorted(hits, key=lambda t: t["jp"])[:80]:
            print("  %-36s %-30s %s" % (token_for(t, idx), t["en"], t["kind"]))
        print("%d of %d terms" % (len(hits), len(g["terms"])))
        return 0

    if cmd == "check":
        dirs = argv[3:] or ["translation"]
        bad = seen = 0
        # expansion is not recursive, so a term whose own English holds a
        # reference would ship `$$...$$` to the screen
        for t in g["terms"]:
            if t.get("en") and "$$" in t["en"]:
                print("  glossary: %r English contains a reference: %r"
                      % (t["jp"], t["en"]))
                bad += 1
        # and every term must be addressable by some token
        for t in g["terms"]:
            try:
                token_for(t, idx)
            except SystemExit as e:
                print("  glossary: %s" % e)
                bad += 1
        for p, field, text in walk_sources(dirs):
            for s in stray(text):
                print("  %s: %s: malformed reference %r" % (p, field, s))
                bad += 1
            for jp, disc in used(text):
                seen += 1
                try:
                    t = resolve(jp, disc, idx)
                    if not t.get("en"):
                        print("  %s: %s: %r has no English" % (p, field, jp))
                        bad += 1
                except SystemExit as e:
                    print("  %s: %s: %s" % (p, field, e))
                    bad += 1
        print("%d references checked, %d problems" % (seen, bad))
        return 1 if bad else 0

    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
