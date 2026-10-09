# Super Robot Taisen Z3: Jigoku-hen — translation project

**Save converter: [Retro Trans](https://github.com/retro-trans/retro-trans-tools).**
The maintained converter is in its **Z3 saves** tab. Choose PS3 to Vita,
Vita to PS3, or both directions; check both save profiles before converting.
Read the [save conversion guide](https://github.com/retro-trans/retro-trans-tools/blob/main/retro_trans/resources/Z3-SAVE-CONVERSION.txt).
Supports decrypted Jigoku-hen RPCS3/Vita3K saves only; it does not decrypt,
resign or install physical-console saves.

**Release maintainers:** see [Retro Trans release preparation](docs/RETRO_TRANS_RELEASES.md)
for the standard patch manifest, PS3/Vita boundaries and private-project workflow.
This does not authorize publication or a repository visibility change.


**Players:** see [docs/INSTALL.md](docs/INSTALL.md) -- download a release, apply the xdelta patches to your own dump.

Download the [latest release](https://github.com/retro-trans/SRW-Z3/releases/latest).
Each release includes its installation instructions, required input hashes,
translation coverage and compatibility notes.
Use [Retro Trans](https://github.com/retro-trans/retro-trans-tools) in Automatic
mode with your own matching game dump, or download a patch from the release
for manual application. Follow that release's instructions for the required
source image and supported platform.

This repository excludes Japanese script dumps; see
[local source requirements](docs/LOCAL_SOURCE_DATA.md).

An open toolchain for translating **Dai-3-Ji Super Robot Taisen Z: Jigoku-hen**
(PlayStation 3, BLJS10256; Vita port starting for PCSG00264) into English.

## Physical Vita rePatch

Use the latest [Retro Trans](https://github.com/retro-trans/retro-trans-tools/releases/latest)
and select **Vita rePatch**: choose your original **PCSG00264 v01.00 PKG** and
matching **NoNpDrm work.bin**, choose a new output folder, then **Create rePatch**.
Keep internet available and at least **6 GB free** on the output drive. The app
automatically downloads the patch and official conversion tool, converts the
PKG locally in an isolated temporary folder, and verifies the output.

Close the game and back up saves/older mods. Copy the generated
`rePatch/PCSG00264` to `ux0:rePatch/PCSG00264` with VitaShell. Compatible rePatch
and your installed original game are required. Do not merge old mods or
overwrite app, updates, or savedata. No Python, terminal commands, pre-decrypted
folder, configured emulator, firmware, or personal auth dump is needed.
Your game package and work.bin stay local and unchanged; they are not supplied
by this release. Download only the app; it handles the bare patch assets.

See the [Vita guide](https://github.com/retro-trans/retro-trans-tools/blob/main/docs/VITA_REPATCH.md)
for exact source hashes, obtaining your own work.bin, privacy and copy steps.
Follow the release notes for tested coverage and runtime limitations. Current
Vita staff roll/ending teaser remain Japanese; physical testing of this exact
integration remains pending. This is not a Vita3K installer or PKG xdelta.

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

See [platforms/vita/README.md](platforms/vita/README.md) for scope and limits.

You need your own copy of the game. This repository contains no disc image, no
game data, no extracted Lua and no dump of the Japanese script.

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

## Credits

| Role | Contributors |
| --- | --- |
| Project Lead | pow |
| Playtesting | SecondarySebs, gabrielgamer99, Theoldnile, Kapt, mr.notaru, GethN7 |

## Not in this repository

Nothing belonging to Banpresto or Bandai Namco: no disc images, no `.SDAT`, no
extracted Lua, no CPK contents, no Japanese script dump. Third-party binaries
(RPCS3, `make_npdata`) come from their own projects.
