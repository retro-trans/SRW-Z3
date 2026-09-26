# English Vita VWF test 16

Complete Vita3K test ZIP for PCSG00264. No original PKG installation or
separate patch is required. Keep Vita firmware and font packages installed.

1. Back up your current PCSG00264 installation and saves before replacing it.
2. In Vita3K, use File > Install .zip, .vpk and select
   `SRW-Z3-Vita-English-VWF-test-16.zip` without extracting it.
3. If prompted to replace the existing game, proceed only after your backup.
   Do not delete saves or firmware. Close the game before installation.
4. Launch New Game and check the opening English dialogue for proportional
   spacing. Then check menus, battle subtitles, keyword links, Back Log and
   skipping dialogue. Existing saves are not modified by the package.

Includes real single-letter VWF, 42,742 source-matched story records, 31,666
battle subtitles, library/keyword text, gameplay terms, 16 suspend lines and
exact UI/title/route keys. English comes from the same catalog as PS3.

Test02 also includes the shared English title logo,
Time Prison Chapter subtitle and five Library menu labels. These changes
are NOT present in the original September14 test01 ZIP.
Test02 includes the startup setup/scenario fixes and all
28 opening-narration rows from the shared PS3 catalog. Those narration rows
live in native member7, separately from Lua dialogue. Timing and other record
fields are preserved. Check these screens and narration skipping during testing.

Test03 addresses the reported Vita screenshots:

- Restores the invisible linked words by preserving the native dialogue row.
- Includes all 38 Spirit and 124 skill descriptions; literal percentages no
  longer get mistaken for printf commands.
- Reads mission conditions from native stage presets, including numbered
  victory/defeat lines, and uses native metadata for composed episode headings.
- Adds 77 date cards, 124 title textures, 83 map captions and 5 episode effects.
- Adds 30 one-cell terrain/status labels without changing per-status indexing.
- Corrects proportional centering for translated SJIS and UTF-8 labels.
- Fits Ally List headers, search tabs, command-menu text and popup labels.

The builder verifies file contents and the tests execute the affected native
Thumb routines. These are not substitutes for live visual/play testing.

Test04 includes all test03 fixes, plus Save to Memory Card, independently
drawn save-confirmation lines, aligned active/inactive Yes/No labels, and
fitted System Settings 1/2 tabs. The tactical episode heading fix from test03
is included. Keep the older test ZIPs for rollback.

Test05 adds the entire nine-line Dancouga Nova suspend scene (Sakuya,
Johnny, Kurara and Aoi), fits both battle-preview Attack labels, and reserves
a gap between the Focus value and pilot name on both sides. Shared wording
is available to both platform adapters; no PS3 game or release is rebuilt.

Test06 connects all 18 post-prologue narration lines to the shared English
wording, translates SP Cost / +Eff. and the map-search help / return label,
and fits MV and HP/EN Rec: captions. Only the redundant SP suffix is hidden;
the actual SP value column and all gameplay values are preserved.

Default Hibiki/Kamishiro names are translated when the native dialogue
substitution table is built, including both default full-name orders. Saved
name buffers are untouched. Custom names and partly customized full names
pass through unchanged. The width table is now non-executable data after the
original BSS, freeing verified RX space for the new name hook.

Test07 replaces the narrow Settings tabs with Settings 1/2 and uses scoped
Rep. / Resup / S. Atk / S. Def roster headings. Width checks now use actual
neighboring column gaps at the conservative 32px runtime pitch, independently
of the smaller requested record font. Thirty native widget bindings preserve
positions, sort/cursor behavior, pointers and original section sizes.
The command menu now uses Move / Stats, while the narrow popup retains MV.
Pilot Info displays Hibiki Kamishiro; Stats and Ace Bonus have explicit native
widget bindings. Locked question marks and gameplay values remain unchanged.

Test08 uses the shared compact Atk. label on both battle-preview buttons,
with a conservative live-width check. Other Attack labels, counter labels,
hit percentages and battle behavior are unchanged. All test07 fixes remain.

Test09 translates the library list titles, name columns, sorting hints,
glossary terms and source-series labels reported in the screenshots. The two
narrow encyclopedia tabs use Character Library / Robot Library. Kana Order
still means the original Japanese reading order; sorting is not changed.
Scenario Chart includes English title/background lettering, Speed Up,
separate episode numbers and bracketed titles. Its private Confirm caption
uses OK to leave room for the Back icon. All earlier fixes remain included.
Chart IDs, unlocks, navigation, source palettes and animation are unchanged.

Test10 translates the Right Stick label in Key Help and fixes both split
Unit result-screen headings plus the whole-word variant. Only the redundant
Japanese suffix in each split heading is hidden. Funds, Z Chips, EXP, PP,
Score, level, control mappings and unknown team names remain unchanged.
All test09 fixes, including startup and Scenario Chart artwork, are retained.

Test11 aligns active and inactive Yes/No text at a common 28px pitch. Reward
messages now read SR Point earned / Bonus funds received: 10000, with their
redundant Japanese emphasis overlays removed. The tiny attack badge uses AT.
Intermission, Team Setup, Pilot Swap and D-Trader captions, SR Points/Z Chips
footer labels and episode/clear/turn captions have scoped native bindings.
Split caption tails are hidden only in those widgets; numeric values and
unlock/menu behavior remain unchanged. All previous artwork is preserved.

Test12 binds the Pilot List and Upgrades headings, DEF stat labels, Wpn Rank
columns and Sight/Wpn Rank footer lines. Only the redundant footer RANK
overlay is hidden; rank values and bars remain unchanged. The Intermission
Library popup's five buttons and the Options Library entry now use English.
These are native text widgets, separate from the already translated title
screen artwork. Tight Confirm/Back widget hints use : OK; general Confirm
text is unchanged. Library rendering modes and all widget coordinates are
preserved, with compact labels checked against the larger live text size.

Test13 translates the Power Parts headings/footer, Select Slot hint, Team
movement label, Upload/Download, PS Store and Bonus Maps. It shortens the
parts-only Repair/Resupply headers to Rep/Resup. Consumable filters use Use,
not the unrelated SP Cost caption; Spirit-list SP Cost remains translated
through dedicated widget aliases. The fixed-width filter retains identical
category indices and byte/character counts. Numeric values, equipment slots,
inventory, buttons and online actions are unchanged. All test12 fixes remain.

Test14 includes native Lua preset-team-name lookup, including Special
Investigator. This display-only lookup uses existing shared translations;
scripts, team assignments and saved names are not rewritten. Unrecognized
custom names remain unchanged. Mech Info and roster Team labels now use one
English word, with only their redundant kana fragments hidden. Numeric
values, size ratings, icons and all widget positions stay unchanged.

Test15 translates the composed remaining-team warning, including the reported
six-team case: "Teams still able to act: 6." All native displayed counts are
covered. The original count calculation, confirmation, Yes/No controls and
widget layout remain untouched; only completed display strings are matched.

Test16 translates the native Intermission heading and Scenario Select word
sprites (Main Scenario / Tutorial Scenario), removes only the separate square
before Scenario Select, and translates the direct Clear footer label.
PS Store receives a position correction measured from the supplied Vita crop;
Upload, Download, Bonus Maps, controls and online behavior remain unchanged.

This is a development test, NOT a finished port. In-game boot/layout remain
unverified for test16. Some dynamic UI, link rectangles, other map/menu
textures, unresolved terms and 856 suspend records still need work. The newly
ported title artwork also needs an in-game check.
Physical Vita support is not verified. Do not mix this executable with the
old fixed-cell pilot font or scripts; install the complete matching ZIP.

No license, work.bin, firmware or saves are included. No PS3 files are changed.
The build checks native source hashes, all changed and unchanged CPK members,
and every ZIP entry's size, SHA256 and CRC. Those checks do not prove gameplay.

If it fails, keep the previous build, and send the Vita3K version, error/log
and a screenshot. Never share your license or work.bin.
