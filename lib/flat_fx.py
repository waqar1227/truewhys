"""Style F effects and small reusable drawings: wall patterns, lamps, snow, sparkles, bolts, arrows, steam, bursts, flames.
All are pure functions of time (seeded), so frames can render in any order."""
import math
from flat2d import G, INK, PAL, TAU, W, H, rgba, mix, shade, clamp, lerp, seg, ease_out, ease_in, ease_io, back_out, pop, wig, rnd


def tiles(g, x0, y0, x1, y1, w=216, h=60, gap=16, col="#FFFFFF", a=0.05, r=14, lw=3, stagger=True):
    """Rounded wall bricks/tiles drawn as faint outlines (the A-008 wall look)."""
    row, y = 0, y0
    while y < y1:
        x = x0 - (w + gap) / 2 if (stagger and row % 2) else x0
        while x < x1:
            g.rect(x, y, w, h, None, col, lw=lw, r=r, a=a)
            x += w + gap
        y += h + gap; row += 1


def room(g, wall=("#0A2F3B", "#0F4553"), floor=("#5B3B2E", "#33211C"), fy=1480, pattern=True, tile=(216, 60)):
    g.fill_all(g.lgrad(0, 0, 0, H, wall[0], wall[1]))
    if pattern:
        with g.layer(0.9):
            tiles(g, -500, -300, W + 500, fy + 60, tile[0], tile[1])
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 500, floor[0], floor[1]), None)
    g.line([(-600, fy), (W + 600, fy)], INK, 8)


def lamp(g, x, y, t=0.0, col="#FF6B5B", light="#FFC93C", r=420, cord_top=-400, on=1.0, sc=1.0):
    """Pendant lamp: cord, dome shade, warm glow rings."""
    fl = 1 + 0.03 * wig(t, 1.3, x)
    g.rings(x, y + 60 * sc, r * fl, light, a=0.055 * on, n=4)
    g.line([(x, cord_top), (x, y - 50 * sc)], INK, 7)
    g.path(f"M{x - 78 * sc} {y} C{x - 78 * sc} {y - 76 * sc} {x + 78 * sc} {y - 76 * sc} {x + 78 * sc} {y} Z", col)
    g.ellipse(x, y + 4 * sc, 30 * sc, 15 * sc, mix(light, "#FFFFFF", 0.4 * on))
    g.glow(x, y + 30 * sc, 150 * sc, light, 0.35 * on)


def flake(g, x, y, r, col="#EAF9FF", rot=0.0, lw=5.0, a=1.0):
    with g.at(x, y, rot):
        for i in range(3):
            a0 = i * TAU / 6
            dx, dy = r * math.cos(a0), r * math.sin(a0)
            g.line([(-dx, -dy), (dx, dy)], col, lw, a=a)
            for sgn in (-1, 1):
                bx, by = sgn * dx * 0.62, sgn * dy * 0.62
                for da in (0.7, -0.7):
                    g.line([(bx, by), (bx + sgn * r * 0.3 * math.cos(a0 + da), by + sgn * r * 0.3 * math.sin(a0 + da))], col, lw * 0.8, a=a)


def snow(g, t, box, n=24, seed=1, col="#EAF9FF", size=(7, 16), speed=70.0, a=0.9, t0=0.0):
    """Drifting snowflakes inside box (x0, y0, x1, y1); they appear from t0."""
    R = rnd(seed)
    x0, y0, x1, y1 = box
    for i in range(n):
        px, ph, sz, sp, rs = R.random(), R.random(), R.uniform(*size), R.uniform(0.6, 1.3), R.uniform(-1.5, 1.5)
        tt = t - t0 - i * 0.02
        if tt < 0: continue
        u = (ph + tt * sp * speed / max(1, (y1 - y0))) % 1.0
        x = x0 + px * (x1 - x0) + 18 * math.sin(tt * 1.7 + i)
        y = y0 + u * (y1 - y0)
        fade = min(1.0, u * 6, (1 - u) * 6, tt * 4)
        flake(g, x, y, sz, col, rs * tt, lw=max(2.5, sz * 0.3), a=a * fade)


def sparkle(g, x, y, r, col="#FFF4E0", rot=0.0, a=1.0, stroke=None):
    if r <= 0.5: return
    with g.at(x, y, rot):
        k = 0.28
        g.path(f"M0 {-r} Q{r * k} {-r * k} {r} 0 Q{r * k} {r * k} 0 {r} Q{-r * k} {r * k} {-r} 0 Q{-r * k} {-r * k} 0 {-r} Z", col, stroke, lw=3.5, a=a)


def sparkles(g, t, pts, seed=3, col="#FFF4E0", r=26, period=0.9, a=1.0, t0=0.0):
    """Twinkling 4-point stars at the given points (staggered)."""
    R = rnd(seed)
    for i, (x, y) in enumerate(pts):
        ph = R.random()
        tt = t - t0
        if tt < 0: continue
        u = ((tt / period) + ph) % 1.0
        k = math.sin(u * math.pi)
        sparkle(g, x, y, r * k * R.uniform(0.6, 1.0), col, u * 1.2, a=a)


def bolt(g, x, y, s=1.0, rot=0.0, col="#FFC93C", a=1.0, lw=None):
    with g.at(x, y, rot, s):
        g.path("M-10 -46 L22 -46 L6 -8 L28 -8 L-18 50 L-4 6 L-26 6 Z", col, INK, lw=lw or 5.5, a=a)


def pain_marks(g, x, y, r, t, n=5, col="#FF6B5B", a0=-2.4, a1=-0.74, sc=1.0):
    """Short zigzag marks radiating around a point, pulsing (cartoon pain)."""
    for i in range(n):
        ang = a0 + (a1 - a0) * i / max(1, n - 1)
        k = 0.6 + 0.4 * math.sin(TAU * 3.2 * t + i * 1.3)
        rr = r * (1 + 0.10 * k)
        with g.at(x + rr * math.cos(ang), y + rr * math.sin(ang), ang + TAU / 4, sc * (0.8 + 0.3 * k)):
            g.limb([(0, 18), (-11, 4), (11, -8), (0, -24)], col, 9, lw=4.5)


def arrow(g, x0, y0, x1, y1, col="#FFC93C", w=22, head=2.3, k=1.0, lw=None, a=1.0):
    """Chunky outlined arrow from (x0, y0) growing to (x1, y1) with k = 0..1."""
    if k <= 0.02: return
    x1, y1 = x0 + (x1 - x0) * k, y0 + (y1 - y0) * k
    d = math.hypot(x1 - x0, y1 - y0)
    if d < 2: return
    ang = math.atan2(y1 - y0, x1 - x0)
    hl = min(d * 0.6, w * head * 0.9); hw = w * head / 2
    with g.at(x0, y0, ang):
        g.poly([(0, -w / 2), (d - hl, -w / 2), (d - hl, -hw), (d, 0), (d - hl, hw), (d - hl, w / 2), (0, w / 2)], col, INK, lw=lw or 5.5, a=a, r=4)


def steam(g, t, x, y, n=3, h=150, col="#FFFFFF", a=0.5, w=11, spread=34):
    for i in range(n):
        u = ((t * 0.55) + i / n) % 1.0
        xx = x + (i - (n - 1) / 2) * spread
        pts = [(xx + 13 * math.sin(v * 5 + t * 2.2 + i), y - (u * h) - v * 62) for v in (0, 0.25, 0.5, 0.75, 1.0)]
        g.line(pts, col, w * (1 - 0.4 * u), a=a * math.sin(u * math.pi))


def puff(g, x, y, r, col="#FFFFFF", a=0.8, stroke=None):
    for dx, dy, rr in ((-0.55, 0.1, 0.62), (0.0, -0.22, 0.8), (0.58, 0.08, 0.6), (0.05, 0.3, 0.6)):
        g.circle(x + dx * r, y + dy * r, rr * r, col, stroke, a=a)


def burst(g, x, y, r0, r1, n=10, col="#FFF4E0", w=10, k=1.0, a=1.0, rot=0.0):
    """Radial lines flying out: k 0..1 (fades at the end)."""
    if k <= 0 or k >= 1: return
    e = ease_out(k)
    for i in range(n):
        ang = rot + i * TAU / n
        ra, rb = r0 + (r1 - r0) * e * 0.75, r0 + (r1 - r0) * e
        g.line([(x + ra * math.cos(ang), y + ra * math.sin(ang)), (x + rb * math.cos(ang), y + rb * math.sin(ang))], col, w * (1 - 0.5 * k), a=a * (1 - k) ** 0.7)


def qmark(g, x, y, size=120, col="#FFC93C", rot=0.0, k=1.0, txt="?"):
    if k <= 0.01: return
    g.text(txt, x, y, size, col, sw=size * 0.2, depth=size * 0.06, rot=rot, sc=k)


def ring_wave(g, x, y, r0, r1, k, col="#BDEBFF", w=10, a=0.9):
    """Expanding ring that fades (impact, cold wave, pulse)."""
    if k <= 0 or k >= 1: return
    g.circle(x, y, r0 + (r1 - r0) * ease_out(k), None, col, lw=w * (1 - 0.6 * k), a=a * (1 - k))


def flame(g, x, y, w, h, t, seed=0.0, cols=("#FF7A1A", "#FFC233", "#FFF0A8")):
    """Layered flat flame, flickering."""
    for i, c in enumerate(cols):
        k = 1 - i * 0.3
        f1 = 1 + 0.10 * wig(t, 2.3 + i * 0.7, seed + i); f2 = 0.12 * wig(t, 1.7 + i * 0.5, seed + 3 + i)
        ww, hh = w * k, h * k * f1
        g.path(f"M{x - ww / 2} {y} C{x - ww * 0.62} {y - hh * 0.42} {x - ww * 0.18 + f2 * ww} {y - hh * 0.62} {x + f2 * ww * 1.6} {y - hh} "
               f"C{x + ww * 0.2 + f2 * ww} {y - hh * 0.6} {x + ww * 0.62} {y - hh * 0.4} {x + ww / 2} {y} Z", c, INK if i == 0 else None)


def no_sign(g, x, y, r, k=1.0, col="#FF5B4B"):
    if k <= 0.01: return
    with g.at(x, y, 0, k):
        g.circle(0, 0, r, None, INK, lw=r * 0.30)
        g.circle(0, 0, r, None, col, lw=r * 0.18)
        g.line([(-r * 0.68, -r * 0.68), (r * 0.68, r * 0.68)], INK, r * 0.30)
        g.line([(-r * 0.68, -r * 0.68), (r * 0.68, r * 0.68)], col, r * 0.18)


def gauge(g, x, y, r, v, k=1.0):
    """Pressure dial: v 0..1 swings the needle from green to red."""
    if k <= 0.01: return
    with g.at(x, y, 0, k):
        g.circle(0, 0, r, "#FFF4E0", INK, lw=9)
        for i, c in enumerate(("#5ED3B5", "#FFC93C", "#FF5B4B")):
            a0 = math.pi + i * math.pi / 3
            g.c.new_path(); g.c.arc(0, 0, r * 0.74, a0 + 0.04, a0 + math.pi / 3 - 0.04)
            g.c.set_source_rgba(*rgba(c)); g.c.set_line_width(r * 0.22); g.c.set_line_cap(0); g.c.stroke(); g.c.set_line_cap(1)
        ang = math.pi + clamp(v, 0, 1.05) * math.pi
        g.line([(0, 0), (r * 0.66 * math.cos(ang), r * 0.66 * math.sin(ang))], INK, r * 0.12)
        g.circle(0, 0, r * 0.14, INK, None)
        g.rect(-r * 0.42, r * 0.28, r * 0.84, r * 0.3, INK, None, r=r * 0.1)
