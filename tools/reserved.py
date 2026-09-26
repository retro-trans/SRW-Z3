"""Every cp932 code the game still draws in Japanese, so no pair may take it.

Computed from the same data that gets translated, so the set is exact: field
labels on the library pages, legacy voice-actor glyphs (reserved for compatibility), any
library field left untouched, and the pid-less caption records in stages.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zukan          # noqa: E402
from cpk import CPK   # noqa: E402

UI_LABELS = "愛称声優登場作品身長重量搭乗者表情台詞図鑑機体名パイロット全高本体"


def codes(text):
    out = set()
    b = text.encode("cp932", "ignore")
    i = 0
    while i < len(b) - 1:
        c = b[i]
        if 0x81 <= c <= 0x9F or 0xE0 <= c <= 0xEF:
            out.add((c << 8) | b[i + 1]); i += 2
        else:
            i += 1
    return out


def reserved(libdir, glossary, translated_entries, rpw_swapped=None):
    """`translated_entries` = {libname: {id: {field: en}}} so untouched fields
    can be spotted. Anything not translated stays Japanese and is reserved."""
    names = {t["jp"] for t in glossary["terms"] if t["en"]}
    res = codes(UI_LABELS)
    # RPW_DATA.CPK is a plain-cp932 <mt>prod string table the game draws AS
    # IS -- unit, pilot and series names for the battle and intermission
    # screens. (The zukan 登場作品 label is neither PRDC nor this file: it
    # is a string table in the EBOOT, see tools/eboot.py.) A
    # series name translated in the zukan is therefore still on screen in
    # Japanese, and releasing its kanji turned 超時空世紀 into 'Gddav世紀.
    # Every code in its j-string chunk is reserved until that file is also
    # translated.
    rpw = os.path.join(libdir, "RPW_DATA.CPK")
    if os.path.exists(rpw):
        import rpw as _rpw
        k = CPK(rpw)
        b = k.read(k.files[0])
        # rpw_swapped: the j-string indices the builder will actually swap in
        # place (a name too long for its slot stays Japanese and stays reserved).
        for i, sj in enumerate(_rpw.jstrings(b)):
            drawn_jp = (i not in rpw_swapped) if rpw_swapped is not None else (sj.strip("「」") not in names)
            if drawn_jp:
                res |= codes(sj)
        # the 23 non-string chunks are data, not glyphs; nothing to reserve there
    for lib, keep in (("MTZKN_PT", ("ACTR",)), ("MTZKN_RT", ()), ("MTZKN_KW", ())):
        k = CPK(os.path.join(libdir, lib + ".CPK"))
        ents = translated_entries.get(lib, {})
        for e in k.files:
            _, fields = zukan.parse_ordered(k.read(e))
            for tag, payload in fields:
                if tag in ("VOIC", "LOOK", "HEIT", "WEIT"):
                    continue
                txt = payload.rstrip(b"\0").decode("cp932", "replace")
                ent = ents.get(e["id"], {})
                # Mirror build_library exactly. DSC2 is filled from DSCR when
                # the source DSC2 equals DSCR (the common case), so a missing
                # DSC2 translation does NOT mean DSC2 stays Japanese. And a
                # placeholder pilot slot (ーーー) is converted, not kept.
                if tag == "DSC2":
                    src_d1 = next((q for t2, q in fields if t2 == "DSCR"), b"")
                    same = src_d1.rstrip(b"\x00") == payload.rstrip(b"\x00")
                    translated = ("DSC2" in ent) or (same and "DSCR" in ent)
                elif tag == "DSCR":
                    translated = "DSCR" in ent
                else:
                    bare = txt.strip("「」")
                    translated = bare in names or (bool(bare) and not bare.strip("－"))
                if not translated or tag in keep:
                    res |= codes(txt)
    return res
