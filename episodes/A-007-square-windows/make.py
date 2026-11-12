"""A-007 "Why Plane Windows Are Never Square" — standalone Short, Style F (flat 2D), 1080x1920.
python episodes/A-007-square-windows/make.py sheet|render|big <t,t,..>
Respectful: no victims, no crash images (a newspaper headline stands for the 1954 losses).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from flat_cast import Char, WY, tie, buttons, amix
from flat_fx import *
from flat_sets import sky, cloud, plane, crack, fuselage_skin, big_window, hangar, tank_back, tank_front, TANK, stress_field, newspaper, xray_bg

V = Video(EP, title=("WHY PLANE WINDOWS", "ARE NEVER SQUARE"),
          keys={"square", "comet", "first", "water", "tank", "thousands", "crack", "sharp", "corner", "stress", "piles", "round", "rounded", "reason"}, music="curious")
ENG1 = Char(skin="#F1C9A5", top="#F6F2EA", hair="side", hair_col="#6B4A2F", glasses=INK, outfit=[tie("#B0413E")], legs="#3A3F4A", seed=1.3)
ENG2 = Char(skin="#C98F62", top="#2F6F8C", hat="cap", hat_col="#7A5236", stache="#3B2A20", outfit=[buttons("#FFC93C", 3)], legs="#27303B", seed=2.6)
WC = (540, 1270)          # big window centre (hook, crack and payoff shots)
WA = 210
CORNER = (WC[0] + WA, WC[1] - WA)


def speed_lines(g, t, y0=120, y1=820, n=9, seed=5):
    R = rnd(seed)
    for i in range(n):
        y, ph, L, sp = R.uniform(y0, y1), R.random(), R.uniform(140, 340), R.uniform(1.4, 2.4)
        x = W + 400 - ((t * sp + ph) % 1.0) * (W + 900)
        g.line([(x, y), (x + L, y)], "#FFFFFF", 7, a=0.22)


def wy_in_window(expr, look, wave=0.0, t=0.0):
    def inside(g):
        g.rect(WC[0] - WA, WC[1] - WA, 2 * WA, 2 * WA, g.lgrad(0, WC[1] - WA, 0, WC[1] + WA, "#17566A", "#0E3A47"), None)
        hy = -250 + (-60 * abs(math.sin(t * 9)) if wave else 0)
        WY.draw(g, t, WC[0], WC[1] + 530, sc=1.55, turn=0.25 if not wave else 0.1, expr=expr, look=look, shadow=False,
                arms=((-118, -252), (118, hy) if not wave else (128 + 18 * math.sin(t * 9), -330)))
    return inside


def s_hook(g, c):
    t = c.gt
    sky(g, t, speed=520)
    with g.layer(0.6):
        speed_lines(g, t)
    fuselage_skin(g, 640)
    ck = 0.42 + 0.58 * ease_io(seg(t, 0.2, 3.3))
    th = 0.7 + 0.3 * math.sin(TAU * 2.4 * t)
    g.glow(CORNER[0], CORNER[1], 230 * th, "#FF3B30", 0.55)
    big_window(g, WC[0], WC[1], WA, 0.0, inside=wy_in_window("shock", (0.7, -0.7), t=t))
    crack(g, CORNER[0] - 6, CORNER[1] + 6, ck, 0.74, 0.9)
    pain_marks(g, CORNER[0] + 30, CORNER[1] - 10, 170, t, n=3, col=PAL["yellow"], a0=-1.5, a1=-0.7, sc=1.1)


def s_comet(g, c):
    t = c.t
    sky(g, c.gt, speed=150)
    x = lerp(400, 560, ease_io(c.u))
    for i in range(2):
        g.line([(x - 470, 1296 + i * 14), (x - 1300, 1296 + i * 14)], "#FFFFFF", 12, a=0.22)
    plane(g, c.gt, x, 1240, 0.94, faces=True)
    sparkles(g, t, [(x + 250, 1120), (x - 120, 1150), (x + 60, 1340)], r=34 * seg(t, c.w("first") - 0.2, 0.3) if c.sh["name"] == "b" else 0)


def s_news(g, c):
    t = c.t
    g.fill_all(g.rgrad(540, 1250, 1300, "#1C4A5C", "#0A2233", "#07121C"))
    g.rings(540, 1250, 620, "#FFC93C", a=0.05, n=3)
    k = back_out(seg(t, 0, 0.42), 1.4)
    newspaper(g, 540, 1262 + 26 * math.sin(c.gt * 1.4), 0.2 + 0.74 * k, -2.6 * (1 - k) - 0.05)
    for i, (x, y) in enumerate(((170, 1010), (905, 1560))):
        qmark(g, x, y, 150, PAL["yellow"], -0.3 + i * 0.6, pop(t, c.w("within") - 0.1 + i * 0.12, 0.3))


def s_why(g, c):
    t = c.t
    hangar(g, c.gt)
    tank_back(g, c.gt); tank_front(g, c.gt)
    ENG1.draw(g, c.gt, 320, 1690, sc=1.18, turn=0.3, expr="think", arms=("hip", "chin"), look=(0.4, -0.6))
    ENG2.draw(g, c.gt, 770, 1690, sc=1.18, face=-1, turn=0.3, expr="confused", arms=("down", "head2"), look=(0.4, -0.6))
    qmark(g, 545, 1010 + 10 * math.sin(c.gt * 4), 230, PAL["yellow"], 0.08, pop(t, 0.1, 0.3))


def tank_scene(g, c, py, swell=0.0, splash=0.0, cables=False, e1=("happy", ("hip", "point")), e2=("happy", ("down", "up"))):
    hangar(g, c.gt)
    tank_back(g, c.gt)
    if cables:
        for dx in (-210, 190):
            g.line([(540 + dx, -200), (540 + dx, py - 60)], INK, 9); g.line([(540 + dx, -200), (540 + dx, py - 60)], "#AEB8C2", 4)
            g.circle(540 + dx, py - 56, 10, "#FFC93C", INK, lw=4)
    plane(g, c.gt, 540, py, 0.86, bob=False, swell=swell)
    tank_front(g, c.gt, splash)
    ENG1.draw(g, c.gt, 150, 1800, sc=0.92, turn=0.35, expr=e1[0], arms=e1[1], look=(0.6, -0.5))
    ENG2.draw(g, c.gt, 935, 1800, sc=0.92, face=-1, turn=0.35, expr=e2[0], arms=e2[1], look=(0.6, -0.5))


def s_sink(g, c):
    t = c.t
    k = ease_io(seg(t, 0.1, 1.5))
    py = lerp(640, 1215, k)
    hit = t - 0.95
    tank_scene(g, c, py, splash=math.exp(-max(0, hit) * 2.2) if hit > 0 else 0, cables=True,
               e1=("surprised" if t < 1.7 else "happy", ("hip", "point")), e2=("surprised" if t < 1.7 else "joy", ("down", "up")))
    if hit > 0:
        for i in range(12):
            a0 = -2.7 + i * 0.21
            v = 420 + 70 * math.sin(i * 2.7)
            x = 540 + (i - 5.5) * 62 + v * 0.35 * math.cos(a0) * hit
            y = TANK[1] + 30 + v * math.sin(a0) * hit + 900 * hit * hit
            if y < TANK[1] + 40:
                g.circle(x, y, 13 - 0.4 * i, "#BFF1FF", INK, lw=4, a=clamp(1.2 - hit * 1.1))


def s_pump(g, c):
    t = c.t
    sw = 0.5 - 0.5 * math.cos(TAU * 1.45 * c.gt)
    arm = amix("hold", "reach", sw)
    tank_scene(g, c, 1215, swell=sw, e1=("neutral", ("hip", "hold")), e2=("determined", ("down", arm)))
    if c.sh["name"] != "count":
        gauge(g, 540, 1640, 104, 0.15 + 0.8 * sw)
    else:
        k = ease_io(seg(t, 0.15, c.T - 0.5))
        n = int(lerp(137, 3040, k)) + int(c.gt * 37) % 9
        g.rect(270, 1560, 540, 124, INK, None, r=24)
        g.rect(270, 1560, 540, 124, None, PAL["yellow"], lw=6, r=24)
        g.text("FLIGHTS", 384, 1622, 50, PAL["cream"], stroke=None)
        g.text(f"{n:,}", 660, 1622, 92, PAL["yellow"], stroke=None)
        for dx in (-250, 0, 250):                 # stress rings pulsing at the window corners
            g.circle(540 + dx * 0.86, 1215 - 44, 26 + 30 * sw, None, PAL["yellow"], lw=7, a=0.75 * (1 - sw))


def s_crack(g, c):
    t = c.gt - V.voice0["L04"]
    g.fill_all("#17688E")
    fuselage_skin(g, 640, water=1.0)
    tc = V.T["L04"]["words"][3]["s"] + 0.42          # the crack lands in the pause after "appeared..."
    ck = 0.9 * ease_out(seg(t, tc - 0.05, 1.1)) + 0.1 * seg(t, tc + 1.1, 2.4)
    if ck > 0:
        g.glow(CORNER[0], CORNER[1], 210, "#FF3B30", 0.5 * min(1, ck * 3) * (0.75 + 0.25 * math.sin(TAU * 2.2 * c.gt)))
    big_window(g, WC[0], WC[1], WA, 0.0, glass="#0B3345")
    crack(g, CORNER[0] - 6, CORNER[1] + 6, ck, 0.74, 0.9)
    ring_wave(g, CORNER[0], CORNER[1], 30, 330, seg(t, tc, 0.55), "#FFF4E0", 14)
    R = rnd(3)
    for i in range(14):                                   # bubbles
        bx, ph, sp, r = R.uniform(40, 1040), R.random(), R.uniform(0.2, 0.45), R.uniform(8, 20)
        u = (ph + c.gt * sp) % 1.0
        g.circle(bx + 12 * math.sin(c.gt * 2 + i), 1900 - u * 1300, r, None, "#BFF1FF", lw=4.5, a=0.7 * math.sin(u * math.pi))
    g.fill_all((0.18, 0.64, 0.78, 0.16))
    if c.sh["name"] == "corner":
        k = pop(c.t, 0.12, 0.35)
        if k > 0:
            with g.at(CORNER[0] + 70, CORNER[1] - 10, 0, k):
                g.circle(0, 0, 178, None, INK, lw=30); g.circle(0, 0, 178, None, PAL["yellow"], lw=16)
                g.line([(126, 126), (236, 236)], INK, 50); g.line([(126, 126), (232, 232)], PAL["coral"], 32)


def diagram(g, c, m=0.0, hot=0.3, ck=0.0):
    xray_bg(g, c.gt, glow=(540, 1290))
    g.rect(30, 880, 1020, 830, "#B9C9D4", r=40)
    for i in range(12):
        for yy in (912, 1678):
            g.circle(85 + i * 83, yy, 7, shade("#B9C9D4", -0.3), None)
    c_ = g.c
    c_.save(); g._rr(36, 886, 1008, 818, 36); c_.clip()
    stress_field(g, c.gt, 540, 1294, a=150, m=m, hot=hot, nlines=6, span=620, col=mix("#FFF4E0", "#2E8C74", m * 0.0))
    c_.restore()
    if ck > 0:
        crack(g, 540 + 146, 1294 - 146, ck, 0.42, 0.34)


def s_flow(g, c):
    t = c.t
    diagram(g, c, 0.0, 0.3)
    k = pop(t, c.w("like") - 0.1, 0.35)
    if k > 0:                                              # inset: water flowing around a rock
        with g.at(850, 1560, 0, k):
            g.circle(0, 0, 150, "#1F7FA6", INK, lw=10)
            with g.clip(circle=(0, 0, 145)):
                stress_field(g, c.gt, 0, 0, a=48, m=1.0, hot=0, nlines=4, span=170, water=True, hole=False, glow=False, speed=160)
                g.poly([(-44, 18), (-30, -34), (12, -46), (46, -14), (38, 34), (-8, 46)], "#8C6A4F", INK, lw=6, r=14)
            g.circle(0, 0, 150, None, INK, lw=10); g.circle(0, 0, 150, None, PAL["cream"], lw=4)


def s_pile(g, c):
    t = c.t
    hot = lerp(0.3, 1.0, ease_io(seg(t, c.w("piles") - 0.5, 0.6)))
    diagram(g, c, 0.0, hot, ck=ease_out(seg(t, c.w("up") - 0.1, 0.5)) * 0.8)


def s_round(g, c):
    t = c.t
    m = ease_io(seg(t, c.w("Round") + 0.05, 0.75))
    diagram(g, c, m, 1.0 * (1 - m))
    check_badge(g, 860, 1040, 92, pop(t, c.w("out") - 0.05, 0.35, 2.4))
    burst(g, 860, 1040, 110, 230, 8, PAL["cream"], 11, seg(t, c.w("out") - 0.05, 0.45))


def s_today(g, c):
    t = c.t
    sky(g, c.gt, top="#0B3A55", bot="#2590A8", speed=520)
    with g.layer(0.6):
        speed_lines(g, c.gt)
    fuselage_skin(g, 640, panel="#E8EEF2")
    big_window(g, WC[0], WC[1], WA, 1.0, inside=wy_in_window("joy", (0, 0), wave=1.0, t=c.gt))
    sparkles(g, t, [(250, 1010), (850, 980), (900, 1500), (190, 1540)], r=44, period=0.9)


def icon(g, kind, x, y, k, t):
    if k <= 0: return
    with g.at(x, y + 10 * math.sin(t * 3 + x), 0.06 * math.sin(t * 2 + x), k):
        if kind == "manhole":
            g.circle(0, 0, 104, "#7F8E99"); g.circle(0, 0, 80, "#93A2AD", INK, lw=5)
            with g.clip(circle=(0, 0, 78)):
                for i in range(-4, 5):
                    g.line([(i * 30 - 80, -80), (i * 30 + 80, 80)], shade("#93A2AD", -0.25), 6)
                    g.line([(i * 30 + 80, -80), (i * 30 - 80, 80)], shade("#93A2AD", -0.25), 6)
        elif kind == "honey":
            for hx, hy in ((0, -58), (-52, 32), (52, 32)):
                g.poly([(hx + 56 * math.cos(TAU * j / 6 + TAU / 12), hy + 56 * math.sin(TAU * j / 6 + TAU / 12)) for j in range(6)], PAL["yellow"], r=6)
                g.poly([(hx + 30 * math.cos(TAU * j / 6 + TAU / 12), hy + 30 * math.sin(TAU * j / 6 + TAU / 12)) for j in range(6)], "#F2A93B", None, r=4)
        else:
            g.poly([(100 * math.cos(TAU * j / 8 + TAU / 16), 100 * math.sin(TAU * j / 8 + TAU / 16)) for j in range(8)], "#FF5B4B", r=6)
            g.poly([(78 * math.cos(TAU * j / 8 + TAU / 16), 78 * math.sin(TAU * j / 8 + TAU / 16)) for j in range(8)], None, "#FFF4E0", lw=8, r=5)
        g.text("?", 92, -96, 110, PAL["yellow"], sw=22, depth=7, rot=0.2)


def s_shapes(g, c):
    t = c.t
    xray_bg(g, c.gt, glow=(540, 1400), col="#1F8A6E")
    for i, (kind, x, y) in enumerate((("manhole", 205, 1130), ("stop", 540, 1010), ("honey", 880, 1130))):
        icon(g, kind, x, y, pop(t, 0.04 + i * 0.14, 0.32), c.gt)
    g.ellipse(540, 1790, 330, 60, "#FFB060", None, a=0.10)
    WY.draw(g, c.gt, 540, 1790, sc=1.3, turn=0.0, expr="think", arms=("hip", "chin"), look=(0.2 * math.sin(c.gt * 2.2), -0.8))


HOOKCAM = roi((600, 1235), 1.22, 1.3, sy=1240)
V.shot("H1", s_hook, part=(0, "square"), cam=HOOKCAM, sfx=[(0.0, "wind", 0.3), (0.0, "click", 0.3)], music="curious", tr="cut")
V.shot("H1", s_hook, part=("square", 1), cam=roi((CORNER[0] - 60, CORNER[1] + 60), 1.42, 1.58, sy=1230), sfx=[(0.0, "thud", 0.45), (0.0, "wind", 0.5), (0.05, "click", 0.5)])
V.shot("L01", s_comet, part=(0, "the"), cam=roi((540, 1240), 1.0, 1.08, sy=1240), sfx=[(0.0, "whoosh", 0.3), (0.0, "wind", 0.4)], name="a")
V.shot("L01", s_comet, part=("the", "broke"), cam=roi((470, 1215), 1.75, 1.9, sy=1230, p1=(680, 1215)), sfx=[(0.0, "wind", 0.5), ("first", "sparkle", 0.4)], name="b")
V.shot("L01", s_news, part=("broke", 1), cam=roi((540, 1250), 1.0, 1.07, sy=1250), sfx=[(0.0, "paper", 0.5), (0.3, "thud", 0.45), ("within", "hmm", 0.4)], music="tension", tr="flash")
V.shot("L02", s_why, part=(0, "engineers"), cam=roi((540, 1330), 1.0, 1.06, sy=1330), sfx=[(0.1, "pop", 0.4)], music="curious")
V.shot("L02", s_sink, part=("engineers", 1), cam=roi((540, 1250), 1.0, 1.08, sy=1250), sfx=[(0.1, "creak", 0.5), (0.95, "splash", 0.6), (1.8, "crowd_cheer", 0.16)])
V.shot("L03", s_pump, part=(0, "again"), cam=roi((540, 1300), 1.0, 1.05, sy=1300), sfx=[("pumped", "bloop", 0.4), ("up", "creak", 0.35), ("down", "bloop", 0.4)], name="pump")
V.shot("L03", s_pump, part=("again", 1), cam=roi((540, 1330), 1.1, 1.2, sy=1300), sfx=[(0.0, "tick", 0.35), (0.45, "tick", 0.35), (0.9, "tick", 0.35), (1.35, "tick", 0.35), ("thousands", "riser", 0.3)], name="count")
V.shot("L04", s_crack, part=(0, "at"), cam=roi((560, 1250), 1.0, 1.1, sy=1250, shake=lambda c: 0.9 * pulse(c.t, c.w("appeared...") + 0.42, 0.5)),
       sfx=[(("appeared...", 0.42), "click", 0.6), (("appeared...", 0.42), "thud", 0.5), (("appeared...", 0.5), "freeze", 0.28)], music="tension", name="crack")
V.shot("L04", s_crack, part=("at", 1), cam=roi((CORNER[0] - 40, CORNER[1] + 50), 1.4, 1.62, sy=1230), sfx=[(0.1, "pop", 0.45), ("squarish", "hmm", 0.35)], name="corner")
V.shot("L05", s_flow, part=(0, "At"), cam=roi((540, 1294), 1.0, 1.06, sy=1294), sfx=[("like", "pop", 0.35), ("water", "splash", 0.2)], music="curious")
V.shot("L05", s_pile, part=("At", 1), cam=roi((600, 1240), 1.2, 1.7, sy=1250, p1=(686, 1150)), sfx=[("piles", "swell", 0.4), ("up", "sting", 0.26)])
V.shot("L06", s_round, part=(0, "So"), cam=roi((540, 1294), 1.08, 1.0, sy=1294), sfx=[(("Round", 0.45), "melt", 0.3), ("out", "ding", 0.4)], music="warm")
V.shot("L06", s_today, part=("So", 1), cam=roi((540, 1270), 1.12, 1.0, sy=1270), sfx=[(0.0, "whoosh", 0.4), (0.0, "wind", 0.45), ("rounded", "sparkle", 0.4)])
V.shot("L07", s_shapes, cam=roi((540, 1400), 1.0, 1.08, sy=1400), sfx=[(0.04, "pop", 0.28), (0.18, "pop", 0.28), (0.32, "pop", 0.28), (("reason", 0.5), "hmm", 0.4)], music="playful")
V.title_out = None
V.build()
V.title_out = V.shots[2]["start"] - 0.25

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    out = EP / "final/A-007.mp4"
    if cmd == "sheet":
        print(V.sheet(EP / "animatic/sheet.jpg", per_shot=2, cols=8, scale=0.22))
    elif cmd == "big":
        print(V.sheet(EP / "animatic/big.jpg", times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.45))
    elif cmd == "render":
        V.render(out); measure(out)
    print(" ".join(f'{sh["id"][-2:]}:{sh["dur"]:.2f}' for sh in V.shots), "| total", V.duration)
