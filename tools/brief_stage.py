"""Cut one prepared stage into translator briefs.

    python tools/brief_stage.py STG0031A [--size 120]

Writes `work/tr/<stage>/brief/m<member>_<a>_<b>.md` for every dialogue member
and prints one line per slice, ready to hand to a subagent. Answers belong
beside them in `work/tr/<stage>/answer/` under the same stem; `merge_stage.py`
takes them all at once. Re-running overwrites the briefs and never touches an
answer.
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
GLOSSARY = os.path.join(ROOT, "analysis", "glossary.json")
MIN_TAIL = 40


def luadir(name):
    n = name[3:].lstrip("0") or "0"
    return os.path.join(ROOT, "work", "lua" + n.lower())


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    names = [a for a in argv[1:] if not a.startswith("-")]
    size = int(argv[argv.index("--size") + 1]) if "--size" in argv else 120
    if not names:
        print(__doc__.strip())
        return 2
    import luarec
    for name in [n.upper() for n in names]:
        src = luadir(name)
        if not os.path.isdir(src):
            print("%s: not prepared -- run tools/prep_stage.py first" % name)
            continue
        base = os.path.join(ROOT, "work", "tr", name)
        bdir, adir = os.path.join(base, "brief"), os.path.join(base, "answer")
        os.makedirs(bdir, exist_ok=True)
        os.makedirs(adir, exist_ok=True)
        for f in sorted(os.listdir(src)):
            m = re.match(r".*_(\d+)\.lua$", f)
            if not m:
                continue
            mid = int(m.group(1))
            lua = os.path.join(src, f)
            n = len(luarec.records(open(lua, "rb").read().decode("cp932", "replace")))
            if not n:
                continue
            # a 6-record tail is not worth a whole translator, and a slice
            # that thin has no surrounding scene to judge register from --
            # fold anything under MIN_TAIL into the slice before it
            bounds = list(range(0, n, size))
            if len(bounds) > 1 and n - bounds[-1] < MIN_TAIL:
                bounds.pop()
            for j, a in enumerate(bounds):
                b = bounds[j + 1] if j + 1 < len(bounds) else n
                stem = "m%d_%d_%d" % (mid, a, b)
                out = os.path.join(bdir, stem + ".md")
                ans = os.path.join(adir, stem + ".json")
                r = subprocess.run([sys.executable,
                                    os.path.join(ROOT, "tools", "export_stage.py"),
                                    lua, GLOSSARY, out, "--range", "%d:%d" % (a, b),
                                    "--answer", ans.replace(os.sep, "/")],
                                   capture_output=True, text=True)
                if not os.path.isfile(out):
                    print("  %s %s: export failed: %s"
                          % (name, stem, (r.stdout + r.stderr)[-200:]))
                    continue
                print("%s %s  brief=%s  answer=%s  %s"
                      % (name, stem,
                         os.path.relpath(out, ROOT).replace(os.sep, "/"),
                         os.path.relpath(ans, ROOT).replace(os.sep, "/"),
                         "DONE" if os.path.isfile(ans) else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
