"""Reusable Style F props for psychology / brain scenes (B-006, 24 Nov 2026). Design units, Style F engine (lib/flat2d.py).

    from flat_brain import brain, doorway, thought, phone, buzz, socket, note, headphones, gum, book, pie, mri, meg_helmet,
                           house_face, car_face, cloud_face, pizza_face, vr_grid, party_crowd, sound_wave, aglet_lace, clock_face
All props are drawn around (x, y) with scale s and use the brand ink outline. Listed in library/index.md.
"""
import math
from flat2d import *

PINK, PINK_D = "#F7A9BC", "#E07A95"
WOOD, WOOD_D = "#B97A4A", "#8A5530"


# ------------------------------------------------------------------ the brain mascot
def brain(g, x, y, s=1.0, expr="happy", t=0.0, rot=0.0, glow=0.0, look=(0, 0), squash=0.0):
    """Cartoon brain with a face. expr: happy | alarm | confused | smug | shout | sleepy | worried. ~300 units wide at s=1."""
    with g.at(x, y, rot, s * (1 + squash * 0.5), s * (1 - squash)):
        if glow > 0:
            g.glow(0, 0, 320, PAL["yellow"], 0.5 * glow)
        # outline lobes
        lobes = [(-95, -40, 85), (-30, -80, 90), (55, -70, 88), (110, -10, 75), (70, 55, 80), (-20, 60, 85), (-105, 35, 72)]
        for lx, ly, r in lobes:
            g.circle(lx, ly, r + 7, INK, None)
        for lx, ly, r in lobes:
            g.circle(lx, ly, r, PINK, None)
        g.circle(0, -5, 120, PINK, None)
        # folds (gyri)
        for d in ("M-150 -30 Q-110 -60 -80 -20 Q-60 10 -100 40", "M-60 -130 Q-40 -90 -70 -60", "M20 -140 Q0 -100 30 -80 Q60 -60 40 -30",
                  "M120 -80 Q90 -50 130 -20", "M150 30 Q110 40 110 80", "M-40 120 Q-20 80 20 100", "M60 120 Q50 90 80 70"):
            g.line(d, PINK_D, 9)
        g.line("M0 -150 Q-10 -60 6 20", PINK_D, 8)
        # face
        ex = 34
        lx, ly = look
        if expr in ("happy", "smug"):
            for sx in (-1, 1):
                g.line(f"M{sx * ex - 20} 0 Q{sx * ex} -24 {sx * ex + 20} 0", INK, 9)
            if expr == "smug":
                g.line("M-30 50 Q0 66 34 40", INK, 8)
            else:
                g.path("M-36 40 Q0 92 36 40 Q0 54 -36 40 Z", "#7A2230", INK, lw=6)
        elif expr == "sleepy":
            for sx in (-1, 1):
                g.line([(sx * ex - 20, 2), (sx * ex + 20, 2)], INK, 8)
            g.ellipse(0, 52, 14, 10, "#7A2230", INK, lw=5)
        else:
            big = expr in ("alarm", "shout")
            ry = 34 if big else 27
            for sx in (-1, 1):
                g.ellipse(sx * ex, -4, 24, ry, "#FFFFFF", INK, lw=6)
                g.circle(sx * ex + 6 * lx, -2 + 6 * ly, 11 if big else 13, INK, None)
                g.circle(sx * ex + 6 * lx - 4, -7 + 6 * ly, 4, "#FFFFFF", None)
            if expr == "confused":
                g.line([(-ex - 22, -50), (-ex + 18, -40)], INK, 8); g.line([(ex - 18, -48), (ex + 22, -60)], INK, 8)
                g.line("M-26 56 q9 -12 18 0 t18 0 t18 0", INK, 7)
            elif expr == "worried":
                g.line([(-ex - 20, -40), (-ex + 18, -52)], INK, 8); g.line([(ex - 18, -52), (ex + 20, -40)], INK, 8)
                g.line("M-24 62 Q0 44 24 62", INK, 7)
            elif expr == "shout":
                g.line([(-ex - 22, -56), (-ex + 18, -44)], INK, 8); g.line([(ex - 18, -44), (ex + 22, -56)], INK, 8)
                o = 1 + 0.12 * math.sin(t * 30)
                g.ellipse(0, 60, 30 * o, 34 * o, "#7A2230", INK, lw=6)
            else:  # alarm
                g.ellipse(0, 56, 16, 20, "#7A2230", INK, lw=6)


# ------------------------------------------------------------------ rooms and doors
def doorway(g, x, y, s=1.0, open_k=1.0, wall="#E9DCC6", door="#B97A4A", inside="#3A3550", light=0.0):
    """Door frame standing on the floor at (x, y) (bottom centre); 260 x 520 units at s=1. open_k 0 closed .. 1 open."""
    with g.at(x, y, 0, s):
        g.rect(-150, -540, 300, 540, shade(wall, 0.8), INK, lw=8)
        g.rect(-130, -520, 260, 520, inside, INK, lw=7)
        if light > 0:
            g.glow(0, -260, 260, "#FFE08A", 0.35 * light)
        w = 260 * (1 - 0.82 * clamp(open_k))
        g.poly([(-130, -520), (-130 + w, -520 + 30 * open_k), (-130 + w, 0 - 0 * open_k), (-130, 0)], door, INK, lw=7)
        if w > 60:
            g.circle(-130 + w - 26, -250, 11, PAL["yellow"], INK, lw=4)


def thought(g, x, y, w, h, k=1.0, fill="#FFFFFF", tail=(-1, 1)):
    """Thought cloud centred at (x, y) with two small bubbles towards `tail` direction; k 0..1 grows it in."""
    if k <= 0: return
    kk = back_out(clamp(k), 1.6)
    with g.at(x, y, 0, kk):
        n = 9
        for i in range(n):
            a = i / n * TAU
            g.circle(w * 0.42 * math.cos(a), h * 0.42 * math.sin(a), h * 0.26 + 6, INK, None)
        for i in range(n):
            a = i / n * TAU
            g.circle(w * 0.42 * math.cos(a), h * 0.42 * math.sin(a), h * 0.26, fill, None)
        g.ellipse(0, 0, w * 0.45, h * 0.42, fill, None)
        tx, ty = tail
        g.circle(tx * w * 0.45, ty * h * 0.62, h * 0.09, fill, INK, lw=6)
        g.circle(tx * w * 0.58, ty * h * 0.82, h * 0.055, fill, INK, lw=5)


def vr_grid(g, t, x0=0, y0=0, w=1920, h=1080, col="#5ED3B5", bg="#0B1F33", horizon=0.42):
    """Wire-frame 'virtual room' floor and walls (a simple video-game look)."""
    g.fill_all(g.lgrad(0, 0, 0, h, bg, shade(bg, 1.25)))
    hy = y0 + h * horizon
    vx = x0 + w / 2
    for i in range(-14, 15):
        g.line([(vx + i * 30, hy), (vx + i * 260, y0 + h + 40)], col, 3, a=0.55)
    for j in range(1, 12):
        yy = hy + (h - h * horizon) * (j / 11) ** 1.8
        g.line([(x0 - 40, yy), (x0 + w + 40, yy)], col, 3, a=0.55)
    for i in range(0, 9):
        xx = x0 + w * i / 8
        g.line([(xx, y0), (xx, hy)], col, 2, a=0.25)
    g.line([(x0 - 40, hy), (x0 + w + 40, hy)], col, 5, a=0.8)


# ------------------------------------------------------------------ phone and buzzing
def phone(g, x, y, s=1.0, rot=0.0, screen="#1E2A3A", lit=0.0, icon=None, case="#2A2A38"):
    """Generic smartphone (no logo), 140 x 280 units at s=1."""
    with g.at(x, y, rot, s):
        g.rc(0, 0, 150, 290, case, INK, lw=8, r=26)
        g.rc(0, 0, 124, 250, mix(screen, "#BDEBFF", lit), None, r=14)
        g.rc(0, -112, 40, 10, INK, None, r=5)
        if icon == "none" and lit > 0.3:
            g.text("0", 0, -20, 70, "#FFFFFF", stroke=None, a=lit)
            g.text("NEW", 0, 40, 30, "#FFFFFF", stroke=None, a=lit)
        elif icon == "msg" and lit > 0.3:
            g.rc(0, -10, 90, 60, "#5ED3B5", INK, lw=5, r=12)
            g.poly([(-20, 18), (-34, 40), (0, 20)], "#5ED3B5", INK, lw=4)


def buzz(g, x, y, r, t, k=1.0, col=None):
    """Vibration marks: short zig-zag arcs on both sides of (x, y)."""
    if k <= 0: return
    col = col or PAL["yellow"]
    for side in (-1, 1):
        for j in range(3):
            rr = r + j * 34 + 10 * math.sin(t * 40 + j)
            pts = []
            for q in range(7):
                a = -0.6 + 1.2 * q / 6
                rq = rr + (8 if q % 2 else -8)
                pts.append((x + side * rq * math.cos(a), y + rq * math.sin(a)))
            g.line(pts, col, 9 - j * 2, a=k * (1 - j * 0.25))


def sound_wave(g, x, y, r0, r1, t, col="#FFFFFF", n=3, a=0.8, ang=0.0, spread=0.7, speed=1.0):
    """Expanding arcs (sound travelling) from (x, y) towards angle `ang`."""
    for j in range(n):
        u = ((t * speed) + j / n) % 1.0
        r = lerp(r0, r1, u)
        pts = [(x + r * math.cos(ang + spread * (q / 10 - 0.5) * 2), y + r * math.sin(ang + spread * (q / 10 - 0.5) * 2)) for q in range(11)]
        g.line(pts, col, 9, a=a * (1 - u))


# ------------------------------------------------------------------ music
def note(g, x, y, s=1.0, col=None, rot=0.0, double=False):
    col = col or PAL["yellow"]
    with g.at(x, y, rot, s):
        g.ellipse(-20, 40, 28, 20, col, INK, lw=6, rot=-0.4)
        g.line([(4, 32), (4, -60)], INK, 10)
        if double:
            g.ellipse(70, 26, 28, 20, col, INK, lw=6, rot=-0.4)
            g.line([(94, 18), (94, -74)], INK, 10)
            g.poly([(4, -60), (94, -74), (94, -50), (4, -36)], INK, None)
        else:
            g.path("M4 -60 Q40 -40 34 0 Q30 -30 4 -36 Z", INK, None)


def headphones(g, x, y, s=1.0, col="#2A2A38", left="#5ED3B5", right="#FF6B5B"):
    """Front view headphones, 300 wide; ear cups coloured left/right (two different messages)."""
    with g.at(x, y, 0, s):
        g.line("M-130 10 Q-130 -150 0 -150 Q130 -150 130 10", INK, 30)
        g.line("M-130 10 Q-130 -150 0 -150 Q130 -150 130 10", col, 18)
        g.rc(-140, 40, 70, 120, left, INK, lw=8, r=28)
        g.rc(140, 40, 70, 120, right, INK, lw=8, r=28)


def gum(g, x, y, s=1.0, rot=0.0, col="#5ED3B5", out=0.5):
    """A pack of chewing gum (generic, no brand) with one pink stick sliding out by `out` (0..1)."""
    with g.at(x, y, rot, s):
        g.rc(70 + 120 * out, -10, 200, 50, "#F7A9BC", INK, lw=6, r=8)          # the stick
        g.line([(10 + 120 * out, -10), (130 + 120 * out, -10)], "#E07A95", 4)
        g.rc(0, 0, 240, 110, col, INK, lw=8, r=14)                             # the pack
        g.rect(-120, -20, 240, 40, "#FFFFFF", INK, lw=5)
        g.text("GUM", 0, 2, 34, INK, stroke=None)
        g.rc(120, 0, 16, 110, shade(col, 0.75), INK, lw=5, r=4)


# ------------------------------------------------------------------ words and books
def book(g, x, y, s=1.0, col="#3E7CB1", rot=0.0, gap=False):
    """Book spine standing (60 x 240). gap=True draws an empty slot instead (the book is out on loan)."""
    with g.at(x, y, rot, s):
        if gap:
            g.rc(0, 0, 60, 240, "#22181B", None, r=4, a=0.35)
            return
        g.rc(0, 0, 60, 240, col, INK, lw=6, r=6)
        g.line([(-30, -80), (30, -80)], shade(col, 0.7), 6); g.line([(-30, 80), (30, 80)], shade(col, 0.7), 6)


def library_card(g, x, y, s=1.0, rot=0.0, txt="MEANING"):
    with g.at(x, y, rot, s):
        g.rc(0, 0, 320, 200, "#FFF4E0", INK, lw=8, r=12)
        g.rect(-160, -100, 320, 46, "#FF6B5B", INK, lw=6)
        for i in range(3):
            g.line([(-130, -10 + i * 36), (130 - 60 * (i == 2), -10 + i * 36)], "#9AA3AD", 5)
        g.text(txt, 0, -76, 30, "#FFFFFF", stroke=None)


def aglet_lace(g, x, y, s=1.0, rot=0.0, glow=0.0):
    """Shoelace end with its plastic tip (aglet) highlighted."""
    with g.at(x, y, rot, s):
        g.line("M-300 40 Q-160 -40 -40 0", INK, 30)
        g.line("M-300 40 Q-160 -40 -40 0", "#FFFFFF", 20)
        if glow > 0:
            g.glow(40, 0, 140, PAL["yellow"], 0.6 * glow)
        g.rc(30, 0, 150, 34, "#BDEBFF", INK, lw=7, r=14)
        g.line([(-30, -8), (100, -8)], "#FFFFFF", 5, a=0.8)


def pie(g, x, y, r, frac, col=None, k=1.0, bg="#22181B", label=None, size=None):
    """Pie chart filling clockwise from 12 o'clock up to frac*k."""
    col = col or PAL["yellow"]
    g.circle(x, y, r, shade(bg, 1.3), INK, lw=8)
    f = clamp(frac * k)
    if f > 0.003:
        pts = [(x, y)] + [(x + r * math.sin(TAU * f * q / 48), y - r * math.cos(TAU * f * q / 48)) for q in range(49)]
        g.poly(pts, col, INK, lw=6)
    if label:
        g.text(label, x, y + r + (size or r * 0.5) * 0.9, size or r * 0.5, "#FFFFFF", sw=(size or r * 0.5) * 0.2)


def clock_face(g, x, y, r, t=0.0, speed=1.0):
    g.circle(x, y, r, "#F4F1EA", INK, lw=8)
    a1 = t * speed; a2 = t * speed / 12
    g.line([(x, y), (x + r * 0.75 * math.sin(a1), y - r * 0.75 * math.cos(a1))], INK, 7)
    g.line([(x, y), (x + r * 0.5 * math.sin(a2), y - r * 0.5 * math.cos(a2))], INK, 9)
    g.circle(x, y, 8, INK, None)


# ------------------------------------------------------------------ brain scanners
def mri(g, x, y, s=1.0, slide=0.0, glow=0.0):
    """Side view of a scanner ring with a sliding bed (no brand marks)."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 520, 520, "#E6ECF0", INK, lw=10, r=120)
        g.circle(0, 0, 170, "#22303A", INK, lw=10)
        if glow > 0:
            g.circle(0, 0, 150, None, "#5ED3B5", lw=12, a=glow)
        g.rc(-120 + 300 * (1 - slide), 120, 700, 40, "#9AA3AD", INK, lw=7, r=10)
        g.rc(0, 230, 360, 60, "#C9D3DA", INK, lw=7, r=10)


def meg_helmet(g, x, y, s=1.0, glow=0.0, t=0.0):
    """Big dome helmet over a head (MEG scanner), seen from the front."""
    with g.at(x, y, 0, s):
        g.path("M-190 60 Q-200 -230 0 -240 Q200 -230 190 60 Z", "#D8DEE4", INK, lw=10)
        g.line("M-190 60 L190 60", INK, 10)
        for i in range(-3, 4):
            g.circle(i * 48, -120 - 40 * math.cos(i * 0.4), 12, "#5ED3B5" if glow > 0 else "#9AA3AD", INK, lw=4,
                     a=1.0 if glow <= 0 else 0.5 + 0.5 * math.sin(t * 8 + i))
        g.rc(0, -420, 120, 200, "#9AA3AD", INK, lw=8, r=20)


# ------------------------------------------------------------------ faces in things (pareidolia)
def socket(g, x, y, s=1.0, face=0.0, plate="#F4F1EA"):
    """Wall power socket: two slots + a round hole underneath read as a surprised face. face 0..1 adds a soft highlight."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 260, 260, plate, INK, lw=9, r=36)
        g.rc(0, 0, 200, 200, mix(plate, "#FFFFFF", 0.5), INK, lw=5, r=28)
        if face > 0:
            g.glow(0, 0, 160, PAL["yellow"], 0.35 * face)
        g.rc(-40, -30, 22, 64, INK, None, r=8)
        g.rc(40, -30, 22, 64, INK, None, r=8)
        g.path("M-20 60 Q-20 30 0 30 Q20 30 20 60 L20 72 L-20 72 Z", INK, None)


def house_face(g, x, y, s=1.0, col="#FFC93C"):
    with g.at(x, y, 0, s):
        g.poly([(-170, -140), (0, -290), (170, -140)], "#C0504D", INK, lw=8)
        g.rect(-150, -140, 300, 260, col, INK, lw=8)
        g.rect(-110, -100, 70, 70, "#BDEBFF", INK, lw=6)
        g.rect(40, -100, 70, 70, "#BDEBFF", INK, lw=6)
        g.rect(-40, 10, 80, 110, "#8A5530", INK, lw=6, r=40)


def car_face(g, x, y, s=1.0, col="#5ED3B5"):
    """Front of a generic car: two round lights and a grille = a face."""
    with g.at(x, y, 0, s):
        g.rc(0, -40, 360, 150, col, INK, lw=8, r=40)
        g.rc(0, -150, 260, 100, shade(col, 0.85), INK, lw=8, r=26)
        g.rc(0, -150, 210, 64, "#BDEBFF", INK, lw=5, r=14)
        for sx in (-1, 1):
            g.circle(sx * 120, -50, 34, "#FFF4E0", INK, lw=6)
        g.rc(0, 10, 160, 40, "#22181B", INK, lw=5, r=14)
        for sx in (-1, 1):
            g.rc(sx * 130, 50, 60, 40, "#22181B", INK, lw=6, r=10)


def cloud_face(g, x, y, s=1.0, t=0.0):
    with g.at(x, y, 0, s):
        for (cx, cy, r) in ((-110, 10, 80), (-30, -40, 100), (80, -20, 90), (140, 30, 64), (0, 40, 90)):
            g.circle(cx, cy, r + 7, INK, None)
        for (cx, cy, r) in ((-110, 10, 80), (-30, -40, 100), (80, -20, 90), (140, 30, 64), (0, 40, 90)):
            g.circle(cx, cy, r, "#FFFFFF", None)
        g.circle(-40, -10, 14, "#9AB8C8", None); g.circle(50, -16, 14, "#9AB8C8", None)
        g.line("M-50 40 Q10 80 60 36", "#9AB8C8", 9)


def pizza_face(g, x, y, s=1.0):
    with g.at(x, y, 0, s):
        g.circle(0, 0, 170, "#C9873E", INK, lw=9)
        g.circle(0, 0, 145, "#F2C66D", None)
        g.circle(-55, -40, 30, "#C0392B", INK, lw=5); g.circle(55, -40, 30, "#C0392B", INK, lw=5)
        g.path("M-80 40 Q0 120 80 40 Q0 76 -80 40 Z", "#C0392B", INK, lw=5)
        g.circle(0, 10, 14, "#3E8E5E", None)


# ------------------------------------------------------------------ party crowd (simple silhouettes, no faces)
def party_crowd(g, t, y=1080, n=9, cols=("#2F5F6A", "#5B3A8C", "#8E2430", "#3E7CB1", "#7A5A3A", "#2F6F62"), a=1.0, seed=1, s=1.0):
    r = rnd(seed)
    for i in range(n):
        x = (i + 0.5) / n * 1920 + (r.random() - 0.5) * 120
        hh = (300 + r.random() * 120) * s
        bob = 8 * math.sin(t * 3 + i)
        c = cols[i % len(cols)]
        with g.group(a):
            g.rc(x, y - hh * 0.35 + bob, hh * 0.42, hh * 0.7, c, INK, lw=7, r=hh * 0.15)
            g.circle(x, y - hh * 0.82 + bob, hh * 0.16, shade(c, 0.6), INK, lw=7)
