"""Source-pinned Vita roster/upgrade labels and Intermission Library buttons.

Only unique text slots change. Preserve special Library rendering modes,
numeric widgets, bars, input mappings, coordinates and all native sections.
Multiline aliases retain their line breaks before the native line splitter.
"""
from category_port import require,digest,encoded
from prepare_vwf import line_widths

LIBRARY=tuple(range(0xA62B4,0xA6374,32))
CONFIRM=(0x9BBB4,0x9BD54,0x9BD94,0x9BDF4,0x9BE54,0x9BEF4,0x9BF54,
         0x9BFB4,0x9C054,0x9C094,0x9C114,0x9C174,0x9C1F4,0x9C214,
         0x9C274,0xA2534,0xA97B4,0xA9814,0xAEE74,0xAF6F4,0xAF7F4,
         0xB0AF4,0xB9494,0xB9674)
BLANKS={0xAF5B4:'ＲＡＮＫ',0xB31D4:'ＲＡＮＫ'}


def specs():
    rows={}
    for off in (0xAEBD4,0xB2E54):
        rows[off]=('【パイロット一覧】','ui.intermission_layout:r_ae4aa1e70c4c9fe0',420)
    for off in (0xAEB74,0xB2BB4):
        rows[off]=('【機体・武器改造】','ui.command_layout:r_5905878053362b35',420)
    for off in (0xAF394,0xAF454,0xAFA54,0xB3674,0xB3874,0xB4A14):
        rows[off]=('防御','ui_hook:r_1568ff6298b12b96',72)
    for off in (0xAFD74,0xB48B4):
        rows[off]=('武器改造度','ui.upgrade_list_labels:r_7cc540f65f4d3eec',200)
    for off in (0xAF594,0xB31B4):
        rows[off]=('照準値\n武器','ui.upgrade_list_labels:r_7cc540f65f4d3eec',160)
    rows[0xA8FD4]=('ライブラリー','ui.intermission_layout:r_22a9c653a7f2b8b7',210)
    titles=(('『ロボット大図鑑』','ui.library_chart:robots'),
            ('『ロボット大図鑑』','ui.library_chart:robots'),
            ('『キャラクター事典』','ui.library_chart:characters'),
            ('『用語事典』','ui.intermission_layout:r_3e085be2698070b7'),
            ('『サウンドセレクト』','ui.intermission_layout:r_5a3e048a2a9ef0b3'),
            ('『シナリオチャート』','ui.intermission_layout:r_aa2969e71a07927d'))
    for off,(jp,mid) in zip(LIBRARY,titles):rows[off]=(jp,mid,380)
    # Compact only the fixed-width button-hint widgets. The general Confirm
    # translation, command names, button icons and their positions stay intact.
    for off in CONFIRM:rows[off]=('：決定','ui.library_chart:confirm',80)
    return rows


def unique(native,ptr,jp):
    require(sum(ptr<=p<ptr+len(jp.encode('cp932'))+1 for p,s in native.values())==1,
            'Roster/Library text slot is shared')


def bindings(raw,port):
    import ui_layout
    require(digest(raw)==ui_layout.SOURCE_SHA,'Roster/Library UI source changed')
    native=ui_layout.records(raw);result=[];index=0
    for off,(jp,mid,budget) in sorted(specs().items()):
        ptr,actual=native[off];require(actual==jp,'Roster/Library record changed')
        unique(native,ptr,jp)
        en=port.text(port.catalog.text(mid))
        # Reuse the catalog's compact rank caption in the narrow header too.
        if jp=='武器改造度':
            require(en.count('\n')==1,'Upgrade caption structure changed')
            en=en.split('\n')[1]
        lines=en.split('\n')
        require(len(lines)==len(jp.split('\n')),'Native caption line count changed')
        aliases=['^%03X'%(index+i) for i in range(len(lines))];index+=len(lines)
        alias='\n'.join(aliases)
        require(len(alias)<=len(jp.encode('cp932')),'Roster/Library alias exceeds slot')
        require(all(a.encode()+b'\0' not in raw for a in aliases),'Source alias collision')
        width=max(line_widths(en,port.widths));require(width<=budget,'Roster/Library caption too wide')
        if off in LIBRARY:
            require(raw[off+23]==1,'Special Library rendering mode changed')
            require(width*38/32+16<475,'Library caption exceeds enlarged live style')
        result.append(dict(record=off,pointer=ptr,source=jp,message=mid,alias=alias,
                           text=en,width=width,budget=budget))
    return result


def apply(raw,out,port,allowed):
    import ui_layout
    native=ui_layout.records(raw);report=bindings(raw,port)
    for r in report:
        p=r['pointer'];payload=r['alias'].encode()+b'\0'
        out[p:p+len(payload)]=payload;allowed.update(range(p,p+len(payload)))
    for off,jp in BLANKS.items():
        p,actual=native[off];require(actual==jp,'Upgrade RANK suffix changed')
        unique(native,p,jp);out[p]=0;allowed.add(p)
    return report


def hooks(port,executable,info,regions):
    import ui_layout,ui_text
    cpk=port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0));rows={}
    for r in bindings(raw,port):
        pairs=[(r['alias'],r['text'])]
        if '\n' in r['alias']:pairs+=list(zip(r['alias'].split('\n'),r['text'].split('\n')))
        for alias,en in pairs:
            for key in (alias.encode(),ui_text.converted_key(alias,executable,info)):
                require(not any(b'\0'+key+b'\0' in region for region in regions),'Executable alias collision')
                require(key not in rows,'Duplicate Roster/Library alias')
                rows[key]=encoded(en,port.mapping)
    return rows
