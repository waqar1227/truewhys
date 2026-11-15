"""A-010 "Why Your Fingers Wrinkle but Your Face Doesn't" — standalone Short, Style F + cast v2.1 (audit §6.3).
python episodes/A-010-wrinkly-fingers/make.py sheet|render|qa|big <t,t,..>
Honest: the purpose of wrinkles is shown as an open question (2013 result vs 2014 replication).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from cast2 import CAST
from flat_fx import qmark, no_sign, sparkles, arrow, ring_wave

V = Video(EP, title=("WHY YOUR FINGERS WRINKLE", "BUT YOUR FACE DOESN'T"), cap_y=0.70,
          keys={"wrinkly", "face", "why", "swells", "nerve", "damaged", "smooth", "water", "purpose", "shrink", "grooves", "2013", "marbles",
                "twelve", "percent", "faster", "tyre", "berlin", "difference", "real", "argument", "fluke", "decide"}, music="curious")
SKIN = CAST["modern"]["skin"]
SKIN_D = shade(SKIN, 0.82)


# ------------------------------------------------------------------ props and sets
def bathroom(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#7FD1C9", "#4FB3B0"))
    with g.layer(0.6):
        for i in range(-2, 10):
            for j in range(0, 12):
                g.rect(i * 150 + (75 if j % 2 else 0), j * 150, 146, 146, "#8FDDD5", None, a=0.55, r=8)
        g.rect(780, 330, 220, 300, "#DFF4F6", INK, lw=8, r=110)          # round mirror
        g.rect(812, 362, 60, 230, "#FFFFFF", None, a=0.4, r=30)
    g.rect(-100, 1700, W + 200, 400, "#E6D3B3", INK, lw=8)                 # floor


def tub_back(g):
    g.ellipse(540, 1280, 560, 120, "#F4F1EA", INK, lw=10)
    g.ellipse(540, 1290, 500, 86, "#9BDDF0", None)


def tub_front(g, t):
    g.path("M-20 1280 Q-10 1760 160 1790 L920 1790 Q1090 1760 1100 1280 Z", "#FFFFFF", INK, lw=10)
    g.path("M40 1330 Q60 1700 200 1730", None, "#DCE6EA", lw=24)
    for i in range(12):                                                     # bubbles on the rim
        x = 40 + i * 92 + 10 * math.sin(t * 1.3 + i)
        g.circle(x, 1278 + 12 * math.sin(i * 2.1), 46 + 10 * math.sin(i * 1.7), "#FFFFFF", INK, lw=6)
    for i in range(5):
        y = 1180 - ((t * 60 + i * 90) % 400)
        g.circle(140 + i * 210, y, 14, None, "#FFFFFF", lw=5, a=0.7)


def big_hand(g, x, y, s=1.0, wr=1.0, rot=0.0, smooth_finger=None, nerve=0.0, cut=0.0, skin=SKIN):
    """Open hand, palm towards camera; (x, y) = wrist; wr = wrinkle amount 0..1 on the fingertips."""
    fingers = [(-120, -330, 54, 250, -0.16), (-40, -390, 56, 300, -0.05), (44, -385, 56, 296, 0.05), (124, -335, 52, 250, 0.16)]
    with g.at(x, y, rot, s):
        g.rc(0, 40, 170, 160, skin, INK, lw=9, r=40)                        # wrist
        g.path("M150 -120 Q240 -150 270 -230 Q296 -280 260 -300 Q220 -310 196 -250 Q170 -190 120 -170 Z", skin, INK, lw=9)   # thumb
        for i, (fx, fy, fw, fh, fr) in enumerate(fingers):
            with g.at(fx, -120, fr):
                g.rc(0, -fh / 2 + 20, fw * 1.6, fh, skin, INK, lw=9, r=fw * 0.8)
                k = 0 if smooth_finger == i else wr
                if k > 0:                                                   # wrinkles on the top segment
                    for j in range(5):
                        yy = -fh + 50 + j * 22
                        a = k * (1 - j * 0.12)
                        g.path(f"M{-fw * 0.55} {yy} Q{-fw * 0.25} {yy - 10 * k} 0 {yy} Q{fw * 0.25} {yy + 10 * k} {fw * 0.55} {yy}", None, SKIN_D, lw=6, a=a)
                    g.ellipse(0, -fh + 72, fw * 0.6, 40, None, SKIN_D, lw=5, a=0.6 * k)
                if nerve > 0:
                    col = "#FF3B30" if (cut > 0 and smooth_finger == i) else "#FFC93C"
                    g.line([(0, 60), (0, -fh + 60)], col, 10, a=nerve)
                    if cut > 0 and smooth_finger == i:
                        with g.at(0, -fh * 0.35, 0, back_out(clamp(cut))):
                            g.line([(-30, -30), (30, 30)], "#FF3B30", 14); g.line([(-30, 30), (30, -30)], "#FF3B30", 14)
        g.rc(0, -40, 330, 260, skin, INK, lw=9, r=70)                       # palm on top of the finger bases
        g.path("M-100 -60 Q0 -10 110 -80", None, SKIN_D, lw=6)
        g.path("M-60 30 Q20 50 90 -10", None, SKIN_D, lw=5)
        if nerve > 0:
            for (fx, _, _, _, _) in fingers:
                g.line([(0, 120), (fx * 0.6, -60), (fx, -120)], "#FFC93C", 10, a=nerve)


def section(g, x, y, s, shrink=0.0, fold=0.0, t=0.0, water=0.0):
    """Cross-section of a fingertip's skin: surface (top), skin layer, blood vessels below that shrink, surface folds into grooves."""
    w = 820
    with g.at(x, y, 0, s):
        pts = []
        for i in range(0, 41):
            xx = -w / 2 + i * w / 40
            pts.append((xx, -170 + fold * 46 * math.sin(i * math.pi / 4) ** 2 * (1 if i % 8 < 4 else 1)))
        top = " ".join(f"L{px:.1f} {py:.1f}" for px, py in pts)
        g.path(f"M{-w / 2} 260 {top.replace('L', 'L', 1)} L{w / 2} 260 Z".replace(f"M{-w / 2} 260 L", f"M{-w / 2} 260 L", 1), "#F2B9A0", INK, lw=10)
        inner = " ".join(f"L{px:.1f} {py + 70:.1f}" for px, py in pts)
        g.path(f"M{-w / 2} 260 {inner} L{w / 2} 260 Z", "#E89A86", None)
        for i in range(4):                                                  # blood vessels
            r = 46 * (1 - 0.55 * shrink)
            vx = -300 + i * 200
            g.ellipse(vx, 150, r * 1.5, r, "#C8323C", INK, lw=7)
            g.ellipse(vx - r * 0.4, 150 - r * 0.3, r * 0.4, r * 0.22, "#FF8A8A", None)
            if shrink > 0.05:
                for sd in (-1, 1):
                    arrow(g, vx + sd * (r * 1.5 + 60), 150, vx + sd * (r * 1.5 + 14), 150, "#FFF4E0", w=10, head=2.2, k=clamp(shrink * 3))
        g.line([(-w / 2, 230), (w / 2, 230)], "#FFC93C", 8, a=0.9)          # nerve
        if water > 0:
            for i in range(9):
                yy = -330 + ((t * 120 + i * 47) % 140)
                g.path(f"M{-360 + i * 90} {yy - 20} Q{-372 + i * 90} {yy} {-360 + i * 90} {yy + 6} Q{-348 + i * 90} {yy} {-360 + i * 90} {yy - 20} Z",
                       "#7FC8E8", INK, lw=4, a=water)
        g.text("SKIN", -w / 2 + 110, -60, 46, "#FFFFFF", sw=8)
        g.text("BLOOD VESSELS", 0, 250 + 70, 44, "#FFFFFF", sw=8)


def lab(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE9C7", "#F6CE8E"))
    with g.layer(0.6):
        g.rect(80, 320, 400, 260, "#FFFFFF", INK, lw=8, r=12)
        for j in range(4):
            g.line([(120, 380 + j * 50), (440, 380 + j * 50)], "#9AA3AD", 8)
        g.rect(600, 300, 380, 300, "#8FD3E8", INK, lw=8, r=12)
    g.rect(-100, 1380, W + 200, 120, "#8A6A44", INK, lw=9)
    g.rect(-100, 1500, W + 200, 600, "#6E5034", INK, lw=9)


MARB = ["#3E7CB1", "#FF6B5B", "#FFC93C", "#5ED3B5", "#7A4FB0"]


def bowls(g, t, k_move=0.0):
    for bx in (300, 780):
        g.ellipse(bx, 1360, 170, 50, "#FFFFFF", INK, lw=8)
        g.path(f"M{bx - 170} 1360 Q{bx - 150} 1450 {bx} 1456 Q{bx + 150} 1450 {bx + 170} 1360 Z", "#DCEFF5", INK, lw=8)
    n_left = int(round(7 * (1 - k_move)))
    for i in range(7):
        bx = 300 if i < n_left else 780
        j = i if i < n_left else i - n_left
        g.circle(bx - 90 + (j % 4) * 58, 1350 - (j // 4) * 34, 26, MARB[i % 5], INK, lw=5)
        g.circle(bx - 98 + (j % 4) * 58, 1342 - (j // 4) * 34, 7, "#FFFFFF", None, a=0.8)


def stopwatch(g, x, y, s, t, run=True):
    with g.at(x, y, 0, s):
        g.rc(0, -150, 50, 40, "#C8CED6", INK, lw=7, r=8)
        g.circle(0, 0, 140, "#FFFFFF", INK, lw=12)
        for i in range(12):
            a = i * TAU / 12
            g.line([(110 * math.cos(a), 110 * math.sin(a)), (125 * math.cos(a), 125 * math.sin(a))], INK, 6)
        a = (t * 2.2 if run else 0) - math.pi / 2
        g.line([(0, 0), (100 * math.cos(a), 100 * math.sin(a))], "#FF3B30", 10)
        g.circle(0, 0, 14, INK, None)


def tyre(g, x, y, s, t, wet=1.0):
    with g.at(x, y, 0, s):
        g.circle(0, 0, 220, "#2A2A38", INK, lw=12)
        for i in range(18):
            a = i * TAU / 18 + t * 2.0
            g.line([(170 * math.cos(a), 170 * math.sin(a)), (218 * math.cos(a), 218 * math.sin(a))], "#5A5A6A", 18)
        g.circle(0, 0, 110, "#9AA3AD", INK, lw=10)
        g.circle(0, 0, 40, "#5A5A6A", INK, lw=8)
        if wet:
            for i in range(6):
                k = ((t * 1.6 + i / 6) % 1.0)
                g.circle(-240 - 180 * k, 200 - 160 * k * (1 - k) * 3, 16 * (1 - k) + 4, "#7FC8E8", INK, lw=4, a=1 - k)


def sign(g, x, y, s, l1, l2):
    with g.at(x, y, -0.04, s):
        g.rc(0, 0, 560, 230, "#FFF4E0", INK, lw=10, r=24)
        g.text(l1, 0, -40, 92, "#22181B", stroke=None)
        g.text(l2, 0, 60, 70, "#B0413E", stroke=None)


def bubble(g, x, y, txt, k, col="#FFFFFF", tail=(-1, 1)):
    if k <= 0.01: return
    with g.at(x, y, 0, back_out(clamp(k), 1.6)):
        g.rc(0, 0, 380, 180, col, INK, lw=9, r=60)
        g.poly([(tail[0] * 60, 80), (tail[0] * 130, 170), (tail[0] * 120 + 60 * tail[0] * -1, 80)], col, INK, lw=9)
        g.rc(0, 0, 360, 160, col, None, r=56)
        g.text(txt, 0, 6, 76, "#22181B", stroke=None)


# ------------------------------------------------------------------ shots
def bath_scene(g, c, expr, hand_k=1.0, hand_s=1.15, hand_x=800, hand_y=1560, wr=1.0, pose=("down", "down")):
    bathroom(g, c.gt)
    tub_back(g)
    char2(g, "modern", 400, 2680, 2050, expr, pose[0], pose[1], t=c.gt)
    tub_front(g, c.gt)
    if hand_k > 0:
        big_hand(g, hand_x, hand_y + 300 * (1 - ease_out(clamp(hand_k))), hand_s, wr, rot=0.12 + 0.03 * math.sin(c.gt * 1.4))


def s_hook(g, c):
    """Frame 1: the object (giant wrinkly hand) + the character reacting, filling the frame."""
    bath_scene(g, c, "suspicious")
    sparkles(g, c.gt, [(700, 900), (880, 960)], r=26)


def s_face(g, c):
    bathroom(g, c.gt)
    tub_back(g)
    char2(g, "modern", 540, 2900, 2300, "curious" if c.t < c.w("why") - 0.1 else "shocked", "down", "down", t=c.gt)
    tub_front(g, c.gt)
    if c.t > c.w("why") - 0.1:
        qmark(g, 860, 760, 240, PAL["yellow"], 0.15, pop(c.t, c.w("why") - 0.1, 0.3))


def fingertip(g, wr, y0=330):
    """A big fingertip from the side at the top of the frame, with a magnifier ring pointing down to the section."""
    g.path(f"M-100 {y0 + 360} L-100 {y0 + 140} Q-100 {y0} 160 {y0} L700 {y0} L700 {y0 + 360} Z".replace("-100", "180").replace("700", "1200"), SKIN, INK, lw=10)
    for j in range(6):
        x = 320 + j * 70
        g.path(f"M{x} {y0 + 6} Q{x + 12} {y0 + 40 * wr + 10} {x} {y0 + 80 * wr + 14}", None, SKIN_D, lw=6, a=wr)
    g.circle(470, y0 + 120, 120, None, "#FFF4E0", lw=12)
    g.line([(400, y0 + 220), (220, 820)], "#FFF4E0", 8, a=0.8); g.line([(540, y0 + 220), (860, 820)], "#FFF4E0", 8, a=0.8)


def s_sponge(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    k = ease_io(seg(c.t, c.w("swells") - 0.3, 0.6))
    fingertip(g, 0.0)
    section(g, 540, 1320, 1.25 + 0.07 * k, 0.0, 0.0, c.gt, water=1.0)
    with g.screen():
        g.text("OLD IDEA", W / 2, 230, 110, PAL["cream"], sw=20, depth=8, sc=pop(c.t, 0.0, 0.3))
    for sd in (-1, 1):
        arrow(g, 540 + sd * 260, 1450, 540 + sd * (330 + 60 * k), 1450, "#FFF4E0", w=14, k=k)


def s_doctor(g, c):
    lab(g, c.gt)
    char2(g, "doctor", 260, 2050, 1180, "curious" if c.t < c.w("damaged") - 0.1 else "shocked", "down", "hold", t=c.gt)
    nk = ease_out(seg(c.t, c.w("nerve") - 0.2, 0.4))
    big_hand(g, 720, 1500, 1.25, 1.0, 0.05, smooth_finger=2, nerve=nk, cut=seg(c.t, c.w("damaged") - 0.1, 0.3))


def s_smooth(g, c):
    lab(g, c.gt)
    big_hand(g, 540, 1650, 1.9, 1.0, 0.0, smooth_finger=2, nerve=1.0, cut=1.0)
    g.glow(588, 900, 160, "#FFFFFF", 0.5 * ease_out(seg(c.t, c.w("smooth") - 0.2, 0.4)))
    sparkles(g, c.gt, [(600, 760), (520, 840)], r=30 * ease_out(seg(c.t, c.w("smooth") - 0.2, 0.3)))


def s_notwater(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    with g.at(540, 1050, 0, 1.0 + 0.04 * math.sin(c.gt * 3)):
        g.path("M0 -220 Q-170 30 -150 120 Q-120 240 0 240 Q120 240 150 120 Q170 30 0 -220 Z", "#7FC8E8", INK, lw=12)
        g.ellipse(-50, 80, 30, 60, "#FFFFFF", None, a=0.5, rot=0.3)
    no_sign(g, 540, 1080, 330, pop(c.t, c.w("water") - 0.1, 0.35))


def s_purpose(g, c):
    bathroom(g, c.gt)
    char2(g, "modern", 540, 2200, 1500, "smug", "hip", "hip", t=c.gt)
    k = ease_out(seg(c.t, c.w("purpose") - 0.3, 0.5))
    g.glow(540, 1050, 600 * k, "#FFC93C", 0.35)
    for i in range(6):                                                      # nerve signals running down the arms
        u = (c.gt * 0.9 + i / 6) % 1.0
        g.circle(540 + (1 if i % 2 else -1) * (120 + 150 * u), 1000 + 420 * u, 16, "#FFC93C", INK, lw=4, a=k)


def s_section(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#F7D6C4", "#E9A98E", "#B86A55"))
    sh = ease_io(seg(c.t, c.w("shrink") - 0.2, 0.7))
    fo = ease_io(seg(c.t, c.w("grooves") - 0.5, 0.8))
    fingertip(g, fo)
    section(g, 540, 1320, 1.25, sh, fo, c.gt)


def s_why(g, c):
    lab(g, c.gt)
    char2(g, "doctor", 540, 2150, 1400, "suspicious", "down", "hold", t=c.gt)
    qmark(g, 840, 700, 230, PAL["yellow"], 0.12, pop(c.t, 0.05, 0.3))
    with g.screen():
        g.text("2013", 250, 640, 150, PAL["yellow"], sw=28, depth=10, sc=pop(c.t, c.w("2013") - 0.1, 0.3), rot=-0.08)


def s_marbles(g, c, after=False):
    lab(g, c.gt)
    char2(g, "modern", 540, 2080, 1250, "curious" if not after else "smug", "down", "hold", t=c.gt, prop=False)
    km = (c.t / max(c.T, 0.1)) if not after else 1.0
    bowls(g, c.gt, km)
    stopwatch(g, 880, 620, 0.8, c.gt, run=not after)
    if not after:
        u = (c.gt * 1.1) % 1.0
        g.circle(lerp(300, 780, u), 1320 - 70 * math.sin(math.pi * u), 26, MARB[1], INK, lw=5)


def s_marbles2(g, c):
    s_marbles(g, c, True)
    with g.at(540, 860, -0.05, back_out(seg(c.t, c.w("twelve") - 0.15, 0.4), 1.6)):
        g.rc(0, 0, 640, 240, "#5ED3B5", INK, lw=12, r=36)
        g.text("12% FASTER", 0, 10, 110, "#FFFFFF", sw=18, depth=6)


def s_tyre(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#9FD8EE", "#4C93B5"))
    g.rect(-100, 1500, W + 200, 600, "#3A4250", INK, lw=9)
    g.rect(-100, 1500, W + 200, 30, "#7FC8E8", None, a=0.6)
    tyre(g, 300, 1280, 0.95, c.gt)
    big_hand(g, 790, 1700, 1.05, 1.0, 0.08)
    with g.screen():
        g.text("=", 545, 1170, 200, PAL["yellow"], sw=30, sc=pop(c.t, c.w("tyre") - 0.1, 0.3))


def s_berlin(g, c):
    lab(g, c.gt)
    char2(g, "doctor", 300, 2080, 1150, "deadpan", "down", "hold", t=c.gt, flip=False)
    sign(g, 720, 760, 1.0, "BERLIN", "2014")
    stopwatch(g, 760, 1250, 0.9, c.gt)


def s_nodiff(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    big_hand(g, 290, 1650, 0.95, 1.0, -0.1)
    big_hand(g, 800, 1650, 0.95, 0.0, 0.1)
    k = pop(c.t, c.w("difference") - 0.15, 0.35)
    with g.screen():
        g.text("=", 545, 1200, 260, PAL["yellow"], sw=36, sc=k)
        g.text("SAME GRIP", W / 2, 700, 120, PAL["cream"], sw=22, depth=8, sc=k)


def s_real(g, c):
    lab(g, c.gt)
    big_hand(g, 540, 1700, 1.7, 1.0, 0.0)
    with g.at(840, 760, 0, pop(c.t, c.w("real") - 0.1, 0.35)):
        g.circle(0, 0, 110, "#5ED3B5", INK, lw=12)
        g.line([(-50, 0), (-12, 40), (54, -40)], INK, 22)


def s_argue(g, c):
    lab(g, c.gt)
    char2(g, "doctor", 280, 2120, 1250, "smug", "down", "point", t=c.gt)
    char2(g, "modern", 800, 2120, 1250, "suspicious", "hip", "hip", t=c.gt, flip=True)
    bubble(g, 300, 640, "GRIP!", seg(c.t, c.w("argument") - 0.6, 0.3), tail=(1, 1))
    bubble(g, 780, 520, "FLUKE?", seg(c.t, c.w("argument") - 0.2, 0.3), "#FFE08A", tail=(-1, 1))


def s_loop(g, c):
    """Last shot = frame 1 (loop): same bath, hand and face."""
    bath_scene(g, c, "suspicious" if c.t < c.w("decide") - 0.3 else "smug")


V.shot("H1", s_hook, part=(0, "His#1"), sfx=[(0.0, "bloop", 0.4)])
V.shot("H1", s_face, part=("His#1", 1), cam=push(1.0, 1.06, (540, 900)), sfx=[("why", "hmm", 0.45)])
V.shot("L01", s_sponge, tr="flash", cap_y=0.475, sfx=[(0.0, "splash", 0.3), ("swells", "swell", 0.35)])
V.shot("L02", s_doctor, part=(0, "that"), cam=push(1.0, 1.05, (640, 1300)), sfx=[("nerve", "zap", 0.35), ("damaged", "sting", 0.35)])
V.shot("L02", s_smooth, part=("that", 1), cam=push(1.0, 1.08, (560, 950)), sfx=[("smooth", "shimmer", 0.45)])
V.shot("L03", s_notwater, part=(0, "It's"), sfx=[("water", "click", 0.5)])
V.shot("L03", s_purpose, part=("It's", 1), cam=push(1.0, 1.06, (540, 1000)), sfx=[("purpose", "swell", 0.35)])
V.shot("L04", s_section, cam=push(1.0, 1.06, (540, 1200)), tr="flash", cap_y=0.475, sfx=[("shrink", "melt", 0.4), ("grooves", "creak", 0.35)])
V.shot("L05", s_why, part=(0, "scientists"), music="playful", sfx=[(0.0, "hmm", 0.4)])
V.shot("L05", s_marbles, part=("scientists", 1), sfx=[(0.1, "tick", 0.4)])
V.shot("L06", s_marbles2, part=(0, "Like"), sfx=[("twelve", "ding", 0.5)])
V.shot("L06", s_tyre, part=("Like", 1), cam=push(1.0, 1.05, (540, 1250)), sfx=[(0.0, "whoosh", 0.4), ("tyre", "splash", 0.3)])
V.shot("L07", s_berlin, part=(0, "found"), cam=push(1.0, 1.04, (540, 1100)), sfx=[(0.0, "whoosh_soft", 0.4)])
V.shot("L07", s_nodiff, part=("found", 1), sfx=[("difference", "drum_hit", 0.4)])
V.shot("L08", s_real, part=(0, "Why"), sfx=[("real", "ding", 0.4)], music="curious")
V.shot("L08", s_argue, part=("Why", 1), sfx=[("argument", "pop", 0.5)])
V.shot("L09", s_loop, cam=push(1.0, 1.04, (540, 1300)), sfx=[(0.0, "bloop", 0.3)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=9, scale=0.15))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-010.mp4"))
