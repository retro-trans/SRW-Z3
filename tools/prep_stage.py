"""Get one stage script ready to translate: decrypt, unpack, count.

    python tools/prep_stage.py STG0031A [STG0031B ..]

Decrypts `DATA/STAGE/<name>.SDAT` from the extracted disc with make_npdata,
writes `work/stage_dec/<name>.cpk`, extracts its Lua members to
`work/lua<n>/`, and prints how many dialogue records each member holds so the
slices can be planned. Skips work that is already there, so it is safe to
re-run. Nothing here writes to the game or to a build.
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
DISC = "E:/SRWZ3/PS3_GAME/USRDIR/DATA/STAGE"
RPCS3 = "E:/RPCS3/rpcs3.exe"


def luadir(name):
    """work/lua31a for STG0031A -- the convention the manifest already uses."""
    n = name[3:].lstrip("0") or "0"
    return os.path.join(ROOT, "work", "lua" + n.lower())


def prep(name):
    sdat = os.path.join(DISC, name + ".SDAT")
    orig = sdat + ".orig"
    src = orig if os.path.isfile(orig) else sdat   # never read a patched stage
    if not os.path.isfile(src):
        print("%s: no such script on the disc" % name)
        return None
    dec = os.path.join(ROOT, "work", "stage_dec", name + ".cpk")
    os.makedirs(os.path.dirname(dec), exist_ok=True)
    if not os.path.isfile(dec):
        # SDAT is self-keyed; tools/unsdat.py drives RPCS3's own decryptor.
        # RPCS3 is single-instance, so a running emulator has to go first --
        # the user has standing authorisation for that.
        subprocess.run(["taskkill", "/F", "/IM", "rpcs3.exe"],
                       capture_output=True, text=True)
        r = subprocess.run([sys.executable,
                            os.path.join(ROOT, "tools", "unsdat.py"),
                            src, os.path.dirname(dec),
                            "--rpcs3", RPCS3],
                           capture_output=True, text=True)
        for cand in (name + ".SDAT", os.path.basename(src)):
            got = os.path.join(os.path.dirname(dec), cand)
            if os.path.isfile(got) and got != dec:
                os.replace(got, dec)
                break
        if not os.path.isfile(dec):
            print("%s: decrypt failed: %s" % (name, (r.stdout + r.stderr)[-400:]))
            return None
    out = luadir(name)
    if not os.path.isdir(out) or not os.listdir(out):
        os.makedirs(out, exist_ok=True)
        r = subprocess.run([sys.executable,
                            os.path.join(ROOT, "tools", "extract_stage.py"),
                            dec, out], capture_output=True, text=True)
        if not os.path.isdir(out) or not os.listdir(out):
            print("%s: extract failed: %s" % (name, (r.stdout + r.stderr)[-300:]))
            return None
    import luarec
    rows = []
    for f in sorted(os.listdir(out)):
        m = re.match(r".*_(\d+)\.lua$", f)
        if not m:
            continue
        p = os.path.join(out, f)
        raw = open(p, "rb").read()
        try:
            raw.decode("cp932")
        except UnicodeDecodeError as e:
            # A patched script's English cells are not valid cp932. The disc
            # copy of STG0700 had been overwritten by an old install with no
            # .orig beside it, and "replace" decoding let it through silently.
            print("%s: %s is not pristine Japanese (%s) -- the disc copy is "
                  "probably a patched build; restore the original SDAT and "
                  "delete %s and %s" % (name, f, e, dec, out))
            return None
        try:
            recs = luarec.records(raw.decode("cp932"))
        except Exception as e:
            recs = []
        rows.append((int(m.group(1)), f, len(recs)))
    total = sum(r[2] for r in rows)
    print("%s -> %s  (%d records)" % (name, os.path.relpath(out, ROOT), total))
    for mid, f, n in rows:
        if n:
            print("    member %-3d %-28s %4d records   %d slices of 120"
                  % (mid, f, n, (n + 119) // 120))
    return rows


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    names = [a for a in argv[1:] if not a.startswith("-")]
    if not names:
        print(__doc__.strip())
        return 2
    for n in names:
        prep(n.upper())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
