"""Language-independent message IDs and explicit platform compatibility views.

No implicit English fallback. Text lives in localization/locales/<language>;
PS3 locations/templates stay in platforms/ps3/localization. Legacy English
JSON is a checked compatibility export, not a second translation authority.
"""
import argparse
from collections import Counter
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from dialogue_structure import speaker_problem

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'\$\$[^$]+\$\$|(?<!\$)\$[A-Za-z](?!\$)|%[-+0-9.]*[sduif]|\{[A-Za-z_][A-Za-z_0-9]*\}')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    with Path(path).open(encoding='utf-8') as stream:
        return json.load(stream)


def dump(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + '\n'


def safe_path(root, relative):
    root = Path(root).resolve()
    require(isinstance(relative, str) and not Path(relative).is_absolute()
            and '\\' not in relative and ':' not in relative, 'Unsafe relative path')
    path = (root / relative).resolve()
    require(root in path.parents, 'Path escapes root')
    return path


class Catalog:
    def __init__(self, root=ROOT, language='en', fallback=None):
        self.root = Path(root).resolve()
        self.manifest = read_json(self.root / 'localization/manifest.json')
        require(self.manifest['schema'] == 1, 'Unsupported localization schema')
        require(language in self.manifest['languages'], 'Unregistered language: ' + language)
        require(fallback is None or fallback in self.manifest['languages'], 'Unregistered fallback')
        self.language, self.fallback = language, fallback
        self.cache = {}

    def document(self, relative):
        if relative not in self.cache:
            path = safe_path(self.root, relative)
            if not path.exists() and (relative.startswith('localization/messages/')
                    or relative == 'platforms/ps3/localization/legacy.json'):
                raise ValueError('Local Japanese source input is not present: ' + relative
                                 + '. These files are intentionally not in Git. '
                                 'See docs/LOCAL_SOURCE_DATA.md; do not regenerate existing IDs.')
            self.cache[relative] = read_json(path)
        return self.cache[relative]

    def definition(self, mid):
        group = mid.split(':', 1)[0]
        require(group in self.manifest['groups'], 'Unknown message group: ' + group)
        definitions = self.document('localization/messages/' + group + '.json')['messages']
        require(mid in definitions, 'Unknown message ID: ' + mid)
        return definitions[mid]

    def locale(self, language, group):
        relative = 'localization/locales/%s/%s.json' % (language, group)
        if relative not in self.cache:
            path = safe_path(self.root, relative)
            self.cache[relative] = read_json(path) if path.exists() else {'messages': {}}
        return self.cache[relative]['messages']

    def text(self, mid, allow_missing=False):
        definition = self.definition(mid)
        group = mid.split(':', 1)[0]
        for language in [self.language] + ([self.fallback] if self.fallback else []):
            rows = self.locale(language, group)
            row = rows.get(mid)
            if row is not None and row.get('text') is not None:
                require(row.get('status') in ('imported','translated','reviewed','missing','needs_review'),
                        'Unknown translation status: ' + mid)
                if row.get('status') in ('missing', 'needs_review'):
                    if self.fallback and language != self.fallback:
                        continue
                    raise ValueError('Unreviewed translation: ' + mid)
                value = row['text']
                require(isinstance(value, str), 'Non-string translation: ' + mid)
                if definition['kind'] == 'dialogue':
                    problem = speaker_problem(definition.get('source'), value)
                    require(problem is None, 'Dialogue speaker: %s: %s' % (mid, problem))
                require(Counter(TOKEN.findall(value)) == Counter(definition.get('tokens', [])),
                        'Placeholder/glossary-token mismatch: ' + mid)
                require(value.count('《') == definition.get('links', 0)
                        and value.count('》') == definition.get('link_closes', definition.get('links', 0)), 'Link-marker mismatch: ' + mid)
                return value
        if allow_missing:
            return None
        raise ValueError('Missing %s translation: %s (no implicit fallback)' % (self.language, mid))

    def render(self, value, allow_missing=False):
        if isinstance(value, dict):
            if set(value) == {'$message'}:
                return self.text(value['$message'], allow_missing)
            if set(value) == {'$join'}:
                return ''.join(self.render(v, allow_missing) for v in value['$join'])
            return {k: self.render(v, allow_missing) for k, v in value.items()}
        if isinstance(value, list):
            return [self.render(v, allow_missing) for v in value]
        return value

    def legacy(self, relative, allow_missing=False):
        bindings = self.document('platforms/ps3/localization/legacy.json')['documents']
        require(relative in bindings, 'Unknown legacy view: ' + relative)
        return self.render(bindings[relative]['template'], allow_missing)

    def dialogue_records(self, group):
        """Platform-neutral stamped records: no legacy file or PS3 binding read.

        Consumers still verify these identities against their OWN game source.
        Glossary references remain tokens until expanded with the same locale.
        """
        require(group in self.manifest['groups'], 'Unknown dialogue group')
        definitions = self.document('localization/messages/' + group + '.json')['messages']
        rows = []
        for mid, definition in definitions.items():
            context = definition['context']
            require(definition['kind'] == 'dialogue' and isinstance(definition['source'], str)
                    and all(k in context for k in ('event','n','pid')), 'Unstamped dialogue: ' + mid)
            source = definition['source']
            rows.append(dict(event=context['event'], n=context['n'], pid=context['pid'], jp=source,
                sha=hashlib.sha1(source.replace('\r\n','\n').encode('utf-8')).hexdigest()[:10],
                en=self.text(mid)))
        return rows

    def literal(self, key):
        bindings = self.document('platforms/ps3/localization/python.json')['literals']
        require(key in bindings, 'Unknown literal binding: ' + key)
        return self.render(bindings[key]['template'])

    def validate(self):
        counts, errors = Counter(), []
        for group in self.manifest['groups']:
            definitions = self.document('localization/messages/' + group + '.json')['messages']
            rows = self.locale(self.language, group)
            errors.extend('Unknown locale ID: ' + mid for mid in rows.keys() - definitions.keys())
            for mid, definition in definitions.items():
                require(mid.startswith(group+':'), 'Wrong group ID: ' + mid)
                counts[definition['kind']] += 1
                try:
                    self.text(mid)
                except ValueError as error:
                    errors.append(str(error))
        return dict(counts), errors

    def check_compatibility(self):
        require(self.language == 'en' and self.fallback is None, 'Current game builders require English')
        bindings = self.document('platforms/ps3/localization/legacy.json')['documents']
        errors = []
        for relative, binding in bindings.items():
            path = safe_path(self.root, relative)
            current = read_json(path) if binding['format'] == 'json' else path.read_text(encoding='utf-8')
            expected = self.render(binding['template'], allow_missing=True)
            if current != expected:
                errors.append(relative)
        require(not errors, 'Legacy views differ from canonical localization: %s. '
                'Use localization.py sync; do not edit generated mirrors.' % ', '.join(errors[:8]))
        return len(bindings)


@lru_cache(maxsize=1)
def english():
    return Catalog()


def message(mid):
    """Current PS3 tools have English-only layout assumptions; never switch
    their language implicitly via environment variables or global monkeypatches.
    Future language builds must explicitly request a Catalog(language=...)."""
    return english().text(mid)


def literal(key):
    return english().literal(key)


def ensure_compatible():
    catalog = Catalog()
    _, errors = catalog.validate()
    require(not errors, 'Invalid English catalog: ' + '; '.join(errors[:8]))
    return catalog.check_compatibility()


def load_legacy(path, language='en', root=ROOT):
    path, root = Path(path).resolve(), Path(root).resolve()
    if root in path.parents and (root / 'localization/manifest.json').exists():
        relative = path.relative_to(root).as_posix()
        catalog = english() if root == ROOT and language == 'en' else Catalog(root, language)
        bindings = catalog.document('platforms/ps3/localization/legacy.json')['documents']
        if relative in bindings:
            return catalog.legacy(relative, allow_missing=language == 'en')
    return read_json(path)


def sync(root=ROOT, write=False):
    catalog = Catalog(root)
    receipt_path = catalog.root / 'localization/compatibility.json'
    receipt = read_json(receipt_path)
    bindings = catalog.document('platforms/ps3/localization/legacy.json')['documents']
    changes = []
    for relative, binding in bindings.items():
        path = safe_path(catalog.root, relative)
        before = path.read_bytes()
        wanted = catalog.render(binding['template'], allow_missing=True)
        current = json.loads(before.decode('utf-8')) if binding['format'] == 'json' else before.decode('utf-8')
        if current == wanted:
            continue
        require(sha(before) == receipt['files'][relative], 'Unexported legacy edit: ' + relative)
        after = (dump(wanted) if binding['format'] == 'json' else wanted).encode('utf-8')
        changes.append((path, before, after, relative))
    print('%s: %d compatibility views would change' % ('WRITE' if write else 'DRY RUN', len(changes)))
    for _, _, _, name in changes[:12]:
        print(' ', name)
    if not write:
        return len(changes)
    applied = []
    receipt_before = receipt_path.read_bytes()
    try:
        for path, before, after, relative in changes:
            require(path.read_bytes() == before, 'Concurrent legacy edit: ' + relative)
            path.write_bytes(after)
            applied.append((path, before))
            receipt['files'][relative] = sha(after)
        receipt_path.write_text(dump(receipt), encoding='utf-8')
    except Exception:
        for path, before in reversed(applied):
            path.write_bytes(before)
        receipt_path.write_bytes(receipt_before)
        raise
    return len(changes)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    check = sub.add_parser('check')
    check.add_argument('--language', default='en')
    check.add_argument('--compatibility', action='store_true')
    syncing = sub.add_parser('sync')
    syncing.add_argument('--write', action='store_true')
    export = sub.add_parser('export')
    export.add_argument('--language', required=True)
    export.add_argument('--out', type=Path, required=True)
    export.add_argument('--fallback', help='Explicit fallback, recorded in the export audit')
    export.add_argument('--write', action='store_true')
    scaffold = sub.add_parser('add-language')
    scaffold.add_argument('language')
    scaffold.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.command == 'sync':
        sync(write=args.write)
        return
    catalog = Catalog(language=getattr(args, 'language', 'en')) if args.command != 'add-language' else Catalog()
    if args.command == 'check':
        counts, errors = catalog.validate()
        print(json.dumps(dict(language=catalog.language, counts=counts, issues=len(errors)), indent=2))
        for error in errors[:15]:
            print(error)
        if args.compatibility:
            print('Compatibility views checked:', catalog.check_compatibility())
        if errors:
            raise SystemExit(1)
    elif args.command == 'add-language':
        language = args.language
        require(re.fullmatch('[a-z]{2,3}(?:-[A-Z]{2})?', language), 'Use a locale code such as fr or pt-BR')
        require(language not in catalog.manifest['languages'], 'Language already registered')
        print('New language:', language, '- empty translations; no automatic English fallback')
        if not args.write:
            print('DRY RUN: add --write to create language files')
            return
        directory = safe_path(ROOT, 'localization/locales/' + language)
        require(not directory.exists(), 'Language directory exists')
        directory.mkdir()
        for group in catalog.manifest['groups']:
            definitions = catalog.document('localization/messages/'+group+'.json')['messages']
            rows = {mid: dict(text=None, status='missing') for mid in definitions}
            (directory / (group+'.json')).write_text(dump(dict(schema=1, language=language, messages=rows)), encoding='utf-8')
        catalog.manifest['languages'][language] = dict(status='incomplete', game_build_ready=False)
        (ROOT / 'localization/manifest.json').write_text(dump(catalog.manifest), encoding='utf-8')
    elif args.command == 'export':
        catalog = Catalog(language=args.language, fallback=args.fallback)
        out = args.out.resolve()
        require((ROOT / 'work').resolve() in out.parents and not out.exists(), 'Use a NEW work/ subfolder')
        bindings = catalog.document('platforms/ps3/localization/legacy.json')['documents']
        planned = {name: catalog.render(row['template']) for name, row in bindings.items()}
        ui = {key: catalog.render(row['template']) for key,row in
              catalog.document('platforms/ps3/localization/python.json')['literals'].items()}
        print('Compatibility export:', args.language, len(planned), 'documents; NOT a game build')
        if not args.write:
            print('DRY RUN: nothing written')
            return
        out.mkdir(parents=True)
        (out / 'LOCALIZATION_UI.json').write_text(dump(ui), encoding='utf-8')
        for name, value in planned.items():
            path = safe_path(out, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(dump(value) if bindings[name]['format']=='json' else value, encoding='utf-8')
        (out / 'LOCALIZATION_EXPORT.json').write_text(dump(dict(language=args.language, fallback=args.fallback,
            game_build_ready=False, documents=len(planned))), encoding='utf-8')


if __name__ == '__main__':
    main()
