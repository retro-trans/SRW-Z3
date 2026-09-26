"""Complete UTF-8 fallback speaker DISPLAY table, not CP932 lookup keys.

All 1,155 slots have explicit canonical bindings. Shared source strings can
name different people (Ray/Rei, Mehna/Mina): translate per table slot, never
globally replace these strings or every pointer to them. Native strings remain
unchanged; immutable UTF-8 display text lives in the existing extension.
"""
from pathlib import Path
import hashlib
import json
import struct
import localization

PATH = Path(__file__).resolve().parents[1] / 'platforms/ps3/localization/battle_speaker_bindings.json'


def inventory():
    return json.loads(PATH.read_text(encoding='utf-8'))


def rows():
    for row in inventory()['bindings']:
        yield row['message_id'], int(row['source_va'], 16), tuple(int(p, 16) for p in row['refs'])


def check_source(blob):
    data = inventory()
    lo, hi = int(data['table_start'], 16), int(data['table_end'], 16)
    assert hashlib.sha256(blob[lo:hi]).hexdigest() == data['table_sha256'], 'Speaker table changed'
    covered = []
    cat = localization.english()
    for mid, va, refs in rows():
        raw = cat.definition(mid)['source'].encode('utf-8') + b'\0'
        assert blob[va - 0x10000:va - 0x10000 + len(raw)] == raw, mid
        for ref in refs:
            assert struct.unpack_from('>I', blob, ref)[0] == va, (mid, hex(ref))
        covered.extend(refs)
    assert sorted(covered) == list(range(lo, hi, 4)), 'Missing or duplicate speaker slot'


def encoded(mid):
    import eboot
    en = localization.message(mid)
    assert en and not any('\u3040' <= c <= '\u9fff' for c in en), mid
    return ''.join(chr(eboot.VWF_CP_BASE + ord(c)) if ' ' <= c <= '~' else c for c in en).encode('utf-8')


def patch(blob, cursor):
    import eboot
    # The main patcher verifies the live source table before legacy UTF-8
    # label edits. Check the pristine inventory independently here as well.
    check_source(Path('work/EBOOT_dec.elf').read_bytes())
    out = bytearray(blob)
    segs = eboot._segments(out)
    limit = eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE
    strings = {}
    for mid, _, refs in rows():
        raw = encoded(mid) + b'\0'
        if raw not in strings:
            assert cursor + len(raw) <= limit, 'Battle speaker text exceeds existing extension'
            out[cursor:cursor + len(raw)] = raw
            strings[raw] = eboot._va(segs, cursor)
            cursor = (cursor + len(raw) + 3) & ~3
        for ref in refs:
            struct.pack_into('>I', out, ref, strings[raw])
    check(out)
    return out, cursor


def check(blob):
    import eboot
    segs = eboot._segments(blob)
    count = 0
    for mid, _, refs in rows():
        for ref in refs:
            va = struct.unpack_from('>I', blob, ref)[0]
            off = eboot._off(segs, va)
            assert off is not None and eboot._cstr(blob, off) == encoded(mid), (mid, hex(ref))
            count += 1
    print('PASS: all %d UTF-8 battle fallback speaker slots use canonical English.' % count)
