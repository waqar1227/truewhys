"""Time-ball / New Year assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-031 why we drop a ball at New Year).

    from flat_timeball import (city_square, tower_top, glow_ball, crowd_sil, fireworks, confetti, harbour_1833, observatory,
                               time_ball, tall_ship, chronometer, sea_chart, clock_face2)
Generic buildings only (no real signs, logos or billboards). All coordinates are design units (1080x1920) under the shot camera.
Every drawing is code-made (no downloaded art).
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd, ease_out, ease_io, back_out, TAU
from flat_fx import sparkle, burst

GOLD = "#FFC93C"
BALL_RED = "#E0503F"
FW_COLS = ("#FF6B5B", "#FFC93C", "#5ED3B5", "#4FA8FF", "#FF8AD8", "#FFFFFF")


# ------------------------------------------------------------------ modern New Year square (night)
def city_square(g, t, fy=1560, era="now", glow=1.0):
    """Night sky, rows of tall generic buildings with lit windows, and a central slim tower whose roof mast carries the ball.
    era='1907' gives lower, older buildings in warm sepia tones and gas-lamp light."""
    old = era == "1907"
    sky = ("#1A1030", "#2E1E4E", "#4A2E5A") if old else ("#0A0F2E", "#1C1F5A", "#3A2A72")
    g.fill_all(g.lgrad(0, 0, 0, H, *sky))
    with g.layer(0.12):
        R = rnd(5).random
        for i in range(50):
            g.circle(R() * (W + 600) - 300, R() * 900 - 100, 1.5 + 2.5 * R(), "#FFFFFF", None, a=(0.3 + 0.5 * R()) * (0.6 + 0.4 * math.sin(t * 2 + i)))
    with g.layer(0.35):
        R = rnd(8 if old else 3).random
        x = -500
        while x < W + 500:
            bw = 110 + R() * 120
            bh = (260 + R() * 260) if old else (500 + R() * 700)
            col = "#3A2A44" if old else "#1F2550"
            g.rect(x, fy - bh, bw, bh + 10, col, INK, lw=5)
            for yy in range(int(fy - bh + 30), int(fy - 20), 44):
                for xx in range(int(x + 16), int(x + bw - 20), 34):
                    if R() < 0.5:
                        g.rect(xx, yy, 16, 22, "#FFD27A" if old else "#FFE7A8", None, a=0.5 + 0.3 * R())
            x += bw + 14
    g.glow(540, fy - 200, 900, "#FF9E5E" if old else "#7A6AFF", 0.18 * glow)


def tower_top(g, x, y, s=1.0, era="now"):
    """Slim tower (centre x, its roof at y) with a flagpole mast above the roof; the ball slides on the mast.
    Returns (mast_top_y, mast_bottom_y) in design units."""
    old = era == "1907"
    with g.at(x, y, 0, s):
        body = "#5A4A5E" if old else "#3A3F78"
        g.path("M-150 0 L-130 -40 L130 -40 L150 0 L170 1700 L-170 1700 Z", body, INK, lw=9)
        for yy in range(40, 1700, 70):
            for xx in (-100, -40, 20, 80):
                g.rect(xx, yy, 26, 36, "#FFE7A8" if not old else "#FFD27A", None, a=0.55)
        g.rect(-150, -60, 300, 30, shade(body, -0.2), INK, lw=7)
        g.rect(-10, -560, 20, 520, "#C9D2DC", INK, lw=6)
        g.circle(0, -566, 14, GOLD, INK, lw=5)
    return y - 540 * s, y - 70 * s


def glow_ball(g, x, y, r, t, k=1.0, col=None, old=False):
    """The glowing New Year ball: faceted sphere with light points; old=True = a simpler 1907 ball of small bulbs."""
    g.glow(x, y, r * 3.2, "#FFF4C8" if old else "#BFE8FF", 0.45 * k)
    base = "#FFE7A8" if old else "#DFF4FF"
    g.circle(x, y, r, base, INK, lw=max(4, r * 0.07))
    with g.clip(circle=(x, y, r)):
        for i in range(-3, 4):
            g.ellipse(x + i * r * 0.28, y, r * 0.12 + abs(i) * 2, r, None, "#9FC8E8" if not old else "#E0B060", lw=3, a=0.7)
        for j in range(-3, 4):
            g.line([(x - r, y + j * r * 0.28), (x + r, y + j * r * 0.28)], "#9FC8E8" if not old else "#E0B060", 3, a=0.7)
        R = rnd(9).random
        for i in range(26):
            a = R() * TAU; d = R() * r * 0.9
            c = FW_COLS[i % 6] if not old else "#FFF4A8"
            g.circle(x + d * math.cos(a), y + d * math.sin(a), r * 0.06, c, None, a=0.6 + 0.4 * math.sin(t * 6 + i))
    g.ellipse(x - r * 0.35, y - r * 0.4, r * 0.25, r * 0.15, "#FFFFFF", None, a=0.6)


def crowd_sil(g, t, y=1920, n=13, cheer=1.0, seed=2, hats=False, col="#140C2A", s=1.0):
    """Dark crowd silhouettes along the bottom, arms up on cheer (hats=True: 1907 top hats and bonnets)."""
    R = rnd(seed).random
    for i in range(n):
        x = -60 + i * (W + 120) / (n - 1) + (R() - 0.5) * 50
        h = (240 + R() * 90) * s
        b = 10 * math.sin(t * 5 + i * 1.7) * cheer
        yy = y + b
        g.rc(x, yy - h * 0.32, h * 0.42, h * 0.75, col, None, r=h * 0.18)
        g.circle(x, yy - h * 0.8, h * 0.15, col, None)
        if hats and i % 2 == 0:
            g.rect(x - h * 0.11, yy - h * 1.05, h * 0.22, h * 0.17, col, None)
            g.rect(x - h * 0.19, yy - h * 0.9, h * 0.38, h * 0.04, col, None)
        if cheer > 0.3 and i % 3 != 1:
            for sd in (-1, 1):
                g.line([(x + sd * h * 0.16, yy - h * 0.6), (x + sd * h * 0.3, yy - h * 1.0 - 20 * math.sin(t * 7 + i))], col, h * 0.09)


def fireworks(g, t, bursts, k=1.0):
    """bursts: [(x, y, r, t0, col)] each blooms at local time t0 and fades over 1.4 s."""
    for (x, y, r, t0, col) in bursts:
        u = (t - t0)
        if u < 0 or u > 1.4: continue
        e = ease_out(clamp(u / 0.6)); fade = clamp(1.4 - u) * k
        for i in range(16):
            a = i / 16 * TAU
            p0 = (x + r * 0.25 * e * math.cos(a), y + r * 0.25 * e * math.sin(a) + 30 * u * u)
            p1 = (x + r * e * math.cos(a), y + r * e * math.sin(a) + 60 * u * u)
            g.line([p0, p1], col, 8, a=fade)
            g.circle(p1[0], p1[1], 7, "#FFFFFF", None, a=fade)
        g.glow(x, y, r * 1.2, col, 0.25 * fade)


def confetti(g, t, box=(-100, -100, W + 100, H), n=40, seed=6, k=1.0):
    R = rnd(seed).random
    x0, y0, x1, y1 = box
    for i in range(n):
        sp = 120 + R() * 160
        x = lerp(x0, x1, R()) + 40 * math.sin(t * 2 + i)
        y = y0 + ((R() * (y1 - y0) + t * sp) % (y1 - y0))
        g.rc(x, y, 18, 10, FW_COLS[i % 6], None, rot=t * 4 + i, a=k)


# ------------------------------------------------------------------ 1833 river + observatory
def harbour_1833(g, t, fy=1250):
    """Daytime 1830s river scene: pale sky, green hill on the left with the observatory, the river with small waves."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#8FD0E8", "#CDEBF2", "#F4E9CC"))
    with g.layer(0.2):
        for cx, cy, sc in ((200, 300, 1.0), (820, 420, 0.8)):
            for dx, dy, r in ((0, 0, 70), (70, -20, 60), (-70, 10, 55), (130, 15, 45)):
                g.circle(cx + dx * sc, cy + dy * sc, r * sc, "#FFFFFF", None, a=0.9)
    with g.layer(0.5):
        g.path(f"M-400 {fy} Q-100 {fy-420} 420 {fy-380} Q700 {fy-360} 900 {fy} Z", "#6FAE5A", INK, lw=7)
        g.path(f"M500 {fy} Q800 {fy-200} 1500 {fy-160} L1500 {fy} Z", "#5E9A4E", INK, lw=7)
    g.rect(-400, fy, W + 800, H - fy + 300, g.lgrad(0, fy, 0, H, "#4A9AB8", "#2E6E8E"), None)
    g.line([(-400, fy), (W + 400, fy)], INK, 6)
    for j in range(8):
        y = fy + 60 + j * 90
        off = (t * 40 * (1 + j * 0.2)) % 160
        for i in range(-1, 9):
            x = i * 160 - off
            g.path(f"M{x} {y} q20 -14 40 0 q20 14 40 0", None, "#BFE8FF", lw=5, a=0.6)


def observatory(g, x, y, s=1.0, ball_v=1.0, ball_col=BALL_RED):
    """Generic old brick observatory on a hill top (base centre x, y) with a tall mast on the roof; the time ball sits on the mast
    at height fraction ball_v (1 = top, 0 = bottom). Returns the ball centre."""
    with g.at(x, y, 0, s):
        g.rect(-230, -330, 460, 330, "#B45A42", INK, lw=8)
        for yy in range(-300, 0, 34):
            g.line([(-230, yy), (230, yy)], "#9E4A36", 3)
        for xx in (-150, 0, 150):
            g.rect(xx - 34, -260, 68, 120, "#FFE7A8", INK, lw=6, r=30)
        g.rect(-250, -360, 500, 40, "#7A3A2C", INK, lw=7)
        g.path("M-120 -360 Q0 -500 120 -360 Z", "#5A6E7A", INK, lw=7)              # small dome
        g.rect(-12, -980, 24, 600, "#5A3E2E", INK, lw=6)
        g.line([(-90, -900), (90, -900)], "#5A3E2E", 10)
        bx, by = 0, lerp(-500, -900, ball_v)
        g.circle(bx, by, 62, ball_col, INK, lw=8)
        g.ellipse(bx - 18, by - 22, 18, 12, "#FFFFFF", None, a=0.5)
    return (x + bx * s, y + by * s)


def tall_ship(g, x, y, s=1.0, t=0.0, flip=False, sails="#F4EBD6", hull="#6E4A32", rock=1.0):
    """Side-view three-masted sailing ship on the water line y."""
    roll = 0.03 * math.sin(t * 1.6 + x) * rock
    with g.at(x, y + 6 * math.sin(t * 1.6 + x) * rock, roll, -s if flip else s, s):
        g.path("M-300 -60 L300 -60 L250 40 L-250 40 Z", hull, INK, lw=8)
        g.rect(-300, -84, 600, 24, shade(hull, -0.2), INK, lw=6)
        for i in range(6):
            g.circle(-200 + i * 80, -14, 10, "#2A1C1E", None)
        for mx, mh in ((-160, 420), (0, 500), (160, 380)):
            g.rect(mx - 7, -84 - mh, 14, mh, "#5A3E2E", INK, lw=5)
            for j, (w_, yy) in enumerate(((150, 0.25), (120, 0.55))):
                top = -84 - mh * (1 - yy) - 20
                g.path(f"M{mx - w_ / 2} {top} Q{mx} {top + 30} {mx + w_ / 2} {top} L{mx + w_ / 2 - 10} {top + 120} Q{mx} {top + 145} {mx - w_ / 2 + 10} {top + 120} Z",
                       sails, INK, lw=5)
        g.path("M300 -70 L420 -150", None, "#5A3E2E", lw=8)
        g.path(f"M0 {-584} l50 14 l-50 14 Z", "#FF6B5B", INK, lw=4)


def chronometer(g, x, y, s=1.0, t=0.0, minute=0.0, hl=0.0):
    """Ship's chronometer in its wooden box (top view of the dial). minute offsets the minute hand by that many minutes (red ghost)."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 420, 420, "#8A5A3A", INK, lw=10, r=26)
        g.rc(0, 0, 360, 360, "#6E4630", INK, lw=6, r=20)
        g.circle(0, 0, 160, "#B8A27A", INK, lw=8)
        g.circle(0, 0, 140, "#FFF8E8", INK, lw=6)
        for i in range(60):
            a = i / 60 * TAU
            r0 = 118 if i % 5 else 104
            g.line([(r0 * math.sin(a), -r0 * math.cos(a)), (132 * math.sin(a), -132 * math.cos(a))], INK, 3 if i % 5 else 6)
        if hl > 0:
            g.circle(0, 0, 175, None, GOLD, lw=10, a=hl)
        hr, mn = 12.0, 0.0
        sec = (t * 6) % 60
        for val, ln, w_, col in ((hr / 12 + mn / 720, 70, 12, INK), (mn / 60, 112, 8, INK)):
            a = val * TAU
            g.line([(0, 0), (ln * math.sin(a), -ln * math.cos(a))], col, w_)
        if minute:
            a = (minute / 60) * TAU
            g.line([(0, 0), (112 * math.sin(a), -112 * math.cos(a))], "#E0503F", 8, a=0.9)
        a = sec / 60 * TAU
        g.line([(0, 0), (124 * math.sin(a), -124 * math.cos(a))], "#E0503F", 3)
        g.circle(0, 0, 10, GOLD, INK, lw=4)


def clock_face2(g, x, y, r, h, m, col="#FFF8E8"):
    """Simple wall clock at hour h, minute m."""
    g.circle(x, y, r * 1.12, "#5A3E2E", INK, lw=8)
    g.circle(x, y, r, col, INK, lw=6)
    for i in range(12):
        a = i / 12 * TAU
        g.line([(x + r * 0.78 * math.sin(a), y - r * 0.78 * math.cos(a)), (x + r * 0.9 * math.sin(a), y - r * 0.9 * math.cos(a))], INK, 6)
    for val, ln, w_ in (((h % 12) / 12 + m / 720, 0.5, 12), (m / 60, 0.75, 8)):
        a = val * TAU
        g.line([(x, y), (x + r * ln * math.sin(a), y - r * ln * math.cos(a))], INK, w_)
    g.circle(x, y, r * 0.08, GOLD, INK, lw=4)


def sea_chart(g, x, y, w, h, t, k=0.0, true_k=1.0, label_pts=True):
    """Old parchment chart: a coastline with rocks, the planned course (dashed) and the real course drifting off by k (0..1)."""
    with g.at(x, y):
        g.rc(0, 0, w, h, "#F1DFB4", INK, lw=10, r=20)
        g.rc(0, 0, w - 40, h - 40, None, "#C9A97A", lw=4, r=14)
        g.path(f"M{w*0.18} {-h/2+20} Q{w*0.3} {-h*0.1} {w*0.22} {h*0.1} Q{w*0.12} {h*0.3} {w*0.3} {h/2-20} L{w/2-20} {h/2-20} L{w/2-20} {-h/2+20} Z",
               "#C9B27A", INK, lw=6)
        for rx, ry in ((w * 0.12, h * 0.18), (w * 0.08, h * 0.05), (w * 0.15, -h * 0.05)):
            g.poly([(rx - 22, ry + 14), (rx, ry - 18), (rx + 24, ry + 14)], "#7A6A5A", INK, lw=4)
        sx, sy = -w * 0.38, h * 0.32
        ex, ey = w * 0.2, -h * 0.36                              # harbour
        g.line([(lerp(sx, ex, q / 20), lerp(sy, ey, q / 20)) for q in range(21)], "#3E7CB1", 7, dash=([18, 14], 0), a=true_k)
        g.circle(ex, ey, 16, "#3E7CB1", INK, lw=4)
        if k > 0:
            dx = w * 0.32 * k
            pts = [(lerp(sx, ex - 0 + dx * 0.0, q / 20) + dx * (q / 20) ** 1.5, lerp(sy, ey + h * 0.5 * k * 0.2, q / 20) + h * 0.4 * k * (q / 20) ** 2)
                   for q in range(21)]
            g.line(pts, "#E0503F", 8, dash=([18, 12], 0))
            px, py = pts[-1]
            with g.at(px, py, -0.4, 0.12):
                g.path("M-300 -60 L300 -60 L250 40 L-250 40 Z", "#6E4A32", INK, lw=40)
                g.rect(-8, -500, 16, 440, "#5A3E2E", INK, lw=20)
                g.path("M-120 -460 L120 -460 L100 -180 L-100 -180 Z", "#F4EBD6", INK, lw=24)
