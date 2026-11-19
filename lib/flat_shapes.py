"""Style F props for everyday-shape stories (B-004, 19 Nov 2026). Original, code-drawn (TrueWhys). Reusable:
coin, coin_edge, scissors, candle, manhole (circle/square/Reuleaux), road_sign (circle/octagon/diamond/square/rect),
paper_bag (envelope or flat-bottomed), bottle (+ cork or crown cap), bottle_cap (top view, n teeth), cracker (holes, puff),
steam, razor_blade, reuleaux_pts, ngon_pts. All take the flat2d G object; (x, y) = centre unless noted; units = design pixels.
"""
import math
from flat2d import INK, PAL, shade, clamp, ease_out, TAU

SILVER, SILVER_D = "#D9DEE4", "#9AA3AD"
COPPER, COPPER_D = "#D98B52", "#9C5A2E"
GOLD = "#F2C14E"
IRON, IRON_D = "#4A4F5A", "#30343C"


def ngon_pts(n, r, rot=0.0):
    return [(r * math.cos(rot + i * TAU / n), r * math.sin(rot + i * TAU / n)) for i in range(n)]


def reuleaux_pts(r, rot=0.0, steps=24):
    """Reuleaux triangle with circumradius r (constant width = r*sqrt(3))."""
    v = ngon_pts(3, r, rot - math.pi / 2)
    w = r * math.sqrt(3)
    pts = []
    for i in range(3):
        c = v[i]; a0 = v[(i + 1) % 3]; a1 = v[(i + 2) % 3]
        t0 = math.atan2(a0[1] - c[1], a0[0] - c[0]); t1 = math.atan2(a1[1] - c[1], a1[0] - c[0])
        while t1 < t0: t1 += TAU
        for k in range(steps + 1):
            t = t0 + (t1 - t0) * k / steps
            pts.append((c[0] + w * math.cos(t), c[1] + w * math.sin(t)))
    return pts


def coin(g, x, y, r, metal="silver", ridges=True, clip=0.0, rot=0.0, face="head", glint=0.0, sx=1.0):
    """Coin seen face-on. clip = 0..1 how much of the rim is snipped off (a flat bite on the right). sx < 1 squashes (tilt)."""
    base, dk = {"silver": (SILVER, SILVER_D), "copper": (COPPER, COPPER_D), "gold": (GOLD, "#B8862A")}[metal]
    with g.at(x, y, rot, sx, 1.0):
        if clip > 0:
            g.c.save(); g.c.new_path(); g.c.rectangle(-r * 1.2, -r * 1.2, r * 2.4 - r * 0.55 * clip - r * 0.2, r * 2.4); g.c.clip()
        g.circle(0, 0, r, base, INK, lw=max(4, r * 0.06))
        if ridges:
            n = 60 if r > 120 else 40
            for i in range(n):
                a = i * TAU / n
                g.line([(r * 0.90 * math.cos(a), r * 0.90 * math.sin(a)), (r * 0.99 * math.cos(a), r * 0.99 * math.sin(a))], dk, max(2, r * 0.025))
        g.circle(0, 0, r * 0.80, None, dk, lw=max(3, r * 0.03))
        if face == "head":      # simple profile bust (generic, no real person/coin design)
            g.path(f"M{-r*0.28} {r*0.45} Q{-r*0.35} {r*0.05} {-r*0.18} {-r*0.18} Q{-r*0.10} {-r*0.48} {r*0.12} {-r*0.46} Q{r*0.32} {-r*0.40} {r*0.30} {-r*0.18}"
                   f" L{r*0.38} {-r*0.04} L{r*0.28} {r*0.02} Q{r*0.30} {r*0.22} {r*0.12} {r*0.24} L{r*0.14} {r*0.45} Z", dk, None, a=0.55)
        elif face == "value":
            g.text("10", 0, r * 0.08, r * 0.7, dk, stroke=None)
        if glint > 0:
            g.ellipse(-r * 0.35, -r * 0.4, r * 0.28, r * 0.12, "#FFFFFF", None, a=0.55 * glint, rot=-0.6)
        if clip > 0:
            g.c.restore()
            xc = r - r * 0.55 * clip
            h = math.sqrt(max(0.0, r * r - xc * xc))
            g.line([(xc, -h), (xc, h)], INK, max(4, r * 0.06))


def coin_edge(g, x, y, w, h, metal="silver", ridges=True, gap=0.0, gap_glow=0.0, layers=False):
    """Edge-on view of a coin rim (a wide band). gap = 0..1 width of a smooth trimmed patch in the middle. layers = clad sandwich."""
    base, dk = {"silver": (SILVER, SILVER_D), "copper": (COPPER, COPPER_D), "gold": (GOLD, "#B8862A")}[metal]
    with g.at(x, y):
        g.rc(0, 0, w, h, base, INK, lw=8, r=h * 0.22)
        if layers:
            g.rc(0, 0, w - 16, h * 0.36, COPPER, None, r=4)
        if ridges:
            n = int(w / 26)
            gw = gap * w * 0.4
            for i in range(n):
                xx = -w / 2 + 18 + i * (w - 36) / (n - 1)
                if abs(xx) < gw / 2: continue
                g.line([(xx, -h / 2 + 10), (xx, h / 2 - 10)], dk, 7)
        if gap > 0:
            gw = gap * w * 0.4
            g.rc(0, 0, gw, h - 16, shade(base, 1.06), None, r=6)
            if gap_glow > 0:
                g.rc(0, 0, gw + 30, h + 30, None, "#FF3B30", lw=10, r=16, a=gap_glow)


def scissors(g, x, y, s=1.0, open_k=0.5, rot=0.0):
    """Old iron shears; pivot at (x, y), blades point to +x."""
    a = 0.06 + 0.32 * open_k
    with g.at(x, y, rot, s):
        for sd in (-1, 1):
            with g.at(0, 0, sd * a):
                g.path(f"M0 {-sd*8} L230 {-sd*4} Q250 0 230 {sd*6} L0 {sd*16} Z", "#C8CED6", INK, lw=6)
                g.path(f"M-10 {sd*6} L-90 {sd*30}", None, "#5A5A6A", lw=18)
                g.circle(-120, sd * 40, 34, None, "#5A5A6A", lw=16)
                g.circle(-120, sd * 40, 34, None, INK, lw=4)
        g.circle(0, 0, 10, "#9AA3AD", INK, lw=4)


def candle(g, x, y, s=1.0, t=0.0, lit=1.0):
    """Candle in a holder; (x, y) = base."""
    with g.at(x, y, 0, s):
        g.ellipse(0, 0, 90, 22, "#8A6A44", INK, lw=6)
        g.rc(0, -110, 60, 200, "#FFF1D0", INK, lw=6, r=8)
        g.path("M-30 -205 Q-20 -190 -24 -170", None, "#F2DFB6", lw=8)
        g.line([(0, -210), (0, -232)], INK, 5)
        if lit > 0:
            f = 1 + 0.08 * math.sin(t * 17) + 0.05 * math.sin(t * 29)
            g.glow(0, -270, 260 * lit, "#FFC93C", 0.22 * lit)
            with g.at(0, -236, 0.04 * math.sin(t * 11), f * lit):
                g.path("M0 -64 Q26 -24 18 -6 Q10 10 0 10 Q-10 10 -18 -6 Q-26 -24 0 -64 Z", "#FFC93C", INK, lw=4)
                g.path("M0 -34 Q10 -14 6 -4 Q0 4 -6 -4 Q-10 -14 0 -34 Z", "#FFF4E0", None)


def steam(g, x, y, t, n=4, s=1.0, a=0.7, col="#FFFFFF"):
    for i in range(n):
        u = (t * 0.6 + i / n) % 1.0
        xx = x + (i - n / 2) * 30 * s + 18 * s * math.sin(u * 6 + i)
        g.circle(xx, y - 160 * s * u, (16 + 26 * u) * s, col, None, a=a * (1 - u))


def manhole(g, x, y, r, shape="circle", rot=0.0, tilt=0.38, lid=True, hole=True, lift=0.0, lid_dx=0.0, lid_rot=0.0):
    """Street manhole seen at an angle (tilt = vertical squash). shape: circle | square | reuleaux. lift raises the lid."""
    def pts(rr, rt):
        if shape == "square": return ngon_pts(4, rr * 1.18, rt + math.pi / 4)
        if shape == "reuleaux": return reuleaux_pts(rr * 1.05, rt)
        return ngon_pts(64, rr, rt)
    with g.at(x, y, 0, 1.0, tilt):
        if hole:
            g.poly(pts(r * 1.08, rot), "#8A8F98", INK, lw=10)
            g.poly(pts(r * 0.98, rot), "#141820", INK, lw=6)
        if lid:
            with g.at(lid_dx, -lift / tilt, 0):
                q = pts(r * 0.97, rot + lid_rot)
                g.poly([(px, py + 26) for px, py in q], IRON_D, None)
                g.poly(q, IRON, INK, lw=10)
                q2 = pts(r * 0.78, rot + lid_rot)
                g.poly(q2, None, "#5E6470", lw=8)
                for i in range(-3, 4):          # grip pattern
                    g.line([(-r * 0.6, i * r * 0.17), (r * 0.6, i * r * 0.17)], "#5E6470", 7, a=0.8)


def road_sign(g, x, y, r, shape="octagon", fill="#D7263D", text="STOP", tcol="#FFFFFF", post=0.0, rot=0.0, border="#FFFFFF", fade=0.0):
    """Road sign centred at (x, y). post = pole length below. fade 0..1 washes the colour towards pale pink."""
    if fade: fill = _mix(fill, "#F2C9C9", fade)
    if post > 0:
        g.rc(x, y + post / 2, r * 0.14, post, "#9AA3AD", INK, lw=6)
    with g.at(x, y, rot):
        if shape == "octagon":
            P = ngon_pts(8, r, math.pi / 8); P2 = ngon_pts(8, r * 0.88, math.pi / 8)
        elif shape == "diamond":
            P = ngon_pts(4, r, 0); P2 = ngon_pts(4, r * 0.86, 0)
        elif shape == "square":
            P = ngon_pts(4, r * 0.95, math.pi / 4); P2 = ngon_pts(4, r * 0.82, math.pi / 4)
        elif shape == "rect":
            P = [(-r * 1.2, -r * 0.7), (r * 1.2, -r * 0.7), (r * 1.2, r * 0.7), (-r * 1.2, r * 0.7)]
            P2 = [(px * 0.9, py * 0.85) for px, py in P]
        else:
            P = ngon_pts(64, r); P2 = ngon_pts(64, r * 0.88)
        g.poly(P, border, INK, lw=max(5, r * 0.06))
        g.poly(P2, fill, None)
        if text:
            g.text(text, 0, r * 0.06, r * (0.52 if len(text) <= 4 else 0.36), tcol, stroke=None)


def _mix(c1, c2, k):
    from flat2d import mix
    return mix(c1, c2, k)


def paper_bag(g, x, y, s=1.0, kind="flat", tip=0.0, col="#C8955A", label=None):
    """Paper bag standing on (x, y). kind: 'flat' (square bottom, gusseted) or 'envelope' (flat sack, V bottom)."""
    dk = shade(col, 0.8)
    with g.at(x, y, tip, s):
        if kind == "flat":
            g.poly([(-110, 0), (110, 0), (100, -300), (-100, -300)], col, INK, lw=7)
            g.poly([(110, 0), (160, -24), (150, -316), (100, -300)], dk, INK, lw=7)
            g.path("M-100 -300 L-86 -326 L-60 -300 L-30 -330 L0 -300 L30 -330 L60 -300 L86 -326 L100 -300", None, INK, lw=6)
            g.line([(-110, 0), (-100, -300)], dk, 4)
            g.poly([(-110, 0), (110, 0), (160, -24), (-60, -24)], shade(col, 0.7), INK, lw=5, a=0.6)
        else:
            g.path("M-90 0 L-100 -300 L100 -300 L90 0 L0 40 Z", col, INK, lw=7)
            g.line([(-90, 0), (0, 40), (90, 0)], dk, 5)
            g.path("M-100 -300 L-86 -326 L-60 -300 L-30 -330 L0 -300 L30 -330 L60 -300 L86 -326 L100 -300", None, INK, lw=6)
        if label:
            g.text(label, 0, -150, 54, "#FFF4E0", sw=8)


def bottle(g, x, y, s=1.0, liquid="#8A4A1E", stopper="crown", fizz=0.0, t=0.0, flat=0.0):
    """Glass bottle standing on (x, y). stopper: crown | cork | none. fizz = bubbles; flat = sad flat drink (fewer bubbles)."""
    with g.at(x, y, 0, s):
        body = "M-70 0 Q-80 0 -80 -20 L-80 -260 Q-80 -330 -34 -370 L-30 -470 L30 -470 L34 -370 Q80 -330 80 -260 L80 -20 Q80 0 70 0 Z"
        g.path(body, "#5FA67A", INK, lw=8, a=0.9)
        g.path("M-66 -12 L-66 -240 Q-66 -300 -24 -340 L24 -340 Q66 -300 66 -240 L66 -12 Z", liquid, None, a=0.9)
        g.rc(0, -170, 120, 90, "#FFF4E0", INK, lw=5, r=8)
        g.path("M-56 -230 L-56 -60", None, "#FFFFFF", lw=10, a=0.35)
        if fizz > 0:
            for i in range(10):
                u = (t * 0.7 + i * 0.137) % 1.0
                g.circle(-40 + (i * 37) % 80, -20 - 300 * u, 7 + (i % 3) * 2, "#FFFFFF", None, a=fizz * (1 - flat) * (1 - u))
        if stopper == "crown":
            g.rc(0, -478, 78, 22, "#C9A23A", INK, lw=5, r=4)
            for i in range(7):
                g.line([(-34 + i * 11.3, -468), (-34 + i * 11.3, -458)], INK, 4)
        elif stopper == "cork":
            g.rc(0, -490, 50, 60, "#B98A5A", INK, lw=5, r=6)
            g.path("M-30 -470 Q0 -540 30 -470", None, "#9AA3AD", lw=5)


def bottle_cap(g, x, y, r, teeth=21, hi=-1, hi_all=0.0, rot=0.0, col="#D7263D", txt=None):
    """Crown cap seen from above with `teeth` crimps. hi = index of the highlighted tooth (counting); hi_all = 0..1 glow on all."""
    with g.at(x, y, rot):
        pts = []
        for i in range(teeth * 2):
            a = i * math.pi / teeth - math.pi / 2
            rr = r if i % 2 == 0 else r * 0.88
            pts.append((rr * math.cos(a), rr * math.sin(a)))
        g.poly(pts, "#D9DEE4", INK, lw=max(4, r * 0.035), r=r * 0.03)
        g.circle(0, 0, r * 0.78, col, INK, lw=max(4, r * 0.03))
        g.circle(0, 0, r * 0.62, None, shade(col, 0.8), lw=max(3, r * 0.025))
        if txt:
            g.text(txt, 0, r * 0.06, r * 0.5, "#FFF4E0", sw=r * 0.06)
        for i in range(teeth):
            a = 2 * i * math.pi / teeth - math.pi / 2
            if i <= hi or hi_all > 0:
                k = 1.0 if i == hi else (0.55 if i < hi else hi_all)
                g.circle(r * 1.0 * math.cos(a), r * 1.0 * math.sin(a), r * 0.07, PAL["yellow"], INK, lw=3, a=k)


def cracker(g, x, y, s=1.0, holes=9, puff=0.0, col="#E9C27A", rot=0.0, square=True):
    """Cracker seen from above at a slight angle; puff 0..1 swells it into a pillow (side bulge + highlight)."""
    dk = shade(col, 0.8)
    with g.at(x, y, rot, s * (1 + 0.06 * puff), s * (1 + 0.10 * puff)):
        if puff > 0:
            g.ellipse(0, 26, 170, 40 + 50 * puff, shade(col, 0.75), INK, lw=6)
        if square:
            g.rc(0, 0, 320 + 30 * puff, 320 + 30 * puff, col, INK, lw=7, r=30 + 60 * puff)
            for i in range(-6, 7):
                g.circle(i * 24, -150, 6, None, dk, lw=4); g.circle(i * 24, 150, 6, None, dk, lw=4)
        else:
            g.circle(0, 0, 170, col, INK, lw=7)
        if puff > 0:
            g.ellipse(-50, -50, 90 * puff, 40 * puff, "#FFFFFF", None, a=0.35 * puff, rot=-0.5)
        m = int(round(math.sqrt(holes)))
        if holes > 0 and puff < 0.95:
            for i in range(m):
                for j in range(m):
                    hx = (i - (m - 1) / 2) * (200 / max(1, m - 1) if m > 1 else 0)
                    hy = (j - (m - 1) / 2) * (200 / max(1, m - 1) if m > 1 else 0)
                    g.circle(hx, hy, 11, shade(col, 0.6), INK, lw=3, a=1 - puff)


def razor_blade(g, x, y, s=1.0, rot=0.0, glint=0.0):
    with g.at(x, y, rot, s):
        g.rc(0, 0, 300, 120, "#D9DEE4", INK, lw=6, r=8)
        g.rc(0, 0, 150, 26, "#9AA3AD", INK, lw=4, r=12)
        g.circle(-110, 0, 18, "#9AA3AD", INK, lw=4); g.circle(110, 0, 18, "#9AA3AD", INK, lw=4)
        if glint:
            g.line([(-120, -40), (60, -40)], "#FFFFFF", 8, a=glint)
