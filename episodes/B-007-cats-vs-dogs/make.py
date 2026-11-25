"""B-007 (L7) "Cats vs Dogs: Who's Smarter, and Who Loves You More?" — long video, Style F + cast v2.2 + pets (lib/flat_pets.py), 1920x1080.
python episodes/B-007-cats-vs-dogs/make.py sheet|qa|times <t,..> <out>|big <t,..>|chapters|animatic|render
Sets: living room + sofa (hook/loop), match arena with scoreboard (round cards), DNA/timeline studio, campfire night, farming village + grain store,
neuron lab (lavender), word lab Tokyo (pale green), garden + toy pile, detection hall, hearing lab (blue), kitchen floor, slow-motion labs (MIT blue,
Virginia Tech orange), shelter kennels, listening lab Sussex (purple), strange-situation room (mint).
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at, turn_at
from flat_fx import sparkles, arrow, burst, ring_wave, no_sign, qmark, gauge
from flat_pets import *
import sfxgen  # noqa: registers ring_bell, purr, lap

V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="match", captions=False)
CH_PAUSE = 1.2
FL = 900
BC = dict(fur="#2A2428", dark="#151215", light="#F4F1EA", ear="#1E1A1C", iris="#6A4020", nose=INK, collar="#FF6B5B")     # border collie
WILD = dict(fur="#B39270", dark="#6E5438", light="#EADBC4", inner="#E8A898", iris="#C9B23A", nose="#C97A7A")                # wildcat
KIT = dict(CAT, fur="#9AA3AD", dark="#5F6670", light="#EEF0F2", inner="#FFB3A6", iris="#7FB8E0")                          # grey kitten
SHELTER = [dict(DOG, fur="#3A3030", ear="#22181B", light="#E8E0D0"), dict(DOG, fur="#E8E0D0", ear="#B8A890", light="#FFFFFF"),
           dict(DOG, fur="#B5652A", ear="#7A3E1E")]


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


def tag(g, txt, x, y, k=1.0, size=46):
    """Small context label (year/place) while the story moves (why_not_viral rule 2)."""
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def studio(g, t, a="#E9A15A", b="#6B3420", cx=None):
    cx = W / 2 if cx is None else cx
    g.fill_all(g.rgrad(cx, H * 0.45, W * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(cx, H * 0.45), (cx + 2400 * math.cos(a0), H * 0.45 + 2400 * math.sin(a0)),
                (cx + 2400 * math.cos(a0 + 0.1), H * 0.45 + 2400 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


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


def bubble(g, x, y, txt, k=1.0, size=60, tail=(-1, 1), col="#FFFFFF"):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.6)):
        w = g.text_w(txt, size) + 70
        h = size * 1.7
        g.poly([(tail[0] * 30, h / 2 - 6), (tail[0] * 80, h / 2 + 50 * tail[1]), (tail[0] * 70 + 40 * tail[0] * -1, h / 2 - 6)], col, INK, lw=6)
        g.rc(0, 0, w, h, col, INK, lw=7, r=h / 2)
        g.text(txt, 0, 4, size, INK, stroke=None)


def heart(g, x, y, r, col="#FF5B6B", a=1.0, k=1.0):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.6) * r / 40):
        g.path("M0 30 Q-60 -10 -36 -40 Q-14 -60 0 -30 Q14 -60 36 -40 Q60 -10 0 30 Z", col, INK, lw=5, a=a)


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


def score_corner(g, c, d, ca, flash=None, k=1.0):
    """Small scoreboard top right (screen space)."""
    with g.screen():
        scoreboard(g, W - 300, 120, d, ca, c.gt, flash, 0.5 * back_out(clamp(k), 1.5))


# ------------------------------------------------------------------ sets
def living(g, t, warm=1.0):
    """Warm living room: peach wall, window onto a sunny garden, paw-print frame, wooden floor, rug, lamp."""
    g.fill_all(g.lgrad(0, 0, 0, H, mix("#F7D9B8", "#EFC39A", 0.3 * warm), "#E7B88E"))
    with g.layer(0.7):
        for i in range(-2, 26):
            g.rect(i * 90, 0, 6, FL, "#EBC7A0", None)
        g.rect(1260, 150, 440, 380, "#7A5236", INK, lw=9, r=10)                    # window
        g.rect(1280, 170, 400, 340, g.lgrad(0, 170, 0, 510, "#9FDCF5", "#D8F2FF"), None)
        g.ellipse(1480, 520, 300, 90, "#7CC56B", None)
        g.circle(1360, 430, 70, "#5FAE55", INK, lw=6); g.circle(1420, 400, 60, "#6FBE60", INK, lw=6)
        g.line([(1480, 170), (1480, 510)], "#7A5236", 10); g.line([(1280, 340), (1680, 340)], "#7A5236", 10)
        g.rect(300, 200, 220, 170, "#7A5236", INK, lw=7)                          # framed paw print
        g.rect(318, 218, 184, 134, "#FFF4E0", None)
        paw(g, 410, 290, 0.9, "#FF6B5B")
        with g.at(120, 900):                                                        # floor lamp
            g.line([(0, 0), (0, -560)], INK, 10)
            g.path("M-80 -560 L80 -560 L50 -680 L-50 -680 Z", "#FFC93C", INK, lw=7)
            g.glow(0, -600, 260, "#FFE29A", 0.35)
    g.rect(-100, FL, W + 200, H, "#B9844F", INK, lw=8)
    for i in range(-1, 14):
        g.line([(i * 170, FL), (i * 170 - 120, H)], "#9E6E3E", 5)
    g.ellipse(960, 990, 720, 70, "#C9584A", INK, lw=7)
    g.ellipse(960, 990, 600, 48, "#E07A5F", None)


def arena(g, t, flash=0.0):
    """Match arena: dark navy, two spotlights, ring ropes in brand colours, crowd silhouettes."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#16233D", "#0B1424"))
    with g.layer(0.5):
        for i in range(30):
            x = i * 70 - 40
            hh = 60 + 20 * math.sin(i * 1.7)
            g.ellipse(x, 640 - hh + 6 * math.sin(t * 3 + i), 34, 40, "#22324F", None)
            g.rect(x - 40, 650 - hh, 80, 200, "#22324F", None, r=30)
    for sx, col in ((420, "#FFE29A"), (1500, "#BDEBFF")):
        g.poly([(sx, -40), (sx - 260, FL + 60), (sx + 260, FL + 60)], col, None, a=0.10 + 0.04 * math.sin(t * 2 + sx))
    g.rect(-100, FL - 40, W + 200, 400, "#2F4F6F", INK, lw=8)
    g.rect(-100, FL - 40, W + 200, 30, "#3E6A8C", None)
    for i, col in enumerate(("#FF6B5B", "#FFC93C", "#5ED3B5")):
        y = 560 + i * 90
        g.line([(-20, y), (W + 20, y)], col, 16)
    for x in (90, W - 90):
        g.rc(x, 650, 40, 520, "#C9CED6", INK, lw=6, r=8)
    if flash > 0:
        g.rect(0, 0, W, H, "#FFFFFF", None, a=0.5 * flash)


def lab_room(g, t, wall="#C9B8E8", bench="#7A5AA0"):
    g.fill_all(g.lgrad(0, 0, 0, H, wall, shade(wall, 0.85)))
    with g.layer(0.7):
        for j in range(8):
            for i in range(-1, 18):
                g.rect(i * 120 + (60 if j % 2 else 0), j * 112, 112, 104, shade(wall, 1.06), None, r=6, a=0.5)
        g.rect(1300, 140, 420, 260, "#FFFFFF", INK, lw=7, r=10)
        for i in range(4):
            g.line([(1340, 200 + i * 50), (1340 + 300 - i * 50, 200 + i * 50)], "#3E7CB1", 10, a=0.6)
        paw(g, 1640, 330, 0.7, "#FF6B5B")
    g.rect(-100, FL, W + 200, H, shade(wall, 0.6), INK, lw=8)


def bench(g, x, y, w=600, col="#7A5AA0"):
    g.rect(x - w / 2, y - 260, w, 40, col, INK, lw=7, r=8)
    for sx in (-w / 2 + 40, w / 2 - 40):
        g.rect(x + sx - 15, y - 220, 30, 220, shade(col, 0.7), INK, lw=6)


def microscope(g, x, y, s=1.0):
    with g.at(x, y, 0, s):
        g.rc(0, -10, 160, 30, "#3A3A48", INK, lw=6, r=8)
        g.limb([(-40, -20), (-40, -150), (10, -200)], "#5A5A6A", 30, lw=6)
        g.limb([(10, -200), (40, -110)], "#3A3A48", 36, lw=6)
        g.rc(20, -80, 100, 14, "#8A8A9A", INK, lw=5)


def village(g, t):
    """Early farming village in the Middle East, ~10,000 years ago: ochre sky, mud-brick houses with flat roofs, wheat."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F7C978", "#F3A65E"))
    g.circle(1600, 220, 90, "#FFF0B8", None)
    g.glow(1600, 220, 300, "#FFF0B8", 0.4)
    with g.layer(0.5):
        for i, (x, w_, h_) in enumerate(((150, 300, 220), (520, 260, 260), (900, 320, 200), (1320, 280, 240), (1700, 300, 210))):
            g.rect(x - w_ / 2, 700 - h_, w_, h_, "#C98E5A", INK, lw=7)
            g.rect(x - w_ / 2 - 10, 700 - h_ - 18, w_ + 20, 24, "#A86E3E", INK, lw=6)
            g.rect(x - 30, 700 - 120, 60, 120, "#5A3A22", INK, lw=6, r=26)
    g.rect(-100, 700, W + 200, H, "#D9A75E", INK, lw=8)
    for i in range(40):
        x = i * 52 - 20
        g.line([(x, 1080), (x + 10 * math.sin(t * 1.5 + i), 800 + 30 * math.sin(i * 2.3))], "#B88A3A", 6)
        g.ellipse(x + 10 * math.sin(t * 1.5 + i), 790 + 30 * math.sin(i * 2.3), 8, 20, "#E8C46A", INK, lw=3)


def night_camp(g, t):
    """Night under stars, a campfire glow, hills: the time of hunters (no people drawn)."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0E1A33", "#24365A"))
    for i in range(60):
        x, y = (i * 383) % W, (i * 211) % 560
        g.circle(x, y, 2 + (i % 3), "#FFF4E0", None, a=0.5 + 0.4 * math.sin(t * 2 + i))
    g.path("M-100 760 Q400 560 900 720 Q1400 600 2020 740 L2020 1100 L-100 1100 Z", "#1C2A44", INK, lw=6)
    g.rect(-100, 860, W + 200, 300, "#2C3A2A", INK, lw=6)
    from flat_fx import flame
    g.glow(1400, 880, 420, "#FF9A3A", 0.35)
    for k in range(5):
        g.limb([(1340 + k * 30, 900), (1400, 870)], "#5A3A22", 16, lw=4)
    flame(g, 1400, 880, 120, 180, t)


def garden(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#8FD3F4", "#DDF4FF"))
    for i, (x, y) in enumerate(((300, 160), (1100, 110), (1650, 200))):
        x += 20 * math.sin(t * 0.2 + i)
        g.ellipse(x, y, 130, 50, "#FFFFFF", None, a=0.9); g.ellipse(x + 70, y - 30, 80, 50, "#FFFFFF", None, a=0.9)
    with g.layer(0.6):
        for i in range(-1, 26):
            g.rect(i * 80, 520, 60, 260, "#F4E3C8", INK, lw=5)
            g.poly([(i * 80, 520), (i * 80 + 30, 480), (i * 80 + 60, 520)], "#F4E3C8", INK, lw=5)
        g.rect(-100, 600, W + 200, 30, "#E2CDAA", INK, lw=5)
        g.circle(1650, 420, 170, "#5FAE55", INK, lw=7); g.rect(1630, 540, 40, 240, "#7A5236", INK, lw=6)
    g.rect(-100, 760, W + 200, H, "#79C25E", INK, lw=8)
    for i in range(60):
        x = (i * 97) % W
        g.line([(x, 1080 - (i % 5) * 50), (x + 8, 1060 - (i % 5) * 50)], "#5FA048", 5)


def kitchen_floor(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE7C2", "#F6D2A2"))
    with g.layer(0.7):
        g.rect(-100, 380, W + 200, 40, "#C9584A", INK, lw=6)
        for i in range(10):
            g.rect(i * 220 - 60, 420, 200, 460, "#FFF4E0", INK, lw=6, r=8)
            g.circle(i * 220 + 100, 640, 10, "#C9A27A", INK, lw=3)
    for j in range(5):
        for i in range(-1, 16):
            g.rect(i * 140 + (70 if j % 2 else 0), FL + j * 60, 140, 60, "#E8EEF2" if (i + j) % 2 else "#CFE3E8", INK, lw=3)


def shelter(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#DCEBD7", "#BFD8BA"))
    for i in range(3):
        x = 330 + i * 630
        g.rect(x - 280, 160, 560, 740, "#F4F1EA", INK, lw=7, r=10)
        g.rect(x - 240, 200, 480, 700, "#E3DCCB", None)
    g.rect(-100, FL, W + 200, H, "#9AA78E", INK, lw=8)


def kennel_bars(g, i, k=0.0):
    x = 330 + i * 630
    for j in range(9):
        xx = x - 240 + j * 60
        g.line([(xx, 200), (xx, 900 - 640 * k)], "#5A6470", 10)
    g.line([(x - 250, 200), (x + 250, 200)], "#5A6470", 14)


def strange_room(g, t, door_open=0.0):
    """Bare test room: pale mint walls, a chair, a door, toys on the floor."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#CFEDE3", "#B0DCCD"))
    with g.layer(0.7):
        g.rect(1500, 260, 300, 640, "#7A5236", INK, lw=8)
        g.rect(1520, 280, 260, 620, "#3A2416", None)
        with g.at(1520, 280, 0, 1 - 0.85 * door_open, 1):
            g.rect(0, 0, 260, 620, "#C98E5A", INK, lw=7)
            g.circle(220, 320, 12, PAL["yellow"], INK, lw=4)
        g.rect(160, 200, 300, 200, "#FFFFFF", INK, lw=7, r=8)
        g.rect(180, 220, 260, 160, "#9FDCF5", None)
    g.rect(-100, FL, W + 200, H, "#E3DCCB", INK, lw=8)


def chair(g, x, y, col="#3E7CB1"):
    g.rect(x - 120, y - 420, 240, 260, col, INK, lw=7, r=20)
    g.rect(x - 140, y - 200, 280, 50, shade(col, 0.9), INK, lw=7, r=12)
    for sx in (-110, 110):
        g.rect(x + sx - 12, y - 160, 24, 160, "#5A3A22", INK, lw=5)


def headphones(g, x, y, s=1.0, col="#2F3A4F"):
    with g.at(x, y, 0, s):
        g.path("M-70 0 Q-70 -90 0 -92 Q70 -90 70 0", None, col, lw=14)
        g.rc(-70, 10, 34, 64, col, INK, lw=5, r=12); g.rc(70, 10, 34, 64, col, INK, lw=5, r=12)


def brain_side(g, x, y, s=1.0, hot=0.0, t=0.0):
    """Simple side-view brain with the cortex (outer layer) highlighted by `hot`."""
    with g.at(x, y, 0, s):
        d = "M-220 40 Q-260 -120 -120 -180 Q0 -240 140 -180 Q260 -120 230 20 Q220 120 100 130 Q20 170 -60 120 Q-200 140 -220 40 Z"
        g.path(d, mix("#FFB8C8", "#FFC93C", hot), INK, lw=10)
        g.path("M-180 30 Q-200 -90 -100 -140 Q0 -190 120 -140 Q200 -90 190 10 Q180 90 90 100 Q20 130 -50 90 Q-170 100 -180 30 Z", "#F59AAE", None)
        for (a, b) in (((-150, -60), (-60, -100)), ((-40, -150), (40, -110)), ((80, -140), (150, -60)), ((-120, 20), (-20, 0)), ((20, 40), (140, 20))):
            g.path(f"M{a[0]} {a[1]} Q{(a[0]+b[0])/2} {a[1]-40} {b[0]} {b[1]}", None, "#C96A82", lw=8)
        g.limb([(40, 120), (60, 200), (50, 260)], "#F59AAE", 50, lw=8)


def wave_line(g, x0, x1, y, amp, f, t, col, w=8, spike=0.0, spike_x=0.5, a=1.0):
    pts = []
    n = 160
    for i in range(n + 1):
        u = i / n
        x = x0 + (x1 - x0) * u
        yy = y + amp * math.sin(TAU * f * u + t * 6)
        if spike > 0:
            yy += spike * amp * 1.2 * math.sin(TAU * f * 9 * u + t * 20) * math.exp(-((u - spike_x) / 0.12) ** 2)
        pts.append((x, yy))
    g.line(pts, col, w, a=a)


def bars(g, x, y, items, k=1.0, maxv=100.0, w=900, size=50):
    """Horizontal bars: items [(label, value, colour, text)]."""
    for i, (lab, v, col, txt) in enumerate(items):
        yy = y + i * 150
        kk = clamp(k * 1.4 - i * 0.3)
        g.rc(x - 120, yy, 200, 90, PAL["navy"], None, r=18)
        g.text(lab, x - 120, yy + 4, size * 0.8, PAL["cream"], stroke=None)
        bw = w * v / maxv * ease_out(kk)
        if bw > 4:
            g.rect(x, yy - 40, bw, 80, col, INK, lw=7, r=18)
        if kk > 0.95:
            g.text(txt, x + bw + 120, yy + 4, size, PAL["yellow"], sw=9)


# ------------------------------------------------------------------ scenes: hook + round 1
def lena_call(g, c, x=430, h=920, k_bub=1.0, txt="MISO!", expr="smile"):
    char2(g, "lena", x, FL + 120, h, expr, "hip", "point", t=c.gt, view="3q")
    for i in range(3):
        ph = (c.gt * 1.8 + i / 3) % 1
        xx = x + 330 + 300 * ph
        g.path(f"M{xx} {330 - 40 * ph} Q{xx + 50} 440 {xx} {550 + 40 * ph}", None, PAL["coral"], lw=12, a=k_bub * (1 - ph))
    bubble(g, x + 330, 300, txt, k_bub, 78, tail=(-1, 1))


def s_hook(g, c):
    living(g, c.gt)
    sofa(g, 1180, FL + 20, 760)
    t = c.t
    ear = -0.7 + 1.7 * ease_out(clamp((t % 1.6) / 0.25)) if t < 1.6 else 1.0   # the ear flicks toward the call from frame 0
    cat_sit(g, 1180, FL - 230, 1.15, c.gt, "deadpan", ear_l=ear, ear_r=-0.2, look=(-0.6, 0), tail=1.4)
    lena_call(g, c, 430, 980, 1.0)
    with g.screen():
        g.text("IGNORING YOU?", W / 2 + 120, 1000, 120, PAL["yellow"], sw=20, depth=9, sc=back_out(clamp(t / 0.25), 1.4) if t > 0 else 1.0)


def s_nocome(g, c):
    living(g, c.gt)
    sofa(g, 960, FL + 20, 900)
    k = on(c, "doesn't")
    cat_sit(g, 960, FL - 230, 1.35, c.gt, "smug" if k > 0.5 else "deadpan", ear_l=1.0, ear_r=0.3, look=(-0.3, 0), tail=0.4)
    for i in range(3):
        kk = clamp(k * 2 - i * 0.3)
        with g.at(560 - i * 110, 700):
            paw(g, 0, 0, 0.6, INK, a=0.25 * kk)
    cross(g, 380, 560, 60, pk(c, "come"))
    label(g, "...NOPE", 1480, 300, 90, k=pk(c, "come"))


def s_muscle(g, c, close=False):
    studio(g, c.gt, "#F2B05A", "#7A3A1E")
    b = clamp(lt(c) / 2.0)
    br = 0.5 + 0.5 * math.sin(lt(c) * 1.4 - 1.5) if not close else ease_io(b)
    if not close:
        dog_sit(g, 760, FL + 150, 1.15, c.gt, "calm", brow=br, tongue=0.0, look=(0.4, -0.3))
        char2(g, "lena", 1450, FL + 120, 900, "shocked" if br > 0.6 else "deadpan", "hold", "hold", t=c.gt, view="3q", flip=True)
        for i in range(3):
            heart(g, 1300 + i * 90, 300 - 60 * ((lt(c) * 0.6 + i * 0.3) % 1), 30, k=br)
    else:
        dog_face(g, 960, 560, 2.3, c.gt, "calm", brow=br, look=(0, -0.3))
        arrow(g, 1500, 220, 1130, 380, k=on(c, "muscle", frac=0.3))
        label(g, "NEW MUSCLE", 1560, 170, 76, k=on(c, "muscle", frac=0.3))


def s_versus(g, c, board=False):
    arena(g, c.gt)
    kk = back_out(seg(c.t, 0.05, 0.5), 1.4)
    dog_sit(g, 420 - 500 * (1 - kk), FL + 120, 1.0, c.gt, "happy", tongue=0.6, look=(0.6, 0))
    cat_sit(g, 1500 + 500 * (1 - kk), FL - 10, 1.15, c.gt, "smug", look=(-0.6, 0))
    with g.screen():
        g.text("VS", W / 2, 480, 220, PAL["yellow"], sw=28, depth=14, sc=pop(c.t, 0.3, 0.4) + 1e-3)
    if board:
        scoreboard(g, W / 2, 190, 0, 0, c.gt, None, 0.8 * back_out(clamp(c.t / 0.4), 1.5))
        label(g, "7 ROUNDS", W / 2, 760, 80, PAL["cream"], k=pk(c, "Seven"))


def s_science(g, c):
    arena(g, c.gt)
    dog_sit(g, 520, FL + 120, 0.95, c.gt, "calm", tongue=0.0, look=(0.8, 0))
    cat_sit(g, 1400, FL - 10, 1.1, c.gt, "deadpan", look=(-0.8, 0))
    k1, k2 = pk(c, "opinions"), pk(c, "science")
    cross(g, W / 2 - 230, 330, 54, k1)
    label(g, "OPINIONS", W / 2 + 40, 330, 76, PAL["cream"], k=k1)
    check(g, W / 2 - 230, 470, 54, k2)
    label(g, "SCIENCE", W / 2 + 40, 470, 86, k=k2)


def round_card(n, title, d, ca):
    def f(g, c):
        arena(g, c.gt, flash=max(0, 1 - c.t / 0.25))
        dog_sit(g, 300, FL + 180, 0.9, c.gt, "happy", tongue=0.5, look=(0.8, 0), seed=n)
        cat_sit(g, 1640, FL + 40, 1.0, c.gt, "deadpan", look=(-0.8, 0), seed=n)
        k = back_out(seg(c.t, 0.0, 0.4), 1.5)
        with g.screen():
            g.text(f"ROUND {n}", W / 2, 360, 170, PAL["yellow"], sw=24, depth=12, sc=0.6 + 0.4 * k)
            kk = back_out(seg(c.t, 0.3, 0.4), 1.5)
            g.rc(W / 2, 560, g.text_w(title, 84) + 90, 140, PAL["coral"], INK, lw=9, r=30, rot=-0.02)
            g.text(title, W / 2, 566, 84, PAL["cream"], sw=10, sc=kk + 1e-3)
        score_corner(g, c, d, ca)
    return f


def s_dna(g, c):
    studio(g, c.gt, "#7BC7B5", "#1F4F4A")
    k = 0.35 + 0.65 * clamp(lt(c) / 2.5)
    dna_tree(g, 960, 1000, 1.25, k, c.gt)
    with g.at(960, 1010, 0, 0.42):
        dog_face(g, 0, 0, 1.0, c.gt, "calm", wolf=True)
    label(g, "WOLF", 1210, 1020, 60, PAL["cream"], k=1.0)
    tag(g, "5 FAMILIES · 11,000 YEARS AGO", 960, 90, on(c, "five", frac=0.3))
    label(g, "NO FARMS YET", 1620, 380, 64, k=on(c, "hunter", frac=0.8), rot=0.04)


def s_wolf_dog(g, c):
    night_camp(g, c.gt)
    u = clamp(c.t / max(0.1, c.T))
    x = 300 + 700 * u
    m = clamp((u - 0.35) / 0.3)
    if m < 1:
        with g.group(1 - m):
            dog_side(g, x, 1010, 1.0, c.gt, walk=1, wolf=True, expr="calm")
    if m > 0:
        with g.group(m):
            dog_side(g, x, 1010, 1.0, c.gt, walk=1, expr="happy")
    label(g, "WOLF", 420, 300, 70, PAL["cream"], k=1 - m)
    label(g, "DOG", 1000, 300, 80, k=m)
    cross(g, 1620, 300, 50, on(c, "farm"))
    label(g, "FIRST FARM", 1620, 400, 50, PAL["cream"], k=on(c, "farm"))


def s_cat_enters(g, c):
    living(g, c.gt)
    sofa(g, 1180, FL + 20, 760)
    u = ease_io(clamp(c.t / max(0.1, c.T * 0.75)))
    cat_side(g, 2100 - 1000 * u, FL + 60, 1.0, c.gt, flip=True, walk=1 - u * 0.8, expr="smug", tail=1.2)
    label(g, "UNINVITED", 600, 300, 90, k=pk(c, "invited"))


def s_village(g, c):
    village(g, c.gt)
    for i, x in enumerate((300, 470, 640, 1500, 1680)):
        grain_jar(g, x, 980 + (i % 2) * 20, 0.9 + 0.1 * (i % 3), ["#C8875A", "#B5703E", "#D99A64"][i % 3])
    km = on(c, "mice")
    for i in range(4):
        mx = 560 + i * 180 + 40 * math.sin(c.gt * 3 + i)
        if km > 0:
            mouse(g, mx, 1010 - 20 * (i % 2), 0.7 * km, c.gt + i, flip=i % 2 == 0)
    kc = on(c, "cats", n=0, frac=0.85)
    if kc > 0:
        cat_side(g, 2100 - 700 * kc, 1000, 0.9, c.gt, flip=True, walk=1 - kc, col=WILD, expr="alert")
    tag(g, "MIDDLE EAST · ~10,000 YEARS AGO", 960, 90, on(c, "farming", frac=0.2))
    label(g, "GRAIN", 470, 620, 70, k=pk(c, "grain", frac=0.5))
    label(g, "MICE", 900, 820, 70, k=pk(c, "mice"))


def s_wildcat(g, c):
    village(g, c.gt)
    with g.at(1000, 1000):
        g.rect(-260, -240, 520, 240, "#C98E5A", INK, lw=7)                        # grain store wall
    for i, x in enumerate((780, 1220)):
        grain_jar(g, x, 1000, 1.0)
    cat_sit(g, 1000, 760, 0.85, c.gt, "smug", col=WILD, look=(0.6, 0.3), tail=0.7)
    mouse(g, 1500 + 200 * ((c.gt * 0.5) % 1), 1010, 0.7, c.gt, flip=False)
    label(g, "BEST HUNTING SPOT", 960, 220, 80, k=pk(c, "hunting", frac=0.4))


def s_to_sofa(g, c):
    living(g, c.gt)
    sofa(g, 960, FL + 20, 900)
    cat_sit(g, 960, FL - 230, 1.25, c.gt, "happy" if c.t > 1.0 else "deadpan", tail=0.5, seed=2)
    label(g, "YOUR SOFA", 960, 160, 80, k=pk(c, "sofa", frac=0.6))


def s_verdict(d, ca, who, text=None, scene="arena"):
    def f(g, c):
        if scene == "living":
            living(g, c.gt); sofa(g, 1180, FL + 20, 760)
            cat_sit(g, 1180, FL - 230, 1.0, c.gt, "smug" if who == "cat" else "deadpan")
            dog_sit(g, 500, FL + 120, 0.95, c.gt, "happy" if who == "dog" else "calm", tongue=0.5)
        else:
            arena(g, c.gt)
            dog_sit(g, 360, FL + 150, 0.9, c.gt, "happy" if who in ("dog", "both") else "sad", tongue=0.6 if who in ("dog", "both") else 0.0,
                    paw=on(c, "Point", frac=0.6) if who in ("dog", "both") else 0)
            cat_sit(g, 1560, FL + 10, 1.05, c.gt, "smug" if who in ("cat", "both") else "bored",
                    paw=on(c, "Point", frac=0.6) if who in ("cat", "both") else 0)
        kp = on(c, "Point", frac=0.55) if "Point" in c.V.T[c.sh["line"]]["text"] else on(c, "One", frac=0.6)
        prev = (d - (1 if who in ("dog", "both") else 0), ca - (1 if who in ("cat", "both") else 0))
        cur = (d, ca) if kp > 0.5 else prev
        scoreboard(g, W / 2, 330, cur[0], cur[1], c.gt, who if kp > 0.5 else None, 1.0 + 0.08 * pop(c.t, tw(c, "Point", frac=0.55), 0.3))
        if text:
            label(g, text, W / 2, 620, 64, PAL["cream"], k=kp)
    return f


# ------------------------------------------------------------------ round 2: brains
def s_vanderbilt(g, c, chart=False):
    lab_room(g, c.gt, "#D4C6EE", "#7A5AA0")
    bench(g, 760, FL, 700)
    microscope(g, 660, FL - 260, 1.1)
    char2(g, "vet", 1150, FL + 100, 860, "deadpan", "hold", pose_at(lt(c), [(0, "down"), (2.5, "explain")]), t=c.gt, view="3q", flip=True)
    tag(g, "2017 · VANDERBILT UNIVERSITY, USA", 960, 90, on(c, "2017", frac=0.0) if not chart else 1.0)
    if chart:
        with g.screen():
            g.rect(1320, 160, 520, 440, "#FFFFFF", INK, lw=8, r=16)
            g.text("NEURON COUNT", 1580, 220, 50, INK, stroke=None)
            for i, fn in enumerate(("cat", "dog", "bear")):
                kk = on(c, "counted", frac=0.5) if i == 0 else clamp(on(c, "counted", frac=0.5) * 2 - i * 0.4)
                y = 320 + i * 100
                if fn == "cat": cat_face(g, 1400, y, 0.3, c.gt)
                elif fn == "dog": dog_face(g, 1400, y, 0.27, c.gt, "happy")
                else:
                    with g.at(1400, y + 30, 0, 0.18): bear_side(g, -60, 0, 1.0)
                g.rect(1460, y - 18, 300 * kk * (0.5, 1.0, 0.5)[i], 36, ["#F29A3E", "#D9A35E", "#8A5A3A"][i], INK, lw=5, r=10)


def s_cortex(g, c):
    studio(g, c.gt, "#B9A3E3", "#3A2A5E")
    hot = 0.5 + 0.5 * math.sin(c.gt * 3)
    brain_side(g, 960, 600, 1.7, hot * on(c, "cortex", frac=0.2), c.gt)
    label(g, "CORTEX", 960, 150, 96, k=pk(c, "cortex", frac=0.2))
    label(g, "PLANNING", 420, 860, 64, PAL["cream"], k=pk(c, "planning"))
    label(g, "PROBLEM-SOLVING", 1500, 860, 64, PAL["cream"], k=pk(c, "problem-solving"))


def s_dots(g, c, bear=False):
    studio(g, c.gt, "#B9A3E3", "#3A2A5E")
    with g.screen():
        if not bear:
            kc = clamp((c.t - 0.1) / 1.2)
            kd = clamp((c.t - tw(c, "dog", frac=0.5)) / 1.4)
            cat_face(g, 330, 400, 0.75, c.gt, "deadpan" if kd < 1 else "shock")
            neuron_dots(g, 560, 480, 25, cols=13, gap=46, r=17, col=CAT["fur"], k=kc)
            g.text("250 MILLION", 690, 230, 56, PAL["cream"], sw=8, sc=pk(c, "fifty") + 1e-3)
            dog_face(g, 330, 820, 0.65, c.gt, "happy" if kd > 0.9 else "calm", tongue=0.4)
            neuron_dots(g, 560, 930, 53, cols=18, gap=46, r=17, col=DOG["fur"], k=kd)
            g.text("530 MILLION", 820, 700, 56, PAL["cream"], sw=8, sc=pk(c, "thirty") + 1e-3)
            g.text("1 DOT = 10 MILLION NEURONS", 1500, 130, 40, PAL["cream"], stroke=None)
            k2 = pk(c, "twice")
            if k2 > 0:
                g.text("2×", 1640, 760, 220, PAL["yellow"], sw=26, depth=14, sc=k2)


def s_bear(g, c):
    studio(g, c.gt, "#A3C9E3", "#1F3A5E")
    kb = on(c, "bear", frac=0.2)
    bear_side(g, 1250, 980, 1.6 * kb + 1e-3, c.gt)
    cat_side(g, 360, 980, 0.8, c.gt, expr="deadpan")
    with g.screen():
        k = pk(c, "ten")
        if k > 0:
            g.text("10× BIGGER CORTEX", 1250, 160, 76, PAL["yellow"], sw=12, sc=k)
        k3 = on(c, "same")
        if k3 > 0:
            neuron_dots(g, 160, 420, 25, cols=5, gap=34, r=12, col=CAT["fur"], k=k3)
            neuron_dots(g, 1100, 420, 25, cols=5, gap=34, r=12, col="#8A5A3A", k=k3)
            g.text("=", 760, 360, 160, PAL["cream"], sw=18, sc=k3)


def s_bigger(g, c):
    studio(g, c.gt, "#B9A3E3", "#3A2A5E")
    with g.screen():
        g.circle(560, 560, 300, "#FFB8C8", INK, lw=10)
        for i in range(10):
            a = i * 2.4
            g.circle(560 + 200 * math.cos(a) * (i % 3 + 1) / 3, 560 + 200 * math.sin(a) * (i % 3 + 1) / 3, 14, PAL["yellow"], INK, lw=3)
        g.circle(1400, 560, 160, "#FFB8C8", INK, lw=10)
        for i in range(40):
            a = i * 2.4; r = 140 * math.sqrt((i + 0.5) / 40)
            g.circle(1400 + r * math.cos(a), 560 + r * math.sin(a), 12, PAL["yellow"], INK, lw=3)
        g.text("≠", 960, 560, 200, PAL["cream"], sw=20, sc=pk(c, "doesn't"))
        label(g, "BIGGER BRAIN", 560, 950, 60, PAL["cream"], k=1)
        label(g, "MORE NEURONS", 1400, 950, 60, k=pk(c, "thinking"))


def s_clever(g, c):
    kitchen_floor(g, c.gt)
    op = ease_io(clamp((c.t - 0.4) / 1.2))
    with g.at(1250, FL + 40):
        g.rect(-220, -380, 440, 380, "#5A3A22", INK, lw=8, r=8)                    # cupboard (inside)
        with g.at(-120, -150, 0.3):
            g.ellipse(0, 0, 70, 34, "#7FB8E0", INK, lw=6); g.poly([(60, 0), (110, -34), (110, 34)], "#7FB8E0", INK, lw=6)
            g.circle(-34, -6, 7, INK, None)
        g.rect(0, -380, 220, 380, "#E0A86E", INK, lw=7, r=6)
        with g.at(-220, -380, 0, max(0.08, 1 - 0.92 * op), 1):
            g.rect(0, 0, 220, 380, "#E0A86E", INK, lw=7, r=6)
            g.circle(190, 190, 12, PAL["yellow"], INK, lw=4)
    cat_sit(g, 830, FL + 60, 1.0, c.gt, "smug" if op > 0.6 else "deadpan", paw=0.9 * clamp(c.t / 0.5) * (1 - op * 0.6), look=(0.8, 0))
    label(g, "CLEVER IN THEIR OWN WAY", 960, 160, 70, k=pk(c, "clever"))


# ------------------------------------------------------------------ round 3: names
def s_chaser(g, c, glow=None, fetch=0.0, newtoy=0.0, dx=500):
    garden(g, c.gt)
    toy_pile(g, 1250, 1000, 1.4, n=60, glow_i=glow, t=c.gt)
    if newtoy > 0:
        with g.at(1500, 900, 0, back_out(clamp(newtoy), 1.6)):
            g.glow(0, 0, 120, PAL["yellow"], 0.5)
            toy(g, 0, 0, 2, 1.6, 0.2)
            g.text("NEW", 0, -90, 46, PAL["yellow"], sw=8)
    dog_sit(g, dx + 300 * fetch, FL + 160, 1.0, c.gt, "happy", tongue=0.6, look=(0.8, 0), col=BC, seed=4)


def s_1022(g, c):
    s_chaser(g, c)
    with g.screen():
        n = int(1022 * ease_out(clamp(c.t / 2.2)))
        g.text(f"{n:,}", 1250, 330, 190, PAL["yellow"], sw=24, depth=12)
        g.text("TOY NAMES", 1250, 470, 70, PAL["cream"], sw=10)


def s_pilley(g, c, pickup=False):
    garden(g, c.gt)
    toy_pile(g, 1450, 1000, 1.2, n=50, glow_i=7 if not pickup else None, t=c.gt)
    char2(g, "prof", 230, FL + 160, 880, "smug", "hold", pose_at(lt(c), [(0, "down"), (1.0, "point")]), t=c.gt, view="3q")
    u = clamp((lt(c) - 3.0) / 2.5)
    run = math.sin(math.pi * u)
    if u <= 0 or u >= 1:
        dog_sit(g, 920, FL + 160, 0.85, c.gt, "happy" if u < 1 else "calm", tongue=0.6 if u < 1 else 0.0, look=(0.8, 0), col=BC)
    else:
        dog_side(g, 920 + 300 * run, FL + 140, 0.7, c.gt, flip=u > 0.5, walk=1, col=BC)
    if u >= 1:
        toy(g, 920, FL + 160 - 380 * 0.85, 7, 0.9)                         # the toy brought back, in the mouth
    bubble(g, 640, 300, "THE BLUE BONE!", on(c, "Ask"), 54, tail=(-1, 1))
    tag(g, "PSYCHOLOGIST JOHN PILLEY", 960, 90, on(c, "Pilley", frac=0.2))


def s_newtoy(g, c):
    s_chaser(g, c, newtoy=on(c, "added"), fetch=0.6 * on(c, "picked", frac=0.7), dx=820)
    char2(g, "prof", 200, FL + 160, 820, "deadpan", "hold", "point", t=c.gt, view="3q")
    bubble(g, 560, 260, "THE DAX?", on(c, "asked"), 60, tail=(-1, 1))
    check(g, 1500, 700, 60, pk(c, "worked"))
    label(g, "SHE WORKED IT OUT", 1300, 180, 70, k=pk(c, "worked"))


def s_notsofast(g, c):
    living(g, c.gt)
    sofa(g, 1180, FL + 20, 760)
    cat_sit(g, 1180, FL - 230, 1.15, c.gt, "smug", paw=on(c, "Not"), look=(-0.5, 0))
    label(g, "NOT SO FAST", 560, 300, 100, k=pk(c, "Not"))


def word_lab(g, t):
    lab_room(g, t, "#CDE8C9", "#5E9E4A")


def s_tokyo(g, c, phase="words"):
    word_lab(g, c.gt)
    with g.at(960, FL + 40):
        g.ellipse(0, 0, 260, 50, "#FF6B5B", INK, lw=7)
    lt_ = lt(c)
    name_k = on(c, "name") if phase == "name" else 0.0
    bored = phase == "words" or (phase == "name" and name_k < 0.5)
    ear = 1.0 if (phase in ("name", "stranger") and not bored) else -0.4
    cat_sit(g, 960, FL + 30, 1.05, c.gt, "bored" if bored else "alert", ear_l=ear, ear_r=ear, tilt=0.12 if not bored else 0.0,
            look=(-0.8, 0) if not bored else (0, 0.3))
    speaker(g, 380, FL - 160, 1.2, c.gt, on=1.0)
    words = ["TABLE", "RAIN", "CHAIR", "PEN"]
    if phase == "words":
        for i, wd in enumerate(words):
            kk = clamp(c.t * 1.2 - i * 0.6)
            if kk > 0:
                bubble(g, 560 + i * 260, 260 + (i % 2) * 120, wd, kk, 50, tail=(-1, 1), col="#E8EEF2")
        tag(g, "2019 · TOKYO, JAPAN", 960, 90, on(c, "2019", frac=0.0))
    elif phase == "name":
        bubble(g, 640, 300, "MISO!", name_k, 80, tail=(-1, 1), col=PAL["yellow"])
        if name_k > 0.5:
            ring_wave(g, 960, 600, 120, 380, (c.gt * 1.5) % 1, PAL["yellow"])
    else:
        char2(g, "vet", 1560, FL + 100, 820, "deadpan", "hold", "explain", t=c.gt, view="3q", flip=True)
        bubble(g, 1260, 280, "MISO!", on(c, "stranger", frac=0.3), 70, tail=(1, 1), col=PAL["yellow"])
        label(g, "STRANGER", 1560, 160, 60, PAL["cream"], k=on(c, "stranger", frac=0.3))


def s_nomove(g, c):
    word_lab(g, c.gt)
    with g.at(960, FL + 40):
        g.ellipse(0, 0, 260, 50, "#FF6B5B", INK, lw=7)
    cat_sit(g, 960, FL + 30, 1.05, c.gt, "deadpan", ear_l=1.0, ear_r=1.0, look=(-0.6, 0))
    k1, k2 = pk(c, "walk"), pk(c, "meow")
    with g.screen():
        for i in range(4):
            paw(g, 300 + i * 90, 820 - i * 50, 0.5, INK, a=0.3 * k1)
        cross(g, 420, 600, 60, k1)
        bubble(g, 1450, 360, "MEOW", k2, 64, tail=(-1, 1))
        cross(g, 1450, 360, 60, k2)


def s_heard(g, c):
    living(g, c.gt)
    sofa(g, 1180, FL + 20, 760)
    cat_sit(g, 1180, FL - 230, 1.15, c.gt, "deadpan", ear_l=1.0, ear_r=0.1, look=(-0.6, 0))
    lena_call(g, c, 430, 960, 1.0, "MISO!", "deadpan")
    label(g, "IT HEARD YOU", 1180, 180, 80, k=pk(c, "heard"))


# ------------------------------------------------------------------ round 4: senses
def s_nose(g, c):
    garden(g, c.gt)
    u = clamp(c.t / max(0.1, c.T))
    dog_side(g, 300 + 900 * u, FL + 120, 0.95, c.gt, walk=1, sniff=1, expr="calm")
    label(g, "FAMOUS NOSE", 960, 200, 90, k=pk(c, "nose", frac=0.8))


def s_receptors(g, c):
    studio(g, c.gt, "#F2B05A", "#7A3A1E")
    with g.screen():
        dog_face(g, 300, 330, 0.72, c.gt, "calm", look=(0.6, 0))
        char2(g, "lena", 300, 1130, 520, "deadpan", "down", "down", t=c.gt, view="front")
        bars(g, 720, 380, [("DOG", 300, DOG["fur"], "300 MILLION"), ("YOU", 6, "#7FCBEF", "6 MILLION")],
             k=clamp((c.t - 0.3) / 2.5), maxv=300, w=760)
        g.text("SMELL RECEPTORS", 1150, 160, 60, PAL["cream"], sw=10)


def s_detect(g, c):
    lab_room(g, c.gt, "#E3E6EA", "#5A6470")
    for i in range(6):
        x = 260 + i * 260
        g.rect(x - 90, FL - 150, 180, 150, ["#3E7CB1", "#FF6B5B", "#5ED3B5", "#FFC93C", "#B05BD6", "#FF8A3D"][i], INK, lw=7, r=14)
        g.rect(x - 30, FL - 175, 60, 30, INK, None, r=8)
    u = clamp(c.t / max(0.1, c.T * 0.8))
    dog_side(g, 160 + 900 * u, FL + 110, 0.75, c.gt, walk=1 - u * 0.7, sniff=1, expr="calm")
    if u > 0.85:
        g.glow(1040, FL - 80, 160, PAL["yellow"], 0.5)
        check(g, 1040, FL - 280, 50, (u - 0.85) / 0.15)


def s_ears(g, c):
    studio(g, c.gt, "#F29A3E", "#6B2A10")
    e = math.sin(c.gt * 3)
    cat_face(g, 960, 620, 2.4, c.gt, "alert", ear_l=e, ear_r=-e)
    arrow(g, 1500, 200, 1250, 330, k=on(c, "weapon", frac=0.4))
    label(g, "SECRET WEAPON", 1560, 140, 72, k=on(c, "weapon", frac=0.4))


def s_heffner(g, c):
    lab_room(g, c.gt, "#BFDDF2", "#3E7CB1")
    speaker(g, 420, FL - 120, 1.3, c.gt, on=1.0)
    char2(g, "vet", 1500, FL + 100, 850, "deadpan", "hold", "explain", t=c.gt, view="3q", flip=True)
    with g.at(960, 420):
        g.rect(-240, -140, 480, 280, "#0B1F33", INK, lw=8, r=14)
        wave_line(g, -210, 210, 0, 60, 3 + 6 * ((c.gt * 0.3) % 1), c.gt, PAL["mint"], w=6)
    tag(g, "1980s · HEARING TESTS", 960, 90, on(c, "1980s", frac=0.0))


def s_freq(g, c, cat=False):
    studio(g, c.gt, "#7FB8E0", "#1F3A5E")
    with g.screen():
        g.text("HIGHEST SOUND HEARD (VIBRATIONS PER SECOND)", W / 2, 140, 46, PAL["cream"], stroke=None)
        kd = clamp((c.t - 0.2) / 1.2) if not cat else 1.0
        kc = clamp((c.t - 0.2) / 1.8) if cat else 0.0
        freq_bar(g, 330, 360, 1100, kd, kc, True, c.gt)
        if not cat:
            label(g, "2× YOU", 1150, 780, 80, k=pk(c, "twice"))
        else:
            label(g, "ONE OF THE WIDEST", 1100, 850, 80, k=pk(c, "widest"))


def s_squeak(g, c):
    garden(g, c.gt)
    sq = 0.5 + 0.5 * math.sin(c.gt * 9)
    mouse(g, 1350, FL + 110, 1.5, c.gt, squeak=sq * on(c, "squeaks", frac=0.4))
    cat_sit(g, 800, FL + 140, 0.95, c.gt, "alert", ear_l=0.8, ear_r=1.0, look=(1, 0.4))
    char2(g, "lena", 260, FL + 160, 820, "deadpan", "down", "down", t=c.gt, view="3q")
    qmark(g, 380, 260, 120, k=pk(c, "never"))
    label(g, "TOO HIGH FOR YOU", 1300, 220, 70, k=pk(c, "never"))


def s_swivel(g, c):
    studio(g, c.gt, "#F29A3E", "#6B2A10")
    ph = c.gt * 1.6
    el = 1.0 if math.sin(ph) > 0 else -0.6
    er = -0.6 if math.sin(ph) > 0 else 1.0
    cat_face(g, 960, 640, 2.2, c.gt, "alert", ear_l=el, ear_r=er, look=(-0.8 if el > 0 else 0.8, 0))
    side = -1 if el > 0 else 1
    ring_wave(g, 960 + side * 700, 400, 40, 220, (c.gt * 1.4) % 1, PAL["yellow"])


# ------------------------------------------------------------------ round 5: drinking
def s_messy(g, c, cat=False):
    kitchen_floor(g, c.gt)
    if not cat:
        ph = (c.gt * 2) % 1
        dog_side(g, 760, FL + 150, 1.05, c.gt, head_down=1.0, expr="happy")
        bowl(g, 1180, FL + 140, 1.1, splash=ph, t=c.gt)
        for i in range(8):
            g.ellipse(1000 + i * 70, FL + 160 + (i % 3) * 20, 40, 10, "#7FCBEF", None, a=0.7)
        label(g, "WATER EVERYWHERE", 960, 170, 80, k=pk(c, "everywhere"))
    else:
        cat_side(g, 760, FL + 150, 1.1, c.gt, head_down=0.8, tongue=0.3 + 0.3 * math.sin(c.gt * 8))
        bowl(g, 1080, FL + 140, 0.9, t=c.gt)
        label(g, "BARELY MOVES", 960, 170, 80, PAL["cream"], k=pk(c, "barely"))


def slowmo_lab(g, t, wall):
    lab_room(g, t, wall, shade(wall, 0.6))


def s_mit(g, c):
    slowmo_lab(g, c.gt, "#BFDDF2")
    hs_camera(g, 420, FL + 60, 1.2, c.gt)
    cat_side(g, 1160, FL + 120, 1.0, c.gt, head_down=0.8, tongue=0.4 + 0.3 * math.sin(c.gt * 3), flip=True)
    bowl(g, 860, FL + 110, 0.8, t=c.gt)
    tag(g, "2010 · MIT, USA", 960, 90, on(c, "2010", frac=0.0))
    label(g, "SLOW MOTION", 1500, 220, 70, PAL["cream"], k=pk(c, "slow"))


def rec_frame(g, c, txt="SLOW MOTION"):
    with g.screen():
        g.rect(40, 40, W - 80, H - 80, None, "#FFFFFF", lw=6, a=0.6)
        if int(c.gt * 2) % 2 == 0:
            g.circle(100, 100, 16, "#FF3B3B", None)
        g.text("REC · " + txt, 300, 102, 40, "#FFFFFF", stroke=None)


def s_lap(g, c, mode="touch"):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE7C2", "#F6D2A2"))
    sp = {"touch": 0.35, "snap": 0.35, "fast": 4.0}[mode]
    lap_closeup(g, 900, 960, 1.22, c.gt, "cat", speed=sp)
    rec_frame(g, c, "SLOW MOTION" if mode != "fast" else "REAL SPEED")
    if mode == "touch":
        label(g, "NO SCOOP", 420, 260, 80, k=pk(c, "scoop"))
        label(g, "TIP TOUCHES", 1500, 260, 70, PAL["cream"], k=pk(c, "touches"))
        label(g, "WATER COLUMN", 1520, 420, 64, k=pk(c, "column"))
    elif mode == "snap":
        label(g, "SNAP!", 1520, 300, 110, k=pk(c, "closes"))
        arrow(g, 360, 300, 360, 640, col="#FF6B5B", k=on(c, "gravity"))
        label(g, "GRAVITY", 360, 240, 70, PAL["cream"], k=on(c, "gravity"))
    else:
        with g.screen():
            g.text("4 LAPS A SECOND", 1440, 260, 90, PAL["yellow"], sw=14, sc=pk(c, "four", frac=0.3) + 1e-3)


def s_vt(g, c, both=False):
    if not both:
        slowmo_lab(g, c.gt, "#F6D2B0")
        hs_camera(g, 380, FL + 60, 1.2, c.gt)
        dog_side(g, 1250, FL + 150, 0.95, c.gt, head_down=1.0, flip=True, expr="calm")
        bowl(g, 860, FL + 120, 0.9, splash=(c.gt * 1.5) % 1, t=c.gt)
        tag(g, "2015 · VIRGINIA TECH, USA", 960, 90, on(c, "2015", frac=0.0))
        label(g, "19 DOGS", 1500, 240, 80, PAL["cream"], k=pk(c, "nineteen"))
    else:
        g.fill_all(g.lgrad(0, 0, 0, H, "#FFE7C2", "#F6D2A2"))
        with g.clip(rect=(0, 0, W / 2 - 6, H)):
            lap_closeup(g, 520, 860, 0.62, c.gt, "cat", speed=0.4)
        with g.clip(rect=(W / 2 + 6, 0, W / 2, H)):
            lap_closeup(g, 1480, 860, 0.62, c.gt, "dog", speed=0.4)
        g.rect(W / 2 - 6, 0, 12, H, INK, None)
        label(g, "SAME TRICK!", W / 2, 200, 110, k=pk(c, "same"))


def s_doglap(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE7C2", "#F6D2A2"))
    lap_closeup(g, 1120, 900, 1.3, c.gt, "dog", speed=0.35)
    rec_frame(g, c)
    label(g, "CURLED BACK", 420, 300, 76, k=pk(c, "curls"))
    label(g, "BITE!", 1560, 260, 110, PAL["cream"], k=pk(c, "bites"))


def s_style(g, c):
    kitchen_floor(g, c.gt)
    dog_side(g, 600, FL + 150, 1.0, c.gt, head_down=1.0, expr="happy")
    bowl(g, 1000, FL + 140, 1.0, splash=(c.gt * 2) % 1, t=c.gt)
    cat_sit(g, 1550, FL + 160, 0.95, c.gt, "smug", look=(-0.8, 0.3))
    label(g, "SAME PHYSICS", 960, 170, 80, k=pk(c, "physics"))


# ------------------------------------------------------------------ round 6: who controls you
def s_puppy(g, c):
    studio(g, c.gt, "#F2B05A", "#7A3A1E")
    br = ease_io(clamp((lt(c) - 1.0) / 1.6))
    dog_face(g, 960, 560, 2.4, c.gt, "calm", brow=br, look=(0, -0.4), blink=0.0 if br > 0.2 else None)
    label(g, "PUPPY EYES", 960, 130, 90, k=pk(c, "puppy"))


def s_wolfdog(g, c):
    lab_room(g, c.gt, "#E8DCC8", "#8A6A44")
    kf_ = on(c, "found")
    dog_face(g, 620, 540, 1.6, c.gt, "calm", brow=0.6 * kf_)
    dog_face(g, 1320, 540, 1.6, c.gt, "calm", wolf=True)
    label(g, "DOG", 620, 900, 70, PAL["cream"], k=1)
    label(g, "WOLF", 1320, 900, 70, PAL["cream"], k=1)
    tag(g, "2019 · DOG AND WOLF FACES", 960, 90, on(c, "2019", frac=0.0))
    if kf_ > 0:
        for sd in (-1, 1):
            g.line([(620 + sd * 30 * 1.6, 540 - 76 * 1.6), (620 + sd * 85 * 1.6, 540 - 66 * 1.6)], "#FF3B3B", 14, a=0.5 + 0.5 * math.sin(c.gt * 8))
        cross(g, 1320, 330, 50, on(c, "wolves", n=0, frac=0.9))


def s_brow(g, c, baby=False):
    studio(g, c.gt, "#F2B05A", "#7A3A1E")
    br = 0.5 + 0.5 * math.sin(lt(c) * 2.2)
    dog_face(g, 760, 560, 2.0, c.gt, "calm", brow=br)
    arrow(g, 1200, 260, 950, 380, k=on(c, "lifts"))
    label(g, "INNER EYEBROW", 1450, 210, 64, k=on(c, "lifts"))
    kb = on(c, "baby's")
    if kb > 0:
        baby_face(g, 1500, 640, 1.1 * kb, c.gt)
        label(g, "LIKE A BABY", 1500, 860, 60, PAL["cream"], k=kb)


def s_shelter(g, c):
    shelter(g, c.gt)
    ka = on(c, "homes", frac=0.7)
    for i in range(3):
        col = SHELTER[i]
        if i == 1:
            dog_sit(g, 330 + i * 630 + 500 * ka, FL + 120, 0.75, c.gt, "calm", brow=0.9, col=col, tongue=0.0)
        else:
            dog_sit(g, 330 + i * 630, FL + 120, 0.75, c.gt, "calm", brow=0.0, col=col, tongue=0.0, seed=i)
        kennel_bars(g, i, ka if i == 1 else 0)
    if ka > 0:
        char2(g, "lena", 1300 + 300 * ka, FL + 120, 860, "smile", "hold", "hold", t=c.gt, view="3q", flip=True)
        heart(g, 1100 + 400 * ka, 260, 50, k=ka)
    label(g, "ADOPTED FASTER", 960, 130, 80, k=pk(c, "faster"))


def s_generations(g, c):
    studio(g, c.gt, "#E9A15A", "#6B3420")
    k = 0.2 + 0.8 * clamp(c.t / max(0.5, c.T * 0.8))
    for i in range(5):
        kk = clamp(k * 5 - i)
        if kk > 0:
            with g.group(kk):
                dog_face(g, 260 + i * 350, 560, 0.85, c.gt + i, "calm", brow=i / 4.0, wolf=(i == 0))
    arrow(g, 200, 880, 1720, 880, col=PAL["cream"], k=k)
    label(g, "THOUSANDS OF YEARS", 960, 980, 60, PAL["cream"], k=k)
    label(g, "SADDEST EYES WIN", 960, 160, 80, k=pk(c, "saddest"))


def s_purr(g, c):
    living(g, c.gt, 1.2)
    sofa(g, 960, FL + 20, 900)
    v = 4 * math.sin(c.gt * 60)
    cat_sit(g, 960 + v * 0.3, FL - 230, 1.3, c.gt, "happy", tail=0.3)
    for i in range(3):
        ph = (c.gt * 1.5 + i / 3) % 1
        g.path(f"M{700 - 80 * ph} {500 - 40 * ph} Q{650 - 100 * ph} 600 {700 - 80 * ph} {700 + 40 * ph}", None, PAL["coral"], lw=8, a=1 - ph)
        g.path(f"M{1220 + 80 * ph} {500 - 40 * ph} Q{1270 + 100 * ph} 600 {1220 + 80 * ph} {700 + 40 * ph}", None, PAL["coral"], lw=8, a=1 - ph)
    label(g, "THE PURR", 960, 150, 100, k=pk(c, "purr"))


def s_sussex(g, c):
    lab_room(g, c.gt, "#D9C2E8", "#7A4A9A")
    speaker(g, 260, FL - 120, 1.2, c.gt, on=1.0)
    for i, cid in enumerate(("lena", "student", "mira", "friend")):
        x = 640 + i * 330
        char2(g, cid, x, FL + 100, 700, "deadpan", "down", "down", t=c.gt + i, view="front")
        with g.at(x, FL + 100 - 700 * 0.92):
            headphones(g, 0, 0, 1.25)
    tag(g, "2009 · UNIVERSITY OF SUSSEX, UK", 960, 90, on(c, "2009", frac=0.0))
    label(g, "50 PEOPLE", 1500, 200, 80, k=pk(c, "fifty"))


def s_cry(g, c):
    studio(g, c.gt, "#B98AD6", "#3A1F5E")
    with g.screen():
        g.rect(160, 260, 1600, 460, "#0B1F33", INK, lw=8, r=20)
        ks = on(c, "cry", frac=0.4)
        wave_line(g, 200, 1720, 490, 120, 6, c.gt, PAL["coral"], w=8, spike=ks, spike_x=0.55)
        label(g, "HIDDEN CRY", 1100, 230, 70, k=ks)
        kb = on(c, "baby's")
        if kb > 0:
            baby_face(g, 1560, 880, 0.9 * kb, c.gt)
            cat_face(g, 360, 880, 0.9, c.gt, "happy")
            g.text("≈", 960, 880, 160, PAL["yellow"], sw=16, sc=kb)
        else:
            cat_face(g, 360, 880, 0.9, c.gt, "happy")


def s_urgent(g, c):
    lab_room(g, c.gt, "#D9C2E8", "#7A4A9A")
    for i, cid in enumerate(("lena", "student")):
        x = 360 + i * 360
        char2(g, cid, x, FL + 100, 760, "worried", "hold", "hold", t=c.gt + i, view="front")
        with g.at(x, FL + 100 - 760 * 0.92):
            headphones(g, 0, 0, 1.3)
    gauge(g, 1350, 650, 260, 0.25 + 0.7 * on(c, "urgent", frac=0.4), k=1.0)
    label(g, "URGENT", 1350, 300, 90, k=pk(c, "urgent"))
    tag(g, "EVEN NON-OWNERS", 1350, 980, on(c, "never"))


def s_draw(g, c):
    studio(g, c.gt, "#E9A15A", "#6B3420")
    with g.clip(rect=(0, 0, W / 2 - 6, H)):
        dog_face(g, 480, 600, 1.7, c.gt, "calm", brow=0.5 + 0.5 * math.sin(c.gt * 2))
    with g.clip(rect=(W / 2 + 6, 0, W / 2, H)):
        cat_face(g, 1440, 600, 1.8, c.gt, "happy")
        for i in range(2):
            ph = (c.gt * 1.5 + i / 2) % 1
            g.path(f"M{1120 - 60 * ph} 500 Q{1080 - 80 * ph} 600 {1120 - 60 * ph} 700", None, PAL["coral"], lw=8, a=1 - ph)
    g.rect(W / 2 - 6, 0, 12, H, INK, None)
    label(g, "A FACE FOR YOU", 480, 160, 64, PAL["cream"], k=pk(c, "face"))
    label(g, "A SOUND FOR YOU", 1440, 160, 64, PAL["cream"], k=pk(c, "sound"))


# ------------------------------------------------------------------ round 7: love
def s_secure_dog(g, c):
    door = on(c, "leaves") * (1 - on(c, "back", frac=0.8))
    strange_room(g, c.gt, door)
    chair(g, 760, FL)
    gone = on(c, "leaves", frac=0.5) > 0.6 and on(c, "back", frac=0.8) < 0.5
    back = on(c, "back", frac=0.8)
    if not gone:
        x = 760 if back <= 0 else 1650 - 700 * back
        char2(g, "lena", x, FL + 80, 860, "deadpan", "down", "hold", t=c.gt, view="3q", flip=back > 0)
    sad = gone
    dx = 1100 if not (back > 0) else 1100 + 300 * back
    dog_sit(g, dx, FL + 120, 0.8, c.gt, "sad" if sad else "happy", tongue=0.0 if sad else 0.5, brow=0.6 if sad else 0.0)
    toy(g, 1350, FL + 60, 0, 1.3)
    if sad:
        label(g, "UPSET", 1100, 200, 76, PAL["cream"], k=1)
    if back > 0.5:
        heart(g, 1250, 260, 50, k=back)


def s_securebond(g, c):
    studio(g, c.gt, "#7FD3B8", "#1F5E4A")
    dog_sit(g, 560, FL + 140, 0.9, c.gt, "happy", tongue=0.5)
    kb = on(c, "babies")
    if kb > 0:
        baby_face(g, 1360, 560, 1.3 * kb, c.gt)
    label(g, "SECURE BOND", 960, 150, 100, k=pk(c, "secure"))
    label(g, "SAME TEST AS BABIES", 1360, 880, 56, PAL["cream"], k=kb)


def s_fail(g, c):
    arena(g, c.gt)
    cat_sit(g, 960, FL + 60, 1.15, c.gt, "smug", look=(0, 0))
    stamp(g, "EXPECTED: FAIL", 960, 300, pk(c, "fail"))


def s_oregon(g, c, timer=False):
    strange_room(g, c.gt)
    chair(g, 760, FL)
    char2(g, "lena", 760, FL + 80, 860, "deadpan", "down", "hold", t=c.gt, view="3q")
    cat_sit(g, 1150, FL + 60, 0.6, c.gt, "alert", col=KIT, look=(-0.6, 0))
    tag(g, "2019 · OREGON STATE UNIVERSITY, USA", 960, 90, on(c, "2019", frac=0.0))
    if timer:
        with g.screen():
            for i, (txt, wd) in enumerate((("2 MIN WITH OWNER", "Two"), ("2 MIN ALONE", "alone"), ("REUNION", "back"))):
                k = pk(c, wd, frac=0.3 + 0.2 * i)
                if k > 0:
                    g.rc(1560, 300 + i * 120, 420, 90, PAL["navy"], PAL["cream"], lw=5, r=18)
                    g.text(txt, 1560, 304 + i * 120, 44, PAL["cream"], stroke=None, sc=k)


def s_kitten(g, c):
    strange_room(g, c.gt)
    chair(g, 760, FL)
    char2(g, "lena", 760, FL + 80, 860, "smile", "down", "hold", t=c.gt, view="3q")
    u = clamp(c.t / max(0.5, c.T))
    if u < 0.45:
        cat_side(g, 1300 - 400 * (u / 0.45), FL + 60, 0.55, c.gt, flip=True, walk=1, col=KIT, expr="happy")
    elif u < 0.6:
        cat_sit(g, 900, FL + 60, 0.6, c.gt, "happy", col=KIT)
        heart(g, 900, 500, 40, k=(u - 0.45) / 0.15)
    else:
        cat_side(g, 900 + 600 * ((u - 0.6) / 0.4), FL + 60, 0.55, c.gt, walk=1, col=KIT, expr="alert")
    toy(g, 1500, FL + 50, 2, 1.3)
    check(g, 1600, 260, 60, pk(c, "secure"))
    with g.screen():
        k = pk(c, "three")
        if k > 0:
            g.text("2 OUT OF 3", 420, 240, 100, PAL["yellow"], sw=16, depth=8, sc=k)


def s_share(g, c):
    studio(g, c.gt, "#7FD3B8", "#1F5E4A")
    with g.screen():
        cat_face(g, 330, 400, 0.6, c.gt, "happy", col=KIT)
        baby_face(g, 330, 700, 0.75, c.gt)
        bars(g, 620, 400, [("KITTENS", 64, KIT["fur"], "64 %"), ("BABIES", 65, "#F6D5BC", "65 %")], k=clamp(c.t / 1.6), maxv=100, w=900)
        g.text("SECURE BOND", 1150, 180, 70, PAL["cream"], sw=10)


def s_lap_love(g, c):
    living(g, c.gt, 1.3)
    sofa(g, 960, FL + 20, 900)
    char2(g, "lena", 960, FL - 60, 760, "deadpan", "hold", "hold", t=c.gt, view="front")
    cat_sit(g, 960, FL - 300, 0.55, c.gt, "happy" if (c.gt % 3) < 1.2 else "sleepy", tail=0.2)
    for i in range(3):
        heart(g, 820 + i * 140, 360 - 40 * ((c.gt * 0.5 + i * 0.3) % 1), 24, a=0.8, k=1)
    label(g, "QUIETLY", 960, 140, 90, k=pk(c, "quietly"))


def s_final(g, c):
    arena(g, c.gt)
    k5 = on(c, "five", frac=0.4); k4 = on(c, "four", frac=0.8)
    scoreboard(g, W / 2, 360, 5 if k5 > 0.5 else 4, 4 if k4 > 0.5 else 3, c.gt, "dog" if k5 > 0.5 and k4 < 0.5 else ("both" if k4 > 0.5 else None), 1.3)
    dog_sit(g, 360, FL + 160, 0.9, c.gt, "happy", tongue=0.7, paw=k5)
    cat_sit(g, 1560, FL + 20, 1.05, c.gt, "smug", paw=k4)
    label(g, "FINAL SCORE", W / 2, 120, 90, k=pk(c, "Final"))
    if k4 > 0:
        sparkles(g, c.gt, [(400, 200), (700, 650), (1200, 640), (1500, 220), (960, 720)], col=PAL["yellow"])


def s_recap(g, c):
    studio(g, c.gt, "#E9A15A", "#6B3420")
    dog_sit(g, 300, FL + 160, 0.75, c.gt, "happy", tongue=0.5)
    cat_sit(g, 1620, FL + 40, 0.85, c.gt, "smug")
    items_d = [("history", 0), ("brains", 1), ("words", 2)]
    items_c = [("ears", 0), ("drinking", 1), ("love", 2)]
    with g.screen():
        for wd, i in items_d:
            k = pk(c, wd, frac=0.2 + 0.1 * i)
            if k <= 0: continue
            y = 260 + i * 210
            with g.at(680, y, 0, k):
                g.circle(0, 0, 90, PAL["cream"], INK, lw=7)
                if i == 0: dna_tree(g, 0, 70, 0.22, 1.0, c.gt, n=3)
                elif i == 1: brain_side(g, 0, 10, 0.3)
                else: toy(g, 0, 0, 1, 1.2)
        for wd, i in items_c:
            k = pk(c, wd, frac=0.6 + 0.1 * i)
            if k <= 0: continue
            y = 260 + i * 210
            with g.at(1240, y, 0, k):
                g.circle(0, 0, 90, PAL["cream"], INK, lw=7)
                if i == 0:
                    ring_wave(g, 0, 0, 20, 70, (c.gt % 1), PAL["coral"])
                    cat_face(g, 0, 10, 0.28, c.gt, "alert")
                elif i == 1: bowl(g, 0, 40, 0.4)
                else: heart(g, 0, 0, 50)


def s_comments(g, c):
    living(g, c.gt)
    dog_sit(g, 560, FL + 130, 0.95, c.gt, "happy", tongue=0.6, look=(0.6, -0.3))
    cat_sit(g, 1360, FL + 10, 1.1, c.gt, "smug", look=(-0.6, -0.3))
    with g.screen():
        k = back_out(clamp(c.t / 0.4), 1.5)
        g.rc(W / 2, 220, 820, 170, "#FFFFFF", INK, lw=8, r=40)
        g.text("TEAM DOG or TEAM CAT?", W / 2, 228, 70, INK, stroke=None, sc=k)
        label(g, "TELL US IN THE COMMENTS", W / 2, 400, 56, PAL["cream"], k=pk(c, "comments"))


def s_loop(g, c):
    living(g, c.gt)
    sofa(g, 1180, FL + 20, 760)
    ear = 0.6 + 0.4 * math.sin(min(c.t, 0.9) * 3.5)
    kd = on(c, "deciding", frac=0.85)
    cat_sit(g, 1180, FL - 230, 1.15, c.gt, "smug" if kd > 0.5 else "deadpan", ear_l=ear, ear_r=-0.2, look=(-0.6, 0), tail=0.6)
    lena_call(g, c, 430, 980, on(c, "call"))
    label(g, "...DECIDING", 1180, 180, 80, k=pk(c, "deciding", frac=0.85))


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

# cold open + round 1 (ch0)
P("O01", s_hook, (0, "It"), cam=Z(1.03, 1.08, (960, 560)), tr="cut", music="playful", sfx=[(0.0, "meow", 0.35), (0.05, "whoosh", 0.4)])
P("O01", s_nocome, ("It", 1), cam=Z(1.0, 1.06, (960, 520)), sfx=[("come", "bloop", 0.4)])
P("O02", s_muscle, (0, "face"), cam=Z(1.0, 1.05, (960, 560)), sfx=[("dog", "bark", 0.3)])
P("O02", lambda g, c: s_muscle(g, c, True), ("face", 1), cam=Z(1.0, 1.06, (960, 500)), sfx=[("muscle", "sting", 0.35)])
P("O03", s_versus, (0, "Seven"), cam=Z(1.0, 1.05, (960, 560)), music="match", sfx=[(0.0, "ring_bell", 0.45), ("versus", "drum_hit", 0.4)])
P("O03", lambda g, c: s_versus(g, c, True), ("Seven", 1), cam=Z(1.0, 1.04, (960, 480)), sfx=[("scoreboard", "ding", 0.4)])
P("O04", s_science, cam=Z(1.0, 1.06, (960, 480)), sfx=[("opinions", "bloop", 0.35), ("science", "chime", 0.4), ("settle", "crowd_cheer", 0.25)])
V.pause["O04"] = 0.5
P("H01", round_card(1, "WHO MOVED IN FIRST?", 0, 0), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("H02", s_dna, (0, "five"), cam=Z(1.0, 1.04, (960, 600)), music="story", sfx=[("DNA", "shimmer", 0.35)])
P("H02", s_dna, ("five", "when"), cam=Z(1.0, 1.05, (960, 560)), music="story", sfx=[("DNA", "shimmer", 0.35)])
P("H02", s_dna, ("when", 1), cam=Z(1.12, 1.18, (1300, 440)))
P("H03", s_wolf_dog, cam=Z(1.0, 1.04, (960, 560)), sfx=[(0.3, "footsteps", 0.2)])
P("H04", s_cat_enters, cam=Z(1.0, 1.05, (1100, 560)), music="playful", sfx=[(0.2, "footsteps", 0.2), ("invited", "meow", 0.3)])
P("H05", s_village, (0, "Grain"), cam=Z(1.0, 1.04, (960, 560)), music="story", sfx=[(0.2, "wind", 0.2)])
P("H05", s_village, ("Grain", 1), cam=Z(1.05, 1.1, (1100, 600)), sfx=[("mice", "rat_squeak", 0.2), ("cats", "pop", 0.35)])
P("H06", s_wildcat, (0, "and"), cam=Z(1.0, 1.05, (1000, 600)), sfx=[("hunting", "ding", 0.3)])
P("H06", s_to_sofa, ("and", 1), cam=Z(1.0, 1.06, (960, 540)), sfx=[("sofa", "pop", 0.35)])
P("H07", s_cat_enters, (0, "Point"), cam=Z(1.06, 1.1, (1000, 560)), music="playful")
P("H07", s_verdict(1, 0, "dog", "GOT HERE FIRST"), ("Point", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("Point", "ding", 0.45), ("Point", "crowd_cheer", 0.2)])
V.pause["H07"] = CH_PAUSE
# round 2 brains (ch1)
P("B01", round_card(2, "WHO IS SMARTER?", 1, 0), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("B02", s_vanderbilt, (0, "at"), cam=Z(1.12, 1.16, (1150, 450)), music="story")
P("B02", s_vanderbilt, ("at", "counted"), cam=Z(1.0, 1.04, (900, 560)), music="story")
P("B02", lambda g, c: s_vanderbilt(g, c, True), ("counted", 1), cam=Z(1.0, 1.03, (1100, 520)), sfx=[("counted", "click", 0.35)])
P("B03", s_cortex, cam=Z(1.0, 1.06, (960, 560)), music="curious", sfx=[("cortex", "shimmer", 0.35)])
P("B04", s_dots, (0, "A#1"), cam=Z(1.0, 1.03, (700, 420)))
P("B04", s_dots, ("A#1", "More"), cam=Z(1.0, 1.03, (960, 540)), sfx=[("cat", "pop", 0.35), ("dog", "pop", 0.35)])
P("B04", s_dots, ("More", 1), cam=Z(1.1, 1.14, (1300, 600)), sfx=[("cat", "pop", 0.35), ("dog", "pop", 0.35), ("twice", "sting", 0.4)])
P("B05", s_bear, (0, "with"), cam=Z(1.0, 1.04, (960, 560)), music="tension", sfx=[("twist", "drum_hit", 0.4), ("ten", "boing", 0.35)])
P("B05", s_bear, ("with", 1), cam=Z(1.06, 1.1, (960, 500)), sfx=[("same", "ding", 0.4)])
P("B06", s_bigger, cam=Z(1.0, 1.04, (960, 560)), music="curious")
P("B07", s_clever, (0, "But"), cam=Z(1.0, 1.05, (1000, 560)), music="playful", sfx=[(0.2, "creak", 0.3)])
P("B07", s_verdict(2, 0, "dog", "BRAIN CELLS"), ("But", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("dog", "ding", 0.45)])
V.pause["B07"] = CH_PAUSE
# round 3 names (ch2)
P("N01", round_card(3, "WHO UNDERSTANDS YOU?", 2, 0), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("N02", s_1022, cam=Z(1.0, 1.05, (1000, 560)), music="playful", sfx=[(0.3, "bark", 0.25), ("twenty-two", "ding", 0.4)])
P("N03", s_pilley, (0, "Ask"), cam=Z(1.0, 1.04, (800, 560)), music="story")
P("N03", s_pilley, ("Ask", 1), cam=Z(1.0, 1.03, (960, 560)), sfx=[("name", "pop", 0.35), ("back", "ding", 0.35)])
P("N04", s_newtoy, (0, "and"), cam=Z(1.0, 1.04, (1000, 560)), sfx=[("added", "shimmer", 0.35)])
P("N04", s_newtoy, ("and", "heard"), cam=Z(1.0, 1.04, (900, 500)))
P("N04", s_newtoy, ("heard", "She"), cam=Z(1.0, 1.04, (1000, 560)), sfx=[("added", "shimmer", 0.35)])
P("N04", s_newtoy, ("She", 1), cam=Z(1.04, 1.08, (1000, 560)), sfx=[("picked", "pop", 0.35), ("worked", "chime", 0.4)])
P("N05", s_notsofast, cam=Z(1.0, 1.06, (1000, 520)), music="playful", sfx=[("Not", "drum_hit", 0.35)])
P("N06", s_tokyo, (0, "one"), cam=Z(1.0, 1.04, (960, 560)), music="curious")
P("N06", s_tokyo, ("one", 1), cam=Z(1.08, 1.12, (1100, 520)), music="curious", sfx=[(0.4, "pop", 0.3), (1.2, "pop", 0.3)])
P("N07", lambda g, c: s_tokyo(g, c, "words"), (0, "But"), cam=Z(1.0, 1.03, (960, 560)))
P("N07", lambda g, c: s_tokyo(g, c, "name"), ("But", "Even"), cam=Z(1.06, 1.12, (960, 520)), sfx=[("name", "sting", 0.35)])
P("N07", lambda g, c: s_tokyo(g, c, "stranger"), ("Even", 1), cam=Z(1.0, 1.04, (1100, 540)), sfx=[("stranger", "ding", 0.35)])
P("N08", s_nomove, cam=Z(1.0, 1.04, (960, 560)), sfx=[("walk", "bloop", 0.35), ("meow", "bloop", 0.35)])
P("N09", s_heard, (0, "A"), cam=Z(1.0, 1.05, (1000, 560)), music="warm")
P("N09", s_verdict(3, 0, "dog", "WORDS (BUT THE CAT LISTENED)"), ("A", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("dog", "ding", 0.45)])
V.pause["N09"] = CH_PAUSE
# round 4 senses (ch3)
P("S01", round_card(4, "SENSES", 3, 0), (0, "And"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("S01", s_nose, ("And", 1), cam=Z(1.0, 1.04, (900, 560)), music="playful", sfx=[(0.2, "footsteps", 0.2)])
P("S02", s_receptors, (0, "Yours"), cam=Z(1.0, 1.03, (960, 540)), music="curious", sfx=[("three", "pop", 0.35)])
P("S02", s_receptors, ("Yours", 1), cam=Z(1.08, 1.12, (1100, 640)), music="curious", sfx=[("three", "pop", 0.35), ("six", "pop", 0.35)])
P("S03", s_detect, cam=Z(1.0, 1.05, (960, 560)), sfx=[(0.3, "footsteps", 0.2)])
P("S04", s_ears, cam=Z(1.0, 1.06, (960, 560)), music="tension", sfx=[("weapon", "sting", 0.4)])
P("S05", s_heffner, (0, "tested"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("S05", s_heffner, ("tested", 1), cam=Z(1.15, 1.2, (960, 440)), music="story", sfx=[(0.4, "shimmer", 0.3)])
P("S06", s_freq, cam=Z(1.0, 1.03, (960, 540)), sfx=[("forty-five", "pop", 0.35), ("twice", "ding", 0.35)])
P("S07", lambda g, c: s_freq(g, c, True), (0, "One"), cam=Z(1.0, 1.04, (1100, 560)), music="curious", sfx=[("eighty-five", "pop", 0.4)])
P("S07", lambda g, c: s_freq(g, c, True), ("One", 1), cam=Z(1.1, 1.16, (1300, 700)), music="curious", sfx=[("eighty-five", "pop", 0.4), ("widest", "chime", 0.4)])
P("S08", s_squeak, cam=Z(1.0, 1.05, (1000, 600)), sfx=[("squeaks", "rat_squeak", 0.15)])
P("S09", s_swivel, (0, "Nose"), cam=Z(1.0, 1.05, (960, 560)), sfx=[(0.3, "whoosh_soft", 0.3)])
P("S09", s_verdict(4, 1, "both", "NOSE TO THE DOG · EARS TO THE CAT"), ("Nose", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("One", "ding", 0.45)])
V.pause["S09"] = CH_PAUSE
# round 5 drinking (ch4)
P("D01", round_card(5, "WHO DRINKS BETTER?", 4, 1), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("D02", s_messy, (0, "Watch#1"), cam=Z(1.0, 1.05, (960, 600)), music="playful", sfx=[(0.3, "splash", 0.3)])
P("D02", lambda g, c: s_messy(g, c, True), ("Watch#1", 1), cam=Z(1.0, 1.05, (960, 600)), sfx=[("barely", "lap", 0.35)])
P("D03", s_mit, (0, "and"), cam=Z(1.0, 1.04, (900, 560)), music="story")
P("D03", s_mit, ("and", 1), cam=Z(1.12, 1.18, (1000, 600)), music="story", sfx=[("slow", "click", 0.35)])
P("D04", lambda g, c: s_lap(g, c, "touch"), (0, "The#1"), cam=Z(1.0, 1.04, (960, 560)), music="curious")
P("D04", lambda g, c: s_lap(g, c, "touch"), ("The#1", "so"), cam=Z(1.0, 1.04, (960, 560)), music="curious", sfx=[("touches", "lap", 0.3)])
P("D04", lambda g, c: s_lap(g, c, "touch"), ("so", 1), cam=Z(1.15, 1.2, (1000, 600)))
P("D05", lambda g, c: s_lap(g, c, "snap"), (0, "before"), cam=Z(1.05, 1.1, (960, 560)))
P("D05", lambda g, c: s_lap(g, c, "snap"), ("before", 1), cam=Z(1.0, 1.03, (700, 560)), sfx=[("closes", "pop", 0.4)])
P("D06", lambda g, c: s_lap(g, c, "fast"), cam=Z(1.0, 1.03, (960, 560)), sfx=[(0.0, "lap", 0.4)])
P("D07", s_vt, (0, "And"), cam=Z(1.0, 1.04, (900, 560)), music="story", sfx=[("nineteen", "pop", 0.35)])
P("D07", lambda g, c: s_vt(g, c, True), ("And", 1), cam=Z(1.0, 1.03, (960, 560)), music="tension", sfx=[("same", "sting", 0.45)])
P("D08", s_doglap, (0, "pulls"), cam=Z(1.0, 1.05, (1000, 600)), music="curious", sfx=[("slams", "splash", 0.35)])
P("D08", s_doglap, ("pulls", 1), cam=Z(1.12, 1.18, (1100, 650)), music="curious", sfx=[("slams", "splash", 0.35), ("bites", "pop", 0.4)])
P("D09", s_style, (0, "Same"), cam=Z(1.0, 1.04, (960, 560)), music="playful", sfx=[(0.3, "splash", 0.25)])
P("D09", s_style, ("Same", "Point"), cam=Z(1.0, 1.05, (960, 560)), music="playful", sfx=[(0.3, "splash", 0.25)])
P("D09", s_verdict(4, 2, "cat", "NEATNESS"), ("Point", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("Point", "ding", 0.45), ("Point", "meow", 0.2)])
V.pause["D09"] = CH_PAUSE
# round 6 who controls you (ch5)
P("C01", round_card(6, "WHO CONTROLS YOU?", 4, 2), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "ring_bell", 0.45)])
P("C02", s_puppy, cam=Z(1.0, 1.08, (960, 520)), music="warm", sfx=[("puppy", "shimmer", 0.35)])
P("C03", s_wolfdog, (0, "found"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("C03", s_wolfdog, ("found", 1), cam=Z(1.12, 1.18, (700, 440)), sfx=[("muscle", "ding", 0.4)])
P("C04", s_brow, (0, "It#1"), cam=Z(1.0, 1.04, (900, 560)), music="curious")
P("C04", lambda g, c: s_brow(g, c, True), ("It#1", 1), cam=Z(1.0, 1.04, (1000, 560)), sfx=[("baby's", "pop", 0.35)])
P("C05", s_shelter, cam=Z(1.0, 1.04, (960, 560)), sfx=[("faster", "chime", 0.4)])
P("C06", lambda g, c: s_wolfdog(g, c), (0, "thousands"), cam=Z(1.1, 1.14, (700, 500)), music="story")
P("C06", s_generations, ("thousands", 1), cam=Z(1.0, 1.04, (960, 560)), music="story", sfx=[("thousands", "whoosh_soft", 0.35)])
P("C07", s_purr, cam=Z(1.0, 1.06, (960, 540)), music="playful", sfx=[("purr", "purr", 0.45)])
P("C08", s_sussex, (0, "and"), cam=Z(1.0, 1.04, (960, 560)), music="story", sfx=[(0.3, "purr", 0.25)])
P("C08", s_sussex, ("and", 1), cam=Z(1.08, 1.14, (1100, 520)), sfx=[("fifty", "pop", 0.35)])
P("C09", s_cry, (0, "at"), cam=Z(1.0, 1.04, (960, 560)), music="tension", sfx=[("cry", "sting", 0.35)])
P("C09", s_cry, ("at", 1), cam=Z(1.06, 1.1, (1100, 700)), music="tension", sfx=[("cry", "sting", 0.35), ("baby's", "ding", 0.35)])
P("C10", s_urgent, cam=Z(1.0, 1.04, (1000, 560)), sfx=[("urgent", "drum_hit", 0.4)])
P("C11", s_draw, (0, "That's"), cam=Z(1.0, 1.03, (960, 560)), music="warm")
P("C11", s_verdict(5, 3, "both", "IT'S A DRAW"), ("That's", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("draw", "ding", 0.45)])
V.pause["C11"] = CH_PAUSE
# round 7 love + verdict (ch6)
P("L01", round_card(7, "WHO LOVES YOU?", 5, 3), tr="flash", cam=Z(1.0, 1.04, (960, 540)), music="cozy", sfx=[(0.0, "ring_bell", 0.45)])
P("L02", s_secure_dog, cam=Z(1.0, 1.03, (1000, 560)), music="cozy", sfx=[("leaves", "door", 0.35), ("back", "bark", 0.25)])
P("L03", s_securebond, cam=Z(1.0, 1.05, (960, 560)), sfx=[("secure", "chime", 0.35)])
P("L04", s_fail, cam=Z(1.0, 1.06, (960, 520)), music="playful", sfx=[("fail", "drum_hit", 0.4)])
P("L05", s_oregon, (0, "Two"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("L05", lambda g, c: s_oregon(g, c, True), ("Two", 1), cam=Z(1.0, 1.03, (1100, 540)), sfx=[("alone", "door", 0.3), ("back", "pop", 0.35)])
P("L06", s_kitten, cam=Z(1.0, 1.04, (960, 560)), music="cozy", sfx=[("greeted", "meow", 0.25), ("secure", "chime", 0.4)])
P("L07", s_share, cam=Z(1.0, 1.03, (960, 540)), sfx=[(0.4, "pop", 0.35), (1.0, "pop", 0.35)])
P("L08", s_lap_love, (0, "Point"), cam=Z(1.0, 1.06, (960, 500)), music="cozy", sfx=[(0.3, "purr", 0.3)])
P("L08", s_verdict(5, 4, "cat", "BIGGEST SURPRISE"), ("Point", 1), cam=Z(1.0, 1.04, (960, 520)), music="match", sfx=[("Point", "ding", 0.45)])
P("E01", s_final, tr="flash", cam=Z(1.0, 1.04, (960, 500)), sfx=[(0.0, "ring_bell", 0.45), ("four", "crowd_cheer", 0.35)])
P("E02", s_recap, cam=Z(1.0, 1.03, (960, 540)), music="warm",
  sfx=[("history", "pop", 0.3), ("brains", "pop", 0.3), ("words", "pop", 0.3), ("ears", "pop", 0.3), ("drinking", "pop", 0.3), ("love", "pop", 0.3)])
P("E03", s_comments, cam=Z(1.0, 1.05, (960, 560)), sfx=[("comments", "pop", 0.4)])
P("E04", s_loop, cam=Z(1.03, 1.08, (960, 560)), music="playful", sfx=[(0.1, "meow", 0.3), ("deciding", "bloop", 0.35)])
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
                    keep.append(e); continue
                if not (sh["start"] - 0.05 <= t < sh["start"] + sh["dur"]):
                    tgt = [x for x in V.shots if x["line"] == sh["line"] and x["start"] - 0.05 <= t < x["start"] + x["dur"]]
                    if tgt:
                        tgt[0]["sfx"] = tgt[0]["sfx"] + [e]
                        continue
            keep.append(e)
        sh["sfx"] = keep


_fix_sfx()

END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line=V.shots[-1]["line"], fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "Cats vs dogs: 7 rounds of real science"), ("H01", "Round 1: Who moved in with us first?"),
            ("B01", "Round 2: Are dogs smarter than cats? (brain cells)"), ("N01", "Round 3: Do cats know their names?"),
            ("S01", "Round 4: Dog nose vs cat ears"), ("D01", "Round 5: How cats and dogs drink water"),
            ("C01", "Round 6: Puppy eyes vs the cat's purr"), ("L01", "Round 7: Do cats love their owners?"), ("E01", "Final score")]


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
        V.render(str(EP / "final/B-007.mp4"))
