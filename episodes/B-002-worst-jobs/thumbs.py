"""Two thumbnail options (1280x720) for B-002. Plates: /tmp/claude-0/thumbplates/THUMB_BACKYARD.png, THUMB_FAIR.png
(rendered from the backyard/night and fair/day sets)."""
import sys
sys.path.insert(0, "lib")
from PIL import Image, ImageFilter, ImageEnhance
import cast, gfx
from compose import human_frame

W, H = 1280, 720
OUT = "episodes/B-002-worst-jobs/final/"


def plate(shot, color=1.2, bright=0.75, blur=5):
    """Background = a frame of the episode's own rendered plate, blurred + darkened so the cast pops (thumbnail checklist)."""
    import subprocess, tempfile
    t = tempfile.mktemp(suffix=".png")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "0.5", "-i", f"episodes/B-002-worst-jobs/renders/{shot}.mp4", "-frames:v", "1", t], check=True)
    bg = Image.open(t).convert("RGBA").resize((W, H)).filter(ImageFilter.GaussianBlur(blur))
    bg = ImageEnhance.Color(bg).enhance(color)
    bg = ImageEnhance.Brightness(bg).enhance(bright)
    vig = Image.radial_gradient("L").resize((W, H)).point(lambda v: int(v * 0.75))
    dark = Image.new("RGBA", (W, H), (5, 8, 16, 255)); dark.putalpha(vig)
    bg.alpha_composite(dark)
    return bg


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

# ---- A (v2, click checklist): huge shocked gong farmer + glowing bucket, dark night, "WORST JOB?" + "#1"
A = plate("S000", 1.1, 0.7)
g = person("gongfarmer", "surprised", "both_up", 1.05)
put(A, glow(g, (255, 210, 140), 22), 720, H + 520)
bk = prop("bucket", 270)
put(A, glow(bk, (140, 255, 120), 30), 1105, H - 20)
t = gfx.text_img("WORST JOB?", gfx.font("lilita", 150), gfx.C["yellow"], stroke=16)
gfx.paste_center(A, t, 450, 115, 1.0, 1.0, rot=-4)
n = gfx.text_img("#1", gfx.font("lilita", 230), gfx.C["coral"], stroke=16)
gfx.paste_center(A, n, 190, 480, 1.0, 1.0, rot=-6)
A.convert("RGB").save(OUT + "thumb_A.jpg", quality=92)

# ---- B (v2): huge shocked boy, giant toad right at his face, "EAT IT?!"
B = plate("S034", 1.25, 0.7)
b = person("toadboy", "surprised", "both_up", 1.15)
put(B, glow(b, (255, 245, 220), 20), 420, H + 560)
td = prop("toad", 430)
put(B, glow(td, (255, 255, 200), 26), 900, H - 90)
t2 = gfx.text_img("EAT IT?!", gfx.font("lilita", 190), gfx.C["cream"], stroke=18)
gfx.paste_center(B, t2, 900, 120, 1.0, 1.0, rot=-4)
B.convert("RGB").save(OUT + "thumb_B.jpg", quality=92)
print("ok")

# ---- C (owner asked for 3 options, 10 Nov): huge shocked Groom of the Stool holding the cloth, the king's red close stool behind, "ROYAL TOILET?!"
Cc = plate("S021", 1.25, 0.8, 3)
gr = person("groom", "surprised", "present", 0.78, hold_r="cloth")
put(Cc, glow(gr, (255, 230, 170), 22), 360, H + 300)
t3a = gfx.text_img("ROYAL", gfx.font("lilita", 150), gfx.C["cream"], stroke=16)
t3b = gfx.text_img("TOILET?!", gfx.font("lilita", 172), gfx.C["yellow"], stroke=18)
gfx.paste_center(Cc, t3a, 900, 110, 1.0, 1.0, rot=-4)
gfx.paste_center(Cc, t3b, 900, 255, 1.0, 1.0, rot=-4)
Cc.convert("RGB").save(OUT + "thumb_C.jpg", quality=92)
print("ok C")
