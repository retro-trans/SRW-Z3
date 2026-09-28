"""Build every translated stage against ONE shared font atlas.

This has to be project-wide, not per-stage. The atlas is a single global file,
so if each stage picked its own codes independently, building the second one
would silently break the first. Every translation module is therefore pooled
into one mapping before anything is written.

Manifest is a python file exposing STAGES:

    STAGES = [
      {"cpk": "...STG0001A.cpk", "sdat": "STG0001A.SDAT",
       "members": [{"id": 4, "lua": "...", "trans": "translation/x.py"}]},
    ]

    python tools/build_project.py <manifest.py> <TPACK.CPK> <outdir> [--npdata p]
"""
import importlib.util
import collections
import json
import os
import struct
import subprocess
import sys
import hashlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK              # noqa: E402
import cpkpatch                  # noqa: E402
import digraph as dg             # noqa: E402
import patch_lua as pl           # noqa: E402
from build_stage import build_atlas   # noqa: E402
import build_library as blib         # noqa: E402
import trdata                        # noqa: E402
import mtfl                          # noqa: E402
import reserved as rsv               # noqa: E402
import rpw                           # noqa: E402
import eboot                         # noqa: E402


def load_mod(path):
    spec = importlib.util.spec_from_file_location("m_" + os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load(path, attr):
    """LINES / ENTRIES come from JSON translation files, parsed not executed.
    The manifest stays a Python module: it is hand-written build config, not
    content, and is loaded by load_mod()."""
    if path.endswith(".json"):
        if attr == "LINES":
            return trdata.records(path)      # patch_lua binds on identity
        return trdata.entries(path)
    if attr == "ENTRIES":                       # library_kw.py shim -> assembled
        return getattr(load_mod(path), "ENTRIES")
    return getattr(load_mod(path), attr)


def load_labels():
    """translation/spirits.json + skills.json: {jp: en}, keys starting with
    '_' are notes. Spirit command and pilot skill names, swapped in RPW and
    hooked in the EBOOT alongside weapons."""
    out = {}
    for f in ("spirits.json", "skills.json", "parts.json"):
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "translation", f)
        if os.path.exists(p):
            out.update({k: v for k, v in json.load(open(p, encoding="utf-8")).items()
                        if not k.startswith("_") and v})
    return out


def write_build_manifest(outdir, expected_version):
    """Record the complete validated set so deployment can detect mixed files."""
    from deploy import LAYOUT
    files = {}
    for name in list(LAYOUT) + ['pairs.json', 'pairs_lib.json', 'widths.json']:
        path = os.path.join(outdir, name)
        with open(path, 'rb') as stream:
            data = stream.read()
        files[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    import build_version
    coverage = json.load(open(os.path.join(outdir, 'message_coverage.json'), encoding='utf-8'))
    coverage_path = os.path.join(outdir, 'message_coverage.json')
    with open(coverage_path, 'rb') as stream:
        coverage_data = stream.read()
    files['message_coverage.json'] = {'bytes': len(coverage_data), 'sha256': hashlib.sha256(coverage_data).hexdigest()}
    import shared_content
    version = build_version.stamp(outdir, {'schema': 1, 'ui_regression_checks': True,
                                  'platform': 'ps3',
                                  'shared_content': shared_content.revision(),
                                  'translation_complete': coverage['complete'],
                                  'untranslated_mission_variants': coverage['missing_count'],
                                  'title_footer_version': expected_version, 'files': files},
                                  expected_version=expected_version)
    print('  [build] successful build %s' % version)


def main(argv):
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    manifest, tpack, outdir = argv[1], argv[2], argv[3]
    import localization
    localization.ensure_compatible()
    if '--dry-run' in argv:
        # Input preflight only: never create/remove an output or reserve a
        # version. Full binary/layout validation still runs during the build.
        from pathlib import Path
        import build_version
        if Path(outdir).exists():
            raise SystemExit('Dry-run requires a NEW output directory')
        paths = [manifest, tpack, 'analysis/glossary.json']
        for flag in ('--npdata', '--eboot', '--ttf'):
            if flag in argv:
                paths.append(argv[argv.index(flag) + 1].split(',')[0])
        config = load_mod(manifest)
        for stage in config.STAGES:
            paths.append(stage['cpk'])
            for member in stage['members']:
                paths.extend((member['lua'], member['trans']))
        for library in getattr(config, 'LIBRARIES', []):
            paths.extend((library['cpk'], library['trans']))
        missing = [p for p in paths if not Path(p).is_file()]
        if missing:
            raise SystemExit('Missing build inputs: ' + ', '.join(missing))
        trdata.use_glossary('analysis/glossary.json')
        count = sum(len(load(m['trans'], 'LINES')) for s in config.STAGES
                    for m in s['members'])
        for library in getattr(config, 'LIBRARIES', []):
            load(library['trans'], 'ENTRIES')
        print('DRY RUN: %d stage containers, %d dialogue records, %d checked paths'
              % (len(config.STAGES), count, len(paths)))
        print('Next successful build: %s; output: %s' % (build_version.next_version(), outdir))
        print('Partial translation allowed: %s' % ('--partial-translation' in argv))
        print('No output, counter, installation or release modified.')
        return 0
    npdata = os.path.abspath(
        argv[argv.index("--npdata") + 1] if "--npdata" in argv else "make_npdata.exe")
    if "--metrics" in argv:
        cap, base = (float(x) for x in argv[argv.index("--metrics") + 1].split(","))
        dg.set_metrics(cap, base)          # scripts that stack marks need room
    use_kanji = "--kanji" in argv
    vwf = "--vwf" in argv
    # The footer needs its number before rendering; numbering at the end
    # checks this expectation under the exclusive lock. A concurrent build
    # can never silently publish a different number from the visible footer.
    import build_version
    title_version = build_version.next_version() if vwf and '--eboot' in argv else None
    if vwf:
        # one letter per cell at natural width; the EBOOT advance patch reads
        # a per-cell width table (tools/eboot.py). Needs a TTF for the letters.
        if "--ttf" not in argv:
            raise SystemExit("--vwf needs --ttf <font>")
        spec = argv[argv.index("--ttf") + 1].split(",")
        cap = float(spec[1]) if len(spec) > 1 else 22.0
        dg.use_letters(spec[0], cap=cap, dilate=float(spec[2]) if len(spec) > 2 else 0.5)
        print("[font]  %s  one letter per cell, cap %.0f, variable width" % (os.path.basename(spec[0]), cap))
    elif "--ttf" in argv:
        # bake a real typeface into the cells: path[,cap,cap_lib,dilate]
        spec = argv[argv.index("--ttf") + 1].split(",")
        nums = [float(x) for x in spec[1:]] + [23.0, 19.0, 1.5][len(spec) - 1:]
        dg.use_ttf(spec[0], cap=nums[0], cap_lib=nums[1], dilate=nums[2])
        print("[font]  %s  cap %.0f / library %.0f, stems +%.1f" % (os.path.basename(spec[0]), *nums[:3]))
    os.makedirs(outdir, exist_ok=True)
    # A failed rebuild must not leave an older success certificate behind.
    old_manifest = os.path.join(outdir, 'build_manifest.json')
    if os.path.exists(old_manifest):
        os.remove(old_manifest)
    here = os.path.dirname(os.path.abspath(__file__))
    metrics = os.path.join(here, "..", "work", "atlas", "metrics.json")
    stages = load(manifest, "STAGES")
    # Prose refers to glossary terms as `$$id$$` (tools/terms.py). Every
    # reader in trdata expands them, so this must happen before the first
    # translation file is opened -- an unexpanded token would reach the
    # screen verbatim, and trdata refuses to guess rather than let it.
    gpath = os.path.join(here, "..", "analysis", "glossary.json")
    print("[terms] %d glossary terms addressable as $$id$$"
          % trdata.use_glossary(gpath))
    # the same index, for readers that do not go through trdata
    import terms as _T
    term_idx = _T.index(json.load(open(gpath, encoding="utf-8")))

    # --- one pooled mapping across every stage ---
    allpairs = []

    def _add(text):
        if vwf and "《" in text:
            # link LINES stay on width-32 pair cells (see digraph.encode_hybrid)
            for p in dg.hybrid_units(text):
                if p not in allpairs:
                    allpairs.append(p)
            return
        for p in dg.mixed_pairs(text):
            if p not in allpairs:
                allpairs.append(p)

    # A few UI slots are far too small for VWF, where every letter costs a
    # 2-byte cell. A PAIR cell packs two letters into the same 2 bytes, which
    # is the only way "Nick" fits 愛称's six bytes. Allocate cells for those
    # pairs even though the rest of the build is letters; build_atlas already
    # draws a tuple key as a pair and a str key as a letter.
    tightp = "translation/ui_tight.json"
    if os.path.exists(tightp):
        tight = json.load(open(tightp, encoding="utf-8"))
        for row in tight["lines"]:
            for pr in dg.pairs_of(row["en"]):
                if pr not in allpairs:
                    allpairs.append(pr)
        print("[tight] %d pair cells for slots too small for letters"
              % len(set(pr for row in tight["lines"] for pr in dg.pairs_of(row["en"]))))

    for st in stages:
        for mem in st["members"]:
            for block in load(mem["trans"], "LINES"):
                _add(block["en"] if isinstance(block, dict) else block)
    # STG0700's end-session scenes are an ordinary manifest stage now (its
    # lines are pooled above); suspend_scene.py only serves frozen builds.
    # The atlas is global, so library text has to share the same mapping as the
    # script. Names come from the glossary; descriptions from the batch modules.
    libs = load(manifest, "LIBRARIES") if hasattr(
        load_mod(manifest), "LIBRARIES") else []
    gl = json.load(open(gpath, encoding="utf-8"))
    for t in gl["terms"]:
        if t["en"]:
            _add(t["en"])
    # The library draws the same cells 1.29x larger at the same advance, so
    # its pairs need a tighter in-cell geometry. They therefore live in their
    # OWN cells, disjoint from dialogue's, and get their own mapping.
    libpairs = []

    def _addlib(text):
        if vwf:                     # letters: one mapping for everything but RPW
            _add(text)
            return
        for p in dg.mixed_pairs(text):
            if p not in libpairs:
                libpairs.append(p)

    # Narration lives in fixed 84-byte slots in a sibling CPK member, not in
    # the Lua, so it needs its letters pooled like everything else.
    narr = []
    for st in load(manifest, "STAGES"):
        cand = "translation/narration_%s.json" % (
            os.path.basename(st["sdat"])[3:-5].lower())
        if os.path.exists(cand):
            doc = json.load(open(cand, encoding="utf-8"))
            narr.append((st, cand, doc))
            for row in doc["lines"]:
                _add(row.get("expanded") or row["en"])
    if narr:
        print("[narr]  %d containers, %d lines"
              % (len(narr), sum(len(d["lines"]) for _s, _c, d in narr)))

    for lib in libs:
        # pool the EXACT strings the library build will encode, brackets and
        # wrapping included -- padding is context sensitive
        for t in blib.collect_texts(lib["cpk"], gl, load(lib["trans"], "ENTRIES")):
            _addlib(t)
    for t in gl["terms"]:
        if t["en"]:
            _addlib(t["en"])
            _addlib("「%s」" % t["en"])
    # Never take a cell the game still draws in Japanese: UI labels (愛称,
    # 声優, 登場作品...), voice-actor names, any untouched field. Taking one
    # turned 愛称 into 愛-v on screen. The set is computed from the same files
    # being translated, so it is exact (346 codes), not a guess.
    tr_ents = {os.path.basename(l["cpk"])[:-4]: load(l["trans"], "ENTRIES") for l in libs}
    # RPW_DATA: every settled glossary name ships. Names that fit their slot are
    # swapped in place; names too long are APPENDED to the end of the string
    # body and their pilot-nw pointers repointed there (rpw.build_grown) -- no
    # existing offset moves, so the crash class from shifting is avoided. All
    # names are drawn, so none stay reserved. RPW is on VWF letters like
    # everything else; a name that does not fit its slot is appended.
    rpw_src = os.path.join(os.path.dirname(libs[0]["cpk"]), "RPW_DATA.CPK") if libs else None
    rpw_swap = None
    if rpw_src and os.path.exists(rpw_src):
        names = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
        # Weapon and attack names are not glossary terms -- they are labels,
        # not referable terminology -- but they live in the same j-string
        # body and swap through the same plan. The glossary wins any
        # collision: a string that is BOTH a settled term and a weapon name
        # must read the same everywhere it appears.
        wp = "translation/weapons.json"
        if os.path.exists(wp):
            weps = json.load(open(wp, encoding="utf-8"))
            clash = [k for k in weps if k in names and names[k] != weps[k]]
            for k in clash:
                print("  [rpw]   glossary wins over weapons.json for %s (%s, not %s)"
                      % (k, names[k], weps[k]))
            names = dict(weps, **names)
            print("  [rpw]   +%d weapon and attack names" % len(weps))
        # Spirit command and pilot skill names: labels in the same j-string
        # body (chunks 'spirit' and 'sk-pri'). Below weapons in precedence:
        # the table is deduplicated, so 突撃 the weapon and 突撃 the spirit
        # are one string.
        labels = load_labels()
        names = dict(labels, **names)
        print("  [rpw]   +%d spirit, skill and part strings" % len(labels))
        # Family / given name pieces (translation/name_pieces.json): lowest
        # precedence, and only the ones whose English is the same for everyone.
        pp = "translation/name_pieces.json"
        if os.path.exists(pp):
            pieces = {k: v for k, v in json.load(open(pp, encoding="utf-8")).items()
                      if not k.startswith("_") and v}
            names = dict(pieces, **names)
            print("  [rpw]   +%d unambiguous name pieces" % len(pieces))
        # Generic enemy / bit-part nameplate names (translation/enemy_names.json):
        # the anonymous grunts the battle nameplate draws -- ネオ・ジオン兵,
        # 高性能ＡＩ and the like. Same lowest precedence as the pieces: a
        # glossary character always wins.
        ep = "translation/enemy_names.json"
        if os.path.exists(ep):
            foes = {k: v for k, v in json.load(open(ep, encoding="utf-8")).items()
                    if not k.startswith("_") and v}
            names = dict(foes, **names)
            print("  [rpw]   +%d generic enemy names" % len(foes))
        rk = CPK(rpw_src); rraw = rk.read(rk.files[0]); js = rpw.jstrings(rraw)
        rpw_swap = {}
        for i, en in rpw.plan_all(js, names).items():
            try:
                dg.encode_mixed(en, collections.defaultdict(int), newline=bytes((10,)))
            except SystemExit:
                continue                      # undrawable char -> leave Japanese
            rpw_swap[i] = en
        if vwf and '--eboot' in argv:
            import battle_name_rendering
            if not eboot.NAME_ENABLE:
                raise SystemExit('Deferred battle names require the draw-time name hook')
            for en in battle_name_rendering.hooks().values():
                _add(en)
            rpw_swap = battle_name_rendering.defer_swaps(rraw, rpw_swap)
        # VWF letters, not pair cells. RPW names had to fit the Japanese
        # byte slot in place, and a pair packs two letters per 2-byte cell
        # against one per cell for a letter -- under VWF only 36 of 689
        # names still fit. build_grown appends the other 653 and repoints
        # them, which is only safe because the repoint follows derived
        # record columns now. The win: the 713 library pair cells collapse
        # into the 79 shared letter cells, and every name on screen is
        # finally the same proportional face.
        for en in rpw_swap.values():
            _add(en)
        print("[rpw]   %d names to swap (in place where they fit, appended where not)"
              % len(rpw_swap))
    # EBOOT name strings translated in place (character/keyword names the lists
    # draw from the executable, e.g. Hibiki Kamishiro) are PAIR cells too --
    # collect their pairs so the atlas has them.
    if vwf and "--eboot" in argv:
        eb = open(argv[argv.index("--eboot") + 1], "rb").read()
        allnm = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
        # through trdata, so `$$id$$` in a batch NAMES entry is expanded
        # here too -- reading the JSON directly used to bypass that
        import glob as _glob
        for f in sorted(_glob.glob(os.path.join(here, "..", "translation", "library", "*.json"))):
            allnm.update(trdata.names(f))
        eboot.HOOK_ALL_SET = set(allnm)   # weapons/spirits/skills stay RPW-only
        for jp, en in allnm.items():
            try:
                jp.encode("cp932")            # every name is hooked now
                _add(en)                      # (eboot.HOOK_ALL_NAMES); letters, same as RPW
            except Exception:
                pass
    # Battle voice lines need their letters in the SAME pooled mapping: the
    # atlas is global, so a cell code allocated for dialogue is the cell the
    # voice writer encodes against. Collected here, spent at the bottom.
    import glob as _g
    voice_docs = []
    for f in sorted(_g.glob(os.path.join(here, "..", "translation", "voice_*.json"))):
        d = trdata.voice_document(f)
        d["_path"] = f
        voice_docs.append(d)
        for v in d.get("lines", {}).values():
            en = v["en"] if isinstance(v, dict) else v
            if not en:
                continue
            # Split on the literal backslash-n exactly as the encoder does.
            # It is a break the game's text parser consumes, not text: asking
            # the atlas for a backslash cell fails the build outright.
            for part in ("「%s」" % en).split(chr(92) + "n"):
                _add(part)
    if voice_docs:
        print("[voice] %d sections, %d lines to encode"
              % (len(voice_docs), sum(len(d.get("lines", {})) for d in voice_docs)))
    reserved = rsv.reserved(os.path.dirname(libs[0]["cpk"]), gl, tr_ents,
                            rpw_swapped=set(rpw_swap) if rpw_swap is not None else None) if libs else set()
    print("[pairs] %d cells reserved for Japanese still on screen" % len(reserved))
    pool = dg.free_pool(metrics, include_kanji=use_kanji, reserved=reserved)
    if len(allpairs) + len(libpairs) > len(pool):
        raise SystemExit("need %d dialogue + %d library cells, only %d free -- open up more codes"
                         % (len(allpairs), len(libpairs), len(pool)))
    mapping = {p: pool[i] for i, p in enumerate(allpairs)}
    lib_mapping = {p: pool[len(allpairs) + i] for i, p in enumerate(libpairs)}
    print("[pairs] library: %d distinct in their own cells" % len(lib_mapping))
    json.dump({(k if isinstance(k, str) else "%s%s" % k): v for k, v in lib_mapping.items()},
              open(os.path.join(outdir, "pairs_lib.json"), "w"), indent=1)
    print("[pairs] %d distinct across %d stages (%d cells spare%s)"
          % (len(mapping), len(stages), len(pool) - len(mapping),
             ", kanji opened" if use_kanji else ""))
    json.dump({(k if isinstance(k, str) else "%s%s" % k): v for k, v in mapping.items()},
              open(os.path.join(outdir, "pairs.json"), "w"), indent=1)

    out_tpack = os.path.join(outdir, "TPACKPS3.CPK")
    n, size = build_atlas(tpack, out_tpack, mapping, lib_mapping)
    print("[atlas] %d pages -> %s (%d B)" % (n, out_tpack, size))
    tmap = mapping if vwf else lib_mapping     # letters everywhere but RPW

    for st in stages:
        reps = {}
        for mem in st["members"]:
            lines = load(mem["trans"], "LINES")
            data = pl.patch(open(mem["lua"], "rb").read(), lines, mapping)
            p = os.path.join(outdir, "%s.m%d.lua"
                             % (os.path.basename(st["sdat"]), mem["id"]))
            open(p, "wb").write(data)
            reps[mem["id"]] = p
            print("  [lua]  %s member %d: %d records"
                  % (os.path.basename(st["sdat"]), mem["id"], len(lines)))
        for st2, cand, doc in narr:
            # compare by name: `narr` was built from its own load() call, so
            # the dicts are equal in content but not the same objects
            if st2["sdat"] != st["sdat"]:
                continue
            import narration as NA
            k = CPK(st["cpk"])
            mem = doc["member"]
            blob = k.read(k.files[mem])
            new_blob, done = NA.apply(blob, doc["lines"], tmap, idx=term_idx)
            probs = NA.verify(blob, new_blob, done)
            if probs:
                raise SystemExit("narration: %s" % "; ".join(probs))
            np_ = os.path.join(outdir, "%s.m%d.narr"
                               % (os.path.basename(st["sdat"]), mem))
            open(np_, "wb").write(new_blob)
            reps[k.files[mem]["id"]] = np_
            print("  [narr] %s member %d: %d slots, size unchanged"
                  % (os.path.basename(st["sdat"]), mem, len(done)))
        cpk_out = os.path.join(outdir, os.path.basename(st["sdat"]) + ".cpk")
        cnt, csz = cpkpatch.build(st["cpk"], cpk_out, reps)
        sdat = os.path.join(outdir, os.path.basename(st["sdat"]))
        if os.path.exists(sdat):
            os.remove(sdat)
        # version 2: the originals are v4 but v3/v4 output is rejected in-game
        subprocess.run([npdata, "-e", cpk_out, sdat,
                        "2", "0", "00", "1", "16", "0", "", "0"],
                       capture_output=True, text=True)
        if not os.path.exists(sdat):
            raise SystemExit("make_npdata failed for %s" % sdat)
        print("  [sdat] %s  %d members, %d B"
              % (os.path.basename(sdat), cnt, os.path.getsize(sdat)))
        for p in reps.values():
            os.remove(p)

    for lib in libs:
        out = os.path.join(outdir, os.path.basename(lib["cpk"]))
        n = blib.build(lib["cpk"], gl, load(lib["trans"], "ENTRIES"), out, tmap)
        print("  [lib]  %s  %d entries" % (os.path.basename(out), n))

    # The KEYWORD screen does not read MTZKN_KW. It reads
    # COMMONDATA/MTDATA/MTV_ALL_KEYWORD_DEF.CPK, a different container with
    # its own index and obfuscation (tools/mtfl.py). Same 141 entries, same
    # english, same shared pair mapping -- so it is built here, not separately.
    # RPW_DATA.CPK: the game's core string table (j-string chunk). Every
    # j-string that is a settled glossary name -- pilot, unit, series -- is
    # swapped for its English here (689 of 4,565). That is what the 登場作品
    # label and the battle-screen names are drawn from; PRDC is not.
    if rpw_swap is not None:
        # rpw pads in-place slack with the fullwidth space; if this run gave
        # that cell to a Latin pair, the padding would draw letters.
        if 0x8140 in set(lib_mapping.values()) | set(mapping.values()):
            raise SystemExit("0x8140 was allocated as a pair cell; rpw padding needs it")
        # --rpw-limit MODE: a debugging knob for bisecting which swapped
        # j-string breaks the game. inplace = only names that fit their slot,
        # append = only names that do not, first:N / rest:N = a prefix/suffix
        # of the sorted index list, none = ship the file untouched.
        sel = dict(rpw_swap)
        if '--rpw-limit' in argv:
            mode = argv[argv.index('--rpw-limit') + 1]
            fits = {i: (len(dg.encode_mixed(en, tmap, newline=bytes((10,)))) <= len(js[i]))
                    for i, en in rpw_swap.items()}
            keys = sorted(rpw_swap)
            if mode == 'none':
                sel = {}
            elif mode == 'inplace':
                sel = {i: e for i, e in rpw_swap.items() if fits[i]}
            elif mode == 'append':
                sel = {i: e for i, e in rpw_swap.items() if not fits[i]}
            elif mode.startswith('first:'):
                keep = set(keys[:int(mode.split(':')[1])])
                sel = {i: e for i, e in rpw_swap.items() if i in keep}
            elif mode.startswith('rest:'):
                keep = set(keys[int(mode.split(':')[1]):])
                sel = {i: e for i, e in rpw_swap.items() if i in keep}
            else:
                raise SystemExit('unknown --rpw-limit %s' % mode)
            print('  [rpw]   --rpw-limit %s: %d of %d names' % (mode, len(sel), len(rpw_swap)))
        rpw_swap = sel
        enc = {i: dg.encode_mixed(en, tmap, newline=bytes((10,))) for i, en in rpw_swap.items()}
        # Boost-part DESCRIPTIONS (boost-p columns 3-8) must stay Japanese: with any
        # of them swapped the game corrupts memory at boot (black screen, or a bogus
        # "257,604 MB more needed" install message). Bisected 2026-09-04 -- not size,
        # count, length, "%" or the DL variants; see CHANGELOG. Names (columns 1-2)
        # are fine. Refuse rather than let a future parts.json bring them back.
        bp_desc = {i_ for (c_, r_, col_), i_ in rpw.slots(rraw).items() if c_ == "boost-p" and 3 <= col_ <= 8}
        bad_desc = [js[i_][:30] for i_ in bp_desc if i_ in enc]
        if bad_desc:
            raise SystemExit("RPW: %d boost-part descriptions would be swapped -- they corrupt boot; keep them in "
                             "translation/parts_descriptions.unshipped.json: %r" % (len(bad_desc), bad_desc[:3]))
        # A pilot-nw record is (given, surname, display) and the j-string table
        # is deduplicated, so one レイ serves Amuro Ray's SURNAME as well as
        # Ray Lovelock's and Rei Ayanami's given names. These slots get their
        # own appended copy so all three read correctly.
        # Every resolvable pilot record gets its own given / surname English
        # (rpw.piece_overrides); name_overrides keeps precedence for the
        # shared-name slots it already settles.
        ovr, unres = rpw.piece_overrides(rraw, gl["terms"])
        ovr.update(rpw.name_overrides(rraw, gl["terms"]))
        ovr.update(rpw.compound_name_overrides(rraw, gl["terms"]))
        print("  [rpw]   %d name-piece slots per record (%d records unresolved)" % (len(ovr), unres))
        spirit_names = json.load(open(os.path.join(here, "..", "translation", "spirits.json"), encoding="utf-8"))
        spirit_ovr = rpw.spirit_name_overrides(rraw, spirit_names)
        ovr.update(spirit_ovr)
        print("  [rpw]   %d spirit full-name slots use their own terms" % len(spirit_ovr))
        if vwf and '--eboot' in argv:
            ovr = battle_name_rendering.defer_overrides(rraw, ovr)
        ov = {k_: dg.encode_mixed(v, tmap, newline=bytes((10,))) for k_, v in ovr.items()}
        new_raw, appended = rpw.build_grown(rraw, enc, ov)
        rpw.check_compound_names(rraw, new_raw, gl['terms'], tmap)
        if vwf and '--eboot' in argv:
            deferred_count = battle_name_rendering.check_rpw(rraw, new_raw)
            print('  [rpw]   %d long-name slots deferred to the exact draw-time hook' % deferred_count)
        tmp = os.path.join(outdir, "rpw.member"); open(tmp, "wb").write(new_raw)
        out = os.path.join(outdir, "RPW_DATA.CPK")
        cpkpatch.build(rpw_src, out, {rk.files[0]["id"]: tmp}); os.remove(tmp)
        print("  [rpw]   RPW_DATA.CPK  %d/%d names English (%d fit in place, %d appended, "
              "%d shared-name slots split)  (member %d -> %d B)"
              % (len(rpw_swap), len(js), len(rpw_swap) - appended, appended, len(ov),
                 len(rraw), len(new_raw)))

    kwdef = next((l for l in libs if "MTV_ALL_KEYWORD_DEF" in l.get("kwdef", "")), None)
    kwdef_src = os.path.join(os.path.dirname(libs[0]["cpk"]), "MTV_ALL_KEYWORD_DEF.CPK") if libs else None
    if kwdef_src and os.path.exists(kwdef_src):
        kw_lib = next(l for l in libs if "MTZKN_KW" in l["cpk"])
        entries = load(kw_lib["trans"], "ENTRIES")
        names = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
        # Weapon and attack names are not glossary terms -- they are labels,
        # not referable terminology -- but they live in the same j-string
        # body and swap through the same plan. The glossary wins any
        # collision: a string that is BOTH a settled term and a weapon name
        # must read the same everywhere it appears.
        wp = "translation/weapons.json"
        if os.path.exists(wp):
            weps = json.load(open(wp, encoding="utf-8"))
            clash = [k for k in weps if k in names and names[k] != weps[k]]
            for k in clash:
                print("  [rpw]   glossary wins over weapons.json for %s (%s, not %s)"
                      % (k, names[k], weps[k]))
            names = dict(weps, **names)
            print("  [rpw]   +%d weapon and attack names" % len(weps))
        cpk = CPK(kwdef_src); raw = cpk.read(cpk.files[0])
        parsed = mtfl.parse(raw); jp = mtfl.strings(raw, parsed)
        texts = {}
        for eid, rec in jp.items():
            t = {}
            for fld in ("WORD", "SRCE"):
                v = rec[fld]; bare = v.strip("「」")
                en = names.get(bare)
                if en is None:
                    t[fld] = v.encode("cp932")
                else:
                    en = ("「%s」" % en) if v.startswith("「") else en
                    t[fld] = dg.encode_mixed(en, tmap, newline=b"\n")
            e = entries.get(eid, {})
            d1 = e.get("DSCR"); d2 = e.get("DSC2") or d1
            t["DSCR"] = dg.encode_mixed(blib.wrap(d1), tmap, newline=b"\n") if d1 else rec["DSCR"].encode("cp932")
            t["DSC2"] = dg.encode_mixed(blib.wrap(d2), tmap, newline=b"\n") if d2 else rec["DSC2"].encode("cp932")
            texts[eid] = t
        new_raw = mtfl.build(raw, parsed, texts)
        tmp = os.path.join(outdir, "kwdef.member")
        open(tmp, "wb").write(new_raw)
        out = os.path.join(outdir, "MTV_ALL_KEYWORD_DEF.CPK")
        cpkpatch.build(kwdef_src, out, {cpk.files[0]["id"]: tmp}); os.remove(tmp)
        print("  [kwdef] MTV_ALL_KEYWORD_DEF.CPK  %d entries  (%d -> %d B member)" % (len(texts), len(raw), len(new_raw)))
    # Battle voice lines (DATA/BTLC/SRVC.BIN). Encoded HERE, never by a side
    # script: atlas cell codes shift between runs, so English encoded against
    # a stale mapping renders as garbage while everything around it looks
    # right. It also has to be part of the build because running the writer
    # by hand was forgotten once and the voice patch regressed silently for
    # four days -- a build that cannot ship without it cannot repeat that.
    #
    # Rebuilt block by block (tools/srvc_blocks.py): a line may be any
    # length. The game reads each unit's block through a table of block
    # offsets in the EBOOT, so the grown file and the rewritten table ship
    # together -- `--eboot` is required the moment any block moves. The
    # old in-place writer (voice_lib) still supplies the per-section
    # geometry that maps a doc's entry numbers to the strings they name.
    voice_src = os.path.join(here, "..", "work", "srvc", "SRVC.BIN")
    voice_table = None
    if voice_docs and os.path.exists(voice_src):
        import voice_lib as V
        import srvc_blocks as S
        BRK = chr(92) + "n"

        def enc(t):
            # The break is a literal backslash-n the game's text parser
            # consumes -- pass it through raw, never encode the backslash.
            whole = "「" + t + "」"
            return BRK.encode("ascii").join(
                dg.encode_mixed(part, tmap, newline=bytes((10,)))
                for part in whole.split(BRK))

        if "--eboot" not in argv:
            raise SystemExit("[voice] SRVC.BIN is rebuilt with grown blocks; its offset table lives in the EBOOT -- pass --eboot")
        pristine = open(voice_src, "rb").read()
        elf0 = open(argv[argv.index("--eboot") + 1], "rb").read()
        vtab = S.read_table(elf0)
        vtab_geo = V.table()
        repl, owner = {}, {}
        for doc in voice_docs:
            index, count, pool, limit = V.geometry(doc, vtab_geo)
            sec = doc.get("section")
            V.prove(pristine, index, count, pool, limit, sec)
            words = V.index_words(pristine, index, count)
            for k, v in doc.get("lines", {}).items():
                en = v["en"] if isinstance(v, dict) else v
                if not en:
                    continue
                n = int(k)
                if not 0 <= n < count:
                    raise SystemExit("[voice] section %s: entry %d is outside the section" % (sec, n))
                off = pool + words[n]
                jp = v.get("jp") if isinstance(v, dict) else None
                have = S.string_at(pristine, off).decode("cp932", "replace")
                if jp and have != jp:
                    raise SystemExit("[voice] section %s entry %d: the file holds %r, the doc says %r -- stale doc, re-run extract.py" % (sec, n, have, jp))
                data = enc(en)
                prev = repl.get(off)
                if prev is not None and prev != data:
                    raise SystemExit("[voice] section %s entry %d shares its string with entry %d (%s) but the English differs" % (sec, n, owner[off][1], owner[off][0]))
                repl[off] = data
                owner[off] = (sec, n)
        vnew, vtab_new, vrep = S.rebuild(pristine, vtab, repl)
        for pr in S.verify(vnew, vtab_new, pristine, vtab, repl):
            raise SystemExit("[voice] %s" % pr)
        open(os.path.join(outdir, "SRVC.BIN"), "wb").write(vnew)
        voice_table = (vtab, vtab_new)
        grown = sum(1 for _i, o, n, _h in vrep if n > o)
        print("  [voice] SRVC.BIN  %d lines in %d sections, %d blocks rebuilt (%d grew), %d -> %d B; EBOOT block table %s"
              % (len(repl), len(voice_docs), len(vrep), grown, len(pristine), len(vnew),
                 "unchanged" if vtab_new == vtab else "rewritten"))
    elif os.path.exists(voice_src):
        # No translated section yet: ship the file pristine rather than not
        # at all, so the deploy set stays complete.
        open(os.path.join(outdir, "SRVC.BIN"), "wb").write(open(voice_src, "rb").read())

    # The 登場作品 label is a string table in the executable; its English is
    # encoded with THIS run's library cells, so it is built here, never apart.
    if "--eboot" in argv:
        elf = open(argv[argv.index("--eboot") + 1], "rb").read()
        names = {t["jp"]: t["en"] for t in gl["terms"] if t["en"]}
        # Weapon and attack names are not glossary terms -- they are labels,
        # not referable terminology -- but they live in the same j-string
        # body and swap through the same plan. The glossary wins any
        # collision: a string that is BOTH a settled term and a weapon name
        # must read the same everywhere it appears.
        wp = "translation/weapons.json"
        if os.path.exists(wp):
            weps = json.load(open(wp, encoding="utf-8"))
            clash = [k for k in weps if k in names and names[k] != weps[k]]
            for k in clash:
                print("  [rpw]   glossary wins over weapons.json for %s (%s, not %s)"
                      % (k, names[k], weps[k]))
            names = dict(weps, **names)
            print("  [rpw]   +%d weapon and attack names" % len(weps))
        names = dict(load_labels(), **names)      # spirit and skill names, hooked too
        # the 用語事典 list draws the 141 keyword names from the same EBOOT table
        names.update(trdata.assemble(os.path.join(here, "..", "translation", "library"), "kw",
                                     trdata.ambiguous_terms(os.path.join(here, "..", "analysis", "glossary.json")))[1])
        used = set(mapping.values()) | set(lib_mapping.values())
        widths = None
        if vwf:
            widths = {dg.cell_index(code): dg.letter_width(ch) for ch, code in mapping.items() if isinstance(ch, str)}
            json.dump({str(k): v for k, v in widths.items()}, open(os.path.join(outdir, "widths.json"), "w"), indent=1)
        new_elf, rep_ = eboot.patch(elf, names, tmap, used, widths, pair_mapping=lib_mapping)
        if rep_.get("hook") and rep_["hook"][1]:
            raise SystemExit("[eboot] refusing incomplete build: undrawable translation hooks")
        n = eboot.verify(elf, new_elf, names, tmap, rep_["vwf"])
        if rep_.get("inplace"):
            print("  [eboot] %d EBOOT names translated in place (%d too long, %d undrawable, %d lookup-keyed stay Japanese)" % rep_["inplace"])
        if rep_.get("ui"):
            n_ui, skipped, _cur = rep_["ui"]
            print("  [eboot] %d menu labels repointed%s"
                  % (n_ui, "" if not skipped else
                     "; skipped " + ", ".join("%#x (%s)" % x for x in skipped)))
        if rep_.get("hook"):
            print("  [eboot] draw-time hook: %d strings, %d of them UI labels (translation/ui_hook.json), %d undrawable"
                  % (rep_["hook"][0], rep_["hook"][3], rep_["hook"][1]))
        if rep_.get("commands"):
            c_in, c_rp, c_stay = rep_["commands"][:3]
            print("  [eboot] COMMAND menu: %d labels in place, %d repointed into the gap, face %s, %d centring pads%s"
                  % (c_in, c_rp, "VWF cells via U+%04X.." % eboot.VWF_CP_BASE if rep_["commands"][4] else "ASCII",
                     rep_["commands"][5],
                     "" if not c_stay else
                     "; still Japanese: " + ", ".join("%s (%s)" % x for x in c_stay)))
        if rep_.get("utf8"):
            u_in, u_rp, u_stay = rep_["utf8"][:3]
            print("  [eboot] UTF-8 labels (translation/ui_utf8.json): %d in place, %d repointed%s"
                  % (u_in, u_rp, "" if not u_stay else
                     "; still Japanese: " + ", ".join("%s (%s)" % x for x in u_stay)))
        if rep_["vwf"]:
            print("  [eboot] VWF stub @%#x, width table @%#x: %d letter cells" % (eboot.STUB_VA, eboot.TABLE_VA, rep_["vwf"]["narrowed"]))
        if voice_table is not None:
            # the SRVC block table: 277 big-endian offsets, rewritten with the rebuilt file
            import srvc_blocks as S
            old_t, new_t = voice_table
            if new_elf[S.TABLE_OFF:S.TABLE_OFF + S.TABLE_LEN] != S.pack_table(old_t):
                raise SystemExit("[voice] EBOOT: the SRVC block table at %#x is not where expected" % S.TABLE_OFF)
            new_elf = new_elf[:S.TABLE_OFF] + S.pack_table(new_t) + new_elf[S.TABLE_OFF + S.TABLE_LEN:]
        open(os.path.join(outdir, "EBOOT.BIN"), "wb").write(new_elf)
        print("  [eboot] EBOOT.BIN  %d series names English, %d entries repointed, %d read back OK%s"
              % (rep_["translated"], rep_["repointed"], n,
                 "" if not rep_["stayed"] else "; still Japanese: " + ", ".join(rep_["stayed"])))
    # UI data is part of the same build, not an optional post-build command.
    # Omitting it shipped Japanese Spirit bands in an otherwise new bundle.
    if vwf:
        import location_caption
        import trophy_labels
        trophy_labels.build(outdir)
        location_caption.build(outdir, spec[0], title_version=title_version)
        import maximum_break_art
        maximum_break_art.build(outdir, spec[0])
        import demo_series_titles
        demo_series_titles.build(outdir)
        subprocess.run([sys.executable, os.path.join(here, "build_ui.py"),
                        "--out", outdir, "--ttf", spec[0]], check=True)
        if "--eboot" in argv:
            import terrain_catalog
            terrain_catalog.prepare(outdir)
            subprocess.run([sys.executable, os.path.join(here, "check_issue_fixes.py"),
                            "--out", outdir, '--version', title_version]
                           + (['--partial-translation'] if '--partial-translation' in argv else []), check=True)
            write_build_manifest(outdir, title_version)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
