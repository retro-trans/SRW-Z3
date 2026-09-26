# Map support popup and preset squad names

## Support lettering

The reported popup uses AIDDATAPACK member 1 texture 2, not the separate
CMN battle-animation banners. Three phrases use six five-vertex XYUV fans
in member 0 at 0x4d518 through 0x4d6e8. Their original word rectangles were
only 72px wide (40px for Re-), squeezing long English into Japanese cells.

`support_popup_layout` widens Support to 132px, Defend to 118px, Attack to
106px and Re- to 62px. Each complete phrase retains its horizontal center;
vertical coordinates, original 8px italic shear, UVs, tint and animation
references stay unchanged. `trader_art` uses one point size with natural
word heights, preserving Support's descender. All six source UV fans are
independently inventoried by the regression test. CMN is unchanged.

## Squad and faction names

`translation/squad_names_hook.json` covers all 157 unique literal team names
in the original 142 stage archives, both ally TEAM_BUILD and enemy spawn
fields. This includes Crusher Squad and the formerly one-off Robot Mafia.
Names are not taken from incidental dialogue or comments. The parser reads
the quoted value next to the preset's team-name field marker and unescapes
Lua at byte level before CP932 decoding (Takeo/Support contain trail 0x5c).

Exact draw-time substitution uses the existing content hook. Native team
IDs, source names, formation logic, custom-name storage, saves, and scripts
are not rewritten. Existing glossary spellings are retained where available;
unknown/event placeholders are translated as labels, not deleted. Missing
names fail the source audit even when partial-story builds are allowed.

Reference checks: Ryujin Gang corresponds to the Ryujin gangsters credited
in [Fumoffu](https://japanese-voiceover.fandom.com/wiki/Full_Metal_Panic%3F_Fumoffu_%282003%29).
Space Demon terminology agrees with the [Akurasu unit list](https://akurasu.net/wiki/Super_Robot_Wars/Z3.2/Mech_List)
and the existing Space Demon King glossary entry.

## Validation

`test_support_squad.py` checks the exact source category, font aspect, all
six UV fans, center preservation, and byte isolation. `check_issue_fixes`
reads the rebuilt AID geometry and every emitted EBOOT translation entry.
These are asset checks; a live RPCS3 visual retest is still required.

Build 0.6.4 completed and was installed on 2026-09-13 after RPCS3 closed.
All 190 build-manifest files, 186 installed translations, 560 complete-disc
files, and 16 unchanged save files were verified. Recoverable backup:
`work/install_backups/0.6.4_20260913_083736`. The single-folder metadata
now advances with the build and is included in installer backup/rollback.
The native-quad comparison was reviewed at `work/support_popup_comparison.png`.
