# Battle action and target-selection screenshot family

## Coverage

- Pending 2026-09-29: shared unit-name centering now measures English glyph
  advances rather than fixed character cells. All17 centered unit-name
  templates (including copied/recolored records) are inventoried by
  `battle_unit_name_layout.py`. Full names and panel/font settings stay
  unchanged; native/hidden strings fall back. Six focused tests cover all281
  distinct packed unit-name variants and existing search-grid behavior.
  Source only; no in-game placement verification or new build yet.
- Power Parts: verified the previously implemented selection heading, together
  with Transform, Spirit Commands, Element Change and adjacent Search Settings.
- Six battle action-menu variants at 0x9c934..0x9c9d4, plus Center/Wide at
  0x9cf74 and standalone Assist Attack at 0xa9174. All multiline row counts,
  coordinates, font sizes, colors and selection state fields are preserved.
- Eight dynamic CP932 labels: Assist Attack, No Assist, Select Weapon,
  Do Not Join, Counterattack, Defend, Evade and Attack. These are runtime
  lookup entries as well as the appropriate static menu variants. “Do Not
  Participate” exceeded the 280 px budget at 28 px, so “Do Not Join” is used.
- Four adjacent UTF-8 battle-selection warnings in EBOOT, bounded by the
  BattleFormationSelect and BGMSelectWindow resource blocks. Test/sample
  messages before this block and unrelated BGM messages are excluded.

| Source offset | English warning |
| --- | --- |
| 0x6d66f8 | No other actions are available. |
| 0x6d6730 | You cannot select an attack target. |
| 0x6d6758 | No usable weapons. |
| 0x6d6780 | This unit is incapacitated. |

The warning path uses standalone UTF-8, not the CP932 drawing hook. The
normal build consumes ui_utf8.json and relocates longer strings through
their data references. Candidate verification checks every original data
reference, its translated target bytes, font encoding and measured width.

## Native battle animation artwork

CMN.CPK member 0 has GTF at 0x9de0 and 20 linear ARGB textures. It is not
AIDDATAPACK's shared word atlas. `maximum_break_art.py` now composes:

- Texture 6: four cyan framed badges, ALL Attack / Center Attack / Wide Attack /
  Assist Attack. Only interior rectangles (5,36/68/100/132,126,24) change.
  Existing Maximum Break badge and the empty/default badge remain intact.
- Texture 10 (192x48): Combo Attack.
- Texture 11 (272x256), four 64 px rows: Counter, Attack Again, Support Attack,
  Support Defend, retaining the pink/purple/gold category colors.
- The Maximum Break badge remains composed. The large texture16 banner now
  uses nine English whole-letter cells and corresponding XY/UV rectangles;
  see the 2026-09-29 correction below.

All other pixels, framing, arrows, animation commands, timing, numeric
textures and controller icons are byte-identical. The source member hash is
validated before editing. Badge and banner atlas previews were visually
reviewed; this is not a claim of live emulator QA.

### Maximum Break nine-piece correction (2026-09-29, not yet built)

The original continuous English banner repaint was wrong despite its clean
atlas preview: nine animated quads sample eight unique Japanese glyph cells,
reusing the first glyph for the fourth letter. Their screen rectangles also
overlap. Projecting the shipped texture with those rectangles reproduces the
user's sliced/repeated English lettering.

`maximum_break_art.BANNER_PIECES` inventories all nine signed XY/unsigned UV
records and their initial anchors. The fix packs MA / XI / M / U / M / B / R /
EA / K separately, with transparent gutters and a larger word gap, and changes
only those nine 16-byte rectangles alongside the texture. Settled screen
bounds are contiguous with one baseline; all keyframe bytes remain intact.
The source hash and exact native rectangle/anchor values fail closed on drift.

`test_maximum_break_art.py` has seven source-level tests, including actual
packed-rectangle projection, old-layout rejection, sampling-edge clearance,
non-target byte preservation and a temporary archive round trip. The local
before/after CPU projection was visually reviewed. This is not a full build
or RPCS3 animation playback test; installation/release remains unchanged.

## Verification and delivery status

`test_battle_action_family.py`: four packed-candidate tests pass, covering
menus/Power Parts, dynamic actions, all warning data references, and CMN
artwork plus untouched archive members. The three previous map-UI tests
also passed after the initial build. AID and CMN were rebuilt normally.
Candidate EBOOT changes are restricted to lookup entries, exact warning
literals/data references and verified unused appended string space;
all unrelated bytes, including voice block offsets, are preserved.

The candidate is `work/out_0.6.3`, still unstamped. No source game, emulator,
save/cache, ISO or release was changed. Successful counter remains 0.6.2.
The independent STG0068 full-build audit blocker remains unresolved.
