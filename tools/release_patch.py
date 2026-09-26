"""Build xdelta patch sets for a release snapshot.

Two sets per version, both written under `releases/<version>_xdelta/`
(gitignored -- patches embed game content, and the repo carries none):

    from-original/   pristine ISO file -> this version. Apply these to a
                     clean dump to reproduce the release.
    from-previous/   previous snapshot -> this version. These are the
                     review view: each patch's very existence and size says
                     what actually changed in that file this version.

Every patch is verified by decoding it and hashing the result against the
snapshot before it is kept. Unchanged files get no patch.

    python tools/release_patch.py <version> [--prev VERSION|none]
                                  [--iso PATH] [--xdelta PATH]

Apply (any platform with xdelta3):
    xdelta3 -d -s <original> <name>.xdelta <name>
"""
import argparse
import hashlib
import io
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import deploy   # noqa: E402  -- LAYOUT names every shipped file and its disc dir

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DEFAULT_ISO = os.path.join(ROOT, "Dai-3-Ji Super Robot Taisen Z - Jigoku-hen (Japan).iso")
DEFAULT_XD = os.path.join(ROOT, "work", "xdelta3-3.1.0-x86_64.exe")


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def pristine(name, iso, cache):
    """The untouched file, pulled from the ISO once and cached in work/."""
    os.makedirs(cache, exist_ok=True)
    dest = os.path.join(cache, name)
    if not os.path.exists(dest):
        sub = deploy.LAYOUT[name]
        want = "PS3_GAME/USRDIR/" + (sub + "/" if sub else "") + name
        import posixpath
        want = posixpath.normpath(want)
        assert want.startswith('PS3_GAME/')
        r = subprocess.run([sys.executable, os.path.join(HERE, "isoread.py"),
                            "extract", iso, want, dest],
                           capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(dest):
            raise SystemExit("cannot pull %s from the ISO: %s" % (want, r.stderr.strip()[:200]))
    return dest


def encode(xd, old, new, patch):
    os.makedirs(os.path.dirname(patch), exist_ok=True)
    r = subprocess.run([xd, "-e", "-9", "-f", "-s", old, new, patch],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("xdelta encode failed for %s: %s" % (patch, r.stderr.strip()[:200]))
    check = patch + ".chk"
    r = subprocess.run([xd, "-d", "-f", "-s", old, patch, check],
                       capture_output=True, text=True)
    ok = r.returncode == 0 and md5(check) == md5(new)
    if os.path.exists(check):
        os.remove(check)
    if not ok:
        raise SystemExit("patch does not reproduce %s" % new)
    return os.path.getsize(patch)


def build_set(xd, outdir, kind, pairs, log):
    made = []
    for name, old, new in pairs:
        if md5(old) == md5(new):
            continue
        patch = os.path.join(outdir, kind, name + ".xdelta")
        size = encode(xd, old, new, patch)
        made.append((name, size, md5(old), md5(new)))
        log("  %-26s %9d B  (%s)" % (name, size, kind))
    return made


def prev_version(version):
    """The highest snapshotted version below `version`."""
    def key(v):
        return tuple(int(x) for x in v.split("."))
    cands = [d for d in os.listdir(os.path.join(ROOT, "releases"))
             if os.path.isdir(os.path.join(ROOT, "releases", d))
             and not d.endswith("_xdelta")
             and all(x.isdigit() for x in d.split("."))
             and key(d) < key(version)]
    return max(cands, key=key) if cands else None


def main(argv=None):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("version")
    ap.add_argument("--prev", default=None,
                    help="previous version for the from-previous set; 'none' skips it")
    ap.add_argument("--iso", default=DEFAULT_ISO)
    ap.add_argument("--xdelta", default=DEFAULT_XD)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    snap = os.path.join(ROOT, "releases", a.version)
    if not os.path.isdir(snap):
        raise SystemExit("no snapshot at %s (run tools/release.py first)" % snap)
    outdir = os.path.join(ROOT, "releases", a.version + "_xdelta")
    names = [n for n in deploy.LAYOUT if os.path.exists(os.path.join(snap, n))]
    cache = os.path.join(ROOT, "work", "patch_orig")
    if a.dry_run:
        if not os.path.isfile(a.iso) or not os.path.isfile(a.xdelta):
            raise SystemExit('Missing original ISO or xdelta3')
        prior = None if a.prev == 'none' else (a.prev or prev_version(a.version))
        with open(os.path.join(ROOT, 'releases', a.version+'.json'), encoding='utf-8') as f:
            recorded = json.load(f)['files']
        import hashlib
        for name in names:
            with open(os.path.join(snap,name),'rb') as f:
                assert hashlib.sha1(f.read()).hexdigest() == recorded[name]['sha1'], name
        print('DRY RUN: %d validated files; original -> %s and %s -> %s under %s; decode-verify every delta.' %
              (len(names), a.version, prior, a.version, outdir))
        print('No files written.')
        return 0

    lines = []
    log = lambda s: (print(s), lines.append(s))     # noqa: E731

    log("== %s: from-original (apply to a clean dump)" % a.version)
    orig_pairs = [(n, pristine(n, a.iso, cache), os.path.join(snap, n)) for n in names]
    made_o = build_set(a.xdelta, outdir, "from-original", orig_pairs, log)

    prev = None if a.prev == "none" else (a.prev or prev_version(a.version))
    made_p = []
    if prev and os.path.isdir(os.path.join(ROOT, "releases", prev)):
        log("== %s: from-previous (%s -> %s: what this version changed)" % (a.version, prev, a.version))
        # Newly translated files were still pristine in the previous release.
        # Include them too, or the update set silently omits required files.
        prev_pairs = []
        for n in names:
            old = os.path.join(ROOT, "releases", prev, n)
            if not os.path.exists(old):
                old = pristine(n, a.iso, cache)
            prev_pairs.append((n, old, os.path.join(snap, n)))
        made_p = build_set(a.xdelta, outdir, "from-previous", prev_pairs, log)
    else:
        log("== no previous snapshot; from-previous skipped")

    with open(os.path.join(outdir, "MANIFEST.txt"), "w", encoding="utf-8") as fh:
        fh.write("xdelta patch set for %s (previous: %s)\n" % (a.version, prev or "-"))
        fh.write("apply: xdelta3 -d -s <source-file> <name>.xdelta <name>\n\n")
        for kind, made in (("from-original", made_o), ("from-previous", made_p)):
            for name, size, src, dst in made:
                fh.write("%-13s %-26s %9d B  %s -> %s\n" % (kind, name, size, src, dst))
    log("-> %s (%d + %d patches, all decode-verified)" % (outdir, len(made_o), len(made_p)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
