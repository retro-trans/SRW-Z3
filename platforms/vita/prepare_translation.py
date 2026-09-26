"""Prepare the shared opening-stage English for Vita review, NOT a game patch.

Dry-run by default. --write saves an ignored review bundle under work/vita.
No PKG/license access, extraction, encryption, atlas generation or deployment.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import luarec
import shared_content
import terms
import trdata


def identity(record):
    if not isinstance(record, dict) or any(
            key not in record for key in ("event", "n", "pid", "jp", "sha")):
        raise ValueError("Unstamped source record; cannot match safely")
    if record["sha"] != luarec.digest(record["jp"]):
        raise ValueError("Source fingerprint does not match Japanese text")
    return (record["event"], record["n"], record["pid"], record["sha"],
            record["jp"].replace("\r\n", "\n"))


def match_records(translations, source):
    """Strict future adapter gate. Caller must supply verified Vita records.

    No fuzzy matches, ordinal-only matches or automatic fallback to PS3 data.
    Even success only verifies text identity, not Vita font/control-code support.
    """
    if not translations or not source:
        raise ValueError("Empty records cannot verify source compatibility")
    source_keys = [identity(record) for record in source]
    translated_keys = [identity(record) for record in translations]
    if (len(set(source_keys)) != len(source_keys) or
            len(set(translated_keys)) != len(translated_keys)):
        raise ValueError("Ambiguous duplicate record identity")
    if collections.Counter(source_keys) != collections.Counter(translated_keys):
        raise ValueError("Vita source differs; manual mapping/review required")
    index = {identity(record): record for record in translations}
    return [index[key] for key in source_keys]


def prepare(root=ROOT):
    root = Path(root)
    config = json.loads((root / "platforms/vita/pilot.json").read_text(encoding="utf-8"))
    trdata.use_glossary(str(root / "analysis/glossary.json"))
    members = []
    for member in config["members"]:
        path = root / member["translation"]
        records = trdata.shared_records(path.stem, root)
        if not records:
            raise ValueError("Empty pilot translation: " + member["translation"])
        for record in records:
            identity(record)
            english = record.get("en")
            if not english or not english.strip() or "$$" in english or terms.stray(english):
                raise ValueError("Missing English or unresolved glossary reference")
            if "]]" in english:
                raise ValueError("Unsafe Lua long-string terminator in English")
        members.append(dict(member, records=len(records),
                            translation_sha256=hashlib.sha256(json.dumps(records,ensure_ascii=False,
                                sort_keys=True).encode('utf-8')).hexdigest(),
                            lines=[{k: r[k] for k in ("event", "n", "pid", "sha", "en")}
                                   for r in records]))
    return {"schema": 1, "platform": "vita", "title_id": config["title_id"],
            "status": "prepared_unverified", "playable": False,
            "shared_content": shared_content.revision(root),
            "limitations": ["Vita source records not yet matched to shared translations",
                            "Member IDs are PS3-derived candidates, not verified Vita IDs",
                            "Vita font, layout, encoding and control metadata unverified"],
            "members": members}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="save review bundle; never builds/installs")
    args = parser.parse_args()
    result = prepare()
    print("Vita PCSG00264: %d opening-stage records prepared across %d candidates" %
          (sum(m["records"] for m in result["members"]), len(result["members"])))
    print("Shared English revision: " + result["shared_content"]["sha256"])
    for member in result["members"]:
        print("  %s: %d records; sample: %s" %
              (member["translation"], member["records"],
               member["lines"][0]["en"].replace("\n", " / ").replace("\r", "")))
    print("UNVERIFIED REVIEW ONLY: no Vita game files patched; source record matching still required.")
    if args.write:
        target = ROOT / "work/vita/initial_translation.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Saved " + str(target))
    else:
        print("Dry-run: nothing written. Add --write to save the review bundle.")


if __name__ == "__main__":
    main()
