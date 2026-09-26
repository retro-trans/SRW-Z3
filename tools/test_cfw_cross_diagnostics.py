"""Synthetic crossover isolation, transfer and path safety tests."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/ps3'))
import cfw_cross_diagnostics as x


class CrossDiagnosticTests(unittest.TestCase):
    def test_only_eboot_is_swapped_relative_to_each_parent(self):
        control = {x.d.EBOOT: 'japanese code', '/DATA/A': 'japanese', '/OTHER': 'same'}
        english = {x.d.EBOOT: 'english code', '/DATA/A': 'english', '/OTHER': 'same'}
        first, second = x.crossover_inventories(control, english)
        self.assertEqual(x.d.changed(control, first), [x.d.EBOOT])
        self.assertEqual(x.d.changed(english, second), [x.d.EBOOT])
        self.assertEqual(first['/DATA/A'], 'japanese')
        self.assertEqual(second['/DATA/A'], 'english')
        self.assertEqual(control[x.d.EBOOT], 'japanese code')
        self.assertEqual(english[x.d.EBOOT], 'english code')

    def test_mismatched_inventory_or_missing_axis_rejected(self):
        with self.assertRaises(ValueError):
            x.crossover_inventories({x.d.EBOOT: 'a'}, {})
        with self.assertRaises(ValueError):
            x.crossover_inventories({x.d.EBOOT: 'a'}, {x.d.EBOOT: 'b'})
        with self.assertRaises(ValueError):
            x.crossover_inventories({x.d.EBOOT: 'a', '/DATA': 'a'},
                                    {x.d.EBOOT: 'a', '/DATA': 'b'})

    def test_output_existing_and_outside_workspace_rejected(self):
        for p in (x.c.ROOT, x.c.ROOT / 'work', x.PRIOR, x.c.ROOT.parent / 'elsewhere'):
            with self.subTest(path=p), self.assertRaises(ValueError):
                x.output_path(p)

    def test_copy_member_exact_bounds_and_hash(self):
        import hashlib
        payload = b'Synthetic member'
        expected = dict(bytes=len(payload), sha256=hashlib.sha256(payload).hexdigest())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, target = root / 'source.iso', root / 'new/member.bin'
            source.write_bytes(bytes(2048) + payload + b'NOT PART OF MEMBER')
            before = x.c.digest(source)
            x.copy_member(source, dict(lba=1, size=len(payload)), target, expected)
            self.assertEqual(target.read_bytes(), payload)
            self.assertEqual(x.c.digest(source), before)
            with self.assertRaisesRegex(ValueError, 'size mismatch'):
                x.copy_member(source, dict(lba=1, size=1), target, expected)
            self.assertEqual(target.read_bytes(), payload)
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                x.copy_member(source, dict(lba=1, size=len(payload)), target,
                              dict(expected, sha256='wrong'))

    def test_truncated_member_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'truncated.iso'
            source.write_bytes(b'X')
            with self.assertRaisesRegex(ValueError, 'Unexpected source EOF'):
                x.copy_member(source, dict(lba=1, size=10), root / 'target',
                              dict(bytes=10, sha256='unused'))

    def test_two_small_isos_have_expected_crossover_contents(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            stage = root / 'stage'
            stage.mkdir()
            (stage / 'EBOOT.BIN').write_bytes(b'English executable fixture')
            (stage / 'DATA.BIN').write_bytes(b'Japanese data fixture')
            inventory = {'/EBOOT.BIN': x.d.info(stage / 'EBOOT.BIN'),
                         '/DATA.BIN': x.d.info(stage / 'DATA.BIN')}
            aliases = {n: n for n in inventory}
            first = x.d.write_image(root / '04.iso', stage, aliases, inventory)
            (stage / 'EBOOT.BIN').write_bytes(b'Japanese executable fixture')
            (stage / 'DATA.BIN').write_bytes(b'English data fixture')
            inventory = {n: x.d.info(stage / n.lstrip('/')) for n in inventory}
            second = x.d.write_image(root / '05.iso', stage, aliases, inventory)
            self.assertEqual(first['files_verified_each_tree'], 2)
            self.assertEqual(second['files_verified_each_tree'], 2)
            self.assertNotEqual(first['sha256'], second['sha256'])
            self.assertEqual(list(root.glob('*.iso.*')), [])


if __name__ == '__main__':
    unittest.main()
