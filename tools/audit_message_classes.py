"""Source-driven inventory of message families, independent of translations."""
import json
import re
from pathlib import Path
from cpk import CPK

ROOT = Path(__file__).resolve().parent.parent


def role_neutral(jp, en):
    """A turn boundary is the same event in either condition panel."""
    match = re.fullmatch(r'([０-９]+)ターン目を迎える。', jp)
    return bool(match and en == 'Turn %d begins.' % int(match[1]))

def preset_text(cpk, path):
    """Find the named preset, not a fixed member ordinal (68 uses member 3)."""
    path = Path(path)
    expected = ('out/stage' + path.stem[3:].lower() + 'preset.lua').encode('ascii')
    candidates = []
    has_table = False
    for entry in cpk.files:
        blob = cpk.read(entry)
        has_table |= re.search(rb'\bOPERATE_TBL\s*=', blob) is not None
        if expected in blob[:4096]:
            candidates.append((entry['id'], blob.decode('cp932')))
    assert len(candidates) <= 1, ('ambiguous mission preset', path, [i for i, _ in candidates])
    if candidates:
        return candidates[0][1]
    assert not has_table, ('objective table without named preset', path)
    # Keep the existing strict exceptions for dialogue-only route archives.
    if path.stem in {'STG0210', 'STG0230', 'STG0240', 'STG0260'}:
        assert {item['id'] for item in cpk.files} == {0, 2, 3, 4}, path
        return None
    entry = next((f for f in cpk.files if f['id'] == 1), None)
    # Ace congratulations are dialogue-only, not a map objective preset.
    if path.stem == 'STG0500':
        assert {item['id'] for item in cpk.files} == {0, 1}, path
        text = cpk.read(entry).decode('cp932')
        assert 'Csz3_0500_SDemo.Cpp' in text and 'ハッピー・エースパイロット' in text, path
        assert 'OPERATE_TBL' not in text, path
        return None
    # STG0700 is the post-save end-session scenes: dialogue only, no map
    if path.stem == 'STG0700':
        text = cpk.read(entry).decode('cp932')
        assert 'OPERATE_TBL' not in text and 't_000' in text, path
        return None
    if entry is not None and re.fullmatch(r'STG02\d{2}', path.stem):
        text = cpk.read(entry).decode('cp932')
        assert 'OPERATE_TBL' not in text and 'SC_PROCESS_STAGE_CLEAR' in text, path
        return None
    raise AssertionError(('missing mission preset', path))


def strings(blob, start, end):
    for match in re.finditer(rb'[^\0]+', blob[start:end]):
        yield start + match.start(), match.group().decode('cp932')

def inventory():
    rows = {}
    def add(kind, jp, source):
        rows.setdefault((kind, jp), []).append(source)
    elf = (ROOT / 'work/EBOOT_dec.elf').read_bytes()
    import episode_heading_hooks
    for jp in episode_heading_hooks.hooks():
        add('episode-heading',jp,'EBOOT episode/title metadata')
    # Independently locate every shop requirement, including wrapped forms.
    for match in re.finditer(rb'[^\0]+', elf):
        raw = match.group()
        if raw.startswith('商品開放条件\n'.encode('cp932')):
            add('unlock-shop', raw.decode('cp932'), 'EBOOT:%x' % match.start())
    for off, jp in strings(elf, 0x70d6f0, 0x70d970):
        add('unlock', '『' + jp + '』を達成', 'EBOOT:%x' % off)
    for off, jp in strings(elf, 0x6e4f30, 0x6e5028):
        if '%s' not in jp:
            add('reward', jp, 'EBOOT:%x' % off)
    import battle_reports, message_class_formats
    format_offsets = {battle_reports.FORMAT_OFF} | set(message_class_formats.FORMATS)
    assert {off for off, jp in strings(elf, 0x6e4f30, 0x6e5028) if '%s' in jp} == format_offsets
    for off, jp in strings(elf, 0x711510, 0x7115b0):
        add('effect', jp, 'EBOOT:%x' % off)
        if jp.rstrip('　 ') != jp:
            add('effect', jp.rstrip('　 '), 'EBOOT:%x trimmed' % off)
    stages = sorted((ROOT / 'work/stage_dec').glob('STG*.cpk'))
    for path in stages:
        cpk = CPK(str(path))
        text = preset_text(cpk, path)
        if text is None:
            continue
        import squad_names
        for jp in squad_names.names(text):
            add('squad-name',jp,path.name)
        match = re.search(r'OPERATE_TBL\s*=\s*\{.*?str_tbl\s*=\s*\{(.*?)\};', text, re.S)
        # Do not silently omit a stage when the source format changes.
        if not match:
            assert '-- 作戦目的テーブルはありません。' in text and 'OPERATE_TBL' not in text, path
            continue
        raw = re.findall(r'"((?:\\.|[^"\\])*)"', match[1])
        assert raw, path
        for value in raw:
            jp = value.replace('\\n', '\n')
            import mission_conditions
            variants = mission_conditions.displayed_variants(jp)
            for variant in variants:
                for prefix in ('', '１．', '２．', '３．'):
                    full = prefix + variant
                    add('mission', full, path.name)
                    for line in full.split('\n'):
                        if len(line.strip('　 ')) >= 6:
                            add('mission', line.strip('　 '), path.name + ' per-line')
    return [{'class': kind, 'jp': jp, 'sources': sorted(set(sources))}
            for (kind, jp), sources in sorted(rows.items())], [p.name for p in stages]

def check(hooks, mapping=None, widths=None, allow_untranslated_missions=False):
    rows, stages = inventory()
    missing = [row for row in rows if row['jp'] not in hooks]
    required_missing = [row for row in missing
                        if not allow_untranslated_missions or row['class'] != 'mission']
    assert not required_missing, 'Untranslated source messages: ' + json.dumps(required_missing, ensure_ascii=False)
    for row in rows:
        if row['jp'] not in hooks:
            continue  # Explicit partial-build mode; listed in returned coverage.
        assert not re.search(r'[ぁ-んァ-ヶ一-龯]', hooks[row['jp']]), row
    check_roles(hooks, allow_untranslated_missions=allow_untranslated_missions)
    if mapping is not None:
        from intermission_layout import ink
        for row in rows:
            if row['jp'] not in hooks:
                continue
            size, limit = (31, 300) if row['class'] == 'effect' else (28, 850)
            for line in hooks[row['jp']].split('\n'):
                assert ink(line, mapping, widths, size) < limit, (row['jp'], line)
    print('PASS: %d translated source variants validated across %d archives; %d untranslated mission variants recorded.' % (len(rows)-len(missing), len(stages), len(missing)))
    return {'complete': not missing, 'partial_translation': allow_untranslated_missions,
            'source_variants': len(rows), 'translated_variants': len(rows)-len(missing),
            'missing_count': len(missing), 'missing': missing, 'stages': stages}


def check_roles(hooks, allow_untranslated_missions=False):
    """Resolve actual operation-table roles, not the Japanese noun suffix."""
    import collections
    counts = collections.Counter()
    roles = collections.defaultdict(set)
    for path in sorted((ROOT / 'work/stage_dec').glob('STG*.cpk')):
        cpk = CPK(str(path))
        text = preset_text(cpk, path)
        if text is None:
            continue
        m = re.search(r'OPERATE_TBL\s*=\s*\{.*?str_tbl\s*=\s*\{(.*?)\};.*?id_tbl\s*=\s*\{(.*?)\};', text, re.S)
        if not m:
            assert '作戦目的テーブルはありません。' in text and 'OPERATE_TBL' not in text, path
            continue
        ss = [s.replace('\\n', '\n') for s in re.findall(r'"((?:\\.|[^"\\])*)"', m[1])]
        tokens = re.findall(r'true|false|-?\d+', re.sub(r'--[^\r\n]*', '', m[2]))
        assert len(tokens) % 8 == 0, path
        for start in range(0, len(tokens), 8):
            assert tokens[start] in {'true', 'false'}, path
            for role, values in [('victory', tokens[start+1:start+4]),
                                 ('defeat', tokens[start+4:start+7]),
                                 ('sr', tokens[start+7:start+8])]:
                for value in values:
                    if int(value) < 0:
                        continue
                    jp = ss[int(value)]
                    roles[jp].add(role)
                    counts[role] += 1
                    if allow_untranslated_missions and jp not in hooks:
                        continue
                    en = hooks[jp]
                    if role == 'victory' and jp.endswith('の撃墜。'):
                        assert en.startswith('Shoot down '), (path, role, jp, en)
                    if role == 'defeat':
                        assert not en.startswith(('Shoot down ', 'Defeat ', 'Destroy ')), (path, role, jp, en)
                        if '撃墜' in jp:
                            assert 'is shot down' in en, (path, role, jp, en)
    conflicts = [jp for jp, value in roles.items() if {'victory', 'defeat'} <= value
                 and (not allow_untranslated_missions or jp in hooks)
                 and not role_neutral(jp, hooks.get(jp))]
    assert not conflicts, ('shared role needs context-specific keys', conflicts)
    doc = json.loads((ROOT / 'translation/mission_conditions_hook.json').read_text(encoding='utf-8'))
    for row in doc['lines']:
        assert row['role'] in roles[row['jp']], row
    import mission_conditions
    for row in mission_conditions.additional_lines():
        assert row['role'] in roles[row['jp']], row
    print('PASS: operation roles:', dict(counts), '; victory and defeat wording distinct.')

if __name__ == '__main__':
    import eboot, trdata
    trdata.use_glossary(str(ROOT / 'analysis/glossary.json'))
    hooks = eboot.load_ui_hook()
    rows, stages = inventory()
    missing = [row for row in rows if row['jp'] not in hooks]
    print('Scanned', len(stages), 'stages;', len(rows), 'variants;', len(missing), 'missing')
    for row in missing:
        print(row['class'], repr(row['jp']), ','.join(row['sources'][:2]))
