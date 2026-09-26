"""Screen-space budgets for the 18 post-prologue narration display hooks.

These are timed single-row draws, not multiline strings. Reflow within the
same page's existing rows; never add LF or overwrite stage record metadata.
The screenshots show a 225px left margin and 32px glyph quads at 1280x720.
"""
import localization as _l10n
import json
from pathlib import Path
import digraph as dg

KEYS = (
    '獣の血、水の交わり、風の行き先、火の文明、',
    'そして、太陽の輝き',
    '終天の静穏を、貴方達に……',
    'ＺＥＵＴＨの帰還直後に発生した時空震動は',
    '新たな世界を創り上げた。',
    '新世時空震動と呼ばれることとなった、この時空震動は',
    '位相の異なる二つの世界、ＵＣＷとＡＤＷ……',
    'そして幾つかの世界を一つに統合した。',
    'しかし、人類はそれに屈しはしなかった……。',
    '人類は、この大規模な時空災害を受け入れ、',
    '新たな世界には新たな秩序が生まれていった。',
    '地球連邦政府の下、地球と転移してきたコロニーは統一され、',
    'わずか数ヶ月で人々の暮らしは新世時空震動前と',
    '変わらぬ平穏さを取り戻していた。',
    '新世時空震動から３ヶ月……。',
    '新世界の混乱の陰に隠れていた陰謀と真実が',
    '動き始める時、時空を揺るがす戦いの序章が',
    '幕を開けようとしていた……。',
)


def rows():
    """Select the timed narration by identity, independent of other UI rows."""
    data = json.loads(Path('translation/issue_hook.json').read_text(encoding='utf-8'))['lines']
    selected = {key: [row for row in data if row['jp'] == key] for key in KEYS}
    assert all(len(value) == 1 for value in selected.values()), 'Missing/duplicate narration key'
    return [selected[key][0] for key in KEYS]

PAGES = (
    (0, 3, 780, _l10n.literal('narration_layout.PAGES/0')),
    (9, 14, 860, _l10n.literal('narration_layout.PAGES/1')),
    (14, 18, 760, _l10n.literal('narration_layout.PAGES/2')),
)


def check(hooks, mapping, widths):
    lines = [hooks[row['jp']] for row in rows()]
    measured = []
    for line in lines:
        assert '\n' not in line and '\r' not in line
        measured.append(sum(widths[dg.cell_index(mapping[c])] for c in line))
        assert measured[-1] <= 900, (line, measured[-1])
        assert 225+measured[-1] <= 1280-150
    for lo, hi, budget, prose in PAGES:
        assert ' '.join(lines[lo:hi]) == prose, 'Narration prose or page boundaries changed'
        assert max(measured[lo:hi]) <= budget
    print('PASS: all 18 narration lines fit native-screen margins; three reflowed pages preserve every word and row count.')
