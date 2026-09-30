"""Upgrade list and stat-panel rank labels; numeric widgets stay intact."""
import localization as _l10n
import struct
import aiddata,digraph as dg
from intermission_layout import text,ink

ROWS={
 0xafd74:('武器改造度',_l10n.literal('upgrade_list_labels.ROWS/0')),
 0xb48b4:('武器改造度',_l10n.literal('upgrade_list_labels.ROWS/1')),
 0xaf594:('照準値\n武器',_l10n.literal('upgrade_list_labels.ROWS/2')),
 0xb31b4:('照準値\n武器',_l10n.literal('upgrade_list_labels.ROWS/3')),
 0xaf5b4:('ＲＡＮＫ',''),0xb31d4:('ＲＡＮＫ',''),
}
# Native 28px Weapon + separate small RANK: shared template and two stat
# upgrade panels. The earlier list-footer fix did not cover these widgets.
RANK_PAIRS=((0x9a454,0x9a474),(0xb9034,0xb9054),(0xb9334,0xb9354))
SHORT_ID='ui.upgrade_list_labels:weapon_rank_short'
for first,suffix in RANK_PAIRS:
    ROWS[first]=('武器',_l10n.message(SHORT_ID))
    ROWS[suffix]=('ＲＡＮＫ','')

def apply(blob,mapping,widths):
    from cpk import CPK
    k=CPK('work/orig/AIDDATAPACK.CPK');source=k.read(k.files[0])
    out=bytearray(blob)
    for r,(jp,en) in ROWS.items():
        assert text(source,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
    for first,suffix in RANK_PAIRS:
        assert source[first+16:first+24]==bytes.fromhex('1c1c1a1c1c1c3100')
        assert source[suffix+16:suffix+24]==bytes.fromhex('1c1c1a1c0f1c2500')
    allowed={p for r in ROWS for p in range(r,r+4)}
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),hex(r)
        for line in en.split('\n'):
            assert ink(line,mapping,widths,blob[r+19])<(200 if en=='Weapon Rank' else 145)
    for first,suffix in RANK_PAIRS:
        assert text(blob,suffix)==b'',hex(suffix)
        assert blob[first+19]==28,hex(first)
        assert ink(_l10n.message(SHORT_ID),mapping,widths,28)<145
    print('PASS: upgrade headers, list footers and all three stat-panel Weapon/Rank pairs; rank values and bars unchanged.')
