"""Read-only Vita pilot/font inspection. --write-preview creates ignored PNG."""
import argparse
import json
from pathlib import Path
import sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from cpk import CPK
import digraph as dg
import trdata
import luarec
from prepare_translation import match_records
from font_gxt import FontPage, unused_codes, index_for_code


def inspect():
    source = ROOT / 'work/vita/decrypted_PCSG00264'
    config = json.loads((ROOT / 'platforms/vita/pilot.json').read_text())
    trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
    pairs = set()
    for member in config['members']:
        cpk = CPK(str(source / member['archive']))
        payload = cpk.read(next(e for e in cpk.files if e['id'] == member['candidate_member_id']))
        lines = match_records(trdata.records(str(ROOT / member['translation'])), luarec.records(payload.decode('cp932')))
        costs = [dg.cell_cost(line) for row in lines for line in row['en'].splitlines()]
        for row in lines:
            pairs.update(dg.mixed_pairs(row['en'].replace('\r\n', '\n')))
        print(member['archive'], len(lines), 'exact source records; max pair cells/line', max(costs))
    cpk = CPK(str(source / 'DATA/TABATA/TPACKVITA.cpk'))
    pages = [FontPage(cpk.read(next(e for e in cpk.files if e['id'] == fid))) for fid in (1, 3)]
    print('Vita font: linear P4, two palettes/page, 4096x1120. Blank unassigned codes:', len(unused_codes(pages)))
    print('Opening-stage pairs needed:', len(pairs))
    return pages


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-preview', action='store_true')
    args = parser.parse_args()
    pages = inspect()
    if args.write_preview:
        out = ROOT / 'work/vita/font_anchors.png'
        if out.exists():
            raise ValueError('Preview exists')
        canvas = Image.new('RGB', (704, 200), '#222222')
        draw = ImageDraw.Draw(canvas)
        codes = [0x8149, 0x824F, 0x8260, 0x8281, 0x82A0, 0x8341, 0x889F, 0x88A0]
        for row, page in enumerate(pages):
            texture = page.image()
            for i, code in enumerate(codes):
                idx = index_for_code(code)
                x, y = idx % 128 * 32, idx // 128 * 32
                cell = texture.crop((x, y, x + 32, y + 32)).resize((64, 64), Image.Resampling.NEAREST)
                canvas.paste(cell, (i * 88, row * 100), cell)
                draw.text((i * 88, row * 100 + 68), '%04X/%d' % (code, idx), fill='white')
        canvas.save(out)
        print('Saved', out)
