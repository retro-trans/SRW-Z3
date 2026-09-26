"""Snapshot a built patch so an old one can always be restored or compared.

    python tools/release.py 0.4.0 "menu text and opening narration"
    python tools/release.py --list
    python tools/release.py --restore 0.3.0        # deploy an older snapshot

Two halves, split by what may be published:

    releases/<version>/         the built files themselves -- GAME CONTENT,
                                gitignored, never committed
    releases/<version>.json     sizes and SHA-1s only -- committed, so the
                                repository records exactly what each release
                                contained without carrying any of it

That split is the same rule the README states for `source/`: the repo holds a
toolchain and translations, never game data. A hash manifest is enough to prove
two builds are identical, to spot which file changed between releases, and to
verify a snapshot has not rotted -- none of which needs the bytes.
"""
import argparse
import hashlib
import io
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deploy   # noqa: E402  -- for LAYOUT, so a release is exactly a deploy
from build_version import version_key

ROOT = "releases"


def digest(path):
    h = hashlib.sha1()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(version, note, build="work/out", dry_run=False):
    missing = [n for n in deploy.LAYOUT
               if not os.path.exists(os.path.join(build, n))]
    if missing:
        raise SystemExit("build is incomplete, refusing to release: %s"
                         % ", ".join(missing))
    manifest_path = os.path.join(build, 'build_manifest.json')
    if not os.path.isfile(manifest_path):
        raise SystemExit('build has no validation manifest; run a complete build first')
    with open(manifest_path, encoding='utf-8') as stream:
        validated = json.load(stream)
    if validated.get('schema') != 1 or not validated.get('ui_regression_checks'):
        raise SystemExit('build did not pass its regression checks')
    build_number = validated.get('version')
    if not build_number:
        raise SystemExit('build has no version; rebuild with the numbered builder')
    version_key(build_number)
    if version is None:
        version = build_number
    if version != build_number:
        raise SystemExit('requested version differs from build version %s' % build_number)
    if not set(deploy.LAYOUT) <= set(validated['files']):
        raise SystemExit('validation manifest omits release files')
    for name, expected in validated['files'].items():
        if os.path.basename(name) != name or name in ('.', '..'):
            raise SystemExit('invalid filename in build manifest')
        path = os.path.join(build, name)
        h = hashlib.sha256()
        with open(path, 'rb') as stream:
            for chunk in iter(lambda: stream.read(1 << 20), b''):
                h.update(chunk)
        if os.path.getsize(path) != expected['bytes'] or h.hexdigest() != expected['sha256']:
            raise SystemExit('build changed since validation: %s' % name)
    dst = os.path.join(ROOT, version)
    if os.path.exists(dst):
        raise SystemExit("%s already exists -- pick another version" % dst)
    if dry_run:
        print('DRY RUN: validated %d release files; snapshot -> %s; no files written.' % (len(deploy.LAYOUT), dst))
        return dst, {'version': version}
    os.makedirs(dst)
    files = {}
    for name in sorted(deploy.LAYOUT):
        src = os.path.join(build, name)
        shutil.copy2(src, os.path.join(dst, name))
        files[name] = {"bytes": os.path.getsize(src), "sha1": digest(src)}
    man = {"version": version, "note": note, "files": files}
    if 'translation_complete' in validated:
        man['translation_complete'] = validated['translation_complete']
        man['untranslated_mission_variants'] = validated['untranslated_mission_variants']
        # Local detailed report may contain source-language strings; do not
        # embed those in the tracked, hash-only release manifest.
        shutil.copy2(os.path.join(build, 'message_coverage.json'),
                     os.path.join(dst, 'message_coverage.json'))
    with open(os.path.join(ROOT, version + ".json"), "w", encoding="utf-8", newline='\n') as fh:
        json.dump(man, fh, ensure_ascii=False, indent=1)
    return dst, man


def manifests():
    if not os.path.isdir(ROOT):
        return []
    out = []
    for f in sorted(os.listdir(ROOT)):
        if f.endswith(".json"):
            out.append(json.load(open(os.path.join(ROOT, f), encoding="utf-8")))
    return sorted(out, key=lambda m: version_key(m['version']))


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("version", nargs="?")
    ap.add_argument("note", nargs="?", default="")
    ap.add_argument("--build", default="work/out")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--restore")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv[1:])

    if a.list:
        mans = manifests()
        if not mans:
            print("no releases yet")
            return 0
        prev = None
        for m in mans:
            print("%-10s %s" % (m["version"], m["note"]))
            if prev:
                changed = [n for n in m["files"]
                           if prev["files"].get(n, {}).get("sha1")
                           != m["files"][n]["sha1"]]
                print("           changed since %s: %s"
                      % (prev["version"], ", ".join(changed) or "nothing"))
            prev = m
        return 0

    if a.restore:
        src = os.path.join(ROOT, a.restore)
        if not os.path.isdir(src):
            raise SystemExit("no snapshot %s" % a.restore)
        man = json.load(open(os.path.join(ROOT, a.restore + ".json"),
                             encoding="utf-8"))
        bad = [n for n, v in man["files"].items()
               if digest(os.path.join(src, n)) != v["sha1"]]
        if bad:
            raise SystemExit("snapshot %s is damaged: %s"
                             % (a.restore, ", ".join(bad)))
        print("snapshot %s verified; deploy it with:" % a.restore)
        print("    python tools/deploy.py %s" % src.replace(chr(92), "/"))
        return 0

    dst, man = snapshot(a.version, a.note, a.build, a.dry_run)
    if a.dry_run:
        return 0
    a.version = man['version']
    print("release %s -> %s/  (%d files, not committed)"
          % (a.version, dst.replace(chr(92), "/"), len(man["files"])))
    print("manifest -> %s/%s.json  (hashes only, committed)" % (ROOT, a.version))
    prev = [m for m in manifests() if m["version"] != a.version]
    if prev:
        p = prev[-1]
        changed = [n for n in man["files"]
                   if p["files"].get(n, {}).get("sha1") != man["files"][n]["sha1"]]
        print("changed since %s: %s" % (p["version"], ", ".join(changed) or "nothing"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
