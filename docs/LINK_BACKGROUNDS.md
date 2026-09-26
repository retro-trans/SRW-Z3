# Proportional link backgrounds

## Dialogue scene context: RPCS3 v5 / Vita v4

User confirmed backlog highlights work but dialogue term highlights disappear
on PS3 v4 and Vita v3. The previous tests supplied the scene reference directly,
missing a separate registration precondition. Backlog sets the explicit scene
context (PS3 `19dab4` / `19dc8c`) and clears it afterward; normal dialogue does
not. Registration therefore stored a null scene, skipped glossary ID resolution,
and failed the primary selector's scene-and-ID match.

New narrowly scoped scene-getter wrappers keep any explicit backlog scene.
Only null context falls back to scene zero from the same manager used by the
primary selector. Registration then runs its existing translated comparison.
PS3 hook `1ce1b4`, helper `78efc0` (48 bytes); Vita hook `810d8d86`, helper
`810d6a64` (14 bytes in unused secondary padding). No geometry, names, colors,
backlog navigation, record layout, fonts, text, or archive assets change.

Native-instruction tests start before scene assignment and reproduce the old
null-scene failure, then pass registered identities through primary geometry.
They also cover explicit backlog references, no current scene, stack balance,
register preservation and Vita relocation. These are CPU tests with external
call fixtures, not a completed visual emulator test. Retest both adjacent terms,
switch to the speaker, follow a link and return, open backlog and change scenes.

RPCS3 v5 is EBOOT-only over pinned v4; do NOT delete the install cache for it.
Vita3K v4 has a full installable 589-file ZIP; the rePatch ZIP is manual-only.

Updated September 17, 2026. PS3 v3 also covers the separate speaker-name
widget and translated glossary registration. V1/v2 were insufficient;
in-game verification of v3 remains pending. The original three hooks alone
were insufficient, including in 0.6.13 and physical-console test06.

## V3: actual speaker widgets and glossary identity

The name background is NOT a keyword render record. Native widget `0x256208`
computes `strlen(name)/2 * pitch` at `0x2562d4`. The v3 helper measures exact
translated names with the installed glyph width bank and the widget's quad
width, retaining fractional pixels and native fallback for unknown text.
The original X/Y, height, colours, record layout and click target stay intact.

Registration's comparison at `0x1ce224` compared English drawn terms to
Japanese glossary labels, leaving unmatched terms at default index zero.
Only this call now looks up the Japanese operand in the exact translation
table before calling the original strcmp. Native registration assigns the
correct glossary index; no global comparisons or source keys are rewritten.

Helpers reuse dead v2 primary arithmetic and reserved RX space. V2 geometry
still matches scene and term ID, and the working secondary path stays intact.
`test_ps3_link_identity.py` executes the original name widget and registration
loop with native-call fixtures. It reproduces the old failures and passes
the real registered ID into the primary geometry test. Coverage includes
Kei/Kira/Alto/Hibiki, narrow/wide names, three font sizes and native fallback.
The former name-like keyword fixtures do not establish speaker-widget coverage.

The matching RPCS3 v3 package also contains the separately requested startup
menu artwork and birthday suffix changes. It replaces two files. Do not use
this decrypted RPCS3 executable on physical PS3 or another release baseline.

The reported Back Log Kurara selection was much wider than its label. The
existing keyword-position fix already measures glyph advance in `PEN_ACC`,
but the selected-link rectangle had a separate, unpatched size calculation.

## Source evidence

- `0x1d1dd8` draws the linked text through `0x1d11fc`.
- `0x1d1e10` is the only direct caller of registration function `0x1ce098`.
- Registration records contain X/Y halfwords, a byte length at +4, active
  flag at +5, pitch/height at +6/+7, and navigation/identity fields at +8..+19.
- `0x1ce140` / `0x1ce148` retrieve the allocated bank/slot from the stack;
  the allocator allows 16 banks of 16 records each.
- `0x1c8730` reads the selected record's byte count; `0x1c8740` halves it;
  `0x1c8778` multiplies by the Japanese style pitch. `0x1c87b0` stores the
  resulting float as rectangle width. This remains wrong after VWF rendering.

## Correction

Cache the actual pen advance during registration, without resetting the
accumulator or rewriting any link record fields. Select the cache entry
using the same link index that the original record lookup uses. Retain it in
an unused local stack slot across the style-fetch call, then substitute only
the rectangle-width store. There is no fixed shrink ratio or name-specific
exception, and no change to link lookup strings/IDs or selection controls.

The cache uses 1KB of already mapped scratch BSS. Code uses three guarded
helpers between command-layout data and the President report helper.
Build-time assertions reject occupied code space or unexpected instructions.

## Verification

### Primary path added in v2

`0x1c680c` is a second rectangle builder. Its `0x1c6964..0x1c6a5c` block
parses a compact row/column/length, multiplies by Japanese pitch and caches
that rectangle. This causes both shifted starts and excess width even after
the secondary path is fixed. `main_link_background_layout.py` branches from
`0x1c6964` to a guarded 252-byte helper at `0x78ee00`. It matches scene-zero
identity and glossary index against active render records (not flat index),
uses their signed X/Y and cached width, and calls the original style selector
for height. Native Y+1 inset, draw/color tail, and navigation are retained.
No match leaves the initially zero rectangle; no guessed geometry is drawn.
No new segments, headers, font assets or translation edits are needed.

`test_main_link_background_layout.py` executes emitted PPC instructions with
native getter/style call fixtures and aggressive volatile-register clobbers.
It covers every slot, wrong scene/keyword, inactive entries, signed positions,
metadata/write isolation, and reproduces old fixed-cell X/width by executing
the original arithmetic. Packaging tests prove baseline and v1 converge on
identical v2 bytes and reject altered input. Native renderer integration and
actual on-screen behavior still require user testing.

### Secondary path

`test_link_background_layout.py` executes the emitted instructions for all
256 slots, replacement of a reused slot, bounded invalid-index reads, and
exact metadata preservation. Width samples run the actual VWF glyph stub
with different pitch and quad sizes, including Kurara, other names, long
terms, narrow/wide English and Japanese. In-memory executable patching checks
allowed byte ranges and source guards. This is not in-game visual validation;
the next authorized build must be tested on the reported Back Log screen and
dialogue links, scrolling and switching between short/long selected entries.
