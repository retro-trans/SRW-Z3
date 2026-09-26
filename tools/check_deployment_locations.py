"""Read-only checks for this UI batch; does not stamp or approve a full build."""
import argparse
import json
import struct
from pathlib import Path
from cpk import CPK
import digraph as dg
import eboot
import trdata
import deployment_layout
import map_locations
import check_command_layout
import scenario_title
import title_footer

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args=parser.parse_args();out=Path(args.out)
    trdata.use_glossary('analysis/glossary.json')
    font='E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF'
    dg.use_letters(font,cap=22,dilate=.5)
    mapping={(k if len(k)==1 else tuple(k)):v for k,v in json.loads((out/'pairs.json').read_text()).items()}
    blob=(out/'EBOOT.BIN').read_bytes();segs=eboot._segments(blob)
    pos=eboot._off(segs,eboot.TABLE_VA)
    widths=dict(enumerate(blob[pos:pos+eboot.ATLAS_CELLS]))
    ui=CPK(str(out/'AIDDATAPACK.CPK'))
    data=ui.read(next(f for f in ui.files if f['id']==0));del ui
    deployment_layout.check(data,mapping,widths)
    import save_prompt_layout
    save_prompt_layout.check(data,mapping)
    import trophy_labels
    trophy_labels.verify(trophy_labels.SOURCE.read_bytes(),(out/'TROPHY.TRP').read_bytes())
    check_command_layout.check(blob,mapping,data)
    for site,reg,va in eboot.KW_SITES:
        pos=eboot._off(segs,site)
        self_branch=0x48000001|((va-site)&0x03fffffc)
        assert struct.unpack_from('>I',blob,pos)[0]==self_branch
        pos=eboot._off(segs,va);stub=eboot.kw_stub(reg)
        assert blob[pos:pos+len(stub)]==stub
    print('PASS: all keyword call targets and emitted helpers match their reserved positions.')
    tpack=CPK(str(out/'TPACKPS3.CPK'))
    check_command_layout.check_blank_cells(tpack);del tpack
    original=CPK('work/orig/EFFPS3.CPK');built=CPK(str(out/'EFFPS3.CPK'))
    import berserk_banner
    map_locations.verify_archive(original,built,font,tuple(scenario_title.EFFECTS)+(title_footer.MEMBER,berserk_banner.MEMBER))
    old_banner=original.read(next(f for f in original.files if f['id']==berserk_banner.MEMBER))
    new_banner=built.read(next(f for f in built.files if f['id']==berserk_banner.MEMBER))
    berserk_banner.verify(old_banner,new_banner,font)
    print('PASS: deployment/map batch only. Full-build validation and in-game QA remain separate requirements.')

if __name__=='__main__':main()
