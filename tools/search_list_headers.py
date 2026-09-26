"""Spirit/Skills search-result columns, including both Spirit list variants."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text,ink

ROWS={
    0xad154:('使用回数\n',_l10n.literal('search_list_headers.ROWS/0')),
    0xad194:('消費\n',_l10n.literal('search_list_headers.ROWS/1')),
    0xad1b4:('ＳＰ',''),
    0xad1f4:('＋効果',_l10n.literal('search_list_headers.ROWS/2')),
    0xad394:('消費\n',_l10n.literal('search_list_headers.ROWS/3')),
    0xad3b4:('ＳＰ',''),
    0xad3f4:('＋効果',_l10n.literal('search_list_headers.ROWS/4')),
}
PAIRS=((0xad194,0xad1b4,0xad1d4),(0xad394,0xad3b4,0xad3d4))

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for row,(jp,en) in ROWS.items():
        assert text(blob,row)==jp.encode('cp932'),hex(row)
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
        struct.pack_into('>I',out,row,p-aiddata.STR_BASE)
        allowed.update(range(row,row+4))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for row,(jp,en) in ROWS.items():
        assert text(blob,row)==dg.encode_mixed(en,mapping,newline=b'\n'),hex(row)
        assert en.count('\n')==jp.count('\n')
        limit=112 if 'SP Cost' in en else 80
        assert ink(en.rstrip('\n'),mapping,widths,blob[row+16])<limit
    for first,suffix,next_column in PAIRS:
        assert text(blob,suffix)==b''
        gap=(struct.unpack_from('>f',blob,next_column+4)[0]-struct.unpack_from('>f',blob,first+4)[0])*640
        assert ink('SP Cost',mapping,widths,blob[first+16])+12<gap
    print('PASS: Uses and both SP Cost/+Eff. result-header variants; SP values, plus markers, row styles and sorting untouched.')
