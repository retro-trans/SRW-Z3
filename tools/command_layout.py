"""Scoped live-pitch centering for COMMAND labels and centered dialog hooks."""
import localization as _l10n
import struct

CAVE = 0x78E400
DATA = 0x78E600
CP_BASE = 0x1F0
CODES = tuple(range(0x8890, 0x8897)) + tuple(range(0x8880, 0x888A))
CODEPOINTS = tuple(range(0x1F0, 0x1F7)) + tuple(range(0x1D0, 0x1DA))
LABELS = (_l10n.literal('command_layout.LABELS/0'), _l10n.literal('command_layout.LABELS/1'), _l10n.literal('command_layout.LABELS/2'), _l10n.literal('command_layout.LABELS/3'),
          _l10n.literal('command_layout.LABELS/4'), _l10n.literal('command_layout.LABELS/5'), _l10n.literal('command_layout.LABELS/6'),
          _l10n.literal('command_layout.LABELS/7'), _l10n.literal('command_layout.LABELS/8'), _l10n.literal('command_layout.LABELS/9'), _l10n.literal('command_layout.LABELS/10'), _l10n.literal('command_layout.LABELS/11'), _l10n.literal('command_layout.LABELS/12'),
          _l10n.literal('command_layout.LABELS/13'), _l10n.literal('command_layout.LABELS/14'), _l10n.literal('command_layout.LABELS/15'), _l10n.literal('command_layout.LABELS/16'))
UTF8_LABELS = LABELS[:13]
SPLIT_RECORDS = (0xA8DF4, 0xA8E14, 0xA8E34, 0xA8E54)

# Retain the first 17 slots so earlier working rows stay byte-compatible.
MORE_COMMANDS = (_l10n.literal('command_layout.MORE_COMMANDS/17'), _l10n.literal('command_layout.MORE_COMMANDS/18'), _l10n.literal('command_layout.MORE_COMMANDS/19'), _l10n.literal('command_layout.MORE_COMMANDS/20'), _l10n.literal('command_layout.MORE_COMMANDS/21'), _l10n.literal('command_layout.MORE_COMMANDS/22'),
                 _l10n.literal('command_layout.MORE_COMMANDS/23'), _l10n.literal('command_layout.MORE_COMMANDS/24'), _l10n.literal('command_layout.MORE_COMMANDS/25'), _l10n.literal('command_layout.MORE_COMMANDS/26'), _l10n.literal('command_layout.MORE_COMMANDS/27'),
                 _l10n.literal('command_layout.MORE_COMMANDS/28'), _l10n.literal('command_layout.MORE_COMMANDS/29'), _l10n.literal('command_layout.MORE_COMMANDS/30'), _l10n.literal('command_layout.MORE_COMMANDS/31'), _l10n.literal('command_layout.MORE_COMMANDS/32'),
                 _l10n.literal('command_layout.MORE_COMMANDS/33'), _l10n.literal('command_layout.MORE_COMMANDS/34'), _l10n.literal('command_layout.MORE_COMMANDS/35'), _l10n.literal('command_layout.MORE_COMMANDS/36'), _l10n.literal('command_layout.MORE_COMMANDS/37'),
                 _l10n.literal('command_layout.MORE_COMMANDS/38'), _l10n.literal('command_layout.MORE_COMMANDS/39'), _l10n.literal('command_layout.MORE_COMMANDS/40'), _l10n.literal('command_layout.MORE_COMMANDS/41'))
DIALOGS = {
    '本体ハードディスクにセーブ': _l10n.literal('command_layout.DIALOGS/42'),
    'ネットワークにアップロード': _l10n.literal('command_layout.DIALOGS/43'),
    'セーブしない': _l10n.literal('command_layout.DIALOGS/44'),
    'ここまでのマップ上の進行状況をセーブします。': _l10n.literal('command_layout.DIALOGS/45'),
    '保存先を選択してください。': _l10n.literal('command_layout.DIALOGS/46'),
    'フェイズを終了しますか？': _l10n.literal('command_layout.DIALOGS/47'),
}
DIALOG_START = len(LABELS)+len(MORE_COMMANDS)
LABELS += MORE_COMMANDS + tuple(DIALOGS.values()) + (_l10n.literal('command_layout.LABELS/48'), _l10n.literal('command_layout.LABELS/49'))
COUNT_START = DIALOG_START+len(DIALOGS)
EXTRA_START = len(LABELS)
EXTRA_DIALOGS = {
    '　ＡＧからのボーナス': _l10n.literal('command_layout.EXTRA_DIALOGS/50'),
    'ＡＧからのボーナス': _l10n.literal('command_layout.EXTRA_DIALOGS/51'),
    '「Ｚチップ　１０００Ｚ」を入手しました': _l10n.literal('command_layout.EXTRA_DIALOGS/52'),
    '「Ｚチップ　１００Ｚ」を入手しました': _l10n.literal('command_layout.EXTRA_DIALOGS/53'),
    '「Ｚチップ　２００Ｚ」を入手しました': _l10n.literal('command_layout.EXTRA_DIALOGS/54'),
}
LABELS += tuple(EXTRA_DIALOGS.values())
WIDGET_START = len(LABELS)
LABELS += (_l10n.literal('command_layout.LABELS/55'), _l10n.literal('command_layout.LABELS/56'), _l10n.literal('command_layout.LABELS/57'))
UTF8_LABELS += MORE_COMMANDS + (_l10n.literal('command_layout.UTF8_LABELS/58'), _l10n.literal('command_layout.UTF8_LABELS/59'))
CODES += tuple(range(0x8850, 0x8850+len(LABELS)-17))
CODEPOINTS += tuple(range(0x1A0, 0x1A0+len(LABELS)-17))
assert CODES[-1] < 0x887F
SETTINGS_START = len(LABELS)
import settings_descriptions
LABELS += settings_descriptions.LABELS
UTF8_LABELS += settings_descriptions.LABELS
CODES += tuple(range(0x87C0, 0x87C0+len(settings_descriptions.LABELS)))
CODEPOINTS += tuple(range(0x240, 0x240+len(settings_descriptions.LABELS)))
TERRAIN_START = len(LABELS)
TERRAIN = {'舗装道路':_l10n.literal('command_layout.TERRAIN/60'), '平地':_l10n.literal('command_layout.TERRAIN/61'),
           'ビル':_l10n.literal('command_layout.TERRAIN/62'), '工事区画':_l10n.literal('command_layout.TERRAIN/63')}
LABELS += tuple(TERRAIN.values())
CODES += tuple(range(0x87DC,0x87E0))
CODEPOINTS += tuple(range(0x25C,0x260))
LIBRARY_START = len(LABELS)
import intermission_layout
LABELS += tuple(intermission_layout.DESCRIPTIONS.values())
UTF8_LABELS += tuple(intermission_layout.DESCRIPTIONS.values())
CODES += tuple(range(0x87E0,0x87E5))
CODEPOINTS += tuple(range(0x260,0x265))
EMPTY_FILTER_INDEX = len(LABELS)
LABELS += (_l10n.literal('command_layout.LABELS/64'),)
CODES += (0x87E5,)
CODEPOINTS += (0x265,)
NAMING_REPORT_START = len(LABELS)
import naming_search_layout
LABELS += tuple(naming_search_layout.REPORTS.values())
CODES += tuple(range(0x87E6,0x87E9))
CODEPOINTS += tuple(range(0x266,0x269))
FOLLOWUP_START = len(LABELS)
# Append only: existing builds depend on every earlier pad index.
FOLLOWUP_TERRAIN = {'崖': _l10n.literal('command_layout.FOLLOWUP_TERRAIN/65')}
FOLLOWUP_LABELS = (_l10n.literal('command_layout.FOLLOWUP_LABELS/66'), _l10n.literal('command_layout.FOLLOWUP_LABELS/67'), _l10n.literal('command_layout.FOLLOWUP_LABELS/68'),
                   _l10n.literal('command_layout.FOLLOWUP_LABELS/69'), _l10n.literal('command_layout.FOLLOWUP_LABELS/70'), _l10n.literal('command_layout.FOLLOWUP_LABELS/71'))
LABELS += tuple(FOLLOWUP_TERRAIN.values()) + FOLLOWUP_LABELS
CODES += tuple(range(0x87E9,0x87E9+7))
CODEPOINTS += tuple(range(0x269,0x269+7))

ALL_TERRAIN_START = len(LABELS)
import terrain_catalog
ALL_TERRAIN = {terrain_catalog.key(jp): en for jp,en in terrain_catalog.EXTRA.items()}
LABELS += tuple(ALL_TERRAIN.values())
# Extend the existing contiguous bank by 11; use 62 verified blank cells
# for the rest. Existing indices/codes are never renumbered.
CODES += tuple(range(0x87F0,0x87FB)) + tuple(range(0x84BF,0x84FD))
CODEPOINTS += tuple(range(0x270,0x2B9))
TERRAIN_BANK_START = ALL_TERRAIN_START+11
assert len(ALL_TERRAIN) == 73 and len(CODES) == len(LABELS) == len(CODEPOINTS)

DEPLOYMENT_START = len(LABELS)
import deployment_layout
LABELS += tuple(deployment_layout.CONFIRMATIONS.values())
CODES += tuple(range(0x8461, 0x8468))
CODEPOINTS += tuple(range(0x2B9, 0x2C0))
assert len(CODES) == len(LABELS) == len(CODEPOINTS)

SAVE_START = len(LABELS)
# These boxes split multiline prompts before drawing. Each source line needs
# its own Japanese-count pad; centering the combined string cannot fix them.
SAVE_DIALOGS = {
    'セーブが終了しました。': _l10n.literal('command_layout.SAVE_DIALOGS/72'),
    'このままゲームを続けますか？': _l10n.literal('command_layout.SAVE_DIALOGS/73'),
    '上書きしてよろしいですか？': _l10n.literal('command_layout.SAVE_DIALOGS/74'),
    '新規作成してよろしいですか？': _l10n.literal('command_layout.SAVE_DIALOGS/75'),
    'このデータを上書きしますか？': _l10n.literal('command_layout.SAVE_DIALOGS/76'),
    'タイトルに戻りますか？': _l10n.literal('command_layout.SAVE_DIALOGS/77'),
}
LABELS += tuple(SAVE_DIALOGS.values())
CODES += tuple(range(0x8468,0x8468+len(SAVE_DIALOGS)))
CODEPOINTS += tuple(range(0x2C0,0x2C0+len(SAVE_DIALOGS)))
assert len(CODES) == len(LABELS) == len(CODEPOINTS)

PREP_START = len(LABELS)
# Separate executable popup table: do not pad other occurrences of these
# shared captions (training headers, help text, team editor, etc.).
PREP_ROWS = {
    0x6d5430: ('チーム編成', _l10n.literal('command_layout.PREP_ROWS/78')),
    0x6d5440: ('パイロット養成', _l10n.literal('command_layout.PREP_ROWS/79')),
    0x6d5458: ('のせかえ', _l10n.literal('command_layout.PREP_ROWS/80')),
    0x6d5468: ('機体・武器改造', _l10n.literal('command_layout.PREP_ROWS/81')),
    0x6d5480: ('強化パーツ', _l10n.literal('command_layout.PREP_ROWS/82')),
    0x6d5490: ('換装パーツ', _l10n.literal('command_layout.PREP_ROWS/83')),
    0x6d54a0: ('母艦の改造', _l10n.literal('command_layout.PREP_ROWS/84')),
}
LABELS += tuple(en for jp,en in PREP_ROWS.values())
# Extend the original upper bank: keep the space-limited VWF dispatcher
# the same size and leave every pre-existing pad index/code unchanged.
CODES += tuple(range(0x8897,0x889E))
CODEPOINTS += tuple(range(0x2C6,0x2CD))
assert len(CODES) == len(LABELS) == len(CODEPOINTS)


ACTIVATION_START = len(LABELS)
import activation_prompts
ACTIVATION_LABELS = activation_prompts.activation_labels()
LABELS += ACTIVATION_LABELS
# Verified blank cells in both native atlas layers, beyond the tiny UI glyphs.
# Undefined CP932 codes alone are insufficient: row 0x85 holds native icons.
CODES += tuple(range(0x86E0, 0x86E0 + len(ACTIVATION_LABELS)))
CODEPOINTS += tuple(range(0x2CD, 0x2CD + len(ACTIVATION_LABELS)))
assert len(CODES) == len(LABELS) == len(CODEPOINTS)
assert DATA + len(LABELS) * 8 <= 0x78ED00


def dialog_index(jp):
    if jp in SAVE_DIALOGS:
        return SAVE_START+list(SAVE_DIALOGS).index(jp)
    if jp in deployment_layout.CONFIRMATIONS:
        return DEPLOYMENT_START+list(deployment_layout.CONFIRMATIONS).index(jp)
    if jp in ALL_TERRAIN:
        return ALL_TERRAIN_START+list(ALL_TERRAIN).index(jp)
    if jp in FOLLOWUP_TERRAIN:
        return FOLLOWUP_START+list(FOLLOWUP_TERRAIN).index(jp)
    if jp in naming_search_layout.REPORTS:
        return NAMING_REPORT_START+list(naming_search_layout.REPORTS).index(jp)
    if jp in TERRAIN:
        return TERRAIN_START+list(TERRAIN).index(jp)
    if jp in EXTRA_DIALOGS:
        return EXTRA_START+list(EXTRA_DIALOGS).index(jp)
    if jp in DIALOGS:
        return DIALOG_START+list(DIALOGS).index(jp)
    import re
    match = re.fullmatch('行動終了していないチームが([０-９]{1,2})チームあります。', jp)
    if match:
        return COUNT_START+(len(match[1])==2)
    return None


def dialog_prefix(jp):
    index = dialog_index(jp)
    return b'' if index is None else struct.pack('>H',CODES[index])


def count_coefficient(index):
    if index >= PREP_START:
        return (len(LABELS[index])+1)/2.
    if index >= SAVE_START:
        return len(list(SAVE_DIALOGS)[index-SAVE_START])/2.
    if index >= DEPLOYMENT_START:
        return len(list(deployment_layout.CONFIRMATIONS)[index-DEPLOYMENT_START])/2.
    if index >= ALL_TERRAIN_START:
        return len(list(ALL_TERRAIN)[index-ALL_TERRAIN_START])/2.
    if index >= FOLLOWUP_START:
        if index == FOLLOWUP_START: return len(next(iter(FOLLOWUP_TERRAIN)))/2.
        return (len(LABELS[index])+1)/2.
    if index >= NAMING_REPORT_START:
        return len(list(naming_search_layout.REPORTS)[index-NAMING_REPORT_START])/2.
    if index >= LIBRARY_START:
        return (len(LABELS[index])+1)/2.
    if index >= TERRAIN_START:
        return len(list(TERRAIN)[index-TERRAIN_START])/2.
    if index >= WIDGET_START:
        return (len(LABELS[index])+1)/2.
    if index < DIALOG_START:
        return (len(LABELS[index])+1)/2.
    if index >= EXTRA_START:
        return len(list(EXTRA_DIALOGS)[index-EXTRA_START])/2.
    jp = (list(DIALOGS)[index-DIALOG_START] if index<COUNT_START
          else '行動終了していないチームが'+('０' if index==COUNT_START else '１０')+'チームあります。')
    # Dialog substitution happens AFTER the original centered draw computes
    # its origin. The injected blank was not part of the original count.
    return len(jp)/2.


def stub():
    import eboot
    import digraph as dg
    p, a = eboot._ppc(), eboot._Asm()
    def emit(op, *args): a.emit(p[op](*args))
    emit('cmpwi', 0, dg.cell_index(CODES[ACTIVATION_START])); a.br('blt', 'prep_bank')
    emit('cmpwi', 0, dg.cell_index(CODES[-1])); a.br('bgt', 'prep_bank')
    emit('addi', 9, 0, ACTIVATION_START-dg.cell_index(CODES[ACTIVATION_START])); a.br('b', 'index')
    a.label('prep_bank')
    emit('cmpwi', 0, dg.cell_index(CODES[PREP_START])); a.br('blt', 'prompt_bank')
    emit('cmpwi', 0, dg.cell_index(CODES[ACTIVATION_START-1])); a.br('bgt', 'prompt_bank')
    emit('addi', 9, 0, PREP_START-dg.cell_index(CODES[PREP_START])); a.br('b', 'index')
    a.label('prompt_bank')
    # Deployment/save prompt cells, separate from the terrain bank.
    emit('cmpwi', 0, dg.cell_index(CODES[DEPLOYMENT_START])); a.br('blt', 'prior_banks')
    emit('cmpwi', 0, dg.cell_index(CODES[PREP_START-1])); a.br('bgt', 'prior_banks')
    emit('addi', 9, 0, DEPLOYMENT_START-dg.cell_index(CODES[DEPLOYMENT_START])); a.br('b', 'index')
    a.label('prior_banks')
    # Entry r0 is the reserved glyph index. Only existing VWF scratch
    # registers r0/r9/f10/f13 and stack +d0 are touched.
    emit('cmpwi', 0, dg.cell_index(CODES[SETTINGS_START])); a.br('bge', 'old_banks')
    emit('addi', 9, 0, TERRAIN_BANK_START-dg.cell_index(CODES[TERRAIN_BANK_START])); a.br('b', 'index')
    a.label('old_banks')
    emit('cmpwi', 0, dg.cell_index(CODES[17])); a.br('bge', 'existing_banks')
    emit('addi', 9, 0, SETTINGS_START-dg.cell_index(CODES[SETTINGS_START])); a.br('b', 'index')
    a.label('existing_banks')
    emit('cmpwi', 0, dg.cell_index(CODES[7])); a.br('bge', 'upper_banks')
    emit('addi', 9, 0, 17-dg.cell_index(CODES[17])); a.br('b', 'index')
    a.label('upper_banks')
    emit('cmpwi', 0, dg.cell_index(CODES[0])); a.br('bge', 'original_bank')
    emit('addi', 9, 0, 7-dg.cell_index(CODES[7])); a.br('b', 'index')
    a.label('original_bank')
    emit('addi', 9, 0, -dg.cell_index(CODES[0]))
    a.label('index')
    emit('add', 0, 9, 0)
    emit('mulli', 0, 0, 8)
    emit('lis', 9, DATA >> 16); emit('ori', 9, 9, DATA & 65535)
    emit('add', 9, 9, 0)
    emit('lfs', 13, 9, 0); emit('lfs', 10, 1, 0x94)
    emit('fmuls', 13, 13, 10); emit('stfs', 13, 1, 0xd0)
    emit('lfs', 13, 9, 4); emit('lfs', 10, 1, 0x9c)
    emit('fmuls', 13, 13, 10); emit('lfs', 10, 1, 0xd0)
    emit('fsubs', 13, 10, 13)
    emit('lis', 9, eboot.PEN_ACC >> 16)
    emit('ori', 9, 9, eboot.PEN_ACC & 65535)
    emit('lfs', 10, 9, 0); emit('fadds', 10, 10, 13)
    emit('stfs', 10, 9, 0); a.emit(0x4e800020)
    assert CAVE + len(a.code()) <= DATA
    return a.code()


def install(b, segs, mapping, widths):
    import eboot
    import digraph as dg
    assert not set(CODES) & set(mapping.values())
    table = eboot.unicode_table(b, segs)
    data = bytearray()
    for i, label in enumerate(LABELS):
        # Centered drawer starts at center - count*pitch/2. The leading
        # blank counts as one character, then advances to center-ink/2.
        ink = sum(widths[dg.cell_index(mapping[c])] for c in label)
        data += struct.pack('>ff', count_coefficient(i), ink/64.)
        pos = table + 2*CODEPOINTS[i]
        assert struct.unpack_from('>H', b, pos)[0] in (0x81a1, CODES[i])
        struct.pack_into('>H', b, pos, CODES[i])
    for va, raw in ((CAVE, stub()), (DATA, data)):
        pos = eboot._off(segs, va)
        if va == DATA:
            # Extending an already validated label table is safe only
            # when the original prefix matches and the remaining space is empty.
            for offset in range(0,len(raw),8):
                assert b[pos+offset:pos+offset+8] in (bytes(8),raw[offset:offset+8])
        else:
            assert not any(b[pos:pos+len(raw)]) or b[pos:pos+len(raw)] == raw
        b[pos:pos+len(raw)] = raw


def prefix(label):
    return chr(CODEPOINTS[LABELS.index(label)])


def split_labels(blob, mapping, widths):
    """Two selected states, each composed from two separately colored records.

    Repoint only these four labels, retaining colors/selection flags. Both
    pieces use the same 28px font and baseline, centered as a complete row.
    The slash stays on the selected piece, as in the original UI.
    """
    import digraph as dg
    result = bytearray(blob)
    for index, record in enumerate(SPLIT_RECORDS):
        label = LABELS[13+index]
        original = ('味方部隊／', '敵', '味方', '／敵部隊')[index].encode('cp932')
        ref = struct.unpack_from('>I',blob,record)[0]+0x59478
        assert blob[ref:ref+len(original)+1] == original+b'\0'
        raw = struct.pack('>H', CODES[13+index])+dg.encode_mixed(label,mapping)+b'\0'
        pos = (len(result)+3)&~3
        result += bytes(pos-len(result))+raw
        struct.pack_into('>I',result,record,pos-0x59478)
        pair = LABELS[13:15] if index<2 else LABELS[15:17]
        wleft,wright = [sum(widths[dg.cell_index(mapping[c])] for c in text)*28/32. for text in pair]
        gap = 10.0
        offset = -(wright+gap)/2 if index%2==0 else (wleft+gap)/2
        struct.pack_into('>ff',result,record+4,-1/1280.+offset/640.,.0055555556900799274)
        result[record+16:record+22] = bytes.fromhex('1c1c1a1c1c1c')
        assert result[record+22:record+32] == blob[record+22:record+32]
    return bytes(result)


def funds_colon(blob):
    """Align the map panel's Funds colon with its Z Chips colon."""
    result = bytearray(blob)
    source, target = 0xABA54, 0xABA74
    assert blob[source:source+4] == struct.pack('>I', 0xBA2C)
    assert blob[target:target+4] == struct.pack('>I', 0xBA30)
    assert blob[target+4:target+8] in (struct.pack('>f', .7007812261581421), blob[source+4:source+8])
    result[target+4:target+8] = blob[source+4:source+8]
    return bytes(result)
