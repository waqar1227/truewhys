"""B-004 long-video thumbnails A/B/C (1280x720): one big cast face with an extreme emotion (face >= 35 % of height) + ONE strange object
+ max 3 giant words (never the title), bright subject on a dark background. python episodes/B-004-shape-secrets/thumbs.py
"""
import os, sys, math
os.environ["TW_FLAT_SIZE"] = "1280x720"
from pathlib import Path
EP = Path(__file__).resolve().parent
sys.path.insert(0, str(EP.parent.parent / "lib"))
import cairocffi as cairo
from flat2d import *
from cast2_flat import char2
from flat_shapes import *
from flat_fx import burst


def bg(g, a, b):
    g.fill_all(g.rgrad(W * 0.62, H * 0.5, W * 0.8, a, shade(a, 0.6), b))
    for i in range(16):
        a0 = i * TAU / 16
        g.poly([(W * 0.62, H * 0.5), (W * 0.62 + 2000 * math.cos(a0), H * 0.5 + 2000 * math.sin(a0)),
                (W * 0.62 + 2000 * math.cos(a0 + 0.12), H * 0.5 + 2000 * math.sin(a0 + 0.12))], "#FFFFFF", None, a=0.06)


def words(g, txt, x, y, size, col, rot=-0.05):
    g.text(txt, x, y, size, col, sw=size * 0.22, depth=size * 0.09, rot=rot)


def face(g, cid, x, expr, flip=False):
    # cast v2.1 head is ~1/4 of the figure: h=2300 puts the head (+hair) at ~45 % of a 720 px frame
    char2(g, cid, x, 1840, 1760, expr, "down", "down", t=None, flip=flip, breathe=False, blink=False)


def thumb_a(g):
    """Newton, shocked, + a giant snipped silver coin. Words: NEWTON'S TRAP"""
    bg(g, "#FFB648", "#2B1E2A")
    coin(g, 860, 400, 250, "silver", ridges=True, clip=0.45, face="head", glint=1.0)
    scissors(g, 1020, 400, 1.5, 0.35, rot=math.pi)
    face(g, "newton", 300, "shocked")
    words(g, "NEWTON'S", 900, 110, 104, PAL["cream"])
    words(g, "TRAP", 960, 650, 150, PAL["yellow"])


def thumb_b(g):
    """Sewer worker, shocked, + a square manhole lid falling into its hole. Words: IT FITS?!"""
    bg(g, "#3E8FB0", "#0B1620")
    g.poly([(920 + px * 1.05, 470 + py * 0.42) for px, py in ngon_pts(4, 330, 0)], "#8A8F98", INK, lw=10)
    g.poly([(920 + px * 0.95, 470 + py * 0.38) for px, py in ngon_pts(4, 330, 0)], "#05080C", INK, lw=8)
    with g.at(920, 420, -0.12):
        g.rc(0, 0, 560, 70, "#9AA3AD", INK, lw=10, r=8)
        g.rc(0, -14, 520, 16, "#C9CED6", None, r=6)
    burst(g, 920, 440, 300, 380, 14, PAL["yellow"], 14, k=1.0)
    face(g, "sewer", 300, "shocked")
    words(g, "IT FITS?!", 900, 120, 130, PAL["yellow"])


def thumb_c(g):
    """1920s engineer, suspicious, + a YELLOW stop sign. Words: WAIT... YELLOW?"""
    bg(g, "#F2C14E", "#3E2A14")
    road_sign(g, 900, 380, 250, "octagon", "#F2C14E", "STOP", INK, border=INK)
    face(g, "engineer", 300, "shocked")
    words(g, "YELLOW?!", 920, 660, 130, "#FFFFFF")


def render(fn, out):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    g = G(surf)
    fn(g)
    surf.write_to_png(str(out).replace(".jpg", ".png"))
    from PIL import Image
    im = Image.open(str(out).replace(".jpg", ".png")).convert("RGB")
    im.save(out, quality=92)
    os.remove(str(out).replace(".jpg", ".png"))
    import cast2_flat
    return cast2_flat.DRAWN[-1] if cast2_flat.DRAWN else None


if __name__ == "__main__":
    (EP / "final").mkdir(exist_ok=True)
    from PIL import Image
    ims = []
    for k, fn in (("A", thumb_a), ("B", thumb_b), ("C", thumb_c)):
        out = EP / f"final/thumb_{k}.jpg"
        render(fn, out)
        ims.append(Image.open(out))
    sheet = Image.new("RGB", (1940, 470), (20, 20, 20))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((640, 360)), (i * 650, 0))
    small = [im.resize((168, 94)) for im in ims]
    for i, s in enumerate(small):
        sheet.paste(s, (i * 200, 362))
    sheet.save(EP / "animatic/thumbs_check.jpg", quality=88)
    print("ok")
