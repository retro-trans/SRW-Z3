"""Scoped parts removal/selection captions; preserve other fragment uses."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text, ink

ROWS = {r: ('：はずし決定', _l10n.literal('parts_menu_followup.ROWS/0')) for r in (0xae0b4,0xb6ab4)}
ROWS.update({r: ('個数', 'Qty.') for r in (0xae514,0xb5754,0xb66b4)})
ROWS.update({r: ('選択Ｎｏ．', 'Select No.') for r in (0xa9694,0xaf9b4,0xb3bb4)})
ROWS.update({0xb6a94: ('パイロット','Pilot'),
             0xae4b4: ('パイ','Pilot'),0xae4d4: ('ロット','')})


def apply(blob,mapping,widths,pristine):
    out=bytearray(blob)
    for r,(jp,en) in ROWS.items():
        assert text(pristine,r)==jp.encode('cp932'),hex(r)
        raw=dg.encode_mixed(en,mapping)+b'\0'
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
    allowed={i for r in ROWS for i in range(r,r+4)}
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths,pristine)
    return bytes(out)


def check(blob,mapping,widths,pristine=None):
    if pristine is None:
        from cpk import CPK
        c=CPK('work/orig/AIDDATAPACK.CPK');pristine=c.read(c.files[0])
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping),(hex(r),en)
        assert blob[r+4:r+32]==pristine[r+4:r+32],hex(r)
        # Selection heading originally has five full-width characters.
        budget=140 if en=='Select No.' else 160 if en==': Remove' else 100
        assert ink(en,mapping,widths,blob[r+20])<=budget,(hex(r),en)
    print('PASS: 11 parts removal, quantity, pilot and selection-number records.')
