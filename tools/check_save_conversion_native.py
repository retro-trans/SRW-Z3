"""Run Vita's native, shared-format save validators in an isolated ARM CPU.

No emulator launch, install, live-save write, or checksum bypass. This verifies
serialized data, not a full game load. PS3 code was statically compared; native
PPC execution is not claimed (the local PPC harness raises a CPU exception).
"""
import argparse
import json
from pathlib import Path
import sys
import zipfile

import convert_z3_saves as c

sys.path.insert(0, str(c.ROOT / 'platforms/vita'))
sys.path.insert(0, str(c.ROOT / 'work/vita/python_deps'))
import build_repatch as r
from self_decrypt import parse
import unicorn as u
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC


def verify(folder):
    folder = folder.resolve()
    c.require((c.ROOT / 'work').resolve() in folder.parents, 'Only local workspace test output')
    audit_path = folder / 'CONVERSION_AUDIT.json'
    audit = json.loads(audit_path.read_text(encoding='utf-8'))
    source_audit = r.SOURCE / 'BUILD_AUDIT.json'
    c.require(r.hash_file(source_audit)[1] == r.AUDIT_SHA, 'Vita source audit pin mismatch')
    reference = json.loads(source_audit.read_text(encoding='utf-8'))
    with zipfile.ZipFile(str(r.SOURCE / r.SOURCE_ZIP)) as archive:
        eboot = archive.read('PCSG00264/eboot.bin')
    c.require(c.row(eboot) == {k: reference['files']['eboot.bin'][k] for k in ('bytes', 'sha256')},
              'Vita executable changed')
    info = parse(eboot)
    section = info['infos'][0]
    code = eboot[section[0]:section[0] + section[1]]
    base = info['phdrs'][0][2]
    c.require(base == 0x81000000, 'Unexpected native code address')
    cpu = u.Uc(u.UC_ARCH_ARM, u.UC_MODE_THUMB)
    cpu.mem_map(base, (len(code) + 4095) & ~4095)
    cpu.mem_write(base, code)
    for address, size in ((0x20000000, 0x10000), (0x30000000, 0x100000), (0x40000000, 0x1000)):
        cpu.mem_map(address, size)

    def call(entry, data, arg0=0x30000000, arg1=0):
        cpu.mem_write(0x30000000, data)
        cpu.reg_write(UC_ARM_REG_SP, 0x20008000)
        cpu.reg_write(UC_ARM_REG_R0, arg0)
        cpu.reg_write(UC_ARM_REG_R1, arg1)
        cpu.reg_write(UC_ARM_REG_LR, 0x40000001)
        cpu.emu_start(entry | 1, 0x40000000, count=20000000)
        c.require(cpu.reg_read(UC_ARM_REG_PC) == 0x40000000, 'Native checker did not return')
        c.require(bytes(cpu.mem_read(0x30000000, len(data))) == data, 'Native checker mutated input')
        return cpu.reg_read(UC_ARM_REG_R0)

    results = []
    for direction, package in audit['packages'].items():
        c.require(c.row((folder / package['name']).read_bytes()) ==
                  {k: package[k] for k in ('bytes', 'sha256')}, 'Converted ZIP changed')
        for name, expected in package['files'].items():
            if Path(name).name not in c.FORMATS:
                continue
            kind = Path(name).name
            data = (folder / direction / name).read_bytes()
            c.require(c.row(data) == expected, 'Converted file changed')
            entry = 0x810B7860 if kind == 'STAGE.BIN' else 0x810B72EA
            version_entry = 0x810B7852 if kind == 'STAGE.BIN' else 0x810B72DC
            payload = c.FORMATS[kind][3]
            c.require(call(entry, data) == 1, 'Native payload checksum rejected save')
            c.require(call(version_entry, data) == 1, 'Native version check rejected save')
            c.require(call(0x810B47BC, data, 0x3FC, 0x30000044) == int.from_bytes(data[0x40:0x42], 'little'),
                      'Native summary checksum rejected save')
            damaged = bytearray(data)
            damaged[payload + 32] ^= 1
            c.require(call(entry, bytes(damaged)) == 0, 'Native checker did not reject corruption')
            damaged = bytearray(data)
            damaged[2] ^= 1
            c.require(call(version_entry, bytes(damaged)) == 0, 'Native version gate did not reject corruption')
            results.append(dict(direction=direction, file=name, **expected,
                                native_payload_checksum=True, native_summary_checksum=True,
                                native_version_gate=True, corrupt_data_rejected=True))
            print('Native shared-payload validator PASS:', direction, name, flush=True)
    report = dict(schema=1, conversion_audit_sha256=c.digest(audit_path.read_bytes()),
                  vita_eboot_sha256=c.digest(eboot), harness='Unicorn ARM Thumb', results=results,
                  full_game_load_tested=False, ps3_native_execution=False,
                  scope='Vita native checks accept the shared serialized data in both directions; '
                        'destination-specific header size and metadata checked separately by converter')
    c.put_files(folder, {'NATIVE_VALIDATION.json': (json.dumps(report, indent=2) + '\n').encode()})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    args = parser.parse_args()
    verify(args.folder)
