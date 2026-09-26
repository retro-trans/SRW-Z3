"""Convert translation modules from Python literals to JSON, without running them.

Why: a translation file is data, but as a .py it is EXECUTED on load -- every
tool that read one used exec_module. A batch written by a subagent, or by a
contributor, should be parsed, never run. json.load makes the wrong thing
impossible. It also gives a line:column on a malformed file instead of a
traceback from inside the assembler.

This reads each file with `ast`, evaluates only literal assignments, and
expands the one non-literal pattern in use (repeated caption constants like
`CLS, CLS, CLS`) so the JSON is self-contained. Nothing is imported.

    python tools/py2json.py <translation-dir>
"""
import ast
import json
import os
import sys

SKIP = ("library_kw.py", "library_pt.py", "library_rt.py", "manifest.py")


def resolve(node, consts):
    """Evaluate a literal, allowing bare Name references to prior constants."""
    if isinstance(node, ast.Name):
        return consts[node.id]
    if isinstance(node, ast.List):
        return [resolve(e, consts) for e in node.elts]
    if isinstance(node, ast.Dict):
        return {resolve(k, consts): resolve(v, consts)
                for k, v in zip(node.keys, node.values)}
    return ast.literal_eval(node)


def convert(path):
    tree = ast.parse(open(path, encoding="utf-8").read())
    consts, out = {}, {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1:
            name = n.targets[0].id
            val = resolve(n.value, consts)
            consts[name] = val
            if name in ("LINES", "ENTRIES", "NAMES"):
                out[name] = val
    return out


def main(argv):
    root = argv[1] if len(argv) > 1 else "translation"
    done = 0
    for dp, _, fns in os.walk(root):
        if "__pycache__" in dp:
            continue
        for fn in sorted(fns):
            if not fn.endswith(".py") or fn in SKIP:
                continue
            src = os.path.join(dp, fn)
            data = convert(src)
            if not data:
                continue
            if "ENTRIES" in data:
                # JSON object keys are strings; keep ids numeric on read
                data["ENTRIES"] = {str(k): v for k, v in data["ENTRIES"].items()}
            dst = src[:-3] + ".json"
            json.dump(data, open(dst, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)
            done += 1
            print("  %s -> %s  (%s)" % (src, os.path.basename(dst),
                                        ", ".join("%s=%d" % (k, len(v)) for k, v in data.items())))
    print("%d files converted" % done)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
