"""Put English series names into the executable's string tables.

The 登場作品 label on a library page is not drawn from PRDC, nor from
RPW_DATA: it is a **string table inside EBOOT**. `.rodata` holds the 32
series names as NUL-terminated cp932 strings, and `.data` holds three arrays
of 34 big-endian u32 pointers (one per series id, NULL where a series has no
name in that context) that the label code indexes. The third array runs
straight on into the keyword names (破界事変, 再世戦争...).

Nothing in the file is moved. The ELF's first LOAD segment ends at file
offset 0x779488 and the second begins at 0x780000; the 27,512 bytes between
are zero padding that exists in the file but is not mapped. Extending the
first segment's filesz/memsz to 0x780000 maps it (VA 0x789488..0x790000,
abutting segment 2), and the English strings are written there. Each array
entry that pointed at a Japanese name is repointed to the English one.

The English is encoded as library-geometry digraph pairs from the SAME build
as the atlas being shipped: pass that run's pairs_lib.json. Verification is
part of the patch: every repointed entry is read back and decoded through
the inverse mapping, every byte outside the three edited regions is asserted
identical, and any table string left Japanese must not share a code with a
pair cell of this run.

    python tools/eboot.py <EBOOT_dec.elf> <glossary.json> <pairs_lib.json> <out EBOOT.BIN> [--pairs pairs.json]

RPCS3 boots the plain decrypted ELF as EBOOT.BIN (gate passed with the
unmodified file: install ran, 0 access violations).

The map COMMAND menu and system menu labels are a separate, UTF-8 string
table in .rodata (see command_labels / translation/ui_eboot.json).
"""
import localization as _l10n
import io
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digraph as dg      # noqa: E402
import reserved as rsv    # noqa: E402

ANCHOR = "無敵ロボ　トライダーＧ７"     # series id 0; its pointer locates each array
ENTRIES = 34                                # series ids 0..33
KW_NAMES = 141                              # keyword names follow in the third array


def _count(arrays, base):
    """Entries to consider in one array: the series, plus the keyword names
    that continue the third array (the 用語事典 list draws them)."""
    return ENTRIES + KW_NAMES if base == arrays[2] else ENTRIES
NUL = bytes((0,))


def _segments(b):
    phoff = struct.unpack(">Q", b[0x20:0x28])[0]
    phnum = struct.unpack(">H", b[0x38:0x3a])[0]
    phsz = struct.unpack(">H", b[0x36:0x38])[0]
    segs = []
    for i in range(phnum):
        o = phoff + i * phsz
        f = struct.unpack(">IIQQQQQQ", b[o:o + 56])
        if f[0] == 1:                      # PT_LOAD
            segs.append({"hdr": o, "off": f[2], "va": f[3], "filesz": f[5], "memsz": f[6]})
    return segs


def _off(segs, va):
    for s in segs:
        if s["va"] <= va < s["va"] + s["filesz"]:
            return s["off"] + (va - s["va"])
    return None


def _cstr(b, off):
    return b[off:b.index(NUL, off)]


def find_arrays(b, segs):
    """File offsets of the three pointer arrays, via the id-0 pointer."""
    a_off = b.index(ANCHOR.encode("cp932") + NUL)
    a_va = segs[0]["va"] + a_off
    key = struct.pack(">I", a_va)
    arrays, p = [], 0
    while True:
        p = b.find(key, p)
        if p < 0:
            break
        if p >= segs[1]["off"]:
            arrays.append(p)
        p += 4
    if len(arrays) != 3:
        raise SystemExit("expected 3 series arrays, found %d" % len(arrays))
    return arrays


# --- variable-width advance -------------------------------------------------
# The string drawer (0x140f4) advances the pen at 0x14774..0x14780 by the
# per-call advance it snapshotted into stack slot 0x94; the glyph's atlas
# cell index is still in stack slot 0xc2. One instruction, `lfs f13,0x94(r1)`
# at 0x14778, becomes `bl STUB`; the stub returns f13 = advance * W[cell]/32
# from a 4,480-byte table. Japanese cells keep 32 and are unchanged.
PATCH_SITE = 0x14778
PATCH_ORIG = 0xC1A10094              # lfs f13, 0x94(r1)
STUB_VA = 0x78C200                   # in the mapped gap, after the table
TABLE_VA = 0x78B000                  # 4480 bytes, one per atlas cell (strings get 0x789490..0x78b000)
ATLAS_CELLS = 4480

# Keyword (《》) lines: the dialogue draws the pink link and the text after
# it as separate passes, positioned by 0x1d0708 as
#     x = style[+0x20] + style[+0x2e] * column      (column = codes before)
# The two callers hold the line text in a register; each gets a stub that
# computes x from the width table instead: W == 32 -> step, else
# W * step * 3 / 128 (the dialogue quad is 3/4 of the advance). y unchanged.
KW_ORIG = 0x1D0708
# (bl site, register holding the keyword state {ptr, len}, stub va); the
# four mode drawers 0x1d19ac / 0x1d1a78 / 0x1d1c64 / 0x1d1e20
# The activation pad-bank dispatch extends VWF through 0x78c317.
# Move the first 68-byte generated keyword helper by 16 bytes, still well
# before the next helper at 0x78c400, inside the same mapped gap.
KW_SITES = ((0x1D1A08, 31, 0x78C320), (0x1D1BA4, 30, 0x78C400),
            (0x1D1D88, 30, 0x78C500), (0x1D1E84, 31, 0x78C600))

# The keyword loop (0x1d16a8) accumulates `column += bytes_drawn / 2` after
# each segment it draws (0x1d18f0). Instead, the drawer (vwf_stub) adds every
# glyph advance into PEN_ACC, the position stub zeroes it before a piece is
# drawn, and the accumulator hook turns it into column = px * 128.
KW_ACC_SITE = 0x1D18F0              # srawi r9, r3, 1 ; addze r9, r9
KW_ACC_ORIG = (0x7C690E70, 0x7D290194)
KW_ACC_STUB = 0x78C700
LOOSE_STR = 0x78C800                # English for loose data-pointer names lives here
SAFE_LO, SAFE_HI = 0x85E000, 0x869000   # display-name arrays; in-place overwrite is safe here
TOC_LO, TOC_HI = 0x7D0000, 0x7E0000     # TOC refs are display-benign
LOOSE_ENABLE = False                # repointing name pointers is unsafe (lookup keys); see loose_names
INPLACE_ENABLE = False              # DISABLED: even display-only in-place overwrite aborts the Genion robot entry -- EBOOT name strings are content-keyed in the entry-render path
KW_LOG = None                      # debug: set to BSS_PAGE to log (ptr, bytes, units) per segment
BSS_PAGE = 0xBFCF80                # segment 1 grows by BSS_GROW; this page is ours (zero-filled, RW)
BSS_GROW = 0x2000
PEN_ACC = BSS_PAGE + 0x1800        # float: sum of glyph advances since the last reset (+8: scratch)
HOOK_SCRATCH = BSS_PAGE            # 4 KB: the composed string for a prefix hook (see name_stub)
HOOK_JSTATE = BSS_PAGE + 0x1700    # joined-match state: [0] first-piece va, [4] end va, [8] a NUL
# Debug probe: when set to two bytes, every drawn string starting with them
# is replaced by the hex dump of its first 16 bytes, drawn as letters. The
# GDB server on this RPCS3 build answers nothing but the handshake, so the
# screen is the memory viewer. None for a real build.
HOOK_HEXPROBE = None
HEXTBL_VA = 0x78CB00               # NAME_STUB + 0x200: 16 letter codes '0'..'f', written by name_hook

# Names that live in the executable (character/mech names in the library
# index, proper nouns) cannot be translated by editing the data: every way
# of doing that -- repointing the pointer, or overwriting the bytes in
# place -- abort()ed the game, because the same strings are lookup KEYS as
# well as display text (see docs/TRANSLATING.md). So translate at DRAW time.
# 0x140f4 is the one string drawer: r3 = cp932 char*, walked byte by byte
# (0x00 ends, 0x0a is a newline, 0x2e..0x39 are escape codes). Its first
# instruction becomes `b NAME_STUB`; the stub looks the whole string up in a
# {Japanese va -> English va} table and, on an exact match, swaps r3 for the
# English before falling back into 0x140f8. Not one byte of game data moves
# or changes, so every comparison, hash and length the game takes still sees
# the original Japanese -- only the pixels differ.
NAME_SITE = 0x140F4
NAME_ORIG = 0x2F870000             # cmpwi cr7, r7, 0  (displaced into the stub)
NAME_STUB = 0x78C900
# The 27 KB gap between the two LOAD segments filled up (hook table at
# 432/448 entries, strings 10,992 B against 10,240). The ELF carries three
# placeholder PT_LOAD entries (vaddr 0, size 0); one becomes a third,
# read-only segment at EXT_VA, backed by zeros appended to the file, and the
# hook table plus every English string the hook, the menu labels and the
# COMMAND menu need live there. Stubs stay in the gap; they address the
# table with lis/ori, so any 32-bit VA is fine.
EXT_VA = 0xC00000                  # above segment 1's BSS (ends 0xbfef80 after BSS_GROW)
EXT_SIZE = 0x90000                 # 576 KB: expanded for source-driven message-family coverage (2026-09-09)
HOOK_ALL_NAMES = True              # hook every glossary name, not only EBOOT-resident ones
HOOK_ALL_SET = set()               # which names qualify (glossary + library; build_project fills it)
EXT_ALIGN = 0x10000
NAME_TBL = EXT_VA                  # 8 B/entry: (jp va, en va), 0 terminates
# Complete operation-condition coverage exceeds the former4095-entry limit.
# Repartition the SAME extension; do not grow/move the hardware LOAD segment.
NAME_STR = EXT_VA + 0x10000        # 8191 entries + terminator, then owned text
NAME_ENABLE = True


def _va(segs, off):
    for s in segs:
        if s["off"] <= off < s["off"] + s["filesz"]:
            return s["va"] + (off - s["off"])
    raise SystemExit("file offset %#x is not mapped" % off)


def add_segment(b, va=EXT_VA, size=EXT_SIZE):
    """Turn the first placeholder PT_LOAD into a read-only segment at `va`,
    backed by `size` zero bytes appended to the file (aligned). Returns the
    file offset of the new region and of the program header it rewrote."""
    phoff = struct.unpack(">Q", b[0x20:0x28])[0]
    phsz, phnum = struct.unpack(">HH", b[0x36:0x3a])
    slot = None
    for i in range(phnum):
        o = phoff + i * phsz
        typ, flags, off, pva, ppa, fsz, msz, al = struct.unpack(">IIQQQQQQ", b[o:o + 56])
        if typ == 1 and pva == 0 and fsz == 0 and msz == 0:
            slot = o
            break
    if slot is None:
        raise SystemExit("no placeholder PT_LOAD to repurpose for the EXT segment")
    foff = (len(b) + EXT_ALIGN - 1) & ~(EXT_ALIGN - 1)
    b += bytes(foff - len(b) + size)
    b[slot:slot + 56] = struct.pack(">IIQQQQQQ", 1, 0x4, foff, va, va, size, size, EXT_ALIGN)
    return foff, slot
# UI labels drawn from the AIDDATAPACK UI member (FSSA) cannot be lengthened
# or moved there, but they are drawn by the same 0x140f4 and the hook matches
# by CONTENT, so a label of any length can be swapped at draw time. Entries
# here win over glossary English for the same whole string (格闘 alone is the
# stat label "CQB", not a sentence's "melee"). Japanese that the executable
# does not hold is copied into the gap so the stub has bytes to compare.
UI_HOOK_FILES = tuple(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "..", "translation", f)
                      for f in ("ui_hook.json", "abilities.json", "spirit_hook.json",
                                "skill_hook.json", "ability_hook.json", "parts_desc_hook.json", "gift_report_hook.json",
                                "tutorial_hook.json", "issue_hook.json", "date_cards.json", "trader_hook.json", "terrain_hook.json", "naming_hook.json", "weapon_effect_hook.json", "battle_report_hook.json", "unlock_report_hook.json", "message_class_hook.json", "unlock_shop_hook.json", "terrain_all_hook.json", "mission_conditions_hook.json", "deployment_hook.json", "squad_names_hook.json"))


UI_PREFIX = set()                  # jp keys whose entry matches as a PREFIX (see name_stub)
UI_JOINED = set()                  # jp keys matched across the NUL gaps of a typeset heading
UI_KEY_VWF = set()                 # mixed keys with already translated Latin letter cells
# UI keys that may point at their Japanese where the ELF already holds it,
# instead of owning a copy in EXT. Only for tables no later build step patches
# (the bonus descriptions): the copies would not fit the unchanged extension.
# check_issue_fixes reads every key back, so an overwritten key fails the gate.
UI_ELF_RESIDENT = set()
# keys a later build step overwrites in place, so they keep an EXT copy:
# movement_type_cells rewrites the first standalone 陸 (see name_hook)
UI_OWN_COPY = {'陸'}


def load_ui_hook(paths=UI_HOOK_FILES):
    """Every content-hooked label: UI labels, then mech ability names. A line
    with "prefix": true matches the head of a longer drawn string and keeps
    the rest (a title the game composes with its body)."""
    out = {}
    no_line_pairs = set()
    for path in paths:
        if os.path.exists(path):
            d = json.load(open(path, encoding="utf-8"))
            if d.get('mission_variants'):
                import mission_conditions
                d['lines'] = mission_conditions.expand(d['lines'])
            for l in d["lines"]:
                if d.get('terrain_table'):
                    import terrain_catalog
                    l = dict(l, jp=terrain_catalog.key(l['jp']))
                if l.get("en") is None:
                    continue
                import trdata
                if "count_range" in l:
                    # End Phase composes a fullwidth count between two strings.
                    # Match the complete result, never a generic numeric suffix.
                    lo, hi = l["count_range"]
                    assert 0 <= lo <= hi <= 99
                    assert "{count}" in l["jp"] and "{count}" in l["en"]
                    for count in range(lo, hi + 1):
                        wide = str(count).translate(str.maketrans("0123456789", "０１２３４５６７８９"))
                        out[l["jp"].replace("{count}", wide)] = trdata._ex(l["en"].replace("{count}", str(count)), path)
                    continue
                out[l["jp"]] = trdata._ex(l["en"], path)
                if d.get('line_pairs') is False:
                    no_line_pairs.add(l['jp'])
                if l.get("prefix"):
                    UI_PREFIX.add(l["jp"])
                if l.get("joined") or d.get('joined_names'):
                    UI_JOINED.add(l["jp"])
                if l.get("jp_vwf"):
                    UI_KEY_VWF.add(l["jp"])
    import mission_conditions
    mission_rows = mission_conditions.additional_lines()
    for row in mission_conditions.expand(mission_rows):
        if row['jp'] in out and out[row['jp']] != row['en']:
            raise ValueError('Conflicting mission condition: ' + row['jp'])
        out[row['jp']] = row['en']
    out.update(mission_conditions.line_hooks(mission_rows))
    import episode_heading_hooks
    out.update(episode_heading_hooks.hooks())
    import chapter_narration
    for jp, en in chapter_narration.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting chapter narration: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
    import name_entry_labels
    out.update(name_entry_labels.hooks())
    import team_order_labels
    out.update(team_order_labels.hooks())
    import required_skill_levels
    for jp, en in required_skill_levels.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting required-skill level: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
    import song_deployment_labels
    for jp, en in song_deployment_labels.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting song/weapon label: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
    import command_swap_labels
    for jp, en in command_swap_labels.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting command/swap label: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
    import map_weapon_info
    for jp, en in map_weapon_info.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting MAP weapon IFF state: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
        UI_ELF_RESIDENT.add(jp)
    import bonus_descriptions
    import weapon_requirement_runtime
    for jp, en in weapon_requirement_runtime.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting runtime weapon requirement: ' + jp)
        out[jp] = en
        no_line_pairs.add(jp)
    for jp, en in bonus_descriptions.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting bonus description: ' + jp)
        out[jp] = en
        UI_ELF_RESIDENT.add(jp)
        # drawn whole, like the parts/skill description tables, which opt
        # out too; per-line pairs would also overflow the extension
        no_line_pairs.add(jp)
    import destroy_quotes
    for jp, en in destroy_quotes.hooks().items():
        if jp in out and out[jp] != en:
            raise ValueError('Conflicting shot-down quote: ' + jp)
        out[jp] = en
        UI_ELF_RESIDENT.add(jp)     # same table kind: resident keys, drawn whole
        no_line_pairs.add(jp)
    import trade_list_flavor,record_screen_labels
    out.update(trade_list_flavor.hooks())
    import trader_upgrade_text
    out.update(trader_upgrade_text.hooks())
    upgrade_notices=trader_upgrade_text.mixed_hooks()
    out.update(upgrade_notices)
    UI_KEY_VWF.update(upgrade_notices)
    record_hooks=record_screen_labels.hooks()
    out.update(record_hooks)
    UI_JOINED.update(record_hooks)
    # These names must stay short in native RPW buffers. Expand only at the
    # final CP932 drawer, using an exact match and separately allocated text.
    import battle_name_rendering
    for jp, en in battle_name_rendering.hooks().items():
        if jp in UI_PREFIX | UI_JOINED | UI_KEY_VWF or (jp in out and out[jp] != en):
            raise ValueError('Deferred battle name conflicts with another UI hook: ' + jp)
        out[jp] = en
    import skill_name_transport
    skill_labels, skill_prefixes = skill_name_transport.hooks()
    for jp, en in skill_labels.items():
        if jp in out and out[jp] != en:
            raise ValueError('Deferred skill name conflicts with another UI hook: ' + jp)
        out[jp] = en
    UI_PREFIX.update(skill_prefixes)
    import command_choice_labels
    for jp,en in command_choice_labels.hooks().items():
        if jp in out and out[jp]!=en:
            raise ValueError('Command choice hook conflict: '+jp)
        out[jp]=en
    import battle_reports
    for jp,en in battle_reports.gold_hook().items():
        if jp in out and out[jp]!=en:
            raise ValueError('Gold reward hook conflict: '+jp)
        out[jp]=en
        UI_PREFIX.add(jp)
    # Some boxes draw a multi-line string ONE LINE PER CALL (the Operation
    # End conditions: stage 3's three-line SR condition stayed Japanese
    # although the whole string was hooked). Register each line pair too,
    # when the line counts agree; a line that is already an entry keeps
    # its own English, and short lines are skipped so a generic word is
    # never claimed by a sentence fragment.
    for jp, en in list(out.items()):
        # Part help is wrapped as complete prose. Pairing its newly wrapped
        # lines with unrelated Japanese line breaks creates false fragments.
        if jp in no_line_pairs:
            continue
        if "\n" not in jp:
            continue
        jl, el = jp.split("\n"), en.split("\n")
        if len(jl) != len(el):
            continue
        for a_, b_ in zip(jl, el):
            a_, b_ = a_.strip("\u3000 "), b_.strip()
            if len(a_) >= 6 and a_ not in out and b_:
                out[a_] = b_
    return out


def _ppc():
    def lis(rD, imm): return 0x3C000000 | (rD << 21) | (imm & 0xffff)
    def ori(rA, rS, imm): return 0x60000000 | (rS << 21) | (rA << 16) | (imm & 0xffff)
    def lhz(rD, rA, d): return 0xA0000000 | (rD << 21) | (rA << 16) | (d & 0xffff)
    def lbzx(rD, rA, rB): return 0x7C000000 | (rD << 21) | (rA << 16) | (rB << 11) | (87 << 1)
    def std(rS, rA, ds): return 0xF8000000 | (rS << 21) | (rA << 16) | (ds & 0xfffc)
    def stw(rS, rA, d): return 0x90000000 | (rS << 21) | (rA << 16) | (d & 0xffff)
    def lfd(fD, rA, d): return 0xC8000000 | (fD << 21) | (rA << 16) | (d & 0xffff)
    def lfs(fD, rA, d): return 0xC0000000 | (fD << 21) | (rA << 16) | (d & 0xffff)
    def fcfid(fD, fB): return 0xFC00069C | (fD << 21) | (fB << 11)
    def frsp(fD, fB): return 0xFC000018 | (fD << 21) | (fB << 11)
    def fmuls(fD, fA, fC): return 0xEC000032 | (fD << 21) | (fA << 16) | (fC << 6)
    def lbz(rD, rA, d): return 0x88000000 | (rD << 21) | (rA << 16) | (d & 0xffff)
    def stb(rS, rA, d): return 0x98000000 | (rS << 21) | (rA << 16) | (d & 0xffff)
    def extsb(rA, rS): return 0x7C000774 | (rS << 21) | (rA << 16)
    def extsh(rA, rS): return 0x7C000734 | (rS << 21) | (rA << 16)
    def mullw(rD, rA, rB): return 0x7C0001D6 | (rD << 21) | (rA << 16) | (rB << 11)
    def mulli(rD, rA, imm): return 0x1C000000 | (rD << 21) | (rA << 16) | (imm & 0xffff)
    def add(rD, rA, rB): return 0x7C000214 | (rD << 21) | (rA << 16) | (rB << 11)
    def addi(rD, rA, imm): return 0x38000000 | (rD << 21) | (rA << 16) | (imm & 0xffff)
    def cmpwi(rA, imm): return 0x2C000000 | (rA << 16) | (imm & 0xffff)
    def cmplwi(rA, imm): return 0x28000000 | (rA << 16) | (imm & 0xffff)
    def srawi(rA, rS, sh): return 0x7C000670 | (rS << 21) | (rA << 16) | (sh << 11)
    def mr(rA, rS): return 0x7C000378 | (rS << 21) | (rA << 16) | (rS << 11)
    def lwz(rD, rA, d): return 0x80000000 | (rD << 21) | (rA << 16) | (d & 0xffff)
    def neg(rD, rA): return 0x7C0000D0 | (rD << 21) | (rA << 16)
    def cmplw(rA, rB): return 0x7C000040 | (rA << 16) | (rB << 11)
    def subf(rD, rA, rB): return 0x7C000050 | (rD << 21) | (rA << 16) | (rB << 11)
    def fadds(fD, fA, fB): return 0xEC00002A | (fD << 21) | (fA << 16) | (fB << 11)
    def fsubs(fD, fA, fB): return 0xEC000028 | (fD << 21) | (fA << 16) | (fB << 11)
    def stfs(fS, rA, d): return 0xD0000000 | (fS << 21) | (rA << 16) | (d & 0xffff)
    def fctiwz(fD, fB): return 0xFC00001E | (fD << 21) | (fB << 11)
    def stfiwx(fS, rA, rB): return 0x7C0007AE | (fS << 21) | (rA << 16) | (rB << 11)
    def ld(rD, rA, ds): return 0xE8000000 | (rD << 21) | (rA << 16) | (ds & 0xfffc)
    def stdu(rS, rA, ds): return 0xF8000001 | (rS << 21) | (rA << 16) | (ds & 0xfffc)
    def clrldi32(rA, rS): return 0x78000020 | (rS << 21) | (rA << 16)
    def clrlwi(rA, rS, n): return 0x54000000 | (rS << 21) | (rA << 16) | (n << 6) | (31 << 1)
    def rlwinm(rA, rS, sh, mb, me): return 0x54000000 | (rS << 21) | (rA << 16) | (sh << 11) | (mb << 6) | (me << 1)
    def lhzx(rD, rA, rB): return 0x7C000000 | (rD << 21) | (rA << 16) | (rB << 11) | (279 << 1)
    def sth(rS, rA, d): return 0xB0000000 | (rS << 21) | (rA << 16) | (d & 0xffff)
    def andis_(rA, rS, ui): return 0x74000000 | (rS << 21) | (rA << 16) | (ui & 0xffff)
    def b(off): return 0x48000000 | (off & 0x03fffffc)
    def beq(off): return 0x41820000 | (off & 0xfffc)
    def bne(off): return 0x40820000 | (off & 0xfffc)
    def ble(off): return 0x40810000 | (off & 0xfffc)
    def bge(off): return 0x40800000 | (off & 0xfffc)
    return locals()


def vwf_stub():
    """Width 32 -> the caller advance, untouched (all Japanese). Otherwise
    f13 = W/32 * quad width (stack 0x9c). Either way the advance is added to
    PEN_ACC, which the keyword layout reads back (see kw_acc_stub). Clobbers
    r0, r9, f10, f13 -- all redefined by the loop head before any use."""
    P = _ppc()
    A = _Asm()
    A.emit(P["lhz"](0, 1, 0xc2))                                            # r0 = cell
    import command_layout
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[command_layout.ACTIVATION_START]))); A.br('blt', 'older_command_banks')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[-1]))); A.br('ble', 'command')
    A.label('older_command_banks')
    A.emit(P['cmpwi'](0, dg.cell_index(0x8461))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[command_layout.PREP_START-1]))); A.br('ble', 'command')
    A.emit(P['cmpwi'](0, dg.cell_index(0x84BF))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(0x84FC))); A.br('ble', 'command')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[command_layout.SETTINGS_START]))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(0x87FA))); A.br('ble', 'command')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[17]))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[command_layout.SETTINGS_START-1]))); A.br('ble', 'command')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[7]))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[16]))); A.br('ble', 'command')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[0]))); A.br('blt', 'ordinary')
    A.emit(P['cmpwi'](0, dg.cell_index(command_layout.CODES[command_layout.ACTIVATION_START-1]))); A.br('bgt', 'ordinary')
    A.label('command')
    A.emit(P['b'](command_layout.CAVE - (STUB_VA + len(A.w)*4)))
    A.label('ordinary')
    # Confirmation tabs use the live pitch; quad width can differ from it.
    # f31 is the original line x (set at 0x1411c and preserved by the drawer).
    A.emit(P['cmpwi'](0, dg.cell_index(0x86D6))); A.br('beq', 'col3')
    A.emit(P['cmpwi'](0, dg.cell_index(0x86D7))); A.br('beq', 'col5')
    A.emit(P["lis"](9, TABLE_VA >> 16)); A.emit(P["ori"](9, 9, TABLE_VA & 0xffff))
    A.emit(P["lbzx"](0, 9, 0))                                              # r0 = W[cell]
    A.emit(P["cmpwi"](0, 32)); A.br("bne", "letter")
    A.emit(P["lfs"](13, 1, 0x94)); A.br("b", "acc")                        # original advance
    A.label("letter")
    A.emit(P["std"](0, 1, 0xd0)); A.emit(P["lfd"](13, 1, 0xd0))
    A.emit(P["fcfid"](13, 13)); A.emit(P["frsp"](13, 13))                   # f13 = float(W)
    A.emit(P["lfs"](10, 1, 0x9c)); A.emit(P["fmuls"](13, 13, 10))           # * quad width
    A.emit(P["lis"](9, 0x3d00)); A.emit(P["stw"](9, 1, 0xd0)); A.emit(P["lfs"](10, 1, 0xd0))
    A.emit(P["fmuls"](13, 13, 10))                                          # * 1/32
    A.br('b', 'acc')
    A.label('col3')
    A.emit(P['addi'](0, 0, 3)); A.br('b', 'tab')
    A.label('col5')
    A.emit(P['addi'](0, 0, 5))
    A.label('tab')
    A.emit(P['std'](0, 1, 0xd0)); A.emit(P['lfd'](13, 1, 0xd0))
    A.emit(P['fcfid'](13, 13)); A.emit(P['frsp'](13, 13))
    A.emit(P['lfs'](10, 1, 0x94)); A.emit(P['fmuls'](13, 13, 10))
    A.emit(P['fadds'](13, 31, 13))                      # target = origin + column * pitch
    A.emit(P['lfs'](10, 1, 0x84)); A.emit(P['fsubs'](13, 13, 10))  # advance = target - pen
    A.label("acc")
    A.emit(P["lis"](9, PEN_ACC >> 16)); A.emit(P["ori"](9, 9, PEN_ACC & 0xffff))
    A.emit(P["lfs"](10, 9, 0)); A.emit(P["fadds"](10, 10, 13)); A.emit(P["stfs"](10, 9, 0))
    A.emit(0x4E800020)
    return A.code()


class _Asm:
    """Tiny label-based assembler for the stubs: words and named branches."""

    def __init__(self):
        self.w, self.labels, self.fix = [], {}, []

    def emit(self, word):
        self.w.append(word)

    def label(self, name):
        self.labels[name] = len(self.w)

    def br(self, kind, name):
        self.fix.append((len(self.w), kind, name))
        self.w.append(0)

    def code(self):
        forms = {"b": 0x48000000, "beq": 0x41820000, "bne": 0x40820000,
                 "ble": 0x40810000, "bge": 0x40800000, "bgt": 0x41810000, "blt": 0x41800000}
        for i, kind, name in self.fix:
            off = (self.labels[name] - i) * 4
            self.w[i] = forms[kind] | (off & (0x03fffffc if kind == "b" else 0xfffc))
        return b"".join(struct.pack(">I", x) for x in self.w)


def kw_acc_stub():
    """r9 = PEN_ACC (px the drawer just advanced for this piece) * 128, as an
    integer, and PEN_ACC is cleared. Replaces `srawi r9, r3, 1; addze` so the
    keyword loop accumulates the drawer's real pen movement. Clobbers r0,
    r9, r10, f12, f13 -- dead at the site."""
    P = _ppc()
    A = _Asm()
    A.emit(P["lis"](10, PEN_ACC >> 16)); A.emit(P["ori"](10, 10, PEN_ACC & 0xffff))
    A.emit(P["lfs"](13, 10, 0))                                             # sum px
    A.emit(P["lis"](0, 0x4300)); A.emit(P["stw"](0, 10, 8)); A.emit(P["lfs"](12, 10, 8))   # 128.0
    A.emit(P["fmuls"](13, 13, 12)); A.emit(P["fctiwz"](13, 13))
    A.emit(P["stfiwx"](13, 0, 10))                                          # -> PEN_ACC as int
    A.emit(P["lwz"](9, 10, 0))
    A.emit(P["addi"](0, 0, 0)); A.emit(P["stw"](0, 10, 0))                  # PEN_ACC = 0
    A.emit(0x4E800020)
    return A.code()



def kw_stub(state_reg):
    """Replacement for 0x1d0708: y as the original; x = base + column >> 7
    with column in 1/128 px (see kw_acc_stub); PEN_ACC is zeroed here so the
    piece about to be drawn accumulates from nothing. `state_reg` unused."""
    P = _ppc()
    A = _Asm()
    A.emit(P["lbz"](0, 4, 0x2f)); A.emit(P["extsb"](0, 0)); A.emit(P["mullw"](0, 0, 6))
    A.emit(P["lhz"](11, 4, 0x22)); A.emit(P["extsh"](11, 11)); A.emit(P["add"](11, 11, 0))
    A.emit(P["stw"](11, 8, 0))                                              # y
    A.emit(P["srawi"](0, 5, 7))
    A.emit(P["lhz"](9, 4, 0x20)); A.emit(P["extsh"](9, 9)); A.emit(P["add"](9, 9, 0))
    A.emit(P["stw"](9, 7, 0))                                               # x
    A.emit(P["lis"](10, PEN_ACC >> 16)); A.emit(P["ori"](10, 10, PEN_ACC & 0xffff))
    A.emit(P["addi"](0, 0, 0)); A.emit(P["stw"](0, 10, 0))                  # PEN_ACC = 0
    A.emit(0x4E800020)
    return A.code()


def name_stub():
    """Draw-time name swap. On entry to 0x140f4 r3 is the cp932 char* and r7
    the count its first instruction tests; r4/r5/r6 and f1..f3 are live too.
    The stub makes its own frame, saves the five GPRs it uses, walks the
    table comparing the whole string, and leaves r3 on English for a hit.
    r0/r11/r12 are volatile and dead here (0x140f8 reloads r0 from LR)."""
    P = _ppc()
    A = _Asm()
    SAVE = (4, 5, 6, 8, 9, 10)
    A.emit(P['stdu'](1, 1, -0x70))
    for i, r in enumerate(SAVE):
        A.emit(P['std'](r, 1, 0x20 + 8 * i))
    A.emit(P['cmpwi'](7, 0)); A.br('beq', 'done')      # r7 == 0: the caller never
    #                                                  reads r3, so neither may we
    A.emit(P['clrldi32'](8, 3))                        # subject, high half cleared
    A.emit(P['lbz'](0, 8, 0))
    A.emit(P['cmplwi'](0, 0x81)); A.br('bge', 'walk')  # Japanese
    A.emit(P['cmplwi'](0, 0x0a)); A.br('beq', 'walk')  # UI labels may start with a newline
    A.emit(P['cmplwi'](0, 0x2e)); A.br('blt', 'done')  # ...or with a drawer escape code
    A.emit(P['cmplwi'](0, 0x39)); A.br('bgt', 'done')  # ASCII/English/empty: no name
    A.label('walk')
    # A later piece of a joined-matched heading: answer with an empty string
    # (the English already drew, at the first piece's call).
    A.emit(P['lis'](11, HOOK_JSTATE >> 16)); A.emit(P['ori'](11, 11, HOOK_JSTATE & 0xffff))
    A.emit(P['lwz'](12, 11, 0))
    A.emit(P['cmpwi'](12, 0)); A.br('beq', 'nojr')     # no active range
    A.emit(P['cmplw'](8, 12)); A.br('ble', 'nojr')     # at or before the first piece
    A.emit(P['lwz'](9, 11, 4))
    A.emit(P['cmplw'](8, 9)); A.br('bgt', 'nojr')      # past the matched extent
    A.emit(P['addi'](3, 11, 8)); A.br('b', 'done')     # r3 -> the stored NUL
    A.label('nojr')
    if HOOK_HEXPROBE:                                  # debug: draw the bytes instead
        A.emit(P['cmplwi'](0, HOOK_HEXPROBE[0])); A.br('bne', 'tbl')
        A.emit(P['lbz'](4, 8, 1))
        A.emit(P['cmplwi'](4, HOOK_HEXPROBE[1])); A.br('bne', 'tbl')
        A.emit(P['lis'](10, HOOK_SCRATCH >> 16)); A.emit(P['ori'](10, 10, HOOK_SCRATCH & 0xffff))
        A.emit(P['mr'](3, 10))
        A.emit(P['lis'](12, HEXTBL_VA >> 16)); A.emit(P['ori'](12, 12, HEXTBL_VA & 0xffff))
        A.emit(P['lhz'](11, 12, 32)); A.emit(P['addi'](6, 0, 28))    # 28 spaces first: clear the overlay
        A.label('pad')
        A.emit(P['sth'](11, 10, 0)); A.emit(P['addi'](10, 10, 2))
        A.emit(P['addi'](6, 6, -1)); A.emit(P['cmpwi'](6, 0)); A.br('bne', 'pad')
        A.emit(P['mr'](5, 8)); A.emit(P['addi'](6, 0, 32))
        A.label('hex')
        A.emit(P['lbz'](0, 5, 0))
        for sh in (28, 0):                             # high nibble, then low
            A.emit(P['rlwinm'](9, 0, sh, 28, 31)); A.emit(P['add'](9, 9, 9))
            A.emit(P['lhzx'](11, 12, 9)); A.emit(P['sth'](11, 10, 0)); A.emit(P['addi'](10, 10, 2))
        A.emit(P['addi'](5, 5, 1)); A.emit(P['addi'](6, 6, -1))
        A.emit(P['cmpwi'](6, 0)); A.br('bne', 'hex')
        A.emit(P['addi'](0, 0, 0)); A.emit(P['stb'](0, 10, 0))
        A.br('b', 'done')
    A.label('tbl')
    A.emit(P['lis'](11, NAME_TBL >> 16)); A.emit(P['ori'](11, 11, NAME_TBL & 0xffff))
    A.label('loop')
    A.emit(P['lwz'](12, 11, 0))
    A.emit(P['cmpwi'](12, 0)); A.br('beq', 'done')     # end of table
    A.emit(P['lbz'](4, 12, 0))
    A.emit(P['cmplw'](0, 4)); A.br('bne', 'next')      # cheap reject on byte 0
    A.emit(P['mr'](5, 8)); A.emit(P['mr'](6, 12))
    A.emit(P['lwz'](12, 11, 4))                        # English va; bit30 = joined entry
    A.emit(P['andis_'](9, 12, 0x4000)); A.br('bne', 'jcmp')
    A.label('cmp')
    A.emit(P['lbz'](9, 6, 0))
    A.emit(P['cmpwi'](9, 0)); A.br('beq', 'endjp')     # the entry's Japanese is exhausted
    A.emit(P['lbz'](4, 5, 0))
    A.emit(P['cmplw'](4, 9)); A.br('bne', 'next')
    A.emit(P['addi'](5, 5, 1)); A.emit(P['addi'](6, 6, 1)); A.br('b', 'cmp')
    A.label('next')
    A.emit(P['addi'](11, 11, 8)); A.br('b', 'loop')
    A.label('endjp')
    A.emit(P['lwz'](12, 11, 4))                        # English va; bit 31 = prefix entry
    A.emit(P['cmpwi'](12, 0)); A.br('blt', 'prefix')
    A.emit(P['lbz'](4, 5, 0))
    A.emit(P['cmpwi'](4, 0)); A.br('bne', 'next')      # exact entry: subject must end too
    A.emit(P['mr'](3, 12)); A.br('b', 'done')          # r3 = English
    # A prefix entry matched the head of a longer string (a title the game
    # composed with its body, e.g. エースボーナス\n<description>): build
    # English + the rest of the subject in HOOK_SCRATCH and draw that.
    A.label('prefix')
    A.emit(P['clrlwi'](12, 12, 1))
    A.emit(P['lis'](10, HOOK_SCRATCH >> 16)); A.emit(P['ori'](10, 10, HOOK_SCRATCH & 0xffff))
    A.emit(P['mr'](3, 10))
    A.label('copy_en')
    A.emit(P['lbz'](0, 12, 0)); A.emit(P['stb'](0, 10, 0))
    A.emit(P['addi'](12, 12, 1)); A.emit(P['addi'](10, 10, 1))
    A.emit(P['cmpwi'](0, 0)); A.br('bne', 'copy_en')
    A.emit(P['addi'](10, 10, -1))                      # back over the NUL
    A.label('copy_rest')
    A.emit(P['lbz'](0, 5, 0)); A.emit(P['stb'](0, 10, 0))
    A.emit(P['addi'](5, 5, 1)); A.emit(P['addi'](10, 10, 1))
    A.emit(P['cmpwi'](0, 0)); A.br('bne', 'copy_rest')
    A.br('b', 'done')                              # do not fall through into joined matching
    # A joined entry matches a heading the game typeset into NUL-separated
    # pieces (エ\0\0ース\0\0ボー\0\0ナス\0): compare the entry's Japanese
    # against the buffer SKIPPING runs of NULs (at most 8 in a row); on a
    # full match, zero the pieces so the later per-piece draws render
    # nothing, and draw the English once, here, at the first piece's spot.
    A.label('jcmp')
    A.emit(P['addi'](10, 0, 0))                        # NUL-run counter
    A.label('jloop')
    A.emit(P['lbz'](9, 6, 0))
    A.emit(P['cmpwi'](9, 0)); A.br('beq', 'jhit')      # entry exhausted: match
    A.emit(P['lbz'](4, 5, 0))
    A.emit(P['cmpwi'](4, 0)); A.br('bne', 'jbyte')
    A.emit(P['addi'](10, 10, 1)); A.emit(P['cmplwi'](10, 8)); A.br('bgt', 'next')
    A.emit(P['addi'](5, 5, 1)); A.br('b', 'jloop')     # skip the gap between pieces
    A.label('jbyte')
    A.emit(P['addi'](10, 0, 0))
    A.emit(P['cmplw'](4, 9)); A.br('bne', 'next')
    A.emit(P['addi'](5, 5, 1)); A.emit(P['addi'](6, 6, 1)); A.br('b', 'jloop')
    A.label('jhit')
    # Joined headings must end here too: チーム must not swallow the suffix
    # of チーム４ or チーム編成 before their complete entries are tried.
    A.emit(P['lbz'](4, 5, 0))
    A.emit(P['cmpwi'](4, 0)); A.br('bne', 'next')
    A.emit(P['lis'](10, HOOK_JSTATE >> 16)); A.emit(P['ori'](10, 10, HOOK_JSTATE & 0xffff))
    A.emit(P['stw'](8, 10, 0))                         # remember the matched range: the
    A.emit(P['stw'](5, 10, 4))                         # later pieces answer empty (see walk)
    A.emit(P['clrlwi'](3, 12, 2))                      # r3 = English, flags cleared
    A.br('b', 'done')
    A.label('done')
    # If this subject IS the remembered first piece but nothing matched (the
    # typeset buffer now holds a different heading), drop the stale range so
    # its later pieces are not blanked.
    A.emit(P['clrldi32'](4, 3))
    A.emit(P['cmplw'](4, 8)); A.br('bne', 'out')       # r3 was swapped: a hit, keep state
    A.emit(P['lis'](11, HOOK_JSTATE >> 16)); A.emit(P['ori'](11, 11, HOOK_JSTATE & 0xffff))
    A.emit(P['lwz'](12, 11, 0))
    A.emit(P['cmplw'](8, 12)); A.br('bne', 'out')
    A.emit(P['addi'](0, 0, 0)); A.emit(P['stw'](0, 11, 0))
    A.label('out')
    for i, r in enumerate(SAVE):
        A.emit(P['ld'](r, 1, 0x20 + 8 * i))
    A.emit(P['addi'](1, 1, 0x70))
    A.emit(NAME_ORIG)                                  # the displaced instruction
    code = A.code()
    back = (NAME_SITE + 4 - (NAME_STUB + len(code))) & 0x03fffffc
    return code + struct.pack('>I', 0x48000000 | back)


def _encode_marked(en, mapping):
    """English -> cells, with the game's inline colour markup passed through.

    The Lecture Plate tutorials emphasise a span as raw bytes: ASCII digit
    + 0x01 opens colour N, a bare ASCII digit closes it (the text drawer
    parses those before glyph lookup, so they must stay raw, not become
    letter cells). Hook English writes them as {cN} ... {/c}; a stray
    brace outside a token still fails the charset check, on purpose."""
    import re
    out = b""
    for part in re.split(r"(\{c\d\}|\{/c\})", en):
        if not part:
            continue
        if part == "{/c}":
            out += b"1"
        elif part.startswith("{c") and part.endswith("}"):
            out += part[2:-1].encode("ascii") + b""
        else:
            out += dg.encode_mixed(part, mapping, newline=bytes((10,)))
    return out


def name_hook(b, segs, names, mapping):
    """Build the draw-time table for every glossary name that exists as a
    string in the executable, write the English into the gap, and point
    0x140f4 at the stub. Returns (entries, undrawable, end_offset)."""
    rod_lo = segs[0]['off']
    rod = bytes(b[rod_lo:rod_lo + segs[0]['filesz']])
    jp_at = {}
    for jp in names:
        try:
            nb = jp.encode('cp932')
        except Exception:
            continue
        if len(nb) < 4:                     # one-character names match too much
            continue
        m = rod.find(NUL + nb + NUL)
        if m >= 0:
            jp_at[jp] = segs[0]['va'] + rod_lo + m + 1
        elif HOOK_ALL_NAMES and jp in HOOK_ALL_SET:
            # Pilot / Unit Info draw names the executable never holds (they
            # come from data tables): 853 glossary names -- Catherine Glass
            # among them -- stayed Japanese on those screens. Copy the
            # Japanese into the gap exactly as a UI label is.
            jp_at[jp] = None
    # UI labels: any length, matched by content; the executable may not hold
    # the Japanese (FSSA strings), in which case a copy goes into the gap
    ui = load_ui_hook()
    en_of = dict(names)
    for jp, en in ui.items():
        en_of[jp] = en
        # UI lookup keys must not alias labels patched later in this build.
        # movement_type_cells overwrites the first standalone 陸, which used
        # to silently change the Grd hook's lookup key into its English cell.
        # Own a stable copy in EXT even when Japanese exists in the ELF.
        jp_at[jp] = None
        # Point at the ELF's own copy wherever it holds the key verbatim and
        # no later step rewrites it: owning a copy of every key cost ~25 KB
        # of the unchanged extension. UI_OWN_COPY lists the known rewrites;
        # check_issue_fixes reads every key back, so a new one fails the gate.
        if jp not in UI_OWN_COPY and jp not in UI_KEY_VWF:
            try:
                m = rod.find(NUL + jp.encode('cp932') + NUL)
            except UnicodeEncodeError:
                m = -1
            if m >= 0:
                jp_at[jp] = segs[0]['va'] + rod_lo + m + 1
    # Strings start right after the largest table this run can emit (every
    # candidate key plus the terminator), not at the fixed 8191-entry mark:
    # the unused reservation was ~22 KB the UTF-8 labels and unlock reports,
    # which follow the hook strings in the same unchanged extension, needed.
    strings_at = min(_off(segs, NAME_STR),
                     (_off(segs, NAME_TBL) + 8 * (len(jp_at) + 1) + 15) & ~15)
    cur = strings_at
    limit = _off(segs, EXT_VA) + EXT_SIZE
    entries, undrawable, n_ui = [], 0, 0
    # Many source/numbering variants have identical immutable output. Own
    # each exact encoded English string once; lookup keys remain separate.
    # Include padding and the tutorial's adjacent punctuation in the key.
    english_at = {}
    for jp in sorted(jp_at, key=lambda k: (k not in ui, k)):   # UI first: first match wins
        try:
            import command_layout
            enc = command_layout.dialog_prefix(jp) + _encode_marked(en_of[jp], mapping) + NUL
            if "" in jp:
                # The tutorial draws a colour-marked line's sentence-final 。 by
                # reading THE NEXT STRING IN MEMORY after the line. With the
                # hook that was whatever entry followed ours, so a stray
                # fragment of another line appeared. Put the "." right there.
                enc += _encode_marked(".", mapping) + NUL
        except SystemExit:
            undrawable += 1
            continue
        jva = jp_at[jp]
        if jva is None:                                # copy the Japanese in
            nb = (_encode_marked(jp, mapping) if jp in UI_KEY_VWF else jp.encode('cp932')) + NUL
            if cur + len(nb) > limit:
                raise SystemExit('name-hook Japanese does not fit the EXT segment '
                                 '(%d entries emitted, needs %d bytes beyond the limit)'
                                 % (len(entries), cur + len(nb) - limit))
            b[cur:cur + len(nb)] = nb
            jva = _va(segs, cur)
            cur = (cur + len(nb) + 1) & ~1
        eva = english_at.get(enc)
        if eva is None:
            if cur + len(enc) > limit:
                raise SystemExit('name-hook English does not fit the EXT segment '
                                 '(%d entries emitted, needs %d bytes beyond the limit)'
                                 % (len(entries), cur + len(enc) - limit))
            b[cur:cur + len(enc)] = enc
            eva = _va(segs, cur)
            english_at[enc] = eva
            cur = (cur + len(enc) + 1) & ~1
        flags = (0x80000000 if jp in UI_PREFIX else 0) | (0x40000000 if jp in UI_JOINED else 0)
        entries.append((jva, eva | flags))
        n_ui += jp in ui
    t = _off(segs, NAME_TBL)
    if t + 8 * (len(entries) + 1) > strings_at:
        raise SystemExit('name-hook table does not fit before its strings')
    for i, (jva, eva) in enumerate(entries):
        struct.pack_into('>II', b, t + 8 * i, jva, eva)
    struct.pack_into('>II', b, t + 8 * len(entries), 0, 0)
    if HOOK_HEXPROBE:
        ho = _off(segs, HEXTBL_VA)
        for i, ch in enumerate("0123456789abcdef "):     # 17th: the space, for the lead-in
            struct.pack_into('>H', b, ho + 2 * i, mapping[ch])
    stub = name_stub()
    so = NAME_STUB - segs[0]['va']
    if so + len(stub) > NAME_TBL - segs[0]['va']:
        raise SystemExit('name-hook stub overruns the table')
    b[so:so + len(stub)] = stub
    site = NAME_SITE - segs[0]['va']
    if struct.unpack_from('>I', b, site)[0] != NAME_ORIG:
        raise SystemExit('name-hook site does not hold the expected cmpwi')
    struct.pack_into('>I', b, site, 0x48000000 | ((NAME_STUB - NAME_SITE) & 0x03fffffc))
    return len(entries), undrawable, cur, n_ui

def apply_kw(b, segs):
    """Patch both keyword-position call sites; returns edited ranges."""
    edited = []
    so = KW_ACC_SITE - segs[0]["va"]
    if struct.unpack(">II", b[so:so + 8]) != KW_ACC_ORIG:
        raise SystemExit("keyword accumulate site does not hold srawi/addze")
    h1 = segs[1]["hdr"]
    memsz = struct.unpack(">Q", b[h1 + 40:h1 + 48])[0]
    if segs[1]["va"] + memsz != BSS_PAGE:
        raise SystemExit("BSS_PAGE must be the old end of segment 1 (%#x)" % (segs[1]["va"] + memsz))
    b[h1 + 40:h1 + 48] = struct.pack(">Q", memsz + BSS_GROW)
    edited.append((h1 + 40, h1 + 48))
    stub = kw_acc_stub(); to = KW_ACC_STUB - segs[0]["va"]
    b[to:to + len(stub)] = stub
    b[so:so + 8] = struct.pack(">II", 0x48000001 | ((KW_ACC_STUB - KW_ACC_SITE) & 0x03fffffc), 0x60000000)
    edited.append((so, so + 8)); edited.append((to, to + len(stub)))
    for site, reg, stub_va in KW_SITES:
        so = site - segs[0]["va"]
        want = 0x48000001 | ((KW_ORIG - site) & 0x03fffffc)
        if struct.unpack(">I", b[so:so + 4])[0] != want:
            raise SystemExit("keyword call site %#x does not hold bl 0x1d0708" % site)
        stub = kw_stub(reg)
        to = stub_va - segs[0]["va"]
        b[to:to + len(stub)] = stub
        b[so:so + 4] = struct.pack(">I", 0x48000001 | ((stub_va - site) & 0x03fffffc))
        edited.append((so, so + 4)); edited.append((to, to + len(stub)))
    return edited


def inplace_names(b, segs, names, mapping):
    """Translate EBOOT name strings IN PLACE: overwrite each Japanese string
    that is a settled glossary/library name with its English pair encoding,
    NUL-padded to the ORIGINAL byte length. No pointer moves and no length
    changes, so lookups that key on a name pointer or its length still work
    (repointing them abort()ed the game); only the content flips, seen the
    same way by the display and any in-EBOOT key comparison. A name whose
    English does not fit its Japanese byte slot is left Japanese.

    Returns (overwritten, left_too_long, left_undrawable)."""
    rod_lo = segs[0]["off"]
    rod_hi = segs[0]["off"] + segs[0]["filesz"]
    done = 0; toolong = 0; undraw = 0; keyed = 0; seen = set()
    for jp in sorted(names, key=len, reverse=True):
        try:
            nb = jp.encode("cp932")
        except Exception:
            continue
        key = NUL + nb + NUL
        start = rod_lo
        while True:
            m = b.find(key, start, rod_hi)
            if m < 0:
                break
            so = m + 1                          # the string bytes
            start = so + 1
            if so in seen:
                continue
            seen.add(so)
            try:
                enc = dg.encode_mixed(names[jp], mapping, newline=bytes((10,)))
            except SystemExit:
                undraw += 1; continue
            if len(enc) > len(nb):
                toolong += 1; continue
            # SAFETY: only overwrite if every pointer to this string is in the
            # display-name arrays (0x85e000..0x869000) or the TOC. Names also
            # referenced by the pilot roster / Lua string pools are used as
            # lookup KEYS; changing their content there abort()ed the game
            # (Genion entry). Skip those -- RPW renders the roster anyway.
            sva = so + segs[0]["va"]
            key4 = struct.pack(">I", sva)
            safe = True
            q = 0
            while True:
                q = b.find(key4, q)
                if q < 0:
                    break
                if (q & 3) == 0:
                    rva = q            # file offset; compare as file, map region below
                    in_display = SAFE_LO - segs[1]["va"] + segs[1]["off"] <= q < SAFE_HI - segs[1]["va"] + segs[1]["off"]
                    in_toc = TOC_LO - segs[1]["va"] + segs[1]["off"] <= q < TOC_HI - segs[1]["va"] + segs[1]["off"]
                    if not (in_display or in_toc):
                        safe = False
                        break
                q += 4
            if not safe:
                keyed += 1
                continue
            b[so:so + len(nb)] = enc + NUL * (len(nb) - len(enc))
            done += 1
    return done, toolong, undraw, keyed

def loose_names(b, segs, names, mapping):
    """Repoint every DATA pointer that still targets a Japanese glossary
    name to an English rendering written into the gap. Catches the many
    hardcoded name-pointer tables the game has beyond the series/keyword
    arrays (character names like Hibiki Kamishiro, keyword/proper nouns).
    Runs AFTER the series/keyword patch, so those pointers already target
    English and are skipped. Returns (repointed, distinct, gap_end_off)."""
    rod = b
    # every JP glossary string present in the executable, longest first so a
    # name that is a prefix of another does not shadow it
    jp_va = {}
    for jp in sorted(names, key=len, reverse=True):
        try:
            nb = jp.encode("cp932")
        except Exception:
            continue
        for m in re.finditer(re.escape(b"\x00" + nb + b"\x00"), rod):
            jp_va.setdefault(m.start() + 1 + segs[0]["va"], names[jp])
    # write English once per distinct string into the gap
    cur = LOOSE_STR - segs[0]["va"]
    en_va = {}
    where = {}
    for sva, en in jp_va.items():
        try:
            enc = dg_encode(en, mapping)
        except SystemExit:
            continue
        if enc not in where:
            if cur + len(enc) + 1 > segs[1]["off"]:
                raise SystemExit("loose-name gap full")
            where[enc] = segs[0]["va"] + cur
            b[cur:cur + len(enc) + 1] = enc + b"\x00"
            cur = (cur + len(enc) + 1 + 3) & ~3
        en_va[sva] = where[enc]
    # Repoint ONLY the character-detail / keyword name tables. The early-data
    # pilot roster (va ~0x795000) and TOC slots hold the SAME names but are
    # lookup keys / structured pointers, not display strings; repointing them to
    # unassigned-SJIS English broke a name lookup and the game abort()ed opening
    # a robot entry (Genion). RPW already renders the roster in the list, so
    # nothing visible is lost by skipping it.
    LO_VA, HI_VA = 0x85E000, 0x869000
    lo = max(segs[1]["off"], LO_VA - segs[1]["va"] + segs[1]["off"])
    hi = min(segs[1]["off"] + segs[1]["filesz"], HI_VA - segs[1]["va"] + segs[1]["off"])
    repointed = 0
    for o in range(lo, hi - 3, 4):
        v = struct.unpack_from(">I", b, o)[0]
        nv = en_va.get(v)
        if nv is not None:
            struct.pack_into(">I", b, o, nv)
            repointed += 1
    return repointed, len(where), cur


def dg_encode(en, mapping):
    import digraph as dg
    return dg.encode_mixed(en, mapping, newline=bytes((10,)))

def apply_vwf(b, segs, widths):
    """widths: {cell_index: texels}; cells not listed keep 32."""
    table = bytearray([32] * ATLAS_CELLS)
    for cell, w in widths.items():
        if not 0 <= cell < ATLAS_CELLS or not 0 <= w <= 64:
            raise SystemExit("bad width entry %r" % ((cell, w),))
        table[cell] = w
    stub = vwf_stub()
    assert STUB_VA + len(stub) <= KW_SITES[0][2], 'VWF stub overlaps keyword stub'
    so, to = STUB_VA - segs[0]["va"], TABLE_VA - segs[0]["va"]
    site = PATCH_SITE - segs[0]["va"]
    if struct.unpack(">I", b[site:site + 4])[0] != PATCH_ORIG:
        raise SystemExit("patch site does not hold the expected lfs")
    b[so:so + len(stub)] = stub
    b[to:to + ATLAS_CELLS] = table
    bl = 0x48000001 | ((STUB_VA - PATCH_SITE) & 0x03fffffc)
    b[site:site + 4] = struct.pack(">I", bl)
    kw = apply_kw(b, segs)
    import search_layout
    kw.extend(search_layout.apply(b, segs))
    import link_background_layout
    kw.extend(link_background_layout.apply(b, _segments(b), dialogue_scene=True))
    return {"kw": kw, "stub": (so, so + len(stub)), "table": (to, to + ATLAS_CELLS), "site": (site, site + 4),
            "narrowed": sum(1 for w in table if w != 32)}

UI_ENABLE = True
# Menu labels whose slot is far too small to translate in place -- 姓 is ONE
# cell, 移動 is two -- but which are reached through a POINTER in a display
# table, so they can be repointed at longer English instead.
#
# Only pointers verified to be display-table entries are listed. The table at
# 0x790794 is 16-byte records of (x, y, index, label); 0x7d7210 is the name
# entry screen's own row. Repointing EBOOT name strings in general abort()ed
# the game because many are lookup KEYS -- these are not, and each was checked
# to have exactly one or two referents.
UI_LABELS = {
    0x790794: _l10n.literal('eboot.UI_LABELS/0'),
    0x7907a4: _l10n.literal('eboot.UI_LABELS/1'),
    0x7907b4: _l10n.literal('eboot.UI_LABELS/2'),
    0x7907c4: _l10n.literal('eboot.UI_LABELS/3'),
    0x7907d8: _l10n.literal('eboot.UI_LABELS/4'),
    0x7907dc: _l10n.literal('eboot.UI_LABELS/5'),
    0x7907e0: _l10n.literal('eboot.UI_LABELS/6'),
    0x7907e4: _l10n.literal('eboot.UI_LABELS/7'),
    0x7d7210: _l10n.literal('eboot.UI_LABELS/8'),
    0x7d7214: _l10n.literal('eboot.UI_LABELS/9'),
}
# REVERTED: repointing カミシロ through 0x8661f8 (display-name array) and
# 0x7dc144 (TOC) produced "ゲームデータが壊れています" on the next boot. Those
# two regions are exactly the ones inplace_names refuses to touch, because
# entries there are lookup KEYS and structured pointers, not display strings --
# the same failure that abort()ed the game on the Genion entry. The 16-byte
# display records at 0x790794 are safe; these are not.
KAMISHIRO_UNSAFE = {0x8661f8: "Kamishiro", 0x7dc144: "Kamishiro"}


# --- the COMMAND menu --------------------------------------------------------
# The map COMMAND menu (移動 / 攻撃 / 地上 / 精神 / 能力 ...) and the system
# menu (フェイズ終了 / 検索 / 部隊表 ...) are NOT textures and are NOT in the
# UI member: their labels are a UTF-8 string table in .rodata (file
# 0x6d4dd8.., VA 0x6e4dd8.., 8-byte slots, right beside the
# AID_CommandMenuMng class name) drawn through a Unicode path -- which is
# why rewriting every cp932 copy of 移動 changed nothing on screen. Each
# label has exactly one referent: the first word of a 36-byte command
# descriptor {label, id, handler, arg, ...} in .data (0x859044.. system
# menu, 0x8591ac.. unit commands). A display descriptor with a handler
# pointer is not a lookup key, so repointing it is safe in the way the
# 0x790794 records are. English that fits the slot is written in place;
# longer English goes into the gap and the descriptor is repointed.
COMMAND_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "translation", "ui_eboot.json")
COMMAND_ANCHOR = b"AID_CommandMenuMngE"  # the class name just before the table; never translated
COMMAND_SPAN = 0x500                    # the table ends within this many bytes after it
COMMAND_ENABLE = True
COMMAND_REPOINT = True                  # False: labels that do not fit stay Japanese
COMMAND_FACE = "vwf"                    # "vwf": the VWF letter cells; "ascii": the game's own Latin

# The UTF-8 path draws through a 65,536-entry Unicode -> cp932 table in
# .data (VA 0x7df8c8; one big-endian u16 per codepoint; 0x81A1 = ■ where
# unmapped; 3,864 entries mapped). ASCII is ■ there too, so plain ASCII
# labels reach the atlas by some other route, at fixed pitch and in the
# shipped Latin. To draw them with the VWF cells instead, U+0100+ch --
# unmapped in the original, and a two-byte sequence that cannot skip the
# table -- is pointed at the VWF cell of ch, and the labels are written with
# those codepoints. Same glyphs, same width table as the dialogue.
UNICODE_ANCHOR = bytes.fromhex("829f82a082a182a2")   # entries U+3041.. = ぁあぃい
UNICODE_ANCHOR_CP = 0x3041
VWF_CP_BASE = 0x100


def unicode_table(b, segs):
    """File offset of the Unicode -> cp932 table, checked by two entries."""
    d_lo, d_hi = segs[1]["off"], segs[1]["off"] + segs[1]["filesz"]
    a = b.find(UNICODE_ANCHOR, d_lo, d_hi)
    if a < 0 or b.find(UNICODE_ANCHOR, a + 1, d_hi) >= 0:
        raise SystemExit("Unicode table anchor not found exactly once in .data")
    t = a - UNICODE_ANCHOR_CP * 2
    if (struct.unpack_from(">H", b, t + 0xFF21 * 2)[0] != 0x8260        # Ａ
            or struct.unpack_from(">H", b, t + 0x4E9C * 2)[0] != 0x889F):  # 亜
        raise SystemExit("Unicode table failed its check entries")
    return t


def vwf_face(b, segs, mapping):
    """Point U+0100+ch at the VWF cell of ch for every letter in `mapping`.
    Returns ((lo, hi) edited, encode) -- or (None, identity) when the
    mapping is a pair mapping, which has no single-letter cells."""
    letters = {k: v for k, v in mapping.items()
               if isinstance(k, str) and len(k) == 1 and 0x20 <= ord(k) < 0x7F}
    if not letters:
        return None, (lambda s: s)
    t = unicode_table(b, segs)
    lo, hi = t + (VWF_CP_BASE + 0x20) * 2, t + (VWF_CP_BASE + 0x7F) * 2
    for ch, code in letters.items():
        o = t + (VWF_CP_BASE + ord(ch)) * 2
        have = struct.unpack_from(">H", b, o)[0]
        if have == code:
            continue                            # already set by an earlier pass
        if have != 0x81A1:
            raise SystemExit("U+%04X is mapped in the original; move VWF_CP_BASE"
                             % (VWF_CP_BASE + ord(ch)))
        struct.pack_into(">H", b, o, code)

    def encode(s):
        return "".join(chr(VWF_CP_BASE + ord(c)) if c in letters else c for c in s)
    return (lo, hi), encode


# Legacy padding allocation. Map and unit COMMAND buttons override this
# with command_layout's live-pitch pads; the historical
# pitch estimate below must not be used for those buttons.
# The menu places a label at centre - count * pitch / 2, where
# pitch is the fixed 37.28/32 cell advance and count the number of codes;
# the VWF ink is narrower, so every label sat left of centre by half the
# difference (seen on screen). One invisible leading glyph per label fixes
# it: its cell is a blank one (cp932 row 0x88 below 0x9F is unassigned and
# empty in the atlas), its Unicode entry is U+0180+k, and its width-table
# byte is chosen so that the extra advance is exactly what re-centres the
# ink -- the VWF stub scales by W/32 and W is a byte, so one pad reaches
# 8 cells. Labels that share a pad width share a pad.
COMMAND_ALIGN = "left"                  # "left", "center" or "none"
COMMAND_PITCH = 37.28 / 32              # nominal advance in cells (docs/FONT_HUNT.md)
# "left": every label's ink starts COMMAND_LEFT cells from the button centre
# (the button is about 4.4 cells wide each side). A label too short to reach
# that far with one pad gets extra zero-width pads, since each code moves the
# start 0.58 cell left; count never exceeds the 9 the Japanese menu uses.
COMMAND_LEFT = -3.4
PAD_CP_BASE = 0x180                     # U+0180.. -> pad cells, one per distinct width
PAD_CODES = [0x8800 | t for t in range(0x40, 0x9F) if t != 0x7F]   # 94 blank cells


class _CenterPads:
    def __init__(self, b, segs, mapping, widths):
        self.b, self.segs = b, segs
        self.t = unicode_table(b, segs)
        self.W = {ch: widths.get(dg.cell_index(code), 32) for ch, code in mapping.items()
                  if isinstance(ch, str) and len(ch) == 1}
        self.used = set(mapping.values())
        self.slots = {}                             # pad width -> codepoint

    def prefix(self, en):
        ink = sum(self.W.get(c, 32) for c in en) / 32.0
        if COMMAND_ALIGN == "left":
            k = 1                                   # pads; each moves the start 0.58 left
            while COMMAND_PITCH * (len(en) + k) / 2 < -COMMAND_LEFT:
                k += 1
            w = int(round(32 * (COMMAND_PITCH * (len(en) + k) / 2 + COMMAND_LEFT)))
            return self._pad(min(w, 255)) + self._pad(0) * (k - 1)
        n = len(en) + 1                             # centre: the one pad counts too
        w = int(round(32 * (COMMAND_PITCH * n / 2 - ink / 2)))
        if w <= 0:
            return ""                               # ink already wider than nominal
        return self._pad(min(w, 255))

    def _pad(self, w):
        if w not in self.slots:
            k = len(self.slots)
            if k >= len(PAD_CODES):
                raise SystemExit("out of pad cells for the COMMAND menu")
            code = PAD_CODES[k]
            import command_layout
            assert code not in command_layout.CODES, 'Legacy padding reached reserved live pads'
            if code in self.used:
                raise SystemExit("pad cell %#x is a letter cell this build" % code)
            cp = PAD_CP_BASE + k
            o = self.t + cp * 2
            if struct.unpack_from(">H", self.b, o)[0] != 0x81A1:
                raise SystemExit("U+%04X is mapped in the original" % cp)
            struct.pack_into(">H", self.b, o, code)
            self.b[TABLE_VA - self.segs[0]["va"] + dg.cell_index(code)] = w
            self.slots[w] = cp
        return chr(self.slots[w])


def load_commands(path=COMMAND_FILE):
    if not os.path.exists(path):
        return {}
    d = json.load(open(path, encoding="utf-8"))
    labels = {l["jp"]: l["en"] for l in d["lines"] if l.get("en")}
    if os.path.abspath(path) == os.path.abspath(UI_UTF8_FILE):
        import battle_screen_labels
        for jp, en in battle_screen_labels.utf8_labels().items():
            if jp in labels and labels[jp] != en:
                raise ValueError('Battle/help UTF-8 label conflicts with canonical text: ' + jp)
            labels[jp] = en
        import battle_effect_labels
        for jp,en in battle_effect_labels.labels().items():
            if jp in labels and labels[jp]!=en:
                raise ValueError('Battle effect UTF-8 label conflicts with canonical text: '+jp)
            labels[jp]=en
        import command_choice_labels
        for jp,en in command_choice_labels.utf8_labels().items():
            if jp in labels and labels[jp]!=en:
                raise ValueError('Command choice UTF-8 conflict: '+jp)
            labels[jp]=en
        import key_help_labels
        for jp,en in {**key_help_labels.LABELS,**key_help_labels.EXTRA}.items():
            # Existing shared labels retain their established wording.
            labels.setdefault(jp,en)
    return labels


UI_UTF8_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "translation", "ui_utf8.json")


def command_labels(b, segs, labels, cur, mapping=None, widths=None, window=True, align=None):
    """Translate UTF-8 label strings. `window=True` is the command-menu
    table around COMMAND_ANCHOR, one occurrence per label, padded to
    COMMAND_ALIGN; `window=False` is every other standalone occurrence in
    .rodata (window titles, prompts), drawn where the game puts them, no
    pads. Returns (in_place, repointed, stayed, cur, face, pads) where
    stayed is [(jp, why)], face is the edited Unicode-table range or None
    for plain ASCII, and pads the number of distinct pad cells."""
    face, enc_fn, pad = None, (lambda s: s), None
    if align is None:
        align = COMMAND_ALIGN if window else "none"
    if COMMAND_FACE == "vwf" and mapping:
        face, enc_fn = vwf_face(b, segs, mapping)
    if face and align in ("left", "center") and widths is not None:
        pad = _CenterPads(b, segs, mapping, widths)
        raw = enc_fn
        import command_layout
        if window:
            command_layout.install(b, segs, mapping, widths)
        def enc_fn(s):
            legacy = pad.prefix(s)  # keep other labels' pad allocation stable
            leading = command_layout.prefix(s) if window and s in command_layout.UTF8_LABELS else legacy
            return leading + raw(s)
    if not window and face:
        import command_layout, settings_descriptions, intermission_layout
        raw_encoder = enc_fn
        def enc_fn(s):
            return (command_layout.prefix(s) if s in settings_descriptions.LABELS or s in intermission_layout.DESCRIPTIONS.values() else '') + raw_encoder(s)
    rod_lo = segs[0]["off"]
    rod_hi = rod_lo + segs[0]["filesz"]
    d_lo, d_hi = segs[1]["off"], segs[1]["off"] + segs[1]["filesz"]
    limit = _off(segs, EXT_VA) + EXT_SIZE
    a = b.find(COMMAND_ANCHOR, rod_lo, rod_hi)
    if a < 0 or b.find(COMMAND_ANCHOR, a + 1, rod_hi) >= 0:
        raise SystemExit("command-menu anchor %r not found exactly once" % COMMAND_ANCHOR)
    lo, hi = a, min(rod_hi, a + COMMAND_SPAN)
    in_place, repointed, stayed = 0, 0, []
    for jp, en in labels.items():
        key = NUL + jp.encode("utf-8") + NUL
        if window:
            m = b.find(key, lo, hi)
            if m < 0 or b.find(key, m + 1, hi) >= 0:
                stayed.append((jp, "not exactly once in the table"))
                continue
            hits = [m]
        else:
            hits, p = [], rod_lo
            while True:
                m = b.find(key, p, rod_hi)
                if m < 0:
                    break
                if not lo <= m < hi:                # the command table is the other file's
                    hits.append(m)
                p = m + 1
            if not hits:
                stayed.append((jp, "no standalone UTF-8 occurrence"))
                continue
        for m in hits:
            encoded = enc_fn(en)
            if not window and face and m+1 in command_layout.PREP_ROWS:
                source_jp, popup_en = command_layout.PREP_ROWS[m+1]
                assert jp == source_jp, 'Prep menu source changed'
                encoded = command_layout.prefix(popup_en) + enc_fn(popup_en)
            r = _label_one(b, segs, m, jp, encoded, cur, limit, d_lo, d_hi, rod_hi)
            kind, cur = r
            if kind == "in_place":
                in_place += 1
            elif kind == "repointed":
                repointed += 1
            else:
                stayed.append((jp, kind))
    return in_place, repointed, stayed, cur, face, (len(pad.slots) if pad else 0)


def _label_one(b, segs, m, jp, text, cur, limit, d_lo, d_hi, rod_hi):
    """One occurrence: in place if the UTF-8 fits its slot, else into the
    EXT segment with every .data referent repointed. Returns (kind, cur)."""
    if True:
        so = m + 1
        end = so + len(jp.encode("utf-8"))
        while end < rod_hi and b[end] == 0:
            end += 1
        cap = end - so - 1                      # keep one NUL
        enc = text.encode("utf-8")
        va = so + segs[0]["va"]
        key4 = struct.pack(">I", va)
        refs, q = [], d_lo
        while True:
            q = b.find(key4, q, d_hi)
            if q < 0:
                break
            if (q & 3) == 0:
                refs.append(q)
            q += 1
        if len(enc) <= cap:
            b[so:so + cap + 1] = enc + NUL * (cap + 1 - len(enc))
            return "in_place", cur
        if not COMMAND_REPOINT:
            return "too long (%d > %d), repoint disabled" % (len(enc), cap), cur
        if not refs:
            return "too long and no referent in .data", cur
        if cur + len(enc) + 1 > limit:
            return "no room in the EXT segment", cur
        b[cur:cur + len(enc) + 1] = enc + NUL
        for q in refs:                          # 検索 has two; both are labels
            struct.pack_into(">I", b, q, _va(segs, cur))
        return "repointed", (cur + len(enc) + 1 + 7) & ~7


def ui_labels(b, segs, mapping, cur):
    """Repoint the menu labels in UI_LABELS at English written from `cur`.

    `cur` is name_hook's high-water mark, so this never collides with the name
    strings -- the alternative was a hardcoded address chosen by estimating
    how much of NAME_STR was in use, which is the sort of guess that has cost
    this project several bad builds already.
    """
    done, skipped = 0, []
    limit = _off(segs, EXT_VA) + EXT_SIZE
    for ptr_va, en in sorted(UI_LABELS.items()):
        po = _off(segs, ptr_va)
        if po is None:
            skipped.append((ptr_va, "pointer not in a mapped segment"))
            continue
        old = struct.unpack(">I", b[po:po + 4])[0]
        oo = _off(segs, old)
        if oo is None:
            skipped.append((ptr_va, "target %#x unmapped" % old))
            continue
        try:
            enc = dg.encode_mixed(en, mapping, newline=bytes((10,))) + NUL
        except SystemExit:
            skipped.append((ptr_va, "undrawable"))
            continue
        if cur + len(enc) > limit:
            skipped.append((ptr_va, "no room"))
            continue
        b[cur:cur + len(enc)] = enc
        b[po:po + 4] = struct.pack(">I", _va(segs, cur))
        cur = (cur + len(enc) + 7) & ~7
        done += 1
    return done, skipped, cur


TRAINING_STAT_CELLS = ((0x710890, '格', '\ue018'), (0x710898, '射', '\ue019'))


def training_stat_cells(b):
    """Patch the runtime overrides for training rows 0/1, not their FSSA template.

    VA 0x31b32c/0x31b34c load these through TOC -0x1a30/-0x1a2c and
    call the widget text setter 0x529fc with row 0/1. The alternate song
    branch uses the adjacent 歌/ー strings, which must remain untouched.
    """
    for off, jp, pua in TRAINING_STAT_CELLS:
        if b[off:off + 8] != jp.encode('cp932') + bytes(6):
            raise SystemExit('unexpected training-stat label at %#x' % off)
    for off, jp, pua in TRAINING_STAT_CELLS:
        b[off:off + 2] = dg._raw_bytes(pua)
    return len(TRAINING_STAT_CELLS)


MOVEMENT_TYPE_TABLES = (0x6D6140, 0x710EA0, 0x711258)
MOVEMENT_TYPE_CHARS = tuple(zip("空陸水地", "\ue000\ue001\ue002\ue004"))
MOVEMENT_EXCLUSIVE = (
    (0x6D6160, '空専用', '\ue000\ue017\u3000'),
    (0x6D6168, '陸専用', '\ue001\ue017\u3000'),
    (0x6D6170, '空水専用', '\ue000\ue002\ue017\u3000'),
    (0x6D6180, '水専用', '\ue002\ue017\u3000'),
    (0x710E80, '空専用', '\ue000\ue017\u3000'),
    (0x710E88, '空水専用', '\ue000\ue002\ue017\u3000'),
    (0x710E98, '水専用', '\ue002\ue017\u3000'),
)


def movement_type_cells(b):
    """Replace the three four-label movement formatter tables in place.

    Each isolated cp932 character occupies an eight-byte, NUL-padded slot.
    The UI assembles these with movement points, slashes and dash variants,
    so matching a complete four-character draw string misses some screens.
    Reuse the terrain's small one-cell words without touching global kanji
    glyphs, text pointers, or the formatter's numbers and punctuation.
    """
    expected = b''.join(jp.encode('cp932') + bytes(6) for jp, _ in MOVEMENT_TYPE_CHARS)
    for base in MOVEMENT_TYPE_TABLES:
        if b[base:base + len(expected)] != expected:
            raise SystemExit('unexpected movement-type table at %#x' % base)
    for base in MOVEMENT_TYPE_TABLES:
        for i, (_jp, pua) in enumerate(MOVEMENT_TYPE_CHARS):
            code = dg.TINY_CELLS[pua][1]
            b[base + i * 8:base + i * 8 + 2] = struct.pack('>H', code)
    for off, jp, en in MOVEMENT_EXCLUSIVE:
        source = jp.encode('cp932')
        encoded = dg._raw_bytes(en)
        if len(encoded) != len(source) or b[off:off + len(source) + 1] != source + NUL:
            raise SystemExit('unexpected exclusive movement label at %#x' % off)
        b[off:off + len(source)] = encoded
    return len(MOVEMENT_TYPE_TABLES) * len(MOVEMENT_TYPE_CHARS) + len(MOVEMENT_EXCLUSIVE)


def patch(b, names, mapping, pairs_used=(), widths=None, pair_mapping=None):
    b = bytearray(b)
    segs = _segments(b)
    if len(segs) < 2 or segs[0]["filesz"] != segs[0]["memsz"]:
        raise SystemExit("unexpected segment layout")
    gap_lo, gap_hi = segs[0]["off"] + segs[0]["filesz"], segs[1]["off"]
    if bytes(b[gap_lo:gap_hi]) != bytes(gap_hi - gap_lo):
        raise SystemExit("padding between segments is not zero; refusing to use it")
    arrays = find_arrays(b, segs)

    # what each table entry names, before the edit
    jp_of = {}
    for base in arrays:
        for i in range(_count(arrays, base)):
            va = struct.unpack(">I", b[base + 4 * i:base + 4 * i + 4])[0]
            if va:
                jp_of[va] = _cstr(b, _off(segs, va)).decode("cp932")

    # English strings go into the (about to be mapped) gap
    new_va, cur = {}, (gap_lo + 15) & ~15
    stayed = []
    for va, jp in sorted(jp_of.items()):
        en = names.get(jp)
        if not en:
            stayed.append(jp)
            continue
        enc = dg.encode_mixed(en, mapping, newline=bytes((10,))) + NUL
        if cur + len(enc) > TABLE_VA - segs[0]["va"]:
            raise SystemExit("string space full at %s (strings %#x.., table at %#x)" % (jp, gap_lo, TABLE_VA))
        b[cur:cur + len(enc)] = enc
        new_va[va] = segs[0]["va"] + cur
        cur = (cur + len(enc) + 7) & ~7

    # repoint every entry that named a translated series
    repointed = 0
    for base in arrays:
        for i in range(_count(arrays, base)):
            o = base + 4 * i
            va = struct.unpack(">I", b[o:o + 4])[0]
            if va in new_va:
                b[o:o + 4] = struct.pack(">I", new_va[va])
                repointed += 1

    # map the gap: segment 0 now ends where segment 1 begins
    h = segs[0]["hdr"]
    new_sz = gap_hi - segs[0]["off"]
    b[h + 32:h + 40] = struct.pack(">Q", new_sz)     # p_filesz
    b[h + 40:h + 48] = struct.pack(">Q", new_sz)     # p_memsz
    # the third segment: hook table and every English string from here on
    ext_off, ext_ph = add_segment(b)
    segs = _segments(b)

    vwf = apply_vwf(b, segs, widths) if widths is not None else None
    if vwf and vwf["stub"][1] > gap_hi - segs[0]["off"] + segs[0]["off"]:
        raise SystemExit("stub outside the gap")
    if vwf and cur > vwf["stub"][0]:
        raise SystemExit("series strings overlap the stub; move STUB_VA")

    # DISABLED: repointing EBOOT name pointers is unsafe -- many are lookup
    # keys / structured pointers (pilot roster, TOC), not display strings, and
    # repointing them abort()ed the game (Genion). Left off; the few library
    # list names sourced here (e.g. Hibiki Kamishiro) stay Japanese.
    # VWF letters, matching RPW_DATA -- the lists draw these names beside
    # the ones RPW supplies, so the two must use the same face.
    hook = name_hook(b, segs, names, mapping) if NAME_ENABLE else None
    ui = ui_labels(b, segs, mapping, hook[2]) if (hook and UI_ENABLE) else None
    cmds = load_commands() if COMMAND_ENABLE else {}
    cmd_cur = ui[2] if ui else (hook[2] if hook else None)
    commands = command_labels(b, segs, cmds, cmd_cur, mapping, widths) if (cmds and cmd_cur) else None
    utf8 = load_commands(UI_UTF8_FILE) if COMMAND_ENABLE else {}
    u_cur = commands[3] if commands else cmd_cur
    if utf8 and u_cur:
        import battle_screen_labels
        battle_screen_labels.check_source_elf(b)
        import battle_effect_labels
        battle_effect_labels.check_source(b)
        import command_choice_labels
        command_choice_labels.check_source(b)
        import skill_name_transport
        skill_name_transport.check_source(b)
        import battle_speaker_names
        battle_speaker_names.check_source(b)
    utf8_labels = command_labels(b, segs, utf8, u_cur, mapping, widths, window=False) if (utf8 and u_cur) else None
    loose =loose_names(b, segs, names, mapping) if (widths is not None and LOOSE_ENABLE) else None
    inplace = inplace_names(b, segs, names, pair_mapping) if (widths is not None and pair_mapping and INPLACE_ENABLE) else None
    # a string still drawn in Japanese must keep its cells
    clash = [jp for jp in stayed if rsv.codes(jp) & set(pairs_used)]
    if clash:
        raise SystemExit("table strings left Japanese share cells with this run's pairs: %r" % clash)

    movement = movement_type_cells(b) if widths is not None else 0
    training = training_stat_cells(b) if widths is not None else 0
    import runtime_names
    runtime = runtime_names.apply(b, segs, mapping) if widths is not None else 0
    report = {"runtime_names": runtime, "training_stats": training, "movement_types": movement, "vwf": vwf, "loose": loose, "inplace": inplace, "hook": hook,
              "ui": ui, "commands": commands, "utf8": utf8_labels, "translated": len(new_va), "stayed": stayed, "repointed": repointed,
              "gap_used": cur - gap_lo, "gap": gap_hi - gap_lo,
              "arrays": [hex(a) for a in arrays], "mapped_va": hex(segs[0]["va"] + gap_lo)}
    import battle_reports
    b=bytearray(battle_reports.patch_format(b,mapping))
    import president_report_layout
    b=bytearray(president_report_layout.apply(b,mapping))
    import date_card_layout
    b=bytearray(date_card_layout.apply(b,mapping)[0])
    import unlock_reports
    b,extra_cursor=unlock_reports.patch(b,mapping,utf8_labels[3] if utf8_labels else u_cur)
    if widths is not None:
        import battle_speaker_names
        b,extra_cursor=battle_speaker_names.patch(b,extra_cursor)
    import activation_prompts
    b,extra_cursor=activation_prompts.patch(b,mapping,extra_cursor)
    report['activation_prompts_end'] = extra_cursor
    if widths is not None:
        import battle_name_transport
        b,extra_cursor=battle_name_transport.patch(b,extra_cursor)
        report['battle_name_transport_end'] = extra_cursor
    import message_class_formats
    b=message_class_formats.patch(b,mapping)
    import trader_spirit_prompts
    b=trader_spirit_prompts.patch_elf(b,mapping)
    import trader_upgrade_text
    b=trader_upgrade_text.patch(b,mapping)
    import operation_indent
    b=operation_indent.apply(b)
    return bytes(b), report


def verify(orig, new, names, mapping, vwf=None):
    """Read the patched file back the way the game will."""
    import ppc_permissions
    ppc_permissions.check_changed_branches(orig, new)
    import trader_spirit_prompts
    trader_spirit_prompts.check_elf(new,mapping)
    if vwf:
        import battle_name_transport
        battle_name_transport.check(new)
        import runtime_names
        runtime_names.verify(new, _segments(new), mapping)
        for off, jp, pua in TRAINING_STAT_CELLS:
            assert orig[off:off + 8] == jp.encode('cp932') + bytes(6)
            assert new[off:off + 8] == dg._raw_bytes(pua) + bytes(6)
        # The special song-pilot branch retains its original labels.
        assert new[0x7108A0:0x7108B0] == orig[0x7108A0:0x7108B0]
        for off, jp, en in MOVEMENT_EXCLUSIVE:
            size = len(jp.encode('cp932'))
            assert orig[off:off + size + 1] == jp.encode('cp932') + NUL
            assert new[off:off + size + 1] == dg._raw_bytes(en) + NUL
        for base in MOVEMENT_TYPE_TABLES:
            for i, (jp, pua) in enumerate(MOVEMENT_TYPE_CHARS):
                off = base + i * 8
                assert orig[off:off + 8] == jp.encode('cp932') + bytes(6)
                assert new[off:off + 8] == struct.pack('>H', dg.TINY_CELLS[pua][1]) + bytes(6)
    inv = {v: k for k, v in mapping.items()}
    segs = _segments(new)
    osegs = _segments(orig)
    arrays = find_arrays(orig, osegs)     # entry 0 is repointed in `new`; same offsets
    checked = 0
    for base in arrays:
        for i in range(_count(arrays, base)):
            va = struct.unpack(">I", new[base + 4 * i:base + 4 * i + 4])[0]
            ova = struct.unpack(">I", orig[base + 4 * i:base + 4 * i + 4])[0]
            if not va:
                assert not ova
                continue
            jp = _cstr(orig, _off(osegs, ova)).decode("cp932")
            raw = _cstr(new, _off(segs, va))
            if va == ova:
                assert raw.decode("cp932") == jp and not names.get(jp)
                continue
            dec = ""
            for k in range(0, len(raw), 2):
                code = (raw[k] << 8) | raw[k + 1]
                dec += "".join(inv[code]) if code in inv else raw[k:k + 2].decode("cp932")
            want = names[jp]
            # padded_runs may add a half-cell of slack; compare without spaces
            assert dec.replace(" ", "") == want.replace(" ", ""), (jp, want, dec)
            checked += 1
    # nothing else changed
    edited = set()
    if vwf:
        for site, original, _, _, _, cave in runtime_names.READERS:
            off = _off(osegs, site)
            assert orig[off:off+8] == struct.pack('>II', original, 0x4e800020)
            edited.update(range(off, off+4))
    h = segs[0]["hdr"]
    edited.update(range(h + 32, h + 48))
    for base in arrays:
        edited.update(range(base, base + 4 * _count(arrays, base)))
    gap_lo = osegs[0]["off"] + osegs[0]["filesz"]
    edited.update(range(gap_lo, osegs[1]["off"]))
    if NAME_ENABLE:
        hs = NAME_SITE - osegs[0]["va"]
        edited.update(range(hs, hs + 4))
        w = struct.unpack_from(">I", new, hs)[0]
        assert w & 0xFC000003 == 0x48000000 and NAME_SITE + (w & 0x03fffffc) == NAME_STUB
        ss = NAME_STUB - osegs[0]["va"]
        assert new[ss:ss + len(name_stub())] == name_stub()
    if COMMAND_ENABLE and COMMAND_FACE == "vwf":
        try:
            t = unicode_table(orig, osegs)
            edited.update(range(t + 0x100 * 2, t + 0x200 * 2))   # U+0100..U+01FF: letters and pads
            import command_layout
            for cp, code in zip(command_layout.CODEPOINTS, command_layout.CODES):
                pos = t + cp * 2
                assert orig[pos:pos+2] == b'\x81\xa1', ('pad cell already mapped', hex(cp))
                assert new[pos:pos+2] == struct.pack('>H', code), ('pad mapping differs', hex(cp))
                edited.update(range(pos, pos+2))
        except SystemExit:
            pass
    if vwf:
        edited.update(range(*vwf["site"]))
        for lo_, hi_ in vwf["kw"]:
            edited.update(range(lo_, hi_))
        # the stub must round-trip and the bl must land on it
        assert new[vwf["stub"][0]:vwf["stub"][1]] == vwf_stub()
        bl = struct.unpack(">I", new[vwf["site"][0]:vwf["site"][1]])[0]
        assert bl & 0xFC000003 == 0x48000001 and (PATCH_SITE + ((bl & 0x03fffffc) ^ 0) ) & 0xffffffff == STUB_VA
    # the EXT segment: the file grew by exactly its (aligned) region, the
    # rewritten placeholder header is the only header change beyond seg 0's
    ext = [s for s in segs if s["va"] == EXT_VA]
    assert len(ext) == 1 and ext[0]["filesz"] == EXT_SIZE, "EXT segment missing"
    assert len(new) == ext[0]["off"] + EXT_SIZE, "file tail is not the EXT segment"
    assert ext[0]["off"] >= len(orig) and not any(new[len(orig):ext[0]["off"]]), "EXT overlaps the original file"
    edited.update(range(ext[0]["hdr"], ext[0]["hdr"] + 56))
    ext_lo, ext_hi = EXT_VA, EXT_VA + EXT_SIZE
    new = new[:len(orig)]
    osegs2 = _segments(orig)
    rod_lo = osegs2[0]["off"]; rod_hi = osegs2[0]["off"] + osegs2[0]["filesz"]
    gaplo = osegs2[0]["off"] + osegs2[0]["filesz"]; gaphi = osegs2[1]["off"]
    for i in range(len(orig)):
        if orig[i] == new[i] or i in edited:
            continue
        if gaplo <= i < gaphi:
            continue                      # gap: strings + loose English
        if rod_lo <= i < rod_hi:
            continue                      # rodata: in-place name translation
        # a repointed data pointer: 4-byte word now aligned pointer into the gap
        w = i & ~3
        nv = struct.unpack_from(">I", new, w)[0]
        if gaplo + osegs2[0]["va"] <= nv < gaphi + osegs2[0]["va"] or ext_lo <= nv < ext_hi:
            continue
        assert False, "unexpected byte change at %#x" % i
    return checked
    return checked


def load_mapping(path):
    return {(k[0], k[1]): v for k, v in json.load(open(path, encoding="utf-8")).items()}


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 5:
        print(__doc__.strip())
        return 2
    elf, glossary, pairs_lib, out = argv[1:5]
    orig = open(elf, "rb").read()
    gl = json.load(open(glossary, encoding="utf-8"))
    names = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
    mapping = load_mapping(pairs_lib)
    used = set(mapping.values())
    if "--pairs" in argv:
        used |= set(load_mapping(argv[argv.index("--pairs") + 1]).values())
    widths = None
    if "--widths" in argv:
        widths = {int(k): v for k, v in json.load(open(argv[argv.index("--widths") + 1])).items()}
    if "--vwf-test" in argv:
        # every current pair cell gets width N: a visible, throwaway experiment
        import digraph as dg
        n_ = int(argv[argv.index("--vwf-test") + 1])
        widths = {dg.cell_index(code): n_ for code in used}
    new, rep = patch(orig, names, mapping, used, widths)
    n = verify(orig, new, names, mapping, rep["vwf"])
    if rep["vwf"]:
        print("VWF:   stub @%#x, table @%#x, bl @%#x; %d cells narrowed" % (STUB_VA, TABLE_VA, PATCH_SITE, rep["vwf"]["narrowed"]))
    if rep.get("loose"):
        rp, ds, _ = rep["loose"]
        print("       loose names: %d data pointers repointed to %d English strings" % (rp, ds))
        print("       keyword layout: %d sites -> pen accumulator @%#x (segment 1 memsz +%#x)" % (len(KW_SITES) + 1, PEN_ACC, BSS_GROW))
    if rep.get("commands"):
        c_in, c_rp, c_stay = rep["commands"][:3]
        print("       COMMAND menu: %d labels in place, %d repointed, face %s%s"
              % (c_in, c_rp, "VWF cells" if rep["commands"][4] else "ASCII",
                 "" if not c_stay else
                 "; still Japanese: " + ", ".join("%s (%s)" % x for x in c_stay)))
    open(out, "wb").write(new)
    print("EBOOT: %d series names -> English, %d table entries repointed, %d read back OK"
          % (rep["translated"], rep["repointed"], n))
    print("       gap %d/%d B used at VA %s; arrays at %s"
          % (rep["gap_used"], rep["gap"], rep["mapped_va"], ", ".join(rep["arrays"])))
    if rep["stayed"]:
        print("       still Japanese (no glossary English): %s" % ", ".join(rep["stayed"]))
    print("       %s  %d B" % (out, len(new)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
