"""B-005 long-video thumbnails A/B/C (1280x720): one big cast face with an extreme emotion + ONE strange object + max 3 giant words
(never the title), bright subject on a dark background. python episodes/B-005-annoying-science/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_fx import burst
from flat_annoy import *


def bg(g, a, b):
    g.fill_all(g.rgrad(W * 0.62, H * 0.5, W * 0.8, a, shade(a, 0.6), b))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * 0.62, H * 0.5), (W * 0.62 + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
                (W * 0.62 + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def face(g, cid, x, expr, flip=False):
    char2(g, cid, x, 1840, 1760, expr, "down", "down", t=None, flip=flip, breathe=False, blink=False)


def thumb_a(g):
    """Shocked everyman + a giant buttered toast flipping in mid-air. Words: TABLE'S FAULT?"""
    bg(g, "#3E8FB0", "#0B1620")
    burst(g, 900, 380, 250, 330, 14, PAL["yellow"], 14, k=1.0)
    toast(g, 900, 380, 2.9, 2.3)
    for i in range(4):
        g.line([(620 - i * 30, 140 + i * 60), (700 - i * 30, 120 + i * 60)], PAL["cream"], 12)
    face(g, "modern", 280, "shocked")
    words(g, "TABLE'S", 930, 110, 110, PAL["cream"])
    words(g, "FAULT?", 980, 650, 150, "#FF6B5B")


def thumb_b(g):
    """Shocked runner + a sneaker whose bow explodes apart. Words: 7× GRAVITY"""
    bg(g, "#2F6F62", "#0B1F26")
    burst(g, 920, 300, 190, 270, 12, PAL["yellow"], 14, k=1.0)
    sneaker(g, 960, 470, 1.05)
    bow_knot(g, 910, 300, 1.7, 0.8, 0.9, undone=0.5)
    face(g, "runner", 280, "shocked")
    words(g, "7× GRAVITY", 900, 650, 120, PAL["yellow"])


def thumb_c(g):
    """Shocked physicist + a spaghetti stick snapping into 3 pieces. Words: NEVER 2?"""
    bg(g, "#8E2430", "#1A0608")
    burst(g, 930, 320, 90, 260, 14, PAL["yellow"], 14, k=1.0)
    spaghetti(g, 580, 460, 840, 340, 0, w=44)
    with g.at(940, 210, 0.6):
        spaghetti(g, -130, 0, 130, 0, 0, w=44)
    spaghetti(g, 1040, 340, 1280, 460, 0, w=44)
    face(g, "physicist", 280, "shocked")
    words(g, "NEVER 2?!", 950, 640, 150, PAL["cream"])


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
