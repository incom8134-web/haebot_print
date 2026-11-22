"""HaebotCase v5 (audited zip-tie edition) — parametric master (build123d / OpenCascade).

The shell hangs on the user's 3-tier mesh cart (no aluminium frame, no screws in the body).
Fixing = hidden zip-tie loops on every fixed part (or hot glue). Doors/vent cassettes = hooks printed into the
corner posts + magnets at the bottom (tool-free). Upper/lower halves align on interrupted tongues.

DESIGN frame: FRONT = -Y (short face: door, smoked brow, tray above), REAR = +Y, robot RIGHT = -X (long side,
vent cassette), robot LEFT = +X (long side, charcoal skin + light windows).  Parts are rotated +90 deg about Z into
WORLD (= original v1 STEP axes): FRONT = +X, RIGHT = -Y, LEFT = +Y.
"""
import collections
from build123d import *

# ---------------------------------------------------------------- cart (user measurements) + wiggle room
CART_L, CART_B, CART_H = 385.0, 245.0, 540.0     # length (along Y), breadth (along X), height
CART_BASE_B = 295.0                              # bottom U-tubes stick out 25 mm each side
CART_Z0 = 60.0                                   # ASSUMED: cart bottom tube at wheel-axle height
WHEEL_D, WHEEL_W = 120.0, 50.0                   # mecanum wheel diameter (given), width (ASSUMED ~50)
WHEEL_Y = 110.0                                  # ASSUMED: wheel centres at +-110 along the long side
AXLE_Z = WHEEL_D / 2
WHEEL_HOLE_R = 56.0                              # plinth opening radius behind each wheel (wheel r = 60)

# ---------------------------------------------------------------- shell parameters
L, W, R = 315.0, 435.0, 35.0      # X = short (breadth side), Y = long; corner radius
T, TP = 3.0, 4.0                  # skin, plinth wall
GAP, CLR, PIN_CLR = 2.0, 0.30, 0.25
LIP_IN, LIP_OUT, LIP_H, TOPLIP_H = 3.3, 6.0, 10.0, 8.0
RIB_T, RIB_D = 1.8, 10.0
MAG_D, MAG_H = 10.2, 3.2          # 10 x 3 mm disc magnets (door/vent bottom)
INS4_D, INS4_L = 5.6, 8.0         # tray M4 inserts (only screws left: inside the tray)
TIE_W, TIE_T = 6.5, 3.0           # tunnel for 4.8 x 1.2 mm zip ties (fits up to 5 mm ties)
LOOP_D = 13.0                     # standoff depth of a wall tie loop (two crossing tunnels: along the wall + vertical)
TRAY_HX = (67.6, 82.4)            # MEASURED from the v1 tray STEP: M4 holes at +-67.6 and +-82.4 mm, z=590, dia 4.5
CART_TOP = CART_Z0 + CART_H
TOP_CLR = 7.0                     # clearance between cart top and anything of the green shoulder

ZB, ZP, ZJ, ZT, ZN, ZS = 40.0, 150.0, 355.0, 560.0, 588.0, 615.0
NY = 66.0                         # top channel half width (132 mm, as v1)
PX, PY = 89.5, 90.0               # post edge on short / long faces
DX, VY = PX - GAP, PY - GAP       # door edge 87.5 (175 wide), cassette edge 88 (176 wide)
DLO = (ZP + GAP, ZJ - 1.0)        # 152..354
DUP = (ZJ + 1.0, 519.0)           # 356..519 (>=10 mm below the brow so the hooks can lift 6 mm)
BROW = (529.0, ZT)
VREC, BREC = 3.0, 1.5
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

def wall_box(face, a0, a1, n0, n1, z0, z1):
    """box on a wall: face 'y' -> along=x, normal=y ; face 'x' -> along=y, normal=x"""
    return box(a0, a1, n0, n1, z0, z1) if face == "y" else box(n0, n1, a0, a1, z0, z1)

def wedge(face, a0, a1, wn, d, ztop):
    """45 deg gusset under a standoff (print-friendly): wall at normal coord wn, depth d (signed)."""
    a0, a1 = sorted((a0, a1))
    pts = [(wn, ztop), (wn + d, ztop), (wn, ztop - abs(d))]
    if face == "y":
        w = extrude(Plane.YZ * Polygon(*pts, align=None), a1 - a0)
        return w.translate((a0 - w.bounding_box().min.X, 0, 0))
    w = extrude(Plane.XZ * Polygon(*pts, align=None), a1 - a0)
    return w.translate((0, a0 - w.bounding_box().min.Y, 0))

def tie_loop(face, ac, zc, wn, s, n=1, gusset=True):
    """hidden zip-tie loop on an inner wall face (wn = inner face coord, s = inward sign).
    Two crossing tunnels at different depths: A runs ALONG the wall (tie wraps a vertical tube or goes through a mesh
    square), B runs UP/DOWN (tie wraps a horizontal rim wire). The user picks whichever suits the cart wire."""
    D = LOOP_D
    blk = wall_box(face, ac - 8, ac + 8, wn - s * 0.5, wn + s * D, zc - 7, zc + 7)
    if gusset:
        blk += wedge(face, ac - 8, ac + 8, wn, s * D, zc - 7)
    blk -= wall_box(face, ac - 9, ac + 9, wn + s * 2.5, wn + s * (2.5 + TIE_T), zc - TIE_W / 2, zc + TIE_W / 2)      # A
    blk -= wall_box(face, ac - TIE_W / 2, ac + TIE_W / 2, wn + s * 7.5, wn + s * (7.5 + TIE_T), zc - 7 - D - 1, zc + 8)  # B
    INS["zip tie (4.8 mm, 200 mm)"] += n
    return blk

def lip_cutter():
    c = None
    for k in range(-3, 4):
        b = box(k * 50 - 4, k * 50 + 4, -300, 300, 0, 800); c = b if c is None else c + b
    for k in range(-4, 5):
        if k: c += box(-300, 300, k * 50 - 4, k * 50 + 4, 0, 800)
    return c
_LC = None
def lip(region, z0, h, exclude=None):
    global _LC
    _LC = _LC or lip_cutter()
    l = (ring(LIP_IN, LIP_OUT, z0, z0 + h) & region) - _LC
    return l - exclude if exclude is not None else l

PARTS = []
def add(name, shape, color, orient=None, kind="print", file=None, note="", world=False):
    PARTS.append(dict(name=name, dshape=None if world else shape, color=color, orient=orient or [], kind=kind,
                      file=file or name, note=note, wshape=shape if world else None, mat="PETG"))

SXN = [(1, "L"), (-1, "R")]
SYN = [(-1, "F"), (1, "B")]
POST_ADD = collections.defaultdict(list)          # (sx, sy, lvl) -> solids merged into that post

# ---------------------------------------------------------------- reference bodies (cart envelope, wheels)
def refs():
    add("ref_cart", box(-CART_B / 2, CART_B / 2, -CART_L / 2, CART_L / 2, CART_Z0, CART_Z0 + CART_H), ALU, kind="ref")
    add("ref_cart_base", box(-CART_BASE_B / 2, CART_BASE_B / 2, -CART_L / 2, CART_L / 2, CART_Z0, CART_Z0 + 25), ALU, kind="ref")
    for sx in (1, -1):
        for sy in (1, -1):
            add("ref_wheel", cyl((sx * (L / 2 + 2), sy * WHEEL_Y, AXLE_Z), "x", sx * WHEEL_W, WHEEL_D), "#555555", kind="ref")

# ---------------------------------------------------------------- removable panel + post-mounted hook/magnet blocks
def panel_local(u0, u1, z0, z1, D, rec, vents=False, ribs_u=(), screws=True):
    """local frame: face normal -Y, panel outer face at y=-D; the posts' inner face is at y=-D-rec+T.
    returns panel, list of (sign_u, block) to merge into the neighbouring post, cap list"""
    yo, yi = -D, -D + T
    ypost = yi - rec                               # post inner face (cassette is recessed by rec)
    p = box(u0, u1, yo, yi, z0, z1)
    for u in ribs_u:
        p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi + RIB_D, z0 + 30, z1 - 42)
    if not vents:
        p += box(u0 + 20, u1 - 20, yi, yi + 8, (z0 + z1) / 2 - .9, (z0 + z1) / 2 + .9)
    for uu in (u0, u1 - 2):                         # edge return flanges (stop below the hook blocks)
        p += box(uu, uu + 2, yi, yi + 6, z0 + 40, z1 - 44)
    blocks = []
    ht, zb = z1, z0
    for sgn in (1, -1):
        e = sgn * u1 if sgn > 0 else u0             # edge coordinate
        hu = sgn * (abs(e) - 10)
        # --- hook on panel (6 mm engagement, tilt-out removal)
        p += box(hu - 10, hu + 10, yi, yi + 10, ht - 8, ht - 4)
        p += box(hu - 10, hu + 10, yi + 6, yi + 10, ht - 14, ht - 8)
        # --- hook block printed into the post
        a_in, a_post = sgn * (abs(e) - 22), sgn * (abs(e) + GAP + 15)
        blk = box(a_in, sgn * (abs(e) + GAP), yi, yi + 14, ht - 26, ht - 8)
        blk += box(sgn * (abs(e) + GAP - 0.5), a_post, ypost - 1, yi + 14, ht - 26, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 5.5, yi + 10.5, ht - 15, ht - 8)
        blk -= box(hu - 10.5, hu + 10.5, yi + 4, yi + 12, ht - 9, ht - 8)          # lead-in
        blk += wedge("y", a_in, a_post, yi, 14, ht - 26)
        blk += wedge("y", sgn * (abs(e) + GAP - 0.5), a_post, ypost, 14 + rec, ht - 26)
        mu = sgn * (abs(e) - 7); mz = zb + 38
        p += box(sgn * (abs(e) - 14), sgn * (abs(e) - 1), yi, yi + 6, zb + 28, zb + 48)          # boss on the panel
        pad = box(sgn * (abs(e) - 14), sgn * (abs(e) + GAP), yi + 6.5, yi + 14.5, zb + 28, zb + 48)
        pad += box(sgn * (abs(e) + GAP - 0.5), sgn * (abs(e) + GAP + 10), ypost - 1, yi + 14.5, zb + 28, zb + 48)
        if screws:
            # M4 x 12 button head from the outside (head sunk in a counterbore) into an M4 nut trap in the post pad
            p -= cyl((mu, yo - 1, mz), "y", (yi + 6.5) - (yo - 1), 4.5)                          # clearance hole
            p -= cyl((mu, yo - 1, mz), "y", 3.6, 8.2)                                            # head counterbore 2.6 deep
            pad -= Pos(mu, yi + 6.5 - 0.01, mz) * Rot(-90, 0, 0) * Rot(0, 0, 30) * extrude(RegularPolygon(4.27, 6), 3.5)   # nut trap
            pad -= cyl((mu, yi + 6.0, mz), "y", 9.0, 4.5)
            INS["M4 x 12 button-head screw (panel)"] += 1; INS["M4 nut (panel)"] += 1
        else:
            # front doors: NO holes in the visible face. Hidden magnet pair (10 x 3 mm) at the bottom corners
            p -= cyl((mu, yi + 6, mz), "y", -MAG_H, MAG_D)
            pad -= cyl((mu, yi + 6.5, mz), "y", MAG_H, MAG_D)
            INS["magnet 10x3 mm"] += 2
        pad += wedge("y", sgn * (abs(e) - 14), sgn * (abs(e) + GAP + 10), yi + 6.5, 8, zb + 28)
        pad += wedge("y", sgn * (abs(e) + GAP - 0.5), sgn * (abs(e) + GAP + 10), ypost, 14.5 + rec, zb + 28)
        blocks.append((sgn, blk + pad))
    if vents:
        for uc in (-40, 40):
            zc = z0 + 24
            while zc <= z1 - 22:
                p -= Pos(uc, yo, zc) * Rot(90, 0, 0) * extrude(SlotOverall(60, 5), -T - 1)
                zc += 10
    return p, blocks

def doors():
    for lvl, (z0, z1) in (("lo", DLO), ("up", DUP)):
        p, blocks = panel_local(-DX, DX, z0, z1, W / 2, 0.0, ribs_u=(-55, -25, 25, 55), screws=False)
        add(f"door_{lvl}", p, WHITE, orient=[("x", 90)], note="outer face down on textured PEI")
        for sgn, b in blocks:
            POST_ADD[(sgn, -1, lvl)].append(b)              # front posts, side = sign(u) = sign(x)

def vents():
    rot = Rot(0, 0, -90)                                   # local -Y face -> design -X (robot right)
    for lvl, (z0, z1) in (("lo", DLO), ("up", (ZJ + 1, ZT - GAP))):
        p, blocks = panel_local(-VY, VY, z0, z1, L / 2 - VREC, VREC, vents=True, ribs_u=(0, -78 + 8, 78 - 8))
        add(f"vent_{lvl}", rot * p, CHAR, orient=[("y", -90)], note="outer face down")
        for sgn, b in blocks:                              # local u>0 -> design y<0
            POST_ADD[(-1, -sgn, lvl)].append(rot * b)

# ---------------------------------------------------------------- corner posts (white)
def posts():
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * PX, sx * 400, sy * PY, sy * 400, 0, 800)
            for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
                p = ring(0, T, z0, z1) & reg
                if lvl == "lo":
                    p += (ring(T - .01, 6, ZJ - 15, ZJ) & reg) + lip(reg, ZJ, LIP_H)
                else:
                    p += (ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg) + lip(reg, ZT, TOPLIP_H)
                    p += ring(T - .01, 6, ZT - 12, ZT) & reg
                zm = (z0 + z1) / 2
                p += tie_loop("y", sx * 113, zm, sy * (W / 2 - T), -sy)          # short-face strip
                p += tie_loop("x", sy * 150, zm, sx * (L / 2 - T), -sx)          # long-face strip
                for b in POST_ADD[(sx, sy, lvl)]:
                    p += b
                p -= ring(0, 1.0, ZJ - 1, ZJ + 1)                                # joint shadow line
                add(f"post_{yn}{xn}_{lvl}", p, WHITE, note="print upright as assembled; gussets under blocks, no supports")

# ---------------------------------------------------------------- fixed skins
def rear():
    reg = box(-DX, DX, 100, 400, 0, 800)
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        p = ring(0, T, z0, z1) & reg
        if lvl == "up":
            p += lip(reg, ZT, TOPLIP_H) + (ring(T - .01, 6, ZT - 12, ZT) & reg) + (ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg)
        else:
            p += (ring(T - .01, 6, ZJ - 15, ZJ) & reg) + lip(reg, ZJ, LIP_H)
        yi = W / 2 - T
        for u in (-75, -25, 25, 75):
            p += box(u - RIB_T / 2, u + RIB_T / 2, yi, yi - RIB_D, z0 + 30, z1 - 30)
        p += box(-81, 81, yi, yi - 8, (z0 + z1) / 2 - .9, (z0 + z1) / 2 + .9)
        for xx in (-50, 0, 50):
            p += tie_loop("y", xx, (z0 + z1) / 2 + 30, yi, -1, gusset=False)
        p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
        add(f"rear_{lvl}", p, WHITE, orient=[("x", -90)], note="outer face down")

def left():
    for lvl, (z0, z1) in (("lo", (ZP, ZJ)), ("up", (ZJ, ZT))):
        reg = box(100, 400, -VY, VY, 0, 800)
        p = ring(0, T, z0, z1) & reg
        if lvl == "lo":
            p += (ring(T - .01, 6, ZJ - 15, ZJ) & reg) + lip(reg, ZJ, LIP_H)
        else:
            p += ring(T - .01, 6, ZJ + LIP_H + CLR, ZJ + 25) & reg
            outer = box(100, 400, NY + 1, VY, 0, 800) + box(100, 400, -VY, -NY - 1, 0, 800)
            p += lip(outer, ZT, TOPLIP_H) + (ring(T - .01, 6, ZT - 12, ZT) & outer)
        xi = L / 2 - T
        for u in (-60, 0, 60):
            p += box(xi, xi - RIB_D, u - RIB_T / 2, u + RIB_T / 2, z0 + 30, z1 - 30)
        zc = (z0 + z1) / 2
        for yy in (-40, 40):
            p -= Pos(L / 2, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(80, 10), T + .1)
        for yy in (-70, 70):
            p += tie_loop("x", yy, zc + 60, xi, -1, gusset=False)
        p -= ring(0, 1.0, ZJ - 1, ZJ + 1)
        add(f"side_L_{lvl}", p, WHITE, orient=[("y", 90)], note="outer face down")
        for yy in (-40, 40):
            lb = Pos(L / 2, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(80 - 2 * CLR, 10 - 2 * CLR), T)
            lb += Pos(xi, yy, zc) * Rot(0, -90, 0) * extrude(SlotOverall(90, 16), 2)
            add(f"lightbar_side_{lvl}_{'ab'[yy > 0]}", lb, GREEN, file="lightbar_side", orient=[("y", 90)],
                note="push in from inside, dot of hot glue on flange")

def channel_caps():
    for sx, xn in SXN:
        c = ring(0, T, ZT, ZN) & box(sx * 100, sx * 400, -NY + 1, NY - 1, 0, 800)
        c += tie_loop("x", 0, (ZT + ZN) / 2, sx * (L / 2 - T), -sx, gusset=False)
        # ledge closing the 22-32 mm gap between shell and cart, so nobody can look down into the shell
        c += box(sx * (L / 2 - T + .01), sx * (CART_B / 2 + 6), -(NY - 1), NY - 1, ZN - 3, ZN)
        add(f"channel_cap_{xn}", c, CHAR, orient=[("y", 90 * sx)], note="outer face down")

# ---------------------------------------------------------------- brow
def brow():
    reg = box(-DX, DX, -400, -100, 0, 800)
    b = ring(BREC, BREC + T, *BROW) & reg
    b += lip(reg, ZT, TOPLIP_H)
    zc = (BROW[0] + BROW[1]) / 2
    yo = -W / 2 + BREC
    b -= cyl((0, yo, zc), "y", 1.0, 22)
    b -= cyl((0, yo, zc), "y", T + 1, 14)
    b += box(-22, 22, yo + T, yo + T + 2, zc - 14, zc + 14) - cyl((0, yo + T, zc), "y", 2, 14)
    for xx in (-60, 60):
        b -= Pos(xx, yo, zc + 5) * Rot(90, 0, 0) * extrude(SlotOverall(34, 6), -T - 1)
    for xx in (-79, 79):
        b += tie_loop("y", xx, BROW[0] + 7.5, yo + T, 1, gusset=False)
    add("brow", b, SMOKE, orient=[("x", 90)], note="front face down; smoked/black PETG")
    for xx in (-60, 60):
        lb = Pos(xx, yo, zc + 5) * Rot(90, 0, 0) * extrude(SlotOverall(34 - 2 * CLR, 6 - 2 * CLR), -T)
        lb += Pos(xx, yo + T, zc + 5) * Rot(90, 0, 0) * extrude(SlotOverall(38, 10), -2)
        add(f"lightbar_brow_{'ab'[xx > 0]}", lb, GREEN, file="lightbar_brow", orient=[("x", 90)],
            note="push in from inside, dot of hot glue")

# ---------------------------------------------------------------- green U shoulder
def shoulder():
    ztop = ZS - T
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * GAP / 2, sx * 400, sy * NY, sy * 400, 0, 800)
            s = (ring(0, T, ZT, ZS) & reg) + (rr(0, ztop, ZS) & reg)
            s += box(sx * GAP / 2, sx * (L / 2 - T + .01), sy * NY, sy * (NY + T), CART_TOP + TOP_CLR, ztop + .01)
            try:
                es = s.edges().filter_by_position(Axis.Z, ZS - .01, ZS + .01)
                es = [e for e in es if abs(e.center().Y) > NY + 2 and abs(e.center().X) > 3]
                s = fillet(es, 6)
            except Exception as ex:
                print("fillet skipped", ex)
            s += box(sx * GAP / 2, sx * 16, sy * 75, sy * 190, ztop - 6, ztop + .01)        # splice strip
            for yy in (sy * 95, sy * 170):
                s -= cyl((sx * 8, yy, ztop - 6), "z", 2.8, 4 + 2 * PIN_CLR)
            for (xx, yy) in ((sx * 60, sy * 150), (sx * 100, sy * 95)):                   # hanging tie loops (+ shaped hole)
                lp = box(xx - 8, xx + 8, yy - 8, yy + 8, CART_TOP + TOP_CLR - 1, ztop + .01)
                zl = CART_TOP + TOP_CLR + 1.5
                lp -= box(xx - 9, xx + 9, yy - TIE_W / 2, yy + TIE_W / 2, zl, zl + TIE_T)
                lp -= box(xx - TIE_W / 2, xx + TIE_W / 2, yy - 9, yy + 9, zl, zl + TIE_T)
                s += lp; INS["zip tie (4.8 mm, 200 mm)"] += 1
            if sy < 0:
                for xx in TRAY_HX:
                    s -= cyl((sx * xx, -W / 2 - 1, 590), "y", 6, 4.8)
            add(f"shoulder_{yn}{xn}", s, GREEN, orient=[("x", 180)], note="top face down, skirts up")
    for sy, yn in SYN:
        sp = box(-15, 15, sy * 80, sy * 185, ztop - 9.5, ztop - 6)
        for sx in (1, -1):
            for yy in (sy * 95, sy * 170):
                sp += cyl((sx * 8, yy, ztop - 6), "z", 2.5, 4.0)
        add(f"splice_shoulder_{yn}", sp, CHAR, file="splice_shoulder", note="pins up; dot of glue in each pin hole")

# ---------------------------------------------------------------- plinth + new fenders for D120 wheels
TAB_A = 60.0     # fender tab angle (deg from horizontal)
def fender_tabs():
    import math
    r = 78.5
    return [(sy * WHEEL_Y + k * r * math.cos(math.radians(TAB_A)), AXLE_Z + r * math.sin(math.radians(TAB_A)))
            for sy in (1, -1) for k in (1, -1)]

def plinth():
    for sx, xn in SXN:
        for sy, yn in SYN:
            reg = box(sx * GAP / 2, sx * 400, sy * GAP / 2, sy * 400, 0, 800)
            p = ring(0, TP, ZB, ZP) & reg
            excl = box(-PX + .5, PX - .5, -400, -100, 0, 800) + box(-400, -100, -PY + .5, PY - .5, 0, 800)
            p += lip(reg, ZP, TOPLIP_H, excl)
            try:
                p -= rr(0, ZB, ZB + 3) - Pos(0, 0, ZB) * extrude(RectangleRounded(L - 6, W - 6, R - 3), 3, taper=-44.9)
            except Exception as ex:
                print("chamfer skip", ex)
            # round wheel/motor-holder opening behind each wheel, a bit smaller than the wheel (hidden by wheel + fender)
            p -= cyl((sx * (L / 2 - TP - 1), sy * WHEEL_Y, AXLE_Z), "x", sx * (TP + 2), 2 * WHEEL_HOLE_R)
            for (ty, tz) in fender_tabs():
                if ty * sy > 0:
                    p -= box(sx * (L / 2 - TP - 1), sx * (L / 2 + 1), ty - 6.3, ty + 6.3, tz - 3.3, tz + 3.3)
            for xx in (sx * 60,):
                p += tie_loop("y", xx, (ZB + ZP) / 2 + 10, sy * (W / 2 - TP), -sy)
            add(f"plinth_{yn}{xn}", p & reg, CHAR, note="print upright, chamfered edge on bed")

FR_IN, FR_OUT, FR_FL = 68.0, 71.0, 85.0      # hood bore / hood outer / flange outer radius (wheel r = 60 -> 8 mm clearance)
def fenders():
    """Fender hood for a D120 mecanum wheel. PRINT with the outer cap on the bed (axis vertical): the flange is
    flared at 45 deg so the whole part prints without supports. Two tabs go through slots in the plinth; the
    fender hangs on them (gravity) and a zip tie / dot of glue stops it pulling out."""
    for sx, xn in SXN:
        for sy, yn in SYN:
            x0 = sx * L / 2
            c = (sy * WHEEL_Y, AXLE_Z)
            def ann(r0, r1, xa, xb):
                a = cyl((xa, c[0], c[1]), "x", xb - xa, 2 * r1)
                return a - cyl((xa - sx, c[0], c[1]), "x", (xb - xa) + 2 * sx, 2 * r0) if r0 else a
            ylim = box(-400, 400, -(W / 2 - R) + 1, (W / 2 - R) - 1, 0, 800)
            hood = ann(FR_IN, FR_OUT, x0, x0 + sx * (WHEEL_W + 10))
            hood += ann(0, FR_OUT, x0 + sx * (WHEEL_W + 10), x0 + sx * (WHEEL_W + 13))          # outer cap
            fl = ann(FR_IN, FR_FL, x0, x0 + sx * T)                                              # flat flange against plinth
            h = 1.2 * (FR_FL - FR_OUT)                                                           # flare 40 deg from vertical
            cone = Pos(x0 + sx * T, c[0], c[1]) * Rot(0, 90 * sx, 0) * Cone(FR_FL, FR_OUT, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
            cone -= cyl((x0, c[0], c[1]), "x", sx * (T + h + 2), 2 * FR_IN)
            hood += (fl + cone) & ylim
            hood &= box(-400, 400, -400, 400, 45, ZP - 1)
            for (ty, tz) in fender_tabs():
                if ty * sy > 0:
                    tab = box(x0 - sx * 18, x0 + sx * 0.5, ty - 6, ty + 6, tz - 3, tz + 3)
                    tab -= box(x0 - sx * 16, x0 - sx * 13, ty - TIE_W / 2, ty + TIE_W / 2, tz - 4, tz + 4)
                    hood += tab; INS["zip tie (4.8 mm, 200 mm)"] += 1
            add(f"fender_{yn}{xn}", hood, GREY, orient=[("y", 90 * sx)],
                note="PRINT cap-down (axis vertical); flare 40 deg from vertical, no supports")

# ---------------------------------------------------------------- tray (original, moved to the new front/top) + mount
def tray_mount():
    yi = -(W / 2 - T - CLR)
    b = box(-88.5, 88.5, yi, yi + 12, 569, ZS - T - 0.5)
    for xx in TRAY_HX:
        for sx in (1, -1):
            b -= cyl((sx * xx, yi, 590), "y", INS4_L, INS4_D)                 # insert bore 5.6 x 8
            b -= cyl((sx * xx, yi + INS4_L, 590), "y", 3.0, 4.4); INS["M4 insert"] += 1   # screw relief
    Yf = -CART_L / 2
    for xx in (-40, 40):          # arms back to the cart's top basket rim, with two crossing tie tunnels
        arm = box(xx - 8, xx + 8, yi + 11, Yf - 0.7, 586, 600)
        arm -= box(xx - 9, xx + 9, Yf - 9.7, Yf - 6.7, 589.75, 596.25)               # tunnel A along X
        arm -= box(xx - TIE_W / 2, xx + TIE_W / 2, Yf - 4.7, Yf - 1.7, 585, 601)       # tunnel B up/down
        b += arm; INS["zip tie (4.8 mm, 200 mm)"] += 1
    add("tray_mount", b, CHAR, orient=[("x", 90)], note="plate face down")

def reused(step_path):
    a = import_step(step_path)
    tray = a.solids()[0].translate((2.5, 0, 45))     # flush to new front skin, up to the green shoulder
    add("tray", tray, GREY, note="original v1 tray geometry, moved +2.5 mm X / +45 mm Z", world=True)

def build(step_path):
    PARTS.clear(); INS.clear(); POST_ADD.clear()
    refs(); doors(); vents(); posts(); rear(); left(); channel_caps(); brow(); shoulder(); plinth(); fenders(); tray_mount()
    toW = Rot(0, 0, 90)
    for p in PARTS:
        if p["wshape"] is None:
            p["wshape"] = toW * p["dshape"]
    reused(step_path)
    for p in PARTS:
        p["shape"] = p["wshape"]
        if p["dshape"] is None:
            p["dshape"] = p["wshape"]
    return PARTS
