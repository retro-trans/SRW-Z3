"""Export a slice of a scenario member as a translation brief.

The library batches have `export_batch.py`; scenario dialogue needs a different
sheet, because a line is not a standalone string -- it carries a speaker, a
hand-wrapped shape, keyword link spans that must survive, and `$n`-style
escapes the game substitutes at runtime.

Each brief is self-contained: conventions, the glossary for the terms that
actually appear in that slice, and the records with their stable `sha`. The
translator writes back one JSON object of {sha: english}, so nothing depends on
order and two briefs can never overwrite each other's work.

    python tools/export_stage.py <member.lua> <glossary.json> <out.md> \
                                 [--range A:B] [--answer path.json]
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import glob   # noqa: E402
import collections   # noqa: E402
import luarec   # noqa: E402
import terms as T   # noqa: E402

MAX_CHARS = 55        # measured: stage 1's widest shipped line is 53 (725 of 963 px)
DRAWABLE = "A-Z a-z 0-9 . , ! ? : ; ' - ( ) / &"

HEAD = """# Translation brief -- %(name)s records %(lo)d..%(hi)d

Japanese -> English for a PS3 Super Robot Wars scenario. %(n)d records below.

Write the result to `%(answer)s` as ONE JSON object mapping each record's
`sha` to its English:

    {"455328beab": "$$シン$$\\n\\u300cLook at that, everyone!\\n\\u3000It's our Earth!\\u300d", ...}

Include every sha in this brief and nothing else.

## Do this before you translate a single line

A record's identity is a hash of its JAPANESE, so a line that already ships
somewhere else is the same record, and its English is not yours to re-decide.
Stages repeat whole scenes from each other: one stage was 65%% lines that
already existed. Check for that IN ONE PASS, before translating, not line by
line while you work -- line-by-line checking is what let 28 records ship
re-worded in stage 81:

    import json
    ship = json.load(open('work/tr/shipped.json', encoding='utf-8'))
    # then print every sha in this brief that appears in `ship`

Each entry is `{"en": majority wording, "n": how many copies}`, plus
`"others"` and `"tied"` when that sha ships more than one way -- 587 of them
do. Take `en`. When `tied` is true there is no majority to defer to, so pick
one, say so in your report, and do not present it as settled.

If `work/tr/shipped.json` is missing, build it with
`python tools/shipped_index.py` -- do NOT rebuild the table inline. Six slices
scanning the corpus in parallel is what a usage limit killed mid-scan, before
any of them had written a record.

Only `stage*.json` holds records with a `sha`. The battle-subtitle files,
`translation/voice_*.json`, are shaped differently -- a `lines` DICT of
`{jp, en}` with no sha at all -- so they cannot be matched this way and a
glob that includes them silently contributes nothing. They are still worth
searching BY JAPANESE TEXT when you need precedent for a term or a phrase:
one slice found the only existing rendering of a term that way.

Every sha that already ships takes the MAJORITY shipped English, character for
character, including the leading fullwidth spaces of a banner. Do not re-word
it, re-wrap it or improve it. Translate only what is genuinely new, and say in
your report how many you reused.

## Rules, in order of how badly breaking them hurts

1. **Keep every `$n`, `$l`, `$F` and `$c` exactly as they appear, and the
   same number of each.** They are runtime substitutions: `$n`/`$l` is the
   player-named protagonist, `$F` a name fragment, and `$c` the player-named
   squad (the ZEUTH/ZEXIS slot, as in `「$cとして行動を開始します」`). Do not
   translate, space or reorder them, and do not repeat one to avoid a
   pronoun: a line with one `$c` must come out with one `$c`.
2. **Keep the same number of `《 》` pairs, in the same order.** Those are
   keyword links; the game matches them positionally against a separate id
   list, so adding or dropping one silently mislinks the rest of the line.
   Translate the text inside them.
3. **Keep the line shape.** A record is a speaker name, then the speech in
   `「 」`. Continuation lines start with ONE `　` (U+3000) -- never two.
   Keep the same `「」` placement. You do NOT have to match the source's
   line count: English often needs one line more, and 40 shipped stage 1
   records use four lines where the Japanese used three. Do not cramp a
   line to preserve parity -- that is not the rule.
   THE CEILING IS 4 LINES PER RECORD *INCLUDING THE SPEAKER NAME*, so a
   spoken record gets at most THREE lines of speech. The checker splits the
   whole record, speaker line and all. No shipped record anywhere exceeds
   this: 5,211 records sit at exactly 3 speech lines, none at 4.
4. **Max %(max)d characters per line.** Lines are hand-wrapped, not reflowed, and
   an overlong one runs off the textbox. Re-wrap within the same line count.
5. **Only these characters can be drawn:** %(draw)s and the fullwidth
   `「 」 《 》 　 （ ） ～`. The fullwidth tilde `～` (U+FF5E) IS
   drawable -- every location banner uses it -- but NEVER the wave dash
   `〜` (U+301C), which looks the same and shipped wrongly 12 times.
   A thought line that the Japanese writes with
   fullwidth `（ ）` keeps them: they are drawable, and the corpus uses them
   1076 times against 164 ASCII. No double quote -- use `'`. Write `...` not
   `…`.
   No em dash and no double hyphen `--`: use a comma, a full stop or `...`.
6. **Write every glossary term as `$$japanese$$`, not as English.** A term
   inside prose is a reference, not text: the build expands `$$スフィア$$`
   to the glossary's English, so renaming a term later changes every line
   at once. Suffixes go OUTSIDE the token (`$$スフィア$$s`), `|lc`
   lower-cases it mid-sentence, and a `#` discriminator separates two terms
   that share one Japanese string (`$$レイ#333$$`). The speaker name on
   line 1 is a term too when it is in the glossary -- write `$$シンジ$$`,
   not `Shinji`. Only words that are NOT in the glossary table below stay
   plain English. `check_stage.py` expands references before it measures, so
   a token is what you check, not something to add afterwards.
7. **Use the glossary below verbatim** for any term in it. Consistency across
   the project matters more than a nicer phrasing.
8. **Never infer gender.** `$n`/`$l` is the protagonist Hibiki: the player
   may rename him, but he is always male -- he/him/his (the user's ruling,
   2026-09-27; the Japanese itself calls him 男). For anyone else, use he/she
   only when the cast sheet or glossary establishes it; an unknown or
   offscreen person gets they/them or a rephrase. A name is not evidence of
   gender.
9. **When a line will not fit, compress or abbreviate -- never cut the end
   of a sentence.** If it still cannot fit, translate it as best you can and
   FLAG the sha in your report rather than silently overflowing. And leave
   every control code and placeholder in place: `$n` expands to a name the
   player typed (assume ~10 letters), so a line carrying it needs slack.

## Voice

Keep each speaker's register. Terse military characters stay terse; a line
that is one word in Japanese should not become a sentence. Keep exclamation
and question marks where the Japanese has them. Do not add content that is not
in the source, and do not explain what the source leaves implicit.

## Cast

Who is speaking, and how they speak. `VOICE` is a curated note about register;
the paragraph under it is the character's own library entry, already translated
elsewhere in this project. Match an established voice rather than inventing one.

%(cast)s

## Glossary for this slice

%(gloss)s

## Context -- DO NOT TRANSLATE

The records just outside your slice, so scene boundaries and running jokes
read correctly. Another translator owns them; answer only your own records.

%(context)s

## Reporting

With your answer file, report: records examined vs records in the slice,
and every sha you are unsure of or had to FLAG (overlong, unverifiable
referent, uncertain reading) with one line on why. A flagged line beats a
silent guess.

## Records

%(recs)s
"""


def cast_for(recs, g, idx):
    """A voice card per speaker, built from what the project already knows.

    A translator's hardest problem is register, and the answer is mostly
    already in the repo: the library has a biography for nearly every
    speaking character and 31 of stage 2's 37 are already in English. So
    derive the cards rather than asking anyone to invent them, and rather
    than copying biography into the glossary where it would be a second
    source of truth that can drift from the zukan.

    The glossary's own `voice` field, where set, carries the thing the
    biography does NOT: how the character SPEAKS. That is curated, short,
    and shown first because it is what actually changes a line.
    """
    # Key on the name the record PRINTS, never on `pid`. `pid` is the portrait
    # the game shows and it is NOT the speaker: 63 of 405 records in stage 2
    # member 3 disagree with their pid's majority name, and record 171 is
    # `pid_AG` while printing 宗介. Keying on pid mis-attributes one line in six.
    printed = collections.defaultdict(collections.Counter)
    for r in recs:
        first = r["jp"].replace("\r\n", "\n").split("\n")[0].strip()
        if first and "\u300c" not in first:
            printed[first][r["pid"] or "-"] += 1
    by_jp = {}
    for t in g["terms"]:
        by_jp.setdefault(t["jp"], []).append(t)
    bios = {}
    for f in sorted(glob.glob(os.path.join("translation", "library", "pt_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        for eid, ent in (d.get("ENTRIES") or {}).items():
            if isinstance(ent, dict) and ent.get("DSCR"):
                bios[int(eid)] = ent["DSCR"]
    out = []
    for name, pids in sorted(printed.items(), key=lambda kv: -sum(kv[1].values())):
        pid = pids.most_common(1)[0][0]
        lines = sum(pids.values())
        pil = [c for c in by_jp.get(name, []) if c["kind"] == "pilot"]
        en = pil[0]["en"] if len(pil) == 1 else None
        voice = next((c.get("voice") for c in pil if c.get("voice")), None)
        # A PRINTED NAME CAN BELONG TO TWO CHARACTERS FROM DIFFERENT SERIES.
        # `レイ` is Rei Ayanami and also Ray Lovelock; `ドロシー` is Dorothy
        # Catalonia and also R. Dorothy Waynewright. Taking the first
        # candidate put the wrong person's biography on the sheet, and in
        # stage 88 a slice believed it and named the wrong character. Carry
        # EVERY candidate so the sheet can say the name is ambiguous instead
        # of quietly choosing.
        cands = []
        for c in pil:
            bio = bios.get(c.get("zukan_id"))
            cands.append((T.token_for(c, idx), c.get("en"),
                          T.expand(bio, idx) if bio else None))
        out.append((pid, name, en, lines, voice, cands))
    return out


def cast_sheet(cast):
    if not cast:
        return "_(no named speakers)_"
    rows = []
    for pid, name, en, lines, voice, cands in cast:
        head = "**%s** (prints as %s, %d lines; usual portrait `%s`)" % (
            en or name, name, lines, pid)
        rows.append(head)
        if voice:
            rows.append("  - VOICE: %s" % voice)
        if len(cands) > 1:
            rows.append("  - AMBIGUOUS: this printed name belongs to %d "
                        "different characters, from different series. DECIDE "
                        "FROM THE SCENE, not from this sheet, and use the "
                        "matching discriminator." % len(cands))
            for tok, cen, bio in cands:
                flat = " ".join(bio.split()) if bio else "(no library entry)"
                rows.append("    - %s = %s -- %s"
                            % (tok, cen or "?",
                               flat[:200] + ("..." if len(flat) > 200 else "")))
        elif cands and cands[0][2]:
            flat = " ".join(cands[0][2].split())
            rows.append("  - %s" % (flat[:300] + ("..." if len(flat) > 300 else "")))
        else:
            rows.append("  - (no library entry -- unnamed or player-named)")
        rows.append("")
    return "\n".join(rows)


def glossary_for(text, terms, idx=None):
    """The terms occurring in this slice, one row each.

    A Japanese string that keys TWO terms got a row apiece, both printed under
    the same bare Japanese -- so the table said `オルソン` twice and left the
    slice to guess which one its line meant. Those rows now carry the
    discriminator token that actually selects the term, and say which series
    each belongs to, the same way the cast sheet marks an ambiguous speaker.
    """
    rows = []
    for t in sorted(terms, key=lambda t: -len(t["jp"])):
        if t.get("en") and t["jp"] in text:
            rows.append(t)
    if not rows:
        return "_(no glossary terms appear in this slice)_"
    shared = collections.Counter(t["jp"] for t in rows)
    keyed = [(T.token_for(t, idx) if shared[t["jp"]] > 1 and idx is not None
              else t["jp"], t) for t in rows]
    out, w = [], max(len(k) for k, _ in keyed)
    for key, t in keyed:
        out.append("    %-*s  %-34s (%s)" % (w, key, t["en"], t["kind"]))
        if shared[t["jp"]] > 1:
            # `source` is not reliable here: both オルソン entries name the same
            # series even though one is from a different show entirely. The
            # note is where the difference is actually written down.
            why = (t.get("note") or "").strip() or t.get("source") or ""
            out.append("        AMBIGUOUS -- DECIDE FROM THE SCENE. %s" % why)
    return "\n".join(out)


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    lua, gpath, outmd = argv[1], argv[2], argv[3]
    recs = luarec.records(open(lua, "rb").read().decode("cp932"))
    lo, hi = 0, len(recs)
    if "--range" in argv:
        a, b = argv[argv.index("--range") + 1].split(":")
        lo, hi = int(a), int(b)
    answer = argv[argv.index("--answer") + 1] if "--answer" in argv else outmd + ".json"
    sl = recs[lo:hi]
    g = json.load(open(gpath, encoding="utf-8"))
    idx = T.index(g)
    cast = cast_for(sl, g, idx)

    body = []
    for i, r in enumerate(sl, lo):
        spk = r["jp"].replace("\r\n", "\n").split("\n")[0].strip()
        body.append("### %d  sha `%s`  speaker %s  (%s #%s, portrait `%s`)"
                    % (i, r["sha"], spk or "-", r["event"], r["n"], r["pid"]))
        body.append("```")
        body.append(r["jp"].replace("\r\n", "\n"))
        body.append("```")
    ctx = []
    for tag, chunk in (("before the slice", recs[max(0, lo - 8):lo]),
                       ("after the slice", recs[hi:hi + 8])):
        if chunk:
            ctx.append("_%s:_" % tag)
            ctx.append("```")
            for r in chunk:
                ctx.append(r["jp"].replace("\r\n", "\n"))
            ctx.append("```")
        else:
            ctx.append("_(nothing %s -- the member %s here)_"
                       % (tag, "starts" if "before" in tag else "ends"))
    text = "\n".join(r["jp"] for r in sl)
    open(outmd, "w", encoding="utf-8").write(HEAD % {
        "name": os.path.basename(lua), "lo": lo, "hi": hi - 1, "n": len(sl),
        "answer": answer.replace("\\", "/"), "max": MAX_CHARS, "draw": DRAWABLE,
        "gloss": glossary_for(text, g["terms"], idx), "recs": "\n".join(body),
        "cast": cast_sheet(cast), "context": "\n".join(ctx)})
    withbio = sum(1 for c in cast if c[5])
    print("%s  %d records (%d..%d), %d jp chars, %d speakers (%d with a bio) -> %s"
          % (outmd, len(sl), lo, hi - 1, sum(len(r["jp"]) for r in sl),
             len(cast), withbio, answer))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
