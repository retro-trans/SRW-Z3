"""Build a NEW portable Windows x64 folder; dry-run unless --write is supplied.

Run with a clean Python 3.12 x64 venv containing PyInstaller 6.22.3.
Only explicit app sources, public docs and runtime libraries are packaged.

Legacy standalone 0.6.14 reference. The maintained converter is now in
../retro-trans-tools/retro_trans/z3_saves.py and Retro Trans's Z3 saves tab.
Keep this historical implementation for existing packagers/native checks;
make future converter changes in Retro Trans. No new standalone release implied.
"""
import argparse
import hashlib
from importlib.metadata import distribution, version
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NAME = 'SRW-Z3-Save-Converter'
SOURCES = ('tools/convert_z3_saves.py', 'tools/save_converter_gui.py',
           'tools/test_save_conversion.py', 'tools/test_save_converter_gui.py',
           'tools/build_save_converter_windows.py', 'docs/SAVE_CONVERTER_RELEASE.md')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(output, tcl_license, write=False):
    output = output.resolve()
    if (ROOT / 'work').resolve() not in output.parents or output.exists():
        raise ValueError('Choose a NEW output folder under workspace work/')
    if sys.platform != 'win32' or struct.calcsize('P') != 8:
        raise ValueError('Build using Windows x64 Python')
    if version('pyinstaller') != '6.22.3':
        raise ValueError('Expected pinned PyInstaller 6.22.3')
    base = Path(sys.base_prefix)
    licenses = {
        'Python-LICENSE.txt': base / 'LICENSE.txt',
        'Tk-license.terms': base / 'tcl/tk8.6/license.terms',
        'Tcl-license.terms': tcl_license.resolve(),
        'PyInstaller-COPYING.txt': Path(distribution('pyinstaller').locate_file(
            'pyinstaller-6.22.3.dist-info/licenses/COPYING.txt')),
    }
    for path in list(licenses.values()) + [ROOT / p for p in SOURCES]:
        if not path.is_file():
            raise ValueError('Missing explicit input: ' + str(path))
    command = [sys.executable, '-m', 'PyInstaller', '--onedir', '--windowed', '--noupx',
               '--name', NAME, '--distpath', str(output / 'dist'),
               '--workpath', str(output / 'build'), '--specpath', str(output),
               '--add-data', str(ROOT / 'docs/SAVE_CONVERTER_RELEASE.md') + ';.',
               str(ROOT / 'tools/save_converter_gui.py')]
    print('NEW Windows x64 portable app:', output)
    print('App source allowlist:', ', '.join(SOURCES))
    print('Runtime: Python', sys.version.split()[0], '/ PyInstaller', version('pyinstaller'))
    print('No game assets, saves, keys or local conversion examples included.')
    print(subprocess.list2cmdline(command))
    if not write:
        print('DRY RUN: no files created.')
        return
    output.mkdir(parents=True)
    env = dict(os.environ, PYINSTALLER_CONFIG_DIR=str(output / 'cache'))
    env.pop('PYTHONPATH', None)
    subprocess.run(command, cwd=str(ROOT), env=env, check=True)
    app = output / 'dist' / NAME
    for relative in SOURCES:
        target = app / 'source' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    for name, source in licenses.items():
        target = app / 'licenses' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    shutil.copyfile(ROOT / 'docs/SAVE_CONVERTER_RELEASE.md', app / 'README-FIRST.md')
    dependencies = {name: version(name) for name in (
        'pyinstaller', 'pyinstaller-hooks-contrib', 'altgraph', 'packaging',
        'pefile', 'pywin32-ctypes', 'setuptools')}
    manifest = dict(version='0.6.14', platform='Windows-x64', python=sys.version,
                    build_dependencies=dependencies, signed=False,
                    files={p.relative_to(app).as_posix(): dict(bytes=p.stat().st_size, sha256=sha(p))
                           for p in sorted(app.rglob('*')) if p.is_file()})
    with (app / 'BUILD-MANIFEST.json').open('x', encoding='utf-8') as stream:
        json.dump(manifest, stream, indent=2)
    print('Built portable folder:', app)
    print('Run the executable --self-test NEW_REPORT.json before creating/uploading a ZIP.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--tcl-license', type=Path, required=True,
                        help='Upstream license.terms matching the bundled Tcl runtime')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    build(args.output, args.tcl_license, args.write)


if __name__ == '__main__':
    main()
