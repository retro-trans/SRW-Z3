"""Inventory literal ally/enemy team names, not comments or player saves."""
import re


def names(text):
    # Lua is CP932; a trail byte 0x5c is escaped as 0x5c 0x5c. Unescape
    # at byte level BEFORE decoding, e.g. Takeo and Support contain it.
    raw=text.encode('cp932')
    pattern=rb'"((?:\\.|[^"\\\r\n])*)"\s*,\s*--[ \t]*'+re.escape('チーム名'.encode('cp932'))
    return sorted({re.sub(rb'\\(.)',rb'\1',m).decode('cp932')
                   for m in re.findall(pattern,raw) if m})
