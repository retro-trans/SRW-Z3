"""Synthetic release ZIP tests; no game files or external publication."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import zipfile
import package_release as P


class PackageReleaseTests(unittest.TestCase):
    def fixture(self,root):
        release=root/'releases/0.6.13_xdelta'
        (release/'from-original').mkdir(parents=True)
        (root/'tools').mkdir();(root/'docs').mkdir()
        (root/'releases/0.6.13.json').write_text(json.dumps({'version':'0.6.13','files':{'A.BIN':{}}}))
        (release/'from-original/A.BIN.xdelta').write_bytes(b'synthetic patch')
        (release/'MANIFEST.txt').write_text('synthetic manifest')
        (root/'tools/apply_xdelta.py').write_text('# synthetic helper')
        (root/'docs/INSTALL.md').write_text('default guide')
        return release

    def test_selected_guide_and_zip_readback(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=self.fixture(root)
            guide=root/'docs/specific.md';guide.write_text('RPCS3 only; hardware unverified')
            with mock.patch.object(P,'__file__',str(root/'tools/package_release.py')):
                P.package('0.6.13',guide=guide)
                self.assertFalse(list(release.glob('*.zip')))
                P.package('0.6.13',write=True,guide=guide)
                with zipfile.ZipFile(next(release.glob('*.zip'))) as z:
                    self.assertEqual(z.read('INSTALL.md'),guide.read_bytes())
                    self.assertEqual(len(z.namelist()),4)
                with self.assertRaises(ValueError):P.package('0.6.13',write=True,guide=guide)

    def test_default_guide_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=self.fixture(root)
            with mock.patch.object(P,'__file__',str(root/'tools/package_release.py')):
                P.package('0.6.13',write=True)
            with zipfile.ZipFile(next(release.glob('*.zip'))) as z:
                self.assertEqual(z.read('INSTALL.md'),b'default guide')

    def test_missing_guide_refused_before_zip_write(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);release=self.fixture(root)
            with mock.patch.object(P,'__file__',str(root/'tools/package_release.py')):
                with self.assertRaises(ValueError):P.package('0.6.13',write=True,guide=root/'missing')
            self.assertFalse(list(release.glob('*.zip')))


if __name__=='__main__':unittest.main()
