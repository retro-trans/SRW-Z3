"""Copy one build onto the disc image and clear the installed copy.

Every file of a build must ship together -- the atlas and every script share
one pair-to-cell mapping, so a half-deployed build draws the wrong glyphs.
And `dev_hdd0/game/BLJS10256_DATA` MUST be deleted afterwards: the installed
copy goes stale against the edited disc and the game answers with
「ゲームデータが壊れています」, which looks exactly like a bad patch. Doing this
by hand is how that trap gets sprung, so it lives in one place instead.

    python tools/deploy.py work/out [--disc E:/SRWZ3/PS3_GAME/USRDIR]
                                    [--hdd  E:/RPCS3/dev_hdd0]
                                    [--keep-install]
    python tools/deploy.py --clear-install     # switching to/from the
                                               # pristine Japanese dump

Every copy is verified by hash before the install cache is removed.
"""
import hashlib
import os
import shutil
import sys
import json

DISC = "E:/SRWZ3/PS3_GAME/USRDIR"
HDD = "E:/RPCS3/dev_hdd0"
TITLE = "BLJS10256_DATA"

# build file -> directory under the disc's USRDIR
LAYOUT = {
    "EBOOT.BIN": "",
    "TPACKPS3.CPK": "DATA/TABATA",
    "STG0001A.SDAT": "DATA/STAGE",
    "STG0001B.SDAT": "DATA/STAGE",
    "STG0002.SDAT": "DATA/STAGE",
    "STG0003.SDAT": "DATA/STAGE",
    "STG0004.SDAT": "DATA/STAGE",
    "STG0005.SDAT": "DATA/STAGE",
    "STG0006.SDAT": "DATA/STAGE",
    "STG0007A.SDAT": "DATA/STAGE",
    "STG0007B.SDAT": "DATA/STAGE",
    "STG0008.SDAT": "DATA/STAGE",
    "STG0009.SDAT": "DATA/STAGE",
    "STG0010.SDAT": "DATA/STAGE",
    "STG0011.SDAT": "DATA/STAGE",
    "STG0012.SDAT": "DATA/STAGE",
    "STG0013.SDAT": "DATA/STAGE",
    "STG0014.SDAT": "DATA/STAGE",
    "STG0015.SDAT": "DATA/STAGE",
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
    "MTZKN_KW.CPK": "COMMONDATA/MTDATA",
    "MTZKN_PT.CPK": "COMMONDATA/MTDATA",
    "MTZKN_RT.CPK": "COMMONDATA/MTDATA",
    "MTV_ALL_KEYWORD_DEF.CPK": "COMMONDATA/MTDATA",
    "RPW_DATA.CPK": "COMMONDATA/MTDATA",
    "AIDDATAPACK.CPK": "DATA/AIDDATA",
    "EFFPS3.CPK": "DATA/ANIME",
    "CMN.CPK": "DATA/BTLC",
    "OP.CPK": "DATA/BTLC",
}
# Terrain-label candidates include complete, text-only map copies. Keep them
# in the same manifest/verification workflow as EBOOT; never deploy half a set.
LAYOUT.update({'MAP_%03d.ZLD' % i: 'DATA/MAPETC/ATTR' for i in range(1,65)})
LAYOUT.update({'STG0500.SDAT':'DATA/STAGE', 'STG0700.SDAT':'DATA/STAGE',
               'TROPHY.TRP':'../TROPDIR/NPWR05207_00'})


def digest(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main(argv):
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    hdd = argv[argv.index("--hdd") + 1] if "--hdd" in argv else HDD
    if argv[1] == "--clear-install":
        # For switching between the patched dump and the pristine Japanese
        # dump: the installed copy only matches whichever disc it was
        # installed from, so clear it before booting the OTHER version.
        inst = os.path.join(hdd, "game", TITLE)
        if os.path.isdir(inst):
            shutil.rmtree(inst)
            print("removed %s (it reinstalls on the next boot)" % inst)
        else:
            print("%s was not present" % inst)
        return 0
    build = argv[1]
    disc = argv[argv.index("--disc") + 1] if "--disc" in argv else DISC

    missing = [n for n in LAYOUT if not os.path.exists(os.path.join(build, n))]
    if missing:
        raise SystemExit("build is incomplete, refusing to deploy: %s" % ", ".join(missing))

    manifest_path = os.path.join(build, 'build_manifest.json')
    if os.path.exists(manifest_path):
        manifest = json.load(open(manifest_path, encoding='utf-8'))
        if manifest.get('schema') != 1 or not manifest.get('ui_regression_checks'):
            raise SystemExit('build manifest is not a validated UI build')
        if not set(LAYOUT) <= set(manifest['files']):
            raise SystemExit('build manifest omits game files')
        for name, expected in manifest['files'].items():
            if os.path.basename(name) != name or name in ('.', '..'):
                raise SystemExit('invalid file name in build manifest')
            with open(os.path.join(build, name), 'rb') as stream:
                data = stream.read()
            if len(data) != expected['bytes'] or hashlib.sha256(data).hexdigest() != expected['sha256']:
                raise SystemExit('build changed since verification: %s; rebuild before deploying' % name)

    copied = 0
    for name, sub in sorted(LAYOUT.items()):
        src = os.path.join(build, name)
        dstdir = os.path.join(disc, sub) if sub else disc
        if not os.path.isdir(dstdir):
            raise SystemExit("no such directory on the disc: %s" % dstdir)
        dst = os.path.join(dstdir, name)
        shutil.copyfile(src, dst)
        a, b = digest(src), digest(dst)
        if a != b:
            raise SystemExit("copy of %s does not match (%s != %s)" % (name, a, b))
        print("  %-26s -> %s  %s" % (name, sub or ".", a[:8]))
        copied += 1

    inst = os.path.join(hdd, "game", TITLE)
    if "--keep-install" in argv:
        print("kept %s -- the game will report corrupt data unless it matches" % inst)
    elif os.path.isdir(inst):
        shutil.rmtree(inst)
        print("removed %s (it reinstalls on the next boot)" % inst)
    else:
        print("%s was not present" % inst)
    print("deployed %d files from %s" % (copied, build))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
