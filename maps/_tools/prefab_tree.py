"""Dump the RectTransform hierarchy of a Unity UI prefab bundle."""
import sys, UnityPy

path = sys.argv[1]
maxdepth = int(sys.argv[2]) if len(sys.argv) > 2 else 99

env = UnityPy.load(path)

rts = {}      # path_id -> parsed RectTransform
for obj in env.objects:
    if obj.type.name in ("RectTransform", "Transform"):
        try:
            rts[obj.path_id] = obj.read()
        except Exception as e:
            print("skip", obj.path_id, e)


def go_name(rt):
    try:
        return rt.m_GameObject.read().m_Name
    except Exception:
        return "?"


def fmt(rt):
    bits = []
    for attr in ("m_AnchoredPosition", "m_SizeDelta", "m_AnchorMin", "m_AnchorMax", "m_Pivot"):
        v = getattr(rt, attr, None)
        if v is not None:
            bits.append(f"{attr[2:]}=({getattr(v,'x',0):.1f},{getattr(v,'y',0):.1f})")
    s = getattr(rt, "m_LocalScale", None)
    if s is not None:
        bits.append(f"scale=({s.x:.2f},{s.y:.2f})")
    return "  ".join(bits)


children_of = {}
roots = []
for pid, rt in rts.items():
    f = getattr(rt, "m_Father", None)
    fid = getattr(f, "path_id", 0) if f else 0
    if fid and fid in rts:
        children_of.setdefault(fid, []).append(pid)
    else:
        roots.append(pid)


def walk(pid, d=0):
    if d > maxdepth:
        return
    rt = rts[pid]
    print("  " * d + f"{go_name(rt)}   {fmt(rt)}")
    for c in children_of.get(pid, []):
        walk(c, d + 1)


print(f"# {len(rts)} transforms, {len(roots)} roots")
for r in roots:
    walk(r)
