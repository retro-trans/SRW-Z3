"""Load translation data. The one place that knows the on-disk format.

Translation files are JSON, and this is the only loader. Every tool that needs
LINES / ENTRIES / NAMES goes through here, so the format can never be read
two different ways by two different tools -- which is exactly the class of bug
the padding rules had earlier.

Nothing here executes a file. A translation file is parsed, never run.

    lines(path)              -> list of dialogue records
    entries(path)            -> {int id: {"DSCR": ..., "DSC2": ...}}
    names(path)              -> {jp: en}
    assemble(dir, prefix)    -> (entries, names) across every <prefix>_*.json
"""
import json
import os


_IDX = None


def use_glossary(path):
    """Load the term index every `$$id$$` in a translation file resolves
    against. Every reader below goes through it, so no build path can
    ship a raw reference to the screen."""
    global _IDX
    import terms
    _IDX = terms.index(_load(path))
    return len(_IDX)


def _ex(text, where=""):
    """Expand glossary references. Refusing to guess when no glossary has
    been loaded is deliberate: a silently unexpanded token reaches the
    player as literal `$$sphere$$`."""
    if text is None or "$$" not in text:
        return text
    if _IDX is None:
        raise SystemExit("%s: glossary reference found but no glossary loaded "
                         "-- call trdata.use_glossary() first" % (where or "translation"))
    import terms
    return terms.expand(text, _IDX, where)


def _load(path):
    # Known project files are generated views of the shared locale catalog.
    # External/temporary translation fixtures retain the ordinary JSON reader.
    import localization
    return localization.load_legacy(path)


def lines(path):
    """English text of every record, in file order. Records may be bare
    strings or stamped dicts with (event, n, pid, sha, jp, en)."""
    return [_ex(r["en"] if isinstance(r, dict) else r, path)
            for r in _load(path)["LINES"]]


def records(path):
    """The full records, stamped or not. patch_lua binds on these."""
    recs = _load(path)["LINES"]
    for r in recs:
        if isinstance(r, dict) and r.get("en"):
            r["en"] = _ex(r["en"], path)
    return recs


def voice_document(path):
    """Expand battle subtitles before both atlas pooling and binary encoding.

    Keep source text, section IDs, budgets and other metadata unchanged.
    """
    doc = _load(path)
    for key, row in doc.get('lines', {}).items():
        if isinstance(row, dict):
            row['en'] = _ex(row.get('en'), str(path) + ':' + key)
        else:
            doc['lines'][key] = _ex(row, str(path) + ':' + key)
    return doc


def shared_records(group, root=None):
    """English stamped dialogue directly from the neutral shared catalog.

    Both platform adapters may use this; their binary layouts stay separate.
    The current glossary expansion API is English-only by design.
    """
    import localization
    catalog = localization.english() if root is None else localization.Catalog(root)
    rows = catalog.dialogue_records(group)
    for row in rows:
        row['en'] = _ex(row['en'], group)
    return rows


def _ex_entry(ent, path):
    if not isinstance(ent, dict):
        return _ex(ent, path)
    return {k: (_ex(v, path) if isinstance(v, str) else v) for k, v in ent.items()}


def entries(path):
    return {int(k): _ex_entry(v, path) for k, v in _load(path).get("ENTRIES", {}).items()}


def names(path):
    return {jp: _ex(en, path) for jp, en in _load(path).get("NAMES", {}).items()}


def assemble(directory, prefix, ambiguous=()):
    """Merge every <prefix>_NNN.json in a directory.

    Two batches defining the same id is a hard error. Two batches rendering
    the same Japanese name differently is a hard error too -- UNLESS the
    glossary marks that term ambiguous, because a shared short name that
    honestly resolves two ways (レイ is Ray Lovelock and Rei Ayanami) is a
    fact to record, not a conflict to pick a winner for.
    """
    ents, nms = {}, {}
    if not os.path.isdir(directory):
        return ents, nms
    for fn in sorted(os.listdir(directory)):
        if not (fn.startswith(prefix + "_") and fn.endswith(".json")):
            continue
        p_ = os.path.join(directory, fn)
        d = _load(p_)
        e = {int(k): _ex_entry(v, p_) for k, v in d.get("ENTRIES", {}).items()}
        dup = set(ents) & set(e)
        if dup:
            raise SystemExit("%s redefines ids: %s" % (fn, sorted(dup)))
        ents.update(e)
        for jp, en in {j: _ex(e_, p_) for j, e_ in d.get("NAMES", {}).items()}.items():
            if jp in nms and nms[jp] != en and jp not in ambiguous:
                raise SystemExit("%s: %r rendered as %r and %r -- if these are "
                                 "two different people, mark the term ambiguous "
                                 "in the glossary" % (fn, jp, nms[jp], en))
            nms.setdefault(jp, en)
    return ents, nms


def ambiguous_terms(glossary_path):
    try:
        g = _load(glossary_path)
    except (OSError, ValueError):
        return set()
    return {t["jp"] for t in g["terms"] if t.get("status") == "ambiguous"}
