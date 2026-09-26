"""Bounded Power Parts and Network captions; no inventory or online actions."""
import struct
from category_port import require,digest,encoded
from prepare_vwf import line_widths

FILTER=0xB5D14
FILTER_SOURCE='全種　機体　地形　消費　特殊'
FILTER_ALIAS='ＵＣ'  # Two CP932 cells, exactly like 消費; category indices stay intact.
BLANKS={0xA9094:'Ｓｔｏｒｅ',0xA90B4:'へ',0xB6414:'）'}
STORE=0xA9074
# Vita crop: glyph ink center 54.5, button center 120.5 at 960/1280 scale.
# The split-label caller retains an origin offset after generic centering.
# Correct only that native widget; this is screenshot-calibrated, not PS3 data.
STORE_X=1/1280+(120.5-54.5)/(960/1280)/640


def specs():
    rows={}
    for off in (0xAEB94,0xB2B54):
        rows[off]=('【強化パーツ】','ui.intermission_layout:r_3116c33439dff787',420)
    for off in (0xAF5D4,0xB3294,0xB3514):
        rows[off]=('装備中の強化パーツ','ui.parts_network:equipped',400)
    for off in (0xAE074,0xB68D4):
        rows[off]=('：スロット決定','ui.parts_network:slot',210)
    for off in (0xAD194,0xAD394):
        rows[off]=('消費\n','ui.search_list_headers:r_0f01041fe7997827',125)
    for off in (0xAFCB4,0xB47F4):
        rows[off]=('修理','ui.roster_settings_layout:repair_compact',64)
        rows[off+32]=('補給','ui.roster_settings_layout:resupply_compact',108)
    rows[0xB63F4]=('（タッグ','ui_hook:r_56edc0d4b579afd1',125)
    for off,jp,mid in ((0xA9034,'「ストア」へ','ui.intermission_layout:r_dabd1c74af49e9a6'),
                       (STORE,'ＰＳ','ui.intermission_layout:r_dabd1c74af49e9a6'),
                       (0xA9054,'ボーナスシナリオ','ui.parts_network:bonus'),
                       (0xA90D4,'アップロード','ui.intermission_layout:r_1b431a6a690abc19'),
                       (0xA90F4,'ダウンロード','ui.intermission_layout:r_2c83af3242843d64')):
        rows[off]=(jp,mid,220)
    return rows


def bindings(raw,port):
    import ui_layout
    from roster_library_fixes import unique
    require(digest(raw)==ui_layout.SOURCE_SHA,'Parts/Network source changed')
    native=ui_layout.records(raw);out=[]
    for i,(off,(jp,mid,budget)) in enumerate(sorted(specs().items())):
        ptr,actual=native[off];require(actual==jp,'Parts/Network record mismatch')
        unique(native,ptr,jp);alias=('}%02X\n'%i) if jp.endswith('\n') else ('}%03X'%i)
        require(len(alias)<=len(jp.encode('cp932')),'Parts/Network alias exceeds slot')
        require(alias.encode()+b'\0' not in raw,'Parts/Network alias collision')
        en=port.text(port.catalog.text(mid))
        if jp=='修理':en=en.rstrip('.')  # This column is one eighth narrower than the roster.
        width=max(line_widths(en,port.widths))
        require(width<=budget,'Parts/Network caption too wide: '+mid)
        out.append(dict(record=off,pointer=ptr,source=jp,message=mid,alias=alias,
                        text=en,width=width,budget=budget))
    byoff={r['record']:r for r in out}
    for first in (0xAFCB4,0xB47F4):
        for off in (first,first+32):
            gap=(struct.unpack_from('<f',raw,off+36)[0]-struct.unpack_from('<f',raw,off+4)[0])*640
            require(gap-byoff[off]['width']>=7.9,'Parts column captions touch at 32px')
    return out


def filter_source(raw):
    import ui_layout
    native=ui_layout.records(raw);p,jp=native[FILTER]
    require(jp==FILTER_SOURCE,'Parts filter layout changed')
    # Preserve byte length, character count, separators and every category's
    # index. Native selection can still copy the same two-cell substrings.
    replacement=jp.replace('消費',FILTER_ALIAS)
    require(len(replacement.encode('cp932'))==len(jp.encode('cp932')),'Filter resized')
    require(FILTER_ALIAS.encode('cp932')+b'\0' not in raw,'Filter alias collision')
    return p,jp,replacement


def apply(raw,out,port,allowed):
    import ui_layout
    from roster_library_fixes import unique
    native=ui_layout.records(raw);report=bindings(raw,port)
    for r in report:
        p=r['pointer'];payload=r['alias'].encode()+b'\0'
        out[p:p+len(payload)]=payload;allowed.update(range(p,p+len(payload)))
    for off,jp in BLANKS.items():
        p,actual=native[off];require(actual==jp,'Parts/Network suffix changed')
        unique(native,p,jp);out[p]=0;allowed.add(p)
    # Compensate the remaining split-label origin using the supplied Vita crop.
    struct.pack_into('<f',out,STORE+4,STORE_X)
    out[STORE+23]|=0x40
    allowed.update(range(STORE+4,STORE+8));allowed.add(STORE+23)
    p,jp,replacement=filter_source(raw);unique(native,p,jp)
    key=replacement.encode('cp932');out[p:p+len(key)]=key
    allowed.update(range(p,p+len(key)))
    return report


def hooks(port,executable,info,regions):
    import ui_layout,ui_text
    cpk=port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0));rows={}
    def add(source,en,private=False):
        for key in (source.encode('cp932'),ui_text.converted_key(source,executable,info)):
            if private:require(not any(b'\0'+key+b'\0' in r for r in regions),'Native alias collision')
            require(key not in rows or rows[key]==encoded(en,port.mapping),'Parts key conflict')
            rows[key]=encoded(en,port.mapping)
    for r in bindings(raw,port):
        add(r['alias'],r['text'],True)
        if '\n' in r['alias']:
            for alias,en in zip(r['alias'].split('\n'),r['text'].split('\n')):
                if alias:add(alias,en,True)
    # These hints also have a direct EBOOT draw path; widget aliases alone
    # would leave that path Japanese. Match complete strings, not fragments.
    add('：スロット決定',port.catalog.text('ui.parts_network:slot'))
    add('（チーム）',port.catalog.text('ui_hook:r_56edc0d4b579afd1'))
    add('（タッグ）',port.catalog.text('ui_hook:r_56edc0d4b579afd1'))
    filter_source(raw)
    # The common noun is Use. SP Cost belongs only to the two Spirit-list
    # header aliases above, not every dynamically drawn 消費 category.
    add('消費',port.catalog.text('ui_hook:r_f03ef5034d024e8e'))
    add(FILTER_ALIAS,port.catalog.text('ui_hook:r_f03ef5034d024e8e'),True)
    return rows
