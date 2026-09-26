"""Snapshot/dry-run/apply only the reward hooks and their centering wrapper."""
import argparse,json,struct
from pathlib import Path
import eboot,trdata,president_report_layout as layout
from patch_parts_candidate import patch

BASE = Path('work/gift_hooks_before.json')
REGIONS = Path('work/gift_center_before.json')
BACKUP = Path('work/gift_reports_EBOOT.before.bin')


def update(old,mapping,before,after,regions):
    data,stats=patch(old,mapping,before,after)
    out=bytearray(data);segs=eboot._segments(out)
    old_regions={int(va):bytes.fromhex(raw) for va,raw in regions}
    for va,raw in layout.regions(mapping):
        p=eboot._off(segs,va);prior=old_regions[va]
        assert out[p:p+len(prior)]==prior,hex(va)
        assert len(raw)>=len(prior)
        assert not any(out[p+len(prior):p+len(raw)]),'Occupied wrapper expansion'
        out[p:p+len(raw)]=raw
    assert len(out)==len(old)
    return bytes(out),stats


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--snapshot',action='store_true')
    ap.add_argument('--write',action='store_true')
    args=ap.parse_args()
    trdata.use_glossary('analysis/glossary.json')
    after=eboot.load_ui_hook()
    out=Path('work/out_0.6.3')
    mapping=json.loads((out/'pairs.json').read_text())
    if args.snapshot:
        assert not args.write and not BASE.exists() and not REGIONS.exists()
        BASE.write_text(json.dumps(after,ensure_ascii=False),encoding='utf-8')
        REGIONS.write_text(json.dumps([(va,b.hex()) for va,b in layout.regions(mapping)]),encoding='utf-8')
        print('Saved effective reward-hook and centering baselines.')
        return
    from gift_reports import hooks
    before=json.loads(BASE.read_text(encoding='utf-8'))
    assert not set(before)-set(after)
    assert {jp for jp in after if before.get(jp)!=after[jp]} <= set(hooks())
    old=(out/'EBOOT.BIN').read_bytes()
    data,stats=update(old,mapping,before,after,json.loads(REGIONS.read_text()))
    print('Reward delta: %d hook changes, %d removals, %d appended bytes, %d lookup rows.'%stats)
    print('Only lookup/text additions and scoped centered-drawer wrapper changed.')
    if args.write:
        assert not BACKUP.exists()
        BACKUP.write_bytes(old)
        (out/'EBOOT.BIN').write_bytes(data)


if __name__=='__main__':main()
