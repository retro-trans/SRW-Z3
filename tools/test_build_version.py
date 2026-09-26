"""Synthetic fixtures only: no game files, release counters or installs touched."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_version
import release


class BuildVersionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'releases').mkdir()
        (self.root / 'build').mkdir()
        (self.root / 'build_version.json').write_text('{"last_successful_build":"0.6.0"}')
        self.manifest = {'schema': 1, 'ui_regression_checks': True,
                         'files': {'test.dat': {'bytes': 4,
                                  'sha256': hashlib.sha256(b'test').hexdigest()}}}
        (self.root / 'build/test.dat').write_bytes(b'test')

    def stamp(self):
        return build_version.stamp(self.root / 'build', self.manifest, self.root)

    def test_sequential_success(self):
        self.assertEqual(self.stamp(), '0.6.1')
        self.assertEqual(self.stamp(), '0.6.2')
        self.assertEqual(json.loads((self.root / 'build/build_manifest.json').read_text())['version'], '0.6.2')

    def test_numeric_order(self):
        for version in ('0.6.9', '0.6.10'):
            (self.root / ('releases/' + version + '.json')).write_text('{}')
        self.assertEqual(build_version.next_version(self.root), '0.6.11')

    def test_unvalidated_does_not_consume(self):
        self.manifest['ui_regression_checks'] = False
        with self.assertRaises(ValueError):
            self.stamp()
        self.assertEqual(build_version.next_version(self.root), '0.6.1')

    def test_failure_does_not_consume(self):
        with patch.object(build_version, 'write_json', side_effect=OSError('test failure')):
            with self.assertRaises(OSError):
                self.stamp()
        self.assertEqual(build_version.next_version(self.root), '0.6.1')
        self.assertFalse((self.root / 'build_version.lock').exists())

    def test_counter_failure_invalidates_manifest(self):
        real_write = build_version.write_json
        def fail_counter(path, data):
            if path.name == 'build_version.json':
                raise OSError('test failure')
            real_write(path, data)
        with patch.object(build_version, 'write_json', side_effect=fail_counter):
            with self.assertRaises(OSError):
                self.stamp()
        self.assertFalse((self.root / 'build/build_manifest.json').exists())
        self.assertEqual(build_version.next_version(self.root), '0.6.1')

    def test_existing_lock_is_preserved(self):
        (self.root / 'build_version.lock').touch()
        with self.assertRaises(RuntimeError):
            self.stamp()
        self.assertTrue((self.root / 'build_version.lock').exists())

    def test_footer_expected_number_matches(self):
        self.manifest['title_footer_version'] = '0.6.1'
        self.assertEqual(build_version.stamp(self.root/'build', self.manifest, self.root,
                                            expected_version='0.6.1'), '0.6.1')

    def test_concurrent_build_cannot_mislabel_footer(self):
        self.stamp()  # Another completed build claimed the prospective number.
        (self.root/'build/build_manifest.json').unlink()
        self.manifest['title_footer_version'] = '0.6.1'
        with self.assertRaisesRegex(RuntimeError, 'build version changed'):
            build_version.stamp(self.root/'build', self.manifest, self.root,
                                expected_version='0.6.1')
        self.assertEqual(build_version.next_version(self.root), '0.6.2')
        self.assertFalse((self.root/'build/build_manifest.json').exists())
        self.assertFalse((self.root/'build_version.lock').exists())

    def test_footer_mismatch_does_not_consume_number(self):
        self.manifest['title_footer_version'] = '0.5.9'
        with self.assertRaisesRegex(ValueError, 'title footer version'):
            self.stamp()
        self.assertEqual(build_version.next_version(self.root), '0.6.1')
        self.assertFalse((self.root/'build/build_manifest.json').exists())

    def snapshot(self, version=None):
        with patch.object(release, 'ROOT', str(self.root / 'releases')), \
             patch.object(release.deploy, 'LAYOUT', {'test.dat': ''}):
            return release.snapshot(version, 'synthetic test', str(self.root / 'build'))

    def test_snapshot_uses_build_number_without_increment(self):
        self.stamp()
        _, manifest = self.snapshot()
        self.assertEqual(manifest['version'], '0.6.1')
        self.assertEqual(build_version.next_version(self.root), '0.6.2')

    def test_snapshot_rejects_tampering(self):
        self.stamp()
        (self.root / 'build/test.dat').write_bytes(b'edit')
        with self.assertRaisesRegex(SystemExit, 'changed since validation'):
            self.snapshot()
        self.assertFalse((self.root / 'releases/0.6.1').exists())

    def test_snapshot_rejects_number_mismatch(self):
        self.stamp()
        with self.assertRaisesRegex(SystemExit, 'differs from build version'):
            self.snapshot('0.6.2')

    def test_snapshot_rejects_missing_validation(self):
        with self.assertRaisesRegex(SystemExit, 'no validation manifest'):
            self.snapshot()

    def test_snapshot_cannot_overwrite(self):
        self.stamp()
        self.snapshot()
        with self.assertRaisesRegex(SystemExit, 'already exists'):
            self.snapshot()

    def test_snapshot_dry_run_validates_without_writing(self):
        self.stamp()
        with patch.object(release, 'ROOT', str(self.root/'releases')), \
             patch.object(release.deploy, 'LAYOUT', {'test.dat': ''}):
            release.snapshot(None, 'dry run', str(self.root/'build'), dry_run=True)
            self.assertEqual(list((self.root/'releases').iterdir()), [])
            (self.root/'build/test.dat').write_bytes(b'bad')
            with self.assertRaisesRegex(SystemExit, 'changed since validation'):
                release.snapshot(None, 'dry run', str(self.root/'build'), dry_run=True)

    def test_installer_layout_matches_release(self):
        import apply_xdelta, deploy
        self.assertEqual(apply_xdelta.LAYOUT, deploy.LAYOUT)


if __name__ == '__main__':
    unittest.main()
