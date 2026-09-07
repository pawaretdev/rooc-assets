# ROOC — Extracted map images

Source: `ROOC_Extracted_158` (Unity 2019.4.36f1, plain unencrypted `UnityFS` bundles).

## What's here

| Path | Count | What it is |
|---|---|---|
| `WorldMapUI.html` | — | **Working demo of the in-game world-map UI** — pan/zoom, clickable grid cells, side panel with the zone's map image |
| `worldmap_cells.json` | — | Cell geometry: every clickable zone's rect in pixels on `WorldMap_Full.png` |
| `index.html` | — | Browsable gallery of all 199 per-zone maps, with search and category filters |
| `_verify_WorldMap_*.png` | 2 | The world map with the cell grid + scene IDs drawn on, for checking alignment |
| `WorldMap_Full.png` | 1 | **Full world map** (2048×2048), stitched from `RO_Map_BG3..6` |
| `WorldMap_Miao_Full.png` | 1 | **Miao / sea-region world map** (2048×2048), stitched from `RO_MiaoMap_BG3..6` |
| `SceneMaps/` | 199 | Per-zone map layouts, one per scene (`sc_<zone>_<nnn>.png`) — from `Resources/UI/Texture/Map` |
| `UI_Atlas_Map/` | 399 | Map-UI atlases + every sprite sliced out of them (icons, NPC markers, minimap chrome, CrossGVG land tiles, PreyMap) |
| `UI_MapBackground/` | 10 | The raw 1024×1024 world-map tiles before stitching |
| `UI_MapStoryBook/` | 9 | Story-book map frames and backdrops |
| `UI_MapArt/` | 7 | Misc map artwork (explore-guide map, contest-centre map, etc.) |
| `MVP_MapImages/` | 12 | MVP-spawn zone images (`UI_Activity_Mvp_Map_*`) |

## Where each zone sits on the world map

`Resources/UI/Prefabs/WorldMap.prefab` holds the layout, and it survived extraction intact
because it is plain `RectTransform` data (unlike the `MonoBehaviour` script fields, which are
stripped). `worldmap_cells.json` is that data converted to image pixels.

The frame comes from the prefab's four background tiles — `BG3 BG4 / BG1 BG2`, 852×852 units
each with left/right pivots, so the world spans x ∈ [-942, 762], y ∈ [-596, 1107] in `Bgs`
space. `WorldMap_Full.png` is 2048×2048 over that, giving **2048 / 1704 = 1.2019 px per unit**:

```
px = (bgs_x + 942) * 1.2019          bgs_x = Panel_BtnMaps.x + cell.x   (-22.5 + cell.x)
py = (1107 - bgs_y) * 1.2019         bgs_y = Panel_BtnMaps.y + cell.y   ( 0.0  + cell.y)
```

Every clickable zone is exactly one 76×76-unit cell = **91.34 px**, which lines up with the
white grid squares painted into the map art — see `_verify_WorldMap_Full.png` to confirm.

- 57 cells on the main world map, 5 on the Miao map.
- Cell names in the prefab are the game's **numeric scene IDs**, not zone names.
- 26 of the 57 are labelled in the JSON, matched by hand against an in-game screenshot;
  25 of those are linked to their `SceneMaps/` image. The rest are left blank — see below.
- `cave_labels` holds the dungeon-entrance captions (`Mayidong`, `Jinzita`, `Xiashuidao`, …),
  which *are* baked into the prefab as pinyin object names.

## About the zone names

The per-zone files are named with the game's internal pinyin stems (`sc_pulongdela_001` = Prontera).
The **display names shown in-game are not recoverable from this dump**: `MapNamePanel.prefab` resolves
them through a `UIStringLocal` component, i.e. a localization string table fetched at runtime, and
that table is not an asset bundle. `Resources/Lang/{en,tha,ko,ja,zh,...}` contains only fonts and
localized images, no text.

So the labels in `index.html` are **my identification from the pinyin**, not game data.
Labels shown in yellow or ending in `?` are uncertain — check them against the thumbnail.
`sc_pulongdela_001` is the only one verified directly against an in-game screenshot.

The icons, NPC markers and place labels you see on the map in-game are drawn as a runtime overlay
(sprites from `UI_Atlas_Map/`); they are not baked into these textures.

## Notes

- `RO_Map_BG1.png` / `RO_Map_BG2.png` (in `UI_MapBackground/`) are two orphan corner tiles from a
  different/older world-map sheet — the other two tiles of that sheet are not present in this dump,
  so they are left unstitched.
- `UI_Atlas_Map/MapUI.png` is a 71-byte stub: that atlas holds only sprite rects, no packed texture
  of its own. The sprites it references were still exported individually.
- Zone names are Chinese pinyin, e.g. `sc_ailebeita_*` = Al De Baran, `sc_bolidao_*` = Byalan,
  `sc_jinzita*` = Pyramid, `sc_mayidong*` = Ant Hell.

## Reproducing / extracting more

`extract_maps.py` and `stitch.py` are in `_tools/`. They use UnityPy (not AssetStudio — this machine
has no .NET SDK and AssetStudio 0.16.47 ships GUI-only, so its DLLs could not be scripted).

```
python -m venv venv
venv\Scripts\python -m pip install UnityPy numpy
venv\Scripts\python _tools\extract_maps.py
```

Edit the `JOBS` list in `extract_maps.py` to point at any other bundle folder under
`ROOC_Extracted_158`.
