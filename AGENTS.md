# Project instructions

Follow [CLAUDE.md](CLAUDE.md) and read [HANDOFF.md](HANDOFF.md) for current
project state. Existing translation, build, installation and changelog rules
continue to apply.

Before preparing patch releases, read
[docs/RETRO_TRANS_RELEASES.md](docs/RETRO_TRANS_RELEASES.md). It defines the
shared Retro Trans manifest, local validation gate, PS3/Vita boundaries and
private-project workflow.

Every future release must work with Retro Trans (retro-trans/retro-trans-tools).
Treat the compatibility checklist in docs/RETRO_TRANS_RELEASES.md as a release
completion gate, including public downloads, catalog discovery and cached-catalog
upgrade checks. Do not declare a release complete while this gate is failing.

Keep this project private. Editing, testing or preparing artifacts does not
authorize a version tag, GitHub release, upload, publication, visibility change,
or addition to the public patch catalog. Do those only when the user explicitly
requests the relevant action. A local game build still requires the explicit
build request specified in CLAUDE.md.
