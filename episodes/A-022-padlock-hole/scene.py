"""A-022 Style R scenes (Blender): "What's this tiny hole in a padlock for?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Our own generic brass padlock (no brand), a hero-size cutaway (water, rust, ice, drain), a garden gate in the rain, our MPFB cast, studio backdrop.
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import key_obj, cam_move, W_, life

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

GAR = dict(macro={"gender": 1, "age": 0.62, "muscle": 0.5, "weight": 0.6, "proportions": 0.55, "height": 0.5}, skin="#E8B48E",
           hair="#8A8178", shirt="#2F7D4F", trousers="#3A4A66", shoes="#5B3B2E", iris="#3E5A7A", sleeve="long")   # older gardener, green top
BW, BT, BH = 0.05, 0.022, 0.045          # padlock body (m, real size)
DRAIN_X = 0.0135
BRASS, STEEL = "#C9A23A", "#C0C4CC"


def mats():
    return dict(brass=C.pbr("brass", BRASS, 0.32, metal=0.95, bump="noise", bstr=0.05),
                cut=C.pbr("brasscut", "#E3C46A", 0.25, metal=0.9),
                steel=C.pbr("steel", STEEL, 0.22, metal=1.0),
                dark=C.pbr("holedark", "#060606", 0.9),
                plug=C.pbr("plug", "#D8B860", 0.3, metal=0.9),
                rust=C.pbr("rust", "#8A3B12", 0.95, bump="noise", bstr=0.7, cvar=0.4, color2="#B45A22"),
                water=C.glass("water", tint=(0.55, 0.78, 1.0), refl=0.05),
                ice=P.ice_mat("ice", cloud=0.6))


def shackle_pts(lift=0.0):
    r = 0.0145; top = 0.04 + lift; pts = [(-r, 0, 0.006 + lift), (-r, 0, top)]
    pts += [(-r * math.cos(a), 0, top + r * math.sin(a)) for a in [i * math.pi / 14 for i in range(1, 14)]]
    pts += [(r, 0, top), (r, 0, 0.012 + lift)]
    return pts


def padlock(name="lock", s=1.0, loc=(0, 0, 0), rot=(0, 0, 0), cut=False):
    """Padlock at real size scaled by s. Local frame: X width, Y thickness (front face -Y), Z up (bottom face has keyway + drain hole).
    cut=True: front half removed, shows the cavity, plug, shackle legs and locking balls. Returns dict of parts (and the root)."""
    M = mats()
    root = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(root)
    out = dict(root=root, M=M)
    def add(o):
        o.parent = root; return o
    if not cut:
        add(C.rbox(name + "_body", (BW, BT, BH), (0, 0, 0), mat=M["brass"], bevel=0.004))
    else:
        add(C.rbox(name + "_back", (BW, 0.005, BH), (0, BT / 2 - 0.0025, 0), mat=M["brass"], bevel=0.0))
        for sx in (-1, 1):
            add(C.rbox(name + "_side", (0.007, BT, BH), (sx * (BW / 2 - 0.0035), 0, 0), mat=M["brass"], bevel=0.0))
        add(C.rbox(name + "_top", (BW, BT, 0.007), (0, 0, BH / 2 - 0.0035), mat=M["brass"], bevel=0.0))
        # bottom wall in two pieces leaving the drain channel open at DRAIN_X
        l0, l1 = -BW / 2, DRAIN_X - 0.0016; r0, r1 = DRAIN_X + 0.0016, BW / 2
        add(C.rbox(name + "_botL", (l1 - l0, BT, 0.007), ((l0 + l1) / 2, 0, -BH / 2 + 0.0035), mat=M["brass"], bevel=0.0))
        add(C.rbox(name + "_botR", (r1 - r0, BT, 0.007), ((r0 + r1) / 2, 0, -BH / 2 + 0.0035), mat=M["brass"], bevel=0.0))
        # bright cut faces on the front edges
        for (sx, w) in ((-1, 0.007), (1, 0.007)):
            add(C.rbox(name + "_cutface", (w, 0.0006, BH), (sx * (BW / 2 - 0.0035), -BT / 2 - 0.0003, 0), mat=M["cut"], bevel=0.0))
        iw = BW - 0.014
        add(C.rbox(name + "_cutface", (iw, 0.0006, 0.007), (0, -BT / 2 - 0.0003, BH / 2 - 0.0035), mat=M["cut"], bevel=0.0))
        add(C.rbox(name + "_cutface", (l1 - l0 - 0.007, 0.0006, 0.007), ((l0 + 0.007 + l1) / 2, -BT / 2 - 0.0003, -BH / 2 + 0.0035), mat=M["cut"], bevel=0.0))
        add(C.rbox(name + "_cutface", (r1 - r0 - 0.007, 0.0006, 0.007), ((r0 + r1 - 0.007) / 2, -BT / 2 - 0.0003, -BH / 2 + 0.0035), mat=M["cut"], bevel=0.0))
        out["plug"] = add(C.cyl(name + "_plug", 0.0075, 0.026, (-0.006, 0.001, -0.007), mat=M["plug"], verts=32, bevel=0.0008))
        out["pins"] = [add(C.cyl(name + "_pin", 0.0013, 0.009, (-0.006 + 0.006, 0.001, -0.015 + 0.0055 * k), rot=(0, math.radians(90), 0), mat=M["steel"], verts=12))
                       for k in range(4)]
        out["balls"] = [add(C.cyl(name + "_ball", 0.0028, 0.0056, (sx * 0.0085, 0.001, 0.013), mat=M["steel"], verts=20, bevel=0.0027)) for sx in (-1, 1)]
    out["shackle"] = add(C.tube(name + "_shackle", shackle_pts(), 0.0035, mat=M["steel"]))
    add(C.rbox(name + "_keyway", (0.0028, 0.012, 0.0008), (-0.006, 0.001, -BH / 2 - 0.0001), mat=M["dark"], bevel=0.0))
    add(C.cyl(name + "_drain", 0.0013, 0.0009, (DRAIN_X, 0.001, -BH / 2 - 0.0001), mat=M["dark"], verts=20))
    root.scale = (s, s, s); root.location = loc; root.rotation_euler = [math.radians(a) for a in rot]
    return out


def stage(top="#1F4F5A", bottom="#F0E2C8", mid="#E7B07A", y0=3.0, flip=False):
    P.world(top, 0.6); cyc = P.studio(top=top, bottom=bottom, mid=mid, y0=y0, glow=0.55, height=12.0, width=30.0, depth=10.0)
    if flip:
        cyc.rotation_euler = (0, 0, math.pi)
    return cyc


HERO = 11.0                                 # hero-size cutaway / macro lock scale
HZ = 1.05                                   # hero lock centre height


def hero_set(cut=True, rot=(0, 0, 0)):
    stage()
    C.cyl("pedestal", 0.32, HZ - BH / 2 * HERO - 0.04, (0, 0.05, (HZ - BH / 2 * HERO - 0.04) / 2), mat=C.pbr("ped", "#F4F1EA", 0.4), verts=48, bevel=0.01)
    lk = padlock("lock", HERO, (0, 0, HZ), rot, cut=cut)
    P.lights((0, 0, HZ), key=1100, rim=1000, scale=1.1)
    return lk


def W2(lk, x, y, z):
    """hero-lock local metres -> world (lock not rotated)."""
    return (x * HERO, y * HERO, HZ + z * HERO)


def water_box(lk, h0=0.0, name="water"):
    """Water in the cavity bottom; returns (obj, set(f, h)) keying the level (local metres above the bottom wall)."""
    M = lk["M"]; zb = -BH / 2 + 0.007; w = BW - 0.014; d = BT - 0.006
    o = C.rbox(name, (w, d, 1.0), (0, -0.0005, zb + 0.5), mat=M["water"], bevel=0.0); o.parent = lk["root"]
    def setk(f, h):
        h = max(h, 0.00005); o.scale = (1, 1, h); o.location = (0, -0.0005, zb + h / 2)
        o.keyframe_insert("scale", frame=f); o.keyframe_insert("location", frame=f)
    setk(0, h0)
    return o, setk


def drops(n_drops, path_fn, n, t0, gap, dur, name="drop", r=0.0016, mat=None, parent=None):
    """Water drops along path_fn(u)->local point, each keyed over `dur` frames, starting t0 + i*gap; hidden (scale 0) outside."""
    out = []
    for i in range(n_drops):
        o = C.cyl(f"{name}{i}", r, 2 * r, (0, 0, 0), mat=mat, verts=16, bevel=r * 0.98)
        if parent: o.parent = parent
        a = t0 + i * gap; b = a + dur
        key_obj(o, 0, loc=path_fn(0), scale=0.0); key_obj(o, max(0, a - 1), loc=path_fn(0), scale=0.0)
        for k in range(0, 9):
            u = k / 8; key_obj(o, int(a + u * dur), loc=path_fn(u), scale=(1, 1, 1.0 + 0.6 * u))
        key_obj(o, b + 1, loc=path_fn(1.0), scale=0.0)
        out.append(o)
    return out


CUTCAM = ((0.0, -1.35, 1.12), (0.0, 0.0, HZ + 0.05), 52)


# ------------------------------------------------------------------ shots
def _gardener(n, lock_rot=(-60, 0, 0)):
    stage(top="#2E5E86", bottom="#E9C9A0")
    h = Hm.build(dict(GAR, loc=(0, 0, 0), rot_z=0), "man"); ct = Hm.controls(h)
    lk = padlock("lock", 1.7, (0, 0, 0), lock_rot)
    ct["handR"].location = (-0.16, -0.36, 1.27); ct["handL"].location = (0.2, -0.12, 0.9)
    Hm.grip(h, "R", 0.55, 0.45)
    Hm.hold(h, lk["root"], "R", offset=(0.02, -0.03, 0.035))
    P.lights((0, -0.3, 1.4), key=900, rim=900)
    return h, ct, lk


GCAM = ((0.02, -0.95, 1.40), (-0.07, -0.2, 1.47), 38)
GCAM2 = ((0.02, -0.87, 1.40), (-0.07, -0.2, 1.48), 41)


def hook_lock(sh, cam, n):
    """Frame 1: she holds a big brass padlock up to her eye, underside to us (keyway + a tiny second hole), squinting; it turns in her fingers."""
    h, ct, lk = _gardener(n)
    key_obj(ct["handR"], 0, loc=(-0.16, -0.36, 1.27)); key_obj(ct["handR"], n, loc=(-0.15, -0.38, 1.3))
    key_obj(ct["look"], 0, loc=(-0.15, -0.38, 1.3)); key_obj(ct["look"], n - 15, loc=(-0.15, -0.38, 1.3)); key_obj(ct["look"], n, loc=(0.1, -1.0, 1.5))
    Hm.face(h["keys"], 0, squint=0.6, brows_down=0.4, purse=0.3); Hm.face(h["keys"], n - 15, squint=0.5, brows_inner=0.5, purse=0.2)
    Hm.face(h["keys"], n, browL_up=0.8, squint=0.2, purse=0.0)
    life(h, n, 2, blinks=False)
    cam_move(cam, n, GCAM, GCAM2, focus=(-0.12, -0.3, 1.38), fstop=4.0)


def loop_q(sh, cam, n):
    """'Ever noticed it?': she looks at us, then back at the lock; ends on hook_lock's first frame."""
    h, ct, lk = _gardener(n)
    key_obj(ct["handR"], 0, loc=(-0.15, -0.38, 1.3)); key_obj(ct["handR"], n, loc=(-0.16, -0.36, 1.27))
    key_obj(ct["look"], 0, loc=(0.1, -1.0, 1.5)); key_obj(ct["look"], max(1, n - 12), loc=(0.1, -1.0, 1.5)); key_obj(ct["look"], n, loc=(-0.15, -0.38, 1.3))
    Hm.face(h["keys"], 0, smile=0.4, browL_up=0.6); Hm.face(h["keys"], n, squint=0.6, brows_down=0.4, purse=0.3, smile=0.0, browL_up=0.0)
    cam_move(cam, n, ((0.02, -0.89, 1.40), (-0.07, -0.2, 1.48), 40), GCAM, focus=(-0.12, -0.3, 1.38), fstop=4.0)


def macro_holes(sh, cam, n):
    """'It's not a keyhole': hero lock bottom-up; camera slides from the keyway to the tiny hole."""
    lk = hero_set(cut=False, rot=(-90, 0, 0))             # bottom faces -Y (camera)
    kx, dx = -0.006 * HERO, DRAIN_X * HERO; zc = HZ + 0.001 * HERO
    cam_move(cam, n, ((kx, -1.05, zc + 0.02), (kx, 0.0, zc), 50), ((dx, -0.95, zc + 0.02), (dx, 0.0, zc), 58), focus=(dx * 0.5, -0.25, zc), fstop=5.6)


def flip_bottom(sh, cam, n):
    """'That's why it sits at the bottom': hero lock turns from its front to its underside; the tiny hole ends up facing us."""
    lk = hero_set(cut=False)
    r = lk["root"]; f0 = 8; f1 = int(n * 0.55)
    key_obj(r, 0, rot=(0, 0, math.radians(-20))); key_obj(r, f0, rot=(0, 0, math.radians(-12)))
    key_obj(r, f1, rot=(math.radians(-90), 0, 0)); key_obj(r, n, rot=(math.radians(-90), 0, math.radians(4)))
    cam_move(cam, n, ((0.0, -1.5, HZ + 0.05), (0, 0, HZ), 46), ((0.04, -1.3, HZ + 0.03), (0.04, 0, HZ), 50), focus=(0, -0.2, HZ), fstop=6.3)


def cutaway_crack(sh, cam, n):
    """'...could break from the inside': the front of the lock slides away, an inside glows warning red."""
    lk = hero_set(cut=True)
    front = C.rbox("front", (BW, BT / 2, BH), (0, -BT / 4, 0), mat=lk["M"]["brass"], bevel=0.004); front.parent = lk["root"]
    fb = W_(sh, "break", 1.0)
    key_obj(front, 0, loc=(0, -BT / 4, 0)); key_obj(front, 6, loc=(0, -BT / 4, 0)); key_obj(front, 26, loc=(0, -BT / 4 - 0.06, 0.0))
    key_obj(front, 27, scale=1.0); key_obj(front, 34, scale=0.0)
    glow = C.area("warn", W2(lk, 0, -0.004, -0.004), (math.radians(90), 0, 0), 0.12, "#FF3020", 0.0)
    for f, e in ((0, 0), (max(1, fb - 4), 0), (fb + 2, 60), (fb + 10, 18), (fb + 18, 60), (n, 25)):
        glow.data.energy = e; glow.data.keyframe_insert("energy", frame=f)
    cam_move(cam, n, ((0.25, -1.5, 1.2), (0, 0, HZ + 0.05), 46), CUTCAM, focus=(0, -0.1, HZ), fstop=6.3)


def drip_in(sh, cam, n):
    """'Rain sneaks in around the shackle... and has nowhere to go': drops run in where the shackle enters, water pools inside."""
    lk = hero_set(cut=True)
    o, setk = water_box(lk)
    fn = W_(sh, "nowhere", 1.8)
    for f, h in ((0, 0.0), (10, 0.0), (fn, 0.005), (n, 0.0065)):
        setk(f, h)
    def path(sx):
        return lambda u: ((sx * 0.0145) + sx * 0.0005 * u, -0.004, 0.034 - 0.052 * u * u) if u > 0 else (sx * 0.0145, -0.004, 0.034)
    drops(6, path(-1), n, 4, 11, 16, name="dl", mat=lk["M"]["water"], parent=lk["root"])
    drops(6, path(1), n, 9, 11, 16, name="dr", mat=lk["M"]["water"], parent=lk["root"])
    cam_move(cam, n, ((0.0, -1.2, 1.32), (0, 0, HZ + 0.12), 54), ((0.0, -1.25, 1.12), (0, 0, HZ - 0.02), 52), focus=(0, -0.1, HZ), fstop=6.3)


def rust(sh, cam, n):
    """'Trapped water rusts the parts': rust creeps over the plug, pins, balls and shackle legs above the standing water."""
    lk = hero_set(cut=True)
    o, setk = water_box(lk, 0.0065)
    M = lk["M"]
    targets = [lk["plug"]] + lk["pins"] + lk["balls"]
    for i, t in enumerate(targets):
        c = t.copy(); c.data = t.data.copy(); c.data.materials.clear(); c.data.materials.append(M["rust"])
        bpy.context.scene.collection.objects.link(c); c.parent = lk["root"]
        s0 = c.scale.copy(); f = 4 + i * 3
        key_obj(c, 0, scale=(s0.x * 0.6, s0.y * 0.6, s0.z * 0.6)); key_obj(c, f, scale=(s0.x * 0.6, s0.y * 0.6, s0.z * 0.6))
        key_obj(c, f + 22, scale=(s0.x * 1.12, s0.y * 1.12, s0.z * 1.04))
    for pts in (shackle_pts()[:2], shackle_pts()[-2:]):
        sh2 = C.tube("shrust", [(x, y, min(z, 0.03)) for x, y, z in pts], 0.0039, mat=M["rust"]); sh2.parent = lk["root"]
        key_obj(sh2, 0, scale=(1, 1, 0.0)); key_obj(sh2, 12, scale=(1, 1, 0.0)); key_obj(sh2, 40, scale=(1, 1, 1))
    cam_move(cam, n, ((-0.12, -1.0, HZ + 0.02), (-0.06, 0, HZ - 0.05), 44), ((-0.1, -0.9, HZ + 0.01), (-0.06, 0, HZ - 0.05), 48), focus=(-0.06, -0.1, HZ - 0.05), fstop=6.3)


def gate(n, frost=False):
    """Garden gate with a hasp and a hanging padlock (s=1.8); returns (lock dict, staple point)."""
    wood = C.pbr("wood", "#7A5236", 0.7, bump="noise", bstr=0.25, cvar=0.2, color2="#5E3E28")
    for k in range(7):
        C.rbox("plank", (0.14, 0.035, 1.25), (-0.95 + k * 0.155, 0.02, 0.72), mat=wood, bevel=0.008)
    for z in (0.35, 1.1):
        C.rbox("rail", (1.1, 0.03, 0.12), (-0.48, -0.015, z), mat=wood, bevel=0.008)
    C.rbox("post", (0.14, 0.14, 1.6), (0.22, 0.04, 0.8), mat=wood, bevel=0.01)
    st = C.pbr("hasp", "#3A3D44", 0.4, metal=0.9)
    C.rbox("hasp", (0.2, 0.008, 0.05), (0.08, -0.04, 1.0), mat=st, bevel=0.003)
    ring = [(0.17 + 0.012 * math.cos(t), -0.05, 1.0 + 0.018 * math.sin(t)) for t in [i * 2 * math.pi / 24 for i in range(24)]]
    C.tube("staple", ring, 0.004, mat=st, closed=True)
    lk = padlock("lock", 1.8, (0.17, -0.055, 1.0 - 0.06), (0, 0, math.radians(8)))
    return lk


def gate_rain(sh, cam, n):
    """'Padlocks live outdoors': the gate in the rain, drops streaking (motion blur), water running off the lock."""
    stage(top="#22384F", bottom="#7D8A99", mid="#4F6276")
    lk = gate(n)
    P.lights((0, -0.2, 1.0), key=700, rim=1300, warm=False)
    rnd = random.Random(5); wm = C.pbr("rain", "#DDEEFF", 0.05, emit="#EAF4FF", estr=0.6)
    for i in range(260):
        x, y = rnd.uniform(-0.35, 0.7), rnd.uniform(-0.35, 0.3); z0 = rnd.uniform(1.6, 3.2); sp = rnd.uniform(0.09, 0.12)
        o = C.rbox("rd", (0.004, 0.004, 0.07), (x, y, z0), mat=wm, bevel=0.0)
        key_obj(o, 0, loc=(x, y, z0)); key_obj(o, n, loc=(x, y, z0 - sp * n))
    cam_move(cam, n, ((0.32, -0.78, 1.06), (0.17, -0.05, 0.95), 48), ((0.3, -0.7, 1.05), (0.17, -0.05, 0.95), 52), focus=(0.17, -0.06, 0.95), fstop=4.0)


def frozen(sh, cam, n):
    """'In winter it freezes, and the lock jams solid': frost on the lock, she tries the key, it won't turn."""
    stage(top="#3A5F86", bottom="#E8EEF4", mid="#B8CCE0")
    lk = gate(n)
    M = lk["M"]
    fm = C.pbr("frost", "#E6F2FF", 0.55, bump="noise", bstr=0.8, bscale=900.0, sss=0.3)
    frost = C.rbox("frost", (BW * 1.05, BT * 1.12, BH * 0.7), (0, 0, -BH * 0.17), mat=fm, bevel=0.006); frost.parent = lk["root"]
    for k, (x, L) in enumerate(((-0.018, 0.012), (-0.004, 0.02), (0.01, 0.009), (0.02, 0.015))):
        ic = C.cyl("icicle", 0.0002, L, (x, 0.0, -BH / 2 - L / 2), mat=M["ice"], verts=10, r2=0.0028); ic.parent = lk["root"]
    h = Hm.build(dict(GAR, loc=(-0.14, -0.47, 0), rot_z=144), "man"); ct = Hm.controls(h)
    key = C.rbox("key", (0.004, 0.022, 0.05), (0, 0, 0), mat=C.pbr("keymetal", "#C9CDD4", 0.25, metal=1.0), bevel=0.002)
    lw = lk["root"].matrix_world
    bpy.context.view_layer.update()
    kp = lk["root"].matrix_world @ Vector((-0.006, 0.001, -BH / 2 - 0.02))
    key.location = kp
    fj = W_(sh, "jams", 2.0)
    for f, dz in ((0, 0.0), (8, 0.0), (14, 0.01), (20, -0.005), (fj, -0.005), (fj + 4, 0.012), (fj + 9, -0.004), (n, 0.0)):
        key_obj(ct["handR"], f, loc=(kp.x - 0.02, kp.y - 0.03, kp.z - 0.02 + dz))
    key_obj(key, 0, rot=(0, 0, 0)); key_obj(key, 14, rot=(0, math.radians(8), 0)); key_obj(key, 18, rot=(0, math.radians(-2), 0))
    key_obj(key, fj + 4, rot=(0, math.radians(10), 0)); key_obj(key, fj + 9, rot=(0, 0, 0))
    ct["handL"].location = (-0.33, -0.33, 0.92)
    Hm.grip(h, "R", 0.7, 0.5)
    key_obj(ct["look"], 0, loc=tuple(kp)); key_obj(ct["look"], fj + 12, loc=(0.6, -2.0, 1.5))
    Hm.face(h["keys"], 0, squint=0.4, purse=0.3); Hm.face(h["keys"], fj + 4, squint=0.7, frown=0.6, brows_down=0.6, purse=0.0)
    Hm.face(h["keys"], fj + 12, frown=0.4, brows_inner=0.7, wide=0.2)
    P.lights((0, -0.3, 1.1), key=900, rim=1100, warm=False)
    cam_move(cam, n, ((0.78, -0.42, 1.32), (0.0, -0.28, 1.2), 32), ((0.74, -0.42, 1.32), (0.0, -0.28, 1.21), 35), focus=(-0.08, -0.4, 1.4), fstop=5.0)


def drain(sh, cam, n):
    """'It's a drain. Gravity pulls the water out': the level drops, drops fall out of the tiny hole at the bottom."""
    lk = hero_set(cut=True)
    o, setk = water_box(lk, 0.0065)
    fd = W_(sh, "drain", 0.3)
    for f, h in ((0, 0.0065), (fd, 0.0065), (int(n * 0.85), 0.0), (n, 0.0)):
        setk(f, h)
    def path(u):
        return (DRAIN_X, 0.0, -BH / 2 - 0.001 - 0.09 * u * u)
    drops(9, path, n, fd + 2, 9, 14, name="dd", r=0.0019, mat=lk["M"]["water"], parent=lk["root"])
    # puddle growing on the pedestal
    pud = C.cyl("puddle", 0.08, 0.002, (DRAIN_X * HERO, 0.0, HZ - BH / 2 * HERO - 0.04 + 0.001), mat=lk["M"]["water"], verts=40)
    key_obj(pud, 0, scale=0.0); key_obj(pud, fd + 10, scale=0.0); key_obj(pud, n, scale=(1, 1, 1))
    cam_move(cam, n, ((0.12, -1.35, HZ - 0.05), (0.06, 0, HZ - 0.1), 48), ((0.14, -1.25, HZ - 0.1), (0.08, 0, HZ - 0.16), 52), focus=(0.1, -0.1, HZ - 0.15), fstop=6.3)


SHOTS = {f.__name__: f for f in (hook_lock, macro_holes, cutaway_crack, gate_rain, drip_in, rust, frozen, flip_bottom, drain, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
