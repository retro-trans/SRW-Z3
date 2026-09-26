"""Halfwidth ASCII -> fullwidth, because the game has no ASCII glyphs.

Verified in-game: a dialogue line written in fullwidth Latin renders as clean
Latin letters, while the same text in halfwidth ASCII renders as unrelated
kanji -- the renderer consumes single bytes as double-byte lead bytes. So every
line of English has to be fullwidth.

The cost: a fullwidth character occupies TWO columns. English is therefore
roughly twice as wide as it looks, and line budgeting is the main constraint on
the translation.

    python tools/fullwidth.py "Look, everyone!"
    python tools/fullwidth.py --width "Look, everyone!"
"""
import sys

# U+0021..U+007E map to U+FF01..U+FF5E; space becomes the ideographic space.
ASCII_LO, ASCII_HI, FULL_LO = 0x21, 0x7E, 0xFF01
IDEOGRAPHIC_SPACE = "\u3000"

# Characters cp932 cannot encode, with a usable stand-in.
SUBSTITUTES = {
    "'": "\u2019",   # cp932 0x8166
    '"': "\u201d",
    "-": "\uFF0D",
    "\u2014": "\uFF0D",   # em dash does not exist
    "\u2013": "\uFF0D",
}


def to_fullwidth(s):
    out = []
    for ch in s:
        ch = SUBSTITUTES.get(ch, ch)
        if ch == " ":
            out.append(IDEOGRAPHIC_SPACE)
        elif ASCII_LO <= ord(ch) <= ASCII_HI:
            out.append(chr(ord(ch) - ASCII_LO + FULL_LO))
        else:
            out.append(ch)
    return "".join(out)


def columns(s):
    """Display width. Fullwidth and Japanese cost 2, halfwidth 1."""
    n = 0
    for ch in s:
        n += 1 if ord(ch) < 0x80 else 2
    return n


def check(s):
    """Return the characters cp932 cannot represent."""
    bad = []
    for ch in s:
        try:
            ch.encode("cp932")
        except UnicodeEncodeError:
            bad.append(ch)
    return bad


def main(argv):
    args = [a for a in argv[1:] if a != "--width"]
    if not args:
        print(__doc__.strip())
        return 2
    for text in args:
        fw = to_fullwidth(text)
        bad = check(fw)
        print(fw)
        if "--width" in argv:
            print("  columns: %d" % columns(fw))
        if bad:
            print("  NOT ENCODABLE in cp932: %r" % bad)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
