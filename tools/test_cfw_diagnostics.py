"""Controlled-difference and full-image read-back checks, using tiny fixtures."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/ps3'))
import cfw_diagnostics as d


class DiagnosticTests(unittest.TestCase):
    def test_clean_headers_match_original_self(self):
        from test_cfw_package import PackagingTests
        original, clean = PackagingTests().self_fixture()
        d.verify_clean_headers(original, clean)

    def test_changed_clean_headers_rejected(self):
        from test_cfw_package import PackagingTests
        original, clean = PackagingTests().self_fixture()
        for offset in (24, 68):
            altered = bytearray(clean)
            altered[offset] ^= 1
            with self.assertRaises(ValueError):
                d.verify_clean_headers(original, altered)

    def test_isolation(self):
        original = {d.EBOOT: 'retail', '/DATA': 'japanese', '/OTHER': 'same'}
        control = dict(original, **{d.EBOOT: 'clean fake'})
        english = dict(control, **{d.EBOOT: 'patched fake', '/DATA': 'english'})
        self.assertEqual(d.verify_isolation(original, control, english,
                                           {d.EBOOT, '/DATA'}, english),
                         ['/DATA', d.EBOOT])

    def test_control_asset_change_rejected(self):
        original = {d.EBOOT: 'retail', '/DATA': 'japanese'}
        control = {d.EBOOT: 'fake', '/DATA': 'changed'}
        with self.assertRaisesRegex(ValueError, 'ONLY EBOOT'):
            d.verify_isolation(original, control, control, control, control)

    def test_english_change_outside_snapshot_rejected(self):
        original = {d.EBOOT: 'retail', '/DATA': 'japanese'}
        control = dict(original, **{d.EBOOT: 'fake'})
        english = {d.EBOOT: 'patched', '/DATA': 'unexpected'}
        with self.assertRaisesRegex(ValueError, 'outside snapshot'):
            d.verify_isolation(original, control, english, {d.EBOOT}, english)

    def test_previous_build_mismatch_rejected(self):
        original = {d.EBOOT: 'retail'}
        control = {d.EBOOT: 'fake'}
        english = {d.EBOOT: 'patched'}
        with self.assertRaisesRegex(ValueError, 'failing CFW-test1'):
            d.verify_isolation(original, control, english, {d.EBOOT}, control)

    def test_missing_file_rejected(self):
        with self.assertRaisesRegex(ValueError, 'inventory changed'):
            d.changed({'a': 1}, {})

    def test_unsplit_image_and_overwrite_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            stage = root / 'stage'
            stage.mkdir()
            (stage / 'Game.bin').write_bytes(b'original data')
            image = root / 'test.iso'
            expected = {'/Game.bin': d.info(stage / 'Game.bin')}
            report = d.write_image(image, stage, {'/Game.bin': '/GAME.BIN'}, expected)
            self.assertEqual(report['files_verified_each_tree'], 1)
            self.assertEqual(report['sha256'], d.c.digest(image))
            self.assertEqual(list(root.glob('*.iso.*')), [])
            with self.assertRaisesRegex(ValueError, 'existing ISO'):
                d.write_image(image, stage, {'/Game.bin': '/GAME.BIN'}, expected)

    def test_changed_stage_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'file').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError, 'Staged file changed'):
                d.write_image(root / 'bad.iso', root, {'/file': '/FILE'},
                              {'/file': {'bytes': 0, 'sha256': 'incorrect'}})


if __name__ == '__main__':
    unittest.main()
