"""Apply a release's xdelta patch set to your own dump of the game.

Standalone: needs only Python 3 and an xdelta3 binary. Run it from the
unzipped release folder (the one holding from-original/ and MANIFEST.txt):

    python apply_xdelta.py --dump "<path to PS3_GAME>" --xdelta xdelta3.exe

    --dump     your BLJS10256 dump: the PS3_GAME folder (or its USRDIR)
    --xdelta   path to xdelta3 (Windows: xdelta3-3.1.0-x86_64.exe; on Linux
               or macOS install xdelta3 from your package manager)
    --patches  the from-original folder (default: ./from-original)
    --dry-run  only check the dump and report what would be patched

What it does, per patch in MANIFEST.txt:
  1. finds the target file inside USRDIR (EBOOT.BIN, DATA/STAGE/*.SDAT ...)
  2. checks its MD5 against the pristine hash -- a wrong-region or already
     patched file is refused, nothing is touched
  3. decodes the patch to a temp file and checks the result's MD5
  4. only then replaces the original, keeping a copy as <name>.orig

Afterwards delete RPCS3's install cache (dev_hdd0/game/BLJS10256_DATA), or
the game will report corrupted data: that folder is a stale copy of the
disc files and is rebuilt on the next boot. See INSTALL.md.
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys

# Where each shipped file lives under PS3_GAME/USRDIR (mirrors tools/deploy.py).
LAYOUT = {
    "EBOOT.BIN": "",
    "TPACKPS3.CPK": "DATA/TABATA",
    "STG0001A.SDAT": "DATA/STAGE", "STG0001B.SDAT": "DATA/STAGE",
    "STG0002.SDAT": "DATA/STAGE", "STG0003.SDAT": "DATA/STAGE",
    "STG0004.SDAT": "DATA/STAGE", "STG0005.SDAT": "DATA/STAGE",
    "STG0006.SDAT": "DATA/STAGE", "STG0007A.SDAT": "DATA/STAGE",
    "STG0007B.SDAT": "DATA/STAGE", "STG0008.SDAT": "DATA/STAGE",
    "STG0009.SDAT": "DATA/STAGE", "STG0010.SDAT": "DATA/STAGE",
    "STG0011.SDAT": "DATA/STAGE",
    "STG0012.SDAT": "DATA/STAGE", "STG0013.SDAT": "DATA/STAGE",
    "STG0014.SDAT": "DATA/STAGE", "STG0015.SDAT": "DATA/STAGE",
    "STG0016.SDAT": "DATA/STAGE",
    "STG0017.SDAT": "DATA/STAGE",
    "STG0018.SDAT": "DATA/STAGE",
    "STG0019.SDAT": "DATA/STAGE",
    "STG0020.SDAT": "DATA/STAGE",
    "STG0021.SDAT": "DATA/STAGE",
    "STG0022.SDAT": "DATA/STAGE",
    "STG0023.SDAT": "DATA/STAGE",
    "STG0024.SDAT": "DATA/STAGE",
    "STG0025.SDAT": "DATA/STAGE",
    "STG0026.SDAT": "DATA/STAGE",
    "STG0027.SDAT": "DATA/STAGE",
    "STG0028.SDAT": "DATA/STAGE",
    "STG0029.SDAT": "DATA/STAGE",
    "STG0030.SDAT": "DATA/STAGE",
    "STG0100B.SDAT": "DATA/STAGE",
    "STG0100A.SDAT": "DATA/STAGE",
    "STG0099.SDAT": "DATA/STAGE",
    "STG0098B.SDAT": "DATA/STAGE",
    "STG0098A.SDAT": "DATA/STAGE",
    "STG0097.SDAT": "DATA/STAGE",
    "STG0096.SDAT": "DATA/STAGE",
    "STG0095.SDAT": "DATA/STAGE",
    "STG0094.SDAT": "DATA/STAGE",
    "STG0093B.SDAT": "DATA/STAGE",
    "STG0093A.SDAT": "DATA/STAGE",
    "STG0092.SDAT": "DATA/STAGE",
    "STG0091.SDAT": "DATA/STAGE",
    "STG0090.SDAT": "DATA/STAGE",
    "STG0089B.SDAT": "DATA/STAGE",
    "STG0089A.SDAT": "DATA/STAGE",
    "STG0088B.SDAT": "DATA/STAGE",
    "STG0088A.SDAT": "DATA/STAGE",
    "STG0087.SDAT": "DATA/STAGE",
    "STG0086.SDAT": "DATA/STAGE",
    "STG0085B.SDAT": "DATA/STAGE",
    "STG0085A.SDAT": "DATA/STAGE",
    "STG0084.SDAT": "DATA/STAGE",
    "STG0083.SDAT": "DATA/STAGE",
    "STG0082.SDAT": "DATA/STAGE",
    "STG0081.SDAT": "DATA/STAGE",
    "STG0080.SDAT": "DATA/STAGE",
    "STG0079.SDAT": "DATA/STAGE",
    "STG0078.SDAT": "DATA/STAGE",
    "STG0077.SDAT": "DATA/STAGE",
    "STG0076.SDAT": "DATA/STAGE",
    "STG0075.SDAT": "DATA/STAGE",
    "STG0074.SDAT": "DATA/STAGE",
    "STG0073.SDAT": "DATA/STAGE",
    "STG0072.SDAT": "DATA/STAGE",
    "STG0071.SDAT": "DATA/STAGE",
    "STG0070.SDAT": "DATA/STAGE",
    "STG0069.SDAT": "DATA/STAGE",
    "STG0068B.SDAT": "DATA/STAGE",
    "STG0068A.SDAT": "DATA/STAGE",
    "STG0067.SDAT": "DATA/STAGE",
    "STG0066.SDAT": "DATA/STAGE",
    "STG0065.SDAT": "DATA/STAGE",
    "STG0064.SDAT": "DATA/STAGE",
    "STG0063.SDAT": "DATA/STAGE",
    "STG0062.SDAT": "DATA/STAGE",
    "STG0061.SDAT": "DATA/STAGE",
    "STG0060.SDAT": "DATA/STAGE",
    "STG0059.SDAT": "DATA/STAGE",
    "STG0058.SDAT": "DATA/STAGE",
    "STG0057.SDAT": "DATA/STAGE",
    "STG0056.SDAT": "DATA/STAGE",
    "STG0055.SDAT": "DATA/STAGE",
    "STG0054.SDAT": "DATA/STAGE",
    "STG0053.SDAT": "DATA/STAGE",
    "STG0052.SDAT": "DATA/STAGE",
    "STG0051B.SDAT": "DATA/STAGE",
    "STG0051A.SDAT": "DATA/STAGE",
    "STG0050B.SDAT": "DATA/STAGE",
    "STG0050A.SDAT": "DATA/STAGE",
    "STG0049.SDAT": "DATA/STAGE",
    "STG0048.SDAT": "DATA/STAGE",
    "STG0047.SDAT": "DATA/STAGE",
    "STG0046B.SDAT": "DATA/STAGE",
    "STG0046A.SDAT": "DATA/STAGE",
    "STG0045.SDAT": "DATA/STAGE",
    "STG0044B.SDAT": "DATA/STAGE",
    "STG0044A.SDAT": "DATA/STAGE",
    "STG0043.SDAT": "DATA/STAGE",
    "STG0042.SDAT": "DATA/STAGE",
    "STG0041.SDAT": "DATA/STAGE",
    "STG0040.SDAT": "DATA/STAGE",
    "STG0039.SDAT": "DATA/STAGE",
    "STG0037.SDAT": "DATA/STAGE",
    "STG0038.SDAT": "DATA/STAGE",
    "STG0036.SDAT": "DATA/STAGE",
    "STG0035.SDAT": "DATA/STAGE",
    "STG0034.SDAT": "DATA/STAGE",
    "STG0033B.SDAT": "DATA/STAGE",
    "STG0033A.SDAT": "DATA/STAGE",
    "STG0032.SDAT": "DATA/STAGE",
    "STG0031B.SDAT": "DATA/STAGE",
    "STG0031A.SDAT": "DATA/STAGE",
    "STG0016.SDAT": "DATA/STAGE",
    "STG0017.SDAT": "DATA/STAGE",
    "STG0200.SDAT": "DATA/STAGE",
    "STG0201.SDAT": "DATA/STAGE",
    "STG0202.SDAT": "DATA/STAGE",
    "STG0210.SDAT": "DATA/STAGE",
    "STG0211.SDAT": "DATA/STAGE",
    "STG0212.SDAT": "DATA/STAGE",
    "STG0220.SDAT": "DATA/STAGE",
    "STG0221.SDAT": "DATA/STAGE",
    "STG0222.SDAT": "DATA/STAGE",
    "STG0223.SDAT": "DATA/STAGE",
    "STG0230.SDAT": "DATA/STAGE",
    "STG0231.SDAT": "DATA/STAGE",
    "STG0232.SDAT": "DATA/STAGE",
    "STG0240.SDAT": "DATA/STAGE",
    "STG0241.SDAT": "DATA/STAGE",
    "STG0242.SDAT": "DATA/STAGE",
    "STG0250.SDAT": "DATA/STAGE",
    "STG0251.SDAT": "DATA/STAGE",
    "STG0252.SDAT": "DATA/STAGE",
    "STG0253.SDAT": "DATA/STAGE",
    "STG0260.SDAT": "DATA/STAGE",
    "STG0261.SDAT": "DATA/STAGE",
    "STG0262.SDAT": "DATA/STAGE",
    "STG0270.SDAT": "DATA/STAGE",
    "STG0271.SDAT": "DATA/STAGE",
    "STG0272.SDAT": "DATA/STAGE",
    "SRVC.BIN": "DATA/BTLC",
    "CMN.CPK": "DATA/BTLC",
    "OP.CPK": "DATA/BTLC",
    "MTZKN_KW.CPK": "COMMONDATA/MTDATA", "MTZKN_PT.CPK": "COMMONDATA/MTDATA",
    "MTZKN_RT.CPK": "COMMONDATA/MTDATA",
    "MTV_ALL_KEYWORD_DEF.CPK": "COMMONDATA/MTDATA",
    "RPW_DATA.CPK": "COMMONDATA/MTDATA",
    "AIDDATAPACK.CPK": "DATA/AIDDATA",
    "EFFPS3.CPK": "DATA/ANIME",
}
LAYOUT.update({'MAP_%03d.ZLD' % i: 'DATA/MAPETC/ATTR' for i in range(1, 65)})
LAYOUT.update({'STG0500.SDAT':'DATA/STAGE', 'STG0700.SDAT':'DATA/STAGE',
               'TROPHY.TRP':'../TROPDIR/NPWR05207_00'})


def md5(path):
    h = hashlib.md5()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_manifest(path):
    """{name: (src_md5, dst_md5)} for the from-original set."""
    out = {}
    for line in open(path, encoding="utf-8"):
        parts = line.split()
        if len(parts) >= 6 and parts[0] == "from-original" and parts[-2] == "->":
            out[parts[1]] = (parts[-3], parts[-1])
    return out


def find_usrdir(dump):
    for cand in (dump, os.path.join(dump, "USRDIR"), os.path.join(dump, "PS3_GAME", "USRDIR")):
        if os.path.isfile(os.path.join(cand, "EBOOT.BIN")):
            return cand
    return None


def find_file(usrdir, name):
    """The shipped location first; then anywhere under USRDIR (dumps vary)."""
    p = os.path.join(usrdir, LAYOUT.get(name, ""), name)
    if os.path.isfile(p):
        return p
    for root, _dirs, files in os.walk(usrdir):
        if name in files:
            return os.path.join(root, name)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dump", required=True, help="your PS3_GAME folder (or its USRDIR)")
    ap.add_argument("--xdelta", default="xdelta3", help="xdelta3 executable (default: xdelta3 on PATH)")
    ap.add_argument("--patches", default="from-original", help="folder of *.xdelta patches")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    usrdir = find_usrdir(a.dump)
    if not usrdir:
        sys.exit("no EBOOT.BIN found under %s -- point --dump at the PS3_GAME folder of your dump" % a.dump)
    manifest = os.path.join(os.path.dirname(os.path.abspath(a.patches)), "MANIFEST.txt")
    if not os.path.isfile(manifest):
        manifest = os.path.join(a.patches, "..", "MANIFEST.txt")
    if not os.path.isfile(manifest):
        sys.exit("MANIFEST.txt not found next to %s" % a.patches)
    hashes = read_manifest(manifest)
    patches = sorted(f for f in os.listdir(a.patches) if f.endswith(".xdelta"))
    if not patches:
        sys.exit("no .xdelta files in %s" % a.patches)
    try:
        subprocess.run([a.xdelta, "-V"], capture_output=True)
    except OSError:
        sys.exit("cannot run xdelta3 at %r -- pass --xdelta with the path to the binary" % a.xdelta)

    print("dump:    %s" % usrdir)
    print("patches: %d in %s" % (len(patches), a.patches))
    plan, problems = [], []
    for pf in patches:
        name = pf[:-len(".xdelta")]
        target = find_file(usrdir, name)
        if not target:
            problems.append("%s: not found in the dump" % name); continue
        if name not in hashes:
            problems.append("%s: not listed in MANIFEST.txt" % name); continue
        src_md5, dst_md5 = hashes[name]
        have = md5(target)
        if have == dst_md5:
            print("  %-26s already patched -- skipping" % name); continue
        if have != src_md5:
            problems.append("%s: MD5 %s is neither the original nor this release (wrong dump, other patch, or already modified)" % (name, have)); continue
        plan.append((name, target, os.path.join(a.patches, pf), dst_md5))
    if problems:
        print("\nrefusing to continue -- fix these first:")
        for p in problems:
            print("  " + p)
        sys.exit(1)
    if not plan:
        print("nothing to do"); return
    for name, target, pf, _ in plan:
        print("  %-26s -> %s" % (name, target))
    if a.dry_run:
        print("dry run: no files changed"); return

    for name, target, pf, dst_md5 in plan:
        tmp = target + ".patched"
        r = subprocess.run([a.xdelta, "-d", "-f", "-s", target, pf, tmp], capture_output=True, text=True)
        if r.returncode != 0 or not os.path.isfile(tmp):
            sys.exit("xdelta3 failed on %s:\n%s" % (name, (r.stderr or r.stdout)[-800:]))
        got = md5(tmp)
        if got != dst_md5:
            os.remove(tmp)
            sys.exit("%s: patched result has MD5 %s, expected %s -- patch not applied" % (name, got, dst_md5))
        backup = target + ".orig"
        if not os.path.exists(backup):
            shutil.copy2(target, backup)
        os.replace(tmp, target)
        print("  patched %s" % name)
    print("\ndone: %d files patched (originals kept as *.orig)." % len(plan))
    print("Now delete RPCS3's dev_hdd0/game/BLJS10256_DATA folder before booting (see INSTALL.md).")


if __name__ == "__main__":
    main()
