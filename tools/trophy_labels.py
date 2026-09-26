"""RPCS3 trophy 022 text only; never reads or changes earned trophy records."""
import localization as _l10n
import hashlib
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

SOURCE=Path('work/orig/TROPHY.TRP')
SOURCE_SHA256='f7c8d2578d213c0ffb7faea89f4c007e3faa354315455fe5db036b1b93c31cb5'
TARGETS=('TROP.SFM','TROP_00.SFM')
NAME=_l10n.literal('trophy_labels.NAME/0')
DETAIL=_l10n.literal('trophy_labels.DETAIL/1')

def entries(blob):
    assert blob[:4]==bytes.fromhex('dca24d00')
    assert struct.unpack_from('>IQII',blob,4)==(2,len(blob),40,64)
    result={}
    for i in range(40):
        p=64+i*64;name=blob[p:p+32].split(b'\0')[0].decode('ascii')
        offset,size=struct.unpack_from('>QQ',blob,p+32)
        assert offset>=64+40*64 and offset+size<=len(blob)
        result[name]=(offset,size)
    assert len(result)==40
    return result

def checksum(blob):
    copy=bytearray(blob);copy[28:48]=bytes(20)
    return hashlib.sha1(copy).digest()

def apply(original):
    assert hashlib.sha256(original).hexdigest()==SOURCE_SHA256
    assert checksum(original)==original[28:48]
    out=bytearray(original)
    for filename in TARGETS:
        offset,size=entries(original)[filename];raw=original[offset:offset+size]
        root=ET.fromstring(raw);target=root.find("trophy[@id='022']")
        assert target is not None and target.attrib=={'id':'022','hidden':'no','ttype':'B','pid':'000'}
        assert target.findtext('name')=='休息の時' and target.findtext('detail')=='終了メッセージを見る。'
        for tag,en in [('name',NAME),('detail',DETAIL)]:
            jp=target.findtext(tag)
            old=('<%s>%s</%s>'%(tag,jp,tag)).encode('utf-8')
            new=('<%s>%s</%s>'%(tag,en,tag)).encode('utf-8')
            assert raw.count(old)==1 and len(new)<=len(old)
            # Outside-element whitespace preserves entry offsets/sizes and
            # does not become part of the visible trophy name/description.
            raw=raw.replace(old,new+b' '*(len(old)-len(new)))
        out[offset:offset+size]=raw
    out[28:48]=checksum(out)
    verify(original,bytes(out))
    return bytes(out)

def verify(original,built):
    assert len(original)==len(built) and checksum(built)==built[28:48]
    assert entries(original)==entries(built)
    a=bytearray(original);b=bytearray(built);a[28:48]=b[28:48]=bytes(20)
    for name,(offset,size) in entries(original).items():
        if name not in TARGETS:
            assert original[offset:offset+size]==built[offset:offset+size]
            continue
        old=ET.fromstring(original[offset:offset+size]);new=ET.fromstring(built[offset:offset+size])
        expected=original[offset:offset+size]
        for tag,jp,en in [('name','休息の時',NAME),('detail','終了メッセージを見る。',DETAIL)]:
            before=('<%s>%s</%s>'%(tag,jp,tag)).encode('utf-8')
            after=('<%s>%s</%s>'%(tag,en,tag)).encode('utf-8')
            expected=expected.replace(before,after+b' '*(len(before)-len(after)))
        assert built[offset:offset+size]==expected
        changed=new.find("trophy[@id='022']")
        assert changed.findtext('name')==NAME and changed.findtext('detail')==DETAIL
        changed.find('name').text='休息の時';changed.find('detail').text='終了メッセージを見る。'
        def semantic(node):return node.tag,node.attrib,(node.text or '').strip(),tuple(semantic(c) for c in node)
        assert semantic(old)==semantic(new)
        a[offset:offset+size]=b[offset:offset+size]=bytes(size)
    assert a==b

def build(out):
    if not SOURCE.exists():
        from extract import Source
        Source(disc='E:/SRWZ3/PS3_GAME/USRDIR').path('TROPHY.TRP')
    original=SOURCE.read_bytes();built=apply(original)
    target=Path(out)/'TROPHY.TRP';target.write_bytes(built)
    verify(original,target.read_bytes())
    print('PASS: trophy 022 Time to Rest; both locale payloads and TRP checksum verified; IDs, conditions, icons and other trophies unchanged.')
