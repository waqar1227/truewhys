"""B-008 cut Short C1 "melted candy bar", re-composed vertically (1080x1920) with its own hook and script (not a crop of L8):
frame-1 rule (motion + sound at 0.0 s, face + object + <= 4-word question), answer at the end, last shot loops to the first, corner badge.
python episodes/B-008-accidental-inventions/shorts/make_short.py C1 sheet|qa|times <t,..> <out>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import arrow, burst, sparkles
from flat_invent import *
import sfxgen  # noqa

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-microwave"}
EP = HERE / DIRS[SID]
FL = 1560


def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def pk(c, word, n=0, frac=0.5):
    return pop(c.t, tw(c, word, n, frac) - 0.1, 0.3)


def label(g, txt, x, y, size=96, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x, y, k=1.0, size=54):
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, "#3A1626", PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def lab_v(g, t):
    """1945 radar lab, vertical: green-grey wall, dial rack, window with a radar dish, bench."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#5E7468", "#3A4C44"))
    with g.layer(0.7):
        g.rect(40, 420, 200, 900, "#3E4A48", INK, lw=7)
        for k in range(6):
            g.circle(100, 500 + k * 130, 30, "#E8E2CC", INK, lw=5)
            g.line([(100, 500 + k * 130), (100 + 22 * math.cos(t * (1 + k) + k), 500 + k * 130 - 20)], "#FF5B4B", 4)
            g.circle(180, 500 + k * 130, 11, ("#7CF0B5" if (int(t * 3) + k) % 3 else "#2A3A30"), INK, lw=3)
        g.rect(640, 200, 360, 300, "#2E3C38", INK, lw=8, r=8)
        g.rect(655, 215, 330, 270, g.lgrad(0, 215, 0, 485, "#8FB8D8", "#D8ECF5"), None)
        with g.at(820, 380, 0.3 * math.sin(t * 0.6)):
            g.path("M-90 -40 Q0 60 90 -40 Z", "#C9CED6", INK, lw=6)
            g.line([(0, 10), (0, 90)], INK, 8)
    g.rect(-100, FL, W + 200, H, "#6E6A60", INK, lw=8)


def kitchen_v(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#DFF3EA", "#BFE3D4"))
    with g.layer(0.7):
        for x in (200, 880):
            g.rect(x - 150, 160, 300, 260, "#FF8A6A", INK, lw=7, r=12)
        g.rect(390, 180, 300, 240, "#7A5236", INK, lw=8, r=10)
        g.rect(405, 195, 270, 210, "#BFE9FA", None)
    g.rect(-100, 1180, W + 200, 60, "#F4F1EA", INK, lw=8, r=6)
    g.rect(-100, 1240, W + 200, 700, "#3E7CB1", INK, lw=8)


def engineer(g, c, x, h=1380, melt=0.5, expr="shocked", pr="down", feet=1930):
    char2(g, "radar", x, feet, h, expr, "down", pr, t=c.gt, view="3q")
    px, py = x + 0.075 * h, feet - 0.6 * h
    candy_bar(g, px, py - 150, 1.5, melt, c.gt, rot=0.08)
    pocket(g, px, py, 235, 150)


def c1_hook(g, c, end=False):
    lab_v(g, c.gt)
    g.rect(560, 1060, 560, 50, "#9A6A44", INK, lw=7, r=8)
    magnetron(g, 830, 1060, 1.0, c.gt, 1.0)
    for i in range(4):
        ph = (c.gt * 1.2 + i / 4) % 1
        x = 760 - 260 * ph
        g.path(f"M{x} 640 q30 45 0 90 q-30 45 0 90", None, "#FFB38A", lw=10, a=0.8 * math.sin(ph * math.pi))
    m = 0.4 + 0.6 * clamp(c.t / 2.6) if not end else 0.3 + 0.5 * clamp(c.t / 2.0)
    engineer(g, c, 330, 1380, m, "shocked", pose_at(c.t, [(0, "down"), (0.5, "explain")]))


def c1_tube(g, c):
    lab_v(g, c.gt)
    g.rect(140, 1180, 800, 50, "#9A6A44", INK, lw=7, r=8)
    magnetron(g, 540, 1180, 1.6, c.gt, 1.0)
    tag(g, "MASSACHUSETTS · 1945", 540, 140, on(c, "1945", frac=0.05))
    label(g, "MAGNETRON", 540, 1420, 90, k=on(c, "magnetrons"))
    label(g, "RADAR", 820, 300, 80, PAL["cream"], k=on(c, "radar"))


def c1_pop(g, c):
    lab_v(g, c.gt)
    g.rect(60, 1200, 960, 50, "#9A6A44", INK, lw=7, r=8)
    magnetron(g, 850, 1200, 0.9, c.gt, 1.0)
    kp_ = clamp((c.t - tw(c, "popped")) / 0.5)
    for i in range(10):
        r = rnd(i)
        x = 520 + i * 30; y = 1180
        if kp_ > 0:
            u = clamp(kp_ * 1.4 - r.random() * 0.4)
            x += (r.random() - 0.5) * 600 * u; y -= 900 * u * (1 - u) * 2
        popcorn(g, x, y, 46, kp_ if kp_ > 0 else 0.0, r.random() * 3, kernel=kp_ <= 0)
    ke = clamp((c.t - tw(c, "exploded")) / 0.5)
    if on(c, "egg") > 0:
        egg(g, 620, 1100, 1.3, ke)
    char2(g, "radar", 190, FL + 300, 1250, "shocked" if ke > 0 else "curious", "down", "up" if ke > 0 else "point", t=c.gt, view="3q")
    tag(g, "SO THE STORY GOES", 540, 140, 1.0)
    label(g, "POP!", 760, 820, 120, k=pk(c, "popped"))
    label(g, "BOOM!", 760, 620, 140, "#FF6B5B", k=pk(c, "exploded"))


def c1_shake(g, c):
    g.fill_all(g.rgrad(W / 2, H / 2, H * 0.6, "#E07A3A", "#9A3A20", "#3A1208"))
    k = on(c, "shaking")
    for i in range(12):
        x = 230 + (i % 3) * 310 + 34 * math.sin(c.gt * 40 + i) * k
        y = 520 + (i // 3) * 300 + 24 * math.cos(c.gt * 37 + i) * k
        g.circle(x, y, 64, "#E8463A", INK, lw=6)
        g.circle(x - 58, y - 46, 36, "#FFFFFF", INK, lw=5)
        g.circle(x + 58, y - 46, 36, "#FFFFFF", INK, lw=5)
    label(g, "WATER", 540, 300, 100, "#BDEBFF", k=on(c, "water"))
    kh = on(c, "heat")
    label(g, "HEAT!", 540, 1720, 140, k=kh)
    for i in range(5):
        if kh <= 0: break
        ph = (c.gt * 1.1 + i / 5) % 1
        x = 140 + i * 200
        g.path(f"M{x} {1600 - 200 * ph} q30 45 0 90 q-30 45 0 90", None, "#FFE29A", lw=12, a=kh * math.sin(ph * math.pi))


def c1_giant(g, c):
    lab_v(g, c.gt)
    oven_1947(g, 730, FL + 120, 1.75, c.gt, on=1.0)
    char2(g, "radar", 260, FL + 120, 1380, "shocked", "down", "point", t=c.gt, view="3q")
    tag(g, "FIRST MICROWAVE OVEN · 1947", 540, 140, on(c, "1947", frac=0.1))
    kt = on(c, "tall")
    with g.screen():
        if kt > 0:
            g.line([(1040, FL + 120), (1040, FL + 120 - 1430 * kt)], PAL["yellow"], 10)
            g.text("6 FT", 960, 300, 90, PAL["yellow"], sw=12)
        kw = on(c, "pounds")
        if kw > 0:
            g.rc(690, 1780, 420, 150, "#3A1626", INK, lw=8, r=24)
            g.text("750 LB", 690, 1790, 96, PAL["yellow"], sw=10, sc=back_out(kw, 1.6))


def c1_end(g, c):
    """Last shot matches frame 1 so the Short loops."""
    if c.t < tw(c, "check", frac=0.5) - 0.1:
        kitchen_v(g, c.gt)
        microwave_modern(g, 640, 1180, 1.25, c.gt, on=1.0)
        char2(g, "modern", 260, FL + 260, 1350, "smile", "down", "hold", t=c.gt, view="3q")
    else:
        c1_hook(g, c, end=True)
        label(g, "CHECK YOUR POCKETS", 540, 330, 86, k=pk(c, "pockets"))


def build():
    V = Video(EP, title=("NOTHING", "WAS HOT?"), cap_y=0.72, music="mystery", sid="B008C1", captions=False)
    V.shot("H1", c1_hook, (0, "and"), tr="cut", sfx=[(0.0, "melt", 0.5), (0.05, "hum", 0.35), (0.1, "whoosh", 0.3)])
    V.shot("H1", c1_hook, ("and", 1), cam=push(1.12, 1.18, (540, 820)), sfx=[("hot", "sting", 0.4)])
    V.shot("L01", c1_tube, (0, "Percy"), cam=push(1.0, 1.04, (540, 1000)), music="story", sfx=[(0.1, "hum", 0.3)])
    V.shot("L01", c1_tube, ("Percy", 1), cam=push(1.06, 1.1, (540, 900)), sfx=[("radar", "beep3", 0.3)])
    V.shot("L02", c1_pop, (0, "Then"), cam=push(1.0, 1.04, (540, 1000)), music="playful", sfx=[("popped", "pop", 0.45), ("popped", "bulb_pop", 0.25)])
    V.shot("L02", c1_pop, ("Then", 1), cam=push(1.08, 1.12, (500, 1000)), sfx=[("exploded", "crash", 0.4)])
    V.shot("L03", c1_shake, (0, "And"), cam=push(1.0, 1.04, (540, 960)), music="curious", sfx=[("shaking", "buzz_fast", 0.25)])
    V.shot("L03", c1_shake, ("And", 1), cam=push(1.06, 1.1, (540, 1100)), sfx=[("heat", "swell", 0.35)])
    V.shot("L04", c1_giant, (0, "was"), cam=push(1.0, 1.04, (540, 1000)), music="inventive", sfx=[("1947", "clunk", 0.35)])
    V.shot("L04", c1_giant, ("was", 1), cam=push(1.04, 1.08, (600, 1000)), sfx=[("tall", "pop", 0.3), ("pounds", "drum_hit", 0.35)])
    V.shot("L05", c1_end, cam=push(1.0, 1.04, (540, 1000)), music="mystery", sfx=[("food", "beep3", 0.3), ("pockets", "melt", 0.4)])
    V.title_y = 0.1
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
        V.render(str(EP / f"final/B-008-{SID}.mp4"))
