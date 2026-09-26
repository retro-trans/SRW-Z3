# Vita screenshot regression checklist

These are implementation and verification tasks, not a list of dismissed reports.
The installed EBOOT and UI archive were last checked during test13 work and
matched test09. No test14 installation has been performed.
A source/test fix is not a live-game pass.

Test-03 is built at work/vita/english_vwf_test_03 with all 95 Vita tests
passing, zero shared-catalog compatibility issues, and all 118 rebuilt
archives / 589 ZIP files verified. It has not been installed or live-tested.

Test-04 includes all of test03 plus the save/settings follow-up rows below.
All 96 tests pass and the complete ZIP has been verified (589 files,
118 rebuilt archives). It also remains uninstalled and requires live retesting.

Test-05 adds the Dancouga Nova suspend scene and battle-preview spacing.
97 Vita tests plus the PS3 scene-isolation regression pass; its complete ZIP
is verified (589 files / 118 archives), not installed or live-tested.

Test-06 adds the post-prologue narration, default-name substitutions and
Spirit/map-search follow-ups below. All 100 Vita tests pass and the complete
ZIP is verified (589 files / 118 archives). Not installed or live-tested.

Test-07 adds scoped compact roster/settings labels, Move/Stats commands and
Pilot Info full-name / Stats / Ace Bonus bindings. All 102 Vita tests pass;
the complete ZIP is verified (589 files / 118 archives). Not installed or
live-tested.

Test-08 adds compact Atk. to both battle-preview buttons. All 102 Vita tests
pass; the rebuilt menu archive and all 589 ZIP files are verified. Unchanged
test07 files were hash-checked before reuse. Not installed or live-tested.

Test-09 adds the reported library lists and Scenario Chart fixes below.
All 106 Vita tests and all 475 compatibility views pass. The full rebuild
verified 118 archives and 589 ZIP files; actual-ZIP native draw/art checks
also pass. It is not installed or live-tested.

Test-10 fixes the reported Right Stick help label and split Unit result
headings. All107 tests pass; the UI archive and all589 package entries are
verified, with earlier startup/chart artwork preserved. Not installed or
live-tested.

| Report | Implementation status | Live-game status |
|---|---|---|
| Intermission header remains Japanese despite text aliases | Test16: replace the actual page0 word sprite; preserve palette and all other cells | Retest required |
| Intermission footer クリア remains Japanese | Test16: source-pinned whole Clear label from native executable, both encoding paths and centering checked | Retest required |
| PS Store still left of its button | Test16: add88 native pixels to this widget only, calibrated from supplied960px Vita crop; previous generic centering was insufficient | Retest required |
| Scenario Select buttons remain Japanese / separate white square | Test16: Main Scenario and Tutorial Scenario sprite cells, native UVs validated; square prefix becomes an equal-width space | Retest required |
| End Phase warning above End the phase? remains Japanese | Test15: native composed count inventory maps complete lines to Teams still able to act: N.; original count calculation, prompt controls and layout unchanged | Retest required |
| Map popup 特別捜査官 stays Japanese | Test14: discovers whole native preset squad names, enabling shared Special Investigator; nonmatching custom names pass through unchanged | Retest required |
| Mech Info split チーム． stays Japanese | Test14: two source-pinned Team variants, three redundant fragments hidden; team values and all widget fields unchanged | Retest required |
| End Phase doubled No | Test11: active and inactive layers normalized to28px; positions and native glyph advances use the same pitch | Retest required |
| SR Point / 10000 bonus message Japanese and overlapping | Test11: complete shared English sentences with two redundant emphasis overlays blanked; reward amount/logic unchanged | Retest required |
| Tiny battle diagram 攻 badge | Test11: scoped AT label in the original one-character slot through a verified two-byte alias | Retest required |
| Intermission heading, Team Setup, Pilot Swap, D-Trader and footer Japanese | Test11: whole captions at split-widget sites;9 episode/turn footer variants; dynamic counters and unlock states intact | Retest required |
| Battle Key Help Right Stick remains Japanese | Test10: direct native-widget binding to shared Right Stick caption; both encoding paths tested | Retest required |
| Get Result Unit heading remains Japanese | Test10: two split native pairs bind complete Unit to first widget and hide only their own suffix; whole-word variant also bound; reward values untouched | Retest required |
| Glossary term list and Original/Orguss source-series labels stay Japanese | Test09: whole native executable keyword/series display names use shared glossary translations; pilot short-name ambiguity remains ID-scoped | Retest required |
| Three library titles, name-column headings and sorting hints | Test09: shared library labels plus compact Character Library / Robot Library scoped aliases; Kana/Series ordering unchanged | Retest required |
| Scenario Chart title, background subtitle, episode number/title and Speed Up | Test09: two native chart atlas members, complete composed episode strings and private OK label; palette/animation/navigation/IDs untouched | Retest required |
| Battle-preview Attack still extends beyond button | Test08: both native buttons use shared Atk. through scoped bindings, checked at full 32px pitch with 16px panel clearance; global Attack and hit rates untouched | Retest required |
| Settings and roster overlap despite prior font changes | Test07: compact Settings 1/2, Rep., Resup, S. Atk/S. Def; scoped aliases and actual neighboring-column gaps checked at 32px live pitch | Retest required |
| Move / Stats command menu still Japanese | Move/Stats conflicts resolved; MV abbreviation restricted to map popup | Retest required |
| Pilot Info full name, Stats and Ace Bonus | Default full-name display keys plus direct native Stats/Ace Bonus widget aliases; both encoding modes CPU-tested | Retest required |
| Post-prologue ZEUTH narration | All 18 exact sources verified in Vita's 80 x 88-byte record grid; shared draw-time translations, timings unchanged | Retest required |
| Japanese Kamishiro in Suzune dialogue | Default-name substitution constructor hooked; both full-name orders covered, saved/custom names unchanged | Retest required |
| Spirit list SP Cost / +Eff. | Shared labels and line-split keys; redundant SP suffix only blanked, actual SP column intact | Retest required |
| Map-search help, return label, Move, HP/EN recovery captions | Shared help plus new source-bound return label; scoped compact captions / line-split keys / local widths | Retest required |
| Spirit / skill descriptions, including Focus and Support Attack | Correct percentage/printf filtering; regression test added | Retest required |
| Ally List Repair / Resupply / support header overlaps | Exact caption conflict resolved; four-column width budgets checked | Retest required |
| Spirit search tab and Special Ability overflow | Spirit caption resolved; local sizes and native VWF centering corrected | Retest required |
| Battle Report clipping and map popup cramped labels | Menu/popup sizes, compact support captions and proportional centering corrected | Retest required |
| Terrain and movement capability names | Native terrain inventory plus 19 native formatter slots and one-cell glyphs | Retest required |
| Spirit status abbreviations | Equal-length semantic arrays patched before per-status indexing; both font pages matched | Retest required |
| Mission conditions and composed episode headings | Native Lua preset discovery, numbered conditions and native 181-record heading table | Retest required |
| Date cards | All 77 complete native date keys included | Retest required |
| Map-pin location captions | All 83 native P8 caption adapters and UV inventories | Retest required |
| Episode title cards | 124 title textures and 5 native episode effects | Retest required |
| Invisible linked words in Kei's opening dialogue | LR held the row across the replaced MLA; restore row from native argument, native X/Y regression passes | Retest required |
| Tactical Situation episode heading | Composed title already included in test03; installed executable verified as test02 | Retest required |
| System Settings 1/2 overlapping tabs | All eight native variants sized to measured 230px budget | Retest required |
| Memory-card save option and new/overwrite confirmation line | Shared memory-card label and bounded native multiline-dialog line discovery | Retest required |
| Japanese inactive No / overlapping Yes | Shared labels, measured column gaps, all four native active/background layers aligned | Retest required |
| Sakuya's Japanese suspend dialogue and name | Complete nine-record Dancouga Nova scene translated; both platform adapters share source-bound catalog | Retest required |
| Battle Attack clipping and Foc/value touching Advanced AI | Two Attack records and four Foc/value states sized to local budgets; names/combat values unchanged | Retest required |
| Battle Air and Spirit status strips | Native one-cell replacements already included since test03; regression verifies Air remains patched | Retest required |
| Pilot List and Upgrades headings, DEF stats | Test12: source-bound native labels in both list variants; combat Defense untouched | Retest required |
| Upgrade Wpn Rank column and Sight/Wpn Rank footer | Test12: multiline aliases preserve two lines; only the redundant RANK label is hidden; values/bars unchanged | Retest required |
| Intermission Library buttons and Options Library entry | Test12: all six native button records including selected Robot variant; original special modes preserved | Retest required |
| Library Confirm/Back hints touching | Test12: compact : OK in fixed-width hint widgets; icons, positions and general Confirm unchanged | Retest required |

| Power Parts title / equipped footer / crowded Repair and Resupply | Test13: both list variants, three footer states, parts-only Rep/Resup captions measured against column gaps | Retest required |
| Select Slot and Team movement label Japanese | Test13: native widget aliases and direct whole-string draw keys; only split Team suffix hidden | Retest required |
| Parts filter SP Cost overlaps Special | Test13: removes global SP Cost leakage into consumable categories; scoped Spirit headers retain SP Cost, filter category uses Use without changing indices | Retest required |
| Network Upload, Download, PS Store tail, Bonus Scenarios | Test13: scoped captions, split PS Store centered as one label, compact Bonus Maps; no online action changes | Retest required |

Preserve locked question marks, unavailable dashes, glossary links, gameplay
values, animation timing, original files, saves, and unrelated worktree changes.

Test14 verification: 115 Vita tests, 161 packaged widget bindings, 328 native
UI drawing cases and 23 library/chart drawing cases pass. All 589 packaged
files are verified; 587 are unchanged from test13. Every prior UI key/value
and nonzero UI archive member is preserved. Live retesting remains required.

Test15 verification: 117 Vita tests pass. Actual ZIP checks cover 105 native
count inputs, 10 warning draws and 10 centered positions, plus all prior
widget/name/chart checks. All 589 entries are verified; only EBOOT differs
from test14. Every prior translation key/value is preserved. Not live-tested.

Test16 verification:120 Vita tests pass. Actual ZIP checks preserve every old
translation key/value and587 unchanged files. Only five UI bytes and four
word-sprite cells differ; palettes, geometry and prior startup/chart art stay.
Native Clear drawing/centering and prior UI/name checks pass. Store placement
and the heading square change still require live visual retesting.
