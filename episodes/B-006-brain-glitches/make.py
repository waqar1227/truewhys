"""B-006 (L6) "Why You Forget Why You Walked Into a Room, Songs Get Stuck and Deja Vu Happens" — long video, Style F + cast v2.2, 1920x1080.
python episodes/B-006-brain-glitches/make.py sheet|qa|times <t,..> <out>|big <t,..>|chapters|animatic|render
Sets: home hallway + kitchen doorway, virtual-room grid, real-room boxes, night bedroom, survey lab, 1966 lecture hall, library, party room,
headphone lab, socket wall, MEG lab, NIMH monitors, desk + pocket, hospital corridor, lecture hall 2012, virtual town, scanner room.
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at, turn_at
from flat_fx import qmark, sparkles, arrow, burst, ring_wave, no_sign
from flat_brain import *

V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="curious", captions=False)
CH_PAUSE = 1.3
FL = 900                      # floor line in most rooms


# ------------------------------------------------------------------ helpers
def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def lt(c):
    """Time since the line's voice started (continues across split shots of the same line)."""
    return c.gt - c.V.voice0[c.sh["line"]]


def ld(c):
    return c.V.T[c.sh["line"]]["dur"]


def pk(c, word, n=0, frac=0.5, d=0.3):
    return pop(c.t, tw(c, word, n, frac) - 0.1, d)


def banner(g, c, txt, t0=0.0):
    t = c.t - t0
    if t > 2.8 or t < 0: return
    k = back_out(seg(t, 0, 0.35), 1.4) * (1 - ease_in(seg(t, 2.3, 0.4)))
    with g.screen():
        with g.at(80 - 900 * (1 - k), 96, -0.02):
            w = g.text_w(txt, 64) + 70
            g.rect(0, -46, w, 92, PAL["yellow"], INK, lw=8, r=18)
            g.text(txt, w / 2, 4, 64, INK, stroke=None)


def label(g, txt, x, y, size=70, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x, y, k=1.0, size=46):
    """Small context label (year/place): why_not_viral rule 2, context as a label while the story moves."""
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def studio(g, t, a="#1590A0", b="#0B3F4C", cx=None):
    cx = W / 2 if cx is None else cx
    g.fill_all(g.rgrad(cx, H * 0.45, W * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(cx, H * 0.45), (cx + 2400 * math.cos(a0), H * 0.45 + 2400 * math.sin(a0)),
                (cx + 2400 * math.cos(a0 + 0.1), H * 0.45 + 2400 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def check(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, PAL["mint"], INK, lw=r * 0.12)
        g.line([(-0.45 * r, 0), (-0.1 * r, 0.35 * r), (0.5 * r, -0.35 * r)], INK, r * 0.2)


def cross(g, x, y, r, k):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.8)):
        g.circle(0, 0, r, "#FF5B4B", INK, lw=r * 0.12)
        g.line([(-0.4 * r, -0.4 * r), (0.4 * r, 0.4 * r)], INK, r * 0.2); g.line([(-0.4 * r, 0.4 * r), (0.4 * r, -0.4 * r)], INK, r * 0.2)


def walker(g, cid, x, y, h, t, expr="deadpan", flip=False, pl="down", pr="down", moving=True, view=None, prop=False):
    """A character walking: small bob + arm swing while `moving`."""
    bob = abs(math.sin(t * 7)) * 10 if moving else 0
    if moving:
        sw = "hold" if math.sin(t * 7) > 0 else "down"
        pl = pl if pl != "down" else ("down" if sw == "hold" else "hold")
        pr = pr if pr != "down" else sw
    char2(g, cid, x, y - bob, h, expr, pl, pr, t=t, flip=flip, view=view, prop=prop)


def mug_icon(g, x, y, s=1.0):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 120, 130, "#FF6B5B", INK, lw=8, r=16)
        g.path("M60 -30 Q110 -30 110 10 Q110 50 60 40", None, INK, lw=14)
        g.path("M60 -30 Q110 -30 110 10 Q110 50 60 40", None, "#FF6B5B", lw=6)
        for i in range(3):
            g.line(f"M{-30 + i * 30} -90 q14 -20 0 -40", "#FFFFFF", 7, a=0.8)


def keys_icon(g, x, y, s=1.0):
    with g.at(x, y, 0.3, s):
        g.circle(-50, 0, 40, PAL["yellow"], INK, lw=7); g.circle(-50, 0, 14, INK, None)
        g.rect(-12, -10, 120, 20, PAL["yellow"], INK, lw=6)
        g.rect(80, 10, 16, 26, PAL["yellow"], INK, lw=5); g.rect(50, 10, 16, 20, PAL["yellow"], INK, lw=5)


def box_prop(g, x, y, s=1.0, col="#C8955A"):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 160, 120, col, INK, lw=7, r=6)
        g.line([(-80, -20), (80, -20)], shade(col, 0.75), 6)
        g.rc(0, -20, 40, 30, "#F4E3C2", INK, lw=4, r=3)


def table_s(g, x, y, w=300, col="#B97A4A", leg=180):
    g.rect(x - w / 2, y, w, 26, col, INK, lw=7, r=5)
    g.rect(x - w / 2 + 20, y + 26, 24, leg, shade(col, 0.75), INK, lw=6)
    g.rect(x + w / 2 - 44, y + 26, 24, leg, shade(col, 0.75), INK, lw=6)


def monitor(g, x, y, w=420, h=280, scr="#0B1F33"):
    g.rc(x, y, w, h, "#22181B", INK, lw=9, r=16)
    g.rc(x, y, w - 36, h - 36, scr, None, r=8)
    g.rect(x - 24, y + h / 2, 48, 50, "#5A5A6A", INK, lw=6)
    g.rc(x, y + h / 2 + 60, 200, 22, "#5A5A6A", INK, lw=6, r=8)


def worm(g, x, y, s=1.0, t=0.0, rot=0.0):
    """The 'earworm': a cute striped worm wearing headphones."""
    with g.at(x, y, rot, s):
        pts = [(-200 + 40 * i, 18 * math.sin(t * 6 + i * 0.9)) for i in range(9)]
        for i, (px, py) in enumerate(pts):
            g.circle(px, py, 40 - i * 1.2, "#F7A9BC" if i % 2 else "#F48FAA", INK, lw=6)
        hx, hy = pts[-1]
        g.circle(hx + 20, hy, 52, "#F7A9BC", INK, lw=7)
        g.circle(hx + 34, hy - 12, 11, INK, None); g.circle(hx + 30, hy - 16, 4, "#FFFFFF", None)
        g.line(f"M{hx + 22} {hy + 20} Q{hx + 40} {hy + 34} {hx + 60} {hy + 16}", INK, 6)
        g.line(f"M{hx - 20} {hy - 30} Q{hx + 20} {hy - 90} {hx + 60} {hy - 30}", INK, 12)
        g.rc(hx - 22, hy - 20, 26, 44, PAL["coral"], INK, lw=5, r=10)
        g.rc(hx + 64, hy - 20, 26, 44, PAL["coral"], INK, lw=5, r=10)


def staff(g, x0, x1, y, gap=34, col="#FFF4E0"):
    for i in range(5):
        g.line([(x0, y + i * gap), (x1, y + i * gap)], col, 4, a=0.7)


# ------------------------------------------------------------------ sets
def hallway(g, t, door_x=1180, light=1.0, wall="#E7D8C0", door_s=1.0):
    """Home hallway: striped wallpaper, picture frames, wooden floor, a doorway into a bright kitchen."""
    g.fill_all(g.lgrad(0, 0, 0, H, wall, shade(wall, 0.92)))
    with g.layer(0.6):
        for i in range(-2, 24):
            g.rect(i * 110, 0, 50, FL, shade(wall, 0.96), None)
        for i, (fx, fy, col) in enumerate(((300, 330, "#3E7CB1"), (560, 300, "#5ED3B5"), (1600, 320, "#FF6B5B"))):
            g.rect(fx - 80, fy - 60, 160, 120, "#7A5236", INK, lw=7)
            g.rect(fx - 62, fy - 42, 124, 84, col, None)
            g.poly([(fx - 62, fy + 42), (fx - 10, fy - 10), (fx + 30, fy + 20), (fx + 62, fy - 20), (fx + 62, fy + 42)], shade(col, 0.7), None)
    doorway(g, door_x, FL, door_s, 0.95, wall=wall, inside="#FFE7B0", light=light)
    with g.at(door_x, FL, 0, door_s):
        g.rect(10, -420, 110, 300, "#E8EEF2", INK, lw=6)          # fridge seen through the door
        g.circle(40, -300, 8, INK, None)
    g.rect(-100, FL, W + 200, H, "#B9844F", INK, lw=8)
    for i in range(-1, 14):
        g.line([(i * 170, FL), (i * 170 - 120, H)], "#9E6E3E", 5)


def kitchen2(g, t):
    """Warm evening kitchen (different from L5's morning kitchen): orange wall, fridge, hanging lamp."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#F2B880", "#E09A62"))
    with g.layer(0.55):
        g.rect(1350, 180, 300, 720, "#E8EEF2", INK, lw=10, r=16)
        g.line([(1350, 470), (1650, 470)], INK, 8)
        g.rect(1380, 300, 16, 120, "#9AA3AD", INK, lw=4); g.rect(1380, 520, 16, 160, "#9AA3AD", INK, lw=4)
        g.rect(-60, 520, 900, 40, "#3E7CB1", INK, lw=8)
        g.rect(-60, 560, 900, 340, "#2F5F8A", INK, lw=8)
        for i in range(4):
            g.rect(40 + i * 200, 600, 170, 260, "#3E6E9A", INK, lw=5, r=8)
        g.line([(700, 0), (700, 150)], INK, 6)
        g.path("M620 150 L780 150 L740 210 L660 210 Z", PAL["yellow"], INK, lw=7)
    g.glow(700, 260, 600, "#FFE08A", 0.25)
    g.rect(-100, FL, W + 200, H, "#D9C3A0", INK, lw=8)
    for i in range(-1, 14):
        for j in range(3):
            g.rect(i * 160 + (80 if j % 2 else 0), FL + j * 70, 156, 66, "#CDB38C", None, a=0.5)


def lab2(g, t, a="#3A3550", b="#221F33"):
    """Psychology lab: dark purple wall, pin board with brain diagrams, shelves."""
    g.fill_all(g.lgrad(0, 0, 0, H, a, b))
    with g.layer(0.5):
        for i in range(9):
            g.line([(i * 240, 0), (i * 240, FL)], shade(a, 0.9), 4)
        g.rect(1180, 150, 560, 320, "#C9A27A", INK, lw=10, r=10)
        for i, (px, py) in enumerate(((1290, 250), (1460, 230), (1620, 290), (1350, 380), (1560, 390))):
            g.rc(px, py, 120, 90, "#FFFDF6", INK, lw=5, r=4, rot=0.05 * (i - 2))
            g.circle(px, py - 40, 8, "#FF6B5B", INK, lw=3)
        brain(g, 1290, 255, 0.18, "happy")
        g.rect(120, 260, 380, 22, "#6E4A3A", INK, lw=6)
        for k in range(4):
            g.rc(170 + k * 90, 220, 50, 80, ("#5ED3B5", "#FFC93C", "#FF6B5B", "#BDEBFF")[k], INK, lw=5, r=10)
    g.rect(-100, FL, W + 200, H, "#2E2A40", INK, lw=8)


def bedroom_night(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#1E2440", "#2C2F4E"))
    with g.layer(0.5):
        g.rect(1300, 140, 380, 300, "#0F1630", INK, lw=10, r=8)
        g.circle(1560, 230, 46, "#FFF4E0", None, a=0.9)
        for (sx, sy) in ((1380, 200), (1430, 350), (1620, 380)):
            g.circle(sx, sy, 5, "#FFF4E0", None)
        g.line([(1490, 140), (1490, 440)], INK, 8)
        clock_face(g, 420, 230, 70, t * 4, 1.0)
    g.glow(700, 500, 700, "#FFC86A", 0.15)
    g.rect(-100, FL, W + 200, H, "#3A3550", INK, lw=8)


def lecture(g, t, board="#24433A", txt=None, year_style=True):
    """Lecture hall: chalkboard, wooden desks in front."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#C9B48A", "#A8925F"))
    with g.layer(0.55):
        g.rect(300, 120, 1320, 520, "#6E4A3A", INK, lw=10, r=8)
        g.rect(330, 150, 1260, 460, board, None)
        if txt:
            g.text(txt, 960, 300, 70, "#F4F1EA", stroke=None, a=0.9)
        g.line([(420, 420), (700, 380), (900, 450)], "#F4F1EA", 5, a=0.5)
        g.rect(300, 640, 1320, 20, "#8A5530", INK, lw=6)
    g.rect(-100, FL, W + 200, H, "#7A5236", INK, lw=8)


def party(g, t, warm=1.0):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3A2350", "#5B2D52"))
    with g.layer(0.5):
        for i in range(24):
            x = i * 90
            y = 90 + 40 * math.sin(i * 0.7)
            g.line([(x - 90, 90 + 40 * math.sin((i - 1) * 0.7)), (x, y)], INK, 4)
            g.circle(x, y + 14, 14, ("#FFC93C", "#FF6B5B", "#5ED3B5", "#BDEBFF")[i % 4], INK, lw=3, a=0.6 + 0.4 * math.sin(t * 3 + i))
        party_crowd(g, t, y=FL + 20, n=10, a=0.75, s=0.9)
    g.rect(-100, FL, W + 200, H, "#2A1A30", INK, lw=8)


def corridor(g, t):
    """Hospital corridor: pale green walls, handrail, doors with round windows."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#DDEFE6", "#C2DDD0"))
    with g.layer(0.55):
        for i, x in enumerate((240, 860, 1480)):
            g.rect(x, 280, 300, 620, "#9FC8B8", INK, lw=8, r=8)
            g.circle(x + 150, 420, 50, "#BDEBFF", INK, lw=6)
        g.rect(-60, 600, W + 120, 18, "#E8EEF2", INK, lw=5)
        g.rect(840, 120, 340, 70, "#3E8E7A", INK, lw=6, r=10)
        g.text("WARD", 1010, 158, 44, "#FFFFFF", stroke=None)
    g.rect(-100, FL, W + 200, H, "#B7C9C0", INK, lw=8)


def street_town(g, t, tint=0.0, ghost=0.0):
    """A small street: shops and houses, used for the deja vu scenes."""
    g.fill_all(g.lgrad(0, 0, 0, H, mix("#BFE6F2", "#B9A6E0", tint), mix("#E8F6FA", "#D9CCF2", tint)))
    with g.layer(0.5):
        for i, (x, col, hh) in enumerate(((120, "#FF8A6B", 420), (520, "#FFC93C", 500), (930, "#5ED3B5", 440), (1340, "#9FB8E8", 520), (1760, "#F7A9BC", 460))):
            g.rect(x - 180, FL - hh, 360, hh, col, INK, lw=8)
            g.poly([(x - 200, FL - hh), (x, FL - hh - 120), (x + 200, FL - hh)], shade(col, 0.7), INK, lw=8)
            g.rect(x - 120, FL - hh + 80, 90, 90, "#BDEBFF", INK, lw=6)
            g.rect(x + 30, FL - hh + 80, 90, 90, "#BDEBFF", INK, lw=6)
            g.rect(x - 50, FL - 180, 100, 180, shade(col, 0.6), INK, lw=6, r=8)
    g.rect(-100, FL, W + 200, H, "#9A9AA8", INK, lw=8)
    if ghost > 0:
        with g.group(0.22 * ghost):
            with g.at(26 * math.sin(t * 2), -10):
                for i, (x, col, hh) in enumerate(((120, "#FFFFFF", 420), (520, "#FFFFFF", 500), (930, "#FFFFFF", 440), (1340, "#FFFFFF", 520), (1760, "#FFFFFF", 460))):
                    g.rect(x - 180, FL - hh, 360, hh, None, "#FFFFFF", lw=10)
    if tint > 0:
        g.glow(W / 2, H / 2, 1200, "#B9A6E0", 0.2 * tint)


def scanner_room(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#DCE6EE", "#BFD0DC"))
    with g.layer(0.55):
        g.rect(1400, 160, 360, 240, "#22303A", INK, lw=8, r=10)
        g.rect(1420, 180, 320, 200, "#0B1F33", None)
        for i in range(5):
            g.line([(1440, 220 + i * 30), (1440 + 100 + 120 * abs(math.sin(t + i)), 220 + i * 30)], "#5ED3B5", 6)
    g.rect(-100, FL, W + 200, H, "#9FB0BC", INK, lw=8)


# ------------------------------------------------------------------ ch0 cold open + doorway
DOOR_X = 1080


def s_hook(g, c):
    """Frame 1: the student already walking through the doorway; the thought (a mug) is erased as he crosses; WHY AM I HERE?"""
    hallway(g, c.gt, door_x=DOOR_X, door_s=1.6)
    k = seg(c.gt, -0.5, 1.5)
    x = lerp(560, DOOR_X, ease_out(k))
    moving = k < 1
    expr = "deadpan" if k < 0.75 else ("curious" if c.gt < 1.5 else "shocked")
    walker(g, "student", x, FL + 10, 800, c.gt, expr, moving=moving, pl="down", pr="down" if moving else "think")
    # the thought bubble rides beside the head; crossing the door plane wipes it
    bx = x - 330
    thought(g, bx, 190, 300, 200, 1.0, tail=(1, 1))
    wipe = clamp((x - DOOR_X + 160) / 140)
    with g.group(1 - wipe):
        mug_icon(g, bx, 190, 0.7)
    if wipe > 0.6:
        qmark(g, bx, 190, 130, PAL["coral"], 0.1 * math.sin(c.gt * 3), pop(c.gt, 0.95, 0.3))
    with g.screen():
        g.text("WHY AM I HERE?", W / 2, 990, 130, PAL["yellow"], sw=22, depth=10, sc=pop(c.gt + 0.25, 0.0, 0.25))


def s_forget(g, c):
    hallway(g, c.gt, door_x=DOOR_X, door_s=1.6)
    char2(g, "student", 1150, FL + 600, 1500, "shocked" if c.t < c.T * 0.5 else "bored", "down", "think", t=c.gt, view="front")
    thought(g, 560, 260, 420, 280, 1.0, tail=(1, 1))
    qmark(g, 560, 260, 180, PAL["coral"], 0.15 * math.sin(c.gt * 2), 1.0)
    label(g, "WHY DID I COME IN?", 470, 960, 64, PAL["cream"], k=pk(c, "forget"))


def s_wiped(g, c):
    """Close on the doorway: a thought bubble slides through the frame and gets erased at the door plane."""
    studio(g, c.gt, "#2F6F8A", "#0B1F33")
    doorway(g, 960, 980, 1.6, 0.9, wall="#E7D8C0", inside="#FFE7B0", light=0.6)
    k = ease_io(seg(c.t, tw(c, "doorway") - 0.6, 1.4))
    bx = lerp(560, 1360, k)
    thought(g, bx, 420, 300, 200, 1.0, tail=(-1, 1))
    erase = clamp((bx - 900) / 240)
    with g.group(1 - erase):
        mug_icon(g, bx, 420, 0.7)
        keys_icon(g, bx + 10, 470, 0.5)
    if erase > 0:
        g.line([(960, 120), (960, 980)], "#FFFFFF", 14, a=0.6 * (1 - abs(erase - 0.5) * 2))
    label(g, "NOT BAD MEMORY", 480, 140, 64, PAL["cream"], k=pk(c, "memory"))
    if c.t > tw(c, "wiped") - 0.1:
        label(g, "THE DOORWAY?!", 1450, 140, 84, "#FF6B5B", k=pk(c, "wiped"))


def ic_song(g, c):
    note(g, -60, 0, 1.3, PAL["yellow"], 0.2 * math.sin(c.gt * 4)); note(g, 70, -40, 1.0, PAL["mint"], 0.2 * math.sin(c.gt * 4 + 1), double=True)
def ic_word(g, c):
    g.rc(0, 0, 300, 160, "#FFFFFF", INK, lw=8, r=30)
    g.poly([(-60, 70), (-100, 130), (-10, 76)], "#FFFFFF", INK, lw=7)
    g.text("A _ _ _ ?", 0, 6, 64, INK, stroke=None)
def ic_phone(g, c):
    phone(g, 0, 0, 1.0, 0.15 * math.sin(c.gt * 40), lit=0.0); buzz(g, 0, 0, 110, c.gt, 1.0)
def ic_door(g, c):
    doorway(g, 0, 160, 0.6, 0.9, inside="#FFE7B0")
def ic_name(g, c):
    g.rc(0, 0, 320, 120, "#FFFFFF", INK, lw=8, r=24); g.text("YOUR NAME!", 0, 6, 50, "#FF6B5B", stroke=None)
def ic_face(g, c):
    socket(g, 0, 0, 0.9, 0.5)
def ic_deja(g, c):
    with g.group(0.4): house_face(g, 30, 30, 0.7, "#B9A6E0")
    house_face(g, 0, 0, 0.7, "#B9A6E0")


def s_montage(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    for wd, x, fn in (("Songs", 420, ic_song), ("words", 960, ic_word), ("phone", 1500, ic_phone)):
        k = back_out(seg(c.t, tw(c, wd) - 0.15, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, 540, 0.06 * math.sin(c.gt * 2 + x), k):
            fn(g, c)
    label(g, "GLITCHES", 960, 150, 100, PAL["cream"], k=pk(c, "glitches"))


def s_shortcut(g, c, hard=False):
    lab2(g, c.gt)
    char2(g, "prof", 480, FL + 40, 760, "smug", "hold", "explain", t=c.gt)
    s = 1.3
    if hard:
        sq = 0.05 * math.sin(c.gt * 18)
        brain(g, 1180, 480, s, "worried", c.gt, squash=sq)
        for i in range(5):
            yy = 330 + i * 60
            g.line([(1450 + (c.gt * 900 + i * 90) % 300, yy), (1520 + (c.gt * 900 + i * 90) % 300, yy)], "#FFFFFF", 8, a=0.6)
        for i in range(3):
            g.ellipse(1000 + i * 40, 300 + ((c.gt * 200 + i * 60) % 160), 10, 16, "#BDEBFF", INK, lw=3)
        label(g, "TOO HARD!", 1180, 860, 80, "#FF6B5B", k=pk(c, "hard"))
    else:
        brain(g, 1180, 500, s, "happy", c.gt, glow=on(c, "lab"))
        label(g, "TESTED", 1180, 150, 84, PAL["cream"], k=pk(c, "tested"))


def s_start(g, c):
    hallway(g, c.gt, door_x=DOOR_X)
    char2(g, "student", 520, FL + 40, 880, "curious", "down", "point", t=c.gt)
    g.circle(DOOR_X, FL - 260, 330, None, PAL["yellow"], lw=10, a=0.7 * on(c, "doorway"))
    for i, (x, y) in enumerate(((900, 220), (1300, 200), (1100, 130))):
        qmark(g, x, y, 90, PAL["coral"], 0.2 * math.sin(i + c.gt), pop(c.t, 0.3 + i * 0.25, 0.3))


def s_radvansky(g, c):
    """2011: a generic psychologist at a computer showing virtual rooms (never the real person's likeness)."""
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    g.rect(760, 640, 1000, 40, "#7A5236", INK, lw=8, r=6)
    g.rect(800, 680, 40, 220, "#5B3B2E", INK, lw=7); g.rect(1680, 680, 40, 220, "#5B3B2E", INK, lw=7)
    char2(g, "engineer", 520, FL + 40, 820, "curious" if c.t < c.T * 0.6 else "smug", "explain", "point", t=c.gt)
    monitor(g, 1260, 470, 520, 320)
    with g.clip(rect=(1018, 328, 484, 284)):
        for i in range(-6, 7):
            g.line([(1260 + i * 8, 470), (1260 + i * 70, 612)], "#5ED3B5", 2, a=0.6)
        for j in range(5):
            g.line([(1018, 480 + j * 30), (1502, 480 + j * 30)], "#5ED3B5", 2, a=0.5)
        doorway(g, 1260, 480, 0.25, 0.9, wall="#5ED3B5", inside="#0B1F33", door="#1E5A64")
    tag(g, "2011 · NOTRE DAME, USA", 1500, 120, k=pk(c, "2011"))


def s_vr_room(g, c, door=True, walker_x=None, carry=True, quiz=0.0, who="student"):
    vr_grid(g, c.gt)
    table_s(g, 420, 640, 260, "#1E5A64", 120)
    table_s(g, 1500, 640, 260, "#1E5A64", 120)
    if door:
        doorway(g, 960, 860, 1.0, 1.0, wall="#5ED3B5", inside="#0B1F33", door="#1E5A64")
    u = seg(lt(c), 0.2, ld(c) - 1.2)
    x = walker_x if walker_x is not None else lerp(420, 1500, ease_io(u))
    walker(g, who, x, 930, 620, c.gt, "deadpan", moving=0 < u < 1)
    if carry:
        box_prop(g, x + 60, 930 - 360, 0.7)
    if quiz > 0:
        with g.screen():
            with g.at(960, 160, 0, back_out(clamp(quiz), 1.6)):
                g.rc(0, 0, 820, 120, "#FFFFFF", INK, lw=8, r=24)
                g.text("WHAT ARE YOU HOLDING?", 0, 6, 54, INK, stroke=None)


def s_d02(g, c):
    s_vr_room(g, c, quiz=on(c, "quizzed"))


def s_compare(g, c):
    """Split screen: same distance in one room (remembers) vs through a doorway (forgets)."""
    for side, x0 in ((0, 0), (1, 960)):
        with g.clip(rect=(x0, 0, 960, 1080)):
            with g.at(x0, 0):
                g.fill_all(g.lgrad(0, 0, 0, H, "#0B1F33", "#14304A"))
                for i in range(-8, 9):
                    g.line([(480 + i * 20, 460), (480 + i * 150, 1100)], "#5ED3B5", 3, a=0.5)
                g.line([(0, 460), (960, 460)], "#5ED3B5", 4, a=0.8)
                if side:
                    doorway(g, 480, 880, 0.8, 1.0, wall="#5ED3B5", inside="#0B1F33", door="#1E5A64")
                k = ease_io(seg(lt(c), 0.3, 2.2))
                x = lerp(140, 820, k)
                walker(g, "student", x, 960, 480, c.gt, "deadpan" if (k < 1 or not side) else "shocked", moving=0 < k < 1)
                box_prop(g, x + 50, 960 - 280, 0.55)
                if k >= 1:
                    (cross if side else check)(g, 820, 380, 60, seg(lt(c), 2.6, 0.3))
    g.line([(960, 0), (960, 1080)], INK, 12)
    label(g, "SAME ROOM", 480, 110, 70, PAL["cream"], k=pop(lt(c), 0.1, 0.3))
    label(g, "THROUGH A DOOR", 1440, 110, 70, PAL["yellow"], k=pop(lt(c), 0.25, 0.3))
    if c.t > tw(c, "forgot") - 0.1:
        label(g, "FORGOT MORE", 1440, 990, 80, "#FF6B5B", k=pk(c, "forgot"))


def real_room(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#E8E0D2", "#D6CBB8"))
    with g.layer(0.6):
        g.rect(1480, 150, 260, 200, "#BDEBFF", INK, lw=8)
        g.line([(1610, 150), (1610, 350)], INK, 6)
    g.rect(-100, FL, W + 200, H, "#9E8466", INK, lw=8)


def s_real(g, c):
    real_room(g, c.gt)
    doorway(g, 980, FL, 1.0, 1.0, wall="#E8E0D2", inside="#8A7A66")
    table_s(g, 380, 640, 280, "#B97A4A", 234)
    table_s(g, 1560, 640, 280, "#B97A4A", 234)
    for i in range(3):
        box_prop(g, 320 + i * 60, 580 - (i % 2) * 40, 0.55, ("#C8955A", "#B8854A", "#D8A56A")[i])
    u = seg(lt(c), 0.3, ld(c) - 1.0)
    x = lerp(400, 1520, ease_io(u))
    walker(g, "mira", x, FL + 30, 700, c.gt, "deadpan", moving=0 < u < 1)
    box_prop(g, x + 70, FL + 30 - 400, 0.7)
    label(g, "REAL ROOMS", 960, 130, 76, PAL["cream"], k=pk(c, "real"))
    check(g, 1560, 400, 60, pop(c.t, tw(c, "Same") - 0.1, 0.3))
    if c.t > tw(c, "result") - 0.2:
        label(g, "SAME RESULT", 1560, 260, 70, PAL["mint"], k=pk(c, "result"))


def s_chapters(g, c):
    """Life as a book of scenes: pages flip; a doorway on the page = NEW CHAPTER."""
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    with g.at(960, 560):
        g.rc(0, 0, 1100, 640, "#7A5236", INK, lw=10, r=20)
        g.rc(-270, 0, 520, 590, "#FFFDF6", INK, lw=6, r=8)
        g.rc(270, 0, 520, 590, "#FFFDF6", INK, lw=6, r=8)
        # left page: the hallway scene
        with g.at(-270, 40, 0, 0.42):
            g.rect(-500, -500, 1000, 700, "#E7D8C0", None)
            char2(g, "student", -150, 200, 700, "deadpan", "down", "down", t=None, breathe=False, blink=False)
            thought(g, -360, -320, 300, 200, 1.0, tail=(1, 1)); mug_icon(g, -360, -320, 0.7)
        # right page: the doorway
        with g.at(270, 40, 0, 0.42):
            doorway(g, 0, 300, 1.4, 0.9, inside="#FFE7B0")
        fk = ease_io(seg(c.t, tw(c, "new") - 0.5, 0.8))
        if 0 < fk < 1:
            w = 520 * math.cos(fk * math.pi)
            g.poly([(0, -295), (w, -295 - 30 * math.sin(fk * math.pi)), (w, 295 - 30 * math.sin(fk * math.pi)), (0, 295)], "#FFFDF6", INK, lw=6)
    label(g, "SCENES", 520, 130, 70, PAL["cream"], k=pk(c, "scenes"))
    if c.t > tw(c, "new") - 0.1:
        label(g, "NEW CHAPTER", 1400, 980, 90, PAL["yellow"], k=pk(c, "new"))


def s_filed(g, c):
    """The old plan (mug thought) slides into a filing drawer that shuts."""
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    with g.at(1100, 640):
        g.rc(0, 0, 420, 520, "#9AA3AD", INK, lw=10, r=12)
        k = ease_io(seg(c.t, tw(c, "filed") - 0.4, 0.7))
        out = 1 - k
        for i in range(3):
            g.rc(0, -170 + i * 170, 360, 140, "#B8C1CA", INK, lw=7, r=8)
            g.rc(0, -170 + i * 170, 80, 20, "#5A5A6A", INK, lw=4, r=6)
        g.rc(-160 * out, -170, 360, 140, "#C9D3DA", INK, lw=7, r=8)
        with g.at(-160 * out, -170 - 130 * (1 - ease_in(clamp(k * 1.4)))):
            thought(g, 0, -40, 240, 160, 1.0 - 0.3 * k)
            mug_icon(g, 0, -40, 0.55)
        g.rc(-160 * out, -170, 360, 140, None, INK, lw=7, r=8)
    char2(g, "student", 460, FL + 40, 820, "bored", "down", "shrug" if c.u > 0.6 else "down", t=c.gt)
    label(g, "FILED AWAY", 1100, 160, 80, PAL["cream"], k=pk(c, "filed"))


def s_australia(g, c):
    lab2(g, c.gt, "#2F4A3E", "#1A2C25")
    char2(g, "doctor", 560, FL + 40, 800, "suspicious", "hold", "explain", t=c.gt)
    char2(g, "physicist", 1400, FL + 40, 780, "curious", "down", "think", t=c.gt, flip=True)
    doorway(g, 980, FL, 0.8, 1.0, wall="#C2DDD0", inside="#1A2C25")
    qmark(g, 980, 300, 140, PAL["yellow"], 0.1 * math.sin(c.gt * 2), pk(c, "couldn't"))
    tag(g, "2021 · AUSTRALIA", 1500, 120, k=pk(c, "2021"))
    label(g, "NOT ALWAYS!", 980, 160, 84, "#FF6B5B", k=pk(c, "always"))


def s_busy(g, c):
    """Mind already busy (counting backwards) + doorway = slip."""
    vr_grid(g, c.gt, bg="#1A2C25")
    doorway(g, 960, 860, 1.0, 1.0, wall="#5ED3B5", inside="#0B1F33", door="#1E5A64")
    u = seg(c.t, 0.2, c.T - 0.4)
    x = lerp(380, 1420, ease_io(u))
    walker(g, "student", x, 930, 620, c.gt, "worried", moving=0 < u < 1)
    for i, n in enumerate(("100", "93", "86", "79", "72")):
        a = c.gt * 2 + i * TAU / 5
        g.text(n, x + 220 * math.cos(a), 360 + 70 * math.sin(a), 56, PAL["yellow"], sw=10)
    label(g, "MIND BUSY", 960, 140, 84, PAL["yellow"], k=pk(c, "busy"))


def s_kitchen_end(g, c):
    kitchen2(g, c.gt)
    k = ease_out(seg(lt(c), 0.0, 1.4))
    x = lerp(300, 760, k)
    walker(g, "modern", x, FL + 40, 760, c.gt, "curious" if k < 1 else "bored", moving=k < 1, pr="down" if k < 1 else "think")
    things = ("$", "@", "!", "9:00", "?", "★", "✉", "♪", "%", "#")
    spots = [(-560, 160), (-420, 70), (-300, 200), (-500, 330), (-330, 400), (300, 200), (420, 70), (560, 170), (480, 330), (330, 410)]
    for i, sym in enumerate(things):
        kk = pop(c.t, tw(c, "ten") - 0.4 + i * 0.06, 0.3)
        if kk <= 0: continue
        dx, dy = spots[i]
        with g.at(x + dx + 8 * math.sin(c.gt * 2 + i), dy + 8 * math.cos(c.gt * 2 + i), 0, kk):
            thought(g, 0, 0, 150, 100, 1.0)
            g.text(sym, 0, 4, 44, INK, stroke=None)
    label(g, "10 OTHER THINGS", 1350, 980, 80, PAL["coral"], k=pk(c, "ten"))


# ------------------------------------------------------------------ ch1 earworm
def notes_loop(g, cx, cy, r, t, n=6, k=1.0):
    for i in range(n):
        a = t * 1.6 + i * TAU / n
        note(g, cx + r * math.cos(a), cy + 0.45 * r * math.sin(a), 0.8 * k, (PAL["yellow"], PAL["mint"], PAL["coral"])[i % 3], 0.3 * math.sin(t * 4 + i), double=i % 2 == 1)


def s_stuck(g, c):
    banner(g, c, "WHY SONGS GET STUCK")
    bedroom_night(g, c.gt)
    g.rect(220, 640, 900, 120, "#5B6ED8", INK, lw=8, r=20)        # bed
    g.rect(220, 600, 260, 70, "#FFFDF6", INK, lw=7, r=20)
    char2(g, "mira", 1300, FL + 40, 860, "bored" if c.t < tw(c, "repeat") else "angry", "down", "think", t=c.gt, flip=True)
    notes_loop(g, 1300, 260, 260, c.gt, k=on(c, "song"))
    if c.t > tw(c, "repeat") - 0.2:
        arrow(g, 1580, 160, 1560, 380, PAL["coral"], 16, k=on(c, "repeat"))
        label(g, "ON REPEAT", 700, 260, 80, "#FF6B5B", k=pk(c, "repeat"))
    label(g, "WHY?", 700, 420, 100, PAL["yellow"], k=pk(c, "Why"))


def s_earworm(g, c):
    studio(g, c.gt, "#F7A9BC", "#8E2450")
    with g.at(1250, 560):                      # a big cartoon ear
        g.path("M-160 -260 Q120 -330 170 -60 Q200 120 40 200 Q-20 240 -40 300 Q-70 360 -150 320", "#E9BC98", INK, lw=12)
        g.path("M-90 -170 Q90 -200 100 -40 Q100 60 0 100", None, "#C99470", lw=12)
        g.circle(-40, 40, 50, "#5A3A2A", INK, lw=8)
    k = ease_io(seg(c.t, 0.2, c.T - 0.3))
    worm(g, lerp(300, 1090, k), lerp(760, 620, k), 0.9, c.gt, -0.2 * k)
    label(g, "EARWORM", 620, 180, 110, PAL["yellow"], k=pk(c, "earworm"))


def s_finland(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    # crowd of tiny figures
    for i in range(40):
        x = 260 + (i % 10) * 70; y = 420 + (i // 10) * 120
        col = PAL["yellow"] if (i * 7) % 12 != 0 else "#7A8A9A"
        kk = pop(c.t, tw(c, "survey") + i * 0.02, 0.25)
        if kk <= 0: continue
        with g.at(x, y, 0, kk):
            g.circle(0, -40, 18, col, INK, lw=4); g.rc(0, 0, 36, 50, col, INK, lw=4, r=12)
    pie(g, 1400, 540, 220, 0.917, PAL["yellow"], k=ease_out(seg(c.t, tw(c, "ninety") - 0.4, 0.9)))
    tag(g, "FINLAND · ~12,000 PEOPLE", 540, 230, k=pk(c, "Finland"))
    if c.t > tw(c, "ninety") - 0.1:
        label(g, "90%+", 1400, 540, 120, "#FFFFFF", k=pk(c, "ninety"), rot=0)
        label(g, "EVERY WEEK", 1400, 880, 70, PAL["cream"], k=pk(c, "week"))


def s_london(g, c):
    lab2(g, c.gt, "#3A3550", "#221F33")
    char2(g, "doctor", 480, FL + 40, 800, "curious", "hold", "explain", t=c.gt)
    for i in range(9):
        a = i * 0.7 + c.gt * 0.4
        x = 1200 + 380 * math.cos(a); y = 480 + 240 * math.sin(a * 1.3)
        with g.at(x, y, 0.2 * math.sin(a), pop(c.t, 0.3 + i * 0.12, 0.3) * 0.6):
            g.rc(0, 0, 180, 230, "#FFFDF6", INK, lw=6, r=8)
            note(g, 0, -30, 0.6, PAL["coral"])
            for j in range(3):
                g.line([(-60, 40 + j * 24), (60, 40 + j * 24)], "#9AA3AD", 4)
    tag(g, "2016 · LONDON", 1500, 120, k=pk(c, "2016"))
    label(g, "3,000 PEOPLE", 1200, 960, 80, PAL["yellow"], k=pk(c, "thousand"))


def s_tune(g, c, jumps=False):
    """Melody drawn on a staff: fast tempo (metronome) + a rise-and-fall contour; jumps=True adds big unusual leaps."""
    studio(g, c.gt, "#FFC93C", "#C97B2A")
    staff(g, 260, 1660, 480, 40, "#22181B")
    n = 12
    k = ease_io(seg(lt(c), 0.2, ld(c) * 0.8))
    for i in range(n):
        u = i / (n - 1)
        if u > k + 1e-3: break
        y = 600 - 240 * math.sin(u * math.pi)
        if jumps and i in (4, 8):
            y -= 220 if i == 4 else -140
        note(g, 300 + u * 1320, y, 0.9, PAL["coral"] if (jumps and i in (4, 8)) else PAL["cream"])
        if jumps and i in (4, 8):
            burst(g, 300 + u * 1320, y - 40, 60, 110, 8, "#FFFFFF", 6, k=pop(c.t, 0.4 + i * 0.1, 0.3))
    if not jumps:
        with g.at(1720, 840):                      # fast metronome
            g.poly([(-80, 120), (80, 120), (40, -120), (-40, -120)], "#7A5236", INK, lw=8)
            a = 0.5 * math.sin(c.gt * 12)
            g.line([(0, 100), (200 * math.sin(a), 100 - 220 * math.cos(a))], INK, 10)
        label(g, "FAST", 1720, 600, 80, "#FF6B5B", k=pk(c, "fast"))
        if c.t > tw(c, "climbs") - 0.1:
            label(g, "UP… AND DOWN", 960, 900, 80, PAL["cream"], k=pk(c, "climbs"))
    else:
        brain(g, 1680, 860, 0.6, "alarm", c.gt)
        label(g, "SURPRISE JUMPS", 960, 900, 80, "#FF6B5B", k=pk(c, "jumps"))


def s_gum(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    gum(g, 480, 560, 1.5, -0.2 + 0.05 * math.sin(c.gt * 2), out=0.15 + 0.7 * on(c, "chewing"))
    tag(g, "UNIVERSITY OF READING, UK", 520, 180, k=pk(c, "Reading"))
    # bar: song in your head
    with g.at(1320, 560):
        g.rc(0, 0, 640, 110, "#0B3F4C", INK, lw=8, r=20)
        kk = ease_io(seg(c.t, tw(c, "third") - 0.4, 0.8))
        w = 600 * (1 - kk / 3)
        g.rect(-300, -42, w, 84, PAL["yellow"], None, r=14)
        notes = int(5 * (1 - kk / 3) + 0.5)
        for i in range(5):
            note(g, -250 + i * 120, -140, 0.5, PAL["cream"] if i < notes else "#4A6A6A")
    label(g, "STRANGE FIX", 1320, 200, 80, PAL["cream"], k=pk(c, "fix"))
    if c.t > tw(c, "third") - 0.1:
        label(g, "−⅓", 1320, 820, 120, "#FF6B5B", k=pk(c, "third"))


def s_inner(g, c):
    studio(g, c.gt, "#9FB8E8", "#2F3A6F")
    brain(g, 700, 520, 1.5, "happy" if c.t < tw(c, "Chewing") + 1.2 else "confused", c.gt)
    for i in range(4):
        a = c.gt * 2 + i * 1.5
        brk = seg(c.t, tw(c, "busy") - 0.3, 0.6)
        note(g, 700 + 320 * math.cos(a), 220 + 60 * math.sin(a) + 300 * brk * ((i % 2) - 0.5), 0.7, PAL["yellow"], 0.4 * brk * (i - 1.5))
    with g.at(1400, 600):                        # chewing jaw
        o = 0.5 + 0.5 * math.sin(c.gt * 10)
        g.rc(0, -60, 340, 120, "#E9BC98", INK, lw=8, r=50)
        g.rc(0, 60 + 40 * o, 300, 100, "#E9BC98", INK, lw=8, r=46)
        g.rc(0, 10 + 20 * o, 200, 30 + 40 * o, "#7A2230", INK, lw=6, r=14)
    label(g, "INNER VOICE", 700, 960, 76, PAL["cream"], k=pk(c, "inner"))
    label(g, "CHEWING", 1400, 300, 76, PAL["yellow"], k=pk(c, "Chewing"))


def s_try_gum(g, c):
    bedroom_night(g, c.gt)
    o = 0.5 + 0.5 * math.sin(c.gt * 9)
    char2(g, "mira", 960, FL + 40, 880, "smug", "hold", "hip", t=c.gt)
    for i in range(5):
        y = 200 + ((c.gt * 120 + i * 90) % 500)
        note(g, 700 + i * 130, y, 0.6, PAL["yellow"], 0.6, )
    g.circle(1010, FL + 40 - 700 + 6 * o, 16, "#F7A9BC", INK, lw=4, a=pk(c, "gum"))
    label(g, "TRY GUM", 1450, 300, 100, PAL["mint"], k=pk(c, "gum"))


# ------------------------------------------------------------------ ch2 tip of the tongue
def s_tot_q(g, c):
    banner(g, c, "THE TIP-OF-THE-TONGUE FEELING")
    studio(g, c.gt, "#FF8A5B", "#5B2030", cx=600)
    char2(g, "student", 620, FL + 360, 1300, "worried" if c.t < tw(c, "something") else "angry", "down", "think", t=c.gt, view="front")
    letters = "?_?_?"
    for i, ch in enumerate(letters):
        a = c.gt * 1.2 + i * TAU / 5
        g.text(ch, 1350 + 330 * math.cos(a), 480 + 200 * math.sin(a), 120, PAL["cream"], sw=18)
    if c.t > tw(c, "starts") - 0.1:
        label(g, "IT STARTS WITH…", 1350, 900, 80, PAL["yellow"], k=pk(c, "starts"))


def s_harvard(g, c):
    lecture(g, c.gt, txt="TIP OF THE TONGUE")
    char2(g, "prof", 560, FL + 40, 800, "smug", "hold", "point", t=c.gt)
    char2(g, "engineer", 1400, FL + 40, 780, "curious", "down", "explain", t=c.gt, flip=True)
    tag(g, "1966 · HARVARD", 1500, 120 + 600, k=pk(c, "1966"))
    label(g, "ON PURPOSE", 960, 980, 80, PAL["yellow"], k=pk(c, "purpose"))


def desk(g, x, y):
    g.rect(x - 170, y, 340, 30, "#B97A4A", INK, lw=7, r=5)
    g.rect(x - 150, y + 30, 300, 150, "#8A5530", INK, lw=7)


def s_cards(g, c):
    lecture(g, c.gt)
    char2(g, "prof", 420, FL + 40, 760, "deadpan", "hold", "explain", t=c.gt)
    with g.at(600, 380, -0.1, 0.8 + 0.05 * math.sin(c.gt * 3)):
        g.rc(0, 0, 260, 170, "#FFFDF6", INK, lw=6, r=10)
        for j in range(4):
            g.line([(-100, -50 + j * 32), (100 - 50 * (j == 3), -50 + j * 32)], "#9AA3AD", 5)
    for i, (x, cid) in enumerate(((1150, "student"), (1580, "mira"))):
        char2(g, cid, x, FL - 20, 600, "worried" if c.t > tw(c, "stuck") else "curious", "down", "think", t=c.gt, flip=True)
        desk(g, x, 760)
    if c.t > tw(c, "stuck") - 0.2:
        label(g, "STUCK!", 1360, 200, 90, "#FF6B5B", k=pk(c, "stuck"))


def s_edge(g, c):
    """A word teetering on the very tip of a giant tongue (comic metaphor)."""
    studio(g, c.gt, "#F7A9BC", "#8E2450", cx=700)
    char2(g, "mira", 640, FL + 620, 1450, "worried", "down", "think", t=c.gt, view="front")
    wob = 0.08 * math.sin(c.gt * 5)
    reach = 0.5 + 0.5 * math.sin(c.gt * 2.2)
    with g.at(lerp(1150, 1080, reach), 520, wob):
        g.rc(0, 0, 380, 130, "#FFFFFF", INK, lw=8, r=24)
        g.text("? ? ? ? ?", 0, 6, 60, INK, stroke=None)
    arrow(g, 1500, 520, 1360, 520, PAL["yellow"], 14, k=0.8)
    label(g, "SO CLOSE", 1350, 260, 100, PAL["yellow"], k=pk(c, "edge"))


def s_guess(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    char2(g, "student", 420, FL + 40, 820, "curious", "down", "count", t=c.gt)
    with g.at(1200, 420):
        for i in range(7):
            x = -360 + i * 120
            g.rc(x, 0, 100, 130, "#FFFDF6", INK, lw=7, r=12)
        kk = pk(c, "first")
        if kk > 0:
            g.rc(-360, 0, 100, 130, PAL["yellow"], INK, lw=7, r=12)
            g.text("A?", -360, 6, 70, INK, stroke=None, sc=kk)
    for i in range(2):
        g.circle(1100 + i * 140, 720, 46, PAL["coral"], INK, lw=7, a=1.0 if pk(c, "syllables") > 0 else 0.0)
    label(g, "FIRST LETTER", 1200, 230, 70, PAL["yellow"], k=pk(c, "first"))
    label(g, "SYLLABLES", 1200, 860, 70, PAL["coral"], k=pk(c, "syllables"))


def s_meaning(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    brain(g, 960, 560, 1.6, "confused", c.gt)
    g.rc(560, 220, 360, 110, PAL["mint"], INK, lw=8, r=24); g.text("MEANING ✓", 560, 226, 50, INK, stroke=None)
    with g.group(1.0 if c.t > tw(c, "sound") - 0.2 else 0.3):
        g.rc(1360, 220, 360, 110, "#FF8A7A", INK, lw=8, r=24); g.text("SOUND ✗", 1360, 226, 50, INK, stroke=None)
    g.line([(740, 220), (1180, 220)], INK, 8, dash=([20, 20], 0))
    no_sign(g, 960, 220, 60, k=pk(c, "can't"))
    label(g, "NOT LOST", 960, 980, 90, PAL["yellow"], k=pk(c, "lost"))


def s_library(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#7A5236", "#5B3B2E"))
    for row in range(3):
        y = 230 + row * 290
        g.rect(160, y + 130, 1600, 24, "#4A3028", INK, lw=6)
        for i in range(22):
            gap = row == 1 and i == 13
            book(g, 210 + i * 70, y, 1.0, ("#3E7CB1", "#FF6B5B", "#5ED3B5", "#FFC93C", "#9FB8E8", "#C0504D")[(i + row) % 6], gap=gap)
    k = ease_io(seg(c.t, 0.2, 1.0))
    library_card(g, lerp(-200, 520, k), 780, 1.3, -0.1)
    if c.t > tw(c, "points") - 0.2:
        arrow(g, 700, 720, 1100, 560, PAL["yellow"], 18, k=on(c, "points"))
    if c.t > tw(c, "loan") - 0.1:
        label(g, "OUT ON LOAN", 1120, 140, 90, "#FF6B5B", k=pk(c, "loan"))
        g.circle(1120, 520, 90, None, PAL["yellow"], lw=10, a=0.8)


def s_aglet(g, c, reveal=False):
    studio(g, c.gt, "#FFC93C" if reveal else "#3E7CB1", "#C97B2A" if reveal else "#10263B")
    aglet_lace(g, 1000, 560, 2.2, -0.15, glow=1.0 if reveal else 0.4 + 0.3 * math.sin(c.gt * 4))
    if not reveal:
        label(g, "WHAT'S THIS CALLED?", 960, 160, 84, PAL["cream"], k=pop(c.t, 0.2, 0.3))
        clock_face(g, 1640, 880, 90, c.gt * 6, 1.0)
        arrow(g, 1500, 300, 1360, 480, PAL["yellow"], 16, k=on(c, "tip"))
    else:
        label(g, "AN AGLET!", 960, 180, 130, "#FF6B5B", k=pop(c.t, 0.05, 0.3))
        char2(g, "student", 330, FL + 40, 760, "smug", "down", "point", t=c.gt)
        label(g, "TIP OF YOUR TONGUE?", 1150, 960, 70, PAL["cream"], k=pk(c, "tongue"))


# ------------------------------------------------------------------ ch3 your name
def s_party(g, c, name=False):
    party(g, c.gt)
    char2(g, "mira", 760, FL + 40, 700, "curious", "hold", "explain", t=c.gt)
    char2(g, "student", 1150, FL + 40, 700, "smug", "down", "hip", t=c.gt, flip=True)
    for i in range(6):
        a = c.gt * 3 + i
        g.text(("blah", "ha!", "♪", "chat", "♪", "clink")[i], 300 + i * 260, 300 + 40 * math.sin(a), 46, "#FFFFFF", sw=8, a=0.55)
    if name:
        sound_wave(g, 1850, 300, 40, 1000, c.gt, PAL["yellow"], ang=math.pi, speed=1.4, a=on(c, "name"))
        if c.t > tw(c, "name") - 0.2:
            with g.screen():
                with g.at(1600, 230, 0, pk(c, "name")):
                    g.rc(0, 0, 380, 120, "#FFFFFF", INK, lw=8, r=26)
                    g.poly([(120, 50), (170, 120), (60, 58)], "#FFFFFF", INK, lw=7)
                    g.text("YOUR NAME!", 0, 6, 56, "#FF6B5B", stroke=None)
        label(g, "HOW?", 400, 200, 110, PAL["yellow"], k=pk(c, "How"))


def s_turn(g, c):
    """Close-up: Mira snaps her head towards her name."""
    party(g, c.gt)
    view, flip = turn_at(c.t, tw(c, "instantly") - 0.6, to_left=False)
    char2(g, "mira", 820, FL + 560, 1500, "shocked" if c.t > tw(c, "instantly") - 0.5 else "curious", "down", "down", t=c.gt, view=view, flip=flip)
    sound_wave(g, 1900, 380, 60, 900, c.gt, PAL["yellow"], ang=math.pi, speed=1.4)
    label(g, "INSTANTLY", 1450, 900, 90, PAL["yellow"], k=pk(c, "instantly"))


def s_cherry(g, c):
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    char2(g, "student", 960, FL + 40, 860, "deadpan", "down", "hold", t=c.gt, view="front")
    headphones(g, 960, FL + 40 - 760, 1.05)
    for side, col, x in ((-1, PAL["mint"], 360), (1, PAL["coral"], 1560)):
        for i in range(3):
            kk = pop(c.t, tw(c, "two") + i * 0.2 + (0.3 if side > 0 else 0), 0.3)
            if kk <= 0: continue
            with g.at(x, 300 + i * 140, 0, kk):
                g.rc(0, 0, 320, 90, col, INK, lw=7, r=20)
                g.text(("HELLO", "THE CAT", "SAT ON") [i] if side < 0 else ("MAY I", "TODAY IS", "LOOK AT")[i], 0, 6, 44, INK, stroke=None)
    tag(g, "1953 · BRITAIN", 1500, 1010, k=pk(c, "1953"))
    label(g, "REPEAT ONLY ONE", 960, 110, 70, PAL["cream"], k=pk(c, "repeat"))


def s_other_ear(g, c):
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    char2(g, "student", 960, FL + 40, 860, "bored", "down", "shrug" if c.u > 0.3 else "down", t=c.gt, view="front")
    headphones(g, 960, FL + 40 - 760, 1.05)
    sw = c.t > tw(c, "switched") - 0.2
    for i in range(3):
        with g.group(0.35):
            with g.at(1560, 300 + i * 140):
                g.rc(0, 0, 320, 90, "#9AA3AD", INK, lw=7, r=20)
                g.text(("GUTEN TAG", "WIE GEHT'S", "DANKE") [i] if sw else ("MAY I", "TODAY IS", "LOOK AT")[i], 0, 6, 40, INK, stroke=None)
    label(g, "BARELY A THING", 520, 300, 70, PAL["cream"], k=pk(c, "barely"))
    if sw:
        label(g, "NEW LANGUAGE?", 520, 520, 70, PAL["yellow"], k=pk(c, "switched"))
        label(g, "DIDN'T NOTICE", 520, 680, 80, "#FF6B5B", k=pk(c, "language"))


def s_moray(g, c):
    lab2(g, c.gt, "#3A3550", "#221F33")
    char2(g, "student", 760, FL + 40, 860, "deadpan" if c.t < tw(c, "name") + 0.4 else "shocked", "down", "hold", t=c.gt, view="front")
    headphones(g, 760, FL + 40 - 760, 1.05)
    for i in range(3):
        nm = i == 1
        with g.at(1400, 300 + i * 150):
            g.rc(0, 0, 400, 100, PAL["yellow"] if nm else "#9AA3AD", INK, lw=7, r=22)
            g.text("YOUR NAME" if nm else ("…TODAY…", "", "…LOOK…")[i], 0, 6, 48, INK, stroke=None)
            if nm:
                g.glow(0, 0, 260, PAL["yellow"], 0.35 * on(c, "name"))
    tag(g, "1959", 1700, 120, k=pk(c, "1959"))
    label(g, "IGNORED EAR", 1400, 900, 70, PAL["cream"], k=pk(c, "ignored"))


def s_third(g, c):
    studio(g, c.gt, "#3E7CB1", "#10263B")
    for row, (yy, wd) in enumerate(((330, "third"), (760, "1995"))):
        if row == 1 and c.t < tw(c, "1995") - 0.2: continue
        for i in range(6):
            lit = i in (1, 4)
            x = 520 + i * 180
            kk = pop(c.t, tw(c, wd) - 0.3 + i * 0.06, 0.3)
            if kk <= 0: continue
            with g.at(x, yy, 0, kk):
                col = PAL["yellow"] if lit else "#7A8A9A"
                g.circle(0, -60, 34, col, INK, lw=5); g.rc(0, 10, 70, 90, col, INK, lw=5, r=22)
                if lit: burst(g, 0, -60, 50, 80, 8, "#FFFFFF", 5, k=1)
        label(g, ("1959", "1995")[row], 260, yy - 20, 64, PAL["cream"], k=1.0 if row == 0 else pk(c, "1995"))
    label(g, "1 IN 3", 1640, 330, 110, PAL["yellow"], k=pk(c, "third"))
    if c.t > tw(c, "same") - 0.1:
        label(g, "SAME!", 1640, 760, 100, PAL["mint"], k=pk(c, "same"))


def s_filter(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    brain(g, 960, 760, 1.0, "smug", c.gt)
    with g.at(960, 470):
        g.path("M-320 -60 L320 -60 L120 120 L-120 120 Z", "#9AA3AD", INK, lw=9)
        for i in range(6):
            g.circle(-200 + i * 80, 0, 10, INK, None)
    words = ("blah", "noise", "chat", "clink", "♪", "ha!", "so…", "hmm")
    for i, wd in enumerate(words):
        u = (c.gt * 0.5 + i / len(words)) % 1.0
        x0 = 620 + i * 97
        y = lerp(180, 400, min(1, u * 1.6))
        bounce = max(0, u * 1.6 - 1)
        x = x0 + (x0 - 960) * 0.9 * bounce
        y -= 120 * math.sin(min(1, bounce) * math.pi)
        g.text(wd, x, y, 48, "#FFFFFF", sw=9, a=0.85 * (1 - bounce * 0.8))
    kn = (c.gt * 0.35) % 1.0
    ny = lerp(200, 680, ease_io(kn))
    g.text("YOUR NAME", 960, ny, 58, PAL["yellow"], sw=12, sc=1 - 0.3 * kn)
    if kn > 0.85:
        g.glow(960, 760, 260, PAL["yellow"], 0.5 * (kn - 0.85) / 0.15)
    label(g, "LISTENING TO ALL OF IT", 960, 110, 64, PAL["cream"], k=pk(c, "listening"))
    if c.t > tw(c, "matters") - 0.1:
        label(g, "LETS THROUGH WHAT MATTERS", 960, 1010, 56, PAL["yellow"], k=pk(c, "matters"))


def s_name_end(g, c):
    party(g, c.gt)
    char2(g, "mira", 760, FL + 40, 720, "smug", "down", "wave", t=c.gt)
    with g.at(1400, 400, 0.05 * math.sin(c.gt * 2), pk(c, "name")):
        g.rc(0, 0, 520, 280, "#FFFFFF", INK, lw=10, r=30)
        g.rect(-260, -140, 520, 90, "#FF6B5B", INK, lw=8)
        g.text("HELLO, MY NAME IS", 0, -94, 40, "#FFFFFF", stroke=None)
        g.text("YOU!", 0, 50, 100, INK, stroke=None)


# ------------------------------------------------------------------ ch4 faces in things
def wall_tiles(g, col="#CFE3E8"):
    g.fill_all(g.lgrad(0, 0, 0, H, col, shade(col, 0.9)))
    for i in range(-1, 16):
        for j in range(10):
            g.rect(i * 130 + (65 if j % 2 else 0), j * 110, 126, 106, shade(col, 1.08), None, r=8, a=0.7)


def s_socket(g, c):
    wall_tiles(g, "#E9DCC6")
    socket(g, 960, 560, 2.4, on(c, "face"))
    label(g, "SEE A FACE?", 960, 130, 110, "#FF6B5B", k=pk(c, "face"))


def s_gallery(g, c):
    studio(g, c.gt, "#9FB8E8", "#2F3A6F")
    for wd, x, fn in (("clouds", 360, lambda: cloud_face(g, 0, 0, 1.0, c.gt)), ("car", 960, lambda: car_face(g, 0, 40, 1.0)),
                      ("pizza", 1560, lambda: pizza_face(g, 0, 0, 1.0))):
        k = back_out(seg(c.t, tw(c, wd) - 0.15, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, 560, 0.05 * math.sin(c.gt * 2 + x), k):
            fn()
    label(g, "PAREIDOLIA", 960, 140, 110, PAL["yellow"], k=pop(c.t, 0.5, 0.3))


def s_meg(g, c):
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    char2(g, "mira", 640, FL + 40, 820, "deadpan", "down", "down", t=c.gt, view="front")
    meg_helmet(g, 640, FL + 40 - 640, 0.85, glow=on(c, "recorded"), t=c.gt)
    monitor(g, 1350, 480, 520, 340, "#E9DCC6")
    socket(g, 1350, 470, 0.9)
    tag(g, "2009 · HARVARD MEDICAL SCHOOL", 1300, 1010, k=pk(c, "2009"))


def s_sixth(g, c):
    studio(g, c.gt, "#2F6F8A", "#0B1F33")
    brain(g, 520, 520, 1.3, "alarm" if c.t > tw(c, "fired") else "happy", c.gt, glow=on(c, "fired"))
    with g.at(1260, 380):
        g.rc(0, 0, 900, 70, "#0B3F4C", INK, lw=8, r=30)
        kk = ease_out(seg(c.t, tw(c, "fired") - 0.3, 0.6))
        g.rect(-430, -24, 860 * 0.33 * kk + 1, 48, PAL["yellow"], None, r=16)
        g.text("0 s", -430, 80, 44, PAL["cream"], sw=8)
        g.text("0.5 s", 430, 80, 44, PAL["cream"], sw=8)
    label(g, "⅙ SECOND", 1260, 230, 90, PAL["yellow"], k=pk(c, "sixth"))
    with g.at(1260, 700):
        socket(g, -200, 0, 0.7, on(c, "fired"))
        check(g, -200, -140, 40, pk(c, "fast"))
        mug_icon(g, 200, 10, 0.8)
        cross(g, 200, -140, 40, pk(c, "Plain"))


def s_before_think(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    brain(g, 960, 600, 1.5, "shout", c.gt)
    with g.at(960, 220, 0, pk(c, "spotted")):
        g.rc(0, 0, 340, 120, "#FFFFFF", INK, lw=8, r=24); g.text("FACE!", 0, 6, 70, "#FF6B5B", stroke=None)
    if c.t > tw(c, "think") - 0.2:
        thought(g, 1560, 300, 320, 200, pk(c, "think"))
        g.text("hmm…", 1560, 306, 56, INK, stroke=None, a=pk(c, "think"))
    label(g, "BEFORE YOU THINK", 960, 990, 80, PAL["yellow"], k=pk(c, "before"))


def s_nimh(g, c):
    lab2(g, c.gt, "#1E3A4A", "#10263B")
    char2(g, "doctor", 460, FL + 40, 800, "curious", "hold", "point", t=c.gt)
    for i, x in enumerate((1000, 1500)):
        monitor(g, x, 470, 420, 300, "#0B1F33")
        for j in range(5):
            yy = 400 + j * 30
            g.line([(x - 170, yy), (x - 170 + 340 * abs(math.sin(c.gt * 2 + i + j)), yy)], "#5ED3B5", 6)
    tag(g, "2020 · NIMH, USA", 1500, 120, k=pk(c, "2020"))
    label(g, "IN MORE DETAIL", 1250, 980, 70, PAL["cream"], k=pk(c, "detail"))


def s_files(g, c):
    """The socket is first labelled FACE, then the label flips to OBJECT."""
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    socket(g, 700, 560, 1.8, 1.0 - on(c, "files"))
    fl = ease_io(seg(c.t, tw(c, "files") - 0.3, 0.5))
    sc = abs(math.cos(fl * math.pi))
    with g.at(1400, 560, 0, 1.0, max(0.02, sc)):
        g.rc(0, 0, 480, 180, "#FFFFFF", INK, lw=10, r=26)
        g.text("FACE" if fl < 0.5 else "OBJECT", 0, 8, 90, "#FF6B5B" if fl < 0.5 else "#3E7CB1", stroke=None)
    label(g, "SPLIT SECOND", 700, 140, 80, PAL["cream"], k=pk(c, "split"))


def s_detector(g, c):
    studio(g, c.gt, "#FFC93C", "#C97B2A")
    with g.at(600, 520):
        socket(g, 0, 0, 1.0)
        g.rc(0, 230, 300, 80, "#5ED3B5", INK, lw=8, r=20)
        g.text("FACE? YES", 0, 236, 40, INK, stroke=None)
        check(g, 160, -150, 50, pk(c, "eager"))
    with g.at(1320, 520):
        char2(g, "modern", 0, 200, 420, "smug", "down", "wave", t=c.gt)
        g.rc(0, 270, 300, 80, "#9AA3AD", INK, lw=8, r=20)
        g.text("FACE? NO", 0, 276, 40, INK, stroke=None)
        cross(g, 160, -230, 50, pk(c, "misses"))
    label(g, "BETTER SAFE", 960, 130, 100, INK, k=pk(c, "safer"))


# ------------------------------------------------------------------ ch5 phantom buzz
def office(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#BFD9E0", "#A6C6CF"))
    with g.layer(0.55):
        g.rect(1300, 140, 420, 300, "#E8F6FA", INK, lw=10, r=8)
        g.line([(1510, 140), (1510, 440)], INK, 8)
        g.rect(150, 200, 300, 200, "#FFFDF6", INK, lw=8)
        g.line([(190, 260), (400, 260)], "#9AA3AD", 6); g.line([(190, 310), (360, 310)], "#9AA3AD", 6)
        clock_face(g, 820, 220, 60, t * 2)
    g.rect(-100, FL, W + 200, H, "#6E7E88", INK, lw=8)


def s_buzz(g, c, check_=False):
    office(g, c.gt)
    char2(g, "mira", 820, FL + 300, 1180, "suspicious" if not check_ else ("bored" if c.t > tw(c, "Nothing") else "curious"),
          "down", "hold" if check_ else "down", t=c.gt, view="front", prop=False)
    if not check_:
        bz = 1.0 if 0.3 < c.t < 1.6 else 0.0
        buzz(g, 960, 830, 70, c.gt, bz)
        g.circle(960, 830, 60, None, PAL["yellow"], lw=8, a=0.6 * bz)
        label(g, "BZZZ!", 1300, 600, 90, PAL["yellow"], k=pop(c.t, 0.3, 0.3))
    else:
        phone(g, 1060, 560, 1.2, -0.1, lit=1.0, icon="none")
        if c.t > tw(c, "Nothing") - 0.1:
            label(g, "NOTHING.", 1450, 300, 100, "#FF6B5B", k=pk(c, "Nothing"))


def s_majority(g, c):
    studio(g, c.gt, "#9FB8E8", "#2F3A6F")
    cast = ("student", "doctor", "modern", "mira", "engineer")
    for i, cid in enumerate(cast):
        x = 300 + i * 330
        kk = pop(c.t, 0.2 + i * 0.12, 0.3)
        if kk <= 0: continue
        char2(g, cid, x, FL + 40, 620, ("shocked", "suspicious", "curious", "bored", "shocked")[i], "down", "hold", t=c.gt, prop=False, flip=i > 2)
        phone(g, x + (60 if i <= 2 else -60), FL + 40 - 300, 0.45, 0.1 * math.sin(c.gt * 40 + i))
        buzz(g, x + (60 if i <= 2 else -60), FL + 40 - 300, 50, c.gt, 0.8)
    label(g, "THE MAJORITY", 960, 130, 100, PAL["yellow"], k=pk(c, "majority"))


def s_hospital(g, c):
    corridor(g, c.gt)
    char2(g, "doctor", 520, FL + 40, 820, "suspicious", "hold", "hold", t=c.gt, prop=False)
    phone(g, 600, FL + 40 - 470, 0.5, 0.1)
    buzz(g, 600, FL + 40 - 470, 50, c.gt, 0.7 if (c.gt % 1.6) < 0.5 else 0)
    pie(g, 1380, 520, 220, 0.68, PAL["coral"], k=ease_out(seg(c.t, tw(c, "sixty-eight") - 0.4, 0.9)), bg="#5A6A70")
    if c.t > tw(c, "sixty-eight") - 0.1:
        label(g, "68%", 1380, 520, 120, "#FFFFFF", k=pk(c, "sixty-eight"), rot=0)
    tag(g, "2010 · US HOSPITAL", 1450, 120, k=pk(c, "2010"))
    label(g, "PHANTOM VIBRATIONS", 1380, 900, 64, PAL["navy"], k=pk(c, "phantom"))


def s_students(g, c):
    lecture(g, c.gt, board="#2F4A6A")
    for i, x in enumerate((300, 560, 820)):
        cid = ("student", "mira", "runner")[i]
        char2(g, cid, x, FL - 20, 560, "curious", "down", "hold", t=c.gt, prop=False)
        desk(g, x, 780)
        phone(g, x + 40, FL - 260, 0.35)
        buzz(g, x + 40, FL - 260, 40, c.gt, 0.8 if ((c.gt + i * 0.5) % 1.5) < 0.4 else 0)
    pie(g, 1450, 450, 220, 0.89, PAL["yellow"], k=ease_out(seg(c.t, tw(c, "eighty-nine") - 0.4, 0.9)))
    if c.t > tw(c, "eighty-nine") - 0.1:
        label(g, "89%", 1450, 450, 120, "#FFFFFF", k=pk(c, "eighty-nine"), rot=0)
    tag(g, "2012 · 290 STUDENTS", 1450, 820, k=pk(c, "2012"))


def s_waiting(g, c):
    office(g, c.gt)
    brain(g, 760, 520, 1.3, "worried", c.gt, look=(1, 0) if math.sin(c.gt * 2) > 0 else (-1, 0))
    with g.at(1380, 520, -0.05):
        g.rc(0, 0, 560, 260, "#FFFDF6", INK, lw=10, r=16)
        g.text("BETTER SAFE", 0, -40, 66, INK, stroke=None)
        g.text("THAN SORRY", 0, 50, 66, "#FF6B5B", stroke=None)
    phone(g, 760, 900, 0.5, 0.0)
    label(g, "WAITING FOR THE BUZZ", 960, 120, 70, PAL["coral"], k=pk(c, "waiting"))


def s_twitch(g, c):
    studio(g, c.gt, "#FF8A5B", "#8E2430")
    with g.at(560, 560):                              # leg + pocket close-up
        g.rc(0, 0, 360, 700, "#3A4A66", INK, lw=10, r=60)
        g.rc(40, -120, 200, 220, "#2E3B52", INK, lw=8, r=20)
        g.rc(40, -120, 110, 190, None, "#BDEBFF", lw=5, r=16, a=0.8)
        g.text("EMPTY", 40, -110, 30, "#BDEBFF", stroke=None)
        tw_ = 1.0 if (seg(c.t, tw(c, "twitch") - 0.1, 0.5) > 0 and seg(c.t, tw(c, "twitch") - 0.1, 0.5) < 1) else 0
        g.line([(-150, 160), (-110, 120), (-70, 170), (-30, 120), (10, 170), (50, 130)], PAL["yellow"], 10, a=tw_)
        k2 = seg(c.t, tw(c, "rubbing") - 0.1, 0.8)
        if 0 < k2 < 1:
            for i in range(3):
                g.line([(-150, -40 + i * 40 + 30 * math.sin(c.gt * 20)), (150, -40 + i * 40 + 30 * math.sin(c.gt * 20))], "#FFFFFF", 5, a=0.5)
    brain(g, 1350, 520, 1.4, "shout" if c.t > tw(c, "shouts") - 0.2 else "worried", c.gt)
    label(g, "TWITCH", 560, 120, 70, PAL["cream"], k=pk(c, "twitch"))
    if c.t > tw(c, "phone") - 0.1:
        label(g, "PHONE!", 1350, 140, 120, PAL["yellow"], k=pk(c, "phone"))


def s_hours(g, c):
    corridor(g, c.gt)
    with g.at(1000, 560):
        g.rect(-500, -300, 1000, 600, "#FFFDF6", INK, lw=10, r=20)
        for i in range(4):
            hh = 80 + i * 90
            kk = ease_out(seg(c.t, 0.3 + i * 0.25, 0.5))
            g.rect(-380 + i * 220, 220 - hh * kk, 140, hh * kk, (PAL["mint"], PAL["yellow"], PAL["coral"], "#C0504D")[i], INK, lw=6)
            if kk >= 1:
                buzz(g, -310 + i * 220, 200 - hh - 30, 30 + i * 4, c.gt, 0.4 + 0.2 * i)
        g.line([(-420, 230), (420, 230)], INK, 8)
        g.text("HOURS CARRIED →", 0, 280, 40, INK, stroke=None)
    label(g, "MORE PHANTOMS", 1000, 120, 80, "#FF6B5B", k=pk(c, "phantom"))
    with g.at(300, 400, 0, pk(c, "vibrate")):
        g.rc(0, 0, 200, 90, PAL["mint"], INK, lw=8, r=45)
        g.circle(50, 0, 34, "#FFFFFF", INK, lw=6)
        g.text("VIBRATE", 0, 90, 34, INK, sw=0, stroke=None)


def s_calm(g, c):
    office(g, c.gt)
    char2(g, "student", 560, FL + 40, 780, "smug", "down", "shrug", t=c.gt)
    brain(g, 1350, 480, 1.0, "sleepy" if c.t > tw(c, "eager") else "smug", c.gt)
    label(g, "90%: BARELY BOTHERED", 1350, 200, 70, PAL["navy"], k=pk(c, "ninety"))
    if c.t > tw(c, "eager") - 0.1:
        label(g, "JUST EAGER", 1350, 860, 80, PAL["coral"], k=pk(c, "eager"))


# ------------------------------------------------------------------ ch6 deja vu
def s_deja_walk(g, c):
    street_town(g, c.gt, tint=on(c, "sure"), ghost=on(c, "sure"))
    k = ease_out(seg(c.t, 0.0, 2.2))
    x = lerp(260, 900, k)
    walker(g, "mira", x, FL + 40, 760, c.gt, "curious" if c.t < tw(c, "sure") else "shocked", moving=k < 1, flip=False)
    if c.t > tw(c, "before") - 0.2:
        label(g, "BEEN HERE BEFORE?", 1300, 150, 84, PAL["yellow"], k=pk(c, "before"))


def s_deja_label(g, c):
    studio(g, c.gt, "#B9A6E0", "#3A2D6A")
    with g.at(560, 560):
        with g.group(0.35):
            with g.at(40 + 10 * math.sin(c.gt * 3), -30): house_face(g, 0, 0, 1.1, "#9FB8E8")
        house_face(g, 0, 0, 1.1, "#9FB8E8")
    label(g, "DÉJÀ VU", 560, 140, 120, PAL["yellow"], k=pop(c.t, 0.2, 0.3))
    pie(g, 1400, 500, 220, 0.6, PAL["yellow"], k=ease_out(seg(c.t, tw(c, "half") - 0.5, 0.9)))
    if c.t > tw(c, "half") - 0.1:
        label(g, "MORE THAN HALF", 1400, 860, 76, PAL["cream"], k=pk(c, "half"))


def s_cleary(g, c):
    lab2(g, c.gt, "#2F3E46", "#1E2A30")
    char2(g, "runner", 560, FL + 40, 820, "curious", "down", "explain", t=c.gt)
    with g.at(560, FL + 40 - 640):
        g.rc(0, 0, 220, 90, "#22181B", INK, lw=8, r=30)
        g.rc(0, 0, 180, 54, "#5ED3B5", None, r=20, a=0.6 + 0.3 * math.sin(c.gt * 4))
    monitor(g, 1300, 470, 600, 360, "#BFE6F2")
    with g.clip(rect=(1018, 308, 564, 324)):
        for i, (x, col) in enumerate(((1100, "#FF8A6B"), (1240, "#FFC93C"), (1380, "#5ED3B5"), (1520, "#9FB8E8"))):
            g.rect(x - 55, 480, 110, 150, col, INK, lw=5)
            g.poly([(x - 65, 480), (x, 430), (x + 65, 480)], shade(col, 0.7), INK, lw=5)
            g.rect(x - 15, 580, 30, 50, shade(col, 0.6), INK, lw=4)
    tag(g, "2012 · COLORADO STATE", 1450, 120, k=pk(c, "2012"))
    label(g, "VIRTUAL TOWN", 1300, 980, 76, PAL["cream"], k=pk(c, "virtual"))


def room_layout(g, x, y, kind, k_out=0.0):
    """Two different rooms with the SAME layout: furniture blocks at identical positions, different things."""
    with g.at(x, y):
        g.rc(0, 0, 640, 440, "#E9DCC6" if kind == 0 else "#BFE6F2", INK, lw=10, r=14)
        spots = ((-200, 100, 160, 120), (150, 110, 200, 100), (0, -110, 260, 90))
        for i, (sx, sy, w, h) in enumerate(spots):
            if kind == 0:
                g.rc(sx, sy, w, h, ("#B97A4A", "#3E7CB1", "#FFFDF6")[i], INK, lw=6, r=10)        # desk, sofa, shelf
            else:
                g.rc(sx, sy, w, h, ("#5ED3B5", "#FFC93C", "#9FB8E8")[i], INK, lw=6, r=40)       # tank, bench, counter
                if i == 0:
                    g.circle(sx - 20, sy, 12, PAL["coral"], INK, lw=3)
            if k_out > 0:
                g.rc(sx, sy, w + 20, h + 20, None, PAL["yellow"], lw=8, r=14, a=k_out)


def s_layout(g, c):
    studio(g, c.gt, "#2F6F8A", "#0B1F33")
    room_layout(g, 520, 520, 0, on(c, "layout"))
    room_layout(g, 1400, 520, 1, on(c, "layout"))
    label(g, "BEFORE", 520, 230, 64, PAL["cream"], k=1)
    label(g, "NEW", 1400, 230, 64, PAL["cream"], k=1)
    if c.t > tw(c, "shape") - 0.1:
        label(g, "SAME SHAPE", 960, 960, 90, PAL["yellow"], k=pk(c, "shape"))


def s_set_off(g, c):
    studio(g, c.gt, "#B9A6E0", "#3A2D6A")
    room_layout(g, 1250, 560, 1, 0.6)
    char2(g, "runner", 460, FL + 40, 800, "shocked", "down", "point", t=c.gt)
    sparkles(g, c.gt, [(1250, 300), (1500, 400), (1000, 700)], col=PAL["yellow"], r=30)
    label(g, "DÉJÀ VU!", 1250, 160, 100, PAL["yellow"], k=pop(c.t, 0.3, 0.3))
    with g.group(0.35 * on(c, "remember")):
        with g.at(800, 300, 0, 0.45):
            room_layout(g, 0, 0, 0)
    if c.t > tw(c, "remember") - 0.1:
        qmark(g, 800, 300, 120, PAL["coral"], 0.1, pk(c, "remember"))


def s_standrews(g, c):
    scanner_room(g, c.gt)
    mri(g, 900, 560, 1.0, slide=ease_io(seg(c.t, 0.3, 1.6)), glow=on(c, "scanner"))
    char2(g, "physicist", 1550, FL + 40, 760, "curious", "hold", "point", t=c.gt, flip=True)
    tag(g, "2016 · ST ANDREWS, SCOTLAND", 700, 120, k=pk(c, "2016"))


def s_front(g, c):
    studio(g, c.gt, "#2F3A6F", "#10263B")
    brain(g, 960, 560, 1.9, "confused", c.gt)
    with g.group(0.5 if c.t > tw(c, "weren't") else 1.0):
        g.rc(1300, 820, 320, 90, "#9AA3AD", INK, lw=7, r=20); g.text("MEMORY STORE", 1300, 826, 34, INK, stroke=None)
    kk = on(c, "front")
    g.glow(700, 400, 260, PAL["yellow"], 0.5 * kk)
    if kk > 0:
        with g.at(560, 300, -0.3, back_out(kk, 1.6)):
            g.circle(0, 0, 70, "#BDEBFF", INK, lw=12)
            g.line([(50, 50), (130, 130)], INK, 22)
        label(g, "CHECKER", 520, 140, 80, PAL["yellow"], k=pk(c, "check"))


def s_false_alarm(g, c):
    studio(g, c.gt, "#B9A6E0", "#3A2D6A")
    brain(g, 760, 560, 1.6, "alarm" if c.t < tw(c, "wait") else "smug", c.gt)
    with g.at(1400, 360, 0, pk(c, "familiar")):
        g.rc(0, 0, 420, 120, "#FFFFFF", INK, lw=8, r=24); g.text("FAMILIAR?", 0, 6, 60, INK, stroke=None)
    if c.t > tw(c, "wait") - 0.1:
        with g.at(1400, 640, -0.12, pop(c.t, tw(c, "wait") - 0.1, 0.3, 2.4)):
            g.rc(0, 0, 460, 140, None, "#FF5B4B", lw=14, r=20)
            g.text("NOPE", 0, 8, 100, "#FF5B4B", stroke=None)
    label(g, "FALSE ALARM", 760, 140, 90, PAL["yellow"], k=pk(c, "alarm"))


def s_good_sign(g, c):
    studio(g, c.gt, "#5ED3B5", "#0F6B78")
    brain(g, 760, 560, 1.5, "happy", c.gt, glow=0.6)
    check(g, 1250, 360, 90, pk(c, "good"))
    check(g, 1450, 560, 90, pk(c, "double-checks"))
    label(g, "A GOOD SIGN", 1350, 860, 90, PAL["cream"], k=pk(c, "good"))


# ------------------------------------------------------------------ ch7 ending
REC = [("doorway", ic_door), ("song", ic_song), ("word", ic_word), ("name", ic_name), ("face", ic_face), ("buzz", ic_phone), ("and", ic_deja)]


def s_recap(g, c):
    studio(g, c.gt)
    for i, (wd, fn) in enumerate(REC):
        x, y = ((330 + i * 420, 330) if i < 4 else (540 + (i - 4) * 420, 760))
        k = back_out(seg(c.t, tw(c, wd, n=(1 if wd == "and" else 0)) - 0.2, 0.35), 1.7)
        if k <= 0: continue
        with g.at(x, y, 0.05 * math.sin(c.gt * 2 + x), k * 0.85):
            fn(g, c)


def s_shortcuts(g, c):
    studio(g, c.gt, "#FFC93C", "#C97B2A")
    broken = c.t < tw(c, "But") - 0.1
    brain(g, 760, 560, 1.6, "worried" if broken else "smug", c.gt)
    if broken:
        with g.at(860, 420, 0.5):
            g.rc(0, 0, 180, 50, "#FFFDF6", INK, lw=6, r=10)
            g.circle(-40, 0, 6, "#C9B48A", None); g.circle(40, 0, 6, "#C9B48A", None)
        label(g, "BROKEN?", 1400, 400, 100, "#FF6B5B", k=pk(c, "broken"))
    else:
        arrow(g, 1150, 700, 1650, 360, PAL["coral"], 26, k=on(c, "shortcut"))
        label(g, "SHORTCUTS", 1400, 220, 100, INK, k=pk(c, "shortcut"))
        label(g, "WORKING TOO HARD", 1300, 900, 70, PAL["cream"], k=pk(c, "hard"))


def s_comments(g, c):
    hallway(g, c.gt, door_x=DOOR_X)
    char2(g, "student", 600, FL + 40, 700, "curious", "down", "point", t=c.gt)
    char2(g, "mira", 1500, FL + 40, 700, "smug", "hip", "wave", t=c.gt, flip=True)
    label(g, "WHICH ONE IS YOU?", 960, 140, 90, PAL["coral"], k=pk(c, "glitch"))
    for i, (x, y) in enumerate(((400, 330), (1100, 290), (1700, 330))):
        qmark(g, x, y, 100, PAL["coral"], 0.2 * math.sin(i + c.gt), pop(c.t, 0.4 + i * 0.25, 0.3))


def s_loop(g, c):
    """Callback to frame 1: the student stops in the doorway, the thought bubble empty."""
    hallway(g, c.gt, door_x=DOOR_X, door_s=1.6)
    k = seg(c.t, 0.0, 1.4)
    x = lerp(560, DOOR_X, ease_out(k))
    walker(g, "student", x, FL + 10, 800, c.gt, "curious" if k < 1 else "shocked", moving=k < 1, pr="down" if k < 1 else "think")
    thought(g, x - 330, 190, 300, 200, 1.0, tail=(1, 1))
    qmark(g, x - 330, 190, 130, PAL["coral"], 0.1 * math.sin(c.gt * 3), pop(c.t, 0.6, 0.3))


def s_endscreen(g, c):
    from flat_cast import wy_bust
    brand_bg(g, c.gt)
    k = back_out(seg(c.t, 0.0, 0.5), 1.5)
    g.text("TrueWhys", W / 2, 150, 150, PAL["cream"], sw=26, depth=10, sc=0.5 + 0.5 * k)
    g.text("The real story behind life's weirdest whys", W / 2, 250, 46, PAL["yellow"], sw=8, sc=k)
    for i, x in enumerate((560, 1360)):
        kk = back_out(seg(c.t, 0.25 + 0.15 * i, 0.45), 1.5)
        g.rc(x, 580, 640 * kk + 1, 360 * kk + 1, None, PAL["cream"], lw=8, r=22)
    wy_bust(g, c.gt, W / 2, H + 40 + (1 - k) * 600, 1.05, talk=0)
    check_badge(g, W / 2 + 170, 980, 52, pop(c.t, 0.8, 0.4, 2.4))


# ------------------------------------------------------------------ shot list
def P(lid, fn, part=(0, 1), **kw):
    if lid in V.T:                       # lines without a voice take yet (quota) are skipped in previews
        V.shot(lid, fn, part=part, **kw)


Z = lambda z0, z1, f: push(z0, z1, f)

# cold open + doorway (ch0)
P("O01", s_hook, (0, "and"), cam=Z(1.04, 1.1, (900, 560)), tr="cut", music="playful", sfx=[(0.0, "whoosh", 0.45), (1.0, "sting", 0.4)])
P("O01", s_forget, ("and", 1), cam=Z(1.0, 1.06, (900, 560)), sfx=[("forget", "bloop", 0.4)])
P("O02", s_wiped, cam=Z(1.0, 1.05, (960, 560)), sfx=[("wiped", "whoosh", 0.45)])
P("O03", s_montage, (0, "words"), cam=Z(1.0, 1.04, (900, 540)), sfx=[("Songs", "pop", 0.4), ("words", "pop", 0.4)])
P("O03", s_montage, ("words", 1), cam=Z(1.12, 1.18, (1150, 560)), sfx=[("phone", "buzz", 0.4)])
P("O04", s_shortcut, (0, "And"), cam=Z(1.0, 1.05, (900, 560)), sfx=[("lab", "shimmer", 0.35)])
P("O04", lambda g, c: s_shortcut(g, c, True), ("And", 1), cam=Z(1.15, 1.22, (1150, 520)), sfx=[("hard", "boing", 0.35)])
P("O05", s_start, cam=Z(1.0, 1.12, (1000, 560)), music="curious", sfx=[(0.1, "shimmer", 0.35)])
V.pause["O05"] = 0.6
P("D01", s_radvansky, (0, "built"), tr="flash", cam=Z(1.0, 1.04, (1000, 560)), music="story")
P("D01", s_radvansky, ("built", 1), cam=Z(1.4, 1.5, (1260, 470)), sfx=[("virtual", "shimmer", 0.35)])
P("D02", s_d02, (0, "were"), cam=Z(1.0, 1.04, (700, 600)), sfx=[(0.3, "footsteps", 0.25)])
P("D02", s_d02, ("were", 1), cam=Z(1.12, 1.18, (1100, 520)), sfx=[("quizzed", "ding", 0.4)])
P("D03", s_compare, (0, "forgot"), sfx=[(0.3, "footsteps", 0.25)])
P("D03", s_compare, ("forgot", 1), cam=Z(1.25, 1.3, (1440, 560)), sfx=[("forgot", "sting", 0.4)])
P("D04", s_real, cam=Z(1.0, 1.05, (1000, 560)), sfx=[("Same", "chime", 0.4)])
P("D05", s_chapters, (0, "A"), cam=Z(1.0, 1.04, (960, 560)), music="curious")
P("D05", s_chapters, ("A", 1), cam=Z(1.15, 1.22, (1100, 560)), sfx=[("new", "whoosh_soft", 0.4)])
P("D06", s_filed, cam=Z(1.0, 1.05, (960, 560)), sfx=[("filed", "thud", 0.4)])
P("D07", s_australia, (0, "The"), cam=Z(1.0, 1.04, (980, 560)), music="tension", sfx=[("couldn't", "drum_hit", 0.4)])
P("D07", s_busy, ("The", 1), cam=Z(1.0, 1.05, (960, 540)), sfx=[("busy", "bloop", 0.35)])
P("D08", s_kitchen_end, (0, "thinking"), cam=Z(1.0, 1.04, (800, 560)), music="playful", sfx=[(0.1, "door", 0.35)])
P("D08", s_kitchen_end, ("thinking", 1), cam=Z(1.12, 1.18, (900, 420)), sfx=[("ten", "pop", 0.4)])
V.pause["D08"] = CH_PAUSE
# earworm (ch1)
P("W01", s_stuck, (0, "and"), tr="flash", music="playful", cam=Z(1.0, 1.04, (900, 560)), sfx=[(0.2, "whoosh", 0.4)])
P("W01", s_stuck, ("and", 1), cam=Z(1.15, 1.22, (1150, 420)), sfx=[("Why", "sting", 0.35)])
P("W02", s_earworm, (0, "In"), cam=Z(1.0, 1.05, (960, 560)), sfx=[("earworm", "boing", 0.35)])
P("W02", s_finland, ("In", "more"), cam=Z(1.0, 1.04, (800, 560)), music="curious")
P("W02", s_finland, ("more", 1), cam=Z(1.12, 1.18, (1400, 600)), sfx=[("ninety", "ding", 0.4)])
P("W03", s_london, cam=Z(1.0, 1.05, (1100, 560)), music="story", sfx=[("thousand", "pop", 0.35)])
P("W04", s_tune, (0, "and"), cam=Z(1.1, 1.14, (1300, 600)), sfx=[("fast", "click", 0.35)])
P("W04", s_tune, ("and", 1), cam=Z(1.0, 1.03, (960, 560)), sfx=[("climbs", "shimmer", 0.35)])
P("W05", lambda g, c: s_tune(g, c, True), cam=Z(1.05, 1.1, (960, 520)), sfx=[("jumps", "boing", 0.4)])
P("W06", s_gum, (0, "chewing"), cam=Z(1.0, 1.04, (900, 560)), music="curious", sfx=[("fix", "sting", 0.35)])
P("W06", s_gum, ("chewing", 1), cam=Z(1.2, 1.26, (1320, 560)), sfx=[("third", "ding", 0.4)])
P("W07", s_inner, cam=Z(1.0, 1.05, (960, 560)), sfx=[("busy", "pop", 0.35)])
P("W08", s_try_gum, cam=Z(1.0, 1.08, (1000, 520)), music="warm", sfx=[("gum", "pop", 0.4)])
V.pause["W08"] = CH_PAUSE
# tip of the tongue (ch2)
P("T01", s_tot_q, (0, "But"), tr="flash", music="tension", cam=Z(1.0, 1.04, (800, 560)), sfx=[(0.2, "whoosh", 0.4)])
P("T01", s_tot_q, ("But", 1), cam=Z(1.2, 1.26, (700, 420)), sfx=[("come", "bloop", 0.35)])
P("T02", s_harvard, (0, "In"), cam=Z(1.2, 1.25, (960, 380)), music="story", sfx=[(0.2, "click", 0.3)])
P("T02", s_harvard, ("In", "decided"), cam=Z(1.0, 1.04, (960, 560)))
P("T02", s_harvard, ("decided", 1), cam=Z(1.15, 1.2, (900, 540)), sfx=[("purpose", "ding", 0.35)])
P("T03", s_cards, cam=Z(1.0, 1.05, (1000, 560)), sfx=[("stuck", "bloop", 0.4)])
P("T04", s_edge, cam=Z(1.0, 1.06, (1100, 600)), sfx=[("edge", "creak", 0.35)])
P("T05", s_guess, cam=Z(1.0, 1.04, (1000, 560)), music="curious", sfx=[("first", "pop", 0.35), ("syllables", "pop", 0.35)])
P("T06", s_meaning, (0, "Your"), cam=Z(1.0, 1.04, (960, 700)))
P("T06", s_meaning, ("Your", 1), cam=Z(1.1, 1.15, (960, 400)), sfx=[("sound", "bloop", 0.35)])
P("T07", s_library, cam=Z(1.0, 1.06, (1000, 560)), sfx=[("loan", "ding", 0.4)])
P("T08", s_aglet, cam=Z(1.0, 1.06, (1000, 560)), music="playful", sfx=[(0.2, "whoosh_soft", 0.35)])
V.pause["T08"] = 0.9
P("T09", lambda g, c: s_aglet(g, c, True), cam=Z(1.05, 1.0, (960, 560)), sfx=[(0.05, "chime", 0.45)])
V.pause["T09"] = CH_PAUSE
# your name (ch3)
P("N01", s_party, tr="flash", cam=Z(1.0, 1.06, (960, 560)), music="warm", sfx=[(0.2, "whoosh", 0.4)])
P("N02", lambda g, c: s_party(g, c, True), (0, "And"), cam=Z(1.06, 1.1, (1000, 560)), sfx=[("name", "sting", 0.4)])
P("N02", s_turn, ("And", 1), cam=Z(1.0, 1.04, (900, 560)), sfx=[("instantly", "whoosh_soft", 0.35)])
P("N03", s_cherry, (0, "played"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("N03", s_cherry, ("played", 1), cam=Z(1.1, 1.15, (960, 480)), sfx=[("repeat", "click", 0.35)])
P("N04", s_other_ear, cam=Z(1.0, 1.04, (900, 560)), sfx=[("switched", "bloop", 0.35)])
P("N05", s_moray, cam=Z(1.0, 1.05, (1100, 560)), music="curious", sfx=[("name", "ding", 0.4)])
P("N06", s_third, cam=Z(1.0, 1.03, (960, 560)), sfx=[("third", "pop", 0.4), ("same", "chime", 0.4)])
P("N07", s_filter, (0, "It's"), cam=Z(1.0, 1.04, (960, 560)), music="warm")
P("N07", s_filter, ("It's", 1), cam=Z(1.12, 1.18, (960, 520)), sfx=[("matters", "shimmer", 0.35)])
P("N08", s_name_end, cam=Z(1.0, 1.06, (1100, 560)), sfx=[("name", "pop", 0.4)])
V.pause["N08"] = CH_PAUSE
# faces (ch4)
P("F01", s_socket, tr="flash", cam=Z(1.0, 1.12, (960, 560)), music="playful", sfx=[(0.2, "whoosh", 0.4), ("face", "sting", 0.4)])
P("F02", s_gallery, cam=Z(1.0, 1.04, (960, 560)), sfx=[("clouds", "pop", 0.35), ("car", "pop", 0.35), ("pizza", "pop", 0.35)])
P("F03", s_meg, cam=Z(1.0, 1.05, (1000, 560)), music="story", sfx=[("recorded", "shimmer", 0.35)])
P("F04", s_sixth, (0, "Plain"), cam=Z(1.0, 1.04, (960, 560)), sfx=[("fired", "ding", 0.4)])
P("F04", s_sixth, ("Plain", 1), cam=Z(1.2, 1.26, (1260, 660)), sfx=[("Plain", "bloop", 0.35)])
P("F05", s_before_think, cam=Z(1.0, 1.06, (960, 560)), music="tension", sfx=[("spotted", "sting", 0.4)])
P("F06", s_nimh, cam=Z(1.0, 1.04, (1100, 560)), music="story")
P("F07", s_files, cam=Z(1.0, 1.04, (960, 560)), music="curious", sfx=[("files", "whoosh_soft", 0.4)])
P("F08", s_detector, cam=Z(1.0, 1.04, (960, 560)), sfx=[("eager", "ding", 0.35), ("misses", "bloop", 0.35)])
V.pause["F08"] = CH_PAUSE
# phantom buzz (ch5)
P("V01", s_buzz, (0, "You"), tr="flash", cam=Z(1.05, 1.1, (900, 600)), music="playful", sfx=[(0.3, "buzz", 0.45)])
P("V01", lambda g, c: s_buzz(g, c, True), ("You", 1), cam=Z(1.0, 1.05, (1000, 560)), sfx=[("Nothing", "bloop", 0.4)])
P("V02", s_majority, sfx=[("majority", "ding", 0.4)])
P("V03", s_hospital, cam=Z(1.0, 1.04, (1000, 560)), music="story", sfx=[("sixty-eight", "pop", 0.4)])
P("V04", s_students, cam=Z(1.0, 1.04, (1000, 560)), sfx=[("eighty-nine", "sting", 0.4)])
P("V05", s_waiting, cam=Z(1.0, 1.05, (960, 560)), music="curious")
P("V06", s_twitch, cam=Z(1.0, 1.05, (960, 560)), music="tension", sfx=[("twitch", "click", 0.35), ("phone", "sting", 0.45)])
P("V07", s_hours, cam=Z(1.0, 1.04, (1000, 560)), music="story", sfx=[("phantom", "pop", 0.35)])
P("V08", s_calm, cam=Z(1.0, 1.05, (1000, 560)), music="warm", sfx=[("eager", "pop", 0.35)])
V.pause["V08"] = CH_PAUSE
# deja vu (ch6)
P("J01", s_deja_walk, tr="flash", cam=Z(1.0, 1.06, (800, 560)), music="tension", sfx=[(0.2, "whoosh_soft", 0.4), ("sure", "shimmer", 0.4)])
P("J02", s_deja_label, cam=Z(1.0, 1.04, (960, 560)), sfx=[("half", "ding", 0.4)])
P("J03", s_cleary, (0, "sent"), cam=Z(1.0, 1.04, (960, 560)), music="story")
P("J03", s_cleary, ("sent", 1), cam=Z(1.3, 1.38, (1300, 480)), sfx=[("virtual", "shimmer", 0.35)])
P("J04", s_layout, cam=Z(1.0, 1.04, (960, 560)), music="curious", sfx=[("shape", "ding", 0.4)])
P("J05", s_set_off, cam=Z(1.0, 1.05, (900, 560)), sfx=[(0.3, "shimmer", 0.4)])
P("J06", s_standrews, cam=Z(1.0, 1.05, (1000, 560)), music="story", sfx=[("scanner", "whoosh_soft", 0.35)])
P("J07", s_front, cam=Z(1.0, 1.06, (900, 520)), sfx=[("front", "shimmer", 0.4)])
P("J08", s_false_alarm, cam=Z(1.0, 1.05, (1000, 560)), music="tension", sfx=[("wait", "drum_hit", 0.45)])
P("J09", s_good_sign, cam=Z(1.0, 1.05, (960, 560)), music="warm", sfx=[("good", "chime", 0.4)])
V.pause["J09"] = CH_PAUSE
# ending (ch7)
P("E01", s_recap, (0, "phantom"), cam=Z(1.0, 1.03, (960, 560)), tr="flash", music="warm",
  sfx=[("doorway", "pop", 0.35), ("song", "pop", 0.35), ("word", "pop", 0.35), ("name", "pop", 0.35), ("face", "pop", 0.35)])
P("E01", s_recap, ("phantom", 1), cam=Z(1.15, 1.2, (1500, 560)), sfx=[("buzz", "pop", 0.35)])
P("E02", s_shortcuts, cam=Z(1.0, 1.04, (960, 560)), sfx=[("shortcut", "whoosh_soft", 0.35)])
P("E03", s_comments, cam=Z(1.0, 1.05, (960, 560)), sfx=[("comments", "pop", 0.4)])
P("E04", s_loop, cam=Z(1.04, 1.1, (900, 560)), sfx=[(0.6, "bloop", 0.4)])
V.build()

END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line=V.shots[-1]["line"], fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "Why you forget why you walked into a room"), ("W01", "Why songs get stuck in your head"),
            ("T01", "Tip of the tongue: why you can't find a word"), ("N01", "Why you hear your name in a noisy room"),
            ("F01", "Why you see faces in things (pareidolia)"), ("V01", "Why your phone buzzes when it didn't"),
            ("J01", "What causes deja vu"), ("E01", "Every glitch is a shortcut")]


def chapters():
    out = []
    for lid, name in CHAPTERS:
        ts = [sh["start"] for sh in V.shots if sh["line"] == lid]
        if not ts: continue
        t = 0.0 if lid == "O01" else min(ts)
        out.append(f"{int(t // 60)}:{int(t % 60):02d} {name}")
    return out


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=10, scale=0.12))
    elif cmd == "qa":
        print(dict(duration=V.duration, shots=len(V.shots), max_shot=max(s["dur"] for s in V.shots if s["kind"] != "end")))
        for s in V.shots:
            if s["dur"] > 5.5 and s["kind"] != "end": print("long shot", s["id"], s["line"], round(s["dur"], 2))
    elif cmd == "times":
        V.qa_numbers()
        print(V.sheet(sys.argv[3], times=[float(x) for x in sys.argv[2].split(",")], cols=4, scale=0.3))
    elif cmd == "chapters":
        print("\n".join(chapters()))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "animatic":
        V.render(str(EP / "animatic/animatic.mp4"), crf=30, preset="veryfast")
    elif cmd == "render":
        V.render(str(EP / "final/B-006.mp4"))
