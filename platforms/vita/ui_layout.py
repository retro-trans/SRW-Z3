"""Scoped Vita ASSF layout and equal-length semantic-glyph replacements.

Never append strings, move sections, edit values or replace individual kanji
globally. Fixed-cell arrays retain one cell per status/terrain slot.
"""
import struct
from category_port import require,digest,encoded
from prepare_vwf import line_widths

ARCHIVE='DATA/AIDDATA/AIDDataPack.cpk'
SOURCE_SHA='3f68877fae3e340eb64d5277fa805b61ed0961798160268af9919477a76191af'
CHOICE_ROWS=((0xA9BD4,0xA9BF4,'はい',0),(0xA9C14,0xA9C34,'いいえ',1),
             (0xA9C54,0xA9C74,'はい',0),(0xA9C94,0xA9CB4,'いいえ',1))
CHOICE_FONT=28


def choice_text(port):
    """Adapt shared fixed-column tabs to native Latin spaces and measured Xs.

    The original slash/No columns are 3/5 cells. Round gaps to the nearest
    Latin space, then align the active layer to those exact rendered words.
    No new font control opcodes or changes to selection behavior are needed.
    """
    text=port.catalog.text('issue_hook:r_ddbe581c5ea9183d')
    yes,tail=text.split('\ue01e');slash,no=tail.split('\ue01f')
    require(yes==port.catalog.text('issue_hook:r_665f01666859013b') and
            no==port.catalog.text('issue_hook:r_a571eec59b258d11') and slash=='/',
            'Confirmation translation needs a locale-specific layout')
    width=lambda s:sum(port.widths[c] for c in s)
    def gap(prefix,column):
        remaining=column*32-width(prefix)
        require(remaining>=0,'Confirmation label exceeds its native column')
        return ' '*int(remaining/port.widths[' ']+0.5)
    prefix=yes+gap(yes,3)+slash
    prefix+=gap(prefix,5)
    return prefix+no,((0,width(yes)),(width(prefix),width(no)))


def records(data):
    require(data[:8]==b'ASSF\1\0\0\0','Not native Vita ASSF')
    base,end,first,last=[struct.unpack_from('<I',data,i)[0] for i in (32,36,72,76)]
    out={}
    for off in range(first,last,32):
        p=base+struct.unpack_from('<I',data,off)[0]
        require(base<=p<end,'Widget pointer outside pool')
        stop=data.find(b'\0',p,end);require(stop>=p,'Unterminated widget')
        out[off]=(p,data[p:stop].decode('cp932'))
    return out


def apply(data,port):
    require(digest(data)==SOURCE_SHA,'Vita widget resource changed')
    native=records(data);out=bytearray(data);allowed=set();audit=[]
    # Result headings use independently drawn "ユニ" + "ット" widgets.
    # Scoped aliases put the complete Unit label in the first slot; hide only
    # that pair's suffix, never globally translate either Japanese fragment.
    for prefix,suffix in ((0xAA694,0xAA6B4),(0xAB354,0xAB374)):
        ptr,jp=native[suffix]
        require(native[prefix][1]=='ユニ' and jp=='ット','Result heading pair changed')
        require(sum(ptr<=p<ptr+len(jp.encode('cp932'))+1 for p,s in native.values())==1,
                'Result heading suffix is shared')
        out[ptr]=0;allowed.add(ptr)
        audit.append(dict(record=hex(suffix),source=jp,hidden_split_suffix=True))
    def size(off,jp,font,budget,mid):
        require(native[off][1]==jp,'Widget source/record mismatch: '+hex(off))
        text=port.text(port.catalog.text(mid))
        width=max(line_widths(text,port.widths))*font/32
        require(width<=budget,'Widget English exceeds local budget: '+mid)
        # Width, height and pitch bytes. Leave line pitch (+21), alignment,
        # position, color, pointer and status bits entirely intact.
        out[off+16:off+21]=bytes((font,font,max(1,font-2),font,font))
        allowed.update(range(off+16,off+21))
        audit.append(dict(record=hex(off),source=jp,message=mid,font=font,width=width,budget=budget))
    headers=('修理','補給','援護攻撃','援護防御')
    import ui_widget_bindings as bindings
    mids=(bindings.REPAIR,bindings.RESUPPLY,bindings.ATTACK,bindings.DEFEND)
    for start in (0xAFEF4,0xB44D4):
        for i,(jp,mid) in enumerate(zip(headers,mids)):
            size(start+32*i,jp,18,(74,106,122,154)[i],mid)
    for start in (0xA8614,0xA87F4,0xA8974):
        for i,jp in enumerate(('精神コマンド','特殊スキル','特殊能力')):
            # Actual middle caption differs from the public "Skills" label.
            off=start+32*i
            if i==1:jp=native[off][1]
            mid=('ui_hook:r_7bea3023abbf8a94',None,'ui_hook:r_dd01a4c0d1b36a8d')[i]
            if mid:size(off,jp,24,180,mid)
    for off in range(0xA8514,0xA8614,32):
        second=((off-0xA8514)//32)%2
        size(off,'システム設定'+('２' if second else '１'),24,230,
             'ui.command_layout:r_e5c678ea31eb53c5' if second else 'ui.command_layout:r_515a34ea2fe71c76')
    for off in (0xA8DB4,0xA8DD4):
        size(off,'フェイズ終了',24,170,'ui.command_layout:r_7f8c6e5c5e4e347e')
    # Use the shared compact preview label, not a global Attack abbreviation.
    # Runtime styles may ignore the requested font size; aliases below also
    # enforce the full 32px live-pitch budget for both preview records.
    for off,mid in ((0x9AC94,'ui.battle_preview_layout:r_0ea619af31c0a4bc'),
                    (0xB11F4,'ui.battle_preview_layout:r_0f01041fe7997827')):
        size(off,'攻撃',24,78,mid)
    # Reserve three native-pitch cells for unknown/max Focus values and a
    # gap before the independently drawn enemy pilot name. Both sides/states.
    for off in (0xB0F34,0xB0F74,0xB0FB4,0xB0FF4):
        size(off,'気力',19,36,'ui_hook:r_a03fabecba1508ca')
    for off in (0xBB254,0xBB274,0xBB2B4,0xBB2D4):
        atk=off in (0xBB254,0xBB274)
        size(off,'援攻．' if atk else '援防．',18,48,
             'ui.map_popup_layout:r_7cc540f65f4d3eec' if atk else 'ui.map_popup_layout:r_e96afa13f4c5fa9c')
    size(0xAC754,'気力',18,34,'ui_hook:r_a03fabecba1508ca')
    size(0xAC714,'移動',22,44,'ui.map_popup_layout:r_0ea619af31c0a4bc')
    for off in (0xAD194,0xAD394):
        size(off,'消費\n',24,112,'ui.search_list_headers:r_0f01041fe7997827')
        suffix=off+32;ptr,jp=native[suffix]
        require(jp=='ＳＰ' and sum(p==ptr for p,s in native.values())==1,
                'Redundant SP suffix is shared with another widget')
        # SP Cost already includes SP. Blank only its separate suffix;
        # the next SP value column remains byte-for-byte unchanged.
        out[ptr]=0;allowed.add(ptr)
        audit.append(dict(record=hex(suffix),source=jp,redundant_suffix=True))
    for off in (0xAD1F4,0xAD3F4):
        size(off,'＋効果',24,80,'ui.search_list_headers:r_7cc540f65f4d3eec')
    size(0xAD154,'使用回数\n',24,112,'ui.search_list_headers:r_0ea619af31c0a4bc')
    for off in (0xAB9B4,0xAC194):
        size(off,'回復：\n回復：',20,48,'ui.map_popup_layout:r_f9b35564aafcd2e7')
    for off in (0x9BC94,0x9BCB4):
        size(off,'：検索結果へ',20,185,'ui.search_list_headers:map_results_back')
    for off in (0xACB74,0xACB94):
        size(off,'＜検索ＭＡＰ確認＞　所持ユニットを確認します。',23,640,
             'ui.deployment_menu_text:r_22a9c653a7f2b8b7')
    _,choices=choice_text(port)
    for row,active,jp,index in CHOICE_ROWS:
        require(native[row][1]=='はい　／　いいえ' and native[active][1]==jp,
                'Native confirmation layers changed')
        require(data[row+16:row+22]==data[active+16:active+22]==bytes.fromhex('191917191919'),
                'Native confirmation font/pitch changed')
        base=struct.unpack_from('<f',data,row+4)[0]*640
        prefix,width=choices[index]
        # The unselected layer uses the live 28px style, while the active
        # overlay previously retained 25px. Normalize both, then align ink.
        for off in (row,active):
            out[off+16:off+21]=bytes((CHOICE_FONT,CHOICE_FONT,CHOICE_FONT-2,CHOICE_FONT,CHOICE_FONT))
            allowed.update(range(off+16,off+21))
        left=base+prefix*CHOICE_FONT/32
        x=left+(width*CHOICE_FONT/64 if data[active+23]&0x40 else 0)
        struct.pack_into('<f',out,active+4,x/640)
        allowed.update(range(active+4,active+8))
        audit.append(dict(record=hex(active),source=jp,confirmation_layer=True,
                          rendered_left=left,rendered_width=width*CHOICE_FONT/32))
    # Translate arrays BEFORE native code selects their individual cells.
    # Whole-string hooks alone cannot translate a per-status colored strip.
    replacements={}
    for group in ('ui_aiddata','ui_hook'):
        for mid,row in port.catalog.document('localization/messages/'+group+'.json')['messages'].items():
            jp=row.get('source');en=port.catalog.text(mid)
            if not jp or not any(0xE000<=ord(ch)<0xE01E for ch in en):continue
            if any(0xE000<=ord(ch)<=0xF8FF and ch not in port.mapping for ch in en):continue
            payload=encoded(en,port.mapping)
            if len(payload)!=len(jp.encode('cp932')):continue
            if jp in replacements:require(replacements[jp][0]==payload,'Conflicting semantic array')
            replacements[jp]=(payload,mid)
    for off,(p,jp) in native.items():
        if jp not in replacements:continue
        payload,mid=replacements[jp]
        out[p:p+len(payload)]=payload;allowed.update(range(p,p+len(payload)))
        audit.append(dict(record=hex(off),source=jp,message=mid,semantic_cells=len(payload)//2))
    context_bindings=bindings.apply(data,out,port,allowed)
    import intermission_fixes
    followup=intermission_fixes.apply(data,out,port,allowed)
    import roster_library_fixes
    roster=roster_library_fixes.apply(data,out,port,allowed)
    import parts_network_fixes
    parts=parts_network_fixes.apply(data,out,port,allowed)
    import team_labels
    teams=team_labels.apply(data,out,port,allowed)
    import menu_followup_text
    menu=menu_followup_text.apply(data,out,port,allowed)
    require(len(out)==len(data) and all(a==b or i in allowed for i,(a,b) in enumerate(zip(data,out))),
            'Widget patch changed an unrelated byte')
    return bytes(out),dict(status='native_widget_layout_candidate',source_sha256=SOURCE_SHA,
        sha256=digest(out),rows=audit,context_bindings=context_bindings,intermission_bindings=followup,
        roster_library_bindings=roster,
        parts_network_bindings=parts,
        team_label_bindings=teams,
        menu_followup=menu,
        pointers_and_section_sizes_preserved=True,runtime_tested=False)


def prepare(port):
    cpk=port.cpk(ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0))
    changed,audit=apply(raw,port);port.emit(ARCHIVE,0,changed)
    return audit


def executable_cells(executable,info,port):
    """Native formatter tables are four-byte slots (PS3 uses eight bytes)."""
    from inspect_vwf import segment
    from eboot import MOVEMENT_TYPE_CHARS,MOVEMENT_EXCLUSIVE
    raw,base=segment(executable,info,0);edits=[]
    expected=b''.join(jp.encode('cp932')+bytes(2) for jp,_ in MOVEMENT_TYPE_CHARS)
    for address in (0x81257DB0,0x812853D8,0x81287B40):
        require(raw[address-base:address-base+16]==expected,'Native movement formatter changed')
        for i,(jp,en) in enumerate(MOVEMENT_TYPE_CHARS):edits.append((address+i*4,jp,encoded(en,port.mapping)))
    labels={jp:en for _,jp,en in MOVEMENT_EXCLUSIVE}
    for address,jp in ((0x81257DC0,'空専用'),(0x81257DC8,'陸専用'),(0x81257DD0,'空水専用'),
                       (0x81257DDC,'水専用'),(0x812853EC,'空専用'),(0x812853F4,'空水専用'),(0x81285400,'水専用')):
        key=jp.encode('cp932');require(raw[address-base:address-base+len(key)+1]==key+b'\0',
                                     'Native exclusive movement label changed')
        edits.append((address,jp,encoded(labels[jp],port.mapping)))
    require(all(len(jp.encode('cp932'))==len(payload) for _,jp,payload in edits),'Movement label changed slot size')
    return edits
