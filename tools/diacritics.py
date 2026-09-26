"""Compose accented Latin letters from a base glyph plus marks.

Vietnamese is the demanding case: a letter can carry a shape modifier AND a
tone at once -- `ế` is e + circumflex + acute, `ệ` is e + circumflex + dot
below. Rather than draw 134 precomposed glyphs by hand, decompose with
Unicode NFD and stack what comes out. That makes every other Latin script
(French, Spanish, Czech, Polish...) fall out for free.

Vertical budget inside the 32-texel cell, for scripts that stack:

    0                       top of cell
    |  tone mark            ~3 texels
    |  shape modifier       ~3 texels
    CAP=11 ---------------  cap height 14 texels
    BASE=25 --------------  baseline
    |  descender / dot below
    32                      bottom of cell

Cap height drops from 20 texels to 14 to buy that room. The marks land around
3 screen pixels tall, which reads -- but tone marks carry meaning in
Vietnamese, so check a real sentence in-game before committing.
"""
import unicodedata

# combining marks, by codepoint
GRAVE, ACUTE, CIRC, TILDE, BREVE, HOOK, HORN, DOT_BELOW = (
    "\u0300", "\u0301", "\u0302", "\u0303", "\u0306", "\u0309", "\u031b", "\u0323")

ABOVE = (GRAVE, ACUTE, CIRC, TILDE, BREVE, HOOK)
BELOW = (DOT_BELOW,)

# Stroke skeletons, in (x relative to the letter's half-width, y in texels
# measured from the mark's own baseline). Drawn by the same distance pen as
# the letterforms, just thinner.
MARK_STROKES = {
    GRAVE: [(-0.50, 0.0), (0.50, 2.5)],
    ACUTE: [(-0.50, 2.5), (0.50, 0.0)],
    CIRC:  [(-0.55, 2.5), (0.0, 0.0), (0.55, 2.5)],
    BREVE: [(-0.55, 0.0), (-0.30, 2.4), (0.30, 2.4), (0.55, 0.0)],
    TILDE: [(-0.60, 2.0), (-0.22, 0.3), (0.22, 2.0), (0.60, 0.3)],
    HOOK:  [(-0.30, 2.6), (-0.05, 0.3), (0.35, 0.5), (0.40, 2.0)],
    DOT_BELOW: [(0.0, 0.0), (0.0, 0.7)],
}

# The horn on o'/u' is not a mark that floats above; it hangs off the letter's
# top right shoulder, so it is positioned against the letter, not stacked.
# Sits ON the shoulder and curls right, so it does not read as an acute. When
# a tone rides on the same letter the tone shifts LEFT to keep them apart --
# at 11 texels wide, o / ơ / ó / ớ otherwise collapse into each other.
HORN_STROKES = [(0.80, 2.2), (1.20, 0.6), (1.15, -1.3)]
HORN_TONE_SHIFT = -0.34

# d-stroke. The bar has to actually CROSS the stem, and the stem sits in a
# different place in each case: lowercase `d` carries it on the right (x=0.93
# in the glyph, i.e. +0.86 in half-width units), uppercase `D` on the left.
DSTROKE_LOWER = [(0.30, 0.0), (1.35, 0.0)]
DSTROKE_UPPER = [(-1.35, 0.0), (-0.10, 0.0)]
DSTROKE_FRAC = {"d": 0.28, "D": 0.50}      # height down from cap

MARK_STEP = 3.2          # vertical pitch when two marks stack
MARK_GAP = 2.6           # gap from cap height to the first mark
BELOW_GAP = 2.2          # gap from baseline down to a dot


def decompose(ch):
    """ch -> (base letter, [marks above], [marks below], horn?, dstroke?)"""
    if ch in ("\u0111", "\u0110"):                 # d-bar / D-bar
        return ("d" if ch == "\u0111" else "D", [], [], False, True)
    nfd = unicodedata.normalize("NFD", ch)
    base, above, below, horn = nfd[0], [], [], False
    for m in nfd[1:]:
        if m == HORN:
            horn = True
        elif m in BELOW:
            below.append(m)
        elif m in ABOVE:
            above.append(m)
    # circumflex/breve sit closest to the letter, the tone rides on top
    above.sort(key=lambda m: 0 if m in (CIRC, BREVE) else 1)
    return (base, above, below, horn, False)


def is_supported(ch, glyphs):
    base, above, below, horn, dstroke = decompose(ch)
    if base not in glyphs:
        return False
    return all(m in MARK_STROKES for m in above + below)


def mark_segments(strokes, cx, half, dy, scale=1.0):
    segs = []
    for i in range(len(strokes) - 1):
        (ax, ay), (bx, by) = strokes[i], strokes[i + 1]
        segs.append((cx + ax * half * scale, dy + ay,
                     cx + bx * half * scale, dy + by))
    return segs


def compose_segments(ch, cx, half, cap, base_y, base_segs_fn):
    """Full segment list for one accented character centred on texel cx."""
    base, above, below, horn, dstroke = decompose(ch)
    segs = list(base_segs_fn(base, cx))
    y = cap - MARK_GAP
    tone_cx = cx + (HORN_TONE_SHIFT * half if horn else 0.0)
    for m in above:
        segs += mark_segments(MARK_STROKES[m], tone_cx, half, y)
        y -= MARK_STEP
    for m in below:
        segs += mark_segments(MARK_STROKES[m], cx, half, base_y + BELOW_GAP)
    if horn:
        segs += mark_segments(HORN_STROKES, cx, half, cap)
    if dstroke:
        strokes = DSTROKE_LOWER if base == "d" else DSTROKE_UPPER
        y = cap + (base_y - cap) * DSTROKE_FRAC.get(base, 0.3)
        segs += mark_segments(strokes, cx, half, y)
    return segs
