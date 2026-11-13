"""Sample comedy Short 2: "Bread" (original). TrueWhys flat-2D look, new cast (Benny + the Goose). 1080x1920, 24 fps, CPU.
Story: Benny is chased by a goose -> phone says "Give it bread!" -> it works -> the goose checks ITS phone:
"where to get more bread" -> the map pin is Benny's backpack -> thirty geese with phones -> "how to escape 30 geese" -> "Good luck."
python comedy/sample2/make_sample2.py [--still t1,t2,...]"""
import sys, io, math, random, subprocess
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "lib")); sys.path.insert(0, str(ROOT / "comedy/sample"))
from toon import *  # noqa

W, H, FPS = 1080, 1920, 24
GROUND = 1600
END_STORY, END = 21.0, 22.6
FONT = str(ROOT / "library/fonts/LilitaOne-Regular.ttf")
FONT2 = str(ROOT / "library/fonts/Poppins-Bold.ttf")
OUT = HERE / "out"
BS, GS = 1.0, 0.95       # Benny / goose scale


def cl(u): return max(0.0, min(1.0, u))
def ease(t, a, b):
    u = cl((t - a) / (b - a)) if b > a else float(t >= a); return u * u * (3 - 2 * u)
def back(t, a, b, k=1.8):
    u = cl((t - a) / (b - a)) - 1; return 1 + u * u * ((k + 1) * u + k)
def lerp(a, b, u): return a + (b - a) * u
def h01(i, k=0): return (math.sin(i * 12.9898 + k * 78.233) * 43758.5453) % 1.0


def svg_doc(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<g stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')


def raster(svg):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGB")


def cam(s, cx, cy, shake=0.0, t=0.0):
    cx = min(max(cx, 540 / s), W - 540 / s); cy = min(max(cy, 960 / s), H - 960 / s)
    sx, sy = shake * math.sin(t * 93), shake * math.cos(t * 71)
    return f'translate({540+sx:.1f} {960+sy:.1f}) scale({s:.4f}) translate({-cx:.1f} {-cy:.1f})'


OVER = ('<defs><radialGradient id="vig" cx="0.5" cy="0.55" r="0.75"><stop offset="0.55" stop-color="#1B1430" stop-opacity="0"/>'
        '<stop offset="1" stop-color="#1B1430" stop-opacity="0.6"/></radialGradient></defs>'
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#vig)" stroke="none"/>')


# ------------------------------------------------------------------ park background (sunset, TrueWhys palette)
def park(scroll=0.0, t=0.0):
    s = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3A6B"/>'
         '<stop offset="0.5" stop-color="#B9607A"/><stop offset="0.8" stop-color="#F59A6B"/><stop offset="1" stop-color="#FFD28A"/></linearGradient>'
         '<radialGradient id="sun"><stop offset="0" stop-color="#FFF2B8"/><stop offset="0.25" stop-color="#FFD98A" stop-opacity="0.8"/>'
         '<stop offset="1" stop-color="#FFB36B" stop-opacity="0"/></radialGradient>'
         '<radialGradient id="lamp"><stop offset="0" stop-color="#FFE7A3" stop-opacity="0.85"/><stop offset="1" stop-color="#FFB36B" stop-opacity="0"/></radialGradient></defs>',
         '<rect x="-400" y="-400" width="1900" height="1720" fill="url(#sky)" stroke="none"/>',
         '<circle cx="780" cy="1120" r="520" fill="url(#sun)" stroke="none"/><circle cx="780" cy="1120" r="110" fill="#FFE9A6" stroke="none"/>']
    # far hills
    pts = []
    for x in range(-400, 1561, 40):
        xx = x + scroll * 0.12
        pts.append(f"{x} {1150 + 40*math.sin(xx/110) + 22*math.sin(xx/41):.0f}")
    s.append(f'<path d="M-400 1400 L{" L".join(pts)} L1560 1400 Z" fill="#6A4E7E" stroke="none"/>')
    # far tree silhouettes
    sp = 120; off = (scroll * 0.25) % sp
    for k in range(-4, 16):
        i = k + int(scroll * 0.25 // sp)
        x = k * sp - off; r = 46 + 26 * h01(i)
        s.append(f'<circle cx="{x:.0f}" cy="{1200 - r*0.6:.0f}" r="{r:.0f}" fill="#4E4A7E" stroke="none"/>'
                 f'<rect x="{x-6:.0f}" y="{1190:.0f}" width="12" height="60" fill="#4E4A7E" stroke="none"/>')
    # mid trees
    sp = 360; off = (scroll * 0.5) % sp
    for k in range(-3, 7):
        i = k + int(scroll * 0.5 // sp)
        x = k * sp - off + 60 * h01(i, 2); r = 120 + 40 * h01(i, 3)
        col = ["#3E7C59", "#4C8A4E", "#3A6E66"][int(h01(i, 4) * 3)]
        s.append(f'<rect x="{x-18:.0f}" y="{1180:.0f}" width="36" height="140" rx="10" fill="#6B4A32" stroke-width="8"/>'
                 f'<circle cx="{x:.0f}" cy="{1160-r*0.5:.0f}" r="{r:.0f}" fill="{col}" stroke-width="8"/>'
                 f'<circle cx="{x-r*0.35:.0f}" cy="{1160-r*0.85:.0f}" r="{r*0.35:.0f}" fill="#FFFFFF" fill-opacity="0.10" stroke="none"/>')
    # grass + bushes
    s.append('<rect x="-400" y="1300" width="1900" height="160" fill="#5E9E52" stroke-width="8"/>')
    sp = 260; off = (scroll * 0.8) % sp
    for k in range(-3, 9):
        i = k + int(scroll * 0.8 // sp)
        x = k * sp - off + 40 * h01(i, 5)
        s.append(f'<path d="M{x-80:.0f} 1360 Q{x-90:.0f} 1290 {x-30:.0f} 1296 Q{x:.0f} 1250 {x+40:.0f} 1290 Q{x+100:.0f} 1290 {x+86:.0f} 1360 Z" fill="#4E8C4A" stroke-width="8"/>')
    # lamps
    sp = 700; off = (scroll * 0.85) % sp
    for k in range(-2, 4):
        x = k * sp - off + 200
        s.append(f'<circle cx="{x:.0f}" cy="980" r="190" fill="url(#lamp)" stroke="none"/>'
                 f'<rect x="{x-9:.0f}" y="990" width="18" height="430" rx="6" fill="#2A2F3A" stroke-width="6"/>'
                 f'<path d="M{x-36:.0f} 990 L{x+36:.0f} 990 L{x+24:.0f} 950 L{x-24:.0f} 950 Z" fill="#FFE7A3" stroke-width="7"/>'
                 f'<path d="M{x-44:.0f} 950 L{x+44:.0f} 950 L{x:.0f} 920 Z" fill="#2A2F3A" stroke-width="7"/>')
    # path
    s.append('<rect x="-400" y="1440" width="1900" height="300" fill="#E6C08E" stroke-width="8"/>'
             '<rect x="-400" y="1440" width="1900" height="26" fill="#CFA36F" stroke="none"/>')
    sp = 230; off = (scroll * 1.0) % sp
    for k in range(-2, 8):
        i = k + int(scroll // sp)
        x = k * sp - off
        s.append(f'<ellipse cx="{x:.0f}" cy="{1560 + 90*h01(i,6):.0f}" rx="{26+14*h01(i,7):.0f}" ry="10" fill="#CFA36F" stroke="none"/>')
    s.append('<rect x="-400" y="1740" width="1900" height="400" fill="#4F8F47" stroke-width="8"/>')
    sp = 300; off = (scroll * 1.3) % sp
    for k in range(-2, 7):
        x = k * sp - off
        s.append(f'<path d="M{x:.0f} 1800 l14 -46 l10 40 l14 -56 l10 60 Z" fill="#3E7A3A" stroke-width="6"/>')
    return "".join(s)


def speedlines(t, op=1.0):
    out = []
    for i in range(9):
        y = 1050 + i * 70 + 20 * h01(i)
        x = (1200 - ((t * 2600 + i * 377) % 1600))
        out.append(f'<path d="M{x:.0f} {y:.0f} L{x+260:.0f} {y:.0f}" stroke="#FFFFFF" stroke-opacity="{0.55*op:.2f}" stroke-width="10"/>')
    return "".join(out)


def dust(x, y, t, t0, n=3):
    k = cl((t - t0) / 0.4)
    if k <= 0 or k >= 1: return ""
    return "".join(f'<circle cx="{x - i*40 - 60*k:.0f}" cy="{y - 10 - 26*k:.0f}" r="{22+26*k:.0f}" fill="#F3E3C8" '
                   f'fill-opacity="{0.9*(1-k):.2f}" stroke-width="6" stroke-opacity="{1-k:.2f}"/>' for i in range(n))


def feathers(t, t0, n=14, cx=400, cy=1300):
    out = []
    for i in range(n):
        u = (t - t0) + h01(i) * 2
        x = cx + (h01(i, 1) - 0.5) * 900 - u * 300
        y = cy + (h01(i, 2) - 0.5) * 500 + 60 * math.sin(u * 3 + i)
        out.append(g('<path d="M-22 0 Q0 -14 22 0 Q0 12 -22 0 Z" fill="#FFFFFF" stroke-width="5"/>', x, y, rot=u * 120 + i * 40))
    return "".join(out)


# ------------------------------------------------------------------ actors helpers
def B(x, y=0, face=1, **kw):
    return g(benny(**kw), x, GROUND + y, BS * face, BS)


def G(x, y=0, face=1, sc=GS, **kw):
    return g(goose(**kw), x, GROUND + y, sc * face, sc)


def beak_world(gx, nx, ny, sc=GS):
    return gx + (162 + nx + 60) * sc, GROUND + (-392 + ny) * sc


# ------------------------------------------------------------------ shots
def chase(t, flock=False):
    t0 = 0.0 if not flock else 17.0
    scroll = (t - t0) * (1400 if not flock else 1700)
    b = [park(scroll, t)]
    ph = (t - t0) * 2.7
    legs, arms, bob = run_pose(ph, 1.0, panic=False)
    kw = dict(legs=legs, arms=arms, bob=bob, lean=12, head=dict(expr="worried", mouth="wide", look=(-1, -0.2)))
    if not flock and t >= 1.45:
        k = ease(t, 1.45, 1.7)
        kw["arms"] = (arms[0], arms[1], lerp(arms[2], -70, k), lerp(arms[3], -100, k))
        kw["hold"] = "phone"; kw["item_rot"] = -20
        kw["head"] = dict(expr="worried", mouth="open", look=(1, -0.6))
    if flock:
        kw["head"] = dict(expr="surprised", mouth="wide", look=(-1, 0), hair_up=0.7)
        if t >= 18.4:
            k = ease(t, 18.4, 18.7)
            kw["arms"] = (arms[0], arms[1], lerp(arms[2], -70, k), lerp(arms[3], -100, k))
            kw["hold"] = "phone"; kw["item_rot"] = -20
            kw["head"] = dict(expr="surprised", mouth="open", look=(1, -0.6), hair_up=0.7)
    bx = 740
    gl = []
    if flock:
        for i in range(16):  # flock behind
            gx = 60 + (i % 8) * 50 + 30 * h01(i, 3) - 40 * (i // 8)
            gy = -60 - 55 * (i // 8) + 10 * h01(i, 4)
            sc = 0.5 + 0.15 * h01(i, 5)
            gl.append(G(gx, gy, 1, sc, ph=(t * 3.3 + h01(i)) % 1, flap=40 * math.sin(t * 40 + i), nx=40, ny=50,
                        beak=0.8 * (math.sin(t * 9 + i * 2) > 0.6), expr="angry", phone=False))
    gx = 300 if not flock else 470
    honks = (0.15, 0.85, 1.55) if not flock else (17.1, 17.6, 18.1, 18.6)
    bk = max([max(0, 1 - abs(t - h - 0.08) / 0.12) for h in honks] + [0])
    gl.append(G(gx, 0, 1, GS, ph=(t * 3.3) % 1, flap=38 * math.sin(t * 38), nx=50, ny=60, beak=bk, expr="angry"))
    b += gl
    b.append(dust(bx - 40, GROUND, (t * 2.7) % 1 / 2.7 + int(t * 2.7) / 2.7, int(t * 2.7) / 2.7))
    b.append(B(bx, 0, 1, **kw))
    b.append(speedlines(t))
    if flock:
        b.append(feathers(t, 17.0, 16, 300, 1250))
    return raster(svg_doc(f'<g transform="{cam(1.25, 520, 1340, 4, t)}">{"".join(b)}</g>' + OVER))


def bread_stop(t):
    """4.7 - 7.7: skid, throw bread, goose catches + munches, Benny relieved, walks off."""
    b = [park(3220, t)]
    # goose
    gx = lerp(-150, 300, ease(t, 4.7, 5.3))
    gk = dict(ph=(t * 3.3) % 1 if t < 5.3 else None, flap=30 * math.sin(t * 36) if t < 5.3 else 0, nx=40, ny=50, expr="angry", look=(1, 0))
    if t >= 5.3:
        gk.update(nx=lerp(40, 10, ease(t, 5.3, 5.6)), ny=lerp(50, 10, ease(t, 5.3, 5.6)), look=(1, -0.6))
    if t >= 5.97:
        bite = cl((t - 5.97) / 1.7) * 0.85
        gk.update(bread=bite, expr="munch", beak=0.35 * (math.sin((t - 5.97) * 50) > 0), look=(1, 0))
    b.append(G(gx, 0, 1, GS, **gk))
    # Benny
    bx = lerp(700, 790, ease(t, 4.7, 4.95)) if t < 7.1 else lerp(790, 980, ease(t, 7.1, 7.9))
    face = 1 if (t < 5.0 or t >= 7.1) else -1
    bk = dict(head=dict(expr="worried", mouth="open", look=(-1, 0)), breads=4)
    if t < 5.0:
        bk.update(lean=-14, legs=(30, 0, 50, 0), arms=(-60, 20, 40, 30))
    elif t < 5.45:
        k = ease(t, 5.05, 5.3)
        bk.update(arms=(-10, 20, lerp(20, 165, k), lerp(20, 30, k)), hold="baguette" if t >= 5.2 else None, item_rot=-70,
                  breads=3 if t >= 5.2 else 4, head=dict(expr="worried", mouth="closed", look=(1, 0)))
    elif t < 6.2:
        k = ease(t, 5.45, 5.6)
        bk.update(arms=(-10, 20, lerp(165, 60, k), 10), breads=3, head=dict(expr="surprised" if t < 6.0 else "happy", mouth="small", look=(1, 0)))
    elif t < 7.1:
        k = ease(t, 6.2, 6.45) * (1 - ease(t, 6.8, 7.0))
        bk.update(arms=(-10, 20, lerp(20, 175, k), lerp(20, 80, k)), breads=3,
                  head=dict(expr="happy" if t > 6.85 else "tired", mouth="closed" if t > 6.85 else "small", eyes="closed" if t < 6.85 else "open"))
        if t > 6.85:
            bk["head"] = dict(expr="smug", mouth="closed", look=(1, 0))
    else:
        legs, arms, bob = walk_pose((t - 7.1) * 1.6)
        bk.update(legs=legs, arms=arms, bob=bob, breads=3, head=dict(expr="happy_closed", mouth="closed"))
    b.append(dust(bx - 40, GROUND, t, 4.72))
    b.append(B(bx, 0, face, **bk))
    # flying baguette
    if 5.55 <= t < 5.97:
        u = (t - 5.55) / 0.42
        x0, y0 = bx - 120, GROUND - 420
        x1, y1 = beak_world(gx, gk["nx"], gk["ny"])
        x = lerp(x0, x1 + 60, u); y = lerp(y0, y1, u) - 240 * math.sin(math.pi * u)
        b.append(baguette(-720 * u, x, y, 190))
    # crumbs
    if 6.0 <= t < 7.7:
        bxw, byw = beak_world(gx, gk["nx"], gk["ny"])
        for i in range(6):
            u = ((t - 6.0) * 1.8 + h01(i)) % 1
            b.append(f'<circle cx="{bxw + 30 + 60*(h01(i,1)-0.5) + 30*u:.0f}" cy="{byw + 20 + 220*u*u:.0f}" r="7" fill="{BREAD}" stroke-width="4"/>')
    # "phew" sweat flick
    s, cx, cy = 1.15, 560, 1330
    return raster(svg_doc(f'<g transform="{cam(s, cx, cy, 6 if 4.7 <= t < 4.95 else 0, t)}">{"".join(b)}</g>' + OVER))


def goose_close(t, phase):
    """phase 'burp' 7.7-9.0, 'evil' 12.4-13.6"""
    b = [park(3220, t)]
    gx = 300
    if phase == "burp":
        gk = dict(nx=10, ny=10, expr="happy", look=(1, 0))
        if t < 7.85:
            gk.update(bread=lerp(0.85, 1.0, cl((t - 7.7) / 0.15)), expr="munch", beak=0.3)
        elif t < 8.2:
            gk.update(beak=1.0 * (1 - ease(t, 8.05, 8.2)), expr="happy", ny=lerp(10, -20, ease(t, 7.85, 7.95)))
        elif t < 8.45:
            gk.update(expr="angry", look=(1, 0))
        else:
            gk.update(expr="angry", look=(1, 0.7), phone=True)
        b.append(G(gx, 0, 1, GS, **gk))
        if 7.9 <= t < 8.5:  # burp cloud
            k = cl((t - 7.9) / 0.6)
            x, y = beak_world(gx, 10, -20)
            b.append(f'<circle cx="{x+40+60*k:.0f}" cy="{y-20-40*k:.0f}" r="{30+50*k:.0f}" fill="#FFFFFF" fill-opacity="{0.8*(1-k):.2f}" stroke-width="6" stroke-opacity="{1-k:.2f}"/>')
        s = 1.9
        return raster(svg_doc(f'<g transform="{cam(s, 470, 1270, 0, t)}">{"".join(b)}</g>' + OVER))
    # evil
    gk = dict(nx=10, ny=10, expr="evil", look=(1, 0), smirk=True, phone=t < 12.7)
    if t >= 12.95:
        gk.update(beak=0.9 * max(0, 1 - abs(t - 13.2) / 0.3))
    b.append(G(gx, 0, 1, GS, **gk))
    s = lerp(2.5, 2.9, ease(t, 12.4, 13.6))
    red = f'<rect x="0" y="0" width="{W}" height="{H}" fill="#8A1E3A" fill-opacity="{0.22*ease(t,12.7,13.0):.2f}" stroke="none"/>'
    return raster(svg_doc(f'<g transform="{cam(s, 430, 1215, 0, t)}">{"".join(b)}</g>' + red + OVER))


def benny_walk(t):
    """13.6 - 15.2 Benny walking happily, stops, feels it, slowly turns."""
    b = [park(3420 + (t - 13.6) * 120, t)]
    bx = 600
    if t < 14.2:
        legs, arms, bob = walk_pose((t - 13.6) * 1.6)
        bk = dict(legs=legs, arms=arms, bob=bob, breads=3, head=dict(expr="happy_closed", mouth="small"))
        face = 1
    else:
        bk = dict(breads=3, head=dict(expr="worried", mouth="closed", look=(-1 if t > 14.45 else 0, 0), sweat=t > 14.35))
        face = 1 if t < 14.85 else -1
        if t >= 14.85:
            bk["head"] = dict(expr="worried", mouth="small", look=(1, 0), sweat=True)
    b.append(B(bx, 0, face, **bk))
    if t < 14.2:  # whistle notes
        for i in range(2):
            k = ((t - 13.6) * 0.9 + i * 0.5) % 1
            b.append(g('<path d="M0 0 L0 -44 L26 -52 L26 -10" fill="none" stroke-width="7"/><ellipse cx="-8" cy="2" rx="12" ry="9" fill="#2A1C1E"/>'
                       '<ellipse cx="18" cy="-8" rx="12" ry="9" fill="#2A1C1E"/>', bx + 120 + 30 * math.sin(k * 6), GROUND - 560 - 120 * k,
                       extra=f'opacity="{math.sin(k*math.pi):.2f}"'))
    s = lerp(1.6, 1.9, ease(t, 14.2, 15.2))
    return raster(svg_doc(f'<g transform="{cam(s, 600, 1300, 0, t)}">{"".join(b)}</g>' + OVER))


FLOCK = []
for i in range(26):
    row = i // 9
    FLOCK.append(dict(x=-40 + (i % 9) * 82 + 30 * h01(i, 1) + (40 if row == 1 else 0), y=-150 + row * 55, sc=0.42 + row * 0.07 + 0.05 * h01(i, 2),
                      d=15.25 + 0.6 * h01(i, 3), face=1))


def reveal(t):
    b = [park(3420, t)]
    for fg in sorted(FLOCK, key=lambda f: f["y"]):
        k = back(t, fg["d"], fg["d"] + 0.25, 2.2)
        if t < fg["d"]: continue
        b.append(g(goose(expr="evil", phone=True, smirk=True, look=(1, 0)), fg["x"], GROUND + fg["y"], fg["sc"] * k, fg["sc"] * k))
    b.append(G(330, 0, 1, GS, expr="evil", phone=True, smirk=True, look=(1, 0)))
    take = t >= 16.1
    bk = dict(breads=3, head=dict(expr="surprised" if take else "worried", mouth="wide" if take else "small", look=(-1, 0),
                                  hair_up=back(t, 16.1, 16.3, 2.5) if take else 0, sweat=True))
    if take:
        bk.update(arms=(-40, 10, -40, 10))
    by = -80 * math.sin(math.pi * cl((t - 16.1) / 0.35)) if take else 0
    b.append(B(900, by, -1, **bk))
    if t < 16.3:
        s, cx, cy = 1.05, 540, 1250
    else:
        s, cx, cy = 1.9, 880, 1170
    return raster(svg_doc(f'<g transform="{cam(s, cx, cy, 8 if 16.1 <= t < 16.35 else 0, t)}">{"".join(b)}</g>' + OVER))


# ---- phone screens (Benny's and the goose's)
def text(d, s, cx, y, size, fill, font=FONT2, stroke=0, sf=(42, 28, 30), anchor="mm"):
    f = ImageFont.truetype(font, size)
    d.text((cx, y), s, font=f, fill=fill, anchor=anchor, stroke_width=stroke, stroke_fill=sf)


def phone_insert(t, t0, query, result, who="benny", t_type=(0.1, 1.3), t_res=1.6, shake=8):
    u = t - t0
    if who == "benny":
        bg = ('<defs><linearGradient id="pb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E3A6B"/><stop offset="1" stop-color="#B9607A"/></linearGradient></defs>'
              f'<rect x="-100" y="-100" width="{W+200}" height="{H+200}" fill="url(#pb)" stroke="none"/>' + speedlines(t, 0.8).replace("1050", "300"))
        for i in range(10):
            y = 200 + i * 180; x = (1300 - ((t * 3000 + i * 411) % 1700))
            bg += f'<path d="M{x:.0f} {y} L{x+360:.0f} {y}" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="14"/>'
    else:
        bg = ('<defs><radialGradient id="pg" cx="0.5" cy="0.4" r="0.8"><stop offset="0" stop-color="#F59A6B"/><stop offset="1" stop-color="#5A3A6E"/></radialGradient></defs>'
              f'<rect x="-100" y="-100" width="{W+200}" height="{H+200}" fill="url(#pg)" stroke="none"/>')
        for i in range(9):
            bg += f'<circle cx="{120 + 110*i}" cy="{300 + 1300*h01(i,9):.0f}" r="{60+60*h01(i,8):.0f}" fill="#FFE7A3" fill-opacity="0.18" stroke="none"/>'
    px0, py0, pw, ph = 200, 330, 680, 1240
    ph_svg = (f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="70" fill="#1F1B24" stroke-width="12"/>'
              f'<rect x="{px0+28}" y="{py0+40}" width="{pw-56}" height="{ph-80}" rx="44" fill="#F7F4EE" stroke="none"/>'
              f'<rect x="{px0+pw/2-60}" y="{py0+16}" width="120" height="14" rx="7" fill="#3A3550" stroke="none"/>'
              f'<rect x="{px0+50}" y="{py0+90}" width="{pw-100}" height="200" rx="40" fill="#FFFFFF" stroke-width="8"/>'
              f'<circle cx="{px0+105}" cy="{py0+150}" r="22" fill="none" stroke-width="8"/><path d="M{px0+121} {py0+166} l20 20" stroke-width="9"/>')
    if who == "goose":  # cracked screen corner
        ph_svg += (f'<path d="M{px0+pw-40} {py0+300} L{px0+pw-150} {py0+380} L{px0+pw-120} {py0+470} M{px0+pw-150} {py0+380} L{px0+pw-260} {py0+350}" '
                   f'fill="none" stroke="#9AA0B0" stroke-width="5"/>')
    # keyboard
    kb_y = py0 + ph - 470
    if u < t_res:
        ph_svg += f'<rect x="{px0+28}" y="{kb_y}" width="{pw-56}" height="430" rx="20" fill="#D9DCE6" stroke="none"/>'
        for r in range(4):
            for c in range(10 - (r == 3) * 6):
                kx = px0 + 48 + c * 59 + (r == 3) * 150; ky = kb_y + 24 + r * 100
                kw_ = 50 if r < 3 else 280
                ph_svg += f'<rect x="{kx}" y="{ky}" width="{kw_}" height="80" rx="10" fill="#FFFFFF" stroke="none"/>'
    # result card
    rk = back(t, t0 + t_res, t0 + t_res + 0.25, 2.0) if u >= t_res else 0
    if rk > 0:
        cx, cy = px0 + pw / 2, py0 + 660
        card = f'<rect x="-270" y="-300" width="540" height="600" rx="40" fill="#FFFFFF" stroke-width="9"/>'
        if result[1] == "bread":
            card += baguette(-20, 0, 120, 300).replace('stroke-width="8"', 'stroke-width="9"')
        elif result[1] == "map":
            card += ('<rect x="-230" y="-60" width="460" height="320" rx="24" fill="#CDE8B0" stroke-width="8"/>'
                     '<path d="M-230 120 Q-60 60 40 140 Q140 220 230 160" fill="none" stroke="#F3DDB0" stroke-width="40"/>'
                     '<ellipse cx="-120" cy="10" rx="70" ry="40" fill="#7CC6E8" stroke-width="6"/>'
                     + g('<path d="M0 0 Q-44 -60 -44 -90 Q-44 -134 0 -134 Q44 -134 44 -90 Q44 -60 0 0 Z" fill="#E8433A" stroke-width="7"/>'
                         '<circle cx="0" cy="-90" r="18" fill="#FFFFFF" stroke-width="6"/>', 70, 140 - 20 * abs(math.sin((t - t0) * 7))))
        elif result[1] == "luck":
            card += '<circle cx="0" cy="130" r="90" fill="#FFD23F" stroke-width="9"/><circle cx="-32" cy="110" r="12" fill="#2A1C1E" stroke="none"/><circle cx="32" cy="110" r="12" fill="#2A1C1E" stroke="none"/><path d="M-40 175 Q0 150 40 175" fill="none" stroke-width="9"/><path d="M60 80 Q70 110 58 122 Q46 110 60 80 Z" fill="#9FE3FF" stroke-width="5"/>'
        ph_svg += g(card, cx, cy, rk, rk)
    # hand / wing holding the phone
    if who == "benny":
        hand = (f'<path d="M150 1700 Q170 1500 260 1460 L300 1600 Q260 1740 230 2000 L120 2000 Z" fill="{SKIN}" stroke-width="12"/>'
                f'<path d="M880 1380 Q980 1400 990 1520 Q980 1700 900 2000 L760 2000 Q800 1700 820 1560 Z" fill="{SKIN}" stroke-width="12"/>'
                f'<path d="M980 1700 L980 2000 L700 2000 Z" fill="{HOODIE}" stroke-width="12"/>')
        thumb_tx = None
    else:
        hand = (f'<path d="M-40 1500 Q140 1400 300 1500 Q380 1560 330 1640 Q250 1700 120 1690 L-40 1800 Z" fill="{WHITE}" stroke-width="12"/>'
                f'<path d="M60 1560 L200 1580 M40 1620 L170 1640" fill="none" stroke="{WING}" stroke-width="10"/>'
                f'<path d="M1120 1300 Q960 1360 880 1480 Q900 1560 980 1560 L1120 1500 Z" fill="{WHITE}" stroke-width="12"/>')
    # pecking beak (goose types with its beak)
    peck = ""
    nq = len(query)
    ta, tb = t_type
    if who == "goose" and ta <= u < tb + 0.1:
        ci = int((u - ta) / (tb - ta) * nq)
        kxs = px0 + 80 + (ci * 137 % 560); kys = kb_y + 60 + (ci * 53 % 300)
        ph_frac = ((u - ta) / (tb - ta) * nq) % 1
        lift = 120 * abs(math.cos(ph_frac * math.pi))
        peck = g(f'<path d="M-10 -300 Q40 -700 260 -1300" fill="none" stroke="{INK}" stroke-width="214" stroke-linecap="round"/>'
                 f'<path d="M-10 -300 Q40 -700 260 -1300" fill="none" stroke="{WHITE}" stroke-width="190" stroke-linecap="round"/>'
                 f'<ellipse cx="-10" cy="-300" rx="160" ry="140" fill="{WHITE}" stroke-width="12"/>'
                 f'<path d="M-70 -190 L0 0 L70 -190 Q0 -170 -70 -190 Z" fill="{ORANGE}" stroke-width="10"/>'
                 f'<circle cx="0" cy="-200" r="22" fill="{ORANGE}" stroke-width="8"/>'
                 f'<ellipse cx="-70" cy="-300" rx="34" ry="42" fill="#FFFFFF" stroke-width="9"/><circle cx="-66" cy="-282" r="13" fill="{INK}" stroke="none"/>'
                 f'<ellipse cx="60" cy="-300" rx="34" ry="42" fill="#FFFFFF" stroke-width="9"/><circle cx="56" cy="-282" r="13" fill="{INK}" stroke="none"/>'
                 f'<path d="M-112 -360 L-36 -334 M24 -334 L100 -360" stroke-width="14"/>', kxs, kys - lift, 0.8, 0.8)
    sh = shake * math.sin(t * 60) if who == "benny" else 0
    svg = svg_doc(f'{bg}<g transform="translate({sh:.1f} {sh*0.6:.1f}) rotate({-3 if who=="benny" else 4} 540 960)">{ph_svg}{hand}{peck}</g>' + OVER)
    im = raster(svg)
    d = ImageDraw.Draw(im)
    # typed query
    if u >= ta:
        n = min(nq, int((u - ta) / (tb - ta) * nq))
        q = query[:n] + ("|" if (int(u * 4) % 2 == 0 and u < t_res) else "")
        rot_im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dd = ImageDraw.Draw(rot_im)
        f = ImageFont.truetype(FONT2, 54)
        lines, cur = [], ""
        for w_ in q.split(" "):
            tryl = (cur + " " + w_).strip()
            if dd.textlength(tryl, font=f) > 470 and cur:
                lines.append(cur); cur = w_
            else:
                cur = tryl
        lines.append(cur)
        for li, ln in enumerate(lines[:2]):
            dd.text((px0 + 145, py0 + 150 + li * 72), ln, font=f, fill=(42, 28, 30), anchor="lm")
        if rk > 0:
            fs = 92
            while ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(result[0], font=ImageFont.truetype(FONT, fs)) > 470:
                fs -= 4
            f = ImageFont.truetype(FONT, max(8, int(fs * rk)))
            dd.text((px0 + pw / 2, py0 + 660 - 185 * rk), result[0], font=f, fill=(232, 67, 58), anchor="mm",
                    stroke_width=0)
        rot_im = rot_im.rotate(3 if who == "benny" else -4, center=(540, 960), resample=Image.BICUBIC)
        rot_im = rot_im.transform(rot_im.size, Image.AFFINE, (1, 0, -sh, 0, 1, -sh * 0.6))
        im.paste(rot_im, (0, 0), rot_im)
    return im


def map_zoom(t):
    u = ease(t, 11.2, 12.2)
    s = lerp(1.0, 3.6, u)
    px, py = 640, 1180
    m = ['<rect x="-200" y="-200" width="1500" height="2400" fill="#CDE8B0" stroke="none"/>',
         '<path d="M-200 1300 Q300 1100 640 1180 Q1000 1260 1300 1000" fill="none" stroke="#2A1C1E" stroke-width="96"/>'
         '<path d="M-200 1300 Q300 1100 640 1180 Q1000 1260 1300 1000" fill="none" stroke="#F3DDB0" stroke-width="80"/>',
         '<path d="M300 -200 Q260 600 420 1160" fill="none" stroke="#F3DDB0" stroke-width="60"/>',
         '<ellipse cx="300" cy="700" rx="230" ry="150" fill="#7CC6E8" stroke-width="9"/>']
    for i in range(30):
        x = 1300 * h01(i, 11) - 100; y = 2100 * h01(i, 12) - 100
        if abs(y - (1180 + (x - 640) * 0.1)) < 160: continue
        m.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{30+30*h01(i,13):.0f}" fill="#5FA052" stroke-width="7"/>')
    # tiny Benny walking on the path, under the pin
    legs, arms, bob = walk_pose(t * 1.6)
    m.append(g(benny(legs=legs, arms=arms, bob=bob, breads=3, head=dict(expr="happy_closed")), px, py + 20, 0.16, 0.16))
    jump = 26 * abs(math.sin(t * 7)) * (1 - u)
    m.append(g('<path d="M0 0 Q-44 -60 -44 -90 Q-44 -134 0 -134 Q44 -134 44 -90 Q44 -60 0 0 Z" fill="#E8433A" stroke-width="7"/>'
               '<circle cx="0" cy="-90" r="18" fill="#FFFFFF" stroke-width="6"/>', px - 14, py - 90 - jump, 1.0 / max(1, s * 0.5), 1.0 / max(1, s * 0.5)))
    ring = ""
    if t >= 12.0:
        k = cl((t - 12.0) / 0.4)
        ring = f'<circle cx="540" cy="960" r="{140+260*k:.0f}" fill="none" stroke="#E8433A" stroke-width="14" stroke-opacity="{1-k:.2f}"/>'
    return raster(svg_doc(f'<g transform="translate(540 960) scale({s:.3f}) translate({-px} {-py+40})">{"".join(m)}</g>{ring}' + OVER))


def end_card(t):
    u = t - END_STORY
    b = ['<defs><radialGradient id="eg"><stop offset="0" stop-color="#3A5A8A"/><stop offset="1" stop-color="#1E2A4A"/></radialGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#eg)" stroke="none"/>']
    for i in range(16):
        a = i * math.pi / 8 + u * 0.25
        b.append(f'<path d="M540 1250 L{540+1700*math.cos(a):.0f} {1250+1700*math.sin(a):.0f} L{540+1700*math.cos(a+0.17):.0f} {1250+1700*math.sin(a+0.17):.0f} Z" fill="#FFFFFF" fill-opacity="0.06" stroke="none"/>')
    k = back(t, END_STORY, END_STORY + 0.35, 2.0)
    legs, arms, bob = run_pose(u * 2.7, 1.0, False)
    b.append(g(benny(legs=legs, arms=arms, bob=bob, lean=12, breads=3, head=dict(expr="worried", mouth="wide", look=(-1, 0))), 720, 1560, 1.15 * k, 1.15 * k))
    b.append(g(goose(ph=(u * 3.3) % 1, flap=38 * math.sin(u * 38), nx=50, ny=60, expr="angry"), 300, 1560, 1.05 * k, 1.05 * k))
    im = raster(svg_doc("".join(b)))
    d = ImageDraw.Draw(im)
    text(d, "Follow for", 540, 470 + 40 * (1 - cl(k)), 140, (255, 255, 255), FONT, 12)
    text(d, "more twists!", 540, 620 + 40 * (1 - cl(k)), 140, (255, 210, 63), FONT, 12)
    return im


SCRIPT = [  # (start, end, fn)
    (0.0, 2.3, lambda t: chase(t)),
    (2.3, 4.7, lambda t: phone_insert(t, 2.3, "how to escape a goose", ("Give it bread!", "bread"), "benny", (0.12, 1.45), 1.65)),
    (4.7, 7.7, bread_stop),
    (7.7, 9.0, lambda t: goose_close(t, "burp")),
    (9.0, 11.2, lambda t: phone_insert(t, 9.0, "where to get more bread", ("Found 1 nearby", "map"), "goose", (0.1, 1.5), 1.6, 0)),
    (11.2, 12.4, map_zoom),
    (12.4, 13.6, lambda t: goose_close(t, "evil")),
    (13.6, 15.2, benny_walk),
    (15.2, 17.0, reveal),
    (17.0, 19.0, lambda t: chase(t, True)),
    (19.0, 21.0, lambda t: phone_insert(t, 19.0, "how to escape 30 geese", ("Good luck.", "luck"), "benny", (0.05, 0.9), 1.05, 12)),
    (21.0, 22.6, end_card),
]


def frame(i):
    t = i / FPS
    for a, b, fn in SCRIPT:
        if a <= t < b:
            return fn(t).tobytes()
    return end_card(t).tobytes()


# ------------------------------------------------------------------ audio
SR = 44100
from make_sample import marimba, pluck, bell, sweep, noise_burst, mhz, popsnd, boing  # noqa: E402


def build_audio(path):
    import audio as A
    import soundfile as sf
    from scipy.signal import butter, lfilter
    n = int(END * SR); mix = np.zeros(n)
    BSB = ROOT / "library/sfx/bsb"

    def ld(name, a=0.0, b=None):
        x = A.load(BSB / name).mean(1)
        i, j = int(a * SR), (int(b * SR) if b else len(x))
        return x[i:j]

    def put(x, at, gain=1.0, rate=1.0):
        if x is None: return
        x = np.asarray(x, float)
        if x.ndim == 2: x = x.mean(1)
        if rate != 1.0:
            idx = np.arange(0, len(x) - 1, rate); x = np.interp(idx, np.arange(len(x)), x)
        i = int(at * SR)
        if i >= n or i < 0: return
        seg = x[:n - i] * gain
        mix[i:i + len(seg)] += seg

    honks = [ld("honk__trumpet-horn-for-bike-3_1086.mp3", a, b) for a, b in ((0.1, 0.38), (1.21, 1.5), (2.57, 2.84), (3.92, 4.19))]
    honk = lambda at, gain=0.8, rate=1.0, k=0: put(honks[k % 4], at, gain, rate)
    laughs = [ld("laugh__laughter_0490.mp3"), ld("laugh__laugh_0475.mp3"), ld("laugh__strident-laughter_0489.mp3"),
              ld("laugh__delirious-laughter-13_2103.mp3"), ld("laugh__delirious-laughter-3_2093.mp3")]
    wings = ld("wings__flight-of-a-pigeon_0840.mp3", 0.1, 0.7)
    lib = lambda name, dur=None: (A.sfx(name)[: int(dur * SR)] if dur else A.sfx(name))

    # --- chase music (original): 150 bpm A minor ostinato, pizz bass + stabs + snare
    def chase_music(t0, t1, intensity=1.0):
        beat = 60 / 150
        bass = [45, 45, 48, 45, 52, 45, 50, 48]
        k = 0; t = t0
        while t < t1 - 0.05:
            put(pluck(mhz(bass[k % 8]), 0.25, 0.32 * intensity), t)
            if k % 2 == 1:
                put(noise_burst(0.12, 0.12 * intensity, 1500, 7000, seed=k), t)
            if k % 8 == 0:
                for m in (69, 72, 76):
                    put(sweep(mhz(m), mhz(m) * 0.98, 0.28, 0.05 * intensity, 0), t)
            if k % 4 == 2:
                put(marimba(mhz([81, 79, 77, 76][(k // 4) % 4]), 0.3, 0.12 * intensity), t)
            t += beat / 2; k += 1

    chase_music(0.0, 2.3)
    chase_music(2.3, 4.6, 0.7)
    chase_music(17.0, 21.0, 1.15)
    # --- shot 1: chase
    for h in (0.15, 0.85, 1.55):
        honk(h, 0.75, 1.0, int(h * 7))
    for k in range(int(2.3 * 5.4)):
        put(lib("footsteps")[: int(0.15 * SR)] if lib("footsteps") is not None else None, k / 5.4, 0.5)
    for k in range(5):
        put(wings, k * 0.48, 0.35)
    put(lib("whoosh_soft"), 1.4, 0.6)
    # --- phone 1
    for c in range(len("how to escape a goose")):
        put(lib("tick"), 2.3 + 0.12 + c * (1.33 / 21), 0.55)
    put(lib("ding"), 2.3 + 1.65, 0.9); put(popsnd(0.4), 2.3 + 1.65)
    # --- skid + throw + catch + munch
    put(ld("skid__screeching-tires-4_2371.mp3", 2.05, 2.6), 4.7, 0.45)
    put(lib("whoosh"), 5.45, 0.8)
    put(sweep(500, 1400, 0.35, 0.12), 5.5)
    put(ld("boing__boing-cartoon-8_2284.mp3"), 5.95, 0.7); put(popsnd(0.5), 5.97)
    munch = ld("chewing__apple-crunched-2_1114.mp3")
    for k in range(5):
        put(munch[: int(0.3 * SR)], 6.05 + k * 0.33, 0.6)
    phew = OUT / "vox/phew.wav"
    if phew.exists():
        x, sr = sf.read(str(phew)); put(np.interp(np.arange(0, len(x), sr / SR * 1.08), np.arange(len(x)), x), 6.3, 0.9)
    # relieved whistle
    def whistle(t0, t1, seed):
        mel = [84, 88, 91, 88, 86, 84, 86, 79]
        t = t0; k = seed
        while t < t1:
            put(sweep(mhz(mel[k % 8]), mhz(mel[k % 8]) * 1.005, 0.22, 0.10, 5.5), t); t += 0.24; k += 1
    whistle(7.05, 7.7, 0)
    # --- burp + phone 2
    put(ld("burp__burp-3_1709.mp3"), 7.88, 1.0)
    put(lib("whoosh_soft"), 8.42, 0.5); put(popsnd(0.3), 8.45)
    for c in range(len("where to get more bread")):
        put(lib("thud"), 9.0 + 0.1 + c * (1.4 / 23), 0.35, 1.6)
    put(lib("ding"), 10.6, 0.9); put(popsnd(0.4), 10.6)
    # --- map zoom
    put(sweep(300, 1200, 1.0, 0.08), 11.2)
    put(bell(mhz(88), 1.0, 0.2), 12.0); put(bell(mhz(91), 1.0, 0.18), 12.12)
    # --- evil goose: sting + slow honk
    for m in (45, 48, 51):
        put(sweep(mhz(m), mhz(m), 1.0, 0.06, 0), 12.7)
    put(pluck(mhz(33), 1.2, 0.5), 12.7)
    honk(13.05, 0.9, 0.62, 2)
    # --- Benny walk: whistle, stop, tension
    whistle(13.6, 14.2, 3)
    put(sweep(220, 330, 0.9, 0.07, 3), 14.3)
    put(lib("whoosh_soft"), 14.82, 0.6)
    # --- reveal: pops + honks + dun dun DUNN + take
    for f in FLOCK:
        put(popsnd(0.18), f["d"]); honk(f["d"] + 0.02, 0.18, 0.9 + 0.5 * h01(int(f["d"] * 100)), int(f["d"] * 50))
    for k, at in enumerate((15.3, 15.6, 15.95)):
        for m in (40 - k * 2, 47 - k * 2):
            put(sweep(mhz(m), mhz(m), 0.5 + 0.3 * k, 0.09, 0), at)
        put(pluck(mhz(28 - k * 2), 0.8, 0.45), at)
    put(ld("boing__boing-cartoon-1_2277.mp3"), 16.1, 0.8)
    put(sweep(400, 1800, 0.3, 0.18), 16.12)
    # --- flock chase: scream + honk storm + laughs
    scream = OUT / "vox/scream.wav"
    if scream.exists():
        x, sr = sf.read(str(scream)); put(np.interp(np.arange(0, len(x), sr / SR * 1.18), np.arange(len(x)), x), 17.0, 1.0)
    rng = random.Random(3)
    for k in range(34):
        honk(17.0 + rng.random() * 3.9, 0.25 + 0.25 * rng.random(), 0.8 + 0.6 * rng.random(), k)
    for k in range(9):
        put(wings, 17.0 + k * 0.45, 0.4)
    for k in range(int(2.0 * 5.4)):
        put(lib("footsteps")[: int(0.15 * SR)], 17.0 + k / 5.4, 0.5)
    put(laughs[0], 17.4, 0.35); put(laughs[1], 17.9, 0.3)
    # --- phone 3 + "Good luck." + sad trombone + big laugh
    for c in range(len("how to escape 30 geese")):
        put(lib("tick"), 19.05 + c * (0.85 / 22), 0.55)
    put(lib("ding"), 20.05, 0.9)
    for k, (m, d) in enumerate(((55, 0.35), (54, 0.35), (53, 0.35), (52, 1.0))):
        put(sweep(mhz(m), mhz(m) * (0.97 if k == 3 else 1), d, 0.16, 5 if k == 3 else 0), 20.15 + k * 0.38)
    put(laughs[2], 20.2, 0.45); put(laughs[3], 20.3, 0.4); put(laughs[4], 20.5, 0.35)
    # end card ta-da
    for k, m in enumerate((72, 76, 79, 84)):
        put(marimba(mhz(m), 1.2, 0.16), END_STORY + 0.05 + k * 0.07)
    mix = np.tanh(mix * 1.1) / 1.1
    mix /= np.abs(mix).max() + 1e-9
    sf.write(str(path), np.stack([mix, mix], 1).astype(np.float32) * 0.9, SR)


def voices():
    """Two short wordless exclamations from the free offline Kokoro voice (no quota)."""
    vox = OUT / "vox"; vox.mkdir(parents=True, exist_ok=True)
    if (vox / "phew.wav").exists() and (vox / "scream.wav").exists():
        return
    from kokoro_onnx import Kokoro
    import soundfile as sf
    k = Kokoro("/opt/kokoro/kokoro-v1.0.onnx", "/opt/kokoro/voices-v1.0.bin")
    for name, txt, v, sp in (("phew", "Phew!", "am_puck", 1.0), ("scream", "AAAAAAAAAAH!", "am_puck", 0.8)):
        a, sr = k.create(txt, voice=v, speed=sp, lang="en-us"); sf.write(str(vox / f"{name}.wav"), a, sr)


def main():
    OUT.mkdir(exist_ok=True)
    if "--still" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--still") + 1].split(",")]
        ims = [Image.frombytes("RGB", (W, H), frame(int(round(t * FPS)))) for t in ts]
        cols = 8; rows = math.ceil(len(ims) / cols); tw, th = 216, 384
        sheet = Image.new("RGB", (cols * tw, rows * th), "white")
        for k, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
            ImageDraw.Draw(sheet).text(((k % cols) * tw + 6, (k // cols) * th + 6), f"{ts[k]:.2f}", fill="white")
        sheet.save(OUT / "contact.png")
        return
    voices()
    wav = OUT / "audio.wav"; build_audio(wav)
    nfr = int(END * FPS); silent = OUT / "video_silent.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", str(silent)], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, fr in enumerate(pool.imap(frame, range(nfr), chunksize=4)):
            ff.stdin.write(fr)
            if k % 96 == 0: print("frame", k, "/", nfr, flush=True)
    ff.stdin.close(); ff.wait()
    final = OUT / "sample_bread.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", str(final)], check=True)
    print("done", final)


if __name__ == "__main__":
    main()
