"""HaebotCase v2 premium — parametric master (build123d / OpenCascade).
Frame: FRONT = -Y (wide 430 face), REAR = +Y, RIGHT = +X (tray side), LEFT = -X, Z up, floor Z=0.
Run:  python3 -I v2.py  -> builds PARTS list (import and use build())
"""
import math
from build123d import *

# ---------------------------------------------------------------- parameters
L, W, R = 430.0, 297.0, 35.0      # outside plan, vertical corner radius
T = 3.0                           # cosmetic skin
TP = 4.0                          # plinth wall (handling)
GAP = 2.0                         # exterior shadow gap (total)
CLR = 0.30                        # PETG sliding fit per side
CAP_CLR = 0.35                    # removable cap
PIN_CLR = 0.25                    # alignment pin radial
EF = 0.4                          # elephant-foot relief on bed-facing mating edges
INS_D, INS_L = 4.0, 6.0           # M3 heat-set insert hole (set to your insert!)
INS4_D, INS4_L = 5.6, 8.0         # M4 heat-set insert hole (fender, tray)
M3, M3_HEAD = 3.4, 6.0
BOSS_OD = 9.0
LIP_IN, LIP_OUT, LIP_H = 3.3, 6.0, 10.0   # rabbet tongue: inset from outside, height (T+CLR .. 6)
TOPLIP_H = 8.0
RIB_T, RIB_D = 1.8, 10.0

ZB, ZP, ZJ, ZT, ZN, ZS = 50.0, 115.0, 312.0, 515.0, 537.0, 564.0   # bottom, plinth top, joint, body top, notch, top
NX = 66.0                         # channel half width (132 notch, preserved)
PX = 156.0                        # post edge on front/rear faces (|x|)
PY = 89.5                         # post edge on side faces (|y|)
DX = PX - GAP                     # door/rear outer edge |x| = 154
VY = PY - GAP                     # cassette / side skin edge |y| = 87.5
DLO = (ZP + GAP, ZJ - GAP / 2)    # lower door z 117..311
DUP = (ZJ + GAP / 2, 478.0)       # upper door z 313..478
BROW = (480.0, ZT)
VREC = 3.0                        # vent cassette recess
BREC = 1.5                        # brow recess
# frame (2020)
FX, FY = 180.0, 115.0             # upright centres
RINGS = [(ZB, ZB + 20), (ZJ - 50, ZJ - 30), (493.0, 513.0)]   # mid ring kept below the side-key zone
FRONT_RAILS = [(120.0, 140.0), (455.0, 475.0)]
SIDE_RAILS = [(120.0, 140.0)]

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
    """cylinder starting at p, running `length` along axis 'x','y','z' (sign = direction)."""
    s = 1 if length > 0 else -1
    c = Cylinder(d / 2, abs(length), align=(Align.CENTER, Align.CENTER, Align.MIN))
    rot = {"x": Rot(0, 90 * s, 0), "y": Rot(-90 * s, 0, 0), "z": Rot(0, 0, 0) if s > 0 else Rot(180, 0, 0)}[axis]
    return Pos(*p) * rot * c

def boss(p, axis, length, hole_d=INS_D, hole_l=INS_L, od=BOSS_OD):
    """insert boss from wall point p, growing `length` along axis; fillet collar + rib. returns (add, cut)."""
    s = 1 if length > 0 else -1
    b = cyl(p, axis, length, od)
    b += cyl(p, axis, 1.6 * s, od + 3.2)                      # base fillet collar (~1.6 mm)
    tip = list(p); i = "xyz".index(axis); tip[i] += length
    cut = cyl(tip, axis, -hole_l * s, hole_d)
    INS['M4 insert' if hole_d > 5 else 'M3 insert (frame-mount boss)'] += 1
    # rib: thin plate through boss axis, tied into the wall
    if axis == "z":
        rib = box(p[0] - RIB_T / 2, p[0] + RIB_T / 2, p[1] - od, p[1] + od, p[2], p[2] + length * 0.75)
    else:
        lo, hi = sorted((p[i], p[i] + length * 0.8))
        q = list(p)
        if axis == "x":
            rib = box(lo, hi, p[1] - RIB_T / 2, p[1] + RIB_T / 2, p[2] - od, p[2] + od)
        else:
            rib = box(p[0] - RIB_T / 2, p[0] + RIB_T / 2, lo, hi, p[2] - od, p[2] + od)
    return b + rib, cut

LIP_CUT = None
def lip_cutter():
    global LIP_CUT
    if LIP_CUT is None:
        c = None
        for k in range(-4, 5):
            b = box(k * 50 - 4, k * 50 + 4, -200, 200, 0, 700)
            c = b if c is None else c + b
        for k in (-2, -1, 1, 2):
            c += box(-300, 300, k * 50 - 4, k * 50 + 4, 0, 700)
        LIP_CUT = c
    return LIP_CUT

def lip(region, z0, h, exclude=None):
    l = (ring(LIP_IN, LIP_OUT, z0, z0 + h) & region) - lip_cutter()
    if exclude is not None:
        l -= exclude
    return l

PARTS = []
import collections
INS = collections.Counter()
def add(name, shape, color, orient=None, kind="print", file=None, mat="PETG", note=""):
    if isinstance(shape, (list, tuple)):
        shape = Compound(children=list(shape))
    PARTS.append(dict(name=name, shape=shape, color=color, orient=orient or [], kind=kind,
                      file=file or name, mat=mat, note=note))

def SX(v):  # signs
    return [(1, "R"), (-1, "L")] if v == "x" else [(-1, "F"), (1, "B")]

KEYZ = lambda sx, sy: box(sx * 166, sx * 214.5, sy * 89, sy * 106.5, 296, 346)

# ---------------------------------------------------------------- frame (REF, aluminium)
def frame():
    out = []
    for sx in (1, -1):
        for sy in (1, -1):
            out.append(("upright", box(sx * (FX - 10), sx * (FX + 10), sy * (FY - 10), sy * (FY + 10), ZB, 513)))
    for i, (z0, z1) in enumerate(RINGS):
        for sy in (1, -1):
            out.append(("rail_x340", box(-FX + 10, FX - 10, sy * (FY - 10), sy * (FY + 10), z0, z1)))
        for sx in (1, -1):
            out.append(("rail_y210", box(sx * (FX - 10), sx * (FX + 10), -FY + 10, FY - 10, z0, z1)))
    for sy in (1, -1):   # centre uprights, split by mid ring
        out.append(("centre_post", box(-10, 10, sy * (FY - 10), sy * (FY + 10), RINGS[0][1], RINGS[1][0])))
        out.append(("centre_post", box(-10, 10, sy * (FY - 10), sy * (FY + 10), RINGS[1][1], RINGS[2][0])))
    for (z0, z1) in FRONT_RAILS:
        for sx in (1, -1):
            out.append(("door_rail160", box(sx * 10, sx * (FX - 10), -FY - 10, -FY + 10, z0, z1)))
    for (z0, z1) in SIDE_RAILS:
        out.append(("rail_y210", box(FX - 10, FX + 10, -FY + 10, FY - 10, z0, z1)))
    for n, s in out:
        add(f"frame_{n}", s, ALU, kind="ref", mat="2020 Al")

# ---------------------------------------------------------------- posts
def posts():
    for sx, xn in SX("x"):
        for sy, yn in SX("y"):
            reg = box(sx * PX, sx * 400, sy * PY, sy * 400, 0, 700)
            kz = KEYZ(sx, sy)
            yc = sy * 97.5
            for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
                p = ring(0, T, z0, z1) & reg
                adds, cuts = [], []
                if lvl == "lo":
                    adds.append(ring(T - 0.01, 6, ZJ - 15, ZJ) & reg)
                    adds.append(lip(reg, ZJ, LIP_H, kz))
                    blk = box(sx * 168, sx * (215 - T + 0.01), sy * 91, sy * 104, ZJ - 25, ZJ)
                else:
                    adds.append(ring(T - 0.01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg)
                    adds.append(lip(reg, ZT, TOPLIP_H))
                    adds.append(ring(T - 0.01, 6, ZT - 12, ZT) & reg)
                    blk = box(sx * 168, sx * (215 - T + 0.01), sy * 91, sy * 104, ZJ, ZJ + 25)
                    # lip relief in upper block (the lower lip passes by -> keep CLR)
                adds.append(blk)
                # frame-mount bosses (front/rear face and side face)
                zm = (z0 + z1) / 2
                a, c = boss((sx * 165, sy * (148.5 - T), zm), "y", -sy * 17.5); adds.append(a); cuts.append(c)
                a, c = boss((sx * (215 - T), sy * 97.0, zm - 30), "x", -sx * 18); adds.append(a); cuts.append(c)
                for a in adds:
                    p = p + a
                # key pocket (double dovetail), port, insert for key screw
                cuts.append(key_shape(sx, yc, clearance=CLR, x0=176 - CLR, x1=216))
                cuts.append(box(sx * 211.5, sx * 216, yc - 9.0, yc + 9.0, ZJ - 9.0, ZJ + 9.0))   # cap port
                if lvl == "up":
                    cuts.append(cyl((sx * (176 - CLR), yc, ZJ + 4), "x", -sx * INS_L, INS_D)); INS['M3 insert (key)'] += 1
                # joint shadow groove
                cuts.append(ring(0, 1.0, ZJ - 1, ZJ + 1))
                for c in cuts:
                    p = p - c
                p = p & reg
                add(f"post_{yn}{xn}_{lvl}", p, WHITE,
                    orient=[] , note="print upright as assembled; lip/flange up")

def key_shape(sx, yc, clearance=0.0, x0=176.0, x1=212.0):
    c = clearance
    pts = [(-7 - c, -8 - c), (7 + c, -8 - c), (4 + c, 0), (7 + c, 8 + c), (-7 - c, 8 + c), (-4 - c, 0)]
    sk = Plane.YZ * Polygon(*pts, align=None)
    k = extrude(sk, x1 - x0)
    k = Pos(sx * x0 if sx > 0 else sx * x1, yc, ZJ) * k
    return k

def keys():
    for sx, xn in SX("x"):
        for sy, yn in SX("y"):
            yc = sy * 97.5
            k = key_shape(sx, yc, 0.0, 176.0, 212.0)
            try:
                k = chamfer(k.edges().filter_by_position(Axis.X, sx * 176 - 0.01, sx * 176 + 0.01) if sx > 0
                            else k.edges().filter_by_position(Axis.X, sx * 176 - 0.01, sx * 176 + 0.01), 0.9)
            except Exception:
                pass
            k -= cyl((sx * 212, yc, ZJ + 4), "x", -sx * 40, M3)
            k -= cyl((sx * 212, yc, ZJ + 4), "x", -sx * 3.5, M3_HEAD + 0.4)
            add(f"key_{yn}{xn}", k, CHAR, file="key", note="lay flat on long side")
            cap = box(sx * 212, sx * 215, yc - 9 + CAP_CLR, yc + 9 - CAP_CLR, ZJ - 9 + CAP_CLR, ZJ + 9 - CAP_CLR)
            cap -= cyl((sx * 212, yc, ZJ), "x", sx * 1.2, 6.2)       # 6x1 magnet pocket (sticks to screw head)
            add(f"keycap_{yn}{xn}", cap, CHAR, file="cap_key", note="outer face down")

# ---------------------------------------------------------------- panels (doors / vent cassettes) built in local frame
def panel_local(u0, u1, z0, z1, D, Drail, hooks_u, latch_u, vents=False, ribs_u=(), hook_rail_top=None):
    """local frame: face normal -Y, outer face at y=-D, panel spans x=u0..u1.  returns (panel, blocks list, cap)"""
    yo, yi = -D, -D + T
    p = box(u0, u1, yo, yi, z0, z1)
    # ribs
    for u in ribs_u:
        p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi + RIB_D, z0 + 30, z1 - (45 if vents else 30))
    if not vents:
        p += box(min(u0, u1) + 6, max(u0, u1) - 6, yi, yi + RIB_D * 0.8, (z0 + z1) / 2 - RIB_T / 2, (z0 + z1) / 2 + RIB_T / 2)
    # perimeter return flange (stiffens edge, hides gap)
    lo, hi = min(u0, u1), max(u0, u1)
    for uu in (lo, hi - 2):
        p += box(uu, uu + 2, yi, yi + 6, z0 + 4, z1 - 4)
    blocks = []
    # hooks at top
    ht = z1
    for hu in hooks_u:
        p += box(hu - 10, hu + 10, yi, yi + 14.5, ht - 8, ht - 4)
        p += box(hu - 10, hu + 10, yi + 10.5, yi + 14.5, ht - 14, ht - 8)   # 6 mm hook engagement -> tilt-out removal
        hb0 = min(ht - 26, hook_rail_top - 10) if hook_rail_top else ht - 26
        blk = box(hu - 12, hu + 12, yi, -Drail, hb0, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 10.5 - 0.5, yi + 14.5 + 0.5, ht - 15, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 10.5 - 1.5, yi + 14.5 + 1.5, ht - 9, ht - 8)   # lead-in
        INS['m5_tnut'] += 1
        blk -= cyl((hu, -Drail, hb0 + 5), "y", -12, 5.5)   # M5 to T-nut
        blocks.append(("hookblock", blk))
    # latch (captive M3 under flush cap) at bottom
    zl = z0 + 10
    p += box(latch_u - 30, latch_u + 30, yi, yi + 6, z0 + 2, z0 + 18)
    pocket = Pos(latch_u, yo, zl) * Rot(90, 0, 0) * extrude(SlotOverall(50, 8), -5.5)
    p -= pocket
    p -= cyl((latch_u, yo, zl), "y", 12, M3)
    cap = Pos(latch_u, yo, zl) * Rot(90, 0, 0) * extrude(SlotOverall(50 - 2 * CAP_CLR, 8 - 2 * CAP_CLR), -2.5)
    cap -= Pos(latch_u, yo + 2.5, zl) * Rot(90, 0, 0) * extrude(Circle(3.1), 1.2)
    tall = z0 > ZJ - 5
    bz0 = (RINGS[1][1] - 10) if tall else (z0)
    blk = box(latch_u - 15, latch_u + 15, yi + 6, -Drail, bz0, z0 + 20)
    blk -= cyl((latch_u, yi + 6, zl), "y", INS_L + 1, INS_D)
    INS['M3 insert (panel latch)'] += 1; INS['m5_tnut'] += 1
    blk -= cyl((latch_u + 9, -Drail, bz0 + 5), "y", -12, 5.5)
    blocks.append(("screwblock_tall" if tall else "screwblock", blk))
    if vents:
        rows = int((z1 - z0 - 44) // 10) + 1
        for uc in (-42, 42):
            for r_ in range(rows):
                zc = z0 + 24 + r_ * 10
                if zc > z1 - 22: break
                p -= Pos(uc, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(70, 5), -T - 1)
    return p, blocks, cap

def doors():
    for sx, xn in SX("x"):
        for lvl, (z0, z1) in (("lo", DLO), ("up", DUP)):
            u0, u1 = sx * GAP / 2, sx * DX
            p, blocks, cap = panel_local(u0, u1, z0, z1, W / 2, FY + 10, hooks_u=(sx * 35, sx * 120),
                                         latch_u=sx * 77.5, ribs_u=(sx * 52, sx * 103),
                                         hook_rail_top=RINGS[1][1] if lvl == "lo" else FRONT_RAILS[1][1])
            add(f"door_{xn}_{lvl}", p, WHITE, orient=[("x", 90)], note="outer face down on textured PEI")
            add(f"doorcap_{xn}_{lvl}", cap, CHAR, file="cap_slot", orient=[("x", 90)])
            for n, b in blocks:
                add(f"{n}_door_{xn}_{lvl}_{len(PARTS)}", b, CHAR, file=f"door_{n}")

def vents():
    rot = Rot(0, 0, 90)
    for lvl, (z0, z1) in (("lo", DLO), ("up", (ZJ + GAP / 2, ZT - GAP))):
        p, blocks, cap = panel_local(-VY, VY, z0, z1, L / 2 - VREC, FX + 10, hooks_u=(-40, 40), latch_u=0,
                                     vents=True, ribs_u=(0, -82, 82),
                                     hook_rail_top=RINGS[1][1] if lvl == "lo" else RINGS[2][1])
        add(f"vent_{lvl}", rot * p, CHAR, orient=[("y", 90)], note="outer face down")
        add(f"ventcap_{lvl}", rot * cap, CHAR, file="cap_slot", orient=[("y", 90)])
        for n, b in blocks:
            add(f"{n}_vent_{lvl}_{len(PARTS)}", rot * b, CHAR, file=f"vent_{n}")

# ---------------------------------------------------------------- fixed skins: rear, left
def rear():
    for sx, xn in SX("x"):
        reg = box(sx * GAP / 2, sx * DX, 100, 400, 0, 700)
        for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
            p = ring(0, T, z0, z1) & reg
            if lvl == "up":
                p += ring(0, T, ZT, ZN) & box(sx * GAP / 2, sx * (NX - 1), 100, 400, 0, 700)
                p += lip(box(sx * (NX + 1), sx * DX, 100, 400, 0, 700), ZT, TOPLIP_H)
                p += ring(T - .01, 6, ZT - 12, ZT) & box(sx * (NX + 1), sx * DX, 100, 400, 0, 700)
                p += ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg
            else:
                p += ring(T - .01, 6, ZJ - 15, ZJ) & reg
                p += lip(reg, ZJ, LIP_H)
            yi = W / 2 - T
            for u in (sx * 55, sx * 105):
                p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi - RIB_D, z0 + 30, z1 - 30)
            p += box(sx * 21, sx * 150, yi, yi - 8, (z0 + z1) / 2 - .9, (z0 + z1) / 2 + .9)
            # splice band along centre reveal
            p += box(sx * GAP / 2, sx * 20, yi, yi - 3, z0 + 10, z1 - 10)
            zs = [z0 + (z1 - z0) / 3, z0 + 2 * (z1 - z0) / 3]
            for zz in zs:
                p -= cyl((sx * 10, yi - 3, zz), "y", 2.8, 4 + 2 * PIN_CLR)
            p -= cyl((sx * 10, yi - 3, (z0 + z1) / 2), "y", 4.5, INS_D); INS['M3 insert (splice)'] += 1
            a, c = boss((sx * 145, yi, (z0 + z1) / 2), "y", -17.5)
            p = p + a - c
            p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
            add(f"rear_{xn}_{lvl}", p, WHITE, orient=[("x", -90)], note="outer face down")
    # splice plates
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        yi = W / 2 - T - 3
        sp = box(-18, 18, yi, yi - 3.5, z0 + 15, z1 - 15)
        sp += box(-1, 1, yi - 3.5, yi - 7.5, z0 + 20, z1 - 20)
        for sx in (1, -1):
            for zz in (z0 + (z1 - z0) / 3, z0 + 2 * (z1 - z0) / 3):
                sp += cyl((sx * 10, yi, zz), "y", 2.5, 4.0)
            sp -= cyl((sx * 10, yi - 3.5, (z0 + z1) / 2), "y", 3.5, M3)
        add(f"splice_rear_{lvl}", sp, CHAR, file=f"splice_rear_{lvl}", orient=[("x", 90)], note="pins up")

def left():
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        reg = box(-400, -100, -VY, VY, 0, 700)
        p = ring(0, T, z0, z1) & reg
        if lvl == "lo":
            p += ring(T - .01, 6, ZJ - 15, ZJ) & reg; p += lip(reg, ZJ, LIP_H)
        else:
            p += ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg; p += lip(reg, ZT, TOPLIP_H)
            p += ring(T - .01, 6, ZT - 12, ZT) & reg
        xi = -L / 2 + T
        for u in (-55, 55):
            p += box(xi, xi + RIB_D, u - RIB_T / 2, u + RIB_T / 2, z0 + 30, z1 - 30)
        zc = (z0 + z1) / 2
        slot = Pos(-L / 2, 0, zc) * Rot(0, 90, 0) * extrude(SlotOverall(80, 10).rotate(Axis.Z, 90), T + 0.1)
        p -= slot
        for yy in (-72, 72):
            a, c = boss((xi, yy, zc), "x", 18); p = p + a - c
        p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
        add(f"side_L_{lvl}", p, CHAR, orient=[("y", -90)], note="outer face down")
        lb = Pos(-L / 2, 0, zc) * Rot(0, 90, 0) * extrude(SlotOverall(80 - 2 * CLR, 10 - 2 * CLR).rotate(Axis.Z, 90), T)
        lb += Pos(xi, 0, zc) * Rot(0, 90, 0) * extrude(SlotOverall(90, 16).rotate(Axis.Z, 90), 2)
        add(f"lightbar_side_{lvl}", lb, GREEN, file="lightbar_side", orient=[("y", -90)], note="translucent green PETG")

# ---------------------------------------------------------------- brow + camera pod
def brow():
    for sx, xn in SX("x"):
        reg = box(sx * (NX + 1), sx * DX, -400, -100, 0, 700)
        b = ring(BREC, BREC + T, *BROW) & reg
        b += lip(reg, ZT, TOPLIP_H)
        zc = (BROW[0] + BROW[1]) / 2
        yo = -W / 2 + BREC
        s = Pos(sx * 112, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(50, 6), -T - 1)
        b -= s
        for xx in (sx * 78, sx * 146):
            a, c = boss((xx, yo + T, zc), "y", 16.5); b = b + a - c
        add(f"brow_{xn}", b, SMOKE, orient=[("x", 90)], note="front face down; smoked/black PETG")
        lb = Pos(sx * 112, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(50 - 2 * CLR, 6 - 2 * CLR), -T)
        lb += Pos(sx * 112, yo + T, zc) * Rot(90, 0, 0) * extrude(SlotOverall(54, 10), -2)
        add(f"lightbar_brow_{xn}", lb, GREEN, file="lightbar_brow", orient=[("x", 90)])
    reg = box(-(NX - 1), NX - 1, -400, -100, 0, 700)
    pod = ring(BREC, BREC + T, BROW[0], ZN) & reg
    yo = -W / 2 + BREC
    zc = 505
    pod -= cyl((0, yo, zc), "y", 1.0, 22)
    pod -= cyl((0, yo, zc), "y", T + 1, 14)
    pod += box(-30, 30, yo + T, yo + T + 2, zc - 14, zc + 14) - cyl((0, yo + T, zc), "y", 2, 14)
    for xx in (-42, 42):
        a, c = boss((xx, yo + T, 497), "y", 16.5); pod = pod + a - c
    add("camera_pod", pod, SMOKE, orient=[("x", 90)], note="front face down")

# ---------------------------------------------------------------- green shoulder
def shoulder():
    for sx, xn in SX("x"):
        for sy, yn in SX("y"):
            reg = box(sx * NX, sx * 400, sy * GAP / 2, sy * 400, 0, 700)
            s = (ring(0, T, ZT, ZS) & reg) + (rr(0, ZS - T, ZS) & reg)
            s += box(sx * NX, sx * (NX + T), sy * GAP / 2, sy * (W / 2 - T + .01), ZN, ZS - T + .01)
            try:
                es = s.edges().filter_by_position(Axis.Z, ZS - .01, ZS + .01)
                es = [e for e in es if abs(e.center().X) > NX + 2 and abs(e.center().Y) > 3]
                s = fillet(es, 6)
            except Exception as ex:
                print("shoulder fillet skipped", ex)
            # seam strip (splice)
            s += box(sx * 75, sx * 190, sy * GAP / 2, sy * 16, ZS - T - 6, ZS - T + .01)
            for xx in (sx * 95, sx * 170):
                s -= cyl((xx, sy * 8, ZS - T - 6), "z", 2.8, 4 + 2 * PIN_CLR)
            s -= cyl((sx * 132, sy * 8, ZS - T - 6), "z", 5, INS_D); INS['M3 insert (splice)'] += 1
            for (xx, yy) in ((sx * 140, sy * 90), (sx * 100, sy * 40), (sx * 160, sy * 60)):
                a, c = boss((xx, yy, ZS - T), "z", -(ZS - T - 516)); s = s + a - c
            if sx > 0:   # tray bolts pass through right skirt
                for yy in (65, 85):
                    s -= cyl((L / 2 + 1, sy * yy, 545), "x", -6, 4.6)
            add(f"shoulder_{yn}{xn}", s, GREEN, orient=[("x", 180)], note="top face down, skirts up")
    for sx, xn in SX("x"):
        sp = box(sx * 80, sx * 185, -15, 15, ZS - T - 6 - 3.5, ZS - T - 6)
        sp += box(sx * 82, sx * 183, -1, 1, ZS - T - 6 - 3.5 - 5, ZS - T - 6 - 3.5)
        for sy in (1, -1):
            for xx in (sx * 95, sx * 170):
                sp += cyl((xx, sy * 8, ZS - T - 6), "z", 2.5, 4.0)
            sp -= cyl((sx * 132, sy * 8, ZS - T - 6), "z", -10, M3)
        add(f"splice_shoulder_{xn}", sp, CHAR, file="splice_shoulder", note="pins up")

# ---------------------------------------------------------------- plinth
FENDER_HOLES = [(51.5, 98.3), (98.2, 104.4), (-47.0, 98.3), (-93.7, 104.4)]
def plinth():
    for sx, xn in SX("x"):
        for sy, yn in SX("y"):
            reg = box(sx * GAP / 2, sx * 400, sy * GAP / 2, sy * 400, 0, 700)
            p = ring(0, TP, ZB, ZP) & reg
            # lip only under fixed skins (not under doors / vent cassette)
            excl = box(-PX + .5, PX - .5, -400, -100, 0, 700) + box(100, 400, -PY + .5, PY - .5, 0, 700)
            p += lip(reg, ZP, TOPLIP_H, excl)
            # bottom handling chamfer (3 mm)
            try:
                ch = rr(0, ZB, ZB + 3) - Pos(0, 0, ZB) * extrude(RectangleRounded(L - 6, W - 6, R - 3), 3, taper=-44.9)
                p -= ch
            except Exception as ex:
                print("chamfer skip", ex)
            yi = sy * (W / 2 - TP)
            for (fx, fz) in FENDER_HOLES:
                if fx * sx > 0:
                    a, c = boss((fx, yi, fz), "y", -sy * 12, INS4_D, INS4_L, od=11); p = p + a - c
            a, c = boss((sx * 165, yi, 85), "y", -sy * 16.5); p = p + a - c
            a, c = boss((sx * (L / 2 - TP), sy * 97, 85), "x", -sx * 17); p = p + a - c
            p = p & reg
            add(f"plinth_{yn}{xn}", p, CHAR, note="print upright, chamfered edge on bed")

# ---------------------------------------------------------------- tray mount
def tray_mount():
    xi = L / 2 - T - CLR
    b = box(xi - 12, xi, -88.5, 88.5, 520, 560)
    for sy in (1, -1):
        b += box(FX + 10, xi, sy * 62, sy * 82, 514, 520)
        b += box(FX + 10, FX + 16, sy * 62, sy * 82, 494, 520)
        b -= cyl((FX + 10, sy * 72, 503.5), "x", 8, 5.5); INS['m5_tnut'] += 1
        for yy in (65, 85):
            b -= cyl((xi, sy * yy, 545), "x", -INS4_L, INS4_D); INS['M4 insert'] += 1
    add("tray_mount", b, CHAR, orient=[("y", 90)], note="load path: tray -> M4 -> mount -> 2020 top ring")

# ---------------------------------------------------------------- reused original parts
def reused(step_path):
    a = import_step(step_path)
    S = a.solids()
    add("tray", S[0], GREY, note="original geometry, unchanged")
    for i, n in zip((25, 26, 27, 28), ("fender_FR", "fender_BR", "fender_FL", "fender_BL")):
        add(n, S[i], GREY, note="original geometry, unchanged")

def build(step_path):
    PARTS.clear(); INS.clear()
    frame(); posts(); keys(); doors(); vents(); rear(); left(); brow(); shoulder(); plinth(); tray_mount()
    reused(step_path)
    return PARTS
