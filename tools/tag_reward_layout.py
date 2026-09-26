"""Tag Command translations, reward ink centering and compact Weapons title."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink

ROWS={0x9cf94:('・マルチアクション\n・ボーナスＰＰ\n・ボーナスチップ\n・チャージＳＰ',
                '・Multi Action\n・Bonus PP\n・Bonus Chips\n・Charge SP'),
      0xa06b4:('武器選択',_l10n.literal('tag_reward_layout.ROWS/0'))}
CHIPS=(0xabbf4,0xabc74,0xabd74,0xabdf4,0xabe74,0xabef4,0xabf74,0xabff4)
ROWS.update({r:('Ｚチップ：','Z Chips:') for r in CHIPS})
REWARDS={0xaa794:('ＳＲポイントを獲得しました。',_l10n.literal('tag_reward_layout.REWARDS/1')),
         0xaa7d4:('ボーナス資金１００００を入手しました。',_l10n.literal('tag_reward_layout.REWARDS/2'))}
HEADERS={0xa9194:('＜変形＞',_l10n.literal('tag_reward_layout.HEADERS/3')),
         0xa91d4:('＜精神コマンド＞',_l10n.literal('tag_reward_layout.HEADERS/4')),
         0xa91f4:('＜エレメントチェンジ＞',_l10n.literal('tag_reward_layout.HEADERS/5')),
         0xa9214:('＜強化パーツ＞',_l10n.literal('tag_reward_layout.HEADERS/6'))}
# Adjacent 0xa9234 (Search Settings) is already owned by naming_search_layout.
ROWS.update(HEADERS)
ACTION_ROWS={
    0x9c934:('・アシスト攻撃\n・アシストなし','・Assist Attack\n・No Assist'),
    0x9c954:('・反撃する\n・防御する\n・回避する','・Counterattack\n・Defend\n・Evade'),
    0x9c974:('・アシスト攻撃\n・アシストなし','・Assist Attack\n・No Assist'),
    0x9c994:('・武器選択\n・参加しない','・Select Weapon\n・Do Not Join'),
    0x9c9b4:('・アシスト攻撃\n・防御する\n・回避する','・Assist Attack\n・Defend\n・Evade'),
    0x9c9d4:('・反撃する\n・防御する\n・回避する','・Counterattack\n・Defend\n・Evade'),
    0x9cf74:('・センター攻撃\n・ワイド攻撃','・Center Attack\n・Wide Attack'),
    0xa9174:('・アシスト攻撃','・Assist Attack'),
}
ROWS.update(ACTION_ROWS)

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'),(hex(r),jp)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in HEADERS:
            assert blob[r+23]&0x40
            # This static widget uses Japanese character-count centering.
            # Use the translated ink width, relative to the same local center.
            x=struct.unpack_from('>f',blob,r+4)[0]-ink(en,mapping,widths,blob[r+16])/1280.
            struct.pack_into('>f',out,r+4,x);out[r+23]&=~0x40
            allowed.update(range(r+4,r+8));allowed.add(r+23)
    # These are joined runtime translations. Keep their original strings and
    # overlay records, but bypass the Japanese character-count centering.
    for r,(jp,en) in REWARDS.items():
        assert text(blob,r)==jp.encode('cp932') and blob[r+23]&0x40
        x=struct.unpack_from('>f',blob,r+4)[0]-ink(en,mapping,widths,blob[r+16])/1280.
        struct.pack_into('>f',out,r+4,x);out[r+23]&=~0x40
        allowed.update(range(r+4,r+8));allowed.add(r+23)
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n')
        for line in en.split('\n'):
            assert ink(line,mapping,widths,blob[r+16])<(280 if r==0x9cf94 or r in HEADERS or r in ACTION_ROWS else 150 if r==0xa06b4 else 120)
        if r in ACTION_ROWS:assert en.count('\n')==jp.count('\n')
        if r in HEADERS:
            assert not blob[r+23]&0x40
            center=struct.unpack_from('>f',blob,r+4)[0]*640+ink(en,mapping,widths,blob[r+16])/2
            assert abs(center+.5)<.001,(en,center)
    assert blob[0x9cf94+21]==40 and text(blob,0x9cf94).count(b'\n')==3
    for r,(jp,en) in REWARDS.items():
        assert text(blob,r)==jp.encode('cp932') and not blob[r+23]&0x40
        center=struct.unpack_from('>f',blob,r+4)[0]*640+ink(en,mapping,widths,blob[r+16])/2
        assert abs(center+.5)<.001,(en,center)
    print('PASS: four Tag Commands, four centered map selection headers, eight Z Chips captions, Weapons title fit; both joined reward lines ink-centered.')
