"""One-time, lossless catalog import. Dry-run first; --write makes the migration.

IDs are minted once from original context, NEVER from translated wording.
Do not rerun to update existing translations; edit the locale files instead.
"""
import argparse
import ast
from collections import Counter, defaultdict
import copy
import hashlib
import json
from pathlib import Path
import re

from localization import ROOT, TOKEN, dump, require, sha

# Only reviewed text-bearing data assignments, not arbitrary Python strings.
UI = {
    'aboard_order_labels': 'ROWS', 'backlog_layout': 'EN',
    'battle_preview_layout': 'ROWS', 'battle_reports': 'HOOKS HELP ROWS',
    'combat_record_links': 'LINKS HELP',
    'command_layout': 'LABELS MORE_COMMANDS DIALOGS EXTRA_DIALOGS UTF8_LABELS TERRAIN FOLLOWUP_TERRAIN FOLLOWUP_LABELS SAVE_DIALOGS PREP_ROWS',
    'deployment_layout': 'ROWS', 'deployment_menu_text': 'ROWS',
    'eboot': 'UI_LABELS', 'episode_heading_hooks': 'EXTRA',
    'gift_reports': 'CONVERSIONS', 'intermission_layout': 'DESCRIPTIONS ROWS PARTS',
    'key_help_labels': 'LABELS SLOT_HELP_EN', 'library_list_labels': 'ROWS',
    'map_popup_layout': 'ROWS', 'maximum_break_art': 'ACTION_RECTS',
    'mech_info_layout': 'LABEL', 'menu_followup': 'PROMPTS',
    'message_class_formats': 'FORMATS', 'naming_search_layout': 'REPORTS ROWS',
    'narration_layout': 'PAGES', 'parts_description_catalog': 'DATA',
    'parts_menu_followup': 'ROWS', 'record_screen_labels': 'TARGETS ROWS TITLE_GROUPS',
    'roster_settings_layout': 'SUPPORT TABS', 'runtime_names': 'READERS',
    'save_prompt_layout': 'EN', 'scenario_title': 'TITLE',
    'search_layout': 'TAB_TEXT', 'search_list_headers': 'ROWS',
    'skill_description_catalog': 'DATA', 'tag_reward_layout': 'ROWS REWARDS HEADERS ACTION_ROWS',
    'team_roster_layout': 'ROWS', 'title_library_buttons': 'ROWS',
    'trader_art': 'CELLS', 'trade_list_flavor': 'TEXT', 'trader_ui': 'ROWS',
    'training_help_layout': 'ROWS', 'trophy_labels': 'NAME DETAIL',
    'ui_followup_layout': 'ROWS', 'unlock_reports': 'CONDITIONS PARTS',
    'upgrade_list_labels': 'ROWS', 'weapon_effect_labels': 'LABELS',
    'weapon_info_layout': 'LABEL', 'weapon_requirements': 'PREFIX HEADER LABELS',
}


def jp(text):
    return isinstance(text, str) and bool(re.search('[\u3040-\u30ff\u3400-\u9fff]', text))


def root_name(node):
    while isinstance(node, ast.Subscript):
        node = node.value
    return node.id if isinstance(node, ast.Name) else None


class Migration:
    def __init__(self, root=ROOT):
        self.root = Path(root)
        self.defs, self.en, self.vi = defaultdict(dict), defaultdict(dict), defaultdict(dict)
        self.documents, self.literals, self.rewrites = {}, {}, {}
        self.originals, self.files = {}, {}
        self.counts = Counter()

    def add(self, group, identity, text, source=None, kind='ui', context=None):
        # The original contextual anchor is only used at import time. The ID
        # persists in bindings even when translators later change the source.
        mid = group + ':r_' + sha(identity.encode('utf-8'))[:16]
        definition = dict(source=source, kind=kind, context=context or {},
                          source_status='available' if source is not None else 'not_extracted',
                          tokens=TOKEN.findall(text or ''), links=(text or '').count('《'),
                          link_closes=(text or '').count('》'))
        require(mid not in self.defs[group], 'ID collision: ' + mid)
        self.defs[group][mid] = definition
        self.en[group][mid] = dict(text=text, status='imported' if text is not None else 'missing')
        self.counts[kind] += 1
        return {'$message': mid}

    def json_view(self, path):
        name = path.relative_to(self.root).as_posix()
        group = ('glossary' if name == 'analysis/glossary.json' else
                 name[len('translation/'): -5].replace('/', '.'))
        original = json.loads(path.read_text(encoding='utf-8'))
        kind = ('dialogue' if group.startswith(('stage', 'suspend_scene')) else
                'battle_subtitle' if group.startswith('voice_') else
                'library' if group.startswith('library.') else
                'glossary' if group == 'glossary' else 'ui')
        vi_path = self.root / 'translation/vi' / path.name
        vi_original = json.loads(vi_path.read_text(encoding='utf-8')) if group.startswith('stage') and vi_path.exists() else None

        def walk(value, pointer='', parent=None):
            if isinstance(value, dict):
                require(not any(k in value for k in ('$message', '$join')), 'Reserved binding key: ' + name)
                out = {}
                for key, item in value.items():
                    loc = pointer + '/' + key.replace('~', '~0').replace('/', '~1')
                    is_text = (key == 'en' or
                               (pointer.startswith('/ENTRIES/') and isinstance(item, str)) or
                               (pointer == '/NAMES' and isinstance(item, str)) or
                               (not pointer and jp(key) and isinstance(item, str) and not key.startswith('_')))
                    if is_text and (item is None or isinstance(item, str)):
                        source = value.get('jp') if key == 'en' else key if jp(key) else None
                        context = {k: value[k] for k in ('event', 'n', 'pid', 'role', 'kind') if k in value}
                        out[key] = self.add(group, loc, item, source, kind, context)
                    elif key == 'expanded' and item == value.get('en') and 'en' in out:
                        out[key] = copy.deepcopy(out['en'])
                    elif key == 'expanded' and isinstance(item, str):
                        out[key] = self.add(group, loc, item, value.get('jp'), kind, {'variant':'expanded'})
                    else:
                        out[key] = walk(item, loc, value)
                return out
            if isinstance(value, list):
                if group == 'map_locations' and pointer.startswith('/rows/') and len(value) == 3:
                    return [value[0], value[1], self.add(group, pointer, value[2], value[1], 'image_text')]
                return [self.add(group, pointer+'/'+str(i), v, None, kind) if pointer == '/LINES' and isinstance(v,str)
                        else walk(v, pointer+'/'+str(i), value) for i,v in enumerate(value)]
            return value

        template = walk(original)
        self.documents[name] = dict(format='json', template=template)
        self.originals[name] = path.read_bytes()
        require(self.render(template) == original, 'JSON round trip: ' + name)
        if vi_original:
            vi_index = {(r['event'],r['n'],r['pid'],r['sha']): r for r in vi_original['LINES']}
            for src, bound in zip(original['LINES'], template['LINES']):
                key = (src['event'],src['n'],src['pid'],src['sha'])
                if key in vi_index:
                    require(vi_index[key]['jp'] == src['jp'], 'Vietnamese source differs')
                    mid = bound['en']['$message']
                    # Existing drafts predate tokenization. Preserve their exact
                    # words, but never pass them off as release-ready translations.
                    self.vi[group][mid] = dict(text=vi_index[key]['en'], status='needs_review')

    def render(self, value):
        if isinstance(value, dict):
            if set(value)=={'$message'}:
                mid=value['$message']; return self.en[mid.split(':')[0]][mid]['text']
            if set(value)=={'$join'}:
                return ''.join(self.render(v) for v in value['$join'])
            return {k:self.render(v) for k,v in value.items()}
        if isinstance(value, list):
            return [self.render(v) for v in value]
        return value

    def python_view(self, path, variables):
        raw = path.read_bytes()
        tree = ast.parse(raw)
        lines = raw.splitlines(keepends=True)
        starts = [0]
        for line in lines: starts.append(starts[-1]+len(line))
        selected = {}
        group = 'ui.' + path.stem
        skip = {'en','jp','lines','utf-8','cp932','cyan','purple','pink','gold'}

        def collect(node, var, source=None):
            # Dictionary keys are source lookup anchors, never translations.
            if isinstance(node, ast.Dict):
                for k,v in zip(node.keys,node.values):
                    hint=k.value if isinstance(k,ast.Constant) and jp(k.value) else source
                    collect(v,var,hint)
                return
            if isinstance(node,(ast.Tuple,ast.List)):
                for child in node.elts:
                    if isinstance(child,ast.Constant) and jp(child.value): source=child.value
                    collect(child,var,source)
                return
            if isinstance(node, ast.Constant) and isinstance(node.value,str):
                text = node.value
                # Pipe tables need per-entry IDs, not one giant translatable blob.
                table = '\n' in text and any('|' in line and jp(line.split('|')[0]) for line in text.splitlines())
                visible = re.sub(r'\$\$.*?\$\$', '', text)
                if table or (re.search('[A-Za-z]', visible) and not jp(visible) and text not in skip and len(text)>1):
                    selected[(node.lineno,node.col_offset)] = (node,var,table,source)
                return
            for child in ast.iter_child_nodes(node): collect(child,var,source)

        for node in ast.walk(tree):
            targets = node.targets if isinstance(node,ast.Assign) else [node.target] if isinstance(node,ast.AugAssign) else []
            for target in targets:
                var = root_name(target)
                if var in variables:
                    collect(node.value,var)
        if not selected: return
        edits=[]
        for number, (_, (node,var,table,source)) in enumerate(sorted(selected.items())):
            identity='%s/%d' % (var,number)
            value=node.value
            if table:
                pieces=[]
                for i,line in enumerate(value.splitlines(keepends=True)):
                    ending='\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
                    body=line[:-len(ending)] if ending else line
                    if '|' in body:
                        source,en=body.split('|',1)
                        pieces.extend([source+'|',self.add(group,identity+'/'+str(i),en,source,'ui',{'table':var}),ending])
                    else: pieces.append(line)
                template={'$join':pieces}
            else:
                template=self.add(group,identity,value,source,'ui',{'role':var})
            key=path.stem+'.'+identity
            self.literals[key]=dict(file=path.relative_to(self.root).as_posix(), variable=var, template=template)
            require(self.render(template)==value, 'Python literal round trip: '+key)
            a=starts[node.lineno-1]+node.col_offset
            b=starts[node.end_lineno-1]+node.end_col_offset
            edits.append((a,b,('_l10n.literal(%r)' % key).encode('ascii')))
        # Insert after module docstring and future imports (if present).
        anchor=0
        for node in tree.body:
            if (isinstance(node,ast.Expr) and isinstance(node.value,ast.Constant) and isinstance(node.value.value,str)) or (isinstance(node,ast.ImportFrom) and node.module=='__future__'):
                anchor=starts[node.end_lineno]
            else: break
        newline=b'\r\n' if b'\r\n' in raw else b'\n'
        edits.append((anchor,anchor,b'import localization as _l10n'+newline))
        out=raw
        for a,b,replacement in sorted(edits,reverse=True): out=out[:a]+replacement+out[b:]
        # Prove ALL non-text Python behavior remains structurally identical.
        owner=self
        class Restore(ast.NodeTransformer):
            def visit_Import(self,node):
                return None if len(node.names)==1 and node.names[0].name=='localization' and node.names[0].asname=='_l10n' else node
            def visit_Call(self,node):
                if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='_l10n':
                    return ast.Constant(value=owner.render(owner.literals[node.args[0].value]['template']), kind=None)
                return self.generic_visit(node)
        require(ast.dump(Restore().visit(ast.parse(out)))==ast.dump(tree), 'Python AST round trip: '+str(path))
        self.rewrites[path.relative_to(self.root).as_posix()] = out
        self.originals[path.relative_to(self.root).as_posix()] = raw

    def plan(self):
        require(not (self.root/'localization/manifest.json').exists(), 'Already migrated; edit locale files, do not regenerate IDs')
        for path in sorted((self.root/'translation').rglob('*.json')):
            if 'vi' not in path.relative_to(self.root/'translation').parts:
                self.json_view(path)
        self.json_view(self.root/'analysis/glossary.json')
        path=self.root/'translation/scenario_titles.tsv'
        if path.exists():
            raw=path.read_bytes(); text=raw.decode('utf-8'); pieces=[]
            for i,line in enumerate(text.splitlines(keepends=True)):
                if i and len(line.rstrip('\r\n').split('\t'))==3:
                    member,source,en=line.rstrip('\r\n').split('\t')
                    ending=line[len(line.rstrip('\r\n')):]
                    pieces.extend([member+'\t'+source+'\t',self.add('scenario_titles',member,en,source,'stage_title'),ending])
                else: pieces.append(line)
            self.documents['translation/scenario_titles.tsv']=dict(format='text',template={'$join':pieces})
            self.originals['translation/scenario_titles.tsv']=raw
            require(self.render({'$join':pieces})==text,'TSV round trip')
        for module,variables in UI.items():
            self.python_view(self.root/'tools'/(module+'.py'),set(variables.split()))
        for group in self.defs:
            self.files['localization/messages/'+group+'.json']=dict(schema=1,messages=self.defs[group])
            self.files['localization/locales/en/'+group+'.json']=dict(schema=1,language='en',messages=self.en[group])
        for group,rows in self.vi.items():
            self.files['localization/locales/vi/'+group+'.json']=dict(schema=1,language='vi',messages=rows)
        self.files['localization/manifest.json']=dict(schema=1,source_language='ja',default_language='en',
            groups=sorted(self.defs),languages={'en':{'status':'imported','game_build_ready':False},
                                             'vi':{'status':'draft_needs_review','game_build_ready':False}},
            coverage='Existing extracted translations and reviewed UI tables only; not an exhaustive game inventory.')
        self.files['platforms/ps3/localization/legacy.json']=dict(schema=1,documents=self.documents)
        self.files['platforms/ps3/localization/python.json']=dict(schema=1,literals=self.literals)
        self.files['platforms/vita/localization/bindings.json']=dict(schema=1,
            adapter='platforms/vita/build_test.py:load_inputs',
            shared_groups=['stage0001a','stage0001b_03','stage0001b_04','glossary'],
            matching='event + ordinal + speaker + Japanese fingerprint; no PS3 offsets',
            other_categories='Shared text available; Vita bindings not yet verified',
            vwf='Source/development candidate only; not runtime verified')
        self.files['localization/compatibility.json']=dict(schema=1,files={n:sha(self.originals[n]) for n in self.documents})
        self.files['localization/migration.json']=dict(schema=1,counts=dict(self.counts),
            legacy_documents=len(self.documents),python_modules=len(self.rewrites),python_literals=len(self.literals),
            vietnamese_drafts=sum(map(len,self.vi.values())),
            original_sha256={n:sha(b) for n,b in sorted(self.originals.items())},
            limitations=['Recorded voice audio is not text and is not dubbed.',
                         'Raster logos remain artwork; their lettering requires per-language asset production.',
                         'Python inventory is an explicit reviewed-table allowlist, not proof that all UI text is extracted.',
                         'Other-language game builds require font, layout and executable adapter validation.'])
        return self

    def write(self):
        backup=self.root/'work/localization/migration_backup'
        require(not backup.exists(),'Migration backup already exists')
        for name,raw in self.originals.items():
            require((self.root/name).read_bytes()==raw,'Source changed during migration: '+name)
        for name,value in self.files.items():
            require(not (self.root/name).exists(),'Destination already exists: '+name)
        # Back up before rewriting any source; all paths are workspace-relative.
        for name in self.rewrites:
            target=backup/name; target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(self.originals[name])
        for name,value in self.files.items():
            target=self.root/name; target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(dump(value),encoding='utf-8')
        for name,value in self.rewrites.items(): (self.root/name).write_bytes(value)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--write',action='store_true')
    args=ap.parse_args(); migration=Migration().plan()
    print(json.dumps(dict(mode='WRITE' if args.write else 'DRY RUN',counts=migration.counts,
                         documents=len(migration.documents),modules=len(migration.rewrites),literals=len(migration.literals)),indent=2))
    if args.write: migration.write()
