# Physical PS Vita English patch 0.6.14 — rePatch hardware test

For the Japanese **PCSG00264, version 01.00** game on a homebrew-enabled Vita.
This is a partial English translation. It uses the current test16-linkfix-v4
content, including dialogue/backlog link fixes and centered date cards.
That content was tested in Vita3K; this exact combined hardware package has
not been verified on a physical Vita. Boot, performance, suspend and save/load
still need hardware testing. It is not a standalone game or a Vita3K installer.

## What to download and prepare

Download `SRW-Z3-Vita-Hardware-0.6.14-from-original.zip`. This contains deltas,
the preparation scripts and this guide, NOT files to install directly.

You need:

- Your own Japanese PCSG00264 v01.00 installed and launching normally on Vita.
- VitaShell and a firmware-compatible rePatch plugin already enabled.
  VitaShell by itself is not enough. Follow the plugin author's
  [installation guidance](https://github.com/dots-tb/rePatch-reDux0/wiki/Usage-(GENERAL)).
  Do not replace your entire tai configuration, duplicate kernel entries, or
  mix different rePatch variants. If unsure about firmware compatibility, ask.
- A PC copy of the original PFS-decrypted PCSG00264 v01.00 game folder.
  It must contain `eboot.bin`, `DATA` and `CommonData` directly. This is the same
  original source format required by this release's Vita3K from-original patch.
  A retail PKG, encrypted PFS directory, patched app or independently rewritten
  SELF executable will not match. The tool checks every required source hash
  and will stop instead of guessing. It does not decrypt games or handle licenses.
- A matching `self_auth.bin` from your own game. An existing working test16
  rePatch auth file can be reused. Otherwise, use your own game's base-EBOOT
  dump from FAGDec's SELF decryption workflow; see the
  [documented workflow](https://github.com/TheRadziu/NoNpDRM-modding/wiki#eboot-modding-andor-running-365-games-on-360-and-365).
  The file is normally under `ux0:FAGDec/app/PCSG00264/`. Keep the original
  decrypted EBOOT alongside your private dump in case format comparison is needed.
  Do not share the auth dump, work.bin, .rif, license keys or account credentials.
- Python 3.8+ and xdelta3 on the PC (not included). The no-Python save converter
  is a separate tool; it does not prepare game patches.
- At least 1 GB extra free space on the PC and 250 MB extra on Vita, plus backups.

If an official game update newer than 01.00 is installed, stop: this package
does not support it. Do not remove updates or delete game data to force a match.

## Build the hardware patch on your PC

Extract the download and open a terminal in its folder. Replace these example
paths with your own. Start with a read-only check:

```text
python apply_vita_hardware.py --source "D:/MyGame/PCSG00264" --self-auth "D:/Private/self_auth.bin" --output "D:/Z3HardwarePatch" --xdelta "D:/Tools/xdelta3.exe"
```

The output folder must not exist and must be separate from both the original
game and extracted patch package. After the check passes, repeat with `--write`:

```text
python apply_vita_hardware.py --source "D:/MyGame/PCSG00264" --self-auth "D:/Private/self_auth.bin" --output "D:/Z3HardwarePatch" --xdelta "D:/Tools/xdelta3.exe" --write
```

Wait for **SUCCESS**. A failed or interrupted output is incomplete: do not copy
it to Vita. Fix the reported input problem and retry using a new output folder.
The original game and auth dump remain unchanged. No device is modified.

The result contains:

- `rePatch/PCSG00264/`: 120 patched game files and a sanitized `self_auth.bin`.
- `SRW-Z3-Vita-rePatch-0.6.14-hardware-test.zip`: the same completed local overlay.
- `FILES.json`: all output hashes, an empty missing-files list and hardware-test status.
- `README-INSTALL.md`: these instructions.

The auth sanitizer retains only the authority ID and capability/attribute
fields consumed by upstream rePatch 3.0. Padding and all shared-secret bytes
are zeroed. This follows [rePatch's hook](https://github.com/dots-tb/rePatch-reDux0/blob/master/repatch.c)
and the [VitaSDK structure](https://github.com/vitasdk/vita-headers/blob/master/include/psp2kern/types.h).
The [rePatch 3.0 release](https://github.com/dots-tb/rePatch-reDux0/releases/tag/3.0)
requires this information for modified EBOOTs. Shape/authority checks do not
prove dump provenance or guarantee compatibility with every firmware/plugin.
No authentication file is included in the GitHub download.

## Install with VitaShell

1. Close the game completely. Back up saves and any existing
   `ux0:rePatch/PCSG00264` folder to your PC.
2. If that patch folder already exists, rename it to an unused backup name
   outside the active title folder. Do not merge two translations/mods.
3. Transfer the completed `rePatch/PCSG00264` folder from your PC into
   `ux0:rePatch/` through VitaShell USB or FTP.
4. Confirm the final layout:

   ```text
   ux0:rePatch/PCSG00264/
     eboot.bin
     self_auth.bin
     CommonData/
     DATA/
   ```

5. Do not nest `rePatch/rePatch` or `PCSG00264/PCSG00264`. Copy the whole
   executable/font/data set together. Do not copy to `ux0:app`, `ux0:patch`,
   `sce_sys` or savedata; do not install the ZIP as a VPK.
6. Disconnect cleanly and launch the existing Japanese game's bubble.
   rePatch supplies replacement files; there is no new English bubble.

Unchanged files and all original modules come from your installed Japanese
game. The five emulator-converted modules are deliberately excluded.

## Test and roll back

Check New Game, dialogue and backlog names/terms, date cards and menus.
Play a battle with animations on and off. Save to a spare slot, fully close
the game, relaunch and reload. Test suspend/resume. Retain your main save backup.

If the game stays Japanese, check plugin activation and folder nesting.
If it crashes or cannot save, close it and rename only
`ux0:rePatch/PCSG00264` to an unused name such as `PCSG00264.english-disabled`.
Restore your previous patch folder if needed. Original game files are untouched;
renaming a patch does not undo saves, so keep the save backup too.
Report the screen/error, firmware and rePatch version. Do not delete saves or
reinstall the game as the first troubleshooting step.

Do not redistribute the complete game or private auth dump. Only the release
delta download is intended for distribution.
