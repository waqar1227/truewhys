"""Two thumbnail options (1280x720) for B-001."""
import sys
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw
import cast, gfx
from compose import human_frame

W, H = 1280, 720
bg = Image.open("/tmp/claude-0/thumbplates/THUMB_COURT.png").convert("RGBA").resize((W, H))
bg = ImageEnhance.Color(bg).enhance(1.25)
bg = ImageEnhance.Brightness(bg).enhance(1.05)

def put(f, im, cx, bottom):
    f.alpha_composite(im, (int(cx - im.width / 2), int(bottom - im.height)))

def glow(im, col=(255, 240, 200), r=18):
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a.point(lambda v: min(255, v * 2)))
    out = Image.new("RGBA", im.size); out.alpha_composite(g); out.alpha_composite(im); return out

# ---- A: pig in a man's clothes in the dock, angry judge, "GUILTY?"
A = bg.copy()
A.alpha_composite(Image.new("RGBA", (W, H), (20, 10, 10, 60)))
pig, _ = cast.animal_img("pig", "worried", "small", "open", "clothes", 1.5)
pig = pig.transpose(Image.FLIP_LEFT_RIGHT)
put(A, glow(pig, (255, 255, 230), 22), 700, H + 10)
judge, pv, u = human_frame(dict(c="judge", expr="angry", arms="point_l", hold_r="gavel"), 1.0, 2, None, 0.3)
judge = judge.resize((int(judge.width * 0.34), int(judge.height * 0.34)), Image.LANCZOS)
put(A, glow(judge, (255, 220, 160), 12), 1110, H + 30)
t = gfx.text_img("GUILTY?", gfx.font("lilita", 160), gfx.C["yellow"], stroke=14)
gfx.paste_center(A, t, 340, 112, 1.0, 1.0, rot=-4)
A.convert("RGB").save("episodes/B-001-animal-trials/final/thumb_A.jpg", quality=92)

# ---- B: shocked Wy + pig in the dock, "PIG ON TRIAL?!"
B = bg.copy()
B.alpha_composite(Image.new("RGBA", (W, H), (11, 63, 76, 70)))
wy, pv, u = human_frame(dict(c="wy", expr="surprised", arms="both_up"), 1.0, 2, None, 0.1)
wy = wy.resize((int(wy.width * 0.44), int(wy.height * 0.44)), Image.LANCZOS)
put(B, glow(wy, (255, 245, 220), 16), 270, H + 95)
pig2, _ = cast.animal_img("pig", "surprised", "open", "open", "clothes", 1.3)
pig2 = pig2.transpose(Image.FLIP_LEFT_RIGHT)
put(B, glow(pig2, (255, 255, 230), 20), 900, H + 5)
t2 = gfx.text_img("ON TRIAL?!", gfx.font("lilita", 150), gfx.C["cream"], stroke=14)
gfx.paste_center(B, t2, 860, 108, 1.0, 1.0, rot=-3)
B.convert("RGB").save("episodes/B-001-animal-trials/final/thumb_B.jpg", quality=92)
print("ok")
