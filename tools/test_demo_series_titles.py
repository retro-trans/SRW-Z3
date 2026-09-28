"""Source-only demo caption tests; no game build or installation."""
import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from cpk import CPK
import demo_series_titles as demo
import localization


class DemoSeriesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = demo.SOURCE
        if not source.exists():
            source = demo.ROOT/'game/PS3_GAME/USRDIR/DATA/BTLC/OP.CPK'
        if not source.exists():
            raise unittest.SkipTest('Local original OP.CPK required')
        cls.originals = demo.members(CPK(str(source)))
        cls.source = source

    def test_complete_category_and_reported_title(self):
        ids = [demo.message_id(m, t) for m in range(4) for t in range(6)]
        self.assertEqual(len(set(ids)), 24)
        self.assertEqual(localization.message(ids[0]), 'Mobile Suit Gundam Unicorn')
        for mid in ids:
            self.assertTrue(localization.message(mid))

    def test_all_captions_fit_and_only_texture_pixels_change(self):
        for member, original in self.originals.items():
            with self.subTest(member=member):
                built = demo.apply(original, member)
                demo.verify(original, built, member)
                # Every slot changes, not only the reported Gundam title.
                for texture in range(6):
                    start, size = demo.span(original, texture)
                    self.assertNotEqual(original[start:start+size], built[start:start+size])
                damaged = bytearray(built)
                damaged[-1] ^= 1
                with self.assertRaises(AssertionError):
                    demo.verify(original, bytes(damaged), member)

    def test_rejects_wrong_source_and_unsupported_text(self):
        bad = bytearray(self.originals[0])
        bad[0] ^= 1
        with self.assertRaises(AssertionError):
            demo.apply(bytes(bad), 0)
        for label in ('', 'line\nbreak', '\u65e5'):
            with patch.object(demo.localization, 'message', return_value=label):
                with self.assertRaises(AssertionError):
                    demo.tile(0, 0)

    def test_delivery_paths_registered(self):
        import deploy
        import extract
        self.assertEqual(deploy.LAYOUT['OP.CPK'], 'DATA/BTLC')
        self.assertEqual(extract.DISC['OP.CPK'], 'DATA/BTLC')
        self.assertIn('"OP.CPK": "DATA/BTLC"',
                      (demo.ROOT/'tools/apply_xdelta.py').read_text(encoding='utf-8'))

    def test_archive_round_trip_in_temporary_test_directory(self):
        # Test this one small archive, never invoke the full game build.
        with tempfile.TemporaryDirectory(prefix='test_demo_', dir=str(demo.ROOT/'work')) as out:
            with patch.object(demo, 'SOURCE', self.source):
                demo.build(out)
            result = Path(out)/'OP.CPK'
            demo.verify_archive(CPK(str(self.source)), CPK(str(result)))


if __name__ == '__main__':
    unittest.main()
