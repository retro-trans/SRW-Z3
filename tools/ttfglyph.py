"""Rasterise the digraph cells from a real TrueType face instead of strokes.

The game never touches the PS3 system font (no cellFont imports), so the
only way to *use* Sony's typeface is to bake it into the atlas cells. This
does exactly what makefont's strokes did -- two letters per 32-texel cell,
each centred in its half-advance slot, capitals from CAP to BASE -- but takes
the letterforms from a TTF (Rodin, `SCE-PS3-RD-*-LATIN.TTF`, is the PS3 XMB
face and ships in RPCS3's dev_flash).

A letter slot is 11.4 texels wide in dialogue and 8.8 in the library, at a
20-texel cap height; Rodin's H is ~17 wide at that height and W ~24. So every
glyph is condensed by one uniform factor chosen so a reference letter (H)
fills the slot, the few wider letters are clamped further, and the vertical
stems are widened first, because condensing thins them. The cap height is part
of the geometry so the library can use a shorter, less squeezed letter.

Letters the face lacks (composed Vietnamese, for instance) fall back to the
stroke renderer, glyph by glyph.
"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFont

import diacritics as dia

CELL = 32
SS = 4                       # supersampling factor


class Face:
    def __init__(self, path, cap_px=20.0, base=26.0, embolden=0.0, dilate=0.0, ref="H"):
        """`embolden` is extra stroke in texels all round; `dilate` widens the
        vertical stems only (texels, before condensing), which is what
        condensing takes away. `ref` is the letter whose ink is condensed to
        exactly fill the slot; anything wider (W, M, m) is clamped further."""
        self.path = path
        self.base = base
        self.cap_px = cap_px
        probe = ImageFont.truetype(path, 100)
        l, t, r, b = probe.getbbox("H", anchor="ls")
        self.size = 100.0 * cap_px / (b - t) if b != t else 100.0
        self.font = ImageFont.truetype(path, int(round(self.size * SS)))
        self.stroke = int(round(embolden * SS))
        self.dilate = int(round(dilate * SS))
        self._wide = max(self._ink(c)[2] - self._ink(c)[0] for c in ref) + self.dilate
        self._cache = {}

    def _ink(self, ch):
        """Ink bbox at SS scale, relative to the baseline origin."""
        return self.font.getbbox(ch, anchor="ls", stroke_width=self.stroke)

    def has(self, ch):
        """True when the face maps the character (its cmap, via fontTools)."""
        if ch == " ":
            return True
        if not hasattr(self, "_cmap"):
            from fontTools.ttLib import TTFont
            self._cmap = TTFont(self.path).getBestCmap()
        return ord(ch) in self._cmap

    def glyph(self, ch, ink_half):
        """Anti-aliased 'L' image of one condensed letter, its width in cell
        texels, and the vertical offset of its top relative to the baseline."""
        key = (ch, ink_half)
        if key in self._cache:
            return self._cache[key]
        l, t, r, b = self._ink(ch)
        w, h = r - l, b - t
        if w <= 0 or h <= 0:
            self._cache[key] = None
            return None
        img = Image.new("L", (w + 2 * SS + self.dilate, h + 2 * SS), 0)
        ImageDraw.Draw(img).text((SS - l, SS - t), ch, font=self.font, fill=255,
                                 anchor="ls", stroke_width=self.stroke, stroke_fill=255)
        if self.dilate:
            base = img.copy()
            for k in range(1, self.dilate + 1):
                img = ImageChops.lighter(img, ImageChops.offset(base, k, 0))
        # condense so the widest letter fills the slot, then bring to texels
        factor = min(1.0, (2.0 * ink_half) / (self._wide / SS))
        ink = (w + self.dilate) / SS
        if ink * factor > 2.0 * ink_half:            # wider than the slot: clamp
            factor = (2.0 * ink_half) / ink
        tw = max(1, int(round(img.width * factor / SS)))
        th = max(1, int(round(img.height / SS)))
        small = img.resize((tw, th), Image.BOX)
        # the image's top edge is SS texels above the ink top: ink top y = t/SS
        out = (small, (l * factor) / SS - 1.0, t / SS - 1.0)
        self._cache[key] = out
        return out

    def raster_pair(self, a, b, step, ink_half, fallback=None):
        """Coverage cell (bytearray CELL*CELL) with `a` and `b` centred in
        their slots. `fallback(ch, cx)` may return segments for a letter the
        face lacks; those are drawn by the caller's stroke rasteriser."""
        cov = bytearray(CELL * CELL)
        left = (CELL - step) / 2.0
        missing = []
        for ch, cx in ((a, left), (b, left + step)):
            if ch == " ":
                continue
            if not self.has(ch):
                missing.append((ch, cx))
                continue
            g = self.glyph(ch, ink_half)
            if g is None:
                continue
            small, dx, dy = g
            # centre the ink in the slot; baseline at self.base
            ink_w = small.width - 2.0 * (1.0 + 0.0)
            x0 = cx - ink_w / 2.0 - 1.0
            y0 = self.base + dy
            self._blit(cov, small, x0, y0)
        return cov, missing

    def natural(self, ch):
        """One letter at its natural proportions for a variable-width cell:
        (image, left bearing, top offset from baseline, advance) in texels.
        The advance is the typeface advance, so spacing is the typeface own."""
        key = ("nat", ch)
        if key in self._cache:
            return self._cache[key]
        adv = self.font.getlength(ch) / SS + (self.dilate / SS)
        l, t, r, b = self._ink(ch)
        w, h = r - l, b - t
        if w <= 0 or h <= 0:
            out = (None, 0.0, 0.0, adv)
            self._cache[key] = out
            return out
        img = Image.new("L", (w + 2 * SS + self.dilate, h + 2 * SS), 0)
        ImageDraw.Draw(img).text((SS - l, SS - t), ch, font=self.font, fill=255,
                                 anchor="ls", stroke_width=self.stroke, stroke_fill=255)
        if self.dilate:
            base = img.copy()
            for k in range(1, self.dilate + 1):
                img = ImageChops.lighter(img, ImageChops.offset(base, k, 0))
        small = img.resize((max(1, int(round(img.width / SS))), max(1, int(round(img.height / SS)))), Image.BOX)
        out = (small, l / SS - 1.0, t / SS - 1.0, adv)
        self._cache[key] = out
        return out

    # Vietnamese and friends: the face has the plain letters and, in LATIN2,
    # the circumflex/breve/d-bar precomposed forms; horn, hook-above, dot-below
    # and the tone stack are drawn as strokes from diacritics.py skeletons.
    MARK_GAP = 1.4        # texels between the ink top and the first mark
    MARK_STEP = 3.0       # vertical pitch of stacked marks
    BELOW_GAP = 2.0       # baseline to the dot below
    MARK_PEN = 1.9        # stroke width of drawn marks, texels

    def has_composed(self, ch):
        base = dia.decompose(ch)[0]
        return ord(ch) > 127 and self.has(base)

    def natural_vi(self, ch, cov, left, base_y):
        """Draw an accented letter into `cov` with its base at x=left, baseline
        base_y. Returns the advance in texels."""
        base, above, below, horn, dstroke = dia.decompose(ch)
        # precomposed forms the face has (LATIN2: a-circ, e-circ, o-circ, a-breve, d-bar)
        glyph = base
        if dstroke and self.has(ch):
            glyph, dstroke = ch, False
        elif above and above[0] in (dia.CIRC, dia.BREVE):
            pre = base + above[0]
            import unicodedata
            pre = unicodedata.normalize("NFC", pre)
            if len(pre) == 1 and self.has(pre):
                glyph, above = pre, above[1:]
        img, lb, top, adv = self.natural(glyph)
        if img is None:
            return adv
        x0 = left + lb - 1.0
        self._blit(cov, img, x0, base_y + top)
        ink_w = img.width - 2.0
        cx = x0 + 1.0 + ink_w / 2.0
        half = max(3.0, ink_w / 2.0)
        ink_top = base_y + top + 1.0                 # top of the drawn ink
        y = ink_top - self.MARK_GAP
        tone_cx = cx + (dia.HORN_TONE_SHIFT * half if horn else 0.0)
        segs = []
        for m in above:
            segs += dia.mark_segments(dia.MARK_STROKES[m], tone_cx, half, y - 2.5)
            y -= self.MARK_STEP
        for m in below:
            segs += dia.mark_segments(dia.MARK_STROKES[m], cx, half, base_y + self.BELOW_GAP)
        if horn:
            # hangs off the top-right shoulder, x-height for o/u
            segs += dia.mark_segments(dia.HORN_STROKES, cx, half, ink_top + 1.0)
            adv += 1.5
        if dstroke:
            strokes = dia.DSTROKE_LOWER if base == "d" else dia.DSTROKE_UPPER
            yy = ink_top + (base_y - ink_top) * dia.DSTROKE_FRAC.get(base, 0.3)
            segs += dia.mark_segments(strokes, cx, half, yy)
        # a tall stack (uppercase + circumflex + tone) must stay inside the cell
        if segs:
            top = min(min(sg[1], sg[3]) for sg in segs)
            if top < 2.6:                          # pen radius + AA fringe
                d = 2.6 - top
                segs = [(x1, y1 + d, x2, y2 + d) if y1 < base_y - 2 else (x1, y1, x2, y2) for x1, y1, x2, y2 in segs]
        self._strokes(cov, segs, self.MARK_PEN)
        return adv

    @staticmethod
    def _strokes(cov, segs, pen):
        """Anti-aliased distance-pen rasteriser for a few short segments."""
        if not segs:
            return
        half = pen / 2.0
        xs = [v for sg in segs for v in (sg[0], sg[2])]; ys = [v for sg in segs for v in (sg[1], sg[3])]
        for y in range(max(0, int(min(ys) - 2)), min(CELL, int(max(ys) + 3))):
            for x in range(max(0, int(min(xs) - 2)), min(CELL, int(max(xs) + 3))):
                px, py = x + 0.5, y + 0.5
                d = min(_dist(px, py, *sg) for sg in segs)
                v = half + 0.5 - d
                if v > 0:
                    i = y * CELL + x
                    cov[i] = max(cov[i], 255 if v >= 1 else int(v * 255))

    @staticmethod
    def _blit(cov, img, x0, y0):
        px = img.load()
        ix, iy = int(round(x0)), int(round(y0))
        for y in range(img.height):
            cy = iy + y
            if not 0 <= cy < CELL:
                continue
            for x in range(img.width):
                cx = ix + x
                if 0 <= cx < CELL:
                    v = px[x, y]
                    if v:
                        i = cy * CELL + cx
                        cov[i] = max(cov[i], v)


def _dist(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))
