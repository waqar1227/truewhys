"""A-013 "The Falling Cat That Broke Physics" — standalone Short, Style F + cast v2.1 (audit §6.3).
python episodes/A-013-falling-cat/make.py sheet|render|qa|big <t,t,..>
Animal welfare: nobody drops a cat on screen; the cat jumps by itself and lands on a cushion.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, sparkles, arrow, no_sign

V = Video(EP, title=("THE FALLING CAT", "THAT BROKE PHYSICS"), cap_y=0.70,
          keys={"upside", "1894", "impossible", "paris", "marey", "super-fast", "camera", "somehow", "over", "baffled", "nothing", "push", "hand",
                "1969", "bends", "middle", "twists", "front", "back", "zero", "feet", "mid-air"}, music="curious")
FUR, FUR_D, BELLY = "#F29A3E", "#C8701F", "#FFE3C2"


# ------------------------------------------------------------------ the cat (two halves that roll separately)
def _roll(g, phi):
    """Scale about the body axis to fake a roll around the spine: cos(phi) < 0 = upside down."""
    k = math.cos(phi)
    return g.at(0, 0, 0, 1.0, k if abs(k) > 0.04 else 0.04 * (1 if k >= 0 else -1))


def cat(g, x, y, s=1.0, rot=0.0, front=0.0, back=0.0, bend=0.0, t=0.0, legs=0.0, tail_w=1.0, expr="calm"):
    """Side view, facing right. front/back = roll angle of each half (0 = feet down, pi = feet up). bend = arch at the waist (rad)."""
    with g.at(x, y, rot, s):
        # back half (drawn first)
        with g.at(-10, 0, -bend * 0.5):
            with _roll(g, back):
                tw = math.sin(t * 3) * 0.3 * tail_w
                g.path(f"M-150 -10 Q-260 {-60 + 40 * tw} -300 {-150 + 60 * tw} Q-306 {-176 + 60 * tw} -290 {-168 + 60 * tw} "
                       f"Q-250 {-70 + 40 * tw} -150 10 Z", FUR_D, INK, lw=8)
                for dx in (-120, -60):
                    sw = 18 * math.sin(t * 8 + dx) * legs
                    g.limb([(dx, 40), (dx + sw, 110), (dx + sw + 8, 150)], FUR, 34, lw=8)
                g.ellipse(-80, 0, 110, 70, FUR, INK, lw=9)
                g.ellipse(-80, 34, 80, 28, BELLY, None)
                for i in range(3):
                    g.path(f"M{-130 + i * 40} -62 Q{-120 + i * 40} -30 {-128 + i * 40} -6", None, FUR_D, lw=8)
        # front half
        with g.at(10, 0, bend * 0.5):
            with _roll(g, front):
                for dx in (60, 120):
                    sw = 18 * math.sin(t * 8 + dx + 1) * legs
                    g.limb([(dx, 40), (dx + sw, 110), (dx + sw + 8, 150)], FUR, 34, lw=8)
                g.ellipse(70, 0, 110, 72, FUR, INK, lw=9)
                g.ellipse(70, 36, 80, 28, BELLY, None)
                # head
                g.poly([(150, -100), (170, -170), (205, -110)], FUR, INK, lw=8)
                g.poly([(225, -110), (262, -170), (272, -96)], FUR, INK, lw=8)
                g.poly([(160, -110), (172, -150), (192, -114)], "#FFB0A0", None)
                g.circle(210, -50, 82, FUR, INK, lw=9)
                g.ellipse(232, -20, 46, 32, BELLY, None)
                big = expr == "shock"
                for ex in (196, 244):
                    g.ellipse(ex, -66, 13 if big else 11, 18 if big else 13, "#FFFFFF", INK, lw=5)
                    g.ellipse(ex + 2, -64, 5, 10 if big else 8, INK, None)
                g.poly([(226, -34), (240, -34), (233, -24)], "#FF7A8A", INK, lw=4)
                for sd in (-1, 1):
                    g.line([(262, -26 + sd * 8), (310, -32 + sd * 16)], INK, 3)
                for i in range(2):
                    g.path(f"M{180 + i * 30} -128 Q{186 + i * 30} -110 {180 + i * 30} -98", None, FUR_D, lw=7)


def room(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE3B8", "#F2B98A"))
    with g.layer(0.55):
        g.rect(620, 300, 360, 440, "#BFE6F2", INK, lw=10, r=12)             # window
        g.line([(800, 300), (800, 740)], INK, 8); g.line([(620, 520), (980, 520)], INK, 8)
        g.rect(60, 560, 420, 40, "#8A6A44", INK, lw=8)                        # shelf
        for i in range(4):
            g.rect(90 + i * 70, 430, 50, 130, ("#FF6B5B", "#3E7CB1", "#5ED3B5", "#FFC93C")[i], INK, lw=6, r=4)
    g.rect(-100, 1650, W + 200, 500, "#B98A5E", INK, lw=8)
    g.rc(560, 1700, 640, 150, "#7A4FB0", INK, lw=9, r=60)                      # cushion
    g.rc(560, 1660, 560, 40, "#9A72CC", None, r=20)


def lab1894(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#E8D9B8", "#C9B48A"))
    with g.layer(0.55):
        g.rect(80, 300, 920, 520, "#5A4A3A", INK, lw=10, r=10)                 # dark backdrop cloth
        for i in range(9):
            g.line([(120 + i * 100, 300), (120 + i * 100, 820)], "#4A3A2C", 6)
    g.rect(-100, 1600, W + 200, 600, "#8A6A44", INK, lw=8)
    for i in range(10):
        g.line([(i * 120, 1600), (i * 120 - 80, 1960)], "#6E5034", 6)


def camera_1894(g, x, y, s, flash=0.0):
    with g.at(x, y, 0, s):
        for a in (-0.25, 0, 0.25):
            g.line([(0, 0), (math.sin(a) * 600, 600)], "#6E5034", 16)
        g.rc(0, -110, 300, 220, "#3A2A20", INK, lw=10, r=20)
        g.circle(170, -110, 70, "#C9A23A", INK, lw=9)
        g.circle(170, -110, 38, "#22303A", INK, lw=6)
        g.rc(-40, -240, 90, 50, "#C9A23A", INK, lw=6, r=6)
        if flash > 0:
            g.glow(170, -110, 300, "#FFFFFF", flash)


def film_strip(g, y, k, t, n=6, highlight=None):
    w = 300
    x0 = W / 2 - (n * w) / 2 + (1 - ease_out(clamp(k))) * 600 - (t * 40) % 40
    g.rect(x0 - 20, y - 230, n * w + 40, 460, "#22181B", None)
    for i in range(n):
        x = x0 + i * w
        for j in range(4):
            g.rect(x + 20 + j * 70, y - 215, 34, 22, "#F4F1EA", None, r=4); g.rect(x + 20 + j * 70, y + 193, 34, 22, "#F4F1EA", None, r=4)
        g.rect(x + 14, y - 175, w - 28, 350, "#F3EAD6" if highlight != i else "#FFF8D6", INK, lw=5)
        u = i / (n - 1)
        fr = math.pi * (1 - clamp(u * 1.6))
        bk = math.pi * (1 - clamp(u * 1.6 - 0.45))
        cat(g, x + w / 2, y - 60 + u * 120, 0.42, 0.0, fr, bk, bend=0.5 * math.sin(math.pi * u), t=0, tail_w=0)


# ------------------------------------------------------------------ shots
def s_hook(g, c):
    """Frame 1: the cat upside down in mid-air (object in action) + the Everyman staring."""
    room(g, c.gt)
    char2(g, "modern", 300, 2350, 1800, "shocked" if c.t > 0.5 else "curious", "down", "up" if c.t > 0.5 else "down", t=c.gt)
    u = clamp(c.t / max(c.T, 0.1))
    cat(g, 700, 900 + 120 * u, 1.35, 0.1, math.pi * (1 - 0.12 * u), math.pi, bend=0.15, t=c.gt, legs=0.6, expr="shock")


def s_paris(g, c):
    lab1894(g, c.gt)
    camera_1894(g, 330, 1300, 1.25, flash=0.8 * max(0.0, 1 - ((c.gt * 2.5) % 1.0) * 4))
    char2(g, "gent", 800, 2080, 1250, "smug", "down", "down", t=c.gt)
    if c.sh["line"] == "H1":
        with g.screen():
            g.text("PARIS 1894", W / 2, 660, 120, PAL["yellow"], sw=22, depth=8, sc=pop(c.t, 0.0, 0.3), rot=-0.05)


def s_strip(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#3A4466", "#1E2440", "#10142A"))
    sw_ = c.w("somehow") if c.sh["line"] == "L02" else 99.0
    hl = min(5, int(clamp((c.t - sw_ + 0.4) / 1.2) * 6)) if c.t > sw_ - 0.4 else None
    film_strip(g, 720, seg(c.t, 0, 0.5), c.gt, highlight=hl)
    cat(g, 520, 1480 - 60 * math.sin(c.gt * 2), 1.35, 0.0, math.pi * (1 - ease_io(seg(c.t, sw_, 1.0))),
        math.pi * (1 - ease_io(seg(c.t, sw_ + 0.4, 1.0))), bend=0.4 * math.sin(math.pi * seg(c.t, sw_, 1.4)), t=c.gt, legs=0.3)


def s_baffled(g, c):
    lab1894(g, c.gt)
    with g.layer(0.7):
        g.rect(120, 380, 560, 340, "#2E5E4A", INK, lw=10, r=10)
        g.text("NO PUSH", 400, 500, 80, "#F4F1EA", stroke=None)
        g.text("= NO SPIN ?", 400, 610, 70, "#F4F1EA", stroke=None)
    char2(g, "prof", 360, 2100, 1300, "shocked" if c.t < c.w("nothing") else "suspicious", "up" if c.t < c.w("nothing") else "hip", "hip", t=c.gt)
    char2(g, "gent", 830, 2120, 1150, "suspicious", "hip", "down", t=c.gt, flip=True)
    qmark(g, 900, 760, 200, PAL["yellow"], 0.12, pop(c.t, c.w("turning") - 0.2, 0.3))


def s_hand(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    with g.at(220, 700, 0.4, 1.6):                                              # a plain cartoon hand, open (just let go)
        g.rc(0, 0, 150, 120, "#F1CDB0", INK, lw=8, r=40)
        for i in range(4):
            g.rc(-50 + i * 34, -90, 28, 90, "#F1CDB0", INK, lw=7, r=14)
        g.rc(90, 10, 80, 30, "#F1CDB0", INK, lw=7, r=14)
    cat(g, 600, 1200, 1.2, -0.3, math.pi * 0.85, math.pi, bend=0.1, t=c.gt, legs=0.4, expr="shock")
    k = ease_out(seg(c.t, c.w("pushed") - 0.2, 0.4))
    arrow(g, 360, 820, 460, 960, "#FF8A6B", w=26, k=k)
    with g.screen():
        g.text("PUSH?", 760, 600, 120, "#FF8A6B", sw=22, depth=8, sc=pop(c.t, c.w("pushed") - 0.1, 0.3))
    char2(g, "prof", 860, 2160, 1050, "suspicious", "down", "point", t=c.gt, flip=True)


def s_1969(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#F6C98E", "#E39B5A"))
    with g.at(540, 820, -0.04, 0.4 + 0.6 * back_out(seg(c.t, c.w("1969") - 0.2, 0.4))):
        g.rc(0, 0, 520, 380, "#FFF4E0", INK, lw=12, r=24)
        g.rc(0, -140, 520, 100, "#3E7CB1", INK, lw=12, r=24)
        g.text("1969", 0, 60, 170, "#22181B", stroke=None)
    bk = ease_io(seg(c.t, c.w("bends") - 0.2, 0.6))
    cat(g, 540, 1500, 1.25, 0.0, math.pi, math.pi, bend=0.9 * bk, t=c.gt, legs=0.2)
    if bk > 0.1:
        g.path("M430 1330 Q540 1240 650 1330", None, PAL["yellow"], lw=14, a=bk)


def s_twist(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#F6C98E", "#E39B5A"))
    fr = math.pi * (1 - ease_io(seg(c.t, c.w("front") - 0.3, 0.9)))
    bk = math.pi * (1 - ease_io(seg(c.t, c.w("back") - 0.3, 0.9)))
    cat(g, 540, 1150, 1.6, 0.0, fr, bk, bend=0.7, t=c.gt, legs=0.2)
    kf_ = ease_out(seg(c.t, c.w("front") - 0.2, 0.3)); kb = ease_out(seg(c.t, c.w("back") - 0.2, 0.3))
    if kf_ > 0:   # curved arrows: opposite directions
        g.path("M700 880 Q860 940 820 1080", None, "#3E7CB1", lw=20, a=kf_)
        arrow(g, 830, 1040, 815, 1100, "#3E7CB1", w=26, k=kf_)
    if kb > 0:
        g.path("M380 1420 Q220 1360 260 1220", None, "#FF6B5B", lw=20, a=kb)
        arrow(g, 250, 1260, 262, 1200, "#FF6B5B", w=26, k=kb)
    with g.screen():
        g.text("NO PUSH", W / 2, 600, 120, PAL["yellow"], sw=22, depth=8, sc=pop(c.t, c.w("No") - 0.1, 0.3))


def s_land(g, c):
    room(g, c.gt)
    u = ease_in(seg(c.t, 0.0, 1.1))
    y = lerp(900, 1560, u)
    sq = 0.12 * math.sin(math.pi * seg(c.t, 1.1, 0.35)) if c.t > 1.1 else 0
    cat(g, 560, y, 1.3 * (1 + sq * 0.5), 0.0, 0.0, 0.0 if c.t > 0.5 else math.pi * (1 - c.t / 0.5), bend=0.0, t=c.gt, legs=0.0, expr="calm")
    with g.at(860, 760, 0, pop(c.t, c.w("zero") - 0.1, 0.35)):
        g.rc(0, 0, 360, 200, "#FFF4E0", INK, lw=10, r=30)
        g.text("SPIN", 0, -40, 60, "#22181B", stroke=None)
        g.text("= 0", 0, 40, 90, "#3E7CB1", stroke=None)
    if c.t > 1.1:
        sparkles(g, c.gt, [(420, 1560), (720, 1560)], r=30 * (1 - seg(c.t, 1.1, 0.8)))


def s_you(g, c):
    """Last shot = frame 1 (loop): the same room, the cat upside down in the air again, the Everyman asked."""
    room(g, c.gt)
    char2(g, "modern", 300, 2350, 1800, "smug" if c.t > c.w("mid-air") - 0.3 else "curious", "down", "down", t=c.gt)
    cat(g, 700, 900, 1.35, 0.1, math.pi, math.pi, bend=0.15, t=c.gt, legs=0.6, expr="shock")


V.shot("H1", s_hook, part=(0, "In"), sfx=[(0.0, "whoosh_soft", 0.4), (0.4, "cat_meow", 0.35)])
V.shot("H1", s_paris, part=("In", 1), tr="flash", music="mystery", sfx=[("1894", "click", 0.4), ("impossible", "sting", 0.3)])
V.shot("L01", s_strip, part=(0, "photographed"), sfx=[(0.0, "whoosh", 0.35)])
V.shot("L01", s_paris, part=("photographed", 1), cam=push(1.45, 1.6, (380, 1180)), sfx=[("camera", "click", 0.5)])
V.shot("L02", s_strip, cam=push(1.0, 1.06, (540, 1300)), sfx=[("somehow", "swell", 0.35)])
V.shot("L03", s_baffled, music="playful", sfx=[("baffled", "hmm", 0.45)])
V.shot("L04", s_hand, sfx=[("pushed", "boing", 0.35)])
V.shot("L05", s_1969, part=(0, "The#1"), music="curious", sfx=[("1969", "ding", 0.4)])
V.shot("L05", s_1969, part=("The#1", 1), cam=push(1.25, 1.35, (540, 1420)), sfx=[("bends", "creak", 0.35)])
V.shot("L06", s_twist, part=(0, "and#1"), cam=push(1.0, 1.05, (540, 1150)), sfx=[("twists", "whoosh_soft", 0.4)])
V.shot("L06", s_twist, part=("and#1", 1), cam=push(1.12, 1.0, (540, 1250)), sfx=[("back", "whoosh_soft", 0.4)])
V.shot("L07", s_land, sfx=[(1.1, "thud", 0.4), ("feet", "shimmer", 0.4)])
V.shot("L08", s_you, cam=push(1.0, 1.04, (540, 1200)), sfx=[(0.1, "cat_meow", 0.25)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=2, cols=8, scale=0.16))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-013.mp4"))
