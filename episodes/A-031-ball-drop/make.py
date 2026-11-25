"""A-031 "Why Do We Drop a Ball on New Year's Eve?" — standalone Short, Style F + cast v2.2 (Runner, Captain, Gentleman). Slot Tue 29 Dec 2026 18:00 UTC.
python episodes/A-031-ball-drop/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: a generic New Year city square at night (no real signs or logos), an 1830s river with an old observatory
and its red time ball, tall ships, a ship's chronometer, an old sea chart with a course drifting off, and a 1907 night square with a
glowing ball. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_split import split_long
from flat_fx import burst, sparkles, arrow
from flat_winter import scarf, hand_pt
from flat_timeball import (city_square, tower_top, glow_ball, crowd_sil, fireworks, confetti, harbour_1833, observatory,
                           tall_ship, chronometer, sea_chart, clock_face2, FW_COLS, BALL_RED)

V = Video(EP, title=("WHY DROP", "A BALL?"), music="adventure")
V.title_y = 0.075
TX, TY, TS = 380, 1000, 1.0                 # tower: centre x, roof y
RX, RY, RH = 790, 1900, 1020                # runner (modern square), 3/4 view facing the tower
BR = 92                                     # ball radius
BURSTS = [(220, 560, 230, 0.0, FW_COLS[0]), (860, 470, 260, 0.35, FW_COLS[1]), (640, 760, 200, 0.8, FW_COLS[2]),
          (150, 820, 210, 1.3, FW_COLS[3]), (900, 760, 220, 1.7, FW_COLS[4])]


def ball_y(v):
    top, bot = TY - 540 * TS + BR * 0.3, TY - 70 * TS - BR * 0.9
    return lerp(bot, top, v)


def square(g, c, v, cheer=1.0, fw_t=None, era="now", conf=1.0):
    city_square(g, c.gt, era=era)
    tower_top(g, TX, TY, TS, era=era)
    glow_ball(g, TX, ball_y(v), BR, c.gt, old=(era == "1907"))
    if fw_t is not None:
        fireworks(g, fw_t % 2.2 if era == "now" else -9, BURSTS)
    crowd_sil(g, c.gt, y=1960, n=13, cheer=cheer, hats=(era == "1907"))
    if conf > 0 and era == "now":
        confetti(g, c.gt, k=conf)


def runner(g, c, expr, pl, pr):
    char2(g, "runner", RX, RY, RH, expr, pl, pr, t=c.gt, flip=True, view="3q", prop=False)
    scarf(g, RX, RY, RH, col="#5ED3B5", stripe="#FFF4E0", flip=True, t=c.gt)


# ------------------------------------------------------------------ hook / loop
def s_hook(g, c):
    """Frame 1: the glowing ball is already sliding down the mast, fireworks bloom, the crowd cheers, the runner gasps, arms up."""
    v = lerp(0.62, 0.15, ease_io(clamp(c.t / 2.6)))
    square(g, c, v, fw_t=c.t)
    runner(g, c, "shocked", "up", pose_at(c.t, [(0, "point"), (0.9, "up")]))


def s_count(g, c):
    """Close on the ball sliding down; big countdown numbers 3-2-1."""
    v = lerp(0.35, 0.0, clamp(c.u))
    square(g, c, v, fw_t=c.t + 1.0)
    with g.screen():
        n = 3 - min(2, int(c.u * 3))
        uu = (c.u * 3) % 1
        g.text(str(n), W / 2, 1450, 260, "#FFFFFF", sw=30, depth=12, sc=pop(uu, 0.0, 0.25))


# ------------------------------------------------------------------ L01: ships
def s_river(g, c):
    """'It started as a signal for ships...': an 1830s river, the observatory on the hill with its red ball, a tall ship sails in."""
    harbour_1833(g, c.gt)
    observatory(g, 250, 900, 0.75, ball_v=1.0)
    tall_ship(g, lerp(1250, 760, ease_out(clamp(c.u * 1.2))), 1400, 0.9, c.gt)
    with g.screen():
        g.text("SHIPS", W / 2, 1700, 120, "#FFFFFF", sw=17, depth=8, sc=pop(c.t, c.w("ships") - 0.08, 0.3), a=c.on("ships", 0.2))


def s_offcourse(g, c):
    """'one wrong clock could send a ship miles off course': on an old chart the real course bends away towards the rocks."""
    g.fill_all(g.rgrad(540, 1000, 1200, "#2E4A6E", "#132238"))
    k = c.on("wrong", 1.2) * 0.7 + 0.3 * c.on("miles", 0.6)
    sea_chart(g, 540, 1020, 960, 1100, c.gt, k=k)
    with g.screen():
        g.text("MILES OFF", W / 2, 360, 140, "#FF6B5B", sw=19, depth=10, sc=pop(c.t, c.w("miles") - 0.08, 0.3), a=c.on("miles", 0.2))


# ------------------------------------------------------------------ L02: clock set to home time
def deck_bg(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#6EC3E6", "#BDE6F2", "#F7E3B0"))
    g.glow(820, 380, 300, "#FFF4A8", 0.6)
    g.circle(820, 380, 90, "#FFE066", INK, lw=8)
    g.rect(-200, 1050, W + 400, 300, g.lgrad(0, 1050, 0, 1350, "#3E8EB8", "#2A6A8E"), None)
    g.line([(-200, 1050), (W + 200, 1050)], INK, 6)
    g.rect(-200, 1300, W + 400, 800, "#8A5A3A", INK, lw=8)                     # deck planks
    for x in range(-200, W + 200, 120):
        g.line([(x, 1300), (x + 60, 1920)], "#6E4630", 5)
    g.rect(-200, 1250, W + 400, 60, "#6E4630", INK, lw=7)                       # rail


def s_deck(g, c):
    """'At sea, sailors worked out where they were...': the captain on deck points at the sun; the chronometer waits on the rail."""
    deck_bg(g, c)
    char2(g, "captain", 380, 1880, 980, "suspicious" if c.t < c.w("where") else "deadpan",
          pose_at(c.t, [(0, "down"), (c.w("worked"), "point")]), "hold", t=c.gt, view="3q", prop=False)
    chronometer(g, 820, 1240, 0.55, c.gt)
    arrow(g, 560, 900, 720, 520, "#FFC93C", w=20, k=c.on("worked", 0.4))


def s_hometime(g, c):
    g.fill_all(g.rgrad(540, 1000, 1200, "#6E4630", "#2A1A14"))
    chronometer(g, 540, 1020, 1.9, c.gt, hl=c.on("home", 0.3))
    with g.screen():
        g.text("HOME TIME", W / 2, 420, 140, "#FFC93C", sw=19, depth=10, sc=pop(c.t, c.w("home") - 0.08, 0.3), a=c.on("home", 0.2))


def s_oneminute(g, c):
    """'Just one minute wrong could mean fifteen miles off': the minute hand is one minute off (red), and on the chart the ship slides 15 miles."""
    g.fill_all(g.rgrad(540, 1000, 1200, "#2E4A6E", "#132238"))
    chronometer(g, 540, 560, 0.95, c.gt, minute=c.on("minute", 0.3) * 1.0)
    sea_chart(g, 540, 1340, 900, 760, c.gt, k=0.45 * c.on("fifteen", 0.6))
    with g.screen():
        g.text("1 MIN", 860, 350, 100, "#FF6B5B", sw=15, depth=7, sc=pop(c.t, c.w("minute") - 0.08, 0.3), a=c.on("minute", 0.2))
        g.text("15 MILES", W / 2, 1810, 120, "#FF6B5B", sw=17, depth=9, sc=pop(c.t, c.w("fifteen") - 0.08, 0.3), a=c.on("fifteen", 0.2))


# ------------------------------------------------------------------ L03: Greenwich 1833
def s_greenwich(g, c):
    """'So in 1833, Greenwich put a big ball on a mast': the observatory, the red ball hoisted up the mast."""
    harbour_1833(g, c.gt)
    v = c.on("ball", 1.0)
    observatory(g, 540, 1230, 1.0, ball_v=v)
    tall_ship(g, 940, 1440, 0.45, c.gt)
    tall_ship(g, 140, 1520, 0.38, c.gt, flip=True)
    with g.screen():
        g.text("1833", 270, 440, 160, "#FFFFFF", sw=22, depth=11, sc=pop(c.t, c.w("1833") - 0.08, 0.3), a=c.on("1833", 0.2))


def s_oneclock(g, c):
    """'Every day at exactly one o'clock': a wall clock ticks from 12:59 to 1:00; the ball waits at the top behind."""
    harbour_1833(g, c.gt)
    observatory(g, 820, 1230, 0.7, ball_v=1.0)
    m = 59 + c.on("one", 0.25)
    clock_face2(g, 400, 1000, 250, 12 if m < 60 else 1, m % 60)
    with g.screen():
        g.text("1:00", 400, 1400, 140, "#FFC93C", sw=19, depth=10, sc=pop(c.t, c.w("one") - 0.08, 0.3), a=c.on("one", 0.2))


def s_drop(g, c):
    """'it dropped': the red ball falls down the mast and stops."""
    harbour_1833(g, c.gt)
    k = ease_io(clamp(c.since("dropped") / 0.45)) if c.t >= c.w("dropped") - 0.05 else 0
    bx, by = observatory(g, 540, 1230, 1.0, ball_v=1.0 - k)
    if 0 < k < 1:
        for i in range(3):
            g.line([(bx - 40 + i * 40, by - 80 - i * 10), (bx - 40 + i * 40, by - 150 - i * 10)], "#FFFFFF", 7, a=0.8)
    tall_ship(g, 940, 1440, 0.45, c.gt)


def s_setclocks(g, c):
    """'and ships on the river set their clocks': ships on the river; each crew's chronometer clicks into line (gold ring)."""
    harbour_1833(g, c.gt)
    observatory(g, 150, 1050, 0.5, ball_v=0.0)
    tall_ship(g, 760, 1380, 0.75, c.gt)
    tall_ship(g, 280, 1560, 0.5, c.gt, flip=True)
    k = c.on("set", 0.3)
    chronometer(g, 540, 1720, 0.6, c.gt, minute=1.0 - k, hl=k)
    if k > 0:
        sparkles(g, c.t, [(380, 1600), (700, 1620), (540, 1520)], seed=3, col="#FFF4A8", r=30, t0=c.w("set"))


# ------------------------------------------------------------------ L04: New York 1907
def s_1907(g, c):
    """'In 1907, New York borrowed the idea for New Year's Eve': an old night square, the glowing ball on the tower, top-hat crowd."""
    square(g, c, 1.0, cheer=0.2, era="1907")
    char2(g, "gent", RX, RY, RH, "smug", "hold", pose_at(c.t, [(0, "down"), (c.w("borrowed"), "point")]), t=c.gt, flip=True, view="3q", prop=False)
    with g.screen():
        g.text("1907", 300, 1430, 170, "#FFE7A8", sw=22, depth=11, sc=pop(c.t, c.w("1907") - 0.08, 0.3), a=c.on("1907", 0.2))


def s_midnight(g, c):
    """'with a glowing ball that dropped at midnight': clock hits 12, the ball drops, the 1907 crowd cheers."""
    k = ease_io(clamp(c.since("dropped") / 1.2)) if c.t >= c.w("dropped") - 0.05 else 0
    square(g, c, 1.0 - k, cheer=0.3 + 0.7 * c.on("midnight", 0.3), era="1907")
    clock_face2(g, 820, 760, 130, 12, lerp(58, 60, c.on("midnight", 0.3)) % 60)
    with g.screen():
        g.text("12:00", 820, 960, 90, "#FFE7A8", sw=13, a=c.on("midnight", 0.2))


# ------------------------------------------------------------------ L05: today = old signal
def s_today(g, c):
    """'So when the ball falls this New Year...': back to today's square, the ball falling, the runner looking up, smiling."""
    v = lerp(0.9, 0.3, ease_io(c.u))
    square(g, c, v, fw_t=c.t + 0.6)
    runner(g, c, "curious", "hip", pose_at(c.t, [(0, "down"), (0.4, "point")]))


def s_signal(g, c):
    """'...you're watching an old clock signal for sailors': same framing as frame 1; a ghost red time ball and a tall ship shimmer
    in the sky over the tower, then the ball slides down again (loop into frame 1)."""
    v = lerp(1.0, 0.62, ease_io(clamp(c.u * 1.05)))
    square(g, c, v, fw_t=c.t + 1.5)
    gk = c.on("old", 0.4) * (1 - clamp((c.u - 0.85) / 0.15))
    if gk > 0:
        with g.group(0.55 * gk):
            g.circle(TX + 330, 640, 70, BALL_RED, INK, lw=7)
            tall_ship(g, TX + 360, 940, 0.42, c.gt)
    runner(g, c, "smile", "up", pose_at(c.t, [(0, "point"), (c.w("sailors"), "up")]))


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, "giant"), cam=ZOOM(1.0, 1.04, (560, 1050)), sfx=[(0.0, "firework", 0.6), (0.0, "crowd_cheer", 0.35), (0.02, "sting", 0.3)], tr="cut")
V.shot("H1", s_count, ("giant", 1), cam=ZOOM(1.7, 1.8, (TX + 80, 820)), tr="cut", sfx=[(0.0, "tick", 0.4), (0.5, "tick", 0.4)])
V.shot("L01", s_river, (0, "because"), cam=ZOOM(1.0, 1.05, (540, 1100)), music="story", sfx=[(0.05, "whoosh", 0.3), (0.1, "waves", 0.25), ("ships", "bell", 0.35)])
V.shot("L01", s_offcourse, ("because", 1), cam=ZOOM(1.0, 1.06, (540, 1000)), tr="cut", sfx=[("wrong", "confuse", 0.35), ("miles", "thud", 0.4)])
V.shot("L02", s_deck, (0, "with"), cam=ZOOM(1.0, 1.05, (540, 1100)), sfx=[(0.1, "waves", 0.25), ("worked", "creak", 0.3)])
V.shot("L02", s_hometime, ("with", "Just"), cam=ZOOM(1.0, 1.06, (540, 1000)), tr="cut", sfx=[(0.0, "tick", 0.35), ("home", "ding", 0.3)])
V.shot("L02", s_oneminute, ("Just", 1), cam=ZOOM(1.0, 1.04, (540, 1000)), tr="cut", sfx=[("minute", "tick", 0.4), ("fifteen", "confuse", 0.35)])
V.shot("L03", s_greenwich, (0, "Every"), cam=ZOOM(1.0, 1.06, (540, 950)), sfx=[("1833", "pop", 0.35), ("ball", "creak", 0.3)])
V.shot("L03", s_oneclock, ("Every", "it"), cam=ZOOM(1.0, 1.05, (540, 1000)), tr="cut", sfx=[(0.1, "tick", 0.35), ("one", "bell", 0.45)])
V.shot("L03", s_drop, ("it", "and"), cam=ZOOM(1.1, 1.14, (540, 860)), tr="cut", sfx=[("dropped", "clunk", 0.6)])
V.shot("L03", s_setclocks, ("and", 1), cam=ZOOM(1.0, 1.04, (540, 1250)), tr="cut", sfx=[("set", "click", 0.5), ("clocks", "sparkle", 0.35)])
V.shot("L04", s_1907, (0, "with"), cam=ZOOM(1.0, 1.05, (560, 1050)), music="playful", sfx=[(0.05, "whoosh", 0.3), ("1907", "pop", 0.35), (0.2, "crowd_murmur", 0.2)])
V.shot("L04", s_midnight, ("with", 1), cam=ZOOM(1.0, 1.05, (500, 900)), tr="cut", sfx=[("midnight", "bell", 0.45), ("dropped", "crowd_cheer", 0.45)])
V.shot("L05", s_today, (0, "you're"), cam=ZOOM(1.0, 1.04, (560, 1050)), music="adventure", sfx=[(0.1, "firework", 0.45), (0.3, "crowd_cheer", 0.3)])
V.shot("L05", s_signal, ("you're", 1), cam=ZOOM(1.0, 1.04, (560, 1050)), tr="cut", sfx=[("old", "shimmer", 0.35), ("sailors", "firework", 0.5)])
V.build()
split_long(V, maxd=2.6, keep_cam=True)          # no shot longer than ~2.6 s (a visual change at least every 3 s)
V.title_out = V.voice0["H1"] + V.T["H1"]["dur"]

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=5, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-031.mp4"))
