# SRW Z3 Jigoku-hen save converter — RPCS3 ↔ Vita3K

> Maintenance note (2026-09-18): the maintained converter has moved to
> `../../retro-trans-tools`, under the **Z3 saves** tab. The integration is local
> and unreleased. Its bundled `retro_trans/resources/Z3-SAVE-CONVERSION.txt`
> contains current usage instructions. This document and the old standalone
> sources are retained for historical 0.6.14 packages; do not build or publish
> another standalone converter by default. Existing published assets are unchanged.

Offline tools only. No game, saves, account information or keys are included.
The portable Windows x64 app needs no Python installation. The separate
source-script ZIP requires Python 3.8 or newer; no extra Python packages.

Supports decrypted emulator saves for PS3 NPJB00520 and Vita PCSG00264.
It does not decrypt, resign, or directly install physical-console saves.
Unknown formats and damaged checksums are rejected. Conversion passes native
format/checksum and exact round-trip checks, but your converted saves still
need an in-game load/save/reload test. Keep your originals.

## Prepare

1. In EACH emulator, start this game and create system data and at least one
   ordinary manual save. These provide your own destination metadata templates.
2. Close both emulators. Back up the entire game save profile on both sides.
3. Extract the entire tool ZIP into a writable folder (for example Documents).
   Do not run the executable from inside the ZIP or move it away from `_internal`.

## Portable Windows app (no Python installation)

Download `SRW-Z3-Save-Converter-0.6.14-Windows-x64.zip` and extract ALL files.
Double-click `SRW-Z3-Save-Converter.exe`. No administrator rights are needed.
Select the two save folders described below, confirm both emulators are closed,
then click **1. Check saves**. Review the slot mappings and click
**2. Convert both directions**. Click **Open output folder** when it finishes.
Each conversion creates a new timestamped folder under `work` beside the app;
nothing is installed into an emulator automatically. If access is denied,
move the complete extracted app folder to a writable location and try again.

This is an unsigned community tool. Verify the download against the supplied
SHA-256 checksums. Do not disable antivirus or Windows security features.
The app operates offline and never uploads your saves. Tested on Windows x64;
this download is not a macOS/Linux or 32-bit Windows application.

The PS3 input is the `savedata` directory containing `NPJB00520-SYS` and
`NPJB00520-STG-*`, commonly `RPCS3/dev_hdd0/home/00000001/savedata`.
The Vita input is the `PCSG00264` save directory beneath your configured
Vita3K storage's `ux0/user/00/savedata` (user number may differ).
Do not point either input at the game's installation directory.

## Source-script alternative (Python required)

If using the Python source ZIP instead of the Windows app, open a terminal
in the extracted folder and follow these commands.

Replace the example input paths with your own. First run without `--write`:

```text
python tools/convert_z3_saves.py --ps3-save-root "D:/RPCS3/dev_hdd0/home/00000001/savedata" --vita-save-root "D:/Vita3K/ux0/user/00/savedata/PCSG00264" --output work/converted
```

Read the reported slot mappings. Run the same command with `--write` added
to create both directions in a NEW `work/converted` folder inside this tool
directory. If that folder already exists, choose a new name. Nothing is
installed automatically and neither input is modified.

- `rpcs3-to-vita3k.zip`: PS3 progress for Vita3K.
- `vita3k-to-rpcs3.zip`: Vita progress for RPCS3.
- `original-backups`: untouched original data; KEEP PRIVATE.
- `CONVERSION_AUDIT.json`: checksums and mappings; may include private metadata.

These are profile conversions, not a merge of two playthroughs. System data
includes settings and global progress. Suspend/Continue must be tested
separately; a system summary does not create a missing manual save.

## Import and verify

With the destination emulator closed, move its existing game save folders
to a backup OUTSIDE `savedata`. Leave other games alone.

For Vita3K, place the converted `PCSG00264` folder directly under
`ux0/user/00/savedata`; do not nest it twice.
For RPCS3, copy the converted `NPJB00520-*` folders from the package's
`savedata` directory into your user's `savedata` directory.

Load each converted manual slot, compare chapter, route, funds, units and
pilots, then play a battle. Save to a spare slot, close the emulator, restart
and reload. If anything is wrong, close it and restore your complete original
game profile. Do not overwrite your only backup.

## Checks

Only the native size field (bytes 4–7) changes byte order in STAGE.BIN and
SYSTEM.BIN. Progress bodies and stored checksums are preserved. Destination
metadata comes from your own existing saves. PS3's zero-based manual directory
indices are mapped to Vita's one-based indices.

Run the included synthetic tests with:

```text
python -m unittest discover -s tools -p test_save_conversion.py
```
