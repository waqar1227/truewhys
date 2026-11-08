"""Facebook still banner (1080x1350) for B-001. Background: an empty court plate from the Shorts render.
/opt/c3d/bin/python episodes/B-001-animal-trials/banner.py <court_plate_frame.png>
"""
import sys
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import cast, gfx
from compose import human_frame

W, H = 1080, 1350
src = Image.open(sys.argv[1]).convert("RGBA")
src = src.resize((W, int(src.height * W / src.width)))
top = (src.height - H) // 2 + 120
bg = src.crop((0, top, W, top + H))
bg = ImageEnhance.Color(bg).enhance(1.2)
B = bg.copy()
B.alpha_composite(Image.new("RGBA", (W, H), (20, 10, 10, 55)))


def put(f, im, cx, bottom):
    f.alpha_composite(im, (int(cx - im.width / 2), int(bottom - im.height)))


def glow(im, col=(255, 240, 200), r=18):
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a.point(lambda v: min(255, v * 2)))
    out = Image.new("RGBA", im.size); out.alpha_composite(g); out.alpha_composite(im); return out


# top gradient for the headline
grad = Image.new("L", (1, 420)); grad.putdata([int(200 * (1 - i / 419) ** 1.4) for i in range(420)])
shade = Image.new("RGBA", (W, 420), gfx.hexa(gfx.C["deep"])); shade.putalpha(grad.resize((W, 420)))
B.alpha_composite(shade, (0, 0))

# cast: judge (right, pointing), pig in a man's clothes (centre), Wy surprised (left)
pig, _ = cast.animal_img("pig", "worried", "small", "open", "clothes", 1.3)
pig = pig.transpose(Image.FLIP_LEFT_RIGHT)
put(B, glow(pig, (255, 255, 230), 22), 470, H - 175)
judge, _, _ = human_frame(dict(c="judge", expr="angry", arms="point_l", hold_r="gavel"), 1.0, 2, None, 0.3)
judge = judge.resize((int(judge.width * 0.5), int(judge.height * 0.5)), Image.LANCZOS)
put(B, glow(judge, (255, 220, 160), 12), 875, H - 125)
wy, _, _ = human_frame(dict(c="wy", expr="surprised", arms="both_up"), 1.0, 2, None, 0.1)
wy = wy.resize((int(wy.width * 0.4), int(wy.height * 0.4)), Image.LANCZOS)
put(B, glow(wy, (255, 245, 220), 14), 150, H - 125)

# headline
t1 = gfx.text_img("A PIG WENT", gfx.font("lilita", 128), gfx.C["cream"], stroke=12)
t2 = gfx.text_img("ON TRIAL?!", gfx.font("lilita", 150), gfx.C["yellow"], stroke=13)
gfx.paste_center(B, t1, W // 2, 120, 1.0, 1.0, rot=-2)
gfx.paste_center(B, t2, W // 2, 262, 1.0, 1.0, rot=-2)

# bottom strip: wordmark + call to action
strip = Image.new("RGBA", (W, 120), gfx.hexa(gfx.C["deep"], 235))
B.alpha_composite(strip, (0, H - 120))
B.alpha_composite(Image.new("RGBA", (W, 8), gfx.hexa(gfx.C["coral"])), (0, H - 120))
wm = gfx.text_img("TrueWhys", gfx.font("lilita", 64), gfx.C["cream"], stroke=6)
gfx.paste_center(B, wm, 190, H - 58)
cta = gfx.text_img("FULL STORY ON YOUTUBE", gfx.font("lilita", 46), gfx.C["yellow"], stroke=5)
gfx.paste_center(B, cta, 720, H - 58)

B.convert("RGB").save("episodes/B-001-animal-trials/social/banner.jpg", quality=92)
print("ok")
