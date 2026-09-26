"""Apply a hash-locked Vita3K file patch to a NEW folder; dry-run by default."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def safe(root, name):
    parts = name.split('/')
    if any(not p or p in ('.', '..') or ':' in p or '\\' in p for p in parts):
        raise ValueError('Unsafe manifest path: ' + name)
    result = root.joinpath(*parts).resolve()
    if root.resolve() not in result.parents:
        raise ValueError('Path leaves root: ' + name)
    return result


def matches(path, info):
    return path.is_file() and path.stat().st_size == info['bytes'] and sha(path) == info['sha256']


def apply(package, source, output, xdelta, write=False, make_zip=False):
    package, source, output = [Path(p).resolve() for p in (package, source, output)]
    manifest = json.loads((package/'manifest.json').read_text(encoding='utf-8'))
    if manifest['schema'] != 1 or manifest['title_id'] != 'PCSG00264':
        raise ValueError('Unsupported manifest')
    if output.exists() or output == source or source in output.parents or output in source.parents:
        raise ValueError('Output must be NEW and separate from the source folder')
    if output == package or package in output.parents or output in package.parents:
        raise ValueError('Output must be separate from the patch package')
    for name, record in manifest['files'].items():
        if not matches(safe(source, name), record['source']):
            raise ValueError('Wrong source file: '+name+'; requires '+manifest['source_label'])
        if 'patch' in record and not matches(safe(package, record['patch']['name']), record['patch']):
            raise ValueError('Damaged patch: '+name)
    print('Verified %d source files; %s -> %s' %
          (len(manifest['files']), manifest['source_label'], manifest['target_label']), flush=True)
    print('Output:', output, '| installable ZIP:', make_zip, flush=True)
    if not write:
        print('DRY RUN: no files changed. Add --write to apply.'); return
    output.mkdir(parents=True)
    tree = output/'PCSG00264'
    tree.mkdir()
    for name, record in manifest['files'].items():
        src, dest = safe(source, name), safe(tree, name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if 'patch' in record:
            subprocess.run([str(xdelta), '-d', '-s', str(src),
                            str(safe(package, record['patch']['name'])), str(dest)], check=True)
        else:
            shutil.copyfile(src, dest)
        if not matches(dest, record['target']):
            raise ValueError('Output mismatch: '+name+'; do NOT install this output')
    # Check source again so concurrent emulator changes cannot go unnoticed.
    for name, record in manifest['files'].items():
        if not matches(safe(source, name), record['source']):
            raise ValueError('Source changed during patching; do NOT use output')
    if make_zip:
        zpath = output/'SRW-Z3-Vita3K-0.6.14-install.zip'
        with zipfile.ZipFile(str(zpath), 'x', zipfile.ZIP_DEFLATED, allowZip64=True) as z:
            for name in manifest['files']:
                z.write(str(safe(tree, name)), 'PCSG00264/'+name)
        with zipfile.ZipFile(str(zpath)) as z:
            if z.testzip() is not None:
                raise ValueError('ZIP verification failed')
    (output/'VERIFIED.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    print('SUCCESS: all target hashes match. Original files were not modified.', flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True, help='Folder directly containing eboot.bin')
    ap.add_argument('--output', type=Path, required=True, help='New folder outside source/package')
    ap.add_argument('--xdelta', default='xdelta3')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--zip', action='store_true', help='Also create a complete Vita3K installer locally')
    a = ap.parse_args()
    apply(Path(__file__).parent, a.source, a.output, a.xdelta, a.write, a.zip)


if __name__ == '__main__':
    main()
