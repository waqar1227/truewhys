"""Sample comedy Short: "The Mailbox" (premise 25 of docs/comedy/plan.md). Wordless, 1080x1920, 24 fps, CPU only.
Snap the crocodile, disguised as a mailbox, sneaks up on Pip the sparrow to steal his cupcake.
Twist: Pip posts him a party invitation - the cupcake was for Snap all along. Button: the candle gust.
python comedy/sample/make_sample.py [--still t1,t2,...]   -> comedy/sample/out/sample_mailbox.mp4 (or contact sheet)"""
import sys, io, math, subprocess, random
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "lib"))
from cast2d import *  # noqa

W, H, FPS = 1080, 1920, 24
GROUND = 1460
END_STORY, END = 17.4, 19.0
PIP_S, SNAP_S = 1.2, 0.82
FONT = str(ROOT / "library/fonts/LilitaOne-Regular.ttf")
OUT = HERE / "out"


# ------------------------------------------------------------------ helpers
def cl(u):
    return max(0.0, min(1.0, u))


def ease(t, a, b):
    u = cl((t - a) / (b - a)) if b > a else float(t >= a)
    return u * u * (3 - 2 * u)


def back(t, a, b, k=1.8):
    u = cl((t - a) / (b - a))
    u -= 1
    return 1 + u * u * ((k + 1) * u + k)


def lerp(a, b, u):
    return a + (b - a) * u


def blink_at(t, times, d=0.12):
    return any(0 <= t - x < d for x in times)


# ------------------------------------------------------------------ background (street with bus stop)
def background(t):
    s = ['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#7CCBFF"/><stop offset="0.75" stop-color="#D9F2FF"/><stop offset="1" stop-color="#FFF4D6"/></linearGradient>'
         '<radialGradient id="sun"><stop offset="0" stop-color="#FFF6B0"/><stop offset="1" stop-color="#FFF6B0" stop-opacity="0"/></radialGradient></defs>',
         f'<rect x="-200" y="-200" width="{W+400}" height="{H+400}" fill="url(#sky)" stroke="none"/>',
         '<circle cx="860" cy="300" r="260" fill="url(#sun)" stroke="none"/><circle cx="860" cy="300" r="90" fill="#FFE45C" stroke="none"/>']
    for i, (cx, cy, k) in enumerate(((160, 380, 1.0), (620, 220, 0.8), (980, 560, 0.7), (360, 640, 0.6))):
        x = (cx + t * 8 * (1 + i * 0.3)) % (W + 400) - 200
        s.append(g('<path d="M-90 30 Q-110 -20 -50 -24 Q-40 -70 10 -60 Q50 -90 80 -40 Q130 -40 120 30 Z" fill="#FFFFFF" stroke="none" fill-opacity="0.95"/>',
                   x, cy, k, k))
    # far hills + trees
    s.append('<path d="M-200 1060 Q150 900 420 1010 Q700 880 1000 990 Q1150 940 1300 1000 L1300 1300 L-200 1300 Z" fill="#A8DE86" stroke="none"/>')
    for tx, ty, r in ((90, 990, 46), (250, 960, 38), (700, 950, 44), (880, 975, 36), (1010, 985, 42)):
        s.append(f'<rect x="{tx-6}" y="{ty}" width="12" height="50" fill="#8A5A3B" stroke-width="5"/>'
                 f'<circle cx="{tx}" cy="{ty-10}" r="{r}" fill="#6CBF4E" stroke-width="5"/>')
    # houses
    houses = ((-30, 230, 300, "#FFB4A2", "#E85D5D"), (230, 220, 340, "#FFE08A", "#5B8DEF"),
              (480, 250, 280, "#B5E6D8", "#F28C28"), (760, 240, 330, "#D7C6FF", "#E85D5D"))
    for x, w, h, wall, roof in houses:
        base = 1250
        s.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="{wall}" stroke-width="7"/>')
        s.append(f'<path d="M{x-20} {base-h} L{x+w/2} {base-h-110} L{x+w+20} {base-h} Z" fill="{roof}" stroke-width="7"/>')
        for wx in (x + 30, x + w - 90):
            s.append(f'<rect x="{wx}" y="{base-h+50}" width="60" height="64" rx="6" fill="#FFF8DC" stroke-width="6"/>'
                     f'<path d="M{wx+30} {base-h+50} L{wx+30} {base-h+114} M{wx} {base-h+82} L{wx+60} {base-h+82}" stroke-width="5"/>')
        s.append(f'<rect x="{x+w/2-34}" y="{base-110}" width="68" height="110" rx="8" fill="#8A5A3B" stroke-width="6"/>')
    # hedge + fence
    s.append('<path d="M-200 1250 L1300 1250 L1300 1330 L-200 1330 Z" fill="#5FAF45" stroke-width="7"/>')
    for i in range(-4, 30):
        x = i * 48
        s.append(f'<path d="M{x} 1336 L{x} 1268 L{x+12} 1254 L{x+24} 1268 L{x+24} 1336 Z" fill="#FFFFFF" stroke-width="5"/>')
    s.append('<rect x="-200" y="1290" width="1500" height="14" fill="#FFFFFF" stroke-width="5"/>')
    # sidewalk
    s.append('<rect x="-200" y="1336" width="1500" height="460" fill="#EFD9B4" stroke-width="7"/>')
    for y in (1420, 1540, 1660):
        s.append(f'<path d="M-200 {y} L1300 {y}" stroke="#D6BC92" stroke-width="5"/>')
    for i in range(-3, 14):
        off = 60 if (i % 2) else 0
        for y0, y1 in ((1336, 1420), (1420, 1540), (1540, 1660), (1660, 1796)):
            x = i * 160 + (off if y0 in (1420, 1660) else 0)
            s.append(f'<path d="M{x} {y0} L{x} {y1}" stroke="#D6BC92" stroke-width="5"/>')
    s.append('<rect x="-200" y="1796" width="1500" height="40" fill="#C9B08A" stroke-width="7"/>'
             '<rect x="-200" y="1836" width="1500" height="300" fill="#6B6F7A" stroke-width="7"/>')
    # flower planter (left)
    s.append('<rect x="20" y="1370" width="150" height="70" rx="10" fill="#B36A3C" stroke-width="7"/>')
    for fx, col in ((45, "#FF6B8A"), (95, "#FFD23F"), (145, "#B07CFF")):
        s.append(f'<path d="M{fx} 1370 L{fx} 1320" stroke="#3E8E2E" stroke-width="6"/>'
                 f'<circle cx="{fx}" cy="1312" r="18" fill="{col}" stroke-width="5"/><circle cx="{fx}" cy="1312" r="6" fill="#FFF3A0" stroke="none"/>')
    # bus stop sign (pictogram only)
    s.append('<rect x="984" y="900" width="18" height="560" rx="6" fill="#9AA3AD" stroke-width="6"/>'
             '<circle cx="993" cy="880" r="74" fill="#2E8BEF" stroke-width="8"/>'
             '<rect x="947" y="846" width="92" height="56" rx="12" fill="#FFFFFF" stroke-width="6"/>'
             '<rect x="957" y="854" width="32" height="20" rx="3" fill="#2E8BEF" stroke="none"/><rect x="997" y="854" width="32" height="20" rx="3" fill="#2E8BEF" stroke="none"/>'
             '<circle cx="965" cy="906" r="9" fill="#2A1C1E" stroke="none"/><circle cx="1021" cy="906" r="9" fill="#2A1C1E" stroke="none"/>')
    return "".join(s)


def shadow(x, w):
    return f'<ellipse cx="{x:.1f}" cy="{GROUND+4}" rx="{w:.1f}" ry="{w*0.16:.1f}" fill="#000000" fill-opacity="0.16" stroke="none"/>'


# ------------------------------------------------------------------ Pip timeline
def pip_state(t):
    st = dict(x=760.0, y=0.0, sx=1.0, sy=1.0, face=1, kw=dict(expr="open", look=(1, 0), front="cupcake"))
    kw = st["kw"]
    # entry hops 0 - 1.8
    if t < 1.8:
        k = int(t / 0.6); u = (t - k * 0.6) / 0.6
        x0 = 560 + k * 67
        st["x"] = x0 + 67 * ease(u, 0.1, 0.9)
        st["y"] = -70 * math.sin(math.pi * cl((u - 0.1) / 0.8))
        sq = 1 - 0.14 * max(0, 1 - abs(u - 0.05) / 0.12) - 0.1 * max(0, 1 - abs(u - 0.98) / 0.1)
        st["sy"], st["sx"] = sq, 2 - sq
        kw.update(expr="happy")
    # humming windows
    hum = [(1.8, 3.3), (4.1, 5.1), (6.1, 11.6)]
    for a, b in hum:
        if a <= t < b:
            kw.update(expr="happy", notes=(t - a) * 0.9)
            st["sy"] = 1 + 0.025 * math.sin((t - a) * 2 * math.pi * 2)
    # suspicious look-backs
    for a, b, ex in ((3.3, 4.1, "half"), (5.1, 6.1, "half")):
        if a <= t < b:
            st["face"] = -1
            kw.update(expr=ex, look=(1, 0.15 if a > 5 else 0), notes=0)
            kw.pop("notes", None)
            pop = max(0, 1 - (t - a) / 0.1)
            st["sy"], st["sx"] = 1 - 0.08 * pop, 1 + 0.08 * pop
            if a > 5 and t > 5.5:
                kw.update(look=(1, 0.5))  # squints at the wagging tail
    # posting the envelope (back wing) 7.9 - 8.7
    if 7.85 <= t < 8.8:
        p = ease(t, 7.85, 8.1) * (1 - ease(t, 8.45, 8.75))
        kw.update(back="envelope" if t < 8.2 else None, back_p=p)
        if t >= 8.2:
            kw.update(back="empty", back_p=p)
    # after the insert: turn around and offer the cupcake
    if t >= 11.6:
        kw.pop("notes", None)
        st["face"] = 1 if t < 11.9 else -1
        kw.update(expr="open", look=(1, -0.4))
        if t >= 11.9:
            pop = max(0, 1 - (t - 11.9) / 0.12)
            st["sy"], st["sx"] = 1 - 0.1 * pop, 1 + 0.1 * pop
        lift = ease(t, 12.1, 12.4)
        kw["lift"] = lift
        if t >= 12.4:
            kw.update(front="cupcake_candle", flame=min(1, back(t, 12.4, 12.55)))
        if t >= 12.8:
            kw.update(expr="happy")
        if t >= 13.3:
            kw.update(expr="open", look=(1, -0.5))
        if t >= 14.3:  # gust!
            kw.update(flame=0, poof=min(1.15, back(t, 14.3, 14.45, 2.5)), expr="half", beak="flat", look=(1, -0.2))
            st["x"] = 760 + 18 * ease(t, 14.3, 14.4)
        if t >= 14.9:
            kw.update(look=(-0.9, 0.25))  # deadpan to camera
        if t >= 16.1:
            kw.update(front=None, lift=0)
        if t >= 16.5:
            kw.update(expr="squint")
    return st


# ------------------------------------------------------------------ Snap timeline
def snap_state(t):
    st = dict(x=340.0, y=0.0, sx=1.0, sy=1.0, rot=0.0,
              kw=dict(eyes=1.0, look=(1, 0.2), eye_expr="open", legs=(0, 0), tail=4 * math.sin(t * 7)))
    kw = st["kw"]
    kw["blink"] = blink_at(t, (0.7, 2.2, 4.6, 11.0))
    # tongue lick
    if 1.1 <= t < 1.8:
        kw["tongue"] = math.sin(math.pi * (t - 1.1) / 0.7)
    moves = ((2.4, 3.25, 340, 410), (4.3, 5.05, 410, 480), (6.3, 6.55, 480, 545))
    x = 340
    for a, b, x0, x1 in moves:
        if t >= a:
            x = lerp(x0, x1, ease(t, a, b)) if a > 6 else lerp(x0, x1, cl((t - a) / (b - a)))
        if a <= t < b and a < 6:  # tiptoe
            ph = (t - a) / (b - a) * 4
            k = ph % 1
            lift = 34 * math.sin(math.pi * k)
            kw["legs"] = (lift, 0) if int(ph) % 2 == 0 else (0, lift)
            st["y"] = -10 * math.sin(math.pi * k)
            kw["eyes"] = 1.0
    st["x"] = x
    # freezes (Pip looks back): leg stays up, eyes sink
    if 3.25 <= t < 4.1:
        kw["legs"] = (34, 0)
        kw["eyes"] = lerp(1, 0.15, ease(t, 3.3, 3.42))
    if 5.05 <= t < 6.1:
        kw["legs"] = (0, 34)
        kw["eyes"] = lerp(1, 0.15, ease(t, 5.1, 5.22))
        kw["tail"] = 18 * math.sin(t * 16) * (1 - ease(t, 5.5, 5.75))  # the tail gives him away... then stops
    if 4.1 <= t < 4.3 or 6.1 <= t < 6.3:
        kw["eyes"] = lerp(0.15, 1, ease(t, 4.1 if t < 5 else 6.1, (4.1 if t < 5 else 6.1) + 0.15))
    # zoom-in move: lean
    if 6.3 <= t < 6.75:
        st["rot"] = 10 * math.sin(math.pi * (t - 6.3) / 0.45)
    # attack: jaw opens slowly
    if 6.9 <= t < 8.25:
        kw["jaw"] = ease(t, 6.9, 7.9)
        kw["eye_expr"] = "half"
        kw["look"] = (1, 0.4)
        st["rot"] = 6 * ease(t, 6.9, 7.6)
        kw["drool"] = ease(t, 7.4, 8.1)
    if 8.25 <= t < 11.6:  # clack + take
        kw["jaw"] = 0
        sq = max(0, 1 - (t - 8.25) / 0.18)
        st["sy"], st["sx"] = 1 - 0.1 * sq, 1 + 0.08 * sq
        kw["eyes"] = 1 + 0.75 * cl(back(t, 8.3, 8.45, 3))
        kw["eye_expr"] = "wide"
        kw["look"] = (0, 0)
        if t > 8.7:
            kw["look"] = (0.6, 0.6)
    # reveal
    if t >= 11.6:
        kw.update(eye_expr="teary", eyes=1.0, look=(1, -0.2), legs=(0, 0), tail=10 * math.sin(t * 10))
        if t >= 11.75:
            u = cl((t - 11.75) / 0.9)
            kw["dome"] = 0
            kw["dome_xy"] = (520 * u, -1400 * u + 1300 * u * u - 160 * u, 400 * u)
            kw["head"] = min(1.08, back(t, 11.75, 12.0, 2.2))
            hk = dict(expr="teary", look=(1, 0))
            if t >= 12.9:
                hk = dict(expr="happy")
            if 13.3 <= t < 14.3:
                hk = dict(expr="inhale", cheeks=ease(t, 13.3, 14.1))
                st["sy"] = 1 + 0.05 * ease(t, 13.3, 14.1)
            if 14.3 <= t < 14.75:
                hk = dict(expr="blow")
            if t >= 14.75:
                hk = dict(expr="sheepish", look=(1, 0.3))
            if 15.95 <= t < 16.15:
                hk = dict(expr="open", mouth=1.0)
            if t >= 16.15:
                hk = dict(expr="chomp", cheeks=0.25 + 0.1 * math.sin(t * 30) * (t < 16.8))
            kw["head_kw"] = hk
            kw["head_tilt"] = (-6 * ease(t, 13.3, 14.1) if t < 14.3 else 10 * (1 - ease(t, 14.7, 15.2)))
            lunge = ease(t, 15.9, 16.0) - ease(t, 16.15, 16.45)
            kw["head_tilt"] += 26 * lunge
            kw["head_dx"] = 40 * lunge
    return st


# ------------------------------------------------------------------ effects
def confetti(t):
    if not 12.8 <= t < 15.5:
        return ""
    rng = random.Random(4)
    out = []
    cols = ["#FF6B8A", "#FFD23F", "#5BC0EB", "#7CD55A", "#B07CFF", "#FF9A2E"]
    dt = t - 12.8
    for i in range(70):
        a = rng.uniform(-2.6, -0.5); v = rng.uniform(600, 1300)
        x = 650 + math.cos(a) * v * dt
        y = 1100 + math.sin(a) * v * dt + 900 * dt * dt
        r = rng.uniform(0, 360) + dt * rng.uniform(200, 700)
        w = 14 + 10 * abs(math.sin(dt * 8 + i))
        out.append(f'<rect x="{x-w/2:.1f}" y="{y-8:.1f}" width="{w:.1f}" height="16" rx="3" fill="{rng.choice(cols)}" '
                   f'transform="rotate({r:.0f} {x:.1f} {y:.1f})" stroke="none"/>')
    return "".join(out)


def speed_lines(t):
    if not 6.3 <= t < 6.75:
        return ""
    op = 1 - ease(t, 6.5, 6.75)
    out = []
    for i, y in enumerate((1100, 1180, 1260, 1340, 1410)):
        x0 = 250 + i * 17
        out.append(f'<path d="M{x0} {y} L{x0+200} {y}" stroke="#FFFFFF" stroke-width="12" stroke-opacity="{op:.2f}"/>')
    for i in range(3):
        k = cl((t - 6.4) / 0.35)
        out.append(f'<circle cx="{460 - i*50 - 60*k:.0f}" cy="{GROUND-10-20*k:.0f}" r="{24+30*k:.0f}" fill="#F3E6CC" fill-opacity="{(1-k)*0.9:.2f}" stroke-width="5" stroke-opacity="{(1-k):.2f}"/>')
    return "".join(out)


def wind_lines(t):
    if not 14.25 <= t < 14.8:
        return ""
    k = cl((t - 14.25) / 0.45)
    out = []
    for i, y in enumerate((1010, 1050, 1090)):
        x0 = 600 + 160 * k
        out.append(f'<path d="M{x0-120:.0f} {y+i*4} Q{x0:.0f} {y-30} {x0+100:.0f} {y+10}" fill="none" stroke="#FFFFFF" stroke-width="10" stroke-opacity="{1-k:.2f}"/>')
    return "".join(out)


def impact(t):
    if not 8.25 <= t < 8.6:
        return ""
    k = cl((t - 8.25) / 0.35)
    cx, cy = 640, 1150
    out = []
    for i in range(8):
        a = i * math.pi / 4 + 0.2
        r0, r1 = 150 + 80 * k, 200 + 120 * k
        out.append(f'<path d="M{cx+r0*math.cos(a):.0f} {cy+r0*math.sin(a):.0f} L{cx+r1*math.cos(a):.0f} {cy+r1*math.sin(a):.0f}" stroke-width="10" stroke-opacity="{1-k:.2f}"/>')
    return "".join(out)


# ------------------------------------------------------------------ camera
def camera(t):
    s, cx, cy = 1.4, 610.0, 1234.0
    if 6.9 <= t < 9.0:
        u = ease(t, 6.9, 8.1)
        s, cx, cy = lerp(1.4, 1.6, u), lerp(610, 640, u), lerp(1234, 1250, u)
    if 11.6 <= t < 14.9:
        s, cx, cy = 1.4, 640, 1200
    if 14.9 <= t < 15.85:
        s, cx, cy = 1.95, 745, 1265
    if 15.85 <= t < 16.5:
        s, cx, cy = 1.4, 650, 1160
    if t >= 16.5:
        s, cx, cy = 1.85, 745, 1265
    cx = min(max(cx, 540 / s), W - 540 / s)
    cy = min(max(cy, 960 / s), H - 960 / s)
    shake = 0
    if 8.25 <= t < 8.5:
        shake = 14 * (1 - (t - 8.25) / 0.25)
    sx = shake * math.sin(t * 90)
    sy = shake * math.cos(t * 77)
    return f'translate({540+sx:.1f} {960+sy:.1f}) scale({s:.4f}) translate({-cx:.1f} {-cy:.1f})'


# ------------------------------------------------------------------ frames
def svg_doc(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<g stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{body}</g></svg>')


def raster(svg):
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGB")


def wide_frame(t):
    ps, ss = pip_state(t), snap_state(t)
    b = [background(t)]
    b.append(shadow(ss["x"], 150 * SNAP_S))
    b.append(shadow(ps["x"], 95 * PIP_S * (1 + 0.6 * ps["kw"].get("poof", 0))))
    kw = dict(ss["kw"])
    tilt, hdx = kw.pop("head_tilt", 0), kw.pop("head_dx", 0)
    snap_body = mailbox_snap(**kw)
    if kw.get("head", 0) > 0:  # tilt/lunge the head: rebuild with a wrapped head
        hk = kw.get("head_kw") or {}
        kw2 = dict(kw); kw2["head"] = 0.0001
        body_no_head = mailbox_snap(**{**kw2, "head": 0})
        head = g(g(croc_head(**hk), 0, 0, rot=tilt), 10 + hdx, -300 - 140 * kw["head"])
        # head behind the box front
        idx = body_no_head.find("<defs>")
        snap_body = body_no_head[:idx] + head + body_no_head[idx:]
    b.append(g(g(snap_body, 0, 0, ss["sx"], ss["sy"], ss["rot"]), ss["x"], GROUND + ss["y"], SNAP_S, SNAP_S))
    pk = dict(ps["kw"])
    lift = pk.pop("lift", 0)
    if pk.get("back") == "empty":
        pk["back"] = "wing"
    pip_body = pip(**pk)
    if lift:
        pip_body = pip_body  # lift handled inside via front offset below
    b.append(g(g(pip_lifted(pk, lift), 0, 0, ps["sx"] * ps["face"], ps["sy"]), ps["x"], GROUND + ps["y"], PIP_S, PIP_S))
    b += [speed_lines(t), impact(t), wind_lines(t), confetti(t)]
    return raster(svg_doc(f'<g transform="{camera(t)}">{"".join(b)}</g>'))


def pip_lifted(pk, lift):
    """Pip with the cupcake raised by `lift` (0..1) for the offer."""
    if not lift or not pk.get("front"):
        return pip(**pk)
    front = pk["front"]
    body = pip(**{**pk, "front": None})
    fl = pk.get("flame", 0)
    up = 95 * lift
    wing = f'<path d="M58 -146 Q118 {-150-up:.0f} 124 {-74-up:.0f} Q96 {-56-up:.0f} 66 -104 Z" fill="{YEL_D}"/>'
    cake = g(cupcake(candle=front == "cupcake_candle", flame=fl), 124, -66 - up, 0.95, 0.95)
    # remove the resting wing drawn by pip(front=None): it is the last wing path before eyes; simpler: draw over it
    return body + wing + cake


# ---- insert shot: inside close-up of the card
CARD_FONT = None


def insert_frame(t):
    u = t - 9.0
    s = 1 + 0.03 * u
    b = [f'<rect x="-100" y="-100" width="{W+200}" height="{H+200}" fill="{RED}" stroke="none"/>',
         f'<rect x="760" y="-100" width="400" height="{H+200}" fill="{RED_D}" stroke="none" fill-opacity="0.5"/>',
         f'<rect x="90" y="-100" width="60" height="{H+200}" fill="{RED_L}" stroke="none" fill-opacity="0.5"/>',
         '<path d="M-100 620 Q540 300 1180 620 L1180 -100 L-100 -100 Z" fill="#7CCBFF" stroke="none"/>',
         f'<path d="M-100 640 Q540 300 1180 640" fill="none" stroke-width="14"/>']
    # big croc eyes peeking over the dome (reading, then teary)
    ex = "open" if u < 1.2 else "teary"
    look = (0, 0.9) if u < 1.2 else (0, 0.5)
    bl = blink_at(t, (9.9,))
    for cx in (360, 720):
        b.append(f'<ellipse cx="{cx}" cy="470" rx="170" ry="150" fill="{GREEN}" stroke-width="14"/>')
        b.append(eye(cx, 430, 105, 118, ex, look, GREEN, bl).replace('stroke-width="7"', 'stroke-width="12"'))
    # mail slot with a claw holding the card
    b.append('<rect x="160" y="1500" width="760" height="90" rx="40" fill="#3A1A1E" stroke-width="14"/>')
    op = ease(t, 9.15, 9.6)
    cw, chh = 700, 520 * (0.35 + 0.65 * op)
    cy0 = 1000
    b.append(f'<g transform="rotate(-3 540 {cy0})"><rect x="{540-cw/2}" y="{cy0-chh/2:.0f}" width="{cw}" height="{chh:.0f}" rx="22" fill="#FFFDF5" stroke-width="12"/>')
    if op > 0.6:
        for bx, by, col in ((240, 860, "#FF6B8A"), (300, 830, "#5BC0EB"), (820, 850, "#FFD23F"), (770, 820, "#7CD55A")):
            b.append(f'<path d="M{bx} {by+60} Q{bx-10} {by+120} {bx+6} {by+170}" fill="none" stroke-width="5"/>'
                     f'<ellipse cx="{bx}" cy="{by}" rx="42" ry="52" fill="{col}" stroke-width="8"/>')
    b.append('</g>')
    # claw from the slot
    b.append(f'<path d="M470 1540 L470 {cy0+chh/2+10:.0f} Q540 {cy0+chh/2-40:.0f} 610 {cy0+chh/2+10:.0f} L610 1540 Z" fill="{GREEN}" stroke-width="12"/>')
    for i in range(4):
        x = 478 + i * 40
        b.append(f'<path d="M{x} {cy0+chh/2-10:.0f} q16 -40 32 0" fill="{GREEN_L}" stroke-width="9"/>')
    svg = svg_doc(f'<g transform="translate(540 960) scale({s:.4f}) translate(-540 -960)">{"".join(b)}</g>')
    im = raster(svg)
    if op > 0.6:
        d = ImageDraw.Draw(im)
        a = cl((op - 0.6) / 0.4)
        for txt, size, y, col in (("PARTY", 170, 930, (255, 107, 91)), ("for SNAP!", 104, 1080, (46, 139, 239))):
            f = ImageFont.truetype(FONT, int(size * s))
            wdt = d.textlength(txt, font=f)
            x = 540 - wdt / 2
            yy = 960 + (y - 960) * s - size * s / 2
            d.text((x, yy), txt, font=f, fill=col, stroke_width=int(8 * s), stroke_fill=(42, 28, 30))
        if a < 1:
            im = Image.blend(raster(svg), im, a)
    return im


def end_frame(t):
    u = t - END_STORY
    b = ['<defs><radialGradient id="eg"><stop offset="0" stop-color="#FFE98A"/><stop offset="1" stop-color="#FFB547"/></radialGradient></defs>',
         f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#eg)" stroke="none"/>']
    for i in range(16):
        a = i * math.pi / 8 + u * 0.3
        b.append(f'<path d="M540 900 L{540+1600*math.cos(a):.0f} {900+1600*math.sin(a):.0f} L{540+1600*math.cos(a+0.18):.0f} {900+1600*math.sin(a+0.18):.0f} Z" fill="#FFFFFF" fill-opacity="0.18" stroke="none"/>')
    k = back(t, END_STORY, END_STORY + 0.35, 2.0)
    b.append(g(pip(expr="happy", front="cupcake", notes=u), 300, 1420, 1.75 * k, 1.75 * k))
    b.append(g(g(croc_head(expr="happy"), 0, 0, -1, 1), 860, 1330, 1.45 * k, 1.45 * k))
    im = raster(svg_doc("".join(b)))
    d = ImageDraw.Draw(im)
    for txt, y in (("Follow for", 420), ("more twists!", 560)):
        f = ImageFont.truetype(FONT, 140)
        w = d.textlength(txt, font=f)
        d.text((540 - w / 2, y + 40 * (1 - cl(k))), txt, font=f, fill=(255, 255, 255), stroke_width=12, stroke_fill=(42, 28, 30))
    return im


def frame(i):
    t = i / FPS
    if t >= END_STORY:
        im = end_frame(t)
    elif 9.0 <= t < 11.6:
        im = insert_frame(t)
    else:
        im = wide_frame(t)
    return im.tobytes()


# ------------------------------------------------------------------ audio
SR = 44100


def tone_env(n, a=0.005, decay=6.0):
    t = np.arange(n) / SR
    return np.minimum(1, t / a) * np.exp(-decay * t)


def mhz(m):
    return 440 * 2 ** ((m - 69) / 12)


def marimba(f, dur=0.5, amp=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    return amp * tone_env(n, 0.003, 7) * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 4 * f * t) * np.exp(-30 * t))


def pluck(f, dur=0.35, amp=0.35):
    n = int(dur * SR); t = np.arange(n) / SR
    return amp * tone_env(n, 0.002, 12) * (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) + 0.2 * np.sin(6 * np.pi * f * t))


def bell(f, dur=1.2, amp=0.25):
    n = int(dur * SR); t = np.arange(n) / SR
    return amp * tone_env(n, 0.002, 3) * (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2.76 * f * t) * np.exp(-4 * t))


def sweep(f0, f1, dur, amp=0.3, vib=6.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f0 * (f1 / f0) ** (t / dur) * (1 + 0.02 * np.sin(2 * np.pi * vib * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.05)
    return amp * env * (np.sin(ph) + 0.15 * np.sin(2 * ph))


def boing(dur=0.6, amp=0.4):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 180 + 120 * np.sin(2 * np.pi * 9 * t) * np.exp(-3 * t) + 60 * t
    ph = 2 * np.pi * np.cumsum(f) / SR
    return amp * np.exp(-4 * t) * np.minimum(1, t / 0.005) * np.sin(ph)


def popsnd(amp=0.5):
    n = int(0.08 * SR); t = np.arange(n) / SR
    f = 1100 * np.exp(-28 * t) + 180
    return amp * np.exp(-30 * t) * np.sin(2 * np.pi * np.cumsum(f) / SR)


def noise_burst(dur, amp, lo=300, hi=6000, shape="fall", seed=0):
    from scipy.signal import butter, lfilter
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.random.default_rng(seed).normal(0, 1, n)
    b, a = butter(2, [lo / (SR / 2), min(0.99, hi / (SR / 2))], "band")
    x = lfilter(b, a, x)
    x /= np.abs(x).max() + 1e-9
    env = np.exp(-6 * t) if shape == "fall" else (t / dur) ** 2 * np.minimum(1, (dur - t) / 0.03)
    return amp * env * x


def party_horn(dur=0.7, amp=0.3):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 420 + 120 * np.minimum(1, t / 0.15)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = 2 * ((ph / (2 * np.pi)) % 1) - 1
    buzz = saw * (1 + 0.4 * np.sin(2 * np.pi * 31 * t))
    env = np.minimum(1, t / 0.02) * np.minimum(1, (dur - t) / 0.08)
    return amp * 0.5 * env * buzz


def hum(t0, t1, seed):
    """Pip humming: a little whistled tune (wordless voice)."""
    rng = random.Random(seed)
    melody = [84, 86, 88, 86, 84, 88, 91, 89, 88, 86, 84, 79]
    n = int((t1 - t0) * SR); out = np.zeros(n)
    step = 0.26; pos = 0; k = rng.randint(0, 4)
    while pos < n:
        m = melody[k % len(melody)]; k += 1
        dn = int(step * SR * (2 if k % 4 == 0 else 1))
        tt = np.arange(min(dn, n - pos)) / SR
        f = mhz(m) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt))
        env = np.minimum(1, tt / 0.03) * np.minimum(1, (dn / SR - tt) / 0.04)
        out[pos:pos + len(tt)] += 0.13 * env * (np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.08 * np.sin(4 * np.pi * np.cumsum(f) / SR))
        pos += dn
    fade = np.minimum(1, np.minimum(np.arange(n), n - np.arange(n)) / (0.05 * SR))
    return out * fade


def music(total):
    """Original bouncy cartoon loop, 120 bpm, C major (code-generated)."""
    n = int(total * SR); out = np.zeros(n)
    rng = random.Random(7)
    beat = 0.5
    chords = [(48, [60, 64, 67]), (45, [57, 60, 64]), (41, [57, 60, 65]), (43, [59, 62, 67])]
    t = 0.0; bar = 0
    while t < total:
        root, tones = chords[bar % 4]
        for b4 in range(4):
            tb = t + b4 * beat
            i = int(tb * SR)
            if i >= n: break
            bass = pluck(mhz(root if b4 % 2 == 0 else root + 7), 0.4, 0.32)
            out[i:i + len(bass)] += bass[:n - i]
            # shaker on off-beats
            j = int((tb + beat / 2) * SR)
            if j < n:
                sh = noise_burst(0.06, 0.05, 4000, 12000, seed=b4)
                out[j:j + len(sh)] += sh[:n - j]
            for e in range(2):
                if rng.random() < 0.8:
                    m = rng.choice(tones) + 12 + (12 if rng.random() < 0.2 else 0)
                    k = int((tb + e * beat / 2) * SR)
                    mm = marimba(mhz(m), 0.45, 0.14)
                    if k < n: out[k:k + len(mm)] += mm[:n - k]
        t += 4 * beat; bar += 1
    return out


def build_audio(path):
    total = END
    n = int(total * SR)
    mix = np.zeros(n)

    def put(x, at, gain=1.0):
        if x is None: return
        x = np.asarray(x)
        if x.ndim == 2: x = x.mean(1)
        i = int(at * SR)
        if i >= n: return
        seg = x[:n - i] * gain
        mix[i:i + len(seg)] += seg

    import audio as A  # lib/audio.py (CC0 library sfx)
    lib = lambda name, dur=None: (A.sfx(name)[: int(dur * SR)] if dur else A.sfx(name))
    # music with gags: it stops dead whenever Pip looks back
    mus = music(total)
    gate = np.zeros(n)
    for a, b, lvl in ((0, 3.3, 1), (4.1, 5.1, 1), (6.1, 6.9, 1), (6.9, 7.9, 0.35), (12.85, 14.2, 1.1)):
        i, j = int(a * SR), int(b * SR)
        gate[i:j] = lvl
    from scipy.ndimage import uniform_filter1d
    gate = uniform_filter1d(gate, int(0.012 * SR))
    mix += mus * gate * 0.9
    # Pip humming
    for a, b, sd in ((1.8, 3.3, 1), (4.1, 5.1, 2), (6.1, 9.0, 3)):
        put(hum(a, b, sd), a)
    # hops
    for k in range(3):
        put(pluck(mhz(76 + k * 2), 0.18, 0.22), k * 0.6 + 0.05)
        put(popsnd(0.18), k * 0.6 + 0.58)
    put(sweep(500, 380, 0.5, 0.12), 1.15)               # tongue lick (slurp-ish whistle)
    # tiptoe sneaks: pizzicato steps
    for a, b, base in ((2.4, 3.25, 60), (4.3, 5.05, 64)):
        for s in range(4):
            put(pluck(mhz(base + [0, 3, 5, 7][s]), 0.25, 0.3), a + s * (b - a) / 4)
    for at in (3.3, 5.1):                                # freeze sting
        put(lib("tick"), at, 0.9)
        put(pluck(mhz(48), 0.3, 0.3), at)
    put(sweep(300, 900, 0.35, 0.15), 5.3)               # Pip squints at the tail
    put(lib("whoosh"), 6.28, 0.9)                        # zoom closer
    put(noise_burst(0.3, 0.12, 200, 2000), 6.5)          # skid
    put(lib("creak", 1.2), 6.95, 0.7)                    # jaw opens
    put(sweep(110, 160, 1.0, 0.1, 3), 6.95)              # low tension
    put(lib("paper", 0.4), 8.05, 0.8)                    # envelope posted
    put(lib("thud"), 8.25, 1.0); put(popsnd(0.5), 8.25)  # CLACK
    put(boing(0.6, 0.45), 8.3)
    put(sweep(400, 1600, 0.35, 0.18), 8.32)              # slide whistle up (take)
    # insert: card opens, sweet chime
    put(lib("paper", 0.5), 9.15, 0.8)
    for k, m in enumerate((72, 76, 79, 84, 88)):
        put(bell(mhz(m), 1.4, 0.16), 9.6 + k * 0.16)
    for k, m in enumerate((60, 64, 67)):
        put(marimba(mhz(m), 1.5, 0.12), 10.4 + k * 0.02)
    put(sweep(700, 520, 0.5, 0.08, 9), 10.6)              # little "aww" sniff
    # reveal
    put(popsnd(0.6), 11.75); put(boing(0.5, 0.35), 11.78)
    put(sweep(500, 1500, 0.3, 0.12), 11.78)
    put(popsnd(0.4), 12.4); put(bell(mhz(96), 0.6, 0.1), 12.42)   # candle lights
    put(party_horn(0.7, 0.35), 12.8); put(lib("crowd_cheer", 1.4), 12.85, 0.25)
    put(noise_burst(0.9, 0.12, 300, 3000, "rise", 5), 13.35)        # inhale
    put(lib("wind", 0.7), 14.28, 0.8); put(lib("whoosh"), 14.28, 0.9)   # blow
    put(noise_burst(0.25, 0.25, 500, 5000, seed=9), 14.32); put(boing(0.4, 0.25), 14.33)  # poof
    put(lib("ding"), 14.92, 0.9)                         # deadpan look to camera
    put(sweep(900, 300, 0.25, 0.12), 15.95)              # lunge
    put(lib("gulp"), 16.2, 1.0)
    put(bell(mhz(100), 0.3, 0.12), 16.5)                 # eye twitch "tink"
    # end card ta-da
    for k, m in enumerate((72, 76, 79, 84)):
        put(marimba(mhz(m), 1.2, 0.16), END_STORY + 0.05 + k * 0.07)
    put(pluck(mhz(48), 0.8, 0.3), END_STORY + 0.26)
    mix = np.tanh(mix * 1.2) / 1.2
    mix /= np.abs(mix).max() + 1e-9
    st = np.stack([mix, mix], 1).astype(np.float32) * 0.9
    import soundfile as sf
    sf.write(str(path), st, SR)


def main():
    OUT.mkdir(exist_ok=True)
    if "--still" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--still") + 1].split(",")]
        ims = [Image.frombytes("RGB", (W, H), frame(int(t * FPS))) for t in ts]
        cols = 6; rows = math.ceil(len(ims) / cols); tw, th = 270, 480
        sheet = Image.new("RGB", (cols * tw, rows * th), "white")
        for k, im in enumerate(ims):
            sheet.paste(im.resize((tw, th)), ((k % cols) * tw, (k // cols) * th))
            ImageDraw.Draw(sheet).text(((k % cols) * tw + 6, (k // cols) * th + 6), f"{ts[k]:.2f}", fill="black")
        sheet.save(OUT / "contact.png")
        return
    wav = OUT / "sample_audio.wav"
    build_audio(wav)
    nfr = int(END * FPS)
    silent = OUT / "video_silent.mp4"
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", str(silent)],
                          stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for k, fr in enumerate(pool.imap(frame, range(nfr), chunksize=4)):
            ff.stdin.write(fr)
            if k % 48 == 0:
                print("frame", k, "/", nfr, flush=True)
    ff.stdin.close(); ff.wait()
    final = OUT / "sample_mailbox.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(silent), "-i", str(wav), "-c:v", "copy",
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest",
                    "-movflags", "+faststart", str(final)], check=True)
    print("done", final)


if __name__ == "__main__":
    main()
