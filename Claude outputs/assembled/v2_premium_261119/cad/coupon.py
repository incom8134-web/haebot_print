"""Tolerance-test coupon: tongue/groove, dovetail key, alignment pin, M3 insert boss, slot cap.
Three variants per feature around nominal. One printable plate (<200 x 200 mm)."""
from build123d import *
import v2

def label(txt, x, y, z, size=5):
    with BuildPart() as tp:
        with BuildSketch(Plane.XY.offset(z - 0.6)):
            with Locations((x, y)):
                Text(txt, size, align=(Align.CENTER, Align.CENTER))
        extrude(amount=0.7)
    return tp.part

def coupon():
    parts = []
    CL = [0.20, 0.30, 0.40]          # sliding clearance per side
    CAP = [0.30, 0.35, 0.45]         # cap clearance
    INSD = [3.8, 4.0, 4.2]           # insert hole options
    for i, c in enumerate(CL):
        y0 = i * 62.0
        # -- tongue / groove (rabbet section, 30 long)
        g = v2.box(0, 30, y0, y0 + 16, 0, 14)
        g -= v2.box(0, 30, y0 + 6 - c, y0 + 6 + 2.7 + c, 4, 14)
        g -= label(f"{c:.2f}", 15, y0 + 13, 14, 3.5)
        t = v2.box(0, 30, y0 + 20, y0 + 30, 0, 3) + v2.box(0, 30, y0 + 23, y0 + 25.7, 3, 13)
        parts += [g, t]
        # -- dovetail key: two half blocks with pocket (+c) and nominal key
        for k, zz in enumerate((0,)):
            lo = v2.box(36, 72, y0, y0 + 22, 0, 12)
            pts = [(-7 - c, -8 - c), (7 + c, -8 - c), (4 + c, 0), (7 + c, 8 + c), (-7 - c, 8 + c), (-4 - c, 0)]
            pk = Pos(36, y0 + 11, 12) * extrude(Plane.YZ * Polygon(*pts, align=None), 36)
            lo -= pk
            parts.append(lo)
            hi = v2.box(36, 72, y0 + 24, y0 + 46, 0, 12)
            pk2 = Pos(36, y0 + 35, 0) * extrude(Plane.YZ * Polygon(*pts, align=None), 36)
            hi -= pk2
            parts.append(hi)
        key = Pos(76, y0 + 11, 8) * extrude(Plane.YZ * Polygon((-7, -8), (7, -8), (4, 0), (7, 8), (-7, 8), (-4, 0), align=None), 30)
        parts.append(key)
        # -- pins / holes
        ph = v2.box(110, 136, y0, y0 + 20, 0, 6)
        for xx in (116, 130):
            ph -= v2.cyl((xx, y0 + 10, 6), "z", -3, 4 + 2 * (c - 0.05))
        pp = v2.box(110, 136, y0 + 24, y0 + 44, 0, 3)
        for xx in (116, 130):
            pp += v2.cyl((xx, y0 + 34, 3), "z", 2.5, 4.0)
        parts += [ph, pp]
        # -- insert boss (hole option)
        bs = v2.box(140, 160, y0, y0 + 20, 0, 3) + v2.cyl((150, y0 + 10, 3), "z", 8, 9) + v2.cyl((150, y0 + 10, 3), "z", 1.6, 12.2)
        bs -= v2.cyl((150, y0 + 10, 11), "z", -7, INSD[i])
        bs -= label(f"{INSD[i]:.1f}", 150, y0 + 17.2, 3, 3)
        parts.append(bs)
        # -- slot cap + port
        cp = v2.box(164, 222, y0, y0 + 16, 0, 5.5)
        cp -= Pos(193, y0 + 8, 5.5) * extrude(SlotOverall(50, 8), -3)
        cap = Pos(193, y0 + 30, 0) * extrude(SlotOverall(50 - 2 * CAP[i], 8 - 2 * CAP[i]), 2.5)
        cap -= label(f"{CAP[i]:.2f}", 193, y0 + 30, 2.5, 3)
        parts += [cp, cap]
    return Compound(children=parts)
