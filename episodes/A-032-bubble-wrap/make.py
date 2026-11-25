"""A-032 "How a Failed 1957 Wallpaper Became Bubble Wrap" — standalone Short, Style F + cast v2.2 (Engineer, Painter, Margaret, Salesman,
Everyman). Studio pattern 1 ("How [X] Happened": accidental origin of an everyday thing). Slot Thu 31 Dec 2026 18:00 UTC.
python episodes/A-032-bubble-wrap/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: a 1950s living room with bubble "wallpaper", a garage workshop with a homemade heat sealer and two
shower curtains, a decorating shop, a greenhouse, a generic 1960 computer (no logo) in a crate on a bumpy road, parcels. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_split import split_long
from flat_fx import burst, sparkles, arrow, ring_wave
from flat_bubble import (bubble_sheet, room_1957, lamp_1957, trash_can, workshop_1957, curtain, sealer, shop_1957, wall_roll, greenhouse,
                         mainframe, crate, road, truck, computer_room, parcel, BUB)

V = Video(EP, title=("WALLPAPER", "OR WRAP?"), music="playful")
V.title_y = 0.075
EX, EY, EH = 700, 2010, 1180                 # engineer in the hook/loop framing (big, 3/4 view, facing the wall on the left)


def wall_pop(t0):
    """Bubbles under the brush pop one after another along the brush path (row 3-5, from the right)."""
    def f(i, j):
        if not 11 <= i <= 13:
            return 0.0
        return clamp((V_t[0] - t0 - (5 - j) * 0.22 - (i - 11) * 0.06) / 0.16)
    return f


V_t = [0.0]


def hook_room(g, c, t0, k_brush, expr, pose_r):
    """1957 room, the left 70 % of the wall already covered in bubble film; the engineer smooths it with a paste brush; bubbles pop."""
    V_t[0] = c.t
    room_1957(g, c.gt, paper=0.0)
    lamp_1957(g, 980, 1560, 1.0)
    bubble_sheet(g, -40, 280, 760, 1220, c.gt, r=34, a=0.82, pop=wall_pop(t0))
    bx = lerp(370, 330, k_brush) + 10 * math.sin(c.t * 7); by = 1290 + 8 * math.sin(c.t * 9)
    with g.at(bx - 60, by, -1.2):                                           # paste brush in his hand, bristles on the film
        g.rc(0, 0, 150, 60, "#C98A5A", INK, lw=7, r=12)
        g.rect(-70, 26, 140, 60, "#F4E7C8", INK, lw=6)
        g.rc(140, -10, 170, 26, "#8A5A3A", INK, lw=6, r=12)
    char2(g, "engineer", EX, EY, EH, expr, pose_r, "down", t=c.gt, flip=True, view="3q", prop=False)


# ------------------------------------------------------------------ hook / loop
def s_hook(g, c):
    """Frame 1: mid-stroke, the brush pops a row of bubbles on the 'wallpaper'; the engineer startled, arm still on the brush."""
    hook_room(g, c, -0.05, ease_io(clamp(c.t / 2.4)), "shocked", "reach_r")


def s_loop(g, c):
    """Last shot: same framing; he gives the wall a satisfied look and starts the brush stroke again (ends on frame 1)."""
    k = 1.0 - ease_io(clamp(c.u * 1.1))
    hook_room(g, c, 99, 0.0, "smile" if c.u < 0.7 else "shocked", "reach_r")


# ------------------------------------------------------------------ L01 nobody wanted it
def s_nobody(g, c):
    """'Nobody wanted it on their walls...': Margaret in a bubbly 1950s room, arms crossed, unimpressed; she pokes a bubble."""
    room_1957(g, c.gt, paper=1.0)
    char2(g, "knight", 560, 1960, 1080, "bored" if c.t < c.w("walls") else "suspicious", "hip", pose_at(c.t, [(0, "hip"), (c.w("walls"), "point")]),
          t=c.gt, view="front", prop=False)


def s_trash(g, c):
    """'...and it almost ended up in the trash': a rolled sheet arcs through the air into a metal bin; the lid rattles."""
    room_1957(g, c.gt)
    lid = 0.6 * (1 - ease_out(clamp(c.since("trash") / 0.4))) if c.t > c.w("trash") else 0.6
    trash_can(g, 560, 1700, 1.6, lid=lid)
    k = ease_io(clamp(c.u * 1.4))
    x, y = lerp(-120, 560, k), lerp(900, 1240, k) - 520 * math.sin(math.pi * k)
    if k < 1:
        with g.at(x, y, k * 6):
            g.rc(0, 0, 240, 90, "#E9F7FF", INK, lw=7, r=45)
            g.ellipse(-120, 0, 20, 45, "#CFEFFF", INK, lw=5)
    with g.screen():
        g.text("TRASH?", W / 2, 470, 130, "#FF6B5B", sw=18, depth=9, sc=pop(c.t, c.w("trash") - 0.08, 0.3), a=c.on("trash", 0.2))


# ------------------------------------------------------------------ L02 1957: two engineers, two shower curtains
def s_workshop(g, c):
    """'In 1957, two engineers': a garage workshop, the Engineer and the Painter look at two shower curtains on the bench."""
    workshop_1957(g, c.gt)
    curtain(g, 300, 980, 240, 380, "#BFE6F2", stripe="#FF8AA8", t=c.gt)
    curtain(g, 560, 980, 240, 380, "#F4E7C8", t=c.gt + 1)
    char2(g, "engineer", 220, 1960, 960, "curious", "down", pose_at(c.t, [(0, "down"), (c.w("engineers"), "point")]), t=c.gt, view="3q", prop=False)
    char2(g, "painter", 880, 1960, 940, "suspicious", "hip", "think", t=c.gt, flip=True, view="3q", prop=False)
    with g.screen():
        g.text("1957", W / 2, 420, 170, "#FFFFFF", sw=22, depth=11, sc=pop(c.t, c.w("1957") - 0.08, 0.3), a=c.on("1957", 0.2))


def s_seal(g, c):
    """'sealed two shower curtains together': both curtains feed into the roller sealer, one sheet comes out."""
    workshop_1957(g, c.gt)
    run = 1.0
    off = (c.t * 140) % 70
    for (y0, col, st) in ((700, "#BFE6F2", "#FF8AA8"), (1180, "#F4E7C8", None)):        # two curtains fed in from a rail on the left
        g.poly([(-100, y0), (430, 935 if y0 < 900 else 985), (430, 955 if y0 < 900 else 1005), (-100, y0 + 110)], col, INK, lw=6)
        if st:
            for k in range(-1, 9):
                x = k * 70 + off
                if x < 430:
                    yy = lerp(y0 + 55, 945, x / 530)
                    g.line([(x - 10, yy - 40 * (1 - x / 530)), (x + 10, yy + 40 * (1 - x / 530))], st, 18, a=0.85)
    sealer(g, 470, 960, 1.0, c.gt, heat=0.7 + 0.3 * math.sin(c.t * 8), run=run)
    bubble_sheet(g, 520, 930, 700, 70, c.gt, r=14, inflate=0.0, a=0.95)
    char2(g, "painter", 830, 1980, 820, "deadpan", "hold", "explain", t=c.gt, flip=True, view="3q", prop=False)


def s_bubbles(g, c):
    """'trapping rows of air bubbles inside': close on the film coming out; row after row of bubbles puffs up."""
    g.fill_all(g.rgrad(540, 960, 1100, "#3E5A6E", "#22323E"))
    rows = (c.t - 0.1) * 3.2
    bubble_sheet(g, 60, 420, 960, 1120, c.gt, r=52, rows=rows, a=0.95)
    sealer(g, 540, 330, 0.9, c.gt, heat=0.8)


def s_sell(g, c):
    """'and sold it as fancy textured wallpaper': a 1950s decorating shop, the Salesman proudly shows a bubbly roll."""
    shop_1957(g, c.gt)
    wall_roll(g, 330, 1080, 1.1, c.gt, unroll=0.3 + 0.7 * ease_out(clamp(c.u * 1.5)))
    char2(g, "gillette", 780, 1960, 1000, "smug", "hip", pose_at(c.t, [(0, "down"), (0.25, "explain")]), t=c.gt, flip=True, view="3q", prop=False)
    if c.t > c.w("fancy"):
        sparkles(g, c.t, [(250, 1150), (420, 1300), (330, 1450)], seed=4, col="#FFF4A8", r=34, t0=c.w("fancy"))


# ------------------------------------------------------------------ L03 greenhouse flop
def s_green(g, c):
    """'So they tried it as greenhouse insulation': sunny greenhouse, bubble panels pressed onto the glass; the Engineer hopeful."""
    greenhouse(g, c.gt, cover=ease_out(clamp(c.u * 1.6)))
    char2(g, "engineer", 820, 1980, 820, "smile", "down", "point", t=c.gt, flip=True, view="3q", prop=False)


def s_flop(g, c):
    """'That flopped too.': the panels peel and slide down, the plants wilt; the Engineer shrugs."""
    k = ease_io(clamp(c.u * 1.3))
    greenhouse(g, c.gt, cover=1.0, slide=k, droop=k)
    char2(g, "engineer", 820, 1980, 820, "bored", "shrug", "shrug", t=c.gt, flip=True, view="3q", prop=False)


# ------------------------------------------------------------------ L04 computer maker
def s_computer(g, c):
    """'Then a computer maker needed to ship its delicate new machine': a 1960 computer room, a tall cabinet lowered into a crate."""
    computer_room(g, c.gt)
    k = ease_io(clamp(c.u * 1.2))
    mainframe(g, 540, lerp(1400, 1700, k), 0.95, c.gt)
    crate(g, 540, 1760, 600, 560, xray=0.0)
    char2(g, "student", 160, 1990, 760, "worried", "down", "hold", t=c.gt, view="3q", prop=False)


def s_road(g, c):
    """'without a single crack': the crate on a 1960 truck bouncing over a cobbled road; a red crack threatens on the crate."""
    road(g, c.gt, bump=1.0)
    jig = 14 * math.sin(c.t * 25)
    def cargo(gg):
        crate(gg, 0, 0, 420, 520, crack=c.on("crack", 0.5) * 0.9)
    truck(g, 600, 1620, 1.05, c.gt, bump=1.0, cargo=cargo)
    with g.screen():
        g.text("CRACK?", W / 2, 470, 130, "#FF6B5B", sw=18, depth=9, sc=pop(c.t, c.w("crack") - 0.08, 0.3), a=c.on("crack", 0.2))


# ------------------------------------------------------------------ L05 the bubbles took the bumps
def s_xray(g, c):
    """'The bubbles took the bumps': X-ray view of the crate: the computer wrapped in bubble film; each bump squashes the bubbles, not the machine."""
    g.fill_all(g.rgrad(540, 1000, 1200, "#1B6E86", "#0B3F4C"))
    hit = (c.t * 2.2) % 1.0
    bump = max(0.0, 1 - hit * 4)
    with g.at(0, -40 * bump):
        crate(g, 540, 1700, 720, 1180, xray=1.0)
        bubble_sheet(g, 200, 560, 680, 1120, c.gt, r=40, a=0.95, squash=lambda i, j: bump * (1.0 if i > 9 else 0.3))
        mainframe(g, 540, 1610, 0.82, c.gt, lights=0.4)
    for k in range(3):
        arrow(g, 220 + k * 320, 1900, 220 + k * 320, 1780 - 80 * bump, "#FFC93C", w=20, k=1.0)


def s_safe(g, c):
    """'The computers arrived safe': the crate lid lifts off, the computer shines, the Engineer cheers."""
    computer_room(g, c.gt)
    k = ease_out(clamp(c.u * 1.5))
    mainframe(g, 430, 1690, 0.95, c.gt, shine=k)
    bubble_sheet(g, 160, 1440, 540, 260, c.gt, r=26, a=0.9)
    crate(g, 430, 1760, 620, 300, open_=k)
    char2(g, "engineer", 860, 1990, 900, "smile", "up", "up", t=c.gt, flip=True, view="3q", prop=False)
    if k > 0.3:
        sparkles(g, c.t, [(300, 900), (560, 820), (430, 1100)], seed=7, col="#FFF4A8", r=34, t0=0.2)


def s_parcels(g, c):
    """'and packing was never the same': a stack of parcels bursting with bubble film slides in, more and more."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE3B8", "#F6B98A"))
    for k, (x, y, w, h, col) in enumerate(((260, 1700, 380, 300, "#C98A4A"), (760, 1700, 420, 360, "#D99A55"), (480, 1400, 340, 280, "#B97A3A"),
                                         (820, 1340, 300, 240, "#C98A4A"), (220, 1400, 280, 220, "#D99A55"), (540, 1120, 300, 240, "#C98A4A"))):
        kk = ease_out(clamp((c.t - k * 0.22) / 0.35))
        if kk > 0:
            parcel(g, x, y - (1 - kk) * 700, w, h, col, c.gt, wrap=kk)


# ------------------------------------------------------------------ L06 every pop
def s_pop(g, c):
    """'So every pop you hear...': today, the Everyman twists a sheet of bubble film, popping it with a grin."""
    g.fill_all(g.rgrad(540, 900, 1300, "#5ED3B5", "#0F6B78"))
    t0 = 0.15
    char2(g, "modern", 540, 2010, 1150, "smile", "hold", "hold", t=c.gt, view="front", prop=False)
    bubble_sheet(g, 250, 1340, 580, 300, c.gt, r=34, a=0.95, rot=0.04 * math.sin(c.t * 5),
                 pop=lambda i, j: clamp((c.t - t0 - (i * 6 + j) * 0.07) / 0.12))


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, 1), cam=ZOOM(1.0, 1.04, (520, 1000)), sfx=[(0.0, "pop", 0.6), (0.05, "pop", 0.5), (0.0, "sting", 0.3), (0.2, "pop", 0.45)], tr="cut")
V.shot("L01", s_nobody, (0, "and"), cam=ZOOM(1.0, 1.05, (540, 1000)), sfx=[(0.05, "whoosh", 0.3), ("walls", "boing", 0.3)])
V.shot("L01", s_trash, ("and", 1), cam=ZOOM(1.0, 1.04, (540, 1100)), tr="cut", sfx=[(0.1, "whoosh", 0.35), ("trash", "clunk", 0.55)])
V.shot("L02", s_workshop, (0, "sealed"), cam=ZOOM(1.0, 1.05, (540, 1100)), music="story", sfx=[("1957", "pop", 0.35)])
V.shot("L02", s_seal, ("sealed", "trapping"), cam=ZOOM(1.0, 1.06, (520, 1000)), tr="cut", sfx=[(0.05, "whir", 0.35), ("curtains", "hiss", 0.25)])
V.shot("L02", s_bubbles, ("trapping", "and"), cam=ZOOM(1.0, 1.05, (540, 1000)), tr="cut", sfx=[(0.1, "bloop", 0.35), (0.5, "bloop", 0.3), (0.9, "bloop", 0.3)])
V.shot("L02", s_sell, ("and", 1), cam=ZOOM(1.0, 1.05, (540, 1100)), tr="cut", sfx=[("fancy", "sparkle", 0.4), ("wallpaper", "ding", 0.3)])
V.shot("L03", s_green, (0, "That"), cam=ZOOM(1.0, 1.05, (540, 1100)), sfx=[(0.05, "whoosh", 0.3)])
V.shot("L03", s_flop, ("That", 1), cam=ZOOM(1.05, 1.0, (540, 1100)), tr="cut", sfx=[("flopped", "confuse", 0.4), ("too", "thud", 0.3)])
V.shot("L04", s_computer, (0, "without"), cam=ZOOM(1.0, 1.05, (540, 1200)), music="adventure", sfx=[(0.1, "beep3", 0.25), ("machine", "creak", 0.3)])
V.shot("L04", s_road, ("without", 1), cam=ZOOM(1.0, 1.04, (560, 1300)), tr="cut", sfx=[(0.0, "rumble", 0.4), ("crack", "glass_crack", 0.4)])
V.shot("L05", s_xray, (0, "computers"), cam=ZOOM(1.0, 1.05, (540, 1100)), sfx=[(0.1, "thud", 0.4), (0.55, "thud", 0.35), ("bumps", "boing", 0.3)])
V.shot("L05", s_safe, ("computers", "and"), cam=ZOOM(1.0, 1.05, (560, 1200)), tr="cut", sfx=[(0.05, "creak", 0.3), ("safe", "sparkle", 0.45)])
V.shot("L05", s_parcels, ("and", 1), cam=ZOOM(1.0, 1.05, (540, 1300)), tr="cut", sfx=[(0.1, "thud", 0.3), (0.35, "thud", 0.3), (0.6, "thud", 0.3)])
V.shot("L06", s_pop, (0, "is"), cam=ZOOM(1.0, 1.05, (540, 1200)), music="playful", sfx=[(0.15, "pop", 0.45), (0.3, "pop", 0.4), (0.45, "pop", 0.45), (0.6, "pop", 0.4)])
V.shot("L06", s_loop, ("is", 1), cam=ZOOM(1.04, 1.0, (520, 1000)), tr="cut", sfx=[("nobody", "hmm", 0.2)])
V.build()
split_long(V, maxd=2.6, keep_cam=True)
V.title_out = V.voice0["H1"] + V.T["H1"]["dur"]

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=6, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.load_env(); V.mix()
        V.render(str(EP / "final/A-032.mp4"))
