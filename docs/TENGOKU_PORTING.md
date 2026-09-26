# Tengoku-hen technical transfer assessment

Inspected 2026-09-11. This is a source-format comparison, NOT proof that a
patched Tengoku-hen build boots. No game, emulator, saves, or files in the new
project folder were modified. That folder was empty at inspection time.

## Source and destination

- New project: `E:/Projects/SRW Z3 2`
- Source ISO: `E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Tengoku-hen (Japan).iso`
- ISO size: 4,888,199,168 bytes.
- PARAM.SFO confirms title ID **BLJS10299** and the Japanese Tengoku-hen title.
- Jigoku-hen reference: original Japanese ISO in the same directory, BLJS10256.
- Existing toolchain: `E:/Projects/SRW Z3/tools`.
- Probe artifacts: `work/tengoku_probe/comparison.json` and `details.json` in
  the Jigoku-hen project. Extracted game bytes remain in ignored `work/`.

## What was actually verified

| Layer | Jigoku-hen | Tengoku-hen | Transfer decision |
| --- | --- | --- | --- |
| Disc | ISO9660/Joliet readable | ISO9660/Joliet readable, one multi-extent file | Extend ISO extraction first |
| Scenario packaging | 153 separate files under DATA/STAGE | One STGZ3OF2.SDAT | Replace stage discovery and mapping |
| Scenario archive | SDAT -> ITOC CPK -> CRILAYLA -> cp932 Lua | Same chain; 876 members extracted with no declared-size mismatches | Readers reusable; writer/runtime still need testing |
| Core text | RPW_DATA.CPK, 24 tagged chunks, 4,565 j-strings | Same ordered chunk names, 5,535 j-strings | Reader works; rederive binary record/pointer layouts before writing |
| Encyclopedia | KW/PT/RT CPK, special XOR 0x5e, tagged fields | Same decoded magic/field families | Reader works; IDs/content differ |
| Font archive | TPACKPS3.CPK, 129 members | 135 members | Re-inventory artwork |
| Font pages | Members 1 and 3, format 0xab, 4096x1120 | Same IDs/format/dimensions; different hashes | Font tooling useful; do not reuse old free-cell allocation |
| Battle dialogue | 276 blocks; 2,192,672 bytes | 368 header-derived candidate blocks; 3,499,808 bytes | Generalize parser; independently locate executable table |

Tengoku's SDAT header is NPD v4, flags 0x0100003c, 16,384-byte blocks.
Existing `work/make_npdata.exe -d input output 0` successfully decrypted a
workspace copy without starting or stopping RPCS3. The resulting archive has
876 ITOC members, alignment 16, CPK version string CPKMC2.47.02 / DLL3.17.00.
All 876 members decompressed to their declared sizes. Of these, 716 were
NUL-free cp932 text; the existing Lua reader found 66,919 long-string records
in 283 members. These are parser counts, NOT an audited count of story lines
or stages: comments, non-dialogue text, speaker/event binding and stage
grouping still need dedicated validation.

The same library reader parsed sample records from all three archives:
143 keyword entries, 539 pilot entries and 331 robot entries. This establishes
format compatibility, not that every entry has been semantically audited.

Battle-file scanning finds 368 aligned 03 4a block headers. Applying the
header/count array walk gives zero block-boundary or cp932 failures, 78,302
line references and 37,187 distinct strings. This is strong data evidence,
but NOT an executable-verified block map. Do not replace NBLOCKS with 368
and assume the rest of `srvc_blocks.py` is portable.

## Important ISO extractor issue

`DATA/BTLC/WP.CPK` is one file with two ISO9660 extents:

- LBA 377399: 1,073,739,776 bytes, flags 0x80 (more extents follow).
- LBA 901686: 506,946,704 bytes, flags 0x00 (last extent).
- Logical file size: **1,580,686,480 bytes**.

Current `isoread.py` yields these as duplicate paths. Its `extractall` would
write the second piece over the first. Add multi-extent aggregation and
streamed reads before extracting the whole disc. Do not collapse a listing
into a dict keyed by path unless extents have already been grouped.
ISO packaging must also handle multi-extent records if replacing such a file.
Unchanged multi-extent files can stay in their original sectors.

## Knowledge/tools worth transferring

1. **Container readers and rebuilding methods:** `cpk.py`, `cpkpatch.py`,
   `isoread.py` after the fix, SDAT tooling, and unchanged-member verification.
   CPK writers must be round-trip tested against Tengoku originals first.
2. **Lua translation workflow:** `luarec.py`, `patch_lua.py`, source hashes,
   glossary expansion and placeholder/link checks. Adapt stage discovery and
   create a member-to-stage index for the single combined archive. Do not use
   Jigoku's hard-coded stage manifest/deploy tables.
3. **Glossary and translation memory:** canonical spellings, identities and
   reviewed translations; use Japanese plus speaker/context/field type to
   propose matches, not numeric record IDs.
4. **Font/VWF methods:** atlas inspection, glyph rendering, width measurement,
   and PPC stub implementation concepts. Find all Tengoku hook sites, tables,
   segment layouts and safe memory ranges independently before patching.
5. **Data formats:** RPW tagged chunks and pointer-column discovery, library
   XOR fixed-point rule, battle block/count/pool model, GTF/artwork inspection.
6. **Validation/release practices:** byte-preservation checks outside intended
   regions, paired EBOOT/SRVC checks, context-aware mission-condition audits,
   image/layout QA, manifest hashes, patch decode verification and automatic
   build numbering. Use a separate version history for this separate game.

Potential text reuse measured in pristine sources:

- **2,971 exact shared nonempty RPW Japanese strings.**
- **20,198 exact Japanese strings** in Tengoku's voice file also occur in
  Jigoku's extracted voice source. This is about 54% of Tengoku's 37,187
  distinct strings, but includes possible silence/placeholders and does not
  mean 20,198 reviewed translations are automatically importable.

Reuse requires matching speaker/context and resolving conflicting English
translations. Unit/pilot IDs, section indices and source offsets are not
portable. Mission objectives and failure events need separate wording even
when their Japanese surface form is similar.

## Do not copy as working patches

- Jigoku's `eboot.py` addresses, branch targets, register assumptions, TOC
  offsets, segment extensions, blank-font-cell mapping and padding codes.
- `srvc_blocks.py` TABLE_OFF=0x830be0 or its fixed 276-block table.
- Encoded SRVC, font atlases, EBOOT, built CPK/SDAT files, or release outputs.
- Artwork member IDs, pixel rectangles or original-file fingerprints.
- Deployment game IDs, cache folders, fixed file lists or stage manifests.
- Historical handoffs verbatim: `docs/FINDINGS.md` is early reconnaissance,
  while `docs/VOICE_HANDOFF.md` still describes the retired in-place writer.
  Later code/handoff sections supersede their claims that relocation cannot
  work. Correct rule: rebuild each pool and update every validated consumer;
  never append beyond the bytes the runtime actually loads.

## Fresh checks still required

- Decrypt Tengoku's executable in an isolated workspace; no live RPCS3
  interruption is authorized by this assessment.
- Locate and validate font routines, character mappings, keyword rendering,
  battle table location/count, buffer sizes and all loader references.
- Determine how STGZ3OF2 members map to stages and whether another offset
  table must change when rebuilding the combined archive.
- Audit RPW binary record schemas before repointing any strings.
- Locate terrain and artwork assets (map and sound archive names/layouts
  changed); remeasure every translated UI class.
- Confirm SDAT re-encryption in-game. Jigoku required version 2 despite
  pristine version 4; that is a warning to test, not a proven Tengoku setting.
- Establish a clean boot and a one-line round trip before large translation.

## Carry over the installed-cache lesson

On 2026-09-10 the Jigoku 0.6.1 ISO contained the correct paired executable
and translated SRVC. However, RPCS3's installed DATA0046.DAT still exactly
matched the original Japanese SRVC (2,192,672 bytes), while the executable
expected 3,032,400 bytes. That pairing gives wrong signatures for 274/276
block starts and explains the missing-dialogue failure mode. Runtime recovery
after the user's cache deletion has not yet been reported.

For Tengoku, discover the actual installed-data identity/path and verify
hashes. Never clear Jigoku's cache while deploying Tengoku; never touch save
data. Prefer backing up obsolete installed game data before reinstalling.

## Recommended initial transfer

Seed the new folder with this handoff, curated format documentation, safe
reader utilities, a copy of the glossary and separate project configuration.
Treat all writer/build/deploy entry points as disabled until Tengoku-specific
addresses, file discovery and runtime checks are established. Do not clone
Jigoku's executable patch configuration and change only its title ID.
