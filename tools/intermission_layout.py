"""Scoped translations for the screenshot-reported intermission menus.

Never replace short fragments globally: Team Setup is stored as three
separate pieces, and the PS Store caption has three independent widgets.
"""
import localization as _l10n
import struct
import aiddata
import digraph as dg

DESCRIPTIONS = {
    'ロボット大図鑑を閲覧します。': _l10n.literal('intermission_layout.DESCRIPTIONS/0'),
    'キャラクター事典を閲覧します。': _l10n.literal('intermission_layout.DESCRIPTIONS/1'),
    '用語事典です。': _l10n.literal('intermission_layout.DESCRIPTIONS/2'),
    'サウンドを鑑賞します。': _l10n.literal('intermission_layout.DESCRIPTIONS/3'),
    'シナリオチャートを閲覧します。': _l10n.literal('intermission_layout.DESCRIPTIONS/4'),
}
ROWS = {
    0xaebd4: ('【パイロット一覧】', _l10n.literal('intermission_layout.ROWS/5')),
    0xb2e54: ('【パイロット一覧】', _l10n.literal('intermission_layout.ROWS/6')),
    0xaeb94: ('【強化パーツ】', _l10n.literal('intermission_layout.ROWS/7')),
    0xb2b54: ('【強化パーツ】', _l10n.literal('intermission_layout.ROWS/8')),
    0xa8fb4: ('システム', _l10n.literal('intermission_layout.ROWS/9')),
    0xa8fd4: ('ライブラリー', _l10n.literal('intermission_layout.ROWS/10')),
    0xa9034: ('「ストア」へ', _l10n.literal('intermission_layout.ROWS/11')),
    0xa9054: ('ボーナスシナリオ', _l10n.literal('intermission_layout.ROWS/12')),
    0xa9074: ('ＰＳ', _l10n.literal('intermission_layout.ROWS/13')),
    0xa9094: ('Ｓｔｏｒｅ', ''),
    0xa90b4: ('へ', ''),
    0xa90d4: ('アップロード', _l10n.literal('intermission_layout.ROWS/14')),
    0xa90f4: ('ダウンロード', _l10n.literal('intermission_layout.ROWS/15')),
    0xb2374: ('自動編成', _l10n.literal('intermission_layout.ROWS/16')),
    0xb2394: ('自動名称', _l10n.literal('intermission_layout.ROWS/17')),
    0xb23b4: ('名称：自動更新', _l10n.literal('intermission_layout.ROWS/18')),
    0xb23d4: ('チームソート', _l10n.literal('intermission_layout.ROWS/19')),
    0xb23f4: ('検索設定', _l10n.literal('intermission_layout.ROWS/20')),
    0xb2414: ('全やり直し', _l10n.literal('intermission_layout.ROWS/21')),
    0xa6254: ('・部隊名変更', '・Rename Squad'),
    0xa62b4: ('『ロボット大図鑑』', _l10n.literal('intermission_layout.ROWS/22')),
    0xa62d4: ('『ロボット大図鑑』', _l10n.literal('intermission_layout.ROWS/23')),
    0xa62f4: ('『キャラクター事典』', _l10n.literal('intermission_layout.ROWS/24')),
    0xa6314: ('『用語事典』', _l10n.literal('intermission_layout.ROWS/25')),
    0xa6334: ('『サウンドセレクト』', _l10n.literal('intermission_layout.ROWS/26')),
    0xa6354: ('『シナリオチャート』', _l10n.literal('intermission_layout.ROWS/27')),
}
LIBRARY = tuple(range(0xa62b4,0xa6374,32))
# Live 2560x1440 capture (2026-09-13), measured colored glyph bounds.
# The special Library renderer adds per-caption offsets after FSSA placement;
# ordinary ink centering alone was insufficient. Corrections are in native
# 1280x720 pixels and preserve its working mode 0x01 and plain glyphs.
LIBRARY_LIVE_X_CORRECTION = {
    0xa62b4:122., 0xa62d4:122., 0xa62f4:128.5,
    0xa6314:87.5, 0xa6334:151.75, 0xa6354:148.75,
}
CENTERED = tuple(r for r in ROWS if 0xa8fb4<=r<=0xa90f4 or 0xb2374<=r<=0xb2414) + LIBRARY
SIZES = {0xa9054:25, 0xb23b4:21, 0xb23f4:25}
# A complete caption replaces only the first piece; suppress the old suffixes.
for first,tail,last in [(0xa0474,0xa0494,0xa04d4),
                        (0xa0774,0xa0794,0xa07d4),
                        (0xa0934,0xa0954,0xa0994)]:
    ROWS[first]=('チー',_l10n.literal('intermission_layout.ROWS/28'));ROWS[tail]=('編成','');ROWS[last]=('ム','')
ROWS[0xa05b4]=('タッグ',_l10n.literal('intermission_layout.ROWS/29'));ROWS[0xa05d4]=('編成','')
for r in (0xa0434,0xa04f4,0xa0534,0xa0574,0xa0734,0xa08f4):
    ROWS[r]=('タッグ編成',_l10n.literal('intermission_layout.ROWS/30'))
TEAM = tuple(r for r in ROWS if 0xa0434<=r<=0xa0994)
for r in TEAM:
    if ROWS[r][1]: ROWS[r]=(ROWS[r][0],_l10n.literal('intermission_layout.ROWS/31'))
# Library buttons use their original special text mode (low byte 0x01),
# not the ordinary centered-text mode. The blank-button report followed
# our leading-pad + mode 0x41 patch; restore the source mode. Keep plain glyphs
# and a measured left edge; do not change the pad IDs used by other menus.
LIVE_CENTERED = (0xa9034,0xa9074)
# Supplied Network crop: PS Store ink centre x=211, button centre x=377.
# 2434 screen pixels per 1280 native pixels. The split-caption renderer
# adds a left offset after the existing centering pad; correct both copies.
STORE_LIVE_X_CORRECTION = (377.-211.)/(2434./1280.)
SETTINGS_ROWS=(0xa65b4,0xa69f4,0xa6a54,0xa6eb4)
PARTS = {'・音声設定（　：　　）':'・Voice    （　：　　）',
         '・ＳＥ設定':'・Sound Effects', '・ＢＧＭ設定':'・Music',
         '・戦闘ＢＧＭ設定':'・Battle Music', '・戦闘ＢＧＭ選曲':'・Battle Theme',
         '・エディットＢＧＭ':'・Custom Music', '・部隊名変更':'・Rename Squad',
         '・ソート・サブ情報の記憶':'・Remember Sort / Info',
         '・ソート／サブ情報の記憶':'・Remember Sort / Info'}

def text(blob,r):
    p=struct.unpack_from('>I',blob,r)[0]+aiddata.STR_BASE
    return blob[p:blob.index(b'\0',p)]

def ink(en,mapping,widths,size):
    return sum(widths[dg.cell_index(mapping[c])] if c in mapping else 32 for c in en)*size/32.

def encoded(r,en,mapping):
    import command_layout
    pad=struct.pack('>H',command_layout.CODES[command_layout.LABELS.index(en)]) if r in LIVE_CENTERED else b''
    return pad+dg.encode_mixed(en,mapping,newline=b'\n')

def apply(blob,mapping,widths):
    out=bytearray(blob);rows=dict(ROWS);allowed=set()
    for r in SETTINGS_ROWS:
        jp=text(blob,r).decode('cp932')
        lines=jp.split('\n');assert len(lines)==8
        assert all(s in PARTS or s in ('','　') for s in lines),jp
        rows[r]=(jp,'\n'.join(PARTS.get(s,s) for s in lines))
    for r,(jp,en) in rows.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        raw=encoded(r,en,mapping)+b'\0'
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in CENTERED:
            size=SIZES.get(r,28)
            center=struct.unpack_from('>f',blob,r+4)[0]
            # These two source captions were left-anchored inside a centered popup.
            if r in (0xa9074,0xb23b4):center=-1/1280.
            struct.pack_into('>f',out,r+4,center-ink(en,mapping,widths,size)/1280.)
            if r in LIBRARY:
                struct.pack_into('>f',out,r+4,
                    center-ink(en,mapping,widths,size)/1280.
                    +LIBRARY_LIVE_X_CORRECTION[r]/640.)
            out[r+16:r+22]=bytes((size,size,size-2,size,size,size))
            out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.update(range(r+16,r+22));allowed.add(r+23)
            if r in LIVE_CENTERED:
                # These menus center by cell count at runtime. Do not subtract
                # the English ink width a second time in the FSSA coordinate.
                struct.pack_into('>f',out,r+4,-1/1280.+STORE_LIVE_X_CORRECTION/640.)
                out[r+23]|=0x40
        if r in TEAM:
            # Keep the first caption's left edge; the next counter starts at x=0.31.
            out[r+16:r+22]=bytes.fromhex('191917191919')
            allowed.update(range(r+16,r+22))
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(_,en) in ROWS.items():
        assert text(blob,r)==encoded(r,en,mapping),(hex(r),en)
        if r in CENTERED:
            assert ink(en,mapping,widths,SIZES.get(r,28))<(430 if r in LIBRARY else 210),(hex(r),en)
            if r in LIBRARY:
                assert blob[r+23]==1, 'Library special text mode must stay original'
                assert text(blob,r)==dg.encode_mixed(en,mapping), 'No Library control prefix'
                expected=-1/1280.-ink(en,mapping,widths,28)/1280.+LIBRARY_LIVE_X_CORRECTION[r]/640.
                assert abs(struct.unpack_from('>f',blob,r+4)[0]-expected)<1e-6,hex(r)
                # The library promotes its text above the stored 28px quad.
                # Even that live size must stay within the ~475px blue panel.
                assert ink(en,mapping,widths,38)+16<475,(hex(r),en)
            assert bool(blob[r+23]&0x40)==(r in LIVE_CENTERED)
            if r in LIVE_CENTERED:
                assert abs(struct.unpack_from('>f',blob,r+4)[0]-(-1/1280.+STORE_LIVE_X_CORRECTION/640.))<1e-7
        if r in (0xb23b4,0xb23f4): assert ink(en,mapping,widths,28)<185
        if r in TEAM:assert ink(en,mapping,widths,25)<154,en
    for r in SETTINGS_ROWS:
        raw=text(blob,r)
        assert raw.count(b'\n')==7
        assert dg.encode_mixed('Remember Sort / Info',mapping) in raw
    # Keep the embedded colon/parentheses beside the separately drawn
    # playback icon at the original six-fullwidth-cell offset.
    assert abs(ink('・Voice    ',mapping,widths,28)-5*28)<4
    print('PASS: intermission popup/library labels, list headers, split Team Setup titles and four settings-page variants.')

def check_descriptions(elf):
    import eboot,command_layout
    segs=eboot._segments(elf);data=segs[1]
    for en in DESCRIPTIONS.values():
        raw=(command_layout.prefix(en)+''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in en)).encode('utf8')+b'\0'
        assert elf.count(raw)==1,en
        pointer=struct.pack('>I',eboot._va(segs,elf.index(raw)))
        assert any(elf[p:p+4]==pointer for p in range(data['off'],data['off']+data['filesz'],4)),en
    print('PASS: all five Library descriptions use the live-centered English strings.')
