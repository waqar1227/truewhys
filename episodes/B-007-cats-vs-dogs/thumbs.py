"""B-007 long-video thumbnails A/B/C (1280x720): one big face with an extreme emotion + ONE strange object + max 3 giant words
(never the title), bright subject on a dark background. python episodes/B-007-cats-vs-dogs/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from flat_fx import burst, arrow
from flat_pets import *


def bg(g, a, b, cx=0.64):
    g.fill_all(g.rgrad(W * cx, H * 0.5, W * 0.8, shade(a, 0.15), shade(a, -0.35), b))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * cx, H * 0.5), (W * cx + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
                (W * cx + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def board(g, x, y, s):
    with g.at(x, y, -0.04, s):
        g.rc(0, 0, 560, 240, PAL["navy"], INK, lw=12, r=34)
        g.rc(0, 0, 520, 200, "#0B1A2B", None, r=26)
        g.text("?", -150, 14, 170, PAL["yellow"], sw=14)
        g.text(":", 0, 6, 120, PAL["cream"], stroke=None)
        g.text("?", 150, 14, 170, PAL["yellow"], sw=14)


def thumb_a(g):
    """Shocked dog face + a smug cat sitting on a scoreboard showing ? : ?. Words: WHO WON?"""
    bg(g, "#B5652A", "#120402")
    burst(g, 930, 300, 190, 300, 14, PAL["yellow"], 12, k=1.0)
    board(g, 930, 330, 0.95)
    cat_sit(g, 990, 214, 0.42, 0.0, "smug", tail=0.4, breathe=False, blink=0.0)
    dog_face(g, 300, 380, 1.55, 0.0, "shock", blink=0.0, brow=0.7, mouth_open=1.0, tongue=0.3)
    words(g, "WHO WON?", 920, 630, 132, PAL["yellow"])


def thumb_b(g):
    """Huge puppy-eyes dog face, a red arrow at the eyebrow. Words: NEW MUSCLE?"""
    bg(g, "#9A3A30", "#120302", cx=0.4)
    dog_face(g, 440, 400, 1.9, 0.0, "calm", brow=1.0, blink=0.0, look=(0.2, -0.5))
    arrow(g, 1120, 150, 540, 245, col=PAL["yellow"], w=34, k=1.0)
    words(g, "NEW MUSCLE?", 930, 610, 104, "#FFFFFF")


def thumb_c(g):
    """Smug cat face with one ear swivelled to a 'MISO!' call it ignores. Words: IT HEARD YOU"""
    bg(g, "#1F6E7E", "#030E12", cx=0.36)
    cat_face(g, 420, 380, 1.75, 0.0, "smug", ear_l=1.0, ear_r=-0.3, look=(-0.4, 0), blink=0.0)
    with g.at(1000, 210, -0.05):
        g.rc(0, 0, 400, 150, "#FFFFFF", INK, lw=10, r=75)
        g.poly([(-120, 60), (-210, 120), (-60, 70)], "#FFFFFF", INK, lw=10)
        g.rc(0, 0, 398, 148, "#FFFFFF", None, r=74)
        g.text("MISO!", 0, 8, 100, INK, stroke=None)
    words(g, "IT HEARD YOU", 900, 615, 98, PAL["yellow"])


def render(fn, out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    g = G(surf)
    fn(g)
    from PIL import Image
    Image.frombuffer("RGBA", (W, H), bytes(surf.get_data()), "raw", "BGRA", 0, 1).convert("RGB").save(out, quality=92)


if __name__ == "__main__":
    (EP / "final").mkdir(exist_ok=True); (EP / "animatic").mkdir(exist_ok=True)
    from PIL import Image
    ims = []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        out = EP / f"final/thumb_{k}.jpg"
        render(fn, out)
        ims.append(Image.open(out))
    sheet = Image.new("RGB", (1940, 470), (20, 20, 20))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((640, 360)), (i * 650, 0))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((168, 94)), (i * 200, 362))
    sheet.save(EP / "animatic/thumbs_check.jpg", quality=88)
    print("ok")
