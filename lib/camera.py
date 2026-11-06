"""Shared camera maths (pure numpy). Used by Blender (to animate the camera) and by the
compositor (to project 3D anchor points of 2D characters), so both always agree."""
import math
import numpy as np

SENSOR = 36.0  # mm, horizontal fit


def ease(t, kind="inout"):
    t = min(1.0, max(0.0, t))
    if kind == "linear":
        return t
    if kind == "out":
        return 1 - (1 - t) ** 3
    if kind == "in":
        return t ** 3
    return t * t * (3 - 2 * t) if kind == "smooth" else (4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2)


def lerp(a, b, t):
    return [x + (y - x) * t for x, y in zip(a, b)]


def cam_at(cam, t):
    """cam = {"from": {"pos":[..],"tgt":[..],"lens":f}, "to": {...}|None, "ease": "inout", "shake": amp}
    t = 0..1 progress through the shot. Returns pos, tgt, lens."""
    a = cam["from"]; b = cam.get("to") or a
    k = ease(t, cam.get("ease", "inout"))
    pos = lerp(a["pos"], b["pos"], k)
    tgt = lerp(a["tgt"], b["tgt"], k)
    lens = a["lens"] + (b["lens"] - a["lens"]) * k
    if cam.get("orbit"):  # degrees around tgt (z axis) over the shot
        ang = math.radians(cam["orbit"] * (k - 0.5))
        dx, dy = pos[0] - tgt[0], pos[1] - tgt[1]
        pos = [tgt[0] + dx * math.cos(ang) - dy * math.sin(ang), tgt[1] + dx * math.sin(ang) + dy * math.cos(ang), pos[2]]
    return pos, tgt, lens


def basis(pos, tgt):
    f = np.array(tgt, float) - np.array(pos, float)
    f /= np.linalg.norm(f)
    up = np.array([0, 0, 1.0])
    r = np.cross(f, up); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return f, r, u


def project(p, pos, tgt, lens, W, H):
    """World point -> (x_px, y_px, depth_m, px_per_m_at_depth)."""
    f, r, u = basis(pos, tgt)
    d = np.array(p, float) - np.array(pos, float)
    z = float(d @ f)
    if z < 0.05:
        z = 0.05
    fpx = lens / SENSOR * W
    return W / 2 + fpx * float(d @ r) / z, H / 2 - fpx * float(d @ u) / z, z, fpx / z
