# -*- coding: utf-8 -*-
"""index.html for the extracted item/equipment/costume icons."""
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_tools"))
import rooc_gallery as G  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Folder names come from the game's own layout; these fold them into something
# you can actually click through.
GROUP = [
    ("Consumables", lambda d: d.startswith("Icon_ItemConsumables")),
    ("Equipment", lambda d: d.startswith("Icon_ItemEquip")),
    ("Materials", lambda d: d.startswith("Icon_ItemMaterial")),
    ("Headwear", lambda d: d.startswith("Icon_ItemHeadwear")),
    ("Costume", lambda d: d.startswith("Icon_Wear_")),
    ("Vehicles", lambda d: d.startswith(("Icon_Vehicles", "Vehicles"))),
    ("Atlas sheets", lambda d: d.startswith("_Atlas_")),
]
GROUPS = [name for name, _ in GROUP] + ["Other"]


def group_of(d):
    for name, test in GROUP:
        if test(d):
            return name
    return "Other"


def main():
    rows = []
    for d in sorted(os.listdir(HERE)):
        sub = os.path.join(HERE, d)
        if not os.path.isdir(sub) or d.startswith("_tools") or d == "_previews":
            continue
        g = group_of(d)
        for f in sorted(os.listdir(sub)):
            if not f.lower().endswith(".png"):
                continue
            rows.append({"src": d + "/" + f, "name": f[:-4], "meta": d, "g": g})

    folders = len({r["meta"] for r in rows})
    print("%s icons across %d folders" % (format(len(rows), ","), folders))

    G.render(
        os.path.join(HERE, "index.html"),
        here="items",
        h1="Item Icons",
        sub=("__N__ item, equipment, costume and mount icons across __F__ folders, kept in the "
             "game's own grouping. <code>_Atlas_*</code> holds packed sheets plus every sprite "
             "sliced out of them. Names are internal pinyin and rarely match the English item "
             "name &mdash; see the repo README."
             ).replace("__N__", format(len(rows), ",")).replace("__F__", str(folders)),
        rows=rows,
        groups=GROUPS,
        placeholder="search filename or folder…",
        min_width=112,
        page=600,
    )


if __name__ == "__main__":
    main()
