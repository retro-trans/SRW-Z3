# PS3 test 06: English executable layout candidate

Use `06-SRW-Z3-English-Two-LOAD-CFW.iso` on the same existing CFW setup and
with the same mount settings that loaded tests 02 and 05.

1. Transfer the full ISO to `/dev_hdd0/PS3ISO/` with your existing transfer
   method. It exceeds FAT32's single-file limit. It is not a PKG.
2. Mount this exact filename, then launch the mounted disc icon.
3. First report whether it reaches the title screen or still shows 80010001.
4. If it boots, start a new game and check English dialogue, menus and one
   battle. Do not overwrite existing progress; use a spare save slot if needed.

Copy only the ISO, not the intermediate folder or generated executable files.
No firmware, plugin, license or installed-game changes are required by this test.
To stop testing, unmount this ISO and return to your previous known-working image.

## What changed

Hardware reports: 01/02/05 load; 03/04 fail with 80010001. This isolates the
immediate launch failure to the English executable under the tested settings.

06 keeps all 553 non-executable files byte-identical to 03. The executable
retains the English code, translation tables and their runtime addresses. Its
third nonempty memory region is folded into the native writable data region;
the original zero-initialized memory and translation scratch space remain zero.
The ELF section table is relocated outside mapped data. The same wrapper tool
and application metadata are retained. No mapped region is both writable and
executable. Translation tables become writable, but not executable.

This tests a plausible loader-layout issue, not a confirmed cause or fix.
Boot and gameplay compatibility still require testing on the physical PS3.
SHA256SUMS.txt and DIAGNOSTIC_AUDIT.json document the completed local checks.
