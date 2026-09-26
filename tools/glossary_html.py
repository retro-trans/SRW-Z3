"""Render the glossary as a single self-contained HTML reference.

One row per term: Japanese, English, and the SOURCE OF THE CLAIM. That last
column is the point of the page, and it is derived rather than read from a
field, because `src` alone would mislead -- a term can be verified against
akurasu and carry no stamp if it came in through a patch that dropped it.

Provenance tiers, strongest first:

    akurasu    a real external citation; the akurasu path is shown verbatim
    official   a hand-set english name for an established anime term, with no
               web citation recorded -- known, but take it on trust
    batch      produced by a translation subagent from series knowledge; not
               independently checked
    proposed   our own coinage, awaiting review

Ambiguous terms (two people sharing an english name) and aliases (one thing
spelled two ways in the game) are marked so a reader never treats either as a
global rename.

The library batch modules (`translation/library/*.json`) carry a NAMES map
of their own. Most of it agrees with the glossary, but a few names were
only ever written there, and a few disagree -- usually because the batch
romanised the katakana (Ruunamaria) where the glossary has the real name
(Lunamaria). Both belong on this page: the first as `library` rows, the
second as a flag on the glossary row. The glossary is what SHIPS -- the
library build reads its names from there -- so a disagreement is shown,
never resolved here.

    python tools/glossary_html.py <glossary.json> <out.html> [--library DIR]
"""
import html
import json
import os
import sys
from collections import Counter


LIB_KIND = {"kw": "keyword", "pt": "pilot", "rt": "robot"}


def library_names(directory):
    """{japanese: (english, kind)} from every library batch module."""
    out = {}
    if not directory or not os.path.isdir(directory):
        return out
    for fn in sorted(os.listdir(directory)):
        pre = fn.split("_")[0]
        if not fn.endswith(".json") or pre not in LIB_KIND:
            continue
        d = json.load(open(os.path.join(directory, fn), encoding="utf-8"))
        for jp, en in d.get("NAMES", {}).items():
            out.setdefault(jp, (en, LIB_KIND[pre]))
    return out


def provenance(t):
    """(tier, citation). A citation is any real URL, not just an akurasu
    path -- the verification pass cited fandom wikis and Wikipedia too, and a
    term checked against the Gundam Wiki with a URL is exactly as verified as
    one checked against akurasu. Showing it as "uncited" would be false."""
    s = t.get("src", "")
    if s.startswith("akurasu:"):
        return "akurasu", "https://akurasu.net/wiki/" + s.split(":", 1)[1].split(" ")[0]
    if s.startswith("http://") or s.startswith("https://"):
        return "cited", s
    if t["status"] == "official" and t["kind"] == "series":
        return "akurasu", "https://akurasu.net/wiki/Super_Robot_Wars/Z3/Series"
    if t["status"] == "official":
        return "official", ""
    if s == "subagent batch":
        return "batch", ""
    return "proposed", ""


TIER_LABEL = {
    "akurasu": "Verified on akurasu",
    "cited": "Verified, wiki cited",
    "official": "Official name, uncited",
    "batch": "Subagent, unchecked",
    "proposed": "Proposed, under review",
    "library": "Library batch only",
}
KIND_LABEL = {"series": "Series", "keyword": "Keyword", "pilot": "Pilot", "robot": "Unit"}
KIND_ORDER = ["keyword", "pilot", "robot", "series"]


def build(g, lib=None):
    lib = lib or {}
    known = {t["jp"] for t in g["terms"]}
    # names the library batches wrote that the glossary never recorded
    extra = [{"jp": jp, "en": en, "kind": kind,
              "status": "library", "src": "library batch",
              "note": "written in a library batch module; not recorded in the glossary"}
             for jp, (en, kind) in sorted(lib.items()) if jp not in known]
    terms = sorted(list(g["terms"]) + extra,
                   key=lambda t: (KIND_ORDER.index(t["kind"]), t["jp"]))
    tiers = Counter(provenance(t)[0] for t in terms)
    kinds = Counter(t["kind"] for t in terms)
    rows = []
    for t in terms:
        tier, path = provenance(t)
        if t.get("status") == "library":
            tier, path = "library", ""
        flags = []
        # a Japanese name can name two different people (レイ is Ray Lovelock
        # and Rei Ayanami), so the batch only disagrees if it matches NEITHER
        all_en = {x["en"] for x in g["terms"] if x["jp"] == t["jp"] and x["en"]}
        other = lib.get(t["jp"], (None, None))[0]
        if other in all_en:
            other = None
        if other and t.get("en") and other != t["en"] and t.get("status") != "library":
            flags.append(
                '<span class="flag flag-lib" title="%s">library: %s</span>'
                % (html.escape('the library batch module renders this name differently; '
                               'the glossary is what ships', quote=True),
                   html.escape(other)))
        if t["status"] == "ambiguous":
            flags.append('<span class="flag flag-amb" title="%s">ambiguous</span>'
                         % html.escape(t.get("note", ""), quote=True))
        if t.get("alias"):
            flags.append('<span class="flag flag-alias" title="%s">alias</span>'
                         % html.escape(t.get("note", ""), quote=True))
        note = t.get("note", "")
        src_html = ('<a href="%s">%s</a>'
                    % (html.escape(path, quote=True),
                       html.escape(path.replace("https://", "").replace("http://", "")))) if path else ""
        rows.append(
            '<tr data-kind="%s" data-tier="%s" data-q="%s">'
            '<td class="jp" lang="ja">%s</td>'
            '<td class="en">%s%s</td>'
            '<td class="kind">%s</td>'
            '<td class="src"><span class="tier tier-%s"></span>'
            '<span class="tier-name">%s</span>%s%s</td>'
            '</tr>'
            % (t["kind"], tier,
               html.escape((t["jp"] + " " + t["en"]).lower(), quote=True),
               html.escape(t["jp"]),
               html.escape(t["en"]), (" " + " ".join(flags)) if flags else "",
               KIND_LABEL[t["kind"]],
               tier, TIER_LABEL[tier],
               ('<span class="path">%s</span>' % src_html) if src_html else "",
               ('<span class="note">%s</span>' % html.escape(note)) if note else ""))

    tier_pills = "".join(
        '<button class="pill" data-filter-tier="%s" type="button">'
        '<span class="tier tier-%s"></span>%s <b>%d</b></button>'
        % (k, k, TIER_LABEL[k], tiers[k])
        for k in ("akurasu", "cited", "official", "batch", "proposed", "library") if tiers[k])
    kind_pills = "".join(
        '<button class="pill" data-filter-kind="%s" type="button">%s <b>%d</b></button>'
        % (k, KIND_LABEL[k], kinds[k]) for k in KIND_ORDER)

    return TEMPLATE.replace("{{ROWS}}", "\n".join(rows)) \
                   .replace("{{TOTAL}}", str(len(terms))) \
                   .replace("{{TIERS}}", tier_pills) \
                   .replace("{{KINDS}}", kind_pills) \
                   .replace("{{VERIFIED}}", str(tiers["akurasu"] + tiers["cited"]))


TEMPLATE = r"""<title>SRW Z3 Glossary</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&family=Source+Sans+3:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400&display=swap">
<style>
:root{
  --bg:#f5f6f8; --surface:#ffffff; --ink:#1c2333; --ink-2:#4b5566; --ink-3:#7a8394;
  --rule:#dde1e8; --rule-2:#eceff3; --accent:#3b5b8c; --accent-ink:#ffffff;
  --row-hover:#eef2f8; --sticky:#f5f6f8f2;
  --t-akurasu:#2e7d4f; --t-cited:#1f7a72; --t-official:#2f5f9e; --t-batch:#9a6b1a; --t-proposed:#6b7280;
  --t-library:#7a4f9a; --lib-bg:#f0e9f7; --lib-ink:#5c3a78;
  --amb-bg:#fbe9e7; --amb-ink:#8a2f24; --alias-bg:#e8eef8; --alias-ink:#2f4f7f;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#12161e; --surface:#181d27; --ink:#e6e9ef; --ink-2:#aab2c0; --ink-3:#7f8898;
    --rule:#2a3140; --rule-2:#222835; --accent:#8fb0e0; --accent-ink:#0f1520;
    --row-hover:#1f2633; --sticky:#12161ef2;
    --t-akurasu:#5ec48c; --t-cited:#5fc7bd; --t-official:#7fa8e6; --t-batch:#d9a441; --t-proposed:#8b95a6;
    --t-library:#c08fe0; --lib-bg:#3a2b4a; --lib-ink:#dcc4f0;
    --amb-bg:#3a1f1c; --amb-ink:#f0a59a; --alias-bg:#1e2a3d; --alias-ink:#a9c4ec;
  }
}
:root[data-theme="dark"]{
  --bg:#12161e; --surface:#181d27; --ink:#e6e9ef; --ink-2:#aab2c0; --ink-3:#7f8898;
  --rule:#2a3140; --rule-2:#222835; --accent:#8fb0e0; --accent-ink:#0f1520;
  --row-hover:#1f2633; --sticky:#12161ef2;
  --t-akurasu:#5ec48c; --t-cited:#5fc7bd; --t-official:#7fa8e6; --t-batch:#d9a441; --t-proposed:#8b95a6;
  --amb-bg:#3a1f1c; --amb-ink:#f0a59a; --alias-bg:#1e2a3d; --alias-ink:#a9c4ec;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"Source Sans 3","Segoe UI",system-ui,sans-serif;font-size:15px;line-height:1.45}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px 64px}
header{padding:36px 0 18px}
h1{margin:0;font-size:26px;font-weight:600;letter-spacing:-.01em;text-wrap:balance}
h1 .ja{font-family:"Noto Sans JP",sans-serif;font-weight:500;color:var(--ink-2);margin-left:10px;font-size:20px}
.lede{margin:8px 0 0;max-width:62ch;color:var(--ink-2)}
.lede b{color:var(--ink);font-weight:600}
.legend{margin:22px 0 0;display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px 22px;
  font-size:13.5px;color:var(--ink-2)}
.legend div{display:flex;gap:10px;align-items:flex-start;line-height:1.35}
.legend .tier{margin-top:5px;flex:none}
.legend b{color:var(--ink);font-weight:600;display:block}

.bar{position:sticky;top:0;z-index:5;background:var(--sticky);backdrop-filter:blur(6px);
  padding:12px 0;border-bottom:1px solid var(--rule);display:flex;flex-wrap:wrap;gap:10px 14px;align-items:center}
.search{flex:1 1 260px;min-width:200px;padding:9px 12px;font:inherit;color:var(--ink);
  background:var(--surface);border:1px solid var(--rule);border-radius:6px}
.search:focus{outline:2px solid var(--accent);outline-offset:1px}
.pills{display:flex;flex-wrap:wrap;gap:6px}
.pill{font:inherit;font-size:13px;padding:5px 10px;border-radius:999px;cursor:pointer;
  color:var(--ink-2);background:var(--surface);border:1px solid var(--rule);display:inline-flex;gap:6px;align-items:center}
.pill b{font-weight:600;color:var(--ink);font-variant-numeric:tabular-nums}
.pill[aria-pressed="true"]{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.pill[aria-pressed="true"] b{color:var(--accent-ink)}
.pill:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.count{font-size:13px;color:var(--ink-3);font-variant-numeric:tabular-nums;margin-left:auto}

.tier{display:inline-block;width:9px;height:9px;border-radius:50%;flex:none}
.tier-akurasu{background:var(--t-akurasu)} .tier-cited{background:var(--t-cited)} .tier-official{background:var(--t-official)}
.tier-batch{background:var(--t-batch)} .tier-proposed{background:var(--t-proposed)}
.tier-library{background:var(--t-library)}

.tablewrap{overflow-x:auto;margin-top:6px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
thead th{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--ink-3);font-weight:600;padding:12px 10px 8px;border-bottom:1px solid var(--rule);
  position:sticky;top:62px;background:var(--bg);z-index:4}
tbody td{padding:8px 10px;border-bottom:1px solid var(--rule-2);vertical-align:top}
tbody tr:hover td{background:var(--row-hover)}
tbody tr[hidden]{display:none}
.jp{font-family:"Noto Sans JP",sans-serif;font-weight:500;white-space:nowrap;min-width:180px}
.en{min-width:220px}
.kind{color:var(--ink-3);white-space:nowrap;font-size:13px}
.src{color:var(--ink-2);font-size:13.5px;min-width:260px}
.src .tier{margin-right:8px;vertical-align:1px}
.tier-name{white-space:nowrap}
.path{display:block;margin-top:2px;font-family:"JetBrains Mono",ui-monospace,monospace;font-size:12px}
.path a{color:var(--accent);text-decoration:none}
.path a:hover{text-decoration:underline}
.note{display:block;margin-top:3px;color:var(--ink-3);font-size:13px;font-style:italic;max-width:56ch}
.flag{font-size:11px;font-weight:600;letter-spacing:.04em;text-transform:uppercase;
  padding:1px 6px;border-radius:4px;vertical-align:1px;margin-left:6px;cursor:help}
.flag-amb{background:var(--amb-bg);color:var(--amb-ink)}
.flag-alias{background:var(--alias-bg);color:var(--alias-ink)}
.flag-lib{background:var(--lib-bg);color:var(--lib-ink)}
.empty{padding:40px 10px;color:var(--ink-3);text-align:center}
@media (prefers-reduced-motion:no-preference){.pill{transition:background .12s,color .12s}}
</style>

<div class="wrap">
<header>
  <h1>SRW Z3 Glossary <span class="ja" lang="ja">用語集</span></h1>
  <p class="lede"><b>{{TOTAL}} terms</b> from the game's own library — every keyword, pilot and unit — with the English form settled for this translation and, for each one, where that English came from. <b>{{VERIFIED}}</b> are cited to a real page (akurasu, a franchise wiki, or Wikipedia); the rest carry a weaker claim, and the colour says how much weaker.</p>
  <div class="legend">
    <div><span class="tier tier-akurasu"></span><span><b>Verified on akurasu</b>A real external citation. The wiki path is linked.</span></div>
    <div><span class="tier tier-cited"></span><span><b>Verified, wiki cited</b>Checked against the franchise wiki or Wikipedia. The page is linked.</span></div>
    <div><span class="tier tier-official"></span><span><b>Official name, uncited</b>A known English name for an established anime term, set by hand. No web citation was recorded.</span></div>
    <div><span class="tier tier-batch"></span><span><b>Subagent, unchecked</b>Produced by a translation agent from series knowledge. Not independently verified.</span></div>
    <div><span class="tier tier-library"></span><span><b>Library batch only</b>Written in a library batch module and never recorded in the glossary. A <span class="flag flag-lib">library: ...</span> flag marks a glossary row the batch renders differently; the glossary is what ships.</span></div>
    <div><span class="tier tier-proposed"></span><span><b>Proposed, under review</b>Our own coinage for an original term with no prior English.</span></div>
  </div>
</header>

<div class="bar">
  <input class="search" type="search" placeholder="Filter by Japanese or English…" aria-label="Filter terms" autocomplete="off">
  <div class="pills" role="group" aria-label="Filter by source">{{TIERS}}</div>
  <div class="pills" role="group" aria-label="Filter by kind">{{KINDS}}</div>
  <span class="count" id="count"></span>
</div>

<div class="tablewrap">
<table>
  <thead><tr><th>Japanese</th><th>English</th><th>Kind</th><th>Source of the claim</th></tr></thead>
  <tbody id="rows">
{{ROWS}}
  </tbody>
</table>
<div class="empty" id="empty" hidden>No terms match.</div>
</div>
</div>

<script>
(function(){
  var rows=[].slice.call(document.querySelectorAll('#rows tr'));
  var q=document.querySelector('.search'), count=document.getElementById('count'), empty=document.getElementById('empty');
  var tier=null, kind=null, total=rows.length;
  function apply(){
    var s=q.value.trim().toLowerCase(), n=0;
    rows.forEach(function(r){
      var ok=(!tier||r.dataset.tier===tier)&&(!kind||r.dataset.kind===kind)&&(!s||r.dataset.q.indexOf(s)>=0);
      r.hidden=!ok; if(ok)n++;
    });
    count.textContent=(n===total?total:n+' of '+total)+' terms';
    empty.hidden=n>0;
  }
  q.addEventListener('input',apply);
  document.querySelectorAll('.pill').forEach(function(p){
    p.setAttribute('aria-pressed','false');
    p.addEventListener('click',function(){
      var t=p.dataset.filterTier, k=p.dataset.filterKind;
      if(t!==undefined){ tier=(tier===t)?null:t; }
      if(k!==undefined){ kind=(kind===k)?null:k; }
      document.querySelectorAll('[data-filter-tier]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.filterTier===tier));});
      document.querySelectorAll('[data-filter-kind]').forEach(function(x){x.setAttribute('aria-pressed',String(x.dataset.filterKind===kind));});
      apply();
    });
  });
  try{ var saved=localStorage.getItem('srwz3-glossary-q'); if(saved){ q.value=saved; } }catch(e){}
  q.addEventListener('input',function(){ try{ localStorage.setItem('srwz3-glossary-q',q.value); }catch(e){} });
  apply();
})();
</script>
"""


def main(argv):
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    g = json.load(open(argv[1], encoding="utf-8"))
    libdir = argv[argv.index("--library") + 1] if "--library" in argv else \
        os.path.join(os.path.dirname(os.path.abspath(argv[1])), "..", "translation", "library")
    lib = library_names(libdir)
    out = build(g, lib)
    open(argv[2], "w", encoding="utf-8").write(out)
    known = {t["jp"] for t in g["terms"]}
    en_of = {}
    for t in g["terms"]:
        en_of.setdefault(t["jp"], set()).add(t["en"])
    added = sum(1 for jp in lib if jp not in known)
    differ = sum(1 for jp, (en, _k) in lib.items()
                 if en_of.get(jp) and en not in en_of[jp])
    print("%d glossary terms + %d library-only names -> %s (%d KB)"
          % (len(g["terms"]), added, argv[2], len(out.encode("utf-8")) // 1024))
    print("%d library names read; %d disagree with the glossary (flagged, not resolved)"
          % (len(lib), differ))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
