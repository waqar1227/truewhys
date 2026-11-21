"""A-020 "Why We Waited 13 Years for GTA 6" — standalone Short, Style F + cast v2.1 (owner request 21 Nov 2026: GTA 6 trending).
python episodes/A-020-gta6-wait/make.py sheet|qa|big <t,..>|render
Our own cast and sets only: a gamer on his sofa whose beard grows over 13 years. No game art, logos, footage or characters; the
name "GTA 6" appears only as plain text in our font (facts in sources.md).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, sparkles, burst
from flat_split import split_long

V = Video(EP, title=("WHY WE WAITED 13 YEARS", "FOR GTA 6"), cap_y=0.70, music="playful",
          keys={"thirteen", "13", "gta", "2013", "2018", "western", "selling", "million", "ninety-three", "day", "delayed", "twice", "may", "november", "worth"})
GREY, BROWN = "#C9C2B8", "#3A2416"


# ------------------------------------------------------------------ set + props
def room(g, t, lamp=1.0):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2B2350", "#1B1838"))
    with g.layer(0.5):
        for i in range(-1, 9):
            g.rect(i * 140, 0, 136, 1500, "#30285A", None, a=0.6)
        g.rect(700, 220, 300, 380, "#3E3570", INK, lw=8, r=8)                      # window at night
        g.circle(900, 330, 40, "#FFF4E0", None, a=0.9)
        g.line([(850, 220), (850, 600)], INK, 8); g.line([(700, 410), (1000, 410)], INK, 8)
    g.glow(540, 1150, 900, "#7A6CFF", 0.12 * lamp)
    g.rect(-100, 1500, W + 200, H, "#3A2E5A", None)                                 # floor
    g.ellipse(540, 1660, 520, 70, "#2A2148", None)                                  # rug


def tv(g, x, y, s, t, text="GTA 6?", col="#FF6B5B", glow=1.0, sub=None):
    with g.at(x, y, 0, s):
        g.glow(0, 0, 520, "#7FD1FF", 0.18 * glow)
        g.rc(0, 0, 640, 380, "#15151F", INK, lw=12, r=18)
        g.rc(0, 0, 590, 330, g.lgrad(0, -165, 0, 165, "#24345E", "#101830"), None, r=8)
        g.text(text, 0, 10 if not sub else -20, 120, col, sw=18, depth=6)
        if sub:
            g.text(sub, 0, 90, 54, PAL["cream"], sw=10)
        g.rc(0, 215, 120, 40, "#2A2A38", INK, lw=8, r=6)


def sofa(g, x=540, y=1560):
    g.rc(x, y - 120, 900, 300, "#8E2430", INK, lw=10, r=50)
    g.rc(x, y - 250, 860, 220, "#A8323E", INK, lw=10, r=60)
    for sd in (-1, 1):
        g.rc(x + sd * 470, y - 140, 130, 340, "#7A1E2A", INK, lw=10, r=50)


def pad(g, x, y, s=1.0, rot=0.0):
    with g.at(x, y, rot, s):
        g.path("M-110 -30 Q-120 60 -70 70 Q-40 74 -20 40 L20 40 Q40 74 70 70 Q120 60 110 -30 Q100 -60 0 -55 Q-100 -60 -110 -30 Z", "#2A2A38", INK, lw=8)
        g.circle(-60, -10, 16, "#5A5A6A", INK, lw=4); g.circle(60, -18, 9, "#FF6B5B", INK, lw=3); g.circle(78, 0, 9, "#5ED3B5", INK, lw=3)


def beard(g, x, y_feet, h, length):
    """Long grey 'waiting' beard + moustache on a char2 figure (feet at x, y_feet; height h). length 0..1."""
    if length <= 0: return
    k = h / 565.0
    cy = y_feet - 418 * k                                                            # chin
    L = (0.25 + length) * h * 0.26
    w = 44 * k
    sway = 6 * k * math.sin(y_feet * 0.01)
    g.path(f"M{x - w} {cy - 14 * k} Q{x - w * 1.25} {cy + L * 0.45} {x - w * 0.35 + sway} {cy + L * 0.9} L{x + sway} {cy + L * 1.05} "
           f"L{x + w * 0.35 + sway} {cy + L * 0.9} Q{x + w * 1.25} {cy + L * 0.45} {x + w} {cy - 14 * k} Q{x} {cy + 6 * k} {x - w} {cy - 14 * k} Z",
           GREY, INK, lw=max(4, 5 * k))
    for i in range(-2, 3):                                                           # hair strands
        g.path(f"M{x + i * w * 0.3} {cy + 6 * k} Q{x + i * w * 0.38 + 4 * k} {cy + L * 0.5} {x + i * w * 0.18 + sway} {cy + L * 0.88}",
               None, shade(GREY, 0.78), lw=max(2, 3 * k))
    g.path(f"M{x - 30 * k} {cy - 34 * k} Q{x - 14 * k} {cy - 46 * k} {x} {cy - 38 * k} Q{x + 14 * k} {cy - 46 * k} {x + 30 * k} {cy - 34 * k} "
           f"Q{x + 14 * k} {cy - 26 * k} {x} {cy - 32 * k} Q{x - 14 * k} {cy - 26 * k} {x - 30 * k} {cy - 34 * k} Z", GREY, INK, lw=max(3, 4 * k))

def cobweb(g, x, y, r, k=1.0, flip=1):
    if k <= 0: return
    for i in range(5):
        a = math.radians(0 + i * 22)
        g.line([(x, y), (x + flip * r * math.cos(a), y + r * math.sin(a))], "#E6E1F0", 3, a=0.7 * k)
    for j in range(1, 4):
        pts = [(x + flip * r * j / 4 * math.cos(math.radians(i * 22)), y + r * j / 4 * math.sin(math.radians(i * 22))) for i in range(5)]
        g.line(pts, "#E6E1F0", 3, a=0.7 * k)


def calendar(g, x, y, s, year, k=1.0, month=None, stamp=0.0, stamp_txt="DELAYED"):
    with g.at(x, y, -0.03, s * back_out(clamp(k), 1.5)):
        g.rc(0, 0, 420, 460, "#FFF4E0", INK, lw=10, r=16)
        g.rc(0, -170, 420, 120, "#FF6B5B", INK, lw=10, r=16)
        for i in (-120, 120):
            g.rc(i, -230, 26, 70, "#5A5A6A", INK, lw=6, r=8)
        if month:
            g.text(month, 0, -160, 64, "#FFF4E0", sw=8)
        g.text(str(year), 0, 60 if not month else 70, 150 if not month else 130, INK, stroke=None)
        if stamp > 0:
            with g.at(0, 40, -0.25, back_out(clamp(stamp), 2.2) * 1.0):
                g.rc(0, 0, 400, 110, None, "#D7263D", lw=12, r=12)
                g.text(stamp_txt, 0, 8, 76, "#D7263D", stroke=None)


def game_box(g, x, y, s, label="5"):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 150, 200, "#2A2A38", INK, lw=7, r=10)
        g.rc(0, 10, 120, 150, "#3E7CB1", None, r=6)
        g.text(label, 0, 26, 90, PAL["cream"], sw=10)


def gamer(g, x, y, h, expr, beard_len, t, pose=("hold", "hold"), flip=False):
    char2(g, "modern", x, y, h, expr, pose[0], pose[1], t=t, prop=False, flip=flip)
    beard(g, x, y, h, beard_len)


# ------------------------------------------------------------------ shots
def s_hook(g, c):
    """Frame 1: the gamer on his sofa, long grey beard, cobwebs, controller in hand, TV asking 'GTA 6?'."""
    room(g, c.gt)
    tv(g, 790, 1000, 0.62, c.gt)
    sofa(g)
    gamer(g, 380, 2420, 1550, "suspicious", 1.0, c.gt)
    pad(g, 380, 1580, 1.3, 0.05 * math.sin(c.gt * 3))
    cobweb(g, 0, 0, 260); cobweb(g, W, 0, 260, flip=-1)


def s_2013(g, c):
    room(g, c.gt)
    tv(g, 790, 900, 0.62, c.gt, "GTA 5", PAL["yellow"], sub="2013")
    sofa(g)
    gamer(g, 380, 2420, 1550, "smug", 0.0, c.gt)
    pad(g, 380, 1580, 1.3)
    calendar(g, 800, 640, 0.55, 2013, pop(c.t, c.w("2013") - 0.2, 0.35))


def s_few_years(g, c):
    room(g, c.gt)
    sofa(g)
    gamer(g, 380, 2420, 1550, "curious", 0.0, c.gt, pose=("hip", "hold"))
    with g.at(780, 820, 0, back_out(seg(c.t, c.w("few") - 0.3, 0.35), 1.6)):
        g.rc(0, 0, 420, 170, "#FFFFFF", INK, lw=8, r=60)
        g.text("2-3 YEARS?", 0, 8, 70, "#22181B", stroke=None)


def s_western(g, c):
    """Rockstar's studios together on one giant western: sunset, cactus, a horse and rider silhouette crossing."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#FF9A4C", "#7A2E3E"))
    g.circle(540, 900, 260, "#FFD27A", None)
    g.rect(-100, 1180, W + 200, 800, "#3A1E1E", None)
    for x, hgt in ((180, 420), (900, 320)):
        g.rc(x, 1180 - hgt / 2, 60, hgt, "#2A1414", None, r=30)
        g.rc(x - 60, 1180 - hgt * 0.6, 40, hgt * 0.35, "#2A1414", None, r=20); g.rc(x + 60, 1180 - hgt * 0.7, 40, hgt * 0.3, "#2A1414", None, r=20)
    xr = -260 + 1600 * c.u
    D = "#140A0A"
    with g.at(xr, 1180):
        for i, dx in enumerate((-95, -60, 70, 105)):                                 # legs (gallop)
            a = 0.45 * math.sin(c.gt * 11 + i * 1.7)
            with g.at(dx, -95, a):
                g.rc(0, 48, 20, 100, D, None, r=8)
        g.ellipse(0, -130, 150, 58, D, None)                                         # body
        g.path("M110 -160 Q150 -230 175 -270 L215 -262 Q215 -235 185 -215 Q165 -180 140 -120 Z", D, None)   # neck + head
        g.path("M-140 -150 Q-200 -120 -205 -60 Q-180 -110 -140 -125 Z", D, None)                          # tail
        g.rc(-5, -235, 56, 110, D, None, r=22)                                       # rider
        g.circle(-5, -305, 26, D, None)
        g.ellipse(-5, -322, 66, 12, D, None); g.rc(-5, -340, 50, 34, D, None, r=8)   # hat
    with g.screen():
        g.text("ONE GIANT WESTERN", W / 2, 420, 92, PAL["cream"], sw=18, depth=8, sc=pop(c.t, c.w("western") - 0.2, 0.3))


def s_2018(g, c):
    room(g, c.gt)
    sofa(g)
    gamer(g, 380, 2420, 1550, "bored", 0.25, c.gt)
    yrs = [2014, 2015, 2016, 2017, 2018]
    i = min(4, int(c.u * 5.5))
    calendar(g, 790, 880, 0.75, yrs[i], 1.0)


def s_selling(g, c):
    room(g, c.gt, 0.6)
    n = int(clamp(c.u * 1.3) * 36)
    for i in range(n):                                                               # a pile of game boxes grows
        x = 140 + (i % 6) * 160; y = 1700 - (i // 6) * 210
        game_box(g, x, y, 1.0)
    cnt = int(200 * ease_out(clamp((c.t - 0.3) / max(0.5, c.T - 1.0))))
    with g.screen():
        g.text(f"{cnt},000,000+", W / 2, 420, 110, PAL["yellow"], sw=20, depth=8)
        g.text("COPIES OF GTA 5", W / 2, 540, 70, PAL["cream"], sw=12)


def s_beard_grows(g, c):
    room(g, c.gt)
    tv(g, 790, 900, 0.62, c.gt, "GTA 6?", glow=0.6)
    sofa(g)
    gamer(g, 380, 2420, 1550, "bored", 0.25 + 0.35 * c.u, c.gt)
    cobweb(g, 0, 0, 160 * c.u, k=c.u)


def s_trailer(g, c):
    room(g, c.gt)
    tv(g, 790, 900, 0.62, c.gt, "TRAILER", PAL["yellow"], glow=1.6, sub="2023")
    sofa(g)
    gamer(g, 380, 2420, 1550, "shocked" if c.t > 0.4 else "bored", 0.6, c.gt, pose=("up", "up"))
    burst(g, 790, 900, 220, 320, 14, PAL["yellow"], 12, k=seg(c.t, 0.2, 0.5))


def s_views(g, c):
    studio_v(g, c.gt)
    cnt = int(93 * ease_out(clamp((c.t - 0.2) / max(0.5, c.T * 0.7))))
    with g.at(540, 900, 0, back_out(seg(c.t, 0.0, 0.35), 1.6)):
        g.rc(0, 0, 820, 470, "#FFFFFF", INK, lw=12, r=36)
        g.poly([(-60, -70), (-60, 70), (70, 0)], "#FF3B30", INK, lw=8, r=8)
        g.text(f"{cnt},000,000", 0, 160, 92, "#22181B", stroke=None)
        g.text("VIEWS", 0, -165, 60, "#22181B", stroke=None)
    with g.screen():
        g.text("IN 1 DAY", W / 2, 470, 120, PAL["yellow"], sw=22, depth=10, sc=pop(c.t, c.w("day") - 0.2, 0.3))


def studio_v(g, t):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, "#3E7CB1", "#26507A", "#10263B"))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def s_delayed(g, c):
    room(g, c.gt)
    sofa(g)
    gamer(g, 300, 2250, 1350, "worried", 0.75, c.gt, pose=("hold", "hold"))
    k_may = seg(c.t, c.w("may") - 0.3, 0.3); k_nov = seg(c.t, c.w("november") - 0.3, 0.3)
    calendar(g, 760, 760, 0.75, 2026, 1.0, month="MAY", stamp=seg(c.t, c.w("delayed") - 0.1, 0.3))
    if k_nov > 0:
        calendar(g, 800, 1100, 0.75, 2026, k_nov, month="NOV")


def s_twice(g, c):
    studio_v(g, c.gt)
    for i, (txt, y) in enumerate((("DELAYED", 760), ("DELAYED", 1050))):
        k = back_out(seg(c.t, 0.1 + i * 0.35, 0.3), 2.2)
        if k > 0:
            with g.at(540, y, -0.2 + 0.3 * i, k):
                g.rc(0, 0, 760, 200, None, "#D7263D", lw=18, r=16)
                g.text(txt, 0, 12, 140, "#D7263D", stroke=None)


def s_loop(g, c):
    """Last shot = frame 1 (loop): beard, cobwebs, TV now says GTA 6 (no question mark); 'Worth the wait?'."""
    room(g, c.gt)
    tv(g, 790, 1000, 0.62, c.gt, "GTA 6", PAL["yellow"], glow=1.4)
    sofa(g)
    gamer(g, 380, 2420, 1550, "smug" if c.t < c.w("worth") - 0.2 else "suspicious", 1.0, c.gt)
    pad(g, 380, 1580, 1.3)
    cobweb(g, 0, 0, 260); cobweb(g, W, 0, 260, flip=-1)
    sparkles(g, c.gt, [(300, 700), (780, 700)], r=26)


V.shot("H1", s_hook, sfx=[(0.0, "pop", 0.3)], tr="cut")
V.shot("L01", s_2013, (0, "Fans"), sfx=[("2013", "ding", 0.35)])
V.shot("L01", s_few_years, ("Fans", 1), sfx=[("few", "hmm", 0.35)])
V.shot("L02", s_western, (0, "It"), music="adventure", sfx=[(0.1, "whoosh", 0.35)])
V.shot("L02", s_2018, ("It", 1), sfx=[(0.1, "page_turn", 0.3), ("2018", "ding", 0.35)])
V.shot("L03", s_selling, (0, "More"), music="playful", sfx=[(0.3, "coins", 0.3)])
V.shot("L03", s_beard_grows, ("More", 1))
V.shot("L04", s_trailer, (0, "it"), sfx=[(0.2, "swell", 0.4)])
V.shot("L04", s_views, ("it", 1), sfx=[("day", "ding", 0.45)])
V.shot("L05", s_delayed, (0, "Twice"), sfx=[("delayed", "drum_hit", 0.45)])
V.shot("L05", s_twice, ("Twice", 1), sfx=[(0.1, "drum_hit", 0.4), (0.45, "drum_hit", 0.4), ("november", "hmm", 0.3)])
V.shot("L06", s_loop, sfx=[("worth", "pop", 0.35)])
V.build()
split_long(V)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=9, scale=0.14))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-020.mp4"))
