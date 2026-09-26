"""Regressions for the stage-10 transition archive-length defect."""
import tempfile
import unittest
from pathlib import Path

from cpk import CPK
from cpkpatch import build, validate_itoc


class ItocTests(unittest.TestCase):
    def rebuild(self, stage, replacements):
        source = Path('work/stage_dec') / (stage + '.cpk')
        if not source.exists():
            self.skipTest('Local original archive required: ' + str(source))
        original = CPK(str(source))
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for fid, data in replacements.items():
                path = Path(tmp) / str(fid)
                path.write_bytes(data)
                paths[fid] = str(path)
            output = Path(tmp) / 'rebuilt.cpk'
            build(str(source), str(output), paths)
            rebuilt = CPK(str(output))
            validate_itoc(rebuilt.buf)
            self.assertEqual(len(original.files), len(rebuilt.files))
            for old, new in zip(original.files, rebuilt.files):
                self.assertEqual(old['id'], new['id'])
                self.assertEqual(rebuilt.read(new),
                                 replacements.get(old['id'], original.read(old)))
            return rebuilt

    def test_no_promotion(self):
        self.rebuild('STG0018', {})

    def test_one_promotion(self):
        self.rebuild('STG0018', {3: b'a' * 70000})

    def test_two_promotions_accumulate_length(self):
        self.rebuild('STG0018', {3: b'a' * 81110, 4: b'b' * 68949})

    def test_empty_high_table(self):
        self.rebuild('STG0019', {3: b'a' * 70000, 4: b'b' * 71000})

    def test_stale_header_is_rejected(self):
        rebuilt = self.rebuild('STG0018', {3: b'a' * 70000, 4: b'b' * 71000})
        corrupt = bytearray(rebuilt.buf)
        rebuilt.header.patch(corrupt, 0, 'ItocSize', rebuilt._h('ItocSize') - 4)
        with self.assertRaisesRegex(ValueError, 'ITOC length mismatch'):
            validate_itoc(corrupt)


if __name__ == '__main__':
    unittest.main()
