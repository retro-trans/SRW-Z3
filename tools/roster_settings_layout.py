"""Scoped support column headings and System Settings tab labels."""
import localization as _l10n
import struct
import aiddata
import command_layout as layout
import digraph as dg

SUPPORT = {
    0xafb34: ('援護攻撃',_l10n.literal('roster_settings_layout.SUPPORT/0')), 0xafb54: ('援護防御',_l10n.literal('roster_settings_layout.SUPPORT/1')),
    0xaff34: ('援護攻撃',_l10n.literal('roster_settings_layout.SUPPORT/2')), 0xaff54: ('援護防御',_l10n.literal('roster_settings_layout.SUPPORT/3')),
    0xb4514: ('援護攻撃',_l10n.literal('roster_settings_layout.SUPPORT/4')), 0xb4534: ('援護防御',_l10n.literal('roster_settings_layout.SUPPORT/5')),
    0xb4c34: ('援護攻撃',_l10n.literal('roster_settings_layout.SUPPORT/6')), 0xb4c54: ('援護防御',_l10n.literal('roster_settings_layout.SUPPORT/7')),
}
TABS = {r: ('システム設定'+('１' if i%2==0 else '２'),
            _l10n.literal('roster_settings_layout.TABS/8')+str(1+i%2)) for i,r in enumerate(range(0xa8514,0xa8614,32))}

def raw(label,mapping):
    prefix = struct.pack('>H',layout.CODES[layout.LABELS.index(label)]) if label.startswith('Settings ') else b''
    return prefix+dg.encode_mixed(label,mapping)+b'\0'

def check(blob,mapping,widths):
    for r,(_,en) in SUPPORT.items():
        ink=sum(widths[dg.cell_index(mapping[c])] for c in en)*28/32.
        assert ink < 90
        assert blob[r+16:r+22]==bytes.fromhex('1c1c1a1c1c1c')
    for r,(_,en) in {**SUPPORT,**TABS}.items():
        p=struct.unpack_from('>I',blob,r)[0]+aiddata.STR_BASE
        expected=raw(en,mapping)
        assert blob[p:p+len(expected)]==expected,(hex(r),en)
        if r in TABS:
            assert blob[r+23]&0x40
            assert sum(widths[dg.cell_index(mapping[c])] for c in en)*31/32. < 210
    # Heading columns are at least 128px apart; short labels leave clear gaps.
    for left,right in [(0xafb34,0xafb54),(0xaff34,0xaff54),(0xb4514,0xb4534),(0xb4c34,0xb4c54)]:
        x1=struct.unpack_from('>f',blob,left+4)[0]*640
        x2=struct.unpack_from('>f',blob,right+4)[0]*640
        w=sum(widths[dg.cell_index(mapping[c])] for c in 'S. Atk')*28/32.
        assert x2-x1-w > 35
    print('PASS: eight support headings and eight System Settings tab states fit their columns/buttons.')

def apply(blob,mapping,widths):
    out=bytearray(blob);allowed=set()
    for r,(jp,en) in {**SUPPORT,**TABS}.items():
        p=struct.unpack_from('>I',blob,r)[0]+aiddata.STR_BASE
        original=jp.encode('cp932')+b'\0'
        assert blob[p:p+len(original)]==original,hex(r)
        p=(len(out)+3)&~3;out+=bytes(p-len(out))+raw(en,mapping)
        struct.pack_into('>I',out,r,p-aiddata.STR_BASE);allowed.update(range(r,r+4))
        if r in SUPPORT:
            ink=sum(widths[dg.cell_index(mapping[c])] for c in en)*28/32.
            x=struct.unpack_from('>f',blob,r+4)[0]
            struct.pack_into('>f',out,r+4,x+(112-ink)/1280.)
            allowed.update(range(r+4,r+8))
    assert all(x==y or i in allowed for i,(x,y) in enumerate(zip(blob,out)))
    check(out,mapping,widths)
    return bytes(out)
