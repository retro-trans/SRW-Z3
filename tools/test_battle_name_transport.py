"""Execute native caption producers, snapshot copy and new PPC transport.

Read-only original/.21 fixtures; no game build or installation performed.
"""
import json
import unittest
from pathlib import Path
import battle_name_transport as B
import battle_speaker_names as S
import digraph
import eboot
import rpw
import trdata
from cpk import CPK
from test_ps3_link_identity import CPU

ROOT = Path('work/build_0.6.21_english_20260925_r2')
BASE = 0x2300000
NAME = BASE + 0x5d54
SNAPSHOT = BASE + 0x9214
SOURCE = 0x2400001  # deliberately unaligned: native strcpy byte path
LINE = 0x2500001
STOP = 0x2600000


class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        trdata.use_glossary('analysis/glossary.json')
        cls.old = ROOT.joinpath('EBOOT.BIN').read_bytes()
        segs = eboot._segments(cls.old)
        # .21's final reported free tail is 5,792 bytes; do not allocate over
        # any existing table/string. Full current patch composition is also
        # exercised by test_activation_prompts.
        cls.cursor = eboot._off(segs, eboot.EXT_VA) + eboot.EXT_SIZE - 5792
        cls.new, cls.end = B.patch(cls.old, cls.cursor)
        cls.mapping = json.loads(ROOT.joinpath('pairs.json').read_text())

    def cpu(self, raw, patched=True):
        c = CPU(self.new if patched else self.old)
        c.put(BASE, b'\xcc' * 0x10000)
        c.put(SOURCE, raw + b'\0')
        c.put(LINE, b'New dialogue!\0')
        return c

    def produce(self, c, site=B.COPY_SITES[0]):
        c.r[3], c.r[4] = NAME, SOURCE
        c.run(site, {site + 4})
        self.assertEqual(c.r[3], NAME)  # strcpy ABI

    def dialogue(self, c):
        # Actual native dialogue formatter, including its final strcpy.
        # This single-line fixture has no newline delimiter to replace.
        c.calls[0x555004] = lambda _: 0
        c.r[3], c.r[4], c.lr = NAME + 31, LINE, STOP
        c.run(0x105a94, {STOP})

    def snapshot(self, c):
        c.r[28], c.r[26], c.r[27] = BASE, BASE + 0x4510, BASE + 0x4dc0
        c.run(0x11fef0, {0x120010})  # real unrolled 31-byte native copy
        self.assertEqual(c.read(SNAPSHOT, 31), c.read(NAME, 31))

    def resolve(self, c, field=NAME, flag=1):
        c.r[3], c.r[4], c.r[5] = 0x2700000, field, flag
        before = c.r[14:].copy(), c.f.copy(), c.r[1], c.r[2]
        c.run(B.DRAW_SITE, {B.DRAW})
        self.assertEqual((c.r[14:], c.f, c.r[1], c.r[2]), before)
        self.assertEqual((c.r[3], c.r[5], c.lr), (0x2700000, flag, B.DRAW_SITE + 4))
        return c.string(c.r[4])

    def test_reproduce_shipped_overflow_with_actual_native_code(self):
        raw = digraph.encode_mixed('Mariemaia Soldier', self.mapping)
        self.assertGreater(len(raw), 30)
        c = self.cpu(raw, False)
        self.produce(c)
        self.assertEqual(c.string(NAME), raw)
        self.assertNotEqual(c.read(NAME + 31, 4), b'\xcc' * 4)
        self.dialogue(c)
        self.assertNotEqual(c.string(NAME), raw)
        self.assertEqual(c.string(NAME)[:31], raw[:31])
        self.assertIn(b'New dialogue!', c.string(NAME))

    def test_all_producers_boundaries_snapshot_flags_and_canaries(self):
        for n in (0, 1, 14, 15, 29, 30, 31, 32, 128, 1024):
            raw = b'X' * n
            for site in B.COPY_SITES:
                with self.subTest(bytes=n, site=hex(site)):
                    c = self.cpu(raw)
                    self.produce(c, site)
                    self.assertTrue(c.writes <= set(range(NAME, NAME + 31)))
                    self.assertEqual(c.read(NAME - 4, 4), b'\xcc' * 4)
                    self.assertEqual(c.read(NAME + 31, 16), b'\xcc' * 16)
                    if n <= 30:self.assertEqual(c.string(NAME), raw)
                    self.dialogue(c)
                    self.snapshot(c)
                    for field in (NAME, SNAPSHOT):
                        for flag in (0, 1):
                            self.assertEqual(self.resolve(c, field, flag), raw)
                    # Reset only byte zero, exactly like native clear path.
                    c.put(NAME, b'\0')
                    self.assertEqual(self.resolve(c), b'')
                    self.assertEqual(self.resolve(c, SNAPSHOT), raw)

    def test_every_fallback_and_rpw_nickname(self):
        fixtures = [(mid, S.encoded(mid), 0) for mid, _, _ in S.rows()]
        k = CPK(str(ROOT / 'RPW_DATA.CPK'))
        raw = k.read(k.files[0])
        _, _, start, end, _ = next(ch for ch in rpw.chunks(raw) if ch[0] == 'j-string')
        strings = raw[start:end].split(b'\0')
        fixtures += [(str(slot), strings[i], 1) for slot, i in rpw.slots(raw).items()
                     if slot[0] == 'pilot-nw' and slot[2] == 0]
        long_count = 0
        for key, raw, flag in fixtures:
            with self.subTest(name=key):
                self.assertFalse(raw.startswith(B.MAGIC.to_bytes(4, 'big')))
                c = self.cpu(raw)
                self.produce(c)
                self.assertTrue(c.writes <= set(range(NAME, NAME + 31)))
                self.dialogue(c)
                self.assertEqual(self.resolve(c, flag=flag), raw)
                long_count += len(raw) > 30
        self.assertGreater(long_count, 20)
        print('Verified %d speaker bindings/nickname slots (%d long) through native producer and dialogue overwrite.' % (len(fixtures), long_count))

    def test_snapshot_keeps_earlier_speaker_when_live_caption_changes(self):
        first = S.encoded(next(mid for mid, _, _ in S.rows()
                              if S.localization.message(mid) == 'Mariemaia Soldier'))
        second = digraph.encode_mixed('Another Very Long Speaker Name', self.mapping)
        c = self.cpu(first)
        self.produce(c)
        self.snapshot(c)
        other = SOURCE + 0x1000
        c.put(other, second + b'\0')
        c.r[3], c.r[4] = NAME, other
        c.run(B.COPY_SITES[1], {B.COPY_SITES[1] + 4})
        self.assertEqual(self.resolve(c), second)
        self.assertEqual(self.resolve(c, SNAPSHOT), first)
        # Follow a long token with a short name in the same native field.
        c.put(other + 0x100, b'Jin\0')
        c.r[3], c.r[4] = NAME, other + 0x100
        c.run(B.COPY_SITES[2], {B.COPY_SITES[2] + 4})
        self.assertEqual(self.resolve(c), b'Jin')
        self.assertEqual(self.resolve(c, SNAPSHOT), first)

    def test_patch_scope_guards_and_no_translation_collision(self):
        allowed = {i for va in (*B.COPY_SITES, B.DRAW_SITE) for i in range(va - 0x10000, va - 0x10000 + 4)}
        allowed.update(range(self.cursor, self.end))
        self.assertEqual(len(self.old), len(self.new))
        self.assertTrue(all(a == b or i in allowed for i, (a, b) in enumerate(zip(self.old, self.new))))
        self.assertLess(self.end - self.cursor, 256)
        for va in (*B.COPY_SITES, B.DRAW_SITE):
            broken = bytearray(self.old)
            broken[va - 0x10000] ^= 1
            with self.assertRaises(AssertionError):B.patch(broken, self.cursor)
        with self.assertRaises(AssertionError):B.patch(self.new, self.cursor)
        broken = bytearray(self.old); broken[self.cursor] = 1
        with self.assertRaises(AssertionError):B.patch(broken, self.cursor)
        with self.assertRaises(AssertionError):B.check(self.old)
        for start, _, _ in B.NATIVE_REGIONS:
            broken = bytearray(self.new); broken[start - 0x10000] ^= 1
            with self.assertRaises(AssertionError):B.check(broken)
        self.assertEqual(eboot.load_ui_hook()['マリーメイア兵'], 'Mariemaia Soldiers')
        for mid, _, _ in S.rows():
            if S.localization.english().definition(mid)['source'] == 'マリーメイア兵':
                self.assertEqual(S.localization.message(mid), 'Mariemaia Soldier')


if __name__ == '__main__':
    unittest.main()
