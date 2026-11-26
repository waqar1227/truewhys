"""B-008 long-video thumbnails A/B/C (1280x720): one big face with an extreme emotion + ONE strange object + max 3 giant words
(never the title), bright subject on a dark background. python episodes/B-008-accidental-inventions/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from flat_fx import burst, arrow
from flat_invent import *
from cast2_flat import char2


def bg(g, a, b, cx=0.64):
    g.fill_all(g.rgrad(W * cx, H * 0.5, W * 0.8, shade(a, 0.15), shade(a, -0.35), b))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * cx, H * 0.5), (W * cx + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
                (W * cx + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def face(g, cid, x, top, expr, flip=False):
    """Head-and-shoulders crop: head top at `top`, head height ~0.42 of the frame."""
    h = 1650
    char2(g, cid, x, top + h, h, expr, "down", "down", t=None, flip=flip, view="3q", blink=False)


def thumb_a(g):
    """Shocked engineer + a huge melting candy bar glowing next to a radar tube. Words: IT MELTED?"""
    bg(g, "#C0582A", "#140502", cx=0.7)
    magnetron(g, 1130, 560, 0.9, 0.3, 1.0)
    burst(g, 860, 300, 120, 230, 12, PAL["yellow"], 10, k=1.0)
    candy_bar(g, 860, 150, 1.6, 0.85, 1.0, rot=0.12)
    face(g, "radar", 330, 20, "shocked")
    words(g, "IT MELTED?", 900, 640, 120, PAL["yellow"])


def thumb_b(g):
    """Lab doctor's amazed face + a giant glowing petri dish with the mould and its clear ring. Words: DIRTY DISH?"""
    bg(g, "#2F7A64", "#020E0A", cx=0.62)
    g.glow(820, 330, 330, "#FFE29A", 0.4)
    petri_dish(g, 820, 330, 260, 0.0, mould=1.0, ring=1.0, seed=8, tilt=0.62)
    arrow(g, 1180, 120, 830, 290, col=PAL["yellow"], w=26, k=1.0)
    face(g, "labdoc", 1090, 60, "shocked", flip=True)
    words(g, "DIRTY DISH?", 620, 640, 112, "#FFFFFF")


def thumb_c(g):
    """Spring flipping down a step by itself + a stunned face. Words: IT WALKED?"""
    bg(g, "#3E5A9A", "#03060F", cx=0.6)
    for i in range(3):
        g.rect(560 + i * 320, 300 + i * 130, 330, 600, "#C98A4A", INK, lw=7)
    slinky_walk(g, 660, 302, 320, 130, 0.55, 1.0, period=1.1, col="#FFC93C", n=15)
    for i in range(3):
        g.path(f"M{780 + i * 40} {130 - i * 10} q20 -20 40 0", None, PAL["cream"], lw=7)
    face(g, "shipwright", 290, 40, "shocked")
    words(g, "IT WALKED?", 900, 640, 118, PAL["yellow"])


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
