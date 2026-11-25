"""Holiday string-light assets for Style F (flat 2D), TrueWhys originals (added 25 Nov 2026 for A-030 one bulb / whole string).

    from flat_lights import porch_dusk, string_pts, light_string, bulb, big_bulb, loop_path, loop_diagram, plug
Neutral winter-holiday look only (snowy porch, coloured string lights, pine garland); no religious symbols.
All coordinates are design units (1080x1920) under the shot camera. Every drawing is code-made (no downloaded art).
"""
import math
from flat2d import W, H, INK, PAL, mix, shade, clamp, lerp, rnd, ease_out, path_at, TAU
from flat_fx import snow, sparkle, burst

BULB_COLS = ("#FF5B5B", "#FFC93C", "#5ED3B5", "#4FA8FF", "#FF8AD8", "#FF9E3D")
SNOW, SNOW_SH = "#F4FBFF", "#C9E2F2"
WIRE = "#1F3B2A"
SPARK = "#FFF4A8"


# ------------------------------------------------------------------ set: snowy porch at dusk
def porch_dusk(g, t, fy=1600, lit=1.0, snowing=True):
    """Purple-blue dusk, snowy roofs across the street, the front of a house with a door, lit windows, a roof edge (gutter) where
    the light string hangs, snow on the ground, two small pines. lit = how much the house windows glow."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#1B1D4A", "#3B2F6E", "#7A4F8E", "#D98A8A"))
    with g.layer(0.15):
        R = rnd(17).random
        for i in range(36):
            g.circle(R() * (W + 600) - 300, R() * 650 - 100, 2 + 3 * R(), "#FFFFFF", None, a=(0.3 + 0.5 * R()) * (0.6 + 0.4 * math.sin(t * 2 + i)))
    with g.layer(0.4):                                                   # houses across the street
        g.path(f"M-600 {fy-300} L-380 {fy-470} L-160 {fy-300} L40 {fy-460} L260 {fy-300} L700 {fy-300} L900 {fy-480} L1120 {fy-300} "
               f"L1500 {fy-300} L1700 {fy-450} L1700 {fy} L-600 {fy} Z", "#2B2A5E", None)
        R = rnd(9).random
        for i in range(14):
            x = -500 + i * 160 + R() * 40
            g.rect(x, fy - 260 + R() * 60, 30, 38, "#FFC96B", None, a=0.55 * lit)
        for i in range(30):                                              # neighbours' tiny lights
            x = -500 + i * 75
            g.circle(x, fy - 300 + 10 * math.sin(i * 1.3), 5, BULB_COLS[i % 6], None, a=0.7)
    with g.layer(0.75):                                                  # our house front
        top = 240
        g.rect(-200, top, W + 400, fy - top, "#3E5A8C", INK, lw=8)
        for yy in range(top + 40, fy, 46):
            g.line([(-200, yy), (W + 200, yy)], "#36507E", 4)
        # window left, door right
        g.rect(80, 760, 340, 300, "#FFD27A", INK, lw=9, r=10)
        g.glow(250, 910, 320, "#FFC96B", 0.28 * lit)
        g.line([(250, 760), (250, 1060)], INK, 7); g.line([(80, 910), (420, 910)], INK, 7)
        g.rect(60, 1060, 380, 30, SNOW, INK, lw=6, r=12)
        g.rect(640, 820, 300, 580, "#B0433E", INK, lw=9, r=10)
        g.rect(680, 870, 220, 200, "#9A3A36", INK, lw=5, r=8); g.rect(680, 1110, 220, 240, "#9A3A36", INK, lw=5, r=8)
        g.circle(900, 1150, 14, "#FFC93C", INK, lw=5)
        g.rect(600, 1400, 380, 46, "#8E9AB0", INK, lw=7, r=6)            # step
        g.rect(570, 1446, 440, 46, "#7A869C", INK, lw=7, r=6)
        # gutter / roof edge at the top
        g.rect(-200, 160, W + 400, 90, "#2A2F55", INK, lw=8)
        g.rect(-200, 130, W + 400, 44, SNOW, INK, lw=6, r=18)
        for i in range(14):                                              # icicles
            x = -60 + i * 90 + (i % 3) * 14
            g.poly([(x - 12, 250), (x + 12, 250), (x, 300 + (i % 4) * 22)], "#DDF1FF", INK, lw=4)
    g.rect(-600, fy, W + 1200, H - fy + 400, g.lgrad(0, fy, 0, H, SNOW, "#C9D9EE"), None)
    g.line([(-600, fy), (W + 600, fy)], INK, 7)
    for x, s in ((-20, 1.0), (1080, 1.1)):                               # small pines with snow
        with g.at(x, fy + 10, 0, s):
            for j in range(3):
                w_ = 180 - j * 45; y0 = -j * 120
                g.poly([(-w_, y0), (w_, y0), (0, y0 - 200)], "#2E6B4E", INK, lw=7)
                g.path(f"M{-w_*0.7} {y0-50} Q0 {y0-90} {w_*0.7} {y0-50}", None, SNOW, lw=14)
            g.rect(-20, 0, 40, 40, "#5A3E2E", INK, lw=5)
    if snowing:
        with g.layer(1.15):
            snow(g, t, (-200, -100, W + 200, H + 100), n=22, seed=11, col="#FFFFFF", size=(5, 11), speed=55, a=0.8)


# ------------------------------------------------------------------ the light string
def string_pts(x0, x1, y, n=14, sag=60, swags=3):
    """Bulb positions along a string hung in swags (catenary-ish) between x0 and x1 at height y."""
    pts = []
    for i in range(n):
        u = i / (n - 1)
        ph = (u * swags) % 1
        pts.append((lerp(x0, x1, u), y + sag * math.sin(math.pi * ph)))
    return pts


def bulb(g, x, y, s, col, on=1.0, rot=0.0, t=0.0, out=0.0):
    """One mini bulb hanging down from its green socket at (x, y). on 0..1 = lit; out 0..1 pulls the bulb out of the socket."""
    with g.at(x, y, rot, s):
        if on > 0.02:
            g.glow(0, 52 + out * 30, 95, col, 0.55 * on * (0.9 + 0.1 * math.sin(t * 7 + x)))
        dark = mix(col, "#2A2238", 0.62)
        g.path(f"M-13 {22 + out*40} Q-24 {52 + out*40} -15 {76 + out*40} Q0 {96 + out*40} 15 {76 + out*40} Q24 {52 + out*40} 13 {22 + out*40} Z",
               mix(dark, col, on), INK, lw=5)
        if on > 0.3:
            g.ellipse(-6, 50 + out * 40, 5, 12, "#FFFFFF", None, a=0.6 * on)
        g.rc(0, 12, 30, 30, "#2F5F3E", INK, lw=5, r=6)


def light_string(g, pts, on, t=0.0, s=1.0, cols=BULB_COLS, dead=None, out=None):
    """Wire through pts with a bulb at each point. on: number or list (per bulb, 0..1). dead: index of a burnt-out bulb (always dark);
    out: (index, 0..1) bulb pulled out of its socket."""
    wire = []
    for i in range(len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        for j in range(8):
            u = j / 8
            wire.append((lerp(xa, xb, u), lerp(ya, yb, u) + 6 * math.sin(math.pi * u)))
    wire.append(pts[-1])
    g.line(wire, INK, 11 * s); g.line(wire, WIRE, 6 * s)
    for i, (x, y) in enumerate(pts):
        k = on[i] if isinstance(on, (list, tuple)) else on
        if dead == i: k = 0.0
        o = out[1] if out and out[0] == i else 0.0
        bulb(g, x, y, s, cols[i % len(cols)], on=k, t=t, out=o)


def wave_on(n, k, start=0, reverse=False):
    """Per-bulb on-levels for a wave of light going out (k 0->1) from bulb `start` along the string."""
    out = []
    for i in range(n):
        d = abs(i - start) / max(1, n - 1)
        out.append(clamp(1 - (k * 1.6 - d) * 5) if not reverse else clamp((k * 1.6 - d) * 5))
    return out


# ------------------------------------------------------------------ big bulb cut-away
def big_bulb(g, x, y, s=1.0, t=0.0, glow=1.0, broken=0.0, shunt=0.0, spark=0.0, col="#FFC93C", arc=0.0):
    """Big mini-bulb seen through clear glass: two lead wires, the thin coiled filament (glows), and the shunt wire wrapped across
    the leads below it. broken 0..1 snaps the filament; shunt 0..1 highlights the shunt; arc 0..1 shows current jumping through it."""
    with g.at(x, y, 0, s):
        if glow > 0.02 and broken < 0.5:
            g.glow(0, -170, 420, col, 0.5 * glow)
        g.path("M-120 120 Q-210 -60 -150 -230 Q-80 -400 0 -410 Q80 -400 150 -230 Q210 -60 120 120 Z",
               mix("#DDEBFF", col, 0.25 * glow * (1 - broken)), INK, lw=10, a=0.95)
        g.path("M-90 60 Q-150 -80 -110 -210", None, "#FFFFFF", lw=12, a=0.45)
        # lead wires
        for sd in (-1, 1):
            g.line([(sd * 50, 160), (sd * 50, 20), (sd * 70, -170)], "#8E9AA8", 12)
            g.line([(sd * 50, 160), (sd * 50, 20), (sd * 70, -170)], "#C9D2DC", 5)
        # filament coil between lead tips
        hot = glow * (1 - broken)
        fil = "#FFF4A8" if hot > 0.3 else "#5A5A68"
        pts = [(-70 + 140 * q / 40, -170 - 26 * math.sin(q * 1.9)) for q in range(41)]
        if broken > 0:
            cut = 20
            dy = 50 * ease_out(broken)
            g.line(pts[:cut - 2] + [(pts[cut - 2][0] + 4, pts[cut - 2][1] + dy)], fil, 9)
            g.line([(pts[cut + 2][0] - 4, pts[cut + 2][1] + dy * 0.8)] + pts[cut + 2:], fil, 9)
        else:
            if hot > 0.3:
                g.line(pts, "#FFE066", 22, a=0.5 * hot)
            g.line(pts, fil, 9)
        if spark > 0:
            burst(g, 0, -170, 20, 40 + 110 * spark, 10, SPARK, 8, k=spark)
        # shunt: fine wire wrapped across both leads below the filament
        sh_c = mix("#9AA3AD", "#5EF0B0", shunt)
        if shunt > 0:
            g.glow(0, -40, 140, "#5EF0B0", 0.45 * shunt * (0.8 + 0.2 * math.sin(t * 12)))
        g.line([(-56, -40), (56, -40)], sh_c, 8)
        for q in range(7):
            xq = -48 + q * 16
            g.ellipse(xq, -40, 6, 16, None, sh_c, lw=5)
        if arc > 0:
            for q in range(3):
                ph = (t * 3 + q / 3) % 1
                g.circle(lerp(-56, 56, ph), -40 + 6 * math.sin(ph * 20), 11, "#FFF4A8", INK, lw=3, a=arc)
        # base
        g.rc(0, 200, 230, 140, "#2F5F3E", INK, lw=10, r=18)
        for yy in (160, 200, 240):
            g.line([(-100, yy), (100, yy)], "#244A30", 6)


# ------------------------------------------------------------------ loop diagram (series circuit)
def loop_path(cx, cy, w, h, r=120):
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    return (f"M{cx} {y1} L{x0 + r} {y1} Q{x0} {y1} {x0} {y1 - r} L{x0} {y0 + r} Q{x0} {y0} {x0 + r} {y0} L{x1 - r} {y0} "
            f"Q{x1} {y0} {x1} {y0 + r} L{x1} {y1 - r} Q{x1} {y1} {x1 - r} {y1} Z")


def plug(g, x, y, s=1.0, rot=0.0):
    with g.at(x, y, rot, s):
        g.rc(0, 0, 110, 80, "#E9EEF4", INK, lw=7, r=14)
        for sd in (-1, 1):
            g.rc(sd * 24, 62, 14, 44, "#C9A23A", INK, lw=4, r=3)


def loop_diagram(g, cx, cy, w, h, t, n=8, on=1.0, flow=0.0, gap=None, gap_k=0.0, dead=None, bypass=0.0, glow_loop=0.0, hl=None):
    """A series loop: wire round a rounded rectangle, a plug at the bottom, n bulbs evenly spaced (skipping the plug side).
    flow 0..1 = moving current dots; gap = bulb index where the loop is broken (gap_k opens it); dead = bulb drawn burnt out;
    bypass 0..1 = a green shunt bridge across the dead bulb; glow_loop highlights the whole loop; hl = bulb index highlighted."""
    d = loop_path(cx, cy, w, h)
    if glow_loop > 0:
        g.line([path_at(d, q / 120)[:2] for q in range(121)], "#FFE066", 34, a=0.35 * glow_loop)
    g.path(d, None, INK, lw=16); g.path(d, None, "#3E8E5E", lw=8)
    us = [0.06 + 0.88 * (i + 0.5) / n for i in range(n)]
    if flow > 0:
        stop = us[gap] if gap is not None and gap_k > 0.5 else 2.0
        for q in range(26):
            u = (q / 26 + t * 0.18) % 1
            if u > stop: u = stop - 0.01 * (q % 4)                 # charges pile up and stop at the break
            x, y = path_at(d, u)[:2]
            g.circle(x, y, 9, "#FFE066", INK, lw=3, a=flow)
    for i, u in enumerate(us):
        x, y = path_at(d, u)[:2]
        k = on[i] if isinstance(on, (list, tuple)) else on
        if dead == i: k = 0
        if hl == i:
            g.circle(x, y, 92, None, PAL["yellow"], lw=8)
        if gap == i and gap_k > 0:
            g.circle(x, y, 42, "#1B1D4A", None)
            g.line([(x - 40 * gap_k, y - 10), (x - 10, y + 10)], "#FF5B5B", 9); g.line([(x + 40 * gap_k, y + 10), (x + 10, y - 10)], "#FF5B5B", 9)
            continue
        if k > 0.05:
            g.glow(x, y, 80, BULB_COLS[i % 6], 0.5 * k)
        g.circle(x, y, 42, mix(mix(BULB_COLS[i % 6], "#2A2238", 0.65), BULB_COLS[i % 6], k), INK, lw=6)
        if dead == i:
            g.line([(x - 16, y - 16), (x + 16, y + 16)], INK, 6); g.line([(x - 16, y + 16), (x + 16, y - 16)], INK, 6)
            if bypass > 0:
                g.path(f"M{x - 52} {y} Q{x} {y - 80 * bypass} {x + 52} {y}", None, "#5EF0B0", lw=10, a=bypass)
    px, py = path_at(d, 0.0)[:2]
    plug(g, px, py + 70, 1.0)
