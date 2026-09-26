# Writing English into this game

Everything here was confirmed **in-game**, not inferred.

## English must be FULLWIDTH

The game's font has no halfwidth ASCII glyphs. Write a line in halfwidth and
the renderer consumes single bytes as double-byte lead bytes, producing
unrelated kanji.

Test run with all three on screen at once:

| written as | rendered |
|---|---|
| `シン` (control) | correct |
| `ＡＢＣ　ＴＥＳＴ` fullwidth | **clean Latin** |
| `ABC TEST` halfwidth | `閉裏槽数` — garbage |

So every line of English goes through `tools/fullwidth.py`.

This is the same reason the PS2 project's menu text used fullwidth `．` and
`０` "on purpose". There it was a menu-renderer quirk; here it is every string.

## The cost: two columns per character

A fullwidth character is **2 columns**. English is therefore about twice as
wide as it looks, and line budgeting is the main constraint on the whole
translation — far more limiting than anything in the file format.

```sh
python tools/fullwidth.py --width "Look, everyone!"
#   Ｌｏｏｋ，　ｅｖｅｒｙｏｎｅ！
#   columns: 30
```

Working budget: **34 columns** per line, inherited from the PS2 project and so
far consistent with what fits. It has not been measured precisely on PS3 — find
the real wrap point before committing to it.

Rough guide: about **15 English characters per line**. Translations have to be
tight. "Look at that, everyone!" is 46 columns and will not fit; "Look,
everyone!" is 30 and does.

## Characters cp932 cannot encode

`tools/fullwidth.py` substitutes automatically:

| wanted | used instead |
|---|---|
| `'` | `’` (cp932 0x8166) |
| `"` | `”` |
| `-`, em dash, en dash | `－` |

Apostrophes are fine — `Ｉｔ’ｓ` encodes and renders. Em dashes do not exist.
`check()` returns anything still unencodable; never ship a line it flags.

## Record shape

Dialogue is a Lua long-bracket string:

```lua
{WPos_B, 3, FDMode_Normal, pid_SIN,
[[シン
「見ろよ、みんな！
　俺達の地球だ！」]],
 0, NULL},
```

- **Line 1 is the speaker name and is structural.** Translate the name, never
  turn it into a sentence. Exactly the PS2 rule, and it still holds.
- Dialogue is wrapped in `「」`, which render correctly — keep them.
- Continuation lines are indented with a fullwidth space `　`, not a halfwidth one.
- Because these are Lua strings and not pointer-table records, **changing the
  length is free.** No relocation, no pointer rewriting. This is the single
  biggest advantage over the PS2 game.

## The game does not use system fonts

Checked, so nobody repeats it: the decrypted `EBOOT.elf` (8.7 MB) contains
**zero** references to `cellFont`, `cellFontFT`, `libfont`, `/dev_flash/data/font/`,
or any `SCE-PS3-*.TTF` name, and the game ships no TTF or OTF of its own.

Firmware 4.9300 does install a full set of Latin and Japanese system fonts, but
this game never loads them. Dropping a different TTF anywhere will do nothing,
and there is no font option to expose in the UI because there is no font system
behind it. Text is drawn from the game's own bitmap glyph data.

Decrypt the executable with `rpcs3 --decrypt EBOOT.BIN` to re-check.

## Texture container format

Two wrappers appear in the CPKs, sharing a 0x80 header:

| offset | field |
|---|---|
| 0x00 | magic — `02 02` (game wrapper) or `01 05` (PS3 GTF) |
| 0x04 | u32 payload size, excluding the header |
| 0x0B | u8 texture count |
| 0x18 | u8 pixel format (`0xA5` = 32bpp, `0xAB` = 16bpp seen) |
| 0x20 | u16 width |
| 0x22 | u16 height |

Confirmed by arithmetic: 1536x256x4 = 1572864 and 1280x720x4 = 3686400, both
exact against real payloads.

`tools/tex.py` decodes these to PNG. **If a dump comes out as horizontal
stripes, the pixel format is wrong** — that is what 32bpp data looks like read
at 8bpp, and it cost several wrong guesses here before the header was decoded
properly.

## Where the dialogue font is NOT

- `DATA/TABATA/TPACKPS3.CPK` holds 124 pages at 1536x256 RGBA plus a few
  larger ones. Sampled pages are large display glyphs and UI artwork, not the
  24px dialogue grid.
- `DATA/HIYAMA/KANJI-FIX.BN` is 12416 bytes, dominated by Shift-JIS lead bytes
  (0x88-0x9F). 6208 two-byte entries, but they do **not** decode as an ordered
  charset (63% valid, scrambled order), so it is more likely a remap/fix table
  than a glyph inventory.

The dialogue atlas is still unlocated. `tools/tex.py` is what makes the search
tractable — sweep the CPK texture members and look for a regular grid of small
cells.
