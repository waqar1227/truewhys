"""Gaming-night assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-029 controller rumble).

    from flat_game import game_room, tv, controller, hands_on, motor_face, coil_actuator, rumble_waves
All coordinates are design units (1080x1920) under the shot camera. Every drawing is code-made (no downloaded art, no brand shapes:
the gamepad is a generic two-grip pad with plain round buttons, the TV game is our own cartoon race).
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd, ease_out, ease_io, back_out, TAU
from flat_fx import burst, sparkle

PAD, PAD_HI = "#323A52", "#47506E"
STEEL, STEEL_D = "#C9D2DC", "#8E9AA8"
COPPER = "#D9824A"
WEIGHT = "#FFC93C"
HEAVY = "#FF6B5B"
LIGHTW = "#5ED3B5"

PAD_PATH = ("M-200 -120 Q0 -150 200 -120 Q300 -110 322 0 Q352 150 302 222 Q252 276 190 212 Q150 152 100 132 L-100 132 "
            "Q-150 152 -190 212 Q-252 276 -302 222 Q-352 150 -322 0 Q-300 -110 -200 -120 Z")
MOTOR_L, MOTOR_R = (-236, 146), (236, 146)          # motor positions in pad units (inside the grips)


# ------------------------------------------------------------------ set: living room at night, lit by the TV
def game_room(g, t, glow=1.0, flash=0.0, fy=1620):
    """Navy room at night: window with city lights, shelf, lamp, rug, a sofa behind the player; the TV light washes the left side."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#121A33", "#1C2747", "#141B33"))
    with g.layer(0.35):                                                    # window: night city
        wx0, wy0, ww, wh = 640, 300, 380, 520
        g.rect(wx0 - 14, wy0 - 14, ww + 28, wh + 28, "#2A3358", INK, lw=8, r=10)
        g.rect(wx0, wy0, ww, wh, g.lgrad(0, wy0, 0, wy0 + wh, "#0C1430", "#26305E"), None)
        with g.clip(rect=(wx0, wy0, ww, wh)):
            R = rnd(31).random
            for i in range(9):
                bx = wx0 + i * 46 - 10; bh = 120 + R() * 260
                g.rect(bx, wy0 + wh - bh, 40, bh + 10, "#1A2246", None)
                for j in range(int(bh // 34)):
                    if R() < 0.45:
                        g.rect(bx + 8 + (j % 2) * 14, wy0 + wh - bh + 14 + j * 30, 9, 12, "#FFD27A", None, a=0.5 + 0.4 * math.sin(t * 0.7 + i + j))
            g.circle(wx0 + 300, wy0 + 90, 34, "#FFF4E0", None, a=0.9)
        g.line([(wx0 + ww / 2, wy0), (wx0 + ww / 2, wy0 + wh)], "#2A3358", 10)
        g.line([(wx0, wy0 + wh / 2), (wx0 + ww, wy0 + wh / 2)], "#2A3358", 10)
    with g.layer(0.6):                                                     # shelf + small plant + lamp
        g.rect(700, 960, 320, 26, "#5A3E2E", INK, lw=6, r=6)
        for i, c in enumerate(("#FF6B5B", "#5ED3B5", "#FFC93C", "#3E7CB1")):
            g.rect(716 + i * 40, 880 - (i % 2) * 14, 32, 80 + (i % 2) * 14, c, INK, lw=5, r=4)
        g.rect(900, 900, 70, 60, "#C8664E", INK, lw=5, r=8)
        for a in (-0.6, 0.0, 0.6):
            g.ellipse(935 + 40 * math.sin(a), 870 - 30 * math.cos(a), 18, 40, "#3E8E5E", INK, lw=4, rot=a)
        g.glow(980, 1180, 260, "#FFC96B", 0.18)
        g.rect(970, 1150, 14, 470, "#2A2F44", INK, lw=4)
        g.path("M920 1150 L1040 1150 L1010 1060 L950 1060 Z", "#FFD27A", INK, lw=6)
    # floor + rug
    g.rect(-400, fy, W + 800, H - fy + 400, g.lgrad(0, fy, 0, H, "#2B2340", "#1C1730"), None)
    g.line([(-400, fy), (W + 400, fy)], INK, 7)
    g.ellipse(560, fy + 170, 520, 110, "#3E7CB1", INK, lw=7, a=0.85)
    g.ellipse(560, fy + 170, 420, 80, None, "#FFC93C", lw=6, a=0.5)
    # sofa behind the player (low, front view)
    with g.at(780, fy + 40):
        g.rc(0, -250, 640, 230, "#5B3A8C", INK, lw=8, r=40)
        g.rc(0, -120, 680, 150, "#6E4AA3", INK, lw=8, r=30)
        for sd in (-1, 1):
            g.rc(sd * 340, -170, 90, 240, "#56368A", INK, lw=8, r=36)
        with g.at(-170, -250, -0.12):
            g.rc(0, 0, 170, 130, "#FFC93C", INK, lw=7, r=36)
    # TV light on the room (flickers with the game; bright on the crash)
    g.glow(260, 700, 900, "#5EB7FF", (0.16 + 0.05 * math.sin(t * 9)) * glow + 0.25 * flash)
    if flash > 0:
        g.glow(300, 650, 1100, "#FFE7A8", 0.22 * flash)


# ------------------------------------------------------------------ the TV and our own cartoon race on it
def _toy_car(g, x, y, s, col, flip=False, squash=0.0):
    with g.at(x, y, 0, -s if flip else s, s * (1 - squash * 0.3)):
        g.path("M-110 0 L-110 -46 Q-100 -60 -70 -62 L-40 -100 Q-30 -110 10 -110 L50 -110 Q70 -108 84 -84 L100 -62 Q118 -58 118 -40 L118 0 Z",
               col, INK, lw=6)
        g.path("M-30 -66 L-14 -96 L22 -96 L22 -66 Z", "#BFE8FF", INK, lw=5)
        g.path("M34 -66 L34 -96 L54 -96 Q64 -92 74 -70 L76 -66 Z", "#BFE8FF", INK, lw=5)
        g.rect(96, -48, 18, 14, "#FFF4A8", INK, lw=3, r=4)
        for wx in (-64, 66):
            g.circle(wx, 0, 26, "#22263A", INK, lw=6); g.circle(wx, 0, 10, "#C9D2DC", None)


def tv(g, x, y, w, h, t, crash=0.0, k_in=1.0, shake=0.0):
    """Wall TV (centre x, y) showing our own cartoon street race: two toy cars race in from both sides and crash when crash goes 0 -> 1."""
    R = rnd(int(t * 30) + 3).random
    jx, jy = (R() - 0.5) * 18 * shake, (R() - 0.5) * 12 * shake
    with g.at(x, y):
        g.rc(0, 0, w + 44, h + 44, "#0E1020", INK, lw=10, r=18)
        sx0, sy0 = -w / 2, -h / 2
        with g.clip(rect=(sx0, sy0, w, h)):
            g.rect(sx0, sy0, w, h, g.lgrad(0, sy0, 0, sy0 + h, "#2B2F6E", "#B0508A", "#FF9E5E"), None)
            with g.at(jx, jy):
                # skyline + road
                for i in range(10):
                    bh = 60 + ((i * 37) % 90)
                    g.rect(sx0 + i * w / 10, h * 0.12 - bh, w / 10 - 6, bh, "#1E1F4A", None)
                g.rect(sx0, h * 0.12, w, h, "#3A3D55", None)
                off = (t * 900) % 120
                for i in range(-1, 12):
                    g.rect(sx0 + i * 120 - off, h * 0.32, 60, 10, "#FFE7A8", None, a=0.9)
                gap = lerp(1.0, 0.0, ease_out(clamp(crash * 1.6)))
                cy = h * 0.36
                hit = crash > 0.6
                _toy_car(g, -110 * gap - 102 - (0 if not hit else -6), cy, 0.85, "#FF6B5B", squash=0.4 if hit else 0)
                _toy_car(g, 110 * gap + 102 + (0 if not hit else -6), cy, 0.85, "#5ED3B5", flip=True, squash=0.4 if hit else 0)
                if crash > 0.55:
                    kb = clamp((crash - 0.55) / 0.45)
                    burst(g, 0, cy - 60, 30, 70 + 160 * ease_out(kb), 12, "#FFC93C", 12, k=kb)
                    g.circle(0, cy - 60, 50 * back_out(kb), "#FFF4A8", INK, lw=6)
                    Rr = rnd(7).random
                    for i in range(9):
                        a = -math.pi * Rr(); d = 60 + 220 * ease_out(kb)
                        g.rc(d * math.cos(a), cy - 60 + d * math.sin(a), 18, 12, ("#FF6B5B", "#5ED3B5", "#C9D2DC")[i % 3], INK, lw=3, rot=a * 3 + kb * 4)
            g.rect(sx0, sy0, w, h * 0.2, "#FFFFFF", None, a=0.05)
        g.rect(-60, h / 2 + 22, 120, 20, "#0E1020", INK, lw=6)


# ------------------------------------------------------------------ the gamepad
def controller(g, x, y, s=1.0, rot=0.0, shake=0.0, t=0.0, xray=0.0, spin=0.0, heavy_k=1.0, light_k=1.0, glow=None, lit=None):
    """Generic two-grip gamepad (no brand). shake: jitter amount; xray 0..1 fades the shell to show the two rumble motors
    (heavy weight left, light weight right), spinning by angle spin (radians); glow='l'|'r'|'both' highlights motors."""
    R = rnd(int(t * 60) + 11).random
    jx, jy, jr = (R() - 0.5) * 22 * shake, (R() - 0.5) * 14 * shake, (R() - 0.5) * 0.05 * shake
    with g.at(x + jx * s, y + jy * s, rot + jr, s):
        if xray < 1:
            with g.group(1 - 0.75 * xray):
                g.path(PAD_PATH, PAD, INK, lw=10)
                g.path("M-196 -104 Q0 -132 196 -104 Q260 -96 286 -40 Q140 -70 0 -70 Q-140 -70 -286 -40 Q-260 -96 -196 -104 Z", PAD_HI, None)
                # d-pad
                g.rc(-190, -20, 92, 30, "#20263A", INK, lw=5, r=6); g.rc(-190, -20, 30, 92, "#20263A", INK, lw=5, r=6)
                # face buttons (plain, one colour, no letters or symbols)
                for dx, dy in ((0, -40), (40, 0), (0, 40), (-40, 0)):
                    g.circle(190 + dx, -20 + dy, 20, "#E9EEF4", INK, lw=5)
                # sticks
                for sx in (-96, 96):
                    g.circle(sx, 70, 46, "#20263A", INK, lw=6); g.circle(sx, 64, 32, "#3A4260", INK, lw=5)
                g.circle(0, -72, 14, lit or PAL["mint"], INK, lw=4)
        if xray > 0:
            with g.group(xray):
                g.path(PAD_PATH, None, "#9FD8F5", lw=8)
                g.path(PAD_PATH, "#0F2D4A", None, a=0.55)
                # circuit board traces
                g.rc(0, 10, 300, 120, "#1E5A4A", "#5ED3B5", lw=4, r=12, a=0.8)
                for i in range(5):
                    g.line([(-130 + i * 60, -30), (-130 + i * 60, 50)], "#5ED3B5", 3, a=0.6)
                for (mx, my), heavy, kk in ((MOTOR_L, True, heavy_k), (MOTOR_R, False, light_k)):
                    on = glow in ("both", "l" if heavy else "r")
                    if on:
                        g.glow(mx, my, 130, HEAVY if heavy else LIGHTW, 0.55 + 0.25 * math.sin(t * 14))
                    _motor_side(g, mx, my, 0.85, spin * (1.0 if heavy else 1.9), heavy)
                    g.line([(mx * 0.5, my - 30), (mx * 0.2, 20)], "#FF9E5E", 4, a=0.8)


def _motor_side(g, x, y, s, ang, heavy=True):
    """Small rumble motor (side view) with its off-centre weight on the shaft; the weight swings round (ang)."""
    sgn = -1 if x < 0 else 1
    with g.at(x, y, 0, s):
        g.rc(0, 0, 120, 74, STEEL, INK, lw=6, r=14)
        g.rect(-60, -37, 22, 74, COPPER, INK, lw=5, r=6)
        sgn = -sgn                                   # shaft points to the middle of the pad
        sx = sgn * 60
        g.line([(sx, 0), (sx + sgn * 40, 0)], "#E9EEF4", 9)
        r = 62 if heavy else 34
        wx = sx + sgn * 44
        yy = r * math.cos(ang)
        g.line([(wx, 0), (wx, -yy)], HEAVY if heavy else LIGHTW, 34 if heavy else 24)
        g.line([(wx, 0), (wx, -yy)], INK, 3)
        g.circle(wx, -yy, 17 if heavy else 12, HEAVY if heavy else LIGHTW, INK, lw=5)
        g.circle(wx, 0, 7, "#E9EEF4", INK, lw=3)


def hands_on(g, x, y, s, skin="#F3D0B5", sleeve="#FFC93C", rot=0.0, shake=0.0, t=0.0):
    """Two cartoon hands gripping a controller drawn at (x, y, s): thumbs on top, sleeves from below. Draw AFTER controller()."""
    R = rnd(int(t * 60) + 11).random
    jx, jy, jr = (R() - 0.5) * 22 * shake, (R() - 0.5) * 14 * shake, (R() - 0.5) * 0.05 * shake
    with g.at(x + jx * s, y + jy * s, rot + jr, s):
        for sd in (-1, 1):
            g.path(f"M{sd*250} 300 Q{sd*300} 420 {sd*330} 560 L{sd*180} 560 Q{sd*190} 420 {sd*190} 300 Z", sleeve, INK, lw=9)
            g.ellipse(sd * 270, 226, 80, 96, skin, INK, lw=9, rot=sd * 0.35)
            for q in range(3):
                g.ellipse(sd * (226 + q * 24), 150 + q * 6, 18, 30, skin, INK, lw=6, rot=sd * 0.2)
            g.ellipse(sd * 150, 88, 30, 58, skin, INK, lw=8, rot=sd * 1.0)        # thumbs on the sticks
            g.line([(sd * 214, 170), (sd * 300, 150)], shade(skin, -0.15), 5)
            g.line([(sd * 220, 214), (sd * 310, 196)], shade(skin, -0.15), 5)


def rumble_waves(g, x, y, r0, r1, t, k=1.0, col="#FFFFFF", n=3, speed=1.6, w=9, deep=False):
    """Vibration marks round an object: n expanding arcs both sides; deep=True gives slow fat waves, else fast thin ones."""
    if k <= 0: return
    for i in range(n):
        u = (t * speed + i / n) % 1
        r = lerp(r0, r1, u)
        a = k * (1 - u)
        for sd in (-1, 1):
            a0 = (math.pi - 0.6) if sd < 0 else -0.6
            pts = [(x + r * math.cos(a0 + 1.2 * j / 12), y + r * math.sin(a0 + 1.2 * j / 12)) for j in range(13)]
            g.line(pts, col, (w * 2.2 if deep else w), a=a)


def motor_face(g, x, y, r, ang, heavy=True, blur=0.0, label_dot=True):
    """Big end-on view of a rumble motor: round can, shaft in the centre, a half-moon weight that is heavier on one side, turning by ang.
    blur 0..1 adds motion-blur ghosts; the red dot marks the weight's centre (off the shaft)."""
    g.circle(x, y, r * 1.18, "#1B2238", INK, lw=10)
    g.circle(x, y, r * 1.1, STEEL, INK, lw=8)
    g.circle(x, y, r * 0.9, STEEL_D, None, a=0.5)
    col = HEAVY if heavy else LIGHTW
    rr = r * (0.82 if heavy else 0.55)
    for j in range(int(blur * 5), -1, -1):
        a = ang - j * 0.32
        al = 1.0 if j == 0 else 0.22 * blur
        with g.at(x, y, a):
            g.poly([(rr * math.cos(math.pi + math.pi * q / 20), rr * math.sin(math.pi + math.pi * q / 20)) for q in range(21)],
                   col, INK if j == 0 else None, lw=8, a=al)
    with g.at(x, y, ang):
        if label_dot:
            g.circle(0, -rr * 0.42, r * 0.09, "#FF3B3B", INK, lw=4)
    g.circle(x, y, r * 0.12, "#E9EEF4", INK, lw=6)


def coil_actuator(g, x, y, s, t, k=1.0, tap=0.0):
    """Newer 'voice-coil' haptic: copper coil round a magnet; the magnet mass taps back and forth (tap = displacement 0..1)."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 520, 200, "#1B2238", INK, lw=9, r=26)
        for i in range(9):
            g.rc(-200 + i * 50, 0, 34, 170, COPPER, INK, lw=5, r=10)
        dx = 70 * tap
        g.rc(dx, 0, 150, 110, "#D84B5A", INK, lw=7, r=14)
        g.rc(dx - 38, 0, 74, 110, "#3E7CB1", None)
        g.rc(dx, 0, 150, 110, None, INK, lw=7, r=14)
        g.text("N", dx + 38, 4, 54, "#FFFFFF", sw=8)
        g.text("S", dx - 38, 4, 54, "#FFFFFF", sw=8)
