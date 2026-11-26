"""B-008 (L8) "How 7 Everyday Things Were Invented by Accident" — long video, Style F + cast v2.2 + lib/flat_invent.py props, 1920x1080.
python episodes/B-008-accidental-inventions/make.py sheet|qa|times <t,..> <out>|big <t,..>|chapters|animatic|render
Sets: Museum of Happy Accidents (countdown hall), 1945 radar lab, modern kitchen, 1943 shipyard workshop, crate steps, 1945 parlour, 1945 department store,
home staircase, alpine meadow, 1941 study + microscope view, 1942/1951 chemistry lab, 1938 gas lab, molecule view, 1903 Paris lab, 1909 road, gas-mask
workshop, car windscreen, 1928 London lab, Oxford lab, penicillin factory.
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at, turn_at
from flat_fx import sparkles, arrow, burst, ring_wave, no_sign, qmark, steam, puff
from flat_invent import *
from flat_pets import dog_side, dog_sit, DOG
from flat_annoy import sneaker
import sfxgen  # noqa: registers generated SFX

V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="inventive", captions=False)
CH_PAUSE = 1.1
FL = 900
HIKEDOG = dict(DOG, fur="#C98A4A", ear="#8A5A2A", light="#F4E6D0")


# ------------------------------------------------------------------ helpers
def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def pk(c, word, n=0, frac=0.5, d=0.3):
    return pop(c.t, tw(c, word, n, frac) - 0.1, d)


def lt(c):
    return c.gt - c.V.voice0[c.sh["line"]]


def label(g, txt, x, y, size=70, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x=W / 2, y=80, k=1.0, size=46):
    """Small context label (year/place) while the story moves (why_not_viral rule 2)."""
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, "#3A1626", PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def check(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, PAL["mint"], INK, lw=r * 0.12)
        g.line([(-0.45 * r, 0), (-0.1 * r, 0.35 * r), (0.5 * r, -0.35 * r)], INK, r * 0.2)


def cross(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, "#FF5B4B", INK, lw=r * 0.12)
        g.line([(-0.4 * r, -0.4 * r), (0.4 * r, 0.4 * r)], INK, r * 0.2); g.line([(-0.4 * r, 0.4 * r), (0.4 * r, -0.4 * r)], INK, r * 0.2)


def stamp(g, txt, x, y, k, col="#FF5B4B", size=90, rot=-0.12):
    if k <= 0: return
    with g.screen():
        with g.at(x, y, rot, 1.6 - 0.6 * back_out(clamp(k), 1.4)):
            w = g.text_w(txt, size) + 60
            g.rc(0, 0, w, size * 1.45, None, col, lw=10, r=18, a=clamp(k * 2))
            g.text(txt, 0, 4, size, col, stroke=None, a=clamp(k * 2))


def walker(g, cid, x, y, h, t, expr="deadpan", flip=False, pl="down", pr="down", moving=True, view=None):
    bob = abs(math.sin(t * 7)) * 10 if moving else 0
    if moving:
        sw = "hold" if math.sin(t * 7) > 0 else "down"
        pl = pl if pl != "down" else ("down" if sw == "hold" else "hold")
        pr = pr if pr != "down" else sw
    char2(g, cid, x, y - bob, h, expr, pl, pr, t=t, flip=flip, view=view)


def chest(x, feet, h, side=1):
    """Shirt-pocket position on a cast figure (feet at x,feet, height h)."""
    return x + side * 0.075 * h, feet - 0.6 * h


def heatwaves(g, x0, y0, x1, y1, t, k=1.0, col="#FFB38A"):
    if k <= 0: return
    for i in range(4):
        ph = (t * 1.2 + i / 4) % 1
        x = x0 + (x1 - x0) * ph; y = y0 + (y1 - y0) * ph
        g.path(f"M{x} {y - 90} q30 45 0 90 q-30 45 0 90", None, col, lw=10, a=k * 0.8 * math.sin(ph * math.pi))


def frame_box(g, x, y, w, h, k, col="#FFF4E0"):
    """Rounded picture frame for montage tiles; returns a context manager clip."""
    g.rc(x, y, w + 16, h + 16, col, INK, lw=8, r=24)


# ------------------------------------------------------------------ sets
def museum(g, t, spot=None, cases=True, glow_i=None, lit=None):
    """Museum of Happy Accidents: plum walls, wood panels, banner, 7 numbered plinths."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#5A2338", "#2E0F1E"))
    with g.layer(0.6):
        for i in range(-1, 12):
            g.rect(i * 190, 120, 150, 560, "#6A2B44", None, r=12, a=0.6)
        g.rc(W / 2, 90, 900, 90, "#C9A23A", INK, lw=7, r=14)
        g.text("MUSEUM OF HAPPY ACCIDENTS", W / 2, 96, 50, "#3A1626", stroke=None)
        for x in (300, 960, 1620):
            g.poly([(x - 30, 0), (x + 30, 0), (x + 230, FL), (x - 230, FL)], "#FFE9B0", None, a=0.06 + 0.02 * math.sin(t * 1.5 + x))
    g.rect(-100, FL - 220, W + 200, 220, "#4A2414", INK, lw=7)
    for i in range(-1, 14):
        g.line([(i * 160, FL - 220), (i * 160, FL)], "#3A1A0E", 5)
    g.rect(-100, FL, W + 200, H, g.lgrad(0, FL, 0, H, "#8A4E2A", "#5A2E18"), INK, lw=8)
    for i in range(-1, 16):
        g.line([(i * 150, FL), (i * 150 - 90, H)], "#74401F", 5)
    if cases:
        for i in range(7):
            x = 200 + i * 253
            n = 7 - i
            hl = (lit or {}).get(n, 0.0)
            g.rc(x, FL - 40, 170, 120, "#6B3A22", INK, lw=6, r=8)
            g.rc(x, FL - 110, 200, 22, "#C9A23A", INK, lw=5, r=6)
            g.rc(x, FL - 200, 150, 150, "#DDF3FF", INK, lw=5, r=12, a=0.22 + 0.4 * hl)
            if hl > 0:
                g.glow(x, FL - 200, 160, "#FFE29A", 0.5 * hl)
            g.text(f"#{n}", x, FL - 40, 50, "#FFC93C", sw=6)


def radar_lab(g, t, glow=1.0):
    """1945 radar lab: green-grey panels, racks of dials, cable runs, window with a radar dish."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#5E7468", "#3A4C44"))
    with g.layer(0.7):
        for j in range(5):
            g.line([(-50, 120 + j * 150), (W + 50, 120 + j * 150)], "#52665C", 4)
        for i, x in enumerate((140, 380)):
            g.rect(x - 100, 160, 200, FL - 160, "#3E4A48", INK, lw=7)
            for k in range(5):
                g.circle(x - 40, 230 + k * 120, 28, "#E8E2CC", INK, lw=5)
                g.line([(x - 40, 230 + k * 120), (x - 40 + 20 * math.cos(t * (1 + k) + k), 230 + k * 120 - 20)], "#FF5B4B", 4)
                g.circle(x + 40, 230 + k * 120, 10, ("#7CF0B5" if (int(t * 3) + k + i) % 3 else "#2A3A30"), INK, lw=3)
        g.rect(1460, 150, 360, 300, "#2E3C38", INK, lw=8, r=8)
        g.rect(1475, 165, 330, 270, g.lgrad(0, 165, 0, 435, "#8FB8D8", "#D8ECF5"), None)
        with g.at(1640, 330, 0.3 * math.sin(t * 0.6)):
            g.path("M-90 -40 Q0 60 90 -40 Z", "#C9CED6", INK, lw=6)
            g.line([(0, 10), (0, 90)], INK, 8)
        g.path(f"M520 140 Q900 {100 + 10 * math.sin(t)} 1300 140", None, "#2A2A34", lw=14)
    g.rect(-100, FL, W + 200, H, "#6E6A60", INK, lw=8)
    for i in range(-1, 12):
        g.line([(i * 200, FL), (i * 200 - 60, H)], "#5E5A52", 4)


def bench(g, x, y, w=700, col="#7A5236", top="#9A6A44"):
    g.rect(x - w / 2, y - 280, w, 44, top, INK, lw=7, r=8)
    for sx in (-w / 2 + 40, w / 2 - 70):
        g.rect(x + sx, y - 236, 30, 236, col, INK, lw=6)


def kitchen(g, t, warm=1.0):
    """Modern kitchen: mint tiles, cupboards, window, counter."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#DFF3EA", "#BFE3D4"))
    with g.layer(0.75):
        for j in range(6):
            for i in range(-1, 22):
                g.rect(i * 96 + (48 if j % 2 else 0), 300 + j * 66, 90, 60, "#CDEBDF", None, r=6)
        for x in (260, 560, 1360, 1660):
            g.rect(x - 140, 40, 280, 220, "#FF8A6A", INK, lw=7, r=12)
            g.circle(x + (100 if x < 900 else -100), 150, 10, INK, None)
        g.rect(820, 60, 300, 230, "#7A5236", INK, lw=8, r=10)
        g.rect(835, 75, 270, 200, g.lgrad(0, 75, 0, 275, "#9FDCF5", "#E3F6FF"), None)
        g.line([(970, 75), (970, 275)], "#7A5236", 8)
    g.rect(-100, 720, W + 200, 60, "#F4F1EA", INK, lw=8, r=6)
    g.rect(-100, 780, W + 200, 320, "#3E7CB1", INK, lw=8)
    for x in range(100, W, 320):
        g.rect(x, 810, 280, 240, "#4A8AC0", INK, lw=6, r=10)
        g.rc(x + 140, 840, 80, 12, "#C9CED6", INK, lw=3, r=6)


def shipyard(g, t):
    """1943 shipyard workshop: steel-blue walls, rivets, portholes onto the river with a crane, shelves of springs."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#5A7894", "#36506A"))
    with g.layer(0.7):
        for j in range(4):
            for i in range(-1, 20):
                g.circle(i * 110 + 40, 140 + j * 200, 7, "#4A6680", None)
        for x in (1250, 1620):
            g.circle(x, 300, 120, "#2F4258", INK, lw=12)
            g.circle(x, 300, 100, g.lgrad(0, 200, 0, 400, "#A8D4EE", "#E6F4FC"), None)
            g.rect(x - 100, 330, 200, 70, "#5E8FB0", None)
        with g.at(1400, 330):
            g.line([(-60, 0), (-60, -120), (120, -120)], "#C9502A", 10)
            g.line([(100, -120), (100, -60)], INK, 4)
        g.rect(80, 200, 560, 24, "#7A5236", INK, lw=6)
        g.rect(80, 420, 560, 24, "#7A5236", INK, lw=6)
        for i in range(6):
            spring_coil(g, 140 + i * 90, 198, 0.7)
            g.circle(140 + i * 90, 400, 34, "#E8E2CC", INK, lw=5)
    g.rect(-100, FL, W + 200, H, "#56626E", INK, lw=8)
    for i in range(-1, 12):
        g.line([(i * 200, FL), (i * 200 - 60, H)], "#4A5560", 4)


def parlour(g, t):
    """1945 home parlour: rose wallpaper stripes, lamp, bookshelf."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F2C7B8", "#E2A898"))
    with g.layer(0.75):
        for i in range(-1, 26):
            g.rect(i * 80, 0, 22, FL, "#EBB6A6", None)
        g.rect(1380, 140, 420, 560, "#7A4A2A", INK, lw=8, r=8)
        for j in range(4):
            g.rect(1395, 270 + j * 130, 390, 16, "#5A3418", None)
            for k in range(9):
                g.rect(1410 + k * 42, 190 + j * 130, 30, 80, ["#3E7CB1", "#FF6B5B", "#5ED3B5", "#FFC93C"][(k + j) % 4], INK, lw=3)
        with g.at(220, FL):
            g.line([(0, 0), (0, -520)], INK, 9)
            g.path("M-80 -520 L80 -520 L50 -640 L-50 -640 Z", "#FFC93C", INK, lw=7)
            g.glow(0, -570, 240, "#FFE29A", 0.35)
    g.rect(-100, FL, W + 200, H, "#9A6238", INK, lw=8)
    g.ellipse(960, 990, 700, 70, "#5E8F6A", INK, lw=7)


def store(g, t):
    """1945 department store: cream columns, garlands of coloured lights, counter, crowd."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F5E3C2", "#E2C79A"))
    with g.layer(0.7):
        for x in (160, 640, 1280, 1760):
            g.rect(x - 50, 60, 100, FL - 60, "#FFF4E0", INK, lw=7)
            g.rect(x - 70, 60, 140, 40, "#E8D2A8", INK, lw=6)
        for i in range(24):
            x = i * 84 + 20
            g.circle(x, 70 + 24 * math.sin(i * 0.8), 12, ["#FF6B5B", "#FFC93C", "#5ED3B5", "#3E7CB1"][i % 4], INK, lw=3,
                     a=0.6 + 0.4 * ((int(t * 4) + i) % 2))
    with g.layer(0.85):
        for i in range(16):
            x = 60 + i * 120 + 30 * math.sin(i)
            hh = 120 + 30 * math.sin(i * 2.1)
            g.circle(x, 560 - hh + 8 * math.sin(t * 3 + i), 42, ["#7A5A4A", "#5A6E8A", "#9A4A2A", "#3E6A5C"][i % 4], None, a=0.7)
            g.rect(x - 55, 600 - hh, 110, 260, ["#7A5A4A", "#5A6E8A", "#9A4A2A", "#3E6A5C"][i % 4], None, r=40, a=0.7)
    g.rect(-100, FL, W + 200, H, "#B88A5A", INK, lw=8)
    g.rect(300, 650, 1320, 280, "#7A3E1E", INK, lw=9, r=12)
    g.rect(300, 650, 1320, 40, "#C9A23A", INK, lw=6)


def staircase(g, t, x0=380, y0=330, sw=180, sh=95, n=6):
    """Home staircase (steps go down to the right). Returns step size."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F7E6C4", "#EBCF9E"))
    with g.layer(0.75):
        for i in range(-1, 26):
            g.rect(i * 80, 0, 6, FL, "#EED8AE", None)
        g.rect(1500, 140, 300, 220, "#7A5236", INK, lw=7)
        g.rect(1515, 155, 270, 190, "#FFF4E0", None)
        spring_coil(g, 1650, 320, 1.0, 0.0, 9, "#FFC93C")
    g.rect(-100, FL, W + 200, H, "#B9844F", INK, lw=8)
    for i in range(n):
        x, y = x0 + i * sw, y0 + i * sh
        g.rect(x, y, sw + 20, FL - y, "#C98A4A", INK, lw=6)
        g.rect(x - 10, y - 14, sw + 40, 24, "#E8A96A", INK, lw=5, r=6)
    g.line([(x0 - 40, y0 - 180), (x0 + n * sw, y0 + n * sh - 180)], "#7A4A2A", 14)
    return sw, sh


def alps(g, t, x_off=0.0):
    """Alpine meadow: snowy peaks, pines, flowers, a path."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#8FD3F5", "#E6F7FF"))
    with g.layer(0.3):
        for x, h, w in ((200, 520, 520), (720, 640, 640), (1300, 560, 600), (1800, 600, 560)):
            g.poly([(x - w / 2, 720), (x, 720 - h), (x + w / 2, 720)], "#7A93B0", INK, lw=6)
            g.poly([(x - w * 0.12, 720 - h * 0.76), (x, 720 - h), (x + w * 0.12, 720 - h * 0.76), (x + 20, 720 - h * 0.7), (x - 30, 720 - h * 0.72)], "#FFFFFF", INK, lw=5)
    with g.layer(0.55):
        g.path("M-100 760 Q500 620 1000 720 Q1500 820 2100 680 L2100 1100 L-100 1100 Z", "#7CC56B", INK, lw=7)
        for i in range(9):
            x = i * 260 + 60 - (x_off * 0.3) % 260
            g.poly([(x - 60, 760), (x, 560), (x + 60, 760)], "#3E7E4A", INK, lw=5)
    g.path("M-100 860 Q600 800 1100 880 Q1600 960 2100 860 L2100 1100 L-100 1100 Z", "#93D67E", INK, lw=7)
    g.path("M-100 1000 Q700 900 2100 1000 L2100 1060 Q700 960 -100 1060 Z", "#E6D2A0", None)
    for i in range(30):
        x = (i * 137 - x_off * 0.8) % (W + 100) - 50
        g.circle(x, 930 + (i * 53) % 120, 9, ["#FFFFFF", "#FFC93C", "#FF8AA0"][i % 3], INK, lw=2)


def study_1941(g, t):
    """1941 Swiss study: pine panels, window with mountains, desk."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#E8C48E", "#D4A86C"))
    with g.layer(0.75):
        for i in range(-1, 14):
            g.rect(i * 160, 0, 150, FL, "#E2BA82", INK, lw=3)
        g.rect(1350, 140, 420, 320, "#7A4A2A", INK, lw=8)
        g.rect(1365, 155, 390, 290, g.lgrad(0, 155, 0, 445, "#8FD3F5", "#E6F7FF"), None)
        g.poly([(1365, 445), (1480, 290), (1580, 445)], "#7A93B0", None)
        g.poly([(1520, 445), (1650, 260), (1755, 445)], "#8AA3C0", None)
        g.poly([(1630, 290), (1650, 260), (1670, 290)], "#FFFFFF", None)
    g.rect(-100, FL, W + 200, H, "#8A5A32", INK, lw=8)


def micro_view(g, t, col="#1E3A44"):
    """Microscope eyepiece view: dark round field with a bright circle."""
    g.fill_all("#0E141A")
    g.circle(W / 2, H / 2, 470, g.rgrad(W / 2, H / 2, 470, "#F7F2E2", "#E9DFC0", "#B8A880"), INK, lw=18)


def chem_lab(g, t, wall="#BFE3D4", year=None):
    """1940s/50s chemistry lab: mint tiles, shelves of bottles, fume hood."""
    g.fill_all(g.lgrad(0, 0, 0, H, wall, shade(wall, 0.85)))
    with g.layer(0.75):
        for j in range(9):
            for i in range(-1, 22):
                g.rect(i * 96 + (48 if j % 2 else 0), j * 100, 90, 94, shade(wall, 1.05), None, r=6, a=0.6)
        for j in range(2):
            g.rect(1180, 180 + j * 200, 640, 20, "#7A5236", INK, lw=5)
            for k in range(8):
                x = 1220 + k * 76
                cols = ["#FF6B5B", "#5ED3B5", "#FFC93C", "#3E7CB1", "#B07AD0"]
                g.rc(x, 140 + j * 200, 46, 76, "#FFFFFF", INK, lw=4, r=10, a=0.85)
                g.rc(x, 156 + j * 200, 40, 40, cols[(k + j) % 5], None, r=8)
        g.rect(80, 120, 420, 520, "#D8DCE0", INK, lw=8, r=10)
        g.rect(110, 150, 360, 300, "#EAF6FA", INK, lw=5, a=0.7)
    g.rect(-100, FL, W + 200, H, "#6A7A80", INK, lw=8)
    for i in range(-1, 12):
        g.line([(i * 200, FL), (i * 200 - 60, H)], "#5A6A70", 4)


def gas_lab(g, t):
    """1938 gas lab: warm brick, pipework, cylinder rack, a 1930s refrigerator."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#C97A5A", "#9A5238"))
    with g.layer(0.75):
        for j in range(12):
            for i in range(-1, 16):
                g.rect(i * 140 + (70 if j % 2 else 0), j * 76, 132, 68, "#BF7052", None, r=4, a=0.7)
        for y in (120, 170):
            g.line([(-50, y), (W + 50, y)], "#8A949E", 18)
            g.line([(-50, y), (W + 50, y)], INK, 3)
        for i in range(4):
            g.line([(300 + i * 400, 170), (300 + i * 400, 300)], "#8A949E", 14)
            g.circle(300 + i * 400, 300, 24, "#C9A23A", INK, lw=5)
        with g.at(1640, FL):                                     # 1930s fridge
            g.rc(0, -270, 260, 540, "#F4F1EA", INK, lw=8, r=40)
            g.line([(-130, -330), (130, -330)], INK, 5)
            g.rc(100, -400, 16, 90, "#C9CED6", INK, lw=4, r=6)
            g.rc(0, -580, 180, 70, "#E6E6E6", INK, lw=6, r=30)
    g.rect(-100, FL, W + 200, H, "#5E5048", INK, lw=8)


def paris_lab(g, t):
    """1903 Paris lab: ochre art-nouveau wallpaper, arched window over rooftops, wooden shelves."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#E8B866", "#C9923E"))
    with g.layer(0.75):
        for i in range(-1, 16):
            x = i * 140
            g.path(f"M{x} 0 Q{x + 40} 200 {x} 400 Q{x - 40} 600 {x} 900", None, "#D9A452", lw=10)
        g.path("M1300 520 L1300 260 Q1300 120 1520 120 Q1740 120 1740 260 L1740 520 Z", "#6B3A22", INK, lw=9)
        g.path("M1320 505 L1320 265 Q1320 140 1520 140 Q1720 140 1720 265 L1720 505 Z", g.lgrad(0, 140, 0, 505, "#F7C9A0", "#FFE9CC"), None)
        for i, (x, h) in enumerate(((1340, 110), (1420, 150), (1500, 90), (1580, 170), (1660, 120))):
            g.rect(x, 505 - h, 70, h, "#8A7A90", INK, lw=3)
            g.poly([(x - 6, 505 - h), (x + 35, 505 - h - 30), (x + 76, 505 - h)], "#5A4A70", INK, lw=3)
        g.line([(1520, 140), (1520, 505)], "#6B3A22", 8)
        g.rect(120, 230, 620, 22, "#6B3A22", INK, lw=6)
        g.rect(120, 430, 620, 22, "#6B3A22", INK, lw=6)
        for k in range(5):
            g.rc(180 + k * 120, 190, 50, 70, ["#CDEFFA", "#FFE29A", "#BDEBFF", "#F4C8C8", "#CDEFFA"][k], INK, lw=4, r=12, a=0.9)
    g.rect(-100, FL, W + 200, H, "#7A4E2E", INK, lw=8)
    for i in range(-1, 20):
        g.rect(i * 120, FL, 60, 200, "#6A4226", None)


def road_1909(g, t, x_car=960, shards=0.0):
    """Early motoring road: hills, a vintage open car (no brand)."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F7D9A0", "#FFF0D0"))
    with g.layer(0.4):
        g.path("M-100 640 Q500 480 1000 600 Q1500 700 2100 560 L2100 900 L-100 900 Z", "#A8C878", INK, lw=6)
        for i in range(8):
            g.circle(100 + i * 260, 600 - 30 * math.sin(i), 60, "#6E9E58", INK, lw=5)
    g.rect(-100, 760, W + 200, 400, "#C9A27A", INK, lw=7)
    for i in range(12):
        x = (i * 220 - t * 300) % (W + 220) - 110
        g.rect(x, 900, 110, 16, "#E8D2A8", None, r=8)
    with g.at(x_car, 860):
        g.rc(0, -110, 520, 120, "#2F5F6A", INK, lw=8, r=30)
        g.rc(-60, -200, 260, 90, "#2F5F6A", INK, lw=7, r=20)
        g.rect(80, -330, 16, 140, INK, None)
        g.rect(70, -330, 120, 150, "#CDEFFA", INK, lw=6, a=0.8 * (1 - shards))
        for wx in (-170, 170):
            g.circle(wx, -40, 72, "#2A2A34", INK, lw=8)
            g.circle(wx, -40, 30, "#C9CED6", INK, lw=5)
            for k in range(6):
                a0 = k * TAU / 6 + t * 6
                g.line([(wx, -40), (wx + 66 * math.cos(a0), -40 + 66 * math.sin(a0))], INK, 4)
        if shards > 0:
            r = rnd(4)
            for k in range(14):
                a0 = -1.8 + r.random() * 2.2
                d = 40 + 380 * ease_out(shards) * (0.6 + 0.4 * r.random())
                px, py = 130 + d * math.cos(a0), -255 + d * math.sin(a0) + 200 * shards ** 2
                g.poly([(px, py), (px + 26, py + 8), (px + 6, py + 30)], "#CDEFFA", INK, lw=3)


def london_lab(g, t):
    """1928 London lab: dark green walls, brick-and-chimney window, crowded bench."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#3E6A5C", "#28463C"))
    with g.layer(0.75):
        g.rect(1260, 130, 520, 400, "#2A1A12", INK, lw=10)
        g.rect(1280, 150, 480, 360, g.lgrad(0, 150, 0, 510, "#C9CED6", "#EDEFF2"), None)
        for i, (x, h) in enumerate(((1290, 160), (1400, 220), (1520, 130), (1640, 200))):
            g.rect(x, 510 - h, 100, h, "#9A5238", INK, lw=4)
            g.rect(x + 30, 510 - h - 60, 26, 60, "#7A4228", INK, lw=3)
            for k in range(2):
                ph = (t * 0.3 + k * 0.5 + i * 0.2) % 1
                g.circle(x + 43 + 30 * ph, 510 - h - 70 - 80 * ph, 16 + 20 * ph, "#FFFFFF", None, a=0.5 * (1 - ph))
        g.line([(1520, 150), (1520, 510)], "#2A1A12", 10); g.line([(1280, 330), (1760, 330)], "#2A1A12", 10)
        g.rect(100, 200, 560, 20, "#5A3A22", INK, lw=5)
        for k in range(6):
            g.rc(150 + k * 90, 160, 50, 74, ["#E8E2CC", "#C9E6D8", "#F4E2B8"][k % 3], INK, lw=4, r=10)
    g.rect(-100, FL, W + 200, H, "#4A3A30", INK, lw=8)
    for i in range(-1, 20):
        g.line([(i * 110, FL), (i * 110 - 40, H)], "#3E3028", 4)


def factory(g, t):
    """1940s penicillin plant: rows of steel fermentation tanks, pipes, gauges."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#CFD8DE", "#A9B6C0"))
    with g.layer(0.6):
        for i in range(9):
            x = 120 + i * 220
            g.rc(x, 520, 160, 520, "#B8C2CA", INK, lw=6, r=60)
            g.circle(x, 400, 26, "#FFF4E0", INK, lw=4)
            g.line([(x, 400), (x + 18 * math.cos(t * 2 + i), 400 - 18 * abs(math.sin(t * 2 + i)))], "#FF5B4B", 4)
        g.line([(-50, 230), (W + 50, 230)], "#8A949E", 22); g.line([(-50, 230), (W + 50, 230)], INK, 3)
    g.rect(-100, FL, W + 200, H, "#7A8690", INK, lw=8)


# ------------------------------------------------------------------ scene helpers
def radar_man(g, c, x=720, feet=FL + 140, h=930, expr="shocked", melt=None, pr="down", pl="down", view="3q", flip=False):
    char2(g, "radar", x, feet, h, expr, pl, pr, t=c.gt, view=view, flip=flip)
    px, py = chest(x, feet, h, -1 if flip else 1)
    if melt is not None:
        candy_bar(g, px, py - 95, 0.95, melt, c.gt, rot=0.08)
        pocket(g, px, py, 150, 95)


def card(n, title, exhibit=None):
    """Countdown card: the museum hall, a brass plaque with the number and a title ribbon; exhibit drawn in the spotlight case."""
    def f(g, c):
        museum(g, c.gt, lit={n: 1.0})
        k = back_out(seg(c.t, 0.0, 0.45), 1.5)
        x = 200 + (7 - n) * 253
        g.glow(x, FL - 200, 300, "#FFE29A", 0.5 * k)
        if exhibit:
            exhibit(g, c, x, FL - 140)
        with g.screen():
            countdown_plaque(g, W / 2, 400, n, k, 1.0, c.gt)
            kk = back_out(seg(c.t, 0.35, 0.4), 1.5)
            if kk > 0.02:
                g.rc(W / 2, 690, (g.text_w(title, 74) + 90) * min(1, kk), 120, PAL["coral"], INK, lw=9, r=30, rot=-0.02)
            g.text(title, W / 2, 696, 74, PAL["cream"], sw=10, sc=kk + 1e-3)
        char2(g, "wy", 1700, FL + 60, 520, "smile", "down", "point", t=c.gt, view="3q", flip=True)
    return f


def ex_springs(g, c, x, y):
    spring_coil(g, x, y - 20, 0.55, 0.0, 9, "#FFC93C")


def ex_burr(g, c, x, y):
    burr(g, x, y - 70, 34, c.gt * 0.3)


def ex_glue(g, c, x, y):
    glue_tube(g, x, y - 150, 0.5, 0.3)


def ex_cyl(g, c, x, y):
    gas_cylinder(g, x, y - 20, 0.42)


def ex_flask(g, c, x, y):
    flask(g, x, y - 20, 0.38, 0.0, crack=1.0)


def ex_candy(g, c, x, y):
    candy_bar(g, x, y - 150, 0.6, 0.5, c.gt)


def ex_dish(g, c, x, y):
    petri_dish(g, x, y - 70, 70, c.gt, mould=1.0, ring=1.0)


# ------------------------------------------------------------------ cold open
def s_hook(g, c, loop=False):
    radar_lab(g, c.gt)
    bench(g, 1350, FL + 40, 620)
    magnetron(g, 1350, FL - 240, 1.15, c.gt, 1.0)
    t = c.t
    m = 0.35 + 0.65 * clamp(t / 3.0) if not loop else 0.3 + 0.5 * clamp(t / 2.5)
    heatwaves(g, 1180, 470, 860, 470, c.gt, 1.0)
    look = pose_at(t, [(0, "down"), (0.6, "explain")])
    radar_man(g, c, 700, FL + 150, 960, "shocked", m, pr=look)
    if not loop:
        with g.screen():
            g.text("WHY IS IT MELTING?", W / 2 + 40, 990, 112, PAL["yellow"], sw=20, depth=9, sc=back_out(clamp(t / 0.25), 1.4) if t > 0 else 1.0)


def s_nothot(g, c):
    radar_lab(g, c.gt)
    radar_man(g, c, 960, FL + 150, 960, "suspicious", 0.7 + 0.3 * c.u, pr="shrug", pl="shrug", view="front")
    for i, (x, kw) in enumerate(((420, "Nothing"), (1500, "hot"))):
        k = on(c, kw)
        with g.at(x, 420, 0, back_out(clamp(k), 1.6) + 1e-3):
            g.rc(0, 0, 70, 300, "#FFFFFF", INK, lw=8, r=35)
            g.circle(0, 150, 60, "#3E9AE0", INK, lw=8)
            g.rc(0, 80, 30, 120, "#3E9AE0", None, r=10)
    label(g, "NOTHING HOT", W / 2, 140, 76, PAL["cream"], k=on(c, "hot"))


def s_your_kitchen(g, c):
    kitchen(g, c.gt)
    k = on(c, "microwave")
    microwave_modern(g, 1250, 720, 1.25, c.gt, on=1.0, food=True)
    char2(g, "modern", 520, FL + 170, 900, "smile" if k > 0.5 else "deadpan", "down", "hold", t=c.gt, view="3q")
    with g.screen():
        kk = on(c, "sticky")
        g.rc(330, 150, 360 * kk + 1, 120 * kk + 1, "#3A1626", INK, lw=7, r=20)
        if kk > 0.5:
            g.text("1945", 330, 158, 72, PAL["yellow"], sw=8)
        arrow(g, 540, 160, 900, 160, k=k)
        label(g, "YOU", 1010, 165, 80, k=k)


def s_montage(g, c):
    museum(g, c.gt, cases=False)
    tiles = [("toy", 480, 330), ("glue", 1440, 330), ("pan", 480, 760), ("dish", 1440, 760)]
    for i, (wd, x, y) in enumerate(tiles):
        k = back_out(clamp(on(c, wd, d=0.4)), 1.5)
        if k <= 0: continue
        with g.at(x, y, (-0.03, 0.025, 0.02, -0.025)[i], k * 0.76):
            g.rc(0, 0, 700, 380, "#FFF4E0", INK, lw=9, r=26)
            g.rc(0, 0, 660, 340, ["#F7E6C4", "#BFE3D4", "#DFF3EA", "#3E6A5C"][i], None, r=20)
            if i == 0:
                for s in range(3):
                    g.rect(-280 + s * 160, -60 + s * 60, 180, 230 - s * 60, "#C98A4A", INK, lw=5)
                slinky_walk(g, -200, -62, 160, 60, (c.t - tw(c, "toy")) % 2.2, 0.6, col="#FFC93C", n=14)
            elif i == 1:
                glue_tube(g, -60, -40, 0.7, 0.4)
                with g.at(180, 60):
                    g.poly([(-80, 100), (80, 100), (100, -60), (-100, -60)], "#8A949E", INK, lw=6)
                cross(g, 230, -100, 40, on(c, "thrown"))
            elif i == 2:
                frying_pan(g, -40, 40, 0.9, 0, math.sin(c.gt * 2.5), c.gt)
            else:
                petri_dish(g, 0, 0, 140, c.gt, mould=1.0, ring=0.4 + 0.6 * on(c, "saved"))
                if on(c, "saved") > 0:
                    g.glow(0, 0, 220, "#FFE29A", 0.35 * on(c, "saved"))


def s_countdown(g, c):
    museum(g, c.gt, lit={n: on(c, "Counting") * (1.0 if n == 7 else 0.0) + on(c, "world") * (1.0 if n == 1 else 0.0) for n in range(1, 8)})
    char2(g, "wy", 960, FL + 120, 720, "smile", "down", pose_at(c.t, [(0, "down"), (tw(c, "Counting"), "point")]), t=c.gt, view="front")
    label(g, "7 ACCIDENTS", W / 2, 230, 92, k=on(c, "Seven"))
    with g.screen():
        k = on(c, "Counting")
        arrow(g, 260, 380, 1660, 380, col=PAL["cream"], w=18, k=k)
        if k > 0.5:
            g.text("SMALL", 300, 330, 50, PAL["cream"], sw=7)
            g.text("WORLD-CHANGING", 1500, 330, 50, PAL["yellow"], sw=7)


# ------------------------------------------------------------------ #7 spring
def s_ship_bench(g, c):
    shipyard(g, c.gt)
    bench(g, 1000, FL + 20, 760, "#5A4030", "#7A5A40")
    with g.at(1000, FL - 270):                          # ship instrument on springs
        for sx in (-120, 120):
            spring_coil(g, sx, 0, 0.8, 0.0, 6 + int(2 * math.sin(c.gt * 6)), "#C9CED6")
        g.rc(0, -110 - 6 * math.sin(c.gt * 6), 300, 120, "#2F3A4F", INK, lw=7, r=14)
        g.circle(0, -110 - 6 * math.sin(c.gt * 6), 44, "#FFF4E0", INK, lw=5)
        g.line([(0, -110), (30 * math.cos(c.gt * 2), -130)], "#FF5B4B", 5)
    char2(g, "shipwright", 1500, FL + 140, 880, "deadpan", "down", "explain", t=c.gt, view="3q", flip=True)
    tag(g, "PHILADELPHIA · 1943", k=on(c, "1943", frac=0.05))
    with g.screen():
        w = 12 * math.sin(c.gt * 2.2)
        g.path(f"M60 1000 Q480 {960 + w} 960 1000 T1860 1000", None, "#5E8FB0", lw=18, a=0.5)


def s_spring_falls(g, c):
    shipyard(g, c.gt)
    sw, sh = 210, 110
    x0, y0 = 300, 470
    for i in range(4):
        x, y = x0 + i * sw, y0 + i * sh
        g.rect(x, y, sw + 10, FL - y, "#9A6A44", INK, lw=6)
        g.line([(x + 20, y + 30), (x + sw - 10, y + 30)], "#7A4A2A", 4)
    kf_ = tw(c, "fell", frac=0.15)
    if c.t < kf_ + 0.35:
        u = clamp((c.t - kf_) / 0.35)
        spring_coil(g, x0 + 60, y0 - 20 + 0 * u, 0.9, u * 0.9, 9, "#C9CED6")
    else:
        slinky_walk(g, x0 + 60, y0 - 10, sw, sh, (c.t - kf_ - 0.35) * 0.9 + 0.0, 0.85, period=1.15)
    sh_ = on(c, "stepped")
    char2(g, "shipwright", 1620, FL + 140, 880, "shocked" if sh_ > 0.5 else "deadpan", "down", "point" if sh_ > 0.5 else "down", t=c.gt, view="3q", flip=True)
    label(g, "WALKING?", 1000, 200, 96, k=pk(c, "walking"))


def s_testing(g, c):
    shipyard(g, c.gt)
    bench(g, 960, FL + 20, 1100, "#5A4030", "#7A5A40")
    cols = ["#C9CED6", "#D98A4A", "#8A949E", "#FFC93C"]
    for i in range(4):
        x = 600 + i * 240
        b = abs(math.sin(c.gt * 3 + i)) * 40
        spring_coil(g, x, FL - 262 - b * (i == 3), 0.75, 0.0, 6 + 2 * i, cols[i])
        if on(c, "steels", frac=0.6) > 0:
            (check if i == 3 else cross)(g, x, FL - 560, 34, on(c, "coils", frac=0.8) if i < 3 else on(c, "coils", frac=0.9))
    char2(g, "shipwright", 260, FL + 140, 860, "curious", "think", "hold", t=c.gt, view="3q")
    label(g, "THE RIGHT SPRING?", 1300, 180, 72, k=on(c, "wondered", frac=0.2))


def s_name(g, c):
    parlour(g, c.gt)
    char2(g, "betty", 760, FL + 150, 880, "smile", "hold", "hold", t=c.gt, view="3q")
    char2(g, "shipwright", 380, FL + 150, 860, "smile", "down", "hip", t=c.gt, view="3q")
    with g.at(900, 600, -0.1):                            # open dictionary
        g.poly([(-150, 0), (0, 20), (0, -150), (-150, -170)], "#FFF4E0", INK, lw=6)
        g.poly([(150, 0), (0, 20), (0, -150), (150, -170)], "#FFF4E0", INK, lw=6)
        for k in range(5):
            g.line([(-130, -140 + k * 28), (-20, -126 + k * 28)], "#B8A890", 4)
            g.line([(20, -126 + k * 28), (130, -140 + k * 28)], "#B8A890", 4)
    k = on(c, "Slinky", d=0.5)
    with g.screen():
        g.text("SLINKY", 1380, 330, 150 * back_out(clamp(k), 1.6) + 1, PAL["yellow"], sw=22, depth=12)
    sparkles(g, c.gt, [(1180, 250), (1580, 260), (1400, 450)], k=k) if False else (sparkles(g, c.gt, [(1180, 250), (1580, 260), (1400, 450)]) if k > 0 else None)
    label(g, "SLEEK · GRACEFUL", 1380, 470, 50, PAL["cream"], k=on(c, "sleek"))


def s_store(g, c):
    store(g, c.gt)
    sold = clamp((c.t - tw(c, "Sold", frac=0.7)) / 1.2)
    n = int(round(400 * (1 - ease_io(sold))))
    for i in range(12):
        if i / 12 < 1 - sold:
            spring_coil(g, 420 + i * 95, 650, 0.45, 0.0, 6, ["#C9CED6", "#D8DCE0"][i % 2])
    char2(g, "shipwright", 1700, FL + 120, 760, "smile", "down", "wave", t=c.gt, view="3q", flip=True)
    tag(g, "PHILADELPHIA · NOVEMBER 1945", k=on(c, "November", frac=0.05))
    with g.screen():
        g.rc(330, 260, 220, 140, "#FFF4E0", INK, lw=7, r=16, rot=-0.06)
        g.text("$1", 330, 270, 100, "#C9302A", stroke=None, sc=0.6 + 0.4 * on(c, "dollar"))
        g.rc(W / 2, 260, 360, 140, "#3A1626", INK, lw=7, r=20)
        g.text(str(n), W / 2, 268, 96, PAL["yellow"], sw=8, sc=1 + 0.1 * pk(c, "Four"))
        k9 = on(c, "ninety")
        if k9 > 0:
            with g.at(1500, 260, 0, back_out(k9, 1.6)):
                g.circle(0, 0, 80, "#FFF4E0", INK, lw=8)
                g.line([(0, 0), (0, -55)], INK, 8)
                g.line([(0, 0), (55 * math.sin(k9 * 3.14), -55 * math.cos(k9 * 3.14))], "#FF5B4B", 6)
            g.text("90 MIN", 1500, 390, 56, PAL["yellow"], sw=8)


def s_stairs_now(g, c):
    sw, sh = staircase(g, c.gt)
    slinky_walk(g, 400, 320, sw, sh, c.gt * 0.9 % 5.4, 1.0, period=1.1, col="#FF6B5B")
    label(g, "HUNDREDS OF MILLIONS", 1240, 170, 74, k=on(c, "Hundreds"))
    with g.screen():
        if on(c, "seven", frac=0.8) > 0:
            countdown_plaque(g, 1640, 760, 7, on(c, "seven", frac=0.8), 0.5, c.gt)


# ------------------------------------------------------------------ #6 hook and loop
def s_walk(g, c, burrs=False):
    alps(g, c.gt, x_off=c.gt * 120)
    walker(g, "hiker", 820, FL + 150, 860, c.gt, "smile" if not burrs else "suspicious", view="3q")
    dog_side(g, 1220, 1010, 0.95, c.gt, walk=1, expr="happy", col=HIKEDOG)
    kb = on(c, "burrs") if burrs else 0
    if kb > 0:
        r = rnd(9)
        for i in range(14):
            bx = 760 + r.random() * 120; by = 560 + r.random() * 380
            burr(g, bx, by, 13 * back_out(clamp(kb * 2 - i * 0.08), 1.6) + 0.1, i)
        for i in range(10):
            burr(g, 1130 + r.random() * 200, 880 + r.random() * 80, 12 * back_out(clamp(kb * 2 - i * 0.1), 1.6) + 0.1, i)
    tag(g, "SWITZERLAND · 1941", k=on(c, "1941", frac=0.05))


def s_pull(g, c):
    study_1941(g, c.gt)
    bench(g, 1050, FL + 20, 700, "#6A4226", "#8A5A32")
    microscope_brass(g, 1150, FL - 262, 1.2)
    k = on(c, "microscope")
    burr(g, 1170 - 200 * (1 - k), FL - 380 + 0 * k, 18, c.gt)
    char2(g, "hiker", 600, FL + 150, 880, "curious" if k > 0.3 else "deadpan", "down", "reach_r" if k > 0.2 else "hold", t=c.gt, view="3q")
    dog_sit(g, 280, FL + 140, 0.7, c.gt, "happy", tongue=0.5, col=HIKEDOG)


def s_hooks(g, c, loops=True):
    micro_view(g, c.gt)
    with g.clip(circle=(W / 2, H / 2, 460)):
        for i in range(5):
            hook_closeup(g, 620 + i * 170, 420 + 30 * math.sin(i * 1.4), 1.0, 0.1 * math.sin(c.gt + i))
        if loops:
            kl = on(c, "loop")
            for i in range(4):
                loop_closeup(g, 700 + i * 170, 760 - 140 * kl, 1.1, 0.1 * math.sin(c.gt * 1.3 + i), ["#E07A5F", "#5ED3B5", "#FFC93C", "#B07AD0"][i])
    label(g, "HOOKS", 400, 240, 70, k=on(c, "hooks", frac=0.4))
    label(g, "LOOPS", 1520, 840, 70, PAL["cream"], k=on(c, "loop"))
    with g.screen():
        for j, (wd, txt) in enumerate((("Fur", "FUR"), ("wool", "WOOL"), ("threads", "THREADS"))):
            k = on(c, wd)
            if k > 0:
                g.text(txt, 1600, 300 + j * 90, 56, PAL["cream"], sw=8, sc=back_out(k, 1.6))


def s_question(g, c):
    study_1941(g, c.gt)
    k = on(c, "loops", frac=0.85)
    hook_strip(g, 1150, 520, 700, k, c.gt)
    label(g, "HOOKS", 1150, 320 - 0 * k, 56, k=on(c, "hooks", frac=0.6))
    label(g, "LOOPS", 1150, 740, 56, PAL["cream"], k=on(c, "loops", frac=0.85))
    char2(g, "hiker", 420, FL + 150, 880, "curious", "think", "down", t=c.gt, view="3q")
    qmark(g, 420, 140, 110, k=on(c, "question"), rot=0.1 * math.sin(c.gt * 2))


def s_years(g, c):
    study_1941(g, c.gt)
    bench(g, 960, FL + 20, 1000, "#6A4226", "#8A5A32")
    kc = on(c, "Cotton")
    kn = on(c, "nylon")
    with g.at(700, FL - 330):
        g.rc(0, 0, 300, 60, "#F4F1EA", INK, lw=6, r=8)
        g.text("COTTON", 0, 4, 34, INK, stroke=None)
        if kc > 0:
            for i in range(6):
                g.line([(-140 + i * 55, 30), (-150 + i * 55, 30 + 40 * kc)], "#B8A890", 4)
        cross(g, 0, -90, 34, on(c, "fast"))
    with g.at(1220, FL - 330):
        g.rc(0, 0, 300, 60, "#3E7CB1", INK, lw=6, r=8, a=kn)
        g.text("NYLON", 0, 4, 34, PAL["cream"], stroke=None, a=kn)
        check(g, 0, -90, 34, on(c, "held"))
    with g.screen():
        for i in range(5):
            k = on(c, "years", frac=0.1)
            if k > 0:
                with g.at(220 + i * 50, 200 + i * 8, -0.1 + i * 0.05, k):
                    g.rc(0, 0, 120, 150, "#FFF4E0", INK, lw=5, r=8)
                    g.text(str(1942 + i * 2), 0, 10, 34, INK, stroke=None)
    char2(g, "hiker", 1660, FL + 150, 840, "smile" if kn > 0.5 else "worried", "down", "hold", t=c.gt, view="3q", flip=True)


def s_wordmix(g, c):
    study_1941(g, c.gt)
    k1, k2, k3 = on(c, "Velours"), on(c, "crochet"), on(c, "Velcro", d=0.6)
    with g.screen():
        for i, (txt, k, x) in enumerate((("VELOURS", k1, 560), ("CROCHET", k2, 1360))):
            if k <= 0: continue
            xx = x + (W / 2 - x) * ease_io(k3) * 0.35
            g.rc(xx, 320, 520, 150, ["#B07AD0", "#3E7CB1"][i], INK, lw=8, r=24, a=1 - 0.6 * k3)
            g.text(txt, xx, 330, 84, PAL["cream"], sw=10, a=1 - 0.6 * k3)
            g.text(["velvet", "hook"][i], xx, 440, 50, PAL["cream"], sw=6, a=k * (1 - k3))
        if k3 > 0:
            g.text("VEL", W / 2 - 140, 640, 140, "#E8C4FF", sw=20, sc=back_out(k3, 1.6))
            g.text("CRO", W / 2 + 140, 640, 140, "#BDEBFF", sw=20, sc=back_out(k3, 1.6))
    burr(g, 1600, 780, 40, c.gt)
    char2(g, "hiker", 260, FL + 150, 820, "smile" if k3 > 0.5 else "curious", "down", "explain", t=c.gt, view="3q")


def s_shoes(g, c):
    kitchen(g, c.gt)
    k = clamp(0.5 + 0.5 * math.sin(c.gt * 1.6))
    sneaker(g, 420, 700, 1.0, "#FF6B5B")
    hook_strip(g, 880, 470, 520, k, c.gt, "#FFC93C", "#2F3A4F")
    dog_sit(g, 1350, FL + 150, 1.0, c.gt, "happy", tongue=0.6, col=HIKEDOG)
    if on(c, "brushing") > 0:
        for i in range(6):
            r = rnd(i)
            burr(g, 1350 + (r.random() - 0.5) * 240 + 120 * on(c, "brushing"), 700 + r.random() * 200 - 160 * on(c, "brushing"), 12, i)
    label(g, "SHOES · JACKETS · BAGS", 760, 180, 64, k=on(c, "shoes"))


# ------------------------------------------------------------------ #5 super glue
def s_gunsight(g, c):
    chem_lab(g, c.gt, "#C9DDE8")
    bench(g, 1000, FL + 20, 900, "#5A6A70", "#8A9AA0")
    char2(g, "chemist", 620, FL + 150, 900, "deadpan", "down", "up", t=c.gt, view="3q")
    with g.at(990, 380, 0.1 * math.sin(c.gt)):
        g.circle(0, 0, 110, "#DDF3FF", INK, lw=10, a=0.85)
        g.line([(-70, 0), (70, 0)], "#3E7CB1", 4, a=0.6); g.line([(0, -70), (0, 70)], "#3E7CB1", 4, a=0.6)
        g.ellipse(-40, -40, 20, 36, "#FFFFFF", None, a=0.7, rot=0.6)
    label(g, "CLEAR PLASTIC", 1450, 300, 70, k=on(c, "clear"))
    tag(g, "1942 · SECOND WORLD WAR", k=on(c, "1942", frac=0.05))


def s_too_sticky(g, c):
    chem_lab(g, c.gt, "#C9DDE8")
    bench(g, 1000, FL + 20, 900, "#5A6A70", "#8A9AA0")
    k = on(c, "stuck")
    char2(g, "chemist", 760, FL + 150, 900, "worried" if k > 0.5 else "deadpan", "down", "up", t=c.gt, view="3q")
    with g.at(900 + 20 * math.sin(c.gt * 9) * k, 380):
        g.rc(0, 0, 100, 140, "#DDF3FF", INK, lw=6, r=12, a=0.8)
        g.rc(0, 30, 90, 70, "#E6F4FF", None, r=10)
    for i in range(5):
        glue_drop(g, 1250 + i * 70, FL - 300, 16, on(c, "touched") * (1 - 0.1 * i))
    kz = on(c, "away")
    with g.at(1550, FL - 80):
        g.rc(0, -100, 300, 200, "#8A949E", INK, lw=7, r=10)
        g.rc(0, -100 - 120 * (1 - kz), 280, 30, "#5A6470", INK, lw=5, r=6)
    stamp(g, "TOO STICKY", 1450, 300, on(c, "Useless"))


def s_1951(g, c, stuck=False):
    chem_lab(g, c.gt, "#D8E8C9")
    bench(g, 960, FL + 20, 900, "#5A6A50", "#8A9A70")
    ks = on(c, "glued") if stuck else 0
    refractometer(g, 960, FL - 262, 1.15, ks, c.gt, lid=1 - ks)
    if not stuck:
        glue_drop(g, 1050, FL - 380 + 60 * on(c, "measuring"), 14, 1.0)
    char2(g, "chemist", 480, FL + 150, 880, "shocked" if ks > 0.5 else "curious", "down", "reach_r" if ks > 0.5 else "hold", t=c.gt, view="3q")
    char2(g, "gaslab", 1480, FL + 150, 880, "shocked" if ks > 0.5 else "deadpan", "reach_l" if ks > 0.5 else "down", "down", t=c.gt, view="3q", flip=True)
    if not stuck:
        tag(g, "1951 · NINE YEARS LATER", k=on(c, "Nine", frac=0.05))
    if stuck:
        label(g, "STUCK!", 960, 200, 110, k=pk(c, "good"))


def s_drop(g, c):
    chem_lab(g, c.gt, "#D8E8C9")
    k = on(c, "drop")
    with g.at(960, 560):
        glue_tube(g, 0, -250, 0.8, math.pi, squeeze=k)
        glue_drop(g, 0, -150 + 120 * k, 18, k)
        dx = 260 * (1 - ease_io(on(c, "seconds")))
        g.rc(-150 - dx, 0, 300, 160, "#C98A4A", INK, lw=7, r=10)
        g.rc(150 + dx, 0, 300, 160, "#3E7CB1", INK, lw=7, r=10)
    cross(g, 400, 300, 50, on(c, "heat")); label(g, "HEAT", 400, 400, 56, PAL["cream"], k=on(c, "heat"))
    cross(g, 1520, 300, 50, on(c, "pressure")); label(g, "PRESSURE", 1520, 400, 56, PAL["cream"], k=on(c, "pressure"))
    if on(c, "seconds") > 0:
        with g.screen():
            g.circle(W / 2, 880, 70, "#FFF4E0", INK, lw=7)
            g.text("5s", W / 2, 888, 60, INK, stroke=None)
    char2(g, "chemist", 1700, FL + 150, 760, "smile", "down", "point", t=c.gt, view="3q", flip=True)


def s_water(g, c):
    g.fill_all(g.rgrad(W / 2, H / 2, W * 0.8, "#2F6A8A", "#1E4A64", "#0E2433"))
    g.rect(-100, 700, W + 200, 400, "#C98A4A", INK, lw=8)
    for i in range(16):
        x = 60 + i * 120
        g.ellipse(x, 690, 46, 18, "#8FD3F5", INK, lw=4, a=0.9)
    k = on(c, "lock", frac=0.6)
    n = int(14 * clamp(0.4 + k))
    for i in range(n):
        x = 220 + i * 110
        y = 560 + 30 * math.sin(i * 0.9 + c.gt)
        if i:
            g.line([(x - 110, 560 + 30 * math.sin((i - 1) * 0.9 + c.gt)), (x, y)], PAL["cream"], 10)
        g.circle(x, y, 26, PAL["yellow"], INK, lw=5)
    label(g, "WATER", 360, 820, 70, "#BDEBFF", k=on(c, "water"))
    label(g, "PLASTIC CHAINS", 1300, 380, 72, k=on(c, "chains"))


def s_fingers(g, c):
    kitchen(g, c.gt)
    tag(g, "ON SALE · 1958", k=on(c, "1958", frac=0.05))
    glue_tube(g, 1560, 560, 0.8, 0.5)
    k = on(c, "fingers")
    char2(g, "modern", 520, FL + 170, 920, "shocked" if k > 0.5 else "deadpan", "hold", "hold", t=c.gt, view="3q")
    if k > 0:
        with g.screen():
            with g.at(1080, 470, 0, back_out(k, 1.5)):
                g.circle(0, 0, 250, "#FFF4E0", INK, lw=10)
                tug = 10 * math.sin(c.gt * 14)
                for sd in (-1, 1):
                    g.rc(sd * (70 + tug * 0.5), 20, 150, 90, "#D8A580", INK, lw=7, r=44)
                    g.ellipse(sd * 20, 20, 22, 30, "#F2D6BE", INK, lw=4)
                g.ellipse(0, 20, 16, 50, "#BDEBFF", None, a=0.8)
                for sd in (-1, 1):
                    g.line([(sd * 170, -40), (sd * 215, -70)], INK, 7)
            label(g, "STUCK", 1080, 170, 80, k=pk(c, "fingers"))


# ------------------------------------------------------------------ #4 non-stick
def s_gaslab(g, c):
    gas_lab(g, c.gt)
    for i in range(4):
        gas_cylinder(g, 600 + i * 170, FL + 20, 0.8)
    char2(g, "gaslab", 260, FL + 150, 880, "deadpan", "down", "hold", t=c.gt, view="3q")
    tag(g, "APRIL 1938", k=on(c, "1938", frac=0.05))
    label(g, "FRIDGE GAS", 1640, 220, 60, k=on(c, "refrigerators"))


def s_valve(g, c):
    gas_lab(g, c.gt)
    kv = on(c, "opened")
    gas_cylinder(g, 960, FL + 20, 1.4, 0.0, valve_open=kv)
    char2(g, "gaslab", 560, FL + 150, 880, "suspicious" if on(c, "Nothing") > 0.5 else "deadpan", "down", "reach_r", t=c.gt, view="3q")
    with g.at(960, FL - 560):
        for i in range(3):
            g.circle(30 + i * 50, -20 - i * 30, 8 + i * 4, None, "#FFFFFF", lw=4, a=0.4 * on(c, "Nothing") * (1 - i * 0.3))
    qmark(g, 1250, 300, 130, k=on(c, "gone"), rot=0.15)


def s_weigh(g, c):
    gas_lab(g, c.gt)
    k = on(c, "weighed")
    scale_dial(g, 1100, FL + 20, 1.3, 0.25 + 0.5 * ease_out(k), c.gt, "WEIGHT")
    gas_cylinder(g, 1100, FL - 30, 0.75)
    char2(g, "gaslab", 560, FL + 150, 880, "suspicious", "think", "down", t=c.gt, view="3q")
    label(g, "STILL FULL?", 1100, 160, 90, k=on(c, "same"))
    qmark(g, 1600, 400, 140, k=on(c, "where"), rot=-0.12)


def s_cut(g, c):
    gas_lab(g, c.gt)
    bench(g, 960, FL + 20, 900, "#5A4A40", "#7A6A5A")
    kc = on(c, "cut")
    gas_cylinder(g, 960, FL - 262, 0.9, 1.57 if kc < 0.5 else 0.0, cut=0 if kc < 0.5 else (kc - 0.5) * 2)
    powder_pile(g, 960, FL - 262, 260, on(c, "powder"), c.gt)
    char2(g, "gaslab", 1550, FL + 150, 860, "shocked" if on(c, "powder") > 0.5 else "curious", "down", "point", t=c.gt, view="3q", flip=True)
    label(g, "SLIPPERY WHITE POWDER", 960, 200, 70, k=on(c, "white"))


def s_chain(g, c):
    g.fill_all(g.rgrad(W / 2, H / 2, W * 0.8, "#3E6A8A", "#24445C", "#0E2433"))
    k = clamp(0.2 + on(c, "chains"))
    n = int(12 * k)
    for i in range(n):
        x = 300 + i * 120
        y = 470 + 20 * math.sin(i * 0.7 + c.gt)
        if i:
            g.line([(x - 120, 470 + 20 * math.sin((i - 1) * 0.7 + c.gt)), (x, y)], INK, 14)
        for s in (-1, 1):
            g.line([(x, y), (x, y + s * 90)], INK, 8)
            g.circle(x, y + s * 90, 34 * on(c, "fluorine"), "#7CE07C", INK, lw=5)
        g.circle(x, y, 32, "#5A5A6A", INK, lw=5)
    kd = on(c, "water", frac=0.7)
    if kd > 0:
        bx = 500 + 900 * clamp((c.t - tw(c, "water", frac=0.7)) / 2.0)
        by = 300 + 60 * abs(math.sin(c.t * 6))
        glue_drop(g, bx, by, 30, 1.0)
    label(g, "FLUORINE", 1500, 770, 64, "#7CE07C", k=on(c, "fluorine"))
    with g.screen():
        if on(c, "egg") > 0:
            frying_pan(g, 1500, 880, 0.55, 0, math.sin(c.gt * 3), c.gt)


def s_pan(g, c):
    kitchen(g, c.gt)
    frying_pan(g, 900, 680, 1.4, 0.04 * math.sin(c.gt * 2.6), math.sin(c.gt * 2.6), c.gt)
    steam(g, c.gt, 900, 600, 3, 160)
    tag(g, "PATENT 1941", k=on(c, "1941", frac=0.05))
    label(g, "NON-STICK", 900, 200, 96, k=on(c, "non-stick"))
    if on(c, "empty") > 0:
        with g.screen():
            gas_cylinder(g, 1600, 760, 0.6)
            qmark(g, 1600, 330, 70, k=on(c, "empty"))


# ------------------------------------------------------------------ #3 safety glass
def s_drop_flask(g, c):
    paris_lab(g, c.gt)
    kd = on(c, "dropped", d=0.6)
    char2(g, "painter", 520, FL + 150, 880, "shocked" if kd > 0.2 else "deadpan", "down", "reach_r" if kd > 0 else "hold", t=c.gt, view="3q")
    u = clamp((c.t - tw(c, "dropped")) / 0.55)
    y = 420 + (FL - 420) * u * u
    flask(g, 820, y, 0.6, 1.4 * u, crack=1.0 if u >= 1 else 0.0)
    tag(g, "PARIS · 1903", k=on(c, "1903", frac=0.05))


def s_cracked(g, c, film=False):
    paris_lab(g, c.gt)
    flask(g, 960, FL + 10, 1.4, 0.06, crack=1.0, film=on(c, "film") if film else 0.0)
    if not film:
        label(g, "STILL IN ONE PIECE", 960, 160, 80, k=on(c, "together"))
    else:
        label(g, "PLASTIC FILM", 960, 160, 80, k=on(c, "film"))
        arrow(g, 1500, 400, 1150, 760, k=on(c, "film"))


def s_crash_glass(g, c):
    k = on(c, "crash", d=0.5)
    road_1909(g, c.gt, 960, k)
    tag(g, "EARLY CARS", k=on(c, "Cars", frac=0.05))
    with g.screen():
        if k > 0.5:
            for i in range(3):
                burst(g, 1090, 600, 40, 160, 10, PAL["cream"], 8, k=clamp(k * 1.5 - 0.5))


def s_sandwich(g, c):
    paris_lab(g, c.gt)
    glass_sandwich(g, 960, 520, 1.4, on(c, "pressed", d=0.8), c.gt)
    label(g, "GLASS", 520, 300, 60, "#BDEBFF", k=1.0)
    label(g, "FILM", 520, 520, 60, PAL["yellow"], k=on(c, "film"))
    label(g, "GLASS", 520, 740, 60, "#BDEBFF", k=1.0)
    tag(g, "PATENT 1909", k=on(c, "1909"))
    char2(g, "painter", 1640, FL + 150, 840, "smile", "down", "point", t=c.gt, view="3q", flip=True)


def s_gasmask(g, c):
    paris_lab(g, c.gt)
    bench(g, 760, FL + 20, 760, "#6A4226", "#8A5A32")
    for i in range(3):
        with g.at(520 + i * 240, FL - 330, 0.05 * math.sin(c.gt + i)):
            for s in (-1, 1):
                g.circle(s * 50, 0, 44, "#CDEFFA", INK, lw=10)
                g.ellipse(s * 50 - 12, -12, 10, 18, "#FFFFFF", None, a=0.7)
            g.line([(-6, 0), (6, 0)], INK, 10)
    tag(g, "FIRST WORLD WAR", k=on(c, "First", frac=0.05))
    label(g, "EYEPIECES", 760, 260, 64, k=on(c, "eyepieces"))
    if on(c, "cars") > 0:
        with g.screen():
            with g.at(1500, 700, 0, back_out(on(c, "cars"), 1.5) * 0.6):
                g.rc(0, -110, 520, 120, "#2F5F6A", INK, lw=8, r=30)
                g.rect(80, -330, 120, 150, "#CDEFFA", INK, lw=6)
                for wx in (-170, 170):
                    g.circle(wx, -40, 72, "#2A2A34", INK, lw=8)


def s_windscreen(g, c):
    from flat_car import car_front, crack_paths, draw_cracks
    g.fill_all(g.lgrad(0, 0, 0, H, "#8FB8D8", "#D8ECF5"))
    g.rect(-100, 820, W + 200, 300, "#5A6470", INK, lw=7)
    k = on(c, "breaks", d=0.8)
    car_front(g, 960, 1060, 1.0, ice=0.0, roof_snow=False, wipers=True, lights=1.0)
    if k > 0:
        paths = crack_paths(930, 520, seed=4, n=9, L=300)
        draw_cracks(g, paths, k)
    label(g, "SPIDER WEB", 960, 140, 80, k=on(c, "spider"))
    check(g, 1600, 260, 56, on(c, "piece"))


# ------------------------------------------------------------------ #2 microwave
def s_radar(g, c):
    radar_lab(g, c.gt)
    bench(g, 1250, FL + 40, 620)
    magnetron(g, 1250, FL - 240, 1.05, c.gt, 1.0)
    char2(g, "radar", 600, FL + 150, 900, "deadpan", "down", "point", t=c.gt, view="3q")
    tag(g, "MASSACHUSETTS · 1945", k=on(c, "1945", frac=0.05))
    label(g, "RADAR", 1640, 120, 70, k=on(c, "radar"))


def s_selftaught(g, c):
    radar_lab(g, c.gt)
    bench(g, 960, FL + 40, 900)
    for i in range(6):
        g.rc(1180 + (i % 2) * 8, FL - 290 - i * 40, 260, 40, ["#3E7CB1", "#FF6B5B", "#5ED3B5", "#FFC93C", "#B07AD0", "#E07A3A"][i], INK, lw=5, r=6)
    with g.at(800, FL - 320, -0.1):
        g.poly([(-120, 0), (0, 14), (0, -110), (-120, -124)], "#FFF4E0", INK, lw=5)
        g.poly([(120, 0), (0, 14), (0, -110), (120, -124)], "#FFF4E0", INK, lw=5)
    char2(g, "radar", 520, FL + 150, 900, "curious", "down", "think", t=c.gt, view="3q")
    cross(g, 1500, 220, 46, on(c, "school"))
    label(g, "NO DIPLOMA", 1500, 320, 54, PAL["cream"], k=on(c, "school"))
    label(g, "SELF-TAUGHT", 960, 150, 84, k=on(c, "taught"))
    sparkles(g, c.gt, [(1300, 330), (700, 420)])


def s_popcorn(g, c):
    radar_lab(g, c.gt)
    bench(g, 1100, FL + 40, 900)
    magnetron(g, 1400, FL - 240, 0.9, c.gt, 1.0)
    kp_ = clamp((c.t - tw(c, "popped")) / 0.5)
    for i in range(9):
        r = rnd(i)
        x = 880 + i * 30; y = FL - 290
        if kp_ > 0:
            u = clamp(kp_ * 1.4 - r.random() * 0.4)
            x += (r.random() - 0.5) * 500 * u; y -= 400 * u * (1 - u) * 2 + 0 * u
        popcorn(g, x, y, 24, kp_ if kp_ > 0 else 0.0, r.random() * 3, kernel=kp_ <= 0)
    ke = clamp((c.t - tw(c, "exploded")) / 0.5)
    if on(c, "egg") > 0:
        egg(g, 1100, FL - 360, 0.9, ke)
    char2(g, "radar", 480, FL + 150, 900, "shocked" if ke > 0 else "curious", "down", "up" if ke > 0 else "point", t=c.gt, view="3q")
    with g.screen():
        if c.t < tw(c, "kernels") + 99:
            g.text("SO THE STORY GOES", W / 2, 90, 44, PAL["cream"], sw=6, a=clamp(c.t / 0.3))


def s_shake(g, c):
    g.fill_all(g.rgrad(W / 2, H / 2, W * 0.8, "#E07A3A", "#9A3A20", "#3A1208"))
    k = on(c, "shaking")
    for i in range(10):
        x = 300 + (i % 5) * 330 + 30 * math.sin(c.gt * 40 + i) * k
        y = 380 + (i // 5) * 340 + 20 * math.cos(c.gt * 37 + i) * k
        g.circle(x, y, 56, "#E8463A", INK, lw=6)
        g.circle(x - 52, y - 40, 32, "#FFFFFF", INK, lw=5)
        g.circle(x + 52, y - 40, 32, "#FFFFFF", INK, lw=5)
    label(g, "WATER", 300, 120, 60, "#BDEBFF", k=on(c, "water"))
    label(g, "HEAT!", W / 2, 980, 100, k=on(c, "heat"))
    if on(c, "heat") > 0:
        heatwaves(g, 200, 900, 1700, 900, c.gt, on(c, "heat"), "#FFE29A")


def s_giant(g, c):
    radar_lab(g, c.gt)
    k = on(c, "1947", frac=0.1)
    oven_1947(g, 1100, FL + 60, 1.1, c.gt, on=1.0)
    char2(g, "radar", 600, FL + 60, 860, "shocked", "down", "point", t=c.gt, view="3q")
    tag(g, "FIRST MICROWAVE OVEN · 1947", k=k)
    with g.screen():
        kt = on(c, "tall")
        if kt > 0:
            g.line([(1400, 900), (1400, 900 - 800 * kt)], PAL["yellow"], 8)
            g.text("6 FT", 1530, 520, 70, PAL["yellow"], sw=9)
        kw = on(c, "pounds")
        if kw > 0:
            g.rc(1640, 780, 300, 120, "#3A1626", INK, lw=7, r=20)
            g.text("750 LB", 1640, 788, 70, PAL["yellow"], sw=8, sc=back_out(kw, 1.6))


def s_shrink(g, c):
    kitchen(g, c.gt)
    u = ease_io(clamp((c.t - 0.3) / max(0.5, c.T - 0.8)))
    if u < 0.55:
        oven_1947(g, 960, 720, 1.0 - 0.8 * u / 0.55, c.gt)
    else:
        microwave_modern(g, 960, 720, 0.4 + 0.8 * (u - 0.55) / 0.45, c.gt, on=1.0)
    with g.screen():
        g.rc(W / 2, 150, 420, 110, "#3A1626", INK, lw=7, r=20)
        g.text("1947" if u < 0.5 else "1967", W / 2, 158, 76, PAL["yellow"], sw=8)
    label(g, "+20 YEARS", 1550, 300, 66, PAL["cream"], k=on(c, "twenty"))


def s_honest(g, c):
    radar_lab(g, c.gt)
    bench(g, 960, FL + 40, 1000)
    magnetron(g, 960, FL - 240, 0.85, c.gt, 1.0)
    for i, (cid, x, fl) in enumerate((("engineer", 300, False), ("physicist", 1560, True), ("radar", 620, False))):
        char2(g, cid, x, FL + 150, 820, "deadpan" if i < 2 else "smile", "down", "hold" if i else "think", t=c.gt, view="3q", flip=fl)
    kb = on(c, "melted")
    if kb > 0:
        with g.screen():
            g.glow(1560, 400, 220, "#FFE29A", 0.5 * kb)
            candy_bar(g, 1560, 260, 1.1 * back_out(kb, 1.5), 0.7, c.gt)
    label(g, "LOTS OF TESTS", 960, 160, 76, PAL["cream"], k=on(c, "tests"))


# ------------------------------------------------------------------ #1 penicillin
def s_holiday(g, c):
    london_lab(g, c.gt)
    bench(g, 760, FL + 20, 900, "#4A3020", "#6A4A30")
    for i in range(7):
        petri_dish(g, 470 + i * 95, FL - 300 - (i % 2) * 18, 46, c.gt, mould=1.0 if i == 4 else 0.0, ring=0.3 if i == 4 else 0, seed=i)
    u = ease_out(clamp(c.t / 1.6))
    char2(g, "labdoc", 1700 - 300 * u, FL + 150, 880, "deadpan", "down", "hold", t=c.gt, view="3q", flip=True)
    with g.at(1820 - 300 * u, FL + 40):
        g.rc(0, -60, 160, 110, "#9A4A2A", INK, lw=6, r=12)
        g.rc(0, -125, 60, 20, None, INK, lw=6, r=8)
    tag(g, "LONDON · SEPTEMBER 1928", k=on(c, "1928", frac=0.05))
    label(g, "MESSY BENCH", 760, 200, 66, PAL["cream"], k=on(c, "messy"))


def s_dishes(g, c):
    london_lab(g, c.gt)
    bench(g, 960, FL + 20, 1100, "#4A3020", "#6A4A30")
    km = on(c, "mould", d=1.0)
    for i in range(3):
        petri_dish(g, 560 + i * 400, FL - 330, 150, c.gt, mould=km if i == 1 else 0.0, ring=0.0, seed=i + 2, tilt=0.5)
    label(g, "BACTERIA", 560, 220, 60, PAL["yellow"], k=on(c, "bacteria"))
    label(g, "MOULD", 960, 220, 66, "#7CE0B0", k=km)


def s_ring(g, c):
    london_lab(g, c.gt)
    kr = on(c, "gone", d=1.2)
    petri_dish(g, 960, 560, 360, c.gt, mould=1.0, ring=kr, seed=8, tilt=0.6)
    if on(c, "ring") > 0:
        ring_wave(g, 870, 500, 100, 260, on(c, "ring"), PAL["yellow"], 8)
    label(g, "NOTHING GROWS", 960, 110, 76, k=on(c, "nothing"))
    char2(g, "labdoc", 1660, FL + 150, 760, "shocked", "down", "point", t=c.gt, view="3q", flip=True)


def s_penicillin(g, c):
    london_lab(g, c.gt)
    bench(g, 960, FL + 20, 900, "#4A3020", "#6A4A30")
    petri_dish(g, 760, FL - 320, 120, c.gt, mould=1.0, ring=1.0, seed=8)
    k = on(c, "penicillin")
    with g.at(1200, FL - 280, 0, back_out(k, 1.5) + 1e-3):
        g.rc(0, -110, 130, 220, "#E8F4E0", INK, lw=7, r=20)
        g.rc(0, -235, 60, 40, "#5A4A3A", INK, lw=5)
        g.rc(0, -100, 120, 60, "#FFF4E0", INK, lw=4)
    char2(g, "labdoc", 380, FL + 150, 880, "smile", "down", "point", t=c.gt, view="3q")
    label(g, "PENICILLIN", 1200, 230, 88, k=k)
    label(g, "KILLS BACTERIA", 760, 230, 54, PAL["cream"], k=on(c, "killed") * (1 - k))


def s_unused(g, c):
    london_lab(g, c.gt)
    bench(g, 960, FL + 20, 900, "#4A3020", "#6A4A30")
    with g.at(960, FL - 280):
        g.rc(0, -110, 130, 220, "#E8F4E0", INK, lw=7, r=20)
        g.rc(0, -235, 60, 40, "#5A4A3A", INK, lw=5)
        for i in range(6):
            g.circle(-60 + i * 25, -230 - 30 * ((c.gt * 0.3 + i * 0.3) % 1), 6, "#C9B8A0", None, a=0.6)
    with g.screen():
        yr = 1929 + int(clamp((c.t - tw(c, "years")) / 2.0) * 10)
        g.rc(1500, 300, 260, 300, "#FFF4E0", INK, lw=7, r=12, rot=0.04)
        g.text(str(min(1939, yr)), 1500, 320, 80, INK, stroke=None)
    char2(g, "labdoc", 420, FL + 150, 860, "worried", "down", "shrug", t=c.gt, view="3q")
    label(g, "HARD TO MAKE", 960, 160, 76, PAL["cream"], k=on(c, "hard"))


def s_oxford(g, c, fac=False):
    if fac:
        factory(g, c.gt)
        label(g, "HUGE AMOUNTS", 960, 140, 90, k=on(c, "huge"))
        with g.screen():
            for i in range(12):
                k = clamp(on(c, "factories") * 2 - i * 0.1)
                if k > 0:
                    with g.at(260 + i * 120, 960, 0, back_out(k, 1.5)):
                        g.rc(0, -50, 60, 100, "#E8F4E0", INK, lw=5, r=12)
        return
    chem_lab(g, c.gt, "#D8D0EE")
    bench(g, 960, FL + 20, 1000, "#5A4A70", "#7A6A90")
    for i in range(6):
        g.rc(620 + i * 130, FL - 330, 80, 100, "#E8F4E0", INK, lw=5, r=16)
    for i, (cid, x, fl) in enumerate((("prof", 300, False), ("doctor", 1440, True), ("physicist", 1790, True))):
        char2(g, cid, x, FL + 150, 840 - 40 * i, "smile", "down", "point" if i == 0 else "hold", t=c.gt, view="3q", flip=fl)
    tag(g, "OXFORD · 1940", k=on(c, "1940", frac=0.05))
    check(g, 960, 300, 70, on(c, "cure"))
    label(g, "IT CURES INFECTIONS", 960, 430, 64, PAL["cream"], k=on(c, "cure"))


def s_nobel(g, c):
    museum(g, c.gt, cases=False)
    medal(g, 520, 560, 130, 0.5 + 0.5 * on(c, "Nobel", frac=0.3), c.gt)
    tag(g, "1945", 520, 790, k=on(c, "1945", frac=0.05))
    k = on(c, "millions")
    with g.screen():
        n = int(40 * clamp((c.t - tw(c, "antibiotics")) / 2.5))
        for i in range(n):
            x = 980 + (i % 10) * 82; y = 360 + (i // 10) * 120
            g.circle(x, y - 30, 20, ["#F1CDB0", "#C99470", "#8D5A3C", "#E9BC98"][i % 4], INK, lw=3)
            g.rc(x, y + 14, 46, 54, ["#FF6B5B", "#3E7CB1", "#5ED3B5", "#FFC93C"][i % 4], INK, lw=3, r=14)
        if k > 0:
            g.text("MANY MILLIONS OF LIVES", 1350, 930, 72, PAL["yellow"], sw=12, sc=back_out(k, 1.5))


# ------------------------------------------------------------------ ending
def s_recap(g, c):
    words = ["spring", "Burrs", "glue", "can", "flask", "candy", "dish"]
    lit = {7 - i: on(c, w) for i, w in enumerate(words)}
    museum(g, c.gt, lit=lit)
    with g.screen():
        for i, w in enumerate(words):
            k = on(c, w)
            if k > 0:
                x = 200 + i * 253
                [ex_springs, ex_burr, ex_glue, ex_cyl, ex_flask, ex_candy, ex_dish][i](g, c, x, FL - 140)


def s_why(g, c):
    museum(g, c.gt, lit={n: 0.35 for n in range(1, 8)})
    char2(g, "wy", 960, FL + 120, 760, "curious" if on(c, "wait") > 0.5 else "smile", "think", "down", t=c.gt, view="front")
    label(g, "NOBODY PLANNED THEM", 960, 170, 80, PAL["cream"], k=on(c, "Nobody", frac=0.05) * (1 - on(c, "wait")))
    if on(c, "wait") > 0:
        label(g, "WAIT... WHY?", 960, 170, 110, k=on(c, "wait"))
        qmark(g, 1300, 360, 130, k=on(c, "why"), rot=0.12 * math.sin(c.gt * 3))


def s_comments(g, c):
    museum(g, c.gt, lit={n: 0.6 for n in range(1, 8)})
    char2(g, "wy", 1500, FL + 120, 680, "smile", "down", "wave", t=c.gt, view="3q", flip=True)
    with g.screen():
        k = back_out(clamp(c.t / 0.4), 1.5)
        g.rc(W / 2 - 200, 300, 940, 170, "#FFFFFF", INK, lw=8, r=40)
        g.text("WHICH ONE SURPRISED YOU?", W / 2 - 200, 308, 62, INK, stroke=None, sc=k)
        label(g, "TELL US IN THE COMMENTS", W / 2 - 200, 480, 56, PAL["cream"], k=pk(c, "comments"))


def s_loop(g, c):
    s_hook(g, c, loop=True)


def s_endscreen(g, c):
    from flat_cast import wy_bust
    brand_bg(g, c.gt)
    k = back_out(seg(c.t, 0.0, 0.5), 1.5)
    g.text("TrueWhys", W / 2, 150, 150, PAL["cream"], sw=26, depth=10, sc=0.5 + 0.5 * k)
    g.text("The real story behind life's weirdest whys", W / 2, 250, 46, PAL["yellow"], sw=8, sc=k)
    for i, x in enumerate((560, 1360)):
        kk = back_out(seg(c.t, 0.25 + 0.15 * i, 0.45), 1.5)
        g.rc(x, 580, 640 * kk + 1, 360 * kk + 1, None, PAL["cream"], lw=8, r=22)
    wy_bust(g, c.gt, W / 2, H + 40 + (1 - k) * 600, 1.05, talk=0)
    check_badge(g, W / 2 + 170, 980, 52, pop(c.t, 0.8, 0.4, 2.4))


# ------------------------------------------------------------------ shot list
def P(lid, fn, part=(0, 1), **kw):
    if lid in V.T:
        V.shot(lid, fn, part=part, **kw)


Z = lambda z0, z1, f: push(z0, z1, f)
L = lambda fn, **a: (lambda g, c: fn(g, c, **a))

# cold open + #7 (ch0)
P("O01", s_hook, (0, "Nothing"), cam=Z(1.2, 1.28, (880, 500)), tr="cut", music="mystery", sfx=[(0.0, "hum", 0.35), (0.05, "melt", 0.4), (0.1, "whoosh", 0.3)])
P("O01", s_nothot, ("Nothing", 1), cam=Z(1.0, 1.05, (960, 520)), sfx=[("hot", "bloop", 0.35)])
P("O02", s_your_kitchen, cam=Z(1.0, 1.05, (960, 520)), music="inventive", sfx=[("microwave", "beep3", 0.35), ("kitchen", "ding", 0.35)])
P("O03", s_montage, cam=Z(1.0, 1.04, (960, 540)), sfx=[("toy", "boing", 0.35), ("glue", "pop", 0.35), ("pan", "pop", 0.35), ("dish", "pop", 0.35), ("saved", "shimmer", 0.35)])
P("O04", s_countdown, cam=Z(1.0, 1.05, (960, 520)), sfx=[("Seven", "drum_hit", 0.35), ("world", "chime", 0.4)])
V.pause["O04"] = 0.4
P("K01", card(7, "THE SPRING THAT WALKED", ex_springs), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45), (0.3, "whoosh_soft", 0.3)])
P("K02", s_ship_bench, cam=Z(1.0, 1.05, (1000, 560)), music="story", sfx=[(0.2, "waves", 0.15), ("springs", "boing", 0.25)])
P("K03", s_spring_falls, cam=Z(1.0, 1.04, (900, 560)), music="playful", sfx=[("fell", "clunk", 0.35), ("stepped", "boing", 0.35), ("Coil", "boing", 0.3), ("walking", "boing", 0.3)])
P("K04", s_testing, cam=Z(1.0, 1.05, (960, 540)), sfx=[("steels", "boing", 0.3), ("coils", "ding", 0.35)])
P("K05", s_name, cam=Z(1.0, 1.05, (1000, 520)), music="warm", sfx=[("dictionary", "paper", 0.35), ("Slinky", "chime", 0.4)])
P("K06", s_store, cam=Z(1.0, 1.04, (960, 540)), music="inventive", sfx=[(0.2, "crowd_murmur", 0.2), ("dollar", "coin_single", 0.35), ("Sold", "crowd_cheer", 0.3)])
P("K07", s_stairs_now, cam=Z(1.0, 1.05, (960, 520)), sfx=[(0.3, "boing", 0.25), ("seven", "drum_hit", 0.35)])
V.pause["K07"] = CH_PAUSE
# #6 hook and loop (ch1)
P("V01", card(6, "A WALK WITH A DOG", ex_burr), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45)])
P("V02", s_walk, (0, "Both"), cam=Z(1.0, 1.04, (960, 540)), music="story", sfx=[(0.2, "birds", 0.2), (0.3, "footsteps", 0.2)])
P("V02", L(s_walk, burrs=True), ("Both", 1), cam=Z(1.06, 1.1, (1000, 620)), sfx=[("burrs", "pop", 0.35), ("covered", "bark", 0.25)])
P("V03", s_pull, cam=Z(1.0, 1.05, (900, 560)), music="curious", sfx=[("microscope", "click", 0.35)])
P("V04", s_hooks, cam=Z(1.0, 1.05, (960, 540)), sfx=[(0.1, "shimmer", 0.35), ("loop", "pop", 0.35)])
P("V05", s_question, cam=Z(1.0, 1.05, (960, 540)), sfx=[("question", "confuse", 0.3), ("loops", "click", 0.4)])
P("V06", s_years, cam=Z(1.0, 1.04, (960, 540)), music="story", sfx=[("Cotton", "scrape", 0.3), ("nylon", "pop", 0.35), ("held", "ding", 0.4)])
P("V07", s_wordmix, cam=Z(1.0, 1.04, (960, 520)), music="inventive", sfx=[("Velours", "pop", 0.35), ("crochet", "pop", 0.35), ("Velcro", "chime", 0.4)])
P("V08", s_shoes, cam=Z(1.0, 1.05, (960, 540)), music="playful", sfx=[(0.3, "scrape", 0.3), ("brushing", "bark", 0.3)])
V.pause["V08"] = CH_PAUSE
# #5 super glue (ch2)
P("G01", card(5, "THE GLUE THAT WAS TOO STICKY", ex_glue), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45)])
P("G02", s_gunsight, cam=Z(1.0, 1.05, (960, 540)), music="story", sfx=[("plastic", "shimmer", 0.3)])
P("G03", s_too_sticky, cam=Z(1.0, 1.04, (1000, 540)), sfx=[("stuck", "bloop", 0.35), ("Useless", "drum_hit", 0.3), ("away", "clunk", 0.35)])
P("G04", s_1951, cam=Z(1.0, 1.04, (960, 540)), music="tension", sfx=[("Nine", "whoosh_soft", 0.3), ("measuring", "click", 0.3)])
P("G05", L(s_1951, stuck=True), cam=Z(1.04, 1.1, (960, 500)), sfx=[("glued", "clunk", 0.4), ("good", "sting", 0.4)])
P("G06", s_drop, cam=Z(1.0, 1.04, (960, 540)), music="inventive", sfx=[("heat", "bloop", 0.3), ("pressure", "bloop", 0.3), ("drop", "pop", 0.35), ("seconds", "ding", 0.4)])
P("G07", s_water, cam=Z(1.0, 1.05, (960, 540)), music="curious", sfx=[("water", "shimmer", 0.35), ("chains", "click", 0.35)])
P("G08", s_fingers, cam=Z(1.0, 1.05, (900, 500)), music="playful", sfx=[("1958", "ding", 0.3), ("fingers", "drum_hit", 0.35)])
V.pause["G08"] = CH_PAUSE
# #4 non-stick (ch3)
P("T01", card(4, "THE CAN THAT WASN'T EMPTY", ex_cyl), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45)])
P("T02", s_gaslab, cam=Z(1.0, 1.04, (960, 540)), music="mystery", sfx=[(0.2, "hum", 0.2)])
P("T03", s_valve, cam=Z(1.0, 1.06, (960, 520)), sfx=[("opened", "creak", 0.35), ("Nothing", "hiss", 0.15), ("gone", "confuse", 0.3)])
P("T04", s_weigh, cam=Z(1.0, 1.05, (1000, 520)), sfx=[("weighed", "clunk", 0.35), ("where", "sting", 0.35)])
P("T05", s_cut, cam=Z(1.0, 1.05, (960, 540)), music="curious", sfx=[("cut", "scrape", 0.4), ("powder", "shimmer", 0.4)])
P("T06", s_chain, cam=Z(1.0, 1.04, (960, 540)), sfx=[("chains", "click", 0.35), ("fluorine", "pop", 0.35), ("egg", "boing", 0.3)])
P("T07", s_pan, cam=Z(1.0, 1.05, (960, 520)), music="inventive", sfx=[(0.2, "hiss", 0.15), ("non-stick", "ding", 0.35)])
V.pause["T07"] = CH_PAUSE
# #3 safety glass (ch4)
P("S01", card(3, "BROKEN, BUT IN ONE PIECE", ex_flask), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45)])
P("S02", s_drop_flask, cam=Z(1.0, 1.05, (900, 540)), music="story", sfx=[("dropped", "whoosh", 0.35)])
P("S03", s_cracked, cam=Z(1.0, 1.06, (960, 560)), sfx=[(0.05, "glass_crack", 0.45), ("together", "ding", 0.35)])
P("S04", L(s_cracked, film=True), cam=Z(1.05, 1.1, (960, 600)), music="curious", sfx=[("film", "shimmer", 0.35)])
P("S05", s_crash_glass, cam=Z(1.0, 1.04, (960, 540)), music="tension", sfx=[(0.1, "rumble", 0.25), ("crash", "glass_crack", 0.4)])
P("S06", s_sandwich, cam=Z(1.0, 1.04, (960, 540)), music="inventive", sfx=[("pressed", "clunk", 0.35), ("1909", "ding", 0.35)])
P("S07", s_gasmask, cam=Z(1.0, 1.04, (900, 540)), music="story", sfx=[("eyepieces", "click", 0.3), ("cars", "pop", 0.3)])
P("S08", s_windscreen, cam=Z(1.0, 1.04, (960, 540)), music="warm", sfx=[("breaks", "glass_crack", 0.4), ("piece", "chime", 0.35)])
V.pause["S08"] = CH_PAUSE
# #2 microwave (ch5)
P("M01", card(2, "BACK TO THAT CANDY BAR", ex_candy), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "drum_hit", 0.45)])
P("M02", s_radar, cam=Z(1.0, 1.05, (960, 540)), music="story", sfx=[(0.1, "hum", 0.25), ("radar", "beep3", 0.3)])
P("M03", s_selftaught, cam=Z(1.0, 1.04, (960, 540)), sfx=[("school", "bloop", 0.3), ("taught", "chime", 0.35)])
P("M04", L(s_hook, loop=True), cam=Z(1.05, 1.12, (760, 420)), music="mystery", sfx=[("odd", "sting", 0.35), ("melted", "melt", 0.4)])
P("M05", s_popcorn, cam=Z(1.0, 1.04, (960, 540)), music="playful", sfx=[("popped", "pop", 0.4), ("popped", "bulb_pop", 0.25), ("exploded", "crash", 0.35)])
P("M06", s_shake, cam=Z(1.0, 1.04, (960, 540)), music="curious", sfx=[("shaking", "buzz_fast", 0.25), ("heat", "swell", 0.3)])
P("M07", s_giant, cam=Z(1.0, 1.04, (1000, 520)), music="inventive", sfx=[("1947", "clunk", 0.35), ("tall", "pop", 0.3), ("pounds", "drum_hit", 0.35)])
P("M08", s_shrink, cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.3, "whoosh_soft", 0.35), ("counter", "ding", 0.35)])
P("M09", s_honest, cam=Z(1.0, 1.04, (960, 540)), music="warm", sfx=[("melted", "shimmer", 0.35)])
V.pause["M09"] = CH_PAUSE
# #1 penicillin + ending (ch6)
P("P01", card(1, "THE DIRTY DISH", ex_dish), tr="flash", cam=Z(1.0, 1.04, (960, 540)), music="mystery", sfx=[(0.0, "drum_hit", 0.45), ("saved", "swell", 0.3)])
P("P02", s_holiday, cam=Z(1.0, 1.05, (960, 540)), music="story", sfx=[(0.2, "footsteps", 0.2), ("bench", "clunk", 0.25)])
P("P03", s_dishes, cam=Z(1.0, 1.05, (960, 540)), sfx=[("mould", "shimmer", 0.35)])
P("P04", s_ring, cam=Z(1.0, 1.06, (960, 540)), music="mystery", sfx=[("gone", "sting", 0.35), ("ring", "chime", 0.35)])
P("P05", s_penicillin, cam=Z(1.0, 1.04, (960, 540)), sfx=[("penicillin", "chime", 0.4)])
P("P06", s_unused, cam=Z(1.0, 1.04, (960, 540)), music="dark" if False else "mystery", sfx=[("years", "paper", 0.3)])
P("P07", s_oxford, (0, "By"), cam=Z(1.0, 1.04, (960, 540)), music="warm", sfx=[("cure", "chime", 0.4)])
P("P07", L(s_oxford, fac=True), ("By", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("factories", "clunk", 0.3), ("huge", "ding", 0.35)])
P("P08", s_nobel, cam=Z(1.0, 1.04, (960, 540)), sfx=[("Nobel", "ring_bell", 0.3), ("millions", "swell", 0.3)])
P("E01", s_recap, cam=Z(1.0, 1.03, (960, 540)), music="inventive",
  sfx=[("spring", "pop", 0.3), ("Burrs", "pop", 0.3), ("glue", "pop", 0.3), ("can", "pop", 0.3), ("flask", "pop", 0.3), ("candy", "pop", 0.3), ("dish", "chime", 0.35)])
P("E02", s_why, cam=Z(1.0, 1.05, (960, 520)), music="warm", sfx=[("why", "chime", 0.35)])
P("E03", s_comments, cam=Z(1.0, 1.04, (960, 540)), sfx=[("comments", "pop", 0.4)])
P("E04", s_loop, cam=Z(1.03, 1.08, (900, 540)), music="mystery", sfx=[(0.1, "hum", 0.3), ("pockets", "melt", 0.35)])
V.build()


def _fix_sfx():
    """A word-anchored sound effect belongs to the split shot that contains its word."""
    for sh in V.shots:
        keep = []
        for e in sh["sfx"]:
            off = e[0]
            if isinstance(off, str):
                wd, n = (off.split("#") + ["0"])[:2]
                try:
                    t = V.word_t(sh["line"], wd, int(n))
                except Exception:
                    continue                     # word not in this line: drop instead of failing
                if not (sh["start"] - 0.05 <= t < sh["start"] + sh["dur"]):
                    tgt = [x for x in V.shots if x["line"] == sh["line"] and x["start"] - 0.05 <= t < x["start"] + x["dur"]]
                    if tgt:
                        tgt[0]["sfx"] = tgt[0]["sfx"] + [e]
                    continue
            keep.append(e)
        sh["sfx"] = keep


_fix_sfx()
from flat_split import split_long
split_long(V, maxd=4.6, keep_cam=True)

END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line=V.shots[-1]["line"], fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "7 everyday things invented by accident"), ("K01", "#7 The spring that walked (Slinky)"),
            ("V01", "#6 A walk with a dog (Velcro)"), ("G01", "#5 The glue that was too sticky (super glue)"),
            ("T01", "#4 The can that wasn't empty (non-stick pans)"), ("S01", "#3 Broken, but in one piece (safety glass)"),
            ("M01", "#2 The melted candy bar (microwave oven)"), ("P01", "#1 The dirty dish (penicillin)"), ("E01", "The countdown")]


def chapters():
    out = []
    for lid, name in CHAPTERS:
        ts = [sh["start"] for sh in V.shots if sh["line"] == lid]
        if not ts: continue
        t = 0.0 if lid == "O01" else min(ts)
        out.append(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=10, scale=0.12))
    elif cmd == "qa":
        print(dict(duration=V.duration, shots=len(V.shots), max_shot=max(s["dur"] for s in V.shots if s["kind"] != "end")))
        for s in V.shots:
            if s["dur"] > 5.5 and s["kind"] != "end": print("long shot", s["id"], s["line"], round(s["dur"], 2))
    elif cmd == "times":
        V.qa_numbers()
        print(V.sheet(sys.argv[3], times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.3))
    elif cmd == "chapters":
        print("\n".join(chapters()))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "animatic":
        V.render(str(EP / "animatic/animatic.mp4"), crf=30, preset="veryfast")
    elif cmd == "render":
        V.render(str(EP / "final/B-008.mp4"))
