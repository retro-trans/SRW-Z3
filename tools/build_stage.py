"""Build a translated stage end to end: atlas + CPK + SDAT.

Chains every proven step so a rebuild is one command instead of five manual
ones, each of which has a trap documented in docs/WRITEBACK.md:

    lua + translation -> digraph-encoded lua      (tools/patch_lua.py)
    TPACK             -> atlas with the pairs     (both pages)
    stage cpk         -> member replaced          (tools/cpkpatch.py)
    cpk               -> SDAT, make_npdata **v2** (v3/v4 are rejected in-game)

    python tools/build_stage.py <stage.cpk> <member-id> <lua> <translation.py> \
        <TPACK.CPK> <outdir> [--npdata make_npdata.exe]
"""
import json
import os
import struct
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK              # noqa: E402
import cpkpatch                  # noqa: E402
import digraph as dg             # noqa: E402
import patch_lua                 # noqa: E402


def build_atlas(src, dst, mapping, lib_mapping=None):
    """Draw dialogue pairs, and optionally a DISJOINT set of library pairs at
    the library's tighter geometry, into the same two atlas pages."""
    cpk = CPK(src)
    reps, tmp = {}, []
    for e in cpk.files:
        b = cpk.read(e)
        if 5 <= e['id'] <= 128 and dg.LETTER_FACE is not None:
            import scenario_title
            patched = scenario_title.title_apply(b, dg.LETTER_FACE.path, e['id'])
            scenario_title.verify_title(b, patched, dg.LETTER_FACE.path, e['id'])
            p = dst + '.m' + str(e['id'])
            open(p, 'wb').write(patched)
            reps[e['id']] = p
            tmp.append(p)
            continue
        if e['id'] == 2 and dg.LETTER_FACE is not None:
            import support_badge
            patched = support_badge.apply(b, dg.LETTER_FACE.path)
            support_badge.verify(b, patched, dg.LETTER_FACE.path)
            p = dst + '.m2'
            open(p, 'wb').write(patched)
            reps[e['id']] = p
            tmp.append(p)
            continue
        if len(b) < 0x80 or b[0x18] != dg.ATLAS_FORMAT:
            continue
        buf = bytearray(b)
        w = struct.unpack_from(">H", buf, 0x20)[0]
        for key, code in mapping.items():
            if isinstance(key, str):            # VWF: one letter, natural width
                dg.put_cell(buf, w, dg.cell_index(code), dg.raster_letter(key)[0])
            else:
                dg.put_cell(buf, w, dg.cell_index(code), dg.raster_pair(*key))
        for (a, bc), code in (lib_mapping or {}).items():
            dg.put_cell(buf, w, dg.cell_index(code),
                        dg.raster_pair(a, bc, dg.LIBRARY_GEOMETRY))
        if dg.LETTER_FACE is not None:          # VWF builds: tiny one-cell UI words
            taken = set(mapping.values()) | set((lib_mapping or {}).values())
            for text, code in dg.TINY_CELLS.values():
                if code in taken:
                    raise SystemExit("tiny cell %#x (%s) is a letter cell this build" % (code, text))
                dg.put_cell(buf, w, dg.cell_index(code), dg.raster_tiny(text, code))
        p = dst + ".m%d" % e["id"]
        open(p, "wb").write(bytes(buf))
        reps[e["id"]] = p
        tmp.append(p)
    if not reps:
        raise SystemExit("no atlas members in %s" % src)
    n, size = cpkpatch.build(src, dst, reps)
    for p in tmp:
        os.remove(p)
    return len(reps), size


def main(argv):
    if len(argv) < 7:
        print(__doc__.strip())
        return 2
    stage_cpk, member, lua, trans, tpack, outdir = argv[1:7]
    member = int(member)
    npdata = argv[argv.index("--npdata") + 1] if "--npdata" in argv else "make_npdata.exe"
    npdata = os.path.abspath(npdata)
    os.makedirs(outdir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    metrics = os.path.join(here, "..", "work", "atlas", "metrics.json")

    lines = patch_lua.load_translation(trans)
    mapping = patch_lua.build_mapping(lines, metrics)
    print("[1/4] %d records, %d pairs" % (len(lines), len(mapping)))

    en_lua = os.path.join(outdir, "member%d_en.lua" % member)
    open(en_lua, "wb").write(
        patch_lua.patch(open(lua, "rb").read(), lines, mapping))
    json.dump({"%s%s" % k: v for k, v in mapping.items()},
              open(os.path.join(outdir, "pairs.json"), "w"), indent=1)

    out_tpack = os.path.join(outdir, "TPACKPS3.CPK")
    n, size = build_atlas(tpack, out_tpack, mapping)
    print("[2/4] atlas: %d pages patched -> %s (%d B)" % (n, out_tpack, size))

    out_cpk = os.path.join(outdir, "stage.cpk")
    cnt, csize = cpkpatch.build(stage_cpk, out_cpk, {member: en_lua})
    print("[3/4] stage cpk: %d members -> %s (%d B)" % (cnt, out_cpk, csize))

    out_sdat = os.path.join(outdir, "stage.SDAT")
    # version 2 on purpose: the originals are v4 but v3/v4 output is rejected
    r = subprocess.run([npdata, "-e", out_cpk, out_sdat,
                        "2", "0", "00", "1", "16", "0", "", "0"],
                       capture_output=True, text=True)
    if not os.path.exists(out_sdat):
        print(r.stdout[-800:])
        raise SystemExit("make_npdata failed")
    print("[4/4] sdat -> %s (%d B)" % (out_sdat, os.path.getsize(out_sdat)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
