# Jigoku-hen: RPCS3 / Vita3K converted-save test packages

These conversions target the existing English-patched emulators. They are
not signed PS3 saves or encrypted physical-Vita saves. Do not copy this Vita3K
folder straight onto a physical Vita. A physical-Vita restore needs a separate
backed-up save-manager workflow and testing.

No live saves have been installed or overwritten. Untouched originals are
preserved in `original-backups` beside the packages. Keep that folder private:
save metadata can contain account information. Do not upload it publicly.

## Which package?

- `vita3k-to-rpcs3.zip`: the Vita system save and manual slot 1 (after chapter 1),
  packaged as NPJB00520-SYS and NPJB00520-STG-000. The manual save has 44,632
  funds and 60 Z chips.
- `rpcs3-to-vita3k.zip`: the PS3 system save, manual slot 1 (after chapter 2),
  and manual slot 4 (chapter 4 route choice). The manual saves have 110,336 / 138
  and 27,098 / 546 funds / Z chips respectively.
- The PS3 system metadata references chapter 10. It is preserved, but this
  does NOT create a chapter-10 manual save or prove that Continue can resume it.

These are full source profiles, not a merge of both sets of progress. A system
save also carries settings and game-wide state. Never replace it without a backup.

## Test in Vita3K

1. Close Vita3K completely.
2. Back up the entire existing PCSG00264 save folder to an unused location.
   Current path on this PC:
   `C:\Users\Binh\AppData\Roaming\Vita3K\Vita3K\ux0\user\00\savedata\PCSG00264`.
3. Rename the existing folder to an unused backup name outside `savedata`, then
   place the converted `PCSG00264` folder under `savedata`. Do not nest it twice.
4. Start the game. Check slots 1 and 4, load each, and compare chapter, funds,
   pilots, units and route. Test a battle and save to a new spare slot; restart
   the emulator and reload. Check Continue separately, without assuming chapter
   10 is a resumable save.
5. If anything fails, close Vita3K and restore the entire original folder.

## Test in RPCS3

1. Close RPCS3 completely.
2. Back up all existing `NPJB00520-*` save folders from
   `E:\RPCS3\dev_hdd0\home\00000001\savedata` to an unused location.
3. Move those existing game folders outside `savedata` for an isolated test.
   Leave other games' saves alone. Copy the two converted folders from the
   package's `savedata` directory into RPCS3's `savedata` directory.
4. Start Jigoku-hen and load manual slot 1. It should show the Vita progress
   after chapter 1 with 44,632 funds and 60 Z chips. Test a battle, then save to
   a new spare slot, restart and reload. Check Continue separately if desired.
5. If anything fails, close RPCS3 and restore the original game folders.

## What was converted and checked

The decrypted save formats share little-endian serialized sections and two
16-bit additive checksums. Their native size field at offsets 4-7 differs in
byte order. Only those four bytes are reversed in STAGE.BIN / SYSTEM.BIN;
every progress byte, stored checksum and section offset is preserved. Each
file validates before and after conversion and converts back byte-for-byte.
Unknown versions, layouts and bad checksums are rejected, not repaired blindly.

PS3's manual directory index starts at zero; Vita's starts at one. Slot 0 on
Vita is system metadata. Display text is transferred between PARAM.SFO and
Vita3K's SlotParam files. RPCS3 destination account/other SFO fields and icons
come from its own existing save templates. Vita icon fields and other slot
settings come from its existing matching-kind templates. Timestamps use source
save-file modification times.

Local code evidence: pristine PS3 ELF checksum at VA0x176824; stage checker
0x17F20C, system checker0x17F2AC. Vita test16 checksum at0x810B47BC; stage checker
0x810B7860, system checker0x810B72EA. Both routines sum little-endian words and
exclude the last word of the supplied region. Stage checksum covers
0x440:0x47FFE; system checksum covers0xD8F8:0xDFFFE; summary checksum covers
0x44:0x43E. Header-size bytes are outside those regions, so no checksum rewrite
is necessary. This is narrower and more precise than generic save-cheat checks.

[Vita3K's AppUtil implementation](https://github.com/Vita3K/Vita3K/blob/master/vita3k/modules/SceAppUtil/SceAppUtil.cpp)
documents the SlotParam file storage. The actual game's samples use UTF-8
strings inside those fixed-width fields. Native checksum validation and
structural tests do not replace a real game-load/save test.

## Rebuild

Use `tools/convert_z3_saves.py` with `--ps3-save-root`, `--vita-save-root` and
`--output work/NEW_FOLDER`. It is dry-run by default; add `--write` to produce
new packages and backups. It has no installation mode. Do not run while either
emulator is saving; a source change during generation makes the build fail.
