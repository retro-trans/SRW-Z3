"""Read-only inventory helpers for the shared localization migration."""
import ast
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def japanese(text):
    return isinstance(text, str) and bool(re.search('[\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]', text))


def literals(node):
    return [n for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def assignments(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    yield target.id, node.value
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Name) and node.target.id.isupper():
            yield node.target.id, node.value


def inventory():
    out = {}
    for path in sorted((ROOT / 'tools').glob('*.py')):
        if path.name.startswith(('test_', 'localization', 'migrate_localization')):
            continue
        tree = ast.parse(path.read_bytes(), filename=str(path))
        rows = []
        for name, value in assignments(tree):
            texts = [n.value for n in literals(value)]
            if any(japanese(t) for t in texts) or any(x in name for x in ('LABEL', 'TEXT', 'TITLE', 'DESCR', 'HEADER', 'CAPTION', 'DIALOG')):
                sample = [t for t in texts if t and not japanese(t)]
                if sample:
                    rows.append(dict(variable=name, count=len(sample), sample=sample[:4]))
        if rows:
            out[path.relative_to(ROOT).as_posix()] = rows
    return out


if __name__ == '__main__':
    print(json.dumps(inventory(), ensure_ascii=True, indent=2))
