"""Current-source hardware packaging guards, without real game contents."""
import copy
import json
from pathlib import Path
import tempfile
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'platforms/ps3'))
import package_hardware_current as m


class CurrentPackageTests(unittest.TestCase):
    def test_dry_run_does_not_package(self):
        with patch('sys.argv', ['package', '--build', 'build', '--out', 'output']), \
             patch.object(m, 'preflight', return_value='checked') as preflight, \
             patch.object(m, 'package') as package:
            m.main()
            preflight.assert_called_once()
            package.assert_not_called()

    def test_write_requires_preflight(self):
        with patch('sys.argv', ['package', '--build', 'build', '--out', 'output', '--write']), \
             patch.object(m, 'preflight', side_effect=ValueError('bad source')), \
             patch.object(m, 'package') as package:
            with self.assertRaises(ValueError):
                m.main()
            package.assert_not_called()

    def test_snapshot_overlay_preserves_source_and_other_files(self):
        self.overlay_case(fresh=True)

    def test_preserved_layout_overlay_preserves_source_and_other_files(self):
        self.overlay_case(fresh=False)

    def overlay_case(self, fresh):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build = root / 'build'
            build.mkdir()
            (build / 'EBOOT.BIN').write_bytes(b'raw ELF')
            (build / 'ASSET').write_bytes(b'new asset')
            manifest = dict(schema=1, platform='ps3', version='0.6.15',
                            title_footer_version='0.6.15', ui_regression_checks=True,
                            files={n: m.d.info(build / n) for n in ('EBOOT.BIN', 'ASSET')})
            original_manifest = copy.deepcopy(manifest)
            (build / 'build_manifest.json').write_text(json.dumps(manifest))
            (root / 'docs').mkdir()
            (root / 'docs/PS3_CURRENT_HARDWARE_TEST.md').write_text('guide')
            output = root / 'output'
            replacements = {m.d.EBOOT: 'EBOOT.BIN', '/ASSET': 'ASSET'}

            def extract(source, stage, inventory):
                files = {}
                for name, data in ((m.d.EBOOT, b'original SELF'),
                                   ('/ASSET', b'old asset'), ('/KEEP', b'keep')):
                    path = stage / m.c.safe_relative(name)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(data)
                    files[name] = m.d.info(path)
                return files

            def image(path, stage, primary, expected):
                self.assertEqual((stage / 'KEEP').read_bytes(), b'keep')
                self.assertEqual((stage / 'ASSET').read_bytes(), b'new asset')
                self.assertEqual((stage / m.c.safe_relative(m.d.EBOOT)).read_bytes(), b'wrapped')
                for name, info in expected.items():
                    self.assertEqual(m.d.info(stage / m.c.safe_relative(name)), info)
                return {'sha256': 'test-hash', 'name': path.name}

            state = ((manifest, replacements, {}, {}), b'original', b'raw ELF', b'folded')
            def preserved(path, source, inventory, primary, staged, expected):
                self.assertEqual(set(staged), set(replacements))
                for name, target in staged.items():
                    self.assertEqual(m.d.info(target), expected[name])
                return image(path, output/'intermediate_disc', primary, expected)

            with patch.object(m.c, 'ROOT', root), \
                 patch.object(m.d, 'extract_original', side_effect=extract), \
                 patch.object(m.d, 'write_image', side_effect=image), \
                 patch.object(m.preserved_iso, 'write', side_effect=preserved), \
                 patch.object(m.d, 'wrap', return_value=(b'wrapped', {})), \
                 patch.object(m.b, 'rpc_decode', return_value=b'folded'), \
                 patch.object(m.layout, 'verify', return_value={'passed': True}):
                report = m.package(root / 'source', build, output, root / 'fself', state, fresh=fresh)
            derived = json.loads((output / 'snapshot/build_manifest.json').read_text())
            self.assertEqual(manifest, original_manifest)
            self.assertEqual((build / 'EBOOT.BIN').read_bytes(), b'raw ELF')
            self.assertEqual(derived['derived_from_manifest_sha256'],
                             m.c.digest(build / 'build_manifest.json'))
            self.assertEqual(derived['files']['EBOOT.BIN'], m.d.info(output / 'snapshot/EBOOT.BIN'))
            self.assertFalse(report['hardware_tested'])
            self.assertFalse(report['rpcs3_runtime_tested'])
            self.assertFalse(report['release_or_upload_performed'])


if __name__ == '__main__':
    unittest.main()
