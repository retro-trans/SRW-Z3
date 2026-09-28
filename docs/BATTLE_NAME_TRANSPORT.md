# PS3 battle-caption name transport

September 26, 2026. Source-only fix; physical PS3/RPCS3 visual verification
still required after an explicitly requested build. User confirmed the
Mariemaia corruption screenshot comes from 0.6.21.

**September 29 correction:** the initial transport shipped in 0.6.22 crashed
at combat startup. Its instructions were incorrectly emitted into the
non-executable translation-data extension. Local RPCS3 reproduced a fault
at0xC8C4B8 from the name draw. Source now reserves RX space at0x78DC00..0x78DD00
after runtime-name data and before the search-layout helper. The data cursor
is unchanged; no LOAD is made writable/executable. This correction is not yet
built, installed or runtime-confirmed.

## Established cause

The native caption object has a **31-byte name array** at `+0xf94`, followed
immediately by dialogue at `+0xfb3`. Three native paths call unbounded
`strcpy` (`0x55a460`) into that name array:

- `0x1073e4`: selected speaker;
- `0x107494`: fallback/current speaker;
- `0x10767c`: alternate caption update.

Each obtains the name pointer from the shared speaker cache at `0x9af05c`,
pointer slots `+0x88 + 4 * index`. Registration at `0x10098c` retains the
supplied pointer unchanged (`0x100a58`). It does not allocate temporary
name text. Actor name selection at `0x10546c` returns the actor's `+0x24`
pointer and encoding flag; fallback setup at `0x1050c0/0x105118` uses the
executable display table. These backing strings already must remain live
through battle caption selection. The patch retains that same ownership;
it does not hold a pointer to the mutable caption array or a stack string.

Dialogue formatter `0x105a94` subsequently overwrites bytes starting at
name byte 31. The first 15 two-byte VWF glyphs survive, followed by a split
glyph/dialogue bytes. This explains why complete, correct English in RPW
and the fallback table did not guarantee correct screen output. This is
not caused by glossary dollar-sign substitution or a 15-letter language rule.

Display selection at `0x11e0a4` uses `+0x1844` relative to its containing
object: `0x4510 + 0x1844 == 0x4dc0 + 0xf94 == 0x5d54`.
The next line starts at `+0x1863`, again 31 bytes later. The name draw is
`0x10826c`; dialogue draws separately at `0x108290`. Both use `0x110c3c`,
which selects CP932 or UTF-8 using the existing flag.

The native snapshot path `0x11fef0..0x120010` copies precisely 31 name bytes
from containing-object `+0x5d54` to `+0x9214`. Native initialization clears
all 31 bytes (`0x105798`); the ordinary clear path also sets the first byte
to zero (`0x105b7c`). None of these structures needs expansion.

## Category-wide fix

`tools/battle_name_transport.py` replaces only the three name-copy calls
and the name-only draw call. Names of up to 30 bytes plus NUL are copied
unchanged. Longer names store a nine-byte tagged pointer in the existing
array (control byte + BNP, 32-bit pointer, zero). The tag cannot start any
current canonical nickname/fallback name and is never passed to the font
drawer. The name-only wrapper resolves it **before** length measurement or
decoding, preserving the original encoding flag and widget.

The 31-byte native snapshot carries the pointer with it. Subsequent caption
changes do not overwrite the referenced immutable name. Clearing byte zero
invalidates the tag; legacy short and empty names still draw normally. No
global string replacement, singular/plural merging, heap allocation, shared
scratch text buffer, native structure growth or new loader segment is used.
This also covers future long names, without adding individual exceptions.

The three older Japanese-key deferrals remain compatible. They are retained
to avoid mixing unrelated RPW changes into this fix; they are no longer the
only protection against long battle names. Mariemaia's plural squad heading
remains separate from the singular battle speaker.

## Validation and limits

`test_battle_name_transport.py` executes the original executable instructions
in the existing PPC test harness. It reproduces the shipped overflow and
subsequent dialogue overwrite, then exercises the emitted patch through all
three call sites, native dialogue formatting, and the actual 31-byte snapshot
copy. Coverage includes both encodings, empty/short/30/31/32/128/1024-byte
names, transitions between speakers, resets, ABI preservation, canaries,
and all 470 fallback bindings plus 1,155 RPW nickname slots (1,625 cases,
62 over 30 bytes in the .21 fixtures). The fallback bindings cover all
1,155 fallback-table pointers, including shared names.

Source guards cover the replaced calls plus hashes of the native cache,
clear, selection and snapshot contracts. The build and production issue gate
verify that all producers and the name drawer use the same emitted transport.
The full in-memory executable patch test checks composition and the unchanged
extension budget. The CPU harness now enforces executable LOAD permissions
on instruction fetch, which was missing from the initial tests. Both raw and
folded .22 fixtures fail the new gate; corrected code executes in both layouts.

`ppc_permissions.py` checks changed direct branches in the original executable
sections and follows reachable injected code, including conditional paths and
call continuations. Targets must be file-backed RX, not R/RW/RWX or BSS. It runs
in EBOOT validation, issue checks, hardware preflight before/after folding,
and on the decoded final SELF before ISO creation. Tests cover negative paths
and the released failure. Indirect branch targets and runtime pointer lifetime
are outside this static check. Static/data checks alone must not be described
as gameplay confirmation. Other unrelated buffers are not enlarged here.
