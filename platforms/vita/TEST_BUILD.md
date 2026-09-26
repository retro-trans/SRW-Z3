# English Vita opening-stage test 01 — PCSG00264 / 01.00

For the newer COMPLETE patched ZIP, use [INSTALL_ZIP.md](INSTALL_ZIP.md).
It installs directly in Vita3K without a separate original PKG or overlay step.
The instructions below apply ONLY to the older three-file overlay.

Experimental Vita3K overlay, NOT a full English release or a standalone game.
Includes 244 dialogue records in the opening stage (0001A and 0001B), from the
same English/glossary as PS3. Menus, speaker names, battle UI and later stages
remain Japanese. Text rendering, spacing and boot still need runtime testing.
No PS3 executable/font binaries are copied; the Vita font is rebuilt in its
native format using only 488 originally blank, unassigned character cells.

## Install for testing

1. Install the original PCSG00264 01.00 PKG and its matching work.bin through
   Vita3K. Install the official firmware/font packages if not already present.
2. Start the unmodified Japanese game first. Confirm a New Game reaches the
   opening dialogue. If the Japanese game fails, fix the base installation
   first; this overlay contains no executable fixes.
3. Close Vita3K normally. Find the configured Vita3K storage folder, then
   `ux0/app/PCSG00264`. Do not select a PS3 folder or `ux0/user` (saves).
4. Use the repository's `platforms/vita/install_test.py` with that app path:

   `python platforms/vita/install_test.py --game "PATH/ux0/app/PCSG00264"`

   Inspect the three-file dry-run, then repeat with `--write`. It checks all
   original hashes before writing, makes a backup outside the game, and verifies
   installed hashes. It refuses unknown/already modified files. Do not drag this
   overlay ZIP into Vita3K's game installer; it is not a full installable game.
5. Launch the game and select New Game. Test the opening dialogue, keyword
   links, Back Log and skipping through both halves of stage 1.

The ZIP's `PCSG00264/DATA` contains ONLY three changed CPKs. No work.bin,
license, EBOOT, firmware or save files are included. Original package and source
files remain untouched. Please keep your base installation backup.

## What to report

- Whether the original Japanese base boots, then whether this overlay boots.
- A screenshot of the first English dialogue and any missing/overlapping glyphs.
- Whether keyword links, Back Log and dialogue skip work without a freeze.
- Vita3K version and any log/error if it fails. Do not share license files.

`font_proof.png` is a reconstructed atlas preview, NOT an emulator screenshot.
Four-line/30-cell checks use a provisional budget, pending real Vita3K results.
The build audit proves archive/control-byte integrity, not gameplay correctness.
