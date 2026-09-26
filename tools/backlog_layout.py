"""Keep backlog help text clear of the separately drawn R1 icons."""
import localization as _l10n
import digraph as dg

JP = '：台詞戻し（＋　　：高速）\n：台詞送り（＋　　：高速）'
EN = _l10n.literal('backlog_layout.EN/0')


def check(hooks, mapping, widths):
    assert hooks[JP] == EN
    def ink(text):
        return sum(widths[dg.cell_index(mapping[c])] for c in text)*28/32.
    # FSSA 0x9b954 uses 28px text. Icon left edge is approximately 214px
    # from the text origin in the supplied native-scale screenshot. Budget
    # <=208px leaves 6px clearance; the fullwidth leading colon advances 28.
    for jp, en in zip(JP.splitlines(), EN.splitlines()):
        assert hooks[jp] == en
        prefix = en[1:en.index('+')+1]
        assert 28+ink(prefix) <= 208
        # Removing the pre-parenthesis space and narrowing the plus saves
        # 17.5px. Two added spaces restore 15.75px of that after the icon.
        old_start = 28+ink(prefix.replace('(+',' ('))+28+56
        new_start = 28+ink(prefix+'  ')+56
        assert abs(old_start-new_start) <= 2
    print('PASS: both backlog plus signs clear the fixed R1 icons; Fast suffix stays within 2px of its original position.')
