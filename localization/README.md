# Shared localization: one translation, separate platform adapters

Japanese `messages/` definitions and the PS3 `legacy.json` template are
**local-only**, as are generated `translation/` JSON/TSV views. They remain
available in the existing workspace but are excluded from Git. A fresh clone
needs these inputs for source-dependent checks, comparison and exports;
see [local source setup and limitations](../docs/LOCAL_SOURCE_DATA.md).

Edit **`locales/<language>/<group>.json`**, not the old `translation/` files.
English is `en`. The Vietnamese worktree's 188 locale files are now merged
under `vi`: 43,104 entries, including 42,155 passing current structural checks,
402 pending reviews and 547 explicit missing entries. Other catalog entries
still lack Vietnamese. See [Vietnamese status](locales/vi/README.md); this
content-only merge is not a ready-to-build Vietnamese release.
`locale.schema.json` describes the editable file format for JSON-aware editors;
the checker additionally verifies IDs, placeholders and link markers.

## What lives where

| Location | Purpose |
| --- | --- |
| `messages/*.json` | Stable message IDs, Japanese source when available, context, required tokens and link markers |
| `locales/en/*.json` | Current English wording and translation status |
| `locales/<language>/*.json` | Another language using the **same IDs** |
| `assets.json` | Logo/artwork and recorded-audio exceptions |
| `../platforms/ps3/localization/` | Legacy JSON templates and Python UI literal bindings; PS3 metadata stays here |
| `../platforms/vita/localization/` | Vita coverage/binding declaration; verified source matching, not copied PS3 addresses |
| `../translation/`, `../analysis/glossary.json` | Generated English compatibility views for old tools |

A message ID is permanent. Changing a translation never changes its ID.
Imported IDs were minted from the original context, **not English wording**.
Similar labels may intentionally have different IDs because their contexts
and width limits differ. Glossary references still use `$$Japanese$$` (with
the existing discriminator/lowercase syntax); translate the glossary entry
once instead of replacing those references with literal names.

## Editing English

For an AI-only meaning/quality review before editing, use
[`docs/AI_PROOFREADING.md`](../docs/AI_PROOFREADING.md) and `tools/mqm.py`.
It freezes canonical entries by stable ID, guides two AI review passes, and
reports MQM penalties with explicit coverage and uncertainty. It never applies
suggestions or marks translations reviewed automatically.

1. Search `locales/en/` for the current wording, then look up that ID in
   `messages/` for its source and context. JSON files remain UTF-8.
2. Change only the locale entry's `text`; use `translated` or `reviewed`
   status. `imported` means copied unchanged from the previous source, not
   newly proofread. Empty strings may intentionally suppress a split label;
   `null` means missing. Preserve every required token and link marker.
3. Run the checks and preview the compatibility changes:

```powershell
python tools/localization.py check
python tools/localization.py sync
```

4. If correct, export the English compatibility views, then verify:

```powershell
python tools/localization.py sync --write
python tools/localization.py check --compatibility
```

These are **content checks/exports, not game builds or installation**.
Synchronization rejects unexpected edits in old compatibility files instead
of overwriting them. Reconcile such edits with the canonical locale manually.
Existing merge/tokenization tools that write `translation/` must not be run
against the canonical working copy: use temporary review output and transfer
approved changes by ID. Their old direct-write workflows are not migrated.
Registering previously unextracted messages also needs new definitions and
verified platform bindings; do not rerun the one-time migration to renumber
the catalog. Preserve existing IDs when adding rows.

## Adding a language

For example, preview and then create a French catalog:

```powershell
python tools/localization.py add-language fr
python tools/localization.py add-language fr --write
```

Translate `locales/fr/`, keeping the IDs and placeholders. Missing entries are
explicitly `null`; the system does **not** silently substitute English.

```powershell
python tools/localization.py check --language fr
python tools/localization.py export --language fr --out work/fr-content
```

`export` is dry-run unless `--write` is supplied. `--fallback en` is an
explicit, audit-recorded option for an incomplete review export, not a claim
of full translation. Exports include legacy JSON/TSV views and the UI literal
dictionary. They contain text, **not an ISO, ZIP game, or patched executable**.

The current game adapters still use English-specific font/layout assumptions.
A new language needs character coverage, font metrics, wrapping, layout and
platform adapter checks before it can be built as a game. Do not enable a
language merely by changing the manifest or swapping the English folder.

## Migration coverage and proof

Initial import: **82,457 entries** — 42,749 dialogue, 31,666 battle subtitles,
4,457 UI strings, 2,222 library fields, 1,156 glossary terms, 83 map-label
image strings and 124 stage titles. Includes existing extracted translations,
not a claim that all possible game text has been discovered.

All 475 legacy data files were left byte-for-byte unchanged. Resolving the
429 extracted Python literals gives identical syntax trees for 45 migrated
UI modules; offsets, conditions, font sizes and layout calculations did not
change. The source hashes and counts are in `migration.json`. Local backups
are under ignored `work/localization/migration_backup/`; the read-only
`tools/check_localization_migration.py` verifies that baseline. This check is
specifically for the migration, not a permanent ban on future UI changes.

`source_status: not_extracted` means the old translated data did not supply
Japanese source; do not invent it. `assets.json` describes recorded-audio and
raster-lettering exceptions. Some remaining embedded UI expressions and
newly discovered assets still need extraction/registration; the allowlist is
in `tools/migrate_localization.py`, with `localization_inventory.py` as a
discovery aid, not proof of exhaustive coverage.

Sharing text does **not** imply equal PS3/Vita coverage. Vita source adapters
now verify story, library, gameplay-name, keyword and battle-subtitle data.
A 1,373-key UI/help hook is CPU-tested but not in-game verified. See
`platforms/vita/COVERAGE.md` for scope and remaining work. The runnable pilot
still contains only the original244 opening records; broader adapters and
VWF/UI candidates are not packaged or installed.
