"""Undo Japanese word-cell squeezing in the shared map support popups.

Five XYUV vertices per word: center plus four corners. Keep UVs, vertical
coordinates, shear, colors, and animation references unchanged. Only widen
the three complete phrases, retaining each phrase's original center.
"""
import struct

# (center-vertex address, texture-2 word x, original cell width, new width)
GROUPS = (
    ((0x4d518, 0, 72, 132), (0x4d568, 144, 72, 118)),
    ((0x4d5b8, 0, 72, 132), (0x4d608, 72, 72, 106)),
    ((0x4d658, 216, 40, 62), (0x4d6a8, 72, 72, 106)),
)


def changes(blob):
    edits = []
    for group in GROUPS:
        first, last = group[0], group[-1]
        left = struct.unpack_from('>f', blob, first[0])[0]*640-first[2]/2
        right = struct.unpack_from('>f', blob, last[0])[0]*640+last[2]/2
        width = sum(row[3] for row in group)-4
        start = (left+right-width)/2
        for p, tx, old_width, new_width in group:
            for i, (u, v) in enumerate(((tx+old_width/2,108), (tx,88),
                                       (tx+old_width,88), (tx+old_width,128), (tx,128))):
                q = p+i*16
                x, y, have_u, have_v = struct.unpack_from('>4f', blob, q)
                assert (have_u,have_v)==(u/512,v/512), hex(q)
                # Maintain the original 8px italic shear, not scale it wider.
                center = struct.unpack_from('>f', blob, p)[0]*640
                frac = (u-tx)/old_width
                shear = x*640-(center-old_width/2+frac*old_width)
                edits.append((q,struct.pack('>f',(start+frac*new_width+shear)/640)))
            start += new_width-4
    return edits


def apply(blob):
    out=bytearray(blob)
    for p,value in changes(blob):out[p:p+4]=value
    return bytes(out)


def verify(source,built):
    for p,value in changes(source):
        assert built[p:p+4]==value, hex(p)
        assert built[p+4:p+16]==source[p+4:p+16], hex(p)
    print('PASS: Support Defend/Attack and Re-Attack natural-width map words; UVs and vertical geometry retained.')


def preview(source,font_path,destination):
    """Offline render of actual word quads for visual QA, not a screenshot."""
    from PIL import Image,ImageDraw
    import trader_art
    canvas=Image.new('RGBA',(520,160),(7,22,24,255))
    draw=ImageDraw.Draw(canvas)
    for version,blob,origin_y in [('0.6.3',source,25),('Revised',apply(source),100)]:
        draw.text((10,origin_y+8),version,fill='white')
        for row,word in zip(GROUPS[0],('Support','Defend')):
            p,tx,w,_=row
            tile=trader_art.tile(word,w,40,30,font_path)
            if version=='0.6.3':
                # Former renderer forced all word masks into 29px height.
                bbox=tile.getbbox();ink=tile.crop(bbox).resize((bbox[2]-bbox[0],29))
                tile=Image.new('RGBA',(w,40));tile.alpha_composite(ink,(bbox[0],4))
            x0,y0=struct.unpack_from('>2f',blob,p+16)
            x1,_=struct.unpack_from('>2f',blob,p+32)
            x2,y2=struct.unpack_from('>2f',blob,p+64)
            left=x0*640+190;top=y0*360+origin_y
            width=(x1-x0)*640;height=(y2-y0)*360
            shear=(x2-x0)*640/height
            a=w/width;b=-a*shear;c=-a*left-b*top
            layer=tile.transform(canvas.size,Image.Transform.AFFINE,
                                 (a,b,c,0,40/height,-top*40/height),
                                 resample=Image.Resampling.BICUBIC)
            tint=Image.new('RGBA',canvas.size,(245,214,66,255));tint.putalpha(layer.getchannel('A'))
            canvas.alpha_composite(tint)
    canvas.convert('RGB').save(destination)
