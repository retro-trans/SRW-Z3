"""Flag a `レイ`-class token whose scene says it names the other character.

The briefs carry an auto-generated cast section keyed on the portrait id, and
for the names two characters share that section is often simply wrong: every
`pid_RAY`/`pid_RAY_S` line gets Ray Lovelock's Macross 7 bio, including Rei
Ayanami's. Roughly half the slices trust it. A wrong discriminator is
invisible to `check_stage.py` -- the token resolves, expands and measures
fine -- and it is only wrong on screen, so it needs its own check.

The evidence is the scene, not the portrait: a record is read together with
its neighbours in the member, because a bare `「………」` carries no evidence of
its own and hashes identically for both characters.

    python tools/check_names.py                      # every registered stage
    python tools/check_stage.py translation/x.json   # or named files
"""
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import luarec  # noqa: E402

# token -> (markers that CONFIRM it, markers that say it is the other one)
PAIRS = {
    # Not a name/name collision like the two below, but a name colliding with
    # an ordinary honorific. `先生` is a Shin Mazinger character, and it is also
    # what a student calls a teacher and what Yu Fan calls Gauron. Of the 332
    # records whose Japanese contains it, only 39 mean the character -- so the
    # token is the rare reading, and a slice that checks `terms.py`, finds a
    # real entry and tokenises it has done everything right and still shipped
    # the wrong person's name into another series' scene.
    "先生": {
        "name": "Sensei (Shin Mazinger)",
        "other": "an ordinary honorific -- teacher, doctor, mentor",
        "confirm": r"甲児|兜|マジンガー|あしゅら|ブロッケン|ミケーネ|ヘル|さやか|鉄也|光子力|剣造|くろがね|五人衆|ジャンゴ|お菊",
        "wrong": r"玉芳|玉蘭|ガウルン|宗介|千鳥|テッサ|ミスリル|スズネ|西条|桃井|いぶき|ノリコ|学長|大学病院",
    },
    "レイ#168": {          # Ray Lovelock, Macross 7
        "name": "Ray Lovelock (Macross 7)",
        "other": "レイ#333",
        "confirm": r"バサラ|ミレーヌ|ガムリン|ビヒーダ|Ｆｉｒｅ|ボンバー|オズマ",
        "wrong": r"碇|綾波|使徒|エヴァ|ＥＶＡ|シンジ|ミサト|アスカ|ボン太くん|初号機|零号機",
    },
    "レイ#333": {          # Rei Ayanami, Evangelion
        "name": "Rei Ayanami (Evangelion)",
        "other": "レイ#168",
        "confirm": r"碇|綾波|使徒|エヴァ|ＥＶＡ|シンジ|ミサト|アスカ|初号機|零号機",
        "wrong": r"バサラ|ミレーヌ|ガムリン|ビヒーダ|Ｆｉｒｅ|ボンバー",
    },
    "ドロシー#86": {        # Dorothy Catalonia, Gundam Wing
        "name": "Dorothy Catalonia (Gundam Wing)",
        "other": "ドロシー#240",
        "confirm": r"リリーナ|トレーズ|ゼクス|ロームフェラ|デルマイユ|マリーメイア",
        "wrong": r"ロジャー|ノーマン|ベック|パラダイム|ビッグオー|大鉄人",
    },
    "ドロシー#240": {       # R. Dorothy Waynewright, The Big O
        "name": "R. Dorothy Waynewright (The Big O)",
        "other": "ドロシー#86",
        "confirm": r"ロジャー|ノーマン|ベック|パラダイム|ビッグオー|大鉄人",
        "wrong": r"リリーナ|トレーズ|ゼクス|ロームフェラ|デルマイユ|マリーメイア",
    },
}
WINDOW = 5     # records either side that count as the scene


def member_lua(trans_path):
    """The .lua whose records this translation module answers."""
    src = open(os.path.join(ROOT, "platforms", "ps3", "manifest.py"),
               encoding="utf-8").read()
    m = re.search(r'"lua":\s*"([^"]+)",\s*\n?\s*"trans":\s*"%s"'
                  % re.escape(trans_path.replace("\\", "/")), src)
    return m.group(1) if m else None


def scan(path):
    doc = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
    lines = doc.get("LINES") or []
    lua = member_lua(path)
    recs = []
    if lua and os.path.isfile(os.path.join(ROOT, lua)):
        recs = luarec.records(open(os.path.join(ROOT, lua), "rb")
                              .read().decode("cp932", "replace"))
    jp_by_pos = [r.get("jp") or "" for r in recs] or [r.get("jp") or "" for r in lines]
    pos = {}
    for i, r in enumerate(recs or lines):
        pos.setdefault(r.get("sha"), []).append(i)

    out = []
    for r in lines:
        en = r.get("en") or ""
        for tok, spec in PAIRS.items():
            if ("$$%s$$" % tok) not in en:
                continue
            for i in pos.get(r.get("sha"), []):
                scene = "".join(jp_by_pos[max(0, i - WINDOW):i + WINDOW + 1])
                if re.search(spec["wrong"], scene) and not re.search(spec["confirm"], scene):
                    out.append((r["sha"], tok, spec, i,
                                (r.get("jp") or "").replace("\n", " / ")[:60],
                                en.replace("\n", " / ")[:70]))
                    break
    return out


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    paths = [a for a in argv[1:] if not a.startswith("-")]
    if not paths:
        src = open(os.path.join(ROOT, "platforms", "ps3", "manifest.py"),
                   encoding="utf-8").read()
        paths = re.findall(r'"trans":\s*"(translation/stage[^"]+)"', src)
    bad = 0
    for p in paths:
        if not os.path.isfile(os.path.join(ROOT, p)):
            continue
        for sha, tok, spec, i, jp, en in scan(p):
            bad += 1
            print("%s  %s  record %d" % (os.path.basename(p), sha, i))
            print("    token $$%s$$ = %s, but the scene says %s"
                  % (tok, spec["name"], spec["other"]))
            print("    jp: %s" % jp)
            print("    en: %s" % en)
    print("%d suspect name references" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
