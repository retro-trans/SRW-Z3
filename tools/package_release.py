"""Package verified per-file patches, never game files. Dry-run by default."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile


def package(version, write=False, guide=None):
    root = Path(__file__).resolve().parents[1]
    release = root / 'releases' / (version + '_xdelta')
    manifest = json.loads((root / 'releases' / (version + '.json')).read_text(encoding='utf-8'))
    if manifest['version'] != version:
        raise ValueError('Release version mismatch')
    archive = release / ('SRW-Z3-English-' + version + '.zip')
    if archive.exists():
        raise ValueError('Refusing to overwrite existing release ZIP')
    sources = [(p, 'from-original/' + p.name) for p in sorted((release / 'from-original').glob('*.xdelta'))]
    if {p.name[:-7] for p, _ in sources} != set(manifest['files']):
        raise ValueError('Patch inventory differs from release manifest')
    sources += [(release / 'MANIFEST.txt', 'MANIFEST.txt'),
                (root / 'tools/apply_xdelta.py', 'apply_xdelta.py'),
                (Path(guide) if guide else root / 'docs/INSTALL.md', 'INSTALL.md')]
    for source, name in sources:
        if not source.is_file() or source.is_symlink():
            raise ValueError('Invalid package input: ' + str(source))
    print('Package: %s; %d patches + 3 support files' % (archive, len(sources) - 3))
    print('Example contents:', ', '.join(name for _, name in sources[:3]))
    if not write:
        print('Dry run: no files changed.')
        return
    with zipfile.ZipFile(archive, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output:
        for source, name in sources:
            output.write(source, name)
    with zipfile.ZipFile(archive) as check:
        if check.testzip() is not None or set(check.namelist()) != {name for _, name in sources}:
            raise ValueError('ZIP inventory/CRC verification failed')
        for source, name in sources:
            if hashlib.sha256(check.read(name)).digest() != hashlib.sha256(source.read_bytes()).digest():
                raise ValueError('ZIP content mismatch: ' + name)
    print('Verified ZIP: %d bytes; all %d entries match sources.' % (archive.stat().st_size, len(sources)))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('version')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--guide', type=Path, help='Version-specific installation guide to include as INSTALL.md')
    args = ap.parse_args()
    package(args.version, args.write, args.guide)
