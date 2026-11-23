"""A-019 Style R scenes (Blender): "Why is AMBULANCE written backwards?". Renders every shot of shots.json as frames.
/opt/c3d/bin/python -I scene.py <shots.json> <out_dir> [--w 540 --h 960 --samples 12 --step 3 --shots a,b --gpu --part 0/2 --mblur --measure]
Our own generic ambulance (white van, coral/blue stripes, red/blue lights; no real service's livery, no protected emblems),
a yellow hatchback with a real Cycles mirror (the rear-view reflection is physically correct, so the mirrored word reads normally in it),
our MPFB cast on a studio backdrop in our colours.
"""
import sys, os, math, glob
HERE = os.path.dirname(os.path.abspath(__file__))
for p in (HERE, os.path.join(HERE, "..", "..", "lib", "style_r"), os.path.join(HERE, "..", "..", "lib")):
    if os.path.isdir(p) and p not in sys.path:
        sys.path.insert(0, p)
import bpy
from mathutils import Vector
import sr_common as C, sr_props as P, sr_human as Hm
from sr_shot import key_obj, cam_move, W_, life

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]

PED = dict(macro={"gender": 1, "age": 0.42, "muscle": 0.5, "weight": 0.5, "proportions": 0.6, "height": 0.55}, skin="#D9A27C",
           hair="#2A170C", shirt="#FF6B5B", trousers="#2B3440", shoes="#F4F1EA", iris="#4A3A2C",
           shirt_push=0.02, shirt_iters=40, tuck=0.025)   # pedestrian, coral tee (loose + extra smoothing: no chest detail, QA 23 Nov)
DRV = dict(macro={"gender": 0, "age": 0.38, "muscle": 0.45, "weight": 0.45, "proportions": 0.6, "height": 0.5}, skin="#C68E64",
           hair="#1E120A", hair_style="bun", shirt="#5ED3B5", trousers="#2B3440", shoes="#F4F1EA", iris="#3A2416", sleeve="long")  # driver, mint top
EMT = dict(macro={"gender": 1, "age": 0.5, "muscle": 0.55, "weight": 0.55, "proportions": 0.55, "height": 0.5}, skin="#8E5A3C",
           hair="#141010", shirt="#1F3A66", trousers="#1F2A3F", shoes="#1A1A1A", iris="#2E1E12", sleeve="short")            # paramedic, navy uniform
WHITE, BLUE, CORAL, NAVY = "#F2F2EE", "#1F4FA8", "#FF6B5B", "#1F2A44"
WORD = "AMBULANCE"


def font():
    for d in (HERE, os.path.join(HERE, "..", "..", "library", "fonts")):
        f = os.path.join(d, "Poppins-ExtraBold.ttf")
        if os.path.exists(f):
            return bpy.data.fonts.load(f, check_existing=True)
    return None


def text3d(txt, loc, size, mat, mirror=False, rot=(90, 0, 0), extrude=0.004, name="txt", both=False):
    """Block letters standing in the XZ plane, reading left->right for a viewer on -Y (mirror=True: printed flipped).
    both=True adds a second copy facing +Y that reads normally from behind (a card printed on both sides)."""
    cu = bpy.data.curves.new(name, "FONT"); cu.body = txt; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    cu.size = size; cu.extrude = extrude
    f = font()
    if f:
        cu.font = f
    o = bpy.data.objects.new(name, cu); bpy.context.scene.collection.objects.link(o)
    o.data.materials.append(mat); o.location = loc; o.rotation_euler = [math.radians(a) for a in rot]
    if mirror:
        o.scale = (-1, 1, 1)
    if both:
        b = text3d(txt, (loc[0], loc[1] + 2 * extrude + 0.004, loc[2]), size, mat, rot=(rot[0], rot[1], rot[2] + 180), extrude=extrude, name=name + "_back")
        return o, b
    return o


def set_stage(top="#2E5E86", bottom="#E9C9A0", mid="#E7A07A", y0=14.0, flip=False, road=True, road_y=(-12, 16)):
    P.world(top, 0.6); cyc = P.studio(top=top, bottom=bottom, mid=mid, y0=y0, glow=0.55, height=22.0, width=60.0, depth=26.0)
    if flip:
        cyc.rotation_euler = (0, 0, math.pi)
    if road:
        L = road_y[1] - road_y[0]; yc = (road_y[0] + road_y[1]) / 2
        C.rbox("road", (5.2, L, 0.01), (0, yc, 0.005), mat=C.pbr("asphalt", "#4A4F5A", 0.85, bump="noise", bstr=0.15), bevel=0.0)
        for sx in (-2.45, 2.45):
            C.rbox("edge", (0.12, L, 0.012), (sx, yc, 0.007), mat=C.pbr("paint", "#F4F1EA", 0.6), bevel=0.0)
    return cyc


def flasher(n, lights_red, lights_blue, mats_red, mats_blue, period=9, e_red=900.0, e_blue=1100.0, s_red=18.0, s_blue=22.0, phase=0):
    """Alternating red/blue flashes (near-square wave): emission strengths + coloured point lights."""
    for f0 in range(-period, n + period, period):
        on_red = ((f0 // period) + phase) % 2 == 0
        for f in (f0, f0 + period - 2):
            for L in lights_red:
                L.data.energy = e_red if on_red else e_red * 0.04; L.data.keyframe_insert("energy", frame=f)
            for L in lights_blue:
                L.data.energy = e_blue if not on_red else e_blue * 0.04; L.data.keyframe_insert("energy", frame=f)
            for m in mats_red:
                s = m.node_tree.nodes["Emission"].inputs["Strength"]; s.default_value = s_red if on_red else 0.4; s.keyframe_insert("default_value", frame=f)
            for m in mats_blue:
                s = m.node_tree.nodes["Emission"].inputs["Strength"]; s.default_value = s_blue if not on_red else 0.4; s.keyframe_insert("default_value", frame=f)


def point(name, loc, col, energy, r=0.15):
    d = bpy.data.lights.new(name, "POINT"); d.energy = energy; d.color = C.srgb(col)[:3]; d.shadow_soft_size = r
    o = bpy.data.objects.new(name, d); bpy.context.scene.collection.objects.link(o); o.location = loc
    return o


def ambulance(F=0.0, x=0.0, n=100, phase=0, glow=1.0):
    """Generic box ambulance, front face at y=F, facing -Y. Mirrored AMBULANCE on the hood front. Returns dict(word=obj, z=word height)."""
    wm = C.pbr("amb_white", WHITE, 0.35, coat=0.5)
    dark = C.pbr("amb_dark", "#23262E", 0.5)
    for wy in (F + 0.75, F + 4.7):
        for sx in (-1.0, 1.0):
            C.cyl("wheel", 0.38, 0.28, (x + sx, wy, 0.38), rot=(0, math.radians(90), 0), mat=C.pbr("tyre", "#17181C", 0.7), verts=40, bevel=0.03)
            C.cyl("hub", 0.18, 0.29, (x + sx, wy, 0.38), rot=(0, math.radians(90), 0), mat=C.pbr("hub", "#C9CDD4", 0.3, metal=0.8), verts=32)
    C.rbox("hood", (2.0, 1.1, 0.78), (x, F + 0.55, 0.77), mat=wm, bevel=0.05)
    C.rbox("bumper", (2.06, 0.18, 0.17), (x, F - 0.01, 0.44), mat=dark, bevel=0.03)
    C.rbox("grille", (1.0, 0.02, 0.2), (x, F - 0.005, 0.66), mat=C.pbr("grille", "#2A2F3A", 0.4, bump="grille", bstr=0.4), bevel=0.01)
    for sx in (-0.74, 0.74):
        C.rbox("headlight", (0.3, 0.03, 0.14), (x + sx, F - 0.01, 0.68), mat=C.pbr("hl", "#FFF6E0", 0.1, emit="#FFF6E0", estr=1.2 * glow), bevel=0.02)
    C.rbox("cab", (2.0, 1.35, 0.86), (x, F + 1.77, 1.58), mat=wm, bevel=0.06)
    C.rbox("windshield", (1.78, 0.03, 0.58), (x, F + 1.09, 1.62), mat=C.pbr("ws", "#1C2A3C", 0.06, coat=1.0), bevel=0.03)
    C.rbox("module", (2.3, 3.95, 2.3), (x, F + 4.42, 1.58), mat=wm, bevel=0.06)
    C.rbox("modstripe", (2.32, 0.02, 0.16), (x, F + 2.44, 2.05), mat=C.pbr("coral", CORAL, 0.4), bevel=0.0)
    C.rbox("modstripe2", (2.32, 0.02, 0.07), (x, F + 2.44, 1.92), mat=C.pbr("blue", BLUE, 0.4), bevel=0.0)
    for sx in (-1.0, 1.0):
        C.rbox("sidestripe", (0.02, 6.2, 0.16), (x + sx * 1.16, F + 3.3, 1.22), mat=C.pbr("coral", CORAL, 0.4), bevel=0.0)
        C.rbox("sidestripe", (0.02, 1.1, 0.12), (x + sx * 1.005, F + 0.55, 0.98), mat=C.pbr("coral", CORAL, 0.4), bevel=0.0)
    red, blue = C.emission("e_red_%d" % phase, "#FF2A2A", 18.0), C.emission("e_blue_%d" % phase, "#2A6BFF", 22.0)
    # light bar on the cab roof + module corner lights
    C.rbox("bar", (1.5, 0.28, 0.06), (x, F + 1.35, 2.04), mat=dark, bevel=0.02)
    C.rbox("bar_r", (0.6, 0.24, 0.1), (x - 0.42, F + 1.35, 2.1), mat=red, bevel=0.03)
    C.rbox("bar_b", (0.6, 0.24, 0.1), (x + 0.42, F + 1.35, 2.1), mat=blue, bevel=0.03)
    C.rbox("bar_w", (0.2, 0.24, 0.1), (x, F + 1.35, 2.1), mat=C.emission("e_white", "#FFFFFF", 4.0), bevel=0.03)
    C.rbox("corner_r", (0.26, 0.06, 0.18), (x - 0.98, F + 2.4, 2.58), mat=red, bevel=0.02)
    C.rbox("corner_b", (0.26, 0.06, 0.18), (x + 0.98, F + 2.4, 2.58), mat=blue, bevel=0.02)
    lr = [point("pl_r", (x - 0.5, F + 1.0, 2.15), "#FF3030", 900), point("pl_r2", (x - 0.98, F + 2.2, 2.6), "#FF3030", 500)]
    lb = [point("pl_b", (x + 0.5, F + 1.0, 2.15), "#3070FF", 1100), point("pl_b2", (x + 0.98, F + 2.2, 2.6), "#3070FF", 600)]
    flasher(n, lr, lb, [red], [blue], phase=phase, e_red=900 * glow, e_blue=1100 * glow)
    wz = 0.98
    word = text3d(WORD, (x, F - 0.006, wz), 0.27, C.pbr("word_blue", BLUE, 0.3), mirror=True, name="word")
    return dict(word=word, z=wz, F=F)


def car(CF=0.0, n=100, col="#22A89A", mirror_to=None, eye=None):
    """Yellow hatchback facing -Y, front at y=CF. Open side/rear windows (clean view in), glass windshield, real mirror.
    mirror_to: world point the rear-view mirror should reflect into the driver's eye (aims the mirror like a real driver would)."""
    body = C.pbr("car_paint", col, 0.3, coat=0.8)
    trim = C.pbr("car_trim", "#22252C", 0.5)
    C.rbox("car_body", (1.76, 4.1, 0.62), (0, CF + 2.05, 0.62), mat=body, bevel=0.12)
    for wy in (CF + 0.8, CF + 3.3):
        for sx in (-0.84, 0.84):
            C.cyl("cwheel", 0.32, 0.24, (sx, wy, 0.32), rot=(0, math.radians(90), 0), mat=C.pbr("tyre", "#17181C", 0.7), verts=40, bevel=0.03)
    C.rbox("cbumper_f", (1.8, 0.16, 0.18), (0, CF - 0.02, 0.42), mat=trim, bevel=0.05)
    C.rbox("cbumper_r", (1.8, 0.16, 0.18), (0, CF + 4.12, 0.42), mat=trim, bevel=0.05)
    for sx in (-0.62, 0.62):
        C.rbox("chead", (0.32, 0.03, 0.12), (sx, CF - 0.005, 0.72), mat=C.pbr("hl", "#FFF6E0", 0.1, emit="#FFF6E0", estr=1.0), bevel=0.02)
        C.rbox("ctail", (0.3, 0.03, 0.12), (sx, CF + 4.105, 0.78), mat=C.pbr("tl", "#C8202A", 0.2, emit="#FF2030", estr=0.8), bevel=0.02)
    for sx in (-0.93, 0.93):
        C.rbox("wingmirror", (0.1, 0.12, 0.09), (sx, CF + 1.5, 1.0), mat=body, bevel=0.03)
    C.rbox("roof", (1.62, 1.75, 0.07), (0, CF + 2.45, 1.44), mat=body, bevel=0.03)
    for sx in (-0.77, 0.77):
        a = C.rbox("apillar", (0.07, 0.07, 0.64), (sx, CF + 1.38, 1.17), mat=body, bevel=0.02); a.rotation_euler = (math.radians(-38.7), 0, 0)
        C.rbox("cpillar", (0.07, 0.12, 0.52), (sx, CF + 3.28, 1.18), mat=body, bevel=0.02)
    ws = C.rbox("wsframe", (1.5, 0.05, 0.05), (0, CF + 1.12, 0.94), mat=body, bevel=0.015)      # windshield left open (glass glare hid her face)
    C.rbox("dash", (1.56, 0.42, 0.14), (0, CF + 1.32, 0.98), mat=trim, bevel=0.03)
    for sx in (-0.38, 0.38):
        C.rbox("seatback", (0.5, 0.12, 0.32), (sx, CF + 2.62, 0.95), mat=C.pbr("seat", "#3A3F4A", 0.8, bump="weave", bstr=0.2), bevel=0.05)
    # steering wheel (ring + column), tilted towards the driver
    wc = Vector((-0.38, CF + 1.78, 1.08))
    ring = [(wc.x + 0.17 * math.cos(t), wc.y + 0.17 * math.sin(t) * math.sin(math.radians(25)), wc.z + 0.17 * math.sin(t) * math.cos(math.radians(25)))
            for t in [i * 2 * math.pi / 40 for i in range(40)]]
    C.tube("wheelring", ring, 0.018, mat=trim, closed=True)
    C.tube("column", [(wc.x, wc.y, wc.z), (wc.x, wc.y - 0.25, wc.z - 0.1)], 0.03, mat=trim)
    # rear-view mirror at the top of the windshield
    M = Vector((0.0, CF + 1.66, 1.33))
    C.tube("mstem", [(0, M.y - 0.04, 1.41), (0, M.y, M.z + 0.03)], 0.01, mat=trim)
    mh = bpy.data.objects.new("mirror_root", None); bpy.context.scene.collection.objects.link(mh); mh.location = M
    back = C.rbox("mback", (0.27, 0.08, 0.035), (0, 0, -0.02), mat=trim, bevel=0.012); back.parent = mh
    glass = C.rbox("mglass", (0.25, 0.066, 0.004), (0, 0, 0.0), mat=C.pbr("mirror", "#FFFFFF", 0.01, metal=1.0), bevel=0.0); glass.parent = mh
    if mirror_to is not None and eye is not None:
        d1 = (Vector(eye) - M).normalized(); d2 = (Vector(mirror_to) - M).normalized()
        nrm = (d1 + d2).normalized()
        mh.rotation_euler = nrm.to_track_quat("Z", "Y").to_euler()
    return dict(M=M, wheel=wc)


def driver(CF, n):
    """Driver sits behind the wheel (standing figure lowered into the car body; legs are hidden inside it)."""
    h = Hm.build(dict(DRV, loc=(-0.38, CF + 2.32, 0.0), rot_z=0), "man")
    h["rig"].location.z = EYE_DZ - h["eye_c"].z                       # seated: eyes at EYE_DZ, legs hidden inside the car body
    ct = Hm.controls(h)
    h["eye"] = (-0.38 + h["eye_c"].x, CF + 2.32 + h["eye_c"].y, EYE_DZ)
    wc = Vector((-0.38, CF + 1.78, 1.08))
    ct["handR"].location = (wc.x - 0.16, wc.y + 0.02, wc.z + 0.05); ct["handL"].location = (wc.x + 0.16, wc.y + 0.02, wc.z + 0.05)
    Hm.grip(h, "R", 0.75, 0.4); Hm.grip(h, "L", 0.75, 0.4)
    return h, ct


EYE_DZ = 1.17           # driver's eye height when seated


# ------------------------------------------------------------------ shots
HOOKCAM = ((0.42, -2.75, 1.15), (0.45, -0.4, 1.12), 27)
HOOKCAM2 = ((0.41, -2.58, 1.16), (0.45, -0.4, 1.14), 29)


def _front_set(n, phase=0):
    set_stage()
    amb = ambulance(0.0, 0.0, n, phase=phase)
    P.lights((0.3, -1.0, 1.2), key=1100, rim=1200, scale=1.4)
    return amb


def _ped(n):
    h = Hm.build(dict(PED, loc=(0.98, -1.25, 0), rot_z=14), "man"); ct = Hm.controls(h)
    # confused shrug, palms up, forearms forward
    ct["handR"].location = (0.72, -1.52, 1.0); ct["handL"].location = (1.28, -1.5, 1.0)
    Hm.grip(h, "R", 0.15, 0.1); Hm.grip(h, "L", 0.15, 0.1)
    return h, ct


def hook_front(sh, cam, n):
    """Frame 1: mirrored AMBULANCE big on the van's nose, lights flashing, a pedestrian already mid-shrug, head turned to the word."""
    amb = _front_set(n)
    h, ct = _ped(n)
    word = (0.0, -0.1, amb["z"])
    key_obj(ct["look"], 0, loc=word); key_obj(ct["look"], 18, loc=word); key_obj(ct["look"], 30, loc=(HOOKCAM[0][0], HOOKCAM[0][1], 1.6))
    key_obj(ct["look"], n - 20, loc=(HOOKCAM[0][0], HOOKCAM[0][1], 1.6)); key_obj(ct["look"], n - 6, loc=word)
    Hm.face(h["keys"], 0, frown=0.55, brows_inner=0.7, squint=0.35); Hm.face(h["keys"], 30, frown=0.3, browL_up=0.9, brows_inner=0.3, squint=0.1)
    key_obj(ct["handR"], 0, loc=(0.72, -1.52, 1.0)); key_obj(ct["handR"], 14, loc=(0.68, -1.56, 1.08)); key_obj(ct["handR"], 30, loc=(0.72, -1.54, 1.02))
    key_obj(ct["handL"], 0, loc=(1.28, -1.5, 1.0)); key_obj(ct["handL"], 14, loc=(1.32, -1.54, 1.08)); key_obj(ct["handL"], 30, loc=(1.28, -1.52, 1.02))
    life(h, n, 2)
    cam_move(cam, n, HOOKCAM, HOOKCAM2, focus=(0.98, -1.25, 1.55), fstop=5.6)


def loop_q(sh, cam, n):
    """'Did you ever notice?': he looks at us with a raised brow, ends on hook_front's first frame (loop)."""
    amb = _front_set(n)
    h, ct = _ped(n)
    word = (0.0, -0.1, amb["z"])
    key_obj(ct["look"], 0, loc=(HOOKCAM[0][0], HOOKCAM[0][1], 1.6)); key_obj(ct["look"], max(1, n - 10), loc=(HOOKCAM[0][0], HOOKCAM[0][1], 1.6))
    key_obj(ct["look"], n, loc=word)
    Hm.face(h["keys"], 0, browL_up=0.9, smile=0.3, squint=0.15); Hm.face(h["keys"], n, frown=0.55, brows_inner=0.7, squint=0.35, smile=0.0, browL_up=0.0)
    cam_move(cam, n, ((0.4, -2.5, 1.16), (0.45, -0.4, 1.14), 30), HOOKCAM, focus=(0.98, -1.25, 1.55), fstop=5.6)


def back_van(sh, cam, n):
    """'Backwards on the van...': low slow slide along the mirrored word, lights flashing."""
    _front_set(n, phase=1)
    cam_move(cam, n, ((-0.75, -1.55, 0.92), (0.05, 0.0, 0.98), 40), ((0.55, -1.5, 0.95), (-0.05, 0.0, 0.99), 40), focus=(0.0, 0.0, 0.98), fstop=4.0)


def print_flip(sh, cam, n):
    """'So the word is printed flipped': a normal AMBULANCE floats in front of the nose and spins round into the mirrored word."""
    set_stage()
    ambulance(0.0, 0.0, n, phase=1)
    bpy.data.objects["word"].hide_render = True
    P.lights((0.0, -1.0, 1.1), key=1100, rim=1200, scale=1.4)
    root = bpy.data.objects.new("spin", None); bpy.context.scene.collection.objects.link(root)
    t = text3d(WORD, (0, 0, 0), 0.27, C.pbr("word_blue", BLUE, 0.3), name="spinword", extrude=0.012)
    t.parent = root
    ff = W_(sh, "flipped", 1.2)
    key_obj(root, 0, loc=(0, -0.45, 1.02), rot=(0, 0, 0)); key_obj(root, max(1, ff - 8), loc=(0, -0.42, 1.02), rot=(0, 0, 0))
    key_obj(root, ff + 10, loc=(0, -0.2, 1.0), rot=(0, 0, math.radians(180))); key_obj(root, n, loc=(0, -0.03, 0.98), rot=(0, 0, math.radians(180)))
    cam_move(cam, n, ((0.0, -2.2, 1.05), (0.0, 0.0, 0.98), 42), ((0.0, -2.0, 1.05), (0.0, 0.0, 0.98), 44), focus=(0.0, -0.3, 1.0), fstop=5.6)


def spec(sh, cam, n):
    """'The official US ambulance spec even requires it': paramedic beside the nose with a clipboard, points at the mirrored word."""
    amb = _front_set(n, phase=1)
    h = Hm.build(dict(EMT, loc=(-1.0, -1.15, 0), rot_z=-25), "man"); ct = Hm.controls(h)
    board = C.rbox("clipboard", (0.24, 0.012, 0.32), (0, 0, 0), mat=C.pbr("clip", "#8B5E3C", 0.6), bevel=0.006)
    paper = C.rbox("paper", (0.21, 0.004, 0.27), (0, -0.008, -0.01), mat=C.pbr("paper", "#FBF8F0", 0.7)); paper.parent = board
    ct["handL"].location = (-0.8, -1.4, 1.0)         # facing -Y: left hand is on +X (towards the van); clipboard in the right hand
    ct["handR"].location = (-1.2, -1.42, 1.05)
    Hm.grip(h, "R", 0.7, 0.4)
    board.rotation_euler = (math.radians(-20), 0, math.radians(-20)); Hm.hold(h, board, "R")
    fo = W_(sh, "official", 0.3); fr = W_(sh, "requires", 1.8)
    key_obj(ct["handL"], 0, loc=(-0.8, -1.4, 1.0)); key_obj(ct["handL"], fo + 10, loc=(-0.45, -1.15, 1.12)); key_obj(ct["handL"], n, loc=(-0.43, -1.13, 1.14))
    key_obj(ct["look"], 0, loc=(1.0, -3.4, 1.6)); key_obj(ct["look"], fo + 10, loc=(0.0, -0.1, 1.0)); key_obj(ct["look"], fr, loc=(1.0, -3.4, 1.6))
    Hm.face(h["keys"], 0, smile=0.2, brows_up=0.2); Hm.face(h["keys"], fr, smile=0.45, brows_up=0.4)
    life(h, n, 4)
    cam_move(cam, n, ((0.3, -2.9, 1.3), (-0.5, -0.6, 1.15), 34), ((0.28, -2.75, 1.3), (-0.5, -0.6, 1.16), 36), focus=(-1.0, -1.15, 1.5), fstop=5.6)


CF = -2.0                       # car front (car faces -Y); the ambulance stops behind it
AF = CF + 4.1 + 0.65            # ambulance front (stopped close behind)


def _road_set(n, flip=False):
    set_stage(flip=flip)
    h, ct = driver(CF, n)
    amb = ambulance(AF, 0.0, n)
    c = car(CF, n, mirror_to=(0.0, AF, amb["z"]), eye=h["eye"])
    return amb, c, h, ct


def behind_car(sh, cam, n):
    """'It's written for one person': from above the ambulance cab, looking down the road at the car stuck in front."""
    amb, c, h, ct = _road_set(n, flip=True)
    key_obj(ct["look"], 0, loc=(-0.38, CF - 3.0, 1.1))
    P.lights((0.0, CF + 2.0, 1.0), key=1400, rim=900, scale=1.8)
    cam_move(cam, n, ((0.1, AF + 1.0, 1.66), (-0.3, CF + 2.3, 1.15), 55), ((0.1, AF + 0.9, 1.65), (-0.3, CF + 2.3, 1.16), 60), focus=(-0.3, CF + 2.3, 1.1), fstop=8)


def driver_car(sh, cam, n):
    """The driver seen through the windshield; red/blue flashes behind her. On 'screams' she startles."""
    amb, c, h, ct = _road_set(n)
    fs = W_(sh, "screams", 3.0)
    key_obj(ct["look"], 0, loc=(-0.38, CF - 3.0, 1.1)); key_obj(ct["look"], fs, loc=(-0.38, CF - 3.0, 1.1)); key_obj(ct["look"], fs + 6, loc=(-0.25, CF - 3.0, 1.25))
    Hm.face(h["keys"], 0, frown=0.2, squint=0.2); Hm.face(h["keys"], max(1, fs - 2), frown=0.2, squint=0.2)
    Hm.face(h["keys"], fs + 4, wide=0.8, brows_up=0.9, open=0.25, frown=0.0, squint=0.0)
    wc = c["wheel"]
    for sd, dx in (("R", -0.16), ("L", 0.16)):
        key_obj(ct["hand" + sd], 0, loc=(wc.x + dx, wc.y + 0.02, wc.z + 0.05)); key_obj(ct["hand" + sd], fs, loc=(wc.x + dx, wc.y + 0.02, wc.z + 0.05))
        key_obj(ct["hand" + sd], fs + 5, loc=(wc.x + dx * 1.05, wc.y + 0.0, wc.z + 0.08))
    life(h, n, 5)
    P.lights((-0.38, CF + 2.2, 1.1), key=500, rim=400, scale=1.2)
    tg = (-0.38, CF + 2.3, 1.05)
    C.area("dashfill", (-0.38, CF + 1.2, 1.25), (math.radians(-80), 0, 0), 0.4, "#FFF1DC", 60.0)
    cam_move(cam, n, ((0.3, CF + 0.5, 1.32), (-0.38, CF + 2.32, 1.17), 36), ((0.29, CF + 0.62, 1.32), (-0.38, CF + 2.32, 1.18), 40), focus=(-0.38, CF + 2.25, 1.15), fstop=4.0)


def glance_mirror(sh, cam, n):
    """'You glance up... at your mirror': from the passenger side, her eyes go up to the mirror."""
    amb, c, h, ct = _road_set(n)
    fg = W_(sh, "glance", 0.3); fm = W_(sh, "mirror", 1.5)
    key_obj(ct["look"], 0, loc=(-0.3, CF - 3.0, 1.2)); key_obj(ct["look"], fg, loc=(-0.3, CF - 3.0, 1.2)); key_obj(ct["look"], fg + 8, loc=tuple(c["M"]))
    Hm.face(h["keys"], 0, wide=0.5, brows_up=0.5); Hm.face(h["keys"], fg + 8, squint=0.3, brows_inner=0.4, wide=0.0, brows_up=0.1)
    life(h, n, 7, blinks=False)
    P.lights((-0.38, CF + 2.2, 1.1), key=500, rim=400, scale=1.2)
    C.area("dashfill", (-0.1, CF + 1.4, 1.2), (math.radians(-80), 0, 0), 0.4, "#FFF1DC", 50.0)
    cam_move(cam, n, ((0.22, CF + 1.48, 1.17), (-0.36, CF + 2.3, 1.22), 30), ((0.21, CF + 1.52, 1.18), (-0.36, CF + 2.28, 1.23), 32),
             focus=(-0.38, CF + 2.25, 1.15), fstop=4.0)


def reveal_mirror(sh, cam, n):
    """'...in your mirror, it reads AMBULANCE': the driver's own view of the mirror; the real reflection reads the right way round."""
    amb, c, h, ct = _road_set(n)
    for o in bpy.data.objects:                         # the camera sits at her eyes: hide her (the mirror shows the road behind)
        if o.name.startswith("man"):
            o.hide_render = True
    eye = h["eye"]; M = c["M"]
    far = tuple(Vector(eye) + (M - Vector(eye)).normalized() * ((M - Vector(eye)).length + (Vector((0, AF, amb["z"])) - M).length))
    C.area("innerfill", (0.0, CF + 2.6, 1.6), (0, 0, 0), 0.8, "#FFF1DC", 40.0)
    cam_move(cam, n, ((eye[0], eye[1], eye[2]), tuple(M), 118), ((eye[0] + 0.01, eye[1] - 0.05, eye[2] + 0.005), tuple(M), 128),
             focus=far, fstop=64)


def mirror_demo(sh, cam, n):
    """'A mirror flips everything left to right': she holds a card (printed both sides) next to a tall mirror; the card reads AMBULANCE,
    its reflection reads backwards."""
    set_stage(road=False, y0=3.0, top="#2E5E86", bottom="#F0D2A8")
    mx, my = 0.7, 0.32
    fr = C.rbox("mframe", (1.0, 0.06, 1.75), (mx, my + 0.032, 1.0), mat=C.pbr("mframe", "#C9A23A", 0.35, metal=0.6), bevel=0.02)
    C.rbox("mglass", (0.9, 0.004, 1.65), (mx, my, 1.0), mat=C.pbr("mirror", "#FFFFFF", 0.01, metal=1.0), bevel=0.0)
    for sx in (-0.42, 0.42):
        C.rbox("mfoot", (0.06, 0.5, 0.04), (mx + sx, my + 0.03, 0.02), mat=C.pbr("mframe", "#C9A23A", 0.35, metal=0.6), bevel=0.01)
    h = Hm.build(dict(DRV, shirt="#3E7CB1", loc=(-0.35, -0.15, 0), rot_z=10), "man"); ct = Hm.controls(h)
    card = bpy.data.objects.new("card", None); bpy.context.scene.collection.objects.link(card)
    cb = C.rbox("cardboard", (0.62, 0.008, 0.22), (0, 0, 0), mat=C.pbr("card", "#FBF8F0", 0.7), bevel=0.004); cb.parent = card
    a, b = text3d(WORD, (0, -0.006, 0), 0.105, C.pbr("word_blue", BLUE, 0.3), extrude=0.001, name="cardword", both=True)
    a.parent = card; b.parent = card
    b.location = (0, 0.006, 0)
    ff = W_(sh, "flips", 0.5)
    key_obj(card, 0, loc=(0.22, -0.30, 1.25)); key_obj(card, ff, loc=(0.26, -0.30, 1.30))
    ct["handR"].location = (-0.55, -0.35, 0.92)
    key_obj(ct["handL"], 0, loc=(0.0, -0.32, 1.22)); key_obj(ct["handL"], ff, loc=(0.03, -0.32, 1.27))
    Hm.grip(h, "L", 0.6, 0.4)
    key_obj(ct["look"], 0, loc=(0.25, -0.3, 1.25)); key_obj(ct["look"], ff + 15, loc=(mx, my, 1.25)); key_obj(ct["look"], n - 10, loc=(1.6, -3.0, 1.6))
    Hm.face(h["keys"], 0, smile=0.3, brows_up=0.3); Hm.face(h["keys"], ff + 15, brows_up=0.6, wide=0.3); Hm.face(h["keys"], n - 10, smile=0.4, browL_up=0.7)
    life(h, n, 8)
    P.lights((0.1, 0.0, 1.2), key=1000, rim=900, scale=1.1)
    cam_move(cam, n, ((1.5, -1.5, 1.35), (0.45, 0.3, 1.25), 30), ((1.46, -1.4, 1.35), (0.46, 0.3, 1.26), 32), focus=(0.3, -0.1, 1.25), fstop=6.3)


SHOTS = {f.__name__: f for f in (hook_front, behind_car, driver_car, glance_mirror, mirror_demo, print_flip, spec, back_van, reveal_mirror, loop_q)}


if __name__ == "__main__":
    from sr_shot import run
    run(SHOTS, argv)
