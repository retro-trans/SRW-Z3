"""Local PCSG00264 executable conversion for Vita3K; no license in outputs.

Format references: Vita3K packages/sce_utils.cpp, packages/sce_types.h and
vitasdk/vita-toolchain/src/self.h. Public format constants are read from the
locally downloaded reference, not from a remote key service. User license
material is used only in memory. This is not retail-console signing.
"""
import hashlib
from pathlib import Path
import re
import struct
import sys
import zlib

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'work/vita/python_deps'))
from Crypto.Cipher import AES


def require(ok, message):
    if not ok:
        raise ValueError(message)


def take(data, offset, length):
    require(0 <= offset <= len(data) and 0 <= length <= len(data) - offset,
            'Truncated or out-of-bounds executable')
    return data[offset:offset + length]


def unpack(fmt, data, offset):
    return struct.unpack(fmt, take(data, offset, struct.calcsize(fmt)))


def parse(data):
    require(take(data, 0, 4) == b'SCE\0', 'Not a SELF executable')
    version, sdk, kind, meta, hlen, elen = unpack('<IHHIQQ', data, 4)
    require(version == 3 and kind == 1 and hlen == 4096 and elen < 64 * 1024**2,
            'Unsupported SELF header')
    fields = unpack('<12Q', data, 32)
    app, eh, ph, si = fields[3], fields[4], fields[5], fields[7]
    ai = unpack('<QIIQQ', data, app)
    elf = take(data, eh, 52)
    hdr = unpack('<16sHHIIIIIHHHHHH', elf, 0)
    require(hdr[0][:7] == b'\x7fELF\1\1\1' and hdr[2] == 40 and
            hdr[8:10] == (52, 32) and 0 < hdr[10] <= 16,
            'Unsupported ELF header')
    require(hdr[5] == 52 and hdr[6] == 0 and hdr[12] == 0,
            'Unexpected ELF table layout')
    phdrs = [unpack('<8I', data, ph + i * 32) for i in range(hdr[10])]
    infos = [unpack('<4Q', data, si + i * 32) for i in range(hdr[10])]
    for p, s in zip(phdrs, infos):
        require(p[1] + p[4] <= elen and s[2] in (1, 2) and s[3] in (1, 2),
                'Invalid executable segment')
        take(data, s[0], s[1])
    return dict(sdk=sdk, meta=meta, hlen=hlen, elen=elen, ai=ai,
                elf=elf, phdrs=phdrs, infos=infos)


def reference_keys(reference, revision):
    # Match the same relaxed version ranges used by Vita3K decrypt_fself.
    entries = re.findall(r'KeyType::(METADATA|NPDRM),\s*SceType::SELF,\s*'
                         r'(\d+),\s*"([0-9A-F]+)",\s*"([0-9A-F]+)",'
                         r'\s*0x[0-9A-Fa-f]+,\s*0x[0-9A-Fa-f]+,\s*SelfType::APP',
                         reference)
    selected = {}
    for kind, rev, key, iv in entries:
        target = revision if kind == 'METADATA' else (int(revision >= 2))
        if int(rev) == target:
            size = 64 if kind == 'METADATA' else 32
            value = (bytes.fromhex(key.zfill(size)), bytes.fromhex(iv.zfill(32)))
            require(len(value[0]) == size // 2 and len(value[1]) == 16,
                    'Invalid public reference constants')
            selected[kind] = value
    require(set(selected) == {'METADATA', 'NPDRM'}, 'Unsupported key revision')
    return selected


def decode_segments(data, license_key, reference):
    info = parse(data)
    require(info['ai'][2] == 8, 'Only APP executables are supported')
    require(len(license_key) == 16, 'Invalid license key length')
    require(all(s[3] == 1 for s in info['infos']), 'Expected encrypted source')
    keys = reference_keys(reference, info['sdk'] >> 8)
    dat = take(data, info['meta'] + 48, info['hlen'] - info['meta'] - 48)
    require(len(dat) >= 96 and len(dat) % 16 == 0, 'Invalid encrypted metadata')
    key, iv = keys['NPDRM']
    pre = AES.new(key, AES.MODE_CBC, iv).decrypt(license_key)
    wrapped = AES.new(pre, AES.MODE_CBC, iv).decrypt(dat[:64])
    key, iv = keys['METADATA']
    meta = AES.new(key, AES.MODE_CBC, iv).decrypt(wrapped)
    require(meta[16:32] == bytes(16) and meta[48:64] == bytes(16),
            'Executable metadata padding validation failed')
    plain = AES.new(meta[:16], AES.MODE_CBC, meta[32:48]).decrypt(dat[64:])
    mh = unpack('<Q6I', plain, 0)
    sections, nkeys = mh[2], mh[3]
    require(0 < sections <= 64 and 0 < nkeys <= 128, 'Invalid metadata counts')
    vault = take(plain, 32 + sections * 48, nkeys * 16)
    by_index = {}
    for i in range(sections):
        off, size, typ, idx, ht, hi, enc, ki, vi, comp = unpack('<QQIiIiIiiI', plain, 32 + i * 48)
        if enc != 3:
            continue
        require(0 <= idx < len(info['phdrs']) and idx not in by_index,
                'Invalid or duplicate metadata segment index')
        require(0 <= ki < nkeys and 0 <= vi < nkeys and comp in (1, 2),
                'Invalid segment crypto metadata')
        require(info['infos'][idx] == (off, size, comp, 1),
                'Metadata and SELF segment tables disagree')
        raw = AES.new(vault[ki*16:(ki+1)*16], AES.MODE_CTR, nonce=b'',
                      initial_value=int.from_bytes(vault[vi*16:(vi+1)*16], 'big')).decrypt(take(data, off, size))
        expected = info['phdrs'][idx][4]
        if comp == 2:
            decoder = zlib.decompressobj()
            raw = decoder.decompress(raw, expected + 1)
            require(decoder.eof and not decoder.unused_data and not decoder.unconsumed_tail,
                    'Invalid or oversized zlib segment')
        require(len(raw) == expected, 'Decrypted segment size mismatch')
        by_index[idx] = raw
    require(set(by_index) == set(range(len(info['phdrs']))), 'Missing executable segment')
    return info, by_index


def make_fself(info, segments):
    """VitaSDK-compatible plain SELF, preserving every decoded segment byte."""
    phdrs = info['phdrs']
    elf = bytearray(info['elen'])
    used = []
    for i, p in enumerate(phdrs):
        raw = segments[i]
        require(len(raw) == p[4], 'Segment length mismatch')
        start, end = p[1], p[1] + len(raw)
        require(not any(start < b and a < end for a, b in used), 'Overlapping ELF segments')
        used.append((start, end))
        elf[start:end] = raw
    prefix = info['elf'] + b''.join(struct.pack('<8I', *p) for p in phdrs)
    # A load segment can include the ELF header; reject contradictions.
    for i, p in enumerate(phdrs):
        if p[1] < len(prefix):
            n = min(p[4], len(prefix) - p[1])
            require(segments[i][:n] == prefix[p[1]:p[1]+n], 'Embedded ELF header differs')
    elf[:len(prefix)] = prefix
    out = bytearray(4096) + elf
    phoff = 0xe0
    sioff = phoff + len(phdrs) * 32
    voff = sioff + len(phdrs) * 32
    coff = voff + 16
    require(coff + 0x270 <= 0x600, 'SELF control tables too large')
    struct.pack_into('<4sIHHIQQ', out, 0, b'SCE\0', 3, 0xc0, 1, 0x600, 4096, len(elf))
    struct.pack_into('<12Q', out, 32, len(out), 0, 4, 0x80, 0xa0, phoff,
                     0, sioff, voff, coff, 0x270, 0)
    struct.pack_into('<QIIQQ', out, 0x80, info['ai'][0], 0, 8, 0x1000000000000, 0)
    out[0xa0:0xa0+52] = info['elf']
    for i, p in enumerate(phdrs):
        struct.pack_into('<8I', out, phoff+i*32, *p)
        struct.pack_into('<4Q', out, sioff+i*32, 4096+p[1], p[4], 1, 2)
    struct.pack_into('<4I', out, voff, 1, 0, 16, 0)
    for offset, typ, size, more in ((coff, 5, 0x110, 1),
                                    (coff+0x110, 6, 0x110, 1),
                                    (coff+0x220, 7, 0x50, 0)):
        struct.pack_into('<4I', out, offset, typ, size, more, 0)
    struct.pack_into('<I', out, coff+0x120, 1)
    result = bytes(out)
    check = parse(result)
    require(check['phdrs'] == phdrs and check['elf'] == info['elf'], 'SELF round-trip failed')
    for i, s in enumerate(check['infos']):
        require(s[2:] == (1, 2) and take(result, s[0], s[1]) == segments[i],
                'SELF segment round-trip failed')
    return result


def convert(data, license_key, reference):
    info, segments = decode_segments(data, license_key, reference)
    result = make_fself(info, segments)
    audit = dict(original_sha256=hashlib.sha256(data).hexdigest(),
                 patched_sha256=hashlib.sha256(result).hexdigest(), bytes=len(result),
                 segments=len(segments), segment_bytes_preserved=True,
                 segment_sha256=[hashlib.sha256(segments[i]).hexdigest() for i in range(len(segments))])
    return result, audit
