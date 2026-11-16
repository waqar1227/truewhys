"""Shared Style R shot helpers (Blender): eased keys, camera moves, word-timed frames, gas wisps rising, idle blinks, and the
standard render loop for an episode's shots.json. Used by episodes/*/scene.py (A-016, A-017, ...)."""
import os, sys, json, math, time, random
import bpy
from mathutils import Vector
import sr_common as C, sr_human as Hm

FPS = 30

def ease(t):
    t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)


def key_obj(o, f, loc=None, rot=None, scale=None):
    if loc is not None:
        o.location = loc; o.keyframe_insert("location", frame=f)
    if rot is not None:
        o.rotation_euler = rot; o.keyframe_insert("rotation_euler", frame=f)
    if scale is not None:
        o.scale = scale if hasattr(scale, "__len__") else (scale,) * 3; o.keyframe_insert("scale", frame=f)


def cam_move(cam, n, a, b=None, orbit=0, fstop=4.0, focus=None):
    c = {"from": {"pos": list(a[0]), "tgt": list(a[1]), "lens": a[2]}, "to": ({"pos": list(b[0]), "tgt": list(b[1]), "lens": b[2]} if b else None),
         "ease": "inout", "fstop": fstop}
    if orbit:
        c["orbit"] = orbit
    if focus:
        c["focus"] = list(focus)
    C.key_camera(cam, c, n)


def W_(sh, word, default=0.0):
    """shot-local frame where `word` starts."""
    t = sh["words"].get(word)
    return int(round((t if t is not None else default) * FPS))


def puffs_rise(ps, n, origin, top_z, drift=(0.0, 0.0), spread=0.05, speed=1.0, t0=0, seed=3, target=None, fade_in=8):
    """Animate gas puffs rising from origin (keys every 2 frames). target: optional point they curve towards."""
    rnd = random.Random(seed)
    for i, p in enumerate(ps):
        ph = rnd.random(); sx, sy = rnd.gauss(0, spread), rnd.gauss(0, spread * 0.5)
        sc0 = p.scale[0]
        for f in range(0, n + 1, 2):
            u = ((f - t0) / max(1, n) * speed + ph) % 1.0 if f >= t0 else 0.0
            if f < t0:
                key_obj(p, f, loc=origin, scale=0.0); continue
            z = origin[2] + (top_z - origin[2]) * u
            x = origin[0] + sx * (0.3 + u) + drift[0] * u + 0.012 * math.sin(f * 0.25 + i)
            y = origin[1] + sy * (0.3 + u) + drift[1] * u
            if target is not None:
                k = ease(u); x = x + (target[0] - x) * k * 0.8; y = y + (target[1] - y) * k * 0.8; z = z + (target[2] - z) * k * 0.6
            s = sc0 * min(1.0, (f - t0) / fade_in) * (1.0 - max(0.0, u - 0.8) / 0.2) * (0.7 + 0.8 * u)
            key_obj(p, f, loc=(x, y, z), scale=max(s, 0.0))




def life(h, n, seed=1, blinks=True):
    """Small idle life: blinks every ~1.5-2.5 s."""
    if not blinks:
        return
    rnd = random.Random(seed); f = rnd.randint(8, 20)
    while f < n - 6:
        Hm.blink(h["keys"], f); f += rnd.randint(40, 70)


def parent_keep(o, parent, bone=None):
    mw = o.matrix_world.copy(); o.parent = parent
    if bone:
        o.parent_type = "BONE"; o.parent_bone = bone
    o.matrix_world = mw


def run(shots_fns, argv):
    """argv: <shots.json> <out_dir> [--w --h --samples --step --at --shots a,b --gpu --part i/n --mblur]"""
    global FPS
    PLAN, OUT = argv[0], argv[1]
    def opt(k, d=None, f=str):
        return f(argv[argv.index(k) + 1]) if k in argv else d
    W, H, SAMPLES, STEP = opt("--w", 540, int), opt("--h", 960, int), opt("--samples", 12, int), opt("--step", 1, int)
    AT = opt("--at", None, float); ONLY = opt("--shots", None); GPU = "--gpu" in argv; MBLUR = "--mblur" in argv; PART = opt("--part", "0/1")
    JPG = "--jpg" in argv; ext = "jpg" if JPG else "png"
    plan = json.load(open(PLAN)); FPS = plan["fps"]
    os.makedirs(OUT, exist_ok=True)
    todo = [s for s in plan["shots"] if (ONLY is None or s["name"] in ONLY.split(","))]
    i, k = map(int, PART.split("/"))
    todo = todo[i::k]
    log = open(os.path.join(OUT, f"render_log_{i}.txt"), "a")
    for sh in todo:
        t0 = time.time()
        C.clear()
        cam = C.make_camera()
        n = sh["frames"]
        shots_fns[sh["name"]](sh, cam, n)
        C.setup_render(W, H, SAMPLES, gpu=GPU, mblur=MBLUR, look="AgX - Punchy")
        sc = bpy.context.scene; sc.render.fps = FPS; sc.frame_start = 0; sc.frame_end = n
        if JPG:
            sc.render.image_settings.file_format = "JPEG"; sc.render.image_settings.quality = 95
        d = os.path.join(OUT, sh["name"]); os.makedirs(d, exist_ok=True)
        frames = [int(n * AT)] if AT is not None else list(range(0, n, STEP))
        for f in frames:
            fn = os.path.join(d, f"f_{f:04d}.{ext}")
            if os.path.exists(fn):
                continue
            sc.frame_set(f); sc.render.filepath = fn
            bpy.ops.render.render(write_still=True)
        msg = f"{sh['name']}: {len(frames)} frames {W}x{H} s{SAMPLES} in {time.time() - t0:.0f}s"
        print(msg, flush=True); log.write(msg + "\n"); log.flush()
