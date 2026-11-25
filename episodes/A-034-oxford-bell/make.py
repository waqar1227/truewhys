"""A-034 "This Bell Has Rung 10 Billion Times on the Same Batteries" — standalone Short, Style F + cast v2.2 (Physicist, Gentleman,
Professor, Student). Studio pattern 3 (singular object spotlight with one vivid number). New idea tested: a fixed "time-lapse room":
the decades change around the bell while it keeps ringing. Slot Sat 2 Jan 2027 18:00 UTC.
python episodes/A-034-oxford-bell/make.py sheet|qa|big <t,..>|render
Code-drawn version of the Oxford Electric Bell's layout (two small brass bells on two tall dry piles, a tiny ball between them, under
glass), a generic old lab corridor (no real people or signs), a generic sandstone college. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_split import split_long
from flat_fx import burst, sparkles, arrow, no_sign, qmark
from flat_bell import bell_case, ball_x, lab_room, college, ten_billion, pile_xray, SULFUR

V = Video(EP, title=("RINGING", "SINCE 1840?"), music="curious")
V.title_y = 0.075
CX, CY, CS = 470, 1200, 0.72                 # bell case on its plinth in the lab framing


def lab(g, c, era="now", ring=1.0, **kw):
    lab_room(g, c.gt, era=era, k_sky=c.t)
    bell_case(g, CX, CY, CS, c.gt, ring=ring, **kw)


def phys(g, c, expr, pl="down", pr="point", x=880, h=1150, a=1.0):
    char2(g, "physicist", x, 2010, h, expr, pl, pr, t=c.gt, flip=True, view="3q", prop=False, a=a)


def lbl(g, c, word, txt, x, y, size=120, col="#FFFFFF"):
    with g.screen():
        g.text(txt, x, y, size, col, sw=size * 0.14, depth=size * 0.08, sc=pop(c.t, c.w(word) - 0.08, 0.3), a=c.on(word, 0.2))


# ------------------------------------------------------------------ hook / loop
def s_hook(g, c):
    """Frame 1: the little ball already flicking between the two brass bells (spark at each touch); the physicist leans in, amazed."""
    lab(g, c)
    phys(g, c, "shocked", "down", pose_at(c.t, [(0, "point"), (1.8, "point")]))


def s_batteries(g, c):
    """'...on the same batteries': push in on the two tall piles; they glow softly."""
    lab(g, c, sulfur=0.4 * c.on("same", 0.4))
    lbl(g, c, "batteries", "SAME BATTERIES", W / 2, 1650, 100, "#FFC93C")


def s_loop(g, c):
    """Last shot: back to the hook framing; the physicist smiles, then leans in amazed again (ends on frame 1)."""
    lab(g, c)
    phys(g, c, "smile" if c.u < 0.75 else "shocked", "down", "point")


# ------------------------------------------------------------------ L01 ten billion rings
def s_count(g, c):
    """'About ten billion rings': a counter rolls up to 10,000,000,000 above the ringing bell."""
    lab(g, c)
    with g.screen():
        ten_billion(g, W / 2, 380, c.u * 1.25, 104)
        g.text("RINGS", W / 2, 510, 90, "#FFFFFF", sw=12, a=c.on("rings", 0.2))


def s_inside(g, c):
    """'and nobody knows exactly what's inside them': X-ray of one pile, stacked discs and a glowing question mark."""
    g.fill_all(g.rgrad(540, 960, 1200, "#1B6E86", "#0B3F4C"))
    pile_xray(g, 540, 1700, 1.25, c.gt, k=ease_out(clamp(c.u * 2.0)))


# ------------------------------------------------------------------ L02 Oxford, two bells on two dry batteries
def s_college(g, c):
    """'It sits in a lab in Oxford': a generic old sandstone college at golden hour."""
    college(g, c.gt)
    lbl(g, c, "Oxford", "OXFORD", W / 2, 1750, 140, "#FFFFFF")


def s_diagram(g, c):
    """'Two little brass bells, each on top of a tall dry battery': big clean view of the apparatus, labels pop."""
    g.fill_all(g.rgrad(540, 900, 1300, "#2E4A6E", "#132238"))
    bell_case(g, 540, 1720, 1.05, c.gt, glass=0, sulfur=0.3 * c.on("battery", 0.4))
    lbl(g, c, "brass", "BRASS BELLS", W / 2, 340, 100, "#FFC93C")
    lbl(g, c, "battery", "DRY BATTERIES", W / 2, 1830, 96, "#FFFFFF")


# ------------------------------------------------------------------ L03 how it rings
def s_pea(g, c):
    """'Between them hangs a metal ball, smaller than a pea': macro of the ball on its thread with a green pea next to it for scale."""
    g.fill_all(g.rgrad(540, 960, 1200, "#3E2A20", "#1A120E"))
    g.line([(470, -20), (470, 900)], "#C9B79A", 6)
    sw = 12 * math.sin(c.t * 3)
    g.circle(470 + sw, 960, 120, "#C9CED6", INK, lw=10)
    g.circle(430 + sw, 920, 36, "#FFFFFF", None, a=0.8)
    k = ease_out(clamp((c.t - c.w("pea") + 0.1) / 0.4))
    if k > 0:
        g.circle(lerp(1200, 790, k), 980, 160, "#7CC452", INK, lw=10)
        g.circle(lerp(1200, 790, k) - 50, 930, 40, "#C8F0A0", None, a=0.7)
        lbl(g, c, "pea", "PEA", 790, 1240, 110, "#C8F0A0")


def s_charge(g, c):
    """'One bell charges it, pushes it away, the other bell pulls it in, and back again': slow motion close on the bells,
    +/- charges flip as the ball swings from one bell to the other."""
    g.fill_all(g.rgrad(540, 900, 1300, "#2E4A6E", "#132238"))
    bell_case(g, 540, 2350, 1.55, c.t * 0.22, glass=0, charge=1.0, hl_ball=0.5 + 0.5 * math.sin(c.t * 6))


def s_twice(g, c):
    """'Twice every second.': the ball back at full speed, a ticking second hand ring."""
    lab(g, c)
    k = (c.t % 1.0)
    with g.screen():
        g.circle(W / 2, 1720, 90, "#FFF4E0", INK, lw=8)
        g.line([(W / 2, 1720), (W / 2 + 70 * math.sin(k * TAU), 1720 - 70 * math.cos(k * TAU))], INK, 8)
    lbl(g, c, "Twice", "2× A SECOND", W / 2, 1560, 110, "#FFC93C")


# ------------------------------------------------------------------ L04 time-lapse through the eras
def s_eras(g, c, eras, labels, who):
    """Fixed camera on the bell; the room snaps from era to era (flash between), the bell never stops."""
    n = len(eras)
    i = min(n - 1, int(c.u * n))
    uu = c.u * n - i
    lab(g, c, era=eras[i])
    cid, flip = who[i]
    char2(g, cid, 880 if flip else 180, 2000, 980, "curious", "down", "hold", t=c.gt, flip=flip, view="3q", prop=False)
    with g.screen():
        g.text(labels[i], W / 2, 1720, 150, "#FFFFFF", sw=20, depth=10, sc=pop(uu, 0.0, 0.25))
        if uu < 0.12:
            g.rect(0, 0, W, H, "#FFFFFF", None, a=0.55 * (1 - uu / 0.12))


def s_wars(g, c):
    """'It kept ringing through two world wars': 1840 lab -> 1914 -> 1939 (taped windows, a radio)."""
    s_eras(g, c, ["1840", "1910", "1940"], ["1840", "1914", "1939"], [("gent", True), ("prof", True), ("prof", False)])


def s_planes(g, c):
    """'the first planes': the 1910s lab, a biplane crosses the window."""
    s_eras(g, c, ["1910"], ["1903"], [("prof", True)])


def s_moon(g, c):
    """'and the moon landing': the 1969 lab, a moon landing on the TV."""
    s_eras(g, c, ["1969"], ["1969"], [("student", True)])


# ------------------------------------------------------------------ L05 silent, sealed, sulfur
def s_hear(g, c):
    """'But you can't hear it.': the physicist cups an ear to the glass; a speaker icon crossed out."""
    lab(g, c)
    phys(g, c, "suspicious", "down", "reach_r", x=820)
    with g.screen():
        with g.at(W / 2, 330):
            g.path("M-70 -40 L-20 -40 L40 -95 L40 95 L-20 40 L-70 40 Z", "#FFF4E0", INK, lw=8)
        no_sign(g, W / 2 - 10, 330, 140, k=c.on("hear", 0.3))


def s_glass(g, c):
    """'It's sealed behind two layers of glass': the two glass covers light up one after the other."""
    lab(g, c, hl_glass=0.5 + 0.5 * math.sin(c.t * 5))
    lbl(g, c, "two", "2 LAYERS OF GLASS", W / 2, 1700, 96, "#BFE9FF")


def s_sulfur(g, c):
    """'and its batteries are coated in sulfur, so their recipe is still a mystery': the piles glow sulfur-yellow, X-ray '?'."""
    g.fill_all(g.rgrad(540, 900, 1300, "#5A3E2A", "#24180F"))
    bell_case(g, 540, 1760, 1.05, c.gt, glass=0, sulfur=c.on("sulfur", 0.4), xray=c.on("recipe", 0.4))
    lbl(g, c, "sulfur", "SULFUR", W / 2, 300, 120, SULFUR)


# ------------------------------------------------------------------ L06 one day
def s_runout(g, c):
    """'One day the charge will run out.': a charge meter beside the bell creeps down very slowly."""
    g.fill_all(g.rgrad(540, 900, 1300, "#4A2E5A", "#1E1430"))
    bell_case(g, 420, 1760, 0.95, c.gt, glass=0)
    v = lerp(0.62, 0.55, c.u)
    with g.at(900, 1100):
        g.rect(-70, -420, 140, 840, "#1A2430", INK, lw=9, r=20)
        g.rect(-50, 400 - 800 * v, 100, 800 * v, mix("#FF6B5B", "#5ED3B5", v), None, r=12)
        g.rect(-30, -450, 60, 40, "#C9CED6", INK, lw=6, r=8)


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, "on"), cam=ZOOM(1.0, 1.04, (560, 900)), sfx=[(0.0, "ring_bell", 0.35), (0.0, "sting", 0.3), (0.5, "tick", 0.3), (1.0, "tick", 0.3)], tr="cut")
V.shot("H1", s_batteries, ("on", 1), cam=ZOOM(1.5, 1.6, (CX, 900)), tr="cut", sfx=[("same", "swell", 0.3)])
V.shot("L01", s_count, (0, "and"), cam=ZOOM(1.0, 1.04, (540, 900)), sfx=[(0.0, "whir", 0.3), ("rings", "ding", 0.35)])
V.shot("L01", s_inside, ("and", 1), cam=ZOOM(1.0, 1.05, (540, 1100)), tr="cut", sfx=[("nobody", "confuse", 0.35)])
V.shot("L02", s_college, (0, "Two"), cam=ZOOM(1.0, 1.05, (540, 900)), music="story", sfx=[(0.05, "whoosh", 0.3), (0.2, "bell", 0.2)])
V.shot("L02", s_diagram, ("Two", 1), cam=ZOOM(1.0, 1.04, (540, 1000)), tr="cut", sfx=[("brass", "ding", 0.35), ("battery", "pop", 0.35)])
V.shot("L03", s_pea, (0, "One"), cam=ZOOM(1.0, 1.05, (560, 960)), sfx=[("ball", "tick", 0.3), ("pea", "pop", 0.35)])
V.shot("L03", s_charge, ("One", "Twice"), cam=ZOOM(1.0, 1.04, (540, 900)), tr="cut", sfx=[("charges", "zap", 0.3), ("pushes", "whoosh_soft", 0.25), ("pulls", "whoosh_soft", 0.25)])
V.shot("L03", s_twice, ("Twice", 1), cam=ZOOM(1.0, 1.04, (540, 900)), tr="cut", sfx=[(0.0, "tick", 0.35), (0.5, "tick", 0.35), (1.0, "tick", 0.35)])
V.shot("L04", s_wars, (0, "first"), cam=still(), music="adventure", sfx=[(0.05, "whoosh", 0.3), (0.6, "whoosh", 0.3), (1.2, "whoosh", 0.3)])
V.shot("L04", s_planes, ("first", "moon"), cam=still(), tr="cut", sfx=[(0.0, "whoosh", 0.3), (0.2, "whir", 0.3)])
V.shot("L04", s_moon, ("moon", 1), cam=still(), tr="cut", sfx=[(0.0, "whoosh", 0.3), ("landing", "beep3", 0.25)])
V.shot("L05", s_hear, (0, "It's"), cam=ZOOM(1.0, 1.05, (620, 900)), music="curious", sfx=[("hear", "hmm", 0.3)])
V.shot("L05", s_glass, ("It's", "and"), cam=ZOOM(1.25, 1.32, (CX, 800)), tr="cut", sfx=[("glass", "shimmer", 0.35)])
V.shot("L05", s_sulfur, ("and", 1), cam=ZOOM(1.0, 1.05, (540, 1100)), tr="cut", sfx=[("sulfur", "sparkle", 0.35), ("mystery", "confuse", 0.35)])
V.shot("L06", s_runout, (0, "Until"), cam=ZOOM(1.0, 1.04, (620, 1100)), sfx=[("out", "power_off", 0.25)])
V.shot("L06", s_loop, ("Until", 1), cam=ZOOM(1.04, 1.0, (560, 900)), tr="cut", sfx=[("ringing", "ring_bell", 0.3)])
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
        V.render(str(EP / "final/A-034.mp4"))
