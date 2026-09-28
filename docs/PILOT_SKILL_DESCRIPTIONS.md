# Pilot-skill description review

Reviewed the Japanese skill-effect text against
[Akurasu's Z3 Pilot Abilities](https://akurasu.net/wiki/Super_Robot_Wars/Z3/Pilot_Abilities)
on 2026-09-11. Wording is adapted for the in-game panel, not copied verbatim.
Skill names, PP prices, levels and gameplay behavior are unchanged.

## Coverage

All 68 numbered `sk-pri` records and all 124 distinct descriptions in columns
4 and 5 are covered. Newtype and Enhanced share descriptions. No generic
Element Ability record was invented from the wiki's introductory entry.
Both long and alternate descriptions receive the same complete effects.

The prose source is `tools/skill_description_catalog.py`; regenerate
`translation/skill_hook.json` using `tools/build_skill_descriptions.py`.
Skill and Spirit references resolve from their existing name dictionaries.
Every variant fits at most three lines and 740 native pixels per line at
the candidate's 28px glyph size. The screenshot's help panel provides the
layout budget; this is not a live-render confirmation.

Half Cut now explains directly that damage is halved when an attack hits
despite a hit chance of 30% or less. Support Attack's Assist Attack bonus is
described per available support use, not as accumulating with every attack.
Other descriptions preserve thresholds, recipients, ranges, skill levels,
rounding, sub-unit/sub-pilot exclusions and activation conditions.

## Reference differences and gaps

- Aggressive Beast (originally labeled Feral; name corrected in source on
  2026-09-28): Akurasu gives a +30% critical bonus, while the Japanese help says
  +20%. Per the requested reference and project rules, descriptions now say
  +30%. Runtime behavior has not been measured or changed.
- Negotiator follows Akurasu's on-hit condition; Japanese help says the
  opponent fought. Mind Resist follows the wiki's Daunt floor of 100;
  the Japanese wording states immunity when already at 100 or below.
- SP Regen includes the wiki's normal-recovery total. E-Save/B-Save include
  its learning restrictions. SP Up/Potential include the level-9 ceiling.
- Combat Program is absent from the page; its +15% effect comes from the
  original Japanese description.
- Gravitational Interference 1 retains Air A and version 2 retains Air S.
  Akurasu describes only the S-rank version, without identifying variants.
- Power of Reversal 1 retains 100% Counter activation; version 2 retains
  the separate +50% bonus. The wiki describes only the 100% version.
- Isolating Power retains the source's named Barrier Field. The wiki's
  damage/EN numbers are question marks, so no unverified values were added.

## Build and safety

Run `python tools/build_skill_descriptions.py` for the dry run, then add
`--write` after reviewing the proposed text. Normal EBOOT generation already
loads `skill_hook.json`. Its `line_pairs:false` prevents newly wrapped English
lines from being paired with unrelated Japanese sentence fragments.

The isolated candidate update uses `tools/patch_skill_candidate.py`: snapshot
the effective hooks before editing, dry-run the delta, then apply with
`--write`. This batch replaced 124 complete hooks, removed 181 obsolete
generated fragments and appended 9,673 bytes of text, leaving 3,465 lookup
entries. Backup: `work/skill_descriptions_EBOOT.before.bin`; baseline:
`work/skill_hooks_before.json`. All bytes outside the lookup table and new
text are preserved, including executable instructions and voice tables.

Six skill tests check coverage, encoding/widths, variant effects, absence of
fragment generation, unchanged RPW descriptions and the installed binary.
Six Power-part, three weapon-requirements and three President-report tests
also pass. The Power-part test now checks its historical batch endpoint
separately from the live part hooks, allowing this subsequent isolated patch.
No ISO, deployment, release or build stamp changes; in-game QA remains pending.
