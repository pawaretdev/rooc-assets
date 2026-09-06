"""Convert WorldMap.prefab cell nodes into pixel coords on WorldMap_Full.png,
emit JSON, and render a verification overlay."""
import json, io, os
from PIL import Image, ImageDraw, ImageFont

SP = os.path.dirname(os.path.abspath(__file__))
OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps"

d = json.load(io.open(os.path.join(SP, "wm_panels.json"), encoding="utf-8"))

# --- coordinate frame, from the four BG tiles (852x852 each, 2x2) -------------
# BG3 pivot(1,.5)@(-90,681)   BG4 pivot(0,.5)@(-90,681)    <- top row
# BG1 pivot(1,.5)@(-90,-170)  BG2 pivot(0,.5)@(-90,-170)   <- bottom row
MAP_L, MAP_R = -942.0, 762.0          # 1704 wide
MAP_B, MAP_T = -596.0, 1107.0         # 1703 tall
UNITS = MAP_R - MAP_L                 # 1704
IMG = 2048                            # WorldMap_Full.png is 2048x2048
S = IMG / UNITS                       # units -> px

CELL_UNITS = 76.0                     # every Panel_BtnMaps child is 76x76


def to_px(bx, by):
    return ((bx - MAP_L) * S, (MAP_T - by) * S)


def panel_children(panel, node):
    for e in d.get(f"{panel}::{node}", []):
        return e
    return None


def collect(panel):
    btn = panel_children(panel, "Panel_BtnMaps")
    cells = []
    if btn:
        ox, oy = btn["pos"]                       # panel offset inside Bgs
        for c in btn["children"]:
            cx, cy = c["pos"]
            bx, by = ox + cx, oy + cy             # centre, Bgs space
            w, h = c["size"]
            px, py = to_px(bx, by)
            cells.append({
                "id": c["name"],
                "center_px": [round(px, 1), round(py, 1)],
                "rect_px": [round(px - w * S / 2, 1), round(py - h * S / 2, 1),
                            round(w * S, 1), round(h * S, 1)],
                "unity_pos": [bx, by],
                "size_units": [w, h],
            })
    # named cave/landmark labels
    labels = []
    cave = panel_children(panel, "Panel_CaveInfo")
    if cave:
        ox, oy = cave["pos"]
        for c in cave["children"]:
            if c["name"].lower().startswith("arrow") or c["name"].isdigit():
                continue
            bx, by = ox + c["pos"][0], oy + c["pos"][1]
            px, py = to_px(bx, by)
            labels.append({"name": c["name"], "center_px": [round(px, 1), round(py, 1)]})
    return cells, labels


result = {
    "image": {"file": "WorldMap_Full.png", "width": IMG, "height": IMG},
    "grid": {"cell_px": round(CELL_UNITS * S, 2),
             "note": "every clickable zone is one 76x76-unit cell = "
                     f"{CELL_UNITS * S:.1f}px on the 2048px world map"},
    "maps": {},
}
for panel, img in (("Panel_DefaultWorldMap", "WorldMap_Full.png"),
                   ("Panel_MiaoWorldMap", "WorldMap_Miao_Full.png")):
    cells, labels = collect(panel)
    result["maps"][panel] = {"image": img, "cells": cells, "cave_labels": labels}
    print(f"{panel}: {len(cells)} cells, {len(labels)} cave labels")

dest = os.path.join(OUT, "worldmap_cells.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
print("->", dest)

# --- verification overlay ----------------------------------------------------
for panel, img in (("Panel_DefaultWorldMap", "WorldMap_Full.png"),
                   ("Panel_MiaoWorldMap", "WorldMap_Miao_Full.png")):
    src = os.path.join(OUT, img)
    if not os.path.exists(src):
        continue
    im = Image.open(src).convert("RGB")
    dr = ImageDraw.Draw(im, "RGBA")
    try:
        font = ImageFont.truetype("arialbd.ttf", 30)
        fsmall = ImageFont.truetype("arial.ttf", 22)
    except Exception:
        font = fsmall = ImageFont.load_default()
    for c in result["maps"][panel]["cells"]:
        x, y, w, h = c["rect_px"]
        dr.rectangle([x, y, x + w, y + h], outline=(0, 255, 120, 255), width=3)
        dr.rectangle([x, y, x + w, y + h], fill=(0, 255, 120, 40))
        t = c["id"]
        dr.text((x + w / 2, y + h / 2), t, fill=(255, 40, 40, 255),
                font=font, anchor="mm", stroke_width=4, stroke_fill=(255, 255, 255, 255))
    for l in result["maps"][panel]["cave_labels"]:
        x, y = l["center_px"]
        dr.text((x, y), l["name"], fill=(30, 60, 255, 255), font=fsmall, anchor="mm",
                stroke_width=3, stroke_fill=(255, 255, 255, 255))
    outp = os.path.join(OUT, "_verify_" + img)
    im.save(outp)
    print("->", outp)
