"""Verify terrain translations against the real per-map name records."""
from pathlib import Path
import command_layout as layout
import digraph as dg
import terrain_catalog

SOURCE = Path('E:/SRWZ3/PS3_GAME/USRDIR/DATA/MAPETC/ATTR/MAP_011.ZLD')
OFFSETS = {'舗装道路':0x44,'平地':0x64,'ビル':0x84,'工事区画':0x164}

def check(hooks,mapping,widths):
    inventory = terrain_catalog.inventory()
    display_key = lambda jp: terrain_catalog.key(jp) if jp in terrain_catalog.EXTRA else jp
    missing = {jp for jp in inventory['names'] if display_key(jp) not in hooks}
    assert not missing, ('Untranslated terrain names', sorted(missing))
    expected = dict(layout.TERRAIN, **layout.FOLLOWUP_TERRAIN, **terrain_catalog.EXTRA)
    assert set(expected) == set(inventory['names']), 'Terrain source inventory changed'
    for jp in inventory['names']:
        en = expected[jp]
        key = display_key(jp)
        assert hooks[key] == en, jp
        width = sum(widths[dg.cell_index(mapping[c])] for c in en)*28/32.
        assert width+24 <= 300, (jp,en,width)
        assert layout.count_coefficient(layout.dialog_index(key)) == len(key)/2.
    cliff=SOURCE.with_name('MAP_002.ZLD').read_bytes()
    assert cliff[0x84:0x87]=='崖'.encode('cp932')+b'\0'
    assert hooks['崖']=='Cliff'
    assert layout.count_coefficient(layout.dialog_index('崖'))==0.5
    source=SOURCE.read_bytes()
    for jp,en in layout.TERRAIN.items():
        raw=jp.encode('cp932')+b'\0';p=OFFSETS[jp]
        assert source[p:p+len(raw)]==raw,jp
        assert hooks[jp]==en
        # MAP-DATA's terrain slot is about 300px wide between the arrows.
        # Check conservatively at 28px quads (larger than the screenshot).
        width=sum(widths[dg.cell_index(mapping[c])] for c in en)*28/32.
        assert width+24<=300,(en,width)
        assert layout.count_coefficient(layout.dialog_index(jp))==len(jp)/2.
    print('PASS: %d terrain names across %d maps / %d records; coverage, width and centering verified.' %
          (len(inventory['names']),len(inventory['files']),len(inventory['records'])))
