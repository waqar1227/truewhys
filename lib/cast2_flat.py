"""Bridge: cast v2.1 (lib/cast2.py, owner-approved 15 Nov 2026) inside the Style F engine (lib/flat2d.py).

    from cast2_flat import char2
    char2(g, "captain", x, y, h=900, expr="shocked", pose_l="down", pose_r="point", t=c.gt, flip=False)

x, y = feet position (design units, under the shot camera); h = height from feet to head top in design units.
The figure is drawn from a cached raster (cairosvg) at a resolution matched to its on-screen size, so it stays sharp.
t enables automatic blinks and a slight breathing motion. Every drawn figure records its on-screen box in DRAWN,
which flat2d.Video uses for the first-frame QA check (audit §6.3: character >= 45 % of frame height on frame 1).
"""
import io, math
import cairocffi as cairo
import cairosvg
import cast2

NOMINAL_H = 565.0                 # feet (y=0) to head top in cast2 units (head scaled by HEAD_K)
VB = (-300, -760, 600, 790)       # viewbox wide enough for pointing arms and tall props
_CACHE = {}
DRAWN = []                        # [(x0, y0, x1, y1) in device pixels] for figures drawn in the current frame

# extra expressions (kept here so the approved sheet's set stays unchanged)
cast2.EXPR.setdefault("blink", dict(lid=1.0, brow=((0, 0), (0, 0)), mouth="flat"))
cast2.EXPR.setdefault("worried", dict(lid=0.25, brow=((-12, 4), (-12, 4)), mouth="flat_down"))
cast2.EXPR.setdefault("curious", dict(lid=0.2, brow=((-4, -10), (6, 0)), mouth="side", look=(1, 0)))


def _q(pose):
    """Quantise a blended pose (a, b, u) to 8 steps so the raster cache stays small."""
    if isinstance(pose, (tuple, list)):
        u = round(max(0.0, min(1.0, pose[2])) * 8) / 8
        return pose[0] if u == 0 else pose[1] if u == 1 else (pose[0], pose[1], u)
    return pose


_EASE = {}


def _ease(cid, side, x, pose, t, dur=0.25):
    """Automatic easing: when a figure's pose changes between frames, blend from the old pose over `dur` s (no snapping)."""
    if not isinstance(pose, str):
        return pose
    key = (cid, side, int(x // 300))
    st = _EASE.get(key)
    if st is None or t < st["t"] or t - st["t"] > 0.4:
        _EASE[key] = dict(t=t, target=pose, src=pose, t0=-9)
        return pose
    st["t"] = t
    if pose != st["target"]:
        u = (t - st["t0"]) / dur
        st["src"] = st["target"] if u >= 0.5 else st["src"]
        st["target"], st["t0"] = pose, t
    u = (t - st["t0"]) / dur
    return (st["src"], st["target"], u) if 0 <= u < 1 and st["src"] != st["target"] else pose


def pose_at(t, keys, dur=0.28):
    """Gradual arm moves: keys = [(t0, pose), (t1, pose), ...]; returns the pose (or a blend) at time t.
    Each change eases over `dur` seconds starting at its key time (no snapping)."""
    cur = keys[0][1]
    for i in range(1, len(keys)):
        tk, pk = keys[i]
        if t < tk:
            break
        u = (t - tk) / dur
        if u < 1:
            return (cur, pk, u) if isinstance(cur, str) and isinstance(pk, str) else pk
        cur = pk
    return cur


def turn_at(t, t0, to_left=True, dur=0.24):
    """A proper turn instead of an instant mirror flip: facing right -> 3/4 -> front -> 3/4 -> facing left (or back).
    Returns (view, flip) for char2. Before t0 the character faces the start side in 3/4 view."""
    u = (t - t0) / dur
    a, b = ("3q", False), ("3q", True)
    if not to_left:
        a, b = b, a
    if u <= 0:
        return a
    if u >= 1:
        return b
    return a if u < 0.33 else ("front", False) if u < 0.67 else b


def _surface(cid, expr, pl, pr, scale, prop=True, view="front"):
    pl, pr = _q(pl), _q(pr)
    key = (cid, expr, pl, pr, scale, prop, view)
    s = _CACHE.get(key)
    if s is None:
        x0, y0, w, h = VB
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w} {h}" width="{w}" height="{h}">'
               f'<g stroke="{cast2.INK}" stroke-width="{cast2.SW}" stroke-linejoin="round" stroke-linecap="round">'
               f'{cast2.figure_svg(cid, expr, pl, pr, prop, view)}</g></svg>')
        png = cairosvg.svg2png(bytestring=svg.encode(), scale=scale)
        s = cairo.ImageSurface.create_from_png(io.BytesIO(png))
        if len(_CACHE) > 400:
            _CACHE.clear()
        _CACHE[key] = s
    return s


def _blinking(t, seed):
    if t is None:
        return False
    period = 3.1 + (seed % 7) * 0.37
    ph = (t + seed * 0.71) % period
    return ph < 0.11


def char2(g, cid, x, y, h=900.0, expr="deadpan", pose_l="down", pose_r="hold", t=None, flip=False, rot=0.0, breathe=True, a=1.0,
          blink=True, squash=0.0, prop=None, view=None):
    """Draw cast v2.2 character `cid` with feet at (x, y), `h` design units tall.
    pose_l/pose_r: a pose name or a blend from pose_at(); view "front" | "3q" (3/4 turn to screen right; flip=True faces left)."""
    k = h / NOMINAL_H
    if t is not None:
        pose_l = _ease(cid, "l", x, pose_l, t); pose_r = _ease(cid, "r", x, pose_r, t)
    if view is None:                                   # auto: a figure in the outer third faces the middle in 3/4 view
        fx = g.c.user_to_device(x, y)[0] / max(1, g.c.get_target().get_width())
        view = "3q" if t is not None and ((fx < 0.36 and not flip) or (fx > 0.64 and flip)) else "front"
    dev = abs(g.c.get_matrix().xx) or 1.0           # current device scale (camera zoom)
    want = k * dev
    scale = min(4.0, max(0.25, math.ceil(want * 4) / 4))   # quantised raster scale (>= on-screen size)
    seed = sum(map(ord, cid))
    e = "blink" if blink and _blinking(t, seed) and expr not in ("shocked",) else expr
    pr_name = pose_r if isinstance(pose_r, str) else (pose_r[1] if pose_r[2] > 0.5 else pose_r[0])
    prop = (pr_name in ("hold", "down", "point")) if prop is None else prop   # hide the role prop when the hands grab or wave
    surf = _surface(cid, e, pose_l, pose_r, scale, prop, view)
    br = 1 + (0.012 * math.sin((t or 0) * 2.4 + seed) if breathe and t is not None else 0)
    sy = br * (1 - squash); sx = (1 + squash * 0.6) / br ** 0.5
    c = g.c
    c.save()
    c.translate(x, y)
    if rot: c.rotate(rot)
    c.scale(k * sx * (-1 if flip else 1), k * sy)
    x0, y0, w, hh = VB
    c.translate(x0, y0)
    c.scale(1 / scale, 1 / scale)
    c.set_source_surface(surf, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint_with_alpha(a) if a < 1 else c.paint()
    c.restore()
    # on-screen box of head top..feet for QA
    c.save(); c.translate(x, y)
    if rot: c.rotate(rot)
    pts = [c.user_to_device(px * k, py * k) for px, py in ((-90, -NOMINAL_H), (90, -NOMINAL_H), (-90, 0), (90, 0))]
    c.restore()
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    DRAWN.append((min(xs), min(ys), max(xs), max(ys)))


def visible_height_frac(H=1920, W=1080):
    """Largest visible character height on the last drawn frame, as a fraction of the frame height."""
    best = 0.0
    for x0, y0, x1, y1 in DRAWN:
        if x1 < 0 or x0 > W:
            continue
        vis = max(0.0, min(y1, H) - max(y0, 0))
        best = max(best, vis / H)
    return best
