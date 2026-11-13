"""A-003 "Why a Plane Door Won't Open Mid-Flight" — standalone Short, Style F (flat 2D), 1080x1920.
python episodes/A-003-plane-door/make.py sheet|render|big <t,t,..>
Safety-positive: shows why it cannot happen; no instructions.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from flat_cast import Char, WY, amix
from flat_fx import *
from flat_sets import sky, plane, cabin, seat, tube_section, plug_diagram, elephant, air_dots, DOOR, HANDLE, TUBE, PLUG_Y

V = Video(EP, title=("WHY A PLANE DOOR", "WON'T OPEN MID-FLIGHT"),
          keys={"handle", "thirty-five", "thousand", "nothing", "air", "door", "plug", "bigger", "inward", "eight", "tonnes", "elephant", "relax", "shut"}, music="tension")
PAS = Char(skin="#C98F62", top="#3E8E5A", hair="spiky", hair_col="#2A1C1E", legs="#2B3A55", shoes="#FFF4E0", seed=5.1)
SX, SY = 150, 1640
GRIP = (194, -330)


def wy_seat(g, t, expr="worried", look=(0.7, -0.1), arms=("down", "down"), **kw):
    seat(g, SX, SY)
    WY.draw(g, t, SX + 100, SY - 112 + 58 * 1.12 + 4, sc=1.12, turn=kw.pop("turn", 0.4), expr=expr, look=look, arms=arms, shadow=False, **kw)
    seat(g, SX, SY, front=True)


def pas(g, t, x=905, expr="scared", arm=GRIP, lean=0.0, other="down", **kw):
    PAS.draw(g, t, x, 1660, sc=1.12, face=-1, turn=0.4, expr=expr, arms=(other, arm), lean=lean, look=(0.7, -0.4), **kw)


def s_hook(g, c):
    t = c.gt
    close = c.sh["name"] == "grip"
    k = ease_out(seg(t, 0.0, 1.3))
    cabin(g, t, pull=0.35 if close else 0.0, alarm=1.0 if close else 0.35 * k)
    wy_seat(g, t, "shock" if close else "surprised", arms=("down", "reach") if close else ("down", "down"))
    pas(g, t, x=lerp(1010, 905, k), arm=amix((120, -230), GRIP, k), expr="scared", sweat=1.0)
    if close:
        hx, hy = HANDLE
        pain_marks(g, hx + 30, hy - 10, 210, t, n=4, col=PAL["yellow"], a0=-2.6, a1=-0.6, sc=1.2)


def s_alt(g, c):
    t = c.t
    sky(g, c.gt, top="#061525", bot="#1D5873", speed=260)
    with g.layer(0.7):
        for i in range(5):
            x = (i * 300 - c.gt * 90) % 1500 - 200
            g.ellipse(x, 1760 + (i % 2) * 40, 190, 34, "#DDF0F3", None, a=0.45)
    for i in range(2):
        g.line([(540 - 420, 1206 + i * 14), (540 - 1500, 1206 + i * 14)], "#FFFFFF", 12, a=0.2)
    plane(g, c.gt, 540, 1150, 0.9, win="round", stripe="#1D9AA8", faces=True)
    k = ease_out(seg(t, c.w("thirty-five") - 0.25, c.w("feet?") - c.w("thirty-five") + 0.2))
    n = int(35000 * k / 500) * 500
    g.rect(190, 1480, 700, 150, INK, None, r=30, a=0.55)
    g.text(f"{n:,} FT", 540, 1556, 128, PAL["yellow"], sw=24, depth=9, sc=1 + 0.12 * pulse(t, c.w("feet?") - 0.05, 0.4))
    for i in range(3):
        kk = (c.gt * 0.9 + i / 3) % 1.0
        arrow(g, 130, 1640 - i * 4, 130, 1470, PAL["cream"], 16, 2.2, kk, a=1 - kk)


def s_nothing(g, c):
    t = c.t
    why = c.sh["name"] == "why"
    cabin(g, c.gt, pull=0.0 if why else 1.0)
    if why:
        wy_seat(g, c.gt, "happy", look=(0, 0), arms=("down", amix("hold", "point_up", back_out(seg(t, 0.0, 0.3)))), turn=0.1)
        pas(g, c.gt, expr="confused", arm=(120, -160), other="head2")
        sparkle(g, SX + 250, 1010, 60 * pop(t, 0.1, 0.3), PAL["yellow"], c.gt * 2, stroke=INK)
    else:
        st = 0.5 + 0.5 * math.sin(c.gt * 16)
        wy_seat(g, c.gt, "confused" if t < 0.9 else "smug", look=(0.7, 0))
        pas(g, c.gt, expr="pain", arm=GRIP, other=(170, -300), lean=0.10 + 0.03 * st, sweat=1.0, shiver=0.4)


def s_air(g, c):
    t = c.gt - V.voice0["L02"]
    w = {x["w"].strip(".,").lower(): x["s"] for x in V.T["L02"]["words"]}
    cx, cy, r = TUBE
    tube_section(g, c.gt)
    k = ease_io(seg(t, w["pumped"] - 0.2, 1.0))
    for i in range(3):                                           # air being pumped in from below
        kk = (c.gt * 1.4 + i / 3) % 1.0
        arrow(g, cx - 90 + i * 90, cy + r + 150, cx - 90 + i * 90, cy + r + 40, "#BFE6F2", 22, 2.1, kk * k, a=(1 - kk) * 0.9)
    if c.sh["name"] == "thin":
        k1, k2 = pop(c.t, c.w("thicker") - 0.1, 0.3), pop(c.t, c.w("thin") - 0.1, 0.3)
        g.text("THICK", cx - 40, cy - 150, 110, PAL["yellow"], sw=22, depth=8, sc=k1)
        g.text("THIN", cx + 330, cy - 430, 96, PAL["cream"], sw=20, depth=7, sc=k2)


def s_push(g, c):
    t = c.t
    door = c.sh["name"] == "door"
    tube_section(g, c.gt, arrows=1.0 if door else seg(t, c.w("pushes") - 0.2, 0.8), door=ease_out(seg(t, 0.0, 0.35)) if door else 0.0)


def s_plug(g, c):
    t = c.t
    name = c.sh["name"]
    y0, y1 = PLUG_Y
    if name == "plug":
        plug_diagram(g, c.gt)
        k = pop(t, c.w("plug:") - 0.15, 0.32)
        with g.at(540, (y0 + y1) / 2 + 2, 0, k):
            g.text("PLUG", 0, 0, 72, PAL["yellow"], sw=16, depth=5)
    elif name == "bigger":
        plug_diagram(g, c.gt, labels=0.5)
        k1 = ease_out(seg(t, 0.1, 0.4)); k2 = ease_out(seg(t, c.w("frame,") - c.w("it's") - 0.1, 0.4))
        for (ya, xa, xb, kk, col) in ((y1 + 46, 324, 756, k1, PAL["yellow"]), (y0 - 46, 360, 720, k2, "#FF8A7A")):
            mid = (xa + xb) / 2
            arrow(g, mid, ya, lerp(mid, xb, kk), ya, col, 18, 2.2, 1.0 if kk > 0.05 else 0, lw=5)
            arrow(g, mid, ya, lerp(mid, xa, kk), ya, col, 18, 2.2, 1.0 if kk > 0.05 else 0, lw=5)
        g.text("DOOR", 540, y1 + 112, 64, PAL["yellow"], sw=14, sc=k1)
        g.text("HOLE", 540, y0 - 112, 64, "#FF8A7A", sw=14, sc=k2)
    else:
        ti = c.w("inward")
        if t < ti - 0.1:
            bump = -13 * abs(math.sin(TAU * 1.6 * t)) * (1 if t > 0.12 else 0)
            plug_diagram(g, c.gt, shift=bump, blocked=seg(t, 0.2, 0.5), labels=0.5)
            for i in range(2):
                kk = (c.gt * 1.6 + i / 2) % 1.0
                arrow(g, 540, y1 - 20 - i * 3, 540, y0 - 110, "#FF8A7A", 26, 2.1, kk, a=1 - kk)
        else:
            k = ease_io(seg(t, ti - 0.1, 0.6))
            plug_diagram(g, c.gt, shift=150 * k, labels=0.5)
            check_badge(g, 820, y1 + 150, 70, pop(t, ti + 0.45, 0.3, 2.4))
            arrow(g, 540, y0 - 60, 540, y1 + 40 + 150 * k, "#5ED3B5", 26, 2.1, k)


def s_force(g, c):
    t = c.t
    y0, y1 = PLUG_Y
    if c.sh["name"] == "press":
        plug_diagram(g, c.gt, press=seg(t, c.w("pushes") - 0.25, 0.8), labels=0.5)
    else:
        plug_diagram(g, c.gt, press=1.0, labels=0.0)
        k = ease_out(seg(t, c.w("eight") - 0.2, 0.6))
        g.rect(150, 860, 780, 210, INK, None, r=40, a=0.6)
        g.text(f"{8 * k:.0f} TONNES", 540, 966, 150, PAL["yellow"], sw=28, depth=10, sc=1 + 0.14 * pulse(t, c.w("tonnes") - 0.05, 0.4))
        with g.screen():
            gauge(g, 205, 1500, 112, 0.1 + 0.9 * k + 0.02 * math.sin(c.gt * 30), pop(t, 0.05, 0.3))


def s_elephant(g, c):
    t = c.t
    cabin(g, c.gt, sign=False)
    dx, dy, dw, dh = DOOR
    k = back_out(seg(t, 0.0, 0.45), 1.5)
    elephant(g, dx + dw / 2 + 30, 1690 + (1 - k) * 900, 0.86, c.gt)
    wy_seat(g, c.gt, "surprised", look=(0.8, -0.3), arms=("down", "cheek"))
    burst(g, dx + dw / 2 + 30, 1300, 300, 520, 12, PAL["yellow"], 12, seg(t, 0.25, 0.5))


def s_arms(g, c):
    st = 0.5 + 0.5 * math.sin(c.gt * 18)
    cabin(g, c.gt, pull=1.0)
    wy_seat(g, c.gt, "smug", look=(0.7, 0), arms=("down", "chin"))
    pas(g, c.gt, expr="pain", arm=GRIP, other=(160, -310), lean=0.14 + 0.04 * st, sweat=1.0, shiver=0.6, tint=("#FF5B4B", 0.25 + 0.15 * st))
    hx, hy = HANDLE
    pain_marks(g, hx + 40, hy, 190, c.gt, n=3, col=PAL["yellow"], a0=-2.4, a1=-1.0, sc=1.1)


def s_relax(g, c):
    t = c.t
    name = c.sh["name"]
    cabin(g, c.gt)
    dx, dy, dw, dh = DOOR
    if name == "exit":
        wy_seat(g, c.gt, "worried", look=(0.8, -0.2), arms=("down", "chin"), sweat=1.0)
        qmark(g, SX + 300, 1040, 150, PAL["yellow"], 0.2, pop(t, c.w("exit...") - 0.1, 0.3))
    elif name == "relax":
        wy_seat(g, c.gt, "relief", look=(0, 0), arms=((-128, -372), (128, -372)), arm_under=(True, True), tilt=-0.12 * ease_out(seg(t, 0, 0.3)))
        sparkles(g, t, [(SX + 300, 1000), (SX - 40, 950)], r=40, period=0.7)
    else:
        wy_seat(g, c.gt, "sleepy", look=(0, 0.3), arms=((-128, -372), (128, -372)), arm_under=(True, True), tilt=-0.12)
        for i in range(3):
            g.text("Z", SX + 250 + i * 46, 1010 - i * 70 - 20 * ((c.gt * 0.8) % 1.0), 60 + i * 22, PAL["cream"], sw=12, a=0.9 - 0.25 * i)
        for i, (ax, ay) in enumerate(((dx - 150, dy + 160), (dx - 150, dy + 450), (dx + dw + 150, dy + 160), (dx + dw + 150, dy + 450))):
            kk = 0.75 + 0.25 * math.sin(c.gt * 5 + i)
            arrow(g, ax, ay, ax + (110 if ax < dx else -110) * kk, ay, PAL["yellow"], 26, 2.1, ease_out(seg(t, 0.1 + i * 0.06, 0.4)), lw=6)
        check_badge(g, dx + dw / 2, dy + 400, 84, pop(t, c.w("shut.") - 0.15, 0.32, 2.4))


CAB = lambda z0, z1, p=(560, 1280): roi(p, z0, z1, sy=1290)
V.shot("H1", s_hook, part=(0, "someone"), cam=CAB(1.0, 1.06), sfx=[(0.0, "ding", 0.3), (0.0, "room_tone", 0.5)], music="tension", tr="cut", name="walk")
V.shot("H1", s_hook, part=("someone", "at"), cam=roi((HANDLE[0] + 40, HANDLE[1] - 20), 1.45, 1.62, sy=1280), sfx=[("handle", "click", 0.45), (0.0, "heartbeat", 0.4)], name="grip")
V.shot("H1", s_alt, part=("at", 1), cam=roi((540, 1300), 1.18, 1.0, sy=1300), sfx=[(0.0, "whoosh", 0.4), (0.0, "wind", 0.45), ("thousand", "riser", 0.25)])
V.shot("L01", s_nothing, part=(0, "And"), cam=CAB(1.08, 1.14), sfx=[(0.0, "creak", 0.45), (("Nothing.", 0.45), "thud", 0.4)], music="playful", name="pull")
V.shot("L01", s_nothing, part=("And", 1), cam=CAB(1.14, 1.2, (420, 1250)), sfx=[(0.05, "pop", 0.35)], name="why")
V.shot("L02", s_air, part=(0, "much"), cam=roi((540, 1270), 1.0, 1.08, sy=1270), sfx=[(0.0, "whoosh_soft", 0.3), ("pumped", "bloop", 0.35), (("pumped", 0.3), "bloop", 0.3)], music="curious", name="pump")
V.shot("L02", s_air, part=("much", 1), cam=roi((700, 1100), 1.25, 1.35, sy=1230), sfx=[("thicker", "pop", 0.35), ("thin", "pop", 0.3)], name="thin")
V.shot("L03", s_push, part=(0, "including"), cam=roi((540, 1270), 1.06, 1.12, sy=1270), sfx=[("pushes", "swell", 0.35)], name="all")
V.shot("L03", s_push, part=("including", 1), cam=roi((860, 1270), 1.5, 1.66, sy=1270), sfx=[(0.0, "whoosh_soft", 0.3), ("door.", "ding", 0.4)], name="door")
V.shot("L04", s_plug, part=(0, "it's"), cam=roi((540, 1250), 1.0, 1.06, sy=1250), sfx=[(0.0, "whoosh_soft", 0.3), ("plug:", "pop", 0.4)], name="plug")
V.shot("L04", s_plug, part=("it's", "so"), cam=roi((540, 1200), 1.2, 1.28, sy=1240), sfx=[(0.12, "bloop", 0.3), (("frame,", -0.1), "bloop", 0.3)], name="bigger")
V.shot("L04", s_plug, part=("so", 1), cam=roi((540, 1240), 1.12, 1.2, sy=1240), sfx=[(0.2, "thud", 0.4), (0.52, "thud", 0.35), ("inward", "bloop", 0.35), (("inward", 0.5), "ding", 0.4)], name="move")
V.shot("L05", s_force, part=(0, "with"), cam=roi((540, 1330), 1.1, 1.18, sy=1280), sfx=[("pushes", "swell", 0.38)], music="tension", name="press")
V.shot("L05", s_force, part=("with", "More"), cam=roi((540, 1250), 1.0, 1.05, sy=1250), sfx=[("eight", "riser", 0.25), ("tonnes", "drum_hit", 0.5)], name="eight")
V.shot("L05", s_elephant, part=("More", 1), cam=CAB(1.0, 1.08, (560, 1250)), sfx=[(0.0, "boing", 0.4), (0.35, "thud", 0.5)], music="playful")
V.shot("L06", s_arms, cam=CAB(1.06, 1.16, (600, 1300)), sfx=[(0.0, "creak", 0.45), ("win", "creak", 0.35)])
V.shot("L07", s_relax, part=(0, "relax."), cam=CAB(1.08, 1.14, (420, 1270)), sfx=[("exit...", "hmm", 0.4)], music="warm", name="exit")
V.shot("L07", s_relax, part=("relax.", "The#1"), cam=CAB(1.2, 1.26, (330, 1230)), sfx=[(0.05, "melt", 0.4)], name="relax")
V.shot("L07", s_relax, part=("The#1", 1), cam=CAB(1.04, 1.0), sfx=[("holding", "swell", 0.25), ("shut.", "ding", 0.45)], name="shut")
V.build()
V.title_out = V.shots[2]["start"] - 0.2

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    out = EP / "final/A-003.mp4"
    if cmd == "sheet":
        print(V.sheet(EP / "animatic/sheet.jpg", per_shot=2, cols=8, scale=0.22))
    elif cmd == "big":
        print(V.sheet(EP / "animatic/big.jpg", times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.45))
    elif cmd == "render":
        V.render(out); measure(out)
    print(" ".join(f'{sh["id"][-2:]}:{sh["dur"]:.2f}' for sh in V.shots), "| total", V.duration)
