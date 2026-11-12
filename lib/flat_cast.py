"""Style F cast: chunky flat characters (big round head, big white eyes, blush cheeks, bean body, noodle arms) + Wy.
    guy = Char(skin="#E3A679", top="#1D7A8C", hat="headband", beard="#6B3F2A", outfit=[apron("#9A6338")])
    guy.draw(g, t, x, y, sc=1.45, face=1, expr="surprised", arms=("down", "up"), hold=(None, sword))
Feet are at (x, y). Units: head half-width ~104, total height ~430 (x sc). `arms` = (back arm, front arm): a pose name
from ARM, an (x, y) hand position in character units, or amix(a, b, k) to blend. `face` = 1 looks right, -1 left.
Expressions: EXPR keys. Everything is a pure function of t (blinks, breathing), so frames render in any order.
"""
import math
from flat2d import G, INK, PAL, TAU, rgba, mix, shade, clamp, lerp, seg, ease_out, ease_io, back_out, pop, wig

ARM = {"down": (104, -112), "hip": (86, -128), "up": (128, -372), "wave": (142, -356), "point": (192, -232), "point_up": (112, -396),
       "cheek": (88, -300), "head": (44, -432), "forehead": (34, -386), "mouth": (40, -270), "chin": (24, -246), "front": (46, -160),
       "out": (178, -198), "shrug": (136, -252), "hold": (116, -236), "hold_up": (112, -330), "back": (-30, -118), "cover": (8, -340),
       "reach": (176, -300), "low": (120, -70), "belly": (30, -130), "temple": (100, -372), "head2": (86, -414), "sip": (62, -262)}

EXPR = {
    "neutral": dict(eye="open", brow=None, mouth="smile"),
    "happy": dict(eye="open", brow=None, mouth="grin"),
    "joy": dict(eye="happy", brow=None, mouth="grin"),
    "relief": dict(eye="happy", brow=None, mouth="smile"),
    "surprised": dict(eye="wide", brow="up", mouth="o"),
    "shock": dict(eye="wide", brow="up", mouth="open"),
    "worried": dict(eye="open", brow="worry", mouth="frown"),
    "scared": dict(eye="wide", brow="worry", mouth="wavy"),
    "pain": dict(eye="pain", brow="worry", mouth="grit"),
    "angry": dict(eye="open", brow="angry", mouth="frown"),
    "determined": dict(eye="open", brow="angry", mouth="flat"),
    "smug": dict(eye="half", brow="one", mouth="smirk"),
    "sad": dict(eye="open", brow="worry", mouth="frown"),
    "think": dict(eye="open", brow="one", mouth="flat"),
    "confused": dict(eye="open", brow="one", mouth="wavy"),
    "dizzy": dict(eye="dizzy", brow="worry", mouth="wavy"),
    "sleepy": dict(eye="half", brow=None, mouth="flat"),
    "eat": dict(eye="happy", brow=None, mouth="open"),
    "talk": dict(eye="open", brow=None, mouth="talk"),
    "cold": dict(eye="pain", brow="worry", mouth="wavy"),
}


def amix(a, b, k):
    """Blend two arm poses (names or points)."""
    pa = ARM[a] if isinstance(a, str) else a
    pb = ARM[b] if isinstance(b, str) else b
    return (pa[0] + (pb[0] - pa[0]) * k, pa[1] + (pb[1] - pa[1]) * k)


def blink_o(t, seed=0.0):
    p = 3.2 + 1.2 * math.sin(seed * 12.9898 + 1.0)
    ph = (t + seed * 7.31 + 1.1) % p
    d = 0.17
    return abs(2 * ph / d - 1) if ph < d else 1.0


def head_path(rx, ry, kt=0.6, kb=0.6):
    return (f"M0 {-ry} C{kt * rx} {-ry} {rx} {-kt * ry} {rx} 0 C{rx} {kb * ry} {kb * rx} {ry} 0 {ry} "
            f"C{-kb * rx} {ry} {-rx} {kb * ry} {-rx} 0 C{-rx} {-kt * ry} {-kt * rx} {-ry} 0 {-ry} Z")


# ------------------------------------------------------------------ outfit layers (body-local: x -85..85, y -192..0)


def apron(col="#9A6338", strap=None):
    def f(g, ch):
        g.line([(-34, -122), (-26, -190)], INK, 15); g.line([(34, -122), (26, -190)], INK, 15)
        g.line([(-34, -122), (-26, -190)], strap or col, 7); g.line([(34, -122), (26, -190)], strap or col, 7)
        g.rect(-56, -128, 112, 116, col, r=24)
    return f


def collar(col="#FFF4E0"):
    def f(g, ch):
        g.poly([(-40, -196), (0, -150), (40, -196)], col)
    return f


def coat(col="#F6F2EA", shirt="#5ED3B5"):
    def f(g, ch):
        g.poly([(-26, -196), (0, -128), (26, -196)], shirt)
        g.line([(0, -128), (0, -6)], INK, 4.8)
        g.line([(-26, -196), (0, -128), (26, -196)], INK, 4.8)
        for y in (-100, -66, -32):
            g.circle(13, y, 5, shade(col, -0.25), None)
        g.rect(-64, -70, 34, 30, None, INK, lw=3.6, r=5)
    return f


def tie(col="#FF6B5B"):
    def f(g, ch):
        g.poly([(-12, -176), (12, -176), (7, -158), (-7, -158)], col)
        g.poly([(-8, -158), (8, -158), (13, -96), (0, -78), (-13, -96)], col)
    return f


def belt(col="#5A3A2C", buckle="#FFC93C"):
    def f(g, ch):
        g.rect(-86, -54, 172, 22, col, r=4)
        g.rect(-15, -57, 30, 28, buckle, r=5)
    return f


def buttons(col="#FFF4E0", n=3):
    def f(g, ch):
        for i in range(n):
            g.circle(0, -150 + i * 40, 7, col, INK, lw=3.4)
    return f


def badge(x=40, y=-142, r=17):
    def f(g, ch):
        with g.at(x, y, 0, ch.face_dir, 1):
            g.circle(0, 0, r, PAL["yellow"], INK, lw=3.6)
            g.line([(-0.45 * r, 0.02 * r), (-0.10 * r, 0.36 * r), (0.50 * r, -0.34 * r)], INK, r * 0.28)
    return f


def stripes(col="#FFF4E0", n=3):
    def f(g, ch):
        with g.clip(rect=(-82, -192, 164, 190)):
            for i in range(n):
                g.rect(-90, -150 + i * 44, 180, 18, col, None)
    return f


def tunic(col="#8C5A3C", trim="#FFC93C"):
    """Long medieval tunic line + belt."""
    def f(g, ch):
        g.rect(-86, -60, 172, 18, trim, r=4)
        g.line([(0, -186), (0, -70)], shade(col, -0.25), 4)
    return f


def armor(col="#AEB8C2"):
    def f(g, ch):
        g.rect(-70, -182, 140, 120, col, r=(40, 40, 26, 26))
        g.line([(0, -182), (0, -62)], shade(col, -0.3), 4.5)
        g.line([(-66, -120), (66, -120)], shade(col, -0.3), 4.5)
        g.rect(-86, -58, 172, 20, "#5A3A2C", r=4)
    return f


def scarf(col="#FF6B5B"):
    def f(g, ch):
        g.rect(-66, -204, 132, 34, col, r=16)
        g.rect(28, -186, 30, 64, col, r=10)
    return f


# ------------------------------------------------------------------ character


class Char:
    def __init__(s, skin="#E3A679", top="#1D7A8C", legs="#3A3140", shoes="#7A4B2E", hair=None, hair_col="#3B2A20", hat=None, hat_col="#FF6B5B",
                 beard=None, stache=None, glasses=None, outfit=(), head=(104, 98), eye=(20, 27), eye_dx=56, brows=False, cheek="#F0706A",
                 sleeve=None, seed=0.0, body=(170, 192), kt=0.6, kb=0.6, lashes=False, hat2=None):
        s.skin, s.top, s.legs, s.shoes, s.hair, s.hair_col, s.hat, s.hat_col = skin, top, legs, shoes, hair, hair_col, hat, hat_col
        s.beard, s.stache, s.glasses, s.outfit, s.head, s.eye, s.eye_dx, s.brows, s.cheek = beard, stache, glasses, list(outfit), head, eye, eye_dx, brows, cheek
        s.sleeve, s.seed, s.body, s.kt, s.kb, s.lashes, s.hat2 = sleeve or top, seed, body, kt, kb, lashes, hat2 or shade(hat_col, -0.25)
        s.face_dir = 1

    # geometry helpers (character units, feet at 0,0)
    def head_c(s):
        return (0.0, -58 - s.body[1] - 0.80 * s.head[1])

    def hand(s, spec, side):
        """Hand position for an arm spec. side = +1 front arm, -1 back arm."""
        if isinstance(spec, dict): spec = spec["h"]
        p = ARM[spec] if isinstance(spec, str) else spec
        return (p[0] * side, p[1]) if isinstance(spec, str) else p

    def draw(s, g, t, x, y, sc=1.45, face=1, turn=0.3, expr="neutral", look=(0.0, 0.0), arms=("down", "down"), hold=(None, None),
             sq=1.0, lean=0.0, tilt=0.0, lift=0.0, talk=None, shadow=True, shiver=0.0, eye=None, mouth=None, brow=None, blink=True,
             tint=None, alive=True, head_fx=None, body_fx=None, hy=0.0, a=1.0, arm_under=(False, False), sweat=0.0, blush=1.0):
        ph = s.seed * 1.37
        br = math.sin(TAU * 0.33 * t + ph) if alive else 0.0
        if shiver:
            x += shiver * 5.5 * math.sin(TAU * 13 * t + ph)
        if shadow:
            k = 1 - 0.45 * clamp(lift / 260)
            g.ellipse(x, y + 5 * sc, 122 * sc * k, 21 * sc * k, INK, None, a=0.30 * a)
        s.face_dir = face
        lw0 = g.lw
        g.lw = 4.8
        skin = s.skin if tint is None else mix(s.skin, tint[0], tint[1])
        bw, bh = s.body
        sx, sy = sc / math.sqrt(sq), sc * sq
        sh_y = -58 - bh + 34
        with g.at(x, y - lift, lean):
            with g.at(0, 0, 0, sx * face, sy):
                # legs + shoes
                g.rect(-50, -70, 36, 62, s.legs, r=6); g.rect(14, -70, 36, 62, s.legs, r=6)
                g.ellipse(-26, -9, 37, 16, s.shoes); g.ellipse(40, -9, 37, 16, s.shoes)
                for i in (0, 1):
                    if arm_under[i] and arms[i] is not None:
                        s._arm(g, t, arms[i], -1 if i == 0 else 1, sh_y, bw, skin, hold[i])
                # body
                with g.at(0, -58, 0, 1, 1 + 0.014 * br):
                    g.rect(-bw / 2, -bh, bw, bh, s.top, r=(64, 64, 48, 48))
                    for f in s.outfit:
                        f(g, s)
                    with g.clip(rect=(-bw / 2, -bh, bw, bh)):
                        g.ellipse(0, -bh + 6, 80, 30, INK, None, a=0.16)
                    if body_fx: body_fx(g)
                # head
                hx, hyy = s.head_c()
                with g.at(hx + turn * 5, hyy + 2.4 * br + hy, tilt):
                    s._head(g, t, turn, expr, look, skin, talk, eye, mouth, brow, blink, head_fx, sweat, blush)
                # arms on top
                for i in (0, 1):
                    if not arm_under[i] and arms[i] is not None:
                        s._arm(g, t, arms[i], -1 if i == 0 else 1, sh_y, bw, skin, hold[i])
        g.lw = lw0

    def _arm(s, g, t, spec, side, sh_y, bw, skin, hold):
        bend = None
        if isinstance(spec, dict):
            bend = spec.get("bend"); spec = spec["h"]
        hx, hy = s.hand(spec, side)
        x0, y0 = side * (bw / 2 - 17), sh_y
        dx, dy = hx - x0, hy - y0
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        if nx * side + ny * 0.7 < 0: nx, ny = -nx, -ny
        m = clamp((175 - d) / 175, 0.06, 0.62) * 150 if bend is None else bend
        cx, cy = (x0 + hx) / 2 + nx * m, (y0 + hy) / 2 + ny * m
        d_ = f"M{x0} {y0} Q{cx} {cy} {hx} {hy}"
        g.limb(d_, s.sleeve, 37)
        ang = math.atan2(hy - cy, hx - cx)
        if hold:
            fn, mode = hold if isinstance(hold, tuple) else (hold, "up")
            rot = 0.0 if mode == "up" else (ang + TAU / 4 if mode == "arm" else mode)
            with g.at(hx, hy, rot):
                with g.at(0, 0, 0, s.face_dir if mode == "up" else 1, 1):
                    fn(g, t)
        g.circle(hx, hy, 23, skin)

    def _head(s, g, t, turn, expr, look, skin, talk, eye, mouth, brow, blink, head_fx, sweat, blush):
        rx, ry = s.head
        E = EXPR[expr]
        ek, bk, mk = eye or E["eye"], brow if brow is not None else E["brow"], mouth or E["mouth"]
        if bk is None and s.brows: bk = "soft"
        hp = head_path(rx, ry, s.kt, s.kb)
        fx = turn * 22
        # back hair
        if s.hair in ("long", "bob"):
            L = ry * (1.55 if s.hair == "long" else 1.02)
            g.path(f"M{-rx - 10} {-ry * 0.2} C{-rx - 16} {-ry * 1.2} {rx + 16} {-ry * 1.2} {rx + 10} {-ry * 0.2} L{rx + 14} {L} Q0 {L + 22} {-rx - 14} {L} Z", s.hair_col)
        if s.hair == "pony":
            g.path(f"M{-rx * 0.7} {-ry * 0.5} C{-rx * 1.9} {-ry * 0.7} {-rx * 1.8} {ry * 0.9} {-rx * 1.25} {ry * 0.95} C{-rx * 1.3} {ry * 0.2} {-rx * 1.1} {-ry * 0.1} {-rx * 0.7} 0 Z", s.hair_col)
        if s.hair == "bun":
            g.circle(0, -ry - 20, 36, s.hair_col)
        g.path(hp, skin)
        with g.clip(hp):
            if s.beard:
                g.rect(-rx - 8, ry * 0.26, 2 * rx + 16, ry, s.beard, None)
                g.line([(-rx - 8, ry * 0.26), (rx + 8, ry * 0.26)], INK, 3.6)
            if s.cheek and blush > 0:
                for sd in (-1, 1):
                    g.circle(sd * (s.eye_dx + 34) + fx * 0.6, ry * 0.34, 19, s.cheek, None, a=0.55 * blush)
            if s.hair in ("short", "side", "bowl", "long", "bob", "pony", "bun", "spiky", "curly"):
                yb = -ry * 0.36
                if s.hair == "bowl":
                    g.path(f"M{-rx - 9} {-ry - 9} L{rx + 9} {-ry - 9} L{rx + 9} {yb} L{-rx - 9} {yb} Z", s.hair_col)
                elif s.hair == "side":
                    g.path(f"M{-rx - 9} {-ry - 9} L{rx + 9} {-ry - 9} L{rx + 9} {yb + 26} Q{rx * 0.3} {yb + 8} {-rx * 0.35} {-ry * 0.82} Q{-rx * 0.7} {yb - 6} {-rx - 9} {yb + 12} Z", s.hair_col)
                else:
                    g.path(f"M{-rx - 9} {-ry - 9} L{rx + 9} {-ry - 9} L{rx + 9} {yb + 18} Q{rx * 0.55} {yb - 22} {rx * 0.1} {yb - 4} Q{-rx * 0.45} {yb - 30} {-rx - 9} {yb + 18} Z", s.hair_col)
            if head_fx:
                head_fx(g)
            g.line(f"M{-rx * 0.66} {-ry * 0.46} Q{-rx * 0.5} {-ry * 0.78} {-rx * 0.14} {-ry * 0.84}", "#FFFFFF", 9, a=0.32)
        g.path(hp, None, INK)
        # hair on top / hats
        if s.hair == "tuft":
            g.path(f"M-22 {-ry + 6} Q-30 {-ry - 34} -6 {-ry - 22} Q2 {-ry - 52} 18 {-ry - 20} Q36 {-ry - 30} 26 {-ry + 8} Z", s.hair_col)
        elif s.hair == "spiky":
            pts = []
            for i in range(9):
                a0 = math.radians(200 + i * 17.5)
                r_ = (1.0 if i % 2 == 0 else 1.26)
                pts.append((rx * r_ * math.cos(a0), ry * r_ * math.sin(a0) + (8 if i % 2 == 0 else 0)))
            g.poly(pts, s.hair_col, r=5)
        elif s.hair == "curly":
            for i in range(7):
                a0 = math.radians(196 + i * 24.5)
                g.circle(rx * 0.96 * math.cos(a0), ry * 0.96 * math.sin(a0), 27, s.hair_col)
        elif s.hair == "curl":  # Wy's question-mark curl (logo)
            d_ = "M-41 -110 C-41 -155 46 -159 46 -116 C46 -90 10 -90 5 -58"
            g.line(d_, INK, 27); g.line(d_, s.hair_col, 15)
        if s.hat:
            s._hat(g, rx, ry, turn)
        # ---- face
        ex, ey = s.eye
        blk = blink_o(t, s.seed) if blink else 1.0
        for sd in (-1, 1):
            cx, cy = sd * s.eye_dx + fx, -ry * 0.06
            _eye(g, ek, cx, cy, ex, ey, sd, look, blk, skin, t, s.lashes)
            _brow(g, bk, cx, cy - ey - 13, ex, sd)
        if s.glasses:
            for sd in (-1, 1):
                g.circle(sd * s.eye_dx + fx, -ry * 0.06, ey + 9, None, s.glasses, lw=6)
            g.line([(-s.eye_dx + ey + 9 + fx, -ry * 0.06), (s.eye_dx - ey - 9 + fx, -ry * 0.06)], s.glasses, 6)
        mx, my = fx * 1.15, ry * 0.46
        if s.stache:
            g.path(f"M{mx - 40} {my - 8} Q{mx - 20} {my - 34} {mx} {my - 16} Q{mx + 20} {my - 34} {mx + 40} {my - 8} Q{mx + 18} {my - 2} {mx} {my - 8} Q{mx - 18} {my - 2} {mx - 40} {my - 8} Z", s.stache)
            my += 12
        _mouth(g, mk, mx, my, talk)
        if sweat > 0:
            k = (t * 0.9) % 1.0
            g.path(f"M{rx * 0.72} {-ry * 0.5 + 60 * k} q-13 20 0 30 q13 -10 0 -30 Z", "#8FD8FF", INK, lw=3.4, a=sweat * (1 - k))

    def _hat(s, g, rx, ry, turn):
        h, c1, c2 = s.hat, s.hat_col, s.hat2
        if h == "headband":
            g.rect(-rx - 7, -ry * 0.56, 2 * rx + 14, 25, c1, r=10)
            g.rect(rx * 0.45, -ry * 0.56 + 6, rx * 0.4, 7, shade(c1, 0.45), None, r=4)
        elif h == "beanie":
            g.path(f"M{-rx - 4} {-ry * 0.42} C{-rx - 8} {-ry * 1.5} {rx + 8} {-ry * 1.5} {rx + 4} {-ry * 0.42} Z", c1)
            g.rect(-rx - 12, -ry * 0.62, 2 * rx + 24, 36, c2, r=16)
            g.circle(0, -ry * 1.22, 21, c2)
        elif h == "cap":
            g.path(f"M{-rx - 2} {-ry * 0.46} C{-rx - 6} {-ry * 1.42} {rx + 6} {-ry * 1.42} {rx + 2} {-ry * 0.46} Z", c1)
            g.path(f"M{rx * 0.1} {-ry * 0.5} L{rx + 62} {-ry * 0.46} Q{rx + 70} {-ry * 0.28} {rx + 40} {-ry * 0.3} L{rx * 0.1} {-ry * 0.36} Z", c2)
        elif h == "pilot":
            g.path(f"M{-rx - 6} {-ry * 0.60} C{-rx - 22} {-ry * 1.5} {rx + 22} {-ry * 1.5} {rx + 6} {-ry * 0.60} Z", c1)
            g.rect(-rx - 8, -ry * 0.70, 2 * rx + 16, 24, c2, r=6)
            g.path(f"M{-rx * 0.2} {-ry * 0.5} L{rx + 46} {-ry * 0.5} Q{rx + 54} {-ry * 0.32} {rx + 26} {-ry * 0.34} L{-rx * 0.2} {-ry * 0.36} Z", INK)
            g.circle(turn * 20, -ry * 1.02, 15, PAL["yellow"], INK, lw=3.6)
        elif h == "hardhat":
            g.path(f"M{-rx - 4} {-ry * 0.5} C{-rx - 4} {-ry * 1.55} {rx + 4} {-ry * 1.55} {rx + 4} {-ry * 0.5} Z", c1)
            g.rect(-rx - 20, -ry * 0.58, 2 * rx + 40, 22, c1, r=10)
            g.rect(-13, -ry * 1.33, 26, ry * 0.76, shade(c1, 0.25), INK, lw=3.6, r=10)
        elif h == "helmet":  # medieval kettle hat
            g.path(f"M{-rx - 2} {-ry * 0.5} C{-rx * 0.96} {-ry * 1.5} {rx * 0.96} {-ry * 1.5} {rx + 2} {-ry * 0.5} Z", c1)
            g.path(f"M{-rx - 34} {-ry * 0.46} Q0 {-ry * 0.78} {rx + 34} {-ry * 0.46} Q0 {-ry * 0.36} {-rx - 34} {-ry * 0.46} Z", c1)
            g.line([(0, -ry * 1.24), (0, -ry * 0.66)], shade(c1, -0.3), 4)
        elif h == "crown":
            g.path(f"M{-rx * 0.72} {-ry * 0.74} L{-rx * 0.84} {-ry * 1.42} L{-rx * 0.36} {-ry * 1.08} L0 {-ry * 1.56} L{rx * 0.36} {-ry * 1.08} L{rx * 0.84} {-ry * 1.42} L{rx * 0.72} {-ry * 0.74} Z", c1)
            for i in (-1, 0, 1):
                g.circle(i * rx * 0.4, -ry * 0.9, 9, PAL["coral"], INK, lw=3)
        elif h == "tophat":
            g.rect(-rx * 0.62, -ry * 2.02, rx * 1.24, ry * 1.2, c1, r=8)
            g.rect(-rx * 0.62, -ry * 1.12, rx * 1.24, 22, c2, None)
            g.rect(-rx * 1.0, -ry * 0.9, rx * 2.0, 24, c1, r=11)
        elif h == "chef":
            for dx_, dy_, r_ in ((-46, -1.3, 44), (46, -1.3, 44), (0, -1.5, 54)):
                g.circle(dx_, ry * dy_, r_, c1)
            g.rect(-rx * 0.74, -ry * 1.22, rx * 1.48, ry * 0.52, c1, r=6)
        elif h == "goggles":  # leather flying cap with goggles
            g.path(f"M{-rx - 5} {-ry * 0.2} C{-rx - 10} {-ry * 1.36} {rx + 10} {-ry * 1.36} {rx + 5} {-ry * 0.2} L{rx - 6} {-ry * 0.36} Q0 {-ry * 0.74} {-rx + 6} {-ry * 0.36} Z", c1)
            for sd in (-1, 1):
                g.circle(sd * 40 + turn * 14, -ry * 0.82, 27, "#9FD8E8", INK)
            g.line([(-13 + turn * 14, -ry * 0.82), (13 + turn * 14, -ry * 0.82)], INK, 7)


def _eye(g, kind, cx, cy, rx, ry, sd, look, blk, skin, t, lashes=False):
    if kind == "happy":
        g.line(f"M{cx - rx} {cy + 6} Q{cx} {cy - ry * 1.0} {cx + rx} {cy + 6}", INK, 7)
        return
    if kind == "shut":
        g.line(f"M{cx - rx} {cy - 2} Q{cx} {cy + ry * 0.55} {cx + rx} {cy - 2}", INK, 7)
        return
    if kind == "pain":
        g.line([(cx - sd * rx * 0.95, cy - ry * 0.55), (cx + sd * rx * 0.75, cy), (cx - sd * rx * 0.95, cy + ry * 0.55)], INK, 7.5)
        return
    if kind == "dizzy":
        pts = []
        for i in range(40):
            a0 = i / 39 * TAU * 2.2 + t * 5 * sd
            r_ = 3 + (rx + 3) * i / 39
            pts.append((cx + r_ * math.cos(a0), cy + r_ * math.sin(a0)))
        g.circle(cx, cy, rx + 7, "#FFFFFF", INK)
        g.line(pts, INK, 4.5)
        return
    wide = kind == "wide"
    rx2, ry2 = (rx * 1.12, ry * 1.14) if wide else (rx, ry)
    if blk < 0.22:
        g.line(f"M{cx - rx2} {cy} Q{cx} {cy + 7} {cx + rx2} {cy}", INK, 6.5)
        return
    ry3 = ry2 * (0.25 + 0.75 * blk)
    g.ellipse(cx, cy, rx2, ry3, "#FFFFFF")
    pr = rx * (0.56 if wide else 0.66)
    px, py = cx + look[0] * rx * 0.36, cy + look[1] * ry * 0.34
    with g.clip(ellipse=(cx, cy, rx2, ry3)):
        g.circle(px, py, pr, INK, None)
        g.circle(px - pr * 0.34, py - pr * 0.38, pr * 0.36, "#FFFFFF", None)
        if kind == "half":
            g.rect(cx - rx2 - 4, cy - ry3 - 4, 2 * rx2 + 8, ry3 * 0.95, skin, None)
            g.line([(cx - rx2 - 2, cy - ry3 * 0.08), (cx + rx2 + 2, cy - ry3 * 0.08)], INK, 5.5)
    g.ellipse(cx, cy, rx2, ry3, None, INK)
    if lashes:
        g.line([(cx + sd * rx2 * 0.8, cy - ry3 * 0.7), (cx + sd * (rx2 + 12), cy - ry3 - 8)], INK, 5)


def _brow(g, kind, cx, cy, rx, sd):
    if kind is None:
        return
    w = rx * 1.15
    if kind == "soft":
        g.line(f"M{cx - w} {cy + 4} Q{cx} {cy - 9} {cx + w} {cy + 4}", INK, 7)
    elif kind == "up":
        g.line(f"M{cx - w} {cy - 8} Q{cx} {cy - 24} {cx + w} {cy - 8}", INK, 7)
    elif kind == "worry":   # inner end up
        g.line([(cx - sd * w, cy - 14), (cx + sd * w, cy + 4)], INK, 7.5)
    elif kind == "angry":   # inner end down
        g.line([(cx - sd * w, cy + 12), (cx + sd * w, cy - 10)], INK, 7.5)
    elif kind == "one":
        if sd > 0: g.line(f"M{cx - w} {cy - 12} Q{cx} {cy - 28} {cx + w} {cy - 14}", INK, 7)
        else: g.line([(cx - w, cy + 4), (cx + w, cy + 4)], INK, 7)


MOUTH_IN, TONGUE = "#7A2230", "#F0808A"


def _mouth(g, kind, x, y, talk=None):
    if talk is not None and kind in ("smile", "grin", "talk"):
        kind = "talk"
    if kind == "smile":
        g.line(f"M{x - 19} {y - 5} Q{x} {y + 15} {x + 19} {y - 5}", INK, 6.5)
    elif kind == "grin":
        d = f"M{x - 27} {y - 9} Q{x} {y + 34} {x + 27} {y - 9} Q{x} {y} {x - 27} {y - 9} Z"
        g.path(d, MOUTH_IN)
        with g.clip(d):
            g.ellipse(x, y + 20, 15, 9, TONGUE, None)
        g.path(d, None, INK)
    elif kind in ("o", "open", "talk"):
        k = clamp(talk if talk is not None else 0.6)
        rx, ry = (13, 15) if kind == "o" else (21, 25) if kind == "open" else (13 + 7 * k, 4 + 19 * k)
        if kind == "talk" and k < 0.08:
            g.line(f"M{x - 19} {y - 5} Q{x} {y + 13} {x + 19} {y - 5}", INK, 6.5)
            return
        g.ellipse(x, y + 2, rx, ry, MOUTH_IN)
        if ry > 12:
            with g.clip(ellipse=(x, y + 2, rx, ry)):
                g.ellipse(x, y + 2 + ry * 0.78, rx * 0.8, ry * 0.5, TONGUE, None)
            g.ellipse(x, y + 2, rx, ry, None, INK)
    elif kind == "frown":
        g.line(f"M{x - 18} {y + 9} Q{x} {y - 9} {x + 18} {y + 9}", INK, 6.5)
    elif kind == "flat":
        g.line([(x - 15, y + 2), (x + 15, y + 2)], INK, 6.5)
    elif kind == "grit":
        g.rect(x - 27, y - 11, 54, 25, "#FFFFFF", r=10)
        g.line([(x - 26, y + 1.5), (x + 26, y + 1.5)], INK, 3.4)
        for dx in (-13, 0, 13):
            g.line([(x + dx, y - 9), (x + dx, y + 12)], INK, 3.4)
    elif kind == "wavy":
        g.line(f"M{x - 24} {y + 3} q6 -12 12 0 t12 0 t12 0 t12 0", INK, 6.5)
    elif kind == "smirk":
        g.line(f"M{x - 13} {y + 3} Q{x + 6} {y + 11} {x + 21} {y - 8}", INK, 6.5)
    elif kind == "tongue":
        g.line(f"M{x - 19} {y - 5} Q{x} {y + 15} {x + 19} {y - 5}", INK, 6.5)
        g.path(f"M{x - 2} {y + 6} q-2 22 9 22 q11 0 9 -22 Z", TONGUE, INK, lw=3.6)


# ------------------------------------------------------------------ Wy (mascot): full body + logo bust


WY = Char(skin="#F4C6A0", top="#FF6B5B", legs="#10263B", shoes="#5B3A29", hair="curl", hair_col="#5B3A29", outfit=[collar(), badge()],
          head=(108, 96), eye=(24, 32), eye_dx=44, brows=True, cheek="#F2918A", kt=0.64, kb=0.58, seed=0.3)


def wy_bust(g, t, x, y, s=1.0, talk=0.0, sq=1.0, look=(0.25, -0.3)):
    """Wy exactly as in branding/TrueWhys_logo.svg (head + shoulders); bottom centre of the shirt at x, y. Blinks, talks."""
    lw0 = g.lw
    bob = 3 * math.sin(TAU * 0.4 * t)
    with g.at(x, y, 0, s / math.sqrt(sq), s * sq):
        with g.at(-200, -470):
            g.path("M95 560 L95 470 Q95 372 200 365 Q305 372 305 470 L305 560 Z", "#FF6B5B", INK, lw=11)
            g.path("M160 372 L200 410 L240 372", "#FFF4E0", INK, lw=9)
            with g.at(0, bob):
                d_ = "M140 74 C140 8 268 2 268 66 C268 104 214 104 208 150"
                g.line(d_, INK, 40); g.line(d_, "#5B3A29", 22)
                g.path("M200 98 C300 98 352 160 352 232 C352 312 288 372 200 372 C112 372 48 312 48 232 C48 160 100 98 200 98 Z", "#F4C6A0", INK, lw=12)
                g.line("M120 140 Q150 116 190 112", "#FFFFFF", 12, a=0.45)
                g.line("M108 168 Q138 146 170 160", INK, 11); g.line("M232 156 Q264 140 294 162", INK, 11)
                blk = blink_o(t, 0.3)
                for ex in (142, 262):
                    if blk < 0.22:
                        g.line(f"M{ex - 36} 226 Q{ex} 238 {ex + 36} 226", INK, 10)
                    else:
                        ry = 48 * (0.25 + 0.75 * blk)
                        g.ellipse(ex, 226, 36, ry, "#FFFFFF", INK, lw=9)
                        with g.clip(ellipse=(ex, 226, 36, ry)):
                            px, py = ex + 8 + (look[0] - 0.25) * 14, 216 + (look[1] + 0.3) * 14
                            g.circle(px, py, 21, INK, None); g.circle(px + 8, py - 10, 7.5, "#FFFFFF", None)
                        g.ellipse(ex, 226, 36, ry, None, INK, lw=9)
                g.ellipse(96, 292, 26, 16, "#F2918A", None, a=0.8); g.ellipse(306, 292, 26, 16, "#F2918A", None, a=0.8)
                k = clamp(0.5 + 0.9 * (talk - 0.25)) if talk > 0.02 else 0.5
                lo, up = 322 + 36 * k, 312 - 4 * k
                d_ = f"M168 300 Q200 {lo} 232 300 Q200 {up} 168 300 Z"
                g.path(d_, "#8A2734", INK, lw=9)
                with g.clip(d_):
                    g.ellipse(200, lo - 12, 20, 9, "#E8707A", None)
    g.lw = lw0
