"""Three very different thumbnails (1280x720) for B-003 from the episode's own Kaggle plates.
A: eye-patch pirate, shocked, night deck, "NOT BLIND?!"  B: captain, shocked, treasure dig + glowing coins, "NO TREASURE?!"
C: captain, shocked, cheering crew behind, "VOTED OUT?!"   python episodes/B-003-pirate-myths/thumbs.py"""
import sys, subprocess, tempfile
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance
import cast, gfx
from compose import human_frame

W, H = 1280, 720
EP = "episodes/B-003-pirate-myths/"


def plate(shot, t=0.5, color=1.2, bright=0.72, blur=5):
    f = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f"{EP}renders/plates/{shot}.mp4", "-frames:v", "1", f], check=True)
    bg = Image.open(f).convert("RGBA").resize((W, H)).filter(ImageFilter.GaussianBlur(blur))
    bg = ImageEnhance.Brightness(ImageEnhance.Color(bg).enhance(color)).enhance(bright)
    vig = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(v * 0.75))
    dark = Image.new("RGBA", (W, H), (5, 8, 16, 255)); dark.putalpha(vig); bg.alpha_composite(dark)
    return bg


def put(f, im, cx, bottom):
    l = Image.new("RGBA", f.size); l.paste(im, (int(cx - im.width / 2), int(bottom - im.height))); f.alpha_composite(l)


def glow(im, col=(255, 240, 200), r=18):
    p = r * 2; big = Image.new("RGBA", (im.width + 2 * p, im.height + 2 * p)); big.alpha_composite(im, (p, p)); im = big
    a = im.split()[-1].filter(ImageFilter.GaussianBlur(r))
    g = Image.new("RGBA", im.size, col + (0,)); g.putalpha(a.point(lambda v: min(255, v * 2)))
    out = Image.new("RGBA", im.size); out.alpha_composite(g); out.alpha_composite(im); return out


def prop(name, width):
    im, _ = cast.prop_img(name, 3.0)
    a = im.split()[-1].point(lambda v: 0 if v < 60 else v); im.putalpha(a); im = im.crop(a.getbbox())
    return im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)


def person(c, expr, arms, k, **kw):
    im, pv, u = human_frame(dict(c=c, expr=expr, arms=arms, **kw), 1.0, 2, None, 0.3)
    return im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)


def words(f, lines, x, y0, rot=-4):
    y = y0
    for txt, size, col in lines:
        t = gfx.text_img(txt, gfx.font("lilita", size), gfx.C[col], stroke=max(14, size // 10))
        gfx.paste_center(f, t, x, y, 1.0, 1.0, rot=rot); y += int(size * 0.98)


A = plate("S026", 0.5, 1.3, 0.75)
put(A, glow(person("pirate2", "surprised", "both_up", 1.1), (190, 210, 255), 22), 420, H + 430)
words(A, [("NOT", 150, "cream"), ("BLIND?!", 185, "yellow")], 930, 150)
A.convert("RGB").save(EP + "final/thumb_A.jpg", quality=92)

B = plate("S036", 0.5, 1.25, 0.7)
put(B, glow(person("captain", "surprised", "both_up", 1.05), (255, 220, 150), 22), 380, H + 430)
put(B, glow(prop("coins", 330), (255, 215, 90), 34), 900, H - 40)
words(B, [("NO", 150, "cream"), ("TREASURE?!", 128, "yellow")], 880, 120)
B.convert("RGB").save(EP + "final/thumb_B.jpg", quality=92)

C = plate("S071", 0.8, 1.2, 0.8, 4)
put(C, glow(person("captain", "surprised", "down", 1.1), (255, 235, 200), 22), 860, H + 430)
words(C, [("VOTED", 160, "cream"), ("OUT?!", 200, "coral")], 330, 160, rot=4)
C.convert("RGB").save(EP + "final/thumb_C.jpg", quality=92)
print("ok")
