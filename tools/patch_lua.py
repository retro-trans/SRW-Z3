"""Substitute English into a scenario Lua, encoded as digraph pairs.

The replacement cannot go through a cp932 codec: the pair codes are
deliberately UNASSIGNED SJIS, so `str.encode('cp932')` rejects them. The file
is therefore rebuilt as bytes -- untouched segments re-encoded as cp932, each
[[...]] block replaced with raw digraph bytes.

Structure that must survive, and is asserted rather than hoped for:
  * the number of [[...]] blocks matches the translation exactly
  * every record keeps the same count of 《》 links, which bind positionally
    to the record's kw_Ary list
  * no encoded block contains ]] , which would close the Lua long string early

    python tools/patch_lua.py <in.lua> <translation.py> <out.lua> [--map m.json]
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import digraph as dg            # noqa: E402
import luarec                   # noqa: E402
import trdata                   # noqa: E402
from dialogue_structure import speaker_problem

# `--[[ ... ]]` is a Lua BLOCK COMMENT, not a string. Some members are
# nothing but comments (STG0001B_00002 is 28 of them, 0 dialogue), and
# rewriting one would burn atlas cells on text no player ever sees.
BLOCK = re.compile(r"(?<!--)\[\[(.*?)\]\]", re.S)


def load_translation(path):
    """Translation files are JSON and are parsed, never executed."""
    return trdata.records(path)


def build_mapping(lines, metrics):
    want = []
    for block in lines:
        for p in dg.mixed_pairs(_en(block)):
            if p not in want:
                want.append(p)
    pool = dg.free_pool(metrics)
    if len(want) > len(pool):
        raise SystemExit("need %d cells, only %d free" % (len(want), len(pool)))
    return {p: pool[i] for i, p in enumerate(want)}


def _en(item):
    return item["en"] if isinstance(item, dict) else item


def patch(lua_bytes, lines, mapping):
    text = lua_bytes.decode("cp932")
    recs = luarec.records(text)
    if len(recs) != len(lines):
        raise SystemExit("lua has %d dialogue records, translation has %d"
                         % (len(recs), len(lines)))

    # Bind each translation to a specific line, not to "the Nth block".
    # A stamped record carries (event, n, pid, sha); each is asserted against
    # the Lua, so a reordered or wrongly-edited entry is a hard error rather
    # than a silent speaker shift. Unstamped records (bare strings) still bind
    # by position, which is what the game itself does.
    # Only records that actually carry an id can be looked up by one. A member
    # made of bare labels (STG0021 member 2 is two team names) has event and n
    # None on every record, so keying by them collapses the whole member onto
    # one entry and every stamp is then checked against the wrong record --
    # which is how "the japanese changed" fired on a correct translation.
    by_id = {(r["event"], r["n"]): r for r in recs
             if r["event"] is not None or r["n"] is not None}
    bound = []
    for i, item in enumerate(lines):
        stamped = (isinstance(item, dict) and "event" in item
                   and (item["event"] is not None or item["n"] is not None))
        if stamped:
            key = (item["event"], item["n"])
            r = by_id.get(key)
            if r is None:
                raise SystemExit("translation record %s#%s does not exist in the lua"
                                 % key)
            if item.get("pid") != r["pid"]:
                raise SystemExit("%s#%s: translation says speaker %s, lua says %s"
                                 % (key[0], key[1], item.get("pid"), r["pid"]))
            if item.get("sha") != r["sha"]:
                raise SystemExit("%s#%s: the japanese changed since this line was "
                                 "translated (sha %s -> %s); re-stamp and re-review"
                                 % (key[0], key[1], item.get("sha"), r["sha"]))
        else:
            r = recs[i]                      # unstamped: bind by position
            if isinstance(item, dict) and item.get("sha") and item["sha"] != r["sha"]:
                raise SystemExit("record %d: the japanese changed since this line was "
                                 "translated (sha %s -> %s); re-stamp and re-review"
                                 % (i, item["sha"], r["sha"]))
        bound.append((r, _en(item)))

    for r, en in bound:
        jp = r["jp"]
        problem = speaker_problem(jp, en)
        if problem:
            raise SystemExit("%s#%s: %s" % (r["event"], r["n"], problem))
        if jp.count("《") != en.count("《"):
            raise SystemExit("%s#%s: %d 《 in japanese, %d in english -- the keyword "
                             "ids bind positionally" % (r["event"], r["n"],
                                                        jp.count("《"), en.count("《")))
        pj = jp.count("$n") + jp.count("$l")
        pe = en.count("$n") + en.count("$l")
        if pj != pe:
            raise SystemExit("%s#%s: %d $-placeholders in japanese, %d in the translation "
                             "-- a speaker or an inline name is wrong"
                             % (r["event"], r["n"], pj, pe))

    # emit in Lua order, whatever order the translation file is in
    en_for = {(r["event"], r["n"]): en for r, en in bound}
    out = bytearray()
    pos = 0
    for r, m in zip(recs, BLOCK.finditer(text)):
        out += text[pos:m.start()].encode("cp932")
        en = en_for[(r["event"], r["n"])]
        encode = dg.encode_hybrid if dg.VWF else dg.encode_mixed
        enc = encode(en.replace("\r\n", "\n"), mapping)
        if b"]]" in enc:
            raise SystemExit("%s#%s encodes a ]] and would close the string"
                             % (r["event"], r["n"]))
        out += b"[[" + enc + b"]]"
        pos = m.end()
    out += text[pos:].encode("cp932")
    return bytes(out)


def main(argv):
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    src, trans, dst = argv[1], argv[2], argv[3]
    here = os.path.dirname(os.path.abspath(__file__))
    metrics = os.path.join(here, "..", "work", "atlas", "metrics.json")
    lines = load_translation(trans)
    mapping = build_mapping(lines, metrics)
    data = patch(open(src, "rb").read(), lines, mapping)
    open(dst, "wb").write(data)
    print("%d records, %d distinct pairs" % (len(lines), len(mapping)))
    print("%s  %d B -> %s  %d B"
          % (os.path.basename(src), os.path.getsize(src), dst, len(data)))
    if "--map" in argv:
        mp = argv[argv.index("--map") + 1]
        json.dump({"%s%s" % k: v for k, v in mapping.items()}, open(mp, "w"), indent=1)
        print("mapping -> %s" % mp)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
