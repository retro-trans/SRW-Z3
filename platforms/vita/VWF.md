# Vita VWF development

## Packaged test01 (2026-09-14)

The coherent broad VWF test is built under work/vita/english_vwf_test_01.
It includes this executable hook plus the separately composed SRVC table,
matching fonts, story/UI/library/keyword/gameplay/battle content. All archive
readbacks pass; runtime remains unverified. See VWF_TEST_ZIP.md. Existing
candidate_01/02 and the old fixed-cell pilot are unchanged historical outputs.

## Native UI/help extension (2026-09-14)

`ui_text.py` composes VWF from the pinned original SELF and adds an exact-text
draw hook at0x81006e50, r7 after optional UTF-8 conversion. The104-byte stub
starts at0x812b5e7c inside the verified VWF reservation;0x812b5f38 holds a second
REL32 delta. Original VWF delta/width bank are untouched. A relative-offset
table starts at0x8168c620 after VWF scratch/BSS. One new SCE format0 REL32 entry
supports independent text/data loads; old segment VAs/relocation prefixes stay.

It replays `vmov.f32 s0, #-1.0`, preserves integer registers/flags except the
deliberate r7 output, and never changes an unmatched pointer. Full comparison
follows hashing. Native tables0x812d8ac0 (ASCII) and0x812b8ac0 (other UCS2)
determine converted key bytes. Native ASCII is two-byte font text, not raw ASCII.

The 32-byte wrapper at0x812b5ee4 also hooks0x810d9dd8 before MtV line counting
and splitting. It translates r2 through the same lookup, preserves original r2,
r7, LR, SP and s0/s1, handles NULL, and replays the displaced ADD flags and
stack store. Guarded source instructions and reservation bounds are checked.
Encoded English lines over256 bytes are rejected, not silently truncated or
given guessed wrapping; none of the current included keys exceed the limit.

1,510 checked keys cover menus/help/tutorials, 109 bare scenario-title keys
and28 additional heading/route labels. These are exact native string matches,
not title-texture edits or arbitrary composed episode headings. Twelve UI
tests execute generated code, independent relocation, register/flag safety,
hash collisions, large tables and original drawer/conversion logic. Original
MtV entry and line counter see translated multiline text; only imported strlen
is intercepted in that test. Imported UTF-8 decoding and GPU calls are intercepted
in drawer tests. Other fragmentation paths and live layout are still pending.

No executable or archive is written by this source extension. Existing
candidate_02 and pilot outputs remain unchanged. A future coherent builder
must combine UI+VWF, SRVC offsets, shared content and matching fonts. Do not
install an executable by itself. See COVERAGE.md for exclusions and audit.

The working pilot ZIP uses adaptive paired glyphs, not variable-width text.
The user confirmed opening dialogue renders and requested real VWF, reusing
the PS3 implementation. The new source is a development candidate only.
Do not install its EBOOT alone over old digraph fonts/scripts.

## Reuse and platform boundaries

Reuse `tools/digraph.py` single-letter rasterization (cap22, dilation0.5),
the same locally available PS3 Latin TTF source and the PS3 spacing algorithm:
sentinel32 means original advance; other widths advance by width/32 times the
current glyph quad width. Reuse actual pen accumulation for MtV pieces, with
columns in 1/128 pixel. Canonical English/glossary are shared and unchanged.

Vita-specific code: Thumb instructions/branches, original instruction guards,
SELF segment handling and native linear-P4 GXT cells. No PS3 binary addresses,
PowerPC instructions or texture payloads are carried over.

## Verified executable locations

Only plain pilot EBOOT SHA256
`14414068b44fa8ded7f9acb467dceddb4cd02c88845a4109a6e811960cc985d1`
is accepted. Its underlying decoded executable is PCSG00264 version01.00.

| Site | Purpose |
| --- | --- |
| 0x81006e10 | Original SJIS string drawer, analyzed and CPU integration-tested |
| 0x81007370 | Advance hook; r9=cell, s19=quad width, s21=pitch, s18=pen |
| 0x810da058 | Normal piece X: r11 base + r3 column |
| 0x810da0f2 | Mode1 piece X: r9 base + r3 column |
| 0x810da1fe | Linked piece X: r10 base + r3 column |
| 0x810da48a | Substitution X: r8 base + r11 column -> r7 |
| 0x810d9f4e | End piece: advance column by actual pixels, leave byte pointers intact |

Text ends at 0x812b5d54; data starts at 0x812b6000, leaving684 bytes.
Append code294 bytes, padding, one relative-address word and a192-byte width
bank in that verified gap. There is NO assumed zero-filled code cave.
Append four-byte float scratch at0x8168c61c after original data BSS. Materialize
the intervening BSS as zeros; original initialized bytes, virtual addresses,
segment indices, original relocation bytes and module entry are preserved. Repack
ELF file offsets to prevent expanded segments overwriting each other.
All six replaced instructions must match exact original four-byte encodings.
Append one12-byte SCE format0 R_ARM_REL32 entry to the final relocation segment
for the scratch delta. This is necessary because the
[Vita3K loader](https://github.com/Vita3K/Vita3K/blob/master/vita3k/kernel/src/load_self.cpp)
allocates load segments separately. The record uses the documented source
layout and REL32 rule in its
[relocator](https://github.com/Vita3K/Vita3K/blob/master/vita3k/kernel/src/relocation.cpp).
Original relocation records remain byte-identical prefixes, not replaced.

Only95 CP932-unassigned, blank cells in0x87xx are used. Both native font pages
are checked before writing; every other cell/header/palette is unchanged.
The table defaults to32, preserving original spacing outside those95 cells.
One glyph represents one printable ASCII character; no pairs or condensation.

## Checks and outputs

```powershell
C:/Python/python.exe tools/test_vita_vwf.py
C:/Python/python.exe -m unittest discover -s tools -p test_vita_*.py
C:/Python/python.exe platforms/vita/prepare_vwf.py
```

The last command is a dry-run. Explicit `--write --out work/vita/NEW_NAME`
writes loose development files only; refuses existing directories. No CPK
repack, complete ZIP, release, emulator install or saves are touched.
Current private output: `work/vita/vwf_candidate_02`, including labeled
offline `font_proof.png`, mapping, audit, EBOOT and five loose archive members.
This is not an installable package. Use a coherent future package combining
the executable, font pages and single-letter encoded dialogue.
Candidate_01 predates the independent-segment REL32 fix; retain as an analysis
intermediate but do not package it.

Ten VWF tests pass (38 total Vita tests, 55 focused including shared/CPK). They execute actual generated ARM
code: all192 bank entries and Japanese fallback at two load bases, preservation
of registers/flags/stack, four piece origins, fractional pixel accumulation,
independently relocated code/data, unknown/double-patch rejection and
segment/BSS integrity. Integration executes
the original decoder/lookup/drawing loop/newline handling with GPU calls
intercepted, proving the selected SJIS row reaches the hooked width bank.
This is CPU/structure validation, NOT Vita3K visual or loader validation.
All244 opening-stage records decode back to canonical English; controls and
all non-dialogue Lua bytes are identical. Four-line/960-texel budget is
conservative and provisional; the original256-byte MtV line limit is checked
separately, including placeholders and keyword markers.

## Still required before claiming a proper completed port

- Package and test coherently in Vita3K when the user requests a build;
  inspect the shown Kei dialogue, pink links, names, Back Log and skip flow.
- Keyword highlight and selection hit-box widths: record builder0x810d8cd8
  still stores byte length at record+4 and pitch at+6. Trace its consumers;
  do not assume the pixel accumulation hook already fixes their rectangles.
- Centering/measure function0x810077f4 and wrapper0x8100791e still use the
  original measurement rules. Port separately, including menu/name layouts.
- Wider translated content and UI need Vita-specific layout checks. This
  candidate still covers the opening244 records, not the entire PS3 port.

Analysis dependencies are local under ignored `work/vita/python_deps`:
Capstone4.0.2, Keystone0.9.2, Unicorn2.1.4 and prior PyCryptodome3.23.0.
`inspect_vwf.py` is read-only unless asked to create a private disassembly.
Thumb data/jump tables can be misread as code; verify known function starts.
