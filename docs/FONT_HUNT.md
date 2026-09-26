# The dialogue font — FOUND

**Located: `DATA/TABATA/TPACKPS3.CPK`, the two 16bpp members (format byte `0xAB`).** This records where it is *not*, so the search is not
repeated, and what the live leads are.

## Why this matters

The dialogue renderer consumes bytes strictly in **pairs** (proven: `ABC TEST`,
8 bytes, rendered as exactly 4 kanji). There is no single-byte path, so:

- halfwidth ASCII and halfwidth katakana are both dead ends
- fullwidth Latin renders correctly but gets a full em cell per letter, which
  is why English looks spaced out

## Ruled out — verified, do not re-check

| Candidate | Result |
|---|---|
| PS3 system fonts (`cellFont`/`cellFontFT`) | **No.** The decrypted 8.7 MB `EBOOT.elf` has zero imports. The two `CELL_SYSMODULE_FONT` hits are a sysmodule enum-name table, not calls. |
| A TTF/OTF shipped with the game | None exist anywhere in the disc tree. |
| `TPACKPS3.CPK` (124 pages) | All 1536x256 **32bpp RGBA**. Sampled pages are large display glyphs and UI art. No 8bpp, no grid signature. |
| `AIDDATAPACK.CPK`, `KDATAPS3.CPK` textures | Same — 32bpp RGBA only. |
| `KDATAPS3.CPK` PNG members | 320x176 and 1000x560 **RGB** DLC banner art (sibling member starts `DLCHSRWZ`). |
| `COMMONDATA/**` | Keyword/zukan data and `LUACPK.CPK`. No textures. |
| Embedded bitmap in the EBOOT | Scanned for periodic glyph structure; no signal above noise. |

A font atlas would be **8bpp alpha/luminance** with a regular small-cell grid.
Nothing matching that has turned up in any small archive.

## Live leads, best first

1. **`DATA/BTLC/CMN.CPK`** — a single 4,143,072-byte member in an archive named
   "common", magic `03 00 00 00 10 00 00 00`. Custom format, internals not yet
   parsed. Best candidate.
2. **`DATA/KURODATA/D_CACHE.CPK`** — exactly 1,048,576 bytes and *not* a CPK.
   The name and size fit a runtime glyph cache (1024x1024 @ 8bpp). If the game
   rasterizes glyphs into a cache on demand, the source font is compressed
   somewhere else and `KANJI-FIX.BN` may be its fix-up table.
3. **`DATA/HIYAMA/KANJI-FIX.BN`** — 12,416 bytes, referenced by the EBOOT,
   dominated by Shift-JIS lead bytes (0x88-0x9F). 6208 two-byte entries that do
   **not** decode as an ordered charset, so likely a remap table.
4. The large battle archives (`BG`, `WP`, `PCI`, ...) — low prior, they are
   battle graphics, but unexamined.

## The strategic point

**Finding the atlas is necessary but not sufficient.** A new font fixes glyph
*shapes*; it does not fix the *advance*, which is one em per double-byte code.
Two ways to real proportional English:

- **Digraph glyphs** — redraw unused glyph cells so each holds TWO Latin
  letters, and encode English into those codes. Works with the fixed advance,
  needs no executable patching, and restores a sane column budget. Needs the
  atlas.
- **Patch the renderer** in `EBOOT.elf` for variable advance. True VWF and the
  best result, but PPC64 work on a decrypted SELF, and a naively narrowed
  advance would squash kanji too.

## Useful tools built along the way

- `tools/tex.py` decodes the texture container to PNG. Header: size at 0x04,
  count at 0x0B, format at 0x18 (`0xA5`=32bpp, `0xAB`=16bpp), w/h at 0x20/0x22.
  **Stripey output means the wrong bit depth**, not corrupt data.
- `rpcs3 --decrypt EBOOT.BIN` yields the ELF for symbol and string analysis.


---

# FOUND: the atlas

`DATA/TABATA/TPACKPS3.CPK`, members **id=1 and id=3**, format byte `0xAB`
(16bpp), **4096x1120** each. My earlier sweep missed them because the grid
detector required `w*h*4` bytes and so silently skipped every 16bpp texture.

Layout: a **32x32 cell grid**, 128 columns x 35 rows = **4480 cells per page**,
3892 inked. Row order follows JIS X 0208 -- symbols, then alphanumerics, then
kana/Greek, then Cyrillic, then kanji.

`tools/fontatlas.py` extracts both pages to PNG and measures every cell.

## The glyphs are ALREADY proportional

This is the key finding. Measured ink widths per 32px cell:

| ink width | cells | what |
|---|---|---|
| exactly 30px | 3281 | full-width CJK -- correctly full-width |
| <= 24px | 268 | Latin, punctuation, narrow forms |
| 5-8px | 10 | `i`, `l`, `.`, `!` and friends |

So **nothing is wrong with the font**. `i` is 8px and `h` is 24px, exactly as
they should be. The renderer simply advances one full 32px cell per glyph
regardless, which is the entire cause of spaced-out English.

**Do not author a new font.** The letterforms are good. The defect is the
advance.

## Every non-code route is closed, tested in-game

| route | result |
|---|---|
| System font swap | no `cellFont`/`libfont` imports in the EBOOT |
| Halfwidth ASCII | renders as paired kanji |
| Halfwidth katakana (`0xA1-0xDF`) | renders as **blanks** -- no single-byte path exists |
| Inline size/width control code | the engine's Lua vocabulary has no such command |
| `KANJI-FIX.BN` as a code/width table | **not** a code table; SJIS-validity scores ~52%, i.e. the random baseline |

## What remains: the advance

Only 268 glyphs need a narrower advance; the 3489 CJK cells stay at 32.
`metrics.json` from `tools/fontatlas.py` already provides every width.

Static search for the advance has **not** succeeded. Tried and failed:
- atlas geometry constants (`4096.0f`/`1120.0f`) -- the one tight cluster is a
  UI layout rect table for 1280x720, not font metrics
- SJIS lead-byte range checks (`cmpli`/`cmpi` against `0x81/0x9F/0xE0/0xEF`):
  91 compares exist but never 3+ distinct bounds in one window, so the decoder
  is not a plain range check

Next step needs **interactive** work, not static heuristics: run under RPCS3's
debugger, breakpoint the dialogue draw, and read the advance from the live
code. Once the instruction is known it becomes an RPCS3 `patch.yml` entry plus
a width table derived from `metrics.json`.

---

# The advance, measured

Confirmed by editing the atlas directly: **TPACK is a plain CPK on the disc, not
SDAT**, so `tools/cpkpatch.py` alone can replace the font. No encryption step.

Filling atlas row 2 (fullwidth lowercase) with solid full-cell blocks and
displaying `abcdef` in-game rendered six solid blocks -- confirming both the
cell mapping and that **atlas edits work**.

Measured from that capture at 1920x1080:

| quantity | screen px | at 1536 internal |
|---|---|---|
| glyph quad | 40.0 | **32.00** = exactly the atlas cell |
| advance | 46.6 | **37.28** |
| gap | 6.6 | ~5.3 |

So the renderer blits the 32px cell 1:1 and adds ~5.3px of fixed letter-spacing.
The advance does **not** vary with ink: the original Latin row has ink widths of
19/20/19/20/19/14 and still renders on an even pitch.

## Code -> cell mapping

Sequential over valid SJIS from 0x8140, 188 codes per lead byte (trails
0x40-0x7E and 0x80-0xFC, 0x7F skipped), 128 cells per atlas row:

```python
def seq(code):
    hi, lo = code >> 8, code & 0xFF
    trail = (lo - 0x40) if lo <= 0x7E else (lo - 0x41)
    return (hi - 0x81) * 188 + trail
cell = seq(code) + OFFSET      # OFFSET = 4, verified against uppercase/digits
```

Verified by rendering predicted cells: with `OFFSET = 4` the strip for
`0x8260..` reads A B C D E F G H I J and `0x824F..` reads 0 1 2 3 4 5 6 7 8 9.
An earlier `OFFSET = 5` guess came from a miscounted in-game block run; **4 is
correct**.

## Why enlarging the glyphs is only cosmetic

Filling each cell would drop the gap to ~14% of pitch, so English would read as
clean monospace instead of broken. But **it does not fit one more character per
line** -- still ~29 per line, because every letter still consumes a full em, the
same em a kanji gets. English needs roughly twice the characters of Japanese for
equivalent text, so density is the real constraint.

The genuine fix is halving the advance, which would give ~58 characters per line
**and needs no new font at all** -- the shipped glyphs are already properly
proportional (8px `i`, 24px `h`).

## What a fix requires

Change the ~37.28 advance to a per-glyph value from `metrics.json`. That is a
code change; no width table exists in the executable to edit (scanned: zero runs
of >=512 bytes in the 4..34 range anywhere in the ELF).

Static searches that did **not** find it, so nobody repeats them:
- atlas geometry constants -- the only tight cluster is a 1280x720 UI rect table
- SJIS lead-byte range checks -- 91 `cmpli`/`cmpi` against 0x81/0x9F/0xE0/0xEF,
  never 3+ distinct bounds in one window
- cell arithmetic (`idx >> 7` with `(idx & 127) << 5`) -- 17 and 0 hits, never
  co-occurring, so cell UVs are likely table-driven rather than computed
- per-glyph width table -- absent

Next step is interactive: breakpoint the dialogue draw in RPCS3's debugger and
read the advance from live code, then express it as an RPCS3 `patch.yml` entry.

---

# The EBOOT hunt, round two

Static constant-hunting is now **exhausted**, and this records the negative
results precisely enough that nobody repeats them. Tooling and addresses that
came out of it are at the bottom; start there.

## Binary mechanics (reusable)

Established once, needed by every future pass:

| fact | value |
|---|---|
| decrypted ELF | 8,774,352 B, PPC64 big-endian (`EM_PPC64`) |
| address mapping | `vaddr = file_offset + 0x10000`, uniform across both PT_LOAD segments |
| TOC base (`r2`) | `0x7dd920` |
| function pointers | PPC64 **OPD descriptors**, not code: `{entry, toc, env}` |
| symbol table | none — stripped; only RTTI names survive |

`rpcs3 --decrypt EBOOT.BIN` needs **no firmware**; SELF keys are built in.

## RTTI gives the renderer's class names

The earlier sweep only looked for `cellFont`/`libfont`. A general RTTI sweep
finds the actual classes, which the docs never had:

| class | RTTI name @ |
|---|---|
| `LibGpu::SpeakFont` | `0x6edf28` |
| `MtV::DialogueText` | `0x701c08` |
| `MtV::DialogueWindow` | `0x701c20` |
| `MtV::AbsText` / `AbsTextFactory` | `0x701b10` / `0x701b20` |
| `z2::mt::FontWrapper` | `0x7136f8` |

Walk it as: name string -> 32-bit ref (typeinfo) -> ref to typeinfo (vtable)
-> OPD -> code.

**`LibGpu::SpeakFont` vtable @ `0x79b5d4`**, methods at `0x10d45c`,
`0x10d52c`, `0x10d5a4`, `0x10f50c`. `MtV::DialogueText` methods resolve to
`0x1b78b0`, `0x1b78fc`, `0x1b7cd0`.

## What the advance is NOT

Each of these was run over the whole 6.3 MB `.text`, not a sample:

- **Not a float literal.** All 1127 distinct TOC float slots referenced by any
  `lfs` were enumerated. In 30.0-42.0 there are only whole numbers
  (30/31/32/37/38/40/42). No 37.28, no 37.33, no 37.5, nothing fractional.
- **Not derived from atlas geometry.** `1/35`, `1/1120`, `32/1120` and
  `1120.0` appear **nowhere** in the TOC float pool. So glyph UVs are not
  computed from the atlas dimensions -- confirming the table-driven theory.
- **No static cell table.** Scanned every `u16` run in the file: zero runs of
  >=24 entries stepping by 32 (cell pixel coords), and no 0..127 column run in
  a plausible table. The glyph table is **built at runtime** into `.bss`
  (3.7 MB, `va 0x869e80`), which is why nothing static ever matched.
- **No literal 192/188 stride.** No `mulli` by 192, 188, 189 or 128 anywhere.
  The cell index is not a literal multiply.

## Two false leads, killed with evidence

Recording these because both look compelling in a grep:

- **`1120.0f` cluster @ `0x84f3c8`** is a **1280x720 UI rect table**
  -- rects like `(160, 72, 1120, 624)` where `160 + 1120 = 1280`. The 1120 is
  a coincidence with the atlas height. (Confirms the earlier finding, and
  confirms the virtual space really is 1280x720.)
- **`31.0f` used 8x around `0x368fd4`**, next door to `0x81` compares, looks
  exactly like an advance beside an SJIS check. It is not: the surrounding
  constants are `1, 3, 7, 15, 31, 63, 127, 255, 1023, 4095, 32767, 65535,
  2^24-1, 2^31, 2^32-1` -- a **bit-mask ladder**. It is a vertex-format
  unpacker and `31.0` is a 5-bit mask.

## The live lead

A structural search (not a constant search) for two byte loads combined with a
shift-by-8 found 105 sites; two of them, `0x10de60` and `0x10e0c0`, are
**inside the SpeakFont region**.

Reading `0x10de30..0x10df90`: it byte-swaps LE `u16` fields out of a struct
(offsets 0x00, 0x02, 0x14, 0x16, plus `u8` at 0x18/0x19), multiplies a `u16`
by a `u8`, then at `0x10df54` does `divw` / `mullw` / `subf` -- an explicit
**modulo**, i.e. grid/cell arithmetic -- and divides again at `0x10df78` for
the row. That is cell-index math on a texture atlas, in the speech-font class.

It is Altivec-heavy and stack-heavy, so it wants a debugger rather than more
reading. **These are the addresses to breakpoint**, which is a far better
starting point than "breakpoint the dialogue draw".

## Tooling added

- `tools/isoread.py` -- pulls any file straight out of the disc image with no
  mounting and no emulator. `TPACKPS3.CPK` and `EBOOT.BIN` both come from here.

## Atlas: page 1 and page 3 are the same charset

Both pages ink **exactly the same 4480 cells** (588 blank in both, identical
blank pattern) with slightly different ink widths -- so page 3 is a second
**style layer** (outline/shadow), not extra characters. **Any atlas edit has
to go into both pages**, or the two layers disagree. `makefont.py` currently
writes only the first matching member and so patches one layer.

---

# SOLVED: two letters per cell

The advance cannot be patched, so stop trying to. What *can* change is what a
cell contains. `tools/digraph.py` puts **two Latin letters in every cell**, so
each letter costs half an advance. No executable patch, no new code path.

## The advance, measured properly at last

From a real dialogue frame (1920x1080 window, game rendering 720p), fitting
34 ink-edge observations across both lines, using each glyph's known ink box
from `metrics.json` to separate pitch from per-glyph bearing:

| quantity | value |
|---|---|
| pitch | **46.412 screen px** (rms 1.40, shared-origin fit) |
| cell | **34.96 screen px** = 32 texels, so 1.0924 px/texel |
| gap | 11.45 px = **24.7% of pitch** |
| **advance, game space** | **31.0 px** at 720p |
| **advance, texel units** | **42.48** for a 32-texel cell |

This supersedes the old `37.28 @ 1536 internal` figure, which came from a
solid-block test with an *assumed* internal resolution. 720p is confirmed from
the log (`cellSysutil: resolutionId=0x2`).

**The fit also proves the advance is uniform.** Pitch was held constant across
glyphs whose atlas ink runs 9-30 texels and the residual is 1.4px. If the
advance tracked ink at all, residuals would be ~17px. So there is no per-glyph
metric anywhere to patch -- the question is closed, not open.

## The geometry that makes it work

For an even rhythm the two letters must sit **half an advance** apart --
21.24 texels, *not* half a cell (16). Then the gap inside a cell equals the
gap between cells and the eye sees one even stream.

Both letters must also fit inside the 32-texel cell, which caps a letter at
`32 - 21.24 = 10.7` texels. `digraph.py` steps 20.6 and draws 11.4-wide
letters; the residual rhythm error (9.2 vs 10.5 texels) is under half a screen
pixel. A pair fills 71% of the cell -- the same coverage a kanji gets.

More letters per cell does **not** help: n letters need `(n-1)*42.48/n` texels
of centre span inside 32, so n=3 leaves 3.7 texels per letter. **Two is the
maximum.**

## Result

- **~29 characters per line -> ~58.** Line budget doubles.
- The gap after every letter disappears; spacing becomes even.
- Kanji are untouched.

## Codes

Pairs are assigned SJIS that English never needs, cheapest first:

1. **Unassigned but structurally valid** positions (blank cell, no character
   loses anything). Note `0x8140` is blank *and* the ideographic space -- the
   pool filter requires the code to fail `cp932` decode, not merely be blank.
2. Greek (48), Cyrillic (66), box drawing (32) -- inked but useless to us.

**634 free cells** without touching a single kanji.

## Verified

- Patched CPK re-reads clean: 129 members, **127 byte-identical**, only atlas
  ids 1 and 3 changed, target cells blank before and inked after.
- Offline render of the true engine geometry (32-texel blit at 42.48 pitch)
  is in `tools/digraph.py:simulate`, with `simulate_current` drawing the same
  line the way the game does today for a like-for-like comparison.
- Encoded output contains no `]]`, so it is safe inside a Lua long string.

## Both pages, always

Page 1 and page 3 ink the identical 4480 cells in two style layers, so every
edit goes into both. `makefont.py` patches only the first member it finds and
is wrong on this point.

## Confirmed in-game

A proof build (pairs drawn into the cells the shipped Japanese line already
uses, so no Lua edit and no SDAT re-encryption -- TPACK is a plain CPK) put
**"Look at that, sir!"** on screen in place of 「見ろよ、みんな！, in tight
evenly-spaced Latin.

Measured back off that frame, against the prediction:

| quantity | predicted | measured |
|---|---|---|
| letter pitch | 23.21 px | **23.45 px** |
| cell pitch | 46.41 px | **46.91 px** |

Within 1%. The word-space shows up as a clean 46.5px step -- a blank half-cell
-- which is the mapping doing exactly what it should.

The second line rendered `俺達の地球だr!」`: the proof map assigns `！` the
pair `r!`, and `！` occurs in both lines. That collision is expected and is
itself evidence the cell remap is exact. Real use takes codes from the
unassigned pool instead and never touches a character the script needs.


# Resolved: the advance is a parameter, and it is now per glyph

Everything above looked for a constant because the measurements said the
advance never varied. It never varied because every caller passes the same
one. The text API is small and lives at `0x13800..0x14b00`:

| entry | role |
|---|---|
| `0x13874(f1..f4)` | stores four floats into the global text state `0x869ef8` at `+0x54/+0x58/+0x5c/+0x60`: quad width, quad height, **x advance**, line advance (720p px) |
| `0x140f4` | the string drawer, 51 callers; `0x14a7c` is a jump to it |
| `0x14a80` | draws one glyph N times (gauges); not text |

`0x140f4` per character: reads two bytes, computes
`cell = (hi-0x81)*192 + (lo-0x40)` (`0x147d8`, the atlas formula), first
consulting a code->cell override table at `0x7ff8c8` (4-byte entries
`[code u16][row u8][col u8]`, 0-terminated), turns the cell into
`u = col*32, v = row*32`, snapshots the four size floats into stack slots
`0x9c/0xa0/0x94/0x98`, builds the quad, and at `0x14774..0x14780` does
`pen_x += stack[0x94]`. The dialogue caller passes 31 (hence 30.94 px at
720p, 42.5 texels), the library 30; the dialogue quad is 23.3 px for a
32-texel cell (the 3/4 that made library glyphs look 1.29x larger).

Found with RPCS3's GDB server (`tools/gdbbridge.py`; memory reads only, the
LLVM recompiler never traps breakpoints) by dumping data+bss and grepping for
31.0/42.5, then reading the caller with capstone (`tools/ppcdis.py`).

**The patch** (`tools/eboot.py`, `apply_vwf`): the one instruction
`lfs f13, 0x94(r1)` at `0x14778` becomes `bl 0x78c200`; the stub reads the
cell index still sitting in stack slot `0xc2`, looks up a 4,480-byte width
table at `0x78b000` (both in the segment-1 padding that the series-name
patch already maps), and returns the original advance when the width is 32
(every Japanese cell) or `W/32 * quad width` otherwise. Latin is therefore
one letter per cell at natural width, on every screen, with the same table.
Proven in-game: `--vwf-test 24` narrowed every English cell and nothing
else; the real build renders proportional Rodin on the library page.

The keyword-highlight layout (`MtV`, pieces positioned by a code count) is
the one other place that assumed a fixed advance; it now reads the pen
movement the drawer stub accumulates. See TRANSLATING.md, "Dialogue lines
with 《》 links".
