"""B-005 (L5) "Why Toast Lands Butter-Side Down, Shoelaces Untie and Earbuds Tangle" — long video, Style F + cast v2.2, 1920x1080.
python episodes/B-005-annoying-science/make.py sheet|qa|big <t,..>|chapters|animatic|render
Sets: morning kitchen, treadmill lab, tumbling-box lab, night pasta kitchen + MIT bench, bathroom, cafe table, breakfast bowl.
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import qmark, no_sign, sparkles, arrow, burst, ring_wave, steam, flake
from flat_annoy import *

V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="curious", captions=False)
CH_PAUSE = 1.3
SKIN = "#D8A580"


# ------------------------------------------------------------------ helpers
def tw(c, word, n=0, frac=0.5):
    """Shot-local time of a word; falls back to a fraction of the shot if the word is not found."""
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def banner(g, c, txt, t0=0.0):
    t = c.t - t0
    if t > 2.8 or t < 0: return
    k = back_out(seg(t, 0, 0.35), 1.4) * (1 - ease_in(seg(t, 2.3, 0.4)))
    with g.screen():
        with g.at(80 - 760 * (1 - k), 96, -0.02):
            w = g.text_w(txt, 64) + 70
            g.rect(0, -46, w, 92, PAL["yellow"], INK, lw=8, r=18)
            g.text(txt, w / 2, 4, 64, INK, stroke=None)


def label(g, txt, x, y, size=70, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x, y, k=1.0, size=46):
    """Small context label (year/place) on screen (why_not_viral rule 2: context as a label, story keeps moving)."""
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def studio(g, t, a="#1590A0", b="#0B3F4C"):
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


def trophy(g, x, y, s=1.0, k=1.0):
    if k <= 0: return
    with g.at(x, y, 0, s * back_out(clamp(k), 1.7)):
        g.path("M-80 -160 L80 -160 Q80 -40 0 -20 Q-80 -40 -80 -160 Z", PAL["yellow"], INK, lw=8)
        g.path("M-80 -140 Q-140 -140 -120 -90 Q-100 -60 -60 -60", None, INK, lw=10)
        g.path("M80 -140 Q140 -140 120 -90 Q100 -60 60 -60", None, INK, lw=10)
        g.rect(-14, -24, 28, 50, "#E0A92A", INK, lw=6)
        g.rc(0, 40, 140, 36, "#6E4A3A", INK, lw=7, r=8)
        g.text("?", 0, -95, 70, INK, stroke=None)


# ------------------------------------------------------------------ sets
FL = 860   # floor line in the kitchen


def kitchen_am(g, t, light=1.0):
    """Morning kitchen: blue-grey tiles, sunny window, counter on the left."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#CFE8EE", "#A9D3DC"))
    with g.layer(0.5):
        for i in range(-1, 16):
            for j in range(8):
                g.rect(i * 130 + (65 if j % 2 else 0), j * 110, 126, 106, "#DDF0F3", None, r=8, a=0.8)
        g.rect(1240, 110, 460, 330, "#FFE9A8", INK, lw=10, r=10)
        g.circle(1560, 220, 70, "#FFC93C", None, a=0.9)
        g.line([(1470, 110), (1470, 440)], INK, 8); g.line([(1240, 275), (1700, 275)], INK, 8)
        g.rect(-60, 470, 520, 40, "#3E8E7A", INK, lw=8)
        g.rect(-60, 510, 520, 360, "#2F6F62", INK, lw=8)
        g.rect(120, 380, 120, 90, "#9AA3AD", INK, lw=7, r=10)      # toaster
        g.rect(150, 360, 20, 30, "#F3D08A", INK, lw=4); g.rect(190, 360, 20, 30, "#F3D08A", INK, lw=4)
    g.rect(-100, FL, W + 200, H, "#E7C9A0", INK, lw=8)
    for i in range(-1, 16):
        g.line([(i * 170, FL), (i * 170 - 120, H)], "#D4B387", 5)
    g.glow(1500, 260, 700 * light, "#FFE08A", 0.22 * light)


def lab(g, t, a="#2F3E46", b="#1E2A30"):
    """Clean physics lab wall with shelves and a whiteboard."""
    g.fill_all(g.lgrad(0, 0, 0, H, a, b))
    with g.layer(0.5):
        for i in range(9):
            g.line([(i * 240, 0), (i * 240, FL)], shade(a, 0.9), 4)
        g.rect(1180, 150, 560, 320, "#F4F6F8", INK, lw=10, r=10)
        g.line([(1230, 260), (1340, 210), (1450, 300), (1560, 240), (1690, 280)], "#3E7CB1", 6)
        g.text("F = ma", 1330, 400, 46, "#FF6B5B", stroke=None)
        g.rect(120, 260, 380, 22, "#6E4A3A", INK, lw=6)
        for k in range(4):
            g.rc(170 + k * 90, 220, 50, 80, ("#5ED3B5", "#FFC93C", "#FF6B5B", "#BDEBFF")[k], INK, lw=5, r=10)
    g.rect(-100, FL, W + 200, H, "#3A4650", INK, lw=8)


def night_kitchen(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#1E2440", "#2C2F4E"))
    with g.layer(0.5):
        g.rect(1300, 120, 380, 300, "#0F1630", INK, lw=10, r=8)
        g.circle(1560, 210, 46, "#FFF4E0", None, a=0.9)
        for (sx, sy) in ((1380, 180), (1430, 330), (1620, 360)):
            g.circle(sx, sy, 5, "#FFF4E0", None)
        g.line([(1490, 120), (1490, 420)], INK, 8)
        g.circle(420, 200, 70, "#F4F1EA", INK, lw=8)                # wall clock
        g.line([(420, 200), (420, 150)], INK, 7); g.line([(420, 200), (460, 220)], INK, 7)
    g.rect(-100, 700, W + 200, 40, "#6E4A3A", INK, lw=8)
    g.rect(-100, 740, W + 200, H, "#4A3028", INK, lw=8)
    g.glow(900, 300, 700, "#FFC86A", 0.22)
    g.line([(900, 0), (900, 160)], INK, 6)
    g.path("M820 160 L980 160 L940 220 L860 220 Z", "#FFC93C", INK, lw=7)


def bathroom(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#E9F4F6", "#CFE3E8"))
    with g.layer(0.6):
        for i in range(-1, 18):
            for j in range(10):
                g.rect(i * 110, j * 110, 106, 106, "#F7FCFD", "#B8D2D8", lw=3, r=6)
    g.rect(-100, 900, W + 200, H, "#9FBFC6", INK, lw=8)


def cafe(g, t):
    """Top view of a wooden cafe table."""
    g.fill_all("#B9824F")
    for i in range(-1, 12):
        g.rect(-60, i * 120, W + 120, 116, "#C38D58" if i % 2 else "#B57F4C", None)
        g.line([(-60, i * 120), (W + 60, i * 120)], "#8A5A32", 4)
        g.ellipse(300 + (i * 470) % 1600, i * 120 + 60, 60, 14, None, "#9A6A3E", lw=3)


def breakfast(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE3B0", "#FFC98A"))
    for i in range(-1, 12):
        for j in range(-1, 7):
            if (i + j) % 2 == 0:
                g.rect(i * 180, j * 180, 180, 180, "#FFD79E", None, a=0.7)


# ------------------------------------------------------------------ toast physics
TBL_Y, TBL_X1 = 560, 1080          # tabletop y and right edge in the kitchen


def toast_fall(g, k, x0=TBL_X1 - 40, y0=TBL_Y - 26, floor=FL - 24, turns=0.5, push=0.0, s=1.0):
    """Toast leaving the table edge at progress k (0..1): tips, spins `turns`, lands on the floor."""
    kk = clamp(k)
    x = x0 + (60 + push * 420) * kk
    y = y0 + (floor - y0) * kk ** 2
    rot = turns * TAU * ease_in(min(1, kk * 1.05))
    toast(g, x, y, s, rot)
    return x, y, rot


def splat(g, x, y, k):
    if k <= 0: return
    burst(g, x, y + 10, 60, 160, 10, PAL["cream"], 10, k=k)


def s_hook(g, c):
    """Frame 1: toast already tumbling off the table; shocked face; NOT BAD LUCK?"""
    kitchen_am(g, c.gt)
    table_side(g, 820, TBL_Y, 560, "#C97B4A", FL - TBL_Y - 36)
    plate(g, 820, TBL_Y - 6, 280)
    char2(g, "modern", 330, 1060, 860, "shocked", "up", "point", t=c.gt, prop=False)
    k = seg(c.gt, -0.35, 1.25)                              # already moving at frame 0
    x, y, _ = toast_fall(g, k, x0=TBL_X1 - 220, turns=0.5, s=1.5)
    if k >= 1:
        splat(g, x, y, seg(c.gt, 0.9, 0.3))
    for i in range(3):
        g.line([(x - 160 - i * 40, y - 60 + i * 30), (x - 110 - i * 40, y - 70 + i * 30)], INK, 6, a=0.5 * (1 - clamp(k)))
    with g.screen():
        g.text("NOT BAD LUCK?", W / 2, 140, 150, "#FF6B5B", sw=22, depth=10, sc=pop(c.gt + 0.25, 0.0, 0.25))


def s_landed(g, c):
    kitchen_am(g, c.gt)
    with g.at(0, 0):
        toast(g, 1150, FL - 22, 1.6, math.pi)
        g.path("M1000 %d Q1150 %d 1300 %d" % (FL + 4, FL + 30, FL + 4), BUTTER, INK, lw=5)
    char2(g, "modern", 600, 1100, 950, "bored" if c.t < tw(c, "luck") else "suspicious", "hip", "point", t=c.gt, prop=False)
    label(g, "BUTTER-SIDE DOWN", 1200, 300, 80, k=pop(c.t, 0.1, 0.3))
    cross(g, 1200, 470, 60, seg(c.t, tw(c, "luck") - 0.2, 0.3))
    if c.t > tw(c, "luck"):
        label(g, "BAD LUCK", 1200, 580, 60, PAL["cream"], k=1)


def s_culprit(g, c):
    lab(g, c.gt)
    table_side(g, 1150, 600, 600, "#C97B4A", FL - 636)
    plate(g, 1150, 594, 260); toast(g, 1150, 570, 0.9)
    char2(g, "physicist", 520, 1080 + 30, 950, "smug", "down", "point", t=c.gt)
    ruler_v(g, 1520, 600, FL, "TABLE HEIGHT", k=ease_out(seg(c.t, tw(c, "height") - 0.4, 0.6)))
    label(g, "THE CULPRIT?", 1150, 260, 84, "#FF6B5B", k=pop(c.t, tw(c, "culprit") - 0.1, 0.3))


def s_montage(g, c, items):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    for wd, x, fn in items:
        k = back_out(seg(c.t, tw(c, wd) - 0.15, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, 560, 0.06 * math.sin(c.gt * 2 + x), k):
            fn(g, c)


def ic_toast(g, c): toast(g, 0, 0, 1.2, 0.5 * math.sin(c.gt * 3))
def ic_lace(g, c): sneaker(g, 0, 80, 0.75); bow_knot(g, -20, -40, 0.75, 0.4 + 0.3 * math.sin(c.gt * 4), 0.6 * math.sin(c.gt * 6))
def ic_buds(g, c): earbuds(g, 0, 0, 0.9, 0.9 + 0.1 * math.sin(c.gt))
def ic_pasta(g, c):
    spaghetti(g, -220, 0, -70, -40, 0); spaghetti(g, -50, -50, 60, -50, 0); spaghetti(g, 80, -40, 220, 0, 0)
    burst(g, -60, -45, 20, 60, 8, PAL["cream"], 6, k=1)
def ic_curtain(g, c): curtain(g, -150, 150, -220, 220, 0.8 + 0.2 * math.sin(c.gt * 2), t=c.gt)
def ic_coffee(g, c): coffee_drop(g, 0, 0, 140, 0.9, 1.0)
def ic_cereal(g, c):
    bowl_top(g, 0, 0, 150)
    for i in range(5):
        cereal_loop(g, -40 + 34 * math.cos(i * 1.3), -20 + 30 * math.sin(i * 1.3), 34, i)


def s_tests(g, c):
    """Treadmill, spinning box and a computer showing a shower curtain pop in on their words."""
    lab(g, c.gt, "#24414A", "#16282E")
    k1, k2, k3 = (back_out(seg(c.t, tw(c, w) - 0.15, 0.35), 1.6) for w in ("treadmills", "spinning", "computer"))
    if k1 > 0:
        with g.at(420, 760, 0, k1):
            g.path("M-260 0 L260 0 L300 60 L-300 60 Z", "#4A4A55", INK, lw=8)
            for i in range(8):
                xx = -260 + ((i * 70 + c.gt * 300) % 520)
                g.line([(xx, 8), (xx + 20, 52)], "#6A6A75", 5)
            g.line([(220, 0), (260, -320)], "#9AA3AD", 14); g.rc(260, -330, 120, 40, "#22181B", INK, lw=6, r=8)
    if k2 > 0:
        with g.at(960, 560, 0, k2):
            tumble_box(g, 0, 0, 140, c.gt * TAU * 0.6, c.gt)
    if k3 > 0:
        with g.at(1500, 600, 0, k3):
            g.rc(0, 0, 420, 300, "#22181B", INK, lw=10, r=16)
            g.rc(0, 0, 380, 260, "#BDEBFF", None, r=8)
            curtain(g, -120, 120, -110, 110, 0.6 + 0.3 * math.sin(c.gt * 2), t=c.gt)
            g.rect(-30, 150, 60, 60, "#5A5A6A", INK, lw=6); g.rc(0, 220, 200, 24, "#5A5A6A", INK, lw=6, r=8)
    if c.t > tw(c, "curtain") - 0.2:
        label(g, "2 WEEKS!", 1500, 300, 80, "#FF6B5B", k=pop(c.t, tw(c, "curtain") - 0.2, 0.3))


def s_start(g, c):
    kitchen_am(g, c.gt)
    table_side(g, 820, TBL_Y, 560, "#C97B4A", FL - TBL_Y - 36)
    plate(g, 820, TBL_Y - 6, 280)
    toast(g, 820, TBL_Y - 30, 1.1, 0.0)
    char2(g, "modern", 1400, 1080 + 40, 980, "curious", "hip", "think", t=c.gt, prop=False, flip=True)
    for i, (x, y) in enumerate(((560, 300), (1080, 280), (820, 220))):
        qmark(g, x, y, 100, PAL["coral"], 0.2 * math.sin(i + c.gt), pop(c.t, 0.2 + i * 0.25, 0.3))


# ch1 toast
def s_push(g, c, slow=False):
    kitchen_am(g, c.gt, 0.8)
    table_side(g, 760, TBL_Y, 640, "#C97B4A", FL - TBL_Y - 36)
    k_push = ease_io(seg(c.t, 0.2, 1.4))
    x = 620 + 400 * k_push
    fist_x = x - 190
    toast(g, x, TBL_Y - 26, 1.2, 0.18 * clamp((x - 990) / 60))
    g.rc(fist_x, TBL_Y - 40, 120, 60, SKIN, INK, lw=8, r=28)
    g.rc(fist_x - 120, TBL_Y - 40, 160, 70, "#3E8E5E", INK, lw=8, r=20)
    label(g, "WATCH CLOSELY", 1400, 250, 70, PAL["cream"], k=pop(c.t, tw(c, "watch") - 0.1, 0.3))
    g.circle(1060, TBL_Y - 40, 120, None, PAL["yellow"], lw=8, a=0.6 * on(c, "closely"))


def s_tip(g, c):
    """Slow motion: the toast pivots on the table edge and starts to spin; ghost trail shows the rotation."""
    kitchen_am(g, c.gt, 0.7)
    table_side(g, 700, TBL_Y, 760, "#C97B4A", FL - TBL_Y - 36)
    k = ease_io(seg(c.t, 0.2, c.T - 0.6))
    for j in range(5):
        kj = k * (j + 1) / 5
        with g.group(0.18 + 0.16 * j):
            toast_fall(g, kj * 0.55, x0=TBL_X1 - 30, turns=0.5, s=1.3)
    if c.t > tw(c, "spin") - 0.2:
        arrow(g, 1280, 380, 1380, 520, PAL["yellow"], 18, k=on(c, "spin"))
        label(g, "SPIN!", 1450, 330, 90, k=pop(c.t, tw(c, "spin") - 0.1, 0.3))
    label(g, "NOT FLAT", 500, 250, 70, PAL["cream"], k=pop(c.t, tw(c, "flat") - 0.1, 0.3))
    tag(g, "SLOW MOTION ×10", 1620, 1010, k=pop(c.t, 0.1, 0.3), size=36)


def s_matthews(g, c):
    """1995: a physicist at a desk calculating (generic cast, never the real person's likeness)."""
    lab(g, c.gt, "#3A3550", "#24203A")
    g.rect(820, 640, 900, 40, "#7A5236", INK, lw=8, r=6)
    g.rect(870, 680, 40, 200, "#5B3B2E", INK, lw=7); g.rect(1630, 680, 40, 200, "#5B3B2E", INK, lw=7)
    char2(g, "prof", 640, 1080 + 30, 980, "curious" if c.t < tw(c, "much") else "smug", "explain", "think", t=c.gt)
    with g.at(1250, 520, -0.05):
        g.rc(0, 0, 520, 220, "#FFFDF6", INK, lw=8, r=8)
        for i in range(4):
            g.line([(-220, -60 + i * 40), (-220 + 380 * clamp(c.u * 1.6 - i * 0.25), -60 + i * 40)], "#3E7CB1", 6)
        toast(g, 170, -30, 0.35, c.gt * 2)
    tag(g, "1995 · BRITAIN", 1500, 140, k=pop(c.t, tw(c, "1995") - 0.1, 0.3))


def s_halfturn(g, c):
    """Diagram: from table height the toast only manages half a turn → butter down."""
    studio(g, c.gt)
    table_side(g, 560, 430, 600, "#C97B4A", 420)
    g.line([(-100, 886), (W + 100, 886)], PAL["cream"], 8)
    k = ease_io(seg(c.t, 0.3, c.T * 0.75))
    for j in range(7):
        kj = j / 6
        if kj > k + 1e-3: break
        x = 820 + 260 * kj; y = 404 + (860 - 404) * kj ** 2
        with g.group(0.35 if kj < k - 0.05 else 1.0):
            toast(g, x, y, 0.9, math.pi * ease_in(kj))
    if k > 0.98:
        label(g, "½ TURN", 1450, 300, 110, k=pop(c.t, c.T * 0.75 + 0.3, 0.3))
    ruler_v(g, 260, 430, 886, "0.7–1.8 m", PAL["cream"], k=ease_out(seg(c.t, 0.4, 0.6)))


def s_flipped(g, c):
    """The side that started on top ends on the bottom: a highlight follows the butter."""
    studio(g, c.gt, "#1590A0", "#0B3F4C")
    k = ease_io(seg(c.t, tw(c, "top") - 0.2, max(0.8, tw(c, "bottom") - tw(c, "top"))))
    toast(g, 960, 560, 2.6, math.pi * k)
    with g.at(960, 560, math.pi * k, 2.6):
        g.circle(30, -40, 26, None, "#FF6B5B", lw=6, a=0.9)
    label(g, "TOP", 480, 300, 80, PAL["cream"], k=pop(c.t, tw(c, "top") - 0.1, 0.3))
    label(g, "BOTTOM", 1440, 820, 80, "#FF6B5B", k=pop(c.t, tw(c, "bottom") - 0.1, 0.3))


def s_tall_table(g, c):
    """A comically tall 3 m table: the toast completes a full turn and lands butter-up."""
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    floor = 1040
    g.line([(-100, floor), (W + 100, floor)], INK, 10)
    k_grow = ease_io(seg(c.t, tw(c, "taller") - 0.3, 0.9))
    top = lerp(700, 120, k_grow)
    table_side(g, 620, top, 420, "#C97B4A", floor - top - 36)
    char2(g, "modern", 1500, floor, 560, "shocked" if k_grow > 0.5 else "curious", "up", "point", t=c.gt, prop=False, flip=True)
    kf = seg(c.t, tw(c, "full") - 1.0, 1.4)
    if kf <= 0:
        toast(g, 700, top - 26, 0.8)
    else:
        x, y, _ = toast_fall(g, kf, x0=800, y0=top - 26, floor=floor - 20, turns=1.0, s=0.8)
        if kf >= 1:
            check(g, x + 160, y - 120, 50, seg(c.t, tw(c, "full") + 0.4, 0.3))
    ruler_v(g, 300, top, floor, "3 m", k=ease_out(seg(c.t, tw(c, "meters") - 0.5, 0.5)))


def s_fast(g, c):
    kitchen_am(g, c.gt, 0.8)
    table_side(g, 760, TBL_Y, 640, "#C97B4A", FL - TBL_Y - 36)
    k = seg(c.t, tw(c, "fast") - 0.2, 0.9)
    x = TBL_X1 - 40 + 760 * ease_out(k)
    y = TBL_Y - 26 + (FL - 24 - TBL_Y + 26) * ease_in(k)
    toast(g, x, y, 1.1, 0.5 * ease_in(k))
    for i in range(4):
        g.line([(x - 180 - i * 60, y - 30 + i * 18), (x - 120 - i * 60, y - 30 + i * 18)], INK, 6, a=0.6 * clamp(k * 3))
    if k >= 1:
        check(g, x, y - 140, 50, seg(c.t, tw(c, "fast") + 0.8, 0.3))
        label(g, "BUTTER UP", x, y - 260, 64, PAL["mint"], k=pop(c.t, tw(c, "fast") + 0.8, 0.3))


def s_ignobel(g, c):
    studio(g, c.gt, "#FFC93C", "#C97B2A")
    trophy(g, 960, 640, 2.0, seg(c.t, tw(c, "Ig") - 0.2, 0.4))
    label(g, "IG NOBEL PRIZE", 960, 170, 96, PAL["cream"], k=pop(c.t, tw(c, "Prize") - 0.1, 0.3))
    if c.t > tw(c, "laugh") - 0.1:
        label(g, "LAUGH…", 480, 820, 80, "#FF6B5B", k=pop(c.t, tw(c, "laugh") - 0.1, 0.3))
    if c.t > tw(c, "think") - 0.1:
        label(g, "…THEN THINK", 1440, 820, 80, PAL["navy"], k=pop(c.t, tw(c, "think") - 0.1, 0.3))
    toast(g, 960, 300 + 10 * math.sin(c.gt * 3), 0.7, 0.2 * math.sin(c.gt * 2))


# ch2 shoelaces
def s_lace_q(g, c):
    banner(g, c, "WHY SHOELACES COME UNDONE")
    g.fill_all(g.lgrad(0, 0, 0, H, "#8FB7C8", "#5E8FA6"))
    g.rect(-100, 820, W + 200, H, "#4A5A66", INK, lw=8)
    sneaker(g, 960, 780, 1.8)
    loose = 0.15 + 0.6 * ease_io(seg(c.t, tw(c, "undone") - 0.3, 1.2))
    bow_knot(g, 880, 470, 1.6, loose, 0.4 * math.sin(c.gt * 3))
    qmark(g, 1450, 300, 160, PAL["yellow"], 0.15, pop(c.t, tw(c, "tight") - 0.1, 0.3))


def s_treadmill(g, c, close=False):
    lab(g, c.gt, "#2C4650", "#1A2C33")
    with g.at(900, 900, 0):
        g.path("M-420 0 L420 0 L470 80 L-470 80 Z", "#4A4A55", INK, lw=9)
        for i in range(12):
            xx = -420 + ((i * 70 + c.gt * 420) % 840)
            g.line([(xx, 10), (xx + 24, 70)], "#6A6A75", 6)
        g.line([(360, 0), (420, -520)], "#9AA3AD", 18); g.rc(420, -530, 180, 56, "#22181B", INK, lw=7, r=10)
    bob = 18 * abs(math.sin(c.gt * 6))
    char2(g, "runner", 860, 900 - bob, 820, "deadpan", ("explain", "hip", 0.5 + 0.5 * math.sin(c.gt * 6)), ("hip", "explain", 0.5 + 0.5 * math.sin(c.gt * 6)), t=c.gt)
    with g.at(1550, 880, 0):                                          # high-speed camera on a tripod
        g.line([(0, 0), (-60, -360)], INK, 10); g.line([(0, 0), (60, -360)], INK, 10); g.line([(0, 0), (0, -360)], INK, 10)
        g.rc(0, -400, 200, 120, "#22181B", INK, lw=8, r=14)
        g.circle(-110, -400, 46, "#3E7CB1", INK, lw=8)
        g.circle(60, -440, 12, "#FF5B4B" if int(c.gt * 2) % 2 else "#5A1E1E", None)
    tag(g, "2017 · UC BERKELEY", 1500, 140, k=pop(c.t, tw(c, "2017") - 0.1, 0.3))
    if c.t > tw(c, "slow") - 0.2:
        tag(g, "SLOW MOTION", 1550, 500, k=pop(c.t, tw(c, "slow") - 0.1, 0.3), size=40)


def s_stomp(g, c):
    """Close-up: the foot slams down; 7× gravity."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#3A4650", "#22303A"))
    g.rect(-100, 860, W + 200, H, "#4A4A55", INK, lw=8)
    ph = (c.t * 1.4) % 1.0
    y = 820 - 260 * (1 - ease_in(clamp(ph / 0.5))) if ph < 0.5 else 820
    sneaker(g, 900, y, 1.6, rot=-0.15 * (1 - clamp(ph / 0.5)) if ph < 0.5 else 0)
    bow_knot(g, 830, y - 300, 1.3, 0.2 + 0.2 * clamp(c.u), 0.3)
    if ph >= 0.5:
        k = seg(ph, 0.5, 0.25)
        burst(g, 900, 880, 160, 360, 12, PAL["yellow"], 12, k=k)
    label(g, "7 × GRAVITY", 1450, 260, 100, "#FF6B5B", k=pop(c.t, tw(c, "seven") - 0.1, 0.3))


def s_squeeze(g, c):
    """Knot macro: each hit squeezes the knot and it opens a little more."""
    studio(g, c.gt, "#3E7CB1", "#10263B")
    hits = int(c.t * 1.6)
    ph = (c.t * 1.6) % 1
    sq = 0.15 * (1 - ease_out(clamp(ph * 3)))
    loosen = min(0.75, 0.1 + 0.12 * hits + 0.12 * ease_out(clamp(ph * 3)))
    with g.at(960, 520, 0, 1 + sq, 1 - sq):
        bow_knot(g, 0, 0, 2.6, loosen, 0.0)
    for side in (-1, 1):
        arrow(g, 960 + side * 520, 520, 960 + side * 330, 520, PAL["yellow"], 22, k=1 - clamp(ph * 3))
    label(g, "LOOSER…", 960, 900, 80, PAL["cream"], k=pop(c.t, tw(c, "loosens") - 0.1, 0.3))


def s_whip(g, c):
    """The swinging leg whips the free ends: tug-of-war arrows."""
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    sw = 0.9 * math.sin(c.gt * 7)
    bow_knot(g, 960, 420, 2.4, 0.45, sw)
    for side in (-1, 1):
        arrow(g, 960 + side * 150, 700, 960 + side * 420, 860, PAL["cream"], 24, k=on(c, "whips"))
    if c.t > tw(c, "tug") - 0.2:
        label(g, "TUG OF WAR!", 960, 150, 96, PAL["yellow"], k=pop(c.t, tw(c, "tug") - 0.1, 0.3))


def s_neither(g, c):
    """Two tests side by side: stomp only ✗, swing only ✗, then both together → the knot fails."""
    studio(g, c.gt)
    k_st, k_sw, k_bo = (seg(c.t, tw(c, w) - 0.2, 0.3) for w in ("Stomping", "Swinging", "together"))
    for i, (x, k, name) in enumerate(((420, k_st, "STOMP"), (960, k_sw, "SWING"), (1500, k_bo, "BOTH"))):
        if k <= 0: continue
        with g.at(x, 560, 0, back_out(clamp(k * 1.5), 1.5)):
            g.rc(0, 0, 440, 560, "#0B3F4C", PAL["cream"], lw=8, r=30)
            if name == "STOMP":
                y = -40 * abs(math.sin(c.gt * 6))
                bow_knot(g, 0, -60 + y, 1.1, 0.2, 0.0)
            elif name == "SWING":
                bow_knot(g, 0, -60, 1.1, 0.2, 0.8 * math.sin(c.gt * 7))
            else:
                u = ease_in(seg(c.t, tw(c, "together") + 0.2, 1.4))
                bow_knot(g, 0, -60 - 30 * abs(math.sin(c.gt * 6)), 1.1, 0.2 + 0.8 * u, 0.8 * math.sin(c.gt * 7), undone=u)
            g.text(name, 0, 210, 56, PAL["cream"], sw=10)
        if name != "BOTH":
            cross(g, x + 150, 340, 46, seg(c.t, tw(c, "didn't" if name == "STOMP" else "either") - 0.1, 0.3))


def s_fail(g, c):
    """Two strides and the bow falls apart (shoe on the treadmill, close)."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#3A4650", "#22303A"))
    g.rect(-100, 860, W + 200, H, "#4A4A55", INK, lw=8)
    u = ease_in(seg(c.t, tw(c, "fell") - 0.6, 1.0))
    ph = (c.t * 1.6) % 1.0
    y = 820 - 120 * abs(math.sin(ph * math.pi))
    sneaker(g, 960, y, 1.6)
    bow_knot(g, 890, y - 300, 1.3, 0.5 + 0.5 * u, 0.9 * math.sin(c.gt * 7), undone=u)
    n = min(2, int(seg(c.t, tw(c, "two") - 0.6, 1.2) * 2.99))
    for i in range(n):
        g.circle(1500 + i * 120, 220, 44, PAL["yellow"], INK, lw=7)
        g.text(str(i + 1), 1500 + i * 120, 224, 50, INK, stroke=None)
    label(g, "2 STRIDES", 1560, 360, 80, k=pop(c.t, tw(c, "strides") - 0.1, 0.3))


def s_knots(g, c):
    """Weak (twisted, vertical) vs strong (flat) bow."""
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    k1 = back_out(seg(c.t, tw(c, "twists") - 0.3, 0.4), 1.6)
    k2 = back_out(seg(c.t, tw(c, "flat") - 0.3, 0.4), 1.6)
    if k1 > 0:
        with g.at(560, 520, 0, k1):
            bow_knot(g, 0, 0, 1.8, 0.15, 0.1, twist=True)
        label(g, "WEAK", 560, 860, 84, "#FF6B5B", k=k1)
    if k2 > 0:
        with g.at(1360, 520, 0, k2):
            bow_knot(g, 0, 0, 1.8, 0.15, 0.1)
        label(g, "STRONGER", 1360, 860, 84, PAL["yellow"], k=k2)
        check(g, 1360 + 300, 340, 50, seg(c.t, tw(c, "longer") - 0.2, 0.3))
    cross(g, 560 + 300, 340, 50, seg(c.t, tw(c, "weak") - 0.2, 0.3))


def s_strong_fails(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    u = ease_in(seg(c.t, tw(c, "fails") - 0.4, 1.4))
    bow_knot(g, 960, 480, 2.3, 0.15 + 0.85 * u, 0.6 * math.sin(c.gt * 5) * u, undone=u)
    with g.screen():                       # clock showing time passing
        g.circle(1600, 220, 90, "#F4F1EA", INK, lw=8)
        a = c.gt * 4
        g.line([(1600, 220), (1600 + 70 * math.sin(a), 220 - 70 * math.cos(a))], INK, 8)
    label(g, "JUST LATER", 960, 900, 80, PAL["cream"], k=pop(c.t, tw(c, "longer") - 0.1, 0.3))


# ch3 earbuds
def pocket(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3E5A7A", "#24384E"))
    for i in range(-2, 20):
        g.line([(i * 110, 0), (i * 110 + 300, H)], "#36506E", 6)
    g.path("M560 120 L1360 120 L1300 1000 Q960 1060 620 1000 Z", "#2E4766", INK, lw=10)
    g.path("M560 120 Q960 260 1360 120", None, "#FFC93C", lw=8)


def s_buds_q(g, c):
    banner(g, c, "WHY EARBUDS TANGLE")
    pocket(g, c.gt)
    k_out = ease_io(seg(c.t, tw(c, "out") - 0.4, 0.7))
    mess = ease_io(seg(c.t, tw(c, "out") - 0.1, 0.5))
    y = lerp(560, 360, k_out)
    earbuds(g, 960, y, 1.6, mess)
    if mess > 0.5:
        label(g, "HOW?!", 960, 900, 110, "#FF6B5B", k=pop(c.t, tw(c, "How") - 0.1, 0.3))


def s_box_lab(g, c):
    lab(g, c.gt, "#2F3E46", "#1E2A30")
    g.rect(560, 700, 900, 40, "#9AA3AD", INK, lw=8, r=6)
    g.rect(620, 740, 40, 140, "#5A5A6A", INK, lw=7); g.rect(1360, 740, 40, 140, "#5A5A6A", INK, lw=7)
    spin = seg(c.t, tw(c, "spun") - 0.2, 0.3)
    tumble_box(g, 1010, 480, 150, c.gt * TAU * 1.0 * spin, c.gt)
    char2(g, "physicist", 380, 1080 + 30, 900, "curious", "point", "down", t=c.gt)
    char2(g, "doctor", 1620, 1080 + 30, 880, "deadpan", "hold", "down", t=c.gt, flip=True)
    tag(g, "2007 · CALIFORNIA", 1500, 140, k=pop(c.t, tw(c, "2007") - 0.1, 0.3))
    if c.t > tw(c, "ten") - 0.2:
        label(g, "10 SECONDS", 1010, 240, 70, k=pop(c.t, tw(c, "ten") - 0.1, 0.3))


def s_again(g, c):
    studio(g, c.gt, "#24414A", "#16282E")
    n = int(lerp(1, 3415, ease_in(seg(c.t, 0.4, c.T - 0.8))))
    for i in range(6):
        x = 260 + i * 280
        tumble_box(g, x, 560 + 30 * math.sin(i), 90, c.gt * TAU * (0.8 + 0.1 * i), c.gt + i)
    label(g, f"{n:,}", 960, 220, 140, PAL["yellow"], k=1.0)
    label(g, "TRIALS", 960, 330, 60, PAL["cream"], k=1.0)


def s_short_string(g, c):
    studio(g, c.gt)
    k = ease_out(seg(c.t, 0.2, 0.5))
    g.line([(560, 520), (560 + 520 * k, 520)], INK, 22); g.line([(560, 520), (560 + 520 * k, 520)], "#FF6B5B", 12)
    with g.at(560, 640, 0):
        g.rect(0, 0, 520, 60, "#FFC93C", INK, lw=6)
        for i in range(0, 47, 2):
            g.line([(i * 11.06, 0), (i * 11.06, 26 if i % 10 else 44)], INK, 4)
    label(g, "UNDER 46 cm", 960, 300, 90, PAL["cream"], k=pop(c.t, tw(c, "forty-six") - 0.1, 0.3))
    label(g, "0 KNOTS", 1400, 520, 90, PAL["mint"], k=pop(c.t, tw(c, "never") - 0.1, 0.3))


def s_half(g, c):
    """Longer strings: half the tumbles end in knots (pie chart + a complex knot)."""
    studio(g, c.gt, "#3E7CB1", "#10263B")
    k = ease_io(seg(c.t, tw(c, "half") - 0.4, 0.8))
    with g.at(560, 540, 0):
        g.circle(0, 0, 230, "#0B3F4C", INK, lw=10)
        if k > 0:
            pts = [(0, 0)] + [(230 * math.cos(-math.pi / 2 + a * math.pi * k / 30), 230 * math.sin(-math.pi / 2 + a * math.pi * k / 30)) for a in range(31)]
            g.poly(pts, "#FF6B5B", INK, lw=8)
        g.text("≈50%", 0, 330, 80, PAL["yellow"], sw=14)
    earbuds(g, 1350, 520, 1.3, 1.0 * on(c, "complicated", 0.6), seed=7, col="#FF6B5B")
    if c.t > tw(c, "seconds") - 0.2:
        tag(g, "WITHIN SECONDS", 1350, 900, k=pop(c.t, tw(c, "seconds") - 0.1, 0.3))


def s_wander(g, c):
    """Over-and-under: a free end wanders through a coil; every crossing flashes."""
    studio(g, c.gt, "#2F3E46", "#1E2A30")
    for r in (140, 200, 260):
        g.ellipse(960, 560, r * 1.6, r, None, INK, lw=22)
        g.ellipse(960, 560, r * 1.6, r, None, "#F4F1EA", lw=12)
    k = clamp(c.t / max(1.0, c.T - 0.5))
    n = int(4 + 60 * k)
    pts = [(260 + i * 22, 560 + 260 * math.sin(i * 0.33)) for i in range(n)]
    g.line(pts, INK, 22); g.line(pts, "#FF6B5B", 12)
    for i in range(1, n, 9):
        g.circle(pts[i][0], pts[i][1], 24, None, PAL["yellow"], lw=7, a=0.8)
    g.circle(pts[-1][0], pts[-1][1], 16, "#9AA3AD", INK, lw=5)
    label(g, "OVER · UNDER", 960, 170, 84, PAL["yellow"], k=pop(c.t, tw(c, "over") - 0.1, 0.3))
    if c.t > tw(c, "crossing") - 0.2:
        label(g, "= A KNOT CHANCE", 960, 960, 70, PAL["cream"], k=pop(c.t, tw(c, "crossing") - 0.1, 0.3))


def s_floppy(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    earbuds(g, 620, 540, 1.1, 0.4, seed=2)
    earbuds(g, 1300, 540, 1.6, 1.0, seed=9, col="#FFC93C")
    label(g, "85%", 1300, 220, 150, PAL["cream"], k=pop(c.t, tw(c, "eighty-five") - 0.1, 0.3))
    label(g, "LONGER + FLOPPIER", 960, 960, 74, PAL["yellow"], k=pop(c.t, tw(c, "floppier") - 0.1, 0.3))


def s_pocket_end(g, c):
    pocket(g, c.gt)
    earbuds(g, 960, 560, 1.4, 0.5 + 0.5 * ease_io(seg(c.t, 0.2, c.T - 0.5)), seed=5)
    char2(g, "modern", 1650, 1080 + 30, 820, "bored", "hip", "down", t=c.gt, prop=False, flip=True)


# ch4 spaghetti
def pasta_kitchen(g, t):
    kitchen_am(g, t, 0.6)
    g.rect(1380, 520, 300, 200, "#9AA3AD", INK, lw=8, r=12)       # pot on the counter
    steam(g, t, 1530, 500, 3, 160)


def s_snap_try(g, c):
    banner(g, c, "WHY SPAGHETTI BREAKS IN 3")
    pasta_kitchen(g, c.gt)
    b = 160 * ease_io(seg(c.t, 0.4, max(1.0, c.T - 0.8)))
    spaghetti(g, 560, 560, 1240, 560, b, w=16)
    fist(g, 560, 590, 1.1); fist(g, 1240, 590, 1.1)
    label(g, "JUST 2 PIECES", 900, 230, 84, PAL["navy"], k=pop(c.t, tw(c, "two") - 0.1, 0.3))


def s_three(g, c):
    pasta_kitchen(g, c.gt)
    tb = tw(c, "three") - 0.6
    k = seg(c.t, tb, 0.6)
    if k <= 0:
        spaghetti(g, 560, 560, 1240, 560, 160, w=16)
    else:
        e = ease_out(k)
        spaghetti(g, 560, 560, 800, 500 - 80 * e, 0, w=16)
        with g.at(900, 420 - 260 * e, 3 * e):
            spaghetti(g, -90, 0, 90, 0, 0, w=16)
        spaghetti(g, 1000, 500 - 80 * e, 1240, 560, 0, w=16)
        burst(g, 900, 480, 40, 140, 10, PAL["cream"], 8, k=k)
    fist(g, 560, 590, 1.1); fist(g, 1240, 590, 1.1)
    for i in range(3):
        g.circle(700 + i * 260, 860, 46, PAL["yellow"], INK, lw=7, a=1 if k > 0.3 else 0)
        if k > 0.3: g.text(str(i + 1), 700 + i * 260, 864, 52, INK, stroke=None)
    label(g, "3 OR MORE!", 960, 200, 96, "#FF6B5B", k=pop(c.t, tw(c, "more") - 0.1, 0.3))


def s_feynman(g, c):
    """An evening at a kitchen table with a pile of broken pasta (the physicist is only named, never drawn as himself)."""
    night_kitchen(g, c.gt)
    for i in range(26):
        a = i * 2.4
        x = 900 + 300 * math.cos(a) * ((i % 5) / 5 + 0.4)
        y = 700 - 10 - (i % 4) * 8
        spaghetti(g, x - 50, y, x + 50, y - 10 * math.sin(a), 0, w=9)
    b = 120 * abs(math.sin(c.gt * 1.5))
    spaghetti(g, 760, 520, 1060, 520, b, w=12)
    fist(g, 760, 545, 0.8); fist(g, 1060, 545, 0.8)
    label(g, "RICHARD FEYNMAN", 960, 160, 72, PAL["cream"], k=pop(c.t, tw(c, "Feynman") - 0.1, 0.3))
    tag(g, "ONE WHOLE EVENING", 1500, 980, k=pop(c.t, tw(c, "evening") - 0.1, 0.3))


def s_french(g, c):
    lab(g, c.gt, "#3A3550", "#24203A")
    char2(g, "physicist", 620, 1080 + 30, 900, "smug", "point", "down", t=c.gt)
    char2(g, "doctor", 1000, 1080 + 30, 880, "smug", "up", "down", t=c.gt)
    spaghetti(g, 1250, 560, 1700, 560, 0, w=14)
    check(g, 1480, 400, 60, seg(c.t, tw(c, "cracked") - 0.1, 0.3))
    tag(g, "2005 · FRANCE", 1500, 140, k=pop(c.t, tw(c, "2005") - 0.1, 0.3))


def s_snapback(g, c, second=False):
    """Diagram: break at the middle, each half springs back and a bending wave runs down it."""
    studio(g, c.gt, "#1590A0", "#0B3F4C")
    t0 = tw(c, "snaps") - 0.2 if not second else -1.0
    k = seg(c.t, t0, 0.25)
    if k <= 0 and not second:
        spaghetti(g, 360, 560, 1560, 560, 220, w=20)
        return
    for side in (-1, 1):
        x_in, x_out = 960 + side * 30, 960 + side * 600
        ph = (c.t - t0) * 2.2
        n = 24
        pts = []
        for i in range(n + 1):
            u = i / n                                  # 0 at the break, 1 at the clamp
            wave = 90 * math.exp(-((u - (ph % 1.3)) ** 2) / 0.01) * (1 if not second else 1.6)
            sag = 220 * 4 * (0.5 + u * 0.5) * (0.5 - u * 0.5) * (1 - ease_out(clamp(ph)))
            pts.append((lerp(x_in, x_out, u), 560 - sag * 0.3 - wave))
        g.line(pts, INK, 29); g.line(pts, PASTA, 20)
        if second and (c.t > tw(c, "again") - 0.3):
            kk = seg(c.t, tw(c, "again") - 0.3, 0.3)
            burst(g, 960 + side * 330, 500, 30, 120, 10, PAL["yellow"], 8, k=kk)
    burst(g, 960, 540, 30, 160, 12, PAL["cream"], 10, k=k)
    if not second:
        label(g, "SNAP-BACK WAVE", 960, 210, 84, PAL["yellow"], k=pop(c.t, tw(c, "wave") - 0.1, 0.3))
        arrow(g, 1100, 400, 1400, 400, PAL["cream"], 18, k=on(c, "wave"))
        arrow(g, 820, 400, 520, 400, PAL["cream"], 18, k=on(c, "wave"))
    else:
        label(g, "SNAP AGAIN!", 960, 210, 96, "#FF6B5B", k=pop(c.t, tw(c, "again") - 0.1, 0.3))


def bench(g, t):
    lab(g, t, "#2C3E50", "#1B2836")
    g.rect(260, 640, 1400, 50, "#9AA3AD", INK, lw=8, r=8)
    g.rect(320, 690, 50, 200, "#5A5A6A", INK, lw=7); g.rect(1550, 690, 50, 200, "#5A5A6A", INK, lw=7)


def s_mit(g, c):
    """Twist-then-bend machine: one clamp turns ~a full turn, then the clamps move together, the stick breaks in two."""
    bench(g, c.gt)
    tg = tw(c, "twist") - 0.2
    tb = tw(c, "bend") - 0.2
    kt = ease_io(seg(c.t, tg, max(0.8, tb - tg)))
    kb = ease_io(seg(c.t, tb, 1.0))
    gap = 900 - 260 * kb
    xa, xb = 960 - gap / 2, 960 + gap / 2
    spaghetti(g, xa, 500, xb, 500, 200 * kb, w=16, twist=kt)
    for x, rot in ((xa, 0), (xb, kt * TAU * 0.95)):
        g.rc(x, 560, 90, 120, "#3E7CB1", INK, lw=8, r=10)
        with g.at(x, 500, rot):
            g.rc(0, 0, 70, 70, "#C9CED6", INK, lw=7, r=8)
            g.line([(0, -26), (0, 26)], "#FF6B5B", 8)
    tag(g, "2018 · MIT", 1550, 140, k=pop(c.t, tw(c, "2018") - 0.1, 0.3))
    if kt > 0.05:
        label(g, f"{int(360 * 0.95 * kt)}°", xb + 120, 330, 80, PAL["yellow"], k=1.0)


def s_clean(g, c):
    bench(g, c.gt)
    k = seg(c.t, tw(c, "cleanly") - 0.5, 0.4)
    if k <= 0:
        spaghetti(g, 700, 500, 1220, 500, 200, w=16, twist=0.95)
    else:
        e = ease_out(k)
        spaghetti(g, 700, 500, 950, 400 - 20 * e, 0, w=16)
        spaghetti(g, 970, 400 - 20 * e, 1220, 500, 0, w=16)
        burst(g, 960, 400, 30, 120, 10, PAL["cream"], 8, k=k)
    for i in range(2):
        g.circle(820 + i * 280, 860, 46, PAL["mint"], INK, lw=7, a=1 if k > 0.5 else 0)
        if k > 0.5: g.text(str(i + 1), 820 + i * 280, 864, 52, INK, stroke=None)
    label(g, "CLEANLY IN TWO", 960, 210, 92, PAL["mint"], k=pop(c.t, tw(c, "two") - 0.1, 0.3))
    label(g, "TWIST SOAKS IT UP", 960, 1000, 54, PAL["cream"], k=pop(c.t, tw(c, "soaks") - 0.1, 0.3))


def s_dinner(g, c):
    pasta_kitchen(g, c.gt)
    char2(g, "modern", 960, 1080 + 40, 980, "bored" if c.t < tw(c, "luck") else "smug", "shrug", "shrug", t=c.gt, prop=False)
    for i in range(5):
        spaghetti(g, 300 + i * 60, 780 - (i % 2) * 20, 360 + i * 60, 770, 0, w=9)
    label(g, "GOOD LUCK!", 1450, 300, 90, PAL["coral"], k=pop(c.t, tw(c, "luck") - 0.1, 0.3))


# ch5 shower curtain
TUB_Y = 820


def tub(g, t):
    g.rect(300, TUB_Y, 1320, 200, "#FFFFFF", INK, lw=10, r=40)
    g.rect(330, TUB_Y + 30, 1260, 30, "#E6F0F2", None, r=10)
    g.line([(1450, 200), (1450, 140), (1350, 140)], "#9AA3AD", 14)
    g.path("M1310 140 L1390 140 L1370 180 L1330 180 Z", "#C9CED6", INK, lw=6)


def drops(g, t, x, y, n=18, col="#7FC8E8", spread=220, h=600):
    for i in range(n):
        ph = (t * 1.6 + i * 0.137) % 1
        xx = x + (i % 7 - 3) * spread / 7 * (0.3 + ph)
        yy = y + ph * h
        g.line([(xx, yy), (xx - 4, yy + 26)], col, 6, a=0.8)


def bath_cut(g, c, bulge, cold=False, weights=False, vortex=0.0, person=True):
    """Cut-away from the front: shower spray on the right, the curtain on the left side of the tub, bulging inward (to the right)."""
    bathroom(g, c.gt)
    tub(g, c.gt)
    if person:
        char2(g, "modern", 1200, TUB_Y + 40, 700, "shocked" if bulge > 0.5 else "deadpan", "down", "down", t=c.gt, prop=False, flip=True)
    drops(g, c.gt, 1350, 190, 18, "#BDEBFF" if cold else "#7FC8E8", 200, 620)
    if cold:
        flake(g, 1560, 300, 40, "#BDEBFF", c.gt)
    if vortex > 0:
        with g.group(vortex):
            for i in range(3):
                a0 = c.gt * 3 + i * TAU / 3
                pts = [(1060 + (60 + 20 * j) * math.cos(a0 + j * 0.35), 520 + (60 + 20 * j) * 0.8 * math.sin(a0 + j * 0.35)) for j in range(16)]
                g.line(pts, "#FFFFFF", 10, a=0.9)
                g.line(pts, "#3E7CB1", 5)
            g.circle(1060, 520, 46, "#FF6B5B", INK, lw=6)
            g.text("LOW", 1060, 524, 30, "#FFFFFF", stroke=None)
    # curtain seen edge-on: a vertical sheet hanging at x≈760 that bows to the right
    n = 20
    pts = []
    for i in range(n + 1):
        v = i / n
        x = 900 + bulge * 200 * math.sin(math.pi * min(1, v * 1.1)) * v + 6 * math.sin(c.gt * 2 + v * 6)
        pts.append((x, 150 + v * (TUB_Y + 20 - 150)))
    g.line([(700, 140), (1500, 140)], "#C9CED6", 14)
    left = [(x - 110, y) for x, y in pts]
    g.poly(left + pts[::-1], "#5ED3B5", INK, lw=8)                     # the curtain sheet (seen from the side, with depth)
    for j in range(1, 4):
        g.line([(x - 110 + j * 27, y) for x, y in pts], shade("#5ED3B5", 0.8), 5)
    for j in range(6):
        g.circle(800 + j * 18, 140, 10, None, "#9AA3AD", lw=5)
    if weights:
        g.circle(pts[-1][0], pts[-1][1], 22, "#5A5A6A", INK, lw=6)


def s_old_theories(g, c):
    banner(g, c, "WHY THE SHOWER CURTAIN BLOWS IN")
    bath_cut(g, c, 0.5)
    k1, k2 = on(c, "hot"), on(c, "fast-moving")
    if k1 > 0:
        for i in range(3):
            arrow(g, 1300 + i * 70, 700 - 200 * k1, 1300 + i * 70, 500 - 200 * k1, "#FF8A3D", 16, k=k1)
        label(g, "HOT AIR?", 1450, 260, 70, "#FF8A3D", k=pop(c.t, tw(c, "hot") - 0.1, 0.3))
    if k2 > 0:
        label(g, "FAST WATER?", 1450, 380, 70, "#7FC8E8", k=pop(c.t, tw(c, "fast-moving") - 0.1, 0.3))


def s_cold(g, c):
    bath_cut(g, c, 0.2 + 0.6 * ease_io(seg(c.t, tw(c, "cold") - 0.3, 1.0)), cold=True)
    cross(g, 1500, 260, 50, seg(c.t, tw(c, "cold") - 0.1, 0.3))
    label(g, "COLD WATER TOO", 1350, 400, 70, "#BDEBFF", k=pop(c.t, tw(c, "cold") - 0.1, 0.3))


def s_cells(g, c):
    """A virtual bathroom split into a grid of cells; counter to 50,000; a home computer runs for two weeks."""
    studio(g, c.gt, "#24414A", "#16282E")
    k = ease_io(seg(c.t, tw(c, "fifty") - 0.8, 1.4))
    with g.at(560, 560, 0):
        g.rc(0, 0, 640, 640, "#0B3F4C", PAL["cream"], lw=8, r=16)
        n = int(4 + 36 * k)
        for i in range(1, n):
            p = -320 + 640 * i / n
            g.line([(p, -320), (p, 320)], "#5ED3B5", 2, a=0.5)
            g.line([(-320, p), (320, p)], "#5ED3B5", 2, a=0.5)
        g.line([(-100, -320), (-100 + 40 * math.sin(c.gt), 300)], PAL["cream"], 12)
    label(g, f"{int(50000 * k):,} CELLS", 560, 970, 64, PAL["yellow"], k=1.0 if k > 0 else 0)
    kc = seg(c.t, tw(c, "computer") - 0.3, 0.4)
    if kc > 0:
        with g.at(1400, 520, 0, back_out(clamp(kc), 1.5)):
            g.rc(0, 0, 520, 360, "#22181B", INK, lw=10, r=16)
            g.rc(0, 0, 480, 320, "#3E7CB1", None, r=8)
            g.rc(0, -40, 280, 160, "#FFFDF6", INK, lw=6, r=8)
            days = int(14 * ease_in(seg(c.t, tw(c, "weeks") - 1.0, 1.4)))
            g.text(f"DAY {max(1, days)}", 0, -40, 64, "#FF6B5B", stroke=None)
            g.rect(-40, 180, 80, 70, "#5A5A6A", INK, lw=6); g.rc(0, 260, 260, 30, "#5A5A6A", INK, lw=6, r=8)
    tag(g, "2001 · ENGINEER DAVID SCHMIDT", 1360, 120, k=pop(c.t, tw(c, "2001") - 0.1, 0.3), size=40)


def s_30s(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    with g.at(960, 520, 0):
        g.circle(0, 0, 220, "#F4F1EA", INK, lw=12)
        a = TAU * 0.5 * ease_io(seg(c.t, 0.2, c.T - 0.6))
        g.poly([(0, 0)] + [(200 * math.sin(a * j / 30), -200 * math.cos(a * j / 30)) for j in range(31)], "#7FC8E8", None, a=0.8)
        g.line([(0, 0), (190 * math.sin(a), -190 * math.cos(a))], INK, 12)
    label(g, "30 SECONDS", 960, 900, 100, PAL["yellow"], k=pop(c.t, tw(c, "thirty") - 0.1, 0.3))
    label(g, "2 WEEKS →", 380, 200, 60, PAL["cream"], k=pop(c.t, 0.1, 0.3))


def s_vortex(g, c, low=False):
    bath_cut(g, c, 0.25 + (0.55 * on(c, "pulls", 0.8) if low else 0.15), vortex=on(c, "vortex" if not low else "middle", 0.5, frac=0.1))
    if not low:
        label(g, "SIDEWAYS WHIRLWIND", 1400, 240, 64, PAL["navy"], k=pop(c.t, tw(c, "whirlwind") - 0.1, 0.3))
    else:
        label(g, "LOW PRESSURE PULLS", 1400, 240, 64, "#FF6B5B", k=pop(c.t, tw(c, "low") - 0.1, 0.3))
        arrow(g, 1150, 520, 900, 520, "#FF6B5B", 20, k=on(c, "pulls"))


def s_fix(g, c):
    ignobel = c.t > tw(c, "Ig") - 0.2
    if not ignobel:
        bath_cut(g, c, 0.0, weights=True)
        label(g, "WEIGHTS IN THE HEM", 1350, 260, 70, PAL["navy"], k=pop(c.t, tw(c, "Weights") - 0.1, 0.3))
        check(g, 860, 960, 46, seg(c.t, tw(c, "hem") - 0.1, 0.3))
    else:
        studio(g, c.gt, "#FFC93C", "#C97B2A")
        trophy(g, 960, 640, 2.0, seg(c.t, tw(c, "Ig") - 0.2, 0.4))
        label(g, "ANOTHER IG NOBEL", 960, 180, 90, PAL["cream"], k=pop(c.t, tw(c, "Ig") - 0.1, 0.3))
        curtain(g, 1350, 1600, 420, 820, 0.2, t=c.gt)


# ch6 coffee
def s_spill(g, c):
    banner(g, c, "WHY COFFEE STAINS ARE RINGS")
    cafe(g, c.gt)
    mug(g, 520, 420, 1.3)
    k = ease_out(seg(c.t, 0.2, 0.5))
    dry = ease_io(seg(c.t, tw(c, "dry") - 0.2, 2.2))
    coffee_drop(g, 1150, 600, 40 + 210 * k, dry, dry)
    if c.t > tw(c, "ring") - 0.2:
        g.circle(1150, 600, 290, None, PAL["yellow"], lw=8, a=0.8)
        label(g, "A RING?", 1150, 230, 90, PAL["cream"], k=pop(c.t, tw(c, "ring") - 0.1, 0.3))
    if c.t > tw(c, "edge") - 0.2:
        arrow(g, 1550, 400, 1380, 520, "#FF6B5B", 18, k=on(c, "edge"))


def s_chicago(g, c):
    lab(g, c.gt, "#3A3550", "#24203A")
    char2(g, "doctor", 560, 1080 + 30, 900, "smug", "point", "down", t=c.gt)
    with g.at(1250, 520, -0.04):
        g.rc(0, 0, 560, 400, "#FFFDF6", INK, lw=8, r=10)
        g.rect(-280, -200, 560, 70, "#FF6B5B", INK, lw=0, r=10)
        g.text("JOURNAL · 1997", 0, -164, 44, "#FFFFFF", stroke=None)
        coffee_drop(g, -120, 50, 90, 1.0, 1.0)
        for i in range(4):
            g.line([(20, -40 + i * 50), (230, -40 + i * 50)], "#9AA3AD", 8)
    tag(g, "1997 · CHICAGO", 1500, 140, k=pop(c.t, tw(c, "1997") - 0.1, 0.3))


def drop_cut(g, c, flow=0.0, evap=0.0, pinned=0.0, deposit=0.0, ell=False, x0=960, w=1300, h=300, seed=1, n=40):
    """Cross-section of a drying drop on a table: dome, pinned edges, evaporation arrows, outward flow of particles."""
    y0 = 760
    g.rect(-100, y0, W + 200, 400, "#B57F4C", INK, lw=8)
    pts = [(x0 - w / 2 + w * i / 40, y0 - h * (1 - deposit * 0.6) * math.sin(math.pi * i / 40)) for i in range(41)]
    g.poly(pts + [(x0 + w / 2, y0), (x0 - w / 2, y0)], "#C08A5A", INK, lw=7, a=0.9)
    R = rnd(seed)
    for i in range(n):
        u0 = (i * 0.618) % 1
        drift = clamp(flow * (0.4 + 0.6 * ((i * 0.37) % 1)))
        side = -1 if u0 < 0.5 else 1
        u = lerp(u0, 0.02 if side < 0 else 0.98, drift) if not ell else lerp(u0, 0.5 + (u0 - 0.5) * 1.15, drift * 0.3)
        hh = h * math.sin(math.pi * u) * (1 - deposit * 0.6)
        y = y0 - 18 - ((i * 0.53) % 1) * max(10, hh - 40)
        x = x0 - w / 2 + w * u
        if ell:
            g.ellipse(x, y, 22, 10, COFFEE_D, INK, lw=3, rot=i)
        else:
            g.circle(x, y, 11, COFFEE_D, INK, lw=3)
    if pinned > 0:
        for side in (-1, 1):
            g.circle(x0 + side * w / 2, y0, 26, "#FF6B5B", INK, lw=6, a=pinned)
    if evap > 0:
        for i in range(9):
            u = (i + 0.5) / 9
            ln = 60 + 120 * (abs(u - 0.5) * 2) ** 2
            x = x0 - w / 2 + w * u
            y = y0 - h * math.sin(math.pi * u) - 20
            arrow(g, x, y, x, y - ln * evap, "#BDEBFF", 12, k=evap)
    if flow > 0 and not ell:
        for side in (-1, 1):
            arrow(g, x0 + side * 80, y0 - 60, x0 + side * (w / 2 - 120), y0 - 60, PAL["yellow"], 16, k=min(1, flow * 2))


def s_stuck(g, c):
    studio(g, c.gt, "#2F3E46", "#1E2A30")
    drop_cut(g, c, pinned=on(c, "stuck"))
    label(g, "EDGE STUCK", 960, 200, 90, "#FF6B5B", k=pop(c.t, tw(c, "stuck") - 0.1, 0.3))


def s_flow(g, c):
    studio(g, c.gt, "#2F3E46", "#1E2A30")
    drop_cut(g, c, pinned=1.0, evap=on(c, "fastest", 0.6), flow=ease_io(seg(c.t, tw(c, "flows") - 0.3, 2.0)))
    label(g, "EDGE DRIES FASTEST", 960, 200, 80, "#BDEBFF", k=pop(c.t, tw(c, "fastest") - 0.1, 0.3))


def s_dump(g, c):
    studio(g, c.gt, "#2F3E46", "#1E2A30")
    f = ease_io(seg(c.t, 0.0, max(1.0, tw(c, "rim") - 0.2)))
    drop_cut(g, c, pinned=1.0, flow=0.5 + 0.5 * f, deposit=f)
    if c.t > tw(c, "rim") - 0.2:
        for side in (-1, 1):
            g.circle(960 + side * 650, 740, 70, None, PAL["yellow"], lw=8)
        label(g, "ALL AT THE RIM", 960, 200, 90, PAL["yellow"], k=pop(c.t, tw(c, "rim") - 0.1, 0.3))


def s_shape(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    tag(g, "2011 · PENNSYLVANIA", 1500, 140, k=pop(c.t, tw(c, "2011") - 0.1, 0.3))
    k = on(c, "shape", 0.4)
    for i in range(12):
        x = 400 + (i % 6) * 90; y = 460 + (i // 6) * 110
        g.circle(x, y, 30, COFFEE_D, INK, lw=4)
    arrow(g, 960, 520, 1180, 520, PAL["yellow"], 22, k=k)
    for i in range(12):
        x = 1300 + (i % 6) * 90; y = 460 + (i // 6) * 110
        g.ellipse(x, y, 30 + 22 * k, 30 - 12 * k, COFFEE_D, INK, lw=4, rot=0.4 * math.sin(i))
    label(g, "CHANGE THE SHAPE", 960, 860, 84, PAL["cream"], k=pop(c.t, tw(c, "shape") - 0.1, 0.3))


def s_noring(g, c):
    cafe(g, c.gt)
    coffee_drop(g, 600, 560, 260, 1.0, 1.0)
    coffee_drop(g, 1320, 560, 260, ease_io(seg(c.t, 0.3, c.T - 0.8)), even=True)
    label(g, "SPHERES", 600, 920, 64, PAL["cream"], k=1.0)
    label(g, "EGG-SHAPED", 1320, 920, 64, PAL["yellow"], k=1.0)
    label(g, "NO RING!", 1320, 210, 96, PAL["mint"], k=pop(c.t, tw(c, "ring") - 0.1, 0.3))
    check(g, 1580, 340, 50, seg(c.t, tw(c, "ring") - 0.1, 0.3))


def s_printer(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    g.rc(960, 420, 1100, 160, "#4A4A55", INK, lw=10, r=24)
    hx = 520 + (c.gt * 300) % 880
    g.rc(hx, 520, 120, 90, "#22181B", INK, lw=7, r=12)
    g.rect(400, 600, 1120, 380, "#FFFDF6", INK, lw=8)
    for i in range(int((c.gt * 300) % 880 / 70)):
        coffee_drop(g, 520 + i * 70, 700, 26, 0.9, 1.0 if c.t < tw(c, "ring") else 1.0)
    for i in range(int((c.gt * 300) % 880 / 70)):
        coffee_drop(g, 520 + i * 70, 860, 26, 0.9, even=True)
    cross(g, 1600, 700, 40, seg(c.t, tw(c, "ring") - 0.1, 0.3))
    check(g, 1600, 860, 40, seg(c.t, tw(c, "ink") - 0.1, 0.3))


# ch7 cereal
LOOPS = [(-210, -120), (180, -160), (-60, 150), (230, 120), (40, -20), (-260, 90), (120, 230), (-140, -230)]


def s_bowl_q(g, c):
    banner(g, c, "WHY CEREAL CLUMPS")
    breakfast(g, c.gt)
    bowl_top(g, 960, 560, 400)
    k = ease_io(seg(c.t, tw(c, "clump") - 0.6, 1.6))
    kw = ease_io(seg(c.t, tw(c, "cling") - 0.6, 1.2))
    for i, (x, y) in enumerate(LOOPS):
        if i < 5:
            tx, ty = lerp(x, -20 + 46 * math.cos(i * 1.25), k), lerp(y, 10 + 46 * math.sin(i * 1.25), k)
        else:
            a = math.atan2(y, x)
            tx, ty = lerp(x, 352 * math.cos(a), kw), lerp(y, 352 * math.sin(a), kw)
        cereal_loop(g, 960 + tx, 560 + ty, 46, i + c.gt * 0.1)
    g.path("M1500 820 L1900 760 L1900 860 L1500 860 Z", "#C9CED6", INK, lw=8)        # spoon
    g.ellipse(1440, 820, 90, 50, "#C9CED6", INK, lw=8)


def s_mathematicians(g, c):
    lab(g, c.gt, "#3A3550", "#24203A")
    char2(g, "prof", 560, 1080 + 30, 900, "curious", "think", "down", t=c.gt)
    char2(g, "physicist", 1000, 1080 + 30, 900, "smug", "point", "down", t=c.gt)
    with g.at(1450, 520, 0.03):
        g.rc(0, 0, 420, 300, "#FFFDF6", INK, lw=8, r=10)
        g.path("M-170 40 Q-100 40 -60 -10 Q-30 40 0 40 Q30 40 60 -10 Q100 40 170 40", None, "#3E7CB1", lw=8)
        cereal_loop(g, -60, -20, 26); cereal_loop(g, 60, -20, 26)
    tag(g, "2005 · PHYSICS JOURNAL", 1460, 140, k=pop(c.t, tw(c, "2005") - 0.1, 0.3))


def milk_side(g, c, pull=0.0, wall=False):
    """Side cut-away of milk: the surface curves up around each floating loop; loops slide toward each other."""
    studio(g, c.gt, "#C97B2A", "#6E3B1E")
    y0 = 560
    d = lerp(640, 300, pull)
    xs = (960 - d / 2, 960 + d / 2) if not wall else (960, 1500 + 120 * pull)
    pts = []
    for i in range(97):
        x = i * 20
        y = y0
        for k_, xc in enumerate(xs):
            if wall and k_ == 1:
                y -= 110 * math.exp(-max(0, 1700 - x) / 140) if x < 1700 else 110
            else:
                y -= 70 * math.exp(-abs(x - xc) / 120)
        pts.append((x, y))
    g.poly(pts + [(W, H), (0, H)], "#FFF4DE", INK, lw=8)
    if wall:
        g.rect(1700, 200, 260, 900, "#3E8E7A", INK, lw=10)
    for k_, xc in enumerate(xs):
        if wall and k_ == 1:
            continue
        with g.at(xc, y0 - 72, 0):
            g.rc(0, 0, 200, 70, "#E8A94A", INK, lw=7, r=32)
            g.rc(0, 0, 50, 70, "#FFF4DE", INK, lw=5, r=12)
    if wall:
        x = lerp(960, 1610, pull)
        y = y0 - 72 - 110 * clamp((x - 1200) / 500) ** 2
        with g.at(x, y, -0.2 * pull):
            g.rc(0, 0, 150, 56, "#E8A94A", INK, lw=7, r=26)
            g.rc(0, 0, 40, 56, "#FFFDF6", INK, lw=5, r=10)


def s_slope(g, c):
    milk_side(g, c, 0.0)
    if c.t > tw(c, "slope") - 0.3:
        arrow(g, 480, 360, 560, 440, PAL["yellow"], 14, k=on(c, "slope"))
        label(g, "TINY SLOPE", 960, 200, 90, PAL["navy"], k=pop(c.t, tw(c, "slope") - 0.1, 0.3))
    label(g, "MILK ISN'T FLAT", 960, 920, 70, PAL["cream"], k=pop(c.t, tw(c, "flat") - 0.1, 0.3))


def s_drift(g, c):
    p = ease_io(seg(c.t, tw(c, "drifts") - 0.2, max(1.0, c.T - 1.0)))
    milk_side(g, c, p)
    if p > 0.95:
        label(g, "CLUMP!", 960, 220, 100, "#FF6B5B", k=pop(c.t, c.T - 0.9, 0.3))


def s_wall(g, c):
    milk_side(g, c, ease_io(seg(c.t, tw(c, "slide") - 0.3, 1.6)), wall=True)
    label(g, "BOWL EDGE", 1830, 160, 60, PAL["cream"], k=pop(c.t, tw(c, "edge") - 0.1, 0.3))


def s_assembly(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    k = ease_io(seg(c.t, 0.4, c.T - 0.8))
    for i in range(19):
        q = [(0, 0), (1, 0), (-1, 0), (0.5, 0.87), (-0.5, 0.87), (0.5, -0.87), (-0.5, -0.87),
             (2, 0), (-2, 0), (1.5, 0.87), (-1.5, 0.87), (1.5, -0.87), (-1.5, -0.87), (1, 1.73), (-1, 1.73), (0, 1.73), (1, -1.73), (-1, -1.73), (0, -1.73)][i]
        ex, ey = 960 + q[0] * 96, 540 + q[1] * 96
        sx, sy = 960 + 700 * math.cos(i * 2.1), 540 + 420 * math.sin(i * 1.7)
        with g.at(lerp(sx, ex, k), lerp(sy, ey, k), (1 - k) * i):
            g.poly([(46 * math.cos(a * TAU / 6 + math.pi / 6), 46 * math.sin(a * TAU / 6 + math.pi / 6)) for a in range(6)],
                   ("#5ED3B5", "#FFC93C", "#FF6B5B")[i % 3], INK, lw=5)
    label(g, "PARTS THAT BUILD THEMSELVES", 960, 960, 66, PAL["cream"], k=pop(c.t, tw(c, "themselves") - 0.1, 0.3))


# ch8 ending
def s_recap(g, c, items):
    studio(g, c.gt)
    for wd, x, y, fn in items:
        k = back_out(seg(c.t, tw(c, wd) - 0.2, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, y, 0.05 * math.sin(c.gt * 2 + x), k * 0.8):
            fn(g, c)


R1 = [("Toast", 360, 560, ic_toast), ("laces", 960, 560, ic_lace), ("earbuds", 1560, 560, ic_buds)]
R2 = [("Spaghetti", 300, 560, ic_pasta), ("curtain", 740, 560, ic_curtain), ("coffee", 1180, 560, ic_coffee), ("cereal", 1620, 560, ic_cereal)]


def s_measure(g, c):
    lab(g, c.gt)
    char2(g, "physicist", 760, 1080 + 30, 980, "smug", "hold", "explain", t=c.gt)
    with g.at(1350, 560, -0.1):
        g.rect(-260, -40, 520, 80, "#FFC93C", INK, lw=8)
        for i in range(27):
            g.line([(-250 + i * 19, -40), (-250 + i * 19, -40 + (36 if i % 5 == 0 else 18))], INK, 4)
    label(g, "STOP AND MEASURE", 1350, 260, 84, PAL["yellow"], k=pop(c.t, tw(c, "measure") - 0.1, 0.3))


def s_comments(g, c):
    kitchen_am(g, c.gt)
    table_side(g, 820, TBL_Y, 560, "#C97B4A", FL - TBL_Y - 36)
    plate(g, 820, TBL_Y - 6, 280)
    toast(g, 820, TBL_Y - 30, 1.1, 0.0)
    char2(g, "modern", 1400, 1080 + 40, 980, "curious", "hip", "point", t=c.gt, prop=False, flip=True)
    for i, (x, y) in enumerate(((400, 300), (1100, 260), (600, 200))):
        qmark(g, x, y, 110, PAL["coral"], 0.2 * math.sin(i + c.gt), pop(c.t, 0.2 + i * 0.25, 0.3))
    label(g, "WHICH ONE FIRST?", 820, 140, 84, PAL["navy"], k=pop(c.t, tw(c, "test") - 0.1, 0.3))


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
    if lid in V.T:                       # lines without a voice take yet (quota) are skipped in previews
        V.shot(lid, fn, part=part, **kw)


Z = lambda z0, z1, f: push(z0, z1, f)
MON_A = [("toast", 360, ic_toast), ("shoelaces", 760, ic_lace), ("earbuds", 1160, ic_buds), ("spaghetti", 1560, ic_pasta)]

# cold open
P("O01", s_hook, (0, "And"), cam=Z(1.08, 1.14, (800, 580)), tr="cut", music="playful", sfx=[(0.0, "whoosh", 0.45), (0.95, "thud", 0.5)])
P("O01", s_landed, ("And", 1), cam=Z(1.1, 1.18, (1000, 600)), sfx=[("luck", "sting", 0.35)])
P("O02", s_culprit, cam=Z(1.0, 1.06, (1050, 560)), sfx=[("culprit", "drum_hit", 0.4)])
P("O03", lambda g, c: s_montage(g, c, MON_A), sfx=[("shoelaces", "pop", 0.4), ("earbuds", "pop", 0.4), ("spaghetti", "pop", 0.4)])
P("O04", s_tests, cam=Z(1.0, 1.05, (960, 560)), sfx=[("treadmills", "pop", 0.35), ("spinning", "pop", 0.35), ("computer", "pop", 0.35)])
P("O05", s_start, cam=Z(1.05, 1.15, (820, 560)), music="curious", sfx=[(0.1, "shimmer", 0.35)])
V.pause["O05"] = CH_PAUSE
# toast
P("T01", s_push, tr="flash", sfx=[(0.2, "whoosh_soft", 0.35)])
P("T02", s_tip, cam=Z(1.1, 1.2, (1100, 520)), music="story", sfx=[("spin", "whoosh", 0.35)])
P("T03", s_matthews, cam=Z(1.0, 1.05, (1000, 560)))
P("T04", s_halfturn, (0, "the#1"), cam=Z(1.25, 1.3, (700, 560)))
P("T04", s_halfturn, ("the#1", 1), cam=Z(1.0, 1.04, (960, 560)), sfx=[("half", "ding", 0.4)])
P("T05", s_flipped, cam=Z(1.0, 1.05, (960, 560)), sfx=[("bottom", "thud", 0.4)])
P("T06", s_tall_table, cam=Z(1.0, 1.03, (960, 560)), music="playful", sfx=[("taller", "boing", 0.35), ("full", "chime", 0.35)])
P("T07", s_fast, cam=Z(1.0, 1.04, (1100, 600)), sfx=[("fast", "whoosh", 0.45)])
P("T08", s_ignobel, cam=Z(1.0, 1.05, (960, 560)), music="warm", sfx=[("Ig", "chime", 0.45), ("laugh", "pop", 0.35)])
V.pause["T08"] = CH_PAUSE
# shoelaces
P("S01", s_lace_q, tr="flash", music="curious", sfx=[(0.2, "whoosh", 0.4)])
P("S02", s_treadmill, (0, "filmed"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("S02", s_treadmill, ("filmed", 1), cam=Z(1.35, 1.45, (1200, 560)), sfx=[("slow", "click", 0.4)])
P("S03", s_stomp, sfx=[("seven", "drum_hit", 0.5)])
P("S04", s_squeeze, cam=Z(1.0, 1.06, (960, 520)), sfx=[(0.3, "thud", 0.25), (0.9, "thud", 0.25)])
P("S05", s_whip, cam=Z(1.0, 1.04, (960, 500)), sfx=[("whips", "whoosh", 0.4), ("tug", "pop", 0.35)])
P("S06", s_neither, music="tension", sfx=[("Stomping", "pop", 0.35), ("Swinging", "pop", 0.35), ("together", "sting", 0.45)])
P("S07", s_fail, cam=Z(1.0, 1.06, (1000, 540)), sfx=[("fell", "rush", 0.4)])
P("S08", s_knots, (0, "A#1"), music="curious", sfx=[("weak", "bloop", 0.35)])
P("S08", s_knots, ("A#1", 1), cam=Z(1.2, 1.25, (1300, 540)), sfx=[("flat", "ding", 0.4)])
P("S09", s_strong_fails, cam=Z(1.0, 1.05, (960, 520)), sfx=[("fails", "bloop", 0.35)])
V.pause["S09"] = CH_PAUSE
# earbuds
P("E01", s_buds_q, (0, "You#1"), tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4)])
P("E01", s_buds_q, ("You#1", 1), cam=Z(1.0, 1.06, (960, 500)), sfx=[("How", "sting", 0.4)])
P("E02", s_box_lab, cam=Z(1.0, 1.04, (1000, 540)), music="story", sfx=[("spun", "whoosh_soft", 0.35)])
P("E03", s_again, sfx=[("again", "pop", 0.35), ("thousand", "ding", 0.4)])
P("E04", s_short_string, cam=Z(1.0, 1.04, (960, 520)), sfx=[("never", "ding", 0.4)])
P("E05", s_half, cam=Z(1.0, 1.04, (960, 540)), sfx=[("half", "pop", 0.35)])
P("E06", s_wander, (0, "Every"), music="curious")
P("E06", s_wander, ("Every", 1), cam=Z(1.2, 1.28, (1100, 560)), sfx=[("crossing", "ding", 0.35)])
P("E07", s_floppy, cam=Z(1.0, 1.05, (1100, 520)), sfx=[("eighty-five", "sting", 0.4)])
P("E08", s_pocket_end, cam=Z(1.0, 1.08, (960, 540)))
V.pause["E08"] = CH_PAUSE
# spaghetti
P("P01", s_snap_try, tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4), (0.8, "creak", 0.3)])
P("P02", s_three, cam=Z(1.0, 1.04, (960, 540)), sfx=[("three", "click", 0.5)])
P("P03", s_feynman, (0, "breaking"), cam=Z(1.0, 1.05, (960, 500)), music="story")
P("P03", s_feynman, ("breaking", 1), cam=Z(1.3, 1.35, (900, 560)), sfx=[("breaking", "click", 0.35)])
P("P04", s_french, cam=Z(1.0, 1.04, (1100, 560)), sfx=[("cracked", "chime", 0.4)])
P("P05", lambda g, c: s_snapback(g, c), (0, "that"), cam=Z(1.0, 1.03, (960, 560)), music="curious", sfx=[("snaps", "click", 0.5)])
P("P05", lambda g, c: s_snapback(g, c), ("that", 1), cam=Z(1.15, 1.2, (960, 520)))
P("P06", lambda g, c: s_snapback(g, c, True), cam=Z(1.0, 1.05, (960, 520)), music="tension", sfx=[("again", "click", 0.5)])
P("P07", s_mit, (0, "twist"), cam=Z(1.0, 1.04, (960, 520)), music="story")
P("P07", s_mit, ("twist", 1), cam=Z(1.2, 1.25, (1100, 480)), sfx=[("bend", "creak", 0.35)])
P("P08", s_clean, cam=Z(1.0, 1.05, (960, 500)), music="warm", sfx=[("cleanly", "click", 0.5), ("two", "chime", 0.4)])
P("P09", s_dinner, cam=Z(1.0, 1.06, (960, 520)), sfx=[("luck", "pop", 0.35)])
V.pause["P09"] = CH_PAUSE
# shower curtain
P("C01", lambda g, c: bath_cut(g, c, ease_io(seg(c.t, tw(c, "creeps") - 0.3, 1.4))) or banner(g, c, "WHY THE SHOWER CURTAIN BLOWS IN") or
  label(g, "WHY?!", 1500, 260, 96, "#FF6B5B", k=pop(c.t, tw(c, "Why") - 0.1, 0.3)), (0, "sticks"), tr="flash", music="playful", sfx=[(0.2, "whoosh", 0.4)])
P("C01", lambda g, c: bath_cut(g, c, 1.0) or label(g, "WHY?!", 1500, 260, 96, "#FF6B5B", k=pop(c.t, tw(c, "Why") - 0.1, 0.3)), ("sticks", 1),
  cam=Z(1.3, 1.36, (1000, 560)), sfx=[("sticks", "boing", 0.35)])
P("C02", s_old_theories, cam=Z(1.0, 1.04, (1100, 520)), music="curious")
P("C03", s_cold, cam=Z(1.0, 1.05, (1000, 540)), sfx=[("cold", "bloop", 0.35)])
P("C04", s_cells, (0, "and"), music="story")
P("C04", s_cells, ("and", 1), cam=Z(1.15, 1.2, (1300, 520)), sfx=[("weeks", "ding", 0.4)])
P("C05", s_30s, sfx=[("thirty", "sting", 0.4)])
P("C06", s_vortex, cam=Z(1.0, 1.06, (1000, 520)), music="curious", sfx=[("vortex", "whoosh", 0.4)])
P("C07", lambda g, c: s_vortex(g, c, True), cam=Z(1.1, 1.18, (950, 520)), sfx=[("pulls", "whoosh_soft", 0.4)])
P("C08", s_fix, (0, "And"), cam=Z(1.0, 1.04, (900, 600)), music="warm")
P("C08", s_fix, ("And", 1), cam=Z(1.0, 1.05, (960, 560)), sfx=[("Ig", "chime", 0.45)])
V.pause["C08"] = CH_PAUSE
# coffee ring
P("R01", s_spill, (0, "You"), tr="flash", music="curious", sfx=[(0.2, "bloop", 0.4)])
P("R01", s_spill, ("You", 1), cam=Z(1.15, 1.2, (1150, 600)), sfx=[("ring", "ding", 0.35)])
P("R02", s_chicago, cam=Z(1.0, 1.04, (1000, 540)), music="story")
P("R03", s_stuck, cam=Z(1.0, 1.04, (960, 620)), sfx=[("stuck", "click", 0.4)])
P("R04", s_flow, cam=Z(1.0, 1.04, (960, 600)), sfx=[("flows", "whoosh_soft", 0.35)])
P("R05", s_dump, cam=Z(1.0, 1.06, (960, 640)), sfx=[("rim", "ding", 0.4)])
P("R06", s_shape, cam=Z(1.0, 1.04, (960, 540)), music="curious", sfx=[("shape", "shimmer", 0.4)])
P("R07", s_noring, cam=Z(1.0, 1.04, (960, 560)), music="warm", sfx=[("ring", "chime", 0.45)])
P("R08", s_printer, cam=Z(1.0, 1.04, (960, 600)), sfx=[(0.2, "click", 0.3)])
V.pause["R08"] = CH_PAUSE
# cereal
P("K01", s_bowl_q, (0, "Why"), tr="flash", music="warm", sfx=[(0.2, "whoosh", 0.4)])
P("K01", s_bowl_q, ("Why", 1), cam=Z(1.15, 1.22, (960, 560)), sfx=[("clump", "pop", 0.35)])
P("K02", s_mathematicians, cam=Z(1.0, 1.04, (1000, 560)), music="story")
P("K03", s_slope, cam=Z(1.35, 1.45, (900, 480)), music="curious")
P("K04", s_drift, cam=Z(1.4, 1.45, (960, 480)), sfx=[("together", "pop", 0.4)])
P("K05", s_wall, cam=Z(1.3, 1.35, (1350, 480)), sfx=[("stick", "pop", 0.4)])
P("K06", s_assembly, music="warm", sfx=[(0.5, "shimmer", 0.35)])
V.pause["K06"] = CH_PAUSE
# ending
P("N01", lambda g, c: s_recap(g, c, R1), tr="flash", music="warm", sfx=[("Toast", "pop", 0.35), ("laces", "pop", 0.35), ("earbuds", "pop", 0.35)])
P("N02", lambda g, c: s_recap(g, c, R2), sfx=[("Spaghetti", "pop", 0.35), ("curtain", "pop", 0.35), ("coffee", "pop", 0.35), ("cereal", "pop", 0.35)])
P("N03", s_measure, cam=Z(1.0, 1.05, (1100, 560)))
P("N04", s_comments, cam=Z(1.0, 1.05, (900, 560)), sfx=[("comments", "pop", 0.4)])
V.build()

END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line=V.shots[-1]["line"], fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "Why toast lands butter-side down (it's the table)"), ("S01", "Why shoelaces come undone"), ("E01", "Why earbuds tangle"),
            ("P01", "Why spaghetti breaks into 3 pieces"), ("C01", "Why the shower curtain blows in"), ("R01", "Why coffee stains dry as rings"),
            ("K01", "Why cereal clumps together"), ("N01", "Every annoying thing has a reason")]


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
    elif cmd == "times":            # make.py times 0.1,2,3 out.jpg -> small sheet of chosen moments + frame-1 QA numbers
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
        V.render(str(EP / "final/B-005.mp4"))
