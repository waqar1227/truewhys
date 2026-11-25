"""Bubble-wrap origin assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-032 how failed wallpaper became bubble wrap).

    from flat_bubble import (bubble_sheet, room_1957, workshop_1957, sealer, curtain, shop_1957, wall_roll, greenhouse, trash_can,
                             computer_room, mainframe, crate, truck, road, parcel, BUB, BUB_HI)
Generic 1950s/60s rooms and machines only: no company names, logos or real products. All coordinates are design units (1080x1920)
under the shot camera. Every drawing is code-made (no downloaded art).
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd, ease_out, ease_io, TAU
from flat_fx import burst, sparkle

BUB = "#BFE9FF"           # bubble film tint
BUB_HI = "#FFFFFF"
MINT, PINK, CREAM, TEAL = "#9ED9C3", "#F4A9B8", "#FFF4E0", "#0F6B78"


# ------------------------------------------------------------------ the bubble film
def bubble_sheet(g, x, y, w, h, t, r=34, pop=None, inflate=1.0, a=0.9, col=BUB, rot=0.0, squash=None, rows=None):
    """Clear plastic film with staggered air bubbles. (x, y) = top-left, size w x h.
    pop(i, j) -> 0..1 how far bubble (row i, col j) has popped (flattened + a little burst at the moment it pops).
    inflate: 0..1 bubbles grow from flat film (for the sealing scene); rows: only the first `rows` rows are inflated (float ok).
    squash(i, j) -> 0..1 how much a bubble is pressed flat (bumps being absorbed)."""
    pitch = r * 2.35
    with g.at(x, y, rot):
        g.rect(0, 0, w, h, col, mix(col, INK, 0.45), lw=5, r=14, a=a * 0.45)
        ny = int(h // (pitch * 0.87)) + 1
        nx = int(w // pitch) + 1
        for i in range(ny):
            cy = r * 1.2 + i * pitch * 0.87
            if cy > h - r * 0.6:
                break
            inf = inflate if rows is None else clamp(rows - i) * inflate
            off = (pitch / 2) if i % 2 else 0.0
            for j in range(nx):
                cx = r * 1.2 + off + j * pitch
                if cx > w - r * 0.6:
                    break
                p = pop(i, j) if pop else 0.0
                sq = squash(i, j) if squash else 0.0
                rr = r * (0.35 + 0.65 * ease_out(inf))
                ry = rr * (1 - 0.75 * p) * (1 - 0.45 * sq)
                rx = rr * (1 + 0.15 * p + 0.2 * sq)
                if inf <= 0.02:
                    g.circle(cx, cy, r * 0.32, None, mix(col, INK, 0.35), lw=3, a=a * 0.6)
                    continue
                g.ellipse(cx, cy, rx, ry, mix(col, "#FFFFFF", 0.25), mix(col, INK, 0.55), lw=4, a=a)
                if p < 0.7:
                    g.ellipse(cx - rx * 0.32, cy - ry * 0.38, rx * 0.32, ry * 0.18, BUB_HI, None, a=a * 0.9, rot=-0.5)
                    g.circle(cx + rx * 0.35, cy + ry * 0.3, rr * 0.08, BUB_HI, None, a=a * 0.7)
                else:
                    g.line([(cx - rx * 0.6, cy), (cx - rx * 0.1, cy - ry * 0.4), (cx + rx * 0.3, cy + ry * 0.2), (cx + rx * 0.6, cy)],
                           mix(col, INK, 0.5), 3, a=a)
                if 0.05 < p < 0.6:
                    burst(g, cx, cy, rr * 0.9, rr * 1.9, n=8, col="#FFFFFF", w=6, k=1.0 - p / 0.6, a=0.9)
    return pitch


def pop_wave(t0, speed=7.0, cx=0.0, cy=0.0, d=0.18, order="radial"):
    """Helper -> pop(i, j): bubbles pop in a wave from (row cy, col cx) starting at time t0 (call with the current time bound)."""
    def make(t):
        def f(i, j):
            dist = math.hypot(i - cy, j - cx)
            return clamp((t - t0 - dist / speed) / d)
        return f
    return make


# ------------------------------------------------------------------ 1957 home
def room_1957(g, t, fy=1560, paper=0.0, warm=1.0):
    """A 1950s living room: pastel striped wallpaper, a picture rail, a standard lamp, the arm of a mint sofa, a sunny window.
    paper (0..1): how much of the wall (from the left) is already covered with bubble film."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#F6D9B0", "#F0C89A"))
    for x in range(-200, W + 200, 90):
        g.rect(x, 0, 44, fy, "#F7E4C4", None, a=0.7)
    with g.layer(0.6):
        g.rect(640, 320, 380, 470, "#BFE7F5", INK, lw=10, r=8)                        # window
        g.glow(830, 560, 320, "#FFF4C8", 0.5 * warm)
        g.line([(830, 320), (830, 790)], INK, 8); g.line([(640, 555), (1020, 555)], INK, 8)
        g.rect(610, 300, 440, 40, "#E07A5F", INK, lw=7, r=10)
        g.rect(600, 330, 70, 520, "#E07A5F", INK, lw=7, r=18); g.rect(990, 330, 70, 520, "#E07A5F", INK, lw=7, r=18)
    g.rect(-200, 250, W + 400, 22, "#C98A5A", INK, lw=5)                              # picture rail
    g.rect(-200, fy - 70, W + 400, 70, "#C98A5A", INK, lw=6)                          # skirting
    g.rect(-200, fy, W + 400, H - fy, g.lgrad(0, fy, 0, H, "#B8794A", "#8A5530"), None)
    for x in range(-200, W + 200, 160):
        g.line([(x, fy), (x - 60, H)], "#7A4A2A", 4, a=0.6)
    if paper > 0:
        bubble_sheet(g, -40, 280, (W + 80) * paper, fy - 360, t, r=30, a=0.8)


def lamp_1957(g, x, y, s=1.0, on=1.0):
    with g.at(x, y, 0, s):
        g.glow(0, -760, 300, "#FFE9A8", 0.45 * on)
        g.line([(0, 0), (0, -700)], INK, 10)
        g.ellipse(0, 0, 90, 20, "#7A5A3A", INK, lw=6)
        g.path("M-110 -680 L110 -680 L70 -840 L-70 -840 Z", "#FFE0A0", INK, lw=7)


def trash_can(g, x, y, s=1.0, lid=0.0):
    """Metal bin, feet at (x, y). lid: 0 closed, 1 lid flipped open (rotated back)."""
    with g.at(x, y, 0, s):
        g.path("M-120 0 L-140 -300 L140 -300 L120 0 Z", "#9AA6B2", INK, lw=8)
        for xx in (-80, -20, 40, 100):
            g.line([(xx - 10, -20), (xx - 14, -280)], "#7E8A96", 6)
        with g.at(-150, -300, -1.9 * lid):
            g.rc(150, -12, 310, 26, "#B6C0CA", INK, lw=7, r=12)
            g.rc(150, -34, 60, 22, "#B6C0CA", INK, lw=6, r=8)


# ------------------------------------------------------------------ 1957 workshop
def workshop_1957(g, t, fy=1500):
    """A garage workshop: pegboard wall with tools, a long workbench, a hanging work lamp."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#3E5A6E", "#2E4658"))
    with g.layer(0.5):
        g.rect(-100, 260, W + 200, 640, "#C9A27A", INK, lw=8)
        R = rnd(4).random
        for yy in range(300, 880, 46):
            for xx in range(-60, W + 120, 46):
                g.circle(xx, yy, 5, "#8A6A44", None, a=0.8)
        for k, (xx, kind) in enumerate(((120, "saw"), (330, "wrench"), (520, "hammer"), (760, "pliers"), (930, "saw"))):
            if kind == "wrench":
                g.rc(xx, 520, 30, 230, "#AEB8C2", INK, lw=6, r=12); g.circle(xx, 400, 40, "#AEB8C2", INK, lw=6)
            elif kind == "hammer":
                g.rc(xx, 560, 26, 240, "#B9804A", INK, lw=6, r=8); g.rc(xx, 440, 120, 50, "#7E8A96", INK, lw=6, r=8)
            elif kind == "pliers":
                g.line([(xx - 30, 640), (xx, 420), (xx + 30, 640)], "#E05A4A", 18)
            else:
                g.path(f"M{xx-70} 380 L{xx+70} 380 L{xx+70} 470 L{xx-70} 540 Z", "#C9D2DC", INK, lw=6)
                g.rc(xx + 90, 420, 60, 80, "#B9804A", INK, lw=6, r=14)
    g.rect(-100, fy - 30, W + 200, 60, "#8A5A3A", INK, lw=8)
    g.rect(-100, fy + 30, W + 200, H - fy, "#4A3A30", None)
    g.line([(540, -10), (540, 120)], INK, 6)
    g.path("M440 200 L640 200 L590 120 L490 120 Z", "#5ED3B5", INK, lw=7)
    g.glow(540, 300, 380, "#FFF0B8", 0.35)


def curtain(g, x, y, w, h, col, stripe=None, t=0.0, wave=1.0, a=1.0):
    """A shower curtain hanging from rings at (x, y) top-left, wavy folds; stripe adds pastel stripes."""
    n = 6
    pts = [(x + w * i / (n * 2), y + h + 18 * wave * math.sin(i * 1.6 + t * 2)) for i in range(n * 2 + 1)]
    d = f"M{x} {y} L{x + w} {y} L{pts[-1][0]} {pts[-1][1]} " + " ".join(f"L{px} {py}" for px, py in reversed(pts)) + " Z"
    g.path(d, col, INK, lw=6, a=a)
    if stripe:
        for i in range(1, n * 2, 2):
            xx = x + w * i / (n * 2)
            g.line([(xx, y + 10), (xx + 6 * math.sin(t + i), y + h - 10)], stripe, w / (n * 2) * 0.6, a=a * 0.85)
    for i in range(n + 1):
        g.circle(x + w * i / n, y, 14, "#C9D2DC", INK, lw=5, a=a)


def sealer(g, x, y, s=1.0, t=0.0, heat=1.0, run=1.0):
    """The engineers' homemade heat-sealing machine: two big rollers with a glowing heater bar between them. (x, y) = roller nip."""
    with g.at(x, y, 0, s):
        g.rect(-260, 60, 520, 330, "#5A6E86", INK, lw=9, r=18)
        g.rect(-220, 110, 120, 70, "#2E3A4A", INK, lw=6, r=8)
        for k in range(3):
            g.circle(-190 + k * 40, 145, 12, ("#FF6B5B", "#FFC93C", "#5ED3B5")[k], INK, lw=4)
        g.rc(140, 150, 90, 40, "#2E3A4A", INK, lw=6, r=8)
        for yy, sgn in ((-80, 1), (80, -1)):
            g.circle(0, yy - 0 if yy < 0 else yy, 82, "#C9D2DC", INK, lw=9)
            for k in range(6):
                a_ = t * 3 * sgn * run + k * TAU / 6
                g.line([(0, yy), (64 * math.cos(a_), yy + 64 * math.sin(a_))], "#8A96A4", 6)
            g.circle(0, yy, 18, "#7E8A96", INK, lw=5)
        g.glow(0, 0, 160, "#FF8A3D", 0.55 * heat)
        g.rc(0, 0, 40, 26, mix("#7E8A96", "#FF6B2E", heat), INK, lw=5, r=8)


def shop_1957(g, t, fy=1580):
    """A 1950s decorating shop: a pastel counter, shelves with wallpaper rolls, bunting."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#FFE6C7", "#F7C9A6"))
    with g.layer(0.5):
        for yy in (420, 700, 980):
            g.rect(-60, yy, W + 120, 26, "#C98A5A", INK, lw=6)
            R = rnd(yy).random
            for k in range(7):
                xx = -20 + k * 170 + R() * 30
                col = (MINT, PINK, "#FFD27A", "#A8C8F0")[k % 4]
                g.rc(xx + 60, yy - 70, 120, 140, col, INK, lw=6, r=60)
                g.circle(xx + 60, yy - 70, 22, shade(col, -0.25), INK, lw=4)
        for k in range(12):
            xx = -40 + k * 100
            g.path(f"M{xx} 150 L{xx + 100} 150 L{xx + 50} 230 Z", ("#FF6B5B", "#FFC93C", "#5ED3B5")[k % 3], INK, lw=5)
        g.line([(-60, 150), (W + 60, 150)], INK, 6)
    g.rect(-100, fy - 300, W + 200, 300, "#5ED3B5", INK, lw=9, r=10)
    g.rect(-100, fy - 330, W + 200, 40, "#FFF4E0", INK, lw=7, r=10)
    g.rect(-100, fy, W + 200, H - fy, "#8A5A3A", None)


def wall_roll(g, x, y, s=1.0, t=0.0, unroll=0.6):
    """A roll of 'textured wallpaper' (bubble film) standing on its end, a sheet unrolled downward for display."""
    with g.at(x, y, 0, s):
        L = 520 * unroll
        bubble_sheet(g, -150, 0, 300, L, t, r=22, a=0.95)
        g.rc(0, 0, 330, 90, "#E9F7FF", INK, lw=8, r=45)
        g.ellipse(-165, 0, 22, 45, "#CFEFFF", INK, lw=6)
        g.rc(0, 0, 120, 92, "#FF6B5B", INK, lw=6, r=8)                               # paper band, no text


# ------------------------------------------------------------------ greenhouse
def greenhouse(g, t, cover=1.0, slide=0.0, droop=0.0, fy=1600):
    """Sunny garden with a glass greenhouse; bubble panels fixed on the glass (cover 0..1); slide: the panels peel and slide down;
    droop: the potted plants inside wilt."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#7EC8EE", "#CDEBF6"))
    g.glow(900, 260, 280, "#FFF4A8", 0.6); g.circle(900, 260, 90, "#FFE066", INK, lw=8)
    g.rect(-100, fy, W + 200, H - fy, g.lgrad(0, fy, 0, H, "#6FBF5A", "#3E8E3A"), None)
    x0, x1, yb, yt, yr = 120, 960, fy + 20, 820, 560
    g.path(f"M{x0} {yb} L{x0} {yt} L{(x0 + x1) / 2} {yr} L{x1} {yt} L{x1} {yb} Z", "#DFF4FA", INK, lw=10, a=0.55)
    for k in range(5):                                                                 # plants inside
        px = x0 + 100 + k * 165
        g.path(f"M{px - 50} {yb - 10} L{px + 50} {yb - 10} L{px + 38} {yb - 110} L{px - 38} {yb - 110} Z", "#D9824A", INK, lw=6)
        g.line([(px, yb - 110), (px + droop * 60, yb - 330 + droop * 140)], "#3E8E3A", 12)
        for sgn in (-1, 1):
            g.ellipse(px + sgn * 50 + droop * 40 * sgn, yb - 270 + droop * (110 + 40 * sgn), 60, 26, "#5EBF5A", INK, lw=5, rot=sgn * (0.5 + droop))
    for xx in range(x0, x1 + 1, 140):
        g.line([(xx, yb), (xx, yt if xx in (x0, x1) else yt - (min(xx - x0, x1 - xx) / ((x1 - x0) / 2)) * (yt - yr))], INK, 8)
    g.line([(x0, yt), ((x0 + x1) / 2, yr), (x1, yt)], INK, 10)
    if cover > 0:
        for k in range(3):
            px = x0 + 20 + k * 280
            dy = slide * (380 + 120 * k) * (k + 1) / 3
            rr = slide * (0.18 if k % 2 else -0.2)
            bubble_sheet(g, px, yt + 20 + dy, 250 * cover, 560, t, r=22, a=0.85, rot=rr)


# ------------------------------------------------------------------ 1960 computer + shipping
def mainframe(g, x, y, s=1.0, t=0.0, lights=1.0, shine=0.0):
    """A generic 1960 room-size computer cabinet (no logo): tall grey unit with tape reels and blinking lamps. Feet at (x, y)."""
    with g.at(x, y, 0, s):
        g.rect(-230, -900, 460, 900, "#C9CED6", INK, lw=10, r=14)
        g.rect(-200, -870, 400, 60, "#3E4A5A", INK, lw=6, r=8)
        for k, rx in enumerate((-95, 95)):
            for rz in (-640, -420):
                g.circle(rx, rz, 82, "#2E3A4A", INK, lw=7)
                a_ = t * (2 + k) * lights
                for q in range(3):
                    g.line([(rx, rz), (rx + 60 * math.cos(a_ + q * 2.09), rz + 60 * math.sin(a_ + q * 2.09))], "#8A96A4", 6)
                g.circle(rx, rz, 20, "#C9CED6", INK, lw=5)
        R = rnd(11).random
        for yy in range(-290, -110, 34):
            for xx in range(-180, 190, 40):
                on = (math.sin(t * 6 + R() * 20) > 0.2) * lights
                g.circle(xx, yy, 10, mix("#556070", ("#FF6B5B", "#FFC93C", "#5ED3B5")[int(R() * 3)], on), INK, lw=3)
        g.rect(-230, -90, 460, 90, "#9AA3AD", INK, lw=8, r=8)
        if shine > 0:
            g.glow(0, -500, 520, "#FFF4C8", 0.4 * shine)


def crate(g, x, y, w=560, h=820, open_=0.0, xray=0.0, crack=0.0, t=0.0):
    """Wooden shipping crate, feet at (x, y). xray 0..1 fades the front planks to see inside; open_ lifts the lid off;
    crack 0..1 draws a red warning crack across the front."""
    with g.at(x, y):
        a = 1.0 - 0.8 * xray
        g.rect(-w / 2, -h, w, h, "#C98A4A", INK, lw=10, a=a)
        for yy in range(int(-h + 90), 0, 120):
            g.line([(-w / 2, yy), (w / 2, yy)], "#9A6232", 6, a=a)
        g.line([(-w / 2, -h), (w / 2, 0)], "#9A6232", 16, a=a)
        g.line([(w / 2, -h), (-w / 2, 0)], "#9A6232", 16, a=a)
        g.rect(-w / 2, -h, w, h, None, INK, lw=10)
        with g.at(0, -h - 140 * open_, 0.25 * open_):
            g.rc(0, -20, w + 40, 46, "#B9783A", INK, lw=9, r=8)
        if crack > 0:
            d = [(-w * 0.35, -h * 0.75), (-w * 0.12, -h * 0.6), (-w * 0.2, -h * 0.45), (w * 0.08, -h * 0.35), (0.0, -h * 0.2), (w * 0.25, -h * 0.1)]
            n = max(2, int(len(d) * crack + 0.999))
            g.line(d[:n], "#FF3B2E", 14)


def road(g, t, fy=1500, speed=600.0, bump=1.0):
    """Night-blue road scene with a bumpy cobbled road scrolling left (motion lines), hills behind."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#F6B98A", "#F7D9B0"))
    with g.layer(0.3):
        g.path(f"M-600 {fy - 200} Q-200 {fy - 520} 200 {fy - 260} Q600 {fy - 560} 1000 {fy - 260} Q1400 {fy - 480} 1800 {fy - 200} L1800 {fy} L-600 {fy} Z",
               "#7FAF6A", INK, lw=7)
    g.rect(-100, fy, W + 200, H - fy, "#5A5048", None)
    off = (t * speed) % 120
    for k in range(-2, 14):
        xx = k * 120 - off
        g.ellipse(xx, fy + 60 + 14 * math.sin(k), 46, 16 * bump, "#7A6E64", INK, lw=4)
    for k in range(6):
        yy = fy - 600 + k * 90
        xx = (W + 200) - ((t * speed * 1.6 + k * 230) % (W + 500))
        g.line([(xx, yy), (xx + 160, yy)], "#FFFFFF", 8, a=0.6)


def truck(g, x, y, s=1.0, t=0.0, bump=0.0, cargo=None):
    """A 1960 delivery truck (no logo), wheels at y. bump shakes the body; cargo(g) draws on the flatbed (origin = bed centre)."""
    jig = bump * 18 * math.sin(t * 25)
    with g.at(x, y, 0, s):
        for wx in (-330, 230):
            g.circle(wx, -60, 70, "#2A2A30", INK, lw=8); g.circle(wx, -60, 28, "#C9CED6", INK, lw=5)
        with g.at(0, jig):
            g.rect(-470, -170, 760, 60, "#3E5A8C", INK, lw=8, r=8)
            g.path("M290 -110 L290 -430 L440 -430 L520 -300 L520 -110 Z", "#FF6B5B", INK, lw=9)
            g.rect(330, -400, 120, 100, "#BFE7F5", INK, lw=6, r=8)
            if cargo:
                with g.at(-90, -170):
                    cargo(g)


def computer_room(g, t, fy=1580):
    """A 1960 office/computer floor: pale green walls, tiled floor, window strip, ceiling lights."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#CFE6D6", "#B8D6C4"))
    for x in range(-60, W + 120, 270):
        g.rect(x, 140, 200, 40, "#FFFBEA", INK, lw=5, r=8)
        g.glow(x + 100, 200, 200, "#FFFBEA", 0.25)
    g.rect(-100, fy, W + 200, H - fy, "#E6E0D2", None)
    for x in range(-200, W + 200, 140):
        g.line([(x, fy), (x - 80, H)], "#C9C2B2", 4)
    for yy in range(fy + 80, H, 110):
        g.line([(-100, yy), (W + 100, yy)], "#C9C2B2", 4)


def parcel(g, x, y, w, h, col="#C98A4A", t=0.0, wrap=1.0, rot=0.0):
    """A cardboard box with bubble film peeking out of the open top, feet at (x, y)."""
    with g.at(x, y, rot):
        if wrap > 0:
            bubble_sheet(g, -w * 0.42, -h - 60 * wrap, w * 0.84, 90 * wrap, t, r=16, a=0.95)
        g.rect(-w / 2, -h, w, h, col, INK, lw=8)
        g.rect(-w * 0.08, -h, w * 0.16, h, "#E9D2A0", None, a=0.8)
        g.path(f"M{-w / 2} {-h} L{-w * 0.62} {-h - 50} L{-w * 0.05} {-h - 40} L0 {-h} Z", shade(col, 0.1), INK, lw=6)
        g.path(f"M{w / 2} {-h} L{w * 0.62} {-h - 50} L{w * 0.05} {-h - 40} L0 {-h} Z", shade(col, 0.1), INK, lw=6)
