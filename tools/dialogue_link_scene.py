"""Supply the scene omitted by normal dialogue keyword registration.

The backlog sets 1c4938's context explicitly (19dab4/19dc8c), and clears it
after each entry (19db90/19dcdc). Normal dialogue does neither. Preserve a
non-null explicit scene; only a null context falls back to scene zero, the
same scene used by the primary selector. Keep record and glossary ID logic.
"""
import struct
import eboot
from main_link_background_layout import branch

SITE = 0x1CE1B4
CAVE = 0x78EFC0


def stub():
    p = eboot._ppc(); a = eboot._Asm(); e = a.emit
    e(p['lwz'](3,3,4))
    e(p['cmpwi'](3,0)); a.br('bne','done')
    e(p['stdu'](1,1,-0x70)); e(0x7c0802a6)
    e(p['std'](0,1,0x80))
    e(branch(CAVE+len(a.w)*4,0x1c93c8,True))
    e(p['lwz'](3,3,12))
    e(p['ld'](0,1,0x80)); e(0x7c0803a6)
    e(p['addi'](1,1,0x70))
    a.label('done'); e(0x4e800020)
    raw=a.code()
    assert CAVE+len(raw)<=0x78f000
    return raw


def apply(b,segs):
    site=eboot._off(segs,SITE); dst=eboot._off(segs,CAVE); raw=stub()
    getter=eboot._off(segs,0x1c4938)
    assert b[getter:getter+8]==bytes.fromhex('806300044e800020')
    assert b[site:site+4]==struct.pack('>I',branch(SITE,0x1c4938,True))
    assert not any(b[dst:dst+len(raw)])
    b[site:site+4]=struct.pack('>I',branch(SITE,CAVE,True))
    b[dst:dst+len(raw)]=raw
    check(b)
    return [(site,site+4),(dst,dst+len(raw))]


def check(b):
    segs=eboot._segments(b)
    for va,raw in ((SITE,struct.pack('>I',branch(SITE,CAVE,True))),(CAVE,stub())):
        at=eboot._off(segs,va)
        assert b[at:at+len(raw)]==raw,hex(va)
