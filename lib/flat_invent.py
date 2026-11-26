"""Style F props for invention stories (B-008 "How 7 Everyday Things Were Invented by Accident", 26 Nov 2026).
All drawn in code, original. Coordinates: x, y = the prop's base centre unless noted; s = scale.
    from flat_invent import *
magnetron, candy_bar (melting), popcorn, egg, slinky (walking steps), spring_shelf, burr, hook_strip, glue_tube, glue_drop, refractometer,
gas_cylinder, scale_dial, powder_pile, frying_pan, flask (crack k), glass_sandwich, petri_dish (mould + clear ring), microscope_brass,
oven_1947, microwave_modern, medal, countdown_plaque, display_case.
"""
import math
from flat2d import *


# ------------------------------------------------------------------ microwave story
def magnetron(g, x, y, s=1.0, t=0.0, on=1.0):
    """Copper radar tube with cooling fins on a black base; glows coral when on."""
    with g.at(x, y, 0, s):
        if on > 0:
            g.glow(0, -170, 330, "#FF9A6A", 0.45 * on * (0.85 + 0.15 * math.sin(t * 9)))
        g.rc(0, -20, 300, 40, "#2A2A34", INK, lw=7, r=10)
        for i in range(7):
            yy = -70 - i * 28
            g.rc(0, yy, 230 - 6 * i, 16, "#D98A4A", INK, lw=5, r=6)
        g.rc(0, -170, 120, 250, "#C46A32", INK, lw=7, r=20)
        g.circle(0, -170, 34, mix("#FFC93C", "#7A3A1E", 1 - on), INK, lw=6)
        g.line([(-150, -40), (-220, -40), (-220, 10)], "#2F3A4F", 12)
        g.line([(150, -40), (220, -40), (220, 10)], "#FF6B5B", 12)
        if on > 0:
            for i in range(3):
                ph = (t * 1.3 + i / 3) % 1
                g.circle(0, -170, 60 + 260 * ph, None, "#FFB38A", lw=6, a=0.55 * on * (1 - ph))


def candy_bar(g, x, y, s=1.0, melt=0.0, t=0.0, rot=0.0, wrap="#FF6B5B"):
    """Chocolate bar in a wrapper (top centre at x,y), melting downward with drips as melt -> 1."""
    with g.at(x, y, rot, s):
        sag = 40 * melt
        g.path(f"M-70 0 L70 0 L70 {150 + sag * 0.3} Q0 {170 + sag} -70 {150 + sag * 0.3} Z", "#6B3A22", INK, lw=6)
        if melt < 0.5:
            for i in range(3):
                g.line([(-70, 40 + i * 40), (70, 40 + i * 40)], "#4E2814", 4, a=1 - melt * 2)
        g.rc(0, 110 + sag * 0.2, 150, 90, wrap, INK, lw=6, r=8)
        g.text("CANDY", 0, 112 + sag * 0.2, 30, PAL["cream"], stroke=None)
        for i, dx in enumerate((-40, 10, 48)):
            L = melt * (120 + 60 * i) * (0.8 + 0.2 * math.sin(t * 2 + i))
            if L > 4:
                yy = 150 + sag * 0.6
                w0, w1 = 26 - 5 * i, 9 - i
                g.path(f"M{dx - w0} {yy - 4} Q{dx - w1} {yy + L * 0.5} {dx - w1} {yy + L} L{dx + w1} {yy + L} Q{dx + w1} {yy + L * 0.5} {dx + w0} {yy - 4} Z",
                       "#6B3A22", INK, lw=4)
                g.circle(dx, yy + L + 6, w1 + 7, "#6B3A22", INK, lw=4)
                g.ellipse(dx - 4, yy + L + 2, 4, 6, "#9A5A3A", None)


def pocket(g, x, y, w=150, h=120, col="#4A5C76"):
    g.rc(x, y + h / 2, w, h, col, INK, lw=6, r=10)
    g.line([(x - w / 2 + 8, y + 16), (x + w / 2 - 8, y + 16)], INK, 4)


def popcorn(g, x, y, r=26, k=1.0, rot=0.0, kernel=False):
    if kernel or k < 0.3:
        g.ellipse(x, y, r * 0.45, r * 0.6, "#E8A94A", INK, lw=4, rot=rot)
        return
    with g.at(x, y, rot, back_out(clamp((k - 0.3) / 0.7), 2.2)):
        for i, (dx, dy) in enumerate(((0, 0), (-0.6, -0.4), (0.6, -0.35), (0.1, -0.8), (-0.4, 0.4), (0.5, 0.45))):
            g.circle(dx * r, dy * r, r * 0.62, "#FFF6DA", INK, lw=4)
        g.ellipse(0, r * 0.3, r * 0.35, r * 0.25, "#E8A94A", None)


def egg(g, x, y, s=1.0, burst=0.0, rot=0.0):
    with g.at(x, y, rot, s):
        if burst <= 0:
            g.ellipse(0, 0, 60, 78, "#FFF4E0", INK, lw=6)
            g.ellipse(-18, -26, 14, 20, "#FFFFFF", None, a=0.8)
            return
        k = ease_out(clamp(burst))
        for i in range(10):
            a0 = i * TAU / 10 + 0.2
            d = 40 + 260 * k
            g.poly([(d * math.cos(a0), d * math.sin(a0)), (d * math.cos(a0) + 30, d * math.sin(a0) + 10),
                    (d * math.cos(a0) + 10, d * math.sin(a0) + 34)], "#FFF4E0", INK, lw=4, a=1 - 0.6 * k)
        g.circle(0, 0, 50 + 120 * k, "#FFC93C", INK, lw=5, a=1 - 0.7 * k)
        g.circle(0, 0, 30 + 160 * k, None, "#FFF4E0", lw=12, a=1 - k)


def oven_1947(g, x, y, s=1.0, t=0.0, on=0.0):
    """The first commercial microwave: a fridge-sized grey cabinet (feet at x,y, ~1.8 m tall at s=1 -> 820 units)."""
    with g.at(x, y, 0, s):
        g.rc(0, -410, 380, 820, "#AEB7C0", INK, lw=9, r=18)
        g.rc(0, -560, 300, 220, "#2F3A4F", INK, lw=7, r=10)
        if on:
            g.rc(0, -560, 280, 200, "#FFB38A", None, r=8, a=0.35 * on * (0.8 + 0.2 * math.sin(t * 6)))
        for i in range(3):
            g.circle(-100 + i * 100, -360, 26, "#5A6470", INK, lw=5)
        for i in range(6):
            g.line([(-150, -240 + i * 34), (150, -240 + i * 34)], "#8A949E", 6)
        g.rc(0, -700, 220, 50, "#5A6470", INK, lw=5, r=8)


def microwave_modern(g, x, y, s=1.0, t=0.0, on=0.0, door=0.0, food=True):
    """Countertop microwave (base centre at x,y)."""
    with g.at(x, y, 0, s):
        g.rc(0, -150, 520, 300, "#E6E9EE", INK, lw=8, r=24)
        g.rc(-60, -150, 340, 230, "#2A3340", INK, lw=6, r=14)
        if on:
            g.rc(-60, -150, 320, 210, "#FFE29A", None, r=10, a=0.35 * on)
        if food:
            g.ellipse(-60, -70, 110, 22, "#F4F1EA", INK, lw=5)
            g.ellipse(-60, -88, 70, 26, "#E07A3A", INK, lw=5)
            if on:
                for i in range(3):
                    ph = (t * 0.8 + i / 3) % 1
                    g.path(f"M{-90 + i * 30} {-120 - 80 * ph} q12 -20 0 -40", None, "#FFFFFF", lw=6, a=0.6 * (1 - ph))
        g.rc(190, -200, 90, 60, "#1E2A36", INK, lw=5, r=8)
        g.text("0:30" if on else "--:--", 190, -198, 30, "#7CF0B5", stroke=None)
        for i in range(3):
            g.circle(165 + i * 25, -120, 9, "#B8BEC6", INK, lw=3)


# ------------------------------------------------------------------ spring toy
def slinky(g, x0, y0, x1, y1, t, s=1.0, col="#C9CED6", n=26, arc=1.0):
    """A coil spring stretched from (x0,y0) to (x1,y1) along an arch (arc>0 = walking over a step)."""
    pts = []
    for i in range(n + 1):
        u = i / n
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - arc * 4 * u * (1 - u) * 180 * s
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        rx, ry = 62 * s, 22 * s
        g.ellipse(x, y, rx, ry, None, INK, lw=13 * s)
        g.ellipse(x, y, rx, ry, None, mix(col, "#FFFFFF", 0.25 * (i % 2)), lw=7 * s)


def _coil_ring(g, x, y, ang, s, col, i):
    g.ellipse(x, y, 13 * s, 58 * s, None, INK, lw=12 * s, rot=ang)
    g.ellipse(x, y, 13 * s, 58 * s, None, mix(col, "#FFFFFF", 0.3 * (i % 2)), lw=6 * s, rot=ang)


def slinky_walk(g, x, y, step_w, step_h, t, s=1.0, period=1.1, col="#C9CED6", n=22):
    """Spring walking down stairs (side view). x,y = where the spring stands on the first step; each period it flips one step down/right.
    The coils travel over a half-circle arch from the back stack to the front stack."""
    k = max(0.0, t) / period
    i = int(k)
    u = ease_io(k - i)
    ax, ay = x + i * step_w, y + i * step_h            # back end (on the upper step)
    bx, by = ax + step_w, ay + step_h                  # front end lands here
    mx, my = (ax + bx) / 2, (ay + by) / 2
    R = math.hypot(bx - ax, by - ay) / 2
    base = math.atan2(ay - my, ax - mx)                # angle of A seen from M
    sweep = -math.pi if bx > ax else math.pi           # go over the top
    # front end angle fa, back end angle ba (fractions of the half circle)
    fa, ba = min(1.0, u * 2), max(0.0, u * 2 - 1)
    m = max(2, int(n * (fa - ba)))
    stackA = n - m if u < 0.5 else 0
    stackB = n - m if u >= 0.5 else 0
    for j in range(stackA):                            # compact stack standing on step A
        _coil_ring(g, ax, ay - 8 * s - j * 9 * s, math.pi / 2, s, col, j)
    for j in range(m + 1):
        f = ba + (fa - ba) * j / m
        a = base + sweep * f
        px, py = mx + R * math.cos(a), my - abs(R * math.sin(a)) * 1.25 - 8 * s
        tang = a + math.pi / 2
        _coil_ring(g, px, py, tang, s, col, j)
    for j in range(stackB):
        _coil_ring(g, bx, by - 8 * s - j * 9 * s, math.pi / 2, s, col, j)
    return bx, by


def spring_coil(g, x, y, s=1.0, rot=0.0, n=12, col="#C9CED6"):
    with g.at(x, y, rot, s):
        for i in range(n):
            g.ellipse(0, -i * 12, 40, 14, None, INK, lw=10)
            g.ellipse(0, -i * 12, 40, 14, None, col, lw=5)


# ------------------------------------------------------------------ hook and loop
def burr(g, x, y, r=40, rot=0.0, col="#8A6A3A", hooks=True, n=18):
    with g.at(x, y, rot):
        if hooks:
            for i in range(n):
                a0 = i * TAU / n
                p0 = (r * 0.8 * math.cos(a0), r * 0.8 * math.sin(a0))
                p1 = (r * 1.45 * math.cos(a0), r * 1.45 * math.sin(a0))
                p2 = (r * 1.45 * math.cos(a0 + 0.22), r * 1.45 * math.sin(a0 + 0.22))
                g.line([p0, p1, p2], shade(col, 0.7), max(3, r * 0.09))
        g.circle(0, 0, r, col, INK, lw=max(3, r * 0.1))
        g.circle(-r * 0.3, -r * 0.3, r * 0.25, shade(col, 1.25), None, a=0.6)


def hook_closeup(g, x, y, s=1.0, rot=0.0, col="#C9A25A"):
    """One magnified hook (microscope view)."""
    with g.at(x, y, rot, s):
        g.path("M0 120 L0 -60 Q0 -110 45 -110 Q90 -110 90 -60 Q90 -30 60 -25", None, INK, lw=34)
        g.path("M0 120 L0 -60 Q0 -110 45 -110 Q90 -110 90 -60 Q90 -30 60 -25", None, col, lw=22)


def loop_closeup(g, x, y, s=1.0, rot=0.0, col="#E07A5F"):
    with g.at(x, y, rot, s):
        g.path("M-60 120 Q-80 -80 0 -90 Q80 -80 60 120", None, INK, lw=26)
        g.path("M-60 120 Q-80 -80 0 -90 Q80 -80 60 120", None, col, lw=14)


def hook_strip(g, x, y, w, k_close=0.0, t=0.0, a_col="#FF6B5B", b_col="#3E7CB1"):
    """Two fabric strips (hooks top, loops bottom) closing together as k_close -> 1. x,y = centre."""
    gap = 120 * (1 - ease_io(clamp(k_close)))
    g.rc(x, y - 40 - gap, w, 60, a_col, INK, lw=7, r=10)
    g.rc(x, y + 40 + gap, w, 60, b_col, INK, lw=7, r=10)
    n = int(w // 40)
    for i in range(n):
        xx = x - w / 2 + 20 + i * 40
        g.path(f"M{xx} {y - 10 - gap} l0 22 q0 10 10 10", None, shade(a_col, 0.6), lw=5)
        g.path(f"M{xx + 10} {y + 10 + gap} q-10 -26 10 -26 q20 0 10 26", None, shade(b_col, 1.4), lw=5)


# ------------------------------------------------------------------ glue
def glue_tube(g, x, y, s=1.0, rot=0.0, col="#F4F1EA", band="#FF6B5B", squeeze=0.0):
    with g.at(x, y, rot, s):
        g.path(f"M-50 0 L50 0 L{60 - 20 * squeeze} 200 L{-60 + 20 * squeeze} 200 Z", col, INK, lw=7)
        g.rc(0, 200, 130, 26, "#C9CED6", INK, lw=6, r=4)
        g.rc(0, 80, 100, 50, band, INK, lw=5, r=6)
        g.poly([(-22, 0), (22, 0), (8, -70), (-8, -70)], "#E6E6E6", INK, lw=6)
        g.rect(-6, -100, 12, 32, "#E6E6E6", INK, lw=4)


def glue_drop(g, x, y, r=18, k=1.0):
    if k <= 0: return
    with g.at(x, y, 0, k):
        g.circle(0, r * 0.3, r, "#E6F4FF", INK, lw=4)
        g.poly([(-r * 0.8, -r * 0.2), (0, -r * 1.6), (r * 0.8, -r * 0.2)], "#E6F4FF", None)
        g.line([(-r * 0.8, -r * 0.2), (0, -r * 1.6), (r * 0.8, -r * 0.2)], INK, 4)
        g.circle(-r * 0.35, 0, r * 0.25, "#FFFFFF", None)


def refractometer(g, x, y, s=1.0, stuck=0.0, t=0.0, lid=0.0):
    """Lab instrument with two hinged glass prism blocks (opens with lid; stuck shake when glued)."""
    sh = math.sin(t * 40) * 4 * stuck
    with g.at(x, y, 0, s):
        g.rc(0, -20, 420, 40, "#3A3A48", INK, lw=7, r=10)
        g.rc(-120, -160, 70, 240, "#5A5A6A", INK, lw=6, r=10)
        g.limb([(-120, -280), (-40, -330)], "#3A3A48", 40, lw=6)
        g.circle(-30, -335, 26, "#2A2A34", INK, lw=5)
        g.rc(80, -70, 220, 60, "#8FD3F0", INK, lw=6, r=6)          # lower prism
        with g.at(-30 + sh, -100, -0.9 * (1 - stuck) * lid):        # upper prism on a hinge at its left edge
            g.rc(110, 0, 220, 60, "#BDEBFF", INK, lw=6, r=6)
        if stuck > 0.5:
            g.line([(-30, -100), (190, -100)], "#FFC93C", 8, a=0.9)


# ------------------------------------------------------------------ non-stick
def gas_cylinder(g, x, y, s=1.0, rot=0.0, cut=0.0, valve_open=0.0, t=0.0, label="GAS"):
    """Small steel cylinder standing on its base (x,y); cut>0 = sawn in half showing the white powder inside."""
    with g.at(x, y, rot, s):
        if cut > 0:
            d = 60 * ease_out(clamp(cut))
            for side in (-1, 1):
                with g.at(side * d, 0):
                    pts = [(0, 0), (side * 70, 0), (side * 70, -300), (side * 40, -340), (0, -340)]
                    g.poly(pts, "#8A949E", INK, lw=7)
                    g.poly([(0, -10), (side * 60, -10), (side * 60, -290), (0, -290)], "#F4F1EA", INK, lw=4)
                    for i in range(5):
                        g.circle(side * (15 + 9 * i % 40), -50 - i * 48, 9, "#FFFFFF", None)
            return
        g.rc(0, -170, 140, 340, "#8A949E", INK, lw=7, r=40)
        g.rc(0, -170, 140, 60, "#FF6B5B", INK, lw=5)
        g.text(label, 0, -168, 34, PAL["cream"], stroke=None)
        g.rc(0, -360, 50, 50, "#5A6470", INK, lw=6, r=6)
        with g.at(0, -395, valve_open * 1.6):
            g.rc(0, 0, 90, 18, "#C9A23A", INK, lw=5, r=8)


def scale_dial(g, x, y, s=1.0, v=0.7, t=0.0, label="WEIGHT"):
    """Platform scale with a big round dial; v 0..1 needle."""
    with g.at(x, y, 0, s):
        g.rc(0, -20, 360, 40, "#5A6470", INK, lw=7, r=10)
        g.rc(0, -110, 60, 150, "#7A8490", INK, lw=6)
        g.circle(0, -270, 130, "#FFF4E0", INK, lw=9)
        for i in range(9):
            a0 = math.pi * (0.8 + 1.4 * i / 8)
            g.line([(100 * math.cos(a0), -270 + 100 * math.sin(a0)), (118 * math.cos(a0), -270 + 118 * math.sin(a0))], INK, 5)
        a = math.pi * (0.8 + 1.4 * v)
        g.line([(0, -270), (95 * math.cos(a), -270 + 95 * math.sin(a))], "#FF5B4B", 9)
        g.circle(0, -270, 14, INK, None)
        g.text(label, 0, -200, 26, INK, stroke=None)


def powder_pile(g, x, y, w=220, k=1.0, t=0.0):
    if k <= 0: return
    h = 90 * ease_out(clamp(k))
    g.path(f"M{x - w / 2} {y} Q{x - w * 0.2} {y - h} {x} {y - h} Q{x + w * 0.2} {y - h} {x + w / 2} {y} Z", "#FFFFFF", INK, lw=6)
    for i in range(6):
        g.circle(x - w * 0.3 + i * w * 0.12, y - h * 0.4 - (i % 2) * 14, 6, "#E6EEF5", None)
    from flat_fx import sparkles
    sparkles(g, t, [(x - w * 0.25, y - h - 20), (x + w * 0.3, y - h * 0.6)], col="#FFFFFF", r=16)


def frying_pan(g, x, y, s=1.0, rot=0.0, egg_slide=0.0, t=0.0):
    """Side-ish view non-stick pan with a fried egg that slides along (egg_slide -1..1)."""
    with g.at(x, y, rot, s):
        g.rc(330, -10, 300, 34, "#2A2A34", INK, lw=7, r=16)
        g.ellipse(0, 0, 250, 70, "#2F3440", INK, lw=9)
        g.ellipse(0, -6, 220, 54, "#3E4554", None)
        ex = 120 * egg_slide
        g.path(f"M{ex - 90} -6 Q{ex - 100} -40 {ex - 40} -44 Q{ex + 10} -70 {ex + 60} -40 Q{ex + 110} -20 {ex + 80} 6 Q{ex} 26 {ex - 90} -6 Z", "#FFFFFF", INK, lw=5)
        g.ellipse(ex - 5, -22, 34, 22, "#FFB627", INK, lw=4)
        g.ellipse(-80, -24, 60, 8, "#FFFFFF", None, a=0.25)


# ------------------------------------------------------------------ safety glass
def flask(g, x, y, s=1.0, rot=0.0, crack=0.0, film=0.0, col="#CDEFFA", seed=3):
    """Round-bottom lab flask (base x,y). crack 0..1 draws a web of cracks that stay inside the outline."""
    with g.at(x, y, rot, s):
        d = "M-40 -330 L-40 -220 Q-150 -170 -150 -90 Q-150 0 0 0 Q150 0 150 -90 Q150 -170 40 -220 L40 -330 Z"
        g.path(d, col, INK, lw=8, a=0.92)
        if film > 0:
            g.path("M-128 -110 Q-130 -20 0 -18 Q130 -20 128 -110", None, "#FFE29A", lw=12, a=0.6 * film)
        g.ellipse(-70, -120, 20, 40, "#FFFFFF", None, a=0.7, rot=0.3)
        g.rc(0, -335, 100, 22, shade(col, 0.85), INK, lw=6, r=6)
        if crack > 0:
            r = rnd(seed)
            cx, cy = 20, -100
            for i in range(9):
                a0 = i * TAU / 9 + r.random() * 0.3
                L = (90 + 50 * r.random()) * clamp(crack * 1.4 - i * 0.04)
                pts = [(cx, cy)]
                for j in range(3):
                    pts.append((cx + L * (j + 1) / 3 * math.cos(a0 + (r.random() - 0.5) * 0.5), cy + L * (j + 1) / 3 * math.sin(a0 + (r.random() - 0.5) * 0.5)))
                g.line(pts, INK, 4)
            for rr in (40, 80):
                if crack > 0.5:
                    g.circle(cx, cy, rr * crack, None, INK, lw=3, a=0.8)


def glass_sandwich(g, x, y, s=1.0, k=1.0, t=0.0):
    """Exploded view: glass / film / glass coming together as k -> 1 (x,y centre)."""
    gap = 90 * (1 - ease_io(clamp(k)))
    with g.at(x, y, -0.25, s):
        for i, (col, dy, lab) in enumerate((("#CDEFFA", -1, None), ("#FFE29A", 0, None), ("#CDEFFA", 1, None))):
            yy = dy * (30 + gap)
            g.poly([(-260, yy - 14), (180, yy - 14), (260, yy + 14), (-180, yy + 14)], col, INK, lw=6, a=0.9)


# ------------------------------------------------------------------ penicillin
def petri_dish(g, x, y, r=200, t=0.0, mould=0.0, ring=0.0, bact=1.0, seed=5, tilt=0.55):
    """Top-ish view dish: yellow bacteria colonies, a blue-green mould colony and a clear ring around it."""
    rr = rnd(seed)
    with g.at(x, y, 0, 1.0, tilt):
        g.circle(0, 0, r * 1.08, "#DDE8EE", INK, lw=8)
        g.circle(0, 0, r, "#F2E3B0", INK, lw=5)
        mx, my = -r * 0.25, -r * 0.2
        clear = r * (0.25 + 0.3 * ease_out(clamp(ring)))
        if ring > 0:
            g.circle(mx, my, clear, "#F8F0D2", None)
        for i in range(70):
            px, py = (rr.random() * 2 - 1) * r * 0.9, (rr.random() * 2 - 1) * r * 0.9
            if px * px + py * py > (r * 0.88) ** 2:
                continue
            dd = math.hypot(px - mx, py - my)
            if ring > 0 and dd < clear:
                continue
            g.circle(px, py, r * 0.035 * bact, "#E2B53C", None)
        if mould > 0:
            k = ease_out(clamp(mould))
            for i in range(9):
                a0 = i * TAU / 9
                g.circle(mx + r * 0.08 * math.cos(a0) * k, my + r * 0.08 * math.sin(a0) * k, r * 0.11 * k, "#5E9E86", None)
            g.circle(mx, my, r * 0.14 * k, "#3E7E6A", INK, lw=4)
            g.circle(mx, my, r * 0.06 * k, "#EAF4E0", None, a=0.7)
        g.ellipse(-r * 0.5, -r * 0.6, r * 0.3, r * 0.08, "#FFFFFF", None, a=0.4, rot=-0.5)


def microscope_brass(g, x, y, s=1.0):
    with g.at(x, y, 0, s):
        g.rc(0, -12, 180, 30, "#3A2A20", INK, lw=6, r=8)
        g.limb([(-50, -24), (-50, -170), (0, -230)], "#C9A23A", 30, lw=6)
        g.limb([(0, -230), (35, -120)], "#B8862A", 38, lw=6)
        g.rc(20, -90, 110, 14, "#8A6A3A", INK, lw=5)
        g.rc(-4, -250, 34, 40, "#2A2A34", INK, lw=5, r=4)


def medal(g, x, y, r=90, k=1.0, t=0.0):
    """Generic gold medal on a ribbon (not a real award design)."""
    if k <= 0: return
    with g.at(x, y, 0.06 * math.sin(t * 2), back_out(clamp(k), 1.6)):
        g.poly([(-50, -r - 160), (-10, -r - 160), (20, -r + 10), (-20, -r + 10)], "#3E7CB1", INK, lw=5)
        g.poly([(50, -r - 160), (10, -r - 160), (-20, -r + 10), (20, -r + 10)], "#FF6B5B", INK, lw=5)
        g.circle(0, 0, r, "#FFC93C", INK, lw=8)
        g.circle(0, 0, r * 0.72, None, "#E8A92A", lw=6)
        g.text("1945", 0, 6, r * 0.45, "#8A5A10", stroke=None)


# ------------------------------------------------------------------ museum
def countdown_plaque(g, x, y, n, k=1.0, s=1.0, t=0.0):
    """Big brass countdown number on a dark velvet plaque."""
    if k <= 0: return
    with g.at(x, y, -0.02 + 0.01 * math.sin(t * 1.5), s * back_out(clamp(k), 1.6)):
        g.rc(0, 0, 360, 420, "#4A1E2E", INK, lw=12, r=30)
        g.rc(0, 0, 320, 380, None, "#C9A23A", lw=8, r=24)
        g.text(f"#{n}", 0, 20, 230, "#FFC93C", sw=22, depth=14)


def display_case(g, x, y, w=320, h=300, t=0.0, lit=1.0):
    """Brass plinth with a glass dome case (base centre x,y); draw the exhibit before calling glass_front."""
    g.rc(x, y - 110, w + 60, 220, "#6B3A22", INK, lw=8, r=10)
    g.rc(x, y - 210, w + 90, 30, "#C9A23A", INK, lw=6, r=8)
    if lit:
        g.poly([(x - 60, -40), (x + 60, -40), (x + w / 2 + 40, y - 230), (x - w / 2 - 40, y - 230)], "#FFF2C0", None, a=0.10 * lit)


def glass_front(g, x, y, w=320, h=300):
    g.rc(x, y - 225 - h / 2, w, h, "#DDF3FF", INK, lw=6, r=14, a=0.25)
    g.line([(x - w / 2 + 30, y - 225 - h + 30), (x - w / 2 + 70, y - 260)], "#FFFFFF", 8, a=0.5)
