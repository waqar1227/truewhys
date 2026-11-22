"""B-004 cut Shorts, re-composed vertically (1080x1920) and rewritten (audit §6.3): frame-1 rule, answer in the last 5 s, loop, corner badge.
python episodes/B-004-shape-secrets/shorts/make_short.py <C1|C2|C3|C4> sheet|qa|big <t,..>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, no_sign, sparkles, arrow, burst, ring_wave
from flat_shapes import *

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-coin-ridges", "C2": "C2-yellow-stop-signs", "C3": "C3-bottle-cap-teeth", "C4": "C4-round-manholes"}
EP = HERE / DIRS[SID]
SKIN = "#D8A580"
FLOOR = 1500


# ------------------------------------------------------------------ sets (vertical)
def room1696(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2B1E2A", "#3E2A2E"))
    with g.layer(0.5):
        for i in range(8):
            g.rect(i * 150 - 40, 0, 146, FLOOR, "#4A3236", "#2A1C1E", lw=4)
        g.rect(700, 200, 280, 300, "#0F2238", INK, lw=10, r=6)
        g.circle(860, 290, 44, "#FFF4E0", None, a=0.9)
        g.line([(840, 200), (840, 500)], INK, 10); g.line([(700, 350), (980, 350)], INK, 10)
    g.rect(-100, FLOOR, W + 200, H, "#2A1C1E", None)
    g.glow(540, 1000, 900, "#FFB648", 0.18)


def table(g, y=1250, x=540, w=1200):
    g.rect(x - w / 2, y, w, 44, "#7A5236", INK, lw=8, r=6)
    g.rect(x - w / 2 + 60, y + 44, 40, 500, "#5B3B2E", INK, lw=7); g.rect(x + w / 2 - 100, y + 44, 40, 500, "#5B3B2E", INK, lw=7)


def studio(g, t, a="#1590A0", b="#0B3F4C"):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def mint(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2F3E46", "#22303A"))
    with g.layer(0.5):
        for i in range(3):
            g.rect(60 + i * 340, 260, 300, 700, "#3A4E58", "#1E2A30", lw=6, r=150)
    g.rect(-100, FLOOR, W + 200, H, "#1E2A30", None)


def road1920(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#F6C98B", "#F7E3B5"))
    with g.layer(0.3):
        g.path("M-100 1100 Q300 900 600 1060 Q900 940 1200 1080 L1200 1300 L-100 1300 Z", "#9DBF7A", INK, lw=8)
        for i in range(4):
            g.line([(80 + i * 300, 1100), (80 + i * 300, 700)], "#6E4A3A", 12)
    g.rect(-100, 1260, W + 200, H, "#C9A27A", None)
    g.path("M380 1920 L500 1260 L580 1260 L700 1920 Z", "#B08A62", None)


def street(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#9FD8EE", "#D6F0F7"))
    with g.layer(0.4):
        for i, (bx, bh, col) in enumerate(((-40, 700, "#E07A5F"), (300, 900, "#3D5A80"), (640, 640, "#F2CC8F"), (900, 820, "#81B29A"))):
            g.rect(bx, 1100 - bh, 320, bh + 100, col, INK, lw=8)
            for r_ in range(int(bh / 140)):
                for cc in range(2):
                    g.rect(bx + 50 + cc * 130, 1100 - bh + 50 + r_ * 140, 90, 80, "#DFF4F6", INK, lw=5)
    g.rect(-100, 1150, W + 200, 70, "#B8BEC6", INK, lw=8)
    g.rect(-100, 1220, W + 200, H, "#4A505A", None)


def workshop(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3E5A6E", "#2A3E4E"))
    with g.layer(0.5):
        g.rect(80, 260, 440, 300, "#F6E7C8", INK, lw=10, r=8)
        g.text("BALTIMORE", 300, 360, 56, "#8E2430", stroke=None)
        g.text("1892", 300, 460, 80, INK, stroke=None)
        for i in range(4):
            g.rect(620 + i * 110, 380, 80, 200, "#5FA67A", INK, lw=5, r=20, a=0.8)
        g.rect(580, 580, 480, 26, "#7A5236", INK, lw=6)
    g.rect(-100, FLOOR, W + 200, H, "#22303A", None)


def label(g, txt, x, y, size=96, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def check(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, PAL["mint"], INK, lw=r * 0.12)
        g.line([(-0.45 * r, 0), (-0.1 * r, 0.35 * r), (0.5 * r, -0.35 * r)], INK, r * 0.2)


def bubble(g, x, y, txt, k, col="#FFFFFF", tail=-1, size=60):
    if k <= 0.01: return
    w = g.text_w(txt, size) + 80
    with g.at(x, y, 0, back_out(clamp(k), 1.6)):
        g.poly([(tail * 30, 40), (tail * 90, 110), (tail * 80 - 50 * tail, 40)], col, INK, lw=7)
        g.rc(0, 0, w, size * 1.9, col, INK, lw=7, r=40)
        g.text(txt, 0, 4, size, "#22181B", stroke=None)


# ------------------------------------------------------------------ C1 coin ridges
def c1_hook(g, c):
    """Frame 1: giant silver coin mid-snip filling the frame, the clipper close behind it."""
    room1696(g, c.gt)
    char2(g, "clipper", 330, 2560, 1900, "suspicious", "reach_r", "reach_r", t=c.gt)
    candle(g, 900, 1500, 1.3, c.gt)
    k = 0.35 + 0.15 * math.sin(c.gt * 4)
    coin(g, 690, 1300, 250, "silver", ridges=False, clip=k, face="head", glint=1.0)
    scissors(g, 830, 1300, 1.7, 0.6 - 0.4 * math.sin(c.gt * 4), rot=math.pi)


def c1_hook2(g, c):
    """'That's why yours have ridges': the clipped coin turns into a modern ridged coin, rim glows."""
    room1696(g, c.gt)
    char2(g, "clipper", 330, 2560, 1900, "shocked", "reach_r", "reach_r", t=c.gt)
    candle(g, 900, 1500, 1.3, c.gt)
    k = ease_out(seg(c.t, 0.1, 0.4))
    coin(g, 690, 1300, 250, "silver", ridges=k > 0.5, clip=0.35 * (1 - k), face="head", glint=1.0)
    g.circle(690, 1300, 250, None, PAL["yellow"], lw=16, a=k)
    label(g, "RIDGES", 690, 960, 120, k=pop(c.t, 0.25, 0.3))


def c1_london(g, c):
    room1696(g, c.gt)
    table(g)
    char2(g, "clipper", 540, 2500, 1900, "smug", "reach_r", "reach_l", t=c.gt)
    label(g, "LONDON · 1696", W / 2, 520, 100, PAL["cream"], k=pop(c.t, 0.05, 0.3))


def c1_slivers(g, c):
    room1696(g, c.gt)
    table(g, 1150)
    for i in range(3):
        coin(g, 270 + i * 270, 1050, 120, "silver", ridges=False, clip=ease_out(clamp(c.u * 3 - i)), face="head")
    for i in range(int(c.u * 10)):
        with g.at(200 + (i * 97) % 700, 1180 + (i % 3) * 10, i):
            g.path("M-26 -6 Q0 -14 26 -6 L22 2 Q0 -4 -22 2 Z", SILVER, INK, lw=4)
    label(g, "SNIP", 800, 760, 110, "#FF6B5B", k=pop(c.t, 0.1, 0.3), rot=0.1)


def c1_spend(g, c):
    room1696(g, c.gt)
    char2(g, "clipper", 280, 2050, 1500, "smug", "down", "reach_r", t=c.gt)
    char2(g, "worker", 820, 2050, 1500, "bored", "down", "reach_l", t=c.gt, prop=False, flip=True)
    k = ease_io(seg(c.t, 0.2, 0.8))
    coin(g, lerp(470, 640, k), 1080, 60, "silver", ridges=False, clip=0.8, face=None)


def c1_treason(g, c):
    mint(g, c.gt)
    char2(g, "guard", 300, 2150, 1550, "angry", "down", "hold", t=c.gt)
    with g.at(760, 900, -0.05, back_out(seg(c.t, c.w("treason") - 0.2, 0.35), 1.8)):
        g.rc(0, 0, 520, 360, "#F3E2BC", INK, lw=9, r=10)
        g.text("CLIPPING", 0, -60, 76, INK, stroke=None)
        g.text("= TREASON", 0, 40, 76, "#8E2430", stroke=None)


def c1_wobbly(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    for i in range(3):
        y = 560 + i * 380
        pts = [(540 + 170 * (1 + 0.08 * math.sin(a * 3 + i * 2) + 0.05 * math.cos(a * 5)) * math.cos(a),
                y + 150 * (1 + 0.08 * math.sin(a * 3 + i * 2)) * math.sin(a)) for a in [j * TAU / 40 for j in range(40)]]
        g.poly(pts, SILVER, INK, lw=8)
    qmark(g, 880, 520, 170, PAL["yellow"], 0.1, pop(c.t, c.w("nobody") - 0.1, 0.3))


def c1_press(g, c):
    mint(g, c.gt)
    k = abs(math.sin(c.gt * 2.6))
    with g.at(540, 300):
        g.rc(0, 900, 520, 60, "#5A5A6A", INK, lw=8, r=8)
        g.rc(-220, 640, 60, 560, "#4A4F5A", INK, lw=8); g.rc(220, 640, 60, 560, "#4A4F5A", INK, lw=8)
        g.rc(0, 360, 520, 70, "#4A4F5A", INK, lw=8, r=10)
        g.rc(0, 560 + 160 * k, 70, 300, "#9AA3AD", INK, lw=7)
        a = math.cos(c.gt * 2.6)
        g.line([(-360 * a, 370), (360 * a, 370)], "#7A5236", 22)
    for i in range(min(6, int(c.t * 2))):
        coin(g, 300 + (i % 3) * 240, 1400 - (i // 3) * 50, 80, "silver", ridges=True, face="head")
    label(g, "MADE BY MACHINE", W / 2, 420, 90, k=pop(c.t, 0.1, 0.3))


def c1_newton(g, c):
    mint(g, c.gt)
    char2(g, "newton", 540, 2300, 1750, "suspicious", "down", "point", t=c.gt)
    label(g, "ISAAC NEWTON", W / 2, 440, 104, k=pop(c.t, c.w("Isaac") - 0.1, 0.3))


def c1_snip_test(g, c):
    studio(g, c.gt, "#3E5A7A", "#1A2638")
    k = ease_io(seg(c.t, 0.2, 0.8))
    coin_edge(g, 540, 1000, 980, 300, "silver", ridges=True, gap=k, gap_glow=ease_out(seg(c.t, c.w("gone") - 0.2, 0.3)))
    scissors(g, 540 + 120, 760, 1.6, 0.5 + 0.5 * math.sin(c.gt * 10), rot=math.pi / 2)
    label(g, "GONE!", W / 2, 1380, 120, "#FF6B5B", k=pop(c.t, c.w("gone") - 0.1, 0.3))


def c1_trap(g, c):
    """Last shot = the coin from frame 1 (loop), now with ridges and a glowing rim."""
    room1696(g, c.gt)
    char2(g, "clipper", 330, 2560, 1900, "shocked" if c.t > c.w("trap") - 0.2 else "suspicious", "reach_r", "reach_r", t=c.gt)
    candle(g, 900, 1500, 1.3, c.gt)
    coin(g, 690, 1300, 250, "silver", ridges=True, face="head", glint=1.0)
    g.circle(690, 1300, 250, None, PAL["yellow"], lw=16, a=ease_out(seg(c.t, c.w("trap") - 0.2, 0.4)))
    label(g, "A TRAP", 690, 960, 120, k=pop(c.t, c.w("trap") - 0.1, 0.3))


# ------------------------------------------------------------------ C2 yellow stop signs
def c2_hook(g, c):
    road1920(g, c.gt)
    road_sign(g, 640, 1010, 300, "octagon", "#F2C14E", "STOP", INK, post=900, border=INK)
    char2(g, "engineer", 260, 2560, 1700, "suspicious", "down", "point", t=c.gt)


def c2_hook2(g, c):
    """'So why did they turn red?': the yellow sign flips to red, question mark pops."""
    road1920(g, c.gt)
    k = ease_io(seg(c.t, 0.05, 0.35))
    sc = abs(math.cos(k * math.pi))                                  # card flip
    with g.at(640, 1010, 0, max(0.05, sc), 1.0):
        road_sign(g, 0, 0, 300, "octagon", "#F2C14E" if k < 0.5 else "#D7263D", "STOP", INK if k < 0.5 else "#FFFFFF", post=900, border=INK)
    char2(g, "engineer", 260, 2560, 1700, "curious", "down", "think", t=c.gt)
    qmark(g, 930, 690, 150, PAL["yellow"], 0.1, pop(c.t, 0.4, 0.3))


def c2_engineers(g, c):
    road1920(g, c.gt)
    char2(g, "engineer", 300, 2150, 1450, "deadpan", "down", "point", t=c.gt)
    char2(g, "prof", 800, 2150, 1450, "curious", "down", "down", t=c.gt, flip=True)
    label(g, "1923", W / 2, 420, 140, k=pop(c.t, 0.05, 0.3))


def c2_rule(g, c):
    studio(g, c.gt, "#B85A3E", "#4A1E14")
    rows = [("square", "#F4F1EA"), ("diamond", "#F2C14E"), ("octagon", "#F2C14E"), ("circle", "#F4F1EA")]
    for i, (sh, col) in enumerate(rows):
        k = back_out(seg(c.t, c.w("sides") - 0.4 + i * 0.25, 0.35), 1.6)
        if k > 0:
            with g.at(540, 1500 - i * 300, 0, k):
                road_sign(g, 0, 0, 120, sh, col, "", border=INK)
    ka = ease_out(seg(c.t, c.w("danger") - 0.5, 0.6))
    arrow(g, 900, 1600, 900, 1600 - 1050 * ka, "#FF5B4B", w=28, k=ka)
    label(g, "MORE DANGER", W / 2, 360, 96, k=pop(c.t, c.w("danger") - 0.2, 0.3))


def c2_shapes(g, c):
    road1920(g, c.gt)
    k1 = back_out(seg(c.t, c.w("circle") - 0.2, 0.35), 1.6)
    k2 = back_out(seg(c.t, c.w("Eight") - 0.2, 0.35), 1.6)
    if k1 > 0:
        with g.at(300, 820, 0, k1): road_sign(g, 0, 0, 200, "circle", "#FFF4E0", "RR", INK, post=600)
    if k2 > 0:
        with g.at(780, 820, 0, k2): road_sign(g, 0, 0, 200, "octagon", "#F2C14E", "STOP", INK, post=600, border=INK)


def c2_thirty(g, c):
    road1920(g, c.gt)
    road_sign(g, 540, 800, 340, "octagon", "#F2C14E", "STOP", INK, post=900, border=INK)
    label(g, "1924 – 1954", W / 2, 380, 110, k=pop(c.t, c.w("thirty") - 0.2, 0.3))


def c2_why(g, c):
    road1920(g, c.gt)
    char2(g, "engineer", 540, 2350, 1750, "suspicious" if c.t < c.w("1954") else "shocked", "hip", "hip", t=c.gt)
    road_sign(g, 860, 700, 150, "octagon", "#D7263D", "STOP", post=0)
    qmark(g, 860, 420, 150, PAL["yellow"], 0.1, pop(c.t, c.w("why") - 0.2, 0.3))


def c2_fade(g, c):
    road1920(g, c.gt)
    g.glow(900, 200, 400, "#FFF4C2", 0.6); g.circle(900, 200, 120, "#FFE58A", INK, lw=8)
    fd = ease_io(seg(c.t, c.w("faded") - 0.3, 1.2))
    road_sign(g, 540, 820, 330, "octagon", "#D7263D", "STOP", post=900, fade=fd)
    label(g, "FADED", W / 2, 1360, 120, "#FF6B5B", k=pop(c.t, c.w("faded") + 0.2, 0.3))


def c2_pink(g, c):
    """Last shot loops to frame 1: the same road, sign and engineer."""
    road1920(g, c.gt)
    road_sign(g, 640, 1010, 300, "octagon", "#D7263D", "STOP", post=900, fade=1.0)
    char2(g, "engineer", 260, 2560, 1700, "deadpan" if c.t < c.w("miss") - 0.3 else "shocked", "down", "point", t=c.gt)


# ------------------------------------------------------------------ C3 bottle caps
def c3_hook(g, c):
    studio(g, c.gt, "#D7263D", "#5A1020")
    char2(g, "modern", 800, 2560, 1800, "suspicious", "point", "down", t=c.gt, prop=False, flip=True)
    n = min(21, int(c.gt * 9))
    bottle_cap(g, 400, 1150, 340, 21, hi=n - 1)


def c3_count(g, c):
    studio(g, c.gt, "#D7263D", "#5A1020")
    n = min(21, int((c.gt) * 9))
    bottle_cap(g, 540, 900, 440, 21, hi=n - 1, hi_all=1.0 if n >= 21 else 0.0)
    label(g, str(n), W / 2, 1560, 220, k=1.0)


def c3_painter(g, c):
    workshop(g, c.gt)
    char2(g, "painter", 360, 2250, 1650, "curious", "down", "reach_r", t=c.gt)
    bottle_cap(g, 800, 1000, 190, 24)
    label(g, "WILLIAM PAINTER", W / 2, 760, 84, k=pop(c.t, c.w("William") - 0.1, 0.3))


def c3_crown(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    bottle_cap(g, 540, 960, 360, 24, col="#3E7CB1")
    with g.screen():
        g.text("♛", 540, 480, 200, PAL["yellow"], sw=14, sc=pop(c.t, c.w("crown") - 0.2, 0.3), font="DejaVu Sans")


def c3_24(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    bottle_cap(g, 540, 900, 380, 24, hi_all=1.0, col="#3E7CB1")
    label(g, "24", W / 2, 1520, 240, k=pop(c.t, 0.1, 0.3))


def c3_advice(g, c):
    workshop(g, c.gt)
    char2(g, "painter", 300, 2150, 1450, "smug", "down", "point", t=c.gt)
    char2(g, "gillette", 800, 2150, 1450, "curious", "down", "down", t=c.gt, flip=True)
    bubble(g, 420, 640, "USE ONCE.", seg(c.t, c.w("once") - 0.3, 0.3), size=64)
    bubble(g, 520, 800, "THROW AWAY.", seg(c.t, c.w("throw") - 0.3, 0.3), "#FFE08A", size=64)


def c3_gillette(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    char2(g, "gillette", 540, 2560, 1750, "smug", "down", "point", t=c.gt)
    label(g, "KING GILLETTE", W / 2, 420, 110, k=pop(c.t, c.w("King") - 0.1, 0.3))
    razor_blade(g, 540, 640, 1.4 * back_out(seg(c.t, c.w("Gillette") - 0.1, 0.35), 1.6) + 0.01, -0.1, glint=0.6)


def c3_21(g, c):
    studio(g, c.gt, "#D7263D", "#5A1020")
    k = ease_io(seg(c.t, 0.1, 0.7))
    bottle_cap(g, 540, 620, 240, 24, col="#3E7CB1")
    arrow(g, 540, 900, 540, 1020, PAL["yellow"], w=26, k=k)
    bottle_cap(g, 540, 1300, 260, 21, hi_all=k)
    label(g, "21", 880, 1300, 160, k=pop(c.t, c.w("twenty-one") - 0.2, 0.3))


def c3_end(g, c):
    """Last shot loops to frame 1: the same man and the same 21-tooth cap; fizz vs opener."""
    studio(g, c.gt, "#D7263D", "#5A1020")
    char2(g, "modern", 800, 2560, 1800, "smug" if c.t > c.w("pop") - 0.3 else "curious", "point", "down", t=c.gt, prop=False, flip=True)
    bottle_cap(g, 400, 1150, 340, 21, hi_all=1.0)
    with g.screen():
        g.text("FIZZ IN", 400, 700, 80, PAL["cream"], sw=14, sc=pop(c.t, c.w("fizz") - 0.2, 0.3))
        g.text("EASY OFF", 400, 1600, 80, PAL["yellow"], sw=14, sc=pop(c.t, c.w("pop") - 0.2, 0.3))


# ------------------------------------------------------------------ C4 manholes
def c4_hook(g, c):
    street(g, c.gt)
    char2(g, "sewer", 330, 2350, 1750, "worried", "reach_r", "reach_r", t=c.gt)
    manhole(g, 640, 1500, 320, "square", tilt=0.4, lid=False)
    with g.at(690, 1080, 0.15 + 0.05 * math.sin(c.gt * 3)):
        g.rc(0, 0, 480, 480, IRON, INK, lw=10, r=8)
        for i in range(-3, 4):
            g.line([(-180, i * 60), (180, i * 60)], "#5E6470", 8)


def c4_edge(g, c):
    street(g, c.gt)
    char2(g, "sewer", 300, 2250, 1650, "worried", "reach_r", "reach_r", t=c.gt)
    k = ease_io(seg(c.t, c.w("edge") - 0.6, 0.6))
    manhole(g, 650, 1500, 300, "square", tilt=0.4, lid=False)
    with g.at(700, 1050, 0, 1 - 0.9 * k, 1.0):
        g.rc(0, 0, 440, 440, IRON, INK, lw=10, r=8)


def c4_diag(g, c):
    """Top view: the lid on its edge lines up with the diagonal and drops."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#9AA3AD", "#7E8790"))
    r = 300
    cx, cy = 540, 960
    g.poly([(cx + px, cy + py) for px, py in ngon_pts(4, r * 1.3, math.pi / 4)], "#5E6470", INK, lw=10)
    g.poly([(cx + px, cy + py) for px, py in ngon_pts(4, r * 1.18, math.pi / 4)], "#141820", INK, lw=6)
    kt = ease_io(seg(c.t, 0.1, 0.6)); kf = ease_in(seg(c.t, c.w("diagonal") - 0.1, 0.5))
    side = r * 1.18 * 1.414 * 0.98
    with g.at(cx, cy, (math.pi / 4) * kt, 1 - 0.55 * kf, 1 - 0.55 * kf):
        g.rc(0, 0, side, 36, mix("#C9A27A", "#22181B", kf), INK, lw=8, r=6, a=1 - 0.6 * kf)
    g.line([(cx - r * 1.18 * 1.414, cy), (cx + r * 1.18 * 1.414, cy)], PAL["yellow"], 8, dash=([22, 16], 0), a=kt)
    label(g, "DIAGONAL", W / 2, 520, 100, k=pop(c.t, c.w("diagonal") - 0.3, 0.3))


def c4_clang(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3A3F48", "#151820"))
    g.rect(-100, 0, W + 200, 300, "#4A505A", INK, lw=8)
    g.rect(340, 0, 400, H, "#0E1116", None)
    g.rect(280, 0, 60, H, "#6E6650", INK, lw=6); g.rect(740, 0, 60, H, "#6E6650", INK, lw=6)
    k = ease_in(seg(c.t, 0.0, 0.6))
    with g.at(540, 200 + 900 * k, 0.3 + 2.4 * k):
        g.rc(0, 0, 380, 50, IRON, INK, lw=8, r=6)
    char2(g, "sewer", 540, 2050, 750, "shocked", "up", "up", t=c.gt)
    if c.t > c.w("Clang") - 0.05:
        burst(g, 540, 1180, 120, 260, 12, PAL["yellow"], 14, k=seg(c.t, c.w("Clang"), 0.3))
        label(g, "CLANG!", W / 2, 560, 140, k=pop(c.t, c.w("Clang") - 0.05, 0.25), rot=0.1)


def c4_circle(g, c):
    studio(g, c.gt, "#1590A0", "#0B3F4C")
    rot = c.gt * 1.4
    g.circle(540, 960, 330, IRON, INK, lw=10)
    g.circle(540, 960, 250, None, "#5E6470", lw=8)
    for sd in (-1, 1):
        g.line([(540 + sd * 330, 500), (540 + sd * 330, 1420)], PAL["yellow"], 10)
    with g.at(540, 960, rot):
        g.line([(-330, 0), (330, 0)], PAL["cream"], 8, dash=([18, 14], 0))
    label(g, "SAME WIDTH", W / 2, 400, 110, k=pop(c.t, c.w("same") - 0.2, 0.3))


def c4_never(g, c):
    street(g, c.gt)
    x = 380 + 300 * ease_io(seg(c.t, c.w("roll") - 0.5, 1.0))
    char2(g, "sewer", x - 200, 2150, 1450, "smug", "reach_r", "reach_r", t=c.gt)
    with g.at(x + 200, 1350, (x - 380) / 200):
        g.circle(0, 0, 230, IRON, INK, lw=10)
        g.circle(0, 0, 180, None, "#5E6470", lw=8)
        for i in range(-3, 4): g.line([(-160, i * 40), (160, i * 40)], "#5E6470", 7)
    check(g, 880, 700, 80, seg(c.t, c.w("never") - 0.2, 0.3))


def c4_end(g, c):
    """Last shot loops to frame 1: the worker over the hole, now with a round lid."""
    street(g, c.gt)
    char2(g, "sewer", 330, 2350, 1750, "smug" if c.t < c.w("square") - 0.2 else "worried", "reach_r", "reach_r", t=c.gt)
    manhole(g, 640, 1500, 320, "circle", tilt=0.4)
    if c.t > c.w("square") - 0.2:
        with g.at(690, 1080, 0.15, pop(c.t, c.w("square") - 0.2, 0.3)):
            g.rc(0, 0, 360, 360, IRON, INK, lw=10, r=8, a=0.9)
        qmark(g, 900, 760, 150, PAL["yellow"], 0.1, pop(c.t, c.w("square") - 0.1, 0.3))


# ------------------------------------------------------------------ the four Shorts
def build():
    if SID == "C1":
        V = Video(EP, title=("HANGED FOR", "CUTTING COINS?"), cap_y=0.72, music="mystery", sid="B004C1",
                  keys={"ridges", "1696", "treason", "newton", "machine", "gone", "trap", "thieves", "snip"})
        V.shot("H1", c1_hook, (0, "That's"), sfx=[(0.0, "click", 0.4), ("hanged", "drum_hit", 0.4)])
        V.shot("H1", c1_hook2, ("That's", 1), cam=push(1.0, 1.06, (690, 1300)), sfx=[(0.15, "chime", 0.35)])
        V.shot("L01", c1_london, (0, "People"), cam=push(1.0, 1.05, (540, 900)))
        V.shot("L01", c1_slivers, ("People", "and"), sfx=[(0.1, "click", 0.4), (0.5, "click", 0.4)])
        V.shot("L01", c1_spend, ("and", 1), sfx=[(0.2, "coin_single", 0.4)])
        V.shot("L02", c1_treason, (0, "But"), sfx=[("treason", "drum_hit", 0.45)])
        V.shot("L02", c1_wobbly, ("But", 1))
        V.shot("L03", c1_press, (0, "And"), sfx=[(0.3, "drum_hit", 0.25)])
        V.shot("L03", c1_newton, ("And", 1), cam=push(1.0, 1.06, (540, 800)), sfx=[("Isaac", "sting", 0.4)])
        V.shot("L04", c1_snip_test, sfx=[("gone", "ding", 0.45)])
        V.shot("L05", c1_trap, cam=push(1.0, 1.04, (690, 1300)), sfx=[("trap", "chime", 0.45)])
    elif SID == "C2":
        V = Video(EP, title=("STOP SIGNS", "WERE YELLOW?!"), cap_y=0.72, music="curious", sid="B004C2",
                  keys={"yellow", "1923", "sides", "danger", "eight", "thirty", "1954", "faded", "pink", "red"})
        V.shot("H1", c2_hook, (0, "So"), sfx=[(0.0, "pop", 0.35)])
        V.shot("H1", c2_hook2, ("So", 1), sfx=[(0.05, "rush", 0.3)])
        V.shot("L01", c2_engineers, (0, "the"), cam=push(1.0, 1.05, (540, 900)))
        V.shot("L01", c2_rule, ("the", 1), sfx=[("danger", "sting", 0.35)])
        V.shot("L02", c2_shapes, sfx=[("circle", "pop", 0.4), ("Eight", "pop", 0.4)])
        V.shot("L03", c2_thirty, cam=push(1.0, 1.06, (540, 800)), sfx=[("yellow", "swell", 0.35)])
        V.shot("L04", c2_why, sfx=[("1954", "hmm", 0.35)])
        V.shot("L05", c2_fade, (0, "And"), cam=push(1.0, 1.05, (540, 820)), sfx=[("faded", "melt", 0.4)])
        V.shot("L05", c2_pink, ("And", 1), sfx=[("miss", "rush", 0.3)])
    elif SID == "C3":
        V = Video(EP, title=("COUNT THE TEETH", "ON A BOTTLE CAP"), cap_y=0.72, music="playful", sid="B004C3",
                  keys={"twenty-one", "21", "1892", "baltimore", "crown", "twenty-four", "24", "gillette", "fizz", "pop"})
        V.shot("H1", c3_hook, sfx=[(0.3, "tick", 0.3)])
        V.shot("L01", c3_count, (0, "Why"), sfx=[(0.1, "tick", 0.3)])
        V.shot("L01", c3_hook, ("Why", 1), cam=push(1.1, 1.15, (500, 1100)))
        V.shot("L02", c3_painter, (0, "like"), sfx=[("crimped", "click", 0.4)])
        V.shot("L02", c3_crown, ("like", 1))
        V.shot("L03", c3_24, sfx=[(0.1, "ding", 0.4)])
        V.shot("L04", c3_advice, (0, "His#1"), music="curious")
        V.shot("L04", c3_gillette, ("His#1", 1), sfx=[("Gillette", "shimmer", 0.45)])
        V.shot("L05", c3_21, (0, "Enough"), sfx=[("twenty-one", "ding", 0.45)])
        V.shot("L05", c3_end, ("Enough", 1), cam=push(1.0, 1.04, (500, 1100)), sfx=[("pop", "pop", 0.45)])
    else:
        V = Video(EP, title=("WHY IS EVERY MANHOLE", "COVER ROUND?"), cap_y=0.72, music="playful", sid="B004C4",
                  keys={"round", "square", "edge", "diagonal", "clang", "circle", "width", "never", "roll"})
        V.shot("H1", c4_hook, sfx=[(0.0, "creak", 0.35)])
        V.shot("L01", c4_edge, cam=push(1.0, 1.05, (640, 1200)), sfx=[("edge", "creak", 0.35)])
        V.shot("L02", c4_diag, (0, "Clang"))
        V.shot("L02", c4_clang, ("Clang", 1), sfx=[("Clang", "drum_hit", 0.6)])
        V.shot("L03", c4_circle, sfx=[("same", "ding", 0.35)])
        V.shot("L04", c4_never, sfx=[("never", "ding", 0.4)])
        V.shot("L05", c4_end, cam=push(1.0, 1.04, (640, 1200)), sfx=[("square", "hmm", 0.35)])
    V.build()
    split_long(V)
    return V


def _cont(fn, sh0):
    """Run a scene with the clock of the original (unsplit) shot, so its animations continue across the cut."""
    def f(g, c):
        off = c.sh["start"] - sh0["start"]
        c.sh = dict(c.sh, start=sh0["start"]); c.t += off; c.T = sh0["dur"]; c.u = clamp(c.t / c.T) if c.T > 0 else 0
        fn(g, c)
    return f


def split_long(V, maxd=2.5):
    out = []
    for sh in V.shots:
        if sh["kind"] == "end" or sh["dur"] <= maxd + 0.5:
            out.append(sh); continue
        n = math.ceil(sh["dur"] / maxd)
        edges = [round((sh["start"] + sh["dur"] * k / n) * FPS) / FPS for k in range(n + 1)]
        for k in range(n):
            part = dict(sh, start=edges[k], dur=edges[k + 1] - edges[k])
            part["sfx"] = []
            for e in sh["sfx"]:                      # each sound effect goes to the piece that contains its moment
                off, nm = e[0], e[1]
                t_abs = (V.word_t(sh["line"], *((off.split("#")[0], int(off.split("#")[1])) if "#" in off else (off, 0)))
                         if isinstance(off, str) else sh["start"] + off)
                if edges[k] <= t_abs < edges[k + 1] or (k == n - 1 and t_abs >= edges[-1]):
                    part["sfx"].append(e if isinstance(off, str) else (t_abs - edges[k],) + tuple(e[1:]))
            if k:
                part["fn"] = _cont(sh["fn"], sh)
                part["tr"] = "cut"
                part["music"] = None
                part["cam"] = push(1.16, 1.2, (540, 1050)) if k % 2 else push(0.96, 1.0, (540, 960))
            out.append(part)
    # keep every SFX on its own word: SFX of the first part with word anchors are fine; numeric offsets beyond the part move along
    for i, sh in enumerate(out):
        sh["id"] = f"{V.sid}_{i:02d}"
    V.shots = out


if __name__ == "__main__":
    V = build()
    cmd = sys.argv[2] if len(sys.argv) > 2 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=8, scale=0.14))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[3].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / f"final/B-004-{SID}.mp4"))
