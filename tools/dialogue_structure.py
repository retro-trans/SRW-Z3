"""Source-bound dialogue header checks, shared by catalogs and Lua patching.

Do not infer names from portrait IDs: they can intentionally differ from the
printed speaker. Only recognize an explicit source name followed by a quoted
speech/thought line. Narration, bare labels and intentionally anonymous source
records are outside this check.
"""

OPENERS = '（(「『'


def named_source(source):
    lines = (source or '').replace('\r\n', '\n').split('\n')
    return (len(lines) > 1 and bool(lines[0].strip())
            and not any(c in lines[0] for c in OPENERS)
            and lines[1].lstrip().startswith(tuple(OPENERS)))


def speaker_problem(source, translation):
    """Return an actionable error, or None. Accept raw or expanded glossary."""
    if not named_source(source):
        return None
    lines = (translation or '').replace('\r\n', '\n').split('\n')
    if not lines[0].strip():
        return 'explicit source speaker was replaced by a blank header'
    if any(c in lines[0] for c in OPENERS):
        return 'dialogue occupies the speaker header; restore name and newline'
    if len(lines) == 1:
        return 'missing newline between speaker header and dialogue'
    return None
