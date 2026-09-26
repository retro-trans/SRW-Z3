"""PCSG00264's linear P4 GXT font pages. No PS3 texture bytes are reused."""
import struct
from PIL import Image


def require(condition, message):
    if not condition:
        raise ValueError(message)


class FontPage:
    def __init__(self, data):
        self.data = bytes(data)
        require(data[:8] == b'GXT\0\x03\0\0\x10', 'Unsupported GXT version')
        count, offset, size, p4, p8 = struct.unpack_from('<5I', data, 8)
        require((count, offset, p4, p8) == (1, 64, 2, 0), 'Unexpected font palettes/layout')
        texture, pixels, palette, flags, kind, fmt = struct.unpack_from('<6I', data, 32)
        self.width, self.height, mipmaps = struct.unpack_from('<HHI', data, 56)
        require((texture, palette, flags, kind, fmt, mipmaps) ==
                (64, 0, 0, 0x60000000, 0x94000000, 1), 'Not a linear P4 font texture')
        require((self.width, self.height) == (4096, 1120), 'Unexpected font dimensions')
        require(pixels == self.width * self.height // 2 and size == pixels + 128
                and len(data) == offset + size, 'Font size mismatch')
        self.pixels = pixels
        self.palettes = [data[64 + pixels + i * 64:64 + pixels + (i + 1) * 64] for i in range(2)]

    def indices(self):
        out = bytearray(self.pixels * 2)
        out[0::2] = bytes(v & 15 for v in self.data[64:64 + self.pixels])
        out[1::2] = bytes(v >> 4 for v in self.data[64:64 + self.pixels])
        return out

    def image(self, palette=1):
        rgba = self.palettes[palette]
        indices = Image.frombytes('P', (self.width, self.height), bytes(self.indices()))
        indices.putpalette(bytes(rgba[i + c] for i in range(0, 64, 4) for c in range(3)))
        indices.info['transparency'] = bytes(rgba[3::4])
        return indices.convert('RGBA')

    def cell(self, index, palette=1):
        x, y = index % 128 * 32, index // 128 * 32
        return self.image(palette).crop((x, y, x + 32, y + 32))

    def blank_cells(self):
        image = self.image(0).getchannel('A')
        return {i for i in range(4480) if image.crop(
            (i % 128 * 32, i // 128 * 32, i % 128 * 32 + 32, i // 128 * 32 + 32)).getbbox() is None}

    def replace(self, coverage_by_index):
        out = bytearray(self.data)
        alphas = self.palettes[1][3::4]
        lut = [min(range(16), key=lambda i: abs(alphas[i] - v)) for v in range(256)]
        for index, coverage in coverage_by_index.items():
            require(0 <= index < 4480 and len(coverage) == 1024, 'Invalid font cell')
            x0, y0 = index % 128 * 32, index // 128 * 32
            for y in range(32):
                start = 64 + ((y0 + y) * self.width + x0) // 2
                for x in range(0, 32, 2):
                    out[start + x // 2] = lut[coverage[y * 32 + x]] | (lut[coverage[y * 32 + x + 1]] << 4)
        require(out[:64] == self.data[:64] and out[-128:] == self.data[-128:], 'Font metadata changed')
        return bytes(out)


def index_for_code(code):
    # Flat SJIS grid: checked against the Vita atlas's punctuation/Latin anchors.
    return ((code >> 8) - 0x81) * 192 + ((code & 255) - 0x40)


def unused_codes(pages):
    blanks = set.intersection(*(p.blank_cells() for p in pages))
    result = []
    for hi in range(0x81, 0x89):
        for lo in range(0x40, 0xFD):
            if lo == 0x7F:
                continue
            code = hi * 256 + lo
            try:
                bytes([hi, lo]).decode('cp932')
            except UnicodeDecodeError:
                if index_for_code(code) in blanks:
                    result.append(code)
    return result
