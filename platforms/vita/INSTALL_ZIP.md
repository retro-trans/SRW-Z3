# English Vita opening-stage test — installable ZIP

This is a complete game archive for testing your own copy in Vita3K on PC.
You do NOT need to install the original PKG first or apply a separate overlay.
This replaces those earlier two-step instructions for this ZIP only.

1. Keep the official Vita firmware and font packages installed in Vita3K.
2. Choose File → Install .zip, .vpk (wording can vary by Vita3K version).
3. Select `SRW-Z3-Vita-English-pilot-01-install.zip`. Do not extract it first.
4. Launch PCSG00264 and choose New Game to see the opening English dialogue.

If Vita3K says the game is already installed, cancel and preserve any existing
installation/saves before replacing it. Do not remove a working setup blindly.

Only the opening-stage dialogue (244 records in 0001A/B) is translated in this
pilot. Menus, speaker names, battle UI and later stages remain Japanese.
This is NOT the complete PS3 English port. Boot and in-game rendering have not
yet been tested; archive checks cannot guarantee Vita3K gameplay compatibility.

Please report whether it boots and send a screenshot of the first English
dialogue. Also check keyword links, Back Log and dialogue skipping. On failure,
send the error/log and Vita3K version, but do not share your license/work.bin.

The archive contains 589 game files: three English dialogue/font archives,
six locally decrypted SELF executables, and 580 unchanged files. Every decoded
executable segment is preserved; no PS3 executable/font binaries are used.
No license, work.bin, firmware or saves are included. Originals are untouched.
This is a Vita3K test package, not a signed retail PKG or a PS3 ISO.

## Rebuilding in this workspace

Run `python platforms/vita/build_install_zip.py` for the read-only checks,
then repeat with `--write` after inspecting the plan. A new output folder is
required; existing builds are never overwritten. Dependencies: Python and
PyCryptodome 3.23.0 in the ignored `work/vita/python_deps` folder.

Public format references (downloaded 2026-09-14, exact SHA256 pins in builder):

- https://github.com/Vita3K/Vita3K/blob/master/vita3k/packages/src/sce_utils.cpp
- https://github.com/Vita3K/Vita3K/blob/master/vita3k/packages/include/packages/sce_types.h
- https://github.com/vitasdk/vita-toolchain/blob/master/src/self.h

ZIP installation structure follows Vita3K's `install_archive_content` in
`vita3k/interface.cpp`: `PCSG00264/sce_sys/param.sfo` identifies the game root.
Decrypted content omits `sce_sys/package` and `sce_pfs` to avoid a second PFS
decryption pass. The executable converter reads the existing local license
in memory only; no remote key service is used.
