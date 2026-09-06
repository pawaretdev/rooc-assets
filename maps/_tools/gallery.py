"""Build a browsable index of the extracted per-scene map images."""
import os, json, html
from PIL import Image

OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps"
SRC = os.path.join(OUT, "SceneMaps")
THUMBS = os.path.join(OUT, "_thumbs")
THUMB_W = 320

# Best-effort identification from the pinyin stem. "?" = uncertain, verify visually.
# These are NOT from the game's string table (it isn't in this dump).
NAMES = {
    "pulongdela": "Prontera",                  # visually confirmed vs in-game screenshot
    "pulongdela_yzhj": "Prontera - ? sub-area",
    "yisilude": "Izlude",
    "ysld_jiuba": "Izlude - Tavern",
    "mengluoke": "Morroc",
    "mlknanbu": "Morroc South",
    "mlkxibu": "Morroc West",
    "mlkchengbao": "Morroc Castle",
    "mlkdilao": "Morroc Dungeon",
    "mlkjianyu": "Morroc Prison",
    "feiyang": "Payon",
    "feiyangdongbu": "Payon East",
    "feiyangdongnan": "Payon Southeast",
    "feiyangnanbu": "Payon South",
    "feiyangshulin": "Payon Forest",
    "gongshoucun": "Archer Village (Payon)",
    "aierbeita": "Alberta",
    "aierbeita_jyhj": "Alberta - ? sub-area",
    "aierpalan": "Al De Baran",
    "jifen": "Geffen",
    "jifenbeibu": "Geffen North",
    "jifendongbu": "Geffen East",
    "jifenxibu": "Geffen West",
    "jifenkuangye": "Geffen Field",
    "jifenguodu": "Geffen - transition",
    "jifenta": "Geffen Tower",
    "zhunuo": "Juno",
    "znqmowulaixi": "Juno - ?",
    "zn_nkldrongdong": "Juno - ? cave",
    "sukelate": "Schwaltzvalt ?",
    "sukelatenanbu": "Schwaltzvalt South ?",
    "gucheng": "Glast Heim",
    "gcchengbao": "Glast Heim - Castle",
    "gcjianyu": "Glast Heim - Prison",
    "gcqst": "Glast Heim - Chivalry",
    "gcxiashuidao": "Glast Heim - Culvert",
    "gcgm": "Glast Heim - ?",
    "guchengxiudaoyuan": "Glast Heim - St. Abbey",
    "bolidao": "Poring Island",
    "boyiyalandao": "Byalan Island",
    "dengtadao": "Lighthouse Island",
    "haididongxue": "Undersea Cave",
    "chenchuanmigong": "Sunken Ship - Labyrinth",
    "chenmozhichuan": "Sunken Ship",
    "xiashuidao": "Prontera Culvert (Sewer)",
    "mayidong": "Ant Hell",
    "jinzita1f": "Pyramid 1F",
    "jinzita2f": "Pyramid 2F",
    "jinzita3f": "Pyramid 3F",
    "shourencunluo": "Orc Village",
    "shourendong": "Orc Dungeon",
    "gebulinsenlin": "Goblin Forest",
    "miaolenishanmai": "Mt. Mjolnir",
    "yinglingdian": "Valhalla",
    "yimierzhixing": "Ymir's Heart ?",
    "huanghunshenyu": "Twilight Realm ?",
    "wuxianta": "Endless Tower",
    "wuxiantarukou": "Endless Tower - Entrance",
    "heianmigong": "Dark Labyrinth",
    "jiangshidong": "Zombie Cave ?",
    "beisenmigong1f": "? Labyrinth 1F",
    "beisenmigong2f": "? Labyrinth 2F",
    "bsmgguodu": "? Labyrinth - transition",
    "beimen": "North Gate",
    "nanmen": "South Gate",
    "dongmen": "East Gate",
    "ximen": "West Gate",
    "huanggong": "Palace",
    "shizhuangdian": "Costume Shop",
    "xianzhedating": "Sage Hall (Chamber of the Mage?)",
    "zhuanzhidating": "Job Change Hall",
    "huayuan": "Garden",
    "jiehun": "Wedding",
    "jiehunshinei": "Wedding - Indoor",
    "xunlianchang": "Training Ground",
    "tiaozhanchang": "Challenge Arena",
    "zhuansheng": "Rebirth / Transcendence",
    "gonghui": "Guild",
    "gonghui_yyh": "Guild - Banquet",
    "gonghuiliansai": "Guild League",
    "shamochadao": "Desert Crossroad ?",
    "shamozhiqiao": "Desert Bridge ?",
    "feiqikuangkeng": "Abandoned Mine",
    "erjingshendian": "? Temple",
    "shenggeshilian": "Hymn Trial ?",
    "jinglianwu": "Refine Room",
    "heidian": "Black Shop ?",
    "heishi": "Black Market ?",
    "wuhui": "Ball / Dance Hall ?",
    "jianyu": "Prison",
    "huanjing": "Illusion Realm ?",
    "paidui": "Queue / Lobby",
    "ketesenlin": "? Forest",
    "machesenlin": "? Forest",
    "moyingzailin": "? Forest",
    "xianluozhidi": "Fallen Land ?",
    "yuchongxiagu": "? Valley",
    "gunayanjiujidi": "? Research Base",
    "moshenta": "Demon Tower ?",
    "kaihong": "?",
    "donglishi": "?",
    "wulinmengzhu": "?",
    "ssdating": "? Hall",
    "szjzzdating": "? Job Change Hall",
    "zzdz": "Job Change - Thief",
    "zzfs": "Job Change - Mage",
    "zzgjs": "Job Change - Archer",
    "zzjs": "Job Change - Swordsman",
    "zzjsshilian": "Job Change - Swordsman Trial",
    "zzms": "Job Change - Acolyte",
    "zzsr": "Job Change - Merchant",
    "zzlianjinshi": "Job Change - Alchemist",
    "zzlm": "Job Change - ?",
    "zzwuniang": "Job Change - Dancer",
    "zzxianzhe": "Job Change - Sage",
    "xiariyouyuanhui": "Summer Fair (event)",
    "guild_tournament_scorebattle": "Guild Tournament - Score Battle",
    "gvehuanzhanlingyu": "GvE - Fantasy Battlefield",
    "gvgchengzhu": "GvG - Castle Lord",
    "srb_longerzhizai": "? boss arena",
    "wszz": "?",
    "mzgshirenben": "?",
    "sfksmx1f": "? 1F",
    "sfksmx2f": "? 2F",
    "gcgm_": "Glast Heim - ?",
}

# prefix-based fallbacks
GROUPS = [
    ("sc_gvgpulongdela", "GvG - Prontera"),
    ("sc_gvgfeiyang", "GvG - Payon"),
    ("sc_gvgjifen", "GvG - Geffen"),
    ("sc_gvg_", "GvG"),
    ("sc_gvg", "GvG"),
    ("sc_pvp_", "PvP"),
    ("sc_PVP_", "PvP"),
    ("sc_dungeon_", "Dungeon"),
]


def label_for(stem):
    body = stem[3:] if stem.startswith("sc_") else stem          # strip "sc_"
    core = body
    # strip a trailing _001 / _002 / _003_1 style suffix
    parts = core.split("_")
    while parts and parts[-1].isdigit():
        parts.pop()
    core = "_".join(parts)
    if core in NAMES:
        return NAMES[core]
    if core.startswith("dungeon_"):
        inner = core[len("dungeon_"):]
        return "Dungeon - " + NAMES.get(inner, inner)
    for pre, lab in GROUPS:
        if stem.startswith(pre):
            return lab + " - " + core
    return ""


def category(stem):
    if stem.startswith(("sc_gvg", "sc_pvp", "sc_PVP")) or "tournament" in stem or "liansai" in stem:
        return "PvP / GvG"
    if "dungeon" in stem or stem.startswith(("sc_jinzita", "sc_wuxianta", "sc_haididong",
                                             "sc_mayidong", "sc_jiangshidong", "sc_heianmigong")):
        return "Dungeon"
    if stem.startswith(("sc_zz", "sc_szjzz")):
        return "Job change"
    return "Town / Field"


os.makedirs(THUMBS, exist_ok=True)
rows = []
for fn in sorted(os.listdir(SRC)):
    if not fn.lower().endswith(".png"):
        continue
    stem = os.path.splitext(fn)[0]
    src = os.path.join(SRC, fn)
    im = Image.open(src)
    w, h = im.size
    tp = os.path.join(THUMBS, fn)
    if not os.path.exists(tp):
        t = im.copy()
        t.thumbnail((THUMB_W, THUMB_W))
        t.save(tp)
    rows.append({"file": fn, "stem": stem, "label": label_for(stem),
                 "cat": category(stem), "dim": f"{w}x{h}"})

cats = ["Town / Field", "Dungeon", "PvP / GvG", "Job change"]
data = json.dumps(rows, ensure_ascii=False)

page = """<!doctype html>
<meta charset="utf-8">
<title>ROOC Scene Maps</title>
<style>
:root{--bg:#12151c;--card:#1b202b;--line:#2a3140;--fg:#e8ecf4;--dim:#98a2b8;--acc:#f0b429}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
     font:14px/1.5 "Segoe UI",system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:rgba(18,21,28,.96);
       border-bottom:1px solid var(--line);padding:16px 24px;
       backdrop-filter:blur(8px)}
h1{margin:0 0 4px;font-size:18px;letter-spacing:.02em}
.sub{color:var(--dim);font-size:13px}
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px;align-items:center}
input{background:var(--card);border:1px solid var(--line);color:var(--fg);
      padding:8px 12px;border-radius:7px;min-width:260px;font-size:14px}
input:focus{outline:2px solid var(--acc);outline-offset:-1px}
button{background:var(--card);border:1px solid var(--line);color:var(--dim);
       padding:8px 14px;border-radius:7px;cursor:pointer;font-size:13px}
button.on{background:var(--acc);border-color:var(--acc);color:#12151c;font-weight:600}
#count{color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));
      gap:16px;padding:24px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;
      overflow:hidden;display:flex;flex-direction:column;transition:.12s}
.card:hover{border-color:var(--acc);transform:translateY(-2px)}
.card a{display:block;background:#0d1016;aspect-ratio:1;overflow:hidden}
.card img{width:100%;height:100%;object-fit:contain;display:block}
.meta{padding:9px 11px;border-top:1px solid var(--line)}
.lab{font-weight:600;font-size:13px;min-height:1.5em}
.lab.q{color:var(--acc)}
.lab.none{color:var(--dim);font-weight:400;font-style:italic}
.fn{color:var(--dim);font-size:11px;font-family:Consolas,monospace;
    word-break:break-all;margin-top:2px}
.dim{color:#5f6a80;font-size:10px;margin-top:2px}
</style>
<header>
  <h1>ROOC — Scene Maps</h1>
  <div class="sub">__N__ per-zone map images extracted from <code>Resources/UI/Texture/Map</code>.
    Labels in <span style="color:var(--acc)">yellow</span> or ending in “?” are my best-effort
    identification, not from the game’s string table — verify visually.</div>
  <div class="controls">
    <input id="q" placeholder="ค้นหา — ชื่อไฟล์ หรือ ชื่อแมพ…" autofocus>
    <span id="tabs"></span>
    <span id="count"></span>
  </div>
</header>
<div class="grid" id="grid"></div>
<script>
const rows = __DATA__;
const cats = __CATS__;
let cat = "All", q = "";
const tabs = document.getElementById("tabs");
["All", ...cats].forEach(c => {
  const b = document.createElement("button");
  b.textContent = c; b.onclick = () => { cat = c; draw(); };
  b.dataset.cat = c; tabs.appendChild(b);
});
function draw() {
  const t = q.trim().toLowerCase();
  const list = rows.filter(r =>
    (cat === "All" || r.cat === cat) &&
    (!t || r.stem.toLowerCase().includes(t) || r.label.toLowerCase().includes(t)));
  document.getElementById("count").textContent = list.length + " / " + rows.length;
  [...tabs.children].forEach(b => b.classList.toggle("on", b.dataset.cat === cat));
  document.getElementById("grid").innerHTML = list.map(r => {
    const cls = !r.label ? "lab none" : (r.label.includes("?") ? "lab q" : "lab");
    const txt = r.label || "unidentified";
    return `<div class="card">
      <a href="SceneMaps/${r.file}" target="_blank">
        <img loading="lazy" src="_thumbs/${r.file}" alt="${r.stem}"></a>
      <div class="meta"><div class="${cls}">${txt}</div>
        <div class="fn">${r.stem}</div><div class="dim">${r.dim}</div></div></div>`;
  }).join("");
}
document.getElementById("q").oninput = e => { q = e.target.value; draw(); };
draw();
</script>
"""

page = (page.replace("__DATA__", data)
            .replace("__CATS__", json.dumps(cats))
            .replace("__N__", str(len(rows))))

dest = os.path.join(OUT, "MapIndex.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(page)

named = sum(1 for r in rows if r["label"] and "?" not in r["label"])
print(f"{len(rows)} maps, {len(os.listdir(THUMBS))} thumbnails")
print(f"confident labels: {named}   uncertain/unlabelled: {len(rows)-named}")
print(dest)
