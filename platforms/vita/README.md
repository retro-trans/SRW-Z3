# Vita — PCSG00264

## Latest candidate: Vita3K link-background v3 (2026-09-17)

V2 was disproved by user testing: names still too wide and dialogue terms lost
their highlights. V3 fixes the separate name-widget width and translated-term
identity comparison. Backlog terms and date centering are retained. CPU tests
now execute the actual name widget and registration, not hand-filled keyword
records pretending to be names. All 53 unique tests pass; in-game retest pending.
Built installer: `work/vita/vita3k_linkfix_install_03/SRW-Z3-Vita3K-test16-linkfix-v3-install.zip`.
All 589 files verified (size, SHA256, CRC); only executable differs from test16.
Back up installation/saves, stop Vita3K fully, then install the ZIP directly.
See its adjacent README-INSTALL.md. No automatic installation.

## Superseded: Vita3K link-background v2 (2026-09-17)

Use `work/vita/vita3k_linkfix_install_02/SRW-Z3-Vita3K-test16-linkfix-v2-install.zip`.
The user confirmed the problem persisted with v1 installed: it missed the primary
fixed-column highlight path. V2 uses the matching rendered link's X/Y and width
for that path, retaining the prior secondary-path and date-card corrections.
Seven focused tests plus42 UI/date regressions pass, including reproduction of
the old overwide Kei highlight. All589installer files verified. In-game retest
is still required; no automatic installation or save changes.
Back up app/saves, choose File > Install .zip, .vpk and select the ZIP directly.
Follow the adjacent README-INSTALL.md. Earlier v1 archives below are superseded.

## Vita3K installable link/date package (2026-09-17)

`work/vita/vita3k_linkfix_install_01/SRW-Z3-Vita3K-test16-linkfix-install.zip`
is the complete Vita3K-installable package (1,872,598,785 bytes). Select it
directly through File > Install .zip, .vpk; do not extract it. Back up the
current installation and saves before accepting a reinstall prompt. See the
adjacent `README-INSTALL.md`; never delete savedata to install an update.
All 589 files passed size/hash/CRC verification. Only EBOOT differs from the
working full test16 ZIP, adding both link-width and date-centering fixes.
No auth/license/firmware/save material; not a physical-Vita package.
Not installed or visually tested. Builder: `build_link_background_install.py`
with `--output work/vita/NEW_FOLDER`, dry-run before `--write`.

## Test16 link-background update (2026-09-17)

`work/vita/link_background_test16_01/SRW-Z3-Vita-test16-link-background-update.zip`
fits selected backgrounds to rendered names/keywords such as Alto and ZEXIS.
It also retains all 77 date-card centering fixes. For existing working test16,
with or without the earlier date-only update; not for a newer/different build.
Its `README-INSTALL.md` covers backing up and replacing ONLY the EBOOT on
physical rePatch or Vita3K, keeping current auth/fonts/assets/saves untouched.
All 46 tests pass: four new CPU tests (all 256 slots and independent relocations)
plus 42 existing date/UI/screenshot regression tests.
ZIP read-back passes; no automatic install or in-game visual verification.
Builder: `python platforms/vita/build_link_background_patch.py --output work/vita/NEW_FOLDER`
(inspect dry-run, then add `--write`). Future `ui_text.prepare` builds with
native-name support include it. Defeat-condition/Z Chips/menu fixes remain pending.

## Test16 date-card centering update (2026-09-17)

`work/vita/date_centering_test16_01/SRW-Z3-Vita-test16-date-centering-update.zip`
is a small EBOOT-only update for existing working test16 installations.
See its `README-INSTALL.md` for physical rePatch/Vita3K backup and rollback.
It centers all77 translated date cards without changing their font size or
vertical position. 42 automated tests pass; visual in-game retest is pending.
It is not installed automatically and does not fix the separately reported
defeat-condition, Z Chips footer or intermission alignment issues.
Builder: `python platforms/vita/build_date_center_patch.py --output work/vita/NEW_FOLDER`
(inspect dry-run, then add `--write`). Future `ui_text.prepare` builds include
the same scoped fix; the update ZIP itself is based only on the pinned test16.

## Physical Vita: rePatch test16 hardware-test package (2026-09-17)

See [physical-Vita preparation, installation and rollback](REPATCH_INSTALL.md).
`build_repatch.py` packages only the 120 changed test16 game files, excluding
the five emulator-converted modules, unchanged content, metadata and licenses.
The completed package is `work/vita/english_repatch_test16_02/`
`SRW-Z3-Vita-rePatch-test16-hardware-test.zip` (94,279,737 bytes).
It adds a validated, sanitized 144-byte auth file from the user's local dump:
only authority ID and capability/attribute fields are retained, with padding
and shared-secret fields zeroed. The raw input remains private and unchanged.
All 123 ZIP entries passed size/SHA256/CRC checks (121 payloads plus two docs).
No physical Vita has been tested, no device changed, and test16 EBOOT/content
are unchanged. The older `NEEDS-SELF-AUTH.zip` remains incomplete; use the new
hardware-test package instead. Target remains PCSG00264 v01.00 with compatible
rePatch; firmware/plugin versions are not yet known.

Latest emulator package: **test16**; see [test instructions](VWF_TEST_ZIP.md).

## Earlier: broad VWF test 01 (2026-09-14)

Built complete ZIP: `work/vita/english_vwf_test_01/SRW-Z3-Vita-English-VWF-test-01.zip`
(1,874,654,431 bytes). See [test instructions](VWF_TEST_ZIP.md).
Matching native VWF/UI executable, single-letter fonts,42,742story records,
31,666battle subtitles,1,510UI keys plus libraries/keywords/gameplay terms.
All116 rebuilt CPKs and589 packaged files passed readback;89focused tests pass.
Not installed or runtime-tested. Incomplete UI/art/layout/suspend categories
are documented; this is a development test, not a finished full port.

Builder: `python platforms/vita/build_vwf_zip.py --output work/vita/NEW_FOLDER`,
inspect dry-run then add `--write`. Original files and older builds preserved.

## Earlier fixed-cell pilot (preserved)

Status: user screenshot confirms the complete English pilot reaches opening
dialogue in Vita3K, but its paired/fixed-cell font is not VWF. A real VWF port
is now implemented as a source/development candidate; CPU tests pass, emulator
runtime/visual testing is still pending. See [VWF.md](VWF.md). NOT a full port.
The existing install ZIP below is unchanged and still uses the old font.
Use [INSTALL_ZIP.md](INSTALL_ZIP.md) for direct ZIP installation; no original
PKG installation or separate patch required for this complete package.

Complete ZIP: work/vita/english_pilot_01_install/
SRW-Z3-Vita-English-pilot-01-install.zip (1,874,630,556 bytes).
589 files: 3 English CPKs, 6 decrypted executables, 580 unchanged base files.
All 30 decoded executable segments preserved; all ZIP hashes/CRC verified.
No license/PFS metadata, firmware or saves; existing inputs and PS3 untouched.
45 focused tests pass. Build: `python platforms/vita/build_install_zip.py`,
inspect dry-run, then add `--write` for a new output folder.

The earlier three-file overlay below is still available for an existing base;
it is NOT the complete install ZIP. See [TEST_BUILD.md](TEST_BUILD.md).

Test output: `work/vita/english_pilot_01_checked/` contains the overlay ZIP,
three changed CPKs, font proof and BUILD_AUDIT.json. All 244 records in stage
0001A/B match shared source identities exactly; English decodes back exactly.
The script's other bytes (events, keyword IDs, speakers, skip flow) are unchanged.
Font pages 1/3 are Vita-native linear P4 GXT, independently inspected: glyph
anchors establish the grid, only 488 unassigned blank cells are modified, and
headers, palettes and every other cell remain intact. Adaptive Latin pairs
avoid overwriting Greek, symbols or Japanese. No PS3 texture or executable
bytes are reused. This prototype uses fixed-cell text, not the PS3 VWF patch.
Maximum encoded width is 28 cells including conservative name placeholders;
four-line/30-cell limits remain provisional until actual Vita3K testing.

Build dry-run: `python platforms/vita/build_test.py`. Add `--write` only for a
new output directory. Installer: `python platforms/vita/install_test.py --game
"PATH/ux0/app/PCSG00264"`, inspect dry-run then add `--write` with Vita3K closed.
Installer checks all base/build hashes before writes, preserves backups and
rolls back interrupted copy errors. It never changes EBOOT, licenses or saves.
35 focused tests passed (18 Vita, 12 shared-platform, 5 CPK ITOC).

The inspected `SRW Z3.1 Vita.pkg` is Jigoku-hen, PCSG00264, version 01.00.
Its inventory includes 176 CPK archives, 189 GXT textures, TPACKVITA.CPK,
AIDDataPack.cpk and matching stage/library families. The five MtData archive
sizes match PS3 originals; that is not proof of matching contents. Outer
PKG decoding alone leaves game payloads PFS-encrypted. On 2026-09-14, user authorized local license validation:
the 512-byte work.bin matches the PKG's FULL content ID for PCSG00264, has
the expected NoNpDrm header/account marker, and contains a nonzero key.
The PKG length matches its header. Keys/account IDs were not printed, saved
in reports, or uploaded. That initial check was structural only. The subsequent
authorized offline PFS decryption succeeded, including metadata/signature and
keystone checks. Output: `work/vita/decrypted_PCSG00264`.
Independent audit: `work/vita/decryption_audit.json`, with SHA-256 for 589 files,
176 readable CPK archives (35,861 indexed members) and 189 GXT signatures.
Three opening-stage members decompress successfully; their translation
record mappings were subsequently verified during the test build. Source EBOOT
remains encrypted; the complete ZIP converts it and five modules into plain
SELF containers with every decoded segment checked. The user's screenshot
subsequently demonstrates opening dialogue; later gameplay remains unverified.

The read-only checker is `platforms/vita/validate_license.py`:

```powershell
python platforms/vita/validate_license.py --pkg 'E:/SRWZ3/iso/SRW Z3.1 Vita.pkg' --license 'E:/SRWZ3/iso/work.bin'
```

After inspecting the output, optional `--report work/vita/license_validation.json`
saves only that non-secret report and refuses overwrite. Five synthetic tests
cover matching/mismatched IDs, malformed headers, absent keys and redaction.

Offline route identified: [Vita3K's parser](https://github.com/Vita3K/psvpfsparser)
contains `F00DNativeKeyEncryptor` and a native factory backend, unlike the
older motoharu-gosuto master that requires an online service or existing key
cache. A locally compiled isolated adapter used only that native backend.
See [DECRYPTION.md](DECRYPTION.md) for provenance, commands and limitations.
No additional license or third-party key service was needed.

## Shared opening-stage pilot

From the repository root:

```powershell
python platforms/vita/prepare_translation.py
# Read the dry-run samples before writing:
python platforms/vita/prepare_translation.py --write
```

This reads the existing shared English/glossary, checks stamped Japanese
identities and glossary resolution, and prepares 3 candidate script members
(opening stage 0001A and both 0001B dialogue members). Generated review output
is `work/vita/initial_translation.json`, NOT an installable patch. It contains
expanded English and source identities, not a second editable translation set.
Regenerate after changing shared content. The preparation helper alone does not
prove source compatibility; build_test.py now checks the three actual Vita
members against the canonical records on every dry-run/build.

`match_records()` is the adapter gate: it requires exact Japanese
text, fingerprint, event, ordinal and speaker, rejects missing/extra/ambiguous
records, and never silently falls back to PS3 source. The build audit records
the actual 244-record source comparison separately from synthetic tests.

## Next required steps

**Broad category source adapters (2026-09-14):** see [COVERAGE.md](COVERAGE.md)
for the 42,742-record story pass, 16 suspend lines, three libraries, actual
keyword popups, gameplay names, and 31,666 battle subtitles. These rebuild and
verify category content. UI/help now has a CPU-tested 1,510-key native hook,
still needing menu-path/layout verification. These adapters now feed the
new VWF test ZIP above; no emulator installation has been performed.

1. Preserve the verified local PFS output, original PKG/license and older builds.
2. Install the COMPLETE patched ZIP in Vita3K. Check New Game boot, actual
   glyph spacing, links, Back Log and skipping; no runtime success assumed.
3. Runtime-validate the native VWF candidate and broader source adapters;
   finish menu/help/graphics bindings and category-specific layout checks.
4. Physical Vita support remains separate and unverified.

Complete ZIP and earlier overlay are both built. No emulator install or runtime
test has been performed. Existing PS3 game files and releases are untouched.
