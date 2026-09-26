"""Normalise a merged stage translation onto `$$japanese$$` references.

    python tools/tokenise_stage.py translation/stage0031b_03.json [..] [--apply]

A slice sometimes writes a glossary name as literal English -- an older
checker rejected `$` outright, so a translator would strip the tokens to get
a clean run, and a term missed by one slice is inconsistent with the twenty
that used it. This puts every record back on the token.

It differs from `tools/tokenise.py`, which matches on the English: a term is a
candidate here only when its JAPANESE occurs in that record's `jp`. That is
much stronger evidence -- it is what makes a two-letter name like `AG` safe,
where matching "AG" in English alone could not tell a name from an initialism.

The safety property is unchanged and mechanical: a record is rewritten only
when expanding the new text reproduces the old English character for
character, so the text on screen cannot move.

What it will NOT touch, because the Japanese matching is evidence and not
proof -- the round trip cannot tell a wrong term from a right one, since both
expand to the same string:

  * a term whose English is an ordinary word (Princess, Zero, Lady, Boss, An,
    President ...). `姫` is the SRW-original keyword, not Unicorn's `姫様`;
    `ゼロ` is Lelouch, not Wing Zero. Convert those by hand, having read them.
  * a Japanese naming two terms, unless the record's English already names
    exactly one of them, or `KNOWN` below settles it.
  * a surname the glossary keys to one series that another series' character
    also carries, where `SHARED_SURNAME` below names the evidence that this
    record means the other person. `赤木博士` is Evangelion's Ritsuko, not
    Dai-Guard's Akagi Shunsuke, and both spell out "Akagi".
"""
import io
import json
import os
import re
import sys
import collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import terms as T  # noqa: E402

# a Japanese shared by a pilot and its machine, settled by reading the scenes:
# the speaker line names the pilot, prose about the thing names the robot
KNOWN = {
    "ボン太くん": ("pilot", "robot"),
    "ブラックオックス": ("pilot", "robot"),
    "宇宙魔王": ("pilot", "pilot"),
    "マーグ": ("pilot", "pilot"),
    "オルソン": ("50", "50"),
}
# never converted automatically: the English is an ordinary word, so a match
# is not evidence the glossary term is what the line means
ORDINARY = {"an", "angel", "boss", "king", "lady", "president", "princess",
            "queen", "sphere", "will", "zero", "sensei", "hill", "roger"}
# a surname the glossary keys to ONE series that a DIFFERENT series' character
# also carries. ORDINARY cannot catch these -- the English is a name, not an
# ordinary word -- and neither can the round trip, because both people expand
# to the same spelling. The value is the evidence that the record means the
# other character, so the term is offered everywhere except there.
SHARED_SURNAME = {
    # The glossary's 赤木 is Dai-Guard's Akagi Shunsuke, who is not a doctor.
    # `赤木博士` is Evangelion's Ritsuko Akagi, and tokenising her would put
    # her name under a Dai-Guard rename.
    "赤木": ("博士",),
}


def build_index():
    g = json.load(open(os.path.join(ROOT, "analysis", "glossary.json"),
                       encoding="utf-8"))
    idx = T.index(g)
    by_first = collections.defaultdict(list)
    for jp in idx:
        by_first[jp[0]].append(jp)
    return idx, by_first


# Katakana, and the prolonged-sound mark: a run of these is ONE name. The
# interpunct is deliberately not here -- `シャア・アズナブル` and `シャア` are
# both entries, so longest-match already settles those.
GLUE = re.compile(r"[ァ-ヺー]")


def inside_a_longer_name(jp, text):
    """True when ANY occurrence of `jp` sits inside a longer katakana run.

    `アークグレンラガン` is its own machine and has no glossary entry, but
    `グレンラガン` does, so a substring match splits the name and produces
    `Arc-$$グレンラガン$$`. THE ROUND TRIP CANNOT CATCH THAT -- both spellings
    expand to the same text -- and the result quietly files one machine under
    another's term, so a rename would rewrite it.

    ANY, not every. `キングキタン` is Kittan's machine and `キタン` is Kittan,
    so a record where he SPEAKS about it contains both a free-standing
    occurrence and one inside the machine's name. Matching on "every" let that
    through and produced `King $$キタン$$`. Nothing in the record tells the
    tool which English "Kittan" is the pilot and which is the machine, so it
    must decline the whole record and leave it to a reader.
    """
    if not GLUE.match(jp[0]):
        return False           # only katakana names run together this way
    start = 0
    while True:
        at = text.find(jp, start)
        if at < 0:
            return False       # never glued to anything: safe to offer
        before = text[at - 1] if at else ""
        after = text[at + len(jp):at + len(jp) + 1]
        if (before and GLUE.match(before)) or (after and GLUE.match(after)):
            return True        # part of a longer name somewhere in this record
        start = at + 1


def refs(jp_text, by_first):
    """Glossary Japanese occurring in this record, longest match wins."""
    hits = []
    for ch in set(jp_text):
        for jp in by_first.get(ch, ()):
            if jp in jp_text and not inside_a_longer_name(jp, jp_text):
                hits.append(jp)
    hits.sort(key=len, reverse=True)
    keep = []
    for jp in hits:
        if not any(jp in k and jp != k for k in keep):
            keep.append(jp)
    return keep


def pick(jp, idx, line, head):
    cands = idx.get(jp, [])
    if len(cands) == 1:
        return cands[0]
    if jp in KNOWN:
        disc = KNOWN[jp][0 if head else 1]
        hit = [c for c in cands
               if c["kind"] == disc or str(c.get("zukan_id")) == disc]
        return hit[0] if len(hit) == 1 else None
    named = [c for c in cands if c.get("en") and
             re.search(r"(?<![A-Za-z])%s(?![A-Za-z])" % re.escape(c["en"]), line)]
    return named[0] if len(named) == 1 else None


def convert(path, idx, by_first, apply):
    doc = json.load(open(path, encoding="utf-8"))
    lines = doc.get("LINES") or []
    changed = 0
    skipped = collections.Counter()
    for r in lines:
        en, jp = r.get("en") or "", r.get("jp") or ""
        if not en:
            continue
        parts = en.split("\n")
        new_parts = list(parts)
        for tjp in refs(jp, by_first):
            for i, line in enumerate(new_parts):
                t = pick(tjp, idx, line, i == 0)
                if t is None or not t.get("en"):
                    skipped["ambiguous"] += 1
                    continue
                if t["en"].lower() in ORDINARY:
                    skipped["ordinary word"] += 1
                    continue
                if any(m in jp for m in SHARED_SURNAME.get(tjp, ())):
                    skipped["shared surname"] += 1
                    continue
                tok = T.token_for(t, idx)
                pat = (r"(?<![A-Za-z$])%s(?=(?:s|'s)?(?![A-Za-z]))"
                       % re.escape(t["en"]))
                new_parts[i] = re.sub(pat, lambda _m, _t=tok: _t, line)
        new = "\n".join(new_parts)
        if new == en:
            continue
        try:
            if T.expand(new, idx, path) != T.expand(en, idx, path):
                skipped["round trip differs"] += 1
                continue
        except SystemExit:
            skipped["expand refused"] += 1
            continue
        changed += 1
        if apply:
            r["en"] = new
    if changed and apply:
        raw = open(path, "rb").read()
        crlf = b"\r\n" in raw
        text = json.dumps(doc, ensure_ascii=False, indent=1)
        if crlf:
            text = text.replace("\n", "\r\n")
        open(path, "wb").write(text.encode("utf-8"))
    print("%-40s %4d records tokenised%s%s"
          % (os.path.basename(path), changed,
             "" if apply else "  (dry run)",
             ("   skipped " + str(dict(skipped))) if skipped else ""))
    return changed


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    paths = [a for a in argv[1:] if not a.startswith("-")]
    if not paths:
        print(__doc__.strip())
        return 2
    idx, by_first = build_index()
    total = 0
    for p in paths:
        total += convert(p, idx, by_first, "--apply" in argv)
    print("%d records %s" % (total, "tokenised" if "--apply" in argv else "would change"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
