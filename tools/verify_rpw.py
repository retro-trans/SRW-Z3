"""Re-parse the BUILT RPW_DATA from scratch, at the byte level.

Nothing here consults build_grown's repoint map -- that is the point. If the
writer repointed something wrongly, the only way to see it is to follow the
record pointers in the result the way the game does.

The invariant is COMPARATIVE, not absolute. pointer_columns is a heuristic, so
some chunks resolve at 90% by luck rather than by being pointer columns at all;
demanding 100% would flag those forever. What must hold is that no chunk
resolves WORSE after the rewrite than before it. That is exactly the failure
that caused the Genion crash -- three coincidental matches in ridividx /
ridwpidx left a robot record unconstructible.
"""
import collections, io, json, os, struct, sys
os.chdir(r"E:\Projects\SRW Z3"); sys.path.insert(0,'tools')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import digraph as dg, rpw
dg.use_letters('E:/RPCS3/dev_flash/data/font/SCE-PS3-RD-B-LATIN.TTF', cap=22, dilate=0.5)
from cpk import CPK

def load(p):
    k = CPK(p); return k.read(k.files[0])
def parts(b):
    for name, s, o, foot, end in rpw.chunks(b):
        if name == "j-string":
            return b[o:foot].split(b"\0"), o
    raise ValueError
def starts_of(b):
    ps, _o = parts(b); st = [0]   # offsets are BODY-relative, not absolute
    for x in ps[:-1]: st.append(st[-1] + len(x) + 1)
    return ps, {v: i for i, v in enumerate(st)}

old, new = load('work/lib/RPW_DATA.CPK'), load('work/out/RPW_DATA.CPK')
po, ao = starts_of(old); pn, an = starts_of(new)
print('j-string parts: %d -> %d  (+%d appended)' % (len(po), len(pn), len(pn)-len(po)))
same = sum(1 for i in range(min(len(po), len(pn))) if po[i] == pn[i])
print('  unchanged: %d   swapped in place: %d' % (same, min(len(po), len(pn)) - same))
print('  originals blanked to empty (ordinal drift): %d  (must be 0)'
      % sum(1 for i in range(len(po)) if i < len(pn) and po[i] and not pn[i]))

cols = rpw.pointer_columns(old)
def rate(b, at, name, stride, phis):
    ch = {c[0]: c for c in rpw.chunks(b)}[name]
    n = ((ch[3] - ch[2]) // 4) // stride
    ok = tot = 0
    for r in range(n):
        for p in phis:
            v = struct.unpack_from('<I', b, ch[2] + 4*(r*stride+p))[0]
            tot += 1; ok += v in at
    return ok, tot

print()
print('  %-10s %8s %8s' % ('chunk', 'before', 'after'))
worse = []
for name in sorted(cols):
    stride, phis = cols[name]
    if not stride or not phis: continue
    a, at_ = rate(old, ao, name, stride, phis)
    b_, bt = rate(new, an, name, stride, phis)
    ra, rb = a/at_, b_/bt
    flag = ''
    if rb < ra - 1e-9:
        worse.append((name, ra, rb)); flag = '  <-- REGRESSED'
    print('  %-10s %7.2f%% %7.2f%%%s' % (name, ra*100, rb*100, flag))
print()
print('chunks that resolve worse after the rewrite: %d  (must be 0)' % len(worse))

weps = json.load(open('translation/weapons.json', encoding='utf-8'))
mp = 'work/out/pairs.json'
enc = set()
if os.path.exists(mp):
    m = json.load(open(mp, encoding='utf-8'))
    m = {(k if len(k) == 1 else (k[0], k[1])): v for k, v in m.items()}
    for v in weps.values():
        try: enc.add(dg.encode_mixed(v, m, newline=bytes((10,))))
        except Exception: pass
# in-place swaps pad the slot's slack with 0x8140 (fullwidth space) so no
# ordinal moves; strip it before comparing or every padded name reads absent
FILL = bytes((0x81, 0x40))
def unpad(x):
    while x.endswith(FILL): x = x[:-2]
    return x
body = {unpad(x) for x in pn}
# the denominator is DISTINCT English: 11 Japanese names share one form
# (ガトリングガン and ガトリング・ガン are both "Gatling Gun"), so 477 was
# never the number to expect here.
print('weapon names found in the built string body: %d of %d distinct'
      % (sum(1 for e in enc if e in body), len(enc)))
stride, _ = cols['weapon']
ch = {c[0]: c for c in rpw.chunks(new)}['weapon']
n = ((ch[3]-ch[2])//4)//stride
c = collections.Counter()
for r in range(n):
    for p in (3, 4):
        v = struct.unpack_from('<I', new, ch[2]+4*(r*stride+p))[0]
        i = an.get(v)
        if i is not None: c['en' if unpad(pn[i]) in enc else 'jp'] += 1
print('weapon name slots pointing at English: %d of %d' % (c['en'], c['en']+c['jp']))
