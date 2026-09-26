"""User-authorized deterministic cleanup of the two imagegen word sprites.

No generated Z pixels are consumed. Outputs are local build inputs, not game
data for source control. Preview by default; --write persists the clean tiles.
"""
import argparse
from collections import deque
from pathlib import Path
from PIL import Image, ImageFilter

SOURCE = Path('work/title_logo_draft/english-logo-v2.png')
DEST = Path('work/title_logo_final')


def cutout(im, box, purple=False):
    im = im.crop(box).convert('RGBA')
    w,h = im.size
    rgb = list(im.getdata())
    outside = bytearray(w*h)
    queue = deque()
    def visit(i):
        if outside[i]: return
        r,g,b,_ = rgb[i]
        # Neutral checkerboard/shadow. Opaque black contour protects the
        # metallic whites inside the plaque; purple protects subtitle whites.
        neutral = max(r,g,b)-min(r,g,b) < (45 if purple else 25)
        if neutral and min(r,g,b) > (125 if not purple else 45):
            outside[i] = 1
            queue.append(i)
    for x in range(w): visit(x); visit((h-1)*w+x)
    for y in range(h): visit(y*w); visit(y*w+w-1)
    while queue:
        i=queue.popleft(); x=i%w
        if x: visit(i-1)
        if x+1<w: visit(i+1)
        if i>=w: visit(i-w)
        if i+w<w*h: visit(i+w)
    # Keep the largest connected silhouette, excluding background artifacts.
    seen=bytearray(outside); largest=[]
    for seed in range(w*h):
        if seen[seed]: continue
        seen[seed]=1; q=deque([seed]); component=[]
        while q:
            i=q.popleft(); component.append(i); x=i%w
            for j in ((i-1 if x else -1), (i+1 if x+1<w else -1), i-w, i+w):
                if 0<=j<w*h and not seen[j]: seen[j]=1; q.append(j)
        if len(component)>len(largest): largest=component
    alpha=bytearray(w*h)
    for i in largest: alpha[i]=255
    mask=Image.frombytes('L',(w,h),bytes(alpha))
    # Half-pixel edge softening is performed on alpha only; don't blur text.
    mask=mask.filter(ImageFilter.GaussianBlur(.35))
    im.putalpha(mask)
    # Zero invisible RGB to avoid interpolation of checkerboard colors.
    im.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in im.getdata()])
    return im.crop(mask.getbbox())


def generate():
    with Image.open(SOURCE) as src:
        assert src.size == (1495,1052) and src.mode == 'RGB'
        main=cutout(src,(0,55,1060,420))
        subtitle=cutout(src,(0,859,510,1040),purple=True)
    # Preserve native artwork footprint and transparent padding/animation pivot.
    plaque=Image.new('RGBA',(706,296))
    plaque.alpha_composite(main.resize((688,233),Image.Resampling.LANCZOS),(0,53))
    sub=Image.new('RGBA',(339,117))
    sub.alpha_composite(subtitle.resize((316,110),Image.Resampling.LANCZOS),(8,5))
    return plaque,sub


def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    tiles=generate()
    for name,tile in zip(('wordmark.png','subtitle.png'),tiles):
        print(name,tile.size,'alpha bounds',tile.getchannel('A').getbbox())
        if args.write:
            DEST.mkdir(parents=True,exist_ok=True);tile.save(DEST/name)
    if args.write:
        qa=Image.new('RGB',(1412,445))
        for col,color in enumerate(('#092345','#eeeeee')):
            bg=Image.new('RGBA',(706,445),color)
            bg.alpha_composite(tiles[0]);bg.alpha_composite(tiles[1],(180,313))
            qa.paste(bg,(706*col,0))
        qa.save(DEST/'alpha-preview.png')


if __name__=='__main__': main()
