# GitHub repair batch — 2026-09-06

## Dialogue default-name insertion — deployed, pending in-game verification

Candidate: `work/out_dialogue_names_20260906`. The reported Kyoko surname and
Jeffrey/Ozma full-name lines use runtime substitutions, not the standalone
draw-time hook used by protagonist setup. Traced `1afcf8` constructing the
`$n` (first), `$f` (nickname), `$l` (surname), and `$F` (nickname + surname)
replacement table. Patched only the leaf readers at `1af5a8/1af5b0/1af5b8`.
They read the existing state, match the whole default including NUL, and return
the current atlas's encoded Hibiki/Kamishiro; other names return their original
pointer. They never write game/save memory or repoint internal name keys.
Full names retain the saved order and original middle-dot separator.

Replacement slots are 41 bytes. A very long custom nickname (21–24 bytes)
combined with the VWF surname could exceed this; only in the two full-name
surname calls, the default surname then uses native ASCII `Kamishiro`. This
preserves the complete custom nickname rather than clipping it. Ordinary
default names and standalone surname use VWF. No font-mapping changes.

Checks: 210 emitted-PPC execution cases (default/custom/empty/null, exact-match
boundaries, register/CR preservation, full-name capacity). Complete integrated
build passed all UI checks and five Spirit-band copies. Byte comparison with
the currently deployed name-field build allows only the three branch sites,
three new stubs and their string data: 373 bytes changed; all other EBOOT bytes
including 3,240 hooks and SRVC offsets identical. Other game content identical;
SDAT plaintext compared because encryption is nondeterministic.
All 21 installed files backed up to
`work/github_issues/before_dialogue_names_20260906` with SHA256 manifest.

After the user closed RPCS3, verified no running process and deployed the full
bundle to `E:/SRWZ3/PS3_GAME/USRDIR`. All 21 installed SHA256 hashes match the
validated build manifest. Cleared only the regenerable BLJS10256_DATA cache
after checking the exact resolved path and absence of reparse points. Saves
untouched. No in-game verification claimed. Detailed fix/test comments posted
on public issues #10/#27/#28; needs-verification added and issues left OPEN.
Test by reloading/re-entering the affected scene, not just examining already
expanded Back Log entries. Existing saves do not require name migration.

## Name-field labels — deployed, pending visual review

User requested 姓 -> LN, 名 -> FN, and カミシロ -> Kamishiro on protagonist
setup. Added three exact display hooks to `translation/ui_hook.json` and built
`work/out_name_fields_20260906` through the integrated pipeline. All 3,237
existing hooks preserved; three added. Spirit bands and full UI checks passed.
All non-EBOOT game content is unchanged (stage plaintext compared separately
from nondeterministic encryption). Both historically unsafe surname pointers
remain identical to pristine; constants are virtual addresses, not file offsets.
This is display translation only, not a change to editable names or save data;
dynamic name substitution inside dialogue remains a separate unresolved issue.
Backup of all 21 installed files: `work/github_issues/before_name_fields_20260906`.
After RPCS3 exited, deployed the full `work/out_name_fields_20260906` bundle
and verified all 21 installed SHA256 hashes against its build manifest.
Cleared only the regenerable BLJS10256_DATA install cache; saves untouched.
Current installed bundle is now `work/out_name_fields_20260906`.
In-game confirmation of LN/FN/Kamishiro remains pending.

## Integrated rollback recovery — deployed, pending visual review

The pre-EN installed EBOOT matched `work/out_grow` exactly; all 20 other
installed files matched it too. Its AID member 0 retained all five Japanese
Spirit bands. A complete rebuild from current sources now ships as
`work/out_integrated_20260906`, not the stale `work/out`/`work/out_grow` sets.

Build-process repairs:

- VWF `build_project.py` invokes `build_ui.py` and the regression checker.
  Previously UI data required an easily missed separate command.
- Undrawable hooks fail the build; all source UI hooks are checked in output.
- UI lookup keys own copied Japanese strings in EXT. A previously borrowed
  standalone 陸 key was overwritten by movement_type_cells, breaking Grd.
- Successful builds record the 21 game files and font metadata in a checksum
  manifest. deploy.py rejects changed/mixed files when that manifest is present.

Checks passed: all 2,838 installed hook keys retained, 399 additional keys;
3,237 total. Earlier UI build retained except its corrupt tiny-cell Grd key,
replaced by correct 陸. 268 issue checks, five Spirit-band copies, and both
atlas pages' tiny glyph pixels verified. Shared letter mapping unchanged from
out_grow. SRVC bytes and executable block offsets identical to the installed
newer build. Decompressed stage members identical except STG0002 member 3,
rebuilt from its current translation source. Four glossary containers unchanged.
No battle voice-line edits made.

Backed up all 21 installed files to
`work/github_issues/before_integrated_20260906` with SHA256 manifest. After RPCS3
closed, deployed the complete set and checked all 21 hashes against the new
build manifest. Cleared only the regenerable BLJS10256_DATA cache; saves remain.
Local deployment only, no published release or issue closure. User should
check Spirit band, small Grd labels, EN and all five save-menu lines in game.

## Save destination regression: current installation repaired

User screenshot confirmed all five save-destination lines Japanese. Binary
audit found four translated hooks in `work/out` but absent in both the installed
executable and its backup taken before the EN fix. The EN fix changed only its
eight caption bytes, so it did not remove these hooks; the earlier replacement
that omitted them has not been identified.

Restored only the four screen hooks and added the previously missing
`保存先を選択してください。` -> `Please select a save destination.` to
`translation/issue_hook.json`. Prepared against the current installed mapping
with `work/github_issues/prepare_save_menu.py`: five appended exact-match table
entries and strings in unused EXT space; all 2,833 existing entries and code
preserved. 380 bytes changed. Backup and manifest:
`work/github_issues/save_menu_current_install/`. Installed SHA256:
`e4a5d66280cd20aae64440ed3f44cb0f653551a809cd5f33bf80a2d503723f8b`.
After RPCS3 closed, deployed only EBOOT, verified all 20 other game files
unchanged, and cleared the regenerable `BLJS10256_DATA` cache; saves untouched.
In-game rendering remains pending user verification. This narrow fix does not
claim to restore all other missing batch translations.

## Public tracker #33 follow-up: current installation patched

User's new screenshot shows Cost in both Weapon Info locations. Read-only
binary comparison (`work/github_issues/check_weapon_cost.py`) confirmed the
`消費ＥＮ` hook in `work/out/EBOOT.BIN` resolves to EN, but the installed
`E:/SRWZ3/PS3_GAME/USRDIR/EBOOT.BIN` resolves to Cost. Built MD5:
`79a6a1f0fe89a3042079d4de82441264`; installed MD5:
`4ca821b7db96748c1b68bdb435b60712`. Installed timestamp is 2026-09-06 11:39:49.
Do not assume the earlier deployment record still describes the current files.
After RPCS3 exited, comparison found 17 of 21 installed files differed from
`work/out`. To preserve that installation, patched only its existing caption
slot from Cost to EN using its own Unicode/font mapping: 8 changed bytes at
file offset 8939556, with the 9-byte slot zero-padded. No full-bundle deployment.
Backup, candidate and SHA256 manifest are in
`work/github_issues/issue33_current_install/` (`EBOOT.BIN.before` is the backup).
Installed output SHA256:
`52570ffe92c0e9f270b8b3e36c1131837e80194184ce98e50146f575ac48bf89`.
Verified the installed hook resolves to EN and all 20 other game files remain
unchanged. Cleared only `E:/RPCS3/dev_hdd0/game/BLJS10256_DATA`, the regenerable
install cache; saves untouched. Both Weapon Info locations still require
in-game review. Keep public issue `retro-trans/SRW-Z3-Issues-Tracker#33` open
with `needs-verification`. Do not blindly deploy the older `work/out` bundle.

Repository: https://github.com/retro-trans/SRW-Z3/issues

User requested individual fixes, excluding battle voice-line reports, and
asked that issues remain open with a review label. The label is
`needs-verification`: a locally built candidate is ready for the user's
in-game review, **not** a claim of screenshot-verified completion or a release.
No commits, pushes, releases, or issue closures were made.

## Deployed candidates

| Issue | Change |
|---|---|
| #7 | Kyoko: “mysterious robots”; Scenario 2 member 3 only |
| #9 | Standalone UTF-8 AI speaker caption |
| #10 | Z Chips and joined Unit heading in Get Result |
| #11 | 18 post-prologue narration lines; STG0001B member 7 has 88-byte records, not 84 |
| #13 | Exact End Phase messages with 0–99 fullwidth team counts and Yes/No |
| #14 | Narrow standalone Funds Earned caption shortened to Funds |
| #16 | Joined SR Point / 10000-fund reward templates and duplicate highlight layers |
| #17 | Operation End victory, defeat and SR Point heading block, plus separate calls |
| #18 | Standalone UTF-8 Branch Member speaker caption |
| #20 | Standalone UTF-8 Shotaro speaker caption |
| #23, #35 | Quick-save destination choices |
| #25 | Counter / Defend / Evade choices, whole blocks and individual lines |
| #26 | Both UTF-8 copies of the marked-Spirits warning; Yes/No hooks |
| #27 | Default Hibiki defeat-condition variants; existing keys used an internal A suffix |
| #30 | Reversed DEF/SKL source block used by Level Up |
| #31 | Post-save Continue prompt |
| #36 | Quick-save overwrite and new-save prompts |
| #38 | Weapon consumption header: EN |
| #40 | Narrow map-command button: Max Break |
| #41 | D-Trader unlock notice from STG0003 member 1 reward data |
| #42 | Chimera Squad ID unlock report, including a Japanese/VWF mixed-key variant |

Review the issue screenshots against these screens in game. In particular,
check reward highlight order, prompt punctuation/selection alignment, narration
placement and the mixed-name D-Trader report; binary checks cannot prove these.

## Still pending — do not label as fixed

| Issue | Finding / next check |
|---|---|
| #6 | Reporter comment says “Do not fix this yet”; deferred |
| #12 | Japan-map location: 第２新東京市 陣代高校; exact location label was not found in decompressed AID or stage 1–3 members; identify its source/render path |
| #15 | Back Log controls translated, but embedded default player name remains part of the runtime-name investigation |
| #19, #32, #33, #34, #37 | Same likely root: display-only name substitution leaves Japanese in the editable/runtime name buffer. Trace default initialization and substitution, preserving custom names. Do not blindly repoint lookup-key tables |
| #24 | Stage 1 title also exists in member 0 at CP932 +0x08 and UTF-8 +0x88 (128-byte slots), plus EBOOT UTF-8 +0x6EE410. Identify the title-card font/draw path and separate episode-number formatter before patching |
| #28 | Map 援護 indicator: exact standalone text absent from scanned sources; identify glyph/texture or composed label |
| #29 | Target-selection 全体攻撃 heading: exact standalone text absent from scanned sources; identify glyph/texture or composed label |
| #39 | Asked user whether to use Focused / Split or retain Center / Wide. Wide is main→main and sub→sub per the game's tutorial; it is not the ALL weapon category |
| #21, #22 | Battle voice-line reports excluded as requested |

## Verification and deployment

- `python -X utf8 tools/check_issue_fixes.py`: PASS, 267 batch hooks checked
  against 3236 generated binary entries; no unencodable UI text; source checks
  for joined rewards and all 18 narration lines; narration width <=1140px at
  the library reference geometry.
- `work/rebuild_battle_ui.py --eboot-only`: 227 existing name-table entries
  verified; 0 undrawable hooks; UTF-8 32 in-place / 66 repointed / 0 skipped;
  19 movement labels verified. The emitted hook stub includes the fix that
  prevents prefix-copy completion falling into the joined matcher.
- Scenario 2: 437 records pass the width/translation checker; only member 3
  changed relative to the existing built CPK; encrypted SDAT decrypts exactly
  to the rebuilt CPK. Other stage members were preserved.
- Only EBOOT and STG0002 differed from the installed files before deployment.
  In particular, SRVC and the atlas were byte-identical and remain unchanged.
- All 21 deployment files hash-verified. EBOOT MD5 prefix `79a6a1f0`;
  STG0002 MD5 prefix `fa6fa9c7`, SHA256
  `accbefed60f532d44359dda2e9cc7a816adfbe8824d46cced91285beba75ea5a`.
- Previous installed copies of the two changed files are backed up under
  `work/github_issues/predeploy_20260906/` (ignored game data).
- RPCS3 was closed. `E:\RPCS3\dev_hdd0\game\BLJS10256_DATA` was already absent;
  no cache deletion was necessary. Save data was not modified.

Implementation: `translation/issue_hook.json` is part of `eboot.UI_HOOK_FILES`.
It supports bounded `count_range` templates and `jp_vwf` for a key that contains
already-translated Latin letter cells. Hook English now expands glossary refs.
Temporary read-only scanners and the targeted rebuild helper are in
`work/github_issues/`. Existing unrelated worktree edits were preserved.
# Public #23 — Support Attack map badge (2026-09-06)

- Source: TPACKPS3.CPK member 2, texture 1 (80x320 linear ARGB32); four
  80x80 tiles have the same Japanese label and original numerals 1–4.
- Changed only each tile's `(37,2)-(77,24)` label rectangle to outlined yellow
  `AT`. No font-cell/string substitution, counter behavior or executable patch.
- Type proof: map producer `2e4a6c` calls `2f3ca0` (pilot +0x50), initialized
  from skill 1 (`sk-pri` = Support Attack). Draw state goes through `329e34`;
  `32a41c` selects texture 1, row=count-1. Defense uses `2f3cac` (+0x51),
  skill 4 (Support Defense), not this badge. Do not label this path DF or
  invent phase-based switching between counters.
- `tools/support_badge.py` is integrated into `build_atlas` for VWF builds;
  `check_issue_fixes.py` checks all four label tiles, unchanged numeral pixels,
  other textures and the attack-reader instructions.
- Candidate `work/out_support_badge_20260906` passes full UI regressions,
  including all 3,240 hooks, all five Spirit bands and 210 name-reader cases.
  Preservation audit compares every TPACK member, other game files, and stage
  plaintext (SDAT headers vary with encryption). Backup of all 21 installed
  files: `work/github_issues/before_support_badge_20260906`.
- Keep OPEN and label `needs-verification`. Test AT 1–4 in the map's support
  selection; original zero-use visibility behavior must remain unchanged.
- Deployed to `E:/SRWZ3/PS3_GAME/USRDIR` with RPCS3 closed; all 21 installed
  SHA256 hashes match the candidate manifest. Cleared only the regenerable
  BLJS10256_DATA cache after path/reparse-point checks. Save files untouched.
# 2026-09-07 public tracker help-wanted batch

Read all three open help-wanted issues and their latest screenshots:
#8 End Phase, #21 Spirit exit, #31 quick-save overwrite. All showed the same
duplicate No caused by translating the inactive row at proportional width
while the selected word retained its original fixed-column position.

Added two invisible, font-metric-derived spacers to the full-row translation.
All four FSSA variants retain their original records, geometry, colors and
choice behavior. Slash stays at column 3; No stays at column 5. Tests check
both active choices and the original half-pixel centered-No rounding.

#21's warning additionally used fixed UTF-8 byte copies in the executable.
Preserved those original source strings and pointers; translated their cp932
display strings instead. This avoids truncated text/missing NUL terminators.

Built/deployed `work/out_confirmations_20260907` with RPCS3 closed, 27 hashes
verified; no install cache present. Baseline was the newer `work/out`.
Backup: `work/github_issues/before_confirmations_20260907`. Every archive and
all stage plaintext unchanged; 3324 previous hooks identical, one row changed,
two prompt hooks added. Full regression suite passed; in-game QA pending.
All three issues remain open, with detailed comments and `needs-verification`.
