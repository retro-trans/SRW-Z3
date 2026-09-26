# Writing changes back

Research notes. **Read this before building any repacking tool** — most of
this problem is already solved by the community, and the first instinct here
(roll our own) was the wrong one.

## The established workflow

The documented route for translating a PS3 game whose data is in SDAT is:

```
decrypt SDAT  ->  edit  ->  RE-ENCRYPT to SDAT  ->  overwrite in USRDIR
```

Re-encryption is **mandatory**. This was tested here, not assumed: dropping a
plaintext CPK in place of `STG0001A.SDAT` / `STG0001B.SDAT` and booting gets

> ゲームデータが壊れています。ゲームを終了して、ゲームデータを削除してください。
> ("The game data is corrupted. Quit the game and delete the game data.")

So there is no plaintext pass-through shortcut, on RPCS3 or anywhere else.
Note the control for this test was inconclusive — see "Unfinished" below.

## Tools to use instead of writing our own

| Layer | Tool | Notes |
|---|---|---|
| SDAT | [`make_npdata`](https://github.com/aniruddh22/make_npdata) (Hykem) | encrypt/decrypt/bruteforce; **compression not implemented** — irrelevant to us, our files have `COMPRESSED` clear |
| SDAT | [TrueAncestor EDAT Rebuilder](https://www.psx-place.com/resources/trueancestor-edat-rebuilder-by-jjkkyu.34/) | GUI; the one most translation guides actually use |
| CPK | [CriPakTools](https://github.com/esperknight/CriPakTools) | list/extract/**update** CPK contents |
| CPK | [CriPack](https://github.com/JFG99/CriPack) | rewrite of CriPakTools; fixes header handling on update |
| CPK | [YACpkTool](https://github.com/Brolijah/YACpkTool) | extract/pack/patch, CLI + drag-and-drop |

`tools/cpk.py` in this repo stays useful as a **reader and verifier** — it is
how we inspect what a repack actually produced. It should not grow into a
writer while `CriPack` exists.

## CRITICAL: make_npdata v3/v4 encryption is broken

`make_npdata -e` with `<version>` **3 or 4 produces files the game and RPCS3
both reject**, even though make_npdata itself decrypts them back perfectly.
Versions **1 and 2 work**.

The originals are version 4, so the obvious parameter is the broken one. This
cost a black screen and a wasted boot cycle before it was found.

| version | RPCS3 | payload |
|---|---|---|
| 1 | accepts | matches |
| 2 | accepts | matches |
| 3 | **rejects** | -- |
| 4 | **rejects** | -- |

Use `2`. Confirmed in-game: a v2-encrypted rebuild of `STG0001A` loads and
renders edited text.

## The acceptance oracle

`rpcs3 --decrypt` is a **fast oracle for "will the game accept this"** --
seconds, no gameplay, no title screen. If RPCS3 will not decrypt a file we
produced, the game will not load it either.

```sh
rpcs3.exe --decrypt candidate.SDAT     # a .unedat appears == accepted
```

**Close RPCS3 first.** It is single-instance, so running the oracle while the
game is open silently produces no output and looks exactly like a rejection.
That false negative wasted a cycle here.

Validate the oracle itself against an untouched file before trusting a run.

## The make_npdata command for these files

`make_npdata -e` takes its parameters positionally:

```
make_npdata [-v] -e <input> <output> <version> <license> <type>
                  <format> <block> <compress> <cID> <klic> [rap]
```

Mapped to the header values actually read from `STG*.SDAT`:

| parameter | value | why |
|---|---|---|
| `<version>` | `2` | headers read 4, but **v4 output is rejected** -- see above |
| `<license>` | `0` | Debug license — this is what SDAT uses |
| `<type>` | `00` | Common; app type field reads 0 |
| `<format>` | `1` | 1 = SDAT (0 would be EDAT) |
| `<block>` | `16` | header block size is 16384 = 16 KB |
| `<compress>` | `0` | `COMPRESSED` flag is clear in the originals |
| `<klic>` | `0` | no key — SDAT is self-keyed |
| `<rap>` | omit | only for local licenses |

So, per stage:

```sh
make_npdata -v -e rebuilt.cpk STG0002.SDAT 4 0 00 1 16 0 <cID> 0
```

`<cID>` (content ID) is worth checking: the originals carry an **empty**
content ID, so passing a dummy may or may not round-trip identically.

## Validating a repack — RESOLVED

`make_npdata` was built here with MSVC (`cl /O2 *.c` over the `Linux/` sources;
only 64-bit printf format warnings). Three tests, all run against real files:

**1. Its decrypt agrees with RPCS3.** Decrypting `STG0002.SDAT` with
`make_npdata -d ... 0` produces output byte-identical to `rpcs3 --decrypt`.
Two independent implementations agreeing is good evidence both are right.

**2. Re-encryption is NOT deterministic.** Encrypting the same plaintext twice
gives two different files. For SDAT the key is `npd->digest XOR SDAT_KEY`, and
the digest at 0x40 is key material generated per run — so `digest`,
`title_hash` and `dev_hash` (0x40-0x6F) differ every time, and with them ~99%
of the encrypted payload.

**A rebuilt SDAT can therefore never be byte-identical to the original, and
does not need to be.** The key travels inside the header; that is what
"self-keyed" means. Do not chase a byte-identical rebuild — it is not a
achievable goal and its absence is not a bug.

**3. The functional round-trip is exact.** encrypt -> decrypt returns the
input plaintext byte for byte, still a valid CPK:

```sh
make_npdata -d orig.SDAT  plain      0
make_npdata -e plain      new.SDAT   4 0 00 1 16 0 "" 0
make_npdata -d new.SDAT   plain2     0
# plain == plain2, verified
```

Note the **empty content ID** (`""`): the originals carry an all-zero content
ID, and passing a dummy string writes it into the header where it does not
belong. The output filename does not affect the hashes.

What this does **not** yet prove: that the *game* accepts a re-encrypted
container. It should — SDAT is self-keyed by design — but it is untested.
## Unfinished

- The pass-through test's **control run never completed** — after restoring
  the original files the game hung at "Analyzing PPU Executable". The failure
  message is almost certainly caused by the swap (it is exactly what the
  community workflow implies), but it has not been proven that the same build
  boots clean with originals restored. Re-run the control; the first run may
  also have left state in `dev_hdd0/game/BLJS10256_DATA`, which the on-screen
  message explicitly told us to delete.
- **The CPK layer.** Rebuilding a CPK with edited members is still untested;
  use `CriPack`, not a homegrown writer.
- **In-game confirmation** that a re-encrypted SDAT boots. The SDAT layer is
  proven in isolation only.

## Prior art on the translation itself

Do not start the English script from zero:

- [Saint-ism — SRW Z3 Jigoku-hen Translation Project](https://www.saint-ism.com/2014/05/super-robot-wars-z3-jigoku-hen-translation-project/)
  — script translated through roughly chapter 10.
- [GBAtemp — menu translation for Z3 Jigoku-hen](https://gbatemp.net/threads/menu-translation-super-robot-wars-z-3-jigoku-hen.522161/)
- [Akurasu — list of English-translated SRW games](https://akurasu.net/wiki/Super_Robot_Wars/List_of_all_English_translated_SRW_games)
  and its terminology pages, already a source in the PS2 project's glossary.

The PS2 project's `glossary_sources.json` precedence rules apply: akurasu
contradicts itself in places, so record provenance rather than trusting a
spelling because it appeared somewhere.
