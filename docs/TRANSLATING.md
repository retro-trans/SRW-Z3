# Translating a stage

**2026-09-14 source-of-truth update:** Edit `localization/locales/<language>/`
by stable message ID. `translation/` JSON/TSV and `analysis/glossary.json` are
now generated English compatibility views. Read [the current workflow](../localization/README.md).
Commands below describe historical extraction/build formats; do not use old
merge writers on canonical data or assume the old Vietnamese build command
is a validated multilingual build path. New languages need font/layout checks.

The whole chain is one command. Everything it does is a step that was proven
separately first; this just stops them being five manual steps with five traps.

```sh
python tools/build_stage.py \
    work/stage_dec/STG0001A.cpk 4 \
    work/luaA/STG0001A_00004.lua \
    translation/stage0001a.py \
    work/TPACKPS3.CPK work/out1a --npdata work/make_npdata.exe
```

Out come three files: `TPACKPS3.CPK` (font atlas carrying the letter pairs),
`stage.cpk`, and `stage.SDAT`. Copy the first into `DATA/TABATA/` and the last
over the stage in `DATA/STAGE/`.

## Getting the inputs

```sh
# decrypt (close RPCS3 first - single instance)
rpcs3.exe --decrypt STG0001A.SDAT          # -> .unedat, rename to .cpk
python tools/extract_stage.py STG0001A.cpk work/luaA
```

`extract_stage.py` names each member `STG0001A_000NN.lua`; **NN is the member
id** `build_stage.py` wants.

## Writing the translation

A translation module is just `LINES = [...]`, one entry per `[[...]]` block in
file order. See `translation/stage0001a.py`.

Structure that is load-bearing, all of it asserted by `patch_lua.py` rather
than left to care:

| rule | why |
|---|---|
| line 1 is the **speaker name** | structural, never prose |
| `《》` count and order must match the Japanese | they bind **positionally** to the record's `kw_Ary` id list -- the text inside is free, the number is not |
| quote opens `「` closes `」`, continuation lines indent with a **fullwidth** space | these already own atlas cells and render as-is |
| no `]]` anywhere | it would close the Lua long string early |

**Line budget is 31 cells**, from the measured 963px text area at a 31.0px
advance. Count with `digraph.cell_cost()`, not `len()`: `「` and `《` cost a
whole cell each while Latin costs half a cell per letter.

Only characters in `makefont.GLYPHS` can be drawn -- ASCII letters, digits,
`. , ! ? : ; ' - ( ) / &`. No double quote, so use `'`. Write `...` not `…`.

## Two traps

1. **`make_npdata` version 2, not 4.** The originals are v4 and v4 output is
   rejected in-game. `build_stage.py` hardcodes 2.
2. **Delete `dev_hdd0/game/BLJS10256_DATA` after every deploy.** The installed
   copy goes stale against the edited disc and the game reports
   「ゲームデータが壊れています」, which looks exactly like a bad patch.

Do not deploy by hand -- that is how trap 2 gets sprung. `tools/deploy.py`
copies all nine files of a build, hash-checks every one, and only then
removes the installed copy:

```sh
python tools/deploy.py work/out
```

It refuses to run on an incomplete build, because the atlas and every
script share one pair-to-cell mapping and must ship together.

Then check acceptance in seconds instead of booting:

```sh
rpcs3.exe --decrypt candidate.SDAT     # a .unedat appears == the game will load it
```

Validate the oracle against an untouched file in the same run before trusting
it.

## Odd-length runs

A cell holds exactly two letters, so an odd run of Latin pairs its tail with a
space. If the run *already* ended in a space that renders as **two**, showing
up as a gap before a following `「` or `《`. `pairs_of()` drops the trailing
space in that case.

## Building make_npdata

`HANDOFF.md` gives an MSVC line. If VS is installed without the C++ workload
there is no `cl.exe`, and the `Linux/` sources build fine with mingw gcc:

```sh
gcc -O2 -o make_npdata.exe *.c
```

Validate it before trusting it -- its decrypt must agree byte-for-byte with
`rpcs3 --decrypt` on an untouched file. It does.

## Building more than one stage

The atlas is a **single global file**. If each stage picked its own codes
independently, building the second would silently break the first. So all
stages build together from one pooled mapping:

```sh
python tools/build_project.py translation/manifest.py \
    work/TPACKPS3.CPK work/out --npdata work/make_npdata.exe --kanji \
    --ttf "E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF,23,19,1.5" \
    --eboot work/EBOOT_dec.elf
```

`--eboot` builds the patched executable from the same run (see "The 登場作品
label lives in the EBOOT"); `--ttf` bakes a real typeface into the cells
(see "Typeface: Sony Rodin in the cells"). Without `--ttf` the cells use
the stroke letterforms in `makefont.py`.

`--kanji` is required for the English build too: the library alone needs
1,523 disjoint cells and the non-kanji pool has 632 free after the reserved
set. (Measured: 2,653 free with kanji, 2,516 needed.)

`translation/manifest.py` lists stages and their members. Add to it; never
build a stage on its own.

## Cell budget is the real ceiling

Stage 1 alone (344 records, ~10k characters) needs **622 distinct pairs** out
of **634 free cells**. That is essentially the whole safe pool for one chapter.

The safe pool is unassigned SJIS plus Greek, Cyrillic and box drawing -- no
kanji touched. To go further you have to open up kanji cells (leads 0x89-0x97,
~2800 more), which is fine for a *complete* translation and ugly for a partial
one, because any Japanese still on screen renders as Latin fragments.

A full 60-stage translation will exhaust even that. Options at that point, in
order of preference: reuse pairs harder by constraining vocabulary, fall back
to one letter per cell for rare pairs (costs density, not correctness), or
revisit the EBOOT advance.

## Things patch_lua.py asserts, and why each exists

| assertion | the bug it caught |
|---|---|
| block count matches | -- |
| `《》` count per record matches | keyword ids bind positionally |
| no `]]` in the encoding | would close the Lua long string early |
| `--[[` is skipped | `STG0001B_00002` is 28 comments and 0 dialogue; translating them burns cells on text no player sees |
| `$n` / `$l` stay atomic | pairing the letter into a cell destroys the runtime placeholder -- 70 of them in stage 1B |

## Where an odd run's half cell goes

A cell holds exactly two letters, so an odd-length Latin run has half a cell
spare and it has to land somewhere. `digraph.padded_runs()` decides:

1. ends in a space with `「`/`《` next -> drop it (else the pair reads as two)
2. starts with a space -> pad at the end (dropping it gave `》CORPORATION`)
3. end of line -> pad at the end, where it is invisible
4. `「`/`《` precedes -> pad at the front, which reads better than jamming the
   slack against a closing bracket
5. otherwise pad at the end

Half a cell (~7px in game space) of wobble around brackets is inherent to two
letters per cell. Word joins and lost spaces are not, and those are the cases
above.

## Vietnamese and other Latin scripts

Built and shipped, not theorised. `translation/vi/` is stage 1 in Vietnamese.

```sh
python tools/build_project.py translation/vi/manifest.py     work/TPACKPS3.CPK work/out_vi --npdata work/make_npdata.exe     --kanji --metrics 11,25
```

`tools/diacritics.py` composes accented letters from a base glyph plus marks,
decomposing with Unicode **NFD** rather than hardcoding 134 precomposed forms.
So French, Spanish, Czech, Polish and the rest come out for free -- only the
mark strokes are defined, and there are eight of them.

### The two settings it needs

**`--metrics 11,25`.** Vietnamese stacks: `ế` is e + circumflex + acute, `ệ` is
e + circumflex + dot below. Cap height drops 20 texels -> 14 to buy room above
for two marks and below for the dot.

**`--kanji`.** Measured, not guessed:

| | pairs |
|---|---|
| stage 1, English | 622 |
| stage 1, Vietnamese | **852** |
| safe pool (no kanji) | 634 |
| pool with kanji opened | 3454 |

Vietnamese runs ~37% more pairs than English, not the 2x a bigger alphabet
suggests -- it repeats syllables heavily. But 852 > 634, so kanji cells are
required from the start.

### Two things that needed care

`đ`/`Đ` first rendered as plain d: the crossbar has to actually cross the stem,
and the stem is on the **right** for lowercase `d` (x=0.93 in the glyph) and on
the **left** for `D`. One bar position cannot serve both.

The horn on `ơ`/`ư` first read as an acute accent. It now sits **on the
shoulder** and curls right, and when the same letter also carries a tone the
tone shifts left so the two do not collide -- at 11 texels wide, o / ơ / ó / ớ
otherwise collapse into each other.

**Open caveat:** tone marks land around 3 screen pixels tall. They are legible,
and `ơ` vs `ó` is still the subtlest pair. Tone is meaning-bearing in
Vietnamese, so read a real scene in-game before committing to this size.

## Switching builds

English and Vietnamese are separate outputs (`work/out`, `work/out_vi`) that
write the same three files. To swap, copy that build's `TPACKPS3.CPK` into
`DATA/TABATA/` and its `STG*.SDAT` into `DATA/STAGE/`, then delete
`dev_hdd0/game/BLJS10256_DATA`. The atlas and the script must come from the
**same** build -- the pair-to-cell mapping differs between them.

## One string, three people: RPW name slots

The j-string table is **deduplicated**. `レイ` is stored once and 21 pointer
slots reference it -- so a name two characters share is not one string the
game forces on both, it is one string they happen to point at. Each slot is
repointable on its own.

A `pilot-nw` record is `(w0 given name, w1 surname, w2 display name)`, and
that one `レイ` serves three different roles:

```
rec 160/184/185/209   w0=アムロ  w1=レイ       -> Amuro Ray   (レイ is a SURNAME)
rec 445/450           w0=レイ    w1=ラブロック   -> Ray Lovelock
rec 855/856/857/...   w0=レイ    w1=綾波        -> Rei Ayanami
```

Swapping the string once got two of the three wrong: the build shipped
`Amuro Rei`, `Ray Lovelock` as `Rei`, and `Mehna Carmine` as `Mina` -- seven
records, from the same flat `{jp: en}` bug the zukan had.

`rpw.name_overrides` resolves it per slot. The `(given, surname)` pair names
the character, so look that up and take the short-name term pinned to the
same `zukan_id`; failing that, split the character's full English (two
Japanese components, two English words, given first and surname last).
`build_grown` then gives each of those slots its own appended copy and
rewrites only that pointer, so every other slot still sees the shared string.
10 slots, 4 characters.

A slot that cannot be resolved is an error **only if its candidates
disagree**. 12 of the 14 ambiguous names here render the same either way
(both 宇宙魔王 are `Space Demon King`), so demanding an answer for those
would be noise; only レイ and ミーナ ever needed one.

The lesson worth keeping: `pilot-nw` is a record array, so anything keyed by
the STRING rather than the RECORD is guessing. The zukan had the same bug
and the same shape of fix.

# Battle voice lines: DATA/BTLC/SRVC.BIN

32,035 distinct Japanese strings, 445,284 characters -- about 20x all the
scenario dialogue translated so far. Short single-line barks: median 16
characters, longest 76, no line breaks in most of them.

## Format

202 sections laid back to back, each one

```
[ index of little-endian u32 offsets ][ text pool ]
```

An entry is an offset relative to **its own section's pool base**, not to
the file. 48,058 entries address 32,035 strings, so a line reused in several
situations is stored once and pointed at repeatedly. `tools/srvc.py` recovers
the sections structurally -- a pool starts where a run of preceding words all
resolve, relative to that point, to decodable Japanese.

Two escapes matter and neither may be encoded as a glyph:

* `\n` -- a LITERAL backslash and n, the game's line break. Three of Genion's
  lines use it. `build_project` splits on it and encodes the parts, joining
  with the raw bytes; encoding it outright fails, because `\` has no glyph.
* `$n` / `$l` / `$F` do NOT appear here at all -- 0 of 202 sections contain
  one. These are voiced lines, so the player-chosen name is never substituted;
  the default is baked in. Only the scenario text uses those.

## Writing: offsets are POOL-BOUNDED, so only in-place edits work

Two attempts failed before the rule was measured, and the second one measured
it. In one proven section (Genion, below) every legitimate index offset is
under `0xec0` -- exactly the pool span. An offset 216x larger crashed the game
the instant the line was reached.

That one fact replaces the earlier explanation of the FIRST failure. It had
been written up as a section-base problem: `sections()` produces overlapping
regions, so `pos - base` was computed against bases the game does not use. The
overlap is real, but it is not the cause. Both failures were the same thing --
**an offset outside the section's pool**. Garbled kanji the first time, a hard
crash the second, one root cause. Appending past the end of the file and
repointing cannot work at any file position, no matter how the base is derived.

An earlier note here claimed 102 pristine entries exceed 0xFFFF, which was used
to argue large offsets are legal. That number came from the broken parser and
should not be trusted. In the one section that is proven, offsets max at
`0xe9c`.

### In-place is the write shape that works

`tools/voice_section.py` overwrites strings inside their own slots. No index
word changes, no offset moves, the file size is byte-identical. A string ends
at its first NUL, so bytes left over in a slot are simply unused -- no padding
glyph and no ordinal shift, unlike RPW_DATA which needs `0x8140` fill.

The one rule: the encoded English must not be LONGER than the Japanese it
replaces. Every Latin letter costs one 2-byte cell and so does every kana, so
the budget works out at roughly **one English letter per Japanese character,
minus the two brackets**. Across Genion's 127 strings that is a median of 12
letters, from 4 (「いけっ！」) to 24. Tight, but barks are short by nature.

Confirmed on hardware: 20 lines written this way, no crash, nothing else in the
2.19 MB file altered.

### The budget, measured over the whole file

31,687 distinct strings across the 211 sections. At one 2-byte cell per letter
and per kana, the English that fits in place is:

    median 14 letters, mean 14.5, min 1, max 74

    1-6 letters    2,250   7.1%
    7-12          10,066  31.8%
    13-20         14,540  45.9%
    21-30          4,506  14.2%
    31+              325   1.0%

**There is no single-byte escape hatch.** An earlier note here read the first
section's index increments as odd and inferred ASCII content; that was wrong.
Counted directly, strings of odd byte length number **zero** file-wide -- every
string is uniformly 2-byte cp932. And bytes `0x2e..0x39` are escape codes into
the drawer's jump table, so the low range is reserved regardless. English
cannot be encoded at 1 byte per letter here.

### Pools can grow: the block table lives in the EBOOT (2026-09-06)

What addresses SRVC.BIN from outside is the executable. The loader (VA
0x11ab20 -> 0x11142c -> 0x114188, parser 0x111488; full notes in
`work/srvc_loader_notes.md`) takes the unit's u16 voice-bank id, reads
`tab[id]` and `tab[id+1]` from a table of **277 big-endian u32 file
offsets at EBOOT file offset 0x830be0** (276 blocks + end sentinel), and
issues a partial read of exactly that window. Inside the block everything
is self-describing: an 8-byte header with five counts, fixed-size arrays,
a cue table, then the string-offset table and the pool. Nothing in the
file records where a block starts, which is why the two shift experiments
blanked every later unit's text: the table still pointed at the old
positions.

`tools/srvc_blocks.py` parses the 276 blocks the way the game does and
rebuilds them with fresh pools of any length, keeping the block count and
order and each block's 16-byte alignment; rebuilding the pristine file with
no changes reproduces it byte for byte. `build_project.py` now ships the
rebuilt SRVC.BIN and writes the new table into the EBOOT in the same run
(it refuses to build voice without `--eboot`, since the two must never
disagree). The per-line `budget` in `source/voice` is the old slot size,
informational only; `check_voice.py` notes lines over a 36-cell display
cap instead of failing on budget. Confirmed in-game on Genion's barks after
a rebuild that moved every block.

### Growing a pool would need the header

Full-length English needs more room than a slot holds, which means relocating
sections, which means knowing what points at them. Neither the index start
(`0x151d44`) nor the pool start (`0x151fc4`) appears anywhere in the file as a
32-bit value, so the table does not store absolute offsets. Partial progress:
the file opens with a count (18947), a long `0xff000000` filler run to `0x130`,
a table of 8-byte records, and at `0x11e8` what looks like the first section's
own offset index (`0, 0x0d, 0x1c, 0x31...`).
This is unfinished.

## Linking mech -> weapon -> voice line

`tools/srvc_link.py`. There is no stored pointer to follow: a unit id (robot
record column 4) appears NOWHERE in SRVC.BIN, in either byte order. The chain
is built from the data that is there.

**wpn-1r** is 918 triples of `(unit id, weapon count, first weapon index)`,
ranges consecutive with no gaps. `(0x0E200220, 4, 2483)` is Genion's four.
This half is exact.

**Sections** are found by byte signature, not by the old structural parser: an
index word is a small offset with two zero high bytes, pool text is cp932 with
bytes >= 0x81, so a run of >=8 small words is an index block. 211 sections,
against the 202 the old parser claimed -- and it missed Genion's entirely.

**Section -> mech** is inference from content: a call-out speaks its weapon's
name, and RPW knows who owns that weapon. Three rules were forced by controls,
each of which a self-consistent check would have passed:

* Score by unit NAME, not unit id. A mech has one robot record per variant --
  Genion has ten -- and keying on the id splits a correct answer ten ways.
* Near-ties that share a weapon list are one family (Genion / Genion GAI); a
  Jaccard test separates a real upgrade form from a coincidence that scored
  close.
* **A robot's name is not weapon evidence.** Pilots address their machine
  constantly and super-robot weapon names embed the robot name, so the two
  signals are otherwise identical and the name mentions win on volume. This one
  cost Tetsujin 28 its own section, which went to Black Ox.

### What it does and does not do

Three player screenshots, none used to build the rules, all pass on the mech:

| control | section | attributed |
|---------|---------|------------|
| Hibiki / Genion | 134 | ジェニオン |
| Shotaro / Tetsujin 28 | 191 | 鉄人２８号 |
| Sousuke / Arbalest | 185 | ＡＲＸ－７ アーバレスト |

141 of 211 sections attributed. 70 remain unattributed, and a unit whose
weapons are all generically named may never be identifiable this way.

**Weapon -> line is much weaker, and the third control is why we know.** It
only works when the call-out actually says the weapon's name. Median coverage
is 25% of a unit's distinct weapon names:

    Trider G7          6 of 6     super robot, every attack is announced
    Genion GAI         4 of 4
    ARX-7 Arbalest     1 of 10    Sousuke says 「白兵戦でいく！」, never
                                  「単分子カッター」

Realistic-military characters do not shout weapon names, so for those units
there is no content signal to find. The Arbalest's one hit is ラムダ・ストライ
ク, the single attack that announces itself.


## Genion's section, and how it was identified

The first voice attribution came from outside the file: a player screenshotted
three barks while using a named weapon. All three landed in one pool.

    pool   0x151fc4 .. 0x152e84   (0xec0 bytes, 135 string starts)
    index  0x151d44 .. 0x151fc4   160 entries, 127 distinct strings

The base is proven three ways, none of them the structural parser: all 160
index words land on real string starts when read pool-relative (a wrong base
would not fit 160 for 160), three strings are screenshot-anchored, and the pool
opens on the developers' silence sentinel.

**The parser does not find this section at all.** No region it reports claims
any of the three anchored barks. It does not merely overlap -- it misses whole
pools. Treat its output as unusable.

The sentinel 「無音（本番では表示しません）…」 is NOT a section marker. It
occurs 17 times, not 202: it marks units with deliberately silent slots.

Attack call-outs speak the weapon name, so the voice table and the weapon table
have to agree:

| idx | line | weapon |
|-----|------|--------|
| 25 | 「ニトロパイク、ファイヤ！」 | Nitro Pike |
| 26 | 「インパクトダガー、セット！」 | Impact Dagger |
| 30 | 「パニッシャー、セット！」 | D Solid Punisher |
| 36 | 「グレイヴ、セット！」 | Accel Glaive |

Pre-attack lines are drawn from a random set (indices 0-21); the call-outs fire
during the animation.

Identity for the other sections is no longer open guesswork:
`tools/srvc_link.py` attributes 141 of the 211 sections to a unit by the
weapons their call-outs name, and `work/voice/sections.json` carries that
attribution with a confidence score. `tools/export_voice.py` puts the score
in every brief, so a weak match is translated as generic barks and flagged
rather than being given a name it may not own.

## The source of truth is the ISO, not the disc

`work/srvc/SRVC.BIN` is extracted from the game ISO with `tools/isoread.py`
and the build always patches from it. Patch the deployed copy instead and the
edit becomes irreversible: a line that appears twice is deduped to one
appended copy, and nothing afterwards can tell the two originals apart. That
was tried; the round-trip check caught it.

The build owns the encoding (`voice_lib.apply_docs`, called from
`build_project`), so voice lines re-encode against the current atlas every
run. Encoding them in a side script leaves them stale after any cell
reshuffle -- and cells DO move: nine shifted when stage 2 was added. It also
leaves them *absent*: the side script was forgotten once and the voice patch
regressed silently for four days. `build_project` now applies every
`translation/voice_*.json` itself, so a build cannot ship without them.
(`srvc.build`, the old append-and-repoint writer, is dead: appending crashed
the game because offsets are pool-bounded. See docs/VOICE_HANDOFF.md.)

## A section is a UNIT's voice set, and may hold two speakers

Section 124 (Genion) contains lines in two different first-person
pronouns, and in the TEXT POOL they sit in clean blocks:

```
ore     (masculine, casual)  44 lines, 0x14d416 .. 0x1503f9
watashi (polite)              6 lines, 0x15066b .. 0x150dff
```

That looks like two sections wrongly merged, and it was written up here as
a parser defect. It is not one. Read the same lines in INDEX order and the
two interleave throughout:

```
ooowooooooooooooowwowowowooooooooooooooowooooooooooooooooooooowowwooooooooooooooo
runs: o3 w1 o13 w2 o1 w1 o1 w1 o1 w1 o15 w1 o21 w1 o1 w2 o15
```

and the 626-byte gap between the two text blocks holds **zero** words that
resolve as offsets from this pool, so there is no second index hiding in it.
One index, weaving both voices through the same situations.

So a section is one UNIT's voice set, not one pilot's, and a unit with a
main pilot and a sub pilot carries both. This also explains two things that
looked odd earlier: sections come in consecutive runs of identical line
count (a pilot owns one section per unit variant -- Genion has ten robot
records), and scoring a section against pilot names finds several names
because several people really do speak in it.

Consequence for `translation/voice/genion.json`: the nine lines that sit
past the pronoun boundary are NOT misfiled. They belong to the same unit's
voice set and were correctly translated.

## OPEN PROBLEM: which unit is each section?

The file carries no speaker information anywhere:

* no prefix on the lines -- 29,914 of 30,112 begin directly with the opening
  bracket, and the 198 exceptions are developer placeholders with no bracket
  at all;
* no directory in the 4,580-byte header -- 0 of 202 pool or index positions
  appear there, in either endianness;
* no cue names in the voice audio -- `TALKZ3PS3.CPK` has 31,413 members, all
  numeric ids. (31,413 audio files against 32,035 strings is suspiciously
  close to 1:1 and may be worth pursuing.)

`tools/srvc_identify.py` scores each section against every glossary pilot
name, on the basis that pilots announce their own name and call out allies
and rivals. It is not good enough: 64 of 202 names win exactly one section,
and most winners have 2-5 mentions against an equal runner-up.

Sections also come in consecutive runs of identical line count (17/18/19 all
397 lines; 21/22/23 all 259), which matches a pilot owning one section per
unit variant -- Genion has ten robot records. So "one pilot, one section" is
the wrong expectation to score against.

**Genion is identified by content, and only Genion.** Its block names its own
systems (TS-DEMON, Vilrest, Vanargand), announces the upgraded form Genion
GAI, addresses Suzune-sensei and names the rival Gadlight. That is strong
circumstantial evidence and it does not generalise.

**The lead worth following:** Z2 runs the same engine, so a Z2 fan-translation
project may have documented this format or published a section-to-pilot
table. That would replace all of the above guessing with a lookup. It was not
checked because the session ran out of web search budget
(`CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`).

Until identity is solved, do not translate further sections: the result would
be lines attributed by guesswork.

```sh
python tools/srvc.py sections work/srvc/SRVC.BIN
python tools/srvc.py find     work/srvc/SRVC.BIN <substring>
python tools/srvc_identify.py work/srvc/SRVC.BIN analysis/glossary.json
```

# Terminology is a reference, not a literal

Names were always dynamic. The zukan, RPW_DATA, the EBOOT tables and the
draw-time hook all look a name up by its Japanese key at build time, so
changing `analysis/glossary.json` changes every one of them. Measured: edit
one pilot name, rebuild, and exactly one output file moves (`MTZKN_PT.CPK`),
one record inside it.

Prose was not. A term inside a sentence was written out literally, so a
terminology change meant editing every line that mentioned it -- `Sphere`
alone appeared 83 times across 11 files. So prose now references a term by
id and the build expands it:

```
"The $$スフィア$$ reacts to his will."  ->  "The Sphere reacts to his will."
"three $$スフィア$$s"                  ->  "three Spheres"
"a $$スフィア|lc$$ bearer"             ->  "a sphere bearer"
```

Suffixes stay outside the token, which is what makes plurals and
possessives need no syntax. `|lc` lower-cases the first letter; there is
deliberately nothing else, because a cleverer template hides the real
sentence from whoever is writing it.

## The key is the Japanese

Not a slug of the English. The English is the thing that changes, so an
English-derived id starts lying the moment a term is renamed --
`$$viachevlav-da-montewells$$` expanding to "Vyacheslav da Montewells" is
the scheme contradicting itself. The Japanese is the game's own bytes and
cannot change, and it is already the key the zukan, RPW_DATA and the EBOOT
hook all use, so a term has one name instead of two that can drift apart.
It also sits in the `jp` field directly beside the `en` being edited, and it
is language-neutral: adding a `vi` field would make the same token resolve
to Vietnamese for that build.

### Why `$$` is safe

The game's own text escapes are `$n` and `$l` -- the player-named
protagonist -- 140 of them across the script, and both are a SINGLE dollar.
**No Japanese source string anywhere contains `$$`**, and RPW_DATA's
j-strings contain no `$` at all. `$` is not in the drawable glyph set
either, so it never reaches the screen on its own. A `$n` sitting directly
against a token (`$n$$スフィア$$`) still parses correctly and is left alone.

### Discriminators

1,125 of 1,141 terms are unique by their Japanese and need nothing. Which
discriminator the rest need falls out of the collision:

```
$$アクエリオンＥＶＯＬ#series$$   12 Japanese strings name two KINDS of thing
                              (a series and its lead robot, a keyword and a
                              pilot) -- the kind settles it
$$レイ#333$$                    4 Japanese short names belong to two different
                              PEOPLE of the same kind -- the zukan entry
                              settles it
```

A numeric discriminator is a zukan entry id and an alphabetic one is a kind,
so they can never be confused. 34 terms have no `zukan_id` at all and every
one is a `series` (they come from the EBOOT table, not a zukan archive); only
two of those are ambiguous and both are settled by kind.

A bare reference to an ambiguous term is a **hard error** that names the
alternatives:

```
'レイ' is ambiguous (pilot/Ray, pilot/Rei) -- name one of: $$レイ#168$$, $$レイ#333$$
```

Picking one silently is exactly how Ray Lovelock came to be labelled Rei.

```sh
python tools/terms.py list  analysis/glossary.json スフィア   # find the token
python tools/terms.py check analysis/glossary.json translation
```

`check` lints unknown terms, ambiguous bare references, terms with no
English, malformed `$$...`, any glossary term whose own English contains a
reference (expansion is not recursive), and any term that no token can
address at all.

## Where expansion happens

In `trdata`, not in the callers -- `lines`, `records`, `entries`, `names`
and `assemble` all go through it, so no build path can bypass it. It is
armed by `trdata.use_glossary()`, which `build_project` calls before it
opens the first translation file, and a reference found with no glossary
loaded is a hard error rather than a silent passthrough. An unexpanded
`$$sphere$$` on screen is worse than a failed build.

Expansion happens before cell collection and before encoding, so the atlas
gets the letters of the expanded text and the library wrapper measures the
real width.

## Migrating literal prose

`tools/tokenise.py` rewrites literal terms into references. Its safety
property is absolute and mechanical: **a rewritten string is kept only if
expanding it again reproduces the original character for character.** So the
test that the migration was correct is not an argument, it is a build --
before and after must be byte-identical. They were, across all seven
deterministic outputs, for 4,707 references in 27 files.

```sh
python tools/tokenise.py analysis/glossary.json translation/library ...   # dry run
python tools/tokenise.py analysis/glossary.json ... --force Sphere --write
```

It matches on the English and emits the Japanese token, so the two never
have to agree by hand.

What it refuses to touch, and why it matters:

* **English shared by two terms.** No way to know which id was meant.
* **Single-word terms that are ordinary English words.** A pilot is named 安
  = `An`, and all 140 matches for it were the article. Capitalisation does
  not separate them, because a sentence starts with one. The list is printed
  on every run -- `an, angel, king, lady, president, princess, queen,
  sphere, will, zero` -- and `--force <id>` re-admits one. `Sphere` is worth
  forcing: capitalised, it is always the plot device. --skip/--only/--force
  take either the Japanese or the English.
* **`NAMES` maps, and the `jp` side of anything.** Only prose is rewritten.
* **`translation/vi`.** Vietnamese prose should reference Vietnamese terms,
  and the glossary has no `vi` field yet. Left alone deliberately.

The stages 11-30 migration matched on the JAPANESE instead: a term is a
candidate only when its Japanese occurs in that record's `jp`, which is what
makes `AG`, `PS`, `Fa`, `UN` and `An` safe to convert -- the English alone
could not tell the pilot 安 from the article. The same evidence resolves the
five names a pilot shares with its machine (`#pilot` on the speaker line,
`#robot` in prose).

It is not proof, though, and the round trip cannot catch the difference: four
records took a token whose term was the wrong one, and every one of them
still expanded to exactly the text that shipped. `姫` is the SRW-original
keyword (the Firebug's Princess), not Unicorn's `姫様` or Klan's `『姫』`;
`ゼロ` is Lelouch, not Duo's Wing Zero; `レディ` is Lady Une, not "a lady";
`ボス` is the Mazinger pilot, not Mao's `姐さん`. So read the contexts of any
term whose English is an ordinary word or whose glossary `status` is
`ambiguous` before converting it, and leave it literal when the term does not
fit -- a literal is honest, a wrong token is a rename waiting to corrupt a
line.

A false positive is not a bug today -- the round trip guarantees the shipped
text is unchanged. It is a latent one: it only misfires when that term is
renamed. That is why the run prints counts per term and stops on ordinary
words instead of guessing.

# The glossary and the library

## The library is the glossary's best source

`COMMONDATA/MTDATA/MTZKN_{KW,PT,RT}.CPK` is the in-game 図鑑: **141 keywords,
408 pilots, 253 robots**, one uncompressed CPK member per entry. It states
which series every term belongs to, which is better provenance than any
outside list -- it is how `ドロシー` can be told apart as Dorothy Catalonia
(Gundam Wing) or R. Dorothy Waynewright (The Big O).

### Obfuscation

**XOR 0x5E, with 0x00 and 0x5E left alone.** Both are fixed points of the key
(`0x5E ^ 0x5E == 0`), so skipping them means the encoder never creates a NUL
and never destroys one. That matters twice over:

* the little-endian length fields survive
* a cp932 trail byte that happens to be 0x5E survives -- `タ` is `0x83 0x5E`,
  and a naive whole-buffer XOR turns `フルメタル・パニック` into `フルメ?ル・パニック`

The header decodes to `ZKANKYWD`, which is how the key was found.

### Container

```
magic(8)  version(4)  hdrval(4)
DSIZ len(4)      -- everything from DATA onward
DATA len(4)      -- the field chunks
<tag(4) len(4) payload> ...
```

Keywords carry `WORD SRCE DSCR DSC2`; pilots `CHFN CHNN PRDC ACTR VOIC LOOK
DSCR DSC2`; robots `RBTN RBN2 PLTN PRDC HEIT WEIT LorR DSCR DSC2`. `LOOK` and
`VOIC` are binary id arrays, not text.

`tools/zukan.py` reads and writes it. **All 802 entries round-trip
byte-identical**, which is the gate that made translation worth starting.

## Glossary

`analysis/glossary.json`, built by `tools/glossary.py`:

```sh
python tools/glossary.py seed  work/lib/json analysis/glossary.json
python tools/glossary.py merge analysis/glossary.json analysis/patches/x.json
python tools/glossary.py stats analysis/glossary.json
python tools/glossary.py check analysis/glossary.json
```

Every term carries `status` (`official` / `proposed` / `ambiguous`), `src`
(where the English came from) and `note`. `ambiguous` means **never globally
replace** -- decide per scene.

`build_library.py` takes names from the glossary rather than from a
translation file, so renaming a term there changes the library and the script
together.

### Verify against akurasu, not from memory

Priority source: <https://akurasu.net/wiki/Super_Robot_Wars/Z3>. It corrected
**17 of 34** series titles against my own coinages, and its Pilot Database
caught three character-name errors that had already shipped in stage 1:

| japanese | shipped | correct |
|---|---|---|
| シン | Shin | **Shinn** (Shinn Asuka) |
| 桂 | Katsura | **Kei** (桂木桂, Kei Katsuragi of Orguss) |
| モーム | Momu | **Mome** |

Akurasu lists English only, so match the Japanese from `MTZKN_PT` -- the game's
spellings differ from the obvious ones (`キリコ・キュービィー` not `キュービー`,
`赤木駿介` not `俊介`, `リチャード・ヘンリー・マデューカス` with the middle name).

### The lint is the point of having a glossary

`glossary.lint_translation()` compares a stage's `《》` links against the
settled English. It caught `時空震動` shipping as "Spacetime Tremor" in stage 1
while the glossary had settled on "Spacequake" -- drift nobody notices until
two scenes disagree on screen.

## Scale

Library description text is **188,076 Japanese characters**: 27,577 across the
141 keywords, 100,125 across 408 pilots, 60,374 across 253 robots. Names are a
day's work; the descriptions are not. Translate `MTZKN_KW` first -- it is what
the script's `《》` links open, and it is a seventh of the volume.

Library lines are **38 cells (76 columns)** wide, not the 31 dialogue gets;
`build_library.wrap()` hard-wraps to it because the shipped Japanese is
hard-wrapped in the data rather than by the renderer.

## Bulk translation with subagents

The library is 188k Japanese characters. That is batch work, so it is farmed
out to cheaper Sonnet subagents rather than done inline.

```sh
# one brief per batch, plus a shared glossary sheet
python tools/export_batch.py work/lib/json/MTZKN_PT.json pt work/tr 40
```

Each agent gets three files and nothing else: `work/tr/STYLE.md` (the rules),
`work/tr/GLOSSARY.md` (settled terminology, regenerated from the glossary so it
is never stale), and its own `work/tr/<kind>_NNNN.md` brief. It writes one
python module into `translation/library/`.

### What the brief has to nail down

Four constraints, because an agent that guesses on any of them produces output
that builds and is wrong:

1. **ASCII only.** The renderer has no curly quotes, em dashes or ellipsis
   character. `'`, `-`, `...`.
2. **Do not wrap.** A newline means a paragraph break; `build_library.wrap()`
   does the 76-column wrapping. An agent that pre-wraps produces ragged text.
3. **Glossary verbatim.** Terms already settled against akurasu are not open
   for improvement.
4. **DSC2 only when it differs**, which the brief marks explicitly.

Each agent verifies its own file with an `ast.literal_eval` check for missing
ids, non-ASCII and syntax errors before reporting, so a bad batch does not
reach the assembler.

### Names come back too

Pilot and robot batches also return a `NAMES` dict of every Japanese name they
rendered. `tools/harvest_names.py` folds those into the glossary as
**proposed** - it never overwrites a term already marked `official` or
`ambiguous`, so an agent cannot quietly undo an akurasu-verified spelling.

The assemblers (`translation/library_{kw,pt,rt}.py`) refuse to load if two
batches define the same id, or if two batches render the same Japanese name
differently. Cross-batch drift is the obvious failure mode of splitting work
this way, so it is made a hard error rather than something to notice later.

## Ambiguity is a fact, not a bug

Splitting the library across batches surfaced something the PS2 doctrine only
warned about: **different characters routinely share an English name.** Every
one of these was caught by the assembler refusing to load because two batches
disagreed, and every one turned out to be two real people:

| japanese | english | who |
|---|---|---|
| 桂 / 渓 | Kei | Kei Katsuragi (Orguss) / Kei (Getter Robo Armageddon) |
| オルソン | Olson | Olson D. Verne (Orguss) / Olson (Gundam 00 movie) |
| レイ | Rei / Ray | Rei Ayanami (Evangelion) / Ray Lovelock (Macross 7) |
| 赤木 / 赤城 | Akagi | Shunsuke Akagi (Dai-Guard) / Ryuunosuke Akagi (FMP) |
| しげる / シゲル | Shigeru | Shigeru Takeo (Trider G7) / Shigeru Aoba (Evangelion) |
| ドロシー | Dorothy | Dorothy Catalonia (Wing) / R. Dorothy Waynewright (Big O) |

The game's own library disambiguates them all by series and id. So the rule
is: **a term marked `ambiguous` may legitimately render differently across
batches, and must never be renamed globally.** The assembler consults the
glossary and permits exactly that case; anything else disagreeing is still a
hard error.

Separately, the game spells some of its own unit names two ways
(`Ｍ６ブッシュネル` / `Ｍ６　ブッシュネル`, `Fire Valkyrie` / `F Valkyrie`).
Those are `alias` -- one thing, two spellings -- and the collision check skips
them.

## Stats and placeholders

`HEIT`/`WEIT` ship as fullwidth numerals (`５７．０ｍ`). Left alone they
render as spaced-out fullwidth digits beside tight Latin. All 506 values are
one of 17 shapes built from digits, `．`, a unit letter and `－`, so
`build_library.stat()` is a pure character-class map: `57.0m`, `---`.

`－－－` also appears in **`PLTN` on 107 of 253 robots** -- unmanned units. It is
a name field, so it never reaches the glossary; the builder converts any name
field that is purely placeholder dashes the same way.

## Verify the artifact, not the tool

Every one of the above was found by decoding the *built* CPK back to text, not
by reading the translation files. The `Framework` rename, the placeholder
pilot, the stat digits -- each looked fine in source and was wrong in the
artifact until the build was re-run after the fix. Decode what shipped.

## Translation files are JSON, not Python

They started as Python literals (`LINES = [...]`, `ENTRIES = {...}`) and were
migrated to `.json` once the pipeline was stable. The reason is not style:
**a translation file is data, but as a `.py` it was executed on load.** Every
tool read them with `exec_module`. A batch written by a subagent or a
contributor should be parsed, never run. `json.load` makes the wrong thing
impossible, and a malformed file fails with a line:column instead of a
traceback from inside the assembler.

`tools/trdata.py` is the only loader. Everything that needs `LINES`,
`ENTRIES` or `NAMES` goes through it, so the format can never be read two
different ways by two different tools.

The migration was proven, not assumed: after converting all 30 files with
`tools/py2json.py` (which uses `ast`, so nothing was executed even then), a
full rebuild produced **byte-identical** library CPKs, atlas, and pair
mapping, and byte-identical decrypted stage payloads. Only the container
changed.

`manifest.py` stays Python on purpose. It is hand-written build config that
lists inputs, never content from an agent -- the line is *config may be
code, content must be data*.

## A line's identity: there is no per-line id, so one is derived

A dialogue record is an anonymous table entry -- the game gives no line
number and no string key; it just walks the table in order. But it does give
structure, and a line's identity is built from that:

| level | key | stable? |
|---|---|---|
| event | `t_000`, `t_001` … (named tables) | yes |
| ordinal within the event | position | yes, unless a line is inserted |
| speaker | `pid_SIN` … (a real numeric id) | yes |
| text | the string | **no** -- STG0001B_00003 has 8 duplicates |

So a line is **`(file, event, n)`**, and text is never used as a key.

`tools/luarec.py` reads those out of the Lua. `tools/stamp_ids.py` writes them
into every stage record, which now looks like:

```json
{"event": "t_001", "n": 2, "pid": "pid_KEI", "sha": "3f9a1c0d2e",
 "jp": "桂\n「《破界事変》と《再世戦争》…",
 "en": "Kei\n「The 《Destruction Incident》 and 《Regeneration War》…"}
```

`patch_lua.patch()` binds on `(event, n)` and asserts `pid` and `sha` against
the Lua. That turns the one silent failure the old positional match allowed --
an inserted, deleted or reordered entry shifting every later line onto the
wrong speaker -- into a hard error. Proven by test:

| case | result |
|---|---|
| file order reversed | output **identical** -- binding is by id, not position |
| english swapped between two records, ids intact | allowed -- ids guard the binding, not the prose |
| wrong `pid` claimed for a line | **refused** |
| `sha` stale (japanese changed since translation) | **refused**: re-stamp and re-review |
| `(event, n)` that does not exist | **refused** |

Carrying `jp` alongside `en` also makes each file self-reviewable -- a
translator sees the source without opening the Lua. Unstamped records (bare
strings) still bind by position, so nothing already written breaks; re-stamp
with `stamp_ids.py` to upgrade a file.

The migration changed matching only, not output: a full rebuild was
byte-identical on every library CPK, the atlas, the pair mapping, and both
decrypted stage payloads.

## The keyword screen reads a different file

Patching `MTZKN_KW.CPK` changed nothing on the keyword page. The game reads
**`COMMONDATA/MTDATA/MTV_ALL_KEYWORD_DEF.CPK`** for it -- the zukan index is a
copy the keyword screen never opens. Found only because an English library
was deployed and the keyword page stayed Japanese. `tools/mtfl.py` reads and
writes it; `build_project.py` emits it alongside the three zukan files.

### Format (`MTFLz2_2`)

```
0x00  'MTFLz2_2' + version '0.94' + two chunk descriptors (kwrb, lkke)
      u32 count = 141
INDEX record 0:        8 u32   off_w len_w off_s len_s off_d len_d off_d2 len_d2
      records 1..140:  FFFFFFFF, id, then the same 8 u32
      then             FFFFFFFF, id(last)
TEXT  starts 16 bytes after the index; offsets are relative to that base.
      base+12 holds a verbatim 2-byte prefix (￠) + NUL; record 0 WORD at +15.
      strings are NUL-terminated, XOR 0x7A -- but the key byte is a FIXED
      POINT: plaintext 0x7A is stored as 0x7A. 33 entries contain 陽/配/越 (cp932
      trail byte 0x7A) and look corrupt without that rule.
      Every distinct string is stored ONCE; identical fields share an offset
      (「オリジナル」 once for 56 entries; 123 DSC2s share their DSCR).
      The last string is not NUL-terminated: 'ENDoMTFLs' follows it directly.
footer  plain ASCII: the converter's source path.
```

The ids are a permutation of 0..140 -- file order is not id order. The link
from a `《》` in dialogue to an entry is by **id** (`kwid_HAKAI = 0`), proven by
shipping `《Break the World Incident》` and having it open entry 0 anyway.

Gate: a no-op rebuild from the Japanese is **byte-identical** (72,989 bytes).
The dedup rule was the last piece -- without it the file came out 51 KB long.

### The library draws at a different pitch

The library body uses the SAME pair cells as dialogue (entry 49 is 927 pair
codes, zero plain) but the panel advances each cell **1.60x** further (74 px
vs 46.4). The two letters in a cell are placed for the dialogue advance, so in
the library the gap after every pair is 3.9x the gap inside it.

Measured limits, not opinions:

| approach | result |
|---|---|
| spread the two letters wider | already at the cell edge (step 20.6 = 32 - ink); no room |
| three letters per cell | even rhythm needs centres at -6.7 and 38.7 texels, outside the cell; AND 8,239 distinct trigrams vs 2,830 spare cells |
| one letter per cell | the spaced-out look already on screen |

So the library advance is a code constant, separate from dialogue's, and no
cell-content trick fixes it. Its exact value is still being measured from a
calibration entry (isolated `i` glyphs so blobs cannot merge); the three
blob-clustering measurements on real text disagreed (1.60x / 2.1x / 1.17x)
because adjacent letters merge into one ink blob at library scale.

### Library pitch, resolved

Measured from a calibration entry of isolated `i`/`ii`/`l` glyphs (blobs cannot
merge, so every blob is one letter). Three rows agreed exactly:

| | dialogue | library |
|---|---|---|
| cell pitch | 46.4 px | **45.0 px** |
| px per texel (glyph scale) | 1.092 | **1.412** |

So the advance is the SAME. What differs is the glyph draw scale: the library
draws the 32-texel cell 1.29x larger but advances it no further, so a pair
placed for dialogue (step 20.6, ink 11.4) fills the whole 45 px and butts into
the next pair. The earlier "1.60x pitch" figure was blob-merging on real text.

The fix is a second pair geometry, `digraph.LIBRARY_GEOMETRY = (16.4, 4.4)`:
the same on-screen letter spacing (23 px) once drawn at 1.412 px/texel. The
library's pairs live in their OWN cells (`pairs_lib.json`), disjoint from
dialogue's, drawn by `build_stage.build_atlas(lib_mapping=)`. Both geometries
coexist in one atlas: 993 + 1523 cells.

### Cells the game still draws in Japanese are reserved

Opening kanji cells to Latin pairs broke UI labels the game draws from its own
strings: 愛称 became 愛-v, 声優 became U,優, and the voice actor 速水奨 became
kw'w-P -- each a library pair sitting in that kanji's cell.

`tools/reserved.py` computes every cp932 code still drawn in Japanese -- UI
labels, `ACTR` voice-actor names (untranslated at that time), any untouched field --
and `free_pool(reserved=)` skips them. It mirrors `build_library` exactly:
a DSC2 filled from DSCR counts as translated, and a `－－－` pilot slot is
converted, so the set is **346 codes**, not the 2,001 a naive check gives.
With them removed the pool is 3,180 cells: both geometries fit with 664 spare.

As of 2026-09-12, `translation/library_voice_actors.json` supplies romanized ACTR
credits through `build_library._rendered`, including text pooling. The original
cast is retained. Legacy ACTR glyph reservations remain conservative to avoid
unrelated global atlas remapping; the figures above describe the original fix.
See `docs/LIBRARY_CV.md` for the catalog and scoped candidate workflow.

**Three size words must follow the text.** The header word at `0x10` and the
`brwk` chunk total are `ENDoMTFLs - 0x20`; the chunk body is `ENDoMTFLs -
0x30` (the `ekkl` index chunk keeps its size). `mtfl.build` recomputes them;
left at the original 72,796 the game read a 72 KB window out of a 178 KB
member and every keyword definition came up EMPTY on screen (the 93 KB pair
build had the same fault, never checked on that screen). A no-op rebuild of
the original is byte-identical, which is the test.

## RPW_DATA.CPK: the core string table

Unit, weapon, spirit and skill names, pilot names on the battle and
intermission screens, and battle quotes are drawn from
**`COMMONDATA/MTDATA/RPW_DATA.CPK`**, an `<mt>prod` container of 24 chunks.
`tools/rpw.py` reads and writes it.

```
<mt>prod#1 .. data#1 .. 1.00   u32 file-total  u32 file-body
<chunk-head>  name padded to 8 bytes   u32 chunk-total   u32 body-len
body
<chunk-foot>  u32   <endofchunk>
```

`chunk-total` runs from `<chunk-head>` through the end of `<endofchunk>`;
`file-total` equals the file length. Both are recomputed on a length change.
The name is padded to 8 -- reading the u32s straight after a short name
(`pilot`, `robot`, `skill`) gives garbage, which made those chunks look
corrupt until the rule was found on all 24.

Only `j-string` is text: **4,565 NUL-separated cp932 strings** (101 KB). The
other 23 chunks are binary data and are copied verbatim.

**The 23 binary chunks hold u32 byte offsets into the j-string body**
(`weapon` alone has 18,279 of them; `p-debug`/`r-debug` are clean
`(id, name-offset)` tables, 100% of their pointer column lands on a string
start). A length-changing rebuild shifted every string after the first
edit and the game crashed on boot (`Access violation reading 0x35000030`),
so `rpw.build` is **in place**: each English string is written into the
slot its Japanese occupied and NUL-padded; a string that does not fit is
refused and stays Japanese. The member length, every original string
start, and the other 23 chunks are asserted unchanged on every build.

Gates passed: no-op in-place rebuild byte-identical; swap rebuild keeps
length 504,740 B, all 4,565 original starts, and all 23 other chunks;
boots with 0 access violations, library labels intact.

### What is swapped, what is reserved

689 j-strings are settled glossary names (398 pilots, 256 units, 31 series).
`rpw.plan_all` returns every settled glossary name (398 pilots, 256 units,
31 series). `rpw.build_grown` ships all of them: a name whose English fits
its Japanese byte slot is swapped IN PLACE (NUL-padded); a name too long is
APPENDED to the end of the j-string body and its `pilot-nw` pointers (stored
little-endian offsets into the body) are repointed there. 533 fit in place,
156 append; the body grows 2,818 B.

Appending is why growth is now safe where a full rebuild crashed: **no
existing string moves**, so all ~42 K offset references (18,279 in `weapon`
alone) stay valid; only the 156 relocated names get a new offset, and only
their own pointers change. The j-string chunk `total`/`body` size fields, and
the file-level total/body, grow by the appended size; boots with 0 access
violations. The character/mech index screens draw these `pilot-nw` names, so
this is what makes those lists fully English. They are VWF letters like
everything else: the slot cannot afford 2 bytes per letter, but a name that
does not fit is appended rather than refused.

The remaining 3,852 j-strings (44k characters: skill text, weapon names,
battle quotes) stay Japanese for now; translating them frees their cells.

## Weapon names, and how wide is too wide

477 distinct weapon and attack names ship English, filling 5,388 of the 5,388
weapon name pointer slots. They are not glossary terms -- a weapon name is a
label, not referable terminology -- but they live in the same j-string body and
go through the same swap. `build_project` merges `work/tr_weapons/weapons.json`
into the name map with the **glossary winning any collision**: a string that is
both a settled term and a weapon name has to read the same everywhere.

### Two name columns, not one

The weapon record's pointer columns are w2, w3, w4, and they are different
things:

| col | what it holds | longest Japanese shipped |
|-----|---------------|--------------------------|
| w2 | one string for all 2,694 records: `-`. A placeholder, not a name. | 1 |
| w3 | the weapon-select list name | 18 fullwidth |
| w4 | the same weapon with its model designation prefixed | 48 fullwidth |

2,107 records use the same string in both; 587 differ (`ソリッドシューター` in w3,
`ＳＡＴ－０３　ソリッドシューター` in w4).

### The width rule is measured, and two earlier guesses were not

Both discarded rules failed the same way: each was a **proxy for the UI space**
instead of the UI space itself.

* *"No wider than the Japanese it replaces."* 284 of the 689 names already on
  screen fail this at 1.0x, 141 at 1.25x. 敷島 -> "Shikishima" is 2.67x; 林水
  -> "Hayashimizu" is 3.11x. Width is not conserved by translation and there is
  no reason it should be.
* *"No wider than the widest name shipping anywhere."* That 1,933 px is measured
  on the intermission unit list -- right units, wrong screen.

What is true is simpler: **wider than the original is fine, as long as it is not
wider than the UI space.** So measure the UI space. A column that already draws
an 18-character Japanese name is *proven* to hold 540 px. That is a floor on its
capacity, not a guess about it, and English measures in the same units through
`dg.line_px`. A name in both columns takes the narrower budget.

    w3   540 px  ~ 34 letters of ordinary text     403 names
    w4  1440 px  ~ 45 letters                       73 names (w4-only)

`tools/check_weapons.py` enforces this. It is conservative by construction: it
can only be too tight, never too loose, and being too tight just asks for a
shorter name.

Two caveats kept honest in the tool's own docstring. The floors are lower
bounds, so a name a few px over may still fit -- "Super Tengen Toppa Giga Drill
Break" misses by 8 px and only a screenshot can settle it. And w4's 1440 px
exceeds the 1,140 px line budget of the screen it is measured in, so that
48-character name is wrapped or drawn somewhere wider: w4 proves the game
HANDLES the string, not that it sets on one line.

The column identity is cross-checked against evidence the pointer parser did not
produce: all four weapon names visible in a player screenshot of the select
screen resolve to w3. That is what keeps this from repeating the SRVC mistake,
where the verifier shared the patch's assumption and confirmed its own error.

### Verifying the result

`tools/verify_rpw.py` re-parses the BUILT file from scratch and follows the
record pointers the way the game does, consulting none of `build_grown`'s
repoint map. The invariant is comparative -- no chunk may resolve *worse* than
before the rewrite -- because `pointer_columns` is a heuristic and some chunks
resolve at 99.7% by luck. Demanding 100% would flag those forever; demanding no
regression catches exactly the Genion failure.

Current: 4,565 -> 5,642 j-strings (+1,077 appended), 0 ordinal drift, every
chunk 100% (boost-p 99.71%) before and after, 0 regressions.

One trap when reading the output: in-place swaps pad the slot's slack with
`0x8140`, so a byte-exact search for the English finds nothing. Strip the fill
first -- 45 names looked absent until the checker did.


## Variable width: one letter per cell

The renderer advance is a per-call parameter, and `tools/eboot.py` patches
the string drawer to make it per glyph (FONT_HUNT.md, "Resolved"). With
`--vwf` the build therefore stops pairing letters: each Latin letter gets
its own cell, drawn at natural proportions from the TTF (`Face.natural`,
`digraph.raster_letter`), and the EBOOT carries a width table with one
entry per cell (`work/out/widths.json`). 79 cells replace 2,516 pairs.

```
python tools/build_project.py translation/manifest.py \
    work/TPACKPS3.CPK work/out --npdata work/make_npdata.exe --kanji \
    --vwf --ttf "E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF,22,0.5" \
    --eboot work/EBOOT_dec.elf
```

What changes in VWF mode, and what does not:

* `digraph.mixed_pairs` / `encode_mixed` switch to letters when the mapping
  is a letter mapping, so stages, the zukan, the keyword definitions and the
  EBOOT series names all go through the same code paths as before.
* **RPW_DATA is VWF too, since it can grow.** It used to keep pair cells:
  its strings were edited in place, and a pair packs two letters into one
  2-byte cell against one letter per cell for VWF, so under VWF only 36 of
  689 names still fit their Japanese slot (533 fit as pairs). `build_grown`
  appends the other 653 and repoints them, which is only safe because the
  repoint follows derived record columns now -- see "The Genion crash was
  RPW_DATA". The body grows 16.7 kB instead of 2.8 kB, and in exchange the
  713 library pair cells collapse into the 79 shared letter cells and every
  name on screen is finally the same proportional face. `pairs_lib.json` is
  now empty; `lib_mapping` only comes back if RPW ever loses the ability to
  grow.
* Line budgets are pixels, not cells: `digraph.SCREENS` holds (fullwidth
  advance, quad width, line width) for the dialogue (31, 23.3, 963) and the
  library (30, 30, 1140) in 720p px; `wrap_px` and `line_px` cost a line
  as `advance` per fullwidth character and `W/32 * quad` per letter.
  `build_library.wrap` uses it in VWF mode.
* The stub only changes cells whose width is not 32, so every Japanese cell
  and every pair cell behaves exactly as before.

**Dialogue lines with `《》` links.** The keyword highlight is not done by
the string drawer. `MtV` draws each dialogue line as PIECES from a copy
buffer (`0xa3b450+0x2b0`): the name, the text before a link, the link
(pink, via one of four mode drawers at `0x1d19ac/0x1d1a78/0x1d1c64/
0x1d1e20`), the text after it, and so on -- the loop is `0x1d16a8`. Each
piece is placed by `0x1d0708`: `x = style[+0x20] + style[+0x2e] * column`,
where `column` is a running count the loop keeps as `bytes_drawn / 2`
(`0x1d18f0`). Under a proportional font that count is the wrong unit, which
is why the pink text and the words after it drifted right (or, with a
width-table estimate, a few px left: the style step and the drawer quad do
not match exactly).

The fix keeps the loop and changes the unit. `tools/eboot.py` (`apply_kw`):

* the drawer stub (`vwf_stub`) adds every glyph advance it computes into a
  float `PEN_ACC` in a page appended to `.bss` (segment 1 memsz + 0x2000;
  the segment-0 gap is read-only, a store there faulted);
* the four `bl 0x1d0708` sites get a stub that computes y as before, x as
  `base + column >> 7`, and zeroes `PEN_ACC` before the piece is drawn;
* `0x1d18f0` (`srawi r9,r3,1; addze`) becomes `bl kw_acc_stub`, which
  returns `PEN_ACC * 128` and clears it.

So `column` is the drawer's own pen movement in 1/128 px: exact for every
piece, every font size, and unchanged in effect for Japanese. Proven on
Kei's `《Destruction Incident》 and 《Regeneration War》` line. `digraph.LINK_PAIRS`
(off) is the old fallback that put link lines on pair cells.

Debugging aid: `eboot.KW_LOG = eboot.BSS_PAGE` makes `kw_acc_stub` log
(ptr, bytes, units, 64 bytes of text) per piece into a 64-entry ring that
freezes 24 entries after the first piece containing 《; read it over
`tools/gdbbridge.py`. That is how the piece structure above was found.

A lesson from the hunt: the static caller lists from a linear capstone
decode missed two of the four `bl 0x1d0708` sites (the decoder desyncs in
places), so "no callers" from that method is not evidence.
The EBOOT gap layout is now: series strings from `0x789490`, width table at
`0x78b000`, stub at `0x78c200`; `patch()` refuses a build where the strings
reach the table.

## Typeface: Sony Rodin in the cells

The game never calls the PS3 font library (no `cellFont` imports -- see
FONT_HUNT.md), so a system font cannot be *used*; it can only be *baked*.
`tools/ttfglyph.py` rasterises the two-letter cells from a TTF, with
`digraph.raster_pair` dispatching to it when `dg.use_ttf(...)` has been
called (`--ttf path[,cap,cap_lib,dilate]`). Rodin (`SCE-PS3-RD-*-LATIN.TTF`,
the XMB face) ships in RPCS3's `dev_flash/data/font`.

Three measured facts shape it, and each was a wrong preview before it was
found:

* **The slot is bigger than the geometry numbers.** The stroke pen (3
  texels) is drawn *outside* the 11.4-texel centreline box and the CAP/BASE
  lines, so the shipping letter is really ~14.4 x 23 texels (library 11.8 x
  23). Rodin condensed to 11.4 x 20 looked small and spaced; the face now
  gets `ink_half + PEN/2` and a cap of 23 (library 19 -- that cell is drawn
  1.29x larger on screen).
* **Condense by a normal letter, clamp the wide ones.** Fitting W/M made
  every other letter ~half a slot wide. The factor now makes H fill the
  slot; W, M, m, w are clamped further individually.
* **Condensing thins stems.** At ~0.6x Rodin Bold's stems fell to ~2
  texels against the strokes' 3. Stems are widened horizontally *before*
  condensing (`dilate`, a horizontal max-filter at 4x supersampling), which
  leaves horizontals alone. 1.5 texels matches the old weight.

Letters the face lacks (composed Vietnamese) fall back to strokes per
glyph. Pair codes, reserved cells and everything downstream are unchanged
by the typeface: the zukan, RPW and EBOOT outputs are byte-identical
between a stroke build and a Rodin build; only the atlas differs.


## The Genion crash was RPW_DATA, not the EBOOT names

**The earlier conclusion in this file -- that EBOOT name strings are
content-keyed and must not be translated -- was wrong.** All three attempts
at translating them failed for a different reason, and the proof is that the
safe baseline EBOOT, with no name edit of any kind, crashed identically.

The crash reproduces with NO input at all: boot and wait. About 80-90
seconds in, the idle title sequence dies with

```
·F {PPU[0x1000000] Thread (main_thread) [0x00231150]}
   VM: Access violation reading location 0x10 (unmapped memory)
```

That makes it testable headlessly -- `rpcs3.exe --no-gui <EBOOT>` and grep
the log -- instead of asking someone to open a library entry.

Reading the fault: `0x2310f4` searches a registry of 982 twelve-byte slots
at `TOC[-0x333c] + 0x42aa0`, calling the comparator `0x5b8a9c`, which is

```
lwz r9, 0(r3)        # r9 = element->obj
lwz r0, 0x10(r9)     # r0 = obj->id      <-- reads 0x10 when obj is NULL
```

There is no null check, so any lookup that scans far enough into a hole in
the registry dies. 918 slots were filled and **slot 373 was NULL**: one
record had failed to construct.

The registry is the `robot` chunk of RPW_DATA -- that chunk is a record
array of stride 23 words holding exactly 918 records.

### Cause: repointing by blind byte scan

`rpw.build_grown` appends the names that do not fit their slot and repoints
the offsets that referred to them. It used to find those offsets by scanning
**every byte position** of every binary chunk for a little-endian u32 equal
to a moved offset. Body offsets are small numbers, so coincidences are
certain: 778 positions matched for 156 moved names, and three of them were
not pointers at all -- two in `ridividx`, one in `ridwpidx`, which are robot
INDEX tables that hold no string offsets. Overwriting them made robot record
373 fail to construct, and the hole did the rest.

### Fix: derive the record structure

`rpw.pointer_columns()` reads the ORIGINAL file and, for each chunk, finds
the smallest record stride that divides it and the word columns in which
~every value is a real j-string start (>= 98%, and at least 8 records, so a
one-record chunk cannot qualify by accident). Only those columns are
repointed. The index tables come out with no pointer column at all:

```
pilot      stride 18   809 recs   w1
pilot-nw   stride  8  1155 recs   w0 w1 w2
robot      stride 23   918 recs   w2 w3
weapon     stride 13  2694 recs   w2 w3 w4
p-debug    stride  2  1155 recs   w1
ridividx   -- no clean pointer column --
ridwpidx   -- no clean pointer column --
```

775 writes instead of 778, and all 156 moved names still keep at least one
reference. A name that had none would silently stay Japanese with its cells
already reallocated, so that count is worth checking when the data changes.

`build_project.py --rpw-limit MODE` is the bisect knob that found this:
`none` ships RPW untouched, `inplace` / `append` keep only the names that
fit or do not, `first:N` / `rest:N` take a prefix or suffix of the index
list. Combined with the headless repro above, one suspect per boot.


### The other bug on the way: NUL padding shifted every ordinal

In-place swaps used to pad the slack of a shortened name with NULs. The
j-string body is a NUL-SEPARATED list and the game indexes it by ordinal as
well as by byte offset, so that padding inserted **1,592 phantom empty
strings** (4,565 parts -> 6,157) and desynchronised every ordinal consumer
from the first shortened name onward. The slack is now filled with 0x8140,
the fullwidth space, which 339 shipped j-strings already contain (so it is
drawable and stays reserved); an odd amount of slack cannot be filled with a
two-byte character, so those names are appended instead. `build_grown` now
asserts the original ordinal count survives, and `build_project` refuses to
ship if this run handed 0x8140 to a Latin pair.

## Names the executable owns: translate at DRAW time

Some library list/index names live in the executable, not in RPW or the
zukan -- character names for story-special pilots (Hibiki Kamishiro) and
proper-noun / keyword terms. Editing that data is still the wrong move even
though it was not what crashed the game: the strings are reachable from
lookups as well as from the screen, and nothing proves which is which.

So nothing in the data is touched. `0x140f4` is the game's ONE string
drawer -- `r3` is a cp932 `char*`, walked a byte at a time, `0x00` ends the
string, `0x0a` is a newline and `0x2e..0x39` are escape codes into a jump
table. Its first instruction becomes `b NAME_STUB`, and the stub:

1. tests `r7` first. The instruction it displaced is `cmpwi cr7, r7, 0`, and
   when `r7` is zero the function returns without ever reading `r3` -- so
   the stub must not read it either, or it faults on the callers that pass
   a stale pointer with a zero count.
2. rejects anything whose first byte is < 0x81 (English, ASCII, empty).
3. walks a `{Japanese va -> English va}` table comparing the WHOLE string,
   and on an exact match puts the English va in `r3`.
4. restores its five saved GPRs and falls into `0x140f8`.

277 names, built from every glossary name that exists as an isolated string
in `.rodata`. Every comparison, hash and length the game takes still sees
the original Japanese; only the pixels differ. Layout in the mapped gap:
stub `0x78c900`, table `0x78ca00` (8 B per entry, a zero entry ends it),
English `0x78d400` up to segment 1 at `0x790000`.

These are encoded as VWF letters, the same face as RPW_DATA. The two must
agree: the lists draw hook names and RPW names in one column, so whichever
way they differ, one of them is the odd one out. They were briefly pair
cells while RPW still was.

`ヒビキ` is worth calling out. It is the protagonist's name, so the game
copies it into a player-name buffer rather than reading the table the
lists use -- which is why it survived RPW and the zukan both going
English. The hook reaches it because it matches on the string's CONTENT,
not on its address, so the copy matches too. A player who renames the
character simply stops matching and sees what they typed.

`loose_names` and `inplace_names` remain in `tools/eboot.py`, disabled. The
draw-time hook does the same job without touching a byte of game data, so
there is no reason to re-enable them.

## Loose name pointers in the EBOOT

Beyond the series (34) and keyword (141) name arrays, the executable holds
**hundreds more hardcoded name pointers** -- character names for
story-special pilots (Hibiki Kamishiro and the Aquarion EVOL cast), and
proper-noun / keyword terms -- scattered through the data segment, not in a
single table. The character-index screen draws some of its names from these,
which is why one name (`ヒビキ`) stayed Japanese after RPW and the zukan were
both English.

`eboot.loose_names` (run for every VWF build, after the series/keyword patch)
sweeps the character-detail / keyword name-table region (va 0x85e000..0x869000):
any big-endian u32 there that points at a Japanese string which is a settled
glossary/library name is repointed to an English rendering written into the
gap after the keyword stubs (`LOOSE_STR`, 0x78c800). ~384 pointers, English
deduped into ~5 KB.

The sweep is deliberately NOT the whole data segment. An earlier full sweep
also hit two regions that hold the SAME names but use them as data, not
display: the pilot roster at va ~0x795000 (a name->id lookup) and a TOC slot
(0x7dc140). Repointing those to unassigned-SJIS English broke a lookup and the
game abort()ed when opening a robot entry (Genion). The roster is already
rendered in English by RPW, so restricting to the name-table region loses
nothing visible.
Because it runs after the series/keyword arrays (already English by then), it
skips those; because it only rewrites pointers whose target is a known JP
name, a stray match still lands on a valid English string. `verify` allows
exactly two kinds of change outside the edited ranges: bytes inside the gap,
and a data word that now points into the gap. Boots with 0 access violations,
0 JP name-pointers left.

## The 登場作品 label lives in the EBOOT

After PRDC (zukan) AND the RPW_DATA copy of 機動戦士ガンダムＳＥＥＤ　ＤＥＳＴＩＮＹ
were both English, Kira Yamato's page still drew the label in Japanese. A
byte search of every data file, decompressed CPK member, XOR-0x5E zukan
member and the install cache found nothing; the decrypted executable has
it twice. **The series names are a string table in `EBOOT`**: `.rodata`
holds 32 NUL-terminated cp932 names in 8-byte slots (file 0x706ea0, VA
0x716ea0), and `.data` holds three arrays of 34 big-endian u32 pointers
(file 0x85621c / 0x8562a4 / 0x85632c), indexed by series id, NULL where a
series has no name in that context. The third array continues with the
**141 keyword names** (破界事変, 再世戦争...) that the 用語事典 list draws --
`eboot.KW_NAMES`; their English comes from the keyword library `NAMES`
merged with the glossary, so the list, the zukan entry and the dialogue
links agree.

`tools/eboot.py` translates it without moving a byte: the 27,512 zero bytes
between the two LOAD segments (file 0x779488..0x780000) exist in the file
but are not mapped; extending segment 0's filesz/memsz to 0x780000 maps
them at VA 0x789488, the English (library-geometry pairs, from the same
run's `pairs_lib.json`) is written there, and the 86 non-NULL array
entries are repointed. Verification is built in: every entry is read back
through the inverse mapping, and every byte outside the header field, the
three arrays and the gap is asserted identical.

```
python tools/eboot.py work/EBOOT_dec.elf analysis/glossary.json \
    work/out/pairs_lib.json work/out/EBOOT.BIN --pairs work/out/pairs.json
```

RPCS3 boots the plain decrypted ELF as `EBOOT.BIN` (gate: the unmodified
`EBOOT_dec.elf` installed and ran, 0 access violations). A real console
would need it re-signed (`make_fself`); not attempted. The original is
kept as `work/EBOOT.BIN.orig` (sha1 79ecd2f2...).

Because the pairs come from a specific build, **rebuild the EBOOT whenever
the atlas is rebuilt** -- a stale one decodes to the wrong letters.

Lesson underneath all of this: **a translated field is only translated if
the game reads it from that file.** Three times now the same string lived in
a second place the game actually drew from (zukan PRDC vs the EBOOT table,
MTZKN_KW vs MTV_ALL_KEYWORD_DEF). Check the screen, then find the file --
and when no data file has the bytes, the executable does.

## The COMMAND menu is a UTF-8 table in the EBOOT

0.4.1 recorded the map COMMAND menu (移動 / 攻撃 / 地上 / 精神 / 能力) as
textures, on the strength of a display test: editing all 19 cp932 copies of
移動 in the UI member changed nothing, RPW had no such string, and the
executable had "no standalone occurrence". All three facts were true. The
search was wrong in one dimension: every pass looked for **cp932**, and this
table is **UTF-8**.

`.rodata` file 0x6d4dd8.. (VA 0x6e4dd8..) holds the labels of both the unit
command menu and the map system menu (フェイズ終了, 検索, 部隊表 ...) as
NUL-terminated UTF-8 in 8-byte slots, directly beside the mangled class name
`AnalImpact::AID_CommandMenuMng`. Nothing else in the executable is UTF-8
except the confirmation dialogs that share this table (トランザム発動を
行いますか？ ...), so the path that draws it is a Unicode one, not the cp932
atlas renderer -- which is also why the menu face is an italic gothic the
atlas does not contain.

Each label has exactly one referent: the first word of a 36-byte descriptor
in `.data`, `{label, id, handler, arg, ...}` -- 0x859044.. for the system
menu, 0x8591ac.. for unit commands. A descriptor with a handler pointer is a
display record, not a lookup key, so repointing it is in the same class as
the 16-byte records at 0x790794, not the display-name arrays that abort()ed
the game.

`eboot.command_labels` (`translation/ui_eboot.json`, 40 labels) writes
English that fits the slot in place -- `Move`, `Attack`, `Ground`,
`Spirit`, `Status` all do, 33 in total -- and puts the seven that do not
(`Persuade`, `Resupply`, `Underground`, `Underwater`, `Tactical Command`,
`Transform`, `Transform Toggle`) into the mapped gap after the name-hook
strings, repointing the descriptor. Plain ASCII, not fullwidth: fullwidth
Latin is three bytes a letter in UTF-8 and would fit nothing in place. Both
edits are covered by `eboot.verify` as it stood (rodata in-place, and data
pointers into the gap).

Lesson, again: a failed search proves only that the bytes were not there **in
the encoding searched for**. When a string is absent from every cp932 table,
try UTF-8 and UTF-16 before concluding it is pixels.

### Giving the menu the VWF face

ASCII labels drew, but in the game's own fullwidth Latin at fixed pitch --
a second face beside the Rodin cells that dialogue and weapon names use. The
UTF-8 path resolves glyphs through a **65,536-entry Unicode → cp932 table**
in `.data` (file 0x7cf8c8, VA 0x7df8c8; one big-endian u16 per codepoint,
0x81A1 = ■ where unmapped, 3,864 entries mapped; found by searching for
ぁあぃい as cp932 and landing at exactly base + 0x3041·2). ASCII is ■ in
that table too, so single-byte labels reach the atlas by some other route
the table does not control.

Two-byte sequences cannot skip it. `eboot.vwf_face` points U+0100+ch --
Latin Extended-A, unmapped in the original -- at the VWF cell of each of
the 79 letters, and `command_labels` writes every label with those
codepoints (`COMMAND_FACE = "vwf"`). The atlas then serves the same Rodin
cell for `M` in the menu as in a weapon name, and the advance comes from
the same width table. Two bytes a letter means most labels outgrow their
slot: 9 stay in place, 31 are repointed (検索 has two referents; both are
labels and both are repointed). `verify` admits the 190-byte table window.
`COMMAND_FACE = "ascii"` restores the previous build.

### Centring the VWF labels

On screen the VWF face was right but every label sat left of centre, more
so the longer it was: the menu places a label at `centre - count × pitch / 2`
with the fixed 37.28/32-cell pitch and the code count, then draws it with
the narrower VWF advances. Padding with spaces cannot fix that -- each
extra code moves the start left by 0.58 cell and a narrow space only moves
the ink 0.28 right -- and a fullwidth space (U+3000, a whole cell) nets
+0.58 per pad, which for a 16-letter label means five pads and a count the
game may treat as too long.

The width table gives a better lever. The VWF stub advances by `W / 32`
cells and `W` is a byte, so one glyph can advance up to eight cells.
`eboot._CenterPads` prefixes each label with ONE invisible glyph: its cell
is a blank one (cp932 0x8840..0x889E is unassigned and empty in the atlas;
`PAD_CODES`), reached through U+0180+k in the Unicode table, and its width
byte is `32 × (pitch × (n+1) / 2 - ink / 2)` -- exactly the advance that
puts the ink's centre on the button's. Labels with the same width share a
pad; this build needs 33. The count grows by one, never more.

`COMMAND_PITCH` is the measured dialogue pitch; if a screenshot shows a
residual drift that grows with label length, that constant is what to tune.

### Left alignment, in the end

Centring worked; the user preferred left-aligned. Same pad, different
target: the pad width is `32 × (pitch × (n+k) / 2 + COMMAND_LEFT)` so
every label's ink starts `COMMAND_LEFT` (-3.4) cells from the button
centre. A short label cannot reach that far with one pad -- each code only
moves the start 0.58 cell left -- so it gets `k` pads, the extras
zero-width; "Air" needs three. Eleven distinct pad widths serve all forty
labels. The right edge of the button is about +4.4 cells, which is what
turned 戦術指揮 into "Tactical Cmd" and 変形トグル into "Auto Transform".

## UI labels through the draw-time hook

The unit / pilot / mech ability screens (ユニット能力 ...) and the list
screens take their labels from the AIDDATAPACK UI member (FSSA), cp932,
some as one multi-line string (`格闘\n射撃`, `移動\n装甲値\n運動性\n照準値`).
Nothing there can be lengthened or moved (0.4.1). But the screen was
already showing "Melee" over 格闘 -- a glossary term the **draw-time name
hook** matched by content after the string reached the drawer. That is the
route: the hook compares whole strings and swaps the pointer, so a UI
label of any length is one table entry away.

`translation/ui_hook.json` holds them (SRW V's terms: Foc, CQB / RNG / SKL /
DEF / EVD / HIT, Move / Armor / Mobi / Sight, Unit Info...). `name_hook`
loads it after the glossary, puts UI entries FIRST in the table so a
whole-string match beats the glossary (格闘 alone is the stat label
"CQB", not "Melee"), and for Japanese the executable does not hold copies
the cp932 bytes into the gap so the stub has something to compare. The
table's string area moved from 0x78d400 to 0x78d800 to hold 448 entries.

What this cannot do: anything the hook cannot see. 空陸海宇 and the single
空 / 陸 / 海 / 宇 column heads are one-cell slots beside a rating letter,
so "Air" would collide; they stay. Strings drawn by something other than
0x140f4 (textures, the tab letters P / R / W) are out of reach.

## Spirit commands and pilot skills: RPW labels

The Pilot Info lists (Skills, Spirit) are RPW_DATA j-strings -- chunk
`spirit` (100 strings: names, `＋` variants, one-kanji abbreviations and
the effect descriptions) and `sk-pri` (74 skill names). They go through the
weapon-name channel exactly: `translation/spirits.json` and `skills.json`
are `{jp: en}` like `weapons.json`, `build_project.load_labels` merges them
below weapons and the glossary, `rpw.plan_all` swaps every whole j-string
that matches, and `build_grown` appends and repoints what does not fit --
its pointer scan covers every record array with derived columns, these
included. The level suffix (援護攻撃Ｌ２) is formatted by the game around
the swapped name.

The j-string body is **deduplicated**: 突撃 serves the weapon "Charge"
and the spirit "Assail". The initial global swap gave both the weapon's
name. `rpw.spirit_name_overrides` now appends each Spirit full name and
repoints column 1 of its `spirit` record, so Spirit names follow
`translation/spirits.json` independently of weapon precedence. Abbreviations
and effects are not repointed. Descriptions quoting Spirit names are
translated through the draw-time hooks.

The same labels are added to the EBOOT hook list, so a skill or spirit
name drawn from an executable or FSSA string (menus, battle popups) reads
the same as the list.

### Mech ability names are hook entries, not RPW

`Ｄ・フォルト` is not a j-string: RPW holds only the ability *descriptions*
(which quote the name in 「」). The standalone name lives in the
executable's cp932 tables (a cluster at VA 0x6ee740: Ｉフィールド,
Ａ．Ｔ．フィールド, ＨＰ回復（小）... 55 names), in the UI member, and in
the zukan -- and the Mech Info list draws it through 0x140f4. So
`translation/abilities.json` is a second content-hook file; `load_ui_hook`
reads it after `ui_hook.json`. Two names carry a trailing fullwidth space
in the data (ジャミング機能　, ラムダ・ドライバ　) and are listed both ways.

Enumerate a family like this by finding one standalone member as
`NUL + cp932 + NUL` in the executable and dumping the NUL-separated
neighbourhood: the tables are contiguous and the names come in the order
the game lists them.

## The EXT segment: room in the executable

The gap between the two LOAD segments is 27,512 bytes and it was full by
the time the ability names arrived: hook table 432 of 448 entries, strings
10,992 B wanted against 10,240. Nothing else in the file is both mapped and
free -- extending segment 1's `filesz` would overlay its BSS with the
section-header table, and BSS itself is not file-backed.

The ELF does carry three placeholder `PT_LOAD` headers (vaddr 0, filesz 0,
memsz 0, at indices 2-4). `eboot.add_segment` rewrites the first as a
read-only segment at `EXT_VA` 0xc00000 (above segment 1's grown BSS, which
ends at 0xbfef80), `EXT_SIZE` 64 KB, `p_align` 0x10000, backed by zeros
appended to the file at the next 64 KB boundary (0x860000). The hook table
(`NAME_TBL`, 2,048 entries) and `NAME_STR` -- the hook's English and copied
Japanese, the 0x790794 menu labels, the COMMAND labels -- all live there;
the stubs stay in the gap and reach it through lis/ori. `verify` checks
that the file grew by exactly the segment, that the only header change
beyond segment 0's is that placeholder, and admits data pointers into the
range. `EBOOT.BIN` is 8,847,360 bytes now.

Everything that allocates strings goes through `_off` / `_va`, so moving
`NAME_STR` again is a constant change.

## Terrain in one cell: tiny words

The Pilot Info training panel dynamically overrides its first two stat labels.
FSSA `格：\n射：` is only a template; replacing it or hooking its separate
lines does not catch the active source. At VA 0x31B32C and 0x31B34C the code
loads TOC -0x1A30/-0x1A2C (pointers to VA 0x720890/0x720898) and calls
0x529FC to set rows 0/1. `eboot.training_stat_cells` replaces those two
standalone cp932 characters in place with U+E018/E019 tiny CQB/RNG cells.
Each eight-byte slot retains its six NUL bytes; the adjacent 歌/ー strings
used by the alternate song-pilot branch are unchanged.

空 / 陸 / 海 / 宇 sit in one-cell slots -- beside a rating letter in the
ability screens, at double pitch in the Pilot Info row, formatted with
－ in the movement-type string. No letter string fits a cell, but a whole
word drawn small does, which is how SRW 30 shows them. `digraph.TINY_CELLS`
maps five private-use characters (U+E000..E004) to cells in cp932 row 0x86
(0x86B8.., unassigned and empty in the atlas), and `raster_tiny` draws
"Air", "Grd", "Wtr", "Spc", "Und" into them from the same Rodin TTF at
`TINY_CAP` 11, centred, baseline lifted `TINY_LIFT` texels so the word sits
on the kanji's body. Their width-table entry stays 32, so they advance at
the caller's pitch exactly as the kanji did -- that is what keeps the
ratings aligned. `build_stage.build_atlas` draws them on VWF builds and
refuses if the letter pool ever claims one of those codes.

Hook English uses the private-use characters directly (`encode_letters`
turns them into the cell codes through `_raw_bytes`). The movement-type
string is formatted per unit, so `ui_hook.json` lists all sixteen
combinations of 空陸水地 / －.

The Unit Info movement row can still bypass those whole-string entries:
the game assembles it from numeric movement points, punctuation and individual
type labels. `eboot.movement_type_cells` therefore replaces the isolated
空 / 陸 / 水 / 地 in three complete four-label formatter tables at file offsets
0x6D6140, 0x710EA0 and 0x711258. Each eight-byte slot contains two cp932 bytes
and six NULs; the replacement preserves that layout and uses the existing
Air / Grd / Wtr / Und cells. It runs only with the VWF atlas and verifies
every original and replacement slot. No global kanji atlas cell is changed.

`MOVEMENT_EXCLUSIVE` also patches the seven dedicated-mode strings in those
UI clusters (空専用 / 陸専用 / 空水専用 / 水専用). Air / Grd / Wtr plus
the cap-11 Only glyph (U+E017, cp932 0x86CF) replace them with a final blank
cell, preserving the original byte length, terminator and cell count.

The MAP-DATA pilot panel's 17 spirit-status abbreviations use the same fixed-
cell technique for a different reason: the game colours a status by cell, so
letting English change the cell count would move the highlight. The exact
17-kanji FSSA row is patched in place by `ui_aiddata.json` to U+E005..U+E015
(cp932 0x86BD..0x86CD). Each cell contains a unique two-letter, mixed-case
label (`Va So Fs Al Pe Wa Fo St Ac Ze Me Sn As Fu Lu Ga Di`) at cap 16 and
baseline 23. The
pair uses a two-texel gap between the visible letter bounds. Narrow pairs
retain their natural widths; pairs wider than 28 texels are condensed to fit,
then centred in the fixed 32-texel cell. This replaces minimum-width tracking,
which spread Ft/Ef/Cf apart and squeezed Me together.
`Fo` is Focus, `Lu` is Luck, `Fu` is Fury, and `Wa` is Wall. Names follow
the user's reference in `docs/SPIRIT_NAMES.md`; `Fs` is Fighting Spirit
(闘志), while `Ze` is Zeal (覚醒).

The enemy battle-preview strip has a different 17-cell layout:
`熱魂闘閃不鉄集必加覚手狙突直／乱分`. Its two FSSA copies are also
patched in place, retaining the fullwidth slash in cell 15. Disrupt uses
the existing cell with its updated `Di` label; Analyze uses `An` at U+E016 / cp932 0x86CE with
the same cap-16 spirit styling.

A hook lesson from the same screen: the stub's "not Japanese" test was
`first byte < 0x81`, which threw out labels that start with a newline.
`\n\n\n移動\nタイプ` never matched until a leading 0x0a was let through.
When a hooked whole string does not swap, check its first byte before
anything else.

## The other UTF-8 strings: ui_utf8.json

The COMMAND menu was the first UTF-8 table found; it is not the only one.
`.rodata` holds about 930 standalone UTF-8 strings: window titles (戦闘結果,
レベルアップ, エースボーナス...), the intermission menu, confirmation
prompts, the manual, battle-dialogue short names. They draw through the
Unicode path, which converts to cp932 by table and never reaches the hooked
drawer -- so a label that exists both as cp932 in the UI member and as
UTF-8 here (エースボーナス) swaps on one screen and not the other.

`translation/ui_utf8.json` is the second input to `eboot.command_labels`,
run with `window=False`: every standalone occurrence in `.rodata` outside
the command table is translated -- in place when the UTF-8 fits the slot,
otherwise into the EXT segment with every `.data` referent repointed -- with
the VWF face and no pads, since these draw wherever the game places them.
The command table's window is now anchored on the class name
`AID_CommandMenuMngE` just before it, which no pass translates; the first
version anchored on フェイズ終了 and the second pass could not find it once
the first had written "End Phase" over it.

`vwf_face` and the label passes are idempotent, so more UTF-8 files can be
added the same way; `verify` admits pointers into the EXT range.

## Prefix hooks: titles the game composes with their body

The Pilot Info ace-bonus title stayed Japanese after its cp932 copy was
hooked AND its UTF-8 copy translated, with the reinstall folder proving
the game had booted the new build. The other hooked labels on that screen
swap, so the drawer is the hooked one; the bytes were searched in every
encoding, so the string is the known one. What differs is the CALL: the
box is drawn as one string, `エースボーナス\n<description>`, so its content
is never equal to the entry.

`name_stub` now understands prefix entries. Bit 31 of the English pointer
flags one (`"prefix": true` on the line in `ui_hook.json`,
`eboot.UI_PREFIX`); in the compare loop the entry's Japanese running out
is a hit for a flagged entry even if the subject continues. On that hit
the stub copies the English, then the remainder of the subject, into
`HOOK_SCRATCH` (the first 4 KB of the BSS page the keyword layout already
owns) and hands the drawer that buffer. Exact entries still require the
subject to end. The stub grew to 296 bytes, which is fine now that the
hook table lives in the EXT segment and the gap after 0x78ca00 is free.

When a hooked label will not swap and its bytes are right, suspect
composition before anything else: title + body, name + suffix, and
anything drawn in two colours from one call.

## Joined hooks: headings typeset as pieces

Intermission's Team Setup button is a reordered case: the FSSA strings are
`チー\0\0編成\0\0ム\0`, although widget positions read `チーム編成`.
The four selected/unselected copies begin at 0x60BD4, 0x60BE4, 0x60D98,
and 0x60DA8. Its joined key is therefore `チー編成ム`, the stored order,
not the visual order. Matching the raw sequence suppresses the later pieces
without globally translating `チー`, `編成`, or `ム`.

The ace-bonus heading beat every text mechanism in this file: its cp932
copy was hooked, its UTF-8 copy translated, prefix entries covered a
composed title, and the screen still said エースボーナス -- in a face with
odd letter-spacing. The spacing was the answer. The game TYPESETS that
heading: it copies it into a buffer as tiny NUL-terminated pieces,
`エ\0\0ース\0\0ボー\0\0ナス\0`, and draws each piece at a computed x. Every
piece is a whole string to the drawer, so no entry for the heading can
match, and an entry for a piece (ース) would be a global menace.

Two debug steps found this, both worth keeping. (1) A prefix entry for the
single character エ -> `[` showed the heading passes through the hooked
drawer at all. (2) With RPCS3's GDB server answering nothing but its
handshake (reads time out on this build, 0.0.42), `eboot.HOOK_HEXPROBE`
turns the stub into a memory viewer: any drawn string starting with two
given bytes is replaced by the hex of its first 16 bytes, drawn as VWF
letters -- the screen shows the buffer. A 28-space lead-in clears the
original, which the un-hooked later pieces still draw over the probe.

`"joined": true` in `ui_hook.json` is the fix (bit 30 on the entry's
English pointer): the compare skips runs of up to eight NULs in the
subject, so the entry's Japanese matches the whole typeset buffer. The
first cut ZEROED the buffer on a hit -- and the heading vanished, because
the matching call was a MEASURE pass; the draw calls then read zeros. So
the stub keeps the buffer intact and remembers the matched range in BSS
(`HOOK_JSTATE`): the first piece re-matches on every pass and draws the
English once, any subject strictly inside the remembered range answers
with an empty string, and a first-piece call that no longer matches drops
the stale range. Content-exact, so no collateral on other typeset
headings.
