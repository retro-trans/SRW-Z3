# Power-part description review

Reviewed all 69 parts against [Akurasu's Z3 Parts table](https://akurasu.net/wiki/Super_Robot_Wars/Z3/Parts)
on 2026-09-11. The descriptions use original concise wording, retaining the
in-game effects and checking them against the reference. Part names are not
renamed. Existing Spirit names come from `translation/spirits.json`.

The original RPW has 300 unique description strings across those 69 parts
(full help, compact help, consumption and DLC variants). All are covered;
299 English variants changed, one was already identical to the new wording.
The catalog is `tools/parts_description_catalog.py`; the two description JSON
files are generated outputs. The historical `unshipped` filename does not
mean these descriptions are withheld: they ship through the display hook.

## Corrections and constraints

- Range bonuses exclude both MAP weapons and range-1 weapons. The old
  translations incorrectly included MAP weapons in every affected family.
- Auto-Defenser spells out pilot status immunity and the targeting/placement
  penalties instead of the opaque `no Focus-Fire/Placement` shorthand.
- Damage Avenger describes missing HP and gives the 60%/20% example.
- Gate Jumper includes movement past enemy units; defensive systems retain
  their thresholds, probabilities, EN costs and team effects.
- Recovery, consumable limits, terrain targets, stacking and main-unit
  requirements are preserved across the short and long variants.
- F Bomber follows Akurasu's second deployed player turn, rather than the
  original Japanese description's first turn. This changes help text only.
- SP Getter retains the Japanese source's precise simultaneous-team-kill
  restriction; Akurasu's “multiples” is nonspecific. Fixed-movement unit
  exceptions in the Japanese terrain-module descriptions are also retained.
- Miracle Fragment lists all nine effects, including in the previously vague
  one-line source variants. Names resolve from the current Spirit dictionary.

All variants, including DLC, are wrapped to at most three lines and 540 native
pixels per line at the candidate's 28px glyph size. This is a conservative
budget within the screenshot's D-Trader description panel, not a live-game
render verification. No ellipses or truncated effects are used to pass it.

## Rebuild and verify

Run `python tools/build_parts_descriptions.py` to inspect the dry run, then
`python tools/build_parts_descriptions.py --write` to regenerate the JSON.
Use `--out` to select the font mapping/widths from the intended build.
Normal EBOOT generation consumes `translation/parts_desc_hook.json`.

This file disables automatic Japanese/English per-line pairing: translated
prose is newly wrapped, so aligning arbitrary line breaks creates incorrect
standalone fragments. Other UI files retain their existing pairing behavior.

`python tools/test_parts_descriptions.py` checks all source variants, effect
regressions, DLC markers, valid glyphs, measured widths, exact installed
hooks and unchanged RPW descriptions. Candidate checks require local game
data and the pre-patch backup.

`tools/patch_parts_candidate.py` applies an isolated delta to the existing
unstamped candidate. It requires the effective pre-edit hook snapshot and
defaults to a dry run. For this batch it replaced 299 complete hooks, removed
207 obsolete generated fragments, and appended 17,534 bytes of text. There
are 3,646 lookup entries afterward. Executable instructions, voice tables,
file size and all RPW data are untouched. Backup:
`work/parts_descriptions_EBOOT.before.bin`.

Never swap RPW boost-p description strings directly: that path corrupts boot.
No release, deployment, ISO or build stamp was changed by this review.
