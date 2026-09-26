# One language-aware source for both platforms

`catalog.json` identifies the canonical localization tree. Text now lives in
`localization/locales/<language>/` with stable IDs and shared definitions in
`localization/messages/`. See [the localization guide](../localization/README.md).
No separate editable Vita translation copy. `translation/` and
`analysis/glossary.json` are generated English compatibility views, not edit targets.

`tools/shared_content.py` fingerprints these files, including uncommitted
changes. Future PS3 builds and Vita review bundles record that same revision.
This detects source drift; it does not guarantee equal coverage or layouts.
The revision selects one locale (English by default), plus shared definitions
and platform bindings. Vietnamese opening drafts were preserved under
`localization/locales/vi/` and require review/token alignment.

Some legacy translation JSON contains PS3-specific hook addresses. Templates
remain under `platforms/ps3/localization/` for compatibility; Vita selects text through verified source
identities, never copy these addresses. Platform offsets, archive IDs, packing,
fonts and layout adjustments belong under the platform adapters. Shared text
must not be silently shortened differently per platform; review/document any
necessary platform-specific presentation exception.
