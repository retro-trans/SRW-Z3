"""Upgrade list headers/footer: both variants, with numeric widgets intact."""
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

def apply(blob,mapping,widths):
    from cpk import CPK
    k=CPK('work/orig/AIDDATAPACK.CPK');source=k.read(k.files[0])
    out=bytearray(blob)
    for r,(jp,en) in ROWS.items():
        assert text(source,r)==jp.encode('cp932'),hex(r)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
    allowed={p for r in ROWS for p in range(r,r+4)}
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),hex(r)
        for line in en.split('\n'):
            assert ink(line,mapping,widths,blob[r+19])<(200 if en=='Weapon Rank' else 145)
    print('PASS: both Weapon Rank headers and Sight/Wpn Rank footers; rank values and bars unchanged.')
