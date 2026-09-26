"""Pinned native split captions and redundant reward emphasis overlays.

Two-byte ASCII aliases fit even the one-kanji attack badge. No relocation,
global fragment translation, counter changes, or menu-state changes.
"""
import struct
from functools import lru_cache
from category_port import require,digest,encoded
from prepare_vwf import line_widths

@lru_cache(maxsize=4)
def alias_bank(raw,count):
    from inspect_vwf import load,segment
    import ui_text
    executable,info=load();regions=[segment(executable,info,i)[0] for i in (0,1)]
    result=[]
    for a in range(64,127):
        for b in range(33,127):
            alias=chr(a)+chr(b);key=alias.encode()
            if key+b'\0' in raw:continue
            converted=ui_text.converted_key(alias,executable,info)
            if any(b'\0'+k+b'\0' in region for k in (key,converted) for region in regions):continue
            result.append(alias)
            if len(result)==count:return result
    raise ValueError('No unused two-byte widget aliases')

def specs(native):
    # record: source, shared message, width at 32px, optional font/center
    rows={0x988B4:('攻','ui.map_popup_layout:r_7cc540f65f4d3eec',48,None,None)}
    for off in (0xA0234,0xA0254):rows[off]=('インターミッション','ui_hook:r_4e63c037d3cb8a3d',350,None,None)
    for off in (0xA3314,0xA3334):rows[off]=('のせかえ','ui.command_layout:r_aabfadaa48196183',240,None,None)
    for off in (0xA3794,0xA37B4):rows[off]=('Ｄトレーダー','ui_hook:r_f69a0e1d0d67fd0e',240,None,None)
    for off in (0xA3594,0xA35F4):rows[off]=('チー','ui.command_layout:r_e77dda179903d616',240,28,-1/1280)
    # Use the longer final fragment, blank the two initial one-cell pieces.
    for off in (0xA3694,0xA36F4):rows[off]=('レーダー','ui_hook:r_f69a0e1d0d67fd0e',240,28,-1/1280)
    rows[0xAA794]=('ＳＲポイントを獲得しました。','ui.tag_reward_layout:r_5aaf68b777e85675',1000,None,None)
    rows[0xAA7D4]=('ボーナス資金１００００を入手しました。','ui.tag_reward_layout:r_bec300a25bfc371e',1000,None,None)
    import ui_followup_layout as foot
    for off in foot.EPISODES:rows[off]=('第話','ui.ui_followup_layout:r_ae4aa1e70c4c9fe0',44,28,None)
    for off in foot.CLEARS:rows[off]=('　クリア','ui.ui_followup_layout:r_f9b35564aafcd2e7',100,None,None)
    for off in foot.TURNS:rows[off]=('＜　　ターン＞','ui.ui_followup_layout:r_3116c33439dff787',280,None,None)
    for off,(p,jp) in native.items():
        if jp=='ＳＲ' and native.get(off+32,(None,None))[1]=='ポイ' and native.get(off+64,(None,None))[1]=='ント．':
            rows[off]=('ＳＲ','ui_hook:r_536e725bfc769e27',180,28,None)
        if jp=='Ｚ' and native.get(off+32,(None,None))[1]=='チップ．':
            rows[off]=('Ｚ','ui_hook:r_62f1de6cdfb87024',170,28,None)
    return rows


def blanks(native):
    rows={0xA35B4:'編成',0xA35D4:'ム',0xA3614:'編成',0xA3634:'ム',
          0xA3654:'Ｄ',0xA3674:'ト',0xA36B4:'Ｄ',0xA36D4:'ト',
          0xAA7B4:'ＳＲポイント',0xAA7F4:'１００００'}
    for off,(p,jp) in native.items():
        if jp=='ＳＲ' and native.get(off+32,(None,None))[1]=='ポイ' and native.get(off+64,(None,None))[1]=='ント．':
            rows[off+32]='ポイ';rows[off+64]='ント．'
        if jp=='Ｚ' and native.get(off+32,(None,None))[1]=='チップ．':rows[off+32]='チップ．'
    return rows


def bindings(raw,port):
    import ui_layout
    require(digest(raw)==ui_layout.SOURCE_SHA,'Intermission UI source changed')
    native=ui_layout.records(raw);out=[]
    aliases=alias_bank(raw,len(specs(native)))
    for i,(off,(jp,mid,budget,font,center)) in enumerate(sorted(specs(native).items())):
        ptr,actual=native[off];require(actual==jp,'Intermission record mismatch')
        alias=aliases[i];require(alias.encode()+b'\0' not in raw,'Alias collision')
        require(len(jp.encode('cp932'))>=2,'Alias exceeds source')
        require(sum(ptr<=p<ptr+len(jp.encode('cp932'))+1 for p,s in native.values())==1,'Shared caption slot')
        text=port.text(port.catalog.text(mid));width=max(line_widths(text,port.widths))
        require(width<=budget,'Intermission text exceeds budget: '+mid)
        out.append(dict(record=off,pointer=ptr,source=jp,alias=alias,message=mid,text=text,
                        width=width,budget=budget,font=font,center=center))
    return out


def apply(raw,out,port,allowed):
    import ui_layout
    native=ui_layout.records(raw);report=bindings(raw,port)
    for r in report:
        p=r['pointer'];out[p:p+3]=r['alias'].encode()+b'\0';allowed.update(range(p,p+3))
        off=r['record']
        if r['font']:
            f=r['font'];out[off+16:off+21]=bytes((f,f,f-2,f,f));allowed.update(range(off+16,off+21))
        if r['center'] is not None:
            struct.pack_into('<f',out,off+4,r['center']);out[off+23]|=0x40
            allowed.update(range(off+4,off+8));allowed.add(off+23)
    for off,jp in blanks(native).items():
        ptr,actual=native[off];require(actual==jp,'Redundant overlay source changed')
        require(sum(ptr<=p<ptr+len(jp.encode('cp932'))+1 for p,s in native.values())==1,'Shared overlay slot')
        out[ptr]=0;allowed.add(ptr)
    return report


def hooks(port,executable,info,regions):
    import ui_layout,ui_text
    cpk=port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0));rows={}
    for r in bindings(raw,port):
        for key in (r['alias'].encode(),ui_text.converted_key(r['alias'],executable,info)):
            require(not any(b'\0'+key+b'\0' in region for region in regions),'Alias executable collision')
            require(key not in rows,'Duplicate compact alias')
            rows[key]=encoded(r['text'],port.mapping)
    return rows
