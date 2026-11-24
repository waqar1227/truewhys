"""Winter + Arctic assets for Style F (flat 2D), TrueWhys originals (added 24 Nov 2026 for A-026 tongue/pole and A-027 reindeer eyes).

    from flat_winter import winter_yard, metal_pole, tongue, tundra_night, tundra_summer, aurora, stars, reindeer, reindeer_face, torch_beam
All coordinates are design units (1080x1920) under the shot camera. Every drawing is code-made (no downloaded art).
"""
import math
from flat2d import G, W, H, INK, PAL, TAU, mix, shade, clamp, lerp, rnd, wig, ease_io
from flat_fx import snow, sparkle

SNOW, SNOW_SH = "#F4FBFF", "#C9E2F2"
FUR, FUR_D, FUR_L, RUFF, ANTLER = "#8A6446", "#6B4A33", "#B89678", "#EDE3D2", "#D8C7A4"


# ------------------------------------------------------------------ daytime snowy yard (A-026)
def winter_yard(g, t, fy=1500, snowing=True, fence=True, building=True):
    """Pale winter sky, distant hills, brick school wall, wooden fence, snow ground with blue shadows, falling snow."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#9FD3EE", "#D6EEFA", "#EEF8FF"))
    with g.layer(0.25):
        g.glow(860, 300, 360, "#FFF6D8", 0.55)                                      # low winter sun haze
        g.circle(860, 300, 70, "#FFF6D8", None, a=0.9)
    with g.layer(0.45):
        g.path(f"M-600 {fy-260} Q-200 {fy-520} 200 {fy-330} Q520 {fy-560} 900 {fy-360} Q1300 {fy-500} 1700 {fy-300} L1700 {fy} L-600 {fy} Z",
               "#DDEFF8", None)
        for i, (x, h) in enumerate(((-120, 260), (60, 330), (980, 300), (1160, 240))):   # bare trees
            g.line([(x, fy - 250), (x, fy - 250 - h)], "#7F8FA0", 16, a=0.8)
            for k in range(4):
                yy = fy - 280 - h * (0.25 + 0.18 * k); d = (-1) ** (k + i)
                g.line([(x, yy), (x + d * (90 - 14 * k), yy - 70)], "#7F8FA0", 9, a=0.8)
    if building:
        with g.layer(0.7):
            g.rect(-400, fy - 560, 2000, 560, "#C8664E", INK, lw=8)                     # brick wall of the school
            for yy in range(int(fy - 520), int(fy), 56):
                g.line([(-400, yy), (1600, yy)], "#A9523F", 4, a=0.6)
            for x in (-180, 260, 700, 1140):
                g.rect(x - 110, fy - 470, 220, 190, "#BFE3F5", INK, lw=8, r=8)
                g.line([(x, fy - 470), (x, fy - 280)], INK, 6); g.line([(x - 110, fy - 375), (x + 110, fy - 375)], INK, 6)
                g.rect(x - 130, fy - 485, 260, 26, SNOW, INK, lw=6, r=10)          # snow on the sills
            g.rect(-400, fy - 590, 2000, 50, SNOW, INK, lw=7, r=20)
    if fence:
        with g.layer(0.85):
            g.rect(-400, fy - 210, 2000, 26, "#A87A4E", INK, lw=6)
            g.rect(-400, fy - 120, 2000, 26, "#A87A4E", INK, lw=6)
            for x in range(-380, 1600, 120):
                g.path(f"M{x-24} {fy} L{x-24} {fy-260} L{x} {fy-290} L{x+24} {fy-260} L{x+24} {fy} Z", "#C8955E", INK, lw=6)
                g.ellipse(x, fy - 284, 30, 12, SNOW, None)
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 600, SNOW, "#E3F1FA"), None)
    g.line([(-600, fy), (W + 600, fy)], INK, 7)
    for x, w_ in ((-60, 420), (760, 520)):                                          # soft snow drifts
        g.ellipse(x + w_ / 2, fy + 40, w_ / 2, 60, SNOW, None)
        g.path(f"M{x} {fy+60} Q{x+w_/2} {fy-40} {x+w_} {fy+60}", None, SNOW_SH, lw=6, a=0.8)
    for i in range(14):                                                             # footprints
        r = rnd(i * 13 + 5).random
        g.ellipse(120 + i * 70 + r() * 20, fy + 200 + (i % 2) * 40 + i * 18, 18, 9, SNOW_SH, None, a=0.7)
    if snowing:
        with g.layer(1.15):
            snow(g, t, (-200, -100, W + 200, H + 100), n=34, seed=11, col="#FFFFFF", size=(6, 14), speed=90, a=0.85)


def metal_pole(g, x, y_top, y_bot, w=74, frost=0.6, cap=True):
    """Steel pole (lamp/flag post): horizontal metal gradient, highlight, base plate, frost speckles."""
    grad = g.lgrad(x - w / 2, 0, x + w / 2, 0, "#5E6B78", "#D7E2EC", "#F4F9FC", "#9AA8B6", "#5E6B78")
    g.rect(x - w / 2, y_top, w, y_bot - y_top, grad, INK, lw=8, r=6)
    g.line([(x - w * 0.12, y_top + 20), (x - w * 0.12, y_bot - 20)], "#FFFFFF", w * 0.12, a=0.7)
    if cap:
        g.rc(x, y_top, w * 1.5, 36, "#7F8D9A", INK, lw=8, r=12)
        g.ellipse(x, y_top - 22, w * 0.7, 20, SNOW, INK, lw=6)
    g.rc(x, y_bot - 14, w * 2.2, 30, "#7F8D9A", INK, lw=8, r=10)
    if frost > 0:
        R = rnd(int(x) + 7).random
        for i in range(int(46 * frost)):
            yy = lerp(y_top + 30, y_bot - 40, R()); xx = x + (R() - 0.5) * w * 0.8
            g.circle(xx, yy, 3 + R() * 4, "#FFFFFF", None, a=0.75)


def tongue(g, x0, y0, x1, y1, w=34, col="#E8677A", stretch=0.0, frozen=0.0):
    """Tongue from the mouth (x0, y0) to a contact point (x1, y1); `stretch` thins it, `frozen` adds a white ice rim at the tip."""
    ww = w * (1 - 0.35 * stretch)
    g.limb([(x0, y0), ((x0 + x1) / 2, (y0 + y1) / 2 + 4), (x1, y1)], col, ww, lw=6)
    g.line([(x0 + (x1 - x0) * 0.15, y0 + 2), (x1 - (x1 - x0) * 0.2, y1 + 2)], shade(col, -0.18), 4, a=0.8)   # centre groove
    g.ellipse(x1, y1, ww * 0.35, ww * 0.62, col, INK, lw=5)
    if frozen > 0:
        g.ellipse(x1, y1, ww * 0.45, ww * 0.8, None, "#E9F8FF", lw=7, a=frozen)
        for i in range(3):
            sparkle(g, x1 + (i - 1) * 16, y1 - ww * 0.9 + i * ww * 0.7, 14, "#FFFFFF", a=frozen)


# ------------------------------------------------------------------ Arctic night / summer (A-027)
def stars(g, n=70, seed=4, box=(-300, -200, W + 300, 1100), t=0.0):
    R = rnd(seed).random
    for i in range(n):
        x, y = lerp(box[0], box[2], R()), lerp(box[1], box[3], R())
        tw = 0.55 + 0.45 * math.sin(t * (1.2 + R() * 2) + i)
        g.circle(x, y, 2 + R() * 3.5, "#EAF6FF", None, a=0.4 + 0.5 * tw)


def aurora(g, t, y0=420, amp=120, a=0.35, cols=("#5EF0B0", "#3FD3C8", "#8AF5A0")):
    """Three slow translucent ribbons (curtains) of polar light."""
    for k, col in enumerate(cols):
        top, bot = [], []
        for i in range(0, 33):
            x = -400 + i * 60
            yy = y0 + k * 90 + amp * math.sin(i * 0.33 + t * 0.35 + k * 1.7) + 40 * math.sin(i * 0.9 - t * 0.6 + k)
            top.append((x, yy - 160 - 60 * math.sin(i * 0.5 + t * 0.4 + k)))
            bot.append((x, yy + 40))
        g.poly(top + bot[::-1], g.lgrad(0, y0 - 300, 0, y0 + 260, (0, mix(col, col, 0)[:3] + (0,)), (0.6, col), (1, col)), None, a=a)
        g.line(bot, col, 10, a=a * 1.4)


def tundra_night(g, t, fy=1400, show_aurora=True, spruce=True):
    g.fill_all(g.lgrad(0, 0, 0, H, "#050C1A", "#0B1F36", "#163A58"))
    with g.layer(0.15):
        stars(g, t=t)
    if show_aurora:
        with g.layer(0.25):
            aurora(g, t)
    with g.layer(0.4):
        g.path(f"M-600 {fy-150} L-200 {fy-470} L60 {fy-260} L380 {fy-560} L700 {fy-280} L1000 {fy-500} L1700 {fy-180} L1700 {fy} L-600 {fy} Z",
               "#122B44", None)
        g.path(f"M-260 {fy-420} L-200 {fy-470} L-140 {fy-420} L-170 {fy-430} Z M320 {fy-510} L380 {fy-560} L440 {fy-505} L400 {fy-515} Z "
               f"M940 {fy-450} L1000 {fy-500} L1060 {fy-450} L1020 {fy-460} Z", "#9FC2DC", None, a=0.8)
    if spruce:
        with g.layer(0.65):
            for x, h in ((-150, 340), (-20, 260), (90, 300), (930, 320), (1050, 260), (1190, 360)):
                for k in range(4):
                    yy = fy - 60 - k * h * 0.22; ww = (1 - k * 0.22) * h * 0.38
                    g.poly([(x - ww, yy), (x, yy - h * 0.34), (x + ww, yy)], "#0A1A2B", None)
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 600, "#3A5E80", "#22405E"), None)
    g.line([(-600, fy), (W + 600, fy)], "#0A1626", 6)
    for x, w_ in ((-100, 500), (700, 600)):
        g.path(f"M{x} {fy+80} Q{x+w_/2} {fy-10} {x+w_} {fy+80}", None, "#5A80A2", lw=6, a=0.8)


def tundra_summer(g, t, fy=1400):
    """Midnight-sun summer tundra: low golden sun on the horizon, green-brown ground, cotton grass."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#7EC4E8", "#F6D9A0", "#FFC38A"))
    with g.layer(0.3):
        g.glow(760, fy - 160, 420, "#FFE7A0", 0.7)
        g.circle(760, fy - 160, 95, "#FFE08A", INK, lw=6)
    with g.layer(0.45):
        g.path(f"M-600 {fy-120} L-200 {fy-330} L100 {fy-180} L420 {fy-380} L760 {fy-200} L1050 {fy-320} L1700 {fy-120} L1700 {fy} L-600 {fy} Z",
               "#6E8F6A", None)
    g.rect(-600, fy, W + 1200, 1400, g.lgrad(0, fy, 0, fy + 600, "#8CB060", "#5E7E3E"), None)
    g.line([(-600, fy), (W + 600, fy)], INK, 6)
    R = rnd(9).random
    for i in range(26):
        x, y = -100 + R() * 1300, fy + 40 + R() * 520
        g.line([(x, y), (x + 4, y - 40)], "#3E5E2E", 4)
        g.circle(x + 4, y - 46, 10, "#FFFFFF", None, a=0.9)


# ------------------------------------------------------------------ reindeer
def _antler(g, root, side, s, lw):
    """One antler: main beam sweeping back and up with 4 tines (side = +1 right antler / -1 mirrored)."""
    x, y = root
    beam = [(x, y), (x - 40 * s * side, y - 120 * s), (x - 130 * s * side, y - 230 * s), (x - 150 * s * side, y - 340 * s), (x - 110 * s * side, y - 430 * s)]
    g.limb(beam, ANTLER, 18 * s, lw=lw)
    for (i, dx, dy) in ((1, 60, -70), (2, 70, -90), (3, 80, -60), (4, 40, -70)):
        bx, by = beam[i]
        g.limb([(bx, by), (bx + dx * s * side * 0.6, by + dy * s * 0.5), (bx + dx * s * side, by + dy * s)], ANTLER, 12 * s, lw=lw)
    g.limb([(x - 10 * s * side, y - 40 * s), (x + 50 * s * side, y - 70 * s), (x + 70 * s * side, y - 40 * s)], ANTLER, 12 * s, lw=lw)   # brow tine


def reindeer(g, x, y, s=1.0, t=0.0, flip=False, eye="#3A2A22", glow=0.0, walk=0.0, head=0.0, seed=0):
    """Side-view reindeer facing right (flip=True faces left), hooves on (x, y). glow 0..1 lights the eye in `eye` colour.
    walk 0..1 = leg swing amount, head = head dip (-1 up .. 1 down, e.g. grazing)."""
    L = 7.0
    with g.at(x, y, 0, -s if flip else s, s):
        br = 1 + 0.01 * math.sin(t * 2.2 + seed)

        def leg(lx, ph, col, near):
            sw = 0.2 * walk * math.sin(t * 6 + seed + ph)
            with g.at(lx, -250, sw):
                g.limb([(0, 0), (8, 120), (2, 228)], col, 44 if near else 38, lw=L)
                if near:
                    g.rc(2, 212, 48, 16, RUFF, None, r=6)
                g.path("M-24 222 L28 222 L32 252 L-28 252 Z", "#2A1C1E", INK, lw=L)
        leg(-150, math.pi + 1.4, "#4A3020", False)
        leg(185, 1.4, "#4A3020", False)
        g.ellipse(-262, -350, 36, 24, RUFF, INK, lw=L, rot=-0.6)                  # tail
        g.path("M-270 -330 Q-280 -440 -120 -455 L140 -455 Q290 -440 280 -330 Q270 -225 130 -215 L-130 -215 Q-270 -225 -270 -330 Z",
               FUR, INK, lw=L)                                                     # barrel body
        g.ellipse(-215, -330, 58, 92, RUFF, None, a=0.95)                          # pale rump
        g.path("M-160 -240 Q0 -200 160 -240 Q120 -214 0 -212 Q-120 -214 -160 -240 Z", FUR_L, None, a=0.9)
        g.path("M-200 -440 Q0 -470 200 -440", None, shade(FUR, -0.18), lw=10, a=0.7)
        hy = 70 * head
        g.path(f"M150 -440 Q230 -520 {300} {-610+hy} L{380} {-560+hy} Q330 -430 270 -300 Z", FUR, INK, lw=L)    # neck
        g.path(f"M{360} {-545+hy} Q410 -420 350 -270 L335 -228 L318 -262 L300 -220 L284 -258 L262 -226 L250 -290 Q300 -420 {320} {-560+hy} Z",
               RUFF, INK, lw=L)                                                    # pale throat mane
        with g.at(330, -610 + hy, 0.45 * head):
            _antler(g, (-40, -70), 1, 0.8, L)
            with g.group(0.9):
                _antler(g, (-6, -82), 1, 0.92, L)
            g.path("M-40 -30 Q-20 -100 60 -80 Q170 -50 205 10 Q215 60 170 66 Q90 72 10 45 Q-50 25 -40 -30 Z", FUR, INK, lw=L)   # head
            g.path("M130 0 Q195 10 205 40 Q185 66 140 58 Z", FUR_L, None)
            g.ellipse(196, 30, 22, 18, "#2A1C1E", INK, lw=L * 0.8)                # nose
            g.path("M-10 -70 Q-80 -125 -95 -84 Q-72 -52 -14 -56 Z", FUR_D, INK, lw=L)   # ear
            ex, ey = 62, -34
            if glow > 0:
                g.glow(ex, ey, 140, eye, 0.75 * glow)
                g.glow(ex, ey, 54, "#FFFFFF", 0.6 * glow)
            g.ellipse(ex, ey, 18, 15, mix("#2A1C1E", eye, glow), INK, lw=L * 0.8)
            g.circle(ex + 5, ey - 5, 5, "#FFFFFF", None, a=0.9)
        leg(-200, 0.0, FUR_D, True)
        leg(140, math.pi, FUR_D, True)


def reindeer_face(g, x, y, s=1.0, t=0.0, eye="#4FA8FF", glow=1.0, blink=0.0, tilt=0.0):
    """Front view head + ruff (hook close-ups): two glowing eyes in torch light. (x, y) = centre of the eyes."""
    lw = 8
    with g.at(x, y, tilt, s):
        g.path("M-150 100 Q-170 400 -260 1500 L260 1500 Q170 400 150 100 Z", FUR, INK, lw=lw)                   # neck (runs off frame)
        zig = " ".join(f"L{-200 + i * 50} {640 + (60 if i % 2 else 0)}" for i in range(9))
        g.path(f"M-170 260 Q-240 420 -200 640 {zig} Q240 420 170 260 Q0 340 -170 260 Z", RUFF, INK, lw=lw)     # shaggy chest ruff
        for i in range(-3, 4):
            g.path(f"M{i*55-15} 380 Q{i*55} 480 {i*55+15} 400", None, shade(RUFF, -0.18), lw=5)
        for sd in (-1, 1):
            _antler(g, (sd * 70, -150), -sd, 1.1, lw)
            with g.at(sd * 165, -95, sd * 0.5):
                g.path("M0 -30 Q90 -60 130 0 Q90 40 0 25 Z" if sd > 0 else "M0 -30 Q-90 -60 -130 0 Q-90 40 0 25 Z", FUR_D, INK, lw=lw)
        g.path("M-150 -170 Q0 -230 150 -170 Q190 -40 130 120 Q100 300 0 330 Q-100 300 -130 120 Q-190 -40 -150 -170 Z", FUR, INK, lw=lw)
        g.path("M-60 -180 Q0 -200 60 -180 Q40 -40 0 -20 Q-40 -40 -60 -180 Z", FUR_D, None, a=0.6)               # darker forehead blaze
        g.path("M-95 150 Q0 120 95 150 Q110 290 0 330 Q-110 290 -95 150 Z", FUR_L, None)                         # muzzle
        g.ellipse(0, 250, 72, 46, "#2A1C1E", INK, lw=lw)                                                          # nose
        g.ellipse(-26, 258, 12, 16, "#120A0C", None); g.ellipse(26, 258, 12, 16, "#120A0C", None)
        g.ellipse(-14, 236, 18, 8, "#FFFFFF", None, a=0.35)
        for sd in (-1, 1):
            ex, ey = sd * 118, -20
            if glow > 0:
                fl = 1 + 0.05 * math.sin(t * 9 + sd)
                g.glow(ex, ey, 230 * fl, eye, 0.55 * glow)
                g.glow(ex, ey, 90, mix(eye, "#FFFFFF", 0.6), 0.8 * glow)
            g.ellipse(ex, ey, 34, 30 * (1 - blink), mix("#2A1C1E", eye, glow), INK, lw=6)
            if glow > 0:
                g.ellipse(ex, ey, 18, 16 * (1 - blink), mix(eye, "#FFFFFF", 0.75), None, a=glow)
            g.circle(ex + sd * 8 - 6, ey - 10, 7, "#FFFFFF", None, a=0.9 * (1 - blink))


def torch_beam(g, x0, y0, x1, y1, w1=420, a=0.28, col="#FFF4C8"):
    """A cone of torch light from (x0, y0) towards (x1, y1), w1 wide at the far end."""
    dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy) or 1
    nx, ny = -dy / L, dx / L
    pts = [(x0 + nx * 18, y0 + ny * 18), (x1 + nx * w1 / 2, y1 + ny * w1 / 2), (x1 - nx * w1 / 2, y1 - ny * w1 / 2), (x0 - nx * 18, y0 - ny * 18)]
    g.poly(pts, g.lgrad(x0, y0, x1, y1, (0, col), (1, mix(col, col, 0)[:3] + (0.15,))), None, a=a)
    g.glow(x1, y1, w1 * 0.7, col, a * 0.8)


# ------------------------------------------------------------------ cast v2.2 helpers (positions in design units)
def head_pt(x, y, h, ux, uy, view="front", flip=False):
    """Point on a char2 figure's head given in cast2 head units (before the head scale)."""
    import cast2
    k = h / 565.0
    dx = (ux + (12 if view == "3q" else 0)) * cast2.HEAD_K
    py = -404 + (uy + 404) * cast2.HEAD_K
    return (x + (-dx if flip else dx) * k, y + py * k)


def mouth_pt(x, y, h, view="front", flip=False):
    return head_pt(x, y, h, 0, -456, view, flip)


def hand_pt(cid, pose, x, y, h, side=1, flip=False):
    """Hand position of a char2 figure (side=1 screen-right arm, -1 left) for a named pose."""
    import cast2
    s = cast2.CAST[cid]
    k = h / 565.0
    sx = side * (74 if s.get("female") else 82)
    (ex, ey), (hx, hy), _ = cast2._arm_pts(side, pose)
    px, py = sx + hx, -384 + hy + 20
    return (x + (-px if flip else px) * k, y + py * k)


def beanie(g, x, y, h, col="#FF6B5B", band="#FFF4E0", view="front", flip=False):
    """Knitted winter hat drawn over a char2 head (sits above the brows), with a pom-pom."""
    import cast2
    k = h / 565.0 * cast2.HEAD_K
    cx, cy = head_pt(x, y, h, 0, -552, view, flip)
    with g.at(cx, cy, 0, k):
        g.path("M-76 6 Q-80 -96 0 -100 Q80 -96 76 6 Z", col, INK, lw=6)
        for i in range(-3, 4):
            g.line([(i * 19, 0), (i * 16, -88)], shade(col, -0.15), 4)
        g.rc(0, 4, 168, 32, band, INK, lw=6, r=14)
        g.circle(0, -108, 22, band, INK, lw=6)


def scarf(g, x, y, h, col="#FFC93C", stripe="#FF6B5B", flip=False, t=0.0):
    k = h / 565.0
    with g.at(x, y - 396 * k, 0, -k if flip else k, k):
        g.rc(0, 0, 150, 40, col, INK, lw=6, r=18)
        for xx in (-40, 0, 40):
            g.line([(xx, -16), (xx, 16)], stripe, 9)
        sw = 0.06 * math.sin(t * 3)
        with g.at(30, 10, sw):
            g.path("M-18 0 L18 0 L22 100 L-12 100 Z", col, INK, lw=6)
            g.line([(-14, 50), (20, 50)], stripe, 9); g.line([(-13, 80), (21, 80)], stripe, 9)


def torch(g, x, y, ang=0.0, on=1.0):
    """Hand torch (flashlight) held at (x, y), pointing along ang (radians, 0 = right)."""
    with g.at(x, y, ang):
        g.rc(10, 0, 90, 34, "#3A3A48", INK, lw=6, r=8)
        g.path("M52 -24 L84 -30 L84 30 L52 24 Z", "#5A5A6A", INK, lw=6)
        g.ellipse(84, 0, 8, 28, mix("#FFF4C8", "#FFFFFF", 0.5), INK, lw=4, a=0.5 + 0.5 * on)
