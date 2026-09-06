"""Extract every item/equipment/costume icon out of the ROOC bundles."""
import os, sys
import UnityPy

ROOT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Extracted_158"
OUT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Items"

# Per-item icon bundles, one texture each.
ICON_DIRS = [
    r"Resources\UI\Texture\DynamicImage",
    r"_UI",
    r"ADeleted\Resources\UI\Texture\DynamicImage",
]

# Packed icon atlases -- exported as the full sheet plus every sprite sliced out.
ATLASES = [
    "Icon01.png.ab", "Icon02.png.ab", "IconMain.png.ab",
    "IconMain_Anniversary2025.png.ab", "Icon_ItemAvatar01.png.ab",
    "Icon_ItemMedal01.png.ab", "Icon_PokemonItem.png.ab",
    "Icon_Item_bingo.png.ab", "Icon_Doodad.png.ab",
    "Icon_Function01.png.ab", "Icon_Guild01.png.ab",
]


def sanitize(n):
    for c in '<>:"/\\|?*':
        n = n.replace(c, "_")
    return n.strip() or "unnamed"


def export(path, outdir):
    """Returns number of images written."""
    os.makedirs(outdir, exist_ok=True)
    env = UnityPy.load(path)
    wrote = 0
    for obj in env.objects:
        if obj.type.name not in ("Texture2D", "Sprite"):
            continue
        try:
            data = obj.read()
            img = data.image
            if img is None:
                continue
            name = sanitize(getattr(data, "m_Name", "") or
                            os.path.basename(path).split(".")[0])
            dest = os.path.join(outdir, name + ".png")
            n = 1
            while os.path.exists(dest):
                dest = os.path.join(outdir, f"{name}__{n}.png")
                n += 1
            img.save(dest)
            wrote += 1
        except Exception as e:
            print(f"    [obj err] {os.path.basename(path)}: {e}", flush=True)
    return wrote


def main():
    total = fails = 0

    # 1. per-item icon folders
    for base in ICON_DIRS:
        basedir = os.path.join(ROOT, base)
        if not os.path.isdir(basedir):
            continue
        for sub in sorted(os.listdir(basedir)):
            subdir = os.path.join(basedir, sub)
            if not os.path.isdir(subdir) or subdir.endswith(".ab_unpacked"):
                continue
            files = [f for f in sorted(os.listdir(subdir)) if f.lower().endswith(".ab")]
            if not files:
                continue
            outdir = os.path.join(OUT, sub)
            n = 0
            for f in files:
                try:
                    n += export(os.path.join(subdir, f), outdir)
                except Exception as e:
                    fails += 1
                    print(f"  [ERROR] {sub}/{f}: {e}", flush=True)
            total += n
            print(f"{sub:<34} {len(files):>5} bundles -> {n:>5} png", flush=True)

    # 2. packed atlases
    adir = os.path.join(ROOT, r"Resources\UI\Atlas")
    for a in ATLASES:
        p = os.path.join(adir, a)
        if not os.path.exists(p):
            print(f"{a:<34} MISSING", flush=True)
            continue
        outdir = os.path.join(OUT, "_Atlas_" + a.split(".")[0])
        try:
            n = export(p, outdir)
            total += n
            print(f"{a:<34} atlas          -> {n:>5} png", flush=True)
        except Exception as e:
            fails += 1
            print(f"  [ERROR] {a}: {e}", flush=True)

    print(f"\nTOTAL {total} images written, {fails} bundle errors")
    print("Output:", OUT)


if __name__ == "__main__":
    main()
