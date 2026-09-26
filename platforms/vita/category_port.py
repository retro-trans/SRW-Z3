"""Verified broad Vita text adapters. Dry-run or review JSON only, never a package.

All wording is read from the shared locale catalog. Native source hashes,
record identities and format round trips are checked before planning edits.
PS3 data containers may be reused ONLY after complete source-byte equality;
PS3 executable addresses/instructions are never copied.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import runpy
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT/'tools'), str(ROOT/'work/vita/python_deps')]
import localization as L
import luarec
import trdata
import rpw
import zukan
import mtfl
import build_library
import srvc_blocks as S
import voice_lib as V
from cpk import CPK
from build_test import patch_script, verify_script, TPACK
from prepare_translation import match_records, identity
from prepare_vwf import font_plan, line_widths, validate_layout
from font_gxt import FontPage
from text_codec import encode, decode, CONTROL
from inspect_vwf import load as load_eboot
from self_decrypt import parse as parse_self

SOURCE = ROOT/'work/vita/decrypted_PCSG00264'
LIBRARIES = {'kw':'MtZkn_KW.cpk','pt':'MtZkn_Pt.cpk','rt':'MtZkn_Rt.cpk'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, why):
    if not ok: raise ValueError(why)


def wrap(text, widths, limit=960):
    """Reflow at spaces, never shorten text or break a keyword-link span."""
    out=[]
    for paragraph in text.replace('\r\n','\n').split('\n'):
        tokens=[]; token=''; depth=0
        for ch in paragraph:
            if ch=='《': depth+=1
            if ch=='》': depth-=1
            require(0<=depth<=1,'Malformed keyword-link span')
            if ch==' ' and depth==0:
                if token: tokens.append(token);token=''
            else: token+=ch
        if token: tokens.append(token)
        require(depth==0,'Unclosed keyword link')
        line=''
        for token in tokens:
            require(max(line_widths(token,widths))<=limit,'Unbreakable token exceeds panel')
            candidate=line+' '+token if line else token
            if max(line_widths(candidate,widths))>limit:
                out.append(line);line=token
            else:line=candidate
        out.append(line)
    result='\n'.join(out)
    require(''.join(text.split())==''.join(result.split()),'Reflow changed wording')
    return result


def encoded(text,mapping,newline=b'\n'):
    payload,_=encode(text,mapping)
    require(decode(payload,mapping)==text.replace('\r\n','\n'),'Encoding round trip')
    return payload.replace(b'\r\n',newline)


def dialogue(text,widths):
    # The native two-byte parser cannot consume CP932 half-width quotes.
    # This is a presentation alias only, not a change to shared wording.
    text=text.replace('\uff62','「').replace('\uff63','」')
    result=wrap(text,widths)
    if len(result.split('\n'))>4:
        # Keep the speaker line separate. Existing dialogue soft line breaks
        # may be reflowed, but blank paragraphs and keyword boundaries survive.
        lines=text.replace('\r\n','\n').split('\n')
        if len(lines)>1 and all(line.strip() for line in lines[1:]):
            result=lines[0]+'\n'+wrap(' '.join(line.strip() for line in lines[1:]),widths)
    return result


def verify_rpw(original,patched,swap,overrides):
    """Follow original proven columns, never infer a new layout from English."""
    old={c[0]:c for c in rpw.chunks(original)}
    new={c[0]:c for c in rpw.chunks(patched)}
    require(old.keys()==new.keys(),'RPW chunk inventory changed')
    starts,_=rpw._starts(original)
    index_at={v:i for i,v in enumerate(starts)}
    oc,nc=old['j-string'],new['j-string']
    before=original[oc[2]:oc[3]].split(b'\0')
    body=patched[nc[2]:nc[3]]
    after=body.split(b'\0')
    for i,raw in enumerate(before):
        if i==len(before)-1 and raw==b'':
            # split()'s trailing sentinel is the append position, not an
            # original string record. The preceding NUL must remain intact.
            require(body[len(original[oc[2]:oc[3]])-1]==0,'RPW original terminator changed')
            continue
        value=swap.get(i,raw);slack=len(raw)-len(value)
        expected=value+rpw.FILL*(slack//2) if slack>=0 and slack%2==0 else raw
        require(after[i]==expected,'RPW original ordinal changed unexpectedly: '+str(i))
    columns=rpw.pointer_columns(original)
    checked=0
    for name,(_,_,co,cf,_) in old.items():
        if name=='j-string':continue
        no,nf=new[name][2:4]
        require(cf-co==nf-no,'RPW binary chunk grew')
        stride,phis=columns.get(name,(None,()))
        for pos in range(0,cf-co,4):
            previous=original[co+pos:co+pos+4]
            current=patched[no+pos:no+pos+4]
            key=(name,(pos//4)//stride,(pos//4)%stride) if stride else None
            value=int.from_bytes(previous,'little')
            if key is None or key[2] not in phis or (value not in index_at and key not in overrides):
                require(previous==current,'RPW non-pointer word changed');continue
            target=int.from_bytes(current,'little')
            require(target<len(body) and (target==0 or body[target-1]==0),'RPW pointer is not a string start')
            end=body.find(b'\0',target)
            require(end>=0,'RPW target unterminated')
            # Offset zero is also NULL. build_grown deliberately never moves
            # these semantic zeros, even when string ordinal zero was appended.
            if value==0 and key not in overrides:
                require(target==0,'RPW semantic NULL repointed');continue
            want=overrides.get(key,swap.get(index_at[value],before[index_at[value]]))
            got=body[target:end];slack=len(got)-len(want)
            require(slack>=0 and slack%2==0 and got==want+rpw.FILL*(slack//2),
                    'RPW pointer target mismatch: '+str(key))
            checked+=1
    return checked


def replace_voice_table(executable,location,old_table,new_table):
    """Native segment-relative LE table edit; safe after VWF SELF repacking."""
    require(len(old_table)==len(new_table)==S.NBLOCKS+1,'Voice table length mismatch')
    require(all(a<b for a,b in zip(new_table,new_table[1:])),'Voice block offsets not ascending')
    info=parse_self(executable)
    segment=location['segment'];relative=location['relative_offset']
    require(0<=segment<len(info['infos']),'Voice segment missing')
    off,size,comp,crypt=info['infos'][segment]
    require((comp,crypt)==(1,2),'Voice segment not plain')
    packed=struct.pack('<%dI'%len(old_table),*old_table)
    require(0<=relative and relative+len(packed)<=size,'Voice table outside segment')
    at=off+relative
    require(executable[at:at+len(packed)]==packed,'Native voice table source changed')
    replacement=struct.pack('<%dI'%len(new_table),*new_table)
    return executable[:at]+replacement+executable[at+len(packed):]


def patch_subset(original,translations,mapping,widths):
    """Strict subset adapter: untranslated strings and every command stay raw."""
    source=original.decode('cp932');records=luarec.records(source)
    wanted={identity(row):row for row in translations}
    require(len(wanted)==len(translations)>0,'Duplicate/empty subset')
    keys=[identity(row) for row in records]
    require(len(keys)==len(set(keys)) and set(wanted)<=set(keys),'Subset source identities differ')
    edits=[]
    for match,row,key in zip(luarec.BLOCK.finditer(source),records,keys):
        if key not in wanted:continue
        text=dialogue(wanted[key]['en'],widths)
        require(text.strip() and ']]' not in text and '$$' not in text,'Invalid subset English')
        require(Counter(CONTROL.findall(text))==Counter(CONTROL.findall(row['jp'])),'Subset control mismatch')
        require(text.count('《')==text.count('》')==row['jp'].count('《'),'Subset keyword mismatch')
        data=encoded(text,mapping,b'\r\n');validate_layout(text,data,widths)
        require(b']]' not in data,'Subset encoded delimiter')
        start=len(source[:match.start(1)].encode('cp932'))
        end=len(source[:match.end(1)].encode('cp932'))
        edits.append((start,end,data))
    out=bytearray();cursor=0
    for start,end,data in edits:out+=original[cursor:start]+data;cursor=end
    out+=original[cursor:];result=bytes(out)
    # Inverse each edited region without parsing VWF bytes as CP932.
    restored=bytearray();cursor=0;delta=0
    for start,end,data in edits:
        at=start+delta
        require(result[at:at+len(data)]==data,'Subset readback differs')
        restored+=result[cursor:at]+original[start:end]
        cursor=at+len(data);delta+=len(data)-(end-start)
    restored+=result[cursor:]
    require(bytes(restored)==original,'Subset altered unrelated bytes')
    return result,len(records),len(edits)


class Port:
    def __init__(self, sink=None):
        # Optional build consumer receives only checked native replacements.
        # The category CLI supplies no sink and remains report-only.
        self.sink=sink
        self.voice_tables=None
        self.catalog=L.Catalog()
        _,issues=self.catalog.validate();require(not issues,'Invalid shared English')
        self.audit=L.read_json(ROOT/'work/vita/decryption_audit.json')['files']
        self.checked={}
        self.glossary=self.catalog.legacy('analysis/glossary.json')
        trdata.use_glossary(str(ROOT/'analysis/glossary.json'))
        font=self.cpk(TPACK)
        pages={i:FontPage(font.read(next(e for e in font.files if e['id']==i))) for i in (1,3)}
        self.mapping,self.coverage,self.width_bank,self.widths=font_plan(pages)
        # Shared one-cell semantic labels retain the native per-cell pitch and
        # highlighting. These are independently verified blank in BOTH Vita
        # pages; PS3 texture bytes are never copied.
        import digraph
        from font_gxt import unused_codes,index_for_code
        blank=set(unused_codes(list(pages.values())))
        for ch,(label,code) in digraph.TINY_CELLS.items():
            if ord(ch)>=0xE01E:continue  # PS3-only positional tab controls
            require(code in blank and code not in self.mapping.values(),'Vita tiny cell is occupied')
            self.mapping[ch]=code
            self.coverage[index_for_code(code)]=bytes(digraph.raster_tiny(label,code))
            self.widths[ch]=32

    def read(self,relative):
        path=L.safe_path(SOURCE,relative)
        data=path.read_bytes()
        require(relative in self.audit,'Source absent from decryption audit: '+relative)
        require(digest(data)==self.audit[relative]['sha256'],'Source changed: '+relative)
        self.checked[relative]=digest(data)
        return data

    def cpk(self,relative,ps3=None):
        data=self.read(relative)
        if ps3:
            require(data==(ROOT/ps3).read_bytes(),'Common container differs; new parser mapping required: '+relative)
        return CPK(str(SOURCE/relative))

    def english(self,group):
        return self.catalog.legacy('translation/'+group+'.json')

    def text(self,value):
        return trdata._ex(value,'Vita category port')

    def emit(self,relative,member,data):
        if self.sink is not None:self.sink(relative,member,data)

    def stages(self):
        configuration=runpy.run_path(str(ROOT/'platforms/ps3/manifest.py'))['STAGES']
        paths={p.name.casefold():p.relative_to(SOURCE).as_posix() for p in (SOURCE/'DATA/STAGE').glob('*.cpk')}
        report=[]
        for stage in configuration:
            candidate=Path(stage['cpk']).name.casefold()
            require(candidate in paths,'Vita stage archive missing: '+candidate)
            relative=paths[candidate];cpk=self.cpk(relative)
            for member in stage['members']:
                group=Path(member['trans']).stem
                raw=cpk.read(next(e for e in cpk.files if e['id']==member['id']))
                row=dict(group=group,archive=relative,member=member['id'],source_sha256=digest(raw),
                         status='blocked',issues=[])
                try:
                    records=match_records(trdata.shared_records(group),luarec.records(raw.decode('cp932')))
                    row['source_matched']=len(records)
                    rendered=[]
                    for index,record in enumerate(records):
                        copy=dict(record)
                        try:
                            copy['en']=dialogue(record['en'],self.widths)
                            payload,_=encode(copy['en'],self.mapping)
                            validate_layout(copy['en'],payload,self.widths)
                            require(Counter(CONTROL.findall(record['jp']))==Counter(CONTROL.findall(copy['en'])), 'Control mismatch')
                            rendered.append(copy)
                        except (ValueError,UnicodeError) as error:
                            row['issues'].append(dict(record=index,event=record['event'],ordinal=record['n'],reason=str(error)))
                    row['layout_passed']=len(rendered)
                    if not row['issues']:
                        patched,_=patch_script(raw,rendered,self.mapping,
                                              lambda text,payload:validate_layout(text,payload,self.widths))
                        verify_script(raw,patched,rendered,self.mapping)
                        self.emit(relative,member['id'],patched)
                        row.update(status='loose_member_verified',patched_sha256=digest(patched),non_dialogue_bytes_unchanged=True)
                except (ValueError,UnicodeError) as error:
                    row['issues'].append(dict(reason=str(error)))
                report.append(row)
        return dict(members=report,source_matched=sum(r.get('source_matched',0) for r in report),
                    layout_passed=sum(r.get('layout_passed',0) for r in report),
                    verified_members=sum(r['status']=='loose_member_verified' for r in report),
                    pending='Any member with an issue is excluded as a whole; no partial or truncated dialogue.')

    def library(self):
        report=[]
        for family,name in LIBRARIES.items():
            relative='CommonData/MtData/'+name
            cpk=self.cpk(relative,'work/lib/MTZKN_'+family.upper()+'.CPK')
            entries={}
            for group in self.catalog.manifest['groups']:
                if group.startswith('library.'+family+'_'):
                    document=self.english(group.replace('.','/',1))
                    for key,value in document.get('ENTRIES',{}).items():
                        require(int(key) not in entries,'Duplicate library entry')
                        entries[int(key)]={tag:self.text(text) for tag,text in value.items()}
            count=Counter();problems=[]
            for entry,magic,fields,outputs in build_library._rendered(str(SOURCE/relative),self.glossary,entries,
                                            wrap_text=lambda text:wrap(text,self.widths,960)):
                original=cpk.read(next(e for e in cpk.files if e['id']==entry['id']))
                require(zukan.build(magic,fields)==original,'Library source round trip failed')
                new=[]
                for index,(tag,payload) in enumerate(fields):
                    if index not in outputs:new.append((tag,payload));continue
                    try:
                        data=encoded(outputs[index],self.mapping)
                        new.append((tag,data));count[tag]+=1
                    except (ValueError,UnicodeError) as error:
                        problems.append(dict(member=entry['id'],field=tag,reason=str(error)))
                        new.append((tag,payload))
                changed=zukan.build(magic,new)
                require(zukan.parse_ordered(changed)==(magic,new),'Library output round trip failed')
                require(all(new[i]==f for i,f in enumerate(fields) if i not in outputs),'Non-text library field changed')
                if not problems:self.emit(relative,entry['id'],changed)
            report.append(dict(family=family,archive=relative,entries=len(cpk.files),fields=dict(count),issues=problems,
                               source_equals_ps3=True,status='loose_members_verified' if not problems else 'blocked'))
        return report

    def suspend(self):
        relative='DATA/STAGE/STG0700.cpk';cpk=self.cpk(relative)
        raw=cpk.read(next(e for e in cpk.files if e['id']==1))
        translations=trdata.shared_records('suspend_scene')+trdata.shared_records('suspend_scene_dancouga')
        patched,total,count=patch_subset(raw,translations,self.mapping,self.widths)
        self.emit(relative,1,patched)
        return dict(status='partial_member_verified',archive=relative,member=1,
                    source_records=total,translated=count,remaining=total-count,
                    unrelated_bytes_unchanged=True,source_sha256=digest(raw),patched_sha256=digest(patched))

    def gameplay_terms(self):
        relative='CommonData/MtData/rpw_data.cpk'
        cpk=self.cpk(relative,'work/lib/RPW_DATA.CPK');raw=cpk.read(cpk.files[0])
        names={}
        for group in ('enemy_names','name_pieces','spirits','skills','parts','weapons'):
            names.update({k:self.text(v) for k,v in self.english(group).items() if not k.startswith('_') and v})
        names.update({t['jp']:t['en'] for t in self.glossary['terms'] if t['en']})
        js=rpw.jstrings(raw)
        plan=rpw.plan_all(js,names)
        forbidden={i for (chunk,rec,col),i in rpw.slots(raw).items() if chunk=='boost-p' and 3<=col<=8}
        require(not forbidden.intersection(plan),'Unsafe RPW part-description rewrite')
        swap={i:encoded(en,self.mapping) for i,en in plan.items()}
        overrides,unresolved=rpw.piece_overrides(raw,self.glossary['terms'])
        overrides.update(rpw.name_overrides(raw,self.glossary['terms']))
        overrides.update(rpw.spirit_name_overrides(raw,self.english('spirits')))
        over={k:encoded(v,self.mapping) for k,v in overrides.items()}
        new,appended=rpw.build_grown(raw,swap,over)
        checked=verify_rpw(raw,new,swap,over)
        self.emit(relative,cpk.files[0]['id'],new)
        return dict(archive=relative,source_equals_ps3=True,status='loose_member_verified',
                    translated_strings=len(swap),original_strings=len(js),overrides=len(over),
                    appended=appended,verified_pointer_targets=checked,
                    unresolved_name_records=unresolved,patched_sha256=digest(new),
                    protected='boost-p description columns 3..8 unchanged; no memory-unsafe description replacements')

    def keywords(self):
        relative='CommonData/MtData/MtV_all_keyword_def.cpk'
        cpk=self.cpk(relative,'work/lib/MTV_ALL_KEYWORD_DEF.CPK')
        require(len(cpk.files)==1,'Keyword member inventory changed')
        raw=cpk.read(cpk.files[0]);parsed=mtfl.parse(raw);source=mtfl.strings(raw,parsed)
        # Re-serialization may deduplicate equal strings; verify semantics
        # and IDs as well as the unindexed prefix/footer in the real parser.
        roundtrip=mtfl.build(raw,parsed,source)
        require(mtfl.strings(roundtrip,mtfl.parse(roundtrip))==source,'Keyword no-op round trip')
        entries={}
        for group in self.catalog.manifest['groups']:
            if group.startswith('library.kw_'):
                for key,row in self.english(group.replace('.','/',1))['ENTRIES'].items():
                    require(int(key) not in entries,'Duplicate keyword translation')
                    entries[int(key)]={k:self.text(v) for k,v in row.items()}
        names={k:self.text(v) for k,v in self.english('weapons').items() if not k.startswith('_') and v}
        names.update({t['jp']:t['en'] for t in self.glossary['terms'] if t['en']})
        texts={};count=Counter();untranslated=[]
        for eid,record in source.items():
            result={}
            for field,value in record.items():
                if field in ('WORD','SRCE'):
                    en=names.get(value.strip('「」'))
                    if en is not None and value.startswith('「'):en='「'+en+'」'
                else:
                    en=entries.get(eid,{}).get(field)
                    if not en and field=='DSC2' and value==record['DSCR']:
                        en=entries.get(eid,{}).get('DSCR')
                    if en:en=wrap(en,self.widths)
                if en is None:
                    result[field]=value.encode('cp932')
                    if value:untranslated.append(dict(entry=eid,field=field))
                else:result[field]=encoded(en,self.mapping);count[field]+=1
            texts[eid]=result
        new=mtfl.build(raw,parsed,texts);out=mtfl.parse(new);pay=new[0x20:]
        require(out['ids']==parsed['ids'],'Keyword ID order changed')
        for eid,window in zip(out['ids'],out['wins']):
            for field,fo,fl in mtfl.FIELDS:
                at=out['base']+window[fo]
                require(mtfl.xor(pay[at:at+window[fl]])==texts[eid][field],'Keyword field readback mismatch')
        self.emit(relative,cpk.files[0]['id'],new)
        return dict(status='loose_member_verified',archive=relative,source_equals_ps3=True,
                    entries=len(texts),fields=dict(count),untranslated=untranslated,
                    patched_sha256=digest(new),layout='Provisional 960-texel reflow; popup runtime pending')

    def voices(self):
        raw=self.read('DATA/BTLC/SRVC.BIN')
        require(raw==(ROOT/'work/srvc/SRVC.BIN').read_bytes(),'Voice banks differ')
        table=S.read_table((ROOT/'work/EBOOT_dec.elf').read_bytes())
        # Data offsets in byte-identical SRVC are transferable; executable
        # locations are NOT. Find the complete native LITTLE-endian array.
        eboot,info=load_eboot();packed=struct.pack('<%dI'%len(table),*table)
        hits=[]
        for i,(off,size,comp,crypt) in enumerate(info['infos']):
            if (comp,crypt)!=(1,2):continue
            body=eboot[off:off+size];at=body.find(packed)
            while at>=0:
                hits.append((i,at));at=body.find(packed,at+1)
        require(len(hits)==1,'Native SRVC table missing or ambiguous')
        rebuilt,unchanged,_=S.rebuild(raw,table,{})
        require(rebuilt==raw and unchanged==table,'SRVC no-op round trip failed')
        geometry=V.table();replacements={};total=0;problems=[]
        for group in self.catalog.manifest['groups']:
            if not group.startswith('voice_'):continue
            doc=self.english(group)
            index,count,pool,limit=V.geometry(doc,geometry)
            V.prove(raw,index,count,pool,limit,doc['section'])
            words=V.index_words(raw,index,count)
            for k,row in doc['lines'].items():
                n=int(k);require(0<=n<count,'Voice entry outside native bank')
                at=pool+words[n]
                require(S.string_at(raw,at).decode('cp932')==row['jp'],'Voice source mismatch')
                try:
                    text=self.text(row['en'])
                    data=b'\\n'.join(encoded(part,self.mapping) for part in ('「'+text+'」').split('\\n'))
                    require(at not in replacements or replacements[at]==data,'Shared voice slot has different English')
                    replacements[at]=data;total+=1
                except (ValueError,UnicodeError) as error:
                    problems.append(dict(group=group,entry=n,reason=str(error)))
        new,newtable,stats=S.rebuild(raw,table,replacements)
        require(not S.verify(new,newtable,raw,table,replacements),'Voice rebuild failed independent verification')
        segment,at=hits[0]
        location=dict(segment=segment,relative_offset=at,entries=len(table),endian='little')
        changed=replace_voice_table(eboot,location,table,newtable)
        require(replace_voice_table(changed,location,newtable,table)==eboot,'Voice executable table inverse failed')
        import vwf
        vwf_executable,_=vwf.patch(eboot,self.width_bank)
        combined=replace_voice_table(vwf_executable,location,table,newtable)
        require(replace_voice_table(combined,location,newtable,table)==vwf_executable,
                'Voice table edit changed repacked VWF code or metadata')
        if not problems:
            self.emit('DATA/BTLC/SRVC.BIN',None,new)
            self.voice_tables=(location,table,newtable)
        return dict(status='data_verified_layout_pending',records=total,distinct_strings=len(replacements),
                    blocks=len(stats),source_equals_ps3=True,issues=problems,
                    native_table=location,table_edit_inverse_verified=True,
                    repacked_vwf_table_inverse_verified=True,
                    old_size=len(raw),new_size=len(new),patched_sha256=digest(new),
                    new_table=newtable,
                    requirement='Rebuilt SRVC and native EBOOT table MUST ship together; battle wrapping/renderer still needs Vita testing')

    def ui_sources(self):
        eboot,info=load_eboot()
        matches=[];ambiguous=0;unlocated=0
        for group in self.catalog.manifest['groups']:
            if not (group.startswith('ui') or group.endswith('_hook')):continue
            defs=self.catalog.document('localization/messages/'+group+'.json')['messages']
            for mid,row in defs.items():
                source=row.get('source')
                if not source:continue
                hits=[]
                for encoding in ('cp932','utf-8'):
                    try: needle=b'\0'+source.encode(encoding)+b'\0'
                    except UnicodeError:continue
                    for segment,(offset,size,comp,crypt) in enumerate(info['infos']):
                        if (comp,crypt)!=(1,2):continue
                        body=eboot[offset:offset+size];pos=body.find(needle)
                        while pos>=0:
                            hits.append(dict(segment=segment,relative_offset=pos+1,encoding=encoding))
                            pos=body.find(needle,pos+1)
                if hits:matches.append(dict(message=mid,hits=hits))
                else:unlocated+=1
                ambiguous+=len(hits)>1
        return dict(status='source_candidates_only',matched_messages=len(matches),unlocated=unlocated,
                    ambiguous=ambiguous,matches=matches,
                    warning='String matches are NOT verified hooks. No blind replacement, UTF-8/font conversion or PS3 positions applied.')

    def ui_text(self):
        import ui_text
        _,audit=ui_text.prepare(self)
        return audit


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--categories',nargs='+',choices=['stages','suspend','library','keywords','gameplay_terms','voices','ui_sources','ui_text'],
                    default=['stages','suspend','library','keywords','gameplay_terms','voices','ui_sources','ui_text'])
    ap.add_argument('--report',type=Path)
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    if args.write:
        require(args.report is not None,'--write requires --report')
        target=args.report.resolve()
        require(ROOT/'work/vita' in target.parents and not target.exists(),'Report must be a NEW work/vita file')
    port=Port();report=dict(schema=1,title_id='PCSG00264',release_ready=False,runtime_tested=False,categories={})
    for category in args.categories:
        print('Checking',category,flush=True)
        try: result=getattr(port,category)()
        except (ValueError,AssertionError,UnicodeError,SystemExit) as error:
            result=dict(status='blocked',reason=str(error))
        report['categories'][category]=result
        if category=='stages' and 'members' in result:
            summary={k:v for k,v in result.items() if k!='members'}
        elif category=='ui_sources': summary={k:v for k,v in result.items() if k!='matches'}
        elif category=='voices':summary={k:v for k,v in result.items() if k!='new_table'}
        elif category=='ui_text':summary={k:v for k,v in result.items() if k!='bindings'}
        else:summary=result
        print(json.dumps(summary,ensure_ascii=True),flush=True)
    report['sources']=port.checked
    report['catalog_revision']=__import__('shared_content').revision()
    if args.write:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(L.dump(report),encoding='utf-8')
        print('Saved review audit only:',target)
    else:print('DRY RUN: no files written; no CPK/ZIP build or installation.')


if __name__=='__main__':main()
