"""B-005 cut Shorts, re-composed vertically (1080x1920) with their own hooks (not crops): frame-1 rule, answer at the end, loop, corner badge.
python episodes/B-005-annoying-science/shorts/make_short.py <C1|C2> sheet|qa|times <t,..> <out>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, arrow, burst, steam
from flat_annoy import *

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-toast", "C2": "C2-spaghetti"}
EP = HERE / DIRS[SID]
SKIN = "#D8A580"
FL = 1500
TY, TX1 = 1050, 900          # tabletop y and right edge


def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def label(g, txt, x, y, size=96, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def check(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, PAL["mint"], INK, lw=r * 0.12)
        g.line([(-0.45 * r, 0), (-0.1 * r, 0.35 * r), (0.5 * r, -0.35 * r)], INK, r * 0.2)


def studio(g, t, a="#1590A0", b="#0B3F4C"):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def kitchen_v(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#CFE8EE", "#A9D3DC"))
    with g.layer(0.5):
        for i in range(-1, 10):
            for j in range(14):
                g.rect(i * 130 + (65 if j % 2 else 0), j * 110, 126, 106, "#DDF0F3", None, r=8, a=0.8)
        g.rect(620, 260, 380, 360, "#FFE9A8", INK, lw=10, r=10)
        g.circle(860, 380, 64, "#FFC93C", None, a=0.9)
        g.line([(810, 260), (810, 620)], INK, 8); g.line([(620, 440), (1000, 440)], INK, 8)
    g.rect(-100, FL, W + 200, H, "#E7C9A0", INK, lw=8)
    for i in range(-1, 10):
        g.line([(i * 170, FL), (i * 170 - 120, H)], "#D4B387", 5)
    g.glow(820, 420, 600, "#FFE08A", 0.22)


def fall(g, k, x0=TX1 - 60, y0=TY - 30, floor=FL - 30, turns=0.5, push=0.0, s=1.6):
    kk = clamp(k)
    x = x0 + (80 + push * 380) * kk
    y = y0 + (floor - y0) * kk ** 2
    toast(g, x, y, s, turns * TAU * ease_in(min(1, kk * 1.05)))
    return x, y


# ------------------------------------------------------------------ C1 toast
def c1_hook(g, c):
    """Frame 1 = motion already happening: toast tumbling off the table; the loop's last shot ends just before this."""
    kitchen_v(g, c.gt)
    char2(g, "modern", 230, 2000, 1250, "shocked", "up", "point", t=c.gt, prop=False)
    table_side(g, 640, TY, 560, "#C97B4A", FL - TY - 36)
    plate(g, 640, TY - 6, 300)
    k = seg(c.gt, -0.3, 1.2)
    x, y = fall(g, k)
    if k >= 1:
        burst(g, x, y + 10, 70, 170, 10, PAL["cream"], 10, k=seg(c.gt, 0.9, 0.3))


def c1_fault(g, c):
    kitchen_v(g, c.gt)
    table_side(g, 540, TY, 760, "#C97B4A", FL - TY - 36)
    toast(g, 820, FL - 26, 1.6, math.pi)
    char2(g, "physicist", 300, 2000, 1300, "smug", "down", "point", t=c.gt)
    ruler_v(g, 960, TY, FL, "", k=ease_out(seg(c.t, tw(c, "table's") - 0.4, 0.5)))
    label(g, "THE TABLE?!", W / 2, 640, 120, "#FF6B5B", k=pop(c.t, tw(c, "fault") - 0.1, 0.3))


def c1_tip(g, c):
    kitchen_v(g, c.gt)
    table_side(g, 320, TY, 700, "#C97B4A", FL - TY - 36)
    k = ease_io(seg(c.t, 0.1, c.T - 0.4))
    for j in range(5):
        with g.group(0.18 + 0.16 * j):
            fall(g, k * (j + 1) / 5 * 0.6, x0=640 - 40)
    label(g, "IT SPINS", W / 2, 620, 120, k=pop(c.t, tw(c, "spin") - 0.1, 0.3))


def c1_half(g, c):
    studio(g, c.gt)
    table_side(g, 300, 700, 520, "#C97B4A", 760)
    g.line([(-100, 1496), (W + 100, 1496)], PAL["cream"], 8)
    k = ease_io(seg(c.t, 0.2, c.T * 0.8))
    for j in range(7):
        kj = j / 6
        if kj > k + 1e-3: break
        with g.group(0.35 if kj < k - 0.05 else 1.0):
            toast(g, 600 + 200 * kj, 674 + (1470 - 674) * kj ** 2, 0.9, math.pi * ease_in(kj))
    label(g, "½ TURN", W / 2, 380, 150, k=pop(c.t, tw(c, "half") - 0.1, 0.3))


def c1_flip(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    k = ease_io(seg(c.t, tw(c, "flips") - 0.2, 0.9))
    toast(g, 540, 960, 3.0, math.pi * k)
    label(g, "BUTTER DOWN", W / 2, 1480, 120, PAL["cream"], k=pop(c.t, tw(c, "bottom") - 0.1, 0.3))


def c1_tall(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    floor = 1800
    g.line([(-100, floor), (W + 100, floor)], INK, 10)
    kg = ease_io(seg(c.t, 0.1, 0.8))
    top = lerp(1300, 420, kg)
    table_side(g, 380, top, 420, "#C97B4A", floor - top - 36)
    char2(g, "modern", 860, floor, 650, "shocked", "up", "down", t=c.gt, prop=False, flip=True)
    kf = seg(c.t, tw(c, "meters") - 0.6, 1.4)
    if kf <= 0:
        toast(g, 460, top - 26, 0.8)
    else:
        x, y = fall(g, kf, x0=560, y0=top - 26, floor=floor - 20, turns=1.0, s=0.8)
        if kf >= 1: check(g, x, y - 140, 56, seg(c.t, tw(c, "meters") + 0.9, 0.3))
    ruler_v(g, 120, top, floor, "", k=ease_out(seg(c.t, tw(c, "three") - 0.4, 0.5)))
    label(g, "3 METERS", W / 2, 260, 130, k=pop(c.t, tw(c, "meters") - 0.1, 0.3))


def c1_fast(g, c):
    kitchen_v(g, c.gt)
    table_side(g, 320, TY, 700, "#C97B4A", FL - TY - 36)
    k = seg(c.t, tw(c, "fast") - 0.3, 0.8)
    x = 600 + 520 * ease_out(k); y = TY - 30 + (FL - 30 - TY + 30) * ease_in(k)
    toast(g, x, y, 1.4, 0.4 * ease_in(k))
    if k >= 1: check(g, x - 40, y - 160, 56, seg(c.t, tw(c, "fast") + 0.6, 0.3))


def c1_end(g, c):
    """Loops into frame 1: toast at the table edge, the hand about to push it."""
    kitchen_v(g, c.gt)
    char2(g, "modern", 230, 2000, 1250, "curious" if c.t < tw(c, "tall") else "suspicious", "hip", "point", t=c.gt, prop=False)
    table_side(g, 640, TY, 560, "#C97B4A", FL - TY - 36)
    plate(g, 640, TY - 6, 300)
    x = lerp(640, TX1 - 70, ease_io(seg(c.t, 0.3, c.T - 0.3)))
    toast(g, x, TY - 30, 1.6, 0.0)
    qmark(g, 700, 700, 170, PAL["coral"], 0.1, pop(c.t, tw(c, "tall") - 0.2, 0.3))


# ------------------------------------------------------------------ C2 spaghetti
def kitchen_pasta(g, t):
    kitchen_v(g, t)
    g.rect(700, 1250, 300, 220, "#9AA3AD", INK, lw=8, r=12)
    steam(g, t, 850, 1230, 3, 160)


def bend_hands(g, b, x0=200, x1=880, y=840, twist=0.0, s=1.4):
    spaghetti(g, x0, y, x1, y, b, w=22, twist=twist)
    fist(g, x0, y + 30, s); fist(g, x1, y + 30, s)


def burst3(g, k, x0=200, x1=880, y=840):
    e = ease_out(k)
    spaghetti(g, x0, y, x0 + 260, y - 100 - 80 * e, 0, w=22)
    with g.at(540, y - 160 - 300 * e, 3 * e):
        spaghetti(g, -90, 0, 90, 0, 0, w=22)
    spaghetti(g, x1 - 260, y - 100 - 80 * e, x1, y, 0, w=22)
    burst(g, 540, y - 120, 50, 180, 10, PAL["cream"], 10, k=k)
    fist(g, x0, y + 30, 1.4); fist(g, x1, y + 30, 1.4)


def c2_hook(g, c):
    kitchen_pasta(g, c.gt)
    char2(g, "modern", 540, 2300, 1350, "shocked", "down", "down", t=c.gt, prop=False)
    tb = tw(c, "can't") - 0.4
    k = seg(c.t, tb, 0.5)
    if k <= 0:
        bend_hands(g, 120 + 140 * ease_io(clamp((c.t + 0.4) / max(0.5, tb + 0.4))))
    else:
        burst3(g, k)
    label(g, "3 PIECES!", W / 2, 1750, 130, "#FF6B5B", k=pop(c.t, tw(c, "can't") - 0.1, 0.3))


def c2_three(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    for i in range(3):
        k = back_out(seg(c.t, 0.1 + i * 0.25, 0.35), 1.6)
        if k <= 0: continue
        with g.at(540, 640 + i * 260, 0.2 * (i - 1), k):
            spaghetti(g, -200 + 40 * i, 0, 200 - 40 * i, 0, 0, w=26)
    label(g, "RICHARD FEYNMAN", W / 2, 1520, 90, PAL["cream"], k=pop(c.t, tw(c, "Feynman") - 0.1, 0.3))
    label(g, "STUMPED", W / 2, 1640, 90, PAL["yellow"], k=pop(c.t, tw(c, "explain") - 0.1, 0.3))


def wave_pieces(g, c, t0, second=False, y=960):
    for side in (-1, 1):
        x_in, x_out = 540 + side * 24, 540 + side * 470
        ph = (c.t - t0) * 2.2
        pts = []
        for i in range(25):
            u = i / 24
            wave = 80 * math.exp(-((u - (ph % 1.3)) ** 2) / 0.01) * (1.5 if second else 1)
            pts.append((lerp(x_in, x_out, u), y - wave))
        g.line(pts, INK, 31); g.line(pts, PASTA, 22)


def c2_spring(g, c):
    studio(g, c.gt)
    t0 = tw(c, "snaps") - 0.2
    if c.t < t0:
        spaghetti(g, 70, 960, 1010, 960, 200, w=22)
    else:
        wave_pieces(g, c, t0)
        burst(g, 540, 940, 30, 150, 12, PAL["cream"], 10, k=seg(c.t, t0, 0.25))
    label(g, "SPRINGS BACK", W / 2, 560, 110, k=pop(c.t, tw(c, "springs") - 0.1, 0.3))


def c2_wave(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    wave_pieces(g, c, -0.5, True)
    if c.t > tw(c, "again") - 0.3:
        k = seg(c.t, tw(c, "again") - 0.3, 0.3)
        for side in (-1, 1):
            burst(g, 540 + side * 260, 900, 30, 130, 10, PAL["yellow"], 8, k=k)
    label(g, "BENDING WAVE", W / 2, 560, 110, PAL["cream"], k=pop(c.t, tw(c, "wave") - 0.1, 0.3))
    label(g, "SNAP AGAIN!", W / 2, 1380, 120, "#FF6B5B", k=pop(c.t, tw(c, "again") - 0.1, 0.3))


def c2_mit(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2C3E50", "#1B2836"))
    g.rect(40, 1100, 1000, 50, "#9AA3AD", INK, lw=8, r=8)
    kt = ease_io(seg(c.t, tw(c, "twist") - 0.2, 1.2))
    kb = ease_io(seg(c.t, tw(c, "bend") - 0.2, 0.8))
    gap = 820 - 220 * kb + 900 * (1 - ease_out(seg(c.gt - c.sh["line_start"], 0.0, 0.6)))
    xa, xb = 540 - gap / 2, 540 + gap / 2
    spaghetti(g, xa, 960, xb, 960, 180 * kb, w=22, twist=kt)
    for x, rot in ((xa, 0), (xb, kt * TAU * 0.95)):
        g.rc(x, 1030, 100, 140, "#3E7CB1", INK, lw=8, r=10)
        with g.at(x, 960, rot):
            g.rc(0, 0, 80, 80, "#C9CED6", INK, lw=7, r=8)
            g.line([(0, -30), (0, 30)], "#FF6B5B", 8)
    label(g, "2018 · MIT", W / 2, 420, 100, PAL["cream"], k=pop(c.t, tw(c, "2018") - 0.1, 0.3))
    if kt <= 0.05:
        qmark(g, 540, 1350, 200, PAL["yellow"], 0.1 * math.sin(c.gt * 3), pop(c.t, tw(c, "trick") - 0.1, 0.3))
    if kt > 0.05:
        label(g, f"{int(342 * kt)}°", W / 2, 640, 130, k=1.0)


def c2_clean(g, c):
    kitchen_pasta(g, c.gt)
    char2(g, "modern", 540, 2300, 1350, "smug", "down", "down", t=c.gt, prop=False)
    k = seg(c.t, tw(c, "cleanly") - 0.5, 0.4)
    if k <= 0:
        bend_hands(g, 200, twist=0.95)
    else:
        e = ease_out(k)
        spaghetti(g, 200, 840, 530, 700 - 30 * e, 0, w=22)
        spaghetti(g, 550, 700 - 30 * e, 880, 840, 0, w=22)
        burst(g, 540, 700, 30, 120, 10, PAL["cream"], 8, k=k)
        fist(g, 200, 870, 1.4); fist(g, 880, 870, 1.4)
        check(g, 540, 560, 70, seg(c.t, tw(c, "two") - 0.1, 0.3))
    label(g, "IN TWO!", W / 2, 1750, 140, PAL["mint"], k=pop(c.t, tw(c, "two") - 0.1, 0.3))
    if c.t > c.T - 0.5:                                  # loop: cross-fade into the frame-1 picture
        u = ease_io(seg(c.t, c.T - 0.5, 0.5))
        with g.group(u):
            kitchen_pasta(g, c.gt)
            char2(g, "modern", 540, 2300, 1350, "shocked", "down", "down", t=c.gt, prop=False)
            bend_hands(g, 120 * u)


def build():
    if SID == "C1":
        V = Video(EP, title=("NOT BAD", "LUCK?"), cap_y=0.72, music="playful", sid="B005C1", captions=False)
        V.shot("H1", c1_hook, (0, "and"), tr="cut", sfx=[(0.0, "whoosh", 0.45), (0.9, "thud", 0.5)])
        V.shot("H1", c1_fault, ("and", 1), cam=push(1.0, 1.05, (540, 1100)), sfx=[("fault", "sting", 0.4)])
        V.shot("L01", c1_tip, cam=push(1.0, 1.06, (600, 1100)), sfx=[("spin", "whoosh", 0.4)])
        V.shot("L02", c1_half, cam=push(1.0, 1.04, (540, 1000)), music="curious", sfx=[("half", "ding", 0.4)])
        V.shot("L03", c1_flip, sfx=[("bottom", "thud", 0.45)])
        V.shot("L04", c1_tall, sfx=[(0.2, "boing", 0.35), ("meters", "chime", 0.35)])
        V.shot("L05", c1_fast, (0, "So"), cam=push(1.0, 1.05, (700, 1200)), sfx=[("fast", "whoosh", 0.45)])
        V.shot("L05", c1_end, ("So", 1), sfx=[("tall", "pop", 0.35)])
    else:
        V = Video(EP, title=("NEVER IN", "TWO?"), cap_y=0.72, music="playful", sid="B005C2", captions=False)
        V.shot("H1", c2_hook, (0, "You"), tr="cut", sfx=[(0.0, "creak", 0.4)])
        V.shot("H1", c2_hook, ("You", 1), cam=push(1.15, 1.22, (540, 900)), sfx=[("can't", "click", 0.55)])
        V.shot("L01", c2_three, (0, "Even"), music="story", sfx=[(0.1, "pop", 0.35), (0.35, "pop", 0.35), (0.6, "pop", 0.35)])
        V.shot("L01", c2_three, ("Even", 1), cam=push(1.2, 1.26, (540, 1500)))
        V.shot("L02", c2_spring, cam=push(1.0, 1.05, (540, 960)), music="curious", sfx=[("snaps", "click", 0.5)])
        V.shot("L03", c2_wave, music="tension", sfx=[("again", "click", 0.5)])
        V.shot("L04", c2_mit, (0, "twist"), cam=push(1.0, 1.04, (540, 900)), music="story")
        V.shot("L04", c2_mit, ("twist", 1), cam=push(1.15, 1.22, (700, 960)), sfx=[("bend", "creak", 0.35)])
        V.shot("L05", c2_clean, cam=push(1.0, 1.04, (540, 900)), music="warm", sfx=[("cleanly", "click", 0.5), ("two", "chime", 0.4)])
    V.build()
    return V


if __name__ == "__main__":
    V = build()
    cmd = sys.argv[2] if len(sys.argv) > 2 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=2, cols=8, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "times":
        V.qa_numbers()
        print(V.sheet(sys.argv[4], times=[float(x) for x in sys.argv[3].split(",")], cols=6, scale=0.2))
    elif cmd == "render":
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / f"final/B-005-{SID}.mp4"))
