"""Tiny z-buffer renderer (orthographic, flat Lambert + part/edge outlines)."""
import numpy as np
from numba import njit
from PIL import Image, ImageDraw, ImageFont

def hex2rgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float) / 255

def mesh_of(shape, tol=0.4, ang=0.25):
    v, t = shape.tessellate(tol, ang)
    V = np.array([[p.X, p.Y, p.Z] for p in v], float)
    Tt = np.array(t, np.int64).reshape(-1, 3) if len(t) else np.zeros((0, 3), np.int64)
    return V, Tt

@njit(cache=True)
def _raster(P, F, C, ids, W, H, zbuf, cbuf, ibuf):
    for k in range(F.shape[0]):
        a, b, c = F[k, 0], F[k, 1], F[k, 2]
        x0, y0, z0 = P[a, 0], P[a, 1], P[a, 2]
        x1, y1, z1 = P[b, 0], P[b, 1], P[b, 2]
        x2, y2, z2 = P[c, 0], P[c, 1], P[c, 2]
        minx = max(int(min(x0, x1, x2)), 0); maxx = min(int(max(x0, x1, x2)) + 1, W - 1)
        miny = max(int(min(y0, y1, y2)), 0); maxy = min(int(max(y0, y1, y2)) + 1, H - 1)
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        for y in range(miny, maxy + 1):
            for x in range(minx, maxx + 1):
                px = x + 0.5; py = y + 0.5
                w0 = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) / den
                w1 = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) / den
                w2 = 1 - w0 - w1
                if w0 < -1e-6 or w1 < -1e-6 or w2 < -1e-6:
                    continue
                z = w0 * z0 + w1 * z1 + w2 * z2
                if z > zbuf[y, x]:
                    zbuf[y, x] = z
                    cbuf[y, x, 0] = C[k, 0]; cbuf[y, x, 1] = C[k, 1]; cbuf[y, x, 2] = C[k, 2]
                    ibuf[y, x] = ids[k]

def view_matrix(azim, elev):
    a, e = np.radians(azim), np.radians(elev)
    d = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])  # toward camera
    up = np.array([0, 0, 1.0])
    if abs(d[2]) > 0.99:
        up = np.array([0, 1.0, 0]) if d[2] > 0 else np.array([0, 1.0, 0])
    r = np.cross(up, d); r /= np.linalg.norm(r)
    u = np.cross(d, r)
    return np.stack([r, u, d]), d

def render(meshes, azim, elev, out, size=(1400, 1100), title=None, bg=(244, 245, 247), ss=2, bounds=None,
           light=None, edges=True, labels=None):
    """meshes: list of (V, T, hexcolor)"""
    M, d = view_matrix(azim, elev)
    Wd, Hd = size[0] * ss, size[1] * ss
    allP = np.vstack([m[0] for m in meshes if len(m[0])])
    Q = allP @ M.T
    lo, hi = Q.min(0), Q.max(0)
    if bounds is not None:
        lo, hi = bounds
    span = max((hi[0] - lo[0]) / (Wd * 0.86), (hi[1] - lo[1]) / (Hd * 0.80))
    cx, cy = (hi[0] + lo[0]) / 2, (hi[1] + lo[1]) / 2
    Ls = np.array(light if light is not None else (0.35, -0.55, 0.75)); Ls /= np.linalg.norm(Ls)
    zbuf = np.full((Hd, Wd), -1e18); cbuf = np.zeros((Hd, Wd, 3)); ibuf = np.full((Hd, Wd), -1, np.int64)
    for mi, (V, Tt, col) in enumerate(meshes):
        if len(Tt) == 0: continue
        q = V @ M.T
        P = np.empty_like(q)
        P[:, 0] = (q[:, 0] - cx) / span + Wd / 2
        P[:, 1] = Hd / 2 - (q[:, 1] - cy) / span
        P[:, 2] = q[:, 2]
        n = np.cross(V[Tt[:, 1]] - V[Tt[:, 0]], V[Tt[:, 2]] - V[Tt[:, 0]])
        nn = np.linalg.norm(n, axis=1, keepdims=True); nn[nn == 0] = 1; n = n / nn
        facing = (n @ d)
        n[facing < 0] *= -1
        lam = np.clip(n @ Ls, 0, 1)
        amb = 0.50
        base = hex2rgb(col)
        sh = (amb + (1 - amb) * lam)[:, None] * base[None, :]
        # subtle view-facing boost
        sh = np.clip(sh + 0.06 * np.abs(facing)[:, None], 0, 1)
        _raster(P, Tt, sh, np.full(len(Tt), mi, np.int64), Wd, Hd, zbuf, cbuf, ibuf)
    img = np.empty((Hd, Wd, 3))
    img[:] = np.array(bg) / 255
    m = ibuf >= 0
    img[m] = cbuf[m]
    if edges:
        idd = ibuf
        e = np.zeros_like(m)
        e[:, 1:] |= idd[:, 1:] != idd[:, :-1]
        e[1:, :] |= idd[1:, :] != idd[:-1, :]
        dz = np.zeros_like(zbuf)
        zb = np.where(m, zbuf, zbuf[m].min() if m.any() else 0)
        dz[:, 1:] = np.abs(zb[:, 1:] - zb[:, :-1]); dz[1:, :] = np.maximum(dz[1:, :], np.abs(zb[1:, :] - zb[:-1, :]))
        e |= dz > 6 * span
        img[e] = img[e] * 0.25
    im = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).resize(size, Image.LANCZOS)
    if title:
        dr = ImageDraw.Draw(im)
        try:
            f = ImageFont.truetype("DejaVuSans-Bold.ttf", 30)
        except Exception:
            f = ImageFont.load_default()
        dr.text((30, 22), title, fill=(40, 42, 46), font=f)
    if labels:
        dr = ImageDraw.Draw(im)
        try: f2 = ImageFont.truetype("DejaVuSans.ttf", 18)
        except Exception: f2 = ImageFont.load_default()
        for (p3, txt) in labels:
            q = np.array(p3) @ M.T
            x = ((q[0] - cx) / span + Wd / 2) / ss; y = (Hd / 2 - (q[1] - cy) / span) / ss
            dr.text((x, y), txt, fill=(200, 30, 30), font=f2)
    im.save(out)
    return im
