"""Extract every Japanese source text the project translates, in one command.

    python tools/extract.py --disc "E:/SRWZ3/PS3_GAME/USRDIR"

Writes `source/`, which is NOT committed, by the same rule the README states:
this repository carries no disc image, no game data and no dump of the Japanese
script. Anyone with their own copy of the game regenerates it from this one
command, so the published repo stays a toolchain plus translations and the
source of truth stays the disc.

Stages need unsdat.py, which drives RPCS3's decryptor: close RPCS3 first, it is
single-instance. Everything else reads the disc directly. A step that cannot
run reports and is skipped; the rest still produce output.

Output is UTF-8 JSON with stable ordering, so a re-extract diffs cleanly:

    source/stages/<STG>_<member>.json   dialogue records: event, n, pid, jp, sha
    source/rpw/names.json               all j-strings, with the chunks using them
    source/rpw/weapons.json             weapon names by record, with owning unit
    source/library/{keywords,pilots,robots}.json
    source/keyword_def.json             MTV_ALL_KEYWORD_DEF entries
    source/voice/sections.json          every voice section, with line counts
    source/voice/<nnn>.json             per section: index, jp, byte budget
    source/MANIFEST.json                what ran, and what failed
"""
import argparse
import collections
import io
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DISC = {
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
    "CMN.CPK": "DATA/BTLC",
    "MTZKN_KW.CPK": "COMMONDATA/MTDATA",
    "MTZKN_PT.CPK": "COMMONDATA/MTDATA",
    "MTZKN_RT.CPK": "COMMONDATA/MTDATA",
    "MTV_ALL_KEYWORD_DEF.CPK": "COMMONDATA/MTDATA",
    "RPW_DATA.CPK": "COMMONDATA/MTDATA",
}

NUL = bytes((0,))


DISC.update({'STG0500.SDAT':'DATA/STAGE', 'STG0700.SDAT':'DATA/STAGE',
             'TROPHY.TRP':'../TROPDIR/NPWR05207_00'})

class Source(object):
    """Where the untouched game files come from.

    This matters more than it looks. `deploy.py` writes the English build over
    the extracted disc, so after the first deploy the disc is NOT a source any
    more -- reading RPW_DATA from it yields VWF cell codes that are not legal
    cp932, and the old failure mode was a bare codec error 200 lines deep.

    Order of preference: an explicit pristine cache, then an ISO (always
    untouched), then the disc. Whatever is found is copied into the cache, so
    a project that deploys once can still re-extract forever.
    """

    def __init__(self, disc=None, iso=None, cache="work/orig"):
        self.disc, self.iso, self.cache = disc, iso, cache
        self._iso = None
        os.makedirs(cache, exist_ok=True)

    def path(self, name):
        cached = os.path.join(self.cache, name)
        if os.path.exists(cached):
            return cached
        if self.iso:
            if self._iso is None:
                import isoread
                self._iso = isoread.ISO9660(self.iso)
            for ent in self._iso.walk():
                if ent[0].upper().endswith("/" + name.upper()):
                    with open(cached, "wb") as fh:
                        fh.write(self._iso.read(ent))
                    return cached
        if self.disc:
            live = os.path.join(self.disc, DISC[name], name)
            if os.path.exists(live):
                import shutil
                shutil.copy2(live, cached)
                return cached
        raise SystemExit("cannot find %s -- pass --iso, or --disc pointing at "
                         "an UNDEPLOYED copy" % name)


def patched(name, err):
    return SystemExit(chr(10).join([
        "%s does not read as Japanese (%s)." % (name, str(err)[:60]),
        "That is what an already-deployed file looks like: deploy.py has "
        "overwritten it with the English build.",
        "Delete work/orig/%s and re-run with --iso, or point --disc at a "
        "pristine copy." % name]))


def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
    return path


def do_stages(S, out, work, rpcs3, log):
    import unsdat
    import luarec
    from cpk import CPK
    dec = os.path.join(work, "stage_dec")
    os.makedirs(dec, exist_ok=True)
    made = []
    for name in sorted(n for n in DISC if n.endswith(".SDAT")):
        # unsdat names its output <stem>.cpk; the .SDAT beside it is still the
        # encrypted original, and feeding that to CPK() gives "not a CPK"
        plain = os.path.join(dec, name[:-5] + ".cpk")
        if not os.path.exists(plain):
            try:
                unsdat.main([S.path(name), dec, "--rpcs3", rpcs3])
            except SystemExit:
                pass
            except Exception as e:
                log("  %s: decrypt failed (%s)" % (name, str(e)[:60]))
        if not os.path.exists(plain):
            log("  %s: not decrypted -- is RPCS3 closed? skipped" % name)
            continue
        k = CPK(plain)
        for i, f in enumerate(k.files):
            try:
                text = k.read(f).decode("cp932")
            except Exception:
                continue
            recs = luarec.records(text)
            if recs:
                made.append(write(os.path.join(
                    out, "stages", "%s_%05d.json" % (name[:-5], i)), recs))
    return made


def do_rpw(S, out, log):
    import rpw
    from cpk import CPK
    k = CPK(S.path("RPW_DATA.CPK"))
    raw = k.read(k.files[0])
    try:
        js = rpw.jstrings(raw)
    except UnicodeDecodeError as e:
        raise patched("RPW_DATA.CPK", e)
    owner = collections.defaultdict(set)
    for (chunk, _r, _c), i in rpw.slots(raw).items():
        owner[i].add(chunk)
    names = [{"i": i, "jp": t, "chunks": sorted(owner.get(i, ()))}
             for i, t in enumerate(js) if t.strip()]
    made = [write(os.path.join(out, "rpw", "names.json"), names)]

    starts, _ = rpw._starts(raw)
    at = {o: i for i, o in enumerate(starts)}
    ch = {c[0]: c for c in rpw.chunks(raw)}
    cols = rpw.pointer_columns(raw)
    stride, _p = cols["weapon"]
    base, end = ch["weapon"][2], ch["weapon"][3]
    nrec = ((end - base) // 4) // stride

    c = ch["wpn-1r"]
    v = [struct.unpack_from("<I", raw, c[2] + 4 * i)[0]
         for i in range((c[3] - c[2]) // 4)]
    unit_of = {}
    for t in range(0, len(v) - 2, 3):
        uid, cnt, first = v[t], v[t + 1], v[t + 2]
        for r in range(first, first + cnt):
            unit_of[r] = uid

    rs, rp = cols["robot"]
    rb = ch["robot"][2]
    rn = ((ch["robot"][3] - rb) // 4) // rs
    uname = {}
    for r in range(rn):
        uid = struct.unpack_from("<I", raw, rb + 4 * (r * rs + 4))[0]
        for p in rp:
            i = at.get(struct.unpack_from("<I", raw, rb + 4 * (r * rs + p))[0])
            if i is not None and js[i].strip():
                uname.setdefault(uid, js[i])
                break

    weps = []
    for r in range(nrec):
        row = {"rec": r, "unit": uname.get(unit_of.get(r))}
        for label, col in (("short", 3), ("long", 4)):
            i = at.get(struct.unpack_from(
                "<I", raw, base + 4 * (r * stride + col))[0])
            row[label] = js[i] if i is not None else None
        if row["short"] or row["long"]:
            weps.append(row)
    made.append(write(os.path.join(out, "rpw", "weapons.json"), weps))
    return made


def do_library(S, out, log):
    import zukan
    from cpk import CPK
    made = []
    for name, label in (("MTZKN_KW.CPK", "keywords"),
                        ("MTZKN_PT.CPK", "pilots"),
                        ("MTZKN_RT.CPK", "robots")):
        k = CPK(S.path(name))
        ents = []
        for i, f in enumerate(k.files):
            try:
                _magic, fields = zukan.parse_ordered(k.read(f))
            except Exception:
                continue
            d = {"i": i}
            for tag, payload in fields:
                try:
                    d[tag] = payload.split(NUL)[0].decode("cp932")
                except Exception:
                    pass
            ents.append(d)
        made.append(write(os.path.join(out, "library", "%s.json" % label), ents))
    return made


def do_keyword_def(S, out, log):
    import mtfl
    from cpk import CPK
    k = CPK(S.path("MTV_ALL_KEYWORD_DEF.CPK"))
    raw = k.read(k.files[0])
    for fn in ("entries", "parse", "read"):
        f = getattr(mtfl, fn, None)
        if not f:
            continue
        try:
            return [write(os.path.join(out, "keyword_def.json"), f(raw))]
        except Exception:
            continue
    log("  keyword_def: no reader in mtfl.py accepted the member")
    return []


def do_voice(S, out, log):
    import srvc_link
    b = open(S.path("SRVC.BIN"), "rb").read()
    secs = srvc_link.sections(b)
    made, table = [], []
    for si, sec in enumerate(secs):
        lines, seen = [], set()
        for i in range(sec["count"]):
            v = struct.unpack_from("<I", b, sec["index"] + 4 * i)[0]
            p = sec["pool"] + v
            e = b.find(NUL, p)
            if e < 0:
                continue
            try:
                jp = b[p:e].decode("cp932")
            except Exception:
                continue
            lines.append({"i": i, "jp": jp, "shared": p in seen,
                          "budget": (e - p) // 2 - 2})
            seen.add(p)
        made.append(write(os.path.join(out, "voice", "%03d.json" % si), lines))
        table.append({"sec": si, "index": sec["index"], "pool": sec["pool"],
                      "count": sec["count"], "distinct": len(seen)})
    made.append(write(os.path.join(out, "voice", "sections.json"), table))
    return made


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--disc", help="path to PS3_GAME/USRDIR (must be UNDEPLOYED)")
    ap.add_argument("--iso", help="path to the disc image (always pristine)")
    ap.add_argument("--out", default="source")
    ap.add_argument("--work", default="work")
    ap.add_argument("--rpcs3", default=r"D:\RPCS3\rpcs3.exe")
    ap.add_argument("--skip", default="", help="comma-separated step names")
    a = ap.parse_args(argv[1:])
    if not a.disc and not a.iso:
        ap.error("give --disc or --iso")
    S = Source(a.disc, a.iso)
    skip = {s.strip() for s in a.skip.split(",") if s.strip()}

    def log(m):
        print(m)

    steps = [
        ("battle_ui", lambda: [S.path("CMN.CPK")]),
        ("stages", lambda: do_stages(S, a.out, a.work, a.rpcs3, log)),
        ("rpw", lambda: do_rpw(S, a.out, log)),
        ("library", lambda: do_library(S, a.out, log)),
        ("keyword_def", lambda: do_keyword_def(S, a.out, log)),
        ("voice", lambda: do_voice(S, a.out, log)),
    ]
    manifest, failed = {}, []
    for name, fn in steps:
        if name in skip:
            print("%-12s skipped" % name)
            continue
        try:
            made = fn()
            manifest[name] = [os.path.relpath(p).replace(chr(92), "/")
                              for p in made]
            print("%-12s %d files" % (name, len(made)))
        except Exception as e:
            failed.append(name)
            print("%-12s FAILED: %s" % (name, str(e)[:90]))
    write(os.path.join(a.out, "MANIFEST.json"),
          {"disc": a.disc, "iso": a.iso, "steps": manifest,
           "failed": failed})
    print("-> %s/   (regenerate any time; never committed)" % a.out)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
