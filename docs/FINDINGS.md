# Format findings — SRW Z3 Jigoku-hen (PS3, BLJS10256)

Recon notes from opening up the disc. Everything here was verified against a
dump, not inferred from the PS2 game.

## The chain

```
PS3_GAME/USRDIR/DATA/STAGE/STG*.SDAT
   |  NPD container, SDAT flag 0x01000000
   v  rpcs3 --decrypt          (tools/unsdat.py)
CPK archive, ITOC layout
   |  CRILAYLA-compressed members
   v  tools/cpk.py             (tools/extract_stage.py)
Lua source, cp932, CRLF
```

Every layer is a documented CRI or Sony format. Nothing here needed the
clean-room reverse engineering that `banlz.py` needed on the PS2 game.

## Layer 1 — SDAT

`STG*.SDAT` are NPD containers. The header at 0x80 reads:

| field | value |
|---|---|
| flags | `0x0100003C` |
| block size | 16384 |
| NPD version | 4 |
| license type | 0 |

Bit `0x01000000` is the **SDAT** flag. SDAT derives its key from its own NPD
header, so it decrypts offline — no console account, no RIF, no klicensee.
This is the single fact that makes the project possible; EDAT would have
required a license tied to a real PSN account.

`COMPRESSED` (bit 0) is clear, so there is no codec under the crypto.

RPCS3 ships a working decryptor (`--decrypt`). Use it rather than
reimplementing PS3 crypto — `tools/unsdat.py` drives it in batches. RPCS3 is
single-instance, so close it before running.

## Layer 2 — CPK

Decrypted STAGE files are CRI **CPK** archives, `CPKMC2.42.00`.

They use the **ITOC** layout, not the named TOC: `TocOffset` is 0 and
`ItocOffset` is set. ITOC members have no filenames — only an ID, a size and
an extract size. Files sit back to back from `ContentOffset`, each padded up
to `Align` (16). A CPK reader that only handles named TOCs silently reports
zero files here, which is exactly what happened first.

Sizes come from two sub-tables inside the ITOC: `DataL` (16-bit) and `DataH`
(32-bit). Both must be read; either alone loses files.

## Layer 3 — CRILAYLA

Every STAGE member is CRILAYLA-compressed. It is an LZ variant that emits its
output **back to front**, reading its bit stream backwards from the end of the
compressed block, with a raw 0x100-byte prefix stored after the compressed
data. Implemented in `cpk.py:decompress_crilayla`.

Verified: all seven members of `STG0002` decompress to exactly their declared
`ExtractSize`.

## Layer 4 — the script is Lua

The scenario is shipped as **uncompiled Lua source** in **cp932**, CRLF line
endings, no NUL bytes.

One member names its own origin in a header comment (`out/stage0002preset.lua`);
most do not, so classify by content, not by declared name. A fixed-size head
slice will cut a two-byte cp932 character in half and make text look binary —
tolerate a decode error in the last two bytes of the window.

`STG0002` breaks down as five Lua members and two NUL-heavy binary tables.

Named command vocabulary seen so far: `Cmd_BGM_Play`, `Cmd_SE_Play`,
`Cmd_BI` / `Cmd_BO`, `Cmd_Black_Flash`, `Cmd_Clear_Face_ThePos`,
`Cmd_SetupForBGNameDraw`, `Cmd_IsLongSkipping`. Table blocks include
`TOUROKU_*`, `SCRAMBLE_*`, `CURPOS_TBL`, `BTLMESS_TBL`. AI definitions live in
their own member (`ns_MtAiDef`, `t_aitk_*_def`).

## What carried over from the PS2 game

Verified present in Z3, so the SRW-Z rules likely still apply:

- **`《》` keyword-bank links** — 13 balanced pairs in one scenario member
  alone. If the PS2 behaviour holds, a link with no bank entry **crashes the
  scene**, and a term plus its links is ONE edit.
- **`$` placeholders** — `$n` (77 uses in one member), `$F`, `$l`, `$D`, `$R`,
  `$A`. Same family as the PS2 game. Expanded widths must be re-measured for
  PS3; do not assume the PS2 column counts.
- **cp932** — the same encoding, so the same character availability limits
  (no em-dash, no curly quotes, no umlauts).

## What did NOT carry over

- **`banlz.py`** — the PS2 custom LZ. Z3 uses CRILAYLA. Irrelevant here.
- **Pointer tables.** The PS2 game's worst failure mode — an edit that moved
  bytes inside a record and orphaned its pointer table, producing an image
  that booted and then froze on save load — has no analogue in a plain-text
  Lua script. `verify_pointers.py` does not port.
- **Disc image surgery.** PS3 games are a folder tree. No ISO rebuild, no
  `chdman`, no sector alignment.
- **ELF patching**, as it stood. `EBOOT.BIN` is a PPC SELF (`SCE\0` magic) and
  decrypts with `rpcs3 --decrypt`, but it is a different architecture and
  toolchain.

## Not yet investigated

- Re-encrypting SDAT after an edit. This is the open risk — see README.
- Where non-scenario text lives (menus, unit names, the library). Candidates:
  `DATA/TABATA/TPACKPS3.CPK`, `DATA/AIDDATA/AIDDATAPACK.CPK`,
  `DATA/KURODATA/KDATAPS3.CPK`.
- Font and glyph tables; whether a variable-width Latin font can be added.
- `DATA/MAPETC/**/*.TXT` are UTF-8 tab-separated spreadsheet exports
  (`[Sheet1]` header) — a **different encoding** from the Lua script.
- `DATA/FACE/FC.BIN` (92 MB) — portrait atlas, format unknown.
