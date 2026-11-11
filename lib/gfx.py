"""TrueWhys 2D motion graphics (Pillow). All functions draw onto an RGBA frame of size (W,H)
for a local time t (s) within an element of duration d. Brand colours + fonts from branding/."""
import math, json, functools
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cast

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "library/fonts"
C = dict(teal="#0F6B78", deep="#0B3F4C", navy="#10263B", yellow="#FFC93C", coral="#FF6B5B", cream="#FFF4E0",
         ink="#2A1C1E", mint="#5ED3B5", parch="#F3E2BC", parch2="#E3C78F")


@functools.lru_cache(maxsize=64)
def font(name, size):
    f = {"lilita": "LilitaOne-Regular.ttf", "poppins": "Poppins-Bold.ttf", "poppinsx": "Poppins-ExtraBold.ttf", "fredoka": "Fredoka.ttf"}[name]
    fo = ImageFont.truetype(str(FONTS / f), size)
    if name == "fredoka":
        try:
            fo.set_variation_by_name("SemiBold")
        except Exception:
            pass
    return fo


def ease_out(t):
    t = min(1, max(0, t)); return 1 - (1 - t) ** 3


def ease_inout(t):
    t = min(1, max(0, t)); return 4 * t ** 3 if t < .5 else 1 - (-2 * t + 2) ** 3 / 2


def back_out(t, s=1.7):
    t = min(1, max(0, t)) - 1; return t * t * ((s + 1) * t + s) + 1


def text_img(txt, fnt, fill, stroke=0, stroke_fill=C["ink"], shadow=True, spacing=0, align="center"):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bb = d.multiline_textbbox((0, 0), txt, font=fnt, stroke_width=stroke, spacing=spacing, align=align)
    w, h = int(bb[2] - bb[0] + 20), int(bb[3] - bb[1] + 30)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dr = ImageDraw.Draw(im)
    if shadow:
        sh = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(sh).multiline_text((10 - bb[0], 18 - bb[1]), txt, font=fnt, fill=(20, 12, 14, 150), stroke_width=stroke, stroke_fill=(20, 12, 14, 150), spacing=spacing, align=align)
        im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(3)))
    dr.multiline_text((10 - bb[0], 10 - bb[1]), txt, font=fnt, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, spacing=spacing, align=align)
    return im


def paste_center(frame, im, cx, cy, scale=1.0, alpha=1.0, rot=0.0):
    if scale <= 0.01 or alpha <= 0.01:
        return
    if scale != 1.0:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.LANCZOS)
    if rot:
        im = im.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1:
        a = np.asarray(im).copy(); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); im = Image.fromarray(a)
    frame.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2))) if _inside(frame, im, cx, cy) else _safe_paste(frame, im, cx, cy)


def _inside(frame, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    return x >= 0 and y >= 0 and x + im.width <= frame.width and y + im.height <= frame.height


def _safe_paste(frame, im, cx, cy):
    x, y = int(cx - im.width / 2), int(cy - im.height / 2)
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(frame.width, x + im.width), min(frame.height, y + im.height)
    if x1 <= x0 or y1 <= y0:
        return
    frame.alpha_composite(im.crop((x0 - x, y0 - y, x1 - x, y1 - y)), (x0, y0))


def hexa(h, a=255):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


@functools.lru_cache(maxsize=8)
def brand_bg(W, H, top=C["teal"], bot=C["deep"]):
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / W) ** 2 + ((y - H * 0.42) / H) ** 2) * 1.6
    c1, c2 = np.array(hexa(top)[:3], float), np.array(hexa(bot)[:3], float)
    k = np.clip(r, 0, 1)[..., None]
    img = (c1 * (1 - k) + c2 * k).astype(np.uint8)
    return Image.fromarray(img).convert("RGBA")


def rays(W, H, t, alpha=22, n=16):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, cy, R = W / 2, H * 0.45, max(W, H) * 1.2
    a0 = t * 0.08
    for k in range(n):
        a = a0 + k * 2 * math.pi / n
        d.polygon([(cx, cy), (cx + R * math.cos(a), cy + R * math.sin(a)), (cx + R * math.cos(a + 0.12), cy + R * math.sin(a + 0.12))], fill=(255, 255, 255, alpha))
    return im


def dotted_ring(W, H, cx, cy, r, t, col=C["yellow"]):
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    n = 40
    for k in range(n):
        a = k * 2 * math.pi / n + t * 0.3
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=hexa(col, 220))
    return im

# ------------------------------------------------------------------ cards

def chapter_card(W, H, t, d, num, title, sub=None):
    f = brand_bg(W, H).copy()
    f.alpha_composite(rays(W, H, t))
    s = W / 1920
    k_in = back_out(t / 0.45)
    k_out = ease_inout((t - (d - 0.35)) / 0.35)
    cx, cy = W / 2, H * 0.40
    f.alpha_composite(dotted_ring(W, H, cx, cy, 150 * s * k_in, t))
    circ = Image.new("RGBA", (int(260 * s), int(260 * s)), (0, 0, 0, 0))
    ImageDraw.Draw(circ).ellipse([8, 8, circ.width - 8, circ.height - 8], fill=hexa(C["yellow"]), outline=hexa(C["ink"]), width=int(12 * s))
    nt = text_img(str(num), font("lilita", int(150 * s)), C["ink"], shadow=False)
    circ.alpha_composite(nt, (int(circ.width / 2 - nt.width / 2), int(circ.height / 2 - nt.height / 2)))
    paste_center(f, circ, cx, cy, k_in * (1 - k_out))
    kt = ease_out((t - 0.18) / 0.5)
    ti = text_img(title, font("lilita", int(104 * s)), C["cream"], stroke=int(8 * s))
    paste_center(f, ti, cx, H * 0.66 + (1 - kt) * 60 * s, 1.0, kt * (1 - k_out))
    ch = text_img(sub or f"CHAPTER {num}", font("poppins", int(34 * s)), C["mint"], shadow=False)
    paste_center(f, ch, cx, H * 0.775 + (1 - kt) * 60 * s, 1.0, kt * (1 - k_out))
    if k_out > 0:  # coral wipe out
        wp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        x = int(W * (1 - k_out) * 1.2 - W * 0.2)
        ImageDraw.Draw(wp).polygon([(x, 0), (W + 400, 0), (W + 400, H), (x - 300, H)], fill=hexa(C["coral"]))
        f.alpha_composite(wp)
    return f


def title_card(W, H, t, d, text, bg=None):
    s = W / 1920
    if bg is not None:
        f = bg.resize((W, H)).filter(ImageFilter.GaussianBlur(14 * s)).convert("RGBA")
        f.alpha_composite(Image.new("RGBA", (W, H), hexa(C["deep"], 150)))
    else:
        f = brand_bg(W, H).copy()
    f.alpha_composite(rays(W, H, t, 16))
    k = back_out(t / 0.6)
    ti = text_img(text, font("lilita", int(118 * s)), C["cream"], stroke=int(9 * s), spacing=int(10 * s))
    paste_center(f, ti, W / 2, H * 0.46, 0.6 + 0.4 * k, min(1, t / 0.25))
    # Wy peeking at bottom-left, presenting
    return f


@functools.lru_cache(maxsize=4)
def _land_polys():
    gj = json.loads((ROOT / "library/maps/ne_50m_land.geojson").read_text())
    polys = []
    for ft in gj["features"]:
        g = ft["geometry"]
        rings = [g["coordinates"]] if g["type"] == "Polygon" else g["coordinates"]
        for poly in rings:
            ring = poly[0]
            if any(-15 < x < 30 and 35 < y < 60 for x, y in ring):
                polys.append(ring)
    return polys


PLACES = {"Falaise": (-0.20, 48.90), "Autun": (4.30, 46.95), "Basel": (7.59, 47.56), "St-Julien": (6.40, 45.25),
          "Paris": (2.35, 48.85), "London": (-0.12, 51.51), "Colchester": (0.90, 51.89), "Hereford": (-2.72, 52.06),
          "Wales": (-3.70, 52.30), "Westminster": (-0.13, 51.50)}


def map_frame(W, H, t, d, pins, villages=False, view=None):
    s = W / 1920
    f = Image.new("RGBA", (W, H), hexa("#1E6E84"))
    # view: zoom in slowly on France / Switzerland
    k = ease_inout(t / d)
    lon0, lat0 = 3.2 + 0.6 * k, 47.2
    span = 18 - 4 * k if not villages else 7 - 2 * k
    if villages:
        lon0, lat0 = 4.3, 46.95
    if view:  # (lon, lat, span in degrees): any region, slow 15% zoom-in
        lon0, lat0, span = view[0], view[1], view[2] * (1 - 0.15 * k)
    sc = W / span
    clat = math.cos(math.radians(lat0 if view else 47))
    def P(lon, lat):
        return (W / 2 + (lon - lon0) * sc * clat, H / 2 - (lat - lat0) * sc)
    d_ = ImageDraw.Draw(f)
    # sea texture: subtle wave lines
    for yy in range(0, H, int(38 * s)):
        d_.line([(0, yy), (W, yy)], fill=hexa("#2A7C92"), width=max(1, int(2 * s)))
    for ring in _land_polys():
        pts = [P(x, y) for x, y in ring]
        d_.polygon([(x + 6 * s, y + 10 * s) for x, y in pts], fill=hexa("#0B3F4C", 120))
    for ring in _land_polys():
        pts = [P(x, y) for x, y in ring]
        d_.polygon(pts, fill=hexa(C["parch"]), outline=hexa(C["ink"]), width=max(2, int(5 * s)))
    if villages:
        import random
        R = random.Random(3)
        for i in range(26):
            lo, la = lon0 + R.uniform(-2.6, 2.6), lat0 + R.uniform(-1.6, 1.6)
            tt = 0.5 + i * 0.1
            if t > tt:
                kk = back_out((t - tt) / 0.3)
                x, y = P(lo, la)
                r = 12 * s * kk
                d_.rectangle([x - r, y - r * 0.6, x + r, y + r], fill=hexa(C["cream"]), outline=hexa(C["ink"]), width=max(2, int(3 * s)))
                d_.polygon([(x - r * 1.2, y - r * 0.6), (x, y - r * 1.6), (x + r * 1.2, y - r * 0.6)], fill=hexa(C["coral"]), outline=hexa(C["ink"]))
                rr = text_img("🐀" if False else "", font("poppins", 10), C["ink"], shadow=False)
    shown_xy = [P(*PLACES[n]) for n, tt_ in pins if n and n in PLACES and t >= tt_]
    for name, tt in pins:
        if not name or name not in PLACES or t < tt:
            continue
        kk = back_out((t - tt) / 0.35)
        x, y = P(*PLACES[name])
        pin = Image.new("RGBA", (int(80 * s), int(110 * s)), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pin)
        pw = pin.width
        pd.polygon([(pw * 0.2, pw * 0.55), (pw * 0.5, pin.height - 4), (pw * 0.8, pw * 0.55)], fill=hexa(C["coral"]), outline=hexa(C["ink"]))
        pd.ellipse([6, 6, pw - 6, pw - 6], fill=hexa(C["coral"]), outline=hexa(C["ink"]), width=max(2, int(6 * s)))
        pd.ellipse([pw * 0.33, pw * 0.33, pw * 0.67, pw * 0.67], fill=hexa(C["cream"]))
        paste_center(f, pin, x, y - pin.height * 0.45 * kk, kk)
        lab = text_img(name.upper().replace("ST-", "SAINT-"), font("lilita", int(44 * s)), C["cream"], stroke=int(5 * s))
        # pins close together: the eastern one's label goes beside it so nothing overlaps
        near = [q for q in shown_xy if q != (x, y) and math.hypot(q[0] - x, q[1] - y) < 170 * s]
        if near and x >= max(q[0] for q in near):  # the eastern pin of a close pair: label to its right
            paste_center(f, lab, x + lab.width / 2 + 34 * s, y - 30 * s, 1.0, min(1, (t - tt) / 0.3))
        else:
            paste_center(f, lab, x, y + 40 * s, 1.0, min(1, (t - tt) / 0.3))
    return f


def split_frame(W, H, t, d, side, items, heading):
    s = W / 1920
    f = brand_bg(W, H, C["navy"], "#081420").copy()
    half = W // 2
    for k_side in ("left", "right"):
        x0 = 0 if k_side == "left" else half
        active = side == k_side
        col = C["teal"] if k_side == "left" else C["coral"]
        panel = Image.new("RGBA", (half - int(40 * s), H - int(80 * s)), hexa(col, 255 if active else 70))
        f.alpha_composite(panel, (x0 + int(20 * s), int(40 * s)))
        if not active:
            continue
        kk = back_out(t / 0.4)
        hd = text_img(heading, font("lilita", int(64 * s)), C["cream"], stroke=int(6 * s))
        paste_center(f, hd, x0 + half / 2, H * 0.16, kk)
        for i, it in enumerate(items):
            tt = 0.35 + i * 0.45
            if t < tt:
                continue
            k2 = back_out((t - tt) / 0.35)
            gx = x0 + half * (0.27 + 0.46 * (i % 2))
            gy = H * (0.42 + 0.33 * (i // 2))
            kind = {"mouse": "rat"}.get(it, it)
            im, pv = cast.animal_img(kind, "neutral" if i % 2 else "worried", scale=0.55 * s * (0.7 if kind == "rat" else 1))
            paste_center(f, im, gx, gy - 20 * s, k2)
            lb = text_img(it.upper(), font("poppins", int(36 * s)), C["cream"], stroke=int(4 * s))
            paste_center(f, lb, gx, gy + im.height * 0.42, k2)
    if side == "right":  # show finished left panel dimmed with its heading
        hd = text_img("GROUP 1", font("lilita", int(54 * s)), C["cream"], stroke=int(5 * s))
        paste_center(f, hd, half / 2, H * 0.5, 1.0, 0.6)
    return f


def parchment(W, H, t, seed=1, torn_bottom=False):
    s = W / 1920
    f = brand_bg(W, H, "#3A2A22", "#1E1410").copy()
    pw, ph = int(1180 * s), int(880 * s)
    rng = np.random.default_rng(seed)
    noise = (rng.normal(0, 1, (ph // 8 + 1, pw // 8 + 1)) * 10).astype(np.float32)
    nimg = Image.fromarray(np.clip(128 + noise, 0, 255).astype(np.uint8)).resize((pw, ph), Image.BICUBIC)
    base = Image.new("RGBA", (pw, ph), hexa(C["parch"]))
    tone = Image.merge("RGBA", [nimg.point(lambda v: int(v * 0.9 + 120))] * 3 + [Image.new("L", (pw, ph), 70)])
    base = Image.alpha_composite(base, tone)
    mask = Image.new("L", (pw, ph), 0)
    md = ImageDraw.Draw(mask)
    pts = []
    for i in range(41):
        pts.append((i / 40 * pw, rng.uniform(0, 10 * s)))
    right = [(pw - rng.uniform(0, 10 * s), i / 30 * ph) for i in range(31)]
    if torn_bottom:
        bot = [(pw * (1 - i / 40), ph * 0.78 + rng.uniform(-40, 40) * s + (60 * s if i % 5 == 0 else 0)) for i in range(41)]
    else:
        bot = [(pw * (1 - i / 40), ph - rng.uniform(0, 10 * s)) for i in range(41)]
    left = [(rng.uniform(0, 10 * s), ph * (1 - i / 30)) for i in range(31)]
    md.polygon(pts + right + bot + left, fill=255)
    base.putalpha(mask)
    edge = base.filter(ImageFilter.GaussianBlur(14 * s))
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0)); sh.putalpha(mask.filter(ImageFilter.GaussianBlur(20 * s)).point(lambda v: v // 2))
    k = ease_out(t / 0.5)
    y = H / 2 + (1 - k) * 80 * s
    paste_center(f, Image.new("RGBA", sh.size, (0, 0, 0, 120)) if False else sh, W / 2 + 14 * s, y + 20 * s, 1.0, k)
    paste_center(f, base, W / 2, y, 1.0, k)
    return f, (W / 2 - pw / 2, y - ph / 2, pw, ph), k


def write_lines(f, box, lines, t, t0=0.3, cps=40, fnt=None, col=C["ink"], start_y=0.16, gap=1.35):
    s = f.width / 1920
    x0, y0, pw, ph = box
    fnt = fnt or font("fredoka", int(46 * s))
    shown = max(0, (t - t0) * cps)
    y = y0 + ph * start_y
    d = ImageDraw.Draw(f)
    for ln in lines:
        n = int(min(len(ln), shown))
        if n > 0:
            d.text((x0 + pw * 0.09, y), ln[:n], font=fnt, fill=hexa(col))
        shown -= len(ln)
        y += fnt.size * gap


def seal(f, cx, cy, t, tt, s, col=C["coral"]):
    if t < tt:
        return
    k = back_out((t - tt) / 0.3)
    r = 70 * s * k
    d = ImageDraw.Draw(f)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=hexa(col), outline=hexa("#8A2734"), width=max(2, int(8 * s)))
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], outline=hexa("#8A2734"), width=max(2, int(5 * s)))


DOCS = {
    "summons": ("SUMMONS", ["To the rats of the diocese of Autun:", "you are hereby ordered to appear", "before this court, on the day", "named below, to answer for", "the barley you have eaten."], "seal"),
    "sentence": ("SENTENCE · FALAISE, 1386", ["The sow shall be wounded in the head", "and front legs, as the child was,", "and then hanged in the public square,", "near the town hall."], "seal"),
    "deed": ("LAND FOR THE WEEVILS · 1587", ["A plot outside the vineyards is given", "to the said insects, \"in good form", "and of perpetual validity\".", "The villagers keep the right of way,", "without spoiling the weevils' pasture."], "seal"),
    "eaten": ("FINAL VERDICT", ["Having heard both parties, and the", "report of the experts, this court", "now decides that the weevils"], "eaten"),
    "tithe": ("THE TITHE", ["One tenth of what you grew or earned,", "paid to the church every year."], "tithe"),
    "paper2013": ("JOURNAL OF LAW AND ECONOMICS · 2013", ["\"Vermin Trials\"", "by Peter T. Leeson", "", "Idea: the trials helped the church", "collect tithes again."], "paper"),
    "basilisk": ("LEGEND: THE BASILISK", ["An egg laid by a rooster...", "could hatch a monster that kills", "with a single look."], "basilisk"),
    "potion": ("WITCHES' POTIONS", ["Rooster eggs were said to be", "the secret ingredient."], "potion"),
    # B-002 (paraphrased summaries, not quotations; sources in episodes/B-002-worst-jobs/sources.md)
    "aleassize": ("THE ASSIZE OF BREAD AND ALE", ["Ale must be sold at a fair price,", "in honest measures, and of good", "strength. Brewers who break the", "rule are fined by the court."], "seal"),
    "toady": ("A WORD IS BORN", ["TOAD-EATER (1600s):", "someone who flatters the powerful", "", "TOADY (1800s):", "the same idea, still used today"], "paper"),
    "aubrey": ("JOHN AUBREY · 1680s", ["In parts of Wales and the border,", "a poor man was hired at funerals", "to eat bread and drink ale passed", "over the body, and so take on", "the sins of the dead."], "paper"),
    "order1627": ("ROYAL ORDER · 1627", ["Saltpetre men may dig in stables,", "dove-houses and cellars.", "Owners must leave those floors", "as loose, open earth, ready", "for the next digging."], "seal"),
    "surnames": ("SURNAMES FROM THIS JOB", ["FULLER", "TUCKER", "WALKER", "", "All mean someone who fulled cloth."], "paper"),
    "colchester": ("COLCHESTER · c. 1425", ["The brewers complain: the tanners", "soak their hides in the river", "the brewers draw their water from."], "seal"),
    "coroner1326": ("LONDON CORONER'S ROLL · 1326", ["Richard le Rakiere was seated on", "the latrine in his house; the planks", "being rotten gave way, and he fell", "in and was drowned."], "seal"),
}


def doc_frame(W, H, t, d, doc):
    s = W / 1920
    title, lines, extra = DOCS[doc]
    f, box, k = parchment(W, H, t, seed=hash(doc) % 100, torn_bottom=(extra == "eaten"))
    x0, y0, pw, ph = box
    dr = ImageDraw.Draw(f)
    tt = text_img(title, font("lilita", int(58 * s)), "#6B2A1E", shadow=False)
    f.alpha_composite(tt, (int(x0 + pw * 0.08), int(y0 + ph * 0.05)))
    dr.line([(x0 + pw * 0.08, y0 + ph * 0.15), (x0 + pw * 0.92, y0 + ph * 0.15)], fill=hexa("#A8865A"), width=max(2, int(4 * s)))
    if extra in ("basilisk", "potion"):
        write_lines(f, box, lines, t, 0.4, 45, start_y=0.62)
        if extra == "basilisk":
            im, _ = cast.animal_img("basilisk", "angry", scale=1.1 * s)
            egg, _ = cast.prop_img("egg", 0.9 * s)
            kk = back_out((t - 0.3) / 0.5)
            paste_center(f, egg, x0 + pw * 0.22, y0 + ph * 0.42, kk)
            paste_center(f, im, x0 + pw * 0.62, y0 + ph * 0.38 + 8 * s * math.sin(t * 3), kk)
        else:
            cx, cy = x0 + pw * 0.5, y0 + ph * 0.42
            r = 150 * s
            dr.ellipse([cx - r, cy - r * 0.5, cx + r, cy + r * 0.9], fill=hexa("#2A1C1E"))
            dr.ellipse([cx - r * 0.9, cy - r * 0.55, cx + r * 0.9, cy - r * 0.15], fill=hexa("#5ED3B5"), outline=hexa(C["ink"]), width=max(2, int(6 * s)))
            for i in range(6):
                bx = cx + math.sin(t * 2 + i) * r * 0.6
                by = cy - r * 0.6 - ((t * 120 * s + i * 40 * s) % (160 * s))
                dr.ellipse([bx - 12 * s, by - 12 * s, bx + 12 * s, by + 12 * s], fill=hexa("#9AF0D8", 200))
            egg, _ = cast.prop_img("egg", 0.7 * s)
            paste_center(f, egg, cx + r * 0.9, cy - r * 0.9 - 20 * s * math.sin(t * 2), 1.0)
        return f
    # type fast enough that every document is fully written by ~70% of its shot
    cps = max(42, sum(len(l) for l in lines) / max(0.5, 0.7 * d - 0.45))
    write_lines(f, box, lines, t, 0.45, cps)
    if extra == "seal":
        seal(f, x0 + pw * 0.8, y0 + ph * 0.82, t, min(d - 0.6, 0.5 + sum(len(l) for l in lines) / cps), s)
    elif extra == "eaten":
        # bite marks along the torn edge + a rat and a weevil peeking
        for i in range(7):
            bx = x0 + pw * (0.12 + i * 0.12)
            by = y0 + ph * 0.8
            dr.ellipse([bx - 30 * s, by - 26 * s, bx + 30 * s, by + 30 * s], fill=hexa("#2A1E18"))
        if t > 1.0:
            kk = back_out((t - 1.0) / 0.4)
            r_, _ = cast.animal_img("rat", "smug", "closed", scale=0.75 * s)
            w_, _ = cast.animal_img("weevil", "smug", scale=0.9 * s)
            paste_center(f, r_, x0 + pw * 0.28, y0 + ph * 0.95 + (1 - kk) * 100 * s, 1.0)
            paste_center(f, w_, x0 + pw * 0.7, y0 + ph * 0.92 + (1 - kk) * 100 * s, 1.0)
    elif extra == "tithe":
        cx, cy = x0 + pw * 0.5, y0 + ph * 0.62
        for i in range(10):
            kk = back_out((t - 0.8 - i * 0.12) / 0.3)
            if kk <= 0:
                continue
            bx = cx - pw * 0.36 + i * pw * 0.08
            church = i == 9
            col = C["coral"] if church else C["yellow"]
            lift = -60 * s * ease_out((t - 2.4) / 0.5) if church else 0
            dr.rounded_rectangle([bx, cy - 90 * s * kk + lift, bx + pw * 0.065, cy + 90 * s + lift], radius=int(12 * s), fill=hexa(col), outline=hexa(C["ink"]), width=max(2, int(5 * s)))
        if t > 2.4:
            lb = text_img("1 / 10 → CHURCH", font("lilita", int(52 * s)), C["coral"], stroke=int(5 * s))
            paste_center(f, lb, cx + pw * 0.2, cy + 160 * s, 1.0, min(1, (t - 2.4) / 0.3))
    elif extra == "paper":
        dr.rectangle([x0 + pw * 0.08, y0 + ph * 0.78, x0 + pw * 0.55, y0 + ph * 0.8], fill=hexa("#A8865A"))
    return f


def end_screen(W, H, t, d):
    s = W / 1920
    f = brand_bg(W, H).copy()
    f.alpha_composite(rays(W, H, t, 18))
    k = back_out(t / 0.6)
    wm = text_img("TrueWhys", font("lilita", int(150 * s)), C["cream"], stroke=int(10 * s))
    paste_center(f, wm, W * 0.30, H * 0.20, k)
    tg = text_img("The real story behind life's weirdest whys", font("fredoka", int(44 * s)), C["yellow"], stroke=int(3 * s))
    paste_center(f, tg, W * 0.30, H * 0.32, 1.0, min(1, max(0, (t - 0.4) / 0.4)))
    # end-screen element areas (YouTube places video cards here): two video boxes, subscribe circle
    dr = ImageDraw.Draw(f)
    for i, (bx, by) in enumerate([(W * 0.56, H * 0.14), (W * 0.56, H * 0.53)]):
        kk = ease_out((t - 0.5 - i * 0.2) / 0.4)
        bw, bh = W * 0.38, W * 0.38 * 9 / 16
        dr.rounded_rectangle([bx, by, bx + bw, by + bh], radius=int(24 * s), outline=hexa(C["yellow"], int(255 * kk)), width=max(3, int(8 * s)), fill=hexa(C["deep"], int(160 * kk)))
        lb = text_img("WATCH NEXT" if i == 0 else "MORE TRUE WHYS", font("lilita", int(48 * s)), C["cream"], shadow=False)
        paste_center(f, lb, bx + bw / 2, by + bh / 2, 1.0, kk * 0.6)
    cx, cy, r = W * 0.30, H * 0.66, 150 * s
    dr.ellipse([cx - r, cy - r, cx + r, cy + r], outline=hexa(C["yellow"]), width=max(3, int(8 * s)))
    sb = text_img("SUBSCRIBE", font("lilita", int(40 * s)), C["cream"], stroke=int(4 * s))
    paste_center(f, sb, cx, cy + r + 40 * s, 1.0, min(1, max(0, (t - 0.8) / 0.4)))
    return f, (cx, cy, r)

def short_end_bg(W, H, t, d):
    """Last seconds of every Short: wordmark, 'Follow for more true whys' (Wy is drawn on top by the compositor)."""
    s = W / 1080
    f = brand_bg(W, H).copy()
    f.alpha_composite(rays(W, H, t, 20))
    k = back_out(min(1, t / 0.5))
    wm = text_img("TrueWhys", font("lilita", int(170 * s)), C["cream"], stroke=int(12 * s))
    paste_center(f, wm, W / 2, H * 0.12, k)
    for i, (txt, col) in enumerate((("FOLLOW FOR MORE", C["cream"]), ("TRUE WHYS", C["yellow"]))):
        kk = back_out(min(1, max(0, (t - 0.25 - i * 0.15) / 0.4)))
        im = text_img(txt, font("lilita", int(118 * s)), col, stroke=int(10 * s))
        paste_center(f, im, W / 2, H * (0.23 + i * 0.075), max(0.01, kk))
    return f


# ------------------------------------------------------------------ overlays on 3D shots

def pop_word(f, text, t, tt, d_left, s, size=1.0):
    if t < tt:
        return
    k = back_out((t - tt) / 0.28)
    out = min(1, max(0, d_left / 0.25))
    im = text_img(text, font("lilita", int(120 * s * size)), C["yellow"], stroke=int(10 * s * size))
    fit = min(1.0, f.width * 0.9 / im.width)  # long words shrink to fit (vertical Shorts)
    paste_center(f, im, f.width / 2, f.height * 0.2, (0.4 + 0.6 * k) * fit, out, rot=3 * (1 - k) - 2)


def tag(f, text, t, d, s):
    k = ease_out((t - 0.15) / 0.45) * min(1, max(0, (d - t) / 0.35))
    if k <= 0:
        return
    fn = font("poppins", int(38 * s))
    tx = text_img(text, fn, C["ink"], shadow=False)
    pad = int(26 * s)
    w, h = tx.width + pad * 2 + int(40 * s), tx.height + int(10 * s)
    pill = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([0, 0, w - 1, h - 1], radius=h // 2, fill=hexa(C["yellow"]), outline=hexa(C["ink"]), width=max(2, int(5 * s)))
    pd.ellipse([pad * 0.6, h / 2 - 12 * s, pad * 0.6 + 24 * s, h / 2 + 12 * s], fill=hexa(C["coral"]), outline=hexa(C["ink"]), width=max(1, int(3 * s)))
    pill.alpha_composite(tx, (pad + int(30 * s), int(2 * s)))
    x = int(70 * s - (1 - k) * (w + 100 * s))
    f.alpha_composite(pill, (max(-w, x), int(f.height * (0.11 if f.height > f.width else 0.08))))


def caption(f, words, t, s, keyset=(), vertical=False):
    """Phrase caption at the bottom with the current word highlighted (vertical: bigger, fewer words, higher up)."""
    chunks, cur = [], []
    mw, mc = (3, 17) if vertical else (5, 30)
    for w in words:
        cur.append(w)
        if len(cur) >= mw or w["w"].endswith((".", ",", "?", "!", ":", "...")) or sum(len(x["w"]) + 1 for x in cur) > mc:
            chunks.append(cur); cur = []
    if cur:
        chunks.append(cur)
    show = None
    for i, c in enumerate(chunks):
        end = chunks[i + 1][0]["s"] if i + 1 < len(chunks) else c[-1]["e"] + 0.25
        if c[0]["s"] - 0.05 <= t < end:
            show = c; break
    if not show:
        return
    fn = font("poppinsx", int((84 if vertical else 50) * s))
    started = [k for k, w in enumerate(show) if w["s"] - 0.03 <= t]
    cur_k = started[-1] if started else -1
    parts = []
    for k, w in enumerate(show):
        active = k == cur_k
        txt = w["w"].strip()
        col = C["yellow"] if active else "#FFFFFF"
        parts.append(text_img(txt, fn, col, stroke=int(6 * s), stroke_fill="#120C0E", shadow=False))
    gap = int(16 * s)
    tw = sum(p.width for p in parts) + gap * (len(parts) - 1)
    x = f.width / 2 - tw / 2
    y = f.height * (0.68 if vertical else 0.915)
    if tw > f.width * 0.92:  # never run off the edge
        k0 = f.width * 0.92 / tw
        parts = [p.resize((max(1, int(p.width * k0)), max(1, int(p.height * k0))), Image.LANCZOS) for p in parts]
        gap = int(gap * k0); tw = sum(p.width for p in parts) + gap * (len(parts) - 1)
    x = f.width / 2 - tw / 2
    for k, (p, w) in enumerate(zip(parts, show)):
        active = k == cur_k
        sc = 1.08 if active else 1.0
        paste_center(f, p, x + p.width / 2, y, sc)
        x += p.width + gap


def vignette(W, H, strength=0.32):
    y, x = np.mgrid[0:H, 0:W]
    r = np.sqrt(((x - W / 2) / (W / 2)) ** 2 + ((y - H / 2) / (H / 2)) ** 2)
    v = 1 - strength * np.clip((r - 0.55) / 0.9, 0, 1) ** 1.6
    return v.astype(np.float32)[..., None]


# ------------------------------------------------------------------ magnifier insets (reusable, on top of a 3D plate)

def _grains_scene(R, t, d):
    """Square RGBA tile (R x R): wet sand grains. Water flows in, grains drift apart (no grip)."""
    im = Image.new("RGBA", (R, R), hexa("#3E8FB0")); dr = ImageDraw.Draw(im)
    rng = np.random.default_rng(7)
    k = ease_inout(min(1.0, max(0.0, (t - 0.4) / max(0.5, d * 0.55))))      # 0 packed -> 1 loose
    n = 9; cell = R / (n - 1.2)
    for gy in range(n):
        for gx in range(n):
            j = rng.uniform(-0.18, 0.18, 2); rr = cell * rng.uniform(0.44, 0.52)
            cx = (gx - 0.1 + j[0]) * cell; cy = (gy - 0.1 + j[1]) * cell
            ox, oy = (cx - R / 2) * 0.16 * k, (cy - R / 2) * 0.16 * k           # spread apart
            wob = math.sin(t * 2.4 + gx * 1.7 + gy * 0.9) * cell * 0.05 * k
            x, y = cx + ox + wob, cy + oy + wob * 0.6
            rr2 = rr * (1 - 0.18 * k)
            col = ["#E3B878", "#D9A964", "#EBC58C", "#CF9E5A"][(gx * 3 + gy) % 4]
            dr.ellipse([x - rr2 + 3, y - rr2 + 5, x + rr2 + 3, y + rr2 + 5], fill=(40, 30, 20, 70))
            dr.ellipse([x - rr2, y - rr2, x + rr2, y + rr2], fill=hexa(col), outline=hexa(C["ink"]), width=max(2, R // 160))
            dr.ellipse([x - rr2 * 0.55, y - rr2 * 0.6, x - rr2 * 0.1, y - rr2 * 0.2], fill=(255, 245, 220, 120))
    for b in range(10):  # little water bubbles rising between grains
        bx = (b * 97 % R); by = (R - (t * 120 + b * 61) * (0.5 + 0.5 * k)) % R
        dr.ellipse([bx - 6, by - 6, bx + 6, by + 6], outline=(220, 245, 255, int(170 * k)), width=2)
    return im


def _svg_tile(body, R, bg):
    """Render an SVG body drawn in a 1000x1000 box (ink outlines) to an R x R RGBA tile."""
    svg = cast._svg(f'<rect x="-50" y="-50" width="1100" height="1100" fill="{bg}" stroke="none"/>' + body, (0, 0, 1000, 1000))
    return cast._png(svg, R / 1000.0).resize((R, R), Image.LANCZOS)


def _foodchain_scene(R, t, d):
    """Arctic food chain: fish -> seal -> polar bear, yellow vitamin-A dots pile up at each step (A-002)."""
    def k(t0, dur=0.35):
        return max(0.0, min(1.0, (t - t0) / dur))
    st = [0.15, d * 0.33, d * 0.62]            # fish, seal, bear appear
    b = ['<rect x="-50" y="560" width="1100" height="500" fill="#1E5E8C" stroke="none"/>',
         '<path d="M-50 560 Q250 540 500 560 T1050 560" fill="none" stroke="#9FD8F0" stroke-width="10"/>',
         '<path d="M500 560 L1050 560 L1050 600 L480 600 Z" fill="#EAF4FF"/>',
         '<path d="M150 560 L450 560 L430 592 L170 592 Z" fill="#EAF4FF"/>']
    def dots(cx, cy, n, r, kk, spread):
        out = []
        for i in range(int(round(n * kk))):
            a = i * 2.39996; rr = spread * math.sqrt((i + 0.5) / n)
            out.append(f'<circle cx="{cx + rr*math.cos(a):.0f}" cy="{cy + rr*math.sin(a)*0.7:.0f}" r="{r}" fill="#FFC93C" stroke-width="5"/>')
        return "".join(out)
    def arrow(x0, y0, x1, y1, kk):
        if kk <= 0:
            return ""
        xe, ye = x0 + (x1 - x0) * kk, y0 + (y1 - y0) * kk
        L = math.hypot(x1 - x0, y1 - y0); ux, uy = (x1 - x0) / L, (y1 - y0) / L
        hd = "" if kk < 0.6 else (f'<path d="M{xe-34*ux+24*uy:.0f} {ye-34*uy-24*ux:.0f} L{xe:.0f} {ye:.0f} L{xe-34*ux-24*uy:.0f} {ye-34*uy+24*ux:.0f}" '
                                  'fill="none" stroke="#FFF4E0" stroke-width="16"/>')
        return f'<path d="M{x0} {y0} L{xe:.0f} {ye:.0f}" fill="none" stroke="#FFF4E0" stroke-width="16"/>' + hd
    # fish swimming in the water, bottom
    kf = back_out(k(st[0]))
    if kf > 0:
        sw = 10 * math.sin(t * 5)
        b.append(f'<g transform="translate(330 {790+sw:.0f}) scale({0.9*kf:.2f})">'
                 '<path d="M-120 0 L-185 -55 L-185 55 Z" fill="#7FB3D6"/><ellipse cx="0" cy="0" rx="130" ry="62" fill="#9FC7E0"/>'
                 '<path d="M-60 -32 Q0 -52 60 -32" fill="none" stroke="#FFFFFF" stroke-width="10" opacity="0.7"/>'
                 '<ellipse cx="72" cy="-12" rx="14" ry="16" fill="#FFFFFF" stroke-width="7"/><circle cx="76" cy="-10" r="7" fill="#1E1A24" stroke="none"/>'
                 '</g>' + dots(320, 795 + sw, 3, 16, k(st[0] + 0.3, 0.5), 45))
    b.append(arrow(440, 730, 420, 620, k(st[1] - 0.35, 0.35)))
    # seal on the ice floe
    ks = back_out(k(st[1]))
    if ks > 0:
        b.append(f'<g transform="translate(330 560) scale({0.8*ks:.2f})">'
                 '<path d="M-150 -10 L-200 -60 L-190 10 Z" fill="#6E7A86"/>'
                 '<path d="M-160 0 Q-90 -130 50 -120 Q140 -110 130 -30 Q120 0 -160 0 Z" fill="#8C98A4"/>'
                 '<circle cx="100" cy="-120" r="52" fill="#8C98A4"/>'
                 '<ellipse cx="94" cy="-134" rx="14" ry="17" fill="#FFFFFF" stroke-width="7"/><circle cx="98" cy="-132" r="8" fill="#1E1A24" stroke="none"/>'
                 '<ellipse cx="140" cy="-106" rx="14" ry="10" fill="#1E1A24" stroke="none"/></g>'
                 + dots(300, 510, 9, 14, k(st[1] + 0.3, 0.6), 60))
    b.append(arrow(470, 470, 540, 400, k(st[2] - 0.35, 0.35)))
    # polar bear on the ice shelf, its liver glowing with the most dots
    kb = back_out(k(st[2]))
    if kb > 0:
        fur = "#F4F1E6"
        b.append(f'<g transform="translate(650 560) scale({0.62*kb:.2f})">'
                 + "".join(f'<rect x="{lx-26}" y="-110" width="52" height="110" rx="22" fill="#E2DED2"/>' for lx in (-110, -55, 55, 110))
                 + f'<ellipse cx="-20" cy="-170" rx="175" ry="100" fill="{fur}"/>'
                 f'<ellipse cx="135" cy="-235" rx="88" ry="74" fill="{fur}"/>'
                 f'<circle cx="86" cy="-296" r="24" fill="{fur}"/><circle cx="178" cy="-296" r="24" fill="{fur}"/>'
                 '<ellipse cx="184" cy="-204" rx="50" ry="36" fill="#E8E4D8"/><ellipse cx="216" cy="-218" rx="16" ry="12" fill="#1E1A24" stroke="none"/>'
                 '<ellipse cx="128" cy="-252" rx="13" ry="16" fill="#FFFFFF" stroke-width="7"/><circle cx="132" cy="-250" r="7" fill="#1E1A24" stroke="none"/>'
                 f'<path d="M-90 -190 Q-120 -230 -60 -228 Q0 -236 6 -196 Q0 -160 -50 -166 Q-90 -154 -90 -190 Z" fill="#B23A3A" opacity="{min(1, k(st[2]+0.4, 0.5)):.2f}"/>'
                 '</g>')
        pulse = 1 + 0.08 * math.sin(t * 9)
        b.append(f'<circle cx="623" cy="436" r="{80*pulse*k(st[2]+0.4, 0.5):.0f}" fill="#FFC93C" opacity="0.25" stroke="none"/>')
        b.append(dots(623, 436, 18, 11, k(st[2] + 0.5, 0.7), 60))
    return _svg_tile("".join(b), R, "#123A5E")


def _peel_scene(R, t, d):
    """Friendly cartoon hand with pale skin flakes curling up and drifting off (no wounds, no gore). A-002."""
    skin, sh = "#E9B48C", "#D49A70"
    b = ['<ellipse cx="500" cy="980" rx="430" ry="160" fill="#1A3150" stroke="none"/>',
         f'<path d="M330 1050 L360 640 Q370 560 430 560 L600 560 Q660 560 670 640 L700 1050 Z" fill="{skin}"/>']
    fingers = [(392, 560, 300, -8), (468, 548, 360, -2), (548, 552, 340, 4), (624, 570, 290, 10)]
    for (x, y, L, a) in fingers:
        b.append(f'<g transform="rotate({a} {x} {y})"><rect x="{x-36}" y="{y-L}" width="72" height="{L+40}" rx="36" fill="{skin}"/>'
                 f'<path d="M{x-18} {y-L+50} Q{x} {y-L+40} {x+18} {y-L+50}" fill="none" stroke="{sh}" stroke-width="7"/></g>')
    b.append(f'<g transform="rotate(-38 330 760)"><rect x="294" y="560" width="72" height="230" rx="36" fill="{skin}"/></g>')
    b.append(f'<path d="M420 760 Q500 800 600 760" fill="none" stroke="{sh}" stroke-width="8"/>')
    rng = np.random.default_rng(11)
    pts = [(rng.uniform(380, 660), rng.uniform(300, 980)) for _ in range(26)]
    for i, (x, y) in enumerate(pts):
        t0 = 0.25 + i * (max(0.6, d - 0.8) / len(pts))
        u = (t - t0)
        if u < 0:
            continue
        lift = min(1.0, u / 0.4)                       # flake curls up
        fall = max(0.0, u - 0.4)                        # then drifts down and sideways
        fx = x + 40 * math.sin(fall * 3 + i) + fall * 30 * (1 if i % 2 else -1)
        fy = y + fall * 260
        rot = (i * 47 + fall * 160) % 360
        sz = 22 + (i % 4) * 6
        op = max(0.0, 1 - fall / 2.2)
        if op <= 0 or fy > 1080:
            continue
        b.append(f'<g transform="translate({fx:.0f} {fy:.0f}) rotate({rot:.0f}) scale(1 {0.4+0.6*lift:.2f})" opacity="{op:.2f}">'
                 f'<path d="M{-sz} 0 Q0 {-sz*0.9:.0f} {sz} 0 Q0 {sz*0.5:.0f} {-sz} 0 Z" fill="#FBEEDC" stroke-width="5"/></g>')
    return _svg_tile("".join(b), R, "#244A70")


def _dose_scene(R, t, d):
    """Gauge: one gram of polar bear liver vs an adult's daily vitamin-A limit; the needle swings past the limit. A-002."""
    u = ease_out(min(1.0, max(0.0, (t - 0.3) / max(0.6, d * 0.5))))
    val = 1.4 * u + (0.03 * math.sin(t * 22) if u > 0.95 else 0)   # 13,000-18,000 IU vs 10,000 IU limit
    def ang(v):                                    # 0..1.6 maps to 200..340 deg (left to right over the top)
        return math.radians(200 + 140 * min(v, 1.6) / 1.6)
    cx, cy, r = 500, 640, 360
    def arc(v0, v1, col):
        a0, a1 = ang(v0), ang(v1)
        return (f'<path d="M{cx + r*math.cos(a0):.0f} {cy + r*math.sin(a0):.0f} A{r} {r} 0 0 1 {cx + r*math.cos(a1):.0f} {cy + r*math.sin(a1):.0f}" '
                f'fill="none" stroke="{col}" stroke-width="70" stroke-linecap="butt"/>')
    b = [f'<circle cx="{cx}" cy="{cy}" r="{r+60}" fill="#FFF4E0"/>',
         arc(0, 0.6, "#5ED38A"), arc(0.6, 1.0, "#FFC93C"), arc(1.0, 1.6, "#FF5B4B")]
    a1 = ang(1.0)
    b.append(f'<path d="M{cx + (r-60)*math.cos(a1):.0f} {cy + (r-60)*math.sin(a1):.0f} L{cx + (r+50)*math.cos(a1):.0f} {cy + (r+50)*math.sin(a1):.0f}" stroke-width="14"/>')
    a = ang(val)
    b.append(f'<path d="M{cx - 40*math.cos(a):.0f} {cy - 40*math.sin(a):.0f} L{cx + (r-20)*math.cos(a):.0f} {cy + (r-20)*math.sin(a):.0f}" stroke="#1E1A24" stroke-width="22"/>')
    b.append(f'<circle cx="{cx}" cy="{cy}" r="44" fill="#FF6B5B" stroke-width="10"/>')
    # one-gram liver cube under the gauge
    b.append('<g transform="translate(500 850)"><path d="M-70 -40 L0 -80 L70 -40 L70 40 L0 80 L-70 40 Z" fill="#9C3A3A"/>'
             '<path d="M-70 -40 L0 0 L70 -40 M0 0 L0 80" fill="none" stroke-width="9"/>'
             '<path d="M-40 -48 L0 -66 L40 -48" fill="none" stroke="#D86A5A" stroke-width="10"/></g>')
    return _svg_tile("".join(b), R, "#123A5E")


LENS_SCENES = {"grains": _grains_scene, "foodchain": _foodchain_scene, "peel": _peel_scene, "dose": _dose_scene}


def lens_inset(f, name, t, d, s, labels=(), at=(0.5, 0.47), rad=0.36):
    """Magnifying-glass circle with an animated close-up (LENS_SCENES[name]) over the frame.
    labels: [(text, x, y, t_in)] in lens units (-1..1). Pops in with back_out, pops out at the end."""
    W, H = f.size
    a_in = back_out(min(1.0, t / 0.35)); a_out = min(1.0, max(0.0, (d - t) / 0.25))
    sc = a_in * a_out
    if sc <= 0.01:
        return
    R = int(W * rad * 2 * sc)
    if R < 8:
        return
    tile = _grains_scene(int(W * rad * 2), t, d) if name == "grains" else LENS_SCENES[name](int(W * rad * 2), t, d)
    tile = tile.resize((R, R), Image.LANCZOS)
    mask = Image.new("L", (R, R), 0); ImageDraw.Draw(mask).ellipse([0, 0, R - 1, R - 1], fill=255)
    cx, cy = int(W * at[0]), int(H * at[1])
    dim = Image.new("RGBA", (W, H), (10, 20, 30, int(110 * sc))); f.alpha_composite(dim)
    f.paste(tile, (cx - R // 2, cy - R // 2), mask)
    d2 = ImageDraw.Draw(f)
    rw = max(6, int(16 * s * sc))
    d2.ellipse([cx - R // 2 - rw, cy - R // 2 - rw, cx + R // 2 + rw, cy + R // 2 + rw], outline=hexa(C["ink"]), width=rw + 4)
    d2.ellipse([cx - R // 2 - rw // 2, cy - R // 2 - rw // 2, cx + R // 2 + rw // 2, cy + R // 2 + rw // 2], outline=hexa(C["yellow"]), width=rw)
    hx, hy = cx + int(R * 0.36), cy + int(R * 0.36)          # handle
    d2.line([hx, hy, hx + int(R * 0.28), hy + int(R * 0.28)], fill=hexa(C["ink"]), width=int(rw * 2.6))
    d2.line([hx, hy, hx + int(R * 0.27), hy + int(R * 0.27)], fill=hexa(C["coral"]), width=int(rw * 1.7))
    for txt, lx, ly, t_in in labels:
        if t < t_in:
            continue
        k = back_out(min(1.0, (t - t_in) / 0.3)) * a_out
        im = text_img(txt, font("lilita", int(54 * s)), C["cream"], stroke=int(6 * s))
        paste_center(f, im, cx + lx * R / 2, cy + ly * R / 2, scale=max(0.01, k))
