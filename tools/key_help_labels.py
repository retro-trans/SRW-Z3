"""Complete UTF-8 Key Help action-label family; unused actions stay dashes."""
import localization as _l10n
START = b'N10AnalImpact15AID_UIT_KeyHelpE'
END = b'N10AnalImpact20AID_UIT_SPTargetListE'
LABELS = dict(line.split('|',1) for line in _l10n.literal('key_help_labels.LABELS/0').strip().splitlines())

SLOT_HELP_JP='強化パーツ装備数のスロットです。パーツを装備すると点灯します。'
SLOT_HELP_EN=_l10n.literal('key_help_labels.SLOT_HELP_EN/1')
EXTRA={SLOT_HELP_JP:SLOT_HELP_EN}


def source_inventory(elf):
    a=elf.index(START)+len(START); z=elf.index(END,a)
    labels=[s.decode('utf8') for s in elf[a:z].split(b'\0') if s]
    assert len(labels)==92 and labels[0]=='－－－－－－－'
    assert set(labels[1:])==set(LABELS), 'Key Help source family changed'
    return labels
