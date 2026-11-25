"""A-030 "Why One Bad Bulb Can Turn Off All Your Christmas Lights" — standalone Short, Style F + cast v2.2 (Friend, winter look). Slot Fri 25 Dec 2026 18:00 UTC.
python episodes/A-030-string-lights/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: a snowy porch at dusk with a string of coloured lights (neutral winter-holiday decoration, no religious
symbols), a series-loop diagram with moving charges, a big bulb cut-away (filament, lead wires, shunt), a loose bulb pushed back in.
Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_split import split_long
from flat_fx import burst, sparkles, steam, pain_marks
from flat_winter import hand_pt, beanie, scarf
from flat_lights import porch_dusk, string_pts, light_string, wave_on, big_bulb, loop_diagram, BULB_COLS

V = Video(EP, title=("ONE BULB,", "ALL DARK?"), music="cozy")
V.title_y = 0.075
WHO = "friend"
FX, FY, FH = 300, 1880, 1000
PTS = string_pts(-60, 1140, 690, n=17, sag=80, swags=3)
BAD = 7                                    # the bulb that fails
N = len(PTS)
SKIN = "#8D5A3C"


def friend(g, c, expr, pl, pr, x=FX):
    char2(g, WHO, x, FY, FH, expr, pl, pr, t=c.gt, view="3q", prop=False)
    beanie(g, x, FY, FH, col="#FF6B5B", band="#FFF4E0", view="3q")
    scarf(g, x, FY, FH, col="#FFC93C", stripe="#5ED3B5", t=c.gt)


def porch(g, c, on, dead=None, out=None, lit=1.0):
    porch_dusk(g, c.gt, lit=lit)
    light_string(g, PTS, on, t=c.gt, s=1.25, dead=dead, out=out)


def xbg(g, c, col="#141638"):
    g.fill_all(g.rgrad(540, 1000, 1200, "#2E2A66", col))
    R = rnd(3).random
    for i in range(40):
        g.circle(R() * W, R() * H, 3 + 4 * R(), "#FFFFFF", None, a=0.12 + 0.1 * math.sin(c.gt * 2 + i))


# ------------------------------------------------------------------ hook / loop framing
def s_hook(g, c):
    """Frame 1: one bulb pops with a spark and the darkness runs along the whole string; the friend jumps, arms up."""
    k = clamp(0.05 + c.t / 1.9)
    porch(g, c, wave_on(N, k, BAD), dead=BAD)
    x, y = PTS[BAD]
    burst(g, x, y + 80, 20, 60 + 120 * seg(c.t, 0, 0.45), 10, "#FFF4A8", 8, k=max(0.0, 1 - c.t / 0.6))
    steam(g, c.gt, x, y + 40, n=2, h=120, col="#DDDDEE", a=0.4, w=8)
    friend(g, c, "shocked", pose_at(c.t, [(0, "shrug"), (0.5, "up")]), "up")


def s_dead_close(g, c):
    """Close on the dark string: the burnt bulb smokes."""
    porch(g, c, 0.0, dead=BAD)
    x, y = PTS[BAD]
    steam(g, c.gt, x, y + 40, n=3, h=160, col="#DDDDEE", a=0.45, w=9)


# ------------------------------------------------------------------ L01
def s_flicker(g, c):
    """'One tiny bulb fails...': close on the lit string; the bad bulb flickers and pops on 'fails'."""
    tf = c.w("fails")
    on = [1.0] * N
    if c.t < tf:
        on[BAD] = 0.6 + 0.4 * (math.sin(c.gt * 37) > 0)
        porch(g, c, on)
    else:
        porch(g, c, on, dead=BAD)
        x, y = PTS[BAD]
        burst(g, x, y + 80, 20, 70 + 100 * seg(c.t, tf, 0.35), 10, "#FFF4A8", 8, k=max(0.0, 1 - (c.t - tf) / 0.5))
    with g.screen():
        g.text("1 BULB", W / 2, 1450, 120, PAL["yellow"], sw=17, depth=9, sc=pop(c.t, c.w("tiny") - 0.08, 0.3), a=c.on("tiny", 0.2))


def s_wave(g, c):
    """'...and suddenly every light on the string goes dark': the wide porch, the dark wave runs out from the dead bulb."""
    k = clamp(c.since("every") / 1.4) if c.t >= c.w("every") else 0.0
    porch(g, c, wave_on(N, k, BAD), dead=BAD)
    friend(g, c, "worried" if k < 0.9 else "deadpan", "hip", pose_at(c.t, [(0, "down"), (c.w("dark"), "shrug")]))


# ------------------------------------------------------------------ L02: series = one loop
LX, LY, LW_, LH_ = 540, 1020, 820, 980


def s_series(g, c):
    xbg(g, c)
    loop_diagram(g, LX, LY, LW_, LH_, c.gt, n=8, on=1.0)
    with g.screen():
        g.text("SERIES", W / 2, 400, 150, PAL["yellow"], sw=20, depth=10, sc=pop(c.t, c.w("series") - 0.08, 0.3), a=c.on("series", 0.2))


def s_loop(g, c):
    xbg(g, c)
    loop_diagram(g, LX, LY, LW_, LH_, c.gt, n=8, on=1.0, glow_loop=c.on("loop", 0.4) * (0.8 + 0.2 * math.sin(c.gt * 6)))
    with g.screen():
        g.text("ONE LOOP", W / 2, 400, 150, "#FFE066", sw=20, depth=10, sc=pop(c.t, c.w("single") - 0.08, 0.3), a=c.on("single", 0.2))


def s_flow(g, c):
    """'the power has to flow through every bulb in a row': current dots run round; a ring hops from bulb to bulb."""
    xbg(g, c)
    k = c.on("power", 0.4)
    hl = None
    if c.t >= c.w("every"):
        hl = min(7, int((c.t - c.w("every")) / max(0.2, (c.sh["dur"] - c.w("every")) / 8)))
    loop_diagram(g, LX, LY, LW_, LH_, c.gt, n=8, on=1.0, flow=k, hl=hl)
    with g.screen():
        g.text("POWER", W / 2, 400, 130, "#FFE066", sw=18, depth=9, sc=pop(c.t, c.w("power") - 0.08, 0.3), a=k)


# ------------------------------------------------------------------ L03: filament snaps, loop breaks
BBX, BBY = 540, 1080


def s_filament(g, c):
    xbg(g, c, "#181232")
    big_bulb(g, BBX, BBY, 1.6, c.gt, glow=0.6 + 0.4 * c.on("glows", 0.4), col="#FFC93C")
    with g.screen():
        g.text("THIN WIRE", W / 2, 360, 130, "#FFE066", sw=18, depth=9, sc=pop(c.t, c.w("wire") - 0.08, 0.3), a=c.on("wire", 0.2))


def s_snap(g, c):
    xbg(g, c, "#181232")
    b = c.on("snaps", 0.25)
    big_bulb(g, BBX, BBY, 1.6, c.gt, glow=1.0, broken=b, spark=max(0.0, 1 - c.since("snaps") / 0.5) if c.t >= c.w("snaps") else 0)
    with g.screen():
        g.text("SNAP!", W / 2, 360, 150, "#FF5B5B", sw=20, depth=10, sc=pop(c.t, c.w("snaps") - 0.08, 0.3), a=b)


def s_broken(g, c):
    """'the loop is broken, and the power stops for all of them': gap opens at one bulb, charges pile up, every bulb goes dark."""
    xbg(g, c)
    gk = c.on("broken", 0.3)
    off = c.on("stops", 0.5)
    loop_diagram(g, LX, LY, LW_, LH_, c.gt, n=8, on=1.0 - off, flow=1.0 - 0.7 * off, gap=3, gap_k=gk)
    with g.screen():
        g.text("BROKEN", W / 2, 400, 140, "#FF5B5B", sw=19, depth=10, sc=pop(c.t, c.w("broken") - 0.08, 0.3), a=gk)


# ------------------------------------------------------------------ L04: the shunt
def s_shunt(g, c):
    xbg(g, c, "#0F2A2A")
    k = c.on("shunt", 0.35)
    big_bulb(g, BBX, BBY, 1.6, c.gt, glow=1.0, shunt=max(c.on("bypass", 0.4) * 0.6, k))
    with g.screen():
        g.text("SHUNT", W / 2, 360, 160, "#5EF0B0", sw=21, depth=11, sc=pop(c.t, c.w("shunt") - 0.08, 0.3), a=k)
        if k > 0:
            g.line([(W / 2 + 180, 420), (BBX + 140, BBY - 64 * 1.6 + 10)], "#5EF0B0", 10, a=k)


def s_burn(g, c):
    xbg(g, c, "#0F2A2A")
    b = c.on("burns", 0.25)
    big_bulb(g, BBX, BBY, 1.6, c.gt, glow=1.0, broken=b, shunt=1.0, spark=max(0.0, 1 - c.since("burns") / 0.5) if c.t >= c.w("burns") else 0)


def s_bypass(g, c):
    """'the power jumps across it and keeps going': split frame feel — the bulb's shunt arcs, and in the loop the charges hop the dead bulb."""
    xbg(g, c, "#0F2A2A")
    k = c.on("jumps", 0.3)
    loop_diagram(g, LX, LY + 120, LW_, LH_ - 200, c.gt, n=8, on=1.0, flow=1.0, dead=3, bypass=k)
    with g.at(0, 0):
        big_bulb(g, 540, 540, 0.8, c.gt, glow=0.0, broken=1.0, shunt=1.0, arc=k)
    with g.screen():
        g.text("KEEPS GOING", W / 2, 1720, 110, "#5EF0B0", sw=16, depth=8, sc=pop(c.t, c.w("keeps") - 0.08, 0.3), a=c.on("keeps", 0.2))


# ------------------------------------------------------------------ L05: loose bulb, push it back
def s_loose(g, c):
    """'But a loose or missing bulb still breaks the loop...': close on the string, one bulb hangs half out; all dark."""
    porch(g, c, 0.0, out=(BAD, 0.8 + 0.2 * math.sin(c.gt * 5)))
    x, y = PTS[BAD]
    if c.t >= c.w("missing"):
        g.circle(x, y + 30, 46, None, "#FF9E3D", lw=8, a=c.on("missing", 0.3))
    with g.screen():
        g.text("LOOSE", W / 2, 1450, 140, "#FF9E3D", sw=19, depth=10, sc=pop(c.t, c.w("loose") - 0.08, 0.3), a=c.on("loose", 0.2))


def s_push(g, c):
    """'so push that one back in': a hand pushes the bulb up into its socket."""
    kp = c.on("push", 0.55)
    porch(g, c, 0.0, out=(BAD, 1 - ease_out(kp)))
    x, y = PTS[BAD]
    s = 1.25
    by = y + (70 + 40 * (1 - ease_out(kp))) * s
    g.path(f"M{x + 46} {by + 420} Q{x + 32} {by + 200} {x + 20} {by + 74} L{x - 24} {by + 74} Q{x - 32} {by + 220} {x - 46} {by + 420} Z",
           "#3E7CB1", INK, lw=9)
    g.ellipse(x, by + 40, 44, 52, SKIN, INK, lw=8)
    g.ellipse(x - 30, by + 10, 14, 28, SKIN, INK, lw=6, rot=-0.3)


def s_lightup(g, c):
    """'...and the whole string lights up': frame-1 framing, light runs out along the string, the friend smiles."""
    k = clamp(c.since("whole") / 1.0) if c.t >= c.w("whole") else 0.0
    porch(g, c, wave_on(N, k, BAD, reverse=True))
    friend(g, c, "smile" if k > 0.2 else "curious", pose_at(c.t, [(0, "hip"), (c.w("whole"), "up")]), "up" if k > 0.2 else "hip")
    if k > 0.3:
        sparkles(g, c.t, [PTS[2], PTS[8], PTS[13]], seed=4, col="#FFF4A8", r=34, t0=c.w("whole"))


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
BX, BY = PTS[BAD]
V.shot("H1", s_hook, (0, "whole"), cam=ZOOM(1.0, 1.04, (540, 1050)), sfx=[(0.0, "bulb_pop", 0.7), (0.05, "power_off", 0.55), (0.02, "sting", 0.3)], tr="cut")
V.shot("H1", s_dead_close, ("whole", 1), cam=ZOOM(2.0, 2.1, (BX, BY + 140)), tr="cut")
V.shot("L01", s_flicker, (0, "and"), cam=ZOOM(1.8, 1.9, (BX, BY + 200)), sfx=[("fails", "bulb_pop", 0.6)])
V.shot("L01", s_wave, ("and", 1), cam=ZOOM(1.0, 1.04, (540, 1050)), tr="cut", sfx=[("every", "power_off", 0.6)])
V.shot("L02", s_series, (0, "That's"), cam=ZOOM(1.0, 1.05, (540, 1000)), sfx=[(0.05, "whoosh", 0.3), ("series", "pop", 0.3)])
V.shot("L02", s_loop, ("That's", "and"), cam=ZOOM(1.04, 1.08, (540, 1000)), tr="cut", sfx=[("loop", "shimmer", 0.35)])
V.shot("L02", s_flow, ("and", 1), cam=ZOOM(1.0, 1.06, (540, 1000)), tr="cut", sfx=[("power", "zap", 0.3), ("row", "chime", 0.3)])
V.shot("L03", s_filament, (0, "If"), cam=ZOOM(1.0, 1.06, (540, 1000)), sfx=[("glows", "hum", 0.3)])
V.shot("L03", s_snap, ("If", "the"), cam=ZOOM(1.25, 1.35, (540, 820)), tr="cut", sfx=[("snaps", "bulb_pop", 0.7)])
V.shot("L03", s_broken, ("the", 1), cam=ZOOM(1.0, 1.04, (540, 1000)), tr="cut", sfx=[("broken", "thud", 0.4), ("stops", "power_off", 0.55)])
V.shot("L04", s_shunt, (0, "When"), cam=ZOOM(1.0, 1.08, (540, 1000)), music="curious", sfx=[("bypass", "shimmer", 0.3), ("shunt", "pop", 0.35)])
V.shot("L04", s_burn, ("When", "jumps"), cam=ZOOM(1.25, 1.32, (540, 820)), tr="cut", sfx=[("burns", "bulb_pop", 0.6)])
V.shot("L04", s_bypass, ("jumps", 1), cam=ZOOM(1.0, 1.04, (540, 1000)), tr="cut", sfx=[("jumps", "zap", 0.45), ("going", "chime", 0.35)])
V.shot("L05", s_loose, (0, "so"), cam=ZOOM(1.9, 2.0, (BX, BY + 220)), sfx=[("loose", "click", 0.4), ("loop", "thud", 0.3)])
V.shot("L05", s_push, ("so", "and"), cam=ZOOM(2.0, 2.1, (BX, BY + 260)), tr="cut", sfx=[("in", "click", 0.55)])
V.shot("L05", s_lightup, ("and", 1), cam=ZOOM(1.0, 1.04, (540, 1050)), tr="cut", music="cozy", sfx=[("whole", "power_on", 0.6), ("up", "sparkle", 0.4)])
V.build()
split_long(V, maxd=2.4, keep_cam=True)          # no shot longer than ~2.6 s (a visual change at least every 3 s)
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
        V.render(str(EP / "final/A-030.mp4"))
