"""Synthetic input checks for the ISO release planner; no game content needed."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import iso_patch as P


class IsoPlannerTests(unittest.TestCase):
    def test_dry_run_checks_explicit_previous_without_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            snapshot = root / 'releases/next'
            snapshot.mkdir(parents=True)
            (snapshot / 'sample').write_bytes(b'test')
            (root / 'releases/next.json').write_text(json.dumps({
                'files': {'sample': {'sha1': hashlib.sha1(b'test').hexdigest()}}}))
            original = root / 'original.iso'
            previous = root / 'custom-previous.iso'
            original.touch()
            previous.touch()
            output = root / 'output.iso'
            args = ['iso_patch', 'next', '--iso', str(original), '--prev', 'old',
                    '--prev-iso', str(previous), '--out', str(output), '--dry-run']
            with mock.patch.object(P, 'ROOT', str(root)), \
                    mock.patch.object(P, 'shipped_paths', return_value={'sample': []}), \
                    mock.patch('sys.argv', args), mock.patch.object(P, 'build') as build, \
                    mock.patch.object(P.subprocess, 'run') as run, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout:
                P.main()
                self.assertIn(str(previous), stdout.getvalue())
                build.assert_not_called()
                run.assert_not_called()
                self.assertFalse(output.exists())
                (snapshot / 'sample').write_bytes(b'changed')
                with self.assertRaisesRegex(SystemExit, 'Snapshot hash mismatch'):
                    P.main()
                previous.unlink()
                with self.assertRaisesRegex(SystemExit, 'Missing original or previous ISO'):
                    P.main()

    def test_previous_path_requires_version(self):
        with mock.patch.object(P.os.path, 'isdir', return_value=True), \
                mock.patch('sys.argv', ['iso_patch', 'next', '--prev-iso', 'old.iso']):
            with self.assertRaisesRegex(SystemExit, '--prev-iso requires --prev'):
                P.main()


if __name__ == '__main__':
    unittest.main()
