"""Link voice sections to mechs through the weapons their call-outs name.

There is no stored pointer to follow. Unit ids (robot record w4) appear nowhere
in SRVC.BIN, in either byte order, so the game does not key voice sets by unit
id -- or not by one written in this file. What DOES connect them is content: an
attack call-out speaks its weapon's name, and RPW knows exactly which unit owns
that weapon.

    weapon name -> weapon record -> wpn-1r triple -> unit id -> robot record

wpn-1r is 918 triples of (unit id, weapon count, first weapon index), and the
ranges are consecutive with no gaps -- (0x0E200220, 4, 2483) is Genion's four.

The link is therefore evidence, not a lookup: a section is attributed to the
unit whose weapons its lines name, and the count is reported so a weak match
can be told from a strong one. Genion is the control -- it was identified from
player screenshots first, so if this disagrees there, the method is wrong.
"""
import collections
import io
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpw             # noqa: E402
from cpk import CPK    # noqa: E402

MAXOWNERS = 4      # a fragment owned by more units than this says nothing
MARGIN = 1.5       # the winner must beat the runner-up by this factor
KATA = re.compile(r"[\u30a1-\u30fa\u30fc\u30fb]{4,}")
SRVC = "work/srvc/SRVC.BIN"
RPWF = "work/lib/RPW_DATA.CPK"


def rpw_tables():
    k = CPK(RPWF)
    raw = k.read(k.files[0])
    js = rpw.jstrings(raw)
    starts, _ = rpw._starts(raw)
    at = {o: i for i, o in enumerate(starts)}
    ch = {c[0]: c for c in rpw.chunks(raw)}
    cols = rpw.pointer_columns(raw)

    def col(name, rec, c):
        s, _p = cols[name]
        return struct.unpack_from("<I", raw, ch[name][2] + 4 * (rec * s + c))[0]

    # weapon record -> its two names
    ws, _wp = cols["weapon"]
    wn = ((ch["weapon"][3] - ch["weapon"][2]) // 4) // ws
    wnames = {}
    for r in range(wn):
        for c in (3, 4):
            i = at.get(col("weapon", r, c))
            if i is not None and js[i].strip():
                wnames.setdefault(r, set()).add(js[i])

    # wpn-1r: 918 triples (unit id, count, first weapon)
    c = ch["wpn-1r"]
    v = [struct.unpack_from("<I", raw, c[2] + 4 * i)[0]
         for i in range((c[3] - c[2]) // 4)]
    owner = {}
    units = {}
    for t in range(0, len(v) - 2, 3):
        uid, cnt, first = v[t], v[t + 1], v[t + 2]
        units[uid] = (cnt, first)
        for r in range(first, first + cnt):
            owner[r] = uid

    # robot record -> name, keyed by unit id in column 4
    rs, rp = cols["robot"]
    rn = ((ch["robot"][3] - ch["robot"][2]) // 4) // rs
    uname = {}
    for r in range(rn):
        uid = col("robot", r, 4)
        for p in rp:
            i = at.get(col("robot", r, p))
            if i is not None and js[i].strip():
                uname.setdefault(uid, js[i])
                break
    return wnames, owner, units, uname


def sections(b):
    """Every [index][pool] section, by the byte signature of an index word."""
    L = len(b) // 4
    w = struct.unpack_from("<%dI" % L, b, 0)
    small = [x < 0x10000 for x in w]
    out, i = [], 0
    while i < L:
        if small[i]:
            j = i
            while j < L and small[j]:
                j += 1
            if j - i >= 8:
                out.append((i * 4, j - i))
            i = j
        else:
            i += 1
    secs = []
    for off, n in out:
        # trim leading words until the rest all resolve into the pool
        for lead in range(0, min(n, 8)):
            s, cnt = off + 4 * lead, n - lead
            pool = s + 4 * cnt
            starts, p = set(), pool
            lim = min(len(b), pool + 0x20000)
            while p < lim:
                starts.add(p)
                e = b.find(bytes((0,)), p)
                if e < 0 or e - p > 400:
                    break
                try:
                    b[p:e].decode("cp932")
                except Exception:
                    break
                p = e + 1
            ok = sum(1 for q in range(cnt)
                     if (pool + struct.unpack_from("<I", b, s + 4 * q)[0]) in starts)
            if ok == cnt and cnt >= 8:
                secs.append({"index": s, "count": cnt, "pool": pool})
                break
    return secs


def strings(b, sec):
    out = []
    for i in range(sec["count"]):
        v = struct.unpack_from("<I", b, sec["index"] + 4 * i)[0]
        p = sec["pool"] + v
        e = b.find(bytes((0,)), p)
        try:
            out.append(b[p:e].decode("cp932"))
        except Exception:
            pass
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    wnames, owner, units, uname = rpw_tables()
    # Score by unit NAME, not unit id. A mech has one robot record per variant
    # and upgrade step -- Genion has ten, 0xe200020 through 0xe201220, each
    # owning its own copy of the weapon list. Keying on the id splits a correct
    # answer ten ways and lets a spurious four-kana match on some unique unit
    # outrank it. That is exactly what buried the control case.
    # katakana fragments -> the unit NAMES that own a weapon containing them
    frag = collections.defaultdict(set)
    for rec, names in wnames.items():
        uid = owner.get(rec)
        if uid is None or uid not in uname:
            continue
        who = uname[uid]
        for nm in names:
            for m in KATA.finditer(nm):
                s = m.group(0)
                for a in range(len(s) - 3):
                    for z in range(a + 4, len(s) + 1):
                        frag[s[a:z]].add(who)
    # A fragment that is part of a ROBOT's name is not weapon evidence. Pilots
    # address their machine constantly ("やるんだ、オックス！"), and super-robot
    # weapon names embed the robot name (ブラックオックス・アタック), so the two
    # signals are otherwise indistinguishable -- and the robot-name mentions
    # win on volume. That is what stole Tetsujin 28's own section, which holds
    # ハンマーパンチ / ローリングアタック / フライングキック, and gave it to
    # Black Ox.
    robot_frags = set()
    for nm in set(uname.values()):
        for m in KATA.finditer(nm):
            g = m.group(0)
            for a in range(len(g) - 3):
                for z in range(a + 4, len(g) + 1):
                    robot_frags.add(g[a:z])
    for f in robot_frags:
        frag.pop(f, None)

    b = open(SRVC, "rb").read()
    secs = sections(b)
    print("%d sections recovered" % len(secs))
    rows = []
    for si, sec in enumerate(secs):
        score = collections.Counter()
        for t in strings(b, sec):
            for m in KATA.finditer(t):
                s = m.group(0)
                best = None
                for a in range(len(s) - 3):
                    for z in range(len(s), a + 3, -1):
                        if s[a:z] in frag:
                            best = s[a:z]
                            break
                    if best:
                        break
                if best and len(frag[best]) <= MAXOWNERS:
                    for who in frag[best]:
                        score[who] += 1.0 / len(frag[best])
        rows.append((si, sec, score))
    named = 0
    for si, sec, score in rows:
        if not score:
            continue
        _who, pts = score.most_common(1)[0]
        if pts >= 1.0:
            named += 1
    print("sections with at least one weapon-name hit: %d" % named)
    print()
    print("  sec  index      count  best unit                      pts")
    for si, sec, score in rows:
        if not score:
            continue
        who, pts = score.most_common(1)[0]
        if pts < 1.0:
            continue
        mark = "  <== the screenshot-proven Genion section" \
            if sec["index"] == 0x151D44 else ""
        print("  %3d  %#08x %5d  %-28s %5.1f%s"
              % (si, sec["index"], sec["count"],
                 who[:28], pts, mark))
    # For the winning unit, which of ITS weapons does each line name? That is
    # the mech -> weapon -> line chain, end to end, and it is checkable: the
    # line has to contain the weapon's own name.
    # weapons owned by each unit name, for the family test below
    byname = collections.defaultdict(set)
    for rec, names in wnames.items():
        who = uname.get(owner.get(rec))
        if who:
            byname[who] |= names

    out = []
    for si, sec, sc in rows:
        # A mech's upgraded form is a separate robot record with its own name
        # but the same weapons -- Genion and Genion GAI tie, and demanding a
        # single winner throws the answer away. Keep every candidate within the
        # margin as one family and pool their weapons.
        best, fam = None, []
        if sc:
            top = sc.most_common()
            if top[0][1] >= 1.0:
                head = top[0][0]
                fam = [head]
                for n, v in top[1:]:
                    if v * MARGIN < top[0][1]:
                        break
                    # an upgrade form shares the weapon list; a coincidence
                    # that merely scored close does not
                    a, bset = byname[n], byname[head]
                    if a and bset and len(a & bset) / len(a | bset) >= 0.4:
                        fam.append(n)
                best = " / ".join(fam[:3])
        calls = {}
        if best:
            mine = {}
            for rec, names in wnames.items():
                if uname.get(owner.get(rec)) in fam:
                    for nm in names:
                        mine[nm] = rec
            for i, t in enumerate(strings(b, sec)):
                for nm, rec in mine.items():
                    # call-outs abbreviate: "パニッシャー、セット！" for
                    # Ｄソリッドパニッシャー, "グレイヴ" for アクセルグレイヴ. So any
                    # katakana run of the weapon name, or any 4+ substring of
                    # one, counts -- not just the longest run whole.
                    # ...but the fragment must also be DISTINCTIVE. Accepting
                    # any 4-kana substring let "アタック" of ブラックオックス
                    # ・アタック claim seventy unrelated lines. Reuse the same
                    # owner-count filter the scorer uses.
                    hit = False
                    for run in (KATA.findall(nm) or []):
                        for a in range(len(run) - 3):
                            for z in range(len(run), a + 3, -1):
                                f = run[a:z]
                                if f in t and len(frag.get(f, ())) <= MAXOWNERS:
                                    hit = True
                                    break
                            if hit:
                                break
                        if hit:
                            break
                    if hit:
                        calls.setdefault(str(rec), []).append(i)
        out.append({"sec": si, "index": sec["index"], "count": sec["count"],
                    "pool": sec["pool"], "unit": best,
                    "pts": round(sc.most_common(1)[0][1], 2) if sc else 0,
                    "weapon_lines": calls})
    json.dump(out, open("work/voice/sections.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    conf = [o for o in out if o["unit"]]
    print()
    print("confident after margin: %d of %d sections, %d distinct mechs"
          % (len(conf), len(out), len({o["unit"] for o in conf})))
    print("sections with a weapon->line map: %d"
          % sum(1 for o in conf if o["weapon_lines"]))
    _old = [{"index": s["index"], "count": s["count"], "pool": s["pool"],
                "unit": sc.most_common(1)[0][0] if sc else None,
                "pts": sc.most_common(1)[0][1] if sc else 0}
               for _i, s, sc in rows]
    print()
    print("-> work/voice/sections.json")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
