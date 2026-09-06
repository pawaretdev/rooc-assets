"""index.html for the HotUpdate extraction, grouped by asset-name prefix."""
import os, json, collections

OUT = r"C:\Users\pawar\rooc-assets\hotupdate"
man = json.load(open(os.path.join(OUT, "manifest.json"), encoding="utf-8"))


def tokens(n):
    return n.replace("-", "_").split("_")


def fine(n):
    p = tokens(n)
    if p[0].lower() in ("ui", "fx") and len(p) > 1:
        return f"{p[0].upper()}_{p[1]}"
    return p[0]


def coarse(n):
    return tokens(n)[0]


def canon(labels):
    by = collections.defaultdict(collections.Counter)
    for l in labels:
        by[l.lower()][l] += 1
    return {k: v.most_common(1)[0][0] for k, v in by.items()}


names = [m["name"] for m in man]
FC, CC = canon(fine(n) for n in names), canon(coarse(n) for n in names)
fc = collections.Counter(fine(n).lower() for n in names)
big_fine = {g for g, c in fc.most_common(30) if c >= 25}
cc = collections.Counter(coarse(n).lower() for n in names if fine(n).lower() not in big_fine)
big_coarse = {g for g, c in cc.most_common(10) if c >= 25}


def group_of(n):
    g = fine(n).lower()
    if g in big_fine:
        return FC[g]
    c = coarse(n).lower()
    return CC[c] if c in big_coarse else "Other"


rows = [{"f": m["file"], "n": m["name"], "b": m["bundle"], "t": m["type"],
         "d": f'{m["w"]}\u00d7{m["h"]}', "g": group_of(m["name"])} for m in man]
gc = collections.Counter(r["g"] for r in rows)
groups = sorted(gc, key=lambda g: (g == "Other", -gc[g], g))
print(f"{len(rows)} images, {len(groups)} groups")
for g in groups:
    print(f"  {gc[g]:>5}  {g}")

HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>ROOC HotUpdate</title>
<style>
:root{--bg:#12151c;--card:#1b202b;--line:#2a3140;--fg:#e8ecf4;--dim:#98a2b8;--acc:#f0b429}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 "Segoe UI",system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(18,21,28,.97);
       border-bottom:1px solid var(--line);padding:14px 22px;backdrop-filter:blur(8px)}
h1{margin:0;font-size:17px}
.sub{color:var(--dim);font-size:13px;margin-top:2px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;align-items:center}
input{background:var(--card);border:1px solid var(--line);color:var(--fg);padding:8px 12px;
      border-radius:7px;min-width:300px;font-size:14px}
input:focus{outline:2px solid var(--acc);outline-offset:-1px}
button{background:var(--card);border:1px solid var(--line);color:var(--dim);padding:6px 12px;
       border-radius:7px;cursor:pointer;font-size:12.5px}
button.on{background:var(--acc);border-color:var(--acc);color:#12151c;font-weight:600}
#count{color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums;white-space:nowrap}
#tabs{display:flex;gap:6px;flex-wrap:wrap}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:12px;padding:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.card:hover{border-color:var(--acc)}
.card a{display:block;background:
  linear-gradient(45deg,#191d26 25%,transparent 25%,transparent 75%,#191d26 75%) 0 0/16px 16px,
  linear-gradient(45deg,#191d26 25%,transparent 25%,transparent 75%,#191d26 75%) 8px 8px/16px 16px,
  #0f1319;aspect-ratio:1;padding:8px}
.card img{width:100%;height:100%;object-fit:contain;display:block}
.meta{padding:5px 8px;border-top:1px solid var(--line)}
.fn{font-size:10.5px;font-family:Consolas,monospace;word-break:break-all;line-height:1.35}
.dm{color:var(--dim);font-size:10px;margin-top:2px}
</style>
<header>
  <h1>ROOC — HotUpdate patch assets</h1>
  <div class="sub">__N__ images from the game's <code>StreamingAssets/HotUpdate</code> —
    content patched in after the base install, so none of it is in the AssetBundles dump.</div>
  <div class="controls"><input id="q" placeholder="ค้นหาชื่อ asset หรือ bundle hash…" autofocus>
    <span id="count"></span></div>
  <div class="controls"><span id="tabs"></span></div>
</header>
<div class="grid" id="grid"></div>
<script>
const rows=__DATA__, groups=__GROUPS__;
let g="All", q="", LIMIT=400;
const tabs=document.getElementById("tabs");
["All",...groups].forEach(c=>{const b=document.createElement("button");
  const n=c==="All"?rows.length:rows.filter(r=>r.g===c).length;
  b.textContent=c+" ("+n+")";b.dataset.g=c;b.onclick=()=>{g=c;LIMIT=400;draw();};tabs.appendChild(b);});
function draw(){
  const t=q.trim().toLowerCase();
  const list=rows.filter(r=>(g==="All"||r.g===g)&&
    (!t||r.n.toLowerCase().includes(t)||r.b.toLowerCase().includes(t)));
  const shown=list.slice(0,LIMIT);
  document.getElementById("count").textContent=
    shown.length+" / "+list.length+(list.length>shown.length?"  · scroll for more":"");
  [...tabs.children].forEach(b=>b.classList.toggle("on",b.dataset.g===g));
  document.getElementById("grid").innerHTML=shown.map(r=>
    `<div class="card"><a href="images/${encodeURIComponent(r.f)}" target="_blank">
      <img loading="lazy" src="images/${encodeURIComponent(r.f)}" alt=""></a>
      <div class="meta"><div class="fn">${r.n}</div>
      <div class="dm">${r.d} · ${r.t} · ${r.b}</div></div></div>`).join("");
}
addEventListener("scroll",()=>{ if(innerHeight+scrollY>document.body.offsetHeight-700){
  const b=LIMIT; LIMIT+=400; if(b!==LIMIT) draw(); }});
document.getElementById("q").oninput=e=>{q=e.target.value;LIMIT=400;draw();};
draw();
</script>
"""
dest = os.path.join(OUT, "index.html")
with open(dest, "w", encoding="utf-8") as fh:
    fh.write(HTML.replace("__DATA__", json.dumps(rows, ensure_ascii=False))
                 .replace("__GROUPS__", json.dumps(groups, ensure_ascii=False))
                 .replace("__N__", f"{len(rows):,}"))
print("->", dest)
