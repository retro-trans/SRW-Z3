"""Prepare loose VWF development candidates; no ZIP, CPK build or installation.

Dry-run first. Uses canonical English and the PS3 single-letter rasterizer,
encoded into independently verified blank Vita-native font cells.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'work/vita/python_deps')]
import digraph
import shared_content
from build_test import load_inputs, patch_script, verify_script, digest, TPACK
from font_gxt import unused_codes, index_for_code, require
from inspect_vwf import load
from text_codec import runs, encode
import vwf

FONT = Path('E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF')


def font_plan(pages, font=FONT):
    codes = [c for c in unused_codes(list(pages.values())) if c >> 8 == 0x87]
    require(len(codes) >= 95, 'Insufficient verified blank Latin bank cells')
    mapping = {chr(ch): codes[ch-32] for ch in range(32, 127)}
    # Explicitly reset the shared rasterizer cache: its key is a character,
    # not a font configuration. Do not inherit another platform's cached face.
    digraph._LETTER_CACHE.clear()
    digraph.use_letters(str(font), cap=22.0, dilate=0.5)
    coverage, widths, by_char = {}, bytearray([32]*192), {}
    for ch, code in mapping.items():
        cell, width = digraph.raster_letter(ch)
        require(0 < width < 32, 'Latin width collides with original-spacing sentinel')
        index = index_for_code(code)
        coverage[index] = bytes(cell)
        widths[index-vwf.BANK_CELL] = width
        by_char[ch] = width
    return mapping, coverage, bytes(widths), by_char


def line_widths(text, by_char):
    widths = []
    for line in text.replace('\r\n', '\n').split('\n'):
        width = 0
        for kind, part in runs(line):
            if kind == 'latin':
                width += sum(by_char[ch] for ch in part)
            elif kind == 'control':
                width += 6 * 32  # Conservative unresolved name placeholder.
            elif part not in '《》':
                width += 32
        widths.append(width)
    return widths


def validate_layout(text, payload, by_char):
    widths = line_widths(text, by_char)
    require(len(widths) <= 4 and max(widths) <= 960,
            'Provisional VWF pixel/line budget exceeded')
    # Original MtV line buffer is 0x101 bytes including terminator. Width
    # alone does not protect it now that each Latin character is two bytes.
    require(max(map(len, payload.split(b'\r\n'))) <= 256, 'MtV byte buffer exceeded')
    return widths


def plan(font=FONT):
    originals, records, pages, _ = load_inputs()
    mapping, coverage, widths, by_char = font_plan(pages, font)
    original_eboot, _ = load()
    candidate, executable = vwf.patch(original_eboot, widths)
    replacements, checks = defaultdict(dict), []
    for key, rows in records.items():
        checked = []

        def layout_check(text, payload):
            checked.append(validate_layout(text, payload, by_char))

        patched, stats = patch_script(originals[key], rows, mapping, layout_check)
        verify_script(originals[key], patched, rows, mapping)
        replacements[key[0]][key[1]] = patched
        checks.append(dict(archive=key[0], member=key[1], records=len(rows),
                           original_sha256=digest(originals[key]), patched_sha256=digest(patched),
                           control_bytes_unchanged=True, line_widths_texels=checked))
    for fid, page in pages.items():
        changed = page.replace(coverage)
        restored = bytearray(changed)
        # Independently restore only the 95 assigned cell rectangles and
        # require the complete texture to equal its original, palettes too.
        for index in coverage:
            x, y = index % 128 * 32, index // 128 * 32
            for row in range(32):
                offset = 64 + ((y+row)*page.width+x)//2
                restored[offset:offset+16] = page.data[offset:offset+16]
        require(bytes(restored) == page.data, 'Unexpected non-Latin font mutation')
        replacements[TPACK][fid] = changed
    report = dict(schema=1, kind='loose-vwf-development-candidate', title_id='PCSG00264',
                  shared_content=shared_content.revision(ROOT),
                  font_sha256=digest(font.read_bytes()), latin_cells=95,
                  rasterizer='tools/digraph.py raster_letter; cap22 dilate0.5',
                  width_rule='original pitch for sentinel32; quad width * glyph width / 32 otherwise',
                  executable=executable, scripts=checks, only_95_blank_cells_changed=True,
                  runtime_tested=False, release_ready=False,
                  remaining=['Vita3K runtime/visual validation', 'Keyword highlight and hit-box widths',
                             'Centered text and name/UI layout', 'Translation coverage beyond opening stage'])
    report['proof_text'] = next(row['en'] for rows in records.values() for row in rows
                                if 'A lot happened in that other world' in row['en'])
    return candidate, report, mapping, replacements, by_char


def font_proof(path, text, replacements, mapping, widths):
    """An explicitly offline GXT proof, never presented as a Vita3K screenshot."""
    from PIL import Image, ImageDraw
    from font_gxt import FontPage
    atlas = FontPage(replacements[TPACK][1]).image()
    canvas = Image.new('RGB', (1100, 230), '#13232c')
    ImageDraw.Draw(canvas).text((16, 12),
        'Vita VWF font/spacing proof - OFFLINE, not a game screenshot (32px quads)', fill='white')
    x, y, linked = 16, 50, False
    for ch in text:
        if ch == '\n':
            x, y = 16, y+40
            continue
        if ch in '《》':
            linked = ch == '《'
            continue
        code = mapping.get(ch)
        if code is None:
            code = int.from_bytes(ch.encode('cp932'), 'big')
        index = index_for_code(code)
        require(0 <= index < 4480, 'Proof contains a non-atlas character')
        gx, gy = index % 128 * 32, index // 128 * 32
        alpha = atlas.crop((gx, gy, gx+32, gy+32)).getchannel('A')
        tile = Image.new('RGB', (32, 32), '#f39cda' if linked else '#ffffff')
        canvas.paste(tile, (x, y), alpha)
        x += widths.get(ch, 32)
        require(x <= 1068 and y <= 198, 'Offline proof exceeds canvas')
    canvas.save(str(path))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--font', type=Path, default=FONT)
    ap.add_argument('--out', type=Path, default=ROOT / 'work/vita/vwf_candidate_02')
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    out = args.out.resolve()
    require(ROOT / 'work/vita' in out.parents, 'Output must be a new private work/vita subfolder')
    require(not out.exists(), 'Refusing existing output folder')
    candidate, report, mapping, replacements, widths = plan(args.font)
    print('VWF: 95 single letters, %d guarded Thumb hooks, %d opening records' %
          (len(report['executable']['sites']), sum(r['records'] for r in report['scripts'])))
    print('Width samples:', {c: widths[c] for c in 'Wi.m '})
    print('Runtime untested; not a release. No ZIP/CPK build or installation.')
    if not args.write:
        print('DRY RUN: --write saves loose development candidates into', out)
        return
    out.mkdir(parents=True, exist_ok=False)
    (out / 'eboot.bin').write_bytes(candidate)
    for archive, members in replacements.items():
        for fid, data in members.items():
            path = out / 'members' / archive / ('%d.bin' % fid)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    (out / 'VWF_AUDIT.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    (out / 'font_mapping.json').write_text(json.dumps(mapping, indent=2), encoding='utf-8')
    font_proof(out / 'font_proof.png', report['proof_text'], replacements, mapping, widths)
    print('Saved loose development candidates:', out)


if __name__ == '__main__':
    main()
