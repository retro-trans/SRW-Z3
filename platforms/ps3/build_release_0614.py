"""Carry scoped, guarded fixes into the validated 0.6.13 build. Dry-run first."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import eboot
from cpk import CPK
import main_link_background_layout as primary
import link_identity_geometry as identity
import dialogue_link_scene as scene
import date_card_layout as dates
import link_background_layout as links
import startup_menu_layout as menu

BASE = ROOT / 'work/build_0.6.13_batched_ui'
OUT = ROOT / 'work/build_0.6.14_release'
VERSION = '0.6.14'


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def executable(raw, mapping):
    b = bytearray(raw)
    segs = eboot._segments(b)
    ranges = primary.apply(b, segs)
    ranges += identity.apply(b, segs)
    ranges += scene.apply(b, segs)
    b, extra = dates.apply(b, mapping)
    ranges += extra
    allowed = {i for lo, hi in ranges for i in range(lo, hi)}
    assert len(b) == len(raw)
    assert all(x == y or i in allowed for i, (x, y) in enumerate(zip(raw, b)))
    links.check(b); identity.check(b); scene.check(b); dates.check(b, mapping)
    return b, ranges


def ui():
    c = CPK(str(BASE / 'AIDDATAPACK.CPK'))
    result = bytearray(c.buf)
    for ident, patch in ((0, menu.apply_ui), (1, menu.apply_art)):
        e = next(e for e in c.files if e['id'] == ident)
        assert e['size'] == e['extract']
        raw = patch(c.read(e))
        assert len(raw) == e['size']
        result[e['offset']:e['offset'] + e['size']] = raw
    # All remaining members and archive metadata are copied verbatim.
    return result


def effects():
    import title_footer as F
    import title_library_buttons as B
    import title_logo as L
    font = 'E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'
    c = CPK(str(ROOT / 'work/orig/EFFPS3.CPK'))
    original = c.read(next(e for e in c.files if e['id'] == F.MEMBER))
    del c
    new = L.apply(B.apply(original, font, VERSION))
    L.verify_complete(original, new, font, VERSION)
    c = CPK(str(BASE / 'EFFPS3.CPK'))
    e = next(e for e in c.files if e['id'] == F.MEMBER)
    old = c.read(e)
    L.verify_complete(original, old, font, '0.6.13')
    assert e['size'] == e['extract'] == len(new)
    # Only the footer rectangle may differ from the last release.
    restored = bytearray(new)
    start, _ = F.texture_span(old)
    x0, y0, x1, y1 = F.BOX
    for y in range(y0, y1):
        p = start + (y * F.SIZE[0] + x0) * 4
        restored[p:p + (x1-x0)*4] = old[p:p + (x1-x0)*4]
    assert restored == old
    result = bytearray(c.buf)
    result[e['offset']:e['offset'] + e['size']] = new
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--validate-existing', action='store_true', help='Resume validation of the exact staged port')
    a = ap.parse_args()
    assert not OUT.exists() or a.validate_existing, 'Use a fresh output directory'
    manifest = json.loads((BASE / 'build_manifest.json').read_text())
    assert manifest['version'] == '0.6.13' and manifest['ui_regression_checks']
    for name, info in manifest['files'].items():
        p = BASE / name
        assert p.stat().st_size == info['bytes'] and digest(p) == info['sha256'], name
    mapping = json.loads((BASE / 'pairs.json').read_text())
    exe, ranges = executable((BASE / 'EBOOT.BIN').read_bytes(), mapping)
    edits = {'EBOOT.BIN': exe, 'AIDDATAPACK.CPK': ui(), 'EFFPS3.CPK': effects()}
    # Deployment also lists later untranslated archives that the old release
    # left in the original ISO. Include those original bytes, never working drafts.
    from deploy import LAYOUT
    from iso_patch import Iso
    original_extras = {}
    with open('E:/SRWZ3/iso/Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso','rb') as f:
        iso = Iso(f)
        for name in set(LAYOUT)-set(manifest['files']):
            assert name.startswith('STG') and LAYOUT[name] == 'DATA/STAGE'
            record = iso.find(iso.trees[0], ['PS3_GAME','USRDIR','DATA','STAGE',name])
            assert record is not None
            _, lba, size = record
            f.seek(lba*2048); original_extras[name] = f.read(size)
    print('Original unchanged later-stage files:',len(original_extras),flush=True)
    report = {'version': VERSION, 'base': '0.6.13', 'runtime_tested': False,
              'method': 'Validated baseline plus guarded binary/UI patches; no translation rebuild',
              'executable_ranges': ranges,
              'changed': {n: {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
                          for n, b in edits.items()}}
    print(json.dumps(report, indent=2), flush=True)
    if not a.write and not a.validate_existing:
        print('DRY RUN: only these three files change; no files written.'); return
    if not a.validate_existing:
        OUT.mkdir()
    names = set(manifest['files']) | {p.name for p in BASE.glob('STG*.cpk')}
    for name in sorted(names):
        if a.validate_existing:
            expected = hashlib.sha256(edits[name]).hexdigest() if name in edits else digest(BASE/name)
            assert digest(OUT/name) == expected, name
            continue
        if name in edits:
            (OUT / name).write_bytes(edits[name])
        else:
            shutil.copy2(BASE / name, OUT / name)
            assert digest(OUT / name) == digest(BASE / name), name
    for name, info in report['changed'].items():
        assert digest(OUT / name) == info['sha256']
    for name, raw in original_extras.items():
        if (OUT/name).exists(): assert (OUT/name).read_bytes() == raw
        else: (OUT/name).write_bytes(raw)
    (OUT / 'PORT_AUDIT.json').write_text(json.dumps(report, indent=2) + '\n')
    # The working catalog has newer, unshipped suspend-scene wording. This is
    # a frozen-baseline release, not a translation rebuild. Check these inherited
    # bytes against the hash-validated baseline instead of claiming they match
    # today's editable text. Every other packed regression still runs normally.
    import suspend_scene
    def check_frozen_suspend(out, mapping, widths):
        for name in ('STG0700.cpk', 'STG0700.SDAT'):
            assert digest(Path(out)/name) == digest(BASE/name), name
        print('PASS: suspend scene is byte-identical to validated 0.6.13; newer catalog wording is not included.')
    suspend_scene.check = check_frozen_suspend
    import unit_info_currency
    def check_frozen_currency(blob, mapping, widths):
        from intermission_layout import text
        c = CPK(str(BASE/'AIDDATAPACK.CPK'))
        original = c.read(next(e for e in c.files if e['id'] == 0))
        for pair in unit_info_currency.ROWS:
            for at in pair:
                assert blob[at:at+32] == original[at:at+32]
                assert text(blob, at) == text(original, at)
        print('PASS: Unit Info currency widgets preserve validated 0.6.13; newer working-label change is not included.')
    unit_info_currency.check = check_frozen_currency
    import check_issue_fixes
    sys.argv = ['check_issue_fixes', '--out', str(OUT), '--version', VERSION, '--partial-translation']
    check_issue_fixes.main()
    from build_project import write_build_manifest
    write_build_manifest(str(OUT), VERSION)
    numbered = json.loads((OUT/'build_manifest.json').read_text())
    numbered['working_tree_shared_content_not_build_inputs'] = numbered.pop('shared_content')
    numbered['translation_baseline'] = {'version': '0.6.13',
        'build_manifest_sha256': digest(BASE/'build_manifest.json'),
        'method': 'Unchanged released translations; guarded UI/runtime fixes only'}
    (OUT/'build_manifest.json').write_text(json.dumps(numbered,indent=2)+'\n')
    print('Verified build:', OUT)


if __name__ == '__main__':
    main()
