"""Two Latin letters per atlas cell, so English stops reading as spaced-out.

The problem, measured in-game and not inferred: the renderer advances a fixed
**42.5 atlas texels** per character while blitting a **32 texel** cell, and the
advance is the same whatever the glyph's ink (proved by a least-squares fit
over real dialogue: pitch is constant to 1.4px rms across glyphs whose ink runs
9-30 texels). There is no per-glyph metric anywhere to patch, and the constant
is computed at runtime, not stored -- see docs/FONT_HUNT.md.

So the only lever left is what a cell *contains*. Put TWO letters in each cell
and every letter costs half an advance: 23.2 screen px instead of 46.4, which
doubles the line budget from ~29 characters to ~58 and removes the gap after
every letter.

Spacing: for an even rhythm the two letters must sit HALF AN ADVANCE apart,
not half a cell -- 21.25 texels, not 16. Centre them at 5.375 and 26.625 and
the inter-cell gap matches the intra-cell gap exactly.

Codes come from SJIS that English never needs -- Greek, Cyrillic, box drawing,
and unassigned-but-valid positions -- so no kanji is harmed. Both atlas pages
are patched, because page 1 and page 3 are two style layers of the same grid.

    python tools/digraph.py plan   <text-file>
    python tools/digraph.py build  <text-file> <TPACK.CPK> <out.CPK> [--preview p.png]
    python tools/digraph.py encode <text-file>
"""
import json
import math
import os
import struct
import sys
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK                      # noqa: E402
from makefont import GLYPHS              # noqa: E402  (original letterforms)
import diacritics as dia                 # noqa: E402
import cpkpatch                          # noqa: E402

CELL = 32
CELLS_PER_ROW = 128
CELLS_PER_LEAD = 192
ATLAS_CELLS = 4480
ATLAS_FORMAT = 0xAB

# Measured in-game: advance 46.412 screen px, cell 34.96 screen px.
ADVANCE_TEXELS = 46.412 / (34.96 / 32.0)      # 42.49
HALF = ADVANCE_TEXELS / 2.0                   # 21.24 -- perfectly even rhythm

# Both letters must sit inside the 32-texel cell while standing HALF apart,
# which caps a letter at 32 - HALF = 10.7 texels. Stepping very slightly under
# HALF buys width for the letterforms; the residual rhythm error (9.2 vs 10.5
# texels) is under half a screen pixel and invisible.
LETTER_STEP = 20.6
INK_HALF = 5.7                                # letter width 11.4 texels

# vertical metrics inside the 32px cell
CAP, BASE, XH_T, DESC_T = 6.0, 26.0, 0.42, 1.22
PEN = 3.0


def cell_index(code):
    hi, lo = code >> 8, code & 0xFF
    idx = (hi - 0x81) * CELLS_PER_LEAD + (lo - 0x40)
    if not 0 <= idx < ATLAS_CELLS:
        raise ValueError("code 0x%04X -> cell %d, outside the atlas" % (code, idx))
    return idx


def valid_sjis(code):
    hi, lo = code >> 8, code & 0xFF
    return 0x81 <= hi <= 0x9F and 0x40 <= lo <= 0xFC and lo != 0x7F


def _segments(shapes, cx):
    """Letter outline -> segments, centred on texel `cx`."""
    segs = []
    for _kind, pts in shapes:
        for i in range(len(pts) - 1):
            (ax, ay), (bx, by) = pts[i], pts[i + 1]
            segs.append((cx + (ax - 0.5) * 2 * INK_HALF, CAP + ay * (BASE - CAP),
                         cx + (bx - 0.5) * 2 * INK_HALF, CAP + by * (BASE - CAP)))
    return segs


def _dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    d2 = dx * dx + dy * dy
    t = 0.0 if d2 == 0 else max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / d2))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))


def set_metrics(cap, base):
    """Scripts that stack diacritics need a shorter cap height to make room.
    Vietnamese uses (11, 25); plain Latin keeps the taller default."""
    global CAP, BASE
    CAP, BASE = cap, base


def glyph_segments(ch, cx):
    """Segments for one character, composing marks when it carries any."""
    if ch in GLYPHS:
        return _segments(GLYPHS[ch], cx)
    if dia.is_supported(ch, GLYPHS):
        return dia.compose_segments(ch, cx, INK_HALF, CAP, BASE,
                                    lambda b, x: _segments(GLYPHS[b], x))
    return []


# The LIBRARY panel draws the same 32-texel cell 1.29x larger but advances it
# the same ~45 px, so a pair placed for dialogue (step 20.6, ink 11.4) fills
# the whole advance and butts into the next pair. Measured from a calibration
# entry of isolated glyphs: 1.412 px/texel vs dialogue's 1.092. For the same
# on-screen letter spacing the library pair must be drawn tighter.
LIBRARY_GEOMETRY = (16.4, 4.4)      # (letter step, ink half-width) in texels


# Optional TrueType faces (tools/ttfglyph.py), keyed by geometry: the dialogue
# default and LIBRARY_GEOMETRY. None -> the stroke letterforms in makefont.
TTF_FACES = {}


def use_ttf(path, cap=20.0, cap_lib=15.0, embolden=0.0, dilate=0.0, dilate_lib=None, ref="H"):
    """Rasterise cells from a TTF. Cap heights are in texels; the library
    cell is drawn 1.29x larger on screen, so it takes a shorter letter.
    `dilate` widens vertical stems before condensing (texels)."""
    import ttfglyph
    TTF_FACES["dialogue"] = ttfglyph.Face(path, cap, BASE, embolden, dilate, ref)
    TTF_FACES["library"] = ttfglyph.Face(path, cap_lib, BASE, embolden,
                                         dilate if dilate_lib is None else dilate_lib, ref)


def _raster_segments(segs, cov=None):
    cov = cov if cov is not None else bytearray(CELL * CELL)
    if not segs:
        return cov
    half = PEN / 2.0
    for y in range(CELL):
        for x in range(CELL):
            px, py = x + 0.5, y + 0.5
            d = min(_dist(px, py, *s) for s in segs)
            v = half + 0.5 - d
            if v > 0:
                i = y * CELL + x
                cov[i] = max(cov[i], 255 if v >= 1 else int(v * 255))
    return cov


def raster_pair(a, b, geometry=None):
    """Draw two letters into one 32x32 coverage cell, half an advance apart.
    `geometry` = (step, ink_half) overrides the dialogue defaults."""
    global INK_HALF
    step, ink_half = geometry if geometry else (LETTER_STEP, INK_HALF)
    face = TTF_FACES.get("library" if geometry == LIBRARY_GEOMETRY else "dialogue")
    saved = INK_HALF
    INK_HALF = ink_half
    left = (CELL - step) / 2.0
    if face is not None:
        # the stroke pen sits outside the centreline box: the real slot is wider
        cov, missing = face.raster_pair(a, b, step, ink_half + PEN / 2.0)
        todo = missing                      # letters the face lacks -> strokes
    else:
        cov, todo = None, [(a, left), (b, left + step)]
    segs = []
    for ch, cx in todo:
        if ch != " ":
            segs += glyph_segments(ch, cx)
    INK_HALF = saved
    return _raster_segments(segs, cov)


# --- variable-width letters (VWF) ------------------------------------------
# With the EBOOT advance patch (tools/eboot.py) every atlas cell carries its
# own width, so Latin can be ONE letter per cell at natural proportions. The
# pair machinery stays for RPW_DATA, whose in-place slots cannot afford two
# bytes per letter.
VWF = False
LINK_PAIRS = False        # True: 《》 lines on pair cells (pre keyword-stub builds)
LETTER_FACE = None
LETTER_LEFT = 1.0                 # texels of left bearing inside the cell
LETTER_SPACE = 9                  # width of the space cell
_LETTER_CACHE = {}


def use_letters(path, cap=22.0, dilate=0.5):
    """Rasterise single letters from a TTF at natural width."""
    global VWF, LETTER_FACE
    import ttfglyph
    VWF = True
    LETTER_FACE = ttfglyph.Face(path, cap, BASE, 0.0, dilate)


def raster_letter(ch):
    """(coverage cell, width in texels) for one letter, left-aligned."""
    if ch in _LETTER_CACHE:
        return _LETTER_CACHE[ch]
    cov = bytearray(CELL * CELL)
    if ch == " ":
        out = (cov, LETTER_SPACE)
    elif LETTER_FACE is not None and LETTER_FACE.has(ch):
        img, lb, top, adv = LETTER_FACE.natural(ch)
        if img is not None:
            LETTER_FACE._blit(cov, img, LETTER_LEFT + lb - 1.0, BASE + top)
        out = (cov, max(1, min(63, int(round(adv + LETTER_LEFT)))))
    elif LETTER_FACE is not None and LETTER_FACE.has_composed(ch):
        adv = LETTER_FACE.natural_vi(ch, cov, LETTER_LEFT, BASE)
        out = (cov, max(1, min(63, int(round(adv + LETTER_LEFT)))))
    else:
        # stroke fallback (composed Vietnamese): centred on its own width
        w = 2 * INK_HALF + PEN + 2
        cov = _raster_segments(glyph_segments(ch, LETTER_LEFT + w / 2.0), cov)
        out = (cov, int(round(w + 1)))
    _LETTER_CACHE[ch] = out
    return out


def letter_width(ch):
    return raster_letter(ch)[1]


# Compact UI labels drawn as a whole word in ONE cell. Terrain kanji and the
# map-data spirit-status flags each occupy fixed one-cell slots, so ordinary
# English would either collide or shift the per-cell highlight. Each label is
# reached through a private-use character, keeps width 32 (the caller's pitch,
# like the kanji it replaces), and lives in an unassigned, empty cp932 slot of
# row 0x86. The short spirit labels use the project's settled full-name terms.
TINY_CELLS = {
    "": ("Air", 0x86B8),
    "": ("Grd", 0x86B9),
    "": ("Wtr", 0x86BA),
    "": ("Spc", 0x86BB),
    "": ("Und", 0x86BC),
    "": ("Va", 0x86BD),        # 熱血 / Valor
    "": ("So", 0x86BE),        # 魂 / Soul
    "": ("Fu", 0x86BF),        # 闘志 / Fury (Akurasu Z3)
    "": ("Al", 0x86C0),        # 閃き / Alert
    "": ("Wa", 0x86C1),        # 不屈 / Wall (Akurasu; was Persist)
    "": ("Gu", 0x86C2),        # 鉄壁 / Guard (Akurasu; was Wall)
    "": ("Fo", 0x86C3),        # 集中 / Focus
    "": ("St", 0x86C4),        # 必中 / Strike
    "": ("Ac", 0x86C5),        # 加速 / Accel
    "": ("Ze", 0x86C6),        # 覚醒 / Zeal
    "": ("Me", 0x86C7),        # てかげん / Mercy
    "": ("Sn", 0x86C8),        # 狙撃 / Snipe
    "": ("As", 0x86C9),        # 突撃 / Assail
    "": ("Br", 0x86CA),        # 直撃 / Break (Akurasu Z3)
    "": ("Lu", 0x86CB),        # 幸運 / Luck
    "": ("Ga", 0x86CC),        # 努力 / Gain
    "": ("Di", 0x86CD),        # かく乱 / Disrupt
    "": ("An", 0x86CE),        # 分析 / Analyze (enemy battle-preview strip)
    "": ("Only", 0x86CF),      # restricted movement; same small face as terrain
    "\ue018": ("CQB", 0x86D0),
    "\ue019": ("RNG", 0x86D1),
    "\ue01a": ("SKL", 0x86D2),
    "\ue01b": ("DEF", 0x86D3),
    "\ue01c": ("EVD", 0x86D4),
    "\ue01d": ("HIT", 0x86D5),
    # Invisible tabs for the confirmation row. The VWF stub places the next
    # glyph at column 3/5 using the live original pitch, NOT atlas texel widths.
    "\ue01e": ("", 0x86D6),
    "\ue01f": ("", 0x86D7),
}


TINY_CAP = 11.0                    # cap height in texels
TINY_LIFT = 6.0                    # baseline raised so the word centres on the kanji body
SPIRIT_TINY_CODES = frozenset(range(0x86BD, 0x86CF))
SPIRIT_TINY_CAP = 16.0             # larger than terrain: this strip has room vertically
SPIRIT_TINY_LIFT = 3.0             # baseline 23; mixed-case ink centres in the 32px cell
SPIRIT_TINY_GAP = 2               # clear texels between visible glyph bounds
SPIRIT_TINY_MAX_WIDTH = 28        # ink width including gap; two texels of side padding
_TINY_FACES = {}


def raster_tiny(text, code=None):
    """Coverage cell with `text` drawn small and centred."""
    import ttfglyph
    if LETTER_FACE is None:
        raise SystemExit("tiny cells need --ttf (use_letters) first")
    spirit = code in SPIRIT_TINY_CODES
    cap = SPIRIT_TINY_CAP if spirit else TINY_CAP
    lift = SPIRIT_TINY_LIFT if spirit else TINY_LIFT
    key = (cap, lift)
    if key not in _TINY_FACES:
        _TINY_FACES[key] = ttfglyph.Face(LETTER_FACE.path, cap, BASE - lift, 0.0, 0.3)
    face = _TINY_FACES[key]
    cov = bytearray(CELL * CELL)
    parts = [face.natural(ch) for ch in text]
    if spirit or 0x86CF <= code <= 0x86D5:  # fit Only and training labels at terrain cap 11
        # Font advances include unequal side bearings. Adding tracking to
        # reach a minimum pair width spread Ft/Ef/Cf apart, while squeezing
        # Me made its letters touch. Place cropped ink with a fixed gap;
        # only condense glyph widths when the complete pair exceeds its cell.
        from PIL import Image
        ink = []
        for img, _lb, top, _adv in parts:
            box = img.getbbox() if img is not None else None
            if box:
                ink.append((img.crop(box), BASE - lift + top + box[1]))
        if not ink:
            return cov
        gap = SPIRIT_TINY_GAP if spirit else 1
        gaps = gap * (len(ink) - 1)
        natural_width = sum(img.width for img, _y in ink)
        budget = min(natural_width, SPIRIT_TINY_MAX_WIDTH - gaps)
        # Cumulative rounding preserves the exact width budget.
        scaled, total, previous = [], 0, 0
        for img, y in ink:
            total += img.width
            edge = round(total * budget / natural_width)
            width = edge - previous
            previous = edge
            scaled.append((img.resize((width, img.height), Image.Resampling.BOX), y))
        x = (CELL - budget - gaps) // 2
        for img, y in scaled:
            face._blit(cov, img, x, y)
            x += img.width + gap
        return cov
    width = sum(p[3] for p in parts)
    x = (CELL - width) / 2.0
    for i, (img, lb, top, adv) in enumerate(parts):
        if img is not None:
            face._blit(cov, img, x + lb, BASE - lift + top)
        x += adv
    return cov


def _raw_bytes(part):
    """cp932 for Japanese, tiny-cell codes for the private-use characters."""
    out = bytearray()
    for ch in part:
        if ch in TINY_CELLS:
            code = TINY_CELLS[ch][1]
            out += bytes((code >> 8, code & 0xFF))
        else:
            out += ch.encode("cp932")
    return bytes(out)


def mixed_letters(text):
    """Every distinct letter a block of mixed text needs (space included)."""
    seen = []
    for line in text.split(chr(10)):
        for kind, part in split_mixed(line):
            if kind == "ascii":
                for ch in part:
                    if ch not in seen:
                        seen.append(ch)
    return seen


def encode_letters(text, mapping, newline=bytes((13, 10))):
    """Mixed text -> cp932 bytes, one code per Latin letter."""
    out = bytearray()
    for i, line in enumerate(text.split(chr(10))):
        if i:
            out += newline
        for kind, part in split_mixed(line):
            if kind == "raw":
                out += _raw_bytes(part)
            elif kind == "ph":
                out += part.encode("ascii")
            else:
                for ch in part:
                    code = mapping[ch]
                    out += bytes((code >> 8, code & 0xFF))
    return bytes(out)


# Pixel cost per screen, in the 1280x720 space the layout works in: a
# fullwidth cell advances by the caller advance, a letter by W/32 of the
# quad width (that is what the patched stub computes).
SCREENS = {"dialogue": (31.0, 23.3, 963.0), "library": (30.0, 30.0, 1140.0)}


def line_px(line, screen="library"):
    adv, quad, _ = SCREENS[screen]
    px = 0.0
    for kind, part in split_mixed(line):
        if kind == "raw":
            px += adv
        elif kind == "ph":
            px += 8 * 16 * quad / 32.0          # a name; budget eight letters
        else:
            px += sum(letter_width(ch) for ch in part) * quad / 32.0
    return px


def wrap_px(text, screen="library", budget=None):
    """Word-wrap each line of text to the pixel budget of the screen."""
    adv, quad, full = SCREENS[screen]
    budget = full if budget is None else budget
    out = []
    for para in text.split(chr(10)):
        line = ""
        for word in para.split(" "):
            cand = word if not line else line + " " + word
            if not line or line_px(cand, screen) <= budget:
                line = cand
            else:
                out.append(line)
                line = word
        out.append(line)
    return chr(10).join(out)


def pairs_needed(text):
    """Pairs for a string that must stay on the pair cells (RPW), whatever
    the mode."""
    seen = []
    for line in text.split(chr(10)):
        for kind, part in padded_runs(line):
            if kind == "ascii":
                for p in pairs_of(part):
                    if p not in seen:
                        seen.append(p)
    return seen


def pairs_of(text):
    """Split a line into 2-character groups; a lone tail pairs with a space.

    An odd-length run that already ends in a space loses it. Otherwise the
    tail pairs with a pad space and the line renders TWO spaces, which shows
    up as a visible gap before a following 「 or 《.
    """
    out = []
    for line in text.split("\n"):
        if len(line) % 2 and line.endswith(" "):
            line = line[:-1]
        i = 0
        while i < len(line):
            a = line[i]
            b = line[i + 1] if i + 1 < len(line) else " "
            out.append((a, b))
            i += 2
    return out


def free_pool(metrics_path, include_kanji=False, reserved=()):
    """SJIS codes English never needs, cheapest first.

    Greek, Cyrillic and box drawing are inked but useless to us; blank cells
    at valid SJIS positions cost nothing at all. Kanji are never touched.
    """
    m = json.load(open(metrics_path))["page_1"]["cells_detail"]
    blank, spare = [], []
    ranges = [(0x839F, 0x83B6), (0x83BF, 0x83D6),      # Greek
              (0x8440, 0x8460), (0x8470, 0x8491),      # Cyrillic
              (0x849F, 0x84BE)]                        # box drawing
    for lo, hi in ranges:
        for c in range(lo, hi + 1):
            if valid_sjis(c):
                spare.append(c)
    for lead in range(0x81, 0x89):                     # symbol/kana leads only
        for trail in range(0x40, 0xFD):
            c = (lead << 8) | trail
            if not valid_sjis(c):
                continue
            try:
                idx = cell_index(c)
            except ValueError:
                continue
            if not m[idx]["blank"]:
                continue
            # A blank cell is only free if the code is UNASSIGNED. 0x8140 is
            # blank too, but it is the ideographic space and very much in use.
            try:
                bytes((c >> 8, c & 0xFF)).decode("cp932")
            except UnicodeDecodeError:
                blank.append(c)                        # unassigned: costs nothing
    # Tiny words are deliberate permanent occupants, not free blank cells.
    # Reserving them here keeps a future larger translation from allocating a
    # normal VWF letter to the same cp932 code and failing late in build_atlas.
    reserved = set(reserved) | {code for _text, code in TINY_CELLS.values()}
    # Live layout prefixes are deliberately blank, never letter allocations.
    import command_layout
    reserved.update(command_layout.CODES)
    if not include_kanji:
        return [c for c in blank + spare if c not in reserved]
    # Kanji cells, last resort. Only for a COMPLETE translation: any Japanese
    # still on screen renders as Latin fragments once these are taken. Leads
    # 0x89-0x97 are JIS level 1; 0x88 is kana plus the first kanji row, so it
    # is left alone.
    kanji = []
    for lead in range(0x89, 0x98):
        for trail in range(0x40, 0xFD):
            c = (lead << 8) | trail
            if not valid_sjis(c):
                continue
            try:
                idx = cell_index(c)
            except ValueError:
                continue
            if not m[idx]["blank"] and c not in reserved:
                kanji.append(c)
    # `reserved`: cp932 codes of every character the game still draws in
    # Japanese -- UI labels (愛称, 声優, 登場作品...), voice-actor names, any
    # untranslated field. Taking one of those cells turns that label into a
    # random Latin pair on screen (愛称 became 愛-v). Callers compute the set
    # from the same files they translate, so it is exact, not a guess.
    return [c for c in blank + spare if c not in reserved] + kanji


def build_map(text, metrics_path):
    want, seen = [], set()
    for p in pairs_of(text):
        if p not in seen:
            seen.add(p)
            want.append(p)
    pool = free_pool(metrics_path)
    if len(want) > len(pool):
        raise SystemExit("need %d cells but only %d are free; reduce the text or "
                         "open up more codes" % (len(want), len(pool)))
    return {p: pool[i] for i, p in enumerate(want)}, len(pool)


def encode(text, mapping):
    out = bytearray()
    for line in text.split("\n"):
        i = 0
        while i < len(line):
            a = line[i]
            b = line[i + 1] if i + 1 < len(line) else " "
            code = mapping[(a, b)]
            out += bytes((code >> 8, code & 0xFF))
            i += 2
        out += newline   # CRLF for the Lua scripts; the library passes bare LF
    return bytes(out[:-2])


def put_cell(buf, w, idx, cov):
    row, col = idx // CELLS_PER_ROW, idx % CELLS_PER_ROW
    x0, y0 = col * CELL, row * CELL
    for y in range(CELL):
        base = 0x80 + ((y0 + y) * w + x0) * 2
        for x in range(CELL):
            n = cov[y * CELL + x] >> 4
            v = (n << 12) | (n << 8) | (n << 4) | n
            i = base + x * 2
            buf[i] = (v >> 8) & 0xFF
            buf[i + 1] = v & 0xFF


def write_png(gray, w, h, path):
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw += gray[y * w:(y + 1) * w]

    def chunk(t, d):
        return (struct.pack(">I", len(d)) + t + d
                + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF))
    open(path, "wb").write(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(bytes(raw), 6)) + chunk(b"IEND", b""))


def simulate(text, mapping, scale=2):
    """Render a line the way the engine does: blit each 32-texel cell, then
    advance 42.5 texels. This is what makes the result checkable offline."""
    lines = text.split("\n")
    ncell = max(len(pairs_of(l)) for l in lines)
    w = int(ncell * ADVANCE_TEXELS + CELL) + 4
    h = len(lines) * (CELL + 6) + 4
    gray = bytearray(w * h)
    for li, line in enumerate(lines):
        y0 = 2 + li * (CELL + 6)
        for ci, (a, b) in enumerate(pairs_of(line)):
            cov = raster_pair(a, b)
            x0 = 2 + int(round(ci * ADVANCE_TEXELS))
            for y in range(CELL):
                for x in range(CELL):
                    v = cov[y * CELL + x]
                    if v:
                        p = (y0 + y) * w + x0 + x
                        if 0 <= p < len(gray):
                            gray[p] = max(gray[p], v)
    if scale > 1:
        W, H = w * scale, h * scale
        big = bytearray(W * H)
        for y in range(H):
            for x in range(W):
                big[y * W + x] = gray[(y // scale) * w + (x // scale)]
        return big, W, H
    return gray, w, h


def simulate_current(text, scale=2):
    """The same line as the game draws it TODAY: one fullwidth letter per
    cell. Kept so the comparison is like-for-like, not a claim."""
    from makefont import raster2
    line = text.split("\n")[0]
    w = int(len(line) * ADVANCE_TEXELS + CELL) + 4
    h = CELL + 6
    gray = bytearray(w * h)
    for ci, ch in enumerate(line):
        if ch not in GLYPHS:
            continue
        cov = raster2(GLYPHS[ch])
        x0 = 2 + int(round(ci * ADVANCE_TEXELS))
        for y in range(CELL):
            for x in range(CELL):
                v = cov[y * CELL + x]
                if v:
                    p = (2 + y) * w + x0 + x
                    if 0 <= p < len(gray):
                        gray[p] = max(gray[p], v)
    if scale > 1:
        W, H = w * scale, h * scale
        big = bytearray(W * H)
        for y in range(H):
            for x in range(W):
                big[y * W + x] = gray[(y // scale) * w + (x // scale)]
        return big, W, H
    return gray, w, h


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    cmd = argv[1]
    text = open(argv[2], encoding="utf-8").read().rstrip("\n")
    here = os.path.dirname(os.path.abspath(__file__))
    metrics = os.path.join(here, "..", "work", "atlas", "metrics.json")
    mapping, pool = build_map(text, metrics)

    if cmd == "plan":
        print("distinct pairs : %d" % len(mapping))
        print("free cells     : %d  (%d spare)" % (pool, pool - len(mapping)))
        adv_game = ADVANCE_TEXELS * (34.96 / 32.0) / 1.5      # 31.0 px at 720p
        area = 963.0                                          # measured text area
        print("chars/line     : %.0f now -> %.0f with pairs"
              % (area / adv_game, 2 * area / adv_game))
        for (a, b), c in list(mapping.items())[:12]:
            print("   %r%r -> 0x%04X  cell %d" % (a, b, c, cell_index(c)))
        return 0

    if cmd == "encode":
        blob = encode(text, mapping)
        print("cp932 bytes: %s" % blob[:40].hex())
        print("as lua string literal, %d bytes for %d chars" % (len(blob), len(text)))
        return 0

    if cmd != "build":
        print("unknown command %r" % cmd)
        return 2

    src, dst = argv[3], argv[4]
    cpk = CPK(src)
    tmp = []
    reps = {}
    for e in cpk.files:
        b = cpk.read(e)
        if len(b) < 0x80 or b[0x18] != ATLAS_FORMAT:
            continue
        buf = bytearray(b)
        w = struct.unpack_from(">H", buf, 0x20)[0]
        for (a, bch), code in mapping.items():
            put_cell(buf, w, cell_index(code), raster_pair(a, bch))
        p = dst + ".m%d" % e["id"]
        open(p, "wb").write(bytes(buf))
        reps[e["id"]] = p
        tmp.append(p)
        print("  patched atlas member id=%d (%d cells)" % (e["id"], len(mapping)))
    if not reps:
        raise SystemExit("no atlas members found in %s" % src)
    n, size = cpkpatch.build(src, dst, reps)
    for p in tmp:
        os.remove(p)
    print("%d members -> %s (%d bytes)" % (n, dst, size))
    json.dump({"%c%c" % k: v for k, v in mapping.items()},
              open(dst + ".map.json", "w"), indent=1)
    print("mapping -> %s.map.json" % dst)

    if "--preview" in argv:
        out = argv[argv.index("--preview") + 1]
        g, w, h = simulate(text, mapping)
        write_png(g, w, h, out)
        print("preview -> %s  (%dx%d)" % (out, w, h))
        g, w, h = simulate_current(text)
        write_png(g, w, h, out.replace(".png", "_before.png"))
        print("before   -> %s" % out.replace(".png", "_before.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))


def proof_map(jp_line, english):
    """Map the cells an on-screen Japanese line already uses to English pairs.

    This proves the whole idea with a single file copy: TPACK is a plain CPK,
    so no Lua edit, no SDAT re-encryption, no make_npdata. The line already on
    screen re-renders as English. It is a throwaway build -- it repurposes
    cells belonging to real characters, so other Japanese text will garble.
    """
    pairs = pairs_of(english)
    if len(pairs) > len(jp_line):
        raise SystemExit("english needs %d cells, the japanese line has %d"
                         % (len(pairs), len(jp_line)))
    mapping, conflict = {}, []
    for ch, pr in zip(jp_line, pairs):
        code = struct.unpack(">H", ch.encode("cp932"))[0]
        if code in mapping and mapping[code] != pr:
            conflict.append((ch, mapping[code], pr))
        mapping[code] = pr
    if conflict:
        for ch, a, b in conflict:
            print("  CONFLICT %r wants %r and %r" % (ch, a, b))
        raise SystemExit("the japanese line repeats a character; pick other text")
    return mapping


def split_mixed(line):
    """Split a line into ASCII runs (to be paired) and passthrough characters.

    Japanese punctuation the script relies on -- the 「」 quotes and the
    fullwidth indent -- already own atlas cells and render correctly at one
    cell each. Only the Latin gets paired, and pairing never crosses a
    passthrough character.
    """
    out, run = [], ""
    i = 0
    while i < len(line):
        ch = line[i]
        # Half-width kana/punctuation encode as single CP932 bytes (A1..DF).
        # They are not valid raw cells in the game's two-byte dialogue stream:
        # an accidental U+FF62 quote shifts every following glyph on the line.
        if 0xff61 <= ord(ch) <= 0xff9f:
            raise SystemExit("unsafe half-width character U+%04X in %r -- use "
                             "full-width punctuation or a supported Latin glyph"
                             % (ord(ch), line[:40]))
        # `$n`, `$l` and friends expand at RUNTIME to the player-named
        # protagonist. They must survive as two literal ASCII bytes -- pairing
        # the letter into a digraph would silently destroy the placeholder.
        if ch == "$" and i + 1 < len(line) and line[i + 1].isalpha():
            if run:
                out.append(("ascii", run))
                run = ""
            out.append(("ph", line[i:i + 2]))
            i += 2
            continue
        if ch == '"':
            ch = "'"          # no double-quote glyph; the style guide asks for '
        if ch == " " or ch in GLYPHS or dia.is_supported(ch, GLYPHS):
            run += ch
        elif ch.isascii() and ch.isprintable():
            # An undrawable ASCII char must NEVER pass through as a raw single
            # byte: inside a 2-byte pair stream it desynchronises every code
            # after it (this is what put a bare 0x22 / 0x3d at 30 line ends).
            raise SystemExit("no glyph for %r in %r -- add it to GLYPHS or "
                             "substitute it" % (ch, line[:40]))
        else:
            if run:
                out.append(("ascii", run))
                run = ""
            out.append(("raw", ch))
        i += 1
    if run:
        out.append(("ascii", run))
    return out


def mixed_pairs(text):
    """Every distinct letter pair a block of mixed text needs (letters in
    VWF mode -- every caller collects units for the same mapping)."""
    if VWF:
        return mixed_letters(text)
    seen = []
    for line in text.split("\n"):
        # padded_runs, not split_mixed: the padding decides the run's final
        # length, and collecting pairs from the unpadded run misses whatever
        # the pad creates at the boundary.
        for kind, part in padded_runs(line):
            if kind == "ascii":
                for p in pairs_of(part):
                    if p not in seen:
                        seen.append(p)
    return seen


def encode_mixed(text, mapping, newline=b"\r\n"):
    """Mixed text -> cp932 bytes, Latin as digraph codes (or one code per
    letter when the mapping is a letter mapping)."""
    if mapping and any(isinstance(k, str) for k in mapping):
        return encode_letters(text, mapping, newline)
    return encode_pairs(text, mapping, newline)


def encode_hybrid(text, mapping, newline=bytes((13, 10))):
    """VWF dialogue: each line with a 《》 link on pair cells (the game places
    the link at codes x advance), every other line on letters."""
    out = []
    for line in text.split(chr(10)):
        enc = encode_pairs if (LINK_PAIRS and "《" in line) else encode_letters
        out.append(enc(line, mapping, newline))
    return newline.join(out)


def hybrid_units(text):
    """Pairs for link lines, letters for the rest -- the cells a VWF dialogue
    block needs."""
    units = []
    for line in text.split(chr(10)):
        for u in (pairs_needed(line) if (LINK_PAIRS and "《" in line) else mixed_letters(line)):
            if u not in units:
                units.append(u)
    return units


def encode_pairs(text, mapping, newline=bytes((13, 10))):
    """Mixed text -> cp932 bytes, Latin as digraph pairs, whatever the mode.
    Dialogue lines with 《》 links must use this even in VWF mode: the game
    positions the pink link text at (codes before it) x advance, a monospace
    assumption that only holds for width-32 pair cells."""
    out = bytearray()
    for i, line in enumerate(text.split("\n")):
        if i:
            out += newline   # CRLF for dialogue; the library passes bare LF
        for kind, part in padded_runs(line):
            if kind == "raw":
                out += part.encode("cp932")
            elif kind == "ph":
                out += part.encode("ascii")      # $n / $l, expanded at runtime
            else:
                for a, b in pairs_of(part):
                    code = mapping[(a, b)]
                    out += bytes((code >> 8, code & 0xFF))
    return bytes(out)


def cell_cost(line):
    """Cells one rendered line consumes.

    Not the character count: 「, 》 and the fullwidth indent each eat a whole
    cell, while Latin costs half a cell per letter. Budget is ~31 cells, from
    the measured 963px text area at 31.0px advance.
    """
    n = 0
    for kind, part in padded_runs(line):
        if kind == "raw":
            n += 1
        elif kind == "ph":
            n += 2          # the expanded name; budget for a short one
        else:
            n += (len(part) + 1) // 2
    return n


LINE_BUDGET = 31


def padded_runs(line):
    """Tokenise a line and decide WHERE each odd run's half-cell of slack goes.

    A cell holds exactly two letters, so an ASCII run of odd length has half a
    cell spare. Where that lands matters:

      * run ends in a space and a fullwidth char follows -> drop the space.
        「 and 《 carry their own side bearing, so the pair would read as two.
      * a fullwidth char precedes -> pad at the FRONT. A space just inside an
        opening 「 or 《 reads naturally; one jammed against a closing 》 does
        not, and padding the end is what produced 《ECS 》.
      * otherwise pad at the end, where a trailing space is invisible.

    Never strips a space before a $-placeholder -- that space separates words
    and dropping it gave "Hold on,$l".
    """
    toks = split_mixed(line)
    out = []
    for i, (kind, part) in enumerate(toks):
        if kind != "ascii" or len(part) % 2 == 0:
            out.append((kind, part))
            continue
        nxt = toks[i + 1][0] if i + 1 < len(toks) else None
        prv = toks[i - 1][0] if i else None
        nxt_ch = toks[i + 1][1] if i + 1 < len(toks) else ""
        if part.endswith(" ") and nxt == "raw" and nxt_ch == "「":
            part = part[:-1]              # 「 carries its own bearing; 《 is
                                          # stripped by the game, keep the space
        elif part.startswith(" "):
            part = part + " "             # never eat a leading space: that is
                                          # what joined 》CORPORATION
        elif nxt is None:
            part = part + " "             # end of line: the pad is invisible
        elif prv == "raw":
            part = " " + part             # slack reads better just inside 「
        else:
            part = part + " "
        out.append((kind, part))
    return out
