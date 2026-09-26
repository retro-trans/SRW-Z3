"""Scoped native widget aliases into the shared draw-time translation table.

Four ASCII bytes and a terminator fit the original verified pools. No pool
growth or pointer relocation. Both native SJIS and UTF-8 draw modes are bound.
Unlike a global Japanese-key preference, these aliases keep compact roster
captions out of other screens. Widths use 32px, even if a runtime style ignores
the record's requested smaller font.
"""
import struct
from category_port import require,digest,encoded

REPAIR='ui.roster_settings_layout:repair_compact'
RESUPPLY='ui.roster_settings_layout:resupply_compact'
ATTACK='ui.roster_settings_layout:r_fc00d6eef03a120d'
DEFEND='ui.roster_settings_layout:r_601d77ae3cbbe336'


def specs():
    rows={}
    rows[0x99334]=('右スティック','ui.training_help_layout:r_0ea619af31c0a4bc',180)
    for off in (0xAA694,0xAB354):
        rows[off]=('ユニ','ui_hook:r_70b9c4b9f1f37eff',160)
    rows[0xAB154]=('ユニット','ui_hook:r_70b9c4b9f1f37eff',160)
    rows[0xA54F4]=('キャラクター事典','ui.library_chart:characters',300)
    rows[0xA5554]=('ロボット大図鑑','ui.library_chart:robots',300)
    for off,mid in ((0x9AC94,'ui.battle_preview_layout:r_0ea619af31c0a4bc'),
                    (0xB11F4,'ui.battle_preview_layout:r_0f01041fe7997827')):
        rows[off]=('攻撃',mid,78)
    for off in range(0xA8514,0xA8614,32):
        second=((off-0xA8514)//32)%2
        rows[off]=('システム設定'+('２' if second else '１'),
                   'ui.command_layout:r_e5c678ea31eb53c5' if second else
                   'ui.command_layout:r_515a34ea2fe71c76',210)
    for start in (0xAFEF4,0xB44D4):
        for i,(jp,mid,budget) in enumerate(zip(('修理','補給','援護攻撃','援護防御'),
                (REPAIR,RESUPPLY,ATTACK,DEFEND),(72,106,120,120))):
            rows[start+i*32]=(jp,mid,budget)
    for off in (0xAFB34,0xB4C34):
        rows[off]=('援護攻撃',ATTACK,120)
        rows[off+32]=('援護防御',DEFEND,120)
    rows[0xAC714]=('移動','ui.map_popup_layout:r_0ea619af31c0a4bc',54)
    for off in (0xAA834,0xB8494,0xB8D54,0xB8F54):
        rows[off]=('エースボーナス','ui_hook:r_d89011fe3e5d082a',210)
    for off in (0xAD7D4,0xB6FF4,0xB8254,0xB8B34,0xB8E74):
        rows[off]=('能力','ui_hook:r_04e815a8d425827d',92)
    return rows


def bindings(data,port):
    import ui_layout
    require(digest(data)==ui_layout.SOURCE_SHA,'Widget alias source changed')
    native=ui_layout.records(data);result=[]
    for index,(off,(jp,mid,budget)) in enumerate(sorted(specs().items())):
        ptr,actual=native[off]
        require(actual==jp,'Widget alias source identity changed')
        alias=('~%03X'%index).encode('ascii')
        require(len(alias)<=len(jp.encode('cp932')),'Alias exceeds native text slot')
        require(not any(ptr<=p<ptr+len(jp.encode('cp932'))+1 for row,(p,s) in native.items() if row!=off),
                'Widget alias pool range is shared')
        require(alias+b'\0' not in data,'Widget alias already occurs in source')
        text=port.text(port.catalog.text(mid));width=sum(port.widths[c] for c in text)
        require(text and '\n' not in text and width<=budget,'Compact widget exceeds live-pitch budget: '+mid)
        result.append(dict(record=hex(off),pointer=ptr,source=jp,message=mid,alias=alias.decode(),
                           text=text,width=width,budget=budget,max_runtime_font=32))
    # Prove neighboring columns cannot touch at the conservative live pitch.
    byoff={int(r['record'],16):r for r in result}
    for start in (0xAFEF4,0xB44D4):
        for i in range(3):
            a=start+32*i;b=a+32
            gap=(struct.unpack_from('<f',data,b+4)[0]-struct.unpack_from('<f',data,a+4)[0])*640
            require(gap-byoff[a]['width']>=7.9,'Roster captions overlap at native live pitch')
    return result


def apply(data,out,port,allowed):
    report=bindings(data,port)
    for row in report:
        p=row['pointer'];payload=row['alias'].encode()+b'\0'
        out[p:p+len(payload)]=payload;allowed.update(range(p,p+len(payload)))
    return report


def hooks(port,executable,info,regions):
    import ui_layout,ui_text
    archive=port.cpk(ui_layout.ARCHIVE);raw=archive.read(next(e for e in archive.files if e['id']==0))
    result={}
    for row in bindings(raw,port):
        alias=row['alias'];keys={alias.encode(),ui_text.converted_key(alias,executable,info)}
        for key in keys:
            require(not any(b'\0'+key+b'\0' in r for r in regions),'Alias collides with native executable string')
            require(key not in result,'Duplicate widget alias')
            result[key]=encoded(row['text'],port.mapping)
    return result
