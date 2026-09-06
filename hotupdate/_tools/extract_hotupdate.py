"""Extract every image out of the game's HotUpdate patch bundles.

HotUpdate holds the content that AssetBundles/ (the base install) does not --
new items, new UI systems, new fashion. Bundle filenames are numeric hashes, so
a manifest records which bundle each asset came from.
"""
import os, json, sys
import UnityPy

H = r"C:\Program Files (x86)\roocalive\exe\rooc_Data\StreamingAssets\HotUpdate"
OUT = r"C:\Users\pawar\rooc-assets\hotupdate"
IMG = os.path.join(OUT, "images")


def sanitize(n):
    for c in '<>:"/\|?*':
        n = n.replace(c, "_")
    n = n.strip()
    if n.lower().endswith(".png"):
        n = n[:-4]
    return n or "unnamed"


os.makedirs(IMG, exist_ok=True)
files = sorted(f for f in os.listdir(H) if f.endswith(".ab"))
print(f"{len(files)} bundles", flush=True)

manifest, wrote, errs = [], 0, 0
for i, f in enumerate(files, 1):
    try:
        env = UnityPy.load(os.path.join(H, f))
    except Exception:
        errs += 1
        continue
    for o in env.objects:
        if o.type.name not in ("Texture2D", "Sprite"):
            continue
        try:
            d = o.read()
            img = d.image
            if img is None:
                continue
            nm = sanitize(str(getattr(d, "m_Name", "")))
            dest = os.path.join(IMG, nm + ".png")
            k = 1
            while os.path.exists(dest):
                dest = os.path.join(IMG, f"{nm}__{k}.png")
                k += 1
            img.convert("RGBA").save(dest)
            manifest.append({"file": os.path.basename(dest), "name": nm,
                             "type": o.type.name, "bundle": f,
                             "w": img.width, "h": img.height})
            wrote += 1
        except Exception:
            errs += 1
    if i % 250 == 0:
        print(f"  {i}/{len(files)}  images={wrote}  errors={errs}", flush=True)

with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=1)
print(f"DONE {wrote} images, {errs} errors -> {IMG}", flush=True)
