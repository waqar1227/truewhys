"""A-026 "Why Your Tongue Sticks to a Frozen Pole" — standalone Short, Style F + cast v2.2 (Everyman + Friend). Slot Tue 15 Dec 2026 18:00 UTC.
python episodes/A-026-tongue-pole/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: snowy school yard, steel pole, metal/wood/plastic heat race, tongue-on-metal macro, microscope view of
spit freezing into tongue bumps and metal pits, warm-water rescue. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import burst, no_sign, arrow, steam, sparkles, sparkle, pain_marks, flake
from flat_winter import winter_yard, metal_pole, tongue, mouth_pt, hand_pt, beanie, scarf

V = Video(EP, title=("WHY IS IT", "STUCK?"), music="playful")
V.title_y = 0.075
TONGUE, ICE, HEAT, STEEL = "#E8677A", "#CFF1FF", "#FF7A3D", "#B9C6D2"
WHO, PAL2 = "modern", "friend"
PX, PTOP, PBOT = 720, 360, 1700            # the pole
CX, CY, CH = 560, 1790, 1080               # Everyman feet + height


# ------------------------------------------------------------------ the stuck kid (hook / pull / rescue)
def stuck_scene(g, c, expr="shocked", pl="up", pr="shrug", lean=0.0, stretch=0.0, frozen=1.0, wobble=1.0, free=0.0):
    winter_yard(g, c.gt)
    metal_pole(g, PX, PTOP, PBOT, frost=0.7)
    x = CX - lean * 70 + wobble * 10 * math.sin(c.gt * 8)
    rot = -0.05 * lean + wobble * 0.03 * math.sin(c.gt * 6)
    char2(g, WHO, x, CY, CH, expr, pl, pr, t=c.gt, rot=rot, view="3q")
    beanie(g, x, CY, CH, view="3q"); scarf(g, x, CY, CH, t=c.gt)
    mx, my = mouth_pt(x, CY, CH, "3q")
    if free < 1:
        tip = (PX - 38, my + 8)
        if free > 0:                                                               # tongue slides back into the mouth
            tip = (lerp(tip[0], mx + 8, ease_out(free)), lerp(tip[1], my, ease_out(free)))
        tongue(g, mx, my, tip[0], tip[1], w=34, stretch=stretch, frozen=frozen * (1 - free))
    return mx, my


def s_hook(g, c):
    """Frame 1: tongue already frozen to the steel pole, arms flailing, frost burst at the contact point."""
    mx, my = stuck_scene(g, c, "shocked", pose_at(c.t, [(0, "up"), (0.9, "wave"), (1.6, "up")]), "shrug")
    burst(g, PX - 30, my + 8, 50, 150, 10, ICE, 9, k=seg(c.t, 0.0, 0.45))
    pain_marks(g, mx - 120, my - 210, 110, c.gt, n=4, col="#FF5B4B", a0=-2.6, a1=-1.0, sc=0.9)
    g.path(f"M{mx-170} {my-120} Q{mx-150} {my-80} {mx-170} {my-60} Q{mx-190} {my-80} {mx-170} {my-120} Z", "#BFE8FF", INK, lw=5)
    for i in range(3):
        flake(g, PX + 40 + 30 * i, my - 80 - 40 * i + 20 * math.sin(c.gt * 3 + i), 14 + 5 * i, "#FFFFFF", c.gt + i, lw=4)


def macro_bg(g):
    g.fill_all(g.lgrad(0, 0, 0, H, "#1B3550", "#0F2236"))
    with g.layer(0.4):
        for i in range(10):
            r = rnd(i + 40).random
            g.circle(r() * W, r() * H, 60 + r() * 120, "#2E5578", None, a=0.25)


def big_tongue(g, x1, y=960, h=420, col=TONGUE):
    """Huge tongue entering from the left, its wet tip pressed on the metal at x1."""
    g.path(f"M-200 {y-h/2} L{x1-140} {y-h/2} Q{x1} {y-h/2} {x1} {y} Q{x1} {y+h/2} {x1-140} {y+h/2} L-200 {y+h/2} Z", col, INK, lw=10)
    g.line([(-200, y + 10), (x1 - 160, y + 10)], shade(col, -0.18), 10)
    R = rnd(3).random
    for i in range(26):                                                            # tongue bumps (papillae)
        g.circle(R() * (x1 - 120), y - h / 2 + 30 + R() * (h - 60), 10 + R() * 8, shade(col, 0.12), None, a=0.8)


def metal_wall(g, x0):
    g.rect(x0, -100, W + 200 - x0, H + 200, g.lgrad(x0, 0, W, 0, "#6E7B88", "#E3ECF3", "#9AA8B6", "#6E7B88"), INK, lw=10)
    for i in range(8):
        g.line([(x0 + 60 + i * 40, -100), (x0 + 60 + i * 40, H + 100)], "#FFFFFF", 4, a=0.12)


def s_glue(g, c):
    """'your own spit just turned into glue': macro of the tongue tip on the steel, spit drops frosting over."""
    macro_bg(g)
    metal_wall(g, 700)
    big_tongue(g, 700)
    k = c.on("glue", 0.45)
    R = rnd(8).random
    for i in range(9):
        y = 820 + i * 34 + R() * 10; x = 690 + R() * 20
        col = mix("#7FD3FF", "#FFFFFF", k)
        g.ellipse(x, y, 22 + 8 * k, 14, col, INK, lw=5, a=0.95)
        if k > 0.3:
            flake(g, x + 20, y, 12 * k, "#FFFFFF", i, lw=3)
    g.glow(700, 960, 260, ICE, 0.35 * k)
    with g.screen():
        g.text("SPIT", 360, 640, 104, "#7FD3FF", sw=16, depth=8, sc=pop(c.t, c.w("spit") - 0.12, 0.3), a=1 - k)
        g.text("ICE GLUE", 380, 640, 116, "#FFFFFF", sw=18, depth=9, sc=pop(c.t, c.w("glue") - 0.1, 0.32), a=k)


def post(g, x, kind, k, flow, t):
    """One post in the heat race: steel / wood / plastic, with a heat meter that drains at `flow` speed."""
    top, bot = 760, 1640
    with g.at(x, 0, 0, 1.0, 1.0):
        if kind == "metal":
            metal_pole(g, 0, top, bot, w=110, frost=0.5)
        elif kind == "wood":
            g.rect(-60, top, 120, bot - top, g.lgrad(-60, 0, 60, 0, "#8A5A34", "#C8955E", "#8A5A34"), INK, lw=8, r=10)
            for j in range(6):
                g.path(f"M-30 {top+80+j*140} Q0 {top+40+j*140} 30 {top+90+j*140}", None, "#7A4A28", lw=5)
        else:
            g.rect(-60, top, 120, bot - top, g.lgrad(-60, 0, 60, 0, "#C83E50", "#FF7A88", "#C83E50"), INK, lw=8, r=30)
            g.line([(-24, top + 40), (-24, bot - 40)], "#FFFFFF", 12, a=0.4)
        # meter: how much warmth the tongue has left after touching
        level = clamp(1 - flow * seg(t, 0, 2.2))
        g.rc(0, top - 230, 100, 300, "#22344A", INK, lw=8, r=46)
        g.rc(0, top - 230 + 140 * (1 - level), 64, 270 * level, mix("#5FB8FF", HEAT, level), None, r=30)
        n = int(3 + 6 * flow)
        for i in range(n):                                                         # heat dots flowing down into the post
            u = (t * (0.4 + 2.2 * flow) + i / n) % 1.0
            g.circle(0 + 18 * math.sin(i * 2.3), top - 60 + u * (bot - top) * (0.3 + 0.7 * flow), 12, HEAT, INK, lw=4, a=k * (1 - u))


def s_race(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#BFE3F5", "#EEF8FF"))
    g.rect(-200, 1640, W + 400, 400, SNOWC, INK, lw=7)
    km, kw, kp = c.on("Metal", 0.3), c.on("wood", 0.3), c.on("plastic", 0.3)
    for x, kind, k, flow, lab in ((200, "metal", km, 1.0, "METAL"), (540, "wood", kw, 0.18, "WOOD"), (880, "plastic", kp, 0.14, "PLASTIC")):
        if k <= 0: continue
        with g.at(x, 1640, 0, back_out(k, 1.5)):
            with g.at(-x, -1640):
                post(g, x, kind, k, flow, c.t - c.w(lab.capitalize() if kind == "metal" else lab.lower()))
        with g.screen():
            g.text(lab, x, 1760, 74, PAL["yellow"] if kind == "metal" else PAL["cream"], sw=12, sc=pop(c.t, c.w("Metal" if kind == "metal" else kind) - 0.1, 0.3))
    if km > 0:
        with g.screen():
            g.text("FAST!", 200, 330, 92, HEAT, sw=14, depth=8, sc=pop(c.t, c.w("faster") - 0.1, 0.3), a=c.on("faster", 0.2))


SNOWC = "#F4FBFF"


def s_drain(g, c):
    """'the warmth drains out of your wet tongue in a flash': heat dots rush from the tongue into the steel; thermometer plunges."""
    macro_bg(g)
    metal_wall(g, 700)
    k = c.on("flash", 0.35)
    cool = clamp(c.since("drains") / 1.6) * 0.6 + 0.4 * k
    big_tongue(g, 700, col=mix(TONGUE, "#B9A6D6", cool * 0.6))
    n = 16
    sp = 0.5 + 1.8 * clamp(c.since("drains") / 0.8)
    for i in range(n):
        u = (c.t * sp + i / n) % 1.0
        y0 = 800 + (i * 37) % 320
        x = lerp(300, 1150, u); y = y0 + (u - 0.45) * 600 * max(0, u - 0.4)
        g.glow(x, y, 40, HEAT, 0.5 * (1 - u))
        g.circle(x, y, 14, HEAT, INK, lw=4, a=1 - u * 0.8)
    arrow(g, 520, 700, 900, 700, HEAT, w=26, k=c.on("drains", 0.3))
    # thermometer on the left
    with g.screen():
        tx, ty = 190, 1530
        g.rc(tx, ty - 200, 70, 420, "#FFFFFF", INK, lw=8, r=35)
        g.circle(tx, ty + 40, 66, mix("#FF4B3A", "#5FB8FF", cool), INK, lw=8)
        lvl = 1 - cool
        g.rc(tx, ty - 10 - 170 * lvl, 34, 40 + 340 * lvl, mix("#FF4B3A", "#5FB8FF", cool), None, r=17)
        g.text("WARMTH", tx + 10, ty + 170, 64, PAL["cream"], sw=11, anchor="m")


def micro(g, c, frz=0.0, hi_bumps=0.0, hi_pits=0.0, lock=0.0):
    """Microscope view: tongue bumps (top) and metal pits (bottom) with a water layer between that freezes left to right."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0E2236", "#173A5C"))
    cx, cy, R = 540, 1000, 470
    g.circle(cx, cy, R + 34, "#2A3A4E", INK, lw=12)
    with g.clip(circle=(cx, cy, R)):
        g.fill_all("#203A55")
        top = [(x, 920 + 34 * math.sin(x / 38) + 14 * math.sin(x / 13)) for x in range(0, W + 1, 12)]
        bot = [(x, 1080 + (40 if (x // 54) % 2 else 0) + 12 * math.sin(x / 17)) for x in range(0, W + 1, 12)]
        # water / ice layer between
        layer = top + bot[::-1]
        g.poly(layer, mix("#7FD3FF", "#EAF8FF", frz), None, a=0.95)
        if frz > 0:
            edge = W * frz
            R2 = rnd(6).random
            for i in range(40):
                x = R2() * W; y = 960 + R2() * 130
                if x < edge:
                    g.poly([(x, y - 18), (x + 14, y), (x, y + 18), (x - 14, y)], "#FFFFFF", None, a=0.7)
            g.line([(edge, 900), (edge, 1140)], "#FFFFFF", 6, a=0.6 * (1 - frz))
        g.poly(top + [(W, 0), (0, 0)], mix(TONGUE, "#FFFFFF", 0.05), INK, lw=8)
        g.poly(bot + [(W, H), (0, H)], g.lgrad(0, 1080, 0, 1500, "#C9D4DE", "#7F8D9A"), INK, lw=8)
        if hi_bumps > 0:
            for x in range(60, W, 240):
                g.glow(x, 935 + 34 * math.sin(x / 38), 110, PAL["yellow"], 0.85 * hi_bumps)
        if hi_pits > 0:
            for x in range(27 + 54, W, 216):
                g.glow(x, 1110, 100, PAL["yellow"], 0.85 * hi_pits)
    with g.screen():
        g.text("TONGUE", cx, cy - R - 90, 80, TONGUE, sw=13, a=1 - lock)
        g.text("METAL", cx, cy + R + 100, 80, STEEL, sw=13, a=1 - lock)


def s_freeze(g, c):
    macro_bg(g)
    metal_wall(g, 700)
    big_tongue(g, 700)
    k = c.on("freezes", 0.5)
    g.ellipse(700, 960, 60, 230 * (0.4 + 0.6 * k), mix("#7FD3FF", "#FFFFFF", k), INK, lw=6, a=0.95)
    sparkles(g, c.t, [(700, 760), (720, 900), (690, 1060), (730, 1180)], seed=2, col="#FFFFFF", r=28, t0=c.w("freezes"))
    with g.screen():
        g.text("FROZEN SOLID", W / 2, 470, 104, "#FFFFFF", sw=16, depth=8, sc=pop(c.t, c.w("solid") - 0.1, 0.3))


def s_micro(g, c):
    micro(g, c, frz=0.25 + 0.55 * clamp(c.u), hi_bumps=c.on("bumps", 0.3) * (1 - c.on("pits", 0.3)), hi_pits=c.on("pits", 0.3))


def s_lock(g, c):
    k = c.on("locks", 0.25)
    micro(g, c, frz=0.8 + 0.2 * clamp(c.t / 0.5), lock=0.0)
    with g.at(540, 1000, 0, back_out(k, 1.8)):                                      # padlock snaps shut
        g.path("M-60 -40 L-60 -110 Q-60 -170 0 -170 Q60 -170 60 -110 L60 " + str(-40 - 50 * (1 - k)), None, INK, lw=34)
        g.path("M-60 -40 L-60 -110 Q-60 -170 0 -170 Q60 -170 60 -110 L60 " + str(-40 - 50 * (1 - k)), None, "#C9D4DE", lw=20)
        g.rc(0, 20, 190, 150, PAL["yellow"], INK, lw=10, r=22)
        g.circle(0, 10, 18, INK, None); g.rc(0, 40, 12, 40, INK, None)
    with g.screen():
        g.text("LOCKED", W / 2, 1640, 120, PAL["yellow"], sw=18, depth=10, sc=pop(c.t, c.w("locks") - 0.05, 0.3))


def s_pull(g, c):
    """'Pull hard, and that ice can tear skin right off': he leans back, the tongue stretches; big warning."""
    lean = ease_io(clamp(c.since("Pull") / 0.8))
    mx, my = stuck_scene(g, c, "angry" if c.t < c.w("tear") else "shocked", "shrug", "reach_r", lean=lean, stretch=lean, wobble=0.4)
    pain_marks(g, PX - 40, my, 100, c.gt, n=5, col="#FF5B4B", a0=-3.0, a1=0.2)
    k = c.on("tear", 0.3)
    with g.screen():
        g.text("DON'T PULL", 540, 300, 128, "#FF5B4B", sw=18, depth=10, sc=pop(c.t, c.w("tear") - 0.05, 0.3), a=k)
    no_sign(g, PX + 150, my - 170, 110, k=k)


def s_never(g, c):
    """'So never pull.' The friend runs in with a steaming mug."""
    winter_yard(g, c.gt)
    metal_pole(g, PX, PTOP, PBOT, frost=0.7)
    char2(g, WHO, CX, CY, CH, "worried", "down", "shrug", t=c.gt, view="3q")
    beanie(g, CX, CY, CH, view="3q"); scarf(g, CX, CY, CH, t=c.gt)
    mx, my = mouth_pt(CX, CY, CH, "3q")
    tongue(g, mx, my, PX - 38, my + 8, frozen=1.0)
    fx = lerp(1300, 985, ease_out(clamp(c.t / 0.6)))
    char2(g, PAL2, fx, 1820, 1000, "deadpan", "point", "hold", t=c.gt, flip=True, view="3q")
    beanie(g, fx, 1820, 1000, col="#FFC93C", band="#3E7CB1", view="3q", flip=True); scarf(g, fx, 1820, 1000, col="#5ED3B5", stripe="#FFF4E0", flip=True, t=c.gt)
    hx, hy = hand_pt(PAL2, "hold", fx, 1820, 1000, side=1, flip=True)
    mug(g, hx, hy - 10, c.gt)


def mug(g, x, y, t, tilt=0.0):
    with g.at(x, y, tilt):
        g.rc(0, 0, 90, 100, "#FFF4E0", INK, lw=7, r=14)
        g.path("M45 -25 Q85 -25 85 5 Q85 35 45 30", None, INK, lw=10)
        g.rc(0, -6, 90, 20, "#FF6B5B", None)
    steam(g, t, x, y - 60, n=3, h=120, col="#FFFFFF", a=0.7, w=9, spread=26)


def s_pour(g, c):
    """'Pour on warm water, the ice glue melts...': the friend pours warm water over the contact point; the ice ring melts away."""
    winter_yard(g, c.gt, snowing=False)
    melt = c.on("melts", 0.8)
    metal_pole(g, PX, PTOP, PBOT, frost=0.7 * (1 - melt))
    char2(g, WHO, CX, CY, CH, "worried" if c.t < c.w("melts") else "deadpan", "down", "down", t=c.gt, view="3q")
    beanie(g, CX, CY, CH, view="3q"); scarf(g, CX, CY, CH, t=c.gt)
    mx, my = mouth_pt(CX, CY, CH, "3q")
    tongue(g, mx, my, PX - 38, my + 8, frozen=1 - melt)
    fx = 985
    char2(g, PAL2, fx, 1820, 1000, "deadpan", "down", "up", t=c.gt, flip=True, view="3q")
    beanie(g, fx, 1820, 1000, col="#FFC93C", band="#3E7CB1", view="3q", flip=True); scarf(g, fx, 1820, 1000, col="#5ED3B5", stripe="#FFF4E0", flip=True, t=c.gt)
    hx, hy = hand_pt(PAL2, "up", fx, 1820, 1000, side=1, flip=True)
    tilt = -1.0 * ease_out(clamp(c.since("Pour") / 0.4))
    mx2, my2 = hx + 40, hy - 40
    mug(g, mx2, my2, c.gt, tilt)
    if c.t > c.w("Pour") + 0.3:                                                     # the water stream onto the contact point
        sx, sy = mx2 - 50, my2 - 10
        k = clamp((c.t - c.w("Pour") - 0.3) / 0.25)
        pts = [(sx, sy), (lerp(sx, PX - 30, 0.5), sy + 10), (PX - 30, lerp(sy, my, k)), (PX - 26, lerp(sy, PBOT - 80, k))]
        g.line(pts, "#7FD3FF", 24, a=0.85); g.line(pts, "#FFFFFF", 7, a=0.6)
        steam(g, c.gt, PX - 30, my - 30, n=3, h=140, col="#FFFFFF", a=0.6, w=10, spread=40)
    with g.screen():
        g.text("WARM, NOT HOT", 540, 330, 96, PAL["yellow"], sw=15, depth=8, sc=pop(c.t, c.w("warm") - 0.1, 0.3), a=c.on("warm", 0.2))


def s_free(g, c):
    """'...and you're free.' Same framing as frame 1 (loop): he pops off the pole, arms up."""
    k = c.on("free", 0.25)
    mx, my = stuck_scene(g, c, "shocked" if k < 0.5 else "smug", "up", "shrug" if k < 0.5 else "up", frozen=0.0, wobble=0.3, free=k)
    burst(g, PX - 50, my, 40, 130, 10, "#FFFFFF", 8, k=seg(c.t, c.w("free"), 0.35))


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, "frozen"), cam=ZOOM(1.0, 1.05, (600, 1150)), sfx=[(0.0, "freeze", 0.5), (0.02, "sting", 0.35)], tr="cut")
V.shot("H1", s_hook, ("frozen", 1), cam=ZOOM(1.45, 1.55, (650, 800)), tr="cut")
V.shot("L01", s_glue, cam=ZOOM(1.0, 1.08, (700, 960)), sfx=[("spit", "bloop", 0.3), ("glue", "freeze", 0.4)])
V.shot("L02", s_race, (0, "than"), cam=ZOOM(1.3, 1.36, (300, 1150)), sfx=[("Metal", "pop", 0.3), ("faster", "whoosh", 0.3)])
V.shot("L02", s_race, ("than", "Touch"), cam=ZOOM(0.98, 1.02, (540, 1150)), tr="cut", sfx=[("wood", "pop", 0.25), ("plastic", "pop", 0.25)])
V.shot("L02", s_drain, ("Touch", "drains"), cam=ZOOM(1.0, 1.06, (640, 960)), sfx=[(0.05, "bloop", 0.25)])
V.shot("L02", s_drain, ("drains", 1), cam=ZOOM(1.12, 1.2, (560, 1050)), tr="cut", sfx=[("drains", "rush", 0.35), ("flash", "freeze", 0.35)])
V.shot("L03", s_freeze, (0, "into"), cam=ZOOM(1.05, 1.15, (700, 960)), sfx=[("freezes", "freeze", 0.4)])
V.shot("L03", s_micro, ("into", "and"), cam=ZOOM(1.0, 1.06, (540, 1000)), sfx=[("bumps", "pop", 0.25)])
V.shot("L03", s_micro, ("and", "Now"), cam=ZOOM(1.25, 1.32, (540, 1060)), tr="cut", sfx=[("pits", "pop", 0.25)])
V.shot("L03", s_lock, ("Now", 1), cam=ZOOM(1.08, 1.0, (540, 1000)), sfx=[("locks", "click", 0.5)])
V.shot("L04", s_pull, (0, "tear"), cam=ZOOM(1.0, 1.06, (600, 1150)), music="tension", sfx=[("Pull", "whoosh", 0.3)])
V.shot("L04", s_pull, ("tear", 1), cam=ZOOM(1.35, 1.45, (560, 850)), tr="cut", sfx=[("tear", "alarm", 0.35)])
V.shot("L05", s_never, (0, "Pour"), cam=ZOOM(0.96, 1.0, (680, 1250)), music="playful", sfx=[(0.1, "footsteps", 0.25)])
V.shot("L05", s_pour, ("Pour", "and"), cam=ZOOM(1.12, 1.2, (700, 980)), sfx=[("Pour", "splash", 0.3), ("melts", "melt", 0.4)])
V.shot("L05", s_free, ("and", 1), cam=ZOOM(1.0, 1.05, (600, 1150)), sfx=[("free", "boing", 0.35)])
V.build()
V.title_out = V.voice0["H1"] + V.T["H1"]["dur"]

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=6, scale=0.16))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-026.mp4"))
