"""UTF-8 battle-animation effect table, separate from CP932 ability hooks.

Reuse canonical ability names; context-only effects live in their own catalog.
Every table slot is inventoried, including duplicates. No battle logic changes.
"""
import struct
import localization

# Canonical message, original VA, ALL data references (file offsets).
BINDINGS=(
 ('battle_effect_labels:barrier_field',0x6ed668,(0x84e61c,0x84e620)),
 ('abilities:r_5dda5198137cb02a',0x6ed688,(0x84e624,0x84e628)),
 ('ui_hook:r_924516c8de2b5342',0x6ed6a8,(0x84e62c,0x84e630,0x84e67c)),
 ('abilities:r_0bbe0b4f5364e732',0x6ed6b8,(0x84e634,)),
 ('abilities:r_0121a166c715cdff',0x6ed6e0,(0x84e638,0x84e63c)),
 ('abilities:r_83ec59afbecdec14',0x6ed700,(0x84e640,0x84e644)),
 ('battle_effect_labels:radiation_wave',0x6ed720,(0x84e648,)),
 ('abilities:r_0f58a8822381e57f',0x6ed730,(0x84e64c,)),
 ('abilities:r_b42ab697149a7c8a',0x6ed748,(0x84e650,)),
 ('abilities:r_77949221bf58f862',0x6ed768,(0x84e654,)),
 ('abilities:r_479b340ccc6c572b',0x6ed788,(0x84e658,)),
 ('abilities:r_70b9c4b9f1f37eff',0x6ed7a8,(0x84e65c,)),
 ('abilities:r_3559d2fad32c2435',0x6ed7c8,(0x84e660,)),
 ('abilities:r_f7570547e9f80a64',0x6ed7e8,(0x84e664,)),
 ('abilities:r_cbab0f4720e1fcf1',0x6ed808,(0x84e668,0x84e66c)),
 ('abilities:r_ca4acbac57a2a35e',0x6ed820,(0x84e670,0x84e674)),
 ('abilities:r_30fad37a42bd3ad3',0x6ed838,(0x84e678,)),
 ('abilities:r_9fcb3754cb1773c7',0x6ed850,(0x84e680,)),
 ('battle_effect_labels:beam_coat',0x6ed860,(0x84e684,)),
 ('abilities:r_ec2ea17765052401',0x6ed878,(0x84e688,0x84e694,0x84e698,0x84e69c,0x84e6a0)),
 ('abilities:r_5d08ad19e2da125b',0x6ed880,(0x84e68c,)),
 ('abilities:r_f2d4255f1c2f7542',0x6ed8a0,(0x84e690,)),
 ('ui_utf8:r_98d15b8cc09bc915',0x6ed8c0,(0x84e6a4,)),
 ('battle_effect_labels:shield_defense',0x6ed8c8,(0x84e6a8,)),
 ('battle_effect_labels:parry',0x6ed8e0,(0x84e6ac,)),
 ('battle_effect_labels:stats_halved',0x6ed8f0,(0x84e6b0,)),
 ('battle_effect_labels:incapacitated',0x6ed900,(0x84e6b4,)),
 ('battle_effect_labels:focus_down',0x6ed910,(0x84e6b8,)),
 ('battle_effect_labels:sp_down',0x6ed920,(0x84e6bc,)),
 ('battle_effect_labels:en_down',0x6ed930,(0x84e6c0,)),
 ('battle_effect_labels:mobility_down',0x6ed940,(0x84e6c4,)),
 ('battle_effect_labels:accuracy_down',0x6ed958,(0x84e6c8,)),
 ('battle_effect_labels:armor_down',0x6ed970,(0x84e6cc,)),
 ('battle_effect_labels:focus_up',0x6ed988,(0x84e6d0,)),
 ('skills:r_1c0b0be02b38d5c4',0x6ed998,(0x84e6d4,)),
 ('battle_effect_labels:stats_up',0x6ed9a8,(0x84e6d8,)),
 ('abilities:r_ac6fe7838e95647b',0x6ed9b8,(0x84e6dc,)),
 ('battle_effect_labels:spirit_effect',0x6ed9c8,(0x84e6e0,)),
 ('battle_effect_labels:move_up',0x6ed9d8,(0x84e6e4,)),
)


def labels():
    cat=localization.english()
    return {cat.definition(mid)['source']:cat.text(mid) for mid,_,_ in BINDINGS}


def check_source(blob):
    import eboot
    segs=eboot._segments(blob);cat=localization.english()
    assert sorted(p for _,_,refs in BINDINGS for p in refs)==list(range(0x84e61c,0x84e6e8,4))
    low=segs[1]['off'];high=low+segs[1]['filesz']
    for mid,va,refs in BINDINGS:
        off=eboot._off(segs,va)
        assert eboot._cstr(blob,off)==cat.definition(mid)['source'].encode('utf-8'),mid
        actual=tuple(p for p in range(low,high-3,4) if struct.unpack_from('>I',blob,p)[0]==va)
        assert actual==refs,('Battle effect reference drift',mid,actual)


def check_built(blob,mapping,widths):
    import eboot
    from intermission_layout import ink
    segs=eboot._segments(blob);cat=localization.english()
    unicode=eboot.unicode_table(blob,segs)
    for mid,_,refs in BINDINGS:
        en=cat.text(mid)
        assert en and all(32<=ord(c)<127 for c in en),mid
        # Conservative banner budget; preserve native font/position/color.
        assert ink(en,mapping,widths,32)<=360,(mid,en)
        expected=''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in en).encode('utf-8')
        for ref in refs:
            va=struct.unpack_from('>I',blob,ref)[0]
            assert eboot._cstr(blob,eboot._off(segs,va))==expected,(mid,hex(ref))
        for c in en:
            assert struct.unpack_from('>H',blob,unicode+2*(eboot.VWF_CP_BASE+ord(c)))[0]==mapping[c]
    print('PASS: 39 UTF-8 battle-effect labels, all 51 references and English font mappings.')
