# Deployment dialogs and map-pin captions

## Scope (2026-09-11)

User requested the deployment confirmation screen and every location label in
the same category as the Japan-map `第２新東京市` caption. This changes source
translations and build tools, not screenshots. No emulator/save files are
modified. Live-game visual confirmation remains pending.

## Deployment coverage

`translation/deployment_hook.json` contains seven distinct strings: two prompts,
team/battleship deploy responses, change map positions, wait, and return to
preparation. `tools/deployment_layout.py` audits all 12 original widget references
(10 options plus two prompts), five related headings, two remaining-team labels
and three help rows. It checks source text and flags before editing. Numeric
counter records are byte-identical; only their adjacent labels become `Left:`.

The dialogs retain their original Japanese strings as hook keys. The live game
centers those original strings first, so the translation receives a pad based on
the original Japanese count, not English length. Seven unused CP932 glyphs
0x8461..0x8467 are verified blank in both original font layers. PPC simulation
tests every old and new pad at multiple pitches and glyph widths.

The additional pad-bank dispatch makes VWF 264 bytes. The first keyword helper
was moved from 0x78c300 to 0x78c310 inside verified zero padding; its 68 bytes still
end before the next helper at 0x78c400. Branches are generated from the new
address. Non-overlap checks remain mandatory.

## Map category coverage

All 334 EFFPS3 archive members were inventoried for texture headers. The complete
Japan/world/space location-caption family contains 83 assets:

- Japan: members 92..113 (22).
- World: members 116..156 (41).
- Space: members 167..186 (20).

These are asset IDs, not stage IDs. All 83 original captions were visually read;
all 83 translated before/after crops were visually reviewed. Member 94 is
`Neo Tokyo-2`. Member 96 now uses `Neo Tokyo-2 - Jindai High School`, replacing
the older isolated caption's inconsistent `Tokyo-2` spelling.

The catalogue is `translation/map_locations.json`; build-time glossary tokens
keep shared terminology consistent. Source SHA-256 fingerprints, GTF offsets,
texture dimensions, caption rectangles and animation-sample counts are in
`translation/map_location_sources.json`. Eight missing location terms were added
to the glossary with provenance; provisional names are marked as such. In
particular, Barueyoruzuru follows existing stage 53 prose, not a verified official
English romanization.

`tools/map_locations.py` only replaces the caption's swizzled ARGB pixels.
Original left/right anchoring is retained. Text keeps its nominal height and
long names are horizontally condensed to fit. Every rectangle is 392x24 at
(0,104), except member 174's 440x24 strip. Member 148's animation uses additional
sample-mode variants; its 177 matching samples are explicitly fingerprinted.
No UV coordinates, vertices, timing, glow or map geometry are changed.

The packed-archive regression checks all 83 resulting captions and compares every
byte outside their rectangles. All other compressed member payloads remain
identical except the previously supported scenario-title assets (87..91) and
version footer (296), which have their own checks.

## Verification and output

- `python tools/test_deployment_locations.py`: eight tests passed, including
  actual PPC centering, helper space, role separation and caption isolation.
- Original font blank-cell checks passed in both atlas layers.
- All 83 caption source/hash/layout checks and before/after previews passed.
- Focused emitted-binary checks: 11,160 PPC centering cases, 199 dialog hooks,
  186 blank glyph cells in both built layers, and keyword branch targets pass.
- Full suite: 33/35 pass. The two failing mission-condition tests reach an
  existing source inventory assumption: STG0068's mission preset is member 3,
  not member 1. The audit scans all extracted stages, including this source
  outside the current build manifest. Neither failure concerns new captions.
- The complete build also stops at that mission-source audit. Candidate files
  are in `work/out_0.6.3`, but **no successful build was stamped**; counter stays
  0.6.2. Do not deploy this candidate or advertise it as a completed 0.6.3.
- `python tools/check_deployment_locations.py --out work/out_0.6.3` separately
  passed against the packed output, including all 83 captions and all protected
  bytes/member payloads. It never skips or overrides the full-build gate.
- Runtime checks pending: both team/ship dialogs, live remaining-team counter,
  long right-anchored map labels and animated map transitions.

Local audit assets and build logs: `work/deploy_locations/` (ignored).
No ISO is created by this work, and no existing release is replaced.
