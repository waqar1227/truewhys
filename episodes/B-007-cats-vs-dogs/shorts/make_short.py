"""B-007 cut Short C1 "puppy eyes", re-composed vertically (1080x1920) with its own hook and script (not a crop of L7):
frame-1 rule (motion + sound at 0.0 s, face + object + <= 4-word question), answer at the end, last shot loops to the first, corner badge.
python episodes/B-007-cats-vs-dogs/shorts/make_short.py C1 sheet|qa|times <t,..> <out>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import arrow, burst
from flat_pets import *

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-puppy-eyes"}
EP = HERE / DIRS[SID]
FL = 1560
SHELTER = [dict(DOG, fur="#3A3030", ear="#22181B", light="#E8E0D0"), dict(DOG, fur="#B5652A", ear="#7A3E1E")]


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


def tag(g, txt, x, y, k=1.0, size=50):
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def studio(g, t, a="#E9A15A", b="#6B3420"):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, a, shade(a, 0.5), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def cross(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, "#FF5B4B", INK, lw=r * 0.12)
        g.line([(-0.4 * r, -0.4 * r), (0.4 * r, 0.4 * r)], INK, r * 0.2); g.line([(-0.4 * r, 0.4 * r), (0.4 * r, -0.4 * r)], INK, r * 0.2)


def heart(g, x, y, r, k=1.0):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.6) * r / 40):
        g.path("M0 30 Q-60 -10 -36 -40 Q-14 -60 0 -30 Q14 -60 36 -40 Q60 -10 0 30 Z", "#FF5B6B", INK, lw=5)


def kitchen_v(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE3B8", "#F2B98A"))
    with g.layer(0.6):
        g.rect(560, 300, 400, 420, "#BFE6F2", INK, lw=10, r=12)
        g.line([(760, 300), (760, 720)], INK, 8); g.line([(560, 510), (960, 510)], INK, 8)
        for i in range(5):
            g.rect(-40 + i * 230, 840, 210, 300, "#FFF4E0", INK, lw=6, r=8)
    g.rect(-100, FL, W + 200, H, "#B9844F", INK, lw=8)


def table_sandwich(g, t, bite=0.0):
    """Table edge in the foreground left with a plate and a sandwich."""
    g.rect(-100, 1080, 640, 70, "#C98E5A", INK, lw=8, r=12)
    g.rect(-100, 1150, 640, 40, "#A86E3E", INK, lw=6)
    g.ellipse(250, 1072, 190, 30, "#FFFFFF", INK, lw=7)
    with g.at(250, 1040):
        g.path("M-130 20 Q-130 -40 0 -46 Q130 -40 130 20 Z", "#F2D27A", INK, lw=7)
        g.path("M-136 8 Q-60 -4 0 10 Q60 -4 136 8 L136 26 L-136 26 Z", "#7CC56B", INK, lw=5)
        g.path("M-130 26 L130 26 L126 44 L-126 44 Z", "#FF8A6A", INK, lw=5)
        g.path("M-134 44 Q0 70 134 44 L130 60 Q0 84 -130 60 Z", "#F2D27A", INK, lw=7)


def c1_hook(g, c, end=False):
    """Frame 1 = the eyebrows already rising at a sandwich (sound at 0.0 s); the dog face fills the lower half."""
    kitchen_v(g, c.gt)
    table_sandwich(g, c.gt)
    br = clamp(0.35 + c.t / 1.2) if not end else clamp(0.4 + c.t / 1.0)
    dog_sit(g, 700, FL + 300, 2.15, c.gt, "calm", brow=br, tongue=0.0, look=(-0.7, -0.5), blink=0.0, wag=0.6)
    for i in range(3):
        ph = (c.gt * 0.8 + i / 3) % 1
        heart(g, 120 + i * 90, 960 - 220 * ph, 30, k=1 - ph)


def c1_brows(g, c):
    studio(g, c.gt)
    br = 0.5 + 0.5 * math.sin(c.gt * 2.4)
    dog_face(g, 540, 1000, 2.6, c.gt, "calm", brow=br, look=(0, -0.4))
    arrow(g, 900, 420, 640, 650, k=on(c, "eyebrows"))
    label(g, "INNER EYEBROWS", 540, 330, 86, k=on(c, "eyebrows"))
    kb = on(c, "baby's")
    if kb > 0:
        baby_face(g, 820, 1560, 1.1 * kb, c.gt)
        label(g, "LIKE A BABY", 820, 1760, 70, PAL["cream"], k=kb)


def c1_wolf(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#F2E6D2", "#E3D3B8"))
    kf = on(c, "tiny")
    dog_face(g, 540, 640, 1.8, c.gt, "calm", brow=0.7 * kf)
    dog_face(g, 540, 1380, 1.8, c.gt, "calm", wolf=True)
    label(g, "DOG", 900, 400, 80, k=1)
    label(g, "WOLF", 900, 1130, 80, k=1)
    tag(g, "2019 · DOG AND WOLF FACES", 540, 140, on(c, "2019", frac=0.0))
    if kf > 0:
        for sd in (-1, 1):
            g.line([(540 + sd * 30 * 1.8, 640 - 76 * 1.8), (540 + sd * 85 * 1.8, 640 - 66 * 1.8)], "#FF3B3B", 16, a=0.5 + 0.5 * math.sin(c.gt * 8))
    cross(g, 540, 1230, 60, on(c, "Wolves", frac=0.9))


def c1_shelter(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#DCEBD7", "#BFD8BA"))
    ka = ease_out(clamp((c.t - 0.4 * c.T) / (0.3 * c.T)))           # the puppy-eyes dog leaves its kennel mid-line
    for i, y in enumerate((760, 1500)):
        g.rect(140, y - 620, 800, 620, "#F4F1EA", INK, lw=7, r=10)
        x = 540 + (600 * ka if i == 1 else 0)
        dog_sit(g, x, y, 0.75, c.gt, "calm", brow=0.9 if i == 1 else 0.0, tongue=0.0, col=SHELTER[i], seed=i)
        for j in range(12):
            xx = 180 + j * 66
            g.line([(xx, y - 600), (xx, y - 600 * (ka if i == 1 else 0.0))], "#5A6470", 10)
        g.line([(150, y - 600), (930, y - 600)], "#5A6470", 14)
    g.rect(-100, FL, W + 200, H, "#9AA78E", INK, lw=8)
    heart(g, 820, 1000, 60, k=ka)
    label(g, "ADOPTED FASTER", 540, 1720, 96, k=pk(c, "faster"))


def c1_gen(g, c):
    studio(g, c.gt, "#E9A15A", "#6B3420")
    k = 0.3 + 0.7 * clamp(c.t / max(0.5, c.T * 0.75))
    for i in range(4):
        kk = clamp(k * 4 - i)
        if kk > 0:
            with g.group(kk):
                dog_face(g, 400 + (i % 2) * 280, 420 + i * 340, 0.9, c.gt + i, "calm", brow=i / 3.0, wolf=(i == 0))
    arrow(g, 960, 300, 960, 1500, col=PAL["cream"], k=k)
    label(g, "THOUSANDS OF YEARS", 540, 1750, 80, PAL["cream"], k=k)


def c1_end(g, c):
    """Last shot matches frame 1 so the Short loops."""
    c1_hook(g, c, end=True)
    label(g, "WHO'S TRAINING WHO?", 540, 300, 92, k=pk(c, "training"))


def build():
    V = Video(EP, title=("MADE FOR", "YOU?"), cap_y=0.72, music="warm", sid="B007C1", captions=False)
    V.shot("H1", c1_hook, (0, "just"), tr="cut", sfx=[(0.0, "shimmer", 0.5), (0.05, "pop", 0.35)])
    V.shot("H1", c1_brows, ("just", 1), cam=push(1.0, 1.05, (540, 1000)), sfx=[("work", "sting", 0.4)])
    V.shot("L01", c1_brows, (0, "and"), cam=push(1.05, 1.1, (540, 900)), sfx=[("Up", "shimmer", 0.35)])
    V.shot("L01", c1_brows, ("and", 1), cam=push(1.0, 1.04, (640, 1100)), sfx=[("baby's", "pop", 0.4)])
    V.shot("L02", c1_wolf, (0, "Dogs"), cam=push(1.0, 1.04, (540, 900)), music="story")
    V.shot("L02", c1_wolf, ("Dogs", "Wolves"), cam=push(1.04, 1.08, (540, 860)), sfx=[("tiny", "ding", 0.4)])
    V.shot("L02", c1_wolf, ("Wolves", 1), cam=push(1.04, 1.08, (540, 1100)), sfx=[("don't", "bloop", 0.4)])
    V.shot("L03", c1_shelter, cam=push(1.0, 1.04, (540, 1000)), music="warm", sfx=[("homes", "chime", 0.4)])
    V.shot("L04", c1_gen, cam=push(1.0, 1.04, (540, 1000)), music="story", sfx=[("thousands", "whoosh_soft", 0.35)])
    V.shot("L05", c1_end, cam=push(1.0, 1.05, (600, 1100)), music="playful", sfx=[(0.1, "shimmer", 0.4)])
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
        V.render(str(EP / f"final/B-007-{SID}.mp4"))
