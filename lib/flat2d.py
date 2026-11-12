"""Style F (flat 2D) engine for TrueWhys: clean vector look drawn with cairo (thick ink outlines, flat fills, warm glows),
camera with parallax layers, word-by-word captions, hook title block, Wy end card, parallel render to MP4. Runs on CPU.

Typical episode script (episodes/<ep>/make.py):
    from flat2d import *                     # G drawing helpers, easing, Video
    V = Video(EP, title=("THE ACCIDENT THAT", "INVENTED STEEL"), keys={"steel"})
    V.shot("H1", fn, part=(0, "inside"), cam=push(1.0, 1.1, (540, 1100)), sfx=[(0.0, "whoosh", 0.5)], music="curious")
    V.build()                                # timings from timing.json (lib/voice_gemini.py), Wy end card appended (line O1)
    V.sheet("stills.png"); V.render("final/A-0xx.mp4")
A shot function is fn(g, c): g = G (drawing in a 1080x1920 design space under the shot camera), c = shot context
(c.t seconds since the shot start, c.T shot length, c.u = t/T, c.w("word") = time of a spoken word in this shot's line,
c.since("word") = seconds since that word, c.env = narrator level 0..1).
"""
import os, sys, re, json, math, functools, subprocess, shutil, random
from contextlib import contextmanager
from pathlib import Path
import numpy as np
import cairocffi as cairo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "lib"))
W, H, FPS = 1080, 1920, 30
TAU = math.tau
PAL = dict(teal="#0F6B78", deep="#0B3F4C", navy="#10263B", yellow="#FFC93C", coral="#FF6B5B", cream="#FFF4E0", ink="#2A1C1E",
           mint="#5ED3B5", white="#FFFFFF", black="#000000")
INK = PAL["ink"]


def ensure_fonts():
    d = Path.home() / ".local/share/fonts"
    if not (d / "LilitaOne-Regular.ttf").exists():
        d.mkdir(parents=True, exist_ok=True)
        for f in (ROOT / "library/fonts").glob("*.ttf"):
            shutil.copy(f, d / f.name)
        subprocess.run(["fc-cache", "-f"], capture_output=True)


ensure_fonts()

# ------------------------------------------------------------------ colour + easing


@functools.lru_cache(maxsize=4096)
def _hex(c):
    c = PAL.get(c, c).lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))


def rgba(c, a=1.0):
    if isinstance(c, str):
        return (*_hex(c), a)
    return (c[0], c[1], c[2], (c[3] if len(c) > 3 else 1.0) * a)


def mix(c1, c2, k):
    a, b = rgba(c1), rgba(c2)
    k = max(0.0, min(1.0, k))
    return tuple(a[i] + (b[i] - a[i]) * k for i in range(4))


def shade(c, k):
    """k < 0 darker, k > 0 lighter."""
    return mix(c, "#000000" if k < 0 else "#FFFFFF", abs(k))


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, k):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * k for x, y in zip(a, b))
    return a + (b - a) * k


def seg(t, t0, d):
    """0..1 progress of an interval starting at t0 lasting d."""
    return clamp((t - t0) / d) if d > 0 else (1.0 if t >= t0 else 0.0)


def ease_out(x):
    x = clamp(x); return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x); return x ** 3


def ease_io(x):
    x = clamp(x); return x * x * (3 - 2 * x)


def back_out(x, s=1.9):
    x = clamp(x) - 1
    return 1 + x * x * ((s + 1) * x + s)


def elastic(x, f=3.0, d=5.5):
    x = clamp(x)
    return 1 - math.exp(-d * x) * math.cos(TAU * f * x) if x < 1 else 1.0


def bounce(x):
    x = clamp(x)
    if x < 1 / 2.75: return 7.5625 * x * x
    if x < 2 / 2.75: x -= 1.5 / 2.75; return 7.5625 * x * x + 0.75
    if x < 2.5 / 2.75: x -= 2.25 / 2.75; return 7.5625 * x * x + 0.9375
    x -= 2.625 / 2.75; return 7.5625 * x * x + 0.984375


def pop(t, t0=0.0, d=0.32, s=1.9):
    """Scale 0 -> 1 with overshoot, starting at t0 (0 before)."""
    return 0.0 if t < t0 else back_out((t - t0) / d, s)


def pulse(t, t0, d=0.3, amp=1.0):
    """A bump 0 -> amp -> 0 starting at t0."""
    x = (t - t0) / d
    return amp * math.sin(math.pi * x) if 0 < x < 1 else 0.0


def wig(t, f=1.0, seed=0.0):
    """Smooth organic wobble in -1..1."""
    return 0.6 * math.sin(TAU * f * t + seed * 1.7) + 0.4 * math.sin(TAU * f * 1.73 * t + seed * 4.1 + 1.3)


def kf(t, keys, ease=ease_io):
    """Keyframes [(time, value[, ease])]; values are numbers or tuples."""
    if t <= keys[0][0]:
        return keys[0][1]
    for a, b in zip(keys, keys[1:]):
        if t <= b[0]:
            e = b[2] if len(b) > 2 else ease
            return lerp(a[1], b[1], e((t - a[0]) / max(1e-6, b[0] - a[0])))
    return keys[-1][1]


def rnd(seed):
    return random.Random(seed)


# ------------------------------------------------------------------ SVG-style path strings

_TOK = re.compile(r"([MLHVCSQTZmlhvcsqtz])|(-?\d*\.?\d+(?:[eE][-+]?\d+)?)")
_NARG = dict(M=2, L=2, H=1, V=1, C=6, S=4, Q=4, T=2, Z=0)


@functools.lru_cache(maxsize=8192)
def parse_path(d):
    out, toks, i, cmd = [], _TOK.findall(d), 0, None
    x = y = sx = sy = 0.0
    pc = None  # previous control point (for S/T)
    while i < len(toks):
        if toks[i][0]:
            cmd = toks[i][0]; i += 1
            if cmd in "Zz":
                out.append(("Z",)); x, y = sx, sy; pc = None
                continue
        n = _NARG[cmd.upper()]
        a = [float(toks[i + k][1]) for k in range(n)]; i += n
        rel = cmd.islower(); C = cmd.upper()
        if C == "M":
            x, y = (x + a[0], y + a[1]) if rel else (a[0], a[1]); sx, sy = x, y
            out.append(("M", x, y)); cmd = "l" if rel else "L"; pc = None
        elif C == "L":
            x, y = (x + a[0], y + a[1]) if rel else (a[0], a[1]); out.append(("L", x, y)); pc = None
        elif C == "H":
            x = x + a[0] if rel else a[0]; out.append(("L", x, y)); pc = None
        elif C == "V":
            y = y + a[0] if rel else a[0]; out.append(("L", x, y)); pc = None
        elif C in "CS":
            if C == "S":
                x1, y1 = (2 * x - pc[0], 2 * y - pc[1]) if pc else (x, y)
                x2, y2, x3, y3 = a
                if rel: x2, y2, x3, y3 = x + x2, y + y2, x + x3, y + y3
            else:
                x1, y1, x2, y2, x3, y3 = a
                if rel: x1, y1, x2, y2, x3, y3 = x + x1, y + y1, x + x2, y + y2, x + x3, y + y3
            out.append(("C", x1, y1, x2, y2, x3, y3)); pc = (x2, y2); x, y = x3, y3
        elif C in "QT":
            if C == "T":
                qx, qy = (2 * x - pc[0], 2 * y - pc[1]) if pc else (x, y)
                x3, y3 = a
                if rel: x3, y3 = x + x3, y + y3
            else:
                qx, qy, x3, y3 = a
                if rel: qx, qy, x3, y3 = x + qx, y + qy, x + x3, y + y3
            out.append(("C", x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y), x3 + 2 / 3 * (qx - x3), y3 + 2 / 3 * (qy - y3), x3, y3))
            pc = (qx, qy); x, y = x3, y3
    return tuple(out)


@functools.lru_cache(maxsize=2048)
def _flat(d, n=18):
    """Path string -> polyline points + cumulative lengths."""
    pts, cur, start = [], (0.0, 0.0), (0.0, 0.0)
    for op in parse_path(d):
        if op[0] == "M":
            cur = start = (op[1], op[2]); pts.append(cur)
        elif op[0] == "L":
            cur = (op[1], op[2]); pts.append(cur)
        elif op[0] == "C":
            x0, y0 = cur
            x1, y1, x2, y2, x3, y3 = op[1:]
            for i in range(1, n + 1):
                u = i / n; v = 1 - u
                pts.append((v ** 3 * x0 + 3 * v * v * u * x1 + 3 * v * u * u * x2 + u ** 3 * x3, v ** 3 * y0 + 3 * v * v * u * y1 + 3 * v * u * u * y2 + u ** 3 * y3))
            cur = (x3, y3)
        else:
            pts.append(start); cur = start
    cum = [0.0]
    for a, b in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return tuple(pts), tuple(cum)


def path_len(d):
    return _flat(d)[1][-1]


def path_at(d, u):
    """Point and direction (x, y, angle) at fraction u (0..1) of a path string's length."""
    pts, cum = _flat(d)
    L = cum[-1] * clamp(u)
    lo, hi = 0, len(cum) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if cum[mid] <= L: lo = mid
        else: hi = mid
    a, b = pts[lo], pts[hi]
    k = (L - cum[lo]) / max(1e-9, cum[hi] - cum[lo])
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, math.atan2(b[1] - a[1], b[0] - a[0]))


def path_part(d, u0, u1):
    """Polyline of the part of a path between fractions u0 and u1 (for drawing a line on progressively)."""
    pts, cum = _flat(d)
    u0, u1 = clamp(u0), clamp(u1)
    if u1 <= u0:
        p = path_at(d, u0); return [(p[0], p[1]), (p[0], p[1])]
    L0, L1 = cum[-1] * u0, cum[-1] * u1
    out = [path_at(d, u0)[:2]]
    out += [p for p, c in zip(pts, cum) if L0 < c < L1]
    out.append(path_at(d, u1)[:2])
    return out


# ------------------------------------------------------------------ drawing context


class G:
    """Thin wrapper over a cairo context: outlined flat shapes in design units (1080x1920)."""

    def __init__(s, surf):
        s.surf = surf
        s.c = cairo.Context(surf)
        s.c.set_line_join(cairo.LINE_JOIN_ROUND); s.c.set_line_cap(cairo.LINE_CAP_ROUND)
        s.lw = 7.0
        s.base = s.c.get_matrix()
        s.cam = (W / 2, H / 2, 1.0, 0.0)

    # -- camera / transforms
    def set_cam(s, cx, cy, z, rot=0.0, depth=1.0):
        c = s.c
        c.set_matrix(s.base)
        zz = max(1e-3, 1 + (z - 1) * depth)
        c.translate(W / 2, H / 2)
        if rot: c.rotate(rot * depth)
        c.scale(zz, zz)
        c.translate(-(W / 2 + (cx - W / 2) * depth), -(H / 2 + (cy - H / 2) * depth))
        if depth == 1.0:
            s.cam = (cx, cy, z, rot)

    @contextmanager
    def layer(s, depth):
        """Parallax layer: depth < 1 moves less than the main plane (far), > 1 more (near), 0 = screen space."""
        m = s.c.get_matrix()
        cam = s.cam
        s.set_cam(*cam, depth=depth)
        try:
            yield
        finally:
            s.c.set_matrix(m); s.cam = cam

    def screen(s):
        return s.layer(0.0)

    @contextmanager
    def at(s, x=0.0, y=0.0, rot=0.0, sx=1.0, sy=None):
        c = s.c
        c.save(); c.translate(x, y)
        if rot: c.rotate(rot)
        sy = sx if sy is None else sy
        if sx != 1 or sy != 1:
            c.scale(sx if abs(sx) > 1e-3 else 1e-3, sy if abs(sy) > 1e-3 else 1e-3)
        try:
            yield
        finally:
            c.restore()

    @contextmanager
    def group(s, alpha=1.0):
        """Draw a group, then composite it with one alpha (no double-darkening where shapes overlap)."""
        s.c.push_group()
        try:
            yield
        finally:
            s.c.pop_group_to_source(); s.c.paint_with_alpha(clamp(alpha))

    @contextmanager
    def clip(s, d=None, circle=None, rect=None, ellipse=None):
        c = s.c
        c.save(); c.new_path()
        if d is not None: s._trace(d)
        if circle is not None: c.arc(circle[0], circle[1], max(0.01, circle[2]), 0, TAU)
        if rect is not None: c.rectangle(*rect)
        if ellipse is not None:
            c.save(); c.translate(ellipse[0], ellipse[1]); c.scale(max(0.01, ellipse[2]), max(0.01, ellipse[3])); c.arc(0, 0, 1, 0, TAU); c.restore()
        c.clip()
        try:
            yield
        finally:
            c.restore()

    @contextmanager
    def clip_out(s, circles):
        """Draw everything except inside the given circles [(x, y, r)] (bite marks, holes)."""
        c = s.c
        c.save(); c.new_path()
        c.rectangle(-20000, -20000, 40000, 40000)
        for x, y, r in circles:
            c.new_sub_path(); c.arc(x, y, max(0.01, r), 0, TAU)
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD); c.clip(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
        try:
            yield
        finally:
            c.restore()

    # -- paint
    def _paint(s, fill, stroke, lw, a=1.0):
        c = s.c
        if fill is not None:
            if isinstance(fill, cairo.Pattern): c.set_source(fill)
            else: c.set_source_rgba(*rgba(fill, a))
            if stroke is not None: c.fill_preserve()
            else: c.fill()
        if stroke is not None:
            c.set_source_rgba(*rgba(stroke, a)); c.set_line_width(s.lw if lw is None else lw); c.stroke()
        elif fill is None:
            c.new_path()

    def _trace(s, d):
        c = s.c
        if isinstance(d, str):
            for op in parse_path(d):
                k = op[0]
                if k == "M": c.move_to(op[1], op[2])
                elif k == "L": c.line_to(op[1], op[2])
                elif k == "C": c.curve_to(*op[1:])
                else: c.close_path()
        else:  # list of points
            c.move_to(*d[0])
            for p in d[1:]:
                c.line_to(*p)

    # -- shapes (fill + ink outline by default; stroke=None for no outline)
    def circle(s, x, y, r, fill=None, stroke=INK, lw=None, a=1.0):
        s.c.new_path(); s.c.arc(x, y, max(r, 0.01), 0, TAU); s._paint(fill, stroke, lw, a)

    def ellipse(s, x, y, rx, ry, fill=None, stroke=INK, lw=None, a=1.0, rot=0.0):
        c = s.c
        c.save(); c.translate(x, y)
        if rot: c.rotate(rot)
        c.scale(max(rx, 0.01), max(ry, 0.01)); c.new_path(); c.arc(0, 0, 1, 0, TAU); c.restore()
        s._paint(fill, stroke, lw, a)

    def _rr(s, x, y, w, h, r):
        c = s.c
        if not isinstance(r, (tuple, list)): r = (r, r, r, r)
        m = min(w, h) / 2
        tl, tr, br, bl = (min(max(0.0, q), m) for q in r)
        c.new_path()
        c.move_to(x + tl, y); c.line_to(x + w - tr, y)
        if tr: c.arc(x + w - tr, y + tr, tr, -TAU / 4, 0)
        c.line_to(x + w, y + h - br)
        if br: c.arc(x + w - br, y + h - br, br, 0, TAU / 4)
        c.line_to(x + bl, y + h)
        if bl: c.arc(x + bl, y + h - bl, bl, TAU / 4, TAU / 2)
        c.line_to(x, y + tl)
        if tl: c.arc(x + tl, y + tl, tl, TAU / 2, TAU * 0.75)
        c.close_path()

    def rect(s, x, y, w, h, fill=None, stroke=INK, lw=None, r=0, a=1.0):
        """Top-left x, y; r = corner radius (number or (tl, tr, br, bl))."""
        s._rr(x, y, w, h, r); s._paint(fill, stroke, lw, a)

    def rc(s, cx, cy, w, h, fill=None, stroke=INK, lw=None, r=0, a=1.0, rot=0.0):
        """Rectangle centred on cx, cy."""
        if rot:
            with s.at(cx, cy, rot):
                s._rr(-w / 2, -h / 2, w, h, r)
            s._paint(fill, stroke, lw, a)
        else:
            s._rr(cx - w / 2, cy - h / 2, w, h, r); s._paint(fill, stroke, lw, a)

    def poly(s, pts, fill=None, stroke=INK, lw=None, a=1.0, close=True, r=0):
        c = s.c
        c.new_path()
        n = len(pts)
        if r and n >= 3 and close:
            for i in range(n):
                p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
                d0 = math.hypot(p1[0] - p0[0], p1[1] - p0[1]) or 1; d2 = math.hypot(p2[0] - p1[0], p2[1] - p1[1]) or 1
                r0, r2 = min(r, d0 / 2), min(r, d2 / 2)
                a_ = (p1[0] + (p0[0] - p1[0]) * r0 / d0, p1[1] + (p0[1] - p1[1]) * r0 / d0)
                b_ = (p1[0] + (p2[0] - p1[0]) * r2 / d2, p1[1] + (p2[1] - p1[1]) * r2 / d2)
                if i == 0: c.move_to(*a_)
                else: c.line_to(*a_)
                c.curve_to(a_[0] + (p1[0] - a_[0]) * 0.6, a_[1] + (p1[1] - a_[1]) * 0.6, b_[0] + (p1[0] - b_[0]) * 0.6, b_[1] + (p1[1] - b_[1]) * 0.6, *b_)
            c.close_path()
        else:
            s._trace(pts)
            if close: c.close_path()
        s._paint(fill, stroke, lw, a)

    def path(s, d, fill=None, stroke=INK, lw=None, a=1.0):
        s.c.new_path(); s._trace(d); s._paint(fill, stroke, lw, a)

    def line(s, d, col=INK, w=None, a=1.0, dash=None, cap="round"):
        """Stroke only: d = path string or list of points."""
        c = s.c
        c.new_path(); s._trace(d)
        if dash: c.set_dash(dash[0], dash[1] if len(dash) > 1 else 0)
        if cap != "round": c.set_line_cap(cairo.LINE_CAP_BUTT)
        c.set_source_rgba(*rgba(col, a)); c.set_line_width(s.lw if w is None else w); c.stroke()
        if dash: c.set_dash([])
        if cap != "round": c.set_line_cap(cairo.LINE_CAP_ROUND)

    def limb(s, d, col, w, lw=None, a=1.0):
        """Thick rounded stroke with an ink outline (arms, tubes, pipes, vessels)."""
        lw = s.lw if lw is None else lw
        s.line(d, INK, w + 2 * lw, a); s.line(d, col, w, a)

    def glow(s, x, y, r, col, a=0.5, r0=0.0):
        g = cairo.RadialGradient(x, y, r0, x, y, max(r, 0.02))
        g.add_color_stop_rgba(0, *rgba(col, a)); g.add_color_stop_rgba(1, *rgba(col, 0))
        s.c.new_path(); s.c.arc(x, y, max(r, 0.02), 0, TAU); s.c.set_source(g); s.c.fill()

    def rings(s, x, y, r, col, a=0.07, n=3):
        """Flat concentric glow rings (the Style F light look)."""
        for i in range(n):
            s.circle(x, y, r * (1 - i / (n + 0.6)), col, None, a=a)

    def lgrad(s, x0, y0, x1, y1, *stops):
        g = cairo.LinearGradient(x0, y0, x1, y1)
        for i, st in enumerate(stops):
            off, col = st if isinstance(st, (tuple, list)) and len(st) == 2 and not isinstance(st[0], str) else (i / max(1, len(stops) - 1), st)
            g.add_color_stop_rgba(off, *rgba(col))
        return g

    def rgrad(s, x, y, r, *stops):
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        for i, col in enumerate(stops):
            g.add_color_stop_rgba(i / max(1, len(stops) - 1), *rgba(col))
        return g

    def fill_all(s, fill):
        c = s.c
        c.save(); c.set_matrix(s.base)
        if isinstance(fill, cairo.Pattern): c.set_source(fill)
        else: c.set_source_rgba(*rgba(fill))
        c.paint(); c.restore()

    # -- text
    def font(s, name="Lilita One", size=100, bold=False):
        s.c.select_font_face(name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
        s.c.set_font_size(size)

    def text_w(s, txt, size, font="Lilita One", bold=False):
        s.font(font, size, bold)
        return s.c.text_extents(txt)[4]

    def text(s, txt, x, y, size, fill="#FFFFFF", font="Lilita One", stroke=INK, sw=None, anchor="m", a=1.0, depth=0.0, bold=False, rot=0.0, sc=1.0):
        """Text centred vertically on y (cap height). anchor m|l|r. sw = outline width, depth = extra 'sticker' drop of the outline."""
        c = s.c
        s.font(font, size, bold)
        adv = c.text_extents(txt)[4]
        ox = -adv / 2 if anchor == "m" else (0 if anchor == "l" else -adv)
        oy = size * (0.36 if font == "Lilita One" else 0.35)
        c.save(); c.translate(x, y)
        if rot: c.rotate(rot)
        if sc != 1.0: c.scale(max(sc, 1e-3), max(sc, 1e-3))
        if stroke is not None:
            sw = size * 0.16 if sw is None else sw
            c.set_source_rgba(*rgba(stroke, a)); c.set_line_width(sw)
            if depth:
                c.new_path(); c.move_to(ox, oy + depth); c.text_path(txt); c.stroke_preserve(); c.fill()
            c.new_path(); c.move_to(ox, oy); c.text_path(txt); c.stroke()
        c.new_path(); c.move_to(ox, oy); c.text_path(txt)
        c.set_source_rgba(*rgba(fill, a)); c.fill()
        c.restore()
        return adv * sc


# ------------------------------------------------------------------ camera helpers (functions of the shot context)


def still(x=W / 2, y=H / 2, z=1.0, drift=1.0):
    def cam(c):
        return (x + 5 * drift * wig(c.gt, 0.11, 1), y + 5 * drift * wig(c.gt, 0.09, 2), z * (1 + 0.012 * drift * c.u), 0.0)
    return cam


def push(z0=1.0, z1=1.1, focus=(W / 2, H / 2), focus1=None, ease=ease_io, drift=1.0):
    """Eased zoom from z0 to z1 towards focus (optionally travelling to focus1)."""
    f1 = focus1 or focus

    def cam(c):
        k = ease(c.u)
        z = z0 + (z1 - z0) * k
        x = lerp(focus[0], f1[0], k); y = lerp(focus[1], f1[1], k)
        # keep the frame inside the design space when zoomed out
        return (x + 4 * drift * wig(c.gt, 0.11, 1), y + 4 * drift * wig(c.gt, 0.09, 2), z, 0.0)
    return cam


def look_at(x, y, z, sy=1250, sx=W / 2):
    """Camera (cx, cy, z) that puts the design point x, y at screen position sx, sy (default: lower-middle, under the captions)."""
    return (x - (sx - W / 2) / z, y - (sy - H / 2) / z, z)


def camkf(keys, ease=ease_io):
    """Keyframed camera: [(u, (x, y, z)), ...] with u = 0..1 of the shot."""
    def cam(c):
        x, y, z = kf(c.u, keys, ease)
        return (x, y, z, 0.0)
    return cam


# ------------------------------------------------------------------ shot context + video


class Ctx:
    __slots__ = ("V", "sh", "t", "T", "u", "gt", "env")

    def __init__(s, V, sh, gt):
        s.V, s.sh, s.gt = V, sh, gt
        s.t = gt - sh["start"]; s.T = sh["dur"]; s.u = clamp(s.t / s.T) if s.T > 0 else 0
        s.env = V.env(gt)

    def w(s, word, n=0, line=None):
        """Shot-local time when `word` (n-th match) starts in this shot's line."""
        return s.V.word_t(line or s.sh["line"], word, n) - s.sh["start"]

    def since(s, word, n=0, line=None):
        return s.t - s.w(word, n, line)

    def on(s, word, d=0.35, n=0):
        """0..1 eased progress starting when the word is spoken."""
        return ease_out(seg(s.t, s.w(word, n), d))


class Video:
    def __init__(s, ep, title=None, keys=(), gap=0.22, lead=0.12, music="curious", cap_y=0.40, title_out=None, end_dur=2.6, sid=None):
        s.ep = Path(ep)
        s.T = {t["id"]: t for t in json.loads((s.ep / "timing.json").read_text())}
        s.title, s.keys, s.gap, s.lead, s.music0, s.cap_y = title, {k.lower() for k in keys}, gap, lead, music, cap_y
        s.title_out, s.end_dur = title_out, end_dur
        s.sid = sid or s.ep.name[:5]
        s.decl, s.shots, s.pause = [], [], {}
        s.voice0, s.duration, s._env, s._words = {}, 0.0, None, None
        s.surf = None

    # ---- declaring shots
    def shot(s, line, fn, part=(0, 1), cam=None, sfx=(), music=None, tr="punch", cap=True, cap_y=None, name=None):
        s.decl.append(dict(line=line, fn=fn, part=part, cam=cam or still(), sfx=list(sfx), music=music, tr=tr, cap=cap, cap_y=cap_y, name=name))

    def _conv(s, L, p, full, v0):
        if isinstance(p, str):
            n = 0
            if "#" in p: p, n = p.split("#"); n = int(n)
            ws = [w for w in L["words"] if _norm(w["w"]) == _norm(p)]
            if not ws: raise KeyError(f"word {p!r} not in line {L['id']}: {L['text']}")
            return clamp(v0 + ws[n]["s"] - 0.07, 0, full)
        return full * p

    def build(s, end=True):
        t, out, k = 0.0, [], 0
        order = []
        for d in s.decl:
            if d["line"] not in order: order.append(d["line"])
        for li, lid in enumerate(order):
            L = s.T[lid]
            gap = s.gap + (0.18 if L["text"].rstrip().endswith(("?", "...")) else 0) + s.pause.get(lid, 0.0)
            v0 = s.lead if li == 0 else 0.05          # voice offset inside the line window
            full = v0 + L["dur"] + gap
            s.voice0[lid] = t + v0
            for d in [d for d in s.decl if d["line"] == lid]:
                p0, p1 = d["part"]
                a, b = s._conv(L, p0, full, v0), s._conv(L, p1, full, v0)
                out.append(dict(d, id=f"{s.sid}_{k:02d}", start=round(t + a, 4), dur=round(b - a, 4), kind="3d", line_start=round(t + v0 - 0.05, 4)))
                k += 1
            t += full
        if end and "O1" in s.T:
            o = s.T["O1"]
            s.voice0["O1"] = t + 0.17
            out.append(dict(id=f"{s.sid}_END", line="O1", fn=end_card, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4), (1.28, "ding", 0.42)],
                            music=None, tr="cut", cap=False, cap_y=None, name="end", start=round(t, 4), dur=round(max(s.end_dur, o["dur"] + 0.75), 4), kind="end",
                            line_start=round(t + 0.12, 4)))
            t += out[-1]["dur"]
        # snap shot boundaries to frames
        for sh in out:
            a = round(sh["start"] * FPS) / FPS; b = round((sh["start"] + sh["dur"]) * FPS) / FPS
            sh["start"], sh["dur"] = a, b - a
        s.shots, s.duration = out, round(t * FPS) / FPS
        s.nframes = int(round(s.duration * FPS))
        s._words = None
        return s

    # ---- timing helpers
    def word_t(s, line, word, n=0):
        ws = [w for w in s.T[line]["words"] if _norm(w["w"]) == _norm(word)]
        if not ws: raise KeyError(f"word {word!r} not in {line}")
        return s.voice0[line] + ws[n]["s"]

    def words(s):
        if s._words is None:
            s._words = []
            for sh in s.shots:
                if not sh["cap"]: continue
                lid = sh["line"]
                if any(w["line"] == lid for w in s._words): continue
                for w in s.T[lid]["words"]:
                    s._words.append(dict(w=w["w"], s=s.voice0[lid] + w["s"], e=s.voice0[lid] + w["e"], line=lid))
            s._chunks = caption_chunks(s._words)
        return s._words

    def plan(s):
        """Plan in the format lib/audio.build_mix expects."""
        shots, mood = [], s.music0
        for sh in s.shots:
            sf_ = []
            for e in sh["sfx"]:
                off, nm, g = e if len(e) == 3 else (e[0], e[1], 0.4)
                if isinstance(off, tuple):      # (word, delta seconds)
                    off = s.word_t(sh["line"], *off[0].split("#")[:1], int(off[0].split("#")[1]) if "#" in off[0] else 0) - sh["start"] + off[1]
                elif isinstance(off, str):
                    wd, n = (off.split("#") + ["0"])[:2]
                    off = s.word_t(sh["line"], wd, int(n)) - sh["start"]
                sf_.append([clamp(off / sh["dur"], 0, 1) if sh["dur"] > 0 else 0, nm, g])
            if sh["music"]: mood = sh["music"]
            shots.append(dict(id=sh["id"], kind=sh["kind"], start=sh["start"], dur=sh["dur"], line=sh["line"], line_start=sh["line_start"], sfx=sf_,
                              music=mood if sh is s.shots[0] or sh["music"] else None))
        return dict(fps=FPS, resolution=[W, H], style="F", episode=s.sid, duration=s.duration, shots=shots)

    def env(s, gt):
        if s._env is None:
            return 0.0
        return s._env(gt)

    def load_env(s):
        import audio
        s._env = audio.voice_env(s.ep, s.plan())

    # ---- drawing one frame
    def _draw_shot(s, g, sh, gt):
        c = Ctx(s, sh, gt)
        cx, cy, z, rot = sh["cam"](c)
        if sh["tr"] == "punch":
            z *= 1 + 0.07 * (1 - ease_out(c.t / 0.22))
        elif sh["tr"] == "drop":
            cy -= 60 * (1 - back_out(c.t / 0.3))
        g.set_cam(cx, cy, z, rot)
        sh["fn"](g, c)
        g.c.set_matrix(g.base)
        return c

    def frame(s, i, g=None):
        gt = i / FPS
        if g is None:
            if s.surf is None:
                s.surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); s.g = G(s.surf)
            g = s.g
        k = max(j for j, sh in enumerate(s.shots) if sh["start"] <= gt + 1e-6)
        sh = s.shots[k]
        c = g.c
        c.set_matrix(g.base); c.reset_clip()
        c.set_source_rgba(*rgba(INK)); c.paint()
        tr = sh["tr"]
        lt = gt - sh["start"]
        if isinstance(tr, tuple) and tr[0] == "iris" and k > 0 and lt < tr[2]:
            # previous shot keeps playing underneath; the new one opens in a growing circle
            s._draw_shot(g, s.shots[k - 1], gt)
            kk = ease_io(lt / tr[2])
            r = 30 + kk * 2300
            c.save(); c.new_path(); c.arc(tr[1][0], tr[1][1], r, 0, TAU); c.clip()
            c.set_source_rgba(*rgba(INK)); c.paint()
            s._draw_shot(g, sh, gt)
            c.restore()
            g.circle(tr[1][0], tr[1][1], r, None, INK, lw=14)
            g.circle(tr[1][0], tr[1][1], r + 9, None, PAL["yellow"], lw=8, a=1 - kk)
        else:
            s._draw_shot(g, sh, gt)
        if tr == "flash" and lt < 0.14:
            c.set_source_rgba(1, 1, 1, 0.42 * (1 - lt / 0.14)); c.paint()
        if sh["kind"] != "end":
            vignette(g)
            if sh["cap"]:
                s.words()
                draw_caption(g, s._chunks, gt, s.keys, (sh["cap_y"] or s.cap_y) * H)
            if s.title:
                t_out = s.title_out if s.title_out is not None else s.shots[1]["start"] if len(s.shots) > 1 else 2.5
                draw_title(g, s.title, gt, t_out)
        return bytes(s.surf.get_data())

    # ---- outputs
    def sheet(s, out, times=None, cols=6, scale=0.25, per_shot=2):
        """Contact sheet (small) of frames: by default `per_shot` frames per shot."""
        from PIL import Image, ImageDraw, ImageFont
        if times is None:
            times = []
            for sh in s.shots:
                for j in range(per_shot):
                    times.append(sh["start"] + sh["dur"] * ((j + 0.5) / per_shot if per_shot > 1 else 0.5))
        idx = [min(s.nframes - 1, int(t * FPS)) for t in times]
        frames = _pool_frames(s, idx)
        tw, th = int(W * scale), int(H * scale)
        rows = math.ceil(len(idx) / cols)
        im = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
        dr = ImageDraw.Draw(im)
        fnt = ImageFont.truetype(str(ROOT / "library/fonts/Poppins-Bold.ttf"), max(12, int(th * 0.045)))
        for n, (i, raw) in enumerate(zip(idx, frames)):
            f = Image.frombuffer("RGBA", (W, H), raw, "raw", "BGRA", 0, 1).convert("RGB").resize((tw, th), Image.LANCZOS)
            x, y = (n % cols) * tw, (n // cols) * th
            im.paste(f, (x, y))
            dr.rectangle([x, y, x + tw - 1, y + th - 1], outline=(0, 0, 0))
            dr.text((x + 6, y + th - fnt.size - 8), f"{i / FPS:.2f}s", font=fnt, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=88)
        return out

    def still(s, t, out, scale=1.0):
        from PIL import Image
        raw = s.frame(min(s.nframes - 1, int(t * FPS)))
        im = Image.frombuffer("RGBA", (W, H), raw, "raw", "BGRA", 0, 1).convert("RGB")
        if scale != 1.0: im = im.resize((int(W * scale), int(H * scale)), Image.LANCZOS)
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        im.save(out, quality=93)
        return out

    def mix(s, wav=None):
        import audio
        try:
            import sfxgen  # registers in-house synthesised effects with lib/audio
        except ImportError:
            pass
        wav = wav or str(s.ep / "audio/mix.wav")
        Path(wav).parent.mkdir(parents=True, exist_ok=True)
        audio.build_mix(s.ep, s.plan(), wav)
        return wav

    def render(s, out, workers=4, crf=15, preset="medium", audio=True, a=None, b=None):
        out = Path(out); out.parent.mkdir(parents=True, exist_ok=True)
        wav = s.mix() if audio else None
        s.load_env()
        a = 0 if a is None else int(a * FPS); b = s.nframes if b is None else int(b * FPS)
        tmp = out.with_suffix(".video.mp4")
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
               "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p", "-c:v", "libx264", "-preset", preset, "-crf", str(crf),
               "-g", str(FPS), "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-movflags", "+faststart", str(tmp)]
        ff = subprocess.Popen(cmd, stdin=subprocess.PIPE)
        import multiprocessing as mp
        global _V
        _V = s
        with mp.get_context("fork").Pool(workers) as pool:
            for n, raw in enumerate(pool.imap(_frame, range(a, b), chunksize=4)):
                ff.stdin.write(raw)
                if n % 150 == 0: print(f"  frame {a + n}/{b}", flush=True)
        ff.stdin.close()
        if ff.wait() != 0: raise RuntimeError("ffmpeg video encode failed")
        if wav:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-ss", str(a / FPS), "-t", str((b - a) / FPS), "-i", wav, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                            "-movflags", "+faststart", str(out)], check=True)
            tmp.unlink()
        else:
            tmp.replace(out)
        print("rendered", out, f"{(b - a) / FPS:.2f}s")
        return out


_V = None


def _frame(i):
    return _V.frame(i)


def _pool_frames(V, idx):
    import multiprocessing as mp
    global _V
    _V = V
    if V._env is None:
        try: V.load_env()
        except Exception: pass
    with mp.get_context("fork").Pool(4) as pool:
        return pool.map(_frame, idx)


def _norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


# ------------------------------------------------------------------ captions, title, vignette


def caption_chunks(words, max_chars=13, max_words=3):
    """Group words into 1-3 word chunks that fit one line of big type; break at punctuation and pauses."""
    chunks, cur = [], []
    for i, w in enumerate(words):
        cur.append(w)
        nxt = words[i + 1] if i + 1 < len(words) else None
        txt = " ".join(_cap(x["w"]) for x in cur)
        brk = nxt is None or w["w"].rstrip().endswith((".", ",", "?", "!", ":", ";", "...")) or nxt["line"] != w["line"] or nxt["s"] - w["e"] > 0.3
        if not brk:
            brk = len(cur) >= max_words or len(txt) + 1 + len(_cap(nxt["w"])) > max_chars
        if brk:
            chunks.append(cur); cur = []
    out = []
    for i, c in enumerate(chunks):
        end = c[-1]["e"] + 0.35
        if i + 1 < len(chunks): end = min(end, chunks[i + 1][0]["s"] - 0.02)
        out.append(dict(words=c, s=c[0]["s"] - 0.04, e=max(end, c[-1]["e"])))
    return out


def _cap(w):
    w = w.strip().upper().replace("...", "").rstrip(".,;:")
    return w.replace("’", "'")


def draw_caption(g, chunks, t, keys, y, size=118):
    ch = next((c for c in chunks if c["s"] <= t < c["e"]), None)
    if ch is None:
        return
    words = [_cap(w["w"]) for w in ch["words"]]
    g.font("Lilita One", size)
    sp = size * 0.26
    ws = [g.c.text_extents(w)[4] for w in words]
    tot = sum(ws) + sp * (len(ws) - 1)
    k = min(1.0, W * 0.88 / tot)
    x = W / 2 - tot * k / 2
    with g.screen():
        for w, ww, src in zip(words, ws, ch["words"]):
            dt = t - (src["s"] - 0.04)
            if dt >= 0:
                key = _norm(src["w"]) in keys or any(ch_.isdigit() for ch_ in w)
                sc = k * (0.72 + 0.28 * back_out(dt / 0.16, 2.6))
                g.text(w, x + ww * k / 2, y - 14 * (1 - ease_out(dt / 0.16)), size, PAL["yellow"] if key else "#FFFFFF", sw=size * 0.20, depth=size * 0.075, sc=sc)
            x += (ww + sp) * k


def draw_title(g, lines, t, t_out, y=0.215):
    """Hook title block (top): cream first line(s), big yellow last line. Fully visible on frame 0."""
    if t > t_out + 0.3:
        return
    k_out = ease_in(seg(t, t_out, 0.28))
    with g.screen():
        sizes = []
        for i, ln in enumerate(lines):
            last = i == len(lines) - 1
            base = 150 if last else 104
            w = g.text_w(ln, base)
            sizes.append(base * min(1.0, W * 0.88 / w))
        yy = H * y
        for i, ln in enumerate(lines):
            last = i == len(lines) - 1
            sz = sizes[i]
            kin = 1 + 0.10 * (1 - ease_out(seg(t, 0.03 * i, 0.3)))
            sc = kin * (1 - 0.5 * k_out)
            with g.group(1 - k_out):
                g.text(ln, W / 2, yy + sz * 0.42 - 90 * k_out, sz, PAL["yellow"] if last else PAL["cream"], sw=sz * 0.2, depth=sz * 0.08,
                       sc=sc, rot=math.radians(-1.2 if last else 0.6) * (1 - ease_out(seg(t, 0, 0.5))))
            yy += sz * 1.02


_VIG = {}


def vignette(g, a=0.34):
    c = g.c
    c.save(); c.set_matrix(g.base)
    p = _VIG.get(a)
    if p is None:
        p = cairo.RadialGradient(W / 2, H * 0.52, H * 0.30, W / 2, H * 0.52, H * 0.78)
        p.add_color_stop_rgba(0, 0, 0, 0, 0); p.add_color_stop_rgba(1, 0.02, 0.03, 0.06, a)
        _VIG[a] = p
    c.set_source(p); c.paint(); c.restore()


# ------------------------------------------------------------------ brand: background + Wy end card


def brand_bg(g, t, rays=True):
    g.fill_all(g.rgrad(W / 2, H * 0.44, H * 0.72, "#1590A0", "#0F6B78", "#0B3F4C"))
    if rays:
        c = g.c
        for i in range(16):
            a0 = i * TAU / 16 + t * 0.12
            g.poly([(W / 2, H * 0.44), (W / 2 + 2600 * math.cos(a0), H * 0.44 + 2600 * math.sin(a0)),
                    (W / 2 + 2600 * math.cos(a0 + 0.12), H * 0.44 + 2600 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.07)


def check_badge(g, x, y, r, k=1.0):
    """Yellow circle with the ink tick (logo badge)."""
    if k <= 0: return
    with g.at(x, y, 0, k):
        g.circle(0, 0, r, PAL["yellow"], INK, lw=r * 0.2)
        g.line([(-0.45 * r, 0.02 * r), (-0.10 * r, 0.36 * r), (0.50 * r, -0.34 * r)], INK, r * 0.26)


def end_card(g, c):
    """Last seconds of every Short: Wy with the tick badge + 'Follow for more true whys'."""
    from flat_cast import wy_bust
    t = c.t
    brand_bg(g, c.gt)
    hy = H + 30 - 235 * 2.45                     # Wy's head centre on the card
    g.c.save(); g.c.set_dash([2, 46], t * 30)
    g.circle(W / 2, hy, 462, None, PAL["yellow"], lw=16, a=0.9)
    g.c.restore()
    k = back_out(seg(t, 0.0, 0.45), 1.6)
    g.text("TrueWhys", W / 2, H * 0.115, 176, PAL["cream"], sw=30, depth=10, sc=0.5 + 0.5 * k)
    for i, (txt, col, sz) in enumerate((("FOLLOW FOR MORE", PAL["cream"], 112), ("TRUE WHYS", PAL["yellow"], 150))):
        kk = pop(t, 0.18 + i * 0.14, 0.36)
        if kk > 0:
            g.text(txt, W / 2, H * (0.222 + i * 0.076), sz, col, sw=sz * 0.2, depth=sz * 0.075, sc=kk)
    kw = back_out(seg(t, 0.05, 0.5), 1.5)
    sq = 1 + 0.10 * math.sin(seg(t, 0.05, 0.6) * math.pi) * (1 - seg(t, 0.05, 0.6))
    wy_bust(g, c.gt, W / 2, H + 30 + (1 - kw) * 1000, 2.45, talk=c.env, sq=sq)
    bx, by = W / 2 + 335, hy + 286
    check_badge(g, bx, by, 138, pop(t, 1.26, 0.4, 2.4))
    kb = seg(t, 1.26, 0.5)
    if 0 < kb < 1:
        for i in range(8):
            a0 = i * TAU / 8
            r0, r1 = 170 + 90 * ease_out(kb), 210 + 120 * ease_out(kb)
            g.line([(bx + r0 * math.cos(a0), by + r0 * math.sin(a0)), (bx + r1 * math.cos(a0), by + r1 * math.sin(a0))],
                   PAL["cream"], 12, a=1 - kb)


# ------------------------------------------------------------------ QA measurement


def measure(mp4):
    """Duration, size, fps, loudness (LUFS) and peak of a finished file: numbers for qa.md."""
    import soundfile as sf, pyloudnorm as pyln
    pr = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,r_frame_rate,nb_frames,codec_name:format=duration,size",
                         "-of", "json", str(mp4)], capture_output=True, text=True)
    info = json.loads(pr.stdout)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(mp4), "-ac", "2", "-ar", "44100", "-f", "f32le", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2)
    lufs = pyln.Meter(44100).integrated_loudness(a) if len(a) else float("nan")
    peak = 20 * math.log10(max(1e-9, float(np.abs(a).max()))) if len(a) else float("nan")
    st = info["streams"][0]
    res = dict(w=st["width"], h=st["height"], fps=st["r_frame_rate"], frames=int(st.get("nb_frames", 0)), dur=round(float(info["format"]["duration"]), 2),
               mb=round(int(info["format"]["size"]) / 1e6, 1), lufs=round(lufs, 1), peak_db=round(peak, 1))
    print(res)
    return res
