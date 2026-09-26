"""Synthetic installer safety: verified backups, atomic copies and rollback."""
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'platforms/vita'))
import install_vwf as I


class InstallTests(unittest.TestCase):
    def test_atomic_copy_does_not_replace_destination_on_bad_hash(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'game.bin';p.write_bytes(b'old')
            with self.assertRaises(ValueError):I.atomic_copy(io.BytesIO(b'bad'),p,(3,'wrong'))
            self.assertEqual(p.read_bytes(),b'old');self.assertEqual(list(Path(d).iterdir()),[p])

    def test_running_emulator_blocks_before_preflight(self):
        with mock.patch.object(I,'running',return_value=True),mock.patch.object(I,'preflight') as preflight:
            with self.assertRaises(ValueError):I.install(Path('game'),Path('build'),True)
            preflight.assert_not_called()

    def test_target_rejects_paths_outside_game_and_license_metadata(self):
        with tempfile.TemporaryDirectory() as d:
            game=Path(d).resolve()
            for name in ('../save.dat','/save.dat','DATA/../save.dat','sce_sys/package/work.bin'):
                with self.assertRaises(ValueError):I.target(game,name)

    def exercise(self,fail=False):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory).resolve();game=root/'ux0/app/PCSG00264';game.mkdir(parents=True)
            save=root/'ux0/user/00/savedata/PCSG00264/save.dat';save.parent.mkdir(parents=True);save.write_bytes(b'save')
            archive=root/'test.zip';before={};after={};changes={}
            with zipfile.ZipFile(str(archive),'w') as z:
                for n in ('one.bin','two.bin'):
                    p=game/n;p.write_bytes(('old '+n).encode());before[n]=p.read_bytes()
                    size,sha=I.hash_file(p);payload=('new '+n).encode();after[n]=payload
                    q=root/n;q.write_bytes(payload);ns,nh=I.hash_file(q)
                    changes[n]=dict(before_bytes=size,before_sha256=sha,after_bytes=ns,after_sha256=nh)
                    z.writestr('PCSG00264/'+n,payload)
            audit=dict(build='vita-english-vwf-test-02',zip=dict(sha256=I.hash_file(archive)[1]),
                       files={n:dict(bytes=r['after_bytes'],sha256=r['after_sha256']) for n,r in changes.items()})
            real=I.atomic_copy;calls=[]
            def copy(*args):
                calls.append(args[1].name)
                if fail and len(calls)==2:raise OSError('Synthetic failure')
                return real(*args)
            with mock.patch.object(I,'ROOT',root),mock.patch.object(I,'running',return_value=False),mock.patch.object(I,'preflight',return_value=(game,archive,audit,changes)),mock.patch.object(I,'atomic_copy',side_effect=copy):
                if fail:
                    with self.assertRaises(OSError):I.install(game,root,True)
                else:I.install(game,root,True)
            for n in before:self.assertEqual((game/n).read_bytes(),before[n] if fail else after[n])
            self.assertEqual(save.read_bytes(),b'save')
            backups=list((root/'work/vita/backups').iterdir());self.assertEqual(len(backups),1)
            for n in before:self.assertEqual((backups[0]/n).read_bytes(),before[n])
            self.assertEqual(json.loads((backups[0]/'INSTALL_AUDIT.json').read_text())['status'],
                             'rolled_back' if fail else 'installed_verified')

    def test_success_keeps_verified_originals_and_saves(self):self.exercise()
    def test_partial_failure_restores_all_attempted_files(self):self.exercise(True)


if __name__=='__main__':unittest.main()
