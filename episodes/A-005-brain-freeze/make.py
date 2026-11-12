"""A-005 "What Brain Freeze Does Inside Your Head" — standalone Short, Style F (flat 2D), 1080x1920.
python episodes/A-005-brain-freeze/make.py sheet|render|still <t>
Sets: parlour (Wy with the ice cream), head cutaway (lib/flat_sets.cutaway), lab (scientist + volunteer + monitor).
Voice: Gemini master voice/ch0.flac -> audio/lines (python lib/voice_gemini.py episodes/A-005-brain-freeze).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from flat_cast import Char, WY, coat, stripes, amix
from flat_fx import *
from flat_sets import (parlour, lab, monitor, xray_bg, cutaway, cut_pt, cone, mug, cup_straw, CUT, PALATE_PT, FOREHEAD_PT, BRAIN_PT, ARTERY_PT, MOUTH_PT)

V = Video(EP, title=("WHAT BRAIN FREEZE DOES", "INSIDE YOUR HEAD"),
          keys={"brain", "freeze", "cold", "vessel", "widens", "skull", "pressure", "hurts", "nerve", "forehead", "tongue", "warm", "seconds", "confused", "you"},
          music="curious")
WX, WFY, WS = 590, 1578, 1.5
HEADC = (WX, WFY - 327 * WS)                      # Wy's head centre in the parlour shots
SCI = Char(skin="#F1C9A5", top="#F6F2EA", hair="side", hair_col="#3B2A20", glasses=INK, outfit=[coat()], legs="#2F3A56", seed=2)
VOL = Char(skin="#8D5A3B", top="#FFC93C", hair="curly", hair_col="#2A1C1E", hat="headband", hat_col="#5ED3B5", outfit=[stripes("#FF6B5B")], seed=4, legs="#27536B")


def roi(pt, z0, z1=None, sy=1250, shake=0.0, cut=True, pt1=None):
    """Camera that keeps a point (cutaway units if cut) at screen height sy while zooming z0 -> z1 (optionally travelling to pt1)."""
    p0 = cut_pt(*pt) if cut else pt
    p1 = (cut_pt(*pt1) if cut else pt1) if pt1 else p0
    z1 = z0 if z1 is None else z1

    def cam(c):
        k = ease_io(c.u)
        z = lerp(z0, z1, k)
        x, y, _ = look_at(lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k), z, sy)
        s_ = shake(c) if callable(shake) else shake
        return (x + 4 * wig(c.gt, 0.13, 1) + s_ * 14 * wig(c.gt, 9.0, 3), y + 4 * wig(c.gt, 0.1, 2) + s_ * 14 * wig(c.gt, 8.0, 5), z, 0.0)
    return cam


def frost(k, glow=0.0):
    """head_fx: ice creeping down Wy's head from the top (k 0..1); glow = red throb on the forehead."""
    def f(g):
        rx, ry = WY.head
        if glow > 0:
            g.glow(18, -ry * 0.52, 95, "#FF3B30", 0.8 * glow)
        if k <= 0.01:
            return
        yb = -ry + ry * 0.74 * k
        n = 8
        pts = [(-rx - 12, -ry - 12), (rx + 12, -ry - 12)]
        edge = []
        for i in range(n + 1):
            x = rx + 12 - i * (2 * rx + 24) / n
            edge.append((x, yb + (20 if i % 2 else -6) + 5 * math.sin(i * 1.7)))
        g.poly(pts + edge, "#A8E2FF", None, a=0.95)
        g.line(edge, "#FFFFFF", 6)
        for (fx, fy, fr) in ((-56, -ry * 0.62, 13), (40, -ry * 0.78, 10), (70, -ry * 0.42, 9), (-14, -ry * 0.36, 8)):
            if fy < yb - 8:
                flake(g, fx, fy, fr, "#FFFFFF", 0.3, lw=3.4)
    return f


def ice_crown(g, t, k):
    """Ice spikes popping out of the top of Wy's head."""
    hx, hy = HEADC
    for i, (dx, h_, rot) in enumerate(((-88, 70, -0.5), (-30, 104, -0.16), (36, 92, 0.2), (96, 62, 0.55))):
        kk = pop(k, i * 0.08, 0.3)
        if kk <= 0: continue
        with g.at(hx + dx * WS * 0.9, hy - 96 * WS * (0.97 - 0.08 * abs(dx) / 96), rot, kk):
            g.poly([(-24, 10), (0, -h_ * 1.45), (24, 10)], "#BDEBFF", r=3)
            g.line([(-6, 0), (0, -h_ * 1.0)], "#FFFFFF", 6, a=0.8)


def wy(g, c, expr="pain", arms=("temple", "hold_up"), hold=(None, cone()), fk=1.0, shiver=1.0, glow=0.0, **kw):
    WY.draw(g, c.gt, WX, WFY, sc=WS, face=1, turn=kw.pop("turn", 0.18), expr=expr, arms=arms, hold=hold, shiver=shiver * (fk > 0.05),
            head_fx=frost(fk, glow), tint=("#A9D8F2", 0.3 * fk), **kw)


# ------------------------------------------------------------------ shots


def s_hook(g, c):
    t = c.t
    parlour(g, c.gt)
    k = 0.72 + 0.28 * ease_out(seg(t, c.w("brain") - 0.2, 0.5))
    wy(g, c, fk=k, look=(0.2, -0.1))
    ice_crown(g, t, 1.0 + t)
    pain_marks(g, HEADC[0] - 215, HEADC[1] - 30, 30, t, n=3, col="#8FD8FF", a0=2.6, a1=3.7)
    pain_marks(g, HEADC[0] + 215, HEADC[1] - 60, 30, t, n=3, col="#8FD8FF", a0=-0.6, a1=0.5)
    snow(g, t + 3, (250, 880, 930, 1420), n=16, seed=4, size=(8, 15), speed=55)
    ring_wave(g, HEADC[0], HEADC[1] - 60, 150, 420, seg(t, c.w("freeze"), 0.6), "#BDEBFF", 14)


def s_reveal(g, c):
    xray_bg(g, c.gt)
    cutaway(g, c.gt, cold=0.55, eye="pain", sweat=1)
    px, py = cut_pt(*BRAIN_PT)
    ring_wave(g, px, py, 120, 520, seg(c.t, 0.25, 0.8), "#FFF4E0", 10, a=0.6)


def s_cold(g, c):
    t = c.t
    th = c.w("hits")
    xray_bg(g, c.gt, glow=cut_pt(*MOUTH_PT))
    kin = ease_in(seg(t, c.w("ice") - 0.25, th - c.w("ice") + 0.25))
    hit = t - th
    cold = ease_out(seg(t, th, 1.0))

    def scoop(g):
        sx = lerp(1230, 738, kin) + (10 * math.sin(hit * 18) * math.exp(-hit * 7) if hit > 0 else 0)
        sy = lerp(742, 692, kin)
        sq = 1 - 0.16 * pulse(t, th, 0.35)
        with g.at(sx + 54, sy + 7, -TAU / 4 - 0.12, 1.04 * sq, 1.04 / sq):
            cone(bite=False)(g, t)
        if hit > 0:
            ring_wave(g, 720, 636, 30, 190, seg(hit, 0, 0.5), "#EAF9FF", 12)
            ring_wave(g, 720, 636, 20, 130, seg(hit, 0.12, 0.5), "#BDEBFF", 9)
            for i in range(7):
                a0 = -2.9 + i * 0.36
                d_ = 60 + 190 * ease_out(seg(hit, 0, 0.7))
                flake(g, 720 + d_ * math.cos(a0), 632 + d_ * math.sin(a0) * 0.7, 15, "#EAF9FF", hit * 3 + i, lw=4, a=1 - seg(hit, 0.35, 0.5))
    cutaway(g, c.gt, cold=cold, eye="open" if hit < 0 else ("wide" if hit < 0.35 else "pain"), extra=scoop, sweat=1 if hit > 0.3 else 0)


def s_lab(g, c):
    t = c.t
    lab(g, c.gt)
    kb = ease_io(seg(t, c.w("big") - 0.15, 0.5))
    monitor(g, c.gt, 548, 1118, 420, 290, widen=0.25 * kb)
    # sensor wire from the volunteer's headband to the monitor
    g.limb("M318 1182 C380 1090 330 1010 372 1010", "#5ED3B5", 9, lw=4.5)
    wince = seg(t, 0.75, 0.2)
    VOL.draw(g, c.gt, 205, 1582, sc=1.22, face=1, turn=0.3, expr="cold" if wince > 0.5 else "neutral", arms=("down", "sip"), hold=(None, cup_straw()),
             shiver=1.0 * (wince > 0.5), tint=("#A9D8F2", 0.25 * wince))
    if wince > 0.5:
        pain_marks(g, 205, 1582 - 327 * 1.22 - 150, 26, t, n=3, col="#8FD8FF", a0=-2.2, a1=-0.9, sc=0.9)
    pt = amix("hold", (-150, -330), ease_io(seg(t, c.w("big") - 0.3, 0.4)))
    SCI.draw(g, c.gt, 905, 1586, sc=1.26, face=-1, turn=0.35, expr="surprised" if kb > 0.3 else "think", arms=("hip", pt), look=(0.6, -0.2))
    # highlight ring on the vessel
    if kb > 0:
        g.circle(548, 1090, 150 - 30 * kb, None, PAL["yellow"], lw=10, a=kb * (0.7 + 0.3 * math.sin(c.gt * 9)))


def s_vessel(g, c):
    t = c.t
    xray_bg(g, c.gt, glow=cut_pt(*ARTERY_PT))
    tw = c.w("widens")
    widen = elastic(seg(t, tw - 0.05, 0.9), 2.2, 5.0) if t > tw - 0.05 else 0.0
    flow = ease_io(seg(t, c.w("blood", 1) - 0.15, 0.5))

    def fx(g):
        # the chill rising from the palate to the vessel
        for i in range(3):
            k = (t * 0.9 + i / 3) % 1.0
            if t < tw + 0.3:
                g.line(f"M{640 + i * 30} {596 - 40 * k} q16 -12 32 0 q16 12 32 0", "#BDEBFF", 8, a=0.9 * math.sin(k * math.pi))
        if flow > 0:
            for i in range(5):
                k = (t * 1.6 + i / 5) % 1.0
                px, py, an = path_at("M560 1080 C556 950 474 870 464 780 C456 700 474 636 522 600 C570 566 640 552 680 504 C702 478 708 444 702 414", 0.45 + 0.5 * k)
                with g.at(px, py, an):
                    g.line([(-46, -44), (-16, -44)], "#FFF4E0", 7, a=0.85 * flow * math.sin(k * math.pi))
                    g.line([(-50, 44), (-20, 44)], "#FFF4E0", 7, a=0.85 * flow * math.sin(k * math.pi))
        if t > tw:
            ring_wave(g, 610, 556, 40, 240, seg(t, tw, 0.6), "#FF9C8E", 12)
    cutaway(g, c.gt, cold=1, widen=widen, flow=flow, eye="pain" if t > tw else "wide", extra=fx, brain_tint=0.5 * flow, sweat=1)


def s_box(g, c):
    t = c.t
    xray_bg(g, c.gt)
    cutaway(g, c.gt, cold=1, widen=1, flow=0.35, eye="pain", flash=pulse(t, c.w("skull") - 0.05, 0.45), rivets=seg(t, c.w("closed") - 0.1, 0.9),
            lock=seg(t, c.w("box") - 0.05, 0.3), brain_tint=0.3)
    kx, ky = cut_pt(176, 196)
    burst(g, kx, ky, 60, 150, 8, PAL["yellow"], 9, seg(t, c.w("box"), 0.4))


def s_pressure(g, c):
    t = c.t
    p = ease_io(seg(t, c.w("pressure") - 0.25, 1.25))
    xray_bg(g, c.gt, col=mix("#1B6E86", "#B03A3A", p))
    cutaway(g, c.gt, cold=1, widen=1, flow=0.6, pressure=p, eye="pain", rivets=1, lock=1, sweat=1)
    with g.screen():
        kk = pop(t, 0.05, 0.35)
        gauge(g, 205, 1500, 112, 0.18 + 0.8 * p + 0.03 * math.sin(c.gt * 30) * p, kk)


def s_hurts(g, c):
    t = c.t
    parlour(g, c.gt)
    th = 0.6 + 0.4 * math.sin(TAU * 2.6 * c.gt)
    wy(g, c, arms=("temple", amix("hold_up", "hold", ease_out(seg(t, 0, 0.3)))), fk=1.0, glow=th, sweat=1.0)
    ice_crown(g, t, 9)
    pain_marks(g, HEADC[0] - 20, HEADC[1], 250, c.gt, n=3, col="#FF6B5B", a0=2.75, a1=3.75, sc=1.5)
    pain_marks(g, HEADC[0] + 20, HEADC[1], 250, c.gt + 0.3, n=3, col="#FF6B5B", a0=-0.6, a1=0.35, sc=1.5)
    for i, (dx, dy, r_) in enumerate(((-250, -250, -0.4), (255, -235, 0.35))):
        bolt(g, HEADC[0] + dx, HEADC[1] + dy, 1.5 * pop(t, 0.04 + i * 0.08, 0.25), r_, PAL["yellow"])


def s_nerve(g, c):
    t = c.t
    xray_bg(g, c.gt, glow=cut_pt(722, 520))
    kp = ease_io(seg(t, c.w("nerve") - 0.2, 0.45))
    kb = ease_io(seg(t, c.w("reports") - 0.1, 0.45))
    kf_ = ease_io(seg(t, c.w("also") - 0.1, 0.8))
    fp = ease_out(seg(t, c.w("forehead") - 0.2, 0.45))
    cutaway(g, c.gt, cold=1, widen=1, flow=0.5, pressure=0.55, nerve=(kp, kb, kf_), signal=seg(t, c.w("reports"), 0.3), fpain=fp * 0.9,
            eye="pain", rivets=0, lock=0, arrows=False)


def s_blame(g, c):
    t = c.t
    xray_bg(g, c.gt, glow=cut_pt(*FOREHEAD_PT), col="#8E3B4A")
    arm = seg(t, c.w("blames") - 0.2, 0.3)
    cutaway(g, c.gt, cold=1, widen=1, flow=0.5, pressure=0.4, nerve=(1, 1, 1), signal=1, fpain=1, eye="up", rivets=0, brain_face="blame", brain_arm=arm, arrows=False)
    fx, fy = cut_pt(FOREHEAD_PT[0] + 150, FOREHEAD_PT[1] - 150)
    qmark(g, fx, fy, 150, PAL["yellow"], 0.2, pop(t, c.w("forehead") - 0.1, 0.3), "!")


def s_tongue(g, c):
    t = c.t
    xray_bg(g, c.gt, glow=cut_pt(*MOUTH_PT), col=mix("#1B6E86", "#B5702A", ease_io(seg(t, c.w("roof") - 0.2, 0.8))))
    tg = ease_io(seg(t, c.w("tongue") - 0.25, 0.5))
    warm = ease_io(seg(t, c.w("roof") - 0.25, 0.9))

    def fx(g):
        if warm > 0.05:
            for i in range(4):
                k = (t * 0.8 + i / 4) % 1.0
                g.path(f"M{600 + i * 52} {660 + 70 * k} q-9 14 0 21 q9 -7 0 -21 Z", "#8FD8FF", INK, lw=3.5, a=(1 - k) * warm)
            for i in range(3):
                k = (t * 0.7 + i / 3) % 1.0
                g.line(f"M{640 + i * 44} {600 - 46 * k} q14 -12 0 -26 q-14 -12 0 -26", "#FFB060", 8, a=0.9 * warm * math.sin(k * math.pi))
    cutaway(g, c.gt, cold=1 - warm, widen=1 - 0.6 * warm, flow=0.3, pressure=0.4 * (1 - warm), tongue=tg, warm=warm, eye="pain" if warm < 0.6 else "open",
            rivets=0, extra=fx, nerve=None)


def s_sip(g, c):
    t = c.t
    parlour(g, c.gt)
    fk = lerp(0.85, 0.5, ease_io(c.u))
    tilt = -0.42 * ease_io(seg(t, 0.1, 0.4))
    wy(g, c, expr="relief", arms=("down", amix("hold", "sip", ease_out(seg(t, 0.0, 0.3)))), hold=(None, (mug(), tilt)), fk=fk, shiver=0.3, mouth="flat")
    ice_crown(g, t, 9)
    hx, hy = WX + 62 * WS, WFY - 262 * WS
    g.rings(hx + 10, hy - 60, 210, "#FFB060", a=0.075, n=3)
    steam(g, c.gt, hx + 6, hy - 150, n=3, h=150, a=0.6)


def s_fades(g, c):
    t = c.t
    parlour(g, c.gt)
    fk = 0.5 * (1 - ease_io(seg(t, c.w("fades") - 0.3, 0.9)))
    done = seg(t, c.w("fades") + 0.5, 0.3)
    wy(g, c, expr="joy" if done > 0.5 else "relief", arms=("down", "hold"), hold=(None, mug()), fk=fk, shiver=0, lift=26 * pulse(t, c.w("seconds") - 0.1, 0.4),
       sq=1 + 0.05 * pulse(t, c.w("seconds") - 0.1, 0.4))
    if fk > 0.02:
        ice_crown(g, t, 9)
        for i in range(5):
            k = (t * 1.1 + i / 5) % 1.0
            x = HEADC[0] - 130 + i * 62
            g.path(f"M{x} {HEADC[1] - 60 + 230 * k} q-11 17 0 26 q11 -9 0 -26 Z", "#8FD8FF", INK, lw=4, a=(1 - k) * min(1, fk * 4))
    sparkles(g, t, [(HEADC[0] - 250, HEADC[1] - 170), (HEADC[0] + 255, HEADC[1] - 120), (HEADC[0] + 190, HEADC[1] - 290), (HEADC[0] - 190, HEADC[1] + 60)],
             r=46 * done, period=0.8)
    steam(g, c.gt, WX + 116 * WS, WFY - 236 * WS - 120, n=2, h=110, a=0.45)


def s_notfrozen(g, c):
    t = c.t
    xray_bg(g, c.gt, col="#1F8A6E")
    cutaway(g, c.gt, warm=0.25, eye="happy", brain_face="happy")
    with g.screen():
        kk = pop(t, c.w("isn't") - 0.15, 0.3)
        if kk > 0:
            with g.at(215, 1500, -0.12, kk):
                g.rect(-74, -74, 148, 148, "#BDEBFF", r=26)
                g.line([(-44, -40), (-10, -52)], "#FFFFFF", 12, a=0.9); g.line([(-48, -8), (-34, -14)], "#FFFFFF", 10, a=0.9)
                flake(g, 16, 18, 30, "#FFFFFF", 0.2, lw=6)
        no_sign(g, 215, 1500, 118, pop(t, c.w("frozen") - 0.1, 0.3, 2.4))


def s_confused(g, c):
    t = c.t
    xray_bg(g, c.gt, col="#6A4FA0")
    cutaway(g, c.gt, warm=0.25, eye="up", brain_face="dizzy")
    for i, (x, y, r_) in enumerate(((250, 110, -0.3), (470, 20, 0.1), (690, 100, 0.35))):
        px, py = cut_pt(x, y)
        qmark(g, px, py + 12 * math.sin(c.gt * 5 + i), 120, PAL["yellow"], r_ + 0.12 * math.sin(c.gt * 4 + i), pop(t, 0.05 + i * 0.1, 0.3))


def s_you(g, c):
    t = c.t
    parlour(g, c.gt)
    wy(g, c, expr="smug", arms=("hip", amix("hold", "reach", ease_out(seg(t, 0.05, 0.35)))), hold=(None, cone()), fk=0, shiver=0, turn=0.1,
       lean=0.05 * ease_out(seg(t, 0.05, 0.35)), look=(0.2, 0.1))
    qmark(g, HEADC[0] - 255, HEADC[1] - 150, 190, PAL["yellow"], -0.25, pop(t, c.w("you") - 0.15, 0.3))


WYCAM = lambda z0, z1, shake=0.0: roi((WX, HEADC[1] + 90), z0, z1, sy=1170, shake=shake, cut=False)
V.shot("H1", s_hook, part=(0, "inside"), cam=WYCAM(1.0, 1.1), sfx=[(0.0, "freeze", 0.6), (0.0, "whoosh_soft", 0.35), ("freeze", "sparkle", 0.3)], music="curious", tr="cut")
V.shot("H1", s_reveal, part=("inside", 1), cam=roi(BRAIN_PT, 0.98, 1.06, sy=1140), sfx=[(0.0, "whoosh", 0.5), (0.3, "bloop", 0.35)], tr=("iris", (WX, HEADC[1] - 20), 0.55))
V.shot("L01", s_cold, cam=roi((720, 660), 1.5, 1.72, sy=1280), sfx=[("ice", "whoosh_soft", 0.4), ("hits", "thud", 0.5), (("hits", 0.04), "freeze", 0.6)])
V.shot("L02", s_lab, part=(0, "suddenly"), cam=roi((548, 1150), 1.0, 1.16, sy=1180, cut=False), sfx=[(0.0, "pop", 0.35), (0.7, "boing", 0.25), ("big", "bloop", 0.4)])
V.shot("L02", s_vessel, part=("suddenly", 1), cam=roi(ARTERY_PT, 1.5, 1.68, sy=1290), sfx=[(0.0, "whoosh_soft", 0.3), ("widens", "swell", 0.7), ("blood#1", "rush", 0.55)])
V.shot("L03", s_box, part=(0, "so"), cam=roi(BRAIN_PT, 1.04, 1.1, sy=1150), sfx=[("skull", "thud", 0.45), ("closed", "tick", 0.4), (("closed", 0.14), "tick", 0.4),
                                                                              (("closed", 0.28), "tick", 0.4), ("box", "click", 0.6)])
V.shot("L03", s_pressure, part=("so", "and"), cam=roi(BRAIN_PT, 1.1, 1.24, sy=1160, shake=lambda c: 0.8 * ease_io(seg(c.t, 0.4, 1.0))),
       sfx=[(0.0, "riser", 0.4), ("pressure", "heartbeat", 0.6)], music="tension")
V.shot("L03", s_hurts, part=("and", 1), cam=WYCAM(1.16, 1.24, shake=0.9), sfx=[(0.0, "sting", 0.55), (0.02, "boing", 0.3)], tr="flash")
V.shot("L04", s_nerve, cam=roi((700, 560), 1.5, 1.42, sy=1300, pt1=(760, 400)), sfx=[("nerve", "zap", 0.45), ("reports", "bloop", 0.3), ("also", "zap", 0.45), ("forehead", "sting", 0.3)])
V.shot("L05", s_blame, cam=roi((700, 300), 1.42, 1.56, sy=1200), sfx=[(0.0, "pop", 0.35), ("blames", "hmm", 0.5)])
V.shot("L06", s_tongue, part=(0, "or"), cam=roi((690, 680), 1.6, 1.78, sy=1280), sfx=[("tongue", "pop", 0.4), ("roof", "melt", 0.45)], music="warm")
V.shot("L06", s_sip, part=("or", "and"), cam=WYCAM(1.12, 1.2), sfx=[(0.05, "drink", 0.5)])
V.shot("L06", s_fades, part=("and", 1), cam=WYCAM(1.2, 1.08), sfx=[("fades", "melt", 0.5), ("seconds", "sparkle", 0.4)])
V.shot("L07", s_notfrozen, part=(0, "Just"), cam=roi(BRAIN_PT, 1.2, 1.3, sy=1170), sfx=[("isn't", "pop", 0.4), ("frozen", "click", 0.45)], music="playful")
V.shot("L07", s_confused, part=("Just", "Does"), cam=roi(BRAIN_PT, 1.3, 1.38, sy=1190), sfx=[(0.0, "confuse", 0.55)])
V.shot("L07", s_you, part=("Does", 1), cam=WYCAM(1.1, 1.2), sfx=[(0.0, "whoosh_soft", 0.35), ("you", "hmm", 0.45)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(EP / "animatic/sheet.jpg", per_shot=int(sys.argv[2]) if len(sys.argv) > 2 else 2, cols=8, scale=0.22))
    elif cmd == "still":
        print(V.still(float(sys.argv[2]), EP / f"animatic/still_{sys.argv[2]}.jpg", scale=float(sys.argv[3]) if len(sys.argv) > 3 else 0.5))
    elif cmd == "big":
        print(V.sheet(EP / "animatic/big.jpg", times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.45))
    elif cmd == "render":
        V.render(EP / "final/A-005.mp4")
        measure(EP / "final/A-005.mp4")
    for sh in V.shots:
        print(sh["id"], sh["line"], round(sh["start"], 2), round(sh["dur"], 2))
    print("duration", V.duration)
