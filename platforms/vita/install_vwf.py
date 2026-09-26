"""Update an existing clean Vita3K game from a verified VWF ZIP, with rollback.

No saves, firmware, licenses, caches or app registration are touched. Every
changed game file is backed up and verified before the first replacement.
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import uuid
import zipfile
from build_install_zip import hash_file,verify_zip,safe_name
from category_port import ROOT,require
from install_test import running
from verify_decryption import sfo


def target(game,name):
    safe_name(name)
    raw=game/name
    require(not any(p.is_symlink() for p in (raw,)+tuple(raw.parents)),
            'Linked target path is not allowed')
    resolved=raw.resolve()
    require(game in resolved.parents,'Target escapes installed game')
    require(resolved.is_file(),'Missing installed game file: '+name)
    return resolved


def preflight(game,build):
    game,build=game.resolve(),build.resolve()
    require(game.name=='PCSG00264' and game.parent.name=='app' and game.parent.parent.name=='ux0',
            'Expected existing Vita3K ux0/app/PCSG00264 directory')
    require((ROOT/'work/vita').resolve() in build.parents,'Build is outside work/vita')
    info=sfo((game/'sce_sys/param.sfo').read_bytes())
    require((info['TITLE_ID'],info['APP_VER'])==('PCSG00264','01.00'),'Wrong installed game/version')
    require(not (game/'sce_pfs').exists() and not (game/'sce_sys/package').exists(),
            'Encrypted install metadata present; use a clean Vita3K ZIP install')
    audit=json.loads((build/'BUILD_AUDIT.json').read_text(encoding='utf-8'))
    require(audit['title_id']=='PCSG00264' and audit['app_version']=='01.00' and
            audit['build'].startswith('vita-english-vwf-test-') and
            audit['no_license_or_key_in_package'] is True,'Not a verified VWF build')
    name=audit['zip']['name'];require(Path(name).name==name and name.endswith('.zip'),'Unsafe ZIP name')
    archive=(build/name).resolve();require(build in archive.parents,'ZIP escapes build')
    require(hash_file(archive)==(audit['zip']['bytes'],audit['zip']['sha256']),'ZIP hash mismatch')
    require(len(audit['files'])==589 and len({n.casefold() for n in audit['files']})==589,
            'Unexpected/case-colliding build inventory')
    verify_zip(archive,audit['files'])
    changes={}
    for name,info in sorted(audit['files'].items()):
        dest=target(game,name);size,sha=hash_file(dest)
        if (size,sha)!=(info['bytes'],info['sha256']):
            changes[name]=dict(before_bytes=size,before_sha256=sha,
                               after_bytes=info['bytes'],after_sha256=info['sha256'])
    return game,archive,audit,changes


def atomic_copy(stream,destination,expected):
    temporary=destination.with_name(destination.name+'.codex-'+uuid.uuid4().hex+'.tmp')
    try:
        with temporary.open('xb') as out:shutil.copyfileobj(stream,out,4*1024*1024)
        require(hash_file(temporary)==expected,'Staged replacement hash mismatch')
        os.replace(str(temporary),str(destination))
    finally:
        if temporary.exists():temporary.unlink()


def install(game,build,write=False):
    if write:require(not running(),'Exit Vita3K before installing')
    game,archive,audit,changes=preflight(game,build)
    print('Verified installed target:',game,flush=True)
    print('Changed files:',len(changes),'; unchanged:',589-len(changes),flush=True)
    if not write:
        print('DRY RUN: no files changed. Saves/firmware are outside this target.',flush=True)
        return
    require(not running(),'Vita3K started during preflight')
    backup=ROOT/'work/vita/backups'/('vwf-'+datetime.now().strftime('%Y%m%d_%H%M%S_')+uuid.uuid4().hex[:8])
    backup.mkdir(parents=True,exist_ok=False)
    journal=dict(schema=1,status='backing_up',game=str(game),build=audit['build'],
                 archive=str(archive),zip_sha256=audit['zip']['sha256'],files=changes,
                 saves_firmware_licenses_untouched=True)
    log=backup/'INSTALL_AUDIT.json'
    def record(status):
        journal['status']=status;log.write_text(json.dumps(journal,indent=2)+'\n',encoding='utf-8')
    record('backing_up')
    for name,row in changes.items():
        source=target(game,name);saved=backup/name;saved.parent.mkdir(parents=True,exist_ok=True)
        expected=(row['before_bytes'],row['before_sha256'])
        require(hash_file(source)==expected,'Installed file changed before backup')
        shutil.copy2(source,saved);require(hash_file(saved)==expected,'Backup verification failed')
    record('backups_verified');print('Verified backups:',backup,flush=True)
    attempted=[]
    try:
        with zipfile.ZipFile(str(archive)) as z:
            for name,row in changes.items():
                require(not running(),'Vita3K started during installation')
                dest=target(game,name)
                require(hash_file(dest)==(row['before_bytes'],row['before_sha256']),
                        'Installed file changed after backup')
                attempted.append(name)
                with z.open('PCSG00264/'+name) as stream:
                    atomic_copy(stream,dest,(row['after_bytes'],row['after_sha256']))
                print('Installed:',name,flush=True)
        for name,info in audit['files'].items():
            require(hash_file(target(game,name))==(info['bytes'],info['sha256']),
                    'Final installed inventory mismatch: '+name)
        record('installed_verified')
    except Exception:
        for name in reversed(attempted):
            row=changes[name]
            with (backup/name).open('rb') as stream:
                atomic_copy(stream,target(game,name),(row['before_bytes'],row['before_sha256']))
        record('rolled_back');raise
    print('INSTALLED AND VERIFIED:',audit['build'],flush=True)
    print('Recovery files:',backup,flush=True)
    return backup


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--game',type=Path,required=True)
    ap.add_argument('--build',type=Path,required=True)
    ap.add_argument('--write',action='store_true')
    a=ap.parse_args();install(a.game,a.build,a.write)
