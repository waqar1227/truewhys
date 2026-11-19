"""B-004 (L4) "Why Everyday Things Are Shaped So Weirdly" — long video, Style F + cast v2.1, 1920x1080 (audit §4, §6.4, §6.5).
python episodes/B-004-shape-secrets/make.py sheet|render|qa|big <t,t,..>|chapters
Every chapter is its own set (1696 candle room, mint, street, 1920s road, 1860s factory + court, 1892 Baltimore workshop, kitchen, bakery).
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, no_sign, sparkles, arrow, burst, ring_wave
from flat_shapes import *

V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="mystery",
          keys={"ridges", "treason", "hanged", "newton", "chaloner", "silver", "round", "width", "fall", "reuleaux", "circle", "eight", "sides",
                "yellow", "red", "1954", "1923", "flat", "square", "won", "1871", "knight", "twenty-one", "21", "24", "gillette", "razor",
                "holes", "steam", "docking", "puffs", "optional", "manufacturing", "accident", "1696", "1699", "clang", "trap", "bump"})
FLOOR = 930
CH_PAUSE = 1.4          # breathing room (chapter banner) after the last line of each chapter


# ------------------------------------------------------------------ shared helpers
def banner(g, c, txt, sub=None, t0=0.0):
    """Chapter banner: slides in at the top-left in the first 2.4 s of a chapter."""
    t = c.t - t0
    if t > 2.8 or t < 0: return
    k = back_out(seg(t, 0, 0.35), 1.4) * (1 - ease_in(seg(t, 2.3, 0.4)))
    with g.screen():
        with g.at(80 - 700 * (1 - k), 96, -0.02):
            w = g.text_w(txt, 64) + 70
            g.rect(0, -46, w, 92, PAL["yellow"], INK, lw=8, r=18)
            g.text(txt, w / 2, 4, 64, INK, stroke=None)
            if sub:
                g.text(sub, 20, 82, 40, PAL["cream"], sw=8, anchor="l")


def bubble(g, x, y, txt, k, col="#FFFFFF", tail=-1, size=58, w=None):
    if k <= 0.01: return
    w = w or g.text_w(txt, size) + 80
    with g.at(x, y, 0, back_out(clamp(k), 1.6)):
        g.poly([(tail * 30, 40), (tail * 90, 110), (tail * 80 - 50 * tail, 40)], col, INK, lw=7)
        g.rc(0, 0, w, size * 1.9, col, INK, lw=7, r=40)
        g.text(txt, 0, 4, size, "#22181B", stroke=None)


def label(g, txt, x, y, size=70, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def studio(g, t, a="#1590A0", b="#0B3F4C"):
    """Explainer backdrop in brand colours with soft rays (diagram shots)."""
    g.fill_all(g.rgrad(W / 2, H * 0.45, W * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2400 * math.cos(a0), H * 0.45 + 2400 * math.sin(a0)),
                (W / 2 + 2400 * math.cos(a0 + 0.1), H * 0.45 + 2400 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


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


# ------------------------------------------------------------------ sets
def room1696(g, t, light=1.0):
    """Candle-lit 1690s room: plank wall, shutter window with moon, table."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#2B1E2A", "#3E2A2E"))
    with g.layer(0.5):
        for i in range(14):
            g.rect(i * 150 - 40, 0, 146, FLOOR, "#4A3236", "#2A1C1E", lw=4)
        g.rect(1380, 140, 300, 300, "#0F2238", INK, lw=10, r=6)
        g.circle(1560, 230, 46, "#FFF4E0", None, a=0.9)
        g.line([(1530, 140), (1530, 440)], INK, 10); g.line([(1380, 290), (1680, 290)], INK, 10)
        for k in range(3):
            g.rect(160 + k * 70, 260, 50, 120, "#6E4A3A", INK, lw=5, r=4)      # books
        g.rect(130, 380, 280, 18, "#5B3B2E", INK, lw=5)
    g.rect(-100, FLOOR, W + 200, H, "#2A1C1E", None)
    g.glow(900, 560, 900 * light, "#FFB648", 0.18 * light)


def table(g, x=960, y=760, w=1300):
    g.rect(x - w / 2, y, w, 40, "#7A5236", INK, lw=8, r=6)
    g.rect(x - w / 2 + 40, y + 40, 40, 300, "#5B3B2E", INK, lw=7)
    g.rect(x + w / 2 - 80, y + 40, 40, 300, "#5B3B2E", INK, lw=7)


def mint_office(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2F3E46", "#22303A"))
    with g.layer(0.5):
        for i in range(5):
            g.rect(120 + i * 360, 90, 300, 520, "#3A4E58", "#1E2A30", lw=6, r=150)        # arches
            g.rect(160 + i * 360, 150, 220, 420, "#1B2A33", None, r=110, a=0.6)
        g.text("ROYAL MINT · 1696", W / 2, 70, 44, "#C9A23A", stroke=None)
    g.rect(-100, FLOOR, W + 200, H, "#1E2A30", None)


def street(g, t):
    """Present-day street, kerb, buildings, low camera."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#9FD8EE", "#D6F0F7"))
    with g.layer(0.4):
        for i, (bx, bh, col) in enumerate(((60, 520, "#E07A5F"), (420, 640, "#3D5A80"), (760, 460, "#F2CC8F"), (1100, 700, "#81B29A"), (1480, 560, "#E07A5F"))):
            g.rect(bx, 640 - bh, 340, bh + 100, col, INK, lw=8)
            for r_ in range(int(bh / 120)):
                for cc in range(2):
                    g.rect(bx + 50 + cc * 140, 640 - bh + 40 + r_ * 120, 90, 70, "#DFF4F6", INK, lw=5)
    g.rect(-100, 680, W + 200, 60, "#B8BEC6", INK, lw=8)                  # pavement
    g.rect(-100, 740, W + 200, H, "#4A505A", None)                         # road
    for i in range(6):
        g.rect(i * 380 - ((t * 0) % 380), 980, 200, 22, "#F4F1EA", None, a=0.8)


def road1920(g, t):
    """1920s country road: hills, telegraph poles, dusty road."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F6C98B", "#F7E3B5"))
    with g.layer(0.3):
        g.path("M-100 640 Q400 420 900 600 Q1400 460 2100 620 L2100 760 L-100 760 Z", "#9DBF7A", INK, lw=8)
        for i in range(6):
            x = 140 + i * 360
            g.line([(x, 640), (x, 300)], "#6E4A3A", 12)
            g.line([(x - 60, 330), (x + 60, 330)], "#6E4A3A", 10)
        g.path("M80 320 Q260 360 440 320 Q620 360 800 320 Q980 360 1160 320 Q1340 360 1520 320 Q1700 360 1880 320", None, INK, lw=3)
    g.rect(-100, 720, W + 200, H, "#C9A27A", None)
    g.path("M700 1080 L900 720 L1020 720 L1220 1080 Z", "#B08A62", None)


def factory1860(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#5A4A5E", "#3E3346"))
    with g.layer(0.5):
        for i in range(4):
            g.rect(140 + i * 460, 120, 300, 380, "#E6D3B3", INK, lw=10, r=6)
            for j in range(3):
                g.line([(140 + i * 460 + j * 100 + 100, 120), (140 + i * 460 + j * 100 + 100, 500)], INK, 6)
            g.line([(140 + i * 460, 310), (440 + i * 460, 310)], INK, 6)
        for i in range(8):                                    # belt-driven shafts
            g.line([(i * 260, 40), (i * 260 + 60, 640)], "#2A1C1E", 6, a=0.6)
    g.rect(-100, FLOOR, W + 200, H, "#2E2430", None)


def court(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#6E4A3A", "#4A3026"))
    with g.layer(0.5):
        for i in range(9):
            g.rect(i * 230 - 40, 60, 200, 600, "#7A5642", "#3A2418", lw=5, r=10)
        g.rect(640, 120, 640, 90, "#C9A23A", INK, lw=8, r=10)
        g.text("PATENT COURT · 1871", 960, 168, 46, INK, stroke=None)
    g.rect(-100, 760, W + 200, H, "#3A2418", None)


def workshop1892(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3E5A6E", "#2A3E4E"))
    with g.layer(0.5):
        g.rect(80, 120, 520, 360, "#F6E7C8", INK, lw=10, r=8)
        g.text("BALTIMORE", 340, 230, 64, "#8E2430", stroke=None)
        g.text("1892", 340, 330, 90, INK, stroke=None)
        for i in range(10):
            g.rect(760 + i * 110, 300, 80, 200, "#5FA67A", INK, lw=5, r=20, a=0.8)       # bottle shelf
        g.rect(720, 500, 1160, 26, "#7A5236", INK, lw=6)
    g.rect(-100, FLOOR, W + 200, H, "#22303A", None)


def kitchen(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE6C7", "#FFD39A"))
    with g.layer(0.5):
        for i in range(-1, 14):
            for j in range(5):
                g.rect(i * 150 + (75 if j % 2 else 0), j * 110, 146, 106, "#FFF1DD", None, r=8, a=0.7)
        g.rect(1320, 120, 420, 320, "#9FD8EE", INK, lw=10, r=10)
        g.line([(1530, 120), (1530, 440)], INK, 8)
    g.rect(-100, 760, W + 200, 60, "#E07A5F", INK, lw=8)
    g.rect(-100, 820, W + 200, H, "#F2CC8F", INK, lw=8)


def bakery(g, t, glow=1.0):
    g.fill_all(g.lgrad(0, 0, 0, H, "#6E3B2E", "#4A2620"))
    with g.layer(0.5):
        g.path("M1100 760 L1100 300 Q1100 120 1440 120 Q1780 120 1780 300 L1780 760 Z", "#B85A3E", INK, lw=10)       # brick oven
        for j in range(6):
            for i in range(5):
                g.rect(1110 + i * 136 + (68 if j % 2 else 0), 300 + j * 76, 120, 66, "#A24E36", "#6E3426", lw=3)
        g.path("M1260 760 L1260 520 Q1260 400 1440 400 Q1620 400 1620 520 L1620 760 Z", "#2A1410", INK, lw=10)
        g.glow(1440, 620, 380 * glow, "#FF8A3D", 0.45 * glow)
    g.rect(-100, 760, W + 200, H, "#3A1E18", None)


def pocket_bg(g, t):
    g.fill_all(g.rgrad(W / 2, H / 2, W * 0.7, "#3E5A7A", "#2A3E56", "#1A2638"))


# ------------------------------------------------------------------ cold open (ch 0)
def coin_pile(g, x, y, n, t, clipped=0):
    for i in range(n):
        coin(g, x + (i % 4) * 54 - 80, y - (i // 4) * 16, 46, "silver", ridges=False, clip=0.8 if i < clipped else 0.0, face=None, sx=1.0)


def slivers(g, x, y, n):
    for i in range(n):
        a = i * 1.7
        with g.at(x + 60 * math.cos(a) * (i % 3 + 1) * 0.5, y + 14 * math.sin(a) + i * 2, a):
            g.path("M-26 -6 Q0 -14 26 -6 L22 2 Q0 -4 -22 2 Z", SILVER, INK, lw=4)


def s_open(g, c):
    """Frame 1: the clipper snipping a silver coin by candlelight, big and close."""
    room1696(g, c.gt)
    char2(g, "clipper", 720, 1480, 1250, "suspicious" if c.t < c.w("snips") else "smug", "reach_r", "reach_r", t=c.gt)
    table(g, 960, 820, 1500)
    candle(g, 1420, 820, 1.25, c.gt)
    coin_pile(g, 560, 800, 8, c.gt)
    k = seg(c.t, c.w("snips") - 0.1, 0.5)
    coin(g, 1050, 640, 120, "silver", ridges=False, clip=ease_out(k), face="head", glint=1.0)
    scissors(g, 1110 + 30 * ease_out(k), 640, 1.15, 1 - ease_out(k), rot=math.pi)
    if k > 0:
        with g.at(1180 + 90 * ease_out(k), 640 + 160 * ease_in(k), 2 * k):
            g.path("M-8 -50 Q6 0 -8 50 L4 50 Q16 0 4 -50 Z", SILVER, INK, lw=4)
    if c.t < 2.2:
        with g.screen():
            g.text("LONDON · 1696", W / 2, 120, 92, PAL["cream"], sw=18, depth=8, sc=pop(c.t, 0.0, 0.3))


def s_snipclose(g, c):
    room1696(g, c.gt, 0.8)
    table(g, 960, 820, 2200)
    n = 1 + int(c.u * 2.99)
    for i in range(3):
        k = clamp(c.u * 3 - i)
        if i < n:
            coin(g, 520 + i * 440, 600, 150, "silver", ridges=False, clip=ease_out(clamp(k * 1.6)), face="head")
    scissors(g, 520 + min(2, int(c.u * 3)) * 440 + 200, 600, 1.3, 0.5 + 0.5 * math.sin(c.gt * 14), rot=math.pi)
    slivers(g, 960, 880, 3 + int(c.u * 9))
    candle(g, 1780, 820, 1.0, c.gt)


def s_melt(g, c):
    room1696(g, c.gt)
    table(g, 960, 820, 1500)
    candle(g, 900, 820, 1.4, c.gt)
    k = ease_io(seg(c.t, 0.3, max(0.5, c.T - 1.0)))
    with g.at(900, 470, 0):                                          # ladle over the flame
        g.line([(-60, 0), (-460, -120)], "#5A5A6A", 18)
        g.path("M-80 -20 Q0 90 80 -20 Z", "#5A5A6A", INK, lw=7)
        g.ellipse(0, -14, 70 * (0.6 + 0.4 * k), 16, mix(SILVER, "#FFE08A", k), INK, lw=4)
    slivers(g, 1250, 800, int(12 * (1 - k)))
    if k > 0.8:
        g.ellipse(1250, 790, 70, 30, SILVER, INK, lw=6)
    char2(g, "clipper", 320, 1320, 1000, "smug", "hold", "down", t=c.gt)


def s_spend(g, c):
    room1696(g, c.gt)
    g.rect(1000, 600, 1100, 50, "#8A6A44", INK, lw=8)                # shop counter
    g.rect(1000, 650, 1100, 400, "#6E5034", INK, lw=8)
    char2(g, "clipper", 600, 1420, 1050, "smug", "down", "reach_r", t=c.gt)
    char2(g, "worker", 1500, 1420, 1050, "deadpan" if c.u < 0.6 else "bored", "down", "reach_l", t=c.gt, prop=False, flip=True)
    k = ease_io(seg(c.t, 0.2, 1.0))
    coin(g, lerp(880, 1170, k), 560, 50, "silver", ridges=False, clip=0.8, face=None)


def s_england(g, c):
    studio(g, c.gt, "#2F5F6A", "#10263B")
    path = ("M820 120 Q900 90 960 150 Q1040 140 1020 230 Q1100 300 1060 380 Q1140 470 1100 560 Q1180 640 1140 760 Q1220 860 1080 900 "
            "Q920 960 780 900 Q700 940 640 880 Q720 800 700 720 Q640 640 700 560 Q640 480 720 420 Q660 340 740 280 Q700 200 820 120 Z")
    g.path(path, "#9DBF7A", INK, lw=10)
    pts = [(860, 820), (940, 760), (800, 700), (1000, 640), (880, 560), (760, 500), (980, 450), (900, 380), (840, 300), (1040, 820), (720, 800), (1060, 720)]
    for i, (x, y) in enumerate(pts):
        k = pop(c.t, 0.25 + i * 0.22, 0.3)
        if k > 0:
            with g.at(x, y, 0, k):
                g.circle(0, 0, 26, PAL["coral"], INK, lw=6)
                g.text("✂", 0, 4, 30, INK, stroke=None, font="DejaVu Sans")
    label(g, "CLIPPING EVERYWHERE", W / 2, 120, 72, k=pop(c.t, 0.2, 0.3))


def s_newton(g, c):
    mint_office(g, c.gt)
    table(g, 1100, 780, 1100)
    candle(g, 1500, 780, 1.0, c.gt)
    g.rect(820, 700, 260, 80, "#F3E2BC", INK, lw=6, r=4)              # ledger
    k = ease_out(seg(c.t, 0, 0.6))
    char2(g, "newton", 900, 1420 + 200 * (1 - k), 1150, "suspicious", "down", "hold", t=c.gt)
    label(g, "ISAAC NEWTON", 1400, 300, 84, k=pop(c.t, c.w("Isaac") - 0.1, 0.35))


def s_pocket(g, c):
    pocket_bg(g, c.gt)
    k = ease_out(seg(c.t, 0, 0.6))
    with g.at(960, 1250 - 650 * k):                                   # palm with a modern coin
        g.ellipse(0, 0, 420, 260, CAST_SKIN, INK, lw=10)
        for i in range(4):
            g.rc(-240 + i * 150, -260, 110, 300, CAST_SKIN, INK, lw=10, r=55)
        g.ellipse(0, 0, 400, 240, CAST_SKIN, None)
    coin(g, 960, 600 - 650 * (1 - k) + 0 * k, 170, "silver", ridges=True, face="value", glint=1.0)
    g.glow(960, 600, 320, "#FFFFFF", 0.25 * ease_out(seg(c.t, 0.6, 0.6)))


CAST_SKIN = "#D8A580"


def s_montage(g, c):
    studio(g, c.gt)
    items = [("stop", 300), ("manhole", 660), ("cap", 1000), ("cracker", 1340), ("bag", 1650)]
    words = ["stop", "manholes", "bottle", "crackers", "crackers"]
    for i, (nm, x) in enumerate(items):
        t0 = c.w(words[i]) - 0.15 if i < 4 else c.w("crackers") + 0.15
        k = back_out(seg(c.t, t0, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, 520, 0.08 * math.sin(c.gt * 2 + i), k):
            if nm == "stop": road_sign(g, 0, 0, 130, "octagon")
            elif nm == "manhole": manhole(g, 0, 0, 140, tilt=1.0, hole=False)
            elif nm == "cap": bottle_cap(g, 0, 0, 130)
            elif nm == "cracker": cracker(g, 0, 0, 0.75)
            else: paper_bag(g, 0, 160, 0.95)


def s_problems(g, c):
    """Problem -> fix: a sad grey blob of 'problem' becomes a shape."""
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    k = ease_io(seg(c.t, c.w("fix") - 0.3, 0.8))
    for i, sh in enumerate(("circle", "octagon", "diamond", "square")):
        x = 360 + i * 400
        with g.at(x, 520, 0, 1.0):
            if k < 0.5:
                g.text("?", 0, 30, 220 * (1 - k), PAL["cream"], sw=24)
            else:
                road_sign(g, 0, 0, 120 * ease_out((k - 0.5) * 2), sh, ["#3E7CB1", "#D7263D", "#FFC93C", "#5ED3B5"][i], "", border="#FFF4E0")
    label(g, "PROBLEM → FIX", W / 2, 140, 84, k=pop(c.t, 0.1, 0.3))


# ------------------------------------------------------------------ coins (ch 1)
def s_coin_q(g, c):
    kitchen(g, c.gt)
    char2(g, "modern", 520, 1480, 1150, "curious", "down", "reach_r", t=c.gt, prop=False)
    u = (c.t * 1.6) % 1.0
    coin(g, 980, 300 + 250 * (2 * u - 1) ** 2, 70, "silver", ridges=True, face="value", sx=abs(math.cos(c.t * 9)) * 0.9 + 0.1)
    qmark(g, 1450, 360, 220, PAL["yellow"], 0.15, pop(c.t, c.w("ridges") - 0.2, 0.3))
    banner(g, c, "COIN RIDGES")


def s_edge_macro(g, c):
    pocket_bg(g, c.gt)
    coin_edge(g, 960, 520, 1500, 300, "silver", ridges=True)
    label(g, "WHY RIDGES?", W / 2, 160, 90, k=pop(c.t, 0.05, 0.3))


def s_hammer(g, c):
    mint_office(g, c.gt)
    table(g, 960, 760, 900)
    char2(g, "worker", 640, 1400, 1050, "bored", "up" if (c.gt * 2.2) % 1 < 0.5 else "hold", "down", t=c.gt, prop=False)
    hk = abs(math.sin(c.gt * math.pi * 2.2))
    g.rc(880, 700, 120, 120, "#5A5A6A", INK, lw=7, r=8)               # anvil die
    with g.at(900, 470 + 160 * (1 - hk), -0.4 * hk):
        g.rc(0, 0, 40, 260, "#7A5236", INK, lw=6, r=8); g.rc(0, -130, 150, 70, "#5A5A6A", INK, lw=7, r=10)
    for i in range(5):                                               # wobbly hand-struck coins
        x = 1180 + i * 120
        g.poly([(x + 44 * math.cos(a) * (1 + 0.12 * math.sin(a * 3 + i)), 730 + 40 * math.sin(a) * (1 + 0.1 * math.cos(a * 2 + i))) for a in [j * TAU / 16 for j in range(16)]],
               SILVER, INK, lw=5)
    label(g, "HAMMERED BY HAND", W / 2, 140, 72, k=pop(c.t, 0.2, 0.3))


def s_wobbly(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    k = ease_io(seg(c.t, 0.4, 1.2))
    for i in range(3):
        x = 520 + i * 440
        bite = (i == 1) * k
        pts = []
        for j in range(40):
            a = j * TAU / 40
            rr = 170 * (1 + 0.07 * math.sin(a * 3 + i * 2) + 0.05 * math.cos(a * 5))
            if bite and -0.6 < a - 0 < 0.6 or (bite and a > TAU - 0.6):
                rr *= 1 - 0.14 * bite
            pts.append((x + rr * math.cos(a), 520 + rr * math.sin(a)))
        g.poly(pts, SILVER, INK, lw=8)
    qmark(g, 1590, 300, 150, PAL["yellow"], 0.1, pop(c.t, c.w("nobody") - 0.1, 0.3))


def s_treason(g, c):
    mint_office(g, c.gt)
    char2(g, "guard", 540, 1430, 1150, "angry", "down", "hold", t=c.gt)
    k = back_out(seg(c.t, c.w("treason") - 0.2, 0.35), 1.8)
    with g.at(1250, 520, -0.05, max(0.01, k)):
        g.rc(0, 0, 620, 420, "#F3E2BC", INK, lw=9, r=10)
        g.text("CLIPPING", 0, -110, 80, INK, stroke=None)
        g.text("= HIGH TREASON", 0, -10, 70, "#8E2430", stroke=None)
        if c.t > c.w("hanged") - 0.2:
            with g.at(0, 110, -0.12, back_out(seg(c.t, c.w("hanged") - 0.2, 0.3), 2.2)):
                g.rc(0, 0, 420, 100, None, "#D7263D", lw=12, r=12)
                g.text("DEATH", 0, 6, 74, "#D7263D", stroke=None)


def s_press(g, c):
    mint_office(g, c.gt)
    k = abs(math.sin(c.gt * 2.4))
    with g.at(960, 0):                                               # screw press
        g.rc(0, 520, 520, 60, "#5A5A6A", INK, lw=8, r=8)
        g.rc(-220, 330, 60, 380, "#4A4F5A", INK, lw=8); g.rc(220, 330, 60, 380, "#4A4F5A", INK, lw=8)
        g.rc(0, 160, 520, 70, "#4A4F5A", INK, lw=8, r=10)
        g.rc(0, 300 + 100 * k, 70, 200, "#9AA3AD", INK, lw=7)
        g.line([(-360 * math.cos(c.gt * 2.4), 170), (360 * math.cos(c.gt * 2.4), 170)], "#7A5236", 22)
        g.circle(-360 * math.cos(c.gt * 2.4), 170, 34, "#5A5A6A", INK, lw=6); g.circle(360 * math.cos(c.gt * 2.4), 170, 34, "#5A5A6A", INK, lw=6)
    char2(g, "worker", 420, 1380, 1000, "deadpan", "reach_r", "reach_r", t=c.gt, prop=False)
    for i in range(min(6, int(c.t * 1.5))):
        coin(g, 1300 + (i % 3) * 140, 840 - (i // 3) * 40, 60, "silver", ridges=True, face="head")
    label(g, "1696 · MADE BY MACHINE", W / 2, 120, 72, k=pop(c.t, 0.1, 0.3))


def s_trim_test(g, c):
    pocket_bg(g, c.gt)
    k = ease_io(seg(c.t, 0.2, 1.0))
    coin_edge(g, 960, 480, 1500, 300, "silver", ridges=True, gap=k, gap_glow=ease_out(seg(c.t, c.w("Anyone") - 0.2, 0.4)))
    char2(g, "worker", 1680, 1500, 900, "shocked" if c.u > 0.5 else "suspicious", "down", "point", t=c.gt, prop=False, flip=True)


def s_newton_desk(g, c):
    mint_office(g, c.gt)
    table(g, 1000, 780, 1200)
    with g.at(1320, 380, -0.03):                                      # evidence board with string
        g.rc(0, 0, 640, 460, "#B98A5A", INK, lw=9, r=8)
        for (x, y) in ((-200, -120), (180, -140), (-160, 120), (200, 110)):
            g.rc(x, y, 160, 110, "#FFF4E0", INK, lw=5, r=4)
        g.line([(-200, -120), (180, -140), (200, 110), (-160, 120), (-200, -120)], "#D7263D", 5)
        g.rc(0, 0, 200, 150, "#FFF4E0", INK, lw=6, r=4)
        g.text("WANTED", 0, 4, 44, "#8E2430", stroke=None)
    char2(g, "newton", 640, 1420, 1100, "suspicious" if c.u < 0.6 else "smug", "down", "point", t=c.gt)
    candle(g, 1000, 780, 0.9, c.gt)


def s_chaloner(g, c):
    room1696(g, c.gt)
    char2(g, "chaloner", 960, 1500, 1250, "smug", "hip", "hip", t=c.gt)
    for i in range(6):
        coin(g, 600 + i * 150, 880 + 20 * math.sin(i), 48, "gold" if i % 2 else "silver", ridges=False, face=None)
    label(g, "WILLIAM CHALONER", W / 2, 120, 80, k=pop(c.t, 0.2, 0.3))
    label(g, "FORGER", 1520, 380, 64, "#FF6B5B", k=pop(c.t, c.w("forgers") - 0.2 if True else 0.5, 0.3), rot=0.08)


def s_candle_out(g, c):
    k = ease_io(seg(c.t, c.w("hanged") - 0.1, 0.8))
    mint_office(g, c.gt)
    table(g, 960, 780, 1100)
    g.rect(760, 700, 260, 80, "#F3E2BC", INK, lw=6, r=4)
    candle(g, 1180, 780, 1.4, c.gt, lit=1 - k)
    if k > 0: steam(g, 1180, 450, c.gt, 3, 1.2, 0.5 * k, "#C9CED6")
    with g.screen():
        g.rect(0, 0, W, H, "#000000", None, a=0.4 * k)
    label(g, "1699", W / 2, 200, 120, PAL["cream"], k=pop(c.t, 0.1, 0.3))


def s_clad(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    k = ease_io(seg(c.t, 0.3, 1.0))
    coin_edge(g, 960, 420 + 60 * k, 1300, 300, "silver", ridges=True, layers=k > 0.4)
    if k > 0.4:
        with g.screen():
            g.text("COPPER", 960, 430 + 60 * k, 60, "#FFF4E0", sw=10)
            g.text("COPPER-NICKEL", 960, 330 + 60 * k, 44, INK, stroke=None)
    no_sign(g, 1640, 820, 120, pop(c.t, c.w("silver") - 0.1, 0.3))
    with g.screen():
        if c.t > c.w("silver") - 0.1:
            g.text("SILVER", 1640, 830, 50, PAL["cream"], sw=10, sc=pop(c.t, c.w("silver") - 0.1, 0.3))
    label(g, "TODAY", 300, 140, 90, k=pop(c.t, 0.05, 0.3))


def s_blind(g, c):
    pocket_bg(g, c.gt)
    char2(g, "modern", 420, 1450, 1150, "blink" if c.t > c.w("eyes") - 0.2 else "curious", "down", "reach_r", t=c.gt, prop=False, blink=False)
    coin(g, 1050, 520, 150, "silver", ridges=True, face="value")
    coin(g, 1500, 520, 160, "copper", ridges=False, face="value")
    k = ease_io(seg(c.t, c.w("ridges", 0) - 0.4, 0.8)) if c.t > 0 else 0
    with g.screen():
        g.text("DIME", 1050, 760, 60, PAL["cream"], sw=10, sc=pop(c.t, c.w("dime") - 0.1, 0.3))
        g.text("PENNY", 1500, 760, 60, PAL["cream"], sw=10, sc=pop(c.t, c.w("penny") - 0.1, 0.3))
    if c.t > c.w("ridges") - 0.3:
        g.circle(1050, 520, 175, None, PAL["yellow"], lw=14, a=0.6 + 0.4 * math.sin(c.gt * 8))
        check(g, 1190, 360, 50, seg(c.t, c.w("which") - 0.2, 0.3))


# ------------------------------------------------------------------ manholes (ch 2)
def s_street_q(g, c):
    street(g, c.gt)
    char2(g, "modern", 520, 1150, 760, "curious", "down", "point", t=c.gt, prop=False)
    manhole(g, 1150, 900, 230, tilt=0.36)
    qmark(g, 1150, 600, 170, PAL["yellow"], 0.1, pop(c.t, c.w("round") - 0.2, 0.3))
    banner(g, c, "MANHOLE COVERS")


def s_square_fall(g, c, shape="square"):
    studio(g, c.gt, "#4A505A", "#22262E")
    r = 260
    k_turn = ease_io(seg(c.t, c.w("side") - 0.4, 0.9)) if shape == "square" else 0
    k_fall = ease_in(seg(c.t, c.w("through") - 0.2, 0.7)) if shape == "square" else 0
    g.poly([(960 + px, 600 + py) for px, py in ngon_pts(4, r * 1.25, math.pi / 4)], "#8A8F98", INK, lw=10)
    g.poly([(960 + px, 600 + py) for px, py in ngon_pts(4, r * 1.12, math.pi / 4)], "#141820", INK, lw=6)
    # the lid seen from the top: it turns 45 degrees, then its side view (thin bar) slides along the diagonal
    with g.at(960, 600 + 900 * k_fall, (math.pi / 4) * k_turn, 1.0, 1.0 - 0.85 * k_turn):
        g.poly(ngon_pts(4, r * 1.12, math.pi / 4), IRON, INK, lw=10)
    if k_turn > 0.5:
        g.line([(960 - r * 1.12 * 1.414 / 1.414 * 1.0, 600 - r * 1.12), (960 + r * 1.12, 600 + r * 1.12)], PAL["yellow"], 8, dash=([20, 16], 0), a=k_turn)
        label(g, "DIAGONAL > SIDE", W / 2, 140, 72, k=pop(c.t, c.w("diagonal") - 0.2, 0.3))


def s_clang(g, c):
    """Side cut-away: the square lid falls down the shaft towards a worker."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#3A3F48", "#151820"))
    g.rect(-100, 0, W + 200, 200, "#4A505A", INK, lw=8)
    g.rect(760, 0, 400, H, "#0E1116", None)
    g.rect(700, 0, 60, H, "#6E6650", INK, lw=6); g.rect(1160, 0, 60, H, "#6E6650", INK, lw=6)
    for i in range(10):
        g.line([(800, 60 + i * 110), (1120, 60 + i * 110)], "#9AA3AD", 8, a=0.4)
    k = ease_in(seg(c.t, 0.0, 0.8))
    with g.at(960, 120 + 640 * k, 0.3 + 2.4 * k):
        g.rc(0, 0, 380, 50, IRON, INK, lw=8, r=6)
    char2(g, "sewer", 960, 1500, 640, "shocked" if c.t > 0.4 else "deadpan", "up", "up", t=c.gt)
    if c.t > c.w("Clang") - 0.05:
        burst(g, 960, 760, 120, 260, 12, PAL["yellow"], 14, k=seg(c.t, c.w("Clang"), 0.3))
        label(g, "CLANG!", 1450, 400, 120, k=pop(c.t, c.w("Clang") - 0.05, 0.25), rot=0.1)


def s_width(g, c):
    studio(g, c.gt, "#1590A0", "#0B3F4C")
    rot = c.gt * 1.4
    g.circle(960, 560, 300, IRON, INK, lw=10)
    g.circle(960, 560, 230, None, "#5E6470", lw=8)
    for sd in (-1, 1):                                                # calipers stay the same width while it turns
        g.line([(960 + sd * 300, 160), (960 + sd * 300, 960)], PAL["yellow"], 10)
    with g.at(960, 560, rot):
        g.line([(-300, 0), (300, 0)], PAL["cream"], 8, dash=([18, 14], 0))
    label(g, "SAME WIDTH EVERY WAY", W / 2, 110, 70, k=pop(c.t, c.w("same") - 0.2, 0.3))
    check(g, 1530, 300, 70, seg(c.t, c.w("never") - 0.2, 0.3))


def s_roll(g, c):
    street(g, c.gt)
    x = 500 + 700 * ease_io(seg(c.t, 0.2, c.T * 0.6))
    char2(g, "sewer", x - 260, 1250, 820, "smug", "reach_r", "reach_r", t=c.gt)
    with g.at(x, 760, (x - 500) / 230):
        g.circle(0, 0, 230, IRON, INK, lw=10)
        for i in range(-3, 4):
            g.line([(-170, i * 40), (170, i * 40)], "#5E6470", 7)
        g.circle(0, 0, 180, None, "#5E6470", lw=8)


def s_reuleaux(g, c):
    studio(g, c.gt, "#7A4FB0", "#2A1840")
    rot = c.gt * 1.2
    w = 260 * math.sqrt(3)
    g.line([(300, 560 - w / 2), (1620, 560 - w / 2)], PAL["yellow"], 10)
    g.line([(300, 560 + w / 2), (1620, 560 + w / 2)], PAL["yellow"], 10)
    # rolling between two parallel lines: centre wobbles; place it so it touches both lines
    P = reuleaux_pts(260, rot)
    ys = [p[1] for p in P]
    cy = 560 - (max(ys) + min(ys)) / 2
    cx = 400 + (c.gt * 160) % 1100
    g.poly([(cx + px, cy + py) for px, py in P], "#FFC93C", INK, lw=10)
    label(g, "REULEAUX TRIANGLE", W / 2, 110, 76, PAL["cream"], k=pop(c.t, c.w("Reuleaux") - 0.2, 0.3))


def s_engineer_shrug(g, c):
    street(g, c.gt)
    char2(g, "sewer", 760, 1380, 1050, "bored", "hip", "hip", t=c.gt)
    manhole(g, 1360, 960, 220, tilt=0.36)
    with g.at(1360, 700, 0, 1 + 0.03 * math.sin(c.gt * 3)):
        g.poly([(px, py) for px, py in reuleaux_pts(120, 0.2)], "#FFC93C", INK, lw=8, a=0.5)
    cross(g, 1490, 600, 44, seg(c.t, c.w("easier") - 0.3, 0.3))


# ------------------------------------------------------------------ stop signs (ch 3)
def s_stop_q(g, c):
    street(g, c.gt)
    road_sign(g, 1260, 380, 210, "octagon", post=520)
    char2(g, "modern", 600, 1200, 820, "suspicious", "down", "point", t=c.gt, prop=False)
    with g.screen():
        for i, (px, py) in enumerate(ngon_pts(8, 250, math.pi / 8)):
            k = pop(c.t, c.w("eight") + i * 0.07 - 0.2, 0.2)
            if k > 0: g.text(str(i + 1), 1260 + px * 1.0, 380 + py * 1.0, 50, PAL["yellow"], sw=10, sc=k)
    banner(g, c, "STOP SIGNS")


def s_1923(g, c):
    road1920(g, c.gt)
    table(g, 960, 760, 1000)
    char2(g, "engineer", 520, 1400, 1000, "deadpan", "down", "point", t=c.gt)
    char2(g, "prof", 1420, 1400, 1000, "curious", "down", "down", t=c.gt, flip=True)
    for i, sh in enumerate(("circle", "octagon", "diamond", "square")):
        k = pop(c.t, c.w("sides") - 0.3 + i * 0.25, 0.3)
        if k > 0:
            with g.at(760 + i * 140, 690, 0, k):
                road_sign(g, 0, 0, 56, sh, "#FFF4E0", "", border="#FFF4E0")
    label(g, "1923", 960, 150, 120, k=pop(c.t, 0.1, 0.3))
    label(g, "MORE SIDES = MORE DANGER", W / 2, 270, 64, PAL["cream"], k=pop(c.t, c.w("dangerous") - 0.3, 0.3))


def s_railway(g, c):
    road1920(g, c.gt)
    g.rect(-100, 820, W + 200, 40, "#6E4A3A", INK, lw=6)              # rails across the road
    for i in range(16):
        g.rect(i * 130, 800, 40, 90, "#5B3B2E", INK, lw=4)
    road_sign(g, 420, 420, 150, "circle", "#FFF4E0", "RR", INK, post=420)
    x = 2200 - ((c.t * 900) % 3400)
    with g.at(x, 680):                                                # steam train silhouette
        g.rc(0, 0, 520, 200, "#22181B", INK, lw=8, r=20); g.rc(-180, -150, 120, 120, "#22181B", INK, lw=8)
        for i in range(4): g.circle(-180 + i * 120, 110, 50, "#3A3046", INK, lw=8)
        steam(g, -180, -220, c.gt, 4, 1.5, 0.7)
    label(g, "DEADLIEST", 1300, 200, 90, "#FF6B5B", k=pop(c.t, c.w("deadliest") - 0.2, 0.3))


def s_shapes_row(g, c):
    studio(g, c.gt, "#2F5F6A", "#10263B")
    rows = [("octagon", "STOP", "stop", "#F2C14E"), ("diamond", "", "caution", "#F2C14E"), ("square", "", "care", "#F4F1EA"), ("rect", "", "information", "#F4F1EA")]
    for i, (sh, txt, wd, col) in enumerate(rows):
        k = back_out(seg(c.t, c.w(wd) - 0.25, 0.35), 1.7)
        if k <= 0: continue
        x = 330 + i * 420
        with g.at(x, 520, 0, k):
            road_sign(g, 0, 0, 140, sh, col, txt, INK, border=INK if col != "#F4F1EA" else "#F4F1EA")
        with g.screen():
            g.text(wd.upper(), x, 760, 54, PAL["cream"], sw=10, sc=k)


def s_twist(g, c):
    road1920(g, c.gt)
    road_sign(g, 1180, 400, 200, "octagon", "#D7263D", "STOP", post=460)
    char2(g, "engineer", 560, 1400, 1100, "suspicious", "down", "point", t=c.gt)
    label(g, "TWIST", 1180, 120, 96, k=pop(c.t, c.w("twist") - 0.2, 0.3))
    cross(g, 1360, 260, 60, seg(c.t, c.w("red") - 0.2, 0.3))


def s_yellow(g, c):
    road1920(g, c.gt)
    k = back_out(seg(c.t, 0.0, 0.4), 1.6)
    road_sign(g, 1000, 420, 240 * k + 1, "octagon", "#F2C14E", "STOP", INK, post=500, border=INK)
    char2(g, "engineer", 420, 1400, 1100, "smug", "down", "point", t=c.gt)
    label(g, "1924–1954", 1500, 200, 80, k=pop(c.t, 0.3, 0.3))


def s_fade(g, c):
    road1920(g, c.gt)
    g.glow(1700, 80, 400, "#FFF4C2", 0.6)
    g.circle(1700, 80, 110, "#FFE58A", INK, lw=8)
    fd = ease_io(seg(c.t, c.w("faded") - 0.3, 1.6))
    road_sign(g, 900, 420, 240, "octagon", "#D7263D", "STOP", post=500, fade=fd)
    with g.at(1450, 760):                                            # 1920s car going past without stopping
        x = -1700 + 3400 * seg(c.t, c.w("miss") - 0.6, 2.2)
        g.rc(x, 0, 380, 120, "#22181B", INK, lw=8, r=30); g.rc(x - 20, -90, 200, 90, "#22181B", INK, lw=8, r=20)
        g.circle(x - 110, 70, 46, "#3A3046", INK, lw=8); g.circle(x + 110, 70, 46, "#3A3046", INK, lw=8)
    label(g, "FADED!", 900, 120, 90, "#FF6B5B", k=pop(c.t, c.w("faded") + 0.4, 0.3))


def s_1954(g, c):
    street(g, c.gt)
    road_sign(g, 960, 400, 250, "octagon", "#D7263D", "STOP", post=520)
    g.glow(960, 400, 420, "#FFFFFF", 0.3 * ease_out(seg(c.t, c.w("red") - 0.2, 0.5)))
    sparkles(g, c.gt, [(760, 220), (1180, 260), (1200, 560)], r=30 * ease_out(seg(c.t, c.w("red") - 0.2, 0.4)))
    label(g, "1954", 960, 80, 110, k=pop(c.t, c.w("1954") - 0.1, 0.3))


# ------------------------------------------------------------------ paper bags (ch 4)
def s_bag_q(g, c):
    kitchen(g, c.gt)
    paper_bag(g, 1200, 800, 1.6, "flat")
    char2(g, "modern", 560, 1350, 1000, "curious", "down", "point", t=c.gt, prop=False)
    qmark(g, 1500, 260, 170, PAL["yellow"], 0.1, pop(c.t, c.w("bottom") - 0.2, 0.3))
    banner(g, c, "PAPER BAGS")


def s_envelope(g, c):
    factory1860(g, c.gt)
    g.rect(400, 700, 1200, 40, "#7A5236", INK, lw=8)
    tip = ease_in(seg(c.t, c.w("fell") - 0.5, 0.5)) * 1.35
    paper_bag(g, 1000, 700, 1.5, "envelope", tip=tip)
    for i in range(3):
        k = seg(c.t, c.w("fell") - 0.2, 0.6)
        if k > 0:
            with g.at(1100 + i * 90 + 200 * k, 660 + 260 * ease_in(k), 3 * k):
                g.circle(0, 0, 34, ["#FF6B5B", "#FFC93C", "#5ED3B5"][i], INK, lw=5)
    char2(g, "worker", 420, 1400, 1000, "bored", "hip", "down", t=c.gt, prop=False)
    label(g, "1860s", 1560, 140, 90, k=pop(c.t, 0.1, 0.3))


def s_knight_factory(g, c):
    factory1860(g, c.gt)
    char2(g, "knight", 760, 1420, 1100, "curious", "down", "hold", t=c.gt)
    for i in range(4):
        paper_bag(g, 1200 + i * 150, 900 - (i % 2) * 20, 0.8, "envelope", tip=0.05 * math.sin(c.gt + i))
    label(g, "MARGARET KNIGHT", W / 2, 120, 84, k=pop(c.t, c.w("Margaret") - 0.1, 0.3))
    label(g, "MASSACHUSETTS", W / 2, 230, 54, PAL["cream"], k=pop(c.t, c.w("Massachusetts") - 0.2, 0.3))


def s_model(g, c):
    factory1860(g, c.gt)
    table(g, 1100, 760, 1100)
    k = ease_io(seg(c.t, 0.3, max(0.4, c.T - 1.2)))
    with g.at(1100, 660):                                             # wooden model with rollers folding a bag
        g.rc(0, 0, 520, 160, "#B98A5A", INK, lw=8, r=10)
        for i in range(3):
            with g.at(-160 + i * 160, -40, c.gt * 3):
                g.circle(0, 0, 50, "#E6CF9E", INK, lw=6); g.line([(-40, 0), (40, 0)], INK, 6)
    paper_bag(g, 1500, 750, 0.9 * k + 0.01, "flat")
    char2(g, "knight", 540, 1420, 1100, "smug" if k > 0.8 else "curious", "reach_r", "reach_r", t=c.gt)


def s_annan(g, c):
    factory1860(g, c.gt)
    g.rect(980, 520, 640, 360, "#5A5A6A", INK, lw=10, r=10)            # iron machine
    for i in range(3):
        with g.at(1120 + i * 180, 640, c.gt * 2):
            g.circle(0, 0, 60, "#9AA3AD", INK, lw=7); g.line([(-50, 0), (50, 0)], INK, 7)
    peek = ease_out(seg(c.t, c.w("saw") - 0.4, 0.5))
    char2(g, "annan", 1880 - 300 * peek, 1450, 1100, "suspicious", "down", "down", t=c.gt, flip=True)
    if c.t > c.w("patented") - 0.2:
        with g.at(1250, 300, -0.06, back_out(seg(c.t, c.w("patented") - 0.2, 0.35), 2)):
            g.rc(0, 0, 420, 140, "#F3E2BC", INK, lw=8, r=8)
            g.text("PATENT", 0, -10, 64, INK, stroke=None); g.text("C. ANNAN", 0, 44, 36, "#8E2430", stroke=None)
    char2(g, "knight", 420, 1420, 1000, "deadpan" if c.t < c.w("patented") else "angry", "down", "hold", t=c.gt)


def s_court(g, c, who="annan"):
    court(g, c.gt)
    g.rect(760, 520, 400, 260, "#5B3B2E", INK, lw=8, r=8)             # judge bench
    char2(g, "prof", 960, 980, 620, "bored", "down", "down", t=c.gt)
    char2(g, "annan", 1450, 1420, 1100, "smug", "hip", "point", t=c.gt, flip=True)
    char2(g, "knight", 430, 1420, 1050, "suspicious", "down", "down", t=c.gt)
    if who == "annan":
        bubble(g, 1480, 260, "A WOMAN? IMPOSSIBLE.", seg(c.t, c.w("woman") - 0.2, 0.3), tail=1, size=50)


def s_evidence(g, c):
    court(g, c.gt)
    char2(g, "knight", 600, 1430, 1150, "smug", "hold", "reach_r", t=c.gt)
    for i, (wd, txt, col) in enumerate((("drawings", "DRAWINGS", "#FFF4E0"), ("notes", "NOTES", "#F3E2BC"), ("diary", "DIARY", "#8E2430"))):
        k = back_out(seg(c.t, c.w(wd) - 0.2, 0.35), 1.8)
        if k <= 0: continue
        with g.at(1050 + i * 260, 560 - i * 30, -0.1 + 0.1 * i, k):
            g.rc(0, 0, 220, 280, col, INK, lw=7, r=8)
            for j in range(5): g.line([(-80, -90 + j * 40), (80, -90 + j * 40)], "#9AA3AD" if col != "#8E2430" else "#E6CF9E", 5)
            g.text(txt, 0, 170, 42, PAL["cream"], sw=8)


def s_won(g, c):
    court(g, c.gt)
    char2(g, "knight", 760, 1430, 1150, "smug", "up", "up", t=c.gt)
    char2(g, "annan", 1500, 1430, 1000, "shocked", "down", "down", t=c.gt, flip=True)
    label(g, "1871: SHE WON", 960, 160, 100, k=pop(c.t, c.w("won") - 0.15, 0.3))
    if c.t > c.w("won"):
        sparkles(g, c.gt, [(600, 300), (920, 260), (700, 520)], r=30)
    if c.t > c.w("bag") - 0.3:
        paper_bag(g, 1150, 940, 0.9 * pop(c.t, c.w("bag") - 0.3, 0.3), "flat")


# ------------------------------------------------------------------ bottle caps (ch 5)
def s_cap_count(g, c):
    studio(g, c.gt, "#D7263D", "#5A1020")
    n = min(21, int(max(0, c.t - 0.6) * 9))
    bottle_cap(g, 960, 520, 330, 21, hi=n - 1)
    label(g, str(n) if n else "?", 1560, 520, 220, k=1.0)
    banner(g, c, "BOTTLE CAPS")


def s_cork(g, c):
    workshop1892(g, c.gt)
    table(g, 960, 780, 1100)
    bottle(g, 960, 780, 1.1, stopper="cork", fizz=1.0, t=c.gt, flat=ease_io(seg(c.t, c.w("flat") - 0.5, 1.0)))
    steam(g, 960, 230, c.gt, 3, 0.8, 0.5, "#DDF0F3")
    char2(g, "gent", 520, 1420, 1050, "bored" if c.t > c.w("flat") - 0.3 else "deadpan", "down", "down", t=c.gt)
    label(g, "1880s", 1500, 160, 90, k=pop(c.t, 0.1, 0.3))
    label(g, "FLAT", 1450, 420, 90, "#FF6B5B", k=pop(c.t, c.w("flat") - 0.1, 0.3), rot=0.1)


def s_painter(g, c):
    workshop1892(g, c.gt)
    table(g, 1100, 780, 900)
    char2(g, "painter", 560, 1420, 1100, "curious", "down", "reach_r", t=c.gt)
    k = ease_io(seg(c.t, c.w("crimped") - 0.4, 0.8))
    with g.at(1150, 560, 0, 1.0, 1.0 - 0.0 * k):
        bottle_cap(g, 0, 0, 160, 24)
    with g.at(1150, 560, 0):
        g.text("♛", 0, -230, 120, PAL["yellow"], sw=10, sc=pop(c.t, c.w("crown") - 0.2, 0.3), font="DejaVu Sans")
    label(g, "WILLIAM PAINTER", W / 2, 120, 80, k=pop(c.t, c.w("William") - 0.1, 0.3))


def s_24(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    bottle_cap(g, 760, 540, 300, 24, hi_all=1.0, col="#3E7CB1")
    label(g, "24", 1450, 540, 260, k=pop(c.t, c.w("twenty-four") - 0.2 if True else 0.3, 0.3))


def s_21(g, c):
    studio(g, c.gt, "#D7263D", "#5A1020")
    k = ease_io(seg(c.t, 0.2, 0.9))
    bottle_cap(g, 620, 540, 260, 24, col="#3E7CB1")
    arrow(g, 960, 540, 1180, 540, PAL["yellow"], w=26, k=k)
    bottle_cap(g, 1460, 540, 260, 21, hi_all=k, col="#D7263D")
    with g.screen():
        g.text("24", 620, 880, 90, PAL["cream"], sw=14)
        g.text("21", 1460, 880, 110, PAL["yellow"], sw=16, sc=pop(c.t, c.w("twenty-one") - 0.2, 0.3))
    check(g, 1720, 300, 60, seg(c.t, c.w("pop") - 0.2, 0.3))


def s_opener(g, c):
    workshop1892(g, c.gt)
    table(g, 960, 780, 900)
    bottle(g, 960, 780, 1.0, stopper="crown", fizz=1.0, t=c.gt)
    with g.at(1100, 290, -0.4 + 0.3 * math.sin(c.gt * 6)):          # opener
        g.rc(0, 0, 60, 260, "#9AA3AD", INK, lw=7, r=24); g.circle(0, -110, 40, None, INK, lw=8)
    char2(g, "painter", 520, 1420, 1050, "smug", "hip", "down", t=c.gt)


def s_advice(g, c):
    workshop1892(g, c.gt)
    char2(g, "painter", 560, 1430, 1100, "smug", "down", "point", t=c.gt)
    char2(g, "gillette", 1380, 1430, 1100, "curious", "down", "down", t=c.gt, flip=True)
    bubble(g, 640, 250, "USE ONCE. THROW AWAY.", seg(c.t, c.w("once") - 0.3, 0.3), tail=-1, size=50)
    bubble(g, 760, 400, "BUY AGAIN.", seg(c.t, c.w("again") - 0.3, 0.3), "#FFE08A", tail=-1, size=50)


def s_gillette(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    char2(g, "gillette", 560, 1430, 1150, "shocked" if c.t > c.w("razor") - 0.4 else "smug", "down", "point", t=c.gt)
    label(g, "KING GILLETTE", 1250, 160, 90, k=pop(c.t, c.w("King") - 0.1, 0.3))
    k = back_out(seg(c.t, c.w("razor") - 0.3, 0.4), 1.7)
    if k > 0:
        razor_blade(g, 1250, 560, 1.5 * k, -0.1, glint=0.5 + 0.5 * math.sin(c.gt * 5))


# ------------------------------------------------------------------ plug prongs (ch 8)
def plug(g, x, y, s=1.0, holes=True):
    with g.at(x, y, 0, s):
        g.rc(0, 80, 220, 170, "#F4F1EA", INK, lw=8, r=30)
        for sd in (-1, 1):
            g.rc(sd * 50, -60, 40, 150, "#D9B26A", INK, lw=6, r=4)
            if holes: g.circle(sd * 50, -90, 11, "#22181B", INK, lw=3)
        g.rc(0, 220, 60, 120, "#22181B", INK, lw=6, r=10)


def s_plug_q(g, c):
    kitchen(g, c.gt)
    g.rect(150, 560, 600, 260, "#3E8E5E", INK, lw=10, r=40)            # sofa
    g.rect(110, 520, 120, 300, "#2F6F4A", INK, lw=10, r=30); g.rect(670, 520, 120, 300, "#2F6F4A", INK, lw=10, r=30)
    plug(g, 1200, 520, 1.6)
    char2(g, "modern", 1650, 1300, 900, "curious", "down", "point", t=c.gt, prop=False, flip=True)
    qmark(g, 1200, 220, 140, PAL["yellow"], 0.1, pop(c.t, c.w("holes") - 0.2, 0.3))
    banner(g, c, "PLUG PRONGS")


def s_socket_bump(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    k = ease_io(seg(c.t, c.w("clicked") - 0.8, 0.8))
    g.rc(1200, 540, 500, 600, "#F4F1EA", INK, lw=10, r=40)            # socket cut-away
    g.rc(1200, 540, 380, 480, "#C9CED6", INK, lw=6, r=20)
    for sd in (-1, 1):
        g.rc(1200 + sd * 60, 540, 30, 380, "#D9B26A", INK, lw=5)
        g.circle(1200 + sd * 60 - sd * 18, 470, 14, "#B08A3A", INK, lw=4)        # the bump
    with g.at(560 + 520 * k, 540, -math.pi / 2):
        plug(g, 0, 0, 1.2)
    if k > 0.95:
        burst(g, 1200, 470, 60, 140, 8, PAL["yellow"], 10, k=seg(c.t, c.w("clicked"), 0.3))
        label(g, "CLICK!", 1200, 140, 90, k=pop(c.t, c.w("clicked") - 0.05, 0.3))


def s_no_bump(g, c):
    studio(g, c.gt, "#5E6C8A", "#26304A")
    g.rc(960, 540, 500, 600, "#F4F1EA", INK, lw=10, r=40)
    g.rc(960, 540, 380, 480, "#C9CED6", INK, lw=6, r=20)
    for sd in (-1, 1):
        g.path(f"M{960 + sd * 60} 330 Q{960 + sd * 30} 540 {960 + sd * 60} 750", None, "#D9B26A", lw=26)
    no_sign(g, 1500, 400, 120, pop(c.t, c.w("bump") - 0.2, 0.3))
    with g.screen():
        if c.t > c.w("bump") - 0.2: g.text("BUMP", 1500, 410, 46, PAL["cream"], sw=8)
    label(g, "SPRINGY METAL", 960, 940, 64, PAL["cream"], k=pop(c.t, c.w("springy") - 0.2, 0.3))


def s_standard(g, c):
    studio(g, c.gt, "#3A4250", "#151820")
    with g.at(960, 540, -0.02, back_out(seg(c.t, 0.1, 0.4), 1.5)):
        g.rc(0, 0, 1100, 640, "#F4F1EA", INK, lw=10, r=8)
        g.text("OFFICIAL STANDARD", 0, -230, 64, INK, stroke=None)
        for j in range(3): g.line([(-420, -140 + j * 50), (420, -140 + j * 50)], "#C9CED6", 10)
        k = seg(c.t, c.w("optional") - 0.3, 0.3)
        if k > 0:
            g.rc(0, 110, 980, 200, "#FFE58A", None, r=10, a=k)
            g.text("\"The hole is optional,", 0, 80, 56, INK, stroke=None)
            g.text("for manufacturing.\"", 0, 150, 56, INK, stroke=None, a=seg(c.t, c.w("manufacturing") - 0.3, 0.3))
    char2(g, "engineer", 1700, 1300, 800, "bored", "down", "down", t=c.gt, flip=True)


def s_mould(g, c):
    studio(g, c.gt, "#2F5F6A", "#10263B")
    k = ease_io(seg(c.t, 0.4, max(0.5, c.T - 1.2)))
    for sd in (-1, 1):
        g.rc(960 + sd * 80, 400, 50, 260, "#D9B26A", INK, lw=6, r=4)
        g.circle(960 + sd * 80, 380, 13, "#22181B", INK, lw=3)
        g.line([(960 + sd * 80, 380), (960 + sd * 240, 380)], "#9AA3AD", 16)            # machine pins through the holes
        g.rc(960 + sd * 300, 380, 140, 70, "#5A5A6A", INK, lw=6, r=8)
    g.rc(960, 620, 360 * k + 1, 260 * k + 1, "#F4F1EA", INK, lw=8, r=40)
    label(g, "PINS HOLD THE PRONGS", W / 2, 120, 70, k=pop(c.t, c.w("hold") - 0.2, 0.3))


def s_boring(g, c):
    kitchen(g, c.gt)
    plug(g, 1250, 560, 1.6)
    char2(g, "modern", 620, 1380, 1050, "bored", "hip", "hip", t=c.gt, prop=False)


# ------------------------------------------------------------------ crackers (ch 6)
def s_cracker_q(g, c):
    kitchen(g, c.gt)
    g.ellipse(1150, 760, 380, 90, "#FFFFFF", INK, lw=8)
    for i in range(3):
        cracker(g, 1000 + i * 150, 690 - i * 30, 0.6, rot=0.2 * i - 0.2)
    char2(g, "modern", 520, 1350, 1000, "curious", "down", "point", t=c.gt, prop=False)
    qmark(g, 1150, 300, 170, PAL["yellow"], 0.1, pop(c.t, c.w("holes") - 0.2, 0.3))
    banner(g, c, "CRACKER HOLES")


def s_oven_steam(g, c):
    bakery(g, c.gt)
    with g.at(1440, 640, 0, 1.2):
        cracker(g, 0, 0, 0.7, holes=0, puff=0.0)
    for i in range(6):
        u = (c.gt * 0.8 + i / 6) % 1
        g.circle(1340 + i * 40, 600 - 120 * u, 14 + 20 * u, "#FFFFFF", None, a=0.6 * (1 - u))
    char2(g, "baker", 600, 1400, 1100, "curious", "down", "point", t=c.gt)
    label(g, "WATER → STEAM", 1440, 160, 80, k=pop(c.t, c.w("steam") - 0.2, 0.3))


def s_puff(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    p = ease_io(seg(c.t, c.w("bubbles") - 0.4, 1.4))
    cracker(g, 960, 560, 1.4, holes=0, puff=p)
    label(g, "PUFF!", 1500, 260, 110, k=pop(c.t, c.w("pillow") - 0.2, 0.3), rot=0.1)


def s_docking(g, c):
    bakery(g, c.gt, 0.5)
    g.rect(300, 700, 1200, 60, "#E9C27A", INK, lw=8, r=8)             # dough sheet
    x = 380 + 1000 * ease_io(seg(c.t, 0.3, max(0.5, c.T - 0.8)))
    for i in range(int((x - 380) / 60)):
        g.circle(410 + i * 60, 730, 8, "#B08A3A", INK, lw=3)
    with g.at(x, 650, c.gt * 6):                                       # spiked roller
        g.circle(0, 0, 60, "#9AA3AD", INK, lw=7)
        for k in range(10):
            a = k * TAU / 10
            g.line([(60 * math.cos(a), 60 * math.sin(a)), (82 * math.cos(a), 82 * math.sin(a))], INK, 8)
    g.line([(x, 650), (x - 120, 420)], "#7A5236", 16)
    char2(g, "baker", x - 330, 1450, 1050, "smug", "reach_r", "reach_r", t=c.gt)
    label(g, "DOCKING", 1400, 200, 100, k=pop(c.t, c.w("docking") - 0.2, 0.3))


def s_escape(g, c):
    studio(g, c.gt, "#FFC93C", "#B8862A")
    cracker(g, 960, 600, 1.4, holes=9)
    for i in range(9):
        hx = 960 + ((i % 3) - 1) * 140; hy = 600 + ((i // 3) - 1) * 140
        u = (c.gt * 0.9 + i * 0.11) % 1
        g.circle(hx, hy - 220 * u, 10 + 16 * u, "#FFFFFF", None, a=0.7 * (1 - u))
    check(g, 1500, 300, 70, seg(c.t, c.w("crisp") - 0.2, 0.3))


def s_holes_compare(g, c):
    studio(g, c.gt, "#2F5F6A", "#10263B")
    cracker(g, 420, 560, 0.85, holes=1, puff=0.8)
    cracker(g, 960, 560, 0.85, holes=9)
    cracker(g, 1500, 560, 0.85, holes=49, col="#C9A262")
    with g.screen():
        g.text("TOO FEW", 420, 860, 56, PAL["cream"], sw=10, sc=pop(c.t, c.w("few") - 0.2, 0.3))
        g.text("TOO MANY", 1500, 860, 56, PAL["cream"], sw=10, sc=pop(c.t, c.w("many") - 0.2, 0.3))
        g.text("JUST RIGHT", 960, 860, 60, PAL["yellow"], sw=12, sc=pop(c.t, c.w("measured") - 0.2, 0.3))


# ------------------------------------------------------------------ ending (ch 7)
def s_recap(g, c, items):
    studio(g, c.gt)
    for i, (wd, fn, x) in enumerate(items):
        k = back_out(seg(c.t, c.w(wd) - 0.2, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, 540, 0.05 * math.sin(c.gt * 2 + i), k):
            fn(g)


R1 = [("Ridges", lambda g: coin(g, 0, 0, 140, "silver", True, face="value"), 300),
      ("lid", lambda g: manhole(g, 0, 0, 140, tilt=1.0, hole=False), 740),
      ("colour", lambda g: road_sign(g, 0, 0, 140, "octagon", "#F2C14E", "STOP", INK, border=INK), 1180),
      ("bag", lambda g: paper_bag(g, 0, 160, 0.95), 1620)]
R2 = [("cap", lambda g: bottle_cap(g, 0, 0, 160), 620),
      ("holes", lambda g: cracker(g, 0, 0, 0.9), 1300)]


def s_accident(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    for i, fn in enumerate((lambda g: coin(g, 0, 0, 90, "silver", True, face="value"), lambda g: manhole(g, 0, 0, 90, tilt=1.0, hole=False),
                            lambda g: road_sign(g, 0, 0, 90, "octagon"), lambda g: paper_bag(g, 0, 100, 0.6), lambda g: bottle_cap(g, 0, 0, 90),
                            lambda g: plug(g, 0, 0, 0.7), lambda g: cracker(g, 0, 0, 0.5))):
        with g.at(240 + i * 240, 600, 0):
            fn(g)
    label(g, "NOT AN ACCIDENT", W / 2, 220, 110, PAL["cream"], k=pop(c.t, c.w("accident") - 0.2, 0.3))


def s_thumb(g, c):
    pocket_bg(g, c.gt)
    with g.group(0.25 * ease_out(seg(c.t, c.w("Newton") - 0.5, 0.8))):
        char2(g, "newton", 1550, 1500, 1200, "smug", "down", "down", t=c.gt, flip=True)
    coin_edge(g, 860, 560, 1300, 260, "silver", ridges=True)
    x = 300 + 1100 * ease_io(seg(c.t, c.w("thumb") - 0.2, 2.0))
    g.rc(x, 360, 200, 260, CAST_SKIN, INK, lw=10, r=100)
    g.rc(x, 280, 120, 90, "#F2DCCB", INK, lw=5, r=40)
    label(g, "THE TRAP", 960, 900, 90, k=pop(c.t, c.w("trap") - 0.2, 0.3))


def s_next(g, c):
    kitchen(g, c.gt)
    char2(g, "modern", 960, 1450, 1150, "curious", "hip", "point", t=c.gt, prop=False)
    for i, (x, y) in enumerate(((400, 300), (1500, 300), (1550, 640), (360, 640))):
        qmark(g, x, y, 120, PAL["yellow"], 0.2 * math.sin(i), pop(c.t, 0.2 + i * 0.25, 0.3))
    bubble(g, 1450, 160, "COMMENTS ↓", seg(c.t, c.w("comments") - 0.3, 0.3), tail=-1, size=52)


def s_endscreen(g, c):
    """20 s end screen: wordmark + two empty frames for YouTube's end-screen video elements + Wy."""
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


# ------------------------------------------------------------------ the cut
def P(lid, fn, part=(0, 1), **kw):
    V.shot(lid, fn, part=part, **kw)


Z = lambda z0, z1, f: push(z0, z1, f)

# cold open
P("O01", s_open, (0, "snips"), cam=Z(1.0, 1.06, (1000, 600)), tr="cut", music="mystery", sfx=[(0.3, "tick", 0.25)])
P("O01", s_snipclose, ("snips", 1), cam=Z(1.04, 1.0, (960, 600)), sfx=[("snips", "click", 0.5)])
P("O02", s_snipclose, cam=Z(1.0, 1.08, (960, 600)), sfx=[(0.1, "click", 0.4), (0.5, "click", 0.4), (0.8, "click", 0.4)])
P("O03", s_melt, (0, "spends"), cam=Z(1.0, 1.05, (900, 500)), sfx=[(0.3, "melt", 0.4)])
P("O03", s_spend, ("spends", 1), cam=Z(1.0, 1.04, (1000, 560)), sfx=[(0.2, "coin_single", 0.4)])
P("O04", s_england, (0, "And"), cam=Z(1.0, 1.05, (900, 520)), sfx=[(0.3, "pop", 0.35)])
P("O04", s_newton, ("And", 1), cam=Z(1.0, 1.08, (900, 420)), tr=("iris", (900, 420), 0.5), sfx=[("Isaac", "sting", 0.45)])
P("O05", s_pocket, (0, "So"), cam=Z(1.0, 1.06, (960, 560)), music="curious", sfx=[(0.1, "shimmer", 0.4)])
P("O05", s_montage, ("So", 1), sfx=[("stop", "pop", 0.4), ("manholes", "pop", 0.4), ("bottle", "pop", 0.4), ("crackers", "pop", 0.4)])
P("O06", s_problems, cam=Z(1.0, 1.05, (960, 540)), sfx=[("fix", "chime", 0.4)])
V.pause["O06"] = CH_PAUSE
# coins
P("C101", s_coin_q, (0, "ridges"), tr="flash", sfx=[(0.2, "whoosh", 0.4)])
P("C101", s_edge_macro, ("ridges", 1), cam=Z(1.0, 1.1, (960, 520)))
P("C102", s_hammer, (0, "They"), music="story", sfx=[(0.2, "drum_hit", 0.25)])
P("C102", s_wobbly, ("They", 1), cam=Z(1.0, 1.05, (960, 520)))
P("C103", s_treason, cam=Z(1.0, 1.06, (1200, 520)), sfx=[("treason", "drum_hit", 0.45)])
P("C104", s_press, cam=Z(1.0, 1.05, (960, 420)), sfx=[(0.4, "drum_hit", 0.25)])
P("C105", s_trim_test, cam=Z(1.0, 1.06, (960, 480)), sfx=[("Anyone", "ding", 0.4)])
P("C106", s_newton_desk, (0, "He"), cam=Z(1.0, 1.05, (900, 500)))
P("C106", s_chaloner, ("He", 1), cam=Z(1.0, 1.06, (960, 600)), sfx=[("Chaloner", "sting", 0.4)])
P("C107", s_candle_out, music="dark", sfx=[("hanged", "whoosh_soft", 0.4)])
P("C108", s_clad, music="curious", tr="flash")
P("C109", s_blind, cam=Z(1.0, 1.05, (1200, 540)), sfx=[("ridges", "shimmer", 0.4)])
V.pause["C109"] = CH_PAUSE
# manholes
P("C201", s_street_q, tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4)])
P("C202", s_square_fall, cam=Z(1.0, 1.04, (960, 600)), sfx=[("side", "creak", 0.35)])
P("C203", s_clang, sfx=[("Clang", "drum_hit", 0.6)])
P("C204", s_width, cam=Z(1.0, 1.04, (960, 560)), sfx=[("never", "ding", 0.4)])
P("C205", s_roll, cam=Z(1.0, 1.03, (900, 760)))
P("C206", s_reuleaux, music="curious")
P("C207", s_engineer_shrug)
V.pause["C207"] = CH_PAUSE
# stop signs
P("C301", s_stop_q, tr="flash", music="curious", sfx=[(0.2, "whoosh", 0.4)])
P("C302", s_1923, cam=Z(1.0, 1.05, (960, 600)), music="story")
P("C303", s_railway, sfx=[(0.3, "rush", 0.35)])
P("C304", s_shapes_row, sfx=[("stop", "pop", 0.4), ("caution", "pop", 0.4), ("care", "pop", 0.4), ("information", "pop", 0.4)])
P("C305", s_twist, cam=Z(1.0, 1.08, (1180, 400)), music="tension", sfx=[("twist", "sting", 0.45)])
P("C306", s_yellow, sfx=[(0.0, "swell", 0.4)])
P("C307", s_fade, music="curious", sfx=[("miss", "rush", 0.3)])
P("C308", s_1954, cam=Z(1.0, 1.05, (960, 400)), sfx=[("red", "chime", 0.45)])
V.pause["C308"] = CH_PAUSE
# paper bags
P("C401", s_bag_q, tr="flash", music="story", sfx=[(0.2, "whoosh", 0.4)])
P("C402", s_envelope, sfx=[("fell", "bloop", 0.4)])
P("C403", s_knight_factory, cam=Z(1.0, 1.05, (760, 600)))
P("C404", s_model, cam=Z(1.0, 1.04, (1000, 600)), sfx=[(0.5, "creak", 0.3)])
P("C405", s_annan, music="tension", sfx=[("patented", "sting", 0.45)])
P("C406", s_court, cam=Z(1.0, 1.04, (1200, 500)), sfx=[(0.1, "gavel", 0.4), ("woman", "hmm", 0.35)])
P("C407", s_evidence, sfx=[("drawings", "pop", 0.4), ("notes", "pop", 0.4), ("diary", "pop", 0.4)])
P("C408", s_won, music="warm", sfx=[("won", "chime", 0.5)])
V.pause["C408"] = CH_PAUSE
# bottle caps
P("C501", s_cap_count, tr="flash", music="playful", sfx=[(0.6, "tick", 0.3)])
P("C502", s_cork, cam=Z(1.0, 1.05, (960, 500)), sfx=[(0.4, "pop", 0.35)])
P("C503", s_painter, cam=Z(1.0, 1.05, (1100, 520)), sfx=[("crimped", "click", 0.4)])
P("C504", s_24, sfx=[(0.1, "ding", 0.4)])
P("C505", s_21, sfx=[("twenty-one", "ding", 0.45)])
P("C506", s_opener, sfx=[(0.3, "pop", 0.45)])
P("C507", s_advice, cam=Z(1.0, 1.04, (960, 500)), music="curious")
P("C508", s_gillette, cam=Z(1.0, 1.05, (1100, 500)), sfx=[("razor", "shimmer", 0.45)])
V.pause["C508"] = CH_PAUSE
# plug prongs
P("P01", s_plug_q, tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4)])
P("P02", s_socket_bump, sfx=[("clicked", "click", 0.5)])
P("P03", s_no_bump, cam=Z(1.0, 1.04, (960, 540)))
P("P04", s_standard, cam=Z(1.0, 1.05, (960, 560)), music="curious", sfx=[("optional", "ding", 0.35)])
P("P05", s_mould)
P("P06", s_boring, cam=Z(1.0, 1.05, (900, 600)))
V.pause["P06"] = CH_PAUSE
# crackers
P("C601", s_cracker_q, tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4)])
P("C602", s_oven_steam, cam=Z(1.0, 1.04, (1200, 560)))
P("C603", s_puff, sfx=[("pillow", "boing", 0.3)])
P("C604", s_docking, sfx=[(0.3, "tick", 0.3)])
P("C605", s_escape, cam=Z(1.0, 1.04, (960, 560)), sfx=[("crisp", "ding", 0.4)])
P("C606", s_holes_compare)
V.pause["C606"] = CH_PAUSE
# ending
P("E01", lambda g, c: s_recap(g, c, R1), music="warm", tr="flash")
P("E02", lambda g, c: s_recap(g, c, R2))
P("E03", s_accident, sfx=[("accident", "drum_hit", 0.4)])
P("E04", s_thumb, cam=Z(1.0, 1.05, (860, 520)))
P("E05", s_next, sfx=[("comments", "pop", 0.4)])
V.build()

# 20 s end screen after the last line (long videos: wordmark end screen, CLAUDE.md)
END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line="E05", fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "Isaac Newton vs the coin clippers"), ("C101", "Why coins have ridges"), ("C201", "Why manhole covers are round"),
            ("C301", "Why stop signs have 8 sides (and used to be yellow)"), ("C401", "Why paper bags have flat bottoms"),
            ("C501", "Why bottle caps have 21 teeth"), ("P01", "Why plug prongs have holes"), ("C601", "Why crackers have holes"),
            ("E01", "None of these shapes are an accident")]


def chapters():
    out = []
    for lid, name in CHAPTERS:
        t = min(sh["start"] for sh in V.shots if sh["line"] == lid)
        out.append(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=10, scale=0.12))
    elif cmd == "qa":
        print(dict(duration=V.duration, shots=len(V.shots), max_shot=max(s["dur"] for s in V.shots if s["kind"] != "end")))
    elif cmd == "chapters":
        print("\n".join(chapters()))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "animatic":
        V.render(str(EP / "animatic/animatic.mp4"), crf=30, preset="veryfast")
    elif cmd == "render":
        V.render(str(EP / "final/B-004.mp4"))
