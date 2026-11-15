"""A-009 "Why You Should Never Shake a Vending Machine" — standalone Short, Style F + cast v2.1 (first new-standard Short, audit §6.3).
python episodes/A-009-vending-machine/make.py sheet|render|qa|big <t,t,..>
Respectful: no victims shown, the machine never lands on anyone; numbers appear on our own tally card (no real logos).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, sparkles, pain_marks, arrow, no_sign

V = Video(EP, title=("WHY YOU SHOULD NEVER", "SHAKE A VENDING MACHINE"), cap_y=0.70,
          keys={"stuck", "rocking", "bad", "1995", "killed", "thirtyseven", "37", "hundred", "injured", "free", "money", "lock", "tip", "nothing",
                "warning", "never", "fall", "protecting", "you", "walk"}, music="curious")

RED, RED2 = "#D23B3F", "#9E2530"
CANS = ["#FFC93C", "#3E8E5E", "#3E7CB1", "#FF6B5B", "#F4F1EA", "#7A4FB0"]


# ------------------------------------------------------------------ props and sets
def can(g, x, y, s, col, rot=0.0):
    with g.at(x, y, rot, s):
        g.rc(0, 0, 46, 84, col, INK, lw=6, r=8)
        g.rc(0, -36, 40, 10, "#C8CED6", INK, lw=4, r=3)
        g.rc(0, 4, 46, 18, "#FFFFFF", None, a=0.55)


def vending(g, x, y, s=1.0, tilt=0.0, t=0.0, stuck=True, xray=0.0, lock=0.0, blocked=0.0, sticker=0.0, glowk=0.0, drop=None):
    """Front view; (x, y) = bottom-left corner (the pivot when it tips left, tilt < 0 = towards screen left)."""
    w, h = 540, 1020
    with g.at(x, y, tilt, s):
        g.rect(4, -h + 14, w, h, INK, None, a=0.25)                      # shadow edge
        g.rect(0, -h, w, h, RED, INK, lw=10, r=26)
        g.rect(0, -h, w, 120, RED2, INK, lw=8, r=26)
        g.text("DRINKS", w * 0.40, -h + 62, 70, "#FFF4E0", sw=10, depth=4)
        # glass with rows of cans on coils
        gx, gy, gw, gh = 34, -h + 150, 340, 640
        g.rect(gx, gy, gw, gh, "#1C3F52", INK, lw=8, r=10)
        for r_ in range(4):
            yy = gy + 130 + r_ * 150
            for k in range(4):
                xx = gx + 50 + k * 80
                stuckhere = stuck and r_ == 1 and k == 2
                if stuckhere:
                    can(g, xx + 6, yy - 6 + 10, 1.0, CANS[(r_ + k) % 6], 0.35 + 0.05 * math.sin(t * 7))
                else:
                    can(g, xx, yy - 10, 1.0, CANS[(r_ * 2 + k) % 6])
                for j in range(5):                                         # coil
                    g.line([(xx - 30 + j * 13, yy + 34), (xx - 22 + j * 13, yy + 48)], "#C8CED6", 5)
            g.rect(gx + 8, yy + 46, gw - 16, 10, "#8796A3", None)
        g.rect(gx + 14, gy + 10, 40, gh - 20, "#FFFFFF", None, a=0.10, r=10)
        # keypad column
        g.rect(392, -h + 150, 116, 300, "#2A2A38", INK, lw=7, r=10)
        g.rect(406, -h + 168, 88, 44, "#5ED3B5", INK, lw=5, r=6)
        for i in range(3):
            for j in range(3):
                g.circle(420 + j * 30, -h + 250 + i * 50, 11, "#C8CED6", INK, lw=4)
        g.rect(410, -h + 480, 80, 110, "#2A2A38", INK, lw=6, r=8)        # coin slot plate
        g.rect(444, -h + 500, 12, 60, INK, None, r=4)
        # dispenser flap
        g.rect(60, -150, 300, 96, "#1A1A24", INK, lw=8, r=12)
        g.rect(70, -142, 280, 30, "#3A3A48", None, r=8)
        if drop is not None:
            can(g, 210, -100, 1.0, CANS[3], 1.57)
        if sticker > 0:
            k = back_out(clamp(sticker), 1.6)
            with g.at(w * 0.5, -h * 0.40, -0.06, 0.4 + 0.6 * k):
                g.rc(0, 0, 470, 300, "#FFC93C", INK, lw=9, r=18)
                g.text("WARNING!", 0, -96, 74, "#22181B", stroke=None)
                g.text("NEVER ROCK OR TILT", 0, -22, 44, "#22181B", stroke=None)
                g.text("MACHINE CAN FALL OVER", 0, 30, 38, "#22181B", stroke=None)
                with g.at(0, 100, 0, 0.5):                                 # tipping icon
                    g.rect(-40, -120, 80, 120, "#22181B", None, r=6)
                    with g.at(60, 0, -0.5):
                        g.rect(-40, -120, 80, 120, None, "#22181B", lw=8, r=6)
        if xray > 0:
            with g.group(xray):
                g.rect(0, -h, w, h, "#0E2A44", "#7FC8E8", lw=8, r=26)
                for i in range(1, 9):
                    g.line([(0, -h + i * h / 9), (w, -h + i * h / 9)], "#7FC8E8", 2, a=0.25)
                for r_ in range(4):
                    yy = -h + 280 + r_ * 150
                    g.line([(40, yy), (370, yy)], "#7FC8E8", 6, a=0.8)
                    for k in range(4):
                        g.rect(64 + k * 80, yy - 70, 46, 70, None, "#7FC8E8", lw=4, r=6)
                # the tilt lock: a pendulum that swings when the cabinet tips and bars the motor
                px, py = 230, -h + 800
                sw_ = -tilt * 2.6 * lock if lock else 0
                g.line([(px, py), (px, -h + 400), (440, -h + 360)], "#FFC93C", 6, a=0.7, dash=([18, 14], 0))
                g.circle(px, py, 14, "#FFC93C", INK, lw=4)
                with g.at(px, py, sw_):
                    g.line([(0, 0), (0, 120)], "#FFC93C", 14)
                    g.circle(0, 140, 46, "#FFC93C", INK, lw=7)
                g.text("TILT LOCK", px, py - 50, 40, "#FFC93C", stroke=None)
                g.rect(400, -h + 280, 100, 80, None, "#7FC8E8", lw=5, r=8)
                g.text("MOTOR", 450, -h + 322, 30, "#7FC8E8", stroke=None)
                if blocked > 0:
                    with g.at(450, -h + 320, 0, 0.6 + 0.4 * back_out(clamp(blocked))):
                        g.circle(0, 0, 70, None, "#FF3B30", lw=16)
                        g.line([(-48, -48), (48, 48)], "#FF3B30", 16)
        if glowk > 0:
            g.rect(0, -h, w, h, None, "#FFC93C", lw=18, r=26, a=glowk)


def corridor(g, t, tint=None):
    """Office/school corridor: cream wall, tiles, floor, a window strip; bright but not empty."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFE3B8", "#F7C98E"))
    with g.layer(0.55):
        for i in range(-1, 6):
            x = i * 260 + 40
            g.rect(x, 420, 200, 380, "#8FD3E8", INK, lw=8, r=12)
            g.line([(x + 100, 420), (x + 100, 800)], INK, 6)
            g.rect(x + 20, 440, 50, 340, "#FFFFFF", None, a=0.25, r=8)
        g.rect(-200, 860, W + 400, 26, "#E0A76A", INK, lw=6)
    g.rect(-200, 1560, W + 400, 600, "#B98A5E", INK, lw=8)
    for i in range(-2, 12):
        g.line([(i * 140, 1560), (i * 140 - 260, 1960)], "#9C7148", 6)
    if tint:
        g.fill_all(tint)


def office(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#CFE7EE", "#9CCAD8"))
    with g.layer(0.6):
        for i in range(3):
            g.rect(90 + i * 320, 380, 250, 330, "#F4F1EA", INK, lw=8, r=8)
            for j in range(4):
                g.line([(120 + i * 320, 440 + j * 60), (300 + i * 320, 440 + j * 60)], "#9AA3AD", 8)
    g.rect(-100, 1380, W + 200, 140, "#8A6A44", INK, lw=9)                 # desk
    g.rect(-100, 1520, W + 200, 600, "#6E5034", INK, lw=9)


def tally(g, x, y, n, label, col, k, icon="can"):
    """Our own tally card: big rolling number + label (no real logos)."""
    with g.at(x, y, -0.03, 0.5 + 0.5 * back_out(clamp(k), 1.5)):
        g.rc(0, 0, 820, 460, "#FFF4E0", INK, lw=12, r=30)
        g.rc(0, -170, 820, 120, col, INK, lw=12, r=30)
        g.text(label, 0, -168, 64, "#FFFFFF", sw=12)
        g.text(str(n), 0, 70, 250, col, sw=26, depth=10)


# ------------------------------------------------------------------ shots
MX = 560          # machine pivot x (bottom-left corner) in the corridor shots


def rock_angle(t, amp=0.10, f=1.6):
    return -amp * (0.5 + 0.5 * math.sin(TAU * f * t))


def s_hook(g, c):
    """Frame 1: object in action + character reacting, filling the frame."""
    corridor(g, c.gt)
    tilt = -0.05 - 0.04 * (0.5 + 0.5 * math.sin(TAU * 1.3 * c.gt))
    vending(g, MX - 40, 1720, 1.18, tilt, c.gt)
    char2(g, "modern", 300, 2010, 1320, "angry" if c.t < c.w("so") else "smug", "reach_r", "reach_r", t=c.gt)
    pain_marks(g, MX + 120, 520, 120, c.gt, n=3, col=PAL["yellow"], a0=-2.2, a1=-1.2, sc=0.9)


def s_rock(g, c):
    corridor(g, c.gt)
    tilt = rock_angle(c.gt, 0.12 + 0.05 * c.u, 1.8)
    vending(g, MX, 1640, 1.0, tilt, c.gt)
    char2(g, "modern", 330, 1830, 1060, "angry", "reach_r", "reach_r", t=c.gt, squash=0.03 * math.sin(TAU * 1.8 * c.gt))
    for i in range(3):
        a = -0.5 - i * 0.25
        g.line([(MX + 560 + 30 * i, 700 + 60 * i), (MX + 640 + 30 * i, 660 + 60 * i)], INK, 9, a=0.6)


def s_freeze(g, c):
    """'Bad idea.' Freeze at the tipping point: red tint, record scratch."""
    corridor(g, c.gt)
    vending(g, MX - 80, 1700, 1.08, -0.30, 0)
    char2(g, "modern", 280, 1960, 1200, "shocked", "up", "up", t=None)
    g.fill_all(rgba("#FF3B30", 0.20))
    pain_marks(g, 330, 760, 160, c.gt, n=5, col=PAL["yellow"], sc=1.2)


def s_official(g, c):
    office(g, c.gt)
    char2(g, "doctor", 560, 1960, 1250, "deadpan" if c.t < c.w("killed") else "worried", "down", "hold", t=c.gt)
    with g.screen():
        k = pop(c.t, c.w("1995") - 0.1, 0.32)
        g.text("1995", 270, 600, 150, PAL["yellow"], sw=28, depth=10, sc=k, rot=-0.08)


def s_tally37(g, c):
    office(g, c.gt)
    char2(g, "doctor", 820, 2050, 1150, "worried", "down", "hold", t=c.gt, flip=True)
    n = int(round(37 * ease_out(seg(c.t, 0.05, 1.1))))
    tally(g, 430, 980, n, "KILLED", "#B0413E", seg(c.t, 0.0, 0.4))


def s_tally113(g, c):
    office(g, c.gt)
    char2(g, "doctor", 820, 2050, 1150, "worried", "down", "hold", t=c.gt, flip=True)
    n = 37 + int(round((113 - 37) * ease_out(seg(c.t, 0.1, 0.9))))
    tally(g, 430, 980, n if c.t > 0.1 else 37, "INJURED", "#E07A2E", 1.0)


def s_motive(g, c):
    corridor(g, c.gt)
    vending(g, MX, 1640, 1.0, rock_angle(c.gt, 0.08, 1.6), c.gt)
    char2(g, "modern", 330, 1830, 1060, "smug", "reach_r", "reach_r", t=c.gt)
    # thought bubble: free drink, then the coin
    k = pop(c.t, 0.0, 0.3)
    with g.at(300, 560, 0, k):
        g.circle(0, 0, 150, "#FFFFFF", INK, lw=9)
        g.circle(110, 170, 26, "#FFFFFF", INK, lw=7); g.circle(140, 220, 14, "#FFFFFF", INK, lw=6)
        if c.t < c.w("money") - 0.05:
            can(g, 0, 0, 1.9, CANS[3], 0.2)
            g.text("FREE", 0, 110, 56, PAL["yellow"], sw=10)
        else:
            g.circle(0, 0, 70, "#FFC93C", INK, lw=9); g.text("$", 0, 4, 90, "#B07A1A", stroke=None)


def s_lock(g, c):
    """X-ray: the tilt lock."""
    g.fill_all(g.rgrad(540, 1100, 1300, "#1E5A74", "#0E2A44", "#081826"))
    tilt = -0.20 * ease_io(seg(c.t, c.w("tip") - 0.1, 0.6))
    vending(g, 270, 1640, 1.0, tilt, c.gt, xray=1.0, lock=1.0, blocked=seg(c.t, c.w("stops") - 0.1, 0.3))
    char2(g, "doctor", 950, 2040, 860, "smug", "down", "point", t=c.gt, flip=True)


def s_nothing(g, c):
    corridor(g, c.gt)
    vending(g, MX, 1640, 1.0, rock_angle(c.gt, 0.06, 1.2), c.gt)
    char2(g, "modern", 330, 1830, 1060, "bored", "reach_r", "reach_r", t=c.gt)
    with g.at(MX + 210, 1540):
        g.text("0", 0, 0, 120 * pop(c.t, 0.4, 0.3), "#FFFFFF", sw=20)


def s_sticker(g, c):
    corridor(g, c.gt)
    with g.layer(1.0):
        vending(g, 270, 1880, 1.25, 0.0, c.gt, sticker=seg(c.t, c.w("sticker") - 0.25, 0.4))
    char2(g, "doctor", 1000, 2080, 1000, "deadpan", "down", "point", t=c.gt, flip=True, prop=False)


def s_protect(g, c):
    corridor(g, c.gt)
    first = c.t < c.w("you") - 0.05
    vending(g, 520, 1700, 1.05, 0.0, c.gt, sticker=1.0)
    k = ease_out(seg(c.t, c.w("you") - 0.05, 0.35))
    if not first:
        g.glow(300, 1350, 620 * k, "#FFF4E0", 0.75)
        g.rings(300, 1350, 520 * k, "#FFC93C", a=0.12, n=3)
    char2(g, "modern", 300, 1960, 1200, "suspicious" if first else "worried", "down", "hold", t=c.gt)


def s_loop(g, c):
    """Matches frame 1 (loop): the same corridor, machine and man, hands hovering."""
    corridor(g, c.gt)
    vending(g, MX - 40, 1720, 1.18, -0.02, c.gt)
    late = c.t > c.w("walk") - 0.2
    char2(g, "modern", 300, 2010, 1320, "suspicious" if late else "curious", "reach_r" if not late else "hip", "reach_r" if not late else "hip", t=c.gt)


V.shot("H1", s_hook, part=(0, "So"), sfx=[(0.0, "creak", 0.5)])
V.shot("H1", s_rock, part=("So", 1), cam=push(1.0, 1.06, (540, 1100)), sfx=[("rocking", "creak", 0.6), (("rocking", 0.5), "thud", 0.4)])
V.shot("L01", s_freeze, part=(0, "By"), tr="flash", sfx=[(0.0, "freeze", 0.5), (0.05, "sting", 0.35)], music="tension")
V.shot("L01", s_official, part=("By", "at"), cam=push(1.0, 1.05, (560, 1200)))
V.shot("L01", s_tally37, part=("at", 1), sfx=[(0.1, "tick", 0.4), ("killed", "drum_hit", 0.45)])
V.shot("L02", s_tally113, sfx=[(0.1, "tick", 0.4)])
V.shot("L03", s_motive, cam=push(1.0, 1.07, (420, 900)), sfx=[(0.0, "bloop", 0.4), ("money", "coin_single", 0.5)], music="curious")
V.shot("L04", s_lock, tr="flash", cap_y=0.24, cam=push(1.0, 1.06, (600, 1100)), sfx=[(0.0, "zap", 0.35), ("tip", "creak", 0.4), ("stops", "click", 0.6)])
V.shot("L05", s_nothing, sfx=[("nothing", "hmm", 0.4)], music="playful")
V.shot("L06", s_sticker, cam=push(1.04, 1.0, (560, 1150)), sfx=[(("sticker", -0.2), "paper", 0.5)])
V.shot("L07", s_protect, part=(0, "It's"), sfx=[])
V.shot("L07", s_protect, part=("It's", 1), cam=push(1.0, 1.12, (320, 1100)), sfx=[("you", "shimmer", 0.4)])
V.shot("L08", s_loop, cam=push(1.0, 1.04, (540, 1100)), sfx=[("walk", "hmm", 0.3)])
V.build()

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=7, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-009.mp4"))
