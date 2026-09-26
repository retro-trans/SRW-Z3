# PS3 CFW hardware-test packaging

This is a separate, **hardware-unverified** package, not a universal PS3 release.
It targets a console already running CFW with Cobra and fake-SELF support.
It does not work on unmodified retail firmware. Do not change firmware for this
test. RPCS3 accepting a file is not evidence that a physical PS3 will accept it.

## Why a separate package

The reported 0.6.10 image was rejected from `/dev_hdd0/PS3ISO/` as
`ENCRYPTED/INVALID ISO`; the console also showed launch error `80010017`.
The local legacy images contain a plain ELF in EBOOT.BIN, and the original
disc sector ranges stop before the appended translation data. Their UDF tree
also still refers to original extents. Those are packaging defects relevant
to hardware; they do not prove the only causes of the reported errors.

The CFW packaging tool starts from the verified original image plus a validated
build snapshot. It creates fresh ISO9660 and Joliet trees, retaining original
primary aliases and full Joliet filenames. It does not carry the stale UDF
tree into the new image. A single plaintext disc region covers the entire
finished ISO, including tail padding.

The patched ELF is enclosed in a debug/fake SELF using PSL1GHT fself. Original
disc application metadata and capability flags are retained. This is **not a
retail signature**. Verification checks the entire embedded ELF byte-for-byte,
every program segment mapping, the embedded headers and executable digest.
All other deployed files remain identical to the selected snapshot.

## Reproduce locally

Requirements: Python with pycdlib 1.15.0, GCC, an own-copy original disc with
MD5 `2cfedd95e5bdde49550cffa21c3c29a3`, and a validated build snapshot.
No game, license or signing-key download is performed.

Compile the MIT-licensed [PSL1GHT fself](https://github.com/ps3dev/PSL1GHT/tree/master/tools/fself)
at commit `f649a08fd536a9e27c08c7db2d93a2d7ee4c3bbe` into an ignored tools folder.
Keep the upstream license with any redistributed copy of its tooling.
The game ELF has no `.sceversion` section. In `tools/fself/source/self.c`,
inside `self_build_sceversion_header`, immediately after zeroing `info`, add:

```c
if (sce_idx < 0) {
    info->unknown1 = 1;
    info->size = 16;
    return;
}
```

This avoids dereferencing the missing section index and emits the basic version
record, as the companion make_self implementation does. No other upstream
source changes are required. With the checkout in `work/cfw_psl1ght`:

```powershell
gcc -O2 -I work/cfw_psl1ght/tools/fself/include work/cfw_psl1ght/tools/fself/source/main.c work/cfw_psl1ght/tools/fself/source/self.c work/cfw_psl1ght/tools/fself/source/tools.c work/cfw_psl1ght/tools/fself/source/sha1.c -o work/cfw_psl1ght/fself.exe
python -m unittest discover -s tools -p test_cfw_package.py -v
python platforms/ps3/cfw_package.py --source 'E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso' --build work/build_0.6.13_batched_ui --out work/cfw_0.6.13_test1 --fself work/cfw_psl1ght/fself.exe
```

Inspect the dry-run, then repeat the last command with `--write`. Output must
be a new directory under ignored `work/`; existing packages are never replaced.
The wrapper executable hash is recorded in `CFW_AUDIT.json`, along with all
554 file hashes, full ISO hash, part hashes and verification results. The audit
is written only after both filesystem trees and all split parts pass checks.

Disc region/header layout follows the open-source
[ps3netsrv implementation](https://github.com/aldostools/ps3netsrv/blob/master/src/VIsoFile.cpp)
and its `include/VIsoFile.h` structures (inspected commit
`158a829a30dd9c5bc61e851f1d3505e2db91b08a`). The `.iso.0`, `.iso.1`, ...
naming follows [webMAN MOD's supported game paths](https://github.com/aldostools/webMAN-MOD/wiki/Game-Paths-%26-Covers).

## Friend's test

### Three-build startup isolation (2026-09-15)

After the tester reported `80010001` with the CFW-test1 ISO, the user requested
all three controlled tests below. These use the same packaging/wrapper method,
not a speculative new fix. Original Japanese boot success is still an assumption
until the tester confirms it; exact CFW/Cobra versions remain unknown.

1. `01-SRW-Z3-Japanese-Repacked.iso`: all 554 files match the original disc,
   including its original SELF. Only the ISO packaging changes.
2. `02-SRW-Z3-Japanese-CFW-Wrapper.iso`: only EBOOT.BIN differs from test01.
   It wraps the existing pristine RPCS3-decrypted ELF, pinned to SHA256
   `d9b198be47421c7fd8725015ef23ea20e327d0b042234516b3d48ea56415f959`;
   ELF and program headers are checked against the original SELF. This baseline
   is not freshly decrypted by the diagnostic script. No translation hooks or
   translated assets are included.
3. `03-SRW-Z3-English-0.6.13-CFW.iso`: every game file must match the existing
   CFW-test1 audit, including its wrapped translated executable. New ISO
   timestamps can differ; this does not introduce a compatibility fix.

All outputs are **full unsplit ISOs** in a new folder. Existing artifacts,
emulator installations, saves and firmware are untouched. Every file is checked
through both ISO directory trees, and the test01/test02 one-file difference is
enforced before completion. The final `DIAGNOSTIC_AUDIT.json` records all three
inventories and full ISO hashes. The work folder also contains staging files;
send only the three ISOs and the README/checksum files.

```powershell
$env:PYTHONPATH='tools;platforms/ps3'
python -m unittest tools.test_cfw_package tools.test_cfw_diagnostics -v
python platforms/ps3/cfw_diagnostics.py --source 'E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso' --build work/build_0.6.13_batched_ui --out work/ps3_boot_diagnostics_20260915 --fself work/cfw_psl1ght/fself.exe --clean-elf work/EBOOT_dec.elf --previous-audit work/cfw_0.6.13_test1/CFW_AUDIT.json
```

Read the dry-run, then repeat with `--write`. An existing output directory is
refused. The shared preflight mentions the older builder's FAT32 parts; the
diagnostic override explicitly disables splitting and never calls that code.

Use the same manager/settings for each test and identify it by exact filename
(both Japanese controls retain the same XMB title/icon). Report mounting,
title-screen success and exact error separately. If test01 fails while the
original image boots, investigate packaging/transfer/mounting. If test01 passes
but test02 fails, investigate the wrapper, decrypted baseline and CFW support.
If both pass but test03 fails, investigate translated executable/asset changes.
Successful boot does not verify gameplay. Do not change firmware for these tests.

### Original CFW-test1 delivery options

- For FAT32 USB: copy **every** split part from the package's `PS3ISO` folder
  to `/PS3ISO/` on the USB. Keep names unchanged and all parts together.
  Each is at most 2 GiB. Refresh the manager's game list, mount this CFW-test1
  title (the first part if a file selection is needed), then launch its disc
  icon from XMB. Do not try to install these as PKG files.
- For internal HDD: transfer the single full ISO to `/dev_hdd0/PS3ISO/`, for
  example using the console's existing FTP facility. Use the full ISO there,
  not both representations in the same location. No USB format change needed.
- Do not copy `intermediate_disc` or `fself_generated.bin`; they are local
  build intermediates. Leave saves, firmware and the existing RPCS3 install
  untouched. Keep the earlier image as a fallback, but make sure the mounted
  filename explicitly contains `0.6.13-CFW-test1`.
- Report the exact CFW/Cobra and manager versions, whether mounting succeeds,
  whether the title screen appears, and any error code. After successful boot,
  check translated menus and the stage-10 ending/skip transition. Packaging
  checks cannot establish runtime stability of the existing translation hooks.

This test reuses 0.6.13 English without retranslating or changing its build
counter. Translation is still partial (1,034 untranslated mission variants).
There is no public release or upload. Distribute patches rather than game ISOs.
