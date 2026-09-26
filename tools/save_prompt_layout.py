"""Protect the left-aligned save notification from centered prompt hooks."""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text

ROW=0xbfa54
JP='セーブが終了しました。'
EN=_l10n.literal('save_prompt_layout.EN/0')

def apply(blob,mapping):
    assert text(blob,ROW)==JP.encode('cp932')
    assert not blob[ROW+23]&0x40
    # The question screen renders this sentence centered, but this distinct
    # status notification is left-aligned. Give it its own encoded text so it
    # cannot match the Japanese centered-dialog key at draw time.
    out=bytearray(blob);pos=(len(out)+3)&~3
    out+=bytes(pos-len(out))+dg.encode_mixed(EN,mapping)+b'\0'
    struct.pack_into('>I',out,ROW,pos-aiddata.STR_BASE)
    assert out[:ROW]==blob[:ROW] and out[ROW+4:len(blob)]==blob[ROW+4:]
    check(out,mapping)
    return bytes(out)

def check(blob,mapping):
    assert text(blob,ROW)==dg.encode_mixed(EN,mapping)
    assert not blob[ROW+23]&0x40
    print('PASS: standalone Save complete notification retains its original left-aligned widget; centered question lines use separate pads.')
