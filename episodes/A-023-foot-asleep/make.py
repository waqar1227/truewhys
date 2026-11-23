"""A-023 "Why Does Your Foot Fall Asleep?" — standalone Short, Style F + cast v2.2 (Runner). Slot Fri 18 Dec 2026 18:00 UTC.
python episodes/A-023-foot-asleep/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: a beanbag living room, an x-ray leg with a glowing nerve and blood vessels, a pressure block,
signal dots, a cartoon brain, crackling 'static' sparks. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2
from flat_fx import room, bolt, pain_marks, sparkles, burst, no_sign, arrow
from flat_split import split_long

V = Video(EP, title=("WHY'S MY FOOT", "ASLEEP?"), music="playful")
V.title_y = 0.13                                                               # title above her head (frame 1 face stays clear)
NERVE, VESSEL, SKIN, XR = "#FFC93C", "#FF5B6B", "#F1CDB0", "#BDEBFF"
WHO = "runner"


# ------------------------------------------------------------------ sets
def lounge(g, t):
    room(g, wall=("#2F2A5A", "#40367A"), floor=("#7A4E3A", "#4E3024"), fy=1500, tile=(180, 180))
    g.glow(820, 560, 520, "#FFC93C", 0.10)
    g.rc(830, 640, 280, 360, "#4E66B0", INK, lw=8, r=10)                         # window
    g.line([(830, 460), (830, 820)], INK, 8); g.line([(690, 640), (970, 640)], INK, 8)
    g.ellipse(250, 1610, 230, 120, "#FF8A3D", INK, lw=10)                        # beanbag she sat on
    g.ellipse(250, 1560, 170, 60, shade("#FF8A3D", 1.12), None, a=0.6)
    g.rc(900, 1560, 230, 26, "#2A2A38", INK, lw=6, r=8)                          # low table + phone
    g.rc(900, 1520, 90, 50, "#15151F", INK, lw=5, r=8)


def xray_bg(g, t):
    g.fill_all(g.rgrad(W / 2, H * 0.52, H * 0.8, "#173A5C", "#0E2235", "#06121F"))
    with g.layer(0.25):
        for i in range(0, W + 1, 90):
            g.line([(i, 0), (i, H)], "#2D5A84", 2)
        for j in range(0, H + 1, 90):
            g.line([(0, j), (W, j)], "#2D5A84", 2)


# leg drawn diagonally down the tall frame: hip top-left, knee right of centre, foot bottom-right (design units)
KNEE = (600, 860)
THIGH = [(300, -40), (420, 420), KNEE]
SHIN = [KNEE, (560, 1240), (520, 1560)]
FOOTL = [(520, 1560), (560, 1680), (660, 1730), (860, 1760)]


def _dense(pts, step=14):
    out = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        n = max(1, int(math.dist(a, b) / step))
        out += [(lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)) for i in range(1, n + 1)]
    return out


def leg(g, squeeze=0.0, glow=1.0, numb=0.0, vessels=1.0, block=True, label=None):
    """X-ray leg: translucent skin, bone, yellow nerve + red vessels pinched at the knee by `squeeze` 0..1."""
    th, sh, ft = _dense(THIGH), _dense(SHIN), _dense(FOOTL)
    for w, col, a in ((352, XR, 0.5), (338, SKIN, 0.22)):
        g.line(th, col, w, a=a); g.line(sh, col, w * 0.74, a=a); g.line(ft, col, w * 0.5, a=a)
    g.line([(x - 22, y) for x, y in th[3:-3]], "#E6E1F0", 46, a=0.35)               # bones (soft)
    g.line([(x - 18, y) for x, y in sh[3:-3]], "#E6E1F0", 34, a=0.35)
    g.circle(KNEE[0] - 20, KNEE[1], 48, "#E6E1F0", None, a=0.3)

    def pinch(p):                                                                # 1 at the knee, 0 away from it
        return clamp(1 - math.dist(p, KNEE) / 170) ** 1.5 * squeeze
    full = th + sh[1:] + ft[1:]
    if vessels > 0:
        for off, ph in ((-58, 0.0), (60, 1.7)):
            vp = []
            for i, p in enumerate(full):
                q = full[min(i + 1, len(full) - 1)] if i < len(full) - 1 else p
                pp = full[i - 1] if i else p
                dx, dy = q[0] - pp[0], q[1] - pp[1]; L = math.hypot(dx, dy) or 1
                nx, ny = -dy / L, dx / L
                o = off * (1 - 0.8 * pinch(p)) * (0.55 if i > len(th) + len(sh) else 1) + 7 * math.sin(i * 0.25 + ph)
                vp.append((p[0] + nx * o, p[1] + ny * o))
            g.line(vp, VESSEL, 13 * vessels, a=0.85 * (1 - 0.5 * numb))
    col = mix(NERVE, "#8A8A9A", numb)
    if glow > 0:
        g.line(full, col, 80, a=0.12 * glow)
    for a_, b_ in zip(full, full[1:]):
        w = 28 * (1 - 0.75 * pinch(((a_[0] + b_[0]) / 2, (a_[1] + b_[1]) / 2)))
        g.line([a_, b_], col, w, cap="round")
    if block and squeeze > 0:
        bx = lerp(1300, KNEE[0] + 300, ease_out(clamp(squeeze * 1.3)))
        g.rc(bx, KNEE[1], 340, 330, SKIN, INK, lw=10, r=130)                      # the other leg pressing from the side
        g.text("PRESSURE", min(bx, 760), KNEE[1] - 250, 72, PAL["cream"], sw=12, a=clamp(squeeze * 2))
        arrow(g, min(bx, 760) + 60, KNEE[1] - 170, min(bx, 760) - 90, KNEE[1] - 170, PAL["yellow"], w=20, k=clamp(squeeze * 2))
    return full


def nerve_pt(full, u):
    """Point at fraction u along the nerve from the FOOT (u=0) to the hip (u=1)."""
    pts = full[::-1]
    L = [0.0]
    for a, b in zip(pts, pts[1:]):
        L.append(L[-1] + math.dist(a, b))
    s = u * L[-1]
    for i in range(1, len(L)):
        if L[i] >= s:
            k = (s - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            return (lerp(pts[i - 1][0], pts[i][0], k), lerp(pts[i - 1][1], pts[i][1], k))
    return pts[-1]


def signals(g, full, t, blocked=0.0, n=6, speed=0.55):
    """Signal dots running from the foot up the nerve; with `blocked` they die at the knee."""
    stop = 0.50                                                                    # knee position along the nerve (from the foot)
    for i in range(n):
        u = (t * speed + i / n) % 1.0
        a = 1.0
        if blocked > 0 and u > stop:
            a = clamp(1 - (u - stop) * 12) * blocked + (1 - blocked)
        x, y = nerve_pt(full, u)
        g.glow(x, y, 60, "#FFF4E0", 0.5 * a)
        g.circle(x, y, 15, "#FFF4E0", INK, lw=4, a=a)


def static(g, full, gt, k=1.0, u0=0.0, u1=0.45, n=10):
    """Crackling 'pins and needles' sparks flickering along the lower nerve."""
    fi = int(gt * 15)
    for i in range(n):
        r = rnd(fi * 31 + i).random
        u = lerp(u0, u1, r())
        x, y = nerve_pt(full, u)
        bolt(g, x + (r() - 0.5) * 120, y + (r() - 0.5) * 110, (0.7 + r() * 0.6) * k, (r() - 0.5) * 1.8, PAL["yellow"])
        g.glow(x, y, 90, "#FFF4E0", 0.25 * k)


def cartoon_foot(g, x, y, s, numb=0.0, zz=0.0):
    with g.at(x, y, 0, s):
        col = mix(SKIN, "#B8B8C8", numb)
        g.path("M-60 -260 L60 -260 L70 -40 Q240 -20 300 40 Q320 100 250 110 L-70 110 Q-110 100 -100 40 Z", col, INK, lw=10)
        for i, tx in enumerate((210, 245, 272, 290)):
            g.circle(tx, 70 - i * 6, 22 - i * 3, shade(col, 1.04), INK, lw=5)
        if zz > 0:
            for i in range(3):
                k = clamp(zz * 3 - i)
                g.text("Z", 40 + i * 70, -330 - i * 80, 70 + i * 20, PAL["cream"], sw=10, a=k)


def brain(g, x, y, s, k=1.0, dots=0.0):
    with g.at(x, y, 0, s * back_out(clamp(k), 1.6)):
        g.ellipse(0, 0, 210, 150, "#FF9FB0", INK, lw=10)
        g.line([(0, -140), (0, 140)], INK, 8)
        for sx in (-1, 1):
            g.path(f"M{sx*40} -90 Q{sx*120} -110 {sx*150} -40 Q{sx*90} -20 {sx*120} 40 Q{sx*70} 70 {sx*110} 110", None, shade("#FF9FB0", 0.7), lw=8)
        if dots > 0:
            for i in range(3):
                g.circle(260 + i * 60, -120 - i * 30, 14 + i * 6, "#FFFFFF", INK, lw=5, a=clamp(dots * 3 - i))


# ------------------------------------------------------------------ shots
def runner_wobble(g, c, title_hold=True):
    lounge(g, c.gt)
    x = 560 + 18 * math.sin(c.gt * 7)
    rot = 0.08 * math.sin(c.gt * 9)
    char2(g, WHO, x, 2240, 1000, "shocked", "up", "shrug", t=c.gt, rot=rot)
    fx, fy = x - 50, 2228                                                          # her left foot (screen left)
    pain_marks(g, fx, fy - 40, 120, c.gt, n=5, col=PAL["yellow"], a0=-3.3, a1=0.2)
    fi = int(c.gt * 15)
    for i in range(5):
        r = rnd(fi * 7 + i).random
        bolt(g, fx + (r() - 0.5) * 220, fy - 60 + (r() - 0.5) * 120, 0.9 + r() * 0.5, (r() - 0.5) * 1.6, PAL["yellow"])


def s_hook(g, c):
    """Frame 1: the Runner just got up off the beanbag, her foot dead: wobbling, sparks crackling at the foot."""
    runner_wobble(g, c)


def s_not_asleep(g, c):
    xray_bg(g, c.gt)
    cartoon_foot(g, 420, 1250, 1.6, zz=clamp(c.t / 0.6))
    no_sign(g, 640, 800, 230, k=c.on("asleep", 0.3))


def s_squashed(g, c):
    xray_bg(g, c.gt)
    sq = c.on("squashed", 0.35)
    full = leg(g, squeeze=sq, glow=1.0 + 0.6 * pulse(c.t, c.w("nerve"), 0.5))
    with g.screen():
        g.text("NERVE", 250, 1250, 92, NERVE, sw=14, sc=pop(c.t, c.w("nerve") - 0.15, 0.3))


def s_sit_cross(g, c):
    """'When you sit on your foot or cross your legs': two big panels pop in on their words."""
    g.fill_all(g.lgrad(0, 0, 0, H, "#2F2A5A", "#1B1838"))
    k1, k2 = c.on("sit", 0.35), c.on("cross", 0.35)
    with g.at(540, 560, 0, back_out(k1, 1.6)):                                     # a foot squashed under a heavy cushion
        g.rc(0, 0, 960, 720, "#40367A", INK, lw=10, r=40)
        g.rc(0, 290, 880, 60, "#7A4E3A", INK, lw=8, r=14)
        cartoon_foot(g, -120, 250, 0.62)
        sq = 0.08 * math.sin(c.gt * 6)
        g.ellipse(20, 40, 330, 150 * (1 - sq), "#FF8A3D", INK, lw=10)               # beanbag pressing down
        g.ellipse(20, -10, 230, 50, shade("#FF8A3D", 1.12), None, a=0.6)
        arrow(g, 20, -250, 20, -140, PAL["yellow"], w=20)
        pain_marks(g, -150, 200, 130, c.gt, n=4, col=PAL["yellow"], a0=-3.0, a1=-1.6, sc=0.9)
        g.text("SITTING ON IT", 0, -300, 76, PAL["cream"], sw=12)
    with g.at(540, 1380, 0, back_out(k2, 1.6)):                                    # crossed legs (front view)
        g.rc(0, 0, 960, 720, "#40367A", INK, lw=10, r=40)
        for (x0, y0, x1, y1, col) in ((-330, -180, 300, 250, "#24476B"), (330, -190, -280, 240, "#2E5A8A")):
            g.line([(x0, y0), (x1, y1)], INK, 166); g.line([(x0, y0), (x1, y1)], col, 150)
        g.glow(5, 20, 140, NERVE, 0.35 + 0.2 * math.sin(c.gt * 8))
        g.circle(5, 20, 42, NERVE, INK, lw=7)
        g.text("CROSSED LEGS", 0, -300, 76, PAL["cream"], sw=12)


def s_vessels(g, c):
    xray_bg(g, c.gt)
    full = leg(g, squeeze=1.0, vessels=0.4 + 0.6 * c.on("blood", 0.3))
    with g.screen():
        g.text("NERVE", 250, 1250, 88, NERVE, sw=14)
        g.text("BLOOD", 250, 1380, 88, VESSEL, sw=14, sc=pop(c.t, c.w("blood") - 0.15, 0.3))


def s_blocked(g, c):
    xray_bg(g, c.gt)
    full = leg(g, squeeze=1.0)
    signals(g, full, c.t, blocked=1.0, n=5, speed=0.6)
    kx = c.on("messages", 0.3)
    if kx > 0:
        with g.at(KNEE[0], KNEE[1], 0, back_out(kx, 2.0)):
            g.line([(-60, -60), (60, 60)], "#FF3B30", 22); g.line([(-60, 60), (60, -60)], "#FF3B30", 22)
    with g.screen():
        g.text("SIGNAL BLOCKED", W / 2, 520, 96, PAL["cream"], sw=16, depth=8, sc=pop(c.t, c.w("messages") - 0.1, 0.3))


def s_numb(g, c):
    lounge(g, c.gt)
    char2(g, WHO, 380, 2350, 1500, "bored" if c.t < c.w("numb") - 0.3 else "worried", "down", "hold", t=c.gt)
    brain(g, 780, 600, 0.95, k=c.on("brain", 0.3), dots=clamp(c.since("hearing") / 0.9))
    cartoon_foot(g, 790, 1520, 0.8, numb=c.on("numb", 0.5))
    with g.screen():
        g.text("NUMB", 790, 1170, 110, "#C9CED6", sw=16, depth=8, sc=pop(c.t, c.w("numb") - 0.15, 0.3))


def s_stand(g, c):
    lounge(g, c.gt)
    k = c.on("stand", 0.45)
    sq = 0.32 * (1 - k)
    char2(g, WHO, 540, 2240, 1060, "worried" if c.t < c.w("stand") + 0.4 else "suspicious", "down", "down", t=c.gt, squash=sq)


def s_restart(g, c):
    xray_bg(g, c.gt)
    rel = 1 - c.on("lifts", 0.35)
    full = leg(g, squeeze=rel, glow=1.0 + 0.8 * c.on("restarts", 0.3))
    if c.t > c.w("restarts") - 0.1:
        static(g, full, c.gt, k=c.on("restarts", 0.25), u0=0.0, u1=0.6, n=12)
        signals(g, full, c.t * 1.7, blocked=0.0, n=9, speed=0.9)
    burst(g, KNEE[0], KNEE[1], 120, 280, 12, PAL["yellow"], 12, k=seg(c.t, c.w("restarts") - 0.1, 0.35))
    with g.screen():
        g.text("MESSY SIGNALS", W / 2, 520, 96, PAL["cream"], sw=16, depth=8, sc=pop(c.t, c.w("messy") - 0.1, 0.3))


def s_static(g, c):
    xray_bg(g, c.gt)
    full = leg(g, squeeze=0.0, glow=1.6)
    static(g, full, c.gt, k=1.0, u0=0.0, u1=0.55, n=14)
    with g.screen():
        g.text("PINS & NEEDLES", W / 2, 520, 104, PAL["yellow"], sw=18, depth=10, sc=pop(c.t, c.w("pins") - 0.1, 0.3))


def s_loop(g, c):
    """Last shot = frame 1 (loop): the Runner wobbling on the waking foot."""
    runner_wobble(g, c)


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, cam=ZOOM(1.0, 1.06, (540, 1500)), sfx=[(0.0, "zap", 0.45), (0.05, "pop", 0.3)], tr="cut")
V.shot("L01", s_not_asleep, (0, "A"), cam=ZOOM(1.0, 1.05, (540, 1000)), sfx=[("asleep", "bloop", 0.35)])
V.shot("L01", s_squashed, ("A", 1), cam=ZOOM(1.0, 1.1, (520, 900)), sfx=[("squashed", "drum_hit", 0.45)])
V.shot("L02", s_sit_cross, (0, "you#1"), sfx=[("sit", "pop", 0.3), ("cross", "pop", 0.3)])
V.shot("L02", s_vessels, ("you#1", 1), cam=ZOOM(1.0, 1.08, (500, 900)), sfx=[("blood", "ding", 0.3)])
V.shot("L03", s_blocked, (0, "Your"), cam=ZOOM(1.0, 1.1, KNEE), sfx=[("messages", "alarm", 0.35)])
V.shot("L03", s_numb, ("Your", 1), sfx=[("numb", "confuse", 0.35)])
V.shot("L04", s_stand, (0, "The"), cam=ZOOM(1.0, 1.04, (540, 1300)), music="adventure", sfx=[("stand", "whoosh", 0.35)])
V.shot("L04", s_restart, ("The", 1), cam=ZOOM(1.0, 1.1, KNEE), sfx=[("restarts", "zap", 0.45), ("messy", "zap", 0.35)])
V.shot("L05", s_static, (0, "Your"), cam=ZOOM(1.05, 1.15, (560, 1300)), sfx=[(0.1, "zap", 0.3), ("pins", "sting", 0.35)])
V.shot("L05", s_loop, ("Your", 1), cam=ZOOM(1.0, 1.06, (540, 1500)), sfx=[(0.1, "zap", 0.3)])
V.build()
split_long(V)

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=6, scale=0.16))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-023.mp4"))
