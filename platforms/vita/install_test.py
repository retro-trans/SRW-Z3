"""Install the three-file Vita3K pilot overlay with backups. Dry-run by default."""
import argparse
import csv
from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BUILD = ROOT / 'work/vita/english_pilot_01_checked'
ALLOWED = frozenset(('DATA/STAGE/STG0001a.cpk', 'DATA/STAGE/STG0001b.cpk', 'DATA/tabata/TPACKVITA.cpk'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def running():
    result = subprocess.run(['tasklist.exe', '/FI', 'IMAGENAME eq Vita3K.exe', '/FO', 'CSV', '/NH'],
                            capture_output=True, text=True, check=True)
    return any(row and row[0].lower() == 'vita3k.exe' for row in csv.reader(io.StringIO(result.stdout)))


def preflight(game, build):
    game, build = game.resolve(), build.resolve()
    require(game.name == 'PCSG00264' and game.parent.name == 'app' and game.parent.parent.name == 'ux0',
            'Select the installed Vita3K ux0/app/PCSG00264 folder')
    require((ROOT / 'work/vita').resolve() in build.parents, 'Build must be in work/vita')
    audit = json.loads((build / 'BUILD_AUDIT.json').read_text())
    require(audit['title_id'] == 'PCSG00264' and audit['app_version'] == '01.00', 'Wrong build title/version')
    require(set(audit['files']) == ALLOWED, 'Unexpected build files; refusing install')
    from verify_decryption import sfo
    metadata = sfo((game / 'sce_sys/param.sfo').read_bytes())
    require(metadata['TITLE_ID'] == 'PCSG00264' and metadata['APP_VER'] == '01.00', 'Wrong installed title/version')
    changes = []
    for name, info in sorted(audit['files'].items()):
        source = (build / 'overlay/PCSG00264' / name).resolve()
        destination = (game / name).resolve()
        require(game in destination.parents and build in source.parents, 'File resolves outside selected folders')
        require(source.is_file() and destination.is_file(), 'Missing build/base file: ' + name)
        require(sha(source) == info['patched_sha256'], 'Build hash mismatch: ' + name)
        require(sha(destination) == info['original_sha256'], 'Base is modified or different: ' + name)
        changes.append((name, source, destination, info))
    return game, audit, changes


def install(game, build, write=False):
    game, audit, changes = preflight(game, build)
    print('Target:', game)
    for name, source, destination, info in changes:
        print('Verified original -> English pilot:', name)
    print('Only these three archives change; executable, license, firmware and saves stay untouched.')
    if not write:
        print('Dry-run: no files written. Close Vita3K before repeating with --write.')
        return None
    require(not running(), 'Close Vita3K normally before installing')
    backup = ROOT / 'work/vita/backups' / (datetime.now().strftime('%Y%m%d_%H%M%S_') + uuid.uuid4().hex[:8])
    backup.mkdir(parents=True, exist_ok=False)
    for name, source, destination, info in changes:
        saved = backup / name
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, saved)
        require(sha(saved) == info['original_sha256'], 'Backup verification failed')
    (backup / 'BACKUP.json').write_text(json.dumps({'game': str(game), 'build': audit['build'],
                                                  'files': audit['files']}, indent=2) + '\n')
    modified = []
    try:
        for name, source, destination, info in changes:
            require(not running(), 'Vita3K started during installation')
            require(sha(destination) == info['original_sha256'], 'Base changed during installation')
            modified.append((name, destination, info))
            shutil.copy2(source, destination)
            require(sha(destination) == info['patched_sha256'], 'Installed hash mismatch')
    except Exception:
        for name, destination, info in reversed(modified):
            shutil.copy2(backup / name, destination)
            require(sha(destination) == info['original_sha256'], 'Rollback failed; retain backup: ' + str(backup))
        raise
    print('Installed and verified. Original files backed up:', backup)
    return backup


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--game', type=Path, required=True)
    parser.add_argument('--build', type=Path, default=DEFAULT_BUILD)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    install(args.game, args.build, args.write)
