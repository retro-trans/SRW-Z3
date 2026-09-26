"""Build the opening-stage English Vita3K overlay; dry-run unless --write.

Only three CPK files change. Requires an installed, working Japanese base game;
never wraps/encrypts/patches the executable or embeds license material.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from cpk import CPK
import cpkpatch
import luarec
import shared_content
import trdata
from font_gxt import FontPage, unused_codes, index_for_code, require
from prepare_translation import match_records
from text_codec import dictionary_for, encode, decode, CONTROL

SOURCE = ROOT / 'work/vita/decrypted_PCSG00264'
DEFAULT_OUTPUT = ROOT / 'work/vita/english_pilot_01_checked'
FONT = Path('C:/Windows/Fonts/arialnb.ttf')
TPACK = 'DATA/tabata/TPACKVITA.cpk'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def raster(token):
    # Deliberately fixed-cell paired prototype; no claim of Vita VWF support.
    # Two 11px-wide glyph slots with 20px centers, within native 32px cells.
    font = ImageFont.truetype(str(FONT), 112)
    canvas = Image.new('L', (128, 128), 0)
    for i, ch in enumerate(token):
        if ch == ' ':
            continue
        box = font.getbbox(ch, anchor='ls')
        width, height = box[2] - box[0], box[3] - box[1]
        require(width > 0 and height > 0, 'Missing font character')
        glyph = Image.new('L', (width, height), 0)
        ImageDraw.Draw(glyph).text((-box[0], -box[1]), ch, font=font, fill=255, anchor='ls')
        # Native cap ~20px, baseline 26px; keep a constant horizontal scale,
        # further condensing unusually wide characters only.
        cap = font.getbbox('H', anchor='ls')
        factor = 80 / (cap[3] - cap[1])
        width, height = min(44, max(1, round(width * factor))), max(1, round(height * factor))
        glyph = glyph.resize((width, height), Image.Resampling.LANCZOS)
        canvas.paste(glyph, (round(24 + i * 80 - width / 2), round(104 + box[1] * factor)))
    return canvas.resize((32, 32), Image.Resampling.LANCZOS).tobytes()


def patch_script(original, lines, mapping, layout_check=None):
    text = original.decode('cp932')
    source = luarec.records(text)
    ordered = match_records(lines, source)
    out, position, stats = bytearray(), 0, []
    for match, jp, item in zip(luarec.BLOCK.finditer(text), source, ordered):
        en = item['en'].replace('\r\n', '\n')
        require(en.strip() and '$$' not in en and ']]' not in en, 'Invalid English string')
        require(Counter(CONTROL.findall(jp['jp'])) == Counter(CONTROL.findall(en)), 'Control token mismatch')
        require(jp['jp'].count('《') == en.count('《') == en.count('》'), 'Keyword link count mismatch')
        depth = 0
        for ch in en:
            if ch == '《':
                depth += 1
                require(depth == 1, 'Nested keyword link')
            elif ch == '》':
                depth -= 1
                require(depth == 0, 'Unbalanced keyword link')
        require(depth == 0, 'Unclosed keyword link')
        payload, costs = encode(en, mapping)
        require(decode(payload, mapping) == en, 'English codec round-trip mismatch')
        if layout_check is None:
            require(len(costs) <= 4 and max(costs) <= 30, 'Provisional cell/line budget exceeded')
        else:
            layout_check(en, payload)
        require(b']]' not in payload, 'Lua delimiter in encoded text')
        start = len(text[:match.start(1)].encode('cp932'))
        end = len(text[:match.end(1)].encode('cp932'))
        require(original[start:end].decode('cp932') == jp['jp'], 'Source byte-boundary mismatch')
        out.extend(original[position:start])
        out.extend(payload)
        position = end
        stats.append({'event': jp['event'], 'ordinal': jp['n'], 'speaker': jp['pid'],
                      'source_fingerprint': jp['sha'], 'line_cells': costs,
                      'english_sha256': digest(en.encode('utf-8'))})
    out.extend(original[position:])
    return bytes(out), stats


def verify_script(original, patched, expected, mapping):
    # Compare all non-dialogue bytes directly, including keyword IDs, event
    # commands, speaker records and stage-skip control flow.
    block = re.compile(br'(?<!--)\[\[(.*?)\]\]', re.S)
    before, after = list(block.finditer(original)), list(block.finditer(patched))
    require(len(before) == len(after) == len(expected), 'Rebuilt Lua record count differs')
    bp, ap = 0, 0
    for b, a, record in zip(before, after, expected):
        require(original[bp:b.start(1)] == patched[ap:a.start(1)], 'Non-dialogue Lua changed')
        require(decode(a.group(1), mapping) == record['en'].replace('\r\n', '\n'), 'Packed English mismatch')
        bp, ap = b.end(1), a.end(1)
    require(original[bp:] == patched[ap:], 'Lua trailing commands changed')


def load_inputs():
    """Shared, audited source loading for the fixed-cell pilot and VWF port."""
    import localization
    localization.ensure_compatible()
    config = json.loads((ROOT / 'platforms/vita/pilot.json').read_text())
    audited = json.loads((ROOT / 'work/vita/decryption_audit.json').read_text())['files']
    trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
    originals, records, cpk_cache = {}, {}, {}
    for name in sorted({TPACK} | {m['archive'] for m in config['members']}):
        blob = (SOURCE / name).read_bytes()
        require(digest(blob) == audited[name]['sha256'], 'Source differs from decryption audit: ' + name)
        cpk_cache[name] = CPK(str(SOURCE / name))
    textures = cpk_cache[TPACK]
    pages = {i: FontPage(textures.read(next(e for e in textures.files if e['id'] == i))) for i in (1, 3)}
    for member in config['members']:
        key = member['archive'], member['candidate_member_id']
        cpk = cpk_cache[key[0]]
        originals[key] = cpk.read(next(e for e in cpk.files if e['id'] == key[1]))
        records[key] = match_records(trdata.shared_records(Path(member['translation']).stem),
                                     luarec.records(originals[key].decode('cp932')))
    return originals, records, pages, cpk_cache


def plan():
    originals, records, pages, cpk_cache = load_inputs()
    texts = [r['en'] for rows in records.values() for r in rows]
    mapping = dictionary_for(texts, unused_codes(list(pages.values())))
    replacements, report_members = defaultdict(dict), []
    for key, rows in records.items():
        patched, stats = patch_script(originals[key], rows, mapping)
        verify_script(originals[key], patched, rows, mapping)
        replacements[key[0]][key[1]] = patched
        report_members.append({'archive': key[0], 'member_id': key[1], 'records': len(rows),
                               'original_sha256': digest(originals[key]), 'patched_sha256': digest(patched),
                               'exact_source_mapping': True, 'control_bytes_unchanged': True, 'record_checks': stats})
    coverages = {index_for_code(code): raster(token) for token, code in mapping.items()}
    for fid, page in pages.items():
        replacements[TPACK][fid] = page.replace(coverages)
    report = {'schema': 1, 'build': 'vita-english-pilot-01', 'title_id': 'PCSG00264', 'app_version': '01.00',
              'target': 'Vita3K overlay for an installed working Japanese base',
              'shared_content': shared_content.revision(ROOT), 'stage_dialogue_records': len(texts),
              'font_cells': len(mapping), 'font_file_sha256': digest(FONT.read_bytes()),
              'runtime_tested': False, 'full_english_port': False,
              'limits': ['Opening stage 0001A and 0001B dialogue only',
                         'Menus, names, combat UI and later stages remain original Japanese',
                         'Fixed-cell experimental Latin font, not PS3 variable-width layout',
                         '30-cell/4-line budget is provisional until Vita3K visual testing',
                         'No executable, firmware, license or save modifications'],
              'members': report_members, 'files': {}}
    return report, mapping, replacements, cpk_cache, records


def preview(mapping, replacements, records, out):
    page = FontPage(replacements[TPACK][1])
    atlas = page.image()
    canvas = Image.new('RGB', (1100, 280), '#14242b')
    draw = ImageDraw.Draw(canvas)
    draw.text((10, 6), 'Vita font proof: reconstructed from patched GXT; NOT a runtime screenshot', fill='white')
    samples = [record['en'] for record in next(iter(records.values()))[:2]]
    row = 0
    for sample in samples:
        encoded, _ = encode(sample, mapping)
        for line in encoded.split(b'\r\n'):
            x, i = 12, 0
            while i < len(line):
                if line[i:i + 1] == b'$':
                    draw.text((x, 30 + row * 38), line[i:i + 2].decode(), fill='yellow')
                    x += 64
                else:
                    code = int.from_bytes(line[i:i + 2], 'big')
                    if code in (0x8173, 0x8174):
                        i += 2
                        continue
                    idx = index_for_code(code)
                    require(0 <= idx < 4480, 'Preview code outside font grid')
                    sx, sy = idx % 128 * 32, idx // 128 * 32
                    cell = atlas.crop((sx, sy, sx + 32, sy + 32))
                    canvas.paste(cell, (x, 30 + row * 38), cell)
                    x += 40  # illustrative spacing only, not measured Vita advance
                i += 2
            row += 1
    canvas.save(out)


def write_build(output, report, mapping, replacements, source_archives, records):
    require(not output.exists(), 'Build destination already exists')
    require((ROOT / 'work/vita').resolve() in output.resolve().parents, 'Output must be inside work/vita')
    output.mkdir(parents=True)
    for name, edits in replacements.items():
        destination = output / 'overlay/PCSG00264' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        paths = {}
        for fid, payload in edits.items():
            path = output / 'members' / (Path(name).stem + '_%d.bin' % fid)
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(payload)
            paths[fid] = str(path)
        cpkpatch.build(str(SOURCE / name), str(destination), paths)
        rebuilt = CPK(str(destination))
        cpkpatch.validate_itoc(rebuilt.buf)
        original = source_archives[name]
        require([e['id'] for e in original.files] == [e['id'] for e in rebuilt.files], 'Archive IDs changed')
        for old, new in zip(original.files, rebuilt.files):
            fid = old['id']
            if fid in edits:
                require(rebuilt.read(new) == edits[fid], 'Replacement not preserved in packed archive')
            else:
                require(original.buf[old['offset']:old['offset'] + old['size']] ==
                        rebuilt.buf[new['offset']:new['offset'] + new['size']], 'Untouched member bytes changed')
        report['files'][name] = {'original_sha256': digest(original.buf),
                                 'patched_sha256': digest(rebuilt.buf), 'bytes': len(rebuilt.buf),
                                 'members_verified': len(rebuilt.files)}
    (output / 'font_mapping.json').write_text(json.dumps(mapping, indent=2) + '\n')
    # Use a corpus sample; a proof label need not be in the font dictionary.
    preview(mapping, replacements, records, output / 'font_proof.png')
    (output / 'BUILD_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n')
    readme = (ROOT / 'platforms/vita/TEST_BUILD.md').read_text(encoding='utf-8')
    (output / 'README-TEST.md').write_text(readme, encoding='utf-8')
    with zipfile.ZipFile(output / 'SRW-Z3-Vita-English-pilot-01-overlay.zip', 'x', zipfile.ZIP_DEFLATED) as archive:
        for file in sorted((output / 'overlay').rglob('*')):
            if file.is_file():
                archive.write(file, file.relative_to(output / 'overlay').as_posix())
        for name in ('README-TEST.md', 'BUILD_AUDIT.json', 'font_mapping.json', 'font_proof.png'):
            archive.write(output / name, name)
    with zipfile.ZipFile(output / 'SRW-Z3-Vita-English-pilot-01-overlay.zip') as archive:
        require(archive.testzip() is None, 'ZIP checksum failure')
        for name, info in report['files'].items():
            require(digest(archive.read('PCSG00264/' + name)) == info['patched_sha256'], 'ZIP payload differs')
    print('Built and verified:', output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    report, mapping, replacements, sources, records = plan()
    print('Vita English opening-stage test:', report['stage_dialogue_records'], 'exact records;', len(mapping), 'blank font cells')
    for member in report['members']:
        print(member['archive'], 'ID', member['member_id'], member['records'], 'records; command bytes unchanged')
    print('Sample:', next(iter(records.values()))[0]['en'].encode('ascii', 'backslashreplace').decode())
    print('Coverage: stage 0001A/B dialogue only. Runtime untested; no PS3 or executable edits.')
    if args.write:
        write_build(args.output, report, mapping, replacements, sources, records)
    else:
        print('Dry-run: nothing written. Inspect before adding --write.')


if __name__ == '__main__':
    main()
