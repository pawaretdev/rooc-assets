"""Build a browsable index of the extracted item icons."""
import os, json

OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Items"

GROUP = [
    ("Consumables", lambda d: d.startswith("Icon_ItemConsumables")),
    ("Equipment",   lambda d: d.startswith("Icon_ItemEquip")),
    ("Materials",   lambda d: d.startswith("Icon_ItemMaterial")),
    ("Headwear",    lambda d: d.startswith("Icon_ItemHeadwear")),
    ("Costume",     lambda d: d.startswith("Icon_Wear_")),
    ("Vehicles",    lambda d: d.startswith("Icon_Vehicles")),
    ("Atlas sheets", lambda d: d.startswith("_Atlas_")),
]


def group_of(d):
    for name, test in GROUP:
        if test(d):
            return name
    return "Other"


rows = []
for d in sorted(os.listdir(OUT)):
    sub = os.path.join(OUT, d)
    if not os.path.isdir(sub) or d.startswith("_tools"):
        continue
    for f in sorted(os.listdir(sub)):
        if f.lower().endswith(".png"):
            rows.append({"d": d, "f": f, "g": group_of(d)})

groups = sorted({r["g"] for r in rows})
print(f"{len(rows)} icons across {len({r['d'] for r in rows})} folders")

HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>ROOC Item Icons</title>
<style>
:root{--bg:#12151c;--card:#1b202b;--line:#2a3140;--fg:#e8ecf4;--dim:#98a2b8;--acc:#f0b429}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 "Segoe UI",system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(18,21,28,.96);
       border-bottom:1px solid var(--line);padding:14px 22px;backdrop-filter:blur(8px)}
h1{margin:0;font-size:17px}
.sub{color:var(--dim);font-size:13px;margin-top:2px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;align-items:center}
input{background:var(--card);border:1px solid var(--line);color:var(--fg);padding:8px 12px;
      border-radius:7px;min-width:280px;font-size:14px}
input:focus{outline:2px solid var(--acc);outline-offset:-1px}
button{background:var(--card);border:1px solid var(--line);color:var(--dim);padding:7px 13px;
       border-radius:7px;cursor:pointer;font-size:13px}
button.on{background:var(--acc);border-color:var(--acc);color:#12151c;font-weight:600}
#count{color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:11px;padding:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;overflow:hidden}
.card:hover{border-color:var(--acc)}
.card a{display:block;background:#0d1016;aspect-ratio:1;padding:7px}
.card img{width:100%;height:100%;object-fit:contain;display:block;image-rendering:auto}
.fn{padding:5px 7px;border-top:1px solid var(--line);color:var(--dim);font-size:10px;
    font-family:Consolas,monospace;word-break:break-all;line-height:1.35}
</style>
<header>
  <h1>ROOC — Item Icons</h1>
  <div class="sub">__N__ icons extracted from the game's asset bundles.</div>
  <div class="controls">
    <input id="q" placeholder="ค้นหาชื่อไฟล์…" autofocus>
    <span id="tabs"></span><span id="count"></span>
  </div>
</header>
<div class="grid" id="grid"></div>
<script>
const rows = __DATA__, groups = __GROUPS__;
let g="All", q="", LIMIT=600;
const tabs=document.getElementById("tabs");
["All",...groups].forEach(c=>{const b=document.createElement("button");
  b.textContent=c;b.dataset.g=c;b.onclick=()=>{g=c;LIMIT=600;draw();};tabs.appendChild(b);});
function draw(){
  const t=q.trim().toLowerCase();
  const list=rows.filter(r=>(g==="All"||r.g===g)&&(!t||r.f.toLowerCase().includes(t)));
  const shown=list.slice(0,LIMIT);
  document.getElementById("count").textContent=
    shown.length+" / "+list.length+(list.length>shown.length?"  (scroll for more)":"");
  [...tabs.children].forEach(b=>b.classList.toggle("on",b.dataset.g===g));
  document.getElementById("grid").innerHTML=shown.map(r=>
    `<div class="card"><a href="${r.d}/${r.f}" target="_blank">
       <img loading="lazy" src="${r.d}/${r.f}" alt=""></a>
     <div class="fn">${r.f.replace(/\.png$/,"")}</div></div>`).join("");
}
addEventListener("scroll",()=>{ if(innerHeight+scrollY>document.body.offsetHeight-600){
  const before=LIMIT; LIMIT+=600; if(before!==LIMIT) draw(); }});
document.getElementById("q").oninput=e=>{q=e.target.value;LIMIT=600;draw();};
draw();
</script>
"""
dest = os.path.join(OUT, "ItemIndex.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(HTML.replace("__DATA__", json.dumps(rows, ensure_ascii=False))
                .replace("__GROUPS__", json.dumps(groups))
                .replace("__N__", f"{len(rows):,}"))
print("->", dest)
