# Battle voice-line translation — handoff

The subtitle lines drawn during battle animations live in
`DATA/BTLC/SRVC.BIN` (2,192,672 bytes). One unit's voice set = one
section; translating proceeds section by section. Genion's set (126
lines, everything Hibiki and Sensei say from that cockpit) shipped first
and is the worked example for everything below.

**Scale:** 211 sections, 50,919 index entries, **31,670 distinct lines**
to translate. A section is 100–860 lines; a repeat costs nothing, because
one stored string serves every entry that points at it.

## File model (derived, then proven in-game)

    212 sections, each:  [ index of LE u32 offsets ][ cp932 text pool ]

- An index word is an offset **relative to its own section's pool base**.
- ~48,000 index entries address ~32,000 distinct strings — a line reused
  by several situations is stored once and pointed at repeatedly
  (`"shared": true` in the dumps). One translation serves all its users,
  so only the first entry holding a string is ever translated.
- Section numbering is `srvc_link.sections()` order (the canonical
  parser; `srvc.sections()` is older, finds 202 overlapping regions, and
  is superseded — do not derive bases from it).
- Genion = **section 134** in this numbering (`source/voice/134.json`).
  Older commits say 125/124 — that was the previous parser's numbering.
- Line breaks inside a line are a literal `\n` two-byte sequence
  (backslash + n) that the game's text parser consumes. Pass it through
  raw; never encode the backslash. It costs **one cell**, not two.

## The law: write IN PLACE. Never append, never move.

Two failures bought this rule:

1. **Append-and-repoint corrupted barks it never selected** (reverted in
   `bea5636`). The verifier resolved entries through the same section
   mapping the patch used, so it confirmed the patch's own mistake — a
   player screenshot caught it. Verification must never share an
   assumption with the writer (the independence rule).
2. **An appended offset crashed the game outright** (`ce7d83c`).
   Measured: every legitimate index offset in the proven section is
   under 0xec0 — exactly the pool span. Offsets are pool-bounded;
   pointing past the pool is not an option, full stop.

So: the English for each line is encoded into **the Japanese line's own
byte slot**, padded as needed, file size unchanged. Outside the chosen
slots, not one byte may differ from pristine — that is byte-verifiable
without trusting any parser.

## The pieces

| thing | where |
|---|---|
| pristine file | `work/srvc/SRVC.BIN` (and `work/patch_orig/SRVC.BIN`) |
| per-section JP dumps | `source/voice/NNN.json` — `{i, jp, shared, budget}` per line, via `tools/extract.py` (`do_voice`) |
| section geometry | `work/voice/sections.json` — `{sec, index, count, pool, unit, pts}`; the writer proves it before every write |
| section → unit/pilot identity | `work/voice/sections.json`, `pilots.json`, `mech_pilot.json`, `clusters.json` |
| identity tooling | `tools/srvc_link.py` (call-out speaks a weapon name → RPW `wpn-1r` → unit; evidence, not lookup), `tools/voice_pilots.py` (3 independent links; sections sharing ≥50% of lines share a pilot — Black Ox and Tetsujin are one set) |
| the brief | `tools/export_voice.py <sec>` → `work/voice/brief/NNN.md` |
| the checker | `tools/check_voice.py <answer or doc>` — budget, drawable charset, coverage |
| the merge | `tools/merge_voice.py <sec>` → `translation/voice_NNN.json`, refuses a failing answer |
| the writer | `tools/voice_lib.py` (geometry, proof, in-place write, independent verify) |
| one-section CLI | `tools/voice_section.py <doc.json>... [--out work/out/SRVC.BIN]` |
| the worked example | `translation/voice_134.json` (was `voice_genion.json`) |

`budget` = cells available in the slot after the 「」 pair (2 bytes per
cell): one per letter, one per `\n` break. `check_voice.py` counts it,
`voice_lib` refuses anything longer — compress, never truncate. Lines the
developers left as placeholders (`－－－…`, or one that says outright
`無音（本番では表示しません）`) never reach the screen; the brief omits
them and they stay Japanese.

## Wiring — it is in the build now

`build_project.py` applies **every `translation/voice_*.json`** itself,
in place, after the atlas step. Two reasons it cannot live anywhere else:

- the letter encoding comes from that run's `work/out/pairs.json`, and
  atlas cell codes shift between builds, so pre-encoded English is
  garbage by definition;
- the side script was forgotten once and the voice patch regressed
  silently for four days (caught 2026-09-01 by hashing every copy). A
  build that cannot ship without the lines cannot repeat that.

`voice_section.py` remains for single-section iteration, and produces
byte-identical output to the build (verified against the shipped Genion
patch). It is no longer a required step, and `translation/voice/` — the
dead append-era channel — stays empty; do not resurrect it.

## Adding a new section

1. Pick a target from `work/voice/pilots.json` / `sections.json`, ranked
   by `pts` (the weapon-match confidence) and line count.
2. `python tools/export_voice.py <sec>` writes a self-contained brief:
   identity and its confidence, the shipped English for every weapon its
   call-outs name, the glossary terms that actually occur, and every
   distinct line with its budget.
3. Brief a subagent with it. The answer is a bare `{entry: english}`
   object at `work/voice/answer/NNN.json` — order-free, so two answers
   can never overwrite each other's work.
4. `python tools/check_voice.py work/voice/answer/NNN.json` must report
   0 problems (the translator runs this too, and iterates, before
   reporting back).
5. `python tools/merge_voice.py <sec>` publishes
   `translation/voice_NNN.json`, re-running the checks first and
   refusing to write on any problem.
6. Build → deploy (`tools/deploy.py work/out`; killing rpcs3.exe first
   is authorized). Verify on screen; a battle with the unit plays its
   set immediately.
7. Changelog, same session, every change (CLAUDE.md rule). Never commit
   game bytes — translations and tools only.

**A confidence score is a suggestion, and the lines outrank it.** Section 8
carries `unit: Strike Freedom Gundam`, pilot Kira Yamato, on a weapon-match
score of 7.5 -- and its lines are a wisecracking Firebug mercenary naming
Beck, Gates, Kang Yu, Mithril, Bonta-kun, Tessa and Kumen: Full Metal
Panic, nothing to do with SEED. It was caught by reading the section, not
by any check. So: read enough of a section to recognise the speaker before
adopting the register the table implies, and when the content disagrees,
translate the content, clear the doc's `unit`, and record the evidence in
its note. Scores in the 1-8 range have matched on generic weapon names
(every "Gundam Mk-II" at 2.0 is suspect); a screenshot is still the only
authority.

**Three units are weapon-name magnets and their attributions mean nothing.**
`Gundam Mk-II` (25 sections), `Strike Freedom Gundam` (15) and `Nu Gundam`
(10) hold 50 of the 141 attributed sections between them, because a beam
rifle or a vulcan is carried by dozens of machines and srvc_link matches on
the name. Both Strike Freedom sections translated so far were something
else entirely: **8** is a Full Metal Panic mercenary (Firebug, Beck, Gates,
Bonta-kun) and **141** is a Branch robot-mafia goon from Tetsujin No. 28.
`export_voice.py` prints DO NOT TRUST on all 48 of those briefs still to
do; work the speaker out from the lines and **record what you concluded in
`analysis/voice_identity.json`**, which `export_voice.py` and
`merge_voice.py` both prefer over the weapon match. A section read once
stays read: the brief then opens with the corrected identity, and the
published doc carries it with the evidence.

## Twenty groups of sections repeat each other

**4,115 of the 31,670 lines are repeats of another section**, in 20 groups
of two or three: 17/18/19 are 197 of 198 identical, and so are 21/23/25,
117/118/119, 148/149/150, 155/156/157, 204/205/206 and others.
`work/voice/clusters.json` has always recorded them.

`tools/voice_propagate.py` carries a translated section's English to its
siblings, matching lines by their **Japanese text, never by entry number** —
the numbering differs between sections of a group, the strings do not — and
leaves anything unmatched for a translator. Run it after every merge.
Translating a repeat a second time is worse than wasted effort: it puts the
same unit on screen saying the same Japanese two different ways.

The base is still proven three ways before a byte is written, none of
them the parser that suggested it: (a) all COUNT index words must resolve
to real string starts inside the section's own pool — a wrong base does
not fit N-for-N, and `voice_lib.prove` refuses to write if it does not;
(b) identity is tied to outside evidence (a screenshot of a bark while
using a named weapon, or an srvc_link weapon match with a clear margin —
the brief prints the score, and a weak one is translated as generic barks
and flagged); (c) the pool typically opens on the silence sentinel.

## Verification checklist per section

- `check_voice.py` clean, and the writer reports the file size unchanged.
- `sha1` differs from pristine only after the writer runs; a byte-diff
  outside the chosen slots must be empty (`voice_lib.verify` asserts
  exactly this, plus that no index word anywhere moved).
- In-game screenshot of at least one bark from the section (the only
  authority on section identity — screenshots created this pipeline's
  every proven fact; parsers only suggested them).
