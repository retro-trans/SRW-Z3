"""Check the screenshot-reported labels without altering effect mechanics."""
import localization as _l10n
from pathlib import Path
from intermission_layout import ink

LABELS={'運動性▼':_l10n.literal('weapon_effect_labels.LABELS/0'),'バリア貫通':_l10n.literal('weapon_effect_labels.LABELS/1')}
SOURCE_OFFSETS={'運動性▼':0x6d5580,'バリア貫通':0x711588}

def check(elf,hooks,mapping,widths):
    source=Path('work/EBOOT_dec.elf').read_bytes()
    for jp,en in LABELS.items():
        p=SOURCE_OFFSETS[jp];raw=jp.encode('cp932')+b'\0'
        assert source[p:p+len(raw)]==raw
        # Leave the Japanese table and neighboring stat/effect data intact.
        assert elf[p-1:p+len(raw)]==source[p-1:p+len(raw)]
        assert hooks[jp]==en
        assert ink(en,mapping,widths,31)<300,(en,ink(en,mapping,widths,31))
    print('PASS: Mobility Down and Barrier Pierce Effect labels fit; source effect tables unchanged.')
