"""Style F pets and props (B-007 "Cats vs Dogs", 25 Nov 2026). Original, code-drawn (TrueWhys).

    from flat_pets import *
    cat_sit(g, x, y, s, t, ...)   dog_sit(g, x, y, s, t, ...)     front view, sitting, feet at (x, y)
    cat_side(g, x, y, s, t, ...)  dog_side(g, x, y, s, t, ...)    side view facing right (flip=True faces left), feet at (x, y)
    cat_face / dog_face / wolf face (dog_face(..., wolf=True))   close-up heads centred at (x, y)
    props: bowl, sofa, scoreboard, toy_pile, toy, mouse, bear_side, baby_face, speaker, hs_camera, paw, neuron_dots, dna_tree, grain_jar
Sizes: s=1 -> sitting cat ~470 units tall, sitting dog ~600 units tall. Cats: deadpan by default (cast v2.2 style: lids, small brows).
"""
import math
from flat2d import INK, PAL, mix, shade, clamp, ease_io, seg

LW = 8
CAT = dict(fur="#F29A3E", dark="#C66A1C", light="#FFE6C8", inner="#FFB3A6", iris="#9BCB4A", nose="#FF8A9A")
DOG = dict(fur="#D9A35E", dark="#9A6430", light="#FFF1DC", ear="#8A5428", iris="#5A3418", nose="#2A1C1E", collar="#2F8FA0")
WOLF = dict(fur="#9AA3AD", dark="#5F6670", light="#E6E8EB", ear="#6E7680", iris="#C9A23A", nose="#2A1C1E", collar=None)


def _blink(t, seed=0.0):
    """Natural blinks every ~3.4 s (0 open .. 1 closed)."""
    if t is None:
        return 0.0
    ph = (t + seed * 1.37) % 3.4
    return max(0.0, 1 - abs(ph - 0.08) / 0.08) if ph < 0.16 else 0.0


# ------------------------------------------------------------------ cat head (front)
def cat_face(g, x, y, s=1.0, t=0.0, expr="deadpan", ear_l=0.0, ear_r=0.0, look=(0.0, 0.0), tilt=0.0, blink=None, pupil=0.35,
             mouth_open=0.0, col=CAT, seed=0.0):
    """Front cat head, centre (x, y), ~250 units wide at s=1.
    expr: deadpan | smug | happy (content, eyes closed curves) | shock | bored | alert | sleepy.
    ear_l / ear_r: -1 (swivelled back/out) .. 0 .. 1 (pricked forward, turned to a sound). pupil 0 slit .. 1 round."""
    b = _blink(t, seed) if blink is None else blink
    with g.at(x, y, tilt, s):
        for sd, e in ((-1, ear_l), (1, ear_r)):
            with g.at(sd * 70, -62, sd * (0.18 + 0.35 * e) if e < 0 else sd * (0.1 - 0.12 * e), 1, 1 - 0.25 * max(0, -e)):
                pts = [(-sd * 46, 18), (sd * 22, -96 - 10 * max(0, e)), (sd * 52, 14)]
                g.poly(pts, col["fur"], INK, lw=LW, r=10)
                g.poly([(-sd * 26, 8), (sd * 20, -66 - 8 * max(0, e)), (sd * 36, 6)], col["inner"], None, r=6)
        g.path("M-128 -10 Q-130 -96 0 -104 Q130 -96 128 -10 Q132 58 92 88 Q40 116 0 114 Q-40 116 -92 88 Q-132 58 -128 -10 Z",
               col["fur"], INK, lw=LW)
        for sd in (-1, 1):                                   # cheek tufts
            g.path(f"M{sd*124} 30 L{sd*150} 44 L{sd*120} 56 L{sd*140} 70 L{sd*104} 78", col["fur"], INK, lw=LW * 0.8)
        for i in (-1, 0, 1):                                 # forehead stripes
            g.path(f"M{i*26} -100 Q{i*30} -78 {i*22} -60", None, col["dark"], lw=9)
        g.path("M-58 30 Q-60 -2 -22 4 Q0 10 22 4 Q60 -2 58 30 Q56 74 0 86 Q-56 74 -58 30 Z", col["light"], None)   # muzzle
        lx, ly = look[0] * 8, look[1] * 6
        for sd in (-1, 1):
            ex, ey = sd * 50, -22
            if expr == "happy":
                g.path(f"M{ex-24} {ey+4} Q{ex} {ey-16} {ex+24} {ey+4}", None, INK, lw=8)
                continue
            ry = 23 * (1 - b)
            if expr == "shock":
                ry *= 1.15
            if ry > 2:
                g.ellipse(ex, ey, 27, ry, col["iris"], INK, lw=6)
                pw = 4 + 14 * (1.0 if expr == "shock" else pupil)
                g.ellipse(ex + lx, ey + ly, pw, max(2, ry * 0.86), INK, None)
                g.circle(ex + lx + 8, ey + ly - 9 * (1 - b), 6, "#FFFFFF", None, a=0.95)
                lid = {"deadpan": 0.38, "smug": 0.52, "bored": 0.62, "sleepy": 0.75, "alert": 0.05, "shock": 0.0}.get(expr, 0.3)
                if lid > 0:                                  # upper lid (fur colour) = the cat's deadpan look
                    yy = ey - ry + 2 * ry * lid
                    g.path(f"M{ex-30} {ey-ry-6} L{ex+30} {ey-ry-6} L{ex+30} {yy} Q{ex} {yy+4} {ex-30} {yy} Z", col["fur"], None)
                    g.line([(ex - 27, yy), (ex + 27, yy + (4 if expr == "smug" else 0) * sd)], INK, 6)
            else:
                g.line([(ex - 26, ey), (ex + 26, ey)], INK, 7)
            by = ey - 40 - (10 if expr in ("shock", "alert") else 0)        # small brow marks
            g.line([(ex - 14 * sd, by + (4 if expr == "smug" and sd < 0 else 0)), (ex + 10 * sd, by - 4)], col["dark"], 7)
        g.path("M-15 12 L15 12 Q0 32 0 32 Q0 32 -15 12 Z", col["nose"], INK, lw=5)
        if mouth_open > 0.05 or expr == "shock":
            mo = max(mouth_open, 0.7 if expr == "shock" else 0)
            g.ellipse(0, 50, 16 + 6 * mo, 10 + 18 * mo, "#5A1E26", INK, lw=5)
            g.ellipse(0, 58 + 8 * mo, 10, 6 * mo, "#FF8A9A", None)
        else:
            up = 6 if expr in ("smug", "happy") else 0
            g.path(f"M0 30 L0 40 Q-14 {54 - up} -30 {44 - up}", None, INK, lw=5)
            g.path(f"M0 40 Q14 {54 - up} 30 {44 - up}", None, INK, lw=5)
        for sd in (-1, 1):
            for k in (-1, 0, 1):
                g.line([(sd * 62, 40 + k * 12), (sd * 150, 30 + k * 22 + 4 * math.sin((t or 0) * 2 + k))], INK, 3, a=0.8)


# ------------------------------------------------------------------ dog head (front)
def dog_face(g, x, y, s=1.0, t=0.0, expr="happy", brow=0.0, tongue=0.0, tilt=0.0, look=(0.0, 0.0), blink=None, ear=0.0,
             wolf=False, col=None, seed=0.0, mouth_open=0.0):
    """Front dog head, centre (x, y), ~300 units wide at s=1.
    expr: happy | calm | sad | shock | proud | sniff. brow 0..1 = inner-eyebrow raise (puppy eyes: bigger, glossier eyes, inner brows up).
    wolf=True draws a grey wolf with upright ears and flat brows (no brow muscle). ear -1..1 flaps the floppy ears."""
    col = col or (WOLF if wolf else DOG)
    b = _blink(t, seed + 0.7) if blink is None else blink
    with g.at(x, y, tilt, s):
        if wolf:
            for sd in (-1, 1):
                g.poly([(sd * 40, -80), (sd * 104, -190), (sd * 128, -50)], col["fur"], INK, lw=LW, r=12)
                g.poly([(sd * 62, -84), (sd * 102, -156), (sd * 112, -66)], col["dark"], None, r=8)
        g.path("M-120 -30 Q-122 -118 0 -124 Q122 -118 120 -30 Q132 40 104 92 Q60 140 0 140 Q-60 140 -104 92 Q-132 40 -120 -30 Z",
               col["fur"], INK, lw=LW)
        g.path("M-24 -124 Q0 -40 -14 30 L14 30 Q0 -40 24 -124 Z", col["light"], None, a=0.9)          # blaze
        if not wolf:
            for sd in (-1, 1):                               # floppy ears
                sw = 0.08 * math.sin((t or 0) * 3 + sd) + 0.25 * ear
                with g.at(sd * 104, -80, sd * sw):
                    g.path(f"M0 -10 Q{sd*70} -30 {sd*76} 60 Q{sd*80} 150 {sd*30} 160 Q{sd*-10} 150 {sd*-6} 60 Q{sd*-8} 10 0 -10 Z",
                           col["ear"], INK, lw=LW)
        g.path("M-80 60 Q-86 10 -30 8 L30 8 Q86 10 80 60 Q76 126 0 132 Q-76 126 -80 60 Z", col["light"], None)   # muzzle
        lx, ly = look[0] * 9, look[1] * 7
        big = 1 + 0.28 * brow
        for sd in (-1, 1):
            ex, ey = sd * 50, -30
            if expr == "happy" and brow < 0.2 and not wolf:
                g.path(f"M{ex-22} {ey+6} Q{ex} {ey-16} {ex+22} {ey+6}", None, INK, lw=8)
            else:
                ry = 21 * big * (1 - b) * (1.15 if expr == "shock" else 1)
                if ry > 2:
                    g.ellipse(ex, ey, 21 * big, ry, "#FFFFFF" if wolf else col["iris"], INK, lw=6)
                    if wolf:
                        g.ellipse(ex + lx, ey + ly, 12, min(ry, 12), col["iris"], None)
                    g.circle(ex + lx, ey + ly, 9 * big if not wolf else 5, INK, None)
                    g.circle(ex + lx + 7, ey + ly - 8, 6 + 4 * brow, "#FFFFFF", None, a=0.95)
                    if brow > 0.3:
                        g.circle(ex + lx - 6, ey + ly + 7, 3 + 2 * brow, "#FFFFFF", None, a=0.8)
                    if expr == "sad" and brow < 0.3:
                        g.path(f"M{ex-24} {ey-ry} L{ex+24} {ey-ry} L{ex+24} {ey-ry*0.2} Q{ex} {ey-ry*0.5} {ex-24} {ey-ry*0.2} Z" if False else
                               f"M{ex-24*sd} {ey-ry-4} L{ex+24*sd} {ey-ry-4} L{ex+24*sd} {ey-ry*0.1}", col["fur"], None)
                else:
                    g.line([(ex - 20, ey), (ex + 20, ey)], INK, 7)
            # brows: the inner end lifts with `brow` (the dog's special muscle); a wolf's brows stay flat
            inner = -14 * brow - (8 if expr == "shock" else 0) + (6 if expr == "sad" and brow < 0.2 else 0)
            outer = 4 * brow
            g.limb([(ex - 22 * sd, ey - 40 + outer), (ex, ey - 46 + (inner + outer) / 2), (ex + 16 * sd * -1 * -1, ey - 42 + inner)] if False else
                   [(ex + 24 * sd, ey - 40 + outer), (ex + 2 * sd, ey - 44 + (inner + outer) / 2), (ex - 18 * sd, ey - 40 + inner * 1.6)],
                   col["dark"], 13, lw=0)
        g.path("M-34 30 Q0 14 34 30 Q38 56 0 66 Q-38 56 -34 30 Z", col["nose"], INK, lw=5)            # nose
        g.ellipse(-12, 32, 10, 5, "#FFFFFF", None, a=0.35)
        mo = max(mouth_open, 0.8 if expr == "shock" else 0, 0.5 if (tongue > 0 and expr == "happy") else 0)
        if mo > 0.05:
            g.path(f"M-46 86 Q0 {86 + 50 * mo} 46 86 Q0 {96 + 10 * mo} -46 86 Z", "#5A1E26", INK, lw=5)
        g.path("M0 66 L0 86 Q-24 100 -46 86", None, INK, lw=5)
        g.path("M0 86 Q24 100 46 86", None, INK, lw=5)
        if tongue > 0.05:
            tl = 30 + 70 * tongue + 6 * math.sin((t or 0) * 9)
            g.path(f"M-22 92 L22 92 L24 {92 + tl} Q0 {112 + tl} -24 {92 + tl} Z", "#FF7A8A", INK, lw=5)
            g.line([(0, 98), (0, 86 + tl)], "#E0566A", 4)
        if not wolf and col.get("collar"):
            g.rc(0, 150, 170, 26, col["collar"], INK, lw=6, r=12)
            g.circle(0, 172, 14, PAL["yellow"], INK, lw=5)


# ------------------------------------------------------------------ full bodies, front, sitting
def cat_sit(g, x, y, s=1.0, t=0.0, expr="deadpan", ear_l=0.0, ear_r=0.0, look=(0, 0), tilt=0.0, tail=1.0, paw=0.0,
            col=CAT, seed=0.0, pupil=0.35, mouth_open=0.0, blink=None, breathe=True):
    """Sitting cat, front view, feet at (x, y). paw 0..1 lifts the right front paw (a wave / point)."""
    br = 1 + (0.012 * math.sin((t or 0) * 2.1 + seed) if breathe else 0)
    with g.at(x, y, 0, s):
        sw = 0.5 * math.sin((t or 0) * 1.6 + seed) * tail
        g.path(f"M60 -20 Q190 -10 {200 + 30 * sw} {-90 - 40 * sw} Q{214 + 30 * sw} {-150 - 40 * sw} {236 + 40 * sw} {-170 - 50 * sw} "
               f"Q{250 + 40 * sw} {-150 - 50 * sw} {228 + 30 * sw} {-90 - 40 * sw} Q220 20 60 16 Z", col["fur"], INK, lw=LW)
        with g.at(0, 0, 0, 1, br):
            g.path("M-70 -300 Q-130 -200 -130 -80 Q-130 0 -60 4 L60 4 Q130 0 130 -80 Q130 -200 70 -300 Z", col["fur"], INK, lw=LW)
            g.path("M-48 -270 Q-80 -150 -60 -60 L60 -60 Q80 -150 48 -270 Z", col["light"], None)
            for i in (-1, 1):
                g.path(f"M{i*118} -170 Q{i*96} -150 {i*112} -128", None, col["dark"], lw=9)
                g.path(f"M{i*124} -120 Q{i*100} -100 {i*118} -80", None, col["dark"], lw=9)
            for sd in (-1, 1):
                lift = paw if sd > 0 else 0
                with g.at(sd * 42, -150, -sd * 0.9 * lift):
                    g.limb([(0, 0), (0, 70 - 50 * lift), (2, 140 - 120 * lift)], col["fur"], 50, lw=LW)
                    g.ellipse(2, 146 - 124 * lift, 32, 18, col["light"], INK, lw=6)
        cat_face(g, 0, -348 * br, 0.95, t, expr, ear_l, ear_r, look, tilt, blink, pupil, mouth_open, col, seed)


def dog_sit(g, x, y, s=1.0, t=0.0, expr="happy", brow=0.0, tongue=0.4, tilt=0.0, look=(0, 0), wag=1.0, paw=0.0,
            col=None, seed=0.0, blink=None, mouth_open=0.0, ear=0.0, wolf=False):
    """Sitting dog, front view, feet at (x, y). wag 0..1 tail wag amount; paw 0..1 lifts the right front paw."""
    col = col or (WOLF if wolf else DOG)
    br = 1 + 0.015 * math.sin((t or 0) * (3.2 if tongue > 0.2 else 2.0) + seed)
    with g.at(x, y, 0, s):
        wg = math.sin((t or 0) * 12 + seed) * wag
        with g.at(110, -60, -0.6 + 0.45 * wg):
            g.limb([(0, 0), (60, -50), (90, -130)], col["fur"], 40, lw=LW)
            g.circle(92, -134, 22, col["light"], None)
        with g.at(0, 0, 0, 1, br):
            g.path("M-90 -380 Q-170 -250 -165 -90 Q-160 4 -80 6 L80 6 Q160 4 165 -90 Q170 -250 90 -380 Z", col["fur"], INK, lw=LW)
            g.path("M-70 -360 Q-100 -230 -64 -120 Q0 -90 64 -120 Q100 -230 70 -360 Z", col["light"], None)
            for sd in (-1, 1):
                lift = paw if sd > 0 else 0
                with g.at(sd * 58, -200, -sd * 0.9 * lift):
                    g.limb([(0, 0), (0, 100 - 60 * lift), (3, 194 - 150 * lift)], col["fur"], 64, lw=LW)
                    g.ellipse(3, 200 - 152 * lift, 42, 22, col["light"], INK, lw=6)
                    for k in (-1, 1):
                        g.line([(3 + k * 13, 190 - 152 * lift), (3 + k * 13, 206 - 152 * lift)], INK, 4)
        dog_face(g, 0, -470 * br, 1.0, t, expr, brow, tongue, tilt, look, blink, ear, wolf, col, seed, mouth_open)


# ------------------------------------------------------------------ side views (facing right)
def cat_side(g, x, y, s=1.0, t=0.0, flip=False, walk=0.0, head_down=0.0, tongue=0.0, expr="deadpan", tail=1.0, col=CAT, seed=0.0,
             crouch=0.0, ear=0.0):
    """Side-view cat facing right, feet at (x, y). walk 0..1 gait; head_down 0..1 lowers the head to a bowl (drinking);
    tongue 0..1 extends the tongue tip down to the water."""
    with g.at(x, y, 0, -s if flip else s, s):
        T = t or 0
        by = -150 + 50 * crouch + 3 * math.sin(T * 2 + seed)

        def leg(lx, ph, near):
            a = 0.35 * walk * math.sin(T * 7 + ph)
            c = col["fur"] if near else col["dark"]
            with g.at(lx, by + 30, a):
                g.limb([(0, 0), (6, 60 - 25 * crouch), (2, 120 - 50 * crouch)], c, 36 if near else 32, lw=LW)
                g.ellipse(8, 122 - 50 * crouch, 24, 12, c, INK, lw=6)
        leg(-100, math.pi, False); leg(95, 0, False)
        sw = math.sin(T * 1.5 + seed) * tail
        g.path(f"M-140 {by-20} Q-250 {by-40} {-270 + 20 * sw} {by-150 - 30 * sw} Q{-268 + 20 * sw} {by-180 - 30 * sw} {-250 + 20 * sw} {by-170 - 30 * sw} "
               f"Q{-236 + 10 * sw} {by-60} -140 {by+6} Z", col["fur"], INK, lw=LW)
        g.ellipse(0, by, 160, 72, col["fur"], INK, lw=LW)
        g.ellipse(20, by + 34, 110, 28, col["light"], None)
        for i in range(3):
            g.path(f"M{-90 + i * 45} {by-68} Q{-80 + i * 45} {by-36} {-90 + i * 45} {by-12}", None, col["dark"], lw=9)
        leg(-130, 0.0, True); leg(120, math.pi, True)
        hd = ease_io(clamp(head_down))
        hx, hy = 170 + 40 * hd, by - 80 + 150 * hd
        g.path(f"M90 {by-50} Q{hx-30} {hy-20} {hx} {hy} L{hx-10} {hy+60} Q110 {by+30} 80 {by+30} Z", col["fur"], INK, lw=LW)   # neck
        with g.at(hx, hy, 0.5 * hd):
            for ex_, rot in ((-34, -0.25 + 0.4 * ear), (8, 0.05 + 0.2 * ear)):
                with g.at(ex_, -48, rot):
                    g.poly([(-26, 10), (2, -66), (28, 8)], col["fur"], INK, lw=LW, r=8)
                    g.poly([(-12, 4), (2, -44), (16, 4)], col["inner"], None, r=5)
            g.path("M-70 0 Q-70 -62 0 -64 Q60 -62 76 -10 Q96 14 82 32 Q60 56 0 58 Q-70 56 -70 0 Z", col["fur"], INK, lw=LW)
            g.ellipse(52, 26, 34, 22, col["light"], None)
            g.path("M80 8 L92 14 L82 22 Z", col["nose"], INK, lw=4)
            if expr == "happy":
                g.path("M18 -12 Q30 -24 42 -12", None, INK, lw=7)
            else:
                g.ellipse(32, -12, 12, 15, col["iris"], INK, lw=5)
                g.ellipse(35, -12, 4, 12, INK, None)
                lid = {"deadpan": 0.4, "smug": 0.55, "alert": 0.0, "shock": 0.0}.get(expr, 0.35)
                if lid:
                    g.path(f"M18 -30 L46 -30 L46 {-27 + 30 * lid} L18 {-27 + 30 * lid} Z", col["fur"], None)
                    g.line([(19, -27 + 30 * lid), (45, -27 + 30 * lid)], INK, 5)
            for k in (-1, 1):
                g.line([(64, 30 + k * 6), (130, 22 + k * 14)], INK, 3, a=0.8)
            if tongue > 0.02:
                L = 90 * tongue
                g.limb([(76, 40), (82, 40 + L * 0.6), (80, 40 + L)], "#FF8A9A", 12, lw=4)


def dog_side(g, x, y, s=1.0, t=0.0, flip=False, walk=0.0, head_down=0.0, tongue=0.0, curl=0.0, expr="happy", wag=1.0, col=None,
             seed=0.0, sniff=0.0, wolf=False):
    """Side-view dog facing right, feet at (x, y). head_down lowers the head; tongue/curl: tongue reaching down, curled back like a ladle."""
    col = col or (WOLF if wolf else DOG)
    with g.at(x, y, 0, -s if flip else s, s):
        T = t or 0
        by = -230 + 4 * math.sin(T * 3 + seed)

        def leg(lx, ph, near):
            a = 0.4 * walk * math.sin(T * 8 + ph)
            c = col["fur"] if near else shade(col["fur"], -0.18)
            with g.at(lx, by + 50, a):
                g.limb([(0, 0), (8, 90), (4, 176)], c, 46 if near else 40, lw=LW)
                g.ellipse(12, 178, 30, 15, col["light"] if near else c, INK, lw=6)
        leg(-130, math.pi, False); leg(120, 0, False)
        wg = math.sin(T * 12 + seed) * wag
        with g.at(-190, by - 30, -0.9 + 0.4 * wg):
            g.limb([(0, 0), (-40, -60), (-50, -130)], col["fur"], 34, lw=LW)
        g.path(f"M-200 {by} Q-210 {by-90} -100 {by-96} L120 {by-100} Q220 {by-96} 220 {by-10} Q216 {by+80} 120 {by+80} L-110 {by+82} Q-200 {by+80} -200 {by} Z",
               col["fur"], INK, lw=LW)
        g.path(f"M60 {by+70} Q160 {by+60} 200 {by+10} Q200 {by+70} 120 {by+82} L40 {by+82} Z", col["light"], None)
        leg(-160, 0.0, True); leg(150, math.pi, True)
        hd = ease_io(clamp(max(head_down, 0.35 * sniff)))
        hx, hy = 250 + 40 * hd, by - 130 + 230 * hd
        g.path(f"M130 {by-80} Q{hx-40} {hy-30} {hx-10} {hy} L{hx-30} {hy+80} Q180 {by+40} 150 {by+40} Z", col["fur"], INK, lw=LW)
        if col.get("collar") and not wolf:
            g.limb([(hx - 74 + 20 * hd, hy + 20), (hx - 40, hy + 60 - 10 * hd)], col["collar"], 26, lw=6)
        with g.at(hx, hy, 0.6 * hd):
            g.path("M-80 0 Q-80 -80 0 -82 Q60 -80 80 -40 L150 -20 Q176 -10 170 20 Q160 46 120 48 L40 56 Q-80 70 -80 0 Z", col["fur"], INK, lw=LW)
            g.path("M70 -20 L150 -14 Q170 -6 166 18 Q156 40 120 44 L60 46 Z", col["light"], None)
            g.ellipse(166, -6, 20, 16, col["nose"], INK, lw=5)
            if sniff:
                for k in range(3):
                    ph = (T * 2.5 + k / 3) % 1
                    g.circle(200 + 60 * ph, -10 - 30 * ph + 10 * math.sin(k + T * 5), 6 + 8 * ph, "#FFFFFF", INK, lw=3, a=0.6 * (1 - ph))
            if expr == "happy":
                g.path("M18 -38 Q32 -52 46 -38", None, INK, lw=7)
            else:
                g.circle(32, -36, 14, "#FFFFFF" if wolf else col["iris"], INK, lw=5)
                g.circle(36, -36, 7, INK, None)
            g.line([(10, -60), (50, -64)], col["dark"], 10)
            if wolf:
                g.poly([(-50, -60), (-30, -140), (6, -70)], col["fur"], INK, lw=LW, r=8)
            else:
                g.path("M-40 -70 Q10 -84 0 -20 Q-10 60 -50 60 Q-80 40 -60 -20 Q-56 -60 -40 -70 Z", col["ear"], INK, lw=LW)
            if tongue > 0.02:
                L = 120 * tongue
                tip = (120 - 40 * curl, 48 + L)
                g.limb([(110, 40), (118, 40 + L * 0.6), tip], "#FF7A8A", 22, lw=5)
                if curl > 0.05:                              # tongue tip curled backwards like a ladle
                    g.path(f"M{tip[0]-14} {tip[1]} Q{tip[0]-40*curl} {tip[1]+30*curl} {tip[0]-60*curl} {tip[1]-6}", None, "#FF7A8A", lw=20)
                    g.path(f"M{tip[0]-14} {tip[1]} Q{tip[0]-40*curl} {tip[1]+30*curl} {tip[0]-60*curl} {tip[1]-6}", None, INK, lw=4)


# ------------------------------------------------------------------ props
def bowl(g, x, y, s=1.0, water=True, splash=0.0, column=0.0, t=0.0, col="#FF6B5B", wide=1.0):
    """Pet water bowl, base centre (x, y). column 0..1 = thin water column pulled up (height ~120*s); splash 0..1 droplets."""
    with g.at(x, y, 0, s):
        w = 150 * wide
        if column > 0.02:
            hgt = 140 * column
            g.path(f"M-10 -50 Q-4 {-50 - hgt*0.5} -7 {-50 - hgt} L7 {-50 - hgt} Q4 {-50 - hgt*0.5} 10 -50 Z", "#9FDCF5", "#3E8FB8", lw=3, a=0.95)
            g.circle(0, -50 - hgt, 9, "#9FDCF5", "#3E8FB8", lw=3)
        g.path(f"M{-w} -60 L{w} -60 L{w*0.8} 0 L{-w*0.8} 0 Z", col, INK, lw=LW)
        g.ellipse(0, -60, w, 22, shade(col, -0.25), INK, lw=LW)
        if water:
            g.ellipse(0, -56, w * 0.86, 15, "#7FCBEF", None)
            g.ellipse(-w * 0.3, -60, w * 0.25, 5, "#FFFFFF", None, a=0.6)
        g.text("WATER" if False else "", 0, -26, 30, PAL["cream"], stroke=None)
        if splash > 0.02:
            for i in range(9):
                a = -math.pi * (0.1 + 0.8 * i / 8)
                r = 60 + 160 * splash + 20 * math.sin(i * 7.1)
                g.ellipse(math.cos(a) * r * 1.3, -60 + math.sin(a) * r - 40 * math.sin(splash * 3.1), 9, 13, "#9FDCF5", "#3E8FB8", lw=3, a=1 - 0.6 * splash)


def sofa(g, x, y, w=900, col="#3E7CB1", cushion="#FFC93C"):
    """Sofa seen from the front, floor contact centre (x, y). Seat top at y-250."""
    with g.at(x, y):
        g.rc(0, -330, w, 300, shade(col, -0.12), INK, lw=LW, r=40)                  # back
        g.rc(0, -170, w + 40, 180, col, INK, lw=LW, r=30)                           # seat
        for sd in (-1, 1):
            g.rc(sd * (w / 2 + 20), -230, 110, 300, shade(col, -0.05), INK, lw=LW, r=40)
            g.rc(sd * (w / 2 - 40), -20, 30, 50, "#5A3A22", INK, lw=6, r=6)
        g.line([(0, -250), (0, -90)], shade(col, -0.25), 6)
        with g.at(w * 0.28, -300, 0.12):
            g.rc(0, 0, 200, 150, cushion, INK, lw=LW, r=40)


def scoreboard(g, x, y, dog=0, cat=0, t=0.0, flash=None, s=1.0, prev=None):
    """Big round scoreboard: DOG n : n CAT. flash = 'dog' | 'cat' | 'both' pulses that side; prev=(d, c) rolls the digits."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 760, 260, PAL["navy"], INK, lw=10, r=34)
        g.rc(0, 0, 720, 220, "#0B1A2B", None, r=26)
        for i, (lab, val, who) in enumerate((("DOG", dog, "dog"), ("CAT", cat, "cat"))):
            cx = -200 if i == 0 else 200
            on = flash in (who, "both")
            k = 0.5 + 0.5 * math.sin(t * 10) if on else 0
            if on:
                g.glow(cx, 10, 170, PAL["yellow"], 0.35 * k + 0.15)
            if who == "dog":
                dog_face(g, cx - 120, -2, 0.36, t, "happy", tongue=0.4)
            else:
                cat_face(g, cx + 120, 0, 0.4, t, "deadpan")
            g.text(str(val), cx + (40 if who == "dog" else -40), 18, 150, PAL["yellow"] if on else PAL["cream"], sw=12, sc=1 + 0.12 * k)
            g.text(lab, cx + (40 if who == "dog" else -40), -96, 34, PAL["mint"], stroke=None)
        g.text(":", 0, 6, 120, PAL["cream"], stroke=None)


def paw(g, x, y, s=1.0, col=INK, a=1.0, rot=0.0):
    with g.at(x, y, rot, s):
        g.ellipse(0, 14, 34, 28, col, None, a=a)
        for (dx, dy) in ((-34, -24), (-12, -42), (12, -42), (34, -24)):
            g.ellipse(dx, dy, 12, 15, col, None, a=a)


TOY_COLS = ["#FF6B5B", "#FFC93C", "#5ED3B5", "#3E7CB1", "#B05BD6", "#FF8A3D", "#7FCBEF"]


def toy(g, x, y, kind=0, s=1.0, rot=0.0):
    c = TOY_COLS[kind % len(TOY_COLS)]
    with g.at(x, y, rot, s):
        k = kind % 4
        if k == 0:
            g.circle(0, 0, 34, c, INK, lw=6); g.path("M-34 0 Q0 -20 34 0", None, "#FFFFFF", lw=5)
        elif k == 1:
            g.rc(0, 0, 80, 26, c, INK, lw=6, r=12); g.circle(-44, 0, 20, c, INK, lw=6); g.circle(44, 0, 20, c, INK, lw=6)
        elif k == 2:
            g.poly([(0, -38), (11, -12), (38, -12), (16, 6), (24, 34), (0, 18), (-24, 34), (-16, 6), (-38, -12), (-11, -12)], c, INK, lw=6)
        else:
            g.rc(0, 0, 60, 60, c, INK, lw=6, r=10); g.circle(0, 0, 10, "#FFFFFF", INK, lw=4)


def toy_pile(g, x, y, s=1.0, n=40, seed=3, glow_i=None, t=0.0):
    with g.at(x, y, 0, s):
        for i in range(n):
            r = (i * 7919 + seed * 104729) % 1000 / 1000.0
            r2 = (i * 6271 + seed * 1299709) % 1000 / 1000.0
            row = int(math.sqrt(i))
            xx = (r - 0.5) * (420 - row * 50)
            yy = -row * 34 - r2 * 20
            if glow_i == i:
                g.glow(xx, yy, 90, PAL["yellow"], 0.5 + 0.2 * math.sin(t * 8))
            toy(g, xx, yy, i, 0.9, r * 6)


def mouse(g, x, y, s=1.0, t=0.0, flip=False, squeak=0.0):
    with g.at(x, y, 0, -s if flip else s, s):
        g.path(f"M-40 -10 Q-90 {-10 + 8 * math.sin(t * 6)} -120 {-30 + 10 * math.sin(t * 6)}", None, "#C9A0A0", lw=6)
        g.path("M-50 0 Q-50 -50 0 -54 Q40 -54 60 -20 L76 -6 Q60 4 40 4 Z", "#B8B2B0", INK, lw=6)
        g.circle(14, -52, 18, "#D9C9C6", INK, lw=5); g.circle(14, -52, 9, "#FFB3A6", None)
        g.circle(46, -24, 5, INK, None)
        g.circle(76, -8, 5, "#FF8A9A", None)
        if squeak > 0.02:
            for k in range(3):
                g.path(f"M{92 + k * 18} {-30 - k * 10} Q{104 + k * 18} {-14} {92 + k * 18} {2 + k * 10}", None, PAL["yellow"], lw=5, a=squeak)


def bear_side(g, x, y, s=1.0, t=0.0):
    with g.at(x, y, 0, s):
        c, d = "#8A5A3A", "#5E3A22"
        for lx in (-150, 130):
            g.limb([(lx, -150), (lx + 4, -60), (lx, 0)], d, 70, lw=LW)
        g.path("M-230 -150 Q-240 -330 -60 -340 L120 -330 Q240 -300 230 -150 Q220 -60 120 -70 L-150 -70 Q-232 -70 -230 -150 Z", c, INK, lw=LW)
        g.path("M170 -300 Q250 -360 320 -300 Q360 -270 350 -230 Q330 -200 280 -205 Q210 -200 180 -230 Z", c, INK, lw=LW)
        g.circle(200, -330, 26, c, INK, lw=LW); g.circle(352, -238, 14, INK, None); g.circle(270, -280, 8, INK, None)
        for lx in (-180, 160):
            g.limb([(lx, -150), (lx + 4, -60), (lx, 0)], c, 76, lw=LW)


def baby_face(g, x, y, s=1.0, t=0.0, expr="happy"):
    with g.at(x, y, 0, s):
        g.circle(0, 0, 110, "#F6D5BC", INK, lw=LW)
        g.path("M-10 -110 Q20 -150 30 -112 Q14 -130 -10 -110 Z", "#7A3E1E", INK, lw=5)
        for sd in (-1, 1):
            g.circle(sd * 40, -10, 13, INK, None); g.circle(sd * 40 + 5, -15, 4, "#FFFFFF", None)
            g.circle(sd * 70, 30, 18, "#FF9A8A", None, a=0.4)
        g.path("M-26 40 Q0 66 26 40", None, INK, lw=6)


def speaker(g, x, y, s=1.0, t=0.0, on=0.0):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 140, 210, "#3A3A48", INK, lw=LW, r=18)
        g.circle(0, 40, 46, "#22222C", INK, lw=6); g.circle(0, 40, 16, "#5A5A6A", None)
        g.circle(0, -56, 22, "#22222C", INK, lw=5)
        if on > 0.02:
            for k in range(3):
                ph = (t * 1.5 + k / 3) % 1
                g.path(f"M{80 + 80 * ph} {-40 - 40 * ph} Q{110 + 100 * ph} 40 {80 + 80 * ph} {120 + 40 * ph}", None, PAL["yellow"], lw=8, a=on * (1 - ph))


def hs_camera(g, x, y, s=1.0, t=0.0, rec=True):
    """High-speed camera on a tripod (slow-motion study), facing right."""
    with g.at(x, y, 0, s):
        for a in (-0.3, 0, 0.3):
            g.line([(0, -260), (math.sin(a) * 160, 0)], "#3A3A48", 12)
        g.rc(0, -330, 220, 130, "#2F3A4F", INK, lw=LW, r=16)
        g.rc(140, -330, 80, 90, "#22222C", INK, lw=6, r=10)
        g.circle(160, -330, 30, "#5A7AA0", INK, lw=5)
        if rec and int(t * 2) % 2 == 0:
            g.circle(-80, -370, 12, "#FF3B3B", None)


def neuron_dots(g, x, y, n, cols=20, gap=26, r=8, col="#FFC93C", k=1.0, t=0.0):
    """A block of n dots (each dot = 10 million neurons), revealed left to right with k 0..1."""
    m = int(round(n * clamp(k)))
    for i in range(m):
        cx, cy = x + (i % cols) * gap, y - (i // cols) * gap
        g.circle(cx, cy, r, col, INK, lw=2)


def dna_tree(g, x, y, s=1.0, k=1.0, t=0.0, n=5):
    """Branching family tree from one wolf root into n dog lineages (k 0..1 grows it)."""
    with g.at(x, y, 0, s):
        g.limb([(0, 0), (0, -120 * clamp(k * 3))], "#8A5A3A", 22, lw=6)
        for i in range(n):
            kk = clamp(k * 1.6 - 0.3 - i * 0.06)
            if kk <= 0: continue
            ex = (i - (n - 1) / 2) * 150
            pts = [(0, -120), (ex * 0.4 * kk, -120 - 90 * kk), (ex * kk, -120 - 200 * kk)]
            g.limb(pts, "#8A5A3A", 16, lw=5)
            if kk > 0.95:
                dog_face(g, ex, -400, 0.28, t + i, "happy", tongue=0.3, col=dict(DOG, fur=["#D9A35E", "#3A3030", "#E8E0D0", "#B5652A", "#8C8C8C"][i % 5],
                         ear=["#8A5428", "#22181B", "#B8A890", "#7A3E1E", "#5A5A5A"][i % 5]))


def grain_jar(g, x, y, s=1.0, col="#C8875A"):
    with g.at(x, y, 0, s):
        g.path("M-60 0 Q-100 -90 -70 -170 L-40 -200 L40 -200 L70 -170 Q100 -90 60 0 Z", col, INK, lw=LW)
        g.rc(0, -204, 100, 20, shade(col, -0.2), INK, lw=6, r=6)
        g.path("M-70 -120 Q0 -100 70 -120", None, shade(col, -0.25), lw=6)
        for i in range(5):
            g.ellipse(-30 + i * 15, -214 - (i % 2) * 8, 7, 10, "#F2D27A", INK, lw=2)


def freq_bar(g, x, y, w, k_dog=0.0, k_cat=0.0, human=True, t=0.0, max_khz=90):
    """Horizontal hearing-range chart (kHz): human ~20, dog ~45, cat ~85. k_* 0..1 grow the bars."""
    with g.at(x, y):
        rows = []
        if human:
            rows.append(("YOU", 20, "#7FCBEF", 1.0))
        rows += [("DOG", 45, DOG["fur"], k_dog), ("CAT", 85, CAT["fur"], k_cat)]
        for i, (lab, khz, c, k) in enumerate(rows):
            yy = i * 120
            g.rc(-80, yy, 140, 70, PAL["navy"], None, r=14)
            g.text(lab, -80, yy + 3, 40, PAL["cream"], stroke=None)
            bw = w * khz / max_khz * clamp(k)
            if bw > 4:
                g.rect(0, yy - 30, bw, 60, c, INK, lw=6, r=14)
                if k > 0.9:
                    g.text(f"{khz},000", bw + 110, yy + 3, 44, PAL["yellow"], sw=8)
