"""Execute live command-pad PPC and verify scoped menu labels."""
import struct
import eboot
import digraph as dg
import command_layout as layout
from check_confirmation_tabs import execute


def check_prep_references(blob, source):
    """Validate actual popup descriptors, not just a spare translated string."""
    segs=eboot._segments(blob);data=segs[1]
    for off,(jp,en) in layout.PREP_ROWS.items():
        assert source[off:off+len(jp.encode('utf8'))+1]==jp.encode('utf8')+b'\0'
        va=eboot._va(segs,off)
        refs=[p for p in range(data['off'],data['off']+data['filesz'],4)
              if source[p:p+4]==struct.pack('>I',va)]
        assert refs,(hex(off),jp)
        raw=(layout.prefix(en)+''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in en)).encode('utf8')+b'\0'
        for p in refs:
            target=eboot._off(segs,struct.unpack_from('>I',blob,p)[0])
            assert blob[target:target+len(raw)]==raw,(hex(p),en)


def check_blank_cells(tpack):
    for ident in (1, 3):
        b = tpack.read(next(f for f in tpack.files if f['id']==ident))
        assert b[0x18] == dg.ATLAS_FORMAT
        width = struct.unpack_from('>H',b,0x20)[0]
        for code in layout.CODES:
            idx = dg.cell_index(code)
            x,y = idx%dg.CELLS_PER_ROW*32,idx//dg.CELLS_PER_ROW*32
            for row in range(32):
                start = 0x80+((y+row)*width+x)*2
                assert not any(b[start:start+64]), (ident,hex(code))
    print('PASS:',len(layout.CODES),'command pad cells are blank in both installed font layers.')


def check(blob, mapping, ui):
    from pathlib import Path
    check_prep_references(blob,Path('work/EBOOT_dec.elf').read_bytes())
    segs = eboot._segments(blob)
    def at(va, size):
        pos = eboot._off(segs, va)
        return blob[pos:pos+size]
    code = at(eboot.STUB_VA, len(eboot.vwf_stub()))
    assert code == eboot.vwf_stub()
    helper = at(layout.CAVE, len(layout.stub()))
    assert helper == layout.stub()
    extra = ((layout.CAVE, helper), (layout.DATA, at(layout.DATA, len(layout.LABELS)*8)))
    widths = at(eboot.TABLE_VA, eboot.ATLAS_CELLS)
    table = eboot.unicode_table(blob, segs)
    cases = 0
    for i, label in enumerate(layout.LABELS):
        text = layout.prefix(label) + ''.join(chr(eboot.VWF_CP_BASE+ord(c)) for c in label)
        if label in layout.UTF8_LABELS:
            assert blob.count(text.encode('utf-8')+b'\0') == 1, label
        if 13 <= i < 17:
            record = layout.SPLIT_RECORDS[i-13]
            pos = struct.unpack_from('>I',ui,record)[0]+0x59478
            raw = struct.pack('>H',layout.CODES[i])+dg.encode_mixed(label,mapping)+b'\0'
            assert ui[pos:pos+len(raw)] == raw
        assert struct.unpack_from('>H',blob,table+2*layout.CODEPOINTS[i])[0] == layout.CODES[i]
        ink = sum(widths[dg.cell_index(mapping[c])] for c in label)
        coefficient = layout.count_coefficient(i)
        assert extra[1][1][i*8:i*8+8] == struct.pack('>ff',coefficient,ink/64.)
        for center in (-150, 0, 1150):
            for pitch in (23, 25, 31, 37.28, 42):
                for quad in (23.3, 25, 28, 32):
                    origin = center-coefficient*pitch
                    advance, acc = execute(code,widths,dg.cell_index(layout.CODES[i]),
                                           origin,origin,pitch,quad,0,extra)
                    assert abs(origin+advance+ink*quad/64-center)<.0001, (label,pitch,quad)
                    assert abs(acc-advance)<.0001
                    cases += 1
    # All decimal counts share one of two pads: the atlas digits have equal
    # advance, and the original centered string differs only in digit count.
    assert len({widths[dg.cell_index(mapping[c])] for c in '0123456789'}) == 1
    hooks = eboot.load_ui_hook()
    seen = set()
    p = eboot._off(segs,eboot.NAME_TBL)
    def zstr(va):
        pos = eboot._off(segs,va)
        return blob[pos:blob.index(b'\0',pos)]
    while True:
        key,target = struct.unpack_from('>II',blob,p); p += 8
        if not key: break
        try: jp = zstr(key).decode('cp932')
        except UnicodeDecodeError: continue
        index = layout.dialog_index(jp)
        if index is None: continue
        assert zstr(target & 0x3fffffff) == layout.dialog_prefix(jp)+eboot._encode_marked(hooks[jp],mapping)
        assert layout.count_coefficient(index) == len(jp)/2.
        seen.add(jp)
    assert len(seen) == 106+len(layout.EXTRA_DIALOGS)+len(layout.TERRAIN)+len(layout.naming_search_layout.REPORTS)+len(layout.FOLLOWUP_TERRAIN)+len(layout.ALL_TERRAIN)+len(layout.deployment_layout.CONFIRMATIONS)+len(layout.SAVE_DIALOGS), len(seen)
    assert ui[0xaba78:0xaba7c] == ui[0xaba58:0xaba5c]
    for first,second in (layout.SPLIT_RECORDS[:2],layout.SPLIT_RECORDS[2:]):
        row_index = layout.SPLIT_RECORDS.index(first)
        left,right = layout.LABELS[13+row_index:15+row_index]
        widths_px = [sum(widths[dg.cell_index(mapping[c])] for c in t)*28/32 for t in (left,right)]
        x1,y1 = struct.unpack_from('>ff',ui,first+4)
        x2,y2 = struct.unpack_from('>ff',ui,second+4)
        assert y1==y2
        assert ui[first+16:first+22] == ui[second+16:second+22] == bytes.fromhex('1c1c1a1c1c1c')
        left_edge,right_edge = x1*640-widths_px[0]/2,x2*640+widths_px[1]/2
        assert abs((left_edge+right_edge)/2+.5)<.0001
        assert abs((x2-x1)*640-sum(widths_px)/2-10)<.0001
        assert right_edge-left_edge<200, 'Split row exceeds map button interior'
    print('PASS:',cases,'emitted-PPC centering cases;',len(seen),'dialog hooks, both split-row states, all unit commands and Funds colon verified.')
