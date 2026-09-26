"""Synchronize the corrected three-line Counterattack menu in a local candidate."""
import argparse
import json
from pathlib import Path
import eboot
from patch_focus_candidate import table
from patch_parts_candidate import patch

KEY='・反撃する\n・防御する\n・回避する'
OLD='・Counter\n・Defend\n・Evade'
NEW='・Counterattack\n・Defend\n・Evade'
OUT=Path('work/out_0.6.3')
BACKUP=Path('work/counterattack_EBOOT.before.bin')


def update(blob,mapping):
    rows=table(blob)
    flags,current=rows[KEY.encode('cp932')]
    assert not flags & 0xc0000000
    if current==eboot._encode_marked(NEW,mapping): return blob
    assert current==eboot._encode_marked(OLD,mapping), 'unexpected existing Counterattack menu'
    built,stats=patch(blob,mapping,{KEY:OLD},{KEY:NEW})
    after=table(built)
    assert set(after)==set(rows)
    for key,value in rows.items():
        if key!=KEY.encode('cp932'): assert after[key]==value, key
    assert after[KEY.encode('cp932')][1]==eboot._encode_marked(NEW,mapping)
    print('One complete-menu lookup updated:',stats,'; every other lookup and executable code preserved.')
    return built


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    mapping=json.loads((OUT/'pairs.json').read_text())
    old=(OUT/'EBOOT.BIN').read_bytes();built=update(old,mapping)
    if built==old: print('Counterattack menu already synchronized.');return
    if args.write:
        assert not BACKUP.exists(), 'backup already exists'
        BACKUP.write_bytes(old);(OUT/'EBOOT.BIN').write_bytes(built)
        print('Local candidate updated; no installation or deployment.')


if __name__=='__main__': main()
