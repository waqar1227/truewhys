"""B-009 cut Short C1 "mask first", re-composed vertically (1080x1920) with its own hook and script (not a crop of L9):
frame-1 rule (masks already dropping + hiss at 0.0 s, shocked face + <= 4-word question), answer at the end, last shot loops to the first.
python episodes/B-009-flight-secrets/shorts/make_short.py C1 sheet|qa|times <t,..> <out>|render
"""
import sys, math
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_fx import arrow, burst, sparkles, qmark
from flat_flight import *
import sfxgen  # noqa

SID = sys.argv[1] if len(sys.argv) > 1 else "C1"
DIRS = {"C1": "C1-mask-first"}
EP = HERE / DIRS[SID]
S2 = (300, 790)            # two seats in the vertical frame
OY = 520                   # the 16:9 seat-row layout is moved down this much
FEET = 1150


def tw(c, word, n=0, frac=0.5):
    try:
        return c.w(word, n)
    except Exception:
        return c.T * frac


def on(c, word, d=0.35, n=0, frac=0.5):
    return ease_out(seg(c.t, tw(c, word, n, frac), d))


def pk(c, word, n=0, frac=0.5):
    return pop(c.t, tw(c, word, n, frac) - 0.1, 0.3)


def label(g, txt, x, y, size=96, col=None, k=1.0, rot=-0.03):
    if k <= 0: return
    with g.screen():
        g.text(txt, x, y, size, col or PAL["yellow"], sw=size * 0.2, depth=size * 0.08, sc=k, rot=rot)


def tag(g, txt, x, y, k=1.0, size=56):
    if k <= 0: return
    with g.screen():
        with g.at(x, y, -0.02, back_out(clamp(k), 1.6)):
            w = g.text_w(txt, size) + 50
            g.rc(0, 0, w, size * 1.6, PAL["navy"], PAL["cream"], lw=5, r=16)
            g.text(txt, 0, 3, size, PAL["cream"], stroke=None)


def studio(g, t, a="#8C2E2E", b="#2A0B0B"):
    g.fill_all(g.rgrad(W / 2, H * 0.45, H * 0.75, a, shade(a, 0.5), b))
    for i in range(14):
        a0 = i * TAU / 14 + t * 0.05
        g.poly([(W / 2, H * 0.45), (W / 2 + 2600 * math.cos(a0), H * 0.45 + 2600 * math.sin(a0)),
                (W / 2 + 2600 * math.cos(a0 + 0.1), H * 0.45 + 2600 * math.sin(a0 + 0.1))], "#FFFFFF", None, a=0.05)


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


import cairocffi as _cairo
_EPD = HERE.parent
PL_DIR = _EPD / "renders" / "plates" if (_EPD / "renders" / "plates" / "v_row_day_bg.png").exists() else _EPD / "plates_lo"
_PL = {}


def plate(g, key, a=1.0):
    if key not in _PL:
        _PL[key] = _cairo.ImageSurface.create_from_png(str(PL_DIR / f"{key}.png"))
    im = _PL[key]; k = W / im.get_width()
    c = g.c; c.save(); c.scale(k, k); c.set_source_surface(im, 0, 0); c.get_source().set_filter(_cairo.FILTER_GOOD)
    c.paint_with_alpha(a) if a < 1 else c.paint(); c.restore()


VX = {"kai": 790, "nia": 400}
VF = 1800


def vrow(g, c, kai="deadpan", nia="deadpan", panel=2.0, mask=(0.0, 0.0), kai_pose=("down", "hold"), kai_view=None, haze=None):
    """Vertical row on the 3D cabin plate: Kai at the window (right), Nia middle; masks drop from the bins; FG = seat backs in front."""
    plate(g, "v_row_day_bg")
    mask_panel(g, 800, 520, panel, c.gt, n=2, gap=430, s=1.0)
    kf = True if kai_view == "3q" else False
    char2(g, "kai", VX["kai"], VF, 1150, kai, kai_pose[0], kai_pose[1], t=c.gt, view=kai_view, flip=not kf if kai_view == "3q" else False)
    char2(g, "nia", VX["nia"], VF, 1000, nia, "down", "hold", t=c.gt)
    mask_on(g, VX["kai"], VF, 1150, mask[0])
    mask_on(g, VX["nia"], VF, 1000, mask[1])
    plate(g, "v_row_day_fg")
    if haze:
        with g.screen():
            g.rect(-50, -50, W + 100, H + 100, haze[0], None, a=haze[1])


def c_hook(g, c, end=False):
    k = clamp(0.45 + c.t / 0.8)
    vrow(g, c, "shocked", "shocked", panel=k)
    burst(g, 760, 660, 60, 140, 10, PAL["yellow"], 8, k=clamp(1 - c.t / 0.6))


def c_clock(g, c):
    studio(g, c.gt)
    frac = 1 - clamp((c.t - 0.2) / 2.5) * 0.85
    tuc_clock(g, 540, 900, 330, frac, clamp(c.t / 0.3), "30 s")
    tag(g, "35,000 ft", 540, 360, 1.0, 64)


def c_first(g, c, phase=0):
    km = 1.0 if phase else on(c, "mask", 0.8)
    kh = 0.0
    vrow(g, c, "deadpan", "shocked", mask=(km, kh),
         kai_pose=pose_at(c.t, [(0, ("down", "hold")), (0.3, ("up", "up"))]) if not phase else ("down", "reach_r"), kai_view="3q" if phase else None)
    tag(g, "1", 120, 820, km, 64)
    if phase:
        tag(g, "2", 960, 820, pk(c, "child's"), 64)


def c_thin(g, c, phase=0):
    if phase == 0:
        plate(g, "v_sky_clouds")
        label(g, "THIN AIR", 540, 380, 110, PAL["cream"], k=pk(c, "thin"))
    elif phase == 1:
        vrow(g, c, "deadpan", "deadpan", panel=2.0)
        cross(g, 860, 360, 70, pk(c, "feel"))
        label(g, "NO WARNING", 540, 230, 90, PAL["cream"], k=pk(c, "feel"))
    else:
        vrow(g, c, "smile", "smile", panel=2.0, haze=("#FFF4E0", 0.18))
        sparkles(g, c.gt, [(260, OY + 280), (820, OY + 300), (540, OY + 150)], col=PAL["yellow"], r=30)
        label(g, "CALM?!", 540, 230, 110, k=pk(c, "calm"))


def c_fumble(g, c):
    vrow(g, c, "bored", "bored", panel=2.0, kai_view="3q", kai_pose=("down", ("reach_r", "hold", 0.5 + 0.5 * math.sin(c.gt * 5))),
         haze=("#2A1C3E", 0.2 * on(c, "pass", 0.6)))
    tuc_clock(g, 860, 300, 120, 0.12, 1.0, "")
    cross(g, 540, 300, 80, pk(c, "pass"))


def c_good(g, c):
    kh = on(c, "help", 0.8)
    vrow(g, c, "smile", "smile" if kh > 0.5 else "deadpan", panel=2.0, mask=(1.0, kh), kai_view="3q", kai_pose=("down", "reach_r"))
    check(g, 540, 300, 90, pk(c, "need"))


def c_dive(g, c):
    studio(g, c.gt, "#2E5A8C", "#0B1730")
    alt_chart(g, 90, 520, 900, 900, clamp(on(c, "dive", 2.2)), c.gt)
    label(g, "THICKER AIR", 540, 1600, 90, k=pk(c, "thicker"))


def c_end(g, c):
    """Last shot matches frame 1 so the Short loops."""
    c_hook(g, c, end=True)
    label(g, "30 SECONDS", 540, 1780, 110, k=pk(c, "Thirty"))


def build():
    V = Video(EP, title=("30", "SECONDS?"), cap_y=0.72, music="tense", sid="B009C1", captions=False, amb="amb_plane_cabin")
    V.shot("H1", c_hook, (0, "you"), tr="cut", sfx=[(0.0, "hiss", 0.5), (0.0, "seatbelt_chime", 0.35)])
    V.shot("H1", c_clock, ("you", 1), cam=push(1.0, 1.05, (540, 900)), sfx=[("thirty", "tick", 0.4)])
    V.shot("L01", c_first, (0, "Even"), cam=push(1.0, 1.05, (500, 1000)), sfx=[("mask", "seatbelt_click", 0.35)])
    V.shot("L01", lambda g, c: c_first(g, c, 1), ("Even", 1), cam=push(1.0, 1.04, (600, 1000)), sfx=[])
    V.shot("L02", c_thin, (0, "And"), cam=push(1.0, 1.05, (540, 900)), music="mystery", sfx=[("thin", "wind", 0.3)])
    V.shot("L02", lambda g, c: c_thin(g, c, 1), ("And", "You"), cam=push(1.0, 1.04, (540, 1000)), sfx=[])
    V.shot("L02", lambda g, c: c_thin(g, c, 2), ("You", 1), cam=push(1.03, 1.08, (540, 1000)), sfx=[])
    V.shot("L03", c_fumble, cam=push(1.0, 1.05, (560, 1000)), music="tension", sfx=[("fumble", "seatbelt_click", 0.3), ("pass", "drum_hit", 0.35)])
    V.shot("L04", c_good, cam=push(1.0, 1.05, (560, 1000)), music="warm", sfx=[("help", "seatbelt_click", 0.3)])
    V.shot("L05", c_dive, (0, "Thirty"), cam=push(1.0, 1.04, (540, 960)), sfx=[("dive", "jet_hum", 0.35)])
    V.shot("L05", c_end, ("Thirty", 1), cam=push(1.0, 1.04, (540, 1000)), music="tension", sfx=[(0.05, "hiss", 0.3)])
    V.title_y = 0.1
    V.build()
    from flat_split import split_long
    split_long(V, maxd=2.5, keep_cam=True)
    return V


if __name__ == "__main__":
    V = build()
    cmd = sys.argv[2] if len(sys.argv) > 2 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=8, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers()
    elif cmd == "times":
        V.qa_numbers()
        print(V.sheet(sys.argv[4], times=[float(x) for x in sys.argv[3].split(",")], cols=6, scale=0.2))
    elif cmd == "render":
        (EP / "final").mkdir(exist_ok=True)
        V.render(str(EP / f"final/B-009-{SID}.mp4"))
