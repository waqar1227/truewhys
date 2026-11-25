"""Car + winter-morning assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-028 hot water / frozen windshield).

    from flat_car import driveway_dawn, car_front, ws_pts, ws_path, ice_layer, crack_paths, draw_cracks, kettle, scraper, spray_bottle,
                         earmuffs, glass_slab, dashboard
All coordinates are design units (1080x1920) under the shot camera. Every drawing is code-made (no downloaded art).
car_front(g, x, y, s): a generic small hatchback seen from the front (no brand, no plate text), wheels on the ground at (x, y).
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd
from flat_fx import snow, sparkle, steam

SNOW, SNOW_SH = "#F4FBFF", "#C9E2F2"
ICE, ICE_D = "#DDF1FF", "#A9D4EE"
CAR = "#F2B33D"                      # mustard-yellow car (reads well on the blue dawn)


# ------------------------------------------------------------------ set: suburban driveway before sunrise
def driveway_dawn(g, t, fy=1560, snowing=False, lit=1.0):
    """Deep-blue to peach dawn sky, house row with warm windows, street lamp, snowy lawn, driveway with tyre tracks."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#1C2A55", "#3E4C8A", "#B07AA8", "#F7B58A"))
    with g.layer(0.15):
        R = rnd(21).random
        for i in range(40):
            x, y = R() * (W + 600) - 300, R() * 700 - 100
            g.circle(x, y, 2 + 3 * R(), "#FFFFFF", None, a=(0.25 + 0.5 * R()) * (0.6 + 0.4 * math.sin(t * 2 + i)))
        g.circle(840, 260, 46, "#FFF4E0", None, a=0.75)                              # fading moon
        g.circle(862, 246, 40, "#3E4C8A", None, a=0.75)
    with g.layer(0.4):                                                              # far roofs
        g.path(f"M-600 {fy-380} L-300 {fy-520} L0 {fy-400} L260 {fy-560} L560 {fy-420} L820 {fy-540} L1100 {fy-410} L1400 {fy-530} "
               f"L1700 {fy-400} L1700 {fy} L-600 {fy} Z", "#2A3466", None)
        R = rnd(5).random
        for i in range(14):
            x = -500 + i * 160 + R() * 40
            g.rect(x, fy - 360 + R() * 80, 34, 44, "#FFC96B", None, a=0.55 * lit)
    with g.layer(0.7):                                                              # the house behind the driveway
        hx0, hx1, top = -260, 1360, fy - 620
        g.rect(hx0, top, hx1 - hx0, 620, "#5B6FA8", INK, lw=8)
        for yy in range(int(top) + 50, int(fy), 50):
            g.line([(hx0, yy), (hx1, yy)], "#51649A", 4)
        g.poly([(hx0 - 60, top + 6), (550, top - 300), (hx1 + 60, top + 6)], "#33406E", INK, lw=8)
        g.poly([(hx0 - 40, top - 14), (550, top - 300), (hx1 + 40, top - 14), (hx1 + 60, top + 6), (550, top - 270), (hx0 - 60, top + 6)],
               SNOW, INK, lw=6)
        for x in (60, 1040):                                                        # lit windows
            g.rect(x - 120, top + 120, 240, 210, "#FFD27A", INK, lw=8, r=8)
            g.glow(x, top + 225, 220, "#FFC96B", 0.25 * lit)
            g.line([(x, top + 120), (x, top + 330)], INK, 6); g.line([(x - 120, top + 225), (x + 120, top + 225)], INK, 6)
            g.rect(x - 140, top + 330, 280, 26, SNOW, INK, lw=6, r=10)
        g.rect(430, fy - 330, 240, 330, "#C8664E", INK, lw=8, r=6)                    # garage door
        for yy in range(int(fy - 300), int(fy), 60):
            g.line([(436, yy), (664, yy)], "#A9523F", 5)
    with g.layer(0.85):                                                             # street lamp
        lx = 1010
        g.rect(lx - 10, fy - 820, 20, 820, "#2A2F44", INK, lw=5)
        g.path(f"M{lx} {fy-820} Q{lx} {fy-880} {lx-70} {fy-880}", None, "#2A2F44", lw=16)
        g.rc(lx - 90, fy - 866, 70, 30, "#FFE7A8", INK, lw=5, r=8)
        g.glow(lx - 90, fy - 840, 260, "#FFE7A8", 0.35 * lit)
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 500, "#E9F3FF", "#C9D9EE"), None)
    g.poly([(180, fy), (900, fy), (1300, H + 200), (-220, H + 200)], g.lgrad(0, fy, 0, H, "#B9C4D8", "#8F9CB6"), None)   # driveway
    for x0 in (330, 760):
        g.poly([(x0, fy), (x0 + 50, fy), (x0 + 50 + (x0 - 540) * 1.2, H + 200), (x0 + (x0 - 540) * 1.2 - 60, H + 200)], "#A5B1C8", None, a=0.7)
    g.line([(-600, fy), (W + 600, fy)], INK, 7)
    for x, w_ in ((-80, 300), (930, 360)):
        g.ellipse(x + w_ / 2, fy + 30, w_ / 2, 46, SNOW, None)
    if snowing:
        with g.layer(1.15):
            snow(g, t, (-200, -100, W + 200, H + 100), n=26, seed=7, col="#FFFFFF", size=(5, 12), speed=60, a=0.8)


# ------------------------------------------------------------------ the car (front view)
WS = [(-300, -425), (300, -425), (228, -668), (-228, -668)]      # windshield corners (car units, wheels at y=0)


def ws_pts(x, y, s):
    return [(x + px * s, y + py * s) for px, py in WS]


def ws_path(x, y, s):
    p = ws_pts(x, y, s)
    return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in p) + " Z"


def ws_at(x, y, s, u, v):
    """Point inside the windshield: u 0..1 left->right, v 0..1 bottom->top."""
    bl, br, tr, tl = ws_pts(x, y, s)
    bx, by = lerp(bl[0], br[0], u), bl[1]
    tx, ty = lerp(tl[0], tr[0], u), tl[1]
    return (lerp(bx, tx, v), lerp(by, ty, v))


def car_front(g, x, y, s=1.0, body=CAR, lights=1.0, ice=1.0, slide=0.0, melt=None, cracks=None, chip=None, roof_snow=True, wipers=True):
    """Generic hatchback, front view. ice 0..1 frost on the windshield; slide 0..1 slides the ice sheet down;
    melt = (u, v, r) clear patch; cracks = list of crack drawings (from crack_paths) with progress; chip = (u, v) small chip star."""
    with g.at(x, y, 0, s):
        g.ellipse(0, 6, 450, 40, "#000000", None, a=0.25)
        for sx in (-1, 1):                                                          # tyres
            g.rect(sx * 300 - 62, -130, 124, 136, "#22232E", INK, lw=8, r=26)
        g.path("M-410 -100 L-410 -300 Q-410 -340 -370 -345 L370 -345 Q410 -340 410 -300 L410 -100 Q410 -84 390 -84 L-390 -84 Q-410 -84 -410 -100 Z",
               body, INK, lw=9)
        g.rect(-400, -170, 800, 80, shade(body, -0.25), INK, lw=8, r=24)          # bumper
        g.rect(-150, -250, 300, 66, "#2A2F44", INK, lw=7, r=18)                     # grille
        for i in range(3):
            g.line([(-130, -232 + i * 16), (130, -232 + i * 16)], "#4A5170", 5)
        g.rect(-90, -150, 180, 44, "#F4F1EA", INK, lw=6, r=8)                        # blank plate
        for sx in (-1, 1):
            g.ellipse(sx * 285, -262, 78, 40, mix("#FFF4C8", "#FFFFFF", 0.4), INK, lw=8)
            if lights > 0:
                g.glow(sx * 285, -262, 170, "#FFF4C8", 0.4 * lights)
            g.ellipse(sx * 300, -270, 28, 14, "#FFFFFF", None, a=0.8)
        g.poly([(-405, -340), (405, -340), (335, -415), (-335, -415)], shade(body, 0.08), INK, lw=8, r=10)   # hood
        g.line([(-120, -350), (-90, -405)], shade(body, -0.12), 5); g.line([(120, -350), (90, -405)], shade(body, -0.12), 5)
        g.poly([(-338, -412), (338, -412), (262, -690), (-262, -690)], body, INK, lw=9, r=16)            # cabin
        for sx in (-1, 1):                                                          # mirrors
            g.path(f"M{sx*332} -440 L{sx*400} -450 Q{sx*420} -452 {sx*418} -470 L{sx*412} -500 Q{sx*408} -512 {sx*392} -510 L{sx*318} -490 Z",
                   body, INK, lw=7)
        d = "M" + " L".join(f"{a} {b}" for a, b in WS) + " Z"
        g.path(d, g.lgrad(0, -668, 0, -425, "#1F2D52", "#3C5B8C", "#26375E"), INK, lw=8)
        with g.clip(d=d):
            g.poly([(-200, -425), (-120, -425), (40, -668), (-40, -668)], "#FFFFFF", None, a=0.08)   # reflection streaks
            g.poly([(10, -425), (40, -425), (200, -668), (170, -668)], "#FFFFFF", None, a=0.06)
            g.rect(-200, -560, 50, 40, "#3A3F55", None, a=0.6)                        # rear-view mirror inside
            if ice > 0:
                ice_layer(g, ice, slide)
            if melt is not None:
                mu, mv, mr = melt
                px, py = _ws_local(mu, mv)
                g.ellipse(px, py, mr * 1.25, mr, g.lgrad(0, py - mr, 0, py + mr, "#2F4A78", "#4A6FA6"), None)
                g.ellipse(px, py, mr * 1.25, mr, None, "#FFFFFF", lw=5, a=0.6)
            if chip is not None:
                cx, cy = _ws_local(*chip)
                for i in range(6):
                    a = i * math.pi / 3 + 0.3
                    g.line([(cx, cy), (cx + 22 * math.cos(a), cy + 22 * math.sin(a))], "#FFFFFF", 4)
                g.circle(cx, cy, 10, "#E8F6FF", INK, lw=3)
            for c in (cracks or []):
                draw_cracks(g, c[0], c[1])
        g.path(d, None, INK, lw=8)
        if wipers:
            g.line([(-250, -432), (-40, -470)], INK, 9); g.line([(40, -432), (250, -470)], INK, 9)
        if roof_snow:
            g.path("M-262 -688 Q-270 -730 -200 -736 Q-60 -760 0 -742 Q90 -764 210 -738 Q272 -730 262 -688 Z", SNOW, INK, lw=7)
            g.path("M-330 -414 Q-200 -440 -60 -420 Q60 -440 200 -422 Q300 -432 334 -414 L320 -405 L-320 -405 Z", SNOW, INK, lw=6)   # snow on the hood


def _ws_local(u, v):
    bl, br, tr, tl = WS
    return (lerp(lerp(bl[0], br[0], u), lerp(tl[0], tr[0], u), v), lerp(bl[1], tl[1], v))


def ice_layer(g, k=1.0, slide=0.0):
    """Frosted ice sheet over the windshield (car units, call inside the windshield clip). slide moves it down off the glass."""
    dy = slide * 320
    with g.at(0, dy):
        g.poly([(-320, -410), (320, -410), (240, -690), (-240, -690)], ICE, None, a=0.92 * k)
        R = rnd(31).random
        for i in range(16):                                                         # frost ferns
            x0, y0 = -280 + R() * 560, -430 - R() * 230
            a = -math.pi / 2 + (R() - 0.5) * 2.2
            L = 50 + R() * 70
            x1, y1 = x0 + L * math.cos(a), y0 + L * math.sin(a)
            g.line([(x0, y0), (x1, y1)], "#FFFFFF", 4, a=0.9 * k)
            for j in range(1, 4):
                bx, by = lerp(x0, x1, j / 4), lerp(y0, y1, j / 4)
                for da in (0.7, -0.7):
                    g.line([(bx, by), (bx + 18 * math.cos(a + da), by + 18 * math.sin(a + da))], "#FFFFFF", 3, a=0.8 * k)
        for i in range(22):
            g.circle(-290 + R() * 580, -430 - R() * 240, 3 + 4 * R(), ICE_D, None, a=0.6 * k)
        if slide > 0:
            g.line([(-320, -410), (320, -410)], "#FFFFFF", 8, a=0.9)


# ------------------------------------------------------------------ cracks
def crack_paths(x0, y0, seed=1, n=6, L=320, branch=2):
    """Pre-computed branching crack from (x0, y0): list of (polyline, start_dist, length). Coordinates in caller units."""
    R = rnd(seed).random
    out = []

    def grow(px, py, ang, length, d0, depth):
        pts, d = [(px, py)], d0
        steps = max(3, int(length / 38))
        for i in range(steps):
            ang += (R() - 0.5) * 0.7
            step = length / steps
            px, py = px + step * math.cos(ang), py + step * math.sin(ang)
            pts.append((px, py)); d += step
            if depth < branch and R() < 0.22:
                grow(px, py, ang + (0.6 if R() < 0.5 else -0.6), length * 0.45, d, depth + 1)
        out.append((pts, d0, d - d0))

    for i in range(n):
        grow(x0, y0, i * 2 * math.pi / n + R() * 0.6, L * (0.6 + 0.6 * R()), 0.0, 0)
    return out


def draw_cracks(g, paths, k, speed=1.0, w=8):
    """Reveal the crack network up to distance k * (longest branch end)."""
    if k <= 0:
        return
    total = max(d0 + l for _, d0, l in paths)
    reach = k * total
    for pts, d0, l in paths:
        if reach <= d0:
            continue
        u = clamp((reach - d0) / max(l, 1e-6))
        n = max(2, int(round(1 + u * (len(pts) - 1))))
        sub = pts[:n]
        if u < 1 and n < len(pts):
            fx = (u * (len(pts) - 1)) % 1
            a, b = pts[n - 1], pts[n] if n < len(pts) else pts[n - 1]
            sub = sub + [(lerp(a[0], b[0], fx), lerp(a[1], b[1], fx))]
        g.line(sub, INK, w + 4, a=0.8)
        g.line(sub, "#FFFFFF", w)


# ------------------------------------------------------------------ props
def kettle(g, x, y, tilt=0.0, s=1.0, t=0.0, hot=True, col="#E04B5A"):
    """Electric-style kettle held by its handle at (x, y); tilt > 0 tips the spout (screen right) down."""
    with g.at(x, y, tilt, s):
        g.path("M-10 -40 Q-60 -40 -60 10 Q-60 60 -10 70", None, INK, lw=22)          # handle
        g.path("M-10 -40 Q-60 -40 -60 10 Q-60 60 -10 70", None, shade(col, -0.2), lw=12)
        g.path("M0 -60 Q10 -80 70 -80 Q130 -80 140 -60 L160 80 Q160 100 140 100 L20 100 Q0 100 0 80 Z", col, INK, lw=8)
        g.path("M150 0 L230 -50 L238 -38 L162 30 Z", col, INK, lw=7)                  # spout
        g.rect(40, -96, 60, 20, shade(col, -0.25), INK, lw=6, r=8)
        g.line([(30, -40), (40, 70)], "#FFFFFF", 8, a=0.35)
    if hot:
        steam(g, t, x + 90 * s, y - 120 * s, n=3, h=130 * s, col="#FFFFFF", a=0.6, w=9 * s, spread=30 * s)


def spout_pt(x, y, tilt=0.0, s=1.0):
    c, sn = math.cos(tilt), math.sin(tilt)
    px, py = 236, -44
    return (x + s * (px * c - py * sn), y + s * (px * sn + py * c))


def scraper(g, x, y, rot=0.0, s=1.0, col="#3EB4E6"):
    """Ice scraper: blade at (x, y) facing screen-left, handle going right."""
    with g.at(x, y, rot, s):
        g.rect(-8, -70, 24, 140, "#E8F6FF", INK, lw=6, r=4)
        g.path("M16 -60 L80 -40 L80 40 L16 60 Z", col, INK, lw=7)
        g.rect(78, -18, 170, 36, shade(col, -0.2), INK, lw=7, r=16)


def spray_bottle(g, x, y, rot=0.0, s=1.0, t=0.0, spraying=0.0, col="#5ED3B5", label="DE-ICER"):
    """Spray bottle; nozzle points screen-left. spraying 0..1 draws a mist cone."""
    with g.at(x, y, rot, s):
        g.rect(-60, -40, 120, 210, col, INK, lw=8, r=24)
        g.rect(-30, -90, 60, 56, "#F4F1EA", INK, lw=7, r=8)
        g.path("M-30 -90 L-110 -96 L-110 -70 L-30 -64 Z", "#F4F1EA", INK, lw=6)
        g.path("M20 -64 Q60 -40 40 0", None, INK, lw=10)
        g.rect(-50, 30, 100, 70, "#FFFFFF", INK, lw=5, r=8)
        g.text(label, 0, 66, 26, INK, stroke=None, sw=0)
        if spraying > 0:
            R = rnd(int(t * 20)).random
            for i in range(26):
                u = R(); a = math.pi + (R() - 0.5) * 0.6
                d = 30 + u * 300 * spraying
                g.circle(-110 + d * math.cos(a), -83 + d * math.sin(a), 4 + 6 * u, "#E8FBFF", None, a=0.8 * (1 - u))


def earmuffs(g, x, y, h, col="#FF6B5B", band="#2A2F44", view="3q", flip=False):
    """Earmuffs over a char2 head (band over the crown, a fluffy muff on the visible ear)."""
    import cast2
    from flat_winter import head_pt
    k = h / 565.0 * cast2.HEAD_K
    top = head_pt(x, y, h, 0, -560, view, flip)
    ear = head_pt(x, y, h, -78 if view == "3q" else -86, -505, view, flip)
    g.path(f"M{ear[0]:.1f} {ear[1]:.1f} Q{lerp(ear[0], top[0], 0.4) - 40*k*(-1 if flip else 1):.1f} {top[1]:.1f} {top[0] + 30*k*(-1 if flip else 1):.1f} {top[1] + 4*k:.1f}",
           None, INK, lw=18 * k)
    g.path(f"M{ear[0]:.1f} {ear[1]:.1f} Q{lerp(ear[0], top[0], 0.4) - 40*k*(-1 if flip else 1):.1f} {top[1]:.1f} {top[0] + 30*k*(-1 if flip else 1):.1f} {top[1] + 4*k:.1f}",
           None, band, lw=10 * k)
    g.circle(ear[0], ear[1], 34 * k, col, INK, lw=6 * k)
    g.circle(ear[0] - 8 * k, ear[1] - 8 * k, 12 * k, mix(col, "#FFFFFF", 0.45), None)


# ------------------------------------------------------------------ explainer pieces
def glass_slab(g, x0, x1, y0, y1, hot=0.0, depth=0.25, swell=0.0, bend=0.0, frost=1.0, t=0.0):
    """Cross-section of windshield glass: outer surface on top. hot 0..1 heats a top band of `depth` of the thickness;
    swell widens that band sideways; bend bows the slab (outer side longer)."""
    def edge(y, sw):
        return [(x0 - sw + (x1 - x0 + 2 * sw) * i / 24, y - bend * 60 * math.sin(math.pi * i / 24)) for i in range(25)]
    yh = lerp(y0, y1, depth)
    top, mid, bot = edge(y0, swell * 40), edge(yh, swell * 22), edge(y1, 0)
    g.poly(mid + bot[::-1], g.lgrad(0, yh, 0, y1, "#9FD8F5", "#6FB7E0"), INK, lw=8)
    g.poly(top + mid[::-1], mix("#9FD8F5", "#FF8A3D", hot), INK, lw=8)
    if hot > 0:
        g.glow((x0 + x1) / 2, y0, (x1 - x0) * 0.5, "#FF8A3D", 0.35 * hot)
    if frost > 0:
        R = rnd(9).random
        for i in range(18):
            px = lerp(x0 + 30, x1 - 30, R()); py = lerp(yh + 30, y1 - 20, R())
            sparkle(g, px, py - bend * 60 * math.sin(math.pi * (px - x0) / (x1 - x0)), 10 + 8 * R(), "#FFFFFF", a=0.8 * frost)
    for xx in (x0 + 80, x1 - 200):
        g.line([(xx, y0 + 20), (xx + 120, y0 + 20)], "#FFFFFF", 6, a=0.4)


def dashboard(g, t, warm=0.0):
    """Inside the car looking out: dashboard, vents, steering wheel rim; warm 0..1 = defroster heat waves rising."""
    g.path(f"M-100 1380 Q540 1250 1180 1380 L1180 {H+100} L-100 {H+100} Z", "#2A2F44", INK, lw=10)
    g.path("M-100 1380 Q540 1250 1180 1380 L1180 1440 Q540 1320 -100 1440 Z", "#3A4058", INK, lw=8)
    for x in (300, 540, 780):
        g.rect(x - 90, 1352 - (40 if x == 540 else 20), 180, 34, "#15182A", INK, lw=6, r=12)
        for j in range(4):
            g.line([(x - 70 + j * 46, 1345 - (40 if x == 540 else 20)), (x - 70 + j * 46, 1365 - (40 if x == 540 else 20))], "#4A5170", 4)
    if warm > 0:
        for i in range(9):
            x = 220 + i * 80
            u = (t * 0.5 + i * 0.13) % 1
            y = 1320 - u * 420
            g.path(f"M{x} {y} q -18 -30 0 -60 q 18 -30 0 -60", None, "#FFB36B", lw=8, a=warm * (1 - u) * 0.9)
    g.circle(540, 1980, 420, None, "#1A1D2C", lw=60)
    g.circle(540, 1980, 420, None, INK, lw=6)
