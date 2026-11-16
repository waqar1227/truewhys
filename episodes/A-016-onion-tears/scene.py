"""A-016 Style R scenes (Blender). Renders every shot of shots.json as PNG frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur]
Kaggle: blender -b --python scene.py -- <same args>. Needs MPFB 2.0.18 installed (docs/audit/style_r/install_mpfb.py).
Every shot: studio backdrop in our colours, one hero prop, characters move (IK hands, head look, expression keys, blinks).
"""
import sys, os, json, math, time, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
PLAN, OUT = argv[0], argv[1]
def opt(k, d=None, f=str):
    return f(argv[argv.index(k) + 1]) if k in argv else d
W, H, SAMPLES, STEP = opt("--w", 540, int), opt("--h", 960, int), opt("--samples", 12, int), opt("--step", 1, int)
AT = opt("--at", None, float); ONLY = opt("--shots", None); GPU = "--gpu" in argv; MBLUR = "--mblur" in argv; PART = opt("--part", "0/1")
plan = json.load(open(PLAN)); FPS = plan["fps"]

MAN = dict(macro={"gender": 1, "age": 0.46, "muscle": 0.55, "weight": 0.5, "proportions": 0.6, "height": 0.55}, skin="#EBB894",
           hair="#2A170C", shirt="#4C7A5B", trousers="#3A3F4A", shoes="#3A2A20", iris="#5A3A22")
SCI = dict(macro={"gender": 0, "age": 0.4, "muscle": 0.5, "weight": 0.45, "proportions": 0.65, "height": 0.45}, skin="#F2C8AE",
           hair="#3A2214", hair_style="bun", shirt="#F4F6F8", trousers="#2B3440", shoes="#FFF4E0", iris="#3E2A1E", sleeve="long")
TOP = 0.92
BOARD = Vector((0, -0.42, TOP)); ONION = Vector((0, -0.42, TOP + 0.024))


# ------------------------------------------------------------------ helpers
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


def kitchen(man=True, onion_gap=0.03, bg=("#14213D", "#FF6B5B")):
    P.world(bg[0], 0.3); P.studio(top=bg[0], bottom=bg[1], y0=1.4)
    P.counter((0, -0.75, 0), w=1.4, d=0.55, top="#F1E8DA", top2="#E6D8C4")
    P.board(BOARD)
    halves = P.onion(ONION, cut=True, gap=onion_gap)
    h = ct = None
    if man:
        h = Hm.build(dict(MAN, loc=(0, -0.08, 0)), "man"); ct = Hm.controls(h)
        ct["handR"].location = (-0.03, -0.27, TOP + 0.08); ct["handL"].location = (0.10, -0.44, TOP + 0.07)
        ct["look"].location = (0, -0.42, TOP)
    kn = P.knife((0, 0, 0), (0, 0, 0))
    if man:
        kn.rotation_euler = (math.radians(0), 0, math.radians(-90)); Hm.hold(h, kn, "R", offset=(0, -0.062, 0.0))
        Hm.grip(h, "R", 0.85, 0.6); Hm.grip(h, "L", 0.35, 0.3)
    else:
        kn.location = (-0.16, -0.36, TOP + 0.03); kn.rotation_euler = (math.radians(90), 0, math.radians(-75))
    P.lights((0, -0.35, TOP + 0.25), key=900, rim=800, scale=0.8)
    return h, ct, halves, kn


def chop_keys(ct, f0, n_chops=2, period=12, x=-0.03):
    """Right hand chops straight down through the onion (blade along -Y crosses the onion at x ~ 0)."""
    hi, lo = TOP + 0.17, TOP + 0.045
    f = f0
    for k in range(n_chops):
        key_obj(ct["handR"], f, loc=(x, -0.27, hi)); key_obj(ct["handR"], f + period // 2, loc=(x, -0.27, lo)); f += period
    key_obj(ct["handR"], f, loc=(x, -0.27, hi * 0.6 + lo * 0.4))


def split_halves(halves, f0, f1, gap0=0.004, gap1=0.035):
    for o, s in ((halves[0], -1), (halves[1], 1)):
        x0 = o.location.x
        key_obj(o, f0, loc=(ONION.x + s * gap0 / 2, o.location.y, o.location.z), rot=(0, 0, 0))
        key_obj(o, f1, loc=(ONION.x + s * gap1 / 2, o.location.y, o.location.z), rot=(0, s * math.radians(-14), 0))


def tear_on(h, side_x, f0, f1, name="tear"):
    """Tear that wells at the lower lid and runs down the cheek (parented to the head bone)."""
    ec, r = h["eye_c"], h["eye_r"]
    t = P.tear((ec.x + side_x * r * 2.6, ec.y - r * 0.9, ec.z - r * 1.1), r * 0.35, name)
    rig = h["rig"]; mw = t.matrix_world.copy(); t.parent = rig; t.parent_type = "BONE"; t.parent_bone = "head"; t.matrix_world = mw
    t.delta_scale = (0.0, 0.0, 0.0); t.keyframe_insert("delta_scale", frame=f0)
    t.delta_scale = (1.0, 1.0, 1.0); t.keyframe_insert("delta_scale", frame=f0 + 6)
    t.delta_location = (0, 0, 0); t.keyframe_insert("delta_location", frame=f0 + 6)
    t.delta_location = (0, -r * 3.5, -r * 0.3); t.keyframe_insert("delta_location", frame=f1)
    return t


def life(h, n, seed=1, blinks=True):
    """Small idle life: blinks every ~1.5-2.5 s."""
    if not blinks:
        return
    rnd = random.Random(seed); f = rnd.randint(8, 20)
    while f < n - 6:
        Hm.blink(h["keys"], f); f += rnd.randint(40, 70)


# ------------------------------------------------------------------ shots
def hook_cut(sh, cam, n):
    h, ct, halves, kn = kitchen(onion_gap=0.004)
    chop_keys(ct, 0, n_chops=2, period=14)
    split_halves(halves, 7, 16)
    Hm.face(h["keys"], 0, squint=0.3, brows_inner=0.2); Hm.face(h["keys"], 18, squint=0.85, brows_inner=0.7, frown=0.4, sneer=0.3)
    key_obj(ct["look"], 0, loc=(0, -0.42, TOP)); key_obj(ct["look"], n, loc=(0.02, -0.5, TOP + 0.05))
    tear_on(h, 1, 14, n)
    gp = P.gas_puffs(ONION + Vector((0, 0, 0.06)), n=26, spread=0.03, size=0.008)
    puffs_rise(gp, n, ONION + Vector((0, 0, 0.05)), TOP + 0.45, drift=(0.02, 0.06), t0=10, speed=0.8)
    cam_move(cam, n, ((0.26, -1.08, TOP + 0.40), (0.0, -0.30, TOP + 0.42), 40), ((0.23, -1.0, TOP + 0.41), (0.0, -0.30, TOP + 0.43), 42),
             focus=(0, -0.3, TOP + 0.3), fstop=8)
    life(h, n, blinks=False)


def fight_back(sh, cam, n):
    h, ct, halves, kn = kitchen(onion_gap=0.035)
    key_obj(ct["handR"], 0, loc=(-0.03, -0.27, TOP + 0.10)); key_obj(ct["handR"], n, loc=(-0.12, -0.22, TOP + 0.16))
    key_obj(ct["look"], 0, loc=(0, -0.5, TOP + 0.05)); key_obj(ct["look"], 14, loc=(0.05, -1.0, TOP + 0.55))   # leans back, looks away
    rig = h["rig"]; key_obj(rig, 0, loc=(0, 0, 0)); key_obj(rig, 14, loc=(0, 0.05, 0))
    Hm.face(h["keys"], 0, squint=0.85, brows_inner=0.7, frown=0.4); Hm.face(h["keys"], 12, close=0.75, squint=1.0, brows_down=0.6, frown=0.6, sneer=0.6)
    tear_on(h, 1, 0, n); tear_on(h, -1, 10, n, "tear2")
    gp = P.gas_puffs(ONION, n=46, spread=0.04, size=0.009)
    puffs_rise(gp, n, ONION + Vector((0, 0, 0.05)), TOP + 0.62, drift=(0.0, 0.25), speed=1.2)
    cam_move(cam, n, ((0.23, -1.0, TOP + 0.41), (0.0, -0.30, TOP + 0.43), 42), ((0.16, -0.90, TOP + 0.42), (0.0, -0.20, TOP + 0.48), 48),
             focus=(0, -0.2, TOP + 0.5), fstop=8)


def slice_macro(sh, cam, n):
    h, ct, halves, kn = kitchen(man=False, onion_gap=0.04)
    # the left half lies cut-face up; the knife slices it, cells burst as glints
    halves[0].rotation_euler = (0, math.radians(-90), 0); halves[0].location = (ONION.x - 0.05, ONION.y, TOP + 0.024 + 0.045)
    kx = ONION.x - 0.05 - 0.12
    kn.rotation_euler = (0, 0, 0)
    key_obj(kn, 0, loc=(kx, ONION.y + 0.01, TOP + 0.20)); key_obj(kn, 9, loc=(kx, ONION.y + 0.01, TOP + 0.075))
    key_obj(kn, 22, loc=(kx, ONION.y - 0.012, TOP + 0.20)); key_obj(kn, 31, loc=(kx, ONION.y - 0.012, TOP + 0.075))
    gp = P.gas_puffs(halves[0].location, n=30, spread=0.025, size=0.006, color="#FFF6C8")
    puffs_rise(gp, n, Vector(halves[0].location) + Vector((0, 0, 0.04)), TOP + 0.25, t0=9, speed=0.9)
    loc = Vector(halves[0].location)
    cam_move(cam, n, ((loc.x + 0.03, loc.y - 0.12, loc.z + 0.24), (loc.x, loc.y, loc.z + 0.03), 55),
             ((loc.x + 0.02, loc.y - 0.09, loc.z + 0.19), (loc.x, loc.y, loc.z + 0.03), 65), focus=loc + Vector((0, 0, 0.045)), fstop=5.6)


def _cells(n, mix_at=None, bg=("#14213D", "#3A2A6E")):
    P.world(bg[0], 0.3); P.studio(top=bg[0], bottom=bg[1], y0=2.5)
    cs = P.cells((0, 0, 0.35), nx=6, nz=5, s=0.5)
    P.lights((0, 0, 1.3), key=1100, rim=900, scale=1.2)
    rnd = random.Random(4)
    for i, (ch, en, cell) in enumerate(zip(cs["chem"], cs["enz"], cs["cells"])):
        ph = rnd.random() * 6
        c0, e0 = Vector(ch.location), Vector(en.location)
        for f in range(0, n + 1, 4):
            if mix_at is None or f < mix_at:
                key_obj(ch, f, loc=c0 + Vector((0, 0, 0.02 * math.sin(f * 0.15 + ph))))
                key_obj(en, f, loc=e0 + Vector((0, 0, 0.02 * math.sin(f * 0.13 + ph + 1))))
        if mix_at is not None:
            m = (c0 + e0) / 2
            f1 = mix_at + 6 + int(rnd.random() * 6)
            key_obj(cell, mix_at, scale=cell.scale[:], rot=(0, 0, 0))
            key_obj(cell, f1, scale=(0.0, 0.0, 0.0), rot=(0.4 * rnd.random(), 0, 0.6 * (rnd.random() - 0.5)))
            key_obj(ch, f1, loc=m + Vector((-0.03, -0.05, 0)), scale=(1.4, 1.0, 1.2)); key_obj(en, f1, loc=m + Vector((0.03, -0.05, 0)), scale=(1.4, 1.0, 1.2))
            key_obj(ch, n, loc=m + Vector((-0.01, -0.06, 0.08)), scale=(1.6, 1.2, 1.4)); key_obj(en, n, loc=m + Vector((0.01, -0.06, 0.09)), scale=(1.6, 1.2, 1.4))
    return cs


def cells_apart(sh, cam, n):
    _cells(n)
    cam_move(cam, n, ((-0.7, -2.4, 1.2), (-0.3, 0, 1.1), 48), ((0.4, -2.1, 1.15), (0.2, 0, 1.1), 52), fstop=8)


def cells_mix(sh, cam, n):
    _cells(n, mix_at=2)
    cam_move(cam, n, ((0.4, -2.1, 1.15), (0.2, 0, 1.1), 52), ((0.3, -1.7, 1.2), (0.2, 0, 1.15), 55), fstop=8)


def gas_rise(sh, cam, n):
    h, ct, halves, kn = kitchen(man=False, onion_gap=0.04)
    gp = P.gas_puffs(ONION, n=80, spread=0.035, size=0.010)
    puffs_rise(gp, n, ONION + Vector((0, 0, 0.05)), TOP + 0.55, speed=1.4)
    cam_move(cam, n, ((0.22, -0.68, TOP + 0.06), (0, -0.42, TOP + 0.10), 40), ((0.20, -0.64, TOP + 0.10), (0, -0.42, TOP + 0.22), 40), fstop=4)


def gas_to_eyes(sh, cam, n):
    h, ct, halves, kn = kitchen(onion_gap=0.035)
    key_obj(ct["handR"], 0, loc=(-0.05, -0.27, TOP + 0.08))
    ec = h["eye_c"]
    key_obj(ct["look"], 0, loc=(0, -0.45, TOP)); key_obj(ct["look"], n, loc=(0.0, -0.6, TOP + 0.1))
    fs = W_(sh, "straight", 1.0)
    Hm.face(h["keys"], 0, squint=0.2); Hm.face(h["keys"], fs, squint=0.4); Hm.face(h["keys"], fs + 8, squint=1.0, brows_inner=0.8, frown=0.4, sneer=0.4)
    Hm.blink(h["keys"], fs + 2, 7)
    gp = P.gas_puffs(ONION, n=60, spread=0.03, size=0.009)
    puffs_rise(gp, n, ONION + Vector((0, 0, 0.05)), ec.z, target=(ec.x, ec.y - 0.06, ec.z), speed=1.1)
    cam_move(cam, n, ((0.20, -0.78, TOP + 0.10), (0, -0.42, TOP + 0.08), 38), ((0.16, -0.62, ec.z - 0.02), (ec.x, ec.y, ec.z - 0.01), 45),
             focus=(ec.x, ec.y, ec.z), fstop=4)


def _eye(n, hit_at=0, alarm_at=None, tears_at=None):
    P.world("#14213D", 0.3); P.studio(top="#14213D", bottom="#1F3A68", y0=1.5)
    e = P.eye_macro((0, 0, 1.0), R=0.5, iris="#5A3A22")
    P.lights((0, 0, 1.0), key=900, rim=700, scale=1.0)
    gp = P.gas_puffs((0, -1.2, 0.4), n=18, spread=0.18, size=0.035)
    puffs_rise(gp, n, Vector((0.25, -0.9, 0.35)), 1.25, target=(0.0, -0.6, 1.0), speed=0.9, t0=hit_at, spread=0.15)
    em = e["nerve_mat"].node_tree.nodes["Emission"].inputs["Strength"]
    em.default_value = 0.0; em.keyframe_insert("default_value", frame=0)
    if alarm_at is not None:
        red = C.area("alarm", (0.0, -1.6, 1.0), (math.radians(90), 0, 0), 1.5, "#FF3B30", 0.0)
        for k in range(4):
            f = alarm_at + k * 9
            em.default_value = 0.5 if k == 0 else 3.0; em.keyframe_insert("default_value", frame=max(0, f - 1))
            em.default_value = 9.0; em.keyframe_insert("default_value", frame=f + 2)
            red.data.energy = 0.0; red.data.keyframe_insert("energy", frame=max(0, f - 1))
            red.data.energy = 900.0; red.data.keyframe_insert("energy", frame=f + 2)
            red.data.energy = 100.0; red.data.keyframe_insert("energy", frame=f + 7)
    else:
        em.default_value = 1.5; em.keyframe_insert("default_value", frame=n)
    if tears_at is not None:
        g = e["gland"]; s0 = g.scale[:]
        for k in range(3):
            f = tears_at + k * 10
            key_obj(g, f, scale=s0); key_obj(g, f + 4, scale=(s0[0] * 1.25, s0[1] * 1.15, s0[2] * 1.2)); key_obj(g, f + 9, scale=s0)
        rnd = random.Random(2)
        for k in range(7):
            x = -0.32 + 0.11 * k + rnd.uniform(-0.02, 0.02)
            t = P.tear((x, -0.55, 0.72), 0.045 + 0.02 * rnd.random(), f"tear{k}")
            f0 = tears_at + 3 + k * 4
            key_obj(t, 0, scale=0.0); key_obj(t, f0, scale=0.0); key_obj(t, f0 + 6, scale=1.0, loc=(x, -0.6, 0.70))
            key_obj(t, min(n, f0 + 40), loc=(x + 0.02, -0.75, 0.05))
    return e


def eye_hit(sh, cam, n):
    _eye(n, hit_at=0)
    cam_move(cam, n, ((0.4, -2.05, 1.05), (0, 0, 1.0), 45), ((0.25, -1.8, 1.02), (0, 0, 1.0), 48), fstop=8)


def eye_alarm(sh, cam, n):
    _eye(n, hit_at=0, alarm_at=max(2, W_(sh, "alarm", 0.6) - 4))
    cam_move(cam, n, ((0.2, -1.5, 1.02), (0, 0, 1.0), 48), ((0.1, -1.3, 1.0), (0, 0, 1.0), 52), fstop=8)


def tears(sh, cam, n):
    _eye(n, alarm_at=None, tears_at=max(2, W_(sh, "flood", 0.4) - 3))
    cam_move(cam, n, ((-0.3, -1.6, 1.1), (-0.1, 0, 0.85), 45), ((-0.35, -1.75, 1.0), (-0.1, 0, 0.78), 43), fstop=8)


def flask(loc, glow=0.0):
    g = C.cyl("flask_neck", 0.012, 0.06, (loc[0], loc[1], loc[2] + 0.11), mat=C.glass("labglass", refl=0.12), verts=32)
    bpy.ops.mesh.primitive_cone_add(radius1=0.045, radius2=0.013, depth=0.09, location=(loc[0], loc[1], loc[2] + 0.045), vertices=48)
    b = bpy.context.object; b.data.materials.append(C.glass("labglass", refl=0.12))
    liq = C.pbr("enzyme_liquid", "#59D18C", 0.1, emit="#59D18C", estr=glow, coat=1.0)
    bpy.ops.mesh.primitive_cone_add(radius1=0.040, radius2=0.022, depth=0.045, location=(loc[0], loc[1], loc[2] + 0.024), vertices=48)
    l = bpy.context.object; l.data.materials.append(liq)
    for o in (g, b, l):
        for p in o.data.polygons:
            p.use_smooth = True
    root = bpy.data.objects.new("flask", None); bpy.context.scene.collection.objects.link(root); root.location = loc
    for o in (g, b, l):
        mw = o.matrix_world.copy(); o.parent = root; o.matrix_world = mw
    return root, liq


def lab(n, face_keys=None):
    P.world("#14213D", 0.25); P.studio(top="#14213D", bottom="#E9A27A", mid="#3A3F6B", glow=0.18, y0=1.4)
    P.counter((0, -0.75, 0), w=1.4, d=0.55, top="#FAFAF7", top2="#EEF0F2", body="#E9ECEF")
    halves = P.onion(ONION + Vector((0.18, 0, -0.024)), cut=True, gap=0.03)
    h = Hm.build(dict(SCI, loc=(0, -0.08, 0)), "sci"); ct = Hm.controls(h)
    fl, liq = flask((0, 0, 0), glow=4.0)
    Hm.hold(h, fl, "R", offset=(0, 0, -0.06)); Hm.grip(h, "R", 0.7, 0.5); Hm.grip(h, "L", 0.3, 0.3)
    ct["handL"].location = (0.16, -0.40, TOP + 0.05)
    P.lights((0, -0.35, TOP + 0.35), key=650, rim=800, fill=150, scale=0.8)
    return h, ct, fl, halves


def lab_2002(sh, cam, n):
    h, ct, fl, halves = lab(n)
    key_obj(ct["handR"], 0, loc=(-0.10, -0.36, TOP + 0.06)); key_obj(ct["handR"], n, loc=(-0.08, -0.40, TOP + 0.30))
    ec = h["eye_c"]
    key_obj(ct["look"], 0, loc=(0.18, -0.42, TOP)); key_obj(ct["look"], int(n * 0.6), loc=(-0.08, -0.45, TOP + 0.30))
    Hm.face(h["keys"], 0, brows_up=0.1); Hm.face(h["keys"], int(n * 0.6), brows_up=0.6, smile=0.3, wide=0.3)
    life(h, n, 3)
    cam_move(cam, n, ((0.12, -1.25, TOP + 0.36), (0, -0.2, TOP + 0.36), 40), ((0.07, -1.12, TOP + 0.38), (0, -0.2, TOP + 0.38), 43), focus=(0, -0.15, TOP + 0.5), fstop=8)


def lab_flask(sh, cam, n):
    h, ct, fl, halves = lab(n)
    key_obj(ct["handR"], 0, loc=(-0.13, -0.40, TOP + 0.22)); key_obj(ct["handR"], n, loc=(-0.12, -0.42, TOP + 0.25))
    ec = h["eye_c"]
    key_obj(ct["look"], 0, loc=(-0.05, -0.45, TOP + 0.38))
    Hm.face(h["keys"], 0, brows_up=0.6, smile=0.3, wide=0.3); Hm.face(h["keys"], n, brows_up=0.8, smile=0.6, wide=0.4)
    life(h, n, 4)
    tgt = Vector((-0.06, -0.40, TOP + 0.32))
    cam_move(cam, n, ((0.10, -0.95, TOP + 0.38), tgt + Vector((0, 0, 0.06)), 50), ((0.06, -0.85, TOP + 0.40), tgt + Vector((0, 0, 0.07)), 55), focus=tgt, fstop=8)


def prize(sh, cam, n):
    h, ct, fl, halves = lab(n)
    key_obj(ct["handR"], 0, loc=(-0.14, -0.30, TOP + 0.05))
    key_obj(ct["look"], 0, loc=(0.0, -0.6, TOP + 0.55))
    Hm.face(h["keys"], 0, brows_up=0.5, smile=0.4); Hm.face(h["keys"], W_(sh, "prize", 1.2), smile=1.0, brows_up=0.7, wide=0.2)
    life(h, n, 5)
    ec = h["eye_c"]
    md = P.medal((0, -0.55, TOP + 0.20), r=0.07)
    root = bpy.data.objects.new("medal_root", None); bpy.context.scene.collection.objects.link(root); root.location = (0, -0.55, TOP + 0.20)
    for o in md:
        mw = o.matrix_world.copy(); o.parent = root; o.matrix_world = mw
    fi = W_(sh, "ig", 0.5)
    key_obj(root, 0, loc=(0, -0.55, TOP - 0.25), rot=(0, 0, 0)); key_obj(root, fi + 6, loc=(0, -0.55, ec.z - 0.30), rot=(0, 0, math.radians(360)))
    key_obj(root, n, loc=(0, -0.55, ec.z - 0.27), rot=(0, 0, math.radians(400)))
    rnd = random.Random(8)
    for k in range(40):   # confetti in our palette
        col = rnd.choice(["#FF6B5B", "#FFC93C", "#59D18C", "#5BC0EB", "#FFF1DC"])
        c = C.rbox(f"conf{k}", (0.012, 0.004, 0.018), (0, 0, 0), mat=C.pbr(f"conf_{col}", col, 0.4), bevel=0.001)
        x, y = rnd.uniform(-0.45, 0.45), rnd.uniform(-0.8, -0.2)
        f0 = fi + rnd.randint(0, 10)
        key_obj(c, 0, loc=(x, y, ec.z + 0.6), scale=0.0); key_obj(c, f0, loc=(x, y, ec.z + 0.6), scale=1.0, rot=(0, 0, 0))
        key_obj(c, n, loc=(x + rnd.uniform(-0.1, 0.1), y, ec.z + 0.6 - 0.9 * (n - f0) / FPS), rot=(rnd.uniform(0, 9), rnd.uniform(0, 9), 0))
    cam_move(cam, n, ((0.05, -1.25, ec.z - 0.15), (0, -0.3, ec.z - 0.15), 40), ((0.02, -1.12, ec.z - 0.14), (0, -0.3, ec.z - 0.14), 43), focus=(0, -0.3, ec.z - 0.2), fstop=8)


def wipe(sh, cam, n):
    h, ct, halves, kn = kitchen(onion_gap=0.035)
    ec = h["eye_c"]
    key_obj(ct["handR"], 0, loc=(-0.10, -0.25, TOP + 0.06))
    key_obj(ct["handL"], 0, loc=(0.10, -0.44, TOP + 0.07)); key_obj(ct["handL"], 12, loc=(ec.x + 0.05, ec.y - 0.07, ec.z - 0.02))
    key_obj(ct["handL"], 22, loc=(ec.x + 0.01, ec.y - 0.07, ec.z - 0.03)); key_obj(ct["handL"], 32, loc=(ec.x + 0.05, ec.y - 0.07, ec.z - 0.02))
    key_obj(ct["handL"], n, loc=(0.12, -0.35, TOP + 0.20))
    key_obj(ct["look"], 0, loc=(0.1, -1.0, ec.z - 0.1)); key_obj(ct["look"], n, loc=(0.0, -1.0, ec.z))
    Hm.face(h["keys"], 0, squint=0.9, frown=0.5, brows_inner=0.7); Hm.face(h["keys"], n, squint=0.4, frown=0.2, brows_inner=0.4, smile=0.15)
    tear_on(h, -1, 0, n)
    cam_move(cam, n, ((0.22, -1.15, ec.z - 0.12), (0, -0.1, ec.z - 0.14), 45), ((0.16, -1.02, ec.z - 0.10), (0, -0.1, ec.z - 0.12), 50), focus=(0, -0.12, ec.z), fstop=8)


def defence(sh, cam, n):
    h, ct, halves, kn = kitchen(man=False, onion_gap=0.035)
    gp = P.gas_puffs(ONION, n=70, spread=0.02, size=0.009, color="#B9F5C9")
    rnd = random.Random(6)
    for i, p in enumerate(gp):   # puffs orbit the onion like a shield
        r = 0.08 + 0.04 * rnd.random(); ph = rnd.random() * 6.28; zz = rnd.uniform(0.0, 0.11); sp = rnd.uniform(0.08, 0.14)
        for f in range(0, n + 1, 2):
            a = ph + f * sp
            key_obj(p, f, loc=(ONION.x + r * math.cos(a), ONION.y + r * math.sin(a), ONION.z + zz + 0.01 * math.sin(f * 0.2 + i)),
                    scale=min(1.0, f / 8.0) * 1.2)
    cam_move(cam, n, ((0.28, -0.72, TOP + 0.16), (0, -0.42, TOP + 0.06), 40), None, orbit=-30, fstop=4)


def loop_q(sh, cam, n):
    h, ct, halves, kn = kitchen(onion_gap=0.035)
    key_obj(ct["handR"], 0, loc=(-0.03, -0.27, TOP + 0.06))
    Hm.hold(h, halves[1], "L", offset=(0, 0, -0.035)); Hm.grip(h, "L", 0.6, 0.5)
    key_obj(ct["handL"], 0, loc=(0.10, -0.42, TOP + 0.07)); key_obj(ct["handL"], 16, loc=(0.13, -0.40, TOP + 0.30))
    key_obj(ct["look"], 0, loc=(0.1, -0.5, TOP + 0.2)); key_obj(ct["look"], 14, loc=(0.25, -1.4, TOP + 0.55))
    Hm.face(h["keys"], 0, squint=0.4, brows_inner=0.3); Hm.face(h["keys"], 16, browL_up=0.9, smile=0.35, squint=0.2)
    life(h, n, 6)
    cam_move(cam, n, ((0.23, -1.0, TOP + 0.41), (0.0, -0.30, TOP + 0.43), 42), ((0.26, -1.08, TOP + 0.40), (0.0, -0.30, TOP + 0.42), 40),
             focus=(0, -0.3, TOP + 0.3), fstop=8)


SHOTS = {f.__name__: f for f in (hook_cut, fight_back, slice_macro, cells_apart, cells_mix, gas_rise, gas_to_eyes, eye_hit, eye_alarm, tears,
                                 lab_2002, lab_flask, prize, wipe, defence, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
