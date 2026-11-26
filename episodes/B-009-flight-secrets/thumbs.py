"""B-009 long-video thumbnail (1280x720), ONE thumbnail (owner 26 Nov: he makes Test & Compare variants himself).
One big face with an extreme emotion (Kai, shocked, face >= 35 % of the height) + ONE strange object (the cabin lights being switched OFF,
a big switch glowing in the dark cabin) + 2 giant words that never repeat the title ("ON PURPOSE?!"). python episodes/B-009-flight-secrets/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from flat_fx import burst, arrow
from cast2_flat import char2
from flat_flight import *


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def switch(g, x, y, s=1.0, off=1.0):
    with g.at(x, y, -0.06, s):
        g.glow(0, 0, 260, "#FFE29A", 0.35)
        g.rc(0, 0, 230, 330, "#E9E4DA", INK, lw=12, r=30)
        g.rc(0, 0, 120, 210, "#2A2F3A", INK, lw=8, r=20)
        yy = 50 * (2 * off - 1)
        g.rc(0, yy, 96, 100, "#FF5B4B" if off > 0.5 else "#7DFF9A", INK, lw=8, r=18)
        g.text("OFF", 0, -130, 44, INK, stroke=None)


def thumb(g):
    # dark cabin: aisle-side wall + rows of seats fading into the dark, glowing floor lights and exit sign
    g.fill_all(g.rgrad(W * 0.62, H * 0.5, W * 0.9, "#1E3566", "#0E1A36", "#03060F"))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * 0.72, H * 0.42), (W * 0.72 + 2000 * math.cos(a0), H * 0.42 + 2000 * math.sin(a0)),
                (W * 0.72 + 2000 * math.cos(a0 + 0.12), H * 0.42 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.05)
    for i in range(6):
        g.glow(560 + i * 130, 700 - i * 18, 40, "#FFB347", 0.7)
        g.circle(560 + i * 130, 700 - i * 18, 7, "#FFD68A", None)
    g.rc(1150, 130, 170, 64, "#1B3A2A", INK, lw=6, r=10)
    g.glow(1150, 130, 140, "#7DFF9A", 0.45)
    g.text("EXIT", 1150, 134, 46, "#7DFF9A", stroke=None)
    g.poly([(-50, -40), (1330, -40), (1330, 30), (-50, 70)], "#2A3A5C", INK, lw=6)         # overhead bins in the dark
    oval_window(g, 640, 250, 120, 175, 0.0, night=True)
    oval_window(g, 1180, 320, 120, 175, 0.0, night=True)
    # the strange object: the cabin light switch flipped OFF
    burst(g, 930, 300, 150, 250, 12, PAL["yellow"], 10, k=1.0)
    switch(g, 930, 300, 0.95, 1.0)
    # big shocked face (feet far below the frame), face >= 35 % of the height
    char2(g, "kai", 330, 1460, 1380, "shocked", "down", "hold", t=None, view="front", breathe=False, blink=False)
    words(g, "ON PURPOSE?!", 900, 610, 112, PAL["yellow"])


def render(fn, out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    g = G(surf)
    fn(g)
    from PIL import Image
    im = Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB")
    im.save(out, quality=92)
    return im


if __name__ == "__main__":
    (EP / "final").mkdir(exist_ok=True)
    im = render(thumb, str(EP / "final/thumb_A.jpg"))
    from PIL import Image
    small = im.resize((168, 94))
    sheet = Image.new("RGB", (1280 + 20 + 336, 720), "#222222")
    sheet.paste(im, (0, 0)); sheet.paste(small.resize((336, 188)), (1300, 0)); sheet.paste(small, (1300, 210))
    sheet.save(EP / "animatic/thumbs_check.jpg", quality=85)
    print("ok")
