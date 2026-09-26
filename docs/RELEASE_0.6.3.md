# English patch 0.6.3 — Time Prison

For the Japanese retail PS3 version of Super Robot Wars Z3: Jigoku-hen
(BLJS10256). Requires your own game dump. Downloads contain patches and
installation tools, not a complete game.

## Changes since 0.6.1

- Story translation expanded to **83 of 116 story scripts** (41,461 records),
  plus all **26 intermission scripts** (1,281 records).
- English **Super Robot Wars** title logo with **Time Prison Chapter**
  subtitle, preserving the original Z artwork and animation.
- English Library menu artwork and romanized voice-actor credits: 153 actors
  across 193 entries. The original game's 215 uncredited entries remain `---`.
- Standardized the stat name to **Focus / Foc** throughout the UI and related
  descriptions; revised power-part and pilot-skill descriptions.
- Weapon Info and Mech Info alignment, Support Def counter spacing, Combat
  Record navigation/help text, battle notices and other menu/report fixes.
- Current battle-line translations, terrain labels, title cards and the
  translated end-session scene and related trophy text are included.
- Version number displayed on the title screen.

## Downloads

- `SRW-Z3-English-0.6.3.iso.xdelta` (149.1 MB): apply to the pristine Japanese ISO.
- `SRW-Z3-English-0.6.1-to-0.6.3.iso.xdelta` (18.9 MB): update the exact 0.6.1 ISO.
- `SRW-Z3-English-0.6.3.zip` (85.1 MB): 186 per-file patches, application helper,
  checksum manifest and instructions for a pristine folder dump.

Original ISO: **4,431,872,000 bytes**, MD5
`2cfedd95e5bdde49550cffa21c3c29a3`.
The update requires the 0.6.1 ISO: **4,935,067,648 bytes**, MD5
`2e8e5dbe6fa92c3f5abdb286da3cd80c`.
Both patches produce the same **4,996,820,992-byte** 0.6.3 image, MD5
`7936d74e28e5b7259ab6666a967e71a7`.

```text
xdelta3 -d -s "original.iso" SRW-Z3-English-0.6.3.iso.xdelta "SRW-Z3-English-0.6.3.iso"
```

For an update, use the 0.6.1 image as the source and the 0.6.1-to-0.6.3 patch.
Close RPCS3 first and move only `dev_hdd0/game/BLJS10256_DATA` to a backup
location before launching the new version. The game recreates this cache.
Preserve your savedata folder. Make sure RPCS3 boots the new image/folder,
not an older ISO still registered in the game list.

For folder dumps, extract the ZIP and read its included `INSTALL.md`.
Install all patches together; translated data and font mappings must match.

## Scope and verification

**This is a partial translation, not a 100% release.** There are 33 remaining
story scripts. Separately, the mission-text audit covers 142 archives and
reports 504 translated variants and 1,034 untranslated variants. Do not
interpret the story-script count as complete mission-text coverage.

The complete build passed its binary/layout checks and 132 regression tests.
All 408 Library CV fields were checked against the build's font mapping.
All 186 game files were read back from both ISO directory trees and compared
with the release snapshot. Per-file patches were decoded and verified;
the ZIP passed CRC and all 189 entry-content checks.
Both distribution ISO patches were independently decoded and compared with
the same release image; both outputs match.

Automated checks are not a full in-game playthrough. Runtime visual testing
of the combined changes remains incomplete. No gameplay-condition changes
are intended; the patch installer does not modify saves.

## Download SHA-256 checksums

```text
192ddec1581b911e022e56c542b2bdc7a66d17669a15125b163f05ef848d34c3  SRW-Z3-English-0.6.3.iso.xdelta
51755f2a13cbd15c3a7db2cbf7de13692e1d60e6e08afb31efb6b12ceb79745a  SRW-Z3-English-0.6.1-to-0.6.3.iso.xdelta
556fe4c680601612c494719f4afe80bad8f83b73b4c23b5f620f60203209f143  SRW-Z3-English-0.6.3.zip
```
