"""Third thumbnail option (1280x720) for B-001: rats sued for eating the barley (Autun, 1522).
/opt/c3d/bin/python episodes/B-001-animal-trials/thumb_c.py <barley_field_still.png>
(still: lib/render_bg.py episodes/B-001-animal-trials/shots.json <dir> --w 1280 --h 720 --stills --shots_only S036)"""
import sys
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance
import cast, gfx

W, H = 1280, 720
bg = Image.open(sys.argv[1]).convert("RGBA").resize((W, H)).filter(ImageFilter.GaussianBlur(4))
bg = ImageEnhance.Color(bg).enhance(1.3); bg = ImageEnhance.Brightness(bg).enhance(0.72)
vig = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(v * 0.7))
dark = Image.new("RGBA", (W, H), (5, 8, 16, 255)); dark.putalpha(vig); bg.alpha_composite(dark)


def glow(im, col=(255, 240, 200), r=18):
    p = r * 2
    big = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p)); big.alpha_composite(im, (p, p)); im = big
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a.point(lambda v: min(255, v * 2)))
    out = Image.new("RGBA", im.size); out.alpha_composite(g); out.alpha_composite(im); return out


def put(f, im, cx, bottom):
    l = Image.new("RGBA", f.size); l.paste(im, (int(cx - im.width / 2), int(bottom - im.height))); f.alpha_composite(l)


def fit(im, h):
    a = im.split()[-1]; im = im.crop(a.getbbox())
    return im.resize((int(im.width * h / im.height), h), Image.LANCZOS)

rat, _ = cast.animal_img("rat", "surprised", "open", scale=3.0)
put(bg, glow(fit(rat, 610), (255, 235, 190), 22), 360, H + 20)
sc, _ = cast.prop_img("scroll", 3.0)
put(bg, glow(fit(sc, 330), (255, 250, 220), 20), 930, H - 30)
t1 = gfx.text_img("RATS", gfx.font("lilita", 170), gfx.C["cream"], stroke=16)
t2 = gfx.text_img("SUED?!", gfx.font("lilita", 200), gfx.C["yellow"], stroke=18)
gfx.paste_center(bg, t1, 905, 105, 1.0, 1.0, rot=-4)
gfx.paste_center(bg, t2, 905, 265, 1.0, 1.0, rot=-4)
bg.convert("RGB").save("episodes/B-001-animal-trials/final/thumb_C.jpg", quality=92)
print("ok")
