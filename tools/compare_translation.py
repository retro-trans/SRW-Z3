"""Offline, side-by-side review of the current canonical localization catalog.

Dry-run by default. --write creates a NEW HTML file below work/; never edits
translations, extracts a disc, builds a game, uploads data or opens a browser.
This shows working-copy text, not proof of what a released patch contains.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import fnmatch
import json
from pathlib import Path
import sys

import localization as L
import terms

FILTERS = ('all', 'untranslated', 'source-unavailable', 'needs-review',
           'invalid', 'same-as-source', 'blank')

# These legacy description generators use $$name$$ for their dedicated name
# dictionaries, not the prose glossary. Preserve their exact scope/precedence.
NAME_DICTIONARIES = {
    'ui.parts_description_catalog': ('spirits',),
    'ui.skill_description_catalog': ('skills', 'spirits'),
}


def glossary_index(catalog):
    """Keep missing target terms visible; never borrow the English glossary."""
    if 'glossary' not in catalog.manifest['groups']:
        return {}
    locale = catalog.locale(catalog.language, 'glossary')
    # Discriminators such as Rei #333 are metadata in the compatibility
    # template, not in the abbreviated message context. Keep that identity,
    # but fetch every English/other-language value from canonical locale rows.
    template = catalog.document('platforms/ps3/localization/legacy.json')['documents'][
        'analysis/glossary.json']['template']
    entries = []
    for definition in template['terms']:
        mid = definition['en']['$message']
        row = locale.get(mid, {})
        entries.append(dict(definition, en=row.get('text'),
                            status=row.get('status', 'missing')))
    return terms.index({'terms': entries})


def expand(text, index, issues):
    if text is None:
        return None
    try:
        for token in terms.TOKEN.finditer(text):
            term = terms.resolve(token[1], token[2], index)
            if not isinstance(term['en'], str) or term['status'] == 'missing':
                raise ValueError('Missing locale glossary term: ' + token[0])
            if term['status'] == 'needs_review':
                issues.append('Glossary term needs review: ' + token[0])
        if terms.stray(text):
            raise ValueError('Unparsed glossary token')
        return terms.expand(text, index)
    except (ValueError, SystemExit) as error:
        issues.append(str(error))
        return None


def dictionary_index(catalog, groups):
    index = {}
    for group in groups:
        if group not in catalog.manifest['groups']:
            continue
        definitions = catalog.document('localization/messages/'+group+'.json')['messages']
        locale = catalog.locale(catalog.language, group)
        for mid, definition in definitions.items():
            entry = locale.get(mid, {})
            jp = definition.get('source')
            if jp is not None:
                index[jp] = [dict(jp=jp, en=entry.get('text'), kind='keyword',
                                  status=entry.get('status', 'missing'))]
    return index


def collect(catalog, patterns=(), kinds=()):
    groups = []
    for pattern in patterns or ('*',):
        hits = [g for g in catalog.manifest['groups'] if fnmatch.fnmatchcase(g, pattern)]
        L.require(hits, 'No catalog groups match: ' + pattern)
        groups.extend(g for g in hits if g not in groups)
    index = glossary_index(catalog)
    rows = []
    for group in groups:
        row_index = (dictionary_index(catalog, NAME_DICTIONARIES[group])
                     if group in NAME_DICTIONARIES else index)
        definitions = catalog.document('localization/messages/'+group+'.json')['messages']
        locale = catalog.locale(catalog.language, group)
        L.require(not (locale.keys() - definitions.keys()), 'Unknown locale IDs in ' + group)
        for mid, definition in definitions.items():
            if kinds and definition['kind'] not in kinds:
                continue
            entry = locale.get(mid, {})
            target = entry.get('text')
            L.require(target is None or isinstance(target, str), 'Non-string translation: '+mid)
            source = definition.get('source')
            L.require(source is None or isinstance(source, str), 'Non-string source: '+mid)
            status = entry.get('status', 'missing')
            flags, issues = [], []
            if target is None or status == 'missing':
                flags.append('untranslated')
            if source is None or definition.get('source_status') != 'available':
                flags.append('source-unavailable')
            if status == 'needs_review':
                flags.append('needs-review')
            if target == '':
                flags.append('blank')
            try:
                catalog.text(mid)
            except ValueError as error:
                if status not in ('missing', 'needs_review') and target is not None:
                    issues.append(str(error))
            expanded = expand(target, row_index, issues)
            if source and expanded == source and 'source-unavailable' not in flags:
                flags.append('same-as-source')
            if issues:
                flags.append('invalid')
            rows.append(dict(id=mid, group=group, kind=definition['kind'],
                             source=source, source_status=definition.get('source_status'),
                             target=target, expanded=expanded, status=status,
                             flags=flags, issues=issues, context=definition.get('context', {}),
                             path='localization/locales/%s/%s.json' % (catalog.language, group)))
    return rows


def select(rows, only='all', search=''):
    query = search.casefold()
    return [r for r in rows if (only == 'all' or only in r['flags']) and
            (not query or query in '\n'.join((r['id'], r['source'] or '',
              r['target'] or '', r['expanded'] or '', json.dumps(r['context'], ensure_ascii=False))).casefold())]


def render(rows, language):
    payload = json.dumps(dict(language=language, generated=datetime.now(timezone.utc).isoformat(),
                              rows=rows), ensure_ascii=False, separators=(',', ':'))
    # A string containing </script> must never escape the inert JSON element.
    for raw, escaped in (('&', '\\u0026'), ('<', '\\u003c'), ('>', '\\u003e'),
                         ('\u2028', '\\u2028'), ('\u2029', '\\u2029')):
        payload = payload.replace(raw, escaped)
    return TEMPLATE.replace('@@DATA@@', payload)


TEMPLATE = '''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>SRW Z3 — Check the translation</title>
<style>
:root{font-family:system-ui,sans-serif;color:#e8edf3;background:#121820;color-scheme:dark}
body{margin:0 auto;padding:24px;max-width:1500px}h1{margin-bottom:8px}p{line-height:1.5}
.note{color:#b7c5d5;max-width:1100px}header{border-bottom:1px solid #394859;padding-bottom:16px}
.filters{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}label{display:flex;flex-direction:column;gap:5px}
input,select,button{font:inherit;padding:9px;border:1px solid #59697c;border-radius:5px;background:#202b38;color:inherit}
input{min-width:280px}button{cursor:pointer}button:disabled{opacity:.4;cursor:default}
nav{display:flex;gap:16px;align-items:center;margin:16px 0}.row{border:1px solid #3b4b5e;border-radius:7px;margin:16px 0;overflow:hidden}
.meta{padding:12px;background:#202b38;overflow-wrap:anywhere}.meta small{display:block;color:#b7c5d5;margin-top:5px}
.columns{display:grid;grid-template-columns:1fr 1fr}.cell{padding:16px;min-width:0}.cell+ .cell{border-left:1px solid #3b4b5e}
.cell h2{font-size:13px;color:#9ccde8;margin:0 0 10px}pre{font:inherit;line-height:1.6;white-space:pre-wrap;overflow-wrap:anywhere;margin:0}
details{margin-top:12px}summary{cursor:pointer;color:#b7c5d5}.issue{color:#ffc18a}.empty{padding:24px;border:1px dashed #59697c}
@media(max-width:720px){body{padding:12px}.columns{grid-template-columns:1fr}.cell+ .cell{border-left:0;border-top:1px solid #3b4b5e}input{min-width:0;width:100%;box-sizing:border-box}}
</style>
<header><h1>Check the translation</h1>
<p class="note">Current SRW Z3 catalog, not a released-patch inspection or a complete inventory of every in-game string.
Japanese comes from recorded source entries. Missing source is not a missing translation.
Glossary references are expanded in the selected language; runtime names such as $n stay symbolic.
No English fallback. Everything on this page works offline.</p>
<p class="note">Untranslated = absent/null text or an explicit missing status. Blank entries may intentionally hide UI labels.
Same-as-source entries may be names or codes, not errors. Imported/translated/reviewed are catalog statuses,
not proof of human review or in-game validation. This report does not edit files.</p><div id="scope"></div></header>
<div class="filters">
<label>Search Japanese, translation, ID or context<input id="search" type="search" placeholder="Name, phrase, or message ID"></label>
<label>Group<select id="group"><option value="">All groups</option></select></label>
<label>Category<select id="kind"><option value="">All categories</option></select></label>
<label>Show<select id="only"><option value="all">All entries</option>
<option value="untranslated">Untranslated</option><option value="source-unavailable">Source unavailable</option>
<option value="needs-review">Needs review</option><option value="invalid">Validation issues</option>
<option value="same-as-source">Same as source</option><option value="blank">Blank target</option></select></label>
</div>
<nav aria-label="Pages"><button id="prev">Previous</button><span id="count" role="status"></span><button id="next">Next</button></nav>
<main id="results"></main><noscript>Enable JavaScript to filter and display this local report.</noscript>
<script type="application/json" id="data">@@DATA@@</script>
<script>
'use strict';
const data=JSON.parse(document.getElementById('data').textContent);
const el=id=>document.getElementById(id), pageSize=50;
let page=0, filtered=data.rows;
const node=(tag,text,cls)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
el('scope').textContent=`Language: ${data.language} | ${data.rows.length.toLocaleString()} entries in this report | Generated ${data.generated}`;
for(const field of ['group','kind'])for(const value of [...new Set(data.rows.map(r=>r[field]))].sort()){
 const option=node('option',value);option.value=value;el(field).append(option);
}
function render(){
 const start=page*pageSize, end=Math.min(start+pageSize,filtered.length);
 el('count').textContent=filtered.length?`${start+1}–${end} of ${filtered.length.toLocaleString()} entries`:'0 entries';
 el('prev').disabled=page===0;el('next').disabled=end>=filtered.length;
 el('results').replaceChildren();
 if(!filtered.length)el('results').append(node('p','No entries match these filters.','empty'));
 for(const row of filtered.slice(start,end)){
  const card=node('article',undefined,'row'),meta=node('div',row.id,'meta');
  meta.append(node('small',`${row.kind} | ${row.status} | ${row.flags.join(', ')||'Text present'}`));
  meta.append(node('small',row.path));meta.append(node('small',JSON.stringify(row.context)));
  card.append(meta);const cols=node('div',undefined,'columns');
  for(const [title,text] of [['Japanese source',row.source??'[Source unavailable]'],
    [`Translation (${data.language})`,row.expanded??row.target??'[No translation]']]){
   const cell=node('section',undefined,'cell');cell.append(node('h2',title),node('pre',text===''?'[Blank entry]':text));cols.append(cell);
  }
  if(row.target!==null&&row.target!==row.expanded){const details=node('details');details.append(node('summary','Raw catalog text'),node('pre',row.target));cols.lastChild.append(details);}
  if(row.flags.includes('source-unavailable'))cols.firstChild.append(node('p','Source unavailable or not verified as available in the catalog.','issue'));
  for(const issue of row.issues)cols.lastChild.append(node('p',issue,'issue'));
  card.append(cols);el('results').append(card);
 }
}
function filter(){
 const query=el('search').value.toLocaleLowerCase(),group=el('group').value,kind=el('kind').value,only=el('only').value;
 filtered=data.rows.filter(r=>(!group||r.group===group)&&(!kind||r.kind===kind)&&(only==='all'||r.flags.includes(only))&&
  (!query||[r.id,r.source,r.target,r.expanded,JSON.stringify(r.context)].join(' ').toLocaleLowerCase().includes(query)));
 page=0;render();
}
let timer;el('search').addEventListener('input',()=>{clearTimeout(timer);timer=setTimeout(filter,120);});
for(const id of ['group','kind','only'])el(id).addEventListener('change',filter);
el('prev').addEventListener('click',()=>{if(page>0){page--;render();}});
el('next').addEventListener('click',()=>{if((page+1)*pageSize<filtered.length){page++;render();}});
render();
</script></html>
'''


def main(argv=None, root=L.ROOT):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', default='en')
    parser.add_argument('--group', action='append', default=[], help='Group or quoted glob; repeatable')
    parser.add_argument('--kind', action='append', default=[], help='Catalog category; repeatable')
    parser.add_argument('--only', choices=FILTERS, default='all')
    parser.add_argument('--search', default='')
    parser.add_argument('--out', type=Path, default=Path('work/translation-review.html'))
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args(argv)
    try:
        catalog = L.Catalog(root, args.language)
        rows = collect(catalog, args.group, args.kind)
        if args.kind:
            found = {r['kind'] for r in rows}
            L.require(set(args.kind) <= found, 'No entries for requested category in selected groups')
        rows = select(rows, args.only, args.search)
        out = args.out.resolve()
        L.require((Path(root).resolve()/'work') in out.parents and out.suffix.lower()=='.html',
                  'Use a NEW .html file below work/')
        L.require(not out.exists(), 'Output already exists; choose a new --out file')
        print('Catalog review: %s, %d entries (not a game-build coverage claim)' % (args.language,len(rows)))
        print('Flags (can overlap):', dict(Counter(f for row in rows for f in row['flags'])))
        print('Sample IDs:', ', '.join(r['id'] for r in rows[:3]) or '(none)')
        if not args.write:
            print('DRY RUN: nothing written. Repeat with --write to create', out)
            return 0
        html = render(rows, args.language)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(html)
        print('Open in a browser:', out)
        return 0
    except (OSError, ValueError) as error:
        print('Error:', error, file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
