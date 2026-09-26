"""Native Vita exact-text draw hook; in-memory candidate, never installation.

At 0x81006e50 r7 holds SJIS after the original optional UTF-8 conversion.
At 0x810d9dd8 r2 holds whole MtV text before line counting and splitting.
Match whole NUL-terminated strings only. Shared wording is relocated after
original BSS; no fixed source slot, PS3 code, prefix or fragment matching.
"""
import copy
import struct
from collections import defaultdict, Counter
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import vwf
from inspect_vwf import load, segment
from self_decrypt import parse, make_fself
from category_port import require, digest, encoded, wrap

SITE=0x81006E50
ORIGINAL='vmov.f32 s0, #-1.0'
DESCRIPTION_SITE=0x810D9DD8
DESCRIPTION_ORIGINAL='adds r0, r2, #0; str r1, [sp, #0x18]'
CENTER_SITE=0x81007974
CENTER_ORIGINAL='vmul.f32 s0, s0, s1'
POINTER=vwf.DELTA-4
NAMES_POINTER=POINTER-4
NAME_SITES=(0x810CBE50,0x810CBE78,0x810CBE9C,0x810CBF46)
GROUPS=('ui_hook','ui_utf8','ui_eboot','abilities','spirit_hook','skill_hook',
        'ability_hook','parts_desc_hook','gift_report_hook','tutorial_hook',
        'issue_hook','trader_hook','terrain_hook','naming_hook','weapon_effect_hook',
        'battle_report_hook','unlock_report_hook','message_class_hook',
        'unlock_shop_hook','terrain_all_hook','mission_conditions_hook',
        'deployment_hook','squad_names_hook','ui.key_help_labels',
        'scenario_titles','ui.episode_heading_hooks','ui_aiddata','ui.runtime_names','date_cards',
        'ui.map_popup_layout','ui.command_layout','ui.storage',
        'ui.search_list_headers','ui.deployment_menu_text','ui.library_list_labels','glossary')
FORMAT=re.compile(r'%(?:[-+0 #]*\d*(?:\.\d+)?[hl]*[diuoxXfFeEgGcsnp])')


def has_format(text,english=False):
    # English percentages such as "30% for" and "5% per" are prose,
    # not printf's space-flag %f/%p. Only exempt digit-following percent
    # signs before whitespace/punctuation; real placeholders remain guarded.
    if english:
        text=re.sub(r'(?<=\d)%(?=\s|[.,;:!?)]|$)','',text)
    return bool(FORMAT.search(text))


def hash_key(data):
    value=5381
    for byte in data:value=(value*33+byte)&0xFFFFFFFF
    return value


def table(rows):
    """Relative offsets only. Full comparison protects against hash collisions."""
    require(rows and all(k and b'\0' not in k and b'\0' not in v for k,v in rows.items()),'Invalid UI key/value')
    require(all(max(map(len,v.split(b'\n')))<=256 for v in rows.values()),
            'UI description exceeds native 256-byte line buffer')
    ordered=sorted(rows.items(),key=lambda pair:(hash_key(pair[0]),pair[0]))
    header=bytearray(4+12*len(ordered));struct.pack_into('<I',header,0,len(ordered))
    payload=bytearray()
    for i,(key,value) in enumerate(ordered):
        ko=len(header)+len(payload);payload+=key+b'\0'
        vo=len(header)+len(payload);payload+=value+b'\0'
        struct.pack_into('<III',header,4+i*12,hash_key(key),ko,vo)
    return bytes(header+payload)


def lookup_prefix(address,pointer):
    return vwf.assemble('''push.w {r0-r6,r12,lr}; mrs r12,apsr; push {r12};
        adr.w r0,#%d; ldr r1,[r0]; add r0,r1'''%pointer,address)


def name_stub(address,lookup):
    # A separate exact-key table prevents a custom name that happens to equal
    # a UI caption from being translated. Share only the comparison code.
    prefix=lookup_prefix(address,NAMES_POINTER)
    core=lookup+len(lookup_prefix(lookup,POINTER))
    entry=prefix+vwf.assemble('b.w %d'%core,address+len(prefix))
    wrapper=address+len(entry)
    code=vwf.assemble('''push {r7,lr}; vpush {s0-s1}; mov r7,r1;
        bl %d; mov r1,r7; vpop {s0-s1}; blx %d; pop {r7,pc}'''
        %(address,0x8121DC20),wrapper)
    require(wrapper+len(code)<=NAMES_POINTER,'Name hook exceeds RX reservation')
    return entry+code,wrapper


def stub(address):
    # r7 is the only intentional integer output. All other integer registers,
    # APSR flags, SP and LR survive; replay exactly the displaced VMOV.
    assembly='''
        push.w {r0-r6, r12, lr}
        mrs r12, apsr
        push {r12}
        adr.w r0, #%d
        ldr r1, [r0]
        add r0, r1
        mov r3, r7
        movw r2, #5381
    hash_loop:
        ldrb r4, [r3], #1
        cbz r4, hash_done
        add.w r2, r2, r2, lsl #5
        add r2, r4
        b hash_loop
    hash_done:
        ldr r1, [r0]
        adds r5, r0, #4
    entry_loop:
        cbz r1, finished
        ldr r4, [r5]
        cmp r4, r2
        bne next_entry
        ldr r3, [r5, #4]
        add r3, r0
        mov r6, r7
    compare_loop:
        ldrb r4, [r3], #1
        ldrb r12, [r6], #1
        cmp r4, r12
        bne next_entry
        cbnz r4, compare_loop
        ldr r7, [r5, #8]
        add r7, r0
        b finished
    next_entry:
        adds r5, #12
        subs r1, #1
        b entry_loop
    finished:
        pop {r12}
        msr apsr_nzcvq, r12
        pop.w {r0-r6, r12, lr}
        vmov.f32 s0, #-1.0
        bx lr
    '''%POINTER
    # Thumb CBNZ only branches forwards; use CMP/BNE for the backwards loop.
    assembly=assembly.replace('cbnz r4, compare_loop','cmp r4, #0\n bne compare_loop')
    code=vwf.assemble(assembly,address)
    require(address+len(code)<=POINTER,'UI hook does not fit verified VWF reservation')
    return code


def description_stub(address,lookup):
    """Translate r2 before native MtV line counting/splitting; keep r2 intact."""
    code=vwf.assemble('''
        push {r7, lr}
        vpush {s0-s1}
        mov r7, r2
        cmp r7, #0
        beq unchanged
        bl %d
    unchanged:
        mov r0, r7
        vpop {s0-s1}
        pop.w {r7, lr}
        adds r0, r0, #0
        str r1, [sp, #0x18]
        bx lr
    '''%lookup,address)
    require(address+len(code)<=POINTER,'Description hook exceeds verified reservation')
    return code


def birthday_stub(address):
    # Same native drawer, inline slash, code-relative addressing. The native
    # month/day numerals and input/editing functions are untouched. Full-width
    # slash is the native-font presentation of the shared numeric format.
    code=vwf.assemble('adr.w r0, #%d; b.w %d'%(address+8,0x81007916),address)
    require(len(code)==8,'Unexpected birthday stub size')
    return code+'／'.encode('cp932')+b'\0\0'


def center_stub(address,lookup):
    """Measure fully translated single-line Latin before native /2 centering.

    At this site r0 is the live native font-state pointer, r6 is source text,
    r5 is encoding. Unknown, Japanese and semantic-cell text uses native pitch.
    """
    code=vwf.assemble('''
        push.w {r0-r4,r7,r12,lr}
        mrs r12,apsr
        push {r12}
        vpush {s0-s3}
        mov r7,r6
        bl %d
        mov r2,r7
        movs r4,#0
        adr r1,#%d
        ldr r3,[r1]
        add r1,r3
        adds r1,#4
    loop:
        ldrb r3,[r2],#1
        cbz r3,done
        cmp r3,#0x87
        bne fallback
        ldrb r3,[r2],#1
        subs r3,#64
        cmp r3,#192
        bhs fallback
        ldrb r3,[r1,r3]
        cmp r3,#32
        beq fallback
        add r4,r3
        b loop
    done:
        vmov s0,r4
        vcvt.f32.u32 s0,s0,#5
        vldr s1,[r0,#0x14]
        b measure
    fallback:
        vldr s0,[sp]
    measure:
        vmul.f32 s0,s0,s1
    finished:
        vstr s0,[sp]
        vpop {s0-s3}
        pop {r12}
        msr apsr_nzcvq,r12
        pop.w {r0-r4,r7,r12,pc}
    '''%(lookup,vwf.DELTA),address)
    require(address+len(code)<=POINTER,'Center hook exceeds verified reservation')
    return code


def patch(original,widths,rows,birthday=False,literal_edits=(),name_rows=None):
    candidate,base_audit=vwf.patch(original,widths)
    info=parse(candidate);p0,p1=info['phdrs'][:2]
    segs={i:candidate[s[0]:s[0]+s[1]] for i,s in enumerate(info['infos'])}
    start=vwf.TEXT_END+((base_audit['code_bytes']+3)&~3)
    code=stub(start);description_start=(start+len(code)+3)&~3
    description_code=description_stub(description_start,start)
    text=bytearray(segs[0])
    a,b=start-p0[2],POINTER-p0[2]+4
    require(not any(text[a:b]),'UI hook reservation occupied')
    old=vwf.assemble(ORIGINAL,SITE);new=vwf.assemble('bl %d'%start,SITE)
    require(len(old)==len(new)==4 and text[SITE-p0[2]:SITE-p0[2]+4]==old,'UI drawer instruction mismatch')
    text[SITE-p0[2]:SITE-p0[2]+4]=new;text[a:a+len(code)]=code
    description_old=vwf.assemble(DESCRIPTION_ORIGINAL,DESCRIPTION_SITE)
    description_new=vwf.assemble('bl %d'%description_start,DESCRIPTION_SITE)
    d=DESCRIPTION_SITE-p0[2]
    require(len(description_old)==len(description_new)==4 and text[d:d+4]==description_old,
            'UI description instruction mismatch')
    text[d:d+4]=description_new
    ds=description_start-p0[2];text[ds:ds+len(description_code)]=description_code
    birthday_edits=[];birthday_start=(description_start+len(description_code)+3)&~3
    if birthday:
        code_date=birthday_stub(birthday_start)
        require(birthday_start+len(code_date)<=POINTER,'Birthday stub exceeds verified reservation')
        for va,source in ((0x8125BF4C,'月'),(0x8125BF50,'日')):
            off=va-p0[2];key=source.encode('cp932')+b'\0'
            require(text[off:off+len(key)]==key,'Birthday source changed')
        for site,assembly in ((0x8106DA7E,'bl %d'%birthday_start),
                              (0x8106DAD6,'nop.w')):
            off=site-p0[2];expected=vwf.assemble('bl %d'%0x81007916,site)
            replacement=vwf.assemble(assembly,site)
            require(text[off:off+4]==expected and len(replacement)==4,'Birthday drawer changed')
            text[off:off+4]=replacement;birthday_edits.append((off,expected))
        off=birthday_start-p0[2];text[off:off+len(code_date)]=code_date
    center_start=(birthday_start+(len(code_date) if birthday else 0)+3)&~3
    center_code=center_stub(center_start,start)
    center_old=vwf.assemble(CENTER_ORIGINAL,CENTER_SITE)
    center_at=CENTER_SITE-p0[2]
    require(text[center_at:center_at+4]==center_old,'Native centering instruction changed')
    text[center_at:center_at+4]=vwf.assemble('bl %d'%center_start,CENTER_SITE)
    off=center_start-p0[2];text[off:off+len(center_code)]=center_code
    name_edits=[];name_audit={}
    if name_rows:
        require(text[0x81272AA8-p0[2]:0x81272AA8-p0[2]+3]=='・'.encode('cp932')+b'\0',
                'Native full-name separator changed')
        name_start=(center_start+len(center_code)+3)&~3
        name_code,name_wrapper=name_stub(name_start,start)
        off=name_start-p0[2];text[off:off+len(name_code)]=name_code
        for site in NAME_SITES:
            off=site-p0[2];expected=vwf.assemble('blx %d'%0x8121DC20,site)
            require(text[off:off+4]==expected,'Native name-table strcpy changed')
            text[off:off+4]=vwf.assemble('bl %d'%name_wrapper,site)
            name_edits.append((off,expected))
        name_audit=dict(stub_address=hex(name_start),wrapper_address=hex(name_wrapper),
                        entries=len(name_rows),sites=[hex(s) for s in NAME_SITES],
                        saved_name_buffers_untouched=True,field_capacity=41)
    for address,jp,payload in literal_edits:
        off=address-p0[2];key=jp.encode('cp932')
        require(len(payload)==len(key) and text[off:off+len(key)]==key,'Native literal slot changed')
        text[off:off+len(payload)]=payload
    target=(p1[2]+len(segs[1])+3)&~3
    struct.pack_into('<I',text,POINTER-p0[2],(target-POINTER)&0xFFFFFFFF)
    segs[1]+=bytes(target-p1[2]-len(segs[1]))+table(rows)
    reloc=struct.pack('<III',0x310,target-p1[2],POINTER-p0[2])
    if name_rows:
        names_target=(p1[2]+len(segs[1])+3)&~3
        segs[1]+=bytes(names_target-p1[2]-len(segs[1]))
        segs[1]+=table(name_rows)
        struct.pack_into('<I',text,NAMES_POINTER-p0[2],(names_target-NAMES_POINTER)&0xFFFFFFFF)
        reloc+=struct.pack('<III',0x310,names_target-p1[2],NAMES_POINTER-p0[2])
        name_audit['table_address']=hex(names_target)
    segs[0]=bytes(text)
    segs[3]+=reloc
    updated=copy.deepcopy(info);headers=[list(p) for p in info['phdrs']]
    headers[1][4]=headers[1][5]=len(segs[1]);headers[3][4]=len(segs[3])
    cursor=52+32*len(headers)
    for i in sorted(range(len(headers)),key=lambda n:headers[n][1]):
        align=max(16,headers[i][7]);cursor=(cursor+align-1)&-align
        headers[i][1]=cursor;cursor+=len(segs[i])
    updated['phdrs']=[tuple(p) for p in headers];updated['elen']=cursor
    result=make_fself(updated,segs)
    restored=bytearray(segs[0]);restored[SITE-p0[2]:SITE-p0[2]+4]=old;restored[a:b]=bytes(b-a)
    restored[d:d+4]=description_old
    restored[center_at:center_at+4]=center_old
    for address,jp,payload in literal_edits:
        off=address-p0[2];restored[off:off+len(payload)]=jp.encode('cp932')
    for off,expected in birthday_edits:restored[off:off+4]=expected
    for off,expected in name_edits:restored[off:off+4]=expected
    require(bytes(restored)==segment(candidate,info,0)[0],'UI changed unrelated code')
    require(segs[1].startswith(segment(candidate,info,1)[0]),'UI changed initialized data/BSS')
    require(segs[3][:-len(reloc)]==segment(candidate,info,3)[0],'UI changed old relocations')
    return result,dict(status='in_memory_hook_candidate',site=hex(SITE),stub_address=hex(start),
        stub_bytes=len(code),table_address=hex(target),table_bytes=len(table(rows)),entries=len(rows),
        description_site=hex(DESCRIPTION_SITE),description_stub_address=hex(description_start),
        description_stub_bytes=len(description_code),max_encoded_line_bytes=256,
        center_site=hex(CENTER_SITE),center_stub_address=hex(center_start),center_stub_bytes=len(center_code),
        movement_literal_slots=sum(address!=0x8126DB68 for address,jp,payload in literal_edits),
        chart_literal_slots=sum(address==0x8126DB68 for address,jp,payload in literal_edits),
        runtime_names=name_audit,
        original_code_data_preserved=True,relocation=reloc.hex(),sha256=digest(result),
        birthday_draw_only=birthday,birthday_stub_address=hex(birthday_start) if birthday else None,
        runtime_tested=False,layout_verified=False)


def native_sources(port):
    """Whole native strings: executable encodings plus header-bounded UI records."""
    eboot,info=load();regions=[]
    for i in (0,1):regions.append(segment(eboot,info,i)[0])
    cpk=port.cpk('DATA/AIDDATA/AIDDataPack.cpk');raw=cpk.read(next(e for e in cpk.files if e['id']==0))
    require(raw[:8]==b'ASSF\1\0\0\0','Unknown native UI resource')
    base,end,first,last=[struct.unpack_from('<I',raw,i)[0] for i in (0x20,0x24,0x48,0x4c)]
    require(0<base<end<=first<last<=len(raw) and (last-first)%32==0,'Invalid native UI sections')
    strings=set()
    for at in range(first,last,32):
        rel=struct.unpack_from('<I',raw,at)[0];require(rel<end-base,'UI string reference outside native pool')
        off=base+rel;stop=raw.find(b'\0',off,end);require(stop>=off,'Native UI string not terminated')
        strings.add(raw[off:stop])
    # Gameplay effect/help strings are loaded from this native data bank,
    # not from the executable's UTF-8 literals or the widget resource.
    import rpw
    gameplay=port.cpk('CommonData/MtData/rpw_data.cpk','work/lib/RPW_DATA.CPK')
    bank=gameplay.read(gameplay.files[0])
    chunk=next(c for c in rpw.chunks(bank) if c[0]=='j-string')
    strings.update(bank[chunk[2]:chunk[3]].split(b'\0'))
    # Mission conditions are Lua preset strings, not EBOOT or RPW literals.
    # Read only the native OPERATE_TBL string table, never dialogue/comment
    # matches, and leave the scripts and gameplay conditions unchanged.
    mission=set();squads=set()
    import squad_names
    for name in sorted(n for n in port.audit if n.startswith('DATA/STAGE/') and n.endswith('.cpk')):
        archive=port.cpk(name);entry=next((e for e in archive.files if e['id']==1),None)
        if entry is None:continue
        script=archive.read(entry).decode('cp932')
        # These names are literal Lua team-name fields, not executable or
        # ASSF strings. Inventory their actual values without editing scripts
        # or player saves; unrelated/custom names remain exact-match misses.
        squads.update(jp.encode('cp932') for jp in squad_names.names(script))
        table=re.search(r'OPERATE_TBL\s*=\s*\{.*?str_tbl\s*=\s*\{(.*?)\}',script,re.S)
        if not table:continue
        for match in re.finditer(r'^\s*"([^"\r\n]*)"\s*,',table.group(1),re.M):
            value=match.group(1)
            for text in (value,value.replace('\\n','\n').replace('ポ\\イント','ポイント')):
                mission.add(text.encode('cp932'))
    port.native_mission_sources=mission
    strings.update(mission)
    port.native_squad_names=squads
    strings.update(squads)
    # The next narration container uses 88-byte Vita records, not the
    # opening's 84-byte grid or a PS3 grid. Only expose verified whole rows.
    import post_narration
    strings.update(jp.encode('cp932') for jp in post_narration.sources(port))
    # Save dialogs split their native multiline literal before calling the
    # drawer. Discover complete lines only in proven shared dialog literals;
    # never accept arbitrary substrings from executable data.
    for row in port.catalog.document('localization/messages/issue_hook.json')['messages'].values():
        source=row.get('source','')
        if '\n' not in source:continue
        key=source.encode('cp932')
        if any(b'\0'+key+b'\0' in region for region in regions):
            strings.update(line.encode('cp932') for line in source.split('\n') if line)
    # Native terrain files have bounded 28-byte names. Do not copy the PS3
    # synthetic terrain aliases or change any tile/stat records.
    from category_port import SOURCE
    for path in sorted((SOURCE/'DATA/mapetc/attr').glob('*.zld')):
        terrain=port.read(path.relative_to(SOURCE).as_posix())
        width,height,count,flags,unit,base,size,grid=struct.unpack_from('<8I',terrain)
        require(base==32 and size==count*32 and grid==width*height and
                len(terrain)==base+size+grid,'Unknown native terrain record grid')
        for i in range(count):
            field=terrain[base+i*32+4:base+(i+1)*32]
            require(b'\0' in field,'Unterminated terrain name')
            strings.add(field.split(b'\0')[0])
    # The native date drawer formats a fixed era prefix with a date-table
    # entry. Match complete results, never the format string or a substring.
    prefix='新多元世紀０００１年'
    require(any((prefix+'%s\0').encode('cp932') in r for r in regions),
            'Native date composition template changed')
    for region in regions:
        for raw in region.split(b'\0'):
            try: suffix=raw.decode('cp932')
            except UnicodeError: continue
            if re.fullmatch(r'[ 　]*[０-９0-9]+月[ 　]*[０-９0-9]+日',suffix):
                strings.add((prefix+suffix).encode('cp932'))
    return eboot,info,regions,strings,len(range(first,last,32))


def converted_key(text,executable,info):
    """Mirror the original 0x81006d54 Unicode-to-font lookup tables.

    In particular its ASCII is two-byte font text, NOT raw ASCII CP932.
    Entries are copied in byte order, exactly as the native LDRB/STRB pair.
    """
    result=bytearray()
    for ch in text:
        value=ord(ch)
        require(0<value<=0xFFFF,'UI converter key outside native UCS2 range')
        if ch=='\n':result+=b'\n';continue
        address=(0x812D8AC0 if value<=0x7F else 0x812B8AC0)+value*2
        hits=[]
        for i,p in enumerate(info['phdrs']):
            if p[0]!=1:continue
            off,size,comp,crypt=info['infos'][i]
            if p[2]<=address and address+2<=p[2]+size:
                require((comp,crypt)==(1,2),'UI conversion table encrypted')
                hits.append(executable[off+address-p[2]:off+address-p[2]+2])
        require(len(hits)==1 and len(hits[0])==2 and b'\0' not in hits[0], 'Missing native font conversion')
        result+=hits[0]
    return bytes(result)


def prepare(port):
    executable,info,regions,native_widgets,widget_count=native_sources(port)
    candidates=defaultdict(list);skipped=Counter();details=[];widget_keys=set(native_widgets)
    for group in GROUPS:
        if group not in port.catalog.manifest['groups']:continue
        defs=port.catalog.document('localization/messages/'+group+'.json')['messages']
        for mid,row in defs.items():
            # Only the unambiguous library term/series display names. Pilot
            # short names can belong to different people and stay ID-scoped.
            if group=='glossary' and row.get('context',{}).get('kind') not in ('keyword','series'):continue
            if group=='ui.command_layout' and row.get('context',{}).get('role')!='SAVE_DIALOGS':continue
            source=row.get('source')
            if not source:skipped['no_source']+=1;continue
            try:
                key=source.encode('cp932');keys=set()
                if key in native_widgets or any(b'\0'+key+b'\0' in region for region in regions):keys.add(key)
                if any(b'\0'+source.encode('utf-8')+b'\0' in region for region in regions):
                    keys.add(converted_key(source,executable,info))
                    # Centering sees the original UTF-8 before the drawer's
                    # conversion. Register that exact key as well.
                    keys.add(source.encode('utf-8'))
                if key in native_widgets:widget_keys.update(keys)
                if not keys:skipped['not_located']+=1;continue
                en=port.text(port.catalog.text(mid))
                if mid=='issue_hook:r_ddbe581c5ea9183d':
                    import ui_layout
                    en=ui_layout.choice_text(port)[0]
                if any(0xE000<=ord(c)<=0xF8FF and c not in port.mapping for c in en):
                    skipped['platform_private_glyph']+=1;continue
                if has_format(source) or has_format(en,english=True) or '$' in source or '$' in en:
                    skipped['runtime_format_or_control']+=1;continue
                if '《' in source or '《' in en:skipped['keyword_link']+=1;continue
                # Keep canonical breaks, but never feed a line the native
                # MtV splitter would discard (0x101-byte buffer incl. NUL).
                value=encoded(en,port.mapping)
                if max(map(len,value.split(b'\n')))>256:
                    skipped['native_line_buffer_limit']+=1;continue
                for key in keys:candidates[key].append((value,mid))
                # Mission screens prefix the original condition with a list
                # number after looking it up. Restrict to proven condition
                # bodies, not arbitrary translated strings or partial keys.
                if source.endswith('。') and (source.encode('cp932') in getattr(port,'native_mission_sources',()) or group=='mission_conditions_hook' or
                        source in ('敵の全滅。','ジェニオンの撃墜。')):
                    for number,wide in enumerate('１２３',1):
                        candidates[(wide+'．'+source).encode('cp932')].append(
                            (encoded(str(number)+'. '+en,port.mapping),mid))
            except (ValueError,UnicodeError):skipped['unsupported_encoding']+=1
    rows={};groups=Counter()
    for key,choices in candidates.items():
        if len({v for v,mid in choices})!=1:
            # These are the shared PS3 widget captions, not the longer key-help
            # or episode headings. Prefer them ONLY for a proven native widget
            # key. Never silently choose a winner for other ambiguous strings.
            widget_choices=[(v,mid) for v,mid in choices if mid.startswith('ui_aiddata:')]
            # Resolve only the two reported caption conflicts, using existing
            # shared wording. A later widget layout pass fits each local row.
            preferred={'修理':'ui_eboot:r_80a0b2a84e05d81a',
                       '移動':'ui_hook:r_428c2116ac3071b1',
                       '能力':'ui_hook:r_04e815a8d425827d',
                       '回復：\n回復：':'ui.map_popup_layout:r_f9b35564aafcd2e7',
                       '精神コマンド':'ui_hook:r_7bea3023abbf8a94',
                       '援攻．':'ui.map_popup_layout:r_7cc540f65f4d3eec',
                       '援防．':'ui.map_popup_layout:r_e96afa13f4c5fa9c'}
            wanted=preferred.get(key.decode('cp932',errors='replace'))
            if not wanted:
                wanted=preferred.get(key.decode('utf-8',errors='replace'))
            if key in widget_keys and wanted:
                widget_choices=[(v,mid) for v,mid in choices if mid==wanted]
            if key in widget_keys and widget_choices and len({v for v,mid in widget_choices})==1:
                details.append(dict(status='widget_context_preferred',
                    messages=[mid for v,mid in choices],
                    selected=[mid for v,mid in widget_choices],source_sha256=digest(key)))
                choices=widget_choices
            else:
                skipped['conflicting_source']+=1
                details.append(dict(status='conflict',messages=[mid for v,mid in choices]));continue
        rows[key]=choices[0][0]
        groups[choices[0][1].split(':',1)[0]]+=1
        details.append(dict(status='included',messages=[mid for v,mid in choices],source_sha256=digest(key)))
    # These proven multiline widgets are split into complete lines by the
    # native widget drawer. Register aligned line pairs, never substrings.
    for source,mid in (('使用回数\n','ui.search_list_headers:r_0ea619af31c0a4bc'),
                       ('回復：\n回復：','ui.map_popup_layout:r_f9b35564aafcd2e7')):
        if mid.split(':')[0] not in port.catalog.manifest['groups']:continue
        require(source.encode('cp932') in native_widgets,'Split widget source missing')
        english=port.text(port.catalog.text(mid))
        require(len(source.split('\n'))==len(english.split('\n')),'Widget line count changed')
        for jp,en in zip(source.split('\n'),english.split('\n')):
            if jp:rows[jp.encode('cp932')]=encoded(en,port.mapping)
    import runtime_headings
    headings=runtime_headings.hooks(executable,info,port.catalog) if 'scenario_titles' in port.catalog.manifest['groups'] else {}
    for source,en in headings.items():
        key=source.encode('cp932');value=encoded(en,port.mapping)
        require(key not in rows or rows[key]==value,'Conflicting composed episode heading')
        rows[key]=value
    groups['native_composed_headings']=len(headings)
    birthday='ui_aiddata' in port.catalog.manifest['groups'] and \
        'ui_aiddata:birthday_format' in port.catalog.document('localization/messages/ui_aiddata.json')['messages']
    if birthday:
        require(port.catalog.text('ui_aiddata:birthday_format')=='{month}/{day}',
                'Birthday format needs a locale-specific native layout adapter')
    import ui_layout
    literals=ui_layout.executable_cells(executable,info,port) if 'scenario_titles' in port.catalog.manifest['groups'] else ()
    if 'ui.library_chart' in port.catalog.manifest['groups']:
        import library_chart
        chart_rows,chart_literals=library_chart.hooks(port,executable,info)
        require(all(k not in rows or rows[k]==v for k,v in chart_rows.items()),'Chart key conflicts with another translation')
        rows.update(chart_rows);groups['library_chart']=len(chart_rows)
        literals=tuple(literals)+tuple(chart_literals)
    import runtime_names_vita
    names=runtime_names_vita.rows(port) if 'ui.runtime_names' in port.catalog.manifest['groups'] else None
    if names:
        # Pilot Info formats the same default full name but does not use the
        # dialogue substitution table. Bind that complete display string too.
        for key,value in names.items():
            require(key not in rows or rows[key]==value,'Conflicting runtime display name')
            rows[key]=value
    if 'scenario_titles' in port.catalog.manifest['groups']:
        import ui_widget_bindings
        aliases=ui_widget_bindings.hooks(port,executable,info,regions)
        require(not set(aliases).intersection(rows),'Widget alias conflicts with translation key')
        rows.update(aliases);groups['scoped_widget_aliases']=len(aliases)
        import intermission_fixes
        extra=intermission_fixes.hooks(port,executable,info,regions)
        require(not set(extra).intersection(rows),'Intermission alias conflict')
        rows.update(extra);groups['intermission_aliases']=len(extra)
        import roster_library_fixes
        extra=roster_library_fixes.hooks(port,executable,info,regions)
        require(not set(extra).intersection(rows),'Roster/Library alias conflict')
        rows.update(extra);groups['roster_library_aliases']=len(extra)
        import parts_network_fixes
        extra=parts_network_fixes.hooks(port,executable,info,regions)
        require(all(k not in rows or rows[k]==v for k,v in extra.items()),'Parts/Network key conflict')
        rows.update(extra);groups['parts_network_aliases']=len(extra)
        import team_labels
        extra=team_labels.hooks(port,executable,info,regions)
        require(not set(extra).intersection(rows),'Team label alias conflict')
        rows.update(extra);groups['team_label_aliases']=len(extra)
        import phase_warning
        extra=phase_warning.hooks(port,executable,info)
        require(all(k not in rows or rows[k]==v for k,v in extra.items()),'Team warning key conflict')
        rows.update(extra);groups['remaining_team_warning']=len(extra)
        import menu_followup_text
        extra=menu_followup_text.hooks(port,executable,info)
        require(all(k not in rows or rows[k]==v for k,v in extra.items()),'Clear footer key conflict')
        rows.update(extra);groups['menu_followup']=len(extra)
    original,_=load();candidate,audit=patch(original,port.width_bank,rows,birthday=birthday,literal_edits=literals,name_rows=names)
    if 'date_cards' in port.catalog.manifest['groups']:
        import date_card_centering
        definitions=port.catalog.document('localization/messages/date_cards.json')['messages']
        for mid,row in definitions.items():
            en=port.text(port.catalog.text(mid))
            require(en and '\n' not in en and all(c in port.widths and port.widths[c]<32 for c in en),
                    'Date centering requires one-line measured Latin: '+mid)
            require(rows.get(row['source'].encode('cp932'))==encoded(en,port.mapping),
                    'Date centering translation missing: '+mid)
        candidate,centering=date_card_centering.apply(candidate,int(audit['stub_address'],16))
        centering['dates']=len(definitions)
        audit['date_card_centering']=centering
        audit['sha256']=digest(candidate)
    if names:
        import link_background
        candidate,links=link_background.apply(candidate)
        audit['link_background']=links
        audit['sha256']=digest(candidate)
    audit.update(native_widget_records=widget_count,native_preset_squad_names=len(getattr(port,'native_squad_names',())),
        skipped=dict(skipped),groups=dict(groups),bindings=details,
        warning='Exact full strings only; dynamic fragments, centering, widths and in-game paths remain unverified')
    return candidate,audit
