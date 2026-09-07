# cards/

Monster card art from `Resources/UI/Texture/MonsterCard` — one `UnityFS` bundle
per card, one `Texture2D` inside, nothing packed into an atlas.

| Path | Files | What |
|---|---|---|
| `images/` | 452 | Every card texture in the dump |
| `manifest.json` | — | name, pixel size and source bundle for each |
| `index.html` | — | searchable grid, open it in a browser |

Three shapes come out:

| Size | Count | What |
|---|---|---|
| 300×400 | 444 | The classic RO card — illustration with the rarity frame and the monster's English name **baked into the texture** |
| 256×512 | 7 | Frameless full art (`HuKeLian`, `KaPuLa`, `Weiguo*`) — a different, newer style |
| 156×192 | 1 | `UI_MonsterCardBack`, the shared card back |

The green `Card: Poring` title bar seen in game is a runtime UI overlay drawn on
top, not part of the texture.

## Names

Filenames are the game's internal pinyin, so searching by the English name will
not work — Poring is `Boli` (波利):

| File | In game |
|---|---|
| `UI_MonsterCard_Boli` | Poring |
| `UI_MonsterCard_Boboli` | Poporing |
| `UI_MonsterCard_Bingboli` | Ice Poring |
| `UI_MonsterCard_Tianshiboli` | Angeling |
| `UI_MonsterCard_Emoboli` | Deviling |
| `UI_MonsterCard_Bolizhiwang` | Poring King |

The 300×400 textures do carry the English name in the artwork itself, so the
fastest way to find a card is to open `index.html` and look.

A `_01` suffix marks a second variant of the same card; `_zn` and `_kkm` suffixes
appear on a handful and are the game's own tags, not something added here.

## Extracting

```
venv\Scripts\python cards\_tools\extract_cards.py    # bundles -> images/ + manifest.json
venv\Scripts\python cards\_tools\card_gallery.py     # manifest.json -> CardIndex.html
```

`extract_cards.py` reads `ROOC_Extracted_69`; change `ROOT` at the top of the file
to point at another dump. See [../EXTRACTING.md](../EXTRACTING.md) for how those
dumps are produced.

## `001.png` … `225.png`

A pre-existing set of 320×432 cards sitting loose in this folder, English-named
with the `Card: <name>` title bar already composited in. Not produced by the
scripts here and not from the `MonsterCard` bundles — those are 300×400 and carry
no title bar. Origin not recorded.
