"""pilot -> voice sections, by composing three links.

    section -> mech    inference from call-outs (srvc_link, 3 controls pass)
    mech    -> pilot   the zukan's own PLTN field -- the game's statement
    section ~ section  sections sharing >=50% of their lines share a pilot

The third is structural and independent of both others: it is what shows Black
Ox and Tetsujin 28 are one voice set (89 identical lines) without knowing any
name at all.
"""
import io, json, os, sys, collections
os.chdir(r"E:\Projects\SRW Z3"); sys.path.insert(0,'tools')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import srvc_link as S, mech_pilot

def norm(x):
    return (x or "").replace("\u3000", "").replace(" ", "").strip()

mp = {norm(k): v for k, v in mech_pilot.pairs().items()}
b = open(S.SRVC, 'rb').read()
d = json.load(open('work/voice/sections.json', encoding='utf-8'))
sets = []
for x in d:
    ts = set(S.strings(b, {'index': x['index'], 'count': x['count'], 'pool': x['pool']}))
    sets.append({t for t in ts if len(t) >= 6})

par = list(range(len(d)))
def find(x):
    while par[x] != x: par[x] = par[par[x]]; x = par[x]
    return x
for i in range(len(d)):
    for j in range(i+1, len(d)):
        a, c = sets[i], sets[j]
        if a and c and len(a & c) / min(len(a), len(c)) >= 0.5:
            ra, rc = find(i), find(j)
            if ra != rc: par[ra] = rc

def pilot_of(x):
    if not x['unit']: return None
    for f in x['unit'].split(' / '):
        p = mp.get(norm(f))
        if p and p not in ('\uff0d\uff0d\uff0d', '-', '\u2015'):
            return p
    return None

# a cluster inherits a name if ANY of its sections has one
cl = collections.defaultdict(list)
for i in range(len(d)): cl[find(i)].append(i)
named = 0
rows = []
for root, mem in cl.items():
    names = [p for p in (pilot_of(d[i]) for i in mem) if p]
    who = collections.Counter(names).most_common(1)[0][0] if names else None
    if who: named += len(mem)
    rows.append((who, [d[i]['sec'] for i in mem],
                 sorted({d[i]['unit'] for i in mem if d[i]['unit']})))
print('sections: %d   clusters: %d' % (len(d), len(cl)))
print('sections with a named pilot: %d' % named)
print('distinct pilots: %d' % len({r[0] for r in rows if r[0]}))
print()
print('clusters covering more than one section (a pilot with several machines):')
for who, secs, units in sorted((r for r in rows if len(r[1]) > 1),
                               key=lambda r: -len(r[1]))[:10]:
    print('   %-14s secs %-22s %s'
          % (who or '(unnamed)', str(secs)[:22], ', '.join(u[:20] for u in units[:3])))
json.dump([{'pilot': w, 'sections': s, 'units': u} for w, s, u in rows],
          open('work/voice/pilots.json','w',encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('-> work/voice/pilots.json')
