# Version 0.6.3 — combined local build

Built September 12, 2026. This combines all currently completed translations
and the latest visual fixes in one matching font/data package.

## Included

- 83 of 116 story scripts (41,461 translated records) and all 26 intermission
  scripts (1,281 records); 109 registered stage archives rebuilt together.
- English Super Robot Wars logo with **Time Prison Chapter** subtitle,
  retaining the original Z artwork and animation.
- Romanized Library CV credits: 153 actors across 193 named entries;
  215 no-credit placeholders retained.
- Focus / Foc terminology; revised power-part and pilot-skill descriptions.
- Library button text, weapon/mech information alignment, Support Def counter
  spacing, Combat Record links, and the other integrated menu/report fixes.
- Battle dialogue, terrain labels, title cards, and the translated end-session
  scene and related trophy label from the current project sources.

## Verification and limits

The complete build validation passed. All 132 regression tests passed, and
the new build's 408 CV fields were independently checked against its font.
The snapshot contains 186 game files; file hashes were independently verified.
The title footer and successful-build manifest both identify version 0.6.3.
Both per-file patch sets are complete: 186 patches from the pristine game
and 122 from version 0.6.1. Every patch was decoded and its result hash checked.

This is **not a 100% translation**. There are 33 untranslated story scripts.
The separate mission-text audit found 504 translated variants and 1,034
untranslated variants across 142 extracted archives. The detailed local
`message_coverage.json` is retained with the build and snapshot. Present
translations and non-mission UI remain strictly validated; missing mission
text is explicitly reported by the partial-translation build mode.

Installed for user testing on September 12, 2026: all 186 deployed file hashes
match the validated build, and all 16 saved-game files are unchanged.
Correction from testing: those files are in the extracted game folder, but
RPCS3's game entry still points to the older patched_0.6.1.iso. The active
boot target has not yet been corrected, so launching that entry still runs
the old version.
In-game visual verification is still pending. The three patch packages were
published as the latest GitHub release after explicit user approval. A
separate local release-packaging ISO was
subsequently generated and verified; the original and older ISOs are unchanged.

Previous game files and the old install cache are recoverable from
`work/install_backups/0.6.3_20260912_182937`. The game recreates its install
cache on next launch. `install_audit.json` in that folder records hashes.

## Local files

- Validated build: `work/build_0.6.3_all`
- Snapshot: `releases/0.6.3`
- Snapshot hash manifest: `releases/0.6.3.json`
- Per-file patches: `releases/0.6.3_xdelta`
- Public release notes and download hashes: `docs/RELEASE_0.6.3.md`
- Full-ISO patch: `releases/0.6.3_xdelta/SRW-Z3-English-0.6.3.iso.xdelta`
- Update patch: `releases/0.6.3_xdelta/SRW-Z3-English-0.6.1-to-0.6.3.iso.xdelta`
- Folder patch ZIP: `releases/0.6.3_xdelta/SRW-Z3-English-0.6.3.zip`
- Build log: `work/build_0.6.3_all.log`
- Regression results: `work/combined_tests_final.log`

Install the **whole validated build** together while RPCS3 is closed; do not
copy only the logo or Library file over a build using a different font mapping.
Back up the installed game before deployment and refresh only this game's
installed-data cache. Saved games must not be removed.

Patch sets target either the pristine Japanese dump or the published 0.6.1
snapshot, not an arbitrary mixture of older candidate files. Do not distribute
the snapshot's game files; distribute patches only.

The user's release request is complete. Both ISO patches were decode-verified;
all 189 ZIP entries passed CRC/content checks. Initial approval review blocked
upload; the user then explicitly approved publishing the three patch assets.
Published as latest at https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.3
on 2026-09-12 at 13:36:57 UTC. All uploaded sizes/SHA-256 digests match local
packages. No complete game files or ISO were uploaded.
