# Rebuilding an ITOC CPK

## Existing tools do not do this

Checked before writing anything, and the answer was no:

| Tool | ITOC write |
|---|---|
| [YACpkTool](https://github.com/Brolijah/YACpkTool) | no ITOC support at all |
| [CriPack](https://github.com/JFG99/CriPack) (JFG99) | `WriteITOC` only in commented-out lines |
| [CriPakTools](https://github.com/esperknight/CriPakTools) | calls `WriteITOC` |
| [cpk-tools](https://github.com/ConnorKrammer/cpk-tools) (LibCPK) | implements it — **but the output is wrong** |

LibCPK was built here (retarget to .NET 4.8.1 + Windows SDK 10.0.26100, and
reference JFG99's prebuilt `LibCRIComp.dll` — the native C++/CLI project cannot
link without `MSCOREE.lib`, which needs the .NET Framework SDK component).

Its **reader is correct**: it agrees with `tools/cpk.py` on all seven members
of `STG0002`, sizes and offsets.

Its **writer is not**. Rebuilding an ITOC archive writes the content region on
**0x800 boundaries** while leaving the ITOC describing the packed layout. The
CRILAYLA headers end up at `0x1000, 0x1800, 0x3800…` while the metadata still
implies `0x9a0, 0xbb0, 0x2a70…`. ITOC has no `FileOffset` column, so a reader
*must* recompute positions — and CriPakTools' own `-l` on its own output points
at padding. The file is self-inconsistent.

That is why `tools/cpkpatch.py` exists.

## The layout rule

Verified against every member of an untouched `STG*.SDAT`:

- Members sit **back to back from `ContentOffset`**, in ID order.
- Each is padded up to `Align` (16).
- **No pad after the final member** — the file ends flush. `0xD880 + 504 =
  55928 = EOF`.

## Header size fields

Decoded by arithmetic against a real archive, not guessed:

| field | value |
|---|---|
| `ContentSize` | aligned total **including** the final pad the file omits (53472) |
| `EnabledDataSize` | `sum(FileSize)` — stored sizes (53444) |
| `EnabledPackedSize` | `sum(ExtractSize)` — unpacked sizes (287950) |

Getting `ContentSize` wrong is invisible until something reads past the end.

## Storing replacements uncompressed

`cpkpatch.py` writes replaced members with `ExtractSize == FileSize`, which the
format allows and which avoids needing a CRILAYLA **compressor** — only the
decompressor was ever required. Untouched members keep their original
compressed bytes verbatim.

The catch: `DataL` holds sizes as **u16**. An uncompressed member over 65535
bytes must live in `DataH`, and moving an entry between the two sub-tables
changes their shapes. `cpkpatch.py` refuses with a clear error rather than
silently truncating. For `STG0002` no member needs to move — the two large
ones are already in `DataH`.

## Verification status

```sh
python tools/cpkpatch.py in.cpk out.cpk                        # no-op
python tools/cpkpatch.py in.cpk out.cpk --replace 3=new.lua    # replace
```

- **No-op rebuild is byte-identical to the source.** Change nothing, get the
  same file back. This is the gate — if it ever stops holding, the layout or a
  header field is wrong.
- **Replacement**: all six untouched members decompress bit-for-bit identical,
  and the replaced member matches its input.
- **Full chain passes**: Lua -> CPK -> SDAT -> CPK -> Lua returns the input
  exactly.

Still **not** proven: that the game accepts any of this. Every test above is
offline. The in-game check is a stage-1 rebuild, re-encrypted, dropped into
`DATA/STAGE`, booted.

## DataL -> DataH: when a replacement outgrows 16 bits

The ITOC keeps two size tables: `CpkItocL` (ID, FileSize, ExtractSize as
u16) and `CpkItocH` (same columns, sizes as u32). The game's own archives
put a member wherever its sizes fit -- STG0004's member 3 ships in DataH
because its uncompressed Lua is 67,917 bytes. The reader merges both
tables and sorts by ID, so which table a member sits in does not affect
layout.

English made this a writer's problem: stage 3 member 3 grew to 68,031
bytes uncompressed (replacements are stored uncompressed), overflowing
DataL's u16 columns. `cpkpatch.build` now detects that and moves the row:
`_rows_edit` splices the fixed-size row area of a sub-@UTF (adjusting its
size and string/data offsets), `_move_to_datah` removes the row from
CpkItocL, inserts it ID-sorted into CpkItocH, rewrites the parent's data
region in place (the chunk grows a few bytes into its own padding --
ContentOffset never moves), and updates FilesL/FilesH, both blob
descriptors, the @UTF size, the LE chunk size and header ItocSize.

Proven by round trip: a 68 KB dummy through the patcher, then every
member of the result decoded byte-identical against the source.
