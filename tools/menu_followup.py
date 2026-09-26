"""September 13 trader prompts, roster heading and live menu alignment.

Keep corrections scoped to records, including highlighted/alternate states.
No global change to Commander, Search, PS Store or the shared font.
"""
import localization as _l10n
import struct
import aiddata
import digraph as dg
from intermission_layout import text, ink

PROMPTS = {
    0xa24b4: ('売却するパーツを決定してください。', _l10n.literal('menu_followup.PROMPTS/0')),
    0xa24d4: ('売却数を決定してください。', _l10n.literal('menu_followup.PROMPTS/1')),
    0xa24f4: ('持ち越すパーツを決定してください。', _l10n.literal('menu_followup.PROMPTS/2')),
    0xa2514: ('持ち越し数を決定してください。', _l10n.literal('menu_followup.PROMPTS/3')),
}
COMMANDER = (0xafb74, 0xb4c74)
CHIPS = (0xa2cb4, 0xa2e94, 0xa3074, 0xa3994, 0xa3d34,
         0xa3f34, 0xa4134, 0xa4334, 0xa4534)
ROWS = dict(PROMPTS)
ROWS.update({r: ('指揮官', 'Cmdr') for r in COMMANDER})
for r in CHIPS:
    ROWS[r] = ('Ｚ', 'Z Chips.')
    ROWS[r+32] = ('チップ．', '')

# Measured ink and button centres in the supplied 2560x1369 capture.
# Active 1280-wide game image spans 2434 screen pixels (pillarboxes excluded).
SCREEN_SCALE = 2434 / 1280.
# jp, record pairs, normal-size correction in native pixels. Preserve the
# original 28/31px fonts, baseline, colours and selection modes.
BUTTONS = (
    ('パイロット一覧', (0xa31d4, 0xa31f4), (1140-1080.5)/SCREEN_SCALE),
    ('機体・武器改造', (0xa3294, 0xa32b4), (1677.5-1621.5)/SCREEN_SCALE),
    ('検索', (0xa33d4, 0xa33f4), (2207.5-2248)/SCREEN_SCALE*28/31),
    ('オプション', (0xa3414, 0xa3434), (2210-2180.5)/SCREEN_SCALE),
    ('ネットワーク', (0xa3714, 0xa3734, 0xa3c14, 0xa3c34),
     (2210-2167)/SCREEN_SCALE),
)


def apply(blob, mapping, widths, pristine):
    out = bytearray(blob)
    allowed = set()
    for r, (jp, en) in ROWS.items():
        assert text(pristine, r) == jp.encode('cp932'), (hex(r), jp)
        raw = dg.encode_mixed(en, mapping) + b'\0'
        p = (len(out)+3)&~3
        out += bytes(p-len(out))+raw
        struct.pack_into('>I', out, r, p-aiddata.STR_BASE)
        allowed.update(range(r,r+4))
        if r in PROMPTS:
            # These are ordinary centered prompts. English is pre-encoded,
            # so remove character-count centering and place actual ink.
            x = struct.unpack_from('>f', pristine, r+4)[0]
            struct.pack_into('>f', out, r+4, x-ink(en,mapping,widths,25)/1280.)
            out[r+23] &= ~0x40
            allowed.update(range(r+4,r+8)); allowed.add(r+23)
        if r in COMMANDER:
            x = struct.unpack_from('>f', pristine, r+4)[0]
            struct.pack_into('>f', out, r+4, x+(84-ink(en,mapping,widths,28))/1280.)
            allowed.update(range(r+4,r+8))
    for jp, records, delta in BUTTONS:
        for r in records:
            assert text(blob,r) == jp.encode('cp932'), hex(r)
            size = blob[r+19]
            assert size in (28,31)
            x = struct.unpack_from('>f', pristine,r+4)[0]
            assert blob[r+4:r+8] == pristine[r+4:r+8]
            struct.pack_into('>f',out,r+4,x+delta*size/28/640.)
            allowed.update(range(r+4,r+8))
    assert all(a==b or i in allowed for i,(a,b) in enumerate(zip(blob,out)))
    check(out,mapping,widths,pristine)
    return bytes(out)


def check(blob,mapping,widths,pristine=None):
    if pristine is None:
        from cpk import CPK
        c=CPK('work/orig/AIDDATAPACK.CPK'); pristine=c.read(c.files[0])
    for r,(_,en) in ROWS.items():
        assert text(blob,r) == dg.encode_mixed(en,mapping), (hex(r),en)
        if r in PROMPTS:
            w=ink(en,mapping,widths,25)
            assert w < 530 and not blob[r+23]&0x40
            expected=struct.unpack_from('>f',pristine,r+4)[0]-w/1280.
            assert abs(struct.unpack_from('>f',blob,r+4)[0]-expected)<1e-7
        if r in COMMANDER:
            w=ink(en,mapping,widths,28)
            assert w < 84
            x=struct.unpack_from('>f',blob,r+4)[0]*640+640
            assert 1100 < x and x+w < 1255
    for jp,records,delta in BUTTONS:
        for r in records:
            assert text(blob,r)==jp.encode('cp932')
            assert blob[r+8:r+32]==pristine[r+8:r+32]
            expected=struct.unpack_from('>f',pristine,r+4)[0]+delta*blob[r+19]/28/640.
            assert abs(struct.unpack_from('>f',blob,r+4)[0]-expected)<1e-7
    print('PASS: four trader prompts, two Cmdr headings, nine Z Chips footers and 12 intermission button states.')
