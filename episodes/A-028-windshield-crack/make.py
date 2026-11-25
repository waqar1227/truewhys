"""A-028 "Why Hot Water Can Crack a Frozen Windshield" — standalone Short, Style F + cast v2.2 (Mira, new winter look). Slot Sat 28 Nov 2026 18:00 UTC (owner one-time exception).
python episodes/A-028-windshield-crack/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: suburban driveway before sunrise, a generic yellow hatchback (no brand), kettle, ice sheet, cracks,
a glass cross-section (outer layer heats + swells, inside stays frozen = thermal shock), a chip that gathers stress, and the safe fixes
(scraper, de-icer spray, defroster from inside the car). Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import burst, no_sign, arrow, steam, sparkles, sparkle, pain_marks, qmark
from flat_winter import hand_pt, scarf
from flat_car import (driveway_dawn, car_front, ws_path, ws_at, crack_paths, draw_cracks, kettle, spout_pt, scraper, spray_bottle,
                      earmuffs, glass_slab, dashboard, ice_layer)

V = Video(EP, title=("WHY DID IT", "CRACK?"), music="tension")
V.title_y = 0.075
HOT, ICEB, STRESS = "#FF8A3D", "#9FD8F5", "#FF4B4B"
WHO = "mira"
CXC, CYC, CS = 650, 1640, 1.0             # car: wheels on the ground at (CXC, CYC)
MX, MY, MH = 225, 1850, 1000              # Mira feet + height
POUR = ("point", "up", 0.85)               # raised right arm holding the kettle over the glass
SPLASH_UV = (0.6, 0.5)                  # where the hot water hits the windshield
CHIP_UV = (0.70, 0.30)
# crack networks in car units (drawn inside the windshield clip), origin = impact point / chip
import flat_car
_imp = flat_car._ws_local(*SPLASH_UV)
CR_HIT = crack_paths(_imp[0], _imp[1], seed=4, n=7, L=330, branch=2)
_chp = flat_car._ws_local(*CHIP_UV)
CR_CHIP = crack_paths(_chp[0], _chp[1], seed=9, n=3, L=520, branch=1)


def mira(g, c, expr, pl, pr, x=MX, y=MY, h=MH, props=False):
    char2(g, WHO, x, y, h, expr, pl, pr, t=c.gt, view="3q", prop=props)
    scarf(g, x, y, h, col="#FF6B5B", stripe="#FFF4E0", t=c.gt)


def stream(g, x0, y0, x1, y1, k, t):
    """Hot water stream from the spout to the glass (arc), with steam."""
    if k <= 0: return
    pts = [(lerp(x0, x1, u) + 30 * math.sin(u * 3.1), lerp(y0, y1, u * u)) for u in [i / 10 * k for i in range(11)]]
    g.line(pts, "#BFE8FF", 22, a=0.9); g.line(pts, "#FFFFFF", 7, a=0.7)
    steam(g, t, x1, y1 - 30, n=4, h=160, col="#FFFFFF", a=0.55, w=11, spread=50)


# ------------------------------------------------------------------ hook / loop framing
def driveway_scene(g, c, ice=1.0, slide=0.0, melt=None, cracks=None, chip=None, lights=1.0):
    driveway_dawn(g, c.gt)
    car_front(g, CXC, CYC, CS, ice=ice, slide=slide, melt=melt, cracks=cracks, chip=chip, lights=lights)


def s_hook(g, c):
    """Frame 1: kettle mid-pour on the iced windshield, a crack already bursting out from the splash, Mira shocked."""
    k = seg(c.gt, 0.0, 1.3)
    driveway_scene(g, c, melt=(*SPLASH_UV, 34 + 20 * k), cracks=[(CR_HIT, 0.25 + 0.75 * ease_out(k))])
    hx, hy = hand_pt(WHO, POUR, MX, MY, MH)
    tilt = 0.55
    sx, sy = spout_pt(hx, hy, tilt)
    ix, iy = ws_at(CXC, CYC, CS, *SPLASH_UV)
    stream(g, sx, sy, ix, iy, 1.0, c.gt)
    burst(g, ix, iy, 40, 150, 10, "#FFFFFF", 8, k=seg(c.gt, 0.0, 0.4))
    mira(g, c, "shocked", pose_at(c.t, [(0, "shrug"), (0.8, "up")]), POUR)
    kettle(g, hx, hy, tilt, 1.0, c.gt)
    pain_marks(g, ix + 10, iy - 40, 120, c.gt, n=5, col="#FFFFFF", a0=-2.8, a1=-0.3, sc=0.8)


def s_hook_close(g, c):
    k = seg(c.gt, 0.0, 1.3)
    driveway_scene(g, c, melt=(*SPLASH_UV, 34 + 20 * k), cracks=[(CR_HIT, 0.25 + 0.75 * ease_out(k))])
    hx, hy = hand_pt(WHO, POUR, MX, MY, MH)
    sx, sy = spout_pt(hx, hy, 0.55)
    ix, iy = ws_at(CXC, CYC, CS, *SPLASH_UV)
    stream(g, sx, sy, ix, iy, 1.0 - c.on("windshield", 0.3), c.gt)
    mira(g, c, "shocked", "up", POUR)
    kettle(g, hx, hy, 0.55 - 0.4 * c.on("windshield", 0.3), 1.0, c.gt)


# ------------------------------------------------------------------ L01: one splash
def s_splash(g, c):
    """Close on the iced glass: the kettle tips, hot water splashes, a clear melt hole spreads; on 'split' a crack races across."""
    k_pour = c.on("splash", 0.3)
    k_crack = clamp(c.since("split") / 0.7) if c.t >= c.w("split") else 0.0
    driveway_scene(g, c, melt=(*SPLASH_UV, 10 + 50 * clamp(c.since("splash") / 1.2)) if k_pour > 0 else None,
                   cracks=[(CR_HIT, ease_out(k_crack))])
    ix, iy = ws_at(CXC, CYC, CS, *SPLASH_UV)
    kx, ky = ix - 230, iy - 260
    tilt = 0.2 + 0.45 * k_pour
    sx, sy = spout_pt(kx, ky, tilt, 0.9)
    stream(g, sx, sy, ix, iy, k_pour, c.gt)
    kettle(g, kx, ky, tilt, 0.9, c.gt)
    if k_pour > 0:
        R = rnd(int(c.gt * 12)).random
        for i in range(8):
            a = -math.pi * R(); d = 30 + 70 * R()
            g.circle(ix + d * math.cos(a), iy + d * math.sin(a) * 0.6, 5 + 5 * R(), "#E8FBFF", INK, lw=2, a=0.8)
    if k_crack > 0:
        burst(g, ix, iy, 30, 170, 12, "#FFFFFF", 8, k=seg(c.t, c.w("split"), 0.35))


# ------------------------------------------------------------------ L02/L03: the glass cross-section
SX0, SX1, SY0, SY1 = 90, 990, 880, 1200


def slab_bg(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#1C2A55", "#2E3F78", "#1C2A55"))
    g.rect(-200, SY1 + 10, W + 400, H, "#141C3A", None, a=0.6)
    with g.screen():                                                                # callout: this is the windshield glass, cut open
        car_front(g, 880, 1720, 0.3, ice=0.6, lights=0.5, roof_snow=True, wipers=False)
        wx, wy = ws_at(880, 1720, 0.3, 0.5, 0.5)
        g.circle(wx, wy, 46, None, PAL["yellow"], lw=8)


def drops(g, t, k):
    for i in range(6):
        u = (t * 1.3 + i / 6) % 1
        x = SX0 + 120 + i * 140
        g.ellipse(x, lerp(300, SY0 - 20, u), 14, 22, "#BFE8FF", INK, lw=4, a=k * (1 - u * 0.3))
    steam(g, t, 540, SY0 - 40, n=5, h=200, col="#FFFFFF", a=0.4 * k, w=12, spread=300)


def s_slow(g, c):
    """'Glass is slow to move heat': hot water sits on top, heat dots crawl into the glass very slowly."""
    slab_bg(g, c)
    kettle(g, 250, 330, 0.7, 1.1, c.gt)
    sx, sy = spout_pt(250, 330, 0.7, 1.1)
    g.line([(sx, sy), (sx + 30, sy + 150), (sx + 40, SY0 - 10)], "#BFE8FF", 22, a=0.9)
    glass_slab(g, SX0, SX1, SY0, SY1, hot=0.15 * clamp(c.t / 2), frost=1.0, t=c.gt)
    drops(g, c.gt, 1.0)
    for i in range(10):
        x = SX0 + 60 + i * 88
        d = 10 + 40 * clamp(c.t / 2.0) + 6 * math.sin(c.gt * 3 + i)
        g.circle(x, SY0 + d, 12, HOT, INK, lw=4)
    with g.screen():
        g.text("SLOW", W / 2, 1460, 120, HOT, sw=16, depth=8, sc=pop(c.t, c.w("slow") - 0.08, 0.3), a=c.on("slow", 0.2))
        g.text("GLASS", W / 2, 700, 84, ICEB, sw=13, a=1 - c.on("slow", 0.3) * 0.0)


def s_swell(g, c):
    """'the outer layer warms and swells in a second': top band turns hot and widens; arrows push outwards."""
    slab_bg(g, c)
    hot = c.on("warms", 0.4); sw = c.on("swells", 0.4)
    glass_slab(g, SX0, SX1, SY0, SY1, hot=hot, swell=sw, frost=1.0, t=c.gt)
    drops(g, c.gt, 0.6)
    for sgn in (-1, 1):
        x0 = 540 + sgn * 330
        arrow(g, x0, SY0 + 40, x0 + sgn * (90 + 20 * math.sin(c.gt * 8)), SY0 + 40, HOT, w=24, k=sw)
    with g.screen():
        g.text("HOT", W / 2, 720, 120, HOT, sw=16, depth=8, sc=pop(c.t, c.w("warms") - 0.08, 0.3), a=hot)


def s_frozen(g, c):
    slab_bg(g, c)
    glass_slab(g, SX0, SX1, SY0, SY1, hot=1.0, swell=1.0, frost=1.0, t=c.gt)
    sparkles(g, c.t, [(250, 1130), (520, 1150), (780, 1120), (900, 1160)], seed=5, col="#FFFFFF", r=30, t0=c.w("frozen") - c.w("while"))
    with g.screen():
        g.text("FROZEN", W / 2, 1420, 120, "#FFFFFF", sw=16, depth=8, sc=pop(c.t, c.w("frozen") - 0.08, 0.3), a=c.on("frozen", 0.2))


def s_stretch(g, c):
    """'One side stretching, the other side not': top arrows pull, bottom holds; the slab bows."""
    slab_bg(g, c)
    bend = 0.6 * c.on("not", 0.5)
    glass_slab(g, SX0, SX1, SY0, SY1, hot=1.0, swell=1.0 + 0.2 * math.sin(c.gt * 6), bend=bend, frost=1.0, t=c.gt)
    k1 = c.on("stretching", 0.3); k2 = c.on("other", 0.3)
    for sgn in (-1, 1):
        x0 = 540 + sgn * 380
        arrow(g, x0, SY0 - 70 - bend * 60, x0 + sgn * (120 + 25 * math.sin(c.gt * 9)), SY0 - 70 - bend * 60, HOT, w=28, k=k1)
    for x in (330, 750):                                                            # the frozen side refuses: small lock bars
        with g.at(x, SY1 + 90, 0, back_out(k2, 1.8)):
            g.rc(0, 0, 150, 34, ICEB, INK, lw=6, r=14)
            g.line([(-40, -40), (40, 40)], STRESS, 12); g.line([(-40, 40), (40, -40)], STRESS, 12)


def s_shock(g, c):
    """'That pull is called thermal shock': stress zig-zags glow where the warm and cold glass meet; a crack starts."""
    slab_bg(g, c)
    glass_slab(g, SX0, SX1, SY0, SY1, hot=1.0, swell=1.0, bend=0.6, frost=1.0, t=c.gt)
    k = c.on("pull", 0.3)
    yh = lerp(SY0, SY1, 0.25)
    for j in range(7):
        x = SX0 + 70 + j * 130
        yy = yh - 0.6 * 60 * math.sin(math.pi * (x - SX0) / (SX1 - SX0))
        a = k * (0.6 + 0.4 * math.sin(c.gt * 14 + j))
        g.path(f"M{x-40} {yy} l20 -24 l20 48 l20 -48 l20 48 l20 -24", None, STRESS, lw=10, a=a)
        g.glow(x + 20, yy, 70, STRESS, 0.3 * a)
    kc = clamp(c.since("shock") / 0.6) if c.t >= c.w("shock") else 0
    if kc > 0:
        cx = 540; cy = SY1 - 4
        g.line([(cx, cy), (cx - 20, cy - 60 * kc), (cx + 15, cy - 130 * kc), (cx - 10, cy - 200 * kc)], INK, 12)
        g.line([(cx, cy), (cx - 20, cy - 60 * kc), (cx + 15, cy - 130 * kc), (cx - 10, cy - 200 * kc)], "#FFFFFF", 6)
    with g.screen():
        g.text("THERMAL", W / 2, 560, 132, HOT, sw=18, depth=10, sc=pop(c.t, c.w("thermal") - 0.08, 0.3), a=c.on("thermal", 0.15))
        g.text("SHOCK", W / 2, 700, 150, "#FFFFFF", sw=20, depth=11, sc=pop(c.t, c.w("shock") - 0.08, 0.32), a=c.on("shock", 0.15))


# ------------------------------------------------------------------ L04: the chip
def s_chip(g, c):
    """Close on a clear windshield with a tiny chip; a magnifier ring circles it; stress arrows gather into it."""
    driveway_scene(g, c, ice=0.0, chip=CHIP_UV)
    px, py = ws_at(CXC, CYC, CS, *CHIP_UV)
    kr = c.on("chip", 0.35)
    g.circle(px, py, 70 * back_out(kr, 1.6), None, PAL["yellow"], lw=10)
    g.line([(px + 50, py + 50), (px + 50 + 70 * kr, py + 50 + 70 * kr)], PAL["yellow"], 16)
    if c.t >= c.w("stress") - 0.05:
        ks = c.on("stress", 0.3)
        for i in range(8):
            a = i * math.pi / 4 + 0.2
            r0 = 300 - 60 * ((c.gt * 1.6 + i * 0.1) % 1)
            arrow(g, px + r0 * math.cos(a), py + r0 * math.sin(a) * 0.7, px + 95 * math.cos(a), py + 95 * math.sin(a) * 0.7, STRESS, w=16, k=ks)
        g.glow(px, py, 120, STRESS, 0.5 * ks * (0.7 + 0.3 * math.sin(c.gt * 12)))
    with g.screen():
        g.text("CHIP", W / 2, 520, 128, PAL["yellow"], sw=17, depth=9, sc=pop(c.t, c.w("chip") - 0.08, 0.3), a=kr)


def s_race(g, c):
    """'a crack can race across the glass': wide shot, the crack runs from the chip across the windshield; Mira's hands fly up."""
    kc = clamp(c.since("crack") / 0.9) if c.t >= c.w("crack") - 0.05 else 0.0
    driveway_scene(g, c, ice=0.0, chip=CHIP_UV, cracks=[(CR_CHIP, ease_in(kc) * 0.6 + 0.4 * kc)])
    mira(g, c, "shocked" if kc > 0.05 else "worried", pose_at(c.t, [(0, "down"), (c.w("crack"), "up")]),
         pose_at(c.t, [(0, "hold"), (c.w("crack"), "up")]), x=MX + 40)


# ------------------------------------------------------------------ L05: the safe way
def s_skip(g, c):
    """'So skip the kettle.' Mira lowers the kettle; a big no-sign stamps over it."""
    driveway_scene(g, c, ice=1.0)
    k = c.on("skip", 0.4)
    mira(g, c, "deadpan", "hip", pose_at(c.t, [(0, "down"), (c.w("skip") - 0.2, "point")]), x=MX + 40)
    kx, ky = MX + 330, MY - 110
    kettle(g, kx, ky, 0.0, 0.9, c.gt)
    no_sign(g, kx + 90, ky - 10, 140, k=k)


def s_scrape(g, c):
    """'Scrape it': close on the iced glass, a scraper sweeps clean stripes."""
    driveway_dawn(g, c.gt)
    car_front(g, CXC, CYC, CS, ice=1.0)
    u = clamp(c.t / max(0.6, c.sh["dur"] - 0.1))
    with g.clip(d=ws_path(CXC, CYC, CS)):
        for j in range(3):
            uj = clamp(u * 3 - j)
            if uj <= 0: continue
            v0 = 0.12 + j * 0.3
            a = ws_at(CXC, CYC, CS, 0.02, v0); b = ws_at(CXC, CYC, CS, 0.02 + 0.96 * uj, v0)
            g.line([a, b], "#3C5B8C", 70)
            g.line([a, b], "#FFFFFF", 3, a=0.4)
    j = min(2, int(u * 3)); uj = clamp(u * 3 - j)
    p = ws_at(CXC, CYC, CS, 0.02 + 0.96 * uj, 0.12 + j * 0.3)
    scraper(g, p[0], p[1], 0.0, 0.9)
    R = rnd(int(c.gt * 10)).random
    for i in range(6):
        g.circle(p[0] - 20 - R() * 60, p[1] + 20 + R() * 60, 5 + 4 * R(), "#FFFFFF", INK, lw=2, a=0.9)


def s_spray(g, c):
    """'spray de-icer': the bottle mists the glass, round patches of ice melt away."""
    driveway_dawn(g, c.gt)
    k = clamp(c.since("spray") / 0.9)
    car_front(g, CXC, CYC, CS, ice=1.0, melt=(0.55, 0.5, 40 + 120 * k))
    bx, by = ws_at(CXC, CYC, CS, 0.98, 0.45)
    spray_bottle(g, bx + 40, by + 150, 0.0, 1.0, c.gt, spraying=c.on("spray", 0.2))


def s_defrost(g, c):
    """'or let the defroster warm it slowly...': from inside the car, warm air rises from the vents and the ice clears from the bottom up."""
    driveway_dawn(g, c.gt)
    k = clamp(c.u * 1.15)
    edge = lerp(1380, 820, ease_io(k))
    g.poly([(-100, -100), (W + 100, -100), (W + 100, edge), (-100, edge)], "#DDF1FF", None, a=0.92)
    R = rnd(12).random
    for i in range(18):
        x, y = R() * W, R() * 900
        if y < edge - 30:
            sparkle(g, x, y, 14 + 10 * R(), "#FFFFFF", a=0.8)
    g.path(f"M-100 {edge} Q540 {edge-40} {W+100} {edge}", None, "#FFFFFF", lw=10, a=0.7)
    g.poly([(-100, -100), (W + 100, -100), (W + 100, 120), (-100, 120)], "#22263A", INK, lw=10)       # roof liner
    g.poly([(-100, 100), (90, 100), (-20, 1500), (-100, 1500)], "#22263A", INK, lw=10)                # A-pillars
    g.poly([(W + 100, 100), (W - 90, 100), (W + 20, 1500), (W + 100, 1500)], "#22263A", INK, lw=10)
    g.rect(470, 120, 140, 70, "#3A3F55", INK, lw=6, r=12)                                           # rear-view mirror
    dashboard(g, c.gt, warm=c.on("defroster", 0.4))
    with g.screen():
        g.text("SLOWLY", W / 2, 1580, 104, HOT, sw=15, depth=8, sc=pop(c.t, c.w("slowly") - 0.08, 0.3), a=c.on("slowly", 0.2))


def s_slide(g, c):
    """'...and the ice slides right off.' Same framing as frame 1 (loop): the loosened ice sheet slides off; Mira, scraper in hand, relaxed."""
    k = c.on("slides", 0.9)
    driveway_scene(g, c, ice=1.0 - 0.2 * k, slide=ease_in(k))
    hx, hy = hand_pt(WHO, POUR, MX, MY, MH)
    mira(g, c, "smug" if k > 0.3 else "curious", pose_at(c.t, [(0, "shrug"), (c.w("slides"), "hip")]), POUR)
    scraper(g, hx + 10, hy, -0.4, 0.8)
    if k > 0:
        sparkles(g, c.t, [ws_at(CXC, CYC, CS, 0.2, 0.7), ws_at(CXC, CYC, CS, 0.75, 0.5), ws_at(CXC, CYC, CS, 0.5, 0.85)],
                 seed=8, col="#FFFFFF", r=30, t0=c.w("slides"))


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
WSC = ws_at(CXC, CYC, CS, 0.5, 0.5)
V.shot("H1", s_hook, (0, "frozen"), cam=ZOOM(1.0, 1.04, (560, 1150)), sfx=[(0.0, "glass_crack", 0.6), (0.0, "pour", 0.35), (0.02, "sting", 0.3)], tr="cut")
V.shot("H1", s_hook_close, ("frozen", 1), cam=ZOOM(1.55, 1.65, (600, 1080)), tr="cut", sfx=[(0.05, "glass_crack", 0.35)])
V.shot("L01", s_splash, (0, "and"), cam=ZOOM(1.7, 1.78, (560, 1040)), sfx=[("splash", "pour", 0.45)])
V.shot("L01", s_splash, ("and", 1), cam=ZOOM(1.45, 1.4, WSC), tr="cut", sfx=[("split", "glass_crack", 0.6)])
V.shot("L02", s_slow, (0, "So"), cam=ZOOM(1.0, 1.06, (540, 1040)), sfx=[(0.05, "whoosh", 0.25), ("slow", "tick", 0.3)])
V.shot("L02", s_swell, ("So", "while"), cam=ZOOM(1.12, 1.2, (540, 980)), tr="cut", sfx=[("warms", "swell", 0.35), ("swells", "pop", 0.3)])
V.shot("L02", s_frozen, ("while", 1), cam=ZOOM(1.35, 1.42, (540, 1180)), tr="cut", sfx=[("frozen", "freeze", 0.4)])
V.shot("L03", s_stretch, (0, "That"), cam=ZOOM(1.0, 1.05, (540, 1000)), sfx=[("stretching", "whoosh", 0.3), ("not", "thud", 0.35)])
V.shot("L03", s_shock, ("That", 1), cam=ZOOM(1.0, 1.1, (540, 920)), tr="cut", sfx=[("thermal", "zap", 0.3), ("shock", "glass_crack", 0.4)])
V.shot("L04", s_chip, (0, "and"), cam=ZOOM(2.1, 2.25, ws_at(CXC, CYC, CS, *CHIP_UV)), sfx=[("chip", "pop", 0.3), ("stress", "heartbeat", 0.35)])
V.shot("L04", s_race, ("and", 1), cam=ZOOM(1.08, 1.14, (620, 1180)), tr="cut", sfx=[("crack", "glass_crack", 0.65)])
V.shot("L05", s_skip, (0, "Scrape"), cam=ZOOM(1.2, 1.25, (420, 1250)), music="warm", sfx=[("skip", "click", 0.4)])
V.shot("L05", s_scrape, ("Scrape", "spray"), cam=ZOOM(1.6, 1.66, WSC), tr="cut", sfx=[("Scrape", "scrape", 0.45)])
V.shot("L05", s_spray, ("spray", "or"), cam=ZOOM(1.4, 1.45, (660, 1130)), tr="cut", sfx=[("spray", "hiss", 0.4)])
V.shot("L05", s_defrost, ("or", "and"), cam=ZOOM(1.0, 1.04, (540, 960)), tr="cut", sfx=[("defroster", "swell", 0.3)])
V.shot("L05", s_slide, ("and", 1), cam=ZOOM(1.0, 1.04, (560, 1150)), tr="cut", sfx=[("slides", "whoosh", 0.35), ("off", "sparkle", 0.35)])
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
        V.render(str(EP / "final/A-028.mp4"))
