"""Freeze tested Vita3K output as verified file deltas, never full game assets."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
from apply_vita_release import sha, matches, safe

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'work/release_0.6.14'
BASE = ROOT/'work/vita/decrypted_PCSG00264'
CURRENT = ROOT/'work/vita/vita3k_linkfix_install_04'
PREVIOUS = ROOT/'work/vita/vita3k_linkfix_install_03'
XD = ROOT/'work/xdelta3-3.1.0-x86_64.exe'

GUIDE = '''# Vita3K English patch 0.6.14

Patch files only: supply your own matching Japanese game, PCSG00264 v01.00.
This download is NOT directly installable in Vita3K. It builds an installable
ZIP locally from your own files. Requires Python 3.8+ and xdelta3 (not bundled).
This release targets Vita3K; it is not a signed/encrypted physical-Vita package.

Choose the right download:
- from-original: original PFS-decrypted game folder, before English patches.
  It must contain eboot.bin, DATA, CommonData, sce_module and sce_sys directly.
  Encrypted PKG/PFS input is not accepted. SELF files must match the manifest.
- test16-linkfix-v3-to-0.6.14: complete previous test16-linkfix-v3 game folder.
  This is a local test-build baseline, NOT a previous GitHub Vita release.
  Only eboot.bin changes. Older test16/v1/v2 builds are not accepted.

Close Vita3K. Extract this patch ZIP. From its folder run (replace the paths):

    python apply_vita_release.py --source "D:/MyGame/PCSG00264" --output "D:/PatchedZ3" --xdelta "D:/Tools/xdelta3.exe" --zip

This first run only checks the input and prints the plan. Repeat with --write
added to apply. Use a NEW output folder outside both the source and patch folder.
Allow at least 6 GB free. Every input, delta and resulting file is hash checked.
Nothing is installed automatically and the source is never changed.

After SUCCESS, back up your Vita3K game/save data, then use Vita3K's ZIP/VPK
installation command to select PatchedZ3/SRW-Z3-Vita3K-0.6.14-install.zip.
Do not select this small patch download as the installer. Alternatively, with
Vita3K closed, the verified output PCSG00264 tree contains the complete app.
Keep saves separate; do not delete the game's savedata folder.

The target is exactly the user-tested test16-linkfix-v4 content. It fixes
dialogue/backlog name and term backgrounds and retains its existing menus,
date centering and translations. The in-game test build label may remain test16.
Translation is partial; not all routes, dialogue or mission text are English.
No keys, licenses, self_auth.bin, personal saves or emulator firmware are included.
Do not redistribute the complete game ZIP you generate locally.
'''


def zip_checked(path, root):
    files = sorted(p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    with zipfile.ZipFile(str(path), 'x', zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(str(p), p.relative_to(root).as_posix())
    with zipfile.ZipFile(str(path)) as z:
        assert z.testzip() is None
        assert len(z.infolist()) == len(files)
        for p in files:
            assert hashlib.sha256(z.read(p.relative_to(root).as_posix())).hexdigest() == sha(p)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    current = json.loads((CURRENT/'BUILD_AUDIT.json').read_text())
    prev = json.loads((PREVIOUS/'BUILD_AUDIT.json').read_text())
    zpath = CURRENT/current['zip']['name']
    assert matches(zpath, current['zip'])
    assert set(current['files']) == set(prev['files'])
    assert set(p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()) == set(current['files'])
    sources = {n: {'bytes': safe(BASE,n).stat().st_size, 'sha256': sha(safe(BASE,n))} for n in current['files']}
    original_audit = json.loads((ROOT/'work/vita/decryption_audit.json').read_text())
    assert all(s == {k:original_audit['files'][n][k] for k in ('bytes','sha256')} for n,s in sources.items())
    with zipfile.ZipFile(str(zpath)) as checked:
        assert set(checked.namelist()) == {'PCSG00264/'+n for n in current['files']}
    specs = [('from-original', 'Original PFS-decrypted PCSG00264 01.00', sources),
             ('test16-linkfix-v3-to-0.6.14', 'test16-linkfix-v3', prev['files'])]
    for kind, label, source in specs:
        changed = [n for n,t in current['files'].items() if source[n]['sha256'] != t['sha256']]
        print(kind, len(source), 'files,', len(changed), 'deltas; sample:', changed[:8], flush=True)
    print('Save tool bundle: converter, synthetic tests and generic guide ONLY.', flush=True)
    if not a.write:
        print('DRY RUN: no output written.'); return
    OUT.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(str(zpath)) as z:
        for kind, label, source in specs:
            name = 'SRW-Z3-Vita3K-0.6.14-'+kind
            staging = OUT/name
            staging.mkdir()
            manifest = dict(schema=1, title_id='PCSG00264', source_label=label,
                            target_label='0.6.14 (test16-linkfix-v4)', files={})
            with tempfile.TemporaryDirectory(prefix='vita-delta-', dir=str(OUT)) as temporary:
                tmp = Path(temporary)
                for n,t in current['files'].items():
                    s = source[n]
                    record = {'source': {k:s[k] for k in ('bytes','sha256')},
                              'target': {k:t[k] for k in ('bytes','sha256')}}
                    manifest['files'][n] = record
                    if s['sha256'] == t['sha256']: continue
                    old = safe(BASE,n) if kind == 'from-original' else ROOT/'work/vita/link_background_test16_03/eboot.bin'
                    if kind != 'from-original': assert n == 'eboot.bin'
                    assert matches(old, s)
                    new, check = tmp/'new.bin', tmp/'check.bin'
                    with z.open('PCSG00264/'+n) as src, new.open('wb') as dst: shutil.copyfileobj(src,dst)
                    assert matches(new,t)
                    delta_name = 'patches/'+n+'.xdelta'
                    delta = safe(staging,delta_name)
                    delta.parent.mkdir(parents=True,exist_ok=True)
                    subprocess.run([str(XD),'-e','-s',str(old),str(new),str(delta)],check=True)
                    subprocess.run([str(XD),'-d','-s',str(old),str(delta),str(check)],check=True)
                    assert matches(check,t)
                    check.unlink(); new.unlink()
                    record['patch'] = dict(name=delta_name, bytes=delta.stat().st_size, sha256=sha(delta))
                    print('Verified',kind,n,flush=True)
            (staging/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
            (staging/'README.md').write_text(GUIDE,encoding='utf-8')
            shutil.copy2(ROOT/'tools/apply_vita_release.py',staging/'apply_vita_release.py')
            zip_checked(OUT/(name+'.zip'), staging)
    bundle = OUT/'SRW-Z3-Save-Converter-0.6.14'
    (bundle/'tools').mkdir(parents=True)
    (bundle/'docs').mkdir()
    for n in ('convert_z3_saves.py','test_save_conversion.py'):
        shutil.copy2(ROOT/'tools'/n,bundle/'tools'/n)
    for dest in (bundle/'README.md',bundle/'docs/SAVE_CONVERSION.md'):
        shutil.copy2(ROOT/'docs/SAVE_CONVERTER_RELEASE.md',dest)
    subprocess.run([__import__('sys').executable,'-m','unittest','discover','-s','tools','-p','test_save_conversion.py'],cwd=str(bundle),check=True)
    zip_checked(OUT/(bundle.name+'.zip'),bundle)
    print('All Vita deltas independently decoded and matched; save tool ZIP tested.',flush=True)


if __name__ == '__main__':
    main()
