"""Deployment confirmation family, scoped headings and separate counters."""
import localization as _l10n
import json
import struct
from pathlib import Path
import aiddata
import digraph as dg
from intermission_layout import text, ink

CATALOG = Path(__file__).resolve().parents[1]/'translation/deployment_hook.json'
CONFIRMATIONS = {r['jp']:r['en'] for r in json.loads(CATALOG.read_text(encoding='utf-8'))['lines']}
OPTIONS = tuple(range(0xa98d4,0xa9a14,32))
QUESTIONS = (0xaa314,0xaa334)
ROWS = {
    0xaec74: ('【発進チーム選択】', _l10n.literal('deployment_layout.ROWS/0')),
    0xaec94: ('【出撃チーム選択】', _l10n.literal('deployment_layout.ROWS/1')),
    0xaed74: ('：発進チーム選択', _l10n.literal('deployment_layout.ROWS/2')),
    0xb2974: ('：発進タッグ選択', _l10n.literal('deployment_layout.ROWS/3')),
    0xb2a14: ('【出撃タッグ選択】', _l10n.literal('deployment_layout.ROWS/4')),
    0xaeff4: ('＜あと　　隊＞', _l10n.literal('deployment_layout.ROWS/5')),
    0xb2a34: ('＜あと　　隊＞', _l10n.literal('deployment_layout.ROWS/6')),
    0xacad4: ('＜母艦出撃＞　出撃母艦を選択します。', _l10n.literal('deployment_layout.ROWS/7')),
    0xacb34: ('＜出撃選択＞　並び替えるチームを指定します。', _l10n.literal('deployment_layout.ROWS/8')),
    0xacb54: ('＜出撃選択＞　入れ替えるチーム／場所を指定します。', _l10n.literal('deployment_layout.ROWS/9'))
}
COUNTERS=(0xaeff4,0xb2a34)
HEADERS=(0xaec74,0xaec94,0xaed74,0xb2974,0xb2a14)

def audit_source(blob):
    refs=aiddata.refs(blob)
    expected=set(OPTIONS+QUESTIONS)
    found=set()
    for jp in CONFIRMATIONS:
        for off,t,_,_ in aiddata.strings(blob):
            if t==jp: found.update(refs.get(off,[]))
    assert found==expected, ('deployment family changed',found ^ expected)
    for r in expected:
        assert text(blob,r).decode('cp932') in CONFIRMATIONS
        assert blob[r+23]&0x40, hex(r)
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==jp.encode('cp932'), (hex(r),jp,text(blob,r))
    return len(found)

def apply(blob,mapping,widths):
    audit_source(blob)
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in ROWS.items():
        p=(len(out)+3)&~3
        out+=bytes(p-len(out))+dg.encode_mixed(en,mapping)+b'\0'
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in HEADERS:
            out[r+16:r+22]=bytes((28,28,26,28,28,28))
            allowed.update(range(r+16,r+22))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    # The live game owns these numeric fields; never freeze or rewrite them.
    for r in COUNTERS:
        assert out[r+32:r+64]==blob[r+32:r+64]
    check(out,mapping,widths)
    return bytes(out)

def check(blob,mapping,widths):
    for r,(jp,en) in ROWS.items():
        assert text(blob,r)==dg.encode_mixed(en,mapping)
        limit=300 if r in HEADERS else 65 if r in COUNTERS else 800
        assert ink(en,mapping,widths,blob[r+16])<limit, (en,limit)
    for r in OPTIONS+QUESTIONS:
        jp=text(blob,r).decode('cp932')
        assert jp in CONFIRMATIONS and blob[r+23]&0x40
        assert ink(CONFIRMATIONS[jp],mapping,widths,31)<590
    print('PASS: deployment source family 12 dialog widgets, 5 headings, 2 live counters and 3 help rows; English fits.')
