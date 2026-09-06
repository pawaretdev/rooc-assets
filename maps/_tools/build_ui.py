"""Enrich worldmap_cells.json with zone identities and emit a working demo UI."""
import json, io, os

OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps"

# id -> (English name, SceneMaps file stem or None)
# "screenshot" = read directly off the user's in-game capture; positions matched
# cell-for-cell against the prefab grid. Others left blank on purpose.
IDENT = {
    "55":  ("Glast Heim",          "sc_gucheng_001"),
    "54":  ("Glast Heim Outskirts", None),
    "10":  ("Northern Geffen",     "sc_jifenbeibu_001"),
    "17":  ("Garden",              "sc_huayuan_001"),
    "9":   ("Larva Canyon",        "sc_yuchongxiagu_001"),
    "53":  ("Geffen Field",        "sc_jifenkuangye_001"),
    "12":  ("Western Geffen",      "sc_jifenxibu_001"),
    "16":  ("Geffen",              "sc_jifen_001"),
    "23":  ("Eastern Geffen",      "sc_jifendongbu_001"),
    "56":  ("Kordt Forest",        "sc_ketesenlin_001"),
    "102": ("Bretonia",            "sc_bulunuosi_001"),
    "1":   ("Prontera West Gate",  "sc_ximen_001"),
    "7":   ("Prontera",            "sc_pulongdela_001"),
    "75":  ("Prontera East Gate",  "sc_dongmen_001"),
    "34":  ("Orc Village",         "sc_shourencunluo_001"),
    "8":   ("Goblin Forest",       "sc_gebulinsenlin_001"),
    "4":   ("Prontera South Gate", "sc_nanmen_001"),
    "21":  ("Izlude",              "sc_yisilude_001"),
    "11":  ("Desert Crossroad",    "sc_shamochadao_001"),
    "13":  ("Poring Island",       "sc_bolidao_001"),
    "25":  ("Western Morroc",      "sc_mlkxibu_001"),
    "26":  ("Morroc",              "sc_mengluoke_001"),
    "35":  ("Bridge of Desert",    "sc_shamozhiqiao_001"),
    "47":  ("Payon",               "sc_feiyang_001"),
    "36":  ("Eastern Payon",       "sc_feiyangdongbu_001"),
    "45":  ("Payon Forest",        "sc_feiyangshulin_001"),
}
CONFIRMED = set(IDENT)

src = os.path.join(OUT, "worldmap_cells.json")
data = json.load(io.open(src, encoding="utf-8"))

scene_dir = os.path.join(OUT, "SceneMaps")
have = {os.path.splitext(f)[0] for f in os.listdir(scene_dir)}

for panel, m in data["maps"].items():
    for c in m["cells"]:
        nm, scene = IDENT.get(c["id"], ("", None))
        c["name"] = nm
        c["scene_file"] = (f"SceneMaps/{scene}.png"
                           if scene and scene in have else None)
        c["identified_from"] = "in-game screenshot" if c["id"] in CONFIRMED else None

data["identification_note"] = (
    "Cell geometry comes from Resources/UI/Prefabs/WorldMap.prefab (exact). "
    "The 'name'/'scene_file' fields were matched by hand against an in-game "
    "screenshot and cover only part of the cells; the rest are left blank "
    "because the game's map-name string table is not in this asset dump."
)
with open(src, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)

cells = data["maps"]["Panel_DefaultWorldMap"]["cells"]
miao = data["maps"]["Panel_MiaoWorldMap"]["cells"]
labels = data["maps"]["Panel_DefaultWorldMap"]["cave_labels"]
print(f"{len(cells)} cells, {sum(1 for c in cells if c['name'])} named, "
      f"{sum(1 for c in cells if c['scene_file'])} linked to a zone image")

payload = json.dumps({"default": {"img": "WorldMap_Full.png", "cells": cells,
                                  "labels": labels},
                      "miao": {"img": "WorldMap_Miao_Full.png", "cells": miao,
                               "labels": data["maps"]["Panel_MiaoWorldMap"]["cave_labels"]}},
                     ensure_ascii=False)

HTML = r"""<!doctype html>
<meta charset="utf-8">
<title>ROOC World Map UI</title>
<style>
:root{--bg:#0f1218;--pane:#171c26;--line:#2b3444;--fg:#e9edf5;--dim:#93a0b8;--acc:#5fd0ff}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bg);color:var(--fg);font:14px/1.5 "Segoe UI",system-ui,sans-serif;
     display:flex;overflow:hidden}
#stage{flex:1;position:relative;overflow:hidden;cursor:grab;background:#0a0d12}
#stage.drag{cursor:grabbing}
#world{position:absolute;transform-origin:0 0;will-change:transform}
#world img{display:block;width:2048px;height:2048px;user-select:none;-webkit-user-drag:none}
.cell{position:absolute;border:2px solid rgba(120,220,255,.30);border-radius:3px;
      background:rgba(120,220,255,.06);transition:background .1s,border-color .1s}
.cell:hover{border-color:var(--acc);background:rgba(95,208,255,.28)}
.cell.on{border-color:#ffd447;background:rgba(255,212,71,.34);box-shadow:0 0 0 3px rgba(255,212,71,.25)}
.cell b{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
        font-size:22px;color:#fff;text-shadow:0 0 4px #000,0 0 8px #000;pointer-events:none}
.cell.named b{color:#ffe9a8}
.cave{position:absolute;transform:translate(-50%,-50%);color:#bfe6ff;font-size:18px;
      text-shadow:0 0 4px #000;pointer-events:none;white-space:nowrap}
#side{width:380px;flex:none;background:var(--pane);border-left:1px solid var(--line);
      display:flex;flex-direction:column}
#side h2{margin:0;padding:16px 18px 12px;font-size:16px;border-bottom:1px solid var(--line)}
#detail{padding:16px 18px;overflow:auto;flex:1}
#detail img{width:100%;background:#0d1016;border:1px solid var(--line);border-radius:8px}
.k{color:var(--dim);font-size:12px;margin-top:14px}
.v{font-family:Consolas,monospace;font-size:13px;word-break:break-all}
#hint{color:var(--dim);font-size:13px}
#bar{padding:10px 18px;border-top:1px solid var(--line);display:flex;gap:8px;align-items:center}
button{background:#222a38;border:1px solid var(--line);color:var(--fg);padding:7px 12px;
       border-radius:6px;cursor:pointer;font-size:13px}
button.on{background:var(--acc);border-color:var(--acc);color:#0f1218;font-weight:600}
#zoom{margin-left:auto;color:var(--dim);font-variant-numeric:tabular-nums}
</style>
<div id="stage"><div id="world"><img id="bgimg" src="WorldMap_Full.png" alt=""></div></div>
<div id="side">
  <h2>ROOC — World Map</h2>
  <div id="detail"><p id="hint">ลากเพื่อเลื่อน · scroll เพื่อซูม · คลิกช่องเพื่อดูแผนที่โซน</p></div>
  <div id="bar">
    <button id="bDef" class="on">World</button>
    <button id="bMiao">Miao</button>
    <button id="bFit">Fit</button>
    <span id="zoom"></span>
  </div>
</div>
<script>
const DATA = __DATA__;
const stage = document.getElementById("stage"), world = document.getElementById("world");
const img = document.getElementById("bgimg"), detail = document.getElementById("detail");
let which = "default", sc = 1, tx = 0, ty = 0;

function apply(){ world.style.transform = `translate(${tx}px,${ty}px) scale(${sc})`;
                  document.getElementById("zoom").textContent = Math.round(sc*100)+"%"; }
function fit(){ const r = stage.getBoundingClientRect();
                sc = Math.min(r.width, r.height)/2048*0.95;
                tx = (r.width-2048*sc)/2; ty = (r.height-2048*sc)/2; apply(); }

function render(){
  const d = DATA[which];
  img.src = d.img;
  [...world.querySelectorAll(".cell,.cave")].forEach(e=>e.remove());
  d.labels.forEach(l=>{ const s=document.createElement("div"); s.className="cave";
    s.style.left=l.center_px[0]+"px"; s.style.top=l.center_px[1]+"px";
    s.textContent=l.name; world.appendChild(s); });
  d.cells.forEach(c=>{
    const [x,y,w,h]=c.rect_px, e=document.createElement("div");
    e.className="cell"+(c.name?" named":"");
    e.style.cssText+=`left:${x}px;top:${y}px;width:${w}px;height:${h}px`;
    e.innerHTML=`<b>${c.name||c.id}</b>`;
    e.title=(c.name?c.name+" — ":"")+"id "+c.id;
    e.onclick=ev=>{ ev.stopPropagation();
      world.querySelectorAll(".cell.on").forEach(o=>o.classList.remove("on"));
      e.classList.add("on"); show(c); };
    world.appendChild(e);
  });
}
function show(c){
  detail.innerHTML =
    (c.scene_file ? `<img src="${c.scene_file}" alt="">` :
      `<p id="hint">ยังไม่ทราบว่าช่องนี้คือแมพไหน — ไม่มีตารางชื่อแมพใน asset dump</p>`) +
    `<div class="k">Name</div><div class="v">${c.name||"—"}</div>` +
    `<div class="k">Scene ID</div><div class="v">${c.id}</div>` +
    `<div class="k">Zone image</div><div class="v">${c.scene_file||"—"}</div>` +
    `<div class="k">Rect on world map (px)</div><div class="v">[${c.rect_px.join(", ")}]</div>` +
    `<div class="k">Unity pos (Bgs space)</div><div class="v">[${c.unity_pos.join(", ")}]</div>` +
    (c.identified_from?`<div class="k">Identified from</div><div class="v">${c.identified_from}</div>`:"");
}

let down=false, px=0, py=0, moved=false;
stage.addEventListener("mousedown",e=>{down=true;moved=false;px=e.clientX;py=e.clientY;
  stage.classList.add("drag");});
addEventListener("mousemove",e=>{ if(!down)return; const dx=e.clientX-px, dy=e.clientY-py;
  if(Math.abs(dx)+Math.abs(dy)>3) moved=true;
  tx+=dx; ty+=dy; px=e.clientX; py=e.clientY; apply(); });
addEventListener("mouseup",()=>{down=false;stage.classList.remove("drag");});
stage.addEventListener("wheel",e=>{ e.preventDefault();
  const r=stage.getBoundingClientRect(), mx=e.clientX-r.left, my=e.clientY-r.top;
  const f=e.deltaY<0?1.15:1/1.15, ns=Math.min(4,Math.max(0.1,sc*f));
  tx=mx-(mx-tx)*(ns/sc); ty=my-(my-ty)*(ns/sc); sc=ns; apply(); },{passive:false});

document.getElementById("bFit").onclick=fit;
document.getElementById("bDef").onclick=e=>{which="default";sel(e.target);render();fit();};
document.getElementById("bMiao").onclick=e=>{which="miao";sel(e.target);render();fit();};
function sel(b){ [...document.querySelectorAll("#bar button")].forEach(x=>x.classList.remove("on"));
                 b.classList.add("on"); }
render(); addEventListener("resize",fit); fit();
</script>
"""
dest = os.path.join(OUT, "WorldMapUI.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(HTML.replace("__DATA__", payload))
print("->", dest)
