"""Translate split Team labels without global kana hooks or moved values."""
from category_port import require,digest,encoded

MESSAGE='ui_hook:r_132f605d02975e71'
SPECS=((0xAD914,'チ',94),(0xAEDF4,'チ　ム',100))
BLANKS={0xAD8F4:'ー',0xAD934:'ム．',0xAEDD4:'ー'}


def bindings(raw,port):
    import ui_layout
    from roster_library_fixes import unique
    require(digest(raw)==ui_layout.SOURCE_SHA,'Team label source changed')
    native=ui_layout.records(raw);en=port.text(port.catalog.text(MESSAGE))
    width=sum(port.widths[c] for c in en);rows=[]
    import intermission_fixes
    used=len(intermission_fixes.specs(native))
    aliases=intermission_fixes.alias_bank(raw,used+len(SPECS))[used:]
    for (off,jp,budget),alias in zip(SPECS,aliases):
        p,actual=native[off];require(actual==jp,'Team label fragment changed')
        unique(native,p,jp)
        require(alias.encode()+b'\0' not in raw,'Team alias collision')
        require(len(alias)<=len(jp.encode('cp932')),'Team alias exceeds slot')
        require(width<=budget,'Team caption exceeds its value column')
        rows.append(dict(record=off,pointer=p,source=jp,alias=alias,message=MESSAGE,
                         text=en,width=width,budget=budget))
    return rows


def apply(raw,out,port,allowed):
    import ui_layout
    from roster_library_fixes import unique
    native=ui_layout.records(raw);report=bindings(raw,port)
    for row in report:
        p=row['pointer'];out[p:p+3]=row['alias'].encode()+b'\0';allowed.update(range(p,p+3))
    for off,jp in BLANKS.items():
        p,actual=native[off];require(actual==jp,'Team overlay identity changed')
        unique(native,p,jp);out[p]=0;allowed.add(p)
    return report


def hooks(port,executable,info,regions):
    import ui_layout,ui_text
    cpk=port.cpk(ui_layout.ARCHIVE);raw=cpk.read(next(e for e in cpk.files if e['id']==0));rows={}
    for r in bindings(raw,port):
        for key in (r['alias'].encode(),ui_text.converted_key(r['alias'],executable,info)):
            require(not any(b'\0'+key+b'\0' in region for region in regions),'Team alias matches native text')
            require(key not in rows,'Duplicate Team alias')
            rows[key]=encoded(r['text'],port.mapping)
    return rows
