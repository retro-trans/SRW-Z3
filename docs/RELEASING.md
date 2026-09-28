# Build and release numbering

PS3 builds now require the [dual-target packaging workflow](../platforms/ps3/README.md#required-dual-target-packaging-2026-09-19):
use the hardware-wrapped snapshot for both console delivery and RPCS3, never
the raw-ELF intermediate. The user-confirmed hardware baseline is local .15;
this does not change previously published artifacts or authorize a release.

For future desktop-patcher distribution, also follow
[Retro Trans release preparation](RETRO_TRANS_RELEASES.md). Existing local build
and snapshot numbering below remains in effect. Standard manifest generation,
private testing and public catalog enrollment are separate steps; publication,
tags and uploads require an explicit user request.


## Public release: 0.6.22 (2026-09-28)

Published latest at2026-09-28T13:47:10Z, release398292582:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.22.
The explicitly requested release uses the existing public destination without
changing visibility. Exactly five assets: original/.21 whole-ISO patches plus
BUILD-MANIFEST.json, SHA256SUMS.txt and VALIDATION.json. Both local round trips,
uploaded digests and actual public downloads passed Retro Trans0.3.1 checks.
Catalog workflow36431167008 succeeded, commitdf0541dc; previous cached-catalog
refresh preserves immutable identities and selects both direct .22 routes.
Existing .21 assets are unchanged. Build source b1ee149, tag57a56ad includes
records/test maintenance. Wrapped snapshot installed,220 hashes verified,
26 saves unchanged. Local snapshot and per-file patches retained. No Vita/VI
game package or full-game upload. Preserved layout remains a PS3 hardware
candidate, and this exact build needs runtime confirmation. See release notes
docs/releases/0.6.22.md and checks/limitations docs/validation/0.6.22.md.

## Public reissue: 0.6.21 (2026-09-26)

**Current download policy:** at the user's later request, the .19->.21 upgrade
is withdrawn. The release retains four assets: the unchanged from-original
xdelta and its three updated metadata files. The catalog likewise exposes only
the original route. Earlier two-route publication checks below are historical.
Existing clients with that two-route catalog cached must reset it to accept
this authorized withdrawal; no runtime validation rules were changed.

Reissued at 2026-09-26T09:44:12Z in a fresh public retro-trans/SRW-Z3 repository,
release ID 397176829. All five uploaded assets match the original validated
0.6.21 bytes, sizes and SHA-256 digests. No new build or installation.
The new tag points to clean source snapshot 77cb479, not the historical build
source; BUILD-MANIFEST.json retains the actual original source commit.
Later source fixes and Vietnamese translations are not in the patch.
Public asset downloads and both routes passed Retro Trans 0.3.0 validation.
The live central catalog includes .21 via commit0208c41a. The general workflow
run36233677979 failed on unrelated SRW-Z v0.9.85 manifest naming; the Z3-only
addition retained all ten prior records and passed immutable-identity checks.
That separate global-refresh issue must be resolved for future scheduled updates.
The former repository remains private and archived under
retro-trans/SRW-Z3-private-archive-20260926; old releases/tags were backed up
locally and withdrawn. The historical publication records below are not
statements of the fresh repository's visibility or available old downloads.

## Historical private publication: 0.6.21 (2026-09-25)

Published latest at 2026-09-25T16:50:04Z:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.21.
Repository remains PRIVATE. Five verified assets: full original-to-.21 ISO
xdelta (154,763,400 bytes), exact-.19-to-.21 update (21,234,653 bytes),
BUILD-MANIFEST.json, SHA256SUMS.txt and VALIDATION.json. Both routes round-trip
to SHA256 b67c0a23924e79ab31d28c9b726535473087eee9bf8e5dd4758ce4c6ec64c3e0
(5,011,013,632 bytes). All uploaded sizes/hashes checked before publication.
Source commit 418c709ad973f02c1dd4fe641cdcec3e9aee9e3b; tag points to descendant
9464ca41692cffa84acfc7e36c617c971752e532, adding release records only.
The wrapped snapshot is installed locally with 22 saves unchanged. Runtime
testing remains pending; preserved layout is a hardware candidate, not confirmed.
See docs/releases/0.6.21.md, releases/0.6.21.json and HANDOFF.md.

## Historical publication: 0.6.13 (2026-09-14)

Published as latest at2026-09-14T13:16:06Z:
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.13.
The repository is PRIVATE (verified via GitHub); published means non-draft,
not publicly accessible. At user request, only two uploaded assets remain:
149,070,914-byte full ISO xdelta and14,825,869-byte from-0.6.3 ISO xdelta.
Per-file ZIP and its checksum were removed from GitHub; local copies retained.
Both ISO patches decode to the same4,996,823,040-byte image; all186 files match
in both directory trees. No full ISO/game/Vita upload, source commit/push or
local install. ISO assets were not changed by the ZIP removal.
Tag uses published source tip69e053705b81304657d528e9b5ee571ddb8ba9bd;
notes explicitly distinguish automatic source archives from local build work.
RPCS3 target; separate CFW hardware test remains unverified. Translation partial.
See docs/releases/0.6.13-github.md and releases/0.6.13.json.

Starting after 0.6.0, every successful complete build increments the final
number: **0.6.1, 0.6.2, 0.6.3**, including local builds not yet published.
Failed builds do not consume a number. Do not reset the counter or reuse a
number for different output.

`tools/build_project.py` assigns the number only after the complete build,
regression checks and file hashing succeed. It records the version in
`build_manifest.json` and advances the tracked `build_version.json` counter.
Its counter also considers existing release manifests, using numeric version
ordering. Concurrent numbering is protected by `build_version.lock`; a lock
left by a terminated process needs manual inspection before removal.

The title-screen footer displays this number automatically (see
TITLE_FOOTER.md). The builder renders the prospective number, then checks
it under the numbering lock. A concurrent build claiming that number causes
a failure, never a build labeled with the wrong version. Both `version` and
`title_footer_version` in the successful manifest must match the artwork.

Run the complete VWF build described in TRANSLATING.md, using a new output
directory. Partial/debug builds without the complete validation step are not
release builds and do not receive a version.

A complete package may still be a partial translation. For an explicitly
requested release of all currently available work, append
`--partial-translation` to the complete build command. This preserves the
source audit, validates every present mission translation and all non-mission
UI, but records untranslated mission variants in `message_coverage.json`
instead of claiming full coverage. Its hash and missing count are included
in the validated build manifest. Without this option the audit remains
strict. State story-script progress separately in release notes.

Snapshot that build with:

```powershell
python tools/release.py --build work/out_0.6.1
```

The version is taken from the validated build manifest. An explicitly supplied
version must match it. The snapshotter checks every validated file's size and
SHA-256 before copying; missing, changed or unnumbered builds are rejected.
The immutable snapshot contains game files locally; only its hash manifest
may be committed. Snapshotting/publishing does not increment again.

Generate per-file patches with `tools/release_patch.py` and whole-ISO plus
previous-version update patches with `tools/iso_patch.py --prev 0.6.0`.
Provide `--iso` with the player's own pristine Japanese ISO. Decode every
distribution patch and verify its output before uploading. Publish only
xdelta patches, the application helper and documentation, never game files
or either ISO. Update installation hashes and release notes from the actual
verified output. Publishing is separate from installing into RPCS3.

## 0.6.1 preparation status (2026-09-10)

Published as the latest release at
https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.1 on 2026-09-10.
Uploaded sizes and SHA-256 digests match all three verified local packages.

Build `work/out_0.6.1` passed the full regression suite and is snapshotted as
`releases/0.6.1`: 133 game files, hash manifest `releases/0.6.1.json`.
All distribution packages are verified. The counter is 0.6.1; next build 0.6.2.
133 original-file and 132 previous-file deltas decoded to matching files.
Both ISO deltas decoded to the same image; all ZIP entries passed CRC and
content-hash checks. SHA-256 download hashes are in RELEASE_0.6.1.md.

- Integration preflight recognizes dialogue-only intermission archives.
  All **504 message variants across 58 archives** are now translated,
  including the 233 missing variants plus displayed point-label variants.
  84 victory, 116 defeat and 78 SR entries pass source-role checks.
- Serpent and Kshatriya victory hooks now say "Shoot down ...", including all
  three numbered variants. These corrections are in the verified build.
- Original ISO verified at
  `E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso`.
  Size: 4,431,872,000 bytes; MD5: `2cfedd95e5bdde49550cffa21c3c29a3`.
  Pass this path explicitly with `--iso` to both packaging tools; do not use
  the English ISO in that folder as the pristine source.
- GitHub authentication is confirmed as binhlt0402 with repository write
  access. On this host the CLI needs execution outside the restricted
  environment to access Windows credentials; the restricted calls falsely
  reported invalid authentication. No credentials were changed by the agent.
- No installed game, emulator state or save data was modified.

## Local build 0.6.2 (2026-09-10)

`work/out_0.6.2` is validated but not snapshotted, published or deployed.
It adds the version and GitHub address to the press-any-button title screen.
All 27 unit tests and the complete regression gate passed; all 136 output
hashes were independently checked. Only EFF member 296 changed among the
334 animation members. The other game data and all 58 plaintext stage
archives match 0.6.1; encryption regenerates the SDAT wrapper bytes.
The counter is now 0.6.2 and the next successful build will be 0.6.3.

## Local combined build 0.6.3 (2026-09-12)

`work/build_0.6.3_all` passed the complete build gate and was snapshotted to
`releases/0.6.3` (186 game files). All 132 regression tests passed. The new
Library credits were also independently verified against its font mapping.
This is an explicitly partial translation: 83/116 story scripts, 26/26
intermissions, and a separate 1034-variant mission-text backlog. The counter
is 0.6.3; the next successful build is 0.6.4. Subsequently installed for user
testing on 2026-09-12 (186 hashes verified, 16 save files unchanged); not
published. Prior game/cache backup: work/install_backups/0.6.3_20260912_182937.
Details: `RELEASE_0.6.3.md`.

On the subsequent user release request, public-facing notes were prepared at
`docs/RELEASE_0.6.3.md`, with ISO deltas and a folder-patch ZIP under
`releases/0.6.3_xdelta`. `tools/package_release.py 0.6.3` previews the patch-only
ZIP; repeat with `--write` to create/verify it (refuses overwrite). Upload
was initially blocked by approval review; the user explicitly approved the
three patch assets and GitHub destination. Published as latest on 2026-09-12
at 13:36:57 UTC: https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.3.
All three remote sizes/SHA-256 digests and release notes were verified before
publication; public status/assets were rechecked afterward. No game files
were uploaded and no local source commit/push was performed.

The user's standing preference is to install successful builds for testing.
Use `tools/install_build.ps1 -Build <validated-directory>` for preflight,
then repeat with `-Write` and filesystem approval as required. RPCS3 must be
closed. This preserves prior files/cache, verifies destination hashes, and
checks saves are unchanged. Do not force-quit gameplay or deploy mixed files.
