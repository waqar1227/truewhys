"""A-017 Style R scenes (Blender): renders every shot of shots.json as PNG frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --at 0.5 --shots a,b --gpu --part 0/2 --mblur]
Studio backdrop in our colours, one hero prop (the ice cube), cross-section diagram shots, the presenter moves (IK hands, look, face keys).
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import ease, key_obj, cam_move, W_, life, parent_keep, run

PRES = dict(macro={"gender": 0, "age": 0.42, "muscle": 0.5, "weight": 0.45, "proportions": 0.65, "height": 0.45}, skin="#F2C8AE",
            hair="#3A2214", hair_style="bun", shirt="#0F6B78", trousers="#2B3440", shoes="#FFF4E0", iris="#3E6E8E", loc=(0, -0.08, 0))
TOP = 0.92
TRAY = Vector((0.14, -0.40, TOP)); JUG = Vector((-0.20, -0.36, TOP))


def studio(bottom="#FF6B5B", glow=0.3):
    P.world("#14213D", 0.3); P.studio(top="#14213D", bottom=bottom, glow=glow, y0=1.4)


def counter_set(tray=True, jug=True, cloud=1.0):
    studio()
    P.counter((0, -0.75, 0), w=1.4, d=0.55, top="#F1E8DA", top2="#E6D8C4")
    if tray:
        P.ice_tray(TRAY, cloud=cloud)
    if jug:
        g = C.cyl("jug", 0.05, 0.16, (JUG.x, JUG.y, TOP + 0.08), mat=C.glass("jugglass", refl=0.12), verts=48, r2=0.045)
        w = C.cyl("jugwater", 0.046, 0.12, (JUG.x, JUG.y, TOP + 0.062), mat=P.ice_mat("water", 0.0), verts=48, r2=0.042)
    P.lights((0, -0.35, TOP + 0.3), key=850, rim=800, scale=0.8)


def presenter():
    h = Hm.build(PRES, "pres"); ct = Hm.controls(h)
    ct["handR"].location = (-0.12, -0.32, TOP + 0.05); ct["handL"].location = (0.14, -0.38, TOP + 0.05)
    ct["look"].location = (0, -0.45, TOP)
    return h, ct


def held_cube(h, cloud=1.0, side="R", s=0.045, bubbles=0):
    c, bs = P.ice_cube((0, 0, 0), s, cloud=cloud, bubbles=bubbles)
    c.rotation_euler = (0.3, 0.2, 0.4); Hm.hold(h, c, side, offset=(0, -0.01, 0.0)); Hm.grip(h, side, 0.55, 0.55)
    return c


def hook_cube(sh, cam, n):
    counter_set()
    h, ct = presenter(); ec = h["eye_c"]
    held_cube(h)
    hp = Vector((ec.x - 0.13, ec.y - 0.30, ec.z - 0.13))
    key_obj(ct["handR"], 0, loc=hp + Vector((0, 0, -0.03))); key_obj(ct["handR"], n, loc=hp)
    key_obj(ct["look"], 0, loc=hp + Vector((0, -0.2, 0)))
    Hm.face(h["keys"], 0, squint=0.4, brows_inner=0.6, frown=0.2); Hm.face(h["keys"], n, squint=0.6, brows_inner=0.8, frown=0.3, browL_up=0.4)
    life(h, n, 2)
    cam_move(cam, n, ((0.10, -0.95, ec.z - 0.08), (-0.04, -0.2, ec.z - 0.12), 42), ((0.08, -0.86, ec.z - 0.07), (-0.04, -0.2, ec.z - 0.11), 45),
             focus=hp, fstop=8)


def cube_macro(sh, cam, n):
    studio(bottom="#1F3A68", glow=0.25)
    c, bs = P.ice_cube((0, 0, 0.5), 0.3, cloud=0.1, bubbles=50, seed=3)
    key_obj(c, 0, rot=(0.2, 0.1, 0.0)); key_obj(c, n, rot=(0.25, 0.1, math.radians(55)))
    P.lights((0, 0, 0.5), key=500, rim=1400, scale=0.7)
    cam_move(cam, n, ((0.08, -1.05, 0.66), (0, 0, 0.5), 50), ((0.04, -0.9, 0.62), (0, 0, 0.5), 55), fstop=8)


def _air_dots(center, R, n=60, seed=1, size=0.006):
    rnd = random.Random(seed); m = C.pbr("airdot", "#FFFFFF", 0.2, emit="#FFFFFF", estr=2.0); out = []
    for i in range(n):
        th, ph, r = rnd.uniform(0, 6.28), math.acos(rnd.uniform(-1, 1)), R * rnd.random() ** 0.5
        p = Vector(center) + Vector((r * math.sin(ph) * math.cos(th), r * math.sin(ph) * math.sin(th), r * math.cos(ph)))
        bpy.ops.mesh.primitive_ico_sphere_add(radius=size * rnd.uniform(0.6, 1.3), subdivisions=2, location=p)
        o = bpy.context.object; o.data.materials.append(m); o["home"] = tuple(p); out.append(o)
        for f in o.data.polygons:
            f.use_smooth = True
    return out


def water_air(sh, cam, n):
    studio(bottom="#1F3A68", glow=0.25)
    g = C.cyl("glass", 0.30, 0.8, (0, 0, 0.4), mat=C.glass("glassbig", refl=0.1), verts=64, r2=0.27)
    w = C.cyl("water", 0.285, 0.62, (0, 0, 0.33), mat=P.ice_mat("water", 0.0), verts=64, r2=0.26)
    dots = _air_dots((0, 0, 0.35), 0.24, n=70, size=0.012)
    fd = W_(sh, "dissolved", 1.6)
    rnd = random.Random(3)
    for d in dots:
        h0 = Vector(d["home"]); ph = rnd.random() * 6
        f0 = rnd.randint(4, max(5, fd))
        key_obj(d, 0, scale=0.0); key_obj(d, f0, scale=0.0, loc=h0); key_obj(d, f0 + 6, scale=1.0)
        for f in range(f0 + 6, n + 1, 6):
            key_obj(d, f, loc=h0 + Vector((0.01 * math.sin(f * 0.2 + ph), 0, 0.01 * math.cos(f * 0.17 + ph))))
    P.lights((0, 0, 0.4), key=600, rim=1200, scale=0.8)
    cam_move(cam, n, ((0.3, -1.9, 0.75), (0, 0, 0.38), 45), None, orbit=20, fstop=8)


def no_room(sh, cam, n):
    studio(bottom="#1F3A68", glow=0.25)
    c, _ = P.ice_cube((0, 0, 0.5), 0.5, cloud=0.0)
    dots = _air_dots((0, 0, 0.5), 0.18, n=40, size=0.014, seed=4)
    rnd = random.Random(5)
    fn = W_(sh, "no", 0.6)
    for d in dots:
        h0 = Vector(d["home"]); v = (h0 - Vector((0, 0, 0.5))); v = v.normalized() if v.length > 1e-4 else Vector((1, 0, 0))
        out = Vector((0, 0, 0.5)) + v * rnd.uniform(0.42, 0.6) + Vector((0, -0.05, 0))
        key_obj(d, 0, loc=h0); key_obj(d, fn, loc=h0); key_obj(d, fn + 14 + rnd.randint(0, 8), loc=out)
    P.lights((0, 0, 0.5), key=600, rim=1300, scale=0.8)
    cam_move(cam, n, ((0.25, -1.9, 0.72), (0, 0, 0.5), 45), ((0.15, -1.7, 0.7), (0, 0, 0.5), 48), fstop=8)


def freezer(sh, cam, n):
    studio(bottom="#2E5C8A", glow=0.18)
    P.counter((0, -0.75, 0), w=1.4, d=0.55, top="#7FA3C2", top2="#6E93B3", body="#1F3A68")
    base, items = P.ice_tray(TRAY + Vector((-0.14, 0, 0)), cubes=False, water=0.9)
    rnd = random.Random(7); fm = C.pbr("frost", "#FFFFFF", 0.3, emit="#E6F5FF", estr=1.5)
    for k in range(40):   # frost sparkles appearing around the tray edge
        x, y = TRAY.x - 0.14 + rnd.uniform(-0.09, 0.09), TRAY.y + rnd.uniform(-0.05, 0.05)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=0.0015, subdivisions=1, location=(x, y, TOP + 0.032))
        o = bpy.context.object; o.data.materials.append(fm); f0 = rnd.randint(0, n - 4)
        key_obj(o, 0, scale=0.0); key_obj(o, f0, scale=0.0); key_obj(o, f0 + 3, scale=1.0)
    C.area("cold", (0, -0.4, TOP + 0.8), (0, 0, 0), 1.0, "#CFE9FF", 120)
    P.lights((0, -0.4, TOP + 0.05), key=600, rim=700, scale=0.6)
    t = TRAY + Vector((-0.14, 0, 0.02))
    cam_move(cam, n, ((t.x + 0.05, t.y - 0.30, t.z + 0.22), t, 45), ((t.x + 0.03, t.y - 0.24, t.z + 0.18), t, 50), fstop=8)


def _xsec(n, k0, k1, mode="all"):
    """mode all: liquid core shrinks to the centre (outside-in); top: liquid shrinks downward (freezing from the top only)."""
    studio(bottom="#244A7A", glow=0.25)
    x = P.freeze_section((0, 0, 1.0), s=1.0)
    core, air, s = x["core"], x["air"], x["s"]
    for f in range(0, n + 1, 2):
        k = k0 + (k1 - k0) * ease(f / max(1, n))
        if mode == "all":
            kk = max(k, 0.0)
            key_obj(core, f, scale=(max(kk, 0.001), 1, max(kk, 0.001)))
            for a in air:
                hx, hy, hz = a["home"]
                key_obj(a, f, loc=(hx * max(kk, 0.10), hy, 1.0 + hz * max(kk, 0.10)))
        else:   # freezing from the top only: liquid height k, bottom fixed
            kk = max(k, 0.06)
            key_obj(core, f, scale=(1, 1, kk), loc=(0, -0.035, 1.0 - 0.41 * (1 - kk)))
            for a in air:
                hx, hy, hz = a["home"]
                key_obj(a, f, loc=(hx, hy, 1.0 - 0.41 + (hz + 0.38) * kk))
    P.lights((0, 0, 1.0), key=700, rim=600, scale=1.0)
    return x


def xsec_start(sh, cam, n):
    _xsec(n, 0.98, 0.75)
    cam_move(cam, n, ((0.05, -2.0, 1.0), (0, 0, 1.0), 42), ((0.03, -1.85, 1.0), (0, 0, 1.0), 44), fstop=11)


def xsec_layers(sh, cam, n):
    _xsec(n, 0.75, 0.42)
    cam_move(cam, n, ((0.03, -1.85, 1.0), (0, 0, 1.0), 44), ((0.02, -1.7, 1.0), (0, 0, 1.0), 47), fstop=11)


def xsec_trapped(sh, cam, n):
    _xsec(n, 0.42, 0.0)
    cam_move(cam, n, ((0.02, -1.7, 1.0), (0, 0, 1.0), 47), ((0.0, -1.45, 1.0), (0, 0, 1.0), 52), fstop=11)


def bubbles_macro(sh, cam, n):
    studio(bottom="#1F3A68", glow=0.22)
    c, bs = P.ice_cube((0, 0, 0.5), 0.34, cloud=0.12, bubbles=90, seed=6)
    key_obj(c, 0, rot=(0.15, 0.05, 0.3)); key_obj(c, n, rot=(0.15, 0.05, 0.7))
    P.lights((0, 0, 0.5), key=450, rim=1500, scale=0.7)
    cam_move(cam, n, ((0.02, -0.95, 0.62), (0, 0, 0.5), 60), ((0.01, -0.80, 0.6), (0, 0, 0.5), 65), fstop=8)


def scatter(sh, cam, n):
    studio(bottom="#14213D", glow=0.15)
    c, bs = P.ice_cube((0, 0, 0.5), 0.34, cloud=0.12, bubbles=60, seed=6); c.rotation_euler = (0.15, 0.05, 0.7)
    beam_m = C.emission("beam", "#FFF1DC", 3.0)
    beam = C.cyl("beam", 0.012, 1.0, (0, 0, 0), (0, math.radians(90), 0), mat=beam_m, verts=16)
    key_obj(beam, 0, loc=(-1.6, 0, 0.5), scale=(1, 1, 1)); key_obj(beam, 8, loc=(-0.65, 0, 0.5))
    fs = W_(sh, "scatter", 0.5)
    rnd = random.Random(9)
    for k in range(16):
        th, ph = rnd.uniform(0, 6.28), math.acos(rnd.uniform(-0.9, 0.9))
        d = Vector((math.sin(ph) * math.cos(th), math.sin(ph) * math.sin(th) * 0.6 - 0.2, math.cos(ph)))
        ray = C.cyl(f"ray{k}", 0.003, 1.0, (0, 0, 0), mat=beam_m, verts=8)
        ray.rotation_mode = "QUATERNION"; ray.rotation_quaternion = d.to_track_quat("Z", "Y")
        L = rnd.uniform(0.35, 0.7); f0 = fs + rnd.randint(0, 8)
        key_obj(ray, 0, loc=(0, 0, 0.5), scale=(1, 1, 0.0)); key_obj(ray, f0, scale=(1, 1, 0.0), loc=(0, 0, 0.5))
        key_obj(ray, f0 + 6, scale=(1, 1, L), loc=Vector((0, 0, 0.5)) + d * (L / 2))
    P.lights((0, 0, 0.5), key=250, rim=900, scale=0.7)
    cam_move(cam, n, ((0.15, -1.6, 0.62), (0, 0, 0.5), 45), ((0.1, -1.45, 0.6), (0, 0, 0.5), 48), fstop=8)


def _lake(n, grow=True):
    P.world("#14213D", 0.3); P.studio(top="#14213D", bottom="#BFE6FF", glow=0.25, y0=2.0)
    water, ice, snow = P.lake((0, 0, 0.8), w=1.0, d=0.8, ice_t=0.18)
    rnd = random.Random(11); bm = C.pbr("lakebub", "#FFFFFF", 0.1, emit="#FFFFFF", estr=1.2)
    if grow:
        key_obj(ice, 0, scale=(1, 1, 0.15), loc=(0, 0, 0.8 - 0.018 * 0.75)); key_obj(ice, n, scale=(1, 1, 1.0), loc=(0, 0, 0.8 - 0.09))
    for k in range(30):   # air bubbles leave the freezing front and drift away into the deep water
        x, y = rnd.uniform(-0.45, 0.45), rnd.uniform(-0.4, -0.3)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=rnd.uniform(0.006, 0.014), subdivisions=2, location=(x, y, 0.65))
        o = bpy.context.object; o.data.materials.append(bm)
        f0 = rnd.randint(0, n // 2)
        key_obj(o, 0, loc=(x, y, 0.64)); key_obj(o, f0, loc=(x, y, 0.64)); key_obj(o, n, loc=(x + rnd.uniform(-0.1, 0.1), y, 0.64 - rnd.uniform(0.2, 0.5)))
    P.lights((0, 0, 0.8), key=700, rim=700, scale=1.2)
    return ice


def lake_down(sh, cam, n):
    _lake(n, grow=True)
    cam_move(cam, n, ((0.9, -2.4, 1.35), (0, 0, 0.55), 40), ((0.75, -2.2, 1.25), (0, 0, 0.55), 42), fstop=11)


def lake_clear(sh, cam, n):
    _lake(n, grow=False)
    cam_move(cam, n, ((0.6, -1.8, 1.05), (0, 0, 0.6), 45), ((0.45, -1.6, 0.98), (0, 0, 0.62), 48), fstop=11)


def one_side(sh, cam, n):
    _xsec(n, 0.95, 0.12, mode="top")
    cam_move(cam, n, ((0.05, -2.0, 1.0), (0, 0, 1.0), 43), ((0.02, -1.8, 1.0), (0, 0, 1.0), 46), fstop=11)


def clear_cube(sh, cam, n):
    counter_set(tray=False)
    h, ct = presenter(); ec = h["eye_c"]
    held_cube(h, cloud=0.0)
    hp = Vector((ec.x - 0.13, ec.y - 0.30, ec.z - 0.13))
    key_obj(ct["handR"], 0, loc=hp + Vector((0, 0, -0.06))); key_obj(ct["handR"], 12, loc=hp)
    key_obj(ct["look"], 0, loc=hp + Vector((0, -0.2, 0))); key_obj(ct["look"], n, loc=(0.1, -1.4, ec.z))
    Hm.face(h["keys"], 0, smile=0.4, brows_up=0.4); Hm.face(h["keys"], n, smile=0.8, brows_up=0.6, wide=0.2)
    life(h, n, 7)
    cam_move(cam, n, ((0.18, -1.0, ec.z - 0.10), (0, -0.2, ec.z - 0.13), 44), ((0.15, -0.92, ec.z - 0.09), (0, -0.2, ec.z - 0.12), 46), focus=hp, fstop=8)


def drink_loop(sh, cam, n):
    counter_set(tray=True, jug=False)
    h, ct = presenter(); ec = h["eye_c"]
    g, liq, cs = P.drink((0.0, -0.40, TOP), r=0.04, h=0.11, cubes=3, cloud=1.0)
    c = held_cube(h)
    key_obj(ct["handR"], 0, loc=(0.0, -0.42, TOP + 0.16)); key_obj(ct["handR"], n, loc=(0.0, -0.42, TOP + 0.24))
    key_obj(ct["look"], 0, loc=(0, -0.42, TOP + 0.1)); key_obj(ct["look"], n, loc=(0, -0.42, TOP + 0.24))
    Hm.face(h["keys"], 0, smile=0.2); Hm.face(h["keys"], n, smile=0.4, brows_up=0.3)
    life(h, n, 8)
    cam_move(cam, n, ((0.18, -0.95, TOP + 0.24), (0, -0.35, TOP + 0.22), 42), ((0.15, -0.88, TOP + 0.30), (0, -0.30, TOP + 0.30), 45), fstop=8)


def loop_end(sh, cam, n):
    counter_set()
    h, ct = presenter(); ec = h["eye_c"]
    held_cube(h)
    hp = Vector((ec.x - 0.13, ec.y - 0.30, ec.z - 0.13))
    key_obj(ct["handR"], 0, loc=hp + Vector((0, 0, -0.05))); key_obj(ct["handR"], n, loc=hp + Vector((0, 0, -0.03)))
    key_obj(ct["look"], 0, loc=(0.1, -1.4, ec.z)); key_obj(ct["look"], n, loc=hp + Vector((0, -0.2, 0)))
    Hm.face(h["keys"], 0, browL_up=0.9, smile=0.4); Hm.face(h["keys"], n, squint=0.4, brows_inner=0.6, browL_up=0.4)
    cam_move(cam, n, ((0.08, -0.86, ec.z - 0.07), (-0.04, -0.2, ec.z - 0.11), 45), ((0.10, -0.95, ec.z - 0.08), (-0.04, -0.2, ec.z - 0.12), 42), focus=hp, fstop=8)


SHOTS = {f.__name__: f for f in (hook_cube, cube_macro, water_air, no_room, freezer, xsec_start, xsec_layers, xsec_trapped, bubbles_macro, scatter,
                                 lake_down, lake_clear, one_side, clear_cube, drink_loop, loop_end)}

if __name__ == "__main__":
    run(SHOTS, sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:])
