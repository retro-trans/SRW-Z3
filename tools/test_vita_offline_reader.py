"""Local integration guards using a synthetic wrong key, never the real RIF."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'work/vita'
READER = WORK / 'offline_pfs.exe'
SOURCE = WORK / 'app/PCSG00264'


@unittest.skipUnless(READER.exists() and SOURCE.exists(), 'Local reader/source required')
class OfflineReaderTests(unittest.TestCase):
    def run_reader(self, destination_exists=False):
        with tempfile.TemporaryDirectory(prefix='reader_test_', dir=str(WORK)) as temp:
            folder = Path(temp)
            license_file = folder / 'synthetic.bin'
            rif = bytearray(512)
            rif[0x17:0x20] = b'PCSG00264'
            rif[0x50:0x60] = b'FAKE_TEST_KEY_12'
            license_file.write_bytes(rif)
            destination = folder / 'output'
            if destination_exists:
                destination.mkdir()
            env = dict(os.environ)
            env['PATH'] = 'C:/Program Files/Git/mingw64/bin;C:/mingw64/bin;' + env.get('PATH', '')
            result = subprocess.run([str(READER), str(SOURCE), str(destination),
                                     str(license_file), '--write'], env=env,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            output = result.stdout + result.stderr
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(b'FAKE_TEST_KEY_12', output)
            self.assertNotIn(b'FAKE_TEST_KEY_12'.hex().encode(), output)
            self.assertEqual(destination.exists(), destination_exists)
            if destination_exists:
                self.assertEqual(list(destination.iterdir()), [])
                self.assertIn(b'destination already exists', output)
            else:
                self.assertIn(b'FAIL; phase=1', output)

    def test_wrong_key_fails_before_output_creation(self):
        self.run_reader()

    def test_existing_destination_is_untouched(self):
        self.run_reader(destination_exists=True)


if __name__ == '__main__':
    unittest.main()
