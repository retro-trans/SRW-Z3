"""Build the isolated native PFS reader from already downloaded public sources.

Uses generated OpenSSL headers with Git's installed libcrypto3 DLL; does not
compile/install OpenSSL or touch game/license files. No network in this script.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / 'work/vita'
OPENSSL = WORK / 'openssl_source'
PARSER = WORK / 'offline_parser_source'
PERL = 'C:/Program Files/Git/usr/bin/perl.exe'
CRYPTO = 'C:/Program Files/Git/mingw64/bin/libcrypto-3-x64.dll'


def main():
    includes = ['-I.', '-I../Locale-Maketext-Simple-0.21/lib',
                '-I../ExtUtils-MakeMaker-7.70/lib', '-I../Pod-Usage-2.03/lib',
                '-I../podlators-v6.1.1/lib', '-I../Pod-Simple-3.48/lib',
                '-I../Pod-Escapes-1.07/lib']
    # Configure already generated configdata.pm; generate only public headers.
    for template in sorted((OPENSSL / 'include/openssl').glob('*.h.in')):
        generated = subprocess.run([PERL] + includes + ['-Mconfigdata', 'util/dofile.pl',
                                   template.relative_to(OPENSSL).as_posix()],
                                   cwd=str(OPENSSL), stdout=subprocess.PIPE, check=True)
        template.with_suffix('').write_bytes(generated.stdout)
    print('OpenSSL public headers generated.', flush=True)
    excluded = {'PsvPfsParserConfig.cpp', 'rif2zrif.cpp', 'zrif2rif.cpp',
                'F00DKeyEncryptorFactory.cpp', 'F00DFileKeyEncryptor.cpp',
                'CryptoOperationsFactory.cpp'}
    sources = [str(path) for path in sorted(PARSER.glob('*.cpp')) if path.name not in excluded]
    command = ['C:/mingw64/bin/g++.exe', '-std=c++17', '-O2', '-static-libgcc',
               '-static-libstdc++', '-include', 'algorithm', '-include', 'cstring',
               '-I', str(PARSER), '-I', str(OPENSSL / 'include')]
    command += sources + [str(ROOT / 'platforms/vita/offline_pfs_main.cpp'), CRYPTO,
                          '-o', str(WORK / 'offline_pfs.exe')]
    subprocess.run(command, check=True)
    print('Offline reader compiled. No game or license was read.', flush=True)


if __name__ == '__main__':
    main()
