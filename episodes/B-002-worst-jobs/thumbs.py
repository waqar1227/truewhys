"""Two thumbnail options (1280x720) for B-002. Plates: /tmp/claude-0/thumbplates/THUMB_BACKYARD.png, THUMB_FAIR.png
(rendered from the backyard/night and fair/day sets)."""
import sys
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance
import cast, gfx
from compose import human_frame

W, H = 1280, 720
OUT = "episodes/B-002-worst-jobs/final/"


def plate(name, color=1.2, bright=1.0):
    bg = Image.open(f"/tmp/claude-0/thumbplates/{name}.png").convert("RGBA").resize((W, H))
    bg = ImageEnhance.Color(bg).enhance(color)
    return ImageEnhance.Brightness(bg).enhance(bright)


def put(f, im, cx, bottom):
    x, y = int(cx - im.width / 2), int(bottom - im.height)
    l = Image.new("RGBA", f.size); l.paste(im, (x, y)); f.alpha_composite(l)


def glow(im, col=(255, 240, 200), r=18):
    p = r * 2  # pad so the blur is never clipped into a box
    big = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p)); big.alpha_composite(im, (p, p)); im = big
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a.point(lambda v: min(255, v * 2)))
    out = Image.new("RGBA", im.size); out.alpha_composite(g); out.alpha_composite(im); return out


def prop(name, width):
    im, _ = cast.prop_img(name, 3.0)
    a = im.split()[-1].point(lambda v: 0 if v < 60 else v)  # drop the faint canvas haze
    im.putalpha(a)
    im = im.crop(a.getbbox())
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


def person(c, expr, arms, k, **kw):
    im, pv, u = human_frame(dict(c=c, expr=expr, arms=arms, **kw), 1.0, 2, None, 0.3)
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)

# ---- A: gong farmer at the privy at night, shovel + bucket, "WORST JOB?"
A = plate("THUMB_BACKYARD", 1.15, 1.25)
A.alpha_composite(Image.new("RGBA", (W, H), (10, 20, 40, 40)))
g = person("gongfarmer", "worried", "raise", 0.5, hold_r="shovel")
put(A, glow(g, (255, 210, 140), 16), 930, H + 95)
bk = prop("bucket", 190)
put(A, glow(bk, (255, 210, 140), 12), 1150, H - 25)
t = gfx.text_img("WORST JOB?", gfx.font("lilita", 138), gfx.C["yellow"], stroke=14)
gfx.paste_center(A, t, 430, 120, 1.0, 1.0, rot=-4)
n = gfx.text_img("#1", gfx.font("lilita", 190), gfx.C["coral"], stroke=14)
gfx.paste_center(A, n, 300, 520, 1.0, 1.0, rot=-6)
A.convert("RGB").save(OUT + "thumb_A.jpg", quality=92)

# ---- B: shocked Wy + toad boy holding up a toad at the fair, "WOULD YOU?!"
B = plate("THUMB_FAIR", 1.2, 1.05)
B.alpha_composite(Image.new("RGBA", (W, H), (11, 63, 76, 50)))
wy = person("wy", "surprised", "both_up", 0.44)
put(B, glow(wy, (255, 245, 220), 16), 260, H + 95)
tb = person("toadboy", "worried", "present", 0.46)
put(B, glow(tb, (255, 255, 230), 18), 900, H + 80)
td = prop("toad", 330)
put(B, glow(td, (255, 255, 200), 22), 650, 600)
t2 = gfx.text_img("WOULD YOU?!", gfx.font("lilita", 140), gfx.C["cream"], stroke=14)
gfx.paste_center(B, t2, 760, 105, 1.0, 1.0, rot=-3)
B.convert("RGB").save(OUT + "thumb_B.jpg", quality=92)
print("ok")
