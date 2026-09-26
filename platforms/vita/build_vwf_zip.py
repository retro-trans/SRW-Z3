"""Coherent broad English VWF Vita3K test ZIP; dry-run before --write.

New work/vita output only. No installation, source overwrite or license output.
Uses checked category adapters; rejects any failed member/category, not a
silent partial rebuild. Known untranslated categories remain documented.
"""
import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys

from category_port import Port, ROOT, SOURCE, digest, require, replace_voice_table
import localization
import shared_content
import cpkpatch
from cpk import CPK
from font_gxt import FontPage
from build_test import TPACK
import build_install_zip as package
import ui_text
import title_art
import startup_art
import menu_followup_art
import opening_narration
import ui_layout
import scene_art
import library_chart

NAME='SRW-Z3-Vita-English-VWF-test-16.zip'
DEFAULT=ROOT/'work/vita/english_vwf_test_16'
CATEGORIES=('stages','suspend','library','keywords','gameplay_terms','voices')


def check_report(value):
    if isinstance(value,dict):
        require(value.get('status')!='blocked','Blocked category/member')
        require(not value.get('issues'),'Category has unresolved build errors')
        for child in value.values():check_report(child)
    elif isinstance(value,list):
        for child in value:check_report(child)


class Replacements:
    def __init__(self):
        self.archives=defaultdict(dict)
        self.files={}

    def put(self,name,member,data):
        package.safe_name(name)
        require(isinstance(data,bytes),'Replacement must be immutable bytes')
        if member is None:
            require(name not in self.archives and name not in self.files,'Duplicate file replacement')
            self.files[name]=data
        else:
            require(isinstance(member,int) and member>=0,'Invalid member ID')
            require(name not in self.files and member not in self.archives[name],'Duplicate member replacement')
            self.archives[name][member]=data


def plan(license_path):
    localization.ensure_compatible()
    revision=shared_content.revision()
    replacements=Replacements();port=Port(replacements.put);categories={}
    for category in CATEGORIES:
        print('Preparing shared English:',category,flush=True)
        categories[category]=getattr(port,category)()
        check_report(categories[category])
    require(categories['stages']['verified_members']==len(categories['stages']['members']),
            'Not all configured story members verified')
    require(port.voice_tables is not None and 'DATA/BTLC/SRVC.BIN' in replacements.files,
            'Missing matched voice data/table pair')
    executable,ui=ui_text.prepare(port);categories['ui_text']=ui
    categories['ui_layout']=ui_layout.prepare(port)
    check_report(categories['ui_layout'])
    print('Preparing native Vita scene artwork',flush=True)
    categories['scene_art']=scene_art.prepare(port)
    check_report(categories['scene_art'])
    categories['library_chart']=library_chart.prepare(port)
    check_report(categories['library_chart'])
    categories['title_art']=title_art.prepare(port)
    check_report(categories['title_art'])
    categories['menu_followup_art']=menu_followup_art.prepare(port)
    categories['startup_art']=categories['menu_followup_art']['prior_startup_headings']
    check_report(categories['menu_followup_art'])
    check_report(categories['startup_art'])
    categories['opening_narration']=opening_narration.prepare(port)
    check_report(categories['opening_narration'])
    location,old,new=port.voice_tables
    combined=replace_voice_table(executable,location,old,new)
    require(replace_voice_table(combined,location,new,old)==executable,'Combined executable inverse failed')
    replacements.put('eboot.bin',None,combined)
    font=port.cpk(TPACK)
    for fid in (1,3):
        page=FontPage(font.read(next(e for e in font.files if e['id']==fid)))
        changed=page.replace(port.coverage);restored=bytearray(changed)
        for index in port.coverage:
            x,y=index%128*32,index//128*32
            for row in range(32):
                at=64+((y+row)*page.width+x)//2
                restored[at:at+16]=page.data[at:at+16]
        require(bytes(restored)==page.data,'Non-Latin font bytes changed')
        replacements.put(TPACK,fid,changed)
    # Reuse verified clean base/module conversion, never the old digraph pilot.
    sources,inventory,executables=package.prepare(license_path,include_pilot=False)
    require(digest(sources['eboot.bin'])==digest(ui_text.load()[0]),'Base EBOOT differs from hook source')
    require(shared_content.revision()==revision,'Shared catalog changed during preparation')
    report=dict(schema=1,build='vita-english-vwf-test-16',title_id='PCSG00264',app_version='01.00',
                shared_content=revision,categories=categories,source_hashes=port.checked,
                runtime_tested=False,full_english_port=False,latin_cells=95,semantic_cells=len(port.coverage)-95,
                executable_sha256=digest(combined),font_mapping=port.mapping,
                converted_modules=executables,
                limits=['Vita3K boot, rendering and later gameplay need testing',
                        'Centered labels and keyword highlight/hit boxes need live checks',
                        'Screenshot fixes, composed UI and scene art need live-game checks',
                        str(categories['suspend']['remaining'])+' suspend records and unresolved source terms remain Japanese',
                        'Physical Vita compatibility unverified'])
    print('PLAN:',len(replacements.archives),'CPKs;',len(replacements.files),
          'direct files;',report['categories']['stages']['source_matched'],'story records;',ui['entries'],'UI keys',flush=True)
    return replacements,sources,inventory,report


def verify_archive(source,destination,edits):
    old=CPK(str(source));new=CPK(str(destination))
    cpkpatch.validate_itoc(new.buf)
    require([e['id'] for e in old.files]==[e['id'] for e in new.files],'CPK member inventory changed')
    require(set(edits)<={e['id'] for e in old.files},'Unknown replacement member')
    for a,b in zip(old.files,new.files):
        if a['id'] in edits:require(new.read(b)==edits[a['id']],'CPK replacement readback differs')
        else:
            require((a['size'],a['extract'])==(b['size'],b['extract']) and
                    old.buf[a['offset']:a['offset']+a['size']]==new.buf[b['offset']:b['offset']+b['size']],
                    'Unchanged CPK member differs')
    return dict(bytes=len(new.buf),sha256=digest(new.buf),change='Shared English/VWF',
                members_verified=len(new.files),changed_members=sorted(edits))


def write(output,replacements,sources,inventory,report):
    output=package.check_output(output)
    require(shared_content.revision()==report['shared_content'],'Catalog changed before build')
    output.mkdir(parents=True,exist_ok=False)
    # No final ZIP until every changed archive has been read back.
    for number,(name,edits) in enumerate(sorted(replacements.archives.items()),1):
        target=output/'changed/PCSG00264'/name
        target.parent.mkdir(parents=True,exist_ok=True);paths={}
        for fid,data in edits.items():
            path=output/'members'/name/('%d.bin'%fid)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);paths[fid]=str(path)
        require(package.hash_file(SOURCE/name)[1]==report['source_hashes'][name],'CPK source changed before packing')
        cpkpatch.build(str(SOURCE/name),str(target),paths)
        inventory[name]=verify_archive(SOURCE/name,target,edits);sources[name]=target
        print('Verified CPK:',number,'/',len(replacements.archives),name,flush=True)
    for name,data in replacements.files.items():
        require(name in inventory,'Replacement outside base inventory')
        sources[name]=data;inventory[name]=dict(bytes=len(data),sha256=digest(data),change='VWF/UI executable or paired battle data')
    require(inventory['eboot.bin']['sha256']==report['executable_sha256'],'Wrong executable selected')
    require(inventory['DATA/BTLC/SRVC.BIN']['sha256']==report['categories']['voices']['patched_sha256'],'Wrong battle data selected')
    require(shared_content.revision()==report['shared_content'],'Catalog changed before ZIP')
    pending=output/(NAME+'.partial')
    package.write_zip(pending,sources,inventory)
    package.verify_zip(pending,inventory)
    size,sha=package.hash_file(pending)
    final=output/NAME
    require(not final.exists(),'Refusing existing package');pending.rename(final)
    report.update(zip=dict(name=NAME,bytes=size,sha256=sha),files=inventory,
                  verification='All CPK member bytes and all ZIP entry sizes/SHA256/CRC verified',
                  no_license_or_key_in_package=True)
    (output/'BUILD_AUDIT.json').write_text(json.dumps(report,ensure_ascii=True,indent=2)+'\n',encoding='utf-8')
    (output/(NAME+'.sha256')).write_text(sha+'  '+NAME+'\n',encoding='ascii')
    (output/'README-TEST.md').write_text((ROOT/'platforms/vita/VWF_TEST_ZIP.md').read_text(encoding='utf-8'),encoding='utf-8')
    print('VERIFIED TEST ZIP:',final,flush=True)
    print('Bytes:',size,'SHA256:',sha,flush=True)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--license',type=Path,default=Path('E:/SRWZ3/iso/work.bin'))
    ap.add_argument('--output',type=Path,default=DEFAULT)
    ap.add_argument('--write',action='store_true');args=ap.parse_args()
    output=package.check_output(args.output)
    replacements,sources,inventory,report=plan(args.license)
    if args.write:write(output,replacements,sources,inventory,report)
    else:print('DRY RUN PASSED: no files written; no installation.',flush=True)


if __name__=='__main__':main()
