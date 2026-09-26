import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import apply_vita_release as A


class PatcherTests(unittest.TestCase):
    def test_copy_dry_run_hashes_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); src=root/'source'; pkg=root/'package'; out=root/'output'
            src.mkdir(); pkg.mkdir()
            data=b'synthetic game file'
            (src/'eboot.bin').write_bytes(data)
            info=dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
            man=dict(schema=1,title_id='PCSG00264',source_label='test source',target_label='test target',
                     files={'eboot.bin':dict(source=info,target=info)})
            (pkg/'manifest.json').write_text(json.dumps(man))
            A.apply(pkg,src,out,'unused')
            self.assertFalse(out.exists())
            A.apply(pkg,src,out,'unused',True,True)
            self.assertEqual((out/'PCSG00264/eboot.bin').read_bytes(),data)
            self.assertTrue((out/'SRW-Z3-Vita3K-0.6.14-install.zip').is_file())
            with self.assertRaises(ValueError): A.apply(pkg,src,out,'unused',True)
            (src/'eboot.bin').write_bytes(b'wrong')
            with self.assertRaises(ValueError): A.apply(pkg,src,root/'other','unused',True)
            self.assertFalse((root/'other').exists())

    def test_unsafe_names(self):
        for name in ('../escape','/absolute','C:/bad','x\\y','x/../bad','x//y'):
            with self.subTest(name=name), self.assertRaises(ValueError): A.safe(Path.cwd(),name)

    def test_delta_decode_hash_failure_is_not_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);src=root/'src';pkg=root/'pkg';out=root/'out'
            src.mkdir();pkg.mkdir()
            (src/'eboot.bin').write_bytes(b'a');(pkg/'delta').write_bytes(b'patch')
            info=lambda data:dict(bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
            man=dict(schema=1,title_id='PCSG00264',source_label='a',target_label='b',files={
                'eboot.bin':dict(source=info(b'a'),target=info(b'b'),patch=dict(name='delta',**info(b'patch')))})
            (pkg/'manifest.json').write_text(json.dumps(man))
            def fake(cmd,**kwargs):Path(cmd[-1]).write_bytes(b'incorrect')
            with patch.object(A.subprocess,'run',fake), self.assertRaises(ValueError):
                A.apply(pkg,src,out,'xdelta',True)
            self.assertFalse((out/'VERIFIED.json').exists())
            self.assertEqual((src/'eboot.bin').read_bytes(),b'a')


if __name__ == '__main__':unittest.main()
