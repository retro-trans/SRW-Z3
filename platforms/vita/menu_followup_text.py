"""Remaining direct footer word and the separate Scenario Select square."""
from category_port import require,encoded
from inspect_vwf import segment

CLEAR='ui.ui_followup_layout:r_7f2318a37843ae64'
HEADING=0xA1454

def apply(raw,out,port,allowed):
    import ui_layout
    from roster_library_fixes import unique
    native=ui_layout.records(raw);p,jp=native[HEADING]
    require(jp=='■シナリオ選択','Scenario heading source changed');unique(native,p,jp)
    # Keep the bullet's native advance, but render a transparent full-width
    # space. The following translated sprite and all other square icons stay.
    out[p:p+2]='　'.encode('cp932');allowed.update(range(p,p+2))
    return dict(record=hex(HEADING),source=jp,blank_square_only=True)

def hooks(port,executable,info):
    import ui_text
    data,base=segment(executable,info,0);address=0x81271B6C
    source='クリア';raw=source.encode('cp932')+b'\0'
    require(data[address-base:address-base+len(raw)]==raw,'Direct Clear footer source changed')
    en=port.text(port.catalog.text(CLEAR));require(sum(port.widths[c] for c in en)<=100,'Clear exceeds footer gap')
    return {key:encoded(en,port.mapping) for key in (source.encode('cp932'),source.encode('utf-8'),ui_text.converted_key(source,executable,info))}
