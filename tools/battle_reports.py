"""Battle/help/repair report strings. Never modify amounts or game logic."""
import localization as _l10n
import struct
import hashlib
import aiddata,digraph as dg
from intermission_layout import text,ink

HOOKS={'特殊スキル「社長」の効果で':_l10n.literal('battle_reports.HOOKS/0'),
       '出撃したパイロットに':_l10n.literal('battle_reports.HOOKS/1')}
HELP={
 '次の行動で敵チームを壊滅させた場合、行動回数が１回プラスされる':_l10n.literal('battle_reports.HELP/2'),
 '次の敵撃墜時に獲得ＰＰが２倍になる':_l10n.literal('battle_reports.HELP/3'),
 '次の敵撃墜時に獲得Ｚチップが２倍になる':_l10n.literal('battle_reports.HELP/4'),
 'チーム内のメインパイロットのＳＰ２５回復':_l10n.literal('battle_reports.HELP/5'),
}
FORMAT_JP='ＰＰが%sずつ加算されました。'
FORMAT_OFF=0x6e4f68
GOLD_JP='金塊　'
GOLD_ID='ui.battle_reports:gold_reward'

def gold_hook():
    return {GOLD_JP:_l10n.message(GOLD_ID)}

def check_gold_source(blob):
    # Result reward constructor copies exactly seven bytes, then appends
    # fullwidth digits and copies into a64-byte item slot. Never lengthen
    # this source in place or alter the amount conversion/cap.
    assert blob[0x70f988:0x70f98f]==GOLD_JP.encode('cp932')+b'\0'
    assert blob[0x7cbafc:0x7cbb00]==struct.pack('>I',0x71f988)
    assert hashlib.sha256(blob[0x2f019c:0x2f0298]).hexdigest()=='47b2923672ada609656ccd75f0a798325a62ec7016144376bae50659bef42d9c'

def check_gold_elf(blob,mapping):
    import eboot
    check_gold_source(blob)
    segs=eboot._segments(blob)
    pos=eboot._off(segs,eboot.NAME_TBL)
    while True:
        jp,en=struct.unpack_from('>II',blob,pos)
        assert jp,'Gold reward hook missing'
        key=eboot._cstr(blob,eboot._off(segs,jp))
        if key==GOLD_JP.encode('cp932'):
            assert en>>30==2,'Gold reward must retain the dynamic amount'
            assert eboot._cstr(blob,eboot._off(segs,en&0x3fffffff))==dg.encode_mixed(_l10n.message(GOLD_ID),mapping)
            break
        pos+=8
        assert pos<eboot._off(segs,eboot.NAME_STR)
ROWS={0xaa0b4:('：機体修理費用・精算',_l10n.literal('battle_reports.ROWS/6')),
      0xaaf54:('：機体修理費用・清算',_l10n.literal('battle_reports.ROWS/7')),
      0xab334:('：機体修理費用・精算',_l10n.literal('battle_reports.ROWS/8')),
      0xaa614:('修理費',_l10n.literal('battle_reports.ROWS/9')),0xaa634:('資金',_l10n.literal('battle_reports.ROWS/10')),
      0xac914:('タッグコマンド',_l10n.literal('battle_reports.ROWS/11'))}

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        raw=dg.encode_mixed(en,mapping)+b'\0'
        if r==0xac914:
            import command_layout as layout
            raw=struct.pack('>H',layout.CODES[layout.LABELS.index(en)])+raw
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check_ui(out,mapping,widths)
    return bytes(out)

def format_bytes(mapping):
    # printf must receive its original ASCII %s placeholder. The incoming
    # amount remains untouched, including multi-digit bonuses.
    raw=dg.encode_mixed('+',mapping)+b'%s'+dg.encode_mixed(' PP.',mapping)+b'\0'
    return raw+bytes(len(FORMAT_JP.encode('cp932'))+1-len(raw))

def patch_format(elf,mapping):
    check_gold_source(elf)
    out=bytearray(elf);old=FORMAT_JP.encode('cp932')+b'\0';new=format_bytes(mapping)
    assert out[FORMAT_OFF:FORMAT_OFF+len(old)]==old
    out[FORMAT_OFF:FORMAT_OFF+len(old)]=new
    return bytes(out)

def check_ui(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        raw=dg.encode_mixed(en,mapping)
        if r==0xac914:
            import command_layout as layout
            raw=struct.pack('>H',layout.CODES[layout.LABELS.index(en)])+raw
        assert text(blob,r)==raw
        assert ink(en,mapping,widths,31)<220
    print('PASS: repair titles/Cost/Funds and Tag Command help heading; amounts and row layout untouched.')

def check_elf(elf,mapping,widths):
    check_gold_elf(elf,mapping)
    import eboot
    import president_report_layout
    president_report_layout.check(elf,mapping)
    assert elf[FORMAT_OFF:FORMAT_OFF+len(format_bytes(mapping))]==format_bytes(mapping)
    assert format_bytes(mapping).count(b'%s')==1
    for amount in ('５','１０','５０','１００'):
        rendered=format_bytes(mapping).split(b'\0')[0].replace(b'%s',amount.encode('cp932'))
        assert amount.encode('cp932') in rendered
    for en in HOOKS.values(): assert ink(en,mapping,widths,28)<450
    for en in HELP.values():
        raw=''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in en).encode('utf8')+b'\0'
        assert elf.count(raw)==1,en
        assert ink(en,mapping,widths,25)<880,(en,ink(en,mapping,widths,25))
    print('PASS: all four Tag Command help descriptions, President report and variable PP placeholder.')
