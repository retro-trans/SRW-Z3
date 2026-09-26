"""Read-only ARM renderer inspection; optional private disassembly under work/vita."""
import argparse
import hashlib
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / 'work/vita/python_deps'), str(Path(__file__).parent)]
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from self_decrypt import parse, require

PILOT = ROOT / 'work/vita/english_pilot_01_install/SRW-Z3-Vita-English-pilot-01-install.zip'
EBOOT_SHA = '14414068b44fa8ded7f9acb467dceddb4cd02c88845a4109a6e811960cc985d1'


def load():
    with zipfile.ZipFile(str(PILOT)) as archive:
        data = archive.read('PCSG00264/eboot.bin')
    require(hashlib.sha256(data).hexdigest() == EBOOT_SHA, 'Unknown Vita pilot executable')
    return data, parse(data)


def segment(data, info, idx=0):
    off, size, comp, crypt = info['infos'][idx]
    require((comp, crypt) == (1, 2), 'Expected plain executable')
    return data[off:off+size], info['phdrs'][idx][2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--start', type=lambda x: int(x, 0))
    ap.add_argument('--size', type=lambda x: int(x, 0), default=0x200)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    data, info = load()
    raw, base = segment(data, info)
    md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    md.skipdata = True
    if args.start is not None:
        start = args.start & ~1
        require(base <= start < base+len(raw), 'Address outside code segment')
        for addr, size, mnemonic, operands in md.disasm_lite(raw[start-base:start-base+args.size], start):
            print('%08x: %-10s %s' % (addr, mnemonic, operands))
        return
    print('Known executable verified. Code bytes:', len(raw), 'VA:', hex(base))
    if args.write:
        out = ROOT / 'work/vita/vwf_original_thumb.txt'
        require(not out.exists(), 'Disassembly already exists')
        with out.open('x', encoding='utf-8') as f:
            for addr, size, mnemonic, operands in md.disasm_lite(raw, base):
                f.write('%08x: %-10s %s\n' % (addr, mnemonic, operands))
        print('Private analysis output:', out)
    else:
        print('DRY RUN: --write creates a private Thumb disassembly, not a game build.')


if __name__ == '__main__':
    main()
