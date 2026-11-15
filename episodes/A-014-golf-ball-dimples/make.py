"""A-014 "Why Golf Balls Have Dimples" — standalone Short, Style F + cast v2.1 (audit §6.3).
python episodes/A-014-golf-ball-dimples/make.py sheet|render|qa|big <t,t,..>
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, sparkles, arrow

V = Video(EP, title=("WHY GOLF BALLS", "HAVE DIMPLES"), cap_y=0.70,
          keys={"smooth", "wrong", "1800s", "gutta-percha", "sap", "odd", "beaten-up", "further", "hammering", "dents", "1900s", "dimples", "trick",
                "air", "clings", "wake", "smaller", "drag", "hundreds", "short", "shiny"}, music="playful")


# ------------------------------------------------------------------ props
def ball(g, x, y, r, kind="dimpled", rot=0.0, shine=1.0, dents=0.0):
    """kind: dimpled (white), smooth (shiny white), gutty (smooth brown), battered (brown with nicks)."""
    col = {"dimpled": "#F7F7F2", "smooth": "#FFFFFF", "gutty": "#7A4A2A", "battered": "#7A4A2A"}[kind]
    g.circle(x, y, r, col, INK, lw=max(4, r * 0.06))
    if kind == "dimpled" or dents > 0:
        R = rnd(7)
        n = 0
        for j in range(-4, 5):
            for i in range(-4, 5):
                px, py = i * 0.22 + (0.11 if j % 2 else 0), j * 0.2
                d = math.hypot(px, py)
                if d < 0.86:
                    sh = math.sqrt(max(0.0, 1 - d * d))
                    k = dents if kind != "dimpled" else 1.0
                    if kind != "dimpled" and R.random() > k:
                        continue
                    g.ellipse(x + (px * math.cos(rot) - py * math.sin(rot)) * r, y + (px * math.sin(rot) + py * math.cos(rot)) * r,
                              r * 0.075 * (0.55 + 0.45 * sh), r * 0.075, shade(col, 0.82), None)
    if kind == "battered":
        for i in range(6):
            a = i * 1.1 + 0.4
            g.line([(x + r * 0.5 * math.cos(a), y + r * 0.5 * math.sin(a)), (x + r * 0.7 * math.cos(a + 0.2), y + r * 0.7 * math.sin(a + 0.2))], "#4A2A16", r * 0.05)
    if shine:
        g.ellipse(x - r * 0.35, y - r * 0.4, r * 0.28, r * 0.16, "#FFFFFF", None, a=0.75 * shine if kind != "dimpled" else 0.35, rot=-0.6)


def course(g, t, old=False):
    g.fill_all(g.lgrad(0, 0, 0, H, "#9ED8F0" if not old else "#E8D9B8", "#DFF4F6" if not old else "#F2E6C8"))
    with g.layer(0.4):
        g.path("M-200 1150 Q300 980 700 1080 Q1000 1150 1300 1040 L1300 1500 L-200 1500 Z", "#7FC46A" if not old else "#9AB86A", INK, lw=8)
        g.line([(820, 1060), (820, 860)], INK, 8); g.poly([(820, 860), (900, 885), (820, 910)], "#FF3B30", INK, lw=5)
        for i in range(3):
            g.circle(120 + i * 380, 900 + 30 * i, 90, "#3E8E5E", INK, lw=7)
    g.path("M-200 1460 Q540 1380 1300 1460 L1300 2100 L-200 2100 Z", "#5FB04E" if not old else "#86A85A", INK, lw=9)
    for i in range(14):
        g.line([(i * 90 - 40, 1500 + (i % 3) * 30), (i * 90 - 30, 1470 + (i % 3) * 30)], "#3E8E3E", 6)


def club(g, x, y, s, ang):
    with g.at(x, y, ang, s):
        g.line([(0, 0), (0, 520)], "#9AA3AD", 16); g.line([(0, 0), (0, 520)], INK, 4)
        g.rc(30, 540, 110, 50, "#C8CED6", INK, lw=7, r=14)
        g.rc(0, 40, 26, 100, "#22181B", INK, lw=5, r=8)


def flight(g, x0, y0, x1, peak, u, col="#FFFFFF", dash=True):
    """Dotted flight path from (x0,y0) to (x1,y0) with apex `peak` px above; drawn up to progress u."""
    pts = []
    n = 30
    for i in range(int(n * clamp(u)) + 1):
        k = i / n
        pts.append((lerp(x0, x1, k), y0 - peak * 4 * k * (1 - k)))
    if len(pts) > 1:
        g.line(pts, col, 10, a=0.9, dash=([4, 26], 0) if dash else None)
    k = clamp(u)
    return lerp(x0, x1, k), y0 - peak * 4 * k * (1 - k)


def airflow(g, cx, cy, r, dimpled, t, k=1.0):
    """Streamlines round a ball, flowing left to right. Smooth: the flow lets go early -> big swirly wake. Dimpled: hugs longer -> small wake."""
    sep = 0.55 if not dimpled else 0.85            # how far round (0..1 of the half-turn) the flow stays attached
    for j, off in enumerate((-2.2, -1.6, 1.6, 2.2)):
        yy = cy + off * r * 0.5
        side = 1 if off > 0 else -1
        pts = []
        for i in range(41):
            x = cx - 3.2 * r + i * 0.16 * r
            dx = (x - cx) / r
            bump = side * r * 0.55 * math.exp(-dx * dx * 1.4) * (1 if dx < sep * 1.2 else 0.6)
            pts.append((x, yy + bump))
        g.line(pts, "#BFE6F2", 8, a=0.9 * k)
    ball(g, cx, cy, r, "dimpled" if dimpled else "smooth", shine=0.8)
    if dimpled:   # thin turbulent layer hugging the ball
        g.circle(cx, cy, r * 1.08, None, PAL["yellow"], lw=8, a=0.8 * k)
    wake = (1.6 if not dimpled else 0.7) * r
    for i in range(7):                             # wake swirls behind the ball
        u = (t * 0.7 + i / 7) % 1.0
        wx = cx + r * 0.9 + u * wake * 2.2
        wy = cy + math.sin(i * 2.3 + t * 4) * wake * 0.45 * (0.4 + u)
        g.circle(wx, wy, wake * 0.18 * (0.6 + u), None, "#FF8A6B", lw=7, a=k * (1 - u) * 0.9)


def hammer(g, x, y, s, ang):
    with g.at(x, y, ang, s):
        g.line([(0, 0), (0, 300)], "#8A5A3A", 22); g.line([(0, 0), (0, 300)], INK, 4)
        g.rc(0, -20, 140, 60, "#7A8290", INK, lw=8, r=8)


# ------------------------------------------------------------------ shots
def s_hook(g, c):
    """Frame 1: a shiny smooth ball in flight (object in action) + the golfer watching."""
    course(g, c.gt)
    char2(g, "modern", 330, 2250, 1650, "curious" if c.t < c.w("They") - 0.2 else "shocked", "up", "up", t=c.gt)
    u = clamp(c.t / max(c.T, 0.1))
    bx, by = 760 + 60 * u, 760 + 260 * u * u
    ball(g, bx, by, 150, "smooth", rot=c.gt)
    if c.t > c.w("They") - 0.2:
        g.line([(bx - 30, by - 180), (bx - 50, by - 260)], INK, 8)


def s_plop(g, c):
    course(g, c.gt)
    x, y = flight(g, 200, 1700, 560, 260, ease_out(seg(c.t, 0.0, 0.8)))
    ball(g, x, y, 48, "smooth")
    char2(g, "modern", 860, 2150, 1300, "shocked" if c.t > 0.8 else "smug", "hip", "hip", t=c.gt, flip=True)
    if c.t > 0.8:
        with g.screen():
            g.text("SHORT!", 380, 1300, 110, "#FF6B5B", sw=20, depth=8, sc=pop(c.t, 0.8, 0.3), rot=-0.08)


def s_1800s(g, c):
    course(g, c.gt, old=True)
    char2(g, "gent", 520, 2150, 1400, "smug", "down", "hold", t=c.gt)
    with g.screen():
        g.text("1800s", 230, 640, 140, PAL["yellow"], sw=24, depth=8, sc=pop(c.t, 0.0, 0.3), rot=-0.08)


def s_gutty(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#E8C08A", "#B07A4A"))
    with g.at(540, 520, 0, 1.0):                                              # sap dripping from a branch
        g.rc(0, 0, 900, 70, "#6E5034", INK, lw=9, r=30)
        for i in range(3):
            u = (c.gt * 0.8 + i / 3) % 1.0
            g.path(f"M{-40 + i * 40} 30 Q{-50 + i * 40} {60 + 300 * u} {-40 + i * 40} {80 + 300 * u} Q{-30 + i * 40} {60 + 300 * u} {-40 + i * 40} 30 Z",
                   "#B07A4A", INK, lw=5, a=1 - u * 0.5)
    ball(g, 540, 1200, 260, "gutty", shine=1.0)
    sparkles(g, c.gt, [(400, 1040), (700, 1100)], r=34 * ease_out(seg(c.t, c.w("smooth") - 0.2, 0.3)))


def s_odd(g, c):
    course(g, c.gt, old=True)
    char2(g, "gent", 330, 2150, 1350, "suspicious", "hold", "hold", t=c.gt, prop=False)
    ball(g, 760, 1150, 120, "gutty")
    ball(g, 760, 1450, 120, "battered")
    qmark(g, 900, 860, 180, PAL["yellow"], 0.12, pop(c.t, c.w("odd") - 0.2, 0.3))


def s_race(g, c):
    course(g, c.gt, old=True)
    u = ease_out(seg(c.t, 0.0, max(0.6, c.T - 0.3)))
    x1, y1 = flight(g, 120, 1650, 640, 380, u, "#FFF4E0")
    x2, y2 = flight(g, 120, 1650, 1000, 560, u, PAL["yellow"])
    ball(g, x1, y1, 46, "gutty")
    ball(g, x2, y2, 46, "battered")
    with g.screen():
        g.text("NEW", 640, 1760, 70, "#FFF4E0", sw=14, sc=pop(c.t, c.T - 0.5, 0.3))
        g.text("OLD", 960, 1760, 70, PAL["yellow"], sw=14, sc=pop(c.t, c.T - 0.5, 0.3))


def s_hammer(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#E8D9B8", "#C9B48A", "#8A6A44"))
    g.rect(-100, 1450, W + 200, 700, "#6E5034", INK, lw=9)
    char2(g, "worker", 300, 2150, 1300, "angry", "reach_r", "reach_r", t=c.gt, prop=False)
    hits = int(c.t * 3.2)
    ball(g, 720, 1380, 150, "battered", dents=min(1.0, hits / 8))
    ph = (c.t * 3.2) % 1.0
    hammer(g, 640, 1180, 1.2, -1.2 + 1.0 * (1 - abs(math.sin(ph * math.pi))))


def s_morph(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#BFE6F2", "#8FCBE0", "#4C93B5"))
    k = ease_io(seg(c.t, c.w("dimples") - 0.8, 0.8))
    if k < 1:
        with g.group(1 - k):
            ball(g, 540, 1150, 330, "battered", dents=1.0)
    if k > 0:
        with g.group(k):
            ball(g, 540, 1150, 330, "dimpled", rot=c.gt * 0.3)
    with g.screen():
        g.text("1900s", W / 2, 620, 140, PAL["yellow"], sw=24, depth=8, sc=pop(c.t, c.w("1900s") - 0.1, 0.3), rot=-0.05)


def s_air(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    k = ease_out(seg(c.t, 0.0, 0.4))
    airflow(g, 420, 760, 150, False, c.gt, k)
    airflow(g, 420, 1360, 150, True, c.gt, ease_out(seg(c.t, c.w("stir") - 0.2, 0.4)))
    g.text("SMOOTH", 880, 600, 60, "#FFFFFF", sw=10)
    g.text("DIMPLED", 880, 1200, 60, PAL["yellow"], sw=10)


def s_wake(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    airflow(g, 330, 760, 140, False, c.gt)
    airflow(g, 330, 1360, 140, True, c.gt)
    kd = ease_out(seg(c.t, c.w("drag") - 0.3, 0.4))
    arrow(g, 180, 760, 180 - 260 * kd, 760, "#FF3B30", w=30, k=kd)
    arrow(g, 180, 1360, 180 - 110 * kd, 1360, "#FF3B30", w=30, k=kd)
    with g.screen():
        g.text("DRAG", 120, 640, 64, "#FF8A6B", sw=10, sc=kd)


def s_hundreds(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#F6C98E", "#E39B5A"))
    ball(g, 540, 1100, 420, "dimpled", rot=c.gt * 0.4)
    with g.at(830, 640, -0.05, pop(c.t, c.w("hundreds") - 0.1, 0.35)):
        g.rc(0, 0, 360, 170, "#5ED3B5", INK, lw=10, r=30)
        g.text("300+", 0, 8, 100, "#FFFFFF", sw=16)


def s_short(g, c):
    course(g, c.gt)
    u = ease_out(seg(c.t, 0.0, max(0.5, c.T - 0.2)))
    x1, y1 = flight(g, 120, 1700, 520, 300, u, "#FFFFFF")
    x2, y2 = flight(g, 120, 1700, 1020, 620, u, PAL["yellow"])
    ball(g, x1, y1, 46, "smooth")
    ball(g, x2, y2, 46, "dimpled")


def s_loop(g, c):
    """Last shot ~ frame 1 (loop): the golfer, a shiny new ball in the air again."""
    course(g, c.gt)
    late = c.t > c.w("shiny") - 0.3
    char2(g, "modern", 330, 2250, 1650, "suspicious" if late else "curious", "up", "up", t=c.gt)
    ball(g, 790, 800, 150, "smooth", rot=c.gt)
    sparkles(g, c.gt, [(700, 660), (900, 720)], r=26 * (1 if late else 0))


V.shot("H1", s_hook, part=(0, "They"), sfx=[(0.0, "whoosh", 0.5)])
V.shot("H1", s_plop, part=("They", 1), sfx=[(0.8, "thud", 0.45), (0.9, "boing", 0.3)])
V.shot("L01", s_1800s, part=(0, "gutta-percha"), tr="flash", music="curious", sfx=[(0.0, "whoosh_soft", 0.4)])
V.shot("L01", s_gutty, part=("gutta-percha", 1), cam=push(1.0, 1.06, (540, 1100)), sfx=[("smooth", "shimmer", 0.35)])
V.shot("L02", s_odd, part=(0, "old"), sfx=[("odd", "hmm", 0.45)])
V.shot("L02", s_race, part=("old", 1), sfx=[(0.0, "whoosh", 0.4)])
V.shot("L03", s_hammer, music="playful", sfx=[(0.1, "thud", 0.35), (0.42, "thud", 0.35), (0.73, "thud", 0.35), (1.04, "thud", 0.35), (1.35, "thud", 0.35)])
V.shot("L04", s_morph, cam=push(1.0, 1.05, (540, 1150)), sfx=[("dimples", "ding", 0.45)])
V.shot("L05", s_air, part=(0, "dimples"), tr="flash", music="curious", sfx=[(0.0, "wind", 0.3)])
V.shot("L05", s_air, part=("dimples", 1), cam=push(1.15, 1.25, (460, 1360)), sfx=[("clings", "swell", 0.35)])
V.shot("L06", s_wake, sfx=[("drag", "drum_hit", 0.35)])
V.shot("L07", s_hundreds, part=(0, "Smooth"), sfx=[("hundreds", "ding", 0.4)])
V.shot("L07", s_short, part=("Smooth", 1), sfx=[(0.0, "whoosh", 0.35)])
V.shot("L08", s_loop, sfx=[(0.0, "whoosh_soft", 0.3)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=7, scale=0.17))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-014.mp4"))
