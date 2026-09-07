# -*- coding: utf-8 -*-
"""Extract every monster card illustration out of the ROOC bundles.

One bundle per card, one Texture2D inside, 300x400 -- the classic RO card
artwork with its rarity frame already baked in. The green "Card: Poring"
title bar seen in game is a runtime UI overlay, not part of the texture.
"""
import json
import os

import UnityPy

ROOT = r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Extracted_69"
SRC = os.path.join(ROOT, r"Resources\UI\Texture\MonsterCard")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images")
MANIFEST = os.path.join(os.path.dirname(OUT), "manifest.json")


def sanitize(n):
    for c in r'<>:"/\|?*':
        n = n.replace(c, "_")
    return n.strip() or "unnamed"


def main():
    os.makedirs(OUT, exist_ok=True)
    bundles = [f for f in sorted(os.listdir(SRC)) if f.lower().endswith(".ab")]
    entries, fails = [], 0

    for f in bundles:
        try:
            env = UnityPy.load(os.path.join(SRC, f))
            for obj in env.objects:
                if obj.type.name != "Texture2D":
                    continue
                data = obj.read()
                img = data.image
                if img is None:
                    continue
                name = sanitize(data.m_Name or f.split(".")[0])
                img.save(os.path.join(OUT, name + ".png"))
                entries.append({
                    "name": name,
                    "file": name + ".png",
                    "size": list(img.size),
                    "bundle": f,
                })
        except Exception as e:
            fails += 1
            print(f"  [ERROR] {f}: {e}", flush=True)

    entries.sort(key=lambda e: e["name"].lower())
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(entries, fh, ensure_ascii=False, indent=1)

    sizes = {}
    for e in entries:
        sizes[tuple(e["size"])] = sizes.get(tuple(e["size"]), 0) + 1
    print(f"{len(bundles)} bundles -> {len(entries)} png, {fails} errors")
    for s, n in sorted(sizes.items(), key=lambda kv: -kv[1]):
        print(f"  {s[0]}x{s[1]:<5} {n}")
    print("Output:", OUT)


if __name__ == "__main__":
    main()
