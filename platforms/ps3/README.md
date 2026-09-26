# PS3 — BLJS10256

`manifest.py` owns the PS3 archive/member paths. Run commands from the repository
root. `translation/manifest.py` is a compatibility entry point with identical
STAGES and LIBRARIES, so existing commands still work.

The implementation remains in `tools/` during this incremental reorganization:
it has many established imports and source-relative assets. Do not bulk-move it
or apply PS3 executable offsets, fonts or archive wrappers to Vita.

`game/` remains the single PS3 test installation. Builds stay in ignored `work/`.
No build/install occurs merely because the project is reorganized.

Future PS3 build manifests include `platform: ps3` and `shared_content`, the
same English source-tree fingerprint used by Vita review preparation. Existing
builds are not restamped retroactively.

## Required dual-target packaging (2026-09-19)

Future requested PS3 builds target **both modified physical PS3 and RPCS3**.
The user-confirmed hardware baseline is `0.6.15-hardware-test1`:

- ISO: `work/ps3_hardware_0.6.15_test1_20260919/SRW-Z3-English-0.6.15-hardware-test1.iso`
- SHA256: `f0b94d9666c1703daf27b05a1d47d401443cdd70d3da73b2497c7ea23ae7abe9`
- Delivered SELF SHA256: `46f0e30fde96d61d62316e96fdbd0fa0db59638021880cc5c77725728843962f`

Keep that image and snapshot for regression comparison; do not overwrite them.
The user reports success, not an exhaustive gameplay or all-firmware test.
The older `.14-dual-test1` separately has an explicit RPCS3 success report.

For each new explicitly authorized build:

1. Run the full current-source build with preflight and regression validation.
   Its raw ELF and font/script set are intermediate outputs, not final delivery.
2. Run `package_hardware_current.py --build <validated-build> --out <new-work-output>`
   as a dry-run, then repeat with `--write` only after checks pass. This uses
   the guarded two-LOAD fold, pinned wrapper and original application
   metadata, and verifies every member in both trees.
   **Disc layout (2026-09-23):** the default is now `preserved_iso.py`. It
   keeps the original disc's layout, appends the changed files, repoints
   ISO9660 and Joliet, zeroes the UDF tree's recognition sequence, anchors and
   descriptors, and applies the same `stamp_disc` header (one whole-image
   plaintext region). This keeps an original-to-release xdelta small. The
   fresh writer relocated every file, which produced a ~3 GB patch, over
   GitHub's 2 GiB asset limit. `--fresh-layout` keeps that writer: it is the
   layout of the user-confirmed `0.6.15-hardware-test1`. **The preserved
   layout itself has no hardware boot report yet**; until one arrives,
   describe a release made with it as hardware-candidate, not
   hardware-confirmed.
3. Use `<new-work-output>/snapshot` with `tools/install_build.ps1`, dry-run
   then `-Write`, following emulator-closed, backup and save-preservation rules.
   **Do not install the raw source-build folder instead.** The ISO and RPCS3
   must use the same wrapped executable and translated assets.
4. Record the new ISO/executable hashes and per-target runtime reports.
   Passing structural checks or reusing the loader does not automatically
   make new translations/code runtime-tested. Stop on loader guard failures;
   investigate rather than falling back to emulator-only output.

No stock-firmware or blanket HEN support is implied. Existing build numbering,
partial-translation reporting and private release-authorization rules remain
in force. A successful local build does not authorize upload or publication.
