"""Fixed-byte D-Trader suffixes and scoped Spirit-caster UI repairs.

The shop composes a string with native fixed-count appends, not the CP932
exact draw hook. Keep every append length, allocation and terminator intact.
The sell-item suffix has an inlined four-byte store as well as a TOC string.
"""
import struct
import aiddata
import digraph as dg
import localization
from intermission_layout import text, ink

GROUP = 'trader_spirit_prompts'
# VA, original instruction, byte index in sell_name_suffix.
INLINE = ((0x2af9bc, 0x3800fff0, 3), (0x2af9c8, 0x3960ff81, 0),
          (0x2af9d8, 0x38000076, 1), (0x2af9dc, 0x3960ff82, 2))


def rows():
    cat = localization.english()
    for mid, d in cat.document('localization/messages/' + GROUP + '.json')['messages'].items():
        yield mid, d, cat.text(mid)


def patch_elf(blob, mapping):
    out = bytearray(blob)
    for mid, d, en in rows():
        c = d['context']
        if 'eboot_offset' not in c:
            continue
        off, pointer = int(c['eboot_offset'],16), int(c['pointer_offset'],16)
        jp, raw = d['source'].encode('cp932'), dg.encode_mixed(en,mapping)
        assert len(raw) == len(jp) == c['bytes'], (mid, 'native append length changed')
        assert blob[off:off+len(jp)+1] == jp+b'\0', mid
        assert struct.unpack_from('>I',blob,pointer)[0] == off+0x10000, mid
        out[off:off+len(raw)] = raw
        if mid.endswith(':sell_name_suffix'):
            for va, expected, index in INLINE:
                assert struct.unpack_from('>I',blob,va-0x10000)[0] == expected, hex(va)
                struct.pack_into('>I',out,va-0x10000,(expected & 0xffff0000)|raw[index])
    check_elf(out,mapping)
    return bytes(out)


def check_elf(blob,mapping):
    for mid,d,en in rows():
        c=d['context']
        if 'eboot_offset' not in c:
            continue
        off=int(c['eboot_offset'],16)
        raw=dg.encode_mixed(en,mapping)
        assert len(raw)==c['bytes'],mid
        assert blob[off:off+len(raw)+1]==raw+b'\0',mid
        assert struct.unpack_from('>I',blob,int(c['pointer_offset'],16))[0]==off+0x10000,mid
        if mid.endswith(':sell_name_suffix'):
            for va,expected,index in INLINE:
                assert struct.unpack_from('>I',blob,va-0x10000)[0]==(expected & 0xffff0000)|raw[index]
    print('PASS: shop buy/sell suffixes and inlined copy; native byte counts/TOC/terminators preserved.')


def apply_ui(blob,mapping,widths,original):
    out=bytearray(blob)
    for mid,d,en in rows():
        for widget in d['context'].get('widgets',[]):
            r=int(widget,16)
            assert text(original,r)==d['source'].encode('cp932'),mid
            assert text(blob,r)==text(original,r),mid
            p=(len(out)+3)&~3
            out+=bytes(p-len(out))+dg.encode_mixed(en,mapping,newline=b'\n')+b'\0'
            struct.pack_into('>I',out,r,p-aiddata.STR_BASE)
    check_ui(out,mapping,widths)
    return bytes(out)


def check_ui(blob,mapping,widths):
    for mid,d,en in rows():
        for widget in d['context'].get('widgets',[]):
            r=int(widget,16)
            assert text(blob,r)==dg.encode_mixed(en,mapping,newline=b'\n'),mid
            for line in en.split('\n'):
                assert ink(line,mapping,widths,blob[r+19])<d['context']['width_limit'],mid
    print('PASS: SP Cost/SP and all four decorative Spirit frames translated; dynamic fields untouched.')
