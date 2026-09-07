# sprites/

A flat dump of 20,902 sprite PNGs (175 MB) — UI parts, monster and NPC
portraits, costume and headgear thumbnails, emoji, effect frames. One folder,
no subdirectories, no manifest.

Open [`index.html`](index.html) to browse it; the grid is grouped by name prefix
and searchable, which is the only practical way through 20k files.

## Filenames

Most files are named `<asset>.png.png`. The doubled suffix is the extractor's —
it appended `.png` to an asset whose internal name already ended in `.png`. The
index hides it in the label, and nothing here is renamed on disk, so a filename
still matches the game's own asset name exactly.

A handful are messier still (`…5D.png.png`, `png #1004638.png`) where the asset
name itself carried odd characters. They are left as-is for the same reason.

## Groups

Tabs in the index come from the leading token(s) of the asset name — `UI_Icon`,
`UI_Common`, `Monster`, `Fashion`, `NPC`, `Helmet`, `emoji` and so on. A prefix
too rare to earn its own tab falls into **Other**. The grouping is derived at
build time by [`../_tools/rooc_gallery.py`](../_tools/rooc_gallery.py), so it
re-shapes itself as the folder grows rather than needing a hand-kept list.

## Rebuilding the index

```
venv\Scripts\python sprites\_tools\sprite_gallery.py
```

It reads whatever PNGs are in the folder and takes each image's dimensions
straight from the PNG header, so a full pass over 20k files is about a minute.
