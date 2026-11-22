"""HaebotCase v2 premium (faces swapped) — parametric master (build123d / OpenCascade).

DESIGN frame (all geometry below): FRONT = -Y = short 297 face (doors, smoked brow, camera, tray above),
REAR = +Y, robot RIGHT = -X (long 430 side, vent cassette), robot LEFT = +X (long side, technical skin).
At the end every part is rotated +90 deg about Z into the WORLD frame of the original STEP:
WORLD  FRONT = +X (tray end), RIGHT = -Y, LEFT = +Y, REAR = -X.  Tray + fenders keep their exact original positions.
"""
import collections
from build123d import *

# ---------------------------------------------------------------- parameters
L, W, R = 297.0, 430.0, 35.0      # X = short, Y = long, vertical corner radius
T = 3.0                           # cosmetic skin
TP = 4.0                          # plinth wall
GAP = 2.0                         # exterior shadow gap
CLR = 0.30                        # PETG sliding fit per side
CAP_CLR = 0.35                    # removable cap
PIN_CLR = 0.25                    # alignment pin radial
INS_D, INS_L = 4.0, 6.0           # M3 heat-set insert hole (set to your insert!)
INS4_D, INS4_L = 5.6, 8.0         # M4 heat-set insert hole
M3, M3_HEAD = 3.4, 6.0
BOSS_OD = 9.0
LIP_IN, LIP_OUT, LIP_H = 3.3, 6.0, 10.0
TOPLIP_H = 8.0
RIB_T, RIB_D = 1.8, 10.0

ZB, ZP, ZJ, ZT, ZN, ZS = 50.0, 115.0, 312.0, 515.0, 537.0, 564.0
NY = 66.0                         # top channel half width (132), notches in the long walls, bottom Z 537
PX = 89.5                         # post edge on short faces |x|
PY = 90.0                         # post edge on long faces |y| (wide white pillars)
DX = PX - GAP                     # door / rear edge |x| 87.5  -> 175 wide
VY = PY - GAP                     # cassette / side skin edge |y| 88 -> 176 wide
DLO = (ZP + GAP, ZJ - GAP / 2)    # 117 .. 311
DUP = (ZJ + GAP / 2, 478.0)       # 313 .. 478
BROW = (480.0, ZT)
VREC, BREC = 3.0, 1.5
FX, FY = 115.0, 180.0             # 2020 upright centres
RINGS = [(ZB, ZB + 20), (ZJ - 50, ZJ - 30), (493.0, 513.0)]
FRONT_RAILS = [(120.0, 140.0), (455.0, 475.0)]
SIDE_RAILS = [(120.0, 140.0)]
KEY_Y = 140.0                     # side-key position along the long side
WHITE, CHAR, GREEN, GREY, SMOKE, ALU = "#ECE9E2", "#3A3D42", "#62C224", "#A6A9AD", "#16181B", "#C9CDD2"

# ---------------------------------------------------------------- helpers
def box(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)

def rr(a, z0, z1):
    return Pos(0, 0, z0) * extrude(RectangleRounded(L - 2 * a, W - 2 * a, R - a), z1 - z0)

def ring(a, b, z0, z1):
    return rr(a, z0, z1) - rr(b, z0, z1)

def cyl(p, axis, length, d):
    s = 1 if length > 0 else -1
    c = Cylinder(d / 2, abs(length), align=(Align.CENTER, Align.CENTER, Align.MIN))
    rot = {"x": Rot(0, 90 * s, 0), "y": Rot(-90 * s, 0, 0), "z": Rot(0, 0, 0) if s > 0 else Rot(180, 0, 0)}[axis]
    return Pos(*p) * rot * c

INS = collections.Counter()
def boss(p, axis, length, hole_d=INS_D, hole_l=INS_L, od=BOSS_OD, tag="M3 insert (frame-mount boss)"):
    s = 1 if length > 0 else -1
    b = cyl(p, axis, length, od) + cyl(p, axis, 1.6 * s, od + 3.2)          # boss + base fillet collar
    tip = list(p); i = "xyz".index(axis); tip[i] += length
    cut = cyl(tip, axis, -hole_l * s, hole_d)
    INS[tag] += 1
    lo, hi = sorted((p[i], p[i] + length * 0.8))
    if axis == "z":
        rib = box(p[0] - RIB_T / 2, p[0] + RIB_T / 2, p[1] - od, p[1] + od, lo, hi)
    elif axis == "x":
        rib = box(lo, hi, p[1] - RIB_T / 2, p[1] + RIB_T / 2, p[2] - od, p[2] + od)
    else:
        rib = box(p[0] - RIB_T / 2, p[0] + RIB_T / 2, lo, hi, p[2] - od, p[2] + od)
    return b + rib, cut

_LC = None
def lip_cutter():          # interrupted tongues: 8 mm breaks every 50 mm (warp tolerance + wiring)
    global _LC
    if _LC is None:
        c = None
        for k in range(-2, 3):
            b = box(k * 50 - 4, k * 50 + 4, -300, 300, 0, 700); c = b if c is None else c + b
        for k in range(-4, 5):
            if k: c += box(-300, 300, k * 50 - 4, k * 50 + 4, 0, 700)
        _LC = c
    return _LC

def lip(region, z0, h, exclude=None):
    l = (ring(LIP_IN, LIP_OUT, z0, z0 + h) & region) - lip_cutter()
    return l - exclude if exclude is not None else l

PARTS = []
def add(name, shape, color, orient=None, kind="print", file=None, mat="PETG", note="", world=False):
    PARTS.append(dict(name=name, dshape=None if world else shape, color=color, orient=orient or [], kind=kind,
                      file=file or name, mat=mat, note=note, wshape=shape if world else None))

SXN = [(1, "L"), (-1, "R")]        # design +X = robot left, -X = robot right
SYN = [(-1, "F"), (1, "B")]

def keyzone(sx, sy):
    return box(sx * (L / 2 - T - 48), sx * (L / 2 + 1), sy * (KEY_Y - 9), sy * (KEY_Y + 9), 296, 346)

# ---------------------------------------------------------------- frame (REF)
def frame():
    out = []
    for sx in (1, -1):
        for sy in (1, -1):
            out.append(("upright_463", box(sx * (FX - 10), sx * (FX + 10), sy * (FY - 10), sy * (FY + 10), ZB, 513)))
    for (z0, z1) in RINGS:
        for sy in (1, -1):
            out.append(("rail_210", box(-FX + 10, FX - 10, sy * (FY - 10), sy * (FY + 10), z0, z1)))
        for sx in (1, -1):
            out.append(("rail_340", box(sx * (FX - 10), sx * (FX + 10), -FY + 10, FY - 10, z0, z1)))
    for (z0, z1) in FRONT_RAILS:
        out.append(("rail_210", box(-FX + 10, FX - 10, -FY - 10, -FY + 10, z0, z1)))
    for (z0, z1) in SIDE_RAILS:
        out.append(("rail_340", box(-FX - 10, -FX + 10, -FY + 10, FY - 10, z0, z1)))
    for n, s in out:
        add(f"frame_{n}", s, ALU, kind="ref", mat="2020 aluminium")

# ---------------------------------------------------------------- side locking key (double dovetail, inserted along X)
def key_shape(sx, yc, c=0.0, xin=None, xout=None):
    pts = [(-7 - c, -8 - c), (7 + c, -8 - c), (4 + c, 0), (7 + c, 8 + c), (-7 - c, 8 + c), (-4 - c, 0)]
    k = extrude(Plane.YZ * Polygon(*pts, align=None), xout - xin)
    return Pos(sx * xin if sx > 0 else -xout, yc, ZJ) * k

XIN = L / 2 - T            # 145.5 inner face of long-side skin
KEY_X0 = XIN - 36          # key 36 long

def posts():
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * PX, sx * 400, sy * PY, sy * 400, 0, 700)
            kz = keyzone(sx, sy)
            yc = sy * KEY_Y
            for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
                p = ring(0, T, z0, z1) & reg
                adds, cuts = [], []
                if lvl == "lo":
                    adds += [ring(T - .01, 6, ZJ - 15, ZJ) & reg, lip(reg, ZJ, LIP_H, kz)]
                    blk = box(sx * (KEY_X0 - 6), sx * (XIN + .01), yc - 9, yc + 9, ZJ - 25, ZJ)
                else:
                    adds += [ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg, lip(reg, ZT, TOPLIP_H),
                             ring(T - .01, 6, ZT - 12, ZT) & reg]
                    blk = box(sx * (KEY_X0 - 6), sx * (XIN + .01), yc - 9, yc + 9, ZJ, ZJ + 25)
                adds.append(blk)
                zm = (z0 + z1) / 2
                a, c = boss((sx * (PX + 9), sy * (W / 2 - T), zm), "y", -sy * 17.5); adds.append(a); cuts.append(c)
                a, c = boss((sx * XIN, sy * (PY + 22), zm - 30), "x", -sx * 18); adds.append(a); cuts.append(c)
                for a in adds:
                    p = p + a
                cuts.append(key_shape(sx, yc, CLR, KEY_X0 - CLR, L / 2 + 1))
                cuts.append(box(sx * (XIN - .5), sx * (L / 2 + 1), yc - 9, yc + 9, ZJ - 9, ZJ + 9))   # cap port
                if lvl == "up":
                    cuts.append(cyl((sx * (KEY_X0 - CLR), yc, ZJ + 4), "x", -sx * INS_L, INS_D)); INS["M3 insert (side key)"] += 1
                cuts.append(ring(0, 1.0, ZJ - 1, ZJ + 1))          # joint shadow line
                for c in cuts:
                    p = p - c
                add(f"post_{yn}{xn}_{lvl}", p & reg, WHITE, note="print upright as assembled (lip up)")

def keys():
    for sx, xn in SXN:
        for sy, yn in SYN:
            yc = sy * KEY_Y
            k = key_shape(sx, yc, 0.0, KEY_X0, XIN)
            try:
                k = chamfer(k.edges().filter_by_position(Axis.X, sx * KEY_X0 - .01, sx * KEY_X0 + .01), 0.9)   # lead-in
            except Exception:
                pass
            k -= cyl((sx * XIN, yc, ZJ + 4), "x", -sx * 40, M3)
            k -= cyl((sx * XIN, yc, ZJ + 4), "x", -sx * 3.5, M3_HEAD + 0.4)
            add(f"key_{yn}{xn}", k, CHAR, file="key", note="lay on long side")
            cap = box(sx * XIN, sx * (L / 2), yc - 9 + CAP_CLR, yc + 9 - CAP_CLR, ZJ - 9 + CAP_CLR, ZJ + 9 - CAP_CLR)
            cap -= cyl((sx * XIN, yc, ZJ), "x", sx * 1.2, 6.2)          # 6x1 magnet -> sticks to steel key screw
            add(f"keycap_{yn}{xn}", cap, CHAR, file="cap_key", orient=[("y", 90 * sx)], note="outer face down")

# ---------------------------------------------------------------- removable panels in a local frame (face normal -Y)
def panel_local(u0, u1, z0, z1, D, Drail, hooks_u, latch_u, vents=False, ribs_u=(), hook_rail_top=None,
                tab=None, vcols=()):
    yo, yi = -D, -D + T
    p = box(u0, u1, yo, yi, z0, z1)
    if tab:                                    # channel tab (long side, |u|<65) up to the notch
        p += box(-tab[0], tab[0], yo, yi, z1, tab[1])
    for u in ribs_u:
        p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi + RIB_D, z0 + 30, z1 - (45 if vents else 30))
    if not vents:
        p += box(min(u0, u1) + 6, max(u0, u1) - 6, yi, yi + RIB_D * .8, (z0 + z1) / 2 - RIB_T / 2, (z0 + z1) / 2 + RIB_T / 2)
    lo, hi = min(u0, u1), max(u0, u1)
    for uu in (lo, hi - 2):                    # edge return flanges
        p += box(uu, uu + 2, yi, yi + 6, z0 + 4, z1 - 4)
    blocks = []
    ht = z1
    for hu in hooks_u:                         # top hooks, 6 mm engagement -> tilt-out removal
        p += box(hu - 10, hu + 10, yi, yi + 14.5, ht - 8, ht - 4)
        p += box(hu - 10, hu + 10, yi + 10.5, yi + 14.5, ht - 14, ht - 8)
        hb0 = min(ht - 26, hook_rail_top - 10) if hook_rail_top else ht - 26
        blk = box(hu - 12, hu + 12, yi, -Drail, hb0, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 10, yi + 15, ht - 15, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 8.5, yi + 16.5, ht - 9, ht - 8)     # lead-in
        blk -= cyl((hu, -Drail, hb0 + 5), "y", -12, 5.5); INS["M5 T-nut"] += 1
        blocks.append(("hookblock", blk))
    zl = z0 + 10                               # bottom latch: captive M3 under flush slot cap
    p += box(latch_u - 30, latch_u + 30, yi, yi + 6, z0 + 2, z0 + 18)
    p -= Pos(latch_u, yo, zl) * Rot(90, 0, 0) * extrude(SlotOverall(50, 8), -5.5)
    p -= cyl((latch_u, yo, zl), "y", 12, M3)
    cap = Pos(latch_u, yo, zl) * Rot(90, 0, 0) * extrude(SlotOverall(50 - 2 * CAP_CLR, 8 - 2 * CAP_CLR), -2.5)
    cap -= Pos(latch_u, yo + 2.5, zl) * Rot(90, 0, 0) * extrude(Circle(3.1), 1.2)
    tall = z0 > ZJ - 5
    bz0 = (RINGS[1][1] - 10) if tall else z0
    blk = box(latch_u - 15, latch_u + 15, yi + 6, -Drail, bz0, z0 + 20)
    blk -= cyl((latch_u, yi + 6, zl), "y", INS_L + 1, INS_D); INS["M3 insert (panel latch)"] += 1
    blk -= cyl((latch_u + 9, -Drail, bz0 + 5), "y", -12, 5.5); INS["M5 T-nut"] += 1
    blocks.append(("screwblock_tall" if tall else "screwblock", blk))
    if vents:
        for uc in vcols:
            zc = z0 + 24
            while zc <= z1 - 22:
                p -= Pos(uc, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(60, 5), -T - 1)
                zc += 10
    return p, blocks, cap

def doors():
    for lvl, (z0, z1) in (("lo", DLO), ("up", DUP)):
        p, blocks, cap = panel_local(-DX, DX, z0, z1, W / 2, FY + 10, hooks_u=(-50, 50), latch_u=0,
                                     ribs_u=(-75, -25, 25, 75),
                                     hook_rail_top=RINGS[1][1] if lvl == "lo" else FRONT_RAILS[1][1])
        add(f"door_{lvl}", p, WHITE, orient=[("x", 90)], note="outer face down on textured PEI")
        add(f"doorcap_{lvl}", cap, CHAR, file="cap_slot", orient=[("x", 90)], note="outer face down")
        for i, (n, b) in enumerate(blocks):
            add(f"{n}_door_{lvl}_{i}", b, CHAR, file=f"door_{n}", note="slot up")

def vents():
    rot = Rot(0, 0, -90)           # local front (-Y) -> design -X (robot right)
    for lvl, (z0, z1) in (("lo", DLO), ("up", (ZJ + GAP / 2, ZT - GAP))):
        p, blocks, cap = panel_local(-VY, VY, z0, z1, L / 2 - VREC, FX + 10, hooks_u=(-50, 50), latch_u=0,
                                     vents=True, ribs_u=(0, -80, 80), vcols=(-40, 40),
                                     hook_rail_top=RINGS[1][1] if lvl == "lo" else RINGS[2][1],
                                     tab=(NY - 1, ZN - 2) if lvl == "up" else None)
        add(f"vent_{lvl}", rot * p, CHAR, orient=[("y", -90)], note="outer face down")
        add(f"ventcap_{lvl}", rot * cap, CHAR, file="cap_slot", orient=[("y", -90)], note="outer face down")
        for i, (n, b) in enumerate(blocks):
            add(f"{n}_vent_{lvl}_{i}", rot * b, CHAR, file=f"vent_{n}", note="slot up")

# ---------------------------------------------------------------- fixed skins
def rear():
    reg = box(-DX, DX, 100, 400, 0, 700)
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        p = ring(0, T, z0, z1) & reg
        if lvl == "up":
            p += lip(reg, ZT, TOPLIP_H) + (ring(T - .01, 6, ZT - 12, ZT) & reg)
            p += ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg
        else:
            p += (ring(T - .01, 6, ZJ - 15, ZJ) & reg) + lip(reg, ZJ, LIP_H)
        yi = W / 2 - T
        for u in (-75, -25, 25, 75):
            p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi - RIB_D, z0 + 30, z1 - 30)
        p += box(-81, 81, yi, yi - 8, (z0 + z1) / 2 - .9, (z0 + z1) / 2 + .9)
        for xx in (-50, 50):
            a, c = boss((xx, yi, (z0 + z1) / 2 + 40), "y", -17.5); p = p + a - c
        p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
        add(f"rear_{lvl}", p, WHITE, orient=[("x", -90)], note="outer face down")

def left():
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        reg = box(100, 400, -VY, VY, 0, 700)
        p = ring(0, T, z0, z1) & reg
        if lvl == "lo":
            p += (ring(T - .01, 6, ZJ - 15, ZJ) & reg) + lip(reg, ZJ, LIP_H)
        else:
            p += ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg
            outer = box(100, 400, NY + 1, VY, 0, 700) + box(100, 400, -VY, -NY - 1, 0, 700)
            p += lip(outer, ZT, TOPLIP_H) + (ring(T - .01, 6, ZT - 12, ZT) & outer)
            p += ring(0, T, ZT, ZN) & box(100, 400, -NY + 1, NY - 1, 0, 700)       # channel tab to notch Z537
        xi = L / 2 - T
        for u in (-60, 0, 60):
            p += box(xi, xi - RIB_D, u - RIB_T / 2, u + RIB_T / 2, z0 + 30, z1 - 30)
        zc = (z0 + z1) / 2
        for yy in (-40, 40):        # vertical green light windows
            p -= Pos(L / 2, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(80, 10), T + .1)
        for yy in (-78, 78):
            a, c = boss((xi, yy, zc), "x", -18); p = p + a - c
        p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
        add(f"side_L_{lvl}", p, CHAR, orient=[("y", 90)], note="outer face down")
        for yy in (-40, 40):
            lb = Pos(L / 2, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(80 - 2 * CLR, 10 - 2 * CLR), T)
            lb += Pos(xi, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(90, 16), 2)
            add(f"lightbar_side_{lvl}_{'ab'[yy > 0]}", lb, GREEN, file="lightbar_side", orient=[("y", 90)],
                note="translucent green PETG, outer face down")

# ---------------------------------------------------------------- smoked brow with camera (front, under the shoulder)
def brow():
    reg = box(-DX, DX, -400, -100, 0, 700)
    b = ring(BREC, BREC + T, *BROW) & reg
    zc = (BROW[0] + BROW[1]) / 2
    yo = -W / 2 + BREC
    b -= cyl((0, yo, zc), "y", 1.0, 22)              # lens recess
    b -= cyl((0, yo, zc), "y", T + 1, 14)            # camera aperture
    b += box(-22, 22, yo + T, yo + T + 2, zc - 14, zc + 14) - cyl((0, yo + T, zc), "y", 2, 14)
    for xx in (-60, 60):
        b -= Pos(xx, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(34, 6), -T - 1)
    for xx in (-32, 32):
        a, c = boss((xx, yo + T, zc), "y", 16.5); b = b + a - c
    add("brow", b, SMOKE, orient=[("x", 90)], note="front face down; smoked/black PETG")
    for xx in (-60, 60):
        lb = Pos(xx, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(34 - 2 * CLR, 6 - 2 * CLR), -T)
        lb += Pos(xx, yo + T, zc) * Rot(90, 0, 0) * extrude(SlotOverall(38, 10), -2)
        add(f"lightbar_brow_{'ab'[xx > 0]}", lb, GREEN, file="lightbar_brow", orient=[("x", 90)], note="outer face down")

# ---------------------------------------------------------------- green U shoulder: 4 keyed segments
def shoulder():
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * GAP / 2, sx * 400, sy * NY, sy * 400, 0, 700)
            s = (ring(0, T, ZT, ZS) & reg) + (rr(0, ZS - T, ZS) & reg)
            s += box(sx * GAP / 2, sx * (L / 2 - T + .01), sy * NY, sy * (NY + T), ZN, ZS - T + .01)   # channel wall
            try:
                es = s.edges().filter_by_position(Axis.Z, ZS - .01, ZS + .01)
                es = [e for e in es if abs(e.center().Y) > NY + 2 and abs(e.center().X) > 3]
                s = fillet(es, 6)
            except Exception as ex:
                print("shoulder fillet skipped", ex)
            s += box(sx * GAP / 2, sx * 16, sy * 75, sy * 190, ZS - T - 6, ZS - T + .01)       # splice strip
            for yy in (sy * 95, sy * 170):
                s -= cyl((sx * 8, yy, ZS - T - 6), "z", 2.8, 4 + 2 * PIN_CLR)
            s -= cyl((sx * 8, sy * 132, ZS - T - 6), "z", 5, INS_D); INS["M3 insert (splice)"] += 1
            for (xx, yy) in ((sx * 60, sy * 160), (sx * 30, sy * 100), (sx * 95, sy * 130)):
                a, c = boss((xx, yy, ZS - T), "z", -(ZS - T - 516)); s = s + a - c
            if sy < 0:      # tray M4 bolts pass through the front skirt
                for xx in (65, 85):
                    s -= cyl((sx * xx, -W / 2 - 1, 545), "y", 6, 4.6)
            add(f"shoulder_{yn}{xn}", s, GREEN, orient=[("x", 180)], note="top face down, skirts up")
    for sy, yn in SYN:
        sp = box(-15, 15, sy * 80, sy * 185, ZS - T - 9.5, ZS - T - 6)
        sp += box(-1, 1, sy * 82, sy * 183, ZS - T - 14.5, ZS - T - 9.5)
        for sx in (1, -1):
            for yy in (sy * 95, sy * 170):
                sp += cyl((sx * 8, yy, ZS - T - 6), "z", 2.5, 4.0)
            sp -= cyl((sx * 8, sy * 132, ZS - T - 6), "z", -10, M3)
        add(f"splice_shoulder_{yn}", sp, CHAR, file="splice_shoulder", note="pins up")

# ---------------------------------------------------------------- plinth (4 frame-mounted segments)
# fender screw holes, design frame (x = +-148.5 side, y, z) -> screws now driven from INSIDE the plinth
FENDER_HOLES_D = [(-49.25, 98.3), (-95.95, 104.4), (49.25, 98.3), (95.95, 104.4)]
def plinth():
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * GAP / 2, sx * 400, sy * GAP / 2, sy * 400, 0, 700)
            p = ring(0, TP, ZB, ZP) & reg
            excl = box(-PX + .5, PX - .5, -400, -100, 0, 700) + box(-400, -100, -PY + .5, PY - .5, 0, 700)
            p += lip(reg, ZP, TOPLIP_H, excl)
            try:
                p -= rr(0, ZB, ZB + 3) - Pos(0, 0, ZB) * extrude(RectangleRounded(L - 6, W - 6, R - 3), 3, taper=-44.9)
            except Exception as ex:
                print("chamfer skip", ex)
            xi = sx * (L / 2 - TP)
            for (fy, fz) in FENDER_HOLES_D:
                if fy * sy > 0:     # clearance hole + inner spot-face pad, head stays inside
                    p -= cyl((sx * (L / 2 + 1), fy, fz), "x", -sx * (TP + 2), 9.0 + 2 * CLR)   # lug hole
            a, c = boss((sx * (PX + 9), sy * (W / 2 - TP), 85), "y", -sy * 16.5); p = p + a - c
            a, c = boss((xi, sy * (PY + 22), 85), "x", -sx * 17); p = p + a - c
            add(f"plinth_{yn}{xn}", p & reg, CHAR, note="print upright, chamfered edge on bed")

# ---------------------------------------------------------------- tray mount (load path tray -> mount -> 2020 top ring)
def tray_mount():
    yi = -(W / 2 - T - CLR)
    b = box(-88.5, 88.5, yi, yi + 12, 521, 560)
    for sx in (1, -1):
        b += box(sx * 62, sx * 82, yi, -FY - 10, 516, 521)
        b += box(sx * 62, sx * 82, -FY - 16, -FY - 10, 494, 521)
        b -= cyl((sx * 72, -FY - 10, 503.5), "y", -8, 5.5); INS["M5 T-nut"] += 1
        for xx in (65, 85):
            b -= cyl((sx * xx, yi, 545), "y", INS4_L, INS4_D); INS["M4 insert (tray)"] += 1
    add("tray_mount", b, CHAR, orient=[("x", 90)], note="plate face down")

# ---------------------------------------------------------------- reused originals (WORLD coords) + hidden fender fixing
def reused(step_path):
    a = import_step(step_path)
    S = a.solids()
    add("tray", S[0], GREY, note="original geometry, unchanged", world=True)
    holes = {25: [(49.25, 98.3), (95.95, 104.4)], 26: [(49.25, 98.3), (95.95, 104.4)],
             27: [(-95.95, 104.4), (-49.25, 98.3)], 28: [(-95.95, 104.4), (-49.25, 98.3)]}
    for i, n in zip((25, 26, 27, 28), ("fender_FR", "fender_FL", "fender_RR", "fender_RL")):
        f = S[i]
        sy = 1 if f.bounding_box().center().Y > 0 else -1
        # fill the visible slotted/countersunk screw holes: rebuild the flange from its outer outline
        slab = f & box(-400, 400, sy * 148.5, sy * 152.5, 0, 200)
        fl = [fc for fc in slab.faces() if abs(abs(fc.center().Y) - 148.5) < 0.01 and fc.geom_type == GeomType.PLANE]
        for fc in fl:
            f = f + extrude(Face(fc.outer_wire()), 4.0, dir=(0, sy, 0))
        for (x, z) in holes[i]:
            f = f + cyl((x, sy * 148.5, z), "y", -sy * (TP - 0.2), 9.0)     # hidden lug through plinth wall
            f = f - cyl((x, sy * (148.5 - TP + 0.2), z), "y", sy * 6.0, INS_D)   # M3 insert in lug end
            INS["M3 large washer d12 (fender clamp)"] += 1
            INS["M3 insert (fender)"] += 1
        add(n, f, GREY, note="print as assembled (open bottom edge down), tree supports inside hood only", world=True)

def build(step_path):
    PARTS.clear(); INS.clear()
    frame(); posts(); keys(); doors(); vents(); rear(); left(); brow(); shoulder(); plinth(); tray_mount()
    toW = Rot(0, 0, 90)
    for p in PARTS:
        if p["wshape"] is None:
            p["wshape"] = toW * p["dshape"]
    reused(step_path)
    for p in PARTS:
        p["shape"] = p["wshape"]
        if p["dshape"] is None:      # world-native parts: orientation from world shape
            p["dshape"] = p["wshape"]
    return PARTS
