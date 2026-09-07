# Extracting the game folder

How the dumps in this repo were produced: **RoBlockExtractor** turns the game's
packed `.block` archives back into a normal folder tree of Unity asset bundles,
then **AssetStudio** is used to see what is inside them.

## Tools

| Tool | Version used | Notes |
|---|---|---|
| RoBlockExtractor | torachiyo, 2024 (RaGEZONE release) | .NET Framework 4.6. Ships as `RoBlockExtractor.exe` (CLI) + `RoBlockExtractorGUI.exe` (WPF front-end) + `MoonClient.dll` + `MoonCommonLib.dll` — keep all four in one folder, the GUI shells out to the CLI next to it and otherwise says *"Can not find RoBlockExtractor.exe"*. |
| [AssetStudio](https://github.com/Perfare/AssetStudio) | net6 v0.16.47 | Needs the .NET 6 **Desktop** runtime. GUI only — it has no scriptable CLI, which is why the `_tools/` scripts in this repo use UnityPy instead. |

## 1. Where the game keeps its assets

```
C:\Program Files (x86)\roocalive\exe\rooc_Data\StreamingAssets\
├── AssetBundles\          5.3 GB   ← the base install, what you extract
│   ├── dep.all                     6 MB dependency table
│   └── BLOCK\
│       ├── BLOCK.blockinfo         index: which asset lives in which block
│       └── BLOCK1..106.block       ~50 MB each, 69,922 bundles packed inside
├── HotUpdate\             693 MB   ← patch content, loose files (see below)
├── Unzips\                1.0 GB
└── ZipFiles\              698 MB
```

`AssetBundles\` is the only part RoBlockExtractor handles. A `.block` file is
just a concatenation of many `UnityFS` bundles; `BLOCK.blockinfo` + `dep.all`
say where each one starts and what its original asset path was.

## 2. Run RoBlockExtractor

Open `RoBlockExtractorGUI.exe`, set the two paths, press **Generate**.

**Source path — pick `...\StreamingAssets\AssetBundles`, not `StreamingAssets`.**
The extractor looks for `dep.all` and `BLOCK\BLOCK.blockinfo` *directly* inside
whatever folder you give it. Point it one level too high and it dies with an
unhandled exception:

```
Unhandled Exception: System.IO.FileNotFoundException: Could not find file
'C:\...\rooc_Data\StreamingAssets\dep.all'.
```

So the correct pair is:

| Field | Value |
|---|---|
| Source path | `C:\Program Files (x86)\roocalive\exe\rooc_Data\StreamingAssets\AssetBundles` |
| Destination path | anywhere with ~6 GB free, e.g. `D:\ROOC_Extracted_158` |

Name the destination after the client patch it came from — the dumps behind this
repo are `ROOC_Extracted_69` and `ROOC_Extracted_158`, and keeping two lets you
diff a patch against the previous one. `StreamingAssets\build_info.txt` records
the build date (`Build from HLPC01396-ROO at 2025/11/3`) and `config.json` a
`SourceVersion`, but neither matches the patch number players see.

### Gotchas

- **Run it as Administrator**, or copy `AssetBundles\` somewhere writable first.
  `readDepFile` opens `dep.all` with `FileMode.Open`, which asks for *read/write*
  access; under `Program Files` a normal user gets
  `System.UnauthorizedAccessException: Access to the path '...\dep.all' is denied`
  and the process crashes.
- **Don't extract into a OneDrive-synced folder** unless you mean it — it is
  ~70,000 files and OneDrive will try to upload all of them.
- Close the game first. Blocks are read-only, but the launcher rewrites
  `StreamingAssets\` during patching.

### Same thing from a terminal

The GUI is only a wrapper; the CLI takes the two paths as positional arguments
and is easier to script or re-run:

```
RoBlockExtractor.exe "C:\Program Files (x86)\roocalive\exe\rooc_Data\StreamingAssets\AssetBundles" "D:\ROOC_Extracted_158"
```

```
Extracting 0/69923
Extracting 1/69923
...
done
```

It walks all 106 blocks in one pass and prints a running count; expect tens of
minutes for the full 5.3 GB, and note there is no resume — a crash means
starting over.

## 3. What you get

A directory tree that mirrors the game's own asset paths, with one `UnityFS`
bundle per asset — the original extension is kept and `.ab` is appended:

```
ROOC_Extracted_158\          69,922 bundles in total
├── Resources\       the bulk of it: UI, Prefabs, Scenes, Anims, Textures, Lang, Effects
│   └── UI\
│       ├── Atlas\   packed sprite sheets
│       ├── Texture\ DynamicImage\ — the item icons
│       └── Prefabs\ WorldMap.prefab, all UI layouts
├── _GameRes\        models, maps, scene data
├── _Creature\       monsters, NPCs, player parts
├── _UI\             extra icon folders (Icon_ItemConsumables01, Vehicles, Wedding, ...)
├── ADeleted\        cut content still shipped in the client
└── _CutSceneResources\, Assets\, PostProcess\, T4M\, ThirdParty\
```

e.g. `Resources\UI\Texture\Festival\UI_Festival_passcheckp1.png.ab` is one PNG
inside one bundle. Nothing is encrypted — plain Unity 2019.4.36f1 `UnityFS`.

## 4. Browse it in AssetStudio

1. Launch `AssetStudioGUI.exe`.
2. **File → Load folder**, pick the extracted folder.
3. **Asset List** tab — sort by *Type* / *Name*, use the filter box, preview by
   clicking. **Export → Filtered assets** writes the real files out.

**Load a subfolder, not the root.** Loading all 69,922 bundles keeps every asset
in memory and will grind or run out of RAM. Pick what you actually want:

| Looking for | Load |
|---|---|
| Item / equipment icons | `Resources\UI\Texture\DynamicImage`, `_UI\Icon_*` |
| Packed sprite sheets | `Resources\UI\Atlas` |
| Maps and world map data | `_GameRes`, `Resources\UI\Prefabs` |
| Monsters / NPCs / costumes | `_Creature` |

AssetStudio is the right tool for *looking* — for bulk, repeatable extraction the
scripts under `maps/_tools/`, `items/_tools/` and `hotupdate/_tools/` use UnityPy
against the same folder (see [README.md](README.md#reproducing)).

## HotUpdate is a separate job

`StreamingAssets\HotUpdate\` is **not** block-packed, so RoBlockExtractor does
not apply. It is 6,634 loose files — 2,804 `.ab` bundles and ~3,800 `.robytes`
(LuaJIT bytecode and protobuf config, not assets) — with hashed filenames like
`928232677.ab`. Copy the folder somewhere and point AssetStudio or UnityPy at it
directly; because the filenames carry no path, the only way to know what a bundle
holds is to open it and read the asset names inside. See
[`hotupdate/manifest.json`](hotupdate/manifest.json) for the name mapping and
the "two asset sources" section of [README.md](README.md) for why anything added
after release is only ever found here.
