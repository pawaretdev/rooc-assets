# ROOC — Extracted item icons

6,646 PNGs (101.7 MB) pulled from `ROOC_Extracted_158`. **Open `index.html`** to browse
them with search and category filters.

## Layout

| Folder pattern | What it holds |
|---|---|
| `Icon_ItemConsumables01..07` | Consumables — potions, food, scrolls, boxes (2,700) |
| `Icon_ItemEquip01..09, 20` | Weapons and armour (952) |
| `Icon_ItemMaterial01..07` | Crafting materials, monster drops (643) |
| `Icon_Wear_Head_01..02`, `Icon_Wear_Other_01..02` | Costume / cosmetic pieces (1,339) |
| `Icon_ItemHeadwear01..02` | Headgear (78) |
| `Icon_Vehicles01..02` | Mounts (168) |
| `Icon_ItemDrawing01` | Blueprints (41) |
| `_Atlas_*` | Packed sprite sheets — the full sheet **plus** every sprite sliced out of it |

Sources: `Resources/UI/Texture/DynamicImage/*`, `_UI/*`,
`ADeleted/Resources/UI/Texture/DynamicImage/*`, and the icon atlases in `Resources/UI/Atlas`.
Every one of the ~5,900 icon bundles decoded without error.

## Names

Filenames are the game's internal asset names (pinyin/English mix, e.g.
`UI_icon_item_mapai.png`). **There is no item-name table in this dump** — item names are
resolved at runtime from a localization string table that is not shipped as an asset bundle,
so mapping icon → item name requires the game's config data.

## Re-running

`_tools/extract_items.py` (see `ROOC_Maps/_tools` for the shared venv setup). Edit `ICON_DIRS`
/ `ATLASES` at the top to widen the sweep.
