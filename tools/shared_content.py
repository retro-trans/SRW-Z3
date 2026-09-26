"""Fingerprint the shared English source tree, including uncommitted edits.

This is a source revision, not a claim that every file applies to both platforms.
"""
import fnmatch
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def revision(root=ROOT, language='en'):
    if not re.fullmatch('[a-z]{2,3}(?:-[A-Z]{2})?', language):
        raise ValueError('Invalid locale code')
    root = Path(root)
    catalog_path = root / "shared/catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    paths = {catalog_path}
    for pattern in catalog["content_globs"]:
        pattern = pattern.replace('{language}', language)
        paths.update(p for p in root.glob(pattern) if p.is_file())
    files = {}
    for path in sorted(paths):
        relative = path.relative_to(root).as_posix()
        if any(fnmatch.fnmatchcase(relative, pattern) for pattern in catalog["exclude"]):
            continue
        files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    digest = hashlib.sha256(json.dumps(files, sort_keys=True,
                                      separators=(",", ":")).encode("utf-8")).hexdigest()
    return {"schema": 1, "language": language, "sha256": digest, "file_count": len(files)}


if __name__ == "__main__":
    print(json.dumps(revision(), indent=2))
