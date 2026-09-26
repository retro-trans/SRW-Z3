"""The stage narration containers: fixed 84-byte, NUL-padded text slots.

The opening crawl and the between-chapter text do not live in the Lua. They sit
in a sibling CPK member as an array of fixed-width records -- 0x54 bytes each,
NUL-padded, one line per slot. That makes them the friendliest text in the game
to translate: no offsets, no index, and 42 cells per line where a voice bark
gets 12.

The array's base offset is NOT the same in every member, so it is detected:
the right base is the one where the most slots begin just after a NUL. Assuming
one splits lines mid-sentence, which is what "界を創り上げた。" was.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cpk import CPK   # noqa: E402

STRIDE = 0x54
NUL = bytes((0,))


def _score(d, base):
    ok = 0
    p = base
    while p + STRIDE <= len(d):
        raw = d[p:p + STRIDE]
        t = raw.split(NUL)[0]
        if t:
            try:
                t.decode("cp932")
            except Exception:
                return -1
            if p == 0 or d[p - 1] == 0:
                ok += 1
            else:
                ok -= 1
        p += STRIDE
    return ok


def base_of(d):
    return max(range(STRIDE), key=lambda b: _score(d, b))


def slots(d, base=None):
    """[(offset, text)] for every non-empty slot."""
    base = base_of(d) if base is None else base
    out, p = [], base
    while p + STRIDE <= len(d):
        t = d[p:p + STRIDE].split(NUL)[0]
        if t:
            try:
                out.append((p, t.decode("cp932")))
            except Exception:
                pass
        p += STRIDE
    return out


def members(cpk_path):
    """[(member index, base, [(offset, text)])] for members that hold slots."""
    k = CPK(cpk_path)
    out = []
    for i, f in enumerate(k.files):
        d = k.read(f)
        if len(d) < 500:
            continue
        # A slot container is mostly padding -- 8,000 bytes carrying 28 short
        # lines is ~90% NUL. Lua source has almost none, and without this gate
        # the detector happily slices a .lua file into 84-byte "slots".
        if d.count(NUL) < len(d) * 0.5:
            continue
        b = base_of(d)
        s = slots(d, b)
        if len(s) >= 3 and sum(len(t) for _o, t in s) >= 40:
            out.append((i, b, s))
    return out


def capacity(d, base=None):
    """Text bytes a record can hold -- MEASURED, not derived.

    Two wrong answers came first, and the game rejected both by crashing.

    The 84-byte stride is not the budget: records carry fields past the string
    (+64 and +77 in STG0001A member 6). Deriving the ceiling from where those
    fields start gives 63 bytes, and that crashed too -- so the text field is
    smaller than the gap to the next non-zero byte, and nothing in the file
    says where it ends.

    What is verifiable is what the game itself writes. The longest string in
    the container is a length it demonstrably handles; a build capped at each
    record's own original length rendered correctly on hardware. So the bound
    is the maximum the container already uses. Conservative by construction,
    and unlike the two derivations it is evidence rather than inference.
    """
    base = base_of(d) if base is None else base
    longest, p = 0, base
    while p + STRIDE <= len(d):
        t = d[p:p + STRIDE].split(NUL)[0]
        if t:
            longest = max(longest, len(t))
        p += STRIDE
    return longest


def apply(d, lines, mapping, idx=None, cap=None):
    """Write English into the slots. In place: no offset moves, no growth.

    Two rules, both learned the hard way:

    * never write past `capacity()`, which is where record fields begin
    * never zero-fill the remainder. The old version padded the whole record
      with NULs and erased the 0x0d / 0xd2 fields of the two records that use
      them. A string ends at its first NUL, so leftover bytes are already
      harmless -- overwriting them is pure risk.
    """
    import digraph as dg
    cap = capacity(d) if cap is None else cap
    out = bytearray(d)
    done = []
    for row in lines:
        en = row["en"]
        if idx is not None:
            import terms as T
            en = T.expand(en, idx, where="narration")
        enc = dg.encode_mixed(en, mapping, newline=bytes((10,)))
        if len(enc) + 1 > cap + 1:
            raise SystemExit("%#06x: %r encodes to %d bytes, text field holds %d"
                             % (row["off"], en, len(enc), cap))
        off = row["off"]
        out[off:off + len(enc)] = enc
        out[off + len(enc)] = 0            # terminate, touch nothing beyond
        done.append((off, len(enc)))
    return bytes(out), done


def verify(old, new, done):
    """Re-derived from the two blobs, not from what apply() decided."""
    problems = []
    if len(new) != len(old):
        problems.append("size changed: %d -> %d" % (len(old), len(new)))
    spans = [(o, o + n + 1) for o, n in done]   # text plus its terminator
    for i in range(min(len(old), len(new))):
        if old[i] != new[i] and not any(a <= i < b for a, b in spans):
            problems.append("byte %#x changed outside every slot" % i)
            break
    return problems


def main(argv):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    if len(argv) < 2:
        print(__doc__.strip())
        return 2
    for i, b, s in members(argv[1]):
        print("member %d  base %#x  %d slots" % (i, b, len(s)))
        for off, t in s:
            print("   %#06x  [%2d]  %s" % (off, len(t), t))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
