"""Rebuild a library (図鑑) CPK with English entries.

Names come from `analysis/glossary.json` so the library and the script cannot
drift apart -- if a term is renamed there, it changes in both. Descriptions
come from a translation module keyed by zukan id.

Two things this has to get right that are easy to miss:

* **The text is digraph-encoded**, exactly like dialogue. The renderer is the
  same one, so plain fullwidth English would read spaced-out here too. The
  mapping is shared with the script because the atlas is global -- which is
  why the real entry point is `build()`, called by `build_project.py`, and not
  this file's own `main()`.
* **Lines are hard-wrapped here.** The library panel is 38 cells (76 columns)
  wide, and the shipped Japanese is wrapped in the data rather than by the
  renderer, so the English has to be wrapped too.

    python tools/build_library.py <in.CPK> <glossary.json> <translations.py> <out.CPK>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK          # noqa: E402
import cpkpatch              # noqa: E402
import digraph as dg         # noqa: E402
import zukan                 # noqa: E402
import trdata                # noqa: E402
import library_cv            # noqa: E402

LIB_CELLS = 38
NAME_FIELDS = ("WORD", "SRCE", "PRDC", "CHFN", "CHNN", "RBTN", "RBN2", "PLTN")
TEXT_FIELDS = ("DSCR", "DSC2")


def wrap(text, cells=LIB_CELLS):
    """Hard-wrap English to the library's line width.

    A cell holds two Latin letters, so the budget is 2*cells characters.
    """
    if dg.VWF:
        return dg.wrap_px(text, "library", cells * dg.SCREENS["library"][0])
    limit = cells * 2
    out = []
    for para in text.split("\n"):
        line = ""
        for word in para.split(" "):
            if not line:
                line = word
            elif len(line) + 1 + len(word) <= limit:
                line += " " + word
            else:
                out.append(line)
                line = word
        out.append(line)
    return "\n".join(out)


def load_entries(path):
    """Descriptions keyed by zukan id. JSON, parsed not executed; a directory
    of batch files is assembled, a single file is read directly."""
    if os.path.isdir(path):
        return trdata.assemble(path, os.path.basename(path.rstrip("/\\")))[0]
    return trdata.entries(path)


LIB_KIND = {"MTZKN_KW": "keyword", "MTZKN_PT": "pilot", "MTZKN_RT": "robot"}


def _names(glossary, kind=None):
    """(flat, keyed) name lookups.

    `flat` is {japanese: english}, which is all most names need. `keyed` is
    {(japanese, library entry id): english}, which is what a Japanese short
    name shared by two DIFFERENT people needs: レイ is entry 168 Ray Lovelock
    and entry 333 Rei Ayanami, ミーナ is 120 Mehna Carmine and 182 Mina
    Roshan. A flat map cannot tell them apart, so whichever term the
    comprehension saw last won and one of the two was mislabelled on screen.

    `kind` scopes the keyed lookup to this file, because entry ids restart
    at 0 in each of the three library archives."""
    flat, keyed = {}, {}
    for t in glossary["terms"]:
        if not t["en"]:
            continue
        flat.setdefault(t["jp"], t["en"])
        zid = t.get("zukan_id")
        if zid is not None and (kind is None or t["kind"] == kind):
            keyed[(t["jp"], zid)] = t["en"]
    return flat, keyed


STAT_FIELDS = ("HEIT", "WEIT")
_FW = {ord(c): chr(ord(c) - 0xFEE0) for c in "０１２３４５６７８９．ｍｔ"}
_FW[ord("－")] = "-"


def stat(text):
    """`５７．０ｍ` -> `57.0m`, `－－－` -> `---`.

    Every HEIT/WEIT value in the shipped data is one of 17 shapes built purely
    from fullwidth digits, `．`, a unit letter and `－`, so a character-class
    map covers all of them. Left fullwidth they would render as spaced-out
    fullwidth numerals next to tight Latin text.
    """
    return text.translate(_FW)


def _rendered(src, glossary, entries, wrap_text=None):
    """Yield (entry, magic, fields, {index: output text}) for every field a
    build would replace.

    Both `collect_texts` and `build` go through here so they cannot disagree.
    That matters more than it looks: padding is context sensitive, so the pairs
    needed by `Aquarion EVOL` differ from those needed by `「Aquarion EVOL」`.
    Pooling the bare name and then encoding the bracketed one is exactly how a
    KeyError on ('E','V') happens.
    """
    kind = LIB_KIND.get(os.path.basename(src)[:-4].upper())
    wrap_text = wrap if wrap_text is None else wrap_text
    names, keyed = _names(glossary, kind)
    actors = library_cv.load_catalog()
    cpk = CPK(src)
    for e in cpk.files:
        magic, fields = zukan.parse_ordered(cpk.read(e))
        outs = {}
        for i, (tag, payload) in enumerate(fields):
            txt = payload.rstrip(b"\0").decode("cp932", "replace")
            out = None
            if tag == "ACTR":
                out = library_cv.romanize(txt, actors)
            elif tag in NAME_FIELDS:
                bare = txt.strip("「」")
                # this entry's own term first, then the shared one
                en = keyed.get((bare, e["id"]), names.get(bare))
                if en:
                    out = (("「%s」" % en)
                           if txt.startswith("「") else en)
                elif bare and not bare.strip("－"):
                    # `－－－`: an unmanned unit's pilot slot. 107 of 253
                    # robots have one. Not a name, so it never reaches the
                    # glossary -- convert it like a stat or it stays fullwidth.
                    out = stat(txt)
            elif tag in TEXT_FIELDS:
                ent = entries.get(e["id"], {})
                tr = ent.get(tag)
                # DSC2 is usually a byte-for-byte copy of DSCR, and the batch
                # modules were told to supply DSC2 only when it DIFFERS. So
                # when the source DSC2 equals DSCR and no separate DSC2 was
                # written, the DSCR translation is the right text for both.
                # Without this, the original Japanese DSC2 passed straight
                # through and the library showed an English DSCR beside a
                # Japanese DSC2 for most entries.
                if not tr and tag == "DSC2" and ent.get("DSCR"):
                    d1 = next((q for g_, q in fields if g_ == "DSCR"), b"")
                    if d1.rstrip(b"\x00") == payload.rstrip(b"\x00"):
                        tr = ent["DSCR"]
                if tr:
                    out = wrap_text(tr)
            elif tag in STAT_FIELDS and txt:
                out = stat(txt)
            if out is not None:
                outs[i] = out
        yield e, magic, fields, outs


def collect_texts(src, glossary, entries):
    """Every string this build will encode, in its final form."""
    for _e, _m, _f, outs in _rendered(src, glossary, entries):
        for t in outs.values():
            yield t


def build(src, glossary, entries, dst, mapping=None):
    """Rebuild one library CPK. `mapping` digraph-encodes; None leaves plain."""
    reps, tmp = {}, []
    changed = 0
    for e, magic, fields, outs in _rendered(src, glossary, entries):
        new, hit = [], False
        for i, (tag, payload) in enumerate(fields):
            out = outs.get(i)
            if out is None:
                new.append((tag, payload))
                continue
            # the shipped library text uses bare LF; a CR is drawn as a stray
            # kanji and desynchronises the 2-byte stream (the 拭 garbage)
            blob = (dg.encode_mixed(out, mapping, newline=b"\n") if mapping
                    else out.encode("cp932"))
            new.append((tag, blob))
            hit = True
        if hit:
            changed += 1
        p = "%s.e%d" % (dst, e["id"])
        open(p, "wb").write(zukan.build(magic, new))
        reps[e["id"]] = p
        tmp.append(p)
    cpkpatch.build(src, dst, reps)
    for p in tmp:
        os.remove(p)
    return changed


def main(argv):
    if len(argv) < 5:
        print(__doc__.strip())
        return 2
    src, gpath, tpath, dst = argv[1], argv[2], argv[3], argv[4]
    g = json.load(open(gpath, encoding="utf-8"))
    entries = load_entries(tpath)
    n = build(src, g, entries, dst)
    print("%d entries touched -> %s (%d B)  [PLAIN, not digraph-encoded: use "
          "build_project.py for a real build]" % (n, dst, os.path.getsize(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
