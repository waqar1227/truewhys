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


# ------------------------------------------------------------------ sky, aircraft, hangar tank, stress diagram (A-007, A-003)


def cloud(g, x, y, s=1.0, col="#DDF0F3", stroke=INK):
    with g.at(x, y, 0, s):
        pts = [(-112, 8, 50), (-50, -24, 66), (28, -12, 58), (98, 12, 46)]
        if stroke:
            for cx, cy, r in pts: g.circle(cx, cy, r, col, stroke, lw=13)
            g.rect(-160, 4, 304, 56, col, stroke, lw=13, r=28)
        for cx, cy, r in pts: g.circle(cx, cy, r, col, None)
        g.rect(-160, 4, 304, 56, col, None, r=28)


def sky(g, t, top="#081F33", bot="#17607A", stars=46, clouds=True, speed=70.0, seed=7):
    """Dusk sky with twinkling stars and clouds drifting left on parallax layers (the aircraft flies right)."""
    g.fill_all(g.lgrad(0, 0, 0, H, top, bot))
    R = rnd(seed)
    with g.layer(0.3):
        for i in range(stars):
            x, y, r, ph = R.uniform(-200, W + 200), R.uniform(-200, H * 0.85), R.uniform(2, 5), R.uniform(0, 6)
            g.circle(x, y, r, "#FFFFFF", None, a=0.35 + 0.3 * math.sin(t * 2 + ph))
    if clouds:
        for y, s_, dep, sp in ((300, 0.6, 0.4, 0.25), (540, 0.8, 0.5, 0.35), (1000, 1.05, 0.7, 0.6), (1760, 1.25, 0.85, 0.8), (1500, 1.5, 1.0, 1.0)):
            with g.layer(dep):
                x = (R.uniform(0, 1900) - t * speed * sp) % 1900 - 400
                cloud(g, x, y, s_, mix("#DDF0F3", bot, 0.6 - 0.5 * dep), None if dep < 0.6 else INK)


def plane(g, t, x, y, s=1.0, win="square", n=9, body="#E8EEF2", stripe="#FF6B5B", faces=False, bob=True, wing=True, fin=True, swell=0.0):
    """Chunky side-view jet airliner flying right (1950s Comet feel: engines buried in the wing root). win = square | round."""
    yy = y + (10 * math.sin(t * 1.3) if bob else 0)
    lw0 = g.lw
    with g.at(x, yy, 0.012 * math.sin(t * 0.9) if bob else 0, s):
        g.lw = 6.5
        if fin:
            g.poly([(-372, -44), (-468, -206), (-388, -206), (-282, -58)], stripe, r=10)
            g.poly([(-392, -4), (-512, -34), (-470, -52), (-340, -30)], shade(body, -0.18), r=8)
        if wing:
            g.poly([(-30, -30), (60, -30), (-10, -96), (-70, -96)], shade(body, -0.3), r=8)
        with g.at(0, 0, 0, 1, 1 + 0.07 * swell):
            d = "M-410 -58 C-486 -50 -490 44 -410 62 L300 72 C400 72 470 46 482 10 C470 -40 400 -72 300 -72 Z"
            g.path(d, body)
            with g.clip(d):
                g.rect(-520, 30, 1040, 60, shade(body, -0.16), None)
                g.rect(-520, 8, 1040, 16, stripe, None)
            g.path(d, None, INK)
            g.path("M392 -44 C430 -40 452 -22 462 -4 L404 -4 Z", "#0E3A47")
            x0, x1 = -300, 330
            for i in range(n):
                wx = x0 + (x1 - x0) * i / (n - 1)
                g.rect(wx - 21, -50, 42, 42, "#0E3A47", r=3 if win == "square" else 15)
                if faces and i % 2 == 1:
                    g.circle(wx, -24, 12, ("#F4C6A0", "#8D5A3B", "#E3A679")[i % 3], None)
                g.line([(wx - 12, -42), (wx - 4, -42)], "#FFFFFF", 4, a=0.5)
        if wing:
            g.poly([(-60, 26), (120, 26), (-70, 214), (-196, 214)], shade(body, -0.08), r=12)
            g.ellipse(52, 44, 26, 13, "#3A3F4A"); g.ellipse(-2, 60, 26, 13, "#3A3F4A")
    g.lw = lw0


def poly_part(pts, k):
    """First fraction k (by length) of a polyline."""
    if k <= 0: return [pts[0], pts[0]]
    L = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:])]
    tot, out, acc = sum(L) * min(1.0, k), [pts[0]], 0.0
    for (a, b), l in zip(zip(pts, pts[1:]), L):
        if acc + l <= tot:
            out.append(b); acc += l
        else:
            u = (tot - acc) / max(1e-9, l)
            out.append((a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u)); break
    return out


def crack(g, x, y, k, s=1.0, ang=0.0, col=INK):
    """A crack growing from (x, y) (k 0..1), with two side branches."""
    if k <= 0: return
    with g.at(x, y, ang, s):
        main = [(0, 0), (36, -48), (26, -96), (82, -132), (66, -190), (126, -236), (116, -304), (168, -352)]
        pts = poly_part(main, k)
        g.line(pts, "#FFFFFF", 17, a=0.35); g.line(pts, col, 9)
        for (i0, br, k0) in ((2, [(26, -96), (-22, -128), (-30, -170)], 0.35), (4, [(66, -190), (112, -200), (150, -182)], 0.6)):
            kk = clamp((k - k0) / 0.3)
            if kk > 0: g.line(poly_part(br, kk), col, 6.5)
        tx, ty = pts[-1]
        if k < 1: sparkle(g, tx, ty, 26, "#FFF4E0", k * 9)


def fuselage_skin(g, y_top=860, panel="#B9C9D4", water=0.0):
    """Close-up of aircraft skin filling the frame below a curved top edge: panel lines and rivets."""
    col = mix(panel, "#3F9CC0", 0.45 * water)
    g.path(f"M-700 {y_top + 90} Q540 {y_top - 70} 1780 {y_top + 90} L1780 2700 L-700 2700 Z", col)
    g.line(f"M-700 {y_top + 122} Q540 {y_top - 38} 1780 {y_top + 122}", "#FFFFFF", 10, a=0.35)
    for yy in (y_top + 250, y_top + 760, y_top + 1100):
        g.line([(-700, yy), (1780, yy)], shade(col, -0.25), 5)
        for i in range(-10, 30):
            g.circle(i * 62 + 20, yy - 22, 5.5, shade(col, -0.3), None); g.circle(i * 62 + 20, yy + 22, 5.5, shade(col, -0.3), None)
    for xx in (-140, 1220):
        g.line([(xx, y_top + 20), (xx, 2700)], shade(col, -0.25), 5)


def big_window(g, cx, cy, a=200, m=0.0, glass="#0E3A47", inside=None, rim="#7F8E99"):
    """One large cabin window on the skin; m: 0 = square corners .. 1 = rounded. inside(g) draws behind the glass (clipped)."""
    r0, r1 = lerp(10, a * 0.62, m), lerp(4, a * 0.55, m)
    g.rect(cx - a - 34, cy - a - 34, 2 * a + 68, 2 * a + 68, rim, r=r0 + 26)
    g.rect(cx - a, cy - a, 2 * a, 2 * a, glass, r=r1)
    if inside:
        c = g.c
        c.save(); g._rr(cx - a, cy - a, 2 * a, 2 * a, r1); c.clip()
        inside(g)
        c.restore()
    g.line([(cx - a + 40, cy - a + 60), (cx - a + 40 + a * 0.5, cy - a + 60 - a * 0.28)], "#FFFFFF", 16, a=0.28)
    g.rect(cx - a, cy - a, 2 * a, 2 * a, None, INK, r=r1)


def hangar(g, t, fy=1500):
    g.fill_all(g.lgrad(0, 0, 0, H, "#0A2233", "#14404F"))
    with g.layer(0.9):
        for i in range(-2, 9):
            g.line([(i * 190 - 60, -300), (i * 190 + 60, fy)], "#FFFFFF", 9, a=0.045)
        for yy in (560, 700):
            g.line([(-500, yy), (W + 500, yy)], "#FFFFFF", 9, a=0.05)
    lamp(g, 250, 600, t, col="#FFC93C", light="#FFE9A8", r=400, sc=0.9); lamp(g, 830, 600, t + 0.7, col="#FFC93C", light="#FFE9A8", r=400, sc=0.9)
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 500, "#3B4858", "#222B37"), None)
    g.line([(-600, fy), (W + 600, fy)], INK, 8)


TANK = (40, 905, 1000, 560)     # x, y, w, h of the water tank front


def tank_back(g, t):
    x, y, w, h = TANK
    g.rect(x - 22, y - 26, w + 44, h + 52, "#7F8E99", r=26)
    g.rect(x, y, w, h, g.lgrad(0, y, 0, y + h, "#2FA4C8", "#17688E"), r=10)


def tank_front(g, t, splash=0.0):
    """Water tint over whatever is in the tank, surface waves, bubbles, glass shine, frame."""
    x, y, w, h = TANK
    c = g.c
    c.save(); c.new_path(); c.rectangle(x, y, w, h); c.clip()
    g.rect(x, y + 34, w, h, "#2FA4C8", None, a=0.34)
    pts = [(x + i * 20, y + 34 + (7 + 14 * splash) * math.sin(i * 0.55 + t * 3.2) + (4 * math.sin(i * 1.3 - t * 2))) for i in range(int(w / 20) + 2)]
    g.poly(pts + [(x + w, y - 5), (x, y - 5)], "#0D2A3A", None)
    g.line(pts, "#BFF1FF", 8)
    R = rnd(11)
    for i in range(16):
        bx, ph, sp, r = R.uniform(x + 30, x + w - 30), R.random(), R.uniform(0.25, 0.5), R.uniform(6, 15)
        u = (ph + t * sp) % 1.0
        g.circle(bx + 10 * math.sin(t * 2 + i), y + h - u * (h - 50), r, None, "#BFF1FF", lw=4, a=0.75 * math.sin(u * math.pi))
    for i in range(4):
        g.line([(x + 110 + i * 250, y + 44), (x + 30 + i * 250, y + h)], "#FFFFFF", 46, a=0.05)
    c.restore()
    g.rect(x, y, w, h, None, INK, r=10)
    g.rect(x - 22, y - 26, w + 44, h + 52, None, INK, r=26)
    for bx in (x - 4, x + w + 4):
        for by in (y + 20, y + h / 2, y + h - 20):
            g.circle(bx, by, 8, "#AEB8C2", INK, lw=4)


def _sup(cx, cy, a, n, grow=0.0, steps=72):
    """Superellipse outline points (n = 2 circle, large n = square) with radius a + grow."""
    out = []
    for i in range(steps + 1):
        th = TAU * i / steps
        cs, sn = math.cos(th), math.sin(th)
        r = (abs(cs) ** n + abs(sn) ** n) ** (-1.0 / n)
        out.append((cx + (a * r + grow * (1 + 0.0)) * cs, cy + (a * r + grow) * sn))
    return out


def stress_field(g, t, cx, cy, a=190, m=0.0, hot=1.0, nlines=9, span=560, col="#FFF4E0", speed=220.0, water=False, hole=True, glow=True):
    """Flow lines (stress) streaming left to right around an opening. m: 0 = sharp square, 1 = rounded.
    With sharp corners the lines crowd together at the corners and glow red (hot 0..1); rounded spreads them evenly."""
    n = lerp(9.0, 2.6, m)
    crowd = (1 - m) * hot
    if glow and crowd > 0.02:
        th = 0.75 + 0.25 * math.sin(TAU * 2.2 * t)
        for sx_, sy_ in ((1, -1), (1, 1), (-1, -1), (-1, 1)):
            g.glow(cx + sx_ * a * 0.93, cy + sy_ * a * 0.93, 150 * crowd * th, "#FF3B30", 0.8 * crowd)
    for side in (-1, 1):
        for k in range(nlines):
            gap = 26 + k * 40
            pts = []
            for i in range(81):
                x = cx - span + i * (2 * span) / 80
                u = (x - cx) / a
                # height of the opening's edge above the centre line at this x (0 outside the opening)
                e = a * (max(0.0, 1 - abs(u) ** n)) ** (1.0 / n) if abs(u) < 1 else 0.0
                # smooth approach before/after the opening
                ap = math.exp(-((max(0.0, abs(u) - 1.0)) / (1.05 + 0.25 * m)) ** 2) if abs(u) >= 1 else 1.0
                edge = max(e, a * ap * (0.86 if abs(u) >= 1 else 0.0) * math.exp(-k * 0.5))
                cw = math.exp(-((abs(u) - 0.96) / 0.2) ** 2)             # near the corners
                gk = gap * (1 - 0.62 * crowd * cw) * (1 + 0.25 * (1 - cw) * crowd)
                base = (k + 0.5) * 44 * (1 - math.exp(-((abs(u)) / 2.1) ** 2) * 0.0)
                y = max(base, edge + gk)
                pts.append((x, cy + side * y))
            heat = clamp(crowd * math.exp(-k * 0.42))
            c_ = "#69C7F0" if water else mix(col, "#FF5B4B", heat)
            g.line(pts, c_, 8 if not water else 7, a=0.95, dash=([34, 22], -t * speed))
    if hole:
        g.poly(_sup(cx, cy, a + 20, n), "#7F8E99", INK, lw=7)
        g.poly(_sup(cx, cy, a, n), "#0E3A47", INK, lw=7)


def newspaper(g, x, y, s=1.0, rot=0.0, head="COMET MYSTERY", sub="WHY?", year="1954"):
    with g.at(x, y, rot, s):
        g.rect(-330, -420, 660, 840, "#2A1C1E", None, r=10, a=0.25)
        g.rect(-340, -436, 660, 840, "#FFF4E0", r=10)
        g.text("THE DAILY NEWS", -10, -372, 62, INK, stroke=None)
        g.line([(-300, -326), (280, -326)], INK, 6); g.line([(-300, -312), (280, -312)], INK, 3)
        g.text(year, 216, -280, 34, INK, stroke=None, font="Poppins", bold=True)
        g.text(head, -10, -196, 92 if len(head) < 14 else 76, INK, stroke=None)
        g.rect(-300, -120, 300, 230, "#C9D6DC", INK, lw=5, r=6)
        with g.at(-150, 6, -0.1, 0.27):
            plane(g, 0, 0, 0, 1.0, bob=False)
        g.text(sub, 150, -8, 150, "#FF5B4B", sw=22, rot=-0.12)
        for i in range(6):
            g.rect(-300, 150 + i * 40, 560 if i % 3 else 470, 16, shade("#FFF4E0", -0.28), None, r=6)
