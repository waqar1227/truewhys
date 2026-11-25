"""Oxford Electric Bell assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-034 the bell ringing since 1840).

    from flat_bell import bell_case, ball_x, lab_room, college, ten_billion, pile_xray, BRASS, SULFUR
A code-drawn version of the bell's layout (two small brass bells on two tall dry piles, a tiny metal ball hanging between them,
under a glass cover) and a generic lab room whose decor changes with the era (1840 -> today) while the bell stays in place.
No real people, logos or signs. All coordinates are design units (1080x1920) under the shot camera.
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd, ease_out, ease_io, TAU
from flat_fx import sparkle, burst

BRASS, BRASS_D = "#E7B547", "#B9862A"
SULFUR, SULFUR_D = "#E9D35A", "#B8A23A"
WOOD, WOOD_D = "#8A5A3A", "#5E3A24"
GLASS = "#CFEFFF"


def ball_x(t, d=1.0):
    """Clapper position -1..1 between the two bells at 2 Hz (it touches a bell every half second); flattened sine = quick swing, short dwell."""
    s = math.sin(TAU * 2.0 * t)
    return d * math.copysign(abs(s) ** 0.55, s)


def bell_case(g, x, y, s=1.0, t=0.0, ring=1.0, glass=2, sulfur=0.0, xray=0.0, charge=0.0, hl_glass=0.0, hl_ball=0.0):
    """The apparatus, base centre at (x, y). ring 0..1 = clapper motion; glass = number of glass covers drawn (0-2);
    sulfur 0..1 highlights the sulfur coat on the piles; xray 0..1 shows layered discs inside the piles with a '?';
    charge 0..1 draws +/- charge signs on the bells and ball; hl_glass / hl_ball pulse highlights."""
    with g.at(x, y, 0, s):
        g.rect(-330, -60, 660, 90, WOOD, INK, lw=9, r=10)                           # wooden base
        g.rect(-300, -90, 600, 40, shade(WOOD, 0.15), INK, lw=7, r=8)
        px = 175
        for sgn in (-1, 1):                                                         # the two dry piles
            cx = sgn * px
            col = mix("#9A6A3A", SULFUR, 0.25 + 0.75 * sulfur)
            g.rect(cx - 55, -760, 110, 670, col, INK, lw=9, r=10)
            for yy in range(-740, -100, 22):
                g.line([(cx - 50, yy), (cx + 50, yy)], shade(col, -0.22), 3, a=0.55)
            g.rect(cx - 62, -120, 124, 36, "#7A6A5A", INK, lw=6, r=6)
            if sulfur > 0:
                g.glow(cx, -430, 180, "#FFF4A8", 0.35 * sulfur)
            if xray > 0:
                with g.group(xray):
                    g.rect(cx - 40, -740, 80, 630, "#2A1C1E", None, r=16, a=0.85)
                    for k in range(22):
                        yy = -728 + k * 28
                        g.rect(cx - 32, yy, 64, 12, ("#C9CED6", "#B8742E", "#E7B547")[k % 3], None, r=4)
                    g.text("?", cx, -420, 150, "#FFC93C", sw=16, a=1.0)
            g.rect(cx - 70, -800, 140, 50, BRASS_D, INK, lw=7, r=10)                # brass cap
            g.path(f"M{cx - 92} -792 C{cx - 72} -806 {cx - 60} -832 {cx - 56} -880 C{cx - 52} -936 {cx + 52} -936 {cx + 56} -880 "
                   f"C{cx + 60} -832 {cx + 72} -806 {cx + 92} -792 Z", BRASS, INK, lw=8)          # flared bell (rim wider than the pile)
            g.ellipse(cx, -792, 92, 14, BRASS_D, INK, lw=6)
            g.circle(cx, -944, 13, BRASS_D, INK, lw=5)
            g.ellipse(cx - 26, -880, 10, 24, "#FFF1C8", None, a=0.7, rot=0.25)
            if charge > 0:
                g.text("+" if sgn < 0 else "−", cx, -1000, 90, "#FF6B5B" if sgn < 0 else "#4FA8FF", sw=12, a=charge)
        g.rect(-12, -1040, 24, 120, "#7A6A5A", INK, lw=5)                            # little frame + thread
        g.rect(-140, -1050, 280, 22, "#7A6A5A", INK, lw=6, r=6)
        bx = ball_x(t) * 88 * ring
        g.line([(0, -1030), (bx, -872)], "#3A2A20", 3)
        r_b = 16
        if hl_ball > 0:
            g.circle(bx, -860, 60, None, "#FFC93C", lw=8, a=hl_ball)
        g.circle(bx, -860, r_b, "#C9CED6", INK, lw=5)
        g.circle(bx - 5, -865, 5, "#FFFFFF", None, a=0.9)
        if charge > 0:
            q = ball_x(t)
            g.text("+" if q < 0 else "−", bx, -800, 54, "#FF6B5B" if q < 0 else "#4FA8FF", sw=8, a=charge)
        hit = abs(ball_x(t)) > 0.97 and ring > 0.5
        if hit:
            sx = math.copysign(px - 75, ball_x(t))
            burst(g, sx, -860, 22, 60, n=7, col="#FFF4A8", w=6, k=1.0, a=0.9)
        for k in range(glass):                                                      # glass covers (bell jars)
            m = 40 + k * 45
            d = f"M{-330 - m * 0.2} -90 L{-330 - m * 0.2} {-1080 - m} Q{-330 - m * 0.2} {-1190 - m} {-200} {-1200 - m} L200 {-1200 - m} " \
                f"Q{330 + m * 0.2} {-1190 - m} {330 + m * 0.2} {-1080 - m} L{330 + m * 0.2} -90 Z"
            g.path(d, GLASS, mix(GLASS, INK, 0.4 + 0.3 * hl_glass), lw=7 + 6 * hl_glass, a=0.18 + 0.12 * hl_glass)
            g.line([(-280 - m * 0.2, -1000 - m), (-280 - m * 0.2, -300)], "#FFFFFF", 10, a=0.45)


# ------------------------------------------------------------------ the lab through the eras
ERA_WALL = {"1840": ("#6E4A3A", "#4A3026"), "1910": ("#5E6A4A", "#3E4A32"), "1940": ("#4A5A6A", "#2E3A4A"),
            "1969": ("#C98A3A", "#8A5A2A"), "now": ("#E6E8EC", "#C9CED6")}


def lab_room(g, t, era="1840", fy=1560, k_sky=0.0):
    """Corridor corner of an old physics lab. The bell case stands on a plinth in the centre (drawn by the caller).
    era: '1840' gas lamp + bookshelves, '1910' first planes in the window, '1940' taped window + radio, '1969' TV with a moon landing,
    'now' white walls + a laptop and phone. k_sky: animation phase for things passing outside."""
    top, bot = ERA_WALL[era]
    g.fill_all(g.lgrad(0, 0, 0, fy, top, bot))
    if era in ("1840", "1910"):
        for x in range(-100, W + 100, 120):
            g.rect(x, 0, 60, fy, shade(top, 0.06), None, a=0.5)
    wx, wy, ww, wh = 690, 300, 330, 520                                            # window (right)
    sky = {"1840": ("#9EC4DE", "#E6EEF2"), "1910": ("#8FC4EA", "#E6F2F8"), "1940": ("#7A8EA8", "#B9C6D4"),
           "1969": ("#14204A", "#2E3A6E"), "now": ("#8FD0F2", "#DDF2FA")}[era]
    g.rect(wx, wy, ww, wh, g.lgrad(0, wy, 0, wy + wh, *sky), None)
    with g.clip(rect=(wx, wy, ww, wh)):
        if era == "1910":                                                           # a biplane crosses
            px = wx - 200 + (k_sky * 700) % (ww + 400)
            with g.at(px, wy + 180, -0.05, 0.8):
                g.rect(-90, -8, 180, 18, "#C98A4A", INK, lw=4, r=6)
                g.rect(-20, -60, 50, 12, "#E9D2A0", INK, lw=4); g.rect(-20, 40, 50, 12, "#E9D2A0", INK, lw=4)
                g.line([(-5, -50), (-5, 42)], INK, 4); g.line([(20, -50), (20, 42)], INK, 4)
                g.line([(90, -30), (90, 30)], INK, 5)
        if era == "1969":
            R = rnd(3).random
            for i in range(20):
                g.circle(wx + R() * ww, wy + R() * wh, 3, "#FFFFFF", None, a=0.8)
            g.circle(wx + 230, wy + 140, 60, "#F4F1E0", INK, lw=5)
        if era in ("now",):
            g.circle(wx + 80 + (k_sky * 60) % 200, wy + 120, 40, "#FFFFFF", None, a=0.7)
    g.rect(wx, wy, ww, wh, None, INK, lw=12)
    g.line([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], INK, 9); g.line([(wx, wy + wh / 2), (wx + ww, wy + wh / 2)], INK, 9)
    if era == "1940":                                                               # taped window panes (neutral wartime detail)
        for (a0, b0) in (((wx, wy), (wx + ww, wy + wh)), ((wx + ww, wy), (wx, wy + wh))):
            g.line([a0, b0], "#F4E7C8", 14, a=0.9)
    # left side decor per era
    if era == "1840":
        g.rect(40, 340, 300, 600, WOOD_D, INK, lw=8)
        for k, yy in enumerate((420, 560, 700, 840)):
            g.rect(40, yy, 300, 16, WOOD, INK, lw=5)
            R = rnd(k + 1).random
            x = 55
            while x < 320:
                bw = 22 + R() * 20
                g.rect(x, yy - 110 + R() * 20, bw, 110 - R() * 20, ("#8E2430", "#2F5F6A", "#C98A3A", "#5B3A8C")[int(R() * 4)], INK, lw=3)
                x += bw + 3
        g.line([(220, 0), (220, 160)], INK, 6)                                     # gas lamp
        g.glow(220, 220, 220, "#FFD27A", 0.5)
        g.path("M180 170 L260 170 L245 260 L195 260 Z", "#F4E7C8", INK, lw=6, a=0.9)
    elif era == "1910":
        g.rect(60, 420, 260, 360, "#F4E7C8", INK, lw=7)                            # a framed chart
        for k in range(5):
            g.line([(90, 480 + k * 60), (290, 480 + k * 60)], "#8A7A6A", 5)
        g.line([(220, 0), (220, 140)], INK, 6); g.circle(220, 160, 28, "#FFF4C8", INK, lw=5); g.glow(220, 170, 200, "#FFF4C8", 0.4)
    elif era == "1940":
        g.rect(70, 1180, 230, 170, "#8A5A3A", INK, lw=8, r=24)                     # radio on a shelf
        g.rect(60, 1350, 260, 20, WOOD, INK, lw=6)
        g.circle(140, 1265, 52, "#C9A27A", INK, lw=6)
        for k in range(4):
            g.line([(205, 1220 + k * 30), (275, 1220 + k * 30)], "#3A2A20", 6)
        g.line([(220, 0), (220, 140)], INK, 6); g.circle(220, 160, 28, "#FFF4C8", INK, lw=5)
    elif era == "1969":
        g.rect(60, 1090, 320, 270, "#7A5A3A", INK, lw=9, r=20)                     # TV showing a moon landing
        g.rect(85, 1115, 230, 200, "#1A1A22", INK, lw=6, r=26)
        with g.clip(rect=(85, 1115, 230, 200)):
            g.rect(85, 1250, 230, 70, "#B9B9B0", None)
            g.circle(240, 1160, 26, "#2E6EA8", None)
            g.path("M150 1250 L170 1205 L210 1205 L230 1250 Z", "#E6E6E0", INK, lw=4)
            g.line([(160, 1250), (148, 1272)], INK, 4); g.line([(220, 1250), (232, 1272)], INK, 4)
        g.circle(345, 1170, 14, "#C9A27A", INK, lw=4); g.circle(345, 1220, 14, "#C9A27A", INK, lw=4)
        g.rect(60, 1360, 320, 20, WOOD, INK, lw=6)
        g.rect(-100, 0, W + 200, 60, "#5A4A3A", None)
        g.rect(200, 60, 500, 30, "#FFFBEA", INK, lw=5, r=8); g.glow(450, 120, 260, "#FFFBEA", 0.3)
    else:
        g.rect(60, 1300, 300, 20, "#C9CED6", INK, lw=6)                            # laptop + phone on a ledge
        g.path("M90 1300 L330 1300 L310 1150 L110 1150 Z", "#3A3F48", INK, lw=6)
        g.rect(125, 1165, 170, 115, "#4FA8FF", None, r=6, a=0.8)
        g.rect(-100, 0, W + 200, 50, "#F4F6F8", None)
        for x in (150, 560):
            g.rect(x, 50, 380, 26, "#FFFFFF", INK, lw=5, r=8); g.glow(x + 190, 100, 240, "#FFFFFF", 0.35)
    g.rect(-100, fy, W + 200, H - fy, g.lgrad(0, fy, 0, H, "#6E5A4A", "#3E3026") if era != "now" else g.lgrad(0, fy, 0, H, "#B9BEC6", "#8E949E"), None)
    g.rect(300, fy - 330, 480, 330, "#C9B79A" if era != "now" else "#E6E8EC", INK, lw=9, r=8)   # plinth for the case
    g.rect(280, fy - 360, 520, 40, shade("#C9B79A", -0.12), INK, lw=7, r=8)


def college(g, t, fy=1600):
    """A generic old sandstone college building at golden hour (arched windows, a small tower), lawn in front. No real building copied."""
    g.fill_all(g.lgrad(0, 0, 0, fy, "#F7B57A", "#FCE0B8"))
    g.glow(820, 380, 380, "#FFF0C0", 0.5)
    with g.layer(0.55):
        g.rect(80, 380, 900, fy - 380, "#D9B57A", INK, lw=10)
        g.rect(420, 120, 240, 280, "#D9B57A", INK, lw=10)
        g.path("M410 120 L540 -20 L670 120 Z", "#8A6A4A", INK, lw=9)
        for k in range(3):
            g.path(f"M{460 + k * 60} 330 L{460 + k * 60} 220 Q{480 + k * 60} 190 {500 + k * 60} 220 L{500 + k * 60} 330 Z", "#4A3A30", INK, lw=5)
        for row, yy in enumerate((560, 900, 1240)):
            for k in range(5):
                x = 140 + k * 170
                g.path(f"M{x} {yy + 220} L{x} {yy + 60} Q{x + 50} {yy - 10} {x + 100} {yy + 60} L{x + 100} {yy + 220} Z",
                       "#3E4A5A" if (k + row) % 3 else "#FFD27A", INK, lw=6)
        for x in range(80, 990, 60):
            g.rect(x, 340, 36, 40, "#D9B57A", INK, lw=5)
    g.rect(-100, fy, W + 200, H - fy, g.lgrad(0, fy, 0, H, "#6FBF5A", "#3E8E3A"), None)


def ten_billion(g, x, y, k, size=130, col="#FFC93C"):
    """Rolling counter from 0 to 10,000,000,000 (k 0..1, eased)."""
    v = int(10_000_000_000 * ease_out(clamp(k)) ** 1.6)
    g.text(f"{v:,}", x, y, size, col, sw=size * 0.14, depth=size * 0.07)


def pile_xray(g, x, y, s=1.0, t=0.0, k=1.0):
    """Big cut-away of one dry pile: thousands of thin discs stacked, a sulfur coat, a glowing question mark."""
    with g.at(x, y, 0, s):
        g.rect(-150, -900, 300, 900, SULFUR, INK, lw=10, r=40)
        g.rect(-110, -860, 220, 820, "#2A1C1E", None, r=30, a=0.9 * k)
        for i in range(40):
            yy = -850 + i * 20.5
            g.rect(-100, yy, 200, 9, ("#C9CED6", "#B8742E", "#E7B547")[i % 3], None, r=3, a=k)
        g.glow(0, -450, 260, "#FFC93C", 0.4 * k)
        g.text("?", 0, -400, 300, "#FFC93C", sw=28, a=k)
