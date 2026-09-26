"""Export one voice section as a self-contained translation brief.

    python tools/export_voice.py 17 [18 ...] [--out work/voice/brief]

A section is one unit's voice set. The brief carries everything the
translator needs and nothing it must look up: who is speaking, the English
already shipped for the weapons their call-outs name, the glossary terms
that actually occur, and every distinct line with its byte budget.

Only DISTINCT lines are listed. ~48,000 index entries address ~32,000
strings: a line reused by several situations is stored once and pointed at
repeatedly, so one translation serves all its users and the repeats are not
work. The entry numbers here are the ones the writer keys on.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voice_lib as V     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
# Lines the developers left as placeholders: a run of fullwidth dashes, or
# one that says outright that it is silent and never displayed in the real
# game. They never reach the screen -- leave them Japanese.
SENTINEL = ("－－－", "無音", "表示しません")
LQ, RQ = "「", "」"
DRAW = "A-Z a-z 0-9 . , ! ? : ; ' - ( ) / & % + = [ ]"
# Units that a weapon match lands on far too often to trust: a beam rifle, a
# vulcan or a beam saber is carried by dozens of machines, so these three
# collect sections that name any of them. They hold 50 of the 141 attributed
# sections between them, and two have been proven wrong outright (8 and 141,
# both "Strike Freedom / Kira Yamato", are a Full Metal Panic mercenary and
# a Tetsujin No. 28 robot-mafia goon). Treat them as unknown until the lines
# say otherwise.
MAGNETS = ("Gundam Mk-II", "Strike Freedom Gundam", "Nu Gundam")


def rd(*parts):
    return json.load(open(os.path.join(ROOT, *parts), encoding="utf-8"))


HEAD = """# Voice brief -- section %(sec)03d%(who)s

Japanese -> English for the battle subtitle lines of ONE unit's voice set in
a PS3 Super Robot Wars game. %(n)d distinct lines below.

Write the result to `%(answer)s` as ONE JSON object mapping each entry
number (a STRING key) to its English:

    {"0": "My chance!", "3": "Can't hesitate!"}

Include every entry listed below and nothing else.

## Length

There is no byte budget any more: the game file is rebuilt block by block,
so a line may be as long as it needs to be. The `budget` column below is
the size of the ORIGINAL Japanese slot, for information only. The limit
that remains is the screen: keep a line under about 36 cells (one per
letter, space or punctuation mark). Write full, natural English -- a bark
is still a shout, not a sentence, but it should carry the whole meaning.

Run `python tools/check_voice.py %(answer)s` yourself before reporting back:
it names any character the font cannot draw and any line over the cap.

**Write the file in batches of roughly 100 entries, not all at once.** Write
the first batch as soon as you have it and add each later batch to what is
already there. Two runs have been lost to this: one agent was killed by a
rate limit before it had written anything, and another tried to emit 379
lines in a single tool call and blew the model's output limit -- in both
cases every line was gone. A file on disk survives; a draft in your head
does not.

Battle barks are shouts, not sentences: 'Take this!', 'Not yet!', 'It's
over!'. Say everything the Japanese says, and nothing more.

## Rules, in order of how badly breaking them hurts

1. **Keep the whole meaning.** Length is no longer a constraint (under
   about 36 cells); do not clip a line to sound terse, and do not pad one.
2. **Only these characters can be drawn:** `%(draw)s` and space. No double
   quote (use the apostrophe), no ellipsis character (three dots cost three
   letters, so usually just drop it), no em dash (use a hyphen).
3. **Do not write the %(lq)s %(rq)s quote brackets.** The writer adds them.
   Your English is the text INSIDE them.
4. **A literal two-character backslash-n in the Japanese is a line break the
   game consumes.** Keep it, exactly as backslash + n, in the same place. It
   costs 1 cell (it is two characters but one cell).
5. **Weapon call-outs must use the shipped English weapon name**, verbatim
   from the weapon table below IF THERE IS ONE -- not every section names a
   weapon this project has already translated, and a section with no table
   simply has none to match. The bark and the weapon label appear on screen
   together, so a mismatch reads as a bug; an invented name is worse than a
   flagged one.
6. **Use the glossary below verbatim** for any term in it.
7. **Never infer gender.** Use he/she only where the notes below establish
   it; anyone else is they/them or a rephrase. A name is not evidence of
   gender.
8. **No honorifics** (-san, -kun, -sama). Render the relationship in English
   or drop it. Sensei is the exception this project already shipped: it
   stays 'Sensei' where it is used as a name.
9. **Leave a line in Japanese by OMITTING its key**, never by inventing
   English for it. Anything you omit ships as the original Japanese, which
   is a safe outcome; a wrong guess is not.

## Voice

Keep the pilot's register: a hot-blooded pilot shouts, a cold one does not.
A line that is two words in Japanese must not become a sentence in English --
the line would only get longer for nothing. Keep exclamation and question marks
where the Japanese has them (they cost a letter each; drop the mark before
you drop a word).

Barks come in families -- attack call-outs, dodges, hits taken, defeat,
support, a spirit command. Lines that are near-identical in Japanese should
stay near-identical in English, and lines that differ should stay different:
the player hears them back to back.

That last part is a rule, not a preference. **Never let two different
Japanese lines collapse to the same English string.** It happens when a long
glossary name is all a short bark has room for and only punctuation varies --
and the fix is to let ONE line carry the name while the others carry their
meaning, not to ship the name three times. Check your answer for repeated
values before you report back.
"""

TAIL = """
## Report back

After writing `%s`, report:

- entries answered vs entries in this brief (equal, minus anything you
  deliberately omitted -- list what you omitted and why)
- every entry where the budget forced you to lose meaning
- anything about the speaker's identity you could not verify
"""


def brief(sec, out_dir):
    lines = rd("source", "voice", "%03d.json" % sec)
    secrow = {r["sec"]: r for r in rd("work", "voice", "sections.json")}[sec]
    gl = rd("analysis", "glossary.json")
    terms = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
    weapons = rd("translation", "weapons.json")
    pilots = rd("work", "voice", "pilots.json")

    def en_of(jp):
        """Glossary English for a name. Unit names arrive as 'A / B' when RPW
        stores two spellings of the same machine -- either half resolves it."""
        if not jp:
            return None
        for cand in [jp] + [h.strip() for h in jp.split("/")]:
            for key in (cand, cand.replace(" ", ""), cand.replace("　", "")):
                if terms.get(key):
                    return terms[key]
        return None

    unit_jp = secrow.get("unit")
    who = next((r for r in pilots if sec in r["sections"]), None)
    pilot_jp = who["pilot"] if who else None
    # Corrections established by reading the lines outrank the parser that
    # suggested the unit (work/voice/identity.json).
    fixed = None
    ipath = os.path.join(ROOT, "analysis", "voice_identity.json")
    if os.path.exists(ipath):
        fixed = json.load(open(ipath, encoding="utf-8")).get(str(sec))

    distinct = [r for r in lines if not r["shared"]]
    todo = [r for r in distinct
            if not any(m in r["jp"] for m in SENTINEL)]
    body = "\n".join(r["jp"] for r in lines)

    # weapon names the call-outs actually speak, with the English that ships
    weps = sorted({(k, weapons[k]) for k in weapons
                   if len(k) >= 3 and k in body}, key=lambda t: -len(t[0]))
    # glossary terms that actually occur (names, series, places)
    seen = sorted({(k, v) for k, v in terms.items()
                   if len(k) >= 3 and k in body}, key=lambda t: -len(t[0]))[:60]

    answer = "work/voice/answer/%03d.json" % sec
    ident = []
    if fixed:
        ident.append("**identity corrected by an earlier reading of these "
                     "lines** -- unit %s, pilot %s. Why: %s  Trust THIS over "
                     "anything below."
                     % (fixed.get("unit") or "unresolved",
                        fixed.get("pilot") or "unresolved", fixed["why"]))
    if unit_jp:
        ident.append("unit %s (%s), matched by weapon call-out, score %.1f"
                     % (en_of(unit_jp) or "?", unit_jp, secrow.get("pts", 0)))
    else:
        ident.append("unit UNKNOWN -- no weapon call-out matched. Infer the "
                     "speaker from the lines themselves and SAY SO in your "
                     "report; if you cannot, translate them as generic battle "
                     "barks with no name in them.")
    if pilot_jp:
        ident.append("pilot %s (%s)" % (en_of(pilot_jp) or "?", pilot_jp))
    # A middling weapon match has been flatly wrong: section 8 scored 7.5 as
    # Strike Freedom / Kira Yamato and its lines are a Full Metal Panic
    # mercenary. Say so in the brief rather than letting the table's register
    # be adopted on trust.
    if unit_jp and (en_of(unit_jp) in MAGNETS):
        ident.append("**DO NOT TRUST that attribution.** %s collects sections "
                     "whose lines merely name a common weapon (a beam rifle, "
                     "a vulcan), and two such sections have been proven to be "
                     "other shows entirely. Work out the speaker FROM THE "
                     "LINES BELOW -- who they name, what they call their "
                     "machine -- and say in your report who you concluded it "
                     "is. If you cannot tell, translate them as generic "
                     "battle barks with no name in them."
                     % (en_of(unit_jp) or unit_jp))
    elif unit_jp and secrow.get("pts", 0) < 9:
        ident.append("**that attribution is a weapon-name match with a "
                     "middling score, and one like it was flatly wrong** "
                     "(section 8 scored 7.5 as Strike Freedom / Kira Yamato; "
                     "its lines are a Full Metal Panic mercenary). Read a "
                     "sample of the lines below BEFORE adopting that "
                     "character's register: if the content names another "
                     "show's people or machines, translate the content and "
                     "say so in your report.")
    if who and len(who["sections"]) > 1:
        ident.append("this pilot also speaks in sections %s -- the same "
                     "phrasing should be used there"
                     % ", ".join(str(x) for x in who["sections"] if x != sec))

    txt = io.StringIO()
    txt.write(HEAD % {
        "sec": sec,
        "who": (" -- %s" % (en_of(unit_jp) or unit_jp)) if unit_jp else "",
        "n": len(todo), "answer": answer, "draw": DRAW, "lq": LQ, "rq": RQ,
    })
    txt.write("\n## Who is speaking\n\n")
    for i in ident:
        txt.write("- %s\n" % i)
    txt.write("- %d index entries in this section, %d distinct strings, %d to "
              "translate (the rest are repeats of these, plus the developers' "
              "silence line, which stays Japanese).\n"
              % (secrow["count"], len(distinct), len(todo)))

    if weps:
        txt.write("\n## Weapon names -- use these EXACTLY\n\n")
        for jp, en in weps:
            txt.write("- `%s` -> **%s**\n" % (jp, en))
    if seen:
        txt.write("\n## Glossary terms that occur here\n\n")
        for jp, en in seen:
            txt.write("- `%s` -> **%s**\n" % (jp, en))

    txt.write("\n## Lines\n\n| entry | budget | Japanese |\n|---|---|---|\n")
    for r in todo:
        txt.write("| %d | %d | %s |\n" % (r["i"], r["budget"],
                                          r["jp"].replace("|", "\\|")))
    txt.write(TAIL % answer)

    os.makedirs(os.path.join(ROOT, out_dir), exist_ok=True)
    path = os.path.join(ROOT, out_dir, "%03d.md" % sec)
    open(path, "w", encoding="utf-8").write(txt.getvalue())
    return path, len(todo)


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    out_dir = "work/voice/brief"
    args = []
    skip = False
    for a in argv[1:]:
        if skip:
            out_dir, skip = a, False
        elif a == "--out":
            skip = True
        elif not a.startswith("--"):
            args.append(a)
    if not args:
        print(__doc__.strip())
        return 2
    V.table()          # fails loudly if the geometry table is missing
    for a in args:
        p, n = brief(int(a), out_dir)
        print("%s  %d lines" % (os.path.relpath(p, ROOT).replace(chr(92), "/"), n))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
