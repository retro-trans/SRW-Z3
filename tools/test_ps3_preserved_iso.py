"""The layout-preserving hardware disc writer, on a synthetic UDF-bridge disc.

    python tools/test_ps3_preserved_iso.py
"""
import hashlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'platforms' / 'ps3'))
sys.path.insert(0, str(ROOT / 'tools'))
import cfw_package as c  # noqa: E402
import preserved_iso  # noqa: E402

FILES = {
    '/PS3_GAME/USRDIR/EBOOT.BIN': b'\x7fELF' + bytes(range(256)) * 40,
    '/PS3_GAME/USRDIR/DATA/KEEP.CPK': b'keep me' * 3000,
    '/PS3_GAME/USRDIR/DATA/SWAP.CPK': b'japanese' * 500,
    '/PS3_GAME/PARAM.SFO': b'PSF\0' + bytes(60),
}
# the real disc's primary names happen to equal its Joliet names
PRIMARY = {k: k for k in FILES}


def info(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def make_disc(path):
    import pycdlib
    iso = pycdlib.PyCdlib()
    iso.new(interchange_level=3, joliet=3, udf='2.60', vol_ident='PS3VOLUME')
    dirs = sorted({str(p).replace('\\', '/') for n in FILES for p in Path(n).parents
                   if str(p) not in ('/', '\\')}, key=lambda p: (p.count('/'), p))
    for d in dirs:
        iso.add_directory(iso_path=d, joliet_path=d, udf_path=d)
    for name, data in FILES.items():
        iso.add_fp(io.BytesIO(data), len(data), iso_path=PRIMARY[name] + ';1',
                   joliet_path=name, udf_path=name)
    iso.write(str(path))
    iso.close()


def inventory(path):
    reader = c.ISO9660(str(path))
    try:
        return dict(reader.walk())
    finally:
        reader.fh.close()


class PreservedIso(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.source = self.tmp / 'original.iso'
        make_disc(self.source)
        self.assertTrue(preserved_iso.udf_present(self.source), 'fixture needs a UDF bridge')

    def build(self, new):
        local = self.tmp / 'SWAP.CPK'
        local.write_bytes(new)
        expected = {k: info(v) for k, v in FILES.items()}
        expected['/PS3_GAME/USRDIR/DATA/SWAP.CPK'] = info(new)
        image = self.tmp / 'out.iso'
        report = preserved_iso.write(image, self.source, inventory(self.source), PRIMARY,
                                     {'/PS3_GAME/USRDIR/DATA/SWAP.CPK': local}, expected)
        return image, report

    def test_grown_file_is_appended_and_both_trees_repointed(self):
        new = b'english!' * 4000                  # much larger than the original
        image, report = self.build(new)
        self.assertEqual(report['udf'], 'absent')
        self.assertEqual(report['files_verified_each_tree'], len(FILES))
        after = inventory(image)
        before = inventory(self.source)
        swapped = '/PS3_GAME/USRDIR/DATA/SWAP.CPK'
        self.assertGreaterEqual(after[swapped]['lba'] * c.SECTOR, self.source.stat().st_size)
        for name in FILES:
            if name != swapped:
                self.assertEqual(after[name]['lba'], before[name]['lba'], name)

    def test_unchanged_bytes_stay_in_place(self):
        image, _ = self.build(b'x' * 10)
        src, out = self.source.read_bytes(), image.read_bytes()
        keep = inventory(self.source)['/PS3_GAME/USRDIR/DATA/KEEP.CPK']
        start = keep['lba'] * c.SECTOR
        self.assertEqual(src[start:start + keep['size']], out[start:start + keep['size']])
        # outside the header, UDF and directory sectors, nothing else changed
        differing = sum(1 for i in range(0, len(src), c.SECTOR)
                        if src[i:i + c.SECTOR] != out[i:i + c.SECTOR])
        self.assertLess(differing, 40)

    def test_disc_header_is_one_whole_image_plaintext_region(self):
        image, report = self.build(b'y' * 5000)
        self.assertEqual(report['disc']['plaintext_regions'], 1)
        self.assertEqual(report['disc']['encrypted_regions'], 0)
        self.assertEqual(report['disc']['sectors'] * c.SECTOR, image.stat().st_size)

    def test_refuses_existing_output(self):
        (self.tmp / 'out.iso').write_bytes(b'')
        with self.assertRaises(ValueError):
            self.build(b'z')


if __name__ == '__main__':
    unittest.main()
