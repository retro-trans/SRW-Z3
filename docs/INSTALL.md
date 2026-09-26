# Installing the English patch

## Current release: PS3 English 0.6.21

Download [Retro Trans](https://github.com/retro-trans/retro-trans-tools) and use
Automatic mode with a refreshed catalog. Select your own Japanese BLJS10256 ISO
or the exact previously patched 0.6.19 ISO, then choose a new output filename.
The catalog verifies the input and chooses the matching patch for 0.6.21.
Keep your original image. Do not apply both patches in sequence.

For manual installation, use the [0.6.21 release](https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.21)
and [its exact filenames, input/output hashes and runtime limitations](releases/0.6.21.md).
This release contains whole-ISO patches only, not a per-file installation ZIP.
It reissues the existing English build; later source corrections and Vietnamese
work are not included. Back up saves and close RPCS3 before replacing game files;
follow the release notes for handling the game's stale installation cache.

## Historical installation guide (0.6.3-era packages)

The examples and coverage below describe withdrawn historical packages, not
the current download names, coverage or hardware packaging. Retained for
reference only; use the current release notes above for 0.6.21.

**Physical PS3 warning (2026-09-14):** the legacy RPCS3 ISO packages are not
console-validated. Local 0.6.3/0.6.10 images have plain-ELF EBOOT packaging and
stale disc-region/UDF metadata; 0.6.10 was reported rejected on CFW. Do not
treat the instructions below as a hardware compatibility claim. A separate
[CFW hardware-test workflow](../platforms/ps3/CFW_TEST.md) rebuilds the disc
and executable wrapper, with FAT32 split files. Actual PS3 boot remains
unverified until the hardware tester confirms it.

Two ways to install. **Option A is one file, one command**; Option B is
for folder dumps. Both need your own dump of the disc -- the patches hold
no complete game files. Distribute patches only, never either ISO.

## Option A -- one xdelta for the whole disc image (recommended)

You need: your own ISO of **第3次スーパーロボット大戦Z 時獄篇** (PS3,
`BLJS10256`, Japanese retail), `xdelta3`, and RPCS3.

The patch only accepts the retail image -- check yours first:

    MD5 of the original ISO:  2cfedd95e5bdde49550cffa21c3c29a3   (4,431,872,000 bytes)

1. Download `SRW-Z3-English-<version>.iso.xdelta` from the release.
2. Run (Windows shown; on Linux/macOS use `xdelta3` from your package manager):

   ```
   xdelta3-3.1.0-x86_64.exe -d -s "Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso" SRW-Z3-English-0.6.3.iso.xdelta "SRW-Z3-English.iso"
   ```

   The result is a full patched image. See this version's release notes for
   its expected size and hashes. xdelta3 refuses any source that is
   not the exact original, so a wrong image fails cleanly.
3. In RPCS3, boot the patched ISO (File > Boot > Boot Game, or add its
   folder to the game list). If you had the Japanese game installed before,
   close RPCS3 and **move `dev_hdd0/game/BLJS10256_DATA` to a backup location** first --
   it is a stale copy of the disc data and the game reports corrupted data
   while it is there; it is rebuilt on the next boot.

The patched image keeps every original sector in place and appends the
translated files at the end (their directory entries are repointed), which
is why a compact patch covers a 4.4 GB disc. xdelta3 for Windows:
https://github.com/jmacd/xdelta-gpl/releases

### Updating from the previous version

If you already have the previous release's patched image, download the
update patch `SRW-Z3-English-<prev>-to-<version>.iso.xdelta` instead and
apply it to THAT image (not the original):

    xdelta3 -d -s "SRW-Z3-English-0.6.1.iso" SRW-Z3-English-0.6.1-to-0.6.3.iso.xdelta "SRW-Z3-English-0.6.3.iso"

The result is byte-identical to Option A's output (same MD5), so either
route gives the same disc. With RPCS3 closed, back up `dev_hdd0/game/BLJS10256_DATA` before
booting the new image, as above.

## Option B -- per-file patches for a folder dump

You need: a folder dump (`PS3_GAME/USRDIR/EBOOT.BIN` inside), `xdelta3`,
Python 3 for the helper script, and RPCS3.

### Steps

1. Download the release zip and unzip it. Inside: `from-original/` (one
   `.xdelta` per game file), `MANIFEST.txt` (the MD5s), `apply_xdelta.py`,
   and this guide.
2. Open a terminal in the unzipped folder and run:

   ```
   python apply_xdelta.py --dump "D:\Games\Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan)\PS3_GAME" --xdelta "C:\path\to\xdelta3-3.1.0-x86_64.exe"
   ```

   Point `--dump` at your dump's `PS3_GAME` folder. The script checks every
   file before touching anything, patches into a temporary file, verifies
   the result, and keeps each original as `<name>.orig`. Add `--dry-run`
   first if you want to see the plan without changing files.
3. **Close RPCS3 and move its install cache to a backup location**:
   `dev_hdd0/game/BLJS10256_DATA` inside
   your RPCS3 folder. The game keeps a copy of the disc data there; if it
   is left over from before patching, the game reports
   「ゲームデータが壊れています」 (game data corrupted). Moving the folder
   makes the game reinstall it on the next boot (one button press).
4. Boot the updated folder, not an older ISO in RPCS3's game list.
   Patch all files together; the font and translated text must match.
   Do not move or delete anything under `dev_hdd0/home/*/savedata`.

### Applying by hand (no Python)

For each `from-original/<name>.xdelta`, find `<name>` in your dump
(`EBOOT.BIN` in `USRDIR`; the rest under `USRDIR/DATA/...` -- the
locations are listed in `apply_xdelta.py`) and run:

```
xdelta3 -d -s <original file> <name>.xdelta <patched file>
```

then replace the original with the patched file. `MANIFEST.txt` gives the
MD5 of every original and every patched file so you can check both.

## What is translated in this release

- 83 of 116 story scripts, plus all 26 intermission/route archives.
- All 211 battle voice-line sets (every unit's in-battle barks).
- Menus, unit / pilot / mech status screens, upgrades, parts, spirit,
  skill and special-ability lists and their descriptions, the Combat
  Record, the Lecture Plate tutorials, and the character / robot library.
- Unit, pilot, weapon, spirit, skill and part names.
- Victory, defeat and SR conditions in the included stages; weapon effects,
  unlock/reward notices and all 78 terrain names across 64 maps.
- Further translations and alignment fixes for Tag Commands, Maximum Break,
  team/status screens, library/network menus, search/settings and reports.

The English title logo and Library menu are included. All 193 original named
Library CV credits are romanized; 215 original no-credit entries remain `---`.
Still incomplete: 33 story scripts and 1,034 mission-text variants in the
broader 142-archive audit. This is not a 100% translation.

0.6.3 passed automated partial-coverage, binary-integrity, text-width and
centering checks. A full in-game playthrough and runtime visual confirmation
of this combined build remain pending. No gameplay conditions were changed.

## Troubleshooting

- **"game data corrupted" on boot** -- with RPCS3 closed, back up
  `dev_hdd0/game/BLJS10256_DATA` and boot again.
- **`apply_xdelta.py` refuses a file with an MD5 mismatch** -- that file is
  not the Japanese retail version, or was patched before. Restore it from
  `<name>.orig` (or from your original dump) and retry.
- **Black screen right after boot** -- RPCS3 auto-updates frequently; if a
  boot that worked yesterday goes black today, try the previous RPCS3
  build (RPCS3 keeps it in `rpcs3_old/`).
- **Undo** -- put the `<name>.orig` files back in place of the patched ones
  and move the install cache aside again with RPCS3 closed. Preserve saves.
