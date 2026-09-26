"""Batch-decrypt the game's SDAT containers using RPCS3's decryptor.

The STAGE scenario files are SDAT (NPD flag 0x01000000): self-keyed, so they
decrypt offline with no console account, RIF or klicensee. Rather than
reimplement PS3 crypto, this drives `rpcs3.exe --decrypt`, which is already
correct and already on your disk.

RPCS3's --decrypt handles only the FIRST path it is given, despite the
"<path(s)>" in its help text, and it does not exit when it is done. So this
runs one invocation per file and kills each one once its output appears.
RPCS3 is single-instance: close it before running this.

    python tools/unsdat.py <src-dir-or-file> <outdir> [--rpcs3 PATH]
"""
import argparse
import os
import shutil
import subprocess
import sys
import time

DEFAULT_RPCS3 = r"D:\RPCS3\rpcs3.exe"


def is_sdat(path):
    try:
        with open(path, "rb") as fh:
            return fh.read(4) == b"NPD\0"
    except OSError:
        return False


def collect(src):
    if os.path.isfile(src):
        return [src] if is_sdat(src) else []
    found = []
    for root, _dirs, names in os.walk(src):
        for n in names:
            p = os.path.join(root, n)
            if is_sdat(p):
                found.append(p)
    return sorted(found)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("src")
    ap.add_argument("outdir")
    ap.add_argument("--rpcs3", default=DEFAULT_RPCS3)
    ap.add_argument("--timeout", type=float, default=60.0,
                    help="seconds to wait for one file")
    a = ap.parse_args(argv)

    if not os.path.isfile(a.rpcs3):
        sys.exit("rpcs3 not found at %s (pass --rpcs3)" % a.rpcs3)

    files = collect(a.src)
    if not files:
        sys.exit("no NPD/SDAT files under %s" % a.src)
    os.makedirs(a.outdir, exist_ok=True)

    # rpcs3 writes <name>.unedat beside its input, so stage copies in outdir
    staged = []
    for f in files:
        dest = os.path.join(a.outdir, os.path.basename(f))
        shutil.copyfile(f, dest)
        staged.append(dest)

    done = 0
    for f in staged:
        out = f + ".unedat"
        proc = subprocess.Popen([a.rpcs3, "--decrypt", f],
                                cwd=os.path.dirname(a.rpcs3),
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        # rpcs3 stays open after decrypting, so wait on the artifact, not the
        # process, then shut it down before the next one hits the instance lock
        deadline = time.time() + a.timeout
        while time.time() < deadline:
            if os.path.isfile(out) and os.path.getsize(out) > 0:
                time.sleep(0.15)          # let the last write land
                break
            if proc.poll() is not None:
                break
            time.sleep(0.1)
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
        done += 1
        if done % 10 == 0 or done == len(staged):
            print("  %d/%d" % (done, len(staged)), flush=True)

    ok = failed = 0
    for s in staged:
        out = s + ".unedat"
        if os.path.isfile(out) and os.path.getsize(out) > 0:
            os.replace(out, s)          # keep the original name
            ok += 1
        else:
            failed += 1
            print("  FAILED: %s" % os.path.basename(s))
    print("%d decrypted, %d failed -> %s" % (ok, failed, a.outdir))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
