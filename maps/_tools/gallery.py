# -*- coding: utf-8 -*-
"""index.html for the extracted per-scene map images."""
import os, sys
from PIL import Image

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_tools"))
import rooc_gallery as G  # noqa: E402

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
    im = Image.open(os.path.join(SRC, fn))
    w, h = im.size
    tp = os.path.join(THUMBS, fn)
    if not os.path.exists(tp):
        t = im.copy()
        t.thumbnail((THUMB_W, THUMB_W))
        t.save(tp)
    rows.append({
        "src": "_thumbs/" + fn,
        "href": "SceneMaps/" + fn,
        "name": stem,
        "label": label_for(stem),
        "meta": "%d×%d" % (w, h),
        "g": category(stem),
    })

groups = ["Town / Field", "Dungeon", "PvP / GvG", "Job change"]
named = sum(1 for r in rows if r["label"] and "?" not in r["label"])
print("%d maps, %d thumbnails" % (len(rows), len(os.listdir(THUMBS))))
print("confident labels: %d   uncertain/unlabelled: %d" % (named, len(rows) - named))

G.render(
    os.path.join(OUT, "index.html"),
    here="maps",
    h1="Scene Maps",
    sub=("__N__ per-zone map images from <code>Resources/UI/Texture/Map</code>. Labels in "
         "<span style=\"color:var(--acc)\">yellow</span> or ending in &ldquo;?&rdquo; are a "
         "best-effort identification matched by hand, not from the game&rsquo;s string table "
         "&mdash; verify visually. The world map itself lives in "
         "<a href=\"WorldMapUI.html\">WorldMapUI.html</a>."
         ).replace("__N__", str(len(rows))),
    rows=rows,
    groups=groups,
    placeholder="search filename or zone name…",
    min_width=210,
    checker=False,
    page=400,
)
