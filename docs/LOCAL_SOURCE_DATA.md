# Local Japanese source data

The editable translation is tracked in `localization/locales/<language>/`.
Japanese script dumps and their duplicate exports are local-only:

| Local path | Contents |
| --- | --- |
| `localization/messages/*.json` | Original text, permanent IDs, context and validation metadata |
| `platforms/ps3/localization/legacy.json` | Source-bearing compatibility templates |
| `translation/**/*.json`, `translation/**/*.tsv` | Generated compatibility views, some with the original script |
| `source/`, `work/` | Extracted game data, comparison reports and build/recovery outputs |

These paths are ignored, not deleted. Do not force-add them to Git or attach
them to releases. `translation/manifest.py` remains tracked as a code wrapper.
Short Japanese lookup keys, glossary names, required `$$Japanese$$` references
and focused regression examples remain in the toolchain; they are not the
complete original script.

## Existing local workspace

No input paths or stable IDs changed. Comparison, validation, synchronization
and builds continue using the same local inputs. Keep these inputs in your
private local backup alongside the locale files. The history-reset archive
also contains the old Git history and source files: it is private recovery
data, not a distribution artifact.

## Fresh clone

A clone includes translation text and tools, but does **not** include the
source catalog/templates or generated compatibility JSON/TSV. You may inspect
and edit the locale JSON by stable ID. Source-dependent comparison, catalog
checks, exports and game builds require the corresponding local inputs first.
Do not disable validation to work around missing source data.

`tools/extract.py` extracts data from your own pristine game into `source/`.
It does **not** currently reconstruct all of the ignored canonical definitions
and compatibility templates. There is not yet a complete, tested fresh-clone
bootstrap for those inputs. Restore your own matching local backup when
available; otherwise source registration/matching work is required. Do not
rerun the historical one-time migration to mint new IDs for existing entries.

## History and publication

The September 26 local reset starts the main repository with one new root
commit containing current edits. Old history is retained only in the ignored
local recovery archive, with the two existing linked worktrees attached to it.
Old branches and release tags are not copied into the new repository.

This does not rewrite GitHub, remove hosted release assets, erase other clones
or change repository visibility. A remote history replacement is a separate
explicitly authorized operation. Existing copies/caches and hosted assets need
their own audit before publication; this cleanup is not publication approval.
