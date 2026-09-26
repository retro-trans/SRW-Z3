# Stage reward reports and Counter-family labels

Local candidate update, 2026-09-11. Not deployed or live-render verified.

The Scopedog report is a quoted MESSAGE in a stage preset's GIFT table,
not a normal dialogue record. `tools/gift_reports.py` inventories nonempty
quoted messages in all extracted `work/lua*/*preset.lua` files as CP932,
excluding comments. All 22 distinct messages / 87 occurrences are covered.
No preset data, reward values, conditions, or stage logic are changed.

Covered family:

- Scopedog Round Mover, Lightweight Configuration, and Assault Configuration
  unlocks: three messages in five stage presets (10, 16, 20, 58, 63).
- Auxiliary GN Drive, Super Repair Kit, and Chogokin Z awards; 50,000 funds.
- AG bonuses: 50, 100, 150, 200, 300, and 1,000 Z Chips, including both
  leading-fullwidth-space variants actually present in the source.
- Sub Orders / D-Trader availability and all three upgrade-refund notices.

Example report:

    Scopedog conversion equipment:
    Received Round Mover.

`translation/gift_report_hook.json` has 39 exact whole-message and explicit
line keys, with automatic line pairing disabled. Original line boundaries
are retained; known proper names are glossary references, and part names
are read from `translation/parts.json`. All expanded lines fit 1,000 pixels
at the native 28-pixel report font (the box is wider than this).

The centered drawer measures Japanese before the English draw hook runs.
`president_report_layout.py` now also recognizes 18 exact single-line reward
keys. It reads their English from the existing lookup table, measures the
live font advance, and retains the previous President handling. All other
calls use the original path. Existing AG lines with command-layout centering
pads are excluded to avoid double correction. Cave/data limits remain the
same; no new font cells or scratch areas are allocated.

Map-battle Counter was already translated in the candidate. Verified its
packed pixels and completed the adjacent Map / Wpn / Song cells in shared
AID texture 2. The first three word rows now contain English ALL Attack,
Center, Wide, Map, Maximum Break, Counter, Support/Attack/Defend, Re-, Wpn,
and Song. Existing CMN battle-animation Counter / support / attack badges
also pass their separate category tests. Frames, UVs, and animations stay
unchanged. Other atlas families are outside this batch.

## Build and checks

`gift_reports.py` previews the complete inventory; `--write` generates the
hook file. `patch_gift_candidate.py --snapshot` saved the effective hook
baseline and previous centered-wrapper regions. Dry run followed by
`--write` added 30 hook entries (no removals), 3,760 text bytes, and the
scoped wrapper extension to `work/out_0.6.3/EBOOT.BIN`. Total lookup entries:
3,495. The byte-isolation/replay test checks the complete result. Backups:

- `work/gift_hooks_before.json`
- `work/gift_center_before.json`
- `work/gift_reports_EBOOT.before.bin`

`build_ui.py --out work/out_0.6.3` rebuilt AIDDATAPACK.CPK: 41 members,
14,242,708 bytes. The standard EBOOT build loads the new hook file and uses
the extended wrapper. Skill-description tests now replay their historical
endpoint before checking the current installed skill strings.

34 targeted tests pass: gift reports (5), President (3), skill descriptions
(6), part descriptions (6), search/shared words (3), battle action family
(4), deployment labels (4), weapon requirements (3). These include 72 reward
and 180 President emitted-PPC centering/register-preservation cases. The
decoded candidate atlas was visually inspected.

The broader `check_issue_fixes.py` audit stops at an existing conflicting
duplicate `・反撃する` in `translation/issue_hook.json`, before its later
checks. This batch does not change that unrelated entry. No full release,
ISO update, deployment, or version stamping was performed. In-game report
rendering and Counter activation still need confirmation after deployment.
