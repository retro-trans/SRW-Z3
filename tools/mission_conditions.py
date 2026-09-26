"""Exact mission-family variants; English is manually reviewed by role."""

def displayed_variants(jp):
    """Keep source keys plus Lua-displayed CP932 keys.

    The source also has redundant escapes before multibyte lead bytes, not
    only doubled trail-0x5c bytes (e.g. ポ\\イント versus ソ\\ーラー).
    Newline escapes were already decoded by the operation-table reader.
    """
    import re
    variants = {jp, jp.replace('ヒビキＡ', 'ヒビキ')}
    variants |= {re.sub(rb'\\(.)', rb'\1', value.encode('cp932')).decode('cp932')
                 for value in variants}
    return variants


def additional_lines():
    """New translations are canonical catalog data, not another text fork."""
    import localization
    import trdata
    cat = localization.english()
    definitions = cat.document('localization/messages/mission_conditions_all.json')['messages']
    return [dict(jp=definition['source'],
                 en=trdata._ex(cat.text(mid), mid),
                 role=definition['context']['roles'][0])
            for mid, definition in definitions.items()]


def line_hooks(lines):
    """Checked mission fragments take priority over generic UI line pairing.

    Never silently choose one translation of a shared source fragment. This
    catches reflow which loses deadlines/names when the game draws each line.
    """
    result = {}
    for row in expand(lines):
        if '\n' not in row['jp']:
            continue
        jl, el = row['jp'].split('\n'), row['en'].split('\n')
        assert len(jl) == len(el), row
        for jp, en in zip(jl, el):
            jp, en = jp.strip('　 '), en.strip()
            if len(jp) < 6 or not en:
                continue
            assert jp not in result or result[jp] == en, ('Mission line conflict', jp, result.get(jp), en)
            result[jp] = en
    return result


def expand(lines):
    result = []
    for row in lines:
        assert row['role'] in {'victory', 'defeat', 'sr'}, row
        jp = row['jp']
        variants = displayed_variants(jp)
        for value in sorted(variants):
            for number, prefix in enumerate(('', '１．', '２．', '３．')):
                result.append(dict(row, jp=prefix + value,
                                   en=(str(number) + '. ' if number else '') + row['en']))
    return result
