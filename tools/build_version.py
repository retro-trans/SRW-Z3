"""Number successful, complete builds; failed builds never consume a number."""
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def version_key(version):
    if not re.fullmatch(r'(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)', version):
        raise ValueError('invalid build version: %s' % version)
    return tuple(map(int, version.split('.')))


def next_version(root=ROOT):
    root = Path(root)
    state = json.loads((root / 'build_version.json').read_text(encoding='utf-8'))
    versions = [state['last_successful_build']]
    versions.extend(p.stem for p in (root / 'releases').glob('*.json'))
    major, minor, build = max(map(version_key, versions))
    return '%d.%d.%d' % (major, minor, build + 1)


def write_json(path, data):
    temp = path.with_name(path.name + '.tmp')
    try:
        with temp.open('w', encoding='utf-8', newline='\n') as stream:
            stream.write(json.dumps(data, indent=2) + '\n')
        os.replace(str(temp), str(path))
    finally:
        if temp.exists():
            temp.unlink()


def stamp(outdir, manifest, root=ROOT, expected_version=None):
    """Called only after all build/regression checks and file hashing pass."""
    if manifest.get('schema') != 1 or not manifest.get('ui_regression_checks') or not manifest.get('files'):
        raise ValueError('refusing to number an unvalidated build')
    root, outdir = Path(root), Path(outdir)
    lock = root / 'build_version.lock'
    # Exclusive creation prevents two builders from claiming the same number.
    try:
        with lock.open('x'):
            pass
    except FileExistsError:
        raise RuntimeError('another build is being numbered; retry after it finishes')
    try:
        version = next_version(root)
        if expected_version is not None and version != expected_version:
            raise RuntimeError('build version changed from %s to %s; rebuild to refresh the title footer'
                               % (expected_version, version))
        if manifest.get('title_footer_version', version) != version:
            raise ValueError('title footer version does not match the build number')
        numbered = dict(manifest, version=version)
        manifest_path = outdir / 'build_manifest.json'
        write_json(manifest_path, numbered)
        try:
            write_json(root / 'build_version.json', {'last_successful_build': version})
        except BaseException:
            manifest_path.unlink()
            raise
        return version
    finally:
        lock.unlink()
