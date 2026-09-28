# Working rules for this repository

- **PS3 hardware + RPCS3 is the default target (2026-09-19).**
  User confirmed `0.6.15-hardware-test1` works after the physical-PS3 test
  request and explicitly asked to retain this method for all future builds.
  Preserve this known-good baseline; its exact hashes and scope are recorded
  in HANDOFF.md. After every requested complete PS3 source build, run
  `platforms/ps3/package_hardware_current.py` dry-run then `--write`, with a
  NEW work output. Use its guarded two-LOAD layout, original-metadata fake
  SELF and verified ISO9660/Joliet packaging. Install its derived `snapshot/`
  into RPCS3, not the raw-ELF build output; both targets must use the same
  executable and assets. Raw ELF is an intermediate, not the default delivery.
  If loader/layout guards fail, investigate; never silently revert to an
  emulator-only package or weaken guards. Validate each new build and track
  runtime reports separately; this confirmation is not blanket firmware/HEN
  support or proof that future edits are tested. Explicit build authorization,
  privacy and publication rules below remain unchanged. See platforms/ps3/README.md.

- **Shared multilingual catalog (2026-09-14).** Canonical text is now in
  localization/locales/<language>/, with stable IDs/source/context in
  localization/messages/. Read localization/README.md before translating.
  Source-bearing messages/, PS3 legacy.json and translation/ JSON/TSV are
  local-only (not tracked); preserve their files and IDs. Fresh clones need
  local inputs: see docs/LOCAL_SOURCE_DATA.md for bootstrap limitations.
  translation/ JSON/TSV and analysis/glossary.json are generated English
  compatibility views, NOT edit targets. Edit English locale files, run
  localization.py check, sync (dry-run), sync --write, check --compatibility.
  Never regenerate existing IDs or overwrite legacy user edits. Old merge
  tools writing translation/ require a temporary review workflow; do not
  silently treat their output as canonical. Other-language exports are text
  only until fonts/layout/adapters pass; no implicit English fallback.

- **Shared PS3/Vita project (2026-09-13, source layout updated 2026-09-14).**
  Keep one canonical translation per language. PS3 configuration lives in
  platforms/ps3/manifest.py; translation/manifest.py remains a compatibility
  entry point. Vita adapters live in platforms/vita/ and generated data in
  ignored work/vita/. Do not copy PS3 offsets/font binaries into Vita or fork
  editable translations. Follow shared/README.md and platforms/vita/README.md.
  Vita opening-stage test overlay AND complete Vita3K install ZIP are built
  (244 source-matched records). User screenshot confirms opening dialogue
  boots but fixed-cell spacing needs VWF. A real VWF source/development
  candidate now exists; not installed or runtime-verified. See Vita VWF.md.
  Not a full English release. INSTALL_ZIP.md describes the OLD fixed-cell ZIP.
  A coherent broad VWF test01 ZIP is now built (2026-09-14), not installed or
  runtime-tested: work/vita/english_vwf_test_01/. See VWF_TEST_ZIP.md and HANDOFF.
  Rebuild with build_vwf_zip.py, dry-run first, NEW output only. Do not use
  the old build_test/build_install_zip defaults for the broad VWF port.
  The single game/ installation rule below currently applies to PS3 only.

- **Batch fixes; build only when explicitly requested (2026-09-13).**
  User is reporting more issues and said to fix all of them until they tell
  us to build. Continue source fixes, focused checks and changelog updates;
  do not start a complete build or install without their explicit go-ahead.
  This overrides the earlier automatic-build workflow. Once a build is
  requested and passes, the default install preference below still applies.

- **Single runnable folder (2026-09-12): `E:/Projects/SRW Z3/game`.**
  All successful builds are installed into this same complete disc tree;
  do not create another user-facing versioned game folder or ISO. Build
  intermediates and recoverable backups may stay under ignored work/.
  tools/prepare_testing_game.ps1 seeds the folder once, dry-run then -Write;
  tools/install_build.ps1 updates it and switches only BLJS10256 registration
  with RPCS3 closed. Preserve other games and old outputs; no cleanup implied.

- **User testing preference (2026-09-12): install successful builds by default.**
  After building and validating a coherent complete package, install it into
  the local RPCS3 game so the user can test, unless they request build-only.
  Use `tools/install_build.ps1` dry-run then `-Write`: back up changed game
  files, retain the old game-data cache, verify hashes and preserve saves.
  If RPCS3 is running, ask the user to close it; do not force-quit gameplay.
  Request filesystem approval when required. Never install a failed or mixed
  build. Installation does not authorize publishing or uploading.
  Verify RPCS3's actual registered/booted game path before deployment: this
  user has used work/patched_0.6.1.iso, which is NOT updated by copying files
  into E:/SRWZ3/PS3_GAME. Do not claim readiness until the active boot copy
  matches the verified build. Preserve other game registrations.

- **Record every change in `CHANGELOG.md`, in the same session as the change.**
  Translation content, tooling, pipeline fixes, corrections to earlier
  entries — all of it. If a shipped label or line is later changed, update the
  entry that documented it (say what shipped first and why it changed) rather
  than leaving the old claim standing. A change that is not in the changelog
  is not done.
- Read `HANDOFF.md` first for project state; `docs/TRANSLATING.md` holds the
  translation workflow and the format findings. `BASE_RULES.md` is the
  translation doctrine; `tools/export_stage.py` bakes its per-line rules
  into every brief.
- **Glossary terms in prose are written `$$japanese$$`, never as literal
  English.** `tools/terms.py` expands them at build time, so renaming a term
  in `analysis/glossary.json` updates every line that mentions it. Writing the
  English directly is what forced the manual project-wide sweeps for Urzu,
  Quent, Chirico, Battling and D-Trader Backdrop. Use `#` discriminators for
  a Japanese string that names two things (`$$レイ#333$$` is Rei Ayanami, not
  Ray Lovelock). Stages 1-10 and the tooling already do this; stages 11-30
  drifted to literal English only because the brief template stopped saying so.
- Stage dialogue is translated by slice: brief each subagent with
  `export_stage.py --range` (about 80-140 records; the brief carries the
  adjacent records as do-not-translate context), collect `{sha: english}`
  answers, `merge_stage.py` them, and accept nothing that does not pass
  `check_stage.py` clean. Agents report records-examined vs records-in-slice
  and flag what they could not verify.
- Releases: `tools/release.py <version>` snapshots `work/out` and writes the
  committed hash manifest; `tools/release_patch.py <version>` builds the
  xdelta patch set for distribution. Cut both for every release.
- Never commit game data: no disc images, SDAT/CPK contents, extracted Lua,
  Japanese script dumps, or patch binaries that embed them. `.gitignore`
  enforces it; the committed manifests carry hashes only.

## Retro Trans distribution instructions (2026-09-18)

**Standing user requirement (2026-09-26): every new release must work with
Retro Trans.** Apply the mandatory compatibility checklist in
docs/RETRO_TRANS_RELEASES.md; a valid local manifest alone is not sufficient.
Preserve existing clients' catalog refresh and patch routes. If a platform or
package is unsupported, resolve that before release or report it as blocked.
This requirement does not itself authorize a new build or publication.

Before preparing future patch releases, read
[docs/RETRO_TRANS_RELEASES.md](docs/RETRO_TRANS_RELEASES.md) and its example
configuration. Use the shared manifest and local round-trip validation gate for
PS3 whole-ISO patches; Vita multi-file installers remain separate. Existing
project build, snapshot, installation and changelog rules still apply.

The project remains private. Do not create version tags, GitHub releases,
uploads, visibility changes or public catalog entries merely because code was
changed or a local build passed. Perform those actions only when explicitly
requested by the user. Preserve withdrawn assets as withdrawn.

