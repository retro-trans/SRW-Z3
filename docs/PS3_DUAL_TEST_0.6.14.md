# PS3 0.6.14 dual-target test 1

This is a test candidate for RPCS3 and an already modified PS3 with compatible
fake-SELF loading (the existing CFW/Cobra setup used for earlier tests).
It is not retail-signed, does not work on stock firmware, and is not a blanket
HEN compatibility claim. No firmware changes are part of this package.

The same executable/data is intended for both targets. It preserves all
0.6.14 translations and fixes. Only the executable's loader layout and SELF
wrapper change; the other 553 disc files remain byte-identical to 0.6.14.
RPCS3's debug-SELF extraction path is verified against the wrapped payload,
but this alone does not establish runtime compatibility.

On 2026-09-18 the user confirmed that this build works in RPCS3. The extent
of gameplay testing was not specified. Physical-PS3 testing remains pending.

## Real PS3

Use `SRW-Z3-English-0.6.14-dual-test1.iso` from the local build folder. Copy
the full, unsplit ISO to `/dev_hdd0/PS3ISO/` using your existing transfer method.
Do not copy this over-4-GB file to FAT32 or install it as a PKG.
Mount it using the same manager/settings that loaded the prior working test,
then launch the disc icon. Keep the old working ISO for rollback.

Back up your saves first. Report whether it reaches the title screen, loads
a save, displays dialogue/link highlights, and runs a battle. Record the
firmware, CFW/HEN, manager version and any exact error. Test saving in a new
slot only after loading/gameplay work; do not overwrite your only good save.

## RPCS3

Use the same files, extracted as a disc folder, not an installable PKG.
For this workspace, the installer-compatible `snapshot` is intended for the
single existing `game` folder using `tools/install_build.ps1`, with RPCS3 closed.
The installer retains backups/cache and leaves saves untouched. Do not copy
just the new executable into an older translation build.

## Apply the xdelta (choose the matching source)

`SRW-Z3-English-0.6.14-dual-test1-from-original.iso.xdelta` accepts the
original Japanese BLJS10256 ISO, 4,431,872,000 bytes, SHA256
`1b45cdd1651b98fe24b544223488289790ae87d5f82f1db272285fb4e4dffa89`.
It produces the same target as the incremental patch below.

`SRW-Z3-English-0.6.14-to-dual-test1.iso.xdelta` accepts only the released
0.6.14 ISO, SHA256
`c15b65a87d35cb4f3478fba829b4f14e6307de96b64979fdbc400b1d25e02462`.
Apply with xdelta3 to a NEW output ISO; keep the source unchanged.
It is not an original-Japanese-to-English patch. The ready-built local ISO
does not need patching again. `SHA256SUMS.txt` records the output hashes.

In an xdelta patcher, select the matching source ISO, the patch file and a
NEW output ISO. Do not apply both patches consecutively. Expected output:
5,012,193,280 bytes, SHA256
`e2be81330cc2e45d8317271c8e290f7cde768749b4ea681114efd95b498c63c7`.

This candidate does not replace the published release until tests pass.

Technical references: [RPCS3 debug SELF loader](https://github.com/RPCS3/rpcs3/blob/master/rpcs3/Crypto/unself.cpp)
and [PSL1GHT](https://github.com/ps3dev/PSL1GHT). Console layout work reuses
the guarded project test-06 transformation, not a new translation build.
