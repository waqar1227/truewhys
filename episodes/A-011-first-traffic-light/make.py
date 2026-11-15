"""A-011 "The Traffic Light That Exploded" — standalone Short, Style F + cast v2.1 (audit §6.3).
python episodes/A-011-first-traffic-light/make.py sheet|render|qa|big <t,t,..>
Respectful: the explosion is a flash and smoke; the constable is never shown injured (a newspaper line says he was hurt).
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import qmark, sparkles, flame, burst, ring_wave

V = Video(EP, title=("THE TRAFFIC LIGHT", "THAT EXPLODED"), cap_y=0.70,
          keys={"first", "explode", "1868", "parliament", "chaos", "railway", "trains", "day", "night", "red", "green", "policeman", "hand", "lever",
                "month", "gas", "explodes", "hurt", "scraps", "sixty", "railways", "never", "stood"}, music="mystery")
POST_C, POST_D = "#2F5D50", "#1E3F36"


# ------------------------------------------------------------------ sets and props
def street(g, t, night=0.0, tower=True):
    sky = mix("#9ED8F0", "#14213D", night)
    g.fill_all(g.lgrad(0, 0, 0, H, sky, mix("#F7D9A8", "#28325A", night)))
    with g.layer(0.45):
        if tower:                                                           # civic gothic skyline (our own drawing)
            g.rect(640, 220, 180, 900, mix("#D9B98A", "#4A4A6A", night), INK, lw=8)
            g.poly([(620, 230), (730, 40), (840, 230)], mix("#6E8A7A", "#2A3A44", night), INK, lw=8)
            g.circle(730, 360, 62, mix("#FFF4E0", "#FFE9A8", night), INK, lw=7)
            g.line([(730, 360), (730, 318)], INK, 6); g.line([(730, 360), (758, 372)], INK, 6)
        for i in range(-1, 4):
            x = i * 300 - 60
            g.rect(x, 700, 260, 520, mix("#E3C79A", "#3E4466", night), INK, lw=8)
            for j in range(3):
                for k in range(2):
                    g.rect(x + 40 + k * 110, 760 + j * 140, 70, 100, mix("#5E7F94", "#FFD36B", night), INK, lw=5, r=30)
            g.poly([(x - 10, 700), (x + 130, 620), (x + 270, 700)], mix("#8A6A54", "#2A2A44", night), INK, lw=7)
    g.rect(-100, 1440, W + 200, 700, mix("#A69580", "#3A3A50", night), INK, lw=8)  # cobbles
    for j in range(8):
        for i in range(-1, 12):
            g.ellipse(i * 110 + (55 if j % 2 else 0), 1480 + j * 62, 46, 22, mix("#8E7E6A", "#2E2E44", night), None, a=0.8)


def signal_post(g, x, y, s=1.0, arm=0.0, lamp=None, spark=0.0, t=0.0, burst_k=0.0, gas=0.0, cut=0.0):
    """Knight's 1868 signal: cast-iron pillar, lantern on top, two semaphore arms. arm 0 = down (go), 1 = horizontal (stop)."""
    with g.at(x, y, 0, s):
        g.rc(0, -40, 170, 80, POST_D, INK, lw=8, r=10)                      # base
        g.path("M-50 -80 L-34 -980 L34 -980 L50 -80 Z", POST_C, INK, lw=9)
        for yy in (-300, -600, -900):
            g.rc(0, yy, 96, 26, POST_D, INK, lw=6, r=6)
        if gas > 0:                                                         # cutaway: gas rising inside the pillar
            g.path("M-26 -100 L-20 -960 L20 -960 L26 -100 Z", "#1A2A24", INK, lw=5)
            for i in range(7):
                u = (t * 0.5 + i / 7) % 1.0
                g.circle(4 * math.sin(i + t * 3), -120 - 820 * u, 16 * gas, "#9BE07A", None, a=0.75 * gas * (1 - u * 0.3))
        for sd in (-1, 1):                                                  # semaphore arms
            ang = sd * (math.radians(55) * (1 - arm))
            with g.at(sd * 36, -900, ang):
                g.rc(sd * 140, 0, 280, 46, "#C8323C", INK, lw=8, r=8)
                g.rc(sd * 220, 0, 30, 46, "#FFFFFF", None)
        if not burst_k:
            g.rc(0, -1040, 150, 130, "#22303A", INK, lw=9, r=16)            # lantern
            g.poly([(-90, -1105), (0, -1170), (90, -1105)], POST_D, INK, lw=8)
            col = {"red": "#FF3B30", "green": "#3EDB6E"}.get(lamp)
            if col:
                g.glow(0, -1040, 210, col, 0.55)
                g.rc(0, -1040, 100, 84, col, INK, lw=6, r=12)
            else:
                g.rc(0, -1040, 100, 84, "#4A5A66", INK, lw=6, r=12)
            if spark > 0:
                flame(g, 0, -980, 70, 120 * spark, t, seed=2)
                sparkles(g, t, [(-80, -1120), (90, -1090), (40, -1180)], r=26 * spark, col="#FFE08A")
        else:
            k = burst_k
            g.glow(0, -1040, 520 * ease_out(k), "#FFE08A", 0.9 * (1 - k * 0.6))
            for i in range(9):
                a = i * TAU / 9 + 0.3
                d = 80 + 420 * ease_out(k)
                g.poly([(d * math.cos(a), -1040 + d * math.sin(a)), (d * math.cos(a) + 30, -1040 + d * math.sin(a) + 12),
                        (d * math.cos(a) + 8, -1040 + d * math.sin(a) + 34)], "#BFE6F2", INK, lw=4, a=1 - k)
            for i in range(6):
                a = i * TAU / 6
                r = 120 + 160 * ease_out(k)
                g.circle(r * math.cos(a) * 0.8, -1040 + r * math.sin(a) * 0.6 - 120 * k, 110 * (0.5 + k), "#6E6E7A", INK, lw=6, a=0.85 * (1 - k * 0.5))
        if cut > 0:
            with g.at(0, -560, 0, back_out(clamp(cut))):
                g.line([(-220, -220), (220, 220)], "#FF3B30", 40); g.line([(-220, 220), (220, -220)], "#FF3B30", 40)


def carriage(g, x, y, s=1.0, t=0.0, face=1):
    """Hansom-style cab with a simple horse, side view, facing `face`."""
    with g.at(x, y, 0, s * face, s):
        # horse
        lg = math.sin(t * 9)
        for i, dx in enumerate((150, 190, 320, 360)):
            sw = 30 * (lg if i % 2 else -lg)
            g.line([(dx, -170), (dx + sw, -20)], "#6B4A2F", 22); g.line([(dx + sw, -20), (dx + sw + 8, 0)], INK, 20)
        g.ellipse(255, -210, 140, 70, "#8A5A3A", INK, lw=8)
        g.path("M360 -240 L430 -360 Q470 -380 500 -350 L470 -300 L410 -230 Z", "#8A5A3A", INK, lw=8)
        g.circle(462, -340, 7, INK, None)
        g.path("M390 -280 L440 -350", None, "#3A2416", lw=12)
        # cab
        g.rect(-200, -420, 260, 280, "#2A2A38", INK, lw=9, r=20)
        g.rect(-170, -390, 120, 110, "#8FD3E8", INK, lw=6, r=10)
        g.line([(60, -200), (220, -230)], "#5B3A29", 12)
        g.circle(-60, -110, 110, None, INK, lw=14)
        for i in range(8):
            a = i * TAU / 8 + t * 4
            g.line([(-60, -110), (-60 + 100 * math.cos(a), -110 + 100 * math.sin(a))], "#C9A23A", 7)
        g.circle(-60, -110, 18, "#C9A23A", INK, lw=5)


def train(g, x, y, s=1.0, t=0.0):
    with g.at(x, y, 0, s):
        g.rect(-300, -260, 420, 200, "#2F4F3F", INK, lw=9, r=20)
        g.rect(120, -380, 200, 320, "#2F4F3F", INK, lw=9, r=16)
        g.rect(150, -350, 120, 100, "#FFD36B", INK, lw=6, r=10)
        g.rect(-250, -360, 70, 100, INK, None, r=8)
        for i in range(3):
            g.circle(-200 + i * 160, -40, 70, "#C8323C", INK, lw=9)
            g.circle(-200 + i * 160, -40, 18, INK, None)
        for i in range(4):
            u = (t * 0.8 + i / 4) % 1.0
            g.circle(-215 - 120 * u, -400 - 260 * u, 50 + 70 * u, "#FFFFFF", INK, lw=5, a=0.9 * (1 - u))


def rail_signal(g, x, y, s, lamp, arm=1.0):
    with g.at(x, y, 0, s):
        g.rect(-18, -700, 36, 700, "#4A4A55", INK, lw=7)
        with g.at(18, -640, -math.radians(40) * (1 - arm)):
            g.rc(110, 0, 220, 44, "#C8323C", INK, lw=7, r=6)
        g.rc(-60, -640, 90, 110, "#22303A", INK, lw=7, r=12)
        col = {"red": "#FF3B30", "green": "#3EDB6E"}[lamp]
        g.glow(-60, -640, 160, col, 0.6)
        g.circle(-60, -640, 34, col, INK, lw=5)


def modern_light(g, x, y, s, phase):
    with g.at(x, y, 0, s):
        g.rect(-22, -900, 44, 900, "#4A4A55", INK, lw=8)
        g.rc(0, -1040, 200, 480, "#22222C", INK, lw=10, r=30)
        for i, col in enumerate(("#FF3B30", "#FFB21E", "#3EDB6E")):
            on = (i == phase)
            if on: g.glow(0, -1200 + i * 160, 200, col, 0.6)
            g.circle(0, -1200 + i * 160, 62, col if on else shade(col, 0.35), INK, lw=8)


def newspaper(g, x, y, s, rot, k):
    with g.at(x, y, rot, s * (0.3 + 0.7 * back_out(clamp(k), 1.4))):
        g.rc(0, 0, 820, 1000, "#F3EAD6", INK, lw=12, r=10)
        g.text("THE LONDON PAPER", 0, -400, 60, "#22181B", stroke=None)
        g.line([(-370, -350), (370, -350)], INK, 6)
        g.text("SIGNAL LAMP", 0, -240, 104, "#22181B", stroke=None)
        g.text("EXPLODES", 0, -120, 120, "#B0413E", stroke=None)
        g.text("CONSTABLE HURT", 0, -10, 64, "#22181B", stroke=None)
        for j in range(8):
            g.line([(-360, 80 + j * 45), (360 if j % 3 else 200, 80 + j * 45)], "#9A8E7A", 12)


def calendar(g, x, y, year, k):
    with g.at(x, y, -0.04, 0.4 + 0.6 * back_out(clamp(k))):
        g.rc(0, 0, 560, 440, "#FFF4E0", INK, lw=12, r=24)
        g.rc(0, -170, 560, 110, "#B0413E", INK, lw=12, r=24)
        for i in (-150, 150):
            g.rc(i, -230, 30, 90, "#9AA3AD", INK, lw=6, r=8)
        g.text(str(year), 0, 60, 190, "#22181B", stroke=None)


# ------------------------------------------------------------------ shots
PX = 640


def s_hook(g, c):
    """Frame 1: the sparking signal lamp (object in action) + the constable looking up in shock."""
    street(g, c.gt, 0.25)
    signal_post(g, PX + 60, 2150, 1.15, 0.6, "red", spark=0.6 + 0.4 * math.sin(c.gt * 7) ** 2, t=c.gt)
    char2(g, "bobby", 300, 2020, 1300, "shocked" if c.t > 0.6 else "suspicious", "down", "up" if c.t > 0.6 else "down", t=c.gt)


def s_about(g, c):
    street(g, c.gt, 0.25)
    signal_post(g, PX + 60, 2150, 1.15, 0.6, "red", spark=1.0, t=c.gt)
    char2(g, "bobby", 300, 2020, 1300, "shocked", "up", "up", t=c.gt, squash=0.02 * math.sin(c.gt * 30))


def s_london(g, c):
    street(g, c.gt)
    carriage(g, -300 + 900 * c.u, 1720, 1.1, c.gt)


def s_chaos(g, c):
    street(g, c.gt)
    carriage(g, 1300 - 1100 * c.u, 1640, 0.9, c.gt, face=-1)
    char2(g, "gent", 330, 2050, 1180, "shocked", "up", "up", t=c.gt)
    carriage(g, -500 + 1300 * c.u, 1900, 1.1, c.gt)


def s_knight(g, c):
    street(g, c.gt, tower=False)
    char2(g, "gent", 520, 2080, 1350, "suspicious" if c.t < c.w("borrows") - 0.2 else "smug", "hip", "down", t=c.gt)
    with g.screen():
        g.rc(780, 640, 380, 90, "#FFF4E0", INK, lw=8, r=20)
        g.text("RAILWAY ENGINEER", 780, 645, 40, "#22181B", stroke=None)


def s_trains(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#BFE6F2", "#F7D9A8"))
    g.rect(-100, 1500, W + 200, 600, "#8E7E6A", INK, lw=8)
    for i in range(-1, 14):
        g.rect(i * 90 - (c.gt * 300) % 90, 1520, 40, 40, "#5B3A29", None)
    g.line([(-100, 1515), (W + 100, 1515)], "#9AA3AD", 12)
    rail_signal(g, 880, 1500, 1.1, "red")
    train(g, -300 + 1100 * c.u, 1500, 1.25, c.gt)
    char2(g, "gent", 260, 2150, 1000, "smug", "point", "down", t=c.gt, prop=False)


def s_day(g, c):
    street(g, c.gt, 0.0)
    arm = 0.5 + 0.5 * math.sin(c.gt * 2.2)
    signal_post(g, PX, 1760, 1.15, arm, None, t=c.gt)
    char2(g, "bobby", 280, 2020, 1250, "deadpan", "down", "hold", t=c.gt, prop=False)


def s_night(g, c):
    street(g, c.gt, 1.0)
    lamp = "red" if c.t < c.w("green") - 0.05 else "green"
    signal_post(g, PX, 1760, 1.15, 1.0 if lamp == "red" else 0.0, lamp, t=c.gt)
    char2(g, "bobby", 280, 2020, 1250, "deadpan", "down", "hold", t=c.gt, prop=False)


def s_lever(g, c):
    street(g, c.gt, 0.15)
    k = 0.5 + 0.5 * math.sin(c.gt * 2.6)
    signal_post(g, 600, 1760, 1.0, k, "red" if k > 0.5 else "green", t=c.gt)
    char2(g, "bobby", 330, 2030, 1250, "deadpan", "reach_r", "reach_r", t=c.gt)
    with g.at(760, 1820, -0.25 + 0.3 * k):                                         # lever, in front, under his hands
        g.rc(0, 30, 120, 60, "#3A3A48", INK, lw=7, r=10)
        g.line([(0, 0), (0, -560)], INK, 30); g.line([(0, 0), (0, -560)], "#7A8290", 18)
        g.circle(0, -570, 34, "#C8323C", INK, lw=7)


def s_gas(g, c):
    street(g, c.gt, 0.35)
    signal_post(g, 540, 2280, 1.45, 0.6, "red", t=c.gt, gas=ease_out(seg(c.t, c.w("gas") - 0.2, 0.6)))
    with g.screen():
        g.text("A MONTH LATER", W / 2, 520, 110, PAL["cream"], sw=20, depth=8, sc=pop(c.t, 0.0, 0.3))


def s_boom(g, c):
    street(g, c.gt, 0.35)
    k = seg(c.t, 0.0, 1.2)
    signal_post(g, 540, 2280, 1.45, 0.6, None, t=c.gt, burst_k=max(0.001, k))
    if c.t < 0.12:
        g.fill_all(rgba("#FFFFFF", 0.7 * (1 - c.t / 0.12)))


def s_paper(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#3A4466", "#1E2440", "#10142A"))
    newspaper(g, 540, 1080, 1.05, -0.04, seg(c.t, 0.0, 0.45))


def s_scrap(g, c):
    street(g, c.gt, 0.1)
    signal_post(g, PX, 1760, 1.15, 1.0, None, t=c.gt, cut=seg(c.t, c.w("scraps") - 0.1, 0.35))
    char2(g, "gent", 280, 2020, 1250, "bored", "hip", "hip", t=c.gt)


def s_years(g, c):
    g.fill_all(g.rgrad(540, 1100, 1300, "#2E7FA0", "#15506A", "#0B2E40"))
    y = 1869 + int(round(57 * ease_io(seg(c.t, 0.3, max(0.5, c.T - 0.8)))))
    calendar(g, 540, 1050, y, seg(c.t, 0, 0.35))


def s_railway(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#14213D", "#3A4466"))
    g.rect(-100, 1500, W + 200, 600, "#2E2E44", INK, lw=8)
    rail_signal(g, 300, 1520, 1.3, "red" if (c.gt * 1.2) % 2 < 1 else "green")
    modern_light(g, 800, 1520, 0.9, 0 if (c.gt * 1.2) % 2 < 1 else 2)
    with g.screen():
        g.text("=", 545, 900, 200, PAL["yellow"], sw=30, sc=pop(c.t, c.w("railways") - 0.1, 0.3))


def s_never(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#9ED8F0", "#F7D9A8"))
    with g.layer(0.5):
        for i in range(-1, 4):
            g.rect(i * 300 - 40, 600, 260, 800, "#B9C6D2", INK, lw=8)
            for j in range(5):
                g.rect(i * 300, 650 + j * 140, 180, 90, "#8FD3E8", INK, lw=5)
    g.rect(-100, 1460, W + 200, 700, "#5A5A6A", INK, lw=8)
    for i in range(6):
        g.rect(80 + i * 170, 1560, 100, 30, "#FFFFFF", None)
    modern_light(g, 820, 1760, 1.0, 0 if c.t < c.w("never") else 2)
    char2(g, "modern", 380, 2060, 1250, "bored" if c.t < c.w("never") else "smug", "down", "hold", t=c.gt)


def s_loop(g, c):
    """Last shot = frame 1 (loop)."""
    street(g, c.gt, 0.25)
    signal_post(g, PX + 60, 2150, 1.15, 0.6, "red", spark=0.5, t=c.gt)
    char2(g, "bobby", 300, 2020, 1300, "suspicious", "down", "down", t=c.gt)


V.shot("H1", s_hook, part=(0, "And"), sfx=[(0.0, "fire", 0.25), (0.6, "zap", 0.3)])
V.shot("H1", s_about, part=("And", 1), cam=push(1.0, 1.12, (640, 1000)), sfx=[("explode", "heartbeat", 0.4)])
V.shot("L01", s_london, part=(0, "Outside"), tr="flash", music="adventure", sfx=[(0.0, "whoosh", 0.4), (0.2, "crowd_murmur", 0.3)])
V.shot("L01", s_chaos, part=("Outside", 1), sfx=[("chaos", "boing", 0.35), (0.2, "crowd_murmur", 0.35)])
V.shot("L02", s_knight, part=(0, "borrows"), cam=push(1.0, 1.05, (520, 1100)))
V.shot("L02", s_trains, part=("borrows", 1), sfx=[(0.0, "whoosh", 0.4)])
V.shot("L03", s_day, part=(0, "By#1"), sfx=[(0.3, "creak", 0.35)])
V.shot("L03", s_night, part=("By#1", 1), tr="flash", sfx=[("red", "click", 0.4), ("green", "click", 0.4)])
V.shot("L04", s_lever, cam=push(1.0, 1.05, (520, 1300)), sfx=[("lever", "creak", 0.5)])
V.shot("L05", s_gas, part=(0, "and"), music="tension", cam=push(1.0, 1.06, (540, 1100)), sfx=[("gas", "rush", 0.35)])
V.shot("L05", s_boom, part=("and", "The#2"), sfx=[("explodes", "cannon", 0.55)])
V.shot("L05", s_paper, part=("The#2", 1), sfx=[(0.0, "paper", 0.5)])
V.shot("L06", s_scrap, part=(0, "Traffic"), music="curious", sfx=[("scraps", "drum_hit", 0.4)])
V.shot("L06", s_years, part=("Traffic", 1), sfx=[(0.3, "tick", 0.35), ("sixty", "ding", 0.4)])
V.shot("L07", s_railway, part=(0, "and#1"), cam=push(1.0, 1.05, (540, 1100)), sfx=[("railways", "shimmer", 0.4)])
V.shot("L07", s_never, part=("and#1", 1), sfx=[("never", "ding", 0.35)])
V.shot("L08", s_loop, cam=push(1.0, 1.05, (540, 1200)), sfx=[(0.0, "fire", 0.2)])
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
        V.render(str(EP / "final/A-011.mp4"))
