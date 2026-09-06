"""Dump every panel under Bgs of WorldMap.prefab with child positions + anchors."""
import json, os, UnityPy

PATH = (r"c:\Users\pawar\OneDrive\เดสก์ท็อป\ROOC_Extracted_158"
        r"\Resources\UI\Prefabs\WorldMap.prefab.ab")
SP = os.path.dirname(os.path.abspath(__file__))

env = UnityPy.load(PATH)
rts, name_of = {}, {}
for obj in env.objects:
    if obj.type.name in ("RectTransform", "Transform"):
        try:
            rts[obj.path_id] = obj.read()
        except Exception:
            pass
for pid, rt in rts.items():
    try:
        name_of[pid] = rt.m_GameObject.read().m_Name
    except Exception:
        name_of[pid] = "?"

kids, parent = {}, {}
for pid, rt in rts.items():
    f = getattr(rt, "m_Father", None)
    fid = getattr(f, "path_id", 0) if f else 0
    parent[pid] = fid
    if fid in rts:
        kids.setdefault(fid, []).append(pid)


def v(rt, attr):
    o = getattr(rt, attr, None)
    return [round(getattr(o, "x", 0), 2), round(getattr(o, "y", 0), 2)] if o else [0, 0]


def node(pid):
    rt = rts[pid]
    return {"name": name_of[pid], "pos": v(rt, "m_AnchoredPosition"),
            "size": v(rt, "m_SizeDelta"), "amin": v(rt, "m_AnchorMin"),
            "amax": v(rt, "m_AnchorMax"), "pivot": v(rt, "m_Pivot"),
            "nkids": len(kids.get(pid, []))}


def chain(pid):
    out = []
    while pid in rts:
        out.append(name_of[pid])
        pid = parent.get(pid, 0)
    return "/".join(reversed(out))


# every node whose parent chain contains "Bgs": dump the panel level
out = {}
for pid, nm in name_of.items():
    p = chain(pid)
    if "/Bgs/" not in p or p.count("/") != 6:      # WorldMap/Panel_X/mapSV/Viewport/Content/Bgs/<panel>
        continue
    panel = p.split("/")[1]
    entry = dict(node(pid))
    entry["path"] = p
    entry["children"] = [node(c) for c in kids.get(pid, [])]
    out.setdefault(f"{panel}::{nm}", []).append(entry)

dest = os.path.join(SP, "wm_panels.json")
with open(dest, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

for k, v_ in sorted(out.items()):
    for e in v_:
        print(f'{k:<46} children={len(e["children"]):>4}  pos={e["pos"]} size={e["size"]}')
print("\n->", dest)
