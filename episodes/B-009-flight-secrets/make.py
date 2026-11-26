"""B-009 (L9) "Why Planes Dim the Lights to Land (and 6 More Flight Secrets)" — long video, Style F + cast v2.2 + lib/flat_flight.py, 1920x1080.
python episodes/B-009-flight-secrets/make.py sheet|qa|times <t,..> <out>|big <t,..>|chapters|animatic|render
One flight from the gate to the runway. Sets: night cabin row (hook/loop), aisle (bright/dim, floor lights), gate apron top-down (jet bridge left,
trucks right), harbour top-down (port side), sky + cell towers, cockpit at dusk, night hangar evacuation test, top-down seat rows, cloud window close-up,
3-pane cross-section, low-pressure taste chamber, meal tray, ocean crossing, mask drop, altitude chart, bright room/dark doorway, night approach, runway rescue.
Cast: Kai (traveller), Nia (young passenger), Rosa (flight attendant), Captain Ade (pilot), firefighter. Music: travel, cruise, curious, tension, warm.
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1920x1080"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at, turn_at
from flat_fx import sparkles, arrow, burst, ring_wave, no_sign, qmark, puff
from flat_flight import *
import cast2
import sfxgen  # noqa: registers cabin_chime, jet_hum, power_off, buzz, hiss ...

cast2.CAST["kai_p"] = dict(cast2.CAST["kai"], prop="phone")
V = Video(EP, title=None, cap_y=0.885, cap_size=74, badge=0, music="travel", captions=False)
CH_PAUSE = 1.1
SEATS = (760, 1200, 1640)
FEET = 1150            # seated people: feet hidden behind the seat in front


# ------------------------------------------------------------------ helpers
def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def pk(c, word, n=0, frac=0.5, d=0.3):
    return pop(c.t, tw(c, word, n, frac) - 0.1, d)


def lt(c):
    return c.gt - c.V.voice0[c.sh["line"]]


def label(g, txt, x, y, size=70, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x, y, k=1.0, size=46):
    """Small context label (year/place) while the story moves (why_not_viral rule 2)."""
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


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


def bubble(g, x, y, txt, k=1.0, size=60, tail=(-1, 1), col="#FFFFFF"):
    if k <= 0: return
    with g.at(x, y, 0, back_out(clamp(k), 1.6)):
        w = g.text_w(txt, size) + 70
        h = size * 1.7
        g.poly([(tail[0] * 30, h / 2 - 6), (tail[0] * 80, h / 2 + 50 * tail[1]), (tail[0] * 70 + 40 * tail[0] * -1, h / 2 - 6)], col, INK, lw=6)
        g.rc(0, 0, w, h, col, INK, lw=7, r=h / 2)
        g.text(txt, 0, 4, size, INK, stroke=None)


def stamp(g, txt, x, y, k, col="#FF5B4B", size=90, rot=-0.12):
    if k <= 0: return
    with g.screen():
        with g.at(x, y, rot, 1.6 - 0.6 * back_out(clamp(k), 1.4)):
            w = g.text_w(txt, size) + 60
            g.rc(0, 0, w, size * 1.45, None, col, lw=10, r=18, a=clamp(k * 2))
            g.text(txt, 0, 4, size, col, stroke=None, a=clamp(k * 2))


def studio(g, t, a="#2E5A8C", b="#0E1F3A", cx=None):
    cx = W / 2 if cx is None else cx
    g.fill_all(g.rgrad(cx, H * 0.45, W * 0.75, a, shade(a, 0.8), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(cx, H * 0.45), (cx + 2400 * math.cos(a0), H * 0.45 + 2400 * math.sin(a0)),
                (cx + 2400 * math.cos(a0 + 0.1), H * 0.45 + 2400 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.04)


def zzz(g, x, y, t, k=1.0):
    for i in range(3):
        ph = (t * 0.7 + i / 3) % 1
        g.text("z", x + 40 * ph + i * 10, y - 120 * ph, 40 + 30 * ph, PAL["cream"], sw=8, a=k * (1 - ph))


# ------------------------------------------------------------------ the seat row (hook / loop / many beats)
def row(g, c, kai="deadpan", nia="deadpan", lights=1.0, night=True, kai_view=None, kai_flip=False, nia_view=None, nia_flip=False,
        kai_pose=("down", "hold"), nia_pose=("down", "hold"), tray=0.0, shade_k=0.0, kai_cid="kai", extra=None, third=None, mask_k=(0.0, 0.0),
        panel=0.0, kai_h=880, front=True):
    cabin_row_back(g, c.gt, 330, SEATS, night=night, shade_k=shade_k)
    if panel > 0:
        mask_panel(g, 980, 182, panel, c.gt, n=3, gap=230)
    char2(g, kai_cid, SEATS[0], FEET, kai_h, kai, kai_pose[0], kai_pose[1], t=c.gt, view=kai_view, flip=kai_flip)
    if nia:
        char2(g, "nia", SEATS[1], FEET, 790, nia, nia_pose[0], nia_pose[1], t=c.gt, view=nia_view, flip=nia_flip)
    if third:
        third(g)
    mask_on(g, SEATS[0], FEET, kai_h, mask_k[0])
    mask_on(g, SEATS[1], FEET, 790, mask_k[1])
    if extra:
        extra(g)
    if front:
        cabin_row_front(g, c.gt, SEATS, 770, tray=tray, lights=lights)


def lights_flicker(t, t0=0.0, lo=0.18):
    """Lights snapping off: two quick flickers, then dim."""
    u = t - t0
    if u < 0: return 1.0
    if u < 0.08: return lo
    if u < 0.16: return 0.85
    if u < 0.24: return lo
    if u < 0.3: return 0.6
    return lo


def strip(g, c, stage, k=1.0):
    flight_strip(g, stage, c.gt, k)


# ------------------------------------------------------------------ cold open
def s_hook(g, c):
    L = lights_flicker(c.t, 0.0)
    row(g, c, "shocked", "bored", lights=L, kai_view="3q", kai_pose=("down", "up"))
    zzz(g, SEATS[1] + 120, 330, c.gt)
    with g.screen():
        g.text("LIGHTS OFF?", 1340, 210, 120, PAL["yellow"], sw=20, depth=9, sc=back_out(clamp(c.t / 0.25), 1.4) if c.t > 0 else 1.0)


def s_outside_dim(g, c):
    k = on(c, "switches", 0.4)
    landing_night(g, c.gt, lights=1 - 0.8 * k, prog=0.15 * c.u)


def s_purpose(g, c):
    def pp(g, i):
        if i == 3:
            char2(g, "rosa", 1120, 905, 560, "deadpan", "down", "point", t=c.gt, view="3q", flip=True)
    aisle(g, c.gt, lights=0.2, people=pp)
    stamp(g, "ON PURPOSE", 640, 300, on(c, "purpose", frac=0.6))


def s_sleep(g, c):
    row(g, c, "deadpan", "bored", lights=0.2, kai_view="3q", kai_flip=False)
    zzz(g, SEATS[1] + 120, 330, c.gt)
    cross(g, 1500, 300, 70, pk(c, "not"))


def s_getout(g, c):
    def pp(g, i):
        if i == 2:
            char2(g, "rosa", 1110, 840, 470, "deadpan", "down", "point", t=c.gt, view="3q", flip=True)
    aisle(g, c.gt, lights=0.1, people=pp)
    k = on(c, "out")
    for i in range(4):
        u = (c.gt * 1.4 + i / 4) % 1
        arrow(g, 960, 1050 - 520 * u, 960, 990 - 520 * u, col=PAL["yellow"], w=26, k=k, a=k * (1 - u))


def s_things(g, c):
    def pp(g, i):
        if i == 4:
            char2(g, "rosa", 960, 1040, 640, "smile", "explain", "explain", t=c.gt)
    aisle(g, c.gt, lights=1.0, people=pp)
    pos = [(300, 300), (560, 160), (1360, 160), (1620, 300), (340, 600), (1580, 600), (960, 120)]
    for i, (x, y) in enumerate(pos):
        k = back_out(seg(c.t, 0.15 + i * 0.18, 0.35), 1.6)
        if k > 0:
            with g.at(x, y + 8 * math.sin(c.gt * 2 + i), 0, k):
                g.circle(0, 0, 66, "#10263B", PAL["cream"], lw=5)
                icon(g, ICONS[i], 0, 0, 1.2, PAL["yellow"], 7)


def gate_dawn(g, t, depart=0.0):
    g.fill_all(g.lgrad(0, 0, 0, H, "#FFB36B", "#FFE2B8"))
    with g.layer(0.3):
        g.circle(1500, 560, 120, "#FFF2C8", None)
        g.glow(1500, 560, 400, "#FFF2C8", 0.5)
    with g.layer(0.6):
        for i in range(6):
            g.ellipse(200 + i * 340, 200 + (i % 2) * 60, 140, 26, "#FFFFFF", None, a=0.6)
    g.rect(-300, 760, 2600, 500, "#6E7684", INK, lw=6)
    g.line([(-300, 900), (2300, 900)], PAL["yellow"], 8, dash=([40, 30],))
    plane_side(g, 900 + 900 * ease_in(depart), 620 - 120 * ease_in(clamp(depart * 1.4 - 0.4)), 0.9, t, lights=0.6, dir=-1, doors=[-470])
    g.rect(-300, 450, 520, 200, "#C9CED6", INK, lw=8)       # terminal edge + jet bridge
    g.rect(200, 520, 230 * (1 - depart), 90, "#B8C2CC", INK, lw=6)


def s_journey(g, c):
    gate_dawn(g, c.gt, depart=clamp((c.t - 0.6) / c.T * 0.6))
    for i, (w, x) in enumerate((("gate", 420), ("runway", 1500))):
        pass
    strip(g, c, 6 * ease_io(clamp(c.u * 1.2)), 1.0)


def s_seven(g, c):
    studio(g, c.gt)
    k = back_out(clamp(c.t / 0.35), 1.5)
    with g.screen():
        g.text("7", W / 2, 420, 300 * k + 1, PAL["yellow"], sw=34, depth=16)
        for i in range(7):
            kk = back_out(seg(c.t, 0.2 + i * 0.12, 0.3), 1.6)
            if kk > 0:
                with g.at(W / 2 - 540 + i * 180, 780, 0, kk):
                    g.circle(0, 0, 70, "#FFF4E0", INK, lw=6)
                    icon(g, ICONS[i], 0, 0, 1.25, PAL["navy"], 7)
        g.text("?", W / 2 + 200, 330, 120, PAL["coral"], sw=18, sc=pk(c, "reason"))


def card(n, kind, txt, bg="studio"):
    def f(g, c):
        studio(g, c.gt, "#2E5A8C", "#0B1730")
        plane_side(g, 960 + 300 * math.sin(c.gt * 0.3), 900, 0.45, c.gt)
        number_card(g, c.gt, n, kind, txt, clamp(c.t / 0.4))
        strip(g, c, n - 1, 1.0)
    return f


# ------------------------------------------------------------------ 1 left door
def s_bridge(g, c):
    kb = clamp(lt(c) / 2.0)
    apron_top(g, c.gt, k_bridge=kb, k_trucks=0.0, hl="left" if on(c, "left") > 0.5 else None)
    label(g, "LEFT", 420, 200, 90, k=pk(c, "left"))
    strip(g, c, 0)


def s_ship(g, c, port=False, sail=None):
    dock_top(g, c.gt)
    if port:
        label(g, "PORT", 500, 500, 110, k=pk(c, "port") if sail is None else 1.0)
        arrow(g, 520, 600, 690, 600, col=PAL["yellow"], k=pk(c, "port") if sail is None else 1.0)
    strip(g, c, 0)


def s_words(g, c):
    gate_dawn(g, c.gt)
    words = [("CAPTAIN", 380, 200), ("CREW", 860, 140), ("CABIN", 1340, 200), ("PORT", 1620, 330)]
    for i, (w_, x, y) in enumerate(words):
        tag(g, w_, x, y + 10 * math.sin(c.gt * 2 + i), back_out(seg(c.t, 0.4 + i * 0.35, 0.35), 1.6), 54)
    with g.at(1700, 650, 0.2 * math.sin(c.gt), 1.0):
        g.path("M0 -60 L0 50 M-40 20 Q0 70 40 20 M-24 -40 L24 -40", None, INK, lw=14)
        g.circle(0, -72, 14, None, INK, lw=8)
    strip(g, c, 0)


def s_trucks(g, c, zoom_flows=False):
    kt = on(c, "right", 1.2) if not zoom_flows else 1.0
    apron_top(g, c.gt, 1.0, kt, hl="left")
    if zoom_flows:
        k = on(c, "so", 0.5)
        for i in range(3):
            u = (c.gt * 0.8 + i / 3) % 1
            g.circle(100 + 700 * u, 375, 16, "#3E7CB1", INK, lw=4, a=k)
        arrow(g, 1500, 900, 1300, 760, col="#FF8A3D", k=k)
        arrow(g, 400, 440, 760, 440, col="#7FC8E8", k=k)
    label(g, "RIGHT", 1560, 160, 90, k=pk(c, "right"))
    strip(g, c, 0)


def s_seat_phone(g, c):
    row(g, c, "smile", "deadpan", lights=1.0, night=False, kai_cid="kai_p", kai_pose=("down", "hold"))
    k = on(c, "phone")
    bubble(g, 1000, 280, "?", k, 80, tail=(-1, 1))
    strip(g, c, 0.5 * on(c, "phone"))


# ------------------------------------------------------------------ 2 airplane mode
def s_crash_myth(g, c):
    row(g, c, "shocked", "deadpan", night=False, kai_cid="kai_p", kai_view="3q")
    with g.at(1430, 260, 0, back_out(clamp(c.t / 0.4), 1.5)):
        g.ellipse(0, 0, 260, 150, "#FFFFFF", INK, lw=7)
        for i, (dx, dy, r) in enumerate(((-200, 150, 26), (-250, 200, 16))):
            g.circle(dx, dy, r, "#FFFFFF", INK, lw=5)
        with g.at(-40, 0, 0.6 + 0.3 * math.sin(c.gt * 3), 0.9):
            g.path("M-60 0 L44 -10 Q66 0 44 10 Z", "#F4F1EA", INK, lw=5)
            g.path("M-8 -5 L-28 -40 L-12 -40 L14 -5 Z", "#F4F1EA", INK, lw=4)
        g.rc(110, 0, 50, 86, "#1E1E26", INK, lw=5, r=10)
    strip(g, c, 1)


def s_never(g, c):
    studio(g, c.gt, "#3A4A66", "#141C2C")
    phone(g, 700, 560, 0.85, 0.0, c.gt, rot=-0.08)
    plane_side(g, 1360, 520, 0.42, c.gt)
    stamp(g, "NEVER PROVEN", 1000, 860, on(c, "proven", frac=0.7), size=100)
    strip(g, c, 1)


def s_towers(g, c, phase=0):
    if phase == 0:
        sky_towers(g, c.gt, hot=0.0)
    elif phase == 1:
        sky_towers(g, c.gt, hot=on(c, "many", 0.6))
    else:
        sky_towers(g, c.gt, hot=1.0)
    strip(g, c, 1)


def s_1991(g, c):
    studio(g, c.gt, "#3A4A66", "#141C2C")
    phone(g, 960, 560, 0.85, 0.0, c.gt)
    no_sign(g, 960, 520, 300, on(c, "banned", 0.4))
    tag(g, "1991 · USA", 960, 120, pk(c, "1991"), 56)
    strip(g, c, 1)


def cockpit(g, c, expr="deadpan", buzz=0.0, pose=("down", "hold"), sky=("#FF9A5A", "#5B3A8C"), mos=0.0, wave=0.0):
    cockpit_back(g, c.gt, sky)
    char2(g, "ade", 960, 1200, 900, expr, pose[0], pose[1], t=c.gt, view="front")
    headset(g, 960, 1200, 900, buzz=buzz, t=c.gt)
    if wave > 0:
        for j in range(2):
            ph = (c.gt * 0.8 + j / 2) % 1
            g.circle(960, 1200 - 0.86 * 900, 160 + 200 * ph, None, "#7FE0FF", lw=6, a=wave * (1 - ph))
    cockpit_front(g, c.gt)
    if mos > 0:
        mosquito(g, 1330, 330, 1.6 * back_out(clamp(mos), 1.5), c.gt)


def s_cockpit_intro(g, c):
    cockpit(g, c, "deadpan")
    strip(g, c, 1)


def s_buzz(g, c):
    kb = on(c, "buzzing", 0.4)
    cockpit(g, c, "suspicious" if kb > 0.5 else "deadpan", buzz=kb, mos=on(c, "mosquito", 0.4),
            pose=pose_at(c.t, [(0, ("down", "hold")), (tw(c, "headsets"), ("down", "think"))]))
    strip(g, c, 1)


def s_search(g, c):
    studio(g, c.gt, "#3A4A66", "#141C2C")
    for i, x in enumerate((420, 960, 1500)):
        phone(g, x, 600, 0.6, 0.0, c.gt + i * 0.3, rot=0.06 * (i - 1))
        for j in range(2):
            ph = (c.gt * 1.1 + j / 2 + i * 0.2) % 1
            g.circle(x, 340, 60 + 160 * ph, None, PAL["yellow"], lw=6, a=1 - ph)
    strip(g, c, 1)


def s_nuisance(g, c):
    cockpit(g, c, "bored", buzz=0.35)
    strip(g, c, 1)


def s_listen(g, c):
    cockpit(g, c, "deadpan", buzz=0.0, wave=1.0, pose=("down", "think"), sky=("#FFC28A", "#2E5A8C"))
    tag(g, "TAKEOFF", 560, 160, pk(c, "takeoff"), 52)
    tag(g, "LANDING", 1360, 160, pk(c, "landing"), 52)
    strip(g, c, 1)


def s_mode_on(g, c):
    studio(g, c.gt, "#2E6A6A", "#0E2A2A")
    m = on(c, "rule", 0.5)
    phone(g, 960, 560, 0.95, m, c.gt)
    check(g, 1260, 300, 70, pk(c, "might", frac=0.8))
    strip(g, c, 1)


def s_next_seat(g, c):
    row(g, c, "deadpan", "smile", night=False, kai_cid="kai_p", nia_view="3q", nia_flip=True)
    g.circle(SEATS[0], 360, 220 + 20 * math.sin(c.gt * 4), None, PAL["yellow"], lw=10, a=on(c, "seat"))
    strip(g, c, 1 + on(c, "seat"))


# ------------------------------------------------------------------ 3 upright seat
def s_trays_up(g, c):
    k = on(c, "Tray", 0.6)
    row(g, c, "bored", "deadpan", night=False, tray=(1 - k, 1 - k, 1 - k * 0.5))
    tag(g, "TAKEOFF + LANDING", 1500, 120, pk(c, "Every"), 48)
    strip(g, c, 2)


def s_fussy(g, c):
    row(g, c, "bored", "suspicious", night=False, nia_view="3q", nia_flip=True)
    strip(g, c, 2)


def s_ninety(g, c):
    studio(g, c.gt, "#8C2E2E", "#2A0B0B")
    tuc_clock(g, 960, 520, 300, 1 - 0.15 * c.u, clamp(c.t / 0.3), label="90 s")
    strip(g, c, 2)


def s_evac(g, c, phase=0):
    if phase == 0:
        evac_test(g, c.gt, people_k=0.0, blocked=0.0)
    elif phase == 1:
        evac_test(g, c.gt, people_k=on(c, "emptied", 0.5), blocked=0.0)
        tuc_clock(g, 1720, 160, 110, 1 - clamp((c.t - tw(c, "emptied")) / 6), on(c, "emptied"), "90 s")
    elif phase == 2:
        evac_test(g, c.gt, people_k=1.0, blocked=on(c, "half", 0.8))
        tuc_clock(g, 1720, 160, 110, 0.7, 1.0, "90 s")
    elif phase == 3:
        k = on(c, "dark", 0.3)
        evac_test(g, c.gt, people_k=1.0, blocked=1.0)
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#000000", None, a=0.45 * k)
    else:
        evac_test(g, c.gt, people_k=1.0, blocked=1.0)
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#000000", None, a=0.35)
        tag(g, "2006", 260, 120, 1.0 if phase == 5 else pk(c, "2006"), 56)
        if phase == 5:
            label(g, "873 PEOPLE", 620, 980, 96, k=pk(c, "eight"))
            label(g, "78 SECONDS", 1340, 980, 96, PAL["coral"], k=pk(c, "seventy-eight", frac=0.8))
    strip(g, c, 2)


def s_rows(g, c, phase=0):
    if phase == 0:
        row_top(g, c.gt, 0.0, 0.0, stand=0.5 + 0.5 * math.sin(c.gt * 2) * 0.2)
    elif phase == 1:
        row_top(g, c.gt, on(c, "reclined", 0.8), 0.0, stand=0.3)
    else:
        row_top(g, c.gt, 1.0, on(c, "tray", 0.6), stand=0.3 + 0.2 * on(c, "blocks"))
        cross(g, 1100, 320, 60, pk(c, "completely", frac=0.8))
    strip(g, c, 2)


def s_stuck(g, c):
    row_top(g, c.gt, 1.0, 1.0, stand=0.3)
    stamp(g, "STUCK", 700, 520, pk(c, "stuck"), size=110)
    strip(g, c, 2)


def s_phases(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3C8DD8", "#BFE6FF"))
    g.rect(-300, 860, 2600, 400, "#6FA34A", INK, lw=6)
    pts = [(160, 860), (520, 420), (700, 300), (1220, 300), (1400, 420), (1760, 860)]
    g.line(pts, "#FFFFFF", 10, a=0.5, dash=([24, 18],))
    kt, kl = on(c, "takeoff", 0.5), on(c, "landing", 0.5)
    g.line(pts[:3], "#FF5B4B", 16, a=kt)
    g.line(pts[3:], "#FF5B4B", 16, a=kl)
    u = clamp(c.u)
    i = min(4, int(u * 5)); f = u * 5 - i
    px, py = lerp(pts[i][0], pts[i + 1][0], f), lerp(pts[i][1], pts[i + 1][1], f)
    plane_side(g, px, py - 40, 0.18, c.gt)
    strip(g, c, 2)


def s_climb(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2E78C8", "#BFE6FF"))
    for i in range(8):
        x = (i * 290 - c.gt * 80) % 2400 - 200
        g.ellipse(x, 820 + (i % 3) * 40, 260, 70, "#FFFFFF", None, a=0.95)
    plane_side(g, 900 + 60 * c.u, 480 - 100 * c.u, 0.7, c.gt)
    strip(g, c, 2.5)


def s_window_hole(g, c, intro=True):
    z = 1.0 + 0.0 * c.u
    window_big(g, c.gt, hole_glow=on(c, "hole", 0.4) if intro else 1.0)
    strip(g, c, 3)


# ------------------------------------------------------------------ 4 window hole
def s_not_crack(g, c):
    window_big(g, c.gt, hole_glow=0.6)
    cross(g, 1280, 360, 60, pk(c, "crack"))
    label(g, "CRACK", 1460, 360, 64, PAL["cream"], k=pk(c, "crack"))
    cross(g, 1280, 520, 60, pk(c, "mistake"))
    label(g, "MISTAKE", 1490, 520, 64, PAL["cream"], k=pk(c, "mistake"))
    check(g, 1280, 680, 60, pk(c, "purpose"))
    label(g, "ON PURPOSE", 1520, 680, 64, k=pk(c, "purpose"))
    strip(g, c, 3)


def pane_labels(g, c, k_out=0.0, k_mid=0.0, k_in=0.0):
    tag(g, "OUTER", 1240, 1000, k_out, 46)
    tag(g, "MIDDLE", 1100, 80, k_mid, 46)
    tag(g, "INNER", 940, 1000, k_in, 46)


def s_layers(g, c, phase=0):
    pane_cut(g, c.gt, push=0.0, flow=0.0)
    if phase == 0:
        pane_labels(g, c, pk(c, "outer"), 0, 0)
        label(g, "3", 520, 300, 220, k=pk(c, "three"))
    elif phase == 1:
        pane_labels(g, c, 1, pk(c, "middle"), 0)
        tag(g, "SPARE", 1100, 170, pk(c, "spare"), 40)
    else:
        pane_labels(g, c, 1, 1, pk(c, "inner"))
        tag(g, "SPARE", 1100, 170, 1, 40)
        k = on(c, "fingers", 0.5)
        with g.at(860 - 300 * (1 - k) + 12 * math.sin(c.gt * 10) * k, 500):
            g.path("M-260 -30 L-30 -30 Q0 -30 0 0 Q0 30 -30 30 L-260 30 Z", "#C68E6A", INK, lw=7)
            g.path("M-40 -18 Q-14 -18 -14 0 Q-14 18 -40 18 Z", "#F2D0B8", INK, lw=4)
    strip(g, c, 3)


def s_push(g, c, phase=0):
    if phase == 0:
        pane_cut(g, c.gt, push=on(c, "pushes", 0.6), flow=0.0)
        tag(g, "CABIN AIR", 380, 120, 1.0, 46)
        tag(g, "THIN AIR", 1640, 120, pk(c, "outward"), 46)
    elif phase == 1:
        pane_cut(g, c.gt, push=1.0, flow=on(c, "breather", 0.5))
        g.circle(1100, 760, 70, None, PAL["yellow"], lw=8, a=on(c, "hole"))
    else:
        pane_cut(g, c.gt, push=1.0 + 0.2 * math.sin(c.gt * 6), flow=1.0)
        g.rc(1240, 500, 90, 760, None, PAL["yellow"], lw=10, r=30, a=on(c, "outer"))
    strip(g, c, 3)


def s_relax(g, c, fail=False):
    if not fail:
        pane_cut(g, c.gt, push=1.0, flow=1.0)
        sparkles(g, c.gt, [(1100, 300), (1100, 520), (1100, 650)], col=PAL["mint"], r=26)
    else:
        pane_cut(g, c.gt, push=1.0, flow=1.0, fail=on(c, "fails", 0.5))
        tag(g, "BACKUP", 1100, 80, pk(c, "take"), 46)
    strip(g, c, 3)


def s_fog(g, c):
    k = 1 - on(c, "escape", 1.2)
    window_big(g, c.gt, fog=k * (0.7 + 0.3 * math.sin(c.gt)), hole_glow=on(c, "hole") * 0.8)
    strip(g, c, 3)


def s_clouds_row(g, c):
    row(g, c, "smile", "smile", night=False, kai_view="3q", kai_flip=True, nia_view="3q", nia_flip=True)
    strip(g, c, 3.5)


def s_lunch(g, c):
    k = on(c, "lunch", 0.5)
    def ex(g):
        if k > 0:
            meal_tray(g, SEATS[0], 980, 0.34, c.gt, 0.0)
    kk = on(c, "strange", 0.3)
    row(g, c, "suspicious" if kk > 0.5 else "smile", "deadpan", night=False, tray=(k, 0.0, 0.0), extra=None,
        kai_pose=pose_at(c.t, [(0, ("down", "hold")), (tw(c, "tastes"), ("down", "up"))]))
    if k > 0:
        meal_tray(g, SEATS[0], 1010, 0.32 * k, c.gt)
    qmark(g, SEATS[0] + 200, 280, 110, k=pk(c, "strange", frac=0.8))
    strip(g, c, 3.5 + 0.5 * k)


# ------------------------------------------------------------------ 5 bland food
def s_tray_close(g, c):
    studio(g, c.gt, "#C9783E", "#3A1E0E")
    meal_tray(g, 960, 560, 1.15, c.gt, salt=0.0)
    strip(g, c, 4)


def s_its_you(g, c):
    row(g, c, "shocked", "smug", night=False, tray=(1.0, 0.0, 0.0), kai_pose=("down", "hold"), nia_view="3q", nia_flip=True)
    meal_tray(g, SEATS[0], 1010, 0.32, c.gt)
    label(g, "YOU", SEATS[0] + 260, 300, 110, k=pk(c, "you"))
    arrow(g, SEATS[0] + 200, 380, SEATS[0] + 90, 440, k=pk(c, "you"))
    strip(g, c, 4)


def s_lufthansa(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#5DB8F0", "#DDF2FF"))
    g.rect(-300, 820, 2600, 400, "#8FB86A", INK, lw=6)
    for i in range(6):
        g.ellipse(200 + i * 330, 160 + (i % 2) * 40, 150, 30, "#FFFFFF", None, a=0.8)
    plane_side(g, 960, 560, 0.85, c.gt)
    tag(g, "2010 · GERMANY", 960, 110, pk(c, "2010"), 56)
    strip(g, c, 4)


def s_chamber(g, c, phase=0):
    if phase == 0:
        chamber(g, c.gt, dry=0.0, low=0.0)
    else:
        chamber(g, c.gt, dry=on(c, "dry", 0.8), low=on(c, "thin", 0.8))
        tag(g, "THIN", 300, 840, pk(c, "thin"), 44)
        tag(g, "DRY", 1620, 840, pk(c, "dry"), 44)
    strip(g, c, 4)


def s_bars(g, c, umami=False):
    studio(g, c.gt, "#3A2A4A", "#120A1C")
    if not umami:
        ks = on(c, "Salt", 0.3)
        k = 0.5 * on(c, "weaker", 0.8) + 0.5 * on(c, "weaker#1", 0.8)
        taste_bars(g, 640, 380, k, items=(("SALT", 0.25), ("SUGAR", 0.18)), t=c.gt, w=800, size=60)
        label(g, "-20–30%", 1580, 380, 64, PAL["coral"], k=pk(c, "thirty"))
        label(g, "-15–20%", 1580, 520, 64, PAL["coral"], k=pk(c, "twenty#1"))
    else:
        taste_bars(g, 640, 300, 1.0, items=(("SALT", 0.25), ("SUGAR", 0.18), ("UMAMI", 0.0)), t=c.gt, w=800, size=60)
        g.rc(1040, 580, 840, 100, None, PAL["yellow"], lw=8, r=24, a=on(c, "Umami"))
        tomato(g, 1640, 580, 70, glow=on(c, "tomatoes"), t=c.gt)
    strip(g, c, 4)


def s_smell(g, c, phase=0):
    if phase == 0:
        row(g, c, "bored", "deadpan", night=False, tray=(1.0, 0.0, 0.0), kai_view="front")
        meal_tray(g, SEATS[0], 1010, 0.32, c.gt)
        k = 1 - on(c, "dries", 1.0)
        for i in range(3):
            ph = (c.gt * 0.6 + i / 3) % 1
            g.path(f"M{SEATS[0] - 40 + i * 40} {960 - 300 * ph} q 30 -40 0 -80", None, "#FFE6A0", lw=10, a=(0.3 + 0.7 * k) * (1 - ph))
    else:
        studio(g, c.gt, "#C9783E", "#3A1E0E")
        with g.at(800, 540, 0, 2.2):
            g.path("M0 -120 Q30 -30 60 40 Q70 70 40 80 Q20 90 0 76 Q-20 90 -40 80 Q-70 70 -60 40 Q-30 -30 0 -120 Z", "#C68E6A", INK, lw=6)
            g.circle(-22, 64, 10, "#5A3A2A", None); g.circle(22, 64, 10, "#5A3A2A", None)
        for i in range(4):
            ph = (c.gt * 0.7 + i / 4) % 1
            g.path(f"M{1500 - 500 * ph} {600 + 40 * math.sin(i)} q -40 -30 -80 0 q -40 30 -80 0", None, "#FFC93C", lw=10, a=1 - ph)
        label(g, "SMELL", 1400, 300, 110, k=pk(c, "smell"))
    strip(g, c, 4)


def s_odd(g, c):
    row(g, c, "suspicious", "smug", night=False, nia_view="3q", nia_flip=True)
    qmark(g, SEATS[0] + 180, 280, 110, k=pk(c, "odd"))
    strip(g, c, 4)


def juice_cart(g, x, y, s=1.0, t=0.0, pour=0.0):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 260, 380, "#C9CED6", INK, lw=8, r=16)
        g.rc(0, -40, 220, 10, "#9AA3AD", None)
        g.rc(0, 60, 220, 10, "#9AA3AD", None)
        for i in range(3):
            g.rc(-80 + i * 80, -230, 50, 90, "#D8432F", INK, lw=5, r=10)


def s_juice(g, c):
    kp = on(c, "order", 0.8)
    def pp(g, i):
        if i == 4:
            char2(g, "rosa", 820, 1040, 640, "smile", "down", "reach_r", t=c.gt, view="3q")
            juice_cart(g, 1120, 900, 0.75, c.gt)
            juice_glass(g, 1120, 690, 0.8, fill=0.2 + 0.8 * kp)
    aisle(g, c.gt, lights=1.0, people=pp)
    strip(g, c, 4)


def s_litres(g, c):
    studio(g, c.gt, "#8C2E2E", "#2A0B0B")
    n = 12
    for i in range(n):
        kk = back_out(seg(c.t, 0.1 + i * 0.12, 0.3), 1.6)
        if kk > 0:
            juice_glass(g, 300 + (i % 6) * 264, 420 + (i // 6) * 300, 0.85 * kk, fill=clamp((c.t - 0.2 - i * 0.12) / 0.6))
    label(g, "100,000s OF LITRES", 960, 980, 80, k=pk(c, "hundreds"))
    tag(g, "EVERY YEAR", 960, 120, pk(c, "year"), 48)
    strip(g, c, 4)


def s_ocean(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#2E78C8", "#BFE6FF"))
    g.rect(-300, 700, 2600, 500, g.lgrad(0, 700, 0, 1080, "#1E6AA8", "#0E3A6A"), None)
    for i in range(30):
        x = (i * 173 - c.gt * 40) % 2300 - 200; y = 740 + (i * 37) % 320
        g.path(f"M{x} {y} q 20 -10 40 0", None, "#7FC8E8", lw=5, a=0.7)
    plane_side(g, 700 + 120 * c.u, 360, 0.55, c.gt)
    strip(g, c, 4.5)


def s_card_pocket(g, c):
    g.fill_all("#DCD5C8")
    seat_back_view(g, 960, 120, 900, tray=0.0, card=False, t=c.gt)
    k = on(c, "safety", 0.5)
    with g.at(860, 640 - 120 * k, -0.08 + 0.06 * k, 1.0):
        g.rc(0, 0, 300, 240, "#FFF4E0", INK, lw=7, r=10)
        g.line([(-110, -80), (60, -80)], "#FF6B5B", 12)
        icon(g, "mask", -60, 20, 1.6, PAL["navy"], 8)
        icon(g, "door", 60, 20, 1.6, PAL["navy"], 8)
    strip(g, c, 5)


# ------------------------------------------------------------------ 6 mask first
def s_masks_drop(g, c):
    k = clamp((c.t - 0.15) / 0.7)
    row(g, c, "shocked", "shocked", night=False, panel=k, kai_view="front")
    strip(g, c, 5)


def s_mask_on(g, c, help_k=None):
    km = on(c, "mask", 0.8) if help_k is None else 1.0
    kh = help_k if help_k is not None else 0.0
    def th(g):
        pass
    row(g, c, "deadpan", "shocked", night=False, panel=2.0, mask_k=(km, kh), kai_view="3q" if help_k else "front",
        kai_pose=pose_at(c.t, [(0, ("down", "hold")), (0.4, ("up", "up")), (1.4, ("down", "reach_r") if help_k is not None else ("down", "hold"))]))
    if help_k is None:
        tag(g, "1", SEATS[0] - 260, 560, km, 60)
    else:
        tag(g, "1", SEATS[0] - 260, 560, 1.0, 60)
        tag(g, "2", SEATS[1] + 240, 560, kh, 60)
    strip(g, c, 5)


def s_selfish(g, c, phase=0):
    row(g, c, "deadpan", "smile", night=False, panel=2.0, mask_k=(1.0, 1.0), kai_view="3q")
    if phase == 0:
        label(g, "SELFISH?", 1500, 230, 100, PAL["cream"], k=pk(c, "selfish"))
    else:
        cross(g, 1250, 230, 60, 1.0)
        label(g, "SELFISH?", 1500, 230, 100, PAL["cream"], k=1.0)
        check(g, 1250, 400, 60, pk(c, "opposite"))
        label(g, "OPPOSITE", 1500, 400, 90, k=pk(c, "opposite"))
    strip(g, c, 5)


def s_altitude(g, c):
    g.fill_all(g.lgrad(0, 0, 0, H, "#0B1E4A", "#3C7AC8"))
    for i in range(6):
        g.ellipse((i * 380 - c.gt * 30) % 2300 - 200, 900 + (i % 2) * 50, 260, 60, "#FFFFFF", None, a=0.5)
    for i in range(7):
        g.circle(1300 + (i * 97) % 500, 160 + (i * 131) % 600, 10, "#FFFFFF", None, a=0.6)
    plane_side(g, 700, 500, 0.75, c.gt)
    tag(g, "35,000 ft", 1500, 120, pk(c, "thirty-five"), 56)
    strip(g, c, 5)


def s_tuc(g, c):
    studio(g, c.gt, "#8C2E2E", "#2A0B0B")
    k = clamp(c.t / 0.4)
    frac = 1 - clamp((c.t - tw(c, "thirty")) / 4.0) * 0.8
    tuc_clock(g, 960, 520, 320, frac, k, "30–60 s")
    strip(g, c, 5)


def s_tuc_name(g, c):
    cockpit(g, c, "deadpan", pose=pose_at(c.t, [(0, ("down", "hold")), (0.3, ("down", "explain"))]))
    tag(g, "TIME OF USEFUL CONSCIOUSNESS", 960, 110, pk(c, "time"), 50)
    tuc_clock(g, 1700, 300, 120, 0.5 + 0.5 * math.cos(c.gt), 1.0, "30–60 s")
    strip(g, c, 5)


def s_hypoxia(g, c, phase=0):
    if phase == 0:
        row(g, c, "deadpan", "deadpan", night=False, panel=2.0)
        cross(g, 1500, 260, 60, pk(c, "pain"))
        label(g, "NO PAIN", 1700, 260, 70, PAL["cream"], k=pk(c, "pain"))
    elif phase == 1:
        row(g, c, "smile", "smile", night=False, panel=2.0)
        sparkles(g, c.gt, [(560, 300), (980, 260), (1380, 330)], col=PAL["yellow"], r=26)
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#FFF4E0", None, a=0.18)
    else:
        row(g, c, "bored", "bored", night=False, panel=2.0)
        for i in range(3):
            qmark(g, 560 + i * 380, 260 + 20 * math.sin(c.gt * 3 + i), 90, k=back_out(seg(c.t, tw(c, "think") + i * 0.12, 0.3), 1.6), rot=0.2 * math.sin(c.gt + i))
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#2A1C3E", None, a=0.25)
    strip(g, c, 5)


def s_fumble(g, c, good=False):
    if not good:
        row(g, c, "bored", "bored", night=False, panel=2.0, kai_view="3q",
            kai_pose=("down", ("reach_r", "hold", 0.5 + 0.5 * math.sin(c.gt * 5))), mask_k=(0.0, 0.0))
        tuc_clock(g, 1560, 330, 110, 0.2, 1.0, "")
        cross(g, 1560, 560, 60, pk(c, "pass"))
    else:
        kh = on(c, "help", 0.8)
        row(g, c, "smile", "smile" if kh > 0.5 else "deadpan", night=False, panel=2.0, kai_view="3q",
            kai_pose=("down", "reach_r"), mask_k=(1.0, kh))
        check(g, 1700, 300, 70, pk(c, "need"))
    strip(g, c, 5)


def s_dive(g, c, chart=False):
    if not chart:
        cockpit(g, c, "deadpan", pose=("hold", "hold"), sky=("#BFE6FF", "#2E78C8"))
        tag(g, "A FEW MINUTES", 960, 110, pk(c, "few"), 52)
    else:
        studio(g, c.gt, "#2E5A8C", "#0B1730")
        alt_chart(g, 260, 140, 1400, 780, clamp(on(c, "dive", 3.0)), c.gt)
        check(g, 1560, 820, 56, pk(c, "breathe", frac=0.85))
    strip(g, c, 5)


def s_descent(g, c):
    landing_night(g, c.gt, lights=1.0, prog=0.3 * c.u)
    strip(g, c, 5 + 0.8 * on(c, "lights"))


# ------------------------------------------------------------------ 7 dim lights
def s_dim(g, c):
    k = on(c, "dim", 0.6)
    row(g, c, "deadpan", "bored", lights=1 - 0.82 * k, kai_view="3q")
    strip(g, c, 6)


def s_shade(g, c):
    k = on(c, "open", 0.8)
    row(g, c, "smile", "deadpan", lights=1.0, night=False, shade_k=1 - k, kai_view="3q", kai_flip=True,
        kai_pose=pose_at(c.t, [(0, ("down", "hold")), (tw(c, "open") - 0.3, ("down", "point"))]))
    strip(g, c, 6)


def s_eye(g, c, p0=0.3, p1=0.3, word=None, ok=False):
    studio(g, c.gt, "#2E5A8C", "#0B1730")
    k = on(c, word, 2.0) if word else clamp(c.u)
    eye_big(g, 960, 520, 220, lerp(p0, p1, k), clamp(c.t / 0.3))
    if ok:
        check(g, 1400, 300, 70, pk(c, "ready", frac=0.85))
    strip(g, c, 6)


def s_door_walk(g, c):
    dark_door(g, c.gt)
    k = clamp(c.u * 1.4)
    x = 400 + 900 * ease_io(k)
    char2(g, "kai", x, 1010, 760, "shocked" if x > 1060 else "smile", "down", "reach_r" if x > 1000 else "hold", t=c.gt, view="3q")
    if x > 1060:
        with g.screen():
            g.rect(1060, -50, W, H + 100, "#050810", None, a=0.75)
        qmark(g, x + 120, 260, 100, k=1.0)
    strip(g, c, 6)


def s_evac_dark(g, c):
    def pp(g, i):
        if i == 3:
            char2(g, "rosa", 1120, 905, 560, "deadpan", "down", "point", t=c.gt, view="3q", flip=True)
        if i == 5:
            char2(g, "kai", 820, 1060, 700, "deadpan", "down", "hold", t=c.gt, view="3q")
    aisle(g, c.gt, lights=0.2, people=pp)
    strip(g, c, 6)


def s_match(g, c):
    kb = on(c, "bright", 0.4)
    night = kb < 0.5
    row(g, c, "deadpan", "deadpan", lights=0.25 if night else 1.0, night=night, kai_view="3q", kai_flip=True)
    tag(g, "NIGHT" if night else "DAY", 960, 110, 1.0, 56)
    strip(g, c, 6)


def s_floorlights(g, c):
    aisle(g, c.gt, lights=0.15)
    arrow(g, 560, 900, 760, 1000, k=on(c, "floor"))
    arrow(g, 1400, 200, 1060, 300, k=on(c, "exit"))
    strip(g, c, 6)


def s_rescue(g, c, smoke=False):
    landing_night(g, c.gt, lights=1.0, prog=1.0)
    with g.at(300, 1030):
        g.rc(0, -70, 380, 140, "#D8432F", INK, lw=7, r=16)
        g.rc(-120, -110, 120, 70, "#9FDCF5", INK, lw=5, r=8)
        g.circle(-110, 0, 34, "#22262E", INK, lw=5); g.circle(110, 0, 34, "#22262E", INK, lw=5)
        g.rc(0, -150, 200, 16, "#FF5B4B", INK, lw=4, r=6, a=0.5 + 0.5 * ((c.gt * 3) % 1 < 0.5))
    char2(g, "fire", 620, 1060, 420, "deadpan", "down", "point", t=c.gt, view="3q")
    if smoke:
        for i in range(4):
            ph = (c.gt * 0.5 + i / 4) % 1
            puff(g, 1370 + 30 * i, 560 - 180 * ph, 30 + 40 * ph, "#9AA3AD", 0.6 * (1 - ph))
        g.circle(1280, 620, 70, None, PAL["yellow"], lw=8, a=on(c, "spot"))
    strip(g, c, 6)


def s_recap(g, c):
    studio(g, c.gt, "#2E5A8C", "#0B1730")
    words = ["left", "phone", "upright", "hole", "food", "mask", "dark"]
    with g.screen():
        for i, w_ in enumerate(words):
            kk = back_out(seg(c.t, tw(c, w_, frac=0.1 + i * 0.12) - 0.1, 0.3), 1.6)
            x = W / 2 - 600 + i * 200
            g.circle(x, 540, 82, "#FFC93C" if kk > 0.5 else "#24476B", PAL["cream"], lw=6)
            icon(g, ICONS[i], x, 540, 1.4, INK if kk > 0.5 else PAL["cream"], 8)
            if kk > 0:
                check(g, x + 60, 470, 26, kk)
        g.line([(W / 2 - 600, 680), (W / 2 + 600, 680)], PAL["cream"], 5, a=0.3, dash=([12, 14],))
        px = W / 2 - 600 + 1200 * clamp(c.u)
        with g.at(px, 680, 0, 1.4):
            g.path("M-30 0 L24 -6 Q36 0 24 6 Z", "#FF6B5B", INK, lw=4)
            g.path("M-4 -3 L-16 -22 L-6 -22 L8 -3 Z", "#FF6B5B", INK, lw=3)
            g.path("M-4 3 L-16 22 L-6 22 L8 3 Z", "#FF6B5B", INK, lw=3)
    label(g, "NOT RANDOM", 960, 230, 100, k=pk(c, "random"))


def s_comments(g, c):
    row(g, c, "smile", "smile", night=False, kai_view="3q", nia_view="3q", nia_flip=True)
    with g.screen():
        k = back_out(clamp(c.t / 0.4), 1.5)
        g.rc(W / 2 + 260, 200, 760, 150, "#FFFFFF", INK, lw=8, r=40)
        for i in range(7):
            icon(g, ICONS[i], W / 2 + 260 - 300 + i * 100, 200, 0.9 * k, PAL["navy"], 6)
    label(g, "WHICH ONE?", 1220, 380, 80, k=pk(c, "Which"))


def s_loop(g, c):
    ko = on(c, "out", 0.2)
    L = 1.0 if c.t < tw(c, "out") else lights_flicker(c.t, tw(c, "out"))
    kk = on(c, "know", 0.3)
    row(g, c, "smile" if kk > 0.5 else "deadpan", "bored", lights=L, kai_view="3q", kai_pose=("down", "hold"))
    zzz(g, SEATS[1] + 120, 330, c.gt)
    check(g, 1340, 230, 70, pk(c, "sleep", frac=0.9))


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
    if lid in V.T:
        V.shot(lid, fn, part=part, **kw)


Z = lambda z0, z1, f: push(z0, z1, f)
L = lambda f, *a, **k: (lambda g, c: f(g, c, *a, **k))

# cold open + 1 left door (ch0)
P("O01", s_hook, (0, "crew"), cam=Z(1.03, 1.08, (900, 520)), tr="cut", music="tension", sfx=[(0.0, "power_off", 0.5), (0.02, "whoosh", 0.35), (0.0, "jet_hum", 0.25)])
P("O01", s_outside_dim, ("crew", "On"), cam=Z(1.0, 1.06, (900, 480)), sfx=[("switches", "click", 0.4)])
P("O01", s_purpose, ("On", 1), cam=Z(1.02, 1.07, (960, 520)), sfx=[("purpose", "drum_hit", 0.35)])
P("O02", s_sleep, (0, "It's#1"), cam=Z(1.0, 1.05, (1000, 520)), sfx=[("not", "bloop", 0.35)])
P("O02", s_getout, ("It's#1", 1), cam=Z(1.0, 1.08, (960, 560)), sfx=[("out", "sting", 0.4), ("fast", "whoosh", 0.35)])
P("O03", s_things, (0, "So"), cam=Z(1.0, 1.04, (960, 540)), music="travel", sfx=[(0.2, "pop", 0.3), (0.6, "pop", 0.3), (1.0, "pop", 0.3)])
P("O03", s_journey, ("So", "seven"), cam=Z(1.0, 1.05, (960, 560)), sfx=[("flight", "whoosh_soft", 0.4)])
P("O03", s_seven, ("seven", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("seven", "ding", 0.4), ("reason", "pop", 0.35)])
V.pause["O03"] = 0.4
P("G01", card(1, "door", "LEFT DOOR"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("G02", s_bridge, cam=Z(1.0, 1.05, (760, 480)), sfx=[(0.2, "whir", 0.3), ("left", "ding", 0.4)])
P("G03", L(s_ship), (0, "Sailors"), cam=Z(1.0, 1.04, (900, 540)), music="curious", sfx=[(0.1, "waves", 0.3), ("ships", "gulls", 0.25)])
P("G03", L(s_ship, True), ("Sailors", "And"), cam=Z(1.05, 1.1, (760, 520)), sfx=[("port", "ding", 0.4)])
P("G03", s_words, ("And", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("words", "pop", 0.3), ("habits", "pop", 0.3)])
P("G04", L(s_trucks), cam=Z(1.0, 1.08, (1100, 520)), music="travel", sfx=[("right", "whoosh_soft", 0.4)])
P("G05", L(s_trucks), (0, "so"), cam=Z(1.12, 1.16, (1300, 560)), sfx=[(0.3, "whir", 0.25)])
P("G05", L(s_trucks, True), ("so", 1), cam=Z(1.0, 1.03, (960, 540)), sfx=[("way", "ding", 0.35)])
P("G06", s_seat_phone, cam=Z(1.0, 1.06, (900, 520)), sfx=[(0.1, "cabin_chime", 0.3), ("phone", "pop", 0.35)])
V.pause["G06"] = CH_PAUSE
# 2 airplane mode (ch1)
P("A01", card(2, "phone", "AIRPLANE MODE"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("A02", s_crash_myth, (0, "Investigators"), cam=Z(1.0, 1.05, (1000, 500)), music="curious", sfx=[("plane", "boing", 0.3)])
P("A02", s_never, ("Investigators", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("proven", "drum_hit", 0.4)])
P("A03", L(s_towers, 0), cam=camkf([(0, (960, 300, 1.25)), (1.0, (960, 540, 1.0))]), sfx=[("ground", "whoosh_soft", 0.35)])
P("A04", L(s_towers, 1), (0, "and"), cam=Z(1.0, 1.04, (960, 520)), sfx=[("many", "beep3", 0.3)])
P("A04", L(s_towers, 2), ("and", "That's"), cam=Z(1.05, 1.1, (960, 560)), sfx=[("calling", "beep3", 0.3)])
P("A04", s_1991, ("That's", 1), cam=Z(1.0, 1.05, (960, 540)), sfx=[("banned", "sting", 0.35)])
P("A05", s_cockpit_intro, (0, "Pilots"), cam=Z(1.0, 1.05, (960, 500)), music="tension", sfx=[(0.1, "jet_hum", 0.25)])
P("A05", s_buzz, ("Pilots", "when"), cam=Z(1.05, 1.12, (1060, 420)), sfx=[("buzzing", "buzz", 0.35), ("mosquito", "buzz_fast", 0.3)])
P("A05", s_search, ("when", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("search", "beep3", 0.3)])
P("A06", s_nuisance, (0, "But"), cam=Z(1.0, 1.05, (960, 480)), sfx=[(0.2, "buzz", 0.15)])
P("A06", s_listen, ("But", 1), cam=Z(1.04, 1.09, (960, 460)), sfx=[("takeoff", "ding", 0.3), ("landing", "ding", 0.3)])
P("A07", s_mode_on, cam=Z(1.0, 1.06, (960, 540)), music="cruise", sfx=[("rule", "click", 0.45), ("might", "chime", 0.35)])
P("A08", s_next_seat, cam=Z(1.0, 1.06, (800, 480)), sfx=[("seat", "pop", 0.35)])
V.pause["A08"] = CH_PAUSE
# 3 upright seat + 90 seconds (ch2)
P("S01", card(3, "seat", "UPRIGHT"), (0, "Seat"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("S01", s_trays_up, ("Seat", 1), cam=Z(1.0, 1.05, (1100, 600)), music="travel", sfx=[("upright", "click", 0.4), ("Tray", "thud", 0.35)])
P("S02", s_fussy, (0, "Ninety"), cam=Z(1.0, 1.04, (960, 520)))
P("S02", s_ninety, ("Ninety", 1), cam=Z(1.0, 1.06, (960, 520)), music="tension", sfx=[("Ninety", "drum_hit", 0.45), (("Ninety", 0.3), "tick", 0.3)])
P("S03", L(s_evac, 0), (0, "its"), cam=Z(1.0, 1.04, (960, 520)), sfx=[(0.2, "hum", 0.2)])
P("S03", L(s_evac, 1), ("its", "with"), cam=Z(1.03, 1.07, (900, 520)), sfx=[("emptied", "whoosh", 0.35), (("emptied", 0.5), "crowd_murmur", 0.2)])
P("S03", L(s_evac, 2), ("with", 1), cam=Z(1.06, 1.1, (1000, 480)), sfx=[("blocked", "thud", 0.4)])
P("S04", L(s_evac, 3), (0, "In"), cam=Z(1.0, 1.04, (960, 520)), sfx=[("dark", "power_off", 0.45)])
P("S04", L(s_evac, 4), ("In", "got"), cam=Z(1.04, 1.08, (960, 560)), sfx=[("2006", "ding", 0.35)])
P("S04", L(s_evac, 5), ("got", 1), cam=Z(1.0, 1.04, (960, 600)), sfx=[("eight", "pop", 0.4), ("seventy-eight", "crowd_cheer", 0.3)])
P("S05", L(s_rows, 0), (0, "A"), cam=Z(1.0, 1.03, (800, 540)), music="curious")
P("S05", L(s_rows, 1), ("A", "A#1"), cam=Z(1.05, 1.1, (800, 560)), sfx=[("reclined", "creak", 0.4)])
P("S05", L(s_rows, 2), ("A#1", 1), cam=Z(1.08, 1.12, (900, 620)), sfx=[("tray", "thud", 0.4), ("completely", "bloop", 0.35)])
P("S06", s_stuck, (0, "And"), cam=Z(1.0, 1.04, (800, 560)), sfx=[("stuck", "drum_hit", 0.35)])
P("S06", s_phases, ("And", 1), cam=Z(1.0, 1.03, (960, 540)), sfx=[("takeoff", "whoosh_soft", 0.3), ("landing", "whoosh_soft", 0.3)])
P("S07", s_climb, (0, "There's"), cam=Z(1.0, 1.04, (960, 540)), music="cruise", sfx=[(0.1, "jet_hum", 0.3)])
P("S07", s_window_hole, ("There's", 1), cam=camkf([(0, (960, 540, 1.0)), (0.75, (960, 770, 2.1))]), sfx=[("hole", "ding", 0.4)])
V.pause["S07"] = CH_PAUSE
# 4 window hole (ch3)
P("W01", card(4, "window", "TINY HOLE"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("W02", s_not_crack, cam=Z(1.0, 1.04, (1100, 540)), music="cruise", sfx=[("crack", "bloop", 0.35), ("mistake", "bloop", 0.35), ("purpose", "chime", 0.4)])
P("W03", L(s_layers, 0), (0, "The#2"), cam=Z(1.0, 1.04, (960, 540)), music="curious", sfx=[("three", "pop", 0.35), ("outer", "pop", 0.35)])
P("W03", L(s_layers, 1), ("The#2", "And"), cam=Z(1.06, 1.1, (1100, 540)), sfx=[("middle", "pop", 0.35)])
P("W03", L(s_layers, 2), ("And", 1), cam=Z(1.04, 1.08, (960, 540)), sfx=[("inner", "pop", 0.35), ("fingers", "boing", 0.3)])
P("W04", L(s_push, 0), (0, "The"), cam=Z(1.0, 1.04, (960, 540)), sfx=[("pushes", "whoosh", 0.4), ("hard", "thud", 0.35)])
P("W04", L(s_push, 1), ("The", "so"), cam=Z(1.12, 1.18, (1100, 720)), sfx=[("breather", "hiss", 0.3)])
P("W04", L(s_push, 2), ("so", 1), cam=Z(1.04, 1.08, (1150, 520)), sfx=[("outer", "ding", 0.35)])
P("W05", s_relax, (0, "ready"), cam=Z(1.0, 1.05, (1100, 520)), sfx=[("relaxed", "shimmer", 0.35)])
P("W05", L(s_relax, True), ("ready", 1), cam=Z(1.05, 1.1, (1150, 520)), sfx=[("fails", "glass_crack", 0.35)])
P("W06", s_fog, cam=Z(1.0, 1.06, (960, 560)), sfx=[("moisture", "hiss", 0.3), ("frost", "shimmer", 0.35)])
P("W07", s_clouds_row, (0, "while"), cam=Z(1.0, 1.04, (700, 520)), music="cruise")
P("W07", s_lunch, ("while", 1), cam=Z(1.02, 1.08, (800, 560)), music="playful", sfx=[("lunch", "thud", 0.35), ("strange", "boing", 0.35)])
V.pause["W07"] = CH_PAUSE
# 5 bland food (ch4)
P("F01", card(5, "fork", "BLAND FOOD"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("F02", s_tray_close, (0, "cooking"), cam=Z(1.0, 1.05, (960, 540)), music="playful", sfx=[(0.2, "chewing", 0.3)])
P("F02", s_its_you, ("cooking", 1), cam=Z(1.0, 1.06, (800, 500)), sfx=[("you", "drum_hit", 0.4)])
P("F03", s_lufthansa, (0, "asked"), cam=Z(1.0, 1.04, (960, 540)), music="curious", sfx=[("2010", "ding", 0.35)])
P("F03", L(s_chamber, 0), ("asked", "inside"), cam=Z(1.0, 1.04, (960, 520)), sfx=[("scientists", "hum", 0.25)])
P("F03", L(s_chamber, 1), ("inside", 1), cam=Z(1.04, 1.08, (960, 560)), sfx=[("thin", "hiss", 0.3), ("dry", "hiss", 0.3)])
P("F04", s_bars, cam=Z(1.0, 1.04, (1000, 480)), sfx=[("Salt", "pop", 0.35), ("weaker", "bloop", 0.35), ("Sugar", "pop", 0.35), ("weaker#1", "bloop", 0.35)])
P("F05", L(s_smell, 0), (0, "And"), cam=Z(1.0, 1.05, (800, 560)))
P("F05", L(s_smell, 1), ("And", 1), cam=Z(1.0, 1.05, (1000, 540)), sfx=[("smell", "sparkle", 0.35)])
P("F06", L(s_bars, True), cam=Z(1.0, 1.05, (1100, 520)), sfx=[("Umami", "chime", 0.4), ("tomatoes", "pop", 0.35)])
P("F07", s_odd, (0, "People"), cam=Z(1.0, 1.04, (900, 520)), music="playful", sfx=[("odd", "boing", 0.3)])
P("F07", s_juice, ("People", "Lufthansa"), cam=Z(1.0, 1.06, (1000, 600)), sfx=[("order", "pour", 0.4)])
P("F07", s_litres, ("Lufthansa", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("hundreds", "pop", 0.35), ("year", "ding", 0.35)])
P("F08", s_ocean, (0, "there's"), cam=Z(1.0, 1.04, (900, 500)), music="cruise", sfx=[(0.1, "waves", 0.25)])
P("F08", s_card_pocket, ("there's", 1), cam=Z(1.0, 1.06, (900, 560)), sfx=[("safety", "paper", 0.4)])
V.pause["F08"] = CH_PAUSE
# 6 mask first (ch5)
P("M01", card(6, "mask", "MASK FIRST"), (0, "If"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("M01", s_masks_drop, ("If", "put"), cam=Z(1.0, 1.04, (980, 520)), music="tension", sfx=[(0.1, "hiss", 0.4), ("drop", "thud", 0.35)])
P("M01", s_mask_on, ("put", "Even"), cam=Z(1.04, 1.1, (800, 480)), sfx=[("mask", "pop", 0.4)])
P("M01", L(s_mask_on, None), ("Even", 1), cam=Z(1.0, 1.05, (980, 500)))
P("M02", L(s_selfish, 0), (0, "It's"), cam=Z(1.0, 1.04, (1000, 520)), music="warm", sfx=[("selfish", "bloop", 0.35)])
P("M02", L(s_selfish, 1), ("It's", 1), cam=Z(1.03, 1.06, (1000, 520)), sfx=[("opposite", "chime", 0.4)])
P("M03", s_altitude, (0, "if"), cam=Z(1.0, 1.05, (960, 540)), music="tension", sfx=[("thin", "wind", 0.35)])
P("M03", s_tuc, ("if", "Pilots"), cam=Z(1.0, 1.05, (960, 520)), sfx=[("thirty", "tick", 0.4), ("minute", "tick", 0.35)])
P("M03", s_tuc_name, ("Pilots", 1), cam=Z(1.0, 1.04, (960, 480)), sfx=[("useful", "ding", 0.35)])
P("M04", L(s_hypoxia, 0), (0, "Often"), cam=Z(1.0, 1.04, (960, 520)), sfx=[("pain", "bloop", 0.3)])
P("M04", L(s_hypoxia, 1), ("Often", "And#1"), cam=Z(1.03, 1.08, (960, 500)), sfx=[("happy", "shimmer", 0.35)])
P("M04", L(s_hypoxia, 2), ("And#1", 1), cam=Z(1.06, 1.1, (960, 500)), sfx=[("think", "confuse", 0.35)])
P("M05", L(s_fumble), (0, "Mask"), cam=Z(1.0, 1.05, (980, 500)), sfx=[("fumble", "click", 0.3), ("pass", "drum_hit", 0.35)])
P("M05", L(s_fumble, True), ("Mask", 1), cam=Z(1.03, 1.06, (980, 500)), music="warm", sfx=[("first", "pop", 0.35), ("help", "chime", 0.4)])
P("M06", L(s_dive), (0, "The#1"), cam=Z(1.0, 1.05, (960, 480)), sfx=[(0.2, "jet_hum", 0.3)])
P("M06", L(s_dive, True), ("The#1", 1), cam=Z(1.0, 1.04, (960, 540)), sfx=[("dive", "whoosh", 0.4), ("breathe", "chime", 0.35)])
P("M07", s_descent, cam=Z(1.0, 1.06, (960, 560)), music="mystery", sfx=[("lights", "sting", 0.35)])
V.pause["M07"] = CH_PAUSE
# 7 dim lights + recap + loop (ch6)
P("L01", card(7, "bulb", "DARK CABIN"), tr="flash", cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.0, "cabin_chime", 0.5)])
P("L02", s_dim, (0, "And"), cam=Z(1.0, 1.05, (900, 520)), music="mystery", sfx=[("dim", "power_off", 0.4)])
P("L02", s_shade, ("And", 1), cam=Z(1.0, 1.05, (600, 520)), sfx=[("open", "whoosh_soft", 0.4)])
P("L03", L(s_eye, 0.3, 0.3), (0, "When"), cam=Z(1.0, 1.05, (960, 520)), music="curious", sfx=[("eyes", "pop", 0.35)])
P("L03", s_door_walk, ("When", "Your#1"), cam=Z(1.0, 1.04, (960, 540)), sfx=[(0.3, "footsteps", 0.3), ("blind", "sting", 0.35)])
P("L03", L(s_eye, 0.2, 0.85, "adjust"), ("Your#1", 1), cam=Z(1.0, 1.06, (960, 520)), sfx=[("adjust", "shimmer", 0.35)])
P("L04", s_evac_dark, (0, "So"), cam=Z(1.0, 1.05, (960, 560)), music="tension")
P("L04", s_match, ("So", "Your"), cam=Z(1.0, 1.05, (900, 520)), sfx=[("Dark", "power_off", 0.35), ("bright", "power_on", 0.35)])
P("L04", L(s_eye, 0.85, 0.85, None, True), ("Your", 1), cam=Z(1.0, 1.05, (960, 520)), music="warm", sfx=[("ready", "chime", 0.4)])
P("L05", s_floorlights, cam=Z(1.0, 1.06, (960, 640)), music="mystery", sfx=[("floor", "shimmer", 0.35), ("exit", "ding", 0.35)])
P("L06", L(s_rescue), (0, "spot"), cam=Z(1.0, 1.04, (900, 640)), sfx=[(0.2, "siren", 0.15)])
P("L06", L(s_rescue, True), ("spot", 1), cam=Z(1.05, 1.1, (1200, 600)), sfx=[("spot", "ding", 0.35)])
P("L07", s_recap, cam=Z(1.0, 1.03, (960, 540)), music="warm",
  sfx=[("left", "pop", 0.3), ("phone", "pop", 0.3), ("upright", "pop", 0.3), ("hole", "pop", 0.3), ("food", "pop", 0.3), ("mask", "pop", 0.3), ("dark", "pop", 0.3)])
P("L08", s_comments, cam=Z(1.0, 1.05, (1000, 520)), sfx=[("comments", "pop", 0.4)])
P("L09", s_loop, cam=Z(1.03, 1.08, (900, 520)), music="mystery", sfx=[("out", "power_off", 0.45), ("sleep", "cabin_chime", 0.3)])
V.build()
from flat_split import split_long
split_long(V, maxd=4.6, keep_cam=True)


def _fix_sfx():
    """A word-anchored sound effect belongs to the split shot that contains its word."""
    for sh in V.shots:
        keep = []
        for e in sh["sfx"]:
            off = e[0]
            if isinstance(off, str):
                wd, n = (off.split("#") + ["0"])[:2]
                try:
                    t = V.word_t(sh["line"], wd, int(n))
                except Exception:
                    keep.append(e); continue
                if not (sh["start"] - 0.05 <= t < sh["start"] + sh["dur"]):
                    tgt = [x for x in V.shots if x["line"] == sh["line"] and x["start"] - 0.05 <= t < x["start"] + x["dur"]]
                    if tgt:
                        tgt[0]["sfx"] = tgt[0]["sfx"] + [e]
                        continue
            keep.append(e)
        sh["sfx"] = keep


_fix_sfx()
END = 20.0
V.shots.append(dict(id=f"{V.sid}_END", line=V.shots[-1]["line"], fn=s_endscreen, part=(0, 1), cam=lambda c: (W / 2, H / 2, 1.0, 0.0), sfx=[(0.0, "whoosh_soft", 0.4)],
                    music="warm", tr="cut", cap=False, cap_y=None, name="end", start=V.duration, dur=END, kind="end", line_start=V.duration))
V.duration = round((V.duration + END) * FPS) / FPS
V.nframes = int(round(V.duration * FPS))

CHAPTERS = [("O01", "7 strange things on every flight"), ("G01", "1: Why you board on the left side"),
            ("A01", "2: Why airplane mode?"), ("S01", "3: Seat upright, tray up (the 90-second rule)"),
            ("W01", "4: The tiny hole in plane windows"), ("F01", "5: Why plane food tastes bland"),
            ("M01", "6: Why you put your own oxygen mask on first"), ("L01", "7: Why planes dim the lights to land"), ("L07", "All 7, recap")]


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
        V.render(str(EP / "final/B-009.mp4"))
