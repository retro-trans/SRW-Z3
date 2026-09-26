# Full terrain-label audit — 2026-09-09

Prepared candidate: `work/out_all_terrain_20260909`. **Not deployed.**
It extends `work/out_message_classes_20260909` and includes every prior
pending translation/layout fix.

Scanned every available attribute file, `MAP_001.ZLD` through `MAP_064.ZLD`:
64 files, 552 terrain records, 78 distinct names. This includes later maps,
the unnamed placeholder, and spelling variants such as both Industrial 7
forms and both Japanese Wasteland spellings. The original five labels are
retained; 73 terrain-only translations and centering pads were added.

## Scope isolation

Names such as Sea, Forest, Axis and Kurogane-ya also have non-terrain lookup
entries. Those original entries are left byte-for-byte intact. New map
copies replace only the relevant 28-byte name fields with short, unique
fullwidth keys (`地０００` etc.), which select the terrain translation and
its live-width centering pad. No new translation globally claims those
shared Japanese names.

The original four parameter bytes in every record, file headers, record
counts and entire tile-index grids are unchanged. The parser validates
their sizes and bounds instead of scanning arbitrary binary text.
Pristine map copies and their source hashes are retained under
`work/orig/MAPATTR`; do not replace them with translated map copies.

All 64 prepared map files are included with EBOOT in the build manifest and
deployment layout. A later deployment must use the complete candidate,
not copy EBOOT alone. Legacy candidates lacking maps are now rejected by
the deployment tool. No deployment or emulator/save operation occurred.

## Verification

- All 78 names have translations and fit a conservative 300px terrain slot
  with 24px clearance at 28px glyph size. Long labels use abbreviations.
- 10,740 emitted-PPC centering cases and 192 centered dialog hooks pass.
- All 179 reserved padding cells are blank in both existing font layers;
  no font or texture file was changed.
- Neighboring non-terrain glyphs still follow their original VWF path.
- Removing a terrain translation intentionally makes the coverage check fail.
- The full regression suite, compilation and all 95 manifest hashes pass.
- All 27 previous non-EBOOT game files are identical to the parent build;
  the 64 additional map files have audited name-field-only changes.
- Installed map hashes are unchanged. In-game visual verification is pending.

The appended terrain strings end at EXT+849d8 (exclusive); 46,632 bytes
remain. The VWF stub is 248 bytes, within its 256-byte slot. The old live-pad
indices are unchanged, with two additional verified blank-cell ranges.

Builder (dry-run default): `work/github_issues/build_all_terrain_20260909.py`.
The generated `terrain_audit.json` in the candidate records each original
name, terrain-only key, English label, map/record offset and source hashes.

EBOOT SHA256:
`4d797bdc270d93bcc3e2094db682f9b8fd5c1cf9b02750a0f28a709e2cdf391b`.
