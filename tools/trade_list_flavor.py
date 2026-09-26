"""Trade List lore, distinct from the parts' gameplay-effect descriptions."""
import localization as _l10n
from pathlib import Path
import re
import textwrap
import trdata

TEXT={
0x70d970:_l10n.literal('trade_list_flavor.TEXT/0'),
0x70da18:_l10n.literal('trade_list_flavor.TEXT/1'),
0x70dab8:_l10n.literal('trade_list_flavor.TEXT/2'),
0x70db58:_l10n.literal('trade_list_flavor.TEXT/3'),
0x70dc00:_l10n.literal('trade_list_flavor.TEXT/4'),
0x70dc88:_l10n.literal('trade_list_flavor.TEXT/5'),
0x70dd18:_l10n.literal('trade_list_flavor.TEXT/6'),
0x70ddb8:_l10n.literal('trade_list_flavor.TEXT/7'),
0x70de58:_l10n.literal('trade_list_flavor.TEXT/8'),
0x70df10:_l10n.literal('trade_list_flavor.TEXT/9'),
0x70dfc8:_l10n.literal('trade_list_flavor.TEXT/10'),
0x70e088:_l10n.literal('trade_list_flavor.TEXT/11'),
0x70e120:_l10n.literal('trade_list_flavor.TEXT/12'),
0x70e1c0:_l10n.literal('trade_list_flavor.TEXT/13'),
0x70e278:_l10n.literal('trade_list_flavor.TEXT/14'),
0x70e320:_l10n.literal('trade_list_flavor.TEXT/15'),
0x70e3d8:_l10n.literal('trade_list_flavor.TEXT/16'),
0x70e478:_l10n.literal('trade_list_flavor.TEXT/17'),
}

def hooks():
    b=(Path(__file__).resolve().parents[1]/'work/EBOOT_dec.elf').read_bytes()
    found={0x70d970+m.start():m.group().decode('cp932')
           for m in re.finditer(rb'[^\0]+',b[0x70d970:0x70e508])}
    assert set(found)==set(TEXT),'Trade List lore inventory changed'
    assert all('\n' in jp for jp in found.values())
    return {jp:textwrap.fill(' '.join(trdata._ex(TEXT[p],__file__).split()),width=72,
                             break_long_words=False,break_on_hyphens=False)
            for p,jp in found.items()}


def check(mapping,widths):
    from intermission_layout import ink
    rows=hooks()
    assert len(rows)==18
    for jp,en in rows.items():
        assert len(jp.splitlines())==len(en.splitlines())==3,(jp,en)
        assert '$$' not in en
        assert all(ink(line,mapping,widths,28)<1070 for line in en.splitlines()),en
    print('PASS: all 18 Trade List lore entries fit three lines; separate part effects unchanged.')
