"""lib/flat_flight.py (B-009, 26 Nov 2026): Style F aviation sets, props and cast for 16:9 long videos. TrueWhys original, code-drawn.
Set TW_FLAT_SIZE=1920x1080 before importing flat2d.  from flat_flight import *
Cast: kai (traveller), rosa (flight attendant, fa_cap + scarf), ade (pilot, pilotcap + wings), nia (young passenger), fire (firefighter).
Sets: cabin_row_back/front (front view of a seat row, seated people between the two calls, lights dimmable), aisle (perspective aisle,
floor-path lights, exit sign), apron_top (top-down plane at the gate: jet bridge left, trucks right), dock_top (old ship tied port-side),
sky_towers (plane + many cell towers), cockpit_back/front (+ headset, buzz), evac_test (double-deck plane, slides, sliding people, blocked exits),
row_top (top-down rows: recline + tray), window_big (+ breather hole, fog), pane_cut (3-pane cross-section, pressure, air through the hole),
meal_tray, chamber (low-pressure test chamber with a cabin inside), taste_bars, tomato/juice, mask_panel/mask_on, alt_chart (dive 35k→10k ft),
landing_night (approach over runway lights), dark_door (bright room → dark doorway), eye_big (pupil), flight_strip (journey progress, icons only).
"""
import math
from flat2d import *
import cast2
from cast2_flat import char2
from flat_fx import arrow, ring_wave, puff, burst, sparkles

cast2.CAST.update({
    "kai":  dict(name="Kai", skin="#C68E6A", iris="#3A2A1E", face="round", hair="short", hair_c="#1E1A24", top="#3E8E7A", top2="#FFF4E0",
                 legs="#3A4A6A", shoes="#F4F1EA", jaw=0.1, prop=None),
    "rosa": dict(name="Rosa", skin="#E9BC98", iris="#4A3A2C", face="long", hair="fa_cap", hair_c="#3A2416", top="#24476B", top2="#FF6B5B",
                 legs="#24476B", shoes=INK, jaw=0.0, prop=None, female=True, scarf="#FFC93C", buttons=True),
    "ade":  dict(name="Captain Ade", skin="#8D5A3C", iris="#2A1C14", face="square", hair="pilotcap", hair_c="#1F2A44", top="#F4F1EA",
                 top2="#1F2A44", legs="#1F2A44", shoes=INK, jaw=0.3, prop=None, wings=True),
    "nia":  dict(name="Nia", skin="#C68E6A", iris="#3A2A1E", face="round", hair="bun", hair_c="#1E1A24", top="#FFC93C", top2="#FF6B5B",
                 legs="#3E7CB1", shoes="#FF6B5B", jaw=0.0, prop=None, female=True, hoodie=True),
    "fire": dict(name="Firefighter", skin="#E9BC98", iris="#3E5A7A", face="square", hair="helmet", hair_c="#D8432F", top="#2F3A4F", top2="#FFC93C",
                 legs="#2F3A4F", shoes=INK, jaw=0.3, prop=None, buttons=True),
})

NAVY_N = "#0A1630"
CABIN_W = "#E9E4DA"      # cabin wall (warm off-white)
SEAT = "#2F5F8C"
SEAT_D = "#1F426A"


def head_pt(x, y, h):
    """Approximate face centre (between eyes and mouth) of a front-facing char2 with feet at (x, y)."""
    return x, y - 0.83 * h


# ------------------------------------------------------------------ small props
def oval_window(g, cx, cy, w, h, t, night=True, shade=0.0, glow=0.0, city=True, frame="#D9D3C7"):
    """Cabin window seen from inside: frame, outside view (night sky + city lights or day sky), pull-down shade 0..1."""
    g.rc(cx, cy, w * 1.32, h * 1.25, frame, INK, lw=6, r=w * 0.55)
    with g.clip(d=_rr_path(cx, cy, w, h, w * 0.48)):
        if night:
            g.rect(cx - w, cy - h, 2 * w, 2 * h, g.lgrad(0, cy - h / 2, 0, cy + h / 2, "#061024", "#1B2C55"), None)
            for i in range(8):
                sx = cx - w / 2 + ((i * 53 + t * 18) % w); sy = cy - h / 2 + (i * 37 % int(h * 0.5))
                g.circle(sx, sy, 2.5, "#FFF4E0", None, a=0.8)
            if city:
                for i in range(14):
                    lx = cx - w / 2 + ((i * 41 + t * 60) % (w * 1.2)) - w * 0.1
                    g.circle(lx, cy + h * 0.32 + (i % 3) * 6, 3.5, "#FFC93C", None, a=0.9)
        else:
            g.rect(cx - w, cy - h, 2 * w, 2 * h, g.lgrad(0, cy - h / 2, 0, cy + h / 2, "#5DB8F0", "#CDEBFF"), None)
            g.ellipse(cx - w * 0.1 + (t * 12) % 40, cy + h * 0.25, w * 0.5, h * 0.12, "#FFFFFF", None, a=0.9)
        if glow:
            g.glow(cx, cy, w, "#FFE6A0", 0.5 * glow)
        if shade > 0:
            g.rect(cx - w, cy - h / 2 - 2, 2 * w, h * shade + 2, "#CFC8BA", INK, lw=4)
            g.rc(cx, cy - h / 2 + h * shade - 8, 40, 10, "#9A9284", None, r=4)
    g.rc(cx, cy, w, h, None, INK, lw=5, r=w * 0.48)


def _rr_path(cx, cy, w, h, r):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    r = min(r, w / 2, h / 2)
    return (f"M{x0 + r} {y0} L{x1 - r} {y0} Q{x1} {y0} {x1} {y0 + r} L{x1} {y1 - r} Q{x1} {y1} {x1 - r} {y1} "
            f"L{x0 + r} {y1} Q{x0} {y1} {x0} {y1 - r} L{x0} {y0 + r} Q{x0} {y0} {x0 + r} {y0} Z")


def seat_front(g, x, top, bottom, w=330, col=SEAT, cover="#F4F1EA"):
    """A seat facing the camera (seen from the front): tall back + headrest cover + armrests."""
    g.rc(x, (top + bottom) / 2, w, bottom - top, col, INK, lw=7, r=60)
    g.rc(x, top + 70, w * 0.62, 110, cover, INK, lw=5, r=26)
    g.line([(x - w * 0.36, top + 170), (x - w * 0.36, bottom - 40)], shade(col, 0.82), 6)
    g.line([(x + w * 0.36, top + 170), (x + w * 0.36, bottom - 40)], shade(col, 0.82), 6)


def seat_back_view(g, x, top, w=360, col=SEAT, tray=0.0, card=True, t=0.0):
    """The back of the seat in front (occluder for seated people): pocket with a card, tray table latch; tray 0..1 folds down toward us."""
    bottom = 1200
    g.rc(x, (top + bottom) / 2, w, bottom - top, col, INK, lw=8, r=56)
    g.rc(x, top + 60, w * 0.66, 70, "#F4F1EA", INK, lw=5, r=22)
    if tray < 1:
        g.rc(x, top + 210, w * 0.72, 230 * (1 - tray) + 2, mix(col, "#FFFFFF", 0.12), INK, lw=5, r=16)
        g.rc(x, top + 110, 46, 16, "#C9CED6", INK, lw=4, r=6)
    g.rc(x, top + 420, w * 0.76, 120, shade(col, 0.82), INK, lw=5, r=14)                  # seat pocket
    if card:
        g.rc(x - 40, top + 385, 90, 70, "#FFF4E0", INK, lw=4, r=6, rot=-0.08)
        g.line([(x - 70, top + 380), (x - 10, top + 376)], "#FF6B5B", 6)
    if tray > 0:
        k = ease_out(tray)
        d = 40 + 140 * k
        g.poly([(x - w * 0.42, top + 230 + d * 0.15), (x + w * 0.42, top + 230 + d * 0.15), (x + w * 0.5, top + 230 + d), (x - w * 0.5, top + 230 + d)],
               mix(col, "#FFFFFF", 0.22), INK, lw=6)


def cabin_row_back(g, t, win_x=330, seats=(760, 1200, 1640), night=True, shade_k=0.0):
    """Front view of a seat row: cabin side wall with a window on the left, overhead bins, seats facing the camera."""
    g.fill_all(CABIN_W)
    with g.layer(0.85):
        g.rect(-300, -200, 2600, 1500, g.lgrad(0, 0, 0, 1080, "#EFEBE3", "#DCD5C8"), None)
        # overhead bins + passenger service units
        g.poly([(-300, -40), (2300, -40), (2300, 150), (-300, 190)], "#F4F1EA", INK, lw=8)
        for i in range(-1, 6):
            g.line([(i * 430 + 100, -40), (i * 430 + 100, 168)], "#CFC8BA", 5)
            g.rc(i * 430 + 300, 120, 90, 20, "#3A3A44", None, r=8)
        for xx in (seats if seats else ()):
            g.circle(xx - 40, 205, 13, "#FFE29A", INK, lw=4)
            g.circle(xx + 30, 205, 10, "#B8C2CC", INK, lw=4)
        oval_window(g, win_x, 470, 190, 270, t, night=night, shade=shade_k)
    for x in seats:
        seat_front(g, x, 300, 960, 360)


def cabin_row_front(g, t, seats=(760, 1200, 1640), top=770, tray=0.0, lights=1.0, floor=True, exit_sign=True):
    """Seat backs of the row in front (hide the seated people's legs) + the lights level (1 = bright, 0 = dimmed for night landing)."""
    trays = tray if isinstance(tray, (tuple, list)) else [tray] * len(seats)
    for x, tr in zip(seats, trays):
        seat_back_view(g, x, top, 380, tray=tr, t=t)
    dim = clamp(1 - lights)
    if dim > 0:
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#061026", None, a=0.78 * dim)
            if exit_sign:
                g.glow(1820, 70, 160, "#7DFF9A", 0.35 * dim)
            if floor:
                for i in range(7):
                    g.glow(120 + i * 290, 1070, 70, "#FFB347", 0.5 * dim)


def aisle(g, t, lights=1.0, shades=0.0, vp=(960, 430), people=None):
    """Perspective view down the cabin aisle: bins, ceiling light strip, seat backs both sides, window rows, floor-path lights, exit sign.
    people(g, depth_index) is called between seat rows (far to near) so figures stand in the aisle at the right depth."""
    vx, vy = vp
    g.fill_all("#DCD5C8")
    with g.layer(0.9):
        g.rect(-400, -300, 2700, 1700, "#E6E0D5", None)
        g.poly([(-400, -300), (2320, -300), (vx + 170, vy - 110), (vx - 170, vy - 110)], "#F4F1EA", INK, lw=6)          # ceiling
        g.poly([(vx - 60, vy - 105), (vx + 60, vy - 105), (1180, -300), (740, -300)], "#FFF8E8", None, a=0.9 * (0.4 + 0.6 * lights))
        g.poly([(-400, 1500), (2320, 1500), (vx + 140, vy + 120), (vx - 140, vy + 120)], "#5A6A80", INK, lw=6)            # floor
        g.poly([(vx - 40, vy + 120), (vx + 40, vy + 120), (1240, 1500), (680, 1500)], "#8E3A40", None)                    # aisle carpet
        g.rc(vx, vy, 340, 230, "#CFC8BA", INK, lw=6, r=10)                                                                # back wall
        g.rc(vx, vy + 30, 90, 170, "#B8B0A2", INK, lw=5, r=8)                                                             # door
        g.rc(vx, vy - 70, 120, 40, "#1B3A2A", INK, lw=4, r=6)                                                             # exit sign
        g.text("EXIT", vx, vy - 68, 26, "#7DFF9A", stroke=None)
    # rows from far to near
    rows = 7
    for i in range(rows):
        k = (i + 1) / rows
        e = k ** 1.7
        y_top = vy - 40 + (1000 - (vy - 40)) * e * 0.62
        hh = 70 + 520 * e
        for side in (-1, 1):
            xc = vx + side * (80 + 900 * e)
            ww = 120 + 640 * e
            g.rc(xc, y_top + hh / 2, ww, hh, SEAT, INK, lw=3 + 5 * e, r=20 + 40 * e)
            g.rc(xc - side * ww * 0.12, y_top + hh * 0.12, ww * 0.5, hh * 0.16, "#F4F1EA", INK, lw=2 + 3 * e, r=10 + 12 * e)
            wy = vy - 30 - 220 * e
            g.ellipse(vx + side * (210 + 1200 * e), wy + 90 * e, 14 + 50 * e, 22 + 80 * e, "#14254A" if True else "#9FDCF5", INK, lw=2 + 3 * e)
            if shades > 0:
                g.ellipse(vx + side * (210 + 1200 * e), wy + 90 * e - (22 + 80 * e) * (1 - shades), 14 + 50 * e, (22 + 80 * e) * shades,
                          "#CFC8BA", None, a=0.95)
        if people:
            people(g, i)
    dim = clamp(1 - lights)
    if dim > 0:
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, "#061026", None, a=0.78 * dim)
        g.glow(vx, vy - 70, 120, "#7DFF9A", 0.5 * dim)
        for side in (-1, 1):
            pts = [(vx + side * 34 + side * (k ** 1.7) * 300, vy + 125 + (1500 - vy - 125) * k ** 1.7) for k in [j / 12 for j in range(13)]]
            for (px, py), j in zip(pts, range(13)):
                g.glow(px, py, 8 + 40 * (j / 12) ** 1.7, "#FFB347", 0.85 * dim)
                g.circle(px, py, 2 + 9 * (j / 12) ** 1.7, "#FFD68A", None, a=dim)


def headset(g, x, y, h, buzz=0.0, t=0.0):
    """Pilot headset on a front-facing char2 with feet at (x, y)."""
    hx, hy = x, y - 0.86 * h
    r = 0.15 * h
    g.path(f"M{hx - r} {hy} Q{hx - r * 1.05} {hy - r * 1.35} {hx} {hy - r * 1.4} Q{hx + r * 1.05} {hy - r * 1.35} {hx + r} {hy}", None, "#2A2A33", lw=0.03 * h)
    for sd in (-1, 1):
        g.rc(hx + sd * r, hy + 0.01 * h, 0.07 * h, 0.11 * h, "#3A3A44", INK, lw=0.008 * h, r=0.03 * h)
    g.path(f"M{hx - r} {hy + 0.04 * h} Q{hx - r * 0.9} {hy + 0.13 * h} {hx - 0.04 * h} {hy + 0.12 * h}", None, "#2A2A33", lw=0.012 * h)
    g.circle(hx - 0.04 * h, hy + 0.12 * h, 0.014 * h, "#2A2A33", None)
    if buzz > 0:
        for sd in (-1, 1):
            for j in range(3):
                ph = (t * 3 + j / 3) % 1
                xx = hx + sd * (r + 0.06 * h + ph * 0.18 * h)
                zz = " ".join(f"L{xx + sd * (i % 2) * 0.02 * h} {hy - 0.08 * h + i * 0.03 * h}" for i in range(7))
                g.path(f"M{xx} {hy - 0.08 * h} " + zz, None, "#FF5B4B", lw=0.008 * h, a=buzz * (1 - ph))


def mosquito(g, x, y, s=1.0, t=0.0, a=1.0):
    with g.at(x + 6 * math.sin(t * 9), y + 4 * math.cos(t * 13), 0.2 * math.sin(t * 7), s):
        for sd in (-1, 1):
            g.ellipse(sd * 22, -26, 26, 12, "#DFF4FF", INK, lw=3, a=a * 0.85, rot=sd * (0.5 + 0.3 * math.sin(t * 60)))
        g.ellipse(0, 0, 34, 12, "#4A3A3A", INK, lw=4, a=a)
        g.circle(-36, -2, 11, "#4A3A3A", INK, lw=4, a=a)
        g.line([(-46, 0), (-74, 10)], INK, 3, a=a)
        for i in range(3):
            g.line([(-14 + i * 14, 8), (-22 + i * 16, 34)], INK, 3, a=a)


def phone(g, x, y, s=1.0, mode=0.0, t=0.0, rot=0.0, hand="#C68E6A"):
    """Big phone in a hand; mode 0 = signal bars searching, 1 = airplane mode on (toggle slides, plane icon lights)."""
    with g.at(x, y, rot, s):
        g.rc(0, 0, 300, 560, "#1E1E26", INK, lw=10, r=48)
        g.rc(0, 0, 262, 500, g.lgrad(0, -250, 0, 250, "#20345A", "#3F6FA8"), None, r=30)
        g.rc(0, -232, 70, 14, "#1E1E26", None, r=7)
        # signal bars (searching = animated)
        for i in range(4):
            on_ = (1 - mode) * (1 if (t * 3 + i * 0.25) % 1 < 0.6 else 0.25)
            g.rect(-110 + i * 26, -170 - i * 18, 18, 30 + i * 18, "#FFFFFF", None, a=0.2 + 0.8 * on_)
        # toggle row
        g.rc(0, 40, 220, 92, "#FFFFFF", None, r=20, a=0.15)
        g.path("M-80 40 L-40 28 L-40 8 Q-34 -6 -28 8 L-28 28 L12 40 L12 50 L-28 42 L-28 62 L-16 70 L-16 78 L-34 72 L-52 78 L-52 70 L-40 62 L-40 42 L-80 50 Z",
               mix("#FFFFFF", "#FFC93C", mode), None)
        g.rc(64, 40, 96, 52, mix("#7A869A", "#FF9A2E", mode), INK, lw=4, r=26)
        g.circle(40 + 48 * ease_io(mode), 40, 21, "#FFFFFF", INK, lw=4)
        # hand
        g.path("M-170 120 Q-190 260 -120 330 L120 330 Q190 250 170 150 Q160 110 140 130 L140 200 L-140 200 L-140 110 Q-160 90 -170 120 Z", hand, INK, lw=8)
        g.ellipse(160, 60, 34, 70, hand, INK, lw=7, rot=0.2)


def tower(g, x, y, s=1.0, hot=0.0, t=0.0):
    with g.at(x, y, 0, s):
        g.poly([(-40, 0), (40, 0), (8, -260), (-8, -260)], None, "#7A869A", lw=8)
        for yy in (-60, -130, -200):
            g.line([(-30 + yy * -0.12, yy), (30 - yy * -0.12, yy)], "#7A869A", 6)
        g.rc(-18, -230, 16, 50, "#C9CED6", INK, lw=4, r=4); g.rc(18, -230, 16, 50, "#C9CED6", INK, lw=4, r=4)
        g.circle(0, -268, 9, "#FF5B4B", INK, lw=3)
        if hot > 0:
            ph = (t * 1.6) % 1
            g.circle(0, -240, 30 + 90 * ph, None, "#FFC93C", lw=6, a=hot * (1 - ph))


def plane_side(g, x, y, s=1.0, t=0.0, lights=1.0, dir=1, body="#F4F1EA", stripe="#FF6B5B", decks=1, doors=None, wins=16):
    """Generic airliner side view (our colours, no logos). dir=1 nose to the right."""
    with g.at(x, y, 0, s * dir, s):
        L, R = -600, 600
        hh = 150 if decks == 1 else 250
        g.path(f"M{R - 640} {-hh / 2 - 6} L{L + 60} {-hh / 2} L{L - 60} {-hh / 2 - 210} L{L - 150} {-hh / 2 - 210} L{L - 70} {-hh / 2 + 20} Z", body, INK, lw=8)   # fin
        g.path(f"M{L} {-hh / 2} L{R - 140} {-hh / 2} Q{R + 40} {-hh / 2 + 10} {R + 70} {hh * 0.18} Q{R + 20} {hh / 2} {R - 120} {hh / 2} L{L + 40} {hh / 2} "
               f"Q{L - 120} {hh * 0.2} {L - 90} {-hh / 2 + 20} Z", body, INK, lw=9)
        g.line([(L - 40, hh * 0.18), (R + 10, hh * 0.18)], stripe, 16)
        g.path(f"M{R - 40} {-hh / 2 + 22} L{R + 30} {-hh / 2 + 40} L{R + 40} {-hh / 2 + 66} L{R - 40} {-hh / 2 + 66} Z", "#1F2A44", INK, lw=5)   # cockpit window
        rowsy = [-hh * 0.12] if decks == 1 else [-hh * 0.28, hh * 0.05]
        for ry in rowsy:
            for i in range(wins):
                wx = L + 90 + i * (R - L - 260) / max(1, wins - 1)
                g.rc(wx, ry, 22, 32, mix("#2A3A55", "#FFE6A0", lights), INK, lw=3, r=10)
        for dx in (doors or []):
            for ry in rowsy:
                g.rc(dx, ry + 8, 40, 64 if decks == 2 else 92, "#E3DED4", "#7A869A", lw=4, r=8)
        g.path(f"M-160 {hh * 0.25} L120 {hh * 0.25} L-60 {hh * 0.25 + 70} L-240 {hh * 0.25 + 70} Z", shade(body, 0.85), INK, lw=7)   # wing (near)
        g.rc(-120, hh * 0.25 + 64, 150, 50, "#C9CED6", INK, lw=6, r=24)                                                                  # engine


def sky_towers(g, t, hot=0.0, plane_x=960, buzz=0.0):
    g.fill_all(g.lgrad(0, 0, 0, H, "#3C8DD8", "#BFE6FF"))
    with g.layer(0.4):
        for i in range(5):
            g.ellipse(-200 + ((i * 520 + t * 30) % 2400), 140 + (i % 3) * 90, 160, 34, "#FFFFFF", None, a=0.8)
    with g.layer(0.8):
        g.rect(-300, 820, 2600, 400, "#6FA34A", INK, lw=7)
        for i in range(16):
            bx = -150 + i * 150
            g.rect(bx, 820 - 40 - (i * 37 % 70), 90, 40 + (i * 37 % 70), ["#E8C9A0", "#C9D6E8", "#F2B05A"][i % 3], INK, lw=4)
    xs = [180, 470, 760, 1120, 1450, 1760]
    for i, x in enumerate(xs):
        tower(g, x, 830, 1.0, hot, t + i * 0.17)
    px, py = plane_x, 250
    if hot > 0:
        for i, x in enumerate(xs):
            g.line([(px, py + 30), (x, 560)], "#FFC93C", 5, a=hot * 0.8, dash=([18, 14],))
    plane_side(g, px, py, 0.32, t)


def cockpit_back(g, t, sky=("#FF9A5A", "#5B3A8C")):
    """Cockpit seen from the instrument panel: big windows with a dusk runway behind the pilot's seat."""
    g.fill_all("#2A2F3A")
    with g.layer(0.7):
        g.rect(-300, -200, 2600, 1500, "#3A404C", None)
        for sd in (-1, 1):
            pts = [(960 + sd * 120, 60), (960 + sd * 900, 120), (960 + sd * 1000, 560), (960 + sd * 140, 520)]
            g.poly(pts, g.lgrad(0, 60, 0, 560, sky[1], sky[0]), INK, lw=10)
        g.rect(-300, 500, 2600, 30, "#1E222A", None)
    with g.layer(0.85):
        g.rc(960, 640, 520, 700, "#4A5060", INK, lw=8, r=80)          # seat back behind the pilot
        g.rc(960, 360, 300, 150, "#5A6070", INK, lw=6, r=40)


def cockpit_front(g, t, glow=1.0):
    """Instrument panel occluder (hides the pilot's legs)."""
    g.poly([(-300, 760), (2300, 760), (2300, 1300), (-300, 1300)], "#22262E", INK, lw=9)
    g.line([(-300, 770), (2300, 770)], "#3A404C", 14)
    for i, x in enumerate((360, 680, 1240, 1560)):
        g.rc(x, 900, 260, 180, "#0B1220", INK, lw=6, r=14)
        if i % 2 == 0:
            g.circle(x, 900, 60, None, "#7FE0FF", lw=5, a=glow)
            g.line([(x, 900), (x + 50 * math.cos(t + i), 900 + 50 * math.sin(t + i))], "#7FE0FF", 5, a=glow)
        else:
            g.rect(x - 110, 880, 220, 60, g.lgrad(0, 880, 0, 940, "#3C8DD8", "#8E5A2A"), None, a=glow)
            g.line([(x - 110, 910 + 10 * math.sin(t * 0.7)), (x + 110, 910 - 10 * math.sin(t * 0.7))], "#FFFFFF", 4, a=glow)
    for i in range(10):
        g.circle(900 + (i % 5) * 30, 880 + (i // 5) * 40, 9, ["#FF5B4B", "#7DFF9A", "#FFC93C"][i % 3], INK, lw=3, a=0.4 + 0.6 * ((t * 2 + i * 0.3) % 1 < 0.5))


def apron_top(g, t, k_bridge=1.0, k_trucks=1.0, hl=None):
    """Top-down: plane at the gate, nose up. Jet bridge to the LEFT front door; baggage, fuel and catering trucks on the RIGHT."""
    g.fill_all("#6E7684")
    with g.layer(0.95):
        g.rect(-300, -200, 2600, 1500, "#7A8290", None)
        for i in range(-3, 20):
            g.rect(i * 130, -200, 3, 1500, "#828A98", None)
        g.line([(960, -200), (960, 1300)], "#FFC93C", 8, dash=([40, 30],))
        g.rect(-300, -200, 360, 1500, "#C9D6E8", INK, lw=8)                     # terminal
        for i in range(8):
            g.rect(40, 40 + i * 130, 20, 80, "#7FC8E8", INK, lw=3)
    cx, nose = 960, 120
    # plane (top view)
    g.path(f"M{cx} {nose} Q{cx + 70} {nose + 30} {cx + 70} {nose + 160} L{cx + 70} {nose + 760} Q{cx + 60} {nose + 860} {cx} {nose + 900} "
           f"Q{cx - 60} {nose + 860} {cx - 70} {nose + 760} L{cx - 70} {nose + 160} Q{cx - 70} {nose + 30} {cx} {nose} Z", "#F4F1EA", INK, lw=9)
    g.path(f"M{cx - 66} {nose + 360} L{cx - 600} {nose + 560} L{cx - 600} {nose + 610} L{cx - 66} {nose + 520} Z", "#E3DED4", INK, lw=8)
    g.path(f"M{cx + 66} {nose + 360} L{cx + 600} {nose + 560} L{cx + 600} {nose + 610} L{cx + 66} {nose + 520} Z", "#E3DED4", INK, lw=8)
    for sd in (-1, 1):
        g.rc(cx + sd * 300, nose + 470, 60, 120, "#C9CED6", INK, lw=6, r=20)
        g.path(f"M{cx + sd * 20} {nose + 800} L{cx + sd * 230} {nose + 860} L{cx + sd * 230} {nose + 890} L{cx + sd * 20} {nose + 870} Z", "#E3DED4", INK, lw=6)
    g.path(f"M{cx - 40} {nose + 60} Q{cx} {nose + 40} {cx + 40} {nose + 60} L{cx + 34} {nose + 80} Q{cx} {nose + 66} {cx - 34} {nose + 80} Z", "#1F2A44", None)
    g.line([(cx, nose + 140), (cx, nose + 860)], "#FF6B5B", 10, a=0.8)
    # doors
    g.rc(cx - 70, nose + 230, 16, 50, "#FFC93C" if hl == "left" else "#7A869A", INK, lw=4, r=4)
    g.rc(cx + 70, nose + 230, 16, 50, "#7A869A", INK, lw=4, r=4)
    # jet bridge (extends from the terminal)
    kb = ease_io(clamp(k_bridge))
    x1 = 60 + (cx - 80 - 60) * kb
    g.rect(60, nose + 205, x1 - 60, 100, "#C9CED6", INK, lw=7)
    for i in range(int((x1 - 60) / 60)):
        g.line([(80 + i * 60, nose + 205), (80 + i * 60, nose + 305)], "#9AA3AD", 4)
    g.rc(x1, nose + 255, 40, 120, "#9AA3AD", INK, lw=6, r=8)
    # trucks on the right (drive in)
    kt = ease_out(clamp(k_trucks))
    def truck(x, y, col, w=90, l=180, ang=0.0, tank=False, label=None):
        with g.at(x, y, ang):
            g.rc(0, 0, w, l, col, INK, lw=6, r=14)
            g.rc(0, -l / 2 + 30, w - 10, 50, shade(col, 0.8), INK, lw=4, r=10)
            if tank:
                g.rc(0, 30, w - 20, l - 80, "#E8EEF2", INK, lw=4, r=30)
    truck(cx + 200 + 400 * (1 - kt), nose + 210, "#FFC93C", 90, 170, 0.0)                      # catering (to the right door)
    truck(cx + 320 + 500 * (1 - kt), nose + 640, "#E8EEF2", 100, 230, 0.15, tank=True)         # fuel (under the right wing)
    with g.at(cx + 190 + 500 * (1 - kt), nose + 300, -0.5):                                    # belt loader
        g.rc(0, 0, 70, 220, "#3E8E7A", INK, lw=6, r=10)
        for i in range(5):
            g.line([(-30, -90 + i * 45), (30, -90 + i * 45)], "#2A5A4E", 5)
    for i in range(3):                                                                          # baggage carts
        g.rc(cx + 380 + i * 110 + 500 * (1 - kt), nose + 400, 90, 60, "#3E7CB1", INK, lw=5, r=8)
        g.rc(cx + 380 + i * 110 + 500 * (1 - kt), nose + 400, 70, 40, "#FF8A3D", INK, lw=3, r=6)


def dock_top(g, t):
    """Top-down: an old sailing ship tied up with its LEFT side to a wooden dock (the port side)."""
    g.fill_all("#2E7DA8")
    with g.layer(0.95):
        g.rect(-300, -200, 2600, 1500, "#2E7DA8", None)
        for i in range(30):
            x = (i * 173 + t * 25) % 2300 - 200; y = (i * 97) % 1100
            g.path(f"M{x} {y} Q{x + 30} {y - 10} {x + 60} {y}", None, "#7FC8E8", lw=5, a=0.6)
        g.rect(-300, -200, 980, 1500, "#9A6A3E", INK, lw=8)                     # dock planks
        for i in range(-3, 9):
            g.line([(-300, i * 120), (680, i * 120)], "#7A5236", 5)
        for y in (200, 520, 840):
            g.circle(620, y, 30, "#5B3A29", INK, lw=6)
    cx, cy = 870, 540
    with g.at(cx, cy):
        g.path("M0 -470 Q170 -300 170 0 Q170 320 110 440 L-110 440 Q-170 320 -170 0 Q-170 -300 0 -470 Z", "#8E5A2A", INK, lw=10)
        g.path("M0 -420 Q140 -280 140 0 Q140 300 90 410 L-90 410 Q-140 300 -140 0 Q-140 -280 0 -420 Z", "#C9925A", INK, lw=5)
        for i in range(-6, 8):
            g.line([(-130, i * 55), (130, i * 55)], "#B07A4A", 4)
        for y in (-200, 40, 260):
            g.circle(0, y, 26, "#5B3A29", INK, lw=5)
            g.rc(0, y, 300, 26, "#F4F1EA", INK, lw=5, r=10)
    for y in (200, 840):
        g.line([(620, y), (cx - 160, cy + (y - 520) * 0.6)], "#E8D2A0", 7)


def evac_test(g, t, people_k=1.0, blocked=0.0):
    """Night hangar evacuation test: double-deck airliner, slides from half the doors, tiny people sliding; blocked doors get a red X."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#0E1A2E", "#22324A"))
    with g.layer(0.6):
        g.rect(-300, -200, 2600, 1500, "#141F33", None)
        for i in range(12):
            g.line([(-300 + i * 230, -200), (-300 + i * 230 + 120, 760)], "#1E2B44", 10)
        for i in range(5):
            g.glow(200 + i * 380, 40, 160, "#9FD8FF", 0.15)
    g.rect(-300, 780, 2600, 500, "#2A3446", INK, lw=6)
    plane_side(g, 960, 470, 1.25, t, lights=0.9, decks=2, doors=[-420, -100, 220, 470], wins=18)
    doors = [(960 + 1.25 * dx, 470 + 1.25 * (dy + 30)) for dx, dy in ((-420, 12.5), (-100, 12.5), (220, 12.5), (470, 12.5), (-420, -70), (220, -70), (-100, -70), (470, -70))]
    open_ = [0, 2, 5, 7]
    for j, (dx, dy) in enumerate(doors):
        if j in open_:
            ex, ey = dx - 260 if j % 2 == 0 else dx + 260, 800
            g.poly([(dx - 20, dy), (dx + 20, dy), (ex + 50, ey), (ex - 50, ey)], "#FFC93C", INK, lw=6)
            for p in range(5):
                u = ((t * 0.9 + p / 5 + j * 0.13) % 1)
                if people_k <= 0: break
                px, py = dx + (ex - dx) * u, dy + (ey - dy) * u
                g.circle(px, py - 22, 14, ["#FF6B5B", "#3E7CB1", "#6FA34A", "#FFF4E0", "#B57AE0"][(p + j) % 5], INK, lw=3, a=people_k)
                g.circle(px, py - 44, 10, "#E9BC98", INK, lw=3, a=people_k)
        elif blocked > 0:
            k = back_out(clamp(blocked * 2 - j * 0.1), 1.6)
            if k > 0:
                with g.at(dx, dy, 0, k):
                    g.line([(-26, -26), (26, 26)], "#FF3B30", 12); g.line([(-26, 26), (26, -26)], "#FF3B30", 12)


def row_top(g, t, recline=0.0, tray=0.0, stand=0.0, gap_lbl=1.0):
    """Top-down seat rows (3 rows, left block) with the aisle on the right: reclined seat + tray table close the escape gap."""
    g.fill_all("#5A6A80")
    with g.layer(0.95):
        g.rect(-300, -200, 2600, 1500, "#5A6A80", None)
        g.rect(1180, -200, 300, 1500, "#8E3A40", INK, lw=6)                      # aisle
        g.rect(1480, -200, 900, 1500, "#5A6A80", None)
    ys = [180, 520, 860]
    for r, y in enumerate(ys):
        for i in range(3):
            x = 380 + i * 270
            rec = recline if r == 1 else 0.0
            g.rc(x, y + 60, 230, 170, SEAT, INK, lw=7, r=26)                        # cushion
            g.rc(x, y + 170 + 50 * rec, 230, 60 + 30 * rec, SEAT_D, INK, lw=7, r=20)  # back (reclines toward the row behind)
            if r == 2 and i == 2:
                pass
    # tray table of row 2 (middle row's back) folded down toward row 3
    if tray > 0:
        k = ease_out(tray)
        g.rc(920, ys[1] + 240 + 60 * k, 190, 90 * k + 2, "#9FB4C8", INK, lw=6, r=10)
    # the escape gap between row 2's seat back and row 3 (yellow band shrinks)
    gap = max(8, 150 - 80 * recline - 62 * tray)
    yy0 = ys[1] + 200 + 50 * recline + (90 * ease_out(tray) if tray > 0 else 0)
    if gap_lbl > 0:
        g.rect(250, yy0, 800, gap, "#FFC93C", None, a=0.35 * gap_lbl)
        g.line([(1100, yy0), (1100, yy0 + gap)], "#FFC93C", 8, a=gap_lbl)
        g.line([(1070, yy0), (1130, yy0)], "#FFC93C", 6, a=gap_lbl); g.line([(1070, yy0 + gap), (1130, yy0 + gap)], "#FFC93C", 6, a=gap_lbl)
    # passenger (top view: shoulders, arms, head) in row 3 window seat, trying to get out toward the aisle
    px = 380 + 760 * ease_io(stand) * (1 if gap > 60 else 0.18)
    py = ys[2] + 60
    with g.at(px, py):
        g.ellipse(0, 0, 92, 46, "#3E8E7A", INK, lw=6)
        g.limb([(-80, 4), (-70, 60)], "#3E8E7A", 26); g.limb([(80, 4), (70, 60)], "#3E8E7A", 26)
        g.circle(0, -6, 38, "#1E1A24", INK, lw=5)
        g.ellipse(0, -40, 14, 8, "#C68E6A", None)


def window_big(g, t, cx=960, cy=520, a=1.0, hole=0.0, fog=0.0, sun=True, wall=CABIN_W, hole_glow=0.0):
    """Close-up of a cabin window at cruising height: clouds below, sun, the breather hole near the bottom of the inner pane."""
    g.fill_all(wall)
    with g.layer(0.95):
        g.rect(-300, -200, 2600, 1500, g.lgrad(0, 0, 0, 1080, "#EFEBE3", "#DCD5C8"), None)
        g.rc(cx, cy, 560 * a, 760 * a, "#D9D3C7", INK, lw=10, r=260 * a)
        with g.clip(d=_rr_path(cx, cy, 440 * a, 640 * a, 210 * a)):
            g.rect(cx - 400, cy - 500, 800, 1000, g.lgrad(0, cy - 320 * a, 0, cy + 320 * a, "#2E78C8", "#9ED4FF"), None)
            if sun:
                g.glow(cx + 120 * a, cy - 160 * a, 240 * a, "#FFF4C0", 0.8)
                g.circle(cx + 120 * a, cy - 160 * a, 40 * a, "#FFF8D8", None)
            for i in range(7):
                x = cx - 300 * a + ((i * 170 + t * 40) % (700 * a))
                y = cy + 140 * a + (i % 3) * 40 * a
                g.ellipse(x, y, 120 * a, 40 * a, "#FFFFFF", None, a=0.95)
                g.ellipse(x + 60 * a, y - 20 * a, 70 * a, 34 * a, "#FFFFFF", None, a=0.95)
            if fog > 0:
                g.rect(cx - 400, cy - 500, 800, 1000, "#E8F0F4", None, a=0.75 * fog)
                for i in range(20):
                    g.circle(cx - 200 * a + (i * 61) % (400 * a), cy - 280 * a + (i * 89) % (560 * a), 10 * a, "#FFFFFF", None, a=0.6 * fog)
            g.path(f"M{cx - 150 * a} {cy - 250 * a} Q{cx - 180 * a} {cy - 50 * a} {cx - 120 * a} {cy + 120 * a}", None, "#FFFFFF", lw=12 * a, a=0.35)
        g.rc(cx, cy, 440 * a, 640 * a, None, INK, lw=8, r=210 * a)
        hx, hy = cx, cy + 250 * a
        if hole_glow > 0:
            g.circle(hx, hy, 60 * a, None, "#FFC93C", lw=10 * a, a=hole_glow)
        g.circle(hx, hy, 7 * a + 3 * hole, "#2A1C1E", None)


def pane_cut(g, t, push=0.0, flow=0.0, labels=1.0, fail=0.0):
    """Cross-section through a cabin window: cabin air (left, dense) | inner pane | middle pane with the hole | outer pane | thin air outside."""
    g.fill_all("#F2EEE6")
    with g.layer(0.95):
        g.rect(-300, -200, 1200, 1500, g.lgrad(0, 0, 0, 1080, "#FFF4E0", "#F6E2C2"), None)
        g.rect(1300, -200, 1200, 1500, g.lgrad(0, 0, 0, 1080, "#2E78C8", "#9ED4FF"), None)
        g.rect(900, -200, 400, 160, "#B9C9D4", INK, lw=8)
        g.rect(900, 860, 400, 400, "#B9C9D4", INK, lw=8)
    rnd_ = rnd(4)
    for i in range(46):                                      # cabin air: dense dots jiggling
        x = -150 + (i * 97) % 1000; y = 40 + (i * 61) % 900
        g.circle(x + 8 * math.sin(t * 3 + i), y + 8 * math.cos(t * 2.6 + i), 11, "#FF8A3D", None, a=0.7)
    for i in range(10):                                      # outside: thin air
        x = 1380 + (i * 151) % 520; y = 60 + (i * 211) % 900
        g.circle(x + 6 * math.sin(t * 2 + i), y, 9, "#FFFFFF", None, a=0.7)
    # panes
    inner_x, mid_x, out_x = 960, 1100, 1240
    g.rc(inner_x, 500, 18, 700, "#DDEFF8", INK, lw=5, r=8)
    g.rc(mid_x, 500, 34, 700, "#BFE3F5", INK, lw=6, r=10)
    bend = 26 * push * (1 - fail)
    g.path(f"M{out_x - 24} 150 Q{out_x - 24 + bend * 2} 500 {out_x - 24} 850 L{out_x + 24} 850 Q{out_x + 24 + bend * 2} 500 {out_x + 24} 150 Z", "#9FD3EE", INK, lw=7)
    # hole in the middle pane (near the bottom)
    hy = 760
    g.rc(mid_x, hy, 40, 22, "#F2EEE6", None)
    g.line([(mid_x - 17, hy - 11), (mid_x + 17, hy - 11)], INK, 5); g.line([(mid_x - 17, hy + 11), (mid_x + 17, hy + 11)], INK, 5)
    # air flowing through the hole into the gap between middle and outer panes
    if flow > 0:
        for i in range(8):
            u = (t * 0.6 + i / 8) % 1
            x = mid_x - 120 + 230 * u
            y = hy + 6 * math.sin(u * 9)
            if x > mid_x + 20:
                y = hy - (x - mid_x - 20) * 1.6 * (i % 3)
            g.circle(x, y, 9, "#FF8A3D", None, a=flow * 0.9)
    # pressure arrows onto the outer pane
    if push > 0:
        for j, y in enumerate((260, 420, 580, 740)):
            k = clamp(push * 1.5 - j * 0.12)
            arrow(g, out_x - 110, y, out_x - 38, y, col="#FF5B4B", w=16, k=k)
    if fail > 0:
        g.line([(out_x - 10, 200), (out_x + 14, 360), (out_x - 6, 500), (out_x + 18, 700)], INK, 5, a=fail)
        for j, y in enumerate((300, 520, 700)):
            arrow(g, mid_x - 110, y, mid_x - 26, y, col="#FF5B4B", w=14, k=fail)


def meal_tray(g, x, y, s=1.0, t=0.0, salt=0.0):
    with g.at(x, y, 0, s):
        g.rc(0, 0, 900, 520, "#9FB4C8", INK, lw=9, r=30)
        g.rc(0, 0, 820, 440, "#C9D6E2", None, r=22)
        g.circle(-120, 30, 190, "#FFFFFF", INK, lw=7)
        g.ellipse(-180, 30, 90, 70, "#F4E3B5", INK, lw=5)                  # rice
        g.ellipse(-60, 0, 80, 55, "#C9783E", INK, lw=5)                    # chicken
        for i in range(5):
            g.circle(-70 + i * 30, 120, 16, "#6FA34A", INK, lw=4)          # peas
        g.ellipse(250, -110, 90, 60, "#E3B270", INK, lw=6)                  # roll
        g.rc(250, 90, 130, 170, "#F4F1EA", INK, lw=6, r=20)                 # cup
        g.rc(250, 70, 110, 90, "#7FC8E8", None, r=10, a=0.6)
        with g.at(-360, -150, -0.3 + 0.5 * math.sin(t * 8) * salt):
            g.rc(0, 0, 60, 100, "#F4F1EA", INK, lw=5, r=14)
            g.rc(0, -56, 50, 22, "#C9CED6", INK, lw=4, r=6)
        if salt > 0:
            for i in range(6):
                g.circle(-340 + (i * 23) % 60, -60 + ((t * 300 + i * 40) % 160), 5, "#FFFFFF", INK, lw=2, a=salt)
        for i in range(3):
            ph = (t * 0.5 + i / 3) % 1
            g.path(f"M{-160 + i * 60} {-150 - 120 * ph} q 20 -30 0 -60", None, "#FFFFFF", lw=8, a=0.6 * (1 - ph))


def chamber(g, t, dry=0.0, low=0.0):
    """Low-pressure test chamber (big steel cylinder) with a section of airplane cabin inside, seen through a cut-away; gauges."""
    g.fill_all("#2A3446")
    with g.layer(0.7):
        g.rect(-300, -200, 2600, 1500, g.lgrad(0, 0, 0, 1080, "#33415A", "#1E2738"), None)
        for i in range(10):
            g.rect(-300 + i * 260, -200, 6, 1500, "#3A4A66", None)
    g.rect(-300, 900, 2600, 400, "#1A202C", INK, lw=6)
    g.rc(960, 520, 1500, 700, "#8A96A8", INK, lw=10, r=350)                # steel cylinder
    for i in range(9):
        g.line([(360 + i * 150, 175), (360 + i * 150, 865)], "#7A869A", 6)
    g.rc(960, 520, 1180, 520, "#F4F1EA", INK, lw=8, r=240)                  # cabin section inside (cut-away)
    with g.clip(d=_rr_path(960, 520, 1180, 520, 240)):
        g.rect(370, 640, 1180, 200, "#5A6A80", None)
        for i in range(5):
            g.rc(520 + i * 230, 560, 150, 200, SEAT, INK, lw=6, r=30)
            g.rc(520 + i * 230, 490, 100, 50, "#F4F1EA", INK, lw=4, r=14)
    # gauges
    for j, (x, lbl, v) in enumerate(((300, "PRESSURE", 1 - 0.75 * low), (1620, "HUMIDITY", 1 - 0.9 * dry))):
        g.circle(x, 960, 70, "#F4F1EA", INK, lw=7)
        a0 = math.pi * (1.2 - 1.4 * v)
        g.line([(x, 960), (x + 50 * math.cos(a0), 960 - 50 * math.sin(a0))], "#FF5B4B", 7)
        g.circle(x, 960, 8, INK, None)


def taste_bars(g, x, y, k=1.0, items=(("SALT", 0.25), ("SUGAR", 0.18)), t=0.0, w=700, size=52):
    """Before/after bars: each item's bar shrinks by its fraction (k animates the drop)."""
    for i, (lbl, drop) in enumerate(items):
        yy = y + i * 140
        kk = ease_io(clamp(k * 1.4 - i * 0.25))
        g.text(lbl, x - 40, yy, size, PAL["cream"], anchor="r", sw=size * 0.18)
        g.rc(x + w / 2, yy, w, 64, "#FFFFFF", INK, lw=5, r=18, a=0.15)
        ww = w * (1 - drop * kk)
        g.rect(x, yy - 32, ww, 64, "#FFC93C" if i == 0 else "#FF8AB8", INK, lw=5, r=18)
        if kk > 0.05:
            g.rect(x + ww, yy - 32, w - ww, 64, None, "#FF5B4B", lw=4, r=18, a=kk)


def tomato(g, x, y, r=60, glow=0.0, t=0.0):
    if glow > 0:
        g.glow(x, y, r * 2.6, "#FFE29A", 0.6 * glow)
    g.circle(x, y, r, "#E8402F", INK, lw=r * 0.1)
    g.ellipse(x - r * 0.35, y - r * 0.35, r * 0.25, r * 0.15, "#FF8A7A", None, rot=-0.5)
    for i in range(5):
        a0 = -math.pi / 2 + i * TAU / 5
        g.poly([(x, y - r * 0.85), (x + r * 0.5 * math.cos(a0), y - r * 0.85 + r * 0.35 * math.sin(a0) + r * 0.1),
                (x + r * 0.15 * math.cos(a0 + 0.6), y - r * 0.85)], "#4E8A3A", INK, lw=r * 0.05)


def juice_glass(g, x, y, s=1.0, fill=1.0, col="#D8432F"):
    with g.at(x, y, 0, s):
        g.poly([(-50, -130), (50, -130), (38, 70), (-38, 70)], "#FFFFFF", INK, lw=6, a=0.55)
        if fill > 0:
            top = 70 - 190 * fill
            g.poly([(-38 - 12 * (70 - top) / 200, top), (38 + 12 * (70 - top) / 200, top), (38, 70), (-38, 70)], col, None)
        g.poly([(-50, -130), (50, -130), (38, 70), (-38, 70)], None, INK, lw=6)
        g.line([(-30, -100), (-24, 40)], "#FFFFFF", 6, a=0.6)


def mask_panel(g, x, y, k=0.0, t=0.0, n=1, gap=110, s=1.0):
    """Ceiling panel opening and yellow oxygen masks dropping on their tubes, swinging. k 0..1."""
    with g.at(x, y, 0, s):
        g.rc(0, 0, 120 + gap * (n - 1), 30, "#E3DED4", INK, lw=5, r=6)
        if k <= 0:
            return
        kk = bounce(clamp(k))
        for i in range(n):
            mx = -gap * (n - 1) / 2 + i * gap
            sw = 0.18 * math.sin(t * 3.2 + i) * math.exp(-max(0, k - 1) * 0.5)
            L = 260 * kk
            ex, ey = mx + L * math.sin(sw), 10 + L * math.cos(sw)
            g.line([(mx, 10), (ex, ey)], "#BFE6F2", 6)
            g.path(f"M{ex - 30} {ey + 10} L{ex + 30} {ey + 10} L{ex + 22} {ey + 110} L{ex - 22} {ey + 110} Z", "#E8F6FF", INK, lw=4, a=0.8)   # bag
            g.ellipse(ex, ey + 4, 34, 22, "#FFC93C", INK, lw=5)


def mask_on(g, x, y, h, k=1.0):
    """Oxygen mask over the nose and mouth of a front-facing char2 (feet at x, y, height h)."""
    if k <= 0:
        return
    fx, fy = x, y - 0.80 * h
    r = 0.075 * h
    with g.at(fx, fy - (1 - k) * 0.4 * h, 0, 1.0):
        g.path(f"M{-0.13 * h} {-0.02 * h} Q0 {-0.07 * h} {0.13 * h} {-0.02 * h}", None, "#BFE6F2", lw=0.012 * h, a=k)
        g.ellipse(0, 0, r, r * 0.8, "#FFC93C", INK, lw=0.01 * h, a=k)
        g.line([(0, -r * 0.8), (0, -0.35 * h)], "#BFE6F2", 0.012 * h, a=k)


def alt_chart(g, x0, y0, w, h, k=0.0, t=0.0, tuc=0.0):
    """Altitude vs time: a plane dives from 35,000 ft to 10,000 ft (k = progress). Labels are numbers only."""
    g.rc(x0 + w / 2, y0 + h / 2, w, h, "#10263B", PAL["cream"], lw=6, r=24, a=0.92)
    ya, yb = y0 + 90, y0 + h - 90
    g.text("35,000 ft", x0 + 150, ya, 40, PAL["cream"], stroke=None)
    g.text("10,000 ft", x0 + 150, yb, 40, PAL["cream"], stroke=None)
    g.line([(x0 + 280, ya), (x0 + w - 40, ya)], "#FFFFFF", 3, a=0.25, dash=([10, 12],))
    g.line([(x0 + 280, yb), (x0 + w - 40, yb)], "#7DFF9A", 3, a=0.6, dash=([10, 12],))
    pts = []
    for i in range(41):
        u = i / 40
        xx = x0 + 300 + (w - 380) * u
        yy = ya + (yb - ya) * ease_io(clamp((u - 0.2) / 0.6))
        pts.append((xx, yy))
    n = max(2, int(41 * clamp(k)))
    g.line(pts[:n], "#FFC93C", 8)
    px, py = pts[n - 1]
    with g.at(px, py, math.atan2(pts[min(n, 40)][1] - pts[n - 2][1], pts[min(n, 40)][0] - pts[n - 2][0]) if n > 1 else 0, 0.9):
        g.path("M-40 0 L30 -8 Q46 0 30 8 Z", "#F4F1EA", INK, lw=4)
        g.path("M-6 -4 L-20 -30 L-8 -30 L10 -4 Z", "#F4F1EA", INK, lw=3)
        g.path("M-6 4 L-20 30 L-8 30 L10 4 Z", "#F4F1EA", INK, lw=3)


def tuc_clock(g, x, y, r, frac, k=1.0, label="30–60 s"):
    """Draining ring timer (time of useful consciousness)."""
    if k <= 0:
        return
    with g.at(x, y, 0, back_out(clamp(k), 1.5)):
        g.circle(0, 0, r, "#10263B", PAL["cream"], lw=r * 0.08)
        g.c.new_path(); g.c.arc(0, 0, r * 0.82, -math.pi / 2, -math.pi / 2 + TAU * clamp(frac))
        g.c.set_source_rgba(*rgba("#FF5B4B")); g.c.set_line_width(r * 0.18); g.c.stroke()
        g.text(label, 0, 6, r * 0.36, PAL["cream"], stroke=None)


def landing_night(g, t, lights=1.0, prog=0.0):
    """Night approach: runway lights converging, city glow, our plane side view gliding down; cabin window glow follows `lights`."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#050B1C", "#1B2C55"))
    with g.layer(0.3):
        for i in range(40):
            g.circle((i * 211) % 1920, (i * 97) % 520, 2.5, "#FFF4E0", None, a=0.7)
        g.circle(1600, 160, 60, "#F4F1EA", INK, lw=5)
    with g.layer(0.7):
        g.rect(-300, 760, 2600, 500, "#0B1530", None)
        for i in range(60):
            g.circle(-200 + (i * 53) % 2400, 780 + (i * 29) % 60, 4, "#FFC93C", None, a=0.7)
    g.poly([(860, 820), (1060, 820), (1700, 1100), (220, 1100)], "#1A1F2A", None)
    for i in range(14):
        u = i / 13
        for sd in (-1, 1):
            xx = 960 + sd * (100 + 640 * u ** 1.4); yy = 820 + 280 * u ** 1.4
            g.glow(xx, yy, 10 + 30 * u, "#FFE29A", 0.8)
            g.circle(xx, yy, 2 + 6 * u, "#FFF4C0", None)
    plane_side(g, 700 + 500 * prog, 380 + 200 * prog, 0.5, t, lights=lights)


def dark_door(g, t, x_walk=0.0):
    """Split scene: a bright room on the left, a dark room through a doorway on the right."""
    g.fill_all("#FFF4E0")
    with g.layer(0.9):
        g.rect(-300, -200, 1360, 1500, g.lgrad(0, 0, 0, 1080, "#FFF4E0", "#F2D9A8"), None)
        g.glow(400, 120, 600, "#FFFFFF", 0.6)
        g.rect(1060, -200, 1300, 1500, "#050810", None)
        g.rect(1000, 120, 120, 820, "#C9A27A", INK, lw=8)
        g.rect(-300, 900, 1360, 400, "#D9B584", INK, lw=6)
        g.rect(1060, 900, 1300, 400, "#07090F", None)


def eye_big(g, x, y, r, pupil=0.3, k=1.0, iris="#3E7A6A"):
    with g.at(x, y, 0, back_out(clamp(k), 1.4)):
        g.path(f"M{-r * 1.6} 0 Q0 {-r * 1.25} {r * 1.6} 0 Q0 {r * 1.25} {-r * 1.6} 0 Z", "#FFFFFF", INK, lw=r * 0.07)
        g.circle(0, 0, r * 0.62, iris, INK, lw=r * 0.04)
        g.circle(0, 0, r * 0.62 * clamp(pupil, 0.12, 0.9), "#0B0B10", None)
        g.circle(-r * 0.2, -r * 0.22, r * 0.1, "#FFFFFF", None)


ICONS = ["door", "phone", "seat", "window", "fork", "mask", "bulb"]


def icon(g, kind, x, y, s=1.0, col="#FFF4E0", lw=6):
    with g.at(x, y, 0, s):
        if kind == "door":
            g.rc(0, 0, 44, 64, None, col, lw=lw, r=8); g.circle(10, 4, 4, col, None)
        elif kind == "phone":
            g.rc(0, 0, 36, 62, None, col, lw=lw, r=8); g.line([(-6, 22), (6, 22)], col, lw)
        elif kind == "seat":
            g.path("M-14 -30 L-14 18 L22 18 L22 30 M-14 18 L-24 -26", None, col, lw=lw)
        elif kind == "window":
            g.rc(0, 0, 40, 60, None, col, lw=lw, r=18); g.circle(0, 20, 4, col, None)
        elif kind == "fork":
            g.line([(0, -30), (0, 30)], col, lw); g.line([(-12, -30), (-12, -10), (12, -10), (12, -30)], col, lw)
        elif kind == "mask":
            g.line([(0, -32), (0, -8)], col, lw); g.ellipse(0, 8, 22, 16, None, col, lw=lw)
        elif kind == "bulb":
            g.circle(0, -6, 20, None, col, lw=lw); g.line([(-8, 22), (8, 22)], col, lw)


def flight_strip(g, stage, t, k=1.0, x=W / 2, y=56):
    """Journey progress (screen space): 7 icons on a dotted route, a little plane moves to `stage` (0..6, fractional ok)."""
    if k <= 0:
        return
    with g.screen():
        with g.group(clamp(k)):
            w = 760
            g.rc(x, y, w + 90, 84, "#10263B", None, r=42, a=0.82)
            g.line([(x - w / 2, y), (x + w / 2, y)], "#FFF4E0", 4, a=0.35, dash=([8, 12],))
            for i, kind in enumerate(ICONS):
                ix = x - w / 2 + i * w / 6
                done = stage >= i - 0.01
                g.circle(ix, y, 26, "#FFC93C" if done else "#24476B", PAL["cream"], lw=3)
                icon(g, kind, ix, y, 0.48, INK if done else PAL["cream"], 5)
            px = x - w / 2 + clamp(stage, 0, 6) * w / 6
            with g.at(px, y - 44, 0, 0.8):
                g.path("M-30 0 L24 -6 Q36 0 24 6 Z", "#FF6B5B", INK, lw=4)
                g.path("M-4 -3 L-16 -22 L-6 -22 L8 -3 Z", "#FF6B5B", INK, lw=3)
                g.path("M-4 3 L-16 22 L-6 22 L8 3 Z", "#FF6B5B", INK, lw=3)


def number_card(g, t, n, kind, txt, k=1.0):
    """Big 'strange thing #n' card (screen space): ticket shape, number, icon, 1–2 words."""
    with g.screen():
        kk = back_out(clamp(k), 1.5)
        with g.at(W / 2, H / 2 - 20, -0.03, kk):
            g.rc(0, 0, 900, 420, "#FFF4E0", INK, lw=10, r=36)
            g.line([(-170, -190), (-170, 190)], INK, 5, dash=([16, 14],))
            g.circle(-450, 0, 40, "#10263B", None); g.circle(450, 0, 40, "#10263B", None)
            g.text(f"#{n}", -300, 10, 190, PAL["coral"], sw=26, depth=10)
            icon(g, kind, 120, -60, 2.4, PAL["navy"], 9)
            g.text(txt, 140, 120, 72, PAL["yellow"], sw=14, depth=5)
