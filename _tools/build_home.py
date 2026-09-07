# -*- coding: utf-8 -*-
"""index.html for the repo root -- one door into the five galleries.

Reads each folder's generated index.html rather than re-scanning the folders,
so the counts and the sample thumbnails can never drift from what the galleries
actually show. Run it after the per-folder gallery scripts.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rooc_gallery as G  # noqa: E402

ROOT = G.repo_root()
SAMPLES = 5

BLURB = {
    "maps": "Per-zone map images, labelled by hand against in-game screenshots, "
            "plus the stitched world map and its cell coordinates.",
    "items": "Item, equipment, costume and mount icons in the game's own folder "
             "layout, plus every atlas sheet sliced apart.",
    "cards": "Monster card art. The frame and the English monster name are baked "
             "into each texture, so this is the one set you can read by eye.",
    "sprites": "The loose sprite dump — UI parts, monster and NPC portraits, "
               "costume and headgear thumbnails, emoji, effect frames.",
    "hotupdate": "Patch content, pulled from the loose HotUpdate bundles. Anything "
                 "added to the game after release exists only here.",
}

CSS = G.BASE_CSS + r"""
main{padding:22px;max-width:1500px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(430px,1fr));gap:15px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:11px;
      overflow:hidden;text-decoration:none;display:flex;flex-direction:column;
      transition:border-color .12s,transform .12s}
.tile:hover{border-color:var(--acc);transform:translateY(-2px)}
.strip{display:grid;grid-template-columns:repeat(__SAMPLES__,1fr);gap:1px;
       background:var(--line);border-bottom:1px solid var(--line)}
.strip span{background:#0f1319;aspect-ratio:1;display:block;padding:7px}
.strip img{width:100%;height:100%;object-fit:contain;display:block}
.body{padding:12px 14px}
.row{display:flex;align-items:baseline;gap:9px}
.name{font-size:16px;font-weight:600}
.n{color:var(--acc);font-size:12.5px;font-variant-numeric:tabular-nums}
.desc{color:var(--dim);font-size:12.5px;margin-top:4px;line-height:1.45}

.aside{margin-top:26px;border-top:1px solid var(--line);padding-top:18px}
h2{font-size:13px;font-weight:600;color:var(--dim);margin:0 0 9px;
   text-transform:uppercase;letter-spacing:.06em}
.links{display:flex;gap:9px;flex-wrap:wrap}
.links a{background:var(--card);border:1px solid var(--line);border-radius:8px;
         padding:9px 13px;text-decoration:none;font-size:13px;max-width:420px}
.links a:hover{border-color:var(--acc)}
.links b{display:block;font-weight:600}
.links i{display:block;color:var(--dim);font-size:12px;font-style:normal;margin-top:2px}
"""

HTML = r"""<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>rooc-assets</title>
<style>__CSS__</style>
<header>
  <nav>__NAV__</nav>
  <h1>rooc-assets</h1>
  <div class="sub">Art extracted from a Ragnarok Origin client &mdash; Unity 2019.4.36f1,
    plain unencrypted <code>UnityFS</code> bundles. __TOTAL__ images across five sets.
    Filenames are the game's internal names, mostly Chinese pinyin; there is no name table
    in the dump, so searching by the English name usually will not work.</div>
</header>
<main>
  <div class="tiles">__TILES__</div>
  <div class="aside">
    <h2>Not a gallery</h2>
    <div class="links">
      <a href="maps/WorldMapUI.html"><b>World map</b>
        <i>Pan/zoom demo of the in-game world map, with clickable zone cells</i></a>
      <a href="README.md"><b>README.md</b>
        <i>What is here, where it came from, and what the known gaps are</i></a>
      <a href="EXTRACTING.md"><b>EXTRACTING.md</b>
        <i>How to unpack the game folder and reproduce these dumps</i></a>
    </div>
  </div>
</main>
"""


def read_rows(slug):
    """Pull the row list back out of a generated gallery page."""
    p = os.path.join(ROOT, slug, "index.html")
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as fh:
        html = fh.read()
    m = re.search(r"const ROWS = (\[.*?\]), GROUPS = ", html, re.S)
    return json.loads(m.group(1)) if m else None


def main():
    tiles, total, missing = [], 0, []
    for slug, label in G.SECTIONS:
        rows = read_rows(slug)
        if not rows:
            missing.append(slug)
            continue
        total += len(rows)

        # Spread the samples through the folder instead of taking the first few,
        # which would only ever show whatever sorts to the top of the alphabet.
        step = max(1, len(rows) // SAMPLES)
        picks = [rows[min(i * step, len(rows) - 1)] for i in range(SAMPLES)]
        strip = "".join(
            '<span><img loading="lazy" src="%s/%s" alt=""></span>' % (slug, r["src"])
            for r in picks)

        tiles.append(
            '<a class="tile" href="%s/index.html">'
            '<div class="strip">%s</div>'
            '<div class="body"><div class="row"><span class="name">%s</span>'
            '<span class="n">%s images</span></div>'
            '<div class="desc">%s</div></div></a>'
            % (slug, strip, label, format(len(rows), ","), BLURB.get(slug, "")))
        print("  %-10s %8s" % (slug, format(len(rows), ",")))

    if missing:
        print("  [skipped, no index.html yet] " + ", ".join(missing))

    dest = os.path.join(ROOT, "index.html")
    with open(dest, "w", encoding="utf-8") as fh:
        fh.write(HTML.replace("__CSS__", CSS.replace("__SAMPLES__", str(SAMPLES)))
                     .replace("__NAV__", G.nav(""))
                     .replace("__TOTAL__", format(total, ","))
                     .replace("__TILES__", "".join(tiles)))
    print("-> %s  (%s images across %d sets)" % (dest, format(total, ","), len(tiles)))


if __name__ == "__main__":
    main()
