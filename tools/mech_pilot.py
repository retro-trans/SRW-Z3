"""Mech -> pilot, from the zukan's own PLTN field.

The encyclopedia entry for a robot names its pilot. That is the game's own
statement, not an inference -- unlike section -> mech, which has to be argued
from what the call-outs say. One CPK member per robot.
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zukan             # noqa: E402
from cpk import CPK      # noqa: E402


def pairs(path="work/lib/MTZKN_RT.CPK"):
    k = CPK(path)
    out = {}
    for f in k.files:
        try:
            _magic, fields = zukan.parse_ordered(k.read(f))
        except Exception:
            continue
        d = {}
        for tag, payload in fields:
            try:
                d[tag] = payload.split(b"\0")[0].decode("cp932")
            except Exception:
                pass
        r, p = d.get("RBTN", "").strip(), d.get("PLTN", "").strip()
        if r and p and p != "-":
            out[r] = p
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    m = pairs()
    print("robot -> pilot pairs from the zukan: %d" % len(m))
    for want in ("\u30b8\u30a7\u30cb\u30aa\u30f3", "\u9244\u4eba\uff12\uff18\u53f7",
                 "\u30d6\u30e9\u30c3\u30af\u30aa\u30c3\u30af\u30b9",
                 "\uff21\uff32\uff38\uff0d\uff17\u30a2\u30fc\u30d0\u30ec\u30b9\u30c8"):
        print("   %-16s -> %s" % (want, m.get(want)))
    os.makedirs("work/voice", exist_ok=True)
    json.dump(m, open("work/voice/mech_pilot.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("-> work/voice/mech_pilot.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
