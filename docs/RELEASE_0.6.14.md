# English patch 0.6.14 — PS3, Vita3K, Vita hardware and save tools

## What changed

PS3 combines the published 0.6.13 menu improvements with the recent fixes:
dialogue/backlog link background geometry, speaker-name widths, dialogue
term selection, centered full-screen date cards, English Scenario Select
artwork and month/day DOB formatting. Its title footer reads 0.6.14.

Vita3K contains exactly the tested test16-linkfix-v4 build, including the
dialogue-scene fix. The in-game build label may still say test16.

This is a partial English patch, not a complete translation. PS3 retains
0.6.13's translation coverage, including 1,034 untranslated mission variants.
Newer working translation drafts are not part of this release. The combined
PS3 build is regression-checked, but has not itself received a full gameplay
test. The user confirmed the underlying recent link fixes on both emulators.

## Downloads

| Download | Required input |
| --- | --- |
| `SRW-Z3-English-0.6.14.iso.xdelta` | Original Japanese PS3 ISO |
| `SRW-Z3-English-0.6.13-to-0.6.14.iso.xdelta` | Exact released 0.6.13 PS3 ISO |
| `SRW-Z3-Vita3K-0.6.14-from-original.zip` | Original PFS-decrypted PCSG00264 v01.00 folder |
| `SRW-Z3-Vita-Hardware-0.6.14-from-original.zip` | Physical Vita with rePatch; original PFS-decrypted PCSG00264 v01.00 files and your own matching self_auth.bin |
| `SRW-Z3-Save-Converter-0.6.14-Windows-x64.zip` | Windows x64; your own decrypted saves/templates from both emulators, no Python installation |

Download checksums and expected game-image hashes are in `SHA256SUMS.txt`
and `RELEASE_MANIFEST.json`. The Vita packages contain their own per-file
source/target/patch manifests. Full games, keys, licenses, authentication
files, firmware and personal saves are not included. The Windows converter
was added on September 18; its ZIP checksum is listed in the save-tools section
below. The hardware patch's ZIP checksum is in its section below. No separate
checksum download is needed for either addition.
The Vita incremental test-build, Python-only converter and Tool Updates
downloads were withdrawn on September 18.
The original metadata files are retained as build records and may still list
those withdrawn assets. Use the Vita original-to-current patch and portable
Windows converter listed above.

## PS3 / RPCS3

Use xdelta3 (supply the tool separately). Keep your original ISO and write
the result to a NEW file. Do not apply both patches in sequence.

Original input:

- Size: 4,431,872,000 bytes
- MD5: `2cfedd95e5bdde49550cffa21c3c29a3`
- SHA256: `1b45cdd1651b98fe24b544223488289790ae87d5f82f1db272285fb4e4dffa89`

```text
xdelta3 -d -s "original-japanese.iso" "SRW-Z3-English-0.6.14.iso.xdelta" "SRW-Z3-English-0.6.14.iso"
```

Or update the exact released 0.6.13 image:

- Size: 4,996,823,040 bytes
- MD5: `3259c2c80a98d846dcf775649990a561`
- SHA256: `701a7e93a3c4e015caf1bbeae670d1cbfbc52c3c9b991c48d63f34091f3d70f6`

```text
xdelta3 -d -s "SRW-Z3-English-0.6.13.iso" "SRW-Z3-English-0.6.13-to-0.6.14.iso.xdelta" "SRW-Z3-English-0.6.14.iso"
```

The incremental patch does NOT accept a custom local v3/v4/v5 executable
update, a rebuilt ISO with a different layout, or an older release. For those,
use your untouched original ISO and the full patch. Check the final image's
SHA256 against `RELEASE_MANIFEST.json` before use.

RPCS3: close the emulator, extract the verified image with an ISO tool if
needed, and boot its `PS3_GAME` folder. Back up your previous installation.
When changing these game archives, the old game-data installation can be
stale. With RPCS3 CLOSED, move only `dev_hdd0/game/BLJS10256_DATA` to a backup
outside `dev_hdd0/game`, then allow the game to rebuild its data on first boot.
Never remove `dev_hdd0/home/.../savedata` or other games' folders.

These are the project's legacy RPCS3 ISO layout/executables. They are NOT
physical-PS3-validated or a console-ready signed SELF release.

## Vita3K

The small patch ZIP is NOT directly installable. Extract it and follow its
README. Python 3.8+ and xdelta3 are required. Run the provided patcher first
without `--write` to check your input, then with `--write --zip` to generate a
complete installable ZIP locally. Output must be a new folder outside your
source/patch directory. Allow at least 6 GB free space.

Install the generated `SRW-Z3-Vita3K-0.6.14-install.zip` through Vita3K's ZIP/VPK
installation command, not the downloaded patch ZIP. Back up existing game
and save data first. No license, key or `self_auth.bin` is supplied or needed
by this offline delta applier; input decryption is a separate prerequisite.

Use the original PFS-decrypted PCSG00264 v01.00 folder as the patch source.
This package targets Vita3K, not direct physical-Vita installation.

## Physical PS Vita — rePatch hardware test

Download `SRW-Z3-Vita-Hardware-0.6.14-from-original.zip` and read its `README.md`.
This is a **hardware test candidate**, not a VPK or a full game. It contains
120 deltas and offline preparation scripts. It uses the current 0.6.14 Vita
content but excludes all five emulator-converted modules. This exact package
still needs physical-Vita boot, battle, suspend and save/load verification.

Requirements: your Japanese **PCSG00264 v01.00** game running normally,
VitaShell, firmware-compatible rePatch enabled, the matching original
PFS-decrypted game folder on PC, your own `self_auth.bin`, Python 3.8+ and xdelta3.
No raw game files, authentication dumps, keys, firmware or plugins are included.
The auth file is sanitized locally; its shared-secret region is zeroed.

Extract the download. From its folder, run this check with your own paths:

```text
python apply_vita_hardware.py --source "D:/MyGame/PCSG00264" --self-auth "D:/Private/self_auth.bin" --output "D:/Z3HardwarePatch" --xdelta "D:/Tools/xdelta3.exe"
```

After the check passes, repeat with `--write`. Use a NEW output folder.
After **SUCCESS**, back up saves and any old patch, close the game, and copy
the generated `rePatch/PCSG00264` folder into `ux0:rePatch/` with VitaShell.
Do not copy into `app`, `patch` or savedata, and do not install either ZIP as a VPK.
The included guide covers obtaining your auth file, exact folder layout and rollback.

All 120 deltas were applied locally, producing 121 verified payloads including
sanitized auth. All output file hashes and the completed local overlay ZIP were
read back successfully. Sixteen synthetic hardware/applier regression tests pass.
These checks do not replace hardware testing.

Hardware download SHA-256:
`c98941abbb041481114cdbd39f5fd65555c8e8ace126af929d23e755ab4f2608`

## Saves in either direction

**Windows, no Python needed:** download
`SRW-Z3-Save-Converter-0.6.14-Windows-x64.zip`, extract ALL files into a writable
folder, and double-click `SRW-Z3-Save-Converter.exe`. Keep `_internal` beside
the executable. Select the RPCS3 `savedata` folder and Vita3K `PCSG00264` save
folder, click **Check saves**, review the mappings, then **Convert both directions**.
The app creates a new timestamped output folder beside itself under `work`.
Built-in instructions explain how to import the result. It needs no admin rights,
is offline, and includes its source and runtime licenses. It is unsigned;
compare the ZIP with the SHA-256 below, and do not disable security software.

Windows converter ZIP SHA-256:
`b786a21490af231ba8621e21de09a0a55d3fe49785ef92c3a6225e23defc5007`

The packaged executable passed 19 synthetic conversion/UI tests with Python
search paths disabled, both before and after extracting the release ZIP.
The window and built-in instructions were also visually checked on Windows 11.

Create system data and a manual save on EACH emulator first, then close both
and supply their save directories. The Windows ZIP includes the converter's
source for developers; no separate Python-only download is offered.

The converter produces both directions without modifying or installing
live saves. It preserves progress/checksums, validates formats and exact
round trips, and uses your own destination metadata templates. Back up
your complete profiles and test loading, saving and reloading before relying
on converted progress. These are profile conversions, not merged playthroughs
or a physical-console decryption/resigning tool. Keep generated backups,
metadata and converted-save ZIPs private.

## Verification and source

Every distributed game delta is decoded back against its specified source
and compared with the intended target. ISO verification also re-reads the
patched file entries through the image directory trees. Vita source/target
inventories cover all 589 files. Automated tests do not replace a full
playthrough on either platform.

GitHub's automatic source ZIP/tarball reflects the tagged repository commit.
The separate Tool Updates source supplement is no longer distributed here.
The tagged source does not include every local patch/build-tool change used
for this release. The portable Windows converter includes its own exact source.
Unrelated working changes have not been committed merely to make this release.
