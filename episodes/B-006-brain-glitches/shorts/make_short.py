"""B-006 cut Short C1 "phantom phone buzz", re-composed vertically (1080x1920) with its own hook (not a crop of L6):
frame-1 rule (motion + sound at 0.0 s, face + object + <= 4-word question), answer at the end, last shot loops to the first, corner badge.
python episodes/B-006-brain-glitches/shorts/make_short.py C1 sheet|qa|times <t,..> <out>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, arrow, burst
from flat_brain import *

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-phantom"}
EP = HERE / DIRS[SID]
FL = 1560


def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def pk(c, word, n=0, frac=0.5):
    return pop(c.t, tw(c, word, n, frac) - 0.1, 0.3)


def label(g, txt, x, y, size=96, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def studio(g, t, a="#1590A0", b="#0B3F4C"):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


def office_v(g, t):
    g.fill_all(g.lgrad(0, 0, 0, H, "#BFD9E0", "#A6C6CF"))
    with g.layer(0.55):
        g.rect(600, 260, 400, 380, "#E8F6FA", INK, lw=10, r=8)
        g.line([(800, 260), (800, 640)], INK, 8); g.line([(600, 450), (1000, 450)], INK, 8)
        g.rect(80, 300, 300, 220, "#FFFDF6", INK, lw=8)
        g.line([(120, 370), (330, 370)], "#9AA3AD", 6); g.line([(120, 430), (290, 430)], "#9AA3AD", 6)
        clock_face(g, 260, 800, 70, t * 2)
    g.rect(-100, FL, W + 200, H, "#6E7E88", INK, lw=8)


def pocket_close(g, t, bz, empty=False):
    """Big close-up of a jeans pocket with the phone shape buzzing inside (or an empty pocket outline)."""
    studio(g, t, "#3E7CB1", "#10263B")
    with g.at(540, 1000):
        g.rect(-800, -1100, 1600, 2200, "#3A5A86", None)
        for i in range(-12, 13):
            g.line([(i * 60, -1100), (i * 60 + 80, 1100)], "#35537C", 4)
        g.rect(-800, -900, 1600, 120, "#2F4C74", INK, lw=10)                     # waistband
        for bx in (-420, 0, 420):
            g.rc(bx, -840, 60, 160, "#2F4C74", INK, lw=7, r=10)                   # belt loops
            g.line([(bx - 18, -900), (bx - 18, -770)], "#E0A040", 4, dash=([14, 10], 0))
        g.line([(-800, -770), (800, -770)], "#E0A040", 5, dash=([18, 12], 0))
        g.path("M-380 -770 Q-60 -560 380 -770", None, INK, lw=10)
        g.path("M-370 -700 L370 -700 L330 260 Q0 360 -330 260 Z", "#33507A", INK, lw=10)
        g.path("M-340 -660 L340 -660 L305 230 Q0 320 -305 230 Z", None, "#E0A040", lw=5)
        for rx in (-360, 360):
            g.circle(rx, -690, 16, "#C9A23A", INK, lw=5)
        sh = 10 * math.sin(t * 60) * bz
        if empty:
            g.rc(0, -120, 260, 420, None, "#BDEBFF", lw=8, r=30, a=0.8)
            g.text("EMPTY?", 0, -120, 60, "#BDEBFF", stroke=None)
        else:
            g.rc(sh, -120, 260, 420, "#25324A", "#1A2236", lw=8, r=34)
            g.glow(sh, -120, 260, PAL["yellow"], 0.25 * bz)
    buzz(g, 540, 880, 190, t, bz)


def c1_hook(g, c):
    """Frame 1 = motion already happening: the phone buzzing in the pocket (sound hit at 0.0 s) + Mira's suspicious face."""
    office_v(g, c.gt)
    bz = 1.0 if (c.gt % 1.0) < 0.75 else 0.3
    char2(g, "mira", 540, FL + 700, 1900, "suspicious", "down", "down", t=c.gt, view="front", prop=False)
    with g.at(780, 1500):
        g.rc(10 * math.sin(c.gt * 60) * bz, 0, 170, 270, "#25324A", PAL["yellow"], lw=8, r=24, a=0.95)
        g.glow(0, 0, 200, PAL["yellow"], 0.3 * bz)
    buzz(g, 780, 1500, 120, c.gt, bz)
    g.circle(780, 1500, 160, None, PAL["yellow"], lw=10, a=0.7 * bz)


def c1_nobody(g, c):
    pocket_close(g, c.gt, 1.0 if c.t < tw(c, "nobody") else 0.0)
    if c.t > tw(c, "nobody") - 0.2:
        label(g, "NOBODY CALLED", 540, 420, 110, "#FF6B5B", k=pk(c, "nobody"))


def c1_check(g, c):
    office_v(g, c.gt)
    char2(g, "mira", 520, FL + 700, 1900, "curious" if c.t < tw(c, "Nothing") else "bored", "down", "hold", t=c.gt, view="front", prop=False)
    phone(g, 760, 1080, 1.6, -0.1, lit=1.0, icon="none")
    if c.t > tw(c, "Nothing") - 0.1:
        label(g, "NOTHING.", 540, 380, 130, "#FF6B5B", k=pk(c, "Nothing"))
    if c.t > tw(c, "alone") - 0.3:
        label(g, "NOT ALONE", 540, 560, 100, PAL["yellow"], k=pk(c, "alone"))


def c1_stats(g, c):
    studio(g, c.gt, "#DDEFE6", "#3E8E7A")
    pie(g, 540, 640, 260, 0.68, PAL["coral"], k=ease_out(seg(c.t, tw(c, "sixty-eight") - 0.4, 0.9)), bg="#5A6A70")
    if c.t > tw(c, "sixty-eight") - 0.1:
        label(g, "68%", 540, 640, 140, "#FFFFFF", k=pk(c, "sixty-eight"), rot=0)
        label(g, "HOSPITAL STAFF", 540, 990, 80, PAL["cream"], k=pk(c, "staff"))
    if c.t > tw(c, "students") - 0.3:
        pie(g, 540, 1420, 260, 0.89, PAL["yellow"], k=ease_out(seg(c.t, tw(c, "eighty-nine") - 0.4, 0.9)))
        if c.t > tw(c, "eighty-nine") - 0.1:
            label(g, "89%", 540, 1420, 140, "#FFFFFF", k=pk(c, "eighty-nine"), rot=0)
        label(g, "STUDENTS", 540, 1770, 80, PAL["cream"], k=pk(c, "students"))
    else:
        for i in range(5):
            x = 160 + i * 190
            char2(g, ("doctor", "physicist", "doctor", "engineer", "doctor")[i], x, 1700, 520, "suspicious", "down", "hold", t=c.gt, prop=False)


def c1_waiting(g, c):
    office_v(g, c.gt)
    brain(g, 540, 800, 2.0, "worried", c.gt, look=(1, 0) if math.sin(c.gt * 2) > 0 else (-1, 0))
    phone(g, 540, 1350, 0.9, 0.0)
    label(g, "WAITING…", 540, 330, 120, PAL["coral"], k=pk(c, "waiting"))
    if c.t > tw(c, "safe") - 0.2:
        label(g, "PLAYS IT SAFE", 540, 1700, 100, "#FF6B5B", k=pk(c, "safe"))


def c1_twitch(g, c):
    shout = c.t > tw(c, "shouts") - 0.2
    if not shout:
        tw1, tw2 = tw(c, "twitch"), tw(c, "rubbing")
        pocket_close(g, c.gt, 0.0, empty=True)
        k1 = seg(c.t, tw1 - 0.1, 0.6)
        if 0 < k1 < 1:
            g.line([(260, 1400), (330, 1330), (400, 1420), (470, 1330), (540, 1420), (610, 1340)], PAL["yellow"], 14)
        k2 = seg(c.t, tw2 - 0.1, 1.0)
        if 0 < k2 < 1:
            for i in range(4):
                yy = 1250 + i * 50 + 30 * math.sin(c.gt * 22 + i)
                g.line([(160, yy), (920, yy)], "#FFFFFF", 6, a=0.55)
        label(g, "TWITCH", 540, 300, 110, PAL["cream"], k=pk(c, "twitch"))
        if c.t > tw2 - 0.1:
            label(g, "RUB", 540, 450, 110, PAL["yellow"], k=pk(c, "rubbing"))
    else:
        studio(g, c.gt, "#FF8A5B", "#8E2430")
        brain(g, 540, 1050, 2.4, "shout", c.gt)
        label(g, "PHONE!", 540, 420, 190, PAL["yellow"], k=pk(c, "phone"))


def c1_end(g, c):
    """Last shot matches frame 1 (buzzing pocket + suspicious face) so the Short loops."""
    office_v(g, c.gt)
    bz = 1.0 if c.t > tw(c, "buzz") - 0.2 else 0.0
    char2(g, "mira", 540, FL + 700, 1900, "suspicious", "down", "down", t=c.gt, view="front", prop=False)
    with g.at(780, 1500):
        g.rc(10 * math.sin(c.gt * 60) * bz, 0, 170, 270, "#25324A", PAL["yellow"], lw=8, r=24, a=0.95)
        g.glow(0, 0, 200, PAL["yellow"], 0.3 * bz)
    buzz(g, 780, 1500, 120, c.gt, bz)


def build():
    V = Video(EP, title=("NOBODY", "CALLED?"), cap_y=0.72, music="playful", sid="B006C1", captions=False)
    V.shot("H1", c1_hook, (0, "but"), tr="cut", sfx=[(0.0, "buzz", 0.55)])
    V.shot("H1", c1_nobody, ("but", 1), cam=push(1.0, 1.05, (540, 1000)), sfx=[("nobody", "sting", 0.4)])
    V.shot("L01", c1_check, (0, "If"), cam=push(1.0, 1.05, (600, 1000)), sfx=[("Nothing", "bloop", 0.45)])
    V.shot("L01", c1_check, ("If", 1), cam=push(1.12, 1.18, (540, 700)), sfx=[("alone", "pop", 0.35)])
    V.shot("L02", c1_stats, (0, "In#1"), cam=push(1.0, 1.04, (540, 900)), music="curious", sfx=[("sixty-eight", "pop", 0.4)])
    V.shot("L02", c1_stats, ("In#1", 1), cam=push(1.0, 1.03, (540, 1100)), sfx=[("eighty-nine", "ding", 0.45)])
    V.shot("L03", c1_waiting, cam=push(1.0, 1.06, (540, 900)), music="story", sfx=[("safe", "pop", 0.35)])
    V.shot("L04", c1_twitch, (0, "and"), cam=push(1.0, 1.04, (540, 1100)), music="tension", sfx=[("twitch", "click", 0.4), ("rubbing", "whoosh_soft", 0.35)])
    V.shot("L04", c1_twitch, ("and", 1), cam=push(1.0, 1.06, (540, 1000)), sfx=[("phone", "sting", 0.5)])
    V.shot("L05", c1_end, cam=push(1.0, 1.05, (600, 1100)), music="playful", sfx=[("buzz", "buzz", 0.5)])
    V.title_y = 0.1
    V.build()
    return V


if __name__ == "__main__":
    V = build()
    cmd = sys.argv[2] if len(sys.argv) > 2 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=2, cols=8, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "times":
        V.qa_numbers()
        print(V.sheet(sys.argv[4], times=[float(x) for x in sys.argv[3].split(",")], cols=6, scale=0.2))
    elif cmd == "render":
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / f"final/B-006-{SID}.mp4"))
