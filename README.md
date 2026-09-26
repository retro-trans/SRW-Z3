# Super Robot Taisen Z3: Jigoku-hen — translation project

**Save converter moved to Retro Trans (2026-09-18, local/unreleased).**
The maintained converter and compact Windows interface now live in
`../retro-trans-tools/retro_trans/z3_saves.py` and the **Z3 saves** tab of
Retro Trans. Choose PS3 to Vita, Vita to PS3, or both directions; check both
save profiles before converting. The bundled guide is
`../retro-trans-tools/retro_trans/resources/Z3-SAVE-CONVERSION.txt`.
Supports decrypted Jigoku-hen RPCS3/Vita3K saves only; it does not decrypt,
resign or install physical-console saves. Existing standalone 0.6.14 files
and historical packagers remain as compatibility references. Develop and
distribute future converter changes through Retro Trans, not another Z3
standalone package. No version tag, release, upload or publication is authorized
by this migration. Game builds, installed games and live saves are unchanged.

**Release maintainers:** see [Retro Trans release preparation](docs/RETRO_TRANS_RELEASES.md)
for the standard patch manifest, PS3/Vita boundaries and private-project workflow.
This does not authorize publication or a repository visibility change.


**Players:** see [docs/INSTALL.md](docs/INSTALL.md) -- download a release, apply the xdelta patches to your own dump.

PS3 English release: [**0.6.21**](https://github.com/retro-trans/SRW-Z3/releases/tag/v0.6.21).
See [installation, hashes and known limitations](docs/releases/0.6.21.md).
Use [Retro Trans](https://github.com/retro-trans/retro-trans-tools) in Automatic
mode with your matching original Japanese ISO or exact 0.6.19 ISO, or download
one xdelta from the release for manual application. Both routes produce the
same 0.6.21 image. Physical PS3 compatibility is a hardware candidate, not a
blanket CFW/HEN guarantee.

The public release preserves the existing 0.6.21 patch bytes; it is not a new
build. Later source fixes and the Vietnamese translation are not included.
Historical releases were backed up privately and withdrawn during the public
repository cleanup. This fresh repository excludes Japanese script dumps and
the old Git history; see [local source requirements](docs/LOCAL_SOURCE_DATA.md).

An open toolchain for translating **Dai-3-Ji Super Robot Taisen Z: Jigoku-hen**
(PlayStation 3, BLJS10256; Vita port starting for PCSG00264) into English.

## Shared PS3 / Vita project

One repository and one English translation/glossary source are used for both
versions. See [shared/README.md](shared/README.md) for the consistency policy.

- `localization/`: shared stable message IDs and editable locale JSON; see
  [the multilingual guide](localization/README.md).
- `translation/` and `analysis/glossary.json`: generated English compatibility views.
- `shared/`: content catalog and cross-platform policy.
- `platforms/ps3/`: PS3 build configuration; legacy tools/paths remain supported.
- `platforms/vita/`: opening-stage English pilot, Vita3K packaging and port status.
- `game/`: existing PS3 test installation, unchanged.
- `work/vita/`: ignored Vita review/extraction/build intermediates.

Vita has a **complete installable ZIP with an opening-stage English pilot**
(244 dialogue records), but no runtime/visual test yet. It is NOT the full
PS3 English port. Use [Vita ZIP instructions](platforms/vita/INSTALL_ZIP.md);
no original-PKG install or separate overlay is needed for that ZIP.
See [platforms/vita/README.md](platforms/vita/README.md) for scope and limits.

Successor to the PS2 [SRW Z project](../SRWZClean/SRW-Z). The *doctrine* is
inherited; almost none of the *plumbing* is, because the platform changed
underneath it. See [`docs/FINDINGS.md`](docs/FINDINGS.md) for what actually
carried over.

You need your own copy of the game. This repository contains no disc image, no
game data, no extracted Lua and no dump of the Japanese script.

## Status

**PS3: end to end, proven in-game.** An edited line has been translated, repacked,
re-encrypted, loaded by the real game and seen on screen. Every layer of the
chain works in both directions.

For PS3, the base pipeline works; translation and UI corrections continue.
Vita still needs source verification and platform-specific reverse engineering.

## Check the translation

These commands require the **local-only Japanese catalog and templates**;
they are not included in a fresh clone. See [local source setup and
limitations](docs/LOCAL_SOURCE_DATA.md). Existing workspaces retain them.

Read the recorded Japanese beside the current translation in an offline,
searchable report. Run from the repository root with Python 3.10+:

```sh
python tools/compare_translation.py          # preview; writes nothing
python tools/compare_translation.py --write
```

Open `work/translation-review.html` in your browser. Filter by script group,
category or status, and search Japanese, translated text or stable message ID.
The report shows glossary-expanded text, raw tokens, source context and the
locale file to edit. No patched game or new disc extraction is needed for
entries whose Japanese source is already recorded in the catalog.

```sh
python tools/compare_translation.py --group stage0050b_04 --out work/stage50-review.html
python tools/compare_translation.py --only untranslated --out work/missing-review.html
```

Add `--write` after reviewing the preview. Each output must be a new file.
Missing translations, unavailable Japanese sources, review drafts and validation
issues are reported separately. Blank UI entries and unchanged names/codes are
not automatically errors. This reviews the current catalog, including unbuilt
edits—not the contents or coverage of a released patch. Keep generated reports
local: they can contain Japanese script text. See [TRANSLATING.md](TRANSLATING.md).

## Translate it

Locale text remains tracked. Source-dependent checks and exports require the
local inputs described in [local source setup](docs/LOCAL_SOURCE_DATA.md).

Fix the English or start another language using the shared canonical catalog.
Start with [TRANSLATING.md](TRANSLATING.md) and the
[localization guide](localization/README.md).

```sh
# Edit text/status by stable ID in localization/locales/en/<group>.json.
python tools/localization.py check
python tools/localization.py sync          # preview generated-view changes
python tools/localization.py sync --write
python tools/localization.py check --compatibility
```

Preserve speaker headers, glossary tokens, runtime placeholders and link markers.
Do not edit generated `translation/` files or `analysis/glossary.json`.
`localization.py add-language fr` previews a new locale; repeat with `--write`
to create it. Missing translations never silently fall back to English.
Content checks and reports do not build or install a game. PS3 and Vita still
require their own validated font/layout adapters and separately requested builds.

## Getting the Japanese source

One command. You need your own copy of the game.

```sh
python tools/extract.py --disc "<game>/PS3_GAME/USRDIR"
python tools/extract.py --iso  "<game>.iso"        # equivalent
```

This writes `source/`, which is **not committed** -- the repository holds a
toolchain and translations, never game data. Re-run it any time; the output
is UTF-8 JSON with stable ordering, so a re-extract diffs cleanly.

| path | what |
|------|------|
| `source/stages/<STG>_<member>.json` | dialogue records: event, ordinal, speaker, jp, sha |
| `source/rpw/names.json` | every j-string in RPW_DATA, with the chunks that use it |
| `source/rpw/weapons.json` | 2,694 weapon records with their owning unit |
| `source/library/*.json` | the in-game encyclopedia: keywords, pilots, robots |
| `source/keyword_def.json` | keyword definitions |
| `source/voice/<nnn>.json` | one file per voice section: index, jp, byte budget |
| `source/voice/sections.json` | all 211 sections with their offsets |
| `source/MANIFEST.json` | what ran, what failed |

Two things to know. **Stages need RPCS3 closed** -- decryption drives its
`--decrypt` and it is single-instance; that step reports and skips if it
cannot run, and the rest still extract. And **point at a pristine copy**:
`deploy.py` overwrites the extracted disc with the English build, so after a
deploy the disc is no longer a source. Originals are cached in `work/orig/`
on first use, so a project that has already deployed can still re-extract;
an ISO is always safe.

Editable translations live in `localization/locales/<language>/`, paired by
stable ID with recorded Japanese and context in `localization/messages/`.
The `translation/` files are generated compatibility views, not edit targets.

## The chain

```
DATA/STAGE/STG*.SDAT
   |  SDAT (NPD flag 0x01000000) — self-keyed, decrypts offline
   v  python tools/unsdat.py <src> <outdir>
CPK archive (ITOC layout)
   |  CRILAYLA-compressed members
   v  python tools/extract_stage.py <decrypted.sdat> <outdir>
Lua source, cp932
```

The scenario ships as **uncompiled Lua source**. That is the good news: no
pointer tables, no binary record surgery, no custom compression to reverse.

```sh
# 1. decrypt (close RPCS3 first — it is single-instance)
python tools/unsdat.py "<game>/PS3_GAME/USRDIR/DATA/STAGE" work/stage

# 2. unwrap one stage to its Lua
python tools/extract_stage.py work/stage/STG0002.SDAT work/lua

# CPK inspection
python tools/cpk.py list   <file.cpk>
python tools/cpk.py info   <file.cpk>
python tools/cpk.py unpack <file.cpk> <outdir>
```

Pure stdlib, no dependencies. `unsdat.py` shells out to RPCS3's `--decrypt`
rather than reimplementing PS3 crypto.

## The working recipe

Historical format demonstration, not the current contributor workflow. Use
[TRANSLATING.md](TRANSLATING.md) for canonical edits; do not follow these older
direct-write examples to prepare or install a current release.

```sh
# 1. decrypt (close RPCS3 first - it is single-instance)
python tools/unsdat.py "<game>/PS3_GAME/USRDIR/DATA/STAGE" work/stage

# 2. unwrap one stage to its Lua
python tools/extract_stage.py work/stage/STG0001A.SDAT work/lua

# 3. edit the Lua - English must be FULLWIDTH, see docs/TEXT_RULES.md
python tools/fullwidth.py --width "Look, everyone!"

# 4. rebuild the CPK
python tools/cpkpatch.py work/stage/STG0001A.SDAT out.cpk --replace 4=edited.lua

# 5. re-encrypt - VERSION 2, not 4; v3/v4 output is rejected
make_npdata -e out.cpk STG0001A.SDAT 2 0 00 1 16 0 "" 0

# 6. check acceptance in seconds instead of booting (close RPCS3 first)
rpcs3.exe --decrypt STG0001A.SDAT     # a .unedat appears == the game will load it

# 7. copy into DATA/STAGE and run
```

Three traps, each of which cost a cycle here:

1. **`make_npdata` version 4 is broken** even though the originals are v4. Use
   2. See [`docs/WRITEBACK.md`](docs/WRITEBACK.md).
2. **English must be fullwidth** or it renders as unrelated kanji, at two
   columns per character. See [`docs/TEXT_RULES.md`](docs/TEXT_RULES.md).
3. **Close RPCS3 before the oracle.** Single-instance means a running copy
   makes every check look like a rejection.

## Inherited from the PS2 project

The rules worth keeping, all verified as still relevant in Z3:

- **A glossary term and its `《》` links are ONE edit.** Balanced `《》` pairs
  exist in the Z3 script. On PS2 a link with no bank entry crashed the scene.
  Assume the same until proven otherwise; rename the bank first.
- **`$` placeholders expand at runtime.** `$n $F $l $D $R $A` all appear.
  Widths must be re-measured on PS3 — do not carry the PS2 column counts over.
- **cp932 limits what you can write.** No em-dashes, no curly quotes, no
  umlauts.
- **A tool being correct is not evidence that its output shipped.** Verify
  against the artifact the game actually loads.
- **`analysis/glossary.json` from the PS2 project is the highest-value
  carryover** — same continuity, overlapping cast and mecha roster. Bring it
  across with its `glossary_sources.json` provenance intact, especially the
  `ambiguous` entries, which are the ones a global rename gets wrong.

## Credits

| Role | Contributors |
| --- | --- |
| Project Lead | pow |
| Playtesting | SecondarySebs, gabrielgamer99, Theoldnile, Kapt, mr.notaru, rikineko |

## Not in this repository

Nothing belonging to Banpresto or Bandai Namco: no disc images, no `.SDAT`, no
extracted Lua, no CPK contents, no Japanese script dump. Third-party binaries
(RPCS3, `make_npdata`) come from their own projects.
