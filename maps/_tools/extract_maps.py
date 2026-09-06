"""Extract Texture2D/Sprite images out of ROOC UnityFS .ab bundles."""
import os, sys, traceback
import UnityPy

ROOT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Extracted_158"
OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Maps"

# (label, path relative to ROOT, recurse) -- path may be a dir or a single .ab file
JOBS = [
    # ("SceneMaps", r"Resources\UI\Texture\Map", False),  # already done
    ("UI_Atlas_Map", r"Resources\UI\Atlas\Map.png.ab", False),
    ("UI_Atlas_Map", r"Resources\UI\Atlas\MapUI.png.ab", False),
    ("UI_Atlas_Map", r"Resources\UI\Atlas\PreyMap.png.ab", False),
    ("UI_Atlas_Map", r"Resources\UI\Atlas\CrossGVGMap.png.ab", False),
    ("UI_Atlas_Map", r"Resources\UI\Atlas\CrossGVGMap2.png.ab", False),
]

# every other map-named texture bundle found by name scan
for _rel in [
    r"Resources\UI\Texture\CommonBackground\UI_Common_NewMap.png.ab",
    r"Resources\UI\Texture\CommonBackground\UI_Common_NewMap_Miao.png.ab",
    r"Resources\UI\Texture\Freya\Fx_Ui_WorldMap_Swirl01.png.ab",
    r"Resources\UI\Texture\Welfare\UI_Welfare_HappyMap.png.ab",
    r"Resources\UI\Texture\Festival\UI_Ditu_ContestCenter.png.ab",
    r"Resources\UI\Texture\ExploreGuide\ExploreGuide_tansuoditu.jpg.ab",
    r"Resources\UI\Texture\ExploreGuide\ExploreGuide_tansuoditu01.jpg.ab",
]:
    JOBS.append(("UI_MapArt", _rel, False))

for _n in range(1, 7):
    JOBS.append(("UI_MapBackground", rf"Resources\UI\Texture\PrefabBg\RO_Map_BG{_n}.png.ab", False))
for _n in range(3, 7):
    JOBS.append(("UI_MapBackground", rf"ADeleted\Resources\UI\Texture\PrefabBg\RO_MiaoMap_BG{_n}.png.ab", False))

for _s in ["backdrop", "PhotosBG", "xiaoyeqian"]:
    JOBS.append(("UI_MapStoryBook", rf"Resources\UI\Texture\Story\UI_map_book_{_s}.png.ab", False))
for _s in ["ExploreGift", "Fellowship_BG", "Fellowship_Sticker", "FrameBGL", "FrameBGR"]:
    JOBS.append(("UI_MapStoryBook", rf"Resources\UI\Texture\Story\UI_map_{_s}.png.ab", False))
JOBS.append(("UI_MapStoryBook", r"Resources\UI\Texture\Story\UI_Map_StoryFrame.png.ab", False))

for _m in ["Beisen", "Bolidao", "Chenchuan", "Feiyangshulin", "Gebulingsenlin", "Huayuan",
           "Jinzitaerceng", "Mayidong", "Mlknanbu", "Nanmen", "Shourencunluo", "Xiashuidao"]:
    JOBS.append(("MVP_MapImages",
                 rf"Resources\UI\Texture\MonsterIllustrated\UI_Activity_Mvp_Map_{_m}.png.ab", False))


def sanitize(name):
    for c in '<>:"/\\|?*':
        name = name.replace(c, "_")
    return name.strip() or "unnamed"


def bundles(rel, recurse):
    base = os.path.join(ROOT, rel)
    if os.path.isfile(base):
        return [base]
    out = []
    for dirpath, dirnames, filenames in os.walk(base):
        # never descend into pre-unpacked CAB dirs
        dirnames[:] = [d for d in dirnames if not d.endswith(".ab_unpacked")]
        out += [os.path.join(dirpath, f) for f in filenames if f.lower().endswith(".ab")]
        if not recurse:
            break
    return sorted(out)


def main():
    total_ok = total_fail = 0
    for label, rel, recurse in JOBS:
        outdir = os.path.join(OUT, label)
        os.makedirs(outdir, exist_ok=True)
        files = bundles(rel, recurse)
        print(f"\n=== {label}: {len(files)} bundles from {rel} ===", flush=True)
        ok = fail = 0
        for i, path in enumerate(files, 1):
            try:
                env = UnityPy.load(path)
                wrote = 0
                for obj in env.objects:
                    if obj.type.name not in ("Texture2D", "Sprite"):
                        continue
                    data = obj.read()
                    img = data.image
                    if img is None:
                        continue
                    name = sanitize(getattr(data, "m_Name", "") or
                                    os.path.basename(path).split(".")[0])
                    dest = os.path.join(outdir, name + ".png")
                    n = 1
                    while os.path.exists(dest):
                        dest = os.path.join(outdir, f"{name}_{n}.png")
                        n += 1
                    img.save(dest)
                    wrote += 1
                if wrote:
                    ok += 1
                else:
                    fail += 1
                    print(f"  [no image] {os.path.basename(path)}", flush=True)
            except Exception as e:
                fail += 1
                print(f"  [ERROR] {os.path.basename(path)}: {e}", flush=True)
            if i % 25 == 0:
                print(f"  ... {i}/{len(files)}", flush=True)
        print(f"=== {label} done: {ok} ok, {fail} failed ===", flush=True)
        total_ok += ok
        total_fail += fail
    print(f"\nTOTAL: {total_ok} bundles exported, {total_fail} failed")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
