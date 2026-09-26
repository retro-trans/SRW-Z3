"""User-authorized cleanup of the approved subtitle, without regeneration.

Only background/alpha and native-slot sizing change. The original approved
preview is retained; the previous subtitle tile is never overwritten.
"""
import argparse
import hashlib
from pathlib import Path
from PIL import Image

SOURCE = Path('work/title_logo_draft/subtitle-approved-v2.png')
DEST = Path('work/title_logo_final/subtitle-v2.png')
SOURCE_SHA = 'ceb0056375a2bf268d378d13fa0b4675f80a7e01abc3a8b5396eec9817cc9439'


def prepare():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
    with Image.open(SOURCE) as src:
        assert src.mode == 'RGB' and src.size == (2135, 736)
        # Background is neutral gray, including holes in P/R/A. Keep white
        # letter faces and violet contours; remove neutral checkerboard even
        # when enclosed by a letter. Chroma supplies a soft outer-glow alpha.
        rgba = []
        for r, g, b in src.getdata():
            if min(r, g, b) >= 235:
                rgba.append((r, g, b, 255))
            else:
                alpha = max(0, min(255, round((b - g - 18) * 255 / 90))) if r > g + 6 else 0
                if not alpha:
                    rgba.append((0, 0, 0, 0))
                elif alpha < 255:
                    # Remove gray contamination from the faint purple glow.
                    rgba.append((90, 0, 180, alpha))
                else:
                    rgba.append((r, g, b, 255))
        art = Image.new('RGBA', src.size)
        art.putdata(rgba)
    art = art.crop(art.getchannel('A').getbbox())
    width = 316
    height = round(art.height * width / art.width)
    assert height <= 110
    tile = Image.new('RGBA', (339, 117))
    # Keep the existing subtitle's top and horizontal anchor. Preserve aspect
    # ratio, letting the smaller CHAPTER shorten the lower extent naturally.
    tile.alpha_composite(art.resize((width, height), Image.Resampling.LANCZOS), (8, 5))
    return tile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    tile = prepare()
    print('Approved subtitle:', tile.size, 'alpha bounds:', tile.getchannel('A').getbbox())
    if args.write:
        DEST.parent.mkdir(parents=True, exist_ok=True)
        if DEST.exists():
            with Image.open(DEST) as existing:
                assert existing.tobytes() == tile.tobytes(), 'Different subtitle already exists'
        else:
            tile.save(DEST)
        preview = Image.new('RGB', (678, 117))
        for x, color in ((0, '#092345'), (339, '#eeeeee')):
            bg = Image.new('RGBA', tile.size, color)
            bg.alpha_composite(tile)
            preview.paste(bg, (x, 0))
        preview.save(DEST.with_name('subtitle-v2-alpha-preview.png'))
        print('SHA256:', hashlib.sha256(DEST.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
