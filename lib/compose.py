"""TrueWhys compositor: shots.json + plates + voice -> finished video.

python lib/compose.py <episode_dir> --plates <dir> --out <file.mp4> [--w 1920 --h 1080] [--workers 4]
       [--shots S000,S001] [--still S010:0.5 (one frame PNG for checks)]
Plates: <dir>/<shot>.mp4 (Kaggle finals) or <dir>/<shot>.png (stills, for animatics).
"""
import sys, os, json, math, argparse, subprocess, random, functools, tempfile, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cast, gfx, camera
from audio import build_mix, voice_env

FPS = 30
UNITS_TALL = 545.0  # puppet height in units (feet to head top, without hats)
TINT = {"dusk": (1.04, 0.93, 0.86), "night": (0.80, 0.84, 1.0), "town": (1.03, 0.97, 0.92), "church": (1.02, 0.96, 0.95),
        "day": (1.0, 0.99, 0.97), "barley": (1.02, 0.99, 0.94), "vineyard": (1.0, 1.0, 0.97), "alpine": (1.0, 1.0, 1.0)}
ARMS = {"down": (8, 8), "point_r": (8, 82), "point_l": (82, 8), "raise": (8, 150), "both_up": (140, 140), "shrug": (52, 52),
        "present": (30, 62), "hold": (8, 28), "chin": (8, -148), "wave": (8, 140), "slam": (8, 150)}
HUMANS = set(cast.CHARS)


def is_human(cid):
    return cid in HUMANS or cid.startswith("villager")


# ------------------------------------------------------------------ puppets
REF = 1.6  # reference raster scale for puppets


@functools.lru_cache(maxsize=512)
def rot_arm(cid, hold, angle_q):
    im, pv = cast.arm_img(cid, REF, hold)
    return im.rotate(angle_q, resample=Image.BICUBIC, center=(pv[0] * REF, pv[1] * REF)), (pv[0] * REF, pv[1] * REF)


def human_frame(a, t, d, env, rng_seed):
    """Return (RGBA image at REF scale, pivot(feet) px) for a human puppet at time t."""
    cid = a["c"]
    expr = a.get("expr", "neutral")
    # arms: ease from rest into the target pose (gesture on each shot), timed gestures after
    tgt = ARMS.get(a.get("arms", "down"), ARMS["down"])
    k = gfx.back_out(min(1, max(0, (t - 0.12) / 0.45)), 1.2)
    aL = 8 + (tgt[0] - 8) * k
    aR = 8 + (tgt[1] - 8) * k
    if a.get("arms") == "wave":
        aR = 140 + 22 * math.sin(t * 9)
    for (gt, g) in a.get("gest", []):
        gtt = gt * d if gt <= 1 else gt
        if g == "slam" and t > gtt - 0.25:
            u = min(1, (t - (gtt - 0.25)) / 0.25)
            aR = 150 + (40 - 150) * gfx.ease_out(u)
    breath = math.sin(2 * math.pi * t / 3.1 + rng_seed)
    # blink: deterministic pseudo-random times
    r = random.Random(rng_seed)
    eyes = "open"
    bt = r.uniform(0.4, 2.0)
    while bt < d + 1:
        if 0 <= t - bt < 0.05 or 0.10 <= t - bt < 0.15:
            eyes = "half"
        elif 0.05 <= t - bt < 0.10:
            eyes = "closed"
        bt += r.uniform(2.2, 4.8)
    mouth = "closed"
    if a.get("talk") and env is not None:
        v = env(t)
        mouth = "closed" if v < 0.08 else "small" if v < 0.22 else "open" if v < 0.45 else "wide"
    face = a.get("face", "R")
    look = (1 if face == "R" else -1, 0)
    if a.get("look"):
        look = tuple(a["look"])
    head, hp = cast.head_img(cid, expr, mouth, eyes, look, REF)
    hold_r = a.get("hold_r") or a.get("hold")
    hold_l = a.get("hold_l")
    armL, apL = rot_arm(cid, hold_l, int(round(-aL / 2)) * 2)
    armR, apR = rot_arm(cid, hold_r, int(round(aR / 2)) * 2)
    body, bp = cast.body_img(cid, REF)
    W, H = int(560 * REF), int(820 * REF)
    fx, fy = W / 2, H - 40 * REF
    can = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sy = 1 + 0.012 * breath
    if abs(sy - 1) > 0.001:
        bimg = body.resize((body.width, int(body.height * sy)), Image.BILINEAR)
    else:
        bimg = body
    can.alpha_composite(bimg, (int(fx - bp[0] * REF), int(fy - bp[1] * REF * sy)))
    neck_y = fy - 248 * REF * sy
    for arm, ap, sx in ((armL, apL, -92), (armR, apR, 92)):
        can.alpha_composite(arm, (int(fx + sx * REF - ap[0]), int(neck_y + 32 * REF - ap[1])))
    tilt = 2.2 * math.sin(t * 0.9 + rng_seed) + (5 if a.get("arms") == "shrug" else 0) * k
    hb = head.rotate(tilt, resample=Image.BICUBIC, center=(hp[0] * REF, hp[1] * REF)) if abs(tilt) > 0.2 else head
    bob = 4 * REF * math.sin(2 * math.pi * t / 3.1 + rng_seed + 0.6)
    can.alpha_composite(hb, (int(fx - hp[0] * REF), int(neck_y + 16 * REF + bob - hp[1] * REF)))
    return can, (fx, fy), 545 * REF


def animal_frame(a, t, d, env, rng_seed):
    kind = a["c"]
    expr = a.get("expr", "neutral")
    r = random.Random(rng_seed)
    eyes = "open"
    bt = r.uniform(0.3, 1.5)
    per = (1.0, 2.0) if a.get("blink_fast") else (2.0, 4.5)
    while bt < d + 1:
        if 0 <= t - bt < 0.12:
            eyes = "closed"
        bt += r.uniform(*per)
    mouth = "closed"
    if kind == "rooster" and expr == "surprised":
        mouth = "open" if (t % 1.6) < 0.4 else "closed"
    im, pv = cast.animal_img(kind, expr, mouth, eyes, a.get("outfit"), REF)
    if a.get("face", "R") == "L":
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        pv = (im.width / REF - pv[0], pv[1])
    breath = 1 + 0.015 * math.sin(2 * math.pi * t / 2.4 + rng_seed)
    if a.get("expr") == "happy":
        breath += 0.02 * abs(math.sin(t * 5))
    im = im.resize((im.width, int(im.height * breath)), Image.BILINEAR)
    native_h = {"pig": 380, "rat": 330, "cat": 400, "rooster": 390, "weevil": 230, "basilisk": 360, "dog": 360,
                "bull": 400, "horse": 420, "locust": 240}[kind]
    return im, (pv[0] * REF, pv[1] * REF * breath), native_h * REF


KEY = {"square": "L", "court": "L", "land": "L", "study": "R"}


def shade_puppet(im, key="L", strength=0.22, rim=0.45):
    """Soft cel shadow on the side away from the key light + rim light on the key side."""
    a = np.asarray(im).astype(np.float32)
    h, w = a.shape[:2]
    if w < 6 or h < 6:
        return im
    x = np.linspace(0, 1, w, dtype=np.float32)[None, :]
    g = x if key == "L" else 1 - x
    shadow = 1 - strength * np.clip((g - 0.45) / 0.55, 0, 1) ** 1.3
    a[..., :3] *= shadow[..., None]
    al = Image.fromarray(a[..., 3].astype(np.uint8))
    k = max(3, (min(w, h) // 45) | 1)
    e1 = np.asarray(al.filter(ImageFilter.MinFilter(k))).astype(np.float32)
    e2 = np.asarray(al.filter(ImageFilter.MinFilter(k * 3 if k * 3 % 2 else k * 3 + 1))).astype(np.float32)
    band = np.clip(e1 - e2, 0, 255) / 255.0
    lum = a[..., :3].mean(2)
    band *= np.clip((lum - 90) / 60, 0, 1) * (1 - g) ** 2
    band = np.asarray(Image.fromarray((band * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(max(1, k / 3)))).astype(np.float32) / 255
    a[..., :3] = a[..., :3] * (1 - band[..., None] * rim) + np.array([255, 246, 228], np.float32) * band[..., None] * rim
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def tint_img(im, tint, glow=False, dark=0.0):
    if tint == (1, 1, 1) and not glow and not dark:
        return im
    a = np.asarray(im).astype(np.float32)
    a[..., :3] *= np.array(tint, np.float32)
    if dark:
        a[..., :3] *= (1 - dark)
    if glow:  # warm fire light from below
        h = a.shape[0]
        ramp = np.linspace(0.0, 1.0, h, dtype=np.float32)[:, None] ** 2
        lumk = np.clip((a[..., :3].mean(2) - 60) / 120, 0, 1)
        a[..., 0] += 70 * ramp * lumk; a[..., 1] += 30 * ramp * lumk
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def draw_actor(frame, a, t, d, cam, tint, env, idx, W, H, shot):
    camd = cam
    pos, tgt, lens = camera.cam_at(camd, t / max(d, 1e-3))
    at = a["at"]
    if a.get("walk"):
        k = camera.ease(t / d, "inout")
        at = [at[i] + (a["walk"]["to"][i] - at[i]) * k for i in range(3)]
    x, y, z, ppm = camera.project(at, pos, tgt, lens, W, H)
    if z <= 0.2:
        return
    seed = (hash(a["c"]) + idx * 17) % 1000 / 100.0
    if is_human(a["c"]):
        im, pv, units = human_frame(a, t, d, env if a.get("talk") else None, seed)
    else:
        im, pv, units = animal_frame(a, t, d, env, seed)
    target_h = a["h"] * ppm
    sc = target_h / units
    if sc * im.height < 8:
        return
    w2, h2 = max(1, int(im.width * sc)), max(1, int(im.height * sc))
    im = im.resize((w2, h2), Image.LANCZOS)
    if a.get("walk"):
        y -= abs(math.sin(t * 7)) * target_h * 0.04
    im = shade_puppet(im, KEY.get(shot.get("set"), "L"), rim=0.15 if shot.get("variant") == "night" else 0.45)
    im = tint_img(im, tint, a.get("glow"), 0.55 if shot.get("silhouette") else 0.0)
    ox, oy = x - pv[0] * sc, y - pv[1] * sc
    # contact shadow
    if not a.get("cut"):
        sw, shh = int(w2 * 0.62), max(2, int(w2 * 0.12))
        sh = Image.new("RGBA", (sw + 40, shh + 40), (0, 0, 0, 0))
        ImageDraw.Draw(sh).ellipse([20, 20, 20 + sw, 20 + shh], fill=(20, 12, 10, 110))
        sh = sh.filter(ImageFilter.GaussianBlur(max(2, shh / 3)))
        gfx._safe_paste(frame, sh, x, y + shh * 0.15)
    # cut-off (character behind a bench / railing): hide below projected line
    if a.get("cut"):
        yc = camera.project([at[0], a["cut"][0], a["cut"][1]], pos, tgt, lens, W, H)[1]
        rows = int(yc - oy)
        if rows <= 0:
            return
        if rows < h2:
            arr = np.asarray(im).copy()
            fade = max(2, int(h2 * 0.01))
            arr[rows:, :, 3] = 0
            arr[max(0, rows - fade):rows, :, 3] = (arr[max(0, rows - fade):rows, :, 3] * np.linspace(1, 0, min(fade, rows))[:, None]).astype(np.uint8)
            im = Image.fromarray(arr)
    gfx._safe_paste(frame, im, ox + w2 / 2, oy + h2 / 2)


def draw_prop(frame, p, t, d, cam, tint, W, H):
    name, at, size = p[0], p[1], p[2]
    opt = p[3] if len(p) > 3 else {}
    pos, tgt, lens = camera.cam_at(cam, t / max(d, 1e-3))
    at = list(at)
    k = 1.0
    if "drop" in opt:
        tt = opt["drop"] * d
        if t < tt - 0.3:
            return
        u = min(1, (t - (tt - 0.3)) / 0.3)
        at[2] += (1 - u * u) * 0.6
        k = 1.0
    if "pop" in opt:
        tt = opt["pop"] * d
        if t < tt:
            return
        k = gfx.back_out((t - tt) / 0.3)
    x, y, z, ppm = camera.project(at, pos, tgt, lens, W, H)
    im, pv = cast.prop_img(name, 1.0)
    natural = {"painting": 220, "coin": 60, "gloves": 160, "sack": 180, "egg": 120, "scroll": 180, "gavel": 140, "staff": 420,
               "toad": 100, "tankard": 120, "bucket": 140, "shovel": 360, "bread": 90, "bowl": 70, "bottle": 190, "cloth": 120}.get(name, 150)
    sc = size * ppm / natural * k
    if sc <= 0.01:
        return
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    im = tint_img(im, tint)
    gfx._safe_paste(frame, im, x - pv[0] * sc + im.width / 2, y - pv[1] * sc + im.height / 2)


# ------------------------------------------------------------------ plates
class Plate:
    def __init__(self, path, nframes, W, H):
        self.W, self.H, self.n = W, H, nframes
        self.still = None
        self.proc = None
        self.src_n = 0
        self.cur_i, self.cur = -1, None
        if path.suffix == ".png":
            self.still = Image.open(path).convert("RGB").resize((W, H), Image.LANCZOS)
        else:
            pr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                                 "stream=nb_read_packets", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
            self.src_n = max(1, int(pr.stdout.strip() or 1))
            self.proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={W}:{H}:flags=lanczos",
                                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)

    def get(self, i):
        if self.still is not None:
            return self.still.copy()
        # retime: map output frame i to source frame (keeps camera ease, fits the final voice timing)
        want = min(self.src_n - 1, int(round(i * (self.src_n - 1) / max(1, self.n - 1)))) if self.src_n > 1 else 0
        while self.cur_i < want:
            buf = self.proc.stdout.read(self.W * self.H * 3)
            if len(buf) < self.W * self.H * 3:
                break
            self.cur = Image.frombytes("RGB", (self.W, self.H), buf)
            self.cur_i += 1
        return (self.cur or Image.new("RGB", (self.W, self.H))).copy()

    def close(self):
        if self.proc:
            self.proc.stdout.close(); self.proc.wait()


def find_plate(plates, sid):
    for ext in (".mp4", ".png"):
        p = Path(plates) / (sid + ext)
        if p.exists():
            return p
    return None


# ------------------------------------------------------------------ shot renderer
def inset_frame(fn, W, H, t, d, zoom=False):
    """Vertical Shorts: a landscape graphic (map, document, comparison) as a card on the brand background.
    zoom: documents are cropped to the parchment (middle 64%) so the writing stays readable on a phone."""
    iw = int(W * 0.94)
    if zoom:
        fw = int(iw / 0.64); fh = int(fw * 9 / 16)
        full = fn(fw, fh).convert("RGBA")
        x0 = int(fw * 0.18)
        card = full.crop((x0, 0, x0 + iw, fh))
        ih = fh
    else:
        ih = int(iw * 9 / 16)
        card = fn(iw, ih).convert("RGBA")
    f = gfx.brand_bg(W, H).copy()
    f.alpha_composite(gfx.rays(W, H, t, 14))
    k = gfx.back_out(min(1, t / 0.35))
    m = Image.new("L", card.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, iw - 1, ih - 1], radius=int(W * 0.035), fill=255)
    card.putalpha(m)
    sh = Image.new("RGBA", (iw + 80, ih + 80), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([40, 50, iw + 40, ih + 50], radius=int(W * 0.035), fill=(0, 0, 0, 120))
    sh = sh.filter(ImageFilter.GaussianBlur(18))
    gfx.paste_center(f, sh, W / 2, H * 0.40, 0.9 + 0.1 * k)
    gfx.paste_center(f, card, W / 2, H * 0.40, 0.9 + 0.1 * k)
    return f


def short_end(W, H, t, d):
    f = gfx.short_end_bg(W, H, t, d)
    a = dict(c="wy", at=[0, 0, 0], h=1, expr="happy", arms="wave", talk=False)
    im, pv, units = human_frame(a, t, d, None, 1.0)
    k = gfx.back_out(min(1, t / 0.45))
    sc = (H * 0.34) / units * (0.6 + 0.4 * k)
    im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
    gfx._safe_paste(f, im, W / 2, H * 0.90 - pv[1] * sc + im.height / 2)
    return f


def render_shot(shot, plates, ep, W, H, lines_t, env_fn):
    vert = H > W
    s = W / 1080 if vert else W / 1920
    n = max(1, int(round(shot["dur"] * FPS)))
    kind = shot["kind"]
    plate = None
    if kind == "3d":
        pp = find_plate(plates, shot["id"])
        plate = Plate(pp, n, W, H) if pp else None
    tint = TINT.get(shot.get("variant") or "day", (1, 1, 1))
    words = []
    if shot.get("line"):
        L = lines_t[shot["line"]]
        off = shot["line_start"] - shot["start"]
        words = [dict(w=w["w"], s=w["s"] + off + 0.05, e=w["e"] + off + 0.05) for w in L["words"]]
    vig = gfx.vignette(W, H)
    bg_title = None
    if kind == "title":
        p2 = find_plate(plates, "TITLE_BG")
        bg_title = Image.open(p2).convert("RGB") if p2 and p2.suffix == ".png" else None
    for i in range(n):
        t = i / FPS
        d = shot["dur"]
        if kind == "3d":
            fr = (plate.get(i) if plate else Image.new("RGB", (W, H), (60, 80, 90))).convert("RGBA")
            if shot.get("mural") and i == 0:
                pass
            env = (lambda tt, _t0=shot["start"]: env_fn(_t0 + tt)) if env_fn else None
            # draw back-to-front by depth
            pos, tgt, lens = camera.cam_at(shot["cam"], t / max(d, 1e-3))
            order = sorted(enumerate(shot["chars"]), key=lambda ia: -camera.project(ia[1]["at"], pos, tgt, lens, W, H)[2])
            items = [("a", j, a) for j, a in order]
            for p in shot.get("props", []):
                items.append(("p", 0, p))
            for typ, j, a in items:
                if typ == "a":
                    draw_actor(fr, a, t, d, shot["cam"], tint, env, j, W, H, shot)
                else:
                    draw_prop(fr, a, t, d, shot["cam"], tint, W, H)
            if shot.get("label"):
                pass
        elif kind == "card":
            fr = gfx.chapter_card(W, H, t, d, shot["num"], shot["text"])
        elif kind == "title":
            fr = gfx.title_card(W, H, t, d, shot["text"], bg_title)
        elif kind in ("map", "split", "doc"):
            fn = {"map": lambda w, h: gfx.map_frame(w, h, t, d, shot.get("pins", []), shot.get("villages", False)),
                  "split": lambda w, h: gfx.split_frame(w, h, t, d, shot["side"], shot["items"], shot["heading"]),
                  "doc": lambda w, h: gfx.doc_frame(w, h, t, d, shot["doc"])}[kind]
            fr = inset_frame(fn, W, H, t, d, zoom=kind == "doc") if vert else fn(W, H)
        elif kind == "end" and vert:
            fr = short_end(W, H, t, d)
        elif kind == "end":
            fr, (cx, cy, r) = gfx.end_screen(W, H, t, d)
            a = dict(c="wy", at=[0, 0, 0], h=1, expr="happy", arms="wave", talk=False)
            im, pv, units = human_frame(a, t, d, None, 1.0)
            sc = (H * 0.42) / units
            im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
            gfx._safe_paste(fr, im, W * 0.12, H * 0.98 - pv[1] * sc + im.height / 2)
        else:
            fr = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        # overlays
        if kind not in ("card", "end"):
            if shot.get("tag"):
                gfx.tag(fr, shot["tag"], t, d, s)
            for (tt, txt) in shot.get("pop", []):
                gfx.pop_word(fr, txt, t, tt * d if tt <= 1 else tt, d - t, s)
            if words:
                gfx.caption(fr, words, t, s, vertical=vert)
        arr = np.asarray(fr.convert("RGB")).astype(np.float32)
        if kind == "3d":
            arr *= vig
        yield np.clip(arr, 0, 255).astype(np.uint8)
    if plate:
        plate.close()


def encode_segment(shots, plates, ep, W, H, lines_t, env_fn, out):
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for sh in shots:
        for fr in render_shot(sh, plates, ep, W, H, lines_t, env_fn):
            p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()


def _worker(args):
    shots, plates, ep, W, H, out, plan_p, timing_p = args
    lines_t = {t["id"]: t for t in json.loads(Path(timing_p).read_text())}
    env_fn = voice_env(Path(ep), json.loads(Path(plan_p).read_text()))
    encode_segment(shots, plates, ep, W, H, lines_t, env_fn, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ep"); ap.add_argument("--plates", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--w", type=int, default=1920); ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--workers", type=int, default=4); ap.add_argument("--shots", default="")
    ap.add_argument("--still", default=""); ap.add_argument("--noaudio", action="store_true")
    ap.add_argument("--plan", default="", help="other shots.json (e.g. a vertical Short)"); ap.add_argument("--timing", default="")
    a = ap.parse_args()
    ep = Path(a.ep)
    plan_p = Path(a.plan) if a.plan else ep / "shots.json"
    timing_p = Path(a.timing) if a.timing else ep / "timing.json"
    plan = json.loads(plan_p.read_text())
    shots = plan["shots"]
    lines_t = {t["id"]: t for t in json.loads(timing_p.read_text())}
    if a.still:
        sid, tt = a.still.split(":")
        sh = next(x for x in shots if x["id"] == sid)
        env_fn = voice_env(ep, plan)
        target = int(float(tt) * sh["dur"] * FPS)
        for i, fr in enumerate(render_shot(sh, a.plates, ep, a.w, a.h, lines_t, env_fn)):
            if i >= target:
                Image.fromarray(fr).save(a.out); break
        return
    if a.shots:
        want = set(a.shots.split(","))
        shots = [x for x in shots if x["id"] in want]
    # split into contiguous segments for workers
    nseg = max(1, min(a.workers * 3, len(shots)))
    tot = sum(x["dur"] for x in shots)
    segs, cur, acc = [], [], 0
    for x in shots:
        cur.append(x); acc += x["dur"]
        if acc >= tot / nseg:
            segs.append(cur); cur, acc = [], 0
    if cur:
        segs.append(cur)
    tmp = Path(tempfile.mkdtemp(prefix="tw_"))
    jobs = [(sg, a.plates, str(ep), a.w, a.h, str(tmp / f"seg{i:03d}.mp4"), str(plan_p), str(timing_p)) for i, sg in enumerate(segs)]
    from multiprocessing import Pool
    with Pool(a.workers) as pool:
        outs = sorted(pool.map(_worker, jobs))
    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{o}'\n" for o in outs))
    video = tmp / "video.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(video)], check=True)
    if a.noaudio or a.shots:
        shutil.move(str(video), a.out)
    else:
        wav = tmp / "mix.wav"
        build_mix(ep, plan, str(wav))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(video), "-i", str(wav), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                        "-shortest", "-movflags", "+faststart", a.out], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
