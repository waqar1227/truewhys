"""A-006 "The Castle Toilet That Let an Army In" — standalone Short, Style F (flat 2D), 1080x1920.
python episodes/A-006-castle-toilets/make.py sheet|render|big <t,t,..>
Clean: no filth shown. The 1204 story is told as "accounts say" (details vary between chroniclers).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from flat_cast import Char, WY, tunic, collar, belt, amix
from flat_fx import *
from flat_sets import (castle_wall, garderobe_room, chute_section, castle_hill, tent, crowd, torch, GBOX, CHUTE, OUTLET, SEAT_Y, HOLE, WALL_FOOT)

V = Video(EP, title=("THE CASTLE TOILET", "THAT LET AN ARMY IN"),
          keys={"toilet", "garderobes", "garderobes:", "seat", "chute", "moat", "strongest", "climbed", "army", "bars", "bends", "smell", "moths", "you"}, music="mystery")
SOL1 = Char(skin="#E3A679", top="#2F5FA8", hat="helmet", hat_col="#AEB8C2", outfit=[tunic("#2F5FA8", "#FFC93C")], legs="#4A3B33", shoes="#5A3A2C", stache="#3B2A20", seed=1.1)
SOL2 = Char(skin="#F1C9A5", top="#2F5FA8", hat="helmet", hat_col="#AEB8C2", outfit=[tunic("#2F5FA8", "#FFC93C")], legs="#4A3B33", shoes="#5A3A2C", beard="#8C5A3C", seed=2.2)
SOL3 = Char(skin="#8D5A3B", top="#2F5FA8", hat="helmet", hat_col="#AEB8C2", outfit=[tunic("#2F5FA8", "#FFC93C")], legs="#4A3B33", shoes="#5A3A2C", seed=3.1)
LADY = Char(skin="#F1C9A5", top="#7A4B8C", legs="#7A4B8C", shoes="#5A3A2C", hair="bun", hair_col="#6B4A2F", outfit=[collar("#FFF4E0"), belt("#FFC93C", "#FFF4E0")], lashes=True, seed=3.3)
HX = HOLE[0]


def emerge(g, t, rise, expr="neutral", arms=("down", "mouth"), look=(0.0, 0.0), sc=1.22, who=SOL1):
    """A soldier coming up through the seat (rise 0 = hidden, 1 = head and shoulders out)."""
    c = g.c
    c.save(); c.new_path(); c.rectangle(-2000, -2000, 5000, 2000 + SEAT_Y + 2); c.clip()
    who.draw(g, t, HX, SEAT_Y + lerp(470, 196, rise) * sc, sc=sc, turn=0.12, expr=expr, arms=arms, look=look, shadow=False)
    c.restore()
    hx, hy, rx, ry = HOLE
    g.line(f"M{hx - rx} {hy} Q{hx} {hy + ry * 2.1} {hx + rx} {hy}", "#9BA6B2", 16)
    g.line(f"M{hx - rx - 6} {hy + 2} Q{hx} {hy + ry * 2.1 + 12} {hx + rx + 6} {hy + 2}", INK, 6)


def s_hook(g, c):
    t = c.gt
    garderobe_room(g, t)
    rise = 0.78 + 0.22 * back_out(seg(t, V.word_t("H1", "into") - 0.1, 0.4), 1.6)
    grin = t > V.word_t("H1", "through") - 0.05
    lk = (0.8 * math.sin(t * 3.2), -0.1) if not grin else (0, 0)
    emerge(g, t, rise, "happy" if grin else "surprised", arms=("down", "mouth") if not grin else ("up", "up"), look=lk)
    if grin:
        k = seg(t, V.word_t("H1", "through"), 0.5)
        burst(g, HX, SEAT_Y - 330, 250, 430, 12, PAL["yellow"], 12, k)


def s_room(g, c):
    t = c.t
    garderobe_room(g, c.gt)
    LADY.draw(g, c.gt, 250, 1700, sc=1.2, turn=0.3, expr="happy", arms=("hip", amix("hold", "point", ease_out(seg(t, 0.2, 0.3)))), look=(0.5, 0))
    k = pop(t, c.w("garderobes:") - 0.15, 0.35)
    if k > 0:
        with g.at(660, 1010, -0.05, k):
            g.rect(-300, -62, 600, 124, "#7A4B2E", r=22)
            g.text("GARDEROBE", 0, 2, 88, PAL["cream"], stroke=None)
            for sx_ in (-270, 270):
                g.circle(sx_, 0, 9, "#3A3F4A", None)


def s_box(g, c):
    castle_wall(g, c.gt, hl=ease_out(seg(c.t, 0.25, 0.5)))


def s_chute(g, c):
    t = c.gt - V.voice0["L02"]
    w = {x["w"].strip(".,").lower(): x["s"] for x in V.T["L02"]["words"]}
    d = seg(t, w["chute"] - 0.1, w["moat"] - w["chute"] + 0.1)
    chute_section(g, c.gt, drop=ease_in(d) if d < 1 else None)
    hit = t - w["moat"]
    if hit > 0:
        for i in range(3):
            g.ellipse(850, 1604, 40 + 150 * ease_out(seg(hit, i * 0.16, 0.7)), 10 + 26 * ease_out(seg(hit, i * 0.16, 0.7)), None, "#BFF1FF", lw=8,
                      a=1 - seg(hit, i * 0.16, 0.7))
        for i in range(5):
            a0 = -2.4 + i * 0.42
            g.circle(850 + 150 * math.cos(a0) * hit, 1596 + 260 * math.sin(a0) * hit + 700 * hit * hit, 11, "#BFF1FF", INK, lw=4, a=clamp(1 - hit * 1.6))


def s_hill(g, c):
    t = c.t
    castle_hill(g, c.gt)
    name = c.sh["name"]
    if name == "date":
        k = pop(t, c.w("1204,") - 0.12, 0.35)
        g.text("1204", 300, 1420, 230, PAL["yellow"], sw=44, depth=16, sc=k, rot=-0.06)
    tent(g, 170, 1790, 1.0); tent(g, 940, 1800, 0.9)
    g.rings(540, 1760, 300, "#FFB060", a=0.08, n=3)
    for dx in (-44, 44):
        g.line([(540 + dx, 1800), (540 - dx * 0.6, 1756)], INK, 22); g.line([(540 + dx, 1800), (540 - dx * 0.6, 1756)], "#7A4B2E", 10)
    flame(g, 540, 1786, 96, 150, c.gt, seed=4)
    if name in ("date", "camp"):
        SOL1.draw(g, c.gt, 350, 1860, sc=0.92, turn=0.35, expr="angry", arms=("hip", "point_up"), look=(0.5, -0.8))
        SOL2.draw(g, c.gt, 740, 1860, sc=0.92, face=-1, turn=0.35, expr="think", arms=("hip", "chin"), look=(0.5, -0.8))
    if name == "strong":
        for i in range(7):                                # arrows bounce off the walls
            t0 = 0.1 + i * 0.22
            u = (t - t0) / 0.42
            hx, hy = 250 + i * 86, 990 - (i % 3) * 70
            if 0 < u < 1:
                x, y = lerp(-80, hx, u), lerp(1500, hy, u) - 150 * math.sin(u * math.pi)
                ang = math.atan2((hy - 1500) - 150 * math.pi * math.cos(u * math.pi), hx + 80)
            elif 1 <= u < 2.2:
                v = u - 1
                x, y = hx - 60 * v, hy + 30 * v + 330 * v * v
                ang = -0.6 + 5.5 * v
                burst(g, hx, hy, 12, 70, 6, PAL["yellow"], 7, min(0.99, v * 2.2))
            else:
                continue
            with g.at(x, y, ang):
                g.line([(-56, 0), (40, 0)], INK, 9); g.line([(-56, 0), (40, 0)], "#C9A26B", 4)
                g.poly([(40, -12), (66, 0), (40, 12)], "#DCE6EA", lw=4)


def s_climb(g, c):
    t = c.t
    castle_wall(g, c.gt)
    ox, oy = OUTLET
    up = ease_io(seg(t, 0.35, 1.3))
    cc = g.c
    cc.save(); cc.new_path(); cc.rectangle(-2000, oy - 66, 6000, 3000); cc.clip()
    SOL1.draw(g, c.gt, ox, lerp(oy + 132, oy - 240, up), sc=0.8, turn=0.0, expr="determined", arms=("up", "up"), shadow=False)
    cc.restore()
    SOL2.draw(g, c.gt, ox - 160, 1650, sc=0.82, turn=0.4, expr="worried" if up < 0.8 else "happy", arms=("down", amix("hold", "up", 0.5 + 0.5 * math.sin(c.gt * 6) * (1 - up))),
              look=(0.6, -0.8))
    x3 = lerp(-140, 330, ease_out(seg(t, 0.2, 1.6)))
    SOL3.draw(g, c.gt, x3, 1660 - 14 * abs(math.sin(c.gt * 7)), sc=0.82, turn=0.4, expr="scared", arms=("down", "mouth"), look=(0.6, -0.3))
    g.text("SHH!", x3 + 130, 1310, 76, PAL["cream"], sw=15, sc=pop(t, 0.9, 0.3), rot=0.1)


def s_inside(g, c):
    garderobe_room(g, c.gt)
    emerge(g, c.gt, back_out(seg(c.t, 0.05, 0.45), 1.8), "happy", arms=("up", "up"))
    burst(g, HX, SEAT_Y - 300, 240, 420, 12, PAL["yellow"], 12, seg(c.t, 0.1, 0.5))


def s_gate(g, c):
    t = c.t
    k = seg(t, 0.05, 0.9)
    castle_wall(g, c.gt, gate=k)
    if k > 0.6:
        SOL1.draw(g, c.gt, 565, 1556, sc=0.72, turn=0.0, expr="joy", arms=("wave", "wave"), lift=12 * abs(math.sin(c.gt * 7)))
    crowd(g, c.gt, 1870, cheer=ease_out(seg(t, 0.4, 0.5)))


def s_bars(g, c):
    t = c.t
    b = seg(t, c.w("bars") - 0.1, 0.5)
    chute_section(g, c.gt, bars=b, bend=ease_io(seg(t, c.w("bends") - 0.15, 0.5)))
    bonk = t - (c.w("bars") + 0.35)
    SOL2.draw(g, c.gt, 985, 1562, sc=0.72, face=-1, turn=0.3, expr="dizzy" if bonk > 0 else "determined", arms=("down", "reach") if bonk <= 0 else ("down", "head2"),
              lean=0.12 * pulse(t, c.w("bars") + 0.35, 0.5), look=(0.6, -0.6))
    if bonk > 0:
        for i in range(3):
            a0 = c.gt * 4 + i * TAU / 3
            sparkle(g, 985 + 96 * math.cos(a0), 1250 + 22 * math.sin(a0), 22, PAL["yellow"], a0, stroke=INK)
        burst(g, 880, 1470, 14, 90, 7, PAL["cream"], 8, min(0.99, bonk * 2.5))


def moth(g, x, y, t, s=1.0, a=1.0):
    fl = 0.35 + 0.65 * abs(math.sin(t * 22))
    with g.at(x, y, 0.3 * math.sin(t * 5), s):
        g.poly([(0, 0), (-34 * fl, -26), (-40 * fl, 16)], "#F1E6CC", lw=4, a=a, r=4); g.poly([(0, 0), (34 * fl, -26), (40 * fl, 16)], "#F1E6CC", lw=4, a=a, r=4)
        g.ellipse(0, 0, 6, 15, "#7A4B2E", INK, lw=3, a=a)


def s_clothes(g, c):
    t = c.t
    garderobe_room(g, c.gt, clothes=True)
    smell = c.sh["name"] == "smell"
    LADY.draw(g, c.gt, 250, 1700, sc=1.2, turn=0.3, expr="cold" if smell else "happy", arms=("hip", "reach") if not smell else ("down", (58, -322)), look=(0.5, -0.4))
    hx, hy = HOLE[0], HOLE[1]
    if smell:
        for i in range(4):
            k = (c.gt * 0.5 + i / 4) % 1.0
            x = hx - 150 + i * 100
            g.line(f"M{x} {hy - 20 - 380 * k} q26 -34 0 -68 q-26 -34 0 -68", "#B7D96A", 13, a=0.85 * math.sin(k * math.pi))
        for i, (mx, my) in enumerate(((560, 1080), (700, 1130), (840, 1070))):
            fk = ease_in(seg(t, c.w("moths") - 0.2 + i * 0.1, 0.9))
            moth(g, mx + (500 + i * 80) * fk * (1 if i != 0 else -1), my - 420 * fk + 16 * math.sin(c.gt * 6 + i), c.gt + i, 1.2, a=1 - fk * 0.3)
    else:
        for i, (mx, my) in enumerate(((560, 1080), (700, 1130), (840, 1070))):
            moth(g, mx + 30 * math.sin(c.gt * 2 + i * 2), my + 16 * math.sin(c.gt * 3.1 + i), c.gt + i, 1.2)


def s_you(g, c):
    t = c.t
    castle_wall(g, c.gt)
    WY.draw(g, c.gt, 330, 1660, sc=1.1, turn=0.4, expr="scared", arms=("down", "chin"), look=(0.7, -0.9), sweat=1.0)
    qmark(g, 520, 1250, 210, PAL["yellow"], 0.15, pop(t, c.w("you") - 0.1, 0.3))
    ox, oy = OUTLET
    for i in range(3):
        k = (c.gt * 0.8 + i / 3) % 1.0
        arrow(g, ox, oy - 90 - i * 2, ox, oy - 210, PAL["yellow"], 18, 2.2, k, a=1 - k)


SEATCAM = lambda z0, z1: roi((HX, SEAT_Y - 180), z0, z1, sy=1230)
V.shot("H1", s_hook, part=(0, "into"), cam=SEATCAM(1.22, 1.3), sfx=[(0.0, "creak", 0.3), (0.35, "pop", 0.25)], music="mystery", tr="cut")
V.shot("H1", s_hook, part=("into", "through"), cam=SEATCAM(1.3, 1.38), sfx=[(0.05, "boing", 0.3)])
V.shot("H1", s_hook, part=("through", 1), cam=SEATCAM(1.5, 1.62), sfx=[(0.0, "drum_hit", 0.45), (0.1, "crowd_cheer", 0.12)], tr="flash")
V.shot("L01", s_room, part=(0, "tiny"), cam=roi((560, 1300), 1.0, 1.06, sy=1300), sfx=[("garderobes:", "pop", 0.4), (0.1, "door", 0.4)], music="curious")
V.shot("L01", s_box, part=("tiny", 1), cam=roi((720, 1150), 1.0, 1.22, sy=1200), sfx=[(0.0, "whoosh_soft", 0.35), (0.3, "ding", 0.35), (0.0, "insects", 0.3)])
V.shot("L02", s_chute, part=(0, "straight"), cam=roi((820, 1050), 1.3, 1.36, sy=1200), sfx=[("chute", "whoosh_soft", 0.3)])
V.shot("L02", s_chute, part=("straight", "often"), cam=roi((840, 1150), 1.36, 1.3, sy=1150, p1=(840, 1400)), sfx=[(0.0, "riser", 0.25)])
V.shot("L02", s_chute, part=("often", 1), cam=roi((850, 1560), 1.3, 1.42, sy=1300), sfx=[("moat", "splash", 0.5)])
V.shot("L03", s_hill, part=(0, "French"), cam=roi((520, 1150), 1.0, 1.06, sy=1250), sfx=[(0.0, "drum_hit", 0.5), ("1204,", "thud", 0.4), (0.0, "wind", 0.4)], music="tension", name="date")
V.shot("L03", s_hill, part=("French", "one"), cam=roi((540, 1640), 1.2, 1.28, sy=1420), sfx=[(0.0, "fire", 0.5), (0.4, "hmm", 0.35)], name="camp")
V.shot("L03", s_hill, part=("one", 1), cam=roi((520, 960), 1.5, 1.7, sy=1250), sfx=[(0.1, "whoosh_soft", 0.3), (0.5, "tick", 0.4), (0.75, "tick", 0.4), (1.0, "tick", 0.4), (1.25, "tick", 0.4)], name="strong")
V.shot("L04", s_climb, part=(0, "got"), cam=roi((640, 1480), 1.25, 1.35, sy=1330), sfx=[(0.0, "insects", 0.35), (0.4, "creak", 0.35), (0.9, "pop", 0.3)], music="mystery")
V.shot("L04", s_inside, part=("got", "and"), cam=SEATCAM(1.25, 1.36), sfx=[(0.05, "boing", 0.4), (0.15, "sparkle", 0.35)])
V.shot("L04", s_gate, part=("and", 1), cam=roi((565, 1500), 1.0, 1.1, sy=1380), sfx=[(0.0, "creak", 0.55), (0.5, "thud", 0.5), (0.6, "crowd_cheer", 0.3)], music="adventure")
V.shot("L05", s_bars, cam=roi((860, 1380), 1.25, 1.36, sy=1300), sfx=[("bars", "click", 0.6), (("bars", 0.35), "thud", 0.5), ("bends", "boing", 0.3)], music="curious")
V.shot("L06", s_clothes, part=(0, "because"), cam=roi((600, 1250), 1.0, 1.08, sy=1280), sfx=[(0.1, "flag_flap", 0.4), ("clothes", "pop", 0.3)], name="clothes")
V.shot("L06", s_clothes, part=("because", 1), cam=roi((520, 1210), 1.06, 1.14, sy=1260), sfx=[("smell", "confuse", 0.26), ("moths", "whoosh_soft", 0.35)], name="smell")
V.shot("L07", s_you, cam=roi((560, 1420), 1.05, 1.16, sy=1330), sfx=[(0.0, "insects", 0.3), ("you", "hmm", 0.45)], music="playful")
V.build()
V.title_out = V.shots[3]["start"] - 0.2

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    out = EP / "final/A-006.mp4"
    if cmd == "sheet":
        print(V.sheet(EP / "animatic/sheet.jpg", per_shot=2, cols=8, scale=0.22))
    elif cmd == "big":
        print(V.sheet(EP / "animatic/big.jpg", times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.45))
    elif cmd == "render":
        V.render(out); measure(out)
    print(" ".join(f'{sh["id"][-2:]}:{sh["dur"]:.2f}' for sh in V.shots), "| total", V.duration)
