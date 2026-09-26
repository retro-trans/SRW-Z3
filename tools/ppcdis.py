"""Disassemble a range of the decrypted EBOOT with the constants resolved.

PPC64 big-endian via capstone. `vaddr = file_offset + 0x10000`, TOC r2 =
0x7dd920. Loads from r2 are annotated with the value in the TOC slot (as
float and as hex), `bl` targets are printed as addresses, and `lis/addi`
pairs are left as-is (rare in this binary; it is TOC-driven).

    python tools/ppcdis.py <elf> <start_va> <end_va> [--grep pattern]
"""
import io
import re
import struct
import sys

from capstone import Cs, CS_ARCH_PPC, CS_MODE_64, CS_MODE_BIG_ENDIAN

VA0 = 0x10000
TOC = 0x7dd920


def load(path):
    return open(path, "rb").read()


def toc_value(b, off):
    fo = TOC + off - VA0
    if not 0 <= fo < len(b) - 4:
        return None
    raw = b[fo:fo + 4]
    f = struct.unpack(">f", raw)[0]
    u = struct.unpack(">I", raw)[0]
    d = struct.unpack(">d", b[fo:fo + 8])[0] if fo + 8 <= len(b) else None
    return f, u, d


def disasm(b, start, end):
    md = Cs(CS_ARCH_PPC, CS_MODE_64 | CS_MODE_BIG_ENDIAN)
    md.detail = False
    lines = []
    pos = start
    while pos < end:
        got = False
        for ins in md.disasm(b[pos - VA0:end - VA0], pos):
            got = True
            pos = ins.address + 4
            _emit(b, ins, lines)
        if not got:
            lines.append("%#8x  .long 0x%08x" % (pos, struct.unpack(">I", b[pos - VA0:pos - VA0 + 4])[0]))
            pos += 4
    return lines


def _emit(b, ins, lines):
    if True:
        txt = "%s %s" % (ins.mnemonic, ins.op_str)
        note = ""
        m = re.search(r"(-?0x[0-9a-f]+|-?\d+)\(r2\)", ins.op_str)
        if m:
            off = int(m.group(1), 0)
            v = toc_value(b, off)
            if v:
                f, u, d = v
                if ins.mnemonic.startswith("lf"):
                    note = "  ; TOC[%#x] = %g (f32) / %s (f64)" % (off, f, ("%g" % d) if d is not None else "?")
                else:
                    note = "  ; TOC[%#x] = %#010x" % (off, u)
        if ins.mnemonic in ("bl", "b") and ins.op_str.startswith("0x"):
            note = "  ; -> %s" % ins.op_str
        lines.append("%#8x  %-36s%s" % (ins.address, txt, note))


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    b = load(argv[1])
    start, end = int(argv[2], 0), int(argv[3], 0)
    lines = disasm(b, start, end)
    pat = re.compile(argv[argv.index("--grep") + 1]) if "--grep" in argv else None
    for ln in lines:
        if pat is None or pat.search(ln):
            print(ln)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
