# Vita category port — development test, not a completed release

Updated 2026-09-14. All wording comes from the canonical English locale and
shared glossary. No second Vita translation set was created. The existing
fixed-cell pilot ZIP and VWF development candidates are unchanged.
The coherent VWF test01 ZIP is now built separately in
`work/vita/english_vwf_test_01/`; all116CPKs/589ZIP entries verified.
See [VWF_TEST_ZIP.md](VWF_TEST_ZIP.md). No installation/runtime test yet.

**2026-09-15 source-only follow-up:** `title_art.py` now ports the approved
English wordmark, Time Prison Chapter subtitle and five title-screen Library
labels into native effvita.cpk member296. Palettes, native Z and5,655 animation
samples are preserved. Registered in the ZIP planner; NOT in the already-built
test01 ZIP. Converted atlas previews checked, in-game title/Library rendering
still needs testing after the next authorized build.

## Verified adapter coverage

**Pending opening narration (2026-09-15):** `opening_narration.py` maps all28
shared `narration_0001a` rows to native STG0001a.cpk member7. These fixed text
records were absent from the Lua-only story adapter. Source hash, all28
Japanese identities,52-byte capacity and preservation of every non-text byte
are checked. Wired into the next ZIP plan, not the existing test01 package.
Live narration rendering, page transitions and skip behavior remain unverified.

**Pending startup follow-up (2026-09-15):** shared ui_aiddata captions and
ui.runtime_names are now discovered by the UI hook (1,523 keys /24 groups).
Nine original captions and four blood-type values are checked against native
sources. Exact Hibiki display matching does not rewrite custom names/saves.
`startup_art.py` translates two heading cells in AID member1 texture2 using
shared messages. The birthday drawer uses the shared numeric month/day format;
372 value combinations and text-relative relocation are CPU-tested. Native
calendar values and other date suffixes remain untouched. Not in test01 ZIP;
runtime layout still needs verification after the next authorized build.

| Category | Checked shared content | Remaining qualification |
| --- | --- | --- |
| Story scripts | 42,742 records, 201 members | Native controls and every non-dialogue byte preserved; visual/runtime testing pending |
| Suspend scenes | 16 of 872 source records | Kouji/Shiro and Dancouga Nova scenes; other 856 records unchanged |
| Robot library | 253 entries | Names, source series, measurements and descriptions; native layout pending |
| Pilot library | 408 entries | Names, actors, source series and descriptions; native layout pending |
| Keyword index | 141 entries | Separate from the actual popup file |
| Keyword popups | 141 entries, all four fields | Actual MTFL file rebuilt and read back; native layout pending |
| Gameplay names/terms | 1,685 of 4,565 strings, 953 per-record overrides | Not all remaining strings are prose. Effect/help descriptions and unresolved names are not claimed complete |
| Battle subtitles | 31,666 records in 276 blocks | Source/cues/pointers verified; native battle renderer and layout pending |
| Menu/UI | 817 shared messages found in native executable | Discovery only: 154 have multiple hits; 1,560 searched source-bearing messages were not found there |
| Native UI/help hook | 1,510 exact keys across 22 shared groups | Included in test ZIP; live paths and layout unverified |

These are **checked adapters now packaged for testing**, not installed or
runtime-verified translations.
UI discovery counts are not the complete 4,457-message UI catalog: some
definitions lack extracted Japanese or belong to different asset families.
Stage titles, map-label sprites and other raster menus still need native
asset mappings. Approved title art and Library buttons have a pending adapter
as noted above. Japanese recorded voices are unchanged; English
subtitles do not constitute an English dub.

## Safety and presentation

- Every native source file used is checked against the local decryption audit.
  Libraries, RPW, actual keyword definitions and SRVC additionally match the
  corresponding PS3 **data** byte-for-byte. No PS3 executable instructions or
  addresses are reused.
- All 201 story members match event, ordinal, speaker, Japanese fingerprint
  and source text. Patching verifies all command/skip/link metadata outside
  dialogue bodies unchanged. A failed row excludes its entire member.
- The current VWF candidate maps 95 ASCII characters to blank native cells.
  Its code/font combination must accompany this content in a future build.
- Display-only aliases convert the 66 pairs of unsupported half-width corner
  quotes to full-width corner quotes. Soft dialogue line breaks can reflow
  without changing words or controls; speaker lines and blank paragraphs stay
  separate. This resolves all initial 81 story-check failures without editing
  the shared English. Four-line/960-texel/256-byte checks remain provisional
  native-MtV limits, not a claim of on-screen approval.
- Library/keyword descriptions use provisional 960-texel reflow. RPW names
  and battle subtitles still need their own native panel measurements.
- RPW checks follow the original pointer columns, preserve semantic NULL
  offsets, original string ordinals and every non-pointer binary word.
  `boost-p` description columns 3–8 are protected. The reported 701 unresolved
  name-component records are not automatically invented or translated.
- The SRVC offset array is independently found in the native SELF: segment 1,
  relative offset 433180, 277 little-endian entries. The adapter resolves the
  segment's current file offset, so a repacked VWF candidate does not reuse a
  stale file position. Source comparison and inverse edit must pass, both on
  the original SELF and the actual in-memory VWF-repacked SELF.
  **SRVC and its corresponding executable table must ship together.**
- Suspend source definitions were enriched with seven actual Japanese strings
  only after matching existing fingerprints. Stable IDs, English and all 475
  compatibility views remain unchanged.

## Review commands

From the repository root (Python dependencies described in VWF.md):

```powershell
python platforms/vita/category_port.py
python platforms/vita/category_port.py --categories keywords gameplay_terms
```

Default is dry-run. After inspecting it, a private JSON audit may be saved to
a **new** file beneath `work/vita`:

```powershell
python platforms/vita/category_port.py --report work/vita/my_category_review.json --write
```

This command has no CPK, ZIP, PKG, installation or release mode. Counts/hashes
are regenerated from the current shared catalog. The detailed local review is
`work/vita/categories_audit_02.json`; the earlier stage-only audit records the
initial failures and is retained. Neither file is editable translation data.

## Next work

1. Map menu/help native readers and relocations; convert string discovery into
   guarded native bindings before replacing text. Verify UTF-8 versus CP932
   paths, buffers, centered text, highlights and link hit boxes.
2. Locate Vita text sprites, stage-title data and title art, and use shared
   message IDs with platform-specific geometry.
3. Inventory the remaining Japanese descriptions and suspend scenes in the
   shared catalog, with source/context; translate only once for both platforms.
4. Integrate these adapters into a coherent VWF build when requested. The old
   pilot/ZIP builder still covers only 244 records and must not be described as
   the broad port. Runtime-test boot, battle, library, skips and menus on Vita3K.

Physical Vita compatibility remains unverified.

## Native UI/help follow-up

`ui_text.py` now provides native whole-description and draw hooks for 1,510 keys, including
387 generic UI labels, 77 UTF-8 UI labels, 29 command/executable labels,
118 skill descriptions, 35 Spirit descriptions, 275 part descriptions,
94 tutorial messages, 83 key-help labels, and other categories. Counts are
distinct keys assigned to their first shared group when duplicates agree.
New:109 bare scenario-title keys and28 heading/route labels reused from shared
English. This does not translate title textures or arbitrary composed headings.

The hook runs after optional UTF-8 conversion, matches whole strings, and
points the drawer to separately stored English. It follows the native ASCII
font-code conversion rather than ordinary CP932. Full comparison including
the terminator follows hashing, so collisions/prefixes cannot select text.
No source string slots are overwritten. Sources include pinned EBOOT,
5,440 header-bounded native ASSF widget records and audited RPW help strings.

Excluded: 13 conflicting keys, 12 messages needing PS3-private glyphs,
46 runtime-format/control messages, 523 unlocated messages and one lacking
source. No context guesses or ordering-based conflict resolution.

Run `python platforms/vita/category_port.py --categories ui_text` for a dry-run.
The existing `--report ... --write` saves JSON only. Latest private audit:
`work/vita/ui_text_audit_02.json`. No loose executable or archive is written.
This composes VWF internally and is not an installable standalone update.

Twelve UI CPU/safety tests pass; all Vita plus localization tests:79. Original
converter/drawer integration is tested, with the imported UTF-8 decoder and
GPU calls intercepted. A32-byte wrapper translates before native MtV line
counting/splitting; integration runs that entry and line counter, intercepting
only imported strlen. NULL, empty/missing keys, flags, registers and floating
state are tested. English lines over256 encoded bytes are rejected; no current
included entries exceed that limit. Other fragmentation paths and live
centering/clipping/dynamic values still need work. Earlier discovery counts must
not be added to these hook counts. No broader package has been built.
