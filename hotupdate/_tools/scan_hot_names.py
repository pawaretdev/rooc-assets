import os, json, sys, UnityPy
H = r"C:\Program Files (x86)\roocalive\exe\rooc_Data\StreamingAssets\HotUpdate"
out = []
files = sorted(f for f in os.listdir(H) if f.endswith(".ab"))
for i, f in enumerate(files, 1):
    try:
        env = UnityPy.load(os.path.join(H, f))
        for o in env.objects:
            if o.type.name in ("Texture2D", "Sprite"):
                try:
                    d = o.read()
                    out.append({"bundle": f, "type": o.type.name,
                                "name": str(getattr(d, "m_Name", "?"))})
                except Exception:
                    pass
    except Exception:
        pass
    if i % 500 == 0:
        print(f"  {i}/{len(files)}  textures={len(out)}", flush=True)
json.dump(out, open("hot_names.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"TOTAL {len(out)} textures/sprites in {len(files)} bundles")
