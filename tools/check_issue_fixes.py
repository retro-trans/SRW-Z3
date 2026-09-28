"""Regression checks for the GitHub UI repair batch (game data is read-only).

Requires the existing built EBOOT and mapping. Verifies binary hook entries,
source matches, glyph encoding and width; it does not claim in-game visual QA.
Writes message_coverage.json beside the checked build for release metadata.
Run: python -X utf8 tools/check_issue_fixes.py
"""
import json
import struct
import argparse
import re
import unicodedata
from pathlib import Path

import aiddata
import digraph as dg
import eboot
import trdata
from cpk import CPK


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='work/out')
    parser.add_argument('--version', help='expected title footer version for an unstamped build')
    parser.add_argument('--partial-translation', action='store_true',
                        help='audit untranslated mission text as a documented backlog, not a complete-translation claim')
    args = parser.parse_args()
    out = Path(args.out)
    from cpkpatch import validate_itoc
    stage_archives = sorted(out.glob('STG*.cpk'))
    assert stage_archives, 'No stage archives to validate'
    for archive in stage_archives:
        validate_itoc(archive.read_bytes())
    print('PASS: %d stage archives have consistent ITOC lengths and member counts.' % len(stage_archives))
    trdata.use_glossary('analysis/glossary.json')
    dg.use_letters('E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF', cap=22, dilate=.5)
    mapping = {(k if len(k) == 1 else tuple(k)): v for k, v in json.loads((out / 'pairs.json').read_text()).items()}
    import patch_library_cv_candidate as library_cv_check
    cv_widths = {int(k): v for k, v in json.loads((out / 'widths.json').read_text()).items()}
    _, cv_changes, cv_rows = library_cv_check.plan(
        CPK(str(library_cv_check.SOURCE)), CPK(str(out / 'MTZKN_PT.CPK')), mapping, cv_widths)
    assert not cv_changes, 'Library CV output differs from the catalog'
    print('PASS: all %d Library CV fields use current font cells and fit header widths.' % len(cv_rows))
    hooks = eboot.load_ui_hook()
    batch_hooks = eboot.load_ui_hook(['translation/issue_hook.json'])
    for jp in ['ユニット', 'Ｚチップ', '獲得資金', '消費ＥＮ']:
        batch_hooks[jp] = hooks[jp]
    for path in eboot.UI_HOOK_FILES:
        rows = json.loads(Path(path).read_text(encoding='utf-8'))['lines']
        seen = {}
        for row in rows:
            assert row['jp'] not in seen or seen[row['jp']] == row['en'], (path, row['jp'])
            seen[row['jp']] = row['en']
    for jp, en in hooks.items():
        assert '$$' not in en
        eboot._encode_marked(en, mapping)
    b = (out / 'EBOOT.BIN').read_bytes()
    import president_report_layout
    president_report_layout.check(b,mapping)
    import weapon_requirement_runtime
    weapon_requirement_runtime.check(b,mapping,cv_widths)
    import support_badge
    original_tpack = CPK('work/TPACKPS3.CPK')
    built_tpack = CPK(str(out / 'TPACKPS3.CPK'))
    def member(cpk, ident):
        return cpk.read(next(f for f in cpk.files if f['id'] == ident))
    support_badge.verify(member(original_tpack, 2), member(built_tpack, 2), dg.LETTER_FACE.path)
    support_badge.verify_attack_reader(b)
    print('PASS: all four AT map badges; original numerals and other map textures unchanged.')
    from check_runtime_names import check as check_runtime_names
    check_runtime_names(b, mapping)
    segs = eboot._segments(b)
    def zstr(va):
        off = eboot._off(segs, va)
        return b[off:b.index(b'\0', off)]
    entries = {}
    p = eboot._off(segs, eboot.NAME_TBL)
    while True:
        key, target = struct.unpack_from('>II', b, p)
        if not key:
            break
        entries.setdefault(zstr(key), (target & 0xc0000000, zstr(target & 0x3fffffff)))
        p += 8
    # the table owns NAME_TBL..NAME_STR: 8-byte rows plus a zero terminator.
    # Derived from eboot's layout, not a constant, so a repartition of the
    # extension cannot leave this check asserting the old capacity.
    capacity = (eboot.NAME_STR - eboot.NAME_TBL) // 8 - 1
    assert len(entries) <= capacity, (len(entries), capacity)
    assert p + 8 <= eboot._off(segs, eboot.NAME_STR), 'name table overruns its region'
    # strings now start right after the emitted table: none may overlap it
    q, first = eboot._off(segs, eboot.NAME_TBL), None
    while struct.unpack_from('>I', b, q)[0]:
        eo = eboot._off(segs, struct.unpack_from('>I', b, q + 4)[0] & 0x3fffffff)
        if eo >= eboot._off(segs, eboot.EXT_VA):
            first = eo if first is None else min(first, eo)
        q += 8
    assert first is None or first >= p + 8, 'hook strings overlap the table'
    squad_rows=json.loads(Path('translation/squad_names_hook.json').read_text(encoding='utf-8'))['lines']
    for row in squad_rows:
        assert entries[row['jp'].encode('cp932')][0]&0x40000000,row['jp']
    for jp, en in dict(hooks, **batch_hooks).items():
        key = eboot._encode_marked(jp, mapping) if jp in eboot.UI_KEY_VWF else jp.encode('cp932')
        import command_layout
        assert entries[key][1] == command_layout.dialog_prefix(jp) + eboot._encode_marked(en, mapping), jp
    # Date cards are composed before drawing, so match the complete result,
    # not the printf template or a generic month/day substring.
    date_rows=json.loads(Path('translation/date_cards.json').read_text(encoding='utf-8'))['lines']
    pristine=Path('work/EBOOT_dec.elf').read_bytes()
    prefix='新多元世紀０００１年'
    assert pristine[0x6e5048:].startswith((prefix+'%s\0').encode('cp932'))
    expected_dates={}
    months=['','January','February','March','April','May','June','July',
            'August','September','October','November','December']
    for raw in pristine[0x6ef5d0:0x6f0000].split(b'\0'):
        text=raw.decode('cp932',errors='replace')
        match=re.fullmatch(r' *([0-9]+)月 *([0-9]+)日',unicodedata.normalize('NFKC',text))
        if match:
            month,day=map(int,match.groups())
            expected_dates[prefix+text]=f'New Multidimensional Century 0001 - {months[month]} {day}'
    assert len(date_rows)==len(expected_dates)==77
    assert {r['jp']:r['en'] for r in date_rows}==expected_dates
    for jp,en in expected_dates.items():
        assert hooks[jp]==en and dg.line_px(en)<=1000
    # Calendar strings/format remain pristine; only draw-time translation changes.
    assert b[0x6ef5d0:0x6f0000]==pristine[0x6ef5d0:0x6f0000]
    assert b[0x6e5048:0x6e5064]==pristine[0x6e5048:0x6e5064]
    print('PASS: 77 complete date cards, including April 10/15; calendar values/format unchanged.')
    for n in [0, 1, 9, 10, 99]:
        wide = str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
        jp = '行動終了していないチームが' + wide + 'チームあります。'
        assert hooks[jp] == f'Teams still able to act: {n}.'
    k = CPK('work/orig/AIDDATAPACK.CPK')
    pool = k.read(k.files[0])
    # Four FSSA Yes/No variants draw an inactive row then an active choice.
    # Keep their original positions; VWF spacers restore the original columns.
    choice = entries['はい　／　いいえ'.encode('cp932')][1]
    assert choice == dg.encode_mixed('Yes\ue01e/\ue01fNo', mapping)
    widths = b[eboot._off(segs, eboot.TABLE_VA):][:eboot.ATLAS_CELLS]
    # STG0700 (end-session scenes) is an ordinary manifest stage now; the
    # stage build verifies it like every other archive.
    import trophy_labels
    trophy_labels.verify(trophy_labels.SOURCE.read_bytes(),(out/'TROPHY.TRP').read_bytes())
    from check_confirmation_tabs import check as check_confirmation_tabs
    check_confirmation_tabs(b, mapping)
    for cp in ('\ue01e', '\ue01f'):
        text, code = dg.TINY_CELLS[cp]
        assert not any(dg.raster_tiny(text, code)), 'Spacer must be invisible'
        assert widths[dg.cell_index(code)] == 32  # tabs are intercepted before width lookup
    for row, active, jp, col in [(0xa9bd4,0xa9bf4,'はい',0),
                                 (0xa9c14,0xa9c34,'いいえ',5),
                                 (0xa9c54,0xa9c74,'はい',0),
                                 (0xa9c94,0xa9cb4,'いいえ',5)]:
        assert pool[row+16:row+20] == pool[active+16:active+20] == bytes.fromhex('19191719')
        base = struct.unpack_from('>f',pool,row+4)[0] * 640
        x = struct.unpack_from('>f',pool,active+4)[0] * 640
        # 0x40 = centered active text; layout still sees the Japanese count.
        centered = bool(pool[active+23] & 0x40)
        if centered:
            x -= len(jp) * 25 / 2
        # The original centered No asset has a half-pixel rounding offset;
        # the left-aligned variants must match exactly.
        assert abs(x - base - col * 25) < (.501 if centered else .0001), (hex(row), x, base)
    # Spirit prompt constructor at 0xabc48 copies fixed UTF-8 byte counts.
    # Keep those source literals and their pointers pristine; translate only
    # after conversion to cp932, so neither line is truncated mid-character.
    for jp in ['マークは全てクリアされてしまいます。','よろしいですか？']:
        key = jp.encode('utf-8') + b'\0'
        start, count = 0, 0
        while True:
            start = pristine.find(key,start)
            if start < 0: break
            assert b[start:start+len(key)] == key
            start += len(key); count += 1
        assert count >= 1
        assert jp.encode('cp932') in entries
    assert b[0x7c6a60:0x7c6a68] == pristine[0x7c6a60:0x7c6a68]
    print('PASS: four Yes/No layer alignments; invisible fixed-column pads; Spirit prompt source copies intact.')
    for jp in ['ＳＲポイントを獲得しました。ＳＲポイント',
               'ボーナス資金１００００を入手しました。１００００', 'ユニット']:
        key = jp.encode('cp932')
        assert key in pool.replace(b'\0', b''), jp
        assert entries[key][0] & 0x40000000
    import narration_layout
    narration = narration_layout.rows()
    k = CPK('work/stage_dec/STG0001B.cpk')
    source = k.read(k.files[7])
    for row in narration:
        assert row['jp'].encode('cp932') in source
    import narration_layout
    narration_width_offset = eboot._off(segs, eboot.TABLE_VA)
    narration_widths = dict(enumerate(b[narration_width_offset:narration_width_offset+eboot.ATLAS_CELLS]))
    from intermission_layout import ink
    for number in range(4):
        jp_prefix = ('', '１．', '２．', '３．')[number]
        en = (str(number) + '. ' if number else '') + 'Hibiki is shot down.'
        for name in ('ヒビキ', 'ヒビキＡ'):
            jp = jp_prefix + name + 'の撃墜。'
            assert hooks[jp] == en
            assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping))
        assert ink(en, mapping, narration_widths, 28) < 850
    print('PASS: Hibiki defeat conditions, unnumbered and 1/2/3; legacy name variants preserved.')
    narration_layout.check(hooks, mapping, narration_widths)
    import chapter_narration
    chapter_narration.check_source()
    chapter_narration.check_hooks(entries,mapping,narration_widths)
    import backlog_layout
    backlog_layout.check(hooks, mapping, narration_widths)
    import terrain_labels
    terrain_labels.check(hooks, mapping, narration_widths)
    import terrain_catalog
    terrain_catalog.check_maps(out)
    import weapon_effect_labels
    weapon_effect_labels.check(b, hooks, mapping, narration_widths)
    import battle_reports
    battle_reports.check_elf(b,mapping,narration_widths)
    import unlock_reports
    unlock_reports.check(b,hooks,mapping,narration_widths)
    import trader_upgrade_text
    trader_upgrade_text.check(b,mapping,narration_widths)
    import audit_message_classes, message_class_formats
    coverage = audit_message_classes.check(hooks, mapping, narration_widths,
                                           allow_untranslated_missions=args.partial_translation)
    (out / 'message_coverage.json').write_text(json.dumps(coverage, ensure_ascii=False, indent=2), encoding='utf-8')
    message_class_formats.check(b, mapping)
    # All source data outside the ELF's declared patch areas are checked by
    # eboot.verify during rebuilding. Here check the exact emitted stub too.
    off = eboot._off(segs, eboot.NAME_STUB)
    assert b[off:off+len(eboot.name_stub())] == eboot.name_stub()
    # Both Spirit bands have multiple copies in UI data; ensure none revert.
    built_ui = CPK(str(out / 'AIDDATAPACK.CPK'))
    import battle_screen_labels
    battle_screen_labels.check_ui(member(built_ui,0),mapping,cv_widths)
    battle_screen_labels.check_elf(b,mapping)
    import battle_speaker_names
    battle_speaker_names.check(b)
    import battle_name_transport
    battle_name_transport.check(b)
    import name_entry_labels
    name_entry_labels.check(member(built_ui,0),mapping,cv_widths)
    name_entry_labels.check_hooks(entries,mapping)
    import team_order_labels
    original_ui = CPK('work/orig/AIDDATAPACK.CPK')
    team_order_labels.check(member(built_ui,0),mapping,cv_widths,member(original_ui,0))
    team_order_labels.check_hooks(entries,mapping)
    import bonus_descriptions
    bonus_descriptions.check_hooks(entries,mapping)
    import destroy_quotes
    destroy_quotes.check_hooks(entries,mapping)
    import required_skill_levels
    required_skill_levels.check(entries,mapping)
    import operation_indent
    operation_indent.check(b)
    import battle_name_rendering
    battle_name_rendering.check_elf(b,mapping)
    battle_name_rendering.check_rpw(member(CPK('work/lib/RPW_DATA.CPK'),0),
                                    member(CPK(str(out / 'RPW_DATA.CPK')),0))
    import rpw
    rpw.check_compound_names(member(CPK('work/lib/RPW_DATA.CPK'),0),
                            member(CPK(str(out / 'RPW_DATA.CPK')),0),
                            trdata._load('analysis/glossary.json')['terms'], mapping)
    print('PASS: Fourth Angel/Neo Zeon/Space Demon King Soldier use short native keys and full exact draw-time names.')
    import support_popup_layout
    support_popup_layout.verify(member(CPK('work/orig/AIDDATAPACK.CPK'),0),member(built_ui,0))
    import attack_heading
    import trader_art
    original_art = member(CPK('work/orig/AIDDATAPACK.CPK'), 1)
    attack_art = attack_heading.apply(original_art, dg.LETTER_FACE.path)
    attack_heading.verify(original_art, attack_art, dg.LETTER_FACE.path)
    trader_base = trader_art.apply(attack_art, dg.LETTER_FACE.path)
    trader_art.verify(attack_art, trader_base, dg.LETTER_FACE.path)
    import startup_menu_layout
    assert member(built_ui, 1) == startup_menu_layout.apply_art(trader_base)
    startup_menu_layout.validate_quads(member(built_ui, 0))
    print('PASS: ALL/Center/Wide/Support Attack, Intermission and startup sprites; all other atlas pixels preserved.')
    import location_caption
    location_caption.verify(member(CPK(str(location_caption.SOURCE)), 96),
                            member(CPK(str(out / 'EFFPS3.CPK')), 96), dg.LETTER_FACE.path)
    print('PASS: Jindai school caption; animation, frame and photo unchanged.')
    import maximum_break_art
    import demo_series_titles
    demo_series_titles.verify_archive(CPK(str(demo_series_titles.SOURCE)),
                                     CPK(str(out/'OP.CPK')))
    print('PASS: All 24 demo series titles; non-texture bytes unchanged.')
    maximum_break_art.verify(member(CPK(str(maximum_break_art.SOURCE)),0),
                             member(CPK(str(out/'CMN.CPK')),0),dg.LETTER_FACE.path)
    import scenario_title
    for ident in scenario_title.TITLES:
        scenario_title.verify_title(member(original_tpack,ident),member(built_tpack,ident),dg.LETTER_FACE.path,ident)
    source_effects=CPK(str(location_caption.SOURCE))
    built_effects=CPK(str(out / 'EFFPS3.CPK'))
    import map_locations
    import title_footer
    import berserk_banner
    map_locations.verify_archive(source_effects,built_effects,dg.LETTER_FACE.path,
                                 tuple(scenario_title.EFFECTS)+(title_footer.MEMBER,berserk_banner.MEMBER))
    berserk_banner.verify(member(source_effects,berserk_banner.MEMBER),
                         member(built_effects,berserk_banner.MEMBER),dg.LETTER_FACE.path)
    for ident in scenario_title.EFFECTS:
        scenario_title.verify_effect(member(source_effects,ident),member(built_effects,ident),dg.LETTER_FACE.path,ident)
    title_version = args.version
    if (out/'build_manifest.json').exists():
        manifest = json.loads((out/'build_manifest.json').read_text(encoding='utf-8'))
        if manifest.get('title_footer_version') is not None:
            assert manifest['title_footer_version'] == manifest['version'], 'title/build version mismatch'
            assert title_version is None or title_version == manifest['version']
            title_version = manifest['version']
    import title_logo
    title_logo.verify_complete(member(source_effects,title_footer.MEMBER),
                        member(built_effects,title_footer.MEMBER),dg.LETTER_FACE.path,title_version)
    del source_effects,built_effects
    print('PASS: all 124 title cards and five effect variants; digit/background artwork preserved.')
    ui_data = built_ui.read(built_ui.files[0])
    import pilot_swap_alignment
    pilot_swap_alignment.check(ui_data)
    import record_screen_labels
    record_screen_labels.check(ui_data,mapping,dict(enumerate(widths)),
                               member(CPK('work/orig/AIDDATAPACK.CPK'),0))
    import trade_list_flavor
    trade_list_flavor.check(mapping,dict(enumerate(widths)))
    import trader_ui
    trader_ui.check_categories(ui_data,mapping,dict(enumerate(widths)))
    import ui_followup_layout
    for r,(_jp,en) in trader_ui.ROWS.items():
        if r in ui_followup_layout.ROWS:
            en=ui_followup_layout.ROWS[r][0]
        p = struct.unpack_from('>I',ui_data,r)[0]+aiddata.STR_BASE
        expected = dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        assert ui_data[p:p+len(expected)] == expected, (hex(r),en)
    print('PASS: D-Trader stats/prices/Buy/Sell, reward headings and AT selector widget.')
    import battle_preview_layout
    width_offset = eboot._off(segs, eboot.TABLE_VA)
    preview_widths = dict(enumerate(b[width_offset:width_offset+eboot.ATLAS_CELLS]))
    import menu_followup
    menu_followup.check(ui_data,mapping,preview_widths)
    import training_help_layout
    training_help_layout.check(ui_data,mapping,preview_widths)
    import link_background_layout
    link_background_layout.check(b)
    import parts_menu_followup
    parts_menu_followup.check(ui_data,mapping,preview_widths)
    battle_preview_layout.check(ui_data, mapping, preview_widths)
    import roster_settings_layout, settings_descriptions
    roster_settings_layout.check(ui_data, mapping, preview_widths)
    import intermission_layout
    intermission_layout.check(ui_data, mapping, preview_widths)
    intermission_layout.check_descriptions(b)
    import naming_search_layout
    naming_search_layout.check(ui_data, mapping, preview_widths)
    naming_search_layout.check_reports(hooks, mapping, preview_widths)
    import team_roster_layout
    team_roster_layout.check(ui_data, mapping, preview_widths)
    import map_popup_layout
    map_popup_layout.check(ui_data, mapping, preview_widths)
    import tag_reward_layout
    tag_reward_layout.check(ui_data, mapping, preview_widths)
    import search_list_headers
    search_list_headers.check(ui_data,mapping,preview_widths)
    import weapon_info_layout
    weapon_info_layout.check(ui_data,mapping,preview_widths)
    import map_weapon_info
    map_weapon_info.check_ui(ui_data,mapping,preview_widths)
    map_weapon_info.check_hooks(entries,mapping)
    import weapon_requirements
    weapon_requirements.check(ui_data,mapping,preview_widths)
    import mech_info_layout
    mech_info_layout.check(ui_data,mapping,preview_widths)
    import unit_info_currency
    unit_info_currency.check(ui_data,mapping,preview_widths)
    import upgrade_list_labels
    upgrade_list_labels.check(ui_data,mapping,preview_widths)
    import combat_record_links
    combat_record_links.check(ui_data,mapping,preview_widths)
    import deployment_layout
    deployment_layout.check(ui_data, mapping, preview_widths)
    import deployment_menu_text
    deployment_menu_text.check(ui_data,mapping,preview_widths)
    import song_deployment_labels
    song_deployment_labels.check_ui(ui_data,mapping,preview_widths)
    song_deployment_labels.check_hooks(entries,mapping)
    import command_swap_labels
    command_swap_labels.check_ui(ui_data,mapping,preview_widths)
    command_swap_labels.check_hooks(entries,mapping,preview_widths)
    command_swap_labels.check_elf(b,mapping,preview_widths)
    import trader_spirit_prompts
    trader_spirit_prompts.check_ui(ui_data,mapping,preview_widths)
    trader_spirit_prompts.check_elf(b,mapping)
    import pilot_spirit_layout
    pilot_spirit_layout.check(ui_data,mapping,preview_widths,
                              member(CPK('work/orig/AIDDATAPACK.CPK'),0))
    song_deployment_labels.check_source(Path('work/EBOOT_dec.elf').read_bytes(),
                                        member(CPK('work/orig/AIDDATAPACK.CPK'),0))
    import aboard_order_labels
    aboard_order_labels.check(ui_data,mapping,preview_widths)
    import library_list_labels
    library_list_labels.check(ui_data,mapping,preview_widths)
    import save_prompt_layout
    save_prompt_layout.check(ui_data,mapping)
    import ui_followup_layout
    ui_followup_layout.check(ui_data, mapping, preview_widths)
    battle_reports.check_ui(ui_data,mapping,preview_widths)
    for text in settings_descriptions.LABELS:
        assert sum(preview_widths[dg.cell_index(mapping[c])] for c in text)*31/32 < 950, text
    import check_search_layout
    check_search_layout.check(b, mapping, ui_data)
    import check_command_layout
    import activation_prompts
    activation_prompts.check(b, mapping, preview_widths)
    check_command_layout.check(b, mapping, ui_data)
    check_command_layout.check_blank_cells(built_tpack)
    spirit_rows = json.loads(Path('translation/ui_aiddata.json').read_text(encoding='utf-8'))['lines'][-2:]
    for row in spirit_rows:
        expected = dg.encode_mixed(row['en'], mapping)
        assert row['jp'].encode('cp932') not in ui_data, 'Japanese Spirit band restored'
        assert ui_data.count(expected) == row['places'], ('Spirit band copies', row['jp'])
    assert not (set(mapping.values()) & {code for _,code in dg.TINY_CELLS.values()}), 'Tiny glyph collision'
    # A newer SRVC uses expanded blocks; do not restore an older EBOOT table.
    import srvc_blocks as voice_blocks
    voice_blocks.parse((out / 'SRVC.BIN').read_bytes(), voice_blocks.read_table(b))
    print('PASS: all five Spirit-band copies translated; tiny cells reserved.')
    print(f'PASS: {len(batch_hooks)} batch hooks verified in {len(entries)} binary entries; all registered UI translations encode;')
    print('count boundaries, joined reward layers, mixed VWF item name and 18 narration lines checked.')
    print('Runtime placement, custom player names and texture-only labels still need in-game checks.')


if __name__ == '__main__':
    main()
