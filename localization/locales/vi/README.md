# Vietnamese translation

## Content merged into the main catalog — 2026-09-26

Imported all 188 Vietnamese locale JSON files from `codex/vietnamese-silver`
at `5dd5d66460ccea7b5f3c606d047e4575fe5bf3a2`. This is a content-only
integration, not a Git history merge. The linked worktree and its original
review notes remain unchanged. Its fonts, build adapters and older English
files were not imported over the current main toolchain.

All 43,104 entries matched current stable IDs, Japanese source, record context
and content kind. Vietnamese wording is unchanged. The 244 old opening drafts
were replaced with the branch's later versions; their local backup is under
`work/vi-merge-20260926/backup/`.

| Imported entry status | Count |
| --- | ---: |
| Passes current catalog and glossary checks | 42,155 |
| Needs review | 402 |
| Explicitly missing | 547 |
| Total imported entries | 43,104 |

393 previously accepted dialogue entries do not match the current required
glossary-token inventory. Their text is preserved, but their status is now
`needs_review`; do not silently drop tokens, change Japanese definitions or
weaken the shared validator to make them pass. The other nine pending reviews
were already pending on the worktree. Six existing title notes are preserved
in the [merge review report](../../qa/vi_worktree_merge_20260926.json), rather
than unsupported extra fields in the locale JSON schema. The report lists all
402 review IDs and the source-file hashes.

Passing entries comprise 41,143 dialogue records, 776 glossary terms, 118 UI
entries and 118 stage titles. These are structural acceptance counts, not a
new meaning review or an in-game rendering test.

## Coverage and remaining work

The worktree checkpoint contains dialogue through Episode 45 (internal stage
74), plus the first 80 story records of Episode 46A (internal stage 75).
Its next translation slice was stage 75 story records 81–160. Later chapters,
route branches, epilogue and between-stage story remain part of the main-game
translation scope; internal script numbers are not displayed episode numbers.
Standalone bonus/DLC work is outside that scope. Preserve existing drafts.

The current shared catalog has 103,183 entries. It has 60,626 Vietnamese entries
missing or absent, including the 547 explicit placeholders above; this is not
a complete Vietnamese translation. Missing Vietnamese never implicitly falls
back to English in the catalog.

## Editing and validation

Edit these locale files by stable ID. Preserve Vietnamese NFC, glossary
references, runtime controls, link markers and speaker headers. See
[the contribution guide](../../../TRANSLATING.md) and
[local source prerequisites](../../../docs/LOCAL_SOURCE_DATA.md).

`python tools/localization.py check --language vi` deliberately reports the
remaining missing/review entries. English validation and generated views must
continue to pass independently. The QA report explains the newly introduced
review flags; do not call a partial-language global check a clean pass.

`game_build_ready` remains false. The older branch's Vietnamese font and
English-fallback build support have not been integrated or validated against
the current main tools. No Vietnamese game was built, installed or published
as part of this content merge.
