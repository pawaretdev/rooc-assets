# rooc-assets

Art extracted from a Ragnarok Origin (ROOC) client — Unity 2019.4.36f1, plain
unencrypted `UnityFS` bundles.

## Contents

| Path | Files | What |
|---|---|---|
| [`maps/`](maps/) | 850 | World map, per-zone maps, map UI art |
| [`items/`](items/) | ~6,700 | Item, equipment, costume and mount icons |
| [`hotupdate/`](hotupdate/) | 8,591 | **Patch content** — everything added after the base install |

Open the index pages in a browser:

- `hotupdate/index.html` — all 8,591 patch images, searchable, grouped
- `items/ItemIndex.html` — the base item icon set
- `maps/MapIndex.html` — all 199 per-zone maps
- `maps/WorldMapUI.html` — working demo of the in-game world map (pan/zoom,
  clickable grid cells, side panel per zone)

## The two asset sources — this matters

The installed game keeps content in two places, and they hold different things:

```
StreamingAssets/
├── AssetBundles/   5.3 GB   base install, 69,922 bundles → maps/ and items/
└── HotUpdate/      693 MB   patched in later, 2,804 .ab  → hotupdate/
```

**Anything added to the game after release lives only in `HotUpdate/`.** Two dumps
of `AssetBundles/` taken three weeks apart were byte-identical except for one font
bundle — the base set barely moves. New items, new UI systems and new fashion all
arrive through `HotUpdate/`.

`HotUpdate` bundle filenames are numeric hashes (`928232677.ab`), so you cannot
find anything by path — you have to open every bundle and read the asset names
inside. [`hotupdate/manifest.json`](hotupdate/manifest.json) records the mapping
(asset name, type, pixel size, source bundle) for all 8,591 images.

The other 3,810 files in `HotUpdate/` are `.robytes` — LuaJIT bytecode and
protobuf config, not images.

### Notable finds in hotupdate/

- `UI_Icon_item_Starpupils_*` — the **Astroco / Main-Star** system (in-game
  "Destroyer Starcore" = `UI_Icon_item_Starpupils_Attack01`). 6 constellations
  (Cat, Fairy, Shooter, Snake, Snowflake, Sun) plus Attack/Defense cores.
- `UI_SuperDivineRealmChallenge_*` — a whole UI system absent from the base dump.
- 156 item icons that do not exist in `items/` at all.

## maps/

- `WorldMap_Full.png` (2048²) — stitched from the four `RO_Map_BG3..6` tiles
- `WorldMap_Miao_Full.png` (2048²) — the Miao / sea-region map
- `worldmap_cells.json` — **where every zone sits on the world map**, in pixels,
  read from `Resources/UI/Prefabs/WorldMap.prefab`. 57 cells on the main map,
  5 on Miao; each zone is one 76×76-unit cell = 91.34 px. See `maps/README.md`
  for the coordinate transform.
- `SceneMaps/` — 199 per-zone map images (`sc_<zone>_<nnn>.png`)
- `_verify_WorldMap_*.png` — grid + scene IDs drawn over the map, to check alignment

## items/

Grouped by the game's own folders: `Icon_ItemConsumables01..07`, `Icon_ItemEquip*`,
`Icon_ItemMaterial*`, `Icon_Wear_*` (costumes), `Icon_Vehicles*`, plus `_Atlas_*`
holding packed sheets and every sprite sliced out of them.

`items/_previews/` holds side-by-side comparison sheets built while identifying
specific icons (card fragments, binding stones, star candidates).

## Known limits

- **No name tables.** Zone and item names resolve at runtime from a localization
  string table that is not shipped as an asset bundle, so filenames are the
  game's internal names — mostly Chinese pinyin, and often unrelated to the
  English name. `古魔石 (gumoshi)` is "Binding Stone"; `绿蓝卡碎片 (lvlankasuipian)`
  is "Rare Card Fragment"; the Astroco system is `Starpupils`. Searching by the
  English name will not work.
- The 26 zone labels in `worldmap_cells.json` were matched by hand against an
  in-game screenshot, not read from game data. The other 31 cells are blank.
- Map icons and NPC markers seen in-game are a runtime overlay, not baked in.

## Reproducing

`maps/_tools/`, `items/_tools/` and `hotupdate/_tools/` hold the extraction
scripts. They use [UnityPy](https://github.com/K0lb3/UnityPy), not AssetStudio —
the machine had no .NET SDK and AssetStudio 0.16.47 ships GUI-only, so its DLLs
could not be scripted.

```
python -m venv venv
venv\Scripts\python -m pip install UnityPy numpy pillow
venv\Scripts\python hotupdate\_tools\extract_hotupdate.py
```

## Note

These are extracted assets from a commercial game and remain the property of
their rights holders. Kept here for reference and tooling work.
