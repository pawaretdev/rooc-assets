# -*- coding: utf-8 -*-
"""index.html for the loose sprite dump, grouped by asset-name prefix.

The folder is flat -- tens of thousands of PNGs straight out of the bundles,
most named `<asset>.png.png` because the extractor appended its own extension
to a name that already carried one. Nothing here is renamed; the index just
hides the duplicated suffix in the label.
"""
import os
import struct
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_tools"))
import rooc_gallery as G  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def png_size(path):
    """Width/height straight out of the IHDR -- far cheaper than decoding."""
    try:
        with open(path, "rb") as fh:
            head = fh.read(24)
        if head[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        return struct.unpack(">II", head[16:24])
    except OSError:
        return None


def stem(fn):
    """Strip the extractor's trailing .png, and the asset's own one under it."""
    n = fn
    while n.lower().endswith(".png"):
        n = n[:-4]
    return n or fn


def main():
    files = sorted(f for f in os.listdir(HERE)
                   if f.lower().endswith(".png") and os.path.isfile(os.path.join(HERE, f)))
    stems = [stem(f) for f in files]
    group_of = G.prefix_groups(stems, fine_min=60, coarse_min=60,
                               fine_top=40, coarse_top=15)

    rows = []
    for fn, st in zip(files, stems):
        wh = png_size(os.path.join(HERE, fn))
        row = {"src": fn, "name": st, "g": group_of(st),
               "meta": ("%d×%d" % wh) if wh else "unreadable"}
        if wh and max(wh) < 64:
            row["px"] = 1
        rows.append(row)

    groups = G.order_groups(rows)

    G.render(
        os.path.join(HERE, "index.html"),
        here="sprites",
        h1="Sprites",
        sub=("__N__ loose sprite PNGs pulled out of the bundles &mdash; UI parts, monster and "
             "NPC portraits, costume and headgear thumbnails. Flat folder, no manifest; "
             "filenames are the game's internal names, and the doubled <code>.png.png</code> "
             "suffix on disk is the extractor's, not the game's."
             ).replace("__N__", format(len(rows), ",")),
        rows=rows,
        groups=groups,
        placeholder="search sprite name…",
        min_width=118,
        page=500,
    )


if __name__ == "__main__":
    main()
