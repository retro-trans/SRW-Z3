# Changelog

## Withdraw 0.6.19 upgrade from first public release (2026-09-26)

- User requested original-only downloads for 0.6.21. Withdrew the 21,234,653-byte
  .19->.21 upgrade from GitHub and its exact route from the Retro Trans catalog.
  Local old assets, original metadata and backups are preserved for recovery.
- Keep full-patch bytes and all source/output identities unchanged. Re-scope
  manifest/validation/checksums to that route, retaining its existing successful
  round-trip evidence; no new game build or installation. Update player docs.
- This explicit withdrawal is not an immutable catalog extension: clients that
  cached the former two-route entry must reset that cache before refresh, or use
  manual full-patch mode. No shared validator weakened and no other routes changed.
- Four remaining public assets match the original-only ready directory and pass
  Retro Trans public-download validation. Catalog withdrawal commit b00b52dc.

## Fresh public repository and 0.6.21 reissue (2026-09-26)

- User approved renaming/preserving the original repository as a private archive
  and creating a separate public SRW-Z3, avoiding retained old source objects.
- Updated README and 0.6.21 notes for Retro Trans, exact original/0.6.19 input
  routes, withdrawn historical assets and the cleaned source-history boundary.
  Explicitly distinguish unchanged 0.6.21 binaries from later source-only fixes
  and Vietnamese work; no new game build or installation.
- Original repository ID 1345954230 is private and archived as
  SRW-Z3-private-archive-20260926. Fresh public SRW-Z3 is independent repository
  ID 1388978408; old commit 1cc692a is not accessible from it. Only cleaned
  master ancestry was uploaded. Preserved linked-worktree remotes now point at
  the private archive, preventing accidental old-history pushes to the public one.
- Published 0.6.21 at 2026-09-26T09:44:12Z (release 397176829), after checking
  the five uploaded asset hashes/sizes and release notes against local inputs.
  Tag points to clean snapshot 77cb479; original source identity stays in the
  unchanged build manifest. Requested Retro Trans catalog refresh 36233677979.
- Added current Retro Trans installation instructions; clearly separated the
  old 0.6.3-era guide and historical private release records from public .21.
- Independently downloaded/verified the public assets through Retro Trans's
  release_record; its route planner resolves original and exact 0.6.19 to .21.
  Global catalog refresh failed on unrelated SRW-Z v0.9.85 manifest naming.
  Published only the verified Z3 record in tools catalog commit0208c41a, with
  all ten previous records unchanged and immutable-identity checks passing.
  The live catalog URL used by the desktop app now resolves both Z3 routes.
  No SRW-Z release changes or validator bypass; the separate global-refresh
  problem remains outside this release's scope.

## Public-repository preparation authorized (2026-09-26)

- User authorized committing the Vietnamese integration, replacing hosted
  history and making the repository public only after the hosted-content audit.
- Initial inventory found one master branch, nine historical tags and nine
  releases. User authorized their local backup and removal, then explicitly
  requested public visibility and a Retro Trans-compatible release.
- Backed up all 36 assets (1,662,554,942 bytes), release notes/metadata and tag
  identities; verified every asset's size and SHA-256 against GitHub twice.
  Replaced hosted master with clean history at 36e601c and deleted all nine
  tags in a leased atomic push, then deleted all nine backed-up releases.
  Verified no remaining releases/tags. Local old Git and linked worktrees remain
  intact. Recovery copies/receipts are in work/publication-audit-20260926/.
- Hosted audit found no artifacts across 85 Actions runs; the sole failed job
  stopped at app authentication. The one closed PR's initial tool/doc history
  contains no source dumps. Current tracked content excludes local source data.
- Publication stopped while PRIVATE: GitHub still returns a removed Japanese
  source catalog file by old commit 1cc692a despite removing its branches/tags.
  Requesting permission for a fresh public repository while preserving this one
  privately; no repository deletion, rename, visibility change or catalog entry.
- Existing PS3 English 0.6.21 assets pass Retro Trans 0.3.0 release validation;
  no patch bytes changed and no new game build/install was run. Re-publication
  awaits the safe destination. Later fixes and VI content remain source-only.
- Corrected the earlier authentication diagnosis: normal Windows keyring access
  works; only the restricted session reported invalid CLI authentication.

## Vietnamese worktree content merge (2026-09-26)

- Imported all 188 Vietnamese locale JSON files from codex/vietnamese-silver
  at 5dd5d66, using the current canonical IDs. All 43,104 source/context/kind
  identities match. Replaced the 244 obsolete opening drafts with the later
  branch versions; preserved every imported Vietnamese text value exactly.
- Current glossary-token guards reject 393 formerly accepted dialogue rows.
  Retained their text and marked them needs_review, alongside the nine already
  pending rows. Recorded all 402 review IDs, original statuses, six existing
  title notes and input hashes in localization/qa/vi_worktree_merge_20260926.json.
  No source definitions or shared validation rules were weakened.
- 42,155 imported rows pass current catalog and glossary checks: 41,143
  dialogue, 776 glossary, 118 UI and 118 titles. 547 imported entries remain
  explicitly missing; including absent catalog entries, Vietnamese has 60,626
  missing entries overall. This is not a new meaning/layout/gameplay review.
- Content-only integration: no old Git history, English changes, Japanese
  script dumps, fonts or Vietnamese build adapters imported. The original
  linked worktree is untouched; old local drafts backed up under ignored
  work/vi-merge-20260926/backup/. No build, installation, commit or publication.

## Local source privacy and fresh Git history (2026-09-26)

- Excluded Japanese message definitions, the source-bearing PS3 compatibility
  template and generated translation JSON/TSV from the new tracked snapshot;
  retained their files locally. Editable locale text, glossary lookup keys
  and code remain tracked. Added archive/executable ignore rules.
- Added fresh-clone prerequisites and documented that extract.py alone does
  not recreate the complete canonical source catalog. Missing local catalog
  inputs now identify the setup guide; no validation fallback was introduced.
- User authorized preserving both linked worktrees against an ignored local
  archive of the former repository, and replacing main history with one new
  initial commit containing current work. No remote rewrite, visibility
  change, release, game build or installation is part of this operation.

## Translation comparison tool and contributor guide (2026-09-26)

- Added README "Check the translation" and "Translate it" sections modeled
  on SRW-Z, adapted to Z3's canonical catalog rather than PS2 disc writers.
- Added tools/compare_translation.py: offline Japanese/locale HTML comparison,
  glossary expansion, stable IDs/context/edit paths, search, filters and
  pagination. Missing translations, unavailable sources, drafts, invalid
  entries, identical strings and intentional blanks are kept distinct.
  No English fallback; dry-run first, new HTML outputs under work/ only.
- Added current TRANSLATING.md instructions reusing localization.py's guarded
  validation/sync/language tools; corrected the README's obsolete edit path.
  No game build, installation, release or upload.
- Matched the legacy parts/skill description adapters' dedicated Spirit/skill
  dictionaries, including precedence and missing-locale handling, instead of
  misclassifying their tokens as absent glossary entries.
- Validation: 7 comparison tests and 18 catalog tests pass. Browser preview
  verified paging, Japanese/English search, category/status filters and
  side-by-side layout; no console errors. Full report includes
  103,183 entries, 1,269 unavailable sources, 7 blanks and 287 identical-text
  hints, with no unresolved-reference/structural flags. These are catalog
  counts, not a gameplay-coverage claim. All 543 compatibility views agree.

## README credits (2026-09-26)

- Added a Credits section using the role-table format of
  [SRW-Z](https://github.com/retro-trans/SRW-Z#credits), with pow as Project
  Lead and SecondarySebs, gabrielgamer99, Theoldnile, Kapt, mr.notaru and
  rikineko credited for Playtesting. Names and capitalization are as supplied.
- Documentation only; no build, installation or publication.

## Unbuilt stage speaker-header restoration (2026-09-26)

- Screenshots traced to stage0050b_04: source speakers Daston, Aoi and Amata
  were absent from English inner thoughts, causing dialogue in the name bar
  and missing speaker changes in the backlog after Angel. Not a name-length
  or dollar-sign replacement issue.
- Audited all 62,788 canonical dialogue records. Restored 13 explicit source
  speakers across stage0050b_04, stage0068b_03, stage0100a_03 and stage0100b_03;
  inserted 105 missing name/dialogue newlines in stage0055_03. Existing body
  wording, source identities, portrait IDs and glossary meanings unchanged.
- Added a shared source-bound structural guard to canonical catalog loading,
  stage validation and Lua patching. Explicit named speech/thought records
  cannot lose their header or join it to dialogue; anonymous source records,
  narration and labels remain untouched. No complete build or installation.
- Validation: 23 tests pass (5 speaker regressions, 18 catalog tests).
  All 1,687 records in the five affected original Lua files match canonical
  identities and pass stage encoding/width/line checks; patched in memory
  only. Exactly 118 English records changed, with dialogue bodies unchanged.
  Catalog reports zero issues; all 543 compatibility views synchronized.

## Unbuilt complete D-Trader upgrade systems / unlock reports (2026-09-26)

- Registered all four native upgrade systems (UNS, ZCI, DME, TEU): names,
  Trade List background descriptions and gameplay effects. The four fixed
  records were absent from earlier part-effect and shop-text bindings.
  Names use exact draw hooks; eight descriptions fit their existing padded
  fields. Record size, IDs, prices, unlock conditions and gameplay stay intact.
- Added the 19 missing completed-condition report forms; with the original
  two, all 21 native conditions are inventoried and verified. Includes the
  reported Raise 3 Ace Pilots requirement, plus the other upgrade systems and
  the full neighboring power-part report family. Existing shop requirements
  are reused unchanged, not replaced by guessed thresholds.
- Fixed the actual native availability constructor: it copies exactly18
  prefix bytes and8 suffix bytes. The old32-byte "Now at D-Trader: " was
  truncated to "Now at D-". New "Unlocked " prefix and padded period honor
  both fixed lengths. Four exact mixed-encoding notice hooks translate the
  inserted system names without expanding native16-byte name fields.
- Added source/field/width guards and native-PPC copy regressions, integrated
  packed-output checks and complete in-memory executable testing. No complete
  build/install/version/publication; .21 remains active, runtime QA pending.
- Validation:19 tests pass (3 upgrade/report,4 activation/full-executable,
  3 shop/Spirit-panel,5 song/deployment,4 Spirit terminology); full current
  executable composes in memory with4,752 EXT bytes free. Catalog zero issues,
  all543 compatibility views agree and diff whitespace check passes.

## Unbuilt D-Trader confirmations / Spirit-use panel (2026-09-26)

- The purchase screenshot combines an English item name and confirmation
  question with a separately assembled Japanese suffix. Earlier shop/header
  and skill-learning fixes did not bind this C++ string append path.
- Added six canonical entries and source-bound trader_spirit_prompts adapter.
  Buy ends in "to buy"; selling uses an item line and quantity "to sell".
  Exact 16/4/18-byte append sizes are retained, including the compiler-inlined
  four-byte sell fragment. Native allocation sizes, counts, names, prices,
  TOC pointers and terminators are untouched. No new executable allocation.
- Translated the shared caster panel's 消費ＳＰ/SP rows to SP Cost/SP.
  Removed all four separate decorative Spirit-name quote frames, including
  the stray closing bracket next to Bless; dynamic names and help remain.
  Only five UI text pointers change, not their positions, fonts or live values.
- Integrated UI build and packed-output checks plus executable verification.
  Regression coverage replays actual native buy/sell copy instructions,
  protects append byte counts, checks duplicate widgets, and composes on
  pristine and installed .21 UI. No full build/install/version/publication;
  .21 remains installed and next-build visual confirmation is still required.
- Twelve focused tests pass (three new, four activation/full-executable,
  five command/speaker regressions); full executable composes in memory with
  5,784 extension bytes free. Catalog zero issues and 543 compatibility views
  agree. New catalog is consumed directly; no legacy-view text rewrite needed.

## Unbuilt compact Song Soul stat label (2026-09-26)

- Basara screenshot shows Song Soul overlapping its live stat value. The
  shared runtime 歌魂 hook used a full term in CQB's two-cell stat slot;
  the earlier 280px help-width check did not cover this narrower use.
- Changed only the compact label to Sng (53.375px at 28px, versus CQB 59.5px
  and old Song Soul 140.875px). Four help variants retain Song Soul. The same
  hook serves related runtime stat displays; values, positions, fonts,
  pilot records and gameplay remain unchanged.
- Runtime hook labels now honor their catalog width limits in production UI
  validation; 歌魂 has a 56px two-cell budget. Added regression coverage at
  all four CQB label sizes, plus preservation of the full explanatory term.
  Source only: no full build, install, version or publication.
- Five song/deployment regressions pass, including rejection of the old long
  label. Catalog has zero issues; all 543 compatibility views pass (this
  adapter reads canonical text directly, so no generated view changes).

## Unbuilt Akurasu Fury / Break terminology correction (2026-09-26)

- Checked Akurasu's Z3 Spirit list and Asuka pilot database: her level-33,
  35-SP command is 闘志 / Fury, not Fighting Spirit. The distinct 直撃
  command is Break, replacing the patch's previous Fury label. Costs,
  effects and unlock levels are unchanged; no unrelated command renaming.
- Updated 18 canonical entries across six catalogs: both command names,
  deployment ability, Bravery effect, two bonuses and twelve part-description
  variants. Compact status cells now use Fu / Br without changing glyph IDs.
  The separate 戦意高揚 pilot skill remains Fighting Sp; 闘争心 stays Instinct.
- Updated terminology documentation and regression coverage. No complete
  game build, installation, version or publication; .21 remains installed.
  The shorter Fury label still needs next-build in-game visual confirmation.
- Validation: 14 focused tests pass (4 terminology, 6 parts, 4 pilot status);
  canonical catalog and all 543 compatibility views pass with zero issues.
  Part descriptions rewrap with existing metrics; the immutable .3 fixture
  test reconstructs its historical names rather than expecting new wording.

## Unbuilt category-wide battle speaker overflow fix (2026-09-26)

- User confirmed Mariemaia's corrupted name is from 0.6.21. The .21 complete
  fallback-table check verified stored names, not native caption transport;
  it did not fix the shared long-name overflow.
- Established the native cause: three strcpy calls at 0x1073e4/0x107494/
  0x10767c overflow a 31-byte name field; the adjacent dialogue write replaces
  its tail. Reproduced this with the original PPC instructions and translated
  Mariemaia Soldier bytes, not a guessed truncation model.
- Added battle_name_transport: bounded short-name copies, tagged references
  for every longer name, resolved before name drawing/length measurement.
  Native caption snapshots preserve the reference. Covers both encodings and
  future long names without a per-name exception list. Keeps full canonical
  names, distinct squad plurals, native structures and loader layout intact.
- Added source-contract guards and build/production-gate verification. Five
  new tests exercise original overflow, all three producers, actual native
  snapshot/line formatting, resets, speaker transitions, 30/31-byte boundaries,
  long synthetic inputs, ABI and canaries. All 1,625 fallback bindings/RPW
  nickname cases pass, including 62 long cases in the .21 fixtures.
- Twenty-seven focused tests pass, including full current executable composition
  in memory and existing name/link regressions. The patch adds 144 bytes;
  5,648 bytes remain in the unchanged extension. Updated the budget test to
  include the new final allocation rather than the earlier prompt allocation.
  Details: docs/BATTLE_NAME_TRANSPORT.md. No full build, install, version change
  or publication; .21 stays installed. Runtime visual confirmation pending.

## 0.6.21 built, installed and published (2026-09-25)

- User approved building all pending fixes and creating the PS3 GitHub release.
  Preflight passes for 143 stage containers / 62,772 dialogue records;
  thirty-five focused regressions pass including fresh-process UI setup.
- Prepared docs/releases/0.6.21.md covering changes since published .19,
  including local .20. Full-original and exact-.19 update routes supplied.
  Repository verified PRIVATE; no visibility or public-catalog change.
  The five unbuilt September 25 batches below are included in this build;
  their original source-only notes record the state when each was prepared.
- First full build safely stopped before numbering: the separate UI-builder
  process had not initialized the glossary used by E-Change help. Added explicit
  initialization and a fresh-process entrypoint regression. Failed output is
  preserved; retry uses a new _r2 directory. No failed output is installed.
- Retry work/build_0.6.21_english_20260925_r2 passed all production checks:
  5,445 executable hooks, 31,666 subtitle readbacks and 2,119 audited mission
  variants with none missing. Counter and title footer are both 0.6.21.
- Required hardware packaging dry-run and write passed; 554 files match in
  both ISO trees, guarded two-LOAD layout and RPCS3 SELF decode agree.
  Image: 5,011,013,632 bytes; SHA256
  b67c0a23924e79ab31d28c9b726535473087eee9bf8e5dd4758ce4c6ec64c3e0.
  SELF SHA256: 5e3a63e99eb4eab1acaa549284bc26e02895e86c0de9cd60c950a564266b3355.
  Package: work/ps3_hardware_0.6.21_20260925; snapshot of its wrapped files
  recorded by releases/0.6.21.json (219 files). Runtime checks still pending.
- Source provenance: 418c709ad973f02c1dd4fe641cdcec3e9aee9e3b includes all
  build inputs changed since .19, including the UI subprocess fix. Only reviewed
  sources were committed/pushed to the private repo; untracked game ZIP and
  executable were excluded. Release patch validation and installation passed.
- Installed the verified wrapped snapshot after dry-run with RPCS3 closed:
  all 219 updated files match, complete-disc check passes, 22 saves unchanged.
  Other game registration preserved; old files recoverable under
  work/install_backups/0.6.21_20260925_233223. No install cache was present
  to move; it will regenerate on launch. Local per-file patch sets pass
  all decode checks (219 original + 149 from .19); no ZIP upload reinstated.
- Shared Retro Trans v0.2.1 build and validation gates pass for both whole-ISO
  routes in work/retro-trans/ready_0.6.21. Full patch: 154,763,400 bytes,
  SHA256 5ba685348e2accb99a8c4a64c53c6ae54d10e5bb5ba30b59c35d56e26b7d969d.
  Exact-.19 update: 21,234,653 bytes,
  SHA256 40c63927c3cc94edb4cf65ed8e2d32b92d3beeb391e9be83d665b57b4f2860d5.
  Both decoded to the full verified target SHA256; five protocol assets only.
- Published latest private release v0.6.21 at 2026-09-25T16:50:04Z:
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.21.
  Draft asset names, sizes, SHA256 digests and notes matched locally before
  publication; latest status and the same five assets rechecked afterward.
  Tag commit 9464ca41692cffa84acfc7e36c617c971752e532 retains the exact build
  sources of 418c709. No ISO, extracted game files, per-file ZIP, Vita assets,
  visibility change or public-catalog enrollment. New runtime tests pending.

## Unbuilt pilot-name composition and Spirit-column fixes (2026-09-25)

- Asuka's status heading combined the translated display prefix "Asuka
  Shikinami" with another "Shikinami". Mari had the same composition problem.
  RPW overrides now resolve display-prefix + surname against the complete
  canonical name before splitting English: Asuka Langley / Shikinami and
  Mari Illustrious / Makinami. All six Asuka and three Mari records covered.
  The whole matching category has fifteen records (also Mardukas, Kalinin,
  Guen and Danigan); full-name spelling stays glossary-driven. Short-name
  field zero and the game's separator are unchanged. No global name rewrite.
- Both pilot-status Spirit lists retained full command names, including the
  then-current Fighting Spirit (renamed Fury per Akurasu on September 26).
  Their name column uses compact 18px metrics and the cost column moves
  24 native pixels right. All canonical Spirit names clear it by at least eight
  pixels; the five-cell cost fits the panel. Original five-row spacing, costs,
  unknown-command markers, text and colors remain unchanged.
- Eight source/in-memory regressions pass against pristine and .20 data;
  unrelated RPW slots and UI bytes are checked unchanged. Production build
  and packed-output gates now check the compound names and both Spirit lists.
  No game build, installation, version change or publication. Runtime visual
  verification remains pending.

## Unbuilt E-Change, battle fallback speakers and swap equipment (2026-09-25)

- Translated the missing E-Change help/footer and its Spirit-effect reset
  warning; audited the adjoining command-help rows. Added area selection /
  confirmation, ally/enemy target help, Element skill help, part/action/stat
  explanations and remaining command labels. Seventeen FSSA widgets keep
  their positions, fonts, states and dynamic placeholders; 21 exact hooks
  cover runtime text. Gepard/Spada prose uses canonical glossary tokens.
  September 26 follow-up: this pass left the separate Spirit-use quote frames
  and caster SP-cost label Japanese; trader_spirit_prompts now covers them.
- Covered all four named swap-equipment options in BOTH native tables:
  Round Mover, Lightweight Configuration, Assault Configuration and BWS.
  Reuses the existing reward-message terminology; None, equipment IDs,
  table pointers, stat changes and selection logic remain unchanged.
- Replaced the previous piecemeal UTF-8 battle-fallback coverage with a
  source-guarded inventory of all 1,155 display slots (470 canonical bindings,
  468 distinct source strings). Includes Zessica and every neighboring series.
  English is allocated separately and only these display pointers are changed;
  native CP932 lookup keys are not repointed. Shared Ray/Rei and Mehna/Mina
  source strings are resolved per slot, not by global spelling replacement.
  Correction after the September 26 .21 runtime report: this covers stored
  fallback text, not the native 31-byte caption copy. The category-wide source
  fix above addresses that separate overflow; the .21 release still has it.
- Catalog check: zero issues; all 543 compatibility views agree. Fifteen
  source, layout, isolation and full executable tests pass; 5,792 bytes remain
  in the unchanged extension after all pending batches. No build, install,
  version increment or publication. In-game confirmation remains pending.

## Unbuilt special-skill activation banner follow-up (2026-09-25)

- Screenshot 特殊スキル発動 now reads Skill Active; the matching 特殊能力発動
  banner reads Ability Active. Both visual variants of each are covered:
  FSSA widgets 0x9a914/0x9a934 and 0x9a954/0x9a974. Compact wording fits
  the existing banners without font, position, color or state changes.
- Screenshot 歌エネルギー is the already-pending Song Energy widget at
  0x9e354; it has not yet been built/installed. The executable occurrence is
  inside a separate bonus description, not a duplicate runtime label; no
  unnecessary partial-string hook added. Numeric value and meter untouched.
- song_deployment_labels now has 30 canonical entries and 26 UI bindings;
  its 19 exact executable hooks are unchanged. All four source/duplicate,
  sizing, isolation and current-.20-UI composition tests pass. Catalog has
  zero issues and all 543 compatibility views agree. No build or install.

## Unbuilt runtime weapon-warning correction (2026-09-25)

- Repeated screenshot report exposed an incomplete earlier fix: the fourteen
  AIDDATAPACK widgets were translated, but the executable rebuilds the live
  dim/highlighted checklist from a separate Japanese table. Constructor VA
  0x331088 loads table VA 0x869194 through TOC -0x1694; the loop copies the
  strings into eight 0x101-byte rows, then selects failure colors. Static
  widget checks alone could not detect this runtime replacement.
- Added canonical weapon_requirement_runtime (14 exact translations) and a
  source-guarded adapter covering all sixteen table slots: fourteen unique
  labels, duplicate Maximum Break and the unchanged dash placeholder.
  Includes Ammo, EN, Focus, Skill, Terrain, Range, Use After Moving, Combo
  Partner, Support Attack Use, Attack Again Use, Counterattack Use, Satellite
  Charge, Max Break Use and Other. Exact keys preserve trailing fullwidth spaces.
  The separate Song EN fixed-size copy uses the previous unbuilt batch's hook.
- Translate only at the final draw call; native Japanese buffers, pointer
  table, constructor, conditions and color/state selection are byte-identical.
  Added source-table/TOC/constructor guards and production binary-hook checks.
  Seven runtime-warning/activation regressions pass, including the whole EBOOT
  patched and verified in memory; 15,384 extension bytes remain after all
  extensions. Canonical validation zero issues. No build/install/publication;
  in-game confirmation is still pending after the next requested build.

## Unbuilt song/weapon and battleship-deployment labels (2026-09-25)

- User screenshots: 消費歌ＥＮ -> Song EN, 気力上昇 -> Focus Up;
  both battleship-list variants now use Ship / Aboard, and the split remaining
  deployment counter uses Left: with the native live number unchanged.
- Added shared song_deployment_labels catalog (28 entries). Category sweep
  covers Song Soul (compact stat label changed to Sng on September 26 after
  reported value overlap), all three Song headings, all three Song EN fields, Song
  Energy, Song Range +1, SP Recovery, Stats Up, Spirit Effects, five song types,
  song-list legends, four song-stat substitution help variants, Charges,
  Special/Beam Weapon and the trailing-space Post-Move variant. Existing
  translated effects such as Ignore Size and Focus Down remain unchanged.
- PS3 adapter: 19 exact draw-time hooks plus 22 explicitly bound FSSA widgets.
  Original executable offsets and every matching duplicate widget are checked.
  Deployment fragments are never global hooks. Only string pointers change;
  live numeric fields, selection state, positions, font sizes and colors remain
  byte-identical. Full strings are relocated, not squeezed into original slots.
  Song legend keeps its icon/colon prefix and uses compact Single to fit.
- Four focused tests pass, including application to original and current .20
  UI in memory, duplicate coverage, width limits and source-corruption refusal.
  Four activation/executable regressions also pass: complete current EBOOT
  patched/verified in memory, 16,048 extension bytes free after all extensions.
  Catalog zero issues; 543 compatibility views agree (no legacy view edits).
  Production UI build and issue gate include the new checks. No complete game
  build, install, version increment or publication; .20 remains installed.
  Vita executable/UI bindings and new in-game visual checks are not performed.

## 0.6.20 - approved screenshot fixes and complete PS3 build (2026-09-25)

- User approved applying the pending checks and building all accumulated fixes.
  Corrected Mikono's Shotaro reference to "looking after him" and the reviewed
  Mikage phrase to "my wish is fulfilled"; both preserve existing tokens.
- Bonus centering now uses the existing guarded centered-draw wrapper to measure
  the actual English font advance. Exact whitelist: 110 single-line bonus effects
  plus the full-upgrade lock message. Other strings and multiline descriptions
  retain the native path; no effects, numbers, colors or widget anchors changed.
  Source-bound pointer keys fit the existing cave without moving ELF segments.
  Complete strict build passed; visual runtime checks remain pending.
- Full-build preflight caught battle subtitles bypassing glossary expansion
  after the Igura normalization. Added a shared voice-document loader used by
  both atlas collection and subtitle encoding; Japanese/section/budget metadata
  stay unchanged. Regression scans all voice sections and checks token expansion.
  The failed attempt was not installed or numbered; retry uses a fresh output.
- Focused tests: nine ace/Igura and ten bonus/required-skill/activation checks
  pass. An additional 28-test mission/loader/deployment run has 26 passes and
  two historical-fixture failures: test_deployment_menu_text compares today's
  artwork/labels with work/out_0.6.3. No guards were weakened; the complete
  build separately checks newly packed labels and the full current art chain.
- Validated source build: work/build_0.6.20_english_20260925_r2. All production
  gates passed, including current deployment labels/artwork, 2,119 mission
  variants (zero missing), 5,394 executable hooks, subtitle readback, activation
  buffers and 12,900 centering cases. Includes the accumulated Igura, Ple Twelve,
  D-Trader ace-scene, activation and skill-confirmation edits below.
  Shared English fingerprint: 07034a88a4b70da975829c7d1242343d6f72907a366e56982b75e84b229d82ae.
  This is a local build, not a release.
- Dual-target package: work/ps3_hardware_0.6.20_20260925. Guarded two-LOAD
  original-metadata SELF round-trips through RPCS3 extraction. Preserved-layout
  ISO: 5,011,013,632 bytes; all 554 disc files verified in both filesystem trees.
  ISO SHA256: 6f6bdf5ec348fb31366f660095faa26f2628867adc6cd2ee7f4ee8f451c1ec77.
  Delivered SELF SHA256: 1fdfa8adde8c40bab523c440ae21bc6c31d4686fabb4eeca16779237fd021c8d.
  New-build hardware/RPCS3 runtime tests remain pending; preserved ISO layout
  is hardware-candidate, not hardware-confirmed.
- Installed the same derived snapshot into game/ after dry-run with RPCS3
  closed. All 219 installed hashes match; all 18 save files unchanged and other
  game registrations preserved. Recoverable game-file backup and receipt:
  work/install_backups/0.6.20_20260925_075836/. No install cache was present
  to move; the game creates it on next launch.
  No tag, GitHub release, upload or public catalog change performed.

## Unbuilt required-skill fix and screenshot checks (2026-09-25)

- Fixed the weapon required-skill family: the existing "Newtype L" translation
  matched only the standalone prefix, while the native composer appends a
  fullwidth level digit before drawing. tools/required_skill_levels.py derives
  ten exact hooks (L0-L9) from that canonical prefix, including reported L3.
  Native level values, conditions, colors and the fixed-size composer are not
  changed. Source prefix, pointer, load site and digit table are guarded.
  Added three regressions and a production check_issue_fixes gate.
- Seven required-skill / activation tests pass, including a complete in-memory
  EBOOT patch and verification. 16,696 bytes remain after all extensions;
  this supersedes the previous batch's 17,176-byte measurement. Catalog zero
  issues, 543 compatibility views agree, sync clean. No build or install.
- Screenshot translation CHECK only: stage0045_03:r_cdb750c9d380881a has
  "looking after her", but the preceding question identifies Shotaro; "him"
  is the supported correction. "Hung up on Gura" is acceptable here. The
  AI-assessed review/challenge is under work/mqm/shotaro_*_20260925*; the
  dialogue was not edited in that checking turn; the next user approval applies
  the confirmed correction in the 0.6.20 batch above.
  Report work/mqm/shotaro_report_20260925_v1: 80 rows assessed in both passes;
  two accepted linguistic defects (6 weighted penalties / 1,926 source
  characters), separate unresolved uncertainties retained. Provisional,
  not a whole-stage/game certification. An additional 11 bonus/name regression
  tests pass; these are rendering/tool checks, not linguistic scoring.
- Screenshot alignment CHECK only: both full-upgrade/custom-bonus descriptions
  are offset. The .19 bonus descriptors retain native centering (0x40); draw-time
  English substitution happens after the Japanese-width origin calculation.
  Using the current font and descriptor sizes predicts about +91 native pixels
  for the full-upgrade lock message and -137 for A.T. Field +400, consistent
  with the screenshot. No layout edits in the checking turn; approved centering
  follows in the 0.6.20 batch above. The cropped long unit name alone
  does not establish whether its runtime scrolling/clipping is defective.

## Unbuilt screenshot fixes - Iguras, activation and ace talks (2026-09-25)

- Corrected the reported Jin line to "Makes no sense, Rare Iguras!" in both
  stage0037_03 and stage0044a_03. Registered singular Rare Igura / Igura
  glossary terms and replaced 112 entries across 35 English groups with tokens,
  including dialogue, library and battle subtitles. Plurals stay outside the
  token. Also caught Rare Igler and Rea Iglar variants; the already-correct
  "Rare Igura" scenario title is unchanged. The mechanical migration is
  dry-run-first and idempotent (tools/normalize_igura_terms.py).
- Context review preserves singular references to individual people, uses
  plurals for the reported collective address and explicit Eve candidates,
  and fixes Kagura's two-route line from "about being Rare Iglars" to "about
  Rare Iguras": the source says they no longer care about them, not that
  Kagura and Mikage are Iguras. Existing Ple Twelve changes are preserved.
- Translated the complete D-Trader ace-congratulations category in previously
  omitted STG0500 member 1: 102 scenes, 1,247 records (941 dialogue and 306
  background markers), 918 unique source strings. Includes both Sousuke branches.
  Reviewed all records in 80-row slices with adjacent context; 343 occurrences
  reuse established translations and 904 are newly translated. Opaque AQ/AG,
  Fa/Faa-sama pork-cutlet and Zentradi pronunciation references are preserved,
  not replaced with invented lore. Registered canonical stage0500_01 and its
  PS3 build, extraction, deployment and patch layouts. Mission audit has an
  exact-family dialogue-only exception. The source SDAT matches the pristine ISO
  member byte-for-byte (SHA256 403479e0b60e90d8a3f492876bfd0dae63cb0d2ab2d83ba617fd1f48b251d4fa).
- Translated the complete adjacent activation-confirmation family: 17 strings
  through 18 pointers for Trans-Am, NT-D, both GAI variants and Tengen Toppa.
  Canonical activation_prompts also includes four dynamic skill-training suffixes
  (new skill, +1, upgrade, overwrite). The reported line becomes
  "B-Save will be learned." with the game's original quotation marks.
  Six exact-opcode-guarded fixed-size copies now copy through the terminator,
  retaining dynamic names/levels and the original two 256-byte buffers.
- Source checks: all 1,247 ace records pass identity, glossary, link and measured
  width validation; in-memory Lua replacement changes only text blocks, not scene
  commands. Catalog has zero issues, 543 compatibility views agree, and sync is
  clean. Regression tests are in tools/test_ace_and_igura.py and
  tools/test_activation_prompts.py. Combined 53-test translation/mission/name/link/
  loader suite and 20-test activation/menu/deployment/save suite pass. Full EBOOT
  patch and verification ran in memory only: 17,176 bytes remain after all
  extensions. All 215 centering cells are blank in both font layers; 12,900
  placement cases pass. New pads use 0x86E0..EF, not native icon row 0x85.
  First generated keyword helper moves 16 bytes within its existing cave;
  ELF segment and loader geometry are unchanged.
- Source-only follow-up to the published 0.6.19. No new game build, installation,
  version bump or publication; do not treat these changes as present in 0.6.19.
  Activation/copy-code integration is PS3-specific; Vita requires its own port.

## Unbuilt source fix - Ple Twelve (2026-09-24, after 0.6.19)

- Alberto's 「そして奴が後退した今、別のニュータイプを見つけて殺しにかかっている！」
  (sha a0d208378a; one copy in stage0037_04, two in stage0043_04) shipped as
  "And now that she's pulled back, it's found another Newtype and means to
  kill them!". 奴 has no gender, and from Alberto's side the pilot is only
  "that Enhanced Human", so at the user's suggestion it now says "they've
  pulled back". The ending became "and is going for the kill!", which is
  closer to 殺しにかかっている, so a second "them" can't be read as the same
  person. check_stage: 0 problems in both stages.
- Checked, not changed: its preceding line is spoken by アルベルト, but the
  original data gives it Reyam's portrait (pid_REYAM) in every copy. The
  speaker field is translated, not the portrait.
- The user flagged Frontal's 「プロト・プル・トゥエルブ…。」 shipped as
  "Proto-Pull-Twelve..." (stage0037_03 and stage0043_03, 4 records, sha
  d8b434e064). プル is Elpeo Ple's line of clones: Marida Cruz is **Ple
  Twelve** in the Gundam wiki and other references (BASE_RULES: the wiki
  wins). The line is now "Proto Ple Twelve..."; its accurate second line is
  unchanged.
- Marida's library bio (library.pt_120) said "Puru Twelve, the twelfth of
  the Puru series" and now says "Ple". No "Puru" or "Pull" rendering
  remains in the corpus.
- Catalog 0 issues; three views regenerated; 542 compatibility views.
  Takes effect in the next build.

## 0.6.19 - GitHub release (2026-09-24)

- Published as Latest on the user's request at 2026-09-24T08:36:48Z:
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.19 (the repository
  is private). Tag `v0.6.19` is at `05f4b46`, which is build source `424cb7d`
  plus the release notes. The manifest's source_commit is `424cb7d`.
- Assets (Retro Trans v0.2.1, both routes round-trip verified):
  - `SRW-Z3-PS3-English-0.6.19-from-original.xdelta`, 154,473,883 B
    (e04fc4ad...4498d563... see SHA256SUMS)
  - `SRW-Z3-PS3-English-0.6.18-to-0.6.19.xdelta`, 20,946,242 B
  - `BUILD-MANIFEST.json`, `SHA256SUMS.txt`, `VALIDATION.json`
- Uploaded as a draft first. All five remote names, sizes and SHA-256
  digests matched `work/retro-trans/ready_0.6.19` before publishing.
- The notes are `docs/releases/0.6.19.md`. They name what is still Japanese
  (preset team names, the opening-movie series cards) and say the preserved
  disc layout has no hardware boot report. PS3 only; no game files were
  uploaded.

## 0.6.19 - build, hardware package, installation (2026-09-24)

The user explicitly asked for a release. The source is `9010eaa` plus the two
build fixes below, which are committed with this entry.

- **The first attempt failed** (`work/build_0.6.19_english_20260924`) in
  `unlock_reports`. Its assertion had no message, so the retry
  (`..._r2`) was used to make it report its cursor: file 0x8f0000, the end
  of the EBOOT extension. The UTF-8 labels and the unlock notices are placed
  *after* the hook strings in that same unchanged extension. The 3,466 bytes
  this batch had left only counted the hook table; those later tenants needed
  more.
- **Fix, `eboot.name_hook`:** the hook strings used to start at the fixed
  `NAME_STR` mark, after a 64 KB reservation for 8,191 table entries, of which
  5,383 are used. They now start right after the largest table this run can
  emit (every candidate key plus the terminator), capped at the old mark.
  About 22 KB comes back: **25,958 bytes** are left after the hook strings.
  EXT_VA / EXT_SIZE and the LOAD geometry are unchanged. The table-fit check
  now compares against where the strings actually start, and
  `check_issue_fixes` reads the table back and asserts that no hook string
  overlaps it. `unlock_reports` now says where it needed space and what was
  there.
- Build `work/build_0.6.19_english_20260924_r3`, strict (no partial flag):
  `translation_complete: true`, 0 untranslated mission variants, 142 stage
  archives, 5,383 hook entries. Shared content e11e7579845e2a2eb7a059c0107bf23b6ebdf62072479ec2eba0df5f1d4402ee
  (1192 files). Every new gate check passes: 85 Team Setup / Sub Orders /
  Custom Bonus widgets, 236 bonus descriptions, the operation indent.
- Hardware package `work/ps3_hardware_0.6.19_20260924`, preserved layout,
  dry-run then write:
  `SRW-Z3-English-0.6.19-hardware-test1.iso`, 5,010,685,952 bytes, SHA256
  8b4a32671862073d5c2097fc19b91fe47046659f972d7b0b43d2065c8d9935e4, MD5
  415c61e5be4d77de3142225b3da6e9e1. SELF 58d8fa6c4f2c8cbc81138121adc233dd0d814279cae0f0d8ac3daa0966571e6a;
  raw ELF afa71374efd5642c801e5b688b3b2174056b079fa35e080db40b80141046c730.
- Installed into `game/`: 218 hashes match, 18 saves unchanged, backup
  `work/install_backups/0.6.19_20260924_152642`. Snapshot `releases/0.6.19`,
  manifest `releases/0.6.19.json`.
- Not runtime-tested. The preserved disc layout still has no hardware boot
  report.

## Unbuilt source fixes - Team Setup, Sub Orders, bonus descriptions, Guren Mk-II (2026-09-24)

These come from the user's screenshots of 0.6.18. Source only; nothing is built.

- **Team Setup and Sub Orders screens:** new `tools/team_order_labels.py`. Its
  wording is in the catalog as `ui_aiddata:team_order_*` (79 entries), and it
  binds 85 FSSA widgets in AIDDATAPACK member 0. Both screens were mostly
  Japanese; only strings some other family happened to hook came out English
  (hence "Change Pilots / Transform / 並び替え / チーム名称"). Rows that an
  existing content hook already translates are left alone. Four kinds of
  binding:
  - **Labels** are repointed.
  - **Blanks:** split phrases (パイ+ロット：, バランス+オーダー) keep the English
    whole in the first widget and set the rest to empty.
  - **Accents:** coloured fragments (自動で編成, 任意のチーム, 全チームの名称,
    自動更新, カスタムボーナス) move to the measured position of their English
    substring, using the weapon_requirements method. The overlapping "Custom
    Bonus" in the screenshot was that accent still sitting at its Japanese
    centre.
  - **Gaps:** templates where another widget draws a live number (PP/kills/
    EXP/funds results, ＜あと　人＞, ＜残り　　隊＞, 【自動名称／チームソート】)
    keep the same full-width gap, moved so it starts exactly where the Japanese
    gap did. The number widgets are untouched.
  - Eight runtime copies drawn from the EBOOT (名称を変更しました。,
    マークしたチームの名称を変更します。, the auto-order message, ：つかむ/：おく/
    ：もちかえ, 移動/交換モードへ) are exact draw hooks.
  - Wording follows what already shipped nearby: "Diamond Force" (voice
    corpus), "Deploy" family, ": Move mode". Undrawable `~` and `<` became
    the font's full-width `～` and `＜＞`.
  - While checking this I found that a widget record spans `[row-8, row+0x18)`:
    pointer, x at +0xc, size at +0x1b, centring flag at +0x1f. The test for
    untouched number widgets checks the next record with that layout.
  - Wired into `build_ui`, `eboot.load_ui_hook` and `check_issue_fixes`.
    `tools/test_team_order_labels.py` has 7 tests.
- **Bonus descriptions:** new catalog group `bonus_descriptions` (236 entries,
  keyed by EBOOT VA) and `tools/bonus_descriptions.py`. The executable's
  Ace / Custom / Full Upgrade bonus table (VA 0x709668-0x70c4c8) had no hooks,
  so every bonus effect drew in Japanese. A translation agent wrote the English,
  taking names from abilities/skills/spirits/weapons/parts.json and shipped UI
  majorities, and measured every line against its Japanese. I reviewed all 236.
  I changed 気合 to "The Spirit command / becomes Spirit+." (the agent's version
  read "Spirit command Spirit") and 未取得 to "None" ("Locked" did not fit in
  84 px). The fragment 武器の射 is left out.
  - **Extension space:** with per-line pairs and copied Japanese keys, these
    needed 10,378 bytes more than the unchanged EBOOT extension holds
    (test_mission_conditions caught it). They now opt out of line pairs, as the
    parts and skill description tables already do, and are
    `eboot.UI_ELF_RESIDENT`: their keys point at the Japanese already in the
    ELF instead of owning copies, because no build step patches that table.
    `check_issue_fixes` reads every key back.
  - The overflow message now reports how far over it is.
  - Totals: 5,383 of 8,191 entries, 0 skipped, **3,466 bytes left**. The
    extension is nearly full; the next large hook batch needs a different home.
  - `tools/test_bonus_descriptions.py` has 4 tests.
- **Post-save (end-session) scenes: all of STG0700 translated.** The user
  reported a Japanese line from Kan Yu after saving, spoken with a voice clip.
  STG0700 has 94 scenes and 872 records. Only 16 had ever been translated
  (`suspend_scene.py`'s partial patch, 2026-09-11); the other 573 speech
  records were Japanese.
  - The lines are voiced because they are battle-voice lines, so 413
    (normalising line breaks and indents) reuse that clip's shipped voice
    English, rewrapped into dialogue format with the corpus speaker form. When
    the same Japanese has several voice renderings, the speaker's own voice
    file wins.
  - The 16 shipped lines are kept as they were; for 13 of them the voice
    English would have differed.
  - The remaining 129 lines, including one thought line, were translated by
    three slice agents from the standard briefs. Everything passed
    `check_stage` with 0 problems: 872 records, 559 answers, no merge
    conflicts.
  - Cross-slice reconciliation: the game's own title is written unquoted
    ("Super Robot Wars Z3", as the voice lines and the prefill have it; one
    slice had quoted it four times), and a two-mark 「……」 uses the corpus
    nine dots.
  - `tokenise_stage` tokenised 68 records, round-trip safe; `check_names`
    found 0 suspects.
  - Registered as catalog group `stage0700_01`; 542 compatibility views.
  - `特殊背景` (282 records) is the location label of background 185, and no
    location window is drawn for it. It is kept byte-identical.
  - Build path: STG0700 is now an ordinary manifest stage (142 containers,
    61,525 dialogue records). `build_project` no longer calls
    `suspend_scene.build`, and the two gates no longer call its check. The
    module stays for the frozen 0.6.14 builder and its tests (5 pass).
  - **Found on the way:** `E:/SRWZ3/.../STG0700.SDAT` is a patched copy from
    an old English install, with no `.orig` beside it. `prep_stage` extracted
    it, and its `errors="replace"` decode hid the problem. It now decodes
    strictly and refuses a non-pristine script with an explanation. STG0700
    was re-extracted from the hash-pinned `work/orig/STG0700.SDAT`. All 645
    other extracted scripts in `work/lua*` decode as pristine cp932.
  - `platforms/ps3/localization/legacy.json` was normalised to the canonical
    dump layout (18 compact rows from the mission-condition batch; parsed JSON
    identical), because the registration tool refuses to reformat rows
    silently.
  - Flagged, not changed: one reused voice line renders ひらめき as "Flash"
    while `spirits.json` says "Alert". That comes from the shipped voice
    subtitle; review it with the voice corpus.
- **Spirit command names now follow Akurasu (user's decision).** Checked
  against [Akurasu's Z3 Spirits page](https://akurasu.net/wiki/Super_Robot_Wars/Z3/Spirits):
  11 of 13 names already matched, including 閃き = Alert. Two were shifted
  by one: **不屈 Persist → Wall** and **鉄壁 Wall → Guard**.
  - Every change was decided by the entry's Japanese source, not by English
    find-and-replace. The Berlin Wall, "No Wall", "Persistent!", Brocken's
    "unbreakable man" and the voice lines' "iron guard" stay as they are.
  - The Miracle Fragment's spirit list is English-only. Akurasu's parts table
    names 鉄壁 in it, so its "Wall" became "Guard".
  - 21 entries changed: spirit names and their + forms, the combined-spirit
    description, 8 parts-description rows (hook and unshipped copies), 2 bonus
    descriptions, and the one "Flash" outlier (voice_111, Tessa: "No! Use
    Alert to escape!") together with its STG0700 reuse.
  - Tiny battle-preview abbreviations: 不屈 Pe → **Wa**, 鉄壁 Wa → **Gu**.
    CONVENTIONS.md records the rename for future slices.
  - Tests: test_parts_descriptions' Miracle Fragment list now expects
    "Guard". Its frozen-0.6.3 comparison maps the rename back.
  - Its "exactly 300 hooks" check had been failing since the mission batch,
    because module families are always appended to the hook table. It now
    proves directly that the part descriptions add no line fragments.
  - `audit_message_classes` recognises STG0700 as dialogue-only.
  - Passing: parts 6, mission_conditions 11, bonus 4, battle_screen_labels
    11, team_order 7, save_quit 5.
- **Second line of numbered mission conditions stayed Japanese.** The user's
  Episode 25 screenshot shows "1. Within 4 turns, have Nahel Argama reach the
  nearer point" over a Japanese line 2. Both line hooks were in 0.6.18, and
  the 0-untranslated audit was right about the catalog. But when a stage
  numbers its conditions, the game draws each line separately: "１．" + line 1,
  then "　　" + each further line. The executable's pointer table at 0x7c8594
  holds １． ２． ３． and the 　　 indent. No key ever had the indent, so
  every numbered multi-line condition showed its continuation in Japanese.
  - Hooking the indented forms would have cost about 10 KB of the 3.5 KB left.
    New `tools/operation_indent.py` instead blanks the indent string (4 bytes).
    Only that table references it, and the bytes and pointer are verified
    before writing.
  - Continuation lines now match their existing hooks. All 85 distinct
    continuation lines across both mission sources are hooked.
  - Cosmetic cost: an English continuation starts under "1." rather than
    under the text after it.
  - Wired into the EBOOT patch chain and `check_issue_fixes`;
    `tools/test_operation_indent.py` has 3 tests.
- **Guren Mk-II:** Asuka's line (stage0042_03 `621b64699b`) shipped 紅蓮弐式 as
  "Guren Nishiki". The user asked for "Guren Mk-II"; it is the only occurrence,
  and it is not a glossary term.
- **Not done, needs a decision:** the opening movie's series-name cards
  (機動戦士ガンダムＵＣ etc.) are burned into `DATA/MOVIE/SRWZ3OP_TITLE_0107.USM`
  (410 MB CRI Sofdec). Nothing in the project edits movies yet.
- **Not found yet:** the preset team names (宇宙の王者, 螺旋の男, ＭＳ隊, グレン団,
  デ・ダナン隊, 超時空世紀, エヴァンゲリオン). They are not plain text in the
  EBOOT (cp932/UTF-8/UTF-16/EUC), in any decompressed CPK under 40 MB, or in
  the Lua scripts. 隊 alone is a composition suffix at 0x70e9d8. They may be
  stored in the name-entry character encoding. Names already saved in a
  playthrough would stay Japanese until renamed or auto-updated, even once
  the source is found.
- Checks: catalog 0 issues; sync regenerated only
  `translation/stage0042_03.json` (one record, plus the usual re-indentation);
  541 compatibility views. These tests pass: team_order 7, bonus 4, name_entry
  4, mission_conditions 11, battle_screen_labels 11, ps3_link_identity 6,
  battle_name_rendering 7, dialogue_halfwidth 5, preserved_iso 4.

## 0.6.18 - GitHub release (2026-09-23)

- Published as Latest on the user's explicit request at 2026-09-23T03:07:41Z:
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.18 (the repository
  is private). Tag `v0.6.18` is at `8feaf49`, the commit containing
  `preserved_iso.py`, which built the target ISO. The Retro Trans manifest was
  rebuilt with that `source_commit`: the first run named `1da624b`, which
  predates the packager. The patch bytes are identical across both runs.
- Assets (Retro Trans v0.2.1 standard, both routes round-trip verified):
  `SRW-Z3-PS3-English-0.6.18-from-original.xdelta` 154,462,906 B
  (e08c40dc...4b34854), `SRW-Z3-PS3-English-0.6.14-to-0.6.18.xdelta`
  28,467,132 B (b2deb97a...2e2cb98), `BUILD-MANIFEST.json`, `SHA256SUMS.txt`,
  `VALIDATION.json`. It was uploaded as a draft first. All five remote names,
  sizes and SHA-256 digests matched `work/retro-trans/ready_0.6.18_r2` before
  it was published. The notes are `docs/releases/0.6.18.md`.
- PS3 only. Vita and save-tool assets stay on v0.6.14, and the notes link to
  them. No game files or ISOs were uploaded.
- The notes say plainly that the preserved disc layout has no hardware boot
  report and that the build has had no gameplay test on either target.

## PS3 hardware disc keeps the original layout, so the xdelta stays small (2026-09-23)

- The first release-builder run for 0.6.18 had written a **3.1 GB**
  original-to-0.6.18 patch when I stopped it. That is over GitHub's 2 GiB
  per-asset limit; the published 0.6.13 full patch was 149 MB. Cause:
  `package_hardware_current.py` rebuilt ISO9660/Joliet from scratch
  (`cfw_diagnostics.write_image`, pycdlib), so almost every file moved.
  xdelta only matches within a limited window of the source, so it stored
  the moved data as new.
- The rebuild was never needed to fix the hardware defects recorded in
  `CFW_TEST.md` (stale region table, stale UDF tree, plain ELF). New
  `platforms/ps3/preserved_iso.py` keeps the original disc byte-for-byte and
  appends the 218 changed files. It repoints both trees and checks each old
  record against the source inventory first. It zeroes the UDF recognition
  sequence, both anchors (256 and N-1) and the main and reserve descriptor
  sequences, after proving none of those sectors belongs to ISO9660 data. It
  then runs the same `stamp_disc` / `verify_disc_header` as the fresh writer.
  Verification re-reads all 554 files through each tree and confirms UDF is
  no longer discoverable.
- It is now the default. `--fresh-layout` keeps the old writer, which is the
  layout of the user-confirmed 0.6.15-hardware-test1.
  `tools/test_ps3_preserved_iso.py` (4 tests) builds a synthetic pycdlib
  ISO9660+Joliet+UDF disc and checks the append and repoint, that UDF is gone,
  that unchanged bytes stay in place, the single-region header and the refusal
  to overwrite.
- 0.6.18 repackaged into `work/ps3_hardware_0.6.18_preserved_20260923`:
  `SRW-Z3-English-0.6.18-hardware-test1.iso`, 5,010,685,952 bytes, SHA256
  0ed6c63a3a330de6c263611726b9df3830b9f288c388305bb4e957e7600dfe83. Its
  `snapshot/` is identical file-for-file to the fresh-layout package, so the
  installed game and `releases/0.6.18` are unchanged. The fresh-layout ISO
  (e44b8130...) remains in `work/ps3_hardware_0.6.18_20260923`.
- **The preserved layout has no hardware boot report yet.**

## 0.6.18 - English build, hardware package and installation (2026-09-23)

The user explicitly asked for a 0.6.18 GitHub release. This build contains
every unbuilt source batch below: Stage 31B/32 screenshot fixes, all mission
conditions, the Space Demon King Soldier name, sword help, Fa and name entry.

- Build command as for 0.6.17, without `--partial-translation`: the strict
  audit now passes. Output is `work/build_0.6.18_english_20260923_r2`
  (log alongside). The first attempt failed at the stale hook-capacity check
  (next entry) and used up no number. The manifest records
  `translation_complete: true` and `untranslated_mission_variants: 0`, which
  is mission-condition coverage. Eleven non-story scripts
  (STG0400/0401/0500/0501/0600/0700/0901/0903/0904/0905/0999) are still
  untranslated. Shared content caf2f98c7b670eba3e1033e65031cdda37aaf937980656080acc897a58a671d8
  (1188 files). Footer v0.6.18; 5139 hook entries.
- `package_hardware_current.py` dry-run then `--write` into
  `work/ps3_hardware_0.6.18_20260923`. Two-LOAD fold, original-metadata
  fake SELF and ISO9660/Joliet checks all pass.
  `SRW-Z3-English-0.6.18-hardware-test1.iso`: 4,752,932,864 bytes, SHA256
  e44b8130c1f7619b99750701dfd11886a199a7bf9a36e2c26cdba20e6a275d57.
  SELF b3bc066b39b69adff7fd59c849b14bb8754c4c306c549aa1ecd791b953799554;
  raw ELF b532dd3c74b73ee452ddaabf6744d8c0dbeb91133037919eccec18bbed820581.
- The derived `snapshot/` was installed into `game/` (dry-run, then `-Write`)
  with RPCS3 closed. All 218 hashes match, the 18 save files are unchanged,
  and the backup is at `work/install_backups/0.6.18_20260923_091143`. The
  BLJS10256 registration was already `game/`.
- Snapshot `releases/0.6.18` (218 files, ignored). Hash manifest
  `releases/0.6.18.json` is committed.
- Not yet runtime-tested by the user on RPCS3 or hardware. Mission-screen text,
  the Episode 19 conditions and the September 20/22 fixes still need in-game
  checks.

## Build gate: hook-table capacity check follows the table layout (2026-09-23)

- The first 0.6.18 build attempt (`work/build_0.6.18_english_20260923`)
  failed in `check_issue_fixes.py` at `assert len(entries) < 4096`. The
  mission-condition work below raised the name-hook table to 8191 entries and
  emitted 5139, but the gate still asserted the old limit. That work updated
  the builder but not this check. The failure happened before numbering, so
  no version was used up.
- The check now takes its limit from `eboot.NAME_STR - eboot.NAME_TBL` (8-byte
  rows plus the terminator). It also asserts that the terminator falls inside
  the table's region, so it is stricter than the old constant: a future
  repartition cannot overrun silently. On the failed output, the rest of the
  gate passed (1865 batch hooks verified across 5139 entries). The complete
  build was then rerun into a NEW directory.

## Stage 31B proofreading fixes from playtest screenshots (2026-09-23)

Records in stages 31B (Operation Yashima) and 32, reported from in-game
screenshots and edited in `localization/locales/en/` (status `translated`):

- `1de198ce72` Shotaro: "I can't finish it off!" -> "That won't finish it
  off!". 仕留めきれない has no subject; the line comes right after Shinji's
  positron shot, and Sosuke's reply ("No good! ...off the core") shows that
  Shotaro means the shot, not himself. The first version made up an "I" and
  made him sound like the one who failed.
- `a02969bfb5` Sosuke: "It's slightly off from the core!!" -> "The shot's
  slightly off the core!!". Same meaning, reads less stiffly, and ties into
  the line above.
- `c8326238c8` Kurz (two copies of the scene): "You're right in Shiny's line
  of fire!" -> "...that shiny thing's line of fire!". テカテカ is a nickname
  Kurz makes up for Ramiel. Capitalised with no article, it read like the name
  of a character nobody had introduced. Wattа's テカテカ怪獣 in the same stage
  already shipped as lowercase "shiny kaiju".
- `1577162364` Rei: "set to launch tomorrow at 0000 hours" -> "tomorrow at
  midnight". 午前０時 is plain Japanese for midnight, not military jargon; the
  user chose this wording.

Two more records from the same kind of report, in stage 32 (`stage0032_03`):

- `1b137a6899` Tessa: "I'm... / 'Kyoshu'... submarine, was it? / Its
  captain, a colonel, Sousuke's superior, right?" -> "I'm the captain of... /
  an 'assault'... submarine, was it? / And a colonel, and Sousuke's superior,
  right?". キョーシュー is 強襲 ("assault") written phonetically: she is
  reciting a cover story she half-remembers and trips over the jargon. Kept
  as romaji, it read like the ship's name. Restored the Japanese order (I'm
  its captain, a colonel, his superior).
- `3994f1d24e` Tessa: "Captain...?" -> "Colonel...?". She repeats Sosuke's
  「大佐殿？」, which shipped as "Colonel?". The joke is that she doesn't
  recognise her own title, and it only works if she repeats the same word.

Checks: `localization.py check` found 0 issues. `sync --write` regenerated
only the three touched views (`stage0031b_03`, `_04`, `stage0032_03`): a JSON comparison
against HEAD shows only these seven records changed; the rest of the diff is
2-space re-indentation. `check --compatibility` passed 541 views, and the
longest new line is 734 px against the 963 px limit. Source only: no build.

## Unbuilt source completion - mission conditions (2026-09-23)

- Episode19 "Bonds That Connect" uses STG0031B, outside the earlier archive
  1-30 translation scope. The English0.6.17 entry below accurately describes
  that shipped build's1034 untranslated mission variants; they are now covered
  in source, not retroactively fixed in the installed build.
- Added180 missing complete victory/defeat/SR Point strings to the shared
  canonical mission_conditions_all catalog, with exact archive/string-index
  provenance and condition roles. All259 unique extracted conditions now have
  English. The expanded source/display/numbered/per-line audit validates2119
  variants across142 archives with0 missing (inventory also includes UI labels).
  Episode19 correctly retains turn5, the Sixth Angel, the four protected pilots,
  and reducing HP to20,000 within4 turns. Other objectives preserve deadlines,
  HP thresholds, turn phases and named participants; script checks confirm
  Kouji OR Zeus being shot down causes defeat, not only both together.
- Added12 canonical glossary aliases for faction, location and abbreviated
  unit labels using existing project spellings. Peace Memorial Hall is backed
  by local scene records. Mechanical Beast stays singular for the shared enemy
  label; mission pluralization is outside its glossary token. Regenerated only
  analysis/glossary.json among the541 compatibility views.
- Added a read-only source catalog scanner with explicit export mode. General
  CP932/Lua display escape handling now covers more than the old Point special
  case. Checked shared-line mappings reject conflicting translations and fix
  generic fragments that previously inherited unrelated English. Source line
  counts, expanded terms, condition roles and rendered widths are checked.
- Complete coverage exceeds the old4095-entry draw table. Increased its space
  to8191 entries within the SAME extension and interned identical fully encoded
  English strings, including padding/tutorial punctuation. Japanese lookup keys
  remain separate. EXT address/size and loader segment geometry are unchanged;
  focused tests rebuild only the table in memory, not a runnable game package.
- Validation:52 focused mission, partial-build, battle-name, link/UI and loader
  tests pass. Production-style name inputs emit5139 table entries with0 skipped
  and22,088 bytes remaining inside the unchanged extension. Canonical validation
  and all541 generated compatibility views pass; runtime checks remain pending.
- Source only: no game build, installation, version bump, ISO or publication.
  The PS3 hook adapter consumes the shared catalog; no Vita executable changes
  or Vita runtime verification are implied. Previous unbuilt fixes are retained.
  Visual and runtime validation awaits the next explicitly requested build,
  using the proven PS3 hardware+RPCS3 packaging path.

## Unbuilt source fix - Space Demon King Soldier name (2026-09-22)

- Screenshot shows the battle speaker cut to "Space Demon Kin" with corrupt
  trailing glyphs. Canonical text is already "Space Demon King Soldier"
  (enemy_names:r_50e87a2fb9246781); all12 pilot-nw references at RPW string
  index3521 also contain the full English in frozen0.6.17. No wording change.
- Extended the existing PS3 deferred-name candidate to 宇宙魔王兵: preserve
  its10-byte native key through name handling, then use the exact draw hook
  for the full English. Now70 references covered across three reported names.
  Distinct joined labels Space Demon King and Space Demon Army are unchanged;
  no prefix match, guessed buffer patch, abbreviation or Vita offset port.
- Twenty-eight focused tests pass: all12 references, original/full stored
  text, RPW isolation, actual PPC hook with modeled short-copy boundary,
  caller/source preservation, exact-match isolation and existing link/UI
  regressions. The native truncation site remains unconfirmed; this is a
  candidate pending an affected-battle test, not a runtime-confirmed fix.
- No build, install, version bump or publication. Previous unbuilt fixes
  remain pending alongside this change.

## Unbuilt source fixes - sword help, Fa and name entry (2026-09-20)

- Translated the PS3 sword-icon Unit Data Help, preserving its two lines,
  final newline and conditional parry meaning. Added the exact source-guarded
  UTF-8 reference to the existing relocation and packed validation paths.
- Corrected Fa's episode28 member3 event t_1 row253 from "that girl" to
  "that guy". Reviewed rows238-264: she refers to Issei Tsubaki after his
  manager request to Kaname, not Kaname. Tokens and line breaks unchanged.
- Added24 canonical name-entry labels/help messages: Rename Squad, Space,
  Delete, Auto, Reset, Confirm, character-set category names and explanations.
  Compact "ABC / 123" fits the letters/numbers category button. Selectable
  kana/kanji/alphabet/symbol grids and entered/preset names remain unchanged.
  Source-guarded AID pointer replacements and exact runtime hooks preserve
  native coordinates, sizes, flags and input behavior; no executable offsets
  copied to Vita. Fa's shared dialogue correction is platform-independent.
- Fifteen focused in-memory tests pass, including existing battle labels,
  sword relocation, palette isolation, source guards and exact-hook loading.
  Name-entry patch also passes against frozen English0.6.17 UI. Fa's target
  passes token/link/encoding/width checks. Canonical validation:0 issues;
  all541 compatibility views pass. Sync changes only the stage0028_03 view
  (generated JSON formatting normalized; one semantic dialogue correction).
- Source only: no new game build, install, ISO, version bump or publication.
  Runtime appearance still needs checking in the next requested build.

## 0.6.17 - English name/quote build, hardware package and installation (2026-09-19)

- Built current English source on explicit request, including both batches
  below. Preflight and full packed/UI checks passed;40 focused/packaging
  tests passed. Canonical compatibility:0 issues,541 views. Translation
  remains partial, with1034 untranslated mission variants documented.
- Confirmed the new font mapping is identical to frozen English0.6.16.
  Built episode25 member3 differs only by132 removed malformed quote bytes.
  Fourth Angel/Neo Zeon storage and exact draw-hook checks passed; the
  affected-battle visual result still needs testing. Mariemaia remains open.
- Packaged using the guarded two-LOAD/fake-SELF method, verifying RPCS3
  extraction and554 files in both ISO9660/Joliet trees. Hardware ISO:
  work/ps3_hardware_0.6.17_namefix_20260919/SRW-Z3-English-0.6.17-hardware-test1.iso.
  Size4752932864; SHA25660350a8c9715908541db11b4715d6f67a5b223ecba041fb2f33aa9627b082dfa.
- User explicitly chose English installation over the Vietnamese test.
  With RPCS3 closed, dry-run then approved installation of the derived
  snapshot passed:218 target hashes and complete disc verified,18 save
  files unchanged. Registration now game/; other games unchanged. Previous
  files backed up at work/install_backups/0.6.17_20260919_161343. No cache
  existed to move. Preserved previous Vietnamese and English outputs.
- Installed SELF SHA256832b5721db1346d25029dabf52164bb26614e7833f2039c6f2da2fd7347214d1
  matches the ISO package. Install receipt copied into hardware output.
  No gameplay launch/runtime confirmation, Vita build, xdelta or publication.

## Source batch included in 0.6.17 - Fourth Angel name workaround (2026-09-19)

- Added a PS3 source candidate for the reported Fourth Angel and Neo Zeon
  Soldier corruption. Keep their short original RPW strings through native
  name handling, then select the complete canonical English in the existing
  exact-match draw hook. No abbreviation, translation edit, speculative
  buffer enlargement, new executable instruction patch or Vita offset port.
- Source RPW indices1778/4205 cover58 references (Fourth Angel10, Neo Zeon48).
  Filter both normal swaps and per-record overrides before packing; retain
  Japanese glyph reservations and explicitly pool the English hook letters.
  Build checks require short native names plus full exact-match hook entries.
- Six focused tests pass: actual emitted PPC hook returns full names after
  a simulated31-byte copy, preserves caller state/source memory, leaves
  unrelated/suffixed names alone, keeps unrelated RPW slots byte-identical,
  rejects changed source, and rejects frozen .16 at the new RPW gate.
  Existing10 battle-label,5 quote and6 link-identity tests also pass.
- The precise native truncation site remains unconfirmed; the copy test is
  a model of the observed boundary, not a runtime reproduction. This is an
  unbuilt workaround awaiting the affected-battle test, NOT a confirmed
  on-screen fix. Mariemaia Soldier remains unresolved: its Japanese key
  shares a joined squad label translated as plural "Mariemaia Soldiers";
  preserve that separate behavior instead of globally overwriting it.
- Read-only investigation helper: work/trace_battle_name.py. The separate
  UTF-8 battle table at VA0x85d410 is accessed through TOC-0x62d8, initialized
  near0x1050c0; no speculative modification to its consumers. No complete
  build, installation, version change or publication performed.

## Source batch included in 0.6.17 - Episode 25 dialogue fixes (2026-09-19)

- User confirmed the five new screenshots are from 0.6.15, not a new .16
  runtime report. Matched Alto, Watta, Ryouma and C.C. to stage0025_03,
  event t_1 rows363-367. Found the same malformed content in frozen .15/.16.
- Removed redundant half-width corner quotes from 66 canonical English
  entries in that member. These were accidental nested wrappers around the
  normal full-width quotes; Japanese source has no corresponding nested
  quotes. U+FF62/U+FF63 emit single CP932 A2/A3 bytes into the two-byte glyph
  stream, explaining the shifted glyphs, blank first lines and stray text.
  No prose, glossary tokens, links, controls or record identities changed.
- Added a hard rejection of U+FF61..U+FF9F in the shared PS3 text tokenizer,
  covering letter, pair and hybrid encoders and the stage checker. No silent
  substitution. Source catalog scan found only those66 rows; none remain.
  Added five regression tests, including in-memory repacking against both
  frozen builds: exactly132 extra quote bytes removed, all other member
  bytes identical. All60,653 stage records pass the updated tokenizer.
- Full affected-member check:966 records,803 unique answers,zero problems
  including measured widths. Canonical check zero issues;541 views match.
  Exactly one generated view exported after a66-row quote-only diff review.
  All15 half-width/battle-label tests pass.
- Mariemaia Soldier is a separate unresolved runtime name-cutoff report,
  matching the earlier roughly15-letter failures. Extended the frozen RPW
  test to verify its full translated name too. Static32-byte copy candidates
  remain unproven as the actual nameplate path; no speculative buffer edit
  or shortening. Requested a save/precise battle reproduction.
- No build/install/publication performed by this task. During read-only
  checks, game/build_manifest.json identified a separate Vietnamese0.6.17
  story-test installation; left it untouched and used frozen English builds
  for regression checks. The English .16 package remains preserved.

## 0.6.16 - Local dual-target build and installation (2026-09-19)

- User resumed the build after the Toji fix. Built the current canonical
  translations and all five September 19 source-fix batches documented below:
  battle labels/names/help, Stage 17 and 19 jokes, and the Berserk cut-in.
  Their earlier no-build notes describe the source-edit sessions, superseded
  by this build and installation. Long battle-name corruption remains unresolved.
- Input dry-run passed (141 stage containers, 60,653 dialogue records,
  687 checked paths). Complete packed/UI regression gate passed, including
  Toji/Misato/Tetsujin references and Berserk sprite isolation. Title footer
  and build counter are 0.6.16. Translation remains partial: 1,034 untranslated
  mission variants are recorded, not hidden or counted as translated.
- 70 focused tests passed, plus the three affected Stage 17/19 member checks.
  Packaging test imports initially needed the PS3 module path; the corrected
  test invocation passed. Font mapping is identical to the confirmed .15 build.
- Hardware packaging dry-run and write passed using the required guarded
  two-LOAD layout, original-metadata fake SELF and RPCS3 extraction check.
  All 554 members verified in both ISO9660 and Joliet. Local ISO:
  `work/ps3_hardware_0.6.16_test1_20260919/SRW-Z3-English-0.6.16-hardware-test1.iso`
  (4,752,932,864 bytes), SHA256
  `d572a2a238e0fe12ac4c4c66a504921e996daf9f167568bbdcfe9931107c0fe6`.
- Installed the derived hardware-compatible snapshot, not the raw ELF,
  into `game/` after installer dry-run and write with RPCS3 closed. All218
  game-file targets and the complete disc verified; all8 save files unchanged.
  Registration switched from the old .15 ISO to `game/`; other games preserved.
  Old files/cache retained at `work/install_backups/0.6.16_20260919_113739`.
  Installation receipt also copied into the hardware output directory.
- Confirmed .15 hardware baseline preserved. New .16 boot/gameplay is not
  runtime-tested on either target yet. No Vita build, xdelta, tag, release,
  upload or publication performed.

## Source fix - Toji battle speaker name (2026-09-19; included in 0.6.16)

- Held the requested build when the user reported Toji's name remaining
  Japanese during battle in scenario 13, when he enters the Eva. No build
  had started. Exact reported build and scene have not been reproduced.
- Confirmed the separate UTF-8 battle-name entry is still Japanese in the
  frozen .15 executable. Added its missing binding to the existing canonical
  glossary entry `glossary:r_0de2d941a5560480` (Toji), not a duplicate translation.
  Guarded source VA 0x6ed118 and sole table reference 0x84e1c8. The encoded
  name fits its original 16-byte slot through the existing UTF-8 label path;
  CP932 lookup keys and unrelated bytes remain untouched.
- Catalog scan found 123 dialogue source mentions, two glossary entries,
  two library entries and one UI entry involving Toji. No unexpected
  untranslated story speaker headings were found. No canonical prose edits.
- Ten battle-label tests and five Berserk sprite tests pass, including a
  regression showing the .15 missing name, current font mapping, source
  guards and byte isolation. Canonical check: zero issues, all 541 views
  match; synchronization previews zero changes. Build/install remain on hold.

## Source fixes - Berserk cut-in and Stage 19 Rhino jokes (2026-09-19; included in 0.6.16)

- Translated the EVA cut-in's Japanese Berserk graphic using the existing
  canonical ability label. New guarded `tools/berserk_banner.py` replaces
  only the solid and outline lettering in EFFPS3 member 307, texture 0.
  Animation/UV records, tint data, wave graphic and all other textures remain
  byte-identical. Transparent background pixels retain zero RGB as well as
  zero alpha. Both sprite styles were visually checked on a dark background.
- Integrated the PS3 sprite adapter into the effects build and both relevant
  validation gates; added its canonical asset mapping. Vita's equivalent
  sprite is not yet source-mapped; PS3 offsets must not be reused there.
- Replaced the previously shipped Stage 19 "RHINO-normous" and "dare-oceros"
  jokes with "Rhinos charges ahead of the competition!" and "Dodge this, or
  you'll get the point!" Sakuya's response is now "Stop turning me into a
  walking rhino joke!" These adapt the Japanese rhino homophones into English
  charge/horn wordplay while preserving the setup and following reactions.
- Three canonical dialogue rows changed; generated stage0019_03 view synced.
  Independent AI meaning review examined 11 context rows (t_1 21-31) for
  these three edits. This is a targeted repair, not a scored MQM assessment.
  Full member check: 349 records, 314 unique answers, zero problems including
  font-width checks. Canonical validation: zero issues, 541 views match.
- Five new sprite tests and nine existing battle-label tests pass. No game
  archive/ISO build, installation, version change or runtime verification;
  the confirmed hardware/RPCS3 packaging baseline is preserved.

## Source fixes - Eva battle and unit-help screenshots (2026-09-19; included in 0.6.16)

- User could not confirm the screenshot build. Do not attribute the reports
  to the current hardware-tested .15 build without a fresh runtime check.
- Added canonical "Sync Rate" for the still-Japanese AIDDATA widget 0x9e394;
  only its text pointer changes, preserving the live percentage and styling.
- Added the missing two-line barrier-icon explanation in the separate UTF-8
  Data Help table: "This icon lights up when the unit has a barrier. / The
  effects and EN cost depend on the type of barrier." Preserved both newline
  delimiters, including the trailing newline. Verified source VA 0x71fe58
  and sole data reference 0x858be4; standard UTF-8 relocation handles growth.
- Bound the four UTF-8 battle-name references to Misato's existing glossary
  entry. Its 12-byte encoded name fits the original 16-byte slot. CP932
  lookup keys and unrelated data remain unchanged. Extended the previous
  battle-label validation gate; the earlier two UI labels are now three.
- Nine focused tests pass, including source guards, current-font encoding,
  width budgets and unchanged bytes outside registered edits. Canonical
  validation: zero issues, all 541 compatibility views match; sync previews
  zero exports because these new labels are consumed directly by the adapter.
- Fourth Angel corruption is NOT fixed or dismissed: .15 RPW pilot-name
  slots contain the complete correctly encoded "the Fourth Angel". Both this
  and the earlier Neo Zeon Soldier report break after about 15 displayed
  characters, suggesting a fixed-size copy/termination problem. Read-only
  executable inspection found multiple 32-byte copy sites, but has not yet
  tied one conclusively to this nameplate. No speculative buffer patch or
  name shortening. Requires a known-build runtime reproduction/trace.
- No build, installation, version increment or runtime verification.

## Source fixes - Stage 17 joke localization (2026-09-19; included in 0.6.16)

- Replaced the previously shipped "Achoo Count" gag with "Count Me-Out" in
  Boss's boast and Roze's question; Akira now explains the count/count-me-out
  wordplay. Japanese hakushaku/hakushon (count/sneeze) does not rhyme in
  English. The adaptation uses the retreat already happening in the scene,
  retaining the detached-head reference, Naoto's identification and the
  following deliberately unimpressed reactions; it is not a literal sneeze joke.
- Replaced Johnny's "rhino-ference" with "Different personalities. But you're
  the Rhino. I thought you'd have a thicker skin." This adapts sai
  (difference/rhinoceros) into a literal/figurative English skin joke while
  preserving Eida's praise and Sakuya's resignation.
- Changed four canonical dialogue entries across stage0017_03/04, preserving
  IDs, glossary tokens and controls. Independent AI meaning review examined
  22 surrounding rows; this targeted repair is not a scored MQM assessment.
  Canonical checks: zero issues; all 541 compatibility views match after
  exporting only the two affected views. Both complete stage members pass
  check_stage.py (245 and 141 records), including font-based width checks.
  No game build, installation, version change or runtime verification.

## Source fixes - September 17 battle-screen report (2026-09-19; included in 0.6.16)

- User clarified these RPCS3 screenshots are from September 17, not confirmed
  .15 regressions. The .15 files already contain all 14 registered weapon
  requirement widgets in English; leave that existing fix intact pending a
  fresh runtime report. The corrupted Neo Zeon Soldier name also needs a
  .15 reproduction; no speculative name/buffer rewrite made.
- Added canonical KO Risk and Armor: labels for the two still-Japanese risk
  panel widgets. Source-guarded relocation preserves skulls, the armor value,
  colors, positions and all other widget bytes; widths checked against the
  original label budgets.
- Added the missing UTF-8 battle-name binding for Tetsujin, reusing the
  existing glossary entry. The standard relocated UTF-8 label pass handles
  both verified references; CP932 lookup keys and gameplay data are untouched.
  Added these checks to the full-build validation gate. No build/install.
- All 7 focused tests pass, covering label budgets, untouched widget fields, exact two-entry
  UTF-8 table guards/relocation, unchanged unrelated ELF bytes and existing
  .15 requirement strings. The .15 RPW soldier-name slots are checked for
  complete English glyph bytes; runtime corruption still requires a fresh
  report. Canonical validation passes, all 541 compatibility views match and
  sync dry-run changes none. Known-good .15 artifacts remain untouched.

## PS3 hardware success and future build policy (2026-09-19)

- User confirmed `0.6.15-hardware-test1` works after the hardware test request.
  Preserved its exact ISO/SELF identities as the known-good hardware baseline;
  firmware and extent of gameplay testing remain unspecified.
- Made dual-target packaging mandatory in CLAUDE.md and PS3 build/release
  guidance: guarded two-LOAD layout, original-metadata fake SELF, verified
  ISO trees, and the same derived snapshot installed into RPCS3. No plain-ELF
  default deliveries or silent fallback if hardware-loader checks fail.
- Updated handoff and test guidance to distinguish the later user report
  from immutable build-time audits. No rebuild, install, game-file changes,
  version increment, commit, upload or release in this follow-up.

## Local current-source PS3 hardware test (2026-09-19)

- User selected current translation edits for the new hardware-test ISO.
  Removed the unbuilt same-content .14 repack helper drafted before that
  choice; the requested candidate instead requires a complete source build.
- Added a read-only build-project input preflight (`--dry-run`) checking the
  canonical compatibility views, manifest inputs and translation parsing.
  It creates no output and does not reserve a version. Full validation still
  runs during the build. No release, tag or upload is authorized.
- Added a current-build hardware packager and test guide. It accepts a fully
  validated PS3 snapshot, reuses the unchanged guarded two-LOAD transform,
  verifies fake-SELF metadata and RPCS3 extraction, and checks every ISO member
  in both filesystem trees. The derived install snapshot records its source
  manifest hash; this does not assert hardware/runtime compatibility.
- Added synthetic tests for dry-run/no-write, failed-preflight refusal and
  overlay/snapshot provenance preservation, without requiring game content.
- Full current-source build completed as **0.6.15** in
  `work/build_0.6.15_hardware_source_20260919`: 141 story containers plus the
  shared end-session container; 60,653 story and 16 end-session records,
  31,666 battle-subtitle lines and 4,019 executable hooks. Full packed/UI
  regression gate passed; 1,034 untranslated mission variants remain recorded
  as a partial-translation backlog. Build counter and title footer both .15.
- 76 focused packaging/link/date/build-number/partial-translation tests pass.
  The separate historical startup-menu incremental test rejects its fixture
  because it reads the already-patched live game instead of its pinned older
  archive. Its guard was not weakened; the full source-build gate separately
  passed startup artwork/isolation and widget validation against originals.
- Hardware ISO completed in `work/ps3_hardware_0.6.15_test1_20260919`:
  `SRW-Z3-English-0.6.15-hardware-test1.iso`, 4,749,131,776 bytes,
  SHA256 `f0b94d9666c1703daf27b05a1d47d401443cdd70d3da73b2497c7ea23ae7abe9`.
  All 554 files verified in both trees; executable metadata, two-LOAD memory
  preservation and RPCS3 debug-SELF extraction verified. Fresh ISO layout,
  current translations; not a new proven hardware-compatibility fix. No
  hardware or RPCS3 runtime test at packaging time; later user-confirmed
  hardware success is recorded above. No xdelta or publication.
- Installed the matching hardware-wrapped .15 snapshot into the existing
  `game/` after installer dry-run: all218targets/complete disc verified,
  eight save files unchanged. Recoverable backup/cache retained at
  `work/install_backups/0.6.15_20260919_081855`; separate install receipt copied
  beside the ISO. RPCS3 left closed for user testing.

## Unreleased - Save converter moved to Retro Trans (2026-09-18)

- Moved ongoing save-converter development to the sibling retro-trans-tools
  project: compact Z3 saves tab, either direction or both, checked inputs,
  cancellable background work, verified output/ZIPs, original backups and
  bundled offline instructions. Existing byte-order, checksum and metadata
  rules are preserved; synthetic round-trip and failure tests accompany it.
- The legacy 0.6.14 standalone sources and packagers remain for compatibility
  and historical checks. New features belong in Retro Trans. No game build,
  game installation, live save conversion, version tag, release or upload.

What each release actually changes on screen. Built patches are snapshotted by
`tools/release.py` into `releases/<version>/` (game content, not committed);
`releases/<version>.json` records every file's size and SHA-1 and *is*
committed, so the repository proves what a release contained without carrying
any of it.

    python tools/release.py --list             what shipped, and what changed
    python tools/release.py --restore 0.3.0    verify an old snapshot
    python tools/deploy.py releases/0.3.0      put it back

## Unreleased - Retro Trans release documentation (2026-09-18)

- Added project instructions, a private local configuration template and a
  release guide for standard whole-ISO manifests and verified full/incremental
  patches. Documented separate Vita installer handling, exact binary identities,
  source-commit provenance, private manual testing and the public catalog limit.
- Tags, uploads, publication and visibility changes require an explicit user
  request; local edits or passing builds do not authorize them. This is a
  documentation-only change: no build, installation, version increment, tag,
  release or catalog update was performed.

## 0.6.14 — GitHub release (2026-09-17)

- Dual RPCS3/physical-PS3 candidate tooling (2026-09-18): added a pinned,
  dry-run-first builder that carries the current 0.6.14 executable through
  the existing guarded two-LOAD transform and fake-SELF wrapper. Preserves
  all other disc files, verifies both ISO trees and delta decoding, and
  mirrors RPCS3's debug-SELF extraction check. Separate test guide; no stock
  firmware or universal HEN claim. Runtime verification remains required;
  published assets are unchanged.
  Built `work/ps3_dual_0614_test1`: 5,012,193,280-byte ISO and 3,701,866-byte
  incremental xdelta from the released 0.6.14 ISO. All 554 members verified
  in both filesystem trees; decoded delta matches exactly. All 31 synthetic
  packaging tests, four live link-highlight guards and 77-date-card guard
  checks pass. Game text/assets and runtime addresses remain unchanged.
  Installed the complete candidate into the existing RPCS3 game folder with
  rollback backup/cache retained; all 218 targets match and eight save files
  are unchanged. RPCS3 launch via computer-use was denied by app permissions,
  so no agent-run runtime test occurred. User subsequently confirmed it works
  in RPCS3 (2026-09-18; gameplay test scope unspecified); physical-console
  verification remains pending. Added a dry-run-first from-original xdelta
  packager for that exact existing ISO and source-selection instructions.
  Created the 154,840,781-byte from-original patch (SHA256
  d2c737448c4134c05a17e8234f180019fdaac8edf3a6da4aed10942c50cd43b7);
  independently decoded it to the exact tested dual-test1 ISO. Existing
  3,701,866-byte incremental patch hash reverified. No game changes or upload.
- Physical-Vita release preparation: added a hardware-only delta packager and
  offline applier for the current 0.6.14/test16-linkfix-v4 files. Uses the 120
  changed rePatch payloads, excluding five emulator-converted modules. The
  existing auth sanitizer is shared as a standalone standard-library module;
  auth remains user-supplied and local, with secrets zeroed in generated output.
  New hardware guide covers source requirements, VitaShell/rePatch transfer,
  testing and rollback. All16 synthetic rePatch/applier tests pass. The actual
  distribution ZIP was extracted and applied with xdelta to the original game;
  all120 game payloads and sanitized auth verified, plus every completed ZIP
  entry. Local hardware ZIP is94,273,385bytes. Exact hardware runtime remains
  unverified; public package contains only deltas/scripts/guide, never auth.
  Published the14,058,604-byte hardware delta ZIP on v0.6.14 and put its SHA256
  directly in the release notes. Upload verified; other seven assets unchanged.

- 2026-09-18: removed SRW-Z3-0.6.14-Tool-Updates.zip from the release at
  the user's request. Other seven downloads unchanged; local ZIP preserved.
  Notes no longer advertise the supplement and clarify that the tagged source
  does not include every local build-tool change used for this release.

- 2026-09-18: removed the Python-only SRW-Z3-Save-Converter-0.6.14.zip
  release download at the user's request. Portable Windows converter remains;
  all eight remaining assets are unchanged. Release notes updated, local ZIP
  retained for recovery. Windows package still contains exact converter source.

- 2026-09-18: removed the standalone Windows converter .sha256 attachment
  at the user's request. Its ZIP checksum now appears directly in the release
  notes; all nine remaining downloads are unchanged. Local checksum retained.

- 2026-09-18: removed the Vita test16-linkfix-v3-to-0.6.14 incremental ZIP
  from GitHub at the user's request and removed its download/instructions from
  the release notes. The other ten downloads are unchanged. The matching local
  ZIP remains available for recovery; original metadata stays as a build record.

- 2026-09-18 follow-up: portable Windows x64 save-converter interface adds
  folder selection, read-only validation, background conversion, public import
  instructions and new timestamped output folders. A checked source fingerprint
  must still match before writing. Original inputs remain untouched. Bundled
  Python 3.12.14 x64/PyInstaller 6.22.3 in a portable folder; no Python install
  is needed by players. All 19 synthetic conversion/UI tests pass from source,
  the frozen executable and the extracted ZIP with Python search paths disabled.
  Computer Use visual inspection confirmed the window and built-in instructions
  are readable. Runtime licenses, exact app sources and file hashes are included.
  No real save data used/uploaded, no game rebuild or emulator installation.
  Published the Windows ZIP and its separate checksum to existing v0.6.14;
  all eleven remote asset hashes/sizes matched local files at publication.
  The Vita incremental download was subsequently withdrawn as recorded above.
  Release notes explain the portable app workflow.

- User confirmed the RPCS3 v5 and Vita3K test16-linkfix-v4 dialogue fixes work.
  Approved carrying those fixes into the latest published PS3 baseline, 0.6.13.
- Guarded PS3 port preserves the 0.6.13 menus, fonts and scenario content;
  changes only executable link/name/DOB/date helpers, startup-menu artwork
  and the title version footer. Later archives newly listed by the working
  deployment tooling remain original Japanese game bytes, not draft text.
- Packed validation now includes the startup-menu atlas pass. Frozen-baseline
  validation explicitly preserves the older suspend scene and Unit Info
  currency widgets instead of claiming they match newer unshipped catalog
  work. All other packed checks run normally. No translation completeness claim.
- Added dry-run release/snapshot planning, verified Vita file-delta packaging,
  safe new-folder application with optional locally generated install ZIP,
  synthetic patcher tests and a portable save-converter guide/tool bundle.
- 64 focused regression tests passed. The combined PS3 packed checks passed;
  all 218 ISO files read back correctly. The original-to-Vita patch completed
  an end-to-end apply/install-ZIP test with all 589 payload hashes matching.
- Cut the 0.6.14 snapshot and per-file patch sets: 186 original patches and
  exactly three changed-file updates, all decode-verified. Only EBOOT,
  AIDDATAPACK and EFFPS3 differ among previously released payloads.
- Release-metadata commit 17dd5e6 is pushed; unrelated dirty work remains.
  Distribution is patch-only. No complete game, personal save, account
  metadata, license, self_auth.bin or firmware is included. GitHub draft
  created; both ISO patches now decode-verified (151,153,200-byte full patch;
  2,121,180-byte update). Target ISO SHA256:
  c15b65a87d35cb4f3478fba829b4f14e6307de96b64979fdbc400b1d25e02462.
  All nine uploaded asset names/sizes/SHA256 digests matched local files.
  Published as the latest non-prerelease at
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.14
  (2026-09-17T16:30:03Z). Both emulators were open, so no new installation
  or cache/save modifications were made. Combined PS3 runtime test pending.

## Dialogue link backgrounds: RPCS3 v5 / Vita v4 (2026-09-17)

- Fix null scene references in dialogue term registration; retain explicit
  backlog scenes and the existing measured rectangle/name logic.
- Preserve previous date/menu fixes. RPCS3 changes EBOOT only and does not
  require install-cache deletion. Vita3K gets a complete installable ZIP.
- Native-instruction regression tests reproduce the prior missing background;
  in-game visual confirmation is still required. Not automatically installed.

## PS3 / RPCS3: centered date cards v4 (2026-09-17)

- Center all 77 translated full-screen date cards by rendered English width,
  including April 10. Preserve font size, vertical position and calendar text.
- Restrict the change to the native date-card caller; unrelated menus and
  unknown text keep native behavior. Preserve existing reward centering.
- Cumulative RPCS3 update includes v3 highlight/menu fixes. Built, not
  automatically installed; visual in-game confirmation remains pending.

## PS3 / RPCS3: name/term highlights and startup-menu v3 (2026-09-17)

- Correct the separate speaker-name widget's fixed-width background, including
  fractional character widths. Repair translated glossary comparisons so
  dialogue terms retain their proper IDs and can draw selection backgrounds.
- Match Vita's Scenario Select / Main Scenario / Tutorial Scenario artwork
  and numeric month/day birthday format. Keep date values and editing intact.
- Two-file update for the inspected older RPCS3 build: executable and startup
  UI archive. Saves, fonts and other archive members stay unchanged.
  28 automated regression tests pass; visual in-game confirmation is pending.
  Built but not automatically installed. Not a physical-PS3 package.

## Vita3K: name-widget and term-identity v3 (2026-09-17)

- V2 user retest exposed a separate name widget and a translated-label mismatch
  in term registration. Fix the actual name-width routine, not a keyword fixture.
  Translate the term comparison operand so registration retains the correct ID.
- Preserve working backlog term width, native record formats/navigation, and
  date centering. Primary terms use the actual rendered style height.
- 53 unique automated tests pass, including real name-widget geometry, real
  term registration, old-failure negative controls, all slots, and independent
  relocation. Visual confirmation remains pending; no automatic installation.

## PS3 / RPCS3: primary link-background v2 (2026-09-17)

- User screenshots confirm the original fix missed a second rectangle path.
  Correct its shifted X position and fixed-cell width using scene/keyword-
  matched rendered coordinates and measured widths; retain native colors,
  height selection, navigation, and the secondary fix.
- EBOOT-only update for the inspected older RPCS3 build, not physical PS3.
  Seven focused tests include the original bad arithmetic, all 256 slots,
  stale records, register/write isolation and baseline/v1 package equivalence.
  No in-game visual success claim; installation remains manual.

## Vita3K: link-background v2 (2026-09-17)

- User retest disproved v1; verified the installed executable was the v1 build.
  The primary highlight path still used fixed columns and character lengths.
- Replaced that path with scene/keyword-matched rendered coordinates and width,
  retaining secondary-path correction, style selection and date centering.
- Regression reproduces old Kei width93 versus rendered38.25; seven focused
  tests and42 prior UI/date tests pass. No in-game success claim yet.
- New installable ZIP: work/vita/vita3k_linkfix_install_02/
  SRW-Z3-Vita3K-test16-linkfix-v2-install.zip (1,872,598,787bytes).
  All589files verified. No automatic installation; old packages preserved.

## Vita3K: installable link/date-fix package (2026-09-17, V1 superseded)

- Built a complete installer ZIP under work/vita/vita3k_linkfix_install_01,
  replacing the manual-overlay workflow for Vita3K. Includes all 589 game files
  and installation metadata; only the executable differs from working test16.
- Retains link-background and date-centering fixes. All 589 files passed
  size/hash/CRC read-back; four focused executable tests rerun successfully.
- 1,872,598,785-byte ZIP, with backup/reinstall guide. No auth, licenses,
  firmware, saves, automatic installation or in-game verification.

## PS3 / RPCS3: older-build link-background update (2026-09-17)

- Verified the secondary-only correction is in PS3 0.6.13 and console test06,
  but absent from the locally configured RPCS3 game's older executable.
- Built a hash-pinned, EBOOT-only update under work/ps3_link_background_20260917
  for that exact older English build. Only 96 executable bytes change; keep
  existing matching fonts/translations. Not for physical PS3, Vita or newer builds.
- Three focused tests pass, now including Alto/ZEXIS. Archive read-back passes;
  no automatic installation or in-game visual verification.

## Vita test16: link-background update (2026-09-17)

- Size selected backlog-name and keyword backgrounds using rendered VWF width,
  fixing the excessive background behind Alto and ZEXIS. Preserve link IDs,
  navigation, colors and native record lengths.
- Combined EBOOT update under work/vita/link_background_test16_01 retains all
  77 date-card corrections. Existing working test16 only; backup/install guide
  included. Older packages remain untouched. Future Vita builds include it.
- Four new CPU tests cover real glyph advances, all 256 link slots, reuse,
  null selections, separate relocations and retained date centering. All 42
  existing date/UI/screenshot regression tests also pass (46 total).
- ZIP/disk read-back passed. Not installed; in-game visual check still needed.
  No translation, auth, save or unrelated menu changes.

## Vita test16: date-card centering update (2026-09-17)

- Center all77 translated date cards using English width in both native font
  modes. Preserve font size, vertical position, date values and animation inputs.
- A guarded date-only draw-call change avoids altering other menus. Future Vita
  builds include it; a small test16 EBOOT update is available under
  work/vita/date_centering_test16_01 with backup/installation instructions.
- 42 tests pass, including actual native-call execution for all77dates in both
  modes and reproduction of the old April27 offset. In-game visual retest pending.
- No installation, saves/auth changes, or fixes to the separately reported
  defeat-condition/Z Chips/intermission-alignment issues in this update.

## AI-only MQM proofreading workflow (2026-09-17)

- Added frozen canonical review packets, 80-row batches with full-scene context,
  glossary expansion, recurring-term concordance, and structured AI review and
  challenge templates. Existing proofreading hints are reused, not auto-scored.
- Added validated coverage-aware MQM reporting and advisory fix queues. Only
  accepted linguistic errors enter the rate; uncertainty, missing Japanese,
  technical hints and platform layout evidence remain explicit and separate.
- Added AI reviewer instructions and correction workflow linked from BASE_RULES.
  Commands are dry-run-first and do not edit translations or invoke paid models.
- Prepared the 244-row stage-one pilot (five batches); linguistic review has not
  started. 18 MQM tests and 18 localization tests pass. No game content changed.

## Bidirectional RPCS3/Vita3K save-conversion candidates (2026-09-17)

- Converted both source profiles into separate emulator-import packages under
  work/save_conversion_20260917. Original live saves remain untouched, with
  additional exact backups. System saves are included; a chapter-10 system
  description is not presented as a newly recovered manual save.
- Only the native-endian size field changes in binary saves; all progress and
  checksum bytes are preserved. Slot numbering/display metadata is adapted to
  each emulator; destination RPCS3 account metadata comes from its own saves.
- Nine synthetic tests pass; all five converted saves round-trip exactly and
  pass native Vita shared-payload checksum/version checks with corruption
  negative controls. ZIP read-back and original-source hashes pass.
- Full game-load/save testing remains pending. These are not signed PS3 or
  encrypted physical-Vita restores; no automatic installation or public push.

## Vita test16: completed rePatch hardware-test package (2026-09-17)

- User supplied the local game auth dump; size, authority ID and capabilities
  validate against the executable. Builder now strips unused padding and
  shared-secret fields, preserving only rePatch's consumed authentication
  fields. The raw input is untouched and never packaged.
- Packaged the existing 120 test16 game files plus sanitized auth; 123 ZIP
  entries including instructions/manifest passed size, SHA256 and CRC checks.
  Output: work/vita/english_repatch_test16_02, 94,279,737-byte ZIP.
- Added three synthetic auth sanitization/archive regression tests; all 131
  Vita tests pass. No new executable patch or translation content changes;
  physical-Vita runtime testing and firmware/plugin confirmation remain pending.

## PS3 hardware test 06: two-LOAD executable candidate (2026-09-17)

- User reports 04 (English EBOOT/Japanese data) fails with 80010001 while
  05 (Japanese EBOOT/English data) loads, isolating the immediate failure to
  the English executable under the tested settings.
- Added a source-pinned test builder that folds the translation region into
  the native writable data region, preserving code, translated bytes, runtime
  addresses, zeroed BSS/scratch, TLS and application metadata. Section metadata
  moves outside the mapped data with alignment preserved. This is a candidate
  for hardware testing, not a proven cause or compatibility fix.
- Only EBOOT differs from exact test 03; all 553 other files are preserved.
  28 packaging/layout tests pass. Full image audit and checksums are generated
  in work/ps3_loader_fix_20260917_aligned after ISO read-back succeeds.
  No installed files, saves, firmware, release version or public push changed.

## BASE_RULES.md gains six rules from stages 90-100 (2026-09-17)

- Four of the ten candidates were dropped on review because the file already
  covered them, which is a fair verdict on how dense it was: character
  research already supplies the voice data, and the slice-context rule already
  says to read the neighbours. TWO STRUCTURAL FIXES landed instead of new
  bullets.
- THE FIT RULE'S OPENING CLAUSE WAS UNREACHABLE. It read "if the translation
  doesn't fit the limit, compress or abbreviate" -- but an agent only gets
  there by drafting something and measuring it, and the stage 94 agent never
  did. It shortened WHILE drafting, from the 55-character rule of thumb, so it
  never had a line that failed; it had a line that passed. The full twelve
  items measured 664, 713 and 658 px against a 963 limit. The rule now opens
  "write the line in full first and let the checker judge it", and adds "never
  drop an item the source lists".
- THE NEIGHBOUR-ROWS OBLIGATION FOLDED INTO THE EXISTING SLICE-CONTEXT LINE
  rather than adding a bullet. That line was framed as permission to look
  OUTSIDE your slice; the stage 96 misreading happened entirely INSIDE one, so
  the rule never bit. It is now also an obligation before deciding who a line
  is aimed at.
- New: DO NOT SUPPLY WHAT THE SOURCE OMITS. The gender rules covered he/she
  only; nothing covered inventing a subject. Two stage 99 agents invented
  opposite ones -- "we" and "I" -- for the same subjectless line. Prefer a
  construction that keeps the ambiguity. An invented subject reads as fluent
  English and passes every check, so only the Japanese shows it.
- New: A SIMILAR EXISTING LINE IS READ, NOT PASTED. Written out in full rather
  than as an aphorism, at the user's request -- "a near match is a prompt, not
  a fill" only parses if you already know what it means. Largely anticipatory:
  nothing in the pipeline hands an agent a near match yet.
- New: COUNT BEFORE CALLING SOMETHING A MAJORITY, and remember a count can be
  real and still mislead -- a lopsided one often means the material changed
  rather than that the question is settled.
- New, under proofreading: AN UNCERTAINTY REPORTED IS WORTH MORE THAN A CLEAN
  REPORT -- report the calls you were unsure of even when the row passes. The
  existing rule covers rows that cannot be verified; this covers the ones that
  pass.
- CORRECTED SAME DAY: the first draft of these two carried the evidence that
  produced them -- a 56-to-1 count, a tally of defects across stages 90-100.
  THAT EVIDENCE DOES NOT BELONG IN A DOCTRINE FILE. `BASE_RULES.md` has to
  survive this project moving to a different game; a rule that cites a stage
  number is a log entry wearing a rule's clothes. The evidence stays here,
  where it is already written down, and the rules state the principle.

## A proofreading pass needs different material from a translating pass (2026-09-17)

- `tools/proofread_stage.py` builds review material for a finished stage:
  scene bundles (Japanese over English, in reading order) plus a concordance
  of recurring plain-text terms. Slices only ever see 120-record windows, so a
  term written two ways is invisible to them; on one page it is obvious.
- IT RE-CHECKS NOTHING `check_stage.py` ALREADY DOES. Across stages 90-100
  every defect that reached review was in a class the checker structurally
  cannot see, and every one surfaced because a slice reported an uncertainty,
  never because a check failed.
- THE FIRST VERSION WAS TOO NOISY TO SHIP AND WAS CUT DOWN. Flags for invented
  subjects, polarity, portrait mismatches and ordinary-word tokens fired on a
  third of a stage between them. A flag that fires often teaches the reader to
  skip flags. `invented-subject` cannot be made precise by pattern at all:
  English requires a subject wherever Japanese omits one, so the SHAPE is
  ordinary translation and only the ambiguous cases matter, which takes
  judgement. What survives fires on about 2% of records.
- THE FLAG THAT MOTIVATED THE TOOL DID NOT WORK EITHER. A token-based
  consistency check found nothing in stage 97, the stage where an epithet
  demonstrably shipped two ways -- because that epithet is plain text, and
  tokens are already enforced by the glossary gate. The concordance replaces
  it: recurring terms with their renderings side by side, glossary entries
  omitted, no verdict offered.
- TWO LOOKUPS ARE ATTACHED PER RECORD, both measured before being built:
  NEAR    the closest line elsewhere in the corpus. Exact-hash reuse reports
          20% of a stage as "new" when a 70%-or-better neighbour exists -- 278
          of stage 97's records have one. A near match is a prompt to read,
          never a fill: the difference is what you are translating, and a
          stage 94 slice lost content exactly by treating a near thing as the
          same thing.
  VOICE   the same Japanese dialogue spoken by a different character, with
          their rendering. 381 lines in the corpus are shared this way and 63%
          were deliberately varied, so the question is live rather than
          rhetorical: does this character say it differently?
- The reuse pass is blind to both because a record's identity is a hash of the
  WHOLE record, speaker line included. Identical dialogue in two mouths hashes
  differently; a line differing by one leading ellipsis hashes differently.

## Stages 100A and 100B translated (715 records) -- ALL STORY DIALOGUE DONE (2026-09-17)

- STG0100A members 3 (508 records) and 4 (91), STG0100B members 3 (112) and 4
  (4), seven slices. All four members pass `check_stage.py` and
  `check_names.py` clean, every `$$` token expands, and the merged stage was
  measured directly: 1,830 lines, none over 963 px or the four-line ceiling,
  no stray Japanese outside tokens, no tilde inside a word.
- **THIS COMPLETES ALL 116 STORY SCRIPTS.** Stages 1-100 including every
  branch half are now translated, registered and shipping as compatibility
  views. 541 views, 0 issues.
- FIFTY-EIGHT MERGE CONFLICTS, the most of any stage, because member 3's
  epilogue replays across slice boundaries and its slices ran before any
  sibling answer existed. They were triaged rather than hand-weighed one by
  one: ONE differed in meaning, the rest were paraphrase. Since the merge
  collapses by sha, the stage is internally consistent either way, and the
  kept versions were then checked against every settled form -- clean.
- THE ONE THAT MATTERED WAS A POLARITY AMBIGUITY, not a slip. The contracted
  form is either the negative "cannot" or a colloquial contraction of "can",
  and the two slices read it opposite ways. The scene settles it: the next
  speaker jokes about whether he would be ACCEPTED back, then offers to come
  along, so returning is the plan and the gate is the means. "If I can" is
  right, and is what the merge had kept.
- A SLICE FOUND TWO SHIPPED SOURCES DISAGREEING on an epithet's length, 4 to 2.
  Both short-form records live OUTSIDE `translation/stage*.json` -- in a
  keyword library entry and an ability file -- which is why the split survived:
  the sha cache indexes only stage files, so no per-stage audit can see them.
  New work takes the majority; reconciling the two is the user's call.
- A SHIPPED RECORD THAT CARRIES A TRAILING FULL STOP WAS REUSED VERBATIM, and
  the slice reported it as contradicting the no-trailing-stop rule. It is not a
  contradiction: that rule is a 76% convention for NEW work, and a shipped
  record's English is not a slice's to rewrite. The two rules govern different
  things and the prompts now say so.
- Also settled: the Geass space compound takes the keyed token; bare Imperium
  is plain; the L.A.I. research arm is "L.A.I. R&D"; convergent evolution and
  departure ceremony are plain; and Aoi's senpai is lowercase "senior",
  matching her own shipped plural rather than a transliteration.
- A SECOND SLICE MISTYPED A NEAR-IDENTICAL KANJI by writing it as a numeric
  escape rather than the literal character. The glossary gate caught it only
  because the wrong character broke a term; it would not catch one in ordinary
  prose. The merged stage was scanned for stray Japanese outside tokens and is
  clean, and the rules now tell slices to write literal Japanese, or to decode
  and diff every escape against the source before finalising.

## Stage 99 translated (984 records) (2026-09-17)

- STG0099 members 3 (405 records) and 4 (579), nine slices. Both pass
  `check_stage.py` and `check_names.py` clean and every `$$` token expands.
  862 unique shas, and after adjudication no sha is answered two ways; none of
  the 64 that also ship elsewhere diverges.
- FOUR MERGE CONFLICTS, DOWN FROM FIFTEEN IN STAGE 98, because the slices were
  told from the start to check the sibling answer files rather than only the
  shipped table. Two were kept as merged and two resettled: one line ends in a
  realisation marker that the statement reading dropped, and one HAS NO SUBJECT
  IN THE JAPANESE -- both candidates had invented one, "we" and "I", so a
  passive now carries the ambiguity the source actually has.
- `check_stage.py` DEGRADES SILENTLY WHEN IT CANNOT REACH THE FONT. One slice
  reported that it printed "(no TTF: width check skipped)"; the run still ends
  "0 problems", which reads exactly like a clean one. The font is present and
  works here, so that slice's sandbox could not see it. ITS LINES WERE NEVER
  MEASURED. All 2,465 lines of the merged stage were then measured directly:
  nothing over 963 px, nothing over the four-line ceiling. Slices are now asked
  to report that line if they see it, and the merged stage gets its own width
  audit before registration rather than trusting the per-slice checks.
- A DRAWN-OUT SHOUT HAD BEEN WRITTEN AS A STAMMER. `アァァクション` carries a
  small-kana stretch the three shipped flat copies do not, so keeping a stretch
  was right -- but it was rendered with hyphens, which in English reads as
  nervous hesitation rather than a battle cry. Now repeated letters, per the
  elongation rule.
- THE TOKENISER'S THREE OFFERS WERE CORRECT THIS TIME, and the distinction
  matters: `ミカゲ空間` genuinely IS that character's, so the name takes the
  token and a rename should propagate. That is the opposite of the machine
  names rejected in stages 97 and 98, which were separate entities whose names
  merely contained another's.
- A SLICE DECLINED TO STRETCH AN ENGLISH WORD where the Japanese stretched a
  COPULA rather than a lexical word -- there is no word the stretch belongs to,
  and lengthening a neighbour would invent emphasis. The rule now says so.
- Stage 98B's one-line judgment call became precedent: where `進化` and `シンカ`
  collide in a single sentence, case separates them. A stage 99 slice found the
  shipped record and followed it rather than applying the blanket lowercase.
- Also settled: `螺旋族` "Spiral race", `螺旋エネルギー` "Spiral energy",
  `超螺旋宇宙` "the Super-Spiral universe", `高位生命体` "higher beings",
  `根源的災厄` "the Primal Catastrophe", `母星` "homeworld", bare `天元突破`
  "Tengen Toppa" (from `abilities.json`) -- ALL PLAIN, and two slices tokenised
  one of them by mistake before the glossary gate caught it. Simon's `アニキ`
  for Kamina is capitalised "Bro", his own idiolect, distinct from another
  pair's lowercase.
- Registered into the shared catalog: 537 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## Stages 98A and 98B translated (1,089 records) (2026-09-17)

- STG0098A members 3 (785 records) and 4 (54), STG0098B members 3 (84) and 4
  (166), eleven slices. All four members pass `check_stage.py` and
  `check_names.py` clean and every `$$` token expands. 930 unique shas, and
  after adjudication no sha is answered two ways.
- FIFTEEN MERGE CONFLICTS, THE MOST OF ANY STAGE, because member 3 replays its
  scenes and most of its seven slices ran before any sibling answer file
  existed to check against. `merge_stage.py` keeps whichever file it was
  handed first, WHICH IS NOT A DECISION, so all fifteen were read against the
  Japanese and settled on the merits: eleven kept the better of the two, four
  were rewritten.
- THE TRAILING FULL STOP IS NOW MEASURED RATHER THAN GUESSED. Several of those
  conflicts differed only by a final period. No shipped record closes the
  Japanese with `。` inside `「」`, and the English omits the stop 39,530 times
  to 12,454. The majority governs, so the period goes.
- Of the four rewritten: `意思` is "will" and `決意` "resolve", kept distinct
  because both appear in the same scene; `嘘つきで逮捕される` is being arrested
  AS a liar, not for the act; a child's `当ったり前だぜ` keeps its casual
  register; and `どやされる` is being yelled at, in a rough regional voice.
- TWO RECORDS DIVERGE FROM SHIPPED TEXT DELIBERATELY, both flagged by their
  slices. A bare `「………」` ships 1-1 tied between three dots and nine;
  CONVENTIONS.md settles that shape absolutely, so doctrine beat the coin-flip.
  A banner ships 1-1 between ten and nine leading spaces while the source
  itself carries eleven; with no majority to copy, the source governs.
- `アンチスパイラル` SPEAKS FOR THE FIRST TIME IN THE SCRIPT HERE, in 31 records
  across both branches. It therefore takes `#pilot` in those and `#keyword`
  everywhere a third party names the species. The corpus's 56-to-1 lean toward
  `#keyword` is not a majority to follow -- it only records that the entity had
  never appeared as a character before.
- `アルト先輩` WAS ANOTHER RULE OF MINE THAT OVERGENERALISED. It said "senior"
  always; the corpus splits by function, dropping the honorific in direct
  address (3 of 4) and keeping "senior" only in third-person reference, the
  same shape as `ロジャーさん`. Honorifics are per-character: `カイエンさん`
  keeps "Mr." even in direct address while `クルツさん`, `キタンさん`,
  `ガムリンさん`, `桂さん` and `ミサトさん` drop theirs.
- Bare `宇宙怪獣` is lowercase "space monster". The corpus drifts across three
  forms and the character who says it most uses all three, so there is no
  register split to follow and the majority governs.
- Also settled: `カテドラル・テラ` "Cathedral Terra"; `螺旋族`/`螺旋の民` "the
  Spiral race"; `スパイラルネメシス` "Spiral Nemesis"; `多元宇宙迷宮` "the
  Multiversal Labyrinth"; `ガンメン` plain "Gunmen"; `大グレン団` "Dai-Gurren
  Brigade" (9 of 10); `市街地` banners "Streets of X"; a fragment missing part
  of its glossary key stays plain.
- Registered into the shared catalog: 535 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## The same tokeniser bug, one stage later, through the gap in my fix (2026-09-17)

- The stage 97 fix refused a katakana term only when EVERY occurrence of it sat
  inside a longer katakana run. A stage 98 record slipped through: the machine
  `キングキタン` is named after its pilot `キタン`, and because the pilot also
  SPEAKS in that record, the term does occur free-standing -- so the test
  passed and the tool offered `King $$キタン$$`, filing the machine under the
  pilot's term.
- The test is now ANY occurrence, not every. Nothing in the record tells the
  tool which English "Kittan" is the man and which is the machine, so it
  declines the whole record and leaves it to a reader. Skipping is safe; a
  wrong token is not.
- CAUGHT THE SAME WAY AS THE FIRST ONE: by reading the proposed change before
  applying it. The round trip passed both times, because both spellings put
  identical words on screen. A tool that cannot distinguish a right token from
  a wrong one must not be trusted on its own confidence.
- Verified: the offer drops from three records to two, the two survivors are
  genuine (a name written as literal English, in records with no compound),
  and stages 87, 93a and 97 still tokenise identically.

## Stage 97 translated (964 records); survived a session limit (2026-09-17)

- STG0097 members 3 (140 records) and 4 (824), eight slices -- the largest
  stage of the project. Both pass `check_stage.py` and `check_names.py` clean
  and every `$$` token expands. 894 unique shas, no sha answered two ways
  across a slice boundary, and none of the 56 that also ship elsewhere
  diverges. Reuse was 6%: almost all new material.
- A SESSION RATE LIMIT KILLED TWO SLICES MID-FLIGHT and the other six
  survived intact. Verified on the spot that member 3 was complete and member
  4's 552 answered shas had no problems beyond the missing records, wrote
  `work/tr/STG0097/RESUME.md` beside the answers, and did not register
  anything partial -- the registrar refuses a record with no English anyway.
  The two were rerun against their existing briefs once the limit reset.
- THE SAME EPITHET WAS WRITTEN TWO WAYS INSIDE ONE STAGE. Two slices rendered
  `いがみ合う双子` differently, one quoted and capitalised, three plain. THE
  CROSS-CORPUS AUDIT CANNOT SEE THIS -- it compares identical shas, and these
  are four different ones. Reading the shipped corpus showed the term splits
  by register rather than drifting: quoted where the Japanese NAMES the
  Sphere or uses it as a title before its pilot, plain where a speaker means
  the pair. Three records moved onto the quoted form and the possessive was
  left alone; a sweep of the stage's other quoted terms found no second case.
- The `'Feuding Twins'` versus `'Bickering Twins'` question is recorded in
  CONVENTIONS.md as the user's, since settling it moves shipped records.
- FOUR TOKENISATIONS WERE REJECTED and the tool fixed; see the entry above.
- `マリィ` WAS A PHONETIC GUESS THAT DID NOT NEED TO BE. The name is spelled
  out in seven `voice_*.json` records, which the sha cache cannot see. The
  slice rules now name `translation/library/`, the voice files and
  `abilities.json` as places to search before coining, and warn that a
  near-identical name one file over belongs to a different character.
- MY TWO RULE FILES DISAGREED ABOUT ROGER. CONVENTIONS.md said his own `了解だ`
  is "Understood"; SLICE_RULES.md said the word "stays plain even when Roger
  himself is speaking", which reads as "Roger!". A slice spotted the conflict
  and said so. The corpus settles it 4 of 4 for "Understood"; the slice rule
  was right about never using the token and wrong about the English word, and
  now says both separately.
- Also settled: `アクシズ落とし` `$$アクシズ$$ Drop`; `インベーダー` and
  `アンチスパイラル` take `#keyword` for the species or collective; `マーグ`
  always `#pilot` (17 of 17); bare `リアクター` is a fragment of the keyed
  Sphere Reactor and stays plain; `シュロウガ` "Shurouga"; `サード・ステージ`
  "Third Stage"; `螺旋の男` "Man of the Spiral"; `カテドラル・テラ` "Cathedral
  Terra"; `隊員` as a speaker "Trooper" (8 to 4); `棄民` "an abandoned people".
- Registered into the shared catalog: 531 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## The tokeniser split one machine's name across another's token (2026-09-17)

- `tools/tokenise_stage.py` offered four stage 97 records in which
  `アークグレンラガン` -- a machine with NO glossary entry of its own -- would
  become `Arc-$$グレンラガン$$`, because the shorter `グレンラガン` IS an entry
  and matched as a substring of the longer name.
- **THE ROUND TRIP CANNOT CATCH THIS.** The tool's safety property is that the
  new text must expand to the old text character for character, and it does:
  both spell "Arc-Gurren Lagann". What changes is which term the line is filed
  under, so a rename of the shorter name would silently rewrite the longer
  one. Same latent shape as the military "Roger!" and the Wing Zero records.
- `refs()` now refuses a katakana term flanked by more katakana, since a run
  of katakana is one name. The interpunct is deliberately NOT treated as
  glue: `シャア・アズナブル` and `シャア` are both entries, so longest-match
  already settles those.
  CORRECTED 2026-09-17: this first said "whose EVERY occurrence is flanked",
  keeping the term where it also stood free-standing somewhere in the
  record. THAT WAS NOT ENOUGH -- see the entry above.
- Verified the four are no longer offered, and that stages 87, 93a and 96
  still tokenise identically. AUDITED THE WHOLE CORPUS FOR RECORDS THAT
  ALREADY SHIPPED THIS WAY: there are none. The 38 records where a token
  follows a hyphenated fragment are all the documented stutter pattern
  (`K-$$風間$$`) or a real prefix (`ex-$$ＺＥＸＩＳ$$`).
- Caught because the pipeline reads every tokenisation before accepting it,
  rather than trusting the round trip. The four looked wrong on sight.

## Stage 96 translated (868 records); a line read backwards (2026-09-17)

- STG0096 members 3 (294 records) and 4 (574), eight slices. Both pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token expands. 752 unique shas, no sha answered two ways
  across a slice boundary, and none of the 42 that also ship elsewhere
  diverges.
- A SLICE READ A LINE BACKWARDS AND SAID SO. Frontal's remark to Amuro was
  rendered as dismissing a third party, when the two records that follow -- an
  objection to someone being called a fake, then an explanation of who is meant
  -- show it is grudging credit aimed at the listener, and the verb is "drove
  back", not "cast aside". Corrected before the merge. THE SLICE FLAGGED IT AS
  INTERPRETATION RATHER THAN FACT, which is the only reason it was looked at.
- THE REMAINING SLICES WERE TOLD TO READ THE NEIGHBOURS. Japanese omits the
  subject and the scene supplies it, so the brief now asks each slice to report
  ANY LINE WHOSE SUBJECT OR ADDRESSEE IT HAD TO INFER. Three did, and all three
  resolutions were checked: a group rebuking Char to his face rather than
  behind his back, a pronoun pointing at the entity named one record earlier,
  and two women belonging to the listener's past rather than the speaker's.
- THE GLOSSARY GATE CAUGHT BAD TOKENS INSIDE FOUR SLICES. Between them:
  `$$アクエリオン$$`-style names with no entry, a set of Zeon family names, an
  `$$おキツネ博士$$`, a `$$Ｚチップ$$`, and an ideographic space that had leaked
  INSIDE a token. All were fixed by the slice before it reported.
- THREE RECORDS WERE REPORTED AS "COMPRESSED TO FIT" AND ALL THREE WERE
  CHECKED, because that phrasing is what preceded the dropped list items in
  stage 94. These were legitimate: each keeps its content, sits inside the
  three-line ceiling, and runs 380-750 px against the 963 limit.
- Also settled: `ネオ・ジオン兵` "Neo Zeon Soldier" (9 of 9); `アンチスパイラル`
  takes `#keyword` for the species or collective (35 to 1) and `#pilot` only
  for a present avatar; bare `フロンタル` and spelled-out `フル・フロンタル` are
  two different entries, read the exact string; `阻止限界点` "the point of no
  return"; `スパイラルネメシス` "Spiral Nemesis"; `ドルイドシステム` "Druid
  System"; `棄民` "an abandoned people"; Zeon family names plain.
- Registered into the shared catalog: 529 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## Stage 95 translated (598 records) (2026-09-17)

- STG0095 members 3 (96 records) and 4 (502), five slices. Both pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token expands. 576 unique shas, no sha answered two ways
  across a slice boundary, and none of the 27 that also ship elsewhere
  diverges.
- REUSE WAS 5%, the lowest of the project. This stage is almost entirely new
  material, and three of the session's findings came out of it.
- TWO SLICES RECOUNTED `総帥` WITHOUT BEING ASKED and both got 47 to 18 for
  "Supreme Commander", which is what prompted the recount recorded in its own
  entry above. One of them had reached the figure independently before the
  rule was updated mid-session.
- A SLICE RESOLVED A NAME THE BRIEF COULD NOT. `オルソン` keys two different
  characters and the brief's glossary table printed both rows identically; the
  slice settled it from a shipped line in stage 230 describing the same two
  singularities. The generator is fixed in its own entry above, so the next
  slice will be told rather than having to deduce it.
- TIES WERE BROKEN BY EVIDENCE, NOT BY COIN. A `でしょうか…` musing splits 15-15
  corpus-wide, so the slice used the speaker's own three prior instances (2-1
  against a question mark). `副長` went to "XO" on a counted 5-2. `邪気` and
  `モビルアーマー` were reported as genuinely unsettled rather than presented as
  decided.
- Also settled: `螺旋力` "Spiral Power"; "Man of the Spiral" keeps its shipped
  epithet rather than being rebuilt from the bare gloss; `ファースト・イノベイター`
  "First Innovator"; `終わらない冬` "endless winter", deliberately distinct from
  the settled `核の冬` "Nuclear Winter"; `私室` "Private Quarters"; bare `アポロ`
  plain, being a different string from the keyed `アポロン`.
- `姫` IS MARKED `"status": "ambiguous"` IN THE GLOSSARY and is not the word for
  an ordinary princess; a slice wrote that plain and lowercase rather than
  reaching for the keyword.
- Registered into the shared catalog: 527 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## The brief's glossary table printed one name twice with no way to tell them apart (2026-09-17)

- `tools/export_stage.py` emitted one row per glossary term keyed by the bare
  Japanese, so a string keying TWO terms appeared twice under the same name.
  A stage 95 brief listed `オルソン` -> "Olson (pilot)" twice, and the slice had
  to work out from a shipped line in another stage which of the two its record
  meant. It got it right; the next one might not.
- Those rows now print the `#` DISCRIMINATOR TOKEN that actually selects the
  term (`$$オルソン#50$$`, `$$オルソン#130$$`) and carry the same
  "AMBIGUOUS -- DECIDE FROM THE SCENE" marker the cast sheet already used.
  The cast-sheet marker, added in stage 88, only ever covered SPEAKERS; the
  glossary table was a second door onto the same mistake.
- THE MARKER QUOTES THE `note` FIELD, NOT `source`. Both `オルソン` entries
  name the same series in `source` even though one of them is a Gundam Meister
  from a different show entirely; only the note says so. That is a glossary
  data fault, left as it is because the note carries the truth and rewriting a
  term's `source` would touch the term itself.
- Verified by regenerating an affected brief to a scratch path -- the live
  stage 95 briefs were not touched, since a slice was still reading one.

## Stage 94 translated (511 records) (2026-09-17)

- STG0094 members 3 (302 records) and 4 (209), five slices. Both pass
  `check_stage.py` and `check_names.py` clean and every `$$` token expands.
  468 unique shas, no sha answered two ways across a slice boundary, and none
  of the 31 that also ship elsewhere diverges.
- REUSE WAS ONLY 7%. Almost all of this stage is new material, which is why
  three separate review catches were needed before it could be registered.
- A SLICE DROPPED TWO ITEMS FROM A TWELVE-ITEM LIST TO MAKE IT FIT. The full
  twelve measured 664, 713 and 658 px against a 963 px limit -- about 30
  percent spare on every line. Restored. DROPPING CONTENT THE SOURCE LISTS IS
  A TRANSLATION ERROR, NOT A LAYOUT DECISION, and the rules now carry the real
  pixel figure rather than only saying the 55-character guideline is not the
  limit.
- TWO MORE TILDES WERE WRITTEN INSIDE ENGLISH WORDS, by a slice reading the
  "a stretch may be kept for a drawn-out call" clause as licence for the
  character itself. Both fixed: the onomatopoeia takes repeated letters, and
  the name takes the flat form four shipped records already use. The rule is
  now absolute with no exception, since three slices have now reached for a
  tilde from three different justifications.
- A `だろう` MUSING HAD ACQUIRED A QUESTION MARK. The corpus is decisive: of
  312 records ending in `だろ`/`だろう` with no `？` in the Japanese, 302 have
  no `?` in the English. The ten that do are confirmatory tags addressed to a
  listener ("..., right?"). A speaker thinking aloud trails off on `...` with
  no mark EVEN WHEN THE JAPANESE CARRIES AN INTERROGATIVE WORD. The rule sent
  to slices only covered `？` and `か`, so the two readings were
  indistinguishable; it now covers this.
- BOTH `ミーナ` READINGS ARE LIVE IN THIS STAGE and both were resolved
  correctly by different slices: `$$ミーナ#182$$` is the Macross Quarter's
  operator, `$$ミーナ#120$$` is Mehna at Scoat Lab. One slice settled Mehna
  from the library biography when the scene alone was ambiguous, and ignored a
  stale portrait on the same line.
- `時空振動` IS NOT THE KEYED `時空震動` -- different kanji, no token. Also
  settled: `スコート・ラボ` "Scoat Lab"; `フィフス・ルナ` "Fifth Luna";
  `メモリーの呪縛` "the curse of Memory"; bare `トレーダー` "Trader"; katakana
  `カナメ`/`チドリ・カナメ` plain, since neither string matches the keyed
  hiragana form.
- The tokeniser moved one record onto a token, read before accepting.
- Registered into the shared catalog: 525 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## A rule I wrote about elongations was backwards (2026-09-17)

- `work/tr/SLICE_RULES.md` said a tilde elongation "is REPEATED LETTERS". The
  shipped corpus says otherwise: of 203 records whose Japanese stretches a
  vowel with `～`, 173 render ordinary English with no stretch at all and only
  30 keep one. The rule was wrong by 173 to 30 and is now corrected.
- WHAT THE CORPUS ACTUALLY DOES: it drops the stretch for a filler vowel
  (`いや～` is "Ah,", `ん～` is "Mmm,", `あ～あ` is "Ah well,") and keeps it
  only where the stretch IS the utterance -- a drawn-out call of a name, or a
  stretched expressive word. Even then the stretch may land on a different
  word than the Japanese stretched it on.
- A SMALL-KANA ELONGATION IS A DIFFERENT THING and does keep its stretch;
  `く、くそぉぉぉっ` -> "D-daaaamn it!!" was never in question. Conflating the two
  is what produced the bad rule.
- THE STAGE 92 RECORD WRITTEN UNDER IT IS CORRECTED, from "T-this won't dooo!"
  to "T-this won't do!". Removing the tilde from inside the English word was
  right; stretching the vowel instead was not.
- FOUND BY A SLICE THAT REFUSED TO FOLLOW THE RULE. A stage 94 slice hit an
  elongated name that four shipped records render with no stretch at all, said
  so, and took the corpus over its brief -- which is exactly what the rules
  ask for, and the second time this session that a slice has overturned one of
  my own notes by reading the text.
- Edited by message ID with the definition's `tokens` list checked; `sync
  --write` regenerated the one affected view. 523 views, 0 issues.

## Stage 93B translated (204 records); stage 93 complete (2026-09-17)

- STG0093B members 3 (178 records) and 4 (26), three slices. Both pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token expands. 195 unique shas, no sha answered two
  ways, and none of the 128 that also ship elsewhere diverges.
- THE TWO BRANCHES AGREE. Only three shas occur in both halves of stage 93,
  and all three carry identical English. One of them was settled before either
  branch shipped: a 93B slice found the sha already answered in a 93A answer
  file and reused that wording rather than drafting its own.
- THE GLOSSARY GATE CAUGHT `$$アルテア$$` AGAIN, in three records of one slice.
  `アルテア` has been settled as plain "Altair" since stage 85 and has no
  glossary entry, so `check_stage.py` refused it and the slice corrected all
  three before reporting. That is the second stage running where the checker
  stopped a bad token inside the slice rather than in review.
- THE STAGE 90 BANNER FIX HAS PROPAGATED. The D-Trader banner's 11-space form
  is now the majority at 55 of 114 copies, up from the 52 it was corrected to,
  so slices reaching for the majority now land on it without being told.
- Two renderings are recorded as judgment calls rather than settled, because
  the corpus has no clear majority for either: a bare `フフ…` from Crea is
  "Heh heh..." (4 of 7 instances of that exact string), and a bare `はあ…`
  sigh is "Haah..." against roughly fifteen scattered shipped forms.
- Also settled: `１００ＺのＺチップ` is "100 Z-Chips" on the `３００Ｚ` pattern;
  AG's `ゼウス様` is "Master $$ゼウス$$"; `オリュンポスの神` is "a god of
  Olympus"; `地獄帰り` is "back from hell"; bare `勇者` is plain "heroes",
  only `勇者ガラダブラ` being keyed.
- Registered into the shared catalog: 523 compatibility views, 0 issues, and
  `sync` reports nothing to change. Stage 93 is now complete at 1,210 records
  across both branches.

## Stage 93A translated (1,006 records) (2026-09-17)

- STG0093A members 3 (79 records) and 4 (927), nine slices. Both pass
  `check_stage.py` and `check_names.py` clean and every `$$` token expands.
  931 unique shas, no sha answered two ways across a slice boundary, and none
  of the 709 that also ship elsewhere diverges.
- REUSE RANGED FROM 18% TO 100% ACROSS THE NINE SLICES, which is the material
  rather than the method: the opening members replay established scenes and
  two slices were pure reuse end to end, while the Hades and Aquarion battle
  arcs in the middle are almost entirely new.
- A SLICE CAUGHT A CLASH `merge_stage.py` COULD NOT HAVE SEEN. Two slices
  independently first-drafted the same unshipped sha, and the merge would have
  taken whichever file was listed first. The later slice compared the sibling
  answer files sha by sha, found the divergence, and conformed to the earlier
  wording rather than leaving one Japanese line with two Englishes.
- CHECKING REUSE BLOCK BY BLOCK WOULD HAVE SHIPPED WRONG LINES. This stage
  repeats battle scenes with small divergences: one slice found a block where
  35 of 36 lines shared a sha with an earlier block and 7 records inside it
  were genuinely new. The sha is the only thing that tells you, and that
  warning went into the remaining slices' prompts.
- A GENUINELY TIED SHA WAS RESOLVED BY DOCTRINE AND REPORTED. `了解！` ships
  1-1 between the plain military "Roger!" and the character token. The slice
  took the plain form because the rule settles it, and flagged the tie; the
  audit that followed is the commit above.
- The tokeniser moved three records onto tokens, each read before accepting:
  two names written as literal English inside a line that already used tokens,
  and a full name the line spelled out. Each round-trips to identical text.
- `ミーナ` was marked AMBIGUOUS and resolved to `$$ミーナ#182$$`, the Macross
  Quarter's operator rather than the astrophysicist, from the bridge crew in
  the scene. `堕天翅` is `$$堕天翅$$`; `理事長` in direct address is
  "Chairwoman $$クレア$$"; `光の巨神` and `光の魔神` are "giant god of light"
  and "demon god of light"; `精神波` is "mental wavelength"; `三大神` is
  "Three Great Gods".
- THE SLICE RULES NOW LIVE IN `work/tr/SLICE_RULES.md` rather than being
  pasted into every prompt. They had grown past 6,000 tokens per slice, and
  stage 93 alone needed twelve.
- Registered into the shared catalog: 521 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## A sixth military "Roger" was filed under the character token (2026-09-17)

- `stage0086_04` record 406: Alto's `了解！` shipped as
  `$$アルト$$「$$ロジャー$$!」`, putting a military acknowledgement under the
  glossary token for Roger Smith. Now plain "Roger!".
- NOTHING CHANGES ON SCREEN TODAY -- the token expands to "Roger" either way.
  The defect is latent: renaming the glossary term would have rewritten an
  acknowledgement that has nothing to do with the character.
- FOUND BECAUSE THE SHA WAS GENUINELY TIED. A stage 93A slice hit this line as
  a 1-1 split between the plain wording and the tokenised one, resolved it by
  doctrine rather than by coin-toss, and reported the tie. A corpus-wide audit
  then confirmed this was the only survivor.
- The entry for stage 86 below claimed the ordinary-word guard meant this
  "cannot recur"; that claim is corrected there. The guard only constrains the
  automatic tokeniser, not a slice writing a token by hand.
- Edited by message ID with the definition's `tokens` list updated to match;
  `sync --write` regenerated the one affected view. 519 views, 0 issues.

## Stage 92 translated (629 records) (2026-09-17)

- STG0092 members 3 (246 records) and 4 (383), five slices. Both pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token expands.
- THE CLEANEST STAGE SO FAR: 596 unique shas, no sha answered two ways across
  a slice boundary, and not one of the 511 shas that also ship elsewhere
  diverges from the shipped wording.
- REUSE WAS 86%, and one slice was 111 of 111 -- this stage replays earlier
  scenes, so a slice that had translated rather than checked would have
  rewritten lines that were already on screen.
- A TILDE WAS ABOUT TO BE WRITTEN INSIDE AN ENGLISH WORD. A slice rendered
  `い、いか～ん！` as "T-this won't d～o!". The fullwidth tilde is drawable, so
  the checker passed it, but every other use of it in the corpus wraps a
  location banner (`～ Paradigm City ～`) and this would have been the only one
  inside a word. That part stands.
  LATER CORRECTION (2026-09-17): the replacement was "T-this won't dooo!",
  justified here as "the rule the project already uses". THAT JUSTIFICATION
  WAS WRONG. The corpus drops a tilde elongation 173 times to 30; it keeps a
  stretch only where the stretch IS the utterance. The record now reads
  "T-this won't do!" and the rule is fixed -- see the entry above.
- THE GLOSSARY GATE CAUGHT A BAD TOKEN IN THE SLICE, NOT IN REVIEW. A slice
  wrote `$$アクエリオン$$`; `check_stage.py` refused it, because bare
  `アクエリオン` has no entry and only compounds are keyed; the slice corrected
  it to plain "Aquarion" and said so in its report.
- Four slices met the AMBIGUOUS cast marker on `ドロシー` and all four
  resolved it to `$$ドロシー#240$$` from Roger, Schwarz and Big O markers in
  the scene; `レイ` beside Shinji and Asuka went to `$$レイ#333$$`.
- "Wings of the sun" was checked rather than assumed: the corpus writes "the"
  mid-sentence, "The" sentence-initially and no article when the phrase stands
  alone, which is not a conflict and needed no change.
- Also settled: `箱庭` "sandbox", `憎しみの三角形` "triangle of hatred",
  `冥府の王` "King of the Underworld", `オリュンポス` "Olympus", `無限の力`
  "infinite power".
- Registered into the shared catalog: 519 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## The F.S. speaker name now reads the same in all 160 records (2026-09-17)

- 19 records across stages 17, 81, 83, 85a, 87, 88a, 88b and 89a printed the
  speaker name as plain fullwidth `Ｆ．Ｓ．`; the other 141 used the glossary
  token. All 19 are now on the token, so the name renders identically
  everywhere and follows a future rename of the term.
- WHAT SHIPPED BEFORE AND WHY IT CHANGED: those records were written under a
  `CONVENTIONS.md` note that stated the rule backwards -- "plain fullwidth
  text, 136 shipped records to 0" -- when the corpus was 135 tokenised to 19
  plain. The note was corrected during stage 91, which is the entry above.
  Nothing is being retranslated here: only the speaker line on line 1 of each
  record changes, and only from one spelling of the same name to another.
- On screen the name goes from 124 px to 50. Fullwidth Latin occupies a 31 px
  CJK cell per character and is absent from the Latin font (as is hiragana,
  which the game draws from a CJK font, so this was a width and consistency
  fault rather than a missing glyph).
- Edited in the catalog by message ID, in `localization/locales/en/`, with the
  matching `tokens` list updated in `localization/messages/` -- `sync` refuses
  a locale edit that adds a token the definition does not declare. `sync
  --write` then regenerated exactly the 8 affected compatibility views and no
  others; 517 views, 0 issues.
- ONE OF THOSE VIEWS HAS A 1,964-LINE DIFF FOR A 3-LINE CHANGE.
  `translation/stage0017_03.json` was a pre-migration file still stored with
  CRLF, and `sync` always renders a view it rewrites with LF. It compares
  PARSED JSON, not bytes, which is why the file sat unflagged for so long and
  why nothing else moved. Verified record by record: exactly 3 of its 245
  records differ, all of them the speaker line. The rest of the diff is the
  line ending and nothing else.

## Stage 91 translated (501 records); a convention note was backwards (2026-09-17)

- STG0091 members 3 (89 records) and 4 (412, four slices). Both pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token expands. 313 of 437 unique shas were already
  shipped and reused; one member ran 95%.
- A SLICE CAUGHT A CONVENTION NOTE OF MINE THAT WAS WRONG. `work/tr/
  CONVENTIONS.md` said `Ｆ．Ｓ．` as a speaker "is left as plain fullwidth
  text, 136 shipped records to 0". The corpus is the other way round: 135
  records use the token `$$Ｆ．Ｓ．$$` and 19 use plain fullwidth. Both the
  form and the count were wrong. The slice noticed because a line it reused
  contradicted its own brief, and reported it instead of following the brief.
- THAT NOTE HAD BEEN GOING INTO EVERY BRIEF SINCE STAGE 75, which is how
  stages 81, 83, 85a and 87 came to write the plain form. The note is now
  corrected. Stage 91's own five plain records were moved onto the token
  before registration, so this stage is internally consistent; the 19 already
  committed records are a separate sweep, not done here.
- The plain form is not a broken glyph -- the Latin font has no fullwidth
  Latin, but neither does it have hiragana, and the game draws those from a
  CJK font. What it costs is width and consistency: 124 px against the
  token's 50, and a speaker name that renders one way in 19 places and
  another in 135.
- `ふ、深い！` WAS NOT A STUTTER. A slice read the comma after a single mora
  as a stammer and wrote "D-deep!". The neighbouring records are a comedy
  beat: Bonta-kun speaks only in `ふも` sounds and the Space Demon King is
  echoing that `ふ` while calling the speech profound, then says "Deeper than
  my black hole!". Now "Fu, so deep!". A COMMA AFTER ONE MORA IS USUALLY A
  STAMMER, BUT NOT WHEN THE MORA ECHOES THE PREVIOUS SPEAKER.
- Two shas were answered two ways across a slice boundary. `邪魔をするのか、
  宇宙魔王！` was settled by a near-exact shipped precedent, `あの少年、我々の
  邪魔をするのか！` -> "Is that boy going to get in our way!?", which matched
  one slice's verb and the other's punctuation, so neither answer was taken
  whole.
- Registered into the shared catalog: 517 compatibility views, 0 issues, and
  `sync` reports nothing to change.

## Stage 90 translated (347 records) (2026-09-17)

- STG0090 members 3 (62 records) and 4 (285, three slices). Both members pass
  `check_stage.py` and `check_names.py` clean, the tokeniser found nothing to
  move, and every `$$` token in the stage expands.
- THE FOUR SLICES DID NOT DISAGREE ONCE. 313 unique shas, no sha answered two
  ways across a slice boundary -- the first stage of the project where the
  cross-member comparison found nothing to settle. Two slices checked the
  sibling answer files directly and reconciled their two shared shas before
  reporting.
- REUSE FELL TO 85 of 313 shas (27%), against 71-88% in stage 89. That is the
  material, not a regression: this stage is a late-game boss sequence in which
  most of the cast challenges Gura in turn, and those lines occur nowhere else
  in the script. The tail slice found exactly one shipped sha in 45 records.
- A LOCATION BANNER WAS REPORTED AS THE MAJORITY WITHOUT BEING COUNTED. The
  D-Trader banner ships in eight indentations; the slice wrote the ten-space
  form and reported it as the majority, which is the six-copy variant. The
  cross-corpus sha comparison caught it and it was moved to the 52-copy form,
  which is also the source's own indentation. The check that found this runs
  on every stage and is the reason the claim was not taken at its word.
- `太陽の翼` LOOKED LIKE A SLIP AND WAS NOT. "Wings of the sun", with that
  capitalisation, is what all eighteen shipped records spell, so it stands.
- `先生` addressed to Gura is plain "Sensei": the glossary's `先生` is the
  Shin Mazinger swordsman, Gura is Tetsujin 28, and no Mazinger marker is in
  the scene. Four records whose speaker is `？？？` kept the literal `???`
  although the portrait named the character -- one of them immediately before
  the script reveals the name.
- Also settled: `心の中` "heart", `殺し合い` "killing spree", `商売、商売！`
  "business, business!", `飢える破壊魔` "hungry destroyer", `果てなき破壊の化身`
  "embodiment of endless destruction", `魔獣王子` "Demon Beast Prince",
  `ナナヒカリ` "Daddy's Boy" (not the `ヒカリ` entry), and `カグラァァァァァッ`
  written plain because an elongation breaks the token.
- Registered into the shared catalog with `register_localization_stage.py`:
  515 compatibility views, 0 issues, and `sync` reports nothing to change.

## Stages 89A and 89B translated (737 records) (2026-09-17)

- STG0089A (197 records, two slices) and STG0089B (540, five slices). All four
  members pass `check_stage.py` and `check_names.py` clean, with no
  cross-member clash, no sha differing from shipped text, and no stutter
  mismatches in either stage.
- THE CAST-SHEET FIX WAS EXERCISED AND WORKS. Four names came up marked
  AMBIGUOUS and all four were resolved from scene evidence -- three of them
  the same `レイ` pair that produced the wrong character in stage 88, where
  the sheet had silently shown one biography and a slice believed it. One
  slice noted the portrait happened to agree with its reading and settled it
  from the surrounding dialogue anyway, which is the right habit: the portrait
  is a lead on the days it is right and on the days it is not.
- REUSE WAS THE HIGHEST OF THE PROJECT SO FAR: 88%, 83%, 79%, 71% and 88%
  across the finished members -- one member was 107 of 122 shas already
  shipped, with 15 genuinely new records. The cached table establishes that in
  one pass per slice instead of leaving it to be rediscovered line by line.
- Five shas were answered two ways where a scene repeats across a slice
  boundary, all settled against the Japanese: `悲しげ` glossing a musical term
  is "sorrowful"; `使命感` is a SENSE of duty and `響く` is "ring out"; but
  `尽きる` is "running out" rather than "fading away", and `俺と同じように`
  compares the speaker to himself rather than to his power -- so that one kept
  the other slice's wording.
- The tokeniser moved three records onto tokens, each read before acceptance:
  character names written plain in dialogue where the name is a glossary key.
- The percent rule recorded in stage 87 caught a live case: a slice wrote out
  "4.63 percent" rather than the percent sign, which the font cannot draw.
- Catalog after registration: 0 issues, 513 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added both stages' members 3
  and 4 to the build, deploy, extract and xdelta tables. Not built.

## Stages 88A and 88B translated (610 records) (2026-09-16)

- STG0088A (500 records, five slices) and STG0088B (110, two slices). All four
  members pass `check_stage.py` clean, with no merge conflict anywhere, no
  cross-member clash, no sha differing from shipped text, no stutter
  mismatches, and nothing for the tokeniser in either stage.
- `check_names.py` CAUGHT A WRONG CHARACTER. Two slices assigned different
  discriminators to the same portrait in the same member: one read a line as
  Macross 7's Ray Lovelock, the other as Evangelion's Rei Ayanami. Reading the
  surrounding scene settled it -- the records are a rotating multi-series
  council, one line each from a dozen casts, and the only series marker
  anywhere near the disputed line is Shinji IMMEDIATELY BEFORE IT, with no
  Fire Bomber presence in the whole window. Corrected to Rei Ayanami.
- THE SLICE THAT GOT IT WRONG TRUSTED THE BRIEF'S CAST BIO. CORRECTION TO
  THIS ENTRY AS FIRST WRITTEN: I said the generator attaches bios by
  portrait id. It does not, and its own comments warn against keying on
  `pid` because the portrait is not the speaker. The real defect was
  narrower: `cast_for` looked a printed name up in the glossary and took
  `pil[0]` -- the first candidate -- for both the English name and the
  biography. For a name belonging to two characters from different series,
  that silently picked one with no ambiguity shown. Fixed in
  `tools/export_stage.py`: the sheet now carries EVERY candidate, marks the
  name AMBIGUOUS, and prints each one's discriminator token beside its own
  biography. The other two failures (a wrong rank in stage 78, a wrong
  series' bio in stage 75) are separate and still stand as reasons to read
  the scene rather than the sheet.
- A slice resolved that same ambiguity from the text instead: a later record
  spells the character's name out in full, which settles it without reference
  to the portrait at all.
- The `roger` guard added last stage held under its hardest case: a line whose
  SPEAKER IS ROGER and whose Japanese is `了解だ`. Every surface cue points at
  the token; the slice wrote "Understood" plain, correctly.
- Slices caught their own defects again: a term tokenised out of habit that
  has no glossary entry, two question marks added where the Japanese has no
  interrogative, and a pronoun drafted onto a line whose Japanese omits one.
- Catalog after registration: 0 issues, 509 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added both stages' members 3
  and 4 to the build, deploy, extract and xdelta tables. Not built.

## Stage 87 translated (682 records) (2026-09-16)

- STG0087 translated in six slices: member 3 (135 records, one slice), member
  4 (547, five slices). Both members pass `check_stage.py` and
  `check_names.py` clean, with NO merge conflict anywhere -- the first
  five-slice member to manage that -- no cross-member clash, no sha differing
  from shipped text, and no stuttered name disagreeing with its own expansion.
- Each slice's settled decisions were fed into the NEXT slice's prompt rather
  than held for the merge, so the epithets, address idiolects and
  first-instance renderings established early were handed forward. The later
  slices reported needing no new coinages, where five slices sharing one
  antagonist's vocabulary would otherwise each have invented parallel terms
  for the merge to reconcile.
- THE PERCENT SIGN IS NOT DRAWABLE, which had not come up before. A slice
  wrote a literal "10%", caught it in its own scan and reworded it; the font
  has no glyph, so it would have drawn as nothing. Recorded with the rest of
  the drawable set.
- Slices caught four more defects in their own output before the merge: a name
  needing a `#pilot` discriminator, another written as a token when only its
  compound form is keyed, and three question marks added to lines whose
  Japanese ends assertively rather than interrogatively. One slice then
  verified programmatically that no other line in its file had the same fault.
- `宇宙の魔王`, with a particle inserted, was correctly left plain as a
  different string from the keyed `宇宙魔王`.
- The tokeniser moved one record onto a token, read before accepting: a
  character naming himself in dialogue, where the in-line mention should match
  the speaker line.
- Catalog after registration: 0 issues, 505 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0087 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 86 translated (966 records); a military "Roger" filed under a character (2026-09-16)

- STG0086 translated in eight slices: member 3 (232 records), member 4 (734).
  Both members pass `check_stage.py` and `check_names.py` clean, with no sha
  differing from shipped text, no stuttered name disagreeing with its own
  expansion, and nothing for the tokeniser to put back.
- A SLICE FOUND A SHIPPED DEFECT BY READING THE TEXT IT REUSED. `了解！` and
  `ラジャ` -- a military "Roger!" -- had been swept into the glossary token
  for Roger Smith of The Big-O in five shipped records across stages 3, 9 and
  10. The token is correct in the 282 records whose Japanese actually names
  him; these five are the same failure the tool's own docstring warns about
  for `先生`. Corrected, and `roger` added to the ordinary-word guard. The
  slice reused the shipped text as the rules require AND flagged it as
  suspect, which is exactly the behaviour that makes this findable.
  LATER CORRECTION (2026-09-17): this entry said the guard meant it "cannot
  recur", which was wrong. The guard is in `tokenise_stage.py` and only
  stops the AUTOMATIC tokeniser; it cannot stop a slice from typing the
  token by hand. A sixth record was found in stage 86 itself -- the stage
  this entry documents -- and is fixed in the entry above.
- THE CATALOG REFUSED MY FIRST ATTEMPT AT THAT FIX, correctly. Each message
  definition records the tokens its English must contain, so removing a token
  from the wording alone left the two disagreeing; `localization.py sync`
  raised and wrote nothing rather than emit a view that contradicts its
  definition. The correct edit touches both the locale text and the
  definition's `tokens` list.
- THE CACHE CANNOT SEE THE BATTLE-SUBTITLE OR WEAPON FILES, because they have
  no `sha`. Three times this stage a slice coined a term that was already
  established in them, and a later slice found the real rendering by searching
  Japanese text: `ドン底女` ships as "Wreck" 7-1, where two slices had written
  "gutter girl" and "down-and-out woman". Corrected, and the instruction is
  now in the brief template and the prompts.
- `ポロン` ships as "Polon" 7-1. Stage 83 shipped one "Poron" -- an
  inconsistency inside a stage I registered earlier today -- and a stage 86
  slice matched that outlier. Both corrected.
- Twenty-three shas were answered two ways where a scene repeats across a
  slice boundary, and one more disagreed across MEMBERS, which
  `merge_stage.py` cannot see. All settled against the Japanese: `因果律` is
  the settled single word "causality", `何だと` is a challenge rather than a
  plain "what", `支配` is "ruled" rather than "consumed", and a line that uses
  both `星` and `世界` needs two different English words rather than one.
- Catalog after registration: 0 issues, 503 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0086 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stages 85A and 85B translated (580 records); branch halves are not variants (2026-09-16)

- STG0085A (189 records) and STG0085B (391) translated in six slices. All four
  members pass `check_stage.py` and `check_names.py` clean, with no
  cross-member clash, no sha differing from shipped text, no stuttered name
  disagreeing with its own expansion, and NOTHING for the tokeniser to put
  back in either stage.
- A CORRECTION TO MY OWN EXPECTATION: I sequenced this batch on the assumption
  that an A/B branch pair shares most of its scenes, so 85A was merged,
  verified and REGISTERED as soon as its two slices landed, and the sha cache
  rebuilt, so that 85B's remaining slices would find the shared lines already
  shipped. They did not exist. 85B reused exactly ONE record from 85A across
  391; three of its four slices reported zero overlap. The halves are
  different scripts, not variants of one scene set. Registering A early cost
  nothing and is still a reasonable default, but the remaining branch pairs
  (88, 89, 93, 98, 100) should not be planned as though the second half is
  cheap.
- `アルテア` was tokenised by THREE separate slices before `check_stage.py`
  stopped each of them. It has no glossary entry at all and is plain "Altair".
  That makes it the most repeated mistake of the stage, and it is now in the
  conventions file and in the slice prompts.
- Slices caught their own defects before the merge in every case this time:
  the three `アルテア` tokenisations, a record that ran to five lines, and a
  fullwidth `ＹＦ－２９` that had to become ASCII because fullwidth Latin is
  not drawable.
- Cleaned four stray scratch files out of the project root, left by earlier
  slices despite the standing instruction to write only their answer file.
  They were corpus-lookup output and one empty file, all untracked, so nothing
  was at risk of being committed. The slice prompts now name the system temp
  directory explicitly rather than only forbidding the project tree.
- THE REMAINING-WORK COUNT WAS OFF BY ONE. Counting the disc against what is
  registered gives 96 of 116 story scripts done after this batch, not the
  running tally I had been quoting. The derived count is the one to trust.
- Catalog after registration: 0 issues, 501 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0085A and STG0085B
  members 3 and 4 to the build, deploy, extract and xdelta tables. Not built.

## Stage 84 translated (617 records); the shipped table is now cached (2026-09-16)

- STG0084 translated in five slices: member 3 (279 records), member 4 (338).
  Both pass `check_stage.py` and `check_names.py` clean, with no cross-member
  clash and no stuttered name disagreeing with its own expansion. Member 3
  merged with no corrections at all.
- New `tools/shipped_index.py` caches the shipped `{sha: english}` table to
  `work/tr/shipped.json` once per batch: 38,026 shas from 221 files. Every
  slice had been rebuilding that table by reading the whole corpus, and six
  slices doing it in parallel is what a usage limit killed mid-scan in stage
  83 -- all six died during the survey, before writing a single record. The
  brief template now loads the cache in one line and says not to rebuild it.
- The index also records `others` and `tied` per sha, so a slice can see that
  a wording is contested without re-deriving the counts. Two slices hit the
  same 1-1 tie this stage and both correctly reported their pick as a pick.
  IT ALSO PUTS A NUMBER ON THE DRIFT: 587 shas already ship more than one
  wording. Not swept -- most are likely harmless near-synonyms -- but the
  list is now bounded rather than discovered one record at a time.
- A slice flagged two renderings it was unsure of, and the corpus split both
  BY SPEAKER rather than by majority: Hades alone says "wheel of rebirth"
  where everyone else says "ring of fate", and Garadabura says "Master
  $$ハーデス$$" 4-0 where the Mycenaean God says "Lord $$ハーデス$$" 4-0. The
  first flag was right as written; the second had a Mycenaean God line using
  "Master", which was corrected. A single shipped record can establish an
  idiolect, so the check is who is speaking, not which wording is commoner.
- `天翅` was coined as "Divine wings" where stage 83 had already shipped "the
  Wings"; aligned, and its second line fixed from a question word order that
  read as ungrammatical with a final exclamation mark.
- One record was written with an honorific the shipped record drops.
- Slices caught three defects in their own output before the merge: four
  records tokenising a bare name that is not keyed, three needing the
  `#pilot` discriminator the checker demands, and a set of question marks
  drafted where the Japanese has none.
- Catalog after registration: 0 issues, 497 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0084 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 83 translated (1,066 records), the largest script in the game (2026-09-16)

- STG0083 translated in ten slices: member 2 (1 record), member 3 (679),
  member 4 (386). All three members pass `check_stage.py` and
  `check_names.py` clean, with no cross-member clash, no sha differing from
  shipped text, and no stuttered name disagreeing with its own expansion.
- Member 2 is the fifth `SC_UNIT_JOIN_TO_TAG` formation label, shipping as a
  bare "Gundam" with no speaker, quotes or token. Five decoy copies sit in
  `--|` dev comments that `luarec.py` does not extract.
- Unlike stage 82, this stage is mostly ORIGINAL material: its slices found
  only 8 of 88, 14 of 110, 16 of 115, 8 of 55, 13 of 70, 8 of 117, 4 of 114
  and 10 of 146 records already shipped. The reuse pass is worth running
  either way -- it is how the low rate was established rather than assumed.
- A slice tokenised two records whose Japanese says `アポロニアス` with the
  glossary entry for `アポロン`. Those are different names for different
  incarnations of the character, so the token would have put "Apollon" on
  screen where the source says "Apollonius". Corrected, and the one record
  whose Japanese really does say `アポロン` kept its token. The evidence was
  in the source text, not in either slice's argument.
- The same term appeared as a third spelling, "Machine Angel", in three
  records; the corpus ships "Mechanical Angel" 31 times to 3.
- CORRECTION TO A RULE I WROTE: the conventions file said `機械天使` was a
  lowercase "mechanical angels", taken from one slice's coinage rather than
  from the corpus. It is capitalised, 31-3, and the wrong note had already put
  one lowercase record into stage 81. Both the note and that record are fixed.
  Where the conventions file and the shipped corpus disagree, the corpus wins
  and the note is the thing that is broken; the briefs now say so.
- CORRECTION TO THE BRIEF TEMPLATE: the reuse script it carries globbed
  `translation/voice_*.json` alongside the stage files, but battle subtitles
  have no `sha` at all -- they are a `lines` dict of `{jp, en}` -- so that
  half of the glob silently contributed nothing. It now scans only the stage
  files and says explicitly that voice files are searched by Japanese text
  for terminology. A slice found the only existing rendering of `太極` that
  way, which is how the gap surfaced.
- Thirteen shas were answered two ways where a scene repeats across a slice
  boundary. All thirteen were settled against the Japanese rather than by
  preference: the pause in `私は…もう` belongs after "I", `人生` is a life and
  not just a path, `最後の一人` is one person, and `話す気はない` is an
  unwillingness to speak rather than having nothing to say.
- Six slices were lost earlier to a usage limit, all of them killed during the
  corpus reuse scan before writing a single record. Nothing committed was at
  risk. They were relaunched in waves of three instead of six, writing after
  every ~15 records instead of ~20.
- Catalog after registration: 0 issues, 495 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0083 members 2, 3
  and 4 to the build, deploy, extract and xdelta tables. Not built.

## Stage 82 translated (407 records); the reuse pass moved into the brief (2026-09-16)

- STG0082 translated in four slices: member 3 (226 records), member 4 (181).
  The merged stage needed NO corrections at all: no merge conflict, no
  cross-member clash, no sha differing from shipped text, nothing for the
  tokeniser to put back, no suspect names. That is a first.
- The reason is that each slice built the reuse table in one pass before
  translating anything, rather than checking line by line as it went. They
  reused 49 of 108, 65 of 94, 48 of 114 and 39 of 61 shas -- this stage
  replays large parts of stages 79 and 80, and one member 4 branch is 30
  records of stage 80 verbatim. Stage 81 checked line by line and shipped 28
  re-worded records that had to be corrected afterwards.
- Moved that instruction OUT of the slice prompt and INTO the brief template
  in `tools/export_stage.py`, where the per-line rules already live, so it
  applies to every future stage rather than depending on how a batch was
  briefed. It sits before the numbered rules as its own section, since it is a
  process step rather than a line rule -- and because renumbering that list
  has introduced a bug before.
- Two slices mistyped a Japanese codepoint while hand-writing `\uXXXX`
  escapes: one wrote the kanji for "cherry" where the character's name uses
  "katsura", the other turned `スパイラル` into `スパイレル`. Both surfaced
  only because `check_stage.py` could not find the resulting term. The fix in
  both cases was to write literal Japanese into the answer file instead.
- Catalog after registration: 0 issues, 492 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0082 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 81 translated (569 records); a stutter that repeated the wrong letter (2026-09-16)

- STG0081 translated in five slices: member 3 (416 records), member 4 (153).
  Both pass `check_stage.py` and `check_names.py` clean.
- 28 shas had been written fresh where the same Japanese already ships --
  an order of magnitude more than any earlier stage, because this stage
  replays whole scenes that ship elsewhere and the slices caught only some of
  them. All 31 affected record slots now carry the shipped English.
- CORRECTION TO STAGE 77, which this work uncovered: Banagher's stuttered
  `ロ、ロニさん` shipped as "R-$$ロニ$$", and the token expands to "Loni", so
  the line stuttered a letter the name does not begin with. It now reads
  "L-". The Japanese syllable is `ロ` and the English is "L" -- the two do not
  have to agree, which is exactly how the error survived review.
- Audited every stuttered name in the corpus against what its token actually
  expands to. 26 were right and that one was wrong; stage 81's own two
  stuttered names were checked the same way before registering.
- `姐さん` for Zessica and MIX was written "Big Sis" by one slice where the
  corpus says "Boss" 19 times to 3, and stage 79 had shipped "Boss" for these
  same two characters days earlier. Corrected, which needed the line rewrapped
  rather than a word swapped, since the phrase straddled a line break. Like
  the stage 78 rank split, this is invisible to the sha comparison: the
  records are different sentences.
- A slice reported that a line it copied from shipped text looked too long.
  It is not: `check_stage.py` measures real font pixels and `$$ $$` markup is
  never drawn, so a 72-character line of narrow letters passes. Confirmed the
  width check has been active all session rather than silently skipped for a
  missing font, which would have printed "0 problems" either way.
- Catalog after registration: 0 issues, 490 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0081 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 80 translated (457 records) (2026-09-16)

- STG0080 translated in four slices: member 3 (264 records), member 4 (193).
  Both pass `check_stage.py` and `check_names.py` clean, with no sha answered
  two ways within a member or across them.
- The tokeniser moved four records onto glossary tokens, and each was read
  before it was accepted rather than trusted to the round-trip proof, after
  stage 79 showed that proof cannot tell two people apart. Three were
  `シンジ君` written as plain "Shinji" -- a slice had found shipped records
  with the plain spelling and matched them, which is reasonable but not
  rename-safe. The fourth was Kittan's self-referential `このキタン様`, which
  now reads "this $$キタン$$", the same shape `ゲイツ様` was settled into.
- One record was written fresh where the same Japanese already ships, and
  differed from it by a single full stop. It now matches.
- The stage 79 surname rule held in both directions: a slice resolved bare
  `赤木` TO the token after confirming from the stage 19 scene that the
  speaker is Dai-Guard's Akagi, rather than over-applying the caution that
  keeps Evangelion's Ritsuko plain.
- Two slices tokenised a word that is not a glossary term at all -- `クロノ`
  in one, `ナナヒカリ` in the other -- and `check_stage.py` caught both before
  they reached the merge.
- Catalog after registration: 0 issues, 488 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0080 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 79 translated (495 records); a surname that belongs to two series (2026-09-16)

- STG0079 translated in five slices: member 3 (295 records), member 4 (200).
  Both pass `check_stage.py` and `check_names.py` clean, with no sha answered
  two ways within a member, across members, or against shipped text.
- `tokenise_stage.py` tried to put Evangelion's Ritsuko Akagi under the
  glossary entry for Dai-Guard's Akagi Shunsuke. The two share a surname, the
  glossary holds only one `赤木`, and both expand to "Akagi" -- so neither the
  ordinary-word guard nor the round-trip proof could see the difference, which
  is exactly the blind spot the tool's own docstring warns about. Three
  records were reverted by hand.
- Added a `SHARED_SURNAME` guard for that class: the term is still offered
  everywhere except where the record carries the evidence that it means the
  other person. For `赤木` that evidence is `博士`, since Dai-Guard's Akagi is
  not a doctor. Verified both directions -- Dr. Akagi is left plain and the
  Dai-Guard character still tokenises.
- Checked whether this had already shipped. It has not: `赤木博士` appears in
  no shipped record, so stage 79 is its first appearance and there was nothing
  to sweep. A first search suggested 75 suspect records, but reading them
  showed they are the Dai-Guard character talking WITH Shinji in crossover
  scenes -- correctly tokenised. The mention of an Evangelion name in a record
  is not evidence that the scene is Evangelion's.
- A slice flagged `仮設ケイジ` as an uncertain reading. It is Evangelion's EVA
  docking cage and the scene is Unit-03's activation test, so "the temporary
  cage" is right. First instance in the corpus; recorded so it is not
  re-derived.
- Catalog after registration: 0 issues, 486 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0079 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## One line of shipped dialogue said two different things (2026-09-16)

- Shinji's `はあ…` shipped as "Um... okay..." in stage 25 and "Uh... okay..."
  in stage 41. Same Japanese, so the same record identity, and the game
  therefore showed one line two ways. A stage 78 slice found it while looking
  for precedent. The stage 25 instance now reads "Uh... okay...", the form the
  other four instances use.
- FIRST CORRECTION MADE THROUGH THE SHARED CATALOG rather than by editing
  `translation/`. The edit is two lines in
  `localization/locales/en/stage0025_03.json` -- the wording, and a status of
  `reviewed` instead of `imported`, since the line is no longer the text that
  came over unchanged in the migration. `localization.py sync --write` then
  regenerated the one compatibility view it affects.
- The regenerated view is a 7,732-line diff for a one-line change. `sync`
  writes a view in its own shape, indent 2 with LF endings, while the file it
  replaces was written years earlier with indent 1 and CRLF. Nothing about the
  content moved but that one line; the noise is the format converging. It is
  committed on its own so it does not bury a stage's diff, and the next edit
  to this file will be a one-line diff.
- Catalog: 0 issues, 484 compatibility views, `check --compatibility` passes.
  Not built.
- STILL UNSWEPT, recorded in the conventions file: `translation/voice_133.json`
  renders `鉄の女` as "Iron Woman" where the corpus says "the Iron Lady". That
  one is a different sha, so it is a wording inconsistency rather than one
  record contradicting itself, and it was left alone.

## Stage 78 translated (521 records) (2026-09-16)

- STG0078 translated in four slices: member 3 (369 records), member 4 (152).
  Both pass `check_stage.py` and `check_names.py` clean.
- Two slices rendered Misato's `一佐` differently, one as "Colonel" and one as
  "Lieutenant Colonel", because the brief's own cast sheet gives the latter
  while the corpus ships "Colonel" 18 times and the other spelling never.
  The corpus wins; the member 4 record was corrected. This class of
  disagreement is invisible to the cross-member sha check, because the two
  records are different sentences.
- Three records were written where the same Japanese already ships: Rei's
  `はい…` (the corpus says "Yes..." 36-3, and the slice's "Okay..." matched
  neither), a scream, and Monica's enemy-wipeout line.
- The tokeniser put one record back on `$$アスカ$$`. It correctly declined
  bare `綾波` in the same line: only the full `綾波レイ` is a key, and the
  corpus ships the bare surname plain 62 times to 5.
- Both EVA slices hit the `pid_RAY_S` portrait trap, where the brief's cast
  section attaches Ray Lovelock's Macross 7 bio to every `レイ` line. Both
  resolved it from the scene and the shipped sha to `$$レイ#333$$`, Rei
  Ayanami. The portrait remains a lead and not evidence.
- The banner comma rule turned out to be about ships specifically: a vessel
  plus a room takes no comma, but NERV's shipped banners all read
  `NERV Headquarters, <room>`. Both shapes are correct for their own kind of
  place; recorded so the difference does not read as drift.
- Catalog after registration: 0 issues, 484 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0078 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 77 translated (715 records) (2026-09-16)

- STG0077 translated in six slices: member 3 (361 records), member 4 (354).
  Both pass `check_stage.py` and `check_names.py` clean.
- A scene that runs TWICE inside one member gets translated twice, by two
  different slices. Member 3 came back with 21 such shas and member 4 with 6,
  and `merge_stage.py` resolves them by keeping whichever answer file it read
  first -- which is arbitrary, not a judgment. All 27 were reviewed by hand;
  five of member 3's were switched to the other slice's wording (10 record
  slots, since each of those shas appears twice).
- The tokeniser put three more records back on `$$ロニ$$` after a slice wrote
  the name as literal English. Those were records only ONE slice answered, so
  the merge never saw a disagreement to report -- the tokeniser is the only
  thing that catches that class.
- `サイコミュ` normalised to the capitalised "Psycommu", which the corpus
  prefers 4-1; one record had the lowercase outlier's spelling.
- One record was written fresh where the same Japanese already ships, and now
  carries the shipped wording.
- Checked a slice's report that a record's source has an opening `「` with no
  closing `」`. It does -- confirmed against the raw Shift-JIS lua, not the
  brief. The corpus is consistent about this and splits by direction: a
  DOUBLED closing bracket is collapsed to one well-formed pair (stages 12, 27,
  76), a MISSING one is preserved exactly (stages 64, 68b). The slice's
  choice was right; the rule is now written down instead of re-derived.
- Both `$$アンチスパイラル$$` discriminators expand to the same string, so the
  `#keyword` / `#pilot` choice a slice flagged moves nothing on screen.
- Catalog after registration: 0 issues, 482 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0077 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 76 translated (446 records) (2026-09-16)

- STG0076 translated in four slices: member 3 (353 records), member 4 (93).
  Both pass `check_stage.py` and `check_names.py` clean, with no sha answered
  two different ways across members or across slices.
- One record was written fresh where the same Japanese already ships three
  times over; the shipped `Eh...` now stands in it too.
- The tokeniser put the new banner for Ronan Marcenas's office back on
  `$$ローナン・マーセナス$$`, which the slice had written as literal English --
  the same drift stage 75 produced twice. A full personal name is nearly
  always a glossary key.
- The `ネェル・アーガマ　通信室` banner ships in two shapes, one with a comma
  between ship and room and two without. The new record takes the form that
  matches both the majority and the written rule; the comma instance is the
  outlier and was left alone rather than swept.
- `register_localization_stage.py` could not write a group's first files: the
  line-ending-preserving writer added for stage 75 reads the file it is about
  to replace, and a new message or locale file has nothing to read. It now
  treats a missing file as empty and uses the platform ending. The failed run
  rolled back completely -- no partial group, no touched control file.
- Catalog after registration: 0 issues, 480 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0076 members 3 and 4
  to the build, deploy, extract and xdelta tables. Not built.

## Stage 75 translated (627 records); first stage registered in the shared catalog (2026-09-16)

- STG0075 translated in six slices: member 2 (1 record), member 3 (271),
  member 4 (355). All three pass `check_stage.py` and `check_names.py` clean,
  with no sha answered two different ways across members.
- Member 2's lone record is the `SC_UNIT_LEAVE_FROM_TAG` formation argument
  and not speech, so it ships as bare `Londo Bell` with no speaker, quotes or
  token -- the same shape as the single member-2 records in stages 64, 70 and
  71. Four decoy copies of the same string sit in `--|` comments that
  `luarec.py` does not extract; only the live argument is a record.
- Three records had been written fresh where the identical Japanese already
  ships elsewhere. Since a record's identity is a hash of its Japanese, the
  shipped English now stands in all of them: `You are...` (was `You...`),
  AG's `Let's give it our all today too!` (was `Let's get fired up today
  too!`) and `N-no...` (was `N-No...`).
- `tokenise_stage.py` put two records back on glossary tokens: `ミネバ・ザビ`
  to `$$ミネバ$$ Zabi`, and `ローナン・マーセナス`, which a slice had written
  as literal English. Both round-trip to the same characters on screen.
- New `tools/register_localization_stage.py`. Stage 75 is the first stage
  finished after the 2026-09-14 migration, which imported the 475 legacy files
  in one pass and must not be rerun. The tool writes the four rows that
  migration would have written for a new dialogue group -- message
  definitions, English locale, manifest group, legacy binding -- mints IDs the
  way migration minted them (sha256 of the record's JSON pointer, so later
  wording edits keep the ID), and proves the group regenerates the checked
  file character for character before writing anything. It also writes the
  first `translation/<group>.json` view and its receipt, which `sync` cannot:
  sync reads the old view before rendering the new one, and for a first
  registration there is no old view. Registration is additive only; changing
  shipped English is an edit to the locale file by ID.
- Merge output went to `work/tr/STG0075/review/`, never to `translation/`,
  per the catalog rule that old merge tools must not write the canonical tree.
- The tool's first write normalised eight lines of `localization/manifest.json`
  that nobody had touched: the file is mixed CRLF/LF because more than one
  person edits it, and a whole-file rewrite converted another session's LF
  lines. Repaired to a three-line diff, and the writer now keeps each
  unchanged line's own ending, the rule `register_stage.py` already follows.
- Catalog after registration: 0 issues, 478 compatibility views, and `sync`
  reports nothing to change. `register_stage.py` added STG0075 members 2, 3
  and 4 to the build, deploy, extract and xdelta tables. Not built.

## PS3 boot crossover diagnostics 04/05 (2026-09-16)

- User reports diagnostic 01/02 load; English 03 still returns 80010001.
- Added an exact EBOOT crossover builder: 04 combines 03's English executable
  with 02's Japanese files; 05 combines 02's working wrapped executable with
  03's translated files. No new translation, wrapper or fix is introduced.
- Boot-only diagnostics: intentionally mismatched code/fonts/data must not be
  used for gameplay or loading/saving progress. Test the immediate launch error.
- Builder verifies source-image hashes and all 554 files through both output
  filesystem trees. Existing images and installations are left untouched.
- All 23 CFW packaging tests pass, including six new crossover tests. Hardware
  results for 04/05 remain pending; this is not a new release-version bump.

## Physical-Vita rePatch test16 staging package (2026-09-15)

- Added a changed-files-only rePatch builder and physical-Vita guide.
- Packaged 120 test16 game files (about 94 MB ZIP); no source game/module,
  license, firmware, plugin or save installation changes.
- INCOMPLETE pending console-dumped PCSG00264 v01.00 `self_auth.bin`.
  The `NEEDS-SELF-AUTH.zip` must not be installed yet. No hardware verification.
- Every package entry read back with size/SHA256/CRC checks; all 128 Vita tests
  pass, including eight new packaging tests. Game bytes match test16.

## Vita Intermission / Store / Scenario Select / test16 built (2026-09-15)

- Translate native word sprites: Intermission, Main Scenario, Tutorial Scenario.
- Translate the direct Clear footer label and blank the separate Scenario
  Select square while preserving its space and other icons.
- Correct PS Store's remaining left offset using the supplied Vita crop.
- All120 tests pass. Actual ZIP art, text, centering and prior UI/name checks
  pass;587 files unchanged from test15. No installation or live visual test.
- ZIP: `work/vita/english_vwf_test_16/SRW-Z3-Vita-English-VWF-test-16.zip`
  (1,872,598,616 bytes; SHA256
  `3a44d8f901af3f9aceab19d9ef44612568e00b59686985cd76ef21aa6b2b6ce8`).

## Vita End Phase remaining-team warning / test15 built (2026-09-15)

- Translate the composed warning as Teams still able to act: N., including
  the reported six-team case and every count the native formatter displays.
- Preserve count calculation, turn logic, Yes/No controls and dialog layout.
- All 117 Vita tests pass, including native formatting, rendering and centering.
  Shared catalog check has zero issues. Not installed or live-tested.
- Actual ZIP verified: only EBOOT differs from test14; all 588 other files
  and all prior translation keys/values remain unchanged. Packaged rendering,
  centering, chart artwork and runtime-name checks pass.
- ZIP: `work/vita/english_vwf_test_15/SRW-Z3-Vita-English-VWF-test-15.zip`
  (1,872,599,730 bytes; SHA256
  `792252bdf7a0c232a69eb508d4df41a0e643542d3428812bfb12455e044a164e`).

## Vita preset squad name / Team labels / test14 built (2026-09-15)

- Translate the reported preset name as Special Investigator using native
  preset discovery and existing shared translations; custom-name misses stay.
- Replace both split Team label variants without moving team values or stats.
- Retain every earlier translation key/value and all prior patched artwork.
- All 115 Vita regression tests pass; shared catalog check has zero issues.
- Packaged checks pass 328 UI and 23 library/chart drawing cases; all 589 files
  verified, with 587 unchanged from test13. Not installed or live-tested.
- ZIP: `work/vita/english_vwf_test_14/SRW-Z3-Vita-English-VWF-test-14.zip`
  (1,872,593,137 bytes; SHA256
  `b3ca400ccc978cdb1a6479f10b843fc67c5c46d3c7f8ee7e5cdbd2f3bfa75622`).

## Vita Power Parts / Network / test13 built (2026-09-15)

- Translate Power Parts headings/footer, Select Slot, Team and Network items.
- Shorten the parts-only Rep/Resup headers and Bonus Maps button to fit.
- Fix consumable filters inheriting SP Cost: use Use for consumables while
  preserving Spirit-list SP Cost via scoped aliases. Category indices stay.
- Retain prior artwork, stats, slot counts, inventory and online behavior.
- All113 tests pass; actual ZIP passes322 UI and23 library/chart drawing
  checks. All589 files verified;587 unchanged from test12. Not live-tested.
- ZIP: `work/vita/english_vwf_test_13/SRW-Z3-Vita-English-VWF-test-13.zip`
  (1,872,590,700 bytes; SHA256
  `f388772d129405a89272c9985b3b02b6fc547209d1a9f10daeedf8d9743d6f7b`).

## Vita Pilot List / upgrades / Library popup / test12 built (2026-09-15)

- Translate remaining list headings, DEF, Sight and Wpn Rank labels.
- Translate the five Intermission Library buttons and Options Library entry;
  retain the special text mode and existing artwork.
- Compact fixed-width Confirm/Back hints; preserve icons and input behavior.
- Only text slots change; numeric values, bars and widget coordinates remain.
- All111 tests pass; actual ZIP passes274 native UI and23 library/chart
  drawing checks. All589 files verified;587 unchanged from test11.
  Not installed or live-tested.
- ZIP: `work/vita/english_vwf_test_12/SRW-Z3-Vita-English-VWF-test-12.zip`
  (1,872,589,938 bytes; SHA256
  `1b0f0afefc70bfb3ef78bc0041f145dbb5ae79eb909e284e91fd1ae3874dcb8a`).

## Vita phase/rewards/Intermission / test11 built (2026-09-15)

- Match Yes/No layers at28px to correct the reported doubled No.
- Translate SR reward / bonus-funds messages and remove their redundant
  overlays. Tiny battle attack badge uses AT.
- Translate split Intermission menus and footer captions without changing
  values, button actions or unlocks. Prior artwork remains intact.
- All109 tests pass; actual ZIP passes180 UI and23 library/chart drawing
  checks. All589 packaged files verified;587 unchanged from test10.
  Not installed or live-tested.
- ZIP: `work/vita/english_vwf_test_11/SRW-Z3-Vita-English-VWF-test-11.zip`
  (1,872,588,849 bytes; SHA256
  `0da07bd181c047346e2f447fe757bbdda3eed78e083f31fefae90326a2adc1e5`).

## Vita battle Key Help / results / test10 built (2026-09-15)

- Translate the Right Stick help label and both split Unit result headings,
  plus their whole-word variant. Preserve input mappings and reward values.
- Scoped bindings and unique suffix blanking avoid global fragment changes.
  The matched UI/executable rebuild retains all test09 files and artwork.
- All107 tests pass; rebuilt UI archive and all589 ZIP files verified.
  Only UI archive member0 and EBOOT change. Not installed or live-tested.
- ZIP: `work/vita/english_vwf_test_10/SRW-Z3-Vita-English-VWF-test-10.zip`
  (1,872,587,604 bytes; SHA256
  `ada583745df2b797de758880e66fa8a89274d9b2a1905e234b2473b2b0c0780a`).

## Vita library / Scenario Chart / test09 built (2026-09-15)

- Translate reported glossary terms, series labels, library headings and
  sort hints. Compact library titles fit their original tabs; sort order,
  IDs and character-name identity are preserved.
- Translate Scenario Chart title/background lettering and complete episode
  captions. Use OK only in its crowded Confirm slot, plus Speed Up.
  Native chart navigation, unlock records, palettes and animations survive.
- Full rebuild includes every previous Vita fix. All 106 tests pass; all
  118 archives and 589 ZIP files verified. Packaged native drawing and art
  read-back checks pass. Only three output files differ from test08.
- Built `work/vita/english_vwf_test_09/SRW-Z3-Vita-English-VWF-test-09.zip`
  (1,872,587,498 bytes; SHA256
  `adbfa29fc203c5228d42fa89f135d6928dc0cb26cd8fa6b5fc73b3e4ebaed8bb`).
  Not installed or live-tested.

## Vita battle-preview Attack / test08 built (2026-09-15)

- Bind both narrow battle-preview buttons to the shared Atk. caption,
  with 16px clearance in the 94px native panel at conservative live pitch.
  Other Attack labels, counters, hit rates and battle behavior are unchanged.
- All 102 Vita tests pass. Built from hash-verified test07 output with an
  unchanged shared-catalog guard; all older fixes remain. Only EBOOT and
  AIDDataPack differ; rebuilt archive and all 589 ZIP entries verified.
  Not installed or live-tested.

## Vita roster/settings/Pilot Info follow-up / test07 built (2026-09-15)

- Replace narrow Settings tabs and roster headings with scoped compact
  shared labels; verify neighboring-column gaps at the runtime pitch instead
  of relying on a smaller requested widget font.
- Translate Move / Stats commands and the default Pilot Info full name.
  Explicitly bind native Stats / Ace Bonus widgets; leave locked question
  marks, custom names, gameplay values and selection behavior intact.
- Thirty source-bound native widget aliases support both encoding modes,
  with no pool growth or pointer changes. All 102 Vita tests pass and shared
  catalog validation has zero issues. Test07 built with all 118 rebuilt
  archives and 589 ZIP entries verified. Not installed; live checks remain
  needed.

## Vita post-prologue/search/name follow-up / test06 built (2026-09-15)

- Connect all 18 post-prologue narration rows to shared English without
  changing their native timing or record fields.
- Translate the default surname/first/nickname during native dialogue
  substitution, including both fully default full-name orders. Save buffers
  and custom names remain untouched.
- Add SP Cost / +Eff., map-search help / Back to Results, compact MV and
  HP/EN recovery captions. Preserve the SP value column and gameplay values.
- All 100 Vita tests pass, with dedicated native name-constructor and
  independent relocation coverage. Shared catalog validation has zero issues.
  Test06 built with all 118 rebuilt archives and 589 ZIP entries verified.
  Not installed; live-game verification remains required.

## Vita suspend/battle follow-up / test05 built (2026-09-15)

- Translate the complete nine-line Dancouga Nova suspend exchange, including
  Sakuya, Johnny, Kurara and Aoi. Shared canonical wording feeds both platform
  adapters; 16 of 872 suspend records are now translated.
- Fit both battle-preview Attack labels and four Foc/value states without
  shortening pilot names or modifying combat values. Includes prior Air and
  Spirit-status glyph fixes and every test04 change.
- All 97 Vita tests and the PS3 scene-isolation regression pass; shared-catalog
  checks report zero issues. Complete ZIP built with all 118 rebuilt archives
  and 589 ZIP entries verified. No installation or PS3 build/release change;
  live-game retesting remains required.

## Vita save/settings follow-up / test04 built (2026-09-15)

- Translate the Vita memory-card save destination and independently drawn
  save-confirmation lines using the shared locale catalog.
- Fit all eight System Settings 1/2 tab variants. Align all four native
  Yes/No active/background layers without changing selection behavior.
- Includes every test03 fix, including composed tactical episode headings.
  Installed executable still matches test02; no automatic installation.
- All 96 Vita tests pass and shared-catalog compatibility has zero issues.
  Full test04 ZIP built with 2,685 UI keys; all 118 rebuilt archives and
  589 ZIP entries verified. Not installed; live-game retesting is pending.

## Vita screenshot fixes / test03 built (2026-09-15)

- Fix native VWF keyword row corruption and proportional label centering.
- Include percentage-bearing Spirit/skill descriptions, native Lua mission
  conditions, numbered conditions,77 date cards and native episode headings.
- Add124 Vita title textures,83 location captions and5 episode effects.
- Fit Ally List/search/command/popup labels; add30 matched one-cell UI glyphs
  and19 native movement-label slots without changing status indexing.
- Add focused native CPU/content/scope regressions. Live-game validation is
  still required; this is not a PS3 release or a claim of a finished Vita port.
- All 95 Vita tests pass, with zero shared-catalog compatibility issues.
  Built work/vita/english_vwf_test_03/SRW-Z3-Vita-English-VWF-test-03.zip;
  all 118 rebuilt archives and 589 ZIP entries verified. Not installed because
  Vita3K remains running; the installed test02 and rollback ZIP are unchanged.

## PS3 boot diagnostic set built (2026-09-15)

- Three full, unsplit ISOs: original Japanese files repacked; Japanese with
  only the executable wrapper changed; existing English0.6.13 CFW contents.
- All554 files verified through both directory trees for each ISO. Enforced
  the one-file difference between Japanese controls and exact game-file hash
  equality between English test03 and the earlier CFW-test1.
- Added guarded diagnostic builder and test instructions;17 focused tests
  pass. Completion audit and full SHA256 checksums in
  work/ps3_boot_diagnostics_20260915. Existing files untouched.
- Diagnostic artifacts only, not a compatibility fix or release. Actual
  console boot remains pending; no firmware, saves or installations modified.

## Vita VWF test02 built (2026-09-15)

- Includes the title/Library artwork, startup-screen translations and opening
  narration fixes described below. All589 ZIP entries and118 rebuilt archives
  verified. Existing test01 retained.
- Installation preflight passed: four installed game files require updating,
  585 already match. Installation is waiting for Vita3K to exit; no installed
  files, saves or firmware changed. Runtime testing remains pending.
- Added a guarded installer with verified backups, atomic replacement and
  rollback; all five installer tests pass.

## Pending Vita opening-narration port (2026-09-15)

- Connect all28 shared English opening-narration lines, including the first
  four-line black-background page. This native Vita fixed-record container
  is separate from Lua dialogue and is member7, not PS3's member6.
- Guard the native source and match every Japanese identity; enforce the
  measured52-byte limit. Preserve page/timing/control data and every byte
  outside the new text and terminator. No padding, truncation or record growth.
- All10 focused narration/build-gate tests pass. Source-only change for the
  next Vita ZIP; nothing rebuilt/installed. Live rendering remains unverified.

## Pending Vita startup-screen translations (2026-09-15)

- Reuse nine shared scenario-selection/setup captions and exact Hibiki name
  aliases in the native Vita UI hook. Resolve short widget wording separately
  from longer help labels; leave other ambiguous translations excluded.
- Add shared blood-type displays, heading labels and numeric birthday format.
  Translate the two native heading sprites to Pilot Setup / Scenario Select;
  preserve palettes, UVs and neighboring art. Birthday display uses month/day
  without changing calendar values, editing logic or other date strings.
- Hook now covers1,523 native keys across24 groups. All24 focused startup,
  native CPU and build-gate tests pass, including372 numeric birthday cases;
  shared catalog has0issues and475 compatibility views remain unchanged.
- Source fixes only: no rebuilt ZIP, installation or release. Converted
  heading preview inspected; actual Vita3K rendering/alignment remains pending.

## Pending Vita title artwork and Library menu port (2026-09-15)

- User screenshots showed Japanese logo/subtitle and five Library buttons
  in Vita, despite their PS3 translations. Located native effvita.cpk member
  296: seven linear P8 textures with separate palettes, not PS3 GTF bytes.
- Added guarded title_art adapter using the approved shared wordmark/subtitle
  and existing locale-driven Library label renderer. Only indices in seven
  sampled rectangles change; native Z, palettes, headers, backgrounds and
  all5,655 animation samples remain unchanged. Quantizes against native
  palettes with alpha-aware matching; diagnostic atlases generated/reviewed.
- Wired adapter into the Vita ZIP planner and shared asset inventory; added
  source, isolation, region, palette and build-sink regression tests.
  All10 focused Vita title/build-gate tests pass. Native converted title and
  Library atlas previews were visually inspected; runtime remains unverified.
  No new ZIP/build, emulator install, PS3 asset or GitHub release changes.

## Pending PS3 Unit Info currency caption (2026-09-15)

- User reported Japanese top-right Funds/Chips header on Unit Info. Located
  both split-caption variants in pristine AIDDATAPACK member0 and added a
  shared locale message for "Funds / Z Chips:".
- Scoped PS3 adapter joins each caption into its first widget and suppresses
  its old Chips fragment;23px glyphs fit before unchanged numeric widgets.
  Source/record guards, mutation isolation and width checks are enforced.
  Wired into UI builder and release regression checks; added focused tests.
- All3 focused tests pass on pristine and existing0.6.13 UI buffers;
  shared catalog has0issues and all475 compatibility views remain consistent.
- Source-only fix: no build/version bump, install, ISO regeneration or GitHub
  release changes. Vita can reuse the message but no Vita layout fix claimed.

## PS3 0.6.13 GitHub publication (2026-09-14)

- User requested removal of the per-file English ZIP. Removed exactly
  SRW-Z3-English-0.6.13.zip and its .zip.sha256 asset from the private release;
  local copies retained, so both can be restored. Kept the two ISO xdelta
  assets unchanged. Removed ZIP download/instructions/checksums from release
  notes; updated README, release metadata, release documentation and handoff.
- Download follow-up completed: uploaded149,070,914-byte full ISO delta and
  14,825,869-byte exact0.6.3 update delta alongside the unchangedZIP/checksum.
  Both independently decode to the same4,996,823,040-byte0.6.13 image (MD5
  3259c2c80a98d846dcf775649990a561); all186files checked in both ISO trees.
  Release Downloads now follows the previous full/update/ZIP format, with
  sizes, original/previous/output hashes, commands and SHA256 list.
  GitHub notes match local; all four uploaded asset sizes/digests verified,
  v0.6.13 remains latest/non-draft/non-prerelease. Repository confirmed PRIVATE.
  Updated manifest, handoff, README and release docs; oldZIP not repackaged.
  No full ISO/game files, Vita files, commits or emulator changes uploaded.
- Further follow-up: user requested the previous release's download options,
  not just note formatting. Preparing full/from-0.6.3 ISO xdelta assets for
  RPCS3; no full game image will be uploaded. Added dry-run validation and
  explicit previous-ISO path support to iso_patch.py, avoiding duplicate
  copies of the preserved release_image_0.6.3.iso. Physical CFW package stays
  separate; these retain the legacy RPCS3 image format.
- Added two synthetic ISO-planner tests covering explicit previous-image
  selection, no-write dry-run, changed snapshot rejection, missing inputs and
  the required previous-version argument; both pass.
- All25 focused ISO/package/build-version/CPK tests pass. Public upload of the
  two new ISO patch assets was blocked by automatic permission review pending
  explicit payload/repository approval; approval requested. No upload or public
  notes change was made by the rejected call.
- User explicitly approved both patch uploads and clarified the repository is
  private. GitHub visibility verified PRIVATE (isPrivate=true); earlier
  references to public publication mean a published, non-draft release inside
  this private repository, not public access. Upload resumed with approval.
- Follow-up: reformatted public notes to match v0.6.3's title, introduction,
  Changes, Downloads, Scope and verification, and Download SHA-256 checksums
  sections. Kept actual available assets and compatibility/coverage warnings;
  no new ISO assets or patch content changes implied.
- User clarified that the requested release should be on GitHub. Published
  v0.6.13 on retro-trans/SRW-Z3 with only the verified85MB patch ZIP and its
  SHA256 file; no game files, ISO, Vita assets, commits or source push.
- Added public notes stating RPCS3 target, partial translation, no whole-ISO
  update asset, and that automatic source archives omit local uncommitted work.
  Draft upload and remote digest verification precede publication.
- Published as latest at2026-09-14T13:16:06Z:
  https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.13.
  Both remote sizes/SHA256 digests and notes matched before publication;
  public status, assets and latest-release endpoint rechecked afterward.
  Updated local manifest, README, release documentation and handoff status.

## PS3 0.6.13 release packaging (2026-09-14)

- User requested a PS3 release. Selected the existing validated
  work/build_0.6.13_batched_ui build rather than rebuilding or renumbering it;
  all190 build-manifest files verified before snapshotting186 deployed files.
- Added version-specific release/install notes distinguishing the RPCS3 ELF
  patch from the separate hardware-unverified CFW package. No ISO, Vita,
  installed game, saves, firmware, upload or public publication changes.
- package_release.py now accepts an optional --guide to include appropriate
  version-specific instructions while preserving its default behavior.
- Added three package-guide/dry-run/overwrite tests; all23 focused package,
  build-version and CPK tests pass. Original ISO MD5 and186 cached pristine
  file hashes verified before generating patches.
- Created releases/0.6.13.json and recoverable186-file local snapshot;
  generated186 from-original and113 from-0.6.3 patches, all decode-verified.
  ZIP releases/0.6.13_xdelta/SRW-Z3-English-0.6.13.zip is85,048,232bytes;
  all189 entries passed CRC and source hash readback. SHA256:
  65635a82bb66df19f23b64b79d1b3db1b47255a98c22e0f88856c9b520bc7b07.
  Added checksum, hash-only package metadata and updated release/handoff links.
  No public upload or emulator install. Build counter stays0.6.13;
  translation remains partial (1,034 missing mission-text variants).

## Vita VWF test ZIP builder (2026-09-14)

- User authorized a new Vita test build. Added build_vwf_zip.py to combine
  the native VWF/UI executable, matching single-letter fonts, story/library/
  keyword/gameplay data and paired SRVC/executable offsets from shared English.
- Category adapters now optionally emit verified bytes to a build consumer;
  their default CLI remains report-only. The legacy ZIP preparer can supply
  clean base files without applying the old fixed-cell pilot overlay.
- New-output-only, source/catalog guards, nested-error gates, CPK member
  readback and complete ZIP size/SHA256/CRC verification. Failed output keeps
  a .partial name until verified. No emulator install or save modifications.
- Added five focused builder safety tests and new VWF test instructions.
  All89 focused tests pass (66Vita,18localization,5CPK). Dry-run then build
  passed; all116 rebuilt CPKs and589 ZIP entries were read back and verified.
- Built work/vita/english_vwf_test_01/SRW-Z3-Vita-English-VWF-test-01.zip,
  1,874,654,431 bytes; SHA256
  0f7ba197c47c8c8a7f86e4cae33bfac6f7d6b2080257cdd54f2487b13cdceb6d.
  Includes116 translated/font archives, paired EBOOT/SRVC,5 converted native
  modules,466 unchanged files. Old pilot, installed game and saves untouched.
  Updated build state/docs and added a hash-only test-build manifest.
  Runtime boot/layout and physical Vita compatibility remain unverified.

## Vita whole-description and title follow-up — source only (2026-09-14)

- Added a guarded32-byte native wrapper before MtV line counting/splitting,
  so whole-description lookup happens before fragments reach the drawer.
  Preserves caller integer/floating state, NULL handling and displaced flags/
  stack store; fits existing reserved code space without another relocation.
- Reject English lines exceeding the native256-byte line buffer. Current
  included entries all fit; canonical wording and line breaks stay unchanged.
- Reused109 independently located scenario-title keys and28 heading/route
  labels from the shared catalog:1510total keys,180404-byte table. Title
  textures and arbitrary composed episode headings are still pending.
- Added wrapper relocation/state/NULL/buffer tests and integration with the
  original MtV entry/line counter (only imported strlen intercepted).
  All61Vita and18localization tests pass. Updated bindings, coverage, VWF
  notes and handoff; review audit02 is JSON only. No game package, install,
  source game files or shared translations changed. Live layout unverified.

## Vita native UI/help hook — source only, NOT released (2026-09-14)

- Added ui_text.py: 104-byte native Thumb exact-text hook at 0x81006e50,
  after optional UTF-8 conversion. Replays the displaced VMOV, preserves
  registers/flags except intended r7 output, compares full strings after
  hashing, and preserves unmatched pointers. No PS3 instructions copied.
- 1,373 native keys across 20 shared groups, including 118 skill, 35 Spirit,
  275 part descriptions, 94 tutorial and 83 key-help messages. Sources are
  pinned EBOOT, audited RPW, and 5,440 header-bounded little-endian ASSF
  widget records. Reproduces the original converter's two-byte font ASCII
  rather than assuming UTF-8 labels become ordinary CP932.
- English occupies a 171,056-byte relative-offset table after original BSS
  and VWF scratch. Stub fits the remaining verified VWF reservation; a second
  SCE REL32 entry supports independent text/data relocation. Original code,
  data and relocation prefixes remain unchanged outside guarded additions.
- Excluded 13 conflicting keys, 12 PS3-private-glyph messages, 46 dynamic
  format/control messages, 519 unlocated messages and one without source.
  No fuzzy/prefix/fragment replacement. Some callers may split descriptions
  before drawing; centering, clipping and actual UI coverage remain unverified.
- Nine new tests exercise actual generated Thumb code, register/flag safety,
  collisions/misses, large-table lookup, independent relocation, catalog
  exclusions and original converter/drawer integration (only the imported
  UTF-8 decoder and GPU calls intercepted), plus composition with the separate
  native SRVC table edit. All 59 focused tests pass; catalog has zero issues
  and all 475 compatibility views match.
- Added category runner integration, native binding metadata and documentation.
  Private JSON audit: work/vita/ui_text_audit_01.json. No executable, archive,
  package, installation, shared wording or previous development output changed.

## Vita category adapters — source only, NOT released (2026-09-14)

- Continued the shared-English Vita port across story scripts, suspend scenes,
  libraries, actual keyword popups, gameplay terms and battle subtitles.
  category_port.py reads canonical wording, guards audited native sources,
  rebuilds in memory, independently checks records/pointers/fields and optionally
  saves a new private JSON audit. No CPK/ZIP/package/install mode was added.
- Verified all 42,742 shared story records in 201 Vita members. Explicit
  half-width-to-full-width quote presentation aliases and soft-line reflow
  resolve 81 initial check failures; shared English/control tokens unchanged.
  Seven source-stamped suspend lines ported; other 865 remain untouched.
  Enriched their canonical Japanese definitions without changing IDs, English
  or generated compatibility views.
- Library data archives, RPW, MTFL and SRVC match PS3 data byte-for-byte.
  Converted 141 keyword-index, 408 pilot and 253 robot entries; actual keyword
  popups have all four fields checked for all 141 IDs. Added optional wrapper
  injection and case-normalized archive kind lookup to build_library._rendered,
  preserving the default PS3 path. RPW adapts 1,685 strings and 953 overrides,
  verifies 13,702 targets, semantic NULLs, ordinals and non-pointer words;
  unsafe part-description columns remain protected.
- All 31,666 battle subtitle records rebuilt with cue/header validation.
  Located the complete native 277-entry little-endian SRVC table independently;
  added guarded segment-relative edits/inverse checks, including the actual
  in-memory VWF-repacked SELF. Battle layout/runtime and coherent build
  integration pending.
- Native executable discovery finds 817 shared UI messages (154 ambiguous),
  with 1,560 searched messages unlocated. These are NOT working UI bindings.
  Documented missing menu/help/graphics/stage-title/art work and honest coverage
  in Vita COVERAGE.md, README, localization bindings and HANDOFF.
- 50 focused tests pass, including 11 new category safeguards and real native
  RPW corruption rejection; full catalog validation has 0 issues and all 475
  compatibility views are unchanged. No game files, releases, installed data,
  old pilot ZIP or VWF development candidates were modified.

## Shared multilingual catalog — source migration, NOT released (2026-09-14)

- User requested shared PS3/Vita translations and an easier path to other
  languages. Added localization/messages (stable IDs, available Japanese
  source/context, tokens) and localization/locales/en (editable English).
  Imported 82,457 entries: 42,749 dialogue, 31,666 battle subtitles, 4,457 UI,
  2,222 library, 1,156 glossary, 83 map image labels, 124 stage titles.
- Preserved all 475 old JSON/TSV data files byte-for-byte as generated English
  compatibility views. PS3 metadata/templates remain in platform bindings.
  45 UI Python modules resolve 429 text literals/table blocks from JSON;
  inverse resolution proves identical ASTs and unchanged English/logic/layout.
  Tools include the dry-run-first one-time importer, read-only inventory and
  pinned local-backup comparison; existing user changes were preserved.
- trdata now loads canonical views; Vita opening adapters read neutral stamped
  records directly, not PS3 binding templates. Both builders check catalog
  validity/stale mirrors before work. Shared content revisions include selected
  locale, definitions and bindings. No executable addresses copied to Vita.
- Added check/sync, language scaffolding, explicit-fallback content export,
  token/link validation, unknown-ID checks and protection against overwriting
  edits to compatibility views. Existing 244 Vietnamese opening drafts were
  preserved as needs_review, not silently promoted to ready translations.
- Documented canonical workflow, old merge-writer limitations, unextracted UI
  coverage, raster-art and recorded-audio exceptions. Text sharing is not a
  claim of a complete Vita port or ready-to-build arbitrary languages.
- Focused catalog/shared/Vita/CPK run: 73 tests passed, including language
  scaffolding/export dry-run/write safeguards, neutral
  dialogue API equality and all 10 real-hook VWF tests. Broad UI run:
  61 of 67 passed; replaying all 67 with hash-verified pre-migration modules
  reproduced the EXACT same six failures (deployment/word-sprite/library old
  candidate comparisons and stale parts/skills hook counts). Those failures
  are pre-existing, not hidden as migration successes; no unrelated fixes made.
- No full build, ISO/ZIP replacement, emulator installation, logo changes or
  VWF candidate modification. Current English compatibility content unchanged.

## Vita VWF port — source/development candidate, NOT released (2026-09-14)

- User's Vita3K screenshot confirms the existing English pilot reaches opening
  dialogue. It also confirms that its adaptive paired font is not VWF. This
  is user-observed opening dialogue only, not full gameplay validation.
- Started the requested proper Vita port from the PS3 VWF implementation:
  reuse tools/digraph.py's single-letter rasterizer, cap22/dilate0.5 and exact
  width/32 * quad-width advance rule. No PPC instructions, PS3 addresses or
  PS3 texture binaries copied. One canonical English source remains unchanged.
- Added Vita-specific, hash/instruction-guarded Thumb hooks for glyph advance,
  four dialogue-piece origins and actual-pixel piece accumulation. Latin uses
  95 verified blank native GXT cells in the 0x87 bank; other cells retain the
  original advance. Measured W=28, i=10, period=11, m=27, space=9 texels.
- Code uses 294 bytes within the verified 684-byte text-to-data gap, plus a
  192-byte width bank and relative-pointer word. New pen scratch is appended
  after original BSS; no guessed unused game global. Segment file offsets are
  repacked, virtual addresses/indexes and original relocation bytes preserved.
  Loader review caught independent code/data relocation; appended one SCE
  format0 REL32 record for the new scratch pointer and tested separate bases.
  Original code is identical except six guarded four-byte replacements;
  original initialized data and BSS zeros remain intact. Relative hooks tested
  at two load addresses. This is not yet a physical Vita compatibility claim.
- Added read-only executable inspection, dry-run-first loose candidate
  preparation, pixel and 256-byte line-buffer guards, and a clearly labeled
  OFFLINE font proof. Reused the pilot's audited input loading and exact script
  verification. All 244 opening records round-trip; non-dialogue/control bytes
  unchanged; only 95 cell rectangles per native font page are modified.
- Ten new tests execute generated ARM hooks, check register/flag/stack safety,
  every width-bank entry, Japanese fallback, all four piece origins and
  accumulation, SELF repacking and guards. An integration test runs the actual
  original character loop/lookup/newline logic with GPU calls intercepted.
  All 55 focused tests pass (38 Vita, 12 shared-platform, 5 CPK ITOC).
  The old fixed-cell builder also passes a fresh dry-run. Isolated local
  analysis dependencies: Capstone4.0.2,
  Keystone0.9.2, Unicorn2.1.4 (no global Python installation changes).
- Private loose output: work/vita/vwf_candidate_02; candidate EBOOT SHA256
  df7a11494282d1d88d47e0ff3571f5c3f845aa62ccb301fc6b8e0df3c22c6044.
  Earlier candidate_01 is retained as an analysis intermediate; it lacked
  the independent-segment relocation entry and must NOT be packaged.
  This is NOT an install ZIP or a release. Existing pilot ZIP, emulator files,
  saves, original source files, PS3 builds and version counter untouched.
  Still pending: Vita3K runtime/visual validation, keyword highlight/hit-box
  widths, centered/name/UI layout and translation beyond the opening stage.
  Full build/install remains held until the user requests it.

## Vita English opening-stage test 01 — complete install ZIP (2026-09-14)

- User requested one already-patched ZIP for Vita3K, superseding the earlier
  original-PKG-then-overlay instructions. Built a complete 589-file archive:
  3 verified English dialogue/font CPKs, 6 locally decrypted SELF executables,
  580 byte-identical base files. English coverage is still ONLY 244 opening
  records; no new translation content and no claim of a full English port.
- Added bounded SELF metadata/segment reader and VitaSDK-compatible plain
  SELF writer. All 30 executable segments passed zlib checksum/length checks
  and exact byte-preserving reconstruction. No executable instructions patched.
  Public Vita3K/VitaSDK format references are SHA256-pinned; PyCryptodome 3.23.0
  is isolated under ignored work/vita. Existing license read in memory only.
- Added dry-run-first full ZIP builder, rejects modified inputs/unsafe names,
  existing output folders and license/PFS metadata; checks streaming source
  hashes, all ZIP entry sizes, SHA256 and CRC on read-back. Added 10 synthetic
  tests (wrong key, corruption, truncation, round-trip and package safety).
  All 45 focused tests pass: 28 Vita, 12 shared-platform, 5 CPK ITOC.
- Output: work/vita/english_pilot_01_install/
  SRW-Z3-Vita-English-pilot-01-install.zip; 1,874,630,556 bytes;
  SHA256 a20e507926427250435dd8f7b150389ff0bb4b8c429751d7b88e02499737818d.
  All 589 entries verified; expanded size 2,341,565,849 bytes. Audit, checksum
  and direct-install instructions accompany it. Source casing retained.
- Updated Vita status, player docs and handoff to distinguish full install
  packaging from limited translation coverage. The earlier overlay remains
  available and unchanged, but is NOT the ZIP to use with Vita3K's installer.
  No license/work.bin, firmware, saves or PFS metadata in the complete ZIP.
  No emulator install/boot test, original input changes, PS3 changes or
  version-counter changes. Runtime/visual correctness still needs user testing.

## Vita English opening-stage test 01 (2026-09-14)

- User requested an English Vita build and selected Vita3K on PC. Built an
  explicitly limited opening-stage test, NOT the full PS3 translation port:
  244 shared records (25/117/102) across stage 0001A/B, exactly matched on
  Japanese text/fingerprint/event/ordinal/speaker. No canonical English edits.
- Added Vita-specific linear P4 GXT font handling and adaptive Latin pairing.
  Native atlas anchors visually verified; used all 488 unassigned blank cells
  common to pages 1/3, without repurposing Japanese, Greek or symbol glyphs.
  Original 625 fixed pairs would not fit, so dictionary segmentation plus
  single-character fallback preserves every English character in 488 cells.
  System Arial Narrow Bold is rasterized into native Vita palettes; no PS3
  font texture/executable is copied. Actual layout remains runtime-unverified.
- Builder is dry-run-first; validates source audit hashes, exact text round
  trips, control tokens, links, four-line/provisional 30-cell budget (max 28),
  and byte-identical non-dialogue Lua, including skip flow and keyword IDs.
  Rebuilt archives preserve all untouched compressed members and pass ITOC
  checks. Only STG0001a.cpk, STG0001b.cpk and DATA/tabata/TPACKVITA.cpk change.
- Checked output: work/vita/english_pilot_01_checked. Overlay ZIP 6,783,105
  bytes, SHA256 f713cfd9bad1dd50a7d1785d54c3f176a2ed5847b05c65eec9c669969e3e6eaa.
  144 total archive members verified; independent font diff confirms only
  selected blank-cell pixel bytes changed, palettes/headers preserved. Font
  proof PNG inspected; clearly labeled reconstruction, not runtime screenshot.
- Added checked installer, backs up originals and rolls back copy failures;
  rejects running Vita3K, unknown bases and mismatched hashes. 35 tests pass:
  18 Vita, 12 shared-platform, 5 ITOC. Added test instructions, updated status
  and handoff. First attempt stopped at preview-only missing label glyph and
  remains incomplete in work/vita/english_pilot_01; do NOT install that folder.
- At the overlay-build step, Vita3K was found at E:/Emu/vita3k and its configured
  app folder was empty. The later complete install ZIP above removes the need
  for a separate original-PKG install. At this earlier step the user said
  firmware installed; original game install/boot confirmation remains needed.
  No install, runtime test, SELF patch, license/firmware/save change, PS3 build
  or version-counter change. Menus, names, combat UI and later stages remain
  Japanese. Full English Vita port and visual/runtime correctness are unfinished.

## Vita offline PFS decryption completed (2026-09-14)

- User approved actual decryption. Built public pkg2zip and an isolated native
  Vita3K PFS adapter, unpacked the original PKG, then decrypted locally using
  existing work.bin. Metadata/signature, file and keystone checks passed.
  No license/key upload or logging; original PKG/license and PS3 are unchanged.
- Independently verified 589 files and hashes, 176 CPK archives with 35,861
  indexed members, 189 GXT signatures and three readable/decompressed opening
  candidates. Output is work/vita/decrypted_PCSG00264; non-secret audit is
  work/vita/decryption_audit.json. Seven validation/safety tests pass, including
  synthetic wrong-key rejection before output creation and overwrite rejection.
- Added build adapter, independent audit tool, integration tests and decryption
  provenance/instructions. Updated Vita pilot status, preparation messaging,
  README and handoff. Shared translations and build counter are unchanged.
- PFS data is ready for source mapping, NOT a playable translation. Inner SELF
  executable handling, exact source matching, font/layout porting and runtime
  checks remain. No Vita patch build/install or PS3 rebuild/install performed.

## Vita local license validation (2026-09-14)

- With user approval, read the existing 512-byte work.bin locally and compare
  its complete content ID against SRW Z3.1 Vita.pkg: matches PCSG00264.
  Expected NoNpDrm header/account marker and nonzero key are present; package
  size matches its header. Original pre-rename filename is not used as identity.
- Added a read-only, bounded-input validator. Optional report stores only
  non-secret booleans/title ID under ignored work/vita and refuses overwrite.
  Dry-run inspected, then saved work/vita/license_validation.json. Five
  synthetic tests pass, including mismatched IDs and secret-redaction checks.
- Inspected upstream NoNpDrm license layout and PFS implementations. Located
  Vita3K's native offline key-processing backend; the older parser's online
  service/cache requirement need not be used. Downloaded only public source
  code into ignored work/vita. No license/key upload, key logging, decryption,
  game modification, build or install. Cryptographic key validity remains
  unverified until actual PFS decryption succeeds; no extra user file needed
  for the next offline attempt. Updated Vita documentation and handoff.

## CFW hardware-test packaging — 0.6.13-CFW-test1 (2026-09-14)

- User approved a separate hardware-test package after the friend's 0.6.10
  image was rejected from internal HDD as ENCRYPTED/INVALID ISO and launch
  returned 80010017. Local 0.6.3/0.6.10 checks found plain ELF EBOOT files,
  stale original disc-region ends and unreconstructed UDF metadata. These
  are confirmed packaging problems, not proof of the only runtime failures.
- Added a dry-run-first CFW packager using the verified original disc and
  validated 0.6.13 snapshot. Fresh ISO9660/Joliet trees retain all 554 files
  and original primary aliases/full Joliet names; stale UDF is not copied.
  Disc plaintext ranges and both volume lengths cover the entire new image.
- Wrap the existing ELF with pinned, locally compiled PSL1GHT fself, adding
  a missing-.sceversion guard to the ignored upstream checkout. Preserve
  original disc application metadata/capabilities and verify byte-identical
  ELF payload, embedded headers, all segment mappings and SHA-1 digest.
  This is a CFW fake SELF, not a retail-signed executable or stock-PS3 support.
- Generate 2-GiB FAT32 `.iso.0`/`.iso.1` parts with hashes and a full-ISO
  reconstruction check. Audit is written only after all 554 files in each
  filesystem tree and all split parts pass. Eight synthetic packaging tests
  pass, including executable/header/metadata corruption, stale region maps
  and split-overwrite rejection.
- Added CFW reproduction/testing instructions and corrected installation
  documentation to distinguish legacy RPCS3 packages from hardware support.
  Completed `work/cfw_0.6.13_test1`: full ISO 4,741,267,456 bytes; split
  parts 2,147,483,648 + 2,147,483,648 + 446,300,160 bytes. All 554 files in
  BOTH trees and concatenated split contents verified; CFW_AUDIT.json saved.
  Physical PS3 boot remains untested; this is not a confirmed hardware fix.
  No translation edits, build-counter change, RPCS3 install, public release,
  game upload, save changes or firmware changes.

## Unreleased — shared PS3/Vita setup (2026-09-13)

- Began incremental single-repository organization: moved the unchanged PS3
  STAGES/LIBRARIES configuration to platforms/ps3/manifest.py with the old
  translation/manifest.py retained as a compatibility loader. Updated stage
  registration, status and name-check readers for the new location. Legacy
  tools, shared translation/glossary paths, installed game and outputs stay put.
- Added shared/catalog.json and source fingerprinting. Future PS3 build
  manifests and Vita review bundles identify the same shared English revision;
  this tracks source consistency, not equal port coverage. Existing builds
  have not been restamped. PS3-specific hook addresses remain nonportable.
- Prepared the initial Vita PCSG00264 opening-stage pilot from the existing
  English: 25 + 117 + 102 = 244 records across 3 candidate members, using the
  same glossary. Dry-run-first preparation saves only an ignored review bundle
  under work/vita; no separate editable Vita translation copy is created.
- Added exact record-matching guards for future decrypted-source comparison,
  with synthetic tests for source drift, duplicate identity, speaker/ordinal
  mismatch and missing records. Current Vita member IDs remain PS3-derived
  candidates. No actual decrypted Vita script comparison or runtime test yet.
- Added platform/shared documentation and Vita game-file ignore patterns.
  User has only the PKG and work.bin. Inner PFS decryption remains required;
  work.bin was not read/uploaded. No full build, ISO, install or release.
- Validation: 12 cross-platform tests, 15 build-version tests and 8 partial
  translation tests passed. Legacy manifest data equals its pre-move version.
  Saved the 244-record review bundle after inspecting dry-run samples. Existing
  unrelated whitespace warnings in deploy/extract/apply_xdelta are unchanged.

## 0.6.13 — Local test build (2026-09-13)

Complete build succeeded in `work/build_0.6.13_batched_ui`; all packed checks
passed. Includes all batches below and the approved 0.6.12 subtitle. The
31 focused regression tests pass; all 110 stage plaintext archives match
0.6.12 exactly. Translation remains partial (1,034 untranslated mission
variants recorded in the coverage report). Installation is pending RPCS3
closure; installed version remains 0.6.12. No new ISO or public release was
created. The staged-only notes below record when each fix was implemented;
those fixes are now included in this validated build, but still await live
in-game verification.

**Pilot TOP 5 / Trade List follow-up (2026-09-13, staged only):** traced the
actual headings to separate Japanese UI fragments; earlier full-string hooks
and the UTF-8 Key Help caption did not cover these widgets. Replace all six
Pilot TOP 5 fragments with one centered English caption, cover both related
Ace Pilot title variants, and translate both four-fragment Trade List headers.
Blank only the obsolete sibling fragments; preserve font sizes, baselines,
colors and animation records. Remove the ineffective guessed title hooks.
In both narrow Trade List category columns, shorten `Upgrade Systems` to
`Systems` and set both category labels to 23px, leaving over 12 native pixels
before the item column. The wider Buy-screen `Upgrade Systems` is unchanged.
Add source guards, title-position and category-fit checks to packed validation.
Eight focused tests, four menu and three Combat Record regressions pass,
including the production UI pass order executed entirely in memory.
No packaged build or installation; visual confirmation awaits the user's
explicit build instruction.

**Linked-name/background width (2026-09-13, staged only):** the Back Log
selection background used `(source byte length / 2) * Japanese character
pitch`, even though English text uses proportional glyph advances. Capture
the actual rendered width when each link is registered, and use that cached
width for the shared selected-link background. Covers names/terms using this
link renderer, not arbitrary menu bars. Preserve link IDs, source strings,
byte lengths, navigation metadata, X/Y, background height and colors. Cache
256 widths in unused space within the existing scratch page; no save-format
or archive changes. Add guarded hooks and packed validation, with focused
machine-instruction tests covering all slots, slot reuse, invalid-index
bounds, metadata isolation, narrow/wide English and unchanged Japanese width.
All three focused tests, three preparation-menu regressions and five
save/quit regressions pass. Scoped whitespace checks pass.
No complete build or installation; in-game confirmation remains pending.

**Parts/preparation popup follow-up (2026-09-13, staged only):** translate
both removal-confirm hints as `: Remove`, three quantity headings as `Qty.`,
three selection-number headings as `Select No.`, and both parts-comparison
Pilot captions (including the split source caption). Eleven UI records are
repointed; their geometry, typography and flags remain unchanged. The reported
Z Chips footer is already covered by the earlier nine-variant pending fix.
Center the separate executable preparation-popup table: Team Setup, Pilot
Training, Pilot Swap, Upgrades, Power Parts, Swap Parts, and the ship variant
(`Ship Upgrades`, shortened only here to fit). Keep the already-centered Search
and popup heading unchanged. Apply live-pitch padding only at these seven
source locations, not other screens using the same words. Append seven blank
font cells without renumbering existing pads or growing the constrained VWF
dispatcher. Add packed descriptor-reference checks and three focused tests:
UI isolation/previous Z Chips coverage, actual in-memory executable pointer
readback, and all 199 padding slots at multiple pitch/quad sizes plus ordinary
glyph regression and both font-layer blank-cell checks. No full build or
installation; live testing awaits the user's build instruction.
The three new tests and 12 training/help, save/quit and prior-menu regression
tests pass. Scoped whitespace checks pass; unrelated older file warnings
were left untouched.

**Training and control-help follow-up (2026-09-13, staged only):** shift all
Learn Skills tab states to match Raise Stats' inset, preserving the reference
tab and all baselines/styles. Translate four Key Help switch hints, both
Select Slot hints, the Right Stick label, and the Power Part slot explanation.
Inventory the separate executable Key Help table and cover all 91 action
labels, retaining the unused-action dashes and existing shared terminology.
Provide the slot explanation in both UI and executable text paths. No full
build or installation: awaiting the user's explicit build instruction.
Three focused tests pass: source-family completeness and width checks,
exact UI-record isolation (including unchanged Raise Stats), and an in-memory
run of the actual UTF-8 patcher that verifies the English text at every
Key Help table reference. Live screen alignment still needs later testing.

**Trader/intermission screenshot follow-up (2026-09-13):** translate all four
sell/carry-over selection prompts, not just the reported sell-parts line.
Use Cmdr in the two narrow roster Commander columns, retaining Commander as
the skill name elsewhere. Replace the split Z Chips caption in all nine
intermission footer variants. Correct normal/highlighted Pilot List,
Upgrades, Search, Options and both Network button pairs using the supplied
live capture; preserve fonts, colours and baselines. The earlier PS Store
centering still appeared left-shifted in the Network popup; compensate its
split-renderer offset in both caption variants. Four focused tests, three
existing alignment tests and the UI preflight pass. User requested batching
further fixes and building only on explicit instruction; stopped the full
build before completion. These changes are not installed. Installed game
and last successful version remain 0.6.12. Updated project working rules
to retain this build gate for subsequent reports.

**Approved subtitle installation (2026-09-13):** the September 12 combined
preview was approved but not installed; builds through 0.6.11 still used
the earlier equal-weight TIME PRISON / CHAPTER tile. Recover the approved
subtitle and combined preview into local project assets. With explicit user
authorization, remove the baked checkerboard by script (including letter
holes) and resize to the native 339x117 slot, retaining the exact lettering
and a smaller CHAPTER line. The main English wordmark, original fiery Z,
geometry and animation remain unchanged. Keep the old subtitle for rollback;
pin subtitle-v2.png's hash in the build and add a deterministic-cleanup test.
This is asset preparation from the existing approved design, not new image
generation. Complete build 0.6.12 passed packed checks and all 19 title tests;
all 110 stage archives match repaired 0.6.11 exactly, with five archive
regression tests passing. Installed to game/ with all 186 updated hashes and
all 560 disc files verified; 17 save files unchanged. Previous files backed
up under work/install_backups/0.6.12_20260913_161159. The stage-transition
repair remains included. No new ISO; in-game verification remains for the
user's next test.
Independent effects comparison confirms the only changes from 0.6.11 are
the subtitle tile and version footer; main wordmark, Z, animation records
and all 333 other archive members are unchanged.

**Stage-10 ending / archive index repair (2026-09-13):** the reported black
screen after skipping the ending coincides with loading internal STG0018.
Its cached archive matches 0.6.10 but declares an ITOC four bytes too short.
The builder reused the original header size when two dialogue members moved
from 16-bit to 32-bit size tables, losing the first growth increment. Derive
the header size from the current chunk instead. Add regression tests for zero,
one and two promotions, an initially empty high-size table and rejection of
the old malformed header; enforce index-length/count checks while packing
and during complete-build validation. The 0.6.10 audit found five affected
archives: STG0016, STG0018, STG0029, STG0067 and STG0074; all 142 original
archives passed. Earlier packed checks did not detect this defect, including
those used for the 0.6.10 ISO. Runtime resolution requires user retest after
installation; no dialogue or event logic is changed by this repair.
Complete build 0.6.11 passed all packed checks. All 110 stage CPKs pass the
new guard; the five repaired archives change only header byte 0x106, with
every member byte-identical to 0.6.10. Independently decrypted all 109
encrypted STG outputs and verified exact CPK matches. Five new regressions
and eight partial-translation regressions pass. Replacement files are now
closed promptly by the packer. After RPCS3 exited, dry-run and approved
installation verified all 186 game targets and 17 unchanged save files.
Old game files and the install cache are retained in
work/install_backups/0.6.11_20260913_155513. Registered game/ folder and the
other game's registration are preserved. The game recreates its cache on
next launch. In-game stage-10 skip retest remains pending; the existing
0.6.10 ISO is unchanged and still affected.

**Requested local ISO 0.6.10 (2026-09-13):** user explicitly
requested an ISO in addition to the single installed game folder. Package
the verified 0.6.10 build against the pristine Japanese disc image using
the existing ISO writer. The local packaging runner checks the original
disc digest, build manifest and installed files first, refuses overwrites,
then verifies both directory trees and all 554 actual disc files before promoting
the temporary image. This adds no translation changes or new build number;
no release, upload, emulator registration change or save modification.
The initial verification expected the folder audit's 560-file count; inspection
showed the original ISO has 554 files. Verify the exact original disc inventory,
matching 553 files to the installed folder and preserving/verifying its original
firmware file separately. Folder-only backups and build metadata are not disc
contents. Completed `SRW-Z3-English-0.6.10.iso` in the project root:
4,996,820,992 bytes; all 186 translated files verified in both directory
trees and all 554 disc files verified. SHA-256:
`41bbdb50d6c558375d08418f044853a158de8c00eec3b8046d7cc5225c8a3f22`.
Receipt: work/iso_0.6.10_audit.json. Installed game remains 0.6.10.

**Spirit targets, Pilot TOP 5 and Trade List (2026-09-13):**
Translate the Spirit reference's composed target family (11 combinations,
including One Ally and Enemy Team), using the existing joined-string
fallback as well as whole-string matching. Set only its target-value font
to 26px to fit the narrow column; leave duration, targeting behavior and
locked question marks unchanged. Translate the ranking-switch hint and
the original Pilot TOP 5 title prototype. Add six screenshot-derived
composed-title fallback keys; the exact live title construction remains
unconfirmed and must be retested, not treated as proven visual coverage.
Translate the UTF-8 Trade List heading and all 18 original item lore entries,
separately from their existing gameplay-effect descriptions. Retain the
original humor, use glossary expansion and Focus terminology, and wrap the
lore to three width-checked lines. Add source-inventory, category, per-line
hook and field-isolation regressions plus packed-build checks. Diagnostic
atlas inspection produced ignored work/ previews only; no artwork changed.
Four new category tests, eight partial-build tests and three Library/episode
regressions passed. Complete build 0.6.10 passed packed checks with 4025
binary hooks and no undrawable entries. Additional candidate checks confirm
all 17 target/title fallback flags, the UTF-8 Trade List caption and unchanged
original lore data. Dry-run then approved installation with RPCS3 closed
verified all 186 game targets and 16 unchanged saves. Backup:
work/install_backups/0.6.10_20260913_105129. Registered game/ folder and other
game registration preserved. Live target/title and layout retest still needed.
No release published.

**Change Pilots alignment (2026-09-13):** move the intermission grid's
normal caption 41.5 native pixels left, measured from the user's 2560x1440
capture. Apply the proportional correction to its separate 31px highlighted
variant. Preserve both original fonts, strings/hooks, colors, Y positions,
button artwork and all other fields; the team-editor caption is untouched.
Add source-isolation, measured-center, highlighted-clearance and packed-X
regressions. Two targeted tests, Library alignment regression and eight
partial-build tests passed, followed by complete packed checks. Comparing
the built UI to 0.6.8 confirms only the two requested X fields changed.
Installed 0.6.9 after dry-run with RPCS3 closed; 186 hashes verified and 16
saves unchanged. Backup: work/install_backups/0.6.9_20260913_100131.
Live highlighted-state confirmation is still required. No release published.

**Library lists, map factions, Operation End titles (2026-09-13):** translate
all three Library list headings and name columns plus both shared sort hints
(12 text records, including the two extra Glossary screen copies)
(`Kana Order` / `Series Order`; actual sorting unchanged). Generate complete
episode-heading hooks from the original 181-record episode metadata and
159-entry title table, reusing all 124 reviewed title translations plus the
35 route/data/gift labels. This avoids stale script-header episode numbers
and covers the composed Episode 10 / Demon King's Invitation heading.
All 157 preset faction/squad names now also accept NUL-separated text pieces
through the existing joined-heading mechanism, a fallback for the still-
Japanese Mechanical Beast Army map label; live confirmation is required.
Source names, title-table pointers, team IDs and saves are untouched.
Add source-driven episode-category coverage, complete caption-family
inventory, scoped Library size/isolation checks, and emitted split-name flags.
All three category tests and eight partial-build tests pass. Complete build
0.6.8 passed packed checks, including 3937 binary hook entries. Dry-run then
approved installation with RPCS3 closed verified all 186 game targets and
16 unchanged saves. Backup: work/install_backups/0.6.8_20260913_094904.
Single game/ folder retained; no public release published. Live retest pending.

**Library button alignment (2026-09-13):** user screenshot confirmed visible
labels but uneven leftward offsets. Apply per-caption native-coordinate
corrections measured from that 2560x1440 capture to all six title records
(five labels, including both Robot Encyclopedia records). Keep the working
special text mode, plain glyphs, font size, vertical positions and colors.
The selected Sound Select uses the same corrected center as the other rows.
Add source/packed-coordinate, capture-boundary and mode-preservation tests.
The targeted regression and complete packed-build checks passed. Installed
0.6.7 after a dry run with RPCS3 closed: all 186 game targets verified,
16 saves unchanged. Backup: work/install_backups/0.6.7_20260913_091550.
No release published; live visual confirmation remains necessary.

**Deployment ordering/aboard labels (2026-09-13):** translate the square-button
hint as `: Reverse Order`. Replace both three-piece Japanese teams-aboard
captions with `Teams Aboard`, clearing only their own remaining fragments.
Use a 20px caption shifted 16 native pixels left within the existing banner
to leave room for the live count, without a colon. Original count widgets,
colors and input behavior remain unchanged. Packed checks added for all
seven affected text records. New source-inventory/isolation regression passes,
as does the previous currency-counter regression. Complete build 0.6.6
passed packed checks and was installed after a dry run with RPCS3 closed.
All 186 game targets verified; 16 save files unchanged. Backup:
work/install_backups/0.6.6_20260913_090341. Single game/ folder retained,
no release published. Live layout confirmation remains for user testing.

**Currency counter overlap (2026-09-13):** the deployment Funds value
119992 overlaps the fixed colon introduced by the earlier counter alignment.
Omit the Funds and Z Chips colons in all three deployment/map panel variants
(six widgets), preserving the live values, font sizes, and numeric positions.
SR Points and Teams/Turns keep their separators. Packed checks now require
all six currency separator strings to be empty. The targeted regression
test verifies all three variants and byte-level isolation of changes;
live numeric widgets and non-currency separators are preserved. Test passes.
Complete build 0.6.5 passed packed checks and was installed after a clean
dry run with RPCS3 closed. All 186 game targets match; 16 save files are
unchanged. Backup (including old game-data cache):
work/install_backups/0.6.5_20260913_085205. Live visual retest remains for
the user. No release published; single runnable game/ folder retained.

**Map support font and preset squad names (2026-09-13):** correct the
shared Support Defend/Support Attack/Re-Attack map-word geometry, widening
the English without enlarging its italic shear or changing UVs/animation.
The words now share a consistent font size instead of stretching every
glyph mask to the same height. Added exact display-only translations for
157 ally/enemy preset squad/faction names, including Crusher Squad. The
subsequent map screenshot still showed Mechanical Beast Army in Japanese;
the later Library/faction batch adds split-text matching for this category.
The source-driven audit reads literal team-name fields across all 142 stage
archives, correctly unescaping CP932 trail bytes, and refuses missing names
even in partial-story builds. Source team IDs, source strings, and saves are
not rewritten. Four new source/geometry/aspect/coverage tests pass.
Complete build 0.6.4 passed the packed checks and all 190 manifest hashes.
Installed into the existing game/ folder after the user closed RPCS3:
186 translated files and all 560 disc files hash-verified; 16 save files
unchanged. Backups: work/install_backups/0.6.4_20260913_083736. The installer
now backs up/refreshes/rolls back the four single-folder metadata files too,
preventing an old version receipt after deployment. It verifies the full
disc audit before recording the new version. Four new tests and eight
partial-build tests pass; offline actual-quad comparison visually reviewed.
Live visual retest remains for the user; no public release was created.

**0.6.3 public-release preparation (2026-09-12):** on user request, package
the existing immutable build without incrementing its number. Added a
dry-run-first patch-only ZIP packager with exact inventory, CRC and entry-hash
checks. Updated installation instructions for 0.6.3 and recoverable cache
refresh, corrected old coverage/CV claims, and added public release notes
with explicit remaining story/mission-text coverage. ISO and folder packages
are distribution patches only; the complete game folder is not uploaded.
ZIP completed: 85,065,423 bytes, all 189 entries passed CRC/content hashes;
all 186 application paths match the release manifest. Public upload was
initially blocked by the approval reviewer pending explicit user approval
of the patch files and retro-trans/SRW-Z3 destination. Approval was then
granted; all three verified packages were uploaded and published as latest
at https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.3 on
2026-09-12 at 13:36:57 UTC. Remote asset sizes/SHA-256 digests and notes match.
Both ISO distribution patches are now decode-verified against the same
4,996,820,992-byte release image (MD5 7936d74e28e5b7259ab6666a967e71a7):
149,090,767-byte pristine-source delta and 18,859,897-byte update from 0.6.1.
All three package SHA-256 hashes are recorded in the public release notes
and a local SHA256SUMS.txt. Packaging and publication are complete. The
release tag targets existing commit 69e0537; no local source commit/push
was made. Working changes, installed game and saves are unchanged.

**Single-folder testing package (2026-09-12):** canonical runnable location
is now E:/Projects/SRW Z3/game, ignored as game content. Added dry-run-first
prepare_testing_game.ps1: verifies the coherent numbered build, copies the
complete disc tree with all translated files substituted, and hash-checks
every destination. No new translation/build number for unchanged 0.6.3.
Preparation completed: 560 disc files copied and hash-verified, including
all 186 translated build outputs. Added a local testing README.
The installer now targets this folder and backs up/updates/verifies only
BLJS10256 in games.yml; unrelated registrations and line endings are retained,
with registration rollback on failure. Tests cover transformation/idempotence,
missing/duplicate registration rejection and PowerShell syntax. Older builds
and saves are retained. Actual registration/cache switch still requires RPCS3
to be closed; preparing the folder alone does not switch a running emulator.

**Local testing installation workflow (2026-09-12):** user now requests
automatic installation after each successful build unless told otherwise.
Added dry-run-first install_build.ps1: checks the numbered manifest, all exact
game paths, closed RPCS3, backup hashes, deployed hashes and save hashes.
Moves only BLJS10256_DATA to a recoverable backup rather than deleting it;
failed deployments roll back copied files. Preference recorded in CLAUDE.md.
Installed version0.6.3 after successful dry run and filesystem approval:
all 186 deployed hashes verified; all 16 save-file hashes unchanged. Old
files and install cache retained in work/install_backups/0.6.3_20260912_182937.
Only the game's install cache was moved; it recreates on next launch.
User testing exposed a deployment-target mismatch: RPCS3's BLJS10256 entry
still points to work/patched_0.6.1.iso, not the updated extracted game folder.
The destination hashes were valid but this did not update the user's active
boot copy. Registration/cache correction is pending RPCS3 being closed.

## 0.6.3 — combined local build (2026-09-12)

Successful complete package at work/build_0.6.3_all; title and build manifest
both stamped 0.6.3. Includes all 109 registered stages (83 story +26
intermissions), current voice/text data, English logo, CV credits, Focus/Foc,
descriptions and UI fixes listed below. All 132 tests pass; 408 CV fields
independently verified against the new font. Snapshot releases/0.6.3 contains
186 game files with independently verified hashes. Partial translation status
and 1034 untranslated mission variants explicitly recorded. No installation,
ISO update, publishing or upload at build time. Subsequently installed at the
user's request; see the installation entry above. See RELEASE_0.6.3.md.
Generated both per-file distribution sets: 186 original-to-0.6.3 patches
and 122 version-0.6.1-to-0.6.3 patches; all decode/hash verified.

**Combined-build preparation (2026-09-12, completed):** rebuilt all 109 registered
stage scripts (83 story + 26 intermission) together with the current UI,
English logo and Library CV catalog in work/build_0.6.3_all. Corrected both
narration validators to select the 18 timed source keys rather than the first
18 rows of an expanding UI file. Added explicit --partial-translation mode:
missing mission variants are inventoried and hashed in message_coverage.json;
missing non-mission UI, bad translated text, source structure and translated
victory/defeat roles still fail. Default coverage checks remain strict.
This is a complete package of available work, not a complete translation.
No installed files or save data changed by the build.
The combined build also exposed a filename collision: renamed the CV catalog
from voice_actors.json to library_voice_actors.json so the battle-voice loader
does not treat proper-name labels as a numbered dialogue section.
The broader source audit found the same Turn 7 event used as victory and
defeat conditions. Exact neutral "Turn 7 begins." is valid in both panels;
role-dependent shoot-down text still requires distinct context.
Mission regression tests now assert the partial-build contract and retain
complete coverage of the previously translated stage 1-30/intermission set;
separate negatives confirm default strictness and missing-UI rejection.
The main build audit now checks all 408 CV fields against the active font.
Release snapshots retain coverage metadata and a local detailed backlog.

**Library CV romanization (2026-09-12):** added a complete dedicated catalog
of 153 original Japanese voice actors plus the no-credit placeholder. Normal
Library builds and font text pooling now translate ACTR through the same
catalog; unknown credits fail for review. Aoi's CV is Haruna Ikezawa. Added a
dry-run-first isolated candidate updater that changes only ACTR, validates all
other fields byte-for-byte, retains a backup, and checks name widths. Legacy
ACTR glyph reservations remain for compatibility (previously these credits
were deliberately left Japanese). Local candidate updated: 408 entries,
193 named credits and 215 placeholders; all non-ACTR fields preserved.
Seven tests pass, including normal build coverage and backup-to-candidate
replay. Second patch run is a verified no-op. Widest name is 340px at 32px
type, below the 400px budget. Backup: work/library_cv.before.CPK; audit:
work/library_cv_audit.json. See docs/LIBRARY_CV.md. No deployment; live
visual verification pending.

**Stage-preset and Counterattack build blockers fixed (2026-09-12):**
audit_message_classes now discovers the named preset in each archive rather
than assuming member1; both coverage and role checks use the same lookup.
STG0068 correctly resolves to member3. Missing/ambiguous presets and unknown
objective-bearing files still fail; known dialogue-only exceptions remain
strict. The scan completes over 142 archives / 1538 variants, including
24 whole/numbered Stage68 variants. It now reports a separate backlog of
1034 untranslated mission variants. The subsequent combined-build request
adds an explicit partial-translation release contract that reports this
backlog while retaining strict validation of every translated message.
Removed the stale duplicate Counter/Defend/Evade entries in issue_hook;
standalone and combined menus consistently use Counterattack. The local
candidate's combined-menu hook was synchronized (1 replacement, 57 new text
bytes, 3495 unchanged lookup keys); every other hook, executable code and
file length preserved. Backup: work/counterattack_EBOOT.before.bin.
Added 10 regression tests; 68 targeted/regression tests pass. Historical
Focus replay uses its pre-Counterattack endpoint; current hooks are still
checked independently. The broader checker now passes the duplicate and
menu-hook checks but stops at its unrelated stale first-18-narration-rows
assumption. Missing stage outputs and mission translations also remain.
No stamp, complete-build claim, release, ISO or installation changes.

**English title logo (local candidate integrated):** first created two
built-in image-generation drafts using the supplied official SRW X lettering
as reference. Both had baked checkerboards; neither was packed directly.
After explicit cleanup approval, clean_title_logo.py extracted only the
3rd SUPER ROBOT WARS plaque and TIME PRISON / CHAPTER subtitle, retaining
their metallic silver/gold and white/purple styling with real alpha.
title_logo.py maps these into EFFPS3 member296 texture1's verified native
706x296 and 339x117 sampling rectangles. Original Z frame/fire pixels,
3363 word-sprite animation samples, backgrounds, prompt and Library labels
are unchanged. Normal build and audit paths now include this layer.
patch_title_logo_candidate.py dry-run/write changed only member296 in
work/out_0.6.3/EFFPS3.CPK; all 333 other stored payloads verified identical.
Backup: work/title_logo.before.member; hash audit: title_logo_patch_audit.json.
All 18 title tests pass; alpha previews checked on dark/light backgrounds.
Final assets: work/title_logo_final; built-in prompt: work/title_logo_draft/PROMPT.md.
No stamping, release, ISO or deployment changes. In-game verification pending.
Details and rebuild requirements: docs/TITLE_LOGO.md.

**Stage 74 translated** (561 records over 5 slices): 303 in member 3, 258 in
member 4. Both clean under `check_stage.py`; `check_names.py` clean corpus-wide.
`tokenise_stage.py` found 0 records to change, so the slices tokenised
everything correctly themselves.

**Reversed word order breaks a glossary key, found twice independently.** One
slice established that `Ｚマジンガー` is not `マジンガーＺ`; another that
`神ミケーネ` is not `ミケーネ神`. Both contain exactly the right elements in the
wrong order, so both survive a "does this record mention the term" eyeball test
and fail the exact lookup. Written plain, one corroborated against a voice-bark
precedent. Recorded in CONVENTIONS beside the partial-name and fragment rules --
and `ミケーネの神`, with an inserted `の`, is a third distinct string again.

**A common noun that is a proper term in another series.** `使徒` is the
Evangelion Angels, but this is a Getter scene where the word means "apostle" of
the Getter rays. A slice deliberately avoided "Angel" to stay clear of the
numbered Evangelion entries. That is the `先生` problem in a new shape: not a
name colliding with a name, but ordinary vocabulary colliding with a term from
a different show.

**Stage 74's portrait metadata is unusually dirty.** One slice found seven
records whose portrait id does not match the speaker; another found two that
look like outright swaps, a Sousuke line carrying Gou's portrait and a Gou line
carrying Sousuke's. All were translated from the speaker field. A slice that
trusted portraits here would have produced plausible, checker-clean, wrong
attributions -- which is exactly why that rule is stated as "a lead, never
evidence".

Both halves of the tokenise decision appeared in one scene: bare `あしゅら` and
`暗黒寺` ARE keys and take tokens without their usual `男爵`/`刑事` suffixes,
while `くろがねの鎧` is not a key and stays plain.

One cross-member conflict: Kouji's shout rendered "Uooooooooh!!" in member 3 and
"Ohhhhhhhh!!" in member 4. Neither sha ships elsewhere, but the corpus writes
these shouts with the leading "Uo" in five records, so the member 4 form was the
outlier and was aligned.

**Stages 72 and 73 translated** (869 records over 7 slices): `STG0072` 483,
`STG0073` 386. All four members clean under `check_stage.py`; `check_names.py`
clean corpus-wide. Paired because each alone was too small for a batch, while
every member still merged whole.

**The portrait trap demonstrated from both sides inside one batch.** The brief's
auto-generated cast section attaches Ray Lovelock's Macross 7 bio to every
`pid_RAY_S` line. In stage 72 that bio was RIGHT -- two slices confirmed Ray
from the Fire Bomber cast around him and used `$$レイ#168$$`. In stage 73 the
same portrait and the same bio were WRONG: the line names Ikari and an EVA, so
it is Rei Ayanami, `$$レイ#333$$`. Same metadata, opposite correct answers, each
settled by reading the scene.

**A name that matched a term from the wrong series.** `地獄王ゴードン` is one of
Dr. Hell's generals; the glossary's bare `ゴードン` is sourced to The Big-O, a
different Gordon from Roger's storyline. A slice checked the term's `source`
field, found the mismatch and wrote plain English -- the 先生 test applied
before anything went wrong rather than after.

**The banner rule's two clauses conflicted, and a slice resolved it correctly.**
Sha `ed6ce3cc16` already ships with 6 leading spaces while its Japanese source
has 9. Copy-the-shipped-sha wins; copy-the-source applies only to banners with
no twin.

Elongation handled with unusual precision: a scream stretching a NAME cannot be
a token, but a scream stretching `貴様` next to a name leaves the name
tokenised. Both appeared in one slice and both were right.

**Two splits with no precedent, recorded rather than swept.** `ミレーヌさん` is
"Ms." in 6 shipped records and "Miss" in 6 -- a dead tie, so a slice picking one
is not ignoring precedent. And `ヴェーガ人` shipped as "Vegan", which parallels
`アルテア人` -> "Altairan" but reads as the dietary word in modern English,
especially in the insult it appears in. Each demonym had exactly one record, so
neither was an established pattern; rewritten as "some fool from Vega".

Also fixed: three records rendered a bare `「！」` as "...!", adding an ellipsis
the source does not have. Zero cross-member conflicts in either stage -- the
first batch since that check was added where it found nothing.

**CLAUDE.md's own cautionary examples had no glossary entries.** It names Urzu,
Quent, Chirico and Battling as the terms whose literal English "forced the
manual project-wide sweeps" -- the story the whole `$$` convention rests on.
Only Chirico was actually a term. ウルズ, クエント and バトリング could not be
tokenised at all, so renaming any of them would have forced the same manual
sweep again. All three added.

Battling looked like the dangerous one, since its English is also an ordinary
participle -- the exact shape of the 先生 and ヒル bugs. It is not, and the
reason is worth recording: `tokenise_stage.py` only offers a term whose
JAPANESE appears in the record, so an everyday "battling" in a record without
バトリング is never a candidate. The corpus confirms it -- 0 capitalised
"Battling" anywhere the Japanese lacks the term. That property is what made the
ゲパルト additions safe too.

**A sweep backlog from another session's terms.** Dry-running the tokeniser
against the HEAD glossary reported 148 records already pending -- nothing to do
with the three new terms. A concurrent session added eight location keywords
(カミナシティ, ヘルマジスタン, 聖天使学園, ア・コバ, アレギウム, バルエヨルズル,
第３新東京市, アクエリア市) and committed them without running the tokeniser, so
the corpus had been carrying literal English for terms that already existed.
Adding a term without sweeping leaves exactly this gap.

234 records tokenised in total across 69 files -- 86 from the three new terms,
148 clearing that backlog. Verified independently of the tool's own round-trip
guard: every record in all 69 changed files was expanded and compared against
HEAD. 17,318 records compared, 0 differences, so nothing on screen moved. All
166 members whose Lua is extracted here pass `check_stage.py` with 0 problems
and `check_names.py` is clean.

**Stage 71 translated** (597 records over 7 slices): 308 in member 3, 288 in
member 4, plus a single-record member 2. All clean under `check_stage.py`;
`check_names.py` clean corpus-wide. The corpus passes 40,000 records.

**A new cross-member check found two inconsistencies the merge cannot see.**
`merge_stage.py` compares answers within ONE member. When two slices in
different members answer the same sha, nothing compares them -- that is how
stage 70 shipped one 先生 record tokenised in member 3 and plain in member 4.
Comparing members directly against each other found two in stage 71:
Bonta-kun's catchphrase split "Fumoff!" against "Fumoffu!" (shipped text
settles it 33 to 2), and a Kaname line where one slice added a question mark
the Japanese does not have. 龍神会 was also split "Ryuujin Society" against
"Ryuujinkai" and went to the in-stage majority. The fixes ran in both
directions, so neither member was the better one -- which is the argument for
comparing rather than trusting file order.

**`check_names.py` raised a false positive, and the gap was mine.** When the
Kurogane Five exception was settled -- that their swordsman IS glossary 208 --
their names were never added to the checker's confirm pattern, which lists only
Shin Mazinger mecha markers. So a Kurogane scene had nothing to confirm it, and
because these late stages mix casts, a Full Metal Panic name five records away
tripped the "wrong" marker. The record was correctly tokenised throughout.
くろがね / 五人衆 / ジャンゴ / お菊 added to the confirm pattern.

**The four-line ceiling counts the speaker name.** Two slices discovered this
independently, each after a draft was rejected: a spoken record gets at most
THREE lines of speech, because `check_stage.py` splits the whole record. The
shipped corpus agrees exactly -- 5,211 records sit at three speech lines and
none at four. Rule 3 now says so. That is the third brief ambiguity this
session, all the same shape: a rule that reads clearly while omitting the
detail that decides it.

**A joke that tokenising would have destroyed.** One record has Alto drop the
"-kun" from Bonta-kun's name, and the next record is Klan correcting him for
exactly that. Tokenising would have expanded the name to its correct form and
erased the setup one line before the punchline. The slice wrote it plain and
said why. No mechanical check could have caught it.

Stage 71 is largely a recap of stage 70: roughly 190 of its 230 dialogue
records reuse shipped answers verbatim by sha, including one slice that was a
complete repeat. Duplicated effort becomes guaranteed consistency.

**Stage 70 translated** (744 records over 7 slices): 505 in member 3, 238 in
member 4, plus a single-record member 2. All clean under `check_stage.py`;
`check_names.py` clean corpus-wide.

**A second term whose English is an ordinary word had been tokenised.** `ヒル`
is a Gundam UC pilot named Hill. The banner 陣代高校　裏山 -- a school's back
hillside -- shipped in stages 2 and 47 as "Jindai High, Back $$ヒル$$",
because `tokenise_stage.py` matches on the English side and saw the word
"hill". Exactly the 先生 failure, found by a slice that then avoided writing
"Hill" in its own new 裏山 banner. Both records de-tokenised with the
expansion asserted identical first, and "hill" added to the tokeniser's
ORDINARY refusal set. The set now holds an, angel, boss, king, lady,
president, princess, queen, sphere, will, zero, sensei, hill.

**The brief contradicted the checker about line counts, and slices obeyed the
brief.** Rule 3 said "keep the same number of lines"; `check_stage.py` says
the opposite in as many words -- "NOT the same count as the source: English
often needs one more line, and 40 shipped stage 1 records use four where the
Japanese used three". Two slices spent real effort recombining lines to
satisfy a rule that shipped stage 1 does not follow. Rule 3 now matches the
checker and carries the single-fullwidth-space rule alongside it, since both
facts about line shape were previously in different documents and one was
wrong.

Last batch I called a slice's parity-checking "stricter than the project
wants". That was half right: the checker allows extra lines, but the brief
demanded parity, so the slice was following instructions exactly. The defect
was the instruction.

**My own 先生 rule caused an error in the opposite direction.** CONVENTIONS
said the token is rare -- 39 of 332 records -- and a slice read that as a
default, writing plain "Sensei" for the Kurogane Five swordsman. He IS
glossary 208: the term and くろがね屋 are both sourced to 真マジンガー　衝撃！Ｚ編.
Two records corrected, text-neutral. The rule now says the test is whether
the TERM'S SERIES matches the SCENE, never frequency.

**`merge_stage.py` cannot see across members.** Those two slices answered the
same sha differently but sat in different members, so the merge compared
nothing and wrote one file tokenised and the other plain. Recorded in
CONVENTIONS: after merging a multi-member stage, compare members against each
other for shared shas.

**A slice wrote its own entry into CHANGELOG.md**, against its instructions.
No content was lost -- every prior entry survived and the file is back to
7,464 lines -- but a 120-record slice's prose does not belong in a
project-level log shared with another session's in-progress work. Removed.

**Stage 69 translated** (1,038 records over 9 slices): member 3 is 907 records,
member 4 is 131. Both clean under `check_stage.py`; `check_names.py` clean
corpus-wide.

**A rank sweep I ran broke a shipped line.** Amuro's 大尉 was "Captain" in 66
records and "Lieutenant" in 5, so I swept the outliers. The sweep matched on
"this record's Japanese contains アムロ大尉 and its English contains
Lieutenant" -- and one stage 37 record names two officers: Amuro (大尉,
Captain) and Apolly (中尉, Lieutenant). It rewrote Apolly's correct rank into
"Captain".

I had flagged that exact risk before running it, checked three records, found
them clean and swept anyway; the record that broke was one my survey had
counted as already-correct because it contained both words. Restored -- stage
37 now shows no diff at all, since the sweep and the repair cancel -- and an
audit of every swept record for a second rank term found no other collision.
CONVENTIONS.md now carries the rule: a rank sweep must require that the record
names no other rank.

**サガラ settled as plain "Sagara".** The one substantive cross-slice conflict
out of 40: a slice tokenised it as the given-name term. The corpus is 41 plain
to 1, and サガラ is not a glossary key -- it is the surname, a different string
from the given-name entry. Both slices' reports argued for plain; one had
written the token anyway. Third report-versus-file mismatch this session, which
is why claims are checked against the JSON rather than the prose.

クロウ normalised to "Crowe" (was a 2-2 split in shipped text).

Of 52 shas answered by more than one slice, 12 were identical and 40 differed;
filtering for token differences left exactly the one above. The rest are
paraphrase of lines repeated within a 907-record member.

**ゼロ appeared in three senses in one stage**, each resolved correctly by a
different slice: Lelouch (tokenised), the literal number zero in a line about
time progression, and the Wing Gundam Zero machine (plain, because the token is
reserved for the person).

The terms check keeps earning its place: six more mistyped kana in one slice's
draft (隼人, 刹那 twice, ロックオン twice, キラ), all from hand-written unicode
escapes in a build script, all caught as unresolvable glossary references.
Across this session that check has caught roughly thirty character-level typos
that reading would not reliably find.

**Branch 68B translated** (1,050 records over 10 slices), the largest single
script in the project: member 3 is 760 records, member 4 is 290. Both clean
under `check_stage.py` and `check_names.py`.

**`tokenise_stage.py` re-created the `先生` bug, and its safety guard could not
see it.** The tokeniser matches on the ENGLISH side, and `先生`'s English is
"Sensei" -- so a slice that correctly wrote plain "Sensei," at the start of a
quote had it converted straight back into `$$先生$$`, putting a Shin Mazinger
character into a Full Metal Panic deathbed line. The round-trip check is blind
to it, because the token expands to "Sensei" character for character.

`check_names.py`, extended two batches ago for precisely this class, caught it
on the run immediately after. `先生` is now in the tokeniser's `ORDINARY`
refusal set -- the mechanism that already refuses an, angel, boss, king, lady,
president, princess, queen, sphere, will and zero. Re-running the tokeniser now
changes 0 records where it previously changed 1, and `check_names.py` is clean
corpus-wide.

This is worth stating plainly: a fix applied to the corpus two batches ago was
being actively undone by another tool in the same pipeline, and only a checker
written for the original bug noticed.

**The brief never listed the fullwidth tilde as drawable.** Rule 5 gave
`「 」 《 》 　 （ ）` and no `～`, yet every location banner uses one and the
checker accepts it. A slice consequently dropped a character's elongated
`キリコちゃ〜ん` as undrawable. Rule 5 now lists `～` and warns against the
wave dash `〜` that looks identical and shipped wrongly 12 times.

**The Gates rule was ambiguous in my own wording.** `CONVENTIONS.md` said his
self-references get plain "Gates"; I meant plain of the honorific, two slices
read it as plain of the token. Reworded to `$$ゲイツ$$` with no "Master". That
rule has now produced a wrong variant twice -- first unwritten, then unclear.

47 shas were answered differently by two slices, which sounds alarming for one
script. Checking the tokens in each showed 0 substantive disagreements: every
one is paraphrase of a line repeated elsewhere in the same 760-record member,
and the merge applies one answer to all its occurrences. A banner was moved
onto its shipped 7-space form, and one mid-sentence "Sensei" lowercased.

Slices caught several of their own errors this batch: ASCII `~` for the
fullwidth tilde in two separate slices, and one build script that had mistyped
22 kana tokens (18 of them `ガイツ` for `ゲイツ`), all surfaced by the checker's
`terms` rule.

**Focus / Foc terminology standardized (user preference):** the earlier
Morale wording in stat requirements, Spirit/mech/skill/part descriptions and
status effects is now Focus. Weapon Info uses `Req. Focus`; compact skill
names use `Foc+ Dmg/Evd/KO/Hit` and `Foc Bonus`. Existing Focus Spirit-command
names and ordinary morale in character dialogue are unchanged. Two voice
tutorial lines about Ace stat bonuses also now say Focus. BASE_RULES records
the convention. This supersedes the Morale wording in earlier description
batches, not their mechanics or numerical effects.
`standardize_focus.py` snapshots and previews the scoped source migration;
part/skill hook generators rewrap to their existing limits (37 part and 59
skill description variants changed). `patch_focus_candidate.py` applies only
163 active EBOOT hook replacements, five RPW skill-name strings, and two
SRVC tutorial strings; no RPW description, offset, block-size, gameplay,
voice-table or executable-code changes. EBOOT adds 15,562 text bytes and
retains 3,495 lookup entries. AID rebuilt for the weapon checklist labels.
All 40 focused/regression tests pass; six new tests cover source consistency and exact binary-delta replay;
reward tests now replay their historical pre-Focus endpoint. Backups under
work/focus_*; no ISO/deployment/version-stamp changes. Live rendering pending.

**Counter-family labels and all stage GIFT report messages:** verified the
already-English Counter popup in the candidate and translated the remaining
Map / Wpn / Song cells beside it. All 22 nonempty stage reward/availability/
refund messages (87 occurrences), including all three Scopedog equipment
unlocks, now have 39 exact whole/line hooks. Proper-name glossary markers,
part-name database spellings, original line boundaries, and reward logic
are preserved. `gift_reports.py` inventories CP932 GIFT tables and generates
the hook file; inspection helpers under work were used for source/atlas QA.
The existing President centered-drawer wrapper now also measures English
for 18 exact reward lines, excluding already-padded AG lines. No generic
centering or reward behavior changes. `patch_gift_candidate.py` snapshots,
previews and applies an isolated candidate update: 30 hook additions, no
removals, 3,760 appended text bytes, 3,495 total lookup entries. AID rebuilt
with 41 members / 14,242,708 bytes. Standard build and audit integrated;
skill regression replay updated to its historical pre-reward endpoint.
34 targeted tests pass, including 252 emitted-PPC centering cases and
packed-art boundary checks. Broader audit still stops at an existing
conflicting `・反撃する` duplicate in issue_hook.json; left untouched.
See `docs/GIFT_REPORTS.md`. No ISO/deployment/release/stamp changes; live
rendering is not yet verified.

**Pilot-skill descriptions reviewed against Akurasu (68 skills / 124 variants):**
rewrote the full and alternate descriptions for clearer in-game help,
including Half Cut, Support Attack's per-available-use Assist bonus, and
conditional/leveled skills. Existing skill names and gameplay data unchanged.
`skill_description_catalog.py` plus dry-run-first `build_skill_descriptions.py`
generate the complete hook file; every variant fits <=3 lines / 740px at 28px.
Retained game-specific variants missing from the wiki; Feral's critical bonus
follows the wiki's +30% rather than the JP help's +20%, without changing
runtime behavior. Other reference differences are recorded in
`docs/PILOT_SKILL_DESCRIPTIONS.md`.
Disabled automatic line pairing for this description file only. Isolated
candidate EBOOT update: 124 full replacements, 181 obsolete fragments removed,
9673 new text bytes; code/voice/RPW data and file size preserved. Six new tests
and twelve regression tests pass. Updated the Power-part test to separate
historical byte-isolation verification from current installed-hook checks.
No ISO/deployment/release/stamp changes; live visual confirmation pending.

**Weapon-use requirements warning translated (14 widgets):** the screenshot's
header now reads “The following requirements are not met.” Ammo, EN, Morale,
Skill, Terrain, Range and Use After Moving are translated in both the dim
checklist templates and individual highlighted failure templates. **Correction
2026-09-25:** this covered stored FSSA widgets only; the native runtime table
replaced their text and was missed. See the runtime weapon-warning correction
above. Morale was subsequently standardized to Focus. The Maximum Break
checklist variant and both related post-move weapon-property blocks are
covered too. Preserved bullets, placeholder rows, line counts, colors and
failure-state metadata. The header and its separate orange “requirements”
overlay use measured English positions so the accent remains registered.
`weapon_requirements.py` is integrated into build_ui/check_issue_fixes;
candidate AID rebuilt. Three new tests pass (exact source-family inventory,
packed text/overlay styles, byte isolation), plus three Weapon Info and six
Power-part regressions. No gameplay/EBOOT/font/ISO/deployment/stamp changes;
live visual confirmation remains pending.

**Power-part descriptions reviewed against Akurasu (69 parts / 300 variants):**
replaced 299 English variants across full, shop, consumption and DLC help;
one was already identical. Corrected MAP/range-1 exclusions throughout,
clarified Auto-Defenser's immunity/penalties and Damage Avenger's missing-HP
formula, restored omitted effects/conditions, and resolved all nine Miracle
Fragment Spirit names from the current dictionary. F Bomber now follows the
reference's second deployed player turn. Names and gameplay values unchanged.
`parts_description_catalog.py` and dry-run-first `build_parts_descriptions.py`
provide a reproducible source; generated JSON replaces the old stale
`unshipped` metadata. All 300 variants fit three lines / 540 native pixels
at the candidate's 28px glyph size, including DLC markers. See
`docs/PARTS_DESCRIPTIONS.md` for reference discrepancies and scope.
Disabled automatic per-line pairing for this hook file only: its newly
wrapped prose must not generate unrelated sentence-fragment translations.
The isolated candidate update replaces 299 full hooks and removes 207 obsolete
fragments (17,534 new text bytes); other hooks, code, voice data, RPW and file
size are preserved. Six tests pass, plus three President-report regressions.
In-game visual verification remains pending. No ISO/deployment/build stamp.

**Upgrade labels / blank intermission Library / support counter follow-up:**
translated both Weapon Rank headers and both Sight/Wpn Rank footer blocks,
suppressing only the old separate RANK suffix widgets. Support Def's narrow
preview title is now S. Def; the adjacent Re-Attack title is Re-Atk, alongside
the previously fixed S. Atk. All three leave over 12 native pixels before
the existing use-counter position, with numeric widgets unchanged.
The prior Library live-centering attempt added a spacer and changed the
buttons' special text mode from 0x01 to 0x41. Reverted those two changes for
all six title widgets (five choices, Robot Encyclopedia has two states):
plain English glyphs, original special mode, measured left-edge placement.
PS Store and the Library help-description centering are unchanged. The later
2026-09-13 live screenshot confirmed visibility but not title centering;
capture-measured X corrections now handle the remaining Library offsets.
Candidate
AID rebuilt; three new packed tests and four deployment regressions pass.
Restored Library visibility still needs in-game confirmation; no ISO,
deployment, EBOOT/font or build stamp changes.

**Stage 67 and branch 68A translated** (547 records over 5 slices): `STG0067`
515, `STG0068A` 32. All three members clean under `check_stage.py` and
`check_names.py`.

**Stage 68 turns out to have no dialogue at all.** Its member 2 is a shared
`common_event.lua` helper and member 8 a binary table; `prep_stage.py` reports
0 records. The disc explains it: `STG0068A.SDAT` and `STG0068B.SDAT` sit beside
it, so 68 is the routing script that chooses between them. It is the only one
of 140 prepared scripts with nothing in it, so the "to go" count includes one
script that can never be completed. `STG0068B` is 1,050 records over two
members and gets its own batch rather than being split across two.

**A rule settled but never written down produced a third variant.** `ゲイツ様`
was decided last batch -- "Master $$ゲイツ$$" when others address him, plain
"Gates" for his own third-person boasting -- and recorded in the changelog and
the commit message but NOT in `CONVENTIONS.md`, which is the only file slices
read. A slice duly coined "Lord Gates" for a self-reference. Fixed, and the
rule is now where it can actually be found.

**`法皇` needed splitting by grammar, not by speaker.** Two slices independently
flagged the token reading oddly. Checking every record showed most were already
right -- "His Holiness $$法皇$$ Theo VIII", "the new $$法皇$$", "I am no longer
the $$法皇$$" -- and only two were wrong, both for the same reason: a token
cannot inflect and cannot be an address form. `法皇猚下` in direct address is
"Your Holiness", not "Pope, please tell me!"; `法皇選` is "the papal election",
not "the Pope election". One slice had already written "the papal seat" in the
same stage, so the natural form was in front of us.

Also recorded: a name broken mid-word by an ellipsis cannot be tokenised at all,
because the token is atomic. A slice hit this with a character gasping a name
across a pause and correctly wrote it plain.

Worth noting against the reports: `tokenise_stage.py` put 15 of branch 68A's 32
records back onto tokens, despite that slice's report listing the tokens it had
applied. The report was written in good faith and was wrong about its own
output -- the second time this batch a slice's description did not match its
file, so the file is what gets checked.

**Barrier/defense popups and deployment menu:** replaced shared map-battle
sprites for Barrier, Shield Def., Parry and Double Image (compact Dbl Img).
Translated seven related map-help widgets, including both Retrieve and Map
Search variants. Translated both deployment SR Points/Teams labels, the
map SR Points/Turns variant and all three paired Z Chips/Funds labels;
removed only the two Japanese team-count suffixes. Aligned 12 separate
colon widgets to avoid English-label overlap, leaving numeric counters untouched.
The later six-digit Funds report exposed number/separator overlap; the
2026-09-13 currency fix removes the six Funds/Z Chips separators instead.
Candidate AID rebuilt and four packed regression tests pass. Added the exact
screenshot-derived Robot Mafia display hook (43 EBOOT bytes changed in the
hook table/reserved string area only). Its underlying faction source table
was unlocated at that time. The 2026-09-13 sweep found the literal preset
team-name fields and covers all 157 names across 142 archives; live retest
remains necessary. No ISO/deployment/build stamp changes in this older batch.

**Decision: the location-banner drift stays as it is.** The same scene-title
card ships at different horizontal positions depending on the stage -- the
leading fullwidth spaces are the layout, and they were re-eyeballed instead of
copied. Re-measured at the time of the decision it is 15 banners across 201
records, up from the 14 / 106 first reported several batches earlier, because
each new stage copies whichever shipped shape its slice found.

The alternatives were to normalise each banner to its most-used shape, or to
centre them properly -- the Japanese source centres by an exact rule, indent =
floor((60 - body half-widths) / 4), which reproduces every source indent tested.
No English banner is actually centred; measured against the real font the
correct indents would be 8-13 where shipped values are 2-12. Centring was the
only option with a derivable answer, and it would have changed how every
location card in the game looks. The user chose to leave it.

Standing rules, unchanged and now not provisional: match a shipped sha
character for character; for a banner with no shipped twin use the Japanese
source's own leading-space counts; never re-centre by eye.

**Mech Info title alignment:** centered both source variants inside the
existing title tab (native center x=312), matching the English label's
152.09375 px advance at its unchanged 31 px font size. Only the two title
x fields change; adjacent tabs, baseline, stats, parts and abilities stay
untouched. Integrated into UI builds and issue checks, with three tests
covering source inventory, packed placement/byte isolation and the actual
English hook. Candidate AID rebuilt; no ISO/deployment/build stamp change.
Live placement still needs checking.

**President Clear Report alignment:** centers all three runtime lines using
their English glyph advances instead of the pre-translation Japanese length.
The variable fullwidth PP amount is preserved, including multi-digit values.
A narrowly matched centered-draw wrapper handles the two exact President
headings and `+<digits> PP.`; unrelated text retains the original drawer.
Three tests pass, including 180 emitted-PPC centering/register cases, malformed
and unrelated input fallbacks, hook agreement and byte isolation. Candidate
EBOOT updated only in three reserved regions; no font, voice, reward logic,
ISO, deployment or build stamp changes. Live placement still needs checking.

**Combat Record navigation and help:** translated Trade List and Z Crystal
Status links, with all three copies of all four navigation choices covered
(12 widgets total). Added the four matching UTF-8 help messages for Pilot
TOP 5, Trade List, Lecture Plates and Z Crystal Status. Removed only the
Japanese 人 suffix from both Ace Pilots counters, retaining their numeric
values. Three new packed tests pass. Candidate-only; not deployed or in an ISO.

**Stages 65 and 66 translated** (1,127 records over 10 Sonnet slices):
`STG0065` 555, `STG0066` 572. All four members clean under `check_stage.py`
and `check_names.py`.

**51 records shipped with over-indented continuation lines, and no check can
see it.** Line 2 onward of a speech starts with a single `　`, matching the
source; one slice used two throughout its range, 65 lines in all.
`check_stage.py` measures line count and real pixel width, and an extra leading
fullwidth space passes both -- the line just sits shifted on screen. Caught by
comparing each record's leading spaces against its own Japanese, and now
written into `CONVENTIONS.md` as a rule with the reason it is invisible.

**Six cross-slice disagreements, three of which were not errors.** Splitting a
member across translators produces terms rendered two ways, and only the merge
sees them -- and only when both slices answer the SAME sha. Where they answer
adjacent records, nothing mechanical notices.

  * `教団` came back as "the cult" and as "the Order". Shipped precedent is
    7 to 2 for "Order", and "cult" is a judgement the Japanese does not make.
  * `触れ得ざる者` normalised to `'Untouchable'`, 9 shipped records.
  * `白いの` -- Gates taunting a white-painted machine -- came back once as
    "whitey", which carries a connotation in English the Japanese does not.
    Now "white one", matching the same speaker's other line about the same
    target.
  * `ゲイツ様` looked like a conflict and was not: subordinates addressing
    him get "Master Gates", his own third-person self-aggrandisement
    (`このゲイツ様`) gets plain "Gates". Both slices were right. Left alone.
  * `スズネ先生` looked like drift in a slice's report, but its actual
    output tokenised the name correctly. The report was wrong, not the file.
  * `ソースケ` is genuinely split in shipped text: 61 records tokenise it,
    56 write plain "Sousuke". New work now tokenises (7 records, each asserted
    text-identical first). The 56 are a corpus sweep, recorded not swept -- and
    since the token expands to exactly "Sousuke", that sweep would move no
    pixel; it is only about keeping the name attached to its glossary entry.

The `先生` fix from last batch propagated on its own: a slice hit the same
characters and the same phrase, found the corrected plain "sensei" in stage 64,
and matched it. Another slice met `先生` four times and split them correctly
without help -- `神楽坂先生` plain, `スズネ先生` with the name tokenised,
neither as the Shin Mazinger term.

**Weapon Info tab alignment:** centered both copies of the heading inside
the existing title tab instead of retaining the Japanese label's starting
position. Measured 190.84 px English width at the existing 31 px glyph size,
centered at native x=400. Only the two title x coordinates change; font,
baseline, U/P/R tabs and weapon data columns remain untouched. Three new
packed-candidate tests pass. Not deployed or included in an ISO yet.

**Support popup and Spirit/Skills result headings:** completed the shared
Support Defend sprite and related Re-Attack/Counter map-popup pieces. Added
SP Cost and +Eff. to both Spirit-result variants and Uses to the Skills list.
SP Cost replaces the complete split Japanese heading; only its obsolete SP
suffix widget is hidden, not the separate current/max SP column. All five
matching source-header occurrences are covered. Three new packed tests pass;
artwork preview reviewed. Local candidate only, not deployed or in an ISO.
The translated words subsequently shipped in 0.6.3, but its Japanese-width
map quads squeezed the English; corrected on 2026-09-13 as noted above.

**Battle action/target-selection category sweep:** translated all four native
battle-animation attack badges (ALL, Center, Wide, Assist), Combo Attack and
the Counter / Attack Again / Support Attack / Support Defend banners. These
are separate CMN textures from the previously translated map-menu sprites.
Translated all six action-menu variants, the Center/Wide selector and the
standalone Assist Attack row; runtime choices include No Assist, Defend,
Evade, Counterattack, Select Weapon and Do Not Join. Added all four adjacent
battle-selection warnings, including “You cannot select an attack target.”
Rechecked Power Parts and its related headings. Four new packed-family tests
pass; menu fit and artwork previews checked. Candidate only, not deployed or
released; the separate stage-68 full-build blocker is not bypassed.

**Map-menu screenshot follow-up:** translated the separate Power Parts,
Transform, Spirit Commands and Element Change popup headings with measured
English centering. Added native Armor/Sight stat-popup sprites and removed
their shared Japanese value suffix; down arrows, colors and animation data
are unchanged. Verified the existing four Tag Command translations and both
clear-marks prompt lines in the packed candidate, preserving the prompt's
fixed-length UTF-8 source copies. Three new packed-asset tests pass. Local
candidate only; no deployment or ISO rebuild.

**Title-screen Library submenu translated in-game:** Robot Encyclopedia,
Character Encyclopedia, Glossary, Sound Select, and Scenario Chart. Replaced
the five Japanese labels in their shared native atlas, including all normal
and highlighted animation references. Existing English buttons, selection
effects, title artwork and version footer are preserved. Local candidate only;
no ISO, deployment or release produced for this change.

**Stages 63 and 64 translated** (1,040 records over 10 Sonnet slices):
`STG0063` 371, `STG0064` 669. 149 registered members pass `check_stage.py`
with 0 problems and `check_names.py` is clean corpus-wide.

**`check_names.py` now catches a term whose English is an ordinary word, and
found 22 shipped records on its first run.** `先生` is a real glossary term --
a Shin Mazinger character, zukan 208 -- and also what a student calls a teacher
and what Yu Fan calls Gauron. Of the 332 records whose Japanese contains it,
only 39 mean the character. A slice hit this in stage 64: it ran `terms.py
list`, found a genuine entry, tokenised it, and so put one series' character
name into another series' private thought. Everything it did was procedurally
right.

The 22 already-shipped cases were all in stages 3 to 9, Suzune addressed by the
protagonist. Nothing was visibly wrong in any of them -- `$$先生$$` expands to
"Sensei", which reads correctly for a student addressing a teacher. The damage
was referential: renaming that Shin Mazinger character would have silently
rewritten Suzune's scenes. Each was de-tokenised to the literal "Sensei", every
replacement asserted to expand identically first, so no rendered character
moved.

The checker previously knew only `レイ` and `ドロシー`, which are name-against-
name collisions. This is a larger class: a name against a common noun that is
seven times more frequent.

**Tessa's rank was wrong in six records.** `大佐` is "Colonel" 96 times across
the corpus, but she commands a submarine and hers is the naval reading.
Counting only records where she is named and the Japanese has no `艦長` to
account for it, the corpus runs 10 "Captain" to 3 "Colonel". Three shipped
outliers in stages 32 and 48 and three new stage 64 records moved to "Captain",
guarding against corrupting "Lt. Colonel" in a line spoken by Mardukas. Also
normalised Sousuke's alias `カシム`: "Kashim" from three slices, "Kassim" from
a fourth.

**Three slices built new location banners three different ways**, each citing
`CONVENTIONS.md`: copying the Japanese source's leading-space counts, a fixed
1/2/6 shape, and analogy from a same-length banner. That file only ever settled
banners that already ship, where the rule is to copy the sha. It now names a
default for new ones -- copy the source's own counts -- and says plainly that
this does not centre the English. The real fix is the open decision on the 106
drifting records.

Stage 64's member 2 holds one record, and members 2 are not normally dialogue.
That slice established from the raw Lua that it is a formation-tag argument to
`SC_UNIT_JOIN_TO_TAG` rather than a spoken line, confirmed the shape against the
same call in stages 41 and 49, and avoided three decoy occurrences of the same
string sitting in `--|` dev comments that `luarec` does not extract.

**Save-question alignment and Kouji's end-session scene (2026-09-11).**
The shipped `Save complete. / Continue playing?` translation was left of center:
this dialog splits the Japanese text into independent draw calls, so a whole
message translation did not correct either line's original-width positioning.
Six save/overwrite/return prompt lines now have individual live-width pads.
The separate left-aligned save-status widget is repointed without a pad to
prevent the shared Japanese sentence from moving it accidentally. Yes/No
layers and selection behavior are untouched.

Translated all seven dialogue records in Kouji/Shiro's `STG0700` event `t_060`,
including the screenshot's opening line. This is separate from the already
translated battle-voice text. All other end-session scenes remain unchanged;
all voice IDs, wait commands, expressions and non-text bytes are preserved.
The new partial scene is source-hash-bound and built into `STG0700.SDAT` with
the global font mapping.

Trophy 022 `休息の時` becomes `Time to Rest`; its description becomes
`View an end-session message.` Both bundled locale files are covered. Trophy
IDs, conditions, icons and other trophy entries are unchanged; the TRP SHA-1
is regenerated for RPCS3. No earned-trophy or save records are touched.
Build/distribution paths now include the scene and the sibling TROPDIR package;
ISO paths are normalized within PS3_GAME. See `docs/SAVE_QUIT_FIXES.md`.
This batch's packed-output checks pass (including 11,520 PPC centering cases
and the scene's SDAT round-trip). At the time, full suite: 38/40 because of
STG0068 source-audit lookup failures. The lookup was fixed on 2026-09-12;
the now-exposed missing mission coverage still prevents deployment.

**Deployment confirmation and complete map-caption family (2026-09-11).**
Translated both team and battleship confirmation prompts/options, five related
headings, two live-counter labels and three deployment help rows. Original
numeric counter fields are untouched. Seven new blank glyph pads preserve
dynamic centering using the original Japanese character count.

Translated all 83 Japan/world/space map-pin caption assets, including the
screenshot's `第２新東京市` (Neo Tokyo-2). Captions retain their original
left/right anchors and sampled rectangles; animation, timing and map art are
unchanged. Eight missing location terms were added to the glossary; uncertain
romanizations remain explicitly provisional. The existing Jindai caption now
uses the glossary's Neo Tokyo-2 consistently. See
`docs/DEPLOYMENT_MAP_CAPTIONS.md` for coverage, checks and runtime limitations.
The candidate build was not stamped or deployed: the mission audit rejected
STG0068's different member layout. That lookup was fixed on 2026-09-12;
missing mission translations still block the build. Counter stays 0.6.2.

**Stages 61 and 62 translated** (1,078 records over 10 Sonnet slices):
`STG0061` 518, `STG0062` 560. All four members clean under `check_stage.py`
and `check_names.py`; 144 registered members now pass with 0 problems.

**211 records showed a Japanese speaker name over English dialogue.** Stage 14
(101), stage 17 (96), stage 53 (12) and stage 47 (2) had the name line left as
raw Japanese -- the player reads an English line under a name written in kana.
Nothing caught it: the build includes kanji, so the glyphs really are drawable
and the charset check has no reason to object, and `tokenise_stage.py` could
not reach them because it finds terms by matching the ENGLISH side and there
was no English to match. 197 of the names matched a glossary term exactly, so
they converted to tokens with the record's own Japanese as proof; the other 14
were role labels (`研究員` Researcher, `市民` Citizen, `傭兵` Mercenary). One of
those carried a fourth near-identical-kanji error: a record whose Japanese is
`傭兵` had `僭兵` in the English.

Also fixed: one record shipped `$$ミコノ$$さん`, keeping the Japanese honorific
attached to the token. The corpus drops it -- 33 shipped records render that
name bare.

**AG spoke in capitals in two stages where he should not have, and the brief
told him to.** His glossary `voice` note said to keep ALL CAPS "until he says
in-story that he will switch to normal speech (stage 2 member 3, record 299)".
Briefs number their own records locally, so "record 299" reads as record 299 of
the member in front of you. Two slices read it that way and kept AG shouting
through stages 58 and 60 -- both of which this session had already registered.
The corpus runs 899 sentence-case records against 37 caps, and every legitimate
caps record is in stage 1b or 2.

20 records converted to sentence case. Not by lowercasing: the lines carry
non-token proper nouns (Char Aznable, Daguza, Sazanka) and the Z currency,
which a blind `.lower()` destroys. The first pass capitalised after every line
break, which is wrong -- a wrapped continuation line is mid-sentence, not a new
one -- and the corrected rule then missed two places where a trailing ellipsis
really does end a sentence, so those two were set by hand. The `voice` note now
says the location is absolute, and `CONVENTIONS.md` records what the misreading
looked like.

**A note on a concurrent edit.** Another session added eight location keywords
to `analysis/glossary.json` while this batch ran, `カミナシティ` among them. Two
slices had reported that term as absent, which was true when they looked and
false by the time the tokeniser ran -- so the stage 62 files now reference an
entry this batch did not add, and the glossary change ships with them. Both of
my earlier `ゲパルト`-family entries survived that session's rewrite intact.

**A machine's short name was not a glossary term, so 88 records named it in
literal English.** The glossary had `アクエリオンゲパルト` and
`アクエリオンスパーダ` but not the bare `ゲパルト` / `スパーダ` the dialogue
actually uses, and the same gap covered `オックス` (for `ブラックオックス`) and
`スペースロボ` (for the numbered `スペースロボ１号` and friends). The short
form is the common one -- 231 occurrences against 68 inside a compound, across
27 stages -- so renaming any of those four machines would have missed most of
its mentions. Four `proposed` entries added; the corpus was otherwise already
fully tokenised, so all 88 changed records come from this one gap.

Two things were checked before touching anything, because the short forms are
suffixes of the compounds:

  * `token_for` needs a `zukan_id` only when two terms of the SAME kind share
    a Japanese string. These four are unique, so `$$ゲパルト$$` addresses
    exactly one term. Non-official entries are established practice -- the
    glossary already carries 53 `proposed`, 16 `ambiguous`, and 34 with no
    `zukan_id` at all.
  * Rewriting "Aquarion Gepard" to "Aquarion $$ゲパルト$$" would expand back
    character for character, so `tokenise_stage.py`'s round-trip guard could
    not catch it. It never arises: `refs()` sorts matches longest-first and
    drops any term contained in a longer kept match, so the bare form is
    suppressed in any record that also names the compound.

Verified independently of the tool's own guard: every record in the 20 changed
files was expanded and compared against `HEAD`. 4,528 records, 0 differences,
so nothing on screen moved. All 140 members whose Lua is extracted here pass
`check_stage.py` with 0 problems.

**Stages 59 and 60 translated** (1,016 records over 10 Sonnet slices):
`STG0059` 513, `STG0060` 503. `check_stage.py` and `check_names.py` clean on
all four members.

**One character held three different titles inside a single member.** Three
slices of `STG0059_00003` rendered `学長` as "Dean", "Chancellor" and
"President". Only two of them collided on the same `sha`, so `merge_stage.py`
reported one conflict and silently kept both of the others -- the drift lives
in adjacent records, where nothing mechanical looks.

`学長` had no shipped instance anywhere in `translation/`, library included,
so there was no precedent to reuse. The corpus still constrained it: `社長` is
"President" in 15 records (Watta) and `長官` is "Director" in 33 (Otsuka), and
both men share Momoi's scenes, so two of the three proposed titles would have
rebuilt the `中佐`/`大佐` collision fixed in the last batch. Settled on "Dean".
Two `専務` records that had come back as "the VP" were moved to the shipped
"Director", and all four members re-measured clean afterwards.

One slice argued for "President" on the grounds that Momoi's library bio
renders `学長選挙` as "university presidential election".
`translation/library/pt_200.json` contains no `学長` at all, so that reading
was not used. A cited precedent is worth opening before building on it.

Recorded in `CONVENTIONS.md` with the shipped counts, plus one genuinely open
collision: `専務` and `長官` both read "Director" and both appear in the
Dai-Guard cast. Separating them means moving shipped records, so it waits for
the user alongside `様` and `総帥`.

Also confirmed this batch: the `#` discriminator takes a kind as well as a
zukan id -- `$$宇宙魔王#pilot$$` distinguishes the character from his machine,
and five slices reached it independently without coordination.

**Stages 57 and 58 translated** (1,091 records over 10 Sonnet slices):
`STG0057` 471, `STG0058` 620. `check_stage.py` and `check_names.py` clean on
all four members; the tokeniser had only 3 records to put back on a token, so
the slices are writing `$$japanese$$` correctly now.

Twenty shas came back answered two ways, because a repeated scene straddles a
slice boundary and two translators rendered it independently. All twenty are
paraphrase, not error; `merge_stage.py` keeps the first file's answer, which at
least applies one reading to every occurrence.

**The same location banner was drawing at different offsets depending on the
stage.** A banner's `sha` is its Japanese, so every stage shows identical
English -- but the leading fullwidth spaces that centre it were re-eyeballed
per stage. 14 banners ship in more than one shape across 106 records; the
D-Trader one alone has nine, spread over 84 records. Stage 57 had just invented
a fourth shape for the Quarter Hangar, so the new stages were normalised onto
each banner's most common shape (5 records). The rest of the corpus is NOT
swept yet -- it is cosmetic, it is 100+ records, and five of the fourteen have
no majority to sweep onto.

Worth being precise about what is and is not a defect here: 544 shas are
translated more than one way corpus-wide, but 530 of those differ in wording,
and that is usually right -- a short line recurs in unrelated scenes and should
read differently. Only the 14 whitespace-only ones are the same text at
different offsets.

**A wave dash was standing in for a fullwidth tilde in 12 banner records.**
`〜` (U+301C) where the other 445 records use `～` (U+FF5E), in stages 47, 48
and 54. Both encode, so nothing failed; they are simply different glyphs in the
same decoration. Normalised to `～`, and all three members re-checked clean.

All 136 registered members whose extracted Lua is present locally pass
`check_stage.py` with 0 problems after these sweeps. The other 29 registered
members could not be re-verified here, their Lua not being extracted in this
worktree.

**`中佐` was shipping under four spellings, one of them the wrong rank.**
Two slices of the same stage rendered Daguza's rank differently, which is what
surfaced it. Across the corpus it was "Lt. Colonel" (17 records), bare
"Colonel" (8), "Lieutenant Colonel" (3) and "Lt. Col." (1).

Bare "Colonel" is the one that mattered: `大佐` renders as "Colonel" in 96
shipped records, so the two ranks read identically -- and they share scenes,
Otto (`大佐`) referring to Daguza (`中佐`) in a single stage 14 line. Real
English does address a lieutenant colonel as "Colonel", which is why the
readings looked fine one at a time; in this script it erases a distinction the
dialogue leans on.

Settled as "Lt. Colonel" everywhere, bare or with the name, and swept across
stages 8, 14, 15, 35, 36, 42, 43 and 48 -- 14 records. The rank is four
characters wider, so every touched member was re-measured: all nine pass
`check_stage.py` with 0 problems. Written into `CONVENTIONS.md` so it is not
re-decided per slice; the earlier "rank words reconciled" pass (stage 43) never
recorded its decision anywhere, which is how the drift resumed.

**The brief template never mentioned `$c`, which is why the stage 31B bug
happened.** `check_stage.py` verifies `$c` as of the last batch, but rule 1 of
every brief still listed only `$n`, `$l` and `$F`, so a translator meeting
`$c` for the first time had nothing to go on. It is documented now -- what it
expands to, and that a line carrying one `$c` must come out with one `$c`,
never two to dodge a pronoun.

**Brief rules were numbered 1,2,3,4,5,7,6,7,8.** The glossary-token rule was
inserted with the wrong number when it was added back, leaving two rule 7s and
one rule out of order. Renumbered 1-9. Nothing about the rules changed; briefs
that cite "rule 7" in an older report mean the glossary-token rule.

Briefs for a stage are generated before its batch runs, so the stage 57 and 58
briefs on disk predated both fixes and were regenerated.

**Stages 55 and 56 translated** (1,030 records over 10 Sonnet slices):
`STG0055` 546, `STG0056` 484. `check_stage.py`, `check_names.py` clean on all
four members.

**`check_stage.py` now verifies `$c`, and found a shipped bug on its first
run.** `$c` is the player-named SQUAD -- the ZEUTH/ZEXIS slot, as in
「$cとして行動を開始します」 -- a runtime placeholder exactly like `$n`. The
escape check had only ever covered `$n`, `$l` and `$F`, so a dropped or
repeated `$c` would have shipped silently. Four separate translators flagged
it as undocumented before anyone wrote it down. With it checked, all 157
registered stage members pass except one: stage 31B used `$c` twice where the
Japanese has it once, so the line read "ZEXIS believed in him too, that's why
ZEXIS joined this dangerous mission!". The second is a pronoun now.

**The conventions file was ambiguous and caused a bug.** Its first-instance
list is written `` `ジェミニス` -> `Geminis` ``, which reads like a token
mapping; a translator duly wrote `$$ジェミニス$$` and the checker rejected it.
The list now says outright that its entries are plain English unless shown
with `$$`, and points at `terms.py list` as the authority.

Two pieces of translation worth keeping: `コミックスター` / `アトミックスマイル`
/ `コスミックスペシャル` each hide ミックス, building to Andy blurting out
MIX's name, and came out as "Comix Star" / "Atomix Smile" / "Cosmix Special"
so the gag survives; and `風呂んてぃあ` (風呂 "bath" grafted onto フロンティア)
is "Bathrontier".

**Stages 53 and 54 translated** (1,142 records over 10 Sonnet slices):
`STG0053` 708, `STG0054` 434. `check_stage.py`, `check_names.py` clean on all
four members.

**The brief was telling translators the wrong drawable characters.** Rule 5
listed the fullwidth set as `「 」 《 》 　` only, omitting `（ ）` -- so a
translator following the rule literally wrote ASCII brackets for thought
lines, and flagged the contradiction with the 1,076 shipped records that use
fullwidth. Both forms encode and fit; fullwidth matches the Japanese shape and
wins 1076 to 164. The 164 ASCII records are normalised, and
`tools/export_stage.py` now lists `（ ）` as drawable so the next translator
is not sent the same wrong instruction.

**An attack name was settled from the weapon list, not from dialogue.**
`無限拳` was split 2-2 between "Infinite Fist" and "Mugen Attack" and a
translator refused to break the tie alone. `translation/weapons.json` ships it
as "Mugen Attack" (with Genesys / Super Dimension / Cluster compounds), so the
two dialogue outliers now match what the weapon list draws.

`桂様` was 16-1 for "Master $$桂$$"; the one "Lord" is corrected.

**Stages 51A, 51B and 52 translated** (1,013 records over 11 Sonnet slices):
`STG0051A` 489, `STG0051B` 120, `STG0052` 524. `check_stage.py`,
`check_names.py` clean on all six members.

**The `ドロシー` trap entry added last batch paid for itself four times.** Four
separate slices met a "Dorothy" whose auto-generated cast bio was Dorothy
Catalonia's (Gundam Wing) and resolved her to `$$ドロシー#240$$`, R. Dorothy
Waynewright, by reading the scene -- Roger, Norman, Schwarz, Paradigm City. One
of them had `check_stage.py` reject a bare `$$ドロシー$$` as ambiguous first,
which is the tooling and the conventions file closing the loop between them.

**Slices are starting to coordinate with each other.** `インベーダー` has a
keyword sense and a robot sense that render identically, and one slice picked
its discriminator by reading the *adjacent slice's already-written answer file*
rather than deciding alone. The three remaining `#robot` uses are now
`#keyword` (29 of 32 already were), since the enemy is always spoken of as a
species, never as a named unit.

Translators again caught their own errors before merge via the checker: `『 』`
where `《 》` keyword links were required, 桜 typed for 桂, katakana where
fullwidth Latin was needed, and two invented tokens (`$$ＮＥＲＶ$$`,
`$$ランド$$`) for names that are not glossary entries.

A translator asked whether `ランド・トラビス` should be "Rand"; the library
already ships "Land Travis", so it stays until someone decides otherwise, and
`work/tr/CONVENTIONS.md` now says so rather than leaving it to be rediscovered.

**Stages 49, 50A and 50B translated** (1,056 records over 8 Sonnet slices):
`STG0049` 542, `STG0050A` 111, `STG0050B` 233. `check_stage.py`,
`check_names.py` clean on all nine members.

**A wrong-term token in shipped text: 10 records called Suzune "Sensei".**
`スズネ先生` was rendered `$$先生$$ $$スズネ$$`, but that `先生` term is Sensei,
a *named Shin Mazinger pilot* -- an unrelated character, matched only because
the honorific happens to be his name. All 10 now read "Miss $$スズネ$$". Found
by a translator searching the corpus for reuse.

**`check_names.py` now covers `ドロシー` as well as `レイ`.** A slice found the
brief labelling R. Dorothy Waynewright (The Big O) with Dorothy Catalonia's
Gundam Wing bio, and proved the right reading from a shipped stage-1 line. The
checker tests both directions -- Roger/Norman/Paradigm means Waynewright,
Relena/Treize/Romefeller means Catalonia -- and reports clean across the corpus.

**The unidentified-speaker marker is ASCII `???`, and I had this backwards.**
I swept 122 records to fullwidth `？？？` on one translator's report without
checking the corpus. Measuring against HEAD showed ASCII was the majority
122 to 76, it is in the documented drawable set where fullwidth `？` is not,
and it matches the ASCII preference the rules apply elsewhere. All 198 records
are now ASCII, and `work/tr/CONVENTIONS.md` records the reasoning rather than
just the rule.

**Three more splits settled from the shipped evidence:** `マリナ様` is
`Lady $$マリナ$$` (12-1, and the corpus already says Lady for the other two
princesses), `ジェミニス` is `Geminis` (33-10), and one record had dropped the
title from AG's "Master X" idiolect. Coordinates get a house form,
`N23-32, E161-22`, since the degree sign is not drawable.

**Stage 48 translated** (748 records over 6 Sonnet slices, the second-largest
script of the run): member 3 638 records, member 4 110. `check_stage.py`,
`check_names.py` clean on both.

**Tessa's rank settled: `テスタロッサ大佐` is "Captain Testarossa".** The corpus
had shipped 7 "Captain" against 6 "Colonel" for the same character -- 大佐 is
literally Colonel, but she commands the submarine Tuatha de Danaan and the
official Full Metal Panic English localisation calls her Captain. Six records
across five files now agree. A translator flagged the split rather than
picking a side and moving on.

**A token outlier restored.** `ソースケ` is the `$$宗介$$` token in about 75
records; one shipped record in stage 29 wrote a literal "Sousuke". A translator
noticed while reusing it, refused to copy it as precedent, and said so.

Five more coinages are in the settled list: `無機質な部屋` "A Featureless
Room" (three slices of this one stage split it two ways again), `タロス`
"TAROS", `艦長室` "Captain's Cabin", `フライトハッチ` "Flight Hatch",
`オーブ連合首長国` "Union of Orb Emirates", and `キミツ` "Sealed" -- the last
chosen to carry both halves of a 機密/気密 pun.

**Stage 47 translated** (459 records over 4 Sonnet slices): member 3 376
records, member 4 83. `check_stage.py`, `check_names.py` clean on both.

Slices are now asked to say explicitly when they COINED a term rather than
reusing one, because stage 46 produced three cases where two slices of the same
stage invented different English for the same Japanese and it was only caught
in passing. It worked immediately: two slices split `銀河の妖精` and
`超時空シンデレラ` four ways between them.

**The library was split on those two as well.** Sheryl's own character entry
calls her "the Galactic Fairy"; a keyword entry called her "the galaxy's
fairy" and Ranka "the super-dimensional Cinderella". Her own entry wins, and
`超時空` is "Super Dimension" by Macross convention (as in Super Dimension
Fortress Macross), so both the keyword entry and the stage text now agree.

Translators also caught their own mistakes mid-run this batch, each via the
checker rather than at merge: an ASCII `~` with no glyph (twice), an invented
`$$ＵＧ$$` token, `マリナ・イスマイル` missing its chōonpu, and `千鴥かなめ`
written with the wrong kanji.

**Stage 46 translated, both branches** (761 records over 8 Sonnet slices):
`STG0046A` 57, `STG0046B` 704. `check_stage.py`, `check_names.py` clean on all
four members. Stage 46A's two members are 57 records between them, so both went
to one translator rather than one each.

**One factual error caught at merge:** a slice rendered `第３新東京市` as "Neo
Tokyo-2". Those are two different cities -- `第２新東京市` is Neo Tokyo-2 and
`第３新東京市` is Tokyo-3, which 45 shipped records already say. Fixed.

**And the same city was shipping under two names.** `第２新東京市` uses the
glossary token in 33 records, expanding to "Neo Tokyo-2", but 9 records wrote a
literal "Tokyo-2". All 9 now use the token, so the city has one name on screen.

**Three terms split between slices of the same stage,** which is exactly what
the first-instance list exists to stop: `墓穴特訓` came out as both "grave
training" and "the Grave Pit Drill" (the drill is *named on screen* by Fudou,
so his line wins), and `Ｇの誇り` as both "G's pride" and "the pride of G".
`ミサトの部屋` split too but `tokenise_stage.py` resolved it on its own. All are
now in `work/tr/CONVENTIONS.md`, along with `墓地` "Graveyard", `アイアンシー`
"Iron-C" and `アルテア` "Altair" (never "Altea").

**Stage 45 translated** (734 records over 6 Sonnet slices): member 3 399
records, member 4 335. `check_stage.py`, `check_names.py` clean on both,
`tokenise_stage.py` found nothing to convert.

One slice split `レイ` correctly *inside a single slice*: four records as
`#333` (Rei Ayanami -- Shinji addresses her as 綾波, EVA context) and two as
`#168` (Ray -- Fire Bomber context), even though the brief's cast section
defaults every `pid_RAY_S`/`pid_RAYM` line to Ray's Macross 7 bio. That is the
bug that shipped wrong four times before `check_names.py` existed, now being
resolved per record from the scene.

More first-instance renderings settled in `work/tr/CONVENTIONS.md` so later
stages match rather than re-decide: `ナナヒカリ` "Daddy's Boy", `エコヒイキ`
"Teacher's Pet", `愛・おぼえていますか` "Do You Remember Love", `運命の赤い糸`
"fate's red thread", and the rule that a `『 』` title becomes `'...'` because
corner brackets are not in the drawable glyph set.

**Stage 44 translated, both branches** (514 records over 5 Sonnet slices):
`STG0044A` 193, `STG0044B` 321. `check_stage.py` and `check_names.py` clean on
all four members, `tokenise_stage.py` found nothing to convert. Stage 44
replays stage 38's Gura/Duncan confrontation and stage 35/37's hangar scene,
so most records were reused by sha.

**`tools/terms.py list` could not find a fullwidth term.** `list ＡＧ`
reported "0 of 1141 terms" for a term that is in the glossary: the command
lowercased the search pattern before matching it against BOTH the Japanese and
the English, and `"ＡＧ".lower()` is `"ａｇ"`, which no glossary key contains.
Every fullwidth query -- `ＡＧ`, `ＷＩＬＬ`, `ＰＳ`, `ＵＮ` -- silently returned
nothing, so a translator checking whether a name was a glossary term got a
false negative and would reasonably write it plain. The Japanese is now
matched as typed and only the English is lowercased. Found by a translator,
who reported it rather than working around it.

**Stage 43 translated** (1,010 records over 9 Sonnet slices, the largest
script of the run): member 3 543 records, member 4 467. `check_stage.py`,
`check_names.py` clean on both, `tokenise_stage.py` found nothing to convert.

Most of it was already written. Stage 43 replays scenes from stages 35-37, and
the slices found exact-sha precedent for 102 of 114 records, 96 of 102, 92 of
107, 81 of 112, 69 of 114 and 61 of 69 -- reusing the shipped English rather
than retranslating it. Record identity is a sha of the Japanese, so a replayed
scene stays word-for-word consistent for free.

**Rank words reconciled.** `司令` is "Commander" (59:1) and `総司令` is
"Supreme Commander" (16:2); three outliers were corrected. `総帥` is recorded
as an open question rather than swept: it splits 13/14 between those two
renderings, so it collides with both and has no dominant form. One translator
used "the Sovereign", the official Gundam UC English rendering, which would be
collision-free -- but adopting it renames a title across ~27 shipped lines.

**Two flags checked and closed without changes.** A translator reported that a
shipped line calls an "Enhanced Human" *she* while its cast sheet says *he* --
reading the neighbouring records, the 奴 who "pulled back" is Marida, the
four-winged Enhanced Human, not Gyunei, and the *it* that found another Newtype
is the NT-D. The line is right as written. `マーティアル教団` was rendered
"cult" once against "Order" three times, and the outlier now matches.

**Stages 41 and 42 translated** (1,180 records over 10 Sonnet slices):
`STG0041` 478 across three members, `STG0042` 521 (its 2-record member 2 was
folded into another slice's agent rather than given a translator of its own).
`check_stage.py` and `check_names.py` clean on all five members, and
`tokenise_stage.py` found nothing to convert.

Reuse is now carrying a large share of the work: 80 of one slice's 114
records, 74 of another's 119 and 38 of a third's 42 already had exact-sha
precedent in earlier stages, so they took the shipped English unchanged.
Record identity is a sha of the Japanese, so a scene reused across route
branches stays word-for-word consistent at no cost.

**Recorded, not swept: `様` is rendered inconsistently.** It comes out as
"Master X" 100+ times including for women (`Master $$オードリー$$` x9,
`Master $$カレン$$` x6, `Master $$Ｃ．Ｃ．$$` x7) and as "Lady X"/"Miss X"
elsewhere (`Lady $$ミネバ$$` x7, `Lady $$マリーメイア$$` x4) -- and Audrey and
Mineva are the same character, so the corpus calls one person both. A
translator flagged it rather than picking a side. Settling it means changing
~40 shipped lines on a judgement about whether the gender-neutral `様` should
render gender-neutrally, which is the user's call, not mine.
`work/tr/CONVENTIONS.md` now tells slices to match whatever that specific
character already has and never to introduce a gendered title.

**Four shipped records called Rei Ayanami "Ray", and there is now a check for
it.** `レイ` is both Rei Ayanami and Macross 7's Ray Lovelock, and the brief's
auto-generated cast section attaches Ray's bio to every `pid_RAY`/`pid_RAY_S`
line -- Rei's included. A wrong discriminator is invisible to
`check_stage.py`: the token resolves, expands and measures fine, and is only
wrong on screen. `tools/check_names.py` reads each `レイ` reference together
with its neighbouring records and flags one whose scene names the other
character. It found all four: stage 29's Bonta-kun gag (2 records), stage 31B's
"Shinji, Rei, Aquarion...", stage 39's "fighting Angels is my duty... I'll
fight alongside Ikari", and stage 40's, where the line before introduces her
as "one more EVA pilot" and the record itself is a bare `「………」` carrying no
evidence at all. All four now say Rei. A translator working stage 41 spotted
the stage 39 one and flagged it rather than copying it as precedent.

**Location captions normalised** (32 records in 6 files): 26 shipped captions
join a place and a room with a plain space (`$$ネェル・アーガマ$$ Hangar`) and 6
used a comma. The comma ones now match: `$$ラー・カイラム$$ Bridge`,
`$$ドラゴンズハイヴ$$ Command Room` and `Salon`, `Tokyo-3 City Streets`,
`NERV Corridor`. `第３新東京市　夕方` keeps its comma -- 夕方 is a time of day,
not a room, and "Tokyo-3, Evening" is the better English.

**Stage 40 translated** (407 records over 4 Sonnet slices), `check_stage.py`
clean on both members, nothing to correct at merge, and `tokenise_stage.py`
found nothing to convert -- the slices wrote every glossary reference as a
token themselves.

18 of one slice's 61 records and 22 of another's 78 had already shipped
verbatim under the same sha in earlier stages, and both reused the existing
English unchanged rather than re-translating. Record identity is a sha of the
Japanese, so a line repeated across stages stays word-for-word consistent for
free.

**Stage 39 translated** (561 records over 5 Sonnet slices), `check_stage.py`
clean on both members, nothing to correct at merge.

Two slices reached `ソウセイの書` independently, with no glossary entry and no
shipped precedent, and both chose "Book of Genesis". One of them flagged the
risk explicitly -- the phrase recurs in stages 41, 45 and 83, so a later slice
deciding differently would need reconciling. `work/tr/CONVENTIONS.md` now
carries a "first-instance renderings" list for exactly this class of name, so
the decision is made once rather than re-made per stage.

`レイ` was resolved correctly in both directions again, and in the harder
direction from scene evidence alone: one slice had the brief's cast section
AND the `pid_RAY_S` portrait both pointing at Ray Lovelock, and still read Rei
Ayanami off the scene (she pilots Unit-00 and is taunted for favouritism).

**Stage 37 translated** (535 records over 4 Sonnet slices), `check_stage.py`
clean on both members, nothing to correct at merge. One slice met the `ゼロ`
trap in its hardest form -- Heero saying he was once controlled by `ゼロ`,
meaning Gundam Wing's ZERO System and not Lelouch -- and wrote plain "Zero"
unprompted, the same call that needed three manual fixes back in stage 32.

**Stage 38 translated** (546 records over 5 Sonnet slices), `check_stage.py`
clean on both members, nothing to correct at merge.

Stage 38 was also the run's first real test of surviving a usage limit: all
five of its slices were killed by a rate limit before any of them had written
a byte. Nothing finished was lost -- the 40 committed story scripts and stage
37's three completed slices were all on disk -- but the five had to be redone
from scratch, so every slice prompt now says to write its answer file after
the first ~20 records rather than the first ~30. Every one of the five losses
was an agent killed before its first checkpoint.

The `レイ` discriminator is now being applied in both directions rather than
defaulted: one slice used `#168` (Ray Lovelock) and `#333` (Rei Ayanami) in
the same member, resolving each by portrait id plus scene content. The terms
check caught two Unicode typos a translator made in its own tokens -- 桜 for
桂, and a halfwidth ｲ for ｒ in `グーラ・キング・Ｊｒ．` -- before either
could reach a merge.

**Stage 36 translated** (456 records over 4 Sonnet slices), `check_stage.py`
clean on both members, nothing to correct at merge. Both slices that met
Unicorn's `姫様` wrote plain "Princess" on their own, and one worked out the
banner conventions from the shipped corpus rather than inventing them
(`Xの部屋` is `X's Room`, `X内` is `Inside X`, a contiguous `X格納庫` is
`X Hangar` while a space-separated one takes a comma).

**Stage 35 translated** (477 records over 5 Sonnet slices), `check_stage.py`
clean on both members. One correction at merge, from a translator's own flag:
Quess introduces herself as `クェス・エア`, not the glossary's
`クェス・パラヤ`. That is not a typo -- she uses her mother's surname after
her parents' divorce -- so the line keeps the divergent surname and reads
`$$クェス$$ Air`, the standard English form, rather than substituting the
established "Paraya" token over what the source actually says.

The traps file kept paying: レイ was correctly read as Rei Ayanami over the
brief's `pid_RAY` cast bio, Unicorn's `姫様` stayed plain "Princess", and a
translator invented `$$ハサ$$` for Katz's nickname for Hathaway and had it
rejected by the checker's terms pass before it could reach a merge.

**Stage 34 translated** (415 records over 4 Sonnet slices), `check_stage.py`
clean on both members. Nothing needed correcting at merge: a translator hit
the `姫` trap itself -- Katz teasing Audrey as `お姫様` in a Unicorn scene,
with the brief's own glossary table offering the token -- and wrote plain
"princess" because `work/tr/CONVENTIONS.md` says Unicorn's 姫 is not the
SRW-original keyword. The traps file is now catching these before merge
rather than after.

**Stage 33 translated, both branches** (731 records over 6 Sonnet slices):
`STG0033A` 276, `STG0033B` 455. `check_stage.py` clean on all four members.
Stage 33A's two corrections at merge: the `ゼロシステム` Wufei
tells Heero to see the future with is Wing Gundam Zero's ZERO System, so it
is plain `Zero System` and not `$$ゼロ$$` (Lelouch); and Kallen's `天子様`
is the Tianzi, Code Geass R2's Chinese Federation Empress, rendered "the
Tianzi" rather than the translator's neutral "the heir" -- it has no glossary
entry, and the translator flagged it rather than guessing, which is the
behaviour the brief asks for.

**Stage 32 translated** (851 records over 8 Sonnet slices): `STG0032`
member 3 584, member 4 267. `check_stage.py` clean on both.

Three records said `$$ゼロ$$` where the line means Wing Gundam Zero, not
Lelouch -- Wufei telling Heero to board it, and the ZERO System showing him
the future. Those are plain `Zero` now. The translator had cited a shipped
line as precedent, but that line was one of the four wrong-term tokens
corrected earlier today, so the precedent no longer existed. Every name trap
of this kind is now written down in `work/tr/CONVENTIONS.md` (レイ, ゼロ, 姫,
レディ, ボス, and the short names that genuinely ARE terms), and slices are
briefed to follow the conventions over a shipped line when the two disagree.

**Stage 31 translated, both branches of the route split** (874 records over
9 Sonnet slices): `STG0031A` 130, `STG0031B` 744. `check_stage.py` clean on
all four members. This is the first stage of the run to finish every
remaining script, and the pipeline is now four tools rather than four
hand-run steps: `prep_stage.py` (decrypt, unpack, count), `brief_stage.py`
(cut slices), `tokenise_stage.py` (normalise onto glossary tokens) and
`register_stage.py` (the manifest plus the three deploy tables at once).
`stage_status.py` derives progress from the disc listing, so no session has
to remember where the run stopped.

**`tools/tokenise_stage.py`** normalises a merged stage onto `$$japanese$$`
references. Unlike `tokenise.py` it matches on the term's JAPANESE occurring
in the record's own `jp`, which is far stronger evidence than matching the
English, and it refuses a term whose English is an ordinary word (Princess,
Zero, Boss, An) because there the match is not evidence at all. The round
trip is still the guarantee: a record is rewritten only when expanding the
new text reproduces the old English exactly. It earned its place immediately
-- two of stage 31B's slices wrote plain English to satisfy the checker bug
below, and it put 259 records back on tokens with the shipped text unmoved.

**`tools/export_stage.py`'s brief contradicted itself** and two translators
reported it. Rule 7 said to write glossary terms as tokens and then that
"speaker names stay plain English", and the worked JSON example showed a
plain `"Shinn"`. Every shipped stage tokenises the speaker line. The rule and
the example now agree.

**`tools/check_stage.py` also accepts a merged translation module,** not only
a translator's raw `{sha: english}` answer, so the file that actually ships
is the file that gets checked.

**`tools/check_stage.py` now expands `$$japanese$$` glossary references before
checking charset and width.** It previously checked the raw token text, so
any line using a glossary term (per `work/tr/CONVENTIONS.md`) failed with
`no glyph for '$'` -- `$` itself is never in the drawable set. The build
(`tools/build_project.py` via `tools/trdata.py`) already expands references
before anything reaches the screen; the checker now loads
`analysis/glossary.json` the same way and checks the expanded English, so
what it measures is what will actually be drawn. An unresolvable reference
(ambiguous or unknown term, or no glossary file to expand against) is now its
own `terms` problem instead of a misleading `charset` one. Re-checked two
already-shipped, build-verified translations against their `.lua` members to
confirm the fix: `translation/stage0020_04.json` (161 answers, several
glossary terms including `$$第５の使徒$$`) went from 154 `charset` problems
to 0, and `translation/stage0001b_03.json` (102 answers, no glossary terms)
stayed clean at 0 either way.

## 0.6.1 -- 2026-09-10

Stages 1–30 and 26 intermissions, all pending UI/terrain fixes, and complete
source coverage for 504 mission/effect/unlock/reward variants across 58
archives. Independently reviewed 84 victory, 116 defeat and 78 SR entries;
all thresholds, ordering and gameplay logic are unchanged. All 78 terrain
names across 64 maps are translated. Full regression passed, including
10740 PPC centering cases and 3830 binary hooks. Runtime visual QA remains
pending. Distribution consists only of xdelta patches and documentation.

Build numbering now advances one patch number per successful complete build,
starting with 0.6.1. Failed builds do not consume a number, and release
snapshots verify the build manifest and retain the assigned number.
Serpent and Kshatriya victory conditions use objective wording ("Shoot down
...") rather than defeat-event wording.

**Stages 11-30 converted to `$$japanese$$` glossary tokens** (10,504 records
in 83 files). Every record whose Japanese names a glossary term now
references it by token instead of spelling the English out: the audit that
opened at 14,049 literal references closes at 23, all of them deliberate
(below). Conversion was mechanical and its safety property is the same one
`tools/tokenise.py` uses -- a record is rewritten only when expanding the new
text reproduces the old character for character -- so nothing on screen
moved. Proved three ways: 13,709 records compared against `HEAD` with *both*
sides expanded (0 differ), `terms.py check` clean on 23,846 references, and a
full build.

Two guards in the first pass had to be lifted to finish, each after reading
every occurrence rather than trusting the count. A term whose English is
under three characters was refused outright, which left `AG` (399 records),
`PS` (40), `Fa` (21), `UN` and `An`; matching on the *Japanese* present in the
record makes those unambiguous, and all 461 were genuine references. A
Japanese naming two terms was refused as ambiguous, which left the five names
a pilot shares with the machine or the keyword: `ボン太くん` and
`ブラックオックス` take `#pilot` on the speaker line and `#robot` in prose,
`宇宙魔王` and `マーグ` are `#pilot` throughout (both are spoken of as people),
and `オルソン` is `#50`, the id the library entry for Kei already used.

**Four tokens named the wrong term and are now literal English again.** The
Japanese matching is not proof the term is meant: `姫` is the SRW-original
keyword for the Firebug's Princess, not Unicorn's `姫様` (Mineva) nor Klan's
`『姫』` -- 21 records; `ゼロ` is Lelouch, not Duo's "your Zero" (Wing Gundam
Zero); `レディ` is Lady Une, not "a pout doesn't suit a Lady"; and `ボス` is
the Mazinger pilot, not Michel's `マオ姐さん` -- rendering 姐さん as "Boss"
is the settled convention and the English is right; the token linking it to
the pilot was not, and had been committed in an earlier batch. Reverting
each restores the literal that was already on screen. The reverse also happened once: the last `President` became
`$$大統領$$`, matching the 39 other references to the same character.

`translation/vi` is deliberately untouched -- Vietnamese prose should
reference Vietnamese terms and the glossary has no `vi` field, as
`docs/TRANSLATING.md` already records. Earlier corrections from this batch
that had not been committed are folded in: "Mechanical Angel" and "Fold Wave"
capitalised in four library entries, `Fumoffu` in voice section 147.

**Stages 26-30 translated** (3,177 records over 33 Sonnet subagent slices):
`STG0026` 493, `STG0027` 986, `STG0028` 647, `STG0029` 590, `STG0030` 461.
`check_stage.py` clean on all 12 members; zero blank, dashed, wave-dash or
all-caps records at merge. Concurrency was three agents until the last
seven slices, which ran together.

**The `$$japanese$$` glossary-token rule is restored and recorded.**
`tools/terms.py` expands a term reference at build time so renaming a term
updates every line, and `#` discriminators separate two terms sharing one
Japanese string (`$$レイ#333$$` is Rei Ayanami, not Ray Lovelock). Stages
1-10 use it; stages 11-30 drifted to literal English purely because the
rule had fallen out of `export_stage.py`'s brief template. It is back as
brief rule 7 and is now a rule in `CLAUDE.md`. The literal-English drift
in stages 11-30 was estimated here at 8,807 records; the conversion that
followed (entry above) rewrote 10,504.

**Corrections made while merging this batch**, several reaching shipped
text: 機械天使 and フォールド波 capitalised project-wide ("Mechanical
Angel", "Fold Wave", 12 files including three library entries) after I
wrongly passed a slice's lowercase claim forward without checking the
counts; ふもっふ standardised on the official spinoff spelling "Fumoffu"
(4 files); Zechs's 火消しの風 restored to the settled "the wind that
smothers fires"; ＦＢ隊員 and 習志野基地隊員 restored to the shipped
"Firebug Trooper" / "Narashino Base Trooper" (8 records). One
wrong-character bug caught before shipping: a slice rendered レイ as
Macross 7's Ray in a scene where Kaname addresses her with a child's
diminutive and she asks after Bonta-kun, which is Rei Ayanami's running
gag from stage 28. A bare 「………」 hashes identically for every speaker, so
the surrounding dialogue is the only evidence.

**Stages 20-25 translated** (3,260 records over 35 Sonnet subagent slices,
three at a time): `STG0020` 422, `STG0021` 456, `STG0022` 397, `STG0023`
412, `STG0024` 473, `STG0025` 1,100 (its member 3 alone is 966 records,
eight slices). `check_stage.py` clean on all 13 members; zero blank,
dashed or bracket-mismatched records at merge. The agents worked from one
shared conventions file that grew as terms were settled, so later slices
inherited decisions instead of re-making them.

**Two build bugs found by this batch and fixed:**
`tools/patch_lua.py` keyed every record by `(event, n)`, but a member of
bare labels (STG0021 member 2, two team names) has both None on every
record, so the whole member collapsed onto one dict entry and each stamp
was checked against the wrong record -- reported as "the japanese changed
since this line was translated" on a correct translation. Unstamped
records now bind by position, still asserting their sha.
`tools/cpkpatch.py` (from the previous batch) grows a member past 64 KB
into a rebuilt CpkItocH.

**Terminology reconciled project-wide,** correcting text shipped earlier:
アンノウン is capitalised "Unknown(s)"; 次元震 "dimensional tremor";
葛城二佐 "Lt. Col. Katsuragi"; クエント "Quent" (not "Kuent"); ウルズ
"Urzu" (21 records across six files, including stages 4, 9 and 11);
ア・コバ "Ah Koba"; バトリング "Battling" (capitalised, per the game's own
keyword dictionary, which also corrected a library entry); キリコ
"Chirico" (nine records said "Kirico"); Ｄトレーダー背景 "D-Trader
Backdrop" (84 records in 28 files); 魔王 is "Demon King" for the
Getter/Gishin villain but "Demon Emperor" for Lelouch. **18 wave-dash
characters (U+301C) were replaced with the fullwidth tilde (U+FF5E)**
across six files including two voice lines: they look identical in a
report but only the fullwidth form has a glyph.

**Stages 18 and 19 translated** (1,083 records: `STG0018` members 3 and 4,
343 + 248; `STG0019` members 3 and 4, 349 + 143). Ten Sonnet subagent
slices, three at a time; `check_stage.py` clean on all four members and
zero blank, dashed or all-caps records at merge.

**`cpkpatch` can now grow a member past 64 KB in an archive whose
CpkItocH is empty.** Stage 19's English member 3 outgrew the 16-bit size
columns of CpkItocL, and moving the row failed with "id 3 has no ITOC
entry". Two faults: `_rows_edit` left `row_len` at 0 when the target table
had never held a row, and STG0019's CpkItocH is a placeholder whose column
schema is unusable (ID flagged STORAGE_ZERO, the other two columns all
zero bytes). The mover now rebuilds a correct CpkItocH from scratch when
the shipped one cannot take a row, matching the schema the populated
archives use. Verified by packing a deliberately oversized member and
reading every member of the result back byte-identical.

**Terminology reconciled project-wide** while merging these stages, which
corrects text shipped earlier: the Evangelion cities now use the canonical
English (第３新東京市 "Tokyo-3", 第２新東京市 "Tokyo-2"; four earlier lines
said "Neo Tokyo-2"), クラッシャー隊 is "Crusher Team" everywhere (11
earlier records said "Crusher Squad"), and 機械獣 is "Mechanical Beast"
(two voice lines said "Machine Beast"). `export_stage.py`'s brief template
told translators "No em dash; use `--`", which contradicted the settled
no-dash rule and is now corrected at the source.

**Stages 16 and 17 translated** (954 records: `STG0016` members 3 and 4,
354 + 214; `STG0017` members 3 and 4, 245 + 141). Nine Sonnet subagent
slices, run three at a time, briefed with the conventions settled earlier
so nothing needed a casing or dash pass afterwards: `check_stage.py` clean
on all four members, and zero blank, dashed or all-caps records at merge.
Renderings chosen: 白き流星 "White Meteor" (kept distinct from Char's
"Red Comet"), the Preventer codenames Wind and Lightning, ルリルリ
"Ruu-Ruu", the アンマン running joke as "Steamed Bun" / "Team Steamed
Bun", 生首ハクション initially as "Achoo Count" with the pun explained in the
following line (replaced in unbuilt source on 2026-09-19 by "Count Me-Out"
because the count/sneeze wordplay was lost in English), and this stage's 魔王 as "Demon King", deliberately not
merged with the Getter villain already shipped as "Space Demon King".
Registered in `manifest.py`, `deploy.py`, `extract.py`, `apply_xdelta.py`.
Stages 1-17 ship.

**The intermission scenes are translated (26 scripts, 1,281 records).** A
player screenshot showed Japanese in the Macross Quarter hangar and in a
route-branch choice, which turned out not to be a gap inside stages 1-15
at all: the between-stage scenes live in their own 0200-series of stage
scripts that the project had never extracted. STG0200 through STG0272 are
now decrypted, extracted to `work/lua02xx`, translated (Codex drafts,
`check_stage.py` clean on every file), and registered in `manifest.py`,
`deploy.py`, `extract.py` and `apply_xdelta.py`. Eight are the large
hangar conversations (61-189 records); the rest are the branch scenes the
flow chart calls the hiking split (stage 5-6) and the pervert-chase split
(stage 9), 11-20 records each. Post-merge passes: 13 shas appear in more
than one file and were made to read identically, preferring the
normal-case rendering, and six ＡＧ lines that came back in all capitals
were recased (the brief now carries that rule). No double dashes.

Still untranslated in the same family, not started: STG0500 (1,247
records, D-Trader shop and reward scenes), STG0700 (872, unit banter) and
STG0600 (236, the tutorial). The 0900-series is developer test material
and is deliberately skipped.

**All terrain labels (prepared; not deployed).** Audit all 64 available maps,
covering 552 records and 78 distinct labels. Add 73 terrain-only translations
with live-width centering, including later maps and spelling variants.
Preserve non-terrain name lookups, terrain bonuses and tile grids. The full
candidate now includes 64 text-only map copies and must be deployed together.
Includes all prior pending fixes. See docs/TERRAIN_AUDIT.md.

**Source-driven message-class audit (prepared; not deployed).** Cover missing
mission conditions through locally extracted Stage 15, all 17 completed
D-Trader unlock notices, all 42 shop requirement variants, weapon effects
and reward-report labels. Add 154 lookup entries and translate the shared
Ace Bonus/part-reward formats without changing inserted values. New coverage
checks compare against original source tables, not just registered hooks.
Includes all previous pending fixes. See docs/MESSAGE_CLASS_AUDIT.md for scope.

**Hibiki defeat conditions (prepared; not deployed).** Translate the displayed
Hibiki name variant in Episodes 4 and 5 as "Hibiki is shot down.", preserving
the numbered entries. Retain the original name variants and all gameplay
conditions. Includes all earlier pending fixes.

**D-Trader unlock notices (prepared; not deployed).** Translate the completed
Stage 4 and ally-HP-at-20%-or-below conditions. Use "Now at D-Trader: [item]."
September 26 correction: the fixed18-byte native copy truncated that English
prefix. It now uses the byte-safe "Unlocked [item]." form; all21 condition
reports and all four upgrade-system names are covered, not just these two.
for the shared availability notice, preserving the inserted item name and
all unlock requirements. Includes all earlier pending fixes.

**Battle/report translations (prepared; not deployed).** Translate the small
Maximum Break and Mobility battle word sprites, all four Tag Command help
descriptions, repair-cost titles/Cost/Funds and the President PP report.
Preserve the variable PP bonus, costs, down-arrow and all gameplay behavior.
Includes the earlier pending Effect and UI fixes.

**Weapon Effect labels (prepared; not deployed).** Translate 運動性▼ as
Mobility Down and バリア貫通 as Barrier Pierce in the Effect panel. Display
text only; weapon stats and effect mechanics are unchanged. Includes the
previous pending nine-screenshot UI follow-up.

**Nine-screenshot UI follow-up (prepared; not deployed).** Translate Cliff,
Upgrades, Record Library and the intermission stage footer. Use live-width
centering for Library/PS Store labels; shorten Teams, Auto-Update, Search
Setup and AT/DF; use MV in the Team Setup footer. Preserve terrain bonuses,
dynamic numbers, selection state and artwork. In-game confirmation pending.
Correction (2026-09-11): the Library-specific spacer/centered-mode change
was reverted after the user reported five blank buttons. Library titles now
use plain English and their original special text mode; PS Store is unchanged.

**2026-09-08 local deployment:** Installed the combined out_tag_reward_20260908_v2
bundle, including all fixes marked prepared below. All 28 file hashes verified;
eight save files unchanged. Previous changed files and stale install cache
are recoverably backed up. In-game visual confirmation remains pending.

**Tag Command, Maximum Break, reward alignment and Weapons (prepared; not deployed).**
Translate the four Tag Commands and Z Chips caption. Replace the gold
Maximum Break banner and small red badge while preserving animation and
other battle artwork. Center both SR Point reward lines by actual English
width, and shorten Weapon Select to Weapons to fit its header. Full checks
passed; texture previews reviewed. In-game confirmation remains pending.
The combined _v2 bundle adds DATA/BTLC/CMN.CPK (28 game files total).

**Map-hover popup overlaps (prepared; not deployed).**
Use MV in the narrow movement field, smaller S.Atk / S.Def without trailing
periods in support boxes, and HP/EN Rec: for recovery percentages. Keep all
values, unknown markers, positions, selection colors and row spacing intact.

**Team roster (prepared; not deployed).**
Translate Team Bonus / Max Break and fit S. Atk / S. Def into narrow columns.
Separate the Ally/Enemy roster-title colon and suffix from the title, and
move the footer value block clear of Move. Preserve values and question marks.

**Naming and search setup (prepared; not deployed).**
Translate naming methods, automatic-name-update options and confirmations,
search setup headings, empty-filter labels, and controller hints. Fit the
English descriptions to their panels and center the three filter variants.
Preserve naming behavior, custom names, search state, and earlier fixes.

**Intermission menu translations (prepared; not deployed).**
Translate Pilot List / Power Parts headers, Options and Network popups,
Library buttons and descriptions, Team Setup's split title and support
commands, and the remaining settings labels in the reported variants.
Center popup labels within their buttons; preserve counters and button icons.
Includes all earlier pending fixes. In-game visual verification is pending.

**Map terrain names (prepared; not deployed).**
Translate Paved Road, Flatland, Building and Construction Site wherever those
exact terrain names appear. Center English between the MAP-DATA arrows.
Do not modify map attributes, terrain bonuses or the pending earlier fixes.

**Roster and settings overlap (prepared; not deployed).**
Shorten roster column headings to S. Atk / S. Def and center them above their
counters. Shorten and center Settings 1 / Settings 2 tabs in every state.
Apply live-width centering to 28 settings descriptions to prevent clipping.
Includes pending backlog fix. Full regression suite passed: 5160 centering
cases; all other game files and image assets preserved.

**Backlog R1 spacing (prepared; deployment deferred by user).**
Narrow the plus sign and adjust surrounding spacing on both Prev/Next quote
help rows to clear the R1 icon, retaining the Fast suffix position. No control
bindings or icons changed. Installed game remains unchanged.

**Narration alignment (deployed; awaiting in-game check).**
Rebalance line breaks on the two reported narration pages and an earlier
overlong poem line. Preserve every word, existing rows and page boundaries;
keep consistent left alignment. All 18 lines now checked against narration
screen margins instead of the wider library budget. Only EBOOT changed;
all other 26 files and earlier fixes preserved. Full regression suite passed.

**Battle-preview overflow (deployed; awaiting in-game check).**
Use Atk. in the narrow action boxes, Rnd. before the ammo colon, and S. Atk
before the support-use counter. Center all four Start Battle button variants
using live English width. Preserve counters, existing translations and image
assets. Full regression suite passed; only EBOOT and AID changed.

**D-Trader, rewards and battle labels (deployed; awaiting in-game check).**
Translate Buy/Sell, shop headings, prices, stats, categories and Maximum Break
unlock text. Translate AG's Z Chip bonus report, Bonus Rewards and Special
Investigator. Replace Intermission and Center/Wide/Support Attack image labels;
change the battle selector's attack kanji to AT. Translate the Intermission
episode-clear footer. Keep locked items as question marks. Existing alignment
fixes and unrelated game data preserved; full regression suite passed.

**Remaining commands and dialogs (deployed; awaiting visual verification).**
Center Attack, Air, Max Break, Tag Command, Parts and the other remaining unit
commands. Center the End Phase prompt/count and Quick Save heading,
instruction and all three choices using actual English width. Shorten Auto
Transform to Auto Trans. for button fit. Preserve working Spirit-grid, Yes/No
and Ally/Enemy fixes. 3000 centering cases and the full regression suite passed;
only EBOOT changed, all other 26 game files unchanged.

**COMMAND submenus (deployed; awaiting visual verification).** Center Move,
Ground, Transform, Change Main, Spirit and Status. Realign both Ally/Enemy
selection states, including the slash, font size and baseline, while retaining
their colors and selection behavior. Main-menu and Spirit-grid fixes preserved;
1020 command-layout cases and the full regression suite passed.

**Map COMMAND alignment (deployed; awaiting in-game verification).** Center End Phase,
Search, Unit List, Objectives, Battle Report, System and Quick Save using
live font pitch/quad width instead of estimated padding. Move the Funds
colon to the Z Chips colon's x coordinate. The user-confirmed Spirit-grid
helper is unchanged. 420 emitted-PPC cases and the full regression suite
pass; an in-game check is still required.

**Search screen alignment.** Spirit names now center using their translated
glyph widths instead of the original full-width Japanese character count,
addressing long names such as Intuition extending outside their column.
Search tabs use Spirit / Skills / Abilities, fitted to their buttons.
The change is limited to this screen's templates; hidden entries and unrelated
widgets keep their original positioning. Automated checks passed and the build
is deployed; in-game verification remains pending.
The first grid revision failed visual QA because colored entries draw from a
stack-copied template, which its address filter missed. The revision recognizes
that specific grid caller and template references. Regression tests reproduce
the old failure and cover 1,060 copied-template cases. All translations and
archive files remain byte-identical; the revised grid still needs in-game QA.

**Confirmation dialogs (#8, #21, #31).** Fixed spacing between the inactive
Yes/No row and its separately drawn highlighted choice. The initial fixed
spacers failed visual QA; revised live-pitch tabs no longer assume glyph
width equals character spacing. Preserved original button/highlight positions. Spirit
exit confirmation now translates after the game's fixed-size string copy,
preventing the clipped warning and square glyph. Automated checks passed;
in-game verification remains pending. Existing translations preserved.

**Battle-screen labels the hook was missing, and a COMMAND menu overflow.**
The draw-time hook matches a whole drawn string, so a label the game draws
as one multi-line block never matched its single-line entry: 攻撃力 was
registered as "Power" but is drawn as the two-line `ＥＮ
攻撃力`, which
now has its own entry. Added with it: 再攻撃 "Re-Attack", 再攻撃：,
武器選択 "Weapon Select", ・武器選択
・参加しない, 援護設定・なし
"Support: None", 攻撃力
装甲値
運動性, 最大攻撃力 "Max Power", and
高性能ＡＩ "Advanced AI" (hooked as well as swapped in RPW, so the unit
popup gets it whichever path draws it). The per-line registration the
loader does only covers lines of six characters or more, which is why the
short labels needed exact entries. In the COMMAND menu the ally and enemy
rows are drawn side by side and "Ally List / Enemy List" ran off the
button, so they are now "Ally" and "Enemy".

**Generic enemy nameplates in English.** The battle nameplate draws its
pilot name from RPW_DATA, and 83 anonymous names covering 530 name slots
had no English at all, so an enemy showed as 高性能ＡＩ. New
`translation/enemy_names.json` (Codex draft, structurally proofread; two
corrections: ヨウヘイ was "Yousuke" and is Yohei, ダ・モンテ＝ウェルズ
capitalised for standalone use) feeds the RPW swap at the same lowest
precedence as the name pieces, so a glossary character always wins.
Covers ネオ・ジオン兵 "Neo Zeon Soldier", テロリスト "Terrorist", 市民
"Citizen", 高性能ＡＩ "Advanced AI" and the rest. All 18 slots of the AI
name verified repointed off the Japanese string; on-screen check pending.
The センター攻撃 button in the same screenshot is a texture, not text (the
string occurs in no game file), so it stays with the texture backlog.

**No more double dashes in dialogue, and two mistranslations fixed.** The
` -- ` the earlier stages used as an em dash is gone from all 192 stage
lines and the one voice line that had it, replaced by a comma, a full stop
or an ellipsis as the sentence wanted. Two lines were wrong, both caught
from screenshots: Mao's 爪のアカを煎じて飲ませてやりたい was translated
literally ("boil down his fingernail dirt and make some perv and silent
type drink it") and is an idiom, now "A certain perv and a certain
stone-face could learn a thing or two from him"; and Mao's own
マオ姐さん read "Boss Mao" in her own mouth, now "big sis Mao" (the
"Boss" rendering stays for other people addressing her).

**The whole battle-voice track is retranslated without budgets.** All 211
sections, 31,666 lines, drafted by Codex and merged; every section came
back `0 problems` from `check_voice.py` and needed no structural fix.
SRVC.BIN grows from 2,192,672 to 3,032,384 bytes (206 of 276 blocks
larger), which the EBOOT block table absorbs. Only the nine developer
placeholder lines ("silence, not shown in the real game") and section
209's four two-cell attack names stay Japanese, as before. No line exceeds
the 36-cell display cap; 1,229 lines sit in the 36-cell band, so that cap
still wants confirming on screen.

**Voice retranslation without budgets, Codex drafts.** Sections are
re-briefed by `export_voice.py` (no budget; 36-cell display cap), drafted
by Codex CLI (`gpt-5.6-sol`, high reasoning, ~50k tokens a section), run
through `check_voice.py` by Codex itself, then a structural pass
(glossary `$$id$$` tokens to English, stray newlines, corner brackets,
unicode punctuation; scratchpad `proof_voice.py`) and `merge_voice.py`.
Done so far: 4 (Lancelot Albion), 13 (Eva Unit-02), 20 (Nu Gundam), 28
(Gundam Harute); 134 (Genion) was done by a Claude agent earlier. Every
draft came back 0 problems with no structural fixes needed. Batches of
six run in parallel; the remaining sections follow in section order.

**Update patch between releases.** `tools/iso_patch.py --prev VERSION`
also encodes `SRW-Z3-English-<prev>-to-<version>.iso.xdelta` from
`work/patched_<prev>.iso`, so a player on the previous release updates
their patched image without the original disc image. Shipped for 0.6.0
(0.5.0 -> 0.6.0, 116 MB, decode-verified to the 0.6.0 image's MD5) and
documented in `docs/INSTALL.md`.

## 0.6.0 -- 2026-09-07

Five more story stages (11-15, 2,200 dialogue records) and the end of the
battle-voice length limit: the game's block table for SRVC.BIN was found in
the executable, so voice lines are now rebuilt at any length, and Genion's
set is the first retranslated in full. Also the other session's UI batch:
episode title and date cards, map captions (new `EFFPS3.CPK`), and UI
regression fixes. 27 files ship.

**Stages 14 and 15 translated.** `STG0014.SDAT` members 2 (caption
シン＆バナージ "Shinn & Banagher"), 3 (470 records) and 4 (165);
`STG0015.SDAT` members 3 (299) and 4 (166). Eleven Sonnet subagents on
`export_stage.py` briefs of 82-118 records, merged by sha, `check_stage.py`
clean on every member. Post-merge fixes: AG's seven stage-15 lines were
delivered in all caps (the agent misread the "normal case after stage 1"
note) and were recased by hand; メガラニカ "Megaranika" -> the official
"Magallanica"; ネェル・アーガマ　通信室 "Comm Room" -> "Communications
Room" to match stage 15; three stage-14 banners joined with ` -- ` -> the
comma form (`～ Vist Mansion, Hidden Passage ～`). Renderings chosen:
ビスト財団 "Vist Foundation", ジオン・ダイクン "Zeon Zum Deikun", 医務室
"Nahel Argama Infirmary", ハサン先生 "Doctor Hasan", 暗礁 "the debris
field", 好きな背景 "Favorite Backdrop" (backdrop label, unverified), 閣下 to
Haman "Your Excellency", 参謀次官 "Deputy Chief of Staff". Registered in
`manifest.py`, `deploy.py`, `extract.py`, `apply_xdelta.py`. Stages 1-15
ship.

**Stages 12 and 13 translated.** `STG0012.SDAT` members 3 (395 records)
and 4 (134); `STG0013.SDAT` members 2 (one caption, 刹那＆ヒイロ "Setsuna &
Heero"), 3 (173) and 4 (96). Seven Sonnet subagents on `export_stage.py`
briefs of 83-134 records, merged by sha, `check_stage.py` clean on every
member. Post-merge fixes: 14 shas answered by two slices (first kept);
stage 13's hangar banner aligned to stage 11's `～ Nahel Argama Hangar ～`;
`Sis Mao` -> `Boss Mao` (姐さん is "Boss" project-wide); two thought lines
that had gained 「」 around their （） restored to bare （）; seven bare
「………」 lines normalised to the nine-dot form the shipped stages use (174
to 14). Stage 12 reuses 57 of stage 11's member-4 lines verbatim (same
sha), carried over unchanged. Renderings chosen: 硝子山高校 "Garasuyama
High School", ＦＢ隊員 "Firebug Trooper", 議会 backdrop "Assembly Hall"
(unverified venue name), 貧乏クジ同盟 "the Short Straw Alliance",
バートン財団 "Barton Foundation", 擬似ＧＮドライヴ "pseudo-GN Drive".
Registered in `manifest.py`, `deploy.py`, `extract.py`, `apply_xdelta.py`.
Stages 1-13 ship.

**Stage 11 (Episode 11) translated.** `STG0011.SDAT` members 3 (366
records) and 4 (134): decrypted with `make_npdata -d`, extracted to
`work/lua11`, briefed in four slices by `export_stage.py`, translated by
four Sonnet subagents, merged by sha (one disagreement, `Pony...` vs
`Poni...` for the Pony Man tag, first answer kept), `check_stage.py` clean
on both members. Renderings settled in the batch: 獣人 speaker tag
"Beastman", ネェル・アーガマ格納庫 "Nahel Argama Hangar", ウルズ７ "Uruz 7",
先生 for Suzune "Miss Suzune" / "Miss", 姐さん (Kurz to Mao) "Boss",
デコ助野郎 "you forehead dummy" (new coinage). `manifest.py`, `deploy.py`,
`extract.py` and `apply_xdelta.py` now list the stage. Stages 1-11 ship.

**Battle voice lines can be any length.** The game does not walk SRVC.BIN:
the executable holds a 277-entry big-endian table of block offsets at file
offset 0x830be0 and reads one unit's block per partial read (loader traced
at VA 0x11ab20 / 0x11142c / 0x114188, parser 0x111488; notes in
`work/srvc_loader_notes.md`). New `tools/srvc_blocks.py` parses the 276
blocks as the parser does and rebuilds them with grown string pools; the
pristine file round-trips byte for byte. `build_project.py` now rebuilds
SRVC.BIN block by block and writes the new table into the EBOOT in the same
run (`--eboot` required for voice). The per-line byte budgets are retired:
`check_voice.py` notes lines over a 36-cell display cap instead of failing,
`merge_voice.py` / `export_voice.py` briefs say so, and `voice_lib.py`
now only supplies section geometry. Two shift experiments without the table
(a 64-byte pad, then a grown last string) blanked every later unit's text
in-game, which is what the table explains. Section 134 (Genion, Hibiki and
Suzune) is retranslated without budgets -- all 126 lines, e.g. `Finale!` ->
`This one ends it!`, `Watch me` -> `I'll pull this off...!`; weapon
call-outs match the shipped Genion GAI spellings (Punisher, Glaive,
TS-DEMON, D-Fault). Every other section still carries its budget-clipped
lines.

**Date cards.** Translated all 77 date strings used by the shared black-screen
calendar display, including April 10 and April 15: `New Multidimensional
Century 0001 - April 10`. Original dates/calendar format and game logic are
unchanged; full rendered strings are translated at draw time. All prior 3,240
translation entries and 124 episode title cards preserved. Deployed for testing;
in-game placement verification pending.

**All episode title cards — #19 follow-up.** Added a complete 124-entry JP/EN
texture catalog covering main-route, split-route, finale, epilogue, and bonus
titles. The build renders all crisp/glow layers and fallback titles. Extended
the Episode heading to two-digit numbers and translated Final Episode and
the finale's embedded title. Existing English bonus/epilogue headers remain.
All 124 text bounds and prior-fix regression checks pass; only remaining title
textures/effect variants differ from the previous installed build. Deployed
for testing; in-game animation checks pending. This is title-card coverage,
not a claim that dialogue for all episodes has been translated.

**Public #19 — Scenario 1 title card.** Translated the baked title artwork to
`A Hope Called Taboo`, including crisp/glow layers and the effects fallback.
The normal one-digit card header uses `Episode` plus its original dynamic digit;
the prefix is widened and the number shifted to fit, without changing timing.
Other title-card variants and scenario titles are not covered by this fix.
Build checks retain the previous ALL Attack and school-caption fixes.

**Public #24 and #7 — attack heading and school location.** Target selection
now uses `ALL Attack` in place of the two Japanese heading sprites. The Japan
map's school caption now reads `Tokyo-2 — Jindai High School`; the photo and
animation are unchanged. Other location captions are outside this fix.
Both patches are reproducible texture-only edits with pixel-preservation checks.
EFFPS3.CPK joins the validated deployment set (now 22 files); the CPK writer
streams output so this larger archive builds with 32-bit Python. Previous
translations retained. Local deployment verified; in-game confirmation pending.

**Public #23 — map Support Attack badge.** Replaced the baked-in Japanese
label with `AT` on all four remaining-use tiles (1–4). Runtime tracing confirms
this particular badge reads only the attack counter; defense's separate counter
and labels are untouched. Original numeral artwork, tile dimensions and all
other map textures are retained. Included in VWF builds via
`tools/support_badge.py`, with pixel-preservation and attack-reader checks.
Deployed locally: `work/out_support_badge_20260906` to `E:/SRWZ3`; all 21
installed hashes verified. In-game verification pending; #23 remains open.

**Dialogue default names (deployed locally).** The dialogue substitution
readers now translate exact default Hibiki/Kamishiro names, including full-name
composition, without changing custom names or save data. 210 emitted-PPC tests
and full UI regression checks passed; existing translations preserved byte for
byte outside the new name-reader patch. Candidate:
`work/out_dialogue_names_20260906`. Deployed after RPCS3 exited; all 21 installed
SHA256 hashes verified, regenerable install cache cleared, saves untouched.
Public issues #10/#27/#28 have detailed comments and needs-verification labels;
they remain open. In-game verification remains pending.

**Name-field display labels (deployed locally).** Built LN for surname,
FN for given name, and Kamishiro for standalone カミシロ. Display hooks only;
editable names, saves, and unsafe internal pointers untouched. All existing
hooks and other game content preserved. Bundle: `work/out_name_fields_20260906`.
Deployed after RPCS3 exited; all 21 installed hashes verified, `_DATA` cleared,
saves untouched. On-screen review pending.

**Integrated UI rollback recovery (2026-09-06).** Complete local build restores
the larger mixed-case Spirit band and missing UI fixes while retaining all
installed translation keys and newer battle-text data/offsets. 399 additional
lookup keys; all five band copies and both font pages verified. The full build
now includes the UI-data step and regression checks automatically. Lookup
keys no longer alias movement-label bytes (fixes standalone Grd regression).
Build checksums guard against mixed-file deployment. All 21 previous game
files backed up; full bundle deployed, `_DATA` cleared, saves untouched.
Output: `work/out_integrated_20260906`. In-game visual review pending.

**Save destination regression (2026-09-06).** Restored the current map-progress
message and Hard Disk / Network / Don't Save choices to the current local
installation; added the missing "Please select a save destination." prompt.
Five hooks appended without replacing existing translations or the current
font mapping. EBOOT backed up; other 20 game files unchanged; install cache
cleared, saves preserved. Binary checks passed; in-game review pending.

**Weapon Cost follow-up (public tracker #33).** New screenshot still shows Cost.
Read-only binary check confirms built EBOOT maps `消費ＥＮ` to EN but current
installed EBOOT maps it to Cost; deployment mismatch, no new translation needed.
After RPCS3 exited, patched only the installed executable's caption slot using
its current font mapping (8 bytes changed); backed up the executable and
verified all 20 other game files unchanged. Cleared the regenerable `_DATA`
install cache, leaving saves untouched. Installed hook now resolves to EN;
both on-screen locations remain pending user verification. No release made.

**Public issue-list labels (2026-09-06).** Published Linear label badges beneath
each issue title, separate from the existing workflow status. Reads all labels
with pagination and exposes names only; empty labels stay unobtrusive. Public
checks: 43 issues, 23 labeled, existing report screenshot still loads. Version 7.

**Linear screenshot import completed (2026-09-06).** Retrieved all 37 original
report screenshots after GitHub sign-in, uploaded actual files into Linear,
verified identical bytes, and replaced pending/source-link blocks with embedded
images in each report description. Linear's normalized `(<url>)` links required
an explicit conversion to image Markdown. All 40 Linear images (37 report,
three comment) pass the image audit. No GitHub or game changes.

**GitHub-to-Linear import (2026-09-06).** All 41 GitHub reports now represented
in SRW Z3: 40 new issues, existing RET-5 reused; two test issues preserved (43
public rows). Eight source comments retain original dates; source labels and
open/closed states retained. Duplicate #8 maps to Canceled with an explanation
because no duplicate target was specified. Two comment screenshots uploaded
and byte-verified; 37 private report screenshots remain pending GitHub sign-in.
Linear rewrote image URLs without retrieving their bytes (404); broken embeds
replaced with pending notes and original source links. No GitHub mutations or
game fixes. Private checkpoint/audit tooling is in work/linear-import.

**Project issue-list page (2026-09-06).** Added a homepage listing all SRW Z3
Linear project issues with status/update date and links to a separate report
page. Queries are paginated and scoped to the configured project; detail and
image reads must match its issue list and project. No sample issues, migrations,
or Linear writes. Version 6 published; anonymous list/detail/API checks passed,
actual Linear title matched, comment/image retained, unrelated issue rejected.

**Linear comments on the public board (2026-09-06).** User approved publishing
all RET-5 comments. Added paginated read-only comment retrieval, oldest-first
text/dates and authenticated Linear screenshot proxying for comment attachments.
Author account fields and internal comment IDs are not returned publicly.
No Linear data or game files changed. Version 5 deployed successfully; anonymous
production API matched the actual comment text/date, and its PNG attachment
returned HTTP 200 (686425 bytes). Build and privacy/pagination tests passed.

**Live Linear issue-board connection (2026-09-06).** Replaced the hand-authored
sample with read-only retrieval of RET-5 using the user's supplied credential,
stored as a Sites secret. Added root `Linear_API.txt` ignore rule (not previously
tracked). Fixed issue/project scope, 60-second upstream cache, privacy filtering,
safe failure state and allowlisted Linear-image endpoint. Removed the substitute
screenshot from the site copy; current Linear report has no hosted image.
Custom dependency-free Worker replaces generated server intermediates. Build
and boundary tests pass; local API returned the real title and Backlog status.
No credential was present in any build file. Original key file remains local.
The first hosted request returned 503 despite passing locally; replaced the
dispatch Cache API dependency with a 60-second per-isolate request cache and
added non-sensitive failure diagnostics. Expired-cache boundary tests pass.
Hosted fetch compatibility was resolved by using manual (unfollowed) redirects
instead of the unsupported error mode. Version 4 deployed successfully; anonymous
API returned HTTP 200 with RET-5's actual Linear title/status and no screenshot.

**Public issue-board sample (2026-09-06).** Created an isolated Sites checkout
at `work/public-issue-board` for RET-5 / GitHub #39. Read-only report, Backlog /
no-fix status, proposed terminology, and an earlier user-supplied Japanese menu
screenshot. Excludes private URLs and Discord user IDs. No Discord link per user;
no live Linear sync or feedback automation. Static-only publication; no game files
changed. Sites project: `appgprj_6a9ccf15d0d481918083784303671c92`.
Published at https://srw-z3-issue-board.binhlt0402.chatgpt.site; anonymous page
and screenshot checks both returned HTTP 200. Handoff: `docs/PUBLIC_ISSUE_BOARD.md`.


**Verification tooling.** Added `tools/check_issue_fixes.py` to check generated
hook bytes, joined reward sources, numeric message bounds, glossary expansion
and narration widths without confusing binary checks with in-game visual QA.
The first GitHub batch was deployed with hash checks and backups of EBOOT and
Scenario 2. Other files, including battle voices, were unchanged; the install
cache was already absent. `docs/GITHUB_ISSUES.md` records ready and pending
reports, with a pointer from the handoff. Issues remain open for user review.

**GitHub #13 and part of #15 — End Phase and Back Log.** Added exact composed
End Phase messages for 0–99 remaining teams without changing the count or the
game's format strings. Added Back Log navigation labels; its dynamic player
name issue is still under investigation.

**GitHub #16/#41/#42 — reward reports.** Get Result's SR Point and 10000-fund
notices now match their duplicated highlight layers together, drawing each
notice once. Added the D-Trader opening notice and the Chimera Squad ID unlock
report. Mixed hook keys can match embedded VWF item names. Also corrected a
prefix-hook fall-through into joined matching after copying the replacement.

**GitHub #27/#38/#40 — missing condition and cramped labels.** Added the
default-name defeat condition (the previous keys incorrectly included the
internal A suffix after Hibiki). Weapon EN consumption now says EN, and the
narrow map-command Maximum Break button says Max Break; full terminology in
other screens and descriptions remains unchanged.

**GitHub #17/#25/#26 — condition headings and confirmations.** Added the
Operation End heading block and its individually drawn headings, all three
counteraction choices, and both UTF-8 copies of the marked-Spirits warning.

**GitHub #11 — post-prologue narration.** Added exact draw-time translations
for all 18 text lines in STG0001B member 7. This is an 88-byte-record container,
unlike the 84-byte opening crawl; its detector previously missed it. Keeping
the container untouched avoids overwriting timing fields or truncating prose.
The UI-hook loader now expands glossary references in English hook text.

**GitHub #23/#35/#36/#31 and #30 — save dialogs and level-up stats.** Added
the save destination choices, new/overwrite prompts, post-save continue prompt
and Yes/No choices. Added the reversed DEF/SKL two-line source used by Level Up.

**GitHub #10 and #14 — Get Result captions.** Added Z Chips and a joined
Unit heading for the split `ユニ` / `ット` source. Shortened the standalone
Funds Earned caption to Funds so it does not collide with the reward amount;
the wider Tactical Situation combined Funds Earned / Total Funds block stays.

**GitHub #9, #18, #20 — battle speaker labels.** Added the executable's
standalone UTF-8 AI, Branch Member and Shotaro labels to the display-label
pass. These are speaker captions, not SRVC battle voice lines; no voice
translation or subtitle slot is changed.

**GitHub #7 — Kyoko's robot description.** Changed "mystery robots" to
"mysterious robots" in Scenario 2, preserving the surrounding dialogue and
glossary reference.

(nothing yet)

## 0.5.0 -- 2026-09-05

The battle voice track is complete: all 211 sections, 31,000+ lines.
With it, the descriptions (spirit, skill, special ability, boost part),
the Lecture Plate tutorials, the Combat Record, the library labels, full
pilot names on the status screens, and the PP / parts / upgrade screens.
Shipped as xdelta patches with an applier script and docs/INSTALL.md.
Also shipped as ONE xdelta for the whole disc image: `tools/iso_patch.py`
copies the pristine ISO, appends the 21 shipped files as new sectors and
repoints their ISO9660 directory records (primary and Joliet trees), so
every original sector stays in place and the image-level delta is 27 MB.
The patched image is verified by reading every shipped file back through
the directory tree against the snapshot's hashes, and the delta by
decoding it and comparing the result byte for byte.

**Voice: section 106 -- Space Galaxy Dai-Gurren's bridge crew, not Black
Getter, 188 lines** -- the brief's weapon-match attribution (Black Getter /
Ryouma Nagare, score 3.0, flagged middling) is wrong: there is no Getter
Robo content in these lines. Every glossary term and every name hailed in
the barks (Leeron, Gabal, Tetsukan, Dayakka, Kittan, Kiyoh, Kamina,
Lordgenome, Anti-Spiral, Mugann, Attenborough) is Tengen Toppa Gurren
Lagann sequel-era cast, and the section's one weapon call-out,
確率変動弾 -> Probability Shift Shell, is Tetsukan's own signature attack
per his bio in `translation/library/pt_280.json` ("fired off a
probability-shifting round that nullified the enemy's defensive odds"),
confirming he voices the Shell sequence (227-241) and the surrounding
gunner-shout run (177-265). The unit is 超銀河ダイグレン, shipped as "Space
Galaxy Dai-Gurren" at `translation/library/rt_160.json:202`, called by its
short form "Dai-Gurren" here the same way section 107 reused "Gunmarl" for
"Space Gunmarl". This is not a single pilot's voice bank but the whole
bridge crew: Leeron answers in character when hailed by name (8-9, 61-96)
in the feminine register his bio documents, Gabal is addressed as helmsman
throughout, Tetsukan is hailed directly and voices the gunnery block, and a
revived Lordgenome -- reactivated as the ship's bio-computer per
`translation/library/pt_320.json`'s Rossiu bio -- delivers the calm status
reports (108-165) then turns playful once he gets an actual voice
(172-174). Recorded under "106" in `analysis/voice_identity.json` as an
ensemble rather than one pilot, since that is what the section actually is.
Budgets were extremely tight throughout (many single-digit budgets forced
whole clauses to drop): entry 143's bare "アンチスパイラル…！" (budget 10)
couldn't fit even the glossary's own "Anti-Spiral" (11 letters) so shipped
as "Antispiral" with the hyphen dropped; entries 191/192 (budgets 18/15)
had to drop the hyphen the same way to fit "Target: Antispiral" and "Hit
Antispiral!"; entry 189 ("ムガンを叩き落とす！", budget 10) dropped the verb
entirely to ship just "Mugann!"; entry 76's beauty-dies-young idiom
(budget 11) compressed to "Bad luck..."; entry 234 dropped Attenborough's
name entirely ("It's the Shell!") since the name alone doesn't fit
budget 16. `check_voice.py` reports 0 problems, 188 of 188 distinct lines
answered.

**Voice: section 64 rebudgeted -- Kira Yamato, Strike Freedom Gundam, 134
lines** -- the file's first draft answered all 134 lines but ignored the
per-line byte budgets almost entirely: `check_voice.py` failed 131 of them
("costs N cells, budget M"). Every flagged line was retranslated from
`work/voice/brief/064.md`'s Japanese to fit its budget, not just trimmed;
one outright meaning inversion surfaced along the way -- entry 162
("シールドがあるんだ！　これぐらいは！", a confident "I have a shield! This much
is fine!", matching entry 53's same これくらい usage) had shipped as "I have
a shield! Not enough!", the opposite sense; fixed to "My shield holds!".
The brief's own attribution (Gundam Mk-II, weapon-match score 2.0,
explicitly flagged as untrustworthy) is wrong: entry 132's self-announcement
("キラ・ヤマト。フリーダム、行きます！", pilot's name plus machine name plus a
launch verb) and entry 160's apology to Lacus for taking Freedom into battle
again ("ごめん、ラクス…またフリーダムを…") both point to Kira Yamato, and
`robots.json` i=67 confirms this game's only mobile suit on file for him is
Strike Freedom Gundam -- there is no standalone Freedom Gundam in this
roster, so "Freedom" in these barks (entries 55, 63, 69, 132) is the
section's own short nickname for Strike Freedom, not a second unit.
Recorded under "64" in `analysis/voice_identity.json`. Budget forced real
meaning loss throughout the tightest lines: entry 134's "No matter how far
we're blown back, we'll surely plant flowers again" (27-cell budget) shipped
as just "We'll plant flowers again", dropping the entire first clause;
entries 155/156/192 (8-10 cell budgets addressing Heero and Setsuna) had to
drop the addressee's name entirely since name-plus-verb does not fit in
single digits; entry 144 keeps "freedom" over "peace" (「自由や平和を」) given
the speaker's own machine's name; entry 197's 超兵 ("Super Soldier" in this
Gundam 00-adjacent context, not SEED's "Extended") was compressed away
entirely, shipping only "Still human!". `check_voice.py` now reports 0
problems, 134 of 134.

**Voice: section 103 is Daguza Mackle, not Gadlight Meonsam/Geminia, 133
lines** -- the brief's own weapon-match attribution (score 3.0, the same
low-confidence method that was flatly wrong for section 8's Strike
Freedom filing) named the wrong pilot and unit. Geminia's own zukan entry
(`robots.json` i=244) is an original mecha piloted in-fiction by Gadlight
Meonsam, a drunkard commander of the villain squad "Geminis" watching
chaos he caused from a bar -- none of that appears anywhere in these
lines, which are pure Mobile Suit Gundam Unicorn content: Full Frontal,
Neo Zeon, the Sleeves, Nahel Argama, Ra Cailum, Banagher, the One Year
War, Red Comet. The speaker self-identifies by radio callsign twice
("Daguza" at entries 2 and 152, "this is Daguza, engaging/supporting")
and by full name in the withdrawal line (226, "Daguza Mackle, withdrawing
from the front line"). `pilots.json` i=137 confirms Daguza Mackle, Lt.
Colonel, commander of "Echoes Squadron 920" -- exactly the "Echoes"
(エコーズ) name repeated through the set (entries 3, 11, 49, 179, 199, 227)
as his own squadron's name, not a coincidence. A crew-support family
(156-158, 165-167) addresses fellow officers by rank alone (Captain,
Lieutenant, Ensign), fitting a Nahel Argama commander giving orders.
Recorded under "103" in `analysis/voice_identity.json`, which also flags
what could not be verified: no `robots.json` entry lists Daguza as PLTN,
so the specific mobile suit voiced here is unconfirmed (Rezel, the
Federation unit several unnamed pilots share with PLTN left blank, is a
plausible but unproven guess). Budget forced compression throughout
(3-9 letter budgets were common): several direct-address lines to
Banagher or a named rank dropped the addressee to fit (163 "Situation!",
164 "Fall back!", 156 "Take over", 157 "Leave it!"), 244's double-bang
"バナージ！戦えっ！！" ships as the bare "Banagher!!", and a few enemy taunts
dropped their glossary reference under pressure (12 "Man Hunter!" alone
loses "misjudged", 199 "Scared, huh?!" drops "Echoes", 207 "This good?!"
drops "Red Comet"). One collision surfaced between two pre-filled
entries sharing "Ha!" (39 せいっ！ vs 42 はっ！, budgets 4 and 3); 39 now
ships as "Hah!" to keep them distinct. `python tools/check_voice.py
work/voice/answer/103.json`: 0 problems, 133 of 133 answered.

**Voice: section 50 is Katz Kobayashi, not Kamille Bidan/Zeta Gundam, 134
lines** -- the brief's own weapon-match attribution (Beam Confuse/Fin
Funnel/Funnel/Beam, score 3.0) named the wrong pilot: entry 17
self-identifies by radio callsign, "こちらカツ！　援護します！"
("This is Katz! Providing support!"), the same kind of self-naming that
settled section 166 as Riddhe Marcenas rather than the brief's guess.
Content matches `pilots.json`'s Katz Kobayashi bio point for point: he
addresses Kamille, Emma Sheen, Captain Quattro, Amuro and Captain Bright
by name in paired support-attack/support-defend lines (82-92) rather
than being any of them (so he is not piloting Zeta Gundam here either --
he calls out to protect Kamille by name at 83/88); he pines for Sarah
Zabiarov and begs her to leave Scirocco's side (134, 151, 243 "Sara, get
away now!", matching the bio's "fell for Sara, tried to talk her away
from Scirocco, she died protecting him instead"); his signature
insecurity about being just a kid tagging along surfaces directly (93
"I can help too!", 80 "I'm no rookie!"); and his family is named outright
(96, "Not Dad's museum" -- his adoptive father Hayato Kobayashi is a One
Year War veteran, fitting a mobile-suit museum backstory; 139 names his
adoptive siblings Letz and Kikka, not in this section's glossary and
romanized here on regular katakana conventions, unconfirmed elsewhere).
A second cluster (234-250) runs a later arc alongside Riddhe Marcenas,
Fa, Hathaway, the Nahel Argama and Ra Cailum -- exactly the ally roster
section 166's own identity note lists Riddhe addressing, which
independently names "Katz" among them, so this project's "Kamille
survives" crossover conceit (already noted for section 56) extends to
Katz surviving his canonical death too, fighting on into the Unicorn-era
cast. Unit is left null: no line names its own machine, and
`robots.json`'s Methuss entries (i=36/37) list no fixed pilot, which
would fit an alternate mount for Katz but isn't confirmed. The Beam
Confuse/Fin Funnel/Funnel weapon magnet is the same cross-unit collision
already documented for sections 56/68/87/131/166. Recorded under "50" in
`analysis/voice_identity.json`. Budget forced compression throughout
(4-11 letter budgets were common): several support lines dropped the
addressee's name entirely to fit (89 "Look out!", 236 "Covering!", 237/242
kept "Nahel Argama" but dropped the verb), entry 83 ("Kamille, leave the
rest to me!") ships as the bare "Kamille!!", and entry 65 ("Me too!")
compresses to "Also!" at a 5-letter budget. python
tools/check_voice.py work/voice/answer/050.json: 0 problems, 134 of 134
answered.

**Voice: section 71 is Sousuke Sagara piloting the ARX-7 Arbalest, 141
lines** -- the brief's own weapon-match attribution (score 3.5, the same
method that was flatly wrong for section 8's Strike Freedom filing) is
confirmed correct here by content: entries 13/14/15/135/143/220
self-identify with the callsign "Urzu 1", matching Sousuke's callsign as
already shipped at `work/voice/answer/072.json` (Kurz Weber's file, entry
187, where Kurz calls out "Urzu 1!" to Sousuke), and the glossary's own
Sousuke voice note ("clipped, literal, military... reports in the form
'Urzu 7, understood'") matches this file's declarative, no-hedging
register throughout. Entries 33/173/203 name the Lambda Driver, the
Arbalest's signature system. A support block (entries 145-155)
addresses two named allies distinctly: "Melissa" by given name (145,
153) and "Urzu 6" by callsign (146, 154) -- both are Kurz Weber, whose
own file self-identifies as Urzu 6; the same block also addresses
"Sarge" (147, 148, 155, 218), this project's already-shipped rendering
of 軍曹 (`work/voice/answer/111.json` entries 322-323). Sousuke can't be
addressing himself, and Kurz holds the same Mithril NCO rank, so "Sarge"
here is Kurz too -- confirmed by entry 218 ("Sarge done?") immediately
preceding entry 219's "Weberrrrr!!", the scream when Kurz's plane goes
down. Entry 151 ("Save the Colonel") reads 大佐殿 as Andrei Kalinin, the
submarine's XO, by title rather than name (the Japanese doesn't name him
either). Entries 37-63 and 95-227 are a long run of enemy-reaction
taunts naming other crossover properties by content: "Red Comet" (47,
Char Aznable, already shipped, e.g. `work/voice/answer/045.json`) and
"Third Impact" (59, Evangelion), alongside generic
soldier/psychic-power/god-of-strife descriptions (33, 40-42) that name
no specific glossaried character and so ship as plain description
rather than invented proper nouns. Recorded under "71" in
`analysis/voice_identity.json`. Budget forced several compressions that
lose real nuance: entry 41 ("Not buying war gods") drops the explicit
"I don't intend to"; entry 95 ("Blended strike / Take it") drops the two
named martial-arts techniques (Tesshi, Sunkei) the Japanese calls out;
entry 151 ("Save the Colonel") drops "and the ship"; entry 155 ("Watch,
Sarge") drops "always"/"the whole picture"; entry 185 ("Nice gear")
turns "your equipment saved you" into a bare acknowledgment. `python
tools/check_voice.py work/voice/answer/071.json`: 0 problems, 141 of 141
answered. Not yet merged to `translation/voice_071.json`.

**Voice: section 116 is the Rewloola's bridge crew, not unit Fatty, 132
lines** -- filed as unit Fatty (the VOTOMS Balarant AT) by weapon-name
match, score 1.0. Wrong: no AT combat, no VOTOMS content anywhere -- the
weapon table matched (Mega Particle Cannon, Missile, Anti-Air Machine
Gun, Anti-Air Cannon) is generic warship armament, and every line is a
warship bridge shouting gunnery orders. This is the same Fatty
weapon-name trap already caught for section 44 (also filed Fatty at
score 1.0, actually the Nahel Argama's own bridge crew) -- 116 is the
other side of that fight: the Neo Zeon flagship Rewloola's bridge crew
from Mobile Suit Gundam Unicorn, attacking the Nahel Argama, matching
this project's own section 135 (unit Rewloola, pilot null) almost line
for line. Entry 16 names the attack target outright ("Nahel Argama!",
glossary'd, this brief's own term); entries 15/17/19/20/178 hunt "Londo
Bell" and its flagship/MS by name. Two superiors are addressed only in
the third person, exactly as established for the Rewloola in 135:
総帥 (entries 116, 122 -- Full Frontal, rendered "Commander"/"him"
elsewhere in this project) is followed and must not be lost, and 大佐
(entries 117, 123 -- the Colonel) is told not to be gotten in the way of
and ordered to retreat, the identical pattern as 135's entries 77/83.
`source/library/pilots.json` documents an unnamed 43-year-old Colonel as
the Rewloola's own captain, uncomfortable with Angelo Sauper's Guard-corps
authority but doing his duty, attacking the Nahel Argama that recovered
the Unicorn Gundam -- so "the Colonel" here is that captain, not the
speaker. 親衛隊 (the Guard, entries 119, 125) is likewise a third party to
be aided/watched, Full Frontal's Sleeves personal guard under Angelo
Sauper. Wider cast confirms the same Unicorn-era crossover-battle register
already shipped for this project's other Rewloola/Sleeves sections
(044/045/094/135/143): Neo Zeon and Spacenoid pride (200-201, 204), the
White Devil legend reviving (172, Amuro's epithet), a Newtype taunt
(175), and taunts against Celestial Being's Gundam (22), the Federation
special-forces unit Echoes (21 -- confirmed by `source/library/pilots.json`
and `robots.json` as the Nahel Argama's own commando unit from Gundam
Unicorn, not the Full Metal Panic mercenary group of the same name), the
Black Knights (38), and a "traitor colony's Gundam" (23). No individual
crew member self-identifies, so pilot is recorded null, matching 135's
own collective-bridge-voice conclusion. Not confirmed by a screenshot.
Recorded under "116" in `analysis/voice_identity.json`. Budget was severe
throughout (6-9 letter budgets common for full gunnery/chain-of-command
orders): entry 116 (budget 6) could not fit "Follow!" (used for the same
near-identical line elsewhere, e.g. `voice_094.json`) and ships as bare
"Follow", losing both the mark and the explicit 総帥/Commander reference;
entries 122, 117, 123, 125 similarly drop the explicit
"Commander"/"Colonel"/"Guard" title for a bare pronoun or generic verb to
fit ("Can't lose him!", "Stay clear!", "Retreat now!", "Watch Guard!");
entry 105 (budget 10) could not fit "Mega Particle Cannon" at all and
ships compressed as "MPC, all!", matching the abbreviation this answer
file's own pre-filled entry 101 already used for the same weapon under
the same pressure. `python tools/check_voice.py work/voice/answer/116.json`:
0 problems, 132 of 132 answered. Not yet merged to `translation/voice_116.json`.

**Voice: section 175 is Rei Ayanami piloting Evangelion Unit-00, 134
lines** -- filed as unit UNKNOWN, no weapon call-out matched. Entry 3
("I'm not a doll") is her single most famous line; entries 17/73/100/140
self-report as 零号機 (Unit-00) beginning combat, counterattacking,
undamaged and disabled; entries 0-8 run her classic self-negation
monologue (nothing else, only EVA connects her to people, EVA as a
mirror, acting on Ikari's wish, her own will); entry 30 defends against
Lilith (the section's one glossed term); and the AT Field vocabulary
(110-123) matches the register already documented for Shinji in section
93. A second voice is bundled in the same way section 93 bundles Misato
into Shinji's set: entries 9, 11, 103, 119, 127 address "Rei" by name,
giving orders and checking on her after damage -- consistent with
Misato Katsuragi's established register but not confirmed by a
screenshot. Entries 142-158 are the fourth-wall "next episode preview"
omake this project has already documented for other sections, closing
with the same stock "Service, service!" sign-off already shipped at
`translation/voice_093.json` entries 264/282, and banter about the warmth
("ぽかぽか") Rei feels around Shinji and wants the player and Commander
Ikari to feel too. Unit names follow the EVA-0N convention already
shipped at `translation/voice_093.json` entry 309 ("EVA-01 pilot,
Shinji!"): EVA-00 for her own unit, EVA-02 for Asuka's (entries 85-86,
92 -- the Japanese never names Asuka, only "the second child"/"the
Unit-02 person"; the name comes from this project's own prior glossary
identification of the Second Child, not an invention). Recorded under
"175" in `analysis/voice_identity.json`. Entry 146 (碇君, budget 2) ships
untranslated -- no two-letter rendering of a name is a translation
rather than an invention. Several lines lost real nuance to budget:
entry 4 drops "of one's own heart" ("EVA - mirror"), entry 41 drops
"that's all I need" ("Want to stay here"), entry 136 drops the name
Shinji to fit "He won't quit", entry 144 drops "people wishing to live"
("Thawed, where's EVA-00 headed?"), and entry 157 drops "get along with"
("Want Ikari warm too"). `python tools/check_voice.py
work/voice/answer/175.json`: 0 problems, 133 of 134 answered. Not yet
merged into `translation/`.

**Voice: section 160 is Gamlin Kizaki piloting the VF-22S Sturmvogel II B,
138 lines** -- the brief's own weapon-match filing (score 2.0) is confirmed
by content, not just trusted on the score: this section's own glossary
table already carries Alto (Alto Saotome), Klan (Klan Klang), Canaria
(Canaria Bernstein, addressed as "Lt Canaria" at entry 107) and the unit
name itself, all Macross Frontier, and the lines name the Vajra enemy
throughout (12-16, 180), the weapon table's Ghost and Reaction Missile are
Frontier ordnance, entry 155 references escorting "Fire Bomber" (a
crossover joke pulling in Macross 7's in-story band), and entries 100/117
name Luca Angelloni's unit Quarter, all consistent with Gamlin's canonical
role escorting the Skull squadron and its idol charges. Male first-person
register ("ore", -ze/-da endings) is corroborated by content, not inferred
from the name alone: entries 121-122 self-declare "can't leave a girl in
trouble" / "a man protects" as his own motivation, and 151/230-233 show him
shielding Alto and fretting over an unnamed "her" while retreating.
Recorded in `analysis/voice_identity.json["160"]`. Budgets were unusually
brutal even by this project's standard (several 4-8 letter budgets):
entry 226 ("反応弾なら！", budget 6) could not fit the shipped weapon name
Reaction Missile at any compression and ships as the generic "Boom!",
losing the weapon call-out entirely -- flagged, no better option existed.
Entry 67 ("一発必中でな！", budget 7) compressed the "one-shot, one-kill"
idiom to "1 shot!" using a numeral to save a letter; entry 102's
"フォーメーションＭＭジーナス" formation name has no prior glossary spelling and is
transliterated "Jeanas" (unconfirmed). Entry 66 ("何せ俺は、女も弾も…", budget 10)
compressed a two-noun setup line to "Girl, gun" ahead of its budget-7
punchline at entry 67. `python tools/check_voice.py
work/voice/answer/160.json` reports 138 of 138 answered, 0 problems.

**Remaining Unit List Team heading.** The roster stores `ー` and `チ　ム`
as separate overlaid strings at FSSA 0x662A6/0x662AA, so normal `チーム`
matches missed it. Hook the spaced label to Team and blank only that exact
overlay stroke in place, guarded against unexpected source bytes. Other kana
and the existing Mech Info Team fragment fix remain unchanged.

**Pilot Training / Unit List headings.** Added exact bracketed window titles
and compact support-skill, team, armor/mobility/sight, max-power, weapon-type,
repair, sword, shield and barrier column captions. Two Unit List Resupply
headings at FSSA 0x66710/0x667A4 use a same-size internal 補． marker hooked
to Sup.; other Resupply labels and Spirit names are unchanged. This avoids
the full Resupply caption running into the sword column.

**Pilot Training PP block and tabs.** Added Raise Stats / Learn Skills
joined labels for the split tab words. The PP block's separate three-row
label and PP-suffix strings get one exact joined replacement, PP Held /
PP Cost / PP Left, suppressing the old suffix block. The combined-label
variant is covered too. All 22 vertical Air/Grd/Wtr/Spc FSSA rows now use
the existing small terrain cells in place, including the missed Grd row;
their byte lengths, line breaks and cell counts are preserved.

**Intermission Team Setup button fragment order.** The selected/unselected
button copies store `チー`, `編成`, `ム` consecutively (four copies at FSSA
0x60BD4/0x60BE4/0x60D98/0x60DA8), not the visual `チーム編成` order.
Added an exact joined `チー編成ム` match so the first fragment draws
Team Setup and the later two fragments are suppressed. Existing normal-order
matches remain available for other screens; no individual kana is replaced.

**Info-screen labels and Spirit footer spacing.** Added Weapon Info class,
target/type, IFF and pattern labels; Unit Info's combined Skills/Spirit
heading; full/custom upgrade bonuses and their unlock message; Spirit-panel
Foc; and pilot-training labels. The six training stats use reserved terrain-
size cells U+E018-E01D (0x86D0-D5), keeping the original two-cell label slots.
The first two fixes left 格/射 Japanese. Combined/per-line hooks and all four
FSSA template replacements were insufficient: the game overwrites those rows
at runtime. Disassembly at VA 0x31B32C/0x31B34C traces the widget text setters
to bare labels at executable offsets 0x710890/0x710898. These two source
cells now become CQB/RNG directly; all padding and adjacent song-pilot labels
remain unchanged. Rebuild verification checks the exact original/new slots.
Mech Info's reordered Team fragments are replaced only in their exact
three-string block, preserving all offsets and avoiding global kana swaps.

**Voice: section 67 is Gura King Jr., Tetsujin 28 crossover, 152 lines** --
brief filed unit/pilot Space Demon King on a weapon-match score of 2.0 (only
entry 38's "Black Hole" call-out, the sole weapon this project's weapons.json
ties to that name) and warned not to trust it. Content confirms it is wrong:
the speaker self-names in third person at entries 19, 151 and 207 (`Gura King
Jr.\nyour foe!`, and twice more taking damage), calls himself "prince" (not
king) at 208, and addresses "Father" as a separate person at 18, 42, 43, 134,
178 and the fourth-wall 212-214 exchange. `source/library/robots.json` splits
the family cleanly: i=12 "Space Demon King" pilots himself (a fused being,
father of Gura per its own DSC2 text); i=9 "Space Robo No. 7" is piloted by
Gura King Jr. and its description is literally Episode 50's title fight,
"Prince Gura Dies!" -- the sword duel with Shotaro/Tetsujin on the moon,
matching this section's sword call-outs (92-94) and named challenges to
Shotaro/Tetsujin/Ox (22-24). Entries 105-118 read as a support/ally family
(protective lines to Duncan, Shotaro, Ox, Mars, Watta), not taunts, matching a
crossover team-up stage. Unit recorded as Space Robo No. 7 with i=8 (Space
Robo No. 5, also his) flagged as a live alternative since the game doesn't
label voice files by robot number. `analysis/voice_identity.json["67"]`
carries the full finding. Budget forced meaning loss on several entries,
flagged in the translator's report: 28, 31, 133 and 166 all drop an explicit
mythological/genre reference (devil god, Gurren-Lagann-style "spiral",
"psychic") to fit; 208 drops its whole second clause to keep the
self-identifying "I'm Earth's prince!"; 214 drops the poetic "after a brief
sleep" image to keep the more plot-relevant "we'll meet again" promise; 107
and 130 drop Shotaro's name outright under budgets too tight to hold both
name and verb. `python tools/check_voice.py work/voice/answer/067.json`: 0
problems, 152 of 152 answered.

**Voice: section 154 is Mikage Towano, Aquarion EVOL, 141 lines** -- filed
as unit UNKNOWN with no weapon-table match; the speaker names herself in
entry 0 ("私の名はミカゲ…", "My name is Mikage...") and `analysis/glossary.json`
carries the fuller pilot record トワノ・ミカゲ -> "Mikage Towano". Content is
unmistakably Aquarion EVOL: the red-dream/blue-reality cosmology (15, 17),
becoming a "genesis god" of a new world (12, 17, echoing the original
series title "Genesis of Aquarion"), an obsessive fixation on Apollonius as
a lost beloved (21, 22, 65-70, 230, 232), direct address to Kagura Demuri
as a "pet dog biting its master's hand" (165, 197), a reference to
Triangler (56), and a "Mechanical Angel" name-inheritance taunt (198).
Entry 253's "蹂躙合体！GO！アクエリオン！" ("Violation Union! GO! Aquarion!") is a
corrupted parody of the canonical "Element, Union! GO! Aquarion!" call,
confirming she has taken over a corrupted Aquarion for the fight -- with no
weapon table for this section, the unit is recorded generically as
"Aquarion" rather than an invented "evil Aquarion" label.
`analysis/voice_identity.json["154"]` records the finding. Budgets were
brutal (many 7-15 letters): entries 65/67/69 (budgets 7/15/10) had to
abbreviate Apollonius to "Apollo" since the 10-letter full name alone would
not fit, even though the full name is kept everywhere else the budget
allows; entry 71 ("神の力こそ、無限…", budget 9) compressed to "Godpower!",
dropping the explicit "infinite"; entry 157 ("笑止…", budget 3) shipped as
just "Ha!"; entry 178 ("愛の調べは…無常", budget 8) shipped as "Loveless" rather
than the more literal "love is impermanent"; entry 234's fourth-wall
postgame line about maxed funds and hidden units (budget 40) dropped "even
once" nuance to fit "Help me once: max funds, hidden units"; entry 240
(budget 38) dropped the "forget the game" aside entirely to keep "Beauty
has no gender. Join me tonight." Entries 239-240 name a "レア・イグラー"
(Rea Iglar) and "アルテア" (Altea) with no established glossary spelling to
match, transliterated as given. `python tools/check_voice.py
work/voice/answer/154.json` reports 141 of 141 answered, 0 problems.

**Voice: section 132 is Zechs Marquise piloting Tallgeese III, 145 lines**
-- filed as unit/pilot Tallgeese III / Zechs Marquise on a weapon-match
score of 1.0 ("middling" per the brief's own caution), and this one checks
out: entries 261-263 are his canon Endless Waltz duel taunts at Wufei
("Wufei, push the self-destruct switch!", "Wufei, is this your idea of
justice?!", "Treize's gone! You killed him."), 145-146 are his despairing
asides to Wufei about looping through the same battles, and 150-155
reference Zero (the Wing Gundam Zero system, not the Code Geass character
sharing the romanization), Relena, and fighting hardest on Earth. Entries
163-176 and 200-201 are a support-bark family addressing fellow pilots by
name (Trowa, Quatre, Wufei, Noin, Duo, Amuro, Kamille, Kira); glossary
names used verbatim. Two entries read oddly for a first-person voice bank
-- 201 ("Zechs... I'll cover") names the speaker's own callsign, and 215
("That all, Zechs?") reads as a taunt directed AT Zechs -- most likely both
are bundled from the other side of a scripted duel exchange that the
extractor filed under Tallgeese III's bank; translated literally rather
than guessed away. `analysis/voice_identity.json["132"]` records the
finding. Budget forced real meaning loss in several places (many budgets
4-11 letters): the support-bark family above mostly dropped either the
ally's name or the verb, never both (e.g. 169 "Retreat!" drops "Trowa",
170 "Easy now" drops "Quatre"); 261's "self-destruct switch" collapsed to
"Wufei, hit it" (13-letter budget); 263 dropped the "Wufei" address to
keep "Treize's gone! You killed him." (30-letter budget, two line breaks);
152's three-line "Relena, / life's cheap / mine most." compresses
"especially mine" into an awkward "mine most" to fit a 31-letter, two-break
budget; 215 dropped the name "Zechs" entirely to fit "Enough?" in a
9-letter budget. `tools/check_voice.py work/voice/answer/132.json` reports
145 of 145 answered, 0 problems.

**Voice: section 124 is Basara Nekki piloting the VF-19 Kai Fire Valkyrie,
143 lines** -- filed as unit/pilot "Space Demon King" (宇宙魔王) on a
weapon-match score of 3.0, the same middling-score trap the brief warns
about (its section-8 example scored 7.5 as Strike Freedom/Kira Yamato and
was really a Full Metal Panic mercenary). Wrong here too: there is no
Space Demon King content anywhere in the section. The catchphrase "俺の歌を
聴け" (Hear my song!, Basara Nekki's series tagline from Macross 7) recurs
throughout (23, 29, 31, 42, 64, 72, 76, 121, 122, 154, 167, 220), the
weapon call-outs are Fire Bomber's own songs (PLANET DANCE, MY FRIENDS, TRY
AGAIN, DYNAMITE EXPLOSION, TOTSUGEKI LOVE HEART -- all in the brief's own
weapon table), and entry 45 names his own machine directly ("俺のバルキリー",
my Valkyrie). `source/library/robots.json` i=106 (VF-19改Fバルキリー / VF-19
Kai Fire Valkyrie) confirms Basara Nekki (熱気バサラ) as its pilot;
`analysis/glossary.json` already ships "Basara"/"Basara Nekki" and "VF-19
Kai Fire Valkyrie". The section bundles two-sided ensemble banter, the
pattern already documented elsewhere in this corpus for Macross content
(Klan Klang's, Canaria's and Michel's own files): Mylene Jenius answers back
in her own feminine register (あたし/わよ endings: 58, 61, 101, 115, 129,
133, 141, 157, 165, 166, 170-172, 215), addresses Basara by name (58, 165,
166), and Ray Lovelock -- the bandmate who "can read Basara's scores" per
his own bio -- calls musical-chord formation orders addressed to both by
name (132, 136, 140, 152, 156, 214), answered "OK Ray"/"Yes, Ray!" in turn
(137, 153, 215); Gamlin Kizaki and Alto Saotome are each addressed once by
name (24, 110) as established SRW Z3 teammates. Budget forced real meaning
loss throughout (many budgets 8-17 letters): the weapon name TOTSUGEKI LOVE
HEART (budgets 14/9) shipped generic ("Charging in!", "Charge!") since the
bare name alone is 20+ letters; entry 24 dropped the literal "can't stand
watching this" down to the interjection "Sheesh, Gamlin" just to keep the
name; entry 111 dropped the causative structure for "No sad sister"; entry
165 (an 8-letter budget) dropped Basara's name entirely, keeping only the
verb ("Hear me"); entry 219 (Black Hole, the brief's own weapon table)
dropped the explicit "with song" clause to land exactly on budget.
Recorded in `analysis/voice_identity.json`. `python tools/check_voice.py
work/voice/answer/124.json`: 0 problems, 143 of 143 answered. Not yet
merged into `translation/`.

**Voice: section 167 is Luca Angelloni piloting the RVF-25 Messiah, 150
lines** -- filed as unit VF-22S Sturmvogel II B / pilot Gamlin Kizaki via a
weapon call-out (Ghost/Reaction Missile, score 1.0), the brief's own example
of a middling score that can be flatly wrong. Wrong here too: the section
self-identifies by radio callsign "Skull 3" (entries 0, 1, 42, 83, 91, 112,
201, 203, matching this project's own rendering already shipped in
voice_043.json) and by name via Luca's three named Ghost QF-4000 escort
drones Simon/Yohane/Petero (22, 24, 26, 153, 157) --
`source/library/robots.json` i=117-120 confirms Luca fights by remotely
directing the unmanned Ghost QF-4000 because his own RVF-25 lacks firepower,
matching entries 180-182's plot beat. `source/library/pilots.json` i=173
confirms Luca Angelloni, S.M.S. Skull Squadron, Ensign, 15, a gentle
mediator between Alto and Michel who rides the RVF-25 -- matching this
section's polite, self-doubting register and its direct-address squadmate
lines to Ozma, Michel, Alto, Klan and Canaria (all established Frontier
castmates already glossed in voice_043/055/070). A running Vajra-data-
collection motif and a romantic subplot naming Nanase both match Luca's
canon arc in the movie "Sayonara no Tsubasa". Recorded in
`analysis/voice_identity.json`. Budgets were severe: "Reaction Missile" (16
letters) could not fit its 8- and 14-letter budgets at entries 200/202 and
shipped generic ("Use it!"/"Cleared, go!"); the drone names Simon/Yohane/
Petero (rendered Simon/John/Pete for length) could only be spelled out in
full once, at entry 157 -- entries 22, 24 and 153 had no room and shipped
the generic "All three!" family instead. `python tools/check_voice.py
work/voice/answer/167.json`: 0 problems, 150 of 150 answered. Not yet
merged into `translation/`.

**Voice: section 129 is Banagher Links piloting Unicorn Gundam, 143
lines** -- filed as unit Gundam Mk-II via a beam-rifle/vulcan common-weapon
match, the same magnet the brief itself warns has misfiled multiple sections
onto Mk-II. Section 128 (this game's correctly-filed Unicorn Gundam/Banagher
section) shares unmistakable content: NT-D (32), the reveal line "A Gundam!"
(35, Banagher's canonical first-boarding moment), Audrey addressed by
glossary name (36, 91), the unit self-addressed as "Unicorn, go!" (216), and
his signature near-death "potential" line (90, the iconic "kanousei" line --
budget forced the trailing scream to drop). He addresses Marida Cruz and
Gilboa Sant by first name without honorifics (59/102/175/194 Marida;
103/176/195 Gilboa) in the same register already shipped for him in section
128, and reacts to Char Aznable, Full Frontal/Frontal, Haman/Haman Karn, the
Guard (親衛隊, this project's established rendering, see
translation/voice_189.json/voice_190.json), and Char's Red Comet epithet
(established elsewhere in this project, e.g. work/voice/answer/020.json) --
all Unicorn's UC-0096 cast, not Zeta-era Mk-II content. Budgets were
severe (many under 10 letters): entry 104's Red Comet reference could not
hold "Red Comet" (9 letters) in a 6-letter budget at all and shipped as the
bare glossary name "Char!" instead; entry 91's "ごめん…オードリー…" dropped
the name "Audrey" to fit 10 letters, shipping "Sorry..." alone; entry 100
dropped its trailing "I'm...!" clause; entry 90 dropped the trailing scream
after "potential". Recorded in `analysis/voice_identity.json`.
`python tools/check_voice.py work/voice/answer/129.json`: 0 problems, 143 of
143 answered. Not yet merged into `translation/`.

**Voice: section 069 is Graham Aker piloting Brave (Mobile Suit Gundam 00),
163 lines** -- filed as unit Geminia / pilot Gadlight Meonsam via a
weapon-name match at score 1.0, the brief's own example of a middling score
that can be flatly wrong (its section-8 case scored 7.5 as Strike
Freedom/Kira Yamato and was really a Full Metal Panic mercenary). Wrong here
too: the section repeatedly self-names "このグラハム・エーカー" ("this
Graham Aker", entries 11, 27, 87, 123, 146, 227) and names its own unit
"ブレイヴ" (Brave, entries 10, 11, 19, 77), and `source/library/robots.json`'s
ブレイヴ entry (RBTN, PLTN グラハム・エーカー) confirms Graham Aker as
Brave's pilot directly -- no Geminia/Gadlight content anywhere. Crossover
content spans the whole game: Patrick Mannequin, Kira Yamato, Char Aznable
(addressed once by his "赤い彗星"/Red Comet epithet, 154, 208), Full
Frontal/Frontal, Unicorn Gundam, and Mikage all match the glossary; entries
218-223 are a distinct extended dialogue with Alto Saotome (Macross
Frontier) about discarding his mask and being a closet romantic ("Virgo,
romantic too") -- exactly Graham's established Mr. Bushido/hopeless-romantic
characterization, not a second misattributed voice. Budgets were severe
(9-letter budgets typical, several under 10): entry 70's "TransAm" dropped
the hyphen and mark that entry 73's larger budget could afford ("Trans-Am!");
entry 94 spent nearly its whole 23-letter budget on "Patrick Mannequin",
leaving only "sure?" for the second clause; entry 150 dropped the "red
thread of fate" imagery to "Your fate, I'll trace!"; entry 153 dropped the
verb entirely once "Kira Yamato" was seated, shipping "such will!"; entry 161
dropped "people understanding each other" to bare "Peace--not there yet?!".
`python tools/check_voice.py work/voice/answer/069.json`: 0 problems, 163 of
163 answered. Not yet merged into `translation/`.

**Voice: section 43 is Michel Blanc (VF-25G Messiah B/TP), 152 lines** --
weapon-name match at score 1.0, much stronger than section 8's flatly-wrong
7.5 Strike Freedom match, and the content confirms it: genuinely Macross
Frontier (movie continuity, Sayonara no Tsubasa), not a cross-show
mismatch. Entries 92-106 are the two-sided squadmate-banter block already
documented elsewhere in this corpus for Macross Frontier sections
(Canaria's and Klan Klang's own ensemble files): Michel calls out to Alto,
Luca, Klan Klang and Canaria by name, and the reciprocal side -- allies
addressing Michel back -- appears in the same block (95 "Well done,
Michel!", 103 "Reposition, Michel!"). Recorded under "43" in
`analysis/voice_identity.json`, which also flags as UNVERIFIED that
entries 120, 137, 142, 145-154 (guarding Ranka from tears, a personal Fire
Bomber/Basara Nekki devotion catchphrase, banter with Captain Gamlin and
Cathy Glass) read closer to Ozma Lee's own established register than to
Michel's -- possibly Ozma's side of a combination-attack exchange bundled
into Michel's file per the same pattern, not confirmed by a screenshot.
Budget forced real compression throughout (most budgets under 15 letters);
two entries could not hold their weapon's shipped English name at all:
144 (budget 12, "TOTSUGEKI LOVE HEART" alone is 20+ letters) shipped as
the generic "Charge!", and 193/195 (budgets 9 and 11, "Reaction Missile"
is 16 letters) shipped as "Missile!"/"Finish it!" with the weapon name
dropped. Other losses: 147/151 dropped "Captain" and "right behind
you"/"leave this to us"; 154 dropped the name "Cathy" and the apology,
keeping only "Falling back!"; 97 could not hold the full glossary form
"Klan Klang" alongside "thanks" and shipped the short form "Klan" instead
(precedented by section 070's own "Quadran" nickname compression).
`python tools/check_voice.py work/voice/answer/043.json`: 0 problems, 152
of 152 answered. Not yet merged into `translation/`.

**Voice: section 74 is Gates (Full Metal Panic! The Second Raid), 158
lines** -- filed as unit Geminia / pilot Gadlight Meonsam via a weapon-name
match, score 3.0, the same middling-score trap the brief's own section-8
warning describes (that section scored 7.5 as Strike Freedom/Kira Yamato
and was also a Full Metal Panic mercenary instead). Wrong: content is
unmistakably Amalgam operative Gates, pilot of the "Venom"-type Plan 1056
Codarl-i (`source/library/pilots.json` i=293, `robots.json` i=190; both
names already shipped as "Gates" and "Plan 1056 Codarl-i" in
`translation/library/rt_160.json`/`pt_280.json`). His bio's one
distinguishing quirk -- "particular about his sideburns, has claimed
their length is a matter of life and death" -- is an exact, repeated
match for this section's own bark family (entries 53, 241, 278, 281: "Sideburns
buzzing!" / "Sideburns quiet" / "Sideburns buzz!" / "Shorter
sideburns\nI'm dead!"). He also self-names in third person repeatedly
("Gates!" 40; "Gates attacks!" 190, a mock baseball-announcer bit; "Prof.
Gates's Lecture!" 288, paired with the section's own running "Balance
matters" bit at 216/234/284/285/287), taunts Mithril by name (32-34,
226-227, 253 -- his actual enemy per the same library records), addresses
the twin assassins Yu Fan / Yu Lan by their already-shipped short names
(198-199, 205-206, 298), and lands crossover gags at Gundam, Evangelion,
Code Geass's Black Knights (52, 261, matching the "Black Knight" rendering
already shipped in `voice_017/018/019.json`) and Bonta-kun (35). Recorded
under "74" in `analysis/voice_identity.json`, which also flags that three
of the brief's four listed glossary terms (Marie, Pen Pen, Traia) are
false-positive katakana-substring matches inside unrelated words (a scat
sound, a spanking onomatopoeia, and an invented gag name "Mr.
Triangler"), not real character references, and that the fourth (Ian)
does not occur anywhere in the section. No collisions: every distinct
Japanese line kept a distinct English string (the recurring "Balance
matters" catchphrase was varied to "Balance matters too" for the one
line, 285, that isn't identical to 216's). Budget forced real
compression throughout (9-15-letter budgets were typical); the
worst losses were entry 10 (dropped "wallet", kept only "ass"), entry
284 ("Balance..." itself doesn't fit in a 6-letter budget, shipped as
"Poise" instead), and entry 288 (dropped the "see you next week"
sign-off, shipped as "Prof. Gates's Lecture!" alone).
`python tools/check_voice.py work/voice/answer/074.json`: 0 problems, 158
of 158 answered. Not yet merged into `translation/`.

**Voice: section 152 is Mari Illustrious Makinami (Evangelion Unit-02),
154 lines** -- filed as unit UNKNOWN, no weapon call-out matched. Five
entries (0, 64, 170, 186, 203) address someone named マリ (Mari) by name,
so the primary voice cannot be Mari in those lines; but most of the
section carries her well-established "nya" sentence-ending tic (entries
46, 147, 150, 165, 171, 184, 200, 210, 218) and cheers on its own machine
as "2号機" (Unit-02) in a way that only makes sense if the speaker is
aboard it (16 "Let's go, Unit-02!", 61 "Unit-02... this is the last
job!"). `translation/library/pt_320.json` line 60, Mari's own shipped
character bio, independently confirms both traits -- "a speech habit of
tacking 'nya' onto the ends of sentences" and nicknaming Shinji "NERV's
little puppy" -- matching entry 152's 「後は任せてよ、ＮＥＲＶのワンコ君！」
and entries 42/156's ワンコ君 (puppy) address of a third party. And
`translation/library/rt_200.json`'s Unit-02 DSC2 explains why this is
Mari's set and not Asuka's usual one: "after its pilot Asuka withdrew from
the front lines, Mari Illustrious Makinami boarded it and fought the
Tenth Angel." The five Mari-addressed lines read as a second, embedded
voice bundled into the unit's own set, the same pattern as section 13's
Misato-in-Asuka's-set: entry 64 entrusts "our future" to Mari before a
decisive fight, entry 186 asks for a status report, entry 203 orders a
retreat, and entries 14 and 195 both have Mari's own reply address
"葛城作戦部長殿" (Director Katsuragi) by title -- consistent with Misato,
though not confirmed by a screenshot. Recorded under "152" in
`analysis/voice_identity.json`. No collisions after translation: two
near-duplicate "feels good" lines (11, 166) were kept distinct as "So
amazing!" and "Felt great!", and three separate "here"-type lines (15,
20, 88) as "There!", "Over here" and "Here!". Several lines lost real
nuance to budget -- entry 61 drops the "Unit-02" address ("Last job!"),
entry 152 drops "NERV" itself ("Rest to me, pup!"), entry 60 drops
"battleship" entirely ("Got it!"), entry 186 drops the "Mari" address
("Report in"), and entry 14 drops "Katsuragi" to fit "Roger" (shipped as
"Aye Katsuragi!" instead, keeping the name at the cost of "Roger").
`python tools/check_voice.py work/voice/answer/152.json`: 0 problems, 154
of 154 answered. Not yet merged into `translation/`.

**Voice: section 59 is Kallen Kozuki (Guren S.E.I.T.E.N. Eight Elements),
152 lines** -- filed as Lancelot Albion / Suzaku Kururugi via a weapon-name
match on the shipped Energy Wing term, score 2.0, the same middling-score
trap the brief's own section-8 warning describes. Wrong: entry 197,
「あたしは紅月カレン！覚えときな！」, has the speaker self-name in the first
person using あたし (atashi), a feminine pronoun this project's Suzaku
sections (4, 95) never use -- he self-refers with 自分/jibun there. She
brags about her own machine and technique by name throughout (9, 23, 79,
102, 117, 119, 201 name Guren; 118, 164, 174, 176, 177, 178 name her
signature 聖天八極式, rendered "Seiten" for budget) and addresses Suzaku,
Lelouch and C.C. as separate people (170/172 to Suzaku, 173/184 to
Lelouch, 169/171 to C.C.), guarding and leading Zero's personal guard
(62, 63) -- Kallen's canonical Code Geass R2 role. `analysis/glossary.json`
term 905 confirms 紅蓮聖天八極式 already ships as "Guren S.E.I.T.E.N. Eight
Elements" (zukan_id 227), filed directly before Lancelot Albion (228) in
the same mech list -- likely why one line (175) genuinely calls out Energy
Wing verbatim per rule 5 despite belonging to Lancelot elsewhere: a shared
team-attack bark between the two paired duel units, not evidence for
Suzaku. Recorded under "59" in `analysis/voice_identity.json`. Budget
forced dropping proper nouns on a few lines (19 loses "Chirico", 58 keeps
"Zero" as "Zero's gap!", 63 drops "captain" rank to "I guard Zero!", 74
compresses "don't underestimate Kallen Kozuki" to "Fear Kallen!", 182
drops "Britannia", 197 itself loses "remember it" to fit "Kallen Kozuki"
verbatim). `python tools/check_voice.py work/voice/answer/059.json`: 0
problems, 152 of 152 answered. Not yet merged into `translation/`.

**Voice: section 63 is Gyunei Guss (Jagd Doga), 171 lines** -- filed as Nu
Gundam / Amuro Ray via a Fin Funnel/Funnel/Beam weapon-call-out match,
score 1.0, the same funnel-callout magnet that already misfiled sections
56 (Kamille Bidan), 68 (Quess Paraya), 87 (Char Aznable) and 168 (Rezin
Schnyder). Wrong again: the speaker self-names twice, "俺はギュネイ・ガスなんだぞ！"
(entry 254, I am Gyunei Guss!) and in the third person at entry 81
("this Gyunei Guss's warning"), and `source/library/robots.json` i=47
confirms his own Jagd Doga really does carry 6 Funnels alongside its beam
weapons -- so unlike Nu Gundam's case, the funnel call-outs genuinely
belong to this unit. The rest of the section matches his CCA arc: devotion
to Quess Paraya by name throughout, repeated address of Char as "大佐"
(the Colonel) and once as "総帥" (Supreme Commander), Marida Cruz named as
an ally, and Amuro Ray/Kamille Bidan singled out as rival Newtypes he must
beat -- all consistent with `source/library/pilots.json` i=67's bio.
Recorded under "63" in `analysis/voice_identity.json`. Codex draft,
Sonnet-reviewed line by line; fixed 9 of 171 lines. Entry 23
("うっ！　まだまだ！", the idiom means "not finished yet", not a request) had
shipped as the ungrammatical "More more"; fixed to "Not done!". Entry 197
("油断したのかよ、アムロ・レイ！", accusing Amuro of dropping his guard) had shipped
as "Amuro Ray, rash", swapping carelessness for recklessness; fixed to
"Careless Amuro!", matching this section's own "Careless!" at entry 195
for the near-synonym 迂闊. Entry 240 ("これがアムロ・レイの力かよ！", marveling at
Amuro's power specifically) had shipped as the content-free "Amuro Ray?!",
dropping the one word (力, power) the line is about; fixed to "Amuro's
power!" (also dropping a stray "?" the source's single "！" doesn't
support). Entry 264 ("あいつをやればいいんだな…！", confirming the kill order on a
target) had shipped as the verb-less "That target..."; fixed to "Kill
that one!". Entry 183 ("見てろよ、クェス！", watch me, Quess!) had shipped word-
order-reversed as "Quess see"; fixed to "See Quess" at the same cost.
Entry 189 ("自分が引き受ける！", I'll take this on) had shipped as the dangling
"I'll take"; fixed to "Leave it!". Entry 169 ("落ちろ！", Fall!) had shipped
as "Die!" -- fitting the budget, but diverging from this same file's own
"Faaaaall!" at entry 10 for the identical verb root and from five other
shipped sections' independent convergence on "Fall" for this exact line;
fixed to "Fall" for consistency, which also resolves a near-collision with
entry 171's own forced "Die" (budget 3, 沈め/Sink!, too tight for any closer
synonym). Two "大佐"/Colonel lines (85, 87) had budget slack and were
unified from the budget-forced "Boss" used elsewhere in the section to
"Colonel" for internal consistency; three others (182, 193, 213) are
genuinely too tight for "Colonel" and keep "Boss". Quality comparable to
the cleaner prior Codex sections (097's 8/183), well clear of the worst
(91's 24/379, 166's 27/189). `python tools/check_voice.py
work/voice/answer/063.json`: 0 problems, 171 of 171 answered. Not yet
merged into `translation/`.

**Voice: section 146 is Boss piloting Boss Borot (Great Mazinger's
crossover arc), 173 lines** -- Codex draft, Sonnet-reviewed. Brief filed
unit Unicorn Gundam / pilot Banagher Links via a weapon-name match, score
1.0, and flagged the match itself as middling, citing section 8's
Strike Freedom/Kira misfile as a precedent -- wrong here too: nothing in
the section names Banagher, the Unicorn, or NT-D. Content is unmistakably
Boss, the delinquent gang leader who pilots the converted work robot Boss
Borot (`source/library/pilots.json` i=197, CHFN/CHNN both "ボス"): entry 2
self-declares in full ("Hear this! I'm Boss Borot!"), entry 5 gives the
canonical gag that even the author doesn't know his real name (matches
pilots.json's bio verbatim), he names his subordinates Nuke and Mucha
(17/125/218, pilots.json i=198/199, both "ボスの子分"), his mecha and home
base "Boss Borot" / "Kurogane-ya" throughout, and the section's back half
(167-222) is the "Kurogane Five" role call naming Cross, Django, Sensei,
Yasu and Kikunosuke/Okiku individually -- all five already in
`analysis/glossary.json`, including the お菊/Okiku (CHNN) vs 菊ノ助/
Kikunosuke (CHFN) split for the same character (zukan_id 210). Recorded
under "146" in `analysis/voice_identity.json`. Not confirmed by a
screenshot.

Found and fixed 19 deficient lines, run through `tools/check_voice.py` to 0
problems:

- **Reversed tone**: entry 10, jp "うるせい！ 見りゃわかる！" (an irritated
  "Shut up! Obviously!" snapped at a subordinate who just yelled "enemy!")
  shipped as the agreeable `"Yeah, I see!"`, inverting a gruff dismissal
  into assent -> `"Shut it! Duh!"`. Entry 129, jp "磨いたのは俺達なんスけど
  …" (a subordinate's muttered, ironic correction -- "well, WE were the
  ones who polished it") shipped as the triumphant `"We did it..."`,
  flipping a grievance into a boast -> `"We buffed..."`.
- **Dropped names**: entry 90 ("お前はすっこんでな、兜！", telling rival
  Kabuto by name to stay out) shipped nameless as `"Stay out!"` ->
  `"Out, Kabuto!"`. Entry 94 ("どうした、兜！ らしくねえぞ！") shipped as
  `"What's wrong?!"`, dropping both the name and adding a "?" the Japanese
  never has -> `"Odd, Kabuto!"`. Entry 180 ("お菊さん！") shipped as
  `"Kiku!"`, the wrong half of this project's own established Okiku/
  Kikunosuke name split -> `"Okiku"` (budget 5 has no room for the "!").
  Entry 120 ("俺もボロットも 頑丈さには自信があんだよ！", both Boss and his
  mecha are tough) shipped as the mecha-less `"Both\nbuilt tough!"` ->
  `"Me, Borot\nboth tough!"`, restoring the name this project already
  abbreviates to elsewhere in this same file (145, 165, 202).
- **Idiom/joke flattened**: entry 22 ("化け物は俺様が退治してやるぜ！", I'll
  personally exterminate the monster) shipped generic as `"Move!\nI'll
  handle it!"`, losing the monster -> `"Move it!\nMonster's mine!"`. Entry
  25 ("相手が機械獣だからって、ビビんなよ！") dropped the established
  "Beast"/"Mechabeast" term entirely -> `"Don't fear it!"` became `"Don't
  fear Beasts!"`. Entry 30's ラスボス pun (calling an enemy the video-game
  "last boss" and daring them to fight "our" Boss instead) shipped as the
  pun-less `"Big boss?\nFace our Boss!"` -> `"Last boss,\nFight Boss!"`.
  Entry 21 had budget to spare (28) but shortened the established
  "Mechabeast" call-out to bare `"Beast!"` -> `"Mechabeast!\nFace Boss
  Borot!"`.
- **Wrong-half drop**: entry 124 ("こ、この野郎！ やったな～！", cursing the
  attacker AND acknowledging the hit landed) kept only the curse as
  `"Y-you jerk!"` -> `"Y-you got me!"`, restoring the actual hit-taken
  content. Entry 207 ("ちょいと痛えが、男は我慢！", it stings but a man
  endures) shipped as the shrugging, unpunctuated `"Pain? So what"` ->
  `"Men endure!"`, restoring both the assertion and the Japanese's closing
  "！".
- **Punctuation mismatched despite spare budget**: entry 184 ended "！"
  but shipped a "？" that isn't in the Japanese, turning an assertive
  challenge into a genuine question -> `"Who's stronger?"` -> `"Who's
  stronger!"`. Entry 139 ("あんな、おっかない奴はお断りですよ～！", no
  thanks to that scary guy) shipped with an invented "？" and lost the
  decline -> `"Not that scary guy!"` -> `"No to scary guys!"`. Entry 4
  ("こちとら、喧嘩で負けるわけには いかねえんだよ！") shipped as `"I won't
  lose a fight!\nNo!"`, tacking a dangling non-sequitur onto the line break
  -> `"I never\nlose a fight!"`. Entry 137 dropped its closing "！" with a
  spare character available -> `"Can't help it"` -> `"Can't help!"`. Entry
  185 added a mid-line "！" the Japanese doesn't have while still missing
  the closing one -> `"We fight too!\nWith Borot"` -> `"We fight,\nwith
  Borot!"`. Entry 197 ("こうなるとわかってるのが辛いのよねん…", the pain of
  already knowing how this ends) shipped as the generic `"Losing
  hurts..."` -> `"I knew it'd hurt..."`, restoring the foreknowledge and
  the Japanese's trailing "…" instead of an invented "!".

**Voice: section 148 is an unnamed Martial cult soldier (VOTOMS: Shining
Heresy), 163 lines** -- filed as Black Getter / Ryouma Nagare via a
weapon-name match, score 3.0 (the brief's own middling-score warning, the
same class of match that was flatly wrong for section 8). Wrong: no Getter
Robo content anywhere. The glossary terms in the brief (Chirico Cuvie,
Martial, Teitania, Mithril, Chirico) are all VOTOMS: Shining Heresy terms
per `analysis/glossary.json`, and the content confirms it independently --
the speaker vows to protect a "猊下" (His/Her Eminence, the Pope) and
addresses "Teitania-sama" with deference as someone they guard and fall back
to protect, not as Teitania herself (she is a named pilot with her own
dedicated section, 110). The speaker invokes the Martial doctrine
repeatedly and reacts with religious awe to "the Untouchable" (触れ得ざる者,
the epithet this project already shipped for Chirico Cuvie in section 110),
naming him directly at entry 217 ("Th-this is Chirico Cuvie!"). No
self-introduction ties the voice to one of the five named Martial pilots in
`pilots.json` (Teitania, Viacheslav da Montewells, Pope Theo VIII, Guno,
Ilin Noskowitz) -- this is the faction's generic rank-and-file soldier,
fighting a multi-crossover battle against Gundam, Mithril mercenaries (FMP),
Black Knights/KMF (Code Geass) and Quentian mercenaries (VOTOMS). Recorded
under "148" in `analysis/voice_identity.json`; sections 149 and 150 are
~99% verbatim twins per the brief and are recorded to ship this same
English by propagation once merged. Codex draft, Sonnet-reviewed line by
line; fixed 9 of 163 lines. Entry 15 ("闘争こそ、我らマーティアルの教義…！",
struggle IS our doctrine) had shipped with subject and predicate swapped,
"Martial is war!"; fixed to "War is our creed!". Entry 36 (触れ得ざる者, the
project's own established "Untouchable" epithet, correctly used elsewhere in
this same draft at entries 92/184 and 150/264) had shipped as the generic
"None untouchable!"; fixed to "No Untouchables!" to keep the term. Entry 52
("まずは戦艦を落とす！", I'll sink the warship first) had shipped as "Drop
ship!", reading as the sci-fi noun rather than a verb clause; fixed to "Sink
ship!". Three bare-noun lines had lost their verb: entry 160 ("秩序の盾に続く！",
I follow the Shield of Order) shipped as the fragment "To Order"; fixed to
"Follow!". Entry 226 ("ガンダムめ！　噂以上の力だ！", damn Gundam, power beyond the
rumors) shipped as the flat possessive "Gundam's power"; fixed to "Strong
Gundam!". Entry 251 ("まだだ！　任務を全うするまでは…！", not until I complete my duty)
shipped as the dangling "Not yet! My duty"; fixed to "Duty isn't done!".
Entry 258 ("い、遺憾ながら機体を破棄する！", r-regrettably I must abandon the unit)
dropped its stutter, shipping as the flat "I abandon unit" with no closing
mark, inconsistent with this draft's own stutters elsewhere (entries
118/123/141/145); fixed to "I-I abandon it!". Entry 167 ("何故だ！？　何故、反撃
できない！？", why can't we counterattack) had shipped as "Why?! Why not?!",
dropping "counter" (already used at entry 58's "Now counter!") even though
the brief's own priority is to drop a punctuation mark before a word; fixed
to "Why?! No counter!" (one fewer "?", same budget). Entry 219 ("さすがは
クエント人！", as expected of a Quentian) had shipped as "A Quentian!\nNo easy
foe!", the only "-ian" form against this project's established bare "Quent"
(voice_088/115/204/205/206); fixed to "Quent!\nNo easy foe!". All fixes fit
their existing budgets. Quality comparable to the better prior Codex
sections (097's 8/183), well clear of the worst (91's 24/379, 166's
27/189). `python tools/check_voice.py work/voice/answer/148.json`: 0
problems, 163 of 163 answered. Not yet merged into `translation/`.

**Voice identity backfilled for sections 204/205/206.** All three ship
(Burglarydog / Chirico Cuvie, per `source/library/robots.json` i=29 and the
sections' own translation headers) but had no `analysis/voice_identity.json`
entry; 205 and 206 are near-verbatim twins of 204.

**Tactical Situation and System Settings pages translated.** Added turn,
funds, Z-Chip, forces, team/unit count, acquired-parts and SR status labels.
Both settings pages now have English titles, map-display and audio options,
and all 28 corresponding option descriptions through the UTF-8 label path.
Settings-update confirmations are translated too. Existing roster and small
movement-label changes remain included in the pending build.

**Voice: section 205 ships** -- 167 of its 168 lines were already carried by
the corpus (a twin of a shipped set), and the one remaining line
(「この俺がガンダムと やる事になるとはな…！」, budget 22) was hand-filled as
"Me, against / a Gundam?!". 186 sections.

**Ally/enemy team rosters translated.** Added exact bracketed Ally List and
Enemy List headings, Mothership, Target Drone and Team 0-9 labels. The Team
column heading supports split-letter drawing; joined matches now require a
string boundary so Team cannot swallow numbered names or Team Setup.
Restricted movement labels (Air/Grd/Wtr Only and Air/Wtr Only) use the terrain
cap-11 font, adding an Only cell at U+E017 / cp932 0x86CF. Seven original
executable labels keep their byte lengths, terminators and cell counts.

**Movement types use the small terrain font.** Unit Info and other movement
rows now assemble Air / Grd / Wtr / Und from the existing cap-11 terrain
cells. Three executable tables of standalone 空 / 陸 / 水 / 地 are patched
in place, retaining each character's two-byte size and padded slot. This
covers runtime-composed rows whose numbers, slashes or dash variants prevent
the old four-character hook entries from matching. Numeric Move values,
dash slots and global Japanese glyphs are unchanged. Original table contents
are checked before patching and all 12 replacement slots are read back.

**Spirit names aligned with the user's Wiki reference.** Names now follow
https://superrobotwars.fandom.com/wiki/Spirit_Commands by Japanese identity:
Wall, Persist, Zeal (覚醒), Fighting Spirit (闘志), Vigor (根性), Guts
(ド根性), Fury, Luck, Gain, Disrupt, Bravery, Faith, Bonds and Revival.
Plus variants and quoted names in spirit/part/ability descriptions follow
the same mapping. Z3's effect values and durations are preserved. The status
cells now read Wa/Pe/Ze/Fs/Fu/Lu/Ga/Di as appropriate, retaining the user's
mixed case and corrected letter spacing. Spirit full-name slots get their
own RPW overrides so Assail no longer inherits a shared weapon's Charge.
See `docs/SPIRIT_NAMES.md` for the old/new mapping and accepted aliases.
September 26 correction: Akurasu's Z3-specific names supersede Fighting Spirit
(闘志) with Fury and Fury (直撃) with Break; their cells now read Fu / Br.

**Attack selection and battle preview translated.** Center Attack / Wide
Attack, Ctr. (Counter), Support, Spirit, Anim: OFF / ON, Action, and Start
Battle now have exact UI hooks; the executable's Advanced AI pilot label
and Start Battle string use the UTF-8 channel. The two enemy spirit-strip
copies retain all 17 cells and their slash separator, with the same mixed-case
abbreviations as the ally strip and a new `An` cell for Analyze (U+E016,
cp932 0x86CE). The existing atlas mapping is reused for this rebuild.

**Voice: section 161 is Malloy Direzza piloting Aquarion Gepard, 177
lines** -- Codex draft, Sonnet-reviewed. Brief filed this as Darry -- wrong;
Darry (ダリー, glossary zukan_id 314) is an unrelated Gurren Lagann
character. Confirmed from content as Malloy Direzza (モロイ・ドレッツァ,
zukan_id 373): he self-names in full at entries 20/77 (shared) and 179
("モロイ・ドレッツァ"), his own machine is named directly at 108/144
and 217 ("やるぜ、ゲパルト！"), and his Element ability is named
throughout as 脆弱力/Fragility (6, 19, 76, and the doubt/reassurance pair
at 145/184), matching his bio in source/library/pilots.json (zukan i=373).
Same ensemble-bark pattern as the rest of the Aquarion cluster (009, 073,
090, 101, 164): the file bundles reply lines from Crea Dolosera (title
addresses at 21/78/134/158/200), MIX, Yunoha Thrul, Shrade Elan, Sazanka
Bianca and Amata Sora, none misattributed. Recorded in
`analysis/voice_identity.json` under "161". Not confirmed by a screenshot.

Found and fixed 24 deficient lines, run through `tools/check_voice.py` to 0
problems:

- **Reversed subject/direction**: entry 21, jp "クレア理事長、行きます
  ！" (Chairwoman Crea, I'm going!, first-person humble 行きます addressed
  to her) shipped as `"Crea, go!"`, readable as an order directed at Crea
  rather than the speaker's own departure -> `"Crea, I go!"`. Entry 129, jp
  "回避成功です、モロイさん！" (evasion successful, Mr. Malloy! -- a
  cadet's own status report to him) shipped as `"Malloy dodged"`, crediting
  Malloy himself with the dodge instead of the speaker -> `"Dodged, sir!"`.
  Entry 157, jp "何言ってる！？　俺じゃなかったら直撃だったんだぞ！"
  (what are you saying?! If it hadn't been me, it would've been a direct
  hit! -- a counterfactual about himself) shipped as `"What?!\nAnyone else
  got hit!"`, asserting an ally actually took a hit that never happened ->
  `"What?!\nOr I'm hit dead-on!"`. Entry 165, jp "くっ…！　避けた方向へ
  来たか！" (it came toward the direction I dodged to?!) shipped as the
  ambiguous `"Dodge read!"`, readable as him reading someone else's dodge
  -> `"My dodge read!"`. Entry 195, jp "わかっている！　これ以上はやらせ
  ん！" (I know! I won't let them do any more!) shipped as `"I know! I'll
  stop!"`, readable as Malloy stopping his own action -> `"I know! Stop
  them!"`.
- **Idiom mistranslation**: entry 101, jp "俺は意外と熱い男なんだよ…！"
  (I'm actually a surprisingly passionate/hot-blooded guy) shipped as `"I'm
  a hot man!"`, which in current English reads as a claim of physical
  attractiveness rather than passion -> `"I'm fired up!"`. Entry 149, jp
  "そうだな。俺にしては、つまらんミスだ" (yeah, for me that's a
  dumb/careless mistake) shipped as `"A dull mistake."`, where "dull" reads
  as boring rather than careless -> `"Yeah, dumb mistake"`.
- **Flattened bite / dropped content**: entry 131, jp "すごい！　見直した
  よ、モロイ！" (amazing! I've reassessed you, gained new respect for you,
  Malloy!) shipped as generic `"Great, Malloy!"`, losing the
  changed-my-opinion idiom -> `"Respect earned!"`. Entry 145, jp "この程度
  でひるむほど、俺の心は脆弱ではない！" (my heart isn't so fragile that
  I'd flinch at this level!) shipped as `"No flinch!\nHeart firm!"`, losing
  the callback to his own Element ability's name (脆弱/Fragile) ->
  `"No flinch!\nNot fragile!"`; its companion self-doubt line, entry 184's
  "脆弱なのは、俺の心なのか…！？" (is it MY HEART that's fragile...?!),
  had the same drop, `"Damn!\nWeak at heart?!"` -> `"Damn!\nAm I
  fragile?!"`, keeping the pun paired. Entry 172, jp "俺の事より、今は敵
  に集中しろ" (forget about me, focus on the enemy now) shipped as the
  fragment `"Foe, not me!"` -> the clearer imperative `"Focus the foe!"`.
  Entry 193, jp "シュレード！　最後の力を俺に貸してくれ！" (Shrade! Lend
  me your last strength!) shipped as `"Shrade!\nLast strength!"`, dropping
  the actual verb for a bare descriptor -> `"Shrade!\nLend strength!"` at
  no extra cost. Entry 217, jp "やるぜ、ゲパルト！" (let's do this,
  Gepard!, addressing his own mecha by name) shipped as bare `"Do it!"`,
  dropping the only named address to his own machine in the file ->
  `"Gepard!"`. Entry 26, jp "大人しく自分達の世界に帰るんだな…！"
  (obediently go back to your own world) shipped as `"Go to your world!"`,
  dropping the "back" (return to origin) sense -> `"Back to your world"`.
- **Ungrammatical fragment**: entry 52, jp "全ミサイル！　発射！" (all
  missiles! Fire!) shipped as the broken `"Missile go"` -> `"All fire!"`.
  Entry 168, jp "わかっている！　次はかわしてみせる！" (I know! Next
  time I'll dodge it!) shipped as the dangling noun fragment `"I know!
  Next dodge"` -> `"Noted! Dodge next!"`. Entry 205, the file's one
  meta/fourth-wall joke line ("プレイヤーの勉強する決意、仕事に行く決意
  を砕いている。これでゲームを続ける気になるはずだ" -- it's crushing the
  player's resolve to study and to go to work; this should make them want
  to keep playing the game) shipped as the ungrammatical `"Study will,
  work will - crushed. Keep gaming"` -> the complete sentence `"Crushes
  study and work resolve. Keep gaming."` at the same 44-cell cost. Entry
  54, jp "行け、バイバイ・ミサイル！" (go, Bye-bye Missile! -- his own
  jokey nickname for the attack) shipped as generic `"Go, Missile!"`,
  losing the joke entirely -> `"Bye, Missile!"`.
- **Title consistency**: entries 134/158/200 all address Crea by her title
  理事長 and had shipped it as "Director" (`"Thanks, Director"`,
  `"Director, OK?"`, `"Director, to end!"`); translation/voice_073.json
  (Crea's own shipped section) establishes "Chair" as the project
  convention for this title and calls for later sections to match it ->
  `"Thanks, Chair"`, `"Chair, OK?"`, `"Chair, to end!"`.
- **Idiom polish**: entry 187, jp 一か八か (an all-or-nothing gamble, the
  idiom's literal source) shipped as the looser paraphrase `"Now\nOne last
  gamble!"` -> the closer idiom match `"Now\nAll or nothing!"`, same cost.

Everything else in the 177-line file read as faithful, correctly registered
(Malloy's dry, composed tone kept distinct from the more excitable cadets'
reply lines), and within budget on the first pass; every name checked out
against katakana with no swaps found. `python tools/check_voice.py
work/voice/answer/161.json`: 0 problems, 177 of 177 answered (post-fix).

**Voice: section 153 is Marida Cruz piloting the Kshatriya (Gundam UC),
174 lines** -- Codex draft, Sonnet-reviewed. Brief filed this as Amuro Ray --
wrong; no White Base, no RX-78, no Char Aznable-era content anywhere. She
self-declares in full at entry 3 ("マリーダ・クルス、攻撃を開始する！",
"Marida Cruz, commencing attack!", repeated at 135/151/302) and names her
own mobile suit repeatedly and only as the Kshatriya (82, 216, 247, 283,
286), whose funnels -- absent from Amuro's RX-78 -- run entries 113-130.
She addresses Suberoa Zinnerman only as "マスター" (Master), the honorific
already established for his Garencieres crew in section 66 (183, 194, 281,
282, 285, including a direct apology at 285), names and fights alongside
Gilboa (184, 195), Gyunei and Quess (187-188, 198-199) of the Sleeves'
Personal Guard, and runs her entire duel arc against Banagher Links by
name (73-75, 190, 201, 221-222, 260-261, 287 -- matching sections
128/130's already-shipped Banagher/Unicorn content), including the beat
where she notices something is wrong with him mid-fight (287) and the line
naming her own nature as an enhanced human (265, matching the "Enhanced"
term already shipped in translation/voice_128.json). Recorded in
`analysis/voice_identity.json` under "153". Not confirmed by a screenshot.

Found and fixed 18 deficient lines, run through `tools/check_voice.py` to 0
problems:

- **Reversed direction/tense**: entry 9, jp "読めているぞ！" (I've already
  read/anticipated it) shipped as the forward-looking `"Predict"`,
  inverting her confident "already read you" into an uncertain forecast
  and breaking consistency with entry 11's `"All read!"` for the same
  読む root -> `"Read!"`. Entry 88, jp "こんなものと戦う事になるとは…！"
  (an exclamation of disbelief, not a question) shipped as `"Fight
  this...?"`, turning disbelief into a genuine question -> `"Fight
  this...!"`.
- **Idiom/meaning mistranslation**: entry 73, jp "バナージ…！　手加減は
  しない…！" (Banagher...! I won't hold back...!, a vow of no mercy
  despite their connection) shipped as `"Banagher, brace!"`, which reads
  as a warning to get ready rather than her vow of no restraint ->
  `"No holding back!"` (name traded away, the 16-cell budget could not
  hold both). Entry 204, jp "この失態は、必ず取り返す…！" (I will
  definitely make up for this blunder) shipped as the morally-loaded
  `"I will atone!"`, overstating a practical military recovery into
  penitential melodrama out of character for her flat register ->
  `"I'll fix this!"`. Entry 244, jp "小賢しい真似を…！" (a cunning/sly
  trick, not a trivial one) shipped as `"Petty act"`, dropping the
  "clever" half for mere smallness -> `"Sly trick"`.
- **Dropped content the budget had room for**: entry 74, jp "覚悟はいい
  か、バナージ！" (are you prepared, Banagher?!) shipped as bare
  `"Banagher?!"`, discarding the entire challenge for a surprised-sounding
  name-check -> `"Prepared?!"` (name traded for content in the 12-cell
  budget). Entry 116, jp "落とせ、ファンネル！" (bring it down, Funnel!)
  shipped as the bare `"Funnel!"`, identical in content to the unrelated
  entry 114 and dropping the order outright -> `"Down now!"`. Entry 121,
  jp "行け、フィン・ファンネル！" (go, Fin Funnel!) shipped as `"Fin
  Funnel!"`, dropping the imperative that fits the budget exactly ->
  `"Go Fin Funnel"`. Entries 195 ("ギルボア、後退を！", Gilboa, retreat!)
  and 201 ("バナージ…！　退け！", Banagher...! Fall back!) both shipped as
  the bare name, conveying no part of the actual order -> `"Retreat!"`
  and `"Fall back!"` (the 10-cell budget cannot hold name plus command in
  either line). Entry 257, jp "ガンダム…！　データ以上か…！" (marveling
  that it exceeds her recorded data) shipped as the near-meaningless
  `"Gundam... More?"` -> `"Beyond data?!"`, restoring the one specific
  detail in a section that says "Gundam" dozens of times. Entry 265, jp
  "強化人間の私では奴に勝てないのか…！？" (as an enhanced human, can I
  not beat him?!) shipped as `"Even I can't win?!"`, dropping her core
  identity term entirely -> `"Enhanced can't win?"`, restoring the
  already-established "Enhanced" term from translation/voice_128.json.
  Entry 287, jp "…どうした？　らしくないぞ、バナージ" (...What's wrong?
  That's not like you, Banagher -- her one line of open personal
  familiarity with him) shipped as the vague `"Odd, Banagher?"`, losing
  the entire "that's not like you" observation that is the point of the
  line -> `"Not you, Banagher?"`, fitting the 18-cell budget exactly.
- **Consistency/capitalization**: entry 189 shipped the established unit
  term as lowercase `"Aid guard"` where entry 200's `"Guard cover"` (same
  親衛隊 term) capitalized it -> `"Aid Guard"`. Entry 120, jp "ファンネル
  からは逃れられん…！" (there's no escaping the Funnels) shipped as the
  incomplete-reading `"Funnel catches"` -> `"Can't escape!"` for a
  cleaner, literal negation. Entry 190, jp "バナージ、続くぞ…！"
  (Banagher, I'm following!) shipped as the imperative-reading `"Follow
  on!"`, which could misread as ordering a third party -> `"I follow!"`
  (name dropped, 10-cell budget too tight for both). Entries 66 and 285
  had spare budget cells left unused despite the Japanese ending "！";
  added the missing exclamation mark to both (`"Not down! Then"` ->
  `"Not down! Then!"`; `"Sorry, Master"` -> `"Sorry, Master!"`).

Everything else in the 174-line file read as faithful, correctly
registered (flat, dutiful, self-effacing -- no swagger, no melodrama
beyond the one overcorrected line above) and within budget on the first
pass.

**Voice: section 123 is Hathaway Noa (Char's Counterattack -- Bright's
teenage son, a nervous Jegan/Nu Gundam-era Federation pilot)** -- Codex
draft, Sonnet-reviewed, 176 of 176 lines. The claimed attribution was
correct: he self-names in full ("ハサウェイ・ノア、行きます！", entries
14/60/82/94) and self-addresses mid-panic by name (222, "Calm down...!
Calm down, Hathaway..."). He calls Bright "Dad" repeatedly, including
ordering his own father's flagship to retreat (159, "Ra Cailum, back!"),
references his civilian Medd craft and its unpaid loan (3, 221), his
mother and Cheimin waiting on Earth (21), and measures himself against
Amuro as mentor/idol (15, 26, 147). Names Kamille, Katz and Otto
(152-154, 163-165), all Ra Cailum/AEUG crew of this era, and carries an
extensive, canon-consistent Quess thread (pleading with her to stop,
agonising over rescuing her, addressing "Char"/"Full Frontal" directly).
Recorded in `analysis/voice_identity.json` under "123".

Found and fixed 9 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Mid-clause/mid-word truncation**: entry 69 ("大丈夫、僕にだって出来
  るさ…！", "It's fine, I can do it too...!") shipped as the dangling
  "I'm fine. I can", cut off before completing the thought; fixed to
  "I can do it too". Entry 148 ("父さん、後は任せて！", "Dad, leave the
  rest to me!") shipped as the equally dangling "Dad, I can"; fixed to
  "Leave it!", a complete imperative within the same 10-cell budget.
  Entry 170 ("あ…あ…！　敵が行っちゃう！", dismay at the enemy getting
  away) shipped as "Ah... ah... go", reading as "going" truncated
  mid-word and dropping the subject entirely; fixed to "It's
  escaping!".
- **Flattened bite / wrong-half drop**: entry 111 ("フル・フロンタルの
  おまけだろ！", dismissing the mystery pilot as no more than an extra
  tagging along with Full Frontal) shipped as the bare "Full Frontal?!",
  discarding the entire insult and reducing it to a name-check already
  covered by the preceding line; fixed to "Frontal's pawn!". Entry 162
  ("クェスを守るんじゃないのかよ！", an accusation -- "weren't you
  supposed to protect her?!") shipped as the flat "Protect Quess?!",
  losing the accusatory aim; fixed to the sarcastic "Some protector!",
  which keeps the bite in budget. Entry 315 ("一対一なんだ！　自分でや
  らなきゃ！", two clauses: it's one-on-one, and he has to do it
  himself) shipped as "It's one on one!", dropping the second clause
  outright; fixed to "1v1! On my own!" to restore both halves.
- **Reversed direction**: entry 209 ("顔を見れば、そんなイライラすぐに
  忘れるよ！", "If you see my face, you'll forget that irritation right
  away!" -- Hathaway telling Quess that seeing him will calm her anger)
  shipped as "Your face\ncalms my rage", swapping whose face and whose
  rage; fixed to "My face\ncalms your rage" within the same budget.
- **Idiom risk**: entry 123 ("今は戦うしかないけど、いつかは…！", "I have
  no choice but to fight now, but someday...!") shipped as "Fight now.
  Later", where "Later" reads as the English farewell slang and flips
  Hathaway's earnest, trailing hope into a smug sign-off; fixed to "For
  now. Someday".
- **Ambiguous retreat order (same failure class as section 151's "TDD-1
  out")**: entry 163 ("カミーユさんは後退を！", ordering Kamille to fall
  back) shipped as "Kamille out", reading as eliminated/defeated rather
  than retreating; fixed to "Kamille go!".

`python tools/check_voice.py work/voice/answer/123.json`: 0 problems,
176 of 176 answered (post-fix). Quality vs prior Codex sections:
middling -- 9 of 176 needed correction, none a meaning inversion or a
swapped character identity, but two mid-sentence truncations (69, 148)
and one reversed-pronoun direction (209) are worth flagging as this
drafter's failure modes here.

**Voice: section 151 is Melissa Mao (Full Metal Panic!'s Mithril SRT
sergeant major, callsign Urzu 2)** -- Codex draft, Sonnet-reviewed, 180
of 180 lines. The claimed attribution was correct: she self-names her
callsign "Urzu 2" directly (15, 190, 192-193, 201, 309), addresses Kurz
Weber by name (20, 198, 210, 236, 237, 261) and Sousuke Sagara by name
(199, 210, 236, 311, 313), is called/calls herself "big sis"/Mao (44,
63, 194, 224), namedrops Tessa (76) and invokes Mithril (229, 279),
gives TDD-1 crew orders (192, 203), and closes with a beer line (80)
matching the glossary's "loves beer more than anything" note. Recorded
in `analysis/voice_identity.json` under "151".

Found and fixed 13 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Wrong project spelling**: entries 15, 190, 193, 201, 309 all
  shipped her callsign as "Uruz" (letters transposed) against this
  project's established "Urzu" (translation/voice_072.json, most stage
  dialogue) -- fixed all five to "Urzu".
- **Meaning reversal**: entry 63 ("見た目にビビるマオ姐さんじゃないよ
  ！", "I'm not the kind of big-sis Mao who gets scared by looks!")
  shipped as "Mao fears freaks!", the exact opposite of her declared
  fearlessness; fixed to "Mao's not scared!".
- **Tone flip risk**: entry 271 ("相当の訓練をしたみたいね…！",
  acknowledging real, considerable training) shipped as "Some
  training!", reading as a dismissive backhand instead of the intended
  respect; fixed to "Well-trained!".
- **Dropped clause**: entry 199 ("ご苦労、ソースケ！　後は任せな！",
  "Good work, Sousuke! Leave the rest to me!") shipped as "Nice,
  Sousuke!", losing the entire second half; fixed to "Nice, my turn!"
  to restore the "leave it to me" idea within budget.
- **Ambiguous order misreads as status report**: entry 203 ("ＴＤＤ１
  は後退を！", ordering TDD-1 to fall back) shipped as "TDD-1 out",
  which reads as "TDD-1 is destroyed/signing off" rather than a
  retreat order; fixed to "TDD-1 go!".
- **Register/subject drift**: entry 32 ("噂じゃかなりヤバいって話だけ
  ど…！", commenting on the opponent's fearsome reputation) shipped as
  "Real bad news...!", reading as alarm about her own situation rather
  than a taunt about theirs; fixed to "Big bad rep, huh!". Entry 261
  ("ヤバ！　クルツ達に示しがつかない！", "I can't set an example for
  Kurz and the others!") shipped as "Kurz can't know!", turning
  embarrassment-in-front-of-Kurz into a secrecy plot; fixed to "No
  face for Kurz!".
- **Garbled/ungrammatical English**: entry 30 ("余所見してっから、こう
  なる！", blaming the target's inattention) shipped as the broken
  "Eyes off: lose"; fixed to "Careless, huh!".
- **Weakened idiom/instruction**: entry 194 ("後はマオ姐さんに任せな
  さいって！", "just leave the rest to big sis Mao!") shipped as the
  boastful "Mao takes it!" instead of the reassurance intended; fixed
  to "Leave it to Mao!". Entry 0 ("さ、仕事、仕事！", psyching herself
  up for a job -- her recurring mercenary "it's just work" framing)
  shipped as the generic "Go! Go!", losing that framing entirely;
  fixed to "To work!".
- **Unused budget/punctuation and naturalness**: entry 204 ("ベン、逃
  げて！", "Ben, run!") shipped as the vaguer "Ben, go"; fixed to "Ben
  run" for clarity. Entry 270 ("…整備班の小言が聞こえてきそう…！")
  ended without its closing "!" despite budget room; added it. Entry
  317 shipped the redundant, choppy "Good! Honest! Player, bye!";
  fixed to "Honest! See ya, player!", echoing her own "See ya!" (314)
  and dropping the doubled praise.

`python tools/check_voice.py work/voice/answer/151.json`: 0 problems,
180 of 180 answered (post-fix). Quality vs prior Codex sections:
comparable to the cleaner end of the range (section 097's 8/183,
section 054's 6/182) -- 13 of 180 needed correction, including one
outright meaning reversal (63) and one order-misread-as-status-report
(203), worth flagging as this drafter's recurring failure modes, but
nothing catastrophic (no swapped character identities, no mid-word
truncation).

**Voice: section 33 is Annalotta Stohls piloting the plain Diosc (SRW
Z3 original -- Gadlight Meonsam's adjutant in the Geminis)** -- Codex
draft, Sonnet-reviewed, 178 of 178 lines. The brief misfiled this as
Anti-Spiral/Granzeboma (section 30's identity); nothing in the content
matches that. Entry 0 (repeated at 81) and entry 151 self-name in full
("アンナロッタ・ストールス、攻撃を開始する！" / "このアンナロッタ、
敵にかける情けはない！"), she addresses Gadlight by name five times
(157, 158, 162, 218, 246) -- ordering, scolding, shielding and finally
apologizing to him -- and two lines (20, 216) protect "この子", her
unborn child with Gadlight per pilots.json's DSC2. The unit is named
"ディオスク" twelve times and never once "ディオスクＡ", distinguishing
this section from section 34 (same pilot, the commander's-model Diosc
A). Recorded in `analysis/voice_identity.json` under "33".

Found and fixed 8 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Dropped the entire apology**: entry 246 (「ごめんなさい…ガドライト
  …」, her line as she falls) shipped as bare "Gadlight..." -- the
  drafter kept the addressee and lost "I'm sorry", the actual content
  of the line. His name is already established by four earlier lines
  in the section; the apology is not recoverable from context. Changed
  to "I'm sorry..." (fits the 13-cell budget; the full name plus any
  apology word does not).
- **Idiom read backwards**: entry 163 (「いい戦術だ。見習わせてもらう
  ぞ」, "good tactic, allow me to take a lesson from it") shipped as
  "Lesson learned!", which in English reads as conceding a painful
  mistake, the opposite of her professional respect for an opponent's
  tactic she intends to adopt. Changed to "I'll copy that!".
- **Dropped term the file uses elsewhere**: entry 17 (「ジェミニスの誇
  り、ジェミナイドの意地を見せる！」) named both Geminis (the unit) and
  Geminaid (the people) but shipped as "Geminis pride\nour grit!",
  flattening Geminaid to "our" even though the section keeps "Geminaid"
  by name at entries 111 and 178. Changed to "Our pride,\nGeminaid
  grit!", same 25-cell budget.
- **Project-term drift**: entry 38 (「噂に聞く機械天使が相手とはな！」)
  rendered 機械天使 as "Machine angel!" where every other section using
  this term (voice_010/021/023/025/035/051/053/082) ships it as plain
  "Angel". Changed to "So, the Angel!".
- **Grammar broken by an omitted article**: entry 14 (「今だけは一人の
  人間として戦おう！」) shipped as "Fight as human!", missing the
  article "a" that "as human" needs to parse. Changed to "For now,
  human!", same 16-cell budget, without inventing an object the
  Japanese doesn't have.
- **Mocking rhetorical question flattened to neutral**: entry 168
  (「貴様の戦技は、その程度か」, "is that the extent of your skill?")
  shipped as the neutral "Your skill?", losing the contempt that
  matches the surrounding taunts ("Feeble", "Slug! Shame!", "Inept
  fool!"). Changed to "That's all?".
- **Dropped question mark where the Japanese asks and budget allowed
  one**: entry 194 (「ほう…ディオスクに当ててきたか」) and entry 224
  (「これが地球のスーパーロボットの力か！」) both end in か (rhetorical
  question) but shipped as flat statements ("A hit on Diosc", "Super
  robot power") with a spare cell going unused in both budgets. Changed
  to "A hit on Diosc?" and "Super robot power?".

**Voice: section 54 is Quatre Raberba Winner piloting Gundam Sandrock
(Gundam Wing / Endless Waltz)** -- Codex draft, Sonnet-reviewed, 182 of
182 lines. This task's own brief misfiled the unit as Kallen Kouzuki's
Guren; nothing in the content matches that. The speaker addresses all
four other Wing pilots by their glossary spellings mid-battle (Heero,
Duo, Trowa, Wufei), names his own mobile suit Sandrock directly across
a dozen lines, hesitates to fight Wufei as a friend (79-82/93-94), and
carries Quatre's canonical register throughout: polite -masu/-desu verb
endings, repeated apology before or after landing a hit, self-doubt
under damage, the character's signature unexplained tears (47), and an
explicit pacifist creed (175/184/186). Recorded in
`analysis/voice_identity.json` under "54".

Found and fixed 6 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Seeded twins left untranslated** (the checker's 3 flagged problems):
  entries 60/62 both shipped "This!", 130/134 both shipped "Yah!", and
  132/138 both shipped "Hah!" -- in each pair the drafter translated one
  member and left its pre-seeded twin untouched despite differing
  Japanese. Verified against the Japanese rather than adopting the
  drafter's own suggested fixes blindly: 60 (「このーっ！！」, an angry
  address at the target) -> "You!!", keeping 62 (「これでっ！」, "take
  this!") as "This!"; 134 (「これで！」, "with this!") -> "Now!",
  keeping 130 (「でいっ！」, a kiai grunt) as "Yah!"; 132 (「だあっ！」,
  a kiai grunt) -> "Dah!", keeping 138 (「はあっ！」, a closer phonetic
  match) as "Hah!".
- **Project-term drift**: entry 183 (「地球もコロニーも あなたの好きに
  はさせない！」) rendered コロニー as generic "space" where the
  project's already-shipped term (translation/voice_117-119.json) is
  "colonies" -- changed "Earth, space\nNot yours!" to "Both worlds\nNot
  yours!", which keeps both referents without the singular/plural
  mismatch a literal "colony" would force under the 23-cell budget.
- **Register flattened into slang**: entry 107 (「この戦いは 僕の宇宙に
  対する償いなんだ…！」) rendered 償い (atonement) as "my space debt",
  reading as flippant gamer slang against Quatre's solemn tone --
  changed "This war\nmy space debt" to "My war\natones to space".
- **Dropped vocative the exchange depends on**: entry 80 (「仕方あり
  ません。行きますよ、五飛！」) dropped "Wufei" though the preceding line
  (79) and habit of naming every ally by name elsewhere in this section
  both lean on it -- changed "So be it\nI come!" to "Then\nI come,
  Wufei!", which fits the 19-cell budget the original also had to fit.

**Voice: section 179 is the Takeo General Company Shuttle crew (Trider
G7), Umemaro Kakikouji chiefly with Touhachirou Kinoshita, Tetsuo Atsui
and Ikue Sunabara rotating in** -- Codex draft, Sonnet-reviewed, 183 of
183 lines. No weapon-table match was on file to override; identity is
confirmed straight from content -- entry 33 self-declares in full
(「ここは不肖、柿小路梅麻呂にお任せを！」, leave this to your humble
servant, Umemaro Kakikouji!), entry 77 self-declares Touhachirou
Kinoshita, and Tetsuo Atsui and Ikue Sunabara are each addressed
directly by title/name (常務/Mgr, 郁絵君/Ikue-kun) throughout -- matching
`source/library/pilots.json` i=1-4 and the officer roles already given
in `translation/library/pt_000.json`. This task's own brief misnamed the
clerk "Ikue Nomura"; the glossary's and library's actual spelling is
Ikue Sunabara (砂原郁絵), corrected in the identity record. Watta Takeo
(社長/"Boss") is addressed throughout but does not clearly self-voice any
line here -- he pilots Trider G7 itself in the separate `voice_173.json`;
this section is the crew's own Shuttle bark bank. Recorded in
`analysis/voice_identity.json` under "179".

Found and fixed 18 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Dangling orphan line-break** (a genuine truncation bug): entries 29
  and 59 both shipped literally ending in a bare `\n` with nothing
  after it -- 29's `21st Century Security\n` and 59's `Owe 21st Century
  Security!\n` each dropped their second line's content outright. The
  full glossary company name already consumes nearly the whole budget
  (the same trade-off already shipped in `translation/voice_192.json`
  entry 133), so both were fixed by dropping the dangling break: 29 ->
  `21st Century Security`, 59 -> `Owe 21st Century Security!`.
- **Entire line dropped for just the speaker's own name**: entry 33, jp
  "leave this to your humble servant, Umemaro Kakikouji!", shipped as
  bare `Umemaro Kakikouji!`, discarding the actual boast; fixed to
  `Kakikouji's on it!`. Entry 77, jp "did you see?! this Ultra C of
  Touhachirou Kinoshita's!", shipped as `Touhachirou Kinoshita\nC!` --
  dropping the "did you see" call-to-attention and mangling the stock
  idiom "Ultra C" into a stray floating "C!"; fixed to `See!\nKinoshita's
  Ultra C!`.
- **Idiom mistranslation**: entry 28, jp "you wretch, monster! I'll
  bring you to justice!", shipped as the vague, legalistic `Beast! Face
  law!`; fixed to `Beast! I'll punish!`. Entry 112, jp "honestly,
  President... you mustn't be so willful/spoiled", shipped as `Boss...
  Don't be greedy.`, swapping the actual vice (childish willfulness) for
  an unrelated one (avarice); fixed to `Boss, don't be selfish.`. Entry
  201, jp "please leave both sales and combat to us!", shipped as the
  unpunctuated fragment `Sales and war`, both dropping "leave it to us"
  and overscaling combat into "war"; fixed to `Sales, combat`.
- **Garbled/ungrammatical line**: entry 132, jp "I hope my office
  experience comes in handy...", shipped as the broken `Office skill,
  help`, reading as two disconnected fragments; fixed to `Office skill
  helps`.
- **Missing terminal punctuation against an exclaiming original**:
  entries 160 (`Missile.` -> `Missiles!`, re-differentiated from entry
  118's own `Missile!`), 161 (`Missile, fire` -> `Fire missile!`), 166
  (`Barrier! Wow` -> `Big barrier!`), 184 (`Beam! Go` -> `Beam!!`), 216
  (`Oho! A shake` -> `Oho! Shake!`). Entry 89, jp "even if we're hit like
  this, no problem, right Exec?", shipped as `That hit was fine.`,
  dropping the direct address to the Exec every other exchange with him
  keeps; fixed to `No harm done, Exec!`.
- **Unforced overclaim**: entry 219, jp "we did it!/we managed it!" (not
  necessarily a final victory), shipped as `Won! I won!`; fixed to `Did
  it! Yes!`.
- **Minor clarity/consistency**: entry 169's `Shuttle, firm, done!`
  (an ambiguous three-item list) repunctuated to `Shuttle, firm: done!`.
  Entry 171's `Sorry, yet again.` -- the Shuttle's own launch
  announcement, already established in `translation/library/rt_000.json`
  as opening with "Sorry for the disturbance as always" -- reworded to
  `Sorry, as always.` to match the shipped phrase. Entry 173's `Stay
  past line!` (ambiguous which side of the line is safe) fixed to `Stay
  behind line!`.

Quality: cleaner than the weaker Codex drafts on file (090/101-era,
B-/C+) -- most running jokes (the spoon-hiding gag at 25, the
salary/loan pun at 71, the delivery-service slogan at 230) survived
intact, and no swapped names or reversed scolding/threat direction were
found anywhere -- but the draft left two dangling orphan line-breaks,
dropped two speakers' own self-declared names for their boasts, and
lost several closing exclamation marks that had a same-cost fix
available. Landing around B/B+. `python tools/check_voice.py
work/voice/answer/179.json`: 0 problems, 183 of 183 answered.

**Voice: section 45 confirmed as the Nahel Argama bridge crew (Gundam
Unicorn), 183 lines** -- Codex draft, Sonnet-reviewed. Brief filed this as
unit Nahel Argama, pilot Otto Mitas, weapon-match score 1.0, and content
confirms it: gunnery orders address "each gun battery" and "this ship"
throughout, Mega Particle Cannon/Anti-Air Machine Gun call-outs appear where
they fit, and the station-readiness/save-quit exchanges are addressed to
"Captain"/"XO", never spoken in mobile-suit-pilot register. Section 44
(already shipped) is this section's twin -- entry 139 here is the identical
Japanese string as 44's entry 0, and the two sections' station-readiness/
save-quit blocks parallel each other almost line for line, confirming both
are companion bridge-crew sets for the same ship voiced by different
officers. Shipped generically with no invented officer name, matching 44's
practice. 9 of 183 lines corrected on review: entry 15 ("Newtype or not!" --
invented a false Newtype/non-Newtype binary, dropping the Enhanced Human
category the line names -- fixed to "No matter the kind!"); entry 21
("One Year War\nis over!" -- dropped the imperative that makes this an order
to prove it to the enemy through battle -- fixed to "Teach them\nwar's
over!"); entry 117 ("Use us!" -- flattened the self-sacrifice sense of
"this ship will become the shield" -- fixed to "Shield!", matching section
44's own choice for the identical construction); entry 119 ("They live!" --
reversed an active protective vow into a passive outcome -- fixed to "Save
them!", matching this section's own "Save Red Comet!"/"Save humanity!"
pattern); entry 161 ("Only a near hit!" -- dropped the relief/lucky-break
framing of the original -- fixed to "Lucky near-miss!"); entry 162 ("Minor
hit taken!" -- dropped the specific damage location this section otherwise
always keeps -- fixed to "Catapult, minor!"); entry 176 ("Damn Sleeves" --
left a cell of budget unused instead of closing the shout -- fixed to
"Damn Sleeves!"); entry 191 ("Nahel Argama! No" -- an unfinished
non-sequitur -- fixed to "Hold on, Argama!"); entry 195 ("Roger! Tell all"
-- reads as the noun "a tell-all" rather than a sentence -- fixed to
"Notifying all!"). Identity and full line-by-line review recorded in
`analysis/voice_identity.json` under "45". python tools/check_voice.py
work/voice/answer/045.json: 0 problems, 183 of 183 answered.

**Voice: section 97 is the Ptolemaios 2 bridge ensemble (Gundam 00), 183
lines** -- Codex draft, Sonnet-reviewed. Brief filed this as Gunbuster/Noriko
-- wrong, no Gunbuster content anywhere. Content is unmistakably the
Ptolemaios 2 bridge crew from the movie A Wakening of the Trailblazer, four
voices bundled in one file (this project's established pattern, e.g. section
13's Asuka/Misato): Sumeragi Lee Noriega, the tactical forecaster/commander,
carries a 予測/読み ("forecast"/"read") motif that pays off across the
section (entry 3 "if my prediction isn't wrong", entry 176 "they read us...
not bad", entry 189 "my read was wrong?!") and is addressed both as the
respectful "ノリエガさん"/Noriega-san (18, 155, 190) and the more familiar
"スメラギさん"/Sumeragi-san (209), kept distinct rather than collapsed to
one name; Mileina Vashti is the chirpy assistant operator, marked by a
です/ですぅ verbal tic on her tactical reports and calling her father,
mechanic Ian Vashti, "パパ"/Dad (160-161); Lasse Aeon is the blunt
helmsman, masculine ぜ/だ/ねえな endings, addressed by Sumeragi on a first-
name basis; Feldt Grace never speaks in her own chirpy register here but is
named as the source of tactical analysis (entry 6) and gives two flat,
formal damage reports with no verbal tic (152, 202) -- distinguishing her
plain register from Mileina's です tic is what confirms two separate
operators. All four Gundam 00 Meisters are named or unmistakably described
on-page (Setsuna F. Seiei, Lockon Stratos, Allelujah Haptism's signature
reflex/thought-fusion trait, Tieria Erde piloting Raphael Gundam per section
109's identity already on file), ruling out Gunbuster entirely. GN Missile,
GN Cannon and GN Field all appear correctly per translation/weapons.json.

Found and fixed 8 defective lines out of 183: two name-spelling errors
against this project's own romanizations (entry 139 "Aarde, sorry!" ->
"Erde, sorry!"; entry 220 "Aion, amazing!" -> "Aeon, amazing!" --
アーデ/アイオン are already shipped as Erde/Aeon, translation/name_pieces.json
lines 46/18/380); one dropped addressee restored within budget (entry 140
"Raphael retreats" -> "Erde, fall back!", Mileina's report to Tieria about
his own unit); two command/report direction flips, both a self-declared
ship action rendered as an order to someone else (entry 120 "Follow 00!" ->
"Following 00!", Sumeragi declaring the Ptolemaios will back up 00's attack,
not ordering Setsuna; entry 127 "Aid them!" -> "Rescue run!", Sumeragi
declaring she's heading to rescue allies); one flattened register (entry
164 "Took one!" -> "My bad, hit!", restoring Lasse's apologetic すまねえ);
one dropped tactical instruction (entry 177 "Wait, wait!" -> "Wait, lure!",
recovering 引きつけて/"lure them in" that had been reduced to a vague
repeated "wait"); and one dropped damage-tier callout (entry 197 "Right
side gone!" -> "Wrecked, right!", restoring the 大破/"severely wrecked"
status this project already renders as "Broken" in voice_177.json/
voice_178.json, alongside the located damage). Notably cleaner than several
prior Codex sections (91 had 24 defects out of 379 lines, 166 had 27 out of
189): none of the 8 fixes here were meaning inversions or swapped character
identities, and all were recoverable within their existing budgets.
`python tools/check_voice.py work/voice/answer/097.json`: 0 problems, 183 of
183 answered.

**Map COMMAND overlay completed.** The remaining ally/enemy selector pieces and
the live map-summary labels now go through the draw-time UI hook: the composed
selector reads `Ally / Enemy` in either selection state, while the two-line
counters read `SR Points` / `Turns` and `Z Chips` / `Funds`. The values and
separately drawn punctuation remain supplied by the game.

**Map-data unit panel translated.** The runtime-composed Team 4 label, support
attack/defense counters, Forest terrain name, DEF/EVD terrain bonuses, and
HP/EN regeneration labels now go through the draw-time UI hook. The panel's
17-cell spirit-status strip cannot hold ordinary English without moving its
per-status colour highlight, so its three exact FSSA copies are patched in
place to 17 private-use cells. Those cells rasterise larger, mixed-case,
two-letter labels (Va, So, Ze, Al, Gu, Iw, Fo, St, Ac, En, Me, Sn, As, Dh,
Ft, Ef, Cf) from the settled spirit names, one word per original kanji cell.
They use their own cap-16 face. The first enlarged version stretched narrow
pairs to a minimum width, spreading Ft/Ef/Cf apart while squeezing Me together.
Pairs now use a consistent two-texel gap between visible letter bounds, keep
natural widths when possible, and condense only to fit a 28-texel ink limit.
Each pair stays centred in its original status cell. The tiny-cell
codes are reserved from the general VWF pool as permanent atlas occupants.

**Tutorial pages re-condensed to actually fit the box.** The earlier
condensing pass (see below) still left 30 of the 95 `translation/tutorial_hook.json`
lines over the measured 66-letters-per-line width; every line has now
been re-measured (fullwidth-space indent and mid-line fullwidth spaces
each costing 2 letters, `{c1}`/`{/c}` costing 0) and the 30 overflowing
lines shortened to fit, meaning and numbers kept.

**Combat Record, Lecture Plates and the tutorial pages.** Combat Record
labels (通算獲得ＰＰトップ "Top PP Earned", 撃墜数トップ "Top Kills", 通算獲得資金
"Total Funds", ＳＲポイント "SR Points", エースパイロット "Ace Pilots",
～獲得エンブレム～, 獲得条件／装備効果, the two 『…』へ links), the five
emblem names and their conditions (Raise 15 Ace Pilots, 150 kills, 1200
PP, 15,000,000 funds, 55 SR Points) and the shop unlock conditions are
hooked. The Lecture Plate menu draws its ten numbered titles from the
executable's UTF-8 table, so they go through `translation/ui_utf8.json`
("1. The Tag Battle System" ... "10. Retrying"). The tutorial pages
themselves are one executable string per screen line
(`translation/tutorial_hook.json`, in UI_HOOK_FILES); lines with an
orange emphasis carry raw colour bytes (ASCII digit + 0x01 opens, a bare
digit closes) and their sentence-final 。 is a separate string, so the
hook encoder now passes a {cN}...{/c} token through as those raw bytes
(`eboot._encode_marked`) and 。 alone is hooked to ".". The EXT segment grew again, 256 KB -> 512 KB
(`EXT_SIZE = 0x80000`). In-game the colour-marked lines were followed by a
stray fragment of another line: the game draws such a line's
sentence-final 。 by reading THE NEXT STRING IN MEMORY, which under the
hook was whatever entry followed ours -- the encoder now places a "."
string right after the English of every colour-marked entry. The
tutorial lines were then re-condensed to the measured box width (about
66 letters at no indent, minus 2 per fullwidth space of indent; the
first pass allowed 78 and overflowed) -- that pass still left 30 of the
95 lines over width; a follow-up pass re-measured every line (counting
fullwidth spaces as 2 letters wherever they fall, not only in the
indent) and tightened all 30 to fit, with no lines over width
remaining. Combat Record: the emblem line is
composed at runtime as one string (name：condition), so the five
composites are translated -- they turned out to be UTF-8 strings in the
executable (the cp932 hook could not see them), so they went through
`translation/ui_utf8.json`, not the hook; 獲得条件： shortened to "Earned:" to clear its value. The ＜レコードライブラリー＞ heading occurs in no
text file at all (cp932 or UTF-8) -- a texture, like the other typeset
headings; it stays Japanese until the atlas pass.

**Lecture Plate tutorial pages translated.** `translation/tutorial_hook.json`
now carries the English for all ten topics (95 entries): the 60 plain-text
screen lines from `work/tutorial_src.json`, plus 35 more found by searching
the executable for the cp932 bytes of known emphasised phrases and walking
the surrounding NUL-delimited strings -- a second, separate block (file
offset 6986160-6987806) holding every orange-emphasis span and its plain
continuations, entirely missed by the plain-text extraction. That block
filled in bullets the extraction had silently dropped: page 1's
team-formation and average-Move bullets, the SR Point Hard/Normal
thresholds, both Tag Tension conditions, two more Maximum Break bullets,
and the Combo Gauge's five per-point bonuses (Multi Action, Bonus PP,
Bonus Chip, Charge SP, and two damage/fund scaling bonuses). One fragment
(Charge SP's SP-recovery amount) is genuinely truncated in the stored
data -- it ends at the object marker を with no completion found nearby
or via a reused "回復する" template -- so its English stays an honest
dangling fragment ("...SP by") rather than inventing a number. Repeated
plain continuations share one entry each: "。" (already hooked to "."),
"、" -> ",", and "になる。" (appears 4 times across the block) -> ".".

**Boost-part descriptions ship after all -- through the draw-time hook.**
The 300 translated descriptions (subsequently revised against Akurasu in the
Unreleased Power-part review above) held back in
`translation/parts_descriptions.unshipped.json` now reach the screen via
`translation/parts_desc_hook.json` (UI_HOOK_FILES): the hook swaps them
by content at draw time and never touches RPW_DATA.CPK, so the boot
corruption that forced the hold cannot occur (the RPW-side guard stays).
Parts screen: the ：パーツ決定 hint "：Set Parts" (a different string from
the ：換装パーツ決定 one already hooked) and shorter Type tabs (地形 "Terr",
消費 "Use", 特殊 "Spec") that no longer overlap. Operation End: stage 3's
three-line SR condition stayed Japanese although the whole string was
hooked -- that box draws one line per call -- so `eboot.load_ui_hook`
now also registers each line pair of every multi-line entry whose line
counts agree (existing entries win; lines under 6 characters are
skipped).

**Mech special-ability descriptions translated.** `translation/ability_hook.json`
now holds the actual English (63 lines) for the executable's mech SPECIAL
ABILITY descriptions (Mech Info screen, battle popups). Re-checked the
executable around the extracted block for any strings the cut heuristic
might have missed (parries, barriers, HP/EN regen, transform/combine,
Newtype/Trans-Am/Spiral Power/Genion Gai bonuses, the Aquarion EVOL Sphere
effects, ...); none found -- the 63-string block is complete. Ability and
spirit names quoted in the text use the settled English from
`translation/abilities.json` and `translation/spirits.json`
(天元突破グレンラガン -> Tengen Toppa Gurren Lagann; 閃き/闘志/突撃 ->
Alert/Zeal/Assail); weapon special-effect and system names follow the
terms already shipped in `translation/parts_descriptions.unshipped.json`
(切り払い -> Parry, バリア貫通 -> Barrier Pierce, 連続ターゲット補正 ->
Focus-Fire, プレースメントシステム -> Placement). Four effect names with no
prior precedent in this project (能力半減, 戦闘不能, 気力低下, ＳＰ低下,
plus the stat-down ▼ effects) are coined here as Ability Halved,
Incapacitate, Morale Down, SP Down, and e.g. Mobi Down. Matched Japanese
line breaks 1:1 and kept every line at or under 56 characters.

**Pilot skill descriptions translated.** `translation/skill_hook.json`
originally supplied the English (124 lines; subsequently revised in the
Unreleased Akurasu review above with complete prose wrapping): both the long and the
alternate/short description column (`sk-pri` columns 4-5) for all 68
skills, one entry per distinct description string (record 0's "－－"
placeholder is skipped; records 38 ニュータイプ and 39 強化人間 share
byte-identical text in the source, so they share one entry). Skill
names referenced in the prose use the settled English from
`translation/skills.json` (底力 -> Potential, 再攻撃 -> Re-Attack, 超能力
-> ESP, 螺旋力 -> Spiral Pow, ...); 援護攻撃/援護防御 render as the full
words Support Attack/Support Defense here (column-4/5 prose has room,
unlike the abbreviated skill-name slot), and アシスト攻撃 -- a distinct
battle mechanic, not the サポートアタック skill -- renders as Assist
Attack. Matched Japanese line breaks 1:1 and stayed under 56 characters
per line.

**Duration values, terrain help, skill and ability descriptions.** The
spirit list's Duration value (即時効果 "Instant", ターン開始 "Turn start",
防御／ダメージ／戦闘／攻撃／移動／行動／撃墜, なし) is drawn from the
executable's UTF-8 table, which the cp932 hook never sees -- it now goes
through `translation/ui_utf8.json` (the hook entries stay for the cp932
twins). PP screen: the four 地形適応「…」を上昇させます。 terrain help lines
and the three PP messages (not enough PP / cannot learn / cannot raise)
are hooked. Two more description families ship through the hook, never
the RPW swap (they are multi-line): pilot SKILL descriptions from the
`sk-pri` table (`translation/skill_hook.json`) and mech SPECIAL ABILITY
descriptions from the executable (`translation/ability_hook.json`); both
files are in `UI_HOOK_FILES`. The hook's EXT segment grew 128 KB -> 256 KB
(`EXT_SIZE = 0x40000`, table 4,096 entries): a skill description's
Japanese is not in the executable, so both halves are copied in, and
~190 multi-line strings overflowed 128 KB. Still Japanese by design: the PP-screen
tab and PP-block textures, voice-actor names, and the spirit-grid
centring (fixed-pitch layout, renderer-side).

**Spirit command descriptions translated.** `translation/spirit_hook.json`
now holds the actual English (38 lines): effect text for all 42 named
spirit commands plus the record-43 "？？？？" unrevealed-spirit placeholder
("？" -> "?", matching the "？？？" -> "???" convention used elsewhere).
Kept every stat number exact (２．２倍 -> 2.2, ３０％ -> 30%, １／８ -> 1/8),
used the settled names from `translation/spirits.json` for anything quoted
in 「」 (「魂」 -> Soul, 「熱血」 -> Valor, ...), matched Japanese line breaks
1:1, and stayed under 58 characters per line (longest shipped is 53).

**Library, spirit-list and PP-screen labels; spirit descriptions.**
Library: 愛称 "Nickname", 声優 "Voice", 登場作品 "From", 名前／愛称 block,
：表情 "：Expression", ：台詞 "：Lines", 全長 "Height", 重量 "Weight" -- all
draw-time hook entries, because 愛称 has six copies in AIDDATAPACK and the
in-place channel only patches member 0 (the library's copy stayed
Japanese). Spirit list: originally 効果 "Effect", 対象 "Target", 持続 "Duration";
now shortened to "Eff.", "Tgt.", "Dur." after screenshots showed overlaps
with their values. The combined footer retains the duration column using
compensating spaces. Also translated: the Target/Duration vocabulary the EBOOT
composes from pieces -- 自分 "Self", 味方 "Ally", 敵 "Enemy", 自チーム "Own
Team", 単体 "Single", 周囲 "Area", 全体 "All", チーム "Team", ターン開始 "Turn
start", 即時効果 "Instant", 防御／ダメージ／戦闘／攻撃／移動／行動／撃墜. The
spirit DESCRIPTIONS ship through a new hook file
`translation/spirit_hook.json` (UI_HOOK_FILES), NOT the RPW swap: they
are one- or two-line RPW strings, the same class that corrupted boot for
the boost-part descriptions. (First noted here as "44 ... two-line",
before the file was authored; the chunk holds 44 records, record 0 is
the "－－" placeholder and is skipped, and five of the remaining 43 are
"＋"-variants whose effect text is byte-identical to their base spirit's,
so the shipped file holds 38 distinct entries covering all 43.) PP
screen: the tabs パラメータ上昇／スキル修得 and the 所持／必要／残りＰＰ block
are TEXTURES -- the only string copy sits in an unused UI member
(replacing it in place changed nothing on screen), so they join the
other pre-rendered headers as future atlas work; the hook and in-place
entries for them were removed. The six stat help texts on that screen
(格闘系の武器使用時の… etc., EBOOT strings) are hooked, three lines each.
Library labels were shortened after the first build overlapped their
values (the value sits at a fixed two-character offset): 愛称 "Nick",
声優 "CV", 全長 "Ht.", 重量 "Wt.". Known and not fixed: the spirit-list
grid centres each name by fixed-pitch character count, so proportional
English sits left of centre by up to half a name -- a renderer-side
issue like the font advance, not a text one. Voice-actor names (声優)
stay Japanese for now.

**Boost-part descriptions held back; names ship.** Final word on the
boot crash after 13 in-game bisect boots: any swapped boost-part
DESCRIPTION (RPW `boost-p` columns 3-8) can corrupt memory at boot --
seen as a black screen and as a bogus "not enough HDD space, 257,604 MB
(later 475,681 MB) more needed" install message with 2.8 TB free. The
two entries below (200-byte per-string cap, 890-byte per-record cap)
were each contradicted by the next test: a 39 KB per-column-capped
subset failed where a 49 KB per-record subset booted, five ordinary
appended strings flipped a booting file into a failing one, and "%" and
the DL variants were cleared too. The file without any part strings
boots every time; the 69 part NAMES alone boot (single-line, the same
class as the proven weapon names). So `translation/parts.json` now holds
only the names; the 300 translated descriptions moved to
`translation/parts_descriptions.unshipped.json`, and `build_project.py`
refuses to swap a boost-p description. The descriptions are the only
multi-line strings in the RPW pool -- the loader evidently handles them
differently; an EBOOT-side look at the boost-p loader is the way in.

**(Superseded -- see the entry above.)** Second diagnosis: a per-record limit, not per-string.
The 200-byte-per-string cap below turned out to describe the wrong unit.
Bisecting in-game (RPCS3, one field at a time) found the game copies each
boost-part *record's* eight column strings (name x2, long/short
descriptions, DLC variants) into one fixed buffer per record, sized to the
largest original record: 890 encoded bytes total, not 200 per string. A
record can black-screen at boot with every individual string under 200
bytes if their sum exceeds 890. Encoded byte cost = 2 x characters (a
newline costs 1, not 2) + 1 for the NUL. 22 of the 69 boost-part records
totalled over budget (up to 1192 bytes, `boost-p` record 35 "Screw
Module"); their long/short descriptions (columns 3-8; names left alone)
were rewritten tighter -- trimming filler words, `&`/`/` for "and"/"with",
dropping repeated "the main unit is equipped" boilerplate to "Main unit
equipped at phase start" -- while keeping every stat number, the DLC-only
marker, and the shipped stat terms exact. Worst rewrites: record 35 (Screw
Module, 1192 -> 868 bytes), record 32/34 (Flight/Land Module, ~1120 ->
~850), record 54 (SP Getter, 1128 -> 788). All 22 records now total 764-880
bytes (890 max, ~10 bytes slack); every rewritten string is under 190
bytes. `rpw.MAX_JSTRING` and `build_project.py`'s per-string check still
stand as a secondary guard but do not by themselves prove a record boots.

**(Superseded -- see the entry above.)** First diagnosis of the boot
crash, kept for the record: bisecting RPW_DATA.CPK alone showed the
known-good content, the name pieces, the per-record name overrides and
the part names all boot, and descriptions capped at 200 bytes booted
while the full set crashed -- so a 200-byte per-string cap shipped
(`rpw.MAX_JSTRING`) with 17 descriptions shortened. It was wrong: with
the part NAMES also present the same descriptions crashed again, and
descriptions up to 199 bytes boot when their record is small. The real
constraint is per record (name twice + six descriptions <= 890 bytes);
`MAX_JSTRING` was removed and replaced by `rpw.MAX_BOOSTP_RECORD`.

**`translation/parts.json`: the 強化パーツ (boost parts) table translated,
370 strings.** RPW_DATA.CPK chunk `boost-p`, 69 records (record 0 is the
"－－" placeholder, skipped): col 1/2 the part name (col 2 duplicates col 1
except record 16, a nakaguro variant of パラジウム・リアクター -- both map to
"Palladium Reactor"), col 3 the long/polite description, col 4/5 a short
line-broken description, col 6/7/8 the same paired with a "ＤＬ専用"
DLC-only suffix. Names follow official SRW English releases where one
exists (Booster, Mega Booster, Magnetic Coating, Chobham/Hybrid Armor,
Haro, Z Chip, Repair Kit, Propellant Tank, Cartridge); series references
resolved against `analysis/glossary.json` (トライデント焼き "Trident-yaki",
カミナ "Kamina" for カミナのサングラス "Kamina's Shades", インサラウム
"Insaraum" for インサラウムの秘宝 "Insaraum's Treasure", バサラ/Fire Bomber
for Ｆボンバーのディスク "Fire Bomber's Disc", ＤＧ "DG" for ＤＧの牙 "DG Fang")
and stat wording kept consistent with `translation/ui_hook.json` /
`skills.json` / `spirits.json` (地形適応 "terrain rating", 精神耐性 "Mind
Resist", サイズ差補正無視 "Ignore Size", the nine spirit-command names).
Three names have no glossary or wiki source and are best-effort
transliterations, flagged in the file's `_note`: クエント製センサー "Kuento
Sensor", カイメラ隊員証 "Chimera Squad ID", 極小次元震システム "Micro
Dimension Quake System". Descriptions mirror the Japanese line breaks
1:1 rather than rewrapping to a fixed width, since the box appears to
render each source `\n` as a hard break; the longest lines are the
single-line (no `\n` in the source) compressed variants, e.g. "Grants
multiple spirit command effects; usable once per map" at 50 letters,
above the ~40/line target because the Japanese itself is one dense line
there.

**Pilot names in pieces, skills shortened, parts and upgrade screens
labelled.** Pilot Info showed "Jeffrey・ワイルダー", "Bobby・マルゴ" and
"相良Sousuke": the status screens draw a name from the `pilot-nw` record
as two separate strings (w0 given, w1 surname), and the j-string table is
deduplicated, so whole-name glossary entries never matched and a content
swap of pieces could not tell Rei Ayanami's レイ from Amuro Ray's. New
`rpw.piece_overrides()` resolves each record's (surname+given) or
(given・surname) to its glossary character and gives BOTH slots their own
English -- 454 records, 908 slots -- with the surname carrying a trailing
space for Japanese-style names, which the game draws with no separator
("Sagara Sousuke"; Western names keep the drawn ・ between "Jeffrey" and
"Wilder"). `tools/name_pieces.py` writes `translation/name_pieces.json`,
the fallback map of the 571 pieces whose English is the same for everyone
(the 6 shared ones -- レイ, アスカ, クラン, ミーナ, 伊集院, Ｆ -- are left to
the per-record override). The earlier hook-all-names change stays for the
whole-name draws. Skills: the PP screen right-aligns an already-learned
row by cell count, so long English names walked left into the Skills
column; every skill is now at most 11 letters (Support Atk, Support Def,
Assist Atk, Morale+ Dmg/Evd/Hit/KO, Limit Break, Precise Atk, Tactic Cmd,
Spiral MAX, Grav Fld 1/2, Fighting Sp, Double/Triple Act, and so on --
42 renamed). `translation/ui_hook.json` +15: the parts screen (：換装パーツ決定
"：Set Parts", ：変形確認 "：Transform", はずす "Remove", 分類 "Type", 全種
"All", 特殊 "Special", 残　総 "Left Total", なし "None", （チーム） "(Team)")
and the upgrade screen (機体改造度 "Upgrade Lv", 武器 "Weapon", the
総資金額／改造費用／残額 block "Total Funds. / Upgrade Cost. / Remaining.").
`load_labels()` now also reads `translation/parts.json` (boost-part names
and descriptions through the RPW swap; the file is written up in the entry
above).

**Every glossary name is now hooked at draw time; skill-acquisition screen
labelled.** Pilot Info showed キャサリン・グラス in Japanese although the
glossary has "Catherine Glass": the draw-time name hook only installed
names it could find inside the EBOOT, and 853 glossary names (599 pilots,
253 mechs) live in data tables instead, so all of them stayed Japanese on
the Pilot Info / Unit Info screens. `eboot.HOOK_ALL_NAMES` now routes an
absent name through the same copy-the-Japanese path a UI label uses, and
`build_project.py` pools the letters of every name. That is 1,554 hook
strings (was 675), ~65 KB, so the EXT segment grew from 64 KB to 128 KB
(`EXT_SIZE = 0x20000`; the 2,048-entry table is unchanged). Also 41 new
`translation/ui_hook.json` labels: the PP screen tabs (パラメータ上昇 "Raise
Stats", スキル修得 "Learn Skills"), its three-line 所持／必要／残りＰＰ block
("PP Held / PP Cost / PP Left"), the ＜…＞ help lines for the stats, skill
and terrain tabs, and the ：hint family (：項目決定 "：Select", ：決定
"：Confirm", ：戻る "：Back", ：キャンセル "：Cancel", and 30 more).

**Voice: section 166 is Riddhe Marcenas (Gundam UC), 189 lines** -- Codex
draft, Sonnet-reviewed. Brief filed unit Zeta Gundam / pilot Kamille Bidan
via a weak weapon-name match (Beam Confuse/Beam, score 1.0) -- wrong, the
same cross-unit weapon-name collision already documented for sections
56/68/87/131. The draft had already ignored the brief and translated the
actual content correctly without ever saying so; identity is recorded here
for the first time. Content is unmistakably Riddhe: entry 3 self-declares in
full ("Riddhe Marcenas, begin combat!"), entry 2 gives his radio callsign
("This is Romeo 008! Going!"), and he names both of his own mounts directly
-- entry 16 the Rezel, entry 17 the Delta Plus -- matching his bio exactly
(originally rode the Rezel, switched to the Delta Plus after the fight with
the Sinanju). The section runs his whole UC-0096 arc: reluctant
confrontations with Char Aznable, Full Frontal and Haman Karn as legends he
measures himself against (75-78), an anguished block pleading with Banagher
by name (97-100, "I really don't want to attack...! Understand!"), and a
late ally-address cluster (186-209) naming Banagher, Kamille, Otto (Captain
of the Nahel Argama), Bright (Captain of the Ra Cailum), Hathaway and Katz --
consistent with his bio's note that he is later dispatched to the Ra Cailum,
matching sections 44/45 and 139 already on file for those two ships. Recorded
in `analysis/voice_identity.json` under "166". Not confirmed by a
screenshot.

Found and fixed 27 deficient lines, run through `tools/check_voice.py` to 0
problems:

- **Known project fix**: entry 73 shipped `"BeamConfuse"` (no separator, not
  this project's own abbreviation) -> `"B.Confuse!"`, per the shipped
  precedent in voice_068.json and voice_131.json.
- **Idiom mistranslation**: entry 74, jp "上手くいったら、お慰みだ！" (a
  modest, self-deprecating "well, if it works, that's something" hedge)
  shipped as `"This'll amuse"`, inverting the register into arrogant
  taunting -> `"If it works!"`. Entry 83, jp "スペースノイドは過激な事しか
  しない" (Spacenoids only ever do extreme/radical things -- an accusation
  of violent extremism) shipped as the trivializing `"Spacenoids go
  wild!"` -> `"Spacenoids extreme!"`. Entry 207, jp "親父さんを悲しませる
  真似はするな" (don't make your father SAD) shipped as `"Don't shame
  Dad!"`, swapping grief for dishonor -> `"Don't sadden Dad!"`.
- **Reversed command/action direction**: entry 70, jp "ランチャーで落とす"
  (I'll bring YOU down with the launcher) shipped as `"Launch it!"`, turning
  an enemy-directed threat into a vague self-reference -> `"Drop you!"`.
  Entry 184, jp "こちらからも攻撃する" (joining an attack already underway)
  shipped as `"Counter now"`, reading as a defensive reaction instead of
  adding offense -> `"I join in!"`. Entry 189, jp "続きます" (Riddhe's own
  polite vow to follow Captain Bright) shipped as the bare imperative
  `"Follow Bright"`, reading as an order for a third party to follow him ->
  `"With Bright!"`. Entry 205, jp "俺の後ろに" (get behind ME) shipped as
  the objectless `"Get behind"` -> `"Behind me!"`. Entry 283's despair
  couplet ended "何も出来ない" (I can do nothing); its second line shipped
  as the imperative `"Do nothing!"`, inverting self-directed helplessness
  into a command -> `"Save none!\nCan't do it!"`.
- **Torment flattened**: entry 287, jp "なんて情けないんだ、俺は" (self-
  loathing) shipped as the generic, subject-less `"How pathetic!"` ->
  `"I'm pathetic!"`, keeping the self-address. Entry 85 used "?" where the
  Japanese ends "！" (mockery misread as a genuine question) -> `"That
  relic?"` -> `"Old relic!"`. Entries 102 and 191 dropped a conditional and
  an addressee, respectively, with budget room to spare: `"Lose now,\nall
  wasted!"` -> `"If I lose,\nall's wasted!"` (restores the "if"); `"I take
  over!"` -> `"Lt, mine now!"` (restores who is being addressed). Entry 11
  (`"Damn you"`, no bite) -> `"Bastard!"` for register.
- **Punctuation dropped despite spare budget**: 13 entries (30, 79, 86, 101,
  194, 202, 211, 220, 241, 243, 253, 278, 280, 281) ended their Japanese with
  "！" but shipped with no closing mark even though the budget had room;
  added it back. Two of those fixes collided with an existing line's English
  for different Japanese (216/241 both `"No big deal!"`; 4/30 both then
  `"Now!"`) -- caught by `check_voice.py` and re-differentiated: 241 ->
  `"Nothing to it!"`, 30 -> `"Fire"` (both `"Now!"` and `"Go!"` were already
  spoken for elsewhere in the section).

**Voice: section 72 is Kurz Weber (Full Metal Panic), 193 lines** -- Codex
draft, Sonnet-reviewed. Brief filed unit UNKNOWN, no weapon call-out matched
-- identity is a content read: he self-names callsign "Urzu 6" directly (15,
16, 165, 187, 296), runs a running gag about wanting to see Teletha
Testarossa (Tessa) naked (41-44, 67-70, 200, 231-234, 271-273, 297),
addresses Melissa Mao as "sis" (39-40, 188-189, 202), needles Sousuke Sagara
by name (30, 190-191, 233, 298), addresses Chirico Cuvie by name and by the
nickname "gloomy guy" (203-204, 274), treats Lockon Stratos as a fellow
sniper (194, 206), calls himself Mithril's number-one sniper (168) and a
"Mithril warrior" saving a princess (211, 213), and names Aoi/Kurara/Eida as
women under his protection (193, 205) alongside a "Red Comet" (Char
Aznable-type) taunt (52-53) -- matching the glossary's own Kurz voice note
("Flippant. Calls Mao 姐さん") exactly. No mecha self-naming occurs anywhere
in the 193 lines, so unit ships null rather than the M9 Gernsback he usually
flies. Recorded in `analysis/voice_identity.json` under "72". Not confirmed
by a screenshot.

The draft's own notes flagged roughly 60 entries where a qualifier or joke
was compressed away for budget; for Kurz the joke often *is* the register, so
each was checked for room to restore it. Found and fixed 13 deficient lines,
run through `tools/check_voice.py` to 0 problems:

- **Spelling inconsistent with the project glossary**: "Sosuke" (missing the
  long vowel) shipped at entries 30, 190, 191, 233 and 298; the glossary and
  every other section spell it "Sousuke". Fixed all five; entry 298 also
  needed its trailing "!" dropped to re-fit the corrected spelling in budget
  (`"Sosuke, you'll pay!"` -> `"Sousuke, you'll pay"`).
- **Threat direction reversed**: entry 71, jp "てめえらみたいな下衆は、
  とっとと片付ける！" (scum like you, I'll finish you off quick -- 片付ける
  here is "dispose of/eliminate", not "leave") shipped as `"You scum,\nget
  lost!"` (tells them to go away instead of threatening to finish them) ->
  `"Scum,\nI'll finish ya!"`.
- **Idiom flattened into an unrelated dedication**: entry 30, jp "ソースケの
  奴が世話になったみてぇだな！" (世話になった used ironically here -- "so
  this is the thing that gave Sousuke trouble", sizing up the tough recurring
  enemy the next several lines describe as a persistent, device-carrying
  "big object") shipped as `"For Sosuke, then!"` (reads as fighting on
  Sousuke's behalf, not recognizing a foe that troubled him) -> `"Gave
  Sousuke grief!"`.
- **Verb dropped, leaving a bare noun phrase**: entry 210, jp "金輪際男の
  ケツを守るのは御免だぜ！" (never again will I babysit some guy's ass)
  shipped as `"No more guy's ass"` (no verb -- reads as a non sequitur) ->
  `"No covering guys!"`.
- **Direct address dropped, breaking a callback**: entry 213, jp "ここは
  あなたのナイトにお任せを！" (leave this to your knight!) shipped as the
  impersonal `"Knight at work!"`, losing the link to 70's "her knight act"
  jab at a rival for doing the very thing Kurz is now doing himself ->
  `"I'm your knight!"`.
- **Dropped jokes restored where budget allowed**: entry 180 ("Hero's late"
  -> `"Late entrance!"`, the self-aggrandizing "heroes always arrive
  fashionably late" bit reads as a boast instead of an apology); entry 193
  ("Aoi, pay up!" -> `"Aoi, reward!"`, ご褒美 is a playful "treat", not a debt
  demand); entry 198 ("So reckless!" -> `"Tch, reckless!"`, restoring the
  ったく interjection); entry 287 ("Breaking..." -> `"Falling apart!"`, the
  idiom ガタが来る is "wearing out/falling apart", not a vague "breaking");
  entry 297 ("Tessa nude...?" -> `"Tessa... a dream?"`, restoring 幻だった
  のか, "was it all just an illusion", the punchline of the whole nudity
  gag as it finally fizzles).
- **Reviewed and left as-is**: entry 205, jp "葵とくららとエイーダは
  やらせねえ！" ships as the bare list `"Aoi, Kurara, Eida"` -- budget is
  exactly zero slack for the three names alone, no room for a verb without
  dropping a proper noun.

**Voice: section 143 is Full Frontal (Sinanju), 195 lines** -- Codex draft,
Sonnet-reviewed. Filed as Gundam Mk-II via weapon-name match (score 1.0,
weapon 333) -- wrong, the same beam-rifle/vulcan/shield common-weapon magnet
that already misfiled 29, 117-119 and 189/190 for this project. Confirmed as
Full Frontal himself (not a rank-and-file Guard grunt like 29/189/190) by
content: he opens with the Axis Shock declaration (17/18/331), demands
Laplace's Box (64-66, 228), and addresses Banagher Links, Amuro Ray, Kamille
Bidan and Londo Bell by name as Unicorn-era adversaries (69-78, 121-125,
162-164, 229-234). He commands his own Personal Guard under Captain Angelo,
addressed directly and personally (90/198, 98/206, 146/271), commands the
ship Garencieres (92/200), and is himself addressed as 総帥 ("Commander" --
the same title 29/189 use for him) by a subordinate (94/202). He runs the
"Red Comet" rivalry-with-Char thread already traced for him at 29 and 189
(79, 104, 128, 154, 179-180, 321-322), names Char Aznable directly as his
measure (80, 101/209, 129/237, 167/292), names his own machine once (216,
"I may have pushed the Sinanju too hard"), and -- distinctive to this
section -- addresses himself by his full alias in a moment of self-reproach
(183/325, "Full Frontal, that is unlike you...!"), the formal self-narration
of a man who treats his own persona as a performance. The section closes
with a fourth-wall thank-you to the player (326-330), the same device
already shipped in Char's own epilogue at section 87 -- here in Frontal's
voice instead. Recorded in `analysis/voice_identity.json` under "143". Not
yet confirmed by a screenshot.

Found and fixed 10 deficient lines, run through `tools/check_voice.py` to
0 problems:

- **Threat/command direction and address reversed**: entry 198, jp "余計な
  真似と言わんでくれよ、アンジェロ" (don't call it needless meddling,
  Angelo! -- Frontal preempting a complaint about stepping into Angelo's
  fight) shipped as `"Forgive me, Angelo"` (an apology, the opposite
  register -- submissive instead of the brisk deflection the line actually
  is) -> `"No offense, Angelo"`.
- **Concessive clause dropped, changing a taunt into a bare name-drop**:
  entry 78, jp "カミーユ・ビダンと言えど！" (even if it's Kamille Bidan!,
  i.e. not even a famous Newtype pilot is spared) shipped as bare
  `"Kamille Bidan"` -> `"Even Kamille!"`.
- **Essential noun truncated, leaving the line unreadable**: entry 79, jp
  "赤い彗星は一人でいい…！" (there is room for only one Red Comet) shipped
  as `"Only one Red"` (drops "Comet", the noun the whole sentence is about)
  -> `"1 Red Comet"` (digit for "one" matches this project's own established
  shorthand, e.g. "1-on-1!", "1 kill each!" elsewhere in translation/).
- **Whole trailing clause dropped with budget left unused**: entry 209, jp
  "シャア・アズナブル…！　それでも…！" (Char Aznable...! Even so...!)
  shipped as `"Char Aznable...!"` (drops "even so" though 2 cells of budget
  sat unused) -> `"Char Aznable! Yet!"`; entry 330, jp "その頃には君も私の
  真意を知る事になるだろう" (by then you too will come to know my true
  intent -- a prophecy, not an order) shipped as the imperative `"Then know
  my intent."` (wrong mood -- reads as a command, not a forecast) ->
  `"You'll know my intent"`.
- **Register regression -- his signature formal imperative flattened into
  a flat statement**: entry 107, jp "君の生まれの不幸を呪いたまえ" (curse
  the misfortune of your birth -- an archaic "-たまえ" command, exactly the
  polished courtesy-as-menace this character runs on) shipped as the
  descriptive `"Born cursed..."` (states a fact instead of issuing the
  order) -> `"Curse your lot"` (keeps the imperative).
- **Self-address collapsed into a vague aside**: entry 325, jp "フル・フロ
  ンタル、お前らしくないな…！" (Full Frontal, that is unlike you...!, said
  by him to himself) shipped as `"Full Frontal, shame"` (loses the "unlike
  you" self-appraisal, reads as a generic bark) -> `"Unlike you, Frontal"`.
- **Vague filler standing in for a specific image**: entry 26, jp "懐が
  がら空きだぞ！" (your guard/chest is wide open) shipped as bare `"Open!"`
  -> `"Exposed!"`.
- **Wrong-direction attack call**: entry 6, jp "行けるか！" (will this
  connect?! -- an attack line challenging the target, not a statement about
  himself) shipped as the self-focused `"Ready"` -> `"Land!"`.
- **Ambiguous fragment (could be misread as a request rather than a
  question)**: entry 215, jp "こちらの手は読まれているか…！" (has my move
  been read?!) shipped as `"Read me...!"` -> `"They read me?!"`.

Quality: cleaner than the 090/101-era Codex drafts (B-/C+) -- the tight
formal-menace register mostly held (the polite "-させてもらう" attack lines
compressed consistently rather than collapsing into generic barking, and
project terms Red Comet/Sinanju/Laplace's Box stayed consistent throughout),
but one line flipped an apology's direction entirely, one dropped the noun
its own sentence needed, and the rest were smaller nuance/mood losses under
budget pressure. Landing around B+. `python tools/check_voice.py
work/voice/answer/143.json`, 0 problems, 195 of 195 answered.

**Voice: section 102 is Shinkiro / Zero (Lelouch Lamperouge), 132 lines** --
filed as Lancelot Albion / Suzaku Kururugi via weapon-name match (score 1.0)
-- wrong, reattributed by content. The unit robots.json entry for 蜃気楼
(Shinkiro, i=226) lists PLTN ゼロ (Zero) as its pilot, and its bio names both
signature weapons that occur in this section verbatim: 拡散構造相転移砲
(entry 30, "Spread Phase-Shift Cannon" in translation/weapons.json, and
confirmed a Shinkiro-only weapon in source/rpw/weapons.json) and the defense
field 絶対守護領域 (entry 101). Entry 102 says outright "this is Shinkiro's
power" (これが蜃気楼の力だよ). The speaker self-identifies as Zero (entry 8,
"I am Zero"), later commands as "Lelouch vi Britannia" (126, 129 -- the
Emperor persona's public declaration from the Zero Requiem climax), addresses
Nunnally with love (14, 130), praises Rakshata's engineering (103), and --
decisively -- addresses Suzaku (59, "What are you doing getting hit,
Suzaku!") and Kallen (51, 55, 56, 59) by name as separate people he is
protecting, which rules out Suzaku as the speaker (he is confirmed piloting
Lancelot Albion himself in section 4, translation/voice_004.json). Recorded
as "102" in `analysis/voice_identity.json`. Budget forced meaning loss
repeatedly at this section's extreme low end: entry 30 (weapon call-out,
budget 8) has no room for any weapon name at all, shipped "Fire!"; entry 126
("ルルーシュ・ヴィ・ブリタニアが命じる", budget 18) dropped the "vi
Britannia" title, shipped "Lelouch commands"; entry 130 (his dying line to
Nunnally, budget 16) dropped "thank you" to keep the declaration itself,
shipped "I love Nunnally". Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/102.json`, 0 problems, 132 of 132
answered. `tools/merge_voice.py 102` -> `translation/voice_102.json`. No
twin section (work/voice/clusters.json lists 102 as a singleton group).

**Voice: section 51 is Geminia / Gadlight Meonsam, 121 lines** -- filed as
Space Gunmarl / Darry Adai via weapon-name match (score 2.0) -- wrong,
reattributed by content. The unit robots.json entry for ジェミニア (i=244)
lists its pilot as ガドライト・メオンサム (Gadlight Meonsam, i=394 in
pilots.json): captain of the Geminis, who loves idleness and drink, watches
the chaos he causes from a bar, and is repeatedly scolded for his
slovenliness by his adjutant Annalotta -- an exact match for this section's
register (hangover jokes, being nagged about drinking, calling himself lazy)
and for entry 173 addressing Annalotta by name directly. The speaker calls
his machine "Geminia" by name five times (44, 48, 54, 112, 132) and his own
Sphere "the culmination of my Sphere and Geminis's technique" (54), matching
Gadlight's Sphere "the Bickering Twins" (いがみ合う双子) from his robots.json
bio -- not a literal twin pilot pair, just the Sphere's name. "ハニー"
(Honey) recurring through the section (3, 136, 168-172) reads as Gadlight's
pet name for Annalotta. The section is a crossover taunt set: he needles a
long list of other shows' protagonists by epithet rather than name (Newtype,
Innovator, SEED, "Man of the Spiral" i.e. Gurren Lagann, "Mechanical Angel",
a Gundam pilot, a "King") without naming his own show's cast. Recorded as
"51" in `analysis/voice_identity.json`. Budget forced meaning loss at the
tightest entries: entry 46 (budget 11, "神の左手、悪魔の右手" -- "God's left
hand, devil's right") dropped the imagery entirely, shipped "Two fists!";
entry 168 (budget 9) and entry 172 (budget 11) both had to drop "Honey" by
name, shipped "Backup!" and "Not Honey!"; entry 173 (budget 13, "下がって
ろ、アンナロッタ！") only fit the glossary-mandated verbatim "Annalotta"
alongside a one-word "Go,", shipped "Go, Annalotta". Not confirmed by a
screenshot. `python tools/check_voice.py work/voice/answer/051.json`, 0
problems, 121 of 121 answered. `tools/merge_voice.py 51` ->
`translation/voice_051.json`. No twin section (work/voice/clusters.json
lists 51 as a singleton group).

**Voice: section 201 is Chrono Reform Faction troops, 119 lines (twin 202,
118 of 119 lines propagated + 1 hand-translated)** -- filed as Gundam Mk-II
(weapon-match, 1.0), another beam-rifle/vulcan common-weapon magnet -- wrong,
no Mk-II/AEUG/Kamille content anywhere. The lines are a collective, zealot
"we" voice preaching forced world-change through power and sacrifice ("for
our noble ideal", "reform demands sacrifice", "we will change the world",
"the powerless have no right to speak of justice"), naming Gundam and
Dancouga as enemies in their way (21, 23, 48, 60, 61, 71, 81), never as
allies. source/library/pilots.json (i=397-401) identifies this as "Chrono"
(クロノ), an original-story organization of "watchers over humanity's
evolution" split into a Reform faction (led by Advent, who pilots a
customized Asclepius) and a Conservative faction (backed by
Geminis/Gadolite); source/library/robots.json (i=251, Asclepius) states the
Reform Faction flies the mass-produced version of that unit. Advent's own
voice set is section 014 (translation/voice_014.json) -- singular "I",
formal and dignified, a different register from this section's collective
"we" -- so this ships as anonymous Reform-faction grunt pilots, not Advent
himself. Recorded as "201"/"202" in `analysis/voice_identity.json`. Budget
forced meaning loss at entry 49 ("甘いな、ダンクーガ！", budget 10): no room
for "too soft" alongside the name, shipped "Dancouga!" alone and flagged.
`tools/voice_propagate.py 201` carried 118 of 202's 119 lines by matching
Japanese text (202 entry 75, "「うっ！　\n　このままでは一方的にやられる…！」",
has no byte-identical match in 201 -- translated by hand as "Ugh!\nit's
one-sided!"). Not confirmed by a screenshot. `python tools/check_voice.py`
on both, 0 problems, 119 of 119 each. `tools/merge_voice.py` run for both
-> `translation/voice_201.json`, `translation/voice_202.json`.

**Voice: section 198 is Akagi Ryunosuke's "Nerima Red Dragon" Arm Slave
team, 132 lines (twin 199, 133 lines after a propagation gap was
hand-filled)** -- filed as Gundam Mk-II (weapon-match, 2.0), the same
common-weapon magnet. The section self-identifies by its own unit nickname
"練馬レッドドラゴン" (Nerima Red Dragon) in pride and dying-words lines (24,
78, 82, 127, 148), while naming Dai-Guard (128, "wasn't Dai-Guard just a
fake prop after all?!") and Gundam (54, "a Gundam over there too?!") as
OPPONENTS met mid-battle -- ruling out both as the speaker. Web research
(srw.wiki.cre.jp) identifies Akagi Ryunosuke as an SRW-original JGSDF pilot
(first added in Super Robot Wars W) who leads a squad called exactly
"Nerima Red Dragon" out of Nerima base, flying red-marked Arm Slaves (Full
Metal Panic! crossover roster); his gimmick is a theatrical, grandiose
speech pattern that deliberately imitates Char Aznable, played for comedy
against his modest combat record -- matching this section's boastful "our
performance rivals a Gundam's!" (29) and reluctant-admiration lines ("I
admit, good hit", 117; "a bad matchup, is it?!", 123), and confirmed by
entries 52-53, which react to the REAL "赤い彗星" (Red Comet = Char Aznable)
appearing as a separate opponent in the same battle -- the parody meeting
the man he imitates. Recorded as "198"/"199" in `analysis/voice_identity.json`.
`tools/voice_propagate.py 198` carried 199's lines by Japanese-text match;
surfaced a `voice_propagate.py` limitation along the way (not fixed in the
tool, only worked around here) -- when a section holds the SAME Japanese
line at two distinct (non-shared) entry indices, the tool's `{jp: entry}`
dict silently collapses them to one, so only the later index gets the
propagated English and the earlier one ships in Japanese. This hit 199
entry 134 (index 142 carries the same "「落ちろぉぉっ！」" and got "Fall!"
from propagation; 134 did not) -- filled by hand with the same "Fall!".
202 entry 75 was a separate case: a genuinely distinct line with no
byte-identical match in 201, also filled by hand. Not confirmed by a
screenshot.
`python tools/check_voice.py` on both, 0 problems, 132 of 132 and 133 of 133.
`tools/merge_voice.py` run for both -> `translation/voice_198.json`,
`translation/voice_199.json`.

**Voice: section 035 is Izumo Kamurogi (Ahura Gnis), 119 lines** -- filed
unit UNKNOWN, no weapon-table match (score 0.33). Content is unmistakably
Aquarion EVOL / Altair, and unmistakably Izumo Kamurogi specifically: he is
named directly ("イズモ・カムロギの戦いを見せてやろう", entry 7) and titled
("アルテアの最高指導者の戦いを...とくと見よ", entry 6 -- Supreme Commander of
Altair per translation/library/pt_360.json entries 104-105). Matches his
canonical bio beat for beat: hunts the Rare Iglar toward the true Eve (2,
13-15, 105, 152, 179 -- both terms already shipped project-wide, e.g.
translation/voice_021.json), distrusts Mikage (24), invokes his mother
Oriza's Iron-C technology (74, 77), taunts a "Gundam" pilot and a
"Mechanical Angel" (Aquarion) opponent (10-12, 23, 26, 102-103, 145-152),
references Vega's giant (22, 138, 149), mentions Alicia's sacrifice (180),
and closes by addressing "winged child" and then his son directly --
"Amata... you've grown" (187) and "this Altair isn't your home anymore"
(188), matching the final battle where he confronts and reconciles with
Amata. Unit is Ahura Gnis, self-named repeatedly (66, 72-74, 142, 150),
using the brief's own glossary spelling (pt_360.json/rt_200.json call the
same unit "Afra Gnis" in prose). Recorded as "35" in
`analysis/voice_identity.json`. The brief's weapon table (母星総力戦砲 ->
Altair Cannon) matches rt_200.json's description of Ahura Gnis's finishing
move, but entry 75's budget (8 cells) cannot fit even "Altair!" alone --
shipped "Cannon!" and flagged. Other budget-forced compression: entry 3
("一刻も早く最強のレア・イグラーを見つけねばならん…！", budget 28) dropped
"as fast as possible" for "Find the best\nRare Iglar!"; entry 146 ("勝たね
ばならん…！私は機械天使に！", an incomplete Japanese sentence, budget 18)
shipped the literal fragment "I must win! I must" since the source clause
itself trails off; entry 148 ("たとえ、翼持つ子が乗っているのだとしても…！",
budget 24) compressed to "Winged child\nor not...!", losing the
"even if" conditional framing. No twin section (work/voice/clusters.json
lists `[35]` alone). Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/035.json`, 0 problems, 119 of 119
answered. `tools/merge_voice.py 35` run -> `translation/voice_035.json`.

**Voice: section 060 is Kan Yu, 118 lines** -- filed unit UNKNOWN, no
weapon-table match at all (score 0). The speaker refers to himself in the
third person with bravado as "このカン・ユー様" (this Kan Yu-sama, entries 6,
26), matching source/library/pilots.json i=35 (VOTOMS): Kan Yu, AT squad
captain of Assemble EX-10, described as petty and cowardly, who flatters
his superior Gon Nu while bullying his subordinates including Chirico, and
who in the end pointed a gun at Chirico's group out of self-preservation
before Shako stopped him and was called "human trash." This section's
content matches exactly: grandiose bravado collapsing into cowardice under
pressure (59 "N-no good! Ejecting!", 60 "H-help meeee!", 162 "I won't die!
Never"), a grudge against Chirico addressed or referenced by name
repeatedly (81, 137, 138, 144), bitterness at Shako specifically for
turning on him (84 "Shako, traitor", 146 "Stop, Shako! Your old CO!"),
blaming Chirico for ruining his life (75, 82 "you wrecked my life", 83),
and post-Kumen-Kingdom opportunism as a "Balarant soldier" (76) chasing pay
and postings (89 "kill Gundam, jobs await"). analysis/glossary.json
confirms Kan Yu, Shako, Chirico, Nextant (an enemy he vows to expose, 85)
and Niva. Recorded as "60" in `analysis/voice_identity.json`.

FLAG -- a block of entries (132-133, 161-171) addresses or discusses
someone as "Niva-sama" respectfully ("For you, Niva" 132, "Niva, get back"
133, "Niva, time to stop" 163, "Orders above" 164, "Soldiers obey!" 165)
and later mocks a defeated enemy while asserting independence (166-171).
Plausibly Kan Yu again -- Shako's own bio (source/library/pilots.json)
notes she kept helping in "battles against Niva" after the Kumen Kingdom's
fall, and Kan Yu's established trait of flattering whichever superior
currently commands him (he flattered Gon Nu earlier) fits an aide serving
Niva just as well. Not confirmed by a screenshot; could instead be a
second, unnamed voice bundled into the same file (the pattern seen at
section 13's Asuka/Misato pair). No unit/mecha name is self-referenced
anywhere in the section (only a claw/pincer weapon at 126 and
piercing/skewering imagery at 93-94, suggesting a crab- or lance-armed AT,
but nothing in robots.json ties a named machine to Kan Yu), so unit ships
null/unresolved. Budget-forced compression: entry 6 ("このカン・ユー様の指揮
に間違いはない！", budget 19) dropped the third-person self-address for
"Kan Yu never errs!"; entry 82 ("貴様に関わってから、俺の人生は急降下だ！",
budget 22) compressed to "You wrecked\nmy life!"; entry 166 (budget 31, the
section's longest) fit "Fainted? Just a big dumb oaf!". No twin section
(clusters.json lists `[60]` alone). `python tools/check_voice.py
work/voice/answer/060.json`, 0 problems, 118 of 118 answered. `tools/
merge_voice.py 60` run -> `translation/voice_060.json`.

**Voice: section 070 is Klan Klang (Queadluun-Rhea), 117 lines** -- filed
unit UNKNOWN, no weapon-table match. The brief's own glossary (Klan Klang,
Michel, Canaria, Klan, Alto, Ozma) points to Macross Frontier; the speaker
self-identifies directly at entry 49 ("クラン・クランだ！援護する！" -- I'm
Klan Klang! Providing support!). source/library/pilots.json i=175 confirms
Klan Klang, S.M.S. Pixie Squadron captain, 18, a Zentradi-pride pilot who
commands the all-Zentradi Pixie Squadron in a crimson Quadran-Rea (shipped
as "Queadluun-Rhea" in translation/library/rt_120.json) and is "always
concerned about" childhood friend Michel -- matching this section's rough
Zentradi-pride bark family (0-27, 109, 112, 132) laid over direct-address
squadmate banter naming Alto, Michel, Luca, Ozma and Canaria by name.
Entries 127-128 are untranslated Zentradi/Zentran war-cries ("ホルト・テーズ",
"ホルト・ダンツ・ゼントラン"), shipped as romanized transliterations ("Holteez!",
"Holt Zentran!" -- the latter drops "Dantz" purely for a 14-cell budget,
no semantic loss since it's an alien battle-cry, not real Japanese).
Entries 175-185 are a separate tsundere block, shifting from a combat
pep-talk into a stammering denial addressed to "貴様" (a familiar, rough
"you") that closes on an explicit "this is a superior officer's order!" --
read as Klan (Michel's superior officer, and canonically his eventual
love interest across the Frontier story) ordering him to rest while
denying any personal motive; no name appears in 175-185 itself, so this
is inferred from register and the established relationship, not
confirmed in-line. Budget forced real meaning loss, flagged in the
translator's report: entry 65 "Konig's no good!" drops addressee
"Canaria"; entries 57/66 drop the ship name "Quarter"; entry 178 (the
section's longest budget, 54 cells) compresses the full tsundere
confession to "N-not like I want you near! Time to teach discipline!";
entry 179 drops the closing "Got it?!" to fit "Argh! Break, now! That's
an order!". Recorded under "070" in analysis/voice_identity.json. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/070.json`, 0 problems, 117 of 117 answered. Not yet
merged into translation/.

**Voice: section 110 is Teitania da Monte-Wells (Order Buckler), 113
lines** -- filed unit UNKNOWN, no weapon-table match. The brief's glossary
(Chirico Cuvie, Martial, Nextant, Fyana, Chirico, Gura) points to VOTOMS;
entry 0 is a direct self-introduction ("私はネクスタント。そして第１３階位秩序の盾だ"
-- I am a Nextant. And the 13th Rank, Shield of Order), matching
source/library/pilots.json's Teitania da Montewells (テイタニア・ダ・モンテ＝ウェルズ,
translated in translation/library/pt_040.json/rt_000.json), the 13th rank
"Shield of Order" who pilots the Order Buckler and was modified into a
Nextant by her father Lord Monte-Wells -- confirmed by entry 167's
"Sorry, Father...!" and her pursuit of Chirico by name throughout (29,
30, 134, 154, 171), including calling him "Untouchable" (32, 155, 169),
the term already shipped for 触れ得ざる者 in translation/voice_017-019.json
and translation/stage0010_03/04.json. Entry 174 is a non-Japanese
liturgical chant embedding グーラ/Gura (the glossary's fifth term) inside
オワグーラ -- not real Japanese, so it ships as a romanized transliteration
("Du Oste Owagura Yashidiro Gratzi Mito") rather than a translation, two
trailing words dropped purely for a 39-cell budget. Entry 172 is a
fourth-wall Easter egg ("中断していたお前のスパロボはクリアしておいてやったぞ" -- I cleared
your suspended Super Robot Wars for you) addressing the player about
their save file, the same idle/meta-gag pattern already flagged for
Gamlin's section. Budget forced real meaning loss, flagged in the
translator's report: entry 29's full glossary name "Chirico Cuvie" (13
cells) does not fit a 12-cell budget and ships as "Chirico C.!"; entry
135 drops the "Untouchable" epithet entirely to ship bare
"Disappointing!"; entry 161 truncates her own title "Shield of Order" to
"Shield" in "Shield weeps now!"; entry 128's creed ("Order is the will of
God, maintained only through power") compresses hard into "God's
will,\norder w/force". Recorded under "110" in
analysis/voice_identity.json. Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/110.json`, 0 problems, 113 of 113
answered. Not yet merged into translation/.

**Voice: section 66 is a Garencieres crew pilot, probably Flast Scoal, 113
lines** -- filed as Gundam Mk-II by weapon call-out, score 1.0 (one hit only,
on "shield", a part every mobile suit carries -- the weakest kind of match).
Content is Sleeves (Neo Zeon remnant) from Mobile Suit Gundam Unicorn: the
speaker fights "Gundam" (never named Mk-II) and addresses Banagher Links by
name three times (75, 80, 122, 149), accuses him of betraying the colony
(78), and protects Marida Cruz by name (98, 104-105). Two different
superiors are addressed under two different titles -- "Captain" (97, 99)
and "Colonel" (99, 106) -- matching Suberoa Zinnerman (Garencieres' captain,
this project's voice_135.json) and Full Frontal (colonel rank,
voice_029.json/voice_189.json) respectively; source/library/pilots.json
independently confirms Zinnerman's own crew call him "キャプテン" specifically
(not 隊長), which places the speaker on the GARENCIERES crew, not Frontal's
Personal Guard (the distinct identity already shipped for 029/189/190, who
address only Frontal/Angelo and never a "Captain"). Entry 76's personal
grudge against "Gundam" and entry 108's jab at the Guard (implying the
speaker isn't part of it) both fit Flast Scoal specifically -- pilots.json
describes him as a Garencieres crewman personally embittered at Banagher for
killing his comrade Gilboa Sant, trusted like a big brother by the crew.
No line self-names the speaker, so this is recorded as probable, not
certain; unit left unresolved (no mobile suit is on record for Flast, and
the weapon match is worthless). Recorded under "66" in
analysis/voice_identity.json. Budgets were severe -- several name-address
lines had to drop the name to fit ("Banagher!" alone at 80; "Banagher no" at
149, missing its comma to make budget) and some lost their referent
entirely (81's shield-block became "Blocked it!", 96's "another angle"
became "New angle!"). Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/066.json`, 0 problems, 113 of
113 answered. Not yet merged into translation/.

**Voice: section 95 is Suzaku Kururugi's Lancelot Albion, 113 lines** --
filed by weapon call-out at score 2.5 (Suzaku/Lancelot Albion), and this
time the match is right: confirmed by content, not just trusted on the
score, since the brief's own warning (a similar mid-range score was flatly
wrong for section 8) made that worth checking. The lines are unmistakably
Suzaku from Code Geass R2 -- his canonical humble self-reference "自分"
throughout, grief/atonement lines naming Euphemia by her nickname Euphie
directly (1, 5, 6, 14, referencing his post-Euphemia-massacre arc), support
exchanges naming Lelouch (67, 71) and Kallen (68, 72) and C.C. (107, 108),
the unit's own glossary weapons Varis and Energy Wing (37, 106) plus Hadron
Mode (33, 37), the Geass-curse-compelled-to-live thread (83-85, 141, tied to
Lelouch's R2 command that Suzaku live), and the ship name Albion itself (3,
105, 140). Recorded under "95" in analysis/voice_identity.json as a
confirmation. Budgets were punishing throughout -- almost every line needed
compressing to a single short clause or bark ("Ready?!", "No falling!"),
entry 76's "Energy Filler" swap lost its "Energy" ("swap the Filler!"),
entry 106's Energy Wing name-check compressed to "Wing's speed then!", and
entry 99's "Yggdrasil Drive" was dropped to generic "The Drive" -- all
flagged in session notes as meaning lost to budget. Not confirmed by a
screenshot. `python tools/check_voice.py work/voice/answer/095.json`, 0
problems, 113 of 113 answered. Not yet merged into translation/.

**Voice: section 195 (and verbatim twin 196) is Emperor Zul, commanding the
weekly Fighting Mecha against Godmars, 112 lines** -- filed unit UNKNOWN, no
weapon-table match (pts 0.33). Content is the overarching villain of Six God
Combination Godmars, not any single mecha's own pilot: the speaker boasts of
wielding psychic power ("俺の超能力", entries 8, 10, 45) and reading the
opponent's mind (9, 44), and frames the stakes on a cosmic scale -- "Kill
Mars!" tied to Earth's survival (14), "Kill Godmars, win!" (16) -- language
no mere monster-of-the-week pilot would use. It addresses "マーズ"/Mars
(Takeru's psychic alias) with personal contempt throughout (13-19, 47,
57-58, 65-67, 76) and calls Roze a traitor (18, 48), consistent only with
Zul, the one figure both Marg and Roze defected from per
translation/library/pt_000.json's bios. The section's own glossary is three
different named Fighting Mecha from three different episodes (Daedalos,
Buffle, Zedfiner, per source/library/robots.json), each addressed in the
THIRD person as a summoned instrument ("Zedfiner, bury him!" 89; "Buffle
sends you!" 88) rather than as the speaker's own machine -- exactly how Zul
commands his rotating weekly monsters instead of piloting one himself.
analysis/glossary.json files Zul as a "keyword", not a "pilot" entry: he has
no dedicated mobile suit in the roster, which is why this voice set attaches
to the generic recurring Fighting Mecha slot. Recorded under "195" and "196"
in analysis/voice_identity.json (196 confirmed 100% verbatim twin of 195 by
direct comparison of both sections' non-shared Japanese lines; only 195 was
translated, to be carried to 196 by tools/voice_propagate.py matching on
Japanese text). Budgets were severe throughout -- most lines are single
shouted words ("Now!", "Vain", "Mine!") -- and several lines lost their
named referent to fit: entry 122's "galaxy" survives as "stars", entry 20
drops the "small mechs" translation to an idiom ("Small fry, away!"), and
a handful of near-identical "don't scorn this mecha" pairs (56/64) and
"damn Mars" pairs (65/80) were deliberately varied so the same English
never covers two different Japanese lines. Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/195.json`, 0 problems, 112 of
112 answered. Not yet merged into translation/.

**Voice: section 107 is Darry Adai's Space Gunmarl, 111 lines** -- filed as
Gundam Mk-II by weapon call-out, score 2.0, and wrong, the same weapon-magnet
trap as the other 24 sections that unit collects. The section's glossary
(Anti-Spiral, Gurren Lagann, Dayakka, Mugann, Yoko, Kittan, Gimmy, Simon,
Darry) is pure Tengen Toppa Gurren Lagann sequel-era cast, and entries 0-19
are byte-identical Japanese to shipped section 62 (Gimmy Adai's own voice
set) entries 20-39 -- a verbatim shared combo-attack exchange already
identified and shipped from 62's side, whose note there names 107 as
Darry's own voice set and calls that English final; those 20 lines were
reused verbatim rather than retranslated. Darry's own half of the exchange
is feminine (-wa/-yo/-dakara endings), matching Gimmy's masculine -ze/-zo
half exactly as predicted. Outside the shared block, the speaker self-names
("Darry Adai, go!", entry 27), addresses Simon respectfully (26, 72, 81),
praises Yoko and Kittan as squadmates (42, 73, 74, 82, 83), repeatedly
worries about Gimmy's recklessness (28, 70, 79), fights the Anti-Spiral and
the faceless Mugann directly (33-38), and pilots a unit named "Gunmarl" in
several lines (54, 90, 99, 113) -- translation/library/rt_200.json ships
"スペースガンマール" as "Space Gunmarl", already used in both full and short
form in section 62 ("Go, Space Gunmarl!" / "Tough Gunmarl!"), so the same
short form carries over here for budget. No Gundam content anywhere.
Recorded under "107" in analysis/voice_identity.json. Budgets were savage
(many single-digit-letter slots): entry 34's "faceless thing" description
of Mugann drops out to plain "Not losing here!", entry 123's "barrier"
detail is lost to bare "I'm fine!", and entry 115's "Gimmy" vocative is
lost to "So sorry!" -- all three flagged. Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/107.json`, 0 problems, 111 of
111 answered. Not yet merged into translation/.

**Voice: section 098 is Seina, co-piloting Behemoth with Kugayama Takuma,
109 lines** -- filed unit UNKNOWN, no weapon-table match. Speaker is female
(wa/kashira endings) who commands "Takuma" by name in the early, villainous
half (entry13 "Go, Takuma! Destroy all!"; entry14 "Takuma, clear them!" --
terrorist rhetoric about painting a "peace-soft world" their color, entry8;
revenge, entry10), then fights beside him as a comrade in the later half
(entry174 "Takuma fights- so do I!"; entry175 "If I go, Takuma!").
source/library/pilots.json i=263 identifies Seina as leader of terrorist
group A21 who commands Takuma -- who believes she is his older sister --
to pilot Behemoth (i=264); her bio notes she shows a human side once
captured, matching the file's turn from cold commander to self-sacrificing
ally. work/voice/mech_pilot.json credits Behemoth's pilot as Kugayama
Takuma alone, so these lines are Seina riding as his co-pilot/commander in
the same unit -- one unit's voice set split between two speakers, the same
situation as Beck's henchmen at section 145. Entry83 ("援護するわ、張五飛" --
support you, Wufei Chang!) confirms an ally-phase alongside the Gundam Wing
pilots; entry40 addresses an opponent from the Black Knights (Code Geass,
term already shipped elsewhere in translation/), both consistent with a
late-game crossover roster. Recorded under "098" in
analysis/voice_identity.json. Two glossary terms lost to budget: entry37's
"21st Century Security" (20 letters, 16-letter budget) ships as generic
"Their robot?", and entry83's "Wufei Chang" (11 letters, 10-letter budget)
ships as bare "Backup!" with the name dropped -- both flagged. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/098.json`, 0 problems, 109 of 109 answered. Not yet
merged into translation/.

**Voice: section 183 is Wufei Chang's Nataku (Altron Gundam), 110 lines** --
filed unit UNKNOWN, no weapon-table match. Entries 71-78 address each of the
other four Gundam Wing pilots by name and take over their fights as a
teammate would ("Heero, go!", "Duo, mine!", "Trowa, mine!", "Quatre, go!",
"Heero! Mine!") -- only a fellow Gundam pilot addresses all four by name
mid-battle. Entry0 addresses the speaker's own unit by name ("Lock on,
go!! Nataku"), repeated at entries 5, 11, 33, 40, 44, 115, confirming
Nataku is the speaker's mobile suit, not an opponent's. Register is
hot-blooded and justice-obsessed throughout ("I define justice!!" entry6;
"My enemy is all evil that brings war to space!!" entry47), matching
source/library/pilots.json i=80's profile of Chang Wufei (Gundam Wing:
Endless Waltz), raised on the creed that strength alone is justice.
work/voice/mech_pilot.json independently maps Altron Gundam to Chang
Wufei, and the glossary (Duo, Trowa, Heero, Quatre) matches the four
teammates addressed by name. Recorded under "183" in
analysis/voice_identity.json. No unresolved lines; budget forced the
"Nataku" name out of a couple of lines about the unit itself -- entry5 and
entry33's 10/11-letter budgets can't hold the 6-letter name plus a verb,
so they ship as "No joke!!" and "No mockery!" instead, and entry67
collapses plural "traitors" to singular "traitor" for the same reason. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/183.json`, 0 problems, 110 of 110 answered. Not yet
merged into translation/.

**Voice: section 203 is the Getter Robo trio (Ryoma Nagare, Hayato Jin,
Benkei Kuruma), 106 lines** -- filed as Lancelot Frontier (C.C.) by
weapon-name match, score 1.0, and wrong, the same trap as section 8's
Strike Freedom mismatch. Content names 真ゲッター３/Shin Getter 3 directly
(entry 3), the attacks are Getter-3's signature Missile Storm and
Daisetsuzan Oroshi (34-42), and entry 127 is the seat-change call "Change!
Getter 3!". Most lines command 弁慶/Benkei by name in the second person
("Benkei, finish it", "Benkei, switch with me" -- 8, 13, 24, 26, 110, 114,
122, 124), reading as Ryoma directing him; entry 15 separately addresses
"竜馬、隼人" (Ryoma, Hayato) together, and 39-42 have the speaker calling an
unnamed 先輩/senior "Senpai" while using a move "taught directly" by them --
this is a shared ensemble bark bank for the Getter-3-formation team, not
one pilot's cockpit alone. Shipped without inventing a name; all three
pilots are named in-line by the Japanese itself. Recorded under "203" in
analysis/voice_identity.json. Budgets were savage for the weapon
call-outs: "Missile Storm" (entry 34, budget 9) could not fit at all and
shipped as "Missiles!"; "Homing Missile" (35, budget 14) shipped without
the "Getter" prefix or its exclamation mark; "Daisetsuzan Oroshi" (18
letters) never fit any of its three call-outs (38, 40, 42, budgets 14/11/17)
and shipped as "Daisetsuzan!!" / "D. Oroshi!" / "Daisetsuzan! Ooh!" instead
-- flagged here since rule 5 (shipped weapon name) lost to rule 1 (budget)
at every one of them. Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/203.json`, 0 problems, 106
of 106 answered. Not yet merged into translation/.

**Voice: section 62 is Gimmy Adai's Black Getter, 95 lines** -- filed as
pilot "Ryouma Nagare" (流竜馬) by weapon-name match, score 1.0, and wrong:
another name collision, not Getter Robo content at all. The glossary this
section actually pulls (Anti-Spiral, Gimmy Adai, Gurren Lagann, Dayakka,
Mugann, Yoko, Kittan, Simon, Darry) is Tengen Toppa Gurren Lagann
sequel-era cast. The speaker self-names twice (entry 3, "Gimmy Adai! Here I
go!"), calls Simon "Simon-san" as a senior he wants to impress (2, 65),
needles his twin sister Darry as a rival (4, 69), and namedrops Yoko/Kittan
as squadmates (66, 67, 71). Entries 20-39 are a verbatim shared
combo-attack exchange with section 107 (Darry's own voice set -- same 20
Japanese/budget pairs at 107:0-19, confirmed by direct comparison): Gimmy's
half stays masculine register, Darry's reply half is feminine, matching
107's own glossary. That shared English should be reused verbatim for
107:0-19 when that section is translated, not retranslated from scratch.
Recorded under "62" in analysis/voice_identity.json. Budgets were tight
throughout (most lines are 8-18 letters); one hit-taken line (98, budget 30)
still needed trimming to "Fall here, can't protect Darry" to fit even with
the line break. Not confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/062.json`, 0 problems, 95 of 95 answered. Not yet merged
into translation/.

**Voice: section 44 is the Nahel Argama's bridge crew, twin of section 45,
108 lines** -- filed as unit Fatty (ファッティー) by weapon-name match, score
only 1.0, and wrong: there is no mobile suit here, every line is a warship
bridge shouting gunnery orders (各砲座/each gun battery, 本艦/this ship) and
invoking the same glossary set section 45 already ships under -- Nahel
Argama, Ra Cailum, Frontal, Banagher, Kamille, Char, Riddhe, One Year War,
Sleeves, Unicorn, Neo Zeon. 44 is 45's twin: entry 0 (敵機の攻撃、外れました！)
is the identical Japanese string as 45's entry 139, and 44:115-118 (anti-air
stations call, an officer reporting "already done, Captain") and 44:131-137
(the developer save/quit-game exchange addressed to "Captain") both parallel
scenes 45 already has (stations call, readiness report, and the same
save/quit exchange almost verbatim). Shipped as unit Nahel Argama with no
pilot name invented -- the speaker addresses "Captain" as someone else, so
is not Otto Mitas himself, most likely the XO or a gunnery officer; recorded
under "44" in analysis/voice_identity.json. Budgets were punishing
throughout (9-letter budgets common for full gunnery orders): "Mega
Particle Cannon" and "Anti-Air Machine Gun" could not fit their slots at
any of their call-outs (entries 20, 22, 24, 25, 26) and shipped as generic
"guns"/"fire" barks instead of the shipped weapon names, flagged here.
`python tools/check_voice.py work/voice/answer/044.json`, 0 problems, 108
of 108 answered. Not yet merged into translation/.

**Voice: section 188 is an unnamed Beast Men Army grunt (Gurren Lagann),
107 lines** -- unit UNKNOWN, no weapon-name match at all (score 0.5, no
weapon call-outs). The speaker names himself a beastman outright (entry
111, 獣人様のお通りだ, "make way, this is a beastman coming through"), pilots
a ガンメン/Gunmen he calls "my Gunmen" (37, 57, 122), and every taunt targets
a Gundam-type opponent by category rather than by name -- "Gundam vs
Gunmen" (10), "how many kinds of Gundam are there" (11), a bird emblem on
the rival's chest (14), "some kind of god" (17), machines that "fuse"/
combine (16) -- reading as a mob soldier taking on the SRW crossover's
assorted protagonist mecha in general, not one named rival. This project
already has a confirmed Beast Men Army character, Viral, in section 38
(self-naming, explicit rivals Simon/Gurren Lagann, glossary ships ヴィラル
as "Viral", zukan_id 310, official) -- but nothing in 188 names Viral,
Simon, or Kamina, and the register does not match: 38's Viral is a serious,
wounded warrior, while 188 swings between crude bravado ("big is fun",
"never lose") and comic cowardice (pleading for help, nosebleeds, panicked
ejection), reading as disposable mob-grunt banter rather than a named
general. Shipped as generic Beast Men Army barks with no character name
invented; recorded pilot/unit null under "188" in analysis/voice_identity.json.
`python tools/check_voice.py work/voice/answer/188.json`, 0 problems, 107
of 107 answered. Not yet merged into translation/.

**Voice: section 177 is an unnamed Space Demon King army grunt, 109 lines**
-- filed as Strike Freedom Gundam / Kira Yamato by weapon call-out (score
2.3, flagged do-not-trust) and wrong. Content is the Tetsujin No. 28
crossover's villain faction (太陽の使者　鉄人２８号): entries 19-21 name
鉄人２８号 (Tetsujin No. 28) and ブラックオックス (Black Ox) as attack
targets and call Tetsujin "our enemy" outright (20); entries 15-16 invoke
serving 宇宙魔王 (the Space Demon King); entries 33-34 order "capture
Milord Gura" then "erase Gura King Jr." -- section 176 (the Space Demon
King's own voice set) independently confirms Gura is the King's son. Same
army as section 108 (General Duncan) and 176 (the Space Demon King
itself), but none of these 109 lines self-identify a speaker -- no name,
no first-person title, only generic "本機" (this unit) -- and the target
list runs across far more franchises than one story arc would need
(Mobile Suit, Gundam, Variable Fighter, AT, AS, KMF, android, enemy
warship, on top of Tetsujin/Black Ox/Mars-Godmars/Earth Super Robots),
reading as a reusable mob/grunt bark table rather than a named pilot's
lines. Recorded pilot/unit null under "177" in analysis/voice_identity.json
(and "178", a verbatim twin of this table -- same 109 (Japanese, budget)
pairs reindexed -- which ships this English by propagation rather than a
separate pass). Glossary terms used verbatim where budget allowed (Black
Ox in full at 21/92/121, Gura at 33/34) and compressed where it did not:
"Tetsujin No. 28" -> "Tetsujin" (19/91/120), "Space Demon King" -> "King"
(15, matching section 108's precedent), "Gura King Jr." -> "Gura King"
(34, dropping the "Jr." suffix to fit budget 15), Godmars/マーズ -> "Mars"
(22/93/122, matching the short form section 108 already shipped). `python
tools/check_voice.py work/voice/answer/177.json`, 0 problems, 109 of 109
answered.

**Voice: section 46 is Yonem Kirks, Zaku I Sniper Type, 95 lines** -- filed
as Gundam Mk-II by weapon call-out (score 1.0, flagged do-not-trust) and
wrong: the "Gundam" named throughout (14, 74-76, 109, 111-112) is addressed
in the third person as the enemy, so the speaker cannot be riding it.
Content is a Zeon-remnant One Year War veteran comparing an old memory of
Gundam to this "quite different" one (74) and mocking it by the nickname
"split-horn Gundam" (16, 29, 76). Entries 59-62 and 134/137 protectively
address an ally by name -- Loni Garvey (source/library/pilots.json i=151,
Gundam Unicorn's 18-year-old Zeon-remnant Shambro pilot) -- ending in a
dying warning (137, "Loni...! You...! Don't end up like us!!").
pilots.json i=152 (Yonem Kirks) is an exact match, not Loni herself: leader
of the Zeon Remnant Army after Mahdi Garvey's death, a father figure to
Loni, sniping from the rear in a Zaku I Sniper Type (robots.json i=96)
while directing the battle -- and his bio's own ending ("he died fighting
Ra Cailum's Tristar, but his will stopped Loni's rampage") is exactly the
death scene translated at 135-137. Glossary ships ロニ as "Loni" (not
"Roni") and ヨンム・カークス as "Yonem Kirks" (pt_120.json; rt_080.json's
"Yonmu Kirks" not followed) -- both used verbatim. Recorded under "46" in
analysis/voice_identity.json. Budget forced meaning loss at several
entries: 17 dropped the explicit "one-shot kill on the transformation
mechanism" to "Hit its weak spot"; 29/76 kept the "split-horn" nickname but
dropped the attached taunt; 59/62 compressed Loni's name-address lines to
bare "Calm Loni" and "Loni?!". Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/046.json`, 0 problems, 95 of 95
answered.

**Voice: section 55 is Canaria Berstein, VB-6 Konig Monster, 97 lines** --
unit UNKNOWN, no weapon call-out matched; the brief's own glossary (Michel,
Canaria, Ranka, Alto, Ozma) already points to Macross Frontier's movie cast
(Sayonara no Tsubasa). Self-identifies twice by callsign and name: entry 2
("Canaria's unit, commencing attack") and entry 41 ("This is Canaria!
Lending a hand!"); callsign "Rabbit 1" recurs at 0, 40, 85. Entries
48/52/59/71/75/78/86 repeatedly name her own machine Konig, matching
source/library/robots.json i=130 (PLTN Canaria Berstein) and
pilots.json i=177 (S.M.S. Skull Squadron Lieutenant, a doctor who also
serves as combat medic, "normally quiet, but has an adult woman's
consideration" -- matching the section's controlled register throughout).
This is an ensemble support file: entries 42-52 and 106-116 are two-sided
squadmate banter bundled into her own bank -- she addresses Michel (43,
50), Luca Angeloni (44, 51), and Ozma Lee (42, 49) by name, and a "Captain"
pairing at 45/52 most likely reads as Klan Klan (pilots.json i=175/176,
Pixie Squadron's captain); 106-116 shifts to supporting Alto Saotome
directly, referencing Ozma entrusting him his YF-29 (107, 110) and covering
Pixie Squadron (108, 111). UNVERIFIED: entries 13 and 80 both invoke
"Eddie" for strength, and 80 pairs it with "Mom" -- no pilots.json,
robots.json, or glossary entry for "Eddie" was found, so it ships as the
bare transliteration; whether "Mom" is a squadmate nickname for Canaria or
something else could not be confirmed. Recorded under "55" in
analysis/voice_identity.json. Budget forced real meaning loss: entry 43
could not hold "Michel" at all in a 10-cell budget and ships nameless as
"Leave it"; 106 could not hold "Alto" in a 7-cell budget and ships as "No
rush"; 109 dropped "Alto" for "Not alone!"; 45 dropped the explicit
"woman's pride" phrase for "show 'em!". Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/055.json`, 0 problems, 97 of
97 answered.

**Voice: sections 135, 109** — the Rewloola's bridge crew (Neo Zeon
flagship orders, no single speaker; unit-level identity per the crew
convention) and Tieria Erde's Raphael Gundam (self-named at entry 29;
the filed Lancelot/Suzaku match was a duplicate of section 4's
legitimate one). Mega Particle Cannon and Quantum Brainwaves both
overflow their tightest slots and ship shortened there, full elsewhere.

**Voice: section 041 is Emma Sheen on Gundam Mk-II, 92 lines** -- brief's
own weapon-name match (unit ジェミニア/Geminia, pilot Gadlight Meonsam, score
1.0) was wrong, exactly the failure the brief itself warns of (section 8
scored 7.5 and was still wrong). Content is unmistakably Mobile Suit Zeta
Gundam: the speaker identifies herself on comms as 'こちらエマ機'/'こちらエマ'
(this is Emma's unit / this is Emma, 39, 85, 91) and as 'エマ、ガンダムＭｋ－
Ⅱ、仕掛けます' (Emma, Gundam Mk-II, engaging, 93), and addresses named Zeta
Gundam cast by their shipped glossary names throughout -- Kamille (101-103,
109), Captain Quattro (104-105, 110), Captain Amuro (106-107, 111), Captain
Bright (112), Katz (108, 113) -- plus a direct callout to Scirocco as "the
man back from Jupiter" (35). This is Emma Sheen, Gundam Mk-II's pilot.
Recorded under "41" in analysis/voice_identity.json; feminine register
(わ/ね/なさい) used to keep her voice distinct only, no pronoun inferred from
it per rule 7 -- unnecessary anyway since every line is first-person or
names someone else by name. Budget forced real meaning loss repeatedly: the
glossary's full 'Gundam Mk-II' (12 cells) never fits any of this section's
budgets and ships as 'Mk-II' everywhere it's named (93, 94); entry 35 drops
"the man back from Jupiter" and ships bare 'Scirocco...!'; entries 101 and
104 drop the explicit "I'll cover you" verb and ship bare 'I'll cover!' /
'Quattro!'; entry 46 compresses "the only choice is to fall back and buy
time" to 'Fall back, stall'; entry 63 swaps "better than I expected" for
the shorter understatement 'Not bad...!!'. `python tools/check_voice.py
work/voice/answer/041.json`, 0 problems, 92 of 92 answered.

**Voice: section 104 is Takuma Kugayama on Behemoth, 91 lines** -- brief
filed unit UNKNOWN, no weapon-table match. Content resolves to Takuma
Kugayama piloting Behemoth: this section's own glossary lists Behemoth
(ベヘモス) and Sousuke Sagara (相良宗介), the speaker calls himself the
"chosen warrior" (選ばれた戦士, 8, 121) and names his own machine Behemoth
repeatedly (25, 100, 104, 119, 144, 148-149, 155, 158), singles out Sousuke
Sagara by name as a personal enemy (23, 129), and cries out to "姉さん"
(sis) while dying (7, 141-143, 150) -- matching analysis/voice_identity.json's
existing note on section "0" (also Takuma Kugayama/Behemoth, also unit
UNKNOWN) that lines addressing Takuma by name there are likely Seina's
paired responses, and analysis/glossary.json confirms Seina is Takuma's
Full Metal Panic co-castmate. Very likely the same character as section 0
but a distinct voice bank at an earlier story beat: this file's register is
a mocking, self-declared-invincible villain (taunting Code Geass' Black
Knights as Federation lackeys at 33, an Odaiba "salaryman" company robot at
26-27/132, a Gundam pilot at 32) that curdles into panic and pain addressed
to "姉さん" once Behemoth is disabled (141-150), rather than section 0's
mentor-death/A21 material -- flagging the link for whoever next touches
either section, since section 0 was not re-read to confirm it. Recorded
under "104" in analysis/voice_identity.json. Budget forced real meaning
loss repeatedly: entry 23 can't hold the full shipped name "Sousuke Sagara"
(13 cells) and ships surname-only, 'Sagara...!'; entry 33 shortens "Black
Knights" to plain 'Knights' and "Federation" to 'Feds' ('Knights serve
Feds!'); entry 35 drops "change the world" entirely ('You tried too...!');
entry 106 compresses the idiom "pointless self-satisfaction" to 'So
pointless\nself-love'; entry 129 drops "how dare you" and ships 'Damn
Sagara!'; entry 143 drops the "sis" address that entries around it keep
('Don't leave me!'). `python tools/check_voice.py
work/voice/answer/104.json`, 0 problems, 91 of 91 answered.

**Voice: section 108 is General Duncan, 90 lines** -- brief filed unit
Strike Freedom Gundam / pilot Kira Yamato on a weapon-match score of 2.3 and
explicitly warned not to trust it (a beam-rifle/vulcan collision, the same
trap that caught sections 8 and 141). Reading the content confirms it is
wrong: the speaker self-identifies by name and title in entries 7, 8, 12,
61, 78, 103, 119 ('魔人将軍ダンカン'/'魔人将軍', Demon General Duncan), and
addresses the enemy directly as 'ブラックオックス' (Black Ox) and
'マーズ'/'ゴッドマーズ' (Mars/Godmars) -- confirmed OPPONENT names, never
claimed as his own. He protects someone addressed 'グーラ殿下' (65, 68:
covers them, tells them to retreat), then retreats himself near the end
(124, 127, 128) and begs forgiveness from '宇宙魔王' (the Space Demon King)
in 125. This is General Duncan, an antagonist commander from the 1976-77
anime Six God Combination Godmars, not Strike Freedom Gundam / Kira Yamato.
No robots.json entry names Duncan's own mecha in this game's library, so
unit is left null in analysis/voice_identity.json. Budget forced real
meaning loss: entries 11, 120 and 125 could not fit the glossary term
'Space Demon King' (16 cells) alongside the rest of the line and drop or
abbreviate it; entry 52 could not fit 'Small Saucer' (12 cells, the exact
budget) plus a verb and drops the term entirely. `python tools/check_voice.py
work/voice/answer/108.json`, 0 problems, 90 of 90 answered.

**Voice: section 144 is Count Brocken, 90 lines** -- brief filed unit
UNKNOWN, no weapon-table match. Entry 5 is a direct self-introduction ('I am
the one entrusted with one of the Five Great Corps... I am Count Brocken').
Entries 7, 8, 22, 77, 86 refer to 'my/our Ghoul' as his own vessel,
including a defensive line about the Ghoul itself being shot down. Entries
4, 93, 94, 118 establish him as Dr. Hell's subordinate ('for my master Dr.
Hell's dream', apologizing directly to 'Dr. Hell!' on defeat). Entries 10,
11, 61, 62, 83, 101 fix Mazinger Z / Kouji Kabuto as his targets, matching
the brief's glossary; entries 63 and 84 address a young lady
('お嬢さん'/'小娘') as a secondary target, consistent with Sayaka Yumi in the
Mazinger Z cast but never named in these lines, so rendered generically
('Miss'/'a girl') rather than guessed. Entry 108's mention of retreating to
'Bardos Island' (Dr. Hell's base in Mazinger Z canon) is consistent, not
contradictory. Identified as Count Brocken, one of Dr. Hell's generals
piloting the flying robot-beast Ghoul, from the original 1972-74 Mazinger Z
anime; recorded with unit 'Flying Fortress Ghoul' in
analysis/voice_identity.json. Budget forced real meaning loss: entry 8
could not fit the full glossary term 'Flying Fortress Ghoul' (22 cells for
the bare name alone) inside a 23-cell two-line budget and drops to 'the
Ghoul'; entry 5 drops 'Five Great Corps' to a bare numeral; entry 62
collapses 'Mazinger Z' to bare 'Z' in the second line; entry 101 drops the
explicit 'Mazinger Z' mention, keeping only the 'Pilder' target it implies.
`python tools/check_voice.py work/voice/answer/144.json`, 0 problems, 90 of
90 answered.

**Voice: section 192 is Ryunosuke Akagi, 86 lines** -- brief filed unit
UNKNOWN, no weapon-table match. The speaker self-names in full at entry 102
('Ryunosuke Akagi.'), matching source/library/pilots.json i=260 (CHFN
赤城龍之介): the narcissistic captain of the Nerima base's AS unit, the
self-styled Nerima Red Dragon, who addresses women as 'Lady' throughout (27,
101). The recurring insult アカテン/'Akaten' (30, 32, 105, 106, 132, 149) is
his own hated nickname -- translation/library/pt_200.json already ships "he
has called him 'Akaten' (failing grade)", from his old instructor; here he
flings it back at his current opponent, and losing (149) means it sticks to
him again, playing against his own claimed Crimson/Red Dragon identity. No
robots.json entry lists him as PLTN, so no unit name exists to call out;
recorded under "192" in analysis/voice_identity.json with unit left null.
Budget forced real meaning loss at 133 (26 cells couldn't hold both an
exclamation and the 21-letter '21st Century Security' plus the "robots are
monsters!?" comparison, which was dropped -- ships as 'Ugh!\n21st Century
Security') and at 132/149 where 'Akaten' itself sometimes had to be dropped
for a same-theme substitute ('Flunk if beaten' at 132). `python
tools/check_voice.py work/voice/answer/192.json`, 0 problems, 86 of 86
answered.

**Voice: section 162, 87 lines** -- brief filed unit ARX-7 Arbalest / pilot
Sousuke Sagara by a middling weapon-name match (score 1.5) and warned this
exact pattern was flatly wrong before (section 8 scored 7.5 for Strike
Freedom and was a Full Metal Panic mercenary). Same trap here: this is not
Sagara's own voice bank but a Full Metal Panic enemy who talks about him and
Mithril in the third person (24 'That's... Sagara?', 118 'Sagara, tougher').
The speaker is female, devoted to a 'Sensei' (7, 80, 84, 95, 125, 129), and
worried over a named ally 玉蘭 (81, 86, 130). source/library/pilots.json
i=294 (CHFN 夏玉芳) matches exactly: devoted to her twin younger sister 玉蘭
and to ガウルン ("Sensei") who trained her; robots.json i=189/191 list her as
pilot of a Zy-98 Shadow and later a stolen Lambda-Driver-equipped Kodar-m,
matching the Lambda Driver lines (105, 135, 137). Identified as Xia Yu Fan
(玉芳 -> Yu Fan / Xia Yu Fan per analysis/glossary.json); her twin Yu Lan
(玉蘭) is voiced separately in section 175, still untranslated. Recorded
under "162" in analysis/voice_identity.json with unit left null (she flies
two different frames across the story). Budget forced real meaning loss
repeatedly: 'Lambda Driver' (13 cells) exactly fills entry 105's budget;
entries 135/137 couldn't hold the full term and drop 'Driver' ('Lambda on',
'Use Lambda'); entry 118 can't fit 'Sousuke Sagara' (14 cells) plus any
reaction and drops the first name ('Sagara, tougher'); entry 28 can't hold
'Mithril' (7 cells) in a 5-cell budget and drops it entirely ('I see');
entries 0 and 3 (2-cell budgets) ship as bare 'No' and 'Go', keeping only
the hostile register; entry 130 (3 cells) can't hold 'Yu Lan' and ships as a
truncated 'Yu!' cry; entry 129 (10 cells) can't hold both 'Sensei' and
'sorry' and drops the address. `python tools/check_voice.py
work/voice/answer/162.json`, 0 problems, 87 of 87 answered.

**Voice: section 138 is Four Murasame piloting the Psycho Gundam, 76 lines**
-- filed as Nu Gundam / Amuro Ray (2.0) via Fin Funnel/Funnel call-outs
(entries 14, 16, 19, 21), the same trap section 56 already documented for its
own leftover Funnel lines. The content is not Amuro's: it addresses Kamille
Bidan by name throughout (6, 55, 116-119), and section 56 independently
confirms the pairing -- Kamille's own voice set has him cry "No! Not you,
Four!" at its entry 181 (`translation/voice_056.json`). The speaker fits Four
Murasame (`source/library/pilots.json` i=54, Psycho Gundam's pilot) beat for
beat: entry 132 ("My head!\nPressure!") is her canonical mind-control
headache; entries 101/121/128/130 track Newtype "pressure" throughout,
matching her bio's "strong headaches from the mind-control wave"; entry 134
("We're not tools!") matches her being an unwilling Cyber Newtype weapon;
entry 119 ("Guard Kamille!") and 55 ("Kamille!!") are her canonical turn and
death cry, sacrificing herself for him in both the TV and film versions.
Entry 135 ("Kamille's ride shows power!") echoes Kamille's own section-56
entry 62 ("Zeta shows the soul!") -- two halves of the same scene. Already
shipped as "she" and as pilot of "the Psycho Gundam"
(`translation/library/pt_040.json` i=54); both reused verbatim. No
`robots.json` entry exists for the Psycho Gundam in this game, so the
Funnel/Fin Funnel lines are flagged, per section 56's precedent, as likely
misrouted/leftover pool strings rather than genuine attacks; entry 97 ("I too
can handle the Zeta Gundam") was compressed to "I fly Zeta!" -- budget 13
could not hold "Zeta Gundam" plus any verb, so only the shorthand survives,
flagged. Recorded under "138" in `analysis/voice_identity.json`. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/138.json`, 0 problems, 76 of 76 answered.

**Voice: section 136 is Hilde Schubaker, unit unresolved, 74 lines** -- unit
UNKNOWN, no weapon call-out matched. Content is unmistakably Gundam Wing's
Mariemaia-rebellion defense of the Sank Kingdom: the speaker individually
addresses, by name, every defender of that arc -- Heero (9, 21), Duo (8, 16,
19, 20), Quatre (10, 22), Trowa (11, 23), Wufei (12, 24), Noin with the -san
honorific (13, 25), and Zechs with -san (104, 116) -- one support/cover/fall-
back line per ally, the classic SRW per-ally support-attack bark table. Of
the seven, Duo alone gets four individual lines against two apiece for the
rest, including two with a register no ally-support line needs: entry 8
needles him ("So I clean, Duo?", teasing over being left the mess) and entry
33 frets about worrying him specifically ("can't have Duo worrying about
me"). That asymmetry, plus entry 31's "training wasn't wasted" (a novice's
relief, not a veteran ace's), points to Hilde Schubaker -- the only named
Gundam Wing woman in this game's library (`source/library/pilots.json` i=87;
already shipped as "Hilde Schubaker" in `translation/library/pt_080.json`)
whose defining relationship is specifically with Duo, and who canonically is
not yet a combat veteran when the Mariemaia arc opens. Sally Po (i=89) was
considered and rejected: her canon warmth is toward Wufei specifically, not
Duo, and she is an established field veteran by this point, which does not
fit entry 31's novice tone. No canonical mobile suit is confirmed for her in
this game -- `robots.json`'s only unassigned Gundam-Wing-era units are the
two Taurus entries (i=60/61, bio says "mainly used by Noin", which allows
but does not confirm a second pilot) and the enemy-only Serpent/Leo (i=63/65)
-- so this ships with unit left unresolved per the brief's fallback, though
every ally name is kept since the identity read is strong even without a
confirmed unit. Recorded under "136" in `analysis/voice_identity.json`. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/136.json`, 0 problems, 74 of 74 answered.

**Voice: section 89 is Schwarzwald piloting Big Duo, 80 lines** -- filed as
Granzeboma / Anti-Spiral by weapon-name match (score 3.0, middling), the same
trap the brief warns about (section 8 scored 7.5 for Strike Freedom and was a
Full Metal Panic mercenary). Content is THE BIG O: every line names Roger
Smith directly or contrasts his mecha 'The Big' with this section's own Big
Duo (58, 59, 84-85, 91), and the section's constant fixation on 真実 "truth"
(5, 37, 45, 72, 76) plus its contempt for 腐った犬 "rotten dogs"/"curs" (0,
24, 42) and 'パラダイムの犬' "Paradigm's dogs" (86) matches
`source/library/pilots.json` i=246 (CHFN シュバルツバルト, CHNN シュバルツ)
almost line for line -- a Memory Digger who "later found Big Duo and
challenged Roger, but lost" and looks down on those who don't seek truth.
`translation/library/pt_240.json`/`rt_160.json` already ship
"Schwarzwald"/"Schwarz"; `translation/voice_169.json` (Roger Smith's own
section) addresses Schwarzwald back, confirming the battle pair. Recorded
under "089" in `analysis/voice_identity.json`. Entry 7
('ドゥームヒト フォルトゲーン…！') does not parse as ordinary Japanese and was
left in Japanese (omitted) rather than guessed. Budget forced meaning loss on
several lines, notably 58 (dropped "The Big" to fit "Roger Smith" in 34
cells), 78 (dropped the "Big Duo" name to fit 21 cells), and 86 (dropped
"Paradigm's" from the dog insult to fit 24 cells). `python
tools/check_voice.py work/voice/answer/089.json`, 0 problems, 79 of 80
answered (1 omitted).

**Voice: section 114 is Trowa Barton, 80 lines** -- brief filed unit UNKNOWN,
no weapon-table match. Content and glossary (Duo, Trowa, Heero, Quatre) are
Gundam Wing, and the section self-identifies twice by radio call-sign: entry
114 "This is Trowa, withdrawing" and entry 136 "This is Trowa, mission
understood". Entries 54 and 55 are Trowa's own iconic lines from the Epyon
arc ("Don't... bully Quatre too much, Heero..." and "Huh? What... is
this... my tears?"), confirming the attribution independent of the
call-signs. 五飛 rendered "Wufei" per the spelling already shipped in
`translation/voice_100.json`/`analysis/glossary.json`. Recorded under "114"
in `analysis/voice_identity.json`. Budget was severe throughout (several
entries budget 3-8 cells): entry 3 ('遅いな', budget 3) shipped as the
non-standard abbreviation "Slo" -- no standard English word for "slow" fits
3 cells. Entries addressing Heero/Quatre/Wufei by name (23-32) mostly lost
their explicit verbs ("leave it to me", "I'll support", "fall back") to bare
name-calls or single words to fit, kept textually distinct per the
no-collapse rule even where the underlying meaning is nearly identical.
`python tools/check_voice.py work/voice/answer/114.json`, 0 problems, 80 of
80 answered.

**Voice: section 120 is Lucrezia Noin (Taurus), 68 lines; section 186 is
Sousuke Sagara and Kaname Chidori, not Genion GAI, 71 lines.** Section 120
filed as unit UNKNOWN with no weapon call-out (only glossary term given was
Zechs). Entries 8/74/75 are the evidence: a hit-taken cry of his name alone
("Zechs...!"), a polite greeting counting the exact time apart ("Zechs,
it's been a year and two days" -- shipped compressed as "367 days" to fit
budget 21), and a reluctant vow to fight him. `source/library/pilots.json`
(i=82) gives this as Noin's defining trait verbatim ("since her academy
days she has deeply loved Zechs, to the point of precisely remembering the
time they were apart"), and her bio names her mecha in this continuity as
the Taurus, recorded as unit though no line self-names it. Budget forced
entry 75 to lose "even if it comes to it," shipping as a flatter "I'll
defeat you!" Section 186 was filed as unit Genion GAI (weapon-match score
1.0) -- wrong, the same failure pattern already documented for section 8.
Genion GAI is an original SRW Z3 mecha with no fixed pilot
(`source/library/robots.json` i=243); this section's own weapon term,
Monomolecular Cutter (entry 83), belongs entirely to Full Metal Panic
mobile weapons (`source/rpw/weapons.json`: M9 Gernsback, ARX-7 Arbalest,
M9D Falke, Rk-92 Savage, Zy-98 Shadow, Plan 1056 Kodiac), which is what
actually explains the false match. Content is call-and-response FMP banter:
one speaker calls the other "Sousuke," the other calls her "Chidori" by
surname -- per this project's own established rule (section 187), only
Sousuke does that, everyone else uses her given name. Entry 87 names
"fumoffu" directly (Sousuke's Bonta-kun gibberish, section 147). Entries
79-94 are a comedic fourth-wall bonus scene (addressing "all the players,"
entry 88) where the pair argue over spirit commands, shipped as this
project's own established names rather than literal translations
(`translation/spirits.json`: 熱血 -> Valor, 閃き -> Alert). No unit self-names
in the section, so unit ships null. Both attributions recorded in
`analysis/voice_identity.json`. `python tools/check_voice.py
work/voice/answer/120.json work/voice/answer/186.json`: 0 problems, 68 of
68 and 71 of 71 answered. Not yet merged into `translation/voice_120.json`
or `translation/voice_186.json`.

**Voice: section 137 is Fa Yuiry piloting Methuss, 83 lines** -- filed as
Nu Gundam / Amuro Ray by weapon-name match (score 1.0, Fin Funnel/Funnel),
the same weapon-name trap the brief warns about. Content is Zeta Gundam
AEUG material, not Char's Counterattack: entry 106 self-identifies
("This is Methuss! Beginning attack!"), and entries 42/43 call the Methuss
her own machine. `source/library/pilots.json` (i=53) confirms Fa Yuiry,
Kamille's childhood friend who volunteered to pilot despite doubting her
own skill -- matching entries 5/8 ("I'm a pilot too!"/"No other way!"),
her protectiveness of Kamille throughout (23, 27, 29, 39), her respect for
Quattro as captain (24, 28), and entry 108's confrontation of Reccoa
("Reccoa! I'll stop you!") -- Fa's canonical opposition to Reccoa's
defection, spoken TO Reccoa, ruling Reccoa out as the speaker.
`source/library/robots.json` (i=36) notes the Methuss was "operated by
Reccoa and Fa"; the Reccoa confrontation rules the other one in. The
Fin Funnel/Funnel call-outs are a game-original ability given to this
Methuss, not evidence of Nu Gundam, and were used verbatim from the
brief's weapon table regardless. `translation/library/pt_040.json` /
`rt_000.json` already ship "Emma Sheen" and "Methuss"; "Methuss" reused,
Fa Yuiry's own name never fit any budget so it never needed reuse. Two
lines (40 "missed" and 134 "won't hit") were kept as distinct English
("Miss!"/"Whiff!") per the no-collapse rule. Recorded under "137" in
`analysis/voice_identity.json`. `python tools/check_voice.py
work/voice/answer/137.json`, 0 problems, 83 of 83 answered.

**Voice: section 165 is Yoko Littner piloting the Yoko M Tank, 85 lines** --
filed as Black Getter / Ryouma Nagare by weapon-name match, flatly wrong,
the same trap the brief calls out (cf. section 8). Every named person is
Gurren Lagann (Anti-Spiral, Kamina, Kittan, Gimmy, Simon, Darry, Dayakka,
Viral, all in this brief's own glossary), and the speaker is unmistakably
a teacher addressing former Dai-Gurren-dan comrades as students -- class,
makeup lesson, test, private tutoring, failing grade, "teacher's pride"
run through entries 0, 5, 10, 52, 53, 72-75, 79, 88, 99. Entry 80 names
Littner Village, Yoko's own home village and surname.
`source/library/pilots.json` (i=311) confirms Yoko Littner left the
Dai-Gurren-dan after the timeskip to teach on Korehana Island, then
rejoined "for the sake of the kids" -- matching entries 2/3/68 and entry
69's farewell to the already-dead Kamina ("Sorry, Kamina...! I might be
joining you soon...!"), which rules Kamina himself out as speaker. Entries
39/40 name the M Tank directly; `source/library/robots.json` (i=203)
confirms "Yoko M Tank" as her own gunmen. `translation/library/pt_280.json`
/ `rt_200.json` already ship Yoko, Kittan Bachika, Dayakka Littner, Darry,
Gimmy, Simon, Viral, and Anti-Spiral, all reused verbatim. Entries 13 and
97 both mean roughly "no escape" but were kept distinct ("Can't hide!" /
"No escape!") per the no-collapse rule. Recorded under "165" in
`analysis/voice_identity.json`. `python tools/check_voice.py
work/voice/answer/165.json`, 0 problems, 85 of 85 answered.

**Voice: section 163 is Full Metal Panic! content, not this game's own
cast -- a twin child soldier (Yu Fan/Yu Lan Xia, Second Raid), 82 lines** --
filed as unit UNKNOWN, no weapon call-out matched. Content is anchored by
this section's own glossary (Mithril, Sousuke Sagara -- entry 24, budget
forced 'found you, Sousuke Sagara' down to just 'Found you') and by a
mentor addressed as Sensei throughout (12, 83, 87, 93, 98, 126, 129),
including entry 119 naming Sousuke as 'Sensei's man' -- Gauron's canonical
fixation on Sousuke. The speaker repeatedly addresses an 'onee-chan' (84,
88, 97, 112, 128, 130) through a death-scene run at the end (127-130):
matches Second Raid's twin child soldiers Yu Fan and Yu Lan Xia, trained by
Gauron and sent after Kaname/Sousuke. Kept the register cold and flat
throughout rather than hot-blooded, per a trained child soldier. Could not
determine which twin is speaking, nor find any unit/mecha name in the
lines -- recorded as unidentified in `analysis/voice_identity.json` under
"163" rather than guessed. `python tools/check_voice.py
work/voice/answer/163.json`: 0 problems, 82 of 82 answered. Not yet merged
into `translation/voice_163.json`.

**Voice: section 78 is Zaied Wasfar (Full Metal Panic!), not VF-22S
Sturmvogel II B / Gamlin Kizaki, 83 lines** -- filed as a weapon-name match,
score 2.0, the same middling-score trap documented for section 8. Entry
123's self-naming support call-out ('ZaiedO da, engo suru', this project's
standard self-identifying convention -- compare MIXY in section 10) ships
as 'Zaied here!' and settles the pilot; this section's own glossary already
glosses Zaied verbatim. The speaker repeatedly addresses a rival named
Kashim (22, 23, 84, 104, 115) -- Full Metal Panic canon: Kashim is what
Zaied called Sousuke Sagara as fellow child soldiers in Afghanistan, before
Zaied mercenaried for Gauron/Amalgam against Sousuke and Mithril at
Helmajistan. Kept 'Kashim' verbatim (the name this speaker actually uses,
not 'Sousuke'). A winning-side/losing-side motif running through the
section was kept consistent across entries: 9 'Winning side!', 101 'No
losing side!', 114 'Not winning side' (his eventual defeat). No VF-22S or
Macross content anywhere in the 83 lines; other enemy-unit reactions (26,
27, 28) are generic and were translated generically rather than matched to
this project's own units. Register kept as a calm, cynical veteran
mercenary. `python tools/check_voice.py work/voice/answer/078.json`: 0
problems, 83 of 83 answered. Not yet merged into `translation/voice_078.json`.

**Voice: section 34 is Annalotta Stohls piloting Diosc A, 48 lines** --
filed as Granzeboma / Anti-Spiral by weapon-name match (score 2.0), the same
kind of middling-score trap the brief warns about for section 8. Content is
original-to-this-game Geminis material: entry 0 self-names in full
("Annalotta Stohls, beginning attack!"), and entries 26/31 repeat the pattern
for counter/support barks. `source/library/pilots.json` (i=395) and
`robots.json` (i=245, Diosc A's pilot field) confirm her as Geminis's
vice-commander, and `translation/library/rt_240.json` /
`translation/voice_082.json` /`voice_083.json` /`voice_133.json` already ship
her name, Diosc A, Command Arts, and Psy-Control -- reused verbatim here.
Budget forced entries 26/31 to drop her name entirely ("Countering!"/
"Covering!" -- 13 cells can't hold "Annalotta" plus a verb), unlike entry 0's
larger two-line budget. Entry 19 (a distinct Japanese term from entry 14's
Command Arts) shipped as "Behold my art!" to keep it different from entry
14. No twin found; Diosc A carries one pilot per `robots.json`. Recorded
under "34" in `analysis/voice_identity.json`. `python tools/check_voice.py
work/voice/answer/034.json`, 0 problems, 48 of 48 answered.

**Voice: section 99 is Zeus (true form Z Mazinger), 49 lines** -- filed as
UNKNOWN, no weapon call-out matched. Self-identifying: entry 58 states "My
name is Zeus -- but in truth, I am Z Mazinger!", and entry 59 is the
Mazinger "ROCKET... PUNCH!" callout stretched across the line break.
`source/library/robots.json` (i=161, PLTN "---") confirms Zeus God as a
self-piloted entity, one of the Three Great Gods of Mycenae from Shin
Mazinger, golden-armored with a "Z"-marked blade (matching entry 42's "my
golden body"). The named opponent, Hades (i=162), and both names' spellings
match `translation/library/pt_200.json`'s existing glossary. Register kept
archaic/godly throughout (short, lofty imperatives -- "Judgment!",
"Unforgiven!", "Fool!"); entries 22-23 address unnamed allies offering to
fight beside them. No twin found; Zeus/Z Mazinger has no co-pilot per
`robots.json`. Recorded under "99" in `analysis/voice_identity.json`.
`python tools/check_voice.py work/voice/answer/099.json`, 0 problems, 49 of
49 answered.

**Voice: section 42 is Angel piloting Big Venus (The Big O), 64 lines** --
unit UNKNOWN in `sections.json` (no weapon call-out at all); identified from
content against `source/library/pilots.json`'s Angel entry. This is the Big O
finale: entry 8 ("I reset the world") and entry 76 ("Big Venus cannot be
stopped") name her plan and unit, entries 14/77/97/98/109 address "Roger" and
78/109 use this section's own glossary's full "Roger Smith", and entry 104
("Fine... after all, I am Memory") is the reveal that Angel is herself
Memory, the entity behind the megadei -- matching pilots.json's DSC2 for her
beat for beat (having learned the truth, she uses Big Venus to erase
everything and reset the world 40 years back, until Roger's negotiation
about the meaning of Memory brings her to accept the present). Shipped under
"Angel" (`translation/library/{pt_240,rt_160}.json`'s already-established
エンジェル -> Angel) rather than "Memory", since that is the name she goes by
throughout and the name pilots.json/robots.json file her under. Established
"she" (pilots.json uses 彼女 for her). Entries 110-113 are a separate
pause-menu comic aside (thanking the players, then a flirtatious exchange
watched by a "grumpy android" -- R. Dorothy Wayneright) rather than in-battle
barks. Recorded under "42" in `analysis/voice_identity.json`. Budgets ran
4-43 letters; three pause-menu lines (110-112) needed heavy compression to
fit ("Glad, but a grumpy android's watching us." for a much longer Japanese
aside). Not confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/042.json`, 0 problems, 64 of 64 answered.

**Voice: section 209 is Shikuu piloting Shiseiten, 60 of 64 lines** -- filed
via this section's own glossary weapon match on 尸獄門 (Shigokumon, entries
26/31); confirmed by `source/rpw/weapons.json` tying that attack (and 骸怨)
to unit 尸逝天, and `source/library/pilots.json` i=396 filing 尸空 as its
pilot -- "the Reactor of the Sphere 'Silent Giant Crab', who pilots the
massive mobile weapon 尸逝天... a man of few words who never shows emotion,
even in battle," an exact match for this section's flat, unexclamated
register ("It's pointless", "Weak", "Accept the result"). Both names are
already shipped: `translation/library/rt_240.json`'s 尸逝天 -> "Shiseiten"
and `translation/library/pt_360.json`'s 尸空 -> "Shikuu", both established
"he". Entries 18-24 are him reacting to crossover elemental/franchise powers
(beast blood, water, wind, fire, a god of light, Getter Rays) in named
opponents, and entry 12 addresses "the new feuding twin Reactors." Four
entries (25, 32, 33, 34) are fragments of an unnamed finishing-move
incantation with 1-8 letter budgets and no glossary entry or established
reading anywhere in the project -- left in Japanese (keys omitted) rather
than guessed; entries 26 and 31 keep their verb ("Steal!", "Open!") but drop
the same untranslatable name for the same reason, and 31 additionally could
not fit the glossary's own "Shigokumon" (10 letters) inside its 6-letter
budget, so the bark carries only the verb. Recorded under "209" in
`analysis/voice_identity.json`. Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/209.json`, 0 problems, 60 of 64
answered (4 omitted as above).

**Voice: section 112 is Teletha Testarossa (Tessa) piloting an AS in a
training skit, 67 lines** -- unit UNKNOWN, no weapon call-out matched
(score 0). Entry 9 self-names: 「テレサ・テスタロッサ、行きます！」
(Teletha Testarossa, going!). This is a different voice from section
111's Testarossa (`analysis/voice_identity.json`): 111 is her
ship-captain register giving helm orders aboard Tuatha de Danaan; 112 is
a mobile-suit pilot's own attack/hit/defeat barks, and entry 119
("so this is... the AS battlefield") confirms an Arm Slave cockpit, not
the submarine. Content is a lighthearted non-canon training bout: she is
coached by "Coach... no, Sagara" (entries 15/80/85 all correct
themselves from "Coach" to "Sagara", i.e. Sousuke Sagara), duels Melissa
Mao by name (22-23, 87, 90, 104, 110-111, 120), and the loser of the bet
runs a naked lap of the base (21, 26, 112, 125) -- Kurz Weber is named
as another possible opponent (24). Shipped as Tessa; unit ships null,
no AS model is named in the lines. Budgets were severe (several
single-digit); "Teletha Testarossa" (18 letters) does not fit entry 9's
16-letter budget, so it ships as the project's own established short
form "Tessa" instead (`translation/library/pt_240.json`), not an
invented abbreviation. Recorded under "112" in
`analysis/voice_identity.json`. Not confirmed by a screenshot.
`python tools/check_voice.py work/voice/answer/112.json`, 0 problems.

**Voice: section 194 is an unnamed grunt fighting Gundam, 65 lines** --
filed as Gundam Mk-II (weapon call-out match, score 1.0); DO NOT TRUST,
and wrong: the speaker addresses "Gundam" as a third-person opponent
throughout (entry 34 "Gundam! Your time is up!", 39 "Gundam, never
learns!", 45 "cant beat Gundam?!", 68 "here I come, Gundam", etc.), which
a unit cannot say of itself. Same failure family already documented for
sections 11/12 (`analysis/voice_identity.json`): an unnamed military
pilot fighting a Gundam-type unit, not piloting one. Entry 15 ("we will
protect Earth with our own hands") and entry 38 (addressing multiple
enemies, "still resisting?") read as a Titans-style Earth-defense grunt
speaking for a squad, matching 11/12's conclusion, though 194 does not
share verbatim lines with 11/12 -- a separate section in the same
generic-grunt family, not a repeat. Checked the note that 194 shares a
few lines with section 201 (also filed Gundam Mk-II, score 1.0):
confirmed by comparing `source/voice/194.json` against `201.json` --
only 7 of 194's 89 index entries match 201's pool, not the whole set, so
this is not a repeat-cluster pair (`work/voice/clusters.json` lists both
as singletons) and 201 was left untranslated, out of this task's scope.
No line self-names the speaker or unit; shipped as unnamed enemy battle
barks, "Gundam" kept as the addressed opponent, no name inserted for the
speaker. Recorded under "194" in `analysis/voice_identity.json`. Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/194.json`, 0 problems.

**Voice: section 39 is Eida Rossa piloting R-Daigan (Dancouga Nova), 64
lines** -- filed as Gundam-adjacent Beck Victory Deluxe / pilot Beck
(weapon-name match, score 2.0) and it was another false attribution like
the section-8 case the brief warns about: Beck (ジェイソン・ベック,
`source/library/pilots.json` i=247) is a Big O criminal with nothing to
do with these lines. Content is unmistakably Eida Rossa (エイーダ・ロッ
サ) from 獣装機攻ダンクーガノヴァ (Dancouga Nova) -- her `robots.json`
card (i=300) states outright "her true identity is the pilot of the
R-Daigan." First-person polite register throughout, piloting "R-Daigan"
by name (entries 4/5/22/24/34/36/39/48/49/57/61/70/73), addressing
teammate "Aoi" (葵さん, entries 58/72 -- Aoi Hidaka, Dancouga Nova's main
pilot) with deference, and repeatedly naming and worrying over "Johnny"
(ジョニーさん, entries 59/62/73 -- Johnny Barnett, the Team D pilot Eida
falls for per both their bios). Entry 71 ("Dancouga Nova is hope for the
future") and 57 ("add R-Daigan's power to Dancouga Nova") track her arc
from enemy pilot to teammate fused into the final MAX GOD combination.
English spellings ("Eida", "Aoi", "R-Daigan", "Johnny", "Dancouga Nova")
all match what `analysis/glossary.json` and
`translation/library/{pt_280,rt_160}.json` already ship. Recorded under
"39" in `analysis/voice_identity.json`. Budgets ran 6-26 letters;
entries 24 and 70 both compressed to "R-Daigan!" at first and had to be
split apart per the no-collision rule ("Next up!" / "R-Daigan!"), and
several weapon call-outs (15/16/17/18) dropped the shipped "Dan" prefix
from `translation/weapons.json`'s "Dan Blade Shoot" family to fit ("cut!
Blade Twin!" instead of "Dan Blade Twin!"). Not confirmed by a
screenshot. `python tools/check_voice.py work/voice/answer/039.json`, 0
problems.

**Voice: section 122 is Hades, Mycenae's Three Great Gods, 61 lines** --
unit UNKNOWN in `sections.json` (no weapon call-out at all). Entry 0
invokes "Mycenae's Three Great Gods, know the power of Hades" and entry
1 opens with the speaker self-naming outright ("My name is Hades!");
entries 40/47/72/74/76 refer to the speaker in third person as "this
Hades," confirming he is Hades himself, not a subordinate. He addresses
Zeus directly as a rival power ("does Zeus's power surpass even this
Hades," entry 76) and is challenged by a look-alike (entry 8, "the
spitting image of Zeus") -- Great Mazinger's Mikene (Mycenae) Empire's
Three Great Gods are Hades, Zeus and Poseidon, so this reads as Hades
confronting a Zeus impostor/rival. This is a *different* character from
the "Mycenae god-general" already filed at sections 75 (Kedora)/155/156/
157, who speak of "Lord Hades" in reverent third person and call Zeus a
traitor from the outside; here the two read as rival co-equal gods.
"Hades" and "Zeus" spellings match what `translation/voice_155.json`,
`voice_184.json`, `voice_197.json` and `voice_207.json` already ship.
No unit/robot card matched; ships pilot-only, recorded under "122" in
`analysis/voice_identity.json`. Budgets were severe (9-31 letters);
entry 0 lost "know the power of" entirely to fit ("Mycenae's gods,
Hades!"), and several taunts lost secondary clauses (e.g. entry 47 "to
outwit this Hades" became "Outwit me?" since "Hades" plus "Insolence!"
did not both fit). Not confirmed by a screenshot. `python
tools/check_voice.py work/voice/answer/122.json`, 0 problems.

**Voice: section 058 is Garadabura, Mycenae's self-piloting Machine God,
60 lines** -- unit UNKNOWN in `sections.json` (no weapon call-out, score
0). Entry 0 self-names outright: 「我が名は、機械神ガラダブラ！」 (My
name is, Machine God Garadabura!), and the speaker calls itself "this
Garadabura" again at entries 37, 45, 71 and 80. `source/library/pilots.json`
i=218 confirms Garadabura is Mycenae's Machine God, called "Hero" (勇者)
for its valor, later split into the Kikaijuu Garada K7 and Doublas M2,
and -- unlike ordinary Kikaijuu -- explicitly "has its own will and can
speak" (自らの意思を持ち、しゃべる事も出来る); the matching
`robots.json` entry is 勇者ガラダブラ (Hero Garadoublas). Pilot and unit
are the same entity, so both are shipped as "Garadabura", the brief's own
glossed short form (used verbatim over the library's longer "Hero
Garadoublas" romanization). Content confirms the Shin Mazinger Z Impact
/ Great Mazinger Mycenae setting: the section repeatedly confronts an
opponent wearing ゼウス's (Zeus, glossed) face, accusing them of being a
lookalike or impostor, and invokes ミケーネ (Mycenae) protection and
pride -- consistent with section 75's Kedora, another Mycenae general
from the same source already in `analysis/voice_identity.json`. No
third-person pronoun was needed for Garadabura in any of the 60 lines
(all first-person), so rule 7 did not come into play. Recorded under
"58". Budgets ran 7-29 letters; entry 0 itself lost "Machine God" to
fit ("I'm Garadabura", 14-letter budget, no room for the title). Not
confirmed by a screenshot. `python tools/check_voice.py
work/voice/answer/058.json`, 0 problems.

**Voice: section 038 is Viral / Enkidudu (Gurren Lagann), 58 lines** --
filed as Gundam Mk-II (weapon-match on 連続攻撃/Combo Attack, score 2.0)
and the brief's own warning not to trust that was correct: no Gundam or
AEUG content anywhere. WebSearch confirmed エンキドゥドゥ is Viral's
Gunmen from Tengen Toppa Gurren Lagann (an upgraded four-armed sword
form of his earlier Enkidu), and Viral is the Beast Men Army's Far East
commander. Content matches: the speaker addresses its own machine by
name repeatedly ("Enkidudu can still fight", "hold on, Enkidudu"),
self-describes as "a wounded beast-man" (entry 38, 手負いの獣人), and
taunts an opposing pilot and mecha named by this section's own glossary
terms シモン/Simon and グレンラガン/Gurren Lagann -- Viral's canonical
rival and Simon's own machine. Register is rough masculine taunting,
matching Viral's brash personality; ヴィラル/Viral is already a
`proposed`-status term in `analysis/glossary.json`. No zukan/library
card exists for Enkidudu itself, so it ships pilot-named with the unit
spelled per the brief's own Japanese and the WebSearch-confirmed
romanization. Recorded under "38". Budgets were severe (7-29 letters);
the unit's own name ("Enkidudu", 8 letters) ate most of any line that
addressed it directly, e.g. entry 16 dropped "this is the crucial
moment" to fit "Now, Enkidudu!" (16-letter budget). Not confirmed by a
screenshot, but the self-naming vocatives, the beast-man
self-description and the named rivals leave no real ambiguity.
`python tools/check_voice.py work/voice/answer/038.json`, 0 problems.

**Voice: section 088 is Shako (full name Ru Shako), a VOTOMS pilot, 54
lines** -- unit UNKNOWN in `sections.json` (no weapon call-out, score 0);
worked out from the lines themselves. The speaker addresses a "キリコ"
(Chirico) by name as someone to protect, not as himself: entry 45
「キリコ、後は任せろ」 (Chirico, leave the rest to me), entry 46
「俺の背中に隠れろ」 (hide behind my back) followed immediately by entry
47 「弾除けぐらいにはなる」 (I can at least serve as a bullet shield),
and entry 48 「後退しろ、キリコ」 (fall back, Chirico). Entry 83
「ル・シャッコ、了解」 (Ru Shako, roger) is a self-identifying radio
callsign acknowledgement -- the pilot naming himself on comms.
`analysis/glossary.json` and `source/library/pilots.json` both carry
シャッコ/Shako and ル・シャッコ/Ru Shako as the short and full forms of
the same VOTOMS pilot (zukan_id 34, both tagged `kind: pilot`), distinct
from キリコ・キュービー/Chirico Cuvie (zukan_id 32). The section also
uses クエント (Quent), the VOTOMS planet already spelled "Quent" in
`translation/library/rt_000.json`/`stage0002_03.json` and tied to
Chirico's own endgame in his `pilots.json` bio -- consistent with a
VOTOMS-internal cast, not a crossover coincidence. No mecha could be
attributed (no robots.json entry named Shako/Ru Shako); ships pilot-only.
Recorded in `analysis/voice_identity.json` under "88". Budgets were
brutal (3-9 letters typical, half the section is single words):
entry 11's line break ("As Quent,\nyou won't win", 23-cell budget) is
the only two-line entry; everything else is one line. Not confirmed by
a screenshot. `python tools/check_voice.py work/voice/answer/088.json`,
0 problems.

**Voice: section 052 is Gadlight Meonsam / Geminia, 52 lines** --
confirmed as filed (weapon-name match on "Light Particle Blast", score
2.0 -- middling, so checked against content rather than trusted). The
match holds up: `source/library/robots.json` i=244 (Geminia) lists PLTN
ガドライト・メオンサム (Gadlight Meonsam) directly and describes him as
planet Geminai's strongest pilot and captain of the elite Geminis squad,
and the lines match point for point -- entry 3 self-declares "Geminis'
captain to the end" (「俺は最後の瞬間までジェミニスの隊長だ」), entry 5
invokes the Geminaids (Geminai's people) by name, entries 56/57 vow
vengeance for what the Geminaids have suffered, and entry 20 calls out
to the Sphere (the reactor core every Geminis-affiliated mech carries).
Nothing in the 52 lines contradicts the attribution. Reused this
project's established spellings verbatim: "Geminis" (the squad, already
shipped in voice_082/083/133), "Geminia" (this unit) and "Geminai" (the
home planet, voice_082/083); "Geminaid(s)" as the demonym has no prior
shipped precedent but follows the same pattern and was used at entries
5/56/57 where budget allowed. Budgets were severe throughout (most
9-15 letters, several single digits): entry 0 dropped "damn" to fit
"Who are they?!", entry 14 dropped the "Geminai" reference to fit "I'll
cut you!", and the weapon call-out at entry 11 (「光粒子ブラスト！」,
an 8-letter budget) could not fit the shipped "Light Particle Blast"
name at all -- shipped as "Blast!" and flagged; entry 12 uses the
shipped short form "Formenia" (from 光破剣フォルメニア -> "Formenia
Light Blade") instead, since its own budget also could not take the
full weapon name. `python tools/check_voice.py work/voice/answer/052.json`,
0 problems.

**Voice: section 036 is an unidentified cosmic-entity voice, 44 lines** --
no weapon call-out matched (score 0) and no glossary terms matched either
(the brief carried no weapon or glossary table at all -- unusually thin).
Content is a collective first-person-plural ("we"/"our") apocalyptic sermon
("we are chaos... we are order...", "we are part of infinity", "kneel to
the supreme power", "cast off flesh, join us", "be swallowed by causality
and reincarnation"), with no self-naming line and nobody addressed by
name. Checked against every other section sharing similar cosmic-villain
vocabulary -- section 030 (Anti-Spiral/Granzeboma), section 053 (Gadlight
Meonsam/Geminia), section 086 (Simon, one stray line) -- all three reuse
overlapping stock phrases but share zero literal strings with section 036
and none speak in this section's plural "we" register, so none of them is
evidence for this section's identity. Recorded as unresolved in
`analysis/voice_identity.json` under "36"; shipped with no character name
inserted, keeping the "we/us/our" voice wherever budget allowed it.
Budgets throughout this section were severe (single-digit letters was the
norm, several as low as 4): the pronoun was the first casualty (entry 0
「破壊する…全てを…」, "Ruin all"; entry 3 「滅べ、生ある者よ…」,
"Die, all"), and entry 15 「大いなる意志…大いなる力…」 (great will...
great power...) compressed to "Will is might", dropping "great" from
both halves. `python tools/check_voice.py work/voice/answer/036.json`,
0 problems.

**Voice: section 147 is Bonta-kun / Sousuke Sagara, 40 lines** -- no
weapon call-out matched (unit UNKNOWN per the brief). All 40 distinct
lines are pure ふ/も nonsense syllables (「ふもっ！」「もっふる！」
「ふもももも」...), no real Japanese words anywhere. This is Bonta-kun,
the Full Metal Panic Fumoffu amusement-park mascot suit Sousuke
modified into a light AS: `source/library/robots.json` i=187 (RBTN/RBN2
ボン太くん, PLTN 相良宗介) spells out that its voice changer cannot be
switched off, so "no matter what it says, the output to the outside
always comes out sounding like some variation of fumoffu" -- only
Kaname can interpret it. `work/voice/mech_pilot.json` independently
maps ボン太くん -> 相良宗介 (Sousuke Sagara), confirming the pilot.
Since the in-game text IS the gibberish itself, not Kaname's
translation of it, the 40 lines shipped as phonetic English nonsense
barks ("Fum!", "Fuff!", "Moff!", "Fumomoo!"...) rather than sentences,
preserving mora count, the っ/ー doubling and elongation, comma/space-
separated multi-part barks, and the one line-break line (entry 55,
"Mom! Fum!\nMoff! Moff!?") exactly to budget -- every budget in this
section is sized letter-for-letter to the Japanese kana count, not to
a meaningful sentence. Entries 0/47/57 share byte-identical Japanese
(「ふもっ！」) and ship identical English ("Fum!"); entries 5/52
(「もふっ！」/「もふ…！」) share the same normalized bark and also
ship identical English ("Mof!") -- both intentional, matching
`check_voice.py`'s own definition of "the same shout, differently
held." Recorded in `analysis/voice_identity.json` under "147". Not
confirmed by a screenshot, but the robots.json bio's exact "fumoffu"
wording leaves no real doubt about identity. `python
tools/check_voice.py work/voice/answer/147.json`, 0 problems.

**Voice: section 187 is ARX-7 Arbalest / Sousuke Sagara, 44 lines** --
no weapon call-out matched (score 0). Content reads as Sousuke Sagara
from Full Metal Panic: entry 47 「千鳥、俺は…！」 addresses Chidori
by surname mid-sentence (only Sousuke calls her that), and entry 98
「ザイードォォォォ！！」 is a scream of Zaied's name, drawn out --
`source/library/pilots.json` #262 identifies Zaied as the terrorist
who fought alongside Gauron and was Sousuke's childhood friend turned
enemy, so shouting his name mid-battle fits. The remaining 42 lines are
a soldier repeatedly defining himself by duty and combat ("俺は…兵士だ！"
I am... a soldier!, "俺には…戦いしかない…" fighting is all I have)
interleaved with a three-line self-doubt family (entries 27, 43, 48,
all near-identical "what am I doing?!") kept distinct in English --
"What am I?!", "Just what am I", "What am I doing". No line
self-names Sousuke or Arbalest, so the identification is inferred from
content, not confirmed; recorded in `analysis/voice_identity.json`
under "187". Budgets were severe throughout (several 4-letter caps):
entry 35 「殺す価値もない相手だ…！」 (not even worth killing) lost
the killing-specific meaning to fit as "Not worth it", and entry 36
「その程度か、下手くそが…！」 (is that all, you're lousy) compressed
to "Is that all?!", dropping the direct insult. `python
tools/check_voice.py work/voice/answer/187.json`, 0 problems.

**Voice: section 130 is Unicorn Gundam / Banagher Links, section 181
reuses section 180's unidentified-unit phrasing, 18 lines total** --
section 130 (10 index entries, 9 distinct lines, too small to carry a
weapon call-out) is Banagher: entry 8 calls out to Audrey by name
mid-anguish, and `analysis/glossary.json` confirms Audrey (オードリー)
is Mobile Suit Gundam Unicorn's Mineva Lao Zabi alias, Banagher's love
interest, whose English name is already shipped in
`translation/library/pt_120.json`. `work/voice/mech_pilot.json`
independently maps Unicorn Gundam to Banagher Links (not Riddhe
Marcenas, who maps to Delta Plus there), and the section sits right
after the already-shipped 354-line Unicorn Gundam/Banagher set
(section 128) in the raw voice index. Recorded under "130" in
`analysis/voice_identity.json`; not screenshot-confirmed, flagged as a
content reading.

Section 181's entries 0-3 and 12 are verbatim, same-budget repeats of
section 180's entries 0/2/3/4/13 (グオオオオッ/ガアアアアッ/ガアッ/
グワッ/ウウッ…！); per the section 180 brief this is the same pilot,
so 181 reuses 180's exact English (Groooh!/Graaah!/Gah!/Gwa!/Uugh!)
rather than retranslating independently. 181's remaining entries (13,
14, 15, 17) have no counterpart in 180: they shift from 180's ga/gu/ku
growl palette to きゃあ (kyaa) screams and a trailing あ…ああ… moan --
still no self-naming, no addressed name, no pronoun, so shipped as
unidentified generic barks like 180, with a note that the growl-plus-
scream combination reads like a possible monster/beast-type or
possession-type unit (a guess, not confirmed). Recorded under "181" in
`analysis/voice_identity.json`. Both files check clean: `python
tools/check_voice.py work/voice/answer/130.json 181.json`, 0 problems.

**Voice: section 075 is Kedora (Great Mazinger's Mycenae general), 9
lines** -- self-naming: entry 1 「我はケドラ…ミケーネの兵士なり」 (I am
Kedora... a soldier of Mycenae) and entry 3 「我はケドラ…最強の兵士」
(I am Kedora... the strongest soldier) both open by name. "Kedora" is
the spelling this project already shipped (`source/library/pilots.json`,
`translation/library/pt_160.json`/`pt_200.json`, and
`work/voice/answer/184.json` entry 254). No robot/pilot card of his own
exists in `source/library/{pilots,robots}.json` -- he appears only in
other characters' bios (Kouji Kabuto, the Kurogane-ya proprietress, the
Mycenae gods) as the general who took over Kenzo Kabuto's body -- so the
unit he pilots here could not be confirmed; recorded pilot-only in
`analysis/voice_identity.json` under "75". Budgets were severe (a
15-letter cap was the largest of the nine): every line compresses hard,
e.g. entry 4 「ミケーネの力にひれ伏せ…」 (kneel before the power of
Mycenae) -> "Kneel to us!" and entry 7's triple "滅ぼす…滅ぼす…滅ぼす…"
(destroy... destroy... destroy...) -> "Destroy it all!", losing the
repetition for a single emphatic line. `python tools/check_voice.py
work/voice/answer/075.json`, 0 problems.

**Voice: section 200, unidentified unit, 8 lines** -- no weapon
call-out matched and no library entry surfaced a match. Entries 1-4 are
a self-contained comic riddle about a donut's "true possibility" that
closes by addressing "you players" directly and saying goodbye ("Fu...
seems the players agree too. Well then, see you again!") -- the same
pause-menu fourth-wall pattern already documented elsewhere in this
project (`analysis/voice_identity.json` "049", "182"), so this reads as
a joke/Easter-egg aside rather than an ordinary battle bark, but no
name, pronoun, or weapon ties it to a specific character; shipped
unidentified (`pilot`/`unit` both null) in `analysis/voice_identity.json`
under "200". Entries 0/5/6 are a "destroy the false name and shout the
true name -- then the myth accepts you" incantation, with entry 0
being the two-part combination of 5 and 6 verbatim, translated
identically across all three per the near-identical-Japanese rule.
Budgets forced heavy compression throughout, most severely entry 7
(9-letter cap) 「以後、恋愛禁止！！」 (from now on, romance is
forbidden!!) -> "No love!!". `python tools/check_voice.py
work/voice/answer/200.json`, 0 problems.

**Voice: sections 40 and 180, unidentified units, 26 lines** -- both
sections are pure wordless battle-roar sets (no dialogue, no self-naming,
no weapon call-out, no addressed name, no pronoun anywhere in either
13-line set), so neither speaker could be identified from content; shipped
as unidentified generic battle barks and recorded as such (`pilot`/`unit`
both null) in `analysis/voice_identity.json` under "40" and "180". Section
40 uses a u/o vocalization palette (グウウ/ウオオオ/オオオ...), climbing
from a 3-letter grunt to a 16-letter double-exclaim roar, read as a
graduated hits-taken ladder ending in a defeat cry at entry 12. Section
180 uses a different ga/gu/ku/gwa growl palette (ガアッ/グオオオオッ/
グワッ...), scaling from a 4-letter sharp bark to an 11-letter drawn-out
roar; per the section 180 brief this same pilot also speaks in section
181, which should reuse this same English phrasing when it is translated.
Both files check clean: `python tools/check_voice.py work/voice/answer/
040.json` and `180.json`, 0 problems.

**Voice: section 182 is Kei Katsuragi (Super Dimension Century Orguss),
with co-pilot Mome** -- Codex draft, Sonnet-reviewed, 208 distinct lines.
Filed by weapon call-out match to Orguss and confirmed from content: he
is addressed throughout as 桂様/桂木桂様 (e.g. 1, 3, 5, 75, 103, 179,
218), entry 233's 「オーガスの体当たりだ！」 matches the shipped
weapons.json term 体当たり -> Ram Attack, and entry 260's ジェミニス
(Geminis) is the faction already shipped in sections 82/83/133. The
library bio (`source/library/pilots.json` i=49) matches beat for beat:
a hot-blooded, incorrigible-womanizer hero who flirts mid-battle (8, 12,
48, 91, 113, 154, 171), keeps ribbing a male opponent about being
pursued by a man while going easy on female ones (110-112, 129,
143-148, 156-157, 257), and whose late-section arc (186-195) pulls in
the bio's other two named singularities -- Olson (オルソン, library
i=50, Olson D. Verne) and Mimsy (ミムジィ, the mother of his child per
the library DSCR, matching entry 187's "my child waits for me"). Mome
(モーム, library i=51) co-pilots, self-referring in third person as his
support (101, 103, 136, 141, 202-205). Recorded in
`analysis/voice_identity.json` under "182".

Found and fixed 16 deficient lines, run through `tools/check_voice.py`
to 0 problems:

- **Threat/command direction flipped**: entry 9, jp "俺に手を出さない
  方が身のためだぜ！" (you'd be better off not laying a hand on me!, a
  boast that touching him is bad for THEM) `"Hands off me!"` ->
  `"You'll regret it!"` (read instead as a defensive plea); entry 64, jp
  "俺のハニーをやらせるか！" (like hell I'll let you have my honey!, a
  protective refusal) `"Not my honey"` -> `"Back off her"` (read instead
  as a flat, ambiguous correction); entry 139, jp "こんな所で退場なんて、
  御免被る！" (I refuse to be knocked out of the fight here!, defiant)
  `"No exit for me!"` -> `"Won't fall here!"` ("no exit" reads as
  trapped/doomed, the opposite of defiant); entry 284, jp "桂様からは
  逃げられないんだから！" (there's no escaping Kei!, describing the
  enemy's inability to flee) `"Kei won't let go"` -> `"No escaping Kei!"`
  (read instead as Kei actively grappling something).
- **Line's entire content dropped for just the speaker's own name**:
  entry 178, jp "桂木桂様の腕、とくと御覧あれ！" (behold well the skill
  of Kei Katsuragi!) shipped as bare `"Kei Katsuragi!"`, discarding the
  actual boast; fixed to `"Watch my skill!"`.
- **Idiom mistranslation**: entry 18, jp "くらえっ！" (a stock "take
  this!" attack shout) shipped as the meaningless grunt `"Hah!"`; fixed
  to `"Take!"`. Entry 97, jp "空戦で負けるわけにはいかないのよね！"
  (I mustn't lose in the air!, resolve) shipped as the boastful
  `"I own the skies!"`, inverting humility into arrogance; fixed to
  `"Can't lose up here"`.
- **Register/nuance flattened under budget pressure**: entry 28, jp
  "遅いぜ！　もう一発！" (too slow! one more!) `"Slow! More"` -> `"Slow!
  One!"` (restored the missing punch and end punctuation); entry 31, jp
  "ほらほら、今日はサービスするよ！" (look, look, I'll give you a treat
  today!) `"Look, look! Free"` (trails off, unclear) -> `"Free show
  today!"`; entry 40, jp "これで最後だ！" (this is the final blow!)
  `"The end"` (reads like narration, not an attack call) -> `"Finish!"`;
  entry 89, jp "俺を取り合うのは、女の子だけでいいの！" (it's fine if
  it's only girls fighting over me!) `"Girls fight over me"` (drops the
  "only", overclaiming) -> `"Only girls, please!"`; entry 92, jp
  "襲われるのは戦場以外でお願いしたいね" (I'd like to be "attacked"
  somewhere other than the battlefield -- a flirty wish) `"Attack
  off-field!"` (reads as a nonsensical tactical order) -> `"Ambush me,
  not war"`; entry 143, jp "本気で頭にきたぜ！　相手が男なら容赦無しだ！"
  (now I'm serious mad! if the opponent's a man, no mercy!)
  `"Mad now!\nNo mercy, man!"` ("man!" reads as a generic "dude"
  interjection, losing the "because you're male" conditional that ties
  to the section's running men-vs-women theme) -> `"Mad!\nMen get no
  mercy!"`; entry 167, jp "縁があったら、また逢いたいね" (if we're fated
  to, I'd like to meet again -- a wistful farewell) `"Fated to meet"`
  (reads as anticipating a first meeting, not a reunion) -> `"See you
  again?"`.

Quality: cleaner than the 090/101-era Codex drafts (B-/C+) but more
correction-heavy than 079/91 (B+/A-) -- most compressions held up (the
Orguss Ram Attack call-out, the recurring kiss-not-attack and
no-mercy-for-men bits, the elongated retreat stutter "Re-trea-at!" at
149), but several tight-budget lines flipped the direction of a threat
or command, one dropped a line's entire content for the speaker's own
name, and a handful flattened idiom or register under space pressure.
Landing around B.

**Voice: section 145 is Beck (The Big O), with henchmen Dove and T-Bone**
-- Codex draft, Sonnet-reviewed, ships as `translation/voice_145.json`
(212 of 212 lines). Confirmed against The Big O: the vain "genius
Beck-sama" self-address (3, 15, 108, 131, 277), the "smart/smooth"
obsession (21, 27, 96, 117, 137), the hatred of Roger Smith -- named
directly (38, 165) and mocked as "crow bastard" (カラス野郎, matching
`source/library/pilots.json`'s own note that Beck calls Roger this after
being jailed by him) and "negotiator" (24, 31, 50, 166). Entries 63-118
and 254-290 are a second voice in the same section: henchmen Dove
(feminine だわよ/わよ endings, named ダヴ at 78, 111, 114) and T-Bone
(named だーボーン at 87, 114), who call Beck "兄貴ィ" (Bro) throughout and
combine with him into the Great RX3 for the "ファイナル・トゥギャザー"
attack (114) -- Dove and T-Bone are the wiki-confirmed names of Beck's
henchmen who pilot the vehicles that form Great RX3. Recorded in
`analysis/voice_identity.json` under "145".

Found and fixed 11 deficient lines, run through `tools/check_voice.py` to
0 problems:

- **Wrong name, corpus-wide spelling**: entry 261, jp "どいてな、
  カン・ユー！" (Move aside, Kan Yu!) the seeded `"Move, Kang!"` misspelled
  the VOTOMS mercenary's name -- every other file that has him
  (`translation/voice_006.json`, `voice_007.json`, `voice_115.json`)
  spells him "Kan Yu". Fixed to `"Out, Kan Yu"`, reusing the exact
  English `voice_006.json`/`voice_007.json` already ship (entries
  362/357) for the near-identical jp "どいてろ、カン・ユー！", same
  11-cell budget. The wrong "Kang" spelling was traced to
  `translation/voice_008.json` (entries 366 and 369, "Move, Kang!" and
  "Back, Kang Yu") -- that file **still ships the misspelling**; it was
  not touched here (out of scope for a section-145 review) but should be
  corrected in a follow-up pass over section 8.
- **Dropped the second half of a two-beat line**: entry 26, jp "無駄無駄！
  そんな攻撃やめちまいな！" (Useless, useless! Quit that attack!)
  `"Useless, useless!"` -> `"No use! Stop that!"` (the "stop that attack"
  half was missing entirely, though the budget had 1 cell of slack --
  raised to fit exactly); entry 140, jp "へへへ！こりゃ使えるぜ！" (Heh
  heh heh! This'll come in handy!) `"Heh heh heh!"` -> `"Heh! Useful!"`
  (the laugh survived, the actual content -- that the trick is useful --
  did not); entry 177, jp "動く棺桶で、ご苦労さんだぜ！" (riding around
  in a moving coffin, good luck with that!) `"Mobile coffin"` ->
  `"Nice coffin!"` (the sarcastic jab was dropped, leaving a bare label).
- **Broken-grammar truncation** (missing question words, reading as
  clipped pidgin rather than a bark): entry 16, jp "なぁ～にやってんだよ！"
  (what are you doing?!) `"You doing?!"` -> `"What now?!"`; entry 23, jp
  "ちゃんと狙ってんのか、カラス野郎！" (are you even aiming, crow
  bastard!) `"You aiming crow?!"` -> `"Aim right, crow?!"`; entry 125, jp
  "や、やっぱり！？" (I-I knew it!?) `"I knew?!"` -> `"Knew it!"`; entry
  146, jp "ヘヘ！全て俺様の計算通りだぜ！" (heh, all according to MY
  plan!) `"Heh! All planned"` -> `"Heh! As planned!"`.
- **Register flattened**: entry 269, jp "見たか、スーパーゴージャス
  バリア様の力を！" (did you see the power of my Super GORGEOUS
  Barrier-sama!) `"See\nMy barrier's power!"` -> `"See\nmy Gorgeous
  Barrier"` (dropped the self-important "Gorgeous ...-sama" naming that
  is the entire joke of the line, consistent with Beck's "genius
  Beck-sama" self-address elsewhere in the section); entry 50, jp
  "お手並み拝見といこうか、ネゴシエイターさんよ！" (let's see what
  you've got, negotiator!) `"Show skill,\nnegotiator"` -> `"Show me,
  \nnegotiator!"` (grammatically incomplete and dropped the source's
  closing "！").
- **Subject miscounted**: entry 199, jp "お前らにも相当恥をかかされた
  からな！" (you lot have ALSO made me feel real shame!) `"You shamed us
  all!"` -> `"You shamed me too!"` (お前ら, plural "you," was read as
  making the *shamed* party plural too; Beck is narcissistically
  singular everywhere else in the section, and も means "also/too," not
  "all").

Quality read as noticeably cleaner than the section-158 pass above: no
swapped names, no meaning inversions, and mechanically clean (0 problems)
before any fixes were made -- the fixes here are truncation/register
polish and one corpus-wide misspelling, not the deeper mistranslations
158 needed.

**Voice: section 158 is Mikono Suzushiro (Aquarion EVOL)** -- Codex draft,
Sonnet-reviewed. This is the EARLIER point of the same Mikono arc already
shipped as section 159 (159's own identity note flagged the link before 158
was translated): entry 70's "I really am the girl who can't do anything"
(私はできっこない子なんだ) is the exact self-doubt that 159 answers at its
entries 6 and 156 ("No more saying I can't!" / "Won't lose...! No 'can't'
now!"). Teammates cutting in by name confirm the ensemble cast -- Amata (64,
72) and Cayenne (72) -- and Zessica is named in an empathic-link exchange at
112-114. Entries 132-139 are the masculine "ore" Trider G7 dig-and-fire combo
(159's note already identified this block as Watta Takeo's, byte-identical
Japanese to 159 entries 276-283); those 8 lines and 20 others were pre-seeded
from 159's shipped English and verified against it -- all 23 Japanese strings
158 shares with 159 carry matching English in both files, zero mismatches.
Recorded in `analysis/voice_identity.json` under "158".

Found and fixed 16 deficient lines out of 106, run through
`tools/check_voice.py` to 0 problems (was already 0 problems/106 answered
before this pass -- these are correctness fixes, not coverage gaps):

- **Dropped half a two-beat line**: entry 1, jp "ミコノ・スズシロ、攻撃を
  開始します！" (Mikono Suzushiro, beginning attack!) `"Mikono Suzushiro!"`
  -> `"Mikono, attacking!"` (kept the action -- the actual point of an
  attack-announcement bark -- over the bare surname); entry 30, jp "ミサイ
  ル…！　発射！" (Missile...! Fire!) `"Missile..."` -> `"Fire away!"` (the
  draft kept the weapon name and dropped the firing command); entry 126, jp
  "倍！　さらに倍！" (Double! Double again!) `"Double!"` -> `"x2! x4!"`
  (dropped the escalation entirely, budget 8 cells); entry 131, jp "ミサイ
  ル、全弾発射！" (Missile, full salvo!) `"Missile!"` -> `"Full fire!"`
  (the weapon is already named by three surrounding lines; this line's own
  content is the "all rounds" escalation).
- **Content word dropped where budget had slack it didn't use**: entry 10,
  jp "しっかり、ミコノ！" (Steady, Mikono!) `"Mikono!!"` -> `"Steady!"`
  (dropped the actual encouragement, kept only her name repeated); entry 57,
  jp "落ち着いて、ミコノ！　狙われてるよ！" (Calm down, Mikono! You're being
  targeted!) `"Mikono! Foe aims!"` -> `"Calm! Targeted!"` (dropped the "calm
  down" half of a reassurance motif that recurs across this section); entry
  26, jp "ミコノさん、あいつが来る！" (Mikono, he's coming!) `"Incoming!"`
  -> `"He's coming!"` (had 4 cells of unused budget and lost the specific
  referent for a generic one).
- **Register flattened**: entry 43, jp "やったよ、ミコノさん！　回避成功
  だ！" (Yes! Mikono! Evasion successful!) `"You dodged, Mikono"` ->
  `"Nailed it, Mikono!"` (a flat third-person statement stood in for a
  celebratory exclamation, dropping the source's "！" along with it).
- **Meaning inverted**: entry 49, jp "もし、バリアがなかったら…" (if there
  hadn't been a barrier...) `"No barrier..."` -> `"If not..."` (asserted the
  opposite of the counterfactual, right after entry 48 established there
  *was* a barrier).
- **Project-term consistency**: entry 13, jp "いけないな、彼女の鼓動がスト
  リンジェンドしている" `"Bad.\nHer pulse quickens"` -> `"Bad.\nHer heart:
  stringendo"` (this project already keeps "Stringendo" untranslated as an
  Aquarion EVOL musical term, `translation/voice_090.json`; the draft's
  generic paraphrase dropped the term).
- **Smaller register/grammar fixes within slack budget**: entry 2
  `"This?! I use it?!"` -> `"This?! Use it?!"` (broken grammar); entry 40
  `"Attack again"` -> `"If again...?"` (flattened a nervous conditional into
  a flat statement); entry 54 `"I think I'm okay"` -> `"I'm okay, but..."`
  (dropped the trailing "but," which sets up the anxiety spiral in the lines
  that follow); entry 75 `"No! No!"` -> `"No! Enough!"` (the second "no"
  carried もう -- "no more/enough" -- not a plain repeat); entry 109
  `"Behind Gepard!"` -> `"Get behind Gepard"` (an ambiguous noun phrase
  stood in for the actual retreat instruction); entry 31 `"Missile"` ->
  `"Missile!"` (missing terminal punctuation, inconsistent with every other
  exclamatory line in the file).

**Voice: section 91 is Shinn Asuka (Destiny Gundam)** -- Codex draft,
Sonnet-reviewed. Identity confirmed from content: entry 108 self-introduces
by name and mecha ("Shinn Asuka. Destiny, I'm going in!" for「シン・アスカ。
デスティニー、行きます！」), and the brief's three franchise anchors all check
out -- Kira Yamato addressed as "Kira-san" (146/155), Orb named directly
(120), and Stella (his dead partner from SEED Destiny) invoked at entry 204
in an accusation that ties into the section's "don't treat a life as
disposable" theme (160). The register holds his hot-headed, grief-driven
anger across two long villain-confrontation blocks (116-145/163-177/229-243/
332-346 arguing against an enemy's hollow "ideals"; 203-228/249-276/351-379
invoking Stella and accusing the enemy of using people as tools of war) and
a run of crossover ally-support exchanges naming Quattro Bajeena, Amuro Ray,
Kamille Bidan, Gyunei Guss, Setsuna F Seiei, Haman Karn and Full Frontal.
Recorded in `analysis/voice_identity.json` under "91".

Found and fixed 24 deficient lines, run through `tools/check_voice.py` to 0
problems after every fix (was already 0 problems/216 answered before this
pass -- these are correctness fixes, not coverage gaps):

- **Wrong character, four times**: entries 32, 39, 289 and 297 all address
  カミーユ (Kamille Bidan, glossed "Kamille") by name, but the draft
  substituted "Gyunei" -- a different, separately-addressed character in
  this same file (184/192, correctly rendered there). `"Gyunei, I go!"` ->
  `"Kamille, mine"` (32); `"Back, Gyunei!"` -> `"Back Kamille!"` (39);
  `"Gyunei, leave it!"` -> `"Kamille, leave it!"` (289); `"Gyunei, eyes up"`
  -> `"Kamille, watch!"` (297).
- **Wrong content**: entry 151's Japanese ("無愛想なやつと組むのは慣れてるよ！",
  I'm used to teaming with blunt guys) was answered with unrelated
  Virgo-formation content that belongs to a nearby but different line.
  `"Virgo team...!?"` -> `"I'm used to this!"`.
- **Direction flipped** (Shinn's own support offer rendered as an order to
  the ally instead): entry 31 `"Go, Quattro!"` -> `"For Quattro!"` (jp:
  "I'll support you, Captain Quattro!"); entry 33 `"Go, Amuro!"` ->
  `"Next, Amuro!"` (jp: "Captain Amuro, I'll follow up!"); entry 328
  `"Shinn, attack!"` -> `"Shinn attacks!"` (jp: "This is Shinn, striking the
  enemy ahead!" -- a radio self-report, not an order aimed at Shinn).
- **Meaning inverted**: entry 66 `"Damn! Don't gloat!"` -> `"Damn, won't
  quit!"` (jp 諦めてたまるか means "I won't give up," not a jab at the enemy
  gloating).
- **Mid-thought truncation**: entry 329 `"Fan out! Hit"` -> `"Spread out!"`
  (trailed off with no object for "Hit").
- **Unnatural coinage / broken grammar**: entry 59 `"Unstopped!"` ->
  `"Won't stop!"`; entry 68 `"You... damn!"` -> `"Damn you!!"`; entry 196
  `"Only you right?\nSure?!"` -> `"You alone\nare right?!"`; entry 197
  `"You fuel war!\nAll!"` (a dangling fragment) -> `"You spread\nthe war!"`.
- **Flattened rhetorical bite / weak register**: entry 0 (and its two shared
  repeats) `"Found you!"` -> `"No hiding!"` (そんな所にいたって means hiding
  there won't save you, not that Shinn located someone); entry 21 `"Go!!"`
  -> `"Here!"` (そこおっ names a location, not a command); entry 67 `"Not
  here!"` -> `"Won't lose here"` (dropped the "defeated" half of こんな所で
  やられてたまるか); entry 106 `"Kira! Come on"` -> `"Kira, what?!"` (キラさん、
  何やってんです is alarmed reproach, not casual encouragement); entry 204
  `"Stella again...?"` -> `"Stella's mistake?!"` (dropped which Stella
  reference -- her mistake -- the line is actually making); entry 222 `"No!
  \nAn evil god?!"` -> `"Enough!\nAn evil god?!"` (ふざけるな is a forceful
  "cut it out," not a mild "No"); entry 223 `"False gods! Foe"` (a sentence
  fragment) -> `"No gods! My foe!"`.
- **Dropped vocative where budget had room**: entry 148 `"I'll take it!"`
  -> `"Setsuna, mine!"`; entry 157 `"I'll do it!"` -> `"Setsuna, ok!"` (also
  fixes a meaning error: こっちはまだもつ is defensive "I can still hold,"
  not an offensive "I'll do it!"); entry 314 `"Don't push\nselfishness"` ->
  `"Don't push\nyour ideals"` (restores 理想/ideals, the section's recurring
  thematic word, dropped for an abstract noun); entry 330 `"I divide!"` ->
  `"I split!"` (more natural verb for 俺が敵を分断する in a tactical-call
  context).

**Voice: section 73 is Crea Dolosera (Aquarion EVOL)** -- Codex draft,
Sonnet-reviewed. Confirmed as Crea, chairwoman of Neo-DEAVA/Holy Angel
Academy, on content, not just title: she is addressed by name and title
together at entries 14/61 ("Crea, Chairwoman"), and her block matches her
library bio (translation/library/pt_360.json ENTRIES.378) beat for beat --
her Element ability, Teleport, is called out at entries 104/299; she is
"always together with Fudou," confirmed at entry 193 addressing him by
name; and she is "extremely fond of donuts, always kept on her desk,"
matched by entries 108 and 194's donut jokes. Entries 201-298 are the
cross-section shared musical-attack block (Crea's Teleport hand-off into
Shrade's solo Vector attack, the Vector-fusion embarrassment stock
content, and the Cayenne & Shrade "Requiem of the Master Musician" duet)
-- byte-identical Japanese to content already shipped in
`translation/voice_009.json`, `translation/voice_164.json` and
`work/voice/answer/101.json`; every matching entry was diffed against
those three files and the pre-seeded English matched verbatim in all 98
cases, so that block was left untouched. Recorded in
`analysis/voice_identity.json` under "73".

Five lines fixed out of 212, all meaning drift rather than budget
casualties. Entry 19 (「は、はい！　喜んで！」, "gladly") shipped as a flat
"Y-yes! OK", losing the eagerness; fixed to "Glad to!". Entry 42
("あなたが愚かという人類の力を見せましょう", "I'll show you the power that
proves you a fool") dropped the insult entirely, shipping "See humanity's
power!"; fixed to "Fool!\nSee our power!" to keep the rhetorical bite.
Entry 108 ("チョコドーナツより甘い攻撃です", mocking an enemy's attack as
softer than a chocolate donut) shipped as the non sequitur "Choco-donut
hit", losing the comparison and the joke; fixed to "Weak as a donut",
which keeps both the donut callback and the mockery. Entry 155 ("私とて
無傷で勝てるとは思っていません", "even I don't expect to win unscathed" --
an assertion that she'll win despite taking damage) shipped as passive
resignation, "I knew I'd get hit"; fixed to "Win, not unscathed" to
restore the "still wins" half. Entry 164 ("そんな事は私だってわかってます",
だって read as emphatic "even/already", an indignant retort) shipped as
"I know that too!", which reads as agreement instead of pushback; fixed
to "I know already!".

`check_voice.py work/voice/answer/073.json`: 212 of 212 answered, 0
problems, both before and after the fix (the five corrections were
meaning-only, no budget or charset issues). Quality: on par with the
079-era Codex draft (B+/A-) -- almost every other compression choice
held up under scrutiny (the "Chair" abbreviation for 理事長, invented
here since no prior section renders that title, is used consistently
across all ~20 occurrences; the reused shared-block lines were exact
matches, not paraphrases), and the five fixes were narrow, targeted
meaning corrections rather than a pattern of systemic register failure.

**Voice: section 79 is Sazanka Bianca (Aquarion EVOL)** -- Codex draft,
Sonnet-reviewed. Confirmed from content, not just the brief's claim: she
self-names in full at entry 3 ("Sazanka Bianca, here I come!") and her
Element ability is self-declared at entries 6-7 as corrosion ("my Element
ability is corrosion power!" / "I'll rot and decay all matter!"), matching
the claimed Corrosion Force ability; she's addressed by name throughout by
Mikono, Cayenne and Malloy, and the section is saturated with her fujoshi
seme/uke (攻め/受け) wordplay and shipping jokes. The shared combination-attack
duet with Cayenne and Shrade (entries 275-357, the same block documented in
009/073/090/101/164's own identity notes) was diffed programmatically
against the shipped `translation/voice_009.json` and `translation/voice_164.json`
by Japanese text: all 51 matches reuse the shipped English verbatim, 0
mismatches. Entries 373-380 (decoy-role lines) are not part of that block
and are Sazanka's own content. Recorded in `analysis/voice_identity.json`
under "79".

Ten lines corrected out of 238: entry 3 fixed a self-name typo
("Sazanke Bianca!" -> "Sazanka Bianca!" -- she misspells her own name in
her own introduction). Entry 2 ("今回は私が攻めだから！") shipped as the
flatly literal "I attack!", dropping the seme/uke pun that entries
18/23/33/36/37/41 all carry as a loanword -- fixed to "Seme today!" for
consistency. Entry 116 ("フッフッフッ、ムダムダ！") shipped "Ha ha! No no",
mistranslating ムダムダ ("useless/futile", a taunt) as a refusal -- fixed
to "Ha! Useless!". Entry 110 ("でしょ！") -- a confident "Right?!" seeking
agreement -- shipped as a confused "Eh?", inverting the emotional register
right before her own smug reaction line; fixed to "Right! Ha ha". Entry
134, a parenthetical inner thought ("I can't say I was staring at Lord
Cayenne...!"), shipped with the agency reversed as "(Cayenne made me
stare!)"; fixed to "(Can't say\nI stared at him)". Entry 148
("ドナール教官にお仕置きされちゃうよ～！", passive voice, self-directed) --
"I'll get punished by Instructor Donar" -- shipped as an outward threat,
"Donar will get you!"; fixed to "Donar'll punish me!". Entry 190 dropped
one name ("Yunoha") from a six-name photo list, silently cutting a named
character; fixed to fit all six as a slash list, "Mikono/Zessica/MIX/
Yunoha/Crea/Suomi". Entries 26, 30 and 378 each paraphrased away the
sentence's actual point under budget pressure -- 26 ("Amata's soul, yet?",
an unfinished fragment) fixed to "Same soul, not him"; 30 ("Women aren't
yours", inventing a claim the Japanese doesn't make) fixed to "Selfish
demands!" for the source's actual "such selfish demands" reproach; 378
("One-on-one?!", dropping the 余裕 "I've got this" boast entirely) fixed to
"1v1's easy..?", keeping both the confidence and its trailing self-doubt.

`check_voice.py work/voice/answer/079.json`: 238 of 238 answered, 0
problems. Cleaner than the section 090/101-era Codex drafts (B-/C+): most
of the doc's compression choices were sound wordplay under real budget
pressure (e.g. entry 80's 攻受/攻守 pun kept as "Uke? No, guard!", entry 41's
"seme/uke" ambiguity kept as "Hard to ship!"), landing closer to B+/A- once
the ten meaning-changing lines above were fixed.

**Voice: section 101 is Zessica Wong, piloting Aquarion Spada** -- filed as
Gundam Mk-II by a common weapon call-out, the same magnet the brief warns
against; wrong. Content resolves on four independent signals: (1) entries
418-419 are an unmistakable confession, "I like Amata" / "I like
Amataaa!!" (jp elongated to six vowels), matching Zessica's canonical
one-sided crush on Amata Sora, and entries 9-19 repeatedly cast fighting as
the only way she can help him; (2) her own machine is named throughout --
entries 60-63, 201, 207, 263, 280, 291, 299 discuss Spada's shield and
thinning armor as HER equipment, not an ally's; (3) the established
nickname exchange with Andy -- entries 35/199/235 call her "Wreck," the
rendering already shipped for this exact nickname (ドン底女) in
`translation/voice_049.json` (Kagura's file), and entry 36 has her fire
back "upside-down man" (逆さま男, no prior shipped rendering) at Andy;
entries 30/70/194/228 have her hailed as, or self-declare, "number one
girl," Zessica's other established self-boast; (4) she is addressed by
name throughout by Andy, Kagura, Mikono, Amata and Jin, and calls each of
them by name in return -- an ensemble voice bank like sections 15 (Amata),
090 (Shrade) and 164 (Yunoha). The section's shared combination-attack duet
with Cayenne (the block already identified from section 164's own identity
note, covering 009/073/079/090/101/164) shipped with English reused
verbatim from `translation/voice_009.json` and `translation/voice_164.json`
-- part of the 57 entries seeded before this session. Recorded in
`analysis/voice_identity.json` under "101". Entries 76-80, addressed to a
villain named Mikage in masculine だぜ speech, read as a different
speaker (likely Cayenne, whose rivalry with Mikage is a separate plot
thread) bundled into this section's climax exchange the same way the duet
is; left the pre-existing seeded English for 78-80 rather than re-guess
who exactly is speaking.

`check_voice.py work/voice/answer/101.json`: 287 of 287 answered, 0
problems. Budgets were tight throughout (a majority of first-draft lines
needed recompression); notable losses -- entry 27 keeps only "But I have
no one!" of the Amata/Mikono contrast, entry 70 drops the explicit "number
one" phrase for "my pride too," entry 248 drops "till I win" for a bare
"I won't stop!," and entry 302 ("Quit joking! not before love") compresses
"there's no way I'm dying before I fall in love" to its bones. Entries 20
and 28 share identical Japanese (「ゼシカ…」, budget 4) and both ship as
the truncated "Zess" -- not a collision, since the source lines are the
same string.

**Voice: section 139 is Bright Noa, captain of the Ra Cailum** -- unit filed
UNKNOWN (no weapon call-out matched). Content is a ship-bridge commander's
barks, not a mobile-suit pilot's: gunnery/missile/beam-cannon fire orders,
damage control, evasive-maneuver calls, and Minovsky-particle deployment.
`work/voice/mech_pilot.json` independently maps Ra Cailum -> Bright Noa, and
entry 142 has the speaker order "Ra Cailum" forward by name (a captain
naming his own ship in a helm order), while entry 155 separately orders the
allied Nahel Argama (captained per the same file by Otto Mitas) to fall in
behind "this ship." The decisive block (129-155) addresses subordinates by
rank immediately followed by name -- Captain/Amuro (a Captain rank in the
Char's Counterattack era), Ensign/Riddhe Marcenas -- plus direct addresses to
Hathaway Noa (Bright's own son), Kamille, Katz, Char, Haman and Banagher as
allied commanders, and an exasperated "Amuro what!" (147) matching the
franchise-established Bright/Amuro dynamic. Recorded in
`analysis/voice_identity.json` under "139".

`check_voice.py work/voice/answer/139.json`: 214 of 214 answered, 0
problems. Budgets were severe (196 of 214 first-draft lines needed
recompression to fit). Two glossed weapon names could not fit their slots
at all -- entries 62/63 (budget 11 and 9 against "Mega Particle Cannon")
ship as "MPC, fire!" / "MPC fire!", and entry 56 (budget 10 against
"Anti-Air Machine Gun") drops the weapon name entirely for "Open fire!";
entry 65 (budget 8 against "Volley Fire") keeps only "Volley!". The "Red
Comet" epithet lost its "Red" under pressure at 151, 167, 204 (kept) and
206 (kept) -- inconsistent by budget, not choice -- and "Londo Bell" was
dropped for space at 176, 210 and 233 (233 also drops "flagship" to
"leads"). Other lines lost a clause but not the core beat: 14 drops "stay
alert" to fit "It's the Red Comet!", 21 drops "intercept", 28 drops the
explicit "One Year War" phrase for "End it for good!", 121 drops its
second clause, 129 drops "opened a hole in the line" for "Captain,
thanks!", 144 drops the "Captain" title, 170 shifts "I don't think that's
all she's got" to a flatter "Haman's better?", 247 drops "break through
their line" for "Full speed ahead!", and 314 drops the "forgive me"
opener for "Lend your lives."

**Voice: section 090 is Shrade Eran (Aquarion EVOL), piloting Aquarion
Spada** -- filed as Gundam Mk-II by a common weapon call-out, one of the
magnets the brief warns against; wrong. Content matches Shrade Eran's
pilots.json bio beat for beat: a frail genius pianist who casts every
battle as a musical performance, willing to spend his own life for it --
the section's constant melody/harmony/perform vocabulary, its Italian
tempo-term barks (Adagio, Lento, Grave, Stringendo, Prestissimo), and its
recurring stake-my-life-for-the-music theme all point the same way; Spada
is named as his own machine twice. This is an ensemble voice bank like
sections 15 (Amata) and 164 (Yunoha): most lines are Shrade's own, but
name-addressed lines are the other cadets (Amata, Mikono, Cayenne, Malloy,
Andy, Jin) lending him power in character, not left anonymous. The
section's shared combination-attack duet with Cayenne (the block already
identified from section 164's own identity note, covering 090/009/073/
079/101/164) shipped with English reused verbatim from
`work/voice/answer/009.json` and `translation/voice_164.json`. Recorded in
`analysis/voice_identity.json` under "090".

A previous run was killed by a session limit after 120 of 252 entries;
finished the remaining 131 this session. `check_voice.py
work/voice/answer/090.json`: 251 of 251 answered, 0 problems. Budgets were
brutal throughout (several single-digit budgets); five entries lost
meaning to fit -- 191 dropped the explicit "friend" vocative, 213 and 234
compressed "I don't expect to win unscathed" / "I too must stake my life"
down to "Scars, I expect" / "Risk my life", 260 and 279 drop the explicit
word "melody" for space (the theme still carries from neighboring lines),
and 282 (budget 38 against a much longer sentence) compresses "beneath
your bluntness you approve of my sound, and now ask me to share it with
the players" down to "Heh-blunt, but you ask me to share it," losing the
"approve of my sound" clause.

**Voice: section 168 is Rezin Schnyder (Char's Counterattack)** -- Codex
draft, Sonnet-reviewed. The brief's attribution (Rezin Schnyder, cited on
an exchange about Gyunei Guss at entry 64) checked out: the section is a
hot-tempered female ace's battle-taunt voice set (feminine あたし
self-reference; mocking のさ/かい sentence endings), and entry 64's
「ガキが実戦に入るのかよ！」 -- "The brat's getting into real combat?!" --
matches Rezin's canonical scorn for Gyunei as a "fake Newtype" too green
for real combat. No self-naming or weapon call-out in the section, so
unit ships as null. Recorded in `analysis/voice_identity.json` under
"168".

One line corrected out of 30: entry 64 itself, the line the identity
claim rests on. The draft shipped "Brat in war?", which drops the
exclamatory mockery of のかよ！ and reads as a genuine question instead
of scornful disbelief. Fixed to "Brat, war?!" (11 of 12 cells), which
keeps the exclamation point the Japanese carries. The other 29 lines
were faithful, correctly registered (grunts, taunts and boasts land
where the Japanese has them, not softened into laughter or surprise),
and within budget as drafted -- markedly cleaner than the previous
Codex section's B-/C+. `check_voice.py work/voice/answer/168.json`:
30 of 30 answered, 0 problems.

**Voice: section 049 is Mithra Gnis, piloted by Kagura Demuri** --
filed UNKNOWN by the brief (no weapon-table match: the only weapons
named -- Dimension Tunnel Shell, Wings of the Sun, Missile -- aren't
his). Content match instead: the file is saturated with the obsessions
that pilots.json/robots.json give to no one else -- a feral hunter with
heightened smell (constant 匂い/臭い "scent/stink" barks), a fixation on
Mikono he calls 俺のクソ女 "my damn woman" (dozens of times), the
"reversed power" (逆さまの力) that is his unique Element ability per
DSC2, and direct address of his canonical rivals Amata and Mikage.
robots.json i=235 confirms RBTN ミスラ・グニス (glossary "Mithra Gnis")
lists PLTN カグラ・デムリ. Not a single speaker throughout, though: a
minority of entries are the other side of his support/combination-attack
banter, bundled into his voice bank the way SRW stores paired combo
dialogue -- Amata and Zessica both get reply lines in a 58-61 exchange;
Zessica recurs as a combo partner under two different teasing nicknames
(ドン底女 -> "Wreck", 穴埋め女 -> "Filler", kept distinct because the
Japanese differs); entries 0/255-264/316/348/356-357 are a separate
music-metaphor exchange (conductor/concerto/Allegro vivace) most
consistent with Claire Drossera ("headmaster", addressed directly at
71/357); 72/76 read as Mikono pleading mid-battle, not Kagura speaking;
389-392 are Mikage's villain monologue delivered at Kagura, not by him.
Entries 378-385 turned out to be byte-identical to section 159's
already-documented Watta Takeo (Trider G7) combo block ("I dig with all
I've got", calling ally "Gepard", firing the glossed Dimension Tunnel
Shell) -- confirmed not Kagura's own lines, and translated to match
159's shipped answers verbatim for consistency across the shared block;
entry 386 right after it is NOT part of that shared block and reads as
Kagura's own follow-up ("beyond love", echoing entry 120). Entries
369-375 are the idle/pause-screen fourth-wall omake seen in other
sections: it addresses "all you players" directly and self-corrects
俺...じゃねえ僕 (ore -> boku) mid-sentence, a register break with no
English pronoun equivalent, dropped rather than guessed at. Full
reasoning in `analysis/voice_identity.json` under "049". Budgets here
ran unusually tight (several single-digit slots); entry 384's own
weapon call-out could not fit "Dimension Tunnel Shell" into its
6-letter slot and ships as "Tunnel" -- flagged, not guessed. Not yet
confirmed by a screenshot.

**Voice: section 159 is Mikono Suzushiro (Aquarion EVOL), not Trider G7** --
filed as Trider G7 / Watta Takeo by a weapon-name match scored 1.0, the
same false-positive pattern the brief warns about for section 8. Wrong
for all but 8 of the 219 distinct lines: entries 276-283 are genuinely
Takeo's, a masculine hot-blooded combo-attack burst ("I dig with all
I've got!", calling out ally "Gepard", firing the glossed "Dimension
Tunnel Shell"), but the other 211 lines are first-person feminine
content naming Amata, Sazanka, Crea, Zessica, Yunoha, Shrade, and
Aquarion -- Aquarion EVOL, not Trider G7. The speaker is Mikono
Suzushiro: addressed by full name by Crea ("Mikono Suzushiro", entries
123/150/173/196), self-identifying as an Element (entry 2), and her arc
across the section ("I won't say I can't anymore", entry 6; "I'm not
the girl who can't now!", entry 156) directly answers the self-doubt
she voices throughout section 158 ("I really am the girl who can't do
anything", 158 entry 70) -- diffing both briefs' Japanese line tables
turns up exactly 23 shared strings (matching the brief's own "~23"
note), all from a common support/finisher pool (the Trider-G7 combo
block, the "Bye-bye Missile" finisher, generic support-guard lines)
rather than character content, so 158 reads as an earlier point in the
same Mikono arc and should carry the same attribution when it is
translated. Per `analysis/glossary.json`, Aquarion EVOL awakens "by
Amata and Mikono's boarding," i.e. she co-pilots the main combination
alongside Amata; unit recorded as Aquarion EVOL on that basis. Full
reasoning in `analysis/voice_identity.json` under "159", including a
line-by-line mapping for section 158's future translator to match
English on the shared combo block.

219 of 219 distinct lines translated, `check_voice.py` clean. Budget was
the binding constraint almost everywhere (initial drafts ran over budget
on more than 150 of 219 lines before compression), and entry 282 is a
genuine, unresolvable rule conflict: the glossed weapon name "Dimension
Tunnel Shell" cannot fit in a 6-letter budget by any measure, so it ships
as the bare fragment "Tunnel" -- flagged rather than guessed. A handful
of other entries lost a proper name to fit: 11 ships "Let's go!" without
"Mikono", 28/123/150/173/196 drop "Suzushiro" and keep only "Mikono" (or
just "Director" for Crea's honorific at 27/174), and 289's "even for ten
thousand and two thousand years" (a Yamato lyric callback) compresses to
a flat "12,000 years", losing the reference. Four near-duplicate English
strings from independent compression (entries 11/277, 29/281, 32/154,
84/85) were caught by `check_voice.py`'s collision check and given
distinct short lines instead.

**Voice: section 093 is Evangelion Unit-01, piloted by Shinji Ikari** --
filed as Big O / Roger Smith by a middling weapon-match score (2.0), the
same false-positive pattern the brief warns about for section 8, and
wrong: there's no Big O content anywhere in the 374 lines. This is
Rebuild-of-Evangelion Shinji through and through -- Misato calls him
シンジ君 constantly, a Kansai-dialect classmate addresses him as 転校生
("transfer student"), and his own lines run through the classic Shinji
anxieties verbatim from the 2007 film (why me, I just do what I'm told,
the enemy isn't even an Angel, why am I even piloting this) plus AT
Field / entry-plug-ejection / Third Impact vocabulary that only makes
sense for an EVA pilot. Bundles the usual nearby-cast lines: Misato runs
support throughout, Rei/Asuka/Mari appear as fellow EVA pilots, and
Shinji's "Volunteer Club" crossover arc pulls in Gunbuster's Simon and
Noriko, Code Geass's Kallen, Dai-Guard's Akagi, and Aquarion EVOL's Jin
Muso. Entries 260-298 are a distinct fourth-wall "next episode preview"
omake bolted onto the end of the voice bank (matching the pattern
documented for sections 56/87/131's epilogues): Shinji grudgingly reads
the preview in Misato's place, delivers stock anime-preview narration
including the genre-standard "service, service!" sign-off (kept as a
stock catchphrase), then the preview corner runs into unscripted-sounding
cast banter -- an unmistakable Kaji-to-Misato tease at 295-298 ("I even
know how badly you sleep", "that's how it is, see ya") and a
Kansai-dialect character volunteering to pilot the EVA in Shinji's
stead. Full reasoning in `analysis/voice_identity.json` under "93". Not
yet confirmed by a screenshot.

374 of 374 distinct lines translated, `check_voice.py` clean. Budgets were
severe throughout (many single-digit budgets for lines that read as full
sentences in Japanese), forcing heavy compression: the omake block's proper
nouns took the worst of it -- 261 ("ヱヴァンゲリヲン新劇場版") could only
fit "Rebuild of Evangelion" with no room for "finally joins"; 262 had to
drop "Volunteer" and ship a bare "the Club"; 281's "Super Robot Wars"
shrank to "SRW"; 150 and 336 each lost half a compound term ("Gurren
[Lagann]", "AT [Field]") to fit a name plus a verdict in one budget. A
handful of repeated-word Japanese lines (110 counting down, 246 and 306's
frantic repeated 止まれ/やらなきゃ) had their repeat count trimmed to fit
English's longer per-word cost, and a few lines (0, 44, 55, 111, 145, 185,
etc.) had to drop the exclamation mark entirely where budget could not
hold both a short word and the mark -- none were left in Japanese, and no
two distinct Japanese lines were left sharing the same English string.

**Voice: section 164 is Yunoha Thrul (Aquarion EVOL), plus a reused
Cayenne/Shrade/Zessica combination-attack cutscene embedded in the same
table** -- filed as Gundam Mk-II (2.0), the brief's own weapon-match
false positive, already flagged as wrong by an earlier reading that
pinned the pilot to Yunoha Thrul via her self-naming at entry 4
(`ユノハ・スルール！戦います！`, "Yunoha Thrul! I'll fight!") and entry 18.
That covers most of the section: a shy, earnest new Element/cadet who
worries about being a burden, is called "Jin's girl" by others several
times (32, 109, 178, 185, 258 -- confirming female by others' address,
not by name), and is paired with Jin Muso (glossary zukan_id 380,
`ジン君` rendered "Jin", no honorific), who self-refers with the male
pronoun "boku" at entry 238, licensing "he/Jin" rather than a name-only
guess.

Entries 275-357 (minus a few gaps) are a different matter: they are part
of the 129 records this section's own source JSON flags `shared: true`
-- a combination-attack cutscene stored byte-identical (same Japanese,
same budgets) in at least section 009 and four others the brief names
(073, 090, 101, 079). 51 of those entries were seeded verbatim from
`work/voice/answer/009.json`, which already ships this content, rather
than re-translated, for consistency across sections. Within that block,
275-294 and 343-357 are Cayenne and Shrade's own duet (male `ore`
register, call-and-response, mecha Spada and Gepard, attack name shipped
as "Requiem"/"Moon Requiem"/"Rhapsody" per 009's existing translation);
295-318 switch to an unmarked third voice giving embarrassed reactions
to Vector fusion ("so sensitive", "shame and relief"), consistent with
Zessica Wong's established comic-relief register. None of this is
evidence against the Yunoha attribution for the rest of the section --
it is reused stock content several pilots' voice banks carry alike (009
itself resolves to MIX, not this trio, for the same reason). Entries
373-376 are NOT part of the shared block and read as Yunoha's own
combination line (feminine "our"), kept as her voice. Full reasoning in
`analysis/voice_identity.json` under "164".

256 of 256 distinct lines translated, `check_voice.py` clean. Budgets
were severe (many single-digit to low-teens for full sentences),
forcing heavy compression throughout; nothing was left in Japanese.
Two early drafting passes produced entries keyed by the wrong index
(a bookkeeping slip mapping translations to sequential row numbers
instead of the actual entry numbers) and one batch of `\n` line breaks
was written as real newlines instead of the required literal
backslash-n -- both caught and fixed before this was reported, and
`check_voice.py` re-run clean afterward.

**Voice: section 047 is Aquarion Gepard, piloted by Andy W. Hole (content
reading -- not self-named in this section)** -- filed as unit "Genion GAI"
by a middling-score weapon match (1.0), the same false-positive pattern
the brief warns about for section 8, and wrong: there's no Genion content
anywhere (no Hibiki/Suzune/Knight register), and the glossary is pure
Aquarion EVOL. This is the same unit/pilot already identified for section
031: the speaker calls his own machine "Gepard" directly (3, 134, 160, 190,
291), his best friend Shrade is addressed constantly with a shared
music/melody motif (0, 21, 24-25, 63, 65-68, 145, 173-176, 190, 202, 298;
バイオリン/violin at 215, "ultimate melody" combo at 65/68), and the section
closes on the exact hole-digging finisher signature section 031 documents
for Andy (290-298: "I'll dig with everything I've got!", "Let's go,
Gepard!", "I... dig a hole!", "Dimension Tunnel Shell!", ending on a
called-out "Shrade!!"). Bundles the usual nearby-ally reaction lines
(Cayenne Suzushiro addressed respectfully throughout including an
unnamed Director/chairwoman exchange at 33-34, Sazanka at 122, MIX at 45/
177/205, Yunoha at 151-152, a fangirl aside about Cayenne at 121, rival
banter with Amata Sora at 13/17-18/46). One open thread: this speaker
repeatedly calls out his own "予知" (foresight/precognition, 103-104,
135-136, 163, 193, 199), which section 031's notes don't mention for
Andy -- translated at face value (hot-blooded pilot's sharp combat reads
described as "foresight"), flagged in `analysis/voice_identity.json`
under "47" in case a screenshot later attributes it to a different Gepard
pilot. Not yet confirmed by a screenshot.

231 of 231 distinct lines translated, `check_voice.py` clean. Budgets were
severe throughout (many single-digit to low-teens budgets for what read as
full sentences in Japanese), forcing heavy compression almost everywhere:
weapon call-out 296 ("次元隧道弾"/"Dimension Tunnel Shell", 6-letter budget)
could not hold the shipped weapon name at all and ships as a bare "Fire!"
-- FLAGGED, the one outright name loss. A handful of other lines lost a
clause or a name to fit (e.g. 121 drops "too dreamy", 143 drops Cayenne's
name-plus-mistake framing down to "That's a first" then recovered to
"Cayenne, a first", 197 keeps the name but drops "retreat" specificity
down to "Cayenne, run!"); none were left in Japanese.

**Voice: section 111 is the Tuatha de Danaan, captained by Teletha
Testarossa -- an ensemble section, not one pilot** -- filed as Big O /
Roger Smith by a middling weapon-match score (2.0), the same
false-positive pattern the brief warns about for section 8, and it's
wrong: there is no Big O content anywhere in the 243 lines. This is Full
Metal Panic bridge and battle chatter -- rudder/course/speed helm
orders, MBT vents, torpedo/Harpoon/Tomahawk/cruise-missile launches, the
submarine Tuatha de Danaan named directly (126, 310, 335), XO Mardukas
addressed by name (13, 115), and the ship personified as "this child"
and comforted/apologized to by pet name "Dana" (44, 97, 125, 131, 145,
147, 301, 309) -- all consistent with Captain Testarossa giving orders
and taking responsibility for her crew (117, 143, 156-157, 176,
178-181), kept distinct from Mardukas's formal register without
assigning her a pronoun (rule 7). The section bundles in three more
clusters under the same voice bank: Sousuke Sagara piloting Arbalest
under callsign Urzu 7 (263-280, Arbalest named at 279), a Kaname
Chidori/Melissa Mao ("Urzu 1") comic rest-break exchange plus Kalinin
dressing down Sergeant Sagara over Testarossa's "ace" status (311-327),
and confrontation lines against named rivals the glossary anticipated
inline -- Zeon's Char Aznable ("the Red Comet", 173) and Evangelion's
Third Impact (180); the Lambda Driver taunt (159) is FMP's own tech
turned on an FMP-side enemy, not a crossover mismatch. Recorded in
`analysis/voice_identity.json` under "111"; that entry flags 126 and
336-338 as speaker-ambiguous (translated so the English doesn't commit
either way) since the brief text alone can't confirm who's talking.

243 of 243 distinct lines translated, `check_voice.py` clean. Budgets
were severe throughout (several single-digit, one as tight as 2 letters
for 結構/"Ok"), forcing heavy compression on nearly every line: weapon
names were abbreviated past recognition in three spots because the
budget couldn't hold them at all -- 対艦ミサイル/"Anti-Ship Missile"
ships as "ASM" (10-letter budgets, entries 69, 73, 74, 76), 巡航ミサイル
/"Cruise Missile" ships as bare "Missiles"/"Fire" (9-12-letter budgets,
59-60, 64), and the glossary's own "Tuatha de Danaan" (16 letters
alone) doesn't fit entry 335's 16-letter budget alongside "surface!!"
so it ships abbreviated as "TDD, surface!!" -- all four FLAGGED. Several
other lines lost secondary clauses to fit (e.g. 315, 336, 338 drop a
clause each); none were left in Japanese.

**Voice: section 031 is Aquarion Gepard, piloted by Andy W. Hole** --
filed as Space Gunmarl / Darry Adai by a middling-score weapon match, the
same false-positive pattern as section 8's Strike Freedom hit, and it's
wrong: the section is saturated with Andy's own hole-digging motif
(holes, graves, "digger brothers" -- entries 3, 25, 27, 55, 73, 74, 86,
90, 99, 103, 108, 109, 125, 147, 150, 192, 193, 202, 299-303), he
self-names his full glossed name at entry 0 and is addressed by it at
138/168/195/220, and he calls his own machine "Gepard" directly at 43,
87, 112, 149, 192, 201 -- a bark ("やるぜ、ゲパルト！") that recurs
verbatim across many other sections' briefs for other Gepard pilots.
`analysis/glossary.json` confirms アクエリオンゲパルト -> "Aquarion
Gepard" (shipped short as "Gepard" elsewhere, e.g.
`work/voice/answer/009.json`'s "Spada and Gepard!") while ダリー・アダイ
/"Darry Adai" is a different character (Space Gunmarl's own pilot) who
never appears in the content. The section bundles in short reaction
lines from Andy's Aquarion EVOL castmates (Zessica, MIX, Yunoha,
Sazanka, Shrade, Amata, the academy Director) responding to or
praising/scolding him -- the normal "nearby ally" pattern for a pilot's
own voice file, not a second voice set. Andy's musical-nickname motif
(forte, capriccioso, appassionato, melody) recurs at 15, 128, 158, 184,
211, kept as the standard lowercase loanwords. Recorded in
`analysis/voice_identity.json` under "31".

227 of 227 distinct lines translated, `check_voice.py` clean. Budgets
were tight throughout (many single-digit to low-teens) and forced heavy
compression on nearly every line; nothing was flagged as unable to fit
except entry 92's weapon call-out, `次元隧道弾！`/"Dimension Tunnel
Shell", whose 6-letter budget cannot hold the shipped weapon name at
all -- it ships as the bare "Tunnel", FLAGGED, weapon name lost.

**Voice: section 015 is Aquarion (EVOL configuration), piloted by Amata
Sora** -- filed as "Genion GAI" by weapon match, score 2.0, and that's
wrong: both weapon-table entries (三位一体拳/Trinity Attack, 無限拳/Mugen
Attack) are Aquarion's own named finishers, and the section's full
glossary is pure Aquarion EVOL cast -- Amata Sora, Mikono, Zessica,
Kagura, Crea, Yunoha, Sazanka, Andy, Malloy, Shrade, MIX. The voice pool
is shared, not solo: most lines are Amata's own call-outs and hit/defeat
barks, but support and team-combination lines are voiced in character by
whichever cadet is lending power that turn (e.g. 20-23 is a two-line
Amata/Mikono exchange, 60-63 is Crea briefing Amata by his full name,
116-117 has Amata insisting to Kagura/Mikage he is not Apollo or Polon).
Recorded in `analysis/voice_identity.json` under "15".

421 of 421 distinct lines translated, `check_voice.py` clean. Budgets
were severe, especially the section's iconic one-word/two-word shouts:
entry 199's "超時空！" ("Hyperspace!", the lead-in to Aquarion's named
finisher) had only a 4-letter budget and could not carry any of that
meaning, so it shipped as the generic "Now!" -- FLAGGED, meaning lost.
Entry 654's bare "アクエリオン！" had a 7-letter budget against an
8-letter proper noun with no shorter true synonym, so it shipped as
"AQ!" -- FLAGGED. Entry 208's "アマタ！" (budget 4) shipped as "Ama!",
and entry 665's "ゼシカさん！" (budget 6) as "Zess!", both name
truncations rather than translations. The two weapon call-outs also hit
this wall: 187 and 200 (budget 7) and 190 (budget 11) could not fit
"Mugen Attack" in full and dropped "Attack", shipping "Mugen!!" and "Go,
Mugen!!"; entry 193 (budget 10, "the legendary Mugen Attack") lost both
"legendary" and "Attack" to become "My Mugen"; entry 656 ("Aquarion
EVOL!!", budget 12) dropped "Aquarion" to "AQ EVOL!!". Several \n-broken
two-clause lines lost secondary names to fit the combined budget --
entry 173 drops an explicit "Kagura" mention, entry 176 drops a second
"Mikono" repeat, entry 117 drops "or Polon" -- documented inline as
compressions rather than errors since the primary clause's meaning
survived.

**Voice: section 027 is VF-22S Sturmvogel II B, piloted by Gamlin
Kizaki** -- filed on a weapon match (score 2.0, "middling" per the brief's
own warning about section 8's false Kira Yamato/Strike Freedom hit) and
here the content confirms it: the speaker self-reports callsign "スカル４"
(Skull 4) in entries 5, 119, 177, 266, 284, 473 and 477, and the glossary
names his real Frontier castmates Michel, Klan, Ranka and Sheryl. Section
57 (already shipped) is the same pilot earlier in the story, callsign
"Diamond 1" of Diamond Force -- his pre-defection NUNS unit; this section
is the post-defection VF-22S under Skull Squadron, matching Macross
Frontier canon (Gamlin joins Skull as Skull 4 after defecting), and the
two sections' registers match (rough masculine ore/ze hot-blooded pilot).
The section's content runs the length of the whole crossover game, not
just Frontier: Zentran taunts, a "Red Comet" rival line (343, Char
Aznable's epithet), a "root calamity... Baal" line (358, Break Blade),
and direct address to Gundam 00's Graham and Quattro Bajeena (342,
445, 456-457) and Aquarion EVOL's Amata (444, 449) -- all names the
brief's own glossary anticipated, read as one pilot's arc across a
crossover story rather than a misattribution. Recorded in
`analysis/voice_identity.json` under "27". No twin section noted in the
brief.

FLAGGED as uncertain: entries 442-462 are a distinct block -- high-school
"club activity"/"volunteer work" phrasing addressed at or about Amata and
thanking "Major Graham" (442-449), running into a fourth-wall idle/standby
Easter egg (451-462) where the speaker is alone, muses about the game
having companions including "you, the player", names the game itself
("第3次スーパーロボット大戦Z"/Super Robot Wars Z3), and begs the player to
come back. This register doesn't obviously match Gamlin's hot-blooded
voice elsewhere in the section, and this kind of self-aware idle line is
usually reserved for one flagship character per game -- but no other
show's mecha/weapon is named in it (unlike the section-8 case) and no
duplicate of these lines exists elsewhere in the corpus to attribute
them to instead, so it shipped under the Gamlin attribution, translated
as written, with the doubt recorded in `analysis/voice_identity.json`.

286 of 287 distinct lines translated (287 to translate per the brief;
entry 452, the developers' silence line "………", ships as Japanese by
omission per the brief's own instruction). `check_voice.py` clean, no
duplicate English strings. Budgets were severe throughout; notable
compressions: entry 180's Zeami quote ("思わざれば花なり、思えば花なら
ざりき", budget 18) collapsed the whole thought/no-thought antithesis to
"Unthought flower."; entries 158, 174, 335, 338, 342 and others had to
drop the recurring "Tornado" (equipment pack) name to fit; entry 343
dropped "Red Comet" for "No mercy!"; entry 283 dropped "Michel" for "Good
spot!"; entries 184 and 445 similarly dropped "Fire Bomber" and "Graham"
by name. Several weapon call-outs (265, 269) had too little budget for
the shipped "Reaction Missile" name and shipped generic "Fire!"/"Fire
it!" instead.

**Voice: section 032 is a Mobile Suit Gundam 00 pair, likely Kati and
Patrick Mannequin** -- unit UNKNOWN, no weapon call-out matched and the
brief carried no weapon or glossary table. Content is unmistakably the
"A Wakening of the Trailblazer" movie setting: the speaker addresses
Gundam as an ally (entries 42, 43, 49, 50), addresses/commands Celestial
Being (44, 51 -- shipped term, `work/tr/GLOSSARY.md` line 134), names its
own side "連邦軍" (Earth Federation Forces, entry 46 --
`source/library/keywords.json` line 664 confirms this is the 00-setting
Federation, distinct from Celestial Being), and worries about GN-particle
reserves and thrust (56, 63). Two voices appear bundled in the file, the
project's established pattern (see section 13's Asuka/Misato): a majority
私-voice, calm and commanding, protecting citizens and peace (6, 7, 8, 15,
48) and ordering Celestial Being to fall back (51), addressed as "少佐"
(Major) by a second, minority 自分-voice that defers to that Major (40,
45, 47) and is self-critical about mistakes when hit (54, 55). Entry 53
("あなたには不死身でいてもらわないと！", "you need to stay
undying/immortal!") reads as a callback to Patrick Mannequin's canonical
nickname "不死身のコーラサワー" ("the Undying Kolasour", per
`source/library/pilots.json` lines 1222-1223 -- an ex-AEU ace married to
Kati Mannequin who still calls her by military rank out of habit), which
is what points the 私-voice at Kati Mannequin and the 自分-voice at
Patrick. Recorded in `analysis/voice_identity.json` under "32", flagged
there as a strong but unconfirmed reading (no screenshot, no explicit
self-naming line in these 72 entries). 72 of 72 distinct lines
translated, `check_voice.py` clean. Budgets were severe throughout;
notable compressions: entry 44 and 51 both had to drop "Celestial Being"
entirely to fit ("Leave it to me!" / "Fall back!") rather than repeat a
half-cut name in both; entry 46 dropped "Federation" for "Our teamwork!";
entries 56 and 63 generalized "GN particle" reserves/thrust to "GN low?!"
and "More thrust"; entry 87 ("まだだ！\n安寧を脅かす脅威を排除するまでは
…！", budget 25) restructured to "Not done!\ntill it's safe!", trading the
literal "threat" for "safe".

**Voice: section 030 is Granzeboma, piloted by the Anti-Spiral** -- filed
as Granzeboma on a weapon-name match at score 2.5 (a "middling" score this
project has learned to distrust), but here the content confirms the match
rather than contradicting it: the lines repeatedly invoke Spiral race and
Spiral warriors (entries 15-17, 20, 66), address Gunmen (entry 20), taunt
in the Anti-Spiral's cosmic-ruler register ("in this universe we rule",
entry 11; "we who are the universe itself", entry 14), and the
finishing-move shout at entries 57/60 is literally "インフィニティ・
ビッグバン・ストォォォォォム" (Infinity Big Bang Storm), Granzeboma's
canonical finisher from *Gurren Lagann the Movie 2: The Lights in the Sky
are Stars* -- the same film `analysis/glossary.json`'s zukan_id 209 entry
(Granzeboma, status official) already cites as its source. Entry 63 has
the pilot name itself outright: "反螺旋ッ！！" (Anti-Spiral!!). Recorded in
`analysis/voice_identity.json` under "30". No twin section noted in the
brief. 63 of 63 distinct lines translated, `check_voice.py` clean.
Budgets were severe throughout (several single-digit, one as low as 6
letters for "反螺旋ッ！！"/Anti-Spiral, shipped as "Anti!!"); other notable
compressions: entry 24 ("母星を守るなどという\n狭い視野しか持たぬ者などに
…！", budget 27) dropped the "those who have nothing but" framing for "So
narrow,\njust guard home!"; entry 85 ("最後まで足掻く事を美しいと感じる！
\nそれがお前達の本能だ！", budget 31) dropped the closing "that's your
instinct" clause entirely, keeping only "I find beauty\nin your struggle!";
entry 12 ("宇宙を守るための覚悟が、\nお前達にあるか！", budget 22) shipped
"Resolve to\nprotect it?" without naming the universe it refers to. No
weapon table was provided for this section, so rule 5 (shipped weapon
names) did not apply.

**Voice: section 029 is a Sleeves Personal Guard grunt pilot loyal to Full
Frontal, not Gundam Mk-II** -- filed as Gundam Mk-II on a beam-rifle/vulcan
weapon-name match (score 1.0), the same common-weapon magnet that already
misfiled sections 117-119 (generic Neo Zeon grunts) and 189/190 (a Sleeves
Personal Guard grunt under Angelo Sauper/Full Frontal, per
`analysis/voice_identity.json`). This section is the same faction and role
as 189/190 -- a rank-and-file Personal Guard (親衛隊) pilot of Full
Frontal's Sleeves from Mobile Suit Gundam Unicorn, addressing an unnamed
superior as both "大佐" (Colonel) and "総帥" (Commander, both established
translations reused from 189/117), naming Garencieres (Frontal's ship),
demanding Laplace's Box, and fighting Londo Bell's ace (Banagher/Unicorn
Gundam) and Amuro Ray by name -- but it is a distinct voice set, not a
twin of 189/190. The section's own tell: it addresses Gyunei Guss by name
twice (entries 115, 124), mockingly, during combat. `source/library/pilots.json`
confirms Gyunei Guss is a Char's-Counterattack-era Neo Zeon pilot loyal to
Char/the original Neo Zeon leadership, not a Sleeves character, so within
this crossover he is fought here as a rival from a competing "who carries
Char's legacy" faction, not addressed as a fellow guardsman. No line
self-names the speaker (always first-person); recorded as an unnamed
Personal Guard grunt in `analysis/voice_identity.json` under "29", not yet
confirmed by a screenshot. 163 of 163 distinct lines translated,
`check_voice.py` clean. Budgets were very tight throughout (many under 15
letters, several under 10); character names and titles were frequently
dropped to fit, keeping only the core sentiment -- e.g. entry 33
("ソレスタルビーイングのガンダムか…！", budget 18) reused the exact
"Celestial Being?!" already shipped for the near-identical line in 189;
entry 34 ("コロニーのガンダムが連邦に手を貸すか！", budget 19) shipped "A
colony Gundam?!", dropping the "aiding the Federation" clause; entry 54
("スペースノイドの敵となった\nニュータイプなど…！", budget 25) shipped "A
traitor\nNewtype...!", dropping "Spacenoids" in favor of keeping
"Newtype"; entry 116 ("目障りだ、小娘！", budget 8) shipped "Eyesore!",
dropping the "girl" address that budget 125's near-twin line ("下がって
いろ、小娘！" -> "Off, girl!") kept. Entries 5 and 25 are independently
listed, byte-identical lines ("消えろっ！", budget 5 each) and intentionally
ship the same English ("Gone!") -- not a same-English-for-different-Japanese
collapse.

**Voice: section 016, unit UNKNOWN, an unidentified Aquarion EVOL pilot
protecting Mikono Suzushiro** -- no weapon call-out matched at all
(`sections.json` scores it 0, unit null). Content is Aquarion EVOL: the
speaker fights to protect Mikono Suzushiro (glossed) and addresses Amata
Sora (glossed) directly and with concern ("A-Amata!", "Amata...") as a
separate person, not as a self-reference, so the speaker is not Amata.
Entry 95 ("We finally did the male-female combination, and this is as far
as we get?!") establishes the speaker is themself the current male half
combined with Mikono's Vector for this fight, not Amata's usual pairing --
the speaker is masculine-coded (ore), explicitly green at this (fumbling
"Like this?! Or this?!", reacting to an enemy as unfamiliar, told to "Back
off!" as an amateur) and fighting the Abductors, Aquarion EVOL's canon
antagonists. No line self-names the speaker; the section's own Aquarion
roster (Amata, Zessica, Cayenne Suzushiro, Mikono, Andy, Shrade, Yunoha)
has no other named male pilot who fits being freshly paired with Mikono
while Amata is elsewhere and worried about. Most likely a scenario-
specific substitute pilot in Amata's usual slot (a common SRW original-
scenario device), but nothing pins a canonical name, so it ships as an
unidentified pilot voice per the standing "unit null" convention recorded
in `analysis/voice_identity.json` under "16". 84 of 84 distinct lines
translated, `check_voice.py` clean. Budgets were exceptionally tight
(several 5-9 letter budgets); most lines dropped stutters or ellipses to
keep the exclamation mark and the core word, per the project's own
priority order. Meaning was measurably compressed on a handful of
entries: 8 ("素人は手を出すな！", budget 9) shipped "Back off!", dropping
"amateur"; 61 ("気を抜くな！次が来るぞ！", budget 13) shipped "Stay
sharp!", dropping the "more coming" clause; 84 ("泣き言を言う前に動け！死
にたいのか！", budget 19) shipped "Move, don't whine!", dropping "wanna
die?!"; 99 ("ごめん、ミコノさん…ごめん…", budget 14) shipped "Sorry,
Mikono.", dropping the repeated "sorry" and its trailing ellipsis. Three
hit-taken screams (71/91/98, all "きゃあ" variants) keep the
conventionally feminine scream sound even though the speaker's own
self-reference is masculine elsewhere -- read as ordinary scripted pained
yelps, not evidence against the ore lines, and no pronoun choice was
actually needed for any of the 84 lines shipped.

**Voice: section 028 is Gundam Harute, voiced by Lockon Stratos (Lyle
Dylandy), not Dancouga Nova Max God / Aoi Hidaka** -- filed as Dancouga
Nova Max God / Aoi Hidaka on a middling weapon-name-match score, wrong,
the same pattern as section 8's Strike Freedom/Kira Yamato misfile. The
128 lines are unmistakably Mobile Suit Gundam 00 (the movie A Wakening of
the Trailblazer): the pilot names their own machine "Gundam Harute"
repeatedly, uses Trans-Am, and the section's own glossary terms (Tieria,
Lockon, Hallelujah, Allelujah, Sumeragi, Ian, Marie) are all Gundam 00
cast, not Dancouga's or SEED's. Two lines address "Allelujah" directly as
a rival ("too soft, Allelujah", "you've finally come, Allelujah"), which
rules out Allelujah/Hallelujah Haptism as the speaker; a companion
"Marie" rides along and is repeatedly thanked/addressed, and a mechanic
"Ian" is complimented once -- matching Marie Parfacy and Ian Vashti, both
tied to Lyle Dylandy, the second Lockon Stratos, who pilots Harute in the
movie. No line has the pilot self-name, so the pilot attribution is the
best-supported reading from content and canon, not a confirmed
self-introduction -- recorded as probable in `analysis/voice_identity.json`
under "28". "飛鷹葵/Aoi Hidaka" from the original filing does not appear
anywhere in the lines. 128 of 128 distinct lines translated,
`check_voice.py` clean. Budgets were extremely tight throughout (single-
digit budgets were common); most named-character references (Harute,
Marie, Allelujah, Ian, Tieria, Lockon, Sumeragi, Setsuna) had to be
dropped from their lines to fit, keeping only the surrounding sentiment --
flagged entries: 24 ("マリー！", budget 4) shipped "Hey!", dropping the
name entirely; 84 ("アレルヤ！", budget 5) shipped "Yo!" for the same
reason; 42 ("甘めぇぜ、アレルヤ！", budget 10) dropped "too soft" to keep
just "Allelujah!"; 50/51 ("未来を…！"/"明日を！", budgets 5/4) shipped
"Hope!"/"Soon" in place of "future"/"tomorrow" to fit and stay distinct
from each other. Entries 27/23/31 (all トランザム variants) ship
"TransOn"/"Trans!"/"TransAm!" respectively, matching the compressed
Trans-Am forms already shipped at sections 170 and 208.

**Voice: sections 022, 024 and 026** -- unit UNKNOWN, no weapon call-out
matched at all. Content is Aquarion EVOL / Neo-DEM: the same "Rare Iglar" /
"true Eve" hunt already attributed to Altair grunt pilots at sections
21/23/25, but a different, comedic register -- a hot-blooded soldier
declaring a personal, romantic quest for love and "his own Eve" (身体がと
ろける, ドキドキが止まらん) rather than the mission-report chatter (capture
orders, signal call-outs, guard duty) of 21/23/25. No line self-names, so
this ships as another unidentified Altair/Neo-DEM rank-and-file pilot --
same faction and plot point, distinct comic-relief voice set. Recorded in
`analysis/voice_identity.json` as "22"/"24"/"26": pilot null, unit null;
all three sections are the same pilot per the brief and ship the same 10
lines. Shipped "Rare Iglar" (not "Iglur") to match the term already used at
sections 21/23/25. Sections 024 and 026's 10 index entries map one-to-one
onto 022's (same budgets throughout) and ship byte-identical English. 10 of
10 lines translated in each section, `check_voice.py` clean; `merge_voice.py`
run for all three (022, 024, 026 -> translation/voice_02{2,4,6}.json). Entry
5/6 ("俺のイヴ！　俺だけのレア・イグラー！", budget 18) dropped "My Eve" to
fit -- shipped "My own Rare Iglar!" alone. Entry 3/4 ("ああ！　トキメキで
身体がとろける！", budget 17) dropped the "ああ" exclamation -- shipped
"Thrill melts me!". Entry 4/5 ("ドキドキが止まらんーっ！！", budget 13)
shipped "Heart races!!" (continuous racing rather than "won't stop").

**Voice: section 5 is Dragon's Hive, voiced by F.S. and Commander Tanaka
(not Strike Freedom Gundam)** -- filed as Strike Freedom Gundam / Kira
Yamato (weapon-match, score 1.2), wrong: no SEED content anywhere in the
section. This is Dragon's Hive, the dragon-shaped mothership/combat unit
from Chou Kishin Dancouga Nova (SRW Z2 Saisei-hen / Z3), and per
docs/TRANSLATING.md ("a section is one UNIT's voice set... and a unit
with a main pilot and a sub pilot carries both") it holds two speakers.
Entries 0-1 open with the Dancouga Nova combination call. Entries 2-141
are mostly F.S.: he self-identifies via the Fog Sweeper wordplay at entry
11 ("So that's what it means to be the Fog Sweeper... that's you?"),
matching translation/library/pt_280.json #301 ("F.S. is taken from the
initials of 'Fog Sweeper'"), develops the fog/hope theme (10, 13), gives
fleet commands (30-45), addresses WILL directly (12, 104, 240), and closes
with his catchphrase "Yatte yaru ze!" at 42 and 250 (pt_280 #301's
documented catchphrase). A breezier, self-deprecating, deflecting register
runs through 113-141 and 196-245, and entries 246-249 are a self-contained
comic vignette where the speaker jokes about preferring rest to combat and
explicitly addresses "F.S." by name before a fourth-wall "next time, SRW
Z3!" gag -- the same next-episode-preview joke format already shipped for
other pilots (voice_086, 087, 173, 184, 191, 193, 208, 210). Since someone
else addresses F.S. by name, this second voice is Commander Tanaka
(pt_280 #302, Dragon's Hive's battle commander and Team D's direct
superior): "mild-mannered and unassuming, always facing matters with a
nonchalant, easygoing attitude" and self-described as "nothing more than
a middle manager" -- an exact match for 246-247's humor and a good fit
for the deflecting enemy banter elsewhere. Both are established "he" in
this project's own shipped translation (pt_280.json #301, #302); WILL is
established "it" (#303); Sammy (Dragon's Hive's chief mechanic) and Aoi
Hidaka are addressed by name but do not speak here. Could not
conclusively assign every individual line between F.S. and Tanaka --
shipped as the Dragon's Hive unit's ensemble voice set (F.S. main, Tanaka
secondary). Recorded in `analysis/voice_identity.json`. 189 of 189
distinct lines translated, `check_voice.py` clean. Budget forced meaning
loss on several lines where the compression cut a modifier or the
"Dragon's Hive"/"humanity" name to fit (e.g. 24, 25, 28, 60, 62, 64, 96,
102, 123), and entry 9's classical "flying dragon rides the clouds" idiom
compresses to "Our time!", losing the dragon imagery entirely.

**Voice: section 131 is Haman Karn, piloting Qubeley** -- filed as Nu Gundam
/ Amuro Ray (3.0) via Beam Confuse/Fin Funnel/Funnel call-outs, the same
weapon magnet that misfiled 56 (Kamille's Zeta), 68 (Quess Paraya's Alpha
Azieru) and 87 (Char's Sazabi). Settled by two first-person self-namings
plus an outside cross-check: entry 335 says "I am Haman Karn...! Until the
very last moment!", entry 120 calls the speaker's own unit "this Qubeley",
and entry 323 has an attacker come at "this Haman" (i.e. the speaker);
`work/voice/mech_pilot.json` independently maps Qubeley -> Haman Karn. This
resolves section 68's open speculation that 56/87/131 might all be "the
Colonel's [Char's] own voice set" on account of addressing Quess Paraya by
name -- 87 confirmed that guess for itself, but 131 reuses the same
by-name-address pattern for a different character: Haman's canonical
Newtype-supremacist rivalry with Kamille Bidan (addressed hostilely
throughout, plus recruitment offers), running exchanges with Char and
Amuro, and a later block confronting Full Frontal as a usurper alongside
Marida Cruz and Banagher Links in both hostile and mentoring registers --
consistent with a Z3 crossover where Haman's Qubeley reaches into the
Unicorn-era cast, matching the cross-era epilogue device already
documented for sections 56 and 87 (this section's own epilogue at
340-344 names "Super Robot Wars" and addresses "players" directly). Two
lines (145, 256) have the speaker piloting a Gundam and using "the Zeta's
power" -- translated as-is, not verified against a specific in-story
scene. Recorded in `analysis/voice_identity.json`. 218 of 218 distinct
lines translated, `check_voice.py` clean, no duplicate values. Budget
forced meaning loss on a handful of name-heavy lines (121, 128, 250, 287,
289, 290, 291, 298, 311, 327) where a glossary name ate nearly the whole
slot, leaving no room for the accompanying compliment/insult/verb --
flagged in the session report; the glossary name was kept over the extra
color in every case.

**Voice: section 11, unnamed enemy pilot -- weapon evidence contradicted by
content** -- filed as Gundam Mk-II (2.0), but unlike the other Mk-II
false-positives this one isn't a generic beam-rifle/vulcan magnet: weapon
record 333 is Shield Launcher, genuinely owned by unit id 0x3100207 =
Gundam Mk-II, matched at entries 162/215 (the two shield call-outs). The
content still rules out Mk-II as the speaker -- twelve lines address an
opponent named "Gundam" in the third person ("I'll drop Gundam!", "We
match Gundam!", "Not over, Gundam!"), which a unit cannot say of itself.
Speaker self-describes with a shield ("I'm a shield!", "I have a
shield!"), rough masculine tough-guy register, derides a civilian company
having no business here, and vows not to let the enemy have Earth --
reads as an unnamed Titans (or otherwise military) grunt piloting one of
Titans' own Mk-IIs (as in canon, before Kamille's crew steals one) or
another shield-carrying unit sharing the weapon name, taunting a
separately-named Gundam-type unit. No pilot names themself, so it ships
as unnamed battle barks -- "Gundam" is kept only where the line names the
addressed opponent, never inserted for the speaker. Recorded in
`analysis/voice_identity.json` under both 11 and 12 (section 12 is the
same 116-line voice set per the brief and must carry matching English
when it's translated). 116 of 116 distinct lines translated,
`check_voice.py` clean, no duplicate values.

**Voice: section 10 is MIXY, piloting Mixy Gnis** — no weapon call-out
matched, but two lines self-name the speaker ("My name is MIXY...!" and
"I'm not MIX...! I'm MIXY!"), and MIX/MIXY/Mixy Gnis are all glossed pilots
and robot (analysis/glossary.json). translation/library/pt_360.json and
rt_200.json fill in the backstory: MIX is a Neo-DEAVA cadet who hates men
and "the very existence of holes," captured by Altair and, under the
"Curse of Eve," turned male and memory-wiped into the soldier MIXY. That
explains an otherwise-baffling "I hate holes...!" bark (entry 12) as MIX's
suppressed personality breaking through, and several deja-vu/headache
lines as memory fragments resurfacing. The ability call-out "Spatial
Compensation!" (entries 95/97) matches MIX's Element ability from
pt_360.json and reuses "Fill!", already shipped for the identical line in
voice_021.json. Altair (not "Alteria"), Vega, and "Angel" (for 機械天使)
follow existing project precedent from voice_021/023/025; Gnis follows the
canonical robot-name spelling even though this section's glossary table
doesn't list it. Recorded in analysis/voice_identity.json. 75 of 75
distinct lines translated, `check_voice.py` clean, no duplicate values.

**Voice: section 96 is Genion, but a third, unidentified pilot** — weapon
call-outs (Impact Dagger, Nitro Pike, Punisher, TS-DEMON, Glaive) confirm
the unit as Genion, matching what's already shipped for it in sections
133/134, but the speaker is neither of section 134's pair (Hibiki
Kamishiro, hot-blooded; Suzune/Sensei, calm navigator). This voice is
frightened and self-doubting, female speech patterns throughout, and the
closing two lines apologize by name to both Hibiki and Knight (ナイト,
already shipped as the name "Knight" in stage0003_03.json and called out
by Suzune in voice_133.json) — so she is addressing them as separate
people, not speaking as either. Suzune's own bio (source/library/pilots.json
i=392) says she fights "alongside her students," implying more than one
student pilots Genion; this is most likely one of those unnamed students.
Recorded in `analysis/voice_identity.json`. 50 of 50 distinct lines
translated, `check_voice.py` clean, no duplicate values. Entry 5 ("Nitro
Pike" call-out, budget 8) couldn't fit the 10-letter shipped weapon name
at all — shipped as a generic "Go now!" bark instead of an invented
abbreviation, flagged in the brief report.

**Voice: section 87 is Char Aznable's Sazabi** — self-named twice, the
"no longer Quattro Bajeena" reveal near-verbatim, the CCA gravity
speech, orders to Quess and Gyunei, and a fourth-wall epilogue naming
SRW Z3. The funnel call-outs shared across funnel units are what fed
the Nu Gundam magnet. 218 lines; recorded in voice_identity.json (which
a concurrent edit had corrupted — recovered from HEAD, all findings
preserved). Section 131 stays open, same pattern.

**Voice: section 000** -- unit UNKNOWN, no weapon call-out matched. Speaker
identified from content alone, cross-checked against `work/tr/pt_0240.md`
(character bios, id 262-264): this is Full Metal Panic!'s terrorist group
A21. The register (hot-blooded, self-destructive, first-person plural
"俺達"/"we" throughout, wanting to "burn" a "rotten world", A21 named
explicitly at entries 17/227, a reference to mentor Takechi Seiji's death
at entry 15) matches Takuma Kugayama, Behemoth's pilot -- not commander
Seina, who the bios describe as coldly composed. Recorded in
`analysis/voice_identity.json`. Two lines (171 "Takuma!", 223 "Takuma,
go!") address Takuma by name and read as Seina's own paired response
lines riding along on Behemoth's single voice table, since Seina has no
independent unit of her own in battle; no pronouns were needed in the
English so the ambiguity doesn't surface in the shipped text. This same
pilot's phrasing recurs in section 1 per the brief's cross-reference.
129 of 129 distinct lines translated, `check_voice.py` clean, no
duplicate values. Budget forced heavy compression throughout -- entry 55
drops "Kozuki" to fit the glossary's full "Kallen Kozuki" into an
8-letter budget ("Kallen?!"), entry 174 drops Seina's name entirely to
fit "Retreat!" (8-letter budget with no room for both a name and a
verb), entry 222 drops Seina's name to fit "I'm sorry!" (10-letter
budget), entry 218 compresses "cornered is when we're strongest" down
to the terse "Trapped, thrive!" to fit a 17-letter budget, and several
entries (26, 178, 207, 212, 215, 221, 231) drop a trailing exclamation
mark to make budget.

**Voice: section 001** -- same voice set as section 000 above: unit
UNKNOWN (no weapon call-out matched), speaker Kugayama Takuma, pilot of
A21's Behemoth. Confirmed independently before comparing notes: same
pilots.json bios (id 263 Seina/264 Takuma), same robots.json entry 186
(Behemoth, PLTN Kugayama Takuma, no co-pilot), same register and the same
named enemies (Kallen Kozuki, C.C., Mithril, Gundam). Section 001 turned
out to carry the identical pool of 129 distinct Japanese lines as section
000 (127 byte-identical, 2 trivial variants -- a `\n` falling one word
earlier, and a script typo `慣れした`/`慣れた`) under a different, non-offset
entry-number assignment and identical per-line budgets throughout, so per
the brief's own cross-reference ("this pilot also speaks in sections 0 --
the same phrasing should be used there") the 85 lines that had drifted
from an independent first pass were reconciled to section 000's already-
shipped English; the 2 near-duplicates were matched to 000's phrasing by
meaning (entry 200 "Veteran, huh!" for 000's singular "Veterans, huh!",
compressed one letter to fit; entry 48 "We both\nlive to fight!" reused
verbatim from 000's line 60, the `\n` re-placed since the two sections
break the same sentence at different words). 129 of 129 distinct lines
translated, `check_voice.py` clean, no duplicate values. `analysis/
voice_identity.json`'s "1" entry cross-references "0" rather than
repeating the full reasoning.

**Voice: section 084** -- filed as Gundam Mk-II via a weapon call-out match
(score 3.0), one of the common-weapon magnets already proven wrong twice
elsewhere in this project; wrong again here. No Gundam Mk-II or Zeta
Gundam/AEUG content anywhere in the section. The lines are Mobile Suit
Gundam UC: the speaker addresses "カークス少佐" (Major Kirks) as a
superior, ordering a retreat rather than issuing one (179 "With Kirks!",
184 "Kirks back!"), and separately worries about a teammate distracted by
"シャンブロ" (Shambro, 178). `source/library/pilots.json` (i=151/152)
identifies Yonem Kirks as the 39-year-old Major leading the Zeon remnant
army out of New Guinea (Zaku I sniper type), with Shambro as the mobile
armor of his subordinate Loni Garvey. The speaker is neither -- a
third, unnamed veteran under Kirks's command, most likely at the
Trinington Base raid: the lines are steeped in Zeon nostalgia (Sieg
Zeon, "Zeon can fight ten more years", "Zeon isn't dead yet"), an old
soldier's pride and grudge (old wounds at the sight of a Gundam,
dismissing a much younger enemy pilot as green), and contempt for the
Federation and its Gundams ("fake Gundam", "worse than the White
Devil", GM-lineage mockery) -- a One Year War veteran now scraping by
as a remnant fighter. No self-naming line exists, so the specific
character stays unresolved; recorded in `analysis/voice_identity.json`
as "84"/"85": unit null, pilot "Zeon remnant army grunt pilot (serving
under Major Yonem Kirks)". Section 85 is the same voice set (near-twin
per its own brief) and should reuse this section's English wherever the
Japanese matches. 187 of 187 distinct lines translated, `check_voice.py`
clean, no duplicate values. Budget forced heavy compression throughout --
entry 20 drops the exclamation mark to fit the "Sieg Zeon" chant into a
9-letter budget, entry 253's two-line 29-budget entry drops "as we
survived" nuance to fit "Like us\nGundam legend lives!", entry 97 drops
the "not by luck" clause to fit "We've survived\ntoo!", entry 203 drops
the explicit "White Devil" name to fit "Far from it!" (13-letter
budget), entry 254 keeps "Devil" but drops "White" to fit "Worse than
Devil!".

**Voice: section 204** -- filed as Burglarydog / Chirico Cuvie via a weapon
call-out match, score 3.0 (middling, the same class of match that was flatly
wrong for section 8). Verified correct this time: `source/library/robots.json`
confirms Burglarydog (バーグラリードッグ) is a genuine rough-terrain
Scopedog color variant used by the Melkia Regional Army (already shipped as
"Burglarydog" in `translation/library/rt_000.json`), and Chirico Cuvie
(キリコ・キュービィー) is `pilots.json`'s Votoms AT pilot. The section's own
content confirms it independently: entry 58 taunts a "クエント人"
(Quent-native mercenary), and `pilots.json`'s Chirico bio places his own
climactic confrontation with Wiseman in the ruins of Quent -- this is
Votoms lore, not a crossover coincidence. Entry 58 originally read "Cuento,
sold?" from a naive romanization before the project's existing spelling
("Quent," used in `translation/library/rt_000.json` and
`translation/stage0002_03.json`) was found and swapped in. 168 of 168
distinct lines translated, `check_voice.py` clean, no duplicate values.
Budget forced heavy compression throughout -- entry 246 drops the "I'm
retiring" clause to fit "Beaten by a suit?!", entry 54 drops "survivor" and
goes singular to fit "Black Knight" (12-letter budget), entry 26 compresses
"I'll finish you in melee" to "In melee!". Same pilot voices sections 205
and 206 per the brief; this translation is the source for propagating to
206 (near-identical twin) once merged.

**Voice: section 006** -- filed as Strike Freedom Gundam / Kira Yamato via a
common beam-rifle/vulcan weapon match (score 2.5); wrong. Same misfiled
family as section 8 (already recorded as a Firebug mercenary in a Full
Metal Panic-adjacent original faction), but a different pilot within it:
this is the squad's commanding leader, not the wisecracking pilot filed
under 8. The lines give orders to named subordinates Beck, Gates and Kan
Yu ("Sloppy Beck", "Weak, Gates", "Cleanup, Kan Yu"), call their own
machine the "Burglar" and insist it's "not just an Axio" (matching
`source/library/robots.json`'s Axio Burglar, i#252 -- the Firebug squad's
tuned Axio custom, PLTN blank, no single fixed pilot on record), taunt
Mithril as a rival force, and repeatedly mourn a dead "Princess"
commander -- `source/library/keywords.json`'s Firebug entry names her as
Marilyn Catt, who led Firebug and died at Mars, leaving the squad to
honor her memory while searching for a new Princess worthy of their
loyalty. No line self-names the speaker, so the pilot is left unresolved;
recorded in `analysis/voice_identity.json` as "6": unit Axio Burglar,
pilot null. Section 7 is the same voice set (near-identical twin per the
006 brief) and carries this same attribution and the same English lines.
220 of 220 lines translated, `check_voice.py` clean, no duplicate values.
Budget forced heavy compression throughout -- entry 5 drops "with fear"
to fit "Fear Firebug's name", entry 225 collapses "your life or death is
mine to decide" to bare "I decide!", entry 372 drops the explicit
Princess reference to fit "Rough lately", entry 392 keeps the line break
but trims to "Princess! I may soon\njoin!" to land the sign-off inside
budget.

**Voice: section 056** -- filed as Nu Gundam / Amuro Ray via Beam
Confuse/Fin Funnel/Funnel call-outs (weapon score 3.0); wrong. The content
is unmistakably Kamille Bidan piloting Zeta Gundam: he defends his own
name at 184/185 ("why's it bad that Kamille's a man's name -- I'm a
man!!", the canonical Zeta Gundam running gag only Kamille himself would
say about himself), addresses Fa Yuiry and Shin Matsunaga by name as a
fellow AEUG pilot (113, 116, 117, 120), reports to "Captain Quattro" as a
subordinate would (114, 118, 218, 403, 407 -- Kamille never learns Quattro
is Char in the TV series), calls his own machine "Zeta" throughout (43,
46, 56, 59, 62, 72, 138, 145), and speaks two of the character's signature
anime lines almost verbatim: 86 ("俺の身体をみんなに貸すぞ" -- "I'll lend my body
to everyone") and 89 ("生命は……生命は宇宙を支える力だって" -- "life is the power
that supports the universe"). Entries 426-432 are an epilogue chat with
Banagher explicitly naming "Super Robot Wars" itself. This also resolves
section 068's open speculation that 56 (with 87 and 131) might be "the
Colonel's [Char's] own voice set" because it addresses Quess Paraya by
name (377, 385): Kamille has his own canonical psychic link to Quess while
comatose in Char's Counterattack (noted in that same 068 entry), which
fits a worried, pleading tone toward her far better than Char commanding
his own subordinate -- treat that speculation as superseded for 56; 87 and
131 remain open. `robots.json`'s own Ζガンダム entry (pilot カミーユ・ビダン)
carries no funnel armament, so entries 16, 18, 20, 23, 26 and 29 (which
shout Funnel/Fin Funnel, Nu-Gundam-exclusive per `weapons.json`) don't fit
this unit's real loadout; they're translated per the weapon glossary
anyway (a mismatch on screen is worse unflagged) but are flagged as likely
misrouted pool strings. Entry 161's "Beam Confuse" is genuine -- Zeta
Gundam carries its own Beam Confuse in `weapons.json`, unrelated to the
misfiling. Recorded in `analysis/voice_identity.json` as "56": unit Zeta
Gundam, pilot Kamille Bidan. Not yet confirmed by a screenshot. 215 of 215
lines translated, `check_voice.py` clean, no duplicate values. Budget
forced heavy compression throughout -- most lines lost a clause or a name
to fit (e.g. entry 233 "A machine ruling people!" drops "such a thing",
entry 373 "Nahel Argama!" drops its verb to keep the glossary name whole,
entry 409 "Losing?\nProves them right!" drops the explicit "enhanced
human", entry 388 "Just widens\nthe rift more!" drops the explicit "Earth
and space" naming) -- flagged in the section brief's own report rather
than listed exhaustively here.

**Voice: section 189** -- filed as Gundam Mk-II / Kira Yamato via a beam-
rifle/vulcan common-weapon match (score 1.0); wrong, no SEED content
anywhere. The lines are an unnamed rank-and-file 親衛隊 (Personal Guard)
pilot of the Sleeves from Mobile Suit Gundam Unicorn: they invoke ガランシェール,
フロンタル大佐 and 総帥 (already glossed Garencieres/Frontal in the brief; 総帥
rendered "Commander" per this project's own `translation/voice_117.json`
precedent), and report to and take orders from アンジェロ大尉 (Captain Angelo,
also glossed) by name in support and defeat lines, separately deferring to
フロンタル大佐. `translation/library/pt_120.json` confirms 親衛隊 = "personal
guard" and that Angelo Sauper (19, Captain) is its commander and Frontal's
(43, Colonel) bodyguard. The speaker never names themself -- a mass-
production Geara Zulu pilot, same pattern as the Neo Zeon grunts at
117/118/119 but a distinct set (Frontal's/Angelo's Personal Guard, not the
generic Neo Zeon rank-and-file). They also taunt a "Red Comet" as having
lost his convictions (line 48) while claiming that title belongs to
Frontal instead (line 197) -- Full Frontal's rivalry with Char Aznable's
UC-era legacy, unrelated to Gundam SEED. Recorded in
`analysis/voice_identity.json` as "189" and "190" (190 is a near-identical
twin per the brief and ships the same English). 180 of 180 lines
translated, `check_voice.py` clean, no duplicate values. Budget forced
several lines to drop a name or nuance: entry 17 ("We're real!" drops
"just a name"), entry 22 ("On target!" for the loanword "target lock",
kept distinct from entry 21's "Lock on!"), entry 29/187 (drop explicit
"Gundam"), entry 168/309 (entry 168 drops Angelo's name to "sir" under a
13-letter budget; 309 keeps it), entry 190 ("Londo Bell?!" drops "is that
all"), entry 242 ("Insulted!\nUnforgivable!" drops the "insult to me is
insult to the Colonel" equivalence), entry 248 ("Bell got me!" for the
ambiguous 鈴の音, unclear referent), and entry 263 ("Toyed by them?!" drops
explicit "civilians").

**Voice: section 068** -- filed as Nu Gundam / Amuro Ray via Fin
Funnel/Beam Confuse call-outs (weapon score 5.0); wrong. The speaker uses
feminine casual first-person (あたし), is devoted to a "大佐" (Colonel)
she'd die for, names her OWN unit "α" (Alpha) twice ("αで大佐を守るんだから",
"αでみんなを守るんだから"), wants to drive out Nanai and Lalah as rivals for
the Colonel's affection, treats Gyunei as a fellow ally, is hostile-yet-
admiring toward Amuro, has "many people's minds" pushing into her, and her
defeat lines invoke Hathaway. That is Quess Paraya, pilot of the Alpha
Azieru (Char's Counterattack) -- a jealous Newtype devoted to Char,
telepathically linked to the comatose Kamille, friend of Hathaway Noa. The
weapon match hit because this game voices Alpha Azieru's funnels with Nu
Gundam's own call-out strings (Fin Funnel/Beam Confuse). Recorded in
`analysis/voice_identity.json` as "68": unit Alpha Azieru, pilot Quess
Paraya. Cross-evidence, not yet independently translated: sections 56, 87
and 131 (also filed under Nu Gundam by the same weapon magnet) contain
lines addressing "クェス"/"クェス・パラヤ" (Quess/Quess Paraya) BY NAME as a
subordinate -- e.g. 056:377 "敵意に呑まれるな、クェス", 087:309 "クェス、いい子だ",
131:290 "まだまだだな、クェス・パラヤ" -- consistent with those being the Colonel's
(Char's) own voice set, not Quess's; flagged for a follow-up section but
not resolved here. 229 of 230 lines translated, `check_voice.py` clean.
Entry 211's weapon call-out "Beam Confuse" (12 letters) does not fit its
11-letter budget even bare -- no abbreviation of a glossary weapon name was
attempted, so the entry was omitted and ships as the original Japanese.
A number of lines lost secondary detail to budget, e.g. entry 3 ("Earth
spawned you --\nit must burn!!" drops "or we won't be saved"), entry 45
("Must stop you!!" drops "or the Colonel--"), entry 104/105 (drop the "α"
unit name they use in Japanese), entry 174 ("Without her,\nI'd be his."
drops Amuro's name, replaced with a pronoun), entry 293 ("Following!" drops
"Unicorn"), and entry 327 ("Thanks, Funnels" drops "Fin" from the weapon
name to fit).

**Voice: section 021** -- filed as Strike Freedom Gundam / Kira Yamato, a
common beam-rifle/missile/volley-fire weapon match (score 2.0); wrong, and
no Kira or SEED content anywhere in the section. The lines are rank-and-file
Altair soldiers (Aquarion EVOL's Neo-DEM empire) addressing their own
superiors Kagura, Izumo and Jin with honorifics (already glossed in this
project as Kagura Demuri, Izumo Kamurogi, Jin Muso, `translation/library/
pt_360.json`), hunting a "Rare Iglar" (also already glossed there) toward
a "true Eve" to break "Eve's curse", calling their war machines "Gunis"
(Misra/Radius/Afra Gunis in pt_360.json), Earth's hero side "Vega", and
taunting an opposing "Mechanical Angel" (i.e. Aquarion) and a "Super
Robot" -- Altair is the enemy faction here, not the Gundam side. Source
kana アルテア for the nation matches this project's own prior "Altair"
rendering (`source/library/pilots.json`'s アルテアの星の力 -> pt_360.json's
"Altair's energy"). No pilot self-identifies -- a mass-production grunt
set, same pattern as the Neo Zeon grunts at 117-119. Recorded in
`analysis/voice_identity.json` as "21"/"23"/"25": pilot "Altair grunt
pilots (Neo-DEM)", unit null; sections 23 and 25 are the same voice set
per the brief and should ship these same 170 lines. 170 of 170 lines
translated, `check_voice.py` clean. The weapon glossary term "Wings of
the Sun" (16 letters) didn't fit its 14-letter budget at entry 198 --
shipped as "Wings of Sun?!" (dropped "the"); "Volley Fire" (11 letters)
didn't fit its 10-letter budget at entry 69 -- shipped as "Volley!".
Entry 247's budget forced "Rare Iglar" down to bare "Iglar". A handful of
others lost secondary detail to budget: "I'll end it!" (23, drops
"legend"), "Fully read!" (192, drops "completely"), "So Vega's\nSuper
Robot?" (36, drops the "boastful/proud" nuance), "Need backup now!" (233,
drops "enemy stronger than expected").

**Voice: section 061** -- Space King Kittan, pilot Kittan Bachika. Filed as
a weapon-name match with a middling score (4.0), flagged for a content
check against the section 8 mismatch (Strike Freedom / Kira Yamato,
actually a Full Metal Panic mercenary). Here the attribution holds: the
lines are unmistakably Kittan's Gurren Lagann register -- Gurren, Yoko,
Simon, "King Kittan", Giga Drill Break, the Dai-Gurren Brigade -- so no
correction was filed to `analysis/voice_identity.json`. 102 of 102 lines
translated, `check_voice.py` clean. Budgets were tight throughout (several
4-13 letter slots); a handful of lines shipped with the closing
exclamation mark dropped to fit ("Just a scratch", "Not my style, ok",
"No range limits now") per the project's own priority (drop the mark
before the word), and a few compressed hard enough to lose secondary
detail: "Kittan finds one!" (loses "fights", 35), "Can't fail my bro!"
(informal shorthand for "older brother", 84), "Lose here,\nGunmen's
done!!" (loses the "no place to stand" idiom, 88), and "Upgraded,\nKing
Kittan!" / "King Kittan,\nfull power!" (both drop "Space" from "Space
King Kittan", 117-118).

**Voice: section 048** — filed as Burglarydog / Chirico Cuvie (VOTOMS,
weapon match 5.0), but the content is not Chirico: the register is a
theatrical, sadistic taunter, not VOTOMS' famously terse protagonist. Lines
use the Lambda Driver, taunt the crossover roster by name (Mithril, an
"ex-Red Shoulder", a "Newtype", EVA, Gundam, the Black Knights, and the KPSA
leader Ali Al-Saachez by his fallen underlings), address two subordinates
by name (Wang Fang, Wang Lan), and repeatedly call an opponent "Kashim"
with romantic-coded intensity ("I love you, Kashim", calls him honey,
begs him to "come back" mid-fight) -- Kashim is Gauron's private nickname
for a young Sousuke Sagara from his guerrilla days, confirmed against
Full Metal Panic sources. Same family as sections 8, 17, 18 and 19
(already-corrected Gauron/FMP mercenary lines misfiled onto common-weapon
Gundam/Strike units); recorded in `analysis/voice_identity.json` as
"48": pilot Gauron (probable). 169 of 169 lines translated,
`check_voice.py` clean. Budgets were brutal on the Wang Fang/Wang Lan
callouts specifically: two slots (7 letters) couldn't fit "Wang Fang"/
"Wang Lan" at all and shipped as "W. Fang"/"W. Lan" with the verb dropped,
one slot (8 letters) shipped the bare name "Wang Lan" with no verb, and
several Kashim lines dropped his epithet ("murder-saint") or the address
itself where the name alone ate the budget -- see the merge report for the
full list.

**Voice: section 208** — filed as Big O / Roger Smith; the lines are
Setsuna F. Seiei in the 00 Qan[T] (GN Bits/Field/Drive, Trans-Am,
Celestial Being, and a fourth-wall SRW Z3 finale speech). 192 lines in
his terse register; recorded in analysis/voice_identity.json. "Trans-Am"
at 9 letters misses 6-8 letter budgets -- Trans!/TransAm variants ship.

**Voice: section 9** — filed as Gundam Mk-II; the lines are Aquarion
EVOL's MIX (Andy addresses her by name; his hole-filler-girl nickname;
Moonlight Requiem with Shrade, Crucifixion Sword with Cayenne). 279
lines in her register; the single "Gundam" line is a taunt at an enemy
unit -- probably what fooled the weapon matcher. Recorded in
analysis/voice_identity.json.

**Voice: section 81** — Macross Quarter (Jeffrey Wilder), 170 lines,
attribution genuine: S.M.S., Vajra, Bobby, Skull and Pixie squadrons,
Pinpoint Barrier, Macross Attack. "Macross Cannon" at 14 letters misses
a 13-letter budget by one -- ships as "Cannon, fire!".

**Voice: section 086** — Gurren Lagann (Simon), 415 lines. The weapon-match
attribution (score 4.5) held up: content confirms Simon, with Viral as a
recurring co-pilot/ally address (status checks, a defeat apology, combo
finishers) and Nia, Kittan, Yoko, Gimmy, Darry, Dayakka/Kiyoh, Adiane,
Lordgenome named throughout. A chunk of the section (entries ~220-227) is
not battle dialogue at all — it's the game's own title-screen/attract-mode
narration ("Super Robot Wars Z3", a thanks-for-playing line, a check-in
with Attenborough) riding the same voice slot; translated as such rather
than forced into bark register. Heavy crossover block against Evangelion
(Shinji/Rei/Asuka, no gender inferred beyond canon pronouns already
established), Zeta's Quattro, and unnamed "space beast" opponents.
Weapon/glossary names shipped verbatim where budget allowed (Giga Drill
Break, Gurren Boomerang, Probability Shift Shell, Black Hole, Anti-Spiral,
Tengen Toppa); several call-outs had budgets too tight for the full shipped
name and were abbreviated (Boomerang!, Shell fire!, Anchor!, G-Drill!) or
dropped the qualifier (Tengen Toppa without Gurren Lagann, Break all!
losing Tengen Toppa entirely at a 10-letter budget) — flagged inline where
it happened. `check_voice.py` also caught several near-identical shouts
(Giga!/Drill! variants, Leave it!/Us too!) that needed differentiating once
punctuation made their source lines distinct.

**Voice: section 197** — Shin Getter 2, 186 lines: the Getter team's
shared set (Ryoma, Hayato, Benkei calling each other by name, plus the
Koji / Kittan / Gimmy / Darry crossover banter block). The translator
also caught a seeding hazard the checker enforces: two different drill
shouts pre-filled with one English line, differentiated on the spot
(Drill Hurricane / Hurricaaaaane!).

**Voice: section 77** — Cosmo Crusher, 112 lines. The weak weapon match
(6.0) proved RIGHT this time: God Mars's Crusher Team, confirmed against
the game's own PLTN record. The whole ensemble speaks — Kenji, Naoto,
Akira, Mika, Roze, Mars, Commander Otsuka — each kept in register; the
looser トリプル攻撃 phrasing uses the shipped "Triple Laser" so bark and
on-screen weapon label agree.

**Voice: section 174** — Dancouga Nova Max God (Aoi Hidaka), 379 lines,
the largest single section and the one that killed an earlier run on the
output limit; batch-writing held. Attack calls rendered syllable-faithful
under 4-6 letter budgets (断空剣→Ken!, 断空斬→Zan!, 彈劾剣→Dangai);
the spirit-chant line names the shipped commands (Strike, Valor...).
Missile Detonator abbreviates to M.Detonator where 18 letters cannot fit.

**Voice: sections 82, 83, 20** — 747 more lines. Section 82's "Strike
Freedom / Kira" attribution was false: an unnamed Geminis rank-and-file
Diosc pilot (Major Annalotta and the Captain as superiors, the mourned
homeworld Geminai) — recorded in analysis/voice_identity.json; new terms
Geminai and Psy-Control. Section 83 proved a 98% twin of 82: seeded
253/257 from 82's answers, four lines translated by hand, one seeded
duplicate differentiated. Section 20 is genuinely Amuro's Nu Gundam
(self-ID line), 233 lines. The Nu-labeled twins 68/56/87/131 share
almost nothing with 20 — more weapon-magnet artifacts, to be identified
from content when their turn comes.

**Voice: sections 65, 170, 57** — 550 more lines in place (Chirico's
Burglary Dog; Lockon's Zabanya with Haro's register kept mechanical; and
section 57, which the weapon match filed as Sousuke's M9 but whose lines
are unmistakably Gamlin Kizaki's VF-17D — Diamond Force, Kinryu and
Physica, Mylene, Basara — recorded in analysis/voice_identity.json).
House fixes on merge: Urzu 7 callsign spelling, Physica (Macross 7
canon). A propagation map of the remaining corpus (work/voice, scratch
tooling) found 3,949 redundant copies across 2,529 repeated lines, so
future batches pre-seed answer files from every line translated so far
and twin sections ship without retranslation.

**Voice translation opened up to the whole file, and wired into the build**
— the voice pipeline was Genion-only in a literal sense: `voice_section.py`
carried that section's POOL/INDEX/COUNT as module constants, so no other
unit could be written at all. Geometry now comes per section from
`work/voice/sections.json` (the same table `extract.py` derives from
`srvc_link.sections()`) and is re-proven before every write —
`voice_lib.prove` refuses a base whose index words do not all land on real
string starts inside that section's own pool. New `tools/voice_lib.py`
holds the geometry, the in-place write and a verify that shares no
assumption with the writer (size unchanged, no byte outside a chosen slot,
no index word moved anywhere in the file). `voice_section.py` is now a thin
CLI over it and takes any number of documents; its output on the shipped
Genion doc is byte-identical to the old writer's, which is how the
generalization was checked.

`build_project.py` applies every `translation/voice_*.json` itself, after
the atlas step, and collects those lines' letters into the pooled mapping
so they get cells. This closes the regression that cost four days: the
English no longer depends on anyone remembering to run a side script, and
a build that omits it cannot happen. Verified: the build's SRVC.BIN is
byte-identical (`c277a89d`) to the manually written file already proven
in-game. The dead append-era channel (`translation/voice/`, `srvc.build`)
is gone from the build path.

New per-section tooling, mirroring the stage-dialogue pipeline:
`tools/export_voice.py` writes a self-contained brief (identity with its
weapon-match confidence, the shipped English for every weapon the section's
call-outs name, the glossary terms that actually occur, and every distinct
line with its budget); `tools/check_voice.py` validates an answer offline —
budget in cells, the drawable character set, leftover Japanese, stray
quote brackets, coverage; `tools/merge_voice.py` publishes
`translation/voice_NNN.json` and refuses to write anything that does not
check clean. Only distinct lines are briefed: 50,919 index entries address
31,670 distinct strings, and a repeat is served by the string it points at.

`tools/voice_status.py` answers "what is done, what is worth doing next"
from the files themselves — 31,670 lines across 211 sections is a
many-session job, and a stale list of targets is how sections get
translated twice or skipped. It ranks what is left by weapon-match
confidence first, then size.

Two corrections to what the handoff claimed. A `
` line break costs **one**
cell, not two — it is two characters but two bytes, the same as one letter —
so budgets were being counted too tightly. And the silence sentinel is not
only `－－－…`: 17 sections carry `無音（本番では表示しません）` lines that
never reach the screen either; both are now excluded from briefs.
`translation/voice_genion.json` is renamed `translation/voice_134.json` so
every section follows one naming rule — with the old name, merging section
134 would have written a second document for the same section.

**Voice translation, first sections** — **185 ARX-7 Arbalest** (363 lines,
Sousuke Sagara) and **184 Mazinger Z** (321 lines, Kouji Kabuto) ship,
taking the voice track from 126 to 810 of 31,670 lines. Both check clean:
every line inside its slot, every `
` break in the position the Japanese
put it. Sousuke stays clipped report-speak and Al keeps his dry register
(both matched against the shipped stage dialogue rather than invented);
Kouji shouts, with the call-outs taking the shipped weapon names verbatim
where the budget holds them (Breast Fire, Rust Hurricane, Photon Beam) and
falling back to the shouted half where it does not (`Rocket!` at 9 cells,
the full `Rocket Punch!` surviving in the 14-cell slots next to it).

Two spellings the corpus does not agree on, surfaced by translators and
left for a name-script pass rather than settled line by line: `Urzu` (stage
dialogue) vs `Uruz` (library pilot entry) for Sousuke's callsign, and
`Mechanical Beast` (stage dialogue, 16 cells — impossible in a bark) vs
`Mechabeast` (shipped in the Genion set) for 機械獣.

Six agents were launched first and all six died at their first tool call on
the account session limit, losing nothing but time — answers are written
only at the end of a run. Batches are three from here.

**207 Shin Getter 1** (349 lines, Ryouma Nagare) ships too, taking the
track to 1,159 of 31,670. Its translator was killed by the session limit
after writing the answer but before its own check pass, which left four
lines one cell over budget; they were closed on review rather than by
re-running the agent (`Invaders!/Kill them!`, `We're breaking up!`,
`Toying with us?`, and サシで as `One-on-one`, exactly 10 cells).

The first multi-section build failed, and correctly: the atlas collection
step asked for a cell for the backslash of a `
` break, because it fed
the raw English to the pair collector while the encoder splits on the
break first. Genion never tripped it -- none of its English carries a
break. Fixed by splitting the same way in both places. This is the class
of bug the build wiring exists to catch: it fails loudly at build time
instead of drawing a backslash on screen.

**115 Burglarydog** (123 lines, Chirico Cuvie -- the strongest weapon-match
in the file at 24.0) and **193 Dai-Guard** (405 lines, Akagi and the crew)
ship, taking the track to 1,687 of 31,670 in 6 sections. Verified by build:
all six written in place, SRVC.BIN size unchanged.

**`check_voice.py` now rejects two different Japanese lines that ship the
same English.** 193 came back with four lines reading `Locked!`, two of
which actually said "parts secured" -- that is a meaning error, not a
nuance, and the player hears barks back to back. It happens when a long
glossary name eats the budget and only punctuation is left to vary; the fix
is to let one line carry the name and the others carry their meaning
(115's three `Red Shoulder!` lines became `Die!`, `There you are` and
`Red Shoulder!!`). The check ignores differences that are only elongation
or punctuation, so genuine repeated grunts (「ハァァ！」 vs 「ハァ…！」) still
pass. It found three collapses in already-shipped sets, including one in
the proven Genion set (32 and 135 both read `Finish it!`; 135 is now
`Finish!!`), and every section is clean under it.

**173 Trider G7** (305 lines, Watta Takeo) and **133 Genion GAI** (467 of
468, the protagonist's upgraded machine) ship, taking the track to 2,459 of
31,670 in 8 sections. Build verified: all eight in place, size unchanged.

173's translator was killed after writing its answer but before its check
pass, and the collapse rule earned its keep on what it left: seven distinct
Japanese lines shipping four English strings, one of which was a plain
mistranslation -- 「よくもやりやがったな」 ("how dare you") and 「悪者の大将め」
("boss of the crooks") had both become "You're the boss! Pay up!". Closed on
review along with one over-budget line.

133 was translated in-session rather than by an agent, because the model
limit had been reached and Genion GAI is the one section where voice
continuity with an already-shipped set (134, the base Genion, same pilot)
matters most. One line ships Japanese: entry 513 「遅い！」 has a 3-cell slot
and "Slow" is four. Names not in the glossary and flagged for it: ジェミニス
as Geminis, ビルレスト as Bilrest, Ｄ・フォルト as D-Fault, and ナイト as
Knight -- that last one is the alternate protagonist name the co-pilot uses
in parallel barks, so it appears on screen and wants confirming.
ニーベルング・アナイレーション cannot fit any of its slots (21 cells against
17), so those lines carry `Nibelung` alone.

**128 Unicorn Gundam** (242 of 243, Banagher Links) and **191 Tetsujin
No. 28** (223, Shotaro Kaneda) follow, both translated in-session while the
model limit held: 2,924 of 31,670 lines in 10 sections, build verified in
place with the file size unchanged. Banagher keeps the polite, arguing
register the show gives him rather than a fighter's; Shotaro's lines are
mostly ORDERS to a machine he steers by remote, not first-person combat
lines, which is a distinction the budgets happen to favour ("Go on!",
"Hold it!", "Pin it down!"). Two entries ship Japanese because no English
fits: 128's 337 「バナージ」 (4 cells, the name is 8) and 133's 513.
Names not in the glossary, flagged: ロニ as Loni, 魔人将軍 as General,
アイアンファイター as Iron Fighter, 敷島博士 abbreviated to Dr S at 36 cells.

**105 Godmars** (169 lines, Takeru Myojin) and **008** (225 lines) as well:
3,318 of 31,670 in 12 sections, past 10%.

**A wrong attribution, caught by reading the lines.** `sections.json` gives
section 8 to Strike Freedom Gundam / Kira Yamato on an srvc_link score of
7.5, and the content refutes it outright: the speaker is a wisecracking
mercenary who names Firebug, Burglar, Axio, Beck, Gates, Kang Yu, Mithril,
Bonta-kun, Tessa and Kumen -- a Full Metal Panic villain, nothing to do with
SEED. Translated to the content and the doc's `unit` cleared to null with the
evidence recorded in its note, rather than shipping Kira's register on
someone else's lines. This is why the brief prints the confidence score
instead of asserting the identity: a mid score is a suggestion, and the
lines themselves outrank it. Naming the unit still needs a screenshot.
`export_voice.py` now prints that warning in every brief whose score is
under 9 -- 126 of the 199 sections still to do -- and `docs/VOICE_HANDOFF.md`
carries the rule.

**141** (139 lines) is the SECOND proven misattribution, and it exposes a
pattern: it is also filed under Strike Freedom Gundam / Kira Yamato (score
6.33), and its lines are Branch robot-mafia goons from Tetsujin No. 28 --
Branch Robo, Black Ox, Shotaro Kaneda, "Otsuka's men". Counting the
attributions afterwards explains why: **Gundam Mk-II (25 sections), Strike
Freedom (15) and Nu Gundam (10) hold 50 of the 141 attributed sections
between them**, because a beam rifle or a vulcan is carried by dozens of
machines and srvc_link matches the name. Those three are weapon-name
magnets, not identifications. `export_voice.py` now prints DO NOT TRUST on
every one of those briefs (48 of the sections still to do) and tells the
translator to work the speaker out from the lines instead.

Sampling the magnet group settled what those sections actually are:
**009 is MIX and 164 is Yunoha Thrul, both Aquarion EVOL** -- each pilot
calls out her own name -- and neither has anything to do with a Gundam
Mk-II. Corrections now live in `analysis/voice_identity.json`, which
`export_voice.py` and `merge_voice.py` both prefer over the weapon match,
so a section read once stays read: the brief opens with the corrected
identity and the published doc carries it with the evidence.

**210 Shin Getter Dragon** (226 lines) ships from that batch. Its
translator identified the three pilots itself from the library's NAMES
table (Gou taciturn, Kei impulsive, Gai gentle) and assigned voice per
line. Flagged as judgment calls, not verified terms: 連獄 as `Purgatory`
(read as a pun on 煉獄) and ゲッターエレキ as `Elek`. 冥府の王 came back as
`Face me!`; changed on review to `Hades!`, which fits the 9-cell slot and
matches the name 207 already ships.

**A third of the identity problem, and 4,115 lines, come from repeats.**
Sections **17, 18 and 19 are the same voice set stored three times** -- 197
of 198 lines byte-identical -- and 18's translator worked out what everyone
before it had missed: the set is not Sousuke Sagara at all. The register is
rough imperative (食らいな, くたばりな), the lines taunt a crossover roster
and address Gates and Fe as subordinates, and the Lambda Driver is shared by
Arbalest and Gauron's Venom, which is exactly what made the weapon match
land on Arbalest. It is Gauron or a mercenary commander. That is the third
proven misattribution, and the first found by a translator rather than by
me.

Counting the repeats across the whole file: **20 groups of sections hold the
same set two or three times over, covering 4,115 of the 31,670 lines** --
13% of the job. `work/voice/clusters.json` had recorded those groups all
along and nothing used them. New `tools/voice_propagate.py` carries a
translated section's English to its siblings, matching lines by their
Japanese rather than by entry number (the numbering differs between sections
of a group, the strings do not), and leaves anything unmatched for a
translator. Translating a repeat again would not merely waste the work: it
would put the same unit on screen saying the same Japanese two different
ways.

Shipped through it: **17**, **18**, **19** (198 each) and **142** (138, all
but one carried from 141), plus **169 Big O** (301, Roger Smith) — 4,843 of
31,670 in 20 sections, build verified in place with the file size unchanged.

Propagation earned its keep immediately on 17. Its translator had already
written a full answer before the correction reached it, and that answer
differs from 18's on **133 of 197 identical lines** — flat and military
("Fire!", "Mark. Fire!", "Just business") where 18's is a mercenary's
("Eat!", "Croak!", "All business!"). Same Japanese, same unit, two
incompatible voices: exactly the failure the propagation rule exists to
prevent. 17's answer was discarded and the set carried across from 18
instead, and 食らいな went from `Take!` (a bare verb no one says) to `Eat!`
in all three copies.

**155, 156 and 157 ship the same way — 618 lines for the price of 206.**
This set had no weapon match at all, and the lines name themselves: a
**Mycenae god-general** out of the Mazinger mythos, invoking Mycenae and
Lord Hades, reviling Zeus as a traitor, swinging a hell scythe, and taunting
Getter Rays, Gundam, the Black History and the ages of Fire, Beast, Water,
Wind and Sun. Haughty and archaic — the first enemy voice in this track that
is neither a grunt nor a mercenary. **6,350 of 31,670 in 27 sections, past a
fifth of the whole track**, build verified.

**117, 118 and 119 ship from one translation — 738 lines for the price of
250.** The set is another Gundam Mk-II magnet victim, and it is not a named
pilot at all: they are generic **Neo Zeon grunts**, invoking Neo Zeon, Axis
and Spacenoid grievance, addressing a Colonel, Captain, Lieutenant and
Ensign, and abusing Amuro, the White Devil, the Red Comet, Londo Bell,
Celestial Being and the Black Knights from the outside. A mass-production
enemy voice set. Translating it once and propagating took the track from
15.8% to **18.1%, 5,732 of 31,670 in 24 sections**, build verified.

That is the pattern the remaining work should follow: the biggest wins left
are the sections that repeat, and a grunt set has no register to get wrong
beyond keeping it terse and hostile.

**140 Black Ox** (151 lines) closes the batch: 89 lines carried from 191,
the other 62 translated here. They are all commands to Black Ox by name and
one invokes Dr Franken, its builder -- the same remote-commander voice as
191, recorded in the identity file. 4,994 of 31,670 in 21 sections.

Section **174 died a new way**: its translator tried to emit all 379 lines
in one tool call and blew the model's 64,000-token output limit, losing
everything. Every brief now says to write the answer in batches of about
100 and to add each batch to what is already on disk -- naming both failures
(the rate-limit kill and this one) so the reason is concrete. A file on
disk survives; a draft in an agent's head does not.

169's translator was killed by the limit after drafting all 301 lines but
before its own check pass, and it had written **137 real newline characters**
where the game wants the literal two-character backslash-n. The checker
caught every one as an undrawable character; converting them was mechanical,
and the twelve genuine budget overruns behind them were then one cell each.

**014 Asclepus** (127 lines) too: 3,445 of 31,670 in 13 sections. The
speaker names himself in his own sign-off line -- Advent, action-squad
leader of Chrono, the ally whose opening Hibiki thanks in 133 -- so the
section gets a pilot that `pilots.json` did not have, recorded in the doc's
note. Formal, dignified register throughout, which is a different voice
problem from the shouting pilots: the budgets fight economy of phrase
harder than they fight volume. マーズフラッシュ is 10 cells against a 9-cell slot in its bare
call-out, so those two lines carry `Flash!` and the full `Maars! Flash!`
survives in the 13-cell one -- the same compromise Mazinger's Rocket Punch
needed.

**Voice patch restored, and a handoff for the rest** — the Genion voice
set silently regressed: `tools/voice_section.py` runs outside the build,
`build_project.py` regenerates `work/out/SRVC.BIN` pristine every run,
and the stages 3-10 rebuilds shipped without re-running it (caught only
by hashing every copy — all five identical to pristine). Re-applied and
deployed: 126 lines in place, file size unchanged. `docs/VOICE_HANDOFF.md`
now carries the whole voice pipeline for the next agent — the in-place
law and the two failures that bought it, the section model and proven-base
checklist, the Genion recipe, and the wiring gap as the first task.
This entry also corrects the 0.4.0 voice note (previous session): the
"decode the header" blocker it described was superseded the same night
by the pool-bounded discovery and the in-place rewrite, and it swapped
the parser numberings (Genion is 134 in the current one).

**Operation End, intermission, and chapter titles** — the objectives
screen's condition lines proved hook-swappable in a probe (the headers
did not: 勝利条件/敗北条件/ＳＲポイント獲得条件 exist nowhere as drawable
text and are textures — future atlas work). All 22 distinct
`OPERATE_TBL.str_tbl` condition strings across stages 1-10 now carry hook
entries in bare and １．/２．/３． numbered forms, so every win / lose /
SR-point line through stage 10 draws in English. Chapter titles for
stages 2-10 are translated (Here Comes the New Problem Boy, Backs
Entrusted, Academy Defense Force, An Unknown Threat, Creeping Malice,
Shadows of War, New Dark Clouds, The Trap Is Set, Fighting Boy Meets
Girl) in bare, 『…』, and 第Ｎ話『…』 forms — the intermission
clear-record bar already showed "A Hope Called Taboo" from the probe.
The intermission screen is translated: all menu buttons (チーム編成 and
Ｄトレーダー are typeset in pieces and needed joined entries, like the
ace-bonus heading), the rotating help line for every button, the team-
organization submenu labels and messages, and the ＳＲポイント．/
Ｚチップ． counters (joined) with 資金． (exact). 183 hook entries added
(283 total; 664 strings in the hook table, 0 undrawable after swapping
ASCII -> and * for drawable → and ※). On-screen check trimmed the fits:
機体・武器改造 is "Upgrades" (the full phrase collided with Options),
the NEXT panel is Deploy/Ships (Deploy Select overlapped the counters),
and the Teams:/Ships: counter labels joined the set. チーム編成 typesets
with a space between its pieces, so space-variant joined entries were
added. The インターミッション header ignored an exact hook entry — a
texture or a second drawer, left with the objective-screen headers.

**Fixed: stage-1 mob one-shotting the Genion for 108,012 damage** — a
player replay caught the ??? enemy (Daimon, a weak AI mob) doing six-digit
damage in the English build; the pristine Japanese dump played the same
fight normally. Bisection with the original EBOOT proved the executable
innocent; the corpse was in `RPW_DATA`. `weapons.json` maps `"-"` to
itself, so the placeholder string at body offset **0** was "translated",
could not fit in place (2 encoded bytes over 1), and was appended -- and
`build_grown` then rewrote every pointer-column word holding `0` to the
new offset 0x18b6f (101,231). But `0` in those arrays is also how records
spell NULL/no-value: 1,400 semantic zeros moved, and whatever reads such
a word as a number exploded. The comparative verifier could not see it --
offset 0 resolves to a valid string before and after. Fix: `build_grown`
never repoints a zero word (`if v and v in repoint`). Rebuilt, re-verified
(zero zeros repointed; all name columns still resolve 100%; 5,388 weapon
slots English), redeployed.

**Stages 6-10 translated** — 2,320 records across 13 members: stages 6,
7A, 7B (the route split), 8, 9, and 10 (whose script spans three members,
including a one-line title card). Translated from 22 ranged briefs by six
concurrent subagents, merged by sha, style-normalised on merge. Terms
coined this batch, now precedent: Hanka Autonomous Region (ハンカ自治州,
converged on independently by two translators), Kashim (Gauron's name for
Sousuke, FMP canon spelling), 'Untouchable' (触れ得ざる者, single quotes,
bare), Anaheim Tech, "military nut". The 月夜 bare tag is "Moonlit Night"
(a mood caption like Blue Sky, verified in review). Kalinin's formal lines
carry the full "Hanka Autonomous Region"; bare "Hanka" stays for casual
speech.

**Stages 6-10 proofread** — eleven reviewer subagents, every record read
against the Japanese, 44 findings applied: two meaning errors (Emma's
Neo Zeon line argued *from* the Enhanced-Human unit, not despite it; the
drug Kaname was given was *called* a supplement — the deception was
dropped), idiom fixes (話せるね "you really get it", プレッシャー
"pressure" not "presence", 悲しいやら情けないやら), four ALL-CAPS AG
lines recased to his normal register, four `Speaker（thought` lines
missing the structural line break, a （） thought wrongly suggested as
「」 by a reviewer (caught on apply — the source decides the brackets),
rank and term unifications (vocative "Colonel" for Daguza, Captain
Testarossa, Master Sergeant Mao, Academy Defense Force, Takeo General
Company, Director for 専務, two more Uruz->Urzu typos), a 気合/spirit
seam at the Lambda Driver climax, Chirico's 不死身の男 epithet unified to
"the immortal man", and overlong lines rewrapped under the 55-char cap.
The consistency script then ran over all 19 stage files (318 changes:
terminal periods, the D-Trader family, trash duty, and the fullwidth （）
rule applied retroactively to stages 3-5); a CJK-leftover scan found
nothing untranslated. `skills.json` 強化人間 renamed "Cyber-Newtype" ->
"Enhanced Human" to match the library's unanimous usage. Everything
tokenised (`$$…$$`), all 19 members re-verify at 0 problems with tokens
expanded, rebuilt and deployed for on-screen check.

**`deploy.py --clear-install`** — clears `dev_hdd0/game/BLJS10256_DATA`
without deploying anything. The installed copy only matches whichever disc
it was installed from, so switching between the patched dump and the
pristine Japanese dump (`E:/SRWZ3/Dai-3-Ji … (Japan)/`) needs this before
booting the other version — otherwise the game answers
「ゲームデータが壊れています」, which is the install-cache trap, not a bad
patch. (Prompted by exactly that error when booting the Japanese copy.)

**Pipeline for the batch** — `extract.py` now lists STG0001A-STG0010 and
fixes the unsdat argv bug; `deploy.py` LAYOUT covers the stage 6-10
SDATs; `manifest.py` builds all thirteen new members. SDAT decryption
moved off `rpcs3 --decrypt` (broken by the 2026-08-31 auto-update, see
HANDOFF trap 6) to `make_npdata -d <in> <out> 0`, validated
byte-identical against the old oracle.

**Stages 3-5 proofread** — six reviewer subagents (one per member, reading
every record against the Japanese) plus a scripted cross-member scan, per
BASE_RULES: agent fixes applied first, the consistency script after. 106
findings, 113 records corrected: 4 meaning errors (a reversed う、うん,
a wrong name in a reunion line, a your/my flip in reported speech, an
untranslated caption), 16 gendered pronouns on $n scrubbed (the biggest
cluster around $n's teleport scenes -- including one where the Japanese
itself says 彼 and the neutrality rule overrides it), a register slip, a
callsign typo (Uruz 2 -> Urzu 2), and 66 missing terminal periods in one
member. The script pass then unified to shipped conventions: untranslated
banners and Branch Member speakers, ??? in ASCII, the D-Trader family,
Academy Defense Force, Photon Power (the library's 7:3 majority), Miss
(not Ms.) Suzune/Kagurazaka/Saijou, banner spacing ～ Text ～, and
restored Bonta-kun (a glossary-official name my honorific strip had
wrongly shortened). Finally tools/tokenise.py rewrote every literal
glossary name to a $$…$$ reference (round-trip byte-identical), so future
renames propagate; all six members re-verify at 0 problems with tokens
expanded the way the build expands them. (Correction, found in the
stages 6-10 pass: the terminal-period rule double-punctuated a
quote-final line — "'Snoopers.'." in stage 5 — now fixed, and the rule
skips quotes that already carry punctuation.)

**Translation doctrine into the brief generator** — `BASE_RULES.md` (the
project owner's accumulated translation rules) is now in the repo, and
`export_stage.py` bakes its per-line rules into every brief: never infer
gender (a name is not evidence; unknown referents get they/them; `$n`/`$l`
always neutral), compress or abbreviate before ever cutting a sentence's
end and FLAG what still cannot fit, keep every control code and leave
width slack for `$n`'s runtime expansion (~10 letters). Ranged briefs now
carry the eight records on either side of the slice as do-not-translate
context, and a Reporting section asks for records-examined vs
records-in-slice plus flagged shas. Stages 3-5 were translated before
this landed: sliced (115-140 records), sha-merged and check_stage-clean,
but without the context block -- the rules are for every brief from here.

**xdelta patch sets per release** — `tools/release_patch.py <version>`
writes `releases/<version>_xdelta/` (gitignored, like the snapshots):
`from-original/` applies to a clean dump and reproduces the release;
`from-previous/` diffs against the prior snapshot, so each patch's
existence and size is the per-file record of what that version changed
(0.4.2 over 0.4.1: EBOOT 6 KB, TPACK 2.4 KB, RPW 19 KB). Every patch is
decode-verified against the snapshot before it is kept. Built for 0.4.0,
0.4.1 and 0.4.2. Caveat: SDAT patches are always near full size -- the
per-run encryption key (HANDOFF trap 5) makes re-encrypted output
incompressible as a delta even when the script barely changed; read the
CPK-level manifests for the real change there. The xdelta3 binary lives in
`work/` (fetched from the official jmacd/xdelta 3.1.0 release).

**CLAUDE.md** — session working rules: every change gets a changelog entry
in the same session (corrections update the entry that documented the old
state), releases cut both the snapshot and the patch set, no game data in
git.

**Stages 3, 4 and 5** — the full scenario script of all six dialogue
members: 1,430 records, ~41k Japanese characters
(`translation/stage000{3,4,5}_0{3,4}.json`). With stages 1-2 already
shipped, the first five stages are in English.

Translated by six parallel subagent translators from `export_stage.py`
briefs (rules, per-speaker voice cards, slice glossaries), answers merged
by sha with `merge_stage.py`, and every member passing `check_stage.py`
clean: escapes, keyword links, line counts, real-pixel widths, charset,
coverage. House style unified after merge: silence lines mirror the
source's ellipsis count, scene banners keep the ～ wrapper, no Japanese
honorific suffixes (the shipped stages 1-2 set that convention), and AG's
ALL-CAPS robot-speak ends where the source's katakana does.

Pipeline changes the new stages forced: `extract.py` lists STG0003-0005
(and passes `unsdat.main` a correct argv -- the old call put the program
name in `src` and every stage decrypt silently failed); `deploy.py`'s
layout ships the three new SDATs (the first deploy silently left the
originals on the disc -- caught by hashing the disc after); and
`cpkpatch.py` moves an ITOC size row from 16-bit `CpkItocL` to 32-bit
`CpkItocH` when a replacement outgrows the columns, which English does:
stage 3 member 3 is 68,031 bytes uncompressed against a 52 KB original,
stage 4 member 4 likewise. Round-tripped byte-identical on a 68 KB dummy;
all three SDATs pass the `rpcs3 --decrypt` acceptance oracle. Details in
`docs/CPK_WRITE.md`.

**Voice: section 003** -- unit UNKNOWN, no weapon call-out matched
(sections.json's weapon_lines is empty for this section). 114 distinct
lines, none self-naming: a rough masculine mercenary register (ore/ze/na/
teme) that taunts a "rumored Gundam" opponent by name three times,
references combat against/as an AT (Armored Trooper -- "no rookie AT
pilot", "perfect prey for an AT") without ever naming a VOTOMS character
by name (checked this project's translated VOTOMS roster -- Chirico
Cuvie, Fyana, Ru Shako, Bolouze Gotho, Vanilla Vartla, Jean Paul Rochina,
Coconna, Kan Yu -- against their established personalities; none match
this cocky, fame-hungry hunter), calls itself/its squad "dogs of war"
(plural "we"), and has hit-taken lines about a malfunctioning Mission
Disc and failing hydraulics. Shipped as an unnamed mercenary grunt voice
with no name in the English, recorded in `analysis/voice_identity.json`.
Section 2 carries this exact same 114-line set verbatim and should ship
the same phrasing. 114 of 114 distinct lines translated, `check_voice.py`
clean, no duplicate English across differing Japanese. Budget forced
heavy compression throughout -- entry 8 "Skilled AT pilot!" and entry 9
"Perfect AT prey!" drop the demonstrative "that one/for an AT" framing,
entry 14 "Bag it, I'm made!" avoids inferring gender on the unnamed
target ("that one") the Japanese does not specify, entry 107 drops the
"Gundam" address entirely to fit "Overhyped!" in a 14-letter budget
(entry 106 nearby still carries the name), and entries 80/84 (both a
Mission Disc failure line, 26-letter two-line budgets) split the
glossary term so only one of the pair carries the full "Mission Disc"
name while the other carries the meaning ("Disc's fried!"), per the
no-duplicate-value rule.

**Voice: section 172 is Loni Garvey's berserk/death scene (Shambro), reviewed
against an external model's draft** -- identity confirmed from the jp: entry
20 calls out her dead parents then her commander in one breath (お父様！
お母様！カークスっ！！), entry 24 addresses Banagher Links by name
(バナージ…悲しいね…), and entries 21-22 fray a Zeon loyalty chant into a
broken half-word as her voice fails; matches `source/library/pilots.json`
i=151 (Loni Garvey, revenge against the Federation as her first priority) and
ties section 84/85's previously-unnamed "Kirks's subordinate" grunt to a name.
Recorded in `analysis/voice_identity.json` under "172". The external draft
was mostly sound (correct speaker register, budgets mostly respected) but
had six real problems, fixed in place: entry 1 "Move! Go!!" broke the jp's
repeated どけ into two different words, losing the escalation, fixed to
"Out! Out!!"; entry 2 "Feel! Feel!\nFeel it!!" mistranslated 思い知れ (closer
to "you'll pay/know the consequence" than generic "feel"), fixed to "Pay!
Pay!\nPay for it!!"; entry 13 "Ha ha hah!" read as laughter for what is
exhausted panting (はあ…はあ…はあ…), fixed to "Hah...hah!"; entry 20
"Parents! Kirks!!" collapsed her two dead parents into one word, fixed to
"Dad! Mom! Kirks!!" (fits the 17-letter budget exactly, keeps all three
addressed individually); entry 21 "Sieg Zeon! Sieg Zeon!\nSieg" truncated the
third repetition mid-word and used shouted "!" for what the jp trails off
with "…", fixed to "Sieg Zeon...\nSieg Zeon..."; entry 24 "Banagher" dropped
the entire second clause (悲しいね, "isn't it sad") -- the 10-letter budget
cannot hold both the name and the clause, and per the project rule to never
drop the end of a sentence, fixed to "So sad..." (drops the name instead,
FLAGGED as a judgment call since this is the line's famous character-name
beat). Entry 22 "Sieg...Z" also nudged to "Sieg...Ze" to use its one spare
budget cell, matching the jp's own mid-word cutoff (ジオ before ン) more
closely. 20 of 20 distinct lines, `check_voice.py` clean.

**Voice: section 94 is the Garencieres' bridge/crew ensemble, 159 lines**
-- filed as unit UNKNOWN, no weapon call-out matched, correctly so: the
section names no mobile-suit weapon, only the ship's own gun (entries
221/222, スキウレ砲, the Garencieres' main cannon, transliterated here as
"Skiure" -- no prior English spelling exists anywhere in this project,
so this is an unverified first-instance transliteration). This is a
multi-voice bundle in one file, the same pattern this project already
uses for other warships (section 135's Rewloola bridge, pilot:null;
section 745's four-person Ptolemaios 2 ensemble). Two named individuals
surface: Suberoa Zinnerman, the Garencieres' 52-year-old captain
(`source/library/pilots.json` i=145: his own crew call him "キャプテン",
Captain, matching this section's own crew-to-captain address at 143,
148, 154, 156, 217), and Flaste Schole, a 27-year-old Garencieres squad
member (pilots.json i=146, glossed "Flaste" in this brief) addressed by
name and answering back within the same file (181, 189, 199, 202 call
out to him; 217 has him apologize to the Captain). Zinnerman carries the
rest of the file: fleet/gunnery orders (0, 2, 3, 4, 7, 22, 56, 57, 144,
146, 147, 149), personal protection of his own named pilots Gilboa (62,
73) and Marida (63, 74) -- matching pilots.json's note that he treats
Marida like a daughter and has known Flaste since a Federation POW camp
-- and a running duel of taunts against Banagher Links by name (10, 64,
75, 89, 92, 93, 118, 122) in a reluctant, weary-veteran register ("don't
wanna kill a kid", "go home quietly, I mean no harm") consistent with
his hatred of the Federation (his hometown Globe was destroyed, wife and
daughter killed) tempered by unwillingness to kill a literal child --
distinct from the colder section 66 Flast(e) mobile-suit voice this
project already recorded. Recorded under "94" in
`analysis/voice_identity.json`. Budget forced heavy compression
throughout (6-9-letter budgets were common); the worst losses were
entry 58 ("Garencieres, moving to support!" shipped as "Here to help!",
ship's own name dropped for a verb), entry 70 ("protect the Red Comet!"
shipped as "Save him!", Frontal's epithet dropped entirely), and entry
78 ("Garencieres" dropped from "treated as a target, how pathetic" to
fit two lines at 24 cells, shipped as "Target practice,\nhow sad!").
Entry 194 (budget 5) was left in Japanese: "Flaste" alone is 6 letters
and cannot be shortened without truncating the name, which the brief
forbids, and no shorter established form exists.
`python tools/check_voice.py work/voice/answer/094.json`: 0 problems, 158
of 159 answered. Not yet merged into `translation/`.

## 0.4.2

**The COMMAND menu** — Move / Attack / Ground / Spirit / Status, and every
other label of the unit command menu and the map system menu (End Phase,
Search, Unit List, Objectives, Quick Save, Persuade, Board, Launch, Song,
Maximum Break, Tag Command, Repair, Resupply, Air, Underground, Underwater,
Parts, E-Change, Tactical Command, Transform, Trans-Am, NT-D, GAI Mode,
Tengen Toppa, Combine, Separate, Change Main, Wait, Recover, Transform
Toggle). 40 labels, `translation/ui_eboot.json`.

0.4.1 recorded this menu as textures. It is not: the labels are a **UTF-8**
string table in the executable (`.rodata` VA 0x6e4dd8.., 8-byte slots, beside
the `AID_CommandMenuMng` class name), drawn through a Unicode path. Every
earlier search was for cp932, which is why "no standalone occurrence in the
executable" was true and still wrong. Each label is referenced exactly once,
from a 36-byte command descriptor {label, id, handler, arg, ...} in `.data`;
`eboot.command_labels` writes English that fits the slot in place (33) and
repoints the descriptor at English in the mapped gap otherwise (7).

Confirmed on screen as plain ASCII (the game's own fullwidth Latin, fixed
pitch). Then switched to the **VWF face**: the UTF-8 path draws through a
65,536-entry Unicode → cp932 table in `.data` (VA 0x7df8c8, ■ where
unmapped); the build points U+0100+ch at the VWF cell of each letter and
writes the labels with those codepoints, so the menu uses the same Rodin
cells and width table as dialogue and weapon names. Confirmed on screen:
Rodin, proportional -- but off-centre, because the menu centres by
character count × the fixed pitch while the VWF ink is narrower. Fixed with
one invisible leading glyph per label (a blank cell from cp932 row 0x88,
reached through U+0180+k) whose width-table byte supplies exactly the
missing advance. Centring confirmed on screen; the user preferred
**left-aligned**, so the pads now put every label's ink 3.4 cells left of the
button centre instead (`COMMAND_LEFT`), with zero-width extra pads for the
short ones; 11 distinct pads. 戦術指揮 → Tactical Cmd and 変形トグル → Auto
Transform so the longest labels end inside the button.

**Unit / pilot / mech ability screens** — Foc / SP / PP, CQB / RNG / SKL /
DEF / EVD / HIT, Move / Armor / Mobi / Sight, Unit Info, Kills, Skills,
Spirit, Parts... 36 labels, SRW V's terms, `translation/ui_hook.json`. These
strings sit in the UI member where nothing can be lengthened, but they are
drawn by the one string drawer the name hook already intercepts, so they are
swapped **by content at draw time** with no length cap -- the same mechanism
that was showing "Melee" over 格闘 (a glossary hit) in that screen. UI entries
sit first in the hook table and win over glossary English for the same whole
string. The table's string area moved up 1 KB (`NAME_STR` 0x78d800) to make
room. Terrain 空陸海宇 stays Japanese (one-cell columns beside a rating).

**Pilot Info** — Stats, Kills (drawn as `\n\n撃墜数\n`, so that exact form is
hooked), Ace Bonus, and the 機 counter suffix hooked to nothing, as SRW T
shows a bare number.

**Spirit command names** (44, `translation/spirits.json`) and **pilot skill
names** (70, `translation/skills.json`) — SRW V / T terms (Focus, Strike,
Alert, Valor, Iron Wall...; Potential, Prevail, Support Attack, Instinct...).
They are RPW_DATA j-strings in the `spirit` and `sk-pri` chunks and go
through the weapon-name swap unchanged: in place where they fit, appended and
repointed where not. The j-string table is deduplicated, so 突撃 -- the
weapon "Charge" and the spirit "Assail" -- is one string and keeps the weapon
name. The one-kanji spirit abbreviations (加 覚 気 ...) are left alone.

**Mech Info** — its stat column is one string (`ＨＰ\nＥＮ\n装甲値\n運動性\n照準値`),
as are `移動\nタイプ` and the other layout variants; each exact form is
hooked. Type, Name (first shipped as SRW T's "Ofl Name" -- Official Name --
but that is 4.5 cells of ink against a 3-cell slot and clipped the mech
name; the snapshot carries the fix), Team; 強化パーツ / 特殊能力 now read
Power Parts / Special Ability as in T.

**Mech special-ability names** (55, `translation/abilities.json`) — I-Field,
A.T. Field, Lambda Driver, D-Fault, HP/EN Regen (S/M/L), Sword / Shield
Equipped, Double Image, Trans-Am, NT-D System... These names are not RPW
j-strings (only their descriptions are); they sit in the executable's cp932
tables and the UI member, and are hooked by content like the labels.

**A third LOAD segment.** The 27 KB gap between the executable's two
segments was full (hook table 432/448, strings 10,992 B against 10,240).
One of the ELF's three placeholder `PT_LOAD` entries now describes a 64 KB
read-only segment at VA 0xc00000, backed by bytes appended to the file; the
hook table (2,048 entries) and every English string the hook, the menu
labels and the COMMAND menu write live there. `EBOOT.BIN` grows from
8,774,352 to 8,847,360 bytes. Boot-tested: the game loads it and every
hooked label draws from it.

**Terrain as words, SRW 30 style.** 空 陸 海 宇 are one-cell slots beside a
rating letter, so no letter string fits -- but a whole word drawn small does:
`digraph.TINY_CELLS` rasterises Air / Grd / Wtr / Spc / Und at cap 11 into
five empty cells of cp932 row 0x86, width 32 so they take the caller's pitch
exactly like the kanji. The hook reaches them through private-use
characters: the ratings row 空陸海宇, the vertical column, the single kanji,
and all 16 formatted movement-type combinations (空陸－－ ...).

**Hook fix.** The stub rejected any string whose first byte is below 0x81 as
"ASCII", which also rejected labels that START with a newline
(`\n\n\n移動\nタイプ` on Mech Info, `\n\n撃墜数\n` on Pilot Info). A leading
0x0a now walks the table.

**Weapon Info** — Weapon Info, Range, Rnds (first shipped as "Ammo", whose
wide m's overran the 2.2-cell 残弾 column into the next header; the
snapshot carries the fix), Cost (消費ＥＮ: the header
column is 2.3 cells wide, so not T's "EN Cost"), Req. Morale / Req. Skill /
Adaptivity (T), Effect, Upgrade, Max Range / Sp. Effect. All hook entries.

**UTF-8 titles and prompts** (`translation/ui_utf8.json`, 29) — Ace Bonus
(the Pilot Info holdout: it is drawn through the UTF-8 path the hook never
sees), Battle Result, Objectives, Battle Report, Parts Obtained, Level Up,
Warning / Report / Select / Confirm, the intermission menu (Team Setup,
Pilot Training, Pilot Swap, Upgrades, Power Parts, Swap Parts, Battleship
Upgrade, ・Sortie Select ...), "Are you sure?". Same writer as the COMMAND
menu, now generalised: every standalone occurrence in `.rodata`, no pads.
930 such strings exist; these are the first.

**Prefix hooks.** The Pilot Info ace-bonus title survived both of those: the
game composes that box as ONE string -- title, newline, description -- so
no whole-string entry can match it. The hook stub now takes flagged
entries (`"prefix": true` in `ui_hook.json`) that match the head of a
longer string; on a hit it writes English + the rest of the subject into a
scratch page and draws that. The stub also lets strings that begin with a
drawer escape code (0x2e-0x39) through to the table.

**Joined hooks, and how the ace-bonus heading was actually drawn.** The
Pilot Info heading survived the exact hook, the prefix hook and the UTF-8
translation. Probes settled it: an entry for the single character エ
swapped, so the drawer IS the hooked one -- and with the GDB server
answering nothing but its handshake on this RPCS3 build, a stub that drew
the subject's first 16 bytes AS HEX put the memory on screen:
`エ\0\0ース\0\0ボー\0\0ナス\0`. The game typesets that heading into tiny
NUL-terminated pieces and draws them one by one (the letter-spacing was the
tell). `"joined": true` entries now match across the NUL gaps. Blanking the
buffer on a hit was wrong -- the matching call is a MEASURE pass, and the
heading vanished; instead the stub remembers the matched range in BSS,
draws the English at the first piece on every pass, answers later pieces
with an empty string, and drops the range when the first piece stops
matching. エースボーナス → Ace Bonus is the first.

## 0.4.0

**Opening narration** — all 28 lines of the crawl. It lives in fixed 84-byte
records in a sibling CPK member, not in the Lua.

**Weapon and attack names** — 477 names, filling all 5,388 weapon name pointer
slots in `RPW_DATA`.

**Genion's voice set** — 126 lines, everything Hibiki and Sensei say from that
cockpit. *(Reverted after release — the append-and-repoint write corrupted
barks it never selected, and its verifier shared the writer's section
mapping, so it validated the mistake. Then re-shipped the same night: the
section was re-decoded from screenshot anchors, appending was proven
impossible (index offsets are pool-bounded — an appended offset crashed
the game), and all 126 lines were rewritten IN PLACE by
`tools/voice_section.py` from `translation/voice_genion.json`. The set is
section 134 in the current parser's numbering; 125/124 were the older
parser's numbers. See docs/VOICE_HANDOFF.md.)*

**Menu text** — the scenario select screen ("Play the game", "Learn basics.")
and the protagonist sheet (Name / DOB / ABO / Done).

### Known limits

* **姓 / 名 / 愛称** stay Japanese: their slots hold one or two letters, and
  nothing in the UI member can be relocated (see below).
* **The battle COMMAND menu is textures.** Established on screen, not guessed:
  editing all 19 copies of 移動 in the UI member -- by the same in-place method
  that demonstrably changes the scenario select and protagonist sheet --
  changed nothing. It is also absent from RPW's string table and has no
  standalone occurrence in the executable.
* **UI strings cannot be relocated.** The member holds 32-byte widget records
  whose first word looks exactly like a string offset relative to 0x59478, and
  every string has precisely one such referent. Rewriting them changes nothing
  on screen, so they are not the reference; the resemblance is coincidence.
  Every UI string is therefore capped at the length of the Japanese it
  replaces.
* **Gold styled titles** (■シナリオ選択, 本編シナリオ, ■主人公設定) are
  textures.
* **Voice is 126 of ~32,000 strings** — reverted once, then rewritten in
  place (see above). The writer runs outside the build, so a rebuild
  drops the patch unless it is re-run — which happened; see Unreleased.
* Abbreviations where a slot is small: DOB, ABO. Pair cells would fit "Birth"
  and "Blood" but draw condensed beside proportional letters, and one screen in
  two faces reads worse than an abbreviation.

### Reverted before release

* **Repointing カミシロ** through the display-name array and the TOC. Those are
  the regions `inplace_names` refuses because entries there are lookup keys,
  not display strings; overriding that produced
  「ゲームデータが壊れています」 on the next boot.
* **Pair cells for menu labels**, for the face-mixing reason above.

## 0.4.1

No new text. Records that the COMMAND menu is textures and that UI strings
cannot be relocated, both settled by display tests rather than by searching.

Note on release diffs: the three `STG*.SDAT` files differ between builds even
when their contents do not, because `make_npdata` encryption is not
reproducible. Compare the `.cpk` inputs, not the SDATs, to tell whether a stage
actually changed.

## 0.3.0 and earlier

Not snapshotted -- releases start at 0.4.0. Earlier work is in the git history:
the font atlas and VWF letter cells, the EBOOT draw-time name hook, RPW_DATA
name swapping, the terminology reference system, and stages 1 and 2.
