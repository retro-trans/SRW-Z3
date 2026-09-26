# Message-class coverage audit — 2026-09-09

## 0.6.1 expansion — 2026-09-10

The integrated source audit now covers 58 stage/intermission archives and
504 exact display variants (including displayed point labels after Lua
escaping). All have English translations. `mission_conditions_hook.json`
adds 41 reviewed base conditions; numbering, Hibiki's displayed name and
per-line forms expand deterministically from those translations.

Operation IDs independently identify 84 victory entries, 116 defeat entries
and 78 SR entries. Victory shoot-down objectives use "Shoot down ...";
defeat conditions retain failure-event wording. Serpent and Kshatriya are
corrected. Thresholds, turn limits, faction-kill restrictions and ordered
objectives are preserved. Source-role and text-width checks are release
gates. Four explicitly identified dialogue-only archives lack member 1;
other table-less intermissions must be route scripts with no OPERATE_TBL.

The notes below describe the earlier 17-archive candidate, not 0.6.1's scope.

Prepared output: `work/out_message_classes_20260909`. **Not deployed.**

Full regression, source compilation, width checks and all 31 manifest hashes
passed. A negative test confirmed that removing an effect translation makes
the coverage guard fail. EBOOT SHA256:
`1d88be104a8b0f5a5d12df8e6ffcfe04e75a67b2f420efb38ca876445e5c0195`.

This audit reads original data independently of the translation lists. It
does not equate passing encoding tests with complete translation coverage.

| Source family | Inventoried display variants |
| --- | ---: |
| Victory, defeat and SR conditions from 17 stage archives | 183 |
| D-Trader shop requirements, including wrapped variants | 42 |
| Completed unlock-condition notices | 17 |
| Weapon effect labels, including trailing-space variant | 11 |
| Fixed reward-report strings | 6 |
| Total exact strings | 259 |

Three reward format strings are checked separately: the existing variable
PP bonus plus the newly translated Ace Bonus and part-reward templates.
Their ASCII `%s` specifiers and runtime values are preserved. The shared
D-Trader availability constructor remains covered by `unlock_reports.py`.

## Findings and changes

The first pass found 88 missing mission/effect/completed-unlock variants.
Expanding to the actual shop strings found 29 more missing full strings;
the reward table had four additional untranslated fixed labels. Per-line
expansion brings the patch to 154 new binary lookup entries. No existing
lookup translation is overwritten. Two reward formats are patched within
their verified source slots; gameplay and stage data are unchanged.

The new mission coverage includes late-local-stage conditions (Stages
11–15), original `ヒビキＡ` and displayed `ヒビキ` variants, numbering 1–3,
and the independently drawn lines of multiline conditions. Translations
retain names established in the glossary/stage scripts and all thresholds.

The final read-only ELF segment grows from 512 to 576 KiB without moving
existing addresses. New strings occupy EXT+80000..83f9e (exclusive); 49250
bytes remain. The hook table holds 3512 entries out of its 4095 usable slots.
The builder checks segment non-overlap, exact allowed byte changes, parent
hashes, text widths, and identity of the other 27 game files.

## Regression guard

`tools/audit_message_classes.py` extracts the inventory from the original
executable and every `work/stage_dec/STG*.cpk` archive. A stage without an
operation table must explicitly declare that absence; an unexpected format
is an error, not a silent skip. Missing keys and Japanese text in English
values fail the check. `check_issue_fixes.py` also verifies the actual binary
entries, widths, the three format placeholders, and earlier pending fixes.

The generated `message_class_audit.json` in the output records every source
reference and resulting English string. The builder is read-only by default:

```
python -X utf8 tools/audit_message_classes.py
python -u -X utf8 work/github_issues/build_message_classes_20260909.py
```

Use the builder's `--write` only for a fresh candidate directory. A valid
`build_manifest.json` is required before deployment.

## Limits

Coverage is for the locally extracted prologue/Stages 1–15 (including the
available branch variants) and the specified executable tables, not all
later stages or all game dialogue, UI artwork, or arbitrary custom-name
substitutions. Naming/search/Tag Command and texture fixes remain covered
by their existing scoped tests; this audit does not claim to inventory all
menus or all textures. No in-game visual QA or deployment was performed.
