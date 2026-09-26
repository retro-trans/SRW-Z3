"""Exact composed-heading hooks from the original episode/title metadata.

Do not repoint title tables or mutate save strings. Script comments contain
obsolete episode numbers; the executable's 181 32-byte records are authoritative.
191564 reads title index +0x10; chapter number is the halfword at +0x0e.
"""
import localization as _l10n
import functools
import struct
import unicodedata
from pathlib import Path
import scenario_title

ROOT=Path(__file__).resolve().parents[1]
EXTRA={
 'ハイキングに行く／ハイキングに行かない':_l10n.literal('episode_heading_hooks.EXTRA/0'),
 'ハイキングに行く':_l10n.literal('episode_heading_hooks.EXTRA/1'),'ハイキングに行かない':_l10n.literal('episode_heading_hooks.EXTRA/2'),
 '変質者を追う／助っ人を引き受ける':_l10n.literal('episode_heading_hooks.EXTRA/3'),
 '変質者を追う':_l10n.literal('episode_heading_hooks.EXTRA/4'),'助っ人を引き受ける':_l10n.literal('episode_heading_hooks.EXTRA/5'),
 '宇宙ルート／地上ルート／ミスリルルート':_l10n.literal('episode_heading_hooks.EXTRA/6'),
 '宇宙ルート':_l10n.literal('episode_heading_hooks.EXTRA/7'),'地上ルート':_l10n.literal('episode_heading_hooks.EXTRA/8'),'ミスリルルート':_l10n.literal('episode_heading_hooks.EXTRA/9'),
 '依頼を受ける／依頼を受けない':_l10n.literal('episode_heading_hooks.EXTRA/10'),
 '依頼を受ける':_l10n.literal('episode_heading_hooks.EXTRA/11'),'依頼を受けない':_l10n.literal('episode_heading_hooks.EXTRA/12'),
 'ネオ・ジオンの調査に向かう／静観する':_l10n.literal('episode_heading_hooks.EXTRA/13'),
 'ネオ・ジオンの調査に向かう':_l10n.literal('episode_heading_hooks.EXTRA/14'),'ネオ・ジオンを静観する':_l10n.literal('episode_heading_hooks.EXTRA/15'),
 '休暇を取る／職務に専念する':_l10n.literal('episode_heading_hooks.EXTRA/16'),
 '休暇を取る':_l10n.literal('episode_heading_hooks.EXTRA/17'),'職務に専念する':_l10n.literal('episode_heading_hooks.EXTRA/18'),
 'メリダ島へ行く／日本に残る':_l10n.literal('episode_heading_hooks.EXTRA/19'),
 'メリダ島ルート':_l10n.literal('episode_heading_hooks.EXTRA/20'),'日本ルート':_l10n.literal('episode_heading_hooks.EXTRA/21'),
 'クリアデータ':_l10n.literal('episode_heading_hooks.EXTRA/22'),'エーストークデータ':_l10n.literal('episode_heading_hooks.EXTRA/23'),
 'ガイダンスシナリオ':_l10n.literal('episode_heading_hooks.EXTRA/24'),'終了メッセージデータ':_l10n.literal('episode_heading_hooks.EXTRA/25'),
 'デバグステージ':_l10n.literal('episode_heading_hooks.EXTRA/26'),'マップデバグステージ':_l10n.literal('episode_heading_hooks.EXTRA/27'),
}
EXTRA.update({'謎のプレゼント'+str(n).translate(str.maketrans('1234567','１２３４５６７')):'Mystery Gift '+str(n) for n in range(1,8)})

@functools.lru_cache(maxsize=1)
def catalog():
    b=(ROOT/'work/EBOOT_dec.elf').read_bytes()
    # Load-address and field-access instruction guards, not guessed table offsets.
    assert b[0x1815f8:0x1815fc]==bytes.fromhex('8122b4e8')
    translations={unicodedata.normalize('NFKC',r['Japanese']):r['English'] for r in scenario_title.ROWS}
    translations.update({unicodedata.normalize('NFKC',jp):en for jp,en in EXTRA.items()})
    titles=[]
    for i in range(159):
        p=struct.unpack_from('>I',b,0x852b70+i*4)[0]-0x10000
        assert 0x6ed700<=p<0x6ef000,hex(p)
        jp=b[p:b.index(b'\0',p)].decode('cp932')
        titles.append((jp,translations[unicodedata.normalize('NFKC',jp)]))
    records=set()
    for i in range(181):
        number,index=struct.unpack_from('>hh',b,0x853070+i*32+14)
        if 0<=index<159:records.add((number,index))
    assert (10,16) in records and titles[16][0]=='魔王の誘い'
    return titles,sorted(records)

def hooks():
    titles,records=catalog();out={jp:en for jp,en in titles}
    locale=_l10n.Catalog()
    for number,index in records:
        jp,en=titles[index]
        if number>0:
            for digits in {str(number),str(number).zfill(2)}:
                wide=digits.translate(str.maketrans('0123456789','０１２３４５６７８９'))
                out['第'+wide+'話『'+jp+'』']=locale.text('ui.episode_heading_hooks:numbered_heading').format(number=number,title=en)
        if number<0:out['『'+jp+'』']='『'+en+'』'
        # Only valid special-heading families, not a title/number Cartesian
        # product: preserve the existing bounded 4096-entry lookup table.
        special=[]
        if number==60:special.append(('最終話',locale.text('ui.episode_heading_hooks:final_label')))
        if number==61:special.append(('エピローグ',locale.text('ui.episode_heading_hooks:epilogue_label')))
        if 100<=index<=121:special.append(('分岐シナリオ',locale.text('ui.episode_heading_hooks:route_label')))
        for a,z in special:
            out[a+'『'+jp+'』']=z+' 『'+en+'』'
    return out
