"""Shorts thumbnail (owner 16 Nov 2026): a clean frame (no captions/title) + ONE engaging hook/suspense line.
Style F (flat2d make.py):  python tools/short_thumb.py --ep episodes/A-010-wrinkly-fingers --t 1.2 --text "IT'S NOT THE *WATER*"
Style R / any image:       python tools/short_thumb.py --img episodes/A-016-onion-tears/renders/frames/hook_cut/f_0030.jpg --text "..." --out <ep>/final/thumb_v2.jpg
*word* = yellow highlight. --y = text centre as a fraction of height (default 0.20). Output 1080x1920 JPEG (default <ep>/final/thumb_v2.jpg)."""
import sys, argparse, runpy
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
FONT = str(ROOT / "library/fonts/LilitaOne-Regular.ttf")
W, H, INK, CREAM, YEL = 1080, 1920, (42, 28, 30), (255, 244, 224), (255, 201, 60)


def flat_frame(ep, t):
    sys.path.insert(0, str(ROOT / "lib"))
    V = runpy.run_path(str(Path(ep) / "make.py"), run_name="thumb")["V"]
    V.title = None; V.badge = 0
    for sh in V.shots:
        sh["cap"] = False
    raw = V.frame(min(V.nframes - 1, int(t * 30)))
    return Image.frombuffer("RGBA", (W, H), raw, "raw", "BGRA", 0, 1).convert("RGB")


def wrap(words, font, d, maxw):
    lines, cur = [], []
    for w in words:
        test = cur + [w]
        if cur and d.textlength(" ".join(x.replace("*", "") for x in test), font=font) > maxw:
            lines.append(cur); cur = [w]
        else:
            cur = test
    return lines + [cur]


def make(im, text, y=0.20, out="thumb.jpg"):
    im = im.convert("RGB").resize((W, H))
    # soft dark band behind the text so it reads at phone size
    band = Image.new("L", (W, H), 0); bd = ImageDraw.Draw(band)
    cy = int(y * H); bd.rectangle([0, cy - 260, W, cy + 260], fill=150)
    im = Image.composite(Image.new("RGB", (W, H), INK), im, band.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(im)
    size = 190
    while True:
        f = ImageFont.truetype(FONT, size)
        lines = wrap(text.upper().split(), f, d, W - 110)
        widest = max(d.textlength(" ".join(w.replace("*", "") for w in ln), font=f) for ln in lines)
        if (len(lines) <= 2 and widest <= W - 110) or size <= 100:
            break
        size -= 10
    lh = int(size * 1.02); y0 = cy - lh * len(lines) // 2
    for i, ln in enumerate(lines):
        total = d.textlength(" ".join(w.replace("*", "") for w in ln), font=f)
        x = (W - total) / 2
        for w in ln:
            word = w.replace("*", ""); col = YEL if w.startswith("*") else CREAM
            d.text((x, y0 + i * lh), word, font=f, fill=col, stroke_width=max(10, size // 12), stroke_fill=INK)
            x += d.textlength(word + " ", font=f)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    im.save(out, quality=92)
    print("wrote", out)


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--ep"); a.add_argument("--t", type=float, default=1.2); a.add_argument("--img")
    a.add_argument("--text", required=True); a.add_argument("--y", type=float, default=0.20); a.add_argument("--out")
    o = a.parse_args()
    im = Image.open(o.img) if o.img else flat_frame(o.ep, o.t)
    out = o.out or str(Path(o.ep or Path(o.img).parents[3]) / "final/thumb_v2.jpg")
    make(im, o.text, o.y, out)
