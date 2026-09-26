# SRW Z3: preparing Retro Trans-compatible patches

This guide applies to future release preparation. It does not publish anything
or change historical releases. Keep the project private unless the user
explicitly requests otherwise. Do not create tags, upload assets, create or
publish GitHub releases, change repository visibility, or add private metadata
to the public catalog as a side effect of a fix or local build.

Follow CLAUDE.md, HANDOFF.md and docs/RELEASING.md for the existing translation,
build and snapshot workflow. Full builds and installation retain their existing
authorization requirements. This document adds the distribution contract; it
does not replace platform-specific build or game-testing checks.

## What the desktop patcher can apply

| Project output | Retro Trans v1 handling |
| --- | --- |
| PS3 whole-ISO xdelta | Supported when the exact source and output ISO are described by a standard manifest. |
| PS3 extracted game folder or a ZIP of per-file patches | Requires the existing project installer; the desktop patcher does not apply a directory patch set. |
| Vita3K installation ZIP or physical-Vita rePatch package | Requires its existing installer and platform-specific instructions. These are not whole-VPK patches. |
| Future whole-file Vita VPK xdelta | Possible only after exact original and output VPK bytes exist and the full round trip is verified. Renaming or wrapping today's ZIP is not sufficient. |

Keep PS3 and Vita verification separate. A matching file hash is not evidence
of physical-console compatibility or gameplay coverage. Document the tested
runtime and remaining limitations in release notes.

The v1 manifest describes one game/platform at the release level. For now the
standard manifest should describe the PS3 ISO patches. Existing Vita installers
may remain separate, clearly documented optional assets; do not attach a second
BUILD-MANIFEST.json or describe them as automatically installable. A future
Vita whole-binary release needs its own game ID and standard release stream
(for example, a dedicated patch repository approved by the user).

## Stable identity and version rules

Use these values for the new PS3 standard release stream:

| Field | Value |
| --- | --- |
| game_id | srw-z3-jigoku-ps3 |
| game_name | Super Robot Taisen Z3: Jigoku-hen (PS3) |
| platform | PS3 |
| edition | jp-bljs10256 |
| language | en |
| source_format / target_format | iso / iso |

These IDs are proposed for the first standard release; keep them stable once
published. Byte-distinct simultaneous variants need distinct edition IDs. Do not
describe two different outputs as the same game/edition/language/version.

- Take the target version from the verified complete build and the existing
  numbering policy. Packaging an existing build does not increment it again.
- Use a numeric stable version such as 1.2.3. A local trial label such as
  0.6.14-dual-test1 is not a supported stable manifest version. Do not silently
  relabel that different image as the already-issued 0.6.14; keep it a local
  candidate until the user requests an appropriate numbered build/release.
- Use source_version = original for the pristine Japanese ISO; use the exact
  previously issued numeric version for an incremental source.
- source_commit must identify the actual translation/tool sources that built
  the target. git rev-parse HEAD is usable only if that commit includes the
  relevant build changes. Do not stamp an older clean tag onto an output built
  from uncommitted changes and claim it is reproducible.
- Preserve every issued input/output image or its verified historical metadata
  locally. New releases require complete SHA-256 hashes and byte sizes; the
  shared builder computes these. Filenames and version labels are not proof
  that a file is compatible.

## Prepare a local configuration

Install the pinned shared builder into a Python 3.12+ environment on Windows x64:

```powershell
python -m pip install git+https://github.com/retro-trans/retro-trans-tools.git@v0.2.1
```

Copy docs/retro-trans-release.example.json to the ignored
work/retro-trans/release-local.json. Replace every SET_* and REPLACE_* value.
Set both input paths to actual existing ISO files: the pristine source and the
verified target of the selected build. The example is intentionally incomplete
and does not assign a new release number. Relative file paths resolve from the
configuration's directory, not the shell's working directory.

The first entry makes an original-to-target full patch. To support an upgrade,
add another entry with the same edition, language, target and target version;
give it a unique .xdelta filename, source_version set to the prior version,
and source pointing at that exact prior ISO. Never use a patch file as source.
Include only routes whose inputs are available for a local round trip.

For example, if only 1.1 -> 1.2 and 1.2 -> 1.3 exist, the app must perform those
two steps. An original -> 1.3 patch can be a separate direct route. Do not invent
a 1.1 -> 1.3 edge without actually generating and verifying it.

## Build and verify, when requested

Run the existing platform preflight/dry-run checks first. The shared builder
below has no --dry-run mode: it really hashes files, encodes deltas and decodes
verification copies. Review the configuration and free space before running it.

From the project root, choose a NEW output directory under ignored work/:

```powershell
python -m retro_trans.release build work/retro-trans/release-local.json --out work/retro-trans/ready
python -m retro_trans.release validate work/retro-trans/ready
```

If ready already exists, preserve it and choose another output name. The builder
must succeed for every configured full/incremental route. It creates exactly
one BUILD-MANIFEST.json, the referenced .xdelta files, SHA256SUMS.txt and
VALIDATION.json. Each generated patch is decoded and the entire output is checked
against the intended ISO's SHA-256 before the directory is accepted. Temporary
verification images and input paths are excluded from the final artifacts.

The legacy snapshot/per-file manifests and PATCH_AUDIT.json remain useful local
records, but are not substitutes for this standard manifest and validation
report. Retain any additional project checks. Do not automatically reinstate
assets the user previously withdrew from a release.

## While the project is private

The desktop app currently uses the public central catalog and public release
download URLs. It has no private-project login, local catalog-import UI or
authenticated private-release download flow. Preparing this manifest alone
does not make the private project available in Automatic mode.

For an authorized private test, obtain the verified .xdelta through the private
project's normal authorized channel, then use Apply xdelta with the matching
local ISO and a new output filename. Manual mode checks xdelta's embedded
checksums; separately compare the resulting complete file SHA-256 and size with
BUILD-MANIFEST.json to reproduce the stronger catalog verification.

Do not put private manifests, source details, URLs or credentials in
retro-trans-tools' public catalog or Actions configuration. Do not broaden the
public catalog workflow's token to expose private projects. Private source may
remain private even if the user later authorizes a separate public patch-only
release repository; that destination and its contents must be explicitly chosen.

## When the user explicitly requests publication

Publish only the validated protocol artifacts plus separately reviewed extras
and documentation to the approved destination. Never upload original/translated
ISOs, extracted game files, Vita auth/license data, or local installation ZIPs
containing game binaries. Optional source archives need their own content review.

The release tag must match the manifest's numeric version, optionally prefixed
with v. Existing patch bytes and identities are immutable: corrections require
a new version. Before publishing a draft, verify uploaded asset names, sizes and
SHA-256 digests against the local ready directory. GitHub can check those assets
without game files; actual ISO round trips run locally.

An approved public standard release under retro-trans can then be discovered by
the central hourly/manual catalog workflow. A private release cannot be consumed
by the current public desktop download flow. This guide adds no publishing job.

Protocol reference: [Retro Trans release standard](https://github.com/retro-trans/retro-trans-tools/blob/v0.2.1/docs/RELEASE_STANDARD.md).
