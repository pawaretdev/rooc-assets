# -*- coding: utf-8 -*-
"""index.html for the extracted monster cards."""
import json
import os
import sys

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "_tools"))
import rooc_gallery as G  # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(HERE, "manifest.json")

GROUPS = ["Framed", "Full art", "Card back"]


def group_of(e):
    # The 300x400 set carries the classic RO card frame; the handful of 256x512
    # are frameless full art, and UI_MonsterCardBack is the shared card back.
    if tuple(e["size"]) == (300, 400):
        return "Framed"
    return "Card back" if e["name"].endswith("CardBack") else "Full art"


def main():
    with open(MANIFEST, encoding="utf-8") as fh:
        entries = json.load(fh)

    rows = [{
        "src": "images/" + e["file"],
        "name": e["name"].replace("UI_MonsterCard_", ""),
        "meta": "%d×%d" % tuple(e["size"]),
        "g": group_of(e),
    } for e in entries]

    G.render(
        os.path.join(HERE, "index.html"),
        here="cards",
        h1="Monster Cards",
        sub=("__N__ cards from <code>Resources/UI/Texture/MonsterCard</code>. The frame and "
             "the monster's English name are baked into the artwork, so you can read a card "
             "off the grid; the filenames are still the game's internal pinyin "
             "(Poring = <code>Boli</code>). The green <em>Card: …</em> bar seen in game is a "
             "runtime overlay, not part of the texture."
             ).replace("__N__", format(len(rows), ",")),
        rows=rows,
        groups=GROUPS,
        placeholder="search card name…",
        min_width=150,
        aspect="3/4",
        pad=0,
        checker=False,
        page=200,
    )


if __name__ == "__main__":
    main()
