# English patch for a physical PS Vita — test16

Target: Japanese **PCSG00264, version 01.00**. This is a development patch,
not a standalone game or VPK. Physical-Vita boot, performance and save/load
have not been verified. The translation content matches Vita3K test16.

## Before installing

- Have a homebrew-enabled Vita with VitaShell and a firmware-compatible
  rePatch plugin enabled. VitaShell alone does not enable game patching.
- Launch your own Japanese game successfully without this patch first.
  Check the game bubble's Information/version and title ID. Do not use this
  build with another title ID or an update newer than 01.00. Do not remove an
  installed update to force compatibility; request a matching build instead.
- Back up your saves and any existing `rePatch/PCSG00264` folder to your PC.
  Do not merge this test with another translation, mod or compatibility pack.
- Allow at least **250 MB of extra free space** on ux0 for the extracted
  patch, plus space for backups. Extract on the PC so the Vita does not need
  room for both the ZIP and extracted files.

## Authentication file: completed versus incomplete packages

A `hardware-test.zip` includes a validated, sanitized `self_auth.bin`.
If you have that package, skip the dump-preparation steps below. Do not replace
its sanitized auth file with the original raw dump. `FILES.json` must report
`hardware_test_candidate` and an empty `missing_files` list.

The raw dump can contain shared-secret/license information. Keep it private.
The builder preserves only the authority ID and capability/attribute fields
used by [rePatch's authentication hook](https://github.com/dots-tb/rePatch-reDux0/blob/master/repatch.c).
It zeros unused padding and the entire shared-secret region, including the
`klicensee` field defined by [VitaSDK](https://github.com/vitasdk/vita-headers/blob/master/include/psp2kern/types.h).
Your original file is never changed or included in the package. This behavior
is based on upstream rePatch 3.0; firmware/plugin compatibility still needs
checking on your setup.

A filename ending `NEEDS-SELF-AUTH.zip` is **incomplete; do not install it**.
rePatch's author specifies that modified EBOOTs should include `self_auth.bin`.
This hardware-generated game-authentication information is absent from the
emulator build. We do not invent a replacement or substitute a license file.
See the [author's release notes](https://github.com/dots-tb/rePatch-reDux0/releases/tag/3.0).

To supply it from your own installed game:

1. Confirm the unmodified PCSG00264 game is version 01.00 and runs normally.
2. Obtain FAGDec from its [official project build folder](https://github.com/TeamFAPS/PSVita-RE-tools/tree/master/FAGDec/build).
   Install its VPK with VitaShell. This is a separate diagnostic tool, not
   the English patch. Do not obtain game files or compatibility packs from
   third-party download sites.
3. In FAGDec select PCSG00264 and use its SELF-format decryption workflow.
   The [documented workflow](https://github.com/TheRadziu/NoNpDRM-modding/wiki#eboot-modding-andor-running-365-games-on-360-and-365)
   selects the game with X, selects DECRYPT ALL (DONE), returns with Circle,
   then uses START / Decrypt modules in list / START DECRYPT (SELF).
   If your menus differ or it errors, stop and send a screenshot.
4. Find the `self_auth.bin` produced for **this game's base EBOOT** under
   `ux0:FAGDec/` (normally in `app/PCSG00264/`). Copy that file to the PC and
   keep it locally for build validation; do not upload or post it. For this
   workspace, place it as `self_auth.bin` in the repository root, which is
   ignored by Git. Keep the accompanying original decrypted
   EBOOT locally in case the loader format needs comparing. Do not send
   `work.bin`, `.rif`, account credentials, or your full game folder.
5. We will check the 144-byte file's structure and matching authority ID,
   sanitize unused sensitive fields and produce a hardware-test ZIP.
   Those checks cannot establish
   the dump's provenance: it must actually come from PCSG00264 v01.00.

If you already have a completed `hardware-test.zip`, this preparation step
was performed for that build. Check `FILES.json`: `missing_files` must be
empty. A complete package is still not proof of successful hardware operation.

## Enable rePatch (only if not already enabled)

Use a version compatible with your actual firmware. The original reDux0
documentation lists 3.60–3.68; do not assume that old release supports every
newer setup. If uncertain, send your firmware version and plugin list first.

For a compatible setup using `ur0:tai/config.txt` as its active configuration:

1. Back up that configuration to your PC.
2. Obtain `repatch.skprx` from the [author's releases](https://github.com/dots-tb/rePatch-reDux0/releases)
   and copy it to `ur0:tai/repatch.skprx` using VitaShell.
3. Add `ur0:tai/repatch.skprx` as a single line immediately below the existing
   `*KERNEL` heading, keeping every other entry. Do not duplicate an existing
   rePatch entry or load multiple rePatch variants.
4. Reboot; if your homebrew setup requires reactivation after reboot, do that.

This is an example for that active configuration, not an instruction to replace
your entire config file. If both ux0 and ur0 have tai configuration files and
you do not know which is active, stop and ask before editing either one.
The [official rePatch instructions](https://github.com/dots-tb/rePatch-reDux0/wiki/Usage-(GENERAL))
describe the kernel-plugin and title-folder arrangement.

## Copy the completed English patch

1. Close the game completely and extract the **completed** hardware-test ZIP
   on your PC. Do not rename it to VPK or use VitaShell's Install command.
2. Connect VitaShell to your PC using its USB or FTP transfer mode. Confirm
   that the destination shown in VitaShell is `ux0:`.
3. If `ux0:rePatch/PCSG00264` already exists, back it up and rename it to
   `PCSG00264.backup-test16` (use a different unused backup name if needed).
4. Copy the extracted `rePatch/PCSG00264` folder into `ux0:rePatch/`.
   The final layout must be:

   ```text
   ux0:rePatch/PCSG00264/
     eboot.bin
     self_auth.bin
     CommonData/
     DATA/
   ```

   Do not accidentally create `rePatch/rePatch` or `PCSG00264/PCSG00264`.
   Copy the whole patch together: the executable and font/data files are paired.
5. Leave the original game under `ux0:app/PCSG00264` and any official game
   data untouched. Do not copy anything to `app`, `patch`, `sce_sys`, or saves.
6. Disconnect cleanly, then launch the existing Japanese game's bubble.
   There is no new English bubble; the game loads replacement files via rePatch.

## First hardware test

Start New Game and check the title, opening narration/dialogue and menus.
Play a battle; check both animation modes, then save to a **new spare slot**,
close the game and reload that slot. Test suspend/resume too. Keep your main
save backed up until these tests pass. Report missing text, loading delays,
crashes or save problems with the exact screen/error code, firmware version
and rePatch version. Do not treat successful boot alone as a complete test.

If it remains Japanese, check plugin activation and the exact folder nesting.
If it crashes or cannot save, disable the patch below before retrying the
unmodified game. Do not delete saves or reinstall the game as a first fix.

## Disable / roll back

Close the game. In VitaShell rename `ux0:rePatch/PCSG00264` to an unused name
such as `PCSG00264.english-disabled`. Launch the original Japanese game again.
To restore an earlier mod, rename its backed-up folder to `PCSG00264` instead.
No original game files are replaced by this installation method. Renaming
the patch does not undo saves created during testing; retain your backup.

## Build notes

The staging package contains 120 changed game files (118 CPKs, the paired
battle data file, and EBOOT), 213,967,924 bytes before ZIP compression.
A completed package adds a sanitized 144-byte `self_auth.bin` derived from
the console dump; no shared-secret bytes are retained.
All unchanged game files, five converted emulator-only modules, sce_sys,
license material, firmware and plugins are excluded. The test16 executable
and translations are copied byte-for-byte; no new executable wrapper or
console compatibility claim is introduced. Each packaged file has size,
SHA256 and ZIP CRC read-back checks. Instructions and a manifest are included.

Developer rebuild (from the repository root; Python dependencies as for Vita):

```text
python platforms/vita/build_repatch.py --output work/vita/NEW_FOLDER --self-auth PATH_TO_SELF_AUTH
```

Inspect the dry run, then add `--write`. The output must be a new directory.
`--allow-incomplete` explicitly creates a staging ZIP when no dump is available.
It never installs anything or reads a license. Generated packages remain local.
