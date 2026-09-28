# Handoff

**2026-09-28 release 0.6.22 complete:** user explicitly requested release.
All pending source batches below are now in the successful strict English
build work/build_0.6.22_english_20260928, source b1ee149. Hardware package
work/ps3_hardware_0.6.22_20260928 passed all554 files in both directory trees;
ISO SHA553a85e458843eb4b28cd0c7105776ed56576cf42c1564f2e7a375d2cc6afbfd,
5,018,877,952 bytes. Original and exact.21 upgrade ISO patches both decoded
to that exact image and passed Retro Trans0.3.1 validation; ready directory
work/retro-trans/ready_0.6.22 contains exactly five protocol artifacts.
Installed wrapped snapshot in game/: all220 hashes match, all26 save files
unchanged; recoverable game/cache backup work/install_backups/0.6.22_20260928_203448.
Snapshot releases/0.6.22 created; local per-file patches220 original +153
previous all decode-verified. See docs/validation/0.6.22.md for current
checks, 96 passing test modules and twelve historical/Vita test limitations.
Published latest at2026-09-28T13:47:10Z, release398292582:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.22.
Tag57a56ad adds records/test maintenance to actual build source b1ee149.
Five uploaded digests match local artifacts; actual public downloads passed
Retro Trans release_record. Scoped catalog run36431167008 succeeded;
live catalog commitdf0541dc exposes both routes. Refresh from the saved prior
20-release cache passes immutable identities and Latest planning for original
and.21, with no cache reset. Existing.21 assets unchanged. No game/ISO upload,
Vita/VI package or visibility change. No runtime confirmation of this exact image.
Earlier pending/unbuilt entries below are chronological source-fix records;
their English changes are now included in.22 unless explicitly excluded above.

**2026-09-28 pending demo series captions:** screenshot84f786ec is OP.CPK
member0/texture0, Mobile Suit Gundam Unicorn. All four BTLC/OP.CPK members
contain six 1280x64 linear ARGB title textures at GTF0x60: 24 distinct series.
tools/demo_series_titles.py maps their visually checked order to existing
glossary IDs, guards each original member hash, and replaces only pixels.
Original input remains game/PS3_GAME/USRDIR/DATA/BTLC/OP.CPK until the next
explicit build caches it at work/orig/OP.CPK (validated before copying).
Integrated build_project/check_issue_fixes and extract/deploy/apply_xdelta;
release/install/hardware packaging inherit deploy.LAYOUT. Registered in
localization/assets.json. Five focused tests, including temporary archive
round trip; work/demo_series_english_preview.png visually checked. No full
game build/install/release or runtime demo verification. Vita not mapped.

**2026-09-28 pending Sphere title corrections:** user explicitly wants
Sorrowful Maiden / Wounded Lion / Lying Black Sheep / Inexhaustable Water
Gourd (preserve exact spelling). Four new glossary entries use source keys
悲しみの乙女 / 傷だらけの獅子 / 偽りの黒羊 / 尽きぬ水瓶. Seven dialogue
records in0052_03/0087_04/0091_04/0097_04 plus four library entries now use
tokens; Black Sheep no longer contains the unrelated character-Ram token.
Source token inventories and local PS3 glossary template updated. Two VI
records migrated with four VI glossary values preserving existing prose.
BASE_RULES and conflicting work/tr/CONVENTIONS.md spellings corrected.
test_sphere_titles.py: four pass; all2,135 dialogue records across four files
pass font/structure checks; localization/543 compatibility views pass.
Wavering Scales and other titles unchanged. No build/install/runtime test.

**2026-09-28 pending Rand/Mel correction:** user wants Rand and Mel, not
Land/Mail. Existing glossary:r_47ca0c51f435e8f8 now Mel. Added glossary:rand
(ランド, Rand) to EN/VI catalogs, local source definition and PS3 legacy
glossary template. Eight dialogue records in0052_03/0060_03/0069_03/0070_04/
0071_04/0087_04/0091_04 and Mel's library.kw_104 biography now reference Rand;
full names resolve Rand Travis / Mel Beater. Nine local source token lists
and six VI token references migrated; unrelated ordinary words untouched.
BASE_RULES records spellings, test_rand_mel.py has four passing tests. All
3,044 dialogue records in those files pass font/structure checks; English
localization/543 compatibility views pass. No build/install/runtime check.

**2026-09-28 pending Sphere/Dimensional Power capitalization:** screenshot
2cd18b45 comes from stage0052_03, Kouji r_adec86483b13599a and Banagher
r_2cf701bbcde3ec13. Glossary already correct; `|lc` overrides caused the bug.
Removed21 overrides in18 English dialogue records (stage0052_03/0055_03/0084_03),
canonicalized25 lowercase literal library references in13 records
(library.kw_000/library.rt_240). Shared source token inventories updated,
plus token-only case-modifier migration for17 Vietnamese records in0052/0055;
no VI prose changes. Ordinary spheres/Earth sphere untouched. Standing rule
in BASE_RULES and terms.py docs; tools/test_lore_capitalization.py guards this.
All869 dialogue records pass font/structure checks; localization/543 views
pass. No build, installation or runtime verification; source batch only.

**2026-09-28 pending chapter narration (source only):** screenshotfcdfb14d
is STG0052 member7, offsets0x114/154/194. Missing three-line page plus related
STG0026(3), STG0083(3), STG0098A(4): 13 rows in new chapter_narration catalog.
tools/chapter_narration.py supplies exact draw hooks through eboot.load_ui_hook;
never patch these resources using narration.py's 84-byte record assumptions.
Their source hashes/offsets are guarded, with single-row translations and
1000px/32px font checks in check_issue_fixes. Three tests pass, including full
UI hook-table emission in memory. All 144 stage CPKs' small padded members
(IDs6+,<=20KB) scanned via work/audit_narration_members.py: only these four
missing pages plus existing opening/post-prologue narration found. Opening
uses member index6 = ID7 and is already handled by narration_0001a.json.
No stage/game file edits, build, install or runtime verification performed.

**2026-09-28 pending Aggressive Beast terminology correction:** user reported
Feral; Akurasu Z3 Pilot Abilities confirms Aggressive Beast with the same
130 Focus / critical +30% / damage x1.1 description. Updated canonical
skills:r_671a3037d9a84efd and bonus_descriptions:va_70a2d8. Existing source key
野性化 remains unchanged (Akurasu spells it 野生化). Tests in
tools/test_aggressive_beast.py cover label export, bonus hook, font fit and
in-memory RPW relocation. No build/install; runtime verification pending.

**2026-09-28 pending MAP weapon info fix (source only):** screenshot457ddb34
shows Japanese IFF 有効 and Pattern/Self-Centered overlap. New
`map_weapon_info` catalog/hooks provide On/Off; `tools/map_weapon_info.py`
repoints the two FSSA Off defaults and moves all three Pattern headers from
native x607.5 to570.5. Canonical ui_hook pattern labels are Centered / Target /
Line Scan / Direction. Native value anchors, font sizes and targeting logic
are unchanged. Source inventory covers both states, four modes, all matching
member-0 widgets; .21 font widths enforce 8px column gaps and right edge830.
Integrated build_ui + check_issue_fixes gates. Five focused tests, three
weapon-heading and four destroy-quote tests pass; full UI hook emission tested
in memory, localization check/543 compatibility views pass. No build/install
or runtime visual verification: batch with other pending fixes only on an
explicit build request. Source definitions remain local/ignored as usual.

**2026-09-26 standing release requirement:** every future release must work with
Retro Trans. AGENTS.md/CLAUDE.md now require the compatibility completion gate in
docs/RETRO_TRANS_RELEASES.md: local round trips, uploaded/public artifact checks,
live catalog discovery, correct routes and previous-cache compatibility.
Unsupported packages or failed enrollment block completion; do not weaken
validators or use cache resets as the normal release process. No new build or
publication is authorized merely by this requirement.

**2026-09-26 original-only public release withdrawal:** user requested removing
the .19->.21 upgrade because .21 is the first public release. Retain only the
unchanged from-original xdelta; regenerate the three metadata assets for that
single route and remove only its upgrade catalog edge. Old full ready directory
and all backup assets remain intact. Original-only preparation:
work/retro-trans/ready_0.6.21_original_only/. Receipt:
work/publication-audit-20260926/upgrade-withdrawal.json. Do not re-add the upgrade.
Withdrawal completed: release397176829 now has four verified assets, and catalog
commit b00b52dc02371f1255a6d3e19209f0d2d7f084e5 removes only the upgrade route.
Existing Retro Trans caches containing the prior two-route catalog reject route
removal through assert_immutable; reset that cached catalog or use manual mode.
No validator changes, new build, installation or change to the full patch.
Earlier five-asset/two-route completion below describes the initial publication,
superseded by this explicitly requested withdrawal.

**2026-09-26 PUBLIC repository / 0.6.21 / Retro Trans complete:** user approved
the replacement. Original repository ID1345954230 is PRIVATE and archived as
retro-trans/SRW-Z3-private-archive-20260926. New independent public SRW-Z3 has
ID1388978408, master branch and only cleaned ancestry. Old commit1cc692a is not
accessible from the new repository. The preserved old Git/common-worktree origin
now points to the private archive; do not push old refs to the public repository.
Published v0.6.21 at09:44:12Z, release397176829, tag77cb47992c4716c3894ff3c186a5c7f390224656.
All five uploaded assets match original local SHA256/size; public downloads were
independently validated with Retro Trans0.3.0 release_record and Catalog.plan.
Both original->.21 and exact.19->.21 routes pass. No new build/install: later
source fixes and VI translations are NOT in this unchanged English PS3 build.
Shared catalog run36233677979 failed on unrelated SRW-Z v0.9.85 manifest naming.
Did not change that project's assets or weaken validation. Added only Z3's
verified record via guarded catalog commit0208c41a47551a11e629f335a5deb285ca2ddd23,
preserving all10 earlier records and passing assert_immutable. Live public raw
catalog URL used by the app now contains Z3 and resolves both one-patch routes.
Future global refresh still requires fixing that separate SRW-Z metadata issue.
Receipts: ignored work/publication-audit-20260926/{fresh-public-repository.json,
public-release-verification.json,public-download-validation.json,catalog-enrollment.json}.
README/install/release notes distinguish historical binaries, clean source tag,
unbuilt fixes and withdrawn historical assets. Earlier blocked entry below
records why the original repository must never be made public.

**2026-09-26 hosted cleanup complete; publication blocked by retained objects:**
User explicitly requested public visibility and Retro Trans-compatible release.
Normal Windows-session GitHub authentication works; the earlier invalid-login
report was a restricted-session failure, not an expired account credential.
All nine historical releases and tags were removed after verifying local backup
of 36 assets (1,662,554,942 bytes), notes and tag identities. Master was replaced
atomically with clean history at 36e601c using exact force-with-lease guards.
Receipts/backups: ignored work/publication-audit-20260926/{remote-cleanup.json,
release-backup/}. Old Git/worktrees remain preserved separately as below.
GitHub still serves localization/messages/activation_prompts.json (10,141 bytes)
at removed commit 1cc692a4fd1d3b7d6ba0b40eb9d842f4c84a5932 after all old tags and
releases are gone. KEEP PRIVATE: a force push does not purge retained objects.
Ask permission to rename/preserve this repository privately and create a fresh
public repository under the original name before publishing. Do not delete the
whole repository or assume this expanded action is authorized.
Existing PS3 English 0.6.21's five artifacts pass current Retro Trans 0.3.0
validation (local/remote tools HEAD a84454d); patch bytes remain unchanged.
No new build/install, recreated release, visibility change or public catalog
entry yet. Latest source-only fixes and Vietnamese merge are NOT in that build.

**2026-09-26 Vietnamese content merged from the linked worktree:** imported
188 locale JSON files /43,104 entries from codex/vietnamese-silver 5dd5d66.
IDs/source/context/kind all match current main; wording preserved exactly.
244 old opening drafts upgraded. 42,155 accepted by current structural and
glossary checks;393 glossary-token mismatches marked needs_review (402 total
including9 inherited reviews),547 explicit missing. Global VI missing count
is60,626 including absent rows. See localization/locales/vi/README.md and the
402-ID QA report localization/qa/vi_worktree_merge_20260926.json. Six inherited
title notes moved into the report to keep locale rows schema-conformant.
No English/shared source edits or old history imported. Branch font/build
adapters were not ported: game_build_ready stays false. Worktree untouched;
draft backups and dry-run/import script under ignored work/vi-merge-20260926/.
No build/install/commit/push. Next translation checkpoint remains Stage75
story81-160, but this merge did not perform additional translation or review.

**2026-09-26 local source privacy / fresh-history reset:** Japanese messages/,
PS3 localization/legacy.json and generated translation JSON/TSV are local-only
and ignored, not deleted. Locale translations/code/glossary remain tracked.
See docs/LOCAL_SOURCE_DATA.md: source-dependent tooling needs these local
inputs; extract.py is NOT a complete fresh-clone catalog bootstrap. The user
authorized a single new main root commit and preserving the two linked
worktrees with archived old Git metadata under ignored work/history-reset-*/.
GitHub history/releases/visibility are unchanged; no force push authorized.
Do not force-add source inputs or publish the local history archive.

**2026-09-26 translation review/contribution tools:** README now has Check the
translation and Translate it sections; current root TRANSLATING.md documents
canonical locale edits, validation/sync and other-language boundaries.
tools/compare_translation.py renders a local searchable/paged JP/locale report
from stable catalog IDs. Dry-run default; --write creates new work/*.html only.
Glossary uses selected locale, no fallback; reports do not prove shipped game
coverage. Separate missing/source-unavailable/draft/invalid/same/blank filters.
No build/install/upload. Existing docs/TRANSLATING.md is historical research.
- 25 tests pass (7 comparison +18 catalog). General glossary metadata retains
  numeric discriminators; the two legacy description catalogs resolve from
  locale-specific Spirit/skill dictionaries just as their generators do.
- Final local report: work/translation-review-20260926-r2.html (103,183 rows,
  no invalid flags; 1,269 source-unavailable,7 blank,287 same-as-source hints).
  Earlier non-r2 report was a development snapshot with false dictionary
  warnings; use r2. Report contents are private/ignored, never publish them.
- Browser checked local HTTP preview (paging/search/filter/layout, no console
  errors); in-app browser blocks direct file URLs, so direct-file opening was
  not verified. The HTML has no external dependencies or requests. Temporary
  preview server stopped. Canonical text unchanged;543 views still agree.

**2026-09-26 README credits:** Added the user-requested Credits role table,
following SRW-Z's format: Project Lead pow; Playtesting SecondarySebs,
gabrielgamer99, Theoldnile, Kapt, mr.notaru, rikineko. Documentation only;
not built, pushed or published.

**2026-09-26 source-only stage dialogue speaker headers:**
- Screenshot stage0050b_04 inner thoughts dropped Daston/Aoi/Amata headers.
  First thought lines therefore occupied the name bar; backlog continued
  without their speaker changes after Angel. Source, not portrait, supplies
  the restored name. Dollar expansion and battle-name transport unrelated.
- 118 repairs in five files:13 missing names (50b:6,68b:4,100a:2,100b:1),
  105 joined name/body lines (55_03). Body wording unchanged, restored names
  use glossary tokens; 13 required-token definitions updated accordingly.
- tools/dialogue_structure.py shared by localization, check_stage and
  patch_lua fails early for this category; does not infer speaker identity
  or classify anonymous/narration sources as named. Focused regression suite
  in test_dialogue_structure.py. No build/install; .21 remains active.
- Validation:5 new speaker tests +18 localization tests pass. All1,687
  records from the five pristine Lua files source-match and pass stage
  width/line/encoding checks; Lua patch composition tested in memory only.
  62,788-record catalog audit clean,543 compatibility views agree. Exactly
  118 text changes verified; Japanese source/context and body prose intact.
  Game-screen/backlog confirmation still awaits the next requested build.

**2026-09-26 source-only complete upgrade-system / unlock-report category:**
- trader_upgrade_text:31 new canonical entries (4names +4lore +4effects +19
  completed-condition forms). Existing two reports plus these cover all21
  native requirements. Source inventory covers17 strings0x70d6f0..70d970 and
  four embedded system-record requirements. No unlock thresholds changed.
- Four0x380-byte records at0x6b0528; exact name hooks preserve16-byte names.
  Eight lore/effect fields translated within original240/128-byte capacities;
  IDs/prices/names/condition fields and all surrounding data remain unchanged.
- unlock_reports previously repointed a32-byte English prefix into a native
  fixed18-byte copy, producing "Now at D-". encoded_part now honors18/8-byte
  prefix/suffix lengths, pads safely and refuses overflow. Prefix "Unlocked ".
  Four exact mixed-VWF/Japanese full-notice hooks expand system names at draw
  time. No native buffer/copy instruction/price/gameplay changes.
- Focused tests replay actual native prefix/suffix copies and match resulting
  mixed keys; catalog/hook coverage, source mutations and byte isolation also
  checked. Full EBOOT composition in memory passes. No build/install/version
  or publication; installed .21 unchanged. In-game confirmation still pending.
- 19 focused regressions pass; full current executable composition leaves
  4,752 EXT bytes free. Catalog zero issues,543 compatibility views agree.
  No generated text-view changes: this new group is consumed directly.

**2026-09-26 source-only D-Trader confirmations / Spirit caster panel:**
- New trader_spirit_prompts catalog/adapter: native buy/sell suffix strings
  file0x70cfd0/70cfe8/70cff0 preserve exact16/4/18-byte append lengths; sell
  fragment has four compiler-inlined immediate stores also patched to match.
  All allocation logic, item names, quantities, pointers/terminators preserved.
  No extension allocation. Previous menu/skill fixes missed this composer.
- FSSA0xabb74 SP Cost/SP; blank decorative quote frames0xac854/aca34/aca94/
  acc54 cover the complete duplicate inventory. Five pointers only; dynamic
  name fields, values, geometry, font/line spacing and controls untouched.
- Build_ui, eboot patch/verify and check_issue_fixes integrate the guards.
  New tests replay native instructions with all part names/quantity examples,
  reject source/byte-budget mutations and verify pristine/.21 UI composition.
  No build/install/publication. Installed .21 unchanged; runtime QA pending.
- 12 focused regressions pass (3 new +4 activation/full ELF +5 command/speaker),
  including current full EBOOT composition in memory with5,784 EXT bytes free.
  Canonical catalog zero issues and543 compatibility views agree; direct
  catalog consumption means no generated text views changed.

**2026-09-26 source-only Basara Song Soul stat overlap:**
- Shared runtime 歌魂 label shortened to Sng; full Song Soul retained in
  all four song_stats help widgets. At 28px: Sng53.375, CQB59.5, old full
  label140.875. No value/position/font/gameplay changes or per-pilot exception.
- song_soul context documents narrow two-cell stat use with56px budget;
  song_deployment_labels.check_ui now also sizes runtime hooks with no FSSA
  widget, closing the earlier broad280px-only validation gap. Regression
  covers25/28/36/42px styles and full-help preservation. No build or install;
  .21 remains active. In-game visual confirmation awaits next requested build.
- Five song/deployment regressions pass, including oversized-hook rejection;
  canonical check and all543 compatibility views pass. This adapter consumes
  canonical text directly, so sync correctly reports no legacy-view changes.

**2026-09-26 source-only Akurasu Spirit terminology correction:**
- User asked to check Akurasu for Asuka's overlapping Fighting Spirit label.
  Z3 Spirits and Asuka pilot database agree: 闘志 is Fury (Lv33, SP35),
  直撃 is Break. Corrected both so command identities remain distinct.
- 18 entries across spirits/ability_hook/spirit_hook/bonus_descriptions/
  parts_desc_hook/parts_descriptions.unshipped updated; generated English
  views synchronized. Compact flags Fu (0x86BF) and Br (0x86CA) preserve IDs.
  Separate Fighting Sp pilot skill untouched. No cost/effect/unlock changes.
- docs/SPIRIT_NAMES.md explains superseded historical mapping. New focused
  terminology regressions cover identities, compatibility view, flags,
  description references and unrelated skill preservation. No full build or
  install; .21 unchanged. Shorter command label requires next-build visual QA.
- 14 focused tests pass (4 terminology +6 parts +4 pilot status); localization
  check and all 543 generated compatibility views pass with zero issues.
  Parts' historical .3 fixture remains unchanged; its replay test restores
  original wording/line wrapping before comparison.

**2026-09-26 source-only category-wide battle speaker transport fix:**
- User confirmed the latest Mariemaia Soldier corruption is from installed
  .21 and asked to fix the whole category. No build requested this turn.
- Proven path: caption object +0xf94 is 31 bytes; dialogue begins +0xfb3.
  Unbounded strcpy at VA0x1073e4/0x107494/0x10767c copies full English over
  that boundary; native dialogue formatting subsequently overwrites the tail.
  Real native instructions reproduce the problem. This replaces the earlier
  unproven 15-letter-copy hypothesis; full stored strings were insufficient.
- tools/battle_name_transport.py hooks all three producers and only the name
  draw at0x10826c. <=30-byte names copy normally; longer ones store a tagged
  reference to their existing battle-lifetime backing string. Resolve before
  0x110c3c measures/decodes. CP932/UTF8 flag untouched; dialogue draw unchanged.
  Native31-byte snapshot0x11fef0..0x120010 preserves reference, byte-zero clear
  invalidates it. No native array/loader growth; no individual name additions.
- Build + check_issue_fixes verify all hooks and cache/clear/selection/snapshot
  hashes. Old three-name deferrals stay compatible; Mariemaia squad plural
  remains independent. 144-byte addition; full in-memory EBOOT composition
  passes with5,648 EXT bytes free. No canonical translation edits this turn.
- 27 tests pass:5new transport +7old name +4activation/full ELF +6link identity
  +5command/swap/fallback inventory regressions.
  1,625 name cases (470 fallback bindings covering1,155 pointers +1,155 RPW
  nickname slots),62long; all three call sites, native line writes/snapshots,
  both encodings, resets/transitions, 30/31-byte boundaries,1024-byte synthetic
  name, ABI/canaries, source guards and unrelated-byte isolation verified.
- docs/BATTLE_NAME_TRANSPORT.md records trace and limitations. No game build,
  install, cache change, version, tag or publication. Installed/published .21
  unchanged; require next explicit build then affected-battle visual testing
  on RPCS3 and PS3. Do not call static PPC emulation gameplay confirmation.

**2026-09-25 English 0.6.21 published and installed:**
- Build, package, snapshot, both per-file sets, both whole-ISO
  round trips and installation ALL PASS. Ready directory:
  work/retro-trans/ready_0.6.21 (154,763,400-byte full / 21,234,653-byte update).
  Published latest at 2026-09-25T16:50:04Z:
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.21.
  All five uploaded names, sizes and SHA256 values match local artifacts;
  release notes match. Repository remains PRIVATE; no public catalog change.
- User confirmed build + PS3 release of all pending fixes. RPCS3 closed by user.
- Original -> .21 and exact published .19 -> .21 ISO deltas plus standard
  validated metadata only. Local snapshot/per-file patches are preserved;
  withdrawn per-file ZIP stays off GitHub. Notes: docs/releases/0.6.21.md.
- All five "unbuilt" September 25 batches below are now shipped in .21;
  those older entries retain their original source-only preparation history.
- First build failed safely in build_ui: missing process-local glossary setup.
  Fixed initialization and added fresh-process entrypoint coverage. Counter
  did not advance on failure; retry work/build_0.6.21_english_20260925_r2 passed.
- Complete .21 build validated: 5,445 hooks, 2,119 audited mission variants,
  zero missing; 35 focused regressions pass. Shared fingerprint:
  933f4397123af5595ba64778cf71679343be9f1c4421c95c96d359e65fb677bf.
- Hardware package work/ps3_hardware_0.6.21_20260925 passed dry/write:
  both trees 554 files, 5,011,013,632-byte ISO SHA256
  b67c0a23924e79ab31d28c9b726535473087eee9bf8e5dd4758ce4c6ec64c3e0.
  SELF SHA256 5e3a63e99eb4eab1acaa549284bc26e02895e86c0de9cd60c950a564266b3355.
  Raw ELF is intermediate only. Wrapped snapshot copied to releases/0.6.21.
- Source commit pushed privately: 418c709ad973f02c1dd4fe641cdcec3e9aee9e3b.
  Tag v0.6.21 points to release-record commit 9464ca41692cffa84acfc7e36c617c971752e532,
  a descendant with identical build sources. Standard builder v0.2.1 config:
  work/retro-trans/release-local-0.6.21.json; validation gate passed.
- Local installation now COMPLETE: .21 wrapped snapshot in game/; all 219
  updated hashes and complete-disc check pass; 22 saves unchanged. Backup:
  work/install_backups/0.6.21_20260925_233223. RPCS3 registration verified.
  No install cache was present to move; it regenerates on launch.
  Local per-file deltas complete: 219 original + 149 from .19, decode-verified.
  Runtime gameplay/visual confirmation remains pending on both targets;
  preserved-layout ISO remains a hardware candidate, not hardware-confirmed.

**2026-09-25 unbuilt pilot status name/Spirit-column batch:**
- rpw.compound_name_overrides resolves col2 + ・ + col1 against complete
  canonical pilot names, then splits English at the final space into col2/col1.
  Fixes six Asuka records (858-860,897-899) and three Mari (861,862,900),
  whose old output duplicated Shikinami/Makinami. Fifteen matching records
  total; six other compound-name records reuse canonical full-name spelling.
  Applied AFTER existing name overrides; nickname col0 remains unchanged.
  RPW check runs before packing and again through check_issue_fixes.
- pilot_spirit_layout: name widgets0xb83f4/0xb8cb4 compact to18px, preserving
  line advance54; cost widgets0xb8414/0xb8cd4 shift +24 native px. Full Spirit
  names retained, >=8px clearance for every catalog name; cost/unknown text,
  colors, row spacing and all unrelated bytes unchanged. Checks integrated
  in build_ui and production gate. Visual confirmation still required.
- Eight tests pass (test_pilot_status_fixes + test_command_swap_labels),
  including pristine/.20 UI and RPW composition with unrelated-slot isolation.
  No canonical spelling edited, build/install/version/publication untouched.
  Installed .20 remains active; this joins the other unbuilt batches below.

**2026-09-25 unbuilt E-Change / battle speakers / swap equipment batch:**
- command_swap_labels: 18 new canonical entries plus existing canonical
  aliases, 21 exact hooks, 17 widget pointers. Covers E-Change help/reset,
  adjoining command-help/footer gaps and four swap-equipment names. Complete
  two-table inventory at file0x84b9fc and0x858d1c (ten slots each) is guarded;
  native None, equipment IDs, stats and table bytes are preserved. Both pristine
  and installed .20 UI compose in memory without geometry/control changes.
- battle_speaker_names + platforms/ps3/localization/battle_speaker_bindings.json:
  full UTF-8 fallback display table file0x84d410..0x84e61c, 1,155 slots / 470
  canonical bindings / 468 source strings. Uses glossary/enemy_names/name_pieces;
  adds only missing ASCII acronym/unknown labels. Zessica sourceVA0x6ed2d0
  has seven slots. Ray/Rei and Mehna/Mina explicitly split by series/slot.
  Unlike unsafe loose CP932-name repointing, this only changes the inventoried
  UTF-8 display table. Native strings/lookup keys stay intact; existing three
  battle-name and barrier/sword UTF-8 checks still pass after composition.
  September26 correction: this verified stored fallback text only. The .21
  Mariemaia report confirms a separate native caption overflow persists;
  category-wide source fix and evidence are now recorded at the top.
- Fifteen regressions pass; full EBOOT patched/verified in memory,
  5,792 bytes free in existing EXT;
  no loader-size/layout change. Canonical zero issues;543 views clean. No
  full build/install/publication; installed .20 and published .19 unchanged.
  Runtime visual confirmation (especially fallback names) still required.

**2026-09-25 unbuilt activation-banner follow-up:**
- song_deployment_labels expanded to 30 entries / 26 widget bindings (still
  19 exact hooks). Added Skill Active and Ability Active, two visual states
  each, at 0x9a914..0x9a974. All descriptor bytes except text pointers stay
  unchanged; widths checked. Song Energy at 0x9e354 was already pending.
- Four focused tests pass against original and .20 UI in memory; catalog
  zero issues / 543 compatibility views clean. No build/install. The apparent
  EBOOT Song Energy match was inside a bonus description, not a standalone
  label, so no duplicate runtime hook was added. Installed .20 unchanged.

**2026-09-25 repeated weapon-warning report fixed in source (unbuilt):**
- Earlier weapon_requirements.py repairs fourteen FSSA templates, but runtime
  constructor VA 0x331060..0x331490 copies separate Japanese strings from
  table VA 0x869194 into eight 0x101-byte rows and selects failure colors.
  Missing executable-table hooks explain the gap despite passing static tests.
- weapon_requirement_runtime catalog/module supplies fourteen exact hooks for
  all sixteen table slots (duplicate Max Break plus unchanged placeholder).
  Includes the seven basic labels and all special-condition alternatives.
  Trailing fullwidth spaces are matched exactly. No native buffer/constructor/
  pointer table/condition/color changes; separate Song EN copy remains native
  and is covered by previous batch. eboot/check_issue_fixes integration complete.
- Seven tests pass including whole current EBOOT patch/verify in memory and
  explicit unchanged-constructor/table checks. 15,384 bytes free after all
  extensions. No build/install/version/publication; .20 still installed.
  Both this and the song/deployment batch await explicit build authorization
  and subsequent in-game visual confirmation.

**2026-09-25 unbuilt song/weapon and deployment screenshot fixes:**
- Canonical song_deployment_labels: 28 entries. tools/song_deployment_labels.py
  integrates 19 exact EBOOT hooks and 22 widget-local UI strings, covering
  Song EN / Focus Up, related effects/song types, Song Soul, song headings and
  legends, stat substitution help and both battleship lists (Ship / Aboard).
  Remaining-deployment fragments become Left: + untouched native count;
  old 機～ suffix is blank. No global short-fragment hooks or numeric edits.
- Verified original offset bindings and duplicate-widget inventory. Four
  regressions pass against pristine and installed-build .20 UI in memory;
  four existing activation tests pass with the complete new executable patched
  and verified in memory. All extensions leave 16,048 bytes free. Catalog zero
  issues, 543 compatibility views clean. Checks are in build_ui/check_issue_fixes.
- Source only, explicitly no new build requested. Installed .20 and published
  .19 unchanged. Runtime visual QA pending; no Vita binary port performed.

**2026-09-25 English 0.6.20 built, packaged and installed (not published):**
- User approved all pending fixes and a complete PS3 build; no publication.
  The two dialogue checks below are now applied: Shotaro "him" and Mikage
  "my wish is fulfilled", with translated status and unchanged glossary tokens.
  Stage0045_03 checker: 364 answered records, zero problems.
- bonus_centering.py extends the existing guarded public centered-draw wrapper
  to 110 exact single-line bonus descriptions plus the full-upgrade lock label.
  Measures actual English advances; multiline/unrelated strings keep native
  behavior. Source pointer table uses verified ELF file offsets + 0x10000;
  historical bonus context.eboot_va values are FILE OFFSETS despite that name.
  Emitted stub 1,012 bytes and data 1,328 bytes fit existing separate 2-KiB caves.
  Three CPU/source regression tests pass; whole executable check passes.
- Initial build stopped on unexpanded Igura glossary tokens in battle subtitles.
  trdata.voice_document now expands English before both atlas and binary writer,
  preserving source/section/budget metadata. Nine ace/Igura tests pass, including
  a new regression scanning all 211 subtitle sections. Failed output is retained
  under work/build_0.6.20_english_20260925, never installed or numbered.
- Retry work/build_0.6.20_english_20260925_r2 passed the strict full gate.
  Includes all unbuilt screenshot batches below. 2,119 mission variants with
  zero missing; 5,394 hooks; 31,666 battle subtitles rebuilt and read back.
  Nine ace/Igura and ten bonus/skill/activation tests pass. Additional 28-test
  mission/loader/deployment run: 26 pass, two historical work/out_0.6.3 fixture
  mismatches in test_deployment_menu_text. The current build's production gate
  passes both deployment labels and complete current artwork composition.
- Package work/ps3_hardware_0.6.20_20260925: two-LOAD, original-metadata SELF;
  RPCS3 debug-SELF extraction round-trip verified. Preserved-layout ISO has
  554 files verified in BOTH trees, 5,011,013,632 bytes.
  ISO SHA256: 6f6bdf5ec348fb31366f660095faa26f2628867adc6cd2ee7f4ee8f451c1ec77.
  SELF SHA256: 1fdfa8adde8c40bab523c440ae21bc6c31d4686fabb4eeca16779237fd021c8d.
- Installed package snapshot to game/ with RPCS3 closed, dry-run then -Write.
  All 219 installed hashes match; all 18 save files unchanged. Backup and
  install receipt: work/install_backups/0.6.20_20260925_075836/.
  BLJS10256 registration remains E:/Projects/SRW Z3/game/; other game unchanged.
  No install cache was present to move; it will regenerate on launch. Runtime reports for THIS
  build remain pending on both targets; preserved-layout hardware status is
  candidate, not confirmed. No tag/release/upload/publication performed.
  Current installed version is 0.6.20; published version remains 0.6.19.

**2026-09-25 follow-up: required skill translated; two checks pending approval:**
- required_skill_levels.py adds exact Newtype L0-L9 hooks derived from existing
  canonical ui_hook:r_c6e2e5a0cf999610. Screenshot L3 was missed because the old
  exact hook ended at L, before the appended runtime digit. Composer/values
  untouched. Three new tests and production issue gate; seven required-skill/
  activation tests pass, full current EBOOT verified in memory. Latest free EXT
  after ALL extensions: 16,696 bytes (supersedes 17,176 below).
- User requested CHECKS for dialogue/alignment, not fixes to these: Mikono's
  stage0045_03:r_cdb750c9d380881a should say "looking after him" (Shotaro).
  Independent AI-assessed MQM review/challenge under work/mqm/shotaro_*;
  also flags "my wish comes full" fluency, with separate uncertainties retained.
  No dialogue wording changed this turn.
- Upgrade bonus descriptions use native Japanese-width centering before English
  hook replacement, producing right shift for lock message and left shift for
  A.T. Field +400. .19 descriptors 0x9e434/0x9e474 and 0xb8774/0xb8794 retain
  flag 0x40. No layout changes made; propose measured English centering scoped
  to these bonus fields when user asks to fix. Do not claim the bottom unit-name
  screenshot crop proves broken clipping/scrolling.
- Catalog zero issues, 543 compatibility views clean. No build/install/release.

**2026-09-25 unbuilt screenshot batch (after published v0.6.19):**
- Rare Igura / Igura are canonical glossary terms. Reported Jin line is "Makes
  no sense, Rare Iguras!" in both routes; 112 entries across 35 groups normalized
  with context-sensitive singular/plural fixes. Migration is dry-run-first and
  idempotent. Preserve the pre-existing unbuilt Ple Twelve edits.
- STG0500 member 1 is now fully translated and registered: 102 D-Trader ace
  scenes, 1,247 records (941 dialogue + 306 background markers). 918 unique
  source strings, zero check_stage problems. Both Sousuke branches covered.
  Original SDAT independently matches the pristine ISO; decrypted CPK SHA256
  6c4d7e6441d0f27cc9aabf73fc005158c47c3826ca4fb480fca91ceb080a668b.
  Source work/stage_dec/STG0500.cpk and work/lua500/STG0500_00001.lua;
  canonical stage0500_01. Build/deploy/extract/xdelta maps include STG0500.
- activation_prompts catalog: 17 activation strings / 18 pointers plus four
  dynamic skill suffixes / six guarded copy sites. New names/levels stay dynamic.
  PS3 integration only; do not claim Vita UI/code is ported. In-memory EBOOT
  patch + verify passed with 17,176 bytes free after ALL extensions. Six copy
  loops preserve registers other than original scratch r0/r8/r11; CR0 is dead
  at their tails. Buffer budgets are checked before patching.
- Added 16 activation-centering cells at 0x86E0..EF, verified blank in both
  font layers and disjoint from letters/library/tiny glyphs. Do not use row
  0x85: undefined CP932 codes there still hold native icons. VWF dispatcher
  grows 16 bytes; first generated keyword helper moves 0x78C310 -> 0x78C320
  inside the same cave (68 bytes; next helper 0x78C400). ELF segment/loader
  geometry is unchanged. All 215 padding cells / 12,900 positioning cases pass.
- Catalog zero issues; 543 compatibility views clean. Eight ace/Igura regressions
  pass; the combined 53-test ace/Igura, mission, catalog, battle-name, link and
  loader run passes, plus 20 activation/menu/deployment/save tests. No build,
  installation, version bump or release this turn; RPCS3 and real
  PS3 visual checks remain for the next explicitly requested build. The current
  installed/published build remains 0.6.19, not this source batch.

**2026-09-24 English 0.6.19 built, packaged, installed; release requested:**
Build work/build_0.6.19_english_20260924_r3 (strict). Hardware ISO
work/ps3_hardware_0.6.19_20260924 (preserved layout), sha256 8b4a3267...8d9935e4.
Installed (218 OK). Hook strings now start right after the emitted table,
which recovers ~22 KB of EXT; 25,958 bytes are free after the hook strings.
Release routes: original and the published 0.6.18 image
(work/ps3_hardware_0.6.18_preserved_20260923, sha verified).

**2026-09-24 unbuilt screenshot batch (after the published v0.6.18):**
Source only; no build or install has been requested. New modules:
- team_order_labels.py covers 85 Team Setup / Sub Orders / Custom Bonus
  widgets (accents moved to measured English positions, live-number gaps kept
  aligned) plus 8 EBOOT hooks.
- bonus_descriptions.py covers 236 Ace / Custom / Full Upgrade bonus
  descriptions (catalog group bonus_descriptions). They are exact hooks with
  keys pointing into the ELF (UI_ELF_RESIDENT) and no per-line pairs.
- **The EXT hook space now has only 3,466 bytes free** (5,383 of 8,191
  entries). Plan the next big hook batch accordingly.
Also Guren Mk-II (stage0042_03). Open items:
- The opening-movie series cards are burned into the USM video; the user has
  to decide whether to take on movie editing.
- The preset team names have not been located (see CHANGELOG).
More in the same batch:
- STG0700 end-session scenes are fully translated and are now a manifest
  stage (see CHANGELOG). suspend_scene.py is retired from the build.
- The numbered-condition indent is blanked (operation_indent.py).
- Warning: E:/SRWZ3 holds at least one patched stage SDAT without a .orig
  (STG0700). prep_stage now refuses non-pristine scripts.
- Ten non-story scripts remain: STG0400/0401/0500/0501/0600/0901/0903/0904/
  0905/0999.
At the next requested build, visually check both screens, the accent headers,
the result messages with numbers, and a Custom Bonus popup.

**2026-09-23 English 0.6.18 built, hardware-packaged, installed; release requested:**
The user explicitly asked for a GitHub release of 0.6.18. The strict build (no
--partial-translation) passed in work/build_0.6.18_english_20260923_r2. The
first attempt failed at a stale `< 4096` hook-count assert in
check_issue_fixes, now derived from the eboot NAME_STR/NAME_TBL layout. It
covers all unbuilt batches below plus stage 31B/32 wording fixes. Hardware
output: work/ps3_hardware_0.6.18_20260923. ISO sha256 e44b8130...6a275d57,
4,752,932,864 bytes. Snapshot installed into game/: 218 hashes OK, saves
unchanged, backup work/install_backups/0.6.18_20260923_091143. Snapshot
releases/0.6.18 + releases/0.6.18.json. Retro Trans builder v0.2.1 is
installed in ignored work/retro-trans/venv (Python 3.12 via uv, since the
system only has 3.8 and 3.11). Release routes: original -> 0.6.18 and the
published 0.6.14 -> 0.6.18 (work/release_image_0.6.14.iso, hash verified).
0.6.15-0.6.17 were never published, so they have no routes. Not yet
runtime-tested.
UPDATE: the fresh-layout ISO made a 3.1 GB xdelta (over GitHub's 2 GiB asset
limit). New platforms/ps3/preserved_iso.py (now the default; --fresh-layout
keeps the 0.6.15 writer) keeps the original disc layout, appends the changed
files, zeroes UDF, and applies the same stamp_disc header. Release ISO:
work/ps3_hardware_0.6.18_preserved_20260923, 5,010,685,952 bytes, sha256
0ed6c63a...0dfe83. Snapshot identical to the fresh package, so the install
is unchanged. Patches in work/retro-trans/ready_0.6.18: from-original
154,462,906 B, 0.6.14-to-0.6.18 28,467,132 B, both round-trip verified.
THE PRESERVED LAYOUT HAS NO HARDWARE BOOT REPORT YET: ask the user to test it
on the console.

**2026-09-23 unbuilt mission-condition coverage completion:**
User's Episode19 Operation End report maps to STG0031B, beyond the earlier
archive1-30 scope. Added180 canonical mission_conditions_all records with
source/role provenance. All259 unique extracted conditions now translated;
expanded audit:2119 variants over142 archives,0 untranslated. The inventory
also includes other UI labels; do not describe2119 as unique mission strings.
Episode19 SR target is20,000 HP within4 turns. All numeric/turn/name conditions
reviewed; ambiguous Kouji/Zeus defeat verified as OR from original script.
Twelve established glossary aliases added, including Peace Memorial Hall;
Mechanical Beast singular avoids changing RPW enemy text, with mission plural
outside token. Generated analysis/glossary.json only; other legacy views intact.
tools/mission_catalog.py scans all archives, exports only with --out + --write.
mission_conditions handles Lua/CP932 display escapes and checks shared line
translations for conflicts; exact fragments override unsafe generic pairing.
EBOOT hook table now8191 capacity; identical encoded English is stored once
(padding/tutorial punctuation included), separate from immutable Japanese keys.
EXT_VA/EXT_SIZE and LOAD geometry unchanged. In-memory table tests only; full
build/runtime result remains pending. All52 focused tests pass;5139 hook entries,
0 skipped,22,088 bytes headroom. Canonical/541 compatibility views pass.
Shared text plus PS3 adapter, not a Vita
executable port. No build/install/version/release authorized this turn; English
0.6.17 remains installed, and September20/22 unbuilt fixes below are preserved.
Next requested build must use the proven hardware+RPCS3 method and check mission
screens, including Episode19, plus the earlier pending screenshot fixes.

**2026-09-22 unbuilt Space Demon King Soldier corruption candidate:**
New screenshot has "Space Demon Kin" plus corrupt glyphs. Canonical enemy
ID enemy_names:r_50e87a2fb9246781 already supplies the complete name. All12
pilot-nw refs to source RPW index3521 contain full English in frozen.17.
Added that ID to battle_name_rendering.MESSAGE_IDS, extending existing
short-native-key/exact-draw-hook approach to70 refs across three names.
The source key 宇宙魔王兵 is10bytes, with no conflicting hook; joined army
宇宙魔王軍 and king 宇宙魔王 labels are preserved. Twenty-eight focused
tests pass, including emitted PPC hook simulation and untouched other slots.
No runtime reproduction of native copy site; needs affected-battle testing.
No build/install requested; .17 remains installed and September20 fixes below
remain unbuilt. No canonical wording changes, version bump or publication.

**2026-09-20 unbuilt screenshot fixes:** Sword-icon Unit Data Help translated
in canonical ui_utf8:sword_icon_help, guarded VA0x71fa20/ref0x858bcc through
battle_screen_labels. Fa stage0028_03:r_a84ab0c3c1ba44d4 (t_1,n253) now says
"that guy": reviewed27 neighboring records confirm Issei as the referent.
Added24 ui_aiddata:name_entry_* labels and tools/name_entry_labels.py;
build_ui and EBOOT exact hooks consume them, check_issue_fixes checks both.
Selectable character grids, entered/preset names, widget placement and input
behavior preserved. PS3 UI implementation only; shared Fa text covers both.
Fifteen focused tests pass plus target Fa constraints and frozen.17 UI
compatibility. Canonical check:0issues/541views. Sync regenerated only
translation/stage0028_03.json (format normalization, one semantic correction).
No build/install requested this turn; English0.6.17 below remains installed.
Next requested build must still use the proven hardware+RPCS3 workflow and
visually verify these new labels. No publication or version bump.

**2026-09-19 English 0.6.17 built, dual-target packaged and installed:**
User explicitly requested build and confirmed replacing the Vietnamese test
installation with English. RPCS3 closed before installation. Current source
output work/build_0.6.17_english_namefix_20260919 passed preflight, canonical
compatibility (0issues,541views), full packed/UI gate and40 focused/loader
tests. This includes both source batches below. Fourth Angel/Neo Zeon still
need affected-battle runtime verification; Mariemaia remains unresolved.
Shared source fingerprint stayed78352dc4e98146987c69d322d407674feb3ba5c8d2b3ae7773c5e99a908c9e61.
Font mapping identical to frozen English.16. New STG0025 member3 equals.16
with exactly132 malformed half-width quote bytes removed; no other differences.
Build remains partial:1034 untranslated mission variants documented.

Hardware output work/ps3_hardware_0.6.17_namefix_20260919 (dry-run then write):
SRW-Z3-English-0.6.17-hardware-test1.iso,4752932864bytes.
ISO SHA25660350a8c9715908541db11b4715d6f67a5b223ecba041fb2f33aa9627b082dfa.
Delivered SELF832b5721db1346d25029dabf52164bb26614e7833f2039c6f2da2fd7347214d1.
Raw ELFe025175e127ec00d2d61d419cc3b4950a5bcc4872b9c691f0eca2f9c89d840e6.
Folded ELF55d1d0e849c61e494f58aefbaf7a42b052a2c16946042b6666821ae042db8451.
Source manifest e8edfebe0ef29433d96c0b99d9dcde3e584a7e7f4e3c1e83c604f135b565874d.
Two-LOAD/fake-SELF/RPCS3 extraction checks pass;554members verified in both
ISO9660 and Joliet. Same derived snapshot installed to game/ with dry-run
then approved -Write. All218targets and complete disc hash-verified;
18savefiles unchanged. Backup work/install_backups/0.6.17_20260919_161343.
Cache absent, so cache_moved:false. Existing other-game registration retained.
Registration immediately before install pointed at separate Vietnamese
0.6.18hardware ISO; now BLJS10256 points at game/. Those prior outputs are
preserved. Post-install SELF hash and registration verified. Receipt copied
to hardware output/install_audit.json; immutable HARDWARE_TEST_AUDIT.json
keeps its original installed:false, with later installation in receipt.
No agent gameplay launch, Vita build, xdelta, release, tag or publication.
Logs: matching work/build_0.6.17_english_namefix_20260919.log and hardware
output-name{_preflight,}.log. Counter/footer English0.6.17 (separate from the
previous Vietnamese test's independently assigned display number).

**2026-09-19 Fourth Angel/Neo Zeon source candidate (now in English0.6.17):**
User asked to find a fix. tools/battle_name_rendering.py keeps original
short RPW strings for 第４の使徒/ネオ・ジオン兵 (indices1778/4205,58 refs:
10/48), then existing exact name-hook selects the complete canonical English
at draw time. build_project filters normal swaps BEFORE glyph reservation
and filters per-slot overrides too; English letters explicitly pooled.
eboot.load_ui_hook adds exact entries and rejects other-hook conflicts.
check_issue_fixes checks both short RPW keys and full executable hook text.
No new PPC production instructions, lookup-table mutation, abbreviation or
translation change. Same PS3 hardware/RPCS3 packaging rules still apply.
Six new in-memory/PPC tests pass; existing10 battle-label+5 quote+6 identity
tests pass. CPU harness gained andis. support for existing name_stub code.
Copy simulation is NOT actual native-path reproduction. Exact truncation
site remains unknown; do not call this runtime-fixed until new affected
battle test. Mariemaia left alone: key also names the joined/plural squad
label "Mariemaia Soldiers"; a global singular override would regress it.
No build/install/version/publication this turn; preserve current live game.
Read-only disassembly helper work/trace_battle_name.py. UTF-8 battle table
VA0x85d410 via TOC-0x62d8, setup0x104fb4/0x1050c0/0x105114. Three original
UTF-8 names remain Japanese in frozen.16; RPW full English already verified.
Earlier "unresolved" notes below describe historical shipped builds; the
new workaround is source-only, while Mariemaia still needs its own solution.

**2026-09-19 Episode25 quote source fix (now in English0.6.17):**
User confirmed these new screenshots are .15. Alto/Watta/Ryouma/C.C. map to
stage0025_03 t_1 rows363-367. Corpus scan found66 English rows in that member
with accidental nested half-width corner quotes (U+FF62/FF63); no other
English half-width rows. Removed only those wrappers, keeping normal「」,
tokens, controls, links and IDs; no meaning changes. Status translated.
digraph.split_mixed now rejects all U+FF61..FF9F (single CP932 high bytes
that break the two-byte glyph stream), for letter/pair/hybrid paths and
check_stage. Five new tests in tools/test_dialogue_halfwidth.py pass, plus
ten battle-label tests. Frozen .15 and .16 STG0025.SDAT.cpk member3 both
contain all66 bad wrappers. In-memory re-patch matches each exactly after
removing132 quote bytes; all other member bytes unchanged. Full stage check:
966records,803uniqueanswers,0problems including widths. All60653 manifest
dialogue records pass updated tokenizer. Canonical0issues,541views match;
only translation/stage0025_03.json synced after inspecting66 en-only edits.
No complete build, installation or publication performed by this task.
Mariemaia Soldier name corruption remains unresolved, like Neo Zeon Soldier
and Fourth Angel. Added Mariemaia to frozen RPW complete-name regression.
32-byte copy sites below are still only leads; requested exact battle/save.

Live-install observation during this task: game/build_manifest.json now says
language=vi,kind=story-test,title_footer_version=0.6.17; installed SELF hash
db8504531397876ba14a5c8f4b8a290d4ce2b2f9e3fb89132238c2b5d23a3d04.
This task did not install it; preserve that separate work and recheck live
state before any future deployment. Use frozen English artifacts for tests.

**2026-09-19 English 0.6.16 built and installed at that time (history):**
User explicitly resumed "ok build" after Toji. All five source-fix batches
below are now included; their no-build/hold notes are historical session state.
Source output: work/build_0.6.16_batched_source_20260919.
Full preflight and packed/UI gate passed; counter/footer0.6.16. 70 focused
tests pass (packaging test import needed PYTHONPATH=tools;platforms/ps3,
then passed). Stage17 members3/4 and stage19 member3 checks pass. Font mapping
is identical to .15; no kanji fallback needed. Canonical fingerprint:
be0785735caf44afda49bdba3fec93e96930689f9ed9ddc6cf814e26a5eef16c.
Translation is partial:1034 untranslated mission variants remain documented.

Hardware package: work/ps3_hardware_0.6.16_test1_20260919/.
Dry-run then --write passed guarded two-LOAD fold, original-metadata fake
SELF, RPCS3 extraction and all554members in both ISO9660/Joliet trees.
ISO: SRW-Z3-English-0.6.16-hardware-test1.iso,4752932864bytes.
SHA256 d572a2a238e0fe12ac4c4c66a504921e996daf9f167568bbdcfe9931107c0fe6
Delivered SELF330b7d8ccf18d88bd051603b76f3df2b74337be5b07f28e0a86b0b9fd170c1bf
Raw ELF cdc6ee76d181cc73f61f8f605f91d2c366e00966221faa8a764e62b5cc21e420
Folded ELF24f63043b071dea82246da92d35a354f605c24ddc085fb656b7285232ad6ca38
Source manifest94d64afd8592d559792d151cac10f6a1940fe86ac363b610bce9621e61da45c0

User closed RPCS3. Installer dry-run then -Write installed the derived
snapshot to game/,218targets and complete disc verified,8savefiles unchanged.
Registration changed from .15hardware ISO to game/; BLJS10299 preserved.
Backup/cache: work/install_backups/0.6.16_20260919_113739.
install_audit.json also copied into hardware output. Build-time audit remains
immutable with installed:false; separate receipt proves later installation.
Logs: work/build_0.6.16_batched_source_20260919.log and
work/ps3_hardware_0.6.16_test1_20260919{_preflight,}.log.
No runtime launch/test by agent; both targets need fresh .16 gameplay checks.
Preserved known-good .15hardware baseline. Long battle-name corruption below
is unresolved. No Vita build, xdelta, release/tag/upload/publication.

**2026-09-19 Toji source fix (now included in 0.6.16):**
User interrupted the build request before any build command started with
a report of Toji's Japanese name during battle in scenario 13, entering Eva.
Added glossary:r_0de2d941a5560480 / Toji to battle_screen_labels.UTF8_BINDINGS:
source VA0x6ed118, sole ref0x84e1c8, original file slot0x6dd118..0x6dd127.
12-byte encoded name plus NUL fits16; existing UTF-8 path handles it in place.
Frozen .15 executable confirmed still Japanese at that reference. This fixes
the verified missing binding; exact reported scene not runtime-reproduced.
Corpus scan:123 dialogue mentions,2 glossary,2 library,1 UI; no untranslated
Toji story speaker headings found. Canonical text unchanged; zero issues,
541 views match, sync dry-run zero changes. Ten battle-label plus five
Berserk tests pass. Full build/install remain held; no version increment.

**2026-09-19 Berserk and Stage 19 source fixes (now included in 0.6.16):**
Three canonical stage0019_03 rows changed (t_1 27-29): Johnny's "charges
ahead of the competition", Eida's "Dodge this, or you'll get the point",
Sakuya's "walking rhino joke". Setup unchanged, glossary tokens preserved.
Independent meaning review read 11 context rows; full stage check passes
349 records / 314 unique answers, font widths included. Generated view synced;
canonical zero issues, all 541 views match. No scored MQM claim.
New tools/berserk_banner.py uses abilities:r_3633df5b7b8f47fa for BERSERK.
Pristine EFFPS3 member307 hash guarded; GTF0x7dd80 texture0 is swizzled
ARGB512x128. Changes only y8..39 solid and y40..79 outline lettering.
All animation/UV/tint/wave/other textures byte-identical. Preserves transparent
black background; dark-composited preview visually checked at
work/ability_banner_review/berserk-English-preview.png. Five focused tests
pass, plus all nine battle-label tests. location_caption.py builds the sprite;
check_issue_fixes.py and check_deployment_locations.py verify it separately
alongside the existing archive-isolation check. Canonical asset mapping added.
PS3 only: Vita sprite not source-mapped. No build/install/version increment;
runtime appearance pending the next explicitly requested build. Earlier
Fourth Angel/Neo Zeon Soldier name corruption remains unresolved below.

**2026-09-19 Eva source fixes (included in 0.6.16); name corruption unresolved:**
User unsure which build produced these screenshots. New direct-catalog IDs
ui_aiddata:sync_rate and ui_utf8:barrier_icon_help translate widget0x9e394 and
UTF-8 VA0x71fe58/ref0x858be4. tools/battle_screen_labels.py now guards three
UI widgets and three UTF-8 bindings (Tetsujin, Misato, barrier help).
Misato glossary:r_bb5d440e312db945 UTF-8 VA0x6ed090 has four refs:
0x84e190/194/224/228. New encoded name fits the 16-byte original slot;
help and Tetsujin relocate. All9 focused tests pass; canonical zero issues,
541 compatibility views match, no generated-view changes. No build/install.
Fourth Angel name is NOT runtime-fixed. Current .15 RPW slots are complete
and correct (test now covers it and Neo Zeon Soldier), but both screenshot
names break after roughly15 letters. Investigate fixed byte-buffer copying;
do not dismiss correct packed data as proof of correct runtime display.
Read-only leads (unconfirmed nameplate provenance): function0x33b410 copies
32 bytes then writes NUL at31; callers0x33eb98/0x33f12c. Function0x189754
copies32 bytes to global+0x20 and256 to+0x40; no direct bl callers found.
Function0x166d38 uses alternating32-byte slots with a30-byte terminator.
No speculative code changes made. Need known-build reproduction/trace before
choosing a bounded fix. Inspection helper: work/inspect_eva_screens.py.

**2026-09-19 Stage 17 joke adaptations (now included in 0.6.16):**
User flagged lost wordplay in two screenshots. Changed four canonical rows:
stage0017_04 t_005 1/2/4 now uses "Count Me-Out" and a matching count/count-me-out
explanation; stage0017_03 t_2 58 uses Rhino / "thicker skin" instead of
"rhino-ference". Deliberate English adaptations, not literal retention of
hakushaku/hakushon or sai homophones. Following reactions and glossary tokens
unchanged. Independent AI meaning review read 22 contextual rows; no MQM
score claimed. Canonical check zero issues, 541 views match; two views exported.
Both complete stage members pass check_stage.py, with font-based widths.
Source only: no build/install/version change, no new runtime test.

**2026-09-19 battle-label fixes (included in 0.6.16); screenshots from Sept17:**
User initially selected RPCS3 .15 but then corrected: report is from Sept17,
an earlier build. Do NOT record these as proven .15 regressions.
Added tools/battle_screen_labels.py: canonical KO Risk / Armor: (two new
ui_aiddata IDs, verified original widgets0xa9754/0xa9794), preserving all
positions/styles/skulls/numbers. Missing UTF-8 Tetsujin binding reuses
glossary:r_33d597bb4a2bdf96; source-guarded refs0x84d46c/0x84d4d8 use the
existing UTF-8 relocation path, not unsafe CP932 name-key rewriting.
Integrated into build_ui.py, eboot.py and full check_issue_fixes.py gate.
Read-only/in-memory tests: all 7 in tools/test_battle_screen_labels.py pass. No full
build/install; counter remains.15 and confirmed hardware baseline preserved.
Existing .15 contains all14 registered weapon-requirement UI widgets in
English; current RPW Neo Zeon Soldier slots contain the full correct English
glyph bytes. Both old runtime reports need a fresh .15 reproduction before
claiming a new bug or speculative buffer/renderer changes. If requirement
rows still appear Japanese, inspect dynamic ELF strings around0x7115b0 and
pointer table0x859194 (may override translated static AIDDATA widgets).
The UTF-8 battle-name table is separate from the CP932 display-name hook.

**2026-09-19 hardware success confirmed; dual-target packaging is now mandatory:**
User replied to the .15 hardware-test delivery: "it works, remember this build
and always build so both hardware and emu work". Record this as user-confirmed
success on the requested physical-PS3 test, with exact firmware and gameplay
coverage unspecified; no agent-run runtime test or separate explicit .15
RPCS3 runtime report. Preserve the ISO/snapshot below as the known-good
hardware baseline. Future PS3 builds must use the same guarded two-LOAD +
original-metadata fake-SELF packaging, and deploy the derived snapshot to
RPCS3 so hardware and emulator use identical executable/assets. See the new
top-level CLAUDE.md rule and platforms/ps3/README.md. Do not revert to plain
ELF deliveries, silently relax loader guards or claim all firmware supported.
No rebuild, installation, counter increment or publication in this follow-up.

**2026-09-19 current-source PS3 hardware build (local only):**
User requested a new hardware-test ISO and explicitly selected **current
translation edits**, not the frozen .14 text. Full build dry-run passed
(canonical checks: zero issues, 541 compatibility views unchanged), then
`tools/build_project.py` built and validated **0.6.15** in
`work/build_0.6.15_hardware_source_20260919`. Counter/footer agree. Includes
141 story archives (60,653 records), shared end-session archive (16 records),
31,666 battle subtitles and 4,019 executable hooks. Full packed/UI gate
passed; 1,034 untranslated mission variants remain explicitly documented.
Canonical source fingerprint: be56342998f32a805ec9e470eab731f16a02faba8fc481f2e4e89918c3c93b43.
No canonical translation edits made in this build turn.

New `platforms/ps3/package_hardware_current.py` dry-run then --write uses
the original Japanese ISO and new .15 snapshot. The existing guarded
two-LOAD fold was reused unchanged, followed by original-metadata fake SELF
wrapping; no claim of new proven hardware compatibility. Fresh ISO9660 and
Joliet image, all554members verified in each tree. Output:
`work/ps3_hardware_0.6.15_test1_20260919/SRW-Z3-English-0.6.15-hardware-test1.iso`
4,749,131,776bytes; SHA256
`f0b94d9666c1703daf27b05a1d47d401443cdd70d3da73b2497c7ea23ae7abe9`.
SELF: `46f0e30fde96d61d62316e96fdbd0fa0db59638021880cc5c77725728843962f`.
Raw ELF: `b02c7df7a2da19f3f6c6dd53a34fdefed22ec364e0fe34df4233016d8b6498a1`.
Folded ELF: `95dbc998d431dd5fcca5d2fcabcf7cd0f3836c3d7e83231df345970c2dfd6f46`.
Source build-manifest SHA256:
`9c55437de407d731b2aa96140dc45a94550f037fa1090ddee579bc083db0acd5`.
Derived installer-compatible `snapshot/` records this provenance and wrapper
hash; no version renumbering during packaging. HARDWARE_TEST_AUDIT.json,
SHA256SUMS.txt and README accompany it. Guide: docs/PS3_CURRENT_HARDWARE_TEST.md.
Full logs: work/build_0.6.15_hardware_source_20260919.log and
work/ps3_hardware_0.6.15_test1_20260919.log.

76 focused tests pass. Separate historical test_ps3_startup_menu fixture
failed its pinned-older-UI check because it reads the updated live game;
not weakened or silently skipped as a pass. Full new source build validated
startup artwork/isolation and widgets against original assets successfully.
At packaging time, this exact .15 build had not been runtime-tested on either
target. The later user hardware success report above supersedes that status;
the older .14 RPCS3 confirmation must not be reused as proof for .15.
No xdelta requested/built, no release/tag/upload/commit/push. Old images
preserved. The abandoned same-content .14 repack draft was removed before
building when the user chose current edits.

Default RPCS3 installation COMPLETED after installer dry-run then -Write:
all218targets and complete disc verified, eight save files unchanged;
registration remains `game/`. Backup/cache retained at
`work/install_backups/0.6.15_20260919_081855`. Installation receipt also copied
to the hardware output's `install_audit.json`. HARDWARE_TEST_AUDIT.json is
immutable build-time state (`installed:false` at packaging); the separate
receipt proves later installation. RPCS3 was closed, not launched or tested.
The immutable hardware audit's `hardware_tested:false` likewise describes
packaging time; later user confirmation is recorded here, not retroactively
inserted into the build-time audit.

**Save converter moved to Retro Trans (2026-09-18, local/unreleased).**
The maintained converter and compact Windows interface now live in
`../retro-trans-tools/retro_trans/z3_saves.py` and the **Z3 saves** tab of
Retro Trans. Choose PS3 to Vita, Vita to PS3, or both directions; check both
save profiles before converting. The bundled guide is
`../retro-trans-tools/retro_trans/resources/Z3-SAVE-CONVERSION.txt`.
Supports decrypted Jigoku-hen RPCS3/Vita3K saves only; it does not decrypt,
resign or install physical-console saves. Existing standalone 0.6.14 files
and historical packagers remain as compatibility references. Develop and
distribute future converter changes through Retro Trans, not another Z3
standalone package. No version tag, release, upload or publication is authorized
by this migration. Game builds, installed games and live saves are unchanged.

Everything a fresh agent needs to continue. Read this first, then
`docs/FINDINGS.md` for the format chain.

**2026-09-18 PS3 dual-target candidate BUILT AND INSTALLED; RPCS3 user-confirmed:**
User now reports "work on RPCS3" and requests an xdelta. Scope of gameplay
testing unspecified; physical console still unconfirmed. From-original
packager platforms/ps3/package_dual_0614_xdelta.py added; no new game build
or install needed. The previous 3.7MB incremental .14 patch remains valid.
From-original package COMPLETED in work/ps3_dual_0614_xdelta_original:
SRW-Z3-English-0.6.14-dual-test1-from-original.iso.xdelta, 154,840,781bytes,
SHA256 d2c737448c4134c05a17e8234f180019fdaac8edf3a6da4aed10942c50cd43b7.
Dry-run then write; decoded against original Japanese ISO and SHA256 matched
the exact tested dual-test1 target. PATCH_AUDIT.json, README.md and checksums
accompany it. Temporary verified decode removed; source/game files untouched.
No upload/release replacement, commit, or push in this follow-up.
User clarified "both" means RPCS3 and physical PS3. Added
platforms/ps3/build_dual_0614.py, tools/test_ps3_dual_0614.py and
docs/PS3_DUAL_TEST_0.6.14.md. Frozen .14 ISO/EBOOT pinned, legacy guarded
two-LOAD fold reused unchanged and pinned fself wrapping retains original
application metadata. The other 553 disc files match .14 exactly.
Output work/ps3_dual_0614_test1, with installer-compatible snapshot.
ISO SRW-Z3-English-0.6.14-dual-test1.iso: 5,012,193,280bytes,
SHA256 e2be81330cc2e45d8317271c8e290f7cde768749b4ea681114efd95b498c63c7.
Incremental SRW-Z3-English-0.6.14-to-dual-test1.iso.xdelta: 3,701,866bytes,
SHA256 8531cc38222f66d7d7370a0d6b9c0ad21f0dd848eb4f358fc4d7c566137c2931.
SELF SHA256 c3804f9ad8de9d2a9e17e044a5b1df19d9981154a268d136026f4992775fbc0c.
All554members checked in both trees; delta decoded/hashed exactly; temporary
decoded duplicate removed. 31 synthetic tests + four link geometry guards +
77 date-card guard checks pass. RPCS3 debug-SELF extraction mirror matches.
AUDIT.json records build-time state, not a hardware/runtime claim. Firmware
unknown; async question asks same earlier console/setup or CFW/HEN version.
No GitHub release changes; no stock PS3 or blanket HEN support claim.
Installer dry-run then -Write completed: all218 game targets match, eight
save files unchanged. Backup/cache retained at
work/install_backups/0.6.14_20260918_083921; registration still game/.
Computer-use launch was denied: "Computer Use was not approved to use RPCS3".
No automation fallback attempted; user must launch/test or enable app control.
No agent-run runtime test occurred; later user RPCS3 confirmation above.
Build-time AUDIT.json remains immutable (installed
false describes packaging time); later install_audit.json proves deployment.

**2026-09-18 physical-Vita release ADDED to v0.6.14:** user asked to include
hardware support. Public SRW-Z3-Vita-Hardware-0.6.14-from-original.zip is published
(14,058,604bytes; SHA256 c98941abbb041481114cdbd39f5fd65555c8e8ace126af929d23e755ab4f2608).
It contains120 from-original deltas (frozen from existing Vita3K .14 package,
excluding5convertedmodules),3stdlib scripts, guide and manifest. NO game files,
auth dump, license, firmware, plugin or saves included. 8releaseassets now;
new asset size/hash verified and other7IDs/digests unchanged. Notes updated.
New tools: tools/package_vita_hardware_release.py, tools/apply_vita_hardware.py,
tools/test_vita_hardware_release.py; auth sanitizer extracted without behavior
change from build_repatch.py into platforms/vita/repatch_auth.py. All16 tests pass.
Generic guide docs/VITA_HARDWARE_RELEASE_0.6.14.md requires original PFS-decrypted
PCSG00264 v01.00, user-local matching self_auth.bin, Python3.8+ and xdelta3.
No no-Python hardware-applier exe was requested/built; save converter is separate.
Built/extracted release in work/release_0.6.14_hardware; ran extracted applier
dry-run then --write using our original game + private root self_auth.bin.
Local ready-to-copy overlay is work/vita/release_0614_hardware_verified/rePatch/PCSG00264;
local ZIP SRW-Z3-Vita-rePatch-0.6.14-hardware-test.zip in same parent94,273,385bytes.
All120patchedfiles + sanitizedauth and all123ZIPentries verified. EBOOT matches
f79fcef07290bbc5c9b4c191c7109514fc7fc97ec191bfebb3be0e77de65ae0d (currentv4).
Only local output includes sanitizedauth; raw input unchanged, secrets zeroed.
No device/emulator installed or modified. Exact hardware boot/save/load NOT tested;
release explicitly labels hardware test candidate. Do not upload local ready ZIP.

**2026-09-18 Tool Updates supplement withdrawn:** removed exact GitHub asset
570608106 (SRW-Z3-0.6.14-Tool-Updates.zip) at user's request. Remaining7
asset IDs/digests unchanged; local matching ZIP retained. Release notes updated,
including source-tag limitations. Do not re-upload any of the four withdrawn
assets from historical upload plans.

**2026-09-18 Python-only converter withdrawn:** removed exact GitHub asset
570598351 (SRW-Z3-Save-Converter-0.6.14.zip) at user's request. Remaining8
asset IDs/digests unchanged; Windows-x64 converter stays. Notes now advertise
only the portable converter; local original ZIP preserved for recovery.
Do not re-upload any of the three withdrawn assets from historical plans.

**2026-09-18 standalone checksum attachment removed:** user requested removal
of SRW-Z3-Save-Converter-0.6.14-Windows-x64.sha256 from v0.6.14.
Deleted exact asset570714423; verified remaining9 asset IDs/digests unchanged.
Windows ZIP remains available. Its SHA256 is now directly in release notes;
local .sha256 preserved. Do NOT re-upload either withdrawn asset automatically.

**2026-09-18 Vita incremental release asset withdrawn:** user explicitly removed
SRW-Z3-Vita3K-0.6.14-test16-linkfix-v3-to-0.6.14.zip from GitHub v0.6.14.
Deleted exact asset570595915; verified absent, remaining10 IDs/hashes unchanged.
Release notes/docs/RELEASE_0.6.14.md no longer advertise/instruct that patch.
Local work/release_0.6.14/ ZIP preserved with matching SHA256 for recovery.
Old UPLOAD_PLAN.json/metadata are historical: do NOT re-upload withdrawn asset.

**2026-09-18 portable Windows save converter PUBLISHED on v0.6.14:**
User requested no-Python app and approved building/adding it to existing release.
New tools/save_converter_gui.py: Tk folder pickers, explicit emulators-closed
checkbox, check-before-convert, worker queue, new app-adjacent work/ output,
public instructions and no live installation. Core convert_z3_saves.py adds
optional guide_path and expected_sources guard; binary conversion is unchanged.
tools/build_save_converter_windows.py builds explicit app sources with a clean
Python3.12.14 x64 venv and PyInstaller6.22.3; no global Python installation.
All19 tests (test_save_conversion + test_save_converter_gui) pass from source,
frozen exe and extracted ZIP with invalid Python paths/minimal PATH, including
spaces/Japanese characters in extraction path. Computer Use checked the real
window/instructions; the test app is closed. No emulators/saves were changed.
Portable output: work/save_converter_windows_build/package01/dist/SRW-Z3-Save-Converter.
Distribution: work/release_0.6.14_windows/SRW-Z3-Save-Converter-0.6.14-Windows-x64.zip
(13,556,876 bytes), SHA256 b786a21490af231ba8621e21de09a0a55d3fe49785ef92c3a6225e23defc5007.
ZIP includes full _internal runtime, six exact source/doc files, runtime licenses,
README and BUILD-MANIFEST.json. No game data, real saves, account info or keys.
Only this ZIP + same-name .sha256 were added; ALL11 GitHub asset hashes/sizes
verified and original9 assets unchanged. Existing manifests cover original9;
the .sha256 covers this addendum. Release notes updated from docs/RELEASE_0.6.14.md.
Tag/repository visibility unchanged; standalone source is in its ZIP, not tagged.
Unsigned Windows-x64 community executable; no bypass-security advice.
App's test mode: exe --self-test NEW_REPORT.json (synthetic data only).
Local diagnostic reports contain temporary paths: never upload these reports.

**2026-09-17 release 0.6.14 PUBLISHED:** user confirmed both latest
dialogue fixes work, requested GitHub release and approved porting to 0.6.13.
PS3 guarded port builder: platforms/ps3/build_release_0614.py, output
work/build_0.6.14_release. Carries only three changed files into frozen .13;
the working deployment list's 32 additional stages come from the original ISO.
Current editable suspend-scene and Unit Info currency changes are NOT included;
their checks explicitly compare the frozen .13 bytes. Startup art validation
now accounts for the new pass. Do not claim new merged build runtime-tested.
Vita delta packages and save tool bundle: work/release_0.6.14, created by
tools/package_vita_release.py. 125 original-to-current file patches and one
test16-linkfix-v3-to-current EBOOT patch, each independently decoded/hashed.
Portable tools/apply_vita_release.py supports dry-run, new output and local
install ZIP. docs/SAVE_CONVERTER_RELEASE.md is the generic public guide;
docs/SAVE_CONVERSION.md remains a private/local example and is NOT bundled.
Both emulators were running, so no new installation or cache changes.
GitHub v0.6.14 published as latest non-prerelease at 2026-09-17T16:30:03Z:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.14
ALL9 remote assets checked against local names, sizes, SHA256 and uploaded state.
Release-metadata-only commit
17dd5e65b70ac88c48110f7216dd10e03b8a7d4d is pushed to master (four files:
version counter, release snapshot hash manifest, two generic guides).
Both PS3 packed validation and all64 focused tests passed. Snapshot218files;
per-file delta set186 original+3 incremental decode-verified. Combined ISO
work/release_image_0.6.14.iso has218 verified files,4,998,940,672bytes.
Both ISO deltas now decode-verified: full151,153,200bytes SHA256
84f8f7f6cb13cb304e5fc75add226f7362f915409f547b8aaee614120be564cf;
incremental2,121,180bytes SHA256
430cf235c4bb315178d823775ab91dfca8f5f32b497680b204c2cf691ffac654.
Target ISO SHA256 c15b65a87d35cb4f3478fba829b4f14e6307de96b64979fdbc400b1d25e02462.
Vita end-to-end patch+installer test passed: all589 ZIP payloads match target.
tools/finalize_release_0614.py dry-run then --write completed. Explicit9-asset
plan/checksums/source-tool supplement under work/release_0.6.14/.
Full151MB PS3 upload completed successfully, as did the other8 assets. No jobs
remain pending. UPLOAD_PLAN.json is the exact allowlist; source overlay is intentional
because unrelated local changes remain uncommitted. Do not upload full ISO,
the full Vita installer, raw saves, licenses or self_auth.bin.

**2026-09-17 RPCS3 v5 and Vita3K v4 INSTALLED at user's request:**
Ran `work/Install-Dialogue-Links-20260917.ps1` dry-run first, verified old/new
executable and ZIP/payload hashes, then ran -Write with approval. RPCS3 was
already closed; gracefully closed Vita3K PID32472. Replaced ONLY:
- `game/PS3_GAME/USRDIR/EBOOT.BIN` with verified
  b7560a584f602513c2017f30c20f14d27b8c7fee64fa5fdff87f9e91048986da.
- `C:/Users/Binh/AppData/Roaming/Vita3K/Vita3K/ux0/app/PCSG00264/eboot.bin`
  with verified f79fcef07290bbc5c9b4c191c7109514fc7fc97ec191bfebb3be0e77de65ae0d.
Old executables and staged new files retained in
`work/dialogue_links_installed_backup_01/` (RPCS3-before.bin, Vita3K-before.bin).
No savedata, fonts, archive assets, authentication material or install-cache
changes. Both emulators left closed. This supersedes NOT-installed below;
in-game dialogue/backlog visual confirmation still needs the user to retest.

**2026-09-17 dialogue-only link fix built: RPCS3 v5 / Vita v4, NOT installed:**
User reports dialogue backgrounds absent on both, backlog now fine. Verified
live PS3 remains v4 `4d30f693...`, Vita3K remains v3 `8289b78b...` before/after.
Normal dialogue registration has no explicit scene context; backlog sets/clears
it. Prior primary rectangle lookup required a matching scene and glossary ID,
but registration stored null and skipped ID resolution. New wrappers retain
explicit backlog scenes and use scene zero only for null dialogue context.
PS3 hook1ce1b4/helper78efc0 (48bytes), Vita810d8d86/helper810d6a64 (14bytes).
Only43 actual PS3 bytes and16 Vita text bytes differ from their last patches;
all Vita other segments, name/date/backlog geometry and assets are unchanged.

Artifacts (all under work; no installs, saves, cache or authentication changes):
- `work/ps3_dialogue_link_v5_20260917/SRW-Z3-PS3-RPCS3-v5-dialogue-links-update.zip`
  3,512,571bytes; ZIP82290faee6c7eb08378c31ecbb2e1f9f339acd8db85fb728bf1ec012b59b7a52;
  EBOOTb7560a584f602513c2017f30c20f14d27b8c7fee64fa5fdff87f9e91048986da.
  Requires pinned v4, EBOOT-only: NO install-cache deletion needed.
- `work/vita/vita3k_linkfix_install_04/SRW-Z3-Vita3K-test16-linkfix-v4-install.zip`
  1,872,598,798bytes; ZIP954a452c9c1a492ebf9952ab2c42b1152b558027178bd136aeaaa77adf5ad70a;
  EBOOTf79fcef07290bbc5c9b4c191c7109514fc7fc97ec191bfebb3be0e77de65ae0d.
  Full Vita3K installer, all589files verified via size/SHA256/CRC.
- Physical/manual overlay and standalone EBOOT: `work/vita/link_background_test16_04/`.

26 PS3 +16 Vita tests passed, including old null-scene negative controls,
native registration into primary geometry, explicit backlog references,
ABI/relocation and prior date/name/loader checks. Tests use native instructions
with external-call fixtures, NOT in-game visual confirmation. Retest both
Destruction Incident/Regeneration War, speaker, follow/return, backlog, later
scene. Vita builder now qualifies platform imports to avoid same-name PS3
modules being selected after ui_text modifies sys.path. Full PS3 eboot builder
opts into the new scene fix; historical v3/v4 packagers retain old defaults.

**2026-09-17 old RPCS3 install-cache backup deleted at user's request:**
User explicitly requested deletion instead of keeping the cache backup.
Validated exact path E:/RPCS3/install-cache-backups/BLJS10256_DATA-before-v4,
no reparse points,192files/4,035,384,618bytes and original UI checksum; deleted
only that directory and verified absence. Permanent deletion (not Recycle Bin).
Active/rebuilt cache, game files, saves and the separate v4 game-file backups
were untouched. The deleted cache can be regenerated by the game, but the
old backup itself is no longer available. This supersedes the retention note below.

**2026-09-17 RPCS3 stale install cache backed up after user approval:**
V4 boot reported Japanese game-data corruption. Confirmed cached
USRDIR/INSCO/DATA0020.DAT matched pre-v4 UI25b31e62..., while disc UI is
9f979073.... docs/INSTALL.md documents this exact stale-cache failure.
The v4 manual installer omitted the required cache refresh; do not repeat.
User approved close+backup. Gracefully closed RPCS3 PID47960 and moved ONLY
E:/RPCS3/dev_hdd0/game/BLJS10256_DATA to
E:/RPCS3/install-cache-backups/BLJS10256_DATA-before-v4.
Verified192files/4,035,384,618bytes and cached UI checksum at the destination;
old active cache path absent. No deletion and no savedata modification.
RPCS3 left closed. Next boot must accept the native game-data installation
prompt to rebuild cache. Success still needs user runtime confirmation.
Future archive-changing installers/guides MUST include recoverable cache
backup while RPCS3 is closed; EBOOT-only changes do not refresh this archive.

**2026-09-17 RPCS3 v4 INSTALLED at user's explicit request:**
User asked to close RPCS3 and install. Elevated process check confirmed RPCS3
already closed; games.yml still maps BLJS10256 to workspace game/.
Verified ZIP/source/payload hashes, dry-ran Install-V4.ps1, then backed up and
replaced ONLY EBOOT.BIN and DATA/AIDDATA/AIDDATAPACK.CPK under game/PS3_GAME/USRDIR.
Installed hashes verified: EBOOT4d30f693ec685e06ff975be9f5d5ed42e0f8fde13674292b11ac26f3ce222621;
UI9f979073c15756d5adfdcd9343ecf215cc36a87f759cb539c643cadb794d5349.
Backups plus staged v4 files are in work/ps3_date_center_v4_20260917/installed-backup-01/.
Before-v4 backups are the prior v2 EBOOTa414df32... and UI25b31e62....
No saves/fonts/other game files touched. RPCS3 left closed; no runtime claim.
Build-time audits below correctly say installed=false at build time; this
installation note supersedes those state statements. Tests that pin the older
UI archive must now use the before-v4 backup, not the live installed UI file.

**2026-09-17 PS3 v4 full-screen date centering BUILT, not installed:**
User requests April10 card and same category centered. Native caller14c588
already passes center640/y340 and sets font40 at14c560, but centered drawer
14954 measures Japanese before the draw-time English substitution. Reuse
existing President/reward VWF measurement: optional date caller LR14c58c
gate goes to exact whole-string NAME_TBL lookup; unknown/malformed/non-CP932
text and other callers keep native fallback. No date string/value/font/position
changes. Tools/date_card_layout.py guards caller and all77 canonical translations,
updates only existing center helper78f000 (924->944bytes, under DATA78f800).
president_report_layout.check accepts the original and extended variants;
eboot.py integrates date upgrade after original President hook installation.
test_ps3_date_cards executes all77 lines across3 actual font-state modes,
preserves registers/CR/other FP values, tests fallback/caller isolation,
old wrapper negative control, reward parity and v2/v3 cumulative equivalence.
All33 focused/date/link/menu/loader/Mech/Weapon/President tests PASS.
Package work/ps3_date_center_v4_20260917/
SRW-Z3-PS3-RPCS3-v4-date-center-update.zip (12,634,318bytes).
SHA2564132a8ff82efec605479cf64d7d001df7f121365e7f74cdbe25b85c6ab7f167f.
EBOOT4d30f693ec685e06ff975be9f5d5ed42e0f8fde13674292b11ac26f3ce222621;
UI archive identical to v3 (9f979073...). Includes previous v3 name/term/menu
fixes; source hashes pinned, dry-run inspected, all ZIP CRC/read-backs verified.
Live game remains v2a414df32.../originalUI25b31e62..., confirmed unchanged.
No automatic install, commit/push or save edits. RPCS3 only, not physical PS3.
In-game centering confirmation still required; guide/audit included in ZIP.

**2026-09-17 PS3 v3 name/term + startup-menu update BUILT, not installed:**
User reports the same remaining faults as Vita and asks for Scenario Select
and DOB parity. Actual PS3 name widget256208 uses strlen/2*pitch at2562d4;
new tools/link_identity_geometry.py measures the displayed encoded name with
the existing width bank and widget quad width, preserving fractional pixels
and native unknown/Japanese fallback. Shared name widget covers dialogue/log.
Scoped strcmp wrapper at1ce224 maps the Japanese second operand through exact
NAME_TBL entries; native registration then retains the correct term index.
CPU tests execute actual name arithmetic and registration loop, then feed its
ID into primary geometry (old second term invisible, new rectangle present).
Code uses previously unreachable primary arithmetic1c6968..1c6a60 and184-byte
name helper78ef00; source hashes and all byte ranges guarded. Existing v2
primary/secondary term geometry kept. DOB callsf7924/f797c draw slash/omit day
suffix only; numeric values/editing unchanged. Full build integrates the hooks.
tools/startup_menu_layout.py patches four texture2 word cells in AID member1:
Scenario Select, Main, Tutorial, Scenario from the same canonical Vita IDs.
Only the separate square prefix changes to equal-width space in member0.
Native UVs, other39members, CPK headers/length, fonts and saves are unchanged.
Integrated in build_ui.py. 28 focused/loader/Mech/Weapon/President tests PASS;
source/changed atlas visually inspected, game runtime still needs user retest.
Package: work/ps3_link_background_v3_20260917/
SRW-Z3-PS3-RPCS3-link-background-v3-menu-update.zip (12,634,194bytes).
ZIP SHA256 bcf18dae33e543cf702a91e2d86f378162ec141abcf5b0a97ac77dbed141584d.
EBOOT SHA256 fe55a5e284096a1ba7a18684e634d490adc97c274283379fbd11860991f3fa97.
AIDDATAPACK SHA256 9f979073c15756d5adfdcd9343ecf215cc36a87f759cb539c643cadb794d5349.
Dry-run inspected then written; ZIP CRC and all payload read-backs pass.
Builder accepts baseline/v1/v2 EBOOT and pins installed older UI archive
25b31e62c3a7f84852ac371e07a34628f34a43df117ef5add18fbb77acf37d8b.
Baseline/v1/v2 converge identically; baseline fixture uses original backup,
not live game. RPCS3 ONLY, not physical-console SELF/ISO. Guide backs up and
replaces TWO files, not EBOOT alone. Live game remains v2; no install, commit,
push, or save modification. Vita v3 from prior turn remains unchanged.

**2026-09-17 Vita v3: actual name widget + translated term registration:**
User disproved v2: backlog terms good, names too wide, main dialogue terms
missing. Verified installed Vita3K EBOOT87b84eed... is v2. Two different causes:
names do NOT use the keyword render record path (earlier tests mislabeled Kei
keyword fixtures); actual name widget8110b37c uses strlen/2*pitch at8110b3fa.
New link_identity_geometry.py calls existing translated Latin measurement
helper with name widget quad width from record+c, retains native unknown/
Japanese fallback and fractional pixel width. Name ID/record fields unchanged.
Second cause: native registration0x810d8cd8 compares English drawn term against
Japanese glossary label, leaving default ID0 for unmatched second term.
Wrapper at0x810d8dc6 translates comparison operand via existing exact UI hook;
native registration then assigns correct index. Actual registration CPU test
uses Destruction Incident/Regeneration War from shipped table, reproduces old
second-term ID0 and corrected ID1. Names test executes actual widget rectangle,
reproduces Kei93 vs38.25, multiple names, fonts and Japanese fallback.
Primary retains rendered X/Y, cache width; now also captures actual style
height, cache1280bytes. Reuses obsolete primary/secondary arithmetic for tiny
name58byte and compare24byte helpers; no new code segments/relocations.
Every edited instruction range checked against native relocations. Code/data
independent relocation tested for the name helper as well as term cache.
52 regression tests passed, plus new relocation test and modified slot/height
test passed separately (53 unique tests). No in-game claim yet.
Manual v3 built work/vita/link_background_test16_03, eboot SHA256
8289b78ba77656bab191e7cf08971c26b561c01850c3b7733d51e9cbfbb4149d.
Manual ZIP2,091,893bytes SHA256aab2f4336020a2fb578f9e25112df3855b3fec5e9a211b26b8f0f14fa8259706.
Full installer BUILT: work/vita/vita3k_linkfix_install_03/
SRW-Z3-Vita3K-test16-linkfix-v3-install.zip,1,872,598,786bytes.
SHA256451045461dbcde4808ba5801a86f78b8d0c48d4d0478dda3c5bb327c81e61326.
All589members verified size/hash/CRC, only executable differs from test16.
Extended native registration test feeds its actual record into primary geometry:
legacy ID0 produces no rectangle, corrected ID1 produces182,121,173.25,29.
That combined regression was rerun and passes. Build guides/checksums alongside.
No installed Vita/PS3 files or saves modified in this turn; old builds preserved.
PS3 may have analogous separate-name/registration gaps: investigate only on
follow-up, do not assume the prior PS3 v2 source covers them.

**2026-09-17 PS3 RPCS3 v2 INSTALLED at user's explicit request:**
Confirmed RPCS3 closed and games.yml points to workspace game/. Verified
source/package hashes, backed up original, then replaced ONLY
game/PS3_GAME/USRDIR/EBOOT.BIN. Installed SHA256:
a414df32b5bffc8ac86877a5b01cb3d2ae4123f3dbab51d5088d3506c5544c3e.
Verified original backup: work/ps3_link_background_v2_20260917/
installed-backup-01/EBOOT-original.BIN (635cf35d... baseline).
Saves/fonts/assets untouched. No runtime launch/visual check yet.
The packager's baseline/v1 equivalence test previously read live game EBOOT;
that location is now v2, so use the verified baseline backup for future tests.

**2026-09-17 PS3 primary highlight v2 update BUILT:**
User reports PS3 still shifted/overwide in dialogue and backlog (Kei/Kira and
Destruction Incident/Regeneration War). Confirmed primary function0x1c680c
still used row/column/length Japanese spacing; previous secondary hooks alone
were insufficient, including release0.6.13 and console test06.
New tools/main_link_background_layout.py hooks0x1c6964 to252-byte helper at
0x78ee00, matches BOTH scene-zero pointer and glossary index in active render
records, uses actual signed X/Y (+1 native Y), cached VWF width, original
style getter/height and draw/color tail. Reuses dead stack temporaries; no
headers/segments/metadata/fonts/text edits. Integrated into link_background_layout.
Seven focused tests: actual emitted instructions, all256slots, stale scene,
wrong glossary, inactive record, volatile-clobber/register/write isolation,
original bad fixed-cell arithmetic, actual glyph advances (Kei/Kira/terms),
and baseline/v1 identical packaging. Still needs visual user confirmation.
Configured RPCS3 game EBOOT still baseline635cf35d... (read-only check).
Builder accepts exact baseline or prior v1 hash95f4a800..., rejects other builds.
Asked asynchronously whether screenshots are RPCS3 or physical PS3; no reply
at this note. Do not give the RPCS3 ELF to a physical console.
All21 focused + loader/Mech Info/Weapon Info/President regression tests pass.
Dry-run reviewed, archive CRC/member read-back and disk/source isolation pass.
Output work/ps3_link_background_v2_20260917/
SRW-Z3-PS3-RPCS3-link-background-v2-update.zip,3,512,406bytes.
ZIP SHA2561ff237b4185f4aa0881fbc06b58133a983a3dd059ecdc23322d047cc9887ddce.
EBOOT SHA256a414df32b5bffc8ac86877a5b01cb3d2ae4123f3dbab51d5088d3506c5544c3e.
Only299 actual EBOOT bytes change from baseline; no headers or other files.
Not installed, not visually tested, old packages preserved. No commit/push.

**2026-09-17 Vita link fix V2: user disproved V1; revised installer BUILT:**
User screenshots show main dialogue background starting mid-Destruction Incident
and overwide backlog Kei. Read-only hash of the configured Vita3K app EBOOT
is42aefa8576c9e32e60a2c6f68e9317c53c77852cf16c6ebd8729cae9de0b9d87,
confirming V1 was installed (not a missed copy). Asked asynchronously whether
Vita3K was fully restarted; no answer received during work. Do NOT claim v1 fixed it.
Cause: v1 patched secondary geometry0x810D6974 but primary0x810D646A still
uses parsed byte columns/lengths. New main_link_background.py replaces ONLY
0x810D64EE..0x810D65C0 with188bytes+NOP padding, within original RX block.
Matches native render records by scene pointer AND glossary index, NOT flat
render slot. Uses actual record X/Y (+1 native primary Y inset), existing
cached VWF width, and unchanged native style selection/height/colors/navigation.
No registered match leaves a zero rectangle; does not fabricate geometry.
Existing secondary hook retained. No new segments or relocations. Guard verifies
original block hash and no relocation overlaps (all native records format0).
Vita3K official relocation source was checked; no native branch relocations
overwrite the hooks. Actual styled drawer0x810D9F92 produces Kei width38.25;
negative-control test runs old primary path and reproduces width93 (69.75 screen
pixels at0.75 scale), matching screenshot. Expanded tests cover Kei, Destruction
Incident, Regeneration War, allslots/banks, scene mismatch, glossary-vs-slot
identity, styles, registers, unchanged records, and retained date centering.
42 prior date/UI/screenshot regressions pass; 7 focused link tests pass.
New EBOOT SHA256 87b84eed60ecc7a4b0f532b61fd1e13860d762eb9495b711e058bf8d6c909d45.
Installer work/vita/vita3k_linkfix_install_02/SRW-Z3-Vita3K-test16-linkfix-v2-install.zip
1,872,598,787 bytes SHA256 56074a2244f6fafab1c9cd9d3f901ea2dbee25162cf3f4e08165b1636e24bc8c.
All589files size/hash/CRC verified; other588files identical to pinnedtest16.
Manual overlay also built under work/vita/link_background_test16_02, but user
needs INSTALLABLE ZIP, not that overlay. Old artifacts preserved. Not installed,
no saves/auth changes, no commit/push. Runtime visual confirmation still needed.
PS3 earlier source check only proved its known hook was included; do not assume
all PS3 geometry paths are fixed if user reports same failure there.

**2026-09-17 Vita3K INSTALLABLE link/date package BUILT (V1, superseded above):**
User could not install the prior rePatch-layout update ZIP, clarified Vita3K,
and explicitly requested an installable package. New dry-run-first builder
platforms/vita/build_link_background_install.py reuses the pinned full test16
ZIP/audit, verifies all589 members, then replaces ONLY eboot.bin with the
verified link/date candidate (42aefa85...); remaining588 files are identical.
Includes PCSG00264/sce_sys/param.sfo and all game assets/converted modules,
not rePatch layout. Local Vita3K interface.cpp confirms metadata detection and
reinstall callback. No auth/license/firmware/saves included or read.
Output work/vita/vita3k_linkfix_install_01/SRW-Z3-Vita3K-test16-linkfix-install.zip
1,872,598,785 bytes SHA256 2bb14bb63cb7bc034460fdd31e811d19f7669d26c80d73db4c9416edce9e62b0.
All589 packaged members passed size/SHA256/CRC read-back against expected
inventory. Four link/date-retention CPU tests rerun and passed; executable
unchanged from prior46-test candidate. BUILD_AUDIT.json, checksum and guide
alongsideZIP. Guide: back up installation/saves, File > Install .zip, .vpk,
select ZIP without extracting, confirm reinstall only after backups, never
delete savedata. No automatic install or in-game test performed. Earlier
packages preserved; not for physical Vita. Other reported issues still pending.

**2026-09-17 PS3 link-background follow-up: older RPCS3 update BUILT:**
User requests PS3 too. Existing tools/link_background_layout.py only fixes
the secondary path in releases/0.6.13/EBOOT.BIN and physical test06; both
pass exact hook verification. However E:/RPCS3/config/games.yml points to
this workspace's game/, whose EBOOT is the older 635cf35d... executable,
matching work/build_0.6.10_record_categories,0.6.11_stage_transition and
0.6.12_approved_subtitle. Its native highlight sites were unpatched.
New platforms/ps3/build_link_background_update.py pins that exact source hash
and applies ONLY the existing three hooks/helpers (96 actual changed bytes).
No headers, fonts, translations, assets or saves changed. Extended existing
glyph tests with Alto/ZEXIS; all3 focused tests pass, including256slots,
reuse/metadata preservation and real VWF glyph advances. Dry-run reviewed.
Output work/ps3_link_background_20260917/SRW-Z3-PS3-RPCS3-link-background-update.zip
3,512,112 bytes SHA256 851f61bc538124d93a42bef4f04235b3847b7c33034ba265049a258847e06202.
EBOOT SHA256 95f4a80073cbc404e3ae4c2796c26e0648da3d3b765774074b8a93265ad10a1a.
ZIP/disk read-back and unchanged source checks pass. NOT installed or visually
tested. Guide says exact older RPCS3 build only, backup/replace EBOOT, rollback.
NOT a physical-console SELF/ISO or Vita update. If user sees issue on0.6.13
or console test06, request exact loaded build and investigate further rather
than applying this older executable. No commit/push or emulator changes.

**2026-09-17 Vita backlog link backgrounds: combined update BUILT:**
User reports ZEXIS highlight covering the following word and Alto highlight
extending into blank space. Native width used byte-length/2 times fixed pitch,
not the rendered VWF width. New platforms/vita/link_background.py captures the
VWF pen at registration (0x810D8D6C) into an appended 256-float RW cache keyed
by native bank/slot; selection (0x810D6A08) restores that width and the old
fixed-width store (0x810D6A6E) is suppressed. Native 20-byte records, lengths,
identity, navigation, x/y/height and colors remain unchanged. Cache uses the
existing relocated names pointer; existing relocation segments stay identical.
76-byte RX hooks at0x812B5FA0/5FCC end before the pointer words at5FF4.
Date stub reservation moved from5F80 to5F68 to fit, with behavior unchanged.
Future ui_text.prepare builds with names include the link fix. Combined builder
build_link_background_patch.py starts from pinned original working test16,
applies date centering then link widths; no new translation/assets/auth/saves.
Output work/vita/link_background_test16_01/SRW-Z3-Vita-test16-link-background-update.zip
2,091,698 bytes SHA256 486df0051e70a0031cadb0897c8344190553fd5955e9a01dcd49e0b7fec4d4d1.
EBOOT 8,129,236 bytes SHA256 42aefa8576c9e32e60a2c6f68e9317c53c77852cf16c6ebd8729cae9de0b9d87.
Four new CPU tests pass: actual native glyph advances for names/terms/Japanese,
all256 slots, reuse, null selection, separate code/data relocation, unchanged
records and retained date centering. All42 existing date/UI/screenshot tests
also pass (46 total). Dry-run and ZIP/disk read-back passed.
NOT installed or visually verified in-game. Guide includes test16-only scope,
physical rePatch and Vita3K EBOOT replacement, backup/rollback and test cases.
Prior date-only artifact is preserved; combined update works over either
original test16 or that date update. Earlier defeat-condition/Z Chips/menu
alignment reports remain pending. No commit/push.

**2026-09-17 Vita date-card centering: date-only update BUILT:**
User requested horizontal centering of April27 and all texts in that category.
Native date call 0x8109E384 already supplies x640/y340/font40, but font state
+0x6c nonzero routes native centering around our VWF width hook (0x81007974).
New date_card_centering.py uses a guarded 56-byte stub at0x812B5F80 and changes
ONLY that date call. Known translations enter the existing measured-width
branch with an identical native frame; unknown text falls back. Drawing font
state, vertical position, alpha/depth and all strings remain unchanged.
ui_text.prepare integrates it for future builds after verifying every date key
and single-line measured Latin. No generic menu alignment changes.
Build_date_center_patch.py (dry-run-first) makes a minimal EBOOT update against
the pinned working test16 rePatch ZIP, with unchanged other segments/relocations.
Output work/vita/date_centering_test16_01/SRW-Z3-Vita-test16-date-centering-update.zip
2,091,486 bytes SHA256 7bdc37acc3bce0cc82cf0d693672077b8464cf4f944a5bad099272a7b1ea112f.
EBOOT SHA256 730575c90504592205697025447c4784b302c81db005a2765f1edf5de10a5bf9.
5 new tests execute all77dates in both font modes, reproduce old April27 offset,
check unchanged unknown-text behavior, registers/SP, code scope/relative branches.
17 UI-hook tests and20 screenshot regression tests also pass (42 total).
ZIP/disk read-back passed. NOT installed or visually retested in-game.
README-INSTALL.md covers physical rePatch and Vita3K, backup/rollback, keeping
existing self_auth and fonts. This update is for test16 ONLY, not a newer build.
Earlier reported issues remain unfixed: Hibiki defeat-condition displayed-name
variant, Z Chips footer, intermission label alignment. No commit/push.

**2026-09-17 AI-only MQM pipeline built; linguistic review NOT started:**
User requested a proofreading pipeline using the new tools and BASE_RULES.md.
`tools/mqm.py` provides dry-run-first prepare/challenge/report commands. It
freezes canonical sources/English/glossary/rules by stable ID, builds up-to-80-row
batches with full scenes and concordance, expands glossary tokens for review,
and validates evidence, coverage, stale hashes, reviewer session separation,
duplicates and severity before scoring accepted findings. Missing source and
design/markup findings are separate; no universal pass threshold or whole-game
claim. Pending findings/uncertainties remain visible. No automatic model calls,
translation edits, status promotion, game builds, installs or external writes.
`docs/AI_PROOFREADING.md` contains reviewer/challenger prompts, JSON examples,
commands and correction order: meaning first, corpus-wide glossary-name script
after, then checks and re-review. BASE_RULES and localization/README link it.
Profile: localization/qa/mqm_profile.json (0/1/5/25; per1,000 source characters).
`proofread_stage.py` gains optional --root for scratch canonical exports and
--dry-run; stage-1 a/b suffixes are now included. Existing hints/term extraction
are reused by MQM; near/voice comparison remains supplemental, not truth.
Ready packet: work/mqm/stage1-pilot-20260917/START-HERE.md, 244 canonical rows,
3 groups, 5 batches, 5,403 source characters, 69 files. No reviews submitted,
no linguistic score assigned. A report dry-run correctly gives zero coverage
and null rate, not a perfect score. NOT an audit of either shipped platform build.
18 new MQM tests + 18 existing localization tests passed; full catalog check
reports 0 structural issues. No translation content, live saves or builds changed.
Next: run fresh AI reviewer sessions on packet batches following the frozen
guide, challenge their findings, then report; do not imply this was already done.

**2026-09-17 bidirectional RPCS3/Vita3K save conversion BUILT:**
User reports Vita patch working and requested both save-conversion directions.
Source RPCS3 root E:/RPCS3/dev_hdd0/home/00000001/savedata has NPJB00520
manual STG-000 (chapter2 cleared, funds110336/chips138), STG-003 (chapter4
route choice, funds27098/chips546), and SYS (metadata references chapter10).
Vita3K config points outside its installation to
C:/Users/Binh/AppData/Roaming/Vita3K/Vita3K/ux0/user/00/savedata/PCSG00264:
STG-001 (chapter1 cleared, funds44632/chips60), SYS and SlotParam0/1.
tools/convert_z3_saves.py validates both checksums/section layout/version101;
only native size header bytes4:8 reverse. All other BIN bytes stay identical.
Stage size0x48000, used0x40610; system size0xE0000, used0xD7A70. Main checksum
LE-word sums exclude final word: stage0x440:0x47FFE, system0xD8F8:0xDFFFE;
summary at0x40 covers0x44:0x43E. PS3 VA0x176824 and Vita0x810B47BC match.
Slot mapping PS3 STG index+1 = Vita STG index; system=VitaSlot0. Transfers
UTF8 display strings SFO<->SlotParam, keeps destination SFO account metadata
and icons from its own templates. No manual chapter10 save manufactured.
Output work/save_conversion_20260917 with originals in original-backups,
CONVERSION_AUDIT.json, NATIVE_VALIDATION.json and README-FIRST.md:
rpcs3-to-vita3k.zip 42183 bytes SHA256
7fae909b6c16f1b62c5a6e349e16263e65a45cc769c7e25dcb8a8376914fab14;
vita3k-to-rpcs3.zip 1650921 bytes SHA256
cafa964d3849d36e80ffc7bc8b5dda5d25f1ace420836707fbcf5e28963b9606.
9 synthetic regression tests pass, all five converted BINs round-trip exactly,
all archive members read back, live sources rehashed unchanged. Native ARM
Vita checksum/version functions accept all five shared payloads and reject
corruption (tools/check_save_conversion_native.py). NOT a full game-load test.
Local PPC harness hit CPU exceptions; no native PS3 execution claim. PS3
algorithm was statically compared and matches. No live emulator launch/save
installation occurred. These are emulator imports, NOT direct physical-console
restores; do not copy Vita3K SlotParam files into an encrypted physical save.
Next user tests: load/manual slots, battle, spare save/reload, Continue separately.
Docs: docs/SAVE_CONVERSION.md. No commit, push, game build or live-save changes.

**2026-09-17 Physical Vita: auth supplied, completed test16 package:**
User supplied root self_auth.bin and authorized Vita work. Local inspection
confirms 144 bytes, authority matching base/test16 EBOOT and nonempty caps.
No raw bytes or raw auth hash logged. Root file is Git-ignored and unchanged.
IMPORTANT correction to earlier staging builder/docs: SceSelfAuthInfo includes
shared secrets at0x50:0x90 (klicensee0x60:0x70). Upstream rePatch3.0 only uses
authority0:8 and capabilities/attributes0x10:0x50. build_repatch.sanitize_auth
now keeps ONLY those fields and zeroes everything else. Archive verification
rejects unsanitized auth even with a matching ZIP checksum. Raw dump is NEVER
included; guide says not to upload it or replace sanitized output with raw.
Source references: dots-tb/rePatch-reDux0/repatch.c auth hook, VitaSDK
vita-headers/include/psp2kern/types.h SceSelfAuthInfo/SceSharedSecret.
BUILT: work/vita/english_repatch_test16_02/
SRW-Z3-Vita-rePatch-test16-hardware-test.zip, 94,279,737 bytes;
SHA256 8dd8d49e9de652edfb6601959965f5e54b5b0cf92457dd34606d832ce0c4f486.
121 payloads, 213,968,068 expanded bytes; 123 ZIP entries including two docs,
all size/SHA256/CRC checked. Test16's120 game files byte-identical; no PS3
layout fix ported, no new translations, no original modules/licenses included.
11 focused rePatch tests pass; full Vita suite: 131 tests pass (289.529s).
Hardware boot/save/suspend remain UNTESTED; asked user for firmware/rePatch
versions asynchronously. Target PCSG00264 v01.00, existing working Japanese
game, compatible active rePatch. Copy folder to ux0:rePatch/PCSG00264; do not
install ZIP as VPK or copy to app/patch. Guide/BUILD_AUDIT.json accompany ZIP.
No device, firmware, plugin config, saves, original game or PS3 build modified.
No commit/push/public release. Older incomplete ZIP preserved, do not deliver.

**2026-09-17 PS3 executable isolation / test 06 candidate:**
User reports 04 fails with 80010001 and 05 loads. With 01/02 loading and
03 failing, this isolates the immediate failure to the English EBOOT under
the tested settings, not the English non-executable files. Exact underlying
defect is NOT proven. User approved a loader-layout candidate.
platforms/ps3/cfw_loader_layout.py folds the pinned 03 English ELF's EXT
VA0xC00000 (0x90000 bytes) into native RW LOAD VA0x790000. That LOAD's
filesz/memsz become0x500000; translation addresses and bytes stay unchanged;
old BSS/scratch/gap are file-initialized zeros. Only two nonempty LOADs remain.
Native code/data/TLS/process headers are preserved except intended ELF/PH
metadata; translation tables become writable/non-executable. Nonloaded tail
relocates to0xC80004 with an aligned section table; original BSS section is
not relocated. Same pinned fself tool and 03 application metadata retained.
28 synthetic packaging/layout tests pass, including corruption and alignment.
Output: work/ps3_loader_fix_20260917_aligned; DIAGNOSTIC_AUDIT.json is the
completion marker, written only after full two-tree ISO member verification.
BUILT AND VERIFIED: 06-SRW-Z3-English-Two-LOAD-CFW.iso, 4,745,068,544 bytes,
SHA256 b8527d620e9ccb64f8a62e7ca98d7b52f9a1b25e5addf0c49d05b97246228b3a.
All 554 members pass SHA256/size checks in both ISO filesystem trees; only
EBOOT differs from 03. README-TEST.md and SHA256SUMS.txt accompany the ISO.
Earlier work/ps3_loader_fix_20260917 was interrupted during extraction to
correct tail alignment: INCOMPLETE, no usable ISO, never deliver that folder.
Guide: platforms/ps3/TWO_LOAD_TEST.md. Candidate is NOT hardware-tested.
No translation catalog changes, emulator installation, save/firmware changes,
public release, commit or push. Other dirty files belong to concurrent work.

**2026-09-16 PS3 hardware report / crossover tests:**
User reports original diagnostics 01 and 02 load, 03 still returns 80010001.
Exact first successful screen and CFW/Cobra versions not supplied; same test
settings assumed. This supports basic wrapper/layout compatibility, but does
not prove the English EBOOT rather than data or transfer is the culprit.
User explicitly approved next diagnostic ISOs. Added
platforms/ps3/cfw_cross_diagnostics.py and CROSS_BOOT_TEST.md plus six tests.
23 CFW packaging/isolation tests pass. Builder pins previous diagnostic audit
e6715d550601c7ca9f6cc3c5f88b0d309d23b8deb0e3e124ab8df652722b9069,
hashes exact source 02/03, and swaps their EBOOTs WITHOUT rebuilding/wrapping:
04 = working02 + only English EBOOT from03; 05 = failing03 + only JP EBOOT02.
These deliberately mismatch code/data: BOOT ONLY, no loading/saving/gameplay.
Different text or later crashes do not equal the immediate 80010001 failure.
Output work/ps3_boot_cross_20260916; see DIAGNOSTIC_AUDIT.json for completion
and hashes. BOTH BUILT AND VERIFIED: 554 files from both trees of each ISO.
04 bytes4,435,476,480 SHA256
b5da7d77d1877777f8d061e20dc4e50b3d203c5ab1c04c25e318e0483adad58a.
05 bytes4,740,677,632 SHA256
a2ef5c72712c4e99a2ace6277a08128275e7a8ae3e272e9519d0d200404132f5.
README-TEST.md and SHA256SUMS.txt are beside the two full unsplit images.
No completion marker means incomplete build. Earlier images,
Vita work, saves, firmware and installed game remain untouched. No push.

**2026-09-15 Physical-Vita rePatch test16 STAGING build:**
User requested a Vita patch and installation guide, assuming VitaShell and
Japanese game installed. Added platforms/vita/build_repatch.py and
REPATCH_INSTALL.md. Output work/vita/english_repatch_test16_01/
SRW-Z3-Vita-rePatch-test16-NEEDS-SELF-AUTH.zip is INCOMPLETE, NOT INSTALL-READY:
rePatch 3.0 release notes explicitly require self_auth.bin for EBOOT mods.
That file is not available locally; must be dumped from user's PCSG00264 v01.00
using FAGDec. Do not invent capabilities, use a license as auth, or call it
console-verified. Builder --self-auth checks 144 bytes, matching authority ID
and nonempty capabilities (not provenance); --allow-incomplete is explicit.
120 payloads, 213,967,924 expanded bytes; ZIP 94,278,878 bytes; SHA256
aac41fd1404f2d210bfae4b500957277ecc068b8d07e024a131c1e43e152c9bd.
All 122 entries (payload + guide + manifest) read back with size/SHA256/CRC.
EBOOT and all changed data byte-identical to test16. No wrapper rewrite,
modules, sce_sys, license, saves, firmware or plugin binaries included.
All 128 Vita tests passed (214.825s), including 8 new synthetic packaging tests.
Physical boot/save/load still pending.
Guide includes auth-dump workflow, conditional plugin setup, folder layout,
backup and rename-to-disable rollback. Nothing installed or pushed this turn.

**2026-09-15 Intermission / Store / Scenario Select, test16 BUILT:**
Text hooks do not cover the native word sprites. menu_followup_art.py patches
four P8 cells: Intermission on page0 (0,192,296,40); Main on page2
(136,472,72,40); Tutorial (208,472,168,40); Scenario (376,472,136,40).
IMPORTANT: the prefix boundary is 208, not216. Four five-vertex native quads
at534C8/53518/53568/535B8 validate these UVs. Pixel changes stay in those cells;
all palettes, UVs, geometry and prior startup headings are preserved. Native
quad comparison preview: work/vita/test16_preview/native_words_comparison.png.
menu_followup_text.py adds exact direct Clear keys, source-pinned to81271B6C.
Scenario Select recordA1454 has only its leading square changed to a fullwidth
space, preserving its advance and all record fields; live check still needed.
parts_network_fixes.STORE_X adds88 native pixels to the existing centered
PS Store widget. Vita crop has ink center54.5 versus button120.5 at960/1280
scale. This is screenshot calibration, NOT proof of native caller behavior or
a PS3-derived correction; live retest is required. Other network rows unchanged.
Three new shared messages in ui.vita_menu_art supply Main/Tutorial/Scenario.
build_test16_ui.py reconstructs test15's catalog fingerprint in memory excluding
only those two new files and one manifest line. Every old catalog byte must
match. Full builder now uses cumulative menu_followup_art instead of emitting
startup_art separately (duplicate member writes are rejected). Incremental
builder regenerates member1 from pristine plus prior startup plus new cells.
All120 Vita tests pass (211.180s); zero catalog issues / zero sync changes.
Actual ZIP QA:161 bindings,328 prior UI draws,23 library/chart draws, both
name orders/relocations, Clear drawing/centering in both modes. All589 files
verified. Only EBOOT and AIDDataPack differ from test15;587 others identical.
verify_test16_scope.py proves only5 UI bytes differ (bullet and Store X), four
art cells change, every old key/value survives, and two Clear keys are added
(3696 total). No installation or live-game visual verification performed.
ZIP: work/vita/english_vwf_test_16/SRW-Z3-Vita-English-VWF-test-16.zip
1,872,598,616 bytes; SHA256
3a44d8f901af3f9aceab19d9ef44612568e00b59686985cd76ef21aa6b2b6ce8.
EBOOT SHA256 ce424db2ce2417b23df01d8cb580c409928a1b3f0ad45ba4f983d7a16b871c2b.

**2026-09-15 End Phase remaining-team warning, test15 BUILT:**
New phase_warning.py inventories completed native count lines. The original
constructor at 8100A094 combines CP932 prefix 812578BC, full-width digits at
812578A4 and suffix 812578D8. Positive counts display modulo 100; zero/negative
counts use the separate plain confirmation. Source routine and literals are
hash/identity checked and left unchanged. All 100 displayed values map to the
existing shared issue_hook:r_065443f6ddfcf0d7: Teams still able to act: {count}.
Adds 200 exact CP932/UTF-8 keys (native converted keys equal CP932 here),
including original UTF-8 centering inputs; no global fragments or format hook.
Shared catalog, font, scripts, counts, buttons and UI positions do not change.
test_vita_phase_warning executes the original constructor for 105 input cases.
Screenshot regression checks all displayed values, untranslated fragment
misses, native drawing and centering for 1,6,9,10,99 in both encoding paths.
All 117 Vita tests pass (208.405s), catalog check has zero issues, and sync
dry-run changes zero compatibility views. No installation or live visual QA.
build_test15_ui.py preserves hash-verified test14/test09 cached files and
earlier artwork; verify_test15_scope.py checks the actual ZIP against test14.
Actual ZIP: all 589 entries verified. Only EBOOT differs; 588 files including
all UI/art archives are identical. Every prior translation key/value remains;
exactly 200 warning keys added (3694 total). Packaged native QA passes 105 count
inputs, 10 warning draws/10 centered positions, all 161 prior widget bindings
and 328 prior UI draws, 23 library/chart draws and both name orders/relocations.
ZIP: work/vita/english_vwf_test_15/SRW-Z3-Vita-English-VWF-test-15.zip
1,872,599,730 bytes; SHA256
792252bdf7a0c232a69eb508d4df41a0e643542d3428812bfb12455e044a164e.
EBOOT SHA256 60f60bda3b1c1e3544eadbfdceff918aa5b03b311df2b3b9587cae32651a5a17.

**2026-09-15 preset squad name / split Team screenshots, test14 BUILT:**
Native Lua squad-name inventory was missing from draw-time translation sources.
ui_text now inventories 242 unique presets using the shared squad_names parser;
existing shared translations include Special Investigator for 特別捜査官.
No script or saved name is rewritten; nonmatching custom names pass through.
New team_labels.py binds AD914 and AEDF4 to whole Team captions and blanks
only their three redundant source fragments. Safe two-byte aliases continue
after the 57 intermission aliases; no global kana keys or widget fields change.
Only eight UI bytes differ from test13. All old UI keys and values remain,
with 84 new keys (3494 total). Catalog and font mapping remain unchanged.
build_test14_ui.py reuses hash-verified test13/test09 cached files and preserves
patched startup/chart artwork. Actual ZIP checks pass 161 bindings, 328 native
UI draws, 23 library/chart draws, name orders/relocations and chart art checks.
All 589 package files verified; only EBOOT and AIDDataPack differ from test13.
All 115 Vita tests pass (169.366s); catalog check has zero issues and sync
dry-run changes zero compatibility views.
Regression helper permits 100000 instructions for a full-table lookup miss;
the old 20000 limit was insufficient for the new custom-name passthrough test.
No installation or live-game visual verification performed.
ZIP: work/vita/english_vwf_test_14/SRW-Z3-Vita-English-VWF-test-14.zip
1,872,593,137 bytes; SHA256
b3ca400ccc978cdb1a6479f10b843fc67c5c46d3c7f8ee7e5cdbd2f3bfa75622.
EBOOT SHA256 9a015548ab6ac21369f266bf46f04e5a8e57aeacda5ae6b7df2cae4999d38d53.

**2026-09-15 Power Parts / Network screenshots, test13 BUILT:**
New parts_network_fixes.py binds19 unique ASSF text slots. Power Parts list
headings/footer, two Select Slot variants, narrower Rep/Resup parts columns,
split (Team), Upload/Download, PS Store and compact Bonus Maps. Three unique
redundant suffixes blanked. Only Store's centering flag/coordinate may change;
all other widget fields, category indices, numeric values, slots and bars stay.
IMPORTANT filter root cause: ui_text's unconditional split-line 消費 -> SP Cost
hook leaked into consumable types. Removed that global override; native noun
is now shared Use. Both Spirit-list 消費-newline headers keep SP Cost through
private aliases (newline preserved), including aliases for the split line.
Filter source record B5D14 also changes only 消費 -> ＵＣ: two CP932 cells,
same four bytes/category positions, private Use binding. Native direct EBOOT
Select Slot and whole (Team)/(Tag) labels have complete-string hooks too.
Adds three messages in shared ui.parts_network (Equipped Power Parts,
Select Slot, Bonus Maps). No existing locale messages change. build_test13_ui.py
reconstructs the test12 catalog fingerprint in memory, omitting only the two
new group files and its one manifest registration; mismatch forces full build.
It retains all hash-verified test12 files/test09 fallback and patched UI art.
Future successors can use test13's normal current catalog revision directly.
Installed executable and UI archive were read-only verified as test09;
no installation performed. Runtime screenshots still need retesting.
All113 Vita tests pass (188.980s). Catalog check has zero issues and sync
dry-run changes zero compatibility views. Actual ZIP QA passes159 bindings,
322 native UI draws,23 library/chart draws, both name orders/relocations and
regenerated chart artwork. All589 packaged files verified. Only EBOOT and
AIDDataPack differ from test12;587 other hashes and all nonzero UI members
are identical. verify_test13_scope.py proves only98 bounded UI bytes change,
all old translation keys remain, and the sole changed old value is 消費 from
SP Cost to Use. Adds46 keys;3410 total. No live verification or installation.
ZIP: work/vita/english_vwf_test_13/SRW-Z3-Vita-English-VWF-test-13.zip
1,872,590,700 bytes; SHA256
f388772d129405a89272c9985b3b02b6fc547209d1a9f10daeedf8d9743d6f7b.
EBOOT SHA256 01e7e375aafff31f7f13611cc8e199ad41c48ff978cbd487cf64db6634fc7009.

**2026-09-15 Pilot List / upgrades / Library popup, test12 BUILT:**
New platforms/vita/roster_library_fixes.py binds45 native ASSF records via
unique ^NNN aliases (98 raw/converted table keys including line aliases).
Two multiline footer aliases retain their newline before native splitting;
only the two unique redundant RANK overlay strings are blanked. Both list
variants receive Pilot List, Upgrades, DEF, Sight and Wpn Rank captions.
All six Intermission Library text records (including selected Robot) use
compact shared labels, separate from title-screen texture translations.
Original special mode0x01, font, coordinates and other widget fields remain
unchanged. Options Library is scoped too. Fixed-width :Confirm hint records
use : OK to leave space before Back; general Confirm and combat Defense
are untouched. Shared catalog revision is unchanged. Default builder now12;
work/vita/build_test12_ui.py reuses verified test11 + test09 fallback cache,
explicitly preserving UI member1. No installation or live visual test.
All111 Vita tests pass (162.582s); native drawer test helper now collects
unused Unicorn machines between cases to release native translation buffers
under 32-bit Python (first full run exhausted that test-harness buffer).
Actual ZIP QA passes140 bindings /274 native UI draws,23 library/chart draws,
both name orders/relocations, and regenerated chart artwork comparisons.
All589 ZIP entries verified; only EBOOT and AIDDataPack differ from test11.
Other587 hashes and nonzero UI members are unchanged. Exactly231 changed UI
bytes lie within the45 new caption slots and two redundant RANK slots;
every widget record field and all previous UI changes are preserved.
ZIP: work/vita/english_vwf_test_12/SRW-Z3-Vita-English-VWF-test-12.zip
1,872,589,938 bytes; SHA256
1b0f0afefc70bfb3ef78bc0041f145dbb5ae79eb909e284e91fd1ae3874dcb8a.
EBOOT SHA256 9e678763dfb2632a31e9abb60d4ff0061e47abc45cf93770367ce7a37933b358;
3364 UI keys. In-game visual verification is still required.

**2026-09-15 phase / SR reward / tiny badge / Intermission, test11 BUILT:**
platforms/vita/intermission_fixes.py adds57 source-pinned native bindings with
unused two-byte ASCII aliases (even the one-kanji 攻 slot fits). Both raw and
converted aliases are checked against original EBOOT and ASSF before use.
Captions cover AT badge, Intermission title, Pilot Swap, both split Team Setup
and D-Trader states, whole SR/bonus-funds messages, all9 footer families.
37 uniquely referenced redundant fragments/colored reward overlays are blanked.
Counters, reward logic, unlocks, input bindings, source section sizes and
pointers stay unchanged. Some complete captions normalize their local font
or centering; field masks are explicit. All wording reuses shared catalog.
The prior confirmation overlay used25px while the live base text used28px:
both layers now request28px and active coordinates use that same pitch.
Tests execute the native drawer at28px for combined and active Yes/No labels.
build_test11_ui.py reuses verified test10 files, falling back to its test09
archive cache only after exact expected hash verification; preserves UI
member1 startup art. Full builder also defaults to11. No installation yet.
All109 Vita tests passed (146.024s). Actual ZIP QA passed95 bindings,
180 native UI drawing cases,23 library/chart cases and both name orders /
independent relocations. Both chart art members match regenerated output.
All589 ZIP entries were read-back verified; only EBOOT and AIDDataPack differ
from test10. Other587 file hashes and all nonzero UI members are identical.
ZIP: work/vita/english_vwf_test_11/SRW-Z3-Vita-English-VWF-test-11.zip
1,872,588,849 bytes; SHA256
0da07bd181c047346e2f447fe757bbdda3eed78e083f31fefae90326a2adc1e5.
EBOOT SHA256 20f9783da1e58c0c22d1b2e745a4acb05baa99c8212773a68f29db358e13619c;
3266 UI keys. No live visual verification; screenshot rows remain retest-required.

**2026-09-15 battle Key Help / Get Result screenshots, test10 BUILT:**
Right Stick is native ASSF record0x99334, bound to the existing shared
ui.training_help_layout caption. Unit result headings are two independently
drawn pieces at0xAA694/0xAA6B4 and0xAB354/0xAB374. The first piece now aliases
the shared Unit label, and only its unique suffix pool slot is blanked.
Whole-word result variant0xAB154 also has an explicit alias. Total38 aliases.
Funds/Z Chips, reward statistics, buttons and unknown team name stay unchanged.
New regression test proves no global ユニ/ット hooks, unchanged unrelated
suffix and stats, and invokes both native encodings for all four new aliases.
work/vita/build_test10_ui.py reuses hash-verified test09 files with an identical
catalog/font guard. IMPORTANT: the standard writer rebuilds from Japanese
source CPKs, so this script explicitly carries forward old changed UI member1
(startup artwork), not just new member0. Do not copy the old test08 cache
script's member0-only pattern: that can revert previous member1 artwork.
The full builder default is also test10. All107 Vita tests pass (135.298s),
with zero catalog issues and all475 compatibility views checked. Built:
work/vita/english_vwf_test_10/SRW-Z3-Vita-English-VWF-test-10.zip
1,872,587,604 bytes; SHA256
ada583745df2b797de758880e66fa8a89274d9b2a1905e234b2473b2b0c0780a.
EBOOT SHA256 38d28607cb607721183306257a2ec89fe141749d760936149db9336c831cde22;
3152 UI keys. UI archive and all589 ZIP entries verified. Only AIDDataPack
and EBOOT differ from test09; other587 file hashes are identical. All nonzero
UI members, including startup artwork, are byte-identical to test09.
Actual packaged executable passes38 widget bindings /84 native drawing cases,
both name orders/relocations. No installation or live test; Vita3K63376 open.

**2026-09-15 library / Scenario Chart screenshots, test09 BUILT:**
The full builder default is now test09 (fresh directory, no cache reuse).
ui_text includes ui.library_list_labels and only keyword/series glossary
sources proven as whole native strings; no ambiguous pilot glossary names.
Two additional ASSF aliases use compact Character Library / Robot Library
(34 widget bindings total). Native chart Confirm at 8126DB68 is an in-place
~COK alias (two callers), leaving generic Confirm unchanged. Separate exact
formatted Episode N and bracketed-title outputs come from verified Vita
metadata. Number/title buffers and native formatter code remain unchanged.
platforms/vita/library_chart.py also changes only bounded letter rectangles
in effvita members297/298, preserving palettes, dimensions and animation.
New ui.library_chart shared catalog group has six messages; compatibility
views remain unchanged. Artwork previews inspected under
work/vita/library_chart_review. All 106 Vita tests pass (119.994s), and all
475 compatibility views pass with zero issues. Full rebuild verified all 118
CPKs and all 589 ZIP sizes/SHA256/CRC. Package:
work/vita/english_vwf_test_09/SRW-Z3-Vita-English-VWF-test-09.zip
1,872,587,498 bytes; SHA256
adbfa29fc203c5228d42fa89f135d6928dc0cb26cd8fa6b5fc73b3e4ebaed8bb.
EBOOT SHA256 e6fdd069c6fe181d57f0e31ba5afef54e2f35dd0488c07b962fe81531f79563f,
3,144 UI keys (160 glossary keys; 223 chart keys). Only AIDDataPack, effvita
and EBOOT differ from test08; the other 586 output hashes match exactly.
Actual-ZIP QA: 34 scoped widgets, 76 native draw cases, both default-name
orders/relocations, plus 23 library/chart draw cases and both exact art members.
Use work/vita/verify_test07_ui.py with the test09 directory and
work/vita/verify_test09_library_chart.py to repeat packaged checks.
No installation or live-game test performed; Vita3K PID63376 was still open.
Keep older packages for rollback.

**2026-09-15 narrow battle Attack screenshot, test08 BUILT:**
Use existing shared ui.battle_preview_layout Atk. captions for native ASSF
records 0x9AC94 and 0xB11F4 via scoped aliases. Global Attack, Ctr. labels,
hit values and all battle logic remain unchanged. Alias inventory now32;
tests enforce width+16 <=94 at full 32px live pitch, and exercise both native
encoding paths. All 102 Vita tests pass (99.1s).
work/vita/build_test08_ui.py is a guarded UI-only rebuild: requires identical
shared-content revision to test07, verifies previous ZIP hash and every
reused output hash, regenerates/compares the matched voice pair, rebuilds only
AIDDataPack and EBOOT, then uses the standard full ZIP read-back verification.
The full build_vwf_zip.py default is also test08. No artwork regeneration is
needed for these two existing ASCII captions. Built
work/vita/english_vwf_test_08/SRW-Z3-Vita-English-VWF-test-08.zip:
1,872,796,848 bytes; SHA256
59b49bd5bdb7b57f0c529041aa950f9df67b3abe43206cfb1a0f833bd295602b.
Rebuilt UI archive member bytes and all 589 ZIP sizes/SHA256/CRC verified.
Only EBOOT and AIDDataPack hashes differ from test07. Vita3K PID63376 remains
open with test04/test05 EBOOT, so no installation or live-game validation.

**2026-09-15 roster/settings/Pilot Info follow-up, test07 BUILT:**
User reports Settings tabs and roster headers still overlap; Move / Stats /
Ace Bonus and Pilot Info full name remain Japanese. Installed EBOOT still
matches test04/test05; installed AID member0 SHA ad27e427...1abf5e25d3 includes
the earlier font edits, proving smaller requested font alone was insufficient.
New ui_widget_bindings.py binds 30 pinned native widgets via four-byte ASCII
aliases in existing text slots. Both original SJIS and native UTF-8 conversion
keys resolve in the executable. No string-pool growth or pointer/coordinate/
state changes. Compact shared Settings 1/2 and S. Atk / S. Def are reused;
new shared Rep. / Resup captions added. Roster checks now use measured native
neighbor gaps at conservative 32px live pitch, independent of requested font.
Move is global default again (MV is scoped only to map popup); Stats conflict
resolved explicitly. Four Ace Bonus and five Pilot Stats widgets are bound
directly. Fully default full-name strings also enter the general display
lookup, not just the dialogue constructor. Native drawing tests pass for
aliases, Move, Stats and Hibiki Kamishiro in both encoding modes. All 102 Vita
tests pass (101.6s). Catalog: 475 compatibility views / zero issues. Built
work/vita/english_vwf_test_07/SRW-Z3-Vita-English-VWF-test-07.zip:
1,872,763,557 bytes; SHA256
a035f5ab2e4872fdf3468801071410ced257371db42db0b1c982a67d31e45785.
All 118 rebuilt archives and 589 ZIP sizes/SHA256/CRC verified; 2782 UI keys.
No installation or live testing; Vita3K PID63376 remains open. Preserve saves
and previous ZIPs; no PS3 build or release changes.

**2026-09-15 post-prologue/search/name screenshots, test06 BUILT:**
Installed EBOOT now matches test04/test05 (SHA256
6d8cae59f8cc7ced8f5c4b708c46e7cbe995c04ee00a82497a92e496673265ba).
New changes are genuine remaining gaps, not the earlier test02 baseline.
Post-prologue STG0001b member7 has 80 records at base20 / stride88, unlike
the opening's stride84. New pinned source adapter exposes all 18 exact
issue_hook narration keys for draw-time translation; no record edits.
Added shared search-list/deployment help groups, source-bound Back to Results
message, verified complete-line aliases for SP Cost and Rec:, scoped MV
preference, local sizes, and only two redundant SP suffix blanks.
Default-name constructor calls 810CBE50/78/9C and 810CBF46 now copy through
a dedicated exact-name table. Covers Hibiki, Kamishiro and both fully default
full-name orders; custom / partly customized full names pass through. Saved
name buffers and order flag stay unchanged. Native constructor CPU tests cover
both orders; wrapper tests cover custom UI-caption names and independent
RX/RW relocation. The 192-byte width table moved to new non-executable data
after BSS beside the pen scratch, freeing the proven RX segment-tail reserve
without W+X or segment overlap. All 100 Vita tests pass; 475 shared catalog
compatibility views / zero issues; focused 29 tests rerun after name-table
alignment pass. Built work/vita/english_vwf_test_06/
SRW-Z3-Vita-English-VWF-test-06.zip: 1,872,762,697 bytes, SHA256
a722c4a3ea584aee29c71270a9858128e900b79ff7fb15ebb6f9245788f195bd.
All 118 rebuilt CPKs and 589 ZIP entry sizes/SHA256/CRC verified. Contains
2718 UI keys plus the separate four-key default-name table. Vita3K PID63376
still open; not installed or live-tested. Do not modify saves. No PS3
build/release changes; older Vita ZIPs retained for rollback.

**2026-09-15 Dancouga suspend / battle-preview screenshots, test05 BUILT:**
Installed EBOOT still matches test02. The Air / per-Spirit status cells in
the battle preview are already included in test03/test04. Added scoped
24px sizing for both native Attack records (0x9AC94,0xB11F4), and 19px
Foc/value sizing for four battle-preview states, reserving three native
numeric/unknown cells plus a gap before the independently drawn pilot name.
Translated ALL nine dialogue records t_057 #3..11, including speaker names,
in new shared suspend_scene_dancouga canonical JSON. Original native Lua
identities match the preserved PS3 member byte-for-byte. Vita subset and
PS3 source-bound adapters now both consume the same 16 translated records
(previous Kouji/Shiro seven plus new nine); other 856 records stay unchanged.
97 Vita tests pass, zero shared-catalog issues / 475 compatibility views.
PS3 adapter encoded all 16 in memory; dedicated test_save_quit regression
with the PS3 mapping also passes, proving only the 16 dialogue bodies change.
Built work/vita/english_vwf_test_05/SRW-Z3-Vita-English-VWF-test-05.zip:
1,872,760,758 bytes; SHA256
a745b0bc709a2bec50e5be463070d581d67b0db8447c8f13774f4b9929e7db97.
All 118 rebuilt archives and 589 ZIP entry sizes/SHA256/CRC verified.
Not installed or live-tested; Vita3K remains open and installed EBOOT was
verified as test02. Saves, firmware, old ZIPs and PS3 releases untouched.

**2026-09-15 additional Vita save/settings screenshots / test04 BUILT:**
Installed EBOOT SHA256 still matches test02 (2f4558b8...982a654), so the
tactical episode heading report predates the composed-heading fix in test03.
No installation performed. New fixes: canonical ui.storage memory-card save
label, bounded discovery of individual lines in native issue_hook dialog
literals, and shared ui.command_layout SAVE_DIALOGS bindings. No arbitrary
substring matching. All eight native System Settings 1/2 records now have
24px font / 230px budget. Shared Yes/No tab controls are adapted to measured
Latin spaces near original slash/No columns; four native active-layer Xs
match the background words, including both centered and left-aligned forms.
Pointers, colors, selection flags and other bytes remain unchanged.
96 Vita tests pass; 475 compatibility views checked with zero issues.
Built work/vita/english_vwf_test_04/SRW-Z3-Vita-English-VWF-test-04.zip:
1,872,760,566 bytes; SHA256
0ec352d1e02fe81f7e6ac7c8aefe6c10ed1fdc789122e3c7da5ac5ec8f415f95.
All 118 rebuilt archives and 589 ZIP entry sizes/SHA256/CRC verified;
2,685 UI keys. BUILD_AUDIT.json and README-TEST.md accompany the ZIP.
NOT installed or live-tested; Vita3K remains running. Preserve older ZIPs
for rollback. No PS3 build, release, save or firmware changes.

**2026-09-15 Vita screenshot fixes / test03 BUILT, live retest pending:**
User explicitly requested implementation of ALL recent Vita screenshot reports,
not descriptions. See platforms/vita/screenshot_fixes.md for the checklist.
Corrected native keyword row corruption: LR contains the row across MLA at
0x810DA1FE, but the inserted BL destroys it. Keyword stub reloads that exact
fifth argument; native callback X/Y regression now passes all four rows.
Refactored shared reset stubs to fit the same verified executable gap. Added
native translated-width centering at0x81007974 (SJIS/UTF8), with native CPU tests.
UI filtering no longer mistakes literal "30% for" / "5% per" for printf;
all38 Spirit and124 skill descriptions now included. Native stage member1
OPERATE_TBL discovery covers mission conditions plus numbered variants.
Native date template/table gives77 full date keys. Native title table at
0x81328CA4 and181 metadata records at0x813291A4 produce composed headings.
Added scene_art.py for124 native P8 titles,83 map captions,5 episode effects;
Vita flags/modes/endian geometry are checked, not PS3 binary-transplanted.
Added ui_layout.py with local budgets and equal-length semantic arrays;
30 verified blank one-cell glyphs in BOTH font pages,19 movement formatter
slots (native4-byte stride), Repair/Spirit caption conflicts, popup AT/DF.
Focused 32 tests and the complete 95-test Vita suite pass. Shared-catalog
compatibility validation reports zero issues across 475 views. Full dry-run
passed: 589 verified base files, 118 CPKs, two direct files, 42,742 story
records and 2,679 UI keys. Test03 build completed successfully:
work/vita/english_vwf_test_03/SRW-Z3-Vita-English-VWF-test-03.zip
1,872,760,360 bytes; SHA256
ecd2e3249a3470315f43968942c65d44a2efe6a214dde966a8cc1c1b18611e7b.
All 118 rebuilt CPKs and all 589 ZIP entry sizes/SHA256/CRC verified.
BUILD_AUDIT.json and README-TEST.md accompany the package. No installation
or live-game validation performed. Existing test02 retained for rollback.
Builder default now fresh work/vita/english_vwf_test_03, never overwrites02.
Do not install while Vita3K PID63376 is running. Earlier read-only preflight
verified all589 installed files already match test02 exactly (user installed
it manually); the older "installation waiting" note below is historical.
No PS3 game build or GitHub release modification is requested here.

**2026-09-15 PS3 three-build boot diagnostics COMPLETE / hardware pending:**
User confirmed latest screenshot80010001 is our ISO; Japanese boot success
remains an assumption and CFW/Cobra version unknown. User requested all three
controlled tests, unsplit. Built ONLY work/ps3_boot_diagnostics_20260915:
01-SRW-Z3-Japanese-Repacked.iso (4,429,578,240 bytes),
02-SRW-Z3-Japanese-CFW-Wrapper.iso (4,434,821,120 bytes),
03-SRW-Z3-English-0.6.13-CFW.iso (4,741,267,456 bytes).
All554 files independently reread from BOTH trees in every ISO. Test01 files
match verified original disc exactly. Test02 changes ONLY EBOOT.BIN using
existing pristine work/EBOOT_dec.elf (pinned d9b198be...f959; ELF+PH headers
match original SELF, NOT newly decrypted) plus the same pinned fself method.
Test03 all554 file hashes match previous CFW-test1; this is NOT a new fix.
Full ISO hashes differ from older images due to repack timestamps. See
DIAGNOSTIC_AUDIT.json and SHA256SUMS.txt for full hashes/inventories.
platforms/ps3/cfw_diagnostics.py dry-run passed before write;17 synthetic
packaging/isolation/header tests pass. README-TEST.txt gives test order and
interpretation. No parts, install, save/firmware change, old-build overwrite,
translation edits, release counter increment, GitHub action or upload.
Send only the three full ISOs plus README/checksums, not intermediate files.
Friend should report mount/title-screen/error for each exact filename using
same manager/settings; obtain CFW/Cobra version if wrapper control fails.
Vita test02 installation below remains on hold, not changed by this task.

**2026-09-15 Vita test02 BUILT / installation waiting for Vita3K exit:**
Supersedes the source-only build status of the three Vita fixes below.
Built work/vita/english_vwf_test_02/SRW-Z3-Vita-English-VWF-test-02.zip,
1,874,616,954 bytes; SHA256
e606b7c3acacd259ce1b8d3cd934740e37b5e088d023c406e4956f754da37073.
BUILD_AUDIT.json verifies 589 entries and 118 rebuilt CPKs; includes title,
Library, startup setup and 28 opening narration rows, with 1,523 UI keys.
User requested installation. Read-only install_vwf.py preflight passed for
C:/Users/Binh/AppData/Roaming/Vita3K/Vita3K/ux0/app/PCSG00264:
4 changed files, 585 unchanged. NOT installed: Vita3K PID63376 still running
despite user's closed confirmation. Asked user to exit the actual application.
Do not kill it or overwrite a running game. Once closed, run install_vwf.py
with --game above, --build work/vita/english_vwf_test_02, --write (external
target requires elevation). Installer backs up all changed files to
work/vita/backups, verifies backups, replaces atomically, verifies all589
installed hashes, and rolls back on failure. Five installer tests pass.
Saves, firmware and licenses untouched. Runtime validation still pending.

**2026-09-15 PENDING SOURCE FIX — Vita opening narration:**
User screenshot showed first four narration rows still Japanese. Shared group
narration_0001a already has28 English rows; these are NOT in stage Lua.
Vita uses DATA/STAGE/STG0001a.cpk member7 (case as decryption audit), unlike
PS3 member6. Native member SHA256
88c8525bfa287ca31c250c7e767f6259aa995381f831088f01929a5d86dfcc8d.
Added platforms/vita/opening_narration.py; verifies8000 bytes,95 records with
20-byte header/84-byte stride,28 unique Japanese identities, measured52-byte
text maximum. Reads canonical non-expanded message IDs and current glossary;
no PS3 offset assumption. Writes only encoded text+NUL, never whole-record
padding. All timing/controls/tails and remaining bytes preserved. Long or
multiline translations fail, never truncate. Registered in build_vwf_zip.plan.
All10 narration/build-gate tests pass; no shared wording edits, ZIP/build,
installation, PS3 changes or release. Actual narration VWF/layout/transition
needs next-build Vita3K test. Other pending source fixes below remain queued.

**2026-09-15 PENDING SOURCE FIX — Vita scenario selection / protagonist setup:**
Added ui_aiddata and ui.runtime_names to native ui_text discovery. Nine existing
shared PS3 captions now included; explicit native-widget preference resolves
Done vs Finish Settings and Tutorial vs Guidance Scenario without changing
other conflict handling. Four new shared whole blood-type values, two heading
sprite messages and birthday format live in shared ui_aiddata definitions/en.
Hibiki is an exact display-only alias (native UTF8 conversion == CP932);
custom names, storage and save values are not rewritten.
startup_art.py changes only AIDDataPack.cpk member1 texture2 rectangles
(304,384,208,48) and (272,432,240,40), native Morton Y-even P8. Source SHA256
d33206f0bf10b45e88ee1b87a58f575241ac9c8e0dca1b4db12e5bf809db360b.
Palettes, UVs, other artwork unchanged. Arial Bold heading previews inspected
under work/vita/startup_review/english-startup-headings.png. Hook+art wired
into build_vwf_zip; ui_text now1523 keys/24groups. All475 compatibility views
unchanged, catalog0issues. Seven new IDs do not change PS3 adapter behavior.
Birthday native drawer at8106da1a draws numbers separately: only month suffix
call8106da7e is redirected to a12-byte relative slash stub; day suffix call
8106dad6 is suppressed. Month/day strings, numbers and input code unchanged.
Format is shared {month}/{day}; other formats fail closed pending adapter.
24 focused tests pass, including372 month/day cases and relocated stub checks.
NO ZIP/build/install/release; live alignment/rendering still needs next-build
Vita3K confirmation. Title/logo fixes immediately below remain pending too.

**2026-09-15 PENDING SOURCE FIX — Vita title/logo and Library buttons:**
User screenshots showed Japanese title wordmark/subtitle and five Library
buttons. Added platforms/vita/title_art.py for native effvita.cpk member296,
source SHA804e3007c4a84ba0181c5d4fae786a70d782d90b4a62d5b20ebec14cf456af71.
Seven linear P8 atlases, per-texture palette bank. Reuses title_logo.tiles()
approved assets and title_library_buttons.tile() shared locale labels; only
indices in7regions change. Palettes, native Z and5,655 animation samples
preserved. Wired into build_vwf_zip.plan and localization/assets.json.
Diagnostic previews under work/vita/title_art_review visually inspected.
Existing VWF-test01 ZIP unchanged; NO new build/install or PS3/release changes.
All10 tests in test_vita_title_art/test_vita_vwf_zip pass; live rendering
pending next build.

**2026-09-15 PENDING SOURCE FIX — Unit Info currency header:**
User requested translation of 所持資金／チップ： in top-right Unit Info.
tools/unit_info_currency.py patches both caption pairs (0x9a7d4/0x9a7f4,
0xb9dd4/0xb9e14) using shared ID ui.mech_info_layout:funds_z_chips,
English "Funds / Z Chips:". Joins the caption, clears the second fragment,
sets first glyph quad to23px; origins/colours/flags/numeric widgets unchanged.
Wired into build_ui.py and check_issue_fixes.py. Three focused tests pass on
pristine and0.6.13 UI buffers, checking isolation, source guards and overflow.
Localization check:0issues,475compatibility views unchanged. Not built or
installed; published0.6.13 assets remain unchanged. Runtime visual check
pending next user-authorized build. No Vita-specific adapter change.

**2026-09-14 PS3 0.6.13 — PUBLISHED ON GITHUB:**
LATEST: user requested removal of the SRW-Z3-English ZIP. Removed exactly
SRW-Z3-English-0.6.13.zip and its .zip.sha256 asset from the GitHub release;
local copies retained for recovery. Notes now list only the full ISO patch
and exact0.6.3 update, with no ZIP instructions/checksums. Two ISO assets
unchanged. Manifest package.published=false records ZIP withdrawal.
The four-asset completion details below are historical.
Latest download follow-up COMPLETE: user explicitly approved both new ISO
patch uploads and clarified repository privacy. GitHub confirms PRIVATE;
earlier mentions of public release mean non-draft publication, not public access.
Four release assets previously verified: full ISO delta149,070,914bytes, exact0.6.3
update14,825,869bytes, unchangedZIP85,048,232bytes and checksum92bytes.
New local image work/release_image_0.6.13.iso is4,996,823,040bytes, MD5
3259c2c80a98d846dcf775649990a561. Both deltas independently decode to this
image; all186 files match in both directory trees. All25 focused tests pass.
docs/releases/0.6.13-github.md now matches the published release body including
previous-format download choices/sizes/source-output hashes and instructions.
All four remote digests/sizes, non-draft/non-prerelease state and latest tag
v0.6.13 reverified. Manifest iso_package records output and patch hashes.
No full ISO uploaded, no old assets replaced, no commits/pushes/install.
Below is the earlier two-asset publication history, superseded by this update.
User follow-up requested previous-release format. Public notes now match
v0.6.3 heading/section order (Changes, Downloads, Scope and verification,
Download SHA-256 checksums); actual two assets and all warnings retained.
No patch contents, release title, tag or publication status changed.
User clarified GitHub publication. Public/latest release verified:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.13
Published2026-09-14T13:16:06Z. Two assets:85,048,232-byte patchZIP and92-byte
SHA256file. Draft notes and both remote digests verified, then published and
rechecked latest/public assets. No source commit/push, emulator install or
game/ISO upload. Tag target69e053705b81304657d528e9b5ee571ddb8ba9bd is published
master, same as preceding release; notes explicitly warn automatic source
archives do not contain uncommitted local source work. CLI requires elevated
access to existing Windows credentials; restricted401 was misleading.
Public notes: docs/releases/0.6.13-github.md. RPCS3 target, CFWtest separate.

**2026-09-14 PS3 0.6.13 — earlier local packaging:**
User requested PS3 release. Used existing validated work/build_0.6.13_batched_ui,
verified all190manifest files, snapshotted186deployedfiles with release.py.
releases/0.6.13.json now includes hash-only package metadata. release_patch.py
produced186from-original+113from-0.6.3 patches, all decoded and checked.
Original ISO MD5 and all186cached original files verified independently first.
ZIP: releases/0.6.13_xdelta/SRW-Z3-English-0.6.13.zip (85,048,232bytes),SHA256
65635a82bb66df19f23b64b79d1b3db1b47255a98c22e0f88856c9b520bc7b07.
All189ZIP entries CRC/hash verified. Includes docs/releases/0.6.13.md as
INSTALL.md through package_release.py --guide; three tests added,23focusedpass.
Target RPCS3 ELF patch; physical PS3 CFW-test1 remains separate/unverified.
No ISO/publicupload/install/translation/Vita changes. Counter stays0.6.13;
installed PS3 still0.6.12, no install performed for release-only request.
Use main ZIP on CLEAN dump, not an already patched0.6.3 dump. Update patches
exist in from-previous but are not in the main full-install ZIP.

**2026-09-14 VWF test01 — BUILT, NOT INSTALLED/RUNTIME-TESTED:**
User explicitly requested build after continued source work. New complete ZIP:
work/vita/english_vwf_test_01/SRW-Z3-Vita-English-VWF-test-01.zip
1,874,654,431bytes; SHA256
0f7ba197c47c8c8a7f86e4cae33bfac6f7d6b2080257cdd54f2487b13cdceb6d.
BUILD_AUDIT.json beside ZIP records catalog revision, categories and589 file
hashes. 116rebuiltCPKs,2directfiles(EBOOT+SRVC),5convertedmodules,466unchanged.
All CPK members and ZIP entries independently read back. 89focusedtests pass.
Builder: platforms/vita/build_vwf_zip.py, dry-run then --write into NEW folder.
Port(sink=...) emits verified bytes; default category CLI still audit-only.
build_install_zip.prepare(include_pilot=False) supplies clean base and native
modules without old digraph overlay. Newbuilder composes UI+VWF then SRVCtable
and matching95single-letter fontcells. Combined EBOOT hash
b996b0b40094fb04a313c22736fe8eec3a250b240487b7a0af24ac862c62eb6f.
42,742story/31,666battle/1,510UI pluslibraries,keywords,gameplay,7suspend lines.
Read VWF_TEST_ZIP.md. No license/firmware/saves included; previous outputs and
installation untouched. First priority now is actual Vita3K boot/VWF/layout
testing; unresolved textures/dynamiclabels/865suspend lines remain incomplete.
Do not confuse this with the earlier244recordfixed-cellpilot below.

**2026-09-14 continuation: MtV descriptions/titles — earlier source pass:**
ui_text.py now hooks0x810d9dd8 before native line counting/splitting;32-byte
wrapper0x812b5ee4 calls existing lookup, preserves r2/r7/LR/SP/s0-s1, handles
NULL, replays ADD flags and stack store. Same REL32/table, no new relocation.
Reject English lines over256 encoded bytes; none of current entries excluded.
Added independently source-located shared scenario_titles (109keys) and
ui.episode_heading_hooks (28keys). Total1510keys,180404-byte table;523unlocated.
No title textures or arbitrary composed episode headings ported by this change.
Latest audit work/vita/ui_text_audit_02.json; in-memory SELF hash
b075d07415ab7a5b382685111654010fa653452469a9d1581a64a53106d92713.
12UI tests including original MtV entry/linecounter with only strlen mocked;
all61Vita+18localization tests pass. No package/install/shared wording edits.
Still need live layout, other dynamic fragments, title sprites, measured
centering/link rectangles, and coherent builder when user requests build.

**2026-09-14 native Vita UI/help hook — SOURCE ONLY, NOT BUILT (earlier pass):**
Latest user said continue. Added ui_text.py and category_port ui_text category:
1,373 checked exact keys across20 shared groups, NOT a runtime-complete UI port.
104-byte Thumb hook0x81006e50 after optional UTF8 conversion; stub0x812b5e7c
in remaining VWF reservation, second REL32 delta0x812b5f38, table0x8168c620
after VWF scratch/BSS. Source guards, old code/data/reloc preservation checked.
Native converter0x81006d54 uses two-byte ASCII font codes: converted_key mirrors
tables0x812d8ac0/0x812b8ac0 and is tested against original converter logic.
Sources: pinned EBOOT, audited AIDDataPack member0 ASSF (5440 header-bounded
LE widget records), audited RPW. Hash+fullcompare, no prefix/fragment edits.
13 conflicts excluded; 12 PUA,46 formats,519 unlocated,1 no-source excluded.
9 new tests; full 59 pass, including original drawer/converter CPU integration,
independent text/data loads, large table, collisions, register/flag safety and
composition with a separate native SRVC table edit.
Audit work/vita/ui_text_audit_01.json; see Vita VWF.md/COVERAGE.md. No shared
wording/IDs, installed game, pilot ZIP or VWF candidate files were changed.
Still need actual Vita3K UI paths/layout: some callers split multiline text
before this hook. Stage-title/sprite/art bindings, scoped conflicts, dynamic
messages and remaining suspend scenes still open. ui_text.patch composes VWF
from pinned ORIGINAL SELF, not an already patched executable. Future coherent
builder must combine this with SRVC table edits and matching data/fonts.

**2026-09-14 broad Vita category pass — SOURCE ONLY, NOT BUILT:**
Latest user asked to continue translating every Vita category. Implemented
platforms/vita/category_port.py, a dry-run/in-memory compiler and JSON audit
writer, NOT connected to old pilot/ZIP builder. Read platforms/vita/COVERAGE.md.
42,742 shared story records / 201 native members match exact source and pass
VWF/layout/control checks. Display-only half-width quote aliases (66 pairs)
and soft-line reflow resolve initial 81 failures without changing wording.
Libraries (141/408/253 entries), actual MTFL keyword popups (141), RPW terms
(1,685 strings + 953 overrides) and 31,666 battle subtitles pass data checks.
SRVC table independently located in native SELF segment 1 +433180, 277 LE
u32s; helper resolves current segment position, guards source and inverse.
Table and rebuilt SRVC must accompany the SAME VWF/font candidate in future.
7/872 suspend records ported in memory; other 865 untouched. Seven canonical
source definitions enriched from fingerprint-matched JP, no English/ID edits.
UI 817 found / 154 ambiguous / 1,560 unlocated = candidates ONLY, not hooks.
Still missing native menu/help placement, effect descriptions, stage-title and
map sprites, approved art conversion, remaining suspend translation, runtime
proof for all categories. No package, installed game, PS3 release or previous
VWF candidate changed. Detailed audit: work/vita/categories_audit_02.json.
50 focused tests pass (11 new category tests); 82,457 catalog entries validate,
all 475 compatibility views unchanged. build_library._rendered now accepts an
optional Vita wrapping callback; default PS3 behavior remains tested.

**2026-09-14 shared localization migration — SOURCE ONLY, NOT BUILT:**
User authorized shared PS3/Vita text and future languages. Canonical English
is now localization/locales/en/*.json; IDs/JP/context in localization/messages/.
475 old JSON/TSV files are byte-identical compatibility views, not editable
authority. 45 UI Python modules now resolve 429 literal bindings from JSON;
AST round-trip proves unchanged English and all non-text code. 82,457 messages
imported; 244 Vietnamese drafts preserved with needs_review status. See
localization/README.md for check/sync/scaffold/export workflow and limits.
PS3 legacy templates and UI literal locators live in platforms/ps3/localization/;
Vita consumes the SAME canonical records through trdata, matching original
source identity. Only its three opening groups are bound; no PS3 offsets copied.
Full English preflight rejects stale compatibility views. No game rebuild,
installation, ISO/ZIP replacement or VWF candidate changes performed here.
Old translation merge writers need temporary output + reconciliation by ID;
do not edit generated mirrors or rerun the one-time importer. Raster logo/audio
exceptions documented in localization/assets.json. See changelog for checks.

**2026-09-14 Vita real VWF — SOURCE/LOOSE CANDIDATE, NOT RELEASED:**
User screenshot now shows the old English pilot running opening dialogue in
Vita3K, with fixed/digraph spacing. User requested a proper Vita VWF port and
asked to reuse the PS3 implementation. Core source port is implemented, NOT
yet runtime verified. Respect batch/build-only-on-request rule: no new ZIP,
CPK build or emulator install this turn. Old runnable pilot is unchanged.
Read platforms/vita/VWF.md for pinned addresses, invariants and next work.
Sources: vwf.py, prepare_vwf.py, inspect_vwf.py; shared audited input loader
extracted from build_test.py without changing default fixed-cell behavior.
PS3 rasterizer + width rules reused, native ARM/Thumb hooks and Vita P4 cells.
Six hooks: glyph advance, four MtV piece positions, pixel accumulation. 95
single-letter cells; all other glyphs retain original spacing. Relative code
in verified text gap; scratch appended after original BSS with a SCE REL32
relocation entry supporting independently relocated code/data. 38 Vita tests
pass, including 10 VWF tests: execute generated hooks at varied load addresses and run
the actual original drawer with only GPU calls intercepted. 244 opening
records verified against shared English, non-dialogue/control bytes exact.
work/vita/vwf_candidate_02 has loose EBOOT, two GXT and three Lua members,
audit/mapping and OFFLINE font_proof.png. EBOOT SHA256
df7a11494282d1d88d47e0ff3571f5c3f845aa62ccb301fc6b8e0df3c22c6044.
Candidate_01 is an earlier analysis intermediate without the added relocation;
retain but NEVER package it. All55 focused tests pass (38 Vita/12 shared/5 CPK).
Do NOT install loose EBOOT alone with old digraph CPKs: encoding/font/hooks
are one unit. Still pending runtime/visual test, link highlight/hit-box sizing,
centered/name/UI layout and wider translation coverage. Do not call complete.
Local dependencies in ignored work/vita/python_deps: Capstone4.0.2,
Keystone0.9.2, Unicorn2.1.4 alongside prior PyCryptodome3.23.0. Read-only
full Thumb analysis at work/vita/vwf_original_thumb.txt; data/jump tables can
misdecode, so start disassembly at known aligned functions. No subagents used.

**Earlier 2026-09-14 Vita complete patched ZIP — BUILT/FILE-VERIFIED:**
Opening dialogue subsequently observed in the user's screenshot (above);
the original packaging handoff below records the checks performed at build time.
Latest user explicitly requested complete installable patched ZIP for Vita3K.
Delivered work/vita/english_pilot_01_install/SRW-Z3-Vita-English-pilot-01-install.zip,
1,874,630,556 bytes, SHA256
a20e507926427250435dd8f7b150389ff0bb4b8c429751d7b88e02499737818d.
This supersedes the two-step original-PKG/overlay instructions below. Use File
-> Install .zip/.vpk in Vita3K, then New Game. Firmware/fonts still required.
Do NOT ask the user to install the original PKG first for THIS complete ZIP.
589 files (2,341,565,849 expanded bytes): 3 English CPKs from checked overlay,
6 decrypted SELF executables, 580 unchanged source files. 244 opening records
only; menus/names/battle UI/later stages remain Japanese, NOT full English port.
All 30 executable segments decrypted and zlib checked, byte-preserved in plain
SELF wrappers. No instruction patching. ZIP read-back verifies every size/SHA256
and CRC; no sce_sys/package, sce_pfs, work.bin, license, firmware or saves.
INSTALL_AUDIT.json, README-INSTALL.md, .sha256 accompany ZIP; summary manifest
platforms/vita/install_pilot_01.json. New source self_decrypt.py and
build_install_zip.py; public references under ignored work/vita/self_reference
with pinned SHA256, isolated PyCryptodome3.23.0 in work/vita/python_deps.
45 focused tests passed (28 Vita/12 shared/5 ITOC), including 10 new synthetic
SELF/package checks. Scripts dry-run first, --write only to new work/vita dir.
No user emulator install, boot test, firmware/save changes, original inputs,
canonical English, PS3 installation/releases/counter changes. Vita3K running
and app folder previously empty; don't force-close or claim runtime success.
Next: user installs complete ZIP and reports first English dialogue screenshot,
boot, links/Back Log/skip. Packaging checks are NOT emulator compatibility proof.

**Earlier 2026-09-14 English Vita pilot overlay — historical:**
User requested English build; target Vita3K PC, E:/Emu/vita3k. Built a LIMITED
opening-stage 244-record overlay (0001A ID4, 0001B IDs3/4), NOT full port.
Output `work/vita/english_pilot_01_checked` has verified overlay ZIP (6,783,105
bytes; SHA256 f713cfd9bad1dd50a7d1785d54c3f176a2ed5847b05c65eec9c669969e3e6eaa),
BUILD_AUDIT.json, font_mapping.json, font_proof.png and README-TEST.md.
First output `work/vita/english_pilot_01` is INCOMPLETE (preview label had a
character absent from corpus); retain as failed intermediate, never install it.
Exact shared record/source matching and English codec round trips passed.
All non-dialogue Lua bytes unchanged: preserve control flow, speakers/keyword IDs.
Only 3 CPKs changed: DATA/STAGE/STG0001a.cpk, STG0001b.cpk, and
DATA/tabata/TPACKVITA.cpk (note original lower-case tabata; don't rename in ZIP).
144 archive members checked; unchanged compressed members byte-identical.
Vita fonts (members1/3) are linear P4 GXT, 4096x1120, 2 palettes. Visually
confirmed SJIS anchors !9/0=207/A224/a257 and Japanese cells. Adaptive pair
dictionary uses 488 originally blank/unassigned cells only; no kanji/Greek loss.
English exactly preserved, max28 cells/line incl conservative placeholders,
up to4 lines. Geometry/budgets provisional until runtime; not a VWF port.
Independent diff checked every changed font byte belongs to selected blank
cells; original palettes/headers intact. Offline rendered preview inspected.
35 tests passed: 18 Vita,12 cross-platform,5 ITOC. No game installed or booted.

Tools: platforms/vita/build_test.py (dry-run then --write/new output),
font_gxt.py, text_codec.py, inspect_pilot.py; install_test.py (dry-run then
--write, verifies base/build hashes, requires Vita3K closed, backs up originals,
rolls back copy failures, no executable/license/saves touched). Tests in
tools/test_vita_build.py; docs platforms/vita/TEST_BUILD.md and README.md.
User says firmware installed, but configured app folder was empty:
`C:/Users/Binh/AppData/Roaming/Vita3K/Vita3K/ux0/app`. Vita3K was running.
Asked user to install original PKG+work.bin, confirm Japanese New Game boots,
then close normally; replied only firmware installed so far. DO NOT claim
firmware/game fully verified or force-close. Next: confirm actual game path,
base boot, then install_test.py --game <.../ux0/app/PCSG00264> dry-run, inspect,
--write with required filesystem approval. Test stage1 text/links/Back Log/skip.
No changes to PS3 game/releases/counter, canonical translations or originals.
Menus/names/combat UI/later stages remain Japanese. Full English port unfinished.

**2026-09-14 Vita PFS decryption — COMPLETE, PORT NOT PLAYABLE YET:**
Latest "do it" authorized actual offline decryption. Extracted with locally
compiled pkg2zip; isolated Vita3K native parser passed metadata/signature,
file decryption and keystone checks. Data: `work/vita/decrypted_PCSG00264`;
encrypted source: `work/vita/app/PCSG00264`; independent audit with all hashes:
`work/vita/decryption_audit.json`. 589 files, 176 CPK archives / 35,861 members,
189 GXT signatures verified; 3 opening candidate members read/decompressed.
EBOOT is SCE SELF: inner executable decryption NOT verified. Translation IDs
and records remain candidates, not confirmed mappings. Seven tests pass,
including fake-key rejection at mount without creating output and overwrite
rejection. No real license in tests/logs/reports/CLI arguments; no key upload.
Original PKG/work.bin, PS3 releases/install, shared English and counter untouched.
See platforms/vita/DECRYPTION.md for public source pins, tool hashes and commands.
Next: strict source/control record matching, then Vita-specific font/layout and
executable work. Do not repeat decryption into existing output or claim playable.
Older license-only note below is historical and superseded by this result.

**2026-09-14 earlier Vita license check — MATCHED, then awaiting PFS:** user said
"do it" to local work.bin validation and offline-path check. Added
platforms/vita/validate_license.py; read-only default, bounded binary reads,
outputs only whitelisted title ID/booleans, never key/zRIF/account values.
Dry-run then optional report saved `work/vita/license_validation.json`.
512-byte license matches full PKG content ID PCSG00264; NoNpDrm header/account
marker + nonzero key present; PKG size matches header. Five synthetic tests
pass. This is NOT cryptographic validation; do not call it decrypted/playable.
No changes to originals, PS3 installation, shared translations or build state.

Public source-only clones under work/vita:
- nonpdrm_source: TheOfficialFloW/NoNpDrm, 83722257a1e68d5eea4cb5823f203d39b19cfd84.
- psvpfstools_source: motoharu-gosuto/psvpfstools master,
  558b91ca401cbf2720b44e8d65e232ce248b795a; only URL/cache F00D backends.
- offline_pfs_source: Vita3K/psvpfstools e21df9a74852433f48d6593b8ef203dc7c424e05;
  submodules uninitialized because git-submodule shell failed to find sed/basename
  even with a scoped Git usr/bin PATH. No source or license failure implied.
- offline_parser_source: standalone Vita3K/psvpfsparser checkout,
  d14381f871a69009bd18b2aaec2213a6738bebba. Factory provides native F00D backend
  using F00DNativeKeyEncryptor; C++17/OpenSSL3/libzRIF/libb64/zlib dependencies.
  This avoids sending keys to an online service; not compiled/run yet.
Next implementation step: prepare that native offline tool, guard/suppress all
secret logging and avoid key command-line arguments, unpack own-copy PKG into
ignored work/vita and verify PFS decryption before comparing shared records.
No extra user file needed to attempt this. Do not request online-key-service
approval or a decrypted dump merely because the OLD tool lacks native crypto.

**2026-09-14 approved CFW hardware-test package — COMPLETE, HARDWARE UNTESTED:**
User approved preparing a separate CFW test after screenshots showed 0.6.10
rejected from internal HDD (`ENCRYPTED/INVALID ISO`, XMB `80010017`). Local
0.6.3/0.6.10 images contained plain ELF EBOOTs and stale original disc-region
ends/UDF metadata. Created a new package ONLY in `work/cfw_0.6.13_test1` from
verified original ISO + validated `work/build_0.6.13_batched_ui` (186 files).
No install, firmware/save changes, public release/upload, translation changes,
or counter increment. Existing RPCS3 game remains 0.6.12; do not install this
CFW wrapper there. The earlier 0.6.13 RPCS3 snapshot remains untouched.

Full image: `SRW-Z3-English-0.6.13-CFW-test1.iso`, 4,741,267,456 bytes.
FAT32 delivery: package `PS3ISO/` contains `.iso.0/.iso.1/.iso.2` of
2,147,483,648 / 2,147,483,648 / 446,300,160 bytes. `README-TEST.md` has transfer
and hardware-test steps. `CFW_AUDIT.json` records full/part hashes and all
554 files. Both fresh ISO9660 and Joliet trees verified independently; split
concatenation matches full ISO. One plaintext region covers all 2,315,072
sectors. Fresh ISO has no stale original UDF tree; primary aliases and full
Joliet shader names preserved.

Tool: `platforms/ps3/cfw_package.py`, dry-run first then --write; refuses old
output directories. Pinned PSL1GHT checkout in ignored `work/cfw_psl1ght`,
commit f649a08fd536a9e27c08c7db2d93a2d7ee4c3bbe. Only source change is missing
.sceversion guard in fself/source/self.c, documented in platforms/ps3/CFW_TEST.md.
GCC 12.2.0 compiled fself.exe SHA256
b3bc066b39b69adff7fd59c849b14bb8754c4c306c549aa1ecd791b953799554.
Fake SELF retains original APP_INFO/capabilities, preserves all 9,371,648
ELF bytes, and passes 8-segment mapping/header/digest checks. Eight synthetic
packaging tests pass, including corruption and overwrite guards. No retail
signing claim: target CFW+Cobra/fake-SELF support only. Physical console
mount/boot/play and translation-hook runtime stability remain UNTESTED.
Next: friend tests this exact filename and reports firmware/Cobra/manager
versions, mount vs launch result, then menus and stage-10 ending skip.
Do not call hardware compatibility fixed until those tests succeed.

**2026-09-13 shared PS3/Vita setup — NO BUILD/INSTALL:** user authorized
reorganization and initial Vita translation. Canonical English remains in
translation/ plus analysis/glossary.json; shared/catalog.json describes it.
Moved PS3 config to platforms/ps3/manifest.py, old path is a runpy compatibility
loader. Verified all 109 STAGES and 3 LIBRARIES equal pre-move HEAD data.
Updated register_stage, stage_status and check_names readers for the new path.
tools/shared_content.py fingerprints actual shared files (not only git HEAD);
future PS3 manifests include platform/shared_content. Prior builds untouched.
Vita pilot config + prepare_translation.py reference 3 opening-stage shared
JSONs: 244 records (25/117/102), expanded from the same glossary. Dry-run then
--write creates work/vita/initial_translation.json, explicitly unverified and
not playable. Its match_records gate is for future exact Vita source matching,
not evidence that matching has happened. See platforms/vita/README.md.
User confirmed only E:/SRWZ3/iso/SRW Z3.1 Vita.pkg + work.bin, no decrypted
folder. Prior read-only PKG inventory found PCSG00264 01.00, 176 CPK, 189 GXT,
matching archive families, but payload remains inner PFS-encrypted after outer
PKG decoding. Five matching library archive sizes are NOT a content match.
Next blocker is local/offline PFS decryption or user's decrypted own-copy dump;
never upload license keys/work.bin to a service without explicit authority.
No license bytes read, no game files moved, no Vita patches or runtime tests.
Saved the ignored 244-record review bundle after dry-run. Checks: 12 new
cross-platform + 15 build-version + 8 partial-translation tests passed. Existing
unrelated whitespace warnings in deploy/extract/apply_xdelta remain untouched.
0.6.13 installation below remains pending; do not confuse it with a Vita build.

**2026-09-13 requested batch build — 0.6.13 BUILT, INSTALL PENDING:** user
said "ok build", lifting the build gate for the accumulated fixes. Complete
build `work/build_0.6.13_batched_ui` exited 0 and stamped build_version.json
0.6.13. Log: work/build_0.6.13_batched_ui.log. All packed validation passed;
4,019 hooks, zero undrawable. All 31 focused tests passed across record
categories, menus, training/help, parts/prep popup, link backgrounds,
save/quit and CPK ITOC. All 110 stage plaintext archives byte/hash-match
0.6.12; approved logo included. Translation remains partial (1,034 mission
variants), accurately recorded in the manifest. No ISO or public release.
RPCS3 process 53916 remained running after build completion; asked user to
close and reply done, including async question. No install attempted or
installed files changed. Next: recheck RPCS3 closed, run install_build.ps1
dry-run for this build, then -Write with required filesystem approval.
Verify all installed hashes/saves/registration, then update this status.
Canonical target is game/, not an older ISO. No active build process remains.
Build command used translation/manifest.py, work/TPACKPS3.CPK, --vwf,
--ttf E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF,
--eboot work/EBOOT_dec.elf, --partial-translation,
--npdata E:/Projects/SRW Z3_wt2/work/make_npdata.exe (read-only helper;
the main workspace's old work/make_npdata.exe no longer exists).

**2026-09-13 record title follow-up — SOURCE FIXES ONLY:** actual Pilot TOP 5
and Trade List captions are fragmented FSSA widgets, not the guessed composed
strings / UTF-8 Key Help caption patched earlier. record_screen_labels now
consolidates a03f4/a03d4/a0374/a0394/a03b4/a0414 into `～ Pilot TOP 5 ～`,
two Ace Pilot variants a07f4..a0854 and a0874..a08d4 into `Ace Pilots TOP 5`,
and a25f4..a2654 plus a2a54..a2ab4 into `: Trade List`. English lives at the
first visual fragment; other group strings blank. Only pointers and first
X change; original group bounds determine ink centering. Styles preserved.
Remove six ineffective whole-title hooks. trader_ui shortens a2694/a2af4
to Systems and sets a2674/a2694/a2ad4/a2af4 to 23px for a >12px gap inside
the screenshot's ~150px category column. Buy a26f4 stays Upgrade Systems.
Packed checks validate title positions/styles and category sizes/fit.
Eight test_record_categories checks pass, including actual production UI
pass ordering in memory (stops before output files), plus four menu and
three Combat Record regressions. See docs/RECORD_SCREEN_TITLES.md.
No build/install, keep batching until user explicitly requests a build.

**2026-09-13 link background batch — SOURCE FIX ONLY:**
tools/link_background_layout.py fixes shared selected-link rectangle width
reported for Kurara in Back Log. Proven original computation at
0x1c8730..0x1c87b0 is `(byte_count>>1)*style[0x2e]`; it ignores VWF.
Only direct caller of link registration 0x1ce098 is 0x1d1e10, after the
0x1d1dd8 draw. Capture PEN_ACC at registration 0x1ce18c (keep original stb),
indexed by stack +0x70 bank / +0x74 slot, 16x16 entries. Float cache lives at
BSS_PAGE+0x1000..0x13ff, outside 4KB HOOK_SCRATCH and before HOOK_JSTATE.
Hook 0x1c871c preserves mr r29,r3 and caches width selected by r4 (still the
index from 0x1cdbb0) to unused highlight-frame +0x88; hook 0x1c87b0 writes it
to rectangle +8 instead of byte-count width. X/Y/height/colors/record metadata
remain unchanged. Three helpers at 0x78ed00/ed80/edc0 fit between command
data and President helper. Integrated in apply_vwf edited ranges and packed
check_issue_fixes. Three focused tests pass, including emitted instructions,
256 slots/reuse, metadata/write isolation, English/Japanese actual glyph
advance and real in-memory patch pipeline. No build/install; keep batching.
Also passed three preparation-menu and five save/quit regression tests;
scoped whitespace checks clean. build_version.json remains 0.6.12.

**2026-09-13 parts/preparation popup batch — SOURCE FIXES ONLY:**
tools/parts_menu_followup.py repoints 11 UI records: two Remove hints,
three Qty., three Select No., standalone Pilot and split Pilot/blank suffix.
Wired after training_help_layout in build_ui and packed checks. Existing nine
Z Chips pairs already cover the repeated screenshot; no duplicate change.
command_layout.PREP_ROWS scopes seven executable source strings
0x6d5430..0x6d54a0 to centered popup labels, with Ship Upgrades shortened only
in this popup. Search and Menu:Command heading unchanged. Appended pad
codes 0x8897..0x889d, Unicode 0x2c6..0x2cc; existing pad indices unchanged.
The VWF dispatcher must remain its original size (additional comparisons
overlap the keyword stub): extend its existing upper bank, recognize new
indices inside command_layout.stub. The lower deployment/save upper bound
now explicitly ends at PREP_START-1. check_command_layout verifies all popup
descriptor pointers against work/EBOOT_dec.elf. Three new focused tests pass,
including real in-memory UTF-8 patching, all 199 live-pad slots, ordinary
glyph boundaries and blank cells in both original font layers. No full build
or installed-file writes. Continue batching; installed version stays 0.6.12.
Also passed all 12 regressions in test_training_help (3), test_save_quit (5)
and test_menu_followup (4). Scoped diff whitespace checks are clean; older
unrelated trailing whitespace in deployment manifests remains untouched.

**2026-09-13 training/help batch — SOURCE FIXES ONLY:** added
tools/training_help_layout.py: Learn Skills tab shift -32 native pixels on
all three split state pairs plus standalone caption, leaving Raise Stats,
baselines/fonts/selection flags unchanged; translates four Key Help hints,
both Select Slot prompts, Right Stick, and parts-slot explanation. Wired
into build_ui and packed checks. tools/key_help_labels.py inventories 91
action strings in the separate UTF-8 Key Help table between class anchors;
eboot.load_commands adds this family for UI_UTF8_FILE only, preserving
existing shared translations. Includes the UTF-8 parts-slot explanation.
All three test_training_help tests pass, including in-memory real UTF-8
patching and readback of every source table reference. No files built or
installed this turn. Keep waiting for explicit build instruction; installed
version is still 0.6.12. Latest source changes accumulate with prior batch.

**2026-09-13 menu screenshot follow-up — FIXES STAGED, BUILD STOPPED:** user requested
D-Trader Sell prompt translation, Network PS Store alignment, clipped
Commander heading, and Pilot List/Upgrades/Search/Options/Network centering.
New tools/menu_followup.py patches four sell/carry prompts, two Cmdr headers,
nine split Z Chips footers (also Japanese in the capture), and 12 normal /
highlighted button records, including alternate Network pair. Corrections
use measured ink/button centres from the supplied capture. Existing
Change Pilots correction remains untouched. intermission_layout.py adds
the live PS Store offset to both captions, keeping blank suffix fragments.
Four new tests and three existing alignment tests pass. build_ui preflight
work/menu_followup_preflight passes. User then instructed: more fixes are
coming; fix all of them and DO NOT BUILD until explicitly told. Interrupted
full build work/build_0.6.13_menu_followup (exit 1); no successful build or
install. build_version.json and installed game remain 0.6.12. No active build
job. Keep batching source fixes and tests, recording each in CHANGELOG.md.
Do not ask to close RPCS3 again until the user requests a build/install.
No ISO or release requested. The new alignment still needs live testing
after a future authorized build; do not claim runtime verification.

**2026-09-13 approved subtitle — 0.6.12 INSTALLED:** user asked to install
the September 12 redesign (large TIME PRISON, small CHAPTER), not the old
equal-weight tile included through 0.6.11. Recovered approved images from
this task's image-generation history, copied into work/title_logo_draft as
subtitle-approved-v2.png and combined-approved-v2.png. User explicitly
authorized scripted background removal/resizing. New tool
prepare_approved_subtitle.py produces work/title_logo_final/subtitle-v2.png;
old subtitle.png is retained. title_logo.py now guards and uses the new tile.
No new image generation; main title and native Z untouched. All 19 title
tests pass. Full build work/build_0.6.12_approved_subtitle completed with
exit 0; all packed checks passed. All 110 stage plaintext archives match
the repaired 0.6.11 outputs exactly; five archive regression tests pass.
With RPCS3 closed, install_build.ps1 dry-run and -Write completed. All 186
installed targets hash-match; all 560 disc files verified; 17 save files
unchanged. Backup: work/install_backups/0.6.12_20260913_161159. Registered
game/ and other-game registration preserved. Cache was already absent, so
none was moved this install. No new ISO; old 0.6.10 ISO remains unchanged.
User should launch game/ to test the new subtitle and stage-10 skip repair;
neither has been runtime-verified this turn.
Independent 0.6.11-vs-0.6.12 effects audit confirms all 333 other stored
members unchanged; member 296 differs only in subtitle pixels and version
footer. Main wordmark, native Z and all animation records are unchanged.
No active build/install/audit jobs remain.

**2026-09-13 stage-10 skip black screen — 0.6.11 INSTALLED:** runtime log last
opened INSCO/DATA0169.DAT, byte-identical to 0.6.10 STG0018.SDAT.cpk.
Stage 10 is internal STG0017; its clear function selects STG0018. Both
dialogue members of STG0018 grew beyond 65535 bytes. cpkpatch._move_to_datah
updated the parent index twice but used the original header ItocSize on each
update, declaring 380 bytes instead of 384. Five 0.6.10 archives affected:
STG0016, STG0018, STG0029, STG0067, STG0074. All 142 originals pass the new
validator. Fixed header calculation from current chunk, added build-time and
complete-build guards and five test_cpk_itoc regressions (all pass); eight
partial-translation tests pass too. Complete rebuild passed as
work/build_0.6.11_stage_transition, log alongside (process completed, exit 0).
Build version is now 0.6.11; 4025 hooks, zero undrawable. All 110 rebuilt stage
archives validate; only byte 0x106 changes in the five affected plaintext
CPKs. All members, dialogue and event logic match 0.6.10; all 109 encrypted
STG outputs independently decrypt/hash-match their rebuilt CPKs. After user
closed RPCS3, install_build.ps1 dry-run then approved -Write completed:
186 installed targets hash-match, 17 saves unchanged, complete disc checked.
Backup: work/install_backups/0.6.11_20260913_155513 (includes old install cache).
Registered game/ and BLJS10299 registration preserved. Game recreates cache
on next launch. No active build/install jobs. User in-game skip retest is
required; archive defect is proven, runtime resolution not yet.
Existing 0.6.10 ISO remains unchanged/affected;
no new ISO requested this turn. Earlier Tag Command live Japanese choices
and footer clipping are diagnosed but NOT fixed by this archive-only change.

**2026-09-13 requested local ISO completed:** user explicitly requested an
ISO despite the default single-folder preference. Project root now contains
SRW-Z3-English-0.6.10.iso (4,996,820,992 bytes), built from verified original
Japanese ISO plus work/build_0.6.10_record_categories. All 186 translated
files match in primary/Joliet trees; all 554 original disc paths verified
(553 against game/, firmware PUP against pristine ISO). Folder-only backups
and build metadata excluded. SHA-256 and details: work/iso_0.6.10_audit.json.
No release, install, registration or saves changed; no active packaging job.

**2026-09-13 build 0.6.10 INSTALLED — record-screen categories:**
work/build_0.6.10_record_categories passed complete packed validation.
tools/record_screen_labels.py adds 11 composite Spirit targets, 26px target
prototype only, ranking-switch hint and source Pilot TOP 5 title prototype.
Six composed-title hooks are screenshot-derived fallbacks; exact live title
construction remains unconfirmed. tools/trade_list_flavor.py covers all 18
original EBOOT lore entries 0x70d970..0x70e508, glossary-expanded and wrapped
to three lines, distinct from part effects. UTF-8 Trade List caption added.
Four new tests, eight partial-build tests and three Library/episode regressions
passed. Build emitted 4025 binary hooks (71 slots below the 4096 cap) with
zero undrawable entries. Additional candidate checks confirm all 17 joined
target/title flags, actual UTF-8 Trade List caption and untouched source lore.
Dry-run then approved install with RPCS3 closed verified 186 game targets and
16 unchanged saves. Backup: work/install_backups/0.6.10_20260913_105129.
Registered game/ and BLJS10299 registration preserved. Changelog updated.
No active build/install sessions or release. User live retest remains needed,
particularly the unconfirmed Pilot TOP 5 runtime title and Spirit targets.

**2026-09-13 build 0.6.9 INSTALLED — Change Pilots alignment:** normal intermission
caption measured x=1032..1405 against button x=876..1395 in user's 2560x1440
capture. tools/pilot_swap_alignment.py moves normal record 0xa3314 by -41.5
native pixels; highlighted 0xa3334 uses proportional 31/28 correction.
Only the two X-coordinate fields change; fonts/hooks/colors/Y and the
team-editor caption 0xb22d4 are untouched. Two targeted tests, Library
alignment regression and eight partial-build tests pass. Complete build
work/build_0.6.9_pilot_swap_alignment passed packed checks. UI member comparison
against 0.6.8 confirms six changed bytes within the two allowed X fields.
User closed RPCS3; dry-run then approved install verified 186 game targets
and 16 unchanged saves. Backup: work/install_backups/0.6.9_20260913_100131.
Registered game/ unchanged. No active build/install sessions. Changelog
updated; no release published. Live user retest, especially highlighted
state (scaled correction, not captured), remains necessary.

**2026-09-13 build 0.6.8 INSTALLED — Library/faction/episode categories:**
tools/library_list_labels.py translates 12 title/name/sort widgets, including
both duplicate Glossary screens. Kana Order remains Japanese sorting, not
English alphabetic sorting. tools/episode_heading_hooks.py derives 369 exact
keys from original EBOOT 181 stage records / 159 title pointers, reusing 124
reviewed titles and translating 35 route/data/gift labels; script comments
have stale episode numbers. Original title pointers and save data untouched.
All 157 preset squad/faction keys now use existing joined-text matching as
well as contiguous matching. This is a fallback for the still-Japanese map
label, not a proven live root cause; user retest remains required.
Three category tests and eight partial-build tests passed. Complete build
work/build_0.6.8_library_categories passed packed checks (3937 binary hooks).
Dry-run then approved installation verified 186 game targets and 16 unchanged
saves with RPCS3 closed. Backup: work/install_backups/0.6.8_20260913_094904.
Single registered game/ folder retained. Earlier attempt was interrupted
before numbering to include duplicate Glossary titles. No running build or
install session remains. Changelog updated; no release published. User live
retest is required, especially the Mech. Beast Army map faction label.

**2026-09-13 build 0.6.7 INSTALLED:** Library title horizontal alignment
corrected using colored-glyph bounds measured in the user's live 2560x1440
capture. intermission_layout.LIBRARY_LIVE_X_CORRECTION adjusts all six
title records (five labels) without touching font size, special mode 0x01,
plain glyph strings, colors or vertical positions. test_library_alignment
passes measured-center/button-boundary/state-preservation checks. Complete
work/build_0.6.7_library_alignment passed packed checks; dry-run then approved
install verified 186 targets and 16 unchanged saves, RPCS3 closed. Backup:
work/install_backups/0.6.7_20260913_091550. Registered game/ unchanged.
Changelog updated; no release published. Live user retest pending.

**2026-09-13 build 0.6.6 INSTALLED:** screenshot's reverse-order button
hint now `: Reverse Order`; both split teams-aboard captions now `Teams Aboard`
via tools/aboard_order_labels.py (seven text records). Captions use 20px
type, 16 native pixels earlier to preserve live-count space; no global
fragment replacements. Source-inventory/isolation and currency tests pass.
work/build_0.6.6_aboard_order passed complete packed checks; dry-run then
approved install verified 186 targets and 16 unchanged saves, RPCS3 closed.
Backup: work/install_backups/0.6.6_20260913_090341. Registered game/ unchanged.
Changelog updated, no release published. User live layout retest pending.

**2026-09-13 build 0.6.5 INSTALLED:** reported 119992 Funds overlaps its
fixed colon. tools/deployment_menu_text.py now omits all six Funds/Z Chips
separators across three panel variants; live values/positions remain intact.
tools/test_currency_counters.py passes isolation/category checks. Complete
work/build_0.6.5_currency passed packed checks; dry-run then approved install
with RPCS3 closed verified 186 game targets and 16 unchanged saves. Backup:
work/install_backups/0.6.5_20260913_085205 (old cache retained). Registered
game remains E:/Projects/SRW Z3/game. Changelog updated, no release published.
User live retest pending. This supersedes the installed version below.

**2026-09-13 build 0.6.4 INSTALLED:** native map support-word quads widened
by tools/support_popup_layout.py; trader_art keeps their natural shared point
size. Separate CMN battle-animation textures are NOT the reported surface and
remain unchanged. translation/squad_names_hook.json covers 157 literal team
names from 142 original stage archives, checked by audit_message_classes.
Four new test_support_squad and eight partial-build tests passed. Complete
build work/build_0.6.4_support_squads passed packed checks and 190 hashes.
User closed RPCS3; dry-run then approved install verified 186 translated
targets, all 560 disc files, and 16 unchanged saves. Backups and old cache:
work/install_backups/0.6.4_20260913_083736. Installer also backs up/refreshes
the four root metadata files and includes their restoration in rollback.
BLJS10256 registration correctly points to E:/Projects/SRW Z3/game; other
game registration preserved. Build counter 0.6.4. No new release published
or snapshot/ISO requested. Actual-quad offline preview reviewed at
work/support_popup_comparison.png; live user retest pending. The older
pending registration warning below is historical, no longer current.

**0.6.3 PUBLISHED AS LATEST (2026-09-12):**
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.3
Published 2026-09-12 13:36:57 UTC; release id 387581709, not draft/prerelease.
Initial upload was approval-blocked; the user then explicitly approved the
three patch payloads and retro-trans/SRW-Z3 destination. Uploaded to a draft,
verified all three remote sizes/SHA-256 digests plus release-note content,
then published as latest and rechecked the public release. Only patches and
ZIP support files uploaded; no full game/ISO or savedata.
Local packaging retains immutable 0.6.3. Public notes:
docs/RELEASE_0.6.3.md. Patch ZIP: releases/0.6.3_xdelta/
SRW-Z3-English-0.6.3.zip (85,065,423 bytes, all 189 entries CRC/hash checked).
tools/package_release.py packages patches/support files only, dry-run first.
Complete local ISO is an intermediate at work/release_image_0.6.3.iso;
never upload this or the game folder. The runnable folder remains game/.
Packaging is COMPLETE: full ISO delta 149,090,767 bytes, update from 0.6.1
18,859,897 bytes; BOTH decoded and hash-compared successfully. Output ISO
4,996,820,992 bytes, MD5 7936d74e28e5b7259ab6666a967e71a7. Download SHA-256
hashes are recorded in public notes and releases/0.6.3_xdelta/SHA256SUMS.txt.
No active packaging sessions remain. Publication is complete.
Remote master and local HEAD match 69e053705b81304657d528e9b5ee571ddb8ba9bd;
UI/tooling working changes remain uncommitted. Do not include unrelated
working changes in a source commit simply to publish the release.
The release tag targets that existing commit; no local source commit/push
was performed. Local game registration/cache were not changed by publication.

**Single-folder request (2026-09-12):** canonical runnable destination is
E:/Projects/SRW Z3/game (complete PS3_GAME plus PS3_DISC.SFB), not a new ISO.
prepare_testing_game.ps1 assembles existing validated 0.6.3 without incrementing
the version; build_manifest.json, message_coverage.json and folder_audit.json
live beside the disc tree. All future successful installs target this folder.
install_build.ps1 also backs up and switches BLJS10256 in games.yml and checks
the result; preserves other registrations and rolls back on failure. RPCS3
is still running, so the actual registration/cache switch is pending closure.
Preparation completed: all 560 disc files (186 translated build outputs)
copied and SHA-256 verified. Registration helper/syntax tests passed.
Older outputs/backups are intentionally untouched.

**Deployment correction after user test (2026-09-12):** the verified 0.6.3
files were copied to E:/SRWZ3/PS3_GAME, but RPCS3/config/games.yml still maps
BLJS10256 to E:/Projects/SRW Z3/work/patched_0.6.1.iso. The active game entry
therefore remains on the older ISO; the earlier "installed for testing"
claim was incomplete. Installed EFFPS3 hash matches 0.6.3, so this is a boot
target mismatch, not proof of an artwork patch failure. RPCS3 is running;
wait for the user to close it before changing its registration/cache. Preserve
BLJS10299's separate entry and all saves. Verify the actual boot target on
future installations, not just destination file hashes.

**2026-09-12 version 0.6.3 INSTALLED for testing.** User explicitly requested
installation and wants successful future builds installed automatically
(see CLAUDE.md; do not force-close RPCS3 or publish without permission).
install_build.ps1 dry-run then approved -Write deployed all 186 verified
game files to E:/SRWZ3/PS3_GAME. All destination SHA-256 hashes match the
numbered build; all 16 saved-game files remained identical. Old game files
and BLJS10256_DATA cache retained in
work/install_backups/0.6.3_20260912_182937, with install_audit.json.
The cache will rebuild on next launch. ISO/published downloads unchanged.

**2026-09-12 combined build 0.6.3 COMPLETE:** user requested a version containing
all available work. Fresh directory work/build_0.6.3_all, log of same name.
83/116 story scripts +26/26 intermission, not a 100% translation. Explicit
--partial-translation build mode documents/hash-records missing mission
variants; non-mission UI and all present translations still require checks.
Default audit remains strict. Narration checks now use exact 18 source keys,
not [:18]. 132 tests pass. Snapshot releases/0.6.3: 186 game files, verified
hashes; counter and footer stamped0.6.3. CV fields independently checked on
the new build. See RELEASE_0.6.3.md. Initially build-only; subsequently
installed on user request as recorded above. Not published.
Per-file patches finished: releases/0.6.3_xdelta, 186 from-original +122
from0.6.1; every delta decoded and output hash verified.

**2026-09-12 Library CV romanization: LOCAL CANDIDATE PATCHED.**
translation/library_voice_actors.json covers
153 named actors plus placeholder. build_library translates ACTR and pools
its text; library_cv rejects unknown credits. patch_library_cv_candidate.py
is dry-run-first, only patches ACTR using existing VWF cells, and verifies all
non-CV fields. Backup/report: work/library_cv.before.CPK and
work/library_cv_audit.json. Dry-run/write/re-run passed: 408 entries (193
named, 215 placeholders), all other fields identical. Seven tests pass,
including normal builder and candidate replay; widest credit 340px at 32px.
No installation changed; live visual check pending. See docs/LIBRARY_CV.md.

**2026-09-12 two requested build blockers: FIXED; broader build still blocked.**
audit_message_classes.preset_text finds each named preset in the archive
instead of member1. Coverage and role checks share it; STG0068 uses member3.
It rejects missing/ambiguous/unnamed objective sources and preserves strict
dialogue-only exceptions. Actual inventory now completes: 142 archives,
1538 variants, 24 Stage68 whole/numbered variants. It exposes 1034 missing
mission translations; report: work/mission_coverage_after_lookup_fix.json.
Default complete-translation coverage remains strict. For the later explicit
combined partial release, missing mission variants are documented rather than
treated as corrupt build data. Never claim a complete translated game.
issue_hook has one standalone Counterattack entry, with the same wording
in its combined Counterattack/Defend/Evade menu. Removed three stale duplicate
action rows. patch_counterattack_candidate.py dry-run/write synchronized one
combined-menu hook: 57 appended bytes, no removals, 3495 lookup rows; all
other hooks/code/file length unchanged. Backup counterattack_EBOOT.before.bin.
10 new tests + 58 other targeted/regression tests pass (68 total). Focus
replay uses that backup as its historical endpoint and checks current hooks.
The subsequent combined-build work fixes both first18 narration assumptions.
It rebuilds all stage outputs and explicitly records unfinished mission text
for a partial translation package. Installation still requires a coherent,
verified complete file set; the old out_0.6.3 candidate is not such a set.

**2026-09-12 English title logo: CANDIDATE PATCHED, live verification pending.**
User approved scripted cleanup after two RGB imagegen drafts had baked
checkerboards. clean_title_logo.py extracts wordmark/subtitle from saved v2;
work/title_logo_final contains reviewed real-alpha PNGs and dark/light preview.
title_logo.py applies only these two sprites in EFFPS3 member296 texture1,
1024x720 linear ARGB. Actual UVs: (0,0,706,296), (0,603,339,117), with 1706
and 1657 references. Native Z frame/fire rectangles remain byte-identical.
Normal location_caption build and check_issue_fixes audit compose this after
Library/footer. Required work assets are hash-guarded; retain the draft and
final PNGs locally (ignored; no extracted game data committed).
patch_title_logo_candidate.py dry-run/write updated local out_0.6.3/EFFPS3.CPK,
preserving all 333 other stored member payloads. Backup title_logo.before.member;
title_logo_patch_audit.json records before/after hashes. 18 title tests pass.
Packed atlas: work/out_0.6.3/title_logo_atlas.png. Prompt: title_logo_draft/PROMPT.md.
No stamp/release/ISO/deploy. See docs/TITLE_LOGO.md for rebuild and rollback.

**2026-09-11 Focus/Foc standardization: CANDIDATE PATCHED.**
User settled 気力 = Focus, compact Foc (BASE_RULES updated). All active UI,
part/skill/mech/Spirit descriptions/status effects now use Focus; Weapon Info
Req. Focus; five skill names Foc+ Dmg/Evd/KO/Hit and Foc Bonus. Ordinary
dialogue morale and the Focus/Focus+ Spirit names are unchanged. Two Ace
tutorial barks in voice_121 also changed. Sources and generators updated;
37 part and 59 skill descriptions rewrapped within existing limits.
standardize_focus.py --snapshot saved focus_hooks_before.json and source
baselines; then preview/write. patch_focus_candidate.py dry-run/write:
163 hook replacements, no removals,15562 new text bytes,3495 lookup rows;
five exact RPW j-string name replacements padded in their existing slots;
two exact SRVC strings shortened/NUL-padded, offsets/block table unchanged.
Backups work/focus_EBOOT.before.bin, focus_RPW.before.bin, focus_SRVC.before.bin.
No executable code or RPW description changes. AID rebuilt (same size).
All 40 targeted/regression tests pass; test_focus_terminology.py adds six
source/binary replay checks. Gift replay
test now uses the pre-Focus endpoint; current gift hooks checked independently.
No release/stamp/ISO/deployment changes. In-game confirmation still pending.

**2026-09-11 Counter / stage GIFT report family: CANDIDATE PATCHED.**
gift_reports.py covers every nonempty MESSAGE in extracted preset GIFT tables:
22 distinct / 87 occurrences, including 3 Scopedog conversion reports in 5
stages, part/fund awards, AG bonuses, feature unlocks and upgrade refunds.
translation/gift_report_hook.json: 39 exact whole/line entries; line_pairs:false;
glossary markers and parts.json spellings; <=1000px per line at 28px.
president_report_layout additionally whitelists 18 single-line report keys,
looks up English dynamically and measures live advance. Existing AG pad
lines and every unrelated call retain their previous paths. Wrapper code
924 bytes, data 858 bytes, original cave boundaries unchanged.
patch_gift_candidate.py snapshot/dry-run/write added 30 hooks, no removals,
3760 text bytes; total lookup rows3495. Backup gift_reports_EBOOT.before.bin;
baselines gift_hooks_before.json and gift_center_before.json. Future batches
must preserve this wrapper and replay skill tests against the pre-gift backup.
Counter already existed in the packed map atlas; confirmed it and CMN sibling
labels. trader_art adds Map/Wpn/Song to finish texture2's first three word
rows. AID rebuilt: 41 members,14242708 bytes. Candidate atlas visually checked.
34 targeted tests pass (252 emitted-PPC center/register cases included).
check_issue_fixes has a new wrapper check. Its earlier conflicting issue_hook
duplicate (・反撃する) was fixed on 2026-09-12; see the current blockers above.
No ISO/deployment/stamping/release. Live UI verification pending.
Details: docs/GIFT_REPORTS.md. Ignore work/inventory_gift_messages.py and
work/inspect_unlock_counter.py as temporary read-only source/atlas helpers.

**2026-09-11 Pilot-skill descriptions: CANDIDATE PATCHED.**
All 68 sk-pri records / 124 distinct column-4/5 strings reviewed against
Akurasu Pilot Abilities. tools/skill_description_catalog.py is the new prose
source; build_skill_descriptions.py generates translation/skill_hook.json
(<=3 lines / 740px at 28px, current skill/Spirit names). Half Cut clearer;
Support Attack bonus now per available support use. Feral follows wiki +30%
crit vs JP help +20%; variant-only Gravity 1 Air A and Reversal 2 +50% retained.
See docs/PILOT_SKILL_DESCRIPTIONS.md for all discrepancies/unknowns. No names,
prices, gameplay behavior or RPW descriptions changed.
skill_hook now line_pairs:false. patch_skill_candidate.py updated candidate
EBOOT only: 124 replacements, 181 obsolete fragments removed, 9673 appended
text bytes, 3465 total lookup entries. Code/voice data/file size preserved.
Backup work/skill_descriptions_EBOOT.before.bin, baseline skill_hooks_before.json.
Six skill + six parts + three weapon-requirements + three President tests pass.
Parts test now replays its own historical endpoint (skill pre-edit backup),
then checks the currently installed part strings independently.
No ISO/deployment/release/stamp changes. In-game appearance/behavior not tested.

**2026-09-11 Weapon-use requirements warning: CANDIDATE PATCHED.**
tools/weapon_requirements.py: 14 AID member-0 widgets. Individual failure
labels a9a14..a9ad4; dim lists bfc14/bfc34 and Max Break sibling bfc54;
post-move property blocks 9cd34/b89d4; header aa354 with orange accent aa374.
English header: The following requirements are not met. Both header layers
use measured left edges with only the center flag cleared; color/style and
all other metadata preserved. Individual label states and dim list styles
unchanged; bullet/dash placeholders and line counts retained.
build_ui/check_issue_fixes integrated, work/out_0.6.3/AIDDATAPACK.CPK rebuilt
(41 members, 14242708 bytes). test_weapon_requirements.py 3 pass, Weapon Info
3 and Power-part 6 regressions pass. No EBOOT/RPW/font/gameplay edits, no ISO,
deployment or stamp changes. In-game appearance still needs confirmation.

**2026-09-11 Power-part descriptions: CANDIDATE PATCHED.**
Reviewed all 69 Akurasu parts and all 300 RPW description variants; 299 English
variants changed. tools/parts_description_catalog.py is now the reviewed
prose source. build_parts_descriptions.py generates the legacy-named
translation/parts_descriptions.unshipped.json and parts_desc_hook.json with
the candidate glyph metrics (<=3 lines, <=540px at 28px). Part names unchanged;
Spirit names read from spirits.json. MAP/range-1 exclusions, Auto-Defenser,
missing-HP formula, all Miracle Fragment effects, and other unclear mechanics
corrected. Wiki second-turn F Bomber wins over JP first-turn wording; see
docs/PARTS_DESCRIPTIONS.md for details and retained JP qualifications.
eboot.load_ui_hook supports per-file line_pairs:false; only this file uses it,
because arbitrary rewrapped prose must not produce mismatched JP fragments.
patch_parts_candidate.py dry-run then --write updated work/out_0.6.3/EBOOT.BIN:
299 replacements, 207 obsolete fragments removed, 17534 new text bytes, 3646
lookup entries. Backup work/parts_descriptions_EBOOT.before.bin and effective
baseline work/parts_hooks_before.json. Every byte outside lookup table/new
text preserved; no RPW edits. Six tests + three President regressions pass.
Not live-render verified or deployed; no ISO or build stamp changes.

**2026-09-11 Upgrade / Library blank buttons / Support Def: CANDIDATE PATCHED.**
upgrade_list_labels.py: Weapon Rank at afd74/b48b4, Sight + Wpn Rank at
af594/b31b4; suppress af5b4/b31d4 separate RANK text. Complete exact-source
inventory verified; only six string pointers change, values/bars untouched.
battle_preview_layout now includes b0ef4 S. Def and b0ed4 Re-Atk, in addition
to b0eb4 S. Atk. Earlier fix missed the defense/re-attack siblings. Three
titles checked at the actual 23px quad against a 96px counter-origin gap.
intermission_layout removes LIBRARY from LIVE_CENTERED: no leading blank
pad, no forced 0x40 flag on the source 0x01 special text mode. All six title
widgets retain plain nonzero-width English glyphs with existing measured
left-edge placement; other popups/PS Store/help descriptions stay unchanged.
This corrects the suspicious mode/prefix introduced by our previous patch;
it is not yet a live-render confirmation of the blank-button root cause.
No pad-bank IDs or font cells removed (other menus may still depend on them).
Normal build_ui/check_issue_fixes integration and candidate AID rebuild done.
test_upgrade_library_support.py 3 pass; deployment-menu 4 regressions pass.
No EBOOT, source game, ISO, deployment or build stamp changes. Verify Library
button visibility and Support Def counter in-game after the next valid build.

**2026-09-11 Barrier / deployment screenshots: CANDIDATE PATCHED; FACTION COVERAGE PARTIAL.**
trader_art adds AID member1 texture0 cells: Shield Def. (0,24,128,48), Parry
(0,48,88,72), Dbl Img (88,48,136,72), Barrier (0,72,64,96). Source/candidate
atlas inspected and work/defensive_words_preview.png visually reviewed;
the game supplies the yellow color and shadow. Surrounding MAX/etc intact.
deployment_menu_text.py translates 7 static help widgets (ac894/ac8b4/ac8d4/
ac8f4/acb74/acb94/acbf4), including all exact duplicate source variants.
Stats: aba94/ac014 SR Points/Teams, ab9d4 SR Points/Turns; abab4/ac034/ab9f4
Z Chips/Funds. Suppresses only abad4/ac054 隊 suffixes. Twelve colon widgets
aligned at native x=174 (left panels), 1166 (right); counters not rewritten.
Integrated build_ui/check_issue_fixes; normal candidate AID rebuild completed.
test_deployment_menu_text.py: 4 tests cover inventory, packed layout/byte
isolation, defensive sprite pixels and exact Robot Mafia hook presence.
Robot Mafia: appended one screenshot-derived exact match to issue_hook.json;
work/build_robot_mafia_hook.py dry-run then applied, 43 changed bytes only
in appended hook entry/EXT strings. Backup work/robot_mafia_EBOOT.before.bin.
IMPORTANT: exact faction source table not found in EBOOT, original RPW/AID,
all cached stage CPKs, LUACPK, KDATAPS3, OP or MAPATTR. Only dialogue mentions
found. Do not claim all faction names translated or this runtime path proven.
Could require a different rendering/source path; ask for an in-game check
after a future build. No saved names, game deployment, ISO or stamp changed.

**2026-09-11 Mech Info title alignment: PACKED CANDIDATE VERIFIED.**
`mech_info_layout.py` handles both 機体能力 headings at AID member 0
records 0xa0654/0xba014. Source inventory confirms these are the only two.
Measured Mech Info width=152.09375 native pixels at quad=31. New left
x=235.953125 centers at x=312 within text-safe bounds 212..412; original
left positions were 255.5/261.5. Only the two four-byte x fields change.
No title string, font/style, baseline, neighboring tabs or mech data edits.
Integrated build_ui/check_issue_fixes; candidate AIDDATAPACK rebuilt normally.
test_mech_info_layout.py: three tests for inventory, packed byte isolation/
fit and EBOOT hook agreement. Weapon Info and President regression tests
also pass. No live test, source-game/ISO/deployment or build stamp changes.

**2026-09-11 President Clear Report alignment: CANDIDATE PATCHED, NOT LIVE-TESTED.**
`president_report_layout.py` wraps centered drawer VA 0x14954 (displaced
stdu r1,-0xc0) using verified empty executable-gap code at 0x78f000 and
English measurement data at 0x78f800. The original Japanese strings at
0x6f4f30/0x6f4f50 remain intact; exact matching measures their existing
English hook replacements before tail-calling 0x140f4. The third line
accepts only the encoded +, 1..10 fullwidth decimal digits, and exact PP.
suffix. Uses live per-category quad widths and fullwidth digit pitches;
preserves all GPRs, CR, LR and all FPRs except the intended x in f1.
Unrelated/malformed/non-CP932 text takes the original centered prologue.
No report constructor, amount, font, pointer table or SRVC edits. Legacy
AID President templates are not the runtime constructor and were not moved.
Normal eboot.patch and battle_reports.check_elf now integrate it. Tests:
test_president_report_layout.py, 3 passed, 180 emitted-machine-code cases.
work/build_president_alignment.py was dry-run then applied to candidate
EBOOT: 674 changed bytes within 879 allowed bytes; every other byte identical.
Backup: work/president_alignment_EBOOT.before.bin. No ISO/deploy/stamp change;
out_0.6.3 remains an unstamped candidate subject to the full-build gate below.

**2026-09-11 Combat Record links/help: PACKED CANDIDATE VERIFIED.**
`combat_record_links.py` handles all 12 navigation widgets: four consecutive
records at each base 0xa79b4, 0xbdd54, 0xbde94. Labels: To 'Pilot TOP 5',
To 'Lecture Plates', To 'Trade List', To 'Z Crystal Status'. Suppresses only
the 人 suffix widgets 0xa7f34/0xa81d4, not Ace Pilot counts. Exact source
inventory, widget metadata preservation and fit checked. build_ui and
check_issue_fixes integrate the patch. Four help messages at original EBOOT
0x6d71f8/0x6d7230/0x6d7268/0x6d72a0 are added to ui_utf8.json (Open ...).
Candidate AID rebuilt normally. One-off work/build_combat_record_help.py
updated only the four original UTF-8 help slots; all other EBOOT bytes
preserved, backup work/combat_record_EBOOT.before.bin. Three tests in
test_combat_record_links.py pass. No runtime/ISO/deployment/release changes;
candidate is still unstamped and subject to the full-build blocker below.

**2026-09-11 Weapon Info title alignment: PACKED CANDIDATE VERIFIED.**
`weapon_info_layout.py` changes only x positions at AID member 0 records
0xa0674 and 0xba094 (both source occurrences of 武器性能). Existing Weapon Info
runtime translation is 190.84375 px at 31 px glyph width. The tab screenshot
spans roughly native x=280..520; title is centered at x=400 with conservative
text bounds 300..500. New start x=304.578125, replacing x=339.5/346.5.
Only two four-byte position fields change: baseline, font/style, strings,
U/P/R tabs, column headings, values and weapon rows remain untouched.
Integrated into build_ui and check_issue_fixes; rebuilt candidate AID.
Three tests in test_weapon_info_layout.py pass (source inventory, byte
isolation/packed fit, actual EBOOT translation matches measured string).
No live emulator check, source game, ISO, deployment or build stamp change.

**2026-09-11 Support popup / search-list columns: PACKED CANDIDATE VERIFIED.**
`search_list_headers.py` patches seven exact widget records: Uses at 0xad154;
SP Cost at 0xad194/0xad394; suppresses only their old suffix SP widgets
0xad1b4/0xad3b4; +Eff. at 0xad1f4/0xad3f4. Current/max SP columns, dynamic
plus markers, positions, colors and sorting stay unchanged. Source inventory
confirms both cost/+effect variants and the sole Uses heading. Integrated
into build_ui and check_issue_fixes. `trader_art` adds Defend (texture 2,
144,88,72,40), Re- (216,88,40,40), Counter (320,40,192,48); this fixes the
mixed-language Support 防御 map popup, distinct from the CMN animation banner.
Three tests in test_search_list_headers.py pass and assembled sprite preview
was reviewed. Candidate AID rebuilt; no EBOOT/font, source game, ISO, cache,
save, release or build counter changed. Not deployed; full-build gate remains.

**2026-09-11 battle-action category sweep: PACKED CANDIDATE VERIFIED, NOT DEPLOYED.**
See `docs/BATTLE_ACTION_FAMILY.md`. Native CMN member 0 textures 6/10/11 now
cover nine additional battle action surfaces, composed with Maximum Break.
Six menu variants plus Center/Wide and standalone Assist are handled in
tag_reward_layout.ACTION_ROWS. Eight dynamic action labels are in issue_hook;
four UTF-8 warnings at 0x6d66f8..0x6d6780 are in ui_utf8. Four new tests pass.
Candidate AID and CMN rebuilt normally; EBOOT incrementally patched using
`work/build_battle_action_eboot.py` (last correction used --actions-only),
with byte-isolation assertions and unchanged font mapping. The committed
JSONs are integrated automatically by the normal full build. Candidate-only
EBOOT backup: work/battle_actions_EBOOT.before.bin. No voice offsets, saves,
emulator/cache, source game, ISO, build stamp or release changed. Counter
remains 0.6.2; do not bypass the existing full-build audit blocker below.

**2026-09-11 map-menu screenshots: PACKED CANDIDATE VERIFIED; NOT DEPLOYED.**
`tag_reward_layout.HEADERS` adds four separately centered headings at
0xa9194/0xa91d4/0xa91f4/0xa9214 (Transform, Spirit Commands, Element Change,
Power Parts). Adjacent Search Settings is already owned by naming_search_layout.
`trader_art` now translates texture-2 Armor and Sight cells and clears their
shared 値 suffix (no English equivalent). Arrows, UVs, tint and animation
remain intact. Existing Tag Command list and Spirit clear-marks translations
were confirmed in candidate AID/EBOOT; screenshots alone do not establish
which old files the running game loaded. No new EBOOT patch was necessary.
Rebuilt only candidate AIDDATAPACK.CPK using its existing font mapping.
Three tests in `test_map_ui_screenshots.py` pass, including fixed-length UTF-8
source-copy preservation. Popup asset preview visually reviewed; no live
emulator QA. See `docs/MAP_UI_SCREENSHOTS.md`. Full-build blocker remains below.

**2026-09-11 title Library submenu: IMPLEMENTED, NOT DEPLOYED.**
All five screenshot labels are English in native EFF member 296, texture 5.
See `docs/TITLE_LIBRARY_BUTTONS.md`. The new patch composes with the version
footer; use `title_library_buttons.verify` for the combined member (the
footer-only verifier intentionally rejects additional texture changes).
Five targeted tests pass; all 2,292 animation sample records are preserved.
Packed EFF in `work/out_0.6.3` verified: five labels plus version footer,
all 83 map captions, scenario title companions and untouched member payloads.
All seven existing footer tests also pass (12 targeted tests total).
The STG0068 lookup blocker below was subsequently fixed on 2026-09-12;
missing mission coverage still blocks stamping/shipping the candidate.

**2026-09-11 save alignment + end-session screenshot: BATCH VERIFIED; FULL BUILD BLOCKED.**
See `docs/SAVE_QUIT_FIXES.md`. Six source-line centering pads appended (no old
pad renumbering), isolated left-aligned status widget, seven Kouji/Shiro scene
records in STG0700/t_060, and trophy 022 text in both bundled locales. Five new
targeted tests pass. New outputs are STG0700.SDAT and TROPHY.TRP; all distribution
maps include them. No deployment, trophy progress, saves or emulator touched.
Packed candidate `work/out_0.6.3` passes this batch's checks: 11,520 emitted-PPC
centering cases, 205 dialog hooks, 192 blank pad cells in both built font layers,
seven correctly encoded/fitting dialogue records, SDAT round-trip, and trophy
metadata/checksum. All 83 prior map captions also pass. Full suite: 38/40 pass;
both remaining failures and the full-build failure are the existing STG0068
source audit (lookup fixed 2026-09-12; missing coverage now exposed).
Counter stays 0.6.2. Do not stamp/ship around the remaining gates.
Other end-session scenes (583 speech records) are unchanged, not translated.

**2026-09-11 deployment dialogs + all 83 map captions: IMPLEMENTED; FULL BUILD BLOCKED.**
Current work is local only; no deployment, ISO, release or save modification.
See `docs/DEPLOYMENT_MAP_CAPTIONS.md`. Candidate output `work/out_0.6.3` is
UNSTAMPED and not approved for deployment; successful counter remains 0.6.2.
The first full-build attempt stopped safely because the extended VWF helper
exceeded its 256-byte slot. Its 264 bytes now end at 0x78c308; first keyword
helper moved to verified pristine padding at 0x78c310 (68 bytes, next helper
0x78c400). Original safety assertion retained; padding/non-overlap unit test
added. Confirmation-tab checker now reads the actual stub length, not 256 bytes.
Eight targeted tests and all 83 caption before/after previews pass. Full suite:
33/35 pass; both failures are the existing source-message audit rejecting
STG0068 because it assumes its mission preset is member 1 (it is member 3;
member 1 is stage_require.lua). This source is outside the registered build
manifest, but the audit scans all extracted stage archives. The integrated
build reaches the same audit failure. Do not bypass that gate or stamp output.
The named-preset lookup was fixed/inventoried on 2026-09-12 (see top entry),
exposing 1034 missing mission variants; completing those is separate work.
Read-only batch checker: `tools/check_deployment_locations.py --out work/out_0.6.3`;
it checks deployment/map assets without claiming full-build approval.
This batch check PASSED against the packed output, including all 83 captions
and byte-identical non-caption regions/undeclared member payloads.

**2026-09-10 title footer: BUILD 0.6.2 VERIFIED; NOT DEPLOYED OR PUBLISHED.**
User requested the version and `github.com/retro-trans` in the lower-right
of the press-any-button title screen. Added `tools/title_footer.py`; automatic
version follows the successful-build counter. Output: `work/out_0.6.2`.
Current counter **0.6.2**, next successful build **0.6.3**. Public latest
remains 0.6.1. No installed game/emulator/save state was changed.
Actual source: EFFPS3.CPK member 296 (ScAnime_Z3TITLE 295 plus shared member),
texture 0 at GTF 0x1fe290. Only bottom-right pixels change; logo, prompt,
animation commands and the other 333 archive-member payloads are identical.
See `docs/TITLE_FOOTER.md` for location, layout and version-transaction details.
All 136 output hashes verified. EBOOT/font mappings are identical to 0.6.1;
all 58 plaintext stage archives are byte-identical (SDAT ciphertext varies).
Full UI/PPC regression passed; all 27 unit tests passed. Footer verification
ran both before packing and against the built archive. Preview:
`work/out_0.6.2/title_footer_corner.png` (extracted asset, not a live screenshot).
Live RPCS3 visual confirmation remains pending. Source edits are uncommitted.

**2026-09-10 release 0.6.1: PUBLISHED AS LATEST; NOT DEPLOYED LOCALLY.**
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.1
Published 2026-09-10 07:15:27 UTC. Tag points to aab12e3; all three uploaded
asset sizes and SHA-256 digests match local verified packages. Not a draft
or prerelease. The next build at publication was 0.6.2 (now built above).
work/out_0.6.1 combines stages 1–30, 26 intermissions and all pending UI/terrain
fixes. Full regression passed, including 10740 PPC centering cases, 3830 hooks,
179 pads and all 504 source message variants across 58 archives. Independently
resolved roles: 84 victory, 116 defeat, 78 SR entries. Serpent/Kshatriya use
objective wording. New tools/mission_conditions.py and reviewed JSON expand
numbering, displayed Hibiki and Lua-escaped point-label variants.
Snapshot: releases/0.6.1 (133 game files), releases/0.6.1.json (hashes only).
Successful builds auto-increment; counter at publication was 0.6.1.
Failed builds do not consume a number. Snapshotting preserves the number and
verifies all build-manifest hashes. Tests: tools/test_build_version.py, 12 pass.
Packaging logs: work/release_patch_0.6.1.log and work/iso_patch_0.6.1.log.
Installer layout now matches all 133 release files; update patches include
newly translated files using pristine sources. Both ISO deltas decode-verified:
full 136623568 bytes; update from 0.6.0 7130945 bytes; ZIP 45021191 bytes.
133 original-file and 132 previous-file deltas decode-verified. ZIP CRC and
all 136 entry hashes checked. Five additional mission-context/negative tests
pass. ISO MD5: 2e8e5dbe6fa92c3f5abdb286da3cd80c (4935067648 bytes).
Release notes: docs/RELEASE_0.6.1.md; target GitHub tag v0.6.1.
Pristine ISO is verified at
E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso;
MD5 2cfedd95e5bdde49550cffa21c3c29a3, 4,431,872,000 bytes. Use --iso explicitly.
GitHub authentication works as binhlt0402 with repository write access when
run outside the restricted environment (required for Windows credentials).
No game/install/save writes. Runtime visual confirmation remains pending.

**2026-09-10 the long run to finish every stage: IN PROGRESS, RESUMABLE.**
Goal: translate every remaining stage script. 32 of 116 story scripts were
done when this started (stages 1-30 plus both route splits) along with all 26
intermissions; 84 story scripts and 11 non-story ones remain. This is many
sessions of work, so it is built to survive one ending mid-flight: every
stage is committed the moment it merges clean, and progress is DERIVED, never
remembered. Start any session with:

    python tools/stage_status.py           # what is done, what is next
    python tools/stage_status.py --all     # every script, one line each

The four steps, each a tool so nothing is hand-run:

    python tools/prep_stage.py STG0031A ..     # decrypt + unpack + count
    python tools/brief_stage.py STG0031A ..    # cut briefs, mark done slices
    (one Sonnet subagent per brief -- see below)
    python tools/merge_stage.py <member.lua> translation/stage0031a_03.json \
        work/tr/STG0031A/answer/m3_*.json
    python tools/check_stage.py <member.lua> translation/stage0031a_03.json
    python tools/register_stage.py STG0031A    # manifest + the 3 deploy tables

`prep_stage` closes RPCS3 (single-instance) to use its decryptor; the user has
standing authorisation for that. `brief_stage` writes
`work/tr/<stage>/brief/m<member>_<a>_<b>.md` and points each brief's answer at
`work/tr/<stage>/answer/<same stem>.json`, so a slice already answered is
visible at a glance and a re-run never destroys one. `register_stage` refuses
a stage whose translation file holds no English, and is a no-op if the stage
is already in all four tables.

Brief every subagent with `BASE_RULES.md`, then
`work/tr/CONVENTIONS.md` (the settled decisions -- glossary tokens, nine-dot
ellipsis, banner shape, no em dash, AG in sentence case), then its own slice
file, and require it to run `check_stage.py` on its own answer before
reporting. Slices are 120 records; about 100k Sonnet tokens each. Answers
under `work/tr/` are NOT committed (work/ is ignored); the committed artefact
is `translation/stage*.json`, so merge and commit rather than leaving answers
sitting in work/.

**2026-09-10 glossary tokens across stages 11-30: COMMITTED, BUILD VERIFIED,
NOT DEPLOYED.** Commits bc510c4 (10,504 records in 83 files) and 600006f
(docs). Every stage record whose Japanese names a glossary term now writes
`$$japanese$$` instead of the English; the audit that opened at 14,049 literal
references closes at 23, all deliberate. Nothing on screen moved and that is
proven, not assumed: 13,709 records compared against the previous commit with
BOTH sides expanded (0 differ), `terms.py check` clean on 23,846 references,
and a full `build_project.py` run to `work/out_tok3` in the clean worktree,
exit 0. Nothing was deployed and no installed build changed.

How the conversion decided, because the next one should decide the same way:
a term is a candidate only when its JAPANESE occurs in that record's `jp`, and
the rewrite is kept only when expanding it reproduces the old English
character for character. Japanese-side matching is what makes two-letter names
safe (`AG` 399 records, `PS` 40, `Fa` 21, `UN`, `An` -- the English alone
cannot tell the pilot 安 from the article) and what resolves the five names a
pilot shares with its machine: `ボン太くん` and `ブラックオックス` take
`#pilot` on the speaker line and `#robot` in prose, `宇宙魔王` and `マーグ`
are `#pilot` throughout, `オルソン` is `#50` as the library entry for Kei
already had it.

**The round trip cannot tell you the TERM is right, only that the TEXT is
unchanged.** Four records took a token for the wrong term and every one of
them still expanded to exactly what shipped: `姫` is the SRW-original keyword
(the Firebug's Princess), not Unicorn's `姫様` or Klan's `『姫』` -- 21
records; `ゼロ` is Lelouch, not Duo's Wing Zero; `レディ` is Lady Une, not "a
lady"; `ボス` is the Mazinger pilot, not Mao's `姐さん` (that one was
committed in an earlier batch). All four are literal English again. Before
converting a term whose English is an ordinary word, or whose glossary
`status` is `ambiguous`, read its contexts -- `docs/TRANSLATING.md`
"Migrating literal prose" now says so. A literal is honest; a wrong token is a
rename waiting to corrupt a line.

`translation/vi` is untouched by design (Vietnamese prose should reference
Vietnamese terms; the glossary has no `vi` field). The one-time scripts live in
the session scratchpad, not the repo: `tools/tokenise.py` remains the
supported tool, and it matches on the English only.

**2026-09-09 all terrain labels: LATEST PREPARED BUILD, NOT DEPLOYED.**
Output: work/out_all_terrain_20260909, extending out_message_classes_20260909.
Installed remains out_tag_reward_20260908_v2; no game/emulator/save writes.
See docs/TERRAIN_AUDIT.md. All 64 available ZLD maps / 552 records / 78 names
are inventoried, including later maps. 73 new terrain-only keys avoid
overriding existing non-terrain Sea, Forest, Axis and Kurogane-ya entries.
Prepared maps change only bounded name fields; parameters/grids are intact.
Pristine snapshots: work/orig/MAPATTR (never overwrite with translated maps).
New modules: tools/terrain_catalog.py, translation/terrain_all_hook.json.
terrain_labels.check now checks full coverage/widths; check_maps verifies
all prepared bytes. command_layout appends 73 pads without moving old indices.
Blank cell ranges: 87f0..87fa and 84bf..84fc; Unicode 270..2b8. The helper
and VWF dispatcher handle the new bank. VWF is 248B within its 256B slot.
New string allocation: EXT+84000..849d8; 46632 bytes remain. 3585 hooks total.
Builder: work/github_issues/build_all_terrain_20260909.py (dry-run default).
IMPORTANT: deploy.LAYOUT now includes all 64 MAP_*.ZLD files; latest manifest
has 95 entries (92 game files plus 3 metadata). Do not deploy EBOOT alone or
use older ad-hoc 28-file deployment scripts. Legacy builds without maps fail
the normal deploy completeness check. Normal build_project prepares maps too.
Full regression, 10740 PPC centering cases, compilation, negative coverage
test and all hashes passed. Other 27 old game files are unchanged; installed
map hashes are unchanged. Runtime visual confirmation remains pending.
EBOOT SHA256: 4d797bdc270d93bcc3e2094db682f9b8fd5c1cf9b02750a0f28a709e2cdf391b.

**2026-09-09 source-driven message-class audit: PREPARED BUILD, NOT DEPLOYED.**
Output: work/out_message_classes_20260909, extending out_hibiki_conditions_20260909.
Require build_manifest.json before use. Installed remains out_tag_reward_20260908_v2.
No installed game/emulator/save writes. See docs/MESSAGE_CLASS_AUDIT.md for
scope, source coverage, limitations and commands. Source inventory covers
259 exact variants across 17 stage archives and EBOOT effect/unlock/reward
tables, plus three shared reward formats. Adds 154 binary hooks; no existing
lookup entries changed. Two shared reward formats preserve inserted names/items.
New sources: translation/message_class_hook.json, translation/unlock_shop_hook.json,
tools/audit_message_classes.py, tools/message_class_formats.py; both checks
are integrated into check_issue_fixes.py. Fresh eboot.patch calls the format patch.
eboot.EXT_SIZE is now 90000; only the last read-only LOAD segment is expanded.
New strings occupy EXT+80000..83f9e, leaving 49250 bytes. Hook count 3512.
Builder: work/github_issues/build_message_classes_20260909.py (dry-run default).
Other 27 game files are identical to the parent. Runtime visual QA is pending.
Full regression, width checks, compilation and all 31 manifest hashes passed.
The coverage guard also rejected an intentionally omitted effect translation.
EBOOT SHA256: 1d88be104a8b0f5a5d12df8e6ffcfe04e75a67b2f420efb38ca876445e5c0195.

**2026-09-09 Hibiki defeat conditions: PREPARED BUILD, NOT DEPLOYED.**
Output: work/out_hibiki_conditions_20260909, extending out_unlock_reports_20260909.
Require its build_manifest.json before use. Installed remains
out_tag_reward_20260908_v2; no game/emulator/save writes.
The screenshots show ヒビキの撃墜。 but the old single-pilot hooks match
ヒビキＡの撃墜。. Four exact hooks in translation/issue_hook.json now cover
the displayed name, unnumbered and numbered 1/2/3. Existing name variants
remain intact. Episode 4 reads "2. Hibiki is shot down." and Episode 5 reads
"1. Hibiki is shot down.". No stage data or gameplay conditions are changed.
Builder: work/github_issues/build_hibiki_conditions_20260909.py.
Only four hook-table rows and new strings at EXT+7fc00 are changed in EBOOT;
the other 27 game files remain identical to the previous pending build.
check_issue_fixes.py checks all eight old/new name variants and text widths.
In-game visual confirmation remains pending; this build is not deployed.
Full regression, source compilation and all 31 manifest hashes passed.
3358 binary hook entries; new tail allocation ends at EXT+7fd06 (exclusive).
EBOOT SHA256: 4dcd7855a334fd5024d39392659b18d2c40c779d8a6e587063e834df74330d6a.

**2026-09-09 unlock notices: PREPARED BUILD, NOT DEPLOYED.**
Output: work/out_unlock_reports_20260909, extending the pending
out_battle_reports_20260909_v2. Require build_manifest.json before use.
Installed remains out_tag_reward_20260908_v2; no game/emulator/save writes.
Two exact completed-condition hooks translate Clear Stage 4 and an ally's
HP falling to 20% or below. The underlying source strings at ELF 70d710 and
70d7d0 are checked and left unchanged; unlocking logic is not touched.
The shared availability constructor now inserts "Now at D-Trader: " before
the runtime item name and "." after it. Only the two verified TOC pointers
at file offsets 7cb71c/7cb720 are repointed; their original Japanese strings
at VAs 71e530/71e548 and the middle item-name field remain untouched.
This covers Worldbreaker Crest, Crest of Rebirth and Auto-Defenser without
hardcoding a different item into the notice, and applies to other items too.

Source: tools/unlock_reports.py, translation/unlock_report_hook.json;
integrated into eboot.patch and check_issue_fixes.py. Builder:
work/github_issues/build_unlock_reports_20260909.py. Only EBOOT differs from
the previous pending output; other 27 game files are identical. New tail
allocation starts at EXT+7fb00; last nonzero byte is EXT+7fbfd. The EXT segment
ends at +80000: future additions must check capacity, not assume unlimited room.
Runtime visual confirmation remains pending; nothing has been deployed.
Full regression, source compilation and all manifest hashes passed.
EBOOT SHA256: 8d9f69c32d74b10e3d66215725519a8a3bbce7a045eb6185c6d484a6e1847969.

**2026-09-09 battle/report screenshot batch: PREPARED, NOT DEPLOYED.**
Latest candidate: work/out_battle_reports_20260909_v2. Based on the pending
out_weapon_effects_20260909; require build_manifest.json before use.
Installed remains out_tag_reward_20260908_v2. No game/save/emulator writes.
The unsuffixed out_battle_reports_20260909 is superseded: its Break sprite
left a sliver of Japanese at x304..320. Do not deploy that preliminary build.

trader_art.py extends the existing deterministic PS3-font atlas generator:
texture 2 Maximum (0,40,176,88), Break (176,40,320,88), Mobi (56,192,112,224)
and lity (56,320,88,352). Two Mobility pieces align inward to join correctly;
the separate down-arrow, colors supplied at runtime, other word sprites,
portraits and UV descriptors are unchanged. AID member 1 is still verified
against the exact allowed atlas rectangles. No AI-generated artwork used.
Tag Command options and Z Chips were already covered by tag_reward_layout;
this batch adds all four UTF-8 help descriptions and the CP932 help heading.
The President report's two fixed lines use exact draw-time hooks; its
CP932 format at original ELF offset 6e4f68 becomes +%s PP. with the literal
ASCII %s preserved, so 5/10/50/100 and other runtime amounts are not hardcoded.
battle_reports.py checks that placeholder and unchanged amounts; eboot.patch
calls patch_format for fresh builds. Three repair title variants, Cost and
Funds use six scoped FSSA records; row coordinates and costs stay intact.

Builder: work/github_issues/build_battle_reports_20260909.py. Owns only new
EXT+7f800 hook/helper strings, verified UTF-8 source slots/data referents,
the bounded PP format slot, six FSSA pointers and four new word rectangles.
The other 26 game files remain identical to the previous pending build.
Preview: work/out_battle_reports_20260909_v2/battle_word_preview.png.
Runtime visual confirmation is still required; nothing has been deployed.
Full regression and compilation passed; all manifest hashes verified.
The revised atlas preview was visually reviewed (no leftover Break fragment).
EBOOT SHA256: cbcf6b9d313405d06c8f0fefe25534bb955fde6cbab30b4d2767fe5883363214.
AID SHA256: 716ebe11a1bb5389ca6b1fc0b25950c4f7d2a189dfda2b73fffc357f1b17edf0.

**2026-09-09 weapon Effect labels: NEW PREPARED BUILD, NOT DEPLOYED.**
Latest output: work/out_weapon_effects_20260909, extending the pending
out_ui_followup_20260908_v2. Require build_manifest.json before using it.
Installed remains out_tag_reward_20260908_v2; no emulator/game/save writes.
User specifically reported the Effect values in screenshots 2 and 3:
運動性▼ -> Mobility Down; バリア貫通 -> Barrier Pierce.
translation/weapon_effect_hook.json supplies exact draw-time matches and is
registered in eboot.UI_HOOK_FILES for fresh builds. No effect flags, stats,
original Japanese tables or artwork change. weapon_effect_labels.py checks
original ELF offsets 6d5580 / 711588, unchanged source table bytes and a
300px width budget at 31px text. The usual complete hook-table checker
verifies both emitted entries. No additional centering or font pads needed.
Builder: work/github_issues/build_weapon_effects_20260909.py; two new hook
keys/values occupy verified-empty EXT+7f700; all earlier hooks preserved.
Only EBOOT.BIN differs from the previous pending build; the other 27 game
files are byte-identical. Screenshot 1's deployment confirmation text was
not changed in this narrowly scoped Effect-label task.
Full regression, source compilation and all 31 manifest hashes passed.
EBOOT SHA256: f8119bc560ad5d19e2107ebadbb8b03f0ce49dfb1f2a3a4f51ad367ce419484a.
In-game visual confirmation is pending; this output has not been deployed.

**2026-09-08 nine-screenshot follow-up: PREPARED, NOT DEPLOYED.**
New output: work/out_ui_followup_20260908_v2, based on the installed
out_tag_reward_20260908_v2. Require its build_manifest.json before use.
Current installed files remain the tag_reward_v2 bundle below. Never stop
RPCS3 or deploy this follow-up without the user's request.

The new screenshots demonstrate that earlier static FSSA x/font changes
were insufficient in several runtime-composed menus. Library labels and
PS Store now use live-pitch padding with the center anchor restored, instead
of a second static subtraction of English ink width. Six English pads plus
the Cliff hook append at indices 99..105 (SJIS 87e9..87ef, Unicode 269..26f).
Keep all earlier pad indices stable. All 106 font cells were already blank
in both shipped atlas layers, so TPACKPS3 stays byte-identical.
ELF metadata extends the existing table; Cliff's key/value occupy only the
audited empty EXT+7f600 tail. MAP_002.ZLD+84 verifies the source Cliff label;
terrain/map/gameplay data are never patched.

intermission_layout.py now uses Teams in title variants, Auto-Update and
Search Setup in Support Command. map_popup_layout.py uses AT/DF, short enough
for the separate unknown counters even at 28px. ui_followup_layout.py adds
two [Upgrades] headings, two Record Library headings, four Team Setup MV
labels and nine stage/turn footer variants (Ep + dynamic number + Clear).
Full-width turn-count slots are retained; an ASCII gap precedes "turns".
All unrelated artwork, dynamic value records and selection colors survive.
Builder: work/github_issues/build_ui_followup_20260908.py. It transplants
only owned records from pristine-scoped renders and audits every changed
byte, verifies unchanged CPK members and the other 26 game files.
Runtime visual QA remains necessary, particularly the Library and split
PS Store runtime anchors; mathematical centering tests are not in-game QA.
The unsuffixed out_ui_followup_20260908 failed the older footer expectation
and is incomplete; never deploy it. The _v2 normalizes the first two footer
variants' older D-Trader offsets so padding is not applied twice.
Full regression passed, including 6,360 emitted-PPC centering cases, 119
dialog hooks, 106 blank font cells and all earlier translation/art checks.
Source compilation passed. A 28-game-file manifest is present.
EBOOT SHA256: 42af9b98db5b526a692c584dee6483f7d321db1b735b8c487ec6cabc03af7721.
AID SHA256: 92a4840334001133f741f159a41bef4b5e3371302c9c288804dde5aa2dcfaa16.

**2026-09-08 deployment completed on explicit user request.**
CURRENT INSTALLED: work/out_tag_reward_20260908_v2 at E:/SRWZ3/PS3_GAME/USRDIR.
All 28 deployed files verified against the build manifest by SHA256. RPCS3
was closed. All eight savedata files hashed identically before/after.
Backup: work/github_issues/before_tag_reward_20260908 contains the previous
EBOOT.BIN, AIDDATAPACK.CPK and CMN.CPK plus deployment.json (before/after hashes).
Stale E:/RPCS3/dev_hdd0/game/BLJS10256_DATA moved into this backup's install_cache
folder (recoverable), not deleted. The next boot can recreate install data.
All earlier pending fixes below are now included in the installed bundle.
In-game visual confirmation is still pending; RPCS3 was not launched.

**2026-09-08 Tag Command / Maximum Break / reward / Weapons: BUILD DETAILS (NOW DEPLOYED).**
Pending output: work/out_tag_reward_20260908_v2, includes all prior pending fixes.
Originally prepared while deployment was deferred; deployment completed above.
Require build_manifest.json. Full regression and source compilation passed.
tag_reward_layout.py changes ten FSSA strings: 9cf94's four Tag Commands,
eight Z Chips captions (abbf4/abc74/abd74/abdf4/abe74/abef4/abf74/abff4),
and a06b4 Weapon Select -> Weapons. Keep original row spacing and values.
Rewards aa794/aa7d4 retain original joined-hook strings and overlay records;
clear their Japanese centering flag and set x to center minus English ink/2.
Measured correction vs old render: +80.0625/+62 native px respectively.
Both rendered English ink centers are -0.5 native px (original box center).
maximum_break_art.py translates CMN member 0 GTF 9de0 texture 16 (1472x176
gold banner) and texture 6 inner badge rectangle (5,164,126,24): MAXIMUM BREAK
and MAX BREAK. Gold palette sampled from original art; PS3 bold italic face.
Texture previews visually checked. All bytes outside these rectangles,
including animation commands, UVs, English ribbon and other badges, preserved.
NEW deployment file: CMN.CPK -> DATA/BTLC. Latest bundle now has 28 game files.
Pristine CMN cached at work/orig/CMN.CPK; member SHA256
1359e4fa6b1adb2ab711a5e7c88960d82d37ae4d927ac9f737fd0e263247e2cc.
extract.py now caches this battle_ui input; build_project/deploy/apply_xdelta
include CMN. Older 27-file builds are incomplete under current deploy layout;
do not blindly re-manifest or deploy them. Back up live CMN before eventual
deployment together with EBOOT and AID. Never stop RPCS3 without permission.
Builder: work/github_issues/build_tag_reward_20260908.py. Preliminary
out_tag_reward_20260908 is superseded; use ONLY the _v2 output.
AID SHA256: 8657dc8b682d0fd4902799213ff895411ffe8a5b6f1e94765ec7cf1e851a5bd1.
CMN SHA256: 9661ef4200280176cd36949c00a56ed4b39d2f640609d7c36b4453abc0ff070d.
EBOOT unchanged: dbea9239914ee88a508afa892074fb8c166e07a634670b69c0db2c9869fb412a.
Other 26 existing game files unchanged from out_map_popup. In-game QA pending.

**2026-09-08 map-popup overlaps: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
Pending output: work/out_map_popup_20260908, includes all prior pending fixes.
Deployment still deferred; installed remains out_narration_layout_20260908.
Require build_manifest.json before use. Eight scoped FSSA widgets only:
ac714 Move -> MV (22px); b9b94 two-row support labels and bb254/bb274/bb2b4/
bb2d4 single-row labels -> S.Atk / S.Def without trailing dots (18px);
ab9b4/ac194 recovery suffix -> Rec: on both rows, keeping separate HP/EN.
Measured widths <=36px, <=50px and <=54px respectively. Preserve all x/y,
line spacing (especially 32px on b9b94), colors/states and unknown values.
No executable changes; only AID differs vs pending team-roster build.
Source: map_popup_layout.py, build_ui.py, check_issue_fixes.py. Audited
builder: work/github_issues/build_map_popup_20260908.py. Visual QA pending.
Full regression passed and manifest written; all eight label edits verified.
AID SHA256: f3c87b63413c320a1cf99354d5cbd92b567484bc8f0a62e4c95406dcc24eb6d9.
EBOOT unchanged: dbea9239914ee88a508afa892074fb8c166e07a634670b69c0db2c9869fb412a.

**2026-09-08 team-roster labels/spacing: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
Pending output: work/out_team_roster_20260908, includes all previous pending
fixes. User deferred deployment; installed remains out_narration_layout_20260908.
Require build_manifest.json before use. Only AID changes versus pending
naming/search build; EBOOT and 25 other game files remain byte-identical.
18 scoped translated widgets: five Team Bonus captions, three Max Break
captions, eight S. Atk / S. Def columns, and two Move labels. Narrow support
headers use 21px glyphs and fit <=63px; original columns are 72px apart.
Move the Ally/Enemy title colon and Unit/Team suffix pieces 28px right in
six variants (12 records); preserve existing faction title and brackets.
Move footer brackets, numeric value and terrain pieces 32px right together
(three records), preserving all text/value/unknown-stat data and styles.
Measured clearance: Enemy List to colon >=10px; Move to value block >=10px;
closing footer bracket remains inside the frame. Artwork unchanged.
Source: team_roster_layout.py, build_ui.py, check_issue_fixes.py. Audited
builder: work/github_issues/build_team_roster_20260908.py. Visual QA pending.
Full regression passed and manifest written: 5940 centering PPC cases,
118 dialog hooks, 99 blank pad cells; 18 text / 15 position-only edits audited.
AID SHA256: 5b0b37e878671fc900551eec50d3451939f39eb090a4a132c3c1e4d196959351.
EBOOT unchanged: dbea9239914ee88a508afa892074fb8c166e07a634670b69c0db2c9869fb412a.

**2026-09-08 naming/search translations: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
Pending combined output: work/out_naming_search_20260908. Deployment is still
deferred; installed game remains out_narration_layout_20260908. Contains all
prior pending fixes. Require build_manifest.json before deploying.
26 scoped FSSA widgets: seven naming descriptions and seven option headings;
search heading; three No Filter templates (: None); eight controller-hint
copies with original LF row counts. Heading positions fit measured widths;
three filter variants retain their templates and use live-width centering.
Three exact CP932 naming reports added for Pilot, Mech, and disabled modes.
Only displayed text changes: automatic-naming logic, custom names, search
settings, icons, colors and selection behavior are untouched.
Helper slots95..98: : None then 3 reports, codes87E5..87E8/U+0265..0268.
Report strings appended at EXT+0x7f400; inspect remaining tail capacity before
any future append. Prior strings ended EXT+0x7f2fd. Source modules:
naming_search_layout.py, naming_hook.json, command_layout.py, eboot.py,
build_ui.py, check_issue_fixes.py, check_command_layout.py. Audit builder:
work/github_issues/build_naming_search_20260908.py. Only EBOOT/AID change;
other 25 game files and all AID art preserved. Visual QA remains pending.
Full regression passed, manifest written: 5940 live-centering PPC cases,
118 dialog hooks, 99 blank pad cells, and 3347 name-hook entries verified.
EBOOT SHA256: dbea9239914ee88a508afa892074fb8c166e07a634670b69c0db2c9869fb412a.
AID SHA256: a2c1b28528b5987e9c1d8da0d80000fb864a4d8df9691832499613ac0e362898.

**2026-09-08 intermission menu translations: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
Pending combined output: work/out_intermission_labels_20260908_v2. User
deferred deployment; installed game is still out_narration_layout_20260908.
Includes every preceding pending fix. Verify build_manifest.json before use.
47 scoped FSSA records: Pilot List / Power Parts headers; System / Library;
Network Upload / Download / PS Store / Bonus Scenarios; Library's five
buttons plus selected-state copy; Team Setup's split captions; six support
commands; Rename Squad and four multiline settings variants. Fixed-size
popup captions are ink-centered with bounded widths. Empty only the old
caption suffix widgets, never counters, icons, or gameplay data. Voice
caption keeps its punctuation within 4px of the fixed playback-icon slot.
Five Library descriptions translated via UTF8 pointers and live centering.
New helper slots90..94, codes87E0..87E4 / U+0260..0264; strings appended at
EXT+0x7f200 (near the extension end: inspect capacity before later additions).
Source: tools/intermission_layout.py, build_ui.py, command_layout.py,
eboot.py, check_issue_fixes.py, translation/ui_utf8.json. Incremental audited
build: work/github_issues/build_intermission_labels_20260908.py.
Earlier out_intermission_labels_20260908 is superseded by v2 because the
Voice punctuation spacing was refined. Do not deploy that earlier candidate.
Only EBOOT/AID change vs pending terrain build; 25 other game files and all
AID artwork preserved. In-game visual confirmation still required.
Full regression passed and manifest written: 5700 centering PPC cases,
95 blank pad cells, all five description pointers and 47 widgets verified.
EBOOT SHA256: e883b99fee2d1f35d40ca3e87eb269d832815ff80fcf1fce9a2c52270178b045.
AID SHA256: e7f19331c7a52f4da057074fed3ebb5c084de040d58dcc04818ba82bd0fe16a6.

**2026-09-08 terrain names: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
Pending combined output: work/out_terrain_labels_20260908. Includes backlog,
roster/settings and all preceding fixes. Installed game remains
out_narration_layout_20260908 because user deferred deployment.
Four exact terrain names: 舗装道路 -> Paved Road, 平地 -> Flatland,
ビル -> Building, 工事区画 -> Construction Site. Actual source is the
per-map DATA/MAPETC/ATTR/MAP_*.ZLD files, not EBOOT/AID. Exact examples
in MAP_011.ZLD at 0x44/0x64/0x84/0x164. Translate at display time; do not
rewrite the 32-byte terrain records or their gameplay attributes.
translation/terrain_hook.json appended to eboot.UI_HOOK_FILES. Four live
post-Japanese-centering pads extend fourth bank at slots86..89, codes
87DC..87DF / U+025C..025F. Terrain index is separate from UTF8 settings
descriptions (which count padded English). Appended key/value data at
EXT+0x7f000, near the end of the extension: check remaining capacity before
any subsequent append. Source tests in terrain_labels.py; incremental audit
work/github_issues/build_terrain_labels_20260908.py. Only EBOOT changes
versus pending roster/settings build; other 26 game files stay identical.
Full regression passed: 5400 live-centering cases, 115 dialog hooks and
90 blank pad cells in both font layers. All 64 map attribute files unchanged.
Manifest written. EBOOT SHA256:
4919ae6d5a1e7c9e6a276bc81b41f0cee75fecafd49fd75259b9aa15f4d56b6c.
In-game visual confirmation is still pending; no deployment performed.

**2026-09-08 roster/settings overlap: PREVIOUS PREPARED BUILD, NOT DEPLOYED.**
User deferred deployment; installed remains out_narration_layout_20260908.
Pending combined build: work/out_roster_settings_20260908, includes backlog
spacing fix. Full regression passed and manifest written. EBOOT SHA256:
a8e84ced037a2d3cdbcc9ffc5796231e230dc69a659f08cc026a9ed1b4a461ea.
AID SHA256: 6f8ff9bcb75122d0cd2fa0a8400b215c17a650f49e5fce62c290e5c7941f5faa.
Eight scoped roster support headings -> S. Atk / S. Def, recentered within
their original 112px Japanese heading footprint; all numbers/checkboxes kept.
Eight System Settings tab variants -> Settings 1 / Settings 2 with live pads.
28 settings descriptions now use live-pitch centering (38 UTF8 pointers);
strings and option semantics unchanged. Unrelated descriptions not modified.
Source: roster_settings_layout.py, settings_descriptions.py, command_layout.py,
eboot.py, build_ui.py, check_issue_fixes.py. digraph.free_pool explicitly
reserves live layout codes to prevent future atlas allocations using them.
Added widget slots 56/57 and fourth bank slots 58..85: CP932 87C0..87DB,
Unicode U+0240..025B. VWF stub 232 bytes; command helper 132 bytes. Previous
Spirit helper's 728 bytes retained exactly. Suite: 5160 live centering cases,
86 blank pad cells in both font layers; all prior regressions passed.
Incremental audit: work/github_issues/build_roster_settings_20260908.py.
Only EBOOT/AID changed versus pending backlog build; other 25 game files and
all AID art members byte-identical. Before deployment compare installed
files to out_narration_layout_20260908, back up EBOOT/AID, and check RPCS3.

**2026-09-08 backlog R1 spacing: PREPARED, DO NOT DEPLOY YET.**
User explicitly deferred closing RPCS3/deployment ("do that later"). Installed
game remains out_narration_layout_20260908 below. Pending candidate:
work/out_backlog_layout_20260908. Shorten the fullwidth plus to ASCII +,
remove the space before its opening parenthesis, add two small spaces after
it to retain the suffix position. Both Prev/Next quote rows affected; R1
icons and all controls unchanged. Source: translation/issue_hook.json,
tools/backlog_layout.py and check_issue_fixes.py. Audit build:
work/github_issues/build_backlog_layout_20260908.py. Only three EBOOT hook
targets plus appended text at EXT+0x7d000; no other game file changes.
Before eventual deployment, recheck RPCS3, installed hashes, back up EBOOT,
and verify candidate build_manifest.json exists (written only after checks).
Full regression passed and manifest written. Candidate EBOOT SHA256:
6e3db2424fbd9828b31d2709bc2fd6818d6a643db89e0a098ddcc9c169788292.

**2026-09-08 narration reflow: CURRENT INSTALLED BUILD.**
`work/out_narration_layout_20260908` deployed to E:/SRWZ3/PS3_GAME/USRDIR;
all 27 copies verified. RPCS3 closed; install cache absent; saves untouched.
All installed baseline files matched out_battle_preview before deployment.
EBOOT backup: work/github_issues/before_narration_layout_20260908/EBOOT.BIN.
EBOOT SHA256: 30bcbe63b629043a641d218cd0d38670b7575f4e5e3f5fe12b0fbc3da08ed466.
AID unchanged: b4731f2225857a2823e181eadfcfedba1ee552cbf5484d9e4b4ae47a2798e3f6.
Reflow nine of the 18 STG0001B narration hooks across existing rows on three
pages (poem, Earth Federation, three months later); every word retained in
the same order. No LF insertion, stage metadata, timing, positions or styles
changed. Earlier width check used library geometry and ignored left margin;
tools/narration_layout.py now checks the actual atlas widths at 32px quads,
225px left margin, 900px general max and tighter per-page budgets. Only nine
hook pointers and appended English at EXT+0x7c000 changed. All other 26 game
files identical; full regression passed. Awaiting in-game visual check.
Audit: work/github_issues/build_narration_layout_20260908.py and predeploy
counterpart. Source reflow in first 18 rows of translation/issue_hook.json.

**2026-09-08 battle-preview overflow: PREVIOUS INSTALLED BUILD.**
`work/out_battle_preview_20260908` deployed to E:/SRWZ3/PS3_GAME/USRDIR;
all 27 copies verified. RPCS3 closed, DATA cache absent, saves untouched.
Baseline 27 files matched out_trader; affected EBOOT/AID backed up under
work/github_issues/before_battle_preview_20260908. Awaiting in-game visual QA.
EBOOT SHA256: a14c5e12416163dc818578e7d69d873e83edf7cbd83668c53da25bad6937b094.
AID SHA256: b4731f2225857a2823e181eadfcfedba1ee552cbf5484d9e4b4ae47a2798e3f6.
Eight scoped FSSA widgets: Attack -> Atk. (two templates), Ammo -> Rnd.,
Support Atk -> S. Atk, and four Start Battle variants with live centering.
Counters/colons, styles/positions and unrelated labels untouched. One appended
command pad (index55, code8876/U+01C6); WIDGET_START separates its English
count coefficient from Japanese post-substitution dialog coefficients.
Full regression passed: 3360 centering cases, 56 blank cells, 3340 hooks.
All other 25 game files, all other AID members and Spirit helper preserved.
Production source: tools/battle_preview_layout.py, command_layout.py,
build_ui.py and check_issue_fixes.py. Incremental audit scripts:
work/github_issues/build_battle_preview_20260908.py and predeploy counterpart.

**2026-09-08 D-Trader/rewards/battle labels: PREVIOUS INSTALLED BUILD.**
`work/out_trader_20260908` deployed to E:/SRWZ3/PS3_GAME/USRDIR; all 27
copies verified. RPCS3 was already closed; the regenerable DATA cache was
absent, so nothing was deleted. Saves untouched. Previous installed 27 files
matched the preceding manifest; EBOOT/AID backups are in
work/github_issues/before_trader_20260908. Awaiting user in-game verification.
EBOOT SHA256: ba362a7c79558989d6218e04559babb83ac2bc7e9696bf9af687e703f38b1022.
AID SHA256: 4b8660f9cd114eff242a56915e0f7cbcf6da980acc40eebec93d0931a5c2f4e1.

Screenshot batch: Buy/Sell, D-Trader page headings/prices/stats/categories,
Maximum Break unlock condition, AG bonus messages (100/200/1000 Z Chips),
Bonus Rewards and Special Investigator. Scoped AT selector widget (FSSA
0x988b4) is distinct from the earlier TPACK support-use badge. Intermission
and Center/Wide/Support Attack use five atlas rectangles, not ordinary text.
Intermission footer is Ep. / Clear; numeric episode value unchanged.
28 scoped FSSA widgets repointed, preserving LF row separators and unknown
item masks; stat Accuracy shortened to Acc. for its 120px column. Confirm
hint shortened to OK here to avoid the next controller icon. Source modules:
trader_ui.py/trader_art.py, translation/trader_hook.json, build_ui.py, eboot.py.
command_layout adds five centered AG-message pads AFTER the existing 50;
existing count indices are now fixed (COUNT_START), not len(LABELS)-2.
Only EBOOT and AID changed; all 25 other files preserved. Atlas preview:
work/out_trader_20260908/trader_preview.png. Full suite passed, including
3300 command/dialog cases, 111 padded hooks, 3340 total hooks, 55 blank cells.
Incremental audit scripts: build_trader_20260908.py and
finish_trader_footer_20260908.py under work/github_issues.

**2026-09-08 remaining commands/dialogs: PREVIOUS INSTALLED BUILD.**
`work/out_dialog_commands_20260908` deployed to E:/SRWZ3/PS3_GAME/USRDIR;
all 27 copies verified. User closed RPCS3, process absence checked. All prior
installed files matched the submenu manifest. EBOOT backup:
work/github_issues/before_dialog_commands_20260908/EBOOT.BIN. Cleared only
validated regenerable BLJS10256_DATA; saves untouched. Awaiting in-game QA.
EBOOT SHA256: 1e2cadad0594cbbdf156cd634c2c9d4e0e8729017faf20203f8dee89ffa694d8.

Centered 27 remaining COMMAND strings (25 new variants plus standalone
Ally/Enemy); includes Attack, Air, Max Break, Tag Command and Parts. Shortened
Auto Transform to Auto Trans. to fit. Original 17 pad slots retained; extended
blank bank 0x8850..0x8870 / U+01A0..01C0. Six exact dialog hooks plus 100
one/two-digit remaining-team counts now correct the pre-substitution Japanese
centering using live pitch and rendered English width. Save FSSA rows have
center flag 0x40 and a common x=-1/1280; their records are unchanged.
Production source: command_layout.py, eboot.py, ui_eboot.json and regression
checks. Incremental audit: work/github_issues/build_dialog_commands_20260908.py.
Only EBOOT changed: all other 26 game files, the 728-byte Spirit-grid helper,
Yes/No layout and split Ally/Enemy widgets preserved. 3000 emitted-PPC
centering cases, 106 hook targets, both blank font layers and full suite passed.

**2026-09-08 COMMAND submenus: PREVIOUS INSTALLED BUILD.**
`work/out_command_submenus_20260908` deployed to E:/SRWZ3/PS3_GAME/USRDIR,
all 27 copies hash-verified. RPCS3 was already closed. Previous 27 installed
files matched the preceding command build; the two affected files were backed
up in work/github_issues/before_command_submenus_20260908. Cleared only the
validated regenerable BLJS10256_DATA cache; saves untouched. Awaiting visual QA.

User's screenshots show the main seven buttons now centered, but the separate
Ally/Enemy states and six unit commands still needed alignment. Added live
pads for Move/Ground/Transform/Change Main/Spirit/Status. Four split-row FSSA
records (0xA8DF4/0xA8E14/0xA8E34/0xA8E54) now point to appended, padded
English strings; each selection state is centered as a complete row with a
10px gap, a common 28px font and baseline. Color/selection flags preserved.
No global Ally/Enemy hook edits. New pad bank 0x8880..0x8889 maps U+01D0..01D9;
original bank/table entries retained. The 728-byte Spirit-grid helper and all
25 other game files remain byte-identical. Both font layers have blank pads.
1020 emitted-PPC command cases and full regression suite passed. Source changes
in command_layout.py, eboot.py, build_ui.py, check_command_layout.py.
Incremental build/audit: work/github_issues/build_command_submenus_20260908.py.

**2026-09-08 COMMAND alignment: PREVIOUS INSTALLED BUILD.**
User confirmed the Spirit grid: "looks great now", then reported map COMMAND
button misalignment and Battle Report overflow. Prepared validated build
`work/out_command_alignment_20260908`. User confirmed RPCS3 closed; verified
no RPCS3 process and all 27 prior installed files matched the confirmed build.
Deployed all 27 files to E:/SRWZ3/PS3_GAME/USRDIR with hash verification.
Cleared only regenerable E:/RPCS3/dev_hdd0/game/BLJS10256_DATA after checking
the exact path and absence of reparse points; saves untouched. Backed up the
two changed files in work/github_issues/before_command_alignment_20260908.
Awaiting the user's in-game alignment check.

`tools/command_layout.py`: seven dedicated blank glyphs 0x8890..8896,
Unicode U+01F0..01F6, dispatch from the VWF stub to 0x78E400, coefficient
table 0x78E600. Leading advance is count*pitch/2 - ink*quad/64, so the
seven buttons center without an assumed pitch. Other command labels keep
their prior allocation/behavior. Both font layers' seven cells verified blank.
Map Funds colon FSSA record 0xABA74 x now matches record 0xABA54 (Z Chips).
Only that coordinate changes in AID member 0; all other members identical.

EBOOT SHA256 `42c9a20fe3c7e04c153b08f0576cb74d31a48f7de80c45f93fd6ff690668cef6`.
AIDDATAPACK SHA256 `9894d3f071937a354146cc11594957dc5ae295c7be3a22103f93e476c27e61fa`.
Builder/audit: `work/github_issues/build_command_alignment_20260908.py`.
420 command PPC cases + all existing regressions passed. Other 25 game files
and the confirmed 728-byte search helper are byte-identical. No in-game
verification yet. Source integration is in eboot.command_labels/build_ui.

**2026-09-07 search grid stack-copy revision (PREVIOUS BUILD, USER CONFIRMED):**
`work/out_search_grid_copy_20260907` deployed to E:/SRWZ3/PS3_GAME/USRDIR.
The user's latest screenshot rejected the previous grid fix: tabs were fixed,
but Intuition and other names remained left-shifted. Root cause: the colored
entry path copies the FSSA template to stack +0x78 (0xadecc..0xadf10), then
draws via 0xae404. The original-address guard skipped this copy. The grid
flags select this path independently of the cursor highlight.

The 728-byte helper also recognizes saved caller LR 0xae408 and one of the
four exact grid string references (0xc2d4/da/e0/e6). Other callers/templates
still fall back. Tests replay the eight real lwz/stw template-copy pairs and
verify their call-site/frame instructions. The old 640-byte helper reproduces
the failure on copied Intuition; the revised helper measures it. 795 original
record + 1060 copied-template PPC cases and the full UI regressions passed.
This is static/emitted-code verification, NOT in-game visual verification.

Incremental audit/build script:
`work/github_issues/build_search_grid_copy_20260907.py`. Only the helper span
differs from the previous validated build. All 26 other game files, all 3327
hooks, the atlas/mapping, translations and stage files are byte-identical.
RPCS3 process absence checked before deployment; only regenerable
E:/RPCS3/dev_hdd0/game/BLJS10256_DATA removed; saves untouched. Previous EBOOT
backup: `work/github_issues/before_search_grid_copy_20260907/EBOOT.BIN`.
Still needs user verification of normal/colored/highlighted grid names.
No commit/push this turn.

**2026-09-07 search alignment (superseded; grid failed visual QA):**
`work/out_search_alignment_20260907` deployed to E:/SRWZ3/PS3_GAME/USRDIR
after user closed RPCS3 and process absence was verified. All 27 installed
SHA256 hashes match the validated manifest. Cleared only regenerable
E:/RPCS3/dev_hdd0/game/BLJS10256_DATA; saves untouched. Prior 27 files backed
up with hashes to `work/github_issues/before_search_alignment_20260907`.
Includes the pending live-pitch confirmation tabs revision below.

`tools/search_layout.py` corrects centering only for four Spirit grid FSSA
templates and nine search tabs. The original centered drawer counts full-pitch
CP932 cells before translated glyph widths are applied, shifting longer English
names left. Scoped call at 0x513d4 now uses a 640-byte helper at 0x78e000 to
measure translated widths with current font state and draw from the corrected
origin. Unknown/Japanese/control strings and unrelated widgets retain the
original path. Nine tab references now use Spirit / Skills / Abilities.
`tools/check_search_layout.py` passed 795 emitted-PPC cases and nine tab checks.
Full regressions passed. Audit `work/github_issues/verify_search_alignment_20260907.py`
confirmed only the new call/stub differs from the pending tabs EBOOT; AID changes
exactly nine tab strings/references, all other members and archives unchanged.
All 3327 hooks and stage plaintext preserved. In-game centering and Yes/No
overlay alignment still require user verification. No commit/push this turn.

**2026-09-07 confirmation tabs revision (included in current build above):**
User screenshot proved the earlier gray No was still offset behind orange No.
Previous fixed spacers assumed glyph quad equals advance; this is false in
the UI renderer. `work/out_confirmation_tabs_20260907` replaces the two blank
cells with live-pitch tabs in vwf_stub: next pen = f31 + 3/5 * original pitch.
f31 is the original draw x (0x1411c); stack +0x84 is current pen, +0x94 is
original pitch, +0x9c is independent glyph quad. No fixed width compensation.
New `tools/check_confirmation_tabs.py` executes emitted PPC including floating
point operations. 548 cases cover unequal quad/pitch, multiple origins,
ordinary glyphs and register preservation. It rejects the previous deployed
stub. Full regression suite passed. Still requires in-game verification.
Audit `work/github_issues/verify_confirmation_tabs_20260907.py` allows only
VWF stub and two former spacer-width bytes to change; all text hooks/archive
content remains unchanged. Backup: before_confirmation_tabs_20260907.
Initially held for RPCS3 process 75164; subsequently included and deployed in
the search alignment build above after process absence was verified.

**2026-09-07 confirmations (superseded build; failed visual QA):**
`work/out_confirmations_20260907` deployed to E:/SRWZ3/PS3_GAME/USRDIR after
verifying RPCS3 was not running. All 27 installed SHA256 hashes match the
validated manifest. No BLJS10256_DATA cache was present; saves untouched.
The actual preceding installed build was `work/out` (includes stages 11–15
and newer battle-screen labels), NOT the older date-card build below.
All 27 previous files backed up with hashes to
`work/github_issues/before_confirmations_20260907`.

Public tracker help-wanted issues #8/#21/#31 share a two-pass Yes/No row.
`issue_hook.json` now uses invisible U+E01E/U+E01F spacer cells, cp932
0x86D6/0x86D7, with font-derived advances 41/51. These put slash at original
column 3 and No at column 5, preserving selected overlays and highlights.
The cells are blank and excluded from letter allocation. All archive bytes
(including atlas) and all stage plaintext match the preceding build exactly.
3324 prior hooks preserved, one choice row changed, two Spirit prompt hooks
added; 3327 total. Audit: `work/github_issues/verify_confirmations_20260907.py`.

#21 also had a fixed-byte-copy bug: 0xabc48..0xabef8 copies the original
UTF-8 warning/prompt including their terminators (55/25 bytes). Translating
those literals to longer VWF UTF-8 truncated them and lost the terminator.
Removed the two `ui_utf8.json` translations; original literals/TOC pointers
stay intact and cp932 display hooks now translate the complete text.
All regression checks passed, including four choice variants (original
centered No has a half-pixel rounding offset), 124 titles, 77 dates, all five
Spirit bands, and 210 runtime name-reader tests. In-game QA remains pending.
Issues remain OPEN with `needs-verification`; detailed public comments added,
no private deployment details posted. No commit/push performed this turn.

**2026-09-06 date cards (older installed build):**
`work/out_date_cards_20260906` deployed to E:/SRWZ3/PS3_GAME/USRDIR with
RPCS3 confirmed closed. All 22 installed SHA256 hashes match validated manifest.
No install cache was present; saves untouched. Previous installed files backed
up to `work/github_issues/before_date_cards_20260906` with manifest.
`translation/date_cards.json` adds 77 exact complete draw-time strings, e.g.
New Multidimensional Century 0001 - April 10 / April 15. Shared sprintf format
at pristine ELF 0x6e5048 is 新多元世紀０００１年%s; dates come from strings in
0x6ef5d0:0x6f0000, including fullwidth month/day padding. Original date values
and format remain unchanged. `tools/eboot.py` loads the new hook file; checks
reconstruct all 77 keys from pristine calendar strings and verify text fit.
Audit `work/github_issues/verify_date_cards.py`: 3240 prior entries identical,
exactly 77 added (3317 total); all archives/title cards and stage plaintext
unchanged. Full regression suite passed. In-game date-card placement still
needs user verification. No new GitHub issue/comment created for this request.

**2026-09-06 all episode titles (previous installed build):**
`work/out_all_titles_20260906` deployed to E:/SRWZ3/PS3_GAME/USRDIR after
user closed RPCS3 and process absence was verified. All 22 installed SHA256
hashes match its validated build manifest. Cleared only regenerable
BLJS10256_DATA cache; saves untouched. Backup of previous installed 22 files:
`work/github_issues/before_all_titles_20260906` (manifest included).
`translation/scenario_titles.tsv` maps all 124 TPACK title IDs 5–128 to JP/EN;
these are texture IDs, NOT stage numbers. Includes branches, finale, epilogue,
and bonus titles; first ten match existing UI hooks. No extra stage dialogue
translation is implied. Full builds now render every title's crisp/glow layers.
EFF 88 two-digit header uses Episode with BOTH original digits shifted; EFF 89
Final Episode and embedded final title translated. EFF 90 bonus/91 epilogue
English headers retained and fallback titles translated. EFF 87 is unchanged
from the previous single-digit fix. All digit pixels/backgrounds preserved.
Audit `work/github_issues/verify_all_titles.py` passed: only TPACK 6–128 and
EFF 88–91 differ from baseline; EBOOT, fonts, AT, AID, school caption, Spirit
bands, save menu, names, libraries/voice and stage plaintext retained.
All 124 title bounds and seven proof sheets checked; heading layout proof is
an asset reconstruction, NOT an in-game screenshot. Runtime animation checks
still pending. Issue #19 stays OPEN / needs-verification. Public comments must
remain status-only: do not publish private local paths or deployment details.

**2026-09-06 public #19 (previous installed build):**
`work/out_scenario_title_20260906`: Scenario 1 title -> A Hope Called Taboo,
normal one-digit card header -> Episode + original dynamic number. User closed
RPCS3; confirmed no process, deployed to E:/SRWZ3/PS3_GAME/USRDIR and verified
all 22 installed SHA256 hashes against the build manifest. Cleared only the
regenerable BLJS10256_DATA install cache; saves untouched. Issue #19 remains
open with needs-verification; in-game checks pending.
New `tools/scenario_title.py`: TPACK member 5 title (crisp/glow),
EFF member 87 texture 3 fallback title and texture 2 Episode word cells.
5,015 identified sprite records modified: 1,691 prefix quads widened, 1,674
digit quads shifted right, 1,650 suffix quads hidden with transparent colors.
Original digit pixels, backgrounds, other animations/members retained. Other
card variants (two-digit/final/epilogue) and other scenario titles untouched.
Integrated with build_atlas and location_caption's EFF build; regression checks
include this fix. `work/github_issues/verify_scenario_title.py` checks all prior
content and backs up all 22 installed files to
`work/github_issues/before_scenario_title_20260906`. Layout preview is a render
from the built assets, not an in-game capture. In-game animation check required.

**2026-09-06 public #24/#7 (previous installed build):**
`work/out_attack_location_20260906` deployed to `E:/SRWZ3/PS3_GAME/USRDIR`
with RPCS3 closed. All **22** installed SHA256 hashes match its validated
manifest. EFFPS3.CPK is now a required build/deploy/release file. All prior
translations preserved: EBOOT, TPACK, voice/library files and stage plaintext
match the #23 baseline. Only AID member 1 texture 2's first two 80x40 word cells
became ALL/Attack; only EFF member 96's (0,104,392,24) caption became
Tokyo-2 — Jindai High School. Photo, animation and all other archive members
preserved. `tools/attack_heading.py` and `tools/location_caption.py` apply these
patches automatically in full VWF builds. EFF pristine cache:
`work/orig/EFFPS3.CPK`; never use the translated disc as fresh source.
`cpkpatch.py` now streams output payloads to avoid a 32-bit MemoryError on EFF;
complete rebuild passed with normal Python 3.8 (the bundled 64-bit environment
lacks fontTools, so do not use it for full builds). Full regression checks and
`work/github_issues/verify_attack_location.py` passed. Backup of all 22 previous
installed targets: `work/github_issues/before_attack_location_20260906`.
No installed cache existed; saves untouched. Both public issues have detailed
comments and needs-verification, remain open; in-game visual checks pending.
Only the school location is translated, not all Japan-map captions (EFF 92+).

**2026-09-06 public #23 support badge (previous installed build):**
`work/out_support_badge_20260906` deployed to `E:/SRWZ3/PS3_GAME/USRDIR` with
RPCS3 closed. All 21 installed SHA256 hashes match its validated build manifest.
Only four label rectangles in TPACK member 2/texture 1 changed to AT; original
numerals 1–4, all other textures, font atlases, EBOOT, UI, voice/library content
and stage plaintext match the previous dialogue-name build. This badge is
attack-only (pilot counter +0x50, skill 1), NOT a generic attack/defense selector.
Defense is a separate +0x51 counter; no gameplay code changed. Full UI checks
passed, including all five Spirit bands and 210 name-reader cases. Backup of
all 21 prior installed files: `work/github_issues/before_support_badge_20260906`.
Only regenerable BLJS10256_DATA cache cleared; saves untouched.
In-game verification pending; issue #23 remains open with needs-verification.

**2026-09-06 dialogue-name fix (previous installed build):**
`work/out_dialogue_names_20260906` is deployed to `E:/SRWZ3/PS3_GAME/USRDIR`.
User closed RPCS3; no running process was found before deployment.
`tools/runtime_names.py` patches
only the three dialogue name getters ($n/$f/$l and consequently $F), translating
exact default Japanese names without writing name buffers or saves. 210 emitted
PPC test cases pass. `work/github_issues/verify_dialogue_names.py` confirmed only
373 EBOOT bytes changed, all 3,240 hooks/other game content retained; all 21
installed files backed up to `work/github_issues/before_dialogue_names_20260906`.
Installed EBOOT SHA256: 5d6aa1a9a3a7ebb003469b4019d89fa87fc6f628dce434b8703a84049a50cb84.
All 21 installed SHA256 hashes match the validated build manifest. Cleared only
the regenerable BLJS10256_DATA cache in native PowerShell after validating its
exact path and absence of reparse points; saves untouched. Detailed comments
posted on public issues #10/#27/#28, with needs-verification (leave OPEN).
Next: in-game visual verification. Re-enter/reload the scene for Back Log testing;
already-expanded cached lines may not refresh. No release published.

**2026-09-06 name-field follow-up (previous installed build):**
`work/out_name_fields_20260906` is deployed and hash-verified, with all integrated
recovery fixes plus LN / FN / standalone Kamishiro display hooks. Backup:
`work/github_issues/before_name_fields_20260906`. `_DATA` cleared, saves untouched.
Visual review pending. Editable names and dynamic dialogue names are unchanged.

**2026-09-06 integrated rollback recovery (previous installed build):**
`work/out_integrated_20260906` is the verified/deployed 21-file bundle, with
`build_manifest.json` checksums. Do NOT deploy stale `work/out` or `work/out_grow`.
Current tracker: `retro-trans/SRW-Z3-Issues-Tracker` (public); Linear/site work was
abandoned by user, not deleted. All 21 pre-recovery files are backed up in
`work/github_issues/before_integrated_20260906`. Full VWF builds now call build_ui
and check_issue_fixes automatically. UI lookup keys are copied into EXT to
avoid later movement-label patches corrupting the Grd hook. See the top of
`docs/GITHUB_ISSUES.md` for preservation checks and verification status.

**2026-09-06 GitHub review batch:** see `docs/GITHUB_ISSUES.md` for deployed
candidates, checks, backup paths and unresolved reports. Leave issues open;
use `needs-verification` for built fixes. Ignore #21/#22 battle voice lines
and defer #6 per the reporter's comment. Do not mistake older “texture”
conclusions below for verified source identification.

## Where the project stands

**Public issue board:** see `docs/PUBLIC_ISSUE_BOARD.md`. Homepage lists the SRW Z3
Linear project's issues through a read-only Worker; separate detail page retains
comments/screenshots. All 41 GitHub reports imported (43 total including two
tests); all 37 original screenshots are now uploaded into Linear and embedded
in report descriptions (40 working images including comments). See the image
audit in the linked document. No Discord
integration or game changes. Credential file is gitignored.

**Working and proven in-game:** the full edit pipeline. Stages 1-5 are
translated (translation/stage*.json; stages 3-5 via subagent briefs from
export_stage.py, merged by sha). Japanese text has been
replaced with English, repacked, re-encrypted, loaded by the real game and read
on screen. See `README.md` for the recipe.

**Not solved:** English still renders one character per em, because the text
renderer advances a fixed ~37.28px per glyph regardless of glyph width. A new
font was drawn and installed successfully, and it did **not** fix this -- it
cannot, because the advance is a code constant. The remaining work is a
renderer patch. Details in `docs/FONT_HUNT.md`.

## Stages: 1-30 plus the intermissions (2026-09-10)

The between-stage scenes live in their own 0200-series scripts
(`STG0200`-`STG0272`, 26 files, 1,281 records) which the project had never
extracted; they are translated and registered now. Stages 11-30 followed
the standard chain (decrypt with `make_npdata -d`,
`extract_stage.py` to `work/lua11`, `export_stage.py --range` briefs of
120-134 records, one Sonnet subagent per brief, `merge_stage.py`,
`check_stage.py` clean, register in `manifest.py` / `deploy.py` /
`extract.py` / `apply_xdelta.py`). Members with dialogue are 3 and 4 (stage 13
also member 2, one caption); members 2/5 otherwise hold no records. Next:
stage 31 (`STG0031A`/`B`, a route split), same recipe; also untranslated: STG0500
(1,247 records, D-Trader), STG0700 (872, banter), STG0600 (236,
tutorial). Run about three agents at a time. about 100 records per agent-slice,
~100k Sonnet tokens each. Brief the agents with the settled conventions
(姐さん = Boss, nine-dot 「………」, （）thoughts stay bare, AG in normal case,
banners `～ Ship, Room ～`), and run the post-merge pass (brackets,
ellipses, honorifics) before building. Agents write glossary names as
`$$japanese$$` tokens -- brief rule 7 says so and stages 1-30 are now
converted, so a stage that comes back in literal English is drift, not a
style choice. The game has 118 story-stage scripts (1-100 with route splits).

## Where English text goes -- the channel map (2026-09-04)

Every string on screen reaches it through exactly one of these channels.
Pick the channel by WHERE THE GAME READS THE BYTES, not by where the
Japanese happens to sit -- the same label often exists in two places and
only one copy is drawn. `docs/TRANSLATING.md` has the mechanics.

| channel | file(s) | matches | notes |
|---|---|---|---|
| draw-time hook (0x140f4) | `translation/ui_hook.json`, `abilities.json`, `spirit_hook.json`, `skill_hook.json`, `ability_hook.json`, `parts_desc_hook.json`, `tutorial_hook.json` (`eboot.UI_HOOK_FILES`) | any cp932 string drawn by the one string drawer, by exact content, any length; Japanese absent from the EBOOT is copied into the EXT segment | multi-line entries are also registered line by line (some boxes draw one line per call). `{cN}...{/c}` in the English passes the game's inline colour bytes through; a colour-marked line gets a "." string placed right after it because the game reads its 。 from the next string in memory. EXT segment is 512 KB (`EXT_SIZE`), table 4,096 entries. |
| UTF-8 label table | `translation/ui_utf8.json` | standalone UTF-8 strings in the EBOOT (window titles, prompts, the spirit-list Duration words, the Lecture Plate titles, the emblem lines) | the hook never sees these. If a hooked label stays Japanese, look here first. |
| COMMAND menu | `translation/ui_eboot.json` | the battle COMMAND UTF-8 table | centring pads, VWF via U+0100+ |
| in-place UI pool | `translation/ui_aiddata.json` | AIDDATAPACK member 0 cp932, capped at the slot | only member 0; a label with copies elsewhere needs the hook |
| RPW j-string swap | `analysis/glossary.json`, `weapons.json`, `spirits.json`, `skills.json`, `parts.json` (names only), `name_pieces.json`; per-record `rpw.piece_overrides` / `name_overrides` | names, weapons, spirit and skill NAMES, part NAMES | pilot names are drawn as separate given/surname slots; each resolvable record gets both slots' English. **Never swap a boost-part description (boost-p columns 3-8): any of them corrupts memory at boot** (13-boot bisect; `build_project.py` refuses). Multi-line RPW strings of every kind go through the hook instead. |
| textures | -- | Operation End / intermission headers, the PP-screen tabs and PP block, ＜レコードライブラリー＞, the spirit/skill/ability tabs' glow text | future atlas work |

Known and deliberately unfixed: the spirit-list grid centres names by
fixed-pitch character count (renderer-side, like the font advance);
voice-actor names in the library; the textures above.

## Battle voice lines

**Retranslated in full 2026-09-07** (Codex drafts, 211 sections, 31,666
lines; pipeline below). The old budget-clipped English is gone.

**No length limit since 2026-09-06.** The game reads each unit's block of
SRVC.BIN through a 277-entry table of block offsets in the EBOOT (file
offset 0x830be0); `tools/srvc_blocks.py` rebuilds the file with grown pools
and `build_project.py` writes the new table in the same run, so a bark may
be any length (keep under ~36 cells for the screen). The retranslation ran as
`export_voice.py` brief -> Codex CLI (`gpt-5.6-sol`, high reasoning,
~50k tokens a section, six in parallel) -> `check_voice.py` -> structural
pass -> `merge_voice.py`. What remains is a screen check: the 36-cell cap
is an estimate, and 1,229 lines sit in the 30-36 band. Details: `docs/TRANSLATING.md`, "Pools can grow".

`docs/VOICE_HANDOFF.md` — one unit's voice set per SRVC.BIN section,
translated IN PLACE only (appending crashes the game: offsets are
pool-bounded). 211 sections, 31,670 distinct lines; **211 sections and
31,661 lines ship** (99%). Sections go through `export_voice.py` → subagent →
`check_voice.py` → `merge_voice.py`, then `voice_propagate.py` to carry the
result to any section that repeats it. The build applies every
`translation/voice_*.json` itself now, so the old "re-run the writer after
every build or it silently regresses" trap is closed.

Two things dominate the remaining work, both in `docs/VOICE_HANDOFF.md`:
**4,115 lines are repeats** of another section (20 groups — translate one,
propagate to the rest), and **the unit attribution is often wrong**. Gundam
Mk-II, Strike Freedom and Nu Gundam collect 50 sections between them on
common weapon names; four sections have already proven to be other shows
entirely. Read enough lines to recognise the speaker before adopting a
register, and record what you conclude in `analysis/voice_identity.json`,
which the brief and merge tools prefer over the weapon match.

## What you need on a new machine

| thing | why | notes |
|---|---|---|
| The game, dumped from your own disc | everything | `PS3_GAME/` folder tree, ~4.1 GB |
| RPCS3 | runs the game; also **decrypts SDAT and the EBOOT** | `--decrypt` is used as a tool, not just an emulator |
| PS3 firmware (`PS3UPDAT.PUP`) | RPCS3 needs it | from Sony; verify the MD5 against the URL path segment |
| `make_npdata` | re-encrypt SDAT | build from source; see below |
| Python 3.12 | the tools | `capstone` optional, only for EBOOT disassembly |

**Put the game on an SSD.** Load times are dominated by disc I/O.

`make_npdata` (Hykem) builds from the `Linux/` C sources with MSVC:
`cl /nologo /W2 /O2 /D_CRT_SECURE_NO_WARNINGS /Fe:make_npdata.exe *.c`
(only 64-bit printf warnings). No prebuilt Windows binary ships with it.

## Traps that cost real time here

1. **`make_npdata` version 3 and 4 produce SDAT the game rejects**, even though
   make_npdata decrypts its own output perfectly. **Use version 2.** The
   originals are v4, so the obvious parameter is the broken one.
2. **After editing any disc file you MUST delete
   `dev_hdd0/game/BLJS10256_DATA`.** Otherwise the installed `INSCO` copy is
   stale against the disc and the game shows
   "ゲームデータが壊れています" (game data corrupted). This looks exactly like a
   bad patch and is not one. Deleting it forces a reinstall, which then needs
   one button press on boot.
3. **Close RPCS3 before using `--decrypt`.** It is single-instance, so running
   the oracle while the game is open produces silence that looks identical to
   rejection.
4. **`rpcs3 --decrypt` only processes its FIRST path argument**, despite the
   `<path(s)>` help text. `tools/unsdat.py` therefore runs one invocation per
   file and kills each one once its output appears.
5. **A byte-identical SDAT rebuild is impossible.** The SDAT key is the per-run
   digest at 0x40, so re-encrypting the same input twice gives different files.
   Do not chase it. Verify functionally instead.
6. **RPCS3 auto-updates break the decryptor.** The updater runs on launch
   and 0.0.42-19895 (2026-08-31) stopped producing `.unedat` from
   `--decrypt` -- every stage decrypt "fails" with no error, exactly like
   trap 3. The previous build survives at `rpcs3_old/rpcs3.exe` and still
   decrypts (the updater overwrites that folder on the NEXT update, so pin
   a copy if it matters). Check `update_history.log` before blaming the
   loop. Better: skip RPCS3 for SDAT decryption entirely --
   `make_npdata -d <in> <out> 0` handles these self-keyed SDATs and its
   output was validated byte-identical to RPCS3's when the oracle was
   built; stages 6-10 were decrypted that way after BOTH rpcs3 builds
   started blocking (likely on the updater prompt, since the same build
   that decrypted at 16:00 failed at 19:00 with a newer version available).
7. Don't keep backups of `BLJS10256_DATA` -- it is ~3.5 GB and regenerates.

## The acceptance oracle

`rpcs3 --decrypt <candidate>.SDAT` answers "will the game load this?" in
seconds. If a `.unedat` appears, the game will accept it. Validate the oracle
against an untouched file before trusting a run. This is far cheaper than a
~2 minute boot.

## English text rules

- **Must be fullwidth.** Halfwidth ASCII renders as paired kanji; halfwidth
  katakana renders as blanks. There is no single-byte path in the renderer.
- Fullwidth costs **2 columns**; budget ~34 columns/line, ~29 characters.
- cp932 cannot encode `'`, `"`, em dash -- `tools/fullwidth.py` substitutes.
- Line 1 of a dialogue record is the **speaker name** and is structural.
- Lengths are free: dialogue is Lua source, not pointer-table records. The
  shipped English line is 77% larger than the Japanese it replaced.

## The font

Atlas: `DATA/TABATA/TPACKPS3.CPK` members **1 and 3**, 16bpp (format `0xAB`),
4096x1120, a **32x32 cell grid**, 128 cols x 35 rows.

**TPACK is a plain CPK on disc, not SDAT** -- `tools/cpkpatch.py` alone
replaces it. Atlas edits are proven to take effect in-game.

Code to cell:

```python
cell = (lead - 0x81) * 192 + (trail - 0x40)      # flat 192 stride, no offset
```

Verified against four in-game anchors: `!`=9, `0`=207, `A`=224, `a`=257. Two
earlier models were wrong and each was caught in-game -- 188 (valid codes only)
turned lowercase into a Caesar cipher (`Look` -> `Lppl`), and 189-with-offset-3
fixed letters but rendered `!` as `:`.

`tools/makefont.py` draws an original geometric sans into the atlas and works
end to end. It improves how the text *looks* but does not change density.

## The one remaining problem

Measured from a solid-block test at 1920x1080: glyph quad **32.00px** at 1536
internal (exactly the cell, blitted 1:1), advance **37.28px**, so ~5.3px of
fixed letter-spacing. The advance ignores ink -- the shipped Latin varies
14-24px and still renders on an even pitch.

The shipped glyphs are **already correctly proportional** (8px `i`, 24px `h`).
`tools/fontatlas.py` emits every glyph's real ink width to `metrics.json`. Only
268 cells are <=24px wide; 3281 are exactly 30px (CJK, correctly full-width).
So a per-glyph advance needs **no new font at all**.

Static searches that did NOT find the advance -- do not repeat them:

- atlas geometry constants (`4096.0f`/`1120.0f`): the one tight cluster is a
  1280x720 UI rect table
- SJIS lead-byte range checks: 91 `cmpli`/`cmpi` against `0x81/0x9F/0xE0/0xEF`,
  never 3+ distinct bounds in one window
- cell arithmetic (`idx>>7` with `(idx&127)<<5`): 17 and 0 hits, never
  co-occurring, so cell UVs are table-driven not computed
- a per-glyph width table: zero runs of >=512 bytes in the 4..34 range anywhere
  in the 8.7 MB ELF

**Next step, and it needs to be interactive:** run under RPCS3's debugger,
breakpoint the dialogue draw, and read the advance from live code. Then express
it as an RPCS3 `patch.yml` entry driving per-glyph widths from `metrics.json`.
Decrypt the executable first with `rpcs3 --decrypt EBOOT.BIN`.

## Prior art -- do not translate from zero

- Saint-ism's Z3 Jigoku-hen project: script through roughly chapter 10
- GBAtemp: a menu translation
- Akurasu: terminology, already a source in the PS2 project's glossary
- The PS2 SRW Z project's `analysis/glossary.json` (1000 terms with provenance)
  is the highest-value carryover -- same continuity, overlapping cast

## Repository hygiene

No disc images, no `.SDAT`, no extracted Lua, no CPK contents, no Japanese
script. `.gitignore` enforces it. Third-party binaries (RPCS3, `make_npdata`)
come from their own projects.
