"""Compare current Python to the pinned pre-migration source without rewriting it.

The optional --baseline-tests runs selected unittest names using the verified
backup modules in memory. Requires this workspace's ignored migration backup.
It never restores files or changes an installed game.
"""
import argparse
import ast
import importlib.abc
import importlib.util
from pathlib import Path
import sys
import unittest

import localization as L


ROOT=L.ROOT
BACKUP=ROOT/'work/localization/migration_backup'


def originals():
    audit=L.read_json(ROOT/'localization/migration.json')
    out={}
    for name,expected in audit['original_sha256'].items():
        if name.startswith('tools/'):
            raw=(BACKUP/name).read_bytes()
            L.require(L.sha(raw)==expected,'Backup changed: '+name)
            out[name]=raw
    return out


def check():
    catalog=L.Catalog()
    class Restore(ast.NodeTransformer):
        def visit_Import(self,node):
            return None if len(node.names)==1 and node.names[0].name=='localization' and node.names[0].asname=='_l10n' else node
        def visit_Call(self,node):
            if isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='_l10n':
                return ast.Constant(value=catalog.literal(node.args[0].value),kind=None)
            return self.generic_visit(node)
    for name,before in originals().items():
        after=Restore().visit(ast.parse((ROOT/name).read_bytes()))
        L.require(ast.dump(after)==ast.dump(ast.parse(before)),'AST/content changed: '+name)
    print('PASS: 45 migrated Python modules are AST-identical after resolving catalog text.')


class BackupLoader(importlib.abc.MetaPathFinder,importlib.abc.Loader):
    def __init__(self):
        self.modules={Path(n).stem:(n,b) for n,b in originals().items()}
    def find_spec(self,fullname,path=None,target=None):
        if fullname in self.modules:
            return importlib.util.spec_from_loader(fullname,self)
    def create_module(self,spec):
        return None
    def exec_module(self,module):
        name,raw=self.modules[module.__name__]
        module.__file__=str(ROOT/name)
        exec(compile(raw,str(ROOT/name),'exec'),module.__dict__)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline-tests',nargs='+')
    args=ap.parse_args()
    if args.baseline_tests:
        sys.meta_path.insert(0,BackupLoader())
        result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromNames(args.baseline_tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    check()
