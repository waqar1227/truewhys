"""A-027 "Why Reindeer Eyes Turn Blue in Winter" — standalone Short, Style F + cast v2.2 (Herder + reindeer). Slot Thu 24 Dec 2026 18:00 UTC.
python episodes/A-027-reindeer-eyes/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: Arctic night with aurora, midnight-sun summer tundra, a herder with a torch, reindeer (side + face),
an eye cross-section with the mirror layer (tapetum), fluid + pressure, fibres packing tighter, twilight. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import burst, arrow, sparkles, ring_wave, gauge, no_sign
from flat_winter import tundra_night, tundra_summer, reindeer, reindeer_face, torch_beam, torch, hand_pt, stars, aurora

V = Video(EP, title=("WHY ARE", "THEY BLUE?"), music="mystery")
V.title_y = 0.075
BLUE, GOLD, RET, LIGHT = "#4FA8FF", "#FFC23A", "#FF9FB0", "#FFF4C8"
WHO = "herder"
HX, HY, HH = 215, 1860, 960                  # herder feet + height (frame 1)
FX, FY, FS = 790, 1060, 0.8                  # reindeer face (eyes centre) + scale


# ------------------------------------------------------------------ night encounter (hook + loop)
def encounter(g, c, k_glow=1.0, expr="shocked"):
    tundra_night(g, c.gt)
    hx, hy = hand_pt(WHO, "explain", HX, HY, HH)
    ang = math.atan2(FY - hy, FX - hx)
    torch_beam(g, hx + 70 * math.cos(ang), hy + 70 * math.sin(ang), FX, FY + 40, w1=560, a=0.2)
    reindeer_face(g, FX, FY, FS, t=c.gt, eye=BLUE, glow=k_glow, tilt=0.03 * math.sin(c.gt * 0.9))
    char2(g, WHO, HX, HY, HH, expr, pose_at(c.t, [(0, "down"), (0.2, "shrug")]), "explain", t=c.gt, view="3q")
    torch(g, hx, hy, ang)


def s_hook(g, c):
    """Frame 1: the torch beam lands on a reindeer in the dark and two eyes flash bright blue; the herder jumps."""
    flash = 1 - seg(c.t, 0.0, 0.5)
    encounter(g, c, k_glow=1.0)
    ring_wave(g, FX - 78, FY, 30, 220, seg(c.t, 0.0, 0.6), BLUE, 12)
    ring_wave(g, FX + 78, FY, 30, 220, seg(c.t, 0.0, 0.6), BLUE, 12)
    if flash > 0:
        g.glow(FX, FY, 700, "#BFE3FF", 0.35 * flash)


def s_hook_close(g, c):
    tundra_night(g, c.gt)
    torch_beam(g, -200, 1900, FX, FY + 60, w1=700, a=0.2)
    reindeer_face(g, FX, FY, FS, t=c.gt, eye=BLUE, glow=1.0 + 0.15 * math.sin(c.gt * 5))


def s_summer(g, c):
    tundra_summer(g, c.gt)
    reindeer(g, 400, 1660, 1.15, t=c.gt, eye=GOLD, glow=0.4 + 0.6 * c.on("gold", 0.3), walk=0.6, head=0.1)
    with g.screen():
        g.text("SUMMER", W / 2, 360, 120, GOLD, sw=18, depth=10, sc=pop(c.t, 0.05, 0.3))


def s_winter(g, c):
    tundra_night(g, c.gt)
    reindeer(g, 400, 1660, 1.15, t=c.gt, eye=BLUE, glow=c.on("blue", 0.4), walk=0.0, head=0.0)
    with g.screen():
        g.text("WINTER", W / 2, 360, 120, BLUE, sw=18, depth=10, sc=pop(c.t, 0.05, 0.3))


# ------------------------------------------------------------------ eye cross-section
EC, ER = (560, 1000), 380


def eye_section(g, c, mirror=GOLD, pupil=0.35, fluid=0.0, bulge=0.0, block=0.0):
    """Side cut of the eye: light enters on the left through the pupil and lens; retina (pink) and the mirror layer behind it on the right."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0B1F36", "#163A58"))
    with g.layer(0.3):
        stars(g, 40, 7, t=c.gt)
    cx, cy = EC
    r = ER * (1 + 0.05 * bulge)
    g.circle(cx, cy, r + 46, "#8A6446", INK, lw=10)                                 # fur around the eye
    g.circle(cx, cy, r, mix("#EAF2F8", "#BFE3FF", 0.3 * fluid), INK, lw=10)
    if fluid > 0:                                                                  # extra fluid: drifting drops
        R = rnd(4).random
        for i in range(int(18 * fluid)):
            a0 = R() * TAU; rr = R() * r * 0.75
            x, y = cx + rr * math.cos(a0 + c.gt * 0.3), cy + rr * math.sin(a0 + c.gt * 0.3)
            g.path(f"M{x} {y-40} Q{x+28} {y} {x} {y+24} Q{x-28} {y} {x} {y-40} Z", "#7FC8FF", INK, lw=5, a=0.9)
    # mirror layer (tapetum) then retina on the back (right) wall
    for rad, col, wd in ((r - 26, mirror, 30), (r - 58, RET, 26)):
        if col is None:
            continue
        g.c.new_path(); g.c.arc(cx, cy, rad, -1.05, 1.05)
        g.c.set_source_rgba(*rgba(INK)); g.c.set_line_width(wd + 10); g.c.stroke()
        g.c.new_path(); g.c.arc(cx, cy, rad, -1.05, 1.05)
        g.c.set_source_rgba(*rgba(col)); g.c.set_line_width(wd); g.c.stroke()
    if mirror:
        for i in range(5):
            a0 = -0.8 + i * 0.4
            g.circle(cx + (r - 26) * math.cos(a0), cy + (r - 26) * math.sin(a0), 6, "#FFFFFF", None, a=0.7)
    # front: cornea bulge, iris + pupil, lens
    g.path(f"M{cx-r*0.86} {cy-r*0.5} Q{cx-r*1.22} {cy} {cx-r*0.86} {cy+r*0.5}", "#DDF1FF", INK, lw=8)
    ph = 40 + 120 * pupil
    g.rect(cx - r * 0.9, cy - 170, 30, 170 - ph / 2, "#5A3A26", INK, lw=6)
    g.rect(cx - r * 0.9, cy + ph / 2, 30, 170 - ph / 2, "#5A3A26", INK, lw=6)
    g.ellipse(cx - r * 0.62, cy, 56, 120, "#CFEFFF", INK, lw=7, a=0.9)
    if block > 0:                                                                  # drain at the front corner blocked
        bx, by = cx - r * 0.78, cy + r * 0.62
        g.circle(bx, by, 26, "#22344A", INK, lw=6)
        with g.at(bx, by, 0, back_out(block, 2.0)):
            g.line([(-30, -30), (30, 30)], "#FF5B4B", 14); g.line([(-30, 30), (30, -30)], "#FF5B4B", 14)
    return cx, cy, r


def ray(g, pts, u, col=LIGHT, w=18, a=1.0):
    """A light ray drawn along pts up to fraction u, with a bright head."""
    L = [0.0]
    for p, q in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(p, q))
    s = clamp(u) * L[-1]
    out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= s:
            out.append(pts[i])
        else:
            k = (s - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append((lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k)))
            break
    if len(out) > 1:
        g.line(out, col, w + 14, a=0.25 * a); g.line(out, col, w, a=a)
        g.glow(out[-1][0], out[-1][1], 60, col, 0.7 * a)


def ray_path(cx, cy, r):
    hit = (cx + (r - 40) * math.cos(-0.12), cy + (r - 40) * math.sin(-0.12))
    return [(-120, cy - 70), (cx - r * 0.9, cy - 20), (cx - r * 0.62, cy - 10), hit, (cx - r * 0.62, cy + 30), (cx - r * 0.9, cy + 40), (-120, cy + 110)]


def s_mirror(g, c):
    cx, cy, r = eye_section(g, c, mirror=GOLD if c.on("mirror", 0.2) > 0 else None)
    pts = ray_path(cx, cy, r)
    ray(g, pts[:4], clamp(c.since("bounces") / 0.5) if c.w("bounces") < c.T else clamp(c.t / 1.2))
    with g.screen():
        g.text("MIRROR", cx + r * 0.62, cy - r - 110, 104, GOLD, sw=16, depth=8, sc=pop(c.t, c.w("mirror") - 0.1, 0.3), a=c.on("mirror", 0.15))


def s_chance(g, c):
    cx, cy, r = eye_section(g, c, mirror=GOLD)
    pts = ray_path(cx, cy, r)
    u = 0.5 + 0.5 * clamp(c.t / 1.0)
    ray(g, pts, u)
    k = c.on("second", 0.3)
    for i in range(4):                                                             # retina cells light up again
        a0 = -0.5 + i * 0.3
        g.glow(cx + (r - 58) * math.cos(a0), cy + (r - 58) * math.sin(a0), 50, "#FFFFFF", 0.7 * k)
    with g.screen():
        g.text("2 CHANCES", W / 2, 470, 110, LIGHT, sw=16, depth=8, sc=pop(c.t, c.w("second") - 0.1, 0.3), a=k)


def s_sun(g, c):
    """'the sun hides for weeks': winter sky, the sun slides under the horizon, day counter flips."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0B1F36", "#24507A", "#5A7FA8"))
    with g.layer(0.3):
        stars(g, 50, 5, t=c.gt)
    k = c.on("hides", 0.8)
    sy = lerp(1280, 1520, k)
    g.glow(540, 1360, 380, "#FFB07A", 0.45 * (1 - k * 0.7))
    g.circle(540, sy, 110, "#FFD08A", INK, lw=8)
    g.rect(-400, 1380, W + 800, 800, g.lgrad(0, 1380, 0, 1900, "#3A5E80", "#1E3A58"), None)
    g.line([(-400, 1380), (W + 400, 1380)], INK, 8)
    reindeer(g, 230, 1640, 0.62, t=c.gt, eye=BLUE, glow=0.3)
    kw = c.on("weeks", 0.3)
    with g.at(790, 840, 0, back_out(kw, 1.7)):                                     # day counter
        g.rc(0, 0, 330, 300, "#FFF4E0", INK, lw=10, r=24)
        g.rc(0, -110, 330, 80, "#FF6B5B", INK, lw=10, r=20)
        n = int(1 + 40 * clamp(c.since("weeks") / 1.2))
        g.text(str(n), 0, 30, 140, INK, stroke=None)
        g.text("DAYS", 0, 120, 52, "#5A5A6A", stroke=None)
    with g.screen():
        g.text("NO SUNRISE", W / 2, 330, 110, PAL["cream"], sw=16, depth=8, sc=pop(c.t, c.w("hides") - 0.1, 0.3), a=c.on("hides", 0.2))


def big_eye(g, c, dil):
    """Front close-up of one reindeer eye; the pupil widens with dil 0..1."""
    g.fill_all("#5A3E2A")
    with g.layer(0.8):
        for i in range(60):
            r = rnd(i + 2).random
            g.line([(r() * W, r() * H), (r() * W + 30, r() * H + 60)], "#6E4E36", 10, a=0.6)
    cx, cy = 540, 980
    g.ellipse(cx, cy, 380, 300, "#3A2A22", INK, lw=12)
    g.ellipse(cx, cy, 330, 260, mix("#7A5A2A", "#1E3A5A", 0.5), INK, lw=8)        # iris
    g.ellipse(cx, cy, 120 + 190 * dil, 50 + 190 * dil, "#05070C", None)           # pupil: slot -> wide
    g.glow(cx, cy, 200 + 120 * dil, BLUE, 0.25 + 0.35 * dil)
    g.ellipse(cx - 120, cy - 120, 50, 30, "#FFFFFF", None, a=0.8)
    g.path(f"M{cx-420} {cy-60} Q{cx} {cy-420} {cx+420} {cy-60}", None, "#2A1C1E", lw=40)   # upper lid
    for i in range(9):
        x = cx - 320 + i * 80
        g.line([(x, cy - 300 + abs(i - 4) * 28), (x - 20, cy - 380 + abs(i - 4) * 28)], INK, 10)


def s_pupil(g, c):
    dil = ease_io(clamp(c.since("wide") / 0.7))
    big_eye(g, c, 0.15 + 0.85 * dil)
    if dil > 0:
        for sd in (-1, 1):
            arrow(g, 540 + sd * 160, 980, 540 + sd * 360, 980, PAL["yellow"], w=24, k=dil)
    with g.screen():
        g.text("WIDE OPEN", W / 2, 1560, 120, PAL["yellow"], sw=18, depth=10, sc=pop(c.t, c.w("wide") - 0.1, 0.3), a=c.on("wide", 0.2))


def s_fluid(g, c):
    k = c.on("drain", 0.35)
    eye_section(g, c, mirror=GOLD, pupil=1.0, fluid=0.4 + 0.6 * clamp(c.t / 1.6), block=k)
    with g.screen():
        g.text("FLUID", W / 2, 360, 120, "#7FC8FF", sw=18, depth=10, sc=pop(c.t, c.w("Fluid") - 0.05, 0.3))


def s_pressure(g, c):
    k = clamp(c.since("Pressure") / 1.2)
    cx, cy, r = eye_section(g, c, mirror=GOLD, pupil=1.0, fluid=1.0, bulge=k, block=1.0)
    for i in range(8):                                                             # pressure arrows pushing outward
        a0 = i * TAU / 8
        arrow(g, cx + (r - 140) * math.cos(a0), cy + (r - 140) * math.sin(a0), cx + (r - 30) * math.cos(a0), cy + (r - 30) * math.sin(a0),
              "#FF6B5B", w=18, k=ease_out(k))
    gauge(g, 860, 420, 150, 0.15 + 0.85 * k, k=c.on("Pressure", 0.3))
    with g.screen():
        g.text("PRESSURE", 330, 420, 96, "#FF6B5B", sw=15, depth=8, sc=pop(c.t, c.w("Pressure") - 0.05, 0.3), a=c.on("Pressure", 0.2))


def fibres(g, c, gap, col=GOLD, refl=None, rk=0.0):
    """Close-up of the mirror layer: rows of fibres; `gap` 1 = loose, 0 = packed tight. refl = colour of the reflected wave."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0B1F36", "#122E4A"))
    cx, cy, R = 540, 1060, 440
    g.circle(cx, cy, R + 30, "#2A3A4E", INK, lw=12)
    with g.clip(circle=(cx, cy, R)):
        g.fill_all("#1A2F48")
        sp = lerp(52, 92, gap)
        for row in range(-8, 9):
            for col_ in range(-8, 9):
                x = cx + col_ * sp + (sp / 2 if row % 2 else 0); y = cy + row * sp * 0.87
                g.circle(x, y, 26, col, INK, lw=5)
                g.circle(x - 8, y - 8, 7, "#FFFFFF", None, a=0.5)
    if refl and rk > 0:                                                            # light wave in (cream), reflected wave out (colour)
        def wave(x0, y0, x1, y1, colr, k, amp=26, n=6):
            pts = []
            for i in range(41):
                u = i / 40 * k
                x, y = lerp(x0, x1, u), lerp(y0, y1, u)
                dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
                pts.append((x - dy / L * amp * math.sin(u * n * TAU / max(k, 1e-3) * k), y + dx / L * amp * math.sin(u * n * TAU)))
            g.line(pts, INK, 22); g.line(pts, colr, 12)
        wave(80, 480, cx - 40, cy - 60, LIGHT, clamp(rk * 2))
        if rk > 0.5:
            wave(cx + 40, cy - 60, 1000, 480, refl, clamp(rk * 2 - 1))


def s_squeeze(g, c):
    k = ease_io(clamp((c.since("squeezes") - 0.35) / 1.5))
    fibres(g, c, 1 - k)
    for sd in (-1, 1):
        arrow(g, 540 + sd * 535, 1060, 540 + sd * 440, 1060, "#FF6B5B", w=40, k=c.on("squeezes", 0.3))
    with g.screen():
        g.text("TINY FIBRES", W / 2, 420, 110, GOLD, sw=16, depth=8, sc=pop(c.t, c.w("fibres") - 0.1, 0.3), a=c.on("fibres", 0.2))


def s_blue(g, c):
    k = c.on("blue", 0.5)
    fibres(g, c, 0.0, col=mix(GOLD, "#7FB8FF", k), refl=BLUE, rk=clamp(c.t / 1.2))
    with g.screen():
        g.text("BLUE", W / 2, 1640, 140, BLUE, sw=20, depth=10, sc=pop(c.t, c.w("blue") - 0.05, 0.3), a=k)


def s_twilight(g, c):
    """'the colour of twilight': the Arctic noon sky in winter is deep blue; a reindeer herd on the ridge."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0E2A54", "#2E5FA0", "#7FA8D8", "#C7B8D8"))
    with g.layer(0.3):
        stars(g, 30, 9, box=(-300, -200, W + 300, 600), t=c.gt)
    g.path("M-300 1350 Q200 1220 540 1300 Q900 1380 1400 1240 L1400 2100 L-300 2100 Z", "#5A7FA8", INK, lw=8)
    for i, (x, s, fl) in enumerate(((190, 0.42, False), (600, 0.5, True), (900, 0.38, False))):
        reindeer(g, x, 1330 + i * 14, s, t=c.gt + i, eye=BLUE, glow=0.5, flip=fl, walk=0.4, seed=i)
    g.rect(-300, 1500, W + 600, 700, g.lgrad(0, 1500, 0, 1920, "#3A5E80", "#22405E"), None)
    with g.screen():
        g.text("TWILIGHT BLUE", W / 2, 420, 110, "#BFE3FF", sw=16, depth=8, sc=pop(c.t, c.w("twilight") - 0.1, 0.3), a=c.on("twilight", 0.2))


def s_escape(g, c):
    """'Less light escapes': the ray goes in, bounces, and only a thin part leaves; most stays to be seen."""
    cx, cy, r = eye_section(g, c, mirror=BLUE, pupil=1.0)
    pts = ray_path(cx, cy, r)
    u = clamp(c.t / 1.1)
    ray(g, pts[:4], u * 2)
    if u > 0.5:
        ray(g, pts[3:], (u - 0.5) * 2, col=BLUE, w=7, a=0.7)
        for i in range(5):
            a0 = -0.6 + i * 0.3
            g.glow(cx + (r - 58) * math.cos(a0), cy + (r - 58) * math.sin(a0), 60, "#BFE3FF", 0.6 * (u - 0.5) * 2)
    with g.screen():
        g.text("LESS ESCAPES", W / 2, 360, 104, BLUE, sw=16, depth=8, sc=pop(c.t, c.w("escapes") - 0.1, 0.3), a=c.on("escapes", 0.2))


def s_loop(g, c):
    """'...so they see more in the dark.' Same framing as frame 1 (loop): torch, herder, glowing blue eyes."""
    encounter(g, c, k_glow=1.0, expr="curious")


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, "blue"), cam=ZOOM(1.0, 1.05, (560, 1080)), sfx=[(0.0, "shimmer", 0.5), (0.0, "sting", 0.3), (0.0, "wind", 0.25)], tr="cut")
V.shot("H1", s_hook_close, ("blue", 1), cam=ZOOM(1.45, 1.6, (FX, FY + 40)), tr="cut", sfx=[("blue", "chime", 0.3)])
V.shot("L01", s_summer, (0, "In#1"), cam=ZOOM(1.0, 1.06, (520, 1200)), sfx=[("gold", "ding", 0.3), (0.0, "birds", 0.15)])
V.shot("L01", s_winter, ("In#1", 1), cam=ZOOM(1.0, 1.08, (600, 1150)), sfx=[("blue", "shimmer", 0.4), (0.0, "wind", 0.25)], tr="drop")
V.shot("L02", s_mirror, (0, "for"), cam=ZOOM(1.0, 1.06, (560, 1000)), sfx=[("mirror", "sparkle", 0.3), ("bounces", "whoosh_soft", 0.3)])
V.shot("L02", s_chance, ("for", 1), cam=ZOOM(1.12, 1.2, (700, 1000)), tr="cut", sfx=[("second", "chime", 0.3)])
V.shot("L03", s_sun, (0, "so"), cam=ZOOM(1.0, 1.05, (540, 1150)), sfx=[("hides", "whoosh_soft", 0.3), ("weeks", "tick", 0.3)])
V.shot("L03", s_pupil, ("so", 1), cam=ZOOM(1.0, 1.1, (540, 980)), sfx=[("wide", "swell", 0.4)])
V.shot("L04", s_fluid, (0, "Pressure"), cam=ZOOM(1.0, 1.06, (560, 1000)), music="tension", sfx=[("Fluid", "bloop", 0.3), ("drain", "alarm", 0.3)])
V.shot("L04", s_pressure, ("Pressure", "squeezes"), cam=ZOOM(1.0, 1.05, (600, 900)), tr="cut", sfx=[("Pressure", "swell", 0.4)])
V.shot("L04", s_squeeze, ("squeezes", 1), cam=ZOOM(1.0, 1.08, (540, 1060)), sfx=[("squeezes", "click", 0.35)])
V.shot("L05", s_blue, (0, "the"), cam=ZOOM(1.0, 1.06, (540, 1000)), music="warm", sfx=[("blue", "shimmer", 0.4)])
V.shot("L05", s_twilight, ("the", "Less"), cam=ZOOM(1.0, 1.06, (540, 1250)), sfx=[("twilight", "chime", 0.3)])
V.shot("L05", s_escape, ("Less", "so"), cam=ZOOM(1.0, 1.06, (560, 1000)), tr="cut", sfx=[("escapes", "whoosh_soft", 0.3)])
V.shot("L05", s_loop, ("so", 1), cam=ZOOM(1.0, 1.05, (560, 1080)), sfx=[("dark", "shimmer", 0.35)])
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
        V.render(str(EP / "final/A-027.mp4"))
