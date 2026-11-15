"""A-012 "Why Pen Caps Have a Tiny Hole" — standalone Short, Style F + cast v2.1 (audit §6.3).
python episodes/A-012-pen-cap-hole/make.py sheet|render|qa|big <t,t,..>
Safety topic told calmly: no one is shown choking; the airway is a simple tube diagram.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, no_sign, sparkles, arrow

V = Video(EP, title=("WHY PEN CAPS HAVE", "A TINY HOLE"), cap_y=0.70,
          keys={"hole", "ink", "chew", "breathes", "accident", "airway", "cork", "safety", "kids", "air", "eight", "litres", "minute", "stuck",
                "big", "swallow", "side", "different", "flowing", "pen", "breathe", "chewing"}, music="curious")
CAP, CAP_D = "#2F6FD0", "#1E4E9C"
BARREL = "#DCEFF8"


# ------------------------------------------------------------------ props
def cap(g, x, y, s=1.0, rot=0.0, glow=0.0, t=0.0):
    """Pen cap: (x, y) = closed tip (with the hole); the cap body runs along +x after rotation."""
    with g.at(x, y, rot, s):
        if glow > 0:
            g.glow(0, 0, 150, "#FFE08A", 0.7 * glow)
            g.circle(0, 0, 70 + 10 * math.sin(t * 6), None, "#FFC93C", lw=8, a=glow)
        g.path("M0 -34 Q-10 0 0 34 L300 40 L300 -40 Z", CAP, INK, lw=9)
        g.path("M60 -38 L300 -44 L300 -26 L60 -24 Z", "#FFFFFF", None, a=0.25)
        g.path("M80 -42 L80 -70 L280 -70 Q300 -70 300 -50 L300 -42 Z", CAP_D, INK, lw=8)   # clip
        g.circle(4, 0, 12, INK, None)                                       # the hole


def pen(g, x, y, s=1.0, rot=0.0, capped=True, glow_cap=0.0, glow_side=0.0, xray=0.0, t=0.0):
    """Clear ballpoint, side view: (x, y) = writing tip, body along +x."""
    with g.at(x, y, rot, s):
        g.path("M0 0 L60 -16 L60 16 Z", "#C8CED6", INK, lw=6)
        g.rc(50, 0, 40, 40, "#C8CED6", INK, lw=6, r=6)
        g.path("M70 -30 L560 -36 L600 -26 L600 26 L560 36 L70 30 Z", BARREL, INK, lw=9)
        g.line([(90, 0), (560, 0)], "#2050B0", 12)                          # ink tube
        if xray > 0:
            u = (t * 0.8) % 1.0
            for i in range(5):
                xx = 100 + ((u + i / 5) % 1.0) * 440
                g.circle(xx, 0, 6, "#7FB8FF", None, a=xray)
            for i in range(3):                                              # air coming in through the side hole
                k = ((t * 1.2 + i / 3) % 1.0)
                g.circle(330 + 10 * math.sin(k * 9), -110 + 80 * k, 10 * (1 - k) + 4, "#FFFFFF", INK, lw=3, a=xray * (1 - k))
        if glow_side > 0:
            g.glow(330, -32, 110, "#FFE08A", 0.8 * glow_side)
        g.circle(330, -24, 7, INK, None)                                    # side hole
        g.rc(610, 0, 40, 52, CAP, INK, lw=7, r=8)                           # end plug
        if capped:
            cap(g, -40, 0, 1.0, 0.0, glow_cap, t)


def big_cap_scene_bg(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#F6C98E", "#E39B5A"))
    with g.layer(0.5):
        for i in range(8):
            g.circle(120 + i * 130, 300 + 80 * math.sin(i), 40, "#FFFFFF", None, a=0.15)


def desk_room(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#BFE6F2", "#8FCBE0"))
    with g.layer(0.55):
        g.rect(120, 300, 840, 420, "#2E5E4A", INK, lw=10, r=12)              # chalkboard
        g.text("A B C", 360, 470, 90, "#F4F1EA", stroke=None)
        g.text("1 + 2 = 3", 620, 600, 70, "#F4F1EA", stroke=None)
    g.rect(-100, 1500, W + 200, 600, "#D9B98A", INK, lw=8)


def airway(g, x, y, s, holed, k_air, t, blocked_mark=0.0):
    """Simple windpipe diagram (a tube with rings) with a cap stuck in it; air arrows pass only through a holed cap."""
    with g.at(x, y, 0, s):
        g.rect(-130, -700, 260, 1400, "#F2B9A0", INK, lw=10, r=40)
        g.rect(-90, -700, 180, 1400, "#F7D3C2", None)
        for j in range(9):
            g.path(f"M-130 {-620 + j * 150} Q0 {-590 + j * 150} 130 {-620 + j * 150}", None, "#E39B86", lw=12)
        cap(g, 0, 60, 1.25, -math.pi / 2, glow=0.0, t=t)
        if holed:
            for i in range(4):
                u = (t * 0.9 + i / 4) % 1.0
                yy = 600 - u * 1250
                if -130 < yy < 140:
                    continue
                arrow(g, 0, yy + 70, 0, yy - 50, "#5ED3B5", w=24, head=2.2, k=k_air)
        else:
            for i in range(3):
                u = (t * 0.9 + i / 3) % 1.0
                yy = 600 - u * 380
                arrow(g, 0, yy + 70, 0, yy - 40, "#FF8A6B", w=24, head=2.2, k=k_air)
            if blocked_mark > 0:
                with g.at(230, 60, 0, back_out(clamp(blocked_mark))):
                    g.line([(-50, -50), (50, 50)], "#FF3B30", 22); g.line([(-50, 50), (50, -50)], "#FF3B30", 22)


def gauge(g, x, y, s, v, label):
    with g.at(x, y, 0, s):
        g.circle(0, 0, 300, "#FFF4E0", INK, lw=14)
        for i in range(11):
            a = math.pi * (0.8 + 1.4 * i / 10)
            g.line([(240 * math.cos(a), 240 * math.sin(a)), (280 * math.cos(a), 280 * math.sin(a))], INK, 10)
        g.line([(250 * math.cos(math.pi * (0.8 + 1.4 * i / 30)), 250 * math.sin(math.pi * (0.8 + 1.4 * i / 30))) for i in range(31)], "#5ED3B5", 26)
        a = math.pi * (0.8 + 1.4 * clamp(v))
        g.line([(0, 0), (220 * math.cos(a), 220 * math.sin(a))], "#FF3B30", 16)
        g.circle(0, 0, 26, INK, None)
        g.text(label, 0, 170, 80, "#22181B", stroke=None)


def chew_head(g, c, x, y, h, expr, chomp=True, show_cap=True):
    """The Everyman chewing a cap: the cap sticks out of the corner of his mouth."""
    char2(g, "modern", x, y, h, expr, "down", "down", t=c.gt)
    k = h / 565.0
    mx, my = x + 10 * k, y - 447 * k
    if show_cap:
        cap(g, mx + 6 * k, my + (3 * k * math.sin(c.gt * 12) if chomp else 0), 0.55 * k / 2.2, 0.25, t=c.gt)


# ------------------------------------------------------------------ shots
def s_hook(g, c):
    """Frame 1: the giant pen cap with its hole (object) + the Everyman looking at it, suspicious."""
    big_cap_scene_bg(g, c)
    char2(g, "modern", 660, 2520, 1900, "suspicious", "down", "down", t=c.gt)
    cap(g, 250, 1520, 2.3, -0.62 + 0.04 * math.sin(c.gt * 1.6), glow=0.6 + 0.4 * math.sin(c.gt * 4) ** 2, t=c.gt)


def s_notink(g, c):
    big_cap_scene_bg(g, c)
    cap(g, 220, 1000, 2.2, 0.08, glow=1.0, t=c.gt)
    with g.at(540, 1500, 0, 1.0):
        g.path("M0 -130 Q-100 20 -88 70 Q-70 140 0 140 Q70 140 88 70 Q100 20 0 -130 Z", "#2050B0", INK, lw=10)
    no_sign(g, 540, 1520, 200, pop(c.t, c.w("not") - 0.1, 0.35))


def s_chew(g, c):
    desk_room(g, c.gt)
    chew_head(g, c, 540, 2400, 1900, "bored")


def s_oops(g, c):
    desk_room(g, c.gt)
    late = c.t > c.w("breathes") - 0.1
    chew_head(g, c, 540, 2400, 1900, "shocked" if late else "bored", chomp=not late, show_cap=not late)
    if late:
        qmark(g, 860, 760, 200, PAL["yellow"], 0.15, pop(c.t, c.w("breathes") - 0.05, 0.3))


def s_cork(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    airway(g, 400, 1150, 0.95, False, ease_out(seg(c.t, 0.1, 0.4)), c.gt, blocked_mark=seg(c.t, c.w("plug") - 0.1, 0.3))
    with g.at(820, 1300, 0.2, pop(c.t, c.w("cork") - 0.1, 0.35)):                # a cork, for the comparison
        g.path("M-70 -90 L70 -90 L54 90 L-54 90 Z", "#C99A62", INK, lw=9)
        for i in range(5):
            g.circle(-30 + (i % 3) * 30, -40 + (i // 3) * 60, 7, "#8A6A44", None)
    g.text("AIRWAY", 400, 380, 70, "#FFFFFF", sw=12)


def s_standard(g, c):
    desk_room(g, c.gt)
    char2(g, "doctor", 300, 2080, 1250, "deadpan", "down", "hold", t=c.gt, prop=False)
    with g.at(760, 1150, 0.05, back_out(seg(c.t, 0.0, 0.4), 1.5)):
        g.rc(0, 0, 520, 680, "#B07A4A", INK, lw=10, r=16)
        g.rc(0, 30, 440, 580, "#FFFFFF", INK, lw=7, r=6)
        g.text("SAFETY", 0, -180, 74, "#22181B", stroke=None)
        g.text("STANDARD", 0, -110, 64, "#B0413E", stroke=None)
        g.text("ISO 11540", 0, -40, 50, "#22181B", stroke=None)
        for j in range(5):
            g.line([(-170, 40 + j * 50), (170 if j % 2 else 90, 40 + j * 50)], "#9AA3AD", 10)


def s_kids(g, c):
    desk_room(g, c.gt)
    g.rect(140, 1280, 800, 70, "#C9A27A", INK, lw=9, r=10)                     # school desk
    g.rect(190, 1350, 40, 500, "#8A6A44", INK, lw=7); g.rect(850, 1350, 40, 500, "#8A6A44", INK, lw=7)
    g.rc(400, 1230, 300, 90, "#FF6B5B", INK, lw=8, r=40)                       # pencil case
    for i, col in enumerate(("#FFC93C", "#5ED3B5", CAP)):
        pen(g, 560 + i * 20, 1180 - i * 60, 0.45, -0.08, True, glow_cap=0.6, t=c.gt)
    char2(g, "modern", 820, 2150, 1150, "curious", "down", "hold", t=c.gt, flip=True, prop=False)


def s_through(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    airway(g, 400, 1150, 0.95, True, ease_out(seg(c.t, 0.1, 0.4)), c.gt)
    g.text("AIRWAY", 400, 380, 70, "#FFFFFF", sw=12)
    char2(g, "doctor", 840, 2120, 1150, "deadpan", "down", "point", t=c.gt, flip=True, prop=False)


def s_gauge(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#FFE9C7", "#F6C98E", "#E39B5A"))
    v = 0.62 * ease_out(seg(c.t, c.w("eight") - 0.3, 0.8))
    gauge(g, 540, 1050, 1.15, v, "8 L / MIN")
    cap(g, 280, 1700, 1.7, 0.0, glow=0.6, t=c.gt)
    for i in range(3):
        u = (c.gt * 0.9 + i / 3) % 1.0
        arrow(g, 150 + 700 * u, 1650, 230 + 700 * u, 1650, "#5ED3B5", w=20, k=1.0, a=1 - u * 0.5)


def s_why(g, c):
    big_cap_scene_bg(g, c)
    cap(g, 170, 1250, 2.5, -0.35, glow=1.0, t=c.gt)
    sparkles(g, c.gt, [(200, 1100), (330, 1380), (120, 1300)], r=30)


def s_toobig(g, c):
    desk_room(g, c.gt)
    with g.at(380, 1200, -0.1, 2.0):                                           # chunky marker cap
        g.rc(0, 0, 160, 300, "#3E8E5E", INK, lw=8, r=50)
        g.rc(0, -110, 120, 40, "#2A6A44", INK, lw=6, r=10)
    with g.at(380, 1600, 0, 1.0):                                              # ruler
        g.rc(0, 0, 520, 90, "#FFC93C", INK, lw=8, r=8)
        for i in range(13):
            g.line([(-240 + i * 40, -45), (-240 + i * 40, -10 if i % 2 else 5)], INK, 5)
    char2(g, "doctor", 840, 2100, 1150, "smug", "down", "hold", t=c.gt, flip=True, prop=False)
    with g.screen():
        g.text("TOO BIG", 380, 760, 110, PAL["yellow"], sw=22, depth=8, sc=pop(c.t, c.w("big") - 0.1, 0.3), rot=-0.06)


def s_side(g, c):
    big_cap_scene_bg(g, c)
    pen(g, 190, 1760, 1.75, -0.98, capped=False, glow_side=ease_out(seg(c.t, c.w("side") - 0.2, 0.4)), t=c.gt)
    qmark(g, 780, 1300, 220, PAL["yellow"], 0.1, pop(c.t, c.w("pen") - 0.1, 0.3))


def s_xray(g, c):
    g.fill_all(g.rgrad(540, 1000, 1300, "#1E5A74", "#0E2A44", "#081826"))
    pen(g, 190, 1760, 1.75, -0.98, capped=False, glow_side=0.6, xray=1.0, t=c.gt)
    g.text("AIR IN", 400, 1020, 70, "#FFFFFF", sw=12)
    g.text("INK OUT", 330, 1880 - 120, 70, "#7FB8FF", sw=12)


def s_two(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE9C7", "#F6C98E"))
    g.rect(W / 2 - 6, 0, 12, H, INK, None)
    pen(g, 270, 1820, 1.5, -math.pi / 2, capped=False, glow_side=1.0, xray=1.0, t=c.gt)
    k = ease_out(seg(c.t, c.w("other") - 0.2, 0.4))
    char2(g, "modern", 800, 2100, 1200, "deadpan" if k < 0.5 else "smug", "down", "down", t=c.gt)
    for i in range(3):
        u = (c.gt * 0.7 + i / 3) % 1.0
        x0, y0 = 700 + 20 * i, 760 - 200 * u
        g.path(f"M{x0} {y0} Q{x0 + 30} {y0 - 30} {x0 + 60} {y0} Q{x0 + 90} {y0 + 30} {x0 + 120} {y0}", None, "#FFFFFF", lw=8, a=k * (1 - u))
    cap(g, 700, 600, 0.9, 0.0, glow=k, t=c.gt)


def s_loop(g, c):
    """Last shot = frame 1 (loop)."""
    big_cap_scene_bg(g, c)
    char2(g, "modern", 660, 2520, 1900, "smug" if c.t > c.w("chewing") else "suspicious", "down", "down", t=c.gt)
    cap(g, 250, 1520, 2.3, -0.62 + 0.04 * math.sin(c.gt * 1.6), glow=0.6, t=c.gt)


V.shot("H1", s_hook, part=(0, "And"), sfx=[(0.0, "shimmer", 0.35)])
V.shot("H1", s_notink, part=("And", 1), cam=push(1.0, 1.06, (540, 1200)), sfx=[("not", "click", 0.5)])
V.shot("L01", s_chew, part=(0, "And"), tr="flash", sfx=[(0.0, "chewing", 0.5)])
V.shot("L01", s_oops, part=("And", 1), cam=push(1.0, 1.06, (540, 1000)), sfx=[("breathes", "gulp", 0.5)])
V.shot("L02", s_cork, music="tension", sfx=[("plug", "thud", 0.45), ("cork", "pop", 0.4)])
V.shot("L03", s_standard, part=(0, "caps"), music="curious", sfx=[(0.0, "paper", 0.5)])
V.shot("L03", s_kids, part=("caps", "need"), cam=push(1.0, 1.05, (520, 1250)))
V.shot("L03", s_through, part=("need", 1), sfx=[("air", "rush", 0.35)])
V.shot("L04", s_gauge, cam=push(1.0, 1.05, (540, 1100)), sfx=[("eight", "tick", 0.4), ("minute", "ding", 0.4)])
V.shot("L05", s_why, part=(0, "Or"), sfx=[(0.0, "shimmer", 0.3)])
V.shot("L05", s_toobig, part=("Or", 1), sfx=[("big", "boing", 0.4)])
V.shot("L06", s_side, part=(0, "Different"), music="playful", sfx=[("side", "hmm", 0.4)])
V.shot("L06", s_xray, part=("Different", 1), tr="flash", sfx=[(0.0, "zap", 0.3)])
V.shot("L07", s_two, cam=push(1.0, 1.04, (540, 1100)), sfx=[("breathe", "shimmer", 0.4)])
V.shot("L08", s_loop, sfx=[(0.0, "chewing", 0.3)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=8, scale=0.16))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-012.mp4"))
