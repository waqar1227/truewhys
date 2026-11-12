"""Style F reusable sets and props (design space 1080x1920, floor line near y=1480, main action in the lower 55 %).
Sets: parlour (ice-cream shop), lab (science lab with monitor), xray_bg (dark diagram backdrop).
Diagram: head cutaway (Wy's head in profile: skull, brain, mouth, artery, nerve) with animatable state.
Props for hands: cone(), mug(), cup_straw().
"""
import math
from flat2d import (G, INK, PAL, TAU, W, H, rgba, mix, shade, clamp, lerp, seg, ease_out, ease_in, ease_io, back_out, pop, pulse, wig, rnd,
                    path_at, path_part, path_len)
from flat_fx import tiles, room, lamp, flake, sparkle, bolt, arrow, ring_wave, steam

# ------------------------------------------------------------------ props (origin = the hand)


def cone(bite=True, scoop="#FFB8C8", top=None):
    def f(g, t):
        g.poly([(-31, -8), (31, -8), (0, 96)], "#E8B060", r=5)
        with g.clip(d="M-31 -8 L31 -8 L0 96 Z"):
            for i in range(-3, 4):
                g.line([(i * 16 - 30, -10), (i * 16 + 30, 100)], "#C98A3C", 3.4); g.line([(i * 16 + 30, -10), (i * 16 - 30, 100)], "#C98A3C", 3.4)
        g.poly([(-31, -8), (31, -8), (0, 96)], None, INK, r=5)
        holes = [(34, -86, 17), (50, -62, 15), (22, -106, 12)] if bite else []
        with g.clip_out(holes):
            g.circle(0, -52, 50, scoop)
            g.path("M-48 -30 q10 26 24 6 q10 22 24 4 q12 20 24 0 q10 12 22 -6", scoop, INK)
            g.line("M-30 -76 q10 -16 28 -18", "#FFFFFF", 8, a=0.55)
        for x, y, r in holes:
            g.c.new_path()
        if bite:
            g.line("M17 -100 q-14 8 -4 22 q-12 10 2 24 q-8 12 10 22", INK, 4.8)
        if top:
            g.circle(-6, -104, 28, top)
    return f


def mug(col="#FFF4E0", band="#FF6B5B"):
    def f(g, t):
        g.line("M30 -50 q40 4 30 34 q-8 22 -30 16", INK, 22); g.line("M30 -50 q40 4 30 34 q-8 22 -30 16", col, 10)
        g.rect(-38, -78, 76, 92, col, r=(10, 10, 22, 22))
        g.rect(-38, -44, 76, 20, band, None)
        g.rect(-38, -78, 76, 92, None, INK, r=(10, 10, 22, 22))
        g.ellipse(0, -78, 38, 9, "#6B3F2A")
    return f


def cup_straw(col="#BFE6F2"):
    def f(g, t):
        g.line([(8, -60), (-34, -150)], INK, 17); g.line([(8, -60), (-34, -150)], "#FF6B5B", 8)
        g.path("M-34 -64 L34 -64 L26 40 L-26 40 Z", col)
        g.rect(-18, -30, 22, 22, "#FFFFFF", INK, lw=3.4, r=5, a=0.9); g.rect(2, -4, 20, 20, "#FFFFFF", INK, lw=3.4, r=5, a=0.9)
        g.rect(-40, -74, 80, 16, "#FFF4E0", r=6)
    return f


# ------------------------------------------------------------------ sets


def parlour(g, t, lights=1.0):
    """Ice-cream shop at night: dark teal tiled wall, display freezer and jar shelf on the left, pendant lamps, warm floor."""
    room(g, wall=("#092B37", "#0F4553"), floor=("#5C3B2E", "#33211C"), fy=1480)
    with g.layer(0.94):
        # shelf with jars (left, above the freezer)
        g.rect(-80, 962, 420, 22, "#7A4B2E", r=6)
        for i, c_ in enumerate(("#FF8FA8", "#5ED3B5", "#FFC93C")):
            x = 0 + i * 112
            g.rect(x, 872, 74, 90, c_, r=(10, 10, 14, 14)); g.rect(x - 5, 856, 84, 22, "#FFF4E0", r=8)
            g.line([(x + 14, 890), (x + 14, 940)], "#FFFFFF", 8, a=0.4)
    lamp(g, 190, 705, t, on=lights, r=470)
    lamp(g, 905, 560, t + 1.3, on=lights, r=330, sc=0.8)
    # display freezer
    x0 = -70
    g.rect(x0, 1228, 520, 262, "#C4574A", r=(22, 22, 0, 0))
    g.rect(x0, 1272, 520, 30, "#FFF4E0", None); g.line([(x0, 1272), (x0 + 520, 1272)], INK, 5); g.line([(x0, 1302), (x0 + 520, 1302)], INK, 5)
    for i in range(4):
        g.circle(x0 + 96 + i * 110, 1390, 20, shade("#C4574A", -0.22), None)
    g.rect(x0 + 16, 1092, 488, 142, "#0B3A47", None, r=(70, 70, 6, 6))
    with g.clip(rect=(x0 + 16, 1092, 488, 142)):
        for i, c_ in enumerate(("#FFB8C8", "#9BE3CC", "#FFF4E0", "#C98A5A")):
            cx = x0 + 104 + i * 112
            g.circle(cx, 1232, 62, c_); g.circle(cx - 30, 1214, 32, c_); g.circle(cx + 28, 1210, 36, c_)
            g.circle(cx - 30, 1214, 32, c_, None); g.circle(cx, 1232, 62, c_, None)
        g.rect(x0 + 16, 1092, 488, 142, "#BFE6F2", None, a=0.20)
        g.line([(x0 + 70, 1220), (x0 + 150, 1108)], "#FFFFFF", 16, a=0.35); g.line([(x0 + 112, 1220), (x0 + 172, 1136)], "#FFFFFF", 8, a=0.35)
    g.rect(x0 + 16, 1092, 488, 142, None, INK, r=(70, 70, 6, 6))
    g.glow(190, 1180, 330, "#FFC93C", 0.16 * lights)
    # warm pool of light on the floor
    g.ellipse(590, 1600, 520, 120, "#FFB060", None, a=0.10 * lights)
    g.ellipse(590, 1600, 330, 76, "#FFB060", None, a=0.08 * lights)


def lab(g, t):
    """Small science lab: tiled wall, long bench, brain poster, clock."""
    room(g, wall=("#0A2740", "#11405A"), floor=("#3B4858", "#222B37"), fy=1480, tile=(150, 110))
    with g.layer(0.94):
        # brain poster
        g.rect(96, 880, 250, 300, "#FFF4E0", r=12)
        g.circle(190, 990, 46, "#F7A9BC"); g.circle(246, 978, 50, "#F7A9BC"); g.circle(222, 1030, 46, "#F7A9BC")
        g.circle(190, 990, 46, "#F7A9BC", None); g.circle(246, 978, 50, "#F7A9BC", None)
        g.line("M176 992 q26 -30 54 -4 q22 22 46 -6", "#E0789A", 7)
        for i in range(3):
            g.line([(130, 1104 + i * 22), (312 - i * 40, 1104 + i * 22)], shade("#FFF4E0", -0.3), 8)
        # clock
        g.circle(900, 960, 74, "#FFF4E0"); g.circle(900, 960, 7, INK, None)
        a1 = t * 0.9
        g.line([(900, 960), (900 + 44 * math.sin(a1), 960 - 44 * math.cos(a1))], INK, 7)
        g.line([(900, 960), (900 + 28, 960 - 14)], INK, 8)
    lamp(g, 540, 640, t, col="#5ED3B5", light="#DFF6FF", r=520)
    # bench
    g.rect(-200, 1318, W + 400, 40, "#DCE6EA", r=8)
    g.rect(-200, 1358, W + 400, 140, "#2F5D74", None); g.line([(-200, 1358), (W + 200, 1358)], INK, 6)
    for x in (120, 430, 740):
        g.rect(x, 1384, 220, 86, None, shade("#2F5D74", -0.3), lw=5, r=10); g.circle(x + 110, 1404, 8, "#DCE6EA", None)


def monitor(g, t, x, y, w=400, h=280, widen=0.0, hot=0.0):
    """Lab monitor showing a blood vessel (red tube, pulsing) and a flow trace. (x, y) = screen centre."""
    g.rect(x - 34, y + h / 2 - 4, 68, 60, "#AEB8C2", r=6); g.rect(x - 96, y + h / 2 + 48, 192, 22, "#AEB8C2", r=9)
    g.rect(x - w / 2 - 16, y - h / 2 - 16, w + 32, h + 32, "#DCE6EA", r=26)
    g.rect(x - w / 2, y - h / 2, w, h, "#0B1E2B", r=12)
    with g.clip(rect=(x - w / 2, y - h / 2, w, h)):
        for i in range(1, 6):
            g.line([(x - w / 2 + i * w / 6, y - h / 2), (x - w / 2 + i * w / 6, y + h / 2)], "#FFFFFF", 2, a=0.07)
        for i in range(1, 4):
            g.line([(x - w / 2, y - h / 2 + i * h / 4), (x + w / 2, y - h / 2 + i * h / 4)], "#FFFFFF", 2, a=0.07)
        beat = 0.5 + 0.5 * math.sin(TAU * 1.5 * t)
        tw = 34 + 8 * beat + 46 * widen
        d = f"M{x - w / 2 - 20} {y - 34} C{x - 90} {y - 84} {x + 60} {y + 10} {x + w / 2 + 20} {y - 44}"
        g.line(d, "#7A1620", tw + 12); g.line(d, mix("#E5423D", "#FF7A5C", hot), tw)
        for i in range(6):
            u = (t * (0.5 + 0.9 * widen) + i / 6) % 1.0
            px, py, _ = path_at(d, u)
            g.circle(px, py + 5 * math.sin(i * 2.1), tw * 0.2, "#FFB3A6", None)
        pts = []
        for i in range(60):
            xx = x - w / 2 + 16 + i * (w - 32) / 59
            ph = (i / 59 * 3.2 - t * 1.5) % 1.0
            yy = y + 84 - (46 * math.exp(-((ph - 0.3) / 0.07) ** 2) + 12 * math.exp(-((ph - 0.55) / 0.12) ** 2)) * (1 + 0.8 * widen)
            pts.append((xx, yy))
        g.line(pts, "#5ED3B5", 6)
    g.circle(x + w / 2 - 6, y + h / 2 + 2, 6, "#5ED3B5", None)


def xray_bg(g, t, glow=(540, 1210), col="#1B6E86"):
    g.fill_all(g.lgrad(0, 0, 0, H, "#091C2B", "#0F3046"))
    with g.layer(0.85):
        for i in range(-6, 22):
            g.line([(i * 96, -400), (i * 96, H + 400)], "#FFFFFF", 2.5, a=0.045)
        for j in range(-4, 26):
            g.line([(-600, j * 96), (W + 600, j * 96)], "#FFFFFF", 2.5, a=0.045)
    g.rings(glow[0], glow[1], 640, col, a=0.085, n=4)


# ------------------------------------------------------------------ head cutaway (units 0..1000, facing right)

CUT = (88, 830, 0.9)   # where the 1000-unit drawing sits in the design space: x, y, scale
HEAD_D = ("M320 1080 L320 850 C170 780 100 610 100 430 C100 200 270 50 480 50 C690 50 830 190 840 360 C842 400 838 425 850 455 "
          "C880 490 905 535 900 565 C896 590 870 600 850 598 L846 648 "
          "C780 620 640 610 540 664 C498 688 494 732 522 754 C620 792 760 786 836 758 "
          "C850 800 836 842 800 864 C760 888 700 892 620 888 L600 1080 Z")
MOUTH_D = "M846 648 C780 620 640 610 540 664 C498 688 494 732 522 754 C620 792 760 786 836 758 Z"
PALATE_D = "M836 634 C776 606 644 596 552 646"
ARTERY_D = "M560 1080 C556 950 474 870 464 780 C456 700 474 636 522 600 C570 566 640 552 680 504 C702 478 708 444 702 414"
NERVE_P = "M772 626 C752 614 738 600 722 578"                                   # palate -> junction
NERVE_B = "M722 578 C694 566 668 540 640 506"                                   # junction -> brain
NERVE_F = "M722 578 C762 562 772 522 774 492 C778 442 812 402 808 332 C805 282 792 244 772 208"   # junction -> forehead
BRAIN_C = [(300, 275, 92), (395, 215, 100), (510, 205, 104), (615, 255, 96), (665, 335, 78), (600, 400, 92), (480, 415, 96), (360, 405, 92), (280, 350, 80)]
SKULL = (445, 338, 327, 262, 293, 230)
PALATE_PT = (700, 612)      # where the cold lands
FOREHEAD_PT = (800, 262)
BRAIN_PT = (455, 320)
ARTERY_PT = (610, 560)
MOUTH_PT = (690, 690)


def cut_pt(x, y):
    """Cutaway units -> design space."""
    return (CUT[0] + x * CUT[2], CUT[1] + y * CUT[2])


def cutaway(g, t, cold=0.0, widen=0.0, flow=0.0, pressure=0.0, nerve=None, signal=0.0, fpain=0.0, tongue=0.0, warm=0.0, eye="open",
            brain_face=None, brain_arm=0.0, lock=0.0, rivets=0.0, flash=0.0, skin="#F4C6A0", extra=None, brain_tint=0.0, sweat=0.0, arrows=True):
    """Wy's head in profile, cut open. All state values 0..1.
    cold: frost on the palate. widen/flow: the artery swells / blood streams. pressure: red glow, arrows on the skull.
    nerve: None (hidden) or (palate branch, brain trunk, forehead branch) reveal 0..1 each; signal: pain dots running.
    fpain: forehead throbs. tongue: pressed up to the palate. warm: orange warmth on the palate. eye: open|wide|pain|happy|up.
    brain_face: None | happy | blame | dizzy | worried. extra(g): draw more in cutaway units (ice cream etc.)."""
    lw0 = g.lw
    with g.at(CUT[0], CUT[1], 0, CUT[2]):
        g.lw = 7.5
        # curl (behind the head)
        d_ = "M436 66 C436 -34 628 -40 628 54 C628 108 550 108 542 176"
        g.line(d_, INK, 44); g.line(d_, "#5B3A29", 26)
        g.path(MOUTH_D, "#6E1E2C", None)
        g.path(HEAD_D, skin)
        # shirt + collar
        g.path("M276 1010 L640 1010 L668 1120 L250 1120 Z", "#FF6B5B")
        g.path("M560 1010 L600 1056 L640 1010 Z", "#FFF4E0")
        # cheek
        g.circle(770, 548, 30, "#F2918A", None, a=0.55)
        # palate (roof of the mouth)
        g.line(PALATE_D, "#F9B4C0", 17)
        if warm > 0:
            g.line(PALATE_D, "#FF9A3C", 19, a=0.85 * warm)
            g.glow(PALATE_PT[0], PALATE_PT[1] + 30, 150, "#FFA63C", 0.5 * warm)
        if cold > 0:
            u0, u1 = 0.48 - 0.48 * cold, 0.48 + 0.52 * cold
            g.line(path_part(PALATE_D, u0, u1), "#BDEBFF", 22)
            g.line(path_part(PALATE_D, u0, u1), "#FFFFFF", 7, a=0.8)
            n = int(9 * cold)
            for i in range(n):
                u = u0 + (u1 - u0) * (i + 0.5) / max(1, n)
                px, py, _ = path_at(PALATE_D, u)
                h_ = 16 + 9 * math.sin(i * 2.3)
                g.poly([(px - 8, py + 6), (px + 8, py + 6), (px + 1, py + 6 + h_)], "#DDF4FF", INK, lw=3.5)
            g.glow(PALATE_PT[0], PALATE_PT[1], 170 * cold, "#9FE0FF", 0.45 * cold)
        # tongue
        k = ease_io(tongue)
        g.path(f"M540 742 C566 {700 - 76 * k} 690 {694 - 92 * k} 792 {724 - 78 * k} C812 {732 - 40 * k} 826 748 834 757 C760 784 620 792 540 742 Z", "#F0808A")
        g.line(f"M600 {730 - 60 * k} Q690 {716 - 80 * k} 770 {738 - 60 * k}", "#D96574", 5, a=0.7)
        # teeth
        g.rect(818, 642, 17, 26, "#FFFFFF", INK, lw=4, r=6); g.rect(806, 728, 17, 24, "#FFFFFF", INK, lw=4, r=6)
        # skull + cavity
        sx, sy, orx, ory, irx, iry = SKULL
        bump = 1 + 0.02 * flash + 0.012 * pressure * math.sin(TAU * 7 * t)
        g.ellipse(sx, sy, orx * bump, ory * bump, mix("#FFF1DC", "#FFFFFF", flash))
        g.ellipse(sx, sy, irx, iry, mix("#43213A", "#8E2433", 0.75 * pressure), INK, lw=5)
        if pressure > 0:
            g.glow(ARTERY_PT[0], ARTERY_PT[1] - 40, 330, "#FF5B4B", 0.42 * pressure)
        # spinal cord + brain stem + cerebellum
        g.limb("M414 600 C418 760 420 900 424 1090", "#F3C9B0", 24, lw=5)
        # artery (under the brain)
        with g.clip(d=HEAD_D):
            beat = math.sin(TAU * 1.6 * t)
            aw = 21 + 27 * widen + (2.5 + 3 * widen) * beat * (0.4 + flow)
            g.limb(ARTERY_D, mix("#E5423D", "#FF5A45", widen), aw, lw=6)
            g.line(ARTERY_D, "#FF9C8E", aw * 0.22, a=0.7)
            n = 6 + int(10 * flow)
            for i in range(n):
                u = (t * (0.22 + 0.75 * flow) + i / n) % 1.0
                px, py, _ = path_at(ARTERY_D, u)
                g.circle(px, py, aw * (0.19 + 0.05 * math.sin(i * 3.1)), "#FFC2B5", None, a=0.95)
        g.limb("M388 462 C400 520 408 560 414 606", "#F3B7A6", 40, lw=5)
        g.circle(300, 468, 58, "#EE8FA6")
        for i in range(3):
            g.line(f"M{258 + i * 4} {448 + i * 20} q40 14 82 {-2 - i * 3}", "#D96A88", 5)
        # brain (squashed a little by the swollen artery / pressure)
        bsy = 1 - 0.055 * widen - 0.045 * pressure + 0.012 * math.sin(TAU * 1.6 * t) * (widen + pressure)
        with g.at(0, 150, 0, 1, bsy):
            with g.at(0, -150):
                bc = mix("#F7A9BC", "#FF7E88", 0.55 * max(brain_tint, 0.6 * pressure))
                for x, y, r in BRAIN_C:
                    g.circle(x, y, r, bc, INK, lw=15)
                for x, y, r in BRAIN_C:
                    g.circle(x, y, r, bc, None)
                g.ellipse(460, 320, 200, 124, bc, None)
                fc = mix("#E0789A", "#D94A60", 0.5 * max(brain_tint, 0.6 * pressure))
                for d_ in ("M290 296 q46 -54 96 -8 q42 36 92 -14", "M476 246 q40 -30 82 8", "M326 396 q52 -40 104 0 q50 38 108 -6", "M568 318 q40 -24 76 10",
                           "M246 336 q22 30 60 22"):
                    g.line(d_, fc, 9)
                g.line("M318 214 q30 -36 80 -42", "#FFFFFF", 12, a=0.38)
                if brain_face:
                    _brain_face(g, t, brain_face, brain_arm)
        # pressure arrows pushing on the skull from inside
        if pressure > 0.05 and arrows:
            for i, ang in enumerate((-2.55, -1.95, -1.2, -0.55, 0.05)):
                kk = ease_out(seg(pressure, 0.1 + i * 0.08, 0.5)) * (0.86 + 0.14 * math.sin(TAU * 3 * t + i))
                r0, r1 = 0.80, 0.985
                arrow(g, sx + irx * r0 * math.cos(ang), sy + iry * r0 * math.sin(ang), sx + irx * r1 * math.cos(ang), sy + iry * r1 * math.sin(ang),
                      "#FFF4E0", 17, 2.2, kk, lw=5)
        # rivets + lock: "a closed box"
        if rivets > 0:
            for i in range(7):
                ang = -2.9 + i * 0.42
                kk = pop(rivets, i * 0.11, 0.22)
                if kk > 0:
                    g.circle(sx + (orx + irx) / 2 * math.cos(ang), sy + (ory + iry) / 2 * math.sin(ang), 9.5 * kk, "#AEB8C2", INK, lw=4)
        if lock > 0:
            kk = back_out(clamp(lock), 2.4)
            with g.at(176, 196, -0.5, kk):
                g.line("M-20 -8 L-20 -34 C-20 -66 20 -66 20 -34 L20 -8", INK, 24); g.line("M-20 -8 L-20 -34 C-20 -66 20 -66 20 -34 L20 -8", "#AEB8C2", 11)
                g.rect(-36, -12, 72, 60, "#FFC93C", r=11)
                g.circle(0, 12, 8, INK, None); g.rect(-3.5, 14, 7, 18, INK, None)
        # nerve
        if nerve is not None:
            kp, kb, kf_ = nerve
            for d_, kk in ((NERVE_P, kp), (NERVE_B, kb), (NERVE_F, kf_)):
                if kk > 0.01:
                    pts = path_part(d_, 0, kk)
                    g.line(pts, "#FFC93C", 44, a=0.22)
                    g.line(pts, INK, 25); g.line(pts, "#FFC93C", 13); g.line(pts, "#FFF4C2", 4, a=0.9)
            if kp > 0.9:
                g.circle(722, 578, 19, "#FFC93C", INK, lw=6)
            if signal > 0:
                for i in range(4):
                    u = (t * 0.9 + i / 4) % 1.0
                    d_, uu = (NERVE_P, u * 2) if u < 0.5 else (NERVE_B, (u - 0.5) * 2)
                    if (d_ is NERVE_P and kp > 0.95) or (d_ is NERVE_B and kb > 0.95):
                        px, py, _ = path_at(d_, uu)
                        g.circle(px, py, 13, "#FFFFFF", INK, lw=4.5, a=signal)
        # forehead pain
        if fpain > 0:
            th = 0.6 + 0.4 * math.sin(TAU * 2.6 * t)
            g.glow(FOREHEAD_PT[0], FOREHEAD_PT[1], 150 * fpain * (0.8 + 0.2 * th), "#FF3B30", 0.75 * fpain)
            g.circle(FOREHEAD_PT[0] + 6, FOREHEAD_PT[1], 50 * fpain * (0.85 + 0.15 * th), "#FF5B4B", None, a=0.55)
            for i, (dx, dy, rr) in enumerate(((78, -74, 0.5), (112, 6, 0.9), (84, 86, 1.3))):
                bolt(g, FOREHEAD_PT[0] + dx, FOREHEAD_PT[1] + dy, 0.95 * fpain * (0.85 + 0.2 * math.sin(TAU * 3 * t + i)), rr - 0.9, "#FFC93C")
        # eye + brow (outside, on the face)
        ex, ey = 806, 458
        if eye == "pain":
            g.line([(ex + 20, ey - 20), (ex - 16, ey), (ex + 20, ey + 20)], INK, 10)
            g.line([(ex - 26, ey - 52), (ex + 26, ey - 40)], INK, 10)
        elif eye == "happy":
            g.line(f"M{ex - 22} {ey + 8} Q{ex} {ey - 26} {ex + 22} {ey + 8}", INK, 10)
            g.line(f"M{ex - 26} {ey - 44} Q{ex} {ey - 58} {ex + 26} {ey - 46}", INK, 9)
        else:
            wide = 1.14 if eye == "wide" else 1.0
            g.ellipse(ex, ey, 22 * wide, 30 * wide, "#FFFFFF")
            dx, dy = (4, -12) if eye == "up" else (8, 0)
            with g.clip(ellipse=(ex, ey, 22 * wide, 30 * wide)):
                g.circle(ex + dx, ey + dy, 13, INK, None); g.circle(ex + dx - 4, ey + dy - 5, 4.5, "#FFFFFF", None)
            g.ellipse(ex, ey, 22 * wide, 30 * wide, None, INK)
            yb = ey - 50 - (10 if eye == "wide" else 0)
            g.line(f"M{ex - 26} {yb + 6} Q{ex} {yb - 10} {ex + 26} {yb + 4}", INK, 9)
        if sweat > 0:
            kk = (t * 0.9) % 1.0
            g.path(f"M{760} {160 + 70 * kk} q-15 24 0 36 q15 -12 0 -36 Z", "#8FD8FF", INK, lw=4, a=sweat * (1 - kk))
        if extra:
            extra(g)
    g.lw = lw0


def _brain_face(g, t, kind, arm):
    """A little face on the front of the brain (it 'thinks'); arm 0..1 raises a pointing arm towards the forehead."""
    ex0, ey0 = 560, 300
    for i, ex in enumerate((ex0, ex0 + 84)):
        if kind == "dizzy":
            pts = []
            for j in range(36):
                a0 = j / 35 * TAU * 2.1 + t * 5 * (1 if i else -1)
                r_ = 3 + 20 * j / 35
                pts.append((ex + r_ * math.cos(a0), ey0 + r_ * math.sin(a0)))
            g.circle(ex, ey0, 27, "#FFFFFF", INK, lw=6); g.line(pts, INK, 5.5)
        elif kind == "happy":
            g.line(f"M{ex - 22} {ey0 + 8} Q{ex} {ey0 - 24} {ex + 22} {ey0 + 8}", INK, 9)
        else:
            g.ellipse(ex, ey0, 22, 28, "#FFFFFF", INK, lw=6)
            dx, dy = (9, -9) if kind == "blame" else (4, 4)
            g.circle(ex + dx, ey0 + dy, 12, INK, None); g.circle(ex + dx - 4, ey0 + dy - 5, 4, "#FFFFFF", None)
    if kind == "blame":
        g.line([(ex0 - 28, ey0 - 50), (ex0 + 22, ey0 - 32)], INK, 9); g.line([(ex0 + 62, ey0 - 32), (ex0 + 112, ey0 - 52)], INK, 9)
        g.line(f"M{ex0 + 16} {ey0 + 66} Q{ex0 + 44} {ey0 + 48} {ex0 + 72} {ey0 + 66}", INK, 8)
    elif kind == "worried":
        g.line([(ex0 - 26, ey0 - 34), (ex0 + 20, ey0 - 48)], INK, 9); g.line([(ex0 + 64, ey0 - 48), (ex0 + 110, ey0 - 34)], INK, 9)
        g.line(f"M{ex0 + 16} {ey0 + 68} Q{ex0 + 44} {ey0 + 50} {ex0 + 72} {ey0 + 68}", INK, 8)
    elif kind == "dizzy":
        g.line(f"M{ex0 + 10} {ey0 + 62} q9 -14 18 0 t18 0 t18 0", INK, 8)
    else:
        g.path(f"M{ex0 + 14} {ey0 + 48} Q{ex0 + 44} {ey0 + 86} {ex0 + 74} {ey0 + 48} Q{ex0 + 44} {ey0 + 58} {ex0 + 14} {ey0 + 48} Z", "#7A2230", INK, lw=6)
    if arm > 0:
        k = back_out(clamp(arm), 2.0)
        hx, hy = lerp(668, 742, k), lerp(392, 262, k) + 5 * math.sin(TAU * 3 * t) * k
        g.limb(f"M664 396 Q{lerp(676, 716, k)} {lerp(404, 360, k)} {hx} {hy}", "#F7A9BC", 17, lw=5.5)
        g.circle(hx, hy, 15, "#F7A9BC", INK, lw=5.5)
        g.limb([(hx + 6, hy - 8), (hx + 30 * k, hy - 34 * k)], "#F7A9BC", 9, lw=5)
