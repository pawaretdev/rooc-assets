# -*- coding: utf-8 -*-
"""One HTML shell for every folder's index.html.

Each folder's gallery script builds a list of rows and calls render(); the
markup, styling and behaviour live here so the indexes stay identical.

A row is a dict:

    src    thumbnail path, relative to the index.html
    href   full-size path (defaults to src)
    name   filename shown under the image, monospace
    label  optional bold line above it -- omit the key for folders that have
           no label at all, pass "" for a row whose label is unknown
    meta   optional dim line below it
    px     set truthy on assets only a few pixels across, so the tile renders
           them with nearest-neighbour instead of smearing them
    g      group name, must be one of the `groups` passed to render()
"""
import collections
import json
import os

# Sibling folders, in the order they appear in the nav bar.
SECTIONS = [
    ("maps", "Maps"),
    ("items", "Items"),
    ("cards", "Cards"),
    ("sprites", "Sprites"),
    ("hotupdate", "HotUpdate"),
]

# Theme and chrome, shared with the root landing page in build_home.py.
BASE_CSS = r"""
:root{
  --bg:#12151c; --card:#1b202b; --line:#2a3140; --fg:#e8ecf4;
  --dim:#98a2b8; --faint:#5f6a80; --acc:#f0b429; --shot:#0f1319;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
     font:14px/1.5 "Segoe UI",system-ui,sans-serif}
a{color:inherit}

header{position:sticky;top:0;z-index:5;background:rgba(18,21,28,.97);
       border-bottom:1px solid var(--line);padding:14px 22px;backdrop-filter:blur(8px)}
nav{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:11px}
nav a{padding:4px 11px;border-radius:6px;font-size:12.5px;color:var(--dim);
      text-decoration:none;border:1px solid transparent}
nav a:hover{background:var(--card);border-color:var(--line)}
nav a.here{background:var(--card);border-color:var(--line);color:var(--fg);font-weight:600}
nav a.home{color:var(--acc)}
h1{margin:0;font-size:17px;letter-spacing:.02em}
.sub{color:var(--dim);font-size:13px;margin-top:3px;max-width:80ch}
.sub code{background:var(--card);padding:1px 5px;border-radius:4px;font-size:12px}
.sub a{color:var(--acc)}
"""

_CSS = BASE_CSS + r"""
.controls{display:flex;gap:8px;flex-wrap:wrap;margin-top:11px;align-items:center}
input{background:var(--card);border:1px solid var(--line);color:var(--fg);
      padding:8px 12px;border-radius:7px;min-width:300px;font-size:14px}
input:focus{outline:2px solid var(--acc);outline-offset:-1px}
#tabs{display:flex;gap:6px;flex-wrap:wrap}
/* Folders like sprites/ produce 40+ groups; two rows of tabs is plenty to see
   before the images start, the rest is one click away. */
#tabs.clamp{max-height:66px;overflow:hidden}
#more{border-style:dashed}
button{background:var(--card);border:1px solid var(--line);color:var(--dim);
       padding:6px 12px;border-radius:7px;cursor:pointer;font-size:12.5px}
button:hover{color:var(--fg)}
button.on{background:var(--acc);border-color:var(--acc);color:#12151c;font-weight:600}
#count{color:var(--dim);margin-left:auto;font-variant-numeric:tabular-nums;
       white-space:nowrap;font-size:13px}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(__MINW__px,1fr));
      gap:13px;padding:20px}
.card{background:var(--card);border:1px solid var(--line);border-radius:9px;
      overflow:hidden;display:flex;flex-direction:column;transition:border-color .12s}
.card:hover{border-color:var(--acc)}
/* flex:none matters -- the grid stretches cards to the tallest in the row, and
   without it the image box grows too and loses its aspect ratio. */
.card a{display:block;flex:none;background:__SHOT__;aspect-ratio:__ASPECT__;padding:__PAD__px}
.card img{width:100%;height:100%;object-fit:contain;display:block}
/* Sprite sheets hold a lot of 8x8 nubs; smoothing those into a smear on a
   130px tile helps nobody. */
.card img.px{image-rendering:pixelated}
.meta{padding:6px 8px;border-top:1px solid var(--line);margin-top:auto}
.lab{font-weight:600;font-size:12.5px;line-height:1.35}
.lab.q{color:var(--acc)}
.lab.none{color:var(--faint);font-weight:400;font-style:italic}
.fn{color:var(--dim);font-size:10.5px;font-family:Consolas,ui-monospace,monospace;
    word-break:break-all;line-height:1.35}
.dm{color:var(--faint);font-size:10px;margin-top:2px}
.empty{padding:60px 22px;color:var(--dim);text-align:center}
"""

# Transparent icons need something behind them; framed art and photos do not.
_CHECKER = ("linear-gradient(45deg,#191d26 25%,transparent 25%,transparent 75%,#191d26 75%)"
            " 0 0/16px 16px,"
            "linear-gradient(45deg,#191d26 25%,transparent 25%,transparent 75%,#191d26 75%)"
            " 8px 8px/16px 16px,#0f1319")

_HTML = r"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<style>__CSS__</style>
<header>
  <nav>__NAV__</nav>
  <h1>__H1__</h1>
  <div class="sub">__SUB__</div>
  <div class="controls">
    <input id="q" placeholder="__PLACEHOLDER__" autofocus>
    <span id="count"></span>
  </div>
  <div class="controls"><span id="tabs" class="clamp"></span>
    <button id="more" hidden></button></div>
</header>
<div class="grid" id="grid"></div>
<div class="empty" id="empty" hidden>no match</div>
<script>
const ROWS = __DATA__, GROUPS = __GROUPS__, PAGE = __PAGE__;
let group = "All", q = "", limit = PAGE;

const $ = id => document.getElementById(id);
const ENT = {"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"};
const esc = s => String(s === undefined || s === null ? "" : s)
  .replace(/[&<>"]/g, c => ENT[c]);

const counts = {All: ROWS.length};
for (const g of GROUPS) counts[g] = 0;
for (const r of ROWS) if (r.g in counts) counts[r.g]++;

$("tabs").innerHTML = ["All"].concat(GROUPS)
  .filter(g => counts[g])
  .map(g => '<button data-g="' + esc(g) + '">' + esc(g) +
            ' <span style="opacity:.55">' + counts[g] + '</span></button>')
  .join("");
$("tabs").onclick = e => {
  const b = e.target.closest("button");
  if (!b) return;
  group = b.dataset.g; limit = PAGE; draw();
};
$("q").oninput = e => { q = e.target.value; limit = PAGE; draw(); };

// Only offer the toggle when the tabs actually overflow their two rows.
const tabs = $("tabs"), more = $("more");
if (tabs.scrollHeight > tabs.clientHeight + 4) {
  more.hidden = false;
  const label = () => tabs.classList.contains("clamp")
    ? "all " + GROUPS.length + " groups ▾" : "fewer ▴";
  more.textContent = label();
  more.onclick = () => { tabs.classList.toggle("clamp"); more.textContent = label(); };
}

// Grow the page as you reach the bottom -- some folders hold thousands of images.
addEventListener("scroll", () => {
  if (innerHeight + scrollY > document.body.offsetHeight - 700) {
    const before = limit;
    limit += PAGE;
    if (before !== limit) draw();
  }
});

function match(r, t) {
  return !t || r.name.toLowerCase().includes(t) ||
         (r.label && r.label.toLowerCase().includes(t)) ||
         (r.meta && r.meta.toLowerCase().includes(t));
}

function draw() {
  const t = q.trim().toLowerCase();
  const list = ROWS.filter(r => (group === "All" || r.g === group) && match(r, t));
  const shown = list.slice(0, limit);

  $("count").textContent = list.length === shown.length
    ? list.length + " / " + ROWS.length
    : shown.length + " / " + list.length + "  · scroll for more";
  for (const b of $("tabs").children) b.classList.toggle("on", b.dataset.g === group);
  $("empty").hidden = list.length > 0;

  $("grid").innerHTML = shown.map(r => {
    let m = "";
    if ("label" in r) {
      const cls = !r.label ? "lab none" : (r.label.indexOf("?") >= 0 ? "lab q" : "lab");
      m += '<div class="' + cls + '">' + esc(r.label || "unidentified") + '</div>';
    }
    m += '<div class="fn">' + esc(r.name) + '</div>';
    if (r.meta) m += '<div class="dm">' + esc(r.meta) + '</div>';
    return '<div class="card"><a href="' + esc(r.href || r.src) +
           '" target="_blank" rel="noopener"><img loading="lazy"' +
           (r.px ? ' class="px"' : '') + ' src="' + esc(r.src) +
           '" alt=""></a><div class="meta">' + m + '</div></div>';
  }).join("");
}
draw();
</script>
"""


def nav(here):
    """Nav bar for a page in folder `here`; here="" is the root landing page."""
    root = here == ""
    out = ['<a href="%s" class="home%s">rooc-assets</a>'
           % ("index.html" if root else "../index.html", " here" if root else "")]
    for slug, label in SECTIONS:
        if slug == here:
            out.append('<a href="index.html" class="here">%s</a>' % label)
        else:
            out.append('<a href="%s%s/index.html">%s</a>'
                       % ("" if root else "../", slug, label))
    return "".join(out)


def render(dest, *, here, h1, sub, rows, groups,
           placeholder="search filename…", min_width=132, aspect="1",
           pad=8, checker=True, page=400):
    """Write one index.html. Returns the path written."""
    css = (_CSS.replace("__MINW__", str(min_width))
               .replace("__ASPECT__", aspect)
               .replace("__PAD__", str(pad))
               .replace("__SHOT__", _CHECKER if checker else "var(--shot)"))
    html = (_HTML.replace("__CSS__", css)
                 .replace("__TITLE__", "ROOC — " + h1)
                 .replace("__NAV__", nav(here))
                 .replace("__H1__", h1)
                 .replace("__SUB__", sub)
                 .replace("__PLACEHOLDER__", placeholder)
                 .replace("__DATA__", json.dumps(rows, ensure_ascii=False))
                 .replace("__GROUPS__", json.dumps(groups, ensure_ascii=False))
                 .replace("__PAGE__", str(page)))
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("-> %s  (%s rows, %d groups)" % (dest, format(len(rows), ","), len(groups)))
    return dest


def repo_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- grouping --
# hotupdate/ and sprites/ are flat folders of thousands of assets whose only
# structure is the naming convention, so both derive their tabs the same way:
# `UI_Icon_foo` groups under "UI_Icon", `Monster_bar` under "Monster", and
# anything whose prefix is too rare to earn a tab falls into "Other".

def _tokens(n):
    return n.replace("-", "_").split("_")


def _fine(n):
    p = _tokens(n)
    if p[0].lower() in ("ui", "fx") and len(p) > 1:
        return p[0].upper() + "_" + p[1]
    return p[0]


def _canon(labels):
    """Fold case variants (ui_ / UI_) onto whichever spelling is most common."""
    by = collections.defaultdict(collections.Counter)
    for l in labels:
        by[l.lower()][l] += 1
    return {k: v.most_common(1)[0][0] for k, v in by.items()}


def prefix_groups(names, *, fine_top=30, fine_min=25, coarse_top=10, coarse_min=25):
    """Return group_of(name) for a flat folder of convention-named assets."""
    names = list(names)
    fine_label = _canon(_fine(n) for n in names)
    coarse_label = _canon(_tokens(n)[0] for n in names)

    fc = collections.Counter(_fine(n).lower() for n in names)
    big_fine = {g for g, c in fc.most_common(fine_top) if c >= fine_min}
    cc = collections.Counter(_tokens(n)[0].lower() for n in names
                             if _fine(n).lower() not in big_fine)
    big_coarse = {g for g, c in cc.most_common(coarse_top) if c >= coarse_min}

    def group_of(n):
        f = _fine(n).lower()
        if f in big_fine:
            return fine_label[f]
        c = _tokens(n)[0].lower()
        return coarse_label[c] if c in big_coarse else "Other"

    return group_of


def order_groups(rows, show=12):
    """Biggest group first, 'Other' always last. Prints the tally."""
    gc = collections.Counter(r["g"] for r in rows)
    groups = sorted(gc, key=lambda g: (g == "Other", -gc[g], g))
    print("%s rows, %d groups" % (format(len(rows), ","), len(groups)))
    for g in groups[:show]:
        print("  %6d  %s" % (gc[g], g))
    if len(groups) > show:
        print("  ... %d more" % (len(groups) - show))
    return groups
