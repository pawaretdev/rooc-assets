# rooc-assets

Art extracted from a Ragnarok Origin (ROOC) client asset dump — build `ROOC_Extracted_158`,
Unity 2019.4.36f1, plain unencrypted `UnityFS` bundles.

**7,520 files · 151.6 MB**

## Contents

| Path | Files | What |
|---|---|---|
| [`maps/`](maps/) | 850 | World map, per-zone maps, map UI art |
| [`items/`](items/) | 6,670 | Item, equipment, costume and mount icons |

Start with the three index pages (open them in a browser):

- `maps/WorldMapUI.html` — working demo of the in-game world map: pan/zoom, clickable
  grid cells, side panel showing each zone's map
- `maps/MapIndex.html` — gallery of all 199 per-zone maps
- `items/ItemIndex.html` — gallery of all 6,662 item icons, searchable

### maps/

- `WorldMap_Full.png` (2048²) — the full world map, stitched from the four
  `RO_Map_BG3..6` tiles
- `WorldMap_Miao_Full.png` (2048²) — the Miao / sea-region world map
- `worldmap_cells.json` — **where every zone sits on the world map**, in pixels.
  Pulled from `Resources/UI/Prefabs/WorldMap.prefab`; 57 cells on the main map, 5 on Miao.
  Each zone is one 76×76-unit cell = 91.34 px. See `maps/README.md` for the transform.
- `SceneMaps/` — 199 per-zone map images (`sc_<zone>_<nnn>.png`)
- `UI_Atlas_Map/`, `UI_MapBackground/`, `UI_MapStoryBook/`, `UI_MapArt/`, `MVP_MapImages/`
- `_verify_WorldMap_*.png` — the grid + scene IDs drawn over the map, for checking alignment

### items/

Grouped by the game's own folders: `Icon_ItemConsumables01..07`, `Icon_ItemEquip*`,
`Icon_ItemMaterial*`, `Icon_Wear_*` (costumes), `Icon_Vehicles*`, plus `_Atlas_*` folders
holding packed sprite sheets and every sprite sliced out of them.

## Known limits

- **No name tables.** Zone and item names are resolved at runtime from a localization
  string table that is not shipped as an asset bundle, so filenames are the game's
  internal names (mostly Chinese pinyin — `sc_pulongdela_001` = Prontera).
- The 26 zone labels in `worldmap_cells.json` were matched by hand against an in-game
  screenshot, not read from game data. The other 31 cells are deliberately left blank.
- Map icons/NPC markers seen in-game are a runtime overlay, not baked into the map images.

## Reproducing

`maps/_tools/` and `items/_tools/` hold the extraction scripts. They use
[UnityPy](https://github.com/K0lb3/UnityPy), not AssetStudio — the machine had no .NET SDK
and AssetStudio 0.16.47 ships GUI-only, so its DLLs could not be scripted.

```
python -m venv venv
venv\Scripts\python -m pip install UnityPy numpy pillow
venv\Scripts\python items\_tools\extract_items.py
```

Edit the job lists at the top of each script to point at other bundle folders.

## Note

These are extracted assets from a commercial game and remain the property of their
rights holders. Kept here for reference/tooling work.
