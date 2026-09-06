"""Compose the tiled world-map textures into single images (verified layouts)."""
import os
import numpy as np
from PIL import Image

D = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps\UI_MapBackground"
OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps"


def compose(grid, outname):
    rows, cols = len(grid), len(grid[0])
    tiles = [[Image.open(os.path.join(D, n)).convert("RGB") for n in row] for row in grid]
    w, h = tiles[0][0].size
    canvas = Image.new("RGB", (w * cols, h * rows))
    for r, row in enumerate(tiles):
        for c, im in enumerate(row):
            canvas.paste(im, (c * w, r * h))
    canvas.save(os.path.join(OUT, outname))
    print(f"{outname}: {canvas.size}")


# Both sheets are 2x2, laid out low tile-number first (top-left -> bottom-right).
compose([["RO_Map_BG3.png", "RO_Map_BG4.png"],
         ["RO_Map_BG5.png", "RO_Map_BG6.png"]], "WorldMap_Full.png")

compose([["RO_MiaoMap_BG3.png", "RO_MiaoMap_BG4.png"],
         ["RO_MiaoMap_BG5.png", "RO_MiaoMap_BG6.png"]], "WorldMap_Miao_Full.png")

# What are RO_Map_BG1 / BG2? Compare them against every other tile.
names = [f"RO_Map_BG{n}.png" for n in range(1, 7)] + \
        [f"RO_MiaoMap_BG{n}.png" for n in range(3, 7)]
arrs = {n: np.asarray(Image.open(os.path.join(D, n)).convert("RGB"), dtype=np.float32)
        for n in names}
print("\nmean abs pixel diff vs RO_Map_BG1 / RO_Map_BG2:")
for probe in ("RO_Map_BG1.png", "RO_Map_BG2.png"):
    scores = sorted(((float(np.mean(np.abs(arrs[probe] - arrs[n]))), n)
                     for n in names if n != probe))
    print(f"  {probe}: " + ", ".join(f"{n}={s:.1f}" for s, n in scores[:4]))
