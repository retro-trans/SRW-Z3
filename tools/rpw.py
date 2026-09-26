"""Read and write RPW_DATA.CPK -- the game's core string/data table.

An `<mt>prod` container of 24 tagged chunks. The 登場作品 series label, unit
names, weapon names, spirit commands, skill text and battle quotes all come
from here (chunk `j-string`: 4,565 NUL-separated cp932 strings). The zukan
library's PRDC field is NOT what the game draws for that label -- found when
a translated PRDC still showed Japanese on screen.

Chunk layout, verified on all 24 chunks:

    <chunk-head>  name padded to 8 bytes  u32 total  u32 body
    body          (j-string: strings joined by NUL)
    <chunk-foot>  u32  <endofchunk>

    total = bytes from '<chunk-head>' through the end of '<endofchunk>'
    body  = bytes between the header and '<chunk-foot>'

A short name (pilot, robot, skill) is padded -- reading the u32s straight
after the name gives garbage, which is what made those chunks look corrupt.

File header `<mt>prod#1 .. data#1 .. 1.00` then u32 file-total, u32 file-body;
both are recomputed when a chunk changes length.
"""
import struct
import sys

HEAD = b"<chunk-head>"
FOOT = b"<chunk-foot>"
EOC = b"<endofchunk>"


def chunks(b):
    """[(name, start, body_off, body_end, chunk_end)] in file order."""
    out = []
    p = 0
    while True:
        s = b.find(HEAD, p)
        if s < 0:
            break
        name = b[s + len(HEAD):s + len(HEAD) + 8].split(b"\0")[0].decode()
        o = s + len(HEAD) + 8 + 8
        foot = b.find(FOOT, o)
        end = b.find(EOC, foot) + len(EOC)
        out.append((name, s, o, foot, end))
        p = end
    return out


def jstrings(b):
    for name, s, o, foot, end in chunks(b):
        if name == "j-string":
            return [x.decode("cp932") for x in b[o:foot].split(b"\0")]
    raise ValueError("no j-string chunk")


def _file_sizes(b):
    """(offset of the two file-level u32s, total, body) from the <mt> header."""
    o = b.find(b"1.00") + 4
    return o, struct.unpack_from("<II", b, o)


def build(b, new_strings):
    """Replace j-strings IN PLACE. Every string keeps its original byte offset
    and slot length; a replacement is written at that offset and NUL-padded
    to the slot. A replacement longer than its slot is refused and the
    original kept.

    Why in place: the 23 binary chunks (pilot, robot, weapon...) hold tens of
    thousands of u32 byte offsets INTO the j-string body (18,279 in `weapon`
    alone). A length-changing rewrite moved every string after the first
    edit and turned all of those into pointers past the end of a string --
    an access violation at 0x35000030 in the game. Preserving offsets makes
    that class of failure structurally impossible; the file never changes
    length, so no size field changes either.

    Returns (bytes, kept) where `kept` lists indices left as the original
    because the replacement did not fit."""
    for name, s, o, foot, end in chunks(b):
        if name != "j-string":
            continue
        body = bytearray(b[o:foot])
        orig = b[o:foot].split(b"\0")
        starts = []
        p = 0
        for x in orig:
            starts.append(p)
            p += len(x) + 1
        if len(new_strings) != len(orig):
            raise ValueError("expected %d strings, got %d" % (len(orig), len(new_strings)))
        kept = []
        for i, (x, st) in enumerate(zip(new_strings, starts)):
            nb = x if isinstance(x, bytes) else x.encode("cp932")
            slot = len(orig[i])
            if len(nb) > slot:
                kept.append(i)
                continue
            body[st:st + slot] = nb + b"\0" * (slot - len(nb))
        return bytes(b[:o]) + bytes(body) + bytes(b[foot:]), kept
    raise ValueError("no j-string chunk")


def _starts(b):
    """Body offset of every j-string, and the body length."""
    js = next(c for c in chunks(b) if c[0] == 'j-string')
    _, _s0, o, foot, _ = js
    out, p = [], 0
    for x in b[o:foot].split(bytes((0,))):
        out.append(p)
        p += len(x) + 1
    return out, foot - o


MIN_RECORDS = 8            # below this a 'column' is coincidence, not structure
COL_HIT = 0.98             # a real pointer column is ~entirely string starts


def pointer_columns(b):
    """Which words of each chunk actually hold j-string offsets.

    The binary chunks are record arrays. Repointing by scanning every byte
    position for a matching little-endian u32 rewrites coincidences too --
    it corrupted `ridividx` and `ridwpidx`, which are robot INDEX tables and
    hold no offsets at all, and one robot record then failed to construct.
    The registry it belongs to is searched linearly with no null check, so
    the game dereferenced the hole and died reading address 0x10.

    So derive the structure instead: for each chunk find the smallest record
    stride that divides it and, at that stride, the word columns in which
    (almost) every value is a real string start. Only those get repointed.
    Returns {chunk: (stride_in_words, (column, ...))}.
    """
    starts, _body = _starts(b)
    sset = set(starts)
    out = {}
    for name, cs, co, cf, ce in chunks(b):
        if name == 'j-string':
            continue
        n = (cf - co) // 4
        ws = [struct.unpack_from('<I', b, w)[0] for w in range(co, cf - 3, 4)]
        found = ()
        stride = None
        for d in range(1, 65):
            if n % d or n // d < MIN_RECORDS:
                continue
            cols = tuple(phi for phi in range(d)
                         if sum(1 for v in ws[phi::d] if v in sset) >= COL_HIT * len(ws[phi::d]))
            if cols:
                stride, found = d, cols
                break
        out[name] = (stride, found)
    return out

# boost-p strings must not exceed their column's largest ORIGINAL byte length --
# fixed per-column slots; longer overwrites neighbours (bisected in-game 2026-09-04)
FILL = b"\x81\x40"                  # fullwidth space; never a NUL


def slots(b):
    """Every pointer slot of every record array, as
    {(chunk, record, column): j-string index}.

    The j-string table is DEDUPLICATED -- `レイ` is stored once and 21 slots
    point at it -- so a name shared by two people is not one string the game
    forces on both. Each slot is repointable on its own, which is what makes
    `Amuro Ray`, `Ray Lovelock` and `Rei Ayanami` separable even though all
    three spell their レイ with the same bytes."""
    st, _body = _starts(b)
    at = {off: i for i, off in enumerate(st)}
    cols = pointer_columns(b)
    out = {}
    for name, cs, co, cf, ce in chunks(b):
        stride, phis = cols.get(name, (None, ()))
        if not phis:
            continue
        for rec in range(((cf - co) // 4) // stride):
            for phi in phis:
                w = co + 4 * (rec * stride + phi)
                if w + 4 > cf:
                    continue
                i = at.get(struct.unpack_from('<I', b, w)[0])
                if i is not None:
                    out[(name, rec, phi)] = i
    return out


DISPLAY = ("pilot-nw",)      # the record array the index and battle screens draw


def name_overrides(b, terms):
    """Which name slots mean something other than their string's default.

    A `pilot-nw` record is (w0 given name, w1 surname, w2 display name), and
    the j-string table is deduplicated, so one `レイ` serves Amuro Ray's
    SURNAME, Ray Lovelock's given name and Rei Ayanami's given name alike.
    Swapping the string once gets two of the three wrong.

    The (given, surname) pair names the character, so look that up, then take
    the short-name term pinned to the same zukan entry. Failing that, split
    the character's full English -- two Japanese components, two English
    words, given first and surname last.

    A slot that cannot be resolved is only an error if its candidates
    actually disagree; 12 of the 14 ambiguous names here render the same
    either way (both 宇宙魔王 are 'Space Demon King'), so demanding an answer
    for those would be noise.

    Returns {(chunk, record, column): english}.
    """
    js = jstrings(b)
    sl = slots(b)
    by_jp = {}
    for t in terms:
        if t.get("en"):
            by_jp.setdefault(t["jp"], []).append(t)
    comp = {}
    for (chunk, rec, col), i in sl.items():
        if chunk in DISPLAY:
            comp.setdefault(rec, {})[col] = js[i]
    out, stuck = {}, []
    for (chunk, rec, col), i in sorted(sl.items()):
        if chunk not in DISPLAY:
            continue
        jp = js[i]
        cands = by_jp.get(jp, [])
        if len(cands) < 2:
            continue                       # unambiguous: the plain swap is right
        parts = comp.get(rec, {})
        w0, w1 = parts.get(0, ""), parts.get(1, "")
        who = None
        for full in (w1 + w0, w0 + "\u30fb" + w1, w0 + w1):
            if by_jp.get(full):
                who = by_jp[full][0]
                break
        en = None
        if who is not None:
            pin = [t for t in cands if t.get("zukan_id") == who.get("zukan_id")]
            if len(pin) == 1:
                en = pin[0]["en"]
            else:
                words = who["en"].split()
                if len(words) == 2 and col in (0, 1):
                    en = words[0] if col == 0 else words[1]
        if en is None:
            if len({t["en"] for t in cands}) > 1:
                stuck.append((rec, col, jp, sorted({t["en"] for t in cands})))
            continue
        if en != cands[-1]["en"]:
            out[(chunk, rec, col)] = en
    if stuck:
        raise SystemExit("cannot tell which term these RPW name "
                         "slots mean, and the candidates differ: %r" % stuck[:8])
    return out

def piece_overrides(b, terms):
    """English for BOTH name slots of every `pilot-nw` record that resolves
    to a glossary character.

    The status screens draw w1 (surname) then w0 (given name) as separate
    strings, and a whole-name glossary term never matches a piece; a plain
    content swap of pieces cannot tell Rei Ayanami's レイ from Amuro Ray's.
    So resolve the record: (w1+w0) Japanese-style or (w0・w1) Western-style
    is a glossary term -> split its English, given first, surname last. A
    Japanese-style name is drawn with no separator, so its surname carries a
    trailing space ("Sagara " + "Sousuke"). Unresolved records are skipped;
    name_overrides() and the piece fallback map still apply to them.

    Returns ({(chunk, record, column): english}, unresolved_count)."""
    js = jstrings(b)
    sl = slots(b)
    by_jp = {}
    for t in terms:
        if t.get("en") and (t.get("kind") or t.get("type")) == "pilot":
            by_jp.setdefault(t["jp"], []).append(t)
    comp = {}
    for (chunk, rec, col), i in sl.items():
        if chunk in DISPLAY:
            comp.setdefault(rec, {})[col] = js[i]
    out, unresolved = {}, 0
    for rec, cols in sorted(comp.items()):
        w0, w1 = cols.get(0, ""), cols.get(1, "")
        if not w0 or not w1 or w0.startswith("－") or w1.startswith("－") or w0 == "-" or w1 == "-":
            continue                              # mononym or placeholder: the plain swap covers it
        who, style = None, None
        for full, st in ((w1 + w0, "jp"), (w0 + "・" + w1, "west"), (w0 + w1, "jp")):
            if by_jp.get(full):
                who, style = by_jp[full][0], st
                break
        if who is None:
            unresolved += 1
            continue
        toks = who["en"].split(" ")
        if len(toks) < 2:
            unresolved += 1
            continue
        if style == "west":
            given, sur = " ".join(toks[:-1]), toks[-1]
        else:
            given, sur = toks[0], " ".join(toks[1:]) + " "
        out[("pilot-nw", rec, 0)] = given
        out[("pilot-nw", rec, 1)] = sur
    return out, unresolved

def compound_name_overrides(b, terms):
    """Resolve long status names composed from display-prefix + surname.

    The third pilot-nw field is not always a short nickname. For example,
    Asuka's status name joins 式波・アスカ and ラングレー. Translating
    those independently produced Asuka Shikinami / Shikinami. Resolve the
    full source first and split its canonical English at the LAST space.
    The short battle-name field (column zero) is deliberately untouched.
    """
    js = jstrings(b)
    records = {}
    for (chunk, rec, col), index in slots(b).items():
        if chunk == 'pilot-nw':
            records.setdefault(rec, {})[col] = js[index]
    full_names = {}
    for term in terms:
        if term.get('kind') == 'pilot' and term.get('en'):
            full_names.setdefault(term['jp'], set()).add(term['en'])
    out = {}
    for rec, cols in records.items():
        prefix, surname = cols.get(2, ''), cols.get(1, '')
        if '・' not in prefix:
            continue
        candidates = full_names.get(prefix + '・' + surname)
        if not candidates:
            continue
        if len(candidates) != 1:
            raise ValueError('Ambiguous compound pilot name: ' + prefix)
        english = next(iter(candidates))
        if ' ' not in english:
            raise ValueError('Compound pilot name has no surname: ' + english)
        given, family = english.rsplit(' ', 1)
        out[('pilot-nw', rec, 2)] = given
        out[('pilot-nw', rec, 1)] = family
    return out


def spirit_name_overrides(b, names):
    """Spirit full-name slots take their own terms, even when a weapon shares
    the Japanese string (e.g. 突撃: Assail spirit versus Charge weapon).
    Abbreviations, effect text, costs and other record fields are untouched.
    """
    js = jstrings(b)
    return {key: names[js[index]] for key, index in slots(b).items()
            if key[0] == 'spirit' and key[2] == 1 and js[index] in names}


def check_compound_names(original, patched, terms, mapping):
    import digraph
    expected = compound_name_overrides(original, terms)
    assert expected, 'Compound pilot-name inventory unexpectedly empty'
    _, _, start, end, _ = next(c for c in chunks(patched) if c[0] == 'j-string')
    strings = patched[start:end].split(b'\0')
    new_slots = slots(patched)
    for slot, en in expected.items():
        assert strings[new_slots[slot]] == digraph.encode_mixed(en, mapping), (slot, en)
    print('PASS: %d compound pilot status names match canonical full names.' % (len(expected)//2))


def build_grown(b, swap, overrides=None):
    """Swap j-strings to English, fitting in place where possible and
    APPENDING where not. Appending never moves an existing string, so every
    offset the 23 binary chunks hold stays valid; only the too-long names get
    a new home at the end of the body, and their `pilot-nw` (etc.) pointers
    are repointed there. The j-string chunk and the file grow accordingly.

    `swap` = {index: english_text|bytes}, one English per j-string.

    `overrides` = {(chunk, record, column): english_bytes} for the slots that
    must NOT take their string's default -- a name two people share. Each
    gets its own appended copy and only its own pointer is rewritten, so the
    string every other slot sees is untouched. Applied after the normal
    repoint, so an override always wins.

    Returns (bytes, appended count)."""
    ch = chunks(b)
    js = next(c for c in ch if c[0] == "j-string")
    _, s0, o, foot, _ = js
    orig = b[o:foot].split(b"\0")
    starts = []
    p = 0
    for x in orig:
        starts.append(p)
        p += len(x) + 1
    body = bytearray(b[o:foot])
    append = bytearray()
    repoint = {}                      # old body offset -> new body offset
    appended = 0
    for i, en in swap.items():
        nb = en if isinstance(en, bytes) else en.encode("cp932")
        slot = len(orig[i])
        pad = slot - len(nb)
        # The slack MUST NOT be NUL. The body is a NUL-SEPARATED list and the
        # game indexes it by ordinal as well as by byte offset, so padding a
        # shortened name with NULs inserts phantom empty strings and shifts
        # every later ordinal (1,592 of them in the first English build).
        # One record then failed to construct, leaving a hole in a registry
        # whose lookup has no null check -- the game read address 0x10 and
        # died. 0x8140 (fullwidth space) is the filler: 339 shipped
        # j-strings already contain it, so it is drawable and stays
        # reserved. An odd amount of slack cannot be filled with it, so
        # those names are appended instead.
        if pad >= 0 and pad % 2 == 0:
            body[starts[i]:starts[i] + slot] = nb + FILL * (pad // 2)
        else:
            new_off = len(body) + len(append)
            append += nb + b"\0"
            repoint[starts[i]] = new_off
            appended += 1
    # one appended copy per distinct override text; only that slot moves
    ov_at, ov_where = {}, {}
    for key, enc in (overrides or {}).items():
        if enc not in ov_where:
            ov_where[enc] = len(body) + len(append)
            append += enc + b"\0"
        ov_at[key] = ov_where[enc]
    body += append
    grow = len(append)
    out = bytearray(b[:o]) + body + bytearray(b[foot:])
    # repoint LE u32 pointers in every binary chunk (offsets are body-relative,
    # stored little-endian). Chunk file positions shift by `grow`; recompute
    # each chunk position in `out`.
    cols = pointer_columns(b)          # structure of the ORIGINAL file
    moved = 0
    for name, cs, co, cf, ce in chunks(out):
        stride, phis = cols.get(name, (None, ()))
        if not phis:
            continue                    # not a record array of j-string offsets
        for base in range(0, (cf - co) // 4, stride):
            for phi in phis:
                w = co + 4 * (base + phi)
                if w + 4 > cf:
                    continue
                v = struct.unpack_from("<I", out, w)[0]
                # v == 0 is ambiguous: the offset of the first string, but
                # also how these arrays spell NULL / no-value. Repointing the
                # zeros (when string 0, "-", moved) rewrote 1,400 semantic
                # NULLs to a six-digit offset; whatever reads such a word as
                # a NUMBER then explodes -- seen in-game as a stage-1 mob
                # one-shotting the Genion for 108,012 damage. Leave 0 alone.
                if v and v in repoint:
                    struct.pack_into("<I", out, w, repoint[v])
                    moved += 1
    if ov_at:
        pos = {c[0]: (c[2], c[3]) for c in chunks(out)}
        for (name, rec, phi), noff in ov_at.items():
            stride = cols.get(name, (None, ()))[0]
            co, cf = pos[name]
            w = co + 4 * (rec * stride + phi)
            if w + 4 > cf:
                raise SystemExit("override slot %s out of range" % ((name, rec, phi),))
            struct.pack_into("<I", out, w, noff)
    # grow the j-string chunk size fields (total at s0+20, body at s0+24)
    total = struct.unpack_from("<I", out, s0 + 20)[0]
    bodylen = struct.unpack_from("<I", out, s0 + 24)[0]
    struct.pack_into("<I", out, s0 + 20, total + grow)
    struct.pack_into("<I", out, s0 + 24, bodylen + grow)
    # grow the file-level total/body
    fo, (ftot, fbody) = _file_sizes(bytes(out))
    struct.pack_into("<II", out, fo, ftot + grow, fbody + grow)
    # The game reads this list by ordinal as well as by offset, so every
    # original string must still be the Nth. Appended ones land after them.
    kept = bytes(body[:len(body) - grow]).split(bytes((0,)))
    if len(kept) != len(orig):
        raise SystemExit("j-string ordinals shifted: %d -> %d"                         % (len(orig), len(kept)))
    return bytes(out), appended


def plan(js, names, encoded_len):
    """Decide which j-strings can be swapped IN PLACE, before any cell is allocated.

    A name is swapped only if its English encoding fits the slot the Japanese
    occupied; a longer one stays Japanese, and its kanji must then stay
    reserved -- which is why this runs before the pool is built. Returns
    ({index: english_text}, [refused indices]).
    """
    swap, refused = {}, []
    for i, sj in enumerate(js):
        bare = sj.strip("「」")
        if bare not in names:
            continue
        en = names[bare]
        en = ("「%s」" % en) if sj.startswith("「") else en
        try:
            n = encoded_len(en)
        except SystemExit:          # undrawable character -> not swappable
            refused.append(i)
            continue
        if n > len(sj.encode("cp932")):
            refused.append(i)
        else:
            swap[i] = en
    return swap, refused

def plan_all(js, names):
    """Every j-string that is a settled glossary name -> its English. No fit
    check: build_grown appends whatever does not fit in place."""
    swap = {}
    for i, sj in enumerate(js):
        bare = sj.strip("「」")
        if bare in names:
            en = names[bare]
            swap[i] = ("「%s」" % en) if sj.startswith("「") else en
    return swap



if __name__ == "__main__":
    sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
    from cpk import CPK
    k = CPK(sys.argv[1]); b = k.read(k.files[0])
    for c in chunks(b):
        print("%-10s start 0x%06x body %7d" % (c[0], c[1], c[3] - c[2]))
