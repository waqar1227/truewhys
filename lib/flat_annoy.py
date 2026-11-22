"""Reusable Style F props for everyday-science scenes (B-005, 22 Nov 2026). Design units, Style F engine (lib/flat2d.py).

    from flat_annoy import toast, plate, sneaker, bow_knot, earbuds, spaghetti, curtain, mug, coffee_drop, cereal_loop, bowl_top, tumble_box
All props are drawn around (x, y) with scale s and use the brand ink outline. Listed in library/index.md.
"""
import math
from flat2d import *

CRUST, BREAD, BUTTER = "#B9773C", "#F3D08A", "#FFD84A"
PASTA = "#F2C66D"
COFFEE, COFFEE_D = "#7A4A2A", "#3E2414"


def toast(g, x, y, s=1.0, rot=0.0, butter=True, bite=False):
    """Side view slice of buttered toast (butter on the local top side). rot in radians."""
    with g.at(x, y, rot, s):
        g.rc(0, 0, 240, 44, BREAD, INK, lw=7, r=14)
        g.rc(0, 0, 240, 44, None, CRUST, lw=9, r=14)
        g.rc(0, 0, 240, 44, None, INK, lw=6, r=14)
        if butter:
            g.path("M-104 -22 Q-60 -40 -10 -30 Q40 -42 100 -24 L100 -20 L-104 -20 Z", BUTTER, INK, lw=5)
            g.rc(30, -34, 52, 14, "#FFF1A8", INK, lw=4, r=4)


def toast_top(g, x, y, s=1.0, rot=0.0, butter=True):
    """Top view of a slice (bread shape) with butter."""
    with g.at(x, y, rot, s):
        d = "M-110 120 L-110 -40 Q-140 -130 -60 -140 Q0 -170 60 -140 Q140 -130 110 -40 L110 120 Q0 132 -110 120 Z"
        g.path(d, CRUST, INK, lw=8)
        with g.at(0, 6, 0, 0.84):
            g.path(d, BREAD, None)
        if butter:
            g.path("M-60 -40 Q-10 -80 50 -50 Q80 0 40 50 Q-20 80 -60 40 Q-80 0 -60 -40 Z", BUTTER, INK, lw=5)
            g.rc(10, -10, 60, 40, "#FFF1A8", INK, lw=4, r=6)


def plate(g, x, y, w=300):
    g.ellipse(x, y, w / 2, w * 0.09, "#FFFFFF", INK, lw=7)
    g.ellipse(x, y - 4, w * 0.34, w * 0.055, "#EDEDF2", None)


def table_side(g, x, y, w=900, col="#C97B4A", leg=330):
    g.rect(x - w / 2, y, w, 36, col, INK, lw=8, r=6)
    g.rect(x - w / 2 + 30, y + 36, 34, leg, shade(col, 0.75), INK, lw=7)
    g.rect(x + w / 2 - 64, y + 36, 34, leg, shade(col, 0.75), INK, lw=7)


def ruler_v(g, x, y0, y1, txt, col=None, k=1.0):
    """Vertical height marker with arrow ends and a label."""
    if k <= 0: return
    col = col or PAL["yellow"]
    ym = lerp(y1, y0, k)
    g.line([(x, y1), (x, ym)], col, 8)
    g.line([(x - 26, y1), (x + 26, y1)], col, 8)
    g.line([(x - 26, ym), (x + 26, ym)], col, 8)
    if k > 0.6:
        g.text(txt, x + 30, (y0 + y1) / 2, 54, col, sw=10, anchor="l", sc=ease_out((k - 0.6) / 0.4))


def sneaker(g, x, y, s=1.0, col="#FF6B5B", sole="#F4F1EA", rot=0.0, flip=False):
    """Side view running shoe, toe to the right (flip: toe left). Laces drawn separately with bow_knot."""
    with g.at(x, y, rot, -s if flip else s, s):
        g.path("M-230 40 L-230 -60 Q-220 -140 -120 -150 L-40 -150 Q0 -80 80 -60 Q200 -40 240 10 L240 40 Z", col, INK, lw=9)
        g.path("M-240 40 L250 40 Q260 70 230 80 L-230 80 Q-250 70 -240 40 Z", sole, INK, lw=8)
        g.path("M-120 -150 Q-150 -190 -100 -200 L-30 -196 Q0 -180 -40 -150 Z", shade(col, 0.8), INK, lw=7)
        for i in range(4):
            g.line([(-60 + i * 36, -130 + i * 18), (-20 + i * 36, -134 + i * 18)], "#FFFFFF", 7)
        g.line([(-200, 10), (200, 20)], shade(col, 0.82), 6)


def bow_knot(g, x, y, s=1.0, loosen=0.0, swing=0.0, col="#FFFFFF", twist=False, undone=0.0):
    """Shoelace bow seen from the side/top: two loops + two free ends. loosen 0..1 widens the knot and shrinks the loops,
    swing = angle (rad) of the free ends, twist=True draws the weak (vertical, twisted) bow, undone 0..1 = laces fall apart."""
    with g.at(x, y, 0, s):
        lo = 1 - 0.7 * clamp(loosen) - 0.3 * undone
        rot = 1.25 if twist else 0.0
        with g.at(0, 0, rot):
            for side in (-1, 1):
                if undone < 0.95:
                    with g.at(side * 18 * (1 + loosen), 0, side * 0.25):
                        g.ellipse(side * 70 * lo, -10, 72 * lo + 8, 34 * lo + 6, None, INK, lw=22)
                        g.ellipse(side * 70 * lo, -10, 72 * lo + 8, 34 * lo + 6, None, col, lw=12)
            for side, ph in ((-1, 0.0), (1, 1.4)):
                a = math.pi / 2 + side * 0.35 + swing * (1 if side > 0 else -0.8)
                L = 110 + 120 * clamp(loosen) + 140 * undone
                pts = [(side * 10, 10), (side * 10 + L * 0.45 * math.cos(a) + side * 16, 10 + L * 0.5 * math.sin(a)),
                       (side * 10 + L * math.cos(a) * 0.9, 10 + L * math.sin(a))]
                g.line(pts, INK, 22); g.line(pts, col, 12)
                g.circle(pts[-1][0], pts[-1][1], 9, "#9AA3AD", INK, lw=4)
            g.rc(0, 0, 48 + 40 * loosen, 40 + 10 * loosen, col, INK, lw=7, r=16)


def earbud(g, x, y, s=1.0, rot=0.0, col="#F4F1EA"):
    with g.at(x, y, rot, s):
        g.rc(0, 34, 22, 70, col, INK, lw=6, r=11)
        g.circle(0, 0, 34, col, INK, lw=7)
        g.circle(-8, -6, 12, "#7FC8E8", INK, lw=4)


def earbuds(g, x, y, s=1.0, mess=0.0, t=0.0, col="#F4F1EA", seed=3):
    """Wired earbuds: mess 0 = neat coil, 1 = tangled mess with knots."""
    R = rnd(seed)
    pts = []
    n = 160
    for i in range(n):
        u = i / (n - 1)
        a = u * TAU * 2.0
        nx, ny = 150 * math.cos(a) * (0.6 + 0.4 * u), 80 * math.sin(a) * (0.6 + 0.4 * u)
        mx = 170 * math.sin(u * 11 + seed) * math.cos(u * 3) + 50 * math.sin(u * 23)
        my = 110 * math.cos(u * 9 + seed * 0.5) * math.sin(u * 4 + 1) + 40 * math.cos(u * 21)
        pts.append((x + s * lerp(nx, mx, mess), y + s * lerp(ny, my, mess)))
    g.line(pts, INK, 15 * s); g.line(pts, col, 8 * s)
    if mess > 0.5:
        for i in range(5):
            px, py = pts[20 + i * 28]
            g.circle(px, py, 16 * s * (mess - 0.5) * 2, None, "#FF6B5B", lw=5, a=0.9)
    earbud(g, pts[0][0], pts[0][1] - 30 * s, 0.9 * s, -0.4 + mess * 1.2, col)
    earbud(g, pts[-1][0] + 20 * s, pts[-1][1] - 30 * s, 0.9 * s, 0.5 - mess, col)


def tumble_box(g, x, y, r, rot, t=0.0, string_n=1.0, knot=0.0):
    """Clear cube seen from the front, rotating (rot rad) on an axle, with a coiled string inside."""
    g.line([(x - r * 1.5, y), (x + r * 1.5, y)], "#5A5A6A", 18)
    g.circle(x - r * 1.5, y, 26, "#9AA3AD", INK, lw=6); g.circle(x + r * 1.5, y, 26, "#9AA3AD", INK, lw=6)
    with g.at(x, y, rot):
        g.rc(0, 0, 2 * r, 2 * r, "#BDEBFF", INK, lw=10, r=18, a=0.55)
        g.rc(0, 0, 2 * r, 2 * r, None, INK, lw=10, r=18)
        pts = []
        n = int(40 * string_n) + 2
        for i in range(n):
            u = i / 41
            a = u * TAU * 3.0 + t * 0.8
            rr = r * (0.55 + 0.25 * math.sin(u * 9 + t))
            pts.append((rr * math.cos(a) * (1 - 0.3 * knot) + knot * 30 * math.sin(u * 40), rr * math.sin(a) + knot * 25 * math.cos(u * 33)))
        g.line(pts, INK, 14); g.line(pts, "#FF6B5B", 7)
        g.line([(-r + 20, -r + 30), (-r + 60, -r + 20)], "#FFFFFF", 8, a=0.7)


def spaghetti(g, x0, y0, x1, y1, bend=0.0, w=14, col=PASTA, twist=0.0):
    """One dry stick from (x0,y0) to (x1,y1), bent upward by `bend` (px of sag at the middle); twist draws spiral stripes."""
    n = 24
    pts = []
    for i in range(n + 1):
        u = i / n
        pts.append((lerp(x0, x1, u), lerp(y0, y1, u) - bend * 4 * u * (1 - u)))
    g.line(pts, INK, w + 9); g.line(pts, col, w)
    if twist > 0:
        for i in range(1, n, 2):
            px, py = pts[i]
            ph = math.sin(i * 0.9 + twist * TAU)
            g.line([(px - 4, py - w * 0.4 * ph), (px + 4, py + w * 0.4 * ph)], shade(col, 0.7), 4)
    return pts


def fist(g, x, y, s=1.0, rot=0.0, skin="#D8A580"):
    with g.at(x, y, rot, s):
        g.rc(0, 0, 110, 120, skin, INK, lw=8, r=46)
        for i in range(3):
            g.line([(-30 + i * 28, -40), (-30 + i * 28, -10)], shade(skin, 0.75), 5)
        g.rc(0, 90, 80, 90, shade("#3E8E5E", 1.0), INK, lw=8, r=20)


def curtain(g, x0, x1, top, bot, bulge=0.0, col="#5ED3B5", t=0.0, weights=False, stripes="#FFFFFF"):
    """Shower curtain hanging from a rod between x0..x1 (side/front view). bulge > 0 pushes the lower middle to the right (inward)."""
    n = 9
    g.line([(x0 - 40, top - 10), (x1 + 40, top - 10)], "#C9CED6", 16)
    folds = []
    for i in range(n + 1):
        u = i / n
        folds.append(lerp(x0, x1, u))
    def pos(u, v):
        bx = lerp(x0, x1, u)
        b = bulge * math.sin(math.pi * u) * (v ** 1.6) * 180 + 6 * math.sin(t * 2 + u * 8) * v
        return bx + b * 0.0, top + (bot - top) * v, b
    pts_top = [(lerp(x0, x1, i / 40), top + 10 * math.sin(i * 1.7)) for i in range(41)]
    pts_bot = []
    for i in range(41):
        u = i / 40
        b = bulge * math.sin(math.pi * u) * 70
        pts_bot.append((lerp(x0, x1, u) + 12 * math.sin(u * 30 + t), bot - b + 8 * math.sin(u * 22 + t * 1.3)))
    g.poly(pts_top + pts_bot[::-1], col, INK, lw=8)
    for i in range(1, n):
        u = i / n
        xb = lerp(x0, x1, u)
        g.line([(xb, top + 10), (xb + 12 * math.sin(u * 30 + t), bot - bulge * math.sin(math.pi * u) * 70)], shade(col, 0.82), 7)
    for i in range(0, n + 1, 2):
        xb = lerp(x0, x1, i / n)
        g.line([(xb + 18, top + 30), (xb + 18, bot - 40)], stripes, 6, a=0.35)
    for i in range(n + 1):
        g.circle(lerp(x0, x1, i / n), top - 10, 12, None, "#9AA3AD", lw=6)
    if weights:
        for i in range(n):
            px, py = pts_bot[int((i + 0.5) / n * 40)]
            g.circle(px, py - 12, 14, "#5A5A6A", INK, lw=5)


def mug(g, x, y, s=1.0, col="#FF6B5B"):
    with g.at(x, y, 0, s):
        g.path("M-90 -120 L90 -120 L80 60 Q0 80 -80 60 Z", col, INK, lw=9)
        g.path("M90 -80 Q160 -80 150 -20 Q140 30 84 30", None, INK, lw=30)
        g.path("M90 -80 Q160 -80 150 -20 Q140 30 84 30", None, col, lw=16)
        g.ellipse(0, -120, 90, 22, COFFEE, INK, lw=8)


def coffee_drop(g, x, y, r, dry=0.0, ring=0.0, even=False):
    """Top view of a spilled drop: dry 0..1 fades the middle; ring 0..1 darkens the rim (even=True: uniform stain, no ring)."""
    if even:
        g.circle(x, y, r, mix(COFFEE, "#D9B48A", 0.55 * dry), INK, lw=5, a=0.95)
        return
    mid = mix(COFFEE, "#E8D2B4", 0.75 * dry)
    g.circle(x, y, r, mid, None, a=0.95)
    g.circle(x, y, r * (1 - 0.04 * ring), None, mix(COFFEE, COFFEE_D, ring), lw=4 + 22 * ring)
    g.circle(x, y, r, None, INK, lw=4, a=0.5)
    if dry < 0.5:
        g.ellipse(x - r * 0.3, y - r * 0.35, r * 0.25, r * 0.12, "#FFFFFF", None, a=0.4 * (1 - 2 * dry))


def cereal_loop(g, x, y, r=40, rot=0.0, col="#E8A94A"):
    with g.at(x, y, rot):
        g.circle(0, 0, r, col, INK, lw=6)
        g.circle(0, 0, r * 0.38, "#FFFDF6", INK, lw=5)
        g.circle(-r * 0.3, -r * 0.5, r * 0.12, shade(col, 0.8), None)


def bowl_top(g, x, y, r, milk="#FFFDF6"):
    g.circle(x, y, r + 50, "#3E8E7A", INK, lw=10)
    g.circle(x, y, r + 30, shade("#3E8E7A", 1.15), None)
    g.circle(x, y, r, milk, INK, lw=6)
    g.circle(x - r * 0.3, y - r * 0.3, r * 0.4, "#FFFFFF", None, a=0.4)
