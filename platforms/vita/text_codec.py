"""Adaptive Latin pairs in blank Vita font cells; original controls pass through.

Dictionary segmentation is dynamic, not a fixed even/odd split. Rare letters
fall back to single-letter cells; this preserves Japanese and stays in the
488 unassigned blank cells of the inspected Vita font.
"""
from collections import Counter
from functools import lru_cache
import re

CONTROL = re.compile(r'\$[A-Za-z]')


def runs(line):
    result, run = [], ''
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '$':
            if not CONTROL.match(line, i):
                raise ValueError('Unrecognized dollar control')
            if run:
                result.append(('latin', run))
                run = ''
            result.append(('control', line[i:i + 2]))
            i += 2
            continue
        if 32 <= ord(ch) <= 126:
            run += ch
        else:
            if run:
                result.append(('latin', run))
                run = ''
            if len(ch.encode('cp932')) != 2:
                raise ValueError('Unexpected non-double-byte character')
            result.append(('raw', ch))
        i += 1
    if run:
        result.append(('latin', run))
    return result


def segment(text, dictionary):
    # Minimize cells, then singleton cells. Exact text reconstructs from tokens.
    best = [(0, 0, [])] * (len(text) + 1)
    for i in range(len(text) - 1, -1, -1):
        options = []
        for n in (2, 1):
            token = text[i:i + n]
            if len(token) == n and token in dictionary:
                cost, singles, tail = best[i + n]
                options.append((cost + 1, singles + (n == 1), [token] + tail))
        if not options:
            raise ValueError('No glyph encoding for Latin text')
        best[i] = min(options, key=lambda item: item[:2])
    return best[0][2]


def dictionary_for(texts, codes):
    pieces = [part for text in texts for line in text.replace('\r\n', '\n').split('\n')
              for kind, part in runs(line) if kind == 'latin']
    singles = sorted(set(''.join(pieces)))
    frequencies = Counter(part[i:i + 2] for part in pieces for i in range(len(part) - 1))
    tokens = singles + [p for p, count in sorted(frequencies.items(), key=lambda item: (-item[1], item[0]))
                        ][:len(codes) - len(singles)]
    if len(singles) > len(codes):
        raise ValueError('Insufficient unused font cells')
    return dict(zip(tokens, codes))


def encode(text, mapping):
    encoded = []
    costs = []
    for line in text.replace('\r\n', '\n').split('\n'):
        out, cost = bytearray(), 0
        for kind, part in runs(line):
            if kind == 'latin':
                tokens = segment(part, mapping)
                for token in tokens:
                    out.extend(mapping[token].to_bytes(2, 'big'))
                cost += len(tokens)
            else:
                # Platform font plans may bind semantic one-cell UI labels.
                # Keep each as one cell rather than expanding Latin letters
                # and breaking the original status-bit/color indexing.
                out.extend(mapping[part].to_bytes(2,'big') if part in mapping else part.encode('cp932'))
                cost += 6 if kind == 'control' else (0 if part in '《》' else 1)
        encoded.append(bytes(out))
        costs.append(cost)
    return b'\r\n'.join(encoded), costs


def decode(data, mapping):
    reverse = {code: token for token, code in mapping.items()}
    result, i = [], 0
    while i < len(data):
        if data[i:i + 2] == b'\r\n':
            result.append('\n')
            i += 2
        elif data[i:i + 1] == b'$':
            result.append(data[i:i + 2].decode('ascii'))
            i += 2
        else:
            code = int.from_bytes(data[i:i + 2], 'big')
            result.append(reverse[code] if code in reverse else data[i:i + 2].decode('cp932'))
            i += 2
    return ''.join(result)
