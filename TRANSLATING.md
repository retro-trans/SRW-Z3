# Translate SRW Z3

Use this guide for current content edits. The PS2 project's direct-disc patching
commands do not apply to Z3. Python 3.10+ is required for the review tools;
they use the standard library and run from the repository root.

**Local source prerequisite:** Japanese message definitions and compatibility
templates/exports are intentionally excluded from Git. The existing workspace
keeps them, but a fresh clone cannot run the source-dependent commands below
without these inputs. See [local source setup](docs/LOCAL_SOURCE_DATA.md),
including the current extraction/bootstrap limitations. Locale JSON remains
tracked and editable; do not change stable IDs or bypass source checks.

## Read Japanese beside the translation

```sh
python tools/compare_translation.py
python tools/compare_translation.py --write
```

Open `work/translation-review.html` in a browser. It is a self-contained,
offline report with search, group/category/status filters and 50-row pages.
It includes the catalog's recorded Japanese, current locale text, stable IDs,
source context and the exact locale file to edit. Glossary references expand
using that language's glossary, never an implicit English fallback. Runtime
names such as `$n` remain symbolic. Raw glossary tokens are also available.
The two legacy parts/skill description catalogs instead use the selected
locale's Spirit/skill dictionaries, matching their existing adapters.

The first command is a preview; the second writes a new report. Existing files
are never overwritten: choose a new `--out` for each later report. Examples:

```sh
python tools/compare_translation.py --group stage0050b_04 --out work/stage50-review.html
python tools/compare_translation.py --group stage0050b_04 --out work/stage50-review.html --write
python tools/compare_translation.py --kind battle_subtitle --out work/battle-review.html
python tools/compare_translation.py --only untranslated --out work/missing-review.html
python tools/compare_translation.py --search "Aoi" --out work/aoi-review.html
```

Repeat a preview with `--write` when ready. `--group` accepts quoted patterns
such as `"stage0050*"` and can be repeated. `--language vi` selects a registered
locale, including its drafts and missing entries. New locales are registered
with the commands below.

These are different conditions, and the filters deliberately keep them separate:

- **Untranslated:** absent/null text or a `missing` status.
- **Source unavailable:** Japanese was not recorded as available; not evidence
  that the translation is missing or that a guessed pairing is correct.
- **Needs review:** a draft explicitly marked `needs_review`.
- **Validation issues:** malformed placeholders, glossary references, links
  or speaker headers; the report shows the issue instead of hiding the row.
- **Same as source:** a review hint, not a verdict; names and codes can match.
- **Blank target:** may intentionally suppress a duplicate UI label.

The report reflects the current working copy, including unbuilt changes. It
does not inspect an ISO, verify what shipped, measure game layout, or prove
complete translation coverage. Source pairing follows stable catalog IDs;
there is no fuzzy matching. No patched game or new disc extraction is needed
to review already-recorded entries. Missing sources require separate verified
extraction from your own game; never invent them. Reports can contain Japanese
script text: keep them local under ignored `work/`, not in commits or releases.

## Fix English

1. Use the report's stable ID and file path to find the entry in
   `localization/locales/en/<group>.json`. Read the same ID in
   `localization/messages/<group>.json` and the neighboring scene for context.
2. Edit `text` and set `status` to `translated` (or `reviewed` after review).
   Preserve IDs, source/context, glossary references `$$Japanese$$`, runtime
   escapes such as `$n`, and `《》` link counts/order. In named dialogue the
   first line is the speaker, followed by a newline; it is not body prose.
   Glossary/placeholder inventory changes need a coordinated definition edit,
   not deletion of the check. Do not edit generated `translation/` files or
   `analysis/glossary.json`.
3. Validate and preview synchronization:

```sh
python tools/localization.py check
python tools/localization.py sync
```

4. Inspect the changes, then export the English compatibility views:

```sh
python tools/localization.py sync --write
python tools/localization.py check --compatibility
```

Record the change in `CHANGELOG.md`. Regenerate a review report to inspect it.
For stage edits, run `tools/check_stage.py` against the matching original Lua
member and generated translation JSON when extracted source/font inputs are
available. Catalog checks alone are not a width, encoding or gameplay test.
Full builds require coherent platform assets and separate build authorization;
these commands do not build, install or publish anything.

## Add a language

```sh
python tools/localization.py add-language fr
python tools/localization.py add-language fr --write
# Edit localization/locales/fr/ by the same stable IDs.
python tools/localization.py check --language fr
python tools/compare_translation.py --language fr --out work/fr-review.html
```

Do not rerun `add-language` for an already registered locale. Missing entries
stay missing. Translate the locale's glossary too. Exporting another language
is text-only until its platform font/layout adapters are validated; it is not
automatically a playable PS3 or Vita patch.

See [the localization guide](localization/README.md) for export details,
[BASE_RULES.md](BASE_RULES.md) for translation rules, and
[the PS3](platforms/ps3/README.md) and [Vita](platforms/vita/README.md) guides
for platform boundaries. [docs/TRANSLATING.md](docs/TRANSLATING.md) contains
historical format research; its older direct-write/build examples are not the
current canonical editing workflow.
