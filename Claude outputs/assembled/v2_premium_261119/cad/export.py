import os, sys, time, json, csv, collections, math, itertools, shutil
import numpy as np
from build123d import *
import v3 as v2, rast, coupon

SRC = "/mnt/user-data/uploads/HaebotCase v1 Khurshidbek 11-18-2026/step/HaebotCase_v1_assembly_20261118_Khurshidbek.step"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/v2_premium_261119"
for d in ("step", "stl", "3mf", "assembled", "renders", "docs", "cad", "coupon"):
    os.makedirs(f"{OUT}/{d}", exist_ok=True)
t0 = time.time()
P = v2.build(SRC)
print("built", len(P), round(time.time() - t0))

def oriented(shape, orient):
    s = shape
    for ax, ang in orient:
        s = s.rotate({"x": Axis.X, "y": Axis.Y, "z": Axis.Z}[ax], ang)
    b = s.bounding_box()
    return s.translate((-b.min.X, -b.min.Y, -b.min.Z))

# ------------------------------------------------ per-file export (dedupe by file key)
files = collections.OrderedDict()
for p in P:
    if p["kind"] != "print":
        continue
    f = p["file"]
    if f not in files:
        files[f] = dict(p, qty=0)
    files[f]["qty"] += 1
rows = []
DENS = 1.27
for f, p in files.items():
    s = p["shape"]
    export_step(s, f"{OUT}/step/{f}.step")
    o = oriented(p["dshape"], p["orient"])
    export_stl(o, f"{OUT}/stl/{f}.stl", tolerance=0.05, angular_tolerance=0.2)
    b = o.bounding_box()
    vol = s.volume / 1000
    mass = vol * DENS * 0.9
    reused = p["name"].startswith(("tray", "fender")) and p["name"] != "tray_mount"
    rows.append(dict(file=f, qty=p["qty"], color={v2.WHITE: "warm white", v2.CHAR: "charcoal", v2.GREEN: "green",
                                                   v2.GREY: "medium grey", v2.SMOKE: "smoked black"}[p["color"]],
                     material="PETG (ASA final)" if not reused else "PETG",
                     x=round(b.size.X, 1), y=round(b.size.Y, 1), z=round(b.size.Z, 1),
                     fits=max(b.size.X, b.size.Y, b.size.Z) <= 245.0,
                     orientation=p["note"] or "as assembled",
                     mass_g=round(mass, 0), time_h=round(mass / 18.0, 1)))
print("files", len(files), round(time.time() - t0))

# ------------------------------------------------ assembly / exploded
def colored(shape, col, label):
    s = shape.copy() if hasattr(shape, "copy") else shape
    s.color = Color(col); s.label = label
    return s
asm = Compound(label="HaebotCase_v2", children=[colored(p["shape"], p["color"], p["name"]) for p in P])
export_step(asm, f"{OUT}/assembled/HaebotCase_v2_assembly.step")

def xoff(p):
    n = p["name"]; c = p["shape"].bounding_box().center()
    sx = 1 if c.X > 0 else -1; sy = 1 if c.Y > 0 else -1
    up = 90 if (c.Z > v2.ZJ + 5) else 0
    if n.startswith("frame"): return (0, 0, 0)
    if n.startswith("shoulder"): return (0, 0, 260)
    if n.startswith("splice_shoulder"): return (0, 0, 200)
    if n.startswith("lightbar_brow"): return (300, 0, 150)
    if n.startswith("brow"): return (240, 0, 150)
    if n.startswith("post"): return (sx * 120, sy * 120, up)
    if n.startswith("doorcap"): return (330, 0, up)
    if n.startswith("door_") : return (240, 0, up)
    if "_door_" in n: return (90, 0, up)
    if n.startswith("ventcap"): return (0, -320, up)
    if n.startswith("vent_"): return (0, -240, up)
    if "_vent_" in n: return (0, -90, up)
    if n.startswith("rear"): return (-240, 0, up)
    if n.startswith("lightbar_side"): return (0, 310, up)
    if n.startswith("side_L"): return (0, 240, up)
    if n.startswith("plinth"): return (sx * 80, sy * 80, -120)
    if n.startswith("fender"): return (0, sy * 170, -150)
    if n.startswith("tray_mount"): return (150, 0, 150)
    if n == "tray": return (320, 0, 240)
    if n.startswith("keycap"): return (0, sy * 200, 45)
    if n.startswith("key"): return (0, sy * 130, 45)
    return (0, 0, 0)
EXP = [(p, xoff(p)) for p in P]
exp = Compound(label="HaebotCase_v2_exploded",
               children=[colored(p["shape"].translate(o), p["color"], p["name"]) for p, o in EXP])
export_step(exp, f"{OUT}/assembled/HaebotCase_v2_exploded.step")
print("asm", round(time.time() - t0))

# ------------------------------------------------ 3MF (one per colour + all) via trimesh
try:
    import trimesh
    by_col = collections.defaultdict(list)
    for f, p in files.items():
        o = oriented(p["dshape"], p["orient"])
        V, Tt = rast.mesh_of(o, 0.05, 0.2)
        m = trimesh.Trimesh(V, Tt, process=True)
        m.visual.face_colors = (np.array(rast.hex2rgb(p["color"])) * 255).astype(np.uint8).tolist() + [255]
        for q in range(p["qty"]):
            by_col[p["color"]].append((f"{f}_{q + 1}", m.copy()))
    allscene = trimesh.Scene()
    gx = 0
    for col, lst in by_col.items():
        sc = trimesh.Scene()
        x = 0; y = 0; rowh = 0
        for name, m in lst:
            e = m.extents
            if x + e[0] > 240: x = 0; y += rowh + 6; rowh = 0
            T_ = np.eye(4); T_[:3, 3] = [x, y, 0]
            sc.add_geometry(m, node_name=name, geom_name=name, transform=T_)
            T2 = T_.copy(); T2[0, 3] += gx
            allscene.add_geometry(m, node_name=name, geom_name=name, transform=T2)
            x += e[0] + 6; rowh = max(rowh, e[1])
        cname = {v2.WHITE: "white", v2.CHAR: "charcoal", v2.GREEN: "green", v2.GREY: "grey", v2.SMOKE: "smoke"}[col]
        sc.export(f"{OUT}/3mf/plates_{cname}.3mf")
        gx += 400
    allscene.export(f"{OUT}/3mf/HaebotCase_v2_all_parts.3mf")
    print("3mf ok")
except Exception as ex:
    print("3mf failed", ex)

# ------------------------------------------------ coupon
cp = coupon.coupon()
export_step(cp, f"{OUT}/coupon/tolerance_coupon.step")
export_stl(cp, f"{OUT}/coupon/tolerance_coupon.stl", tolerance=0.03, angular_tolerance=0.15)
cb = cp.bounding_box(); print("coupon", cb.size)

# ------------------------------------------------ renders
meshes = [rast.mesh_of(p["shape"]) + (p["color"],) for p in P]
vis = [m for m, p in zip(meshes, P) if p["kind"] != "ref"]
views = [("front", 0, 0), ("rear", 180, 0), ("left", 90, 0), ("right", -90, 0), ("top", 0, 89.9),
         ("bottom", 0, -89.9), ("34_front_right", -35, 22), ("34_rear_left", 145, 22)]
pix = collections.Counter()
for n, az, el in views:
    im = rast.render(vis, az, el, f"{OUT}/renders/{n}.png", title=f"HaebotCase v2 — {n.replace('_', ' ')}")
print("views", round(time.time() - t0))
fr = collections.Counter()
for n, az, el in views[:5]:
    Mv, d = rast.view_matrix(az, el)
    for (V, Tt, c) in vis:
        if len(Tt) == 0: continue
        nrm = np.cross(V[Tt[:, 1]] - V[Tt[:, 0]], V[Tt[:, 2]] - V[Tt[:, 0]])
        area = np.linalg.norm(nrm, axis=1) / 2
        nn = nrm / np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-9)
        fr[c] += float((area * np.clip(nn @ d, 0, None)).sum())
tot = sum(fr.values())
cfr = {k: round(100 * v / tot, 1) for k, v in fr.items()}
print("colour %", cfr)

# exploded render
emeshes = [(V + np.array(o), Tt, c) for (V, Tt, c), (p, o) in zip(meshes, EXP)]
rast.render(emeshes, -35, 22, f"{OUT}/renders/exploded.png", size=(1600, 1400), title="HaebotCase v2 — exploded (2020 frame stays in place)")
# skeleton / frame + seam layout
rast.render([m for m, p in zip(meshes, P) if p["kind"] == "ref" or p["name"].startswith(("plinth", "post", "fender"))],
            -35, 22, f"{OUT}/renders/skeleton_frame_posts.png", title="Master skeleton: 2020 frame + corner posts + plinth")

# ------------------------------------------------ sections (cutaways)
SECT = [
    ("section_joint_key", (140, 182, -152, -95, 275, 352), 180, 0, "Upper/lower rabbet joint + side dovetail key, M3 into insert (cut X=140)"),
    ("section_shoulder_splice", (132, 175, -32, 32, 536, 566), 180, 0, "Green shoulder splice plate: pins + M3 into insert (cut X=132)"),
    ("section_insert_boss", (185, 218, 98.5, 130, 195, 232), -90, 0, "Frame-mount M3 insert boss on post, collar + rib (cut Y=98.5)"),
    ("section_door_latch", (180, 218, 0, 45, 100, 150), -90, 0, "Door latch: flush slot cap, captive M3, insert block on 2020 (cut Y=0)"),
    ("section_door_hook", (180, 218, 50, 80, 255, 322), -90, 0, "Door top hook (6 mm) in slotted block on 2020 mid ring (cut Y=50)"),
    ("section_fender_lug", (40, 51.5, -165, -125, 82, 116), 180, 0, "Fender hidden fixing: lug through plinth, M3 + washer from inside (cut X=51.5)"),
]
for n, (x0, x1, y0, y1, z0, z1), az, el, title in SECT:
    reg = v2.box(x0, x1, y0, y1, z0, z1)
    ms = []
    for p in P:
        b = p["shape"].bounding_box()
        if b.max.X < x0 or b.min.X > x1 or b.max.Y < y0 or b.min.Y > y1 or b.max.Z < z0 or b.min.Z > z1:
            continue
        try:
            c = p["shape"] & reg
            if c.volume > 0.01:
                ms.append(rast.mesh_of(c, 0.05, 0.1) + (p["color"],))
        except Exception:
            pass
    rast.render(ms, az, el, f"{OUT}/renders/{n}.png", size=(1100, 900), title=title)
print("sections", round(time.time() - t0))
# coupon render
cm = rast.mesh_of(cp, 0.05, 0.1)
rast.render([cm + ("#7f8c99",)], -60, 45, f"{OUT}/renders/tolerance_coupon.png", size=(1100, 800), title="Tolerance coupon (0.20 / 0.30 / 0.40 mm rows)")

# ------------------------------------------------ data for docs
json.dump(dict(rows=rows, collisions=0, colour=cfr, ins=dict(v2.INS), n_parts=len([p for p in P if p["kind"] == "print"]),
               frame=collections.Counter(p["name"] for p in P if p["kind"] == "ref"),
               coupon=[cb.size.X, cb.size.Y, cb.size.Z]),
          open(f"{OUT}/docs/_data.json", "w"), indent=1, default=str)
with open(f"{OUT}/docs/parts_table.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
for f in ("v2.py", "rast.py", "coupon.py", "export.py"):
    shutil.copy(f, f"{OUT}/cad/{f}")
print("done", round(time.time() - t0))
