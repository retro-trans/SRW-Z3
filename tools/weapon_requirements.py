"""Weapon-use warning family: dim lists, failure overlays and header accent."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text, ink

BASE, ACCENT = 0xaa354, 0xaa374
PREFIX = _l10n.literal('weapon_requirements.PREFIX/0')
HEADER = PREFIX + _l10n.literal('weapon_requirements.HEADER/1')
LABELS = [('弾数', _l10n.literal('weapon_requirements.LABELS/2')), ('ＥＮ', _l10n.literal('weapon_requirements.LABELS/3')), ('気力', _l10n.literal('weapon_requirements.LABELS/4')),
          ('スキル', _l10n.literal('weapon_requirements.LABELS/5')), ('地形', _l10n.literal('weapon_requirements.LABELS/6')), ('射程', _l10n.literal('weapon_requirements.LABELS/7')),
          ('移動後可能', _l10n.literal('weapon_requirements.LABELS/8'))]
ROWS = {0xa9a14 + i*32: ('・'+jp, '・'+en) for i,(jp,en) in enumerate(LABELS)}
ROWS.update({
    BASE: ('下記の使用条件を満たしていません。', HEADER),
    ACCENT: ('使用条件', 'requirements'),
    0xbfc14: ('・地形\n・射程\n・移動後可能\n・－－－－－－－－－',
                '・Terrain\n・Range\n・Use After Moving\n・－－－－－－－－－'),
    0xbfc34: ('・弾数\n・ＥＮ\n・気力\n・スキル',
                '・Ammo\n・EN\n・Focus\n・Skill'),
    0xbfc54: ('・地形\n・射程\n・移動後可能\n・マキシマムブレイク使用可能',
                '・Terrain\n・Range\n・Use After Moving\n・Max Break Use'),
    0x9cd34: ('移動後使用可能\n－－－－－－－－\n－－－－－－－－',
                'Use After Moving\n－－－－－－－－\n－－－－－－－－'),
    0xb89d4: ('移動後使用可能\n－－－－－－－－\n－－－－－－－－',
                'Use After Moving\n－－－－－－－－\n－－－－－－－－'),
})


def apply(blob, mapping, widths):
    out = bytearray(blob)
    allowed = set()
    center = struct.unpack_from('>f', blob, BASE+4)[0]
    size = blob[BASE+19]
    left = center - ink(HEADER, mapping, widths, size)/1280.
    for r,(jp,en) in ROWS.items():
        assert text(blob,r) == jp.encode('cp932'), hex(r)
        assert jp.count('\n') == en.count('\n')
        p = (len(out)+3)&~3
        out += bytes(p-len(out)) + dg.encode_mixed(en,mapping,newline=b'\n') + b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
        allowed.update(range(r,r+4))
        if r in (BASE, ACCENT):
            x = left if r == BASE else left + ink(PREFIX,mapping,widths,size)/640.
            struct.pack_into('>f',out,r+4,x)
            out[r+23] &= ~0x40
            allowed.update(range(r+4,r+8)); allowed.add(r+23)
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)


def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r) == dg.encode_mixed(en,mapping,newline=b'\n'), hex(r)
        for line in en.split('\n'):
            assert ink(line,mapping,widths,blob[r+19]) < (1000 if r == BASE else 420), (hex(r),line)
    x = struct.unpack_from('>f',blob,BASE+4)[0]
    accent = struct.unpack_from('>f',blob,ACCENT+4)[0]
    size = blob[BASE+19]
    assert abs((accent-x)*640 - ink(PREFIX,mapping,widths,size)) < .001
    assert not blob[BASE+23]&0x40 and not blob[ACCENT+23]&0x40
    print('PASS: 14 weapon-requirement widgets; checklist/failure variants, post-move labels, measured header accent.')


if __name__ == '__main__':
    import json
    from pathlib import Path
    from cpk import CPK
    out = Path('work/out_0.6.3')
    mapping = json.loads((out/'pairs.json').read_text())
    widths = {int(k):v for k,v in json.loads((out/'widths.json').read_text()).items()}
    k = CPK('work/orig/AIDDATAPACK.CPK')
    blob = k.read(next(f for f in k.files if f['id']==0))
    apply(blob,mapping,widths)
    print('DRY RUN: no files written. Header:',HEADER)
    print('Checklist:', ', '.join(en for jp,en in LABELS), ', Max Break Use')
