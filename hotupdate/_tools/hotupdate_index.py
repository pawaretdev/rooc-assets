# -*- coding: utf-8 -*-
"""index.html for the HotUpdate extraction, grouped by asset-name prefix."""
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_tools"))
import rooc_gallery as G  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(HERE, "manifest.json")


def main():
    with open(MANIFEST, encoding="utf-8") as fh:
        man = json.load(fh)

    group_of = G.prefix_groups(m["name"] for m in man)
    rows = [{
        "src": "images/" + m["file"],
        "name": m["name"],
        "meta": "%d×%d · %s · %s" % (m["w"], m["h"], m["type"], m["bundle"]),
        "g": group_of(m["name"]),
        "px": 1 if max(m["w"], m["h"]) < 64 else 0,
    } for m in man]

    groups = G.order_groups(rows)

    G.render(
        os.path.join(HERE, "index.html"),
        here="hotupdate",
        h1="HotUpdate patch assets",
        sub=("__N__ images from the game's <code>StreamingAssets/HotUpdate</code> &mdash; content "
             "patched in after the base install, so none of it is in the AssetBundles dump. "
             "Bundle filenames are numeric hashes, so the only way to find anything is by asset "
             "name; the hash is on each tile and is searchable."
             ).replace("__N__", format(len(rows), ",")),
        rows=rows,
        groups=groups,
        placeholder="search asset name or bundle hash…",
        min_width=132,
        page=400,
    )


if __name__ == "__main__":
    main()
