"""A-033 Style R scenes (Blender): "Why does a no-smoking plane toilet have an ashtray?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur]
Our own generic airliner cabin and lavatory (no airline, brand or logo): a folding lavatory door with a small hinged steel ashtray under a
generic no-smoking pictogram, a cabin aisle with seats and ceiling no-smoking signs, the waste-bin flap under the basin with an X-ray
cut-away (paper towels, a small automatic fire-extinguisher bottle), and a ceiling smoke detector. Our MPFB passenger. Facts in sources.md.
No person is ever shown smoking: the cigarette is only an object.
"""
import sys, os, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import key_obj, cam_move, W_, life, ease

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

PAX = dict(macro={"gender": 0, "age": 0.36, "muscle": 0.45, "weight": 0.45, "proportions": 0.62, "height": 0.5}, skin="#D9A27C",
           hair="#2A170C", hair_style="bun", shirt="#D4921A", trousers="#2B3440", shoes="#F4F1EA", iris="#4A3A2C", sleeve="long",
           shirt_push=0.04, shirt_iters=60, tuck=0.05)        # passenger, mustard long-sleeve top (loose), bun
EMBER = "#FF5A1A"
DOOR_X0, DOOR_W, DOOR_H = 0.0, 0.66, 1.86                     # lavatory door, front face at y = DY (aisle is y > 0)
DY = 0.03
ASH = Vector((0.20, DY, 1.02))                                # ashtray centre on the door (passenger's left of the door)
HANDLE = Vector((-0.24, DY + 0.03, 1.00))
SIGN = Vector((0.20, DY + 0.002, 1.20))


def mats():
    return dict(
        panel=C.pbr("panel", "#D9D3C7", 0.45, bump="noise", bscale=900, bstr=0.05, cvar=0.04, cscale=30.0),
        panel2=C.pbr("panel2", "#B9B3A8", 0.45, bump="noise", bscale=900, bstr=0.04),
        steel=C.pbr("steel", "#C9CDD2", 0.28, metal=0.9, bump="noise", bscale=2500, bstr=0.05),
        dark=C.pbr("dark", "#1C1E22", 0.6),
        carpet=C.pbr("carpet", "#3A4A66", 0.95, bump="weave", bscale=500, bstr=0.4, cvar=0.05),
        seat=C.pbr("seat", "#24386A", 0.9, bump="weave", bscale=700, bstr=0.35, cvar=0.04, sheen=0.3),
        head=C.pbr("headcover", "#F2F2EE", 0.85, bump="weave", bscale=900, bstr=0.2),
        white=C.pbr("signwhite", "#F7F7F4", 0.4),
        red=C.pbr("signred", "#D8262E", 0.4),
        black=C.pbr("signblack", "#151515", 0.5),
        paper=C.pbr("paper", "#F4F2EC", 0.85, bump="noise", bscale=300, bstr=0.25, cvar=0.03),
        filt=C.pbr("filter", "#D9A15E", 0.7, bump="noise", bscale=1500, bstr=0.1, cvar=0.08),
        ash=C.pbr("ashtip", "#8E8A86", 0.9, bump="noise", bscale=2000, bstr=0.3),
    )


def point(name, loc, col, energy, r=0.01):
    d = bpy.data.lights.new(name, "POINT"); d.energy = energy; d.color = C.srgb(col)[:3]; d.shadow_soft_size = r
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    return o


def key_energy(lt, f, e):
    lt.data.energy = e; lt.data.keyframe_insert("energy", frame=f)


def key_emit(mat, f, s):
    n = mat.node_tree.nodes.get("Emission")
    n.inputs["Strength"].default_value = s; n.inputs["Strength"].keyframe_insert("default_value", frame=f)


# ------------------------------------------------------------------ props
def no_smoking(loc, s=1.0, lit=None, name="nosmk"):
    """Generic no-smoking pictogram plate (white disc, red ring + slash over a black cigarette). lit: emission material for a backlit sign."""
    M = mats()
    base = C.rbox(name + "_plate", (0.085 * s, 0.006, 0.085 * s), (loc[0], loc[1] + 0.003, loc[2]), mat=lit or M["white"], bevel=0.004 * s)
    y = loc[1] + 0.0075
    pts = [(loc[0] + 0.03 * s * math.cos(a), y, loc[2] + 0.03 * s * math.sin(a)) for a in [i * 2 * math.pi / 48 for i in range(48)]]
    C.tube(name + "_ring", pts, 0.0045 * s, mat=M["red"], closed=True, n=8)
    C.rbox(name + "_cig", (0.034 * s, 0.002, 0.007 * s), (loc[0] - 0.003 * s, y - 0.001, loc[2]), mat=M["black"], bevel=0.0)
    C.rbox(name + "_slash", (0.066 * s, 0.003, 0.007 * s), (loc[0], y + 0.001, loc[2]), rot=(0, math.radians(-45), 0), mat=M["red"], bevel=0.0)
    return base


def ashtray(loc, open_=0.0, name="ash"):
    """Small recessed stainless ashtray with a hinged flap (hinge along the top edge). Returns the flap pivot (rotate X to open)."""
    M = mats()
    x, y, z = loc
    C.rbox(name + "_well", (0.088, 0.034, 0.054), (x, y + 0.017, z), mat=M["dark"], bevel=0.002)      # dark recess front reads as the opening
    for nm, size, loc in (("t", (0.11, 0.008, 0.012), (x, y + 0.064, z + 0.033)), ("b", (0.11, 0.008, 0.012), (x, y + 0.064, z - 0.033)),
                          ("l", (0.012, 0.008, 0.078), (x - 0.049, y + 0.064, z)), ("r", (0.012, 0.008, 0.078), (x + 0.049, y + 0.064, z))):
        C.rbox(name + "_frame" + nm, size, loc, mat=M["steel"], bevel=0.002)
    for sx in (-1, 1):
        C.rbox(name + "_side", (0.004, 0.034, 0.066), (x + sx * 0.047, y + 0.045, z), mat=M["steel"], bevel=0.001)
    C.rbox(name + "_top", (0.098, 0.034, 0.004), (x, y + 0.045, z + 0.031), mat=M["steel"], bevel=0.001)
    C.rbox(name + "_tray", (0.088, 0.03, 0.004), (x, y + 0.050, z - 0.026), mat=M["steel"], bevel=0.001)
    piv = C.empty(name + "_hinge", (x, y + 0.071, z - 0.027))                  # hinge along the bottom edge: the lid tips out and down
    fl = C.rbox(name + "_flap", (0.09, 0.004, 0.056), (0, 0.0, 0.028), mat=M["steel"], bevel=0.0015, parent=piv)
    C.rbox(name + "_lip", (0.03, 0.006, 0.004), (0, 0.003, 0.054), mat=M["steel"], bevel=0.0015, parent=piv)
    piv.rotation_euler = (math.radians(-55 * open_), 0, 0)
    return piv


def cigarette(loc=(0, 0, 0), rot=(0, 0, 0), lit=True, name="cig", glow=6.0):
    """8.4 cm cigarette along local X (ember end at +X). Returns (root empty, ember material, ember light)."""
    M = mats()
    root = C.empty(name, loc, rot)
    C.cyl(name + "_paper", 0.0039, 0.058, (0.008, 0, 0), rot=(0, math.radians(90), 0), mat=M["paper"], verts=24, parent=root)
    C.cyl(name + "_filter", 0.0040, 0.024, (-0.033, 0, 0), rot=(0, math.radians(90), 0), mat=M["filt"], verts=24, parent=root)
    C.cyl(name + "_ash", 0.0037, 0.004, (0.039, 0, 0), rot=(0, math.radians(90), 0), mat=M["ash"], verts=24, parent=root)
    em = C.emission(name + "_ember", EMBER, glow if lit else 0.0)
    C.cyl(name + "_tip", 0.0034, 0.0025, (0.0425, 0, 0), rot=(0, math.radians(90), 0), mat=em, verts=24, parent=root)
    lt = point(name + "_light", (0, 0, 0), EMBER, 0.35 if lit else 0.0, r=0.004)
    lt.parent = root; lt.location = (0.047, 0, 0)
    return root, em, lt


def towels(loc, w=0.24, d=0.18, n=26, seed=3, top=0.0):
    """Crumpled paper towels filling a bin: displaced ico spheres in white paper."""
    M = mats(); rnd = random.Random(seed); out = []
    tex = bpy.data.textures.new("crumple", "VORONOI"); tex.noise_scale = 0.015
    for i in range(n):
        r = rnd.uniform(0.028, 0.045)
        bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=3,
                                              location=(loc[0] + rnd.uniform(-w / 2 + r, w / 2 - r), loc[1] + rnd.uniform(-d / 2 + r, d / 2 - r),
                                                        loc[2] + rnd.uniform(0, top)))
        o = bpy.context.object; o.name = f"towel{i}"; o.data.materials.append(M["paper"])
        o.scale = (1.0, rnd.uniform(0.7, 1.0), rnd.uniform(0.5, 0.8)); o.rotation_euler = (rnd.random() * 3, rnd.random() * 3, rnd.random() * 3)
        md = o.modifiers.new("d", "DISPLACE"); md.texture = tex; md.strength = r * 0.45
        for p in o.data.polygons:
            p.use_smooth = False
        out.append(o)
    return out


def smoulder(loc):
    """A small glowing burn spot: an irregular ember-orange patch with a hot core (scale it up as the paper catches)."""
    root = C.empty("smoulder", loc)
    tex = bpy.data.textures.new("emb", "CLOUDS"); tex.noise_scale = 0.01
    for k, (r, col, st) in enumerate(((0.022, "#FF3A08", 30.0), (0.012, "#FFB040", 60.0))):
        bpy.ops.mesh.primitive_ico_sphere_add(radius=r, subdivisions=3, location=(0, 0, 0))
        o = bpy.context.object; o.name = f"emb{k}"; o.parent = root; o.scale = (1.0, 0.8, 0.45)
        md = o.modifiers.new("d", "DISPLACE"); md.texture = tex; md.strength = r * 0.6
        o.data.materials.append(C.emission(f"emb_e{k}", col, st))
    return root


def extinguisher(loc, name="ext"):
    """Small automatic lavatory extinguisher bottle with a heat-tipped nozzle tube bending down into the bin."""
    M = mats()
    x, y, z = loc
    C.cyl(name + "_bottle", 0.022, 0.13, (x, y, z), mat=C.pbr("extbottle", "#B8BCC2", 0.25, metal=0.95), verts=32, bevel=0.01)
    C.cyl(name + "_neck", 0.009, 0.025, (x, y, z + 0.077), mat=M["steel"], verts=20)
    pts = [(x, y, z + 0.09), (x, y, z + 0.11), (x - 0.03, y, z + 0.12), (x - 0.07, y, z + 0.11), (x - 0.09, y, z + 0.07)]
    C.tube(name + "_tube", pts, 0.004, mat=M["steel"], n=10)
    C.cyl(name + "_tip", 0.006, 0.014, (x - 0.09, y, z + 0.063), mat=C.pbr("exttip", "#C8312B", 0.4), verts=16)
    return Vector((x - 0.09, y, z + 0.055))


# ------------------------------------------------------------------ sets
def lav_door(M, ash_open=0.0):
    """Aisle side of the lavatory: wall panels either side, folding door with a centre crease, handle, sign and ashtray."""
    C.rbox("door_a", (DOOR_W / 2 - 0.004, 0.03, DOOR_H), (DOOR_X0 - DOOR_W / 4, DY - 0.015, DOOR_H / 2 + 0.02), mat=M["panel"], bevel=0.006)
    C.rbox("door_b", (DOOR_W / 2 - 0.004, 0.03, DOOR_H), (DOOR_X0 + DOOR_W / 4, DY - 0.015, DOOR_H / 2 + 0.02), mat=M["panel"], bevel=0.006)
    C.rbox("frame_l", (0.06, 0.06, DOOR_H + 0.1), (DOOR_X0 - DOOR_W / 2 - 0.03, DY - 0.01, DOOR_H / 2), mat=M["panel2"], bevel=0.01)
    C.rbox("frame_r", (0.06, 0.06, DOOR_H + 0.1), (DOOR_X0 + DOOR_W / 2 + 0.03, DY - 0.01, DOOR_H / 2), mat=M["panel2"], bevel=0.01)
    C.rbox("frame_t", (DOOR_W + 0.12, 0.06, 0.08), (DOOR_X0, DY - 0.01, DOOR_H + 0.08), mat=M["panel2"], bevel=0.01)
    for s in (-1, 1):
        C.rbox("wall", (1.2, 0.05, 2.3), (DOOR_X0 + s * (DOOR_W / 2 + 0.66), DY - 0.03, 1.15), mat=M["panel"], bevel=0.0)
    C.rbox("ceil", (3.0, 2.4, 0.04), (0, 1.0, 2.12), mat=M["panel"], bevel=0.0)
    C.rbox("galley", (0.05, 2.2, 2.2), (-0.95, 1.1, 1.1), mat=M["panel2"], bevel=0.0)
    for k in range(3):
        C.rbox("galley_box", (0.06, 0.42, 0.34), (-0.92, 0.35 + k * 0.46, 1.35), mat=C.pbr("galleysteel", "#AEB4BA", 0.3, metal=0.8), bevel=0.01)
        C.rbox("galley_latch", (0.07, 0.06, 0.02), (-0.91, 0.35 + k * 0.46, 1.48), mat=C.pbr("latch", "#C8312B", 0.4), bevel=0.004)
    C.rbox("galley_bench", (0.30, 1.4, 0.04), (-0.80, 0.9, 0.95), mat=C.pbr("galleysteel", "#AEB4BA", 0.3, metal=0.8), bevel=0.005)
    C.rbox("backwall", (3.0, 0.05, 2.2), (0, 2.2, 1.1), mat=M["panel"], bevel=0.0)
    C.rbox("curtain", (0.9, 0.03, 1.9), (0.6, 2.15, 1.0), mat=C.pbr("curtain", "#2E4A7A", 0.9, bump="weave", bscale=300, bstr=0.4), bevel=0.0)
    C.rbox("ceil_light", (1.6, 0.06, 0.01), (0, 0.5, 2.095), mat=C.emission("ceil_e", "#FFF1DC", 1.5), bevel=0.0)
    C.rbox("floor", (3.0, 2.4, 0.02), (0, 1.0, -0.01), mat=M["carpet"], bevel=0.0)
    C.rbox("kick", (DOOR_W + 0.2, 0.02, 0.12), (0, DY + 0.01, 0.06), mat=M["panel2"], bevel=0.002)
    hb = C.rbox("handle", (0.035, 0.03, 0.10), tuple(HANDLE), mat=M["steel"], bevel=0.008)
    C.rbox("vacant", (0.05, 0.006, 0.016), (HANDLE.x, DY + 0.003, HANDLE.z + 0.10), mat=C.emission("vac_e", "#3FD27A", 3.0), bevel=0.002)
    no_smoking(SIGN, 0.9)
    return ashtray(ASH, ash_open)


def lav_lights(target, key=80, fill=45, rim=70):
    C.area("cabin_top", (0.0, 0.7, 2.05), (0, 0, 0), 1.2, "#FFF1DC", key)
    C.area("cabin_fill", (0.9, 1.4, 1.3), (math.radians(80), 0, math.radians(140)), 1.0, "#DCE6FF", fill)
    C.area("cabin_rim", (-0.9, 0.2, 1.8), (math.radians(60), 0, math.radians(-120)), 0.6, "#FFD7B0", rim)


PX, PY = -0.16, 0.36                                          # passenger stands in front of the left door leaf, facing the aisle (camera)


def passenger(face_door=True):
    h = Hm.build(dict(PAX, loc=(PX, PY, 0), rot_z=180), "pax"); ct = Hm.controls(h)
    E = h["eye_c"].z
    ct["handR"].location = (PX + 0.20, PY + 0.06, E - 0.72); ct["handL"].location = (PX - 0.22, PY + 0.06, E - 0.72)
    return h, ct, E


CAMF = Vector((0.0, 0.0, 0.0))
POINT = ASH + Vector((-0.04, 0.16, 0.05))                     # her right hand points at the ashtray from ~15 cm away
REST = Vector((PX + 0.20, PY + 0.08, 0.86))


def door_cam(cam, n, a, b):
    """Hook framing: low beside the door, the ashtray big in the lower foreground, the passenger's face above it."""
    A = ((0.04, 1.02, 1.32), (0.02, 0.10, 1.24), 30)
    B = ((0.04, 0.96, 1.31), (0.02, 0.10, 1.24), 31)
    P0, P1 = (A, B) if a == 0 else (B, A)
    cam_move(cam, n, P0, P1, focus=(PX, PY, 1.45), fstop=5.6)


def door_set(n):
    M = mats(); P.world("#3A4A5A", 0.25)
    piv = lav_door(M)
    h, ct, E = passenger()
    lav_lights((0, 0.4, 1.4))
    C.area("facekey", (0.45, 1.0, E + 0.3), (math.radians(60), 0, math.radians(150)), 0.5, "#FFF1DC", 12.0)
    return M, piv, h, ct, E


def hook_door(sh, cam, n):
    """Frame 1: the passenger already reaching for the lavatory handle; she stops, eyes snap to the steel ashtray under the sign; flap pops."""
    M, piv, h, ct, E = door_set(n)
    key_obj(ct["handR"], 0, loc=tuple(REST.lerp(POINT, 0.45))); key_obj(ct["handR"], 10, loc=tuple(POINT))
    key_obj(ct["handR"], n, loc=tuple(POINT + Vector((0.0, 0.0, 0.015))))
    key_obj(ct["look"], 0, loc=(0.04, 1.0, 1.40)); key_obj(ct["look"], 26, loc=(0.04, 1.0, 1.40))
    key_obj(ct["look"], 38, loc=tuple(ASH + Vector((0, 0.3, 0.3)))); key_obj(ct["look"], 56, loc=tuple(ASH + Vector((0, 0.3, 0.3))))
    key_obj(ct["look"], min(n, 70), loc=(0.04, 1.0, 1.38))
    Hm.face(h["keys"], 0, wide=1.0, brows_up=0.9, open=0.35); Hm.face(h["keys"], 18, wide=1.0, brows_up=0.9, open=0.35)
    Hm.face(h["keys"], n, wide=0.8, brows_up=0.6, browL_up=0.4, open=0.15)
    key_obj(piv, 0, rot=(0, 0, 0)); key_obj(piv, 16, rot=(0, 0, 0)); key_obj(piv, 22, rot=(math.radians(-40), 0, 0)); key_obj(piv, n, rot=(math.radians(-40), 0, 0))
    door_cam(cam, n, 0, 1)


def loop_door(sh, cam, n):
    """Last shot: same framing; she gives the ashtray a small nod, the flap swings shut, her hand goes back to the handle,
    ending on hook_door's first frame (loop)."""
    M, piv, h, ct, E = door_set(n)
    key_obj(ct["handR"], 0, loc=tuple(REST)); key_obj(ct["handR"], n - 16, loc=tuple(REST)); key_obj(ct["handR"], n, loc=tuple(REST.lerp(POINT, 0.45)))
    key_obj(ct["look"], 0, loc=(0.04, 1.0, 1.38)); key_obj(ct["look"], 20, loc=(0.04, 1.0, 1.32))
    key_obj(ct["look"], 30, loc=(0.04, 1.0, 1.40)); key_obj(ct["look"], n, loc=(0.04, 1.0, 1.40))
    Hm.face(h["keys"], 0, smile=0.3, browL_up=0.3); Hm.face(h["keys"], 30, smile=0.55, squint=0.2)
    Hm.face(h["keys"], n - 8, smile=0.2); Hm.face(h["keys"], n, wide=1.0, brows_up=0.9, open=0.35, smile=0.0, squint=0.0, browL_up=0.0)
    key_obj(piv, 0, rot=(math.radians(-40), 0, 0)); key_obj(piv, n - 20, rot=(math.radians(-40), 0, 0)); key_obj(piv, n - 12, rot=(0, 0, 0))
    life(h, n - 12, 4)
    door_cam(cam, n, 1, 0)


def loop_ots(sh, cam, n):
    """'So this ashtray isn't for smokers': close on her face from the door side, she studies the ashtray, head tilting, small smile."""
    M, piv, h, ct, E = door_set(n)
    piv.rotation_euler = (math.radians(-40), 0, 0)
    ct["handR"].location = tuple(REST)
    key_obj(ct["look"], 0, loc=tuple(ASH + Vector((0.0, 0.35, 0.35)))); key_obj(ct["look"], 18, loc=tuple(ASH + Vector((0.0, 0.35, 0.35))))
    key_obj(ct["look"], n, loc=(PX + 0.1, 0.95, 1.52))
    Hm.face(h["keys"], 0, squint=0.25, browL_up=0.3); Hm.face(h["keys"], n, smile=0.3, browL_up=0.3)
    life(h, n, 6)
    cam_move(cam, n, ((PX + 0.12, 0.98, 1.50), (PX, PY, 1.45), 42), ((PX + 0.10, 0.93, 1.50), (PX, PY, 1.45), 46), focus=(PX, PY + 0.08, 1.50), fstop=2.8)


def cabin(M):
    """Generic single-aisle cabin looking aft from the front: 3+3 navy seats, overhead bins, ceiling signs, window light."""
    P.world("#5A6E86", 0.6)
    C.rbox("cfloor", (3.6, 14, 0.02), (0, -6.0, -0.01), mat=M["carpet"], bevel=0.0)
    C.rbox("aisle_strip", (0.5, 14, 0.004), (0, -6.0, 0.002), mat=C.pbr("aislecarpet", "#2E3A52", 0.95, bump="weave", bscale=500, bstr=0.4), bevel=0.0)
    for s in (-1, 1):
        C.rbox("sidewall", (0.05, 14, 1.6), (s * 1.75, -6.0, 1.05), mat=M["panel"], bevel=0.0)
        C.rbox("bin", (0.62, 14, 0.36), (s * 1.42, -6.0, 1.82), mat=M["panel"], bevel=0.04)
        C.rbox("bin_lip", (0.64, 14, 0.03), (s * 1.42, -6.0, 1.63), mat=M["panel2"], bevel=0.01)
        for i in range(12):
            y = -0.6 - i * 0.82
            C.rbox("win", (0.02, 0.24, 0.34), (s * 1.72, y, 1.15), mat=C.emission("win_e", "#CFE6FF", 3.0), bevel=0.06)
    C.rbox("cceil", (2.2, 14, 0.04), (0, -6.0, 2.15), mat=M["panel"], bevel=0.0)
    C.rbox("cceil_lt", (0.9, 14, 0.01), (0, -6.0, 2.125), mat=C.emission("cceil_e", "#FFF1DC", 1.2), bevel=0.0)
    for s in (-1, 1):
        C.rbox("cove", (0.05, 14, 0.02), (s * 0.95, -6.0, 2.10), mat=C.emission("cove_e", "#9FC8FF", 3.0), bevel=0.0)
    seat_back = C.rbox("seatback", (0.46, 0.12, 0.72), (0, 0, 0), mat=M["seat"], bevel=0.03, subsurf=1)
    cush = C.rbox("cushion", (0.46, 0.46, 0.12), (0, 0, 0), mat=M["seat"], bevel=0.03, subsurf=1)
    hc = C.rbox("headcover", (0.40, 0.125, 0.18), (0, 0, 0), mat=M["head"], bevel=0.02)
    arm = C.rbox("armrest", (0.05, 0.42, 0.05), (0, 0, 0), mat=M["panel2"], bevel=0.01)
    def dup(o, loc, rx=0.0):
        c = o.copy(); bpy.context.scene.collection.objects.link(c); c.location = loc; c.rotation_euler = (rx, 0, 0); return c
    for r in range(11):
        y = -0.9 - r * 0.82
        for s in (-1, 1):
            for k in range(3):
                x = s * (0.42 + k * 0.47)
                dup(seat_back, (x, y + 0.02, 0.86), math.radians(-8)); dup(cush, (x, y - 0.24, 0.46)); dup(hc, (x, y + 0.01, 1.14), math.radians(-8))
            dup(arm, (s * 0.18, y - 0.22, 0.62)); dup(arm, (s * 1.62, y - 0.22, 0.62))
    for o in (seat_back, cush, hc, arm):
        bpy.data.objects.remove(o, do_unlink=True)


def cabin_sign(sh, cam, n):
    """'Smoking on every US flight has been banned since 2000': cabin aisle; the ceiling no-smoking signs light up row by row with a chime."""
    M = mats(); cabin(M)
    for r in range(8):
        y = -0.6 - r * 1.64
        lit = C.emission(f"sign_lit{r}", "#FFFFFF", 0.0)
        for s in (-1, 1):
            C.rbox("psu", (0.14, 0.03, 0.14), (s * 0.62, y - 0.02, 1.96), mat=M["panel2"], bevel=0.01)
            no_smoking((s * 0.62, y, 1.96), 1.2, lit=lit, name=f"ns{r}{s}")
        f0 = 6 + r * 4
        key_emit(lit, 0, 0.15); key_emit(lit, f0, 0.15); key_emit(lit, f0 + 3, 3.5); key_emit(lit, n, 3.5)
    C.area("ckey", (0, -2.5, 2.0), (0, 0, 0), 2.0, "#FFF1DC", 160)
    C.area("cfill", (0, 1.0, 1.4), (math.radians(90), 0, 0), 2.0, "#DCE6FF", 120)
    cam_move(cam, n, ((0.0, 0.6, 1.45), (0.0, -6.0, 1.45), 26), ((0.0, 0.2, 1.42), (0.0, -6.0, 1.5), 27), focus=(0, -2.5, 1.6), fstop=6.3)


def _ash_closeup():
    M = mats(); P.world("#3A4A5A", 0.5)
    piv = lav_door(M)
    lav_lights((0, 0.3, 1.0))
    C.area("ashkey", (0.35, 0.45, 1.25), (math.radians(60), 0, math.radians(140)), 0.3, "#FFF1DC", 14.0)
    return M, piv


def ashtray_macro(sh, cam, n):
    """'yet the rules still demand an ashtray on every toilet door': slow orbit close to the ashtray, the flap tips open."""
    M, piv = _ash_closeup()
    f0 = W_(sh, "ashtray", 1.6)
    key_obj(piv, 0, rot=(0, 0, 0)); key_obj(piv, max(1, f0 - 4), rot=(0, 0, 0)); key_obj(piv, f0 + 6, rot=(math.radians(-50), 0, 0)); key_obj(piv, n, rot=(math.radians(-50), 0, 0))
    cam_move(cam, n, ((0.42, 0.42, 1.18), tuple(ASH + Vector((0, 0, 0.04))), 46), ((0.02, 0.40, 1.15), tuple(ASH + Vector((0, 0, 0.03))), 50),
             focus=tuple(ASH), fstop=5.6)


def stub_out(sh, cam, n):
    """'one obvious, safe place to put it out first': the lit cigarette lies on the open ashtray tray; the flap closes on it, the glow dies."""
    M, piv = _ash_closeup()
    cg, em, lt = cigarette((ASH.x - 0.003, ASH.y + 0.052, ASH.z - 0.020), rot=(0, 0, math.radians(4)), name="cig")
    fc = W_(sh, "out", 1.6)
    key_obj(piv, 0, rot=(math.radians(-52), 0, 0)); key_obj(piv, max(1, fc - 6), rot=(math.radians(-52), 0, 0)); key_obj(piv, fc + 3, rot=(0, 0, 0))
    key_emit(em, 0, 6.0); key_emit(em, fc + 2, 6.0); key_emit(em, fc + 14, 0.0)
    key_energy(lt, 0, 0.35); key_energy(lt, fc + 2, 0.35); key_energy(lt, fc + 14, 0.0)
    cam_move(cam, n, ((0.10, 0.30, 1.14), tuple(ASH + Vector((0, 0, -0.01))), 55), ((0.07, 0.26, 1.12), tuple(ASH + Vector((0, 0, -0.01))), 60),
             focus=tuple(ASH + Vector((0, 0, -0.02))), fstop=6.3)


def cig_fall(sh, cam, n):
    """'It's where the cigarette ends up': slow motion, a lit cigarette tumbles down through a dark studio, ember glowing."""
    P.world("#0E1A2A", 0.25)
    P.studio(top="#0E2A44", bottom="#1B3A5C", mid="#14304E", y0=0.6, glow=0.25, height=4.0, width=8.0, depth=3.0)
    cg, em, lt = cigarette((0, 0, 1.35), name="cig", glow=9.0)
    lt.data.energy = 0.6
    for f in range(0, n + 1, 3):
        u = f / max(1, n)
        key_obj(cg, f, loc=(0.01 * math.sin(u * 3), 0, 1.35 - 0.28 * u), rot=(0.3 + u * 1.4, 0.2, -0.4 + u * 2.6))
    P.lights((0, 0, 1.2), key=200, rim=260, fill=60, scale=0.5)
    cam_move(cam, n, ((0.0, -0.32, 1.40), (0.0, 0.0, 1.33), 50), ((0.0, -0.30, 1.12), (0.0, 0.0, 1.08), 52), focus=(0, 0, 1.22), fstop=4.0)


# ------------------------------------------------------------------ inside the lavatory
LAV_Y = -0.9                                                  # cabinet front plane inside the lavatory (cabinet occupies y < LAV_Y)
BIN = Vector((0.0, LAV_Y - 0.17, 0.30))


def lav_inside(M, xray=False):
    """Lavatory cabinet under the basin: counter + steel basin, the waste flap, and (xray) a see-through front showing the bin."""
    P.world("#4A5A6A", 0.5)
    front = C.ghost("xray_front", "#9FD8FF", glow=0.9, core=0.02) if xray else M["panel"]
    C.rbox("cab_front", (0.62, 0.02, 0.78), (0, LAV_Y + 0.01, 0.39), mat=front, bevel=0.004)
    for s in (-1, 1):
        C.rbox("cab_side", (0.02, 0.4, 0.78), (s * 0.31, LAV_Y - 0.19, 0.39), mat=front if xray else M["panel2"], bevel=0.003)
    C.rbox("counter", (0.66, 0.44, 0.04), (0, LAV_Y - 0.2, 0.80), mat=M["panel2"], bevel=0.01)
    C.cyl("basin", 0.13, 0.035, (0.1, LAV_Y - 0.2, 0.815), mat=M["steel"], verts=48)
    C.cyl("basin_in", 0.115, 0.02, (0.1, LAV_Y - 0.2, 0.825), mat=C.pbr("basin_in", "#9DA3AA", 0.2, metal=1.0), verts=48)
    C.cyl("tap", 0.012, 0.12, (0.1, LAV_Y - 0.36, 0.88), mat=M["steel"], verts=20)
    C.rbox("flap_frame", (0.20, 0.012, 0.11), (-0.16, LAV_Y + 0.02, 0.68), mat=M["steel"], bevel=0.004)
    piv = C.empty("flap_hinge", (-0.16, LAV_Y + 0.026, 0.725))
    C.rbox("flap", (0.17, 0.006, 0.085), (0, 0, -0.043), mat=C.pbr("flapsteel", "#B9BEC4", 0.3, metal=0.9), bevel=0.002, parent=piv)
    C.rbox("wall_back", (2.0, 0.04, 2.2), (0, LAV_Y - 0.45, 1.1), mat=M["panel"], bevel=0.0)
    C.rbox("lfloor", (2.0, 2.0, 0.02), (0, LAV_Y + 0.6, -0.01), mat=C.pbr("lavfloor", "#5E6670", 0.6, bump="noise", bscale=600, bstr=0.1), bevel=0.0)
    C.rbox("mirror", (0.6, 0.01, 0.5), (0, LAV_Y - 0.43, 1.3), mat=C.pbr("mirror", "#DDE3EA", 0.03, metal=1.0), bevel=0.003)
    for s in (-1, 1):
        C.rbox("lav_side", (0.04, 1.6, 2.2), (s * 0.62, LAV_Y + 0.35, 1.1), mat=M["panel"], bevel=0.0)
    C.rbox("lav_ceil", (1.3, 1.6, 0.04), (0, LAV_Y + 0.35, 2.1), mat=M["panel"], bevel=0.0)
    C.rbox("lav_door_in", (1.3, 0.04, 2.2), (0, LAV_Y + 1.15, 1.1), mat=M["panel2"], bevel=0.0)
    if xray:
        C.rbox("bin_box", (0.40, 0.30, 0.42), (BIN.x - 0.06, BIN.y, 0.26), mat=C.ghost("xray_bin", "#7FC4FF", glow=0.7, core=0.03), bevel=0.01)
        C.rbox("chute", (0.18, 0.16, 0.1), (-0.16, LAV_Y - 0.06, 0.60), rot=(math.radians(25), 0, 0), mat=C.ghost("xray_chute", "#7FC4FF", glow=0.6, core=0.03), bevel=0.005)
    C.area("lav_top", (0, LAV_Y + 0.2, 2.0), (0, 0, 0), 0.8, "#FFF1DC", 140)
    C.area("lav_fill", (0.6, LAV_Y + 1.1, 1.0), (math.radians(75), 0, math.radians(160)), 0.8, "#DCE6FF", 90)
    return piv


def bin_flap(sh, cam, n):
    """'Someone who breaks the rule panics and hides it': the spring flap under the basin swings in, a lit cigarette slips through, flap snaps back."""
    M = mats(); piv = lav_inside(M)
    cg, em, lt = cigarette((-0.16, LAV_Y + 0.08, 0.70), rot=(0, 0, math.radians(90)), name="cig")
    f0 = W_(sh, "hides", 1.2)
    key_obj(cg, 0, loc=(-0.16, LAV_Y + 0.12, 0.70), rot=(0, math.radians(-10), math.radians(95)))
    key_obj(cg, f0, loc=(-0.16, LAV_Y + 0.05, 0.69)); key_obj(cg, f0 + 10, loc=(-0.16, LAV_Y - 0.06, 0.64), rot=(0, math.radians(-35), math.radians(95)))
    key_obj(piv, 0, rot=(0, 0, 0)); key_obj(piv, max(1, f0 - 2), rot=(0, 0, 0)); key_obj(piv, f0 + 4, rot=(math.radians(-45), 0, 0))
    key_obj(piv, f0 + 12, rot=(math.radians(-45), 0, 0)); key_obj(piv, f0 + 18, rot=(math.radians(6), 0, 0)); key_obj(piv, f0 + 22, rot=(0, 0, 0))
    cam_move(cam, n, ((0.18, LAV_Y + 0.62, 0.92), (-0.14, LAV_Y, 0.66), 34), ((0.12, LAV_Y + 0.52, 0.86), (-0.15, LAV_Y, 0.66), 38),
             focus=(-0.16, LAV_Y + 0.02, 0.68), fstop=4.5)


def bin_xray(sh, cam, n):
    """'the nearest hiding spot is a bin full of paper towels': X-ray cut-away of the cabinet: the bin heaped with paper towels,
    the cigarette lands on top and its glow grows into the paper."""
    M = mats(); lav_inside(M, xray=True)
    towels((BIN.x - 0.06, BIN.y, 0.10), w=0.36, d=0.26, n=34, seed=3, top=0.26)
    cg, em, lt = cigarette((-0.12, BIN.y + 0.05, 0.62), rot=(0.3, 0.2, 0.4), name="cig", glow=9.0)
    fl = W_(sh, "bin", 1.0)
    key_obj(cg, 0, loc=(-0.15, LAV_Y - 0.06, 0.58), rot=(0.3, -0.5, 1.4)); key_obj(cg, fl + 6, loc=(-0.10, BIN.y + 0.02, 0.43), rot=(0.1, 0.1, 0.9))
    glow = point("hot", (-0.10, BIN.y + 0.02, 0.41), "#FF6A20", 0.0, r=0.03)
    fp = W_(sh, "paper", 2.0)
    key_energy(glow, 0, 0.0); key_energy(glow, fl + 6, 0.4); key_energy(glow, fp, 2.5); key_energy(glow, n, 8.0)
    sm = smoulder((-0.10, BIN.y + 0.02, 0.405))
    key_obj(sm, 0, scale=0.0); key_obj(sm, fl + 6, scale=0.2); key_obj(sm, fp, scale=0.7); key_obj(sm, n, scale=1.3)
    key_energy(lt, 0, 0.6)
    cam_move(cam, n, ((0.48, LAV_Y + 0.75, 0.78), (-0.06, BIN.y, 0.34), 30), ((0.40, LAV_Y + 0.62, 0.70), (-0.08, BIN.y, 0.36), 34),
             focus=(-0.08, BIN.y + 0.05, 0.40), fstop=5.6)


def ext_shot(sh, cam, n):
    """'That bin even has its own tiny fire extinguisher': X-ray close on the steel bottle in the cabinet; its nozzle fires a white puff
    into the bin and the hot glow is gone."""
    M = mats(); lav_inside(M, xray=True)
    towels((BIN.x - 0.06, BIN.y, 0.10), w=0.36, d=0.26, n=34, seed=3, top=0.26)
    nz = extinguisher((0.12, BIN.y - 0.02, 0.30))
    glow = point("hot", (-0.06, BIN.y + 0.02, 0.41), "#FF6A20", 8.0, r=0.03)
    sm = smoulder((-0.06, BIN.y + 0.02, 0.405))
    ff = W_(sh, "extinguisher", 1.2)
    key_energy(glow, 0, 8.0); key_energy(glow, ff + 2, 8.0); key_energy(glow, ff + 14, 0.0)
    key_obj(sm, 0, scale=1.0); key_obj(sm, ff + 2, scale=1.0); key_obj(sm, ff + 14, scale=0.0)
    ps = P.gas_puffs(origin=tuple(nz), n=40, spread=0.01, seed=9, color="#F4F8FF", size=0.01)
    for i, p in enumerate(ps):
        rnd = random.Random(i); d = Vector((rnd.uniform(-0.12, -0.02), rnd.uniform(-0.06, 0.06), rnd.uniform(-0.12, 0.02)))
        a = ff + rnd.randint(0, 6)
        key_obj(p, 0, loc=tuple(nz), scale=0.0); key_obj(p, a, loc=tuple(nz), scale=0.0)
        key_obj(p, a + 10, loc=tuple(nz + d), scale=2.2); key_obj(p, min(n, a + 30), loc=tuple(nz + d * 1.4), scale=0.0)
    cam_move(cam, n, ((0.40, LAV_Y + 0.42, 0.52), (0.02, BIN.y, 0.36), 36), ((0.33, LAV_Y + 0.38, 0.50), (0.0, BIN.y, 0.36), 40),
             focus=(0.04, BIN.y, 0.38), fstop=5.6)


def detector(sh, cam, n):
    """'and a smoke detector watches the room': looking up at the lavatory ceiling, a round smoke detector, its green light blinking."""
    M = mats(); P.world("#4A5A6A", 0.5)
    Z = 2.05
    C.rbox("lceil", (1.4, 1.4, 0.03), (0, 0, Z + 0.015), mat=M["panel"], bevel=0.0)
    for s in (-1, 1):
        C.rbox("lwall", (0.03, 1.4, 2.2), (s * 0.55, 0, Z - 1.1), mat=M["panel2"], bevel=0.0)
    C.rbox("lwall_b", (1.2, 0.03, 2.2), (0, -0.6, Z - 1.1), mat=M["panel"], bevel=0.0)
    C.rbox("lwall_f", (1.2, 0.03, 2.2), (0, 0.7, Z - 1.1), mat=M["panel"], bevel=0.0)
    C.rbox("lmirror", (0.5, 0.01, 0.45), (0, -0.585, 1.3), mat=C.pbr("mirror", "#DDE3EA", 0.03, metal=1.0), bevel=0.003)
    C.rbox("llight", (0.5, 0.12, 0.012), (0, 0.32, Z - 0.006), mat=C.emission("ll_e", "#FFF1DC", 5.0), bevel=0.004)
    C.cyl("det_base", 0.06, 0.02, (0, -0.05, Z - 0.01), mat=M["white"], verts=48, bevel=0.006)
    C.cyl("det_dome", 0.045, 0.022, (0, -0.05, Z - 0.03), mat=M["white"], verts=48, bevel=0.01)
    for i in range(12):
        a = i * math.pi / 6
        C.rbox("slot", (0.012, 0.004, 0.012), (0.047 * math.cos(a), -0.05 + 0.047 * math.sin(a), Z - 0.03), rot=(0, 0, a), mat=M["dark"], bevel=0.0)
    led = C.emission("led", "#3FFF7A", 0.0)
    C.cyl("det_led", 0.004, 0.004, (0.028, -0.05, Z - 0.042), mat=led, verts=12)
    for f in range(0, n + 1, 12):
        key_emit(led, f, 12.0); key_emit(led, min(n, f + 4), 0.2)
    C.area("dkey", (0.3, 0.6, 1.0), (math.radians(-60), 0, math.radians(30)), 0.6, "#FFF1DC", 40)
    cam_move(cam, n, ((0.10, 0.35, 1.55), (0.0, -0.05, Z - 0.03), 40), ((0.05, 0.28, 1.62), (0.0, -0.05, Z - 0.03), 46),
             focus=(0, -0.05, Z - 0.03), fstop=5.6)


SHOTS = {f.__name__: f for f in (hook_door, cabin_sign, ashtray_macro, cig_fall, bin_flap, bin_xray, stub_out, ext_shot, detector,
                                 loop_ots, loop_door)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
