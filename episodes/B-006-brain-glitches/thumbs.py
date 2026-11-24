"""B-006 long-video thumbnails A/B/C (1280x720): one big cast face with an extreme emotion + ONE strange object + max 3 giant words
(never the title), bright subject on a dark background. python episodes/B-006-brain-glitches/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_fx import burst, qmark
from flat_brain import *


def bg(g, a, b, cx=0.64):
    g.fill_all(g.rgrad(W * cx, H * 0.5, W * 0.8, a, shade(a, 0.6), b))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * cx, H * 0.5), (W * cx + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
                (W * cx + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def face(g, cid, x, expr, flip=False, pr="down"):
    char2(g, cid, x, 1840, 1760, expr, "down", pr, t=None, flip=flip, breathe=False, blink=False)


def thumb_a(g):
    """Shocked student in a glowing doorway, an empty thought bubble with a big '?'. Words: FORGOT WHY?"""
    bg(g, "#B8732E", "#0E0703")
    doorway(g, 900, 760, 1.25, 0.9, wall="#3A2A1E", inside="#FFE7B0", light=1.0)
    thought(g, 930, 230, 340, 230, 1.0, tail=(-1, 1))
    qmark(g, 930, 230, 190, "#FF6B5B", 0.08, 1.0)
    face(g, "student", 290, "shocked")
    words(g, "FORGOT WHY?", 900, 640, 120, PAL["yellow"])


def thumb_b(g):
    """Shocked Mira + a phone buzzing hard with an empty screen. Words: NOBODY CALLED?"""
    bg(g, "#2F8FA0", "#06161C")
    burst(g, 930, 330, 190, 280, 14, PAL["yellow"], 14, k=1.0)
    phone(g, 930, 330, 1.25, 0.18, lit=1.0, icon="none")
    buzz(g, 930, 330, 170, 0.3, 1.0)
    face(g, "mira", 290, "shocked")
    words(g, "NOBODY CALLED?", 870, 650, 104, "#FFFFFF")


def thumb_c(g):
    """The brain mascot shouting at a power socket that looks like a face. Words: SEE A FACE?"""
    bg(g, "#8E2450", "#14040C", cx=0.5)
    socket(g, 920, 320, 1.55, 1.0)
    brain(g, 330, 420, 1.35, "shout", 0.0)
    words(g, "SEE A FACE?", 860, 640, 120, PAL["yellow"])


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
