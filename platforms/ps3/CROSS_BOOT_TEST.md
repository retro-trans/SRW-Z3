# PS3 boot isolation — tests 04 and 05

Based on your report: 01 and 02 load; 03 fails with **80010001**.
These two new images isolate the executable from all other translated files.
They are diagnostics, **not playable English releases or confirmed fixes**.

| ISO | Executable | All other files |
| --- | --- | --- |
| 04-SRW-Z3-English-EBOOT-Japanese-Data.iso | Exact English EBOOT from failing 03 | Exact Japanese files from working 02 |
| 05-SRW-Z3-Japanese-EBOOT-English-Data.iso | Exact Japanese wrapped EBOOT from working 02 | Exact English-build files from failing 03 |

No new wrapper, translation edits or executable fixes are introduced. The
non-executable files include fonts, dialogue, UI/art, battle data and trophies.
The existing 01/02/03 images remain untouched. New images contain the same
554 paths, verified through both ISO9660 and Joliet trees.

## Test procedure

1. Transfer both **full, unsplit** ISOs to `/dev_hdd0/PS3ISO/` using the same
   method as working 02. They exceed FAT32's single-file limit; do not place
   the unsplit files on a FAT32 USB drive. Compare sizes/checksums after
   transfer when your transfer tool supports it; see `SHA256SUMS.txt`.
2. Use the same manager, mount settings and console setup as tests 01–03.
   Do not change firmware or clear/delete game data, trophy data or saves.
3. Mount **04**, launch the mounted disc icon, and record whether the immediate
   **80010001** error appears. If it starts, record the farthest screen reached.
4. Close the game, unmount 04, then repeat with **05**. Select by exact ISO
   filename: the game bubble/title ID is shared between these tests.
5. **Stop at the title screen. Do not start gameplay, load saves or save.**
   Fonts and text encoding intentionally do not match the executable in these
   crossover images. Garbled/missing text or later crashes are possible and
   are not equivalent to the immediate launch error we are isolating.

Copy only the two ISOs and this README/checksum file. `intermediate_disc` and
the audit are local build records, not additional files to install on the PS3.

## What to report

For each exact filename: mounts successfully? same immediate 80010001?
first visible screen? title screen? later freeze/error? Include an error photo.
Also record the manager and CFW/Cobra versions if available; do not update them.

Interpret the following specifically for the **immediate 80010001 failure**:

- **04 fails, 05 gets past that error:** the English executable is implicated;
  inspect its loader headers/segments and then narrow its patches.
- **04 gets past it, 05 fails:** the translated non-executable files or their
  packaging are implicated; split those file groups next.
- **Both fail:** check transfer integrity, differing failure stages and the
  deliberately mismatched executable/data combinations before assigning blame.
- **Both get past it:** the combined build, interaction between changes, or
  the transferred 03 image needs further investigation.

None of these outcomes alone proves complete gameplay or save compatibility.
After the test, unmount the diagnostic ISO and return to working 02/original.

## Local rebuild

The builder pins the previous audit and hashes both complete source images.
It refuses existing output folders, swaps only the two already-built EBOOTs,
and independently rereads all 554 files from both trees of each output.

```text
python platforms/ps3/cfw_cross_diagnostics.py --out work/NEW_CROSS_TEST_FOLDER
```

Inspect the dry run, then add `--write`. Requires the same Python/pycdlib
environment as `cfw_diagnostics.py`. No license or signing keys are needed.
