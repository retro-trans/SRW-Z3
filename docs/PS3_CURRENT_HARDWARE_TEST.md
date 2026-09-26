# Current-source PS3 hardware test

This local candidate contains the current translation edits, rebuilt together
with their shared fonts and executable. It is not the frozen 0.6.14 release.
The build number is in the ISO filename and title footer. Remaining untranslated
mission variants are recorded in HARDWARE_TEST_AUDIT.json; this is not a claim
of complete translation or human proofreading.

The executable uses the existing guarded two-LOAD layout and fake SELF wrapper,
with original disc application metadata. Static checks preserve translated
code/data and verify every disc file in both ISO9660 and Joliet. These checks
do not prove console compatibility, boot, or gameplay. Each new build needs
its own runtime checks; this packaging is not for a stock PS3.

On 2026-09-19 the user confirmed that `0.6.15-hardware-test1` works after the
physical-PS3 test request. Firmware and gameplay coverage were not specified.
That exact ISO is the preserved hardware baseline; its identity and mandatory
future hardware/RPCS3 packaging workflow are in
[the PS3 build instructions](../platforms/ps3/README.md#required-dual-target-packaging-2026-09-19).
This report does not retroactively change the immutable build-time audit or
establish runtime success for every future build.

## Test using your existing console setup

1. Transfer the full `.iso` to `/dev_hdd0/PS3ISO/` using your existing method.
   It is larger than FAT32's single-file limit; no split parts are included.
2. Select that exact filename in your existing ISO manager, mount it, then
   launch the disc icon. Do not install it as a PKG or change firmware for this test.
3. Confirm the title footer build number. Test New Game, a copied save,
   dialogue/backlog links, menus, and one battle before relying on the build.
4. Report whether it mounts, boots, and reaches gameplay, or the exact error.
   Include your firmware/CFW or HEN and ISO manager versions if available.

Keep savedata intact. If a game-data corruption message appears, stop and
report it: game installation cache and savedata are different things, and
you should not delete savedata. Old images remain available for comparison.

`SHA256SUMS.txt` identifies the exact tested ISO. Intermediate folders and
loose executable files are build inputs, not separate installation packages.
Do not upload this full game image. No release, tag or publication was made.
