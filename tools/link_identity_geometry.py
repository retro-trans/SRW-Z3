"""PS3 name-widget measurement and translated glossary registration.

Uses only dead primary arithmetic and the reserved RX cave. No global strcmp
or source strings are changed. Original name record, navigation and colours
are retained. Unknown/non-VWF names retain the native strlen/2 * pitch rule.
"""
import struct
import eboot
from main_link_background_layout import branch

DEAD = 0x1C6968
LOOKUP = DEAD
COMPARE = 0x1C69F0
BIRTHDAY = 0x1C6A38
NAME = 0x78EF00
DEAD_NATIVE = bytes.fromhex('600000007c7d1b787fe3fb784808d77160000000388000007c6507b438c100707ba3002048002ccd600000007b6400205460063e7fe3fb782f800000419eff5c4bfffd7588e100718963002e880100727d6b077488c3002f8923002da10300227cc607747d290774894100707d080734392900017d4a31d67d2907b4390800017ce759d67d4a42147d6b01d6a00300207d6b07b47d4a07b47c0007347c003a147c0007b4f8010090c9610090fd605e9cf9610090c9810090f9210090fd80669cfc005818c9610090fd605e9cfda06018d01e0000fd805818d1be0008d19e000cf9410090c9810090fd80669cfc006018d01e00044bfffea4')


def lookup():
    """Exact entries only; r3 in/out, r4 and all nonvolatile registers survive."""
    p=eboot._ppc();a=eboot._Asm();e=a.emit
    e(p['lis'](5,eboot.NAME_TBL>>16));e(p['ori'](5,5,eboot.NAME_TBL&65535))
    a.label('entry');e(p['lwz'](6,5,0));e(p['cmpwi'](6,0));a.br('beq','done')
    e(p['lwz'](7,5,4));e(p['lis'](8,0x4000));e(p['cmplw'](7,8));a.br('bge','next')
    e(p['mr'](8,3))
    a.label('compare');e(p['lbz'](9,6,0));e(p['lbz'](10,8,0))
    e(p['cmplw'](9,10));a.br('bne','next')
    e(p['cmpwi'](9,0));a.br('beq','hit')
    e(p['addi'](6,6,1));e(p['addi'](8,8,1));a.br('b','compare')
    a.label('next');e(p['addi'](5,5,8));a.br('b','entry')
    a.label('hit');e(p['mr'](3,7))
    a.label('done');e(0x4e800020)
    raw=a.code();assert LOOKUP+len(raw)<=COMPARE
    return raw


def compare():
    # Preserve first strcmp operand and LR across the exact lookup. Tail-call
    # the same native strcmp; its result feeds the original registration loop.
    p=eboot._ppc();a=eboot._Asm();e=a.emit
    e(p['stdu'](1,1,-0x80));e(0x7c0802a6);e(p['std'](0,1,0x90))
    e(p['std'](3,1,0x70));e(p['mr'](3,4))
    e(branch(COMPARE+len(a.w)*4,LOOKUP,True));e(p['mr'](4,3))
    e(p['ld'](3,1,0x70));e(p['ld'](0,1,0x90));e(0x7c0803a6)
    e(p['addi'](1,1,0x80));e(branch(COMPARE+len(a.w)*4,0x55a30c))
    raw=a.code();assert COMPARE+len(raw)<=BIRTHDAY
    return raw


def name():
    # Enter by B, not BL: this function already saved LR. r31 = widget,
    # r29 = output rectangle. Stack+70 is the native dead conversion scratch.
    p=eboot._ppc();a=eboot._Asm();e=a.emit
    e(branch(NAME,LOOKUP,True));e(p['stw'](3,1,0x70))
    e(p['mr'](4,3));e(p['addi'](8,0,0))
    e(p['lis'](5,eboot.TABLE_VA>>16));e(p['ori'](5,5,eboot.TABLE_VA&65535))
    a.label('loop');e(p['lbz'](6,4,0));e(p['cmpwi'](6,0));a.br('beq','measured')
    e(p['addi'](6,6,-0x81));e(p['cmplwi'](6,0x1e));a.br('bgt','fallback')
    e(p['lbz'](7,4,1));e(p['addi'](7,7,-0x40));e(p['cmplwi'](7,191));a.br('bgt','fallback')
    e(p['mulli'](6,6,192));e(p['add'](6,6,7))
    e(p['cmplwi'](6,eboot.ATLAS_CELLS-1));a.br('bgt','fallback')
    e(p['lbzx'](6,5,6));e(p['cmpwi'](6,32));a.br('beq','fallback')
    e(p['add'](8,8,6));e(p['addi'](4,4,2));a.br('b','loop')
    a.label('measured')
    e(p['lwz'](9,31,0xc));e(p['mullw'](8,8,9))
    e(p['lis'](9,0x3d00));a.br('b','float') # 1/32, preserve fractional pixels
    a.label('fallback');e(p['lwz'](3,1,0x70))
    e(branch(NAME+len(a.w)*4,0x554dac,True))
    e(p['rlwinm'](8,3,31,1,31));e(p['lwz'](9,31,0x14))
    e(p['mullw'](8,8,9));e(p['lis'](9,0x3f80)) # native width * 1
    a.label('float');e(p['std'](8,1,0x70));e(p['lfd'](0,1,0x70))
    e(p['fcfid'](0,0));e(p['frsp'](0,0))
    e(p['stw'](9,1,0x70));e(p['lfs'](10,1,0x70));e(p['fmuls'](0,0,10))
    e(p['stfs'](0,1,0x70));e(p['lwz'](3,1,0x70))
    e(branch(NAME+len(a.w)*4,0x2562dc))
    raw=a.code();assert NAME+len(raw)<=0x78f000
    return raw


def dead_code():
    out=bytearray(DEAD_NATIVE)
    p=eboot._ppc();slash=BIRTHDAY+12
    birthday=struct.pack('>III',p['lis'](3,slash>>16),p['ori'](3,3,slash&65535),
                         branch(BIRTHDAY+8,0x14a7c))+'／'.encode('cp932')+b'\0\0'
    for va,raw in ((LOOKUP,lookup()),(COMPARE,compare()),(BIRTHDAY,birthday)):
        out[va-DEAD:va-DEAD+len(raw)]=raw
    return bytes(out)


def edits():
    p=eboot._ppc()
    words={0x1ce224:(branch(0x1ce224,0x55a30c,True),branch(0x1ce224,COMPARE,True)),
           0x2562d4:(branch(0x2562d4,0x554dac,True),branch(0x2562d4,NAME)),
           0x2562e4:(0x5463f87e,0x60000000),
           0x256300:(0x7c6349d6,0x60000000),
           0x25630c:(0xf8610070,p['stw'](3,1,0x70)),
           0x256310:(0xc9410070,p['lfs'](0,1,0x70)),
           0x256314:(0xfd40569c,0x60000000),
           0x256318:(0xfc005018,0x60000000)}
    words.update({0xf7924:(branch(0xf7924,0x14a7c,True),branch(0xf7924,BIRTHDAY,True)),
                  0xf797c:(branch(0xf797c,0x14a7c,True),0x60000000)})
    return [(DEAD,DEAD_NATIVE,dead_code()),(NAME,bytes(len(name())),name())]+[
        (va,struct.pack('>I',old),struct.pack('>I',new)) for va,(old,new) in words.items()]


def apply(b,segs):
    from localization import Catalog
    assert Catalog().text('ui_aiddata:birthday_format')=='{month}/{day}'
    for va,text in ((0x6eab60,'月'),(0x6eab68,'日')):
        off=eboot._off(segs,va);key=text.encode('cp932')+b'\0'
        assert b[off:off+len(key)]==key
    ranges=[]
    for va,old,new in edits():
        off=eboot._off(segs,va)
        assert b[off:off+len(old)]==old,hex(va)
        assert len(old)==len(new)
        b[off:off+len(new)]=new;ranges.append((off,off+len(new)))
    check(b)
    return ranges


def check(b):
    segs=eboot._segments(b)
    for va,old,new in edits():
        off=eboot._off(segs,va);assert b[off:off+len(new)]==new,hex(va)
