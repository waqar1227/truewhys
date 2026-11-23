"""A-025 Style R scenes (Blender): "Why can only one company build this machine?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Our own generic chip-printing machine (no logos, no brand look) in a yellow-lit clean room, a hero-size tin-droplet chamber with laser pulses
and plasma, a collector mirror, a wafer with nanometre lines next to a human hair (scaled), a giant mirror plain; our MPFB cast in a clean-room suit.
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

TECH = dict(macro={"gender": 0, "age": 0.4, "muscle": 0.45, "weight": 0.55, "proportions": 0.55, "height": 0.5}, skin="#C68E64",
            hair="#EEF1F4", hair_style="bun", shirt="#F2F4F6", trousers="#F2F4F6", shoes="#E8ECF0", iris="#3A2416", sleeve="long",
            shirt_push=0.03, shirt_iters=45, tuck=0.035)                 # technician in a loose white clean-room suit + white cap
TIN, LASER, PLASMA, EUV = "#D9DEE6", "#FF3B30", "#E9D6FF", "#B57BFF"
YEL = "#FFD27A"                                                          # clean-room yellow light (chip fabs use yellow light)


def sphere(name, r, loc, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=r, location=loc, segments=48, ring_count=24)
    o = bpy.context.active_object; o.name = name
    o.data.materials.append(mat)
    for p_ in o.data.polygons:
        p_.use_smooth = True
    return o


# ------------------------------------------------------------------ sets
def cleanroom():
    P.world("#3A3320", 0.35)
    C.rbox("floor", (14, 14, 0.02), (0, 0, -0.01), mat=C.pbr("cr_floor", "#D9D2BC", 0.35, bump="cells", bscale=6, bstr=0.08), bevel=0.0)
    C.rbox("backwall", (14, 0.1, 6), (0, 4.0, 3), mat=C.pbr("cr_wall", "#E8E0C8", 0.6), bevel=0.0)
    for s in (-1, 1):
        C.rbox("sidewall", (0.1, 14, 6), (s * 6.0, 0, 3), mat=C.pbr("cr_wall", "#E8E0C8", 0.6), bevel=0.0)
    C.rbox("ceiling", (14, 14, 0.05), (0, 0, 4.65), mat=C.pbr("cr_ceil", "#D8D0B8", 0.7), bevel=0.0)
    lm = C.emission("cr_panel", YEL, 3.0)
    for i in range(-2, 3):
        for j in range(0, 3):
            C.rbox("ceilpanel", (1.2, 0.6, 0.02), (i * 2.0, -1.0 + j * 2.0, 4.61), mat=lm, bevel=0.0)
    C.area("ceilkey", (0, 0.5, 4.4), (0, 0, 0), 6.0, YEL, 450)


def machine(x=0.0, y=1.6, glow=1.0):
    """Generic chip-printing machine: long rounded white housing, side modules, a round viewport into the glowing light-source chamber."""
    W_m = C.pbr("mach", "#F4F4F0", 0.3, coat=0.4)
    G_m = C.pbr("mach_grey", "#9AA3AD", 0.35, metal=0.6)
    D_m = C.pbr("mach_dark", "#2A2F36", 0.4)
    C.rbox("m_main", (3.6, 1.6, 2.3), (x, y, 1.15 + 0.05), mat=W_m, bevel=0.08)
    C.rbox("m_top", (2.6, 1.3, 0.5), (x - 0.3, y + 0.1, 2.55), mat=W_m, bevel=0.06)
    C.rbox("m_src", (1.2, 1.4, 1.9), (x + 2.4, y + 0.05, 0.95 + 0.05), mat=W_m, bevel=0.07)    # light-source module
    C.rbox("m_base", (4.9, 1.8, 0.1), (x + 0.6, y, 0.05), mat=G_m, bevel=0.01)
    for k in range(5):
        C.rbox("m_stripe", (3.4, 0.01, 0.025), (x, y - 0.805, 0.5 + k * 0.38), mat=G_m, bevel=0.0)
    C.rbox("m_panel", (0.7, 0.03, 0.45), (x - 1.1, y - 0.81, 1.45), mat=D_m, bevel=0.02)
    C.rbox("m_screen", (0.6, 0.01, 0.33), (x - 1.1, y - 0.83, 1.47), mat=C.emission("m_scr", "#7CC8FF", 2.5), bevel=0.0)
    for k in range(4):
        C.tube("pipe", [(x + 1.85, y - 0.4 + k * 0.25, 1.9), (x + 1.85, y - 0.4 + k * 0.25, 2.3), (x + 1.4, y - 0.4 + k * 0.25, 2.55)], 0.04, mat=G_m, n=12)
    # viewport into the source chamber
    vx, vz = x + 2.4, 1.15
    C.cyl("port_ring", 0.3, 0.06, (vx, y - 0.68, vz), rot=(math.radians(90), 0, 0), mat=G_m, verts=48, bevel=0.01)
    C.cyl("port_glass", 0.24, 0.01, (vx, y - 0.71, vz), rot=(math.radians(90), 0, 0), mat=C.glass("port", refl=0.1), verts=48)
    C.cyl("port_glow", 0.22, 0.01, (vx, y - 0.6, vz), rot=(math.radians(90), 0, 0), mat=C.emission("port_glow", EUV, 6.0 * glow), verts=48)
    C.area("portlight", (vx, y - 0.9, vz), (math.radians(90), 0, 0), 0.4, "#C9A6FF", 60 * glow)
    return dict(port=(vx, y - 0.71, vz))


def tech(loc=(0, 0, 0), rot_z=0):
    h = Hm.build(dict(TECH, loc=loc, rot_z=rot_z), "woman"); ct = Hm.controls(h)
    return h, ct


def chamber(dark="#05070C"):
    P.world(dark, 0.15)
    C.rbox("ch_back", (3, 0.05, 3), (0, 0.6, 1.0), mat=C.pbr("ch_wall", "#14181F", 0.5, metal=0.4, bump="noise", bstr=0.1), bevel=0.0)
    C.rbox("ch_floor", (3, 3, 0.05), (0, 0, -0.3), mat=C.pbr("ch_wall", "#14181F", 0.5, metal=0.4), bevel=0.0)


def droplet_stream(n, z=1.0, x0=-0.6, x1=0.6, r=0.012, gap=4, speed=0.05, name="tin"):
    """Drops flying left->right along X at height z (each keyed linear), new one every `gap` frames."""
    tm = C.pbr("tin_m", TIN, 0.12, metal=1.0, emit="#FFB070", estr=3.0)
    out = []
    for i in range(-40, n // gap + 2):
        f0 = i * gap
        o = C.cyl(f"{name}{i}", r, 2 * r, (x0, 0, z), mat=tm, verts=16, bevel=r * 0.98)
        fa, fb = f0, f0 + int((x1 - x0) / speed)
        key_obj(o, fa, loc=(x0, 0, z)); key_obj(o, fb, loc=(x1, 0, z)); C.set_interp(o, "LINEAR")
        out.append(o)
    return out


def nozzle(x=-0.62, z=1.0):
    C.cyl("nozzle", 0.05, 0.25, (x - 0.12, 0, z), rot=(0, math.radians(90), 0), mat=C.pbr("noz", "#8A939E", 0.3, metal=1.0), verts=32, r2=0.02, bevel=0.004)


# ------------------------------------------------------------------ shots
def _spectacle(n, f_off=0):
    """Inside the machine: tin drops stream from the nozzle; a laser fires every 7 frames and each hit drop bursts into a violet-white plasma flash."""
    chamber(); nozzle()
    droplet_stream(n + 40, gap=3, speed=0.06, r=0.016)
    pm = C.emission("plasma_m", PLASMA, 40.0); hm = C.ghost("plasma_halo", EUV, glow=6.0, core=0.0); lm = C.emission("laser_m", LASER, 30.0)
    beam = C.cyl("beam", 0.006, 1.4, (0.0, -0.7, 1.0), rot=(math.radians(90), 0, 0), mat=lm, verts=12)
    key_obj(beam, 0, scale=0.0)
    for k, f in enumerate(range(-((f_off) % 7), n + 7, 7)):
        core = sphere(f"pc{k}", 0.035, (0.0, 0, 1.0), pm); halo = sphere(f"ph{k}", 0.09, (0.0, 0, 1.0), hm)
        for o in (core, halo):
            key_obj(o, max(0, f - 1), scale=0.0); key_obj(o, max(0, f), scale=0.0); key_obj(o, f + 2, scale=1.3); key_obj(o, f + 6, scale=0.0)
        key_obj(beam, max(0, f - 1), scale=0.0); key_obj(beam, max(0, f), scale=(1, 1, 1)); key_obj(beam, f + 2, scale=0.0)
    C.area("tinlight", (0, -0.4, 1.4), (math.radians(30), 0, 0), 1.0, "#FFB070", 90)
    C.area("violet", (0.15, -0.25, 1.15), (math.radians(70), 0, 0), 0.4, "#C9A6FF", 120)


SPEC_A = ((-0.3, -0.36, 1.1), (-0.02, 0.0, 1.0), 34)
SPEC_B = ((-0.26, -0.32, 1.09), (0.0, 0.0, 1.0), 37)


def hook_machine(sh, cam, n):
    """Frame 1 (action): inside the machine - glowing tin drops streak past, a laser fires and drops burst into violet-white plasma, again and again."""
    _spectacle(n)
    cam_move(cam, n, SPEC_A, SPEC_B, focus=(0.0, 0, 1.0), fstop=4.0)


def loop_q(sh, cam, n):
    """Last shot = frame 1 (loop): same chamber view, camera easing back to the hook's first frame."""
    _spectacle(n, f_off=n)
    cam_move(cam, n, SPEC_B, SPEC_A, focus=(0.0, 0, 1.0), fstop=4.0)


def phone_chip(sh, cam, n):
    """'The most advanced chips in your phone': a see-through phone on a pedestal; its chip glows and rises out, circuit lines lighting up."""
    P.world("#101820", 0.3)
    P.studio(top="#10283E", bottom="#1E3A56", mid="#16324C", y0=0.6, glow=0.35, height=4.0, width=8.0, depth=3.0)
    Z0 = 1.0
    C.cyl("ped", 0.22, Z0 - 0.05, (0, 0.05, (Z0 - 0.05) / 2), mat=C.pbr("ped", "#E8ECF0", 0.4), verts=48, bevel=0.01)
    ph = C.rbox("phone", (0.075, 0.155, 0.008), (0, 0.05, Z0 + 0.004), mat=C.pbr("phone_m", "#1A1D22", 0.15, coat=0.9), bevel=0.006)
    C.rbox("phone_scr", (0.069, 0.147, 0.0005), (0, 0.05, Z0 + 0.0082), mat=C.emission("phone_scr", "#1E3A66", 1.5), bevel=0.0)
    chip = C.rbox("chip", (0.022, 0.022, 0.002), (0, 0.06, Z0 + 0.006), mat=C.pbr("chip", "#2A2F36", 0.3, metal=0.5, emit="#B57BFF", estr=4.0, bump="grille", bscale=600, bstr=0.4), bevel=0.0008)
    key_obj(chip, 0, loc=(0, 0.06, Z0 + 0.006), rot=(0, 0, 0)); key_obj(chip, int(n * 0.35), loc=(0, 0.06, Z0 + 0.006), rot=(0, 0, 0))
    key_obj(chip, n, loc=(0, 0.04, Z0 + 0.07), rot=(math.radians(-55), 0, math.radians(20)))
    P.lights((0, 0, Z0), key=300, rim=500, fill=100, scale=0.5)
    cam_move(cam, n, ((0.02, -0.2, Z0 + 0.16), (0.0, 0.05, Z0 + 0.01), 45), ((0.03, -0.14, Z0 + 0.12), (0.0, 0.05, Z0 + 0.04), 50), focus=(0, 0.05, Z0 + 0.03), fstop=6.3)


def only_one(sh, cam, n):
    """'And no other company sells one': the machine alone in a dim clean room under one spotlight; slow push in."""
    P.world("#1A160C", 0.15)
    C.rbox("floor", (14, 14, 0.02), (0, 0, -0.01), mat=C.pbr("cr_floor_d", "#3A3528", 0.35), bevel=0.0)
    machine()
    C.area("spot", (0.6, -0.5, 5.0), (0, 0, 0), 2.5, YEL, 1800)
    cam_move(cam, n, ((-2.6, -5.2, 1.6), (0.7, 1.6, 1.4), 30), ((-2.3, -4.6, 1.55), (0.7, 1.6, 1.4), 32), focus=(0.5, 1.0, 1.3), fstop=5.6)


def droplets(sh, cam, n):
    """'Fifty thousand drops of molten tin every second': a hero-size stream of glowing tin drops shooting from a nozzle across the dark chamber."""
    chamber(); nozzle()
    droplet_stream(n, gap=3, speed=0.06, r=0.016)
    C.area("tinlight", (0, -0.4, 1.4), (math.radians(30), 0, 0), 1.0, "#FFB070", 90)
    C.area("rim", (0.3, 0.5, 1.3), (math.radians(-120), 0, 0), 1.0, "#7FA8FF", 40)
    cam_move(cam, n, ((-0.62, -0.3, 1.05), (-0.25, 0.0, 1.0), 40), ((-0.5, -0.26, 1.04), (-0.1, 0.0, 1.0), 44), focus=(-0.35, 0, 1.0), fstop=4.0)


def laser_hit(sh, cam, n):
    """'A laser hits each drop twice: first to flatten it': slow motion - a red pulse hits one drop, it squashes into a pancake."""
    chamber(); nozzle(x=-0.42)
    tm = C.pbr("tin_m", TIN, 0.12, metal=1.0, emit="#FFB070", estr=0.6)
    d = C.cyl("hero_drop", 0.02, 0.04, (-0.3, 0, 1.0), mat=tm, verts=32, bevel=0.0199)
    f1 = W_(sh, "flatten", 1.5)
    key_obj(d, 0, loc=(-0.3, 0, 1.0), scale=(1, 1, 1)); key_obj(d, f1 - 2, loc=(0.0, 0, 1.0), scale=(1, 1, 1))
    key_obj(d, f1 + 6, loc=(0.02, 0, 1.0), scale=(0.35, 2.6, 2.6)); key_obj(d, n, loc=(0.06, 0, 1.0), scale=(0.3, 2.8, 2.8))
    beam = C.cyl("beam1", 0.006, 1.2, (-0.6, 0, 1.0), rot=(0, math.radians(90), 0), mat=C.emission("laser_m", LASER, 30.0), verts=12)
    key_obj(beam, 0, scale=0.0); key_obj(beam, f1 - 3, scale=0.0); key_obj(beam, f1 - 1, scale=(1, 1, 1)); key_obj(beam, f1 + 3, scale=(1, 1, 1)); key_obj(beam, f1 + 5, scale=0.0)
    fl = C.area("flash", (0.0, -0.2, 1.0), (math.radians(90), 0, 0), 0.2, LASER, 0.0)
    fl.data.energy = 0; fl.data.keyframe_insert("energy", frame=f1 - 2); fl.data.energy = 400; fl.data.keyframe_insert("energy", frame=f1)
    fl.data.energy = 0; fl.data.keyframe_insert("energy", frame=f1 + 6)
    C.area("tinlight", (0, -0.4, 1.4), (math.radians(30), 0, 0), 1.0, "#FFB070", 20)
    C.area("dropfill", (-0.05, -0.45, 1.35), (math.radians(50), 0, 0), 0.5, "#FFE2C0", 60)
    cam_move(cam, n, ((-0.24, -0.24, 1.06), (-0.02, 0.0, 1.0), 45), ((-0.2, -0.2, 1.05), (0.0, 0.0, 1.0), 50), focus=(0.0, 0, 1.0), fstop=5.6)


def plasma(sh, cam, n):
    """'...then to blast it into plasma, hotter than the surface of the Sun': second pulse, the pancake explodes into a blazing violet-white ball."""
    chamber()
    tm = C.pbr("tin_m", TIN, 0.12, metal=1.0, emit="#FFB070", estr=0.6)
    d = C.cyl("pancake", 0.02, 0.04, (0.06, 0, 1.0), mat=tm, verts=32, bevel=0.0199); d.scale = (0.3, 2.8, 2.8)
    fb = W_(sh, "blast", 0.5)
    key_obj(d, 0, scale=(0.3, 2.8, 2.8)); key_obj(d, fb, scale=(0.3, 2.8, 2.8)); key_obj(d, fb + 2, scale=0.0)
    core = sphere("plasma_core", 0.05, (0.06, 0, 1.0), C.emission("plasma_m", PLASMA, 40.0))
    halo = sphere("plasma_halo", 0.12, (0.06, 0, 1.0), C.ghost("plasma_halo", EUV, glow=6.0, core=0.0))
    for o, s1 in ((core, 1.0), (halo, 1.0)):
        key_obj(o, 0, scale=0.0); key_obj(o, fb, scale=0.0); key_obj(o, fb + 6, scale=s1 * 1.3); key_obj(o, n, scale=s1 * (1.0 + 0.1 * math.sin(n)))
    beam = C.cyl("beam2", 0.008, 1.2, (-0.54, 0, 1.0), rot=(0, math.radians(90), 0), mat=C.emission("laser2_m", LASER, 40.0), verts=12)
    key_obj(beam, 0, scale=0.0); key_obj(beam, fb - 2, scale=0.0); key_obj(beam, fb, scale=(1, 1, 1)); key_obj(beam, fb + 4, scale=0.0)
    pl = C.area("plasmalight", (0.06, -0.15, 1.0), (math.radians(90), 0, 0), 0.1, "#D9B8FF", 0.0)
    pl.data.energy = 0; pl.data.keyframe_insert("energy", frame=fb); pl.data.energy = 900; pl.data.keyframe_insert("energy", frame=fb + 5)
    pl.data.energy = 600; pl.data.keyframe_insert("energy", frame=n)
    cam_move(cam, n, ((0.02, -0.5, 1.04), (0.05, 0.0, 1.0), 42), ((0.02, -0.4, 1.03), (0.05, 0.0, 1.0), 46), focus=(0.06, 0, 1.0), fstop=5.6)


def euv_light(sh, cam, n):
    """'That plasma glows with extreme ultraviolet light': a big gold-and-mirror collector dish catches the violet glow and sends a beam away."""
    chamber()
    dish = C.cyl("collector", 0.45, 0.06, (0.0, 0.35, 1.0), rot=(math.radians(90), 0, 0), mat=C.pbr("coll", "#E9C46A", 0.18, metal=1.0, emit="#B57BFF", estr=0.4), verts=96, r2=0.38)
    sphere("plasma_s", 0.025, (0.0, -0.05, 1.0), C.emission("plasma_m2", PLASMA, 40.0))
    sphere("glow_s", 0.08, (0.0, -0.05, 1.0), C.ghost("plasma_halo2", EUV, glow=5.0, core=0.0))
    cone = C.cyl("beam_cone", 0.035, 1.6, (0.0, -0.85, 1.0), rot=(math.radians(90), 0, 0), mat=C.ghost("euv_beam", EUV, glow=2.5, core=0.05), verts=32)
    key_obj(cone, 0, scale=(0.0, 0.0, 1.0)); key_obj(cone, int(n * 0.4), scale=(1, 1, 1.0))
    C.area("euvfill", (0, -0.3, 1.3), (math.radians(60), 0, 0), 0.6, "#C9A6FF", 120)
    cam_move(cam, n, ((0.95, -0.55, 1.15), (0.0, 0.0, 1.0), 30), ((0.85, -0.45, 1.12), (0.0, 0.05, 1.0), 32), focus=(0, 0.1, 1.0), fstop=5.6)


def wafer_lines(sh, cam, n):
    """'...draw lines thousands of times thinner than a hair': macro of a wafer; rows of tiny bright lines appear; a giant hair rolls in beside them."""
    P.world("#0E1218", 0.3)
    Z0 = 1.0
    C.rbox("wafer", (0.6, 0.6, 0.004), (0, 0, Z0 - 0.002), mat=C.pbr("wafer", "#6E7FA6", 0.18, metal=1.0), bevel=0.0)
    lm = C.emission("line_m", "#9FE6FF", 6.0)
    fl = W_(sh, "lines", 0.3)
    for i in range(24):
        L = C.rbox(f"ln{i}", (0.0006, 0.06, 0.0004), (-0.02 + i * 0.0018, 0.0, Z0 + 0.0002), mat=lm, bevel=0.0)
        key_obj(L, 0, scale=(1, 0.0, 1)); key_obj(L, fl + i, scale=(1, 0.0, 1)); key_obj(L, fl + i + 10, scale=(1, 1, 1))
    hair = C.cyl("hair", 0.012, 0.3, (0.07, 0.0, Z0 + 0.012), rot=(math.radians(90), 0, 0), mat=C.pbr("hair_m", "#5A3A22", 0.4, coat=0.5, bump="noise", bscale=400, bstr=0.2), verts=32)
    fh = W_(sh, "hair", 2.5)
    key_obj(hair, 0, loc=(0.2, 0.0, Z0 + 0.012)); key_obj(hair, max(1, fh - 18), loc=(0.2, 0.0, Z0 + 0.012)); key_obj(hair, fh + 4, loc=(0.045, 0.0, Z0 + 0.012))
    P.lights((0, 0, Z0), key=200, rim=300, fill=60, scale=0.4)
    cam_move(cam, n, ((0.0, -0.12, Z0 + 0.06), (0.0, 0.0, Z0), 50), ((0.02, -0.11, Z0 + 0.05), (0.015, 0.0, Z0), 52), focus=(0.01, 0, Z0), fstop=8.0)


def mirror(sh, cam, n):
    """'Its mirrors are so smooth...': a flawless round mirror on a mount, the clean room reflected perfectly as the camera glides over it."""
    cleanroom()
    C.cyl("mount", 0.32, 0.9, (0, 0.2, 0.45), mat=C.pbr("mount", "#9AA3AD", 0.35, metal=0.6), verts=48, bevel=0.01)
    mr = C.cyl("mirror", 0.3, 0.05, (0, 0.2, 0.93), mat=C.pbr("mirror_m", "#F0F4FF", 0.01, metal=1.0), verts=96, bevel=0.004)
    C.cyl("mirror_rim", 0.315, 0.04, (0, 0.2, 0.92), mat=C.pbr("rim", "#C9A23A", 0.3, metal=1.0), verts=96, bevel=0.004)
    P.lights((0, 0.2, 0.95), key=400, rim=600, fill=150)
    cam_move(cam, n, ((-0.45, -0.35, 1.6), (0.0, 0.2, 0.95), 36), ((-0.2, -0.3, 1.45), (0.0, 0.2, 0.95), 38), focus=(0, 0.2, 0.95), fstop=6.3)


def germany(sh, cam, n):
    """'...scaled up to the size of Germany, the tallest bump would be no higher than a millimetre': a mirror plain to the horizon; we fly
    down to one tiny bump, a person beside it for scale (bump far lower than their shoe)."""
    P.world("#8FB8E8", 0.9)
    C.rbox("mirrorplain", (400, 400, 0.02), (0, 150, -0.01), mat=C.pbr("plain_m", "#E8EEFA", 0.02, metal=1.0), bevel=0.0)
    sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 3.0; so = bpy.data.objects.new("sun", sun); bpy.context.scene.collection.objects.link(so)
    so.rotation_euler = (math.radians(50), 0, math.radians(30))
    bump = C.cyl("bump", 0.05, 0.002, (0.0, 0.0, 0.0), mat=C.pbr("bump_m", "#FFD27A", 0.3, metal=0.6, emit="#FFC93C", estr=0.6), verts=32, bevel=0.0019)
    h, ct = tech(loc=(0.12, 0.05, 0), rot_z=-30)
    key_obj(ct["look"], 0, loc=(0.0, 0.0, 0.0)); Hm.face(h["keys"], 0, squint=0.5, brows_down=0.3)
    cam_move(cam, n, ((0.0, -60.0, 40.0), (0.0, 40.0, 0.0), 24), ((0.05, -0.9, 0.42), (0.06, 0.03, 0.3), 28), focus=(0.03, 0, 0.05), fstop=8.0)


def final_wide(sh, cam, n):
    """'Decades of work, in one machine...': the full machine and the small technician, camera rising."""
    cleanroom(); machine()
    h, ct = tech(loc=(1.65, -0.35, 0), rot_z=200)
    key_obj(ct["look"], 0, loc=(2.4, 0.9, 1.2))
    P.lights((1.0, 0.5, 1.2), key=500, rim=800, fill=200, scale=1.5)
    cam_move(cam, n, ((-1.8, -5.0, 1.0), (0.8, 1.4, 1.2), 26), ((-1.7, -4.7, 1.5), (0.8, 1.4, 1.2), 27), focus=(1.3, 0.2, 1.2), fstop=6.3)


SHOTS = {f.__name__: f for f in (hook_machine, phone_chip, only_one, droplets, laser_hit, plasma, euv_light, wafer_lines, mirror, germany, final_wide, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
