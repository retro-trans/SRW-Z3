"""Song/weapon labels and scoped battleship-deployment fragments.

Text lives in the canonical catalog. Runtime weapon labels use exact hooks;
split deployment counters use widget-local replacement, never a global hook.
No numeric widgets, selection state, positions or command logic are changed.
"""
from pathlib import Path
import struct
import aiddata
import digraph as dg
import localization
from intermission_layout import text, ink

GROUP = 'song_deployment_labels'


def rows():
    cat = localization.english()
    for mid, definition in cat.document('localization/messages/' + GROUP + '.json')['messages'].items():
        yield mid, definition, cat.text(mid)


def hooks():
    return {d['source']: en for _, d, en in rows() if d['context']['hook']}


def check_source(elf, ui):
    for mid, d, en in rows():
        raw = d['source'].encode('cp932')
        context = d['context']
        if 'eboot_offset' in context:
            off = int(context['eboot_offset'], 16)
            assert elf[off:off + len(raw) + 1] == raw + b'\0', mid
        for widget in context['widgets']:
            assert text(ui, int(widget, 16)) == raw, (mid, widget)


def apply(blob, mapping, widths, original):
    check_source(Path('work/EBOOT_dec.elf').read_bytes(), original)
    out = bytearray(blob)
    allowed = set()
    for mid, d, en in rows():
        for widget in d['context']['widgets']:
            r = int(widget, 16)
            assert text(blob, r) == d['source'].encode('cp932'), (mid, widget)
            p = (len(out) + 3) & ~3
            out += bytes(p - len(out)) + dg.encode_mixed(en, mapping, newline=b'\n') + b'\0'
            struct.pack_into('>I', out, r, p - aiddata.STR_BASE)
            allowed.update(range(r, r + 4))
    assert all(a == b or i in allowed for i, (a, b) in enumerate(zip(blob, out)))
    check_ui(out, mapping, widths)
    return bytes(out)


def check_ui(blob, mapping, widths):
    count = 0
    for mid, d, en in rows():
        # Runtime labels have no FSSA string widget of their own. They still
        # need sizing checks: the Song Soul substitution shares CQB's two-cell
        # slot, not the 280px help-text area used by the original broad check.
        if d['context']['hook']:
            for line in en.split('\n'):
                assert ink(line, mapping, widths, 28) < d['context']['width_limit'], mid
        for widget in d['context']['widgets']:
            r = int(widget, 16)
            assert text(blob, r) == dg.encode_mixed(en, mapping, newline=b'\n'), mid
            for line in en.split('\n'):
                assert ink(line, mapping, widths, blob[r + 19]) < d['context']['width_limit'], mid
            count += 1
    print('PASS: %d song/deployment widgets; all live numbers and widget geometry unchanged.' % count)


def check_hooks(entries, mapping):
    import eboot
    for jp, en in hooks().items():
        assert entries[jp.encode('cp932')] == (0, eboot._encode_marked(en, mapping)), jp
    print('PASS: %d exact song/weapon hooks.' % len(hooks()))
