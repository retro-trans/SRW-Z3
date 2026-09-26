"""Build review material for a human or agent proofreading a finished stage.

    python tools/proofread_stage.py STG0092 [--out work/tr/STG0092/proof]

`check_stage.py` verifies what is mechanically checkable -- tokens resolve,
brackets balance, placeholders survive, lines fit the font -- and then reports
"0 problems". In stages 90-100 EVERY defect that reached review was in a class
it structurally cannot see: a line read backwards, a subject invented where the
Japanese has none, one term written two ways, a drawn-out shout rendered as a
nervous stammer.

This does not re-check any of that. It produces two things.

**Scene bundles.** The stage regrouped into scenes, Japanese over English, in
reading order. Slices only ever see 120-record windows, so a term written two
ways is invisible to them; on one page it is obvious.

**A concordance.** Every recurring Japanese term with the English lines that
render it, side by side. No verdict is offered -- the reviewer sees the
renderings together and judges. This is how an epithet that shipped two ways in
stage 97 would have been caught, and it works on plain text, where a
token-based check is blind.

Two lookups are attached per record where they exist:

  near    the closest line elsewhere in the corpus, and its English. Exact
          hash matching reports 20% of a stage as "new" when a >=70% neighbour
          already exists. A near match is a prompt to read, NEVER a fill: the
          difference is what you are translating.
  voice   the same Japanese dialogue spoken by a different character, and how
          it was rendered for them. 381 lines are shared this way and 63% were
          deliberately varied, so this asks the live question -- does this
          character say it differently?

Flags are deliberately few. Ones that fired on a tenth of a stage were cut:
a flag that fires often teaches the reader to skip flags.
"""
import argparse
import collections
import difflib
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

INTERROG_JP = re.compile(r"[？?]|か[\s　]*[」』）\)]?$|のか|ですか|ますか|だろ|かい|かな")
STRETCH_JP = re.compile(r"[ぁぃぅぇぉっゃゅょァィゥェォッャュョー～]{2,}")
STAMMER_EN = re.compile(r"(?<![A-Za-z$])([A-Za-z])-\1?[a-z]")
# A term worth tracking across a stage. Three characters minimum in both
# scripts: two-kanji runs are mostly fragments, because a run starting after a
# hiragana prefix cannot see the prefix -- `お前達` arrives here as `前達`, which
# is not a term and renders every which way.
TERMLIKE = re.compile(r"[ァ-ヺー]{3,}|[一-鿿]{3,}")


def load(path):
    with io.open(path, encoding="utf-8") as fh:
        return json.load(fh)


def body(text):
    """A record without its speaker line."""
    return "\n".join(text.split("\n")[1:]) or text


def corpus(exclude, root=ROOT):
    """Every shipped record except the stage under review."""
    out = {}
    for path in sorted(glob.glob(os.path.join(root, "translation", "stage*.json"))):
        if os.path.basename(path).startswith(exclude):
            continue
        try:
            rows = load(path)["LINES"]
        except Exception:
            continue
        for row in rows:
            jp, en = row.get("jp") or "", row.get("en") or ""
            if jp and en:
                out.setdefault(row["sha"], (jp, en))
    return out


def trigrams(text):
    text = text.replace("\n", "")
    return {text[i:i + 3] for i in range(max(0, len(text) - 2))}


class Neighbours(object):
    """Closest existing line, by trigram blocking then a real similarity score.

    Scoring one record against forty-six thousand is far too slow; the index
    narrows it to a few dozen candidates that share enough character triples
    to be worth measuring.
    """

    def __init__(self, ship):
        self.ship = ship
        self.index = collections.defaultdict(set)
        for sha, (jp, _) in ship.items():
            for gram in trigrams(jp):
                self.index[gram].add(sha)

    def nearest(self, jp, floor=0.70):
        counts = collections.Counter()
        for gram in trigrams(jp):
            for sha in self.index.get(gram, ()):
                counts[sha] += 1
        best, score = None, 0.0
        for sha, _ in counts.most_common(40):
            ratio = difflib.SequenceMatcher(None, jp, self.ship[sha][0]).ratio()
            if ratio > score:
                best, score = sha, ratio
        return (best, score) if best and score >= floor else (None, 0.0)


def voices(ship):
    """Japanese dialogue -> {speaker: English}, for lines several characters say."""
    out = collections.defaultdict(dict)
    for jp, en in ship.values():
        if "\n" not in jp or "\n" not in en:
            continue
        jb = body(jp)
        if len(jb) >= 8:
            out[jb].setdefault(jp.split("\n")[0], body(en))
    return out


def flags_for(row, majority):
    jp, en = body(row.get("jp") or ""), body(row.get("en") or "")
    out = []
    if "?" in en and not INTERROG_JP.search(jp):
        out.append("invented-?")
    if STAMMER_EN.search(en) and STRETCH_JP.search(jp):
        out.append("stammer")
    items = jp.count("、") + jp.count("，")
    if items >= 4 and en.count(",") < items - 1:
        out.append("count")
    for token in re.findall(r"\$\$([^$]+)\$\$", en):
        want = majority.get(token.split("#")[0])
        if want and "$$%s$$" % token != want:
            out.append("against-corpus")
    return sorted(set(out))


def majority_tokens(root=ROOT):
    seen = collections.defaultdict(collections.Counter)
    for path in sorted(glob.glob(os.path.join(root, "translation", "stage*.json"))):
        try:
            rows = load(path)["LINES"]
        except Exception:
            continue
        for row in rows:
            for hit in re.findall(r"\$\$[^$]+\$\$", row.get("en") or ""):
                seen[hit[2:-2].split("#")[0]][hit] += 1
    return {k: c.most_common(1)[0][0] for k, c in seen.items() if c}


def write(path, lines):
    with io.open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(lines))


def bundle(stage, out_dir, root=ROOT):
    prefix = stage.lower().replace("stg", "stage")
    paths = sorted(glob.glob(os.path.join(root, "translation", "%s*.json" % prefix)))
    if not paths:
        raise SystemExit("no shipped views for %s -- register it first" % stage)
    ship = corpus(prefix, root)
    near = Neighbours(ship)
    spoken = voices(ship)
    majority = majority_tokens(root)
    glossary_keys = {t.get("jp") for t in
                     load(os.path.join(root, "analysis", "glossary.json"))["terms"]}
    os.makedirs(out_dir, exist_ok=True)

    scenes = collections.OrderedDict()
    for path in paths:
        member = os.path.basename(path)[:-len(".json")]
        for row in load(path)["LINES"]:
            if row.get("en"):
                scenes.setdefault((member, row.get("event") or "?"), []).append(row)

    counts = collections.Counter()
    concord = collections.defaultdict(list)
    for (member, event), rows in scenes.items():
        out = ["# %s  scene %s" % (member, event), "",
               "%d records, in reading order." % len(rows), ""]
        for row in rows:
            jp, en = row.get("jp") or "", row["en"]
            marks = flags_for(row, majority)
            counts.update(marks)
            head = "## %s" % row["sha"]
            if marks:
                head += "   **%s**" % ", ".join(marks)
            out.append(head)
            out += ["    JP  " + l for l in jp.split("\n")]
            out += ["    EN  " + l for l in en.split("\n")]
            sha, score = near.nearest(jp)
            if sha:
                counts["near"] += 1
                out.append("    near %.0f%%  %s" % (score * 100, body(ship[sha][0]).replace("\n", " / ")))
                out.append("             %s" % body(ship[sha][1]).replace("\n", " / "))
            others = {s: e for s, e in spoken.get(body(jp), {}).items()
                      if s != jp.split("\n")[0]}
            for speaker, other in list(others.items())[:2]:
                counts["voice"] += 1
                out.append("    voice %s says it as: %s" % (speaker, other.replace("\n", " / ")))
            out.append("")
            for term in set(TERMLIKE.findall(body(jp))):
                concord[term].append((row["sha"], body(en).replace("\n", " / ")))
        write(os.path.join(out_dir, "%s_%s.md" % (member, event)), out)

    lines = ["# %s concordance" % stage.upper(), "",
             "Japanese terms used in more than one record, with the English that",
             "renders them. Terms that ARE glossary entries are omitted: the",
             "checker already enforces those, so they cannot drift. What is left",
             "is the plain text nobody is guarding -- which is where an epithet",
             "shipped two ways in stage 97.", "",
             "No verdict is offered. Read the renderings together and judge",
             "whether a difference is meant.", ""]
    shown = 0
    for term, uses in sorted(concord.items(), key=lambda kv: -len(kv[1])):
        # a glossary term expands from one token, so it cannot disagree with
        # itself; only unguarded plain text is worth a reader's attention
        if len(uses) < 2 or term in glossary_keys:
            continue
        shown += 1
        lines.append("## %s   (%d records)" % (term, len(uses)))
        for sha, text in uses[:12]:
            lines.append("    %s  %s" % (sha, text[:96]))
        lines.append("")
    write(os.path.join(out_dir, "_concordance.md"), lines)
    return len(scenes), sum(len(r) for r in scenes.values()), shown, counts


def main():
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("stage")
    parser.add_argument("--out", default=None)
    parser.add_argument("--root", default=ROOT, help="Read a scratch canonical compatibility export")
    parser.add_argument("--dry-run", action="store_true", help="Preview stage inputs without writing")
    args = parser.parse_args()
    out = args.out or os.path.join(ROOT, "work", "tr", args.stage.upper(), "proof")
    if args.dry_run:
        prefix = args.stage.lower().replace("stg", "stage")
        paths = sorted(glob.glob(os.path.join(args.root, "translation", "%s*.json" % prefix)))
        if not paths:
            raise SystemExit("no stage views under the selected root")
        print("DRY RUN: %d member files -> %s; no files written" % (len(paths), out))
        for path in paths:
            rows = load(path).get("LINES") or []
            print("  %s: %d records" % (os.path.basename(path), len(rows)))
            if rows:
                print("  sample: %s" % json.dumps(rows[0], ensure_ascii=False))
        return 0
    scenes, records, terms, counts = bundle(args.stage, out, args.root)
    print("%s: %d records over %d scenes -> %s"
          % (args.stage.upper(), records, scenes, os.path.relpath(out, ROOT)))
    print("  concordance: %d recurring terms" % terms)
    for name, n in counts.most_common():
        print("  %-16s %4d" % (name, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
