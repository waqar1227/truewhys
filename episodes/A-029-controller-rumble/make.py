"""A-029 "Why Does Your Controller Shake?" — standalone Short, Style F + cast v2.2 (Student, night gaming look). Slot Sat 12 Dec 2026 18:00 UTC.
python episodes/A-029-controller-rumble/make.py sheet|qa|big <t,..>|render
Our own cast and drawings only: a living room at night lit by the TV, our own cartoon street race on the screen (two toy cars, no game
footage, no brand), a generic two-grip gamepad (plain buttons, no logos), its x-ray with the two rumble motors, a big end-on motor with its
off-centre weight, heavy-left / light-right, and the newer voice-coil actuator. Facts in sources.md.
"""
import sys, math
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
from flat2d import *
from cast2_flat import char2, pose_at
from flat_split import split_long
from flat_fx import burst, arrow, sparkles, pain_marks
from flat_winter import hand_pt
from flat_game import (game_room, tv, controller, hands_on, motor_face, coil_actuator, rumble_waves, MOTOR_L, MOTOR_R,
                       HEAVY, LIGHTW)

V = Video(EP, title=("WHY DOES IT", "SHAKE?"), music="match")
V.title_y = 0.075
WHO = "student"
SKIN, SLEEVE = "#F3D0B5", "#FFC93C"
PX, PY, PH = 700, 1900, 1050            # player feet + height (3/4 view, facing the TV on the left)
TVX, TVY, TVW, TVH = 520, 640, 860, 440


def pad_at():
    """Controller centre in the player's hands (between both 'hold' hands)."""
    a = hand_pt(WHO, "hold", PX, PY, PH, side=1, flip=True)
    b = hand_pt(WHO, "hold", PX, PY, PH, side=-1, flip=True)
    return ((a[0] + b[0]) / 2 - 10, (a[1] + b[1]) / 2 + 10)


def player(g, c, expr, shake=0.0, pl="hold", pr="hold"):
    R = rnd(int(c.gt * 30)).random
    jx = (R() - 0.5) * 8 * shake
    char2(g, WHO, PX + jx, PY, PH, expr, pl, pr, t=c.gt, flip=True, view="3q", prop=False)
    x, y = pad_at()
    controller(g, x + jx, y, 0.42, rot=0.18, shake=shake, t=c.gt)
    if shake > 0:
        rumble_waves(g, x, y, 150, 260, c.gt, k=shake, col="#FFFFFF", speed=2.4, w=8)


def living(g, c, crash, flash=0.0, tvshake=0.0):
    game_room(g, c.gt, glow=1.0, flash=flash)
    tv(g, TVX, TVY, TVW, TVH, c.gt, crash=crash, shake=tvshake)


def xbg(g, c, col="#0E2540"):
    """Dark blueprint backdrop for x-ray / motor close-ups."""
    g.fill_all(g.rgrad(540, 1000, 1200, "#1C3D63", col))
    for i in range(-2, 14):
        g.line([(i * 100, -200), (i * 100, H + 200)], "#2C5A84", 2, a=0.35)
    for j in range(-2, 24):
        g.line([(-200, j * 100), (W + 200, j * 100)], "#2C5A84", 2, a=0.35)


# ------------------------------------------------------------------ hook / loop framing
def s_hook(g, c):
    """Frame 1: the race on the TV is already crashing, the room flashes, the controller jolts in the player's hands, shocked face."""
    k = clamp(0.58 + c.t / 0.7)
    living(g, c, crash=k, flash=max(0, 1 - c.t / 0.5), tvshake=max(0, 1 - c.t / 0.8))
    player(g, c, "shocked", shake=1.0)
    pain_marks(g, PX - 40, PY - PH * 1.02, 120, c.gt, n=5, col="#FFFFFF", sc=0.8)


def s_hands(g, c):
    """Close on the hands: the controller kicks; rumble waves on 'shake'."""
    xbg(g, c, "#141B33")
    game_room(g, c.gt, glow=1.2)
    sh = 0.8 + 0.2 * math.sin(c.gt * 20)
    controller(g, 540, 1000, 1.25, shake=sh, t=c.gt)
    hands_on(g, 540, 1000, 1.25, SKIN, SLEEVE, shake=sh, t=c.gt)
    rumble_waves(g, 540, 1000, 470, 640, c.gt, k=1.0, col="#FFFFFF", speed=2.2, w=12)


# ------------------------------------------------------------------ L01: every hit, every crash
def s_tvhits(g, c):
    """TV close-up: the cars bump on 'hit', then crash big on 'crash'."""
    game_room(g, c.gt, glow=1.3, flash=0.6 * max(0, 1 - c.since("crash") / 0.4) if c.t >= c.w("crash") else 0)
    if c.t < c.w("crash"):
        kk = clamp(c.since("hit") / 0.5) if c.t >= c.w("hit") else 0
        cr = 0.62 * math.sin(math.pi * kk) if kk < 1 else 0.0
    else:
        cr = clamp(0.55 + c.since("crash") / 0.5)
    tv(g, 540, 900, 900, 560, c.gt, crash=cr, shake=1.0 if cr > 0.55 else 0.0)


def s_feel(g, c):
    """'you feel it in your hands': hands + controller, a jolt on 'feel' and on 'hands'."""
    game_room(g, c.gt, glow=1.2)
    k = max(pulse(c.t, c.w("feel"), 0.45), pulse(c.t, c.w("hands"), 0.45))
    controller(g, 540, 1040, 1.15, shake=0.15 + k, t=c.gt)
    hands_on(g, 540, 1040, 1.15, SKIN, SLEEVE, shake=0.15 + k, t=c.gt)
    rumble_waves(g, 540, 1040, 430, 600, c.gt, k=0.3 + 0.7 * k, col="#FFC93C", speed=2.0, w=11)


def s_reveal(g, c):
    """'...and it all comes from one lopsided weight': the shell fades to x-ray, both motors glow, the weights spin."""
    xbg(g, c)
    xr = c.on("comes", 0.6)
    sp = 14 * c.t * c.on("lopsided", 0.3)
    controller(g, 540, 1000, 1.35, shake=0.2 * c.on("lopsided", 0.3), t=c.gt, xray=xr, spin=sp, glow="both" if c.t >= c.w("one") else None)
    if c.t >= c.w("one") - 0.05:
        for (mx, my) in (MOTOR_L, MOTOR_R):
            x, y = 540 + mx * 1.35, 1000 + my * 1.35
            g.circle(x, y, 120 * back_out(c.on("one", 0.35), 1.6), None, PAL["yellow"], lw=9)
    with g.screen():
        g.text("?", 540, 520, 200, PAL["yellow"], sw=24, depth=10, sc=pop(c.t, c.w("lopsided") - 0.08, 0.3), a=c.on("lopsided", 0.2))


# ------------------------------------------------------------------ L02: motor + weight
def s_inside(g, c):
    xbg(g, c)
    controller(g, 540, 1000, 1.35, t=c.gt, xray=1.0, spin=0.0, glow="both")
    k = c.on("motor", 0.35)
    for (mx, my), sd in ((MOTOR_L, -1), (MOTOR_R, 1)):
        x, y = 540 + mx * 1.35, 1000 + my * 1.35
        arrow(g, x + sd * 10, 1560, x, y + 90, PAL["yellow"], w=26, k=c.on("handle", 0.3))
    with g.screen():
        g.text("MOTOR", W / 2, 1640, 130, PAL["yellow"], sw=18, depth=9, sc=pop(c.t, c.w("motor") - 0.08, 0.3), a=k)


def s_weight(g, c):
    """Big end-on motor: the half-moon weight on the shaft, red dot = its heavy side, a see-saw tips under 'heavier'."""
    xbg(g, c)
    hv = c.on("heavier", 0.4)
    motor_face(g, 540, 980, 300, 0.0 + 0.12 * math.sin(c.gt * 2), heavy=True, blur=0.0)
    g.glow(540, 980 - 300 * 0.82 * 0.42, 160, "#FF3B3B", 0.5 * hv * (0.7 + 0.3 * math.sin(c.gt * 10)))
    with g.screen():
        g.text("WEIGHT", W / 2, 470, 140, HEAVY, sw=19, depth=10, sc=pop(c.t, c.w("weight") - 0.08, 0.3), a=c.on("weight", 0.2))
        g.text("SHAFT", W / 2, 1520, 92, "#E9EEF4", sw=13, a=c.on("shaft", 0.25) * (1 - c.on("heavier", 0.3)))
        if hv > 0:
            arrow(g, 820, 1450, 620, 980 - 300 * 0.82 * 0.42 + 60, PAL["yellow"], w=22, k=hv)
            g.text("HEAVY SIDE", 800, 1520, 92, PAL["yellow"], sw=13, a=hv)


# ------------------------------------------------------------------ L03: spins + yanks
def s_spin(g, c):
    """'When it spins, that uneven weight...': the weight whirls with motion blur; the whole motor is dragged towards the weight."""
    xbg(g, c)
    sp = c.on("spins", 0.5)
    ang = 22 * (c.t - c.w("spins")) * sp if c.t > c.w("spins") else 0
    dx, dy = 26 * math.sin(ang) * sp, -26 * math.cos(ang) * sp
    motor_face(g, 540 + dx, 980 + dy, 300, ang, heavy=True, blur=sp)
    rumble_waves(g, 540, 980, 380, 520, c.gt, k=sp, col="#FFC93C", speed=2.6, w=12)


def s_yank(g, c):
    """'yanks the controller back and forth': the solid pad swings left/right; big arrows alternate with the swing."""
    xbg(g, c, "#141B33")
    ph = math.sin(c.gt * 16)
    k = c.on("yanks", 0.2)
    controller(g, 540 + 70 * ph * k, 1000, 1.25, rot=0.06 * ph * k, t=c.gt)
    rumble_waves(g, 540 + 70 * ph * k, 1000, 430, 560, c.gt, k=k, col="#FFC93C", speed=2.6, w=11)
    for sd in (-1, 1):
        on = (ph * sd > 0)
        arrow(g, 540 + sd * 250, 1460, 540 + sd * 430, 1460, PAL["yellow"] if on else "#5A6A8A", w=36, k=c.on("back", 0.3), a=1 if on else 0.5)
    with g.screen():
        g.text("BACK", 340, 1600, 100, "#FFFFFF", sw=14, a=c.on("back", 0.25))
        g.text("FORTH", 740, 1600, 100, "#FFFFFF", sw=14, a=c.on("forth", 0.25))


def s_dozens(g, c):
    """'dozens of times a second': a one-second clock sweeps while a spin counter climbs to 30 (rumble motors run about 15-45 turns a second)."""
    xbg(g, c)
    u = clamp(c.since("dozens") / 1.4)
    motor_face(g, 540, 900, 230, c.gt * 30, heavy=True, blur=1.0)
    n = int(round(30 * ease_out(u)))
    with g.screen():
        g.circle(540, 1430, 120, "#1B2238", INK, lw=10)
        g.poly([(540, 1430)] + [(540 + 110 * math.sin(TAU * u * q / 30), 1430 - 110 * math.cos(TAU * u * q / 30)) for q in range(31)],
               "#5ED3B5", None, a=0.8)
        g.line([(540, 1430), (540 + 100 * math.sin(TAU * u), 1430 - 100 * math.cos(TAU * u))], "#FFFFFF", 10)
        g.text("1 SEC", 540, 1620, 80, "#E9EEF4", sw=12)
        g.text(f"{n} SPINS", 540, 450, 130, PAL["yellow"], sw=18, depth=9, sc=pop(c.t, c.w("dozens") - 0.08, 0.3))


# ------------------------------------------------------------------ L04: heavy left / light right
def s_heavy(g, c):
    xbg(g, c)
    k = c.on("heavy", 0.35)
    S = 2.1; x, y = 520, 1060
    controller(g, x - MOTOR_L[0] * S, y - MOTOR_L[1] * S, S, t=c.gt, xray=1.0, spin=c.gt * 9, glow="l" if k > 0 else None, shake=0.25 * k)
    rumble_waves(g, x, y, 260, 460, c.gt * 0.6, k=c.on("deep", 0.3), col=HEAVY, speed=1.0, w=14, deep=True)
    with g.screen():
        g.text("HEAVY", W / 2, 560, 140, HEAVY, sw=19, depth=10, sc=pop(c.t, c.w("heavy") - 0.08, 0.3), a=k)
        g.text("RUMBLE", W / 2, 1600, 100, "#FFFFFF", sw=14, a=c.on("rumbles", 0.25))


def s_light(g, c):
    xbg(g, c)
    k = c.on("light", 0.35)
    S = 2.1; x, y = 560, 1060
    controller(g, x - MOTOR_R[0] * S, y - MOTOR_R[1] * S, S, t=c.gt, xray=1.0, spin=c.gt * 26, glow="r" if k > 0 else None, shake=0.12 * k)
    rumble_waves(g, x, y, 170, 300, c.gt * 1.8, k=c.on("quick", 0.3), col=LIGHTW, speed=3.0, w=7, n=5)
    with g.screen():
        g.text("LIGHT", W / 2, 560, 140, LIGHTW, sw=19, depth=10, sc=pop(c.t, c.w("light") - 0.08, 0.3), a=k)
        g.text("BUZZ", W / 2, 1600, 100, "#FFFFFF", sw=14, a=c.on("buzzes", 0.25))


# ------------------------------------------------------------------ L05: newer coils + loop
def s_coil(g, c):
    """'Newer controllers add magnet coils for tiny taps': inside a faded pad grip, a coil actuator; the magnet taps fast; tap ripples."""
    xbg(g, c, "#1A1530")
    tap = math.sin(c.gt * 30) * c.on("taps", 0.3) + 0.35 * math.sin(c.gt * 7) * (1 - c.on("taps", 0.3))
    coil_actuator(g, 540, 1000, 1.45 + 0.03 * abs(tap), c.gt, tap=tap)
    kt = c.on("taps", 0.2)
    for i in range(3):
        u = (c.gt * 3 + i / 3) % 1
        for sd in (-1, 1):
            g.path(f"M{540 + sd * (420 + 90 * u)} {940 - 40 * u} Q{540 + sd * (460 + 90 * u)} 1000 {540 + sd * (420 + 90 * u)} {1060 + 40 * u}",
                   None, "#FFC93C", lw=10, a=kt * (1 - u))
    with g.screen():
        g.text("COIL", W / 2, 560, 140, "#FF9E5E", sw=19, depth=10, sc=pop(c.t, c.w("coils") - 0.08, 0.3), a=c.on("coils", 0.2))
        g.text("TAP TAP", W / 2, 1460, 110, "#FFC93C", sw=16, depth=8, sc=pop(c.t, c.w("taps") - 0.08, 0.3), a=kt)
        g.text("NEWER", W / 2, 360, 92, "#E9EEF4", sw=13, a=c.on("Newer", 0.25) * (1 - c.on("coils", 0.3)))


def s_loop(g, c):
    """'...but that crash you just felt?' Back to the frame-1 framing: the race crashes again, the pad jolts."""
    k = clamp(0.5 + c.since("crash") / 0.5) if c.t >= c.w("crash") - 0.1 else 0.0
    living(g, c, crash=k, flash=0.8 * max(0, 1 - c.since("crash") / 0.4) if k > 0 else 0, tvshake=1.0 if k > 0.55 else 0)
    player(g, c, "shocked" if k > 0.5 else "curious", shake=0.9 if k > 0.55 else 0.0)


def s_end(g, c):
    """'A spinning weight.' Same framing; x-ray flashes over the pad in his hands, he grins."""
    living(g, c, crash=1.0, tvshake=0.0)
    player(g, c, "smug", shake=0.5)
    x, y = pad_at()
    k = c.on("spinning", 0.3)
    if k > 0:
        controller(g, x, y, 0.42, rot=0.18, t=c.gt, xray=k, spin=c.gt * 20, glow="both")


ZOOM = lambda z0, z1, f: push(z0, z1, focus=f)
V.shot("H1", s_hook, (0, "shake"), cam=ZOOM(1.0, 1.04, (540, 1020)), sfx=[(0.0, "crash", 0.7), (0.0, "rumble", 0.55), (0.02, "sting", 0.3)], tr="cut")
V.shot("H1", s_hands, ("shake", 1), cam=ZOOM(1.0, 1.06, (540, 1000)), tr="cut", sfx=[(0.0, "rumble", 0.5)])
V.shot("L01", s_tvhits, (0, "you"), cam=ZOOM(1.0, 1.08, (540, 900)), sfx=[("hit", "thud", 0.5), ("crash", "crash", 0.6)])
V.shot("L01", s_feel, ("you", "and"), cam=ZOOM(1.05, 1.12, (540, 1040)), tr="cut", sfx=[("feel", "rumble", 0.5), ("hands", "rumble", 0.45)])
V.shot("L01", s_reveal, ("and", 1), cam=ZOOM(1.0, 1.08, (540, 1000)), tr="cut", sfx=[("comes", "shimmer", 0.3), ("lopsided", "whir", 0.35)])
V.shot("L02", s_inside, (0, "On"), cam=ZOOM(1.0, 1.05, (540, 1080)), sfx=[("motor", "pop", 0.35)])
V.shot("L02", s_weight, ("On", 1), cam=ZOOM(1.0, 1.06, (540, 1000)), tr="cut", sfx=[("weight", "thud", 0.35), ("heavier", "swell", 0.3)])
V.shot("L03", s_spin, (0, "yanks"), cam=ZOOM(1.0, 1.06, (540, 1000)), sfx=[("spins", "whir", 0.45)])
V.shot("L03", s_yank, ("yanks", "dozens"), cam=ZOOM(1.0, 1.04, (540, 1100)), tr="cut", sfx=[("yanks", "rumble", 0.55), ("forth", "rumble", 0.4)])
V.shot("L03", s_dozens, ("dozens", 1), cam=ZOOM(1.0, 1.05, (540, 1000)), tr="cut", sfx=[("dozens", "tick", 0.35), ("second", "ding", 0.3)])
V.shot("L04", s_heavy, (0, "The#1"), cam=ZOOM(1.0, 1.05, (540, 1000)), sfx=[("heavy", "thud", 0.4), ("rumbles", "rumble", 0.6)])
V.shot("L04", s_light, ("The#1", 1), cam=ZOOM(1.0, 1.05, (540, 1000)), tr="cut", sfx=[("light", "pop", 0.3), ("buzzes", "buzz_fast", 0.5)])
V.shot("L05", s_coil, (0, "but"), cam=ZOOM(1.0, 1.06, (540, 1000)), music="playful", sfx=[("coils", "zap", 0.3), ("taps", "tick", 0.35)])
V.shot("L05", s_loop, ("but", "A"), cam=ZOOM(1.0, 1.04, (540, 1020)), tr="cut", sfx=[("crash", "crash", 0.6), ("felt", "rumble", 0.5)])
V.shot("L05", s_end, ("A", 1), cam=ZOOM(1.0, 1.04, (540, 1020)), tr="cut", sfx=[("spinning", "whir", 0.35), ("weight", "sparkle", 0.3)])
V.build()
split_long(V, maxd=2.6, keep_cam=True)          # no shot longer than ~2.6 s (a visual change at least every 3 s)
V.title_out = V.voice0["H1"] + V.T["H1"]["dur"]

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if cmd == "sheet":
        print(V.sheet(str(EP / "animatic/stills.jpg"), per_shot=1, cols=5, scale=0.18))
    elif cmd == "qa":
        V.qa_numbers(str(EP / "animatic/frame1.jpg"))
    elif cmd == "big":
        for t in sys.argv[2].split(","):
            V.still(float(t), str(EP / f"animatic/big_{t}.jpg"), 0.5)
    elif cmd == "render":
        V.render(str(EP / "final/A-029.mp4"))
